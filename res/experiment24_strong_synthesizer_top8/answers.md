# experiment24: retrieval sweep, strong final synthesizer only, top_k=8

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

REALM retrieves from a large textual knowledge corpus, such as Wikipedia [1, 2]. This corpus is used as a source of external knowledge during the pre-training, fine-tuning, and inference stages [2].

The model uses the retriever to find potentially helpful documents ($z$) based on an input ($x$) [3]. The process is modeled as a "retrieve-then-predict" approach, which decomposes the probability of an output ($y$) into two steps:
1.  **Retrieve:** The model first retrieves documents from the knowledge corpus $Z$ by modeling the retrieval as a sample from the distribution $p(z | x)$ [3].
2.  **Predict:** The model then conditions on both the retrieved documents and the original input to generate the output, modeled as $p(y | z, x)$ [3].

By treating the retrieved document as a latent variable and marginalizing over all possible documents, the model optimizes its overall likelihood [3]. This allows the model to attend over the retrieved documents to help inform its predictions [1].

Citations:
[1] data/2002.08909v1.pdf (chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952)
[2] data/2002.08909v1.pdf (chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2)
[3] data/2002.08909v1.pdf (chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7)

### Multi-Agent Answer

REALM retrieves information from a large knowledge corpus, such as Wikipedia [E2, E3]. This corpus can consist of millions of documents [E1, E3]. The framework can be applied in single-corpus settings where both the input and knowledge source are Wikipedia, or in separate-corpus settings where the input is CC-News and the knowledge source is Wikipedia [E5].

The model uses this external knowledge through a two-step process: first, it retrieves potentially helpful documents $z$ from a knowledge corpus $Z$ [E1]. Second, it predicts the output $y$ by conditioning on both the input $x$ and the retrieved documents $z$ [E1]. During this process, the language model attends over the retrieved documents to help inform its predictions [E2]. For fine-tuning inference, the model considers the top-5 candidate documents [E7].

### Metrics

- baseline_latency_seconds: 7.620
- orchestrator_latency_seconds: 81.078
- baseline_total_tokens: 8660
- orchestrator_total_tokens: 55218
- baseline_citation_count: 8
- orchestrator_evidence_count: 9
- fact_check_status_counts: {'unsupported': 2, 'supported': 5}

## Question 2

Type: easy lookup

Which downstream tasks or benchmarks does the paper use to evaluate REALM?

### Baseline Answer

To evaluate REALM, the paper uses the following Open-QA benchmarks:

*   **NQ** (NaturalQuestions) [6]
*   **WQ** (WebQuestions) [6]
*   **CT** (ComplexType) [6]

Additionally, the paper presents ablation experiments specifically for the **NaturalQuestions-Open** dataset [1, 7].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[6] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-11-3fa55fc3148d1188cb70ab91
[7] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e

### Multi-Agent Answer

The paper evaluates REALM using three popular Open-domain Question Answering (Open-QA) benchmarks: NATURAL QUESTIONS-OPEN, WEB QUESTIONS, and CURATED TREC [E5].

### Metrics

- baseline_latency_seconds: 5.796
- orchestrator_latency_seconds: 34.773
- baseline_total_tokens: 8159
- orchestrator_total_tokens: 28695
- baseline_citation_count: 8
- orchestrator_evidence_count: 9
- fact_check_status_counts: {'supported': 1}

## Question 3

Type: definition

What is REALM, and what does the paper mean by retrieval-augmented language model pre-training?

### Baseline Answer

**REALM** (Retrieval-Augmented Language Model) is a novel framework designed to capture knowledge in a more modular and interpretable way [1, 2]. Unlike traditional models that store knowledge implicitly within their parameters, REALM augments language model pre-training algorithms with a learned textual knowledge retriever [1, 2]. This approach explicitly exposes the role of world knowledge by requiring the model to decide what knowledge to retrieve and use during inference [1]. Specifically, the language model uses the retriever to select documents from a large corpus (such as Wikipedia) and then attends over those documents to inform its predictions [1].

**Retrieval-augmented language model pre-training** refers to the process of augmenting language model pre-training algorithms with a learned textual knowledge retriever [1]. In this framework:
*   **The Process:** The model follows a "retrieve-then-predict" approach [1]. For the pre-training task (specifically masked language modeling), the model must predict missing tokens by first retrieving potentially helpful documents from a knowledge corpus and then conditioning its prediction on both the original input and the retrieved documents [3].
*   **The Learning Signal:** The retriever is trained using a performance-based signal from unsupervised text [1]. The intuition is that a retrieval that improves the language model's perplexity should be rewarded, while an uninformative retrieval should be penalized [1].
*   **End-to-End Training:** The model is learned end-to-end by backpropagating through the retrieval step, even though the retriever must consider millions of candidate documents [1, 2].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e02

### Multi-Agent Answer

