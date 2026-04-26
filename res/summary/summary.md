# Cross-Experiment Summary

This summary is generated from the persisted `metrics.json` files in each experiment folder.

| Experiment | Family | Control Variable | top_k | Avg Baseline Latency | Avg Multi-Agent Latency | Avg Baseline Tokens | Avg Multi-Agent Tokens | Avg Baseline Citations | Avg Multi-Agent Evidence | Unsupported Claims/Q |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| experiment01: architecture control, all small models, top_k=5 | architecture_control | agent_architecture | 5 | 6.411s | 47.791s | 5272.0 | 30125.2 | 5.0 | 8.4 | 1.33 |
| experiment02: model ablation, strong orchestrator only, top_k=5 | model_ablation | orchestrator_model | 5 | 5.954s | 45.986s | 5237.5 | 28979.2 | 5.0 | 8.9 | 0.60 |
| experiment03: model ablation, strong search agent only, top_k=5 | model_ablation | search_model | 5 | 6.155s | 49.103s | 5262.0 | 31368.1 | 5.0 | 8.5 | 1.00 |
| experiment04: model ablation, strong summarizer only, top_k=5 | model_ablation | summarization_model | 5 | 6.221s | 42.805s | 5262.9 | 26844.7 | 5.0 | 9.1 | 0.53 |
| experiment05: model ablation, strong fact checker only, top_k=5 | model_ablation | fact_check_model | 5 | 5.903s | 42.002s | 5250.2 | 27957.7 | 5.0 | 8.3 | 1.00 |
| experiment06: model ablation, strong final synthesizer only, top_k=5 | model_ablation | final_synthesis_model | 5 | 5.748s | 47.961s | 5257.9 | 31513.9 | 5.0 | 8.5 | 1.20 |
| experiment07: model interaction, strong checker and synthesizer, top_k=5 | model_interaction | fact_check_and_final_synthesis_models | 5 | 5.801s | 43.517s | 5267.8 | 29075.0 | 5.0 | 8.4 | 1.13 |
| experiment08: upper bound, all strong models, top_k=5 | model_upper_bound | all_agent_models | 5 | 5.542s | 42.675s | 5239.1 | 28729.9 | 5.0 | 8.3 | 0.93 |
| experiment09: retrieval sweep, all small models, top_k=3 | top_k_sweep | top_k | 3 | 4.673s | 27.606s | 3079.5 | 17600.3 | 3.0 | 5.4 | 0.73 |
| experiment10: retrieval sweep, all small models, top_k=8 | top_k_sweep | top_k | 8 | 6.685s | 66.811s | 8214.9 | 47522.2 | 8.0 | 12.6 | 1.33 |
| experiment11: retrieval sweep, strong checker and synthesizer, top_k=3 | top_k_sweep | top_k | 3 | 5.168s | 30.814s | 3074.2 | 18039.6 | 3.0 | 5.8 | 0.80 |
| experiment12: retrieval sweep, strong checker and synthesizer, top_k=8 | top_k_sweep | top_k | 8 | 6.623s | 69.539s | 8197.0 | 48333.5 | 8.0 | 12.7 | 1.73 |
| experiment13: retrieval sweep, all strong models, top_k=3 | top_k_sweep | top_k | 3 | 5.251s | 30.570s | 3095.7 | 18412.9 | 3.0 | 6.0 | 0.80 |
| experiment14: retrieval sweep, all strong models, top_k=8 | top_k_sweep | top_k | 8 | 6.269s | 68.065s | 8179.7 | 47594.7 | 8.0 | 12.6 | 1.80 |
| experiment15: retrieval sweep, strong orchestrator only, top_k=3 | top_k_sweep | top_k | 3 | 4.992s | 31.586s | 3092.7 | 19584.9 | 3.0 | 5.5 | 0.67 |
| experiment16: retrieval sweep, strong orchestrator only, top_k=8 | top_k_sweep | top_k | 8 | 6.553s | 71.793s | 8192.9 | 50013.1 | 8.0 | 12.1 | 1.80 |
| experiment17: retrieval sweep, strong search agent only, top_k=3 | top_k_sweep | top_k | 3 | 4.776s | 29.083s | 3084.2 | 17693.7 | 3.0 | 5.4 | 1.07 |
| experiment18: retrieval sweep, strong search agent only, top_k=8 | top_k_sweep | top_k | 8 | 6.257s | 65.504s | 8176.2 | 46312.5 | 8.0 | 12.1 | 1.07 |
| experiment19: retrieval sweep, strong summarizer only, top_k=3 | top_k_sweep | top_k | 3 | 4.941s | 33.516s | 3092.1 | 20350.7 | 3.0 | 6.2 | 1.13 |
| experiment20: retrieval sweep, strong summarizer only, top_k=8 | top_k_sweep | top_k | 8 | 6.206s | 62.899s | 8179.9 | 44761.6 | 8.0 | 12.1 | 1.00 |
| experiment21: retrieval sweep, strong fact checker only, top_k=3 | top_k_sweep | top_k | 3 | 4.825s | 31.486s | 3084.7 | 19148.3 | 3.0 | 5.8 | 0.93 |
| experiment22: retrieval sweep, strong fact checker only, top_k=8 | top_k_sweep | top_k | 8 | 6.913s | 73.948s | 8183.1 | 49708.3 | 8.0 | 12.2 | 1.33 |
| experiment23: retrieval sweep, strong final synthesizer only, top_k=3 | top_k_sweep | top_k | 3 | 4.790s | 30.671s | 3078.9 | 18145.5 | 3.0 | 5.4 | 0.87 |
| experiment24: retrieval sweep, strong final synthesizer only, top_k=8 | top_k_sweep | top_k | 8 | 6.844s | 66.247s | 8216.7 | 45203.8 | 8.0 | 12.1 | 1.53 |

