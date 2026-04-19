from __future__ import annotations

import asyncio
import json
import logging
import os
import shutil
import time
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Awaitable, Callable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from dotenv import load_dotenv

from app.agents.baseline import BaselineAgent, BaselineAgentResult
from app.agents.multi_agent import (
    FactCheckingAgent,
    FinalSynthesisAgent,
    MultiAgentAnswer,
    OrchestratorAgent,
    SearchAgent,
    SummarizationAgent,
)
from app.config import OpenAISettings, PineconeSettings
from app.embedder import OpenAIEmbedder
from app.ingestor import ResearchPaperIngestor
from app.llm_client import LLMClient
from app.models.answer import TokenUsage
from app.retriever import ResearchPaperRetriever
from app.vector_store import PineconeVectorStore

logger = logging.getLogger(__name__)

QUESTIONS = [
  "What is REALM and how does it differ from traditional language models like BERT in terms of knowledge storage and retrieval?",
  "Explain how the retrieve-then-predict framework works in REALM, including the role of the latent variable z and backpropagation through the retriever.",
  "What evidence does the paper provide that REALM improves Open-domain Question Answering performance compared to methods like ORQA, and what are the key reasons for this improvement?"
]
RESULTS_DIR = Path("res")


@dataclass(frozen=True)
class AgentModelConfig:
    slug: str
    name: str
    top_k: int
    orchestrator_model: str
    search_model: str
    summarization_model: str
    fact_check_model: str
    final_synthesis_model: str


@dataclass(frozen=True)
class QuestionRunMetrics:
    experiment_slug: str
    experiment_name: str
    question_index: int
    question: str
    top_k: int
    baseline_latency_seconds: float
    orchestrator_latency_seconds: float
    baseline_token_usage: TokenUsage
    orchestrator_token_usage: TokenUsage
    baseline_citation_count: int
    orchestrator_evidence_count: int
    fact_check_status_counts: dict[str, int]
    baseline_evidence: list[dict[str, object]]
    orchestrator_evidence: list[dict[str, object]]
    baseline_answer: str
    orchestrator_answer: str


ExperimentFn = Callable[[BaselineAgent, ResearchPaperRetriever, OpenAISettings], Awaitable[None]]


def _llm_client(settings: OpenAISettings, model: str | None = None) -> LLMClient:
    if model:
        settings = replace(settings, openai_answer_model=model)
    return LLMClient(settings)


def _model_for(role: str, default_model: str) -> str:
    env_name = f"{role.upper()}_MODEL"
    return os.getenv(env_name, default_model)


def _configure_logging() -> None:
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )
    logger.info("Logging configured level=%s", log_level)


def build_baseline_agent(
    retriever: ResearchPaperRetriever,
    settings: OpenAISettings,
) -> BaselineAgent:
    baseline_model = _model_for("baseline", settings.openai_answer_model)
    logger.info("Building baseline agent model=%s", baseline_model)
    return BaselineAgent(retriever=retriever, llm_client=_llm_client(settings, baseline_model))


def build_orchestrator_agent(
    retriever: ResearchPaperRetriever,
    settings: OpenAISettings,
    config: AgentModelConfig | None = None,
) -> OrchestratorAgent:
    default_model = settings.openai_answer_model
    config = config or _default_agent_model_config(default_model)
    logger.info("Building orchestrator agent config=%s", config)
    planner_client = _llm_client(settings, config.orchestrator_model)
    search_client = _llm_client(settings, config.search_model)
    summary_client = _llm_client(settings, config.summarization_model)
    fact_check_client = _llm_client(settings, config.fact_check_model)
    synthesis_client = _llm_client(settings, config.final_synthesis_model)

    return OrchestratorAgent(
        llm_client=planner_client,
        search_agent=SearchAgent(retriever=retriever, llm_client=search_client),
        summarization_agent=SummarizationAgent(llm_client=summary_client),
        fact_checking_agent=FactCheckingAgent(llm_client=fact_check_client),
        final_synthesis_agent=FinalSynthesisAgent(llm_client=synthesis_client),
    )


async def _measure(label: str, run: Callable[[], Awaitable[object]]) -> tuple[object, float]:
    logger.info("Starting measured run label=%s", label)
    start = time.perf_counter()
    result = await run()
    latency_seconds = time.perf_counter() - start
    logger.info("Finished measured run label=%s latency_seconds=%.3f", label, latency_seconds)
    print(f"\n--- {label} ---")
    print(f"latency_seconds: {latency_seconds:.3f}")
    return result, latency_seconds


