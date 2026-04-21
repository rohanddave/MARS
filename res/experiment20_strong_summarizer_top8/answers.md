# experiment20: retrieval sweep, strong summarizer only, top_k=8

## Agent Configuration

- family: top_k_sweep
- control_variable: top_k
- top_k: 8
- max_evidence_chunks: 8
- baseline_model: google/gemma-4-26B-A4B-it
- orchestrator_model: google/gemma-4-26B-A4B-it
- search_model: google/gemma-4-26B-A4B-it
- summarization_model: google/gemma-4-26B-A4B-it
- fact_check_model: google/gemma-4-26B-A4B-it
- final_synthesis_model: google/gemma-4-26B-A4B-it

## Question 1

Type: easy lookup

What external knowledge source or corpus does REALM retrieve from, and how is it used by the model?

### Baseline Answer

REALM retrieves from a large textual knowledge corpus, such as Wikipedia [1, 2]. This knowledge corpus is used during pre-training, fine-tuning, and inference [2].

The model uses this external knowledge through a "retrieve-then-predict" generative process [3]. Specifically:
*   **Retrieve:** Given an input $x$, the model first uses a learned textual knowledge retriever to retrieve potentially helpful documents $z$ from the knowledge corpus $Z$ [1, 3]. This is modeled as a sample from the distribution $p(z | x)$ [3].
*   **Predict:** The model then conditions on both the retrieved documents $z$ and the original input $x$ to generate the output $y$, modeled as $p(y | z, x)$ [3].

The overall process is modeled as a latent variable language model where the model marginalizes over all possible documents $z$ to obtain the likelihood of generating $y$ [1, 3].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7

### Multi-Agent Answer

REALM retrieves information from a large knowledge corpus $Z$, such as Wikipedia [E2, E3]. The model can be applied in a single-corpus setting where both the input and the knowledge source are Wikipedia, or in a separate-corpus setting where the input is CC-News and the knowledge source is Wikipedia [E4].

The model uses this information through a two-step process [E1]:

1.  **Retrieval:** A learned textual knowledge retriever models $p(z |x)$ to retrieve a document $z$ from the corpus $Z$ [E1]. This retriever uses BERT-style Transformer embedding functions to map the input and documents to $d$-dimensional vectors [E1]. Relevance is determined using a dense inner product model [E1].
2.  **Prediction:** The model then predicts the output $y$ conditioned on both the input and the retrieved document, modeled as $p(y |z, x)$ [E1]. The model attends over the retrieved documents to help inform its prediction [E2, E3].

### Metrics

- baseline_latency_seconds: 7.509
- orchestrator_latency_seconds: 74.193
- baseline_total_tokens: 8649
- orchestrator_total_tokens: 54051
- baseline_citation_count: 8
- orchestrator_evidence_count: 12
- fact_check_status_counts: {'unsupported': 4, 'supported': 6}

## Question 2

Type: easy lookup

Which downstream tasks or benchmarks does the paper use to evaluate REALM?

### Baseline Answer

To evaluate REALM, the paper uses the following Open-QA benchmarks:

*   **NQ** (NaturalQuestions) [6]
*   **WQ** (WebQuestions) [6]
*   **CT** (ComplexType) [6]

Additionally, the paper presents ablation experiments specifically using the **NaturalQuestions-Open** (NQ-Open) dataset [1, 7].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05, chunk_index: 12
[6] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-11-3fa55fc3148d1188cb70ab91, chunk_index: 11
[7] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e, chunk_index: 13

### Multi-Agent Answer

The paper evaluates REALM by fine-tuning the model on the task of Open-domain Question Answering (Open-QA) [E10]. Specifically, REALM achieves state-of-the-art results on three popular Open-QA benchmarks: NATURAL QUESTIONS, WEB QUESTIONS, and CURATED TREC [E5].

### Metrics

- baseline_latency_seconds: 6.249
- orchestrator_latency_seconds: 34.128
- baseline_total_tokens: 8188
- orchestrator_total_tokens: 29671
- baseline_citation_count: 8
- orchestrator_evidence_count: 10
- fact_check_status_counts: {'supported': 2}

## Question 3

Type: definition

What is REALM, and what does the paper mean by retrieval-augmented language model pre-training?

### Baseline Answer

REALM stands for Retrieval-Augmented Language Model [1, 2]. It is a framework designed to capture knowledge in a more modular and interpretable way by augmenting language model pre-training algorithms with a learned textual knowledge retriever [1, 2]. Unlike traditional models that store knowledge implicitly within their parameters, REALM explicitly exposes the role of world knowledge by requiring the model to decide what knowledge to retrieve and use during inference [1, 2]. Before making a prediction, the language model uses the retriever to pull documents from a large corpus (such as Wikipedia) and then attends over those documents to inform its prediction [1].

