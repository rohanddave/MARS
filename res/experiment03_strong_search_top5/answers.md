# experiment03: model ablation, strong search agent only, top_k=5

## Agent Configuration

- family: model_ablation
- control_variable: search_model
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

REALM retrieves information from a large textual knowledge corpus, $Z$ [1, 3]. An example of such a corpus is Wikipedia [1, 2].

The model uses this external knowledge through a "retrieve-then-predict" generative process [1, 3]. This process involves two main steps:
1.  **Retrieve:** Given an input $x$, the model uses a learned neural knowledge retriever to retrieve potentially helpful documents $z$ from the corpus $Z$ [1, 3]. This is modeled as a sample from the distribution $p(z |x)$ [3].
2.  **Predict:** The model then conditions on both the retrieved documents $z$ and the original input $x$ to generate the output $y$, modeled as $p(y |z, x)$ [3]. The model attends over these retrieved documents to help inform its prediction [1].

This framework is used during pre-training, fine-tuning, and inference [2].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7

### Multi-Agent Answer

REALM retrieves information from a large knowledge corpus, such as Wikipedia [E2, E3]. The model can be applied in a single-corpus setting where both the pre-training and knowledge corpora are Wikipedia, or in a separate-corpus setting where the knowledge corpus is Wikipedia and the pre-training corpus is CC-News [E4].

The model uses this external knowledge through a two-step process that decomposes the generative process $p(y|x)$ [E1]:

1.  **Retrieval:** A neural knowledge retriever, modeled as $p(z|x)$, identifies potentially helpful documents ($z$) from the knowledge corpus ($Z$) [E1]. This retriever is trained using a performance-based signal from unsupervised text, which rewards retrievals that improve the language model's perplexity [E2].
2.  **Generation:** A process modeled as $p(y|z, x)$ then generates the output ($y$) by conditioning on both the input ($x$) and the retrieved documents ($z$) [E1]. During this stage, the language model attends over the retrieved documents to help inform its prediction [E2, E3].

### Metrics

- baseline_latency_seconds: 6.907
- orchestrator_latency_seconds: 56.849
- baseline_total_tokens: 5480
- orchestrator_total_tokens: 36558
- baseline_citation_count: 5
- orchestrator_evidence_count: 8
- fact_check_status_counts: {'unsupported': 2, 'supported': 6}

## Question 2

Type: easy lookup

Which downstream tasks or benchmarks does the paper use to evaluate REALM?

### Baseline Answer