async def _compare_question(
    config: AgentModelConfig,
    experiment_name: str,
    question_index: int,
    question: str,
    baseline_agent: BaselineAgent,
    orchestrator_agent: OrchestratorAgent,
    top_k: int = 5,
) -> QuestionRunMetrics:
    logger.info(
        "Comparing question experiment=%s question_index=%s top_k=%s",
        experiment_name,
        question_index,
        top_k,
    )
    print(f"\n{'=' * 80}")
    print(experiment_name)
    print(f"question: {question}")
    print(f"top_k: {top_k}")

    baseline_result, baseline_latency = await _measure(
        "baseline",
        lambda: baseline_agent.answer(question, top_k=top_k),
    )
    _print_baseline_result(baseline_result, baseline_latency)

    orchestrator_result, orchestrator_latency = await _measure(
        "multi_agent_orchestrator",
        lambda: orchestrator_agent.answer(question, top_k=top_k),
    )
    _print_orchestrator_result(orchestrator_result, orchestrator_latency)

    print("\ncomparison")
    print(f"baseline_latency_seconds: {baseline_latency:.3f}")
    print(f"orchestrator_latency_seconds: {orchestrator_latency:.3f}")
    print(f"baseline_total_tokens: {_total_tokens(baseline_result.token_usage)}")
    print(f"orchestrator_total_tokens: {_total_tokens(orchestrator_result.token_usage)}")
    print(f"baseline_citation_count: {len(baseline_result.citations)}")
    print(f"orchestrator_evidence_count: {len(orchestrator_result.evidence)}")

    status_counts = _fact_check_status_counts(orchestrator_result)
    logger.info(
        "Question comparison complete experiment=%s question_index=%s baseline_latency=%.3f orchestrator_latency=%.3f",
        experiment_name,
        question_index,
        baseline_latency,
        orchestrator_latency,
    )
    return QuestionRunMetrics(
        experiment_slug=config.slug,
        experiment_name=experiment_name,
        question_index=question_index,
        question=question,
        top_k=top_k,
        baseline_latency_seconds=baseline_latency,
        orchestrator_latency_seconds=orchestrator_latency,
        baseline_token_usage=baseline_result.token_usage,
        orchestrator_token_usage=orchestrator_result.token_usage,
        baseline_citation_count=len(baseline_result.citations),
        orchestrator_evidence_count=len(orchestrator_result.evidence),
        fact_check_status_counts=status_counts,
        baseline_evidence=_baseline_evidence_payload(baseline_result),
        orchestrator_evidence=_orchestrator_evidence_payload(orchestrator_result),
        baseline_answer=baseline_result.answer,
        orchestrator_answer=orchestrator_result.answer,
    )


async def _run_agent_config_experiment(
    config: AgentModelConfig,
    baseline_agent: BaselineAgent,
    retriever: ResearchPaperRetriever,
    settings: OpenAISettings,
) -> None:
    logger.info("Starting experiment slug=%s name=%s", config.slug, config.name)
    print(f"\n\n{'#' * 80}")
    print(f"running {config.name}")
    _print_agent_config(config)

    orchestrator_agent = build_orchestrator_agent(retriever, settings, config)
    metrics: list[QuestionRunMetrics] = []
    for index, question in enumerate(QUESTIONS, start=1):
        metrics.append(
            await _compare_question(
                config=config,
                experiment_name=f"{config.name}: question {index}",
                question_index=index,
                question=question,
                baseline_agent=baseline_agent,
                orchestrator_agent=orchestrator_agent,
                top_k=config.top_k,
            )
        )

    output_dir = _save_experiment_results(config, metrics)
    await _judge_experiment_results(output_dir, settings)
    logger.info("Finished experiment slug=%s output_dir=%s", config.slug, output_dir)
    print(f"\nsaved_results: {output_dir}")


async def experiment1(
    baseline_agent: BaselineAgent,
    retriever: ResearchPaperRetriever,
    settings: OpenAISettings,
) -> None:
    default_model = settings.openai_answer_model
    config = AgentModelConfig(
        slug="experiment1_balanced",
        name="experiment1: balanced multi-agent config",
        top_k=5,
        orchestrator_model=_model_for("orchestrator", default_model),
        search_model=_model_for("search", default_model),
        summarization_model=_model_for("summarization", default_model),
        fact_check_model=_model_for("fact_check", default_model),
        final_synthesis_model=_model_for("final_synthesis", default_model),
    )
    await _run_agent_config_experiment(config, baseline_agent, retriever, settings)


async def experiment2(
    baseline_agent: BaselineAgent,
    retriever: ResearchPaperRetriever,
    settings: OpenAISettings,
) -> None:
    fast_model = os.getenv("FAST_AGENT_MODEL", settings.openai_answer_model)
    config = AgentModelConfig(
        slug="experiment2_fast_same_model",
        name="experiment2: fast same-model config",
        top_k=3,
        orchestrator_model=fast_model,
        search_model=fast_model,
        summarization_model=fast_model,
        fact_check_model=fast_model,
        final_synthesis_model=fast_model,
    )
    await _run_agent_config_experiment(config, baseline_agent, retriever, settings)


async def experiment3(
    baseline_agent: BaselineAgent,
    retriever: ResearchPaperRetriever,
    settings: OpenAISettings,
) -> None:
    default_model = settings.openai_answer_model
    strong_model = os.getenv("STRONG_AGENT_MODEL", default_model)
    fast_model = os.getenv("FAST_AGENT_MODEL", default_model)
    config = AgentModelConfig(
        slug="experiment3_strong_verifier_synthesizer",
        name="experiment3: strong verifier and synthesizer config",
        top_k=8,
        orchestrator_model=fast_model,
        search_model=fast_model,
        summarization_model=fast_model,
        fact_check_model=strong_model,
        final_synthesis_model=strong_model,
    )
    await _run_agent_config_experiment(config, baseline_agent, retriever, settings)


def _print_baseline_result(result: object, latency_seconds: float) -> None:
    if not isinstance(result, BaselineAgentResult):
        raise TypeError("Expected BaselineAgentResult")

    print(f"answer:\n{result.answer}")
    print(f"token_usage: {_format_usage(result.token_usage)}")
    print(f"citations_returned: {len(result.citations)}")
    for citation in result.citations:
        score = f"{citation.score:.4f}" if citation.score is not None else "unknown"
        print(f"  [{citation.number}] source={citation.source} chunk_id={citation.chunk_id} score={score}")


