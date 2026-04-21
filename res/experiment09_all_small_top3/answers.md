# experiment09: retrieval sweep, all small models, top_k=3

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

REALM retrieves from a large textual knowledge corpus, such as Wikipedia [1, 2].

The model uses this corpus through a "retrieve-then-predict" process [1, 3]:

*   **Retrieval:** Given an input $x$, the neural knowledge retriever models the distribution $p(z | x)$ to retrieve potentially helpful documents $z$ from the corpus $Z$ [3]. The relevance score between the input and a document is defined as the inner product of their vector embeddings [3].
*   **Prediction:** The language model then attends over the retrieved documents to help inform its prediction, modeling the output $y$ as $p(y | z, x)$ [1, 3]. 

This process is used during pre-training, fine-tuning, and inference [2].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7

### Multi-Agent Answer

REALM retrieves documents from a large corpus, such as Wikipedia [E2, E3]. This corpus may contain millions of documents [E1, E3].

The model utilizes this knowledge through a "retrieve-then-predict" paradigm [E1]. Specifically, the framework uses a learned textual knowledge retriever to retrieve potentially relevant documents ($z$) from the knowledge corpus ($Z$) based on an input ($x$) [E1]. The language model then attends over these retrieved documents to help inform its prediction [E2]. This retrieval and attention mechanism is utilized during the stages of pre-training, fine-tuning, and inference [E3].

### Metrics

- baseline_latency_seconds: 6.091
- orchestrator_latency_seconds: 37.815
- baseline_total_tokens: 3770
- orchestrator_total_tokens: 25089
- baseline_citation_count: 3
- orchestrator_evidence_count: 4
- fact_check_status_counts: {'unsupported': 2, 'supported': 4}

## Question 2

Type: easy lookup

Which downstream tasks or benchmarks does the paper use to evaluate REALM?

### Baseline Answer

