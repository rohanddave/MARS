# experiment22: retrieval sweep, strong fact checker only, top_k=8

## Agent Configuration

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

## Question 1

Type: easy lookup

What external knowledge source or corpus does REALM retrieve from, and how is it used by the model?

### Baseline Answer

The provided context does not contain information about the external knowledge source or corpus that REALM retrieves from, nor does it explain how this is used by the model. Therefore, this information is missing.

Citations: None

### Multi-Agent Answer

The provided evidence does not include any information about the external knowledge source or corpus that REALM retrieves from, nor how it is used by the model. Therefore, this question cannot be answered based on the available context.

### Metrics

- baseline_latency_seconds: 1.634
- orchestrator_latency_seconds: 16.025
- baseline_total_tokens: 197
- orchestrator_total_tokens: 2887
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 2}

## Question 2

Type: easy lookup

Which downstream tasks or benchmarks does the paper use to evaluate REALM?

### Baseline Answer

The context does not provide information about the downstream tasks or benchmarks used to evaluate REALM. Therefore, this information is missing.

Citations:
No citations available due to missing context.

### Multi-Agent Answer

The provided evidence does not include information about the downstream tasks or benchmarks used to evaluate REALM. Therefore, it is not possible to specify which tasks or benchmarks the paper uses for evaluation based on the available evidence. Additional information would be needed to answer this question.

### Metrics

- baseline_latency_seconds: 3.441
- orchestrator_latency_seconds: 13.303
- baseline_total_tokens: 183
- orchestrator_total_tokens: 2797
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 2}

## Question 3

Type: definition

What is REALM, and what does the paper mean by retrieval-augmented language model pre-training?

### Baseline Answer

The provided context does not contain any information about REALM or the meaning of retrieval-augmented language model pre-training. Therefore, I cannot answer the question based on the available context.

Citations:  
No citations available.

### Multi-Agent Answer

The provided evidence does not include any information about what REALM is or what is meant by retrieval-augmented language model pre-training, so that explanation cannot be provided from these notes.

### Metrics

- baseline_latency_seconds: 1.730
- orchestrator_latency_seconds: 14.559
- baseline_total_tokens: 199
- orchestrator_total_tokens: 2726
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 1}

## Question 4

Type: definition

How does REALM differ from a standard parametric language model such as BERT in where knowledge is stored and accessed?

### Baseline Answer

The provided context does not contain any information about how REALM differs from a standard parametric language model such as BERT in terms of where knowledge is stored and accessed. More details or specific descriptions comparing REALM and BERT are needed to answer this question.

Citations:
None

### Multi-Agent Answer

The provided evidence does not include information about how REALM differs from a standard parametric language model such as BERT in where knowledge is stored and accessed [E1]. Therefore, this comparison cannot be addressed based on the available context [E1].

### Metrics

- baseline_latency_seconds: 1.760
- orchestrator_latency_seconds: 16.876
- baseline_total_tokens: 213
- orchestrator_total_tokens: 3103
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 2}

## Question 5

Type: method/mechanism

How does REALM's retrieve-then-predict framework work, including the role of the latent document variable z?

### Baseline Answer

The provided context does not contain any information about REALM's retrieve-then-predict framework or the role of the latent document variable z. Therefore, I cannot answer the question based on the supplied context.

Citations: 
No citations available due to lack of context.

### Multi-Agent Answer

The provided evidence does not include information about how REALM's retrieve-then-predict framework works or the role of the latent document variable z [E1]. Therefore, an answer to this question cannot be provided based on the available evidence [E1].

### Metrics

- baseline_latency_seconds: 3.620
- orchestrator_latency_seconds: 15.090
- baseline_total_tokens: 210
- orchestrator_total_tokens: 2815
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 2}

## Question 6

Type: method/mechanism

How does the paper train the retriever when the retrieved document is latent, and how does learning signal flow back to retrieval?

### Baseline Answer

