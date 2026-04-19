# experiment15: retrieval sweep, strong orchestrator only, top_k=3

## Agent Configuration

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

## Question 1

Type: easy lookup

What external knowledge source or corpus does REALM retrieve from, and how is it used by the model?

### Baseline Answer

The context provided does not contain any information about the external knowledge source or corpus that REALM retrieves from, nor how it is used by the model. Therefore, this information is missing.

Citations:
None

### Multi-Agent Answer

No evidence notes were provided regarding the external knowledge source or corpus that REALM retrieves from, nor about how this information is used by the model. Therefore, the available evidence does not contain details on REALM’s retrieval corpus or its integration into the model’s prediction process.

### Metrics

- baseline_latency_seconds: 1.748
- orchestrator_latency_seconds: 15.761
- baseline_total_tokens: 195
- orchestrator_total_tokens: 2930
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 2}

## Question 2

Type: easy lookup

Which downstream tasks or benchmarks does the paper use to evaluate REALM?

### Baseline Answer

The provided context does not include any information about the downstream tasks or benchmarks used to evaluate REALM. Therefore, I cannot answer the question based on the given context.

Citations:  
None

### Multi-Agent Answer

No evidence notes were provided to identify the downstream tasks or benchmarks used to evaluate REALM. Therefore, the specific evaluation tasks for REALM cannot be determined from the available information. Additional evidence or documentation about REALM’s evaluation is needed to answer this question accurately.

### Metrics

- baseline_latency_seconds: 2.123
- orchestrator_latency_seconds: 12.161
- baseline_total_tokens: 185
- orchestrator_total_tokens: 2601
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 3}

## Question 3

Type: definition

What is REALM, and what does the paper mean by retrieval-augmented language model pre-training?

### Baseline Answer

The provided context does not contain any information about REALM or what is meant by retrieval-augmented language model pre-training. Therefore, it is not possible to answer the question based on the given context.

Citations:  
None available.

### Multi-Agent Answer

The provided evidence does not contain information about what REALM is or what is meant by retrieval-augmented language model pre-training, so this question cannot be answered from the supplied context.

### Metrics

- baseline_latency_seconds: 1.716
- orchestrator_latency_seconds: 15.596
- baseline_total_tokens: 202
- orchestrator_total_tokens: 2564
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 1}

## Question 4

Type: definition

How does REALM differ from a standard parametric language model such as BERT in where knowledge is stored and accessed?

### Baseline Answer

The provided context does not contain any information about REALM or how it differs from a standard parametric language model such as BERT in terms of where knowledge is stored and accessed. Therefore, it is not possible to answer the question based on the given context.

Citations:
None (insufficient context)

### Multi-Agent Answer

No evidence notes were provided to verify how REALM differs from a standard parametric language model such as BERT in terms of where knowledge is stored and accessed. Therefore, this comparison cannot be answered based on the available context.

### Metrics

- baseline_latency_seconds: 2.616
- orchestrator_latency_seconds: 13.909
- baseline_total_tokens: 218
- orchestrator_total_tokens: 2857
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 2}

## Question 5

Type: method/mechanism

How does REALM's retrieve-then-predict framework work, including the role of the latent document variable z?

### Baseline Answer

The provided context does not include any information about REALM's retrieve-then-predict framework or the role of the latent document variable z. Therefore, I cannot answer the question based on the given context.

Citations:
None

### Multi-Agent Answer

No evidence was provided to support any claims about how REALM's retrieve-then-predict framework works or the role of the latent document variable z. Therefore, a detailed explanation cannot be given based on the available context. Additional evidence or information is needed to address this question properly.

### Metrics

- baseline_latency_seconds: 1.623
- orchestrator_latency_seconds: 14.994
- baseline_total_tokens: 201
- orchestrator_total_tokens: 2776
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 3}

## Question 6

Type: method/mechanism

How does the paper train the retriever when the retrieved document is latent, and how does learning signal flow back to retrieval?

### Baseline Answer

The context provided explicitly states that no retrieved context was available, which means there is no information given about how the paper trains the retriever when the retrieved document is latent or how learning signal flows back to retrieval.