Retrieval-augmented language model pre-training refers to the process of augmenting the pre-training of a language model with a latent knowledge retriever [2]. This approach involves:
*   **Unsupervised Learning:** The knowledge retriever is trained in an unsupervised manner, using masked language modeling as the learning signal [2].
*   **Performance-Based Signal:** The retriever is trained using a signal from unsupervised text where retrievals that improve the language model's perplexity are rewarded, while uninformative retrievals are penalized [1].
*   **End-to-End Optimization:** The model is trained end-to-end by backpropagating through a retrieval step that considers an entire corpus of textual knowledge [1].
*   **Generative Process:** The process is modeled as a "retrieve-then-predict" generative process where, given an input $x$, the model first retrieves documents $z$ from a knowledge corpus $Z$ (modeled as $p(z|x)$) and then conditions on both $z$ and $x$ to generate an output $y$ (modeled as $p(y|z, x)$) [3].

Citations:
[1] data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[3] data/2002

### Multi-Agent Answer

REALM (Retrieval-Augmented Language Model) extends the retrieval-based approach—which involves retrieving potentially relevant documents $z$ from a corpus $Z$ to extract an answer $y$ from a question $x$—to the process of language model pre-training [E6]. The model decomposes the generative process $p(y |x)$ into two steps: it first retrieves documents and then predicts [E6]. Specifically, it utilizes a "knowledge retriever" to model $p(z |x)$ and a "knowledge-augmented encoder" to model $p(y |z, x)$ [E6]. REALM functions as a generalization of previous models that conditioned on words, sentences, or paragraphs by extending the scope to the entire text corpus [E8]. Furthermore, the model's document index serves as a scalable grounded neural memory where the keys are document embeddings [E8]. This grounding—where each memory is associated with a specific document rather than unnamed value vectors—provides interpretability and provenance, which is considered crucial for trustworthiness in Open-domain Question Answering (Open-QA) applications [E7, E8].

### Metrics

- baseline_latency_seconds: 8.571
- orchestrator_latency_seconds: 77.311
- baseline_total_tokens: 9006
- orchestrator_total_tokens: 52435
- baseline_citation_count: 8
- orchestrator_evidence_count: 14
- fact_check_status_counts: {'supported': 9, 'unsupported': 1}

## Question 4

Type: definition

How does REALM differ from a standard parametric language model such as BERT in where knowledge is stored and accessed?

### Baseline Answer

Standard parametric language models, such as BERT, store learned world knowledge implicitly within the parameters of the underlying neural network [1]. This method makes it difficult to determine what knowledge is stored and where it is located, and because storage space is limited by the network size, capturing more knowledge requires training increasingly larger networks [1].

In contrast, REALM (Retrieval-Augmented Language Model) differs in the following ways:

*   **Storage:** Instead of storing knowledge solely in parameters, REALM uses a learned textual knowledge retriever to access a large textual knowledge corpus, such as Wikipedia [1, 2]. Its memories are "grounded," meaning each memory is associated with a specific document rather than unnamed value vectors [3].
*   **Access:** During pre-training, fine-tuning, and inference, the model explicitly decides what knowledge to retrieve [1, 2]. It uses the retriever to retrieve documents from the corpus and then attends over those documents to inform its predictions [1, 2].

### Multi-Agent Answer

Standard parametric language models, such as BERT, store world knowledge implicitly within the neural network parameters [E3]. This method of implicit storage requires the use of increasingly larger networks to cover a greater number of facts [E3]. Additionally, because knowledge is stored in parameters, it is difficult to determine what knowledge is stored or where it is located, and the storage space is limited to the size of the network [E3].

In contrast, REALM (Retrieval-Augmented Language Model) captures knowledge in a more modular and interpretable way by augmenting language model pre-training with a learned textual knowledge retriever [E2, E3]. Rather than relying solely on parameters, REALM utilizes a document index that functions as a scalable, grounded neural memory [E7]. These memories are considered "grounded" because each memory is associated with a specific document rather than unnamed value vectors [E8].

To access knowledge, REALM explicitly requires the model to decide what to retrieve and use during inference [E2]. Before making each prediction, the language model uses the retriever to retrieve documents from a large corpus, such as Wikipedia, and then attends over those documents to help inform its prediction [E2].

### Metrics

- baseline_latency_seconds: 3.124
- orchestrator_latency_seconds: 78.092
- baseline_total_tokens: 7986
- orchestrator_total_tokens: 57199
- baseline_citation_count: 8
- orchestrator_evidence_count: 17
- fact_check_status_counts: {'supported': 7, 'unsupported': 1}

## Question 5

Type: method/mechanism

How does REALM's retrieve-then-predict framework work, including the role of the latent document variable z?

### Baseline Answer

REALM's retrieve-then-predict framework is a generative process that decomposes the probability of an output $p(y | x)$ into two distinct steps:

1.  **Retrieve:** Given an input $x$, the model first retrieves potentially helpful documents $z$ from a knowledge corpus $Z$ [3]. This is modeled as a sample from the distribution $p(z | x)$ [3].
2.  **Predict:** The model then conditions on both the retrieved document $z$ and the original input $x$ to generate the output $y$, which is modeled as $p(y | z, x)$ [3].

