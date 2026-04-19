# experiment14: retrieval sweep, all strong models, top_k=8

## Agent Configuration

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

## Question 1

Type: easy lookup

What external knowledge source or corpus does REALM retrieve from, and how is it used by the model?

### Baseline Answer

The context provided does not contain information about the external knowledge source or corpus that REALM retrieves from, nor how it is used by the model.

Citations:
None (insufficient context provided).

### Multi-Agent Answer

The evidence notes do not contain any information about what external knowledge source or corpus REALM retrieves from, nor how it is used by the model [E1]. Therefore, this cannot be answered based on the provided evidence [E1].

### Metrics

- baseline_latency_seconds: 2.898
- orchestrator_latency_seconds: 14.952
- baseline_total_tokens: 193
- orchestrator_total_tokens: 2830
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 2}

## Question 2

Type: easy lookup

Which downstream tasks or benchmarks does the paper use to evaluate REALM?

### Baseline Answer

The context does not provide information about which downstream tasks or benchmarks the paper uses to evaluate REALM.

Citations:
None (no relevant information in the supplied context).

### Multi-Agent Answer

The provided evidence does not include information about which downstream tasks or benchmarks are used to evaluate REALM. Thus, this cannot be determined from the available notes.

### Metrics

- baseline_latency_seconds: 1.538
- orchestrator_latency_seconds: 17.974
- baseline_total_tokens: 180
- orchestrator_total_tokens: 2616
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 2}

## Question 3

Type: definition

What is REALM, and what does the paper mean by retrieval-augmented language model pre-training?

### Baseline Answer

The context provided does not contain information about what REALM is or what is meant by retrieval-augmented language model pre-training. As a result, I cannot answer the question based only on the given context.

Citations:
None (no relevant context provided).

### Multi-Agent Answer

The provided evidence notes are insufficient to answer the question about what REALM is or what is meant by retrieval-augmented language model pre-training [E1]. There are no evidence notes available to support any factual claims [E1].

### Metrics

- baseline_latency_seconds: 1.918
- orchestrator_latency_seconds: 15.959
- baseline_total_tokens: 206
- orchestrator_total_tokens: 2920
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 2}

## Question 4

Type: definition

How does REALM differ from a standard parametric language model such as BERT in where knowledge is stored and accessed?

### Baseline Answer

The context provided does not contain information about how REALM differs from a standard parametric language model such as BERT in terms of where knowledge is stored and accessed.

Citations:
None (no relevant context provided).

### Multi-Agent Answer

The evidence notes are not available, so it is not possible to answer how REALM differs from a standard parametric language model such as BERT in where knowledge is stored and accessed.

### Metrics

- baseline_latency_seconds: 1.478
- orchestrator_latency_seconds: 12.979
- baseline_total_tokens: 200
- orchestrator_total_tokens: 2770
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 1}

## Question 5

Type: method/mechanism

How does REALM's retrieve-then-predict framework work, including the role of the latent document variable z?

### Baseline Answer

The context provided does not contain information about how REALM's retrieve-then-predict framework works or the role of the latent document variable z.

Citations:
None (no relevant context was provided).

### Multi-Agent Answer

The provided evidence does not contain any information about how REALM's retrieve-then-predict framework works or the role of the latent document variable z. Therefore, this question cannot be answered based on the available evidence notes.

### Metrics

- baseline_latency_seconds: 2.073
- orchestrator_latency_seconds: 17.533
- baseline_total_tokens: 196
- orchestrator_total_tokens: 2778
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 2}

## Question 6

Type: method/mechanism

How does the paper train the retriever when the retrieved document is latent, and how does learning signal flow back to retrieval?

### Baseline Answer

The context provided does not contain information about how the paper trains the retriever when the retrieved document is latent, or how the learning signal flows back to retrieval. 

Citations:
No citations available due to insufficient context.

### Multi-Agent Answer

Because there are no evidence notes available, it is not possible to answer the question regarding how the paper trains the retriever when the retrieved document is latent or how the learning signal flows back to retrieval [No evidence notes available].

### Metrics

- baseline_latency_seconds: 1.590
- orchestrator_latency_seconds: 21.183
- baseline_total_tokens: 202
- orchestrator_total_tokens: 3321
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 1}

## Question 7

Type: method/mechanism / implementation

What approximations or engineering choices does REALM use to make retrieval over a large corpus practical during training and inference?

### Baseline Answer

The context does not provide information about the approximations or engineering choices REALM uses to make retrieval over a large corpus practical during training and inference.

Citations:
None (no context provided).

### Multi-Agent Answer

The evidence notes do not provide any information about the approximations or engineering choices that REALM uses to make retrieval over a large corpus practical during training and inference.

### Metrics

- baseline_latency_seconds: 2.247
- orchestrator_latency_seconds: 15.605
- baseline_total_tokens: 194
- orchestrator_total_tokens: 2733
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 1}

## Question 8

Type: comparison

How does REALM compare with ORQA or other open-domain QA baselines, and what evidence supports that comparison?

### Baseline Answer

The context provided does not include any information about how REALM compares with ORQA or other open-domain QA baselines, nor does it provide evidence supporting such a comparison.

Citations:
None—no relevant context provided.

### Multi-Agent Answer

The provided evidence does not include any information about how REALM compares with ORQA or other open-domain QA baselines, so this comparison cannot be made based on the available notes. If a substantive comparison is required, further evidence regarding REALM, ORQA, and open-domain QA baselines is necessary.

### Metrics

- baseline_latency_seconds: 2.179
- orchestrator_latency_seconds: 19.092
- baseline_total_tokens: 200
- orchestrator_total_tokens: 3299
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 2}