The provided context does not contain any information about how the paper trains the retriever when the retrieved document is latent or how the learning signal flows back to retrieval. More context is needed to answer the question.

Citations:
No citations available in the provided context.

### Multi-Agent Answer

The provided evidence does not include information about how the paper trains the retriever when the retrieved document is latent or how the learning signal flows back to retrieval. Therefore, this detail cannot be answered from the available notes.

### Metrics

- baseline_latency_seconds: 1.954
- orchestrator_latency_seconds: 14.694
- baseline_total_tokens: 210
- orchestrator_total_tokens: 2766
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 2}

## Question 7

Type: method/mechanism / implementation

What approximations or engineering choices does REALM use to make retrieval over a large corpus practical during training and inference?

### Baseline Answer

The context provided does not contain any information about the approximations or engineering choices used by REALM to make retrieval over a large corpus practical during training and inference. Therefore, this information is missing.

Citations: None

### Multi-Agent Answer

The provided evidence does not include any information about the approximations or engineering choices that REALM uses to make retrieval over a large corpus practical during training and inference. Therefore, this question cannot be answered based on the available context.

### Metrics

- baseline_latency_seconds: 1.880
- orchestrator_latency_seconds: 14.694
- baseline_total_tokens: 199
- orchestrator_total_tokens: 3069
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 2}

## Question 8

Type: comparison

How does REALM compare with ORQA or other open-domain QA baselines, and what evidence supports that comparison?

### Baseline Answer

The provided context does not contain any information about how REALM compares with ORQA or other open-domain QA baselines, nor any evidence supporting such comparisons.

Citations:  
No citations available in the provided context.

### Multi-Agent Answer

No evidence is provided regarding how REALM compares with ORQA or other open-domain QA baselines. Therefore, it is not possible to make any factual claims or draw comparisons about their performance or characteristics based on the available information. Additional evidence or documentation is needed to evaluate these systems comparatively.

### Metrics

- baseline_latency_seconds: 1.424
- orchestrator_latency_seconds: 14.450
- baseline_total_tokens: 199
- orchestrator_total_tokens: 3370
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 2}

## Question 9

Type: comparison

How does REALM's retrieval-based approach compare with storing knowledge only in model parameters?

### Baseline Answer

The provided context does not contain any information about REALM's retrieval-based approach or its comparison with storing knowledge solely in model parameters. Therefore, it is insufficient to answer the question.

Citations:
No citations available.

### Multi-Agent Answer

The provided evidence does not include any information about how REALM's retrieval-based approach compares with storing knowledge only in model parameters [E1]. Therefore, a comparison between these two approaches cannot be made based on the available evidence [E1].

### Metrics

- baseline_latency_seconds: 2.050
- orchestrator_latency_seconds: 15.455
- baseline_total_tokens: 193
- orchestrator_total_tokens: 3037
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 2}

## Question 10

Type: evidence synthesis / ablation

What ablation or diagnostic evidence shows that retrieval pre-training improves REALM rather than only the reader component?

### Baseline Answer

The provided context does not include any ablation or diagnostic evidence regarding how retrieval pre-training specifically improves the REALM model beyond the reader component. Therefore, the context is insufficient to answer the question.

Citations: None

### Multi-Agent Answer

The available evidence does not include any ablation or diagnostic studies that specifically isolate the effect of retrieval pre-training on improving REALM, as distinct from improvements arising solely from the reader component. Therefore, no conclusions can be drawn about whether or how retrieval pre-training independently contributes to REALM’s performance based on the currently supplied information. Additional evidence focusing on retrieval pre-training ablations or diagnostics would be needed to answer this question.

### Metrics

- baseline_latency_seconds: 1.833
- orchestrator_latency_seconds: 16.470
- baseline_total_tokens: 197
- orchestrator_total_tokens: 3203
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 2}

## Question 11

Type: evidence synthesis

Synthesize the evidence for why REALM improves open-domain QA performance, including retrieval quality, pre-training, and downstream fine-tuning.

