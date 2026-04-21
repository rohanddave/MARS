# experiment14: retrieval sweep, all strong models, top_k=8

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

The model uses this external knowledge through a "retrieve-then-predict" generative process [3]:

1.  **Retrieve:** Given an input $x$, the model first uses a learned neural knowledge retriever to retrieve potentially helpful documents $z$ from the knowledge corpus $Z$, modeled as a sample from the distribution $p(z | x)$ [3].
2.  **Predict:** The model then conditions on both the original input $x$ and the retrieved documents $z$ to generate the output $y$, modeled as $p(y | z, x)$ [3].

By treating the retrieved document $z$ as a latent variable and marginalizing over all possible documents, the model learns to optimize the marginal likelihood $p(y | x) = \sum_{z \in Z} p(y | z, x) p(z | x)$ [3]. This allows the language model to attend over the retrieved documents to inform its predictions [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7

### Multi-Agent Answer

REALM retrieves documents from a large knowledge corpus, such as Wikipedia [E2, E3]. The model can be applied in a single-corpus setting where both the input and knowledge corpus are Wikipedia, or in a separate-corpus setting where the knowledge corpus is Wikipedia and the input source is different, such as CC-News [E4].

The model uses the retrieved information through a two-step "retrieve-then-predict" generative process [E1]:

*   **Retrieval:** The model first retrieves documents $z$ from a corpus $Z$ by modeling the distribution $p(z | x)$ [E1]. This is performed by a neural knowledge retriever based on a dense inner product model, which maps inputs and documents to $d$-dimensional vector embeddings [E1].
*   **Prediction:** The model then generates the output $y$ by conditioning on both the input and the retrieved documents, modeled as $p(y | z, x)$ [E1].

### Metrics

- baseline_latency_seconds: 7.655
- orchestrator_latency_seconds: 77.419
- baseline_total_tokens: 8663
- orchestrator_total_tokens: 54758
- baseline_citation_count: 8
- orchestrator_evidence_count: 12
- fact_check_status_counts: {'unsupported': 2, 'supported': 6}

## Question 2

Type: easy lookup

Which downstream tasks or benchmarks does the paper use to evaluate REALM?

### Baseline Answer

The paper uses the following Open-QA benchmarks to evaluate REALM:

*   **NQ (NaturalQuestions)** [6]
*   **WQ (WebQuestions)** [6]
*   **CT (ComplexType)** [6]

Additionally, the paper conducts ablation experiments specifically on the **NaturalQuestions-Open** dataset [1, 7].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[6] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-11-3fa55fc3148d1188cb70ab91
[7] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e

### Multi-Agent Answer

REALM is evaluated on three Open-domain Question Answering (Open-QA) benchmarks: Natural Questions, Web Questions, and Curated TREC [E5]. The model achieves new state-of-the-art results on these benchmarks, outperforming all previous systems by an absolute accuracy improvement of 4-16% [E5]. Additionally, the paper uses the NaturalQuestions-Open dataset to conduct ablation studies on critical components of REALM [E8].

### Metrics

- baseline_latency_seconds: 5.825
- orchestrator_latency_seconds: 36.600
- baseline_total_tokens: 8155
- orchestrator_total_tokens: 28851
- baseline_citation_count: 8
- orchestrator_evidence_count: 9
- fact_check_status_counts: {'supported': 3}

## Question 3

Type: definition

What is REALM, and what does the paper mean by retrieval-augmented language model pre-training?

### Baseline Answer

REALM (Retrieval-Augmented Language Model) is a framework designed to capture knowledge in a more modular and interpretable way by augmenting language model pre-training algorithms with a learned textual knowledge retriever [1, 2]. Unlike traditional models that store knowledge implicitly within their parameters, REALM explicitly exposes the role of world knowledge by requiring the model to decide what knowledge to retrieve and use during inference [1, 2]. Before making a prediction, the language model uses the retriever to select documents from a large corpus (such as Wikipedia) and attends over those documents to inform its prediction [1].

Retrieval-augmented language model pre-training refers to a process where:
*   **Augmentation:** Language model pre-training is augmented with a latent knowledge retriever [2].
*   **Unsupervised Learning:** The knowledge retriever is pre-trained in an unsupervised manner, using masked language modeling as the learning signal [2].
*   **Performance-based Signal:** The retriever is trained using a performance-based signal from unsupervised text; specifically, retrievals that improve the language model's perplexity are rewarded, while uninformative retrievals are penalized [1].
*   **End-to-end Optimization:** The model is learned end-to-end by backpropagating through a retrieval step that considers an entire corpus of textual knowledge [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2

### Multi-Agent Answer

REALM (Retrieval-Augmented Language Model) extends the retrieval-based approach to the paradigm of language model pre-training [E6]. The model's document index acts as a scalable, grounded neural memory where the keys are document embeddings [E8]. Because these memories are "grounded," each memory is associated with a specific document rather than unnamed value vectors, which provides interpretability and provenance [E7, E8].

In this paper, retrieval-augmented language model pre-training refers to a process that decomposes the generative process $p(y|x)$ into two distinct steps [E6]:

*   **Step 1:** Retrieving potentially helpful documents ($z$) from a knowledge corpus ($Z$) [E6].
*   **Step 2:** Predicting the output ($y$) conditioned on both the input ($x$) and the retrieved documents ($z$) [E6].

The REALM framework uses this "retrieve-then-predict" generative process for both fine-tuning (Open-QA) and pre-training (masked language modeling) [E6].

### Metrics

- baseline_latency_seconds: 7.497
- orchestrator_latency_seconds: 75.969
- baseline_total_tokens: 8909
- orchestrator_total_tokens: 52212
- baseline_citation_count: 8
- orchestrator_evidence_count: 14
- fact_check_status_counts: {'supported': 6, 'unsupported': 2}

## Question 4

Type: definition

How does REALM differ from a standard parametric language model such as BERT in where knowledge is stored and accessed?

### Baseline Answer

Standard parametric language models, such as BERT, store learned world knowledge implicitly in the parameters of the underlying neural network [1]. This implicit storage makes it difficult to determine what knowledge is stored and where, and the storage space is limited by the size of the network, requiring ever-larger networks to capture more facts [1].

In contrast, REALM differs in the following ways:

*   **Storage:** Instead of storing knowledge only in parameters, REALM augments pre-training with a learned textual knowledge retriever that accesses a large knowledge corpus, such as Wikipedia [1, 2]. The document index in REALM can be viewed as a "grounded" memory, where each memory is associated with a specific document rather than unnamed value vectors [3].
*   **Access:** Before making a prediction, the REALM model uses its retriever to retrieve documents from the knowledge corpus and then attends over those documents to help inform its prediction [2]. This process allows the model to decide what knowledge to retrieve and use during inference [2].

### Multi-Agent Answer

Standard parametric language model pre-training stores world knowledge implicitly within the neural network parameters [E3]. This method requires increasingly larger networks to cover more facts [E3].

In contrast, the REALM (Retrieval-Augmented Language Model) framework augments language model pre-training with a learned textual knowledge retriever to capture knowledge in a more modular and interpretable way [E2, E3]. Instead of relying solely on internal parameters, REALM explicitly exposes the role of world knowledge by asking the model to decide what knowledge to retrieve and use during inference [E2]. Specifically, the model uses the retriever to pull documents from a large corpus, such as Wikipedia, and then attends over those documents to help inform its prediction [E2]. This approach allows REALM to generalize language modeling to the scope of an entire text corpus [E8].

### Metrics

- baseline_latency_seconds: 3.312
- orchestrator_latency_seconds: 73.052
- baseline_total_tokens: 7991
- orchestrator_total_tokens: 53625
- baseline_citation_count: 8
- orchestrator_evidence_count: 16
- fact_check_status_counts: {'supported': 5, 'unsupported': 1}

## Question 5

Type: method/mechanism

How does REALM's retrieve-then-predict framework work, including the role of the latent document variable z?

### Baseline Answer

REALM's retrieve-then-predict framework is a generative process that decomposes the probability of an output $y$ given an input $x$, denoted as $p(y|x)$, into two distinct steps [3]:

1.  **Retrieve**: The model first retrieves potentially helpful documents $z$ from a knowledge corpus $Z$ [3]. This step is modeled as sampling from the distribution $p(z|x)$ [3].
2.  **Predict**: The model then conditions on both the retrieved document $z$ and the original input $x$ to generate the output $y$, modeled as $p(y|z, x)$ [3].

The framework treats the retrieved document $z$ as a **latent variable** [3]. To obtain the overall likelihood of generating $y$, the model marginalizes over all possible documents $z$ in the corpus $Z$ using the following equation:
$$p(y |x) = \sum_{z \in Z} p(y |z, x) p(z |x)$$ [3]

The framework consists of two key components: a **neural knowledge retriever**, which models $p(z|x)$, and a **knowledge-augmented encoder**, which models $p(y|z, x)$ [3].

Citations:
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7

### Multi-Agent Answer

The REALM (Retrieval-Augmented Language Model) framework decomposes the process of learning a distribution $p(y | x)$ into a two-step generative process [E4]. First, the model retrieves helpful documents $z$ from a knowledge corpus $Z$, which is modeled as $p(z | x)$ [E4]. Second, the model conditions on both the input $x$ and the retrieved document $z$ to generate the output $y$, modeled as $p(y | z, x)$ [E4].

In this framework, the latent document variable $z$ represents the retrieved knowledge used to inform predictions [E1][E2]. The model utilizes a neural knowledge retriever to pull documents from a large corpus, such as Wikipedia, and then attends over those documents to help inform its prediction [E1][E2]. To optimize this process, REALM models the retrieve-then-predict process as a latent variable language model and optimizes the marginal likelihood [E1].

### Metrics

- baseline_latency_seconds: 5.262
- orchestrator_latency_seconds: 46.975
- baseline_total_tokens: 7897
- orchestrator_total_tokens: 33320
- baseline_citation_count: 8
- orchestrator_evidence_count: 12
- fact_check_status_counts: {'supported': 9}

## Question 6

Type: method/mechanism

How does the paper train the retriever when the retrieved document is latent, and how does learning signal flow back to retrieval?

### Baseline Answer

The paper trains the retriever by modeling the retrieve-then-predict approach as a latent variable language model and optimizing the marginal likelihood [1]. Specifically, the overall likelihood of generating an output $y$ given an input $x$ is obtained by treating the retrieved document $z$ as a latent variable and marginalizing over all possible documents $z$ in the corpus $Z$:

$$p(y |x) = \sum_{z \in Z} p(y |z, x) p(z |x)$$ [4]

The learning signal flows back to the retriever through the gradient of the pre-training objective (a log-likelihood) with respect to the retriever's parameters $\theta$ [6]. This gradient can be expressed as:

$$\nabla \log p (y |x) = \sum_{z} [p(z |y, x) - p(z |x)] \nabla \log p(z |x)$$ [6]

This indicates that the retriever is rewarded when it selects a document that improves the language model's perplexity and penalized when it provides uninformative retrieval [1]. If a single "gold" document $z^*$ exists that allows for perfect prediction accuracy, the gradient descent on the REALM objective becomes equivalent to gradient descent on $\log p(z^* |x)$, which is the standard maximum likelihood training objective used in supervised learning [6].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7
[6] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-19-a8290af7e1b5f4bf2a71d9c0

### Multi-Agent Answer

The REALM framework models the "retrieve-then-predict" method as a latent variable language model [E1]. In this approach, the likelihood of generating an output $y$ given an input $x$ is calculated by treating the retrieved document $z$ as a latent variable and marginalizing over all possible documents $z$ in the knowledge corpus $Z$ using the formula $p(y | x) = \sum_{z \in Z} p(y | z, x) p(z | x)$ [E5].

The retriever is trained using a performance-based signal from unsupervised text [E1]. Specifically, the training process rewards retrievals that improve the language model's perplexity and penalizes uninformative retrievals [E1]. This training can be performed in an unsupervised manner by using masked language modeling as the learning signal [E2]. Learning the model end-to-end requires backpropagating through a retrieval step that considers an entire corpus of textual knowledge [E1, E2].

### Metrics

- baseline_latency_seconds: 6.806
- orchestrator_latency_seconds: 75.703
- baseline_total_tokens: 7900
- orchestrator_total_tokens: 53889
- baseline_citation_count: 8
- orchestrator_evidence_count: 10
- fact_check_status_counts: {'supported': 5, 'unsupported': 1}

## Question 7

Type: method/mechanism / implementation

What approximations or engineering choices does REALM use to make retrieval over a large corpus practical during training and inference?

### Baseline Answer

To make retrieval over a large corpus practical during training and inference, REALM uses the following engineering choices and approximations:

*   **MIPS Formulation:** The selection of the best documents is formulated as a Maximum Inner Product Search (MIPS) [2].
*   **Caching and Asynchronous Updates:** The retriever is structured so that the computation performed for each individual document can be cached and updated asynchronously [2].
*   **Parallelized Indexing:** During pre-training, the document embedding step for the MIPS index is parallelized over 16 TPUs [4].
*   **Index Refresh Rate:** To manage the large-scale retrieval during pre-training, a parallel process is run to re-embed corpus documents and rebuild the MIPS index, resulting in one index refresh approximately every 500 training steps [5].
*   **Candidate Marginalization:** During pre-training, the model retrieves and marginalizes over 8 candidate documents, including a null document [4]. During fine-tuning inference, the model considers the top-5 candidates [4].

Citations:
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-11-3fa55fc3148d1188cb70ab91
[5] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e

### Multi-Agent Answer

To make retrieval over a large corpus practical, REALM employs several engineering choices and approximations:

*   **Document Selection Formulation:** To manage the computational challenge of evaluating millions of candidate documents, document selection is formulated as a Maximum Inner Product Search (MIPS) [E1].
*   **Caching and Asynchrony:** The retriever is structured such that the computation for each individual document can be cached and updated asynchronously [E1].
*   **Dense Inner Product Model:** The neural knowledge retriever utilizes a dense inner product model, where the relevance score is determined by the inner product of $d$-dimensional vector embeddings [E4].
*   **Parallelization:** During the document embedding step, the process is parallelized over 16 TPUs [E3].
*   **Inference Approximation:** Although the retrieval step can consider millions of documents, the model only considers the top-5 candidates during fine-tuning inference [E3].

### Metrics

- baseline_latency_seconds: 5.488
- orchestrator_latency_seconds: 41.026
- baseline_total_tokens: 8614
- orchestrator_total_tokens: 31639
- baseline_citation_count: 8
- orchestrator_evidence_count: 13
- fact_check_status_counts: {'supported': 5}

## Question 8

Type: comparison

How does REALM compare with ORQA or other open-domain QA baselines, and what evidence supports that comparison?

### Baseline Answer

REALM compares to ORQA and other open-domain QA baselines as follows:

**Comparison with ORQA**
*   **Direct Comparison:** ORQA is the most direct comparison to REALM because the fine-tuning setup, hyperparameters, and training data are identical [1]. Both systems' retrievers are also initialized using the Inverse Cloze Task (ICT) [2].
*   **Key Differences:** While ORQA formulates Open-QA using a similar latent variable model and maximizes marginal likelihood, REALM adds a novel language model pre-training step and backpropagates into the MIPS index instead of using a fixed index [7]. 
*   **Performance:** The improvement of REALM over ORQA is attributed purely to better pre-training methods [1]. Resetting both the retriever and encoder to their baseline states reduces the system to the ORQA baseline [5].

**Comparison with Other Baselines**
*   **Retrieval-based Systems:** Compared to other retrieval-based systems (such as DrQA, HardEM, GraphRetriever, and PathRetriever), which often retrieve between 20 to 80 documents, REALM achieves the overall best performance while only retrieving 5 documents [1, 7].
*   **Generation-based Systems:** REALM compares against competitive generation-based baselines, specifically concurrent work that fine-tunes T5 for Open-QA (including Base, Large, and an 11-billion parameter model) [2].

**Supporting Evidence**
*   REALM achieves new state-of-the-art results across three benchmarks, outperforming all previous systems by 4-16% in absolute accuracy [8].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-10-8ea61faa3a17c1fc8f8725d8
[5] source: data/2002.08909v1.pdf, chunk_id: 2

### Multi-Agent Answer

REALM achieves new state-of-the-art results on three Open-domain Question Answering (Open-QA) benchmarks, outperforming all previous systems by 4-16% absolute accuracy [E3, E4]. Among the retrieval-based systems compared, REALM achieves the best overall performance while retrieving significantly fewer documents than other systems [E1]. While other retrieval-based systems typically retrieve between 20 and 80 documents, REALM achieves its best performance by retrieving only 5 documents [E1].

In comparisons to specific baselines:

* **ORQA:** ORQA is the most direct comparison to REALM because the fine-tuning setup, hyperparameters, and training data are identical [E1]. Both REALM and ORQA initialize their retrievers using the Inverse Cloze Task [E2, E5]. However, REALM differs from ORQA by backpropagating into the MIPS index rather than using a fixed index [E2, E5]. The improvement seen in REALM over ORQA is attributed purely to superior pre-training methods [E1].

### Metrics

- baseline_latency_seconds: 6.401
- orchestrator_latency_seconds: 78.820
- baseline_total_tokens: 7685
- orchestrator_total_tokens: 51743
- baseline_citation_count: 8
- orchestrator_evidence_count: 13
- fact_check_status_counts: {'supported': 4, 'unsupported': 5}

## Question 9

Type: comparison

How does REALM's retrieval-based approach compare with storing knowledge only in model parameters?

### Baseline Answer

Compared to models that store knowledge implicitly in their parameters, REALM's retrieval-based approach offers several distinctions:

*   **Interpretability and Modularity:** REALM captures knowledge in a more modular and interpretable way [1, 3]. Because its "memories" are grounded—meaning each memory is associated with a specific document rather than unnamed value vectors—it provides a level of interpretability that is crucial for applications like Open-domain Question Answering (Open-QA), where users require provenance for an answer to be considered trustworthy [6].
*   **Explicit Role of Knowledge:** Unlike models that store knowledge in parameters, REALM's approach explicitly exposes the role of world knowledge by requiring the model to decide what knowledge to retrieve and use during inference [1].
*   **Scalability of Knowledge:** In models where knowledge is stored implicitly in parameters, the storage space is limited by the size of the network; capturing more knowledge requires training increasingly larger networks, which can be prohibitively expensive or slow [3].
*   **Adaptability:** REALM is able to adapt to an updated knowledge corpus [8]. For example, a model pre-trained on a 2018 corpus can successfully retrieve a document and generate a correct token from a 2020 corpus containing information that was not previously available [8].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952, chunk_index: 1
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2, chunk_index: 0
[6] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-14-83fbe5c3ec4e1ed386558b56, chunk_index: 14
[8] source: data/2002.0

### Multi-Agent Answer

In contrast to models that store knowledge within their parameters, REALM's retrieval-based approach explicitly exposes the role of world knowledge by requiring the model to decide what knowledge to retrieve and use during inference [E2]. This approach allows the model to function by using a learned textual retriever to pull documents from a large corpus and then attending over those documents to inform its prediction [E2].

The retrieval-based approach offers several qualitative advantages:

*   **Interpretability and Provenance:** REALM's memories are "grounded," meaning each memory is associated with a specific document rather than unnamed value vectors [E6, E7]. This grounding provides a level of interpretability and provenance that is crucial for Open-QA applications, as users require a source to ensure predicted answers are trustworthy [E6, E7].
*   **Scope and Generalization:** REALM generalizes previous modeling work—which typically conditioned on words, sentences, or paragraphs—by extending the scope of context to an entire text corpus [E7]. This is significant because Open-QA models must retain knowledge from millions of documents, as a question could pertain to any of them [E5].

### Metrics

- baseline_latency_seconds: 7.032
- orchestrator_latency_seconds: 76.114
- baseline_total_tokens: 7854
- orchestrator_total_tokens: 49894
- baseline_citation_count: 8
- orchestrator_evidence_count: 14
- fact_check_status_counts: {'supported': 3, 'unsupported': 2}

## Question 10

Type: evidence synthesis / ablation

What ablation or diagnostic evidence shows that retrieval pre-training improves REALM rather than only the reader component?

### Baseline Answer

To determine whether REALM pre-training improves the retriever, the encoder, or both, researchers performed an ablation study by resetting the parameters of either the retriever or the encoder to their baseline state before fine-tuning [4].

The following diagnostic and ablation evidence was found:

*   **Component Analysis:** Resetting both the retriever and the encoder reduces the system to the ORQA baseline [4]. The study found that while both the encoder and retriever benefit from REALM training separately, the best results are achieved when both components act in unison [4].
*   **Retrieval Metric:** To more significantly isolate the contribution of improving the retriever during pre-training, the researchers reported how often the gold answer appears in the top-5 retrievals before applying any fine-tuning [1, 4].
*   **Ablation Results (NaturalQuestions-Open):** In ablation experiments, the "Baseline retriever + REALM encoder" configuration yielded an Exact Match score of 35.3 and a Zero-shot Retrieval Recall@5 of 13.9, whereas the full "REALM" system achieved a higher Exact Match of 38.2 and a Recall@5 of 38.5 [8].
*   **Comparison to ORQA:** The improvement of REALM over ORQA (which shares an identical fine-tuning setup, hyperparameters, and training data) is attributed purely to better pre-training methods [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e
[8] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-11-3fa55fc3148d1188cb70ab91

### Multi-Agent Answer

To demonstrate that retrieval pre-training improves the REALM model rather than just the reader component, several diagnostic and ablation methods are used:

* **Comparison with ORQA:** REALM's improvement over ORQA is attributed purely to better pre-training methods [E2]. This comparison is considered direct because the fine-tuning setup, hyperparameters, and training data are identical for both systems [E2].
* **Isolation of Retriever Contribution:** The contribution of improving the retriever during pre-training is more significantly isolated by measuring how frequently the gold answer appears in the top-5 retrievals before any fine-tuning is applied [E1].
* **Ablation of Components:** The individual contributions of the encoder and the retriever can be tested by resetting the parameters of either component to its baseline state before REALM pre-training [E1]. While both the encoder and the retriever benefit from REALM training separately, optimal results are achieved when both components act in unison [E1].

### Metrics

- baseline_latency_seconds: 6.718
- orchestrator_latency_seconds: 38.970
- baseline_total_tokens: 7999
- orchestrator_total_tokens: 29975
- baseline_citation_count: 8
- orchestrator_evidence_count: 14
- fact_check_status_counts: {'supported': 5}

## Question 11

Type: evidence synthesis

Synthesize the evidence for why REALM improves open-domain QA performance, including retrieval quality, pre-training, and downstream fine-tuning.

### Baseline Answer

REALM improves open-domain question answering (Open-QA) performance through the following mechanisms:

*   **Pre-training:** The improvement of REALM over the direct comparison model, ORQA, is attributed purely to better pre-training methods [1]. REALM utilizes a masked language modeling (MLM) task as an unsupervised learning signal during pre-training [4, 5]. This pre-training process optimizes a latent variable language model by marginalizing over possible documents, which rewards retrievals that improve the language model's perplexity [5]. This method can be applied to both single-corpus (e.g., Wikipedia) and separate-corpus (e.g., CC-News and Wikipedia) settings [1].
*   **Retrieval Quality:** REALM uses a learned neural knowledge retriever that is trained end-to-end by backpropagating through a retrieval step that considers millions of documents [4]. This pre-training significantly improves the retriever; ablation studies show that improving the retriever during pre-training specifically isolates its contribution to performance [1]. Furthermore, REALM's retriever is designed to transfer to other tasks because it retrieves raw text rather than labeled examples [5]. While other retrieval-based systems often require retrieving 20 to 80 documents, REALM achieves the overall best performance while only retrieving 5 documents [1].
*   **Downstream Fine-tuning:** REALM is fine-tuned on the Open-QA task, where it learns to predict an answer $y$ given a question $x$ by first retrieving documents $z$ from a knowledge corpus $Z$ [2]. It outperforms all previous methods on three popular Open-QA benchmarks (NaturalQuestions-Open, Web Questions, and Curated TREC) by a margin of 4-16% in absolute accuracy [4, 5]. Notably, REALM outperforms the largest T5-11B model while being 30 times smaller [4].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1

### Multi-Agent Answer

REALM improves open-domain question answering (Open-QA) performance by utilizing a "retrieve-then-predict" architecture that employs a specialized pre-training approach and an enhanced retrieval mechanism [E2].

**Pre-training and Learning Signal**
The primary driver for REALM's improvement over systems such as ORQA is its superior pre-training method [E1]. While traditional language models store world knowledge implicitly in neural network parameters—necessitating increasingly large networks to cover more facts—REALM uses a latent knowledge retriever to capture knowledge in a more modular and interpretable way [E5, E6]. During pre-training, the retriever is trained in an unsupervised manner using masked language modeling (MLM) as the learning signal [E2, E6]. This training is guided by a performance-based signal where retrievals that improve the language model’s perplexity are rewarded, while uninformative retrievals are penalized [E5]. Furthermore, unlike previous retrieve-and-edit frameworks that rely on high lexical overlap, REALM learns which texts are most useful for reducing perplexity, allowing it to utilize information beyond simple lexical overlap [E8].

**Retrieval Quality**
REALM utilizes a neural knowledge retriever based on a dense inner product model [E2]. This retriever maps inputs and documents to $d$-dimensional vectors to calculate relevance scores [E2]. This approach allows REALM to achieve its best performance while retrieving significantly fewer documents than other retrieval-based systems; specifically, REALM retrieves approximately 5 documents, whereas other systems typically retrieve between 20 and 80 documents [E1].

**Downstream Fine-tuning**
For the fine-tuning stage, the model's task shifts from masked language modeling to Open-QA, where it predicts an answer $y$ given a question $x$ [E2]. During fine-tuning inference, the system considers the top-5 candidates [E7]. REALM's pre-training method is versatile and can be applied to both single-corpus settings (where the input and knowledge corpus are both Wikipedia) and separate-corpus settings (such as using CC-News as input and Wikipedia as the knowledge corpus) [E1].

### Metrics

- baseline_latency_seconds: 6.478
- orchestrator_latency_seconds: 88.094
- baseline_total_tokens: 8205
- orchestrator_total_tokens: 57279
- baseline_citation_count: 8
- orchestrator_evidence_count: 12
- fact_check_status_counts: {'supported': 10, 'unsupported': 2}

## Question 12

Type: multi-step reasoning

Explain step by step how a masked-language-model pre-training objective can improve downstream open-domain QA in REALM.

### Baseline Answer

In REALM, a masked-language-model (MLM) pre-training objective improves downstream open-domain question answering (Open-QA) through the following process:

1.  **Unsupervised Pre-training with MLM:** During pre-training, the model is given an unlabeled text corpus $\mathcal{X}$ [1]. The MLM task is performed by randomly masking tokens in a sampled piece of text and requiring the model to predict those missing tokens [1].
2.  **Learning Representations and World Knowledge:** To successfully predict the masked tokens, the model must learn to encode syntactic and semantic information as well as world knowledge [1]. 
3.  **Integration with a Latent Knowledge Retriever:** REALM augments the MLM pre-training with a learned textual knowledge retriever [2]. Instead of relying solely on implicit knowledge stored in neural network parameters, the model is trained to decide what knowledge to retrieve from a large corpus (such as Wikipedia) and use during its predictions [2, 5].
4.  **End-to-End Training via Backpropagation:** The MLM objective serves as a learning signal that is backpropagated all the way through the retrieval step [2]. This rewards the retriever when it selects documents that improve the language model's performance (e.g., helping it fill in a blank) and penalizes it for uninformative retrievals [5].
5.  **Transfer to Downstream Open-QA:** Because the retriever is trained to fetch text that aids language modeling rather than just labeled examples, it is designed to transfer to other tasks [5]. For the downstream Open-QA task, the model is fine-tuned to take a question $x$ and predict an answer $y$ by first retrieving relevant documents $z$ from a knowledge corpus $\mathcal{Z}$ and then attending over those documents to inform its prediction [2, 3, 5].

Citations:
[1] data/2002.08909v1.pdf, chunk_id: 2002.08909v1-2-7f240c64641ad3f52fc62e97
[2] data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc

### Multi-Agent Answer

The masked-language-model (MLM) pre-training objective improves downstream open-domain question answering (Open-QA) in REALM through the following process:

**1. Learning Representations from Unlabeled Text**
The model undergoes pre-training on unlabeled text corpora using an MLM objective [E1]. In this variant, the model is trained to predict the original value of missing (masked) tokens within an input text passage [E1][E4]. This process requires the model to learn syntactic information, semantic information, and world knowledge [E1]. Pre-training in this manner often leads to better generalization on downstream tasks, such as Open-QA, than training the model from scratch [E1].

**2. Unsupervised Training of the Knowledge Retriever**
REALM uses the MLM task as a learning signal to perform unsupervised pre-training of a latent knowledge retriever [E2]. The retriever is trained using a performance-based signal from unsupervised text, where retrievals that improve the language model’s perplexity are rewarded, while uninformative retrievals are penalized [E3].

**3. Capturing Modular and Interpretable Knowledge**
While standard language model pre-training captures world knowledge implicitly within neural network parameters, REALM augments this process with a retriever to capture knowledge in a more modular and interpretable way [E2]. This allows the model to retrieve and attend over documents from a large corpus, such as Wikipedia, during pre-training, fine-tuning, and inference [E2]. By deciding what to retrieve and use during inference, the model explicitly exposes the role of world knowledge [E3].

### Metrics

- baseline_latency_seconds: 6.466
- orchestrator_latency_seconds: 84.691
- baseline_total_tokens: 9087
- orchestrator_total_tokens: 57928
- baseline_citation_count: 8
- orchestrator_evidence_count: 14
- fact_check_status_counts: {'unsupported': 3, 'supported': 9}

## Question 13

Type: multi-step reasoning / error analysis

If REALM retrieves an irrelevant document, how would that affect p(z|x), p(y|z,x), and the final answer prediction?

### Baseline Answer

If REALM retrieves an irrelevant document $z$, the effects are as follows:

*   **$p(z|x)$**: The context states that the retriever models the distribution of potentially helpful documents $z$ given an input $x$ [3]. If a document is irrelevant, it would not be a "helpful" document, though the provided text does not explicitly state how the probability value of $p(z|x)$ changes specifically for an irrelevant document, other than noting that the retriever is trained to reward helpful retrievals and penalize uninformative ones [4].
*   **$p(y|z,x)$**: A negative Retrieval Utility (RU) indicates that $z$ is less useful for predicting $y$ than a null document $\emptyset$ [1]. A negative RU is one way to show that $z$ is irrelevant to $x$ [1].
*   **Final answer prediction ($p(y|x)$)**: The final prediction $p(y|x)$ is obtained by marginalizing over all possible documents $z$, using the formula $p(y|x) = \sum_{z \in Z} p(y|z, x) p(z|x)$ [3]. In the provided example of a correct prediction, the marginalized probability of the correct answer "dramatically increases" because the model manages to retrieve documents with a related fact [2]. Conversely, if the retrieved documents are uninformative, they do not provide the necessary world knowledge to improve the prediction [4].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-20-58cd33db77feaae8a3f8d036, chunk_index: 20
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e, chunk_index: 13
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e

### Multi-Agent Answer

If a retrieved document $z$ is irrelevant, its impact on the components of the REALM model is characterized as follows:

**Retrieval Utility (RU) and $p(y|z, x)$**
An irrelevant document $z$ results in a negative Retrieval Utility (RU), which is mathematically defined as $\log p(y |z, x) - \log p(y |\emptyset, x) < 0$ [E1, E8]. This negative value indicates that the document $z$ is less useful for predicting the target $y$ than a null document $\emptyset$ [E1, E8]. This lack of utility may suggest that $z$ is irrelevant to $x$, that the masked tokens in $x$ do not require world knowledge, or that the necessary knowledge is already baked into the model's parameters [E1, E8].

**$p(z|x)$ and Final Answer Prediction**
The provided evidence does not contain a specific formula or a direct description of how the irrelevance of $z$ itself impacts the probability $p(z|x)$ [No evidence]. However, the notes do indicate that "too informative" or trivial retrieval candidates result in a large positive gradient for $p(z|x)$ [E6]. The evidence is insufficient to determine how an irrelevant document specifically affects the final answer prediction, other than the fact that RU (which measures the usefulness of $z$ for predicting $y$) is a more predictive indicator of high performance on Open-QA downstream tasks than overall log-likelihood [E1].

### Metrics

- baseline_latency_seconds: 6.503
- orchestrator_latency_seconds: 83.675
- baseline_total_tokens: 8309
- orchestrator_total_tokens: 50269
- baseline_citation_count: 8
- orchestrator_evidence_count: 13
- fact_check_status_counts: {'unsupported': 5, 'supported': 1}

## Question 14

Type: limitation/uncertainty

What limitations, uncertainties, or missing comparisons should be noted when interpreting REALM's reported results?

### Baseline Answer

When interpreting REALM's reported results, the following limitations, uncertainties, and missing comparisons should be noted:

*   **Uncertainties in Retrieval Utility (RU):** A negative RU indicates that the retrieved document $z$ is less useful for predicting $y$ than a null document [2]. However, this result is uncertain because it could mean the document is irrelevant to $x$, or it could mean the masked tokens in $x$ do not require world knowledge, or that the required knowledge is already sufficiently "baked into" the model's parameters [2].
*   **Impact of Index Staleness:** The results suggest that a "stale index" can negatively impact model training, and that further reducing this staleness might offer better optimization [4].
*   **Missing Data in Experiments:** Certain data that could potentially benefit REALM was not used in the experiments conducted [1].
*   **Comparison Contexts:** While REALM is compared to ORQA (where hyperparameters, fine-tuning setup, and training data are identical), it is also compared against other retrieval-based systems that often retrieve 20 to 80 documents, whereas REALM achieves its performance while only retrieving 5 documents [1]. For generation-based models, the text notes that while T5 is a viable approach, previous T5 experiments only focused on reading comprehension tasks where a context document is provided [6].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-20-58cd33db77feaae8a3f8d036
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e
[6] source: data/2002.08909v1.pdf, chunk_id

### Multi-Agent Answer

When interpreting REALM's reported results, several limitations, uncertainties, and missing comparisons should be noted:

**Data and Experimental Constraints**
*   The improvement of REALM over ORQA is attributed purely to superior pre-training methods, as the fine-tuning setup, hyperparameters, and training data are identical between the two systems [E1, E6].
*   Certain data that could have potentially benefited REALM was not used in the presented experiments [E1].
*   While REALM is compared to T5, T5's experiments were limited to reading comprehension tasks that utilized provided context documents [E5], whereas Open-QA models generally must retain knowledge from millions of documents [E4].
*   T5's performance was also aided by accessing additional reading comprehension data from SQuAD during pre-training, a resource that was not used in REALM experiments [E6].

**Knowledge and Parameter Uncertainties**
*   Although REALM can adapt to updated knowledge corpora, the knowledge-augmented encoder may still retain old world knowledge, which can potentially lead to outdated predictions [E7].
*   A negative Retrieval Utility (RU) indicates that a document is less useful for predicting an output than a null document [E7, E8]. This uncertainty may arise because the document is irrelevant to the input, the masked tokens do not require world knowledge, or the necessary knowledge is already "baked into the model's parameters" or is "sufficiently commonplace" [E8].

### Metrics

- baseline_latency_seconds: 6.287
- orchestrator_latency_seconds: 76.882
- baseline_total_tokens: 7497
- orchestrator_total_tokens: 54737
- baseline_citation_count: 8
- orchestrator_evidence_count: 13
- fact_check_status_counts: {'unsupported': 3, 'supported': 3}

## Question 15

Type: citation grounding / uncertainty

Which claims about REALM's performance or mechanism cannot be verified unless the answer cites specific experimental evidence from the paper?

### Baseline Answer

Based on the provided context, the following claims regarding REALM's performance or mechanism require specific experimental evidence from the paper to be verified:

*   **Performance comparisons:** The claim that REALM outperforms all previous methods by a significant margin (4-16% absolute accuracy) on three popular Open-QA benchmarks (NaturalQuestions-Open, Web Questions, and Curated TREC) [1, 7].
*   **Comparison with ORQA:** The claim that the improvement of REALM over ORQA is due purely to better pre-training methods, given that the fine-tuning setup, hyperparameters, and training data are identical [1].
*   **Efficiency in retrieval:** The claim that REALM achieves the overall best performance while only retrieving 5 documents, compared to other retrieval-based systems that often retrieve between 20 and 80 documents [1].
*   **Component contribution:** The claim that both the encoder and retriever benefit from REALM training separately, but that the best results require both components to act in unison [4].
*   **Effect of index staleness:** The claim that a stale MIPS index can hurt model training, as suggested by results in Table 2 [4].
*   **Masking scheme impact:** The claim that salient span masking is crucial for REALM, even though it has not been shown to be impactful in previous work with standard BERT training [4].
*   **Retrieval Utility (RU) effectiveness:** The claim that RU is more predictive of good performance on the downstream Open-QA task than the overall log-likelihood [3].
*   **Knowledge adaptation:** The claim that a REALM model pre-trained on a 2018 corpus is able to retrieve documents in an updated 2020 corpus and generate the correct token [3].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-20-58cd33db77feaae8a3f8d036
[4] source

### Multi-Agent Answer

Based on the provided evidence, the following claims regarding REALM's performance or mechanism cannot be fully verified because the specific experimental data is missing from the notes:

*   **Benchmark-Specific Accuracy:** While it is stated that REALM outperforms previous methods by a margin of 4–16% absolute accuracy across three benchmarks—Natural Questions-Open, Web Questions, and Curated TREC [E2, E3]—the notes do not provide the specific individual accuracy scores or a detailed experimental breakdown for each of these specific benchmarks [E2, E3].
*   **Impact of Retrieval Volume:** The notes indicate that REALM achieves its best overall performance by retrieving only 5 documents [E1], whereas other retrieval-based systems typically retrieve between 20 and 80 documents [E1]. However, the evidence does not include comparative performance data or experimental results showing how REALM's performance would change if a different number of documents were retrieved [E1].
*   **Model Scale Performance:** The study compares REALM against Base, Large, and 11-billion parameter models to measure the effects of model size [E7]. However, the specific experimental results, performance metrics, or accuracy scores associated with each of these particular model scales are not provided in the notes [E7].

### Metrics

- baseline_latency_seconds: 6.301
- orchestrator_latency_seconds: 66.985
- baseline_total_tokens: 7930
- orchestrator_total_tokens: 53802
- baseline_citation_count: 8
- orchestrator_evidence_count: 10
- fact_check_status_counts: {'unsupported': 1, 'supported': 4}