## Question Coverage

- experiment01: architecture control, all small models, top_k=5: citation grounding / uncertainty: 1, comparison: 2, definition: 2, easy lookup: 2, evidence synthesis: 1, evidence synthesis / ablation: 1, limitation/uncertainty: 1, method/mechanism: 2, method/mechanism / implementation: 1, multi-step reasoning: 1, multi-step reasoning / error analysis: 1
- experiment02: model ablation, strong orchestrator only, top_k=5: citation grounding / uncertainty: 1, comparison: 2, definition: 2, easy lookup: 2, evidence synthesis: 1, evidence synthesis / ablation: 1, limitation/uncertainty: 1, method/mechanism: 2, method/mechanism / implementation: 1, multi-step reasoning: 1, multi-step reasoning / error analysis: 1
- experiment03: model ablation, strong search agent only, top_k=5: citation grounding / uncertainty: 1, comparison: 2, definition: 2, easy lookup: 2, evidence synthesis: 1, evidence synthesis / ablation: 1, limitation/uncertainty: 1, method/mechanism: 2, method/mechanism / implementation: 1, multi-step reasoning: 1, multi-step reasoning / error analysis: 1
- experiment04: model ablation, strong summarizer only, top_k=5: citation grounding / uncertainty: 1, comparison: 2, definition: 2, easy lookup: 2, evidence synthesis: 1, evidence synthesis / ablation: 1, limitation/uncertainty: 1, method/mechanism: 2, method/mechanism / implementation: 1, multi-step reasoning: 1, multi-step reasoning / error analysis: 1
- experiment05: model ablation, strong fact checker only, top_k=5: citation grounding / uncertainty: 1, comparison: 2, definition: 2, easy lookup: 2, evidence synthesis: 1, evidence synthesis / ablation: 1, limitation/uncertainty: 1, method/mechanism: 2, method/mechanism / implementation: 1, multi-step reasoning: 1, multi-step reasoning / error analysis: 1
- experiment06: model ablation, strong final synthesizer only, top_k=5: citation grounding / uncertainty: 1, comparison: 2, definition: 2, easy lookup: 2, evidence synthesis: 1, evidence synthesis / ablation: 1, limitation/uncertainty: 1, method/mechanism: 2, method/mechanism / implementation: 1, multi-step reasoning: 1, multi-step reasoning / error analysis: 1
- experiment07: model interaction, strong checker and synthesizer, top_k=5: citation grounding / uncertainty: 1, comparison: 2, definition: 2, easy lookup: 2, evidence synthesis: 1, evidence synthesis / ablation: 1, limitation/uncertainty: 1, method/mechanism: 2, method/mechanism / implementation: 1, multi-step reasoning: 1, multi-step reasoning / error analysis: 1
- experiment08: upper bound, all strong models, top_k=5: citation grounding / uncertainty: 1, comparison: 2, definition: 2, easy lookup: 2, evidence synthesis: 1, evidence synthesis / ablation: 1, limitation/uncertainty: 1, method/mechanism: 2, method/mechanism / implementation: 1, multi-step reasoning: 1, multi-step reasoning / error analysis: 1
- experiment09: retrieval sweep, all small models, top_k=3: citation grounding / uncertainty: 1, comparison: 2, definition: 2, easy lookup: 2, evidence synthesis: 1, evidence synthesis / ablation: 1, limitation/uncertainty: 1, method/mechanism: 2, method/mechanism / implementation: 1, multi-step reasoning: 1, multi-step reasoning / error analysis: 1
- experiment10: retrieval sweep, all small models, top_k=8: citation grounding / uncertainty: 1, comparison: 2, definition: 2, easy lookup: 2, evidence synthesis: 1, evidence synthesis / ablation: 1, limitation/uncertainty: 1, method/mechanism: 2, method/mechanism / implementation: 1, multi-step reasoning: 1, multi-step reasoning / error analysis: 1
- experiment11: retrieval sweep, strong checker and synthesizer, top_k=3: citation grounding / uncertainty: 1, comparison: 2, definition: 2, easy lookup: 2, evidence synthesis: 1, evidence synthesis / ablation: 1, limitation/uncertainty: 1, method/mechanism: 2, method/mechanism / implementation: 1, multi-step reasoning: 1, multi-step reasoning / error analysis: 1
- experiment12: retrieval sweep, strong checker and synthesizer, top_k=8: citation grounding / uncertainty: 1, comparison: 2, definition: 2, easy lookup: 2, evidence synthesis: 1, evidence synthesis / ablation: 1, limitation/uncertainty: 1, method/mechanism: 2, method/mechanism / implementation: 1, multi-step reasoning: 1, multi-step reasoning / error analysis: 1
- experiment13: retrieval sweep, all strong models, top_k=3: citation grounding / uncertainty: 1, comparison: 2, definition: 2, easy lookup: 2, evidence synthesis: 1, evidence synthesis / ablation: 1, limitation/uncertainty: 1, method/mechanism: 2, method/mechanism / implementation: 1, multi-step reasoning: 1, multi-step reasoning / error analysis: 1
- experiment14: retrieval sweep, all strong models, top_k=8: citation grounding / uncertainty: 1, comparison: 2, definition: 2, easy lookup: 2, evidence synthesis: 1, evidence synthesis / ablation: 1, limitation/uncertainty: 1, method/mechanism: 2, method/mechanism / implementation: 1, multi-step reasoning: 1, multi-step reasoning / error analysis: 1
- experiment15: retrieval sweep, strong orchestrator only, top_k=3: citation grounding / uncertainty: 1, comparison: 2, definition: 2, easy lookup: 2, evidence synthesis: 1, evidence synthesis / ablation: 1, limitation/uncertainty: 1, method/mechanism: 2, method/mechanism / implementation: 1, multi-step reasoning: 1, multi-step reasoning / error analysis: 1
- experiment16: retrieval sweep, strong orchestrator only, top_k=8: citation grounding / uncertainty: 1, comparison: 2, definition: 2, easy lookup: 2, evidence synthesis: 1, evidence synthesis / ablation: 1, limitation/uncertainty: 1, method/mechanism: 2, method/mechanism / implementation: 1, multi-step reasoning: 1, multi-step reasoning / error analysis: 1
- experiment17: retrieval sweep, strong search agent only, top_k=3: citation grounding / uncertainty: 1, comparison: 2, definition: 2, easy lookup: 2, evidence synthesis: 1, evidence synthesis / ablation: 1, limitation/uncertainty: 1, method/mechanism: 2, method/mechanism / implementation: 1, multi-step reasoning: 1, multi-step reasoning / error analysis: 1
- experiment18: retrieval sweep, strong search agent only, top_k=8: citation grounding / uncertainty: 1, comparison: 2, definition: 2, easy lookup: 2, evidence synthesis: 1, evidence synthesis / ablation: 1, limitation/uncertainty: 1, method/mechanism: 2, method/mechanism / implementation: 1, multi-step reasoning: 1, multi-step reasoning / error analysis: 1
- experiment19: retrieval sweep, strong summarizer only, top_k=3: citation grounding / uncertainty: 1, comparison: 2, definition: 2, easy lookup: 2, evidence synthesis: 1, evidence synthesis / ablation: 1, limitation/uncertainty: 1, method/mechanism: 2, method/mechanism / implementation: 1, multi-step reasoning: 1, multi-step reasoning / error analysis: 1
- experiment20: retrieval sweep, strong summarizer only, top_k=8: citation grounding / uncertainty: 1, comparison: 2, definition: 2, easy lookup: 2, evidence synthesis: 1, evidence synthesis / ablation: 1, limitation/uncertainty: 1, method/mechanism: 2, method/mechanism / implementation: 1, multi-step reasoning: 1, multi-step reasoning / error analysis: 1
- experiment21: retrieval sweep, strong fact checker only, top_k=3: citation grounding / uncertainty: 1, comparison: 2, definition: 2, easy lookup: 2, evidence synthesis: 1, evidence synthesis / ablation: 1, limitation/uncertainty: 1, method/mechanism: 2, method/mechanism / implementation: 1, multi-step reasoning: 1, multi-step reasoning / error analysis: 1
- experiment22: retrieval sweep, strong fact checker only, top_k=8: citation grounding / uncertainty: 1, comparison: 2, definition: 2, easy lookup: 2, evidence synthesis: 1, evidence synthesis / ablation: 1, limitation/uncertainty: 1, method/mechanism: 2, method/mechanism / implementation: 1, multi-step reasoning: 1, multi-step reasoning / error analysis: 1
- experiment23: retrieval sweep, strong final synthesizer only, top_k=3: citation grounding / uncertainty: 1, comparison: 2, definition: 2, easy lookup: 2, evidence synthesis: 1, evidence synthesis / ablation: 1, limitation/uncertainty: 1, method/mechanism: 2, method/mechanism / implementation: 1, multi-step reasoning: 1, multi-step reasoning / error analysis: 1
- experiment24: retrieval sweep, strong final synthesizer only, top_k=8: citation grounding / uncertainty: 1, comparison: 2, definition: 2, easy lookup: 2, evidence synthesis: 1, evidence synthesis / ablation: 1, limitation/uncertainty: 1, method/mechanism: 2, method/mechanism / implementation: 1, multi-step reasoning: 1, multi-step reasoning / error analysis: 1