def _print_orchestrator_result(result: object, latency_seconds: float) -> None:
    if not isinstance(result, MultiAgentAnswer):
        raise TypeError("Expected MultiAgentAnswer")

    print(f"answer:\n{result.answer}")
    print(f"token_usage: {_format_usage(result.token_usage)}")
    print(f"plan_type: {result.plan.query_type}")
    print(f"plan_use_web: {result.plan.use_web}")
    print(f"plan_subquestions: {result.plan.subquestions}")
    print(f"agent_order: {result.plan.agent_order}")
    print(f"evidence_count: {len(result.evidence)}")
    for item in result.evidence:
        score = f"{item.score:.4f}" if item.score is not None else "unknown"
        print(f"  [{item.citation_id}] source={item.source} chunk_id={item.chunk_id} score={score}")

    status_counts = _fact_check_status_counts(result)
    print(f"fact_check_status_counts: {status_counts}")
    print(f"fact_check_needs_more_retrieval: {result.fact_check.needs_more_retrieval}")
    if result.fact_check.suggested_queries:
        print(f"fact_check_suggested_queries: {result.fact_check.suggested_queries}")


def _format_usage(token_usage: TokenUsage) -> str:
    return (
        f"input={token_usage.input_tokens or 0}, "
        f"output={token_usage.output_tokens or 0}, "
        f"total={token_usage.total_tokens or 0}"
    )


def _total_tokens(token_usage: TokenUsage) -> int:
    return token_usage.total_tokens or 0


def _fact_check_status_counts(result: MultiAgentAnswer) -> dict[str, int]:
    status_counts: dict[str, int] = {}
    for check in result.fact_check.checks:
        status_counts[check.status] = status_counts.get(check.status, 0) + 1
    return status_counts


def _baseline_evidence_payload(result: BaselineAgentResult) -> list[dict[str, object]]:
    evidence: list[dict[str, object]] = []
    for index, chunk in enumerate(result.retrieved_chunks, start=1):
        source = chunk.metadata.get("source") or chunk.metadata.get("filename") or "unknown source"
        evidence.append(
            {
                "citation_id": str(index),
                "chunk_id": chunk.id,
                "source": str(source),
                "score": chunk.score,
                "text": chunk.text,
            }
        )
    return evidence


def _orchestrator_evidence_payload(result: MultiAgentAnswer) -> list[dict[str, object]]:
    return [
        {
            "citation_id": item.citation_id,
            "chunk_id": item.chunk_id,
            "source": item.source,
            "score": item.score,
            "text": item.text,
        }
        for item in result.evidence
    ]


def _print_model_config(settings: OpenAISettings) -> None:
    default_model = settings.openai_answer_model
    print("model_config")
    print(f"  baseline: {_model_for('baseline', default_model)}")
    print(f"  orchestrator: {_model_for('orchestrator', default_model)}")
    print(f"  search: {_model_for('search', default_model)}")
    print(f"  summarization: {_model_for('summarization', default_model)}")
    print(f"  fact_check: {_model_for('fact_check', default_model)}")
    print(f"  final_synthesis: {_model_for('final_synthesis', default_model)}")
    print(f"  fast_agent: {os.getenv('FAST_AGENT_MODEL', default_model)}")
    print(f"  strong_agent: {os.getenv('STRONG_AGENT_MODEL', "gpt-4.1")}")
    print(f"  judge: {os.getenv('JUDGE_MODEL', 'gpt-5.1')}")
    print(f"  embedding: {settings.openai_embedding_model}")


def _default_agent_model_config(default_model: str) -> AgentModelConfig:
    return AgentModelConfig(
        slug="default",
        name="default",
        top_k=5,
        orchestrator_model=_model_for("orchestrator", default_model),
        search_model=_model_for("search", default_model),
        summarization_model=_model_for("summarization", default_model),
        fact_check_model=_model_for("fact_check", default_model),
        final_synthesis_model=_model_for("final_synthesis", default_model),
    )


def _print_agent_config(config: AgentModelConfig) -> None:
    print("agent_config")
    print(f"  top_k: {config.top_k}")
    print(f"  orchestrator: {config.orchestrator_model}")
    print(f"  search: {config.search_model}")
    print(f"  summarization: {config.summarization_model}")
    print(f"  fact_check: {config.fact_check_model}")
    print(f"  final_synthesis: {config.final_synthesis_model}")


def _save_experiment_results(config: AgentModelConfig, metrics: list[QuestionRunMetrics]) -> Path:
    output_dir = RESULTS_DIR / config.slug
    if output_dir.exists():
        logger.info("Removing existing result directory path=%s", output_dir)
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info("Saving experiment results path=%s metrics=%s", output_dir, len(metrics))

    _write_answers(output_dir, config, metrics)
    _write_metrics_json(output_dir, config, metrics)
    _plot_latency(output_dir, metrics)
    _plot_token_usage(output_dir, metrics)
    _plot_citations(output_dir, metrics)
    _plot_fact_check_statuses(output_dir, metrics)
    return output_dir


def _write_answers(output_dir: Path, config: AgentModelConfig, metrics: list[QuestionRunMetrics]) -> None:
    logger.info("Writing answers output_dir=%s", output_dir)
    lines = [
        f"# {config.name}",
        "",
        "## Agent Configuration",
        "",
        f"- top_k: {config.top_k}",
        f"- orchestrator_model: {config.orchestrator_model}",
        f"- search_model: {config.search_model}",
        f"- summarization_model: {config.summarization_model}",
        f"- fact_check_model: {config.fact_check_model}",
        f"- final_synthesis_model: {config.final_synthesis_model}",
        "",
    ]

    for metric in metrics:
        lines.extend(
            [
                f"## Question {metric.question_index}",
                "",
                metric.question,
                "",
                "### Baseline Answer",
                "",
                metric.baseline_answer,
                "",
                "### Multi-Agent Answer",
                "",
                metric.orchestrator_answer,
                "",
                "### Metrics",
                "",
                f"- baseline_latency_seconds: {metric.baseline_latency_seconds:.3f}",
                f"- orchestrator_latency_seconds: {metric.orchestrator_latency_seconds:.3f}",
                f"- baseline_total_tokens: {_total_tokens(metric.baseline_token_usage)}",
                f"- orchestrator_total_tokens: {_total_tokens(metric.orchestrator_token_usage)}",
                f"- baseline_citation_count: {metric.baseline_citation_count}",
                f"- orchestrator_evidence_count: {metric.orchestrator_evidence_count}",
                f"- fact_check_status_counts: {metric.fact_check_status_counts}",
                "",
            ]
        )

    (output_dir / "answers.md").write_text("\n".join(lines), encoding="utf-8")
    logger.info("Wrote answers file=%s", output_dir / "answers.md")


