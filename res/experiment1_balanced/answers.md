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

REALM, which stands for Retrieval-Augmented Language Model, is a novel framework that enhances language model pre-training by incorporating a learned textual knowledge retriever. Unlike traditional language models like BERT, which store knowledge implicitly within their model parameters, REALM explicitly integrates world knowledge by enabling the model to retrieve relevant information from an external knowledge source during training and inference. This design makes the role of world knowledge explicit rather than embedding it solely inside the model parameters as in traditional approaches [1][2][3][4][5].

Citations:  
[1][2][3][4][5] - data/2002.08909v1.pdf chunks 73.0 to 75.0

### Multi-Agent Answer

REALM (Retrieval-Augmented Language Model) is a language model pre-training approach that integrates a learned textual knowledge retriever into the model’s architecture [E1][E2][E3]. Unlike traditional language models like BERT, which store world knowledge implicitly within their neural network parameters, REALM explicitly incorporates external knowledge by retrieving and attending to relevant documents from a large corpus such as Wikipedia during pre-training, fine-tuning, and inference [E9][E11][E12]. This retrieval mechanism allows REALM to condition its predictions on retrieved text, making knowledge storage more modular and interpretable rather than embedding all information in fixed parameters [E9].

For example, when predicting a masked token, REALM assigns a significantly higher probability to the correct answer by using retrieved documents containing relevant facts—REALM’s conditional probability given a relevant document can be as high as 1.0 compared to an extremely low probability of 1.1 × 10⁻¹⁴ assigned by BERT without retrieval [E11]. Moreover, REALM’s latent knowledge retriever is pre-trained in an unsupervised manner using masked language modeling, jointly optimizing the retrieval and encoding components, which contrasts with traditional models that do not explicitly separate these parts [E9][E11].

### Metrics

- baseline_latency_seconds: 3.595
- orchestrator_latency_seconds: 55.545
- baseline_total_tokens: 932
- orchestrator_total_tokens: 25300
- baseline_citation_count: 5
- orchestrator_evidence_count: 15
- fact_check_status_counts: {'supported': 7}

## Question 2

Explain how the retrieve-then-predict framework works in REALM, including the role of the latent variable z and backpropagation through the retriever.

### Baseline Answer

The retrieve-then-predict framework in REALM works by decomposing the overall probability of generating an output \( y \) given an input \( x \) into two steps: first retrieving relevant documents \( z \) from a large corpus \( Z \), then predicting \( y \) conditioned on both \( x \) and \( z \). In this framework, \( z \) is treated as a latent variable representing the retrieved documents that might be useful for prediction. Formally, the model marginalizes over all possible documents:

\[
p(y|x) = \sum_{z \in Z} p(y|z,x) p(z|x)
\]

where \( p(z|x) \) is the distribution over documents given input \( x \), and \( p(y|z,x) \) is the distribution of the output given the input and retrieved documents [1].

The retrieval component \( p(z|x) \) is modeled using a dense inner product between learned embeddings of the input \( x \) and each document \( z \): 

\[
p(z|x) = \frac{\exp f(x,z)}{\sum_{z'} \exp f(x,z')}
\]

with

\[
f(x,z) = \text{Embed}_{input}(x)^\top \text{Embed}_{doc}(z)
\]

where the embedding functions are implemented with BERT-style Transformers followed by projection matrices, mapping \( x \) and \( z \) to vector representations [1].

The latent variable \( z \) plays a critical role in allowing the model to reason over which documents are relevant without explicit supervision on the retrieval step. By marginalizing over \( z \), the model softly considers all documents weighted by their relevance scores when predicting \( y \).

Regarding training and backpropagation: the gradient of the log-likelihood objective with respect to parameters \( \theta \) of the retriever involves an expectation over \( z \):

\[
\nabla \log p(y|x) = \sum_{z \in Z} r(z) \nabla f(x,z)
\]

where

\[
r(z) = \left[\frac{p(y|z,x)}{p(y|x)} - 1\right] p(z|x).
\]

This means the retriever receives a positive update for documents \( z \) when they lead to better-than-expected prediction performance \( p(y|z,x) > p(y|x) \), reinforcing their

### Multi-Agent Answer

