# Cross-Experiment Summary

This summary is generated from the persisted `metrics.json` files in each experiment folder.

| Experiment | top_k | Avg Baseline Latency | Avg Multi-Agent Latency | Avg Baseline Tokens | Avg Multi-Agent Tokens | Avg Baseline Citations | Avg Multi-Agent Evidence | Unsupported Claims/Q |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| experiment1: balanced evidence config | 5 | 4.105s | 41.774s | 2163.5 | 13957.9 | 5.0 | 16.8 | 1.40 |
| experiment2: precision small-context config | 3 | 3.767s | 32.043s | 1551.8 | 9440.5 | 3.0 | 11.4 | 1.20 |
| experiment3: high-recall strong verifier/synthesizer config | 8 | 4.500s | 42.586s | 2893.5 | 16081.6 | 8.0 | 20.9 | 0.27 |

## Question Coverage

- experiment1: balanced evidence config: citation grounding / uncertainty: 1, comparison: 2, definition: 2, easy lookup: 2, evidence synthesis: 1, evidence synthesis / ablation: 1, limitation/uncertainty: 1, method/mechanism: 2, method/mechanism / implementation: 1, multi-step reasoning: 1, multi-step reasoning / error analysis: 1
- experiment2: precision small-context config: citation grounding / uncertainty: 1, comparison: 2, definition: 2, easy lookup: 2, evidence synthesis: 1, evidence synthesis / ablation: 1, limitation/uncertainty: 1, method/mechanism: 2, method/mechanism / implementation: 1, multi-step reasoning: 1, multi-step reasoning / error analysis: 1
- experiment3: high-recall strong verifier/synthesizer config: citation grounding / uncertainty: 1, comparison: 2, definition: 2, easy lookup: 2, evidence synthesis: 1, evidence synthesis / ablation: 1, limitation/uncertainty: 1, method/mechanism: 2, method/mechanism / implementation: 1, multi-step reasoning: 1, multi-step reasoning / error analysis: 1

## Model Configurations

### experiment1: balanced evidence config

- orchestrator_model: gpt-4.1-mini
- search_model: gpt-4.1-mini
- summarization_model: gpt-4.1-mini
- fact_check_model: gpt-4.1-mini
- final_synthesis_model: gpt-4.1-mini
- judge_model: gpt-5.1

### experiment2: precision small-context config

- orchestrator_model: gpt-4.1-mini
- search_model: gpt-4.1-mini
- summarization_model: gpt-4.1-mini
- fact_check_model: gpt-4.1-mini
- final_synthesis_model: gpt-4.1-mini
- judge_model: gpt-5.1

### experiment3: high-recall strong verifier/synthesizer config

- orchestrator_model: gpt-4.1-mini
- search_model: gpt-4.1-mini
- summarization_model: gpt-4.1-mini
- fact_check_model: gpt-4.1
- final_synthesis_model: gpt-4.1
- judge_model: gpt-5.1


## External Judge Averages

| Experiment | System | Factual Accuracy | Completeness | Citation Quality | Clarity | Unsupported Claims |
|---|---|---:|---:|---:|---:|---:|
| experiment1: balanced evidence config | baseline | 3.87 | 3.40 | 3.00 | 4.67 | 1.67 |
| experiment1: balanced evidence config | multi_agent | 4.00 | 3.13 | 3.67 | 4.33 | 1.20 |
| experiment2: precision small-context config | baseline | 4.20 | 3.53 | 3.40 | 4.53 | 1.00 |
| experiment2: precision small-context config | multi_agent | 4.00 | 3.20 | 3.40 | 4.47 | 0.93 |
| experiment3: high-recall strong verifier/synthesizer config | baseline | 4.33 | 4.13 | 3.13 | 4.67 | 1.20 |
| experiment3: high-recall strong verifier/synthesizer config | multi_agent | 4.07 | 3.53 | 3.80 | 4.67 | 0.87 |