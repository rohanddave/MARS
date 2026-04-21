# experiment05: model ablation, strong fact checker only, top_k=5

## Agent Configuration

- family: model_ablation
- control_variable: fact_check_model
- top_k: 5
- max_evidence_chunks: 5
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

The model uses this external knowledge through a "retrieve-then-predict" process [1, 3]:

*   **Retrieval:** Given an input $x$, the model first uses a learned neural knowledge retriever to retrieve potentially helpful documents $z$ from the knowledge corpus $Z$ [1, 3]. This retriever is defined using a dense inner product model that calculates relevance scores between the input and documents [3].
*   **Prediction:** The model then conditions on both the retrieved documents $z$ and the original input $x$ to generate an output $y$ [3]. During this stage, the model attends over the retrieved documents to help inform its prediction [1].

This process is used during pre-training, fine-tuning, and inference [2].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7

### Multi-Agent Answer

REALM retrieves information from a large knowledge corpus ($Z$), such as Wikipedia [E2, E3]. This knowledge corpus can be the same as the pre-training corpus ($X$), such as in single-corpus settings where both $X$ and $Z$ are Wikipedia [E4], or it can be different, such as in separate-corpus settings where $X$ is CC-News and $Z$ is Wikipedia [E4].

The model uses this external knowledge through a two-step generative process [E1]:

*   **Step 1: Retrieval:** The model first retrieves potentially helpful documents ($z$) from the knowledge corpus ($Z$) [E1]. The retriever utilizes a dense inner product model where relevance scores are determined by the inner product of $d$-dimensional vector embeddings [E1].
*   **Step 2: Prediction:** The model then predicts the output ($y$) conditioned on both the input ($x$) and the retrieved documents ($z$) [E1]. To help inform its prediction, the language model attends over the retrieved documents [E2, E3].

### Metrics

- baseline_latency_seconds: 6.771
- orchestrator_latency_seconds: 55.339
- baseline_total_tokens: 5454
- orchestrator_total_tokens: 36011
- baseline_citation_count: 5
- orchestrator_evidence_count: 7
- fact_check_status_counts: {'unsupported': 3, 'supported': 5}

## Question 2

Type: easy lookup

Which downstream tasks or benchmarks does the paper use to evaluate REALM?

### Baseline Answer

The paper uses the following to evaluate REALM:

*   **NaturalQuestions-Open**: The paper presents results for this benchmark after performing ablation studies on critical components of REALM [1].
*   **Open-QA**: The paper discusses the capacity of the model for applications such as Open-QA, where users require provenance for predicted answers [2, 5].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-14-83fbe5c3ec4e1ed386558b56
[5] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-15-e73576ceacc6e97a0666fd10

### Multi-Agent Answer

REALM is evaluated using three Open-domain Question Answering (Open-QA) benchmarks: NATURAL QUESTIONS, WEB QUESTIONS, and CURATED TREC [E5]. On these three benchmarks, REALM achieves new state-of-the-art results [E5]. Specifically, the model outperforms previous systems by 4-16% in absolute accuracy across these benchmarks [E5].

### Metrics

- baseline_latency_seconds: 5.387
- orchestrator_latency_seconds: 25.826
- baseline_total_tokens: 4378
- orchestrator_total_tokens: 18361
- baseline_citation_count: 5
- orchestrator_evidence_count: 7
- fact_check_status_counts: {'supported': 2}

## Question 3

Type: definition

What is REALM, and what does the paper mean by retrieval-augmented language model pre-training?

### Baseline Answer

REALM, which stands for Retrieval-Augmented Language Model, is a novel framework that augments language model pre-training algorithms with a learned textual knowledge retriever [1, 2]. Unlike traditional models that store world knowledge implicitly in their parameters, REALM explicitly exposes the role of world knowledge by requiring the model to decide what knowledge to retrieve and use during inference [1, 2]. The process involves the language model using a retriever to pull documents from a large corpus (such as Wikipedia) and then attending over those documents to inform its predictions [1].

Retrieval-augmented language model pre-training refers to a method where the language model's pre-training is augmented with a latent knowledge retriever [2]. In this framework:
*   **Generative Process:** The model follows a "retrieve-then-predict" approach [3]. For pre-training, the task is masked language modeling, where the model must predict missing tokens ($y$) from a sentence ($x$) [3]. This is decomposed into first retrieving potentially helpful documents ($z$) from a knowledge corpus ($Z$) based on the distribution $p(z|x)$, and then conditioning on both the input and the retrieved documents to generate the output $p(y|z, x)$ [3].
*   **Learning Signal:** The retriever is trained in an unsupervised manner using a performance-based signal from text; specifically, retrievals that improve the language model's perplexity are rewarded, while uninformative retrievals are penalized [1]. This is achieved by modeling the approach as a latent variable language model and optimizing the marginal likelihood [1].
*   **End-to-End Training:** The framework requires backpropagating through a retrieval step that considers an entire corpus of textual knowledge [1, 2].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[3] source: data/2