REALM (Retrieval-Augmented Language Model) is a framework that augments language model pre-training with a latent knowledge retriever [E9]. This approach is designed to capture knowledge in a modular and interpretable way [E9]. The architecture decomposes the process of learning a distribution $p(y |x)$ into two distinct steps: first retrieving a document, and then predicting [E2]. The model consists of two primary components: a neural knowledge retriever that models $p(z |x)$ and a knowledge-augmented encoder that models $p(y |z, x)$ [E2].

In the context of this paper, retrieval-augmented language model pre-training refers to a process where the retriever allows the model to retrieve and attend over documents from a large corpus, such as Wikipedia, during the pre-training stage [E9]. This differs from standard language model pre-training, where world knowledge is stored implicitly within the neural network parameters, which requires ever-larger networks to cover more facts [E9]. Additionally, REALM allows for the unsupervised pre-training of a knowledge retriever by using masked language modeling as the learning signal [E9].

### Metrics

- baseline_latency_seconds: 8.592
- orchestrator_latency_seconds: 45.192
- baseline_total_tokens: 9006
- orchestrator_total_tokens: 31085
- baseline_citation_count: 8
- orchestrator_evidence_count: 14
- fact_check_status_counts: {'supported': 10}

## Question 4

Type: definition

How does REALM differ from a standard parametric language model such as BERT in where knowledge is stored and accessed?

### Baseline Answer

Standard parametric language models, such as BERT, store learned world knowledge implicitly within the parameters of the underlying neural network [1]. This implicit storage makes it difficult to determine where knowledge is stored or what specific knowledge is contained within the network, and it also means that storage space is limited by the size of the network, requiring ever-larger networks to capture more facts [1].

In contrast, REALM differs in the following ways:
* **Storage:** Instead of storing knowledge only in its parameters, REALM augments pre-training with a learned textual knowledge retriever that allows the model to access knowledge from a large external corpus, such as Wikipedia [1, 2]. The document index can be viewed as a memory where the keys are document embeddings, and unlike unnamed value vectors in other systems, these memories are "grounded" because each memory is associated with a specific document [6].
* **Access:** REALM uses a "retrieve-then-predict" process [4]. Before making a prediction, the model uses its retriever to select documents from a knowledge corpus and then attends over those documents to inform its prediction [2]. This approach explicitly exposes the role of world knowledge by requiring the model to decide what knowledge to retrieve and use during inference [1, 2].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7
[6] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-14-83fbe5c3ec

### Multi-Agent Answer

Standard parametric language models store world knowledge implicitly within their neural network parameters [E2]. To increase the knowledge capacity of these models, ever-larger networks are required [E2].

In contrast, REALM (Retrieval-Augmented Language Model pre-training) captures knowledge in a more modular and interpretable way by using a learned textual knowledge retriever [E1], [E2]. Rather than relying solely on internal parameters, REALM explicitly exposes the role of world knowledge by requiring the model to decide what to retrieve and use during inference [E1]. The model accesses this knowledge by retrieving documents from a large corpus, such as Wikipedia, and then attending over those documents to inform its predictions [E1], [E2].

Furthermore, the document index in REALM functions as a grounded memory, meaning each memory is explicitly associated with a specific document rather than unnamed value vectors [E5], [E6].

### Metrics

- baseline_latency_seconds: 6.549
- orchestrator_latency_seconds: 41.018
- baseline_total_tokens: 8291
- orchestrator_total_tokens: 31715
- baseline_citation_count: 8
- orchestrator_evidence_count: 16
- fact_check_status_counts: {'supported': 7}

## Question 5

Type: method/mechanism

How does REALM's retrieve-then-predict framework work, including the role of the latent document variable z?

### Baseline Answer

REALM's retrieve-then-predict framework decomposes the probability of an output $y$ given an input $x$, $p(y|x)$, into two distinct steps:

1.  **Retrieve**: The model first retrieves potentially helpful documents $z$ from a knowledge corpus $Z$ [3]. This retrieval is modeled as a sample from the distribution $p(z|x)$ [3].
2.  **Predict**: The model then conditions on both the retrieved document $z$ and the original input $x$ to generate the output $y$, modeled as $p(y|z, x)$ [3].

**The Role of the Latent Document Variable $z$**
The framework treats the document $z$ as a latent variable [3]. To obtain the overall likelihood of generating the output $y$, the model marginalizes over all possible documents $z$ in the corpus $Z$, expressed by the formula:
$p(y |x) = \sum_{z \in Z} p(y |z, x) p(z |x)$ [3].

The importance or "usefulness" of a retrieved document $z$ can be measured via Retrieval Utility (RU), which is defined as the difference between the log-likelihood of the encoder when conditioning on $z$ versus a null document $\emptyset$:
$RU(z |x) = \log p(y |z, x) - \log p(y | \emptyset, x)$ [2].

Citations:
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-20-58cd33db77feaae8a3f8d036
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7

### Multi-Agent Answer

