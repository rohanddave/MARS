# experiment01: architecture control, all small models, top_k=5

## Agent Configuration

- family: architecture_control
- control_variable: agent_architecture
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

REALM retrieves from a large textual knowledge corpus ($Z$), such as Wikipedia [1, 2]. This retrieval is used during pre-training, fine-tuning, and inference [2].

The model uses this information through a "retrieve-then-predict" generative process [3]:
1.  **Retrieve:** Given an input $x$, the model first retrieves potentially helpful documents $z$ from the knowledge corpus $Z$ by modeling it as a sample from the distribution $p(z | x)$ [3].
2.  **Predict:** The model then conditions on both the retrieved documents $z$ and the original input $x$ to generate the output $y$, modeled as $p(y | z, x)$ [3]. The language model attends over these retrieved documents to help inform its prediction [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7

### Multi-Agent Answer

REALM retrieves information from a large knowledge corpus ($Z$), such as Wikipedia [E2, E3]. The framework can be applied in a single-corpus setting where both the input and knowledge source are Wikipedia, or in a separate-corpus setting where the knowledge corpus is Wikipedia and the input text comes from a different source, such as CC-News [E4].

The model uses this retrieved knowledge through a "retrieve-then-predict" generative process [E1]. Specifically, the process is decomposed into two steps: the model first retrieves documents $z$ from the corpus $Z$ based on the probability $p(z|x)$, and then it conditions the output generation on both the retrieved documents and the input $x$ [E1]. During pre-training, fine-tuning, and inference, the model attends over the retrieved documents to help inform its predictions [E3]. This approach allows the model to use the retrieved documents as grounded memories, which provides provenance for predicted answers [E5].

### Metrics

- baseline_latency_seconds: 8.725
- orchestrator_latency_seconds: 34.382
- baseline_total_tokens: 5445
- orchestrator_total_tokens: 20722
- baseline_citation_count: 5
- orchestrator_evidence_count: 7
- fact_check_status_counts: {'supported': 6}

## Question 2

Type: easy lookup

Which downstream tasks or benchmarks does the paper use to evaluate REALM?

### Baseline Answer

The paper uses the NaturalQuestions-Open benchmark to evaluate REALM [1]. Additionally, the text mentions that the model is relevant for applications such as Open-QA [2, 5].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-14-83fbe5c3ec4e1ed386558b56
[5] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-15-e73576ceacc6e97a0666fd10

### Multi-Agent Answer

REALM is used to achieve state-of-the-art results on Open-domain Question Answering (Open-QA) benchmarks [E5]. Specifically, the paper notes that REALM outperformed previous systems by 4-16% absolute accuracy across three benchmarks: Natural Questions-Open, Web Questions, and Curated TREC [E5].

### Metrics

- baseline_latency_seconds: 7.111
- orchestrator_latency_seconds: 27.345
- baseline_total_tokens: 4341
- orchestrator_total_tokens: 17949
- baseline_citation_count: 5
- orchestrator_evidence_count: 7
- fact_check_status_counts: {'supported': 2}

## Question 3

Type: definition

What is REALM, and what does the paper mean by retrieval-augmented language model pre-training?

### Baseline Answer

REALM (Retrieval-Augmented Language Model) is a novel framework that augments language model pre-training algorithms with a learned textual knowledge retriever [1, 2]. Unlike traditional models that store knowledge implicitly in their parameters, REALM explicitly exposes the role of world knowledge by requiring the model to decide what knowledge to retrieve and use during inference [1, 2]. This approach allows the model to retrieve and attend over documents from a large corpus, such as Wikipedia, to inform its predictions [1, 2].

The paper defines "retrieval-augmented language model pre-training" as a process that incorporates a large-scale neural retrieval module during the pre-training stage [1]. In this framework, the model follows a "retrieve-then-predict" approach:
*   **Retrieve:** Given an input $x$, the model first retrieves potentially helpful documents $z$ from a knowledge corpus $Z$ [3]. 
*   **Predict:** The model then conditions on both the retrieved documents and the original input to generate an output $y$ [3].

For the pre-training task specifically, the model performs masked language modeling, where $x$ is a sentence from a pre-training corpus with certain tokens masked, and the model must predict those missing tokens $y$ [3]. The retriever is trained in an unsupervised manner using a performance-based signal: retrieval that improves the language model's perplexity is rewarded, while uninformative retrieval is penalized [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7

### Multi-Agent Answer

REALM (Retrieval-Augmented Language Model) is a retrieval-augmented language model that extends the retrieval-based approach to language model pre-training [E2]. It augments pre-training with a latent knowledge retriever to capture knowledge in a modular and interpretable way [E6]. Unlike standard reading comprehension models that comprehend a single document, REALM is designed for Open-domain Question Answering (Open-QA), which requires retaining knowledge from millions of documents [E2].

The model consists of two primary components: a neural knowledge retriever, which models $p(z|x)$, and a knowledge-augmented encoder, which models $p(y|z, x)$ [E2]. The retriever uses a dense inner product model where relevance scores are defined as the inner product of $d$-dimensional vector embeddings [E2]. Because the model's memories are associated with specific documents, they are considered "grounded," providing a level of interpretability and provenance necessary for trustworthy Open-QA applications [E1].

Retrieval-augmented language model pre-training refers to a method where the model's ability to retrieve and attend over documents from a large corpus—such as Wikipedia—is integrated into the pre-training process [E6]. This framework allows the model to use a knowledge retriever during pre-training, fine-tuning, and inference [E6]. During pre-training, the retriever can be trained in an unsupervised manner using masked language modeling as the learning signal [E6]. This approach decomposes the process of learning a distribution $p(y|x)$ into two steps: retrieving a document and then predicting [E2].

### Metrics

- baseline_latency_seconds: 10.115
- orchestrator_latency_seconds: 39.313
- baseline_total_tokens: 5740
- orchestrator_total_tokens: 21836
- baseline_citation_count: 5
- orchestrator_evidence_count: 7
- fact_check_status_counts: {'supported': 10}

## Question 4

Type: definition

How does REALM differ from a standard parametric language model such as BERT in where knowledge is stored and accessed?

### Baseline Answer

Standard parametric language models, such as BERT, store learned world knowledge implicitly within the parameters of the underlying neural network [1]. This approach has limitations: it is difficult to determine what knowledge is stored or where it is located, and because storage space is limited by the size of the network, capturing more facts requires training increasingly larger networks, which can be expensive or slow [1].

In contrast, REALM (Retrieval-Augmented Language Model) differs in the following ways:

*   **Storage:** Instead of relying solely on implicit parameter storage, REALM augments language model pre-training with a learned textual knowledge retriever that allows the model to access a large textual knowledge corpus, such as Wikipedia [1, 2].
*   **Access:** Before making a prediction, the model uses the retriever to retrieve documents from the knowledge corpus and then attends over those documents to inform its prediction [2].
*   **Qualitative Benefits:** This method provides more modular and interpretable knowledge storage compared to standard models [1]. Specifically, REALM's memories are "grounded" because each memory is associated with a specific document rather than unnamed value vectors [3].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-15-e73576ceacc6e97a0666fd10

### Multi-Agent Answer

Standard language model pre-training captures world knowledge implicitly within the parameters of a neural network [E4]. This implicit storage of knowledge requires increasingly larger networks to cover more facts [E4].

In contrast, REALM (Retrieval-Augmented Language Model) uses a learned textual knowledge retriever to capture knowledge in a more modular and interpretable way [E2]. Rather than relying solely on parameters, REALM explicitly exposes the role of world knowledge by requiring the model to decide what knowledge to retrieve and use during inference [E2]. Specifically, before making a prediction, the language model uses the retriever to retrieve documents from a large corpus, such as Wikipedia, and then attends over those documents to help inform its prediction [E2].

### Metrics

- baseline_latency_seconds: 5.825
- orchestrator_latency_seconds: 54.912
- baseline_total_tokens: 6577
- orchestrator_total_tokens: 37575
- baseline_citation_count: 5
- orchestrator_evidence_count: 8
- fact_check_status_counts: {'supported': 5}

## Question 5

Type: method/mechanism

How does REALM's retrieve-then-predict framework work, including the role of the latent document variable z?

### Baseline Answer

REALM's retrieve-then-predict framework decomposes the probability of an output $y$ given an input $x$, denoted as $p(y | x)$, into two distinct steps:

1.  **Retrieve**: Given an input $x$, the model first retrieves potentially helpful documents $z$ from a knowledge corpus $Z$ [3]. This retrieval step is modeled as a sample from the distribution $p(z | x)$ [3].
2.  **Predict**: The model then conditions on both the retrieved document $z$ and the original input $x$ to generate the output $y$, which is modeled as $p(y | z, x)$ [3].

**The Role of the Latent Document Variable $z$**
The framework treats the retrieved document $z$ as a latent variable [3]. To obtain the overall likelihood of generating an output $y$ for a given input $x$, the model marginalizes over all possible documents $z$ in the corpus $Z$ [3]. This is expressed mathematically as:
$$p(y | x) = \sum_{z \in Z} p(y | z, x) p(z | x)$$ [3]

By modeling the approach as a latent variable language model and optimizing the marginal likelihood, the model can be trained using a performance-based signal from unsupervised text [1]. For example, a retrieval that improves the language model's perplexity is rewarded, while uninformative retrievals are penalized [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952, chunk_index: 1
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7, chunk_index: 3

### Multi-Agent Answer

REALM (Retrieval-Augmented Language Model) decomposes the generation of an output $y$ from an input $x$ into a two-step process [E4]. First, the model uses a learned textual knowledge retriever to retrieve documents $z$ from a knowledge corpus $Z$ using $p(z|x)$ [E4]. Second, the model generates the output $y$ conditioned on both the input $x$ and the retrieved documents $z$ using $p(y|z, x)$ [E4]. Before making each prediction, the language model attends over the retrieved documents to help inform its prediction [E1].

The framework is modeled as a latent variable language model where the marginal likelihood is optimized [E1]. The retriever is described as a "latent knowledge retriever" [E2], and the model can marginalize over candidate documents [E3]. During fine-tuning inference, the model specifically considers the top-5 candidates [E3].

### Metrics

- baseline_latency_seconds: 5.910
- orchestrator_latency_seconds: 63.453
- baseline_total_tokens: 5594
- orchestrator_total_tokens: 41184
- baseline_citation_count: 5
- orchestrator_evidence_count: 9
- fact_check_status_counts: {'supported': 6}

## Question 6

Type: method/mechanism

How does the paper train the retriever when the retrieved document is latent, and how does learning signal flow back to retrieval?

### Baseline Answer

To train the retriever when the retrieved document is treated as a latent variable, REALM models the retrieve-then-predict approach as a latent variable language model and optimizes the marginal likelihood [1]. Specifically, the model decomposes the probability of an output $y$ given an input $x$, denoted as $p(y|x)$, by marginalizing over all possible documents $z$ in the knowledge corpus $Z$, expressed by the formula:
$p(y |x) = \sum_{z \in Z} p(y |z, x) p(z |x)$ [4].

The learning signal flows back to the retrieval module through backpropagation from the language modeling objective [2]. The training uses a performance-based signal from unsupervised text: a retrieval that improves the language model's perplexity is rewarded, while uninformative retrievals are penalized [1]. For example, if the model needs to fill a blank in a sentence, the retriever is rewarded for selecting a document that contains the information necessary to complete that blank [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7

### Multi-Agent Answer

The REALM framework treats the retrieved document $z$ as a latent variable [E1, E5]. To train the model, the overall likelihood of generating a target $y$ is obtained by marginalizing over all possible documents $z$ in the knowledge corpus $Z$ [E5].

The learning signal for the retriever is provided by masked language modeling, which serves as an unsupervised signal for pre-training [E2]. The retriever is trained using a performance-based signal where a retrieval is rewarded if it improves the language model's perplexity and penalized if it is uninformative [E1]. Specifically, the signal from the language modeling objective backpropagates through the retrieval step to optimize the marginal likelihood [E1, E2].

### Metrics

- baseline_latency_seconds: 5.247
- orchestrator_latency_seconds: 52.698
- baseline_total_tokens: 5399
- orchestrator_total_tokens: 36558
- baseline_citation_count: 5
- orchestrator_evidence_count: 9
- fact_check_status_counts: {'unsupported': 2, 'supported': 3}

## Question 7

Type: method/mechanism / implementation

What approximations or engineering choices does REALM use to make retrieval over a large corpus practical during training and inference?

### Baseline Answer

To make retrieval over a large corpus practical during training and inference, REALM employs the following engineering choices and approximations:

*   **Retriever Structure:** The retriever is structured so that the computation performed for each document can be cached and updated asynchronously [2].
*   **MIPS Formulation:** The selection of the best documents is formulated as a Maximum Inner Product Search (MIPS) [2]. 
*   **MIPS Index Management:** During pre-training, a parallel process is used to re-embed corpus documents and rebuild the MIPS index, resulting in an index refresh approximately every 500 training steps [5].
*   **Pre-training Retrieval:** For each pre-training example, the model retrieves and marginalizes over 8 candidate documents, which includes a null document $\emptyset$ [4].
*   **Fine-tuning Inference:** During fine-tuning inference, the system considers only the top-5 candidate documents [1, 4].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05, chunk_index: 12
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952, chunk_index: 1
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-11-3fa55fc3148d1188cb70ab91, chunk_index: 11
[5] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e, chunk_index: 13

### Multi-Agent Answer

To handle the computational challenge of considering millions of documents within a corpus, REALM employs several engineering choices and approximations:

*   **Efficiency Solutions:** The retriever uses cached computation and Maximum Inner Product Search (MIPS) [E1].
*   **Training Approximations:** The framework is designed to address the computational challenge of backpropagating through a retrieval step that involves millions of documents [E3]. The retriever is trained using a performance-based signal from unsupervised text, rewarding retrievals that improve the language model's perplexity [E1].
*   **Inference Approximations:** During fine-tuning inference, the model considers the top-5 candidate documents [E2, E4]. Additionally, for each example, the model retrieves and marginalizes over 8 candidate documents, which includes a null document [E4].

### Metrics

- baseline_latency_seconds: 6.375
- orchestrator_latency_seconds: 31.834
- baseline_total_tokens: 5652
- orchestrator_total_tokens: 21660
- baseline_citation_count: 5
- orchestrator_evidence_count: 6
- fact_check_status_counts: {'supported': 5}

## Question 8

Type: comparison

How does REALM compare with ORQA or other open-domain QA baselines, and what evidence supports that comparison?

### Baseline Answer

REALM compares to ORQA and other baselines as follows:

*   **Comparison with ORQA:** ORQA is considered the most direct comparison to REALM because the fine-tuning setup, training data, and hyperparameters are identical [1]. The improvement REALM shows over ORQA is attributed solely to better pre-training methods [1]. Additionally, resetting both the REALM encoder and retriever parameters to their baseline states reduces the system to the ORQA baseline [5].
*   **Comparison with Retrieval-based Systems:** Compared to other retrieval-based systems (such as Asai et al., 2019; Min et al., 2019a;b), which frequently retrieve between 20 to 80 documents, REALM achieves the overall best performance while retrieving only 5 documents [1].
*   **Comparison with Generation-based Systems:** REALM is compared against state-of-the-art systems from the generation paradigm [4]. A competitive generation-based baseline used for comparison is T5, specifically concurrent work that fine-tunes T5 for Open-QA [2].
*   **Comparison with BERT:** In terms of masked language model prediction, REALM assigns a much higher probability to a correct term than the BERT model does [5]. For example, when predicting the term "Fermat," BERT assigned a probability of $1.1 \times 10^{-14}$, whereas REALM's marginal probability was $0.129$ [5].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-10-8ea61faa3a17c1fc8f8725d8
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7
[5

### Multi-Agent Answer

REALM demonstrates superior performance compared to ORQA and other open-domain QA baselines across several benchmarks [E4].

### Comparison with ORQA
ORQA is considered the most direct comparison to REALM because both systems utilize identical training data, hyperparameters, and fine-tuning setups [E2]. Additionally, the retrievers for both REALM pretraining and ORQA are initialized using the Inverse Cloze Task [E1]. The improvement of REALM over ORQA is attributed purely to its superior pre-training methods [E2, E4]. 

Specific benchmark performance for the NaturalQuestions (NQ) dataset shows REALM achieved a score of 39.2 (using Wikipedia) or 40.4 (using CC-News), while ORQA scored 33.3 [E4]. On the WQ benchmark, REALM achieved 40.2 (Wikipedia) or 40.7 (CC-News) compared to ORQA's 36.4 [E4]. On the CT benchmark, REALM achieved 46.8 (Wikipedia) or 42.9 (CC-News) compared to ORQA's 30.1 [E4].

### Comparison with Other Baselines
REALM outperforms the largest T5-11B model while being 30 times smaller [E4]. In the NQ (79k/4k) benchmark, REALM scored 39.2 (Wikipedia) and 40.4 (CC-News), outperforming T5-11B's scores of 34.5 and 33.3 respectively [E4]. In the WQ (3k/2k) benchmark, REALM achieved 40.2 (Wikipedia) and 40.7 (CC-News), whereas T5-11B achieved 37.4 [E4]. 

Compared to other retrieval-based systems, such as those by Asai et al. (2019) and Min et al. (2019a;b), REALM achieves the best overall performance while retrieving fewer documents [E2]. While those other systems typically retrieve between 20 to 80 documents, REALM achieves its best performance by retrieving only 5 documents [E2].

### Metrics

- baseline_latency_seconds: 6.637
- orchestrator_latency_seconds: 72.033
- baseline_total_tokens: 5305
- orchestrator_total_tokens: 37179
- baseline_citation_count: 5
- orchestrator_evidence_count: 8
- fact_check_status_counts: {'unsupported': 4, 'supported': 8}

## Question 9

Type: comparison

How does REALM's retrieval-based approach compare with storing knowledge only in model parameters?

### Baseline Answer

REALM's retrieval-based approach differs from models that store knowledge only in their parameters in several ways:

*   **Interpretability and Modularity:** Unlike models that store knowledge implicitly in their parameters, making it difficult to determine what knowledge is stored and where, REALM's approach captures knowledge in a more interpretable and modular way [1, 3]. REALM's "memories" are grounded because each memory is associated with a specific document rather than unnamed value vectors, which is crucial for providing provenance for predicted answers in tasks like Open-domain Question Answering (Open-QA) [5].
*   **Explicit Knowledge Role:** REALM explicitly exposes the role of world knowledge by requiring the model to decide what knowledge to retrieve and use during inference [1].
*   **Storage Constraints:** In models where knowledge is stored implicitly in parameters, storage space is limited by the size of the network; capturing more knowledge requires training increasingly larger networks, which can be prohibitively expensive or slow [3].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952, chunk_index: 1
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2, chunk_index: 0
[5] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-15-e73576ceacc6e97a0666fd10, chunk_index: 15

### Multi-Agent Answer

Traditional language model pre-training captures world knowledge by storing it implicitly within the parameters of a neural network [E4]. This method of implicit storage requires increasingly larger networks to cover more facts, which can be prohibitively slow or expensive [E4].

In contrast, the REALM framework augments pre-training with a learned textual knowledge retriever to capture knowledge in a more modular and interpretable manner [E2, E4]. This approach explicitly exposes the role of world knowledge by requiring the model to decide what knowledge to retrieve and use during inference [E2]. During this process, the model retrieves documents from a large corpus, such as Wikipedia, and attends over those documents to help inform its predictions [E2].

REALM provides specific qualitative benefits over models that rely on unnamed value vectors [E5]:

*   **Interpretability and Modularity:** The framework is designed to be more modular and interpretable [E2, E4].
*   **Grounded Memories:** REALM's memories are grounded, meaning each memory is associated with a specific document rather than unnamed value vectors [E5]. This level of interpretability is considered crucial for Open-QA applications, where users require provenance for a predicted answer to be trustworthy [E5].

### Metrics

- baseline_latency_seconds: 5.438
- orchestrator_latency_seconds: 56.035
- baseline_total_tokens: 5501
- orchestrator_total_tokens: 36718
- baseline_citation_count: 5
- orchestrator_evidence_count: 8
- fact_check_status_counts: {'supported': 6, 'unsupported': 2}

## Question 10

Type: evidence synthesis / ablation

What ablation or diagnostic evidence shows that retrieval pre-training improves REALM rather than only the reader component?

### Baseline Answer

To determine whether REALM pre-training improves the retriever, the encoder, or both, researchers performed an ablation where they reset the parameters of either the retriever or the encoder to their baseline state before fine-tuning [4]. 

The diagnostic evidence from this ablation shows that:
*   Both the encoder and the retriever benefit from REALM training when treated separately [4].
*   The best results are achieved when both components act in unison [4].
*   Resetting both the retriever and the encoder reduces the system to the main baseline, ORQA [4].

Additionally, the researchers reported how often the gold answer appears in the top-5 retrievals before applying any fine-tuning; this specific metric is used to more significantly isolate the contribution of improving the retriever during pre-training [1, 4].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e

### Multi-Agent Answer

The improvement of REALM over ORQA is attributed purely to better pre-training methods [E3]. ORQA serves as the most direct comparison to REALM because the fine-tuning setup, hyperparameters, and training data are identical between the two models [E3]. 

To isolate the specific contribution of improving the retriever during pre-training, the authors use the frequency of the gold answer appearing in the top-5 retrievals before any fine-tuning is applied as a metric [E6]. While the evidence notes indicate that results for ablating critical components of REALM were presented in a "Table 2," the specific numerical data or findings from that table are not provided in the notes [E6].

### Metrics

- baseline_latency_seconds: 4.208
- orchestrator_latency_seconds: 27.290
- baseline_total_tokens: 4551
- orchestrator_total_tokens: 20059
- baseline_citation_count: 5
- orchestrator_evidence_count: 7
- fact_check_status_counts: {'supported': 4}

## Question 11

Type: evidence synthesis

Synthesize the evidence for why REALM improves open-domain QA performance, including retrieval quality, pre-training, and downstream fine-tuning.

### Baseline Answer

REALM improves open-domain Question Answering (Open-QA) performance through the following mechanisms:

*   **Pre-training:** REALM uses a novel approach where the language model is augmented with a learned textual knowledge retriever during pre-training [4]. The retriever is trained in an unsupervised manner using masked language modeling as the learning signal [4]. The system is optimized by maximizing the marginal likelihood of a "retrieve-then-predict" generative process, where the retriever is rewarded if it selects documents that improve the language model's perplexity [2, 5]. This pre-training method can be applied in both single-corpus (e.g., Wikipedia) and separate-corpus settings [1].
*   **Retrieval Quality:** Unlike previous systems that used non-learned or heuristic retrievers, REALM's retriever is designed to transfer to other tasks because it retrieves raw text rather than labeled examples [5]. The retriever's contribution to performance can be isolated by measuring how often the gold answer appears in the top-5 retrievals before fine-tuning [1]. Additionally, REALM achieves high performance with efficient retrieval, obtaining the best overall results while only retrieving 5 documents, whereas other retrieval-based systems often retrieve between 20 to 80 documents [1].
*   **Downstream Fine-tuning:** REALM's retriever is specifically designed to transfer to downstream tasks [5]. When fine-tuned on Open-QA benchmarks, REALM outperformed previous state-of-the-art methods by a significant margin of 4-16% absolute accuracy [4, 5]. Comparisons with ORQA show that REALM's improvements are purely due to its superior pre-training methods, even when the fine-tuning setup, hyperparameters, and training data are identical [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7
[4] source: data/

### Multi-Agent Answer

REALM improves open-domain question answering (Open-QA) performance by extending the retrieval-based paradigm to language model pre-training [E5]. 

**Pre-training and Knowledge Representation**
The framework utilizes masked language modeling (MLM) as an unsupervised learning signal to pre-train a latent knowledge retriever [E3]. This pre-training process allows the model to learn useful representations of language from unlabeled text corpora [E2]. While traditional language model pre-training often stores world knowledge implicitly within neural network parameters—requiring increasingly larger networks to cover more facts [E3]—REALM augments the model with a latent knowledge retriever to capture knowledge in a more modular and interpretable way [E3]. This approach provides qualitative benefits, including improved modularity and interpretability [E2, E3].

**Retrieval Quality**
The model's retrieval process is designed to handle the scale of Open-QA, where questions may pertain to any document within a corpus of millions [E3, E5]. REALM achieves its best performance by retrieving as few as five documents, whereas other retrieval-based systems typically retrieve between 20 and 80 documents [E1]. The relevance of a document is determined using a dense inner product model, where the relevance score is defined as the inner product of the vector embeddings for the input and the document [E5].

**Downstream Fine-tuning**
The effectiveness of REALM is demonstrated by fine-tuning it on the task of Open-domain Question Answering [E3]. When compared to ORQA, the improvement in REALM's performance is attributed purely to its superior pre-training methods, as the fine-tuning setups, hyperparameters, and training data are identical between the two [E1]. Through this method, REALM achieves new state-of-the-art results on three benchmarks, outperforming previous systems by 4-16% in absolute accuracy [E2, E3].

### Metrics

- baseline_latency_seconds: 6.490
- orchestrator_latency_seconds: 61.121
- baseline_total_tokens: 4915
- orchestrator_total_tokens: 33997
- baseline_citation_count: 5
- orchestrator_evidence_count: 10
- fact_check_status_counts: {'unsupported': 4, 'supported': 8}

## Question 12

Type: multi-step reasoning

Explain step by step how a masked-language-model pre-training objective can improve downstream open-domain QA in REALM.

### Baseline Answer

In REALM, a masked-language-model (MLM) pre-training objective improves downstream open-domain question answering (Open-QA) through the following process:

1.  **Unsupervised Pre-training with MLM**: The model is pre-trained on an unlabeled corpus (such as Wikipedia) using a masked language modeling task [1]. In this task, tokens are randomly masked in a text passage, and the model must predict the value of those missing tokens [1, 4].
2.  **Integration of a Latent Knowledge Retriever**: Unlike standard language models that store world knowledge implicitly in their parameters, REALM augments pre-training with a learned textual knowledge retriever [2, 5]. This retriever allows the model to retrieve and attend over documents from a large corpus to help inform its predictions [2, 5].
3.  **Joint Training via Performance-Based Signals**: The retriever is trained using an unsupervised performance-based signal [5]. A retrieval that improves the language model's perplexity is rewarded, while uninformative retrievals are penalized [5]. This is achieved by modeling the "retrieve-then-predict" approach as a latent variable language model and optimizing the marginal likelihood, which allows the signal from the MLM objective to backpropagate through the retrieval step [2, 5].
4.  **Transfer to Downstream Open-QA**: Because the retriever is designed to transfer to other tasks—retrieving raw text rather than labeled examples—the model can be fine-tuned for Open-QA [5]. During fine-tuning, the task shifts from predicting masked tokens to predicting an answer string $y$ given a question $x$ [3, 4].

This approach allows the model to capture world knowledge in a more modular and interpretable way compared to models that rely solely on implicit parameter storage [2].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-2-7f240c64641ad3f52fc62e97
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b94

### Multi-Agent Answer

The masked-language-model (MLM) pre-training objective improves downstream open-domain question answering (Open-QA) in REALM through the following steps:

1.  **Unsupervised Pre-training on Unlabeled Corpora:** The model undergoes pre-training on unlabeled text corpora using an MLM objective [E1]. In this task, the model is required to predict the original value of each [MASK] token within an input text passage [E4].
2.  **Learning Essential Information:** Through this MLM pre-training process, the model learns syntactic information, semantic information, and world knowledge [E1].
3.  **Unsupervised Retriever Training:** REALM uses the MLM objective as a learning signal to perform unsupervised pre-training of a latent knowledge retriever [E2]. This training uses a performance-based signal from unsupervised text: retrievals that improve the language model's perplexity are rewarded, while uninformative retrievals are penalized [E3].
4.  **End-to-End Optimization:** The signal from the language modeling objective backpropagates through the retrieval step [E2]. This process enables the model to learn to retrieve and attend over documents from a large corpus to inform its predictions [E2, E3].
5.  **Downstream Generalization:** The resulting pre-trained model can then be fine-tuned for downstream tasks such as Open-QA, a process that often leads to better generalization than training the model from scratch [E1].

### Metrics

- baseline_latency_seconds: 6.391
- orchestrator_latency_seconds: 60.417
- baseline_total_tokens: 5874
- orchestrator_total_tokens: 38007
- baseline_citation_count: 5
- orchestrator_evidence_count: 12
- fact_check_status_counts: {'unsupported': 6, 'supported': 6}

## Question 13

Type: multi-step reasoning / error analysis

If REALM retrieves an irrelevant document, how would that affect p(z|x), p(y|z,x), and the final answer prediction?

### Baseline Answer

If REALM retrieves an irrelevant document, it affects the components as follows:

*   **$p(z|x)$**: An irrelevant document $z$ is one that is less useful for predicting the target $y$ than a null document $\emptyset$ [1]. The "usefulness" of retrieval is estimated by the Retrieval Utility (RU), and a negative RU indicates that $z$ is less useful for predicting $y$ than the null document [1].
*   **$p(y|z,x)$**: The context does not explicitly state how an irrelevant document changes the conditional probability $p(y|z,x)$, though it notes that the knowledge-augmented encoder is responsible for modeling this probability [3].
*   **Final answer prediction**: The overall likelihood of generating the answer $y$, denoted as $p(y|x)$, is obtained by treating $z$ as a latent variable and marginalizing over all possible documents $z$ [3]. This is calculated as $p(y |x) = \sum_{z \in Z} p(y |z, x) p(z |x)$ [3].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-20-58cd33db77feaae8a3f8d036, chunk_index: 20
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7, chunk_index: 3

### Multi-Agent Answer

The provided evidence does not explicitly state how $p(z|x)$ is affected specifically by an irrelevant document, though it notes that a "trivial" retrieval—where the masked sentence $x$ comes from document $z$—results in a large positive gradient for $p(z|x)$ [E2].

Regarding $p(y|z,x)$ and the final answer prediction, the following can be inferred from the evidence:

*   **Effect on $p(y|z,x)$:** If a retrieved document $z$ is irrelevant, it may result in a negative Retrieval Utility (RU) [E1]. A negative RU indicates that $z$ is less useful for predicting the target $y$ than the null document ($\emptyset$) [E1]. This relationship is defined by the formula $\text{RU} = \log p(y|z, x) - \log p(y|\emptyset, x)$ [E1].
*   **Possible causes for low utility:** A negative RU, which implies $z$ is less useful for predicting $y$, may suggest that $z$ is irrelevant to $x$, that the masked tokens do not require world knowledge, or that the necessary knowledge is already embedded in the model's parameters [E1].
*   **Training implications:** The training intuition for REALM is that retrieval that improves the language model’s perplexity should be rewarded, while an uninformative retrieval should be penalized [E8].

### Metrics

- baseline_latency_seconds: 5.207
- orchestrator_latency_seconds: 32.334
- baseline_total_tokens: 4939
- orchestrator_total_tokens: 19644
- baseline_citation_count: 5
- orchestrator_evidence_count: 9
- fact_check_status_counts: {'supported': 5}

## Question 14

Type: limitation/uncertainty

What limitations, uncertainties, or missing comparisons should be noted when interpreting REALM's reported results?

### Baseline Answer

When interpreting REALM's reported results, the following limitations, uncertainties, and missing comparisons should be noted:

*   **Missing Data in Experiments:** Certain data that could potentially benefit REALM was not used in the experiments conducted [1].
*   **Uncertainty in Retrieval Utility (RU) Interpretations:** A negative RU indicates that a document $z$ is less useful for predicting $y$ than a null document [2]. However, this could be due to several uncertain factors: the document $z$ may be irrelevant to $x$, the masked tokens in $x$ may not require world knowledge for prediction, or the necessary world knowledge may already be sufficiently commonplace and "baked into" the model's parameters [2].
*   **Optimization Constraints:** The results suggest that a "stale" MIPS index can negatively impact model training, and that further reducing this staleness might offer better optimization [4].
*   **Scope of Work:** The presented work is described as a "minimal instantiation" of a broader family of REALM-like approaches [5]. Future generalizations to structured knowledge, multi-lingual settings, and multi-modal settings have not yet been addressed [5].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-20-58cd33db77feaae8a3f8d036
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e
[5] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-15-e73576ceacc6e97a0666fd10

### Multi-Agent Answer

When interpreting REALM's reported results, the following limitations, uncertainties, and dependencies should be noted:

**Experimental and Data Limitations**
* The researchers acknowledged that certain data could have potentially benefited REALM, but this data was not used in their experiments [E1].
* While REALM achieves high performance, it retrieves significantly fewer documents (5 documents) compared to other retrieval-based systems, which typically retrieve between 20 and 80 documents [E1].

**Uncertainties in Retrieval Utility (RU)**
* A negative Retrieval Utility (RU) indicates that a retrieved document $z$ is less useful for predicting a target $y$ than a null document [E3].
* There is uncertainty regarding the cause of a negative RU, as it may stem from the document being irrelevant to the input $x$, the masked tokens in $x$ not requiring world knowledge to predict, or the necessary world knowledge being sufficiently commonplace that it is already embedded in the model's parameters [E3].

**Component Dependencies and Optimization**
* Optimal results for REALM require both the encoder and the retriever to act in unison, although both components benefit from training separately [E2].
* The use of a stale Maximum Inner Product Search (MIPS) index can negatively impact model training, suggesting that more frequent index refreshes may be necessary for better optimization [E2].

### Metrics

- baseline_latency_seconds: 6.249
- orchestrator_latency_seconds: 51.431
- baseline_total_tokens: 4628
- orchestrator_total_tokens: 34364
- baseline_citation_count: 5
- orchestrator_evidence_count: 11
- fact_check_status_counts: {'supported': 7}

## Question 15

Type: citation grounding / uncertainty

Which claims about REALM's performance or mechanism cannot be verified unless the answer cites specific experimental evidence from the paper?

### Baseline Answer

Based on the provided context, the following claims regarding REALM's performance or mechanism cannot be verified without citing specific experimental evidence (such as data from the mentioned Tables or Figures):

*   **The exact extent of performance improvement over ORQA:** While it is stated that the improvement of REALM over ORQA is "purely due to better pre-training methods" [1], the specific magnitude of this improvement requires Table 2 [1, 4].
*   **The efficacy of different masking schemes:** The claim that "salient span masking... is crucial for REALM" [4] and its impact relative to random token or span masking requires comparison with experimental results [4].
*   **The impact of MIPS index refresh rates:** The claim that a "stale index can hurt model training" and that further reducing staleness could improve optimization requires the results found in Table 2 [4].
*   **The specific benefit of the retriever vs. the encoder:** The claim that both components benefit from REALM training separately, but the "best result requires both components acting in unison," requires ablation results [4].
*   **The relationship between Retrieval Utility (RU) and performance:** The claim that RU "is more predictive of good performance on the downstream task of Open-QA than even the overall log-likelihood" requires reference to Figure 4 [3].
*   **The specific performance metrics for NaturalQuestions-Open:** Claims regarding how often the "gold answer appears in the top-5 retrievals" require Table 2 [1, 4].
*   **The effectiveness of REALM in retrieving updated knowledge:** The claim that a model pre-trained on a 2018 corpus can retrieve documents and generate correct tokens for information added in 2019 requires the example provided in Table 4 [3].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-20-58cd33db77feaae8a3f8d036

### Multi-Agent Answer

Based on the provided evidence, the following claims regarding REALM's performance and mechanisms are supported by specific experimental evidence or direct statements:

**Performance and Comparisons**
* REALM achieves the best overall performance compared to other retrieval-based systems while retrieving fewer documents [E2].
* While other retrieval-based systems typically retrieve between 20 to 80 documents, REALM retrieves only 5 [E2].
* The improvement of REALM over ORQA is attributed purely to better pre-training methods [E2].

**Mechanism and Training**
* The REALM pre-training method is applicable to both single-corpus settings (where X = Wikipedia and Z = Wikipedia) and separate-corpus settings (where X = CC-News and Z = Wikipedia) [E2].
* REALM's document index functions as a memory where keys are document embeddings [E3].
* The model's memories are "grounded" because each memory is associated with a specific document rather than unnamed value vectors [E3, E5].
* This grounding provides interpretability and provenance, which is considered crucial for Open-QA applications [E3, E5].
* Both the encoder and the retriever benefit separately from REALM training, though optimal results require both components to act in unison [E4].
* Salient span masking is identified as crucial for REALM, whereas it has not been shown to be impactful in standard BERT training [E4].
* Using a stale MIPS index can negatively impact model training, suggesting that frequent index refreshes are important for optimization [E4].
* A negative Retrieval Utility (RU) indicates that the retrieved document is less useful for predicting the target than a null document [E1].
* RU increases steadily throughout the pre-training process and is more predictive of performance on the Open-QA downstream task than the overall log-likelihood [E1].

### Metrics

- baseline_latency_seconds: 6.242
- orchestrator_latency_seconds: 52.268
- baseline_total_tokens: 4619
- orchestrator_total_tokens: 34426
- baseline_citation_count: 5
- orchestrator_evidence_count: 8
- fact_check_status_counts: {'supported': 10, 'unsupported': 2}
