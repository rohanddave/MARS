# experiment1: balanced multi-agent config

## Agent Configuration

- top_k: 5
- orchestrator_model: gpt-4.1-mini
- search_model: gpt-4.1-mini
- summarization_model: gpt-4.1-mini
- fact_check_model: gpt-4.1-mini
- final_synthesis_model: gpt-4.1-mini

## Question 1

What is REALM and how does it differ from traditional language models like BERT in terms of knowledge storage and retrieval?

### Baseline Answer

REALM (Retrieval-Augmented Language Model) is a novel framework that enhances language model pre-training algorithms by integrating a learned textual knowledge retriever. Unlike traditional language models like BERT that store knowledge implicitly within their parameters, REALM explicitly exposes and utilizes world knowledge by retrieving relevant textual information during processing rather than relying solely on internal parameter storage. This approach allows REALM to access and leverage external knowledge dynamically, which contrasts with the fixed knowledge encoded in the parameters of conventional models such as BERT[1][2][3][4][5].

Citations:  
[1][2][3][4][5] data/2002.08909v1.pdf, chunks 73.0, 74.0, 75.0, 85.0, 92.0

### Multi-Agent Answer

REALM (Retrieval-Augmented Language Model) is a language model pre-training method that enhances traditional language model training by incorporating a learned textual knowledge retriever [E1], [E2], [E3], [E4]. Unlike traditional language models that store knowledge implicitly and solely within their parameters, REALM explicitly incorporates world knowledge by prompting the model to retrieve relevant textual information from an external source during training [E5], [E6], [E7]. This approach differs fundamentally from models that embed knowledge only in their parameters by separating the storage of knowledge from the model parameters and instead involving a retrieval mechanism that accesses and uses external information, thereby explicitly exposing the role of world knowledge in the model’s predictions [E8], [E9], [E10].

The evidence notes do not explicitly mention BERT by name; therefore, any direct comparison to BERT specifically is not supported by the provided evidence.

### Metrics

- baseline_latency_seconds: 5.828
- orchestrator_latency_seconds: 48.983
- baseline_total_tokens: 952
- orchestrator_total_tokens: 21506
- baseline_citation_count: 5
- orchestrator_evidence_count: 20
- fact_check_status_counts: {'supported': 5}

## Question 2

Explain how the retrieve-then-predict framework works in REALM, including the role of the latent variable z and backpropagation through the retriever.

### Baseline Answer

REALM employs a retrieve-then-predict framework in which the overall goal is to model the probability of an output y given an input x, denoted as p(y|x). This is decomposed into two steps through a latent variable z, representing documents retrieved from a knowledge corpus Z:

1. **Retrieval Step**: Given the input x, the model samples documents z from a retrieval distribution p(z|x). This distribution is defined by a neural knowledge retriever that scores documents by a relevance function f(x,z), which is based on dense vector embeddings of the input and documents. Specifically, each input x and document z are embedded into vectors using BERT-based Transformers followed by a linear projection, and the relevance score is the inner product of these vectors. The retrieval distribution p(z|x) is then a softmax over all these relevance scores.

2. **Prediction Step**: Conditioning on both the input x and a retrieved document z, the model predicts the output y according to p(y|z,x).

The latent variable z is crucial because the final likelihood of generating y from x requires marginalizing over all possible retrieved documents z:

\[
p(y|x) = \sum_{z \in Z} p(y|z,x) p(z|x)
\]

This formulation treats retrieval as a probabilistic latent variable selection step, enabling the model to integrate knowledge retrieval explicitly during pre-training and fine-tuning (masked language modeling and open-domain QA tasks respectively) [1].

Regarding backpropagation through the retriever, the training objective maximizes the likelihood p(y|x) by updating the retriever's parameters θ through gradients that consider contributions from all possible documents z. The gradient of the log likelihood with respect to the retriever's parameters is:

\[
\nabla \log p(y|x) = \sum_{z \in Z} r(z) \nabla f(x,z)
\]

where

\[
r(z) = \left( \frac{p(y|z,x)}{p(y|x)} - 1 \right) p(z|x)
\]

This means that each document's score f(x,z) is adjusted positively if the document helps better predict y (i.e., if \(p(y|z, x)\) is greater than the expected \(p(y|x)\)) and negatively otherwise. This mechanism effectively backpropagates the prediction loss through the retrieval step, enabling the retriever to learn to identify documents that improve the prediction accuracy of y

### Multi-Agent Answer

The retrieve-then-predict framework in REALM operates by explicitly integrating a learned textual knowledge retriever into the language model pre-training process [E1][E2][E3][E4][E5][E7]. Unlike traditional models that store knowledge solely within their parameters, REALM exposes the role of world knowledge by requiring the model to retrieve relevant documents from a large text corpus before making predictions [E1][E9].