REALM (Retrieval-Augmented Language Model) utilizes a retrieve-then-predict framework that decomposes the generation of an output $y$ from an input $x$ into two distinct steps [E3]. First, the model retrieves relevant documents $z$ from a knowledge corpus $Z$ [E3]. Second, the model predicts the output $y$ by attending over those retrieved documents to help inform its prediction [E1, E2].

In this framework, $z$ is treated as a latent variable [E3]. The generative process is modeled as a latent variable language model that optimizes the marginal likelihood, expressed by the formula $p(y |x) = \sum_{z \in Z} p(y |z, x) p(z |x)$ [E1, E3]. To handle the computational challenge of considering millions of candidate documents, the retriever is structured so that computation for each document can be cached and asynchronously updated, utilizing Maximum Inner Product Search (MIPS) for document selection [E1].

### Metrics

- baseline_latency_seconds: 5.719
- orchestrator_latency_seconds: 86.217
- baseline_total_tokens: 8004
- orchestrator_total_tokens: 56998
- baseline_citation_count: 8
- orchestrator_evidence_count: 11
- fact_check_status_counts: {'supported': 7, 'unsupported': 2}

## Question 6

Type: method/mechanism

How does the paper train the retriever when the retrieved document is latent, and how does learning signal flow back to retrieval?

### Baseline Answer

The paper treats the retrieved document $z$ as a latent variable and optimizes the marginal likelihood to train the retriever [1]. Specifically, the model decomposes the probability of generating an output $y$ given an input $x$, $p(y|x)$, by marginalizing over all possible documents $z$ in the knowledge corpus $Z$:

$p(y|x) = \sum_{z \in Z} p(y|z, x) p(z|x)$ [4]

The learning signal flows back to the retrieval module through backpropagation from the language modeling objective [2]. The gradient of the log-likelihood with respect to the retriever parameters $\theta$ is calculated as:

$\nabla \log p(y|x) = \sum_{z} [p(z|y, x) - p(z|x)] \nabla f(x, z)$ [6]

This mathematical derivation shows that the gradient descent process on the REALM objective is equivalent to supervised maximum likelihood training on a "gold" document $z^*$ that would allow the model to achieve perfect prediction accuracy [6].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952, chunk_index: 1
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2, chunk_index: 0
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7, chunk_index: 3
[6] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-19-a8290af7e1b5f4bf

### Multi-Agent Answer

The REALM framework models the "retrieve-then-predict" method as a latent variable language model and optimizes the marginal likelihood [E1]. To train the retriever, the model uses a performance-based signal derived from unsupervised text [E1]. Specifically, the retriever is rewarded if its retrieval improves the language model’s perplexity and is penalized if the retrieval is uninformative [E1].

The learning signal flows back to the retriever via backpropagation through a retrieval step [E1], [E2]. This process allows for end-to-end learning that considers an entire corpus of textual knowledge [E1], [E2]. During pre-training, the model uses masked language modeling as the learning signal [E2]. In this task, the model predicts masked tokens ($y$) from a sentence ($x$) [E5].

### Metrics

- baseline_latency_seconds: 7.415
- orchestrator_latency_seconds: 41.811
- baseline_total_tokens: 7920
- orchestrator_total_tokens: 30689
- baseline_citation_count: 8
- orchestrator_evidence_count: 10
- fact_check_status_counts: {'supported': 7}

## Question 7

Type: method/mechanism / implementation

What approximations or engineering choices does REALM use to make retrieval over a large corpus practical during training and inference?

### Baseline Answer

To make retrieval over a large corpus practical during training and inference, REALM employs the following engineering choices and approximations:

*   **MIPS Formulation:** The selection of the best documents is formulated as a Maximum Inner Product Search (MIPS) [2].
*   **Caching and Asynchronous Updates:** The retriever is structured so that the computations performed for each document can be cached and updated asynchronously [2].
*   **Parallelization:** During pre-training, the document embedding step for the MIPS index is parallelized over 16 TPUs [4].
*   **Index Refresh Rate:** To manage the index during training, a parallel process re-embeds corpus documents and rebuilds the MIPS index approximately every 500 training steps [5].
*   **Candidate Reduction:**
    *   **During Pre-training:** The model retrieves and marginalizes over 8 candidate documents, which includes a null document $\emptyset$ [4].
    *   **During Fine-tuning Inference:** The system considers only the top-5 candidate documents [1, 4].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-11-3fa55fc3148d1188cb70ab91
[5] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e

### Multi-Agent Answer

To make retrieval over a large corpus practical during training and inference, REALM employs several engineering choices and structural approximations:

*   **Document Selection and Caching:** Document selection is formulated as a Maximum Inner Product Search (MIPS) [E1]. To address the computational challenges associated with large-scale neural retrieval, the retriever is structured so that computations for each individual document can be cached and updated asynchronously [E1].
*   **Parallelization:** During training, the document embedding step is parallelized over 16 TPUs [E3].
*   **Inference Constraints:** During fine-tuning inference, the model limits its scope by considering only the top-5 candidates [E3].

