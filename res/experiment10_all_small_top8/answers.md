# experiment10: retrieval sweep, all small models, top_k=8

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

REALM retrieves from a large textual knowledge corpus, such as Wikipedia [1, 2]. This knowledge corpus can be used in a single-corpus setting (where the pre-training corpus and knowledge corpus are both Wikipedia) or a separate-corpus setting (e.g., pre-training on CC-News while retrieving from Wikipedia) [5].

The model uses this corpus through a "retrieve-then-predict" process:
*   **Retrieval:** Given an input $x$, the model uses a learned neural knowledge retriever to retrieve potentially helpful documents $z$ from the corpus $Z$ [1, 3]. This retrieval is modeled as a sample from the distribution $p(z|x)$ [3].
*   **Prediction:** The model then conditions on both the original input $x$ and the retrieved documents $z$ to generate an output $y$, modeled as $p(y|z, x)$ [3]. During inference, the language model attends over these retrieved documents to help inform its prediction [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7
[5] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-12-69a8bcd84db848ef23c1fa05

### Multi-Agent Answer

REALM retrieves information from a large knowledge corpus $Z$, such as Wikipedia [E2, E3]. The model's application can include a single-corpus setting where the pre-training corpus $X$ and knowledge corpus $Z$ are the same (e.g., $X = \text{Wikipedia}$, $Z = \text{Wikipedia}$) [E4]. Alternatively, it can function in a separate-corpus setting where $X$ is different from $Z$, such as using CC-News for $X$ and Wikipedia for $Z$ [E4].

The model uses this information through a process that decomposes the generative process $p(y|x)$ into two steps: retrieve, then predict [E1]. This process consists of first retrieving documents $z$ from the knowledge corpus $Z$, and then predicting an output $y$ conditioned on both the input $x$ and the retrieved documents $z$, which is formulated as $p(y|z, x)$ [E1]. Specifically, the language model uses a learned textual knowledge retriever to select documents and then attends over those documents to help inform its prediction [E2, E3].

### Metrics

- baseline_latency_seconds: 8.296
- orchestrator_latency_seconds: 77.802
- baseline_total_tokens: 8721
- orchestrator_total_tokens: 54543
- baseline_citation_count: 8
- orchestrator_evidence_count: 9
- fact_check_status_counts: {'unsupported': 2, 'supported': 4}

## Question 2

Type: easy lookup

Which downstream tasks or benchmarks does the paper use to evaluate REALM?

### Baseline Answer

To evaluate REALM, the paper uses the following Open-QA benchmarks:

*   **NQ** (NaturalQuestions) [6]
*   **WQ** (WebQuestions) [6]
*   **CT** (Curatest) [6]

Additionally, the paper presents ablation experiments specifically using the **NaturalQuestions-Open** (NQ-Open) dataset [1, 7].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05, chunk_index: 12
[6] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-11-3fa55fc3148d1188cb70ab91, chunk_index: 11
[7] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e, chunk_index: 13

### Multi-Agent Answer

REALM achieves state-of-the-art results on three Open-domain Question Answering (Open-QA) benchmarks [E6]. These benchmarks are:

*   NATURAL QUESTIONS [E6]
*   WEB QUESTIONS [E6]
*   CURATED TREC [E6]

### Metrics

- baseline_latency_seconds: 6.148
- orchestrator_latency_seconds: 71.247
- baseline_total_tokens: 8189
- orchestrator_total_tokens: 53314
- baseline_citation_count: 8
- orchestrator_evidence_count: 10
- fact_check_status_counts: {'supported': 2}

## Question 3

Type: definition

What is REALM, and what does the paper mean by retrieval-augmented language model pre-training?

### Baseline Answer

REALM (Retrieval-Augmented Language Model) is a novel framework designed to capture knowledge in a more modular and interpretable way [1, 2]. Unlike traditional models that store world knowledge implicitly within their parameters [2], REALM augments language model pre-training algorithms with a learned textual knowledge retriever [1, 2]. This retriever allows the model to explicitly decide what knowledge to retrieve and use during inference by retrieving and attending over documents from a large corpus, such as Wikipedia [1, 2].

Retrieval-augmented language model pre-training refers to the process of augmenting language model pre-training algorithms with a learned textual knowledge retriever [1]. In this approach, the model uses a "retrieve-then-predict" process [3]. For the pre-training task specifically, the model performs masked language modeling, where it must predict the value of missing (masked) tokens in a sentence [3, 4]. The model achieves this by first retrieving potentially helpful documents from a knowledge corpus and then conditioning on both the input and the retrieved documents to generate the output [3]. The retriever is trained in an unsupervised manner using a performance-based signal: retrievals that improve the language model's perplexity are rewarded, while uninformative retrievals are penalized [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-12-69a

### Multi-Agent Answer

REALM (Retrieval-Augmented Language Model) is a method that augments language model pre-training with a latent knowledge retriever [E1]. This retriever allows the model to retrieve and attend over documents from a large corpus, such as Wikipedia, during the pre-training, fine-tuning, and inference stages [E1]. Unlike models that use unnamed value vectors, REALM's memories are "grounded," meaning each memory is associated with a specific document [E8]. This grounding provides qualitative benefits such as modularity and interpretability [E1, E6, E8]. Such interpretability is considered crucial for applications like Open-domain Question Answering (Open-QA), where users require provenance for a predicted answer to be trustworthy [E8].

Retrieval-augmented language model pre-training refers to the process of augmenting standard language model pre-training—the goal of which is to learn useful representations of language from unlabeled text corpora [E6]—with a retrieval step [E1]. In this framework, the learning signal from the language modeling objective backpropagates through the retrieval step [E1]. The knowledge retriever can be pre-trained in an unsupervised manner using masked language modeling as the learning signal [E1].

### Metrics

- baseline_latency_seconds: 8.555
- orchestrator_latency_seconds: 75.151
- baseline_total_tokens: 9006
- orchestrator_total_tokens: 51495
- baseline_citation_count: 8
- orchestrator_evidence_count: 15
- fact_check_status_counts: {'supported': 8, 'unsupported': 1}

## Question 4

Type: definition

How does REALM differ from a standard parametric language model such as BERT in where knowledge is stored and accessed?

### Baseline Answer

Standard parametric language models, such as BERT, store world knowledge implicitly within the parameters of the underlying neural network [1]. This implicit storage makes it difficult to determine what knowledge is stored and where, and limits storage space to the size of the network, requiring increasingly larger networks to capture more facts [1].

In contrast, REALM (Retrieval-Augmented Language Model) differs in the following ways:

*   **Storage:** Instead of relying solely on parameters, REALM augments language model pre-training with a learned textual knowledge retriever that accesses a large external corpus, such as Wikipedia [1, 2].
*   **Access:** Before making a prediction, REALM uses the retriever to retrieve documents from the knowledge corpus and then attends over those documents to inform its prediction [2].
*   **Nature of Memory:** REALM's memories are "grounded," meaning each memory is associated with a specific document rather than unnamed value vectors [3]. This provides qualitative benefits such as increased modularity and interpretability [1, 2].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-15-e73576ceacc6e97a0666fd10

### Multi-Agent Answer

Standard parametric language models store world knowledge implicitly within the neural network's parameters [E2]. This method of implicit storage requires increasingly larger networks to cover more facts [E2].

In contrast, REALM (Retrieval-Augmented Language Model) augments language model pre-training with a learned textual knowledge retriever to capture knowledge in a more modular and interpretable way [E1, E2]. Rather than relying solely on internal parameters, REALM explicitly exposes the role of world knowledge by requiring the model to decide what to retrieve and use during inference [E1]. Specifically, the model uses the retriever to pull documents from a large corpus, such as Wikipedia, and then attends over those documents to inform its predictions [E1]. This ability to retrieve and attend over documents is utilized during pre-training, fine-tuning, and inference [E2].

Furthermore, REALM utilizes a grounded memory where each memory is associated with a specific document, rather than using unnamed value vectors [E7, E8].

### Metrics

- baseline_latency_seconds: 5.997
- orchestrator_latency_seconds: 72.103
- baseline_total_tokens: 8195
- orchestrator_total_tokens: 52331
- baseline_citation_count: 8
- orchestrator_evidence_count: 17
- fact_check_status_counts: {'supported': 6, 'unsupported': 2}

## Question 5

Type: method/mechanism

How does REALM's retrieve-then-predict framework work, including the role of the latent document variable z?

### Baseline Answer

REALM’s retrieve-then-predict framework decomposes the probability of an output $p(y|x)$ into two distinct steps:

1.  **Retrieve**: Given an input $x$, the model first retrieves potentially helpful documents $z$ from a knowledge corpus $Z$ by modeling them as a sample from the distribution $p(z|x)$ [3]. This is implemented using a neural knowledge retriever based on a dense inner product model [3].
2.  **Predict**: The model then conditions on both the retrieved document $z$ and the original input $x$ to generate the output $y$, modeled as $p(y|z, x)$ [3].

**The Role of the Latent Document Variable $z$**
The framework treats the retrieved document $z$ as a latent variable [3]. To obtain the overall likelihood of generating an output $y$ for a given input $x$, the model marginalizes over all possible documents $z$ in the corpus $Z$, expressed by the formula:
$p(y|x) = \sum_{z \in Z} p(y|z, x)p(z|x)$ [3].

By modeling the approach as a latent variable language model and optimizing the marginal likelihood, the retriever can be trained using a performance-based signal from unsupervised text [1]. This allows the model to be rewarded for retrieving informative documents that improve the language model's perplexity and penalized for uninformative retrievals [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952, chunk_index: 1
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7, chunk_index: 3

### Multi-Agent Answer

REALM (Retrieval-Augmented Language Model) employs a "retrieve-then-predict" framework that decomposes the generative process $p(y|x)$ into two distinct steps [E3]. This approach models the method as a latent variable language model and optimizes the marginal likelihood [E1].

In this framework, the process is broken down as follows:

*   **Retrieval Step:** The model uses a learned textual knowledge retriever to select potentially helpful documents $z$ from a large knowledge corpus $Z$, such as Wikipedia [E1, E2, E3]. The retriever is defined using a dense inner product model, where relevance is determined by the inner product of $d$-dimensional vector embeddings [E3].
*   **Prediction Step:** After retrieving documents, the language model attends over them to help inform its prediction of the output $y$, conditioned on both the input $x$ and the retrieved document $z$ [E1, E3].

The document $z$ serves as a latent variable [E1]. The overall likelihood of generating the output $y$ is calculated by treating $z$ as a latent variable and marginalizing over all possible documents in the corpus: $p(y |x) = \sum_{z \in Z} p(y |z, x) p(z |x)$ [E3].

### Metrics

- baseline_latency_seconds: 6.352
- orchestrator_latency_seconds: 80.264
- baseline_total_tokens: 8019
- orchestrator_total_tokens: 55977
- baseline_citation_count: 8
- orchestrator_evidence_count: 11
- fact_check_status_counts: {'supported': 8, 'unsupported': 1}

## Question 6

Type: method/mechanism

How does the paper train the retriever when the retrieved document is latent, and how does learning signal flow back to retrieval?

### Baseline Answer

The paper trains the retriever by modeling the "retrieve-then-predict" approach as a latent variable language model and optimizing the marginal likelihood [1]. Specifically, the model treats the retrieved document $z$ as a latent variable and marginalizes over all possible documents in the corpus $Z$ to obtain the overall likelihood of generating an output $y$ given an input $x$, expressed as $p(y|x) = \sum_{z \in Z} p(y|z, x) p(z|x)$ [4]. The training signal is performance-based and derived from unsupervised text, where retrieval that improves the language model's perplexity is rewarded and uninformative retrieval is penalized [1].

The learning signal flows back to the retrieval module through backpropagation [1, 2]. The gradient of the pre-training objective (the log-likelihood) with respect to the retriever's parameters $\theta$ is computed as:
$$\nabla \log p(y|x) = \sum_{z} [p(z|y, x) - p(z|x)] \nabla \log p(z|x)$$
This mathematical derivation shows that the gradient can be viewed as an expectation with respect to the conditional distribution $p(z|y, x)$ [6]. If a specific document $z^*$ allows for perfect prediction accuracy, the gradient descent on the REALM objective becomes equivalent to gradient descent on $\log p(z^*|x)$, similar to typical maximum likelihood training in supervised learning where $z^*$ is a "gold" document [6].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8

### Multi-Agent Answer

The REALM framework models the retrieve-then-predict process as a latent variable language model [E1]. To optimize this model, the overall likelihood of generating an output $y$ is obtained by treating the retrieved document $z$ as a latent variable and marginalizing over all possible documents in the corpus $Z$, which is expressed mathematically as $p(y |x) = \sum_{z \in Z} p(y |z, x) p(z |x)$ [E4].

The retriever is pre-trained in an unsupervised manner using masked language modeling (MLM) as the learning signal [E2]. The training intuition is based on a performance-based signal from unsupervised text: retrievals that improve the language model’s perplexity are rewarded, while uninformative retrievals are penalized [E1]. Learning the model end-to-end requires backpropagating through a retrieval step that considers an entire corpus of textual knowledge containing millions of documents [E1, E2].

### Metrics

- baseline_latency_seconds: 6.505
- orchestrator_latency_seconds: 40.575
- baseline_total_tokens: 7920
- orchestrator_total_tokens: 31002
- baseline_citation_count: 8
- orchestrator_evidence_count: 11
- fact_check_status_counts: {'supported': 5}

## Question 7

Type: method/mechanism / implementation

What approximations or engineering choices does REALM use to make retrieval over a large corpus practical during training and inference?

### Baseline Answer

To make retrieval over a large corpus practical during training and inference, REALM employs the following engineering choices and approximations:

*   **MIPS Formulation:** The selection of the best documents is formulated as a Maximum Inner Product Search (MIPS) [2].
*   **Caching and Asynchronous Updates:** The retriever is structured so that the computation performed for each document can be cached and updated asynchronously [2].
*   **Parallelized Indexing:** During pre-training, the document embedding step for the MIPS index is parallelized over 16 TPUs [4].
*   **Index Refresh Rate:** To manage the scale of the corpus, a parallel process is run to re-embed corpus documents and rebuild the MIPS index, resulting in one index refresh approximately every 500 training steps [5].
*   **Candidate Selection (Inference/Fine-tuning):** During fine-tuning inference, the system considers only the top-5 candidates [4]. This is noted as an improvement over other retrieval-based systems that often retrieve between 20 to 80 documents [1].
*   **Marginalization (Pre-training):** For each pre-training example, the model retrieves and marginalizes over 8 candidate documents, which includes a null document $\emptyset$ [4].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-11-3fa55fc3148d1188cb70ab91
[5] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-

### Multi-Agent Answer

To make retrieval over a large corpus practical, REALM employs the following engineering choices and approximations:

*   **Document Selection Formulation:** Document selection is formulated as a Maximum Inner Product Search (MIPS) [E1].
*   **Computational Efficiency:** The retriever is structured so that computation for each individual document can be cached and updated asynchronously [E1].
*   **Pre-training Marginalization:** During pre-training, the model performs marginalization over 8 candidate documents, which includes a null document [E3].
*   **Inference Constraints:** During fine-tuning inference, the model limits its consideration to the top-5 candidate documents [E3].

### Metrics

- baseline_latency_seconds: 6.298
- orchestrator_latency_seconds: 37.941
- baseline_total_tokens: 8702
- orchestrator_total_tokens: 30832
- baseline_citation_count: 8
- orchestrator_evidence_count: 13
- fact_check_status_counts: {'supported': 4}

## Question 8

Type: comparison

How does REALM compare with ORQA or other open-domain QA baselines, and what evidence supports that comparison?

### Baseline Answer

REALM compares to other open-domain QA baselines in the following ways:

**Comparison with ORQA**
* **Direct Comparison:** ORQA is considered the most direct comparison to REALM because both systems use an identical fine-tuning setup, hyperparameters, and training data [1]. Additionally, the retrievers for both REALM pre-training and ORQA are initialized using the Inverse Cloze Task (ICT) [2].
* **Key Differences:** While ORQA formulates Open-QA using a similar latent variable model to REALM and maximizes marginal likelihood, REALM introduces a novel language model pre-training step and backpropagates into the MIPS index instead of using a fixed index [7].
* **Performance Evidence:** The improvement of REALM over ORQA is attributed purely to better pre-training methods [1]. If the parameters for both the encoder and retriever are reset to their baseline state, the system reduces to the main baseline, ORQA [5].

**Comparison with Other Baselines**
* **Retrieval-based Systems:** Compared to other retrieval-based systems (such as DrQA, HardEM, GraphRetriever, and PathRetriever) which often retrieve between 20 to 80 documents, REALM achieves the overall best performance while only retrieving 5 documents [1, 7].
* **Generation-based Systems:** REALM compares against state-of-the-art generation-based systems, specifically a version of T5 that was fine-tuned for Open-QA [4].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-10-8ea61faa3a17c1fc8f8725d8
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7

### Multi-Agent Answer

REALM achieves new state-of-the-art results on three Open-domain Question Answering (Open-QA) benchmarks [E3, E6]. It significantly outperforms all previous systems by 4-16% absolute accuracy [E3, E6].

Compared to other retrieval-based systems, REALM achieves its best overall performance while retrieving fewer documents [E1]. Specifically, REALM retrieves 5 documents to achieve its performance, whereas other retrieval-based systems typically retrieve between 20 and 80 documents [E1].

ORQA is the most direct comparison to REALM because the fine-tuning setup, hyperparameters, and training data are identical [E1]. To enable this direct comparison, all hyperparameters from Lee et al. (2019) were reused [E2]. The improvement of REALM over ORQA is attributed purely to better pre-training methods [E1]. Additionally, the retrievers for both REALM pre-training and ORQA are initialized using the Inverse Cloze Task [E2].

### Metrics

- baseline_latency_seconds: 6.580
- orchestrator_latency_seconds: 80.491
- baseline_total_tokens: 7685
- orchestrator_total_tokens: 52393
- baseline_citation_count: 8
- orchestrator_evidence_count: 16
- fact_check_status_counts: {'unsupported': 2, 'supported': 6}

## Question 9

Type: comparison

How does REALM's retrieval-based approach compare with storing knowledge only in model parameters?

### Baseline Answer

REALM's retrieval-based approach differs from models that store knowledge only in parameters in the following ways:

*   **Interpretability and Modularity:** Unlike models that store knowledge implicitly in their parameters, REALM captures knowledge in a more modular and interpretable way [1, 3]. Its memories are "grounded," meaning each memory is associated with a specific document rather than unnamed value vectors, which provides provenance for predicted answers [6].
*   **Explicit Knowledge Role:** REALM explicitly exposes the role of world knowledge by requiring the model to decide what knowledge to retrieve and use during inference [1].
*   **Scalability of Knowledge:** In models where knowledge is stored implicitly in parameters, the storage space is limited by the size of the network; capturing more knowledge requires training increasingly larger networks, which can be expensive or prohibitively slow [3].
*   **Adaptability:** REALM can adapt to updated knowledge corpora [8]. For example, a model pre-trained on a 2018 corpus can retrieve documents from an updated 2020 corpus to generate correct tokens for information that was not present in the original training data [8].

Citations:
[1] data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[3] data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[6] data/2002.08909v1.pdf, chunk_id: 2002.08909v1-14-83fbe5c3ec4e1ed386558b56
[8] data/2002.08909v1.pdf, chunk_id: 2002.08909v1-20-58cd33db77feaae8a3f8d036

### Multi-Agent Answer

Standard language model pre-training stores knowledge implicitly in the parameters of a neural network [E8]. This implicit storage makes it difficult to determine what knowledge is stored or where it is located, and it requires ever-larger, expensive networks to cover more facts [E8].

In contrast, REALM (Retrieval-Augmented Language Model) augments pre-training with a learned textual knowledge retriever to capture knowledge in a more modular and interpretable way [E2, E8]. This approach explicitly exposes the role of world knowledge by requiring the model to decide what knowledge to retrieve and use during inference [E2].

A key difference is that REALM's memories are "grounded," meaning each memory is associated with a specific document rather than unnamed value vectors [E6, E7]. This grounding provides interpretability and provenance, which is essential for Open-domain Question Answering (Open-QA) applications to ensure that predicted answers are trustworthy [E6, E7]. Additionally, REALM outperforms previous state-of-the-art methods for both explicit and implicit knowledge storage on three popular Open-QA benchmarks [E8].

### Metrics

- baseline_latency_seconds: 6.939
- orchestrator_latency_seconds: 77.239
- baseline_total_tokens: 7839
- orchestrator_total_tokens: 51700
- baseline_citation_count: 8
- orchestrator_evidence_count: 12
- fact_check_status_counts: {'supported': 4, 'unsupported': 2}

## Question 10

Type: evidence synthesis / ablation

What ablation or diagnostic evidence shows that retrieval pre-training improves REALM rather than only the reader component?

### Baseline Answer

To determine whether REALM pre-training improves the retriever, the encoder, or both, researchers performed an ablation study where they reset the parameters of either the retriever or the encoder to their baseline state before fine-tuning [4].

The evidence provided includes:

*   **Component Analysis:** Testing revealed that both the encoder and the retriever benefit from REALM training separately, though the best results are achieved when both components act in unison [4].
*   **Retrieval Performance Metric:** To more significantly isolate the contribution of improving the retriever during pre-training, the researchers reported how often the gold answer appears in the top-5 retrievals before applying any fine-tuning [1, 4]. 
*   **Ablation Results:** In ablation experiments on the NaturalQuestions-Open development set, the "Baseline retriever + REALM encoder" (which resets the retriever) resulted in a zero-shot retrieval recall of 13.9 [8], whereas the full REALM model achieved a zero-shot retrieval recall of 38.5 [8].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e
[8] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-11-3fa55fc3148d1188cb70ab91

### Multi-Agent Answer

Ablation and diagnostic evidence regarding the benefits of REALM's components include:

* **Component Contributions:** Both the retriever and the encoder benefit separately from REALM training, although optimal results require both components to act in unison [E9].
* **Ablation Results:** Resetting both the retriever and the encoder reduces the system to the main baseline, ORQA [E9].
* **Diagnostic Metrics:** To isolate the specific contribution of improving the retriever during pre-training, the model reports how often the gold answer appears in the top-5 retrievals before any fine-tuning [E9].

### Metrics

- baseline_latency_seconds: 5.973
- orchestrator_latency_seconds: 35.027
- baseline_total_tokens: 7920
- orchestrator_total_tokens: 28910
- baseline_citation_count: 8
- orchestrator_evidence_count: 13
- fact_check_status_counts: {'supported': 3}

## Question 11

Type: evidence synthesis

Synthesize the evidence for why REALM improves open-domain QA performance, including retrieval quality, pre-training, and downstream fine-tuning.

### Baseline Answer

REALM improves open-domain question answering (Open-QA) performance through the following mechanisms:

*   **Pre-training:** The improvement of REALM over the ORQA baseline is attributed purely to its better pre-training methods [1]. REALM uses a masked language modeling (MLM) task as a learning signal during pre-training [4]. This unsupervised pre-training allows the model to learn to retrieve helpful documents by rewarding retrievals that improve the language model's perplexity [5]. This method has been shown to work in both single-corpus (Wikipedia) and separate-corpus (CC-News and Wikipedia) settings [1].
*   **Retrieval Quality:** Unlike prior systems that often retrieve between 20 to 80 documents, REALM achieves the best overall performance while only retrieving 5 documents [1]. The REALM pre-training process improves both the retriever and the encoder, though the best results require both components to act in unison [8]. Furthermore, the pre-training process enables the retriever to find relevant documents even when trained with unsupervised text only [8].
*   **Downstream Fine-tuning:** REALM is designed so that its retriever can transfer to other tasks because it retrieves raw text rather than labeled examples [5]. When fine-tuned on Open-QA benchmarks, REALM outperforms previous state-of-the-art methods by a margin of 4-16% in absolute accuracy [4, 5]. Notably, REALM outperforms the largest T5-11B model while being 30 times smaller [4].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[5] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9

### Multi-Agent Answer

REALM improves open-domain question answering (Open-QA) performance through a specialized pre-training framework that augments language model pre-training with a learned textual knowledge retriever [E2, E6]. This approach captures knowledge in a more modular and interpretable way compared to traditional models that store world knowledge implicitly within neural network parameters [E2, E6].

**Retrieval Quality and Mechanism**
REALM's retriever is designed to transfer to other tasks because it retrieves raw text rather than labeled examples [E2]. The system utilizes a dense inner product model, where relevance is determined by the inner product of $d$-dimensional vector embeddings [E3]. To handle the computational challenge of selecting from millions of candidate documents, the retriever employs cached computation and Maximum Inner Product Search (MIPS) [E2]. To ensure stable optimization during training, the system implements asynchronous MIPS refreshes by running a primary trainer job and a secondary index builder job in parallel [E8].

**Pre-training Improvements**
The performance improvement of REALM over systems such as ORQA is attributed purely to its superior pre-training methods [E1, E4]. The retriever is trained using a performance-based signal from unsupervised text, where retrievals that improve the language model's perplexity are rewarded [E2]. Specifically, the training gradient encourages the retriever to increase the relevance score for documents that perform better than expected, defined as $p(y |z, x) > p(y |x)$ [E8]. Additionally, REALM employs a "salient span masking" scheme—masking entities or dates—to focus the model on problems requiring world knowledge rather than local context [E8]. Both the encoder and the retriever benefit individually from REALM training, though optimal results are achieved when both components act in unison [E5].

**Downstream Fine-tuning**
For the fine-tuning task of Open-QA, the input is a question and the output is the answer [E3]. During fine-tuning inference, the model considers the top-5 candidates [E4, E7]. REALM achieves state-of-the-art results, outperforming previous systems by 4-16% absolute accuracy across benchmarks such as Natural Questions, Web Questions, and Curated TREC [E2, E6]. Notably, REALM outperforms the significantly larger T5-11B model while being 30 times smaller [E4].

### Metrics

- baseline_latency_seconds: 6.682
- orchestrator_latency_seconds: 91.246
- baseline_total_tokens: 8205
- orchestrator_total_tokens: 57247
- baseline_citation_count: 8
- orchestrator_evidence_count: 15
- fact_check_status_counts: {'unsupported': 5, 'supported': 7}

## Question 12

Type: multi-step reasoning

Explain step by step how a masked-language-model pre-training objective can improve downstream open-domain QA in REALM.

### Baseline Answer

In REALM, a masked-language-model (MLM) pre-training objective improves downstream open-domain question answering (Open-QA) through the following steps:

1.  **Unsupervised Pre-training with Latent Retrieval:** During pre-training, the model is given an input $x$, which is a sentence from an unlabeled corpus $X$ with certain tokens masked out [1, 3]. The model's goal is to predict these missing tokens $y$ [3]. REALM decomposes this process into a "retrieve-then-predict" generative process: first, it retrieves potentially helpful documents $z$ from a large knowledge corpus $Z$ (such as Wikipedia) [2, 3].
2.  **Learning via Performance-Based Signals:** The retriever is trained using a performance-based signal from this unsupervised text [2]. Specifically, the training process rewards the retriever if it selects documents that improve the language model's ability to predict the masked tokens (improving perplexity) and penalizes it for uninformative retrievals [2].
3.  **End-to-End Optimization:** The model is optimized by maximizing the marginal likelihood of the correct output $y$ [3]. Because both the knowledge retriever and the knowledge-augmented encoder are differentiable neural networks, the signal from the MLM objective can be backpropagated all the way through the retrieval step [2]. This allows the retriever to be learned in an unsupervised manner [2].
4.  **Transfer to Open-QA:** After pre-training, the parameters of the retriever and the encoder are fine-tuned on the supervised Open-QA task, where $x$ is a question and $y$ is the answer [2, 3]. Because the retriever was trained to find documents that provide the necessary information to complete a sentence, it can transfer this ability to finding documents that contain answers to questions [2].

**Citations**
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-2-7f240c64641ad3f52fc62e97
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268

### Multi-Agent Answer

In REALM, a masked-language-model (MLM) pre-training objective improves downstream open-domain question answering (Open-QA) through the following process:

1.  **Learning Representations via MLM:** The primary goal of language model pre-training is to learn useful representations of language from unlabeled text corpora [E2]. A successful MLM must learn to encode syntactic information, semantic information, and world knowledge [E2].
2.  **Unsupervised Retriever Training:** REALM augments this pre-training by adding a latent knowledge retriever [E3]. This retriever is trained in an unsupervised manner, using the MLM objective as a learning signal [E3]. The retriever is rewarded when a retrieval improves the language model's perplexity and is penalized when a retrieval is uninformative [E6].
3.  **Backpropagation through Retrieval:** The signal from the language modeling objective is backpropagated through a retrieval step that can consider millions of documents [E3]. This process allows the model to learn to retrieve and attend over documents from a large corpus to help inform its predictions [E3].
4.  **Improving Answer Probability:** By retrieving documents that contain related facts, the model can increase the marginal probability of the correct answer [E4]. For example, while a standard BERT model might assign an extremely low probability to a specific answer, REALM can achieve a significantly higher marginal probability by marginalizing over retrieved documents [E4].

### Metrics

- baseline_latency_seconds: 6.662
- orchestrator_latency_seconds: 84.889
- baseline_total_tokens: 9087
- orchestrator_total_tokens: 56285
- baseline_citation_count: 8
- orchestrator_evidence_count: 14
- fact_check_status_counts: {'unsupported': 4, 'supported': 8}

## Question 13

Type: multi-step reasoning / error analysis

If REALM retrieves an irrelevant document, how would that affect p(z|x), p(y|z,x), and the final answer prediction?

### Baseline Answer

If REALM retrieves an irrelevant document $z$, the effects are as follows:

*   **$p(z|x)$**: The retriever models this distribution [3]. If the document is irrelevant, it implies the retriever has sampled a $z$ that may not be helpful for the input $x$ [1].
*   **$p(y|z,x)$**: This represents the probability of the output $y$ conditioned on both the input $x$ and the retrieved document $z$ [3]. If $z$ is irrelevant, it may be less useful for predicting $y$ than a null document $\emptyset$ [1].
*   **Final answer prediction ($p(y|x)$)**: The overall likelihood is obtained by marginalizing over all possible documents $z$ using the formula $p(y|x) = \sum_{z \in Z} p(y|z, x)p(z|x)$ [3]. While retrieving relevant documents can dramatically increase the marginalized probability of a correct answer, an uninformative retrieval is penalized during training [2, 4].

Additionally, the "Retrieval Utility" (RU) can be used to measure this impact; a negative RU indicates that the retrieved document $z$ is less useful for predicting $y$ than the null document $\emptyset$ [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-20-58cd33db77feaae8a3f8d036, chunk_index: 20
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e, chunk_index: 13
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7, chunk_index: 3
[4] source: data/20

### Multi-Agent Answer

The provided evidence does not contain a specific mathematical description of how $p(z|x)$ and $p(y|z,x)$ change when an irrelevant document is retrieved, nor does it explicitly state how these changes affect the final answer prediction.

However, the evidence provides the following related information regarding retrieval utility and irrelevance:

*   **Retrieval Utility (RU) Definition:** RU is defined as the difference between the log-likelihood of the target $y$ given the document $z$ and input $x$, and the log-likelihood of the target given only the input: $\text{RU} = \log p(y | z, x) - \log p(y | \emptyset, x)$ [E1].
*   **Implications of Irrelevance:** A negative RU indicates that the retrieved document $z$ is less useful for predicting $y$ than a null document [E1]. This negative utility may imply that the document $z$ is irrelevant to $x$ [E1].

### Metrics

- baseline_latency_seconds: 6.773
- orchestrator_latency_seconds: 74.972
- baseline_total_tokens: 8309
- orchestrator_total_tokens: 49230
- baseline_citation_count: 8
- orchestrator_evidence_count: 12
- fact_check_status_counts: {'unsupported': 1, 'supported': 3}

## Question 14

Type: limitation/uncertainty

What limitations, uncertainties, or missing comparisons should be noted when interpreting REALM's reported results?

### Baseline Answer

When interpreting REALM's reported results, the following limitations, uncertainties, or missing comparisons should be noted:

*   **Data Usage:** Certain types of data could potentially benefit REALM but were not utilized in the experiments [1].
*   **Index Staleness:** The results suggest that using a stale MIPS index can hurt model training, and the authors note that further reducing this staleness might offer better optimization [4].
*   **Uncertainty in Retrieval Utility (RU):** A negative RU indicates that a document $z$ is less useful for predicting $y$ than a null document; however, this could mean the document is irrelevant to $x$, or it could mean the masked tokens in $x$ do not require world knowledge, or that the required knowledge is already sufficiently "baked into" the model's parameters [2].
*   **Comparison Contexts:** 
    *   While REALM is compared to ORQA (where hyperparameters, fine-tuning setup, and training data are identical), the improvement of REALM over ORQA is attributed purely to better pre-training methods [1].
    *   In the context of generation-based models, while T5 was used as a baseline, the text notes that T5 only experimented on reading comprehension tasks where a context document is provided [6].
*   **Future Generalizations:** The current work is described as a "minimal instantiation," implying that results may differ when generalized to structured knowledge, multi-lingual settings, or multi-modal settings (such as images or videos) [5].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-20-58cd33db77feaae8a3f8d036
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a6

### Multi-Agent Answer

When interpreting REALM's reported results, several limitations, uncertainties, and missing comparisons should be noted:

*   **Potential for Trivial Retrieval:** If the pre-training corpus and the knowledge corpus are identical, the model may engage in trivial retrieval, where it predicts the output by looking at the unmasked version of the input sentence within the corpus [E4].
*   **Knowledge Persistence in Parameters:** Although REALM can adapt to new world knowledge by modifying corpus documents, the knowledge-augmented encoder may still retain old knowledge because information can be "baked into the model's parameters" [E6].
*   **Experimental Data Limitations:** The researchers noted that certain types of data could potentially benefit REALM, but such data was not used in their experiments [E1].
*   **Comparison to Generative Approaches:** While generation-based Open-QA is described as an emerging alternative approach that models the task as a sequence prediction task [E9], the provided evidence does not include a direct performance comparison between REALM and these generative models [E9].

### Metrics

- baseline_latency_seconds: 6.166
- orchestrator_latency_seconds: 40.770
- baseline_total_tokens: 7497
- orchestrator_total_tokens: 29841
- baseline_citation_count: 8
- orchestrator_evidence_count: 9
- fact_check_status_counts: {'supported': 5}

## Question 15

Type: citation grounding / uncertainty

Which claims about REALM's performance or mechanism cannot be verified unless the answer cites specific experimental evidence from the paper?

### Baseline Answer

Based on the provided text, the following claims about REALM's performance or mechanism require specific experimental evidence from the paper for verification:

*   **Performance relative to ORQA:** The claim that the improvement of REALM over ORQA is "purely due to better pre-training methods" [1].
*   **Performance relative to other retrieval-based systems:** The claim that REALM "gets the overall best performance while only retrieving 5 documents" compared to other retrieval-based systems that "often retrieve from 20 to 80 documents" [1].
*   **Impact of components (Encoder vs. Retriever):** The claim that "both the encoder and retriever benefit from REALM training separately, but the best result requires both components acting in unison" [4].
*   **Effectiveness of masking schemes:** The claim that salient span masking is "crucial for REALM," whereas it has not been shown to be impactful in previous work with standard BERT training [4].
*   **Impact of index refresh rates:** The claim that "a stale index can hurt model training" and that reducing staleness could offer "better optimization" [4].
*   **Effect of retrieval on masked token prediction:** The claim that REALM is able to "retrieve document to fill in the masked word even though it is trained with unsupervised text only" [4].
*   **Predictive value of Retrieval Utility (RU):** The claim that RU is "more predictive of good performance on the downstream task of Open-QA than even the overall log-likelihood" [3].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-20-58cd33db77feaae8a3f8d036
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb4354

### Multi-Agent Answer

Based on the provided evidence notes, the following claims about REALM's performance or mechanism cannot be fully verified without citing specific experimental data or values that are missing from the summaries:

*   **The exact magnitude of REALM's improvement over ORQA:** While it is stated that the improvement of REALM over ORQA is purely due to better pre-training methods because fine-tuning setups, hyperparameters, and training data are identical [E1, E5], the provided notes do not explicitly summarize the exact percentage of improvement as a single value, although specific benchmark scores for both models are provided [E5].
*   **The quantitative performance gain of salient span masking:** The notes claim that salient span masking is crucial and outperforms other masking strategies, such as random token masking or random span masking [E3, E4], but the provided summaries do not include the specific numerical data from the ablation studies required to quantify the exact performance gain [E3].
*   **The specific metrics used to measure optimization stability:** It is claimed that implementing asynchronous MIPS refreshes leads to stable optimization, provided refreshes occur at a sufficiently frequent rate [E4]. However, the evidence does not include the specific experimental metrics or comparative data used to measure this stability [E4].

### Metrics

- baseline_latency_seconds: 6.350
- orchestrator_latency_seconds: 62.453
- baseline_total_tokens: 7930
- orchestrator_total_tokens: 57733
- baseline_citation_count: 8
- orchestrator_evidence_count: 12
- fact_check_status_counts: {'supported': 6}