Therefore, the context is insufficient to answer the question.

Citations:  
None – context insufficient.

### Multi-Agent Answer

The provided evidence notes do not contain any information on how the paper trains the retriever when the retrieved document is latent, nor do they explain how the learning signal flows back to retrieval. Therefore, it is not possible to answer this question based on the current evidence. Additional details or excerpts from the paper regarding the retriever training methodology and the propagation of learning signals would be needed to provide a complete response.

### Metrics

- baseline_latency_seconds: 2.125
- orchestrator_latency_seconds: 13.495
- baseline_total_tokens: 220
- orchestrator_total_tokens: 3062
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 3}

## Question 7

Type: method/mechanism / implementation

What approximations or engineering choices does REALM use to make retrieval over a large corpus practical during training and inference?

### Baseline Answer

The provided context does not contain any information about the approximations or engineering choices made by REALM to make retrieval over a large corpus practical during training and inference. Therefore, this information is missing.

Citations:  
No citations available.

### Multi-Agent Answer

The provided evidence does not include any information about the approximations or engineering choices used by REALM to make retrieval over a large corpus practical during training and inference.

### Metrics

- baseline_latency_seconds: 1.608
- orchestrator_latency_seconds: 13.405
- baseline_total_tokens: 203
- orchestrator_total_tokens: 2716
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 1}

## Question 8

Type: comparison

How does REALM compare with ORQA or other open-domain QA baselines, and what evidence supports that comparison?

### Baseline Answer

The provided context does not contain any information about how REALM compares with ORQA or other open-domain QA baselines, nor does it provide any supporting evidence for such a comparison.

Citations:  
No citations available due to missing context.

### Multi-Agent Answer

There is no evidence provided regarding how REALM compares with ORQA or other open-domain QA baselines because the supplied context does not include any information or data supporting such a comparison. Therefore, a direct comparison cannot be made based on the available evidence.

### Metrics

- baseline_latency_seconds: 5.000
- orchestrator_latency_seconds: 14.442
- baseline_total_tokens: 204
- orchestrator_total_tokens: 2466
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 3}

## Question 9

Type: comparison

How does REALM's retrieval-based approach compare with storing knowledge only in model parameters?

### Baseline Answer

The provided context does not contain any information about REALM's retrieval-based approach or how it compares with storing knowledge only in model parameters. Therefore, the answer cannot be determined from the given context.

Citations:  
No citations available from the provided context.

### Multi-Agent Answer

There are no evidence notes available to compare REALM's retrieval-based approach with storing knowledge only in model parameters.

### Metrics

- baseline_latency_seconds: 1.714
- orchestrator_latency_seconds: 16.340
- baseline_total_tokens: 201
- orchestrator_total_tokens: 3096
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 2}

## Question 10

Type: evidence synthesis / ablation

What ablation or diagnostic evidence shows that retrieval pre-training improves REALM rather than only the reader component?

### Baseline Answer

The provided context does not contain any information about ablation or diagnostic evidence showing that retrieval pre-training improves REALM rather than only the reader component. Therefore, this information is missing.

Citations:  
None.

### Multi-Agent Answer

The provided evidence does not include any ablation or diagnostic experiments that specifically demonstrate that retrieval pre-training improves REALM independently of the reader component. There is no information about analyses isolating the effect of retrieval pre-training from the reader’s performance. Therefore, based on the current available evidence, it is not possible to determine whether retrieval pre-training alone contributes to the improvements observed in REALM. Additional experimental results or detailed ablation studies would be needed to verify this claim.

### Metrics

- baseline_latency_seconds: 2.117
- orchestrator_latency_seconds: 19.871
- baseline_total_tokens: 196
- orchestrator_total_tokens: 3510
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 4}

## Question 11

Type: evidence synthesis

Synthesize the evidence for why REALM improves open-domain QA performance, including retrieval quality, pre-training, and downstream fine-tuning.

### Baseline Answer

The provided context does not contain any information regarding REALM or its impact on open-domain QA performance, including details about retrieval quality, pre-training, or downstream fine-tuning. Therefore, it is not possible to synthesize evidence or answer the question based on the available information.

