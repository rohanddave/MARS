# experiment04: model ablation, strong summarizer only, top_k=5

## Agent Configuration

- family: model_ablation
- control_variable: summarization_model
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

REALM retrieves from a large textual knowledge corpus $Z$, such as Wikipedia [1, 2].

The model uses this knowledge through a "retrieve-then-predict" generative process [3]. Specifically:
*   **Retrieval:** Given an input $x$, the model first uses a learned textual knowledge retriever to retrieve potentially helpful documents $z$ from the knowledge corpus $Z$ [1, 3]. This retrieval is modeled as a sample from the distribution $p(z |x)$ [3].
*   **Prediction:** The model then conditions on both the retrieved documents $z$ and the original input $x$ to generate the output $y$, modeled as $p(y |z, x)$ [3]. The language model attends over the retrieved documents to help inform its prediction [1].

This framework is used during pre-training, fine-tuning, and inference [2].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7

### Multi-Agent Answer

REALM retrieves documents from a large knowledge corpus, such as Wikipedia [E2, E3]. The model can operate in a single-corpus setting where both the input and the knowledge source are Wikipedia, or in a separate-corpus setting where the knowledge source is Wikipedia but the input comes from a different source, such as CC-News [E5].

The model decomposes the process of learning a distribution $p(y |x)$ into two distinct steps: retrieve, then predict [E1]. Specifically, the generative process involves retrieving potentially helpful documents $z$ from a knowledge corpus $Z$ (modeled as $p(z |x)$) and then conditioning on both the retrieved $z$ and the input $x$ to generate an output $y$ (modeled as $p(y |z, x)$) [E1].

To perform this, the model uses a learned textual knowledge retriever [E2]. The retriever utilizes a dense inner product model where the relevance score $f(x, z)$ is the inner product of $d$-dimensional vector embeddings [E1].

### Metrics

- baseline_latency_seconds: 6.543
- orchestrator_latency_seconds: 55.596
- baseline_total_tokens: 5461
- orchestrator_total_tokens: 35408
- baseline_citation_count: 5
- orchestrator_evidence_count: 6
- fact_check_status_counts: {'unsupported': 2, 'supported': 5}

## Question 2

Type: easy lookup

Which downstream tasks or benchmarks does the paper use to evaluate REALM?

### Baseline Answer