The REALM (Retrieval-Augmented Language Model) framework employs a retrieve-then-predict generative process in which the model first retrieves relevant documents \( z \) from a large textual knowledge corpus \( Z \) given an input \( x \), and then predicts the output \( y \) conditioned on both \( x \) and the retrieved documents \( z \) [E9]. This process is formalized by marginalizing over all possible retrieved documents as \( p(y|x) = \sum_{z \in Z} p(y|z,x) p(z|x) \) [E9]. In this framework, \( z \) acts as a latent variable representing the relevant world knowledge retrieved to help predict \( y \) [E9][E6].

The knowledge retriever models the distribution \( p(z|x) \) using a learned dense embedding mechanism, where embeddings for the input \( x \) and candidate documents \( z \) are computed through BERT-style Transformer encoders [E9]. The retrieval probabilities are then derived from a softmax over the inner product of these embeddings [E9]. The knowledge-augmented encoder predicts \( y \) conditioned on \( x \) and the retrieved \( z \), modeling \( p(y|z,x) \) [E9].

Importantly, REALM allows backpropagation of gradients through the retriever by deriving the gradient of the likelihood objective with respect to the retriever parameters. This is done by treating \( z \) as a latent variable and marginalizing over it, enabling the training signal to flow through the retrieval step [E6]. Specifically, the gradient of the log-likelihood is expressed as an expectation over \( z \) weighted by their posterior probabilities, which connects to supervised learning when a single document \( z^* \) perfectly predicts the target \( y \) [E6]. This formulation allows REALM to update both the retriever and the encoder jointly during pre-training, thus improving retrieval quality and downstream prediction [E6][E10].

In summary, REALM’s retrieve-then-predict framework decomposes prediction into retrieval of documents \( z \) as latent variables and prediction conditioned on those documents, with gradient-based end-to-end training enabling backpropagation through the retriever to optimize retrieval jointly with language understanding [E9][E6][E10].

### Metrics

- baseline_latency_seconds: 5.602
- orchestrator_latency_seconds: 76.317
- baseline_total_tokens: 3153
- orchestrator_total_tokens: 42076
- baseline_citation_count: 5
- orchestrator_evidence_count: 20
- fact_check_status_counts: {'supported': 8, 'unsupported': 3}

## Question 3

What evidence does the paper provide that REALM improves Open-domain Question Answering performance compared to methods like ORQA, and what are the key reasons for this improvement?

### Baseline Answer

The paper provides evidence that REALM improves Open-domain Question Answering (QA) performance by demonstrating results on the NaturalQuestions-Open dataset after ablating critical components of REALM. Specifically, the paper reports both end-to-end performance and the frequency with which the gold answer appears in the top-5 retrievals before any fine-tuning. This latter metric isolates the contribution of pre-training the retriever component, showing that improving the retriever during pre-training leads to better retrieval of relevant documents, which in turn enhances the QA performance. This indicates that a key reason for REALM's improvement over methods like ORQA is its ability to better train the retriever component in an end-to-end fashion prior to fine-tuning, resulting in improved retrieval quality that supports more accurate question answering [1][2][3][4][5].

Citations:  
[1][2][3][4][5] — data/2002.08909v1.pdf chunks 2444.0 to 2448.0

### Multi-Agent Answer

The paper provides evidence that REALM improves Open-domain Question Answering (QA) performance by presenting results on the NaturalQuestions-Open dataset after ablating critical components of the REALM model [E1][E2][E3][E4][E5]. A key metric reported is the frequency with which the gold answer appears in the top-5 retrieved documents before applying any fine-tuning [E1][E2][E3][E4][E5][E6]. This metric is used to more significantly isolate the contribution of the retriever’s improvement obtained during pre-training from the overall end-to-end QA performance [E2][E3][E4][E5][E6]. By analyzing how often the gold answer is present in these top-5 retrievals prior to fine-tuning, the study clearly identifies the impact of the learned retriever component in REALM [E1][E2][E3]. However, the evidence does not explicitly quantify how much this retriever improvement contributes to the overall QA performance or directly state the effectiveness of the retriever beyond this metric, so conclusions about the magnitude of improvement should be drawn cautiously [E4].

### Metrics

- baseline_latency_seconds: 3.373
- orchestrator_latency_seconds: 51.095
- baseline_total_tokens: 1084
- orchestrator_total_tokens: 18655
- baseline_citation_count: 5
- orchestrator_evidence_count: 14
- fact_check_status_counts: {'supported': 5}