## Model Configurations

### experiment01: architecture control, all small models, top_k=5

- family: architecture_control
- control_variable: agent_architecture
- top_k: 5
- max_evidence_chunks: 5
- baseline_model: google/gemma-4-26B-A4B-it
- orchestrator_model: google/gemma-4-26B-A4B-it
- search_model: google/gemma-4-26B-A4B-it
- summarization_model: google/gemma-4-26B-A4B-it
- fact_check_model: google/gemma-4-26B-A4B-it
- final_synthesis_model: google/gemma-4-26B-A4B-it
- judge_model: gpt-4.1

### experiment02: model ablation, strong orchestrator only, top_k=5

- family: model_ablation
- control_variable: orchestrator_model
- top_k: 5
- max_evidence_chunks: 5
- baseline_model: google/gemma-4-26B-A4B-it
- orchestrator_model: google/gemma-4-26B-A4B-it
- search_model: google/gemma-4-26B-A4B-it
- summarization_model: google/gemma-4-26B-A4B-it
- fact_check_model: google/gemma-4-26B-A4B-it
- final_synthesis_model: google/gemma-4-26B-A4B-it
- judge_model: gpt-4.1

### experiment03: model ablation, strong search agent only, top_k=5

- family: model_ablation
- control_variable: search_model
- top_k: 5
- max_evidence_chunks: 5
- baseline_model: google/gemma-4-26B-A4B-it
- orchestrator_model: google/gemma-4-26B-A4B-it
- search_model: google/gemma-4-26B-A4B-it
- summarization_model: google/gemma-4-26B-A4B-it
- fact_check_model: google/gemma-4-26B-A4B-it
- final_synthesis_model: google/gemma-4-26B-A4B-it
- judge_model: gpt-4.1

