# experiment2: fast same-model config

## Agent Configuration

- top_k: 3
- orchestrator_model: gpt-4.1-mini
- search_model: gpt-4.1-mini
- summarization_model: gpt-4.1-mini
- fact_check_model: gpt-4.1-mini
- final_synthesis_model: gpt-4.1-mini

## Question 1

What is REALM and how does it differ from traditional language models like BERT in terms of knowledge storage and retrieval?

### Baseline Answer

REALM (Retrieval-Augmented Language Model) is a novel framework for language model pre-training that incorporates a learned textual knowledge retriever. Unlike traditional language models like BERT that store knowledge within their parameters, REALM explicitly separates the process of knowledge retrieval from language modeling. This framework exposes the role of world knowledge by allowing the model to retrieve relevant information from external text sources dynamically, rather than relying solely on the fixed information encoded in its parameters during training [1][2][3].

Citations:  
[1][2][3] data/2002.08909v1.pdf

### Multi-Agent Answer

REALM, which stands for Retrieval-Augmented Language Model pre-training, is a novel framework that enhances language model pre-training by integrating a learned textual knowledge retriever [E1][E2][E5][E6][E9]. Unlike traditional language models such as BERT that store knowledge solely within their parameters, REALM explicitly exposes the role of world knowledge by requiring the model to retrieve relevant external documents during training [E1][E2][E3][E4][E5][E6][E9]. This retrieval mechanism allows REALM to access and incorporate information from external textual knowledge dynamically instead of relying on static knowledge encoded inside fixed model parameters [E1][E2][E5][E6].

As an example of this advantage, REALM can assign significantly higher probabilities to correct masked tokens by conditioning on retrieved documents. Specifically, for the masked token “Fermat,” REALM assigns a much higher likelihood compared to BERT without retrieval—REALM’s marginalized probability is 0.129, while BERT’s probability is 1.1 × 10⁻¹⁴ [E8].

### Metrics

- baseline_latency_seconds: 2.736
- orchestrator_latency_seconds: 70.249
- baseline_total_tokens: 651
- orchestrator_total_tokens: 25939
- baseline_citation_count: 3
- orchestrator_evidence_count: 12
- fact_check_status_counts: {'supported': 5, 'unsupported': 2}

## Question 2

Explain how the retrieve-then-predict framework works in REALM, including the role of the latent variable z and backpropagation through the retriever.

### Baseline Answer

The retrieve-then-predict framework in REALM works by decomposing the conditional probability of an output \( y \) given input \( x \) into two steps: retrieval and prediction. Specifically, REALM models the output distribution as

\[
p(y|x) = \sum_{z \in Z} p(y|z,x) p(z|x),
\]

where \( Z \) is a large corpus of documents and \( z \) is treated as a latent variable representing the retrieved document(s) relevant to \( x \) [1].

1. **Role of the latent variable \( z \):**  
   The variable \( z \) stands for the documents retrieved from the knowledge corpus that help in answering the query or predicting the missing token. Since \( z \) is latent, REALM marginalizes over all possible documents \( z \in Z \) to compute the output likelihood. This means the model effectively considers multiple possible relevant documents when generating the final prediction \( y \).

2. **Retriever component (modeling \( p(z|x) \)):**  
   The retriever assigns probabilities to documents conditioned on the input \( x \) by embedding both \( x \) and candidate documents \( z \) into a shared vector space and computing their inner product as a relevance score:

   \[
   p(z|x) = \frac{\exp(f(x,z))}{\sum_{z'} \exp(f(x,z'))}, \quad f(x,z) = \text{Embed}_{\text{input}}(x)^\top \text{Embed}_{\text{doc}}(z).
   \]

   Embeddings are produced by BERT-style Transformers followed by a linear projection to a lower dimension, e.g.,

   \[
   \text{Embed}_{\text{input}}(x) = W_{\text{input}} \cdot \text{BERT}_{\text{CLS}}(\text{joinBERT}(x)),
   \]

   \[
   \text{Embed}_{\text{doc}}(z) = W_{\text{doc}} \cdot \text{BERT}_{\text{CLS}}(\text{joinBERT}(z_{\text{title}}, z_{\text{body}})),
   \]

   where joinBERT formats input and document text appropriately with [CLS] and [SEP] tokens [1].

