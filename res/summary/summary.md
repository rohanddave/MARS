# Cross-Experiment Summary

This summary is generated from the persisted `metrics.json` files in each experiment folder.

| Experiment | Family | Control Variable | top_k | Avg Baseline Latency | Avg Multi-Agent Latency | Avg Baseline Tokens | Avg Multi-Agent Tokens | Avg Baseline Citations | Avg Multi-Agent Evidence | Unsupported Claims/Q |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| experiment01: architecture control, all small models, top_k=5 | architecture_control | agent_architecture | 5 | 4.256s | 40.132s | 2143.2 | 12736.1 | 5.0 | 16.3 | 0.80 |
| experiment02: model ablation, strong orchestrator only, top_k=5 | model_ablation | orchestrator_model | 5 | 4.897s | 47.352s | 2140.2 | 15493.5 | 5.0 | 17.3 | 1.60 |
| experiment03: model ablation, strong search agent only, top_k=5 | model_ablation | search_model | 5 | 3.925s | 43.317s | 2140.3 | 12799.7 | 5.0 | 20.1 | 1.27 |
| experiment04: model ablation, strong summarizer only, top_k=5 | model_ablation | summarization_model | 5 | 3.484s | 45.523s | 2110.9 | 15329.0 | 5.0 | 18.9 | 1.40 |
| experiment05: model ablation, strong fact checker only, top_k=5 | model_ablation | fact_check_model | 5 | 4.305s | 40.493s | 2137.8 | 13906.2 | 5.0 | 16.5 | 0.73 |
| experiment06: model ablation, strong final synthesizer only, top_k=5 | model_ablation | final_synthesis_model | 5 | 3.623s | 32.404s | 2114.1 | 11080.1 | 5.0 | 14.1 | 0.27 |
| experiment07: model interaction, strong checker and synthesizer, top_k=5 | model_interaction | fact_check_and_final_synthesis_models | 5 | 2.043s | 17.977s | 205.0 | 2990.0 | 0.0 | 0.0 | 2.00 |
| experiment08: upper bound, all strong models, top_k=5 | model_upper_bound | all_agent_models | 5 | 2.412s | 16.368s | 198.4 | 2942.1 | 0.0 | 0.0 | 1.87 |
| experiment09: retrieval sweep, all small models, top_k=3 | top_k_sweep | top_k | 3 | 1.928s | 15.013s | 205.9 | 2752.3 | 0.0 | 0.0 | 2.20 |
| experiment10: retrieval sweep, all small models, top_k=8 | top_k_sweep | top_k | 8 | 1.881s | 14.166s | 203.6 | 2752.3 | 0.0 | 0.0 | 2.13 |
| experiment11: retrieval sweep, strong checker and synthesizer, top_k=3 | top_k_sweep | top_k | 3 | 1.836s | 16.102s | 205.6 | 2979.2 | 0.0 | 0.0 | 1.87 |
| experiment12: retrieval sweep, strong checker and synthesizer, top_k=8 | top_k_sweep | top_k | 8 | 2.442s | 15.444s | 208.1 | 2924.6 | 0.0 | 0.0 | 1.80 |
| experiment13: retrieval sweep, all strong models, top_k=3 | top_k_sweep | top_k | 3 | 1.840s | 15.399s | 199.1 | 2944.1 | 0.0 | 0.0 | 2.00 |
| experiment14: retrieval sweep, all strong models, top_k=8 | top_k_sweep | top_k | 8 | 1.868s | 16.893s | 200.5 | 3004.7 | 0.0 | 0.0 | 1.87 |
| experiment15: retrieval sweep, strong orchestrator only, top_k=3 | top_k_sweep | top_k | 3 | 2.261s | 15.031s | 206.1 | 2908.9 | 0.0 | 0.0 | 2.40 |
| experiment16: retrieval sweep, strong orchestrator only, top_k=8 | top_k_sweep | top_k | 8 | 1.696s | 14.867s | 204.1 | 2789.1 | 0.0 | 0.0 | 2.27 |
| experiment17: retrieval sweep, strong search agent only, top_k=3 | top_k_sweep | top_k | 3 | 1.720s | 16.021s | 204.9 | 2835.5 | 0.0 | 0.0 | 2.33 |
| experiment18: retrieval sweep, strong search agent only, top_k=8 | top_k_sweep | top_k | 8 | 2.207s | 16.354s | 206.5 | 2770.5 | 0.0 | 0.0 | 2.13 |
| experiment19: retrieval sweep, strong summarizer only, top_k=3 | top_k_sweep | top_k | 3 | 1.845s | 15.281s | 202.9 | 2742.3 | 0.0 | 0.0 | 2.00 |
| experiment20: retrieval sweep, strong summarizer only, top_k=8 | top_k_sweep | top_k | 8 | 2.059s | 15.486s | 203.3 | 2756.7 | 0.0 | 0.0 | 2.33 |
| experiment21: retrieval sweep, strong fact checker only, top_k=3 | top_k_sweep | top_k | 3 | 1.741s | 16.516s | 207.3 | 3025.3 | 0.0 | 0.0 | 2.13 |
| experiment22: retrieval sweep, strong fact checker only, top_k=8 | top_k_sweep | top_k | 8 | 1.935s | 14.975s | 203.1 | 3011.1 | 0.0 | 0.0 | 2.00 |
| experiment23: retrieval sweep, strong final synthesizer only, top_k=3 | top_k_sweep | top_k | 3 | 2.069s | 13.917s | 205.2 | 2713.5 | 0.0 | 0.0 | 2.07 |
| experiment24: retrieval sweep, strong final synthesizer only, top_k=8 | top_k_sweep | top_k | 8 | 1.953s | 15.365s | 206.3 | 2703.5 | 0.0 | 0.0 | 2.07 |

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
- baseline_model: gpt-4.1-mini
- orchestrator_model: gpt-4.1-mini
- search_model: gpt-4.1-mini
- summarization_model: gpt-4.1-mini
- fact_check_model: gpt-4.1-mini
- final_synthesis_model: gpt-4.1-mini
- judge_model: gpt-5.1