### Multi-Agent Answer

REALM, which stands for Retrieval-Augmented Language Model, is a framework that augments language model pre-training with a latent knowledge retriever [E6]. This approach is designed to capture knowledge in a more modular and interpretable way compared to standard language model pre-training, which stores world knowledge implicitly within neural network parameters [E6].

Retrieval-augmented language model pre-training involves a model that retrieves and attends over documents from a large corpus, such as Wikipedia, during the stages of pre-training, fine-tuning, and inference [E6]. The retrieval step is capable of considering millions of documents [E6]. Furthermore, the knowledge retriever can be pre-trained in an unsupervised manner by using masked language modeling as the learning signal [E6]. During this pre-training process, backpropagation occurs through a retrieval step that considers millions of documents [E6].

### Metrics

- baseline_latency_seconds: 8.063
- orchestrator_latency_seconds: 29.653
- baseline_total_tokens: 5743
- orchestrator_total_tokens: 19757
- baseline_citation_count: 5
- orchestrator_evidence_count: 9
- fact_check_status_counts: {'supported': 6}

## Question 4

Type: definition

How does REALM differ from a standard parametric language model such as BERT in where knowledge is stored and accessed?

### Baseline Answer

Standard parametric language models, such as BERT, store world knowledge implicitly within the parameters of the underlying neural network [1]. This implicit storage makes it difficult to determine where knowledge is located or what specific knowledge is stored, and it limits storage space to the size of the network, requiring larger networks to capture more facts [1].

In contrast, REALM (Retrieval-Augmented Language Model) differs in the following ways:

*   **Storage:** Instead of relying solely on parameters, REALM augments pre-training with a learned textual knowledge retriever that uses a large textual knowledge corpus (such as Wikipedia) as a knowledge source [1, 2].
*   **Access:** REALM uses a "retrieve-then-predict" process where, before making a prediction, the model uses the retriever to retrieve documents from the corpus and then attends over those documents to inform its prediction [2].
*   **Qualitative Benefits:** Because REALM's memories are grounded—meaning each memory is associated with a specific document rather than unnamed value vectors—the approach provides benefits in terms of modularity and interpretability [1, 3].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-15-e73576ceacc6e97a0666fd10

### Multi-Agent Answer

Standard language model pre-training stores world knowledge implicitly within the parameters of a neural network [E3]. This approach requires increasingly larger networks to cover a greater number of facts [E3]. 

In contrast, REALM (Retrieval-Augmented Language Model) utilizes a learned textual knowledge retriever to capture knowledge in a more modular and interpretable way [E2]. Unlike models that rely on parameter storage, REALM explicitly exposes the role of world knowledge by requiring the model to decide what knowledge to retrieve and use during inference [E2]. Before making a prediction, the language model uses the retriever to retrieve documents from a large corpus, such as Wikipedia, and then attends over those documents to help inform its prediction [E2].

### Metrics

- baseline_latency_seconds: 6.182
- orchestrator_latency_seconds: 58.368
- baseline_total_tokens: 6572
- orchestrator_total_tokens: 40301
- baseline_citation_count: 5
- orchestrator_evidence_count: 9
- fact_check_status_counts: {'supported': 5}

## Question 5

Type: method/mechanism

How does REALM's retrieve-then-predict framework work, including the role of the latent document variable z?

### Baseline Answer

REALM's retrieve-then-predict framework decomposes the probability of an output $y$ given an input $x$, denoted as $p(y | x)$, into a two-step generative process [3].

1.  **Retrieve**: The model first retrieves potentially helpful documents $z$ from a knowledge corpus $\mathcal{Z}$ [3]. This step is modeled as a sample from the distribution $p(z | x)$ [3].
2.  **Predict**: The model then conditions on both the original input $x$ and the retrieved document $z$ to generate the output $y$, which is modeled as $p(y | z, x)$ [3].

**Role of the latent document variable $z$**
The document $z$ is treated as a latent variable [3]. To obtain the overall likelihood of generating an output $y$, the model marginalizes over all possible documents $z$ in the corpus $\mathcal{Z}$ [3]. This is expressed mathematically as:
$$p(y |x) = \sum_{z \in \mathcal{Z}} p(y |z, x) p(z |x)$$ [3]