**The Role of the Latent Document Variable $z$**
The framework treats the retrieved document $z$ as a latent variable [3]. To obtain the overall likelihood of generating the output $y$ given the input $x$, the model marginalizes over all possible documents $z$ in the corpus $Z$ [3]. This is expressed by the formula:
$$p(y | x) = \sum_{z \in Z} p(y | z, x) p(z | x)$$ [3]

By modeling the approach this way, the framework can be optimized by maximizing the marginal likelihood [1].

Citations:
[1] data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[3] data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7

### Multi-Agent Answer

REALM (Retrieval-Augmented Language Model) employs a "retrieve-then-predict" framework that models the process as a latent variable language model and optimizes the marginal likelihood [E1]. This framework decomposes the learning of a distribution $p(y|x)$ into two distinct steps: first, retrieving potentially helpful documents $z$ from a knowledge corpus $Z$, and second, predicting the output $y$ conditioned on both the input $x$ and the retrieved $z$ [E3].

The framework consists of two primary architectural components:

*   **Neural Knowledge Retriever:** This component models the distribution $p(z|x)$ [E3]. It retrieves documents from a large corpus, such as Wikipedia [E1, E2]. The retriever uses a dense inner product model where the relevance score $f(x, z)$ is defined as the inner product of the vector embeddings [E3].
*   **Knowledge-Augmented Encoder:** This component models the distribution $p(y|z, x)$ [E3]. Once the retriever selects documents, the language model attends over those documents to help inform its prediction [E1, E2].

### Metrics

- baseline_latency_seconds: 5.596
- orchestrator_latency_seconds: 83.837
- baseline_total_tokens: 7954
- orchestrator_total_tokens: 57305
- baseline_citation_count: 8
- orchestrator_evidence_count: 11
- fact_check_status_counts: {'supported': 7, 'unsupported': 2}

## Question 6

Type: method/mechanism

How does the paper train the retriever when the retrieved document is latent, and how does learning signal flow back to retrieval?

### Baseline Answer

The paper trains the retriever by modeling the retrieve-then-predict approach as a latent variable language model and optimizing the marginal likelihood [1]. Specifically, the overall likelihood of generating an output $y$ given an input $x$ is obtained by treating the retrieved document $z$ as a latent variable and marginalizing over all possible documents $z$ in the knowledge corpus $Z$, expressed by the formula $p(y |x) = \sum_{z \in Z} p(y |z, x) p(z |x)$ [4].

The learning signal flows back to the retrieval module through backpropagation [1, 2]. The gradient of the pre-training objective (the log-likelihood) with respect to the parameters of the knowledge retriever $\theta$ is calculated as:
$$\nabla \log p(y |x) = \sum_{z} [p(z |y, x) - p(z |x)] \nabla f(x, z)$$
[6]. 

This signal essentially rewards retrievals that improve the language model's perplexity and penalizes uninformative ones [1]. If a single document $z^*$ exists that allows for perfect prediction accuracy, the gradient descent on the REALM objective becomes equivalent to gradient descent on $\log p(z^* |x)$, similar to typical maximum likelihood training used in supervised learning [6].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7
[6] source: data/2002.08909v1.pdf, chunk_id

### Multi-Agent Answer

In the REALM framework, the "retrieve-then-predict" approach is modeled as a latent variable language model optimized by marginal likelihood [E1]. This process decomposes the learning of the distribution $p(y|x)$ into two distinct steps: first, retrieving potentially helpful documents $z$ from a knowledge corpus $Z$, and second, predicting the output $y$ conditioned on both the input $x$ and the retrieved documents $z$ [E4]. Consequently, the overall likelihood of generating $y$ is obtained by treating $z$ as a latent variable and marginalizing over all possible documents: $p(y |x) = \sum_{z \in Z} p(y |z, x) p(z |x)$ [E4].

The learning signal flows back to the retriever via the language modeling objective, which backpropagates through the retrieval step [E2]. The retriever is trained using a performance-based signal derived from unsupervised text; specifically, retrievals that improve the language model's perplexity are rewarded, while uninformative retrievals are penalized [E1].

### Metrics

- baseline_latency_seconds: 6.431
- orchestrator_latency_seconds: 41.607
- baseline_total_tokens: 7920
- orchestrator_total_tokens: 31019
- baseline_citation_count: 8
- orchestrator_evidence_count: 13
- fact_check_status_counts: {'supported': 6}

## Question 7

Type: method/mechanism / implementation

What approximations or engineering choices does REALM use to make retrieval over a large corpus practical during training and inference?

### Baseline Answer

To make retrieval over a large corpus practical during training and inference, REALM employs the following engineering choices and approximations:

*   **MIPS Formulation:** The selection of the best documents is formulated as a Maximum Inner Product Search (MIPS) [2].
*   **Caching and Asynchronous Updates:** The retriever is structured so that computations performed for each document can be cached and updated asynchronously [2].
*   **Parallelization:** During pre-training, the document embedding step for the MIPS index is parallelized over 16 TPUs [4].
*   **Index Refreshing:** To manage the large-scale retrieval, REALM runs a parallel process to re-embed corpus documents and rebuild the MIPS index, resulting in an index refresh approximately every 500 training steps [5].
*   **Candidate Reduction:** During fine-tuning inference, the system considers only the top-5 candidates [4]. In the pre-training phase, the model retrieves and marginalizes over 8 candidate documents, which includes a null document $\emptyset$ [4].