### experiment02: model ablation, strong orchestrator only, top_k=5

- family: model_ablation
- control_variable: orchestrator_model
- top_k: 5
- max_evidence_chunks: 5
- baseline_model: gpt-4.1-mini
- orchestrator_model: gpt-4.1
- search_model: gpt-4.1-mini
- summarization_model: gpt-4.1-mini
- fact_check_model: gpt-4.1-mini
- final_synthesis_model: gpt-4.1-mini
- judge_model: gpt-5.1

### experiment03: model ablation, strong search agent only, top_k=5

- family: model_ablation
- control_variable: search_model
- top_k: 5
- max_evidence_chunks: 5
- baseline_model: gpt-4.1-mini
- orchestrator_model: gpt-4.1-mini
- search_model: gpt-4.1
- summarization_model: gpt-4.1-mini
- fact_check_model: gpt-4.1-mini
- final_synthesis_model: gpt-4.1-mini
- judge_model: gpt-5.1

### experiment04: model ablation, strong summarizer only, top_k=5

- family: model_ablation
- control_variable: summarization_model
- top_k: 5
- max_evidence_chunks: 5
- baseline_model: gpt-4.1-mini
- orchestrator_model: gpt-4.1-mini
- search_model: gpt-4.1-mini
- summarization_model: gpt-4.1
- fact_check_model: gpt-4.1-mini
- final_synthesis_model: gpt-4.1-mini
- judge_model: gpt-5.1

### experiment05: model ablation, strong fact checker only, top_k=5

- family: model_ablation
- control_variable: fact_check_model
- top_k: 5
- max_evidence_chunks: 5
- baseline_model: gpt-4.1-mini
- orchestrator_model: gpt-4.1-mini
- search_model: gpt-4.1-mini
- summarization_model: gpt-4.1-mini
- fact_check_model: gpt-4.1
- final_synthesis_model: gpt-4.1-mini
- judge_model: gpt-5.1

### experiment06: model ablation, strong final synthesizer only, top_k=5

- family: model_ablation
- control_variable: final_synthesis_model
- top_k: 5
- max_evidence_chunks: 5
- baseline_model: gpt-4.1-mini
- orchestrator_model: gpt-4.1-mini
- search_model: gpt-4.1-mini
- summarization_model: gpt-4.1-mini
- fact_check_model: gpt-4.1-mini
- final_synthesis_model: gpt-4.1
- judge_model: gpt-5.1