### Metrics

- baseline_latency_seconds: 6.499
- orchestrator_latency_seconds: 40.656
- baseline_total_tokens: 8680
- orchestrator_total_tokens: 31681
- baseline_citation_count: 8
- orchestrator_evidence_count: 13
- fact_check_status_counts: {'supported': 4}

## Question 8

Type: comparison

How does REALM compare with ORQA or other open-domain QA baselines, and what evidence supports that comparison?

### Baseline Answer

REALM compares to ORQA and other open-domain QA baselines in the following ways:

*   **Comparison with ORQA:** ORQA is considered the most direct comparison to REALM because the fine-tuning setup, hyperparameters, and training data are identical [1]. While both systems formulate Open-QA using a similar latent variable model and initialize retrievers using the Inverse Cloze Task, REALM differs by adding a novel language model pre-training step and backpropagating into the MIPS index rather than using a fixed index [2, 7]. The improvement of REALM over ORQA is attributed purely to better pre-training methods [1]. Additionally, resetting both the encoder and retriever in REALM reduces the system to the ORQA baseline [5].
*   **Comparison with Retrieval-based Systems:** Compared to other retrieval-based systems (such as DrQA, HardEM, GraphRetriever, and PathRetriever) which often retrieve between 20 to 80 documents, REALM achieves the overall best performance while retrieving only 5 documents [1, 7].
*   **Comparison with Generation-based Systems:** REALM compares against state-of-the-art generation-based systems, specifically including a version of T5 that has been fine-tuned for Open-QA [4].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-10-8ea61faa3a17c1fc8f8725d8
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7
[5] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8

### Multi-Agent Answer

REALM compares favorably to several Open-domain Question Answering (Open-QA) baselines, including ORQA and generation-based models like T5 [E1, E4, E7].

### Comparison with ORQA
ORQA is the most direct comparison to REALM because both systems utilize identical training data, hyperparameters, and fine-tuning setups [E1]. Additionally, the retrievers for both REALM pre-training and ORQA are initialized using the Inverse Cloze Task [E2]. The improvement of REALM over ORQA is attributed purely to superior pre-training methods [E1, E7].

### Comparison with Other Retrieval-Based Systems
REALM achieves the best overall performance among the compared retrieval-based systems, even though it retrieves fewer documents [E1]. While other compared retrieval-based systems typically retrieve between 20 and 80 documents, REALM can achieve its performance by retrieving only 5 documents [E1].

### Comparison with Generation-Based Baselines (T5)
REALM achieves new state-of-the-art results in Open-QA, outperforming previous systems by 4-16% absolute accuracy across three benchmarks [E4, E8]. This includes outperforming the largest T5-11B model, despite REALM being 30 times smaller [E7]. While the T5-11B model outperforms the previous best Open-QA system, it utilizes additional reading comprehension data from SQuAD during pre-training that was not used for REALM [E7].

### Metrics

- baseline_latency_seconds: 7.582
- orchestrator_latency_seconds: 86.643
- baseline_total_tokens: 7685
- orchestrator_total_tokens: 54260
- baseline_citation_count: 8
- orchestrator_evidence_count: 10
- fact_check_status_counts: {'unsupported': 2, 'supported': 7}

## Question 9

Type: comparison

How does REALM's retrieval-based approach compare with storing knowledge only in model parameters?

### Baseline Answer

Compared to models that store knowledge implicitly in their parameters, REALM's retrieval-based approach offers the following differences:

*   **Interpretability and Modularity:** REALM captures knowledge in a more modular and interpretable way [1, 3]. Because its memories are "grounded"—meaning each memory is associated with a specific document rather than unnamed value vectors—it provides a level of interpretability that is crucial for applications like Open-domain Question Answering (Open-QA), where users require provenance to trust a predicted answer [6].
*   **Explicit Knowledge Role:** In contrast to parameter-based storage, REALM's approach explicitly exposes the role of world knowledge by requiring the model to decide what knowledge to retrieve and use during inference [1].
*   **Storage Constraints:** In models where knowledge is stored implicitly in parameters, storage space is limited by the size of the network; capturing more world knowledge requires training ever-larger networks, which can be expensive or prohibitively slow [3].
*   **Adaptability:** REALM demonstrates the ability to adapt to updated knowledge corpora [8]. For example, a model pre-trained on a 2018 corpus can retrieve a document from an updated 2020 corpus to correctly generate a token that was not present in its original training data [8].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952, chunk_index: 1
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2, chunk_index: 0
[6] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-14-83fbe5c3ec4e1ed386558b56, chunk_index: 14
[8] source: data/2002.089

### Multi-Agent Answer

