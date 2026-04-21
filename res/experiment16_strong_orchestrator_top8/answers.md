# experiment16: retrieval sweep, strong orchestrator only, top_k=8

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

REALM retrieves from a large textual knowledge corpus, such as Wikipedia [1, 2].

The model uses this external knowledge through a "retrieve-then-predict" process:
*   **Retrieval:** Given an input $x$, the model uses a learned textual knowledge retriever to retrieve potentially helpful documents $z$ from the corpus $Z$ [1, 3]. This is modeled as a sample from the distribution $p(z | x)$ [3].
*   **Prediction:** The model then conditions on both the retrieved documents $z$ and the original input $x$ to generate the output $y$, modeled as $p(y | z, x)$ [3]. 

During pre-training and inference, the language model attends over these retrieved documents to help inform its predictions [1]. The framework treats the retrieved document as a latent variable and optimizes the marginal likelihood [1, 3].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7

### Multi-Agent Answer

REALM retrieves documents from a large knowledge corpus, such as Wikipedia [E2, E3]. The model's approach can be applied in a single-corpus setting where both the input and the knowledge corpus are Wikipedia, or in a separate-corpus setting where the input is CC-News and the knowledge corpus is Wikipedia [E4].

The model decomposes the generative process of an output $y$ given an input $x$ into two distinct steps: first, retrieving a document $z$ from a knowledge corpus $Z$ via $p(z |x)$, and second, predicting the output $y$ via $p(y |z, x)$ [E1]. To manage the computational scale of considering millions of documents, the retriever utilizes Maximum Inner Product Search (MIPS) for document selection [E2]. Specifically, a dense inner product model determines relevance scores using the inner product of $d$-dimensional vector embeddings [E1].

Before making a prediction, the language model uses the retriever to retrieve documents and then attends over those documents to help inform its prediction [E2]. During fine-tuning inference, the system considers the top-5 candidates [E7].

### Metrics

- baseline_latency_seconds: 7.453
- orchestrator_latency_seconds: 80.909
- baseline_total_tokens: 8631
- orchestrator_total_tokens: 55522
- baseline_citation_count: 8
- orchestrator_evidence_count: 9
- fact_check_status_counts: {'unsupported': 1, 'supported': 6}

## Question 2

Type: easy lookup

Which downstream tasks or benchmarks does the paper use to evaluate REALM?

### Baseline Answer

To evaluate REALM, the paper uses the following Open-QA benchmarks:

*   **NQ** (NaturalQuestions) [6]
*   **WQ** (WebQuestions) [6]
*   **CT** (TriviaQA) [6]