### experiment04: model ablation, strong summarizer only, top_k=5

- family: model_ablation
- control_variable: summarization_model
- top_k: 5
- max_evidence_chunks: 5
- baseline_model: google/gemma-4-26B-A4B-it
- orchestrator_model: google/gemma-4-26B-A4B-it
- search_model: google/gemma-4-26B-A4B-it
- summarization_model: google/gemma-4-26B-A4B-it
- fact_check_model: google/gemma-4-26B-A4B-it
- final_synthesis_model: google/gemma-4-26B-A4B-it
- judge_model: gpt-4.1

### experiment05: model ablation, strong fact checker only, top_k=5

- family: model_ablation
- control_variable: fact_check_model
- top_k: 5
- max_evidence_chunks: 5
- baseline_model: google/gemma-4-26B-A4B-it
- orchestrator_model: google/gemma-4-26B-A4B-it
- search_model: google/gemma-4-26B-A4B-it
- summarization_model: google/gemma-4-26B-A4B-it
- fact_check_model: google/gemma-4-26B-A4B-it
- final_synthesis_model: google/gemma-4-26B-A4B-it
- judge_model: gpt-4.1

### experiment06: model ablation, strong final synthesizer only, top_k=5

- family: model_ablation
- control_variable: final_synthesis_model
- top_k: 5
- max_evidence_chunks: 5
- baseline_model: google/gemma-4-26B-A4B-it
- orchestrator_model: google/gemma-4-26B-A4B-it
- search_model: google/gemma-4-26B-A4B-it
- summarization_model: google/gemma-4-26B-A4B-it
- fact_check_model: google/gemma-4-26B-A4B-it
- final_synthesis_model: google/gemma-4-26B-A4B-it
- judge_model: gpt-4.1

