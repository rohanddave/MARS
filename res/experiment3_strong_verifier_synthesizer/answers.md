# experiment3: strong verifier and synthesizer config

## Agent Configuration

- top_k: 8
- orchestrator_model: gpt-4.1-mini
- search_model: gpt-4.1-mini
- summarization_model: gpt-4.1-mini
- fact_check_model: gpt-4.1-mini
- final_synthesis_model: gpt-4.1-mini

## Question 1

What is REALM and how does it differ from traditional language models like BERT in terms of knowledge storage and retrieval?

### Baseline Answer

REALM, which stands for Retrieval-Augmented Language Model, is a novel framework in language model pre-training that augments traditional language models with a learned textual knowledge retriever. Unlike traditional models like BERT, which store knowledge implicitly within their parameters, REALM explicitly incorporates world knowledge by having the model retrieve relevant information from an external textual knowledge source during processing. This approach highlights the distinct role of world knowledge by not relying solely on the parameters of the model to store factual information, but rather by actively querying and retrieving knowledge as needed [1][2][3][4][5][6][7][8].

Citations:  
[1] data/2002.08909v1.pdf chunk_id: 2002.08909v1-73-c400c3c7dce704c45e999d16  
[2] data/2002.08909v1.pdf chunk_id: 2002.08909v1-92-006a44dd9d154f2cf726767d  
[3] data/2002.08909v1.pdf chunk_id: 2002.08909v1-85-e46d21d216aaf6bb414137f5  
[4] data/2002.08909v1.pdf chunk_id: 2002.08909v1-74-f80fa1f123d2843de2a120bb  
[5] data/2002.08909v1.pdf chunk_id: 2002.08909v1-75-b1af4fde93b942c4e78a5e8b  
[6] data/2002.08909v1.pdf chunk_id: 2002.08909v1-113-7be700bfe5ee2d36f33c1fda  
[7] data/2002.08909v1.pdf chunk_id: 2002.08909v1-114-a369a374ce16232eaff0c526  
[8] data/2002.08909v1.pdf chunk_id: 2002.08909v1-93-ee13a60af2042b149fa9a24b

### Multi-Agent Answer

REALM (Retrieval-Augmented Language Model) is a language model pre-training framework that improves standard language model training by integrating a learned textual knowledge retriever into the training process. This approach augments traditional language model pre-training algorithms by explicitly incorporating a retrieval mechanism that accesses relevant external textual information during training [E1–E30].

Unlike traditional language models such as BERT—which implicitly and solely store knowledge within their model parameters—REALM explicitly exposes and utilizes world knowledge by requiring the model to retrieve relevant external text. This retrieval-based approach makes the role of world knowledge more interpretable and modular during training, contrasting with conventional models that embed knowledge statically in their parameters [E1–E30]. Although BERT is not explicitly named in the evidence, it is representative of traditional parameter-embedded language models; therefore, the comparison to BERT is plausible but only weakly supported by name, while strongly supported conceptually [E1–E30].

This retrieval mechanism enables REALM to dynamically access and incorporate external knowledge, potentially allowing for up-to-date or more extensive information use, rather than depending entirely on static knowledge embedded at training time within model parameters. However, explicit evidence detailing how REALM handles up-to-date or extensive knowledge dynamically beyond exposing retrieval is limited, so this claim is weakly supported based on the provided documents [E1–E30].

In summary, REALM differs from traditional models by embedding an explicit learned knowledge retriever during pre-training, enabling the model to query and incorporate external textual knowledge dynamically, unlike models like BERT that store knowledge solely within their internal parameters [E1–E30].

### Metrics

- baseline_latency_seconds: 6.085
- orchestrator_latency_seconds: 74.094
- baseline_total_tokens: 1616
- orchestrator_total_tokens: 34071
- baseline_citation_count: 8
- orchestrator_evidence_count: 30
- fact_check_status_counts: {'weakly_supported': 7}

## Question 2

