# experiment22: retrieval sweep, strong fact checker only, top_k=8

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

REALM retrieves from a large textual knowledge corpus, such as Wikipedia [1, 2]. This corpus is used during the pre-training, fine-tuning, and inference stages of the model [2].

The model uses this external knowledge through a "retrieve-then-predict" process [3]:
1.  **Retrieve:** Given an input $x$, the model first uses a learned neural knowledge retriever to retrieve potentially helpful documents $z$ from the knowledge corpus $Z$ [2, 3]. This is modeled as a sample from the distribution $p(z | x)$ [3].
2.  **Predict:** The model then conditions on both the original input $x$ and the retrieved documents $z$ to generate the output $y$, modeled as $p(y | z, x)$ [3].

By treating the retrieved document $z$ as a latent variable and marginalizing over all possible documents, the model achieves an overall likelihood of $p(y | x) = \sum_{z \in Z} p(y | z, x) p(z | x)$ [3].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7

### Multi-Agent Answer

REALM retrieves information from a large knowledge corpus, such as Wikipedia [E2, E3]. The model can be configured for single-corpus settings, where both the input and knowledge source are Wikipedia, or separate-corpus settings, such as using CC-News as the input and Wikipedia as the knowledge source [E4]. In these contexts, the term "document" is used loosely to refer to a passage from the knowledge corpus rather than a complete article [E1].

The model uses this retrieved information through a "retrieve, then predict" process [E1]. This approach decomposes the process of learning a distribution $p(y|x)$ into two steps [E1]:

*   **Retrieve:** A learned textual knowledge retriever models the selection of relevant documents or passages from the corpus [E1]. The retriever uses a dense inner product model to calculate relevance scores by mapping inputs and documents to $d$-dimensional vectors [E1]. 
*   **Predict:** The model then predicts an answer based on the retrieved information [E1]. The generative process treats the retrieved document $z$ as a latent variable, modeled as $p(y|x) = \sum_{z \in Z} p(y|z, x) p(z|x)$ [E1]. During this stage, the language model attends over the retrieved documents to inform its predictions [E2, E3].

### Metrics

- baseline_latency_seconds: 9.755
- orchestrator_latency_seconds: 83.617
- baseline_total_tokens: 8674
- orchestrator_total_tokens: 55174
- baseline_citation_count: 8
- orchestrator_evidence_count: 10
- fact_check_status_counts: {'unsupported': 1, 'supported': 7}

## Question 2

Type: easy lookup

Which downstream tasks or benchmarks does the paper use to evaluate REALM?

### Baseline Answer

To evaluate REALM, the paper uses the following Open-QA benchmarks:

*   **NQ** (NaturalQuestions) [6]
*   **WQ** (WebQuestions) [6]
*   **CT** (Complex Type) [6]

Additionally, the paper presents ablation experiments specifically for the **NaturalQuestions-Open** (NQ-Open) dataset [1, 7].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[6] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-11-3fa55fc3148d1188cb70ab91
[7] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e

### Multi-Agent Answer

REALM is evaluated using three Open-domain Question Answering (Open-QA) benchmarks [E5]. These benchmarks are:

*   **Natural Questions (NQ)** [E5, E7]
*   **Web Questions (WQ)** [E5, E7]
*   **Curated TREC (CT)** [E5, E7]

### Metrics

- baseline_latency_seconds: 7.885
- orchestrator_latency_seconds: 76.960
- baseline_total_tokens: 8164
- orchestrator_total_tokens: 53116
- baseline_citation_count: 8
- orchestrator_evidence_count: 11
- fact_check_status_counts: {'supported': 1, 'unsupported': 1}

## Question 3

Type: definition

What is REALM, and what does the paper mean by retrieval-augmented language model pre-training?

### Baseline Answer

REALM (Retrieval-Augmented Language Model) is a novel framework designed to capture knowledge in a more modular and interpretable way [1, 2]. Unlike traditional models that store world knowledge implicitly in their parameters [2], REALM augments language model pre-training algorithms with a learned textual knowledge retriever [1, 2]. This allows the model to explicitly decide what knowledge to retrieve from a large corpus (such as Wikipedia) and attend over those documents to inform its predictions during both pre-training and inference [1, 2].