### experiment07: model interaction, strong checker and synthesizer, top_k=5

- family: model_interaction
- control_variable: fact_check_and_final_synthesis_models
- top_k: 5
- max_evidence_chunks: 5
- baseline_model: google/gemma-4-26B-A4B-it
- orchestrator_model: google/gemma-4-26B-A4B-it
- search_model: google/gemma-4-26B-A4B-it
- summarization_model: google/gemma-4-26B-A4B-it
- fact_check_model: google/gemma-4-26B-A4B-it
- final_synthesis_model: google/gemma-4-26B-A4B-it
- judge_model: gpt-4.1

### experiment08: upper bound, all strong models, top_k=5

- family: model_upper_bound
- control_variable: all_agent_models
- top_k: 5
- max_evidence_chunks: 5
- baseline_model: google/gemma-4-26B-A4B-it
- orchestrator_model: google/gemma-4-26B-A4B-it
- search_model: google/gemma-4-26B-A4B-it
- summarization_model: google/gemma-4-26B-A4B-it
- fact_check_model: google/gemma-4-26B-A4B-it
- final_synthesis_model: google/gemma-4-26B-A4B-it
- judge_model: gpt-4.1

### experiment09: retrieval sweep, all small models, top_k=3

- family: top_k_sweep
- control_variable: top_k
- top_k: 3
- max_evidence_chunks: 3
- baseline_model: google/gemma-4-26B-A4B-it
- orchestrator_model: google/gemma-4-26B-A4B-it
- search_model: google/gemma-4-26B-A4B-it
- summarization_model: google/gemma-4-26B-A4B-it
- fact_check_model: google/gemma-4-26B-A4B-it
- final_synthesis_model: google/gemma-4-26B-A4B-it
- judge_model: gpt-4.1

### experiment10: retrieval sweep, all small models, top_k=8

- family: top_k_sweep
- control_variable: top_k
- top_k: 8
- max_evidence_chunks: 8
- baseline_model: google/gemma-4-26B-A4B-it
- orchestrator_model: google/gemma-4-26B-A4B-it
- search_model: google/gemma-4-26B-A4B-it
- summarization_model: google/gemma-4-26B-A4B-it
- fact_check_model: google/gemma-4-26B-A4B-it
- final_synthesis_model: google/gemma-4-26B-A4B-it
- judge_model: gpt-4.1

### experiment11: retrieval sweep, strong checker and synthesizer, top_k=3

- family: top_k_sweep
- control_variable: top_k
- top_k: 3
- max_evidence_chunks: 3
- baseline_model: google/gemma-4-26B-A4B-it
- orchestrator_model: google/gemma-4-26B-A4B-it
- search_model: google/gemma-4-26B-A4B-it
- summarization_model: google/gemma-4-26B-A4B-it
- fact_check_model: google/gemma-4-26B-A4B-it
- final_synthesis_model: google/gemma-4-26B-A4B-it
- judge_model: gpt-4.1

### experiment12: retrieval sweep, strong checker and synthesizer, top_k=8

- family: top_k_sweep
- control_variable: top_k
- top_k: 8
- max_evidence_chunks: 8
- baseline_model: google/gemma-4-26B-A4B-it
- orchestrator_model: google/gemma-4-26B-A4B-it
- search_model: google/gemma-4-26B-A4B-it
- summarization_model: google/gemma-4-26B-A4B-it
- fact_check_model: google/gemma-4-26B-A4B-it
- final_synthesis_model: google/gemma-4-26B-A4B-it
- judge_model: gpt-4.1

### experiment13: retrieval sweep, all strong models, top_k=3

- family: top_k_sweep
- control_variable: top_k
- top_k: 3
- max_evidence_chunks: 3
- baseline_model: google/gemma-4-26B-A4B-it
- orchestrator_model: google/gemma-4-26B-A4B-it
- search_model: google/gemma-4-26B-A4B-it
- summarization_model: google/gemma-4-26B-A4B-it
- fact_check_model: google/gemma-4-26B-A4B-it
- final_synthesis_model: google/gemma-4-26B-A4B-it
- judge_model: gpt-4.1

### experiment14: retrieval sweep, all strong models, top_k=8

- family: top_k_sweep
- control_variable: top_k
- top_k: 8
- max_evidence_chunks: 8
- baseline_model: google/gemma-4-26B-A4B-it
- orchestrator_model: google/gemma-4-26B-A4B-it
- search_model: google/gemma-4-26B-A4B-it
- summarization_model: google/gemma-4-26B-A4B-it
- fact_check_model: google/gemma-4-26B-A4B-it
- final_synthesis_model: google/gemma-4-26B-A4B-it
- judge_model: gpt-4.1

