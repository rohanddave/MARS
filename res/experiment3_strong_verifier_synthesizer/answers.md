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

REALM (Retrieval-Augmented Language Model) is a novel framework for language model pre-training that integrates a learned textual knowledge retriever into the process. Unlike traditional language models like BERT that store knowledge implicitly within their model parameters, REALM explicitly exposes and utilizes world knowledge by retrieving relevant textual information during inference. This augmentation enables REALM to access external knowledge dynamically rather than relying solely on the static knowledge encoded within its parameters [1][2][3][4][5][6][7][8].

Citations:  
[1][2][3][4][5][6][7][8] data/2002.08909v1.pdf

### Multi-Agent Answer

REALM (Retrieval-Augmented Language Model) is a language model pre-training framework that enhances traditional language model training by incorporating a learned textual knowledge retriever [E1][E2][E3][E4][E5]. Unlike traditional models such as BERT, which store knowledge implicitly within their model parameters, REALM explicitly exposes and utilizes world knowledge during training by querying and retrieving relevant external textual information [E6][E7][E8][E9][E10][E11][E12]. This retrieval mechanism enables REALM to condition its predictions not only on the input text but also on documents retrieved from a large external corpus, thereby extending language modeling beyond the fixed parameters of the model [E24]. For example, REALM can assign a significantly higher probability to a correct masked token when conditioned on retrieved documents compared to BERT, which does not use retrieval; in one instance, REALM assigned a probability of 1.0 to the correct token “Fermat” given the retrieved document, whereas BERT’s probability without retrieval was about \(1.1 \times 10^{-14}\) [E24]. In summary, the key difference between REALM and traditional language models like BERT lies in knowledge storage and retrieval: REALM integrates an explicit, learned retrieval component that accesses world knowledge as needed during training and inference, rather than relying solely on knowledge implicitly stored in model parameters [E1][E2][E3][E4][E5][E6][E7][E8][E9][E10][E11][E12].

### Metrics

- baseline_latency_seconds: 2.146
- orchestrator_latency_seconds: 76.975
- baseline_total_tokens: 1290
- orchestrator_total_tokens: 34239
- baseline_citation_count: 8
- orchestrator_evidence_count: 27
- fact_check_status_counts: {'supported': 5}

## Question 2

Explain how the retrieve-then-predict framework works in REALM, including the role of the latent variable z and backpropagation through the retriever.

### Baseline Answer

The retrieve-then-predict framework in REALM works as a two-step generative process where, given an input \( x \), the model first retrieves potentially relevant documents \( z \) from a large textual knowledge corpus \( Z \), and then predicts the output \( y \) conditioned on both \( x \) and the retrieved documents \( z \).

Specifically, REALM models the likelihood \( p(y|x) \) of generating an output \( y \) given the input \( x \) by treating \( z \) (the retrieved documents) as a latent variable. It marginalizes over \( z \) to capture the uncertainty in retrieval:

\[
p(y|x) = \sum_{z \in Z} p(y|z, x) \, p(z|x)
\]

Here, \( p(z|x) \) is the retrieval distribution over the corpus \( Z \), which gives the probability of retrieving document \( z \) given input \( x \), and \( p(y|z, x) \) is the prediction distribution that generates output \( y \) conditioned on \( x \) and \( z \) [1].

The latent variable \( z \) thus represents the document(s) retrieved from the knowledge corpus to help in predicting the output. By considering \( z \) as latent, REALM enables the model to learn to retrieve helpful documents even when the relevant knowledge is not explicitly given.

The retriever, which models \( p(z|x) \), is implemented by encoding both the input \( x \) and each document \( z \) into dense vector embeddings using BERT-style Transformers. The relevance score \( f(x, z) \) is computed as the inner product between these embeddings:

\[
f(x, z) = \text{Embed}_{\text{input}}(x)^\top \, \text{Embed}_{\text{doc}}(z)
\]

The retrieval distribution is a softmax over these relevance scores across all documents \( z \) in \( Z \):

\[
p(z|x) = \frac{\exp(f(x,z))}{\sum_{z'} \exp(f(x,z'))}
\]

The embedding functions \( \text{Embed}_{\text{input}} \) and \( \text{Embed}_{\text{doc}} \) map the input and documents respectively into vectors via BERT and linear projections [1].

Regarding backpropagation through the retriever, REALM optimizes

### Multi-Agent Answer

The retrieve-then-predict framework in REALM operates by first retrieving relevant textual knowledge from an external corpus before making predictions, thereby explicitly incorporating world knowledge into language model pre-training [E1][E2][E3][E4][E5][E6][E7][E8][E10][E14][E15][E16][E18][E19][E20][E21].  