### experiment07: model interaction, strong checker and synthesizer, top_k=5

- family: model_interaction
- control_variable: fact_check_and_final_synthesis_models
- top_k: 5
- max_evidence_chunks: 5
- baseline_model: gpt-4.1-mini
- orchestrator_model: gpt-4.1-mini
- search_model: gpt-4.1-mini
- summarization_model: gpt-4.1-mini
- fact_check_model: gpt-4.1
- final_synthesis_model: gpt-4.1
- judge_model: gpt-5.1

### experiment08: upper bound, all strong models, top_k=5

- family: model_upper_bound
- control_variable: all_agent_models
- top_k: 5
- max_evidence_chunks: 5
- baseline_model: gpt-4.1
- orchestrator_model: gpt-4.1
- search_model: gpt-4.1
- summarization_model: gpt-4.1
- fact_check_model: gpt-4.1
- final_synthesis_model: gpt-4.1
- judge_model: gpt-5.1

### experiment09: retrieval sweep, all small models, top_k=3

- family: top_k_sweep
- control_variable: top_k
- top_k: 3
- max_evidence_chunks: 3
- baseline_model: gpt-4.1-mini
- orchestrator_model: gpt-4.1-mini
- search_model: gpt-4.1-mini
- summarization_model: gpt-4.1-mini
- fact_check_model: gpt-4.1-mini
- final_synthesis_model: gpt-4.1-mini
- judge_model: gpt-5.1

### experiment10: retrieval sweep, all small models, top_k=8

- family: top_k_sweep
- control_variable: top_k
- top_k: 8
- max_evidence_chunks: 8
- baseline_model: gpt-4.1-mini
- orchestrator_model: gpt-4.1-mini
- search_model: gpt-4.1-mini
- summarization_model: gpt-4.1-mini
- fact_check_model: gpt-4.1-mini
- final_synthesis_model: gpt-4.1-mini
- judge_model: gpt-5.1

### experiment11: retrieval sweep, strong checker and synthesizer, top_k=3

- family: top_k_sweep
- control_variable: top_k
- top_k: 3
- max_evidence_chunks: 3
- baseline_model: gpt-4.1-mini
- orchestrator_model: gpt-4.1-mini
- search_model: gpt-4.1-mini
- summarization_model: gpt-4.1-mini
- fact_check_model: gpt-4.1
- final_synthesis_model: gpt-4.1
- judge_model: gpt-5.1

### experiment12: retrieval sweep, strong checker and synthesizer, top_k=8

- family: top_k_sweep
- control_variable: top_k
- top_k: 8
- max_evidence_chunks: 8
- baseline_model: gpt-4.1-mini
- orchestrator_model: gpt-4.1-mini
- search_model: gpt-4.1-mini
- summarization_model: gpt-4.1-mini
- fact_check_model: gpt-4.1
- final_synthesis_model: gpt-4.1
- judge_model: gpt-5.1

### experiment13: retrieval sweep, all strong models, top_k=3

- family: top_k_sweep
- control_variable: top_k
- top_k: 3
- max_evidence_chunks: 3
- baseline_model: gpt-4.1
- orchestrator_model: gpt-4.1
- search_model: gpt-4.1
- summarization_model: gpt-4.1
- fact_check_model: gpt-4.1
- final_synthesis_model: gpt-4.1
- judge_model: gpt-5.1

### experiment14: retrieval sweep, all strong models, top_k=8

- family: top_k_sweep
- control_variable: top_k
- top_k: 8
- max_evidence_chunks: 8
- baseline_model: gpt-4.1
- orchestrator_model: gpt-4.1
- search_model: gpt-4.1
- summarization_model: gpt-4.1
- fact_check_model: gpt-4.1
- final_synthesis_model: gpt-4.1
- judge_model: gpt-5.1

### experiment15: retrieval sweep, strong orchestrator only, top_k=3