Additionally, the paper presents ablation experiments specifically on the **NaturalQuestions-Open** (NQ's development set) dataset [1, 6, 7].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05, chunk_index: 12
[6] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-11-3fa55fc3148d1188cb70ab91, chunk_index: 11
[7] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e, chunk_index: 13

### Multi-Agent Answer

The paper evaluates REALM using three Open-domain Question Answering (Open-QA) benchmarks [E5]:

*   **Natural Questions (NQ):** REALM achieves an exact match score of 39.2 when using Wikipedia as the corpus (X=Wikipedia) and 40.4 when using CC-News (X=CC-News) [E9].
*   **Web Questions (WQ):** REALM achieves an exact match score of 40.2 (X=Wikipedia) and 40.7 (X=CC-News) [E9].
*   **Curated TREC (CT):** REALM achieves an exact match score of 46.8 (X=Wikipedia) and 42.9 (X=CC-News) [E9].

### Metrics

- baseline_latency_seconds: 6.413
- orchestrator_latency_seconds: 41.065
- baseline_total_tokens: 8193
- orchestrator_total_tokens: 30182
- baseline_citation_count: 8
- orchestrator_evidence_count: 10
- fact_check_status_counts: {'supported': 5}

## Question 3

Type: definition

What is REALM, and what does the paper mean by retrieval-augmented language model pre-training?

### Baseline Answer

REALM stands for Retrieval-Augmented Language Model pre-training [1]. It is a novel framework designed to capture knowledge in a more modular and interpretable way [1, 2]. Unlike traditional models that store world knowledge implicitly within their parameters [2], REALM augments language model pre-training algorithms with a learned textual knowledge retriever [1]. This allows the model to explicitly decide what knowledge to retrieve and attend over documents from a large corpus, such as Wikipedia, to inform its predictions [1].

In this paper, retrieval-augmented language model pre-training refers to a process where:
*   **The mechanism:** The model decomposes the task into a "retrieve-then-predict" generative process [3]. Given an input $x$, it first retrieves potentially helpful documents $z$ from a knowledge corpus $Z$ (modeled as a sample from the distribution $p(z|x)$) and then conditions on both the retrieved documents and the original input to generate an output $y$ (modeled as $p(y|z, x)$) [3].
*   **The pre-training task:** For pre-training specifically, the task is masked language modeling, where the model must predict the value of masked tokens in a sentence from a pre-training corpus [3].
*   **The learning signal:** The retriever is trained in an unsupervised manner using a performance-based signal: retrieval that improves the language model's perplexity is rewarded, while uninformative retrieval is penalized [1]. This is achieved by modeling the approach as a latent variable language model and optimizing the marginal likelihood [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3

### Multi-Agent Answer

REALM (Retrieval-Augmented Language Model) is a framework that augments language model pre-training with a latent knowledge retriever [E1]. This framework allows a model to retrieve and attend over documents from a large corpus, such as Wikipedia, during pre-training, fine-tuning, and inference [E1]. Unlike traditional language models that store world knowledge implicitly in neural network parameters—a process that requires increasingly larger networks to cover more facts—REALM captures knowledge in a more modular and interpretable way [E1]. This approach provides qualitative benefits, such as modularity and interpretability, because its memories are "grounded," meaning each memory is associated with a specific document rather than unnamed value vectors [E7].

In the context of this paper, retrieval-augmented language model pre-training refers to extending the retrieval-based paradigm to the language model pre-training stage [E8]. This process decomposes the probability of an output $p(y | x)$ into a two-step process: first, retrieving potentially helpful documents $z$ from a knowledge corpus $Z$, and second, predicting the output $y$ conditioned on both the input $x$ and the retrieved $z$ [E8]. For the pre-training task specifically, the model uses masked language modeling as the learning signal to allow for unsupervised pre-training of the knowledge retriever [E1].

### Metrics

- baseline_latency_seconds: 8.629
- orchestrator_latency_seconds: 76.878
- baseline_total_tokens: 9006
- orchestrator_total_tokens: 53827
- baseline_citation_count: 8
- orchestrator_evidence_count: 14
- fact_check_status_counts: {'supported': 6}

## Question 4

Type: definition

How does REALM differ from a standard parametric language model such as BERT in where knowledge is stored and accessed?

### Baseline Answer

Standard parametric language models, such as BERT, store world knowledge implicitly within the parameters of the underlying neural network [1]. This implicit storage makes it difficult to determine exactly what knowledge is stored and where it is located; furthermore, the storage space for such knowledge is limited by the size of the network [1].

In contrast, REALM differs in the following ways:

*   **Storage:** Instead of relying solely on parameters, REALM augments language model pre-training with a learned textual knowledge retriever that accesses a large knowledge corpus, such as Wikipedia [1, 2]. This allows knowledge to be captured in a more modular and interpretable way [1, 2].
*   **Access:** Before making a prediction, the REALM model uses its retriever to retrieve documents from the knowledge corpus and then attends over those documents to inform its prediction [2].
*   **Interpretability:** Because REALM's "memories" are grounded—meaning each memory is associated with a specific document rather than unnamed value vectors—it provides a higher level of interpretability [3].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-14-83fbe5c3ec4e1ed386558b56

### Multi-Agent Answer

Standard parametric language models store world knowledge implicitly within their neural network parameters [E5]. This implicit storage method requires increasingly larger networks to cover more facts [E5].

In contrast, REALM (Retrieval-Augmented Language Model) captures knowledge in a more modular and interpretable way by using a learned textual knowledge retriever [E2, E5]. Rather than relying solely on internal parameters, REALM allows the model to retrieve and attend over documents from a large corpus, such as Wikipedia, during pre-training, fine-tuning, and inference [E2, E5]. 

The REALM process is decomposed into two specific steps: first, retrieving potentially helpful documents from a corpus, and second, conditioning on both the input and the retrieved documents to generate an output [E3]. During inference, REALM explicitly exposes the role of world knowledge by requiring the model to decide what knowledge to retrieve and use to inform its predictions [E2].

### Metrics

- baseline_latency_seconds: 5.571
- orchestrator_latency_seconds: 79.952
- baseline_total_tokens: 8202
- orchestrator_total_tokens: 57056
- baseline_citation_count: 8
- orchestrator_evidence_count: 14
- fact_check_status_counts: {'supported': 4, 'unsupported': 2}

## Question 5

Type: method/mechanism

How does REALM's retrieve-then-predict framework work, including the role of the latent document variable z?

### Baseline Answer

REALM's retrieve-then-predict framework decomposes the probability of an output $p(y|x)$ into two distinct steps [3]:

1.  **Retrieve:** Given an input $x$, the model first retrieves potentially helpful documents $z$ from a knowledge corpus $Z$ [3]. This is modeled as a sample from the distribution $p(z|x)$ [3].
2.  **Predict:** The model then conditions on both the retrieved document $z$ and the original input $x$ to generate the output $y$, modeled as $p(y|z, x)$ [3].

**Role of the latent document variable $z$**
The framework treats $z$ as a latent variable and marginalizes over all possible documents in the corpus to obtain the overall likelihood of generating $y$ [3]. This process is expressed mathematically as:
$$p(y|x) = \sum_{z \in Z} p(y|z, x) p(z|x)$$ [3].

The framework is optimized by maximizing this marginal likelihood [1]. By treating $z$ as a latent variable, the model can be trained end-to-end, allowing the language modeling objective to backpropagate through the retrieval step [1].

Citations:
[1] data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[3] data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7

### Multi-Agent Answer

The REALM (Retrieval-Augmented Language Model) framework operates as a retrieve-then-predict method that decomposes the generative process $p(y|x)$ into two distinct steps [E3]. First, the model uses a retriever to retrieve documents $z$ from a large corpus $Z$ [E3]. Second, the language model attends over those retrieved documents to help inform its prediction [E1, E2].

The role of the latent document variable $z$ is central to this framework [E3]. REALM models the probability $p(y|x)$ by treating the retrieved document $z$ as a latent variable and marginalizing over the knowledge corpus $Z$ [E3]. This mathematical relationship is expressed as $p(y |x) = \sum_{z \in Z} p(y |z, x) p(z |x)$ [E3]. By using a latent knowledge retriever, REALM can capture knowledge in a way that is both modular and interpretable [E2].

### Metrics

- baseline_latency_seconds: 5.335
- orchestrator_latency_seconds: 82.485
- baseline_total_tokens: 7955
- orchestrator_total_tokens: 57250
- baseline_citation_count: 8
- orchestrator_evidence_count: 11
- fact_check_status_counts: {'supported': 7, 'unsupported': 1}

## Question 6

Type: method/mechanism

How does the paper train the retriever when the retrieved document is latent, and how does learning signal flow back to retrieval?

### Baseline Answer

To train the retriever when the retrieved document is a latent variable, REALM models the "retrieve-then-predict" approach as a latent variable language model and optimizes the marginal likelihood [1]. Specifically, the model decomposes the probability of generating an output $y$ from an input $x$, $p(y|x)$, by treating the document $z$ as a latent variable and marginalizing over all possible documents $z$ in the knowledge corpus $Z$:

$p(y |x) = \sum_{z \in Z} p(y |z, x) p(z |x)$ [4].

The learning signal flows back to the retrieval module through backpropagation. The gradient of the log-likelihood of the pre-training objective with respect to the retriever parameters $\theta$ is calculated as an expectation with respect to $p(z|y, x)$ [6]. This mathematical derivation shows that the gradient can be expressed as:

$\nabla \log p(y|x) = \sum_{z} [p(z|y, x) - p(z|x)] \nabla f(x, z)$ [6].

Under the specific setting where a single "gold" document $z^*$ leads to perfect prediction accuracy while all other documents result in zero accuracy, the gradient descent on the REALM objective becomes equivalent to gradient descent on the log-likelihood of that gold document, $\nabla \log p(z^*|x)$ [6]. This connects the unsupervised pre-training approach to the typical maximum likelihood training objective used in supervised learning [6].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952, chunk_index: 1
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7, chunk_index: 3
[6] source: data/2002.08909v1.pdf, chunk_id: 2002.08

### Multi-Agent Answer

The REALM framework models the retrieve-then-predict method as a latent variable language model [E1]. In this approach, the overall likelihood of generating an output $y$ is calculated by treating the retrieved document $z$ as a latent variable and marginalizing over all possible documents in the corpus $Z$, formulated as $p(y |x) = \sum_{z \in Z} p(y |z, x) p(z |x)$ [E4].

The retriever is trained using a performance-based signal derived from unsupervised text [E1]. Specifically, a retrieval that improves the language model’s perplexity is considered helpful and rewarded, while uninformative retrievals are penalized [E1]. The signal from the language modeling objective backpropagates through the retrieval step [E2]. This process enables learning the model end-to-end, even as the retrieval step considers an entire corpus of textual knowledge [E1].

### Metrics

- baseline_latency_seconds: 6.878
- orchestrator_latency_seconds: 39.517
- baseline_total_tokens: 7920
- orchestrator_total_tokens: 30752
- baseline_citation_count: 8
- orchestrator_evidence_count: 13
- fact_check_status_counts: {'supported': 6}

## Question 7

Type: method/mechanism / implementation

What approximations or engineering choices does REALM use to make retrieval over a large corpus practical during training and inference?

### Baseline Answer

To make retrieval over a large corpus practical during training and inference, REALM employs the following engineering choices and approximations:

*   **MIPS Formulation:** The selection of the best documents is formulated as a Maximum Inner Product Search (MIPS) [2].
*   **Caching and Asynchronous Updates:** The retriever is structured so that the computations performed for each individual document can be cached and updated asynchronously [2].
*   **Parallelized Indexing:** During pre-training, the document embedding step for the MIPS index is parallelized over 16 TPUs [4].
*   **Index Refreshing:** To manage the index during pre-training, REALM runs a parallel process to re-embed corpus documents and rebuild the MIPS index, resulting in an index refresh approximately every 500 training steps [5].
*   **Candidate Sampling:** During pre-training, the model retrieves and marginalizes over 8 candidate documents, which includes a null document [4]. During fine-tuning inference, the system considers the top-5 candidates [4].

Citations:
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-11-3fa55fc3148d1188cb70ab91
[5] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e

### Multi-Agent Answer

To make retrieval over a large corpus practical during training and inference, REALM employs several engineering choices and approximations:

*   **MIPS Formulation and Caching:** Document selection is formulated as a Maximum Inner Product Search (MIPS) [E1]. To manage computational challenges, the retriever is structured so that computation for each document can be cached and updated asynchronously [E1].
*   **Scalable Indexing:** The system utilizes a document index that functions as a scalable, grounded neural memory where the keys are document embeddings [E10]. This approach enables sub-linear memory access, similar to the functionality seen in product key memory [E10].
*   **Index Management:** The MIPS index is refreshed approximately once every 500 training steps [E9].
*   **Retrieval Limits:** During fine-tuning inference, the model considers only the top-5 candidate documents [E4]. It has been noted that REALM can achieve its best overall performance by retrieving as few as 5 documents [E2].

### Metrics

- baseline_latency_seconds: 6.321
- orchestrator_latency_seconds: 39.295
- baseline_total_tokens: 8612
- orchestrator_total_tokens: 31118
- baseline_citation_count: 8
- orchestrator_evidence_count: 10
- fact_check_status_counts: {'supported': 8}

## Question 8

Type: comparison

How does REALM compare with ORQA or other open-domain QA baselines, and what evidence supports that comparison?

### Baseline Answer

REALM compares to other open-domain QA systems in the following ways:

*   **Comparison with ORQA:** ORQA is the most direct comparison to REALM, as both use a similar latent variable model and maximize marginal likelihood [1, 7]. Additionally, the fine-tuning setup, hyperparameters, and training data are identical between the two, and both utilize the Inverse Cloze Task to initialize their retrievers [1, 7]. The improvement of REALM over ORQA is attributed purely to better pre-training methods [1]. If both the retriever and encoder of REALM are reset to their baseline states, the system reduces to the ORQA baseline [5].
*   **Comparison with Retrieval-Based Systems:** Unlike many other retrieval-based systems (such as DrQA, HardEM, GraphRetriever, and PathRetriever) which often retrieve between 20 to 80 documents, REALM achieves the overall best performance while only retrieving 5 documents [1, 7].
*   **Comparison with Generation-Based Systems:** REALM is compared against state-of-the-art generation-based systems, specifically a version of T5 that was fine-tuned for Open-QA [4].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7
[5] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e
[7] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-9-28fdbaa31084f99a63b56

### Multi-Agent Answer

REALM compares to other open-domain question answering (Open-QA) systems in the following ways:

**Comparison with ORQA**
*   ORQA is considered the most direct comparison to REALM because the fine-tuning setup, hyperparameters, and training data are identical [E1].
*   The retrievers for both REALM pretraining and ORQA are initialized using the Inverse Cloze Task [E2].
*   REALM differs from ORQA by backpropagating into the MIPS index rather than using a fixed index [E4].
*   The improvement of REALM over ORQA is attributed purely to better pre-training methods [E1].

**Comparison with Other Retrieval-Based Systems**
*   REALM achieves the best overall performance compared to other retrieval-based systems despite retrieving fewer documents [E1].
*   Specifically, REALM achieves its best performance by retrieving 5 documents, whereas other retrieval-based systems (such as Asai et al., 2019; Min et al., 2019a;b) typically retrieve between 20 and 80 documents [E1].

**General Performance**
*   REALM achieves new state-of-the-art results on three evaluated Open-QA benchmarks: Natural Questions, Web Questions, and Curated TREC [E3].
*   REALM outperforms all previous systems by 4-16% absolute accuracy on these three benchmarks [E3].

### Metrics

- baseline_latency_seconds: 6.880
- orchestrator_latency_seconds: 79.562
- baseline_total_tokens: 7685
- orchestrator_total_tokens: 53005
- baseline_citation_count: 8
- orchestrator_evidence_count: 12
- fact_check_status_counts: {'unsupported': 3, 'supported': 8}

## Question 9

Type: comparison

How does REALM's retrieval-based approach compare with storing knowledge only in model parameters?

### Baseline Answer

Compared to models that store knowledge implicitly in their parameters, REALM's retrieval-based approach offers the following differences:

*   **Interpretability and Modularity:** REALM captures knowledge in a more modular and interpretable way [1, 3]. Unlike implicit storage, REALM's memories are "grounded," meaning each memory is associated with a specific document rather than unnamed value vectors [6]. This provides provenance for predicted answers, which is essential for applications like Open-domain Question Answering (Open-QA) to be considered trustworthy [6].
*   **Explicit Role of Knowledge:** This approach explicitly exposes the role of world knowledge by requiring the model to decide what knowledge to retrieve and use during inference [1].
*   **Storage and Scalability:** In models where knowledge is stored implicitly in parameters, storage space is limited by the size of the network; capturing more world knowledge requires training ever-larger networks, which can be expensive or prohibitively slow [3]. REALM instead uses a learned textual knowledge retriever to access documents from a large corpus [1, 3].
*   **Adaptability:** REALM can adapt to updated knowledge corpora; for example, a model pre-trained on an older corpus can retrieve documents from an updated corpus to generate correct tokens for new information [8].

Citations:
[1] data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[3] data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[6] data/2002.08909v1.pdf, chunk_id: 2002.08909v1-14-83fbe5c3ec4e1ed386558b56
[8] data/2002.08909v1.pdf, chunk_id: 2002.08909v1-20-58cd33db7

### Multi-Agent Answer

In contrast to models that store knowledge within their parameters, REALM's approach explicitly exposes the role of world knowledge by requiring the model to decide which knowledge to retrieve and use during inference [E3].

REALM's memories are considered "grounded," meaning each memory is associated with a specific document rather than unnamed value vectors [E6, E7]. This grounding provides a level of interpretability and the provenance necessary for users to trust predicted answers in Open-QA applications [E6, E7].

While standard reading comprehension (RC) models may focus on a single document, Open-QA models must retain knowledge from millions of documents because a question could be about any of them [E5]. REALM generalizes existing language modeling work by conditioning on an entire text corpus [E7].

### Metrics

- baseline_latency_seconds: 7.455
- orchestrator_latency_seconds: 73.004
- baseline_total_tokens: 7854
- orchestrator_total_tokens: 50733
- baseline_citation_count: 8
- orchestrator_evidence_count: 14
- fact_check_status_counts: {'supported': 3, 'unsupported': 2}

## Question 10

Type: evidence synthesis / ablation

What ablation or diagnostic evidence shows that retrieval pre-training improves REALM rather than only the reader component?

### Baseline Answer

To determine whether REALM pre-training improves the retriever, the encoder, or both, the researchers performed an ablation study where they reset the parameters of either the retriever or the encoder to their baseline state before fine-tuning [4].

The evidence shows that:
*   **Both components benefit:** Both the encoder and the retriever benefit from REALM training when addressed separately [4].
*   **Synergy is required for peak performance:** The best results are achieved when both components act in unison [4].
*   **Retriever contribution isolation:** To more significantly isolate the contribution of improving the retriever during pre-training, the researchers reported how often the gold answer appears in the top-5 retrievals before any fine-tuning was applied [1, 4].

In the specific ablation experiments on the NaturalQuestions development set, the "REALM retriever + Baseline encoder" achieved an Exact Match score of 37.4, while the "Baseline retriever + REALM encoder" achieved a score of 35.3 [8].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e
[8] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-11-3fa55fc3148d1188cb70ab91

### Multi-Agent Answer

Evidence showing that retrieval pre-training improves the REALM system, rather than just the reader component, is provided through several diagnostic metrics and comparisons:

* **Component Analysis**: While both the retriever and the encoder benefit separately from REALM training, the best results are achieved when both components act in unison [E6]. Resetting both the retriever and the encoder reduces the system to the baseline, ORQA [E6].
* **Isolation of Retriever Improvement**: To specifically isolate the contribution of improving the retriever during pre-training, researchers report how frequently the gold answer appears in the top-5 retrievals before any fine-tuning is applied [E6, E7].
* **Comparison to ORQA**: ORQA serves as the most direct comparison to REALM because the fine-tuning setup, hyperparameters, and training data are identical [E7]. The improvement of REALM over ORQA is attributed purely to better pre-training methods [E7].
* **Ablation Studies**: Ablation studies were performed on critical components of REALM using results from the NaturalQuestions-Open dataset to analyze their impact [E6].

### Metrics

- baseline_latency_seconds: 6.556
- orchestrator_latency_seconds: 82.092
- baseline_total_tokens: 7915
- orchestrator_total_tokens: 55397
- baseline_citation_count: 8
- orchestrator_evidence_count: 13
- fact_check_status_counts: {'supported': 6}

## Question 11

Type: evidence synthesis

Synthesize the evidence for why REALM improves open-domain QA performance, including retrieval quality, pre-training, and downstream fine-tuning.

### Baseline Answer

REALM improves open-domain question answering (Open-QA) performance through the following mechanisms:

*   **Pre-training:** The improvement of REALM over its direct comparison, ORQA, is attributed purely to better pre-training methods [1]. REALM uses a masked language modeling (MLM) task as an unsupervised learning signal during pre-training [4]. This process optimizes a latent variable language model by marginalizing over possible documents, which rewards the retriever for selecting documents that improve the language model's perplexity [5]. This method is effective in both single-corpus (Wikipedia) and separate-corpus (CC-News and Wikipedia) settings [1].
*   **Retrieval Quality:** REALM utilizes a learned neural knowledge retriever that retrieves documents from a large corpus, such as Wikipedia, before making a prediction [4, 5]. Unlike other retrieval-based systems that often retrieve between 20 and 80 documents, REALM achieves the overall best performance while only retrieving 5 documents [1]. Ablation studies show that the pre-training process improves both the encoder and the retriever, but the best results require both components to act in unison [8].
*   **Downstream Fine-tuning:** REALM's retriever is specifically designed to transfer to downstream tasks because it retrieves raw text rather than labeled examples [5]. When fine-tuned on Open-QA benchmarks, REALM outperforms previous state-of-the-art methods by a significant margin of 4-16% absolute accuracy [4, 5]. Notably, REALM outperforms the 11-billion parameter T5 model while being 30 times smaller [4].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[5] source: data/2002.08909v1.pdf, chunk_id: 2002.089

### Multi-Agent Answer

REALM (Retrieval-Augmented Language Model) improves open-domain QA performance through a novel pre-training framework that integrates a learned textual knowledge retriever with a language model [E2]. The improvement of REALM over the ORQA baseline is attributed entirely to its superior pre-training methods [E1, E3].

**Pre-training and Masking**
During pre-training, the model utilizes a masked language modeling (MLM) task to predict masked tokens in a sentence [E5, E8]. A critical component of this process is the salient span masking scheme, which targets entities or dates to focus the model on examples requiring world knowledge [E4, E7]. This specific masking strategy significantly outperforms other masking strategies [E7].

**Retrieval Quality and Mechanism**
The retriever is trained using a performance-based signal from unsupervised text, where retrievals that improve the language model's perplexity are rewarded [E2]. Specifically, the gradient encourages the retriever to increase the relevance score of a document if that document performs better than expected, defined as $p(y|z, x) > p(y|x)$ [E7]. To manage the large corpus, REALM uses Maximum Inner Product Search (MIPS) for document selection, with an asynchronous refresh mechanism to ensure the index remains stable during training [E2, E7]. To address the computational challenge of summing over all documents, the model approximates the marginal probability by summing over the top $k$ documents with the highest probability under $p(z|x)$ [E8].

**Downstream Fine-tuning**
While the pre-training task is masked language modeling, the fine-tuning task is Open-QA, which involves predicting an answer $y$ for a question $x$ [E5]. During fine-tuning inference, the model considers the top-5 candidate documents [E3]. REALM achieves high performance by retrieving fewer documents than other retrieval-based systems; it can achieve its best overall performance by retrieving only 5 documents, whereas other systems typically retrieve between 20 and 80 documents [E1].

### Metrics

- baseline_latency_seconds: 6.494
- orchestrator_latency_seconds: 96.520
- baseline_total_tokens: 8205
- orchestrator_total_tokens: 59691
- baseline_citation_count: 8
- orchestrator_evidence_count: 13
- fact_check_status_counts: {'supported': 5, 'unsupported': 7}

## Question 12

Type: multi-step reasoning

Explain step by step how a masked-language-model pre-training objective can improve downstream open-domain QA in REALM.

### Baseline Answer

In REALM, a masked-language-model (MLM) pre-training objective improves downstream open-domain question answering (Open-QA) through the following process:

1.  **Unsupervised Pre-training via MLM**: The model is pre-trained on an unlabeled corpus (e.g., Wikipedia text) using the MLM objective, where it must predict missing tokens ($y$) in a masked input sentence ($x$) [1].
2.  **Joint Training of Retriever and Encoder**: REALM augments standard language model pre-training with a learned textual knowledge retriever [2]. During the unsupervised pre-training phase, the knowledge retriever and the knowledge-augmented encoder are trained jointly [4].
3.  **Performance-Based Learning Signal**: The retriever is trained using a performance-based signal from the unsupervised text [5]. A retrieval that improves the language model's perplexity is rewarded, while an uninformative retrieval is penalized [5].
4.  **End-to-End Backpropagation**: The signal from the language modeling objective is backpropagated through the entire system, including the retrieval step, which can consider millions of documents [2]. This allows the model to learn to decide what knowledge to retrieve and use [5].
5.  **Transfer to Open-QA**: Because the retriever is trained to find documents that provide necessary information for the MLM task, it learns to transfer to other tasks, such as Open-QA [5]. During Open-QA fine-tuning, the model uses the learned retriever to pull relevant documents from a corpus to help inform the prediction of an answer string [2, 5].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-2-7f240c64641ad3f52fc62e97, chunk_index: 2
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2, chunk_index: 0
[4] source: data/2002.08909v1.pdf, chunk_id

### Multi-Agent Answer

A masked-language-model (MLM) pre-training objective improves downstream open-domain question answering (Open-QA) in REALM through the following steps:

1.  **Learning Representations and Knowledge**: During pre-training, the MLM task requires the model to predict missing tokens within an input text passage [E1]. This objective enables the model to learn and encode syntactic and semantic information, as well as world knowledge, from unlabeled text corpora [E1].
2.  **Unsupervised Retriever Training**: Unlike standard models that store world knowledge implicitly in neural network parameters [E2], REALM uses the MLM signal to train a latent knowledge retriever in an unsupervised manner [E2]. The retriever is trained using a performance-based signal from unsupervised text, where retrievals that improve the language model’s perplexity are rewarded [E3].
3.  **Augmenting the Model with Retrieval**: The framework augments language model pre-training by allowing the model to retrieve and attend over documents from a large corpus, such as Wikipedia [E2]. This establishes a "retrieve-then-predict" process where the model learns to decide what knowledge to retrieve and use during inference [E3].
4.  **Improving Downstream Generalization**: Pre-training for a downstream task like Open-QA often leads to better generalization than training from scratch [E1]. In REALM, the signal from the language modeling objective backpropagates through the retrieval step [E2].

### Metrics

- baseline_latency_seconds: 6.636
- orchestrator_latency_seconds: 84.749
- baseline_total_tokens: 9087
- orchestrator_total_tokens: 58005
- baseline_citation_count: 8
- orchestrator_evidence_count: 14
- fact_check_status_counts: {'unsupported': 4, 'supported': 8}

## Question 13

Type: multi-step reasoning / error analysis

If REALM retrieves an irrelevant document, how would that affect p(z|x), p(y|z,x), and the final answer prediction?

### Baseline Answer

If REALM retrieves an irrelevant document $z$, the effects are as follows:

*   **$p(z|x)$:** The retriever models the distribution of possibly helpful documents as $p(z|x)$ [3]. While the context does not explicitly state how the value of $p(z|x)$ changes specifically when a document is irrelevant, it notes that at the beginning of training, if the retriever lacks good embeddings, retrieved documents will likely be unrelated to $x$ [7].
*   **$p(y|z,x)$:** An irrelevant document $z$ can result in a negative Retrieval Utility (RU), which is defined as $\text{RU}(z|x) = \log p(y|z, x) - \log p(y|\emptyset, x)$ [1, 7]. A negative RU indicates that $z$ is less useful for predicting $y$ than the null document $\emptyset$ [1].
*   **Final answer prediction ($p(y|x)$):** The overall likelihood of generating $y$ is obtained by treating $z$ as a latent variable and marginalizing over all possible documents: $p(y|x) = \sum_{z \in Z} p(y|z, x)p(z|x)$ [3]. The context illustrates that when REALM retrieves documents with a related fact, the marginalized probability of the correct answer increases dramatically [2]. Conversely, if the retriever selects uninformative documents, the model's performance is impacted [4].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-20-58cd33db77feaae8a3f8d036
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b

### Multi-Agent Answer

The provided evidence does not explicitly state the mathematical impact of an irrelevant document on $p(z|x)$ or $p(y|z,x)$, but it describes the implications for Retrieval Utility (RU) and predictive usefulness.

If a retrieved document $z$ is irrelevant to the input $x$, the following effects are indicated:

*   **Retrieval Utility (RU):** An irrelevant document $z$ can result in a negative Retrieval Utility, which is defined as $RU(z|x) = \log p(y |z, x) - \log p(y |\emptyset, x)$ [E1, E8].
*   **Predictive Usefulness:** A negative RU indicates that the document $z$ is less useful for predicting the target $y$ than the null document ($\emptyset$) [E1, E8]. This may occur if $z$ is irrelevant to $x$, if the masked tokens in $x$ do not require world knowledge to predict, or if the knowledge is already sufficiently commonplace that it has been "baked into" the model's parameters [E1, E8].
*   **Final Answer Prediction:** While the exact change to the final answer prediction for an irrelevant document is not quantified, the evidence notes that the marginal probability of the correct answer increases dramatically when the model manages to retrieve documents containing a related fact [E7].

### Metrics

- baseline_latency_seconds: 6.389
- orchestrator_latency_seconds: 84.718
- baseline_total_tokens: 8309
- orchestrator_total_tokens: 50759
- baseline_citation_count: 8
- orchestrator_evidence_count: 12
- fact_check_status_counts: {'unsupported': 3, 'supported': 2}

## Question 14

Type: limitation/uncertainty

What limitations, uncertainties, or missing comparisons should be noted when interpreting REALM's reported results?

### Baseline Answer

When interpreting REALM's reported results, the following limitations, uncertainties, and missing comparisons should be noted:

*   **Uncertainty in Retrieval Utility (RU):** A negative RU indicates that the retrieved document ($z$) is less useful for predicting the target ($y$) than a null document [2]. This uncertainty arises because a negative RU could mean the document is irrelevant to the input ($x$), or it could mean the masked tokens in $x$ do not require world knowledge, or that the necessary world knowledge is already sufficiently "baked into" the model's parameters [2].
*   **Impact of Index Staleness:** The results suggest that a "stale index" can negatively impact model training, and further reducing this staleness could potentially offer better optimization [4].
*   **Missing Data/Experiments:** Certain types of data that could potentially benefit REALM were not used in the experiments [1].
*   **Potential for Further Optimization:** While the system achieves high performance while retrieving only 5 documents, the text notes that reducing index staleness might improve optimization [1, 4].

**Citations**
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-20-58cd33db77feaae8a3f8d036
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e

### Multi-Agent Answer

When interpreting REALM's reported results, several limitations, uncertainties, and missing experimental components should be noted:

**Knowledge Retention and Adaptation**
* While REALM can adapt to an updated knowledge corpus, the knowledge-augmented encoder may still retain some old world knowledge even after the corpus has been updated [E4].
* This can lead to the model failing to update predictions for certain queries; for example, it may continue to predict "Thatcher" for the question "is the prime minister of United Kingdom" despite the use of an updated corpus [E4].

**Uncertainty in Retrieval Utility (RU)**
* A negative Retrieval Utility (RU) indicates that a retrieved document is less useful for predicting a target than a null document [E4, E8].
* The exact cause of a negative RU is uncertain, as it could be due to the document being irrelevant to the input, the masked tokens not requiring world knowledge, or the necessary world knowledge already being "baked into" the model's parameters [E4, E8].

**Optimization and Data Limitations**
* The training process is sensitive to the freshness of the index, as using a stale MIPS (Maximum Inner Product Search) index can hurt model training [E2].
* Additionally, the researchers noted that certain data could have potentially benefited REALM, but this data was not used in their experiments [E1].

### Metrics

- baseline_latency_seconds: 5.260
- orchestrator_latency_seconds: 71.055
- baseline_total_tokens: 7412
- orchestrator_total_tokens: 52652
- baseline_citation_count: 8
- orchestrator_evidence_count: 11
- fact_check_status_counts: {'supported': 4, 'unsupported': 2}

## Question 15

Type: citation grounding / uncertainty

Which claims about REALM's performance or mechanism cannot be verified unless the answer cites specific experimental evidence from the paper?

### Baseline Answer

Based on the provided context, the following claims regarding REALM's performance or mechanism cannot be verified without citing specific experimental evidence from the paper:

*   **Performance comparison with ORQA:** While the text states that the improvement of REALM over ORQA is "purely due to better pre-training methods" [1], the specific experimental results or data supporting this direct comparison are not provided in the text (it notes that the fine-tuning setup, hyperparameters, and training data are identical, but does not provide the evidence for the claim of improvement).
*   **Performance relative to other retrieval-based systems:** The claim that REALM "gets the overall best performance while only retrieving 5 documents" compared to other retrieval-based systems that often retrieve 20 to 80 documents [1] requires specific experimental evidence/results not fully detailed in the snippets.
*   **Effectiveness of the MIPS index refresh rate:** The text states that "results in Table 2 suggests that a stale index can hurt model training," but the specific experimental data from Table 2 is missing [4].
*   **Impact of the masking scheme:** The text claims that salient span masking is "crucial for REALM" and that "latent variable learning relies heavily on the utility of retrieval and is therefore more sensitive to a consistent learning signal" [4], but the specific experimental evidence proving this necessity is not present in the provided text.
*   **Improvement of components (Encoder vs. Retriever):** The claim that both the encoder and retriever "benefit from REALM training separately, but the best result requires both components acting in unison" [4] refers to findings that would be contained in specific experimental results not fully provided.

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e

### Multi-Agent Answer

Based on the provided evidence notes, the following claims regarding REALM's performance and mechanism can be verified:

*   **Performance Gains:** REALM outperforms all previous state-of-the-art methods on three Open-domain Question Answering (Open-QA) benchmarks—Natural Questions, Web Questions, and Curated TREC—by an absolute accuracy margin of 4-16% [E2, E3].
*   **Comparison to ORQA:** The improvement of REALM over ORQA is attributed purely to better pre-training methods, because the fine-tuning setups, hyperparameters, and training data are identical [E1].
*   **Retrieval Efficiency:** REALM achieves its best overall performance by retrieving only 5 documents [E1]. This is significantly fewer than other retrieval-based systems, which typically retrieve between 20 and 80 documents [E1].
*   **Pre-training Mechanism:** The retriever is trained using a performance-based signal from unsupervised text, where retrievals that improve the language model's perplexity are rewarded [E2].
*   **Masking Strategy:** The "salient span masking" scheme is crucial for REALM because it focuses the model on examples requiring world knowledge and significantly outperforms other masking strategies [E4, E6].
*   **Architectural Mechanism:** REALM decomposes the generative process into two steps: first retrieving potentially helpful documents $z$ from a corpus $Z$ ($p(z|x)$), and then conditioning on both the retrieved $z$ and the input $x$ to generate the output $y$ ($p(y|z, x)$) [E5].
*   **Index Management:** Implementing asynchronous Maximum Inner Product Search (MIPS) refreshes results in stable optimization, provided refreshes occur at a sufficiently frequent rate [E6]. A stale MIPS index can negatively impact model training [E4].

### Metrics

- baseline_latency_seconds: 6.018
- orchestrator_latency_seconds: 65.089
- baseline_total_tokens: 7907
- orchestrator_total_tokens: 54247
- baseline_citation_count: 8
- orchestrator_evidence_count: 11
- fact_check_status_counts: {'unsupported': 2, 'supported': 4}
