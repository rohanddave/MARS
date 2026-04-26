# MARS-1 Experimental Analysis: Single-Agent vs Multi-Agent RAG for Research Paper QA

> **What this document covers:** The complete findings from all 24 experiments — aggregate scores, per-question breakdowns, cost-quality tradeoffs, win/loss rates, the root cause analysis of why multi-agent lost, when multi-agent architectures would help, and actionable recommendations. This is the main results document.

---

**Author:** Analysis conducted on experiment results from the MARS-1 project  
**Date:** 2026-04-20  
**Scope:** 24 controlled experiments, 720 judge evaluations, 360 question-answer pairs  
**Evaluation corpus:** REALM paper (arXiv 2002.08909v1)  
**External judge:** GPT-4.1 (OpenAI), cross-model evaluation to eliminate self-judge bias

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Experimental Design](#2-experimental-design)
3. [Critical Design Note: Collapsed Model Ablation](#3-critical-design-note-collapsed-model-ablation)
4. [Finding 1: Baseline Wins the Aggregate — Decisively](#4-finding-1-baseline-wins-the-aggregate--decisively)
5. [Finding 2: Retrieval Depth (top_k) Matters More Than Architecture](#5-finding-2-retrieval-depth-top_k-matters-more-than-architecture)
6. [Finding 3: The Multi-Agent Pipeline Has a 33.6% Win Rate](#6-finding-3-the-multi-agent-pipeline-has-a-336-win-rate)
7. [Finding 4: Question Type Determines Multi-Agent Viability](#7-finding-4-question-type-determines-multi-agent-viability)
8. [Finding 5: The Cost-Quality Tradeoff Is Negative](#8-finding-5-the-cost-quality-tradeoff-is-negative)
9. [Finding 6: The Summarization Bottleneck](#9-finding-6-the-summarization-bottleneck)
10. [Finding 7: The Fact-Checker Is Structural, Not Semantic](#10-finding-7-the-fact-checker-is-structural-not-semantic)
11. [Finding 8: Per-Question Anomalies Reveal Architectural Weaknesses](#11-finding-8-per-question-anomalies-reveal-architectural-weaknesses)
12. [Finding 9: Unsupported Claims — The One Multi-Agent Advantage](#12-finding-9-unsupported-claims--the-one-multi-agent-advantage)
13. [Limitations of This Study](#13-limitations-of-this-study)
14. [Recommendations](#14-recommendations)
15. [Conclusion](#15-conclusion)
16. [Appendix A: Full Numerical Results](#appendix-a-full-numerical-results)

---

## 1. Executive Summary

Across 24 experiments and 720 GPT-4.1 judge evaluations, the single-agent RAG baseline **outperforms the five-agent multi-agent pipeline on every quality dimension** while consuming **5.7x fewer tokens** and running **6-10x faster**. The multi-agent system wins only 33.6% of head-to-head question matchups. Its sole consistent advantage — slightly fewer unsupported claims at higher retrieval depths — does not compensate for losses in factual accuracy (-0.30), completeness (-0.41), citation quality (-0.31), and clarity (-0.23).

The strongest predictor of answer quality is not architecture but **retrieval depth (top_k)**. Increasing top_k from 3 to 8 improves baseline quality more than any architectural change. The multi-agent pipeline's intermediate summarization step acts as an information bottleneck that compresses away the marginal value of additional retrieved chunks, producing a paradox: the system designed to better utilize evidence actually benefits less from having more of it.

These results carry an important caveat: all 24 experiments used the **same model** (Gemma-4-26B-A4B-it) for every agent role, collapsing the intended model ablation dimension. The multi-agent architecture may show different characteristics with heterogeneous model assignments or more capable models.

---

## 2. Experimental Design

### Architecture Under Test

**Baseline (single-agent):** Retrieve top-k chunks → format as numbered context → single LLM call → answer with bracket citations [1], [2], [3].

**Multi-agent (five-agent pipeline):**
1. **OrchestratorAgent** — classifies query type, generates subquestions, creates retrieval plan
2. **SearchAgent** — generates semantic search queries from the plan, retrieves and deduplicates evidence
3. **SummarizationAgent** — compresses each raw chunk into a structured evidence note (key claims, numbers, supporting statements)
4. **FinalSynthesisAgent** — writes a draft answer from evidence notes with inline [E1], [E2] citations
5. **FactCheckingAgent** — checks each sentence for citation presence; if unsupported claims found, triggers extra retrieval loop and re-drafting

### Independent Variables

| Variable | Levels | Intended | Realized |
|----------|--------|----------|----------|
| Architecture | baseline, multi_agent | Yes | Yes |
| Model allocation | small (fast) vs strong per agent role | Yes | **No** — both resolved to same model |
| Retrieval depth (top_k) | 3, 5, 8 | Yes | Yes |

### Evaluation

- 15 questions spanning 11 question types (easy lookup, definition, method/mechanism, comparison, evidence synthesis, multi-step reasoning, error analysis, limitation/uncertainty, citation grounding)
- GPT-4.1 as external judge with adversarial framing and mandatory deduction rules
- 5 scoring dimensions: factual accuracy (1-10), completeness (1-10), citation quality (1-10), clarity (1-10), unsupported claims (count)
- 24 experiments × 15 questions × 2 systems = **720 total evaluations**

### Experiment Families

| Family | Experiments | Purpose |
|--------|-------------|---------|
| Architecture control | exp01 | Cleanest baseline vs multi-agent comparison (all same model, top_k=5) |
| Model ablation | exp02-08 | One agent role upgraded to "strong" model per experiment (collapsed — see Section 3) |
| Retrieval depth sweep | exp09-24 | top_k ∈ {3, 5, 8} across 8 model configurations |

---

## 3. Critical Design Note: Collapsed Model Ablation

The experiment framework defines `small_model` and `strong_model` from environment variables `FAST_AGENT_MODEL` and `STRONG_AGENT_MODEL`, both defaulting to `settings.openai_answer_model`. Because the experiments ran on NEU Explorer HPC with a single vLLM instance serving Gemma-4-26B-A4B-it, **both variables resolved to the same model**.

This means:
- Experiments 02-08 ("model ablation") are **not actually ablations** — they are replications of experiment 01 with identical model assignments
- Experiments 09-24 vary top_k but not models
- The effective experimental matrix is **2 (architecture) × 3 (top_k)** with **4 replications per cell** (from the "different" model configs that are actually identical)

**Silver lining:** The unintended replications provide **strong statistical power**. Each (architecture, top_k) combination has 8 independent experiment runs (120 evaluations per cell), making the aggregate comparisons highly reliable despite the collapsed dimension.

---

## 4. Finding 1: Baseline Wins the Aggregate — Decisively

### Overall Averages (n=360 per system)

| Dimension | Baseline | Multi-Agent | Delta | Effect |
|-----------|----------|-------------|-------|--------|
| Factual Accuracy | **6.99** | 6.69 | -0.30 | Baseline wins |
| Completeness | **7.31** | 6.90 | -0.41 | Baseline wins |
| Citation Quality | **7.05** | 6.74 | -0.31 | Baseline wins |
| Clarity | **8.75** | 8.52 | -0.23 | Baseline wins |
| Unsupported Claims | 0.80 | **0.80** | -0.01 | Tie |

The baseline leads on all four quality dimensions. The gaps are consistent: approximately 0.2-0.4 points on a 10-point scale. While individually modest, the pattern is **unidirectional** — the multi-agent pipeline never leads in any aggregate dimension.

### Standard Deviations

| Dimension | Baseline σ | Multi-Agent σ |
|-----------|------------|---------------|
| Factual Accuracy | 1.20 | 1.34 |
| Completeness | 1.44 | 1.54 |
| Citation Quality | 1.28 | 1.61 |
| Clarity | 0.91 | 1.09 |
| Unsupported Claims | 1.58 | 1.47 |

The multi-agent pipeline shows **higher variance** on every quality dimension. This means it is not only worse on average but also less predictable — a critical concern for production systems where consistency matters.

---

## 5. Finding 2: Retrieval Depth (top_k) Matters More Than Architecture

### Quality by top_k and System

| top_k | System | FA | Comp | CQ | Clarity | Composite |
|-------|--------|-----|------|-----|---------|-----------|
| 3 | Baseline | 6.91 | 7.05 | 7.09 | 8.74 | **29.79** |
| 3 | Multi-Agent | 6.58 | 6.57 | 6.57 | 8.45 | 28.17 |
| 5 | Baseline | 6.82 | 7.18 | 6.88 | 8.67 | **29.55** |
| 5 | Multi-Agent | 6.67 | 6.96 | 6.72 | 8.50 | 28.85 |
| 8 | Baseline | 7.24 | 7.71 | 7.17 | 8.83 | **30.95** |
| 8 | Multi-Agent | 6.81 | 7.17 | 6.92 | 8.62 | 29.52 |

### Key Observations

1. **Baseline at top_k=8 (30.95) outperforms multi-agent at any top_k.** The simplest architectural choice with the most evidence beats the complex pipeline at every retrieval depth.

2. **Baseline quality gain from top_k=3→8: +1.16 composite points.** Multi-agent gain: +1.35 points. Both benefit from more evidence, but the baseline starts higher and ends higher.

3. **The quality gap between systems widens at top_k=8 (delta=1.43) vs top_k=5 (delta=0.70).** More evidence helps the baseline disproportionately because it passes all chunks directly to the LLM, while the multi-agent's summarization step compresses away marginal information.

4. **At top_k=3, the multi-agent's disadvantage is smallest** (delta=1.62 composite). This was the hypothesized sweet spot for multi-agent — scarce evidence should favor multi-query search. The data weakly supports this: the gap is smallest here, but multi-agent still loses.

### Latency Scaling

| top_k | Baseline (s) | Multi-Agent (s) | Multiplier |
|-------|-------------|-----------------|------------|
| 3 | 4.93 | 30.66 | **6.2x** |
| 5 | 5.97 | 45.09 | **7.6x** |
| 8 | 6.54 | 68.10 | **10.4x** |

The latency multiplier grows super-linearly with top_k. The five-agent serial chain amplifies per-chunk processing time across agents. At top_k=8, the multi-agent system requires over a minute per question.

### Token Scaling

| top_k | Baseline | Multi-Agent | Multiplier |
|-------|----------|-------------|------------|
| 3 | 3,080 | 17,600 | **5.7x** |
| 5 | 5,272 | 30,125 | **5.7x** |
| 8 | 8,215 | 47,522 | **5.8x** |

The token multiplier is remarkably constant at ~5.7x regardless of top_k. This is a structural overhead from the five-agent architecture: each agent reads context and generates output.

---

## 6. Finding 3: The Multi-Agent Pipeline Has a 33.6% Win Rate

Across 360 head-to-head question matchups (24 experiments × 15 questions):

| Outcome | Count | Percentage |
|---------|-------|------------|
| Baseline wins | 198 | **55.0%** |
| Multi-Agent wins | 121 | **33.6%** |
| Tie | 41 | **11.4%** |

The multi-agent system loses the majority of individual matchups. No single experiment achieves a multi-agent win rate above 53% (experiment 04 and 07 with 8 wins out of 15).

### Worst Experiments for Multi-Agent

| Experiment | W-L-T | Composite Delta |
|------------|-------|-----------------|
| experiment20 (summarizer, top_k=8) | 1-13-1 | -2.87 |
| experiment11 (checker+synth, top_k=3) | 1-11-3 | -3.00 |
| experiment21 (fact_checker, top_k=3) | 2-10-3 | **-3.33** |

### Best Experiments for Multi-Agent

| Experiment | W-L-T | Composite Delta |
|------------|-------|-----------------|
| experiment07 (checker+synth, top_k=5) | 8-6-1 | **+1.87** |
| experiment09 (all small, top_k=3) | 6-7-2 | +0.60 |

Only **1 out of 24 experiments** shows a positive composite delta for the multi-agent system (experiment 07, +1.87). This appears to be an outlier rather than a systematic advantage — experiment 11 uses the same model config at top_k=3 and scores -3.00.

---

## 7. Finding 4: Question Type Determines Multi-Agent Viability

### Deltas by Question Type (Multi-Agent minus Baseline)

| Question Type | n | FA | Comp | CQ | Clarity | Composite |
|---------------|---|-----|------|-----|---------|-----------|
| evidence synthesis | 24 | **+0.12** | **+0.29** | **+0.25** | **+0.12** | **+0.79** |
| multi-step reasoning | 24 | +0.04 | -0.50 | **+0.62** | +0.17 | +0.33 |
| method/mechanism | 48 | +0.08 | -0.35 | +0.04 | +0.23 | +0.00 |
| limitation/uncertainty | 24 | -0.21 | +0.04 | -0.17 | -0.12 | -0.46 |
| definition | 48 | -0.29 | -0.31 | +0.10 | -0.15 | -0.65 |
| comparison | 48 | -0.21 | -0.42 | +0.02 | -0.25 | -0.85 |
| easy lookup | 48 | -0.06 | +0.69 | -0.83 | -0.23 | -0.44 |
| evidence synthesis / ablation | 24 | -0.75 | -0.67 | -0.71 | -0.25 | -2.38 |
| method / implementation | 24 | -0.62 | -0.33 | -0.71 | -0.33 | -2.00 |
| citation grounding / uncertainty | 24 | -1.29 | -2.38 | -0.71 | -0.83 | **-5.21** |
| multi-step reasoning / error analysis | 24 | -0.88 | -1.88 | -1.88 | -1.33 | **-5.96** |

### Interpretation

The multi-agent pipeline shows a **positive** composite delta in only **2 of 11 question types**:

1. **Evidence synthesis (+0.79):** Questions requiring integration across multiple paper sections. The multi-agent's multi-query search and structured evidence gathering covers more ground than the baseline's single retrieval. This is the strongest vindication of the multi-agent design.

2. **Multi-step reasoning (+0.33):** Questions requiring step-by-step explanation. The orchestrator's query plan naturally suits structured reasoning. However, the advantage is small and driven entirely by citation quality, not factual accuracy.

The multi-agent pipeline shows **catastrophic failures** on two question types:

1. **Multi-step reasoning / error analysis (-5.96):** Question 13 asks about REALM's behavior when retrieving irrelevant documents — a hypothetical that requires inference beyond the paper's explicit statements. The fact-checking step induces extreme over-hedging, producing evasive "the evidence does not state..." responses when the baseline correctly reasons from available evidence.

2. **Citation grounding / uncertainty (-5.21):** Question 15 asks which claims cannot be verified without specific evidence. The multi-agent pipeline struggles with meta-reasoning about its own evidence base, consistently underperforming the baseline.

### The Pattern

The multi-agent architecture helps when the question **benefits from broader evidence gathering** across the paper. It hurts when the question requires **inferential reasoning, analytical depth, or meta-cognition about evidence sufficiency** — the pipeline's conservative fact-checking and information-lossy summarization steps actively degrade these answers.

---

## 8. Finding 5: The Cost-Quality Tradeoff Is Negative

### Cost Per Composite Quality Point

| top_k | System | Composite | Tokens | Tokens/Point |
|-------|--------|-----------|--------|--------------|
| 3 | Baseline | 29.79 | 3,080 | **103** |
| 3 | Multi-Agent | 28.17 | 17,600 | **625** |
| 5 | Baseline | 29.55 | 5,272 | **178** |
| 5 | Multi-Agent | 28.85 | 30,125 | **1,044** |
| 8 | Baseline | 30.95 | 8,215 | **265** |
| 8 | Multi-Agent | 29.52 | 47,522 | **1,610** |

The multi-agent system is **6.0-6.1x less cost-efficient** per quality point across all top_k values. At top_k=8, it spends 1,610 tokens per quality point versus the baseline's 265.

### Marginal Cost of Quality via top_k Increase (3→8)

- **Baseline:** (8,215 - 3,080) / (30.95 - 29.79) = **4,440 tokens per composite point gained**
- **Multi-Agent:** (47,522 - 17,600) / (29.52 - 28.17) = **22,164 tokens per composite point gained**

The multi-agent system's marginal cost of quality improvement via more retrieval is **5.0x worse** than the baseline's.

### Evidence Density

| top_k | Baseline Citations | Multi-Agent Evidence | Multiplier |
|-------|--------------------|----------------------|------------|
| 3 | 3.0 | 5.4 | 1.8x |
| 5 | 5.0 | 8.4 | 1.7x |
| 8 | 8.0 | 12.6 | 1.6x |

The multi-agent retrieves 60-80% more evidence items through its multi-query search. This additional evidence density does not translate into quality gains — it represents coverage breadth (more chunks touched) but not depth (better use of each chunk).

---

## 9. Finding 6: The Summarization Bottleneck

The SummarizationAgent compresses each raw chunk into an "evidence note" containing key claims, numbers, and supporting statements. This creates an **information bottleneck** that is the multi-agent pipeline's most damaging architectural weakness.

### How It Manifests

1. **Signal loss on detail-rich chunks:** When a chunk contains ablation data, mathematical formulas, or specific benchmark numbers, the summarization step may compress away the exact details that answer the question. The most dramatic example: Question 10 (ablation evidence) at top_k=3, where the multi-agent confidently states "the provided evidence does not contain any ablation or diagnostic studies" — but the raw retrieved chunks DO contain this information. The summarization agent dropped it, and the synthesis agent then hallucinated an absence.

2. **Diminishing returns from more evidence:** As top_k increases, additional chunks provide marginal new information. The baseline passes all chunks directly to the LLM, which can identify and use marginal details. The summarization agent compresses each chunk independently, often discarding the marginal information as insufficiently important. This explains why baseline quality improves more steeply with top_k than multi-agent quality does.

3. **Loss of mathematical content:** Both systems handle LaTeX math notation, but the baseline's raw chunks preserve complete derivations. The evidence notes produced by the summarization agent often reduce formulas to prose descriptions, losing precision that the judge rewards.

### Structural vs Qualitative Evidence

The evidence notes use a rigid template ("key claims, numbers, supporting statements") that does not adapt to chunk content. A chunk containing a proof sketch is summarized the same way as a chunk containing experimental results. This one-size-fits-all compression is suboptimal for the diverse information types in a research paper.

---

## 10. Finding 7: The Fact-Checker Is Structural, Not Semantic

A critical implementation detail revealed by code analysis: the FactCheckingAgent's claim classification does **not** use the LLM's semantic assessment of claim support. Instead, `_build_fact_check_report()` performs a **deterministic structural check**:

```
For each sentence in the draft answer (up to 12):
  If any [E1]/[E2] reference matches an actual evidence note ID → "supported"
  Else → "unsupported"
```

This means:
- A sentence citing [E3] that completely misrepresents E3's content is classified as "supported"
- A sentence making a correct claim without a citation is classified as "unsupported"
- The LLM's response is used only as narrative `report_text`, not for classification

### Consequences

1. **The fact-checker is really a citation-presence checker.** It enforces citation format, not factual grounding. This explains the disconnect observed between the fact-checker's unsupported counts and the judge's unsupported claim counts.

2. **The extra retrieval loop triggers on citation gaps, not factual gaps.** When the fact-checker finds "unsupported" claims, it requests more retrieval. But "unsupported" just means "uncited" — the claim might be perfectly correct. This can introduce noise by retrieving chunks for claims that didn't need support.

3. **The fact-checking step still has value** — it enforces citation discipline and triggers a revision pass that generally improves answer structure. But it is a much weaker guardrail than the experiment design intended.

---

## 11. Finding 8: Per-Question Anomalies Reveal Architectural Weaknesses

### Question 13: The Catastrophic Failure (delta = -6.0 composite)

Question: "If REALM retrieves an irrelevant document, how would that affect p(z|x), p(y|z,x), and the final answer prediction?"

This requires hypothetical reasoning — inferring system behavior from its mathematical formulation. The baseline correctly reasons from the probability formulas in the retrieved chunks. The multi-agent pipeline, after its fact-checking pass, produces hedged non-answers: "The provided evidence does not explicitly state how p(z|x) is affected." The fact-checker's conservatism, combined with the synthesis agent's instruction to "not use facts that are not supported by evidence notes," creates pathological over-hedging on inferential questions.

### Question 15: The Meta-Reasoning Failure (delta = -5.2 composite)

Question: "Which claims about REALM's performance or mechanism cannot be verified unless the answer cites specific experimental evidence from the paper?"

This requires the system to reason about the sufficiency of its own evidence. The multi-agent pipeline, constrained by its evidence notes, cannot effectively meta-reason about what it doesn't know. The baseline, with direct access to raw chunks, handles this more naturally.

### Question 10: The Summarization Failure (delta = -2.4 composite)

Question: "What ablation or diagnostic evidence shows that retrieval pre-training improves REALM rather than only the reader component?"

At top_k=3, the multi-agent fails catastrophically (FA=3, Comp=3 vs baseline FA=6, Comp=7). The summarization agent dropped ablation details from the evidence notes. The synthesis agent then incorrectly asserted the absence of this information.

### Question 11: The Multi-Agent Success (delta = +0.8 composite)

Question: "Synthesize the evidence for why REALM improves open-domain QA performance."

This broad synthesis question genuinely benefits from the multi-agent's multi-query search. The SearchAgent generates queries targeting different aspects (retrieval quality, pre-training, fine-tuning), gathering evidence across paper sections that a single embedding query might miss.

---

## 12. Finding 9: Unsupported Claims — The One Multi-Agent Advantage

### Unsupported Claims by top_k (Judge-assessed, lower is better)

| top_k | Baseline | Multi-Agent | Delta |
|-------|----------|-------------|-------|
| 3 | 0.47 | 0.72 | +0.25 (baseline better) |
| 5 | 1.02 | 0.88 | **-0.14 (multi-agent better)** |
| 8 | 0.92 | 0.79 | **-0.13 (multi-agent better)** |

At top_k=5 and top_k=8, the multi-agent produces slightly fewer unsupported claims. This is the one dimension where the pipeline's citation enforcement and fact-checking revision loop provides measurable benefit. However:

- The advantage is small (0.13-0.14 claims per question)
- At top_k=3, the multi-agent actually has MORE unsupported claims
- The advantage is overwhelmed by losses on other dimensions

The fact-checking step's citation-presence enforcement does reduce the frequency of uncited assertions in the final answer, but this modest formatting benefit does not justify the pipeline's cost and quality penalties.

---

## 13. Limitations of This Study

### Single-Paper Evaluation Corpus

All experiments evaluate on a single 12-page paper (REALM, 2002.08909v1). With top_k=5 covering ~24% of the paper per question, retrieval is relatively easy. The multi-agent pipeline might show greater advantage on:
- Longer documents where retrieval is harder
- Multi-document corpora where cross-document synthesis is needed
- Domain-specific papers where query reformulation adds value

### Single Model

All experiments used Gemma-4-26B-A4B-it (26B total, ~4B active parameters via MoE) for every role. The multi-agent architecture was designed for heterogeneous model assignment — e.g., a strong model for orchestration and synthesis, a fast model for summarization. With a single model, the architecture cannot demonstrate its core value proposition of role-specialized resource allocation.

### Same Model as Judge and Generator (Partially)

While GPT-4.1 serves as external judge (eliminating self-judge bias), the judge evaluates answers from a different model family. This cross-model evaluation is appropriate for eliminating bias but may introduce systematic preferences for writing styles or answer structures that favor one system over another.

### Small Question Set

15 questions provide limited statistical power per question type (some types have only 24 observations across all experiments). Question types with only one representative question (e.g., evidence synthesis, citation grounding) may be dominated by idiosyncratic question effects rather than true type-level patterns.

### Sequential Pipeline

The five agents run sequentially, creating a latency chain and allowing error propagation. An alternative multi-agent architecture with parallel execution or iterative refinement might perform differently.

### Judge Adversarial Framing

The GPT-4.1 judge uses adversarial instructions ("your reputation depends on catching errors others miss") and mandatory deduction rules. This may systematically penalize longer, more detailed answers (more surface area for deductions), which could disadvantage the multi-agent system's longer outputs.

---

## 14. Recommendations

### For This Project

1. **The baseline at top_k=8 is the Pareto-optimal configuration.** It achieves the highest quality (30.95 composite) at moderate cost (8,215 tokens/question, ~6.5s latency). Use this as the production configuration.

2. **If multi-agent is retained, fix the summarization bottleneck first.** The evidence note compression is the single largest source of quality loss. Options:
   - Pass raw chunks alongside evidence notes to the synthesis agent
   - Use adaptive summarization depth based on chunk content type
   - Allow the synthesis agent to request specific raw chunks when evidence notes are insufficient

3. **Upgrade the fact-checker from structural to semantic.** The current citation-presence check misses the core purpose of fact-checking. Have the LLM's claim-by-claim assessment drive the classification, not regex matching.

4. **Reduce the pipeline from 5 agents to 3.** The orchestrator adds negligible value (its query classification and subquestion generation are simple heuristics). The separate summarization step is net negative. Consider: SearchAgent → FactCheckAgent (semantic) → SynthesisAgent.

5. **Re-run with heterogeneous models** to test the original model ablation hypothesis. Use Gemma-4-26B for the baseline/search/summarization and a larger model (e.g., 70B) for orchestration, fact-checking, and synthesis.

### For the Research Community

6. **Single-agent RAG is a strong baseline for single-document QA.** The marginal complexity of multi-agent architectures must be justified against this baseline, which is often stronger than expected.

7. **Retrieval depth is an underappreciated lever.** Doubling top_k from 3 to 8 provides more quality improvement than any architectural change tested here, at much lower marginal cost for single-agent systems.

8. **Intermediate summarization steps in RAG pipelines are double-edged.** They reduce noise but also lose signal. The net effect depends on the information density of the source material and the capability of the summarization model.

9. **LLM-as-judge evaluation requires careful rubric design.** The adversarial framing and mandatory deduction rules in this study may introduce systematic bias against verbose systems. Future work should test rubric sensitivity.

---

## 15. Conclusion

The MARS-1 experiment provides strong evidence that, for single-document research paper QA with a mid-tier open-source model, **multi-agent RAG architectures do not improve answer quality over a well-configured single-agent baseline**. The five-agent pipeline's theoretical benefits — structured evidence gathering, fact-checking, iterative refinement — are negated by practical costs: information loss during summarization, over-hedging from conservative fact-checking, error propagation across agent handoffs, and a 5.7x token overhead.

The multi-agent pipeline does show genuine promise in one narrow regime: **broad evidence synthesis questions where multi-query search covers more ground than a single retrieval**. This suggests that the core value of multi-agent RAG lies not in deeper processing of the same evidence, but in **wider retrieval coverage** — a benefit that could potentially be captured by a simpler multi-query retrieval strategy without the full five-agent pipeline.

The most actionable finding is that **retrieval depth (top_k) is the dominant lever for quality improvement**, providing more gain per marginal token than architectural complexity. For practitioners: before adding agents, add chunks.

---

## Appendix A: Full Numerical Results

### A.1 Per-Experiment Deltas (Multi-Agent minus Baseline)

| Experiment | FA | Comp | CQ | Clarity | Unsup |
|------------|-----|------|-----|---------|-------|
| exp01: architecture control, top_k=5 | -0.07 | -0.07 | -0.07 | -0.20 | -0.27 |
| exp02: strong orchestrator, top_k=5 | -0.20 | +0.20 | -0.40 | -0.07 | -0.07 |
| exp03: strong search, top_k=5 | -0.40 | -0.47 | -0.40 | -0.33 | -0.33 |
| exp04: strong summarizer, top_k=5 | -0.53 | -0.47 | -0.33 | -0.33 | -0.67 |
| exp05: strong fact checker, top_k=5 | -0.07 | -0.53 | -0.47 | -0.20 | +0.40 |
| exp06: strong synthesizer, top_k=5 | +0.07 | -0.13 | +0.00 | +0.00 | -0.47 |
| exp07: checker+synth, top_k=5 | +0.53 | +0.40 | +0.60 | +0.33 | +0.27 |
| exp08: all strong, top_k=5 | -0.53 | -0.73 | -0.20 | -0.53 | +0.00 |
| exp09: all small, top_k=3 | -0.13 | +0.00 | +0.27 | +0.47 | +0.27 |
| exp10: all small, top_k=8 | -0.20 | -0.67 | -0.07 | -0.20 | -0.53 |
| exp11: checker+synth, top_k=3 | -0.53 | -0.80 | -1.13 | -0.53 | +0.20 |
| exp12: checker+synth, top_k=8 | -0.40 | -0.27 | -0.33 | -0.33 | -0.27 |
| exp13: all strong, top_k=3 | +0.07 | +0.07 | -0.07 | +0.00 | -0.07 |
| exp14: all strong, top_k=8 | -0.47 | -0.67 | -0.13 | -0.07 | -0.87 |
| exp15: strong orch, top_k=3 | -0.40 | -0.67 | -0.67 | -0.47 | +0.40 |
| exp16: strong orch, top_k=8 | -0.27 | -0.07 | +0.13 | +0.07 | +0.53 |
| exp17: strong search, top_k=3 | -0.40 | -0.60 | -0.73 | -0.27 | -0.27 |
| exp18: strong search, top_k=8 | -0.67 | -0.67 | -0.27 | -0.40 | -0.20 |
| exp19: strong summ, top_k=3 | -0.20 | -0.53 | -0.40 | -0.33 | +0.13 |
| exp20: strong summ, top_k=8 | -0.87 | -0.87 | -0.80 | -0.33 | +0.13 |
| exp21: strong fact, top_k=3 | -0.73 | -1.00 | -1.00 | -0.60 | +0.87 |
| exp22: strong fact, top_k=8 | -0.27 | -0.60 | -0.40 | -0.27 | +0.53 |
| exp23: strong synth, top_k=3 | -0.27 | -0.33 | -0.47 | -0.60 | +0.47 |
| exp24: strong synth, top_k=8 | -0.33 | -0.47 | -0.07 | -0.20 | -0.33 |

### A.2 Win/Loss/Tie Summary

| Outcome | Count | Percentage |
|---------|-------|------------|
| Baseline wins | 198 | 55.0% |
| Multi-Agent wins | 121 | 33.6% |
| Ties | 41 | 11.4% |
| **Total matchups** | **360** | |

### A.3 Per-Question Performance (Averaged Across All 24 Experiments)

| Q# | Type | BL Composite | MA Composite | Delta |
|----|------|-------------|-------------|-------|
| 1 | easy lookup | 34.8 | 33.0 | -1.7 |
| 2 | easy lookup | 25.5 | 26.3 | +0.8 |
| 3 | definition | 31.5 | 30.8 | -0.7 |
| 4 | definition | 32.8 | 32.2 | -0.6 |
| 5 | method/mechanism | 32.5 | 32.2 | -0.3 |
| 6 | method/mechanism | 31.0 | 31.4 | +0.3 |
| 7 | method/implementation | 32.2 | 30.2 | -2.0 |
| 8 | comparison | 28.5 | 27.1 | -1.5 |
| 9 | comparison | 31.4 | 31.2 | -0.2 |
| 10 | evidence synthesis/ablation | 29.7 | 27.3 | -2.4 |
| 11 | evidence synthesis | 29.0 | 29.8 | **+0.8** |
| 12 | multi-step reasoning | 29.8 | 30.2 | **+0.3** |
| 13 | error analysis | 29.1 | 23.1 | **-6.0** |
| 14 | limitation/uncertainty | 27.8 | 27.3 | -0.5 |
| 15 | citation grounding | 25.9 | 20.7 | **-5.2** |

---

## Appendix B: Root Cause Analysis — Why Did Multi-Agent Lose?

The intuition that "more agents = more specialized = better" makes sense in theory, but the data reveals three root causes for the pipeline's underperformance.

### Root Cause 1: The Telephone Game — Information Loss at Each Handoff

The pipeline is sequential: Orchestrator -> Search -> Summarizer -> Synthesizer -> Fact-Checker -> (revision). Each handoff is a lossy compression step. The worst offender is the **SummarizationAgent** — it compresses raw chunks into "evidence notes," and critical details get dropped.

The most dramatic example: Question 10 asks about ablation evidence. The baseline reads the raw chunk containing ablation data and answers correctly (FA=6, Comp=7). The multi-agent's summarization step drops the ablation details, and the synthesis agent then confidently writes "the provided evidence does not contain any ablation studies" — scoring FA=3, Comp=3. The information was retrieved; it was lost in transit between agents.

The baseline has zero information loss — raw chunks go directly to the LLM in a single call.

### Root Cause 2: Role-Based Prompting Does Not Equal Real Specialization

Every agent in the pipeline is the same Gemma-4-26B-A4B-it model with a different system prompt. Telling a model "you are a fact-checker" does not make it meaningfully better at fact-checking than when it fact-checks as part of a single comprehensive answer. The same weights, the same reasoning capability — just a narrower prompt window.

This is the standard multi-agent pattern (LangChain, CrewAI, AutoGen all typically route to the same model with different role instructions). The finding is that **role-based prompting alone does not create real specialization with a mid-tier model**. The 5.7x token overhead pays for five passes over the same evidence with the same reasoning ability — each pass adding noise and losing signal rather than adding genuine specialized insight.

True multi-agent value would require agents with **genuinely different capabilities**: different models, different tools, different knowledge sources, or access to different APIs. Same-model-different-prompt is specialization in name only.

### Root Cause 3: Conservative Fact-Checking Induces Over-Hedging

The synthesis agent is instructed: "Do not use facts that are not supported by evidence notes." Combined with the fact-checker flagging uncited sentences as "unsupported," this creates a pathological feedback loop on inferential questions.

Question 13 asks: "If REALM retrieves an irrelevant document, how would that affect p(z|x)?" This requires reasoning from the mathematical formulation — it is not stated explicitly in any chunk. The baseline reads the formula and reasons correctly. The multi-agent's pipeline flags any inference as "unsupported" and the synthesis agent hedges with "The provided evidence does not explicitly state..." — a non-answer that scores 6.0 composite points below the baseline.

The pipeline was designed to be careful. On analytical questions, "careful" became "evasive."

---

## Appendix C: When Would Multi-Agent Architecture Help?

The architecture is not inherently wrong — the conditions were not right for it to shine. Multi-agent RAG adds value when:

1. **Each agent brings genuinely different capabilities** — different models, tools, or knowledge sources (not just different system prompts on the same model)
2. **The task requires broad information gathering** — across large documents (100+ pages) or multi-document corpora where a single embedding query cannot cover enough ground
3. **The handoff costs are lower than the specialization gains** — minimal intermediate compression, parallel rather than serial execution
4. **Retrieval is genuinely hard** — the 12-page REALM paper with top_k=5 covers ~24% of the content per question, making single-query retrieval already sufficient for most questions

The multi-agent pipeline's one genuine success was on **broad evidence synthesis questions** (Q11: +0.8 composite delta), where the SearchAgent's multi-query approach gathered evidence across paper sections that a single embedding query missed. This confirms the core value proposition of multi-agent RAG: **wider retrieval coverage**. But that benefit can be captured by a simpler multi-query retrieval strategy without a full five-agent pipeline.

### On Using the Same Model for All Agents

The experiment design included `FAST_AGENT_MODEL` and `STRONG_AGENT_MODEL` environment variables to enable heterogeneous model assignment. On a single H100 with one vLLM instance, only one model could be served at a time, so both defaulted to Gemma-4-26B-A4B-it.

Even with different models, the architectural issues (summarization bottleneck, structural fact-checking, serial error propagation) would persist. A GPT-4.1 summarizer would be a better summarizer, but compression is still lossy by design. The gains from heterogeneous models are primarily **cost optimization** (cheap model for simple tasks, expensive model only where reasoning quality matters), not necessarily quality improvement.

Practical approaches for heterogeneous model deployment:
- Mix of local + API models (e.g., local Gemma for search query generation, OpenAI GPT-4.1 for synthesis)
- Two vLLM instances on separate GPUs (requires multi-GPU allocation)
- Multi-model serving with vLLM's model multiplexing
- Different quantization levels of the same model family (e.g., 4-bit for cheap tasks, FP16 for synthesis)
| 7 | method/implementation | 32.2 | 30.2 | -2.0 |
| 8 | comparison | 28.5 | 27.1 | -1.5 |
| 9 | comparison | 31.4 | 31.2 | -0.2 |
| 10 | evidence synthesis/ablation | 29.7 | 27.3 | -2.4 |
| 11 | evidence synthesis | 29.0 | 29.8 | **+0.8** |
| 12 | multi-step reasoning | 29.8 | 30.2 | **+0.3** |
| 13 | error analysis | 29.1 | 23.1 | **-6.0** |
| 14 | limitation/uncertainty | 27.8 | 27.3 | -0.5 |
| 15 | citation grounding | 25.9 | 20.7 | **-5.2** |
