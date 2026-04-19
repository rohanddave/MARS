# Cross-Experiment Summary

This summary is generated from the persisted `metrics.json` files in each experiment folder.

| Experiment | top_k | Avg Baseline Latency | Avg Multi-Agent Latency | Avg Baseline Tokens | Avg Multi-Agent Tokens | Avg Baseline Citations | Avg Multi-Agent Evidence | Unsupported Claims/Q |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| experiment1: balanced multi-agent config | 5 | 3.776s | 48.824s | 1714.3 | 18228.0 | 5.0 | 12.3 | 0.00 |
| experiment2: fast same-model config | 3 | 4.860s | 36.977s | 1173.7 | 12301.3 | 3.0 | 8.0 | 0.00 |
| experiment3: strong verifier and synthesizer config | 8 | 5.340s | 61.491s | 2247.0 | 27063.0 | 8.0 | 20.0 | 0.00 |

## Model Configurations

### experiment1: balanced multi-agent config

- orchestrator_model: gpt-4.1-mini
- search_model: gpt-4.1-mini
- summarization_model: gpt-4.1-mini
- fact_check_model: gpt-4.1-mini
- final_synthesis_model: gpt-4.1-mini

### experiment2: fast same-model config

- orchestrator_model: gpt-4.1-mini
- search_model: gpt-4.1-mini
- summarization_model: gpt-4.1-mini
- fact_check_model: gpt-4.1-mini
- final_synthesis_model: gpt-4.1-mini

### experiment3: strong verifier and synthesizer config

- orchestrator_model: gpt-4.1-mini
- search_model: gpt-4.1-mini
- summarization_model: gpt-4.1-mini
- fact_check_model: gpt-4.1-mini
- final_synthesis_model: gpt-4.1-mini
