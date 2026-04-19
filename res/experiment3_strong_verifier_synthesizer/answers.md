# experiment3: strong verifier and synthesizer config

## Agent Configuration

- top_k: 8
- orchestrator_model: gpt-4.1-mini
- search_model: gpt-4.1-mini
- summarization_model: gpt-4.1-mini
- fact_check_model: gpt-4.1
- final_synthesis_model: gpt-4.1

## Question 1

What is REALM and how does it differ from traditional language models like BERT in terms of knowledge storage and retrieval?

### Baseline Answer

REALM, which stands for Retrieval-Augmented Language Model, is a novel framework that enhances language model pre-training algorithms by incorporating a learned textual knowledge retriever. Unlike traditional language models such as BERT that store knowledge implicitly in their model parameters, REALM explicitly handles world knowledge by leveraging an external retrieval mechanism during training and inference. This means that REALM does not rely solely on the fixed knowledge encoded within its parameters but actively retrieves relevant textual information from an external source to aid in knowledge utilization and reasoning tasks [1][2][3][4][5][6][7][8].

Citations:  
[1] data/2002.08909v1.pdf chunk 73.0  
[2] data/2002.08909v1.pdf chunk 92.0  
[3] data/2002.08909v1.pdf chunk 85.0  
[4] data/2002.08909v1.pdf chunk 74.0  
[5] data/2002.08909v1.pdf chunk 75.0  
[6] data/2002.08909v1.pdf chunk 113.0  
[7] data/2002.08909v1.pdf chunk 114.0  
[8] data/2002.08909v1.pdf chunk 93.0

### Multi-Agent Answer

REALM, or Retrieval-Augmented Language Model, is a novel framework for language model pre-training that augments standard pre-training algorithms with a learned textual knowledge retriever [E17][E13][E3]. Unlike traditional language models such as BERT, which store knowledge implicitly within their model parameters, REALM explicitly highlights the role of world knowledge by requiring the model to actively retrieve relevant external textual information during training [E17][E22][E3][E4][E21][E16]. This explicit retrieval mechanism differentiates REALM from models like BERT, as REALM accesses needed knowledge from a large external corpus as part of its learning and prediction process, rather than only relying on what is embedded in model weights [E3][E12][E1].

### Metrics

- baseline_latency_seconds: 3.808
- orchestrator_latency_seconds: 74.449
- baseline_total_tokens: 1430
- orchestrator_total_tokens: 38041
- baseline_citation_count: 8
- orchestrator_evidence_count: 30
- fact_check_status_counts: {'supported': 6}

## Question 2

Explain how the retrieve-then-predict framework works in REALM, including the role of the latent variable z and backpropagation through the retriever.

### Baseline Answer

The retrieve-then-predict framework in REALM works by decomposing the probability of generating an output y given an input x into two steps: retrieval of documents and prediction conditioned on the retrieved documents. Specifically, REALM first samples potentially relevant documents \( z \) from a knowledge corpus \( Z \) using a learned retriever, modeling this as \( p(z|x) \). Then it predicts the output \( y \) conditioned on both the input \( x \) and the retrieved documents \( z \), modeled as \( p(y|z,x) \). The overall likelihood is obtained by treating \( z \) as a latent variable and marginalizing over all documents:

\[
p(y|x) = \sum_{z \in Z} p(y|z,x) p(z|x)
\]

Here, \( z \) represents the latent variable corresponding to the retrieved document(s) from the corpus that may provide useful knowledge for the prediction task [1].

The role of the latent variable \( z \) is critical—it captures the uncertainty over which document(s) should be retrieved to best inform the prediction of \( y \). Since there is often more than one relevant document or incomplete knowledge, \( z \) acts as a latent variable that the model marginalizes over to incorporate knowledge retrieval directly within the language model’s generative process [1].

For the retriever modeling \( p(z|x) \), REALM uses a dense inner product model based on embeddings of the input \( x \) and documents \( z \):

\[
p(z|x) = \frac{\exp(f(x,z))}{\sum_{z'} \exp(f(x,z'))}, \quad f(x,z) = \text{Embed}_{input}(x)^\top \text{Embed}_{doc}(z)
\]

The embeddings are generated via BERT-style transformers, which produce vector representations for both input queries and candidate documents. The inner product of these embeddings gives a relevance score \( f(x,z) \), which is transformed via softmax over the corpus to obtain a retrieval distribution [1].

