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

REALM, which stands for Retrieval-Augmented Language Model, is a framework that enhances language model pre-training by integrating a learned textual knowledge retriever. Unlike traditional language models like BERT that store knowledge implicitly within their model parameters, REALM explicitly separates the storage and retrieval of knowledge. It achieves this by incorporating a component that actively retrieves world knowledge from an external textual knowledge base during pre-training, rather than relying solely on stored parameters. This approach makes the role of world knowledge more explicit in the model's operation and potentially allows for more effective use and updating of knowledge compared to models that embed knowledge only within their weights [1][2][3].

Citations:  
[1][2][3] data/2002.08909v1.pdf

### Multi-Agent Answer

REALM (Retrieval-Augmented Language Model) is a pre-training framework that enhances language model training by integrating a learned textual knowledge retriever. Unlike traditional language models that store knowledge implicitly and solely within their fixed model parameters, REALM explicitly incorporates a retrieval mechanism that enables the model to dynamically fetch relevant textual information from external sources during pre-training. This design explicitly exposes and utilizes world knowledge rather than embedding all information within the model itself [E4][E5][E6][E7][E8][E9].

In contrast to classical language models (e.g., those that embed knowledge only in parameters), REALM’s learned retriever component allows it to access and leverage external knowledge bases at inference time, thereby augmenting the language model with up-to-date or extensive information. This retrieval-augmented approach distinctly separates the storage of knowledge (external corpora) from the language model parameters, highlighting a fundamental architectural and functional difference [E4][E7][E8].

While the evidence notes repeatedly contrast REALM with models that embed knowledge solely in parameters, they do not explicitly name BERT or provide detailed quantitative comparisons between REALM and specific traditional models. Therefore, statements associating REALM’s differences directly with BERT are only weakly supported by the provided evidence [E4][E7][E8].

In summary, REALM differs from traditional parameter-only language models by explicitly incorporating a learned retrieval mechanism into pre-training, enabling dynamic access to external textual knowledge, which exposes and leverages world knowledge more transparently and effectively [E4][E5][E6][E7][E8][E9]. Specific quantitative performance details or exact mechanisms of the retriever are not provided in the evidence.

### Metrics

- baseline_latency_seconds: 4.581
- orchestrator_latency_seconds: 38.667
- baseline_total_tokens: 683
- orchestrator_total_tokens: 11554
- baseline_citation_count: 3
- orchestrator_evidence_count: 9
- fact_check_status_counts: {'weakly_supported': 4, 'supported': 2}

## Question 2

Explain how the retrieve-then-predict framework works in REALM, including the role of the latent variable z and backpropagation through the retriever.

### Baseline Answer

The retrieve-then-predict framework in REALM works by decomposing the conditional probability of an output \(y\) given an input \(x\), \(p(y|x)\), into two steps involving a latent variable \(z\) representing retrieved documents:

1. **Retrieval Step:** Given the input \(x\), the model first retrieves potentially relevant documents \(z\) from a large knowledge corpus \(Z\) by modeling a distribution \(p(z|x)\). This is done using a neural knowledge retriever that scores candidate documents with a relevance function \(f(x,z)\), defined as the inner product of dense vector embeddings of \(x\) and \(z\). These embeddings are produced by BERT-style Transformer models followed by dimensionality reduction via linear projection matrices:
   \[
   p(z|x) = \frac{\exp(f(x,z))}{\sum_{z'} \exp(f(x,z'))}, \quad f(x,z) = \text{Embed}_{\text{input}}(x)^\top \text{Embed}_{\text{doc}}(z),
   \]
   where \(\text{Embed}_{\text{input}}(x)\) and \(\text{Embed}_{\text{doc}}(z)\) map the input and document, respectively, to the same vector space [1].

2. **Prediction Step:** Conditioned on the retrieved document \(z\) and input \(x\), the model then predicts the output \(y\) through a knowledge-augmented encoder, modeling \(p(y|z,x)\).

3. **Marginalization Over Documents:** Since the retrieved document \(z\) is unknown during training and inference, it is treated as a latent variable. The overall likelihood is computed by marginalizing over all possible retrieved documents:
   \[
   p(y|x) = \sum_{z \in Z} p(y|z,x) p(z|x).
   \]

Regarding the **role of the latent variable \(z\)**, by marginalizing over \(z\), the model captures the uncertainty about which document is relevant for generating \(y\), integrating retrieval into end-to-end prediction rather than treating retrieval and prediction as separate stages [1].

