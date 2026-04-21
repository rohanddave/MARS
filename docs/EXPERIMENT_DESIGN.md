# MARS-1 — Experiment Design & Methodology

> **What this document covers:** The research question, all 24 experiment configurations (architecture control, model ablations, retrieval depth sweep), the evaluation methodology (external GPT-4.1 judge, scoring rubric, adversarial framing), the 15-question test set, known limitations, and the full story of migrating from OpenAI API to self-hosted Gemma on NEU Explorer HPC — including every bug found and fixed.

---

## Table of Contents

1. [Research Question](#1-research-question)
2. [Experiment Design](#2-experiment-design)
3. [Evaluation Methodology](#3-evaluation-methodology)
4. [Question Set](#4-question-set)
5. [Limitations and Threats to Validity](#5-limitations-and-threats-to-validity)
6. [HPC Migration and Infrastructure](#6-hpc-migration-and-infrastructure)
7. [Bugs Found and Fixed During Development](#7-bugs-found-and-fixed-during-development)
8. [Design Rationale](#8-design-rationale)

---

## 1. Research Question

> **Can agent specialization — breaking retrieval-augmented QA into dedicated search, summarization, fact-checking, and synthesis roles — improve answer quality compared to a single prompt baseline, and if so, under which conditions?**

Three sub-questions guide the experiment design:

1. **Architecture effect:** Does the multi-agent pipeline outperform the baseline when model and retrieval budget are held constant?
2. **Model allocation effect:** Which agent role benefits most from upgrading to a stronger model?
3. **Retrieval depth effect:** Does increasing `top_k` (more evidence chunks) improve answers, or does noisy context hurt performance?

---

## 2. Experiment Design

All 24 experiments are defined in `main.py::_experiment_configs()`. Each is a frozen `AgentModelConfig` dataclass specifying per-agent model names, `top_k`, and `max_evidence_chunks`.

### Controlled Variables

The experiment design changes one major variable at a time where possible:

- **Architecture:** single-agent baseline vs multi-agent pipeline with the same model and same `top_k`.
- **Model allocation:** keep `top_k=5` fixed and change which subagent uses a stronger model.
- **Retrieval depth:** keep model allocation fixed and vary `top_k`.

### Family 1 — Architecture Control (1 experiment)

| Experiment | Description | Models | top_k |
|---|---|---|---:|
| `experiment01_architecture_control_top5` | Cleanest test of architecture — everything else held constant | All small (`FAST_AGENT_MODEL`) | 5 |

This is the primary answer to the research question. If the multi-agent system shows improvement here, it is attributable to architecture alone.

### Family 2 — Model Allocation Ablations (7 experiments)

All experiments in this family use `top_k=5`. One agent role at a time is upgraded to `STRONG_AGENT_MODEL`. The baseline always uses `FAST_AGENT_MODEL`.

| Experiment | Strong Agent | Rationale |
|---|---|---|
| `experiment02_strong_orchestrator_top5` | Orchestrator | Better query classification and planning |
| `experiment03_strong_search_top5` | Search | Better search query generation |
| `experiment04_strong_summarizer_top5` | Summarization | Better evidence compression |
| `experiment05_strong_fact_checker_top5` | Fact-checking | Stricter claim verification |
| `experiment06_strong_synthesizer_top5` | Final synthesis | Better answer writing and citation discipline |
| `experiment07_strong_checker_synth_top5` | Fact-checking + Final synthesis | Tests interaction between the two output-quality roles |
| `experiment08_all_strong_top5` | All agents | Upper-bound — best possible quality at full cost |

### Family 3 — Retrieval Depth Sweep (16 experiments)

For each of 8 model configurations, `top_k` is varied across {3, 5, 8}. The `top_k=5` results from Family 2 serve as the midpoint anchor. New experiments cover `top_k=3` and `top_k=8` for each model setup.

| Model Configuration | top_k Values Tested |
|---|---|
| All small | 3, 5, 8 |
| Strong orchestrator only | 3, 5, 8 |
| Strong search only | 3, 5, 8 |
| Strong summarizer only | 3, 5, 8 |
| Strong fact checker only | 3, 5, 8 |
| Strong final synthesizer only | 3, 5, 8 |
| Strong checker + synthesizer | 3, 5, 8 |
| All strong | 3, 5, 8 |

(The `top_k=5` row for each configuration is shared with experiments 01-08, giving 8 x 3 - 8 = 16 new experiments, 24 total.)

### Specialized Model Allocation

The project tests smaller and larger models for different subagents. A "specialized model" in this context means a model assigned to a specific role in the multi-agent pipeline. It can be the same base model as the other agents, or a stronger model used only for a high-impact role.

This matters because using a larger model for every step is expensive. A useful multi-agent system should ideally show where stronger models are worth the cost. For example, it may be better to use a larger model only for fact-checking and final synthesis rather than for search and orchestration.

### Evidence Capping

The multi-agent system caps evidence passed into summarization at the experiment's `top_k`. This keeps the evidence budget controlled. If `top_k=5`, the summarizer sees at most five evidence chunks. This avoids comparing systems where one condition silently receives much more context than another.

---

## 3. Evaluation Methodology

### Per-Experiment Metrics

For each question in each experiment, the runner captures:

| Metric | Description |
|--------|-------------|
| `baseline_latency_seconds` | Wall-clock time for baseline to answer |
| `orchestrator_latency_seconds` | Wall-clock time for multi-agent to answer |
| `baseline_total_tokens` | Total LLM tokens used by baseline |
| `orchestrator_total_tokens` | Total LLM tokens used across all multi-agent stages |
| `baseline_citation_count` | Number of retrieved chunks provided to baseline |
| `orchestrator_evidence_count` | Number of deduplicated evidence chunks used by multi-agent |
| `fact_check_status_counts` | Count of `supported` / `weakly_supported` / `unsupported` claims |

### External Judge

After each experiment, an external judge LLM (`JUDGE_MODEL`) scores both the baseline and multi-agent answers for all 15 questions. The judge is given:
- The original question
- The answer to evaluate
- The retrieved evidence (up to 12 chunks, 2500 chars each)

The judge prompt instructs strict evaluation against provided evidence only — not general knowledge. It returns JSON with:

| Score | Scale | Definition |
|-------|-------|-----------|
| `factual_accuracy` | 1-10 | All important claims are supported by evidence |
| `completeness` | 1-10 | Answer fully addresses the question |
| `citation_quality` | 1-10 | Citations are present, valid, specific, and tied to claims |
| `clarity` | 1-10 | Clear, well-organized, easy to follow |
| `unsupported_claims` | count | Number of claims not supported by evidence |

The judge uses adversarial framing ("your reputation depends on catching errors others miss") and mandatory deduction rules (-1 for uncited claims, -2 for hallucination, -2 per unaddressed question part) to create meaningful score differentiation.

### Why GPT-4.1 as External Judge

The initial judge was the same Gemma model that generated the answers. This created two problems:

1. **Self-judge bias.** Models are systematically lenient when evaluating their own output. With gemma judging gemma's answers, nearly everything scored 5/5 on the 1-5 scale. There was no meaningful differentiation between baseline and orchestrator quality.
2. **Scale ceiling effect.** Even with a stricter rubric and expanded 1-10 scale, a model judging its own output tends to find fewer flaws than an independent evaluator would.

The solution: use GPT-4.1 (via OpenAI API) as an external judge. This gives us:
- **Cross-model evaluation** — a different model family with different training data and biases evaluates the answers, eliminating self-judge bias
- **Stronger reasoning** — GPT-4.1 is better calibrated at following complex rubrics and catching subtle errors than any open model we could run on a single H100
- **Separation of concerns** — answer generation is fully open-source and self-hosted; only the evaluation layer uses a commercial API
- **Minimal cost** — 720 judge calls (24 experiments x 15 questions x 2 systems) costs ~$2-5

The architecture supports this cleanly because answer generation and judging are checkpointed independently. Setting `JUDGE_MODEL=gpt-4.1` triggers automatic re-judging of all experiments without regenerating any answers.

### Cross-Experiment Summary

`_save_summary_results()` reads all `metrics.json` and `judge_scores.json` files and generates:
- `res/summary/summary.md` — markdown table comparing all experiments
- `res/summary/summary_metrics.json` — machine-readable aggregate data
- Several PNG plots comparing experiments side-by-side

---

## 4. Question Set

15 fixed questions cover 11 category types, all targeting the REALM paper. Both systems answer the same questions in every experiment.

| # | Question (abbreviated) | Type |
|---|---|---|
| 1 | What external knowledge source does REALM retrieve from? | easy lookup |
| 2 | Which benchmarks does the paper use to evaluate REALM? | easy lookup |
| 3 | What is REALM and what is retrieval-augmented LM pre-training? | definition |
| 4 | How does REALM differ from a parametric model like BERT? | definition |
| 5 | How does REALM's retrieve-then-predict framework work? | method/mechanism |
| 6 | How does REALM train the retriever when the document is latent? | method/mechanism |
| 7 | What approximations make REALM practical at scale? | method/mechanism / implementation |
| 8 | How does REALM compare with ORQA or other baselines? | comparison |
| 9 | How does REALM's retrieval approach compare with parametric knowledge? | comparison |
| 10 | What ablation evidence shows retrieval pre-training helps? | evidence synthesis / ablation |
| 11 | Synthesize the evidence for why REALM improves open-domain QA. | evidence synthesis |
| 12 | How does masked-LM pre-training improve downstream QA in REALM? | multi-step reasoning |
| 13 | If REALM retrieves an irrelevant document, how does it affect p(z\|x), p(y\|z,x)? | multi-step reasoning / error analysis |
| 14 | What limitations should be noted when interpreting REALM's results? | limitation/uncertainty |
| 15 | Which claims cannot be verified without specific experimental evidence? | citation grounding / uncertainty |

Using multiple question types is important because agent specialization may not help equally across all tasks. The hypothesis is that simple lookup (Q1, Q2) shows minimal benefit from multi-agent processing, while synthesis (Q11), reasoning (Q12, Q13), and uncertainty (Q14, Q15) questions should benefit most.

---

## 5. Limitations and Threats to Validity

| Limitation | Impact |
|---|---|
| Single-paper corpus (REALM only) | Results may not generalize to other papers or domains |
| LLM judge | Judge scores are approximate; the judge itself may have biases toward verbosity or citation density |
| Parallel API calls | Latency measurements are noisier because multiple calls compete for provider capacity |
| PDF extraction quality | Text extracted from PDFs may miss figures, tables, equations, and math notation |
| Chunking sensitivity | Answers depend on how well 4000-char chunks preserve the relevant sections |
| Prompt sensitivity | The multi-agent pipeline has more prompt surfaces than the baseline — small prompt changes could significantly shift results |
| No ground-truth answers | There are no human-written reference answers; quality is measured only by judge LLM |
| Retrieval overlap | Multiple search queries in the multi-agent system may retrieve redundant evidence even after deduplication |
| Collapsed model ablation | All 24 experiments used the same model (Gemma-4-26B-A4B-it); "strong" vs "small" model distinction was not realized (see [analysis](res/analysis.md) for details) |
| Adversarial judge framing | The GPT-4.1 judge uses mandatory deduction rules that may systematically penalize longer, more detailed answers — potentially disadvantaging the multi-agent system |

---

## 6. HPC Migration and Infrastructure

### Background: Why Migrate

The first complete run of all 24 experiments used OpenAI's GPT-4.1-mini (small) and GPT-4.1 (strong) via the OpenAI API. Results are preserved in git at commit `5e6cd3a`. A critical issue was discovered in those results: from experiment 7 onward, the vector database (Pinecone local via Docker) returned empty evidence for every question. Both systems answered "no context provided" with empty evidence arrays across all 15 questions. Experiments 1-6 had valid data; 7-24 were useless. The vector DB likely got wiped or corrupted mid-run.

To avoid API costs, gain reproducibility, and use a single self-hosted model, the pipeline was migrated to Northeastern's Explorer HPC cluster.

### HPC Setup

- **Cluster:** NEU Explorer (login.explorer.northeastern.edu)
- **GPU:** NVIDIA H100 (1x, shared partition)
- **Allocation:** 1 hour per `srun` session (hard limit, non-negotiable)
- **Model:** `google/gemma-4-26B-A4B-it` — 26B total parameters, ~4B active via mixture-of-experts. Served locally through vLLM on port 8000 with an OpenAI-compatible API.
- **Embeddings:** `BAAI/bge-large-en-v1.5` via sentence-transformers (local, 1024 dimensions). No API calls for embeddings.
- **Vector store:** Replaced Pinecone with a local JSON-based cosine similarity store (`app/vector_store.py`). Stores vectors as numpy arrays, computes cosine similarity on query. Eliminates the Docker/Pinecone dependency entirely.

The code talks to vLLM exactly like it would talk to OpenAI — same endpoint format, same request/response shape. The only config change is `OPENAI_BASE_URL=http://localhost:8000/v1`.

Since all experiments now use the same self-hosted model, the "strong" vs "small" distinction from the original design collapses. Every agent role runs `google/gemma-4-26B-A4B-it`. The experiment structure is preserved (all 24 configs), but the model ablation experiments (2-8) effectively become architecture-only comparisons since there's no model quality difference between roles.

### Why HPC with Gemma Instead of OpenAI API

1. **Evaluate an open model.** Google's Gemma-4-26B-A4B-it is a state-of-the-art open-weight mixture-of-experts model (~4B active parameters from 26B total). Running it self-hosted on an H100 lets us evaluate how open models perform in a multi-agent RAG pipeline — a question that matters for cost-sensitive and privacy-sensitive deployments where API access isn't viable.
2. **Eliminate API cost as a variable.** With 24 experiments x 15 questions x multiple LLM calls per question, API costs add up. Self-hosting removes per-call pricing and makes re-runs free.
3. **Full reproducibility.** The model weights, serving configuration, and inference parameters are all fixed. No risk of API-side model updates changing results between runs.
4. **Demonstrate pipeline portability.** The codebase talks to vLLM via the same OpenAI-compatible API format. Switching between OpenAI, vLLM, or any other provider requires only changing `OPENAI_BASE_URL` — zero code changes.

The trade-off: HPC deployment is operationally complex. One-hour srun allocations, /tmp wipes between sessions, Squid proxy issues, and manual rsync for results. An API run takes 1 hour unattended; the HPC run took 8+ hours across multiple sessions with manual intervention.

### 1-Hour srun Limit vs 8-Hour Total Runtime

Each `srun` allocation is limited to 1 hour. The full 24-experiment run takes roughly 8 hours. The existing checkpointing system handles this naturally. Each question result is saved to `metrics.json` immediately upon completion. On re-run, `_load_partial_metrics()` reads saved results and only runs remaining questions. So each 1-hour session picks up exactly where the last one left off.

The workflow across sessions:
1. Get a GPU, rsync fresh code, activate env, start vLLM, run `main.py`
2. Experiments run until allocation expires (or Ctrl+C near the end)
3. Background sync has been copying results to home dir every 5 minutes
4. Next session: get a new GPU, check if `/tmp` survived, restart from where it left off

See [HPC_DEPLOY.md](HPC_DEPLOY.md) for the full step-by-step deployment runbook.

---

## 7. Bugs Found and Fixed During Development

### Bug 1: Chunker Overlap Crawl

**When found:** First HPC run, during ingestion.

**Symptoms:** The PDF (50,521 chars, 12 pages) was being split into 3,840 chunks. Log output showed chunk sizes decreasing by exactly 1 character per iteration: 257, 256, 255, 254... all the way down to 1-2 character chunks being individually embedded at ~400ms each. Ingestion was going to take over 25 minutes for a single paper.

**Investigation:** The chunker in `app/ingestor.py` (`_chunk_text()`) uses a sliding window of `chunk_size_chars` (4000) with `chunk_overlap_chars` (400) overlap. The advance logic was:

```python
start = max(end - self.chunk_overlap_chars, start + 1)
```

When `_best_chunk_boundary()` found a `\n\n` paragraph break that produced a chunk shorter than the overlap (e.g., a 250-char paragraph), then `end - overlap` would be less than `start + 1`, and the chunker would advance by just 1 character. The REALM paper has many short paragraphs — abstract, section headings, table captions, references — each under 400 chars. Each short paragraph triggered hundreds of near-duplicate tiny chunks as the chunker crawled forward one character at a time.

**Fix:** Two changes to `_chunk_text()`:

1. Only accept a boundary if the resulting chunk is at least `overlap + 1` chars:
```python
if boundary > start and (boundary - start) >= min_chunk_chars:
    end = boundary
```

2. Ensure start advances by at least `min_chunk_chars` per iteration:
```python
step = max(end - start - self.chunk_overlap_chars, min_chunk_chars)
start = start + step
```

### Bug 2: Step Calculation Used Absolute Position

**When found:** Immediately after fixing Bug 1.

**Symptoms:** The PDF now produced only 5 chunks instead of ~14-20. Chunks were proper size (~3400-4000 chars) but covered only ~17K of 50K chars. Two-thirds of the paper was being skipped entirely.

**Investigation:** The step calculation in the initial fix used `end` as an absolute text position instead of a relative chunk length:

```python
# BUG: end is absolute (e.g., 6992), not relative to start
step = max(end - self.chunk_overlap_chars, min_chunk_chars)
```

With `start=2993, end=6992, overlap=400`: step became `max(6992 - 400, 401) = 6592`, jumping start to position 9585. That's a 6592-char jump from a 3999-char chunk — skipping thousands of characters of text.

**Fix:** Use relative chunk length:
```python
step = max(end - start - self.chunk_overlap_chars, min_chunk_chars)
```

Now: `max((6992-2993) - 400, 401) = 3599`, proper overlap behavior.

**After both fixes:** 21 chunks, sizes ranging from 776 to 4000 chars, full paper coverage with proper overlap. Ingestion takes ~55 seconds.

### Bug 3: Citation ID Numbering

**When found:** During deep codebase audit after the chunking bugs.

**Location:** `app/agents/multi_agent.py`, `_chunks_to_evidence()` at line 404.

**Issue:** `citation_id=f"E{len(evidence) + index}"` with `enumerate(chunks, start=1)` produces E1, E3, E5 instead of E1, E2, E3. First iteration: `len([]) + 1 = 1` (correct). Second: `len([item]) + 2 = 3` (wrong).

**Impact:** Harmless — `_dedupe_evidence()` downstream immediately re-assigns sequential IDs. Fixed to `f"E{index}"` anyway for correctness.

### Issue: Squid Proxy Blocking localhost

**When found:** First experiment run on HPC after ingestion completed successfully.

**Symptoms:** All LLM calls returned `403 Forbidden` with an HTML error page from Squid proxy.

**Fix:** Set proxy bypass:
```bash
export no_proxy="localhost,127.0.0.1"
export NO_PROXY="localhost,127.0.0.1"
```

### Issue: Context Window Overflow on Judge Prompts

**When found:** End of experiment 1, during the judging phase.

**Symptoms:** vLLM returned `400 Bad Request` — prompt + output tokens exceeded 8192 token limit.

**Fix:** Increased `--max-model-len` from 8192 to 32768. Gemma-4-26B supports up to 128K tokens, and on the H100, GPU KV cache usage at 32K is only ~5.8%.

### Issue: Results Inaccessible from Login Node

**Problem:** `/tmp` on the compute node is local storage — the login node can't see it.

**Solution:** A background sync loop on the compute node copies results to the home directory every 5 minutes:
```bash
while true; do rsync -az $PROJECT_DIR/res/ ~/mars1_staging/res/ 2>/dev/null; sleep 300; done &
```

---

## 8. Design Rationale

### Early Results and the Judge Scale Problem (Experiments 1-2)

The baseline achieved 5/5 factual accuracy on nearly all questions with the initial 1-5 judge scale. Both systems clustered at 5/5, making differentiation impossible. The judge prompt was redesigned with three changes:

1. **Scale expanded to 1-10** with a detailed rubric defining each score band (9-10 = near perfect, 7-8 = good with minor gaps, 5-6 = adequate, 3-4 = significant issues, 1-2 = fundamentally broken).
2. **Adversarial framing** — the judge starts from a baseline score of 5 and adjusts up/down. The system instruction says "your reputation depends on catching errors others miss."
3. **Mandatory deduction rules** — specific penalties for uncited claims (-1 citation_quality), citation mismatches (-1 factual_accuracy), unaddressed question parts (-2 completeness), filler sentences (-1 clarity), and hallucinated facts (-2 factual_accuracy).

### What the Early Hypotheses Predicted

- top_k=3 experiments were expected to be the most interesting: scarce evidence should favor multi-agent's multi-query search
- top_k=8 was expected to test whether more context helps or introduces noise
- Simple lookup questions (Q1, Q2) were expected to show minimal multi-agent benefit; synthesis/reasoning/uncertainty questions (Q11-Q15) were expected to benefit most

For what actually happened, see the full [analysis of results](res/analysis.md).