The paper uses NaturalQuestions-Open to present results after ablating critical components of REALM [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05, chunk_index: 12

### Multi-Agent Answer

REALM was evaluated using three benchmarks: NATURAL QUESTIONS, WEB QUESTIONS, and CURATED TREC [E5]. Through these evaluations, the paper reports that REALM achieves new state-of-the-art results on Open-domain Question Answering (Open-QA) benchmarks [E5].

### Metrics

- baseline_latency_seconds: 3.120
- orchestrator_latency_seconds: 25.052
- baseline_total_tokens: 4202
- orchestrator_total_tokens: 18090
- baseline_citation_count: 5
- orchestrator_evidence_count: 9
- fact_check_status_counts: {'supported': 2}

## Question 3

Type: definition

What is REALM, and what does the paper mean by retrieval-augmented language model pre-training?

### Baseline Answer

REALM stands for Retrieval-Augmented Language Model pre-training [1, 2]. It is a framework designed to capture knowledge in a way that is more modular and interpretable than traditional models that store knowledge implicitly in their parameters [1, 2].

Retrieval-augmented language model pre-training refers to a method that augments language model pre-training algorithms with a learned textual knowledge retriever [1]. Instead of relying solely on internal parameters, this approach explicitly exposes the role of world knowledge by requiring the model to decide what knowledge to retrieve and use during inference [1]. The process works as follows:

*   **Mechanism:** Before making a prediction, the language model uses a retriever to pull documents from a large corpus (such as Wikipedia) and attends over those documents to inform its prediction [1].
*   **Learning Signal:** The retriever is trained using a performance-based signal from unsupervised text [1]. Specifically, a retrieval that improves the language model's perplexity is rewarded, while uninformative retrievals are penalized [1].
*   **Pre-training Task:** During pre-training, the specific task used is masked language modeling, where the model must predict the value of missing tokens in a sentence [2].
*   **Generative Process:** The process is modeled as a "retrieve-then-predict" approach, where the model first retrieves potentially helpful documents $z$ from a knowledge corpus $Z$ given an input $x$, and then conditions on both the retrieved documents and the original input to generate the output $y$ [2].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2; chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7

### Multi-Agent Answer

REALM (Retrieval-Augmented Language Model) is a pre-training approach designed to capture world knowledge in a more modular and interpretable way than traditional language model pre-training [E6]. While standard language model pre-training stores knowledge implicitly within neural network parameters—making it difficult to determine what is stored or where [E6]—REALM augments the process with a latent knowledge retriever [E6]. This retriever allows the model to retrieve and attend over documents from a large corpus, such as Wikipedia, during pre-training, fine-tuning, and inference [E6]. A key feature of REALM is that its memories are "grounded," meaning each memory is associated with a specific document rather than unnamed value vectors, which provides the provenance necessary for applications like Open-domain Question Answering (Open-QA) [E1].

Retrieval-augmented language model pre-training refers to the method of augmenting language model pre-training with this latent knowledge retriever [E6]. In this framework, the model uses masked language modeling as an unsupervised learning signal to pre-train the knowledge retriever [E6]. This retrieval step can consider millions of documents [E6].

### Metrics

- baseline_latency_seconds: 7.896
- orchestrator_latency_seconds: 33.280
- baseline_total_tokens: 5734
- orchestrator_total_tokens: 21396
- baseline_citation_count: 5
- orchestrator_evidence_count: 9
- fact_check_status_counts: {'supported': 8}

## Question 4

Type: definition

How does REALM differ from a standard parametric language model such as BERT in where knowledge is stored and accessed?

### Baseline Answer

Standard parametric language models, such as BERT, store learned world knowledge implicitly within the parameters of the underlying neural network [1]. This implicit storage makes it difficult to determine what knowledge is stored and where, and requires ever-larger networks to capture more facts because storage space is limited by the size of the network [1].

In contrast, REALM (Retrieval-Augmented Language Model) differs in the following ways:

*   **Storage:** Instead of relying solely on parameters, REALM uses a learned textual knowledge retriever to access knowledge from a large external corpus, such as Wikipedia [1, 2].
*   **Access:** Before making a prediction, the model uses the retriever to retrieve documents from the knowledge corpus and then attends over those documents to inform its prediction [2].
*   **Characteristics:** This approach allows knowledge to be captured in a more modular and interpretable way [1, 2]. Unlike standard models, REALM's "memories" are grounded, meaning each memory is associated with a specific document rather than unnamed value vectors [3].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-15-e73576ceacc6e97a0666fd10

### Multi-Agent Answer

Standard parametric language models store world knowledge implicitly within the parameters of a neural network [E3]. This method of implicit storage requires increasingly larger networks to cover more facts [E3].

In contrast, REALM captures knowledge in a more modular and interpretable way by using a learned textual knowledge retriever [E2, E3]. This framework allows the model to retrieve and attend over documents from a large corpus, such as Wikipedia, during pre-training, fine-tuning, and inference [E3]. During inference, REALM explicitly exposes the role of world knowledge by requiring the model to decide what to retrieve and use [E2].

### Metrics

- baseline_latency_seconds: 5.442
- orchestrator_latency_seconds: 59.725
- baseline_total_tokens: 6558
- orchestrator_total_tokens: 40834
- baseline_citation_count: 5
- orchestrator_evidence_count: 10
- fact_check_status_counts: {'supported': 4, 'unsupported': 2}

## Question 5

Type: method/mechanism

How does REALM's retrieve-then-predict framework work, including the role of the latent document variable z?

### Baseline Answer

REALM's retrieve-then-predict framework decomposes the probability of an output $p(y | x)$ into two distinct steps:

1.  **Retrieve**: Given an input $x$, the model first retrieves potentially helpful documents $z$ from a knowledge corpus $Z$ [3]. This is modeled as sampling from the distribution $p(z | x)$ [3].
2.  **Predict**: The model then conditions on both the original input $x$ and the retrieved document $z$ to generate the output $y$, modeled as $p(y | z, x)$ [3].

The role of the latent document variable $z$ is to allow the model to obtain the overall likelihood of generating $y$ by marginalizing over all possible documents in the corpus $Z$ [3]. This is expressed mathematically as:
$p(y | x) = \sum_{z \in Z} p(y | z, x) p(z | x)$ [3].

By treating $z$ as a latent variable, the framework can be optimized by maximizing the marginal likelihood [1]. This approach allows the model to use the retrieved documents to inform its predictions, such as using a document to help fill in masked tokens during pre-training [1, 4].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-13-8b5179bb43546a69e37d136e

### Multi-Agent Answer

REALM (Retrieval-Augmented Language Model) utilizes a "retrieve-then-predict" framework that decomposes the generative process $p(y|x)$ into two distinct steps [E3]. In this framework, the model first uses a learned textual knowledge retriever to retrieve documents from a large corpus, such as Wikipedia [E1, E2]. The language model then attends over these retrieved documents to help inform its prediction [E1].

The framework models this retrieve-then-predict method as a latent variable language model [E1]. The role of the latent document variable $z$ is to represent the retrieved documents from a knowledge corpus $Z$ [E3]. The model learns the overall likelihood of generating an output $y$ for an input $x$ by treating $z$ as a latent variable and marginalizing over all possible documents $z$ [E3]. This is achieved by first modeling the retrieval of documents $z$ given an input $x$ as $p(z|x)$, and then conditioning on both the input $x$ and the retrieved documents $z$ to generate the output $y$, modeled as $p(y|z, x)$ [E3].

### Metrics

- baseline_latency_seconds: 5.750
- orchestrator_latency_seconds: 57.232
- baseline_total_tokens: 5604
- orchestrator_total_tokens: 36401
- baseline_citation_count: 5
- orchestrator_evidence_count: 8
- fact_check_status_counts: {'supported': 6, 'unsupported': 1}

## Question 6

Type: method/mechanism

How does the paper train the retriever when the retrieved document is latent, and how does learning signal flow back to retrieval?

### Baseline Answer

When the retrieved document is treated as a latent variable, the paper trains the retriever by modeling the "retrieve-then-predict" approach as a latent variable language model and optimizing the marginal likelihood [1]. Specifically, the model calculates the overall likelihood of generating an output $y$ from an input $x$ by marginalizing over all possible documents $z$ in the corpus $Z$, using the formula $p(y |x) = \sum_{z \in Z} p(y |z, x) p(z |x)$ [4].

The learning signal flows back to the retrieval module through backpropagation from the language modeling objective [2]. The intuition behind this signal is performance-based: a retrieval that improves the language model's perplexity is considered helpful and rewarded, whereas an uninformative retrieval should be penalized [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952, chunk_index: 1
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2, chunk_index: 0
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7, chunk_index: 3

### Multi-Agent Answer

The REALM framework models the retrieve-then-predict approach as a latent variable language model [E1]. The retriever is trained using a performance-based signal derived from unsupervised text [E1]. Specifically, the training process rewards retrievals that improve the language model's perplexity and penalizes uninformative retrievals [E1]. During pre-training, the model can be trained in an unsupervised manner by using masked language modeling as the learning signal [E2].

The learning signal flows back to the retriever via backpropagation through a retrieval step that considers an entire corpus of textual knowledge [E1][E2]. To manage the computational challenges of backpropagating through a retriever that considers millions of documents, the retriever is structured so that computation can be cached or updated asynchronously, and document selection is formulated as Maximum Inner Product Search (MIPS) [E1].

### Metrics

- baseline_latency_seconds: 5.035
- orchestrator_latency_seconds: 28.469
- baseline_total_tokens: 5378
- orchestrator_total_tokens: 20957
- baseline_citation_count: 5
- orchestrator_evidence_count: 9
- fact_check_status_counts: {'supported': 6}

## Question 7

Type: method/mechanism / implementation

What approximations or engineering choices does REALM use to make retrieval over a large corpus practical during training and inference?

### Baseline Answer

To make retrieval over a large corpus practical during training and inference, REALM employs the following engineering choices and approximations:

*   **Retriever Structure and Search:** The retriever is structured so that the computation for each document can be cached and updated asynchronously [2]. Additionally, the selection of the best documents is formulated as a Maximum Inner Product Search (MIPS) [2].
*   **Parallelization and Indexing:** During pre-training, the document embedding step for the MIPS index is parallelized over 16 TPUs [4]. To maintain the index, a parallel process runs to re-embed corpus documents and rebuild the MIPS index, resulting in an index refresh approximately every 500 training steps [5].
*   **Candidate Selection/Marginalization:** 
    *   **During Pre-training:** For each example, the system retrieves and marginalizes over 8 candidate documents, which includes a null document $\emptyset$ [4].
    *   **During Fine-tuning Inference:** The system considers only the top-5 candidate documents [1, 4].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05, chunk_index: 12
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952, chunk_index: 1
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-11-3fa55fc3148d1188cb70ab91, chunk_index: 11
[5] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136

### Multi-Agent Answer

To manage the computational challenges of considering millions of candidate documents, REALM employs several engineering choices and approximations:

*   **Document Selection:** The retriever uses Maximum Inner Product Search (MIPS) for document selection [E1].
*   **Computational Structure:** The retriever is structured so that computation can be cached and updated asynchronously [E1]. 
*   **Parallelization:** The document embedding step for the MIPS index is parallelized over 16 TPUs [E3].
*   **Candidate Pruning during Inference:** During fine-tuning inference, the system considers only the top-5 candidates [E3]. 
*   **Marginalization:** For each example, the model retrieves and marginalizes over 8 candidate documents, which includes a null document $\emptyset$ [E3].

### Metrics

- baseline_latency_seconds: 7.299
- orchestrator_latency_seconds: 30.795
- baseline_total_tokens: 5668
- orchestrator_total_tokens: 21525
- baseline_citation_count: 5
- orchestrator_evidence_count: 5
- fact_check_status_counts: {'supported': 5}

## Question 8

Type: comparison

How does REALM compare with ORQA or other open-domain QA baselines, and what evidence supports that comparison?

### Baseline Answer

REALM compares to ORQA and other baselines as follows:

*   **Comparison with ORQA:** ORQA is considered the most direct comparison to REALM because the fine-tuning setup, training data, and hyperparameters are identical [1]. The improvement REALM achieves over ORQA is attributed solely to superior pre-training methods [1]. Evidence for this is found through ablation studies: resetting both the retriever and encoder parameters to their baseline state reduces the system to the ORQA baseline [5].
*   **Comparison with other retrieval-based systems:** Compared to other retrieval-based systems (such as Asai et al., 2019; Min et al., 2019a;b), which typically retrieve between 20 to 80 documents, REALM achieves the best overall performance while only retrieving 5 documents [1].
*   **Comparison with generation-based systems:** REALM is compared against state-of-the-art systems from the generation-based paradigm [4]. For the most competitive and comparable generation-based baseline, REALM is compared against concurrent work that fine-tunes T5 for Open-QA [2].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-10-8ea61faa3a17c1fc8f8725d8
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7
[5] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e

### Multi-Agent Answer

REALM demonstrates superior performance compared to ORQA and other retrieval-based systems [E1].

**Comparison with ORQA**
ORQA is considered the most direct comparison to REALM because both systems utilize identical training data, hyperparameters, and fine-tuning setups [E1][E3]. The improvement seen in REALM over ORQA is attributed entirely to superior pre-training methods [E1][E3]. Additionally, the retrievers for both REALM pre-training and ORQA are initialized using the Inverse Cloze Task [E2].

**Comparison with Other Baselines**
Among all retrieval-based systems, REALM achieves the best overall performance despite retrieving fewer documents [E1]. While other retrieval-based systems often retrieve a range of 20 to 80 documents, REALM achieves its best overall performance by retrieving only 5 documents [E1]. Furthermore, REALM outperforms the T5-11B model, even though REALM is 30 times smaller [E3].

### Metrics

- baseline_latency_seconds: 7.149
- orchestrator_latency_seconds: 60.350
- baseline_total_tokens: 5298
- orchestrator_total_tokens: 36101
- baseline_citation_count: 5
- orchestrator_evidence_count: 6
- fact_check_status_counts: {'supported': 7}

## Question 9

Type: comparison

How does REALM's retrieval-based approach compare with storing knowledge only in model parameters?

### Baseline Answer

REALM's retrieval-based approach differs from models that store knowledge only in their parameters in several ways:

*   **Interpretability and Modularity:** REALM captures knowledge in a more modular and interpretable way compared to models that store knowledge implicitly in their parameters [1, 3]. This approach explicitly exposes the role of world knowledge by requiring the model to decide what knowledge to retrieve and use during inference [1]. Furthermore, REALM's "memories" are grounded, meaning each memory is associated with a document rather than unnamed value vectors, which provides the provenance necessary for trustworthy predictions in tasks like Open-QA [5].
*   **Storage and Scalability:** In models where knowledge is stored implicitly in parameters, it is difficult to determine what knowledge is stored and where [3]. Additionally, the storage space in such models is limited by the size of the network; capturing more world knowledge requires training increasingly larger networks, which can be expensive or prohibitively slow [3].
*   **Performance:** When evaluated on three popular Open-domain Question Answering (Open-QA) benchmarks, REALM outperformed state-of-the-art models that store knowledge implicitly (such as T5) by a margin of 4-16% in absolute accuracy [1, 3].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952, chunk_index: 1
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2, chunk_index: 0
[5] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-15-e73576ceacc6e97a0666fd10, chunk_index: 15

### Multi-Agent Answer

Standard language model pre-training captures world knowledge implicitly within the parameters of a neural network [E4]. This implicit storage method requires increasingly larger networks to cover a greater number of facts [E4].

In contrast, REALM's retrieval-based approach augments language model pre-training with a learned textual knowledge retriever to capture knowledge in a more modular and interpretable way [E2, E4]. Rather than relying solely on stored parameters, REALM explicitly exposes the role of world knowledge by requiring the model to decide what to retrieve and use during inference [E2]. Before making a prediction, the model uses the retriever to select documents from a large corpus, such as Wikipedia, and attends over those documents to inform its prediction [E2].

REALM's approach also provides specific advantages regarding interpretability and grounding. Unlike models that use unnamed value vectors, REALM's memories are grounded, meaning each memory is associated with a specific document [E5]. This grounding provides a level of interpretability and provenance that is necessary for users to trust predicted answers in Open-QA applications [E5].

### Metrics

- baseline_latency_seconds: 6.289
- orchestrator_latency_seconds: 55.431
- baseline_total_tokens: 5560
- orchestrator_total_tokens: 36328
- baseline_citation_count: 5
- orchestrator_evidence_count: 9
- fact_check_status_counts: {'supported': 6, 'unsupported': 2}

## Question 10

Type: evidence synthesis / ablation

What ablation or diagnostic evidence shows that retrieval pre-training improves REALM rather than only the reader component?

### Baseline Answer

To determine whether REALM pre-training improves the retriever, the encoder, or both, the researchers conducted an ablation where they reset the parameters of either the retriever or the encoder to their baseline state before fine-tuning [4]. 

The diagnostic evidence shows that:
*   Both the encoder and the retriever benefit from REALM training when they are improved separately [4].
*   The best results are achieved when both components act in unison [4].
*   Resetting both the retriever and the encoder reduces the system to the main baseline, ORQA [4].
*   The frequency with which the "gold answer" appears in the top-5 retrievals before any fine-tuning is applied serves as a metric that more significantly isolates the contribution of improving the retriever during pre-training [1, 4].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e

### Multi-Agent Answer

The provided evidence does not contain specific ablation or diagnostic results that isolate the improvements of the retrieval pre-training from the reader component.

However, the evidence does provide a comparison between REALM and ORQA to support the impact of pre-training [E2]. The improvement of REALM over ORQA is attributed purely to better pre-training methods, as the fine-tuning setups, hyperparameters, and training data are identical [E2]. Regarding the mechanism of REALM's pre-training, the retriever is trained using a performance-based signal from unsupervised text, where retrievals that improve the language model's perplexity are rewarded [E4]. The signal from the language modeling objective backpropagates through the retriever [E1].

### Metrics

- baseline_latency_seconds: 4.473
- orchestrator_latency_seconds: 57.961
- baseline_total_tokens: 4551
- orchestrator_total_tokens: 38832
- baseline_citation_count: 5
- orchestrator_evidence_count: 10
- fact_check_status_counts: {'unsupported': 2, 'supported': 3}

## Question 11

Type: evidence synthesis

Synthesize the evidence for why REALM improves open-domain QA performance, including retrieval quality, pre-training, and downstream fine-tuning.

### Baseline Answer

REALM improves open-domain question answering (Open-QA) performance through the following mechanisms:

*   **Pre-training:** REALM augments language model pre-training with a learned textual knowledge retriever [4]. This retriever is trained in an unsupervised manner using masked language modeling as the learning signal [4]. The key intuition is to use a performance-based signal from unsupervised text: the retriever is rewarded if it selects documents that improve the language model's perplexity [5]. This pre-training method can be applied in both single-corpus (e.g., Wikipedia to Wikipedia) and separate-corpus (e.g., CC-News to Wikipedia) settings [1].
*   **Retrieval Quality:** Unlike previous systems that used non-learned or heuristic retrievers [4, 5], REALM uses a neural knowledge retriever that is trained end-to-end by backpropagating through a retrieval step that considers millions of documents [4]. This improves the retriever's ability to find relevant information; for example, the improvement of REALM over ORQA is attributed purely to these better pre-training methods [1]. Additionally, REALM achieves state-of-the-art performance while only needing to retrieve 5 documents, whereas other retrieval-based systems often retrieve between 20 and 80 documents [1].
*   **Downstream Fine-tuning:** REALM's retriever is specifically designed to transfer to other tasks because it retrieves raw text rather than labeled examples [5]. When fine-tuned on Open-QA benchmarks, REALM outperformed all previous methods by a significant margin of 4-16% absolute accuracy [4, 5].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[5] source: data/2002.08909v1.pdf, chunk_id: 2002.0

### Multi-Agent Answer

REALM improves open-domain question answering (Open-QA) performance through a retrieval-augmented pre-training framework that enhances retrieval quality, leverages unsupervised pre-training, and improves downstream fine-tuning [E3].

**Retrieval Quality**
REALM utilizes an architecture consisting of two key components: a neural knowledge retriever and a knowledge-augmented encoder [E4]. The retriever is defined using a dense inner product model where the relevance score is the inner product of vector embeddings [E4]. This retriever can access documents from a large corpus, such as Wikipedia, during pre-training, fine-tuning, and inference [E3]. While other retrieval-based systems typically retrieve between 20 and 80 documents, REALM achieves the overall best performance among compared systems despite retrieving only 5 documents [E1].

**Pre-training**
The improvement of REALM over ORQA is attributed purely to its superior pre-training methods [E1]. REALM allows for unsupervised pre-training of the knowledge retriever by using masked language modeling (MLM) as the learning signal [E3]. This pre-training process involves backpropagating through a retrieval step that considers millions of documents [E3]. The goal of language model pre-training is to learn useful representations of language from unlabeled text corpora, which can lead to better generalization for downstream tasks than training from scratch [E2]. Specifically, the MLM variant is used to learn syntactic, semantic, and world knowledge by predicting missing tokens [E2].

**Downstream Fine-tuning**
REALM demonstrates its effectiveness by fine-tuning on the challenging task of Open-QA [E3]. This fine-tuning process involves predicting an answer $y$ from a question $x$ [E4]. Through this approach, REALM achieves new state-of-the-art results across three benchmarks, outperforming previous systems by 4-16% absolute accuracy [E2][E3].

### Metrics

- baseline_latency_seconds: 7.528
- orchestrator_latency_seconds: 60.553
- baseline_total_tokens: 4915
- orchestrator_total_tokens: 34174
- baseline_citation_count: 5
- orchestrator_evidence_count: 7
- fact_check_status_counts: {'supported': 12}

## Question 12

Type: multi-step reasoning

Explain step by step how a masked-language-model pre-training objective can improve downstream open-domain QA in REALM.

### Baseline Answer

The masked-language-model (MLM) pre-training objective improves downstream open-domain question answering (Open-QA) in REALM through the following process:

1.  **Unsupervised Pre-training with Latent Retrieval:** REALM augments standard language model pre-training by adding a learned textual knowledge retriever [2]. During pre-training, the model performs a "retrieve-then-predict" generative process using an unsupervised masked language modeling task [3].
2.  **Generating Training Examples:** Training examples are generated from an unlabeled pre-training corpus by randomly masking tokens in a sampled piece of text [1]. The model's task is to predict the values of these missing tokens ($y$) [3, 4].
3.  **Learning via Performance-Based Signals:** The retriever is trained using a performance-based signal from the unsupervised text [5]. A retrieval that improves the language model's perplexity is rewarded, while uninformative retrievals are penalized [5]. This is achieved by modeling the approach as a latent variable language model and optimizing the marginal likelihood [5].
4.  **End-to-End Optimization:** Because both the knowledge retriever and the knowledge-augmented encoder are differentiable neural networks, the signal from the MLM objective can be backpropagated all the way through the retrieval step [2, 5]. This allows the retriever to learn how to select documents from a large corpus (such as Wikipedia) that are helpful for predicting masked tokens [2, 5].
5.  **Knowledge Capture and Transfer:** While standard language models store world knowledge implicitly in their parameters, REALM's retriever is designed to capture knowledge in a more modular and interpretable way by retrieving and attending over documents [2]. The retriever is trained to transfer to other tasks because it retrieves raw text rather than task-specific labeled examples [5].
6.  **Fine-tuning for Open-QA:** Once pre-trained, the retriever and encoder parameters are fine-tuned on the supervised Open-QA task, where the input is a question and the target is the correct answer string [3, 4].

Citations:
[1] data/2002.08909v1.pdf (chunk_id: 2002.08909v1-2-7f240c64641ad3f52fc62e97)
[2] data

### Multi-Agent Answer

In REALM, a masked-language-model (MLM) pre-training objective improves downstream open-domain question answering (Open-QA) through the following process:

1.  **Learning Representations and Knowledge:** The model utilizes the MLM variant of pre-training, where it is trained to predict missing tokens within an input text passage [E1]. This task helps the model learn to encode syntactic information, semantic information, and world knowledge from unlabeled text corpora [E1].
2.  **Unsupervised Retriever Training:** During pre-training, the MLM objective serves as an unsupervised learning signal used to train a latent knowledge retriever [E2]. The retriever is trained using a performance-based signal where retrievals that improve the language model's perplexity are rewarded, while uninformative retrievals are penalized [E4].
3.  **Backpropagation through Retrieval:** The learning signal from the language modeling objective is backpropagated through the retrieval step [E2]. This mechanism allows the model to learn to retrieve and attend over documents from a large corpus, such as Wikipedia, to assist in its predictions [E2].
4.  **Transfer to Downstream Open-QA:** The pre-trained model, which has learned useful representations and how to utilize a retriever, can then be further trained (fine-tuned) for the downstream task of Open-QA [E1]. This pre-training approach often leads to better generalization for the downstream task than training from scratch [E1].

### Metrics

- baseline_latency_seconds: 7.512
- orchestrator_latency_seconds: 62.465
- baseline_total_tokens: 5874
- orchestrator_total_tokens: 37979
- baseline_citation_count: 5
- orchestrator_evidence_count: 11
- fact_check_status_counts: {'unsupported': 4, 'supported': 8}

## Question 13

Type: multi-step reasoning / error analysis

If REALM retrieves an irrelevant document, how would that affect p(z|x), p(y|z,x), and the final answer prediction?

### Baseline Answer

If REALM retrieves an irrelevant document, the effects on the components are as follows:

*   **$p(z|x)$**: The retrieval process models $p(z|x)$ as a sample from a distribution derived from the softmax over all relevance scores [3]. An irrelevant document would have a lower relevance score $f(x, z)$ (defined as the inner product of the vector embeddings) compared to relevant documents [3].
*   **$p(y|z,x)$**: The Retrieval Utility (RU) is used to measure the "usefulness" of a document $z$ for predicting $y$ [1]. A negative RU indicates that $z$ is less useful for predicting $y$ than the null document, which could mean that $z$ is irrelevant to $x$ [1].
*   **Final answer prediction ($p(y|x)$)**: REALM obtains the overall likelihood of generating $y$ by treating $z$ as a latent variable and marginalizing over all possible documents $z$ [3]. The model is trained such that a retrieval that improves the language model's perplexity is rewarded, while an uninformative retrieval should be penalized [4]. Because the marginalized probability $p(y|x)$ is the sum of the products of the conditional probability $p(y|z, x)$ and the retrieval distribution $p(z|x)$, retrieving documents with related facts is what allows the marginalized probability of the correct answer to increase [2].

### Multi-Agent Answer

The provided evidence does not explicitly detail how an irrelevant document specifically changes the individual values of $p(z|x)$ and $p(y|z,x)$ in a single step. However, the components and their relationships are defined as follows:

*   **$p(z|x)$ (The Retriever):** This term represents the neural knowledge retriever, which models the probability of retrieving a document $z$ given an input $x$ [E4]. The retriever uses a dense inner product model where the relevance score $f(x, z)$ is the inner product of the vector embeddings [E4].
*   **$p(y|z,x)$ (The Knowledge-Augmented Encoder):** This term represents the probability of predicting the output $y$ conditioned on both the input $x$ and the retrieved document $z$ [E4]. If a document $z$ is irrelevant, it may result in a negative Retrieval Utility (RU), which indicates that $z$ is less useful for predicting $y$ than the null document $\emptyset$ [E1, E5].
*   **Final Answer Prediction:** REALM decomposes the process of learning the distribution $p(y|x)$ into two distinct steps: "retrieve, then predict" [E4]. The overall likelihood of generating $y$ is modeled by treating the retrieved document $z$ as a latent variable: $p(y|x) = \sum_{z \in Z} p(y|z, x)p(z|x)$ [E4].

### Metrics

- baseline_latency_seconds: 4.279
- orchestrator_latency_seconds: 69.479
- baseline_total_tokens: 4865
- orchestrator_total_tokens: 38881
- baseline_citation_count: 5
- orchestrator_evidence_count: 9
- fact_check_status_counts: {'unsupported': 2, 'supported': 5}

## Question 14

Type: limitation/uncertainty

What limitations, uncertainties, or missing comparisons should be noted when interpreting REALM's reported results?

### Baseline Answer

When interpreting REALM's reported results, the following limitations, uncertainties, and missing comparisons should be noted:

*   **Uncertainty in Retrieval Utility (RU):** A negative RU indicates that the document $z$ is less useful for predicting $y$ than a null document [2]. However, this could mean several different things: that $z$ is irrelevant to $x$, that the masked tokens in $x$ do not require world knowledge for prediction, or that the required world knowledge is already sufficiently commonplace and has been "baked into the model's parameters" [2].
*   **Impact of Index Staleness:** The staleness of a MIPS index can hurt model training, and the text suggests that further reducing this staleness could potentially offer better optimization [4].
*   **Missing Data Usage:** Certain data could have benefited REALM but was not utilized in the experiments [1].
*   **Sensitivity to Masking:** The latent variable learning process is sensitive to the learning signal and relies heavily on the utility of retrieval, which is impacted by the choice of masking [2, 4].
*   **Comparison with Other Systems:** While REALM's most direct comparison is with ORQA (where the improvement is attributed purely to better pre-training methods), REALM's performance is noted in contrast to other retrieval-based systems that retrieve 20 to 80 documents, whereas REALM achieves its performance by only retrieving 5 documents [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-20-58cd33db77feaae8a3f8d036
[4] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e

### Multi-Agent Answer

When interpreting REALM's reported results, several limitations, uncertainties, and missing comparisons should be noted:

*   **Experimental Scope and Data:** Certain types of data that could potentially benefit REALM were not used in the reported experiments [E1].
*   **Interpretation of Retrieval Utility (RU):** A negative RU does not definitively prove a document is irrelevant; it may instead indicate that the masked tokens do not require world knowledge or that the necessary knowledge is already embedded within the model's parameters [E4].
*   **Model Training Sensitivities:** The effectiveness of latent variable learning relies heavily on the utility of retrieval, which makes the process more sensitive to a consistent learning signal [E2]. Additionally, using a stale MIPS index can negatively impact model training [E2].
*   **Component Interdependence:** While both the encoder and retriever benefit separately from REALM training, achieving optimal results requires both components to act in unison [E2].
*   **Baseline Comparisons:** Regarding generation-based Open-QA, GPT-2's performance was not competitive, which may be due to a lack of fine-tuning [E5].

### Metrics

- baseline_latency_seconds: 6.848
- orchestrator_latency_seconds: 32.530
- baseline_total_tokens: 4624
- orchestrator_total_tokens: 19279
- baseline_citation_count: 5
- orchestrator_evidence_count: 8
- fact_check_status_counts: {'supported': 7}

## Question 15

Type: citation grounding / uncertainty

Which claims about REALM's performance or mechanism cannot be verified unless the answer cites specific experimental evidence from the paper?

### Baseline Answer

Based on the provided context, the following claims about REALM's performance or mechanism cannot be verified without citing specific experimental evidence (such as specific tables or figures) mentioned in the text:

*   **Performance relative to ORQA:** While it is claimed that the improvement of REALM over ORQA is "purely due to better pre-training methods" [1], the specific magnitude or data supporting this comparison requires the context of the identical fine-tuning setup, hyperparameters, and training data mentioned in that same section [1].
*   **Retrieval efficiency:** The claim that REALM achieves the "overall best performance while only retrieving 5 documents" compared to other retrieval-based systems that retrieve 20 to 80 documents [1] requires the specific experimental results to be verified.
*   **Ablation study results:** The effectiveness of ablating critical components of REALM and the specific metric regarding how often the "gold answer appears in the top-5 retrievals" [1, 4] relies on data presented in "Table 2," which is not fully provided in the text.
*   **Encoder vs. Retriever benefit:** The claim that "both the encoder and retriever benefit from REALM training separately, but the best result requires both components acting in unison" [4] requires the experimental results described in the "Encoder or Retriever" analysis.
*   **MIPS index refresh rate:** The claim that a "stale index can hurt model training" [4] is supported by results in "Table 2," which is not provided.
*   **Retrieval Utility (RU) behavior:** The claim that RU "increases steadily over the course of pre-training" and is "more predictive of good performance on the downstream task of Open-QA than even the overall log-likelihood" [3] requires verification via the data in "Figure 4" and the associated equations [3].
*   **Masked language model prediction:** The claim that REALM assigns a "much higher probability" to a correct term (e.g., "Fermat") compared to BERT [4] requires the specific data provided in "Table 3" [4].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23

### Multi-Agent Answer

Based on the provided evidence, the following claims regarding REALM's performance or mechanism cannot be verified as the specific experimental data is missing:

*   **Comparative performance between corpus settings:** While the REALM pre-training method is applicable to both single-corpus settings (where X = Wikipedia and Z = Wikipedia) and separate-corpus settings (where X = CC-News and Z = Wikipedia) [E1], the provided notes do not include numerical data or a comparison of the degree of performance gain between these two specific configurations [E1].
*   **Optimal refresh rate for MIPS:** It is noted that asynchronous MIPS (Maximum Inner Product Search) refreshes lead to stable optimization if they occur at a "sufficiently frequent rate" [E5], but the evidence does not specify the exact frequency or threshold required to maintain this stability [E5].

### Metrics

- baseline_latency_seconds: 6.800
- orchestrator_latency_seconds: 46.381
- baseline_total_tokens: 4619
- orchestrator_total_tokens: 33187
- baseline_citation_count: 5
- orchestrator_evidence_count: 10
- fact_check_status_counts: {'supported': 2}