Citations:
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-11-3fa55fc3148d1188cb70ab91
[5] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e

### Multi-Agent Answer

To make retrieval over a large corpus of millions of documents practical during training and inference, REALM employs several engineering choices and approximations:

*   **Document Selection and Search:** To address the computational challenges of considering millions of candidate documents [E1, E2], REALM uses Maximum Inner Product Search (MIPS) for document selection [E1]. The retriever is implemented as a dense inner product model, where the relevance score is determined by the inner product of vector embeddings [E4].
*   **Caching and Asynchronicity:** The retriever is structured so that the computation for each document can be cached and updated asynchronously [E1].
*   **Inference Optimization:** During fine-tuning inference, the model optimizes performance by considering only the top-5 candidate documents [E3, E5].
*   **Parallelization:** To assist with training, the document embedding step is parallelized over 16 TPUs [E3].

### Metrics

- baseline_latency_seconds: 5.530
- orchestrator_latency_seconds: 40.052
- baseline_total_tokens: 8613
- orchestrator_total_tokens: 31516
- baseline_citation_count: 8
- orchestrator_evidence_count: 13
- fact_check_status_counts: {'supported': 5}

## Question 8

Type: comparison

How does REALM compare with ORQA or other open-domain QA baselines, and what evidence supports that comparison?

### Baseline Answer

REALM compares to ORQA and other open-domain QA baselines as follows:

*   **Comparison with ORQA:** ORQA is the most direct comparison to REALM because the fine-tuning setup, hyperparameters, and training data are identical [1]. Additionally, the retrievers for both REALM pre-training and ORQA are initialized using the Inverse Cloze Task [2]. The improvement REALM shows over ORQA is attributed entirely to better pre-training methods [1]. Furthermore, while ORQA uses a fixed index, REALM adds a novel language model pre-training step and backpropagates into the MIPS index [7].
*   **Comparison with other Retrieval-based systems:** Compared to other retrieval-based systems (such as DrQA, HardEM, GraphRetriever, and PathRetriever), which often retrieve between 20 to 80 documents, REALM achieves the overall best performance while only retrieving 5 documents [1, 7].
*   **Comparison with Generation-based systems:** REALM compares against state-of-the-art systems from the generation paradigm, specifically comparing to concurrent work that fine-tunes T5 for Open-QA [4].

**Evidence supporting these comparisons:**
The text notes that resetting both the retriever and encoder parameters to their baseline state reduces the system to its main baseline, ORQA [5]. Results presented in the text indicate that REALM achieves new state-of-the-art results on three benchmarks, outperforming all previous systems by 4-16% absolute accuracy [8].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-10-8ea61faa3a17c1fc8f8725d8
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b5

### Multi-Agent Answer

REALM achieves new state-of-the-art results on all three tested benchmarks, significantly outperforming all previous systems by 4-16% absolute accuracy [E7].

Regarding specific comparisons:

*   **ORQA:** ORQA serves as the most direct comparison to REALM because the fine-tuning setup, hyperparameters, and training data are identical [E1]. Additionally, the retrievers for both REALM pre-training and ORQA are initialized using the Inverse Cloze Task [E2]. The improvement of REALM over ORQA is attributed purely to better pre-training methods [E1].
*   **Other Retrieval-Based Systems:** REALM achieves the best overall performance compared to other retrieval-based systems despite retrieving fewer documents [E1]. While other retrieval-based systems typically retrieve between 20 to 80 documents, REALM achieves its best performance by retrieving only 5 documents [E1].
*   **T5 Models:** REALM outperforms the largest T5-11B model while being 30 times smaller [E8]. Specifically, on the NQ (79k/4k) benchmark, REALM (Wikipedia) achieves 39.2 compared to T5 (11b)'s 34.5 [E8]. On the WQ (3k/2k) benchmark, REALM (Wikipedia) achieves 40.2 while T5 (11b) achieves 37.4 [E8].

### Metrics

- baseline_latency_seconds: 6.163
- orchestrator_latency_seconds: 79.277
- baseline_total_tokens: 7685
- orchestrator_total_tokens: 52427
- baseline_citation_count: 8
- orchestrator_evidence_count: 9
- fact_check_status_counts: {'supported': 8}

## Question 9

Type: comparison

How does REALM's retrieval-based approach compare with storing knowledge only in model parameters?

### Baseline Answer

In contrast to models that store world knowledge implicitly in their parameters, REALM's retrieval-based approach offers the following comparisons:

