from __future__ import annotations

import re
from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass, field
from typing import Any, Literal

from app.llm_client import LLMClient
from app.models.answer import TokenUsage
from app.retriever import ResearchPaperRetriever, RetrievedChunk

ClaimStatus = Literal["supported", "weakly_supported", "unsupported"]


@dataclass(frozen=True)
class QueryPlan:
    query_type: str
    subquestions: list[str]
    use_web: bool
    agent_order: list[str]
    reasoning: str


@dataclass(frozen=True)
class Evidence:
    citation_id: str
    query: str
    chunk_id: str
    source: str
    text: str
    score: float | None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class EvidenceNote:
    citation_id: str
    source: str
    key_claims: list[str]
    numbers: list[str]
    supporting_statements: list[str]
    summary: str


@dataclass(frozen=True)
class ClaimCheck:
    claim: str
    status: ClaimStatus
    evidence_refs: list[str]
    note: str


@dataclass(frozen=True)
class FactCheckReport:
    checks: list[ClaimCheck]
    needs_more_retrieval: bool
    suggested_queries: list[str]
    report_text: str


@dataclass(frozen=True)
class MultiAgentAnswer:
    answer: str
    plan: QueryPlan
    evidence: list[Evidence]
    evidence_notes: list[EvidenceNote]
    fact_check: FactCheckReport
    token_usage: TokenUsage


class OrchestratorAgent:
    def __init__(
        self,
        llm_client: LLMClient,
        search_agent: "SearchAgent",
        summarization_agent: "SummarizationAgent",
        fact_checking_agent: "FactCheckingAgent",
        final_synthesis_agent: "FinalSynthesisAgent",
    ) -> None:
        self.llm_client = llm_client
        self.search_agent = search_agent
        self.summarization_agent = summarization_agent
        self.fact_checking_agent = fact_checking_agent
        self.final_synthesis_agent = final_synthesis_agent

    async def answer(self, query: str, top_k: int = 5) -> MultiAgentAnswer:
        plan, planning_usage = await self.plan(query)
        evidence, search_usage = await self.search_agent.search(query, plan, top_k=top_k)
        evidence_notes, summary_usage = await self.summarization_agent.summarize(evidence)
        draft_answer, draft_usage = await self.final_synthesis_agent.write_answer(
            query=query,
            evidence_notes=evidence_notes,
            fact_check=None,
        )
        fact_check, fact_usage = await self.fact_checking_agent.check(draft_answer, evidence_notes)

        if fact_check.needs_more_retrieval and fact_check.suggested_queries:
            extra_evidence, extra_search_usage = await self.search_agent.search_queries(
                fact_check.suggested_queries,
                top_k=max(1, min(3, top_k)),
                use_web=plan.use_web,
            )
            evidence = _dedupe_evidence([*evidence, *extra_evidence])
            extra_notes, extra_summary_usage = await self.summarization_agent.summarize(extra_evidence)
            evidence_notes = _dedupe_notes([*evidence_notes, *extra_notes])
            draft_answer, extra_draft_usage = await self.final_synthesis_agent.write_answer(
                query=query,
                evidence_notes=evidence_notes,
                fact_check=fact_check,
            )
            fact_check, extra_fact_usage = await self.fact_checking_agent.check(draft_answer, evidence_notes)
            token_usage = _sum_usage(
                planning_usage,
                search_usage,
                summary_usage,
                draft_usage,
                fact_usage,
                extra_search_usage,
                extra_summary_usage,
                extra_draft_usage,
                extra_fact_usage,
            )
        else:
            token_usage = _sum_usage(planning_usage, search_usage, summary_usage, draft_usage, fact_usage)

        final_answer, final_usage = await self.final_synthesis_agent.write_answer(
            query=query,
            evidence_notes=evidence_notes,
            fact_check=fact_check,
        )

        return MultiAgentAnswer(
            answer=final_answer,
            plan=plan,
            evidence=evidence,
            evidence_notes=evidence_notes,
            fact_check=fact_check,
            token_usage=_sum_usage(token_usage, final_usage),
        )

    async def plan(self, query: str) -> tuple[QueryPlan, TokenUsage]:
        prompt = f"""Classify this research-paper QA query and make a short retrieval plan.

Return plain text with these fields:
query_type: one of simple, comparative, multi_part, methodological, factual
subquestions: semicolon-separated subquestions
use_web: yes or no
reasoning: one sentence

Query:
{query}
"""
        completion = await self.llm_client.complete(prompt)
        plan = _parse_plan(query, completion.text)
        return plan, completion.token_usage


