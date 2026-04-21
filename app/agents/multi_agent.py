from __future__ import annotations

import logging
import re
from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass, field
from typing import Any, Literal

from app.llm_client import LLMClient
from app.models.answer import TokenUsage
from app.retriever import ResearchPaperRetriever, RetrievedChunk

logger = logging.getLogger(__name__)

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
        max_evidence_chunks: int = 8,
    ) -> None:
        if max_evidence_chunks <= 0:
            raise ValueError("max_evidence_chunks must be greater than 0")
        self.llm_client = llm_client
        self.search_agent = search_agent
        self.summarization_agent = summarization_agent
        self.fact_checking_agent = fact_checking_agent
        self.final_synthesis_agent = final_synthesis_agent
        self.max_evidence_chunks = max_evidence_chunks

    async def answer(self, query: str, top_k: int = 5) -> MultiAgentAnswer:
        logger.info("Orchestrator starting query_chars=%s top_k=%s", len(query), top_k)
        plan, planning_usage = await self.plan(query)
        logger.info(
            "Orchestrator plan query_type=%s subquestions=%s use_web=%s",
            plan.query_type,
            len(plan.subquestions),
            plan.use_web,
        )
        evidence, search_usage = await self.search_agent.search(query, plan, top_k=top_k)
        logger.info("Orchestrator search complete evidence=%s", len(evidence))
        selected_evidence = self._select_evidence_for_summarization(evidence)
        evidence_notes, summary_usage = await self.summarization_agent.summarize(selected_evidence)
        logger.info("Orchestrator summarization complete notes=%s", len(evidence_notes))
        draft_answer, draft_usage = await self.final_synthesis_agent.write_answer(
            query=query,
            evidence_notes=evidence_notes,
            fact_check=None,
            draft=True,
        )
        logger.info("Orchestrator draft synthesis complete answer_chars=%s", len(draft_answer))
        fact_check, fact_usage = await self.fact_checking_agent.check(draft_answer, evidence_notes)
        logger.info(
            "Orchestrator fact check complete checks=%s needs_more_retrieval=%s",
            len(fact_check.checks),
            fact_check.needs_more_retrieval,
        )

        if fact_check.needs_more_retrieval and fact_check.suggested_queries:
            logger.info("Orchestrator running extra retrieval queries=%s", len(fact_check.suggested_queries))
            extra_evidence, extra_search_usage = await self.search_agent.search_queries(
                fact_check.suggested_queries,
                top_k=max(1, min(3, top_k)),
                use_web=plan.use_web,
            )
            evidence = _dedupe_evidence([*evidence, *extra_evidence])
            selected_evidence = self._select_evidence_for_summarization(evidence)
            evidence_notes, extra_summary_usage = await self.summarization_agent.summarize(selected_evidence)
            draft_answer, extra_draft_usage = await self.final_synthesis_agent.write_answer(
                query=query,
                evidence_notes=evidence_notes,
                fact_check=fact_check,
                draft=True,
            )
            fact_check, extra_fact_usage = await self.fact_checking_agent.check(draft_answer, evidence_notes)
            logger.info("Orchestrator extra retrieval complete total_evidence=%s notes=%s", len(evidence), len(evidence_notes))
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
            draft=False,
        )
        logger.info("Orchestrator final synthesis complete answer_chars=%s total_tokens=%s", len(final_answer), _sum_usage(token_usage, final_usage).total_tokens)

        return MultiAgentAnswer(
            answer=final_answer,
            plan=plan,
            evidence=evidence,
            evidence_notes=evidence_notes,
            fact_check=fact_check,
            token_usage=_sum_usage(token_usage, final_usage),
        )

    def _select_evidence_for_summarization(self, evidence: list[Evidence]) -> list[Evidence]:
        selected = evidence[: self.max_evidence_chunks]
        if len(evidence) > len(selected):
            logger.info(
                "Capped evidence for summarization selected=%s available=%s",
                len(selected),
                len(evidence),
            )
        return selected

    async def plan(self, query: str) -> tuple[QueryPlan, TokenUsage]:
        logger.info("Planning query query_chars=%s", len(query))
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
        logger.info("Planning complete query_type=%s subquestions=%s", plan.query_type, len(plan.subquestions))
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
        logger.info("Search agent starting top_k=%s plan_subquestions=%s", top_k, len(plan.subquestions))
        search_queries, usage = await self.generate_search_queries(query, plan)
        logger.info("Search agent generated queries=%s", len(search_queries))
        evidence, _ = await self.search_queries(search_queries, top_k=top_k, use_web=plan.use_web)
        logger.info("Search agent complete evidence=%s", len(evidence))
        return evidence, usage

    async def generate_search_queries(self, query: str, plan: QueryPlan) -> tuple[list[str], TokenUsage]:
        logger.info("Generating search queries query_chars=%s subquestions=%s", len(query), len(plan.subquestions))
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
        queries = _dedupe_strings(queries)
        logger.info("Generated search queries count=%s", len(queries))
        return queries, completion.token_usage

    async def search_queries(self, queries: list[str], top_k: int = 5, use_web: bool = False) -> tuple[list[Evidence], TokenUsage]:
        logger.info("Searching queries count=%s top_k=%s use_web=%s", len(queries), top_k, use_web)
        evidence: list[Evidence] = []
        for query in queries:
            logger.info("Searching corpus query_chars=%s", len(query))
            chunks = await self.retriever.retrieve(query, top_k=top_k)
            if use_web and self.web_retriever is not None:
                logger.info("Searching web query_chars=%s top_k=%s", len(query), top_k)
                chunks = [*chunks, *await self.web_retriever(query, top_k)]
            evidence.extend(_chunks_to_evidence(query, chunks))
        ranked = self.rank_evidence(_dedupe_evidence(evidence))
        logger.info("Search queries complete raw_evidence=%s ranked_evidence=%s", len(evidence), len(ranked))
        return ranked, TokenUsage()

    def rank_evidence(self, evidence: list[Evidence]) -> list[Evidence]:
        return sorted(evidence, key=lambda item: item.score if item.score is not None else -1.0, reverse=True)