By modeling the approach as a latent variable language model and optimizing the marginal likelihood, the retriever can be trained using a performance-based signal from unsupervised text [1]. Specifically, the retriever is rewarded if the retrieval improves the language model's perplexity [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7

### Multi-Agent Answer

REALM's retrieve-then-predict framework decomposes the generation of an output $y$ from an input $x$ into a two-step process [E3]. First, the model retrieves potentially helpful documents $z$ from a knowledge corpus $Z$ [E3]. Second, the model predicts the output $y$ by conditioning on both the input $x$ and the retrieved documents $z$ [E3].

The framework models this retrieve-then-predict method as a latent variable language model and optimizes the marginal likelihood [E1]. The generative process is expressed mathematically as $p(y |x) = \sum_{z \in Z} p(y |z, x) p(z |x)$ [E3]. In this formulation, $z$ represents the retrieved documents from the knowledge corpus [E3].

### Metrics

- baseline_latency_seconds: 5.583
- orchestrator_latency_seconds: 28.567
- baseline_total_tokens: 5567
- orchestrator_total_tokens: 20112
- baseline_citation_count: 5
- orchestrator_evidence_count: 8
- fact_check_status_counts: {'supported': 6}

## Question 6

Type: method/mechanism

How does the paper train the retriever when the retrieved document is latent, and how does learning signal flow back to retrieval?

### Baseline Answer

The paper trains the retriever by modeling the "retrieve-then-predict" approach as a latent variable language model [1]. To obtain the overall likelihood of generating an output $y$ from an input $x$, the model treats the retrieved document $z$ as a latent variable and marginalizes over all possible documents $z$ in the knowledge corpus $Z$, following the formula: $p(y |x) = \sum_{z \in Z} p(y |z, x) p(z |x)$ [4].