Explain how the retrieve-then-predict framework works in REALM, including the role of the latent variable z and backpropagation through the retriever.

### Baseline Answer

The retrieve-then-predict framework in REALM works by decomposing the conditional probability of predicting an output y given an input x, p(y|x), into two steps involving a latent retrieval variable z. Specifically, the model first retrieves potentially relevant documents z from a large knowledge corpus Z according to a learned retrieval distribution p(z|x), and then predicts the output y conditioned on both x and the retrieved documents as p(y|z,x). The overall likelihood is obtained by marginalizing over all possible documents z in the corpus, treating z as a latent variable:

\[
p(y|x) = \sum_{z \in Z} p(y|z, x) p(z|x).
\]

Here, z represents the documents retrieved from the knowledge corpus relevant to the input x (which might be a question in Open-QA or a masked sentence in pre-training) [1].

The retriever models p(z|x) using a learned dense embedding approach. Both the input query x and candidate documents z are embedded into a shared vector space via embedding functions (implemented with BERT-style Transformers followed by a linear projection). The relevance score f(x,z) is computed as the inner product of these embeddings, and p(z|x) is a softmax over these scores across all documents in Z:

\[
p(z|x) = \frac{\exp f(x,z)}{\sum_{z'} \exp f(x,z')}, \quad f(x,z) = \text{Embed}_{input}(x)^\top \text{Embed}_{doc}(z).
\]

The prediction model p(y|z,x) is a knowledge-augmented encoder conditioned on both x and the retrieved document z [1].

Regarding the latent variable z, it is crucial as it represents the unknown retrieved knowledge document needed to generate y. The model's training objective implicitly marginalizes over z, encouraging the retriever to find documents that improve the prediction accuracy.

Importantly, backpropagation is carried out through the retriever despite z being a latent variable. The gradient of the log-likelihood w.r.t retriever parameters θ involves an expectation over documents weighted by their posterior importance r(z):