class SearchAgent:
    def __init__(
        self,
        retriever: ResearchPaperRetriever,
        llm_client: LLMClient,
        web_retriever: Callable[[str, int], Awaitable[list[RetrievedChunk]]] | None = None,
    ) -> None:
        self.retriever = retriever
        self.llm_client = llm_client
        self.web_retriever = web_retriever

    async def search(self, query: str, plan: QueryPlan, top_k: int = 5) -> tuple[list[Evidence], TokenUsage]:
        search_queries, usage = await self.generate_search_queries(query, plan)
        evidence, _ = await self.search_queries(search_queries, top_k=top_k, use_web=plan.use_web)
        return evidence, usage

    async def generate_search_queries(self, query: str, plan: QueryPlan) -> tuple[list[str], TokenUsage]:
        prompt = f"""Generate concise semantic search queries for retrieving evidence from research papers.
Return one query per line. Avoid numbering.

Original query:
{query}

Subquestions:
{chr(10).join(plan.subquestions)}
"""
        completion = await self.llm_client.complete(prompt)
        queries = _parse_lines(completion.text)
        if not queries or _looks_unconfigured(completion.text):
            queries = [query, *plan.subquestions]
        return _dedupe_strings(queries), completion.token_usage

    async def search_queries(self, queries: list[str], top_k: int = 5, use_web: bool = False) -> tuple[list[Evidence], TokenUsage]:
        evidence: list[Evidence] = []
        for query in queries:
            chunks = await self.retriever.retrieve(query, top_k=top_k)
            if use_web and self.web_retriever is not None:
                chunks = [*chunks, *await self.web_retriever(query, top_k)]
            evidence.extend(_chunks_to_evidence(query, chunks))
        return self.rank_evidence(_dedupe_evidence(evidence)), TokenUsage()

    def rank_evidence(self, evidence: list[Evidence]) -> list[Evidence]:
        return sorted(evidence, key=lambda item: item.score if item.score is not None else -1.0, reverse=True)


class SummarizationAgent:
    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client

    async def summarize(self, evidence: list[Evidence]) -> tuple[list[EvidenceNote], TokenUsage]:
        notes: list[EvidenceNote] = []
        total_usage = TokenUsage()

        for item in evidence:
            prompt = f"""Create a short evidence note for this source.

Extract:
- key claims
- numbers or measurements
- supporting statements

Use only the text below.

Citation: {item.citation_id}
Source: {item.source}
Text:
{item.text}
"""
            completion = await self.llm_client.complete(prompt)
            total_usage = _sum_usage(total_usage, completion.token_usage)
            notes.append(_build_evidence_note(item, completion.text))

        return notes, total_usage


class FactCheckingAgent:
    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client

    async def check(self, draft_answer: str, evidence_notes: list[EvidenceNote]) -> tuple[FactCheckReport, TokenUsage]:
        prompt = f"""Inspect this draft answer claim by claim against the evidence notes.

For each important claim, mark it supported, weakly_supported, or unsupported.
Ask for more retrieval if evidence is missing.

Draft answer:
{draft_answer}

Evidence notes:
{_format_notes(evidence_notes)}
"""
        completion = await self.llm_client.complete(prompt)
        return _build_fact_check_report(draft_answer, evidence_notes, completion.text), completion.token_usage