While language model pre-training can capture world knowledge, this knowledge is stored implicitly within the parameters of a neural network, which necessitates increasingly large networks to cover more facts [E6]. In contrast, REALM (Retrieval-Augmented Language Model) uses a retrieval-based approach that provides several distinctions:

*   **Explicit Knowledge Exposure:** Rather than relying on parameters, REALM explicitly exposes the role of world knowledge by requiring the model to decide what to retrieve from a large corpus and then attend over those documents during inference [E2].
*   **Modularity and Interpretability:** The framework captures knowledge in a more modular and interpretable manner [E2, E6]. Specifically, REALM utilizes "grounded memories," where each memory is associated with a specific document rather than unnamed value vectors [E4, E5]. This grounding provides the provenance necessary for predicted answers to be considered trustworthy in Open-QA applications [E4, E5].

### Metrics

- baseline_latency_seconds: 6.800
- orchestrator_latency_seconds: 39.203
- baseline_total_tokens: 7854
- orchestrator_total_tokens: 28509
- baseline_citation_count: 8
- orchestrator_evidence_count: 12
- fact_check_status_counts: {'supported': 8}

## Question 10

Type: evidence synthesis / ablation

What ablation or diagnostic evidence shows that retrieval pre-training improves REALM rather than only the reader component?

### Baseline Answer

To determine whether REALM pre-training improves the retriever, the encoder, or both, the researchers performed an ablation by resetting the parameters of either the retriever or the encoder to their baseline state before fine-tuning [4].

The evidence showing the impact on both components includes:
* **Individual Component Improvement:** The researchers found that both the encoder and the retriever benefit from REALM training when improved separately [4].
* **Synergistic Effect:** The best results require both components to act in unison [4]. 
* **Ablation Results:** In ablation experiments conducted on the NaturalQuestions-Open development set, the "REALM retriever + Baseline encoder" configuration achieved an exact match score of 37.4, which is higher than the "Baseline retriever + REALM encoder" score of 35.3 and the "Baseline (ORQA)" score of 31.3 [8].
* **Retrieval Isolation:** To more significantly isolate the contribution of improving the retriever during pre-training, the researchers reported how often the gold answer appears in the top-5 retrievals before applying any fine-tuning [1, 4].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05, chunk_index: 12
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e, chunk_index: 13
[8] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-11-3fa55fc3148d1188cb70ab91, chunk_index: 11

### Multi-Agent Answer

To isolate the contribution of improving the retriever during pre-training, researchers reported how frequently the gold answer appears in the top-5 retrievals before any fine-tuning is applied [E2, E4]. While both the encoder and the retriever benefit separately from REALM training, achieving optimal results requires both components to act in unison [E4].

Evidence regarding the specific performance improvements of the retriever component is provided through a comparison with ORQA, which is considered a direct comparison because the two models share identical training data, hyperparameters, and fine-tuning setups [E2]. The improvement of REALM over ORQA is attributed purely to better pre-training methods [E2, E5].

### Metrics

- baseline_latency_seconds: 6.087
- orchestrator_latency_seconds: 84.123
- baseline_total_tokens: 7963
- orchestrator_total_tokens: 58304
- baseline_citation_count: 8
- orchestrator_evidence_count: 17
- fact_check_status_counts: {'supported': 2, 'unsupported': 2}

## Question 11

Type: evidence synthesis

Synthesize the evidence for why REALM improves open-domain QA performance, including retrieval quality, pre-training, and downstream fine-tuning.

### Baseline Answer

REALM improves open-domain question answering (Open-QA) performance through several key mechanisms involving pre-training, retrieval quality, and fine-tuning:

*   **Pre-training Methods:** The improvement of REALM over comparable systems like ORQA is attributed purely to its better pre-training methods [1]. Unlike standard language models that store knowledge implicitly in parameters, REALM uses a masked language modeling (MLM) signal during unsupervised pre-training to train a neural knowledge retriever [4, 5]. This pre-training process uses the marginal likelihood of a "retrieve-then-predict" generative process, which rewards the retriever when it selects documents that help improve the language model's perplexity [5].
*   **Retrieval Quality:** REALM improves retrieval by training the retriever end-to-end using the language modeling objective [4]. This allows the model to retrieve relevant documents to help fill in masked words even when trained only on unsupervised text [8]. Ablation studies show that the retriever significantly benefits from REALM training [8]. Furthermore, REALM can achieve state-of-the-art performance while only retrieving 5 documents, whereas other retrieval-based systems often retrieve between 20 and 80 documents [1].
*   **Downstream Fine-tuning:** REALM is designed so that its retriever can transfer to other tasks because it retrieves raw text rather than labeled examples [5]. When fine-tuned on Open-QA tasks, REALM outperforms previous methods by a significant margin (4-16% absolute accuracy) across multiple benchmarks [4, 5]. It specifically outperforms large generative models like T5-11B while being 30 times smaller [4]. The system achieves its best results when both the encoder and the retriever, which both benefit from REALM pre-training, act in unison during fine-tuning [8].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b94