### experiment15: retrieval sweep, strong orchestrator only, top_k=3

- family: top_k_sweep
- control_variable: top_k
- top_k: 3
- max_evidence_chunks: 3
- baseline_model: google/gemma-4-26B-A4B-it
- orchestrator_model: google/gemma-4-26B-A4B-it
- search_model: google/gemma-4-26B-A4B-it
- summarization_model: google/gemma-4-26B-A4B-it
- fact_check_model: google/gemma-4-26B-A4B-it
- final_synthesis_model: google/gemma-4-26B-A4B-it
- judge_model: gpt-4.1

### experiment16: retrieval sweep, strong orchestrator only, top_k=8

- family: top_k_sweep
- control_variable: top_k
- top_k: 8
- max_evidence_chunks: 8
- baseline_model: google/gemma-4-26B-A4B-it
- orchestrator_model: google/gemma-4-26B-A4B-it
- search_model: google/gemma-4-26B-A4B-it
- summarization_model: google/gemma-4-26B-A4B-it
- fact_check_model: google/gemma-4-26B-A4B-it
- final_synthesis_model: google/gemma-4-26B-A4B-it
- judge_model: gpt-4.1

### experiment17: retrieval sweep, strong search agent only, top_k=3

- family: top_k_sweep
- control_variable: top_k
- top_k: 3
- max_evidence_chunks: 3
- baseline_model: google/gemma-4-26B-A4B-it
- orchestrator_model: google/gemma-4-26B-A4B-it
- search_model: google/gemma-4-26B-A4B-it
- summarization_model: google/gemma-4-26B-A4B-it
- fact_check_model: google/gemma-4-26B-A4B-it
- final_synthesis_model: google/gemma-4-26B-A4B-it
- judge_model: gpt-4.1

### experiment18: retrieval sweep, strong search agent only, top_k=8

- family: top_k_sweep
- control_variable: top_k
- top_k: 8
- max_evidence_chunks: 8
- baseline_model: google/gemma-4-26B-A4B-it
- orchestrator_model: google/gemma-4-26B-A4B-it
- search_model: google/gemma-4-26B-A4B-it
- summarization_model: google/gemma-4-26B-A4B-it
- fact_check_model: google/gemma-4-26B-A4B-it
- final_synthesis_model: google/gemma-4-26B-A4B-it
- judge_model: gpt-4.1

### experiment19: retrieval sweep, strong summarizer only, top_k=3

- family: top_k_sweep
- control_variable: top_k
- top_k: 3
- max_evidence_chunks: 3
- baseline_model: google/gemma-4-26B-A4B-it
- orchestrator_model: google/gemma-4-26B-A4B-it
- search_model: google/gemma-4-26B-A4B-it
- summarization_model: google/gemma-4-26B-A4B-it
- fact_check_model: google/gemma-4-26B-A4B-it
- final_synthesis_model: google/gemma-4-26B-A4B-it
- judge_model: gpt-4.1

### experiment20: retrieval sweep, strong summarizer only, top_k=8

- family: top_k_sweep
- control_variable: top_k
- top_k: 8
- max_evidence_chunks: 8
- baseline_model: google/gemma-4-26B-A4B-it
- orchestrator_model: google/gemma-4-26B-A4B-it
- search_model: google/gemma-4-26B-A4B-it
- summarization_model: google/gemma-4-26B-A4B-it
- fact_check_model: google/gemma-4-26B-A4B-it
- final_synthesis_model: google/gemma-4-26B-A4B-it
- judge_model: gpt-4.1

### experiment21: retrieval sweep, strong fact checker only, top_k=3

- family: top_k_sweep
- control_variable: top_k
- top_k: 3
- max_evidence_chunks: 3
- baseline_model: google/gemma-4-26B-A4B-it
- orchestrator_model: google/gemma-4-26B-A4B-it
- search_model: google/gemma-4-26B-A4B-it
- summarization_model: google/gemma-4-26B-A4B-it
- fact_check_model: google/gemma-4-26B-A4B-it
- final_synthesis_model: google/gemma-4-26B-A4B-it
- judge_model: gpt-4.1

### experiment22: retrieval sweep, strong fact checker only, top_k=8

- family: top_k_sweep
- control_variable: top_k
- top_k: 8
- max_evidence_chunks: 8
- baseline_model: google/gemma-4-26B-A4B-it
- orchestrator_model: google/gemma-4-26B-A4B-it
- search_model: google/gemma-4-26B-A4B-it
- summarization_model: google/gemma-4-26B-A4B-it
- fact_check_model: google/gemma-4-26B-A4B-it
- final_synthesis_model: google/gemma-4-26B-A4B-it
- judge_model: gpt-4.1

