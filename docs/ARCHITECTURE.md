# MARS-1 — System Architecture & Technical Reference

> **What this document covers:** How the system is built — the data pipeline (PDF ingestion, chunking, embedding, vector storage), both agent implementations (single-agent baseline and five-agent multi-agent pipeline), concurrency design, configuration options, output file formats, and all design decisions and bug fixes made during development.

---

## Table of Contents

1. [System Architecture](#1-system-architecture)
2. [Data Pipeline](#2-data-pipeline)
3. [Agent Systems](#3-agent-systems)
   - [Single-Agent Baseline](#single-agent-baseline)
   - [Multi-Agent Pipeline](#multi-agent-pipeline)
4. [Concurrency Model](#4-concurrency-model)
5. [Configuration Reference](#5-configuration-reference)
6. [Output Artifacts](#6-output-artifacts)
7. [Design Decisions and Trade-offs](#7-design-decisions-and-trade-offs)
8. [Robustness Fixes](#8-robustness-fixes)
9. [File Reference](#9-file-reference)

---

## 1. System Architecture

```
Research PDFs (data/)
        │
        ▼
  PDFTextReader          — extracts text page-by-page via pypdf
        │
        ▼
ResearchPaperIngestor    — chunks text (4000 chars, 400 overlap), checks manifest cache
        │
        ▼
  OpenAIEmbedder         — local sentence-transformers (BAAI/bge-large-en-v1.5) → 1024-dim vectors
        │
        ▼
PineconeVectorStore      — gRPC Pinecone local instance (port 5080 via Docker)

─────────────────────────────── At query time ────────────────────────────────

   Question
        │
        ▼
ResearchPaperRetriever   — embed query → Pinecone top-k similarity search
        │
        ├──────────────────────────┐
        ▼                          ▼
  BaselineAgent            OrchestratorAgent
  (single prompt)          (5-stage pipeline)
        │                          │
        ▼                          ▼
  baseline_answer         multi_agent_answer
        │                          │
        └──────────┬───────────────┘
                   ▼
         External Judge LLM
                   │
                   ▼
        Scores, plots, answers saved to res/
```

---

## 2. Data Pipeline

### PDF Ingestion (`app/ingestor.py`)

`ResearchPaperIngestor` processes all PDFs under `data/`:

1. **Text extraction:** `PDFTextReader` (`app/file_reader.py`) reads each page using `pypdf` and concatenates the text.
2. **Chunking:** Each document is split into overlapping 4000-character chunks with a 400-character overlap. This preserves sentence context across chunk boundaries.
3. **Embedding:** `OpenAIEmbedder` (`app/embedder.py`) uses sentence-transformers (`BAAI/bge-large-en-v1.5`) locally to produce a 1024-dimensional vector per chunk.
4. **Indexing:** Chunks and their embeddings are upserted into Pinecone via gRPC. Each record stores the chunk text, source filename, chunk index, and chunk ID as metadata.

### Caching

Two levels of caching avoid re-processing on reruns:

| Cache | Location | Purpose |
|-------|----------|---------|
| Ingestion manifest | `data/.ingestion_manifest.json` | Tracks which PDF files have been fully indexed. Files present here are skipped entirely. |
| Embedding cache | `data/.embedding_cache/` | Stores chunk-level embedding results. Avoids re-calling the Embeddings API for already-embedded chunks. |

A file is added to the manifest only after all its chunks have been successfully indexed — ensuring the cache is never in a partial state.

### Retrieval (`app/retriever.py`)

`ResearchPaperRetriever` takes a text query, embeds it using the same `OpenAIEmbedder`, and asks Pinecone for the top-k most similar chunks by cosine similarity. The retrieved chunks include their text, metadata, and similarity score. Both the baseline and the multi-agent system use the same retriever, ensuring a fair comparison.

---

## 3. Agent Systems

### Single-Agent Baseline

**File:** `app/agents/baseline.py`

The baseline (`BaselineAgent`) implements a standard single-step RAG pattern:

1. Retrieve the top-k chunks for the question.
2. Format all chunks as numbered context blocks (with source, chunk ID, and similarity score).
3. Pass question + all context into one LLM prompt.
4. The LLM is instructed to cite every factual claim with bracket citations `[1]`, `[2]`, etc., and end with a Citations section.

The baseline intentionally uses a single prompt to represent what a typical production RAG assistant does. All complexity is left to the LLM.

**Output:** `BaselineAgentResult` — answer text, list of `Citation` objects, retrieved chunks, token usage.

---

### Multi-Agent Pipeline

**File:** `app/agents/multi_agent.py`

The multi-agent system runs five sequential stages, each implemented as a separate agent class with its own LLM client (which may use a different model).

#### Stage 1: OrchestratorAgent — Planning

Classifies the query and produces a `QueryPlan`:
- `query_type`: one of `simple`, `comparative`, `multi_part`, `methodological`, `factual`
- `subquestions`: sub-parts of the query for targeted retrieval
- `use_web`: whether web retrieval is needed (always `no` in current experiments)
- `agent_order`: fixed sequence — search → summarization → draft → fact-check → final synthesis

Parsing uses regex against the LLM's plain-text response, with heuristic fallbacks if the LLM output is malformed.

#### Stage 2: SearchAgent — Evidence Retrieval

Given the original query and the plan:
1. Calls an LLM to generate multiple semantic search queries (one per line) from the original question and its subquestions.
2. Retrieves top-k chunks from Pinecone for **each** generated search query.
3. Deduplicates chunks by `chunk_id`.
4. Re-ranks remaining evidence by similarity score (descending).

If the fact-check stage later identifies unsupported claims and requests more retrieval, `SearchAgent.search_queries()` is called again with up to 3 additional queries.

#### Stage 3: SummarizationAgent — Evidence Compression

For each retrieved chunk (up to `max_evidence_chunks`, capped at `top_k`):
1. Sends chunk text to the LLM with a prompt asking it to extract key claims, numbers, and supporting statements.
2. Also extracts numbers with regex and splits sentences heuristically.
3. Produces an `EvidenceNote` per chunk.

The evidence cap ensures both systems operate within the same retrieval budget.

#### Stage 4: FinalSynthesisAgent — Draft Answer

Writes an initial answer from the evidence notes. Uses a strict citation discipline prompt:
- Every factual sentence must include at least one inline citation like `[E1]` or `[E2]`.
- Citations must immediately follow the specific claim they support — not dumped at the end of a paragraph.
- Vague multi-citation dumps like `[E1][E2][E3]` are explicitly discouraged.

#### Stage 5: FactCheckingAgent — Claim Verification

Inspects the draft answer sentence-by-sentence against the evidence notes. Classifies each claim as:
- `supported` — claim has an inline citation that directly supports it
- `weakly_supported` — citation present but evidence is indirect or incomplete
- `unsupported` — no citation, cites missing evidence, or contradicts evidence

If any unsupported claims are found, `needs_more_retrieval = True` and up to 3 suggested follow-up queries are extracted from those claims. The orchestrator then runs a second retrieval pass, re-summarizes, re-drafts, and re-checks before the final synthesis.

#### Stage 6: FinalSynthesisAgent — Final Answer

Runs again with the same prompt but with the fact-check report included as feedback. The LLM is instructed to revise or remove weak/unsupported claims and include uncertainty language when evidence is missing.

**Output:** `MultiAgentAnswer` — final answer text, `QueryPlan`, `list[Evidence]`, `list[EvidenceNote]`, `FactCheckReport`, aggregated `TokenUsage` across all stages.

---

#### Multi-Agent Flow Summary

```
Query
  │
  ├─ OrchestratorAgent.plan()           → QueryPlan
  │
  ├─ SearchAgent.search()               → list[Evidence]  (ranked, deduped)
  │
  ├─ [cap evidence at max_evidence_chunks]
  │
  ├─ SummarizationAgent.summarize()     → list[EvidenceNote]
  │
  ├─ FinalSynthesisAgent.write_answer(draft=True) → draft_answer
  │
  ├─ FactCheckingAgent.check()          → FactCheckReport
  │     │
  │     └─ if needs_more_retrieval:
  │           SearchAgent.search_queries()      (extra retrieval)
  │           SummarizationAgent.summarize()    (re-summarize)
  │           FinalSynthesisAgent.write_answer(draft=True)  (re-draft)
  │           FactCheckingAgent.check()          (re-check)
  │
  └─ FinalSynthesisAgent.write_answer(draft=False) → final_answer
```

---

## 4. Concurrency Model

```
main() — sequential
  │
  ├─ ingest data (sequential)
  │
  └─ for each experiment (sequential):
         │
         ├─ asyncio.gather(*run_question(i) for i in 1..15)
         │    │
         │    └─ each question: asyncio.gather(baseline.answer(), orchestrator.answer())
         │         (baseline and multi-agent run concurrently per question)
         │
         └─ judge_experiment_results()
               │
               └─ asyncio.gather(*judge_with_limit(q, system) for all 30 pairs)
                    (bounded by JUDGE_CONCURRENCY semaphore)
```

Key design choices:
- **Experiments are sequential** — results are written deterministically and don't interfere.
- **Questions within an experiment are parallel** — controlled by `QUESTION_CONCURRENCY` semaphore (default 3).
- **Baseline and multi-agent run concurrently per question** — via `asyncio.gather`, so per-question latency is the max of the two, not the sum.
- **Judge calls are parallel** — 30 judge calls per experiment (15 questions × 2 systems), bounded by `JUDGE_CONCURRENCY` semaphore (default 4).
- **A global `_PRINT_LOCK`** serializes stdout output so concurrent question results don't interleave.

---

## 5. Configuration Reference

### Required

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI API key |

### Optional — Models

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_ANSWER_MODEL` | `google/gemma-4-26B-A4B-it` | Default model for all agents and baseline |
| `FAST_AGENT_MODEL` | `OPENAI_ANSWER_MODEL` | Small model used in ablation experiments |
| `STRONG_AGENT_MODEL` | `OPENAI_ANSWER_MODEL` | Strong model used in ablation experiments |
| `JUDGE_MODEL` | `google/gemma-4-26B-A4B-it` | Model used to evaluate answers |

Per-role overrides (rarely needed — the experiment configs set these directly):

`BASELINE_MODEL`, `ORCHESTRATOR_MODEL`, `SEARCH_MODEL`, `SUMMARIZATION_MODEL`, `FACT_CHECK_MODEL`, `FINAL_SYNTHESIS_MODEL`

### Optional — Concurrency

| Variable | Default | Description |
|----------|---------|-------------|
| `QUESTION_CONCURRENCY` | `3` | Max parallel questions per experiment |
| `JUDGE_CONCURRENCY` | `4` | Max parallel judge calls per experiment |
| `LOG_LEVEL` | `INFO` | Python logging level |

### Optional — Pinecone

| Variable | Default | Description |
|----------|---------|-------------|
| `PINECONE_HOST` | `http://localhost:5080` | Pinecone local host |
| `PINECONE_INDEX_NAME` | `research-papers` | Index name |
| `PINECONE_NAMESPACE` | `default` | Namespace within the index |

### Experiment Selection

| Variable | Default | Description |
|----------|---------|-------------|
| `EXPERIMENT_SLUGS` | (all) | Comma-separated list of experiment slugs to run. Example: `experiment01_architecture_control_top5,experiment07_strong_checker_synth_top5` |

---

## 6. Output Artifacts

Each completed experiment produces the following files under `res/<experiment_slug>/`:

| File | Contents |
|------|----------|
| `answers.md` | Full baseline and multi-agent answers for all 15 questions, with per-question metrics |
| `metrics.json` | Machine-readable per-question metrics and experiment config |
| `latency_seconds.png` | Side-by-side bar chart: baseline vs multi-agent latency per question |
| `token_usage_total.png` | Side-by-side bar chart: total tokens per question |
| `citations_and_evidence.png` | Baseline citation count vs multi-agent evidence chunk count |
| `fact_check_statuses.png` | Stacked bar: supported / weakly_supported / unsupported claims per question |
| `judge_scores.md` | Human-readable table of judge scores for all 15 questions × 2 systems |
| `judge_scores.json` | Machine-readable judge scores |
| `judge_factual_accuracy.png` | Bar chart: factual accuracy scores per question |
| `judge_completeness.png` | Bar chart: completeness scores per question |
| `judge_citation_quality.png` | Bar chart: citation quality scores per question |
| `judge_clarity.png` | Bar chart: clarity scores per question |
| `judge_unsupported_claims.png` | Bar chart: unsupported claim counts per question |

Cross-experiment aggregates are saved under `res/summary/`:

| File | Contents |
|------|----------|
| `summary.md` | Full markdown comparison table across all 24 experiments |
| `summary_metrics.json` | Machine-readable aggregate data |
| `avg_latency_seconds.png` | Average latency per experiment |
| `avg_token_usage_total.png` | Average token usage per experiment |
| `avg_citations_and_evidence.png` | Average citation/evidence counts per experiment |
| `avg_fact_check_statuses.png` | Average fact-check status counts per experiment |
| `judge_avg_*.png` | One plot per judge metric across experiments |

---

## 7. Design Decisions and Trade-offs

### Why evidence is capped at `top_k`

The multi-agent system generates multiple search queries (one per subquestion plus the original), which can retrieve more chunks than `top_k`. Without capping, the multi-agent system would receive more context than the baseline, making comparison unfair. Capping evidence at `max_evidence_chunks = top_k` ensures both systems operate within the same retrieval budget.

### Why experiments run sequentially

Parallel experiment execution would cause concurrent writes to `res/`, shared Pinecone state, and interleaved console output. Sequential execution keeps results deterministic and easy to inspect.

### Why baseline and multi-agent run concurrently within a question

For latency measurement, they run via `asyncio.gather` so that real wall-clock time for each system is captured independently, without one blocking the other. This simulates a real comparison where both systems are given the same starting conditions.

### Why Pinecone is run locally via Docker

Using a local Pinecone instance avoids per-query network latency to a cloud service and removes external service availability as a variable. It also makes the experiment free to rerun without ongoing cloud costs.

### Why LLM responses use heuristic parsing instead of structured output

The agents use plain-text prompts and regex parsing with heuristic fallbacks. This keeps prompts simple and avoids forcing structured output formats that some models handle inconsistently. Fallbacks (`_heuristic_query_type`, `_heuristic_subquestions`) ensure the pipeline continues even when the LLM's output format is unexpected.

### Why fact-checking uses sentence-splitting rather than a pure LLM decision

`_build_fact_check_report` determines claim support by checking whether the draft answer's sentences contain inline `[E1]` style references that correspond to actual evidence notes. This is a deterministic structural check layered on top of the LLM's narrative fact-check report. It avoids relying entirely on the LLM's self-assessment.

---

## 8. Robustness Fixes

A comprehensive 4-agent parallel audit of the codebase identified 5 real issues (after filtering out 7 false positives). The following fixes were applied:

### Fix 1: Atomic Summary Writes
**Files:** `main.py:1519, 1602`

`_write_summary_json()` and `_write_summary_markdown()` were using raw `path.write_text()`. If the process crashed mid-write (e.g., srun timeout), the summary files would be left in a corrupted half-written state. Changed to use `_atomic_write_text()` which writes to a temp file first, then atomically replaces the target — guaranteeing either the complete new file or the old file, never a broken one.

### Fix 2: Corrupted metrics.json Handling
**File:** `main.py:1075`

The judge pass reads `metrics.json` with `json.loads()` but had no try/except. If a metrics file was corrupted (e.g., process killed during a write), the entire pipeline would crash with an unhandled `JSONDecodeError`. Added a try/except that logs a warning and skips the judge pass for that experiment, allowing the rest to continue.

### Fix 3: Malformed vLLM Response Handling
**File:** `app/llm_client.py:78`

After receiving a 200 OK from vLLM, `response.json()` could still fail if the response body wasn't valid JSON (e.g., vLLM internal error returning HTML). This would crash with a cryptic Python error. Added a try/except that raises a clear `LLMClientError` with the response body for debugging.

### Fix 4: Judge Parse Failure Flagging
**File:** `main.py:1282-1296`

When the judge LLM returns non-JSON output, `_parse_judge_response()` was silently defaulting all scores to 1 (minimum). This made genuine parse failures indistinguishable from legitimately terrible answers. Changed to return a result with `rationale: "JUDGE_PARSE_FAILURE"` and `parse_failed: True`, making failures visible in the judge scores output.

### False Positives Identified and Dismissed

| Finding | Why it's not a bug |
|---------|-------------------|
| Cosine similarity math in vector_store.py | Broadcasting is correct — both numerator `(N,)` and denominator `(N,)` divide element-wise. Embeddings are also pre-normalized (`normalize_embeddings=True`). |
| Citation ID renumbering after extra retrieval | Everything (evidence notes, draft answer, fact-check) is fully regenerated in the extra retrieval path. IDs are consistent within each pass. |
| Zero token tracking in `search_queries()` | This method makes no LLM calls (only vector retrieval). Returning zero tokens is correct. |
| Multi-query search "bias" | The multi-agent system generating multiple queries is by design — it's the core architectural difference being tested. |

---

## 9. File Reference

| File | Purpose |
|------|---------|
| `main.py` | Experiment orchestration, judge evaluation, result saving (~1900 lines) |
| `app/agents/multi_agent.py` | Five-agent pipeline implementation |
| `app/agents/baseline.py` | Single-agent baseline |
| `app/ingestor.py` | PDF ingestion with chunking and caching |
| `app/embedder.py` | Local sentence-transformers embedding |
| `app/vector_store.py` | JSON-based cosine similarity vector store |
| `app/retriever.py` | Query embedding + vector store retrieval |
| `app/llm_client.py` | Async OpenAI-compatible API wrapper (talks to vLLM) |
| `app/config.py` | `OpenAIConfig` and `PineconeConfig` dataclasses |
| `app/file_reader.py` | PDF text extraction via pypdf |
| `HPC_DEPLOY.md` | Step-by-step HPC deployment runbook |
| `CLAUDE.md` | Project context for Claude Code |
| `data/2002.08909v1.pdf` | The REALM paper (evaluation corpus) |
| `res/experiment*/` | Per-experiment results (metrics, answers, charts, judge scores) |
| `res/summary/` | Cross-experiment comparison (generated after all 24 complete) |