Backpropagation through the retriever is achieved by defining the objective as the log likelihood of generating the correct \( y \) given \( x \), marginalizing over the latent document \( z \). The gradient of this likelihood with respect to the retriever parameters \( \theta \) decomposes into terms over all documents \( z \), weighted by the difference between the conditional prediction probability \( p(y|z,x) \

### Multi-Agent Answer

The retrieve-then-predict framework in REALM operates by enhancing language model pre-training with a learned textual knowledge retriever, explicitly incorporating the retrieval of relevant information from an external knowledge corpus during pre-training and downstream tasks [E1][E13]. In this framework, for a given input text x, the model retrieves a potentially relevant document z from a large knowledge corpus Z by computing a probability distribution p(z|x) over all possible documents using a dense retriever [E13]. The retrieved document z serves as a latent variable, meaning its identity is not directly observed but is inferred by the model and marginalized out during training [E13]. After retrieving z, the language model predicts the output y (such as a masked token or an answer) conditioned on both x and z, forming the conditional probability p(y|z, x) [E13]. The overall likelihood of producing the correct output y given x, denoted p(y|x), is calculated by marginalizing over all possible z, thereby integrating retrieval and prediction in a unified probabilistic model [E13].

The retriever is trained jointly with the rest of the model parameters by optimizing the prediction objective, which requires backpropagating gradients through the retrieval mechanism [E9]. The gradient of the REALM training objective with respect to the retriever parameters can be derived using conditional Bayes' rule, linking the retrieval and prediction components [E9]. Thus, during training, updates to the retriever are guided by how well the retrieved documents help the language model make accurate predictions, allowing the retrieval process to evolve toward selecting more useful evidence [E9].

### Metrics

- baseline_latency_seconds: 5.781
- orchestrator_latency_seconds: 73.168
- baseline_total_tokens: 3548
- orchestrator_total_tokens: 35126
- baseline_citation_count: 8
- orchestrator_evidence_count: 23
- fact_check_status_counts: {'supported': 10}

## Question 3

What evidence does the paper provide that REALM improves Open-domain Question Answering performance compared to methods like ORQA, and what are the key reasons for this improvement?

### Baseline Answer

The paper provides evidence that REALM improves Open-domain Question Answering (QA) performance by presenting results on the NaturalQuestions-Open dataset after selectively ablating critical components of REALM. These results include both end-to-end QA performance and an analysis of retrieval quality, specifically how often the gold answer appears in the top-5 retrievals before any fine-tuning is applied. The latter metric isolates the contribution of improving the retriever during pre-training, indicating that REALM's enhanced retriever is a significant factor for its improved performance. This improvement in the retriever’s ability to surface relevant passages before fine-tuning differentiates REALM from methods like ORQA and contributes to better overall QA outcomes [1][2][3][4][5][6][7][8].

Key reasons for this performance improvement include:

1. End-to-end integration of retrieval and reading modules that allows for joint optimization.
2. The use of pre-training strategies that enhance the retriever’s capacity to identify relevant documents before the answer extraction step.
3. Ablation studies showing that these retrieval improvements have a direct impact on QA accuracy, isolating the retriever’s role in performance gains.

Thus, REALM’s improvement over ORQA can be attributed mainly to its advanced retriever, improved through pre-training and fine-tuning, which more often retrieves passages containing the gold answer prior to answer extraction.

Citations:  
[1][2][3][4][5][6][7][8] — source: data/2002.08909v1.pdf

### Multi-Agent Answer

The paper provides evidence that REALM improves Open-domain Question Answering (QA) performance by presenting results for the NaturalQuestions-Open dataset after ablating critical components of the REALM model and reporting the impact on key retrieval metrics [E1][E2][E3][E4][E5][E6][E7][E8][E9][E10]. In particular, the authors measure how frequently the gold (correct) answer appears in the top-5 retrievals before any fine-tuning is applied, which serves to more directly assess the contribution of the retrieval component pre-trained within REALM [E1][E2][E3][E4][E5][E6][E7][E8][E9][E10].

The key reason identified for improvement is that reporting the gold answer frequency in the top-5 retrievals before fine-tuning more significantly isolates the gains from enhancing the retriever during pre-training, as opposed to improvements from downstream fine-tuning or other modeling components [E1][E2][E3][E4][E5][E6][E7][E8][E9][E10]. However, the provided evidence does not include a direct comparison to ORQA or specific quantitative results, so the extent of REALM’s improvement over ORQA cannot be precisely determined from these notes [E1][E2][E3][E4][E5][E6][E7][E8][E9][E10].

### Metrics

- baseline_latency_seconds: 4.708
- orchestrator_latency_seconds: 33.734
- baseline_total_tokens: 1627
- orchestrator_total_tokens: 14946
- baseline_citation_count: 8
- orchestrator_evidence_count: 10
- fact_check_status_counts: {'supported': 6}