\[
\nabla \log p(y|x) = \sum_{z \in Z} r(z) \nabla f(x,z),
\]
where
\[
r(z) = \left[ \frac{p(y|z,x)}{p(y|x)} - 1 \right] p(z|x).

### Multi-Agent Answer

The retrieve-then-predict framework in REALM (Retrieval-Augmented Language Model) operates by explicitly integrating a learned textual knowledge retriever into the language model pre-training process. Unlike traditional models that embed knowledge solely within their parameters, REALM requires the model to retrieve relevant textual knowledge from an external corpus during both training and inference, thus explicitly leveraging world knowledge rather than relying purely on parameterized memory [E1–E8, E10, E14, E15, E18, E19, E20, E21].

Concretely, the retrieval step models a distribution \( p(z|x) \) over documents \( z \) in a large knowledge corpus \( Z \) given an input \( x \) (e.g., a question or masked context). The prediction step then models \( p(y|z, x) \), the probability of the output \( y \) (such as a masked token or an answer) conditioned on the retrieved document \( z \) and the input \( x \). The document \( z \) serves as a latent variable; the overall output likelihood is computed by marginalizing over all possible documents:

\[
p(y|x) = \sum_{z} p(y|z, x) \, p(z|x).
\]

This formalization frames retrieval and prediction as a single generative process with a latent variable representing the retrieved document [E12].

REALM implements retrieval by encoding both the input \( x \) and each document \( z \) into dense embeddings using BERT-style Transformer encoders. The relevance function \( f(x, z) \) is defined as the inner product of the input and document embeddings:

\[
f(x,z) = \text{Embed}_{\text{input}}(x)^\top \text{Embed}_{\text{doc}}(z).
\]

These relevance scores are then normalized via a softmax over the entire corpus to form the retrieval distribution:

\[
p(z|x) = \frac{\exp f(x,z)}{\sum_{z'} \exp f(x,z')}.
\]

This approach allows REALM to perform learned, contextual retrieval that goes beyond simple lexical overlap, enabling the model to identify relevant documents based on semantic similarity [E12].

Furthermore, REALM’s training procedure enables backpropagation through the retriever by deriving gradient computations with respect to retriever parameters based on the expected posterior over retrieved documents. This is crucial for end-to-end learning of the retrieval component jointly with the

### Metrics

- baseline_latency_seconds: 5.645
- orchestrator_latency_seconds: 71.327
- baseline_total_tokens: 3548
- orchestrator_total_tokens: 34192
- baseline_citation_count: 8
- orchestrator_evidence_count: 22
- fact_check_status_counts: {'weakly_supported': 10, 'supported': 2}

## Question 3

What evidence does the paper provide that REALM improves Open-domain Question Answering performance compared to methods like ORQA, and what are the key reasons for this improvement?

### Baseline Answer

The provided context includes multiple instances of the same text fragment discussing results for NaturalQuestions-Open after ablating critical components of REALM. It mentions that the paper presents both end-to-end results and how often the gold answer appears in the top-5 retrievals before fine-tuning, emphasizing this latter metric isolates the impact of improving the retriever during pre-training [1][2][3][4][5][6][7][8].

However, the context does not provide any direct comparative results between REALM and other methods such as ORQA. It also does not specify quantitative evidence or the specific reasons why REALM improves Open-domain Question Answering (QA) performance over those methods.

Therefore, the key evidence, the exact performance comparison, and the reasons for improvement by REALM relative to ORQA or other retrieval methods are missing from the provided context.

### Missing information:
- Quantitative performance results comparing REALM and ORQA.
- Explanation or analysis of the reasons behind REALM's improvement.
- Details on the differences in retrieval or model architecture contributing to performance gains.

### Citations:
[1][2][3][4][5][6][7][8]: data/2002.08909v1.pdf, chunks 2443.0 to 2450.0

### Multi-Agent Answer

The paper provides evidence that REALM improves Open-domain Question Answering (QA) performance primarily by enhancing the retriever component through pre-training. This is demonstrated via results on the NaturalQuestions-Open dataset where critical components of REALM are ablated to analyze their impact. Both end-to-end system performance and retrieval-focused metrics are reported, specifically the frequency with which the gold (correct) answer appears in the top-5 retrieved documents before any fine-tuning is applied. This metric is emphasized as key to isolating the contribution of retriever improvements acquired during pre-training, separate from overall fine-tuned system results [E1][E2][E3][E4][E5][E6][E7][E8].

While the evidence consistently highlights the value of this retriever-focused metric, no specific numerical values or direct comparisons to other methods such as ORQA are provided in the available extracts. Therefore, although the paper suggests that REALM’s retriever is more effective at retrieving relevant documents containing the gold answer than prior approaches, the evidence to explicitly confirm this relative improvement over ORQA is missing or not detailed [E1–E8].

Key reasons for the observed improvement include REALM’s design that integrates an explicit retriever jointly pre-trained with the reader model, enabling better retrieval pre-training and thus more accurate identification of relevant evidence before answer extraction. The focus on pre-training the retriever and measuring retrieval quality before fine-tuning separates the retriever’s contribution from downstream fine-tuning effects, underscoring its critical role in enhanced QA performance [E1–E8].

In summary, the paper’s main evidence for REALM’s improvement over baseline methods lies in the isolation and evaluation of retriever effectiveness via top-5 gold answer retrieval frequency prior to fine-tuning, supported by ablation studies. However, explicit quantitative comparisons to ORQA or detailed numerical results are not present in the provided context, limiting the strength of conclusion about the magnitude of improvement relative to ORQA.

### Metrics

- baseline_latency_seconds: 4.292
- orchestrator_latency_seconds: 39.051
- baseline_total_tokens: 1577
- orchestrator_total_tokens: 12926
- baseline_citation_count: 8
- orchestrator_evidence_count: 8
- fact_check_status_counts: {'weakly_supported': 11, 'supported': 1}
