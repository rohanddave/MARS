# Cross-Experiment Summary

This summary is generated from the persisted `metrics.json` files in each experiment folder.

| Experiment | top_k | Avg Baseline Latency | Avg Multi-Agent Latency | Avg Baseline Tokens | Avg Multi-Agent Tokens | Avg Baseline Citations | Avg Multi-Agent Evidence | Unsupported Claims/Q |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| experiment1: balanced multi-agent config | 5 | 4.190s | 60.986s | 1723.0 | 28677.0 | 5.0 | 16.3 | 1.00 |
| experiment2: fast same-model config | 3 | 4.308s | 48.036s | 1160.0 | 17525.7 | 3.0 | 10.7 | 1.33 |
| experiment3: strong verifier and synthesizer config | 8 | 4.766s | 60.450s | 2201.7 | 29371.0 | 8.0 | 21.0 | 0.00 |

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
- fact_check_model: gpt-4.1
- final_synthesis_model: gpt-4.1
- judge_model: gpt-5.1


## External Judge Averages

| Experiment | System | Factual Accuracy | Completeness | Citation Quality | Clarity | Unsupported Claims |
|---|---|---:|---:|---:|---:|---:|
| experiment1: balanced multi-agent config | baseline | 4.00 | 3.67 | 2.67 | 4.33 | 1.33 |
| experiment1: balanced multi-agent config | multi_agent | 2.67 | 3.00 | 2.33 | 4.67 | 3.00 |
| experiment2: fast same-model config | baseline | 3.33 | 3.00 | 2.00 | 4.00 | 2.33 |
| experiment2: fast same-model config | multi_agent | 4.00 | 3.33 | 3.33 | 4.67 | 1.33 |
| experiment3: strong verifier and synthesizer config | baseline | 3.00 | 3.33 | 3.33 | 3.67 | 2.33 |
| experiment3: strong verifier and synthesizer config | multi_agent | 3.33 | 3.33 | 2.33 | 4.33 | 3.00 |