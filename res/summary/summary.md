# Cross-Experiment Summary

This summary is generated from the persisted `metrics.json` files in each experiment folder.

| Experiment | top_k | Avg Baseline Latency | Avg Multi-Agent Latency | Avg Baseline Tokens | Avg Multi-Agent Tokens | Avg Baseline Citations | Avg Multi-Agent Evidence | Unsupported Claims/Q |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| experiment1: balanced multi-agent config | 5 | 5.124s | 66.365s | 1739.7 | 27738.3 | 5.0 | 17.7 | 1.00 |
| experiment2: fast same-model config | 3 | 4.483s | 57.707s | 1205.7 | 22040.7 | 3.0 | 11.7 | 2.00 |
| experiment3: strong verifier and synthesizer config | 8 | 3.964s | 78.120s | 2143.0 | 37065.3 | 8.0 | 23.7 | 1.00 |

## Model Configurations

### experiment1: balanced multi-agent config

- orchestrator_model: gpt-4.1-mini
- search_model: gpt-4.1-mini
- summarization_model: gpt-4.1-mini
- fact_check_model: gpt-4.1-mini
- final_synthesis_model: gpt-4.1-mini
- judge_model: gpt-5.1

### experiment2: fast same-model config

- orchestrator_model: gpt-4.1-mini
- search_model: gpt-4.1-mini
- summarization_model: gpt-4.1-mini
- fact_check_model: gpt-4.1-mini
- final_synthesis_model: gpt-4.1-mini
- judge_model: gpt-5.1

### experiment3: strong verifier and synthesizer config

- orchestrator_model: gpt-4.1-mini
- search_model: gpt-4.1-mini
- summarization_model: gpt-4.1-mini
- fact_check_model: gpt-4.1-mini
- final_synthesis_model: gpt-4.1-mini
- judge_model: gpt-5.1


## External Judge Averages

| Experiment | System | Factual Accuracy | Completeness | Citation Quality | Clarity | Unsupported Claims |
|---|---|---:|---:|---:|---:|---:|
| experiment1: balanced multi-agent config | baseline | 4.33 | 3.67 | 3.33 | 4.67 | 1.33 |
| experiment1: balanced multi-agent config | multi_agent | 3.33 | 3.33 | 2.33 | 4.67 | 2.67 |
| experiment2: fast same-model config | baseline | 3.00 | 3.00 | 3.00 | 3.67 | 2.67 |
| experiment2: fast same-model config | multi_agent | 4.33 | 4.00 | 3.67 | 5.00 | 0.67 |
| experiment3: strong verifier and synthesizer config | baseline | 3.67 | 3.33 | 3.00 | 4.00 | 2.00 |
| experiment3: strong verifier and synthesizer config | multi_agent | 3.33 | 3.33 | 2.33 | 4.33 | 3.33 |