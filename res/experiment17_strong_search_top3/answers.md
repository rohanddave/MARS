# experiment17: retrieval sweep, strong search agent only, top_k=3

## Agent Configuration

- family: top_k_sweep
- control_variable: top_k
- top_k: 3
- max_evidence_chunks: 3
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

REALM retrieves information from a large textual knowledge corpus, such as Wikipedia [1, 2].

The model uses this corpus through a "retrieve-then-predict" process [1, 3]:
1.  **Retrieve:** Given an input $x$, the model uses a learned neural knowledge retriever to retrieve potentially helpful documents $z$ from the corpus $Z$ [1, 3]. This is modeled as a sample from the distribution $p(z|x)$ [3].
2.  **Predict:** The language model then attends over the retrieved documents to help inform its prediction, generating an output $y$ by conditioning on both the original input $x$ and the retrieved documents $z$—modeled as $p(y|z, x)$ [1, 3].

During pre-training, the retriever is trained in an unsupervised manner using a performance-based signal from unsupervised text, where retrievals that improve the language model's perplexity are rewarded [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7

### Multi-Agent Answer

REALM retrieves information from a large knowledge corpus, such as Wikipedia [E2, E3]. The retriever considers millions of documents or passages from this corpus [E1, E2, E3].

The model utilizes this retrieved information through a "retrieve-then-predict" paradigm [E1]. This process is used during pre-training, fine-tuning, and inference [E3].

*   **Retrieval:** Based on an input $x$, the model retrieves a document $z$ from the knowledge corpus $Z$ [E1]. The retriever uses a neural knowledge retriever based on a dense inner product model to calculate relevance scores using $d$-dimensional vector embeddings [E1].
*   **Prediction:** The model generates an output $y$ by conditioning it on both the original input $x$ and the retrieved document $z$ [E1].

### Metrics

- baseline_latency_seconds: 6.439
- orchestrator_latency_seconds: 44.186
- baseline_total_tokens: 3807
- orchestrator_total_tokens: 26470
- baseline_citation_count: 3
- orchestrator_evidence_count: 5
- fact_check_status_counts: {'unsupported': 3, 'supported': 5}

## Question 2

Type: easy lookup

Which downstream tasks or benchmarks does the paper use to evaluate REALM?

### Baseline Answer

