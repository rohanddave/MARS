# experiment12: retrieval sweep, strong checker and synthesizer, top_k=8

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

REALM retrieves from a large textual knowledge corpus ($Z$), such as Wikipedia [1, 2].

The model uses this external knowledge through a "retrieve-then-predict" generative process [3]. This process is decomposed into two specific steps:
1.  **Retrieve:** Given an input $x$, the model first retrieves potentially helpful documents $z$ from the knowledge corpus $Z$ [3]. This is modeled as a sample from the distribution $p(z | x)$ [3].
2.  **Predict:** The model then conditions on both the retrieved documents $z$ and the original input $x$ to generate the output $y$, modeled as $p(y | z, x)$ [3].

During inference, the language model uses the retriever to fetch documents from the corpus and then attends over those documents to inform its prediction [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7

### Multi-Agent Answer

REALM retrieves information from a large knowledge corpus, such as Wikipedia [E2, E3]. The model can be applied in a single-corpus setting where both the pre-training corpus and the knowledge corpus are Wikipedia, or in a separate-corpus setting where the pre-training corpus is CC-News and the knowledge corpus is Wikipedia [E5].

The model utilizes this external knowledge through a two-step process [E1]:

*   **Retrieval:** A "neural knowledge retriever" models the retrieval distribution $p(z |x)$ to identify potentially helpful documents $z$ from the knowledge corpus [E1]. This retriever is defined using a dense inner product model, where the relevance score is the inner product of the vector embeddings [E1].
*   **Prediction:** A "knowledge-augmented encoder" models the distribution $p(y |z, x)$ to predict the output $y$ conditioned on both the input $x$ and the retrieved documents $z$ [E1]. 

During this process, the language model retrieves documents and then attends over those documents to help inform its prediction [E2]. This approach allows the model to retrieve and attend over documents during pre-training, fine-tuning, and inference [E3].

### Metrics

- baseline_latency_seconds: 7.176
- orchestrator_latency_seconds: 84.262
- baseline_total_tokens: 8621
- orchestrator_total_tokens: 55844
- baseline_citation_count: 8
- orchestrator_evidence_count: 11
- fact_check_status_counts: {'unsupported': 2, 'supported': 6}

## Question 2

Type: easy lookup

Which downstream tasks or benchmarks does the paper use to evaluate REALM?

### Baseline Answer

To evaluate REALM, the paper uses the following Open-QA benchmarks:

*   **NQ** (NaturalQuestions) [6]
*   **WQ** (WebQuestions) [6]
*   **CT** (ComplexType) [6]

Additionally, the paper presents ablation experiments using the **NaturalQuestions-Open** (NQ-Open) development set [1, 7].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05, chunk_index: 12
[6] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-11-3fa55fc3148d1188cb70ab91, chunk_index: 11
[7] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e, chunk_index: 13

### Multi-Agent Answer

To evaluate REALM, the paper uses three Open-domain Question Answering (Open-QA) benchmarks: NATURAL QUESTIONS, WEB QUESTIONS, and CURATED TREC [E4]. The model's performance on these benchmarks is reported under different settings [E9]:

*   **NQ (Natural Questions):** REALM achieved an exact match score of 39.2 in a single-corpus setting (X=Wikipedia, Z=Wikipedia) and 40.4 in a separate-corpus setting (X=CC-News, Z=Wikipedia) [E9].
*   **WQ (Web Questions):** REALM achieved an exact match score of 40.2 in the single-corpus setting and 40.7 in the separate-corpus setting [E9].
*   **CT (Curated TREC):** REALM achieved an exact match score of 46.8 in the single-corpus setting and 42.9 in the separate-corpus setting [E9].

### Metrics

- baseline_latency_seconds: 6.234
- orchestrator_latency_seconds: 46.183
- baseline_total_tokens: 8188
- orchestrator_total_tokens: 31201
- baseline_citation_count: 8
- orchestrator_evidence_count: 10
- fact_check_status_counts: {'supported': 4}

## Question 3

Type: definition

What is REALM, and what does the paper mean by retrieval-augmented language model pre-training?

### Baseline Answer

REALM (Retrieval-Augmented Language Model) is a framework designed to capture knowledge in a modular and interpretable way [1, 2]. Instead of storing world knowledge implicitly in the parameters of a neural network, REALM augments language model pre-training algorithms with a learned textual knowledge retriever [1, 2]. This approach explicitly exposes the role of world knowledge by requiring the model to decide what knowledge to retrieve and use during inference [1]. Before making a prediction, the language model uses the retriever to pull documents from a large corpus, such as Wikipedia, and then attends over those documents to inform its prediction [1].

Retrieval-augmented language model pre-training refers to the process of augmenting language model pre-training with a latent knowledge retriever [2]. In this framework, the model is trained using a "retrieve-then-predict" approach [3]. For the pre-training task, which is masked language modeling, the model must predict the value of missing tokens in a sentence [3, 4]. The pre-training is performed in an unsupervised manner, using masked language modeling as the learning signal and backpropagating through a retrieval step that can consider millions of documents [2]. The key intuition is to train the retriever using a performance-based signal from unsupervised text: a retrieval that improves the language model's perplexity is rewarded, while uninformative retrieval is penalized [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7
[4] source: data/2002.08909v1.pdf, chunk

### Multi-Agent Answer

REALM (Retrieval-Augmented Language Model) is a framework that augments language model pre-training with a latent knowledge retriever [E9]. This approach is designed to capture knowledge in a more modular and interpretable way compared to traditional language model pre-training, where knowledge is stored implicitly in the parameters of a neural network [E9]. A key feature of REALM is that its memories are "grounded," meaning each memory is associated with a specific document rather than unnamed value vectors [E1]. This grounding provides a level of interpretability that is crucial for applications like Open-domain Question Answering (Open-QA), as it allows users to have provenance for a predicted answer [E1].

In the context of this paper, retrieval-augmented language model pre-training refers to a process where the model retrieves and attends over documents from a large corpus, such as Wikipedia, during the pre-training phase [E9]. The framework decomposes the process of learning a distribution $p(y |x)$ into two steps: retrieving a document and then predicting [E2]. Specifically, the generative process is formalized as $p(y |x) = \sum_{z \in Z} p(y |z, x) p(z |x)$, which treats the retrieved document $z$ as a latent variable [E2]. This allows for the first unsupervised pre-training of a knowledge retriever using masked language modeling as the learning signal [E9].

### Metrics

- baseline_latency_seconds: 8.655
- orchestrator_latency_seconds: 43.599
- baseline_total_tokens: 9006
- orchestrator_total_tokens: 30363
- baseline_citation_count: 8
- orchestrator_evidence_count: 14
- fact_check_status_counts: {'supported': 9}

## Question 4

Type: definition

How does REALM differ from a standard parametric language model such as BERT in where knowledge is stored and accessed?

### Baseline Answer

Standard parametric language models, such as BERT, store learned world knowledge implicitly within the parameters of the underlying neural network [1]. This implicit storage makes it difficult to determine what knowledge is stored and where, and it also limits storage space to the size of the network, meaning that capturing more knowledge requires training ever-larger networks [1].

In contrast, REALM augments language model pre-training with a learned textual knowledge retriever to capture knowledge in a more modular and interpretable way [1, 2]. Rather than relying solely on stored parameters, REALM explicitly exposes the role of world knowledge by using a retriever to retrieve and attend over documents from a large textual knowledge corpus (such as Wikipedia) during pre-training, fine-tuning, and inference [1, 2]. This approach allows the model to decide what knowledge to retrieve and use to inform its predictions [2]. Additionally, REALM's memories are "grounded" because each memory is associated with a specific document rather than unnamed value vectors [6].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[6] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-14-83fbe5c3ec4e1ed386558b56

### Multi-Agent Answer

Standard parametric language models store world knowledge implicitly within the parameters of a neural network [E3]. This implicit storage method requires the use of increasingly larger networks to cover more facts [E3].

In contrast, the REALM (Retrieval-Augmented Language Model) framework augments language model pre-training with a learned textual knowledge retriever [E2]. Unlike models that rely on stored parameters, REALM explicitly exposes the role of world knowledge by requiring the model to decide what to retrieve and use during inference [E2]. This approach allows the model to retrieve and attend over documents from a large corpus, such as Wikipedia, during pre-training, fine-tuning, and inference [E2, E3].

Furthermore, REALM's document index functions as a scalable grounded neural memory where the keys are document embeddings [E8]. Because these memories are grounded—meaning they are associated with a specific document rather than unnamed value vectors—the framework captures knowledge in a more modular and interpretable way [E2, E3, E8].

### Metrics

- baseline_latency_seconds: 6.008
- orchestrator_latency_seconds: 76.979
- baseline_total_tokens: 8188
- orchestrator_total_tokens: 54219
- baseline_citation_count: 8
- orchestrator_evidence_count: 15
- fact_check_status_counts: {'supported': 5, 'unsupported': 2}

## Question 5

Type: method/mechanism

How does REALM's retrieve-then-predict framework work, including the role of the latent document variable z?

### Baseline Answer

REALM's retrieve-then-predict framework decomposes the probability of an output $p(y|x)$ into two distinct steps:

1.  **Retrieve**: Given an input $x$, the model first retrieves potentially helpful documents $z$ from a knowledge corpus $Z$ [3]. This is modeled as a sample from the distribution $p(z|x)$ [3].
2.  **Predict**: The model then conditions on both the retrieved document $z$ and the original input $x$ to generate the output $y$, modeled as $p(y|z, x)$ [3].

**The Role of the Latent Document Variable $z$**
The framework treats the retrieved document $z$ as a latent variable [3]. To obtain the overall likelihood of generating an output $y$ given $x$, the model marginalizes over all possible documents $z$ in the corpus $Z$, expressed by the formula:
$p(y|x) = \sum_{z \in Z} p(y|z, x) p(z|x)$ [3].

This approach allows the model to be trained end-to-end by optimizing the marginal likelihood [1]. The retriever is trained using a performance-based signal from unsupervised text, where retrievals that improve the language model's perplexity are rewarded [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7

### Multi-Agent Answer

REALM employs a "retrieve-then-predict" framework that decomposes the generative process of producing an output $y$ from an input $x$ into two distinct stages: first retrieving potentially helpful documents $z$ from a knowledge corpus $Z$, and then predicting the output conditioned on both the input and the retrieved documents [E3]. This approach is utilized for both pre-training via masked language modeling and fine-tuning on Open-domain Question Answering (Open-QA) tasks [E3].

In this framework, the retrieved document, denoted as the latent variable $z$, is central to the generative process [E3]. The approach is modeled as a latent variable language model that optimizes the marginal likelihood [E1]. This is expressed mathematically as $p(y | x) = \sum_{z \in Z} p(y | z, x) p(z | x)$, where the model marginalizes over all possible documents $z$ within the knowledge corpus $Z$ [E3].

The knowledge retriever models the distribution $p(z | x)$ using a dense inner product model, where the relevance score $f(x, z)$ is defined as the inner product of the vector embeddings [E3]. During this process, the retriever identifies documents from a large corpus, such as Wikipedia, and the language model then attends over those documents to inform its prediction [E1, E2].

### Metrics

- baseline_latency_seconds: 5.716
- orchestrator_latency_seconds: 87.145
- baseline_total_tokens: 7976
- orchestrator_total_tokens: 57089
- baseline_citation_count: 8
- orchestrator_evidence_count: 11
- fact_check_status_counts: {'supported': 7, 'unsupported': 2}

## Question 6

Type: method/mechanism

How does the paper train the retriever when the retrieved document is latent, and how does learning signal flow back to retrieval?

### Baseline Answer

The paper trains the retriever by modeling the retrieve-then-predict approach as a latent variable language model and optimizing the marginal likelihood [1]. Specifically, the model treats the retrieved document $z$ as a latent variable and marginalizes over all possible documents $z$ to obtain the overall likelihood of generating an output $y$ given input $x$, expressed as $p(y |x) = \sum_{z \in Z} p(y |z, x) p(z |x)$ [4]. 

The learning signal flows back to the retrieval module through backpropagation [1, 2]. The gradient of the pre-training objective (a log-likelihood) with respect to the retriever parameters $\theta$ is calculated as:
$$\nabla \log p(y |x) = \sum_{z} [p(z |y, x) - p(z |x)] \nabla f(x, z)$$
where $f(x, z)$ represents the relevance score [6]. This demonstrates that the signal from the language modeling objective backpropagates through the retriever [2]. In a setting where a single "gold" document $z^*$ enables perfect prediction accuracy, gradient descent on the REALM objective becomes equivalent to gradient descent on $\log p(z^* |x)$, similar to typical maximum likelihood training in supervised learning [6].

Citations:
[1] data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[4] data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7
[6] data/2002.08909v1.pdf, chunk_id: 2002.08909v

### Multi-Agent Answer

The REALM framework models the "retrieve-then-predict" approach as a latent variable language model and optimizes the marginal likelihood [E1]. The retriever is pre-trained in an unsupervised manner, using masked language modeling as the learning signal [E2].

Learning signal flows back to the retriever through a performance-based mechanism [E1]. Specifically, the retriever is rewarded when it provides retrievals that improve the language model's perplexity, while uninformative retrievals are penalized [E1]. This allows for end-to-end learning by backpropagating through a retrieval step that considers an entire corpus of textual knowledge [E1, E2]. To prevent the retriever from merely learning to find exact string matches rather than other forms of relevance, trivial retrieval candidates are excluded during pre-training [E5].

### Metrics

- baseline_latency_seconds: 6.501
- orchestrator_latency_seconds: 39.905
- baseline_total_tokens: 7920
- orchestrator_total_tokens: 29440
- baseline_citation_count: 8
- orchestrator_evidence_count: 12
- fact_check_status_counts: {'supported': 6}

## Question 7

Type: method/mechanism / implementation

What approximations or engineering choices does REALM use to make retrieval over a large corpus practical during training and inference?

### Baseline Answer

To make retrieval over a large corpus practical during training and inference, REALM utilizes the following engineering choices and approximations:

*   **MIPS Formulation:** The selection of the best documents is formulated as a Maximum Inner Product Search (MIPS) [2].
*   **Caching and Asynchronous Updates:** The retriever is structured so that the computation performed for each document can be cached and updated asynchronously [2].
*   **Parallelization:** For the pre-training process, the document embedding step for the MIPS index is parallelized over 16 TPUs [4].
*   **Index Refreshing:** During pre-training, a parallel process is run to re-embed corpus documents and rebuild the MIPS index, resulting in an index refresh approximately every 500 training steps [5].
*   **Candidate Selection:**
    *   **During Pre-training:** For each example, the system retrieves and marginalizes over 8 candidate documents, which includes a null document $\emptyset$ [4].
    *   **During Fine-tuning Inference:** The system considers the top-5 candidate documents [1, 4].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05, chunk_index: 12
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952, chunk_index: 1
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-11-3fa55fc3148d1188cb70ab91, chunk_index: 11
[5] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a

### Multi-Agent Answer

To make retrieval over a large corpus practical during training and inference, REALM employs several engineering choices and approximations:

*   **MIPS Formulation and Caching:** Document selection is formulated as a Maximum Inner Product Search (MIPS) problem [E1]. To manage the computational challenge of considering millions of candidate documents, the retriever is structured so that computations can be cached and updated asynchronously [E1].
*   **Dense Inner Product Model:** The retriever uses a dense inner product model where the relevance score between an input and a document is calculated as the inner product of their vector embeddings [E4].
*   **Index Management:** To prevent a stale MIPS index from hurting model training, the index is refreshed approximately once every 500 training steps [E9].
*   **Parallelization:** Document embedding is parallelized over 16 TPUs [E3].
*   **Candidate Approximations:**
    *   During pre-training, the model marginalizes over 8 candidate documents, which includes a null document [E3].
    *   During fine-tuning inference, the model considers only the top-5 candidate documents [E3].

### Metrics

- baseline_latency_seconds: 7.481
- orchestrator_latency_seconds: 44.143
- baseline_total_tokens: 8702
- orchestrator_total_tokens: 31606
- baseline_citation_count: 8
- orchestrator_evidence_count: 11
- fact_check_status_counts: {'supported': 7}

## Question 8

Type: comparison

How does REALM compare with ORQA or other open-domain QA baselines, and what evidence supports that comparison?

### Baseline Answer

REALM compares to ORQA and other open-domain QA baselines as follows:

*   **Comparison with ORQA:** ORQA is described as the most direct comparison to REALM because they utilize identical training data, hyperparameters, and fine-tuning setups [1]. Additionally, the retrievers for both REALM pre-training and ORQA are initialized using the Inverse Cloze Task [2]. The improvement REALM shows over ORQA is attributed purely to its better pre-training methods [1]. While ORQA uses a fixed index, REALM adds a novel language model pre-training step and backpropagates into the MIPS index [7].
*   **Comparison with other Retrieval-based systems:** Compared to other retrieval-based systems (such as DrQA, HardEM, GraphRetriever, and PathRetriever), which often retrieve between 20 to 80 documents, REALM achieves the overall best performance while only retrieving 5 documents [1, 7].
*   **Comparison with Generation-based systems:** REALM is compared against concurrent work that fine-tunes T5 for Open-QA, including Base, Large, and an 11-billion parameter model [2]. 

**Evidence supporting these comparisons:**
*   The improvement over ORQA is linked to REALM's pre-training method, which can be applied to both single-corpus (X = Wikipedia, Z = Wikipedia) and separate-corpus (X = CC-News, Z = Wikipedia) settings [1].
*   Regarding retrieval efficiency, the text states that REALM gets the "overall best performance" while only retrieving 5 documents compared to the 20 to 80 documents used by other retrieval-based systems [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-10-8ea61faa3a17c1fc8f8725d8
[7] source: data/2002.08909v1

### Multi-Agent Answer

REALM outperforms all existing systems on Open-QA benchmarks [E4]. It achieves new state-of-the-art results across three benchmarks, significantly outperforming all previous systems by 4-16% absolute accuracy [E7].

The most direct comparison for REALM is ORQA (Lee et al., 2019) [E2]. The improvement of REALM over ORQA is attributed purely to better pre-training methods [E2, E4]. This is due to the fact that the fine-tuning setup, hyperparameters, and training data are identical between the two systems [E2]. Additionally, resetting both the retriever and the encoder in the REALM system reduces it to the ORQA baseline [E5].

Regarding specific performance on the NaturalQuestions-Open benchmark (79k/4k), REALM using Wikipedia for both the pre-training and knowledge corpus achieved an exact match score of 39.2 [E4]. While the provided evidence notes that REALM outperforms ORQA [E2], the specific exact match score for ORQA is not explicitly stated in the provided text [E4].

Compared to other retrieval-based systems, such as those by Asai et al. (2019) and Min et al. (2019a;b), REALM achieves its best performance while retrieving only 5 documents, whereas those other systems typically retrieve between 20 and 80 documents [E2]. REALM also outperforms the largest T5-11B model, despite being 30 times smaller [E4].

### Metrics

- baseline_latency_seconds: 6.967
- orchestrator_latency_seconds: 83.074
- baseline_total_tokens: 7685
- orchestrator_total_tokens: 52808
- baseline_citation_count: 8
- orchestrator_evidence_count: 13
- fact_check_status_counts: {'supported': 8, 'unsupported': 1}

## Question 9

Type: comparison

How does REALM's retrieval-based approach compare with storing knowledge only in model parameters?

### Baseline Answer

Compared to models that store knowledge implicitly in their parameters, REALM's retrieval-based approach offers the following differences:

*   **Interpretability and Modularity:** REALM captures knowledge in a more interpretable and modular way [1, 3]. It explicitly exposes the role of world knowledge by requiring the model to decide what knowledge to retrieve and use during inference [1]. Additionally, because REALM's memories are "grounded"—meaning each memory is associated with a specific document rather than unnamed value vectors—it provides a level of interpretability crucial for applications like Open-QA, where users require provenance for predicted answers to be trustworthy [6].
*   **Storage Constraints:** In models where knowledge is stored implicitly in parameters, storage space is limited by the size of the network; capturing more world knowledge requires training increasingly larger networks, which can be prohibitively expensive or slow [3].
*   **Knowledge Accessibility:** It is difficult to determine what knowledge is stored and where in models that rely on implicit parameter storage [3].
*   **Adaptability:** REALM can adapt to updated knowledge corpora [8]. For example, a model pre-trained on a 2018 corpus can retrieve documents from an updated 2020 corpus to generate correct tokens for information added after its original training [8].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952, chunk_index: 1
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2, chunk_index: 0
[6] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-14-83fbe5c3ec4e1ed386558b56, chunk_index: 14
[8] source: data/2002.08909

### Multi-Agent Answer

In contrast to traditional language model pre-training, which captures world knowledge implicitly within neural network parameters, REALM's retrieval-based approach captures knowledge in a more modular and interpretable way [E3, E8]. While implicit knowledge storage in parameters requires increasingly larger networks to cover more facts, REALM utilizes a latent knowledge retriever to retrieve and attend over documents from a large corpus, such as Wikipedia, during pre-training, fine-tuning, and inference [E3, E8].

Unlike models that store knowledge in parameters, REALM explicitly exposes the role of world knowledge by having the model decide what to retrieve and use during inference [E3]. This approach provides qualitative benefits in terms of modularity and interpretability [E3, E8]. Specifically, REALM's memories are "grounded," meaning each memory is associated with a specific document rather than unnamed value vectors [E5, E6]. This grounding provides a level of interpretability and provenance that is considered crucial for applications like Open-domain Question Answering (Open-QA), where users require provenance for predicted answers to be trustworthy [E5, E6].

### Metrics

- baseline_latency_seconds: 6.386
- orchestrator_latency_seconds: 71.153
- baseline_total_tokens: 7854
- orchestrator_total_tokens: 50850
- baseline_citation_count: 8
- orchestrator_evidence_count: 14
- fact_check_status_counts: {'unsupported': 4, 'supported': 2}

## Question 10

Type: evidence synthesis / ablation

What ablation or diagnostic evidence shows that retrieval pre-training improves REALM rather than only the reader component?

### Baseline Answer

To determine whether REALM pre-training improves the retriever, the encoder, or both, researchers conducted an ablation study by resetting the parameters of either the retriever or the encoder to their baseline state before fine-tuning [4].

The evidence shows the following:
*   **Both components benefit:** Both the encoder and the retriever benefit from REALM training when evaluated separately [4].
*   **Synergy is required for best results:** While both components benefit individually, the best performance requires both the encoder and retriever to act in unison [4].
*   **Specific ablation results:** In ablation experiments on the NaturalQuestions development set, the "REALM retriever + Baseline encoder" achieved an exact match score of 37.4, whereas the "Baseline retriever + REALM encoder" achieved 35.3 [8]. Both of these configurations outperformed the "Baseline (ORQA)" which had an exact match score of 31.3 [8].
*   **Isolating retriever contribution:** To more significantly isolate the specific contribution of improving the retriever during pre-training, the researchers reported how often the gold answer appears in the top-5 retrievals before any fine-tuning is applied [1, 4].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05, chunk_index: 12
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e, chunk_index: 13
[8] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-11-3fa55fc3148d1188cb70ab91, chunk_index: 11

### Multi-Agent Answer

The improvement of REALM over ORQA is attributed purely to superior pre-training methods [E5, E6]. ORQA serves as the most direct comparison to REALM because the fine-tuning setups, hyperparameters, and training data used for both are identical [E5, E6].

Diagnostic and ablation evidence regarding the model components includes:

*   **Component Benefits:** Both the encoder and the retriever receive separate benefits from REALM training, but the optimal performance is achieved when both components function in unison [E7].
*   **Isolating Retriever Contributions:** To significantly isolate the contribution of the retriever's improvement during pre-training, the metric of how often the gold answer appears in the top-5 retrievals before applying any fine-tuning is utilized [E7].

### Metrics

- baseline_latency_seconds: 6.244
- orchestrator_latency_seconds: 76.169
- baseline_total_tokens: 7977
- orchestrator_total_tokens: 55157
- baseline_citation_count: 8
- orchestrator_evidence_count: 16
- fact_check_status_counts: {'unsupported': 2, 'supported': 3}

## Question 11

Type: evidence synthesis

Synthesize the evidence for why REALM improves open-domain QA performance, including retrieval quality, pre-training, and downstream fine-tuning.

### Baseline Answer

REALM improves open-domain question answering (Open-QA) performance through the following mechanisms:

*   **Pre-training:** The improvement of REALM over direct comparisons like ORQA is attributed purely to its superior pre-training methods [1]. REALM utilizes a masked language modeling (MLM) task as an unsupervised learning signal during pre-training [4]. This process involves backpropagating through a retrieval step that considers millions of documents, rewarding the retriever when it selects documents that improve the language model's perplexity [4, 5]. Additionally, the use of a "salient span masking" scheme is described as crucial for REALM [8].
*   **Retrieval Quality:** REALM employs a neural knowledge retriever that can be trained in an unsupervised manner [4]. Unlike some other retrieval-based systems that require retrieving 20 to 80 documents, REALM achieves the overall best performance while only retrieving 5 documents [1]. Ablation studies indicate that the pre-training process improves both the encoder and the retriever, though the best results require both components to act in unison [8].
*   **Downstream Fine-tuning:** While language model pre-training typically stores knowledge implicitly in parameters, REALM's approach allows for knowledge to be captured in a more modular and interpretable way by using a learned textual knowledge retriever [4, 5]. During fine-tuning, the task shifts to Open-QA, where the model uses the retriever to find potentially relevant documents from a knowledge corpus and then attends to them to inform its prediction [2, 5]. This method allows REALM to outperform state-of-the-art models, including the 11-billion parameter T5 model, while being 30 times smaller [4].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7
[4] source: data/2002.08

### Multi-Agent Answer

REALM improves open-domain question answering (Open-QA) performance through a pre-training framework that augments language model pre-training with a learned textual knowledge retriever [E2, E6].

**Retrieval Quality**
The retriever is trained using a performance-based signal from unsupervised text [E2]. Specifically, the training objective rewards retrievals that improve the language model's perplexity and penalizes uninformative retrievals [E2]. This mechanism allows the retriever to function even when trained solely with unsupervised text [E4]. To manage the scale of millions of candidate documents, REALM utilizes Maximum Inner Product Search (MIPS) for selection, where computation for each document can be cached and updated asynchronously [E2]. Frequent index refreshes are important, as using a stale MIPS index can negatively impact model training [E4, E7].

**Pre-training**
The improvement of REALM over ORQA is attributed entirely to its better pre-training methods [E1, E3]. This pre-training method is applicable to both single-corpus settings, such as using Wikipedia for both input and knowledge, and separate-corpus settings [E1]. During pre-training, the model retrieves and marginalizes over eight candidate documents, which includes a null document [E3]. The framework also utilizes a salient span masking scheme, which is crucial for REALM's performance [E4].

**Downstream Fine-tuning**
During fine-tuning inference, REALM considers the top-5 candidates [E3, E8]. Unlike traditional models that store knowledge implicitly in parameters, REALM's approach explicitly exposes the role of world knowledge by requiring the model to decide what to retrieve and use during inference [E2].

### Metrics

- baseline_latency_seconds: 7.053
- orchestrator_latency_seconds: 89.629
- baseline_total_tokens: 8205
- orchestrator_total_tokens: 57856
- baseline_citation_count: 8
- orchestrator_evidence_count: 12
- fact_check_status_counts: {'unsupported': 3, 'supported': 9}

## Question 12

Type: multi-step reasoning

Explain step by step how a masked-language-model pre-training objective can improve downstream open-domain QA in REALM.

### Baseline Answer

In REALM, a masked-language-model (MLM) pre-training objective improves downstream open-domain question answering (Open-QA) through the following process:

1.  **Unsupervised Pre-training with MLM**: The model undergoes pre-training on an unlabeled text corpus (such as Wikipedia) using a masked language modeling objective [1]. In this task, tokens are randomly masked in a text passage, and the model is trained to predict these missing tokens [1]. 
2.  **Learning Knowledge and Representations**: To successfully predict masked tokens, the MLM must learn to encode syntactic and semantic information as well as world knowledge [1].
3.  **Joint Training of Retriever and Encoder**: REALM augments the MLM pre-training with a learned textual knowledge retriever [2]. During pre-training, the retriever and the knowledge-augmented encoder are jointly trained [4]. The model uses a "retrieve-then-predict" approach where it retrieves potentially helpful documents from a knowledge corpus and then attends over those documents to inform its prediction of the masked tokens [2, 3].
4.  **Backpropagation through Retrieval**: The signal from the MLM objective is used to train the retriever in an unsupervised manner [2]. Specifically, the model optimizes the marginal likelihood, which allows the gradient to backpropagate through the retrieval step [2, 3]. This rewards the retriever for selecting documents that improve the language model's performance (e.g., improving perplexity) and penalizes uninformative retrievals [5].
5.  **Transfer to Open-QA**: After pre-training, the parameters of the retriever and encoder are fine-tuned on the supervised Open-QA task [4]. Because the retriever was trained to find knowledge-rich documents to satisfy the MLM objective, it is designed to transfer to other tasks like Open-QA, where it must decide what knowledge to retrieve and use to answer a question [2, 5].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-2-7f240c64641ad3f52fc62e97
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-

### Multi-Agent Answer

In REALM, a masked-language-model (MLM) pre-training objective improves downstream open-domain question answering (Open-QA) through the following steps:

*   **Unsupervised Representation Learning:** The model undergoes MLM pre-training, which involves predicting the original values of missing `[MASK]` tokens in an input text passage [E1, E4]. This process allows the model to encode syntactic, semantic, and world knowledge from unlabeled text corpora [E1].
*   **Unsupervised Retriever Training:** REALM uses the MLM task as a learning signal to pre-train a latent knowledge retriever in an unsupervised manner [E2]. The retriever is trained using a performance-based signal where retrievals that improve the language model's perplexity are rewarded, while uninformative retrievals are penalized [E3].
*   **Knowledge Integration via Retrieval:** During pre-training, the model is augmented with a retriever that allows it to retrieve and attend over documents from a large corpus, such as Wikipedia [E2]. This mechanism enables the model to capture knowledge in a modular and interpretable way, rather than storing it all implicitly in the parameters of a neural network [E2].

### Metrics

- baseline_latency_seconds: 6.782
- orchestrator_latency_seconds: 88.930
- baseline_total_tokens: 9087
- orchestrator_total_tokens: 59390
- baseline_citation_count: 8
- orchestrator_evidence_count: 14
- fact_check_status_counts: {'unsupported': 6, 'supported': 6}

## Question 13

Type: multi-step reasoning / error analysis

If REALM retrieves an irrelevant document, how would that affect p(z|x), p(y|z,x), and the final answer prediction?

### Baseline Answer

If REALM retrieves an irrelevant document $z$, the effects are as follows:

*   **$p(z|x)$:** The retriever models the distribution of possibly helpful documents based on the input $x$ [3]. An irrelevant document is one that does not provide useful information for the task [4].
*   **$p(y|z,x)$:** If a document $z$ is irrelevant to $x$, it may be less useful for predicting the output $y$ than a null document ($\emptyset$) [1]. This is reflected in the Retrieval Utility (RU), where a negative RU indicates that $z$ is less useful for predicting $y$ than the null document, which can occur if $z$ is irrelevant to $x$ [1].
*   **Final answer prediction $p(y|x)$:** The overall likelihood of generating $y$ is obtained by marginalizing over all possible documents $z$: $p(y |x) = \sum_{z \in Z} p(y |z, x) p(z |x)$ [3]. In cases where REALM retrieves relevant documents with related facts, the marginalized probability of the correct answer dramatically increases [2]. Conversely, if retrieval is uninformative, it should be penalized [4].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-20-58cd33db77feaae8a3f8d036
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db5

### Multi-Agent Answer

The provided evidence does not contain specific information regarding how the retrieval of an irrelevant document affects the individual probability terms $p(z|x)$, $p(y|z,x)$, or the final answer prediction [Fact check feedback].

However, the evidence does provide information regarding the Retrieval Utility (RU) metric, which is used to measure the usefulness of a document $z$ for predicting $y$ compared to a null document $\emptyset$ [E1]. The RU is defined as $\text{RU} = \log p(y | z, x) - \log p(y | \emptyset, x)$ [E1]. A negative RU indicates that the document $z$ is less useful for predicting $y$ than the null document [E1]. One reason for a negative RU is that $z$ may be irrelevant to $x$ [E1].

### Metrics

- baseline_latency_seconds: 6.866
- orchestrator_latency_seconds: 70.960
- baseline_total_tokens: 8309
- orchestrator_total_tokens: 48083
- baseline_citation_count: 8
- orchestrator_evidence_count: 12
- fact_check_status_counts: {'unsupported': 1, 'supported': 3}

## Question 14

Type: limitation/uncertainty

What limitations, uncertainties, or missing comparisons should be noted when interpreting REALM's reported results?

### Baseline Answer

When interpreting REALM's reported results, the following limitations, uncertainties, or missing comparisons should be noted:

*   **Data Usage:** Certain types of data that could potentially benefit REALM were not used in the experiments [1].
*   **Index Staleness:** The frequency of MIPS index refreshes affects training; results suggest that a "stale index" can be detrimental to model training, and further reducing this staleness might improve optimization [4].
*   **Uncertainty in Retrieval Utility (RU):** A negative RU indicates that a retrieved document $z$ is less useful for predicting $y$ than a null document; however, this uncertainty arises because a negative RU could mean the document is irrelevant to $x$, that the masked tokens do not require world knowledge, or that the required knowledge is already sufficiently "baked into" the model's parameters [2].
*   **Missing Comparison/Context for Generation-based Models:** While the authors compare against T5 for Open-QA, they note that T5's previous experiments only focused on reading comprehension tasks where a context document is provided, rather than Open-QA [6]. Additionally, they note that the performance of GPT-2 in generating answers without context was not competitive, possibly due to a lack of fine-tuning [6].
*   **Scope of Current Work:** The presented work is described as a "minimal instantiation" of a family of REALM-like approaches, with future generalizations suggested for structured knowledge, multi-lingual settings, and multi-modal settings [5].

### Multi-Agent Answer

When interpreting REALM's reported results, the following limitations, uncertainties, and missing comparisons should be noted:

**Experimental Constraints and Data Usage**
*   The researchers noted that certain data could have potentially benefited REALM, but this data was not used in their experiments [E1].
*   The improvement of REALM over ORQA is attributed purely to better pre-training methods, as the fine-tuning setup, hyperparameters, and training data are identical [E1].

**Uncertainties in Model Behavior**
*   While the explicit retrieval system allows for adaptation to new world knowledge by modifying corpus documents, the knowledge-augmented encoder may still "remember" old knowledge [E4]. 
*   For example, the model might still predict "Thatcher" for the question "is the prime minister of United Kingdom" even after a corpus update, potentially due to her name being frequently mentioned in Wikipedia articles [E4].
*   A negative Retrieval Utility (RU) indicates that a document $z$ is less useful for predicting $y$ than the null document $\emptyset$ [E4, E8].
*   Uncertainty regarding a document's utility (a negative RU) may occur because the document is irrelevant to the query, the masked tokens do not require world knowledge to predict, or the necessary world knowledge is already "baked into" the model's parameters [E4, E8].
*   Using a stale MIPS index can negatively impact model training [E2].

### Metrics

- baseline_latency_seconds: 4.813
- orchestrator_latency_seconds: 70.479
- baseline_total_tokens: 7307
- orchestrator_total_tokens: 53228
- baseline_citation_count: 8
- orchestrator_evidence_count: 13
- fact_check_status_counts: {'supported': 5, 'unsupported': 2}

## Question 15

Type: citation grounding / uncertainty

Which claims about REALM's performance or mechanism cannot be verified unless the answer cites specific experimental evidence from the paper?

### Baseline Answer

Based on the provided text, the following claims regarding REALM's performance or mechanism cannot be verified without citing specific experimental evidence (such as results from tables or figures):

*   **Performance relative to other systems:** The claim that the improvement of REALM over ORQA is "purely due to better pre-training methods" [1].
*   **Retrieval efficiency:** The claim that REALM achieves the "overall best performance while only retrieving 5 documents" compared to other retrieval-based systems that often retrieve 20 to 80 documents [1].
*   **Component contribution:** The claim that both the encoder and retriever benefit from REALM training separately, but the "best result requires both components acting in unison" [4].
*   **Impact of masking:** The claim that salient span masking is "crucial for REALM," whereas it has not been shown to be impactful in previous work with standard BERT training [4].
*   **Index freshness:** The claim that a "stale index can hurt model training" [4].
*   **Retrieval Utility (RU) effectiveness:** The claim that RU is "more predictive of good performance on the downstream task of Open-QA than even the overall log-likelihood" [3].
*   **Benchmark superiority:** The claim that REALM outperforms all previous methods by a "significant margin (4-16% absolute accuracy)" across three popular Open-QA benchmarks [7].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-20-58cd33db77feaae8a3f8d036
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e
[7] source: data/2002.08

### Multi-Agent Answer

Based on the provided evidence, the following claims regarding REALM's performance or mechanism cannot be fully verified without specific experimental evidence or complete data:

*   **T5-11B Performance on Curated TREC:** While performance metrics are provided for REALM and T5-11B on other benchmarks, the specific accuracy score for the T5-11B model on the Curated TREC (CT) benchmark is not listed in the provided data [E4].
*   **Impact of Unused Data:** Although it is noted that certain types of data could potentially benefit REALM, such data was not used in the reported experiments, making the quantifiable impact of such data impossible to verify [E1].
*   **Detailed Comparison Against All Previous State-of-the-Art Methods:** While the evidence claims that REALM outperforms all previous state-of-the-art methods for both explicit and implicit knowledge storage [E2] and achieves the best overall performance compared to other retrieval-based systems [E1], the provided notes do not list all the specific "previous state-of-the-art methods" being compared, nor do they provide a complete side-by-side experimental breakdown for every system implied by these broad claims [E1, E2].

### Metrics

- baseline_latency_seconds: 6.458
- orchestrator_latency_seconds: 70.472
- baseline_total_tokens: 7930
- orchestrator_total_tokens: 57869
- baseline_citation_count: 8
- orchestrator_evidence_count: 12
- fact_check_status_counts: {'supported': 3, 'unsupported': 1}