### Multi-Agent Answer

REALM improves open-domain question answering (Open-QA) performance by augmenting language model pre-training with a learned textual knowledge retriever [E3, E8]. This framework achieves new state-of-the-art results across three Open-QA benchmarks, outperforming previous systems by 4-16% absolute accuracy [E2, E3, E8].

**Retrieval Quality**
The REALM retriever is trained using a performance-based signal from unsupervised text, where retrievals that improve the language model's perplexity are rewarded and uninformative retrievals are penalized [E3]. Unlike traditional models that store world knowledge implicitly in neural network parameters, REALM explicitly exposes the role of world knowledge by requiring the model to decide what knowledge to retrieve and use during inference [E3, E8]. The retriever is designed to consider millions of documents from a large corpus, such as Wikipedia [E3, E6, E8]. During fine-tuning inference, the system considers the top-5 candidates [E6].

**Pre-training**
The improvement of REALM over ORQA is attributed purely to its better pre-training methods, as the fine-tuning setups, hyperparameters, and training data are identical [E1, E6]. REALM utilizes masked language model (MLM) pre-training to learn syntactic information, semantic information, and world knowledge [E2]. During this process, the model uses an Inverse Cloze Task (ICT) objective, where it is trained to retrieve the document from which a given sentence originated [E5]. This pre-training approach is applicable to both single-corpus settings (Wikipedia/Wikipedia) and separate-corpus settings (CC-News/Wikipedia) [E1].

**Downstream Fine-tuning**
For the downstream task of Open-QA, the model is fine-tuned to answer questions by predicting an output conditioned on both the input and the retrieved document [E4]. While standard language model pre-training aims to learn useful representations from unlabeled text to improve generalization, REALM's specific pre-training method allows it to achieve high performance even while retrieving fewer documents than other retrieval-based systems [E1, E2]. Specifically, REALM achieves its best performance by retrieving only 5 documents, whereas other retrieval-based systems typically use a range of 20 to 80 documents [E1].

### Metrics

- baseline_latency_seconds: 6.996
- orchestrator_latency_seconds: 95.257
- baseline_total_tokens: 8205
- orchestrator_total_tokens: 57672
- baseline_citation_count: 8
- orchestrator_evidence_count: 11
- fact_check_status_counts: {'unsupported': 5, 'supported': 6}

## Question 12

Type: multi-step reasoning

Explain step by step how a masked-language-model pre-training objective can improve downstream open-domain QA in REALM.

### Baseline Answer

In REALM, a masked-language-model (MLM) pre-training objective improves downstream open-domain question answering (Open-QA) through the following process:

1.  **Unsupervised Pre-training with MLM**: The model undergoes pre-training on an unlabeled text corpus (such as Wikipedia) using a masked language modeling objective [1]. In this task, tokens are randomly masked in a text passage, and the model must predict the missing tokens [1].
2.  **Learning World Knowledge and Representations**: To successfully predict masked tokens, the MLM must learn to encode syntactic and semantic information as well as world knowledge [1]. 
3.  **Joint Training of Retriever and Encoder**: REALM augments the MLM pre-training by adding a learned textual knowledge retriever [2]. The pre-training is treated as a "retrieve-then-predict" process where the knowledge retriever and the knowledge-augmented encoder are jointly pre-trained [3]. The retriever is trained using a performance-based signal from the unsupervised text; a retrieval that improves the language model's perplexity is rewarded [5].
4.  **End-to-End Backpropagation**: The signal from the MLM objective is backpropagated through the retrieval step, which considers millions of documents [2]. This allows the model to learn to decide what knowledge to retrieve and use [5].
5.  **Transfer to Downstream Open-QA**: After pre-training, the parameters of the retriever and encoder are fine-tuned on the Open-QA task [3]. Because the retriever was trained to find documents that help the language model predict masked tokens, it is designed to transfer to other tasks like Open-QA, where it retrieves relevant text rather than labeled examples [5].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-2-7f240c64641ad3f52fc62e97
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[3] source: data/2002.08

### Multi-Agent Answer

In REALM, a masked-language-model (MLM) pre-training objective improves downstream open-domain question answering (Open-QA) through the following steps:

1.  **Unsupervised Representation Learning**: During pre-training, the model utilizes an MLM task to learn useful language representations from unlabeled text corpora [E1]. This task involves training the model to predict the original values of missing [MASK] tokens within an input text passage [E1][E4]. Through this process, the model encodes syntactic, semantic, and world knowledge [E1].
2.  **Simultaneous Retriever Training**: Unlike traditional models that store knowledge implicitly in neural network parameters [E2], REALM uses the MLM task as a learning signal to perform unsupervised pre-training of a latent knowledge retriever [E2]. The framework functions by rewarding retrievals that improve the language model's perplexity [E3].
3.  **Knowledge Integration**: This pre-training approach enables the model to retrieve and attend over documents from a large corpus, such as Wikipedia, to help inform its predictions [E2][E3]. By implementing this method, the model explicitly exposes the role of world knowledge by requiring the model to decide what knowledge to retrieve and use [E3].