For **backpropagation through the retriever**, REALM performs joint optimization of both the retriever and the reader components by maximizing the likelihood of the generative process including the retrieval distribution. This requires propagating gradients through the retrieval distribution \(p(z|

### Multi-Agent Answer

The retrieve-then-predict framework in REALM works by augmenting language model pre-training with a learned textual knowledge retriever. Rather than storing all world knowledge solely within the model’s parameters, REALM explicitly queries an external corpus of text documents to retrieve relevant information conditional on the input, thereby explicitly exposing the role of world knowledge in prediction [E1], [E2], [E3].

In this framework, the latent variable \( z \) represents a retrieved knowledge document conditioned on the input \( x \). The model then computes predictions \( y \) based on both \( x \) and the retrieved document \( z \), integrating the retrieved external knowledge to improve prediction accuracy [E4], [E6].

During training, the objective’s gradient is derived with respect to both the language model parameters and the retriever parameters. This involves applying Bayes’ rule and marginalizing over the latent retrieval variable \( z \), which allows the gradient to flow through the retriever based on how useful each retrieved document is for predicting the output \( y \). Consequently, the retriever is directly improved through backpropagation as the model learns to favor documents that increase the likelihood of the correct prediction [E4].

Moreover, when a single “gold” document \( z \) perfectly predicts the target \( y \), the training objective simplifies to maximizing the likelihood of that document alone, making REALM’s training equivalent to supervised maximum likelihood training on that document [E4].

In summary, REALM’s retrieve-then-predict approach explicitly models retrieval as a latent variable and enables end-to-end learning by backpropagating through the retriever, improving both retrieval and prediction jointly [E1], [E2], [E3], [E4], [E6]. 

The provided evidence sufficiently explains the mechanism, the role of \( z \), and the backpropagation through the retriever. However, details on specific algorithmic implementation or quantitative results about backpropagation dynamics are not included in the extracts.

### Metrics

- baseline_latency_seconds: 6.777
- orchestrator_latency_seconds: 41.989
- baseline_total_tokens: 2022
- orchestrator_total_tokens: 15701
- baseline_citation_count: 3
- orchestrator_evidence_count: 9
- fact_check_status_counts: {'weakly_supported': 7, 'supported': 5}

## Question 3

What evidence does the paper provide that REALM improves Open-domain Question Answering performance compared to methods like ORQA, and what are the key reasons for this improvement?

### Baseline Answer

The paper provides evidence that REALM improves Open-domain Question Answering (QA) performance by presenting results on the NaturalQuestions-Open dataset, where critical components of REALM are ablated to evaluate their impact. The authors report not only the end-to-end QA results but also how frequently the gold answer appears among the top-5 retrievals before any fine-tuning is applied. This additional metric helps to isolate the contribution of the retrieval component during pre-training, demonstrating that REALM achieves better retrieval accuracy compared to previous methods like ORQA. The improved retriever pre-training in REALM is cited as a key reason for enhanced performance in Open-domain QA.

Thus, the paper argues that the key reason REALM outperforms ORQA in Open-domain QA is its improved retriever training, which leads to more accurate retrieval of relevant passages containing the answer before fine-tuning [1][2][3].

Citations:  
[1][2][3] - data/2002.08909v1.pdf (chunks 2444.0, 2445.0, 2446.0)

### Multi-Agent Answer

The paper provides evidence that REALM improves Open-domain Question Answering (QA) performance primarily by enhancing the effectiveness of the retriever component during pre-training. This is demonstrated through experiments on the NaturalQuestions-Open dataset, where the authors conduct ablation studies removing critical components of REALM to isolate their individual impacts [E1][E2][E3][E5][E6].

Specifically, the paper reports end-to-end QA results alongside a key metric: how often the gold answer appears in the top-5 retrieved documents before any fine-tuning is applied. Measuring this metric prior to fine-tuning serves as a more direct and isolated evaluation of the retriever’s capability, separating it from subsequent refinements introduced during the reader fine-tuning process [E1][E2][E3][E4][E5][E6].

The main reason attributed to REALM’s improvement is its pre-training approach, which focuses on improving the retriever’s ability to retrieve relevant documents containing the gold answers. While the evidence clearly supports the importance of retriever pre-training in enhancing retrieval performance, direct details or quantitative comparisons specifically contrasting REALM with methods like ORQA—especially regarding joint training of retriever and reader or other architectural distinctions—are not provided in the available evidence. Therefore, claims about improvements relative to ORQA or the exact mechanisms behind REALM’s gains should be considered weakly supported due to insufficient direct evidence [E1–E6].

In summary, the paper demonstrates that REALM’s improved open-domain QA performance stems from better retriever effectiveness isolated by the gold answer frequency in the top-5 retrievals before fine-tuning, attributing improvements mainly to enhanced retriever pre-training. However, explicit evidence comparing REALM’s performance to ORQA or clarifying all key reasons for the improvement is missing from the provided context.

### Metrics

- baseline_latency_seconds: 3.223
- orchestrator_latency_seconds: 30.274
- baseline_total_tokens: 816
- orchestrator_total_tokens: 9649
- baseline_citation_count: 3
- orchestrator_evidence_count: 6
- fact_check_status_counts: {'weakly_supported': 9, 'supported': 1}