## Question 9

Type: comparison

How does REALM's retrieval-based approach compare with storing knowledge only in model parameters?

### Baseline Answer

The context provided does not contain information about how REALM's retrieval-based approach compares with storing knowledge only in model parameters.

Citations:
None (no relevant context provided).

### Multi-Agent Answer

The provided evidence does not include any information regarding how REALM's retrieval-based approach compares with storing knowledge only in model parameters. Therefore, this comparison cannot be answered based on the available evidence.

### Metrics

- baseline_latency_seconds: 1.713
- orchestrator_latency_seconds: 17.772
- baseline_total_tokens: 184
- orchestrator_total_tokens: 2924
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 2}

## Question 10

Type: evidence synthesis / ablation

What ablation or diagnostic evidence shows that retrieval pre-training improves REALM rather than only the reader component?

### Baseline Answer

The context provided does not contain any information regarding ablation or diagnostic evidence about retrieval pre-training improving REALM, nor does it discuss whether improvements are due to retrieval or the reader component.

Citations:
N/A (No relevant sources were provided in the context.)

### Multi-Agent Answer

The provided evidence does not include any notes [E1]. As a result, it is not possible to determine what ablation or diagnostic evidence—if any—shows that retrieval pre-training improves REALM rather than only the reader component [E1].

### Metrics

- baseline_latency_seconds: 1.756
- orchestrator_latency_seconds: 15.927
- baseline_total_tokens: 206
- orchestrator_total_tokens: 3041
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 2}

## Question 11

Type: evidence synthesis

Synthesize the evidence for why REALM improves open-domain QA performance, including retrieval quality, pre-training, and downstream fine-tuning.

### Baseline Answer

There is no information available in the provided context to synthesize the evidence for why REALM improves open-domain QA performance, including retrieval quality, pre-training, and downstream fine-tuning.

Citations:
None (no context provided)

### Multi-Agent Answer

The provided evidence does not include any notes, so it is not possible to synthesize supported reasons for why REALM improves open-domain QA performance, including retrieval quality, pre-training, and downstream fine-tuning. Further evidence is needed to answer this question.

### Metrics

- baseline_latency_seconds: 1.749
- orchestrator_latency_seconds: 16.326
- baseline_total_tokens: 206
- orchestrator_total_tokens: 3165
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 2}

## Question 12

Type: multi-step reasoning

Explain step by step how a masked-language-model pre-training objective can improve downstream open-domain QA in REALM.

### Baseline Answer

There is insufficient context to answer the question about how a masked-language-model pre-training objective can improve downstream open-domain QA in REALM.

Citations:
None (no context was provided).

### Multi-Agent Answer

The evidence notes required to answer this question are not available. Therefore, it is not possible to explain step by step how a masked-language-model pre-training objective can improve downstream open-domain QA in REALM based on the supplied evidence.

### Metrics

- baseline_latency_seconds: 1.392
- orchestrator_latency_seconds: 16.476
- baseline_total_tokens: 192
- orchestrator_total_tokens: 2946
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 2}

## Question 13

Type: multi-step reasoning / error analysis

If REALM retrieves an irrelevant document, how would that affect p(z|x), p(y|z,x), and the final answer prediction?

### Baseline Answer

The context does not provide information about how REALM's retrieval of an irrelevant document would affect p(z|x), p(y|z,x), or the final answer prediction.

Citations:
None (no relevant context provided).

### Multi-Agent Answer

The provided evidence does not include any information about how REALM handles the situation when an irrelevant document is retrieved [E1]. The notes also do not specify the impact on p(z|x), p(y|z,x), or the final answer prediction [E1]. Therefore, it is not possible to answer this question based on the evidence notes provided [E1].

### Metrics

- baseline_latency_seconds: 2.036
- orchestrator_latency_seconds: 15.625
- baseline_total_tokens: 207
- orchestrator_total_tokens: 3333
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 3}

## Question 14

Type: limitation/uncertainty

What limitations, uncertainties, or missing comparisons should be noted when interpreting REALM's reported results?

### Baseline Answer

The provided context does not include any information about the limitations, uncertainties, or missing comparisons related to REALM's reported results. Therefore, it is not possible to answer the question based on the supplied context.

Citations
None (no relevant context provided).

### Multi-Agent Answer

The provided evidence notes do not include any information about REALM's limitations, uncertainties, or missing comparisons. Therefore, it is not possible to identify or discuss these aspects based on the available evidence. Additional evidence would be needed to answer this question fully.

### Metrics

- baseline_latency_seconds: 1.504
- orchestrator_latency_seconds: 17.299
- baseline_total_tokens: 203
- orchestrator_total_tokens: 3155
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 3}

## Question 15

Type: citation grounding / uncertainty

Which claims about REALM's performance or mechanism cannot be verified unless the answer cites specific experimental evidence from the paper?

### Baseline Answer

Claims about REALM's performance or mechanism that cannot be verified unless the answer cites specific experimental evidence from the paper include any statements about how well REALM performs on certain tasks, comparisons to other models, or details about its empirical results. Because no specific experimental evidence from the paper is included in the provided context, none of these claims can currently be verified.

Citations
None—no retrieved context was available.

### Multi-Agent Answer

No claims about REALM's performance or mechanism can be verified because there are no evidence notes available to support such claims [No evidence notes available].

### Metrics

- baseline_latency_seconds: 1.954
- orchestrator_latency_seconds: 18.700
- baseline_total_tokens: 238
- orchestrator_total_tokens: 3239
- baseline_citation_count: 0
- orchestrator_evidence_count: 0
- fact_check_status_counts: {'unsupported': 1}
