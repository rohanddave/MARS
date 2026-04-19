from __future__ import annotations

import logging
from dataclasses import dataclass

from app.llm_client import LLMClient
from app.models.answer import TokenUsage
from app.retriever import ResearchPaperRetriever, RetrievedChunk

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Citation:
    number: int
    chunk_id: str
    source: str
    score: float | None


@dataclass(frozen=True)
class BaselineAgentResult:
    answer: str
    citations: list[Citation]
    retrieved_chunks: list[RetrievedChunk]
    token_usage: TokenUsage


class BaselineAgent:
    def __init__(self, retriever: ResearchPaperRetriever, llm_client: LLMClient) -> None:
        self.retriever = retriever
        self.llm_client = llm_client

    async def answer(self, question: str, top_k: int = 5) -> BaselineAgentResult:
        logger.info("Baseline agent answering question_chars=%s top_k=%s", len(question), top_k)
        chunks = await self.retriever.retrieve(question, top_k=top_k)
        logger.info("Baseline agent retrieved chunks=%s", len(chunks))
        prompt = _build_prompt(question, chunks)
        completion = await self.llm_client.complete(prompt)
        logger.info(
            "Baseline agent completed answer_chars=%s total_tokens=%s citations=%s",
            len(completion.text),
            completion.token_usage.total_tokens,
            len(chunks),
        )

        return BaselineAgentResult(
            answer=completion.text,
            citations=_build_citations(chunks),
            retrieved_chunks=chunks,
            token_usage=completion.token_usage,
        )


def _build_prompt(question: str, chunks: list[RetrievedChunk]) -> str:
    context = _format_context(chunks)
    if not context:
        context = "No retrieved context was available."

    return f"""Answer the question using only the context below.

Rules:
- Cite every factual claim using bracket citations like [1] or [2].
- Use only the provided context. If the context is insufficient, say what is missing.
- Do not invent citations or cite sources that are not listed in the context.
- End with a short "Citations" section that maps each used citation number to its source.

Question:
{question}

Context:
{context}

Answer:
"""


def _format_context(chunks: list[RetrievedChunk]) -> str:
    blocks: list[str] = []
    for index, chunk in enumerate(chunks, start=1):
        source = chunk.metadata.get("source") or chunk.metadata.get("filename") or "unknown source"
        chunk_index = chunk.metadata.get("chunk_index", "unknown")
        score = f"{chunk.score:.4f}" if chunk.score is not None else "unknown"
        blocks.append(
            f"""[{index}]
source: {source}
chunk_id: {chunk.id}
chunk_index: {chunk_index}
score: {score}
text:
{chunk.text}"""
        )
    return "\n\n".join(blocks)


def _build_citations(chunks: list[RetrievedChunk]) -> list[Citation]:
    citations: list[Citation] = []
    for index, chunk in enumerate(chunks, start=1):
        source = chunk.metadata.get("source") or chunk.metadata.get("filename") or "unknown source"
        citations.append(
            Citation(
                number=index,
                chunk_id=chunk.id,
                source=str(source),
                score=chunk.score,
            )
        )
    return citations