Citations:  
No citations available due to lack of context.

### Multi-Agent Answer

The provided evidence does not include any information on why REALM improves open-domain QA performance, including aspects such as retrieval quality, pre-training, or downstream fine-tuning. Therefore, a synthesis on this topic cannot be provided from these notes due to insufficient evidence.

### Metrics

- baseline_latency_seconds: 3.705
- orchestrator_latency_seconds: 15.053
- baseline_total_tokens: 228
- orchestrator_total_tokens: 2863
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 2}

## Question 12

Type: multi-step reasoning

Explain step by step how a masked-language-model pre-training objective can improve downstream open-domain QA in REALM.

### Baseline Answer

The provided context does not contain any information about masked-language-model pre-training objectives or how they improve downstream open-domain question answering (QA) in REALM. Therefore, it is not possible to explain the step-by-step process based on the given context.

Citations:  
No sources provided in the context.

### Multi-Agent Answer

The provided evidence does not include information on how a masked-language-model pre-training objective can improve downstream open-domain QA in REALM. Therefore, a step-by-step explanation based on the supplied context cannot be provided. Additional evidence would be needed to supply such an explanation.

### Metrics

- baseline_latency_seconds: 1.471
- orchestrator_latency_seconds: 13.100
- baseline_total_tokens: 216
- orchestrator_total_tokens: 2824
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 2}

## Question 13

Type: multi-step reasoning / error analysis

If REALM retrieves an irrelevant document, how would that affect p(z|x), p(y|z,x), and the final answer prediction?

### Baseline Answer

The provided context does not contain any information about how retrieving an irrelevant document with REALM would affect p(z|x), p(y|z,x), or the final answer prediction.

Citations:  
No citations available due to missing context.

### Multi-Agent Answer

The provided evidence does not include any information about how retrieving an irrelevant document by REALM would affect the distributions \( p(z|x) \), \( p(y|z,x) \), or the final answer prediction. Therefore, no supported conclusions can be drawn about these effects based on the available evidence. Additional evidence specifically addressing REALM’s behavior with irrelevant documents and the impact on these probability distributions and final predictions would be needed to answer the question.

### Metrics

- baseline_latency_seconds: 1.540
- orchestrator_latency_seconds: 16.641
- baseline_total_tokens: 210
- orchestrator_total_tokens: 3435
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 2}

## Question 14

Type: limitation/uncertainty

What limitations, uncertainties, or missing comparisons should be noted when interpreting REALM's reported results?

### Baseline Answer

The context provided does not contain any information about REALM or its reported results, including any limitations, uncertainties, or missing comparisons. Therefore, it is not possible to answer the question based on the given context.

Citations:  
None – no context provided.

### Multi-Agent Answer

There are no evidence notes available to determine the limitations, uncertainties, or missing comparisons in interpreting REALM's reported results [E1]. Therefore, it is not possible to provide a detailed answer based on the supplied context [E1]. Additional information or evidence regarding REALM's evaluation, benchmarks, or comparative analyses would be needed to address this question accurately [E1].

### Metrics

- baseline_latency_seconds: 3.392
- orchestrator_latency_seconds: 15.627
- baseline_total_tokens: 204
- orchestrator_total_tokens: 3045
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 3}

## Question 15

Type: citation grounding / uncertainty

Which claims about REALM's performance or mechanism cannot be verified unless the answer cites specific experimental evidence from the paper?

### Baseline Answer

The context provided does not contain any information about REALM's performance, mechanism, or experimental evidence. Therefore, it is impossible to verify which claims about REALM require citation from specific experimental evidence in the paper.

Citations:
None – no context was provided.

### Multi-Agent Answer

There are no evidence notes available that provide information about REALM’s performance or mechanism [E0]. Therefore, any claims regarding these aspects cannot be verified without citing specific experimental evidence from the paper [E0]. To verify such claims, more detailed evidence directly related to REALM’s experimental results or methodological descriptions would be required [E0].

### Metrics

- baseline_latency_seconds: 1.424
- orchestrator_latency_seconds: 15.070
- baseline_total_tokens: 208
- orchestrator_total_tokens: 2889
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 3}