def _write_metrics_json(output_dir: Path, config: AgentModelConfig, metrics: list[QuestionRunMetrics]) -> None:
    logger.info("Writing metrics JSON output_dir=%s", output_dir)
    payload = {
        "config": asdict(config),
        "questions": [
            {
                **asdict(metric),
                "baseline_token_usage": asdict(metric.baseline_token_usage),
                "orchestrator_token_usage": asdict(metric.orchestrator_token_usage),
            }
            for metric in metrics
        ],
    }
    (output_dir / "metrics.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    logger.info("Wrote metrics file=%s", output_dir / "metrics.json")


def _plot_latency(output_dir: Path, metrics: list[QuestionRunMetrics]) -> None:
    logger.info("Plotting latency output_dir=%s", output_dir)
    labels = _question_labels(metrics)
    _bar_pair_plot(
        output_path=output_dir / "latency_seconds.png",
        title="Latency by Question",
        ylabel="seconds",
        labels=labels,
        baseline_values=[metric.baseline_latency_seconds for metric in metrics],
        orchestrator_values=[metric.orchestrator_latency_seconds for metric in metrics],
    )


def _plot_token_usage(output_dir: Path, metrics: list[QuestionRunMetrics]) -> None:
    logger.info("Plotting token usage output_dir=%s", output_dir)
    labels = _question_labels(metrics)
    _bar_pair_plot(
        output_path=output_dir / "token_usage_total.png",
        title="Total Token Usage by Question",
        ylabel="tokens",
        labels=labels,
        baseline_values=[_total_tokens(metric.baseline_token_usage) for metric in metrics],
        orchestrator_values=[_total_tokens(metric.orchestrator_token_usage) for metric in metrics],
    )


def _plot_citations(output_dir: Path, metrics: list[QuestionRunMetrics]) -> None:
    logger.info("Plotting citations/evidence output_dir=%s", output_dir)
    labels = _question_labels(metrics)
    _bar_pair_plot(
        output_path=output_dir / "citations_and_evidence.png",
        title="Citations and Evidence by Question",
        ylabel="count",
        labels=labels,
        baseline_values=[metric.baseline_citation_count for metric in metrics],
        orchestrator_values=[metric.orchestrator_evidence_count for metric in metrics],
        baseline_label="baseline citations",
        orchestrator_label="orchestrator evidence",
    )


def _plot_fact_check_statuses(output_dir: Path, metrics: list[QuestionRunMetrics]) -> None:
    logger.info("Plotting fact check statuses output_dir=%s", output_dir)
    labels = _question_labels(metrics)
    statuses = ["supported", "weakly_supported", "unsupported"]
    x_positions = list(range(len(metrics)))
    bottoms = [0 for _ in metrics]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    for status in statuses:
        values = [metric.fact_check_status_counts.get(status, 0) for metric in metrics]
        ax.bar(x_positions, values, bottom=bottoms, label=status)
        bottoms = [bottom + value for bottom, value in zip(bottoms, values)]

    ax.set_title("Fact Check Status Counts")
    ax.set_ylabel("claims")
    ax.set_xticks(x_positions)
    ax.set_xticklabels(labels)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_dir / "fact_check_statuses.png", dpi=160)
    plt.close(fig)
    logger.info("Saved plot file=%s", output_dir / "fact_check_statuses.png")


def _bar_pair_plot(
    output_path: Path,
    title: str,
    ylabel: str,
    labels: list[str],
    baseline_values: list[float],
    orchestrator_values: list[float],
    baseline_label: str = "baseline",
    orchestrator_label: str = "orchestrator",
) -> None:
    x_positions = list(range(len(labels)))
    width = 0.36
    baseline_positions = [position - width / 2 for position in x_positions]
    orchestrator_positions = [position + width / 2 for position in x_positions]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(baseline_positions, baseline_values, width=width, label=baseline_label)
    ax.bar(orchestrator_positions, orchestrator_values, width=width, label=orchestrator_label)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xticks(x_positions)
    ax.set_xticklabels(labels)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)
    logger.info("Saved plot file=%s", output_path)


def _question_labels(metrics: list[QuestionRunMetrics]) -> list[str]:
    return [f"Q{metric.question_index}" for metric in metrics]