In this framework, the latent variable \( z \) represents the retrieved document from the knowledge corpus that is relevant to the input \( x \) [E12]. The retrieval component models a distribution \( p(z|x) \), which is computed based on dense embeddings of the question \( x \) and documents \( z \). These embeddings are typically generated using BERT-style Transformer models followed by a learned projection matrix to reduce embedding dimensionality [E12].  

Following retrieval, the prediction component models \( p(y|z, x) \), generating the output \( y \) conditioned on both the input \( x \) and the retrieved document \( z \) [E12]. Training REALM involves marginalizing over the latent retrieved documents \( z \), accounting for multiple possible retrievals to compute the overall likelihood of the output [E12].  

Regarding backpropagation through the retriever, the REALM paper derives the gradient of the pre-training objective with respect to the retriever parameters, enabling end-to-end learning of the retrieval module. This gradient computation involves summations over documents \( z \) weighted by their retrieval probabilities \( p(z|x) \) and their contribution to the correct prediction \( p(y|z, x) \). Under assumptions such as the existence of a gold document \( z^* \) that perfectly predicts the output, the gradient reduces to supervised learning of the retriever on that document [E9]. This end-to-end optimization allows the retriever to improve through feedback from the prediction task, rather than being fixed or trained separately.  

In summary, REALM’s retrieve-then-predict framework uses \( z \) as a latent variable representing retrieved documents; these are selected by a learned retriever modeled by \( p(z|x) \) based on dense embeddings. The prediction \( p(y|z, x) \) is conditioned on both \( x \) and \( z \), and training marginalizes over \( z \). Crucially, backpropagation is propagated through the retriever by deriving gradients of the overall objective with respect to retriever parameters

### Metrics

- baseline_latency_seconds: 6.406
- orchestrator_latency_seconds: 91.652
- baseline_total_tokens: 3548
- orchestrator_total_tokens: 51922
- baseline_citation_count: 8
- orchestrator_evidence_count: 25
- fact_check_status_counts: {'supported': 9, 'unsupported': 1}

## Question 3

What evidence does the paper provide that REALM improves Open-domain Question Answering performance compared to methods like ORQA, and what are the key reasons for this improvement?

### Baseline Answer

The paper provides evidence that REALM improves Open-domain Question Answering (OpenQA) performance by showing the results on the NaturalQuestions-Open dataset after ablating critical components of REALM. It reports both end-to-end results and the frequency with which the gold answer appears in the top-5 retrieved documents before any fine-tuning is applied. This latter metric isolates the contribution of improving the retriever during pre-training, underscoring that REALM's retriever enhancement is a key factor in performance improvement. By enhancing the retriever with pre-training, REALM achieves better retrieval of relevant documents containing the answer, which leads to superior OpenQA performance compared to methods like ORQA that may not pre-train their retriever as effectively [1][2][3][4][5][6][7][8].

The key reasons for this improvement are:

1. Pre-training the retriever within an end-to-end differentiable model framework, which improves retrieval quality.
2. Ablation studies that demonstrate how critical components of REALM contribute to this improvement.
3. Showing that better retrieval of relevant documents before fine-tuning leads to higher chances of finding the correct answer, thereby improving downstream QA performance.

Citations:
[1] – [8]: data/2002.08909v1.pdf (sections 2443.0 to 2450.0)

### Multi-Agent Answer

The paper provides evidence that REALM improves Open-domain Question Answering (QA) performance by presenting results on the NaturalQuestions-Open dataset after ablating critical components of the REALM model [E1][E2][E3][E4][E5][E6][E7][E8][E9][E10]. In particular, the study reports the frequency with which the gold answer appears in the top-5 retrievals prior to any fine-tuning [E1][E2][E3][E4][E5][E6][E7][E8][E9][E10]. This metric helps isolate the contribution of improvements in the retriever component made during pre-training, separate from the end-to-end model performance [E1][E2][E3][E4][E5][E6][E7][E8][E9][E10]. However, while the study emphasizes that measuring the gold answer presence in top-5 retrievals isolates the retriever’s contribution during pre-training, the evidence notes do not provide detailed quantitative comparisons or explicit claims demonstrating that the enhanced retriever is the key reason for overall performance gains relative to methods like ORQA. Therefore, specific evidence supporting the magnitude or exact nature of improvement over ORQA and the detailed reasons for this improvement beyond retriever enhancement is missing from the provided evidence [E1–E10].

### Metrics

- baseline_latency_seconds: 3.340
- orchestrator_latency_seconds: 65.732
- baseline_total_tokens: 1591
- orchestrator_total_tokens: 25035
- baseline_citation_count: 8
- orchestrator_evidence_count: 19
- fact_check_status_counts: {'supported': 4, 'unsupported': 2}