### Metrics

- baseline_latency_seconds: 7.252
- orchestrator_latency_seconds: 78.806
- baseline_total_tokens: 9087
- orchestrator_total_tokens: 52714
- baseline_citation_count: 8
- orchestrator_evidence_count: 13
- fact_check_status_counts: {'unsupported': 4, 'supported': 8}

## Question 13

Type: multi-step reasoning / error analysis

If REALM retrieves an irrelevant document, how would that affect p(z|x), p(y|z,x), and the final answer prediction?

### Baseline Answer

If REALM retrieves an irrelevant document $z$, the effects are as follows:

*   **$p(z|x)$**: The retriever models this distribution to sample potentially helpful documents $z$ given an input $x$ [3]. If a document is irrelevant, it implies the retrieval does not necessarily provide useful information for the task [1].
*   **$p(y|z,x)$**: This represents the conditional probability of generating the output $y$ given the retrieved document $z$ and input $x$ [3]. An irrelevant document $z$ can result in a negative Retrieval Utility (RU), which is defined as $\text{RU}(z|x) = \log p(y|z, x) - \log p(y|\emptyset, x)$ [1]. A negative RU indicates that $z$ is less useful for predicting $y$ than the null document $\emptyset$ [1].
*   **Final answer prediction ($p(y|x)$)**: The overall likelihood is obtained by treating $z$ as a latent variable and marginalizing over all possible documents $z$: $p(y|x) = \sum_{z \in Z} p(y|z, x)p(z|x)$ [3]. When REALM retrieves relevant documents containing related facts, the marginalized probability of the correct answer increases dramatically [2]. Conversely, if the retriever does not have good embeddings, it may retrieve unrelated documents, which can cause the knowledge-augmented encoder to learn to ignore them [7].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-20-58cd33db77feaae8a3f8d036, chunk_index: 20
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e, chunk_index: 13
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-

### Multi-Agent Answer

The provided evidence does not contain specific mathematical formulas or direct descriptions of how $p(z|x)$ or $p(y|z,x)$ change specifically when a document is "irrelevant."

However, the evidence provides the following information regarding document utility and the Retrieval Utility (RU) metric:

*   **Retrieval Utility (RU) Definition:** The RU of a document $z$ for a masked input $x$ is defined as $RU = \log p(y |z, x) - \log p(y |\emptyset, x)$ [E1, E8].
*   **Implications of Negative RU:** A negative RU indicates that a retrieved document $z$ is less useful for predicting the target $y$ than a null document $\emptyset$ [E1, E8].
*   **Causes of Irrelevance/Low Utility:** A document $z$ may be less useful (resulting in a negative RU) if $z$ is irrelevant to $x$, if the masked tokens in $x$ do not require world knowledge to predict, or if the required world knowledge is already embedded in the model parameters [E1, E8].

### Metrics

- baseline_latency_seconds: 6.666
- orchestrator_latency_seconds: 85.890
- baseline_total_tokens: 8309
- orchestrator_total_tokens: 49625
- baseline_citation_count: 8
- orchestrator_evidence_count: 12
- fact_check_status_counts: {'unsupported': 4}

## Question 14

Type: limitation/uncertainty

What limitations, uncertainties, or missing comparisons should be noted when interpreting REALM's reported results?

### Baseline Answer

When interpreting REALM's reported results, the following limitations, uncertainties, or missing comparisons should be noted:

*   **Retrieval Staleness:** The rate at which the MIPS index is refreshed can impact performance; a "stale index" can hurt model training, and the authors suggest that further reducing this staleness might offer better optimization [4].
*   **Retrieval Utility Uncertainties:** A negative Retrieval Utility (RU) indicates that the retrieved document $z$ is less useful for predicting $y$ than a null document [2]. However, this uncertainty could stem from several factors: $z$ might be irrelevant to $x$, the masked tokens in $x$ might not require world knowledge to predict, or the necessary world knowledge may already be sufficiently commonplace and "baked into the model’s parameters" [2].
*   **Data Usage:** Certain types of data could potentially benefit REALM but were not utilized in the experiments conducted [1].
*   **Comparison with Other Systems:** 
    *   The most direct comparison provided is with ORQA, which uses identical training data, hyperparameters, and fine-tuning setups; the improvement seen in REALM over ORQA is attributed purely to better pre-training methods [1].
    *   While REALM achieves the best overall performance among retrieval-based systems, it does so while only retrieving 5 documents, whereas other systems often retrieve between 20 to 80 documents [1, 4].
    *   Regarding generation-based models, while T5 showed that generating answers without explicit extraction is a viable approach, T5 only experimented on reading comprehension tasks where a context document is provided [6].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-20-58cd33db77feaae8a3f8d036
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08