async def _judge_experiment_results(output_dir: Path, settings: OpenAISettings) -> None:
    metrics_path = output_dir / "metrics.json"
    if not metrics_path.exists():
        logger.warning("No metrics file found for judge path=%s", metrics_path)
        return

    judge_model = os.getenv("JUDGE_MODEL", "gpt-5.1")
    logger.info("Starting judge pass output_dir=%s judge_model=%s", output_dir, judge_model)
    judge_client = _llm_client(settings, judge_model)

    payload = json.loads(metrics_path.read_text(encoding="utf-8"))
    questions = payload.get("questions") if isinstance(payload, dict) else None
    if not isinstance(questions, list):
        logger.warning("Metrics file does not contain question list path=%s", metrics_path)
        return

    scores: list[dict[str, object]] = []
    for question in questions:
        if not isinstance(question, dict):
            continue
        question_index = _optional_int(question.get("question_index")) or 0
        question_text = str(question.get("question", ""))
        logger.info("Judging experiment=%s question=%s baseline", output_dir.name, question_index)
        scores.append(
            await _judge_single_answer(
                judge_client=judge_client,
                judge_model=judge_model,
                experiment_slug=output_dir.name,
                system_name="baseline",
                question_index=question_index,
                question=question_text,
                answer=str(question.get("baseline_answer", "")),
                evidence=_list_of_dicts(question.get("baseline_evidence")),
            )
        )
        logger.info("Judging experiment=%s question=%s multi_agent", output_dir.name, question_index)
        scores.append(
            await _judge_single_answer(
                judge_client=judge_client,
                judge_model=judge_model,
                experiment_slug=output_dir.name,
                system_name="multi_agent",
                question_index=question_index,
                question=question_text,
                answer=str(question.get("orchestrator_answer", "")),
                evidence=_list_of_dicts(question.get("orchestrator_evidence")),
            )
        )

    _write_judge_scores(output_dir, judge_model, scores)
    _plot_judge_scores(output_dir, scores)
    logger.info("Judge pass complete output_dir=%s scores=%s", output_dir, len(scores))


async def _judge_single_answer(
    judge_client: LLMClient,
    judge_model: str,
    experiment_slug: str,
    system_name: str,
    question_index: int,
    question: str,
    answer: str,
    evidence: list[dict[str, object]],
) -> dict[str, object]:
    evidence_text = _format_judge_evidence(evidence)
    prompt = f"""Evaluate the answer against the question and provided evidence.

Return only JSON with this exact shape:
{{
  "factual_accuracy": 1,
  "completeness": 1,
  "citation_quality": 1,
  "clarity": 1,
  "unsupported_claims": 0,
  "rationale": "short explanation"
}}

Scoring:
- factual_accuracy: 1-5, where 5 means all important claims are supported by the evidence.
- completeness: 1-5, where 5 means the answer fully addresses the question.
- citation_quality: 1-5, where 5 means citations are present, valid, specific, and tied to claims.
- clarity: 1-5, where 5 means clear, well organized, and easy to follow.
- unsupported_claims: count claims in the answer that are not supported by the evidence.

Question:
{question}

Evidence:
{evidence_text}

Answer:
{answer}
"""
    completion = await judge_client.complete(
        prompt,
        instructions=(
            "You are an external research QA evaluator. Judge only against the provided evidence. "
            "Be strict about unsupported claims and citation quality. Return valid JSON only."
        ),
        max_output_tokens=800,
    )
    parsed = _parse_judge_response(completion.text)
    parsed.update(
        {
            "experiment_slug": experiment_slug,
            "system": system_name,
            "question_index": question_index,
            "question": question,
            "judge_model": judge_model,
            "judge_token_usage": asdict(completion.token_usage),
        }
    )
    return parsed


def _parse_judge_response(text: str) -> dict[str, object]:
    try:
        payload = json.loads(_extract_json_object(text))
    except json.JSONDecodeError:
        logger.warning("Could not parse judge JSON response; using fallback scores text=%s", text[:500])
        payload = {}

    return {
        "factual_accuracy": _clamp_score(payload.get("factual_accuracy")),
        "completeness": _clamp_score(payload.get("completeness")),
        "citation_quality": _clamp_score(payload.get("citation_quality")),
        "clarity": _clamp_score(payload.get("clarity")),
        "unsupported_claims": max(0, _optional_int(payload.get("unsupported_claims")) or 0),
        "rationale": str(payload.get("rationale", "")),
    }


def _extract_json_object(text: str) -> str:
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise json.JSONDecodeError("No JSON object found", text, 0)
    return text[start : end + 1]


def _clamp_score(value: object) -> int:
    if isinstance(value, bool):
        return 1
    if isinstance(value, (int, float)):
        return min(5, max(1, int(round(value))))
    return 1


def _format_judge_evidence(evidence: list[dict[str, object]]) -> str:
    if not evidence:
        return "No evidence provided."
    blocks: list[str] = []
    for item in evidence[:12]:
        citation_id = item.get("citation_id", "?")
        source = item.get("source", "unknown source")
        text = str(item.get("text", ""))[:2500]
        blocks.append(f"[{citation_id}] source: {source}\n{text}")
    return "\n\n".join(blocks)