class SummarizationAgent:
    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client

    async def summarize(self, evidence: list[Evidence]) -> tuple[list[EvidenceNote], TokenUsage]:
        logger.info("Summarization agent starting evidence=%s", len(evidence))
        notes: list[EvidenceNote] = []
        total_usage = TokenUsage()

        for item in evidence:
            logger.debug("Summarizing evidence citation_id=%s source=%s text_chars=%s", item.citation_id, item.source, len(item.text))
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

        logger.info("Summarization agent complete notes=%s total_tokens=%s", len(notes), total_usage.total_tokens)
        return notes, total_usage


class FactCheckingAgent:
    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client

    async def check(self, draft_answer: str, evidence_notes: list[EvidenceNote]) -> tuple[FactCheckReport, TokenUsage]:
        logger.info("Fact checking draft answer_chars=%s evidence_notes=%s", len(draft_answer), len(evidence_notes))
        prompt = f"""Inspect this draft answer claim by claim against the evidence notes before the final answer is written.

Use strict definitions:
- supported: the claim has at least one citation and the cited evidence directly supports the claim.
- weakly_supported: the claim has a citation, but the evidence is indirect, incomplete, ambiguous, or only partially supports it.
- unsupported: the claim has no citation, cites missing evidence, contradicts the evidence, or cannot be verified from the notes.

Check every factual sentence. Do not give credit for a paragraph-level citation if a factual sentence itself lacks a citation.
Ask for more retrieval if evidence is missing.
When useful, recommend how the final answer should revise or remove weak/unsupported claims.

Draft answer:
{draft_answer}

Evidence notes:
{_format_notes(evidence_notes)}
"""
        completion = await self.llm_client.complete(prompt)
        report = _build_fact_check_report(draft_answer, evidence_notes, completion.text)
        logger.info(
            "Fact check complete checks=%s needs_more_retrieval=%s suggested_queries=%s",
            len(report.checks),
            report.needs_more_retrieval,
            len(report.suggested_queries),
        )
        return report, completion.token_usage


class FinalSynthesisAgent:
    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client

    async def write_answer(
        self,
        query: str,
        evidence_notes: list[EvidenceNote],
        fact_check: FactCheckReport | None,
        draft: bool = False,
    ) -> tuple[str, TokenUsage]:
        logger.info(
            "Final synthesis starting query_chars=%s evidence_notes=%s has_fact_check=%s draft=%s",
            len(query),
            len(evidence_notes),
            fact_check is not None,
            draft,
        )
        answer_kind = "draft answer" if draft else "final answer"
        prompt = f"""Write a clean {answer_kind} to the question using the evidence notes.

Requirements:
- Every factual sentence must include at least one evidence citation like [E1] or [E2].
- Do not place citations only at the end of a paragraph; cite each factual sentence individually.
- Put the citation immediately after the specific factual claim it supports.
- Avoid citation dumps like [E1][E2][E3] unless every cited source directly supports that exact sentence.
- Prefer one or two precise citations per factual sentence over many broad citations.
- If no evidence supports a sentence, remove it or state the uncertainty with a citation to the closest relevant evidence.
- Include uncertainty when evidence is weak, missing, or conflicting.
- Do not use facts that are not supported by the evidence notes.
- If the evidence is insufficient, say what is missing.
- Do not invent evidence references. Only cite IDs that appear in the evidence notes.
- Avoid broad comparative or causal claims unless directly supported by cited evidence.

Citation discipline examples:
- Good: REALM uses a learned textual retriever to retrieve documents before prediction [E2].
- Bad: REALM uses retrieval and improves QA. [E2][E5]
- Good: The provided evidence does not include a direct ORQA comparison, so that comparison cannot be verified from these notes [E4].
- Bad: REALM outperforms ORQA because retrieval improves QA [E1][E2][E3].

Question:
{query}

Evidence notes:
{_format_notes(evidence_notes)}

Fact check feedback:
{fact_check.report_text if fact_check else "No fact check feedback yet."}

Final answer:
"""
        completion = await self.llm_client.complete(prompt)
        logger.info("Final synthesis complete answer_chars=%s total_tokens=%s", len(completion.text), completion.token_usage.total_tokens)
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
                citation_id=f"E{index}",
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
        status: ClaimStatus = "supported" if claim_refs else "unsupported"
        if "not configured" in claim.lower() or "insufficient" in claim.lower():
            status = "unsupported"
        checks.append(
            ClaimCheck(
                claim=claim,
                status=status,
                evidence_refs=claim_refs,
                note="Claim has explicit evidence references." if claim_refs else "No sentence-level evidence reference found.",
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