### Multi-Agent Answer

When interpreting REALM's reported results, several limitations, uncertainties, and missing comparisons should be noted:

**Experimental and Data Limitations**
*   The researchers acknowledged that while certain data could have potentially benefited REALM, it was not used in their experiments [E1].
*   The improvement of REALM over ORQA is attributed entirely to superior pre-training methods, as the fine-tuning setup, hyperparameters, and training data are identical [E1].

**Knowledge Retention and Corpus Updates**
*   While the explicit retrieval system allows for adaptation to new world knowledge by modifying corpus documents, the knowledge-augmented encoder may still retain some old knowledge [E8].
*   This retention can result in the model continuing to predict outdated facts even after a corpus update occurs [E8].
*   For example, the model might still predict "Thatcher" as Prime Minister of the UK if that knowledge has become "baked into the model's parameters" [E8].

**Interpretation of Retrieval Utility (RU)**
*   A negative RU score indicates that a retrieved document is less useful for predicting an answer than a null document [E6, E8].
*   This occurrence may be due to the document being irrelevant to the input, the masked tokens not requiring world knowledge, or the necessary knowledge already being "baked into" the model's parameters [E6, E8].

### Metrics

- baseline_latency_seconds: 6.468
- orchestrator_latency_seconds: 82.690
- baseline_total_tokens: 7497
- orchestrator_total_tokens: 54982
- baseline_citation_count: 8
- orchestrator_evidence_count: 12
- fact_check_status_counts: {'supported': 5, 'unsupported': 2}

## Question 15

Type: citation grounding / uncertainty

Which claims about REALM's performance or mechanism cannot be verified unless the answer cites specific experimental evidence from the paper?

### Baseline Answer

Based on the provided context, the following claims about REALM's performance or mechanism cannot be verified without citing specific experimental evidence (such as results from specific tables or figures) from the paper:

*   **Performance comparisons:** While the text states that REALM achieves new state-of-the-art results on three popular Open-QA benchmarks, outperforming previous systems by 4-16% absolute accuracy [7], the specific performance values for NaturalQuestions-Open, Web Questions, or Curated TREC are not provided in the text, and the claim regarding the specific improvement over ORQA being "purely due to better pre-training methods" requires the context of the identical fine-tuning setup, hyperparameters, and training data mentioned [1].
*   **Effectiveness of components:** The claim that both the encoder and retriever benefit from REALM training separately, but the best result requires both components acting in unison, is a finding that necessitates the experimental ablation results mentioned as being in Table 2 [4].
*   **Impact of index staleness:** The claim that a stale MIPS index can hurt model training and that further reducing staleness could offer better optimization is based on results found in Table 2 [4].
*   **Masking scheme importance:** The assertion that salient span masking is "crucial for REALM" compared to random token or span masking requires the comparative experimental results [4].
*   **Retrieval Utility (RU) behavior:** The claim that RU increases steadily over the course of pre-training and is more predictive of good performance on downstream Open-QA tasks than overall log-likelihood requires the evidence presented in Figure 4 [3].
*   **Adaptability to updated knowledge:** The claim that a REALM model can adapt to an updated knowledge corpus (e.g., recovering a word from a 2019 Wikipedia addition using a model pre-trained on a 2018 corpus) requires the specific example provided in Table 4 [3].
*   **Probability increases via retrieval:** The claim that REALM's marginalized probability for a correct answer increases dramatically because it manages to retrieve related documents requires the specific probability comparisons (e.g., 0.129 vs 1.1 x 10⁻¹⁴) found in Table 3 [4].

Citations:
[1] data/2002.08909v1.pdf (chunk_id: 20

### Multi-Agent Answer

Based on the provided evidence, the following claims about REALM's performance or mechanism cannot be fully verified because specific experimental data or comparative results are missing:

* **The quantified importance of the salient span masking scheme:** While it is stated that salient span masking is crucial for REALM [E4] and helps the model focus on problems requiring world knowledge rather than local context [E5], the provided notes do not include the specific numerical ablation results or experimental data required to quantify this importance [E4].
* **The optimal MIPS index refresh rate:** The notes indicate that using a stale MIPS index can negatively impact model training [E4] and that asynchronous MIPS refreshes lead to stable optimization if they occur at a sufficiently frequent rate [E5]; however, the specific experimental evidence comparing different refresh rates is missing [E5].
* **The specific individual contributions of the encoder and retriever:** It is noted that both the encoder and the retriever benefit individually from REALM training, but optimal results require both components to act in unison [E4]; however, the specific experimental breakdown or numerical evidence of these individual contributions is not provided [E4].

### Metrics

- baseline_latency_seconds: 6.625
- orchestrator_latency_seconds: 70.350
- baseline_total_tokens: 7930
- orchestrator_total_tokens: 55910
- baseline_citation_count: 8
- orchestrator_evidence_count: 12
- fact_check_status_counts: {'supported': 3}