*   **Interpretability and Modularity:** REALM captures knowledge in a more modular and interpretable way [1, 3]. While implicit storage makes it difficult to determine what knowledge is stored and where, REALM's memories are "grounded," meaning each memory is associated with a specific document rather than unnamed value vectors [3, 6]. This provides provenance for predicted answers, which is crucial for trustworthiness in applications like Open-domain Question Answering (Open-QA) [6].
*   **Explicit Knowledge Role:** The approach explicitly exposes the role of world knowledge by requiring the model to decide what knowledge to retrieve and use during inference [1, 3].
*   **Storage Capacity and Efficiency:** In models where knowledge is stored in parameters, storage space is limited by the size of the network, requiring increasingly larger networks to cover more facts, which can be expensive or slow [3]. REALM avoids this by retrieving and attending over documents from a large corpus (such as Wikipedia) [1, 3].
*   **Adaptability:** REALM can adapt to updated knowledge corpora; for example, a model pre-trained on an older corpus can still retrieve information from an updated corpus to generate correct tokens [8].

Citations:
[1] data/2002.08909v1.pdf (chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952)
[3] data/2002.08909v1.pdf (chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2)
[6] data/2002.08909v1.pdf (chunk_id: 2002.08909v1-14-83fbe5c3ec4e1ed386558b56)
[8] data/2002.08909v1.pdf (chunk_id: 2002.089

### Multi-Agent Answer

In contrast to standard language model pre-training, which stores world knowledge implicitly within the parameters of a neural network, REALM (Retrieval-Augmented Language Model) uses a learned textual knowledge retriever to capture knowledge in a more modular and interpretable way [E3, E7]. While implicit storage requires ever-larger networks to cover an increasing number of facts, REALM's approach allows the model to retrieve and attend over documents from a large corpus during pre-training, fine-tuning, and inference [E7].

REALM's approach provides specific advantages regarding interpretability and provenance:

* **Grounded Memories:** Unlike models that use unnamed value vectors, REALM's memories are "grounded," meaning each memory is associated with a specific document [E5, E6].
* **Interpretability and Trustworthiness:** This grounding provides a level of interpretability and provenance that is considered crucial for Open-domain Question Answering (Open-QA) applications, as users require provenance for a predicted answer to be trustworthy [E5, E6].

### Metrics

- baseline_latency_seconds: 6.414
- orchestrator_latency_seconds: 80.287
- baseline_total_tokens: 7854
- orchestrator_total_tokens: 55575
- baseline_citation_count: 8
- orchestrator_evidence_count: 14
- fact_check_status_counts: {'unsupported': 3, 'supported': 3}

## Question 10

Type: evidence synthesis / ablation

What ablation or diagnostic evidence shows that retrieval pre-training improves REALM rather than only the reader component?

### Baseline Answer

To determine whether REALM pre-training improves the retriever, the encoder, or both, researchers conducted an ablation study where they reset the parameters of either the retriever or the encoder to their baseline state before fine-tuning [4]. 

The diagnostic evidence from this ablation shows:
* **Individual Benefits:** Both the retriever and the encoder benefit from REALM training when improved separately [4].
* **Synergy:** The best results are achieved when both components act in unison [4].
* **Comparison to Baseline:** When both the retriever and encoder are reset, the system reduces to the main baseline, ORQA [4].
* **Retrieval Performance:** The metric of how often the gold answer appears in the top-5 retrievals before fine-tuning was used to more significantly isolate the specific contribution of improving the retriever during pre-training [1, 4].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e

### Multi-Agent Answer

The improvement of REALM over the ORQA baseline is attributed purely to better pre-training methods [E3, E6]. This is demonstrated by the fact that the fine-tuning setups, hyperparameters, and training data are identical between REALM and ORQA [E3, E6].

Ablation analysis shows that both the retriever and the encoder components benefit from REALM training independently [E10]. However, resetting both the retriever and encoder parameters to their baseline states reduces the system's performance to the ORQA baseline [E10].

To specifically isolate the contribution of retriever improvement during pre-training, the authors use a metric measuring how often the gold answer appears in the top-5 retrievals before applying fine-tuning [E3, E10].

### Metrics

- baseline_latency_seconds: 4.239
- orchestrator_latency_seconds: 38.619
- baseline_total_tokens: 7816
- orchestrator_total_tokens: 31085
- baseline_citation_count: 8
- orchestrator_evidence_count: 10
- fact_check_status_counts: {'supported': 5}

## Question 11

Type: evidence synthesis

Synthesize the evidence for why REALM improves open-domain QA performance, including retrieval quality, pre-training, and downstream fine-tuning.

### Baseline Answer

REALM improves open-domain question answering (Open-QA) performance through the following mechanisms:

*   **Pre-training Improvements:** The improvement of REALM over the baseline ORQA is attributed purely to better pre-training methods [1]. REALM utilizes a masked language modeling (MLM) task as an unsupervised learning signal during pre-training [4]. This process optimizes a latent variable language model by maximizing the marginal likelihood, which rewards the retriever for selecting documents that improve the language model's perplexity [5]. This pre-training approach benefits both the encoder and the retriever components [8].
*   **Retrieval Quality:** Unlike prior works that used non-learned or heuristic retrievers, REALM uses a learned neural knowledge retriever [4, 5]. During pre-training, the model learns to retrieve helpful documents from a large corpus (such as Wikipedia) to fill in masked tokens [5]. This enables the system to achieve high performance even when retrieving a very small number of documents; for example, REALM achieves its best overall performance while retrieving only 5 documents, whereas other retrieval-based systems often retrieve between 20 and 80 documents [1].
*   **Downstream Fine-tuning:** REALM is designed so that its retriever can transfer to downstream tasks because it retrieves raw text rather than labeled examples [5]. When fine-tuned on Open-QA tasks, REALM outperforms state-of-the-art models—including extremely large implicit knowledge models like T5-11B—by a significant margin of 4-16% absolute accuracy, despite being 30 times smaller [4, 5]. Additionally, REALM provides qualitative benefits such as increased modularity and interpretability [4, 5].

**Citations**
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[5] source: data/2002.0890

### Multi-Agent Answer

REALM improves open-domain question answering (Open-QA) performance through a framework that augments language model pre-training algorithms with a learned textual knowledge retriever [E5]. The core of REALM's improvement over models like ORQA is attributed purely to its superior pre-training methods, as the fine-tuning setups, hyperparameters, and training data are identical [E1][E6].

**Retrieval Quality**
REALM's retriever is trained using a performance-based signal from unsupervised text, where retrievals that improve the language model's perplexity are rewarded and uninformative retrievals are penalized [E5]. This training allows the retriever to be used even when trained with unsupervised text only [E8]. The retriever's effectiveness is demonstrated by its ability to assign a much higher probability to a correct masked term compared to models without retrieval because it can retrieve documents containing related facts [E8]. This high quality of retrieval enables REALM to achieve its best overall performance by retrieving as few as five documents, whereas other retrieval-based systems typically retrieve between 20 and 80 documents [E1].

**Pre-training and Fine-tuning**
The pre-training task in REALM is masked language modeling (predicting missing tokens from a sentence), while the fine-tuning task is Open-QA (predicting an answer from a question) [E4]. This process involves a generative process that treats the retrieved document as a latent variable [E4]. During pre-training, the retriever and language model can be trained in an unsupervised manner using masked language modeling as the learning signal [E7]. While the encoder and retriever can benefit from being trained separately, the best results are achieved when both components act in unison [E8]. By using pre-trained models that are then fine-tuned for downstream tasks like Open-QA, the system often achieves better generalization than training from scratch [E2].

### Metrics

- baseline_latency_seconds: 7.037
- orchestrator_latency_seconds: 86.116
- baseline_total_tokens: 8205
- orchestrator_total_tokens: 55846
- baseline_citation_count: 8
- orchestrator_evidence_count: 10
- fact_check_status_counts: {'supported': 12}

## Question 12

Type: multi-step reasoning

Explain step by step how a masked-language-model pre-training objective can improve downstream open-domain QA in REALM.

### Baseline Answer

In REALM, a masked-language-model (MLM) pre-training objective improves downstream open-domain question answering (Open-QA) through the following process:

1.  **Unsupervised Pre-training with MLM:** The model undergoes pre-training on an unlabeled corpus (such as Wikipedia) using an MLM objective [1]. In this task, tokens are randomly masked in a text passage, and the model must predict the value of these missing tokens [1].
2.  **Learning Representations and Knowledge:** To successfully predict masked tokens, the model must learn to encode syntactic and semantic information, as well as world knowledge [1]. This pre-training helps the model learn useful representations of language [1].
3.  **Joint Training of Retriever and Encoder:** REALM augments the MLM process with a learned textual knowledge retriever [2]. The system is modeled as a "retrieve-then-predict" process where the model retrieves potentially helpful documents from a knowledge corpus and then attends over those documents to inform its prediction [2, 3]. Crucially, the signal from the MLM objective backpropagates through the retrieval step [2].
4.  **Rewarding Informative Retrieval:** The retriever is trained using a performance-based signal from the unsupervised text; a retrieval that improves the language model's perplexity is rewarded, while uninformative retrievals are penalized [5].
5.  **Transfer to Downstream Open-QA:** After pre-training, the parameters of the retriever and the knowledge-augmented encoder are fine-tuned on the downstream Open-QA task [2]. Because the retriever was trained to find documents that assist in language modeling, it is designed to transfer to other tasks, such as retrieving documents to help answer a question [5].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-2-7f240c64641ad3f52fc62e97, chunk_index: 2
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2, chunk_index: 0

### Multi-Agent Answer

The masked-language-model (MLM) pre-training objective improves downstream open-domain question answering (Open-QA) in REALM through the following steps:

1.  **Learning Representations and Knowledge via MLM:** The primary goal of language model pre-training is to learn useful language representations from unlabeled text corpora [E1]. In the MLM variant of pre-training, the model is trained to predict missing tokens within an input text passage [E1, E4, E7]. To succeed at this task, the model must encode syntactic information, semantic information, and world knowledge [E1].
2.  **Unsupervised Training of the Retriever:** REALM uses the MLM task as an unsupervised learning signal to pre-train a latent knowledge retriever [E2]. This retriever is trained using a performance-based signal from unsupervised text, where retrievals that improve the language model's perplexity are rewarded and uninformative retrievals are penalized [E3]. During this phase, the model learns to retrieve and attend over documents from a large corpus, such as Wikipedia [E2, E3].
3.  **Improved Generalization for Downstream Tasks:** By learning these representations and utilizing the retriever during pre-training, the model achieves better generalization for downstream tasks like Open-QA compared to training from scratch [E1]. This pre-training process specifically improves the retriever's ability to capture knowledge in a modular and interpretable way [E2]. The effectiveness of this method is evidenced by REALM's ability to outperform previous systems by 4-16% absolute accuracy on Open-QA benchmarks [E1, E2, E3].

### Metrics

- baseline_latency_seconds: 6.974
- orchestrator_latency_seconds: 78.396
- baseline_total_tokens: 9087
- orchestrator_total_tokens: 53933
- baseline_citation_count: 8
- orchestrator_evidence_count: 14
- fact_check_status_counts: {'unsupported': 3, 'supported': 9}

## Question 13

Type: multi-step reasoning / error analysis

If REALM retrieves an irrelevant document, how would that affect p(z|x), p(y|z,x), and the final answer prediction?

### Baseline Answer

If REALM retrieves an irrelevant document $z$, the effects are as follows:

*   **$p(z|x)$:** This represents the distribution modeled by the neural knowledge retriever [3]. While the context does not explicitly state how an irrelevant document affects the specific value of $p(z|x)$ in a single instance, it notes that at the beginning of training, if the retriever does not have good embeddings, the retrieved documents $z$ will likely be unrelated to $x$ [7].
*   **$p(y|z, x)$:** This is the conditional probability modeled by the knowledge-augmented encoder [3]. An irrelevant document $z$ can result in a negative Retrieval Utility (RU), which is defined as $\text{RU}(z |x) = \log p(y |z, x) - \log p(y |\emptyset, x)$ [1]. A negative RU indicates that the retrieved document $z$ is less useful for predicting $y$ than the null document $\emptyset$ [1].
*   **Final answer prediction ($p(y|x)$):** The overall likelihood of generating $y$ is obtained by marginalizing over all possible documents $z$: $p(y |x) = \sum_{z \in Z} p(y |z, x) p(z |x)$ [3]. The context indicates that when REALM retrieves documents with related facts, the marginalized probability of the correct answer increases [2]. Conversely, if the retriever provides uninformative retrievals, it should be penalized [4]. Furthermore, if the knowledge-augmented encoder learns to ignore retrieved documents because they are unrelated, the retriever may fail to receive a meaningful gradient to improve, potentially creating a "vicious cycle" [7].

Citations:
[1] data/2002.08909v1.pdf, chunk_id: 2002.08909v1-20-58cd33db77feaae8a3f8d036
[2] data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e
[3] data/2002.089

### Multi-Agent Answer

The provided evidence does not contain specific information regarding the exact mathematical or qualitative impact that retrieving an irrelevant document has on the individual components $p(z|x)$, $p(y|z,x)$, or the final answer prediction.

However, the evidence does provide the following related information:
*   A negative Retrieval Utility (RU) indicates that a retrieved document ($z$) is less useful for predicting the target ($y$) than a null document [E1].
*   A negative RU may occur if the retrieved document $z$ is irrelevant to the input $x$ [E1].
*   In contrast to the effects of irrelevant retrieval, the ability to retrieve documents containing related facts can dramatically increase the marginalized probability of the correct answer [E7].
*   For example, when predicting the term "Fermat," REALM (calculating marginal probability over the top 8 retrieved documents) assigns a probability of 0.129, whereas BERT (which does not use retrieval) assigns a probability of $1.1 \times 10^{-14}$ [E7].

### Metrics

- baseline_latency_seconds: 6.579
- orchestrator_latency_seconds: 71.220
- baseline_total_tokens: 8309
- orchestrator_total_tokens: 48024
- baseline_citation_count: 8
- orchestrator_evidence_count: 12
- fact_check_status_counts: {'unsupported': 1, 'supported': 4}

## Question 14

Type: limitation/uncertainty

What limitations, uncertainties, or missing comparisons should be noted when interpreting REALM's reported results?

### Baseline Answer

When interpreting REALM's reported results, the following limitations, uncertainties, and missing comparisons should be noted:

*   **Missing Data in Experiments:** Certain data that could potentially benefit REALM was not used in the experiments conducted [1].
*   **Index Staleness:** The frequency of MIPS index refreshes impacts model training; results suggest that a stale index can be detrimental, and further reducing staleness might offer better optimization [4].
*   **Uncertainty in Retrieval Utility (RU):** A negative RU indicates that the retrieved document $z$ is less useful for predicting $y$ than a null document [2]. However, this could be due to $z$ being irrelevant to $x$, or it could mean the masked tokens in $x$ do not require world knowledge, or that the necessary knowledge is already sufficiently embedded in the model's parameters [2].
*   **Sensitivity to Masking:** The utility of retrieval is impacted by the choice of masking [2]. The latent variable learning process is specifically noted to be sensitive to a consistent learning signal, making the salient span masking scheme crucial for REALM [4].
*   **Scope of Results:** While REALM achieved state-of-the-art results on three Open-QA benchmarks (NaturalQuestions-Open, Web Questions, and Curated TREC), the presented work is considered a "minimal instantiation" of a family of REALM-like approaches [8]. Future work is required to generalize these results to structured knowledge, multi-lingual settings, and multi-modal settings [5].

**Citations**
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-20-58cd33db77feaae8a3f8d036
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a6

### Multi-Agent Answer

When interpreting REALM's reported results, the following limitations, uncertainties, and missing data should be noted:

*   **Knowledge Update Limitations:** Although REALM can adapt to an updated knowledge corpus, the knowledge-augmented encoder may still "remember" certain old knowledge, which can lead to failures in updating specific predictions [E4].
*   **Retrieval Utility Uncertainties:** A negative Retrieval Utility (RU) indicates that a document is less useful for predicting the target than a null document [E4, E6]. This may occur if the document is irrelevant to the input, if the masked tokens do not require world knowledge, or if the required knowledge is already baked into the model's parameters [E4, E6].
*   **Optimization and Implementation Sensitivity:** The model's performance is sensitive to technical implementation details, such as the masking scheme used during training, where salient span masking is considered crucial [E2]. Additionally, using a stale MIPS index can negatively impact model training, making frequent index refreshes important for optimization [E2].
*   **Unused Experimental Data:** The researchers noted that certain types of data could potentially benefit REALM, but this data was not utilized in their experiments [E1].

### Metrics

- baseline_latency_seconds: 6.338
- orchestrator_latency_seconds: 40.128
- baseline_total_tokens: 7497
- orchestrator_total_tokens: 30395
- baseline_citation_count: 8
- orchestrator_evidence_count: 12
- fact_check_status_counts: {'supported': 5}

## Question 15

Type: citation grounding / uncertainty

Which claims about REALM's performance or mechanism cannot be verified unless the answer cites specific experimental evidence from the paper?

### Baseline Answer

Based on the provided context, the following claims about REALM's performance or mechanism cannot be verified without citing specific experimental evidence (such as results from Tables 1, 2, 3, or 4, or Figure 4) found in the paper:

*   **Performance relative to other systems:** Claims that REALM outperforms all previous methods by a margin of 4-16% absolute accuracy [7], that it achieves the "overall best performance" while only retrieving 5 documents compared to other retrieval-based systems that retrieve 20 to 80 documents [1], or that its improvement over ORQA is "purely due to better pre-training methods" [1], require specific experimental comparisons.
*   **Mechanism components:** Claims regarding whether the encoder, the retriever, or both benefit from REALM training [4], the impact of the masking scheme (salient span masking vs. random token/span masking) [4], or the effect of MIPS index refresh rates on model training [4] require the experimental data presented in the paper's tables.
*   **Retrieval Utility (RU):** Claims that RU increases steadily over the course of pre-training and is more predictive of good performance on Open-QA downstream tasks than overall log-likelihood [3] require reference to the specific behavior shown in Figure 4.
*   **Knowledge Adaptation:** The claim that a REALM model can adapt to updated knowledge (e.g., retrieving a document from a 2020 corpus when pre-trained on a 2018 corpus) requires the specific example provided in Table 4 [3].
*   **Masked Token Prediction:** The claim that REALM assigns a much higher probability to a correct masked term (like "Fermat") compared to BERT requires the quantitative comparison provided in Table 3 [4].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-20-58cd33db77feaae8a3f8d

### Multi-Agent Answer

Based on the provided evidence, the following claims regarding REALM's mechanism or performance are supported by specific experimental data or findings:

*   **Performance relative to ORQA:** The improvement of REALM over ORQA is attributed purely to better pre-training methods [E1].
*   **Performance relative to other retrieval systems:** REALM achieves the overall best performance compared to other retrieval-based systems while retrieving significantly fewer documents—specifically 5 documents, whereas other systems typically retrieve 20 to 80 documents [E1].
*   **Accuracy across benchmarks:** REALM outperforms all previous systems by 4-16% absolute accuracy across three Open-QA benchmarks: NATURAL QUESTIONS, WEB QUESTIONS, and CURATED TREC [E9].
*   **Predictive power of Retrieval Utility (RU):** RU is more predictive of good performance on downstream Open-QA tasks than the overall log-likelihood [E11].
*   **Component contributions:** Both the encoder and the retriever benefit from training separately, but optimal results are achieved when both components work in unison [E4]. This can be substantiated through ablation studies on critical components of REALM [E4].
*   **Adaptability to new knowledge:** REALM can adapt to an updated knowledge corpus, such as a model pre-trained on a 2018 corpus being able to retrieve correct tokens when using an updated 2020 corpus [E11].

### Metrics

- baseline_latency_seconds: 6.338
- orchestrator_latency_seconds: 40.225
- baseline_total_tokens: 7930
- orchestrator_total_tokens: 30943
- baseline_citation_count: 8
- orchestrator_evidence_count: 11
- fact_check_status_counts: {'supported': 5}