- family: top_k_sweep
- control_variable: top_k
- top_k: 3
- max_evidence_chunks: 3
- baseline_model: gpt-4.1-mini
- orchestrator_model: gpt-4.1
- search_model: gpt-4.1-mini
- summarization_model: gpt-4.1-mini
- fact_check_model: gpt-4.1-mini
- final_synthesis_model: gpt-4.1-mini
- judge_model: gpt-5.1

### experiment16: retrieval sweep, strong orchestrator only, top_k=8

- family: top_k_sweep
- control_variable: top_k
- top_k: 8
- max_evidence_chunks: 8
- baseline_model: gpt-4.1-mini
- orchestrator_model: gpt-4.1
- search_model: gpt-4.1-mini
- summarization_model: gpt-4.1-mini
- fact_check_model: gpt-4.1-mini
- final_synthesis_model: gpt-4.1-mini
- judge_model: gpt-5.1

### experiment17: retrieval sweep, strong search agent only, top_k=3

- family: top_k_sweep
- control_variable: top_k
- top_k: 3
- max_evidence_chunks: 3
- baseline_model: gpt-4.1-mini
- orchestrator_model: gpt-4.1-mini
- search_model: gpt-4.1
- summarization_model: gpt-4.1-mini
- fact_check_model: gpt-4.1-mini
- final_synthesis_model: gpt-4.1-mini
- judge_model: gpt-5.1

### experiment18: retrieval sweep, strong search agent only, top_k=8

- family: top_k_sweep
- control_variable: top_k
- top_k: 8
- max_evidence_chunks: 8
- baseline_model: gpt-4.1-mini
- orchestrator_model: gpt-4.1-mini
- search_model: gpt-4.1
- summarization_model: gpt-4.1-mini
- fact_check_model: gpt-4.1-mini
- final_synthesis_model: gpt-4.1-mini
- judge_model: gpt-5.1

### experiment19: retrieval sweep, strong summarizer only, top_k=3

- family: top_k_sweep
- control_variable: top_k
- top_k: 3
- max_evidence_chunks: 3
- baseline_model: gpt-4.1-mini
- orchestrator_model: gpt-4.1-mini
- search_model: gpt-4.1-mini
- summarization_model: gpt-4.1
- fact_check_model: gpt-4.1-mini
- final_synthesis_model: gpt-4.1-mini
- judge_model: gpt-5.1

### experiment20: retrieval sweep, strong summarizer only, top_k=8

- family: top_k_sweep
- control_variable: top_k
- top_k: 8
- max_evidence_chunks: 8
- baseline_model: gpt-4.1-mini
- orchestrator_model: gpt-4.1-mini
- search_model: gpt-4.1-mini
- summarization_model: gpt-4.1
- fact_check_model: gpt-4.1-mini
- final_synthesis_model: gpt-4.1-mini
- judge_model: gpt-5.1

### experiment21: retrieval sweep, strong fact checker only, top_k=3

- family: top_k_sweep
- control_variable: top_k
- top_k: 3
- max_evidence_chunks: 3
- baseline_model: gpt-4.1-mini
- orchestrator_model: gpt-4.1-mini
- search_model: gpt-4.1-mini
- summarization_model: gpt-4.1-mini
- fact_check_model: gpt-4.1
- final_synthesis_model: gpt-4.1-mini
- judge_model: gpt-5.1

### experiment22: retrieval sweep, strong fact checker only, top_k=8

- family: top_k_sweep
- control_variable: top_k
- top_k: 8
- max_evidence_chunks: 8
- baseline_model: gpt-4.1-mini
- orchestrator_model: gpt-4.1-mini
- search_model: gpt-4.1-mini
- summarization_model: gpt-4.1-mini
- fact_check_model: gpt-4.1
- final_synthesis_model: gpt-4.1-mini
- judge_model: gpt-5.1

### experiment23: retrieval sweep, strong final synthesizer only, top_k=3

- family: top_k_sweep
- control_variable: top_k
- top_k: 3
- max_evidence_chunks: 3
- baseline_model: gpt-4.1-mini
- orchestrator_model: gpt-4.1-mini
- search_model: gpt-4.1-mini
- summarization_model: gpt-4.1-mini
- fact_check_model: gpt-4.1-mini
- final_synthesis_model: gpt-4.1
- judge_model: gpt-5.1