The learning signal flows back to the retrieval module through backpropagation from the language modeling objective [2]. Specifically:
*   **Performance-based signal:** The retriever is trained using a signal from unsupervised text, where retrieval that improves the language model's perplexity is rewarded, and uninformative retrieval is penalized [1].
*   **Unsupervised learning:** During pre-training, the model uses masked language modeling as the learning signal to backpropagate through the retrieval step [2].
*   **End-to-end training:** The model is trained end-to-end by backpropagating through a retrieval step that considers an entire corpus of textual knowledge [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7

### Multi-Agent Answer

The REALM framework models the "retrieve-then-predict" process as a latent variable language model [E1]. Specifically, the model decomposes the generative process $p(y|x)$ into two steps: first, it retrieves documents $z$ from a corpus $Z$ based on $p(z|x)$, and then it predicts the output $y$ based on the input and the retrieved documents $p(y|z, x)$ [E3].

The retriever is trained using a performance-based signal derived from unsupervised text [E1]. During pre-training, masked language modeling is used as the learning signal to train the knowledge retriever in an unsupervised manner [E2]. This training process rewards retrievals that improve the language model's perplexity and penalizes uninformative retrievals [E1]. Learning is achieved end-to-end by backpropagating through a retrieval step that considers an entire corpus of textual knowledge [E1, E2].

### Metrics

- baseline_latency_seconds: 6.846
- orchestrator_latency_seconds: 54.845
- baseline_total_tokens: 5433
- orchestrator_total_tokens: 36797
- baseline_citation_count: 5
- orchestrator_evidence_count: 9
- fact_check_status_counts: {'supported': 5, 'unsupported': 1}

## Question 7

Type: method/mechanism / implementation

What approximations or engineering choices does REALM use to make retrieval over a large corpus practical during training and inference?

### Baseline Answer

To make retrieval over a large corpus practical during training and inference, REALM employs the following engineering choices and approximations:

*   **Retriever Structure and Computation:** The retriever is structured so that the computation for each document can be cached and updated asynchronously [2]. 
*   **Selection Method:** The selection of the best documents is formulated as a Maximum Inner Product Search (MIPS) [2].
*   **Index Management:** During pre-training, a parallel process is used to re-embed corpus documents and rebuild the MIPS index, resulting in an index refresh approximately every 500 training steps [5].
*   **Pre-training Retrieval:** For each example during pre-training, the model retrieves and marginalizes over 8 candidate documents, which includes a null document $\emptyset$ [4].
*   **Inference Retrieval:** During fine-tuning inference, the system considers only the top-5 candidates [4].

Citations:
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-11-3fa55fc3148d1188cb70ab91
[5] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e

### Multi-Agent Answer

To make retrieval over a large corpus practical, REALM employs several technical implementations and engineering choices:

*   **Document Selection Mechanisms:** The retriever utilizes Maximum Inner Product Search (MIPS) for document selection [E1]. To manage computational challenges, it also uses cached computation that is updated asynchronously [E1].
*   **Candidate Selection:** During fine-tuning inference, the model considers the top-5 candidates [E3, E4]. For retrieval and marginalization, the model considers 8 candidate documents, which includes a null document [E4].
*   **Hardware and Parallelization:** The document embedding step is parallelized over 16 TPUs [E4].

### Metrics

- baseline_latency_seconds: 5.297
- orchestrator_latency_seconds: 28.997
- baseline_total_tokens: 5552
- orchestrator_total_tokens: 21149
- baseline_citation_count: 5
- orchestrator_evidence_count: 6
- fact_check_status_counts: {'supported': 5}

## Question 8

Type: comparison

How does REALM compare with ORQA or other open-domain QA baselines, and what evidence supports that comparison?

### Baseline Answer

REALM compares to ORQA and other baselines in the following ways:

*   **Comparison with ORQA:** ORQA is considered the most direct comparison to REALM because the fine-tuning setup, training data, and hyperparameters are identical [1]. Additionally, the retrievers for both REALM pre-training and ORQA are initialized using the Inverse Cloze Task [2]. The improvement REALM shows over ORQA is attributed purely to better pre-training methods [1]. If both the encoder and retriever in REALM are reset to their baseline states before fine-tuning, the system reduces to the ORQA baseline [5].
*   **Comparison with Retrieval-Based Systems:** Compared to other retrieval-based systems (such as Asai et al., 2019; Min et al., 2019a;b), which often retrieve between 20 and 80 documents, REALM achieves the overall best performance while retrieving only 5 documents [1].
*   **Comparison with Generation-Based Systems:** REALM is compared against state-of-the-art systems from the generation-based paradigm [4]. For the most competitive and comparable generation-based baseline, REALM is compared against concurrent work that fine-tunes T5 for Open-QA [2].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-10-8ea61faa3a17c1fc8f8725d8
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7
[5] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b51

### Multi-Agent Answer

ORQA is identified as the most direct comparison to REALM [E1]. The two systems utilize identical training data, hyperparameters, and fine-tuning setups [E1]. Additionally, the retrievers for both REALM pretraining and ORQA are initialized using the Inverse Cloze Task [E2].

The improvement of REALM over ORQA is attributed solely to its superior pre-training methods [E1]. Unlike ORQA, REALM differs by backpropagating into the MIPS index rather than using a fixed index [E7].

Compared to other retrieval-based systems, REALM achieves the best overall performance while retrieving fewer documents [E1]. While other retrieval-based systems typically retrieve between 20 and 80 documents, REALM achieves its performance by retrieving only 5 documents [E1].

### Metrics

- baseline_latency_seconds: 7.121
- orchestrator_latency_seconds: 31.406
- baseline_total_tokens: 5305
- orchestrator_total_tokens: 19517
- baseline_citation_count: 5
- orchestrator_evidence_count: 7
- fact_check_status_counts: {'supported': 7}

## Question 9

Type: comparison

How does REALM's retrieval-based approach compare with storing knowledge only in model parameters?

### Baseline Answer

Compared to models that store knowledge implicitly in their parameters, REALM's retrieval-based approach offers several distinctions:

*   **Interpretability and Modularity:** REALM captures knowledge in a more modular and interpretable way [1, 3]. Because the model's memories are "grounded"—meaning each memory is associated with a specific document rather than unnamed value vectors—it provides a level of interpretability that is crucial for applications like Open-domain Question Answering (Open-QA), where users require provenance for a predicted answer to be trustworthy [5].
*   **Explicit Role of Knowledge:** This approach explicitly exposes the role of world knowledge by requiring the model to decide what knowledge to retrieve and use during inference [1].
*   **Storage and Scalability:** In models where knowledge is stored implicitly in parameters, it is difficult to determine what knowledge is stored and where [3]. Furthermore, storage space in such models is limited by the size of the network; to capture more world knowledge, one must train ever-larger networks, which can be prohibitively expensive or slow [3].

Citations:
[1] data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952, chunk_index: 1
[3] data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2, chunk_index: 0
[5] data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-15-e73576ceacc6e97a0666fd10, chunk_index: 15

### Multi-Agent Answer

In contrast to standard language model pre-training, where world knowledge is stored implicitly within the neural network's parameters, REALM uses a retrieval-based approach that augments pre-training with a learned textual knowledge retriever [E2, E4].

**Knowledge Storage and Scaling**
Implicit knowledge storage in parameters makes it difficult to determine what knowledge is stored and where, and it requires increasingly larger networks to accommodate more facts [E4]. In contrast, REALM captures knowledge in a more modular and interpretable way [E2, E4].

**Mechanism of Use**
Instead of relying solely on parameters, REALM explicitly exposes the role of world knowledge by asking the model to decide what knowledge to retrieve and use during inference [E2]. To do this, the model uses a retriever to select documents from a large corpus, such as Wikipedia, and then attends over those documents to inform its prediction [E2].

**Interpretability and Provenance**
REALM's approach provides qualitative benefits regarding interpretability and modularity [E2, E4]. Unlike models that use unnamed value vectors, REALM's memories are "grounded," meaning each memory is associated with a specific document [E5]. This grounding provides a level of interpretability that is crucial for Open-QA applications, as users require provenance to trust a predicted answer [E5].

### Metrics

- baseline_latency_seconds: 5.855
- orchestrator_latency_seconds: 60.075
- baseline_total_tokens: 5513
- orchestrator_total_tokens: 37162
- baseline_citation_count: 5
- orchestrator_evidence_count: 11
- fact_check_status_counts: {'unsupported': 3, 'supported': 5}

## Question 10

Type: evidence synthesis / ablation

What ablation or diagnostic evidence shows that retrieval pre-training improves REALM rather than only the reader component?

### Baseline Answer

To determine whether REALM pre-training improves the retriever, the encoder, or both, the researchers conducted an ablation by resetting the parameters of either the retriever or the encoder to their baseline state before fine-tuning [4]. 

The diagnostic evidence shows that:
*   Both the encoder and the retriever benefit from REALM training when they are improved separately [4].
*   The best results are achieved when both components act in unison [4].
*   A metric reporting how often the gold answer appears in the top-5 retrievals before applying any fine-tuning was used, as this metric "more significantly isolates the contribution of improving the retriever during pre-training" [1, 4].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05, chunk_index: 12
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e, chunk_index: 13

### Multi-Agent Answer

To demonstrate that retrieval pre-training improves the retriever component specifically, the authors use a metric that measures how frequently the gold answer appears in the top-5 retrievals before any fine-tuning is applied [E1, E4]. This metric is used because it more significantly isolates the contribution of improving the retriever during pre-training [E4].

Further evidence showing the impact of pre-training is provided through a comparison with ORQA; the improvement of REALM over ORQA is attributed purely to better pre-training methods because the fine-tuning setup, hyperparameters, and training data used in the comparison are identical [E1, E5]. Additionally, while both the encoder and the retriever benefit separately from REALM training, the best results are achieved when both components act in unison [E4].

### Metrics

- baseline_latency_seconds: 4.239
- orchestrator_latency_seconds: 29.101
- baseline_total_tokens: 4543
- orchestrator_total_tokens: 20707
- baseline_citation_count: 5
- orchestrator_evidence_count: 6
- fact_check_status_counts: {'supported': 3}

## Question 11

Type: evidence synthesis

Synthesize the evidence for why REALM improves open-domain QA performance, including retrieval quality, pre-training, and downstream fine-tuning.

### Baseline Answer

REALM improves open-domain question answering (Open-QA) performance through the following mechanisms:

*   **Pre-training:** REALM augments language model pre-training with a learned textual knowledge retriever [4]. Unlike traditional models that store knowledge implicitly in parameters, REALM uses a masked language modeling task as an unsupervised learning signal during pre-training [2, 4]. This allows the model to backpropagate through a retrieval step that considers millions of documents, rewarding retrievals that improve the language model's perplexity [4, 5]. The improvement of REALM over systems like ORQA is attributed purely to these better pre-training methods [1].
*   **Retrieval Quality:** REALM uses a neural knowledge retriever modeled as a dense inner product model [2]. The retriever is designed to transfer to other tasks because it retrieves raw text rather than labeled examples [5]. Evidence of improved retrieval quality is seen in the fact that REALM achieves its best performance while retrieving only 5 documents, whereas other retrieval-based systems often retrieve between 20 and 80 documents [1]. Additionally, the retriever is initialized using the Inverse Cloze Task [3].
*   **Downstream Fine-tuning:** The model is fine-tuned on the Open-QA task, where the input is a question and the goal is to predict the answer [2]. This approach allows the model to outperform previous methods by a significant margin of 4-16% absolute accuracy across three popular Open-QA benchmarks [4, 5].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-10-8ea61faa3a17c1fc8f8725d

### Multi-Agent Answer

REALM improves open-domain question answering (Open-QA) performance through a framework that augments language model pre-training with a learned textual knowledge retriever [E7].

**Retrieval Quality**
REALM utilizes a latent knowledge retriever that allows the model to retrieve and attend over documents from a large corpus, such as Wikipedia, during pre-training, fine-tuning, and inference [E7]. The retrieval step is designed to consider millions of documents [E7]. The model uses a neural knowledge retriever based on a dense inner product model, where relevance is determined by the inner product of vector embeddings [E3]. This retriever is trained in an unsupervised manner using masked language modeling (MLM) as the learning signal [E7]. Notably, REALM achieves its superior performance while retrieving significantly fewer documents—specifically 5 documents—compared to other retrieval-based systems that typically retrieve between 20 and 80 documents [E1].

**Pre-training**
The core of REALM's improvement over systems like ORQA is its pre-training method [E1]. Unlike standard language models that store world knowledge implicitly in neural network parameters, REALM's retrieval-augmented pre-training captures knowledge in a more modular and interpretable way [E7]. The goal of this pre-training is to learn useful representations of language from unlabeled text corpora to improve generalization for downstream tasks [E6]. The pre-training method is versatile and can be applied to both single-corpus settings (where the input and knowledge corpora are the same, such as Wikipedia) and separate-corpus settings [E1].

**Downstream Fine-tuning**
The pre-trained model can be further trained through fine-tuning for the downstream Open-QA task, which often leads to better generalization than training from scratch [E6]. During fine-tuning, the model's generative process is decomposed into two distinct steps: retrieving documents and then predicting the answer [E3]. REALM achieves new state-of-the-art results across three benchmarks, outperforming previous systems by 4-16% absolute accuracy [E6].

### Metrics

- baseline_latency_seconds: 6.241
- orchestrator_latency_seconds: 35.582
- baseline_total_tokens: 4915
- orchestrator_total_tokens: 19846
- baseline_citation_count: 5
- orchestrator_evidence_count: 8
- fact_check_status_counts: {'supported': 12}

## Question 12

Type: multi-step reasoning

Explain step by step how a masked-language-model pre-training objective can improve downstream open-domain QA in REALM.

### Baseline Answer

In REALM, the masked-language-model (MLM) pre-training objective improves downstream open-domain question answering (Open-QA) through the following process:

1.  **Unsupervised Pre-training with MLM**: The model is pre-trained on an unlabeled corpus using a masked language modeling objective [1]. In this task, tokens are randomly masked in a text passage, and the model must predict the missing tokens [1].
2.  **Learning Knowledge through Retrieval**: Unlike standard language models that store world knowledge implicitly in their parameters [2], REALM augments pre-training with a learned textual knowledge retriever [2, 5]. The retriever identifies potentially helpful documents from a large corpus (such as Wikipedia) to assist in predicting the masked tokens [2, 5].
3.  **Performance-Based Learning Signal**: The retriever is trained using a performance-based signal from the unsupervised text [5]. A retrieval that improves the language model's perplexity is rewarded, while uninformative retrievals are penalized [5]. This is achieved by modeling the retrieve-then-predict approach as a latent variable language model and optimizing the marginal likelihood [5].
4.  **End-to-End Training**: The signal from the MLM objective backpropagates through the retrieval step, allowing the model to learn to decide what knowledge to retrieve and use [2, 5].
5.  **Transfer to Downstream Open-QA**: Because the retriever is designed to retrieve text rather than labeled examples, it can transfer to other tasks [5]. During fine-tuning, the pre-trained retriever and knowledge-augmented encoder are applied to the Open-QA task, where the model uses the retriever to find relevant documents to inform its answer to a question [2, 5].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-2-7f240c64641ad3f52fc62e97, chunk_index: 2
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2, chunk

### Multi-Agent Answer

In REALM, a masked-language-model (MLM) pre-training objective improves downstream open-domain question answering (Open-QA) through the following steps:

1.  **Unsupervised Representation Learning**: During the pre-training phase, the model learns useful representations from unlabeled text corpora [E1]. Specifically, for the MLM pre-training task, the model must predict the original value of each $[MASK]$ token within an input text passage [E4].
2.  **Encoding Knowledge**: This MLM pre-training process allows the model to encode syntactic, semantic, and world knowledge [E1].
3.  **Unsupervised Retriever Training**: REALM uses the MLM task as a learning signal to train a latent knowledge retriever in an unsupervised manner [E2]. The training uses a performance-based signal where retrievals that improve the language model's perplexity are rewarded, while uninformative retrievals are penalized [E3].
4.  **Modular Knowledge Storage**: Unlike traditional models that store world knowledge implicitly in neural network parameters, REALM augments the language model with a learned textual knowledge retriever to capture knowledge in a more modular and interpretable way [E2].
5.  **Improved Generalization for Downstream Tasks**: The resulting pre-trained model can then be fine-tuned for a downstream task, such as Open-QA [E1]. This process often leads to better generalization than training from scratch [E1].

### Metrics

- baseline_latency_seconds: 6.257
- orchestrator_latency_seconds: 59.743
- baseline_total_tokens: 5874
- orchestrator_total_tokens: 38428
- baseline_citation_count: 5
- orchestrator_evidence_count: 12
- fact_check_status_counts: {'unsupported': 5, 'supported': 7}

## Question 13

Type: multi-step reasoning / error analysis

If REALM retrieves an irrelevant document, how would that affect p(z|x), p(y|z,x), and the final answer prediction?

### Baseline Answer

If REALM retrieves an irrelevant document, the effects are as follows:

*   **$p(z|x)$**: The retrieval process models the probability of a document $z$ given an input $x$ [3]. An irrelevant document would result in a lower relevance score $f(x, z)$, as relevance is defined by the inner product of the vector embeddings of $x$ and $z$ [3].
*   **$p(y|z,x)$**: If the retrieved document $z$ is irrelevant to $x$, it may lead to a negative Retrieval Utility (RU) [1]. A negative RU indicates that $z$ is less useful for predicting $y$ than a null document [1]. This can occur if $z$ is irrelevant to $x$, if the masked tokens in $x$ do not require world knowledge, or if the necessary world knowledge is already contained within the model's parameters [1].
*   **Final answer prediction**: The overall likelihood of generating an answer $y$, denoted as $p(y|x)$, is obtained by marginalizing over all possible documents $z$ in the corpus $Z$ [3]. Specifically, $p(y|x) = \sum_{z \in Z} p(y|z, x) p(z|x)$ [3]. Because the model is trained to reward helpful retrievals (those that improve perplexity) and penalize uninformative ones, the training signal is designed to optimize this marginal likelihood [4].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-20-58cd33db77feaae8a3f8d036, chunk_index: 20
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7, chunk_index: 3
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f

### Multi-Agent Answer

The provided evidence does not contain specific information regarding the exact mathematical impact of an irrelevant document on the probability $p(z|x)$ or the conditional probability $p(y|z,x)$ [E1, E3].

However, the evidence provides the following information regarding retrieval utility and prediction:

*   **Retrieval Utility (RU):** The utility of a retrieval is defined as $\text{RU} = \log p(y | z, x) - \log p(y | \emptyset, x)$ [E1].
*   **Impact of Irrelevance on RU:** A negative RU indicates that the retrieved document $z$ is less useful for predicting the target $y$ than a null document $\emptyset$ [E1]. This negative utility may suggest that the document $z$ is irrelevant to $x$ [E1].
*   **Impact on Predictions:** While the specific mathematical shift for an irrelevant document is not detailed, the evidence indicates that REALM's performance improves when it manages to retrieve documents containing related facts [E5]. For example, in a "Fermat" prediction task, the marginal probability over the top 8 retrieved documents was 0.129, compared to a BERT (no retrieval) probability of $1.1 \times 10^{-14}$ [E5].

### Metrics

- baseline_latency_seconds: 6.748
- orchestrator_latency_seconds: 56.231
- baseline_total_tokens: 5064
- orchestrator_total_tokens: 35645
- baseline_citation_count: 5
- orchestrator_evidence_count: 8
- fact_check_status_counts: {'unsupported': 1, 'supported': 5}

## Question 14

Type: limitation/uncertainty

What limitations, uncertainties, or missing comparisons should be noted when interpreting REALM's reported results?

### Baseline Answer

When interpreting REALM's reported results, the following limitations, uncertainties, and missing comparisons should be noted:

*   **Missing Data:** Certain data that could potentially benefit REALM was not used in the experiments [1].
*   **Uncertainty in Retrieval Utility (RU):** A negative RU indicates that the document $z$ is less useful for predicting $y$ than a null document; however, this uncertainty arises because it could mean the document is irrelevant to $x$, the masked tokens in $x$ do not require world knowledge to predict, or the necessary world knowledge is already sufficiently commonplace within the model's parameters [2].
*   **Optimization Limitations:** While the researchers compared the system against a slower refresh rate for the MIPS index, results suggest that a "stale index" can hurt model training, and further reducing this staleness might offer better optimization [4].
*   **Scope of Current Work:** The presented work is considered a "minimal instantiation" of a family of REALM-like approaches [5]. Future generalizations to structured knowledge, multi-lingual settings, and multi-modal settings (such as retrieving images or videos) have not yet been addressed [5].

### Multi-Agent Answer

When interpreting REALM's reported results, the following limitations, uncertainties, and technical requirements should be noted:

*   **Data Limitations:** Certain data that could potentially benefit REALM was not utilized in the researchers' experiments [E1].
*   **Uncertainty in Retrieval Utility (RU):** A negative Retrieval Utility (RU) score does not definitively identify why a retrieval was poor; it may indicate that the document is irrelevant to the input, that the masked tokens do not require world knowledge, or that the necessary world knowledge is already baked into the model's parameters [E6].
*   **Component Dependency:** While both the encoder and the retriever benefit from being trained separately, achieving optimal results requires both components to act in unison [E2].
*   **Index Maintenance:** Using a stale MIPS index can negatively impact model training, which necessitates frequent index refreshes [E2].

### Metrics

- baseline_latency_seconds: 3.523
- orchestrator_latency_seconds: 26.606
- baseline_total_tokens: 4368
- orchestrator_total_tokens: 18620
- baseline_citation_count: 5
- orchestrator_evidence_count: 9
- fact_check_status_counts: {'supported': 4}

## Question 15

Type: citation grounding / uncertainty

Which claims about REALM's performance or mechanism cannot be verified unless the answer cites specific experimental evidence from the paper?

### Baseline Answer

Based on the provided context, the following claims about REALM's performance or mechanism cannot be verified without citing specific experimental evidence (such as results from the referenced Tables):

*   **Performance relative to ORQA:** The claim that the improvement of REALM over ORQA is "purely due to better pre-training methods" requires verification through the experimental comparison where hyperparameters and training data are identical [1].
*   **Performance relative to other retrieval-based systems:** The claim that REALM achieves the "overall best performance" while retrieving only 5 documents compared to other systems that retrieve 20 to 80 documents requires verification via experimental results [1].
*   **Impact of component ablation:** Claims regarding the end-to-end results for NaturalQuestions-Open after ablating critical components of REALM require the data presented in Table 2 [1, 4].
*   **Encoder and Retriever benefits:** The claim that both the encoder and retriever benefit from REALM training separately, but that the "best result requires both components acting in unison," requires verification through the ablation experiments described [4].
*   **MIPS index refresh rate:** The claim that a "stale index can hurt model training" and that reducing staleness could offer better optimization requires verification from the results in Table 2 [4].
*   **Effectiveness of masking schemes:** The claim that salient span masking is "crucial for REALM" (unlike its effect in standard BERT training) requires verification through the comparison of masking schemes [4].
*   **Retrieval Utility (RU) behavior:** The claim that RU is more predictive of good performance on the downstream task of Open-QA than the overall log-likelihood requires verification from the analysis and Figure 4 [3].

### Multi-Agent Answer

Based on the provided evidence notes, the following claims regarding REALM's mechanism and performance are verified:

**Mechanisms**
*   REALM utilizes a "retrieve-then-predict" generative process that decomposes learning the distribution $p(y|x)$ into retrieving documents $z$ from a knowledge corpus $Z$ (modeling $p(z|x)$) and then conditioning on both the retrieved documents and the original input to generate the output $y$ (modeling $p(y|z, x)$) [E3].
*   The neural knowledge retriever employs a dense inner product model, where relevance scores are determined by the inner product of $d$-dimensional vector embeddings [E3].
*   To manage the computational challenge of selecting from millions of candidate documents, the retriever uses Maximum Inner Product Search (MIPS) [E5].
*   Asynchronous MIPS refreshes are implemented through two parallel jobs: a primary trainer job that performs gradient updates and a secondary index builder job that embeds and indexes documents [E4].
*   The model utilizes salient span masking, such as masking named entities or dates, to focus on examples that require world knowledge [E4].

**Performance**
*   REALM achieves new state-of-the-art results on Open-domain Question Answering (Open-QA) benchmarks, specifically outperforming previous systems by 4-16% absolute accuracy across the Natural Questions-Open, Web Questions, and Curated TREC benchmarks [E5].
*   Compared to other retrieval-based systems that often retrieve between 20 to 80 documents, REALM achieves its best overall performance while retrieving only 5 documents [E1].
*   The improvement of REALM over ORQA is attributed purely to better pre-training methods [E1].
*   Retrieval Utility (RU) is more predictive of good performance on the Open-QA downstream task than the overall log-likelihood [E2].

### Metrics

- baseline_latency_seconds: 4.436
- orchestrator_latency_seconds: 49.698
- baseline_total_tokens: 4472
- orchestrator_total_tokens: 36953
- baseline_citation_count: 5
- orchestrator_evidence_count: 8
- fact_check_status_counts: {'unsupported': 2, 'supported': 9}