class FinalSynthesisAgent:
    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client

    async def write_answer(
        self,
        query: str,
        evidence_notes: list[EvidenceNote],
        fact_check: FactCheckReport | None,
    ) -> tuple[str, TokenUsage]:
        prompt = f"""Write a clean final answer to the question using the evidence notes.

Requirements:
- Cite claims with evidence references like [E1], [E2].
- Include uncertainty when evidence is weak, missing, or conflicting.
- Do not use facts that are not supported by the evidence notes.
- If the evidence is insufficient, say what is missing.

Question:
{query}

Evidence notes:
{_format_notes(evidence_notes)}

Fact check feedback:
{fact_check.report_text if fact_check else "No fact check feedback yet."}

Final answer:
"""
        completion = await self.llm_client.complete(prompt)
        return completion.text, completion.token_usage


def _parse_plan(query: str, text: str) -> QueryPlan:
    lower_text = text.lower()
    query_type = _field_value(text, "query_type") or _heuristic_query_type(query)
    subquestions = _split_subquestions(_field_value(text, "subquestions") or "")
    if not subquestions or _looks_unconfigured(text):
        subquestions = _heuristic_subquestions(query)

    use_web_value = _field_value(text, "use_web") or "no"
    use_web = use_web_value.strip().lower() in {"yes", "true", "1"} or "web" in lower_text
    reasoning = _field_value(text, "reasoning") or "Use corpus retrieval, summarize evidence, fact check, then synthesize."

    return QueryPlan(
        query_type=query_type,
        subquestions=subquestions,
        use_web=use_web,
        agent_order=["search", "summarization", "draft_synthesis", "fact_check", "final_synthesis"],
        reasoning=reasoning,
    )


def _chunks_to_evidence(query: str, chunks: list[RetrievedChunk]) -> list[Evidence]:
    evidence: list[Evidence] = []
    for index, chunk in enumerate(chunks, start=1):
        source = chunk.metadata.get("source") or chunk.metadata.get("filename") or "unknown source"
        evidence.append(
            Evidence(
                citation_id=f"E{len(evidence) + index}",
                query=query,
                chunk_id=chunk.id,
                source=str(source),
                text=chunk.text,
                score=chunk.score,
                metadata=chunk.metadata,
            )
        )
    return evidence


def _build_evidence_note(evidence: Evidence, llm_note: str) -> EvidenceNote:
    text = evidence.text
    sentences = _sentences(text)
    numbers = re.findall(r"\b\d+(?:\.\d+)?%?\b", text)
    summary = llm_note.strip()
    if not summary or _looks_unconfigured(summary):
        summary = " ".join(sentences[:2]).strip()

    return EvidenceNote(
        citation_id=evidence.citation_id,
        source=evidence.source,
        key_claims=sentences[:3],
        numbers=numbers[:10],
        supporting_statements=sentences[:5],
        summary=summary,
    )


def _build_fact_check_report(
    draft_answer: str,
    evidence_notes: list[EvidenceNote],
    llm_report: str,
) -> FactCheckReport:
    refs = {note.citation_id for note in evidence_notes}
    claims = _sentences(draft_answer)
    checks: list[ClaimCheck] = []

    for claim in claims[:12]:
        claim_refs = sorted(ref for ref in refs if f"[{ref}]" in claim)
        status: ClaimStatus = "supported" if claim_refs else "weakly_supported"
        if "not configured" in claim.lower() or "insufficient" in claim.lower():
            status = "unsupported"
        checks.append(
            ClaimCheck(
                claim=claim,
                status=status,
                evidence_refs=claim_refs,
                note="Claim has explicit evidence references." if claim_refs else "No explicit evidence reference found.",
            )
        )

    needs_more_retrieval = any(check.status == "unsupported" for check in checks)
    suggested_queries = _unsupported_claim_queries(checks)
    report_text = llm_report.strip()
    if not report_text or _looks_unconfigured(report_text):
        report_text = "\n".join(f"- {check.status}: {check.claim}" for check in checks)

    return FactCheckReport(
        checks=checks,
        needs_more_retrieval=needs_more_retrieval,
        suggested_queries=suggested_queries,
        report_text=report_text,
    )


def _format_notes(notes: list[EvidenceNote]) -> str:
    blocks: list[str] = []
    for note in notes:
        blocks.append(
            f"""[{note.citation_id}]
source: {note.source}
summary: {note.summary}
key_claims: {"; ".join(note.key_claims)}
numbers: {", ".join(note.numbers)}
supporting_statements: {"; ".join(note.supporting_statements)}"""
        )
    return "\n\n".join(blocks) if blocks else "No evidence notes available."


def _field_value(text: str, field_name: str) -> str | None:
    match = re.search(rf"^{re.escape(field_name)}\s*:\s*(.+)$", text, flags=re.IGNORECASE | re.MULTILINE)
    return match.group(1).strip() if match else None


def _heuristic_query_type(query: str) -> str:
    lower_query = query.lower()
    if any(term in lower_query for term in ("compare", "contrast", "versus", " vs ")):
        return "comparative"
    if any(term in lower_query for term in (" and ", "also", "as well as")):
        return "multi_part"
    if any(term in lower_query for term in ("method", "algorithm", "approach", "experiment")):
        return "methodological"
    return "factual"


def _heuristic_subquestions(query: str) -> list[str]:
    parts = re.split(r"\s+(?:and|also|as well as)\s+", query)
    cleaned = [part.strip(" ?.") for part in parts if part.strip(" ?.")]
    return cleaned if len(cleaned) > 1 else [query]


def _split_subquestions(value: str) -> list[str]:
    return [item.strip(" -.") for item in re.split(r";|\n", value) if item.strip(" -.")]


def _parse_lines(text: str) -> list[str]:
    lines = []
    for line in text.splitlines():
        cleaned = re.sub(r"^\s*(?:[-*]|\d+[.)])\s*", "", line).strip()
        if cleaned and ":" not in cleaned[:18]:
            lines.append(cleaned)
    return lines


def _sentences(text: str) -> list[str]:
    return [sentence.strip() for sentence in re.split(r"(?<=[.!?])\s+", text.strip()) if sentence.strip()]


def _unsupported_claim_queries(checks: list[ClaimCheck]) -> list[str]:
    queries = [check.claim for check in checks if check.status == "unsupported"]
    return queries[:3]


def _dedupe_strings(values: list[str]) -> list[str]:
    seen: set[str] = set()
    deduped: list[str] = []
    for value in values:
        key = value.lower()
        if key not in seen:
            seen.add(key)
            deduped.append(value)
    return deduped


def _dedupe_evidence(evidence: list[Evidence]) -> list[Evidence]:
    seen: set[str] = set()
    deduped: list[Evidence] = []
    for item in evidence:
        if item.chunk_id in seen:
            continue
        seen.add(item.chunk_id)
        deduped.append(item)
    return [
        Evidence(
            citation_id=f"E{index}",
            query=item.query,
            chunk_id=item.chunk_id,
            source=item.source,
            text=item.text,
            score=item.score,
            metadata=item.metadata,
        )
        for index, item in enumerate(deduped, start=1)
    ]


def _dedupe_notes(notes: list[EvidenceNote]) -> list[EvidenceNote]:
    seen: set[str] = set()
    deduped: list[EvidenceNote] = []
    for note in notes:
        if note.citation_id in seen:
            continue
        seen.add(note.citation_id)
        deduped.append(note)
    return deduped


def _sum_usage(*usages: TokenUsage) -> TokenUsage:
    return TokenUsage(
        input_tokens=sum(usage.input_tokens or 0 for usage in usages),
        output_tokens=sum(usage.output_tokens or 0 for usage in usages),
        total_tokens=sum(usage.total_tokens or 0 for usage in usages),
    )


def _looks_unconfigured(text: str) -> bool:
    return "llm answering is not configured" in text.lower()