### experiment24: retrieval sweep, strong final synthesizer only, top_k=8

- family: top_k_sweep
- control_variable: top_k
- top_k: 8
- max_evidence_chunks: 8
- baseline_model: gpt-4.1-mini
- orchestrator_model: gpt-4.1-mini
- search_model: gpt-4.1-mini
- summarization_model: gpt-4.1-mini
- fact_check_model: gpt-4.1-mini
- final_synthesis_model: gpt-4.1
- judge_model: gpt-5.1


## External Judge Averages

| Experiment | System | Factual Accuracy | Completeness | Citation Quality | Clarity | Unsupported Claims |
|---|---|---:|---:|---:|---:|---:|
| experiment01: architecture control, all small models, top_k=5 | baseline | 3.93 | 3.67 | 3.33 | 4.53 | 1.27 |
| experiment01: architecture control, all small models, top_k=5 | multi_agent | 3.67 | 3.20 | 3.33 | 4.40 | 1.27 |
| experiment02: model ablation, strong orchestrator only, top_k=5 | baseline | 4.27 | 3.73 | 3.40 | 4.67 | 1.13 |
| experiment02: model ablation, strong orchestrator only, top_k=5 | multi_agent | 3.87 | 3.33 | 3.67 | 4.60 | 1.33 |
| experiment03: model ablation, strong search agent only, top_k=5 | baseline | 4.07 | 3.53 | 3.07 | 4.73 | 1.27 |
| experiment03: model ablation, strong search agent only, top_k=5 | multi_agent | 4.13 | 3.13 | 3.47 | 4.60 | 0.93 |
| experiment04: model ablation, strong summarizer only, top_k=5 | baseline | 4.20 | 3.67 | 3.20 | 4.53 | 1.07 |
| experiment04: model ablation, strong summarizer only, top_k=5 | multi_agent | 4.20 | 3.00 | 3.67 | 4.53 | 1.00 |
| experiment05: model ablation, strong fact checker only, top_k=5 | baseline | 4.13 | 3.60 | 3.33 | 4.73 | 1.33 |
| experiment05: model ablation, strong fact checker only, top_k=5 | multi_agent | 3.87 | 3.13 | 3.20 | 4.33 | 0.93 |
| experiment06: model ablation, strong final synthesizer only, top_k=5 | baseline | 4.13 | 3.80 | 3.27 | 4.60 | 1.27 |
| experiment06: model ablation, strong final synthesizer only, top_k=5 | multi_agent | 4.00 | 3.07 | 3.47 | 4.47 | 1.20 |
| experiment07: model interaction, strong checker and synthesizer, top_k=5 | baseline | 5.00 | 3.53 | 3.80 | 4.93 | 0.00 |
| experiment07: model interaction, strong checker and synthesizer, top_k=5 | multi_agent | 5.00 | 4.00 | 2.60 | 5.00 | 0.00 |
| experiment08: upper bound, all strong models, top_k=5 | baseline | 5.00 | 3.67 | 3.80 | 5.00 | 0.00 |
| experiment08: upper bound, all strong models, top_k=5 | multi_agent | 4.93 | 4.47 | 2.47 | 5.00 | 0.00 |
| experiment09: retrieval sweep, all small models, top_k=3 | baseline | 5.00 | 3.33 | 3.40 | 5.00 | 0.00 |
| experiment09: retrieval sweep, all small models, top_k=3 | multi_agent | 4.80 | 3.93 | 2.07 | 4.87 | 0.13 |
| experiment10: retrieval sweep, all small models, top_k=8 | baseline | 5.00 | 3.60 | 3.40 | 4.93 | 0.00 |
| experiment10: retrieval sweep, all small models, top_k=8 | multi_agent | 5.00 | 3.27 | 2.33 | 5.00 | 0.00 |
| experiment11: retrieval sweep, strong checker and synthesizer, top_k=3 | baseline | 4.80 | 4.20 | 3.93 | 4.93 | 0.07 |
| experiment11: retrieval sweep, strong checker and synthesizer, top_k=3 | multi_agent | 5.00 | 4.27 | 2.47 | 4.93 | 0.07 |
| experiment12: retrieval sweep, strong checker and synthesizer, top_k=8 | baseline | 5.00 | 4.20 | 3.93 | 5.00 | 0.00 |
| experiment12: retrieval sweep, strong checker and synthesizer, top_k=8 | multi_agent | 4.87 | 4.20 | 3.53 | 5.00 | 0.00 |
| experiment13: retrieval sweep, all strong models, top_k=3 | baseline | 4.93 | 3.20 | 2.73 | 5.00 | 0.07 |
| experiment13: retrieval sweep, all strong models, top_k=3 | multi_agent | 5.00 | 4.47 | 3.27 | 5.00 | 0.00 |
| experiment14: retrieval sweep, all strong models, top_k=8 | baseline | 4.80 | 3.27 | 3.13 | 4.93 | 0.00 |
| experiment14: retrieval sweep, all strong models, top_k=8 | multi_agent | 5.00 | 3.47 | 3.07 | 4.93 | 0.00 |
| experiment15: retrieval sweep, strong orchestrator only, top_k=3 | baseline | 5.00 | 4.00 | 4.47 | 5.00 | 0.00 |
| experiment15: retrieval sweep, strong orchestrator only, top_k=3 | multi_agent | 5.00 | 3.67 | 2.00 | 4.93 | 0.00 |
| experiment16: retrieval sweep, strong orchestrator only, top_k=8 | baseline | 5.00 | 4.13 | 3.93 | 5.00 | 0.00 |
| experiment16: retrieval sweep, strong orchestrator only, top_k=8 | multi_agent | 4.80 | 3.93 | 2.07 | 4.87 | 0.13 |
| experiment17: retrieval sweep, strong search agent only, top_k=3 | baseline | 5.00 | 4.27 | 4.33 | 5.00 | 0.00 |
| experiment17: retrieval sweep, strong search agent only, top_k=3 | multi_agent | 5.00 | 3.40 | 1.80 | 4.93 | 0.00 |
| experiment18: retrieval sweep, strong search agent only, top_k=8 | baseline | 5.00 | 3.87 | 3.27 | 5.00 | 0.00 |
| experiment18: retrieval sweep, strong search agent only, top_k=8 | multi_agent | 4.93 | 3.60 | 2.20 | 4.93 | 0.07 |
| experiment19: retrieval sweep, strong summarizer only, top_k=3 | baseline | 5.00 | 3.67 | 3.13 | 4.93 | 0.00 |
| experiment19: retrieval sweep, strong summarizer only, top_k=3 | multi_agent | 4.93 | 3.73 | 1.27 | 4.93 | 0.07 |
| experiment20: retrieval sweep, strong summarizer only, top_k=8 | baseline | 5.00 | 3.47 | 3.40 | 5.00 | 0.00 |
| experiment20: retrieval sweep, strong summarizer only, top_k=8 | multi_agent | 5.00 | 3.87 | 2.33 | 4.87 | 0.00 |
| experiment21: retrieval sweep, strong fact checker only, top_k=3 | baseline | 5.00 | 4.00 | 3.93 | 5.00 | 0.00 |
| experiment21: retrieval sweep, strong fact checker only, top_k=3 | multi_agent | 5.00 | 3.40 | 1.27 | 4.93 | 0.00 |
| experiment22: retrieval sweep, strong fact checker only, top_k=8 | baseline | 5.00 | 3.67 | 3.67 | 5.00 | 0.00 |
| experiment22: retrieval sweep, strong fact checker only, top_k=8 | multi_agent | 4.87 | 3.73 | 1.80 | 4.93 | 0.07 |
| experiment23: retrieval sweep, strong final synthesizer only, top_k=3 | baseline | 5.00 | 3.73 | 4.20 | 4.93 | 0.00 |
| experiment23: retrieval sweep, strong final synthesizer only, top_k=3 | multi_agent | 5.00 | 3.47 | 2.07 | 4.93 | 0.00 |
| experiment24: retrieval sweep, strong final synthesizer only, top_k=8 | baseline | 5.00 | 4.13 | 4.73 | 4.93 | 0.00 |
| experiment24: retrieval sweep, strong final synthesizer only, top_k=8 | multi_agent | 4.93 | 3.53 | 2.73 | 4.87 | 0.07 |