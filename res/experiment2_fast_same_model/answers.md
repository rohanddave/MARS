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

REALM (Retrieval-Augmented Language Model) is a novel framework that enhances traditional language model pre-training by incorporating a learned textual knowledge retriever. Unlike models such as BERT, which store knowledge implicitly within their model parameters, REALM explicitly exposes the role of world knowledge by actively retrieving relevant information during processing rather than relying solely on stored parameters. This means REALM accesses external knowledge dynamically through retrieval, whereas traditional models depend on fixed internalized knowledge encoded during training [1][2][3].

Citations:  
[1] data/2002.08909v1.pdf, chunk 73  
[2] data/2002.08909v1.pdf, chunk 92  
[3] data/2002.08909v1.pdf, chunk 85

### Multi-Agent Answer

REALM is a novel framework called Retrieval-Augmented Language Model pre-training that enhances language model training by integrating a learned textual knowledge retriever [E1][E3]. Unlike traditional language models that store knowledge solely within their model parameters, REALM explicitly exposes and incorporates world knowledge by querying an external textual retriever during pre-training [E2][E4]. This means that instead of embedding all information directly inside the model weights, REALM asks the model to retrieve relevant textual information from an external source, thereby explicitly using world knowledge as part of its function [E5][E6][E7].

### Metrics

- baseline_latency_seconds: 2.602
- orchestrator_latency_seconds: 27.351
- baseline_total_tokens: 689
- orchestrator_total_tokens: 9700
- baseline_citation_count: 3
- orchestrator_evidence_count: 7
- fact_check_status_counts: {'supported': 3}

## Question 2

Explain how the retrieve-then-predict framework works in REALM, including the role of the latent variable z and backpropagation through the retriever.

### Baseline Answer

The retrieve-then-predict framework in REALM operates by first retrieving relevant documents from a large textual knowledge corpus \( Z \) given an input \( x \), and then predicting the output \( y \) based on both the input and the retrieved documents. Specifically, REALM models the likelihood \( p(y|x) \) by introducing a latent variable \( z \) representing a retrieved document from \( Z \). The process decomposes as follows:

1. **Retrieval step**: Sample a document \( z \) from the distribution \( p(z|x) \), which represents the probability of \( z \) being relevant to the input \( x \).

2. **Prediction step**: Condition on the retrieved document \( z \) and input \( x \) to generate the output \( y \), modeled as \( p(y|z,x) \).

The overall likelihood of generating \( y \) given \( x \) is obtained by marginalizing over all possible documents \( z \):

\[
p(y|x) = \sum_{z \in Z} p(y|z,x) p(z|x).
\]

Here, the latent variable \( z \) serves a crucial role for retrieval—it represents the documents that potentially contain the answer or information necessary to predict \( y \). By treating \( z \) as latent, REALM jointly learns to retrieve relevant documents and to predict the output conditioned on those documents, rather than relying solely on fixed stored knowledge in the model parameters.

Regarding the retriever, REALM uses a neural knowledge retriever modeled via dense vector embeddings. The probability \( p(z|x) \) is defined as a softmax over relevance scores computed by the inner product of learned embeddings for the input and documents:

\[
p(z|x) = \frac{\exp f(x,z)}{\sum_{z'} \exp f(x,z')},
\]
where
\[
f(x,z) = \text{Embed}_{\text{input}}(x)^\top \text{Embed}_{\text{doc}}(z).
\]

Both \( \text{Embed}_{\text{input}} \) and \( \text{Embed}_{\text{doc}} \) are learned embedding functions implemented with BERT-style Transformers whose outputs are then projected to lower-dimensional vectors [1].

Crucially, REALM enables **backpropagation through the retriever** by treating the retrieval as a differentiable latent variable model. Since \( z \) is latent

### Multi-Agent Answer

The retrieve-then-predict framework in REALM operates by augmenting language model pre-training with a learned textual knowledge retriever [E1][E2]. Unlike traditional language models that embed knowledge entirely within their parameters, REALM explicitly involves the model in retrieving relevant textual information from an external corpus during training, thereby exposing the role of world knowledge [E1][E3]. 

In this framework, the latent variable \( z \) represents the retrieved textual document(s) conditioned on the input \( x \). The model treats \( z \) as a latent variable to be inferred, reflecting which document is most relevant for predicting the output \( y \) given the input \( x \) [E4]. REALM models the probability \( p(y|x) \) by marginalizing over \( z \), i.e., \( p(y|x) = \sum_z p(y|z, x) p(z|x) \), where \( p(z|x) \) is the learned retriever distribution that selects relevant documents [E4].

Backpropagation through the retriever is enabled by a gradient derivation of the REALM objective with respect to the retriever parameters. This gradient allows end-to-end training of the retriever by connecting the predicted output likelihood with the retrieval probabilities, effectively updating the retriever based on downstream task performance [E4].

### Metrics

- baseline_latency_seconds: 7.697
- orchestrator_latency_seconds: 67.111
- baseline_total_tokens: 2022
- orchestrator_total_tokens: 26413
- baseline_citation_count: 3
- orchestrator_evidence_count: 17
- fact_check_status_counts: {'supported': 7, 'unsupported': 1}

## Question 3

What evidence does the paper provide that REALM improves Open-domain Question Answering performance compared to methods like ORQA, and what are the key reasons for this improvement?

### Baseline Answer

The paper provides evidence that REALM improves Open-domain Question Answering (QA) performance by presenting results on the NaturalQuestions-Open dataset. It reports both end-to-end results and retrieval performance specifically measuring the frequency at which the gold answer appears among the top-5 retrievals before any fine-tuning. This latter metric importantly highlights how the retrieval component of REALM improves during pre-training, thus contributing significantly to overall QA performance improvements compared to previous methods like ORQA. The ablation studies removing critical components of REALM further support understanding the contribution of each part. This suggests that better retriever pre-training is a key reason for REALM's improvement in Open-domain QA [1][2][3].

Citations:  
[1][2][3] data/2002.08909v1.pdf (chunks 2444, 2445, 2446)

### Multi-Agent Answer

The paper provides evidence that REALM’s improvements in Open-domain Question Answering (QA) performance are closely linked to enhancements in the retriever component during pre-training [E1][E2]. Specifically, the study presents results on the NaturalQuestions-Open dataset after ablating critical components of REALM to analyze their impact [E1][E2]. A key metric reported is the frequency with which the gold answer appears in the top-5 retrieved documents before any fine-tuning; this metric is used to isolate the contribution of retriever improvements independently of downstream fine-tuning [E1][E3]. By focusing on this retrieval metric prior to fine-tuning, the paper highlights that better retrieval quality achieved during pre-training significantly contributes to the model’s overall QA performance [E4][E5].

However, the provided evidence does not include explicit quantitative comparisons demonstrating that REALM outperforms other methods such as ORQA, nor does it provide detailed causal explanations for the improvements beyond the emphasis on retrieval enhancement [E1][E4]. Therefore, while retrieval improvement is clearly emphasized as a key reason for REALM’s QA gains, direct comparative evidence against ORQA and attribution of improvements to other components are not presented in the available sources [E1][E4].

### Metrics

- baseline_latency_seconds: 2.626
- orchestrator_latency_seconds: 49.647
- baseline_total_tokens: 769
- orchestrator_total_tokens: 16464
- baseline_citation_count: 3
- orchestrator_evidence_count: 8
- fact_check_status_counts: {'unsupported': 3, 'supported': 3}