The paper uses the NaturalQuestions-Open benchmark to present results after ablating critical components of REALM [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05, chunk_index: 12

### Multi-Agent Answer

REALM is evaluated using three Open-domain Question Answering (Open-QA) benchmarks [E4]. The paper reports state-of-the-art results on these specific benchmarks: Natural Questions-Open (NQ), Web Questions (WQ), and Curated TREC (CT) [E4].

The exact match scores achieved by REALM on these benchmarks are as follows:
* **Natural Questions-Open (NQ):** REALM achieved scores of 39.2 using Wikipedia and 40.4 using CC-News [E5].
* **Web Questions (WQ):** REALM achieved scores of 40.2 using Wikipedia and 40.7 using CC-News [E5].
* **Curated TREC (CT):** REALM achieved scores of 46.8 using Wikipedia and 42.9 using CC-News [E5].

### Metrics

- baseline_latency_seconds: 3.362
- orchestrator_latency_seconds: 56.690
- baseline_total_tokens: 4204
- orchestrator_total_tokens: 36733
- baseline_citation_count: 5
- orchestrator_evidence_count: 10
- fact_check_status_counts: {'supported': 5}

## Question 3

Type: definition

What is REALM, and what does the paper mean by retrieval-augmented language model pre-training?

### Baseline Answer

REALM stands for Retrieval-Augmented Language Model pre-training [1]. It is a novel framework designed to capture knowledge in a more modular and interpretable way by augmenting language model pre-training algorithms with a learned textual knowledge retriever [1, 2]. Unlike traditional models that store knowledge implicitly within their parameters, REALM explicitly exposes the role of world knowledge by requiring the model to decide what knowledge to retrieve and use during inference [1, 2].

The paper defines "retrieval-augmented language model pre-training" as a process that includes the following characteristics:
*   **Mechanism:** The framework augments pre-training with a latent knowledge retriever that retrieves documents from a large corpus (such as Wikipedia) and then attends over those documents to inform its predictions [1, 2]. 
*   **Generative Process:** The process is modeled as a "retrieve-then-predict" generative process [3]. For pre-training, the specific task is masked language modeling, where the model must predict missing tokens ($y$) from a sentence ($x$) by first retrieving helpful documents ($z$) from a knowledge corpus ($Z$) [3].
*   **Learning Signal:** The retriever is trained in an unsupervised manner using a performance-based signal from text; specifically, a retrieval that improves the language model's perplexity is rewarded, while uninformative retrieval is penalized [1]. This is achieved by modeling the approach as a latent variable language model and optimizing the marginal likelihood [1].
*   **Scale:** The pre-training involves backpropagating through a retrieval step that must consider millions of candidate documents for each step [1, 2].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.0

### Multi-Agent Answer

REALM (Retrieval-Augmented Language Model) is a framework that augments language model pre-training with a latent knowledge retriever [E1]. This approach is designed to capture knowledge in a more modular and interpretable way than traditional language model pre-training, which stores world knowledge implicitly in the parameters of a neural network [E1].

The term "retrieval-augmented language model pre-training" refers to extending the retrieval-based approach to the pre-training stage of language models [E5]. This process decomposes the probability of an output $p(y|x)$ into a "retrieve, then predict" process [E5]. This involves two components: a neural knowledge retriever and a knowledge-augmented encoder [E5]. Specifically, the model treats the retrieved document $z$ as a latent variable to model the likelihood of generating an output $y$ given an input $x$ [E5].

During pre-training, REALM utilizes masked language modeling as the learning signal to perform unsupervised pre-training of the knowledge retriever [E1]. The retriever allows the model to retrieve and attend over documents from a large corpus, such as Wikipedia, during pre-training, fine-tuning, and inference [E1].

### Metrics

- baseline_latency_seconds: 7.935
- orchestrator_latency_seconds: 62.596
- baseline_total_tokens: 5743
- orchestrator_total_tokens: 39060
- baseline_citation_count: 5
- orchestrator_evidence_count: 11
- fact_check_status_counts: {'supported': 7}

## Question 4

Type: definition

How does REALM differ from a standard parametric language model such as BERT in where knowledge is stored and accessed?

### Baseline Answer

Standard parametric language models, such as BERT, store learned world knowledge implicitly within the parameters of the underlying neural network [1]. This implicit storage makes it difficult to determine what knowledge is stored in the network or where it is located, and it limits storage space to the size of the network, necessitating larger networks to capture more facts [1].

In contrast, REALM (Retrieval-Augmented Language Model) differs in the following ways:

*   **Storage:** Instead of relying solely on parameters, REALM uses a learned textual knowledge retriever to access a large textual knowledge corpus, such as Wikipedia [1, 2]. 
*   **Access:** Before making a prediction, the model uses the retriever to retrieve documents from the corpus and then attends over those documents to inform its prediction [2].
*   **Nature of Knowledge:** REALM's approach captures knowledge in a more modular and interpretable way [1]. Its memories are "grounded," meaning each memory is associated with a specific document rather than unnamed value vectors [3].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-15-e73576ceacc6e97a0666fd10

### Multi-Agent Answer

REALM differs from standard parametric language models, such as BERT, in the following ways regarding how knowledge is stored and accessed:

**Knowledge Storage**
While standard models store knowledge within their parameters [E1], REALM's memories are "grounded," meaning each memory is associated with a specific document rather than being stored as unnamed value vectors [E6].

**Knowledge Access**
Unlike models that rely on stored parameters, REALM explicitly exposes the role of world knowledge by requiring the model to decide what to retrieve and use during inference [E1]. Before making each prediction, the language model uses a learned textual knowledge retriever to retrieve documents from a large corpus, such as Wikipedia, and then attends over those documents to inform its prediction [E1].

This retrieval-based approach allows REALM to assign higher probabilities to correct terms compared to BERT [E8]. For example, in a case involving the term "Fermat," BERT assigned a probability of $1.1 \times 10^{-14}$ without retrieval, whereas REALM achieved a marginal probability of $0.129$ by marginalizing over the top 8 retrieved documents [E8].

### Metrics

- baseline_latency_seconds: 6.246
- orchestrator_latency_seconds: 35.289
- baseline_total_tokens: 6552
- orchestrator_total_tokens: 21133
- baseline_citation_count: 5
- orchestrator_evidence_count: 14
- fact_check_status_counts: {'supported': 5}

## Question 5

Type: method/mechanism

How does REALM's retrieve-then-predict framework work, including the role of the latent document variable z?

### Baseline Answer

REALM's retrieve-then-predict framework decomposes the probability of an output $y$ given an input $x$, denoted as $p(y|x)$, into two sequential steps:

1.  **Retrieve:** The model first retrieves potentially helpful documents $z$ from a knowledge corpus $Z$ [3]. This step is modeled as a sample from the distribution $p(z|x)$ [3].
2.  **Predict:** The model then conditions on both the original input $x$ and the retrieved document $z$ to generate the output $y$, modeled as $p(y|z, x)$ [3].

The latent document variable $z$ is used to obtain the overall likelihood of generating $y$ by treating it as a latent variable and marginalizing over all possible documents in the corpus $Z$ [3]. This is expressed mathematically as:
$p(y|x) = \sum_{z \in Z} p(y|z, x)p(z|x)$ [3].

In practice, the framework uses a neural knowledge retriever to model $p(z|x)$ and a knowledge-augmented encoder to model $p(y|z, x)$ [3].

Citations:
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7, chunk_index: 3

### Multi-Agent Answer

REALM (Retrieval-Augmented Language Model) is a framework that augments language model pre-training with a learned textual knowledge retriever [E1, E2]. The framework decomposes the process of generating an output $y$ given an input $x$ into two steps: first, it retrieves potentially helpful documents $z$ from a knowledge corpus $Z$ (modeled as $p(z | x)$), and second, it conditions on both the original input $x$ and the retrieved document $z$ to generate the output $y$ (modeled as $p(y | z, x)$) [E3].

In this approach, $z$ is treated as a latent variable [E3]. The overall likelihood of generating the output $y$ is obtained by treating $z$ as a latent variable and marginalizing over all possible documents $z$ in the corpus $Z$, expressed as $p(y | x) = \sum_{z \in Z} p(y | z, x) p(z | x)$ [E3].

During inference, the language model uses the retriever to retrieve documents from a large corpus, such as Wikipedia, and then attends over those documents to help inform its prediction [E1, E2]. The retriever is trained using a performance-based signal from unsupervised text, which rewards retrievals that improve the language model's perplexity and penalizes uninformative retrievals [E1].

### Metrics

- baseline_latency_seconds: 5.288
- orchestrator_latency_seconds: 60.457
- baseline_total_tokens: 5464
- orchestrator_total_tokens: 36390
- baseline_citation_count: 5
- orchestrator_evidence_count: 8
- fact_check_status_counts: {'unsupported': 2, 'supported': 4}

## Question 6

Type: method/mechanism

How does the paper train the retriever when the retrieved document is latent, and how does learning signal flow back to retrieval?

### Baseline Answer

The paper trains the retriever by modeling the "retrieve-then-predict" approach as a latent variable language model and optimizing the marginal likelihood [1]. To obtain the overall likelihood of generating an output $y$ from an input $x$, the model treats the retrieved document $z$ as a latent variable and marginalizes over all possible documents $z$ in the corpus $Z$, using the formula $p(y |x) = \sum_{z \in Z} p(y |z, x) p(z |x)$ [4].

The learning signal flows back to the retrieval module through backpropagation from the language modeling objective [2]. Specifically, the retriever is trained using a performance-based signal from unsupervised text: a retrieval that improves the language model’s perplexity is rewarded, while an uninformative retrieval is penalized [1]. During pre-training, the model uses masked language modeling as the learning signal [2].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952, chunk_index: 1
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2, chunk_index: 0
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7, chunk_index: 3

### Multi-Agent Answer

The REALM framework models the "retrieve-then-predict" approach as a latent variable language model, which is optimized by maximizing marginal likelihood [E1]. The retriever is trained using a performance-based signal derived from unsupervised text [E1]. Specifically, the model rewards retrievals that improve the language model's perplexity and penalizes uninformative retrievals [E1]. This training can be implemented in an unsupervised manner by using masked language modeling as the learning signal [E2].

To learn the model end-to-end, the system backpropagates through a retrieval step that considers an entire corpus of textual knowledge [E1]. This retrieval step can consider millions of documents [E2]. One challenge in this process is the "cold-start problem," where poor initial embeddings for the input and document can lead the encoder to ignore retrieved documents, resulting in a lack of meaningful gradient to improve the retriever [E4].

### Metrics

- baseline_latency_seconds: 5.422
- orchestrator_latency_seconds: 29.581
- baseline_total_tokens: 5397
- orchestrator_total_tokens: 20981
- baseline_citation_count: 5
- orchestrator_evidence_count: 10
- fact_check_status_counts: {'supported': 8}

## Question 7

Type: method/mechanism / implementation

What approximations or engineering choices does REALM use to make retrieval over a large corpus practical during training and inference?

### Baseline Answer

To make retrieval over a large corpus practical during training and inference, REALM uses the following engineering choices and approximations:

*   **Retriever Structure and MIPS:** The retriever is structured so that computations for each document can be cached and updated asynchronously [2]. Additionally, the selection of the best documents is formulated as a Maximum Inner Product Search (MIPS) [2].
*   **Parallelization and Indexing:** During pre-training, the document embedding step for the MIPS index is parallelized over 16 TPUs [4]. To maintain the index, a parallel process runs to re-embed corpus documents and rebuild the MIPS index, resulting in an index refresh approximately every 500 training steps [5].
*   **Candidate Selection (Marginalization and Top-K):** 
    *   **During Pre-training:** For each example, the model retrieves and marginalizes over 8 candidate documents, which includes a null document $\emptyset$ [4].
    *   **During Fine-tuning Inference:** The system considers only the top-5 candidate documents [1, 4].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05, chunk_index: 12
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952, chunk_index: 1
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-11-3fa55fc3148d1188cb70ab91, chunk_index: 11
[5] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e3

### Multi-Agent Answer

To make retrieval over a large corpus practical, REALM employs several engineering choices and approximations:

*   **Maximum Inner Product Search (MIPS):** To handle the computational challenge of evaluating millions of candidate documents, the retriever formulates document selection as a Maximum Inner Product Search [E1].
*   **Caching and Asynchronous Updates:** The retriever is structured such that the computation for each document can be cached and updated asynchronously [E1].
*   **Dense Vector Embeddings:** The knowledge retriever uses a dense inner product model, where relevance is defined by the inner product of $d$-dimensional vector embeddings [E6].
*   **Inference Constraints:** During fine-tuning inference, the model limits its consideration to the top-5 candidate documents [E3].
*   **Parallelization:** The document embedding step is parallelized over 16 TPUs to improve efficiency [E3].

### Metrics

- baseline_latency_seconds: 6.869
- orchestrator_latency_seconds: 30.732
- baseline_total_tokens: 5668
- orchestrator_total_tokens: 21090
- baseline_citation_count: 5
- orchestrator_evidence_count: 6
- fact_check_status_counts: {'supported': 5}

## Question 8

Type: comparison

How does REALM compare with ORQA or other open-domain QA baselines, and what evidence supports that comparison?

### Baseline Answer

REALM compares to ORQA and other open-domain QA baselines in the following ways:

*   **Comparison with ORQA:** ORQA is considered the most direct comparison to REALM because the fine-tuning setup, hyperparameters, and training data are identical [1]. The improvement demonstrated by REALM over ORQA is attributed entirely to superior pre-training methods [1]. Furthermore, resetting both the retriever and encoder parameters to their baseline state reduces the REALM system to its main baseline, ORQA [5]. Both REALM and ORQA initialize their retrievers using the Inverse Cloze Task [2].
*   **Comparison with Retrieval-based Systems:** Compared to other retrieval-based systems (such as Asai et al., 2019; Min et al., 2019a;b), which typically retrieve between 20 to 80 documents, REALM achieves the overall best performance while only retrieving 5 documents [1].
*   **Comparison with Generation-based Systems:** REALM compares against state-of-the-art systems from the generation-based paradigm [4]. Specifically, it is compared against concurrent work that fine-tunes T5 for Open-QA, utilizing Base, Large, and 11-billion parameter models to measure the effects of model size [2].
*   **Comparison with BERT:** In terms of masked language model prediction, REALM assigns a much higher probability to correct terms than BERT does [5]. For example, when predicting the word "Fermat," BERT assigned a probability of $1.1 \times 10^{-14}$ (without retrieval), whereas REALM's marginalized probability was $0.129$ [5].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-10-8ea61faa3a17c1fc8f8725d8
[4] source: data/2002.08909v1.pdf, chunk_

### Multi-Agent Answer

ORQA is considered the most direct comparison to REALM because the fine-tuning setup, hyperparameters, and training data are identical [E1]. Additionally, the retrievers for both REALM pretraining and ORQA are initialized using the Inverse Cloze Task [E2]. The improvement of REALM over ORQA is attributed purely to better pre-training methods [E1].

Compared to other retrieval-based systems, REALM achieves the overall best performance despite retrieving fewer documents [E1]. Specifically, REALM achieves its best performance by retrieving only 5 documents, whereas other retrieval-based systems typically retrieve between 20 and 80 documents [E1].

The study also references the following baselines:
* **T5:** A fine-tuned T5 model is used as a generation-based baseline to measure the effects of model size [E2].
* **GPT-2:** While GPT-2 hinted at the possibility of generating answers without context, its performance was not competitive, which may be due to a lack of fine-tuning [E2].

### Metrics

- baseline_latency_seconds: 7.127
- orchestrator_latency_seconds: 31.702
- baseline_total_tokens: 5305
- orchestrator_total_tokens: 18629
- baseline_citation_count: 5
- orchestrator_evidence_count: 7
- fact_check_status_counts: {'supported': 9}

## Question 9

Type: comparison

How does REALM's retrieval-based approach compare with storing knowledge only in model parameters?

### Baseline Answer

REALM's retrieval-based approach differs from models that store knowledge only in their parameters in several ways:

*   **Interpretability and Modularity:** Unlike models that store knowledge implicitly in parameters, making it difficult to determine what knowledge is stored and where, REALM's approach captures knowledge in a more interpretable and modular way [1, 3]. Specifically, its memories are "grounded," meaning each memory is associated with a specific document rather than unnamed value vectors, which provides provenance for predicted answers [5].
*   **Explicit Role of Knowledge:** This approach explicitly exposes the role of world knowledge by requiring the model to decide what knowledge to retrieve and use during inference [1].
*   **Storage Capacity:** In models where knowledge is stored implicitly in parameters, the storage space is limited by the size of the network; capturing more knowledge requires training ever-larger networks, which can be expensive or prohibitively slow [3].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[5] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-15-e73576ceacc6e97a0666fd10

### Multi-Agent Answer

In contrast to models that store world knowledge implicitly within neural network parameters, REALM's retrieval-based approach explicitly exposes the role of world knowledge [E2]. While implicit storage in parameters requires ever-larger networks to cover more facts, REALM augments pre-training with a latent textual knowledge retriever to capture knowledge in a more modular and interpretable way [E6].

### Interpretability and Modularity
REALM provides qualitative benefits such as interpretability and modularity [E2]. Because its memories are "grounded"—meaning each memory is associated with a specific document rather than unnamed value vectors—it provides a level of interpretability that allows users to find provenance for predicted answers [E4].

### Knowledge Capture
Standard language model pre-training captures knowledge implicitly in parameters [E6]. REALM, however, uses a "retrieve, then predict" approach where the model decides what knowledge to retrieve and use during inference [E2][E3].

### Metrics

- baseline_latency_seconds: 5.472
- orchestrator_latency_seconds: 28.991
- baseline_total_tokens: 5463
- orchestrator_total_tokens: 20054
- baseline_citation_count: 5
- orchestrator_evidence_count: 8
- fact_check_status_counts: {'supported': 8}

## Question 10

Type: evidence synthesis / ablation

What ablation or diagnostic evidence shows that retrieval pre-training improves REALM rather than only the reader component?

### Baseline Answer

To determine whether REALM pre-training improves the retriever, the encoder, or both, the researchers performed an ablation where they reset the parameters of either the retriever or the encoder to their baseline state before fine-tuning [4].

The diagnostic and ablation evidence includes:
* **Encoder and Retriever separately:** The researchers found that both the encoder and the retriever benefit from REALM training when they are improved separately [4].
* **Combined improvement:** The best results are achieved when both components act in unison [4].
* **Baseline comparison:** Resetting both the retriever and the encoder reduces the system to the main baseline, ORQA [4].
* **Isolating retriever contribution:** To more significantly isolate the contribution of improving the retriever during pre-training, the researchers reported how often the gold answer appears in the top-5 retrievals before any fine-tuning is applied [1, 4].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05, chunk_index: 12
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e, chunk_index: 13

### Multi-Agent Answer

To isolate the contribution of improving the retriever during pre-training, the authors report how frequently the gold answer appears in the top-5 retrievals before any fine-tuning is applied [E7]. Regarding the individual components of the model, both the encoder and the retriever benefit separately from REALM training, though optimal results require both components to act in unison [E7]. Furthermore, the improvement of REALM over ORQA is attributed purely to better pre-training methods [E6].

### Metrics

- baseline_latency_seconds: 5.094
- orchestrator_latency_seconds: 31.625
- baseline_total_tokens: 4584
- orchestrator_total_tokens: 22113
- baseline_citation_count: 5
- orchestrator_evidence_count: 9
- fact_check_status_counts: {'supported': 3}

## Question 11

Type: evidence synthesis

Synthesize the evidence for why REALM improves open-domain QA performance, including retrieval quality, pre-training, and downstream fine-tuning.

### Baseline Answer

REALM improves open-domain question answering (Open-QA) performance through the following mechanisms:

*   **Pre-training:** REALM augments language model pre-training with a learned textual knowledge retriever [4]. It uses a masked language modeling task as an unsupervised learning signal, where the model must predict missing tokens [2, 4]. The retriever is trained using a performance-based signal: retrieval that improves the language model's perplexity is rewarded, while uninformative retrieval is penalized [5]. This allows the retriever to be trained in an unsupervised manner by backpropagating through the retrieval step across millions of documents [4]. This pre-training method can be applied to both single-corpus and separate-corpus settings [1].
*   **Retrieval Quality:** Unlike previous retrieval-based systems that often retrieve between 20 to 80 documents, REALM achieves the overall best performance while only retrieving 5 documents [1]. The improvement of REALM over similar systems like ORQA is attributed purely to its superior pre-training methods [1]. Additionally, the retriever is designed to transfer to other tasks because it retrieves raw text rather than labeled examples [5].
*   **Downstream Fine-tuning:** REALM's architecture decomposes the prediction process into a "retrieve-then-predict" generative process [2]. During fine-tuning for Open-QA, the model takes a question as input and retrieves potentially helpful documents from a knowledge corpus to help inform the prediction of the answer [2, 5]. By fine-tuning on Open-QA benchmarks, REALM has outperformed previous state-of-the-art methods by a margin of 4-16% in absolute accuracy [4, 5].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7
[4] source: data/2002.08909v1.pdf, chunk_

### Multi-Agent Answer

REALM improves open-domain question answering (Open-QA) performance through its unique pre-training approach, which integrates a learned textual knowledge retriever [E5]. The improvement of REALM over the ORQA system is attributed purely to its better pre-training methods, as the fine-tuning setups, hyperparameters, and training data are identical [E1].

**Pre-training**
REALM augments language model pre-training with a learned textual knowledge retriever [E5]. This framework enables the unsupervised pre-training of a knowledge retriever by using masked language modeling (MLM) as the learning signal [E4]. Through this MLM pre-training, the model aims to learn useful representations from unlabeled text corpora, specifically learning to encode syntactic, semantic, and world knowledge [E2]. This pre-training method is versatile and can be applied to both single-corpus settings (where both the question and knowledge source are Wikipedia) and separate-corpus settings (where the question source is CC-News and the knowledge source is Wikipedia) [E1].

**Retrieval Quality**
The retriever is trained using a performance-based signal from unsupervised text, rewarding retrievals that improve the language model's perplexity [E5]. The model is designed to retrieve and attend over documents from a large corpus, such as Wikipedia, during pre-training, fine-tuning, and inference [E4]. To manage the computational challenge of considering millions of candidate documents, the retriever is structured to use Maximum Inner Product Search (MIPS) so that computations can be cached and asynchronously updated [E5]. As a result, REALM achieves high performance while retrieving significantly fewer documents than other retrieval-based systems; specifically, REALM retrieves 5 documents to achieve its best performance, whereas other systems typically retrieve between 20 and 80 documents [E1].

**Downstream Fine-tuning**
The pre-trained model can be further trained through fine-tuning for downstream tasks like Open-QA, which often leads to better generalization than training from scratch [E2]. REALM's approach provides qualitative benefits during these stages, including increased modularity and interpretability [E2, E4, E5].

### Metrics

- baseline_latency_seconds: 6.997
- orchestrator_latency_seconds: 61.073
- baseline_total_tokens: 4915
- orchestrator_total_tokens: 34658
- baseline_citation_count: 5
- orchestrator_evidence_count: 9
- fact_check_status_counts: {'supported': 12}

## Question 12

Type: multi-step reasoning

Explain step by step how a masked-language-model pre-training objective can improve downstream open-domain QA in REALM.

### Baseline Answer

In REALM, a masked-language-model (MLM) pre-training objective improves downstream open-domain question answering (Open-QA) through the following process:

1.  **Unsupervised Pre-training with MLM:** The model is pre-trained on an unlabeled corpus using a masked language modeling objective [1]. In this task, tokens are randomly masked in a text passage, and the model must predict the missing tokens using its representation of the masked input [1].
2.  **Learning World Knowledge:** To successfully predict these missing tokens, a good MLM must learn to encode syntactic and semantic information as well as world knowledge [1]. 
3.  **Augmentation with a Latent Knowledge Retriever:** REALM augments this pre-training by adding a learned textual knowledge retriever [2, 5]. This retriever allows the model to retrieve and attend over documents from a large corpus (such as Wikipedia) during the pre-training phase [2].
4.  **End-to-End Optimization:** The retriever is trained using the performance-based signal from the MLM objective [5]. A retrieval that improves the language model's perplexity is rewarded, while uninformative retrievals are penalized [5]. This is achieved by modeling the "retrieve-then-predict" approach as a latent variable language model and optimizing the marginal likelihood [5]. This allows the signal from the language modeling objective to backpropagate through the retrieval step [2].
5.  **Transfer to Downstream Open-QA:** Because the retriever is designed to retrieve text rather than labeled examples, it can transfer to other tasks [5]. The model, having learned to use retrieved documents to inform its predictions during pre-training, can then be fine-tuned for Open-QA, where it uses the retriever to find potentially relevant documents to help identify the correct answer string [3, 5].

Citations:
[1] data/2002.08909v1.pdf, chunk_id: 2002.08909v1-2-7f240c64641ad3f52fc62e97
[2] data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944

### Multi-Agent Answer

The process of using a masked-language-model (MLM) pre-training objective to improve downstream open-domain question answering (Open-QA) in REALM involves the following steps:

1.  **Unsupervised Pre-training via MLM**: The model performs a masked language modeling task, which requires predicting the original value of each [MASK] token in an input sentence [E4]. This process uses unlabeled text to learn useful language representations, including syntactic information, semantic information, and world knowledge [E1].
2.  **Integration of a Latent Knowledge Retriever**: To capture knowledge in a more modular and interpretable way than storing it implicitly in neural network parameters, REALM augments pre-training with a latent knowledge retriever [E2]. This retriever allows the model to retrieve and attend over documents from a large corpus, such as Wikipedia, during the pre-training stage [E2].
3.  **Backpropagation through Retrieval**: The MLM task serves as the learning signal for the entire system [E2]. This signal is backpropagated through a retrieval step that considers millions of documents [E2]. In this framework, retrieval that improves the language model's perplexity is rewarded, while uninformative retrieval is penalized [E3].
4.  **Fine-tuning for Open-QA**: The resulting pre-trained model is then fine-tuned for the downstream Open-QA task [E1]. While the pre-training task involves predicting masked tokens, the fine-tuning task involves predicting an answer string that is found as a contiguous sequence of tokens within a document [E4, E5].

### Metrics

- baseline_latency_seconds: 6.640
- orchestrator_latency_seconds: 63.573
- baseline_total_tokens: 5874
- orchestrator_total_tokens: 38107
- baseline_citation_count: 5
- orchestrator_evidence_count: 11
- fact_check_status_counts: {'unsupported': 4, 'supported': 8}

## Question 13

Type: multi-step reasoning / error analysis

If REALM retrieves an irrelevant document, how would that affect p(z|x), p(y|z,x), and the final answer prediction?

### Baseline Answer

If REALM retrieves an irrelevant document $z$, the following effects occur based on the provided context:

*   **$p(z|x)$:** The retriever models the distribution of possibly helpful documents $z$ given input $x$ [3]. An irrelevant document would be one where the relevance score $f(x, z)$ (the inner product of the vector embeddings of $x$ and $z$) does not appropriately reflect its lack of usefulness [3].
*   **$p(y|z, x)$:** The value of the Retrieval Utility (RU) is used to measure how useful a document $z$ is for predicting the output $y$ [1]. If a document is irrelevant, it may result in a negative RU, which indicates that $z$ is less useful for predicting $y$ than a null document [1].
*   **Final answer prediction ($p(y|x)$):** The overall likelihood of generating the answer $y$ is obtained by marginalizing over all possible documents $z$ using the formula $p(y|x) = \sum_{z \in Z} p(y|z, x)p(z|x)$ [3]. Because the model is trained to reward retrievals that improve perplexity and penalize uninformative ones, an uninformative (irrelevant) retrieval is something the system is designed to penalize [4].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-20-58cd33db77feaae8a3f8d036, chunk_index: 20
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7, chunk_index: 3
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952, chunk_index: 1

### Multi-Agent Answer

The provided evidence does not explicitly state the specific mathematical changes to $p(z|x)$ or $p(y|z,x)$ when an irrelevant document is retrieved, but it provides information regarding Retrieval Utility (RU) and training signals:

*   **Retrieval Utility and $p(y|z, x)$:** Retrieval Utility is defined as $RU = \log p(y |z, x) - \log p(y |\emptyset, x)$ [E1]. If a retrieved document $z$ is irrelevant to $x$, the RU may be negative, indicating that $z$ is less useful for predicting $y$ than a null document [E1].
*   **Training Signals:** During training, the retriever is rewarded for retrievals that improve the language model's perplexity, while uninformative retrievals should be penalized [E8].
*   **$p(z|x)$:** The evidence does not provide a direct description of how the probability $p(z|x)$ specifically changes when a document is irrelevant, though it notes that a "trivial" retrieval (where $z$ is too informative due to being an exact match) results in a large positive gradient for $p(z|x)$ [E2].

In summary, while the notes do not provide the exact functional form for how these probabilities shift when a document is irrelevant, they indicate that an irrelevant retrieval results in a negative RU [E1] and that such uninformative retrievals are intended to be penalized during the training process [E8].

### Metrics

- baseline_latency_seconds: 6.745
- orchestrator_latency_seconds: 32.564
- baseline_total_tokens: 5063
- orchestrator_total_tokens: 19562
- baseline_citation_count: 5
- orchestrator_evidence_count: 9
- fact_check_status_counts: {'supported': 5}

## Question 14

Type: limitation/uncertainty

What limitations, uncertainties, or missing comparisons should be noted when interpreting REALM's reported results?

### Baseline Answer

When interpreting REALM's reported results, the following limitations, uncertainties, or missing comparisons should be noted:

*   **Missing Data for Benefit:** Certain data could potentially benefit REALM, but it was not used in the experiments [1].
*   **Uncertainty in Retrieval Utility (RU):** A negative RU indicates that the document $z$ is less useful for predicting $y$ than the null document; however, this could mean $z$ is irrelevant to $x$, or it could mean the masked tokens in $x$ do not require world knowledge, or that the necessary world knowledge is already sufficiently commonplace within the model's parameters [2].
*   **Impact of Index Staleness:** Using a stale MIPS index can hurt model training, and results suggest that further reducing this staleness could offer better optimization [4].
*   **Sensitivity to Masking:** The latent variable learning used in REALM relies heavily on the utility of retrieval and is therefore more sensitive to a consistent learning signal [4].
*   **Scope of Work:** The presented work is considered a "minimal instantiation" of a family of REALM-like approaches [5]. Potential generalizations to structured knowledge, multi-lingual settings, and multi-modal settings were identified as future work [5].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-20-58cd33db77feaae8a3f8d036
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e
[5] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-15-e73576

### Multi-Agent Answer

When interpreting REALM's reported results, the following limitations, uncertainties, and comparisons should be noted:

**Data and Experimental Limitations**
* Certain types of data that could potentially benefit REALM were not used in the experiments [E1].
* Using a stale MIPS index can negatively impact model training, which necessitates frequent index refreshes for optimization [E2].
* Optimal results for the model require both the encoder and the retriever to act in unison, even though both components benefit from being trained separately [E2].

**Uncertainties in Retrieval Utility (RU)**
* A negative Retrieval Utility (RU) indicates that a retrieved document is less useful for predicting a masked token than a null document [E4].
* This negative utility is uncertain in its cause, as it could mean the document is irrelevant to the question, the masked tokens do not require world knowledge, or the necessary world knowledge is already embedded within the model’s parameters [E4].

**Comparisons and Baselines**
* The most direct comparison to REALM is ORQA, because the two share identical training data, hyperparameters, and fine-tuning setups [E1, E5].
* For generation-based baselines, the study compares REALM against T5 [E5].

### Metrics

- baseline_latency_seconds: 6.835
- orchestrator_latency_seconds: 31.781
- baseline_total_tokens: 4632
- orchestrator_total_tokens: 19097
- baseline_citation_count: 5
- orchestrator_evidence_count: 9
- fact_check_status_counts: {'supported': 8}

## Question 15

Type: citation grounding / uncertainty

Which claims about REALM's performance or mechanism cannot be verified unless the answer cites specific experimental evidence from the paper?

### Baseline Answer

Based on the provided text, the following claims about REALM's performance or mechanism cannot be verified without citing specific experimental evidence (such as the contents of Table 2, Table 1, or Table 4):

*   **Comparison to ORQA:** While it is stated that the improvement of REALM over ORQA is "purely due to better pre-training methods" [1], the specific extent of this improvement or the direct comparison of results requires the experimental data mentioned in the context.
*   **Overall Performance vs. Document Count:** The claim that REALM "gets the overall best performance while only retrieving 5 documents" compared to other retrieval-based systems that retrieve 20 to 80 documents [1] requires the underlying experimental results to be verified.
*   **Ablation Results for NaturalQuestions-Open:** The specific findings regarding the ablation of critical components of REALM and how often the gold answer appears in the top-5 retrievals are contained in Table 2 [1, 4], which is not provided in full detail.
*   **Encoder and Retriever Benefits:** The claim that "both the encoder and retriever benefit from REALM training separately, but the best result requires both components acting in unison" [4] relies on the results of resetting parameters to their baseline state, which are part of the experimental analysis.
*   **MIPS Index Refresh Rate:** The assertion that "a stale index can hurt model training" and that reducing staleness could offer better optimization is based on results in Table 2 [4].
*   **Knowledge Adaptation:** The example demonstrating how REALM adapts to an updated knowledge corpus (specifically regarding the "Excellent Cadaver" Wikipedia page) is illustrated in Table 4 [3], which provides the specific evidence for this mechanism.
*   **Retrieval Utility (RU) Trends:** The observation that RU "increases steadily over the course of pre-training" and is "more predictive of good performance... than even the overall log-likelihood" [3] refers to data presented in Figure 4 [3].
*   **Direct Comparison of Models:** The comparison between REALM and BERT regarding the probability assigned to the correct term "Fermat" is presented as evidence in Table 3 [4].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-

### Multi-Agent Answer

Based on the provided evidence, the following claims regarding REALM's performance and mechanism are verifiable through specific experimental evidence or data:

*   **Improvement over ORQA:** The claim that REALM's improvement over ORQA is purely due to better pre-training methods can be verified because the fine-tuning setup, hyperparameters, and training data between the two models were identical [E1].
*   **Comparative Accuracy:** The claim that REALM outperforms all previous state-of-the-art methods for both explicit and implicit knowledge storage on three popular Open-QA benchmarks can be verified by the reported margin of 4-16% absolute accuracy [E9, E10].
*   **Retrieval Efficiency:** The claim that REALM achieves the best overall performance while retrieving fewer documents can be verified by the specific measurements that REALM retrieves 5 documents, whereas other retrieval-based systems typically retrieve between 20 and 80 documents [E1].
*   **Predictive Utility of RU:** The claim that Retrieval Utility (RU) is a more predictive indicator of good performance on downstream Open-QA tasks than overall log-likelihood is supported by the findings regarding RU behavior [E8].
*   **Corpus Adaptability:** The claim that a REALM model can adapt to an updated knowledge corpus can be verified by the example of a model pre-trained on a 2018 corpus successfully retrieving "Lawrence" from a Wikipedia page added in 2019 when using a 2020 corpus [E8].

### Metrics

- baseline_latency_seconds: 6.744
- orchestrator_latency_seconds: 29.822
- baseline_total_tokens: 4619
- orchestrator_total_tokens: 19656
- baseline_citation_count: 5
- orchestrator_evidence_count: 10
- fact_check_status_counts: {'supported': 5}