The paper uses NaturalQuestions-Open to present results after ablating critical components of REALM [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05, chunk_index: 12

### Multi-Agent Answer

The paper evaluates REALM on Open-QA benchmarks [E4]. Specifically, the evidence notes detail performance measurements for three benchmarks: NQ, WQ, and CT [E4].

### Metrics

- baseline_latency_seconds: 3.022
- orchestrator_latency_seconds: 15.855
- baseline_total_tokens: 2299
- orchestrator_total_tokens: 11500
- baseline_citation_count: 3
- orchestrator_evidence_count: 4
- fact_check_status_counts: {'supported': 2}

## Question 3

Type: definition

What is REALM, and what does the paper mean by retrieval-augmented language model pre-training?

### Baseline Answer

REALM (Retrieval-Augmented Language Model) is a novel framework designed to capture knowledge in a more modular and interpretable way than traditional models that store knowledge implicitly in their parameters [1, 2]. Instead of relying solely on internal parameters, REALM augments language model pre-training algorithms with a learned textual knowledge retriever [1]. This allows the model to explicitly decide what knowledge to retrieve and use during inference by retrieving documents from a large corpus, such as Wikipedia, and attending over them to inform its predictions [1].

The paper defines retrieval-augmented language model pre-training as a process that:
*   **Augments pre-training with a retriever:** It incorporates a latent knowledge retriever into the language model pre-training algorithms [1, 2].
*   **Uses a "retrieve-then-predict" process:** For pre-training, the model performs masked language modeling where the input $x$ is a sentence with masked tokens; the model first retrieves potentially helpful documents $z$ from a knowledge corpus $Z$ based on the distribution $p(z|x)$, and then predicts the missing tokens $y$ by conditioning on both the input and the retrieved documents, modeled as $p(y|z, x)$ [3].
*   **Employs unsupervised learning:** The retriever is trained in an unsupervised manner using masked language modeling as the learning signal [2]. A retrieval is rewarded if it improves the language model's perplexity and penalized if it is uninformative [1].
*   **Backpropagates through retrieval:** The framework involves backpropagating through a retrieval step that considers an entire corpus of textual knowledge (potentially millions of documents) [1, 2].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[3] source: data/2002.08909v1.pdf, chunk

### Multi-Agent Answer

REALM (Retrieval-Augmented Language Model) is a framework that augments language model pre-training algorithms with a learned textual knowledge retriever [E4]. Unlike traditional models that store world knowledge implicitly within neural network parameters [E5], REALM is designed to capture knowledge in a more modular and interpretable way [E4, E5]. This approach explicitly exposes the role of world knowledge by requiring the model to decide what knowledge to retrieve and use during the inference process [E4].

Retrieval-augmented language model pre-training refers to a method where a latent knowledge retriever is integrated into the pre-training process [E5]. This integration allows the model to retrieve and attend over documents from a large corpus, such as Wikipedia, during pre-training, fine-tuning, and inference [E5]. The retriever can be trained in an unsupervised manner, using masked language modeling as the learning signal [E5].

### Metrics

- baseline_latency_seconds: 7.417
- orchestrator_latency_seconds: 23.440
- baseline_total_tokens: 3910
- orchestrator_total_tokens: 14940
- baseline_citation_count: 3
- orchestrator_evidence_count: 6
- fact_check_status_counts: {'supported': 7}

## Question 4

Type: definition

How does REALM differ from a standard parametric language model such as BERT in where knowledge is stored and accessed?

### Baseline Answer

In standard parametric language models such as BERT, world knowledge is stored implicitly in the parameters of the underlying neural network [1]. This implicit storage makes it difficult to determine what knowledge is stored and where, and limits storage space to the size of the network, meaning that capturing more knowledge requires training ever-larger networks [1].

In contrast, REALM (Retrieval-Augmented Language Model) differs in the following ways:

*   **Knowledge Storage:** Instead of relying solely on parameters, REALM augments pre-training with a learned textual knowledge retriever that accesses a large textual knowledge corpus, such as Wikipedia [1, 2].
*   **Knowledge Access:** Before making a prediction, the model uses the retriever to retrieve documents from the corpus and then attends over those documents to inform its prediction [2].
*   **Characteristics:** This approach allows for knowledge to be captured in a more modular and interpretable way [1]. Additionally, REALM's memories are "grounded," meaning each memory is associated with a specific document rather than unnamed value vectors [3].

Citations:
[1] data/2002.08909v1.pdf (chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2)
[2] data/2002.08909v1.pdf (chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952)
[3] data/2002.08909v1.pdf (chunk_id: 2002.08909v1-1-15-e73576ceacc6e97a0666fd10)

### Multi-Agent Answer

Unlike models that store knowledge within their parameters, REALM explicitly exposes the role of world knowledge by requiring the model to decide what to retrieve and use during inference [E2]. The framework achieves this by augmenting language model pre-training with a learned textual knowledge retriever [E2].

The REALM process is decomposed into two steps: first, the model retrieves potentially helpful documents from a knowledge corpus, and second, it generates an output conditioned on both the input and the retrieved documents [E3]. This architecture utilizes two key components: a neural knowledge retriever and a knowledge-augmented encoder [E3]. This approach differs from standard Reading Comprehension (RC) models, which may only comprehend a single document; instead, REALM is designed to access knowledge from a large corpus, such as Wikipedia [E2, E3].

### Metrics

- baseline_latency_seconds: 4.993
- orchestrator_latency_seconds: 43.694
- baseline_total_tokens: 3907
- orchestrator_total_tokens: 26825
- baseline_citation_count: 3
- orchestrator_evidence_count: 5
- fact_check_status_counts: {'supported': 4, 'unsupported': 1}

## Question 5

Type: method/mechanism

How does REALM's retrieve-then-predict framework work, including the role of the latent document variable z?

### Baseline Answer

REALM's retrieve-then-predict framework decomposes the probability of an output $y$ given an input $x$, denoted as $p(y | x)$, into two distinct steps:

1.  **Retrieve**: Given an input $x$, the model first retrieves potentially helpful documents $z$ from a knowledge corpus $Z$ [3]. This retrieval is modeled as a sample from the distribution $p(z | x)$ [3].
2.  **Predict**: The model then conditions on both the retrieved document $z$ and the original input $x$ to generate the output $y$, which is modeled as $p(y | z, x)$ [3].

The latent document variable $z$ is treated as a latent variable, and the model calculates the overall likelihood of generating $y$ by marginalizing over all possible documents $z$ in the corpus $Z$, following the formula:
$p(y | x) = \sum_{z \in Z} p(y | z, x) p(z | x)$ [3].

To implement the retrieval component, REALM uses a dense inner product model where the relevance score $f(x, z)$ between the input and a document is defined as the inner product of their respective vector embeddings [3].

Citations:
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7

### Multi-Agent Answer

The REALM framework utilizes a "retrieve-then-predict" method that models the generative process as a latent variable language model [E1]. This approach decomposes the generative process $p(y |x)$ into two steps: the model first retrieves documents $z$ from a knowledge corpus $Z$, and then predicts the output $y$ based on both the input $x$ and the retrieved documents $z$ [E3].

The latent document variable $z$ represents documents retrieved from a large corpus, such as Wikipedia, to help inform the model's prediction [E1, E2]. During this process, the language model attends over these retrieved documents to assist in making its prediction [E1]. To manage the computational challenge of considering millions of candidate documents, the retriever is structured so that computation for each document can be cached and asynchronously updated, using Maximum Inner Product Search (MIPS) for selection [E1].

### Metrics

- baseline_latency_seconds: 4.062
- orchestrator_latency_seconds: 37.220
- baseline_total_tokens: 3372
- orchestrator_total_tokens: 25315
- baseline_citation_count: 3
- orchestrator_evidence_count: 5
- fact_check_status_counts: {'supported': 4, 'unsupported': 1}

## Question 6

Type: method/mechanism

How does the paper train the retriever when the retrieved document is latent, and how does learning signal flow back to retrieval?

### Baseline Answer

The paper trains the retriever by modeling the "retrieve-then-predict" approach as a latent variable language model and optimizing the marginal likelihood [1]. The training uses a performance-based signal from unsupervised text, where retrievals that improve the language model's perplexity are rewarded and uninformative retrievals are penalized [1]. Specifically, during pre-training, masked language modeling is used as the learning signal [2].

To enable the learning signal to flow back to the retrieval module, the model backpropagates through the retrieval step [1, 2]. Because the retriever must consider millions of candidate documents, the paper addresses the computational challenge of backpropagating through these decisions by structuring the retriever so that computation for each document can be cached and asynchronously updated, and by formulating the selection of the best documents as Maximum Inner Product Search (MIPS) [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2

### Multi-Agent Answer

The REALM framework uses a latent knowledge retriever to capture knowledge in a modular and interpretable way [E2]. The retriever is trained in an unsupervised manner using masked language modeling as the learning signal [E2]. This training process utilizes a performance-based signal from unsupervised text, where retrievals that improve the language model's perplexity are rewarded, while uninformative retrievals are penalized [E1]. To enable learning, the signal from the language modeling objective backpropagates through the retrieval step [E2].

### Metrics

- baseline_latency_seconds: 4.217
- orchestrator_latency_seconds: 18.424
- baseline_total_tokens: 2966
- orchestrator_total_tokens: 14218
- baseline_citation_count: 3
- orchestrator_evidence_count: 6
- fact_check_status_counts: {'supported': 4}

## Question 7

Type: method/mechanism / implementation

What approximations or engineering choices does REALM use to make retrieval over a large corpus practical during training and inference?

### Baseline Answer

To address the computational challenge of a retriever having to consider millions of candidate documents for each pre-training step, REALM employs the following engineering choices:

*   **Caching and Asynchronous Updates:** The retriever is structured so that the computation performed for each document can be cached and updated asynchronously [2].
*   **Maximum Inner Product Search (MIPS):** The selection of the best documents is formulated as a Maximum Inner Product Search (MIPS) [2].

Citations:
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952, chunk_index: 1

### Multi-Agent Answer

To make retrieval over a large corpus of millions of documents practical, REALM employs the following engineering choices and approximations:

*   **Efficient Document Selection:** The retriever uses Maximum Inner Product Search (MIPS) for document selection [E1].
*   **Computational Optimization:** The retriever is structured to allow computation to be cached and updated asynchronously [E1].
*   **Reduced Retrieval Volume:** REALM is capable of achieving its best overall performance while retrieving only 5 documents [E2].

### Metrics

- baseline_latency_seconds: 2.739
- orchestrator_latency_seconds: 17.333
- baseline_total_tokens: 2754
- orchestrator_total_tokens: 12797
- baseline_citation_count: 3
- orchestrator_evidence_count: 4
- fact_check_status_counts: {'supported': 3}

## Question 8

Type: comparison

How does REALM compare with ORQA or other open-domain QA baselines, and what evidence supports that comparison?

### Baseline Answer

Compared to ORQA, REALM's improvement is attributed purely to better pre-training methods [1]. This comparison is considered direct because the fine-tuning setup, hyperparameters, and training data are identical between the two systems [1]. Additionally, the retrievers for both REALM pre-training and ORQA are initialized using the Inverse Cloze Task [2].

In comparison to other retrieval-based baselines (such as Asai et al., 2019; Min et al., 2019a;b), REALM achieves the overall best performance while retrieving only 5 documents, whereas those other systems often retrieve between 20 to 80 documents [1].

Regarding generation-based baselines, REALM is compared to concurrent work that fine-tunes T5 for Open-QA, specifically using T5 Base, Large, and an 11-billion parameter model [2].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-10-8ea61faa3a17c1fc8f8725d8

### Multi-Agent Answer

Among the systems compared, the most direct comparison with REALM is ORQA [E1]. The improvement of REALM over ORQA is attributed solely to superior pre-training methods, as the fine-tuning setup, hyperparameters, and training data are identical between the two [E1]. Additionally, the retrievers for both REALM pre-training and ORQA are initialized using the Inverse Cloze Task [E2].

In terms of performance, REALM achieves the best overall performance among the compared systems [E1]. REALM also reaches this performance while retrieving a significantly smaller number of documents—specifically 5 documents [E1]. This contrasts with other retrieval-based systems, which typically retrieve between 20 to 80 documents [E1].

### Metrics

- baseline_latency_seconds: 4.435
- orchestrator_latency_seconds: 18.624
- baseline_total_tokens: 2787
- orchestrator_total_tokens: 11294
- baseline_citation_count: 3
- orchestrator_evidence_count: 4
- fact_check_status_counts: {'supported': 5}

## Question 9

Type: comparison

How does REALM's retrieval-based approach compare with storing knowledge only in model parameters?

### Baseline Answer

In contrast to models that store world knowledge implicitly in their parameters [1, 3], REALM's retrieval-based approach provides the following differences:

*   **Interpretability and Modularity:** REALM captures knowledge in a more interpretable and modular way [1, 3]. Because knowledge is stored in parameters in other models, it is difficult to determine what knowledge is stored and where [3].
*   **Explicit Knowledge Role:** While parameter-based models store knowledge implicitly, REALM explicitly exposes the role of world knowledge by requiring the model to decide what knowledge to retrieve and use during inference [1].
*   **Storage and Scalability:** In models where knowledge is stored in parameters, the storage space is limited by the size of the network, meaning ever-larger networks are required to capture more facts, which can be expensive or prohibitively slow [3]. 
*   **Mechanism:** REALM augments language model pre-training with a learned textual knowledge retriever that allows the model to retrieve and attend over documents from a large corpus (such as Wikipedia) during pre-training, fine-tuning, and inference [1, 3].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2

### Multi-Agent Answer

Unlike models that store knowledge within their parameters, REALM's approach explicitly exposes the role of world knowledge by requiring the model to decide which knowledge to retrieve and use during inference [E2]. This retrieval-augmented framework is designed to capture knowledge in a way that is both modular and interpretable [E2].

Under the REALM paradigm, the process of generating an output is decomposed into two steps: first, the model retrieves potentially helpful documents from a corpus, and second, it generates an output conditioned on both the input and those retrieved documents [E3]. This approach differs from Reading Comprehension models that process a single document, as Open-QA models must be able to retain knowledge from millions of documents [E3].

### Metrics

- baseline_latency_seconds: 5.119
- orchestrator_latency_seconds: 20.149
- baseline_total_tokens: 2952
- orchestrator_total_tokens: 12824
- baseline_citation_count: 3
- orchestrator_evidence_count: 4
- fact_check_status_counts: {'supported': 4}

## Question 10

Type: evidence synthesis / ablation

What ablation or diagnostic evidence shows that retrieval pre-training improves REALM rather than only the reader component?

### Baseline Answer

To isolate the contribution of improving the retriever during pre-training, the researchers report a metric measuring how often the gold answer appears in the top-5 retrievals before any fine-tuning is applied [1]. 

Additionally, the researchers note that the improvement of REALM over ORQA is purely due to better pre-training methods, as the two systems share identical fine-tuning setups, hyperparameters, and training data [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05, chunk_index: 12

### Multi-Agent Answer

The provided evidence does not contain any ablation or diagnostic studies that specifically compare the improvements gained from retrieval pre-training against the improvements gained from the reader component alone [E1, E2].

While the evidence states that REALM's pre-training framework augments language model pre-training with a learned textual knowledge retriever [E1] and that the model outperforms previous state-of-the-art methods for both explicit and implicit knowledge storage on three Open-QA benchmarks [E2], it does not provide the specific experimental data or ablation results required to isolate the retriever's contribution from the reader's contribution [E1, E2].

### Metrics

- baseline_latency_seconds: 2.472
- orchestrator_latency_seconds: 35.739
- baseline_total_tokens: 2743
- orchestrator_total_tokens: 25477
- baseline_citation_count: 3
- orchestrator_evidence_count: 9
- fact_check_status_counts: {'unsupported': 1, 'supported': 1}

## Question 11

Type: evidence synthesis

Synthesize the evidence for why REALM improves open-domain QA performance, including retrieval quality, pre-training, and downstream fine-tuning.

### Baseline Answer

Evidence for REALM's improved open-domain QA performance can be synthesized as follows:

*   **Pre-training:** The improvement of REALM over ORQA is attributed purely to better pre-training methods [1]. REALM extends the retrieval-based paradigm to language model pre-training [2]. During pre-training, the task is masked language modeling, where the model must predict missing tokens from a pre-training corpus [2]. This pre-training method can be applied in both a single-corpus setting (where the pre-training corpus and knowledge corpus are both Wikipedia) or a separate-corpus setting (where the pre-training corpus is CC-News and the knowledge corpus is Wikipedia) [1].
*   **Retrieval Quality:** REALM achieves its overall best performance while only retrieving 5 documents, whereas other retrieval-based systems often retrieve between 20 to 80 documents [1]. The contribution of improving the retriever during pre-training can be isolated by measuring how often the gold answer appears in the top-5 retrievals before any fine-tuning is applied [1].
*   **Downstream Fine-tuning:** For fine-tuning, the task is transitioned to Open-QA, where the input is a question and the output is an answer [2]. REALM decomposes the generation of the answer into two steps: first, retrieving potentially helpful documents from a knowledge corpus, and second, conditioning on both the retrieved documents and the original input to generate the output [2].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7

### Multi-Agent Answer

REALM improves open-domain QA performance through a framework that augments language model pre-training with a learned textual knowledge retriever [E2].

**Retrieval Quality**
The REALM retriever is trained using a performance-based signal derived from unsupervised text [E2]. Specifically, the system rewards retrievals that improve the language model's perplexity and penalizes uninformative retrievals [E2]. The retriever utilizes a dense inner product model where relevance is defined as the inner product of $d$-dimensional vector embeddings [E3]. This approach allows REALM to achieve superior performance despite retrieving only 5 documents, whereas other retrieval-based systems typically retrieve between 20 and 80 documents [E1]. Additionally, the retriever is designed to transfer to other tasks because it retrieves raw text rather than labeled examples [E2].

**Pre-training**
During pre-training, REALM decomposes the likelihood of generating an output by treating the retrieved document as a latent variable and marginalizing over all possible documents in the corpus [E3]. The pre-training task itself is formulated as masked language modeling [E3]. The improvement of REALM over comparable systems, such as ORQA, is attributed purely to these better pre-training methods, as fine-tuning setups, hyperparameters, and training data remain identical [E1]. Furthermore, this pre-training method is applicable to both single-corpus settings and separate-corpus settings [E1].

**Downstream Fine-tuning**
In the fine-tuning stage, the task transitions from masked language modeling to Open-QA [E3]. During inference, the model explicitly decides what knowledge to retrieve and use, rather than storing all knowledge within its parameters [E2].

### Metrics

- baseline_latency_seconds: 5.377
- orchestrator_latency_seconds: 24.394
- baseline_total_tokens: 2824
- orchestrator_total_tokens: 13546
- baseline_citation_count: 3
- orchestrator_evidence_count: 5
- fact_check_status_counts: {'supported': 12}

## Question 12

Type: multi-step reasoning

Explain step by step how a masked-language-model pre-training objective can improve downstream open-domain QA in REALM.

### Baseline Answer

In REALM, the masked-language-model (MLM) pre-training objective improves downstream open-domain question answering (Open-QA) through the following process:

1.  **MLM Pre-training Task**: During pre-training, the model is given an input $x$, which is a sentence from an unlabeled pre-training corpus $X$ with certain tokens masked out [1]. The goal is to predict the values of these missing tokens, $y$ [3]. 
2.  **Learning Representations and Knowledge**: To successfully predict masked tokens, a good MLM must learn to encode syntactic and semantic information, as well as world knowledge [1]. While traditional language models store this knowledge implicitly in their parameters, REALM augments the pre-training process with a latent knowledge retriever [2].
3.  **The Retrieve-then-Predict Process**: REALM decomposes the generative process into two steps:
    *   **Retrieve**: Given the input $x$, the model first retrieves potentially helpful documents $z$ from a large knowledge corpus $Z$ [3].
    *   **Predict**: The model then conditions on both the original input $x$ and the retrieved documents $z$ to generate the output $y$ [3].
4.  **Unsupervised Retriever Training**: The knowledge retriever is trained in an unsupervised manner using the MLM objective as a learning signal [2]. Specifically, the signal from the language modeling objective is backpropagated through the retrieval step, which considers millions of documents [2].
5.  **Downstream Open-QA Application**: The model is then fine-tuned for the Open-QA task, where the input $x$ is a question and the output $y$ is the correct answer string [3]. Because the model was pre-trained to retrieve and attend over documents to solve the MLM task, it can better incorporate the world knowledge necessary for Open-QA [2].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-2-7f240c64641ad3f52fc62e97
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7

### Multi-Agent Answer

In REALM, a masked-language-model (MLM) pre-training objective improves downstream open-domain question answering (Open-QA) through the following process:

1.  **Unsupervised Pre-training via MLM**: The model undergoes unsupervised pre-training using a masked language modeling objective [E2]. In this task, the model is trained to predict missing tokens ($y$) from an input text passage ($x$) that contains masked tokens [E1, E3].
2.  **Encoding Diverse Information**: This MLM pre-training process requires the model to encode syntactic information, semantic information, and world knowledge [E1]. 
3.  **Augmenting Knowledge Capture**: While traditional language model pre-training captures world knowledge implicitly within the parameters of a neural network [E2], the REALM framework augments this by using a latent knowledge retriever to capture knowledge in a more modular and interpretable way [E2].
4.  **Training the Retriever**: REALM uses the MLM task as a learning signal to enable the unsupervised pre-training of its knowledge retriever [E2]. The signal from the language modeling objective backpropagates through the retrieval step [E2]. During this stage, the retriever can access and attend over documents from a large corpus, such as Wikipedia [E2].
5.  **Downstream Generalization**: By learning useful representations of language from unlabeled text corpora during pre-training, the model can be fine-tuned for downstream tasks like Open-QA, which often leads to better generalization than training from scratch [E1].

### Metrics

- baseline_latency_seconds: 5.928
- orchestrator_latency_seconds: 42.543
- baseline_total_tokens: 3580
- orchestrator_total_tokens: 24417
- baseline_citation_count: 3
- orchestrator_evidence_count: 9
- fact_check_status_counts: {'unsupported': 5, 'supported': 7}

## Question 13

Type: multi-step reasoning / error analysis

If REALM retrieves an irrelevant document, how would that affect p(z|x), p(y|z,x), and the final answer prediction?

### Baseline Answer

If REALM retrieves an irrelevant document $z$, the effects are as follows:

*   **$p(z|x)$**: The document $z$ is modeled as a sample from the distribution $p(z|x)$, which is the retrieval distribution [3].
*   **$p(y|z,x)$**: A negative Retrieval Utility (RU) indicates that $z$ is less useful for predicting $y$ than a null document [1]. This negative RU could specifically mean that the document $z$ is irrelevant to $x$ [1].
*   **Final answer prediction**: The final prediction $p(y|x)$ is obtained by treating $z$ as a latent variable and marginalizing over all possible documents $z$, calculated as $p(y|x) = \sum_{z \in Z} p(y|z, x)p(z|x)$ [3].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-20-58cd33db77feaae8a3f8d036, chunk_index: 20
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7, chunk_index: 3

### Multi-Agent Answer

The provided evidence does not explicitly state how an irrelevant document specifically affects the individual probability values of $p(z|x)$ and $p(y|z,x)$, but it provides information regarding the Retrieval Utility (RU) and the model's generative process [E1, E2].

**$p(z|x)$**
The retriever models $p(z|x)$ using a "neural knowledge retriever" [E2]. This is implemented as a dense inner product model where the relevance score $f(x, z)$ is the inner product of the vector embeddings [E2]. While the notes explain this mechanism, they do not explicitly describe the specific numerical impact or change in probability for $p(z|x)$ when a document is irrelevant [E2].

**$p(y|z,x)$ and the final answer prediction**
REALM predicts the output $y$ by conditioning on both the input $x$ and the retrieved documents $z$, modeling $p(y|z,x)$ via a "knowledge-augmented encoder" [E2]. If a retrieved document $z$ is irrelevant to $x$, it may result in a negative Retrieval Utility (RU) [E1]. RU is defined as $\text{RU} = \log p(y |z, x) - \log p(y | \emptyset, x)$ [E1]. A negative RU indicates that the retrieved document $z$ is less useful for predicting $y$ than a null document [E1]. This lack of utility can occur because $z$ is irrelevant to $x$, or because the required world knowledge is already contained within the model's parameters [E1].

### Metrics

- baseline_latency_seconds: 4.367
- orchestrator_latency_seconds: 40.686
- baseline_total_tokens: 3458
- orchestrator_total_tokens: 22527
- baseline_citation_count: 3
- orchestrator_evidence_count: 7
- fact_check_status_counts: {'unsupported': 1, 'supported': 7}

## Question 14

Type: limitation/uncertainty

What limitations, uncertainties, or missing comparisons should be noted when interpreting REALM's reported results?

### Baseline Answer

When interpreting REALM's reported results, the following limitations, uncertainties, and missing comparisons should be noted:

*   **Missing Data:** Certain data could benefit REALM, but such data was not used in the experiments [1].
*   **Uncertainty in Retrieval Utility (RU):** A negative RU indicates that the retrieved document $z$ is less useful for predicting $y$ than a null document [2]. However, this could mean several things: $z$ is irrelevant to $x$, the masked tokens in $x$ do not require world knowledge to predict, or the required world knowledge is common enough that it has already been incorporated into the model's parameters [2].
*   **Impact of Masking and Training:** The Retrieval Utility (RU) is impacted by the number of pre-training steps and the specific choice of masking used [2].
*   **Comparisons:** The most direct comparison provided is with ORQA, which shares identical fine-tuning setups, hyperparameters, and training data [1]. While REALM is compared to other retrieval-based systems, those systems often retrieve 20 to 80 documents, whereas REALM achieves its performance while only retrieving 5 documents [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-20-58cd33db77feaae8a3f8d036

### Multi-Agent Answer

When interpreting REALM's reported results, the following limitations, uncertainties, and sensitivities should be noted:

*   **Data Limitations:** There is certain data that could have potentially benefited REALM, but it was not utilized in the experiments [E1].
*   **Uncertainties in Retrieval Utility (RU):** A negative RU indicates that a retrieved document ($z$) is less useful for predicting the target ($y$) than a null document [E3]. This negative value is uncertain because it could stem from several different factors: the document may be irrelevant to the input ($x$), the masked tokens may not require world knowledge, or the necessary world knowledge may already be embedded within the model's parameters [E3].
*   **Optimization Sensitivity:** The model's training can be negatively impacted by a stale MIPS index, meaning frequent index refreshes are necessary for proper optimization [E2].

### Metrics

- baseline_latency_seconds: 4.584
- orchestrator_latency_seconds: 20.888
- baseline_total_tokens: 2088
- orchestrator_total_tokens: 11903
- baseline_citation_count: 3
- orchestrator_evidence_count: 3
- fact_check_status_counts: {'supported': 4}

## Question 15

Type: citation grounding / uncertainty

Which claims about REALM's performance or mechanism cannot be verified unless the answer cites specific experimental evidence from the paper?

### Baseline Answer

Based on the provided text, the following claims regarding REALM's performance or mechanism require specific experimental evidence (such as results from tables or figures) to be verified:

*   **Performance relative to ORQA:** The claim that the improvement of REALM over ORQA is "purely due to better pre-training methods" [1].
*   **Performance relative to other retrieval-based systems:** The claim that REALM "gets the overall best performance while only retrieving 5 documents" compared to other retrieval-based systems that often retrieve between 20 to 80 documents [1].
*   **Effectiveness of pre-training on different settings:** The claim that the pre-training method can be applied to both the "single-corpus setting" and the "separate-corpus setting" [1].
*   **Retrieval Utility (RU) trends:** The claim that RU "increases steadily over the course of pre-training" and is "more predictive of good performance on the downstream task of Open-QA than even the overall log-likelihood" [3].
*   **Adaptation to updated knowledge:** The claim (illustrated in Table 4) that a REALM model pre-trained on an outdated corpus (2018) is able to retrieve documents and generate correct tokens when used with an updated corpus (2020) [3].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-20-58cd33db77feaae8a3f8d036

### Multi-Agent Answer

Based on the provided evidence, the following claims regarding REALM's mechanism and performance are supported:

*   **Performance Comparison:** The improvement of REALM over ORQA is attributed purely to better pre-training methods [E1].
*   **System Superiority:** REALM achieves the overall best performance compared to other retrieval-based systems while retrieving fewer documents [E1].
*   **Retrieval Efficiency:** REALM retrieves 5 documents, whereas other retrieval-based systems typically retrieve between 20 and 80 documents [E1].
*   **Generalization Capability:** REALM is a generalization of previous language modeling work that conditions on the entire text corpus [E4].
*   **Information Dependency:** Unlike models that rely on high lexical overlap, REALM learns which texts are most useful for reducing perplexity, allowing it to depend on information beyond lexical overlap [E4].

### Metrics

- baseline_latency_seconds: 5.268
- orchestrator_latency_seconds: 17.286
- baseline_total_tokens: 2782
- orchestrator_total_tokens: 11332
- baseline_citation_count: 3
- orchestrator_evidence_count: 6
- fact_check_status_counts: {'supported': 5}