In this framework, the retrieval process is modeled as a latent variable \( z \), which represents the document retrieved from the corpus given an input query \( x \) [E9]. The overall generative likelihood for predicting an answer \( y \) is decomposed by marginalizing over this latent retrieval variable \( z \), formally expressed as:
\[
p(y|x) = \sum_z p(y|z, x) \, p(z|x)
\]
where \( p(z|x) \) denotes the retrieval distribution and \( p(y|z, x) \) is the prediction distribution conditioned on the retrieved document and the input query [E9].

The retrieval distribution \( p(z|x) \) is modeled by a neural knowledge retriever that computes relevance scores based on dense vector embeddings of both the input query and documents in the corpus. This is commonly implemented using BERT-style Transformer encoders followed by learned linear projection layers, and relevance is scored via an inner product between embedded query and document vectors [E9].

Regarding training, REALM treats the retrieval variable \( z \) as latent and learns to optimize the likelihood of correct predictions by marginalizing over possible retrieved documents. Through this latent variable modeling, the retriever parameters receive gradient signals derived from their impact on the final prediction \( p(y|x) \). This enables backpropagation through the retriever network, effectively integrating retrieval learning into end-to-end pre-training [E6][E10].

Specifically, the gradient of the REALM pre-training objective with respect to the retriever parameters is derived using conditional Bayes’ rule, and under ideal conditions (such as a perfect retrieval document existing), gradient descent on the REALM objective is equivalent to supervised maximum likelihood training [E6]. This approach allows REALM to learn which texts to retrieve that most improve masked token prediction and downstream tasks, thereby adapting both the retriever and the knowledge-augmented encoder jointly [E10].

In summary, REALM’s retrieve-then-predict framework models retrieval as a latent variable \( z \), marginalizes over

### Metrics

- baseline_latency_seconds: 5.056
- orchestrator_latency_seconds: 99.018
- baseline_total_tokens: 3153
- orchestrator_total_tokens: 46345
- baseline_citation_count: 5
- orchestrator_evidence_count: 23
- fact_check_status_counts: {'supported': 10, 'unsupported': 1}

## Question 3

What evidence does the paper provide that REALM improves Open-domain Question Answering performance compared to methods like ORQA, and what are the key reasons for this improvement?

### Baseline Answer

The paper provides evidence that REALM improves Open-domain Question Answering (QA) performance by presenting results on the NaturalQuestions-Open dataset after ablating critical components of REALM. These results include both end-to-end performance and a metric indicating how often the gold answer appears in the top-5 retrievals before any fine-tuning. This latter metric serves to isolate the contribution of improving the retriever during pre-training, suggesting that enhancements in retrieval quality before fine-tuning play a significant role in the overall performance gain of REALM compared to previous methods like ORQA [1][2][3][4][5].

The key reasons for this improvement stem from REALM's retrieval mechanism that is integrated and improved via end-to-end training, particularly focusing on the retriever's pre-training to better locate relevant documents. By effectively increasing the chances that the correct answer is found among the top retrieved documents even before fine-tuning, REALM's approach facilitates better downstream question answering accuracy.

Citations:  
[1][2][3][4][5] data/2002.08909v1.pdf (chunks 2444.0 to 2448.0)

### Multi-Agent Answer

The paper provides evidence that REALM improves Open-domain Question Answering (QA) performance by presenting results on the NaturalQuestions-Open dataset after ablating key components of the REALM model [E1][E2][E3][E4][E5]. A critical metric used in these experiments is how often the gold answer appears in the top-5 retrievals before applying any fine-tuning [E1][E2][E3][E4][E5]. This metric is specifically designed to isolate the contribution of retriever improvements made during pre-training from the overall end-to-end model performance, thereby highlighting the effect of enhancing the retrieval component [E1][E2][E3][E4][E5]. The findings indicate that improvements to the retriever during pre-training play a significant role in the model’s capacity to retrieve relevant passages containing the gold answer prior to fine-tuning [E1][E2][E3][E4][E5].

However, the evidence does not explicitly demonstrate that REALM’s retriever is more effective compared to methods like ORQA, nor does it provide detailed explanations beyond isolating the retriever’s contribution as the key reason for performance gains [E1][E2][E3][E4][E5]. Furthermore, precise quantitative comparisons between REALM and ORQA or similarly related approaches are not included in the available evidence [E1][E2][E3][E4][E5]. Therefore, while the paper shows that improvements in the retriever during pre-training significantly benefit REALM’s Open-domain QA performance, the provided evidence is insufficient to fully explain or quantify how and why REALM outperforms ORQA specifically.

### Metrics

- baseline_latency_seconds: 4.487
- orchestrator_latency_seconds: 51.094
- baseline_total_tokens: 1114
- orchestrator_total_tokens: 15364
- baseline_citation_count: 5
- orchestrator_evidence_count: 10
- fact_check_status_counts: {'supported': 5, 'unsupported': 2}