3. **Knowledge-augmented encoder (modeling \( p(y|z,x)

### Multi-Agent Answer

The retrieve-then-predict framework in REALM operates by augmenting standard language model pre-training with a learned textual knowledge retriever that explicitly retrieves relevant information during training [E1][E2][E3][E5]. Instead of relying solely on the model's parameters to store knowledge, REALM exposes the role of external world knowledge by querying documents from a knowledge corpus to assist in prediction tasks [E1][E2][E3][E5].

Within this framework, the latent variable \( z \) represents a retrieved document from the knowledge corpus that the model conditions on to generate or predict the answer \( y \) given the input \( x \) [E4]. The conditional probability distributions \( p(z|x) \) and \( p(y|z,x) \) characterize the retrieval and prediction components, respectively, and the training objective uses these distributions to compute gradients that adjust both the retriever and the language model [E4].

Specifically, the gradient of the pre-training objective with respect to the retriever parameters is expressed as a sum over documents weighted by differences in conditional probabilities, derived using conditional Bayes’ rule [E4]. This formulation enables backpropagation through the retriever, allowing its parameters to be updated end-to-end alongside the language model [E4]. In an idealized case where a single perfect document is retrieved, the gradient simplifies to standard supervised learning on that "gold" document [E4].

Thus, REALM’s retrieve-then-predict framework incorporates latent retrieval variables and supports gradient flow through the retriever component, facilitating joint optimization of retrieval and prediction [E4]. However, detailed procedural descriptions of how backpropagation is implemented through discrete retrieval steps are not included in the provided evidence.

### Metrics

- baseline_latency_seconds: 5.477
- orchestrator_latency_seconds: 60.773
- baseline_total_tokens: 2022
- orchestrator_total_tokens: 25588
- baseline_citation_count: 3
- orchestrator_evidence_count: 15
- fact_check_status_counts: {'supported': 7, 'unsupported': 2}

## Question 3

What evidence does the paper provide that REALM improves Open-domain Question Answering performance compared to methods like ORQA, and what are the key reasons for this improvement?

### Baseline Answer

The paper provides evidence that REALM improves Open-domain Question Answering (QA) performance by demonstrating results on the NaturalQuestions-Open dataset, including after ablating critical components of REALM. Importantly, the paper reports not only end-to-end QA results but also evaluates how often the gold answer appears in the top-5 retrieved documents before any fine-tuning. This specific metric isolates the contribution of an improved retriever during the pre-training phase, highlighting the key reason for REALM's performance gains: enhanced retrieval capabilities from pre-training the retriever end-to-end with the reader component.

This contrasts with prior methods like ORQA, implying that REALM's joint training of retriever and reader, and its pre-training strategy, lead to more relevant documents being retrieved early on, which subsequently improves the answer extraction and overall QA accuracy. Thus, the key reasons for improvement are the end-to-end training approach and improved retrieval precision during pre-training, as evidenced by the higher frequency of gold answers appearing in early top-k retrievals even before fine-tuning [1][2][3].

Citations:  
[1] data/2002.08909v1.pdf, chunk_id: 2002.08909v1-2444-af66052c100f86e99778527e  
[2] data/2002.08909v1.pdf, chunk_id: 2002.08909v1-2445-2d2fda09148bafc8f9d92bd8  
[3] data/2002.08909v1.pdf, chunk_id: 2002.08909v1-2446-41ffd4fc5e72f3639367551d

### Multi-Agent Answer

The paper provides evidence that REALM improves Open-domain Question Answering (QA) performance by presenting results on the NaturalQuestions-Open dataset after ablating critical components of the REALM model [E1][E2][E3][E4][E5]. It reports both end-to-end QA results as well as the frequency with which the gold answer appears in the top-5 retrieved passages before any fine-tuning is applied [E1][E2][E3][E4][E5]. This top-5 retrieval metric prior to fine-tuning is used to isolate the retriever component’s contribution to performance improvements, highlighting that enhancements in the retriever during pre-training are key to the observed gains [E1][E2][E3][E4][E5].

However, the evidence does not provide specific information about comparisons to methods like ORQA or quantitative performance differences relative to such baselines [E1][E2][E3][E4][E5]. Consequently, claims regarding REALM’s improvement over ORQA or other methods, as well as the precise reasons for such improvement beyond retriever pre-training effectiveness, are not supported by the provided evidence.

### Metrics

- baseline_latency_seconds: 5.235
- orchestrator_latency_seconds: 42.098
- baseline_total_tokens: 944
- orchestrator_total_tokens: 14595
- baseline_citation_count: 3
- orchestrator_evidence_count: 8
- fact_check_status_counts: {'supported': 3, 'unsupported': 2}