The paper uses NaturalQuestions-Open to present results after ablating critical components of REALM [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05, chunk_index: 12

### Multi-Agent Answer

The paper evaluates REALM using three Open-QA datasets: NQ, WQ, and CT [E4].

### Metrics

- baseline_latency_seconds: 2.897
- orchestrator_latency_seconds: 15.865
- baseline_total_tokens: 2299
- orchestrator_total_tokens: 11707
- baseline_citation_count: 3
- orchestrator_evidence_count: 4
- fact_check_status_counts: {'supported': 1}

## Question 3

Type: definition

What is REALM, and what does the paper mean by retrieval-augmented language model pre-training?

### Baseline Answer

REALM (Retrieval-Augmented Language Model) is a novel framework that augments language model pre-training algorithms with a learned textual knowledge retriever [1, 2]. Unlike traditional models that store world knowledge implicitly within their parameters, REALM captures knowledge in a more modular and interpretable way by explicitly exposing the role of world knowledge, requiring the model to decide what knowledge to retrieve and use during inference [1, 2].

The paper's concept of retrieval-augmented language model pre-training involves the following:

*   **Process:** The framework decomposes the task into a "retrieve-then-predict" generative process [3]. Given an input $x$, the model first retrieves potentially helpful documents $z$ from a large knowledge corpus $Z$ (such as Wikipedia) [1, 3]. It then attends over those retrieved documents to inform its prediction of the output $y$ [1].
*   **Pre-training Task:** During pre-training, the specific task used is masked language modeling, where the model must predict the value of tokens that have been masked out in a sentence from a pre-training corpus [3].
*   **Learning Mechanism:** The retriever is trained in an unsupervised manner using a performance-based signal from unsupervised text [1]. Specifically, the model uses masked language modeling as the learning signal, where a retrieval that improves the language model's perplexity is rewarded, while uninformative retrieval is penalized [1, 2]. This is achieved by modeling the approach as a latent variable language model and optimizing the marginal likelihood [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59

### Multi-Agent Answer

REALM (Retrieval-Augmented Language Model) is a framework designed to capture knowledge in a more modular and interpretable way [E1, E2]. Unlike traditional language models that store world knowledge implicitly in neural network parameters [E2], REALM augments language model pre-training with a learned, latent textual knowledge retriever [E1, E2]. This approach explicitly exposes the role of world knowledge by requiring the model to decide what knowledge to retrieve and use during inference [E1].

In this paper, retrieval-augmented language model pre-training refers to the process of augmenting language model pre-training algorithms with a learned textual knowledge retriever [E1]. This retriever allows the model to retrieve documents from a large corpus, such as Wikipedia, and then attend over those documents to help inform its predictions [E1, E2]. The retriever can be pre-trained in an unsupervised manner using masked language modeling as a learning signal [E2].

### Metrics

- baseline_latency_seconds: 7.416
- orchestrator_latency_seconds: 38.709
- baseline_total_tokens: 3910
- orchestrator_total_tokens: 25476
- baseline_citation_count: 3
- orchestrator_evidence_count: 6
- fact_check_status_counts: {'unsupported': 2, 'supported': 6}

## Question 4

Type: definition

How does REALM differ from a standard parametric language model such as BERT in where knowledge is stored and accessed?

### Baseline Answer

Standard parametric language models, such as BERT, store world knowledge implicitly within the parameters of the underlying neural network [1]. This approach makes it difficult to determine what knowledge is stored and where, and storage space is limited by the size of the network, requiring ever-larger networks to capture more facts [1].

In contrast, REALM (Retrieval-Augmented Language Model) differs by augmenting language model pre-training with a learned textual knowledge retriever [1, 2]. Instead of relying solely on stored parameters, REALM explicitly exposes the role of world knowledge by having the model decide what knowledge to retrieve and use during inference [2]. The model uses the retriever to pull documents from a large corpus (such as Wikipedia) and then attends over those documents to inform its predictions [1, 2]. This method provides more interpretable and modular memories because each memory is grounded and associated with a specific document rather than unnamed value vectors [3].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-15-e73576ceacc6e97a0666fd10

### Multi-Agent Answer

Unlike models that store knowledge in their parameters [E1], REALM augments language model pre-training with a learned textual knowledge retriever [E1]. In the REALM framework, the model explicitly exposes the role of world knowledge by deciding what to retrieve and use during inference [E1]. Before making each prediction, the language model uses the retriever to pull documents from a large corpus, such as Wikipedia, and then attends over those documents to help inform its prediction [E1].

The provided evidence does not explicitly detail the specific knowledge storage and access mechanisms of BERT to allow for a direct comparison, although it notes that REALM's embedding functions are implemented using BERT-style Transformers [E2].

### Metrics

- baseline_latency_seconds: 4.723
- orchestrator_latency_seconds: 21.691
- baseline_total_tokens: 3881
- orchestrator_total_tokens: 14992
- baseline_citation_count: 3
- orchestrator_evidence_count: 4
- fact_check_status_counts: {'supported': 4}

## Question 5

Type: method/mechanism

How does REALM's retrieve-then-predict framework work, including the role of the latent document variable z?

### Baseline Answer

REALM’s retrieve-then-predict framework decomposes the learning of a distribution $p(y|x)$ over possible outputs $y$ into two steps: first, retrieving potentially helpful documents $z$ from a knowledge corpus $Z$ based on an input $x$, and second, conditioning on both the retrieved $z$ and the original input $x$ to generate the output $y$ [3].

The process is modeled as follows:
*   **Retrieval:** The model samples a document $z$ from the distribution $p(z|x)$ [3]. The retriever is defined using a dense inner product model where the relevance score $f(x, z)$ is the inner product of the vector embeddings of the input and the document [3].
*   **Prediction:** The model generates the output $y$ by modeling $p(y|z, x)$ [3].

**Role of the latent document variable $z$:**
The document $z$ is treated as a latent variable [3]. To obtain the overall likelihood of generating an output $y$ given an input $x$, the model marginalizes over all possible documents $z$ in the corpus $Z$ [3]. This is expressed by the formula:
$$p(y|x) = \sum_{z \in Z} p(y|z, x)p(z|x)$$ [3].

Citations:
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7

### Multi-Agent Answer

REALM's retrieve-then-predict framework augments language model pre-training by incorporating a learned textual knowledge retriever [E1]. This framework decomposes the probability of an output $y$ given an input $x$, $p(y|x)$, into a two-step generative process [E3].

The process works as follows:
*   First, the model retrieves documents $z$ from a large knowledge corpus $Z$ based on the input, represented as $p(z|x)$ [E3].
*   Second, the model predicts the output $y$ by conditioning on both the original input and the retrieved documents, represented as $p(y|z, x)$ [E3].

The framework models the overall likelihood by treating $z$ as a latent variable, following the formula $p(y |x) = \sum_{z \in Z} p(y |z, x) p(z |x)$ [E3]. In practice, the language model uses the retriever to select documents from a large corpus, such as Wikipedia, and then attends over those documents to inform its prediction [E1].

### Metrics

- baseline_latency_seconds: 4.698
- orchestrator_latency_seconds: 24.826
- baseline_total_tokens: 3396
- orchestrator_total_tokens: 15354
- baseline_citation_count: 3
- orchestrator_evidence_count: 5
- fact_check_status_counts: {'supported': 7}

## Question 6

Type: method/mechanism

How does the paper train the retriever when the retrieved document is latent, and how does learning signal flow back to retrieval?

### Baseline Answer

The paper trains the retriever by modeling the "retrieve-then-predict" approach as a latent variable language model and optimizing the marginal likelihood [1]. The retriever is trained using a performance-based signal from unsupervised text, where retrievals that improve the language model's perplexity are rewarded, while uninformative retrievals are penalized [1]. Specifically, the paper uses masked language modeling as the learning signal to pre-train the knowledge retriever in an unsupervised manner [2].

The learning signal flows back to the retrieval by backpropagating through the retrieval step, which considers an entire corpus of textual knowledge [1]. The signal from the language modeling objective backpropagates "all the way through the retriever" [2]. To manage the computational challenge of backpropagating through millions of candidate documents, the retriever is structured so that computations for each document can be cached and updated asynchronously, and document selection is formulated as Maximum Inner Product Search (MIPS) [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2

### Multi-Agent Answer

The REALM framework models the retrieve-then-predict approach as a latent variable language model that optimizes marginal likelihood [E1]. 

To train the retriever, the model uses a performance-based signal derived from unsupervised text [E1]. Specifically, the retriever is rewarded when it retrieves information that improves the language model's perplexity and is penalized when it provides uninformative retrieval [E1]. This unsupervised pre-training can utilize masked language modeling as the learning signal [E2].

Learning the model end-to-end involves backpropagating through a retrieval step that considers an entire corpus of textual knowledge, which can consist of millions of documents [E1][E2].

### Metrics

- baseline_latency_seconds: 4.846
- orchestrator_latency_seconds: 19.583
- baseline_total_tokens: 2985
- orchestrator_total_tokens: 14499
- baseline_citation_count: 3
- orchestrator_evidence_count: 5
- fact_check_status_counts: {'supported': 5}

## Question 7

Type: method/mechanism / implementation

What approximations or engineering choices does REALM use to make retrieval over a large corpus practical during training and inference?

### Baseline Answer

To address the significant computational challenge of a retriever that must consider millions of candidate documents for each pre-training step, REALM uses the following engineering choices:

*   **Caching and Asynchronous Updates:** The retriever is structured so that the computation performed for each individual document can be cached and updated asynchronously [2].
*   **Maximum Inner Product Search (MIPS):** The selection of the best documents is formulated as a Maximum Inner Product Search (MIPS) [2].

Additionally, while other retrieval-based systems often retrieve between 20 to 80 documents, REALM achieves its best performance while only retrieving 5 documents [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05, chunk_index: 12
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952, chunk_index: 1

### Multi-Agent Answer

To make retrieval over a large corpus of millions of documents practical [E1, E3], REALM employs the following engineering choices and approximations:

*   **Document Selection Method:** The retriever uses Maximum Inner Product Search (MIPS) to select documents [E1].
*   **Update Structure:** The retriever is structured to allow for both cached and asynchronous updates [E1].
*   **Retrieval Volume:** While other retrieval-based systems typically retrieve between 20 and 80 documents, REALM achieves its performance by retrieving only 5 documents [E2].

### Metrics

- baseline_latency_seconds: 3.379
- orchestrator_latency_seconds: 18.137
- baseline_total_tokens: 2863
- orchestrator_total_tokens: 13046
- baseline_citation_count: 3
- orchestrator_evidence_count: 4
- fact_check_status_counts: {'supported': 3}

## Question 8

Type: comparison

How does REALM compare with ORQA or other open-domain QA baselines, and what evidence supports that comparison?

### Baseline Answer

REALM compares to ORQA as its most direct comparison, as they utilize identical training data, hyperparameters, and fine-tuning setups [1]. The improvement REALM shows over ORQA is attributed entirely to better pre-training methods [1]. Both systems initialize their retrievers using the Inverse Cloze Task [2].

Regarding other open-domain QA baselines:
* **Retrieval-based systems:** Compared to other retrieval-based systems (such as Asai et al., 2019; Min et al., 2019a;b), which often retrieve between 20 to 80 documents, REALM achieves the overall best performance while only retrieving 5 documents [1].
* **Generation-based systems:** For a competitive generation-based baseline, REALM is compared against concurrent work that fine-tunes T5 for Open-QA (Roberts et al., 2020) [2].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-10-8ea61faa3a17c1fc8f8725d8

### Multi-Agent Answer

ORQA is considered the most direct comparison to REALM because the fine-tuning setup, hyperparameters, and training data are identical [E1]. Additionally, the retrievers for both REALM pre-training and ORQA are initialized using the Inverse Cloze Task [E2]. 

The improvement of REALM over ORQA is attributed purely to better pre-training methods [E1]. Among all retrieval-based systems, REALM achieves the overall best performance despite retrieving fewer documents [E1]. Specifically, REALM retrieves only 5 documents, while other retrieval-based systems often retrieve between 20 and 80 documents [E1].

### Metrics

- baseline_latency_seconds: 4.293
- orchestrator_latency_seconds: 19.086
- baseline_total_tokens: 2791
- orchestrator_total_tokens: 11358
- baseline_citation_count: 3
- orchestrator_evidence_count: 4
- fact_check_status_counts: {'supported': 5}

## Question 9

Type: comparison

How does REALM's retrieval-based approach compare with storing knowledge only in model parameters?

### Baseline Answer

In contrast to models that store world knowledge implicitly in their parameters, REALM's retrieval-based approach offers the following differences:

*   **Interpretability and Modularity:** REALM captures knowledge in a more modular and interpretable way [1, 3]. Because knowledge is stored in parameters implicitly, it is difficult to determine what knowledge is stored in a network and where [3].
*   **Explicit Knowledge Use:** REALM explicitly exposes the role of world knowledge by requiring the model to decide what knowledge to retrieve and use during inference [1]. The model uses a retriever to pull documents from a large corpus (such as Wikipedia) and attends over them to inform its predictions [1].
*   **Scalability of Knowledge:** In models where knowledge is stored in parameters, storage space is limited by the size of the network, meaning ever-larger networks must be trained to capture more facts, which can be expensive or slow [3]. 

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952, chunk_index: 1
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2, chunk_index: 0

### Multi-Agent Answer

In contrast to models that store knowledge within their parameters, REALM's approach explicitly exposes the role of world knowledge [E2]. This is achieved by requiring the model to decide what knowledge to retrieve and use during the inference process [E2]. Specifically, before making a prediction, the language model uses a learned textual knowledge retriever to retrieve documents from a large corpus and then attends over those documents to help inform its prediction [E2]. This framework provides qualitative benefits in terms of modularity and interpretability [E2].

### Metrics

- baseline_latency_seconds: 5.202
- orchestrator_latency_seconds: 19.564
- baseline_total_tokens: 2922
- orchestrator_total_tokens: 12464
- baseline_citation_count: 3
- orchestrator_evidence_count: 4
- fact_check_status_counts: {'supported': 4}

## Question 10

Type: evidence synthesis / ablation

What ablation or diagnostic evidence shows that retrieval pre-training improves REALM rather than only the reader component?

### Baseline Answer

To isolate the contribution of improving the retriever during pre-training, the researchers report a metric measuring how often the gold answer appears in the top-5 retrievals before any fine-tuning is applied [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05, chunk_index: 12

### Multi-Agent Answer

The provided evidence does not contain any ablation or diagnostic studies that specifically isolate whether retrieval pre-training improves the REALM retriever or the reader component [E1, E2, E3]. 

While the notes state that REALM's retriever is trained using a performance-based signal from unsupervised text—where retrievals that improve the language model's perplexity are rewarded [E2]—the evidence does not provide diagnostic results or comparative data to separate the performance gains of the retriever from those of the reader [E2].

### Metrics

- baseline_latency_seconds: 2.545
- orchestrator_latency_seconds: 35.972
- baseline_total_tokens: 2698
- orchestrator_total_tokens: 22978
- baseline_citation_count: 3
- orchestrator_evidence_count: 8
- fact_check_status_counts: {'unsupported': 1, 'supported': 1}

## Question 11

Type: evidence synthesis

Synthesize the evidence for why REALM improves open-domain QA performance, including retrieval quality, pre-training, and downstream fine-tuning.

### Baseline Answer

REALM improves open-domain QA performance through the following factors:

*   **Pre-training:** The improvement of REALM over the ORQA system is attributed purely to better pre-training methods [1]. REALM extends the retrieval-based paradigm to language model pre-training [2]. This pre-training method can be applied in both single-corpus settings (where the pre-training corpus $X$ and knowledge corpus $Z$ are both Wikipedia) and separate-corpus settings (where $X$ is CC-News and $Z$ is Wikipedia) [1].
*   **Retrieval Quality:** REALM demonstrates superior retrieval efficiency and effectiveness, achieving its overall best performance while retrieving only 5 documents [1]. This contrasts with other retrieval-based systems that often retrieve between 20 to 80 documents [1]. Additionally, the contribution of improving the retriever during pre-training can be isolated by measuring how often the gold answer appears in the top-5 retrievals before any fine-tuning is applied [1].
*   **Downstream Fine-tuning:** For the fine-tuning task of Open-QA, the model takes a question as input $x$ and learns to predict the answer $y$ [2]. During fine-tuning inference, the system considers the top-5 candidates from the knowledge corpus [3].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-10-8ea61faa3a17c1fc8f8725d8

### Multi-Agent Answer

REALM improves open-domain question answering (Open-QA) performance by augmenting language model pre-training with a learned textual knowledge retriever [E1]. This approach captures knowledge in a more modular and interpretable way compared to models that store knowledge implicitly in neural network parameters [E1, E2]. Consequently, REALM achieves an absolute accuracy improvement of 4-16% across three benchmarks: Natural Questions, Web Questions, and Curated TREC [E1].

**Retrieval Quality**
The REALM retriever is designed to retrieve documents from a large corpus, such as Wikipedia, and allows the model to attend over those documents [E1, E2]. The retriever is trained using a performance-based signal from unsupervised text, where retrievals that improve the language model's perplexity are rewarded, while uninformative retrievals are penalized [E1]. This training method enables REALM to achieve superior performance while retrieving fewer documents—specifically five documents for its best performance—compared to other retrieval-based systems that typically retrieve between 20 and 80 documents [E3]. Additionally, the retriever is designed to transfer to other tasks because it retrieves raw text rather than labeled examples [E1].

**Pre-training and Fine-tuning**
The retriever can be pre-trained in an unsupervised manner using masked language modeling as the learning signal [E2]. This pre-training method is versatile and can be applied to both single-corpus settings (Wikipedia/Wikipedia) and separate-corpus settings (CC-News/Wikipedia) [E3]. The improvement of REALM over the ORQA system is attributed entirely to these superior pre-training methods, as the fine-tuning setups, hyperparameters, and training data are identical between the two [E3].

### Metrics

- baseline_latency_seconds: 5.698
- orchestrator_latency_seconds: 45.251
- baseline_total_tokens: 2855
- orchestrator_total_tokens: 24217
- baseline_citation_count: 3
- orchestrator_evidence_count: 7
- fact_check_status_counts: {'supported': 9, 'unsupported': 2}

## Question 12

Type: multi-step reasoning

Explain step by step how a masked-language-model pre-training objective can improve downstream open-domain QA in REALM.

### Baseline Answer

In REALM, a masked-language-model (MLM) pre-training objective improves downstream open-domain question answering (Open-QA) through the following process:

1.  **MLM Pre-training Task**: The model is trained on an unlabeled pre-training corpus (such as Wikipedia) by randomly masking tokens in a text passage [1]. The model must then use its representation of the masked input to predict the missing tokens [1].
2.  **Learning Representations and Knowledge**: To successfully predict masked tokens, the MLM must learn to encode syntactic and semantic information as well as world knowledge [1].
3.  **Augmentation with a Knowledge Retriever**: Unlike standard models that store knowledge implicitly in their parameters, REALM augments pre-training with a learned textual knowledge retriever [2]. This allows the model to retrieve and attend over documents from a large knowledge corpus (e.g., Wikipedia) during the pre-training stage [2].
4.  **Unsupervised Training Signal**: The MLM serves as an unsupervised learning signal [2]. The signal from the language modeling objective is backpropagated through the retrieval step, which considers millions of documents [2].
5.  **Retrieve-then-Predict Process**: The pre-training decomposes the generation of the output $y$ into two steps: first, retrieving potentially helpful documents $z$ from a corpus $Z$ based on the input $x$, and second, conditioning on both the retrieved documents and the original input to predict the missing tokens $y$ [3].
6.  **Transfer to Downstream Open-QA**: The resulting pre-trained model can be fine-tuned for the Open-QA task, where the input $x$ is a question and the output $y$ is the correct answer string [1, 3]. Because the model was pre-trained to retrieve and use external documents to solve the MLM task, it is better equipped for Open-QA, which requires retaining knowledge from millions of documents [3].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-2-7f240c64641ad3f52fc62e97
[2] source: data/2002.08909v1.pdf, chunk_id: 20

### Multi-Agent Answer

The masked-language-model (MLM) pre-training objective improves downstream open-domain question answering (Open-QA) in REALM through the following steps:

1.  **Unsupervised Pre-training with MLM**: The process begins with unsupervised pre-training where the model uses MLM as a learning signal [E3]. In this task, the model is trained to predict the original value of each [MASK] token within an input text passage $x$ [E2].
2.  **Learning Representations and Knowledge**: The primary goal of this pre-training is to learn useful language representations from unlabeled text corpora [E1]. Through this MLM objective, a successful model learns to encode syntactic information, semantic information, and world knowledge [E1]. Learning these representations through pre-training often leads to better generalization on downstream tasks than training from scratch [E1].
3.  **Augmentation with a Latent Retriever**: Unlike traditional pre-training, which stores world knowledge implicitly in neural network parameters [E3], REALM augments the pre-training process with a latent knowledge retriever [E3]. This retriever allows the model to retrieve and attend over documents from a large corpus, such as Wikipedia, during the pre-training stage [E3].
4.  **Learning via Backpropagation**: The model learns by backpropagating the signal from the language modeling objective through a retrieval step that can consider millions of documents [E3].
5.  **Fine-tuning for Open-QA**: After pre-training, the resulting model can be fine-tuned for the downstream task of Open-QA [E1]. During Open-QA fine-tuning, the architecture aims to produce an answer string $y$ that is assumed to be a contiguous sequence of tokens in a document $z$ [E2].

### Metrics

- baseline_latency_seconds: 6.040
- orchestrator_latency_seconds: 45.276
- baseline_total_tokens: 3580
- orchestrator_total_tokens: 24453
- baseline_citation_count: 3
- orchestrator_evidence_count: 7
- fact_check_status_counts: {'unsupported': 5, 'supported': 7}

## Question 13

Type: multi-step reasoning / error analysis

If REALM retrieves an irrelevant document, how would that affect p(z|x), p(y|z,x), and the final answer prediction?

### Baseline Answer

If REALM retrieves an irrelevant document $z$, the effects are as follows:

*   **$p(z|x)$**: This is the distribution modeled by the neural knowledge retriever [3]. While the context does not explicitly state how $p(z|x)$ changes when a document is irrelevant, it defines the retriever as using a dense inner product model where the relevance score $f(x, z)$ is the inner product of vector embeddings [3].
*   **$p(y|z,x)$**: A negative Retrieval Utility (RU) can indicate that $z$ is less useful for predicting $y$ than a null document, which could mean that $z$ is irrelevant to $x$ [1].
*   **Final answer prediction $p(y|x)$**: The overall likelihood is obtained by marginalizing over all possible documents $z$, calculated as $p(y |x) = \sum_{z \in Z} p(y |z, x) p(z |x)$ [3]. In an example where REALM retrieves documents with a related fact, the marginalized probability of the correct answer "dramatically increases" [2]. Conversely, if the retrieved documents do not contain the necessary information (such as when the knowledge corpus is outdated), the model may not be able to recover the correct token [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-20-58cd33db77feaae8a3f8d036
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7

### Multi-Agent Answer

The provided evidence does not contain specific information regarding how an irrelevant document directly affects the individual probability term $p(z|x)$ [E1, E2].

Regarding the other components of the generative process:

*   **$p(y|z,x)$ and Retrieval Utility (RU):** If a retrieved document $z$ is irrelevant to $x$, it may result in a negative Retrieval Utility (RU) [E1]. A negative RU indicates that the document $z$ is less useful for predicting the target $y$ than a null document $\emptyset$ [E1]. The relationship between these terms is defined by the formula $RU = \log p(y | z, x) - \log p(y | \emptyset, x)$ [E1].
*   **Final Answer Prediction:** The REALM model decomposes the output distribution $p(y|x)$ into two steps: retrieving documents $z$ from a corpus $Z$ (modeled as $p(z|x)$), and then conditioning on both $z$ and $x$ to generate the output $y$ (modeled as $p(y|z,x)$) [E2]. While the evidence defines this decomposition, it does not explicitly provide the mathematical formula for the final answer prediction $p(y|x)$ in relation to these terms [E1, E2].

### Metrics

- baseline_latency_seconds: 5.936
- orchestrator_latency_seconds: 44.000
- baseline_total_tokens: 3599
- orchestrator_total_tokens: 22694
- baseline_citation_count: 3
- orchestrator_evidence_count: 6
- fact_check_status_counts: {'unsupported': 3, 'supported': 4}

## Question 14

Type: limitation/uncertainty

What limitations, uncertainties, or missing comparisons should be noted when interpreting REALM's reported results?

### Baseline Answer

When interpreting REALM's reported results, the following limitations, uncertainties, or missing comparisons should be noted:

*   **Unused Data:** Certain data could have potentially benefited REALM but was not utilized in the experiments [1].
*   **Interpretations of Negative Retrieval Utility (RU):** A negative RU indicates that the document $z$ is less useful for predicting $y$ than a null document [2]. However, this result is uncertain as it could mean $z$ is irrelevant to $x$, or it could mean that the masked tokens in $x$ do not require world knowledge, or that the necessary world knowledge is already sufficiently commonplace and "baked into" the model's parameters [2].
*   **Impact of Masking and Training Steps:** The Retrieval Utility (RU) is impacted by the number of pre-training steps and the specific choice of masking used [2].

### Multi-Agent Answer

When interpreting REALM's reported results, the following limitations, uncertainties, and technical dependencies should be noted:

*   **Data Limitations:** There are certain types of data that could potentially benefit REALM, but such data was not utilized in the conducted experiments [E1].
*   **Interpretations of Negative Retrieval Utility (RU):** A negative RU indicates that a document $z$ is less useful for predicting an answer $y$ than a null document [E4]. This outcome presents several uncertainties, as it could mean the document $z$ is irrelevant to $x$, the masked tokens do not require world knowledge, or the necessary knowledge is already baked into the model's parameters [E4]. Additionally, RU is impacted by the specific choice of masking and the number of pre-training steps [E4].
*   **Component Interdependency:** While both the encoder and retriever benefit from training separately, achieving optimal results requires both components to act in unison [E2]. If both parameters are reset, the system is reduced to the ORQA baseline [E2].
*   **Index Staleness:** Using a stale MIPS index can negatively impact model training [E2].

### Metrics

- baseline_latency_seconds: 2.690
- orchestrator_latency_seconds: 21.943
- baseline_total_tokens: 1890
- orchestrator_total_tokens: 12238
- baseline_citation_count: 3
- orchestrator_evidence_count: 5
- fact_check_status_counts: {'supported': 7}

## Question 15

Type: citation grounding / uncertainty

Which claims about REALM's performance or mechanism cannot be verified unless the answer cites specific experimental evidence from the paper?

### Baseline Answer

Based on the provided text, the following claims regarding REALM's performance or mechanism require specific experimental evidence from the paper to be verified:

*   **Performance comparison to ORQA:** The claim that the improvement of REALM over ORQA is "purely due to better pre-training methods" [1].
*   **Overall best performance with minimal retrieval:** The claim that REALM "gets the overall best performance while only retrieving 5 documents" compared to other retrieval-based systems that often retrieve between 20 and 80 documents [1].
*   **Applicability of pre-training methods:** The claim that the pre-training method can be applied to both the "single-corpus setting" and the "separate-corpus setting" [1].
*   **Predictive power of Retrieval Utility (RU):** The claim that RU "is more predictive of good performance on the downstream task of Open-QA than even the overall log-likelihood" [3].
*   **Behavior of RU during pre-training:** The claim that "RU increases steadily over the course of pre-training" [3].
*   **Adaptability to updated knowledge:** The claim that a REALM model pre-trained on an outdated corpus (2018) is able to "retrieve the document in the updated corpus (2020) and generate the correct token" [3].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-20-58cd33db77feaae8a3f8d036

### Multi-Agent Answer

Based on the provided evidence, several claims regarding REALM's performance and mechanisms can be identified, but their specific results or quantitative validations cannot be verified without the experimental data from the paper:

*   **Comparison between REALM pretraining and ORQA:** While it is noted that the retrievers for both REALM pretraining and ORQA are initialized using the Inverse Cloze Task [E5], the specific results of the direct comparison between the two mentioned in Table 1 are not included in the notes [E5].
*   **Effects of model size:** Although the study measures the effect of model size by making comparisons against Base, Large, and an 11-billion parameter model [E5], the specific performance outcomes or improvements resulting from these comparisons are not detailed [E5].
*   **Perplexity reduction mechanism:** The notes state that REALM learns to identify which texts are most useful for reducing perplexity, which distinguishes it from frameworks that rely on high lexical overlap [E6]; however, the notes do not provide experimental measurements or quantitative data quantifying this reduction in perplexity [E6].
*   **Knowledge update failures:** The notes mention that a knowledge-augmented encoder may fail to reflect updates in certain predictions—for example, potentially predicting "Thatcher" for the query "is the prime minister of United Kingdom" regardless of the corpus version [E7]—but they do not provide statistical evidence or experimental data regarding the frequency or extent of these failures [E7].

### Metrics

- baseline_latency_seconds: 4.844
- orchestrator_latency_seconds: 22.161
- baseline_total_tokens: 2787
- orchestrator_total_tokens: 13460
- baseline_citation_count: 3
- orchestrator_evidence_count: 7
- fact_check_status_counts: {'supported': 4}