In the context of this paper, **retrieval-augmented language model pre-training** refers to a process where:
*   The language model pre-training is augmented with a latent knowledge retriever [2].
*   The pre-training task is modeled as a "retrieve-then-predict" generative process [3]. For pre-training, this specifically involves a masked language modeling (MLM) task where the model must predict missing tokens in a sentence [3].
*   The retriever is trained in an unsupervised manner using a performance-based signal from unsupervised text; specifically, retrievals that improve the language model's perplexity are rewarded, while uninformative retrievals are penalized [1]. 
*   The framework is learned end-to-end by backpropagating through the retrieval step, which involves considering an entire corpus of textual knowledge [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7

### Multi-Agent Answer

REALM (Retrieval-Augmented Language Model) is a framework that augments language model pre-training with a latent knowledge retriever to capture knowledge in a more modular and interpretable way [E1]. While standard language model pre-training stores world knowledge implicitly within neural network parameters—a method that requires increasingly larger networks to accommodate more facts—REALM allows the model to retrieve and attend over documents from a large corpus, such as Wikipedia, during pre-training, fine-tuning, and inference [E1]. A key feature of this approach is that its memories are "grounded," meaning each memory is associated with a specific document rather than unnamed value vectors, which provides interpretability for applications like Open-domain Question Answering (Open-QA) [E7].

Retrieval-augmented language model pre-training refers to a paradigm that extends retrieval-based approaches to the language model pre-training stage [E8]. In this framework, the generation of an output $y$ from an input $x$ is decomposed into two steps: first, retrieving helpful documents $z$ from a knowledge corpus $Z$, and second, predicting $y$ conditioned on both $x$ and $z$ [E8]. The model utilizes a neural knowledge retriever and a knowledge-augmented encoder [E8]. During pre-training, the task is masked language modeling, which requires predicting the original value of each [MASK] token in $x$ [E6].

### Metrics

- baseline_latency_seconds: 10.419
- orchestrator_latency_seconds: 90.564
- baseline_total_tokens: 8987
- orchestrator_total_tokens: 56898
- baseline_citation_count: 8
- orchestrator_evidence_count: 15
- fact_check_status_counts: {'supported': 7}

## Question 4

Type: definition

How does REALM differ from a standard parametric language model such as BERT in where knowledge is stored and accessed?

### Baseline Answer

Standard parametric language models, such as BERT, store learned world knowledge implicitly within the parameters of the underlying neural network [1]. This implicit storage makes it difficult to determine what knowledge is stored and where, and limits storage space to the size of the network, requiring ever-larger networks to capture more facts [1].

In contrast, REALM (Retrieval-Augmented Language Model) differs in the following ways:

*   **Storage:** Instead of relying solely on parameters, REALM augments pre-training with a learned textual knowledge retriever that allows the model to access a large textual knowledge corpus, such as Wikipedia [1, 2]. Its "memories" are grounded, meaning each memory is associated with a specific document rather than unnamed value vectors [3].
*   **Access:** REALM uses a "retrieve-then-predict" process [2]. Before making a prediction, the model uses the retriever to retrieve documents from a large corpus and then attends over those documents to inform its prediction [2]. This approach explicitly exposes the role of world knowledge by asking the model to decide what knowledge to retrieve and use during inference [1, 2].

Citations:
[1] data/2002.08909v1.pdf (chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2)
[2] data/2002.08909v1.pdf (chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952)
[3] data/2002.08909v1.pdf (chunk_id: 2002.08909v1-14-83fbe5c3ec4e1ed386558b56)

### Multi-Agent Answer

In a standard parametric language model, world knowledge is stored implicitly within the neural network's parameters [E2]. This implicit storage typically requires increasingly larger networks to cover a greater number of facts [E2].

In contrast, the Retrieval-Augmented Language Model (REALM) framework captures knowledge in a more modular and interpretable way [E1, E2]. Instead of relying solely on parameters, REALM utilizes a learned textual knowledge retriever to pull documents from a large corpus, such as Wikipedia [E1, E2]. During inference, the model is required to decide which specific knowledge to retrieve and then attends over those retrieved documents to help inform its predictions [E1]. This process decomposes the learning of a distribution into two steps: first retrieving documents and then predicting [E3].

### Metrics

- baseline_latency_seconds: 6.092
- orchestrator_latency_seconds: 80.612
- baseline_total_tokens: 8214
- orchestrator_total_tokens: 54074
- baseline_citation_count: 8
- orchestrator_evidence_count: 15
- fact_check_status_counts: {'supported': 4, 'unsupported': 2}

## Question 5

Type: method/mechanism

How does REALM's retrieve-then-predict framework work, including the role of the latent document variable z?

### Baseline Answer

REALM decomposes the task of learning a distribution $p(y|x)$ over possible outputs $y$ for a given input $x$ into a two-step "retrieve-then-predict" generative process [3].

**The Retrieve-then-Predict Framework:**
1.  **Retrieve:** Given an input $x$, the model first retrieves potentially helpful documents $z$ from a knowledge corpus $Z$ [3]. This step is modeled as a sample from the distribution $p(z|x)$ [3]. The retrieval is performed by a neural knowledge retriever using a dense inner product model, where the relevance score between $x$ and $z$ is the inner product of their vector embeddings [3].
2.  **Predict:** The model then conditions on both the retrieved document $z$ and the original input $x$ to generate the output $y$, modeled as $p(y|z, x)$ [3]. This component is handled by a knowledge-augmented encoder [3].

**The Role of the Latent Document Variable $z$:**
The framework treats the retrieved document $z$ as a latent variable [3]. To obtain the overall likelihood of generating the output $y$, the model marginalizes over all possible documents $z$ in the corpus $Z$ [3]. This is expressed mathematically as:
$$p(y|x) = \sum_{z \in Z} p(y|z, x) p(z|x)$$ [3]

By modeling the approach this way, REALM can be optimized by maximizing the marginal likelihood [1].

Citations:
[1] data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[3] data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7

### Multi-Agent Answer

The REALM framework utilizes a "retrieve-then-predict" method that decomposes the process of learning a distribution $p(y | x)$ into two distinct steps [E4]. This approach is modeled as a latent variable language model that optimizes the marginal likelihood [E1].

The framework consists of two primary components:
*   **Neural Knowledge Retriever:** This component models the distribution $p(z | x)$ [E4]. Before making a prediction, the model uses the retriever to pull documents from a large corpus, such as Wikipedia [E1]. 
*   **Knowledge-Augmented Encoder:** This component models the distribution $p(y | z, x)$ [E4]. The model attends over the retrieved documents to help inform its predictions [E1].

In this framework, the latent document variable $z$ represents the documents retrieved from the corpus [E4]. The training objective encourages the retriever to increase the relevance score $f(x, z)$ for documents that improve prediction accuracy, specifically when $p(y | z, x) > p(y | x)$ [E8].

### Metrics

- baseline_latency_seconds: 6.065
- orchestrator_latency_seconds: 45.814
- baseline_total_tokens: 8021
- orchestrator_total_tokens: 32209
- baseline_citation_count: 8
- orchestrator_evidence_count: 12
- fact_check_status_counts: {'supported': 9}

## Question 6

Type: method/mechanism

How does the paper train the retriever when the retrieved document is latent, and how does learning signal flow back to retrieval?

### Baseline Answer

The paper trains the retriever by modeling the retrieve-then-predict approach as a latent variable language model and optimizing the marginal likelihood [1]. Specifically, for the pre-training task of masked language modeling, the model treats the retrieved document $z$ as a latent variable and marginalizes over all possible documents $z$ to obtain the overall likelihood of generating the target output $y$ [4]. The training signal is performance-based, using unsupervised text where a retrieval that improves the language model's perplexity is rewarded, while uninformative retrievals are penalized [1].

The learning signal flows back to the retrieval module via backpropagation through the retrieval step [1, 2]. The gradient of the log-likelihood with respect to the retriever parameters $\theta$ is derived as:

$$\nabla \log p(y |x) = \sum_{z} \left[ \frac{p(y |z, x)}{p(y |x)} - 1 \right] p(z |x) \nabla f(x, z)$$

[6]

This derivation shows that the signal from the language modeling objective backpropagates all the way through the retriever [2]. In a setting where a single "gold" document $z^*$ allows for perfect prediction accuracy, this gradient descent is equivalent to the typical maximum likelihood training objective used in supervised learning [6].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7
[6] source: data/2002.08909v1.pdf, chunk_id: 2

### Multi-Agent Answer

The REALM framework models the "retrieve-then-predict" process as a latent variable language model and optimizes the marginal likelihood [E1]. In this framework, the generative process decomposes the probability of an output $p(y|x)$ into two steps: first, retrieving documents $z$ from a knowledge corpus $Z$ ($p(z|x)$), and second, conditioning on both the retrieved $z$ and input $x$ to generate output $y$ ($p(y|z,x)$) [E5].

The retriever is trained using a performance-based signal derived from unsupervised text [E1]. Specifically, the model rewards retrievals that improve the language model's perplexity and penalizes uninformative retrievals [E1]. This training is conducted in an unsupervised manner, using masked language modeling as the learning signal [E2].

Learning is performed end-to-end by backpropagating through a retrieval step that considers an entire corpus of textual knowledge [E1, E2]. The framework uses a signal from the language modeling objective that backpropagates through the retrieval step [E2].

### Metrics

- baseline_latency_seconds: 6.531
- orchestrator_latency_seconds: 84.202
- baseline_total_tokens: 7920
- orchestrator_total_tokens: 55173
- baseline_citation_count: 8
- orchestrator_evidence_count: 11
- fact_check_status_counts: {'supported': 6, 'unsupported': 1}

## Question 7

Type: method/mechanism / implementation

What approximations or engineering choices does REALM use to make retrieval over a large corpus practical during training and inference?

### Baseline Answer

To make retrieval over a large corpus practical during training and inference, REALM employs several engineering choices and approximations:

*   **MIPS Formulation:** The selection of the best documents is formulated as a Maximum Inner Product Search (MIPS) [2].
*   **Caching and Asynchronous Updates:** The retriever is structured so that the computation performed for each document can be cached and updated asynchronously [2].
*   **Parallelization:** During pre-training, the document embedding step for the MIPS index is parallelized over 16 TPUs [4].
*   **Index Refresh Rate:** Instead of updating the index constantly, REALM runs a parallel process to re-embed corpus documents and rebuild the MIPS index approximately once every 500 training steps [5].
*   **Document Retrieval Limits:** 
    *   During **pre-training**, for each example, the model retrieves and marginalizes over 8 candidate documents, which includes a null document $\emptyset$ [4].
    *   During **fine-tuning inference**, the system considers only the top-5 candidate documents [1, 4].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-11-3fa55fc3148d1188cb70ab91
[5] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e

### Multi-Agent Answer

To manage the computational challenge of selecting documents from a corpus containing millions of items, REALM employs the following approximations and engineering choices:

*   **Document Selection:** The retriever uses Maximum Inner Product Search (MIPS) for document selection [E1]. 
*   **Computational Efficiency:** The system utilizes cached and asynchronously updated computations to handle the scale of the retrieval process [E1]. Specifically, the MIPS index is updated periodically, with one refresh occurring approximately every 500 training steps [E9].
*   **Candidate Management:** During the pre-training phase, the model marginalizes over 8 candidate documents [E3]. For fine-tuning inference, the model considers the top-5 candidates [E3].

### Metrics

- baseline_latency_seconds: 6.535
- orchestrator_latency_seconds: 44.073
- baseline_total_tokens: 8688
- orchestrator_total_tokens: 32389
- baseline_citation_count: 8
- orchestrator_evidence_count: 11
- fact_check_status_counts: {'supported': 5}

## Question 8

Type: comparison

How does REALM compare with ORQA or other open-domain QA baselines, and what evidence supports that comparison?

### Baseline Answer

REALM compares to ORQA and other open-domain QA baselines as follows:

*   **Comparison with ORQA:** ORQA is the most direct comparison to REALM because both use identical fine-tuning setups, hyperparameters, and training data [1]. Additionally, the retrievers for both REALM pre-training and ORQA are initialized using the Inverse Cloze Task [2]. While ORQA uses a fixed index, REALM adds a novel language model pre-training step and backpropagates into the MIPS index [7]. The improvement of REALM over ORQA is attributed purely to better pre-training methods [1].
*   **Comparison with other Retrieval-based systems:** Compared to other retrieval-based systems (such as Asai et al., 2019; Min et al., 2019a;b) that often retrieve between 20 to 80 documents, REALM achieves the overall best performance while retrieving only 5 documents [1].
*   **Comparison with Generation-based systems:** REALM compares against state-of-the-art systems from the generation-based paradigm [4]. For the most competitive and comparable generation-based baseline, REALM is compared against concurrent work that fine-tunes T5 for Open-QA, including Base, Large, and an 11-billion parameter model [2].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-10-8ea61faa3a17c1fc8f8725d8
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7
[7] source: data/2002.08909v1.pdf, chunk_id: 2002

### Multi-Agent Answer

REALM outperforms all existing systems on Open-QA benchmarks, outperforming previous systems by 4–16% absolute accuracy [E7].

**Comparison with ORQA**
ORQA is considered the most direct comparison to REALM because the fine-tuning setup, hyperparameters, and training data are identical [E2]. While the retrievers for both REALM pre-training and ORQA are initialized using the Inverse Cloze Task [E1], REALM is distinguished by its pre-training step and its ability to backpropagate into the MIPS index, whereas ORQA uses a fixed index [E8]. The improvement of REALM over ORQA is attributed entirely to its superior pre-training methods [E2][E4]. 

Quantitative comparisons between the two models include:
* **NaturalQuestions (NQ):** REALM (using Wikipedia/Wikipedia) achieved a score of 39.2, while ORQA achieved 33.3 [E4].
* **WebQuestions (WQ):** REALM (using Wikipedia/Wikipedia) achieved a score of 40.2, while ORQA achieved 36.4 [E4].
* **CuratedTrec (CT):** REALM (using Wikipedia/Wikipedia) achieved a score of 46.8, while ORQA achieved 30.1 [E4].

**Comparison with Other Baselines**
REALM also outperforms the T5-11B model while being 30 times smaller [E4]. Specifically, in the NaturalQuestions (NQ) benchmark, REALM (using Wikipedia/Wikipedia) achieved a score of 39.2 compared to T5-11B's score of 34.5 [E4]. In WebQuestions (WQ), REALM achieved 40.2 compared to T5-11B's 37.4 [E4]. Additionally, REALM achieves the best overall performance among compared retrieval-based systems despite retrieving fewer documents (5) than other typical retrieval-based systems, which range from 20 to 80 documents [E2].

### Metrics

- baseline_latency_seconds: 6.717
- orchestrator_latency_seconds: 50.278
- baseline_total_tokens: 7685
- orchestrator_total_tokens: 30472
- baseline_citation_count: 8
- orchestrator_evidence_count: 11
- fact_check_status_counts: {'supported': 11}

## Question 9

Type: comparison

How does REALM's retrieval-based approach compare with storing knowledge only in model parameters?

### Baseline Answer

REALM's retrieval-based approach differs from models that store knowledge only in their parameters in the following ways:

*   **Interpretability and Modularity:** Unlike models that store knowledge implicitly in their parameters, the REALM approach captures knowledge in a more modular and interpretable way [1, 3]. The model's memories are "grounded" because each memory is associated with a specific document rather than unnamed value vectors, which provides provenance that is crucial for applications like Open-domain Question Answering (Open-QA) [6].
*   **Explicit Role of Knowledge:** REALM explicitly exposes the role of world knowledge by requiring the model to decide what knowledge to retrieve and use during inference [1]. 
*   **Storage Limitations:** In models where knowledge is stored implicitly in the parameters of a neural network, it is difficult to determine what knowledge is stored and where [3]. Furthermore, the storage space in such models is limited by the size of the network, meaning that capturing more world knowledge requires training increasingly larger networks, which can be prohibitively expensive or slow [3].
*   **Performance:** In evaluations on Open-QA benchmarks, REALM outperformed state-of-the-art models that store knowledge implicitly (such as T5) by a margin of 4-16% in absolute accuracy [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952, chunk_index: 1
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2, chunk_index: 0
[6] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e, chunk_index: 13

### Multi-Agent Answer

While standard language model pre-training captures world knowledge, that knowledge is typically stored implicitly within the neural network parameters [E8]. This implicit storage approach requires increasingly larger networks to cover an increasing number of facts [E8].

In contrast, the REALM (Retrieval-Augmented Language Model) framework augments pre-training with a learned textual knowledge retriever to capture knowledge in a more modular and interpretable way [E3, E8]. Instead of relying solely on parameters, REALM allows the model to retrieve and attend over documents from a large corpus, such as Wikipedia, during pre-training, fine-tuning, and inference [E3, E8].

Key differences include:

*   **Interpretability and Grounding:** Unlike models that use unnamed value vectors to store knowledge, REALM's memories are "grounded," meaning each memory is associated with a specific document [E6, E7]. This grounding provides a level of interpretability and provenance that is considered crucial for users to trust predicted answers in Open-domain Question Answering (Open-QA) [E6, E7].
*   **Knowledge Scope:** REALM generalizes the scope of previous language models—which condition on surrounding words, sentences, or paragraphs—by extending the scope to the entire text corpus [E5, E7].

### Metrics

- baseline_latency_seconds: 7.296
- orchestrator_latency_seconds: 78.454
- baseline_total_tokens: 7842
- orchestrator_total_tokens: 52754
- baseline_citation_count: 8
- orchestrator_evidence_count: 15
- fact_check_status_counts: {'supported': 3, 'unsupported': 5}

## Question 10

Type: evidence synthesis / ablation

What ablation or diagnostic evidence shows that retrieval pre-training improves REALM rather than only the reader component?

### Baseline Answer

To determine whether REALM pre-training improves the retriever, the encoder, or both, researchers performed an ablation by resetting the parameters of either the retriever or the encoder to their baseline state before fine-tuning [4].

The evidence shows that:
*   **Both components benefit:** Both the encoder and the retriever benefit from REALM training when treated separately [4].
*   **Synergistic effect:** The best performance requires both components to act in unison [4].
*   **Retriever contribution metric:** To more significantly isolate the contribution of improving the retriever during pre-training, the researchers reported how often the gold answer appears in the top-5 retrievals before applying any fine-tuning [1, 4].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05, chunk_index: 12
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e, chunk_index: 13

### Multi-Agent Answer

The provided evidence does not contain specific ablation or diagnostic studies that directly isolate whether retrieval pre-training improves the REALM model overall or exclusively the reader component.

However, the evidence provides the following related information regarding the components and diagnostic metrics of the model:

*   **Knowledge Storage and Modularity**: Standard language model pre-training captures world knowledge implicitly within neural network parameters [E2]. In contrast, REALM augments pre-training with a latent knowledge retriever to capture knowledge in a more modular and interpretable way [E2].
*   **Retrieval Utility (RU) Metric**: The usefulness of retrieval can be measured using the Retrieval Utility (RU) metric, where a negative RU indicates that a retrieved document is less useful for predicting a target than a null document [E6].
*   **RU as a Diagnostic Indicator**: The RU value increases steadily throughout the pre-training process [E6]. Furthermore, RU is a stronger predictor of performance on downstream Open-domain Question Answering (Open-QA) tasks than the overall log-likelihood [E6].
*   **Adaptability**: The REALM model can adapt to an updated knowledge corpus; for example, a model pre-trained on a 2018 corpus can successfully retrieve documents and generate correct tokens when using a 2020 corpus [E6].

### Metrics

- baseline_latency_seconds: 4.937
- orchestrator_latency_seconds: 83.248
- baseline_total_tokens: 7803
- orchestrator_total_tokens: 53865
- baseline_citation_count: 8
- orchestrator_evidence_count: 13
- fact_check_status_counts: {'unsupported': 1, 'supported': 6}

## Question 11

Type: evidence synthesis

Synthesize the evidence for why REALM improves open-domain QA performance, including retrieval quality, pre-training, and downstream fine-tuning.

### Baseline Answer

REALM improves open-domain question answering (Open-QA) performance through several interconnected mechanisms involving pre-training, retrieval quality, and the relationship between its components:

*   **Pre-training:** REALM uses a novel pre-training method that augments language model pre-training with a learned textual knowledge retriever [4]. Unlike models that store knowledge implicitly in parameters, REALM's retriever is trained using a performance-based signal from unsupervised text [5]. Specifically, it uses masked language modeling (MLM) as a learning signal, where the retriever is rewarded for selecting documents that improve the language model's perplexity [5]. The improvement of REALM over the direct baseline ORQA is attributed purely to these better pre-training methods [1].
*   **Retrieval Quality:** REALM's pre-training significantly improves the retriever, allowing it to retrieve relevant information even when trained only on unsupervised text [8]. For example, the model can achieve a much higher probability for a correct masked term by retrieving a document containing a related fact [8]. Additionally, REALM can achieve superior overall performance while retrieving only 5 documents, whereas other retrieval-based systems often retrieve between 20 and 80 documents [1].
*   **Downstream Fine-tuning:** The pre-trained components are then fine-tuned on Open-QA tasks [4]. Ablation studies indicate that while both the encoder and the retriever benefit from REALM pre-training individually, the best downstream results require both components to act in unison [8]. REALM's retriever is specifically designed to transfer to other tasks because it retrieves raw text rather than labeled examples [5].

As a result of these factors, REALM outperforms previous state-of-the-art methods on three popular Open-QA benchmarks by a margin of 4-16% absolute accuracy [4, 5].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b

### Multi-Agent Answer

REALM improves open-domain question answering (Open-QA) performance through a framework that augments language model pre-training with a learned textual knowledge retriever [E6].

**Retrieval Quality**
The neural knowledge retriever utilizes a dense inner product model to calculate relevance scores [E4]. The retriever is trained using a performance-based signal from unsupervised text, where retrievals that improve the language model's perplexity are rewarded and uninformative retrievals are penalized [E6]. This allows the retriever to be pre-trained in an unsupervised manner using masked language modeling as the learning signal [E7]. This approach enables high retrieval quality; REALM achieves its best overall performance while retrieving only 5 documents, whereas other retrieval-based systems often retrieve between 20 and 80 documents [E1].

**Pre-training**
The improvement of REALM over ORQA is attributed purely to its superior pre-training methods, as the fine-tuning setups, hyperparameters, and training data are identical [E1]. While standard language model pre-training stores world knowledge implicitly in neural network parameters [E7], REALM's pre-training uses a latent knowledge retriever to capture knowledge in a modular and interpretable way [E7]. This pre-training method is applicable to both single-corpus settings (where the question and knowledge source are both Wikipedia) and separate-corpus settings (where the question is from CC-News and the knowledge source is Wikipedia) [E1].

**Downstream Fine-tuning**
The pre-trained model can be further trained (fine-tuned) for the downstream task of Open-QA, which often leads to better generalization than training from scratch [E3]. During fine-tuning inference, the top-5 candidates are considered [E5]. REALM achieves new state-of-the-art results on three benchmarks, outperforming previous systems by 4-16% absolute accuracy [E3][E6]. Additionally, REALM outperforms the T5-11B model despite being 30 times smaller [E5].

### Metrics

- baseline_latency_seconds: 6.995
- orchestrator_latency_seconds: 88.229
- baseline_total_tokens: 8205
- orchestrator_total_tokens: 54998
- baseline_citation_count: 8
- orchestrator_evidence_count: 11
- fact_check_status_counts: {'supported': 11}

## Question 12

Type: multi-step reasoning

Explain step by step how a masked-language-model pre-training objective can improve downstream open-domain QA in REALM.

### Baseline Answer

In REALM, the masked-language-model (MLM) pre-training objective improves downstream open-domain question answering (Open-QA) through the following process:

1.  **Unsupervised Pre-training with MLM**: The model undergoes pre-training using an unsupervised masked language modeling task on a corpus $X$ [1, 3]. In this task, tokens are randomly masked in a text passage, and the model must predict the original value of those missing tokens [1, 4].
2.  **Learning Representations and World Knowledge**: To successfully predict masked tokens, a good MLM must learn to encode syntactic and semantic information as well as world knowledge [1].
3.  **Joint Training of Retriever and Encoder**: REALM augments the MLM pre-training by adding a learned textual knowledge retriever [2, 5]. The model is trained as a "retrieve-then-predict" process where the knowledge retriever and the knowledge-augmented encoder are jointly pre-trained [2, 3].
4.  **Performance-Based Learning Signal**: The retriever is trained using a performance-based signal from the unsupervised text [5]. A retrieval that improves the language model's perplexity is rewarded, while uninformative retrievals are penalized [5]. Specifically, the signal from the MLM objective backpropagates through the retrieval step to the retriever [2].
5.  **Transfer to Open-QA**: Because the retriever is designed to transfer to other tasks (retrieving text rather than labeled examples), the representations and retrieval capabilities learned during pre-training are then used during supervised fine-tuning for the Open-QA task [5].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-2-7f240c64641ad3f52fc62e97, chunk_index: 2
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2, chunk_index: 0
[3] source: data/2002.08909v1.pdf,

### Multi-Agent Answer

A masked-language-model (MLM) pre-training objective improves downstream open-domain question answering (Open-QA) in REALM through the following steps:

1.  **Learning Language Representations:** The MLM pre-training objective aims to learn useful language representations from unlabeled text corpora [E1]. A successful MLM learns to encode syntactic information, semantic information, and world knowledge [E1].
2.  **Unsupervised Retriever Training:** REALM augments language model pre-training with a latent knowledge retriever [E2]. This retriever is trained in an unsupervised manner, using the MLM task as the learning signal [E2]. During this pre-training task, the model must predict the original value of each [MASK] token in an input text passage [E3].
3.  **Performance-Based Optimization:** The retriever is optimized using a performance-based signal derived from unsupervised text [E4]. The training process rewards retrievals that improve the language model's perplexity and penalizes uninformative retrievals [E4].
4.  **Downstream Generalization:** This pre-training allows the model to be fine-tuned for downstream tasks, such as Open-QA, which often leads to better generalization than training from scratch [E1]. Because the retriever is trained on text rather than labeled examples, it is designed to transfer to other tasks [E4].

### Metrics

- baseline_latency_seconds: 7.169
- orchestrator_latency_seconds: 84.988
- baseline_total_tokens: 9087
- orchestrator_total_tokens: 55560
- baseline_citation_count: 8
- orchestrator_evidence_count: 13
- fact_check_status_counts: {'unsupported': 4, 'supported': 8}

## Question 13

Type: multi-step reasoning / error analysis

If REALM retrieves an irrelevant document, how would that affect p(z|x), p(y|z,x), and the final answer prediction?

### Baseline Answer

If REALM retrieves an irrelevant document ($z$), it would affect the components of the model as follows:

*   **$p(z|x)$**: This represents the retrieval distribution, which is modeled as a sample from the distribution of potentially helpful documents given an input $x$ [3]. If a document is irrelevant, it implies the retriever has selected a document that does not provide useful information for the input [1].
*   **$p(y|z,x)$**: This is the conditional probability of generating the output $y$ given the retrieved document $z$ and the original input $x$ [3]. If the document $z$ is irrelevant, it results in a negative Retrieval Utility (RU), meaning $z$ is less useful for predicting $y$ than a null document ($\emptyset$) [1].
*   **Final answer prediction ($p(y|x)$)**: The overall likelihood of generating the answer $y$ is obtained by marginalizing over all possible documents $z$ using the formula $p(y |x) = \sum_{z \in Z} p(y |z, x) p(z |x)$ [3]. When REALM retrieves documents with related facts, the marginalized probability of the correct answer increases [2]. Conversely, if the retriever lacks good embeddings at the start of training, it may retrieve unrelated documents, which can cause the knowledge-augmented encoder to learn to ignore them, potentially creating a "vicious cycle" where the retriever fails to receive meaningful gradients for improvement [7].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-20-58cd33db77feaae8a3f8d036
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51

### Multi-Agent Answer

The provided evidence does not explicitly state the mathematical effect of an irrelevant document on $p(z|x)$, $p(y|z,x)$, or the final answer prediction.

However, the evidence does provide information regarding Retrieval Utility (RU), which is defined as $\text{RU} = \log p(y | z, x) - \log p(y | \emptyset, x)$ [E1]. A negative RU indicates that the retrieved document $z$ is less useful for predicting $y$ than a null document $\emptyset$ [E1]. One reason for a negative RU is that the document $z$ may be irrelevant to $x$ [E1].

### Metrics

- baseline_latency_seconds: 6.751
- orchestrator_latency_seconds: 72.522
- baseline_total_tokens: 8309
- orchestrator_total_tokens: 48178
- baseline_citation_count: 8
- orchestrator_evidence_count: 12
- fact_check_status_counts: {'unsupported': 1, 'supported': 3}

## Question 14

Type: limitation/uncertainty

What limitations, uncertainties, or missing comparisons should be noted when interpreting REALM's reported results?

### Baseline Answer

When interpreting REALM's reported results, the following limitations, uncertainties, or missing comparisons should be noted:

*   **Unused Data:** Some data that could potentially benefit REALM was not used in the experiments [1].
*   **MIPS Index Staleness:** The researchers found that a "stale index" can hurt model training, suggesting that further reducing the staleness of the index could potentially offer better optimization [4].
*   **Uncertainty in Retrieval Utility (RU):** A negative RU indicates that the retrieved document $z$ is less useful for predicting $y$ than a null document; however, this could be due to $z$ being irrelevant to $x$, or it could mean the masked tokens do not require world knowledge, or that the necessary knowledge is already sufficiently "baked into the model’s parameters" [2].
*   **Missing Comparisons/Generalizations:** The presented work is described as a "minimal instantiation" of a family of REALM-like approaches, with future work suggested for generalizing to structured knowledge, multi-lingual settings, and multi-modal settings [5].

### Multi-Agent Answer

When interpreting REALM's reported results, several limitations, uncertainties, and experimental considerations should be noted:

**Experimental Limitations and Data Utilization**
* Certain data that could potentially benefit REALM was not used in the conducted experiments [E1].
* While REALM can adapt to new knowledge by modifying corpus documents, the encoder may still retain old knowledge in its parameters [E6]. This can result in the model making predictions based on outdated information, such as predicting "Thatcher" for the UK Prime Minister due to frequent mentions in Wikipedia [E6].

**Optimization and Component Interaction**
* The use of a stale MIPS index can negatively impact model training [E2]. Consequently, frequent index refreshes are considered important for optimization [E2].
* Although both the encoder and the retriever benefit from being trained separately, optimal results require both components to act in unison [E2].

**Uncertainties in Retrieval Utility (RU)**
* A negative Retrieval Utility (RU) indicates that a document $z$ is less useful for predicting a masked token than a null document $\emptyset$ [E6, E8]. 
* A negative RU may imply several different things: the document $z$ is irrelevant to the input $x$, the masked tokens do not require world knowledge to predict, or the necessary knowledge is already sufficiently common and "baked into" the model's parameters [E6, E8].

### Metrics

- baseline_latency_seconds: 3.689
- orchestrator_latency_seconds: 79.858
- baseline_total_tokens: 7217
- orchestrator_total_tokens: 55599
- baseline_citation_count: 8
- orchestrator_evidence_count: 11
- fact_check_status_counts: {'supported': 6, 'unsupported': 2}

## Question 15

Type: citation grounding / uncertainty

Which claims about REALM's performance or mechanism cannot be verified unless the answer cites specific experimental evidence from the paper?

### Baseline Answer

Based on the provided context, the following claims regarding REALM's performance or mechanism cannot be verified without citing specific experimental evidence (such as results from Tables 1 or 2):

*   **Performance comparison to ORQA:** While the text states that the improvement of REALM over ORQA is due to better pre-training methods [1], the specific magnitude or degree of this improvement requires Table 1 for verification [5].
*   **Overall performance relative to other systems:** The claim that REALM gets the "overall best performance" while only retrieving 5 documents compared to other retrieval-based systems that retrieve 20 to 80 documents [1] requires experimental data for verification.
*   **Effectiveness of individual components:** The claim that both the encoder and retriever benefit from REALM training separately, but the best results require both acting in unison, requires the ablation results presented in Table 2 [4].
*   **Impact of index refresh rates:** The claim that a stale MIPS index can hurt model training and that further reducing staleness could offer better optimization is based on results from Table 2 [4].
*   **Benchmark accuracy:** The claim that REALM outperforms previous methods on three Open-QA benchmarks by a margin of 4-16% absolute accuracy requires the specific experimental results from the paper [7].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05, chunk_index: 12
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e, chunk_index: 13
[5] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-10-8ea61faa3a17c1fc8f8725d8, chunk_index: 10
[7] source: data/2002.

### Multi-Agent Answer

Based on the provided evidence, the following claims regarding REALM's performance and mechanism are verified:

*   **Performance:** REALM achieves new state-of-the-art results on three Open-domain Question Answering (Open-QA) benchmarks: NATURAL QUESTIONS, WEB QUESTIONS, and CURATED TREC [E1]. Specifically, it outperforms previous systems by a margin of 4-16% in absolute accuracy [E1, E2].
*   **Comparison to ORQA:** The improvement of REALM over ORQA is attributed purely to better pre-training methods, as the fine-tuning setup, hyperparameters, and training data are identical [E3].
*   **Pre-training Mechanism:** The retriever is trained using a performance-based signal from unsupervised text, where retrievals that improve the language model's perplexity are rewarded and uninformative retrievals are penalized [E1].
*   **Component Synergy:** While both the encoder and the retriever benefit separately from REALM training, optimal results require both components to act in unison [E4].
*   **Masking Strategy:** The salient span masking scheme (masking entities or dates) is a crucial component of REALM [E4, E5].
*   **Optimization and Indexing:** Stable optimization is achieved through asynchronous Maximum Inner Product Search (MIPS) index refreshes, provided they occur at a sufficiently frequent rate [E5].
*   **Knowledge Adaptation:** REALM can adapt to new world knowledge by modifying corpus documents, though the knowledge-augmented encoder may still "remember" old knowledge, potentially causing outdated predictions [E6].

The provided evidence does not contain claims that cannot be verified; all major functional and performance claims mentioned in the notes are accompanied by specific supporting details or experimental results.

### Metrics

- baseline_latency_seconds: 6.854
- orchestrator_latency_seconds: 65.804
- baseline_total_tokens: 7930
- orchestrator_total_tokens: 55166
- baseline_citation_count: 8
- orchestrator_evidence_count: 12
- fact_check_status_counts: {'unsupported': 2, 'supported': 5}