### Baseline Answer

The context provided is insufficient to synthesize the evidence for why REALM improves open-domain QA performance, including details about retrieval quality, pre-training, and downstream fine-tuning.

Citations:  
No citations available in the provided context.

### Multi-Agent Answer

No evidence notes are available to synthesize the reasons why REALM improves open-domain QA performance, including aspects such as retrieval quality, pre-training, and downstream fine-tuning.

### Metrics

- baseline_latency_seconds: 1.538
- orchestrator_latency_seconds: 13.846
- baseline_total_tokens: 207
- orchestrator_total_tokens: 3224
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 2}

## Question 12

Type: multi-step reasoning

Explain step by step how a masked-language-model pre-training objective can improve downstream open-domain QA in REALM.

### Baseline Answer

The provided context does not include information about how a masked-language-model pre-training objective can improve downstream open-domain QA in REALM. Therefore, I cannot provide a step-by-step explanation based on the available data.

Citations:  
No relevant sources provided.

### Multi-Agent Answer

The provided evidence does not include information on how a masked-language-model pre-training objective can improve downstream open-domain QA in REALM. Therefore, a step-by-step explanation based on the current context cannot be given.

### Metrics

- baseline_latency_seconds: 1.586
- orchestrator_latency_seconds: 12.557
- baseline_total_tokens: 206
- orchestrator_total_tokens: 2935
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 2}

## Question 13

Type: multi-step reasoning / error analysis

If REALM retrieves an irrelevant document, how would that affect p(z|x), p(y|z,x), and the final answer prediction?

### Baseline Answer

The provided context does not contain any information about how REALM's retrieval of an irrelevant document would affect p(z|x), p(y|z,x), or the final answer prediction. Therefore, it is not possible to answer the question based on the given context.

Citations:  
No citations available.

### Multi-Agent Answer

The provided evidence does not include information about how retrieving an irrelevant document would affect p(z|x), p(y|z,x), or the final answer prediction in REALM [E1]. Therefore, this impact cannot be determined from the available evidence [E1].

### Metrics

- baseline_latency_seconds: 1.433
- orchestrator_latency_seconds: 16.376
- baseline_total_tokens: 223
- orchestrator_total_tokens: 2950
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 2}

## Question 14

Type: limitation/uncertainty

What limitations, uncertainties, or missing comparisons should be noted when interpreting REALM's reported results?

### Baseline Answer

The provided context does not contain any information about the limitations, uncertainties, or missing comparisons related to interpreting REALM's reported results. Therefore, this information is missing.

Citations: None

### Multi-Agent Answer

The provided evidence does not contain information regarding limitations, uncertainties, or missing comparisons related to REALM’s reported results. Therefore, these aspects cannot be addressed based on the available context. Additional evidence or retrieval would be necessary to provide a detailed response on this question.

### Metrics

- baseline_latency_seconds: 1.448
- orchestrator_latency_seconds: 14.243
- baseline_total_tokens: 189
- orchestrator_total_tokens: 3002
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 3}

## Question 15

Type: citation grounding / uncertainty

Which claims about REALM's performance or mechanism cannot be verified unless the answer cites specific experimental evidence from the paper?

### Baseline Answer

The context provided does not include any information about REALM's performance or mechanism, nor does it contain any experimental evidence or claims about these aspects. Therefore, it is impossible to verify any claims about REALM's performance or mechanism without specific experimental evidence from the paper.

Citations:  
No citations available due to lack of context.

### Multi-Agent Answer

No evidence notes are available, so no claims about REALM’s performance or mechanism can be verified or evaluated. Please provide the relevant experimental evidence from the paper to enable a proper claim-by-claim analysis.

### Metrics

- baseline_latency_seconds: 1.696
- orchestrator_latency_seconds: 15.992
- baseline_total_tokens: 222
- orchestrator_total_tokens: 3283
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 2}