### experiment23: retrieval sweep, strong final synthesizer only, top_k=3

- family: top_k_sweep
- control_variable: top_k
- top_k: 3
- max_evidence_chunks: 3
- baseline_model: google/gemma-4-26B-A4B-it
- orchestrator_model: google/gemma-4-26B-A4B-it
- search_model: google/gemma-4-26B-A4B-it
- summarization_model: google/gemma-4-26B-A4B-it
- fact_check_model: google/gemma-4-26B-A4B-it
- final_synthesis_model: google/gemma-4-26B-A4B-it
- judge_model: gpt-4.1

### experiment24: retrieval sweep, strong final synthesizer only, top_k=8

- family: top_k_sweep
- control_variable: top_k
- top_k: 8
- max_evidence_chunks: 8
- baseline_model: google/gemma-4-26B-A4B-it
- orchestrator_model: google/gemma-4-26B-A4B-it
- search_model: google/gemma-4-26B-A4B-it
- summarization_model: google/gemma-4-26B-A4B-it
- fact_check_model: google/gemma-4-26B-A4B-it
- final_synthesis_model: google/gemma-4-26B-A4B-it
- judge_model: gpt-4.1


## External Judge Averages

| Experiment | System | Factual Accuracy | Completeness | Citation Quality | Clarity | Unsupported Claims |
|---|---|---:|---:|---:|---:|---:|
| experiment01: architecture control, all small models, top_k=5 | baseline | 6.67 | 7.13 | 6.80 | 8.80 | 0.93 |
| experiment01: architecture control, all small models, top_k=5 | multi_agent | 6.60 | 7.07 | 6.73 | 8.60 | 0.67 |
| experiment02: model ablation, strong orchestrator only, top_k=5 | baseline | 6.93 | 7.07 | 7.40 | 8.67 | 0.60 |
| experiment02: model ablation, strong orchestrator only, top_k=5 | multi_agent | 6.73 | 7.27 | 7.00 | 8.60 | 0.53 |
| experiment03: model ablation, strong search agent only, top_k=5 | baseline | 7.20 | 7.53 | 7.07 | 8.87 | 1.13 |
| experiment03: model ablation, strong search agent only, top_k=5 | multi_agent | 6.80 | 7.07 | 6.67 | 8.53 | 0.80 |
| experiment04: model ablation, strong summarizer only, top_k=5 | baseline | 7.00 | 7.40 | 6.73 | 8.53 | 1.47 |
| experiment04: model ablation, strong summarizer only, top_k=5 | multi_agent | 6.47 | 6.93 | 6.40 | 8.20 | 0.80 |
| experiment05: model ablation, strong fact checker only, top_k=5 | baseline | 6.67 | 7.33 | 6.93 | 8.87 | 1.00 |
| experiment05: model ablation, strong fact checker only, top_k=5 | multi_agent | 6.60 | 6.80 | 6.47 | 8.67 | 1.40 |
| experiment06: model ablation, strong final synthesizer only, top_k=5 | baseline | 6.73 | 7.07 | 6.73 | 8.67 | 1.20 |
| experiment06: model ablation, strong final synthesizer only, top_k=5 | multi_agent | 6.80 | 6.93 | 6.73 | 8.67 | 0.73 |
| experiment07: model interaction, strong checker and synthesizer, top_k=5 | baseline | 6.33 | 6.60 | 6.60 | 8.27 | 0.60 |
| experiment07: model interaction, strong checker and synthesizer, top_k=5 | multi_agent | 6.87 | 7.00 | 7.20 | 8.60 | 0.87 |
| experiment08: upper bound, all strong models, top_k=5 | baseline | 7.00 | 7.33 | 6.80 | 8.67 | 1.20 |
| experiment08: upper bound, all strong models, top_k=5 | multi_agent | 6.47 | 6.60 | 6.60 | 8.13 | 1.20 |
| experiment09: retrieval sweep, all small models, top_k=3 | baseline | 6.40 | 6.53 | 6.53 | 8.13 | 0.27 |
| experiment09: retrieval sweep, all small models, top_k=3 | multi_agent | 6.27 | 6.53 | 6.80 | 8.60 | 0.53 |
| experiment10: retrieval sweep, all small models, top_k=8 | baseline | 7.07 | 7.93 | 7.07 | 8.73 | 1.13 |
| experiment10: retrieval sweep, all small models, top_k=8 | multi_agent | 6.87 | 7.27 | 7.00 | 8.53 | 0.60 |
| experiment11: retrieval sweep, strong checker and synthesizer, top_k=3 | baseline | 7.07 | 7.20 | 7.53 | 8.80 | 0.47 |
| experiment11: retrieval sweep, strong checker and synthesizer, top_k=3 | multi_agent | 6.53 | 6.40 | 6.40 | 8.27 | 0.67 |
| experiment12: retrieval sweep, strong checker and synthesizer, top_k=8 | baseline | 7.40 | 7.80 | 7.20 | 8.93 | 0.87 |
| experiment12: retrieval sweep, strong checker and synthesizer, top_k=8 | multi_agent | 7.00 | 7.53 | 6.87 | 8.60 | 0.60 |
| experiment13: retrieval sweep, all strong models, top_k=3 | baseline | 6.87 | 7.07 | 6.80 | 8.80 | 0.40 |
| experiment13: retrieval sweep, all strong models, top_k=3 | multi_agent | 6.93 | 7.13 | 6.73 | 8.80 | 0.33 |
| experiment14: retrieval sweep, all strong models, top_k=8 | baseline | 7.20 | 7.73 | 7.07 | 8.93 | 1.33 |
| experiment14: retrieval sweep, all strong models, top_k=8 | multi_agent | 6.73 | 7.07 | 6.93 | 8.87 | 0.47 |
| experiment15: retrieval sweep, strong orchestrator only, top_k=3 | baseline | 6.93 | 7.07 | 7.13 | 8.93 | 0.40 |
| experiment15: retrieval sweep, strong orchestrator only, top_k=3 | multi_agent | 6.53 | 6.40 | 6.47 | 8.47 | 0.80 |
| experiment16: retrieval sweep, strong orchestrator only, top_k=8 | baseline | 6.87 | 7.00 | 6.73 | 8.33 | 0.60 |
| experiment16: retrieval sweep, strong orchestrator only, top_k=8 | multi_agent | 6.60 | 6.93 | 6.87 | 8.40 | 1.13 |
| experiment17: retrieval sweep, strong search agent only, top_k=3 | baseline | 6.93 | 7.20 | 7.27 | 8.80 | 0.73 |
| experiment17: retrieval sweep, strong search agent only, top_k=3 | multi_agent | 6.53 | 6.60 | 6.53 | 8.53 | 0.47 |
| experiment18: retrieval sweep, strong search agent only, top_k=8 | baseline | 7.53 | 8.00 | 7.40 | 9.00 | 0.87 |
| experiment18: retrieval sweep, strong search agent only, top_k=8 | multi_agent | 6.87 | 7.33 | 7.13 | 8.60 | 0.67 |
| experiment19: retrieval sweep, strong summarizer only, top_k=3 | baseline | 7.00 | 7.33 | 7.27 | 8.73 | 0.67 |
| experiment19: retrieval sweep, strong summarizer only, top_k=3 | multi_agent | 6.80 | 6.80 | 6.87 | 8.40 | 0.80 |
| experiment20: retrieval sweep, strong summarizer only, top_k=8 | baseline | 7.47 | 7.93 | 7.53 | 8.87 | 0.73 |
| experiment20: retrieval sweep, strong summarizer only, top_k=8 | multi_agent | 6.60 | 7.07 | 6.73 | 8.53 | 0.87 |
| experiment21: retrieval sweep, strong fact checker only, top_k=3 | baseline | 7.13 | 7.20 | 7.27 | 8.93 | 0.53 |
| experiment21: retrieval sweep, strong fact checker only, top_k=3 | multi_agent | 6.40 | 6.20 | 6.27 | 8.33 | 1.40 |
| experiment22: retrieval sweep, strong fact checker only, top_k=8 | baseline | 7.20 | 7.60 | 7.27 | 8.93 | 0.60 |
| experiment22: retrieval sweep, strong fact checker only, top_k=8 | multi_agent | 6.93 | 7.00 | 6.87 | 8.67 | 1.13 |
| experiment23: retrieval sweep, strong final synthesizer only, top_k=3 | baseline | 6.93 | 6.80 | 6.93 | 8.80 | 0.33 |
| experiment23: retrieval sweep, strong final synthesizer only, top_k=3 | multi_agent | 6.67 | 6.47 | 6.47 | 8.20 | 0.80 |
| experiment24: retrieval sweep, strong final synthesizer only, top_k=8 | baseline | 7.20 | 7.67 | 7.07 | 8.93 | 1.20 |
| experiment24: retrieval sweep, strong final synthesizer only, top_k=8 | multi_agent | 6.87 | 7.20 | 7.00 | 8.73 | 0.87 |