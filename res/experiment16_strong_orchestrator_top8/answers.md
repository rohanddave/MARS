# experiment16: retrieval sweep, strong orchestrator only, top_k=8

## Agent Configuration

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

## Question 1

Type: easy lookup

What external knowledge source or corpus does REALM retrieve from, and how is it used by the model?

### Baseline Answer

The provided context does not contain any information about the external knowledge source or corpus that REALM retrieves from, nor how it is used by the model. Therefore, this information is missing.

Citations: None

### Multi-Agent Answer

The provided evidence does not include information about the external knowledge source or corpus that REALM retrieves from, nor how this external knowledge is used by the model. Therefore, this question cannot be answered based on the current evidence. Additional details or evidence about REALM’s retrieval sources and usage would be needed to provide a definitive answer.

### Metrics

- baseline_latency_seconds: 1.587
- orchestrator_latency_seconds: 14.140
- baseline_total_tokens: 195
- orchestrator_total_tokens: 2602
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 3}

## Question 2

Type: easy lookup

Which downstream tasks or benchmarks does the paper use to evaluate REALM?

### Baseline Answer

The context provided does not include any information about the downstream tasks or benchmarks used to evaluate REALM. Therefore, it is missing the necessary details to answer the question.

Citations:
None.

### Multi-Agent Answer

No evidence notes are available that specify which downstream tasks or benchmarks are used to evaluate REALM. Therefore, the paper’s evaluation setup regarding downstream tasks or benchmarks cannot be determined from the provided information.

### Metrics

- baseline_latency_seconds: 1.321
- orchestrator_latency_seconds: 12.072
- baseline_total_tokens: 185
- orchestrator_total_tokens: 2432
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 1}

## Question 3

Type: definition

What is REALM, and what does the paper mean by retrieval-augmented language model pre-training?

### Baseline Answer

The provided context does not include any information about what REALM is or what is meant by retrieval-augmented language model pre-training. Additional context is needed to answer this question.

Citations:  
No citations available.

### Multi-Agent Answer

The available evidence does not include any information about REALM or the concept of retrieval-augmented language model pre-training. Therefore, it is not possible to provide a description or explanation of these terms based on the supplied context.

### Metrics

- baseline_latency_seconds: 1.424
- orchestrator_latency_seconds: 13.868
- baseline_total_tokens: 198
- orchestrator_total_tokens: 2497
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 1}

## Question 4

Type: definition

How does REALM differ from a standard parametric language model such as BERT in where knowledge is stored and accessed?

### Baseline Answer

The provided context does not contain information about how REALM differs from a standard parametric language model such as BERT in terms of where knowledge is stored and accessed.

Citations: None

### Multi-Agent Answer

No evidence is available to determine how REALM differs from a standard parametric language model such as BERT in where knowledge is stored and accessed [E1].

### Metrics

- baseline_latency_seconds: 1.600
- orchestrator_latency_seconds: 13.656
- baseline_total_tokens: 194
- orchestrator_total_tokens: 2781
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 1}

## Question 5

Type: method/mechanism

How does REALM's retrieve-then-predict framework work, including the role of the latent document variable z?

### Baseline Answer

The provided context does not contain any information about REALM's retrieve-then-predict framework or the role of the latent document variable z. Therefore, there is insufficient information to answer the question.

Citations:  
No citations available.

### Multi-Agent Answer

The provided evidence does not include any information about how REALM’s retrieve-then-predict framework works or about the role of the latent document variable z in this framework. Therefore, an answer to the question cannot be given based on the available evidence. To accurately respond, more evidence notes specifically describing REALM and the latent document variable z are needed.

### Metrics

- baseline_latency_seconds: 1.622
- orchestrator_latency_seconds: 16.810
- baseline_total_tokens: 203
- orchestrator_total_tokens: 2922
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 2}

## Question 6

Type: method/mechanism

How does the paper train the retriever when the retrieved document is latent, and how does learning signal flow back to retrieval?

### Baseline Answer

The provided context does not contain any information about training the retriever when the retrieved document is latent or how the learning signal flows back to retrieval. Therefore, the question cannot be answered based on the given context.

Citations:  
No citations available due to insufficient context.

### Multi-Agent Answer

There is no information available in the provided evidence regarding how the paper trains the retriever when the retrieved document is latent. The mechanism by which the learning signal flows back to the retrieval component is also not described in the given context. Therefore, these aspects cannot be addressed based on the current evidence. Additional evidence would be needed to provide a detailed answer.

### Metrics

- baseline_latency_seconds: 1.415
- orchestrator_latency_seconds: 16.761
- baseline_total_tokens: 212
- orchestrator_total_tokens: 3052
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 4}

## Question 7

Type: method/mechanism / implementation

What approximations or engineering choices does REALM use to make retrieval over a large corpus practical during training and inference?

### Baseline Answer

The provided context does not contain any information about the approximations or engineering choices used by REALM to make retrieval over a large corpus practical during training and inference. Therefore, I cannot answer the question based on the given context.

Citations:
No citations available from the given context.

### Multi-Agent Answer

There is no evidence available in the provided context regarding the approximations or engineering choices REALM uses to make retrieval over a large corpus practical during training and inference.

### Metrics

- baseline_latency_seconds: 3.606
- orchestrator_latency_seconds: 12.405
- baseline_total_tokens: 212
- orchestrator_total_tokens: 2528
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 1}

## Question 8

Type: comparison

How does REALM compare with ORQA or other open-domain QA baselines, and what evidence supports that comparison?

### Baseline Answer

The provided context does not contain any information regarding how REALM compares with ORQA or other open-domain QA baselines, nor does it provide any evidence to support such a comparison.

Citations:  
No citations available due to lack of context.

### Multi-Agent Answer

The provided evidence does not contain any information regarding the comparison between REALM and ORQA or other open-domain QA baselines [No evidence notes available]. Therefore, no supported statements can be made about how REALM compares with these models [No evidence notes available]. Additional evidence or sources are needed to answer this question accurately [No evidence notes available].

### Metrics

- baseline_latency_seconds: 2.068
- orchestrator_latency_seconds: 14.247
- baseline_total_tokens: 205
- orchestrator_total_tokens: 2934
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 3}

## Question 9

Type: comparison

How does REALM's retrieval-based approach compare with storing knowledge only in model parameters?

### Baseline Answer

The provided context does not contain information about how REALM's retrieval-based approach compares with storing knowledge only in model parameters. Therefore, this information is missing.

Citations:
None

### Multi-Agent Answer

The provided evidence does not include any information about how REALM’s retrieval-based approach compares with storing knowledge only in model parameters. Therefore, this question cannot be answered based on the available notes. Additional evidence specifically addressing REALM’s retrieval method versus parameter-based knowledge storage is needed to provide a complete answer.

### Metrics

- baseline_latency_seconds: 1.396
- orchestrator_latency_seconds: 15.771
- baseline_total_tokens: 185
- orchestrator_total_tokens: 2636
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 2}

## Question 10

Type: evidence synthesis / ablation

What ablation or diagnostic evidence shows that retrieval pre-training improves REALM rather than only the reader component?

### Baseline Answer

The provided context does not contain any information regarding ablation or diagnostic evidence showing that retrieval pre-training improves REALM rather than only the reader component. Therefore, it is not possible to answer the question based on the given context.

Citations: None

### Multi-Agent Answer

No evidence notes were provided that include ablation or diagnostic experiments demonstrating that retrieval pre-training improves REALM beyond improvements to the reader component. Therefore, it is not possible to determine from the available information whether retrieval pre-training itself contributes to REALM’s performance or if observed improvements arise solely from the reader.

### Metrics

- baseline_latency_seconds: 1.341
- orchestrator_latency_seconds: 13.573
- baseline_total_tokens: 203
- orchestrator_total_tokens: 2964
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 2}

## Question 11

Type: evidence synthesis

Synthesize the evidence for why REALM improves open-domain QA performance, including retrieval quality, pre-training, and downstream fine-tuning.

### Baseline Answer

The context provided does not contain any information regarding why REALM improves open-domain QA performance, including details about retrieval quality, pre-training, or downstream fine-tuning. Therefore, it is not possible to synthesize evidence on this topic from the given context.

Citations:  
No citations available due to lack of context.

### Multi-Agent Answer

There are no evidence notes available that provide information on why REALM improves open-domain QA performance, including aspects such as retrieval quality, pre-training, or downstream fine-tuning. Because of this lack of evidence, it is not possible to synthesize or make supported claims about the factors contributing to REALM’s performance improvements. Additional evidence retrieval would be necessary to address this question in detail.

### Metrics

- baseline_latency_seconds: 1.575
- orchestrator_latency_seconds: 16.707
- baseline_total_tokens: 224
- orchestrator_total_tokens: 2996
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 3}

## Question 12

Type: multi-step reasoning

Explain step by step how a masked-language-model pre-training objective can improve downstream open-domain QA in REALM.

### Baseline Answer

The provided context does not contain any information about how a masked-language-model (MLM) pre-training objective can improve downstream open-domain question answering (QA) in REALM. Therefore, it is not possible to explain this step by step using the given materials.

Citations:
No citations available due to insufficient context.

### Multi-Agent Answer

There are no evidence notes available to explain how a masked-language-model pre-training objective can improve downstream open-domain question answering in REALM. Therefore, it is not possible to provide a supported, step-by-step explanation for this process based on the current information. Additional specific evidence or sources would be needed to give an accurate and verified answer.

### Metrics

- baseline_latency_seconds: 1.519
- orchestrator_latency_seconds: 16.833
- baseline_total_tokens: 218
- orchestrator_total_tokens: 2550
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 3}

## Question 13

Type: multi-step reasoning / error analysis

If REALM retrieves an irrelevant document, how would that affect p(z|x), p(y|z,x), and the final answer prediction?

### Baseline Answer

The context provided contains no information regarding REALM, the effect of retrieving an irrelevant document, or how it would affect p(z|x), p(y|z,x), and the final answer prediction. Therefore, it is not possible to answer the question based on the given context.

Citations: None

### Multi-Agent Answer

There are no evidence notes available that address how retrieving an irrelevant document would affect \( p(z|x) \), \( p(y|z,x) \), or the final answer prediction in REALM. Therefore, the impact of retrieving an irrelevant document on these probabilities and the overall prediction cannot be determined from the available information.

### Metrics

- baseline_latency_seconds: 1.778
- orchestrator_latency_seconds: 15.684
- baseline_total_tokens: 222
- orchestrator_total_tokens: 3097
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 2}

## Question 14

Type: limitation/uncertainty

What limitations, uncertainties, or missing comparisons should be noted when interpreting REALM's reported results?

### Baseline Answer

The provided context does not include any information regarding REALM's reported results, their limitations, uncertainties, or comparisons. Therefore, it is not possible to identify or describe these aspects based on the given information.

Citations:
None.

### Multi-Agent Answer

There is insufficient information in the provided evidence notes to identify any limitations, uncertainties, or missing comparisons related to REALM’s reported results. No details or evaluations regarding these aspects are available for citation. Additional evidence or documentation would be needed to offer a supported analysis of REALM’s reported results and their interpretation.

### Metrics

- baseline_latency_seconds: 1.569
- orchestrator_latency_seconds: 14.868
- baseline_total_tokens: 198
- orchestrator_total_tokens: 2879
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 3}

## Question 15

Type: citation grounding / uncertainty

Which claims about REALM's performance or mechanism cannot be verified unless the answer cites specific experimental evidence from the paper?

### Baseline Answer

The context does not provide any information about REALM's performance or mechanism, nor does it include any specific experimental evidence from the paper. Therefore, it is impossible to verify any claims related to REALM without citing such evidence.

Citations:
No citations available.

### Multi-Agent Answer

Claims about REALM’s performance or mechanism cannot be verified without citing specific experimental evidence from the original paper because the provided evidence notes do not contain any information about REALM’s performance or mechanism [E1]. They also do not include specific experimental evidence from the original paper regarding REALM [E1]. Therefore, verification of such claims is not possible without referencing that specific experimental evidence [E1].

### Metrics

- baseline_latency_seconds: 1.621
- orchestrator_latency_seconds: 15.605
- baseline_total_tokens: 208
- orchestrator_total_tokens: 2967
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 3}