def _write_judge_scores(output_dir: Path, judge_model: str, scores: list[dict[str, object]]) -> None:
    json_path = output_dir / "judge_scores.json"
    json_path.write_text(json.dumps({"judge_model": judge_model, "scores": scores}, indent=2), encoding="utf-8")

    lines = [
        "# External Judge Scores",
        "",
        f"Judge model: `{judge_model}`",
        "",
        "| System | Question | Factual Accuracy | Completeness | Citation Quality | Clarity | Unsupported Claims |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for score in scores:
        lines.append(
            "| {system} | Q{question} | {factual} | {complete} | {citation} | {clarity} | {unsupported} |".format(
                system=score["system"],
                question=score["question_index"],
                factual=score["factual_accuracy"],
                complete=score["completeness"],
                citation=score["citation_quality"],
                clarity=score["clarity"],
                unsupported=score["unsupported_claims"],
            )
        )
    md_path = output_dir / "judge_scores.md"
    md_path.write_text("\n".join(lines), encoding="utf-8")
    logger.info("Wrote judge scores files json=%s markdown=%s", json_path, md_path)


def _plot_judge_scores(output_dir: Path, scores: list[dict[str, object]]) -> None:
    metrics = ["factual_accuracy", "completeness", "citation_quality", "clarity"]
    for metric in metrics:
        _bar_pair_plot(
            output_path=output_dir / f"judge_{metric}.png",
            title=f"Judge {metric.replace('_', ' ').title()}",
            ylabel="score",
            labels=_judge_question_labels(scores),
            baseline_values=_judge_values(scores, "baseline", metric),
            orchestrator_values=_judge_values(scores, "multi_agent", metric),
        )
    _bar_pair_plot(
        output_path=output_dir / "judge_unsupported_claims.png",
        title="Judge Unsupported Claims",
        ylabel="count",
        labels=_judge_question_labels(scores),
        baseline_values=_judge_values(scores, "baseline", "unsupported_claims"),
        orchestrator_values=_judge_values(scores, "multi_agent", "unsupported_claims"),
    )


def _judge_question_labels(scores: list[dict[str, object]]) -> list[str]:
    question_ids = sorted({_optional_int(score.get("question_index")) or 0 for score in scores})
    return [f"Q{question_id}" for question_id in question_ids]


def _judge_values(scores: list[dict[str, object]], system: str, metric: str) -> list[float]:
    values: list[float] = []
    for question_id in sorted({_optional_int(score.get("question_index")) or 0 for score in scores}):
        match = next(
            (
                score
                for score in scores
                if score.get("system") == system and (_optional_int(score.get("question_index")) or 0) == question_id
            ),
            None,
        )
        values.append(_float_value(match.get(metric)) if match else 0.0)
    return values


def _list_of_dicts(value: object) -> list[dict[str, object]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _save_summary_results() -> None:
    logger.info("Generating cross-experiment summary from persisted metrics")
    experiment_metrics = _load_persisted_experiment_metrics()
    if not experiment_metrics:
        logger.warning("No experiment metrics found; skipping summary generation")
        return

    output_dir = RESULTS_DIR / "summary"
    if output_dir.exists():
        logger.info("Removing existing summary directory path=%s", output_dir)
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    for slug, payload in experiment_metrics:
        row = _summarize_experiment(slug, payload)
        _add_judge_summary(row, RESULTS_DIR / slug / "judge_scores.json")
        rows.append(row)
    _write_summary_json(output_dir, rows)
    _write_summary_markdown(output_dir, rows)
    _plot_summary_latency(output_dir, rows)
    _plot_summary_token_usage(output_dir, rows)
    _plot_summary_citations(output_dir, rows)
    _plot_summary_fact_checks(output_dir, rows)
    _plot_summary_judge_scores(output_dir, rows)
    logger.info("Summary results saved output_dir=%s experiments=%s", output_dir, len(rows))


def _load_persisted_experiment_metrics() -> list[tuple[str, dict[str, object]]]:
    metrics: list[tuple[str, dict[str, object]]] = []
    if not RESULTS_DIR.exists():
        return metrics

    for metrics_path in sorted(RESULTS_DIR.glob("experiment*/metrics.json")):
        try:
            payload = json.loads(metrics_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            logger.warning("Skipping invalid metrics file path=%s", metrics_path)
            continue
        if not isinstance(payload, dict):
            logger.warning("Skipping metrics file with invalid shape path=%s", metrics_path)
            continue
        metrics.append((metrics_path.parent.name, payload))
    return metrics


def _summarize_experiment(slug: str, payload: dict[str, object]) -> dict[str, object]:
    config = payload.get("config")
    questions = payload.get("questions")
    if not isinstance(config, dict):
        config = {}
    if not isinstance(questions, list):
        questions = []

    baseline_latencies = [_float_from_question(question, "baseline_latency_seconds") for question in questions]
    orchestrator_latencies = [_float_from_question(question, "orchestrator_latency_seconds") for question in questions]
    baseline_tokens = [_token_total_from_question(question, "baseline_token_usage") for question in questions]
    orchestrator_tokens = [_token_total_from_question(question, "orchestrator_token_usage") for question in questions]
    baseline_citations = [_int_from_question(question, "baseline_citation_count") for question in questions]
    orchestrator_evidence = [_int_from_question(question, "orchestrator_evidence_count") for question in questions]
    fact_counts = _sum_fact_check_counts(questions)

    return {
        "slug": slug,
        "name": str(config.get("name", slug)),
        "top_k": _optional_int(config.get("top_k")) or 0,
        "orchestrator_model": str(config.get("orchestrator_model", "")),
        "search_model": str(config.get("search_model", "")),
        "summarization_model": str(config.get("summarization_model", "")),
        "fact_check_model": str(config.get("fact_check_model", "")),
        "final_synthesis_model": str(config.get("final_synthesis_model", "")),
        "question_count": len(questions),
        "avg_baseline_latency_seconds": _avg(baseline_latencies),
        "avg_orchestrator_latency_seconds": _avg(orchestrator_latencies),
        "avg_baseline_total_tokens": _avg(baseline_tokens),
        "avg_orchestrator_total_tokens": _avg(orchestrator_tokens),
        "avg_baseline_citation_count": _avg(baseline_citations),
        "avg_orchestrator_evidence_count": _avg(orchestrator_evidence),
        "fact_check_status_counts": fact_counts,
        "avg_supported_claims": fact_counts.get("supported", 0) / len(questions) if questions else 0.0,
        "avg_weakly_supported_claims": fact_counts.get("weakly_supported", 0) / len(questions) if questions else 0.0,
        "avg_unsupported_claims": fact_counts.get("unsupported", 0) / len(questions) if questions else 0.0,
    }


def _add_judge_summary(row: dict[str, object], judge_path: Path) -> None:
    if not judge_path.exists():
        logger.warning("Judge scores not found for summary path=%s", judge_path)
        return
    try:
        payload = json.loads(judge_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        logger.warning("Invalid judge scores JSON path=%s", judge_path)
        return

    scores = payload.get("scores") if isinstance(payload, dict) else None
    if not isinstance(scores, list):
        return
    row["judge_model"] = str(payload.get("judge_model", ""))
    for system in ("baseline", "multi_agent"):
        system_scores = [score for score in scores if isinstance(score, dict) and score.get("system") == system]
        for metric in ("factual_accuracy", "completeness", "citation_quality", "clarity", "unsupported_claims"):
            row[f"judge_avg_{system}_{metric}"] = _avg([_float_value(score.get(metric)) for score in system_scores])


def _write_summary_json(output_dir: Path, rows: list[dict[str, object]]) -> None:
    path = output_dir / "summary_metrics.json"
    path.write_text(json.dumps({"experiments": rows}, indent=2), encoding="utf-8")
    logger.info("Wrote summary metrics file=%s", path)


def _write_summary_markdown(output_dir: Path, rows: list[dict[str, object]]) -> None:
    lines = [
        "# Cross-Experiment Summary",
        "",
        "This summary is generated from the persisted `metrics.json` files in each experiment folder.",
        "",
        "| Experiment | top_k | Avg Baseline Latency | Avg Multi-Agent Latency | Avg Baseline Tokens | Avg Multi-Agent Tokens | Avg Baseline Citations | Avg Multi-Agent Evidence | Unsupported Claims/Q |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            "| {name} | {top_k} | {baseline_latency:.3f}s | {orchestrator_latency:.3f}s | {baseline_tokens:.1f} | {orchestrator_tokens:.1f} | {baseline_citations:.1f} | {orchestrator_evidence:.1f} | {unsupported:.2f} |".format(
                name=row["name"],
                top_k=row["top_k"],
                baseline_latency=row["avg_baseline_latency_seconds"],
                orchestrator_latency=row["avg_orchestrator_latency_seconds"],
                baseline_tokens=row["avg_baseline_total_tokens"],
                orchestrator_tokens=row["avg_orchestrator_total_tokens"],
                baseline_citations=row["avg_baseline_citation_count"],
                orchestrator_evidence=row["avg_orchestrator_evidence_count"],
                unsupported=row["avg_unsupported_claims"],
            )
        )

    lines.extend(["", "## Model Configurations", ""])
    for row in rows:
        lines.extend(
            [
                f"### {row['name']}",
                "",
                f"- orchestrator_model: {row['orchestrator_model']}",
                f"- search_model: {row['search_model']}",
                f"- summarization_model: {row['summarization_model']}",
                f"- fact_check_model: {row['fact_check_model']}",
                f"- final_synthesis_model: {row['final_synthesis_model']}",
                f"- judge_model: {row.get('judge_model', '')}",
                "",
            ]
        )

    lines.extend(
        [
            "",
            "## External Judge Averages",
            "",
            "| Experiment | System | Factual Accuracy | Completeness | Citation Quality | Clarity | Unsupported Claims |",
            "|---|---|---:|---:|---:|---:|---:|",
        ]
    )
    for row in rows:
        for system in ("baseline", "multi_agent"):
            lines.append(
                "| {name} | {system} | {factual:.2f} | {complete:.2f} | {citation:.2f} | {clarity:.2f} | {unsupported:.2f} |".format(
                    name=row["name"],
                    system=system,
                    factual=_float_value(row.get(f"judge_avg_{system}_factual_accuracy")),
                    complete=_float_value(row.get(f"judge_avg_{system}_completeness")),
                    citation=_float_value(row.get(f"judge_avg_{system}_citation_quality")),
                    clarity=_float_value(row.get(f"judge_avg_{system}_clarity")),
                    unsupported=_float_value(row.get(f"judge_avg_{system}_unsupported_claims")),
                )
            )

    path = output_dir / "summary.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    logger.info("Wrote summary markdown file=%s", path)


def _plot_summary_latency(output_dir: Path, rows: list[dict[str, object]]) -> None:
    _bar_pair_plot(
        output_path=output_dir / "avg_latency_seconds.png",
        title="Average Latency Across Experiments",
        ylabel="seconds",
        labels=_summary_labels(rows),
        baseline_values=[float(row["avg_baseline_latency_seconds"]) for row in rows],
        orchestrator_values=[float(row["avg_orchestrator_latency_seconds"]) for row in rows],
    )


def _plot_summary_token_usage(output_dir: Path, rows: list[dict[str, object]]) -> None:
    _bar_pair_plot(
        output_path=output_dir / "avg_token_usage_total.png",
        title="Average Token Usage Across Experiments",
        ylabel="tokens",
        labels=_summary_labels(rows),
        baseline_values=[float(row["avg_baseline_total_tokens"]) for row in rows],
        orchestrator_values=[float(row["avg_orchestrator_total_tokens"]) for row in rows],
    )


def _plot_summary_citations(output_dir: Path, rows: list[dict[str, object]]) -> None:
    _bar_pair_plot(
        output_path=output_dir / "avg_citations_and_evidence.png",
        title="Average Citations and Evidence Across Experiments",
        ylabel="count",
        labels=_summary_labels(rows),
        baseline_values=[float(row["avg_baseline_citation_count"]) for row in rows],
        orchestrator_values=[float(row["avg_orchestrator_evidence_count"]) for row in rows],
        baseline_label="baseline citations",
        orchestrator_label="orchestrator evidence",
    )


def _plot_summary_fact_checks(output_dir: Path, rows: list[dict[str, object]]) -> None:
    labels = _summary_labels(rows)
    statuses = ["supported", "weakly_supported", "unsupported"]
    x_positions = list(range(len(rows)))
    bottoms = [0.0 for _ in rows]

    fig, ax = plt.subplots(figsize=(9, 4.8))
    for status in statuses:
        values = [float(row.get(f"avg_{status}_claims", 0.0)) for row in rows]
        ax.bar(x_positions, values, bottom=bottoms, label=status)
        bottoms = [bottom + value for bottom, value in zip(bottoms, values)]

    ax.set_title("Average Fact Check Status Counts Across Experiments")
    ax.set_ylabel("claims per question")
    ax.set_xticks(x_positions)
    ax.set_xticklabels(labels)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_dir / "avg_fact_check_statuses.png", dpi=160)
    plt.close(fig)
    logger.info("Saved summary plot file=%s", output_dir / "avg_fact_check_statuses.png")


def _plot_summary_judge_scores(output_dir: Path, rows: list[dict[str, object]]) -> None:
    for metric in ("factual_accuracy", "completeness", "citation_quality", "clarity", "unsupported_claims"):
        _bar_pair_plot(
            output_path=output_dir / f"judge_avg_{metric}.png",
            title=f"Average Judge {metric.replace('_', ' ').title()} Across Experiments",
            ylabel="count" if metric == "unsupported_claims" else "score",
            labels=_summary_labels(rows),
            baseline_values=[_float_value(row.get(f"judge_avg_baseline_{metric}")) for row in rows],
            orchestrator_values=[_float_value(row.get(f"judge_avg_multi_agent_{metric}")) for row in rows],
        )


def _summary_labels(rows: list[dict[str, object]]) -> list[str]:
    return [f"E{index}" for index, _ in enumerate(rows, start=1)]


def _float_from_question(question: object, key: str) -> float:
    if not isinstance(question, dict):
        return 0.0
    value = question.get(key)
    if isinstance(value, bool):
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    return 0.0


def _float_value(value: object) -> float:
    if isinstance(value, bool):
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    return 0.0


def _int_from_question(question: object, key: str) -> int:
    if not isinstance(question, dict):
        return 0
    return _optional_int(question.get(key)) or 0


def _token_total_from_question(question: object, key: str) -> int:
    if not isinstance(question, dict):
        return 0
    token_usage = question.get(key)
    if not isinstance(token_usage, dict):
        return 0
    return _optional_int(token_usage.get("total_tokens")) or 0


def _sum_fact_check_counts(questions: list[object]) -> dict[str, int]:
    totals = {"supported": 0, "weakly_supported": 0, "unsupported": 0}
    for question in questions:
        if not isinstance(question, dict):
            continue
        counts = question.get("fact_check_status_counts")
        if not isinstance(counts, dict):
            continue
        for status in totals:
            totals[status] += _optional_int(counts.get(status)) or 0
    return totals


def _avg(values: list[float | int]) -> float:
    return sum(values) / len(values) if values else 0.0


def _optional_int(value: object) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    return None


async def _ingest_data(embedder: OpenAIEmbedder, vector_store: PineconeVectorStore) -> None:
    logger.info("Starting pre-experiment ingestion")
    print("\ningestion")
    start = time.perf_counter()
    ingestor = ResearchPaperIngestor(embedder=embedder, vector_store=vector_store, data_dir="data")
    result = await ingestor.ingest()
    latency_seconds = time.perf_counter() - start

    print(f"files_seen: {len(result.files)}")
    print(f"new_chunks_indexed: {result.chunk_count}")
    print(f"files_skipped: {result.skipped_file_count}")
    print(f"latency_seconds: {latency_seconds:.3f}")
    for file_result in result.files:
        status = "skipped" if file_result.skipped else "indexed"
        print(f"  {file_result.path}: {file_result.chunk_count} chunks ({status})")
    logger.info(
        "Pre-experiment ingestion complete files=%s chunks=%s latency_seconds=%.3f",
        len(result.files),
        result.chunk_count,
        latency_seconds,
    )


async def main() -> None:
    load_dotenv()
    _configure_logging()
    logger.info("Starting experiment runner")

    openai_settings = OpenAISettings.from_env()
    pinecone_settings = PineconeSettings.from_env()
    logger.info(
        "Loaded settings answer_model=%s embedding_model=%s pinecone_host=%s pinecone_index=%s",
        openai_settings.openai_answer_model,
        openai_settings.openai_embedding_model,
        pinecone_settings.pinecone_host,
        pinecone_settings.pinecone_index_name,
    )

    _print_model_config(openai_settings)
    print(f"pinecone_index: {pinecone_settings.pinecone_index_name}")
    print(f"pinecone_namespace: {pinecone_settings.pinecone_namespace}")

    shared_llm_client = _llm_client(openai_settings)
    embedder = OpenAIEmbedder(shared_llm_client)
    vector_store = PineconeVectorStore(pinecone_settings)
    await _ingest_data(embedder, vector_store)
    retriever = ResearchPaperRetriever(embedder=embedder, vector_store=vector_store)

    baseline_agent = build_baseline_agent(retriever, openai_settings)

    experiments: list[ExperimentFn] = [experiment1, experiment2, experiment3]
    for experiment in experiments:
        logger.info("Dispatching experiment function=%s", experiment.__name__)
        await experiment(baseline_agent, retriever, openai_settings)
    _save_summary_results()
    logger.info("Experiment runner complete")


if __name__ == "__main__":
    asyncio.run(main())
