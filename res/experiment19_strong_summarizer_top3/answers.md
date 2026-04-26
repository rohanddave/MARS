# experiment19: retrieval sweep, strong summarizer only, top_k=3

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

The model uses this corpus through a "retrieve-then-predict" process [3]:
* **Retrieval:** Given an input $x$, the model uses a learned textual knowledge retriever to retrieve potentially helpful documents $z$ from the corpus $Z$ [1, 3]. This is modeled as a sample from the distribution $p(z | x)$ [3]. The retriever uses a dense inner product model where the relevance score between the input and a document is the inner product of their vector embeddings [3].
* **Prediction:** The model then conditions on both the original input $x$ and the retrieved documents $z$ to generate an output $y$ (mode-led as $p(y | z, x)$) [3]. The language model attends over the retrieved documents to help inform its prediction [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7

### Multi-Agent Answer

REALM retrieves information from a large knowledge corpus, such as Wikipedia [E2, E3]. Within this context, the term "document" is used loosely to refer to a passage from the knowledge corpus rather than necessarily a whole article [E1].

The model uses this retrieved knowledge through a two-step decomposition of the output distribution $p(y|x)$ [E1]:

1.  **Retrieval:** The model uses a learned neural knowledge retriever to retrieve documents $z$ from a corpus $Z$ based on the input $x$ [E1]. This retriever employs BERT-style Transformers for its embedding functions [E1] and uses Maximum Inner Product Search (MIPS) to manage the computational challenge of selecting from millions of documents [E2].
2.  **Generation/Prediction:** The model then generates an output $y$ based on both the retrieved documents and the original input $x$, specifically $p(y|z, x)$ [E1]. This process involves the language model attending over the retrieved documents to help inform its prediction [E2].

### Metrics

- baseline_latency_seconds: 6.539
- orchestrator_latency_seconds: 43.515
- baseline_total_tokens: 3791
- orchestrator_total_tokens: 26166
- baseline_citation_count: 3
- orchestrator_evidence_count: 8
- fact_check_status_counts: {'unsupported': 3, 'supported': 6}

## Question 2

Type: easy lookup

Which downstream tasks or benchmarks does the paper use to evaluate REALM?

### Baseline Answer

The paper evaluates REALM using the NaturalQuestions-Open benchmark [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05, chunk_index: 12

### Multi-Agent Answer

The provided evidence does not explicitly list the specific downstream tasks or benchmarks used to evaluate REALM's performance. While the notes mention that the grounded nature of REALM's memory is essential for applications like Open-QA [E3], and that ORQA is the most direct comparison for REALM among retrieval-based systems [E1], they do not specify which datasets (such as SQuAD or Natural Questions) were used for these evaluations. The only specific dataset mentioned is CoNLL-2003, which was used to train a BERT-based tagger for identifying named entities rather than as a downstream evaluation benchmark for REALM [E2].

### Metrics

- baseline_latency_seconds: 2.953
- orchestrator_latency_seconds: 35.008
- baseline_total_tokens: 2293
- orchestrator_total_tokens: 20658
- baseline_citation_count: 3
- orchestrator_evidence_count: 5
- fact_check_status_counts: {'unsupported': 1, 'supported': 3}

## Question 3

Type: definition

What is REALM, and what does the paper mean by retrieval-augmented language model pre-training?

### Baseline Answer

REALM (Retrieval-Augmented Language Model) is a novel framework designed to capture knowledge in a more modular and interpretable way than traditional models that store knowledge implicitly in their parameters [1, 2]. Instead of relying solely on internal parameters, REALM augments language model pre-training with a learned textual knowledge retriever [1, 2]. This approach explicitly exposes the role of world knowledge by requiring the model to decide what knowledge to retrieve and use during inference [1].

Retrieval-augmented language model pre-training refers to a process that:
*   **Augments pre-training algorithms:** It incorporates a learned textual knowledge retriever into the language model pre-training process [1].
*   **Uses a retrieve-then-predict process:** Before making a prediction, the language model uses the retriever to pull documents from a large corpus (such as Wikipedia) and then attends over those documents to inform its prediction [1].
*   **Utilizes unsupervised signals:** The retriever is trained using a performance-based signal from unsupervised text; specifically, the model is rewarded when a retrieval improves the language model's perplexity and penalized when a retrieval is uninformative [1]. 
*   **Employs masked language modeling:** For the pre-training task, the model uses masked language modeling, where it must predict missing tokens ($y$) from a sentence ($x$) by retrieving helpful documents ($z$) from a knowledge corpus ($Z$) [3].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7

### Multi-Agent Answer

REALM (Retrieval-Augmented Language Model) is a framework that augments language model pre-training algorithms with a learned textual knowledge retriever [E1, E2]. The framework is designed to capture knowledge in a modular and interpretable way [E1, E2]. Unlike traditional models that store world knowledge implicitly in neural network parameters—a method that requires ever-larger networks to cover more facts [E2]—REALM explicitly exposes the role of world knowledge by having the model decide what to retrieve and use during inference [E1].

Retrieval-augmented language model pre-training refers to a process where, before making a prediction, the language model uses a retriever to pull documents from a large corpus, such as Wikipedia, and then attends over those documents to inform its prediction [E1]. This retrieval process is utilized during pre-training, fine-tuning, and inference [E2]. Additionally, the retriever can be pre-trained in an unsupervised manner by using masked language modeling as the learning signal [E2].

### Metrics

- baseline_latency_seconds: 7.544
- orchestrator_latency_seconds: 40.759
- baseline_total_tokens: 3901
- orchestrator_total_tokens: 25820
- baseline_citation_count: 3
- orchestrator_evidence_count: 8
- fact_check_status_counts: {'unsupported': 2, 'supported': 4}

## Question 4

Type: definition

How does REALM differ from a standard parametric language model such as BERT in where knowledge is stored and accessed?

### Baseline Answer

In standard parametric language models such as BERT, world knowledge is stored implicitly within the parameters of the underlying neural network [1]. This implicit storage makes it difficult to determine what knowledge is stored and where, and limits storage space to the size of the network [1].

In contrast, REALM augments language model pre-training with a learned textual knowledge retriever [1, 2]. Instead of relying solely on parameters, this approach explicitly exposes the role of world knowledge by having the model decide what knowledge to retrieve and use during inference [2]. The model uses the retriever to access documents from a large corpus, such as Wikipedia, and then attends over those documents to inform its predictions [1, 2]. This method provides qualitative benefits, including modularity and interpretability, because the memories are grounded—meaning each memory is associated with a specific document rather than unnamed value vectors [1, 3].

Citations:
[1] data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2
[2] data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[3] data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-15-e73576ceacc6e97a0666fd10

### Multi-Agent Answer

Unlike models that store knowledge within their parameters, REALM uses a learned textual knowledge retriever to capture knowledge in a more interpretable and modular way [E3]. Before making each prediction, the language model uses this retriever to retrieve documents from a large corpus, such as Wikipedia, and then attends over those documents to help inform its prediction [E3]. This approach explicitly exposes the role of world knowledge by requiring the model to decide what knowledge to retrieve and use during inference [E3].

The provided evidence does not describe the specific knowledge storage or access mechanisms of a standard parametric language model such as BERT [E2].

### Metrics

- baseline_latency_seconds: 4.707
- orchestrator_latency_seconds: 39.868
- baseline_total_tokens: 3866
- orchestrator_total_tokens: 24133
- baseline_citation_count: 3
- orchestrator_evidence_count: 7
- fact_check_status_counts: {'unsupported': 1, 'supported': 3}

## Question 5

Type: method/mechanism

How does REALM's retrieve-then-predict framework work, including the role of the latent document variable z?

### Baseline Answer

REALM's retrieve-then-predict framework decomposes the probability of an output $y$ given an input $x$, $p(y|x)$, into two distinct steps:

1.  **Retrieve:** Given an input $x$, the model first retrieves potentially helpful documents $z$ from a knowledge corpus $Z$ [3]. This step is modeled as a sample from the distribution $p(z|x)$ [3].
2.  **Predict:** The model then conditions on both the original input $x$ and the retrieved document $z$ to generate the output $y$, modeled as $p(y|z,x)$ [3].

**The Role of the Latent Document Variable $z$**
In this framework, $z$ is treated as a latent variable [3]. To calculate the overall likelihood of generating the output $y$, the model marginalizes over all possible documents $z$ in the corpus $Z$, using the following formula:
$$p(y |x) = \sum_{z \in Z} p(y |z, x) p(z |x)$$ [3]

The knowledge retriever is responsible for modeling $p(z|x)$ using a dense inner product model, where the relevance score between $x$ and $z$ is the inner product of their respective vector embeddings [3].

Citations:
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7

### Multi-Agent Answer

The REALM (Retrieval-Augmented Language Model) framework augments language model pre-training algorithms with a learned textual knowledge retriever [E1]. The framework decomposes the generative process $p(y|x)$ into two distinct steps: first, retrieving potentially helpful documents $z$ from a knowledge corpus $Z$, and second, predicting the output $y$ conditioned on both the input $x$ and the retrieved $z$ [E3].

In this framework, the approach is modeled as a latent variable language model [E1]. The document $z$ is treated as a latent variable, and the overall likelihood is calculated by marginalizing over all possible documents $z$ using the mathematical representation $p(y|x) = \sum_{z \in Z} p(y|z, x) p(z|x)$ [E3]. To inform its predictions, the language model uses the retriever to pull documents from a large corpus, such as Wikipedia, and then attends over those documents [E1, E2].

### Metrics

- baseline_latency_seconds: 4.486
- orchestrator_latency_seconds: 38.237
- baseline_total_tokens: 3386
- orchestrator_total_tokens: 25543
- baseline_citation_count: 3
- orchestrator_evidence_count: 5
- fact_check_status_counts: {'supported': 4, 'unsupported': 1}

## Question 6

Type: method/mechanism

How does the paper train the retriever when the retrieved document is latent, and how does learning signal flow back to retrieval?

### Baseline Answer

The paper trains the retriever by modeling the "retrieve-then-predict" approach as a latent variable language model and optimizing the marginal likelihood [1]. The training utilizes a performance-based signal from unsupervised text, where the retriever is rewarded for selecting documents that improve the language model's perplexity and penalized for uninformative retrievals [1]. Specifically, the retriever is pre-trained in an unsupervised manner using masked language modeling as the learning signal [2].

The learning signal flows back to the retrieval module through backpropagation [1, 2]. The signal from the language modeling objective backpropagates all the way through the retriever, even though the retriever must consider millions of documents [2]. To handle the computational challenge of this end-to-end learning, the retriever is structured so that computations for each document can be cached and updated asynchronously, and document selection is formulated as Maximum Inner Product Search (MIPS) [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2

### Multi-Agent Answer

The REALM framework uses a latent knowledge retriever that is trained in an unsupervised manner [E2]. The retriever is trained using a performance-based signal from unsupervised text, where retrieval is rewarded if it improves the language model's perplexity and penalized if the retrieval is uninformative [E1]. Specifically, masked language modeling is used as the learning signal for the unsupervised pre-training of the retriever [E2].

To enable training, the learning signal from the language modeling objective is backpropagated through the retrieval step [E2]. This process allows for end-to-end learning by backpropagating through a retrieval step that considers an entire corpus of textual knowledge, which can consist of millions of documents [E1][E2].

### Metrics

- baseline_latency_seconds: 3.945
- orchestrator_latency_seconds: 18.439
- baseline_total_tokens: 2979
- orchestrator_total_tokens: 14277
- baseline_citation_count: 3
- orchestrator_evidence_count: 5
- fact_check_status_counts: {'supported': 5}

## Question 7

Type: method/mechanism / implementation

What approximations or engineering choices does REALM use to make retrieval over a large corpus practical during training and inference?

### Baseline Answer

To address the significant computational challenge of considering millions of candidate documents during pre-training while backpropagating through retrieval decisions, REALM employs the following engineering choices:

*   **Caching and Asynchronous Updates:** The retriever is structured so that the computation performed for each individual document can be cached and updated asynchronously [2].
*   **Maximum Inner Product Search (MIPS):** The selection of the best documents is formulated as a Maximum Inner Product Search [2].

Additionally, while other retrieval-based systems often retrieve between 20 to 80 documents, the REALM system achieves its best performance while only retrieving 5 documents [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952

### Multi-Agent Answer

To manage the computational challenges of large-scale neural retrieval, REALM employs several engineering choices and approximations:

*   **MIPS Formulation and Caching:** The authors formulated the document selection process as a Maximum Inner Product Search (MIPS) [E1]. To handle large-scale retrieval, the retriever is structured so that the computation for each document can be cached and updated asynchronously [E1]. Additionally, the document embedding for the MIPS index is parallelized over 16 TPUs [E3].
*   **Candidate Selection and Marginalization:** Although the system may involve just over 13 million retrieval candidates [E3], the model uses approximations during different stages. During fine-tuning inference, the model considers only the top-5 candidates [E3]. For each example, the model retrieves and marginalizes over 8 candidate documents, a set that includes a null document [E3].

### Metrics

- baseline_latency_seconds: 3.332
- orchestrator_latency_seconds: 21.317
- baseline_total_tokens: 2847
- orchestrator_total_tokens: 13526
- baseline_citation_count: 3
- orchestrator_evidence_count: 3
- fact_check_status_counts: {'supported': 5}

## Question 8

Type: comparison

How does REALM compare with ORQA or other open-domain QA baselines, and what evidence supports that comparison?

### Baseline Answer

Compared to ORQA, the most direct comparison to REALM, the improvement of REALM is attributed purely to better pre-training methods [1]. In this comparison, the fine-tuning setup, hyperparameters, and training data are identical [1]. Additionally, the retrievers for both REALM pre-training and ORQA are initialized using the Inverse Cloze Task [2].

Regarding other open-domain QA baselines:
* **Retrieval-based systems:** Compared to other retrieval-based systems (such as Asai et al., 2019; Min et al., 2019a;b) which typically retrieve between 20 to 80 documents, REALM achieves the "overall best performance" while retrieving only 5 documents [1].
* **Generation-based systems:** For the most competitive and comparable generation-based baseline, REALM is compared against concurrent work that fine-tunes T5 for Open-QA [2].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-10-8ea61faa3a17c1fc8f8725d8

### Multi-Agent Answer

ORQA is considered the most direct comparison to REALM because the fine-tuning setup, hyperparameters, and training data are identical [E1]. The improvement demonstrated by REALM over ORQA is attributed purely to superior pre-training methods [E1]. Additionally, the retrievers for both REALM pre-training and ORQA are initialized using the Inverse Cloze Task [E2].

Compared to other retrieval-based systems, REALM achieves the overall best performance despite retrieving fewer documents [E1]. Specifically, REALM achieves its best performance by retrieving 5 documents, whereas other retrieval-based systems typically retrieve between 20 and 80 documents [E1].

### Metrics

- baseline_latency_seconds: 4.289
- orchestrator_latency_seconds: 20.178
- baseline_total_tokens: 2797
- orchestrator_total_tokens: 12162
- baseline_citation_count: 3
- orchestrator_evidence_count: 5
- fact_check_status_counts: {'supported': 5}

## Question 9

Type: comparison

How does REALM's retrieval-based approach compare with storing knowledge only in model parameters?

### Baseline Answer

Compared to models that store knowledge implicitly in their parameters, REALM's retrieval-based approach offers the following differences:

*   **Interpretability and Modularity:** REALM captures knowledge in a more interpretable and modular way [1, 3]. Storing knowledge implicitly in parameters makes it difficult to determine what knowledge is stored in the network and where [3].
*   **Explicit Role of Knowledge:** Unlike models that store knowledge in parameters, REALM's approach explicitly exposes the role of world knowledge by requiring the model to decide what knowledge to retrieve and use during inference [1].
*   **Storage and Scaling:** In models where knowledge is stored in parameters, the storage space is limited by the size of the network, meaning that capturing more world knowledge requires training ever-larger networks, which can be prohibitively expensive or slow [3]. 
*   **Mechanism:** Instead of relying solely on parameters, REALM uses a learned textual knowledge retriever to retrieve and attend over documents from a large corpus (such as Wikipedia) during pre-training, fine-tuning, and inference [1, 3].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-1-4db590f52f9234a64d454952, chunk_index: 1
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-0-7d4268087c32fc1b944606b2, chunk_index: 0

### Multi-Agent Answer

In contrast to models that store knowledge within their parameters, the REALM approach explicitly exposes the role of world knowledge [E2]. REALM achieves this by having the model decide what knowledge to retrieve and use during the inference process [E2].

The REALM framework augments language model pre-training with a learned textual knowledge retriever [E2]. This method decomposes the process of learning a distribution into two distinct steps: first retrieving helpful documents from a corpus, and then predicting the output conditioned on both the input and the retrieved documents [E3]. This approach differs from standard reading comprehension models that comprehend a single document, as Open-QA models must retain knowledge from millions of documents [E3].

### Metrics

- baseline_latency_seconds: 4.466
- orchestrator_latency_seconds: 19.808
- baseline_total_tokens: 2957
- orchestrator_total_tokens: 12885
- baseline_citation_count: 3
- orchestrator_evidence_count: 4
- fact_check_status_counts: {'supported': 5}

## Question 10

Type: evidence synthesis / ablation

What ablation or diagnostic evidence shows that retrieval pre-training improves REALM rather than only the reader component?

### Baseline Answer

To isolate the contribution of improving the retriever during pre-training, the authors report a metric regarding how often the gold answer appears in the top-5 retrievals before any fine-tuning is applied [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05, chunk_index: 12

### Multi-Agent Answer

The improvement of REALM over ORQA is attributed purely to its superior pre-training methods [E1, E3]. ORQA serves as the most direct comparison to REALM because the fine-tuning setup, hyperparameters, and training data are identical between the two systems [E1, E3]. To specifically isolate the contribution of improving the retriever during pre-training, the metric of how often the gold answer appears in the top-5 retrievals is used [E1].

### Metrics

- baseline_latency_seconds: 1.951
- orchestrator_latency_seconds: 36.072
- baseline_total_tokens: 2698
- orchestrator_total_tokens: 23453
- baseline_citation_count: 3
- orchestrator_evidence_count: 7
- fact_check_status_counts: {'unsupported': 2, 'supported': 1}

## Question 11

Type: evidence synthesis

Synthesize the evidence for why REALM improves open-domain QA performance, including retrieval quality, pre-training, and downstream fine-tuning.

### Baseline Answer

Based on the provided text, the evidence for why REALM improves open-domain QA performance is synthesized as follows:

*   **Pre-training Methods:** The improvement of REALM over the ORQA system is attributed purely to its better pre-training methods [1]. REALM's approach extends language model pre-training to include retrieval [2]. This method of pre-training can be applied in both a single-corpus setting (where the pre-training corpus and knowledge corpus are both Wikipedia) and a separate-corpus setting (where the pre-training corpus is CC-News and the knowledge corpus is Wikipedia) [1].
*   **Retrieval Quality:** REALM demonstrates superior retrieval efficiency compared to other retrieval-based systems; while other systems often retrieve between 20 to 80 documents, REALM achieves the overall best performance while only retrieving 5 documents [1]. Additionally, the model's performance is aided by improving the retriever during the pre-training phase [1].
*   **Downstream Fine-tuning:** For fine-tuning, REALM treats the Open-QA task as a "retrieve-then-predict" generative process [2]. Given a question ($x$), the model first retrieves potentially helpful documents ($z$) from a knowledge corpus ($Z$), and then conditions on both the retrieved documents and the original input to generate the answer ($y$) [2].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7

### Multi-Agent Answer

REALM improves open-domain QA performance through a novel pre-training framework that augments language model algorithms with a learned textual knowledge retriever [E2]. The improvement of REALM over systems like ORQA is attributed purely to these superior pre-training methods [E1, E3]. This pre-training approach is versatile and can be applied to both single-corpus settings, such as using Wikipedia for both training and retrieval, and separate-corpus settings, such as using CC-News for training and Wikipedia for retrieval [E1].

Regarding retrieval quality, the retriever is trained using a performance-based signal from unsupervised text, where retrievals that improve the language model's perplexity are rewarded [E2]. Unlike models that store knowledge within their parameters, REALM explicitly exposes the role of world knowledge by requiring the model to decide what to retrieve and use during inference [E2]. This allows the retriever to be designed for transferability to other tasks because it retrieves actual text rather than labeled examples [E2]. Additionally, REALM achieves its best performance while retrieving fewer documents—specifically 5 documents—compared to other retrieval-based systems, which often retrieve between 20 to 80 documents [E1].

### Metrics

- baseline_latency_seconds: 5.172
- orchestrator_latency_seconds: 45.638
- baseline_total_tokens: 2801
- orchestrator_total_tokens: 25050
- baseline_citation_count: 3
- orchestrator_evidence_count: 8
- fact_check_status_counts: {'supported': 10}

## Question 12

Type: multi-step reasoning

Explain step by step how a masked-language-model pre-training objective can improve downstream open-domain QA in REALM.

### Baseline Answer

In REALM, a masked-language-model (MLM) pre-training objective improves downstream open-domain question answering (Open-QA) through the following process:

1.  **Pre-training with MLM**: The model is trained on an unlabeled corpus (such as Wikipedia) using the MLM variant of pre-training [1]. In this task, tokens are randomly masked in a sentence, and the model must use its representation of the masked input to predict the missing tokens [1].
2.  **Learning Knowledge and Syntax**: To successfully predict missing tokens, the MLM must learn to encode syntactic and semantic information as well as world knowledge [1].
3.  **Integration of a Latent Knowledge Retriever**: REALM augments the pre-training process with a neural knowledge retriever that retrieves potentially helpful documents ($z$) from a large knowledge corpus ($Z$) based on the input ($x$) [2, 3]. This allows the model to retrieve and attend over documents during pre-training, fine-tuning, and inference [2].
4.  **Unsupervised Learning via Backpropagation**: The MLM serves as the learning signal for the retriever; the signal from the language modeling objective is backpropagated through the retrieval step [2]. This allows the retriever to be trained in an unsupervised manner [2].
5.  **Decomposition of the Generative Process**: The model learns a distribution $p(y|x)$ by decomposing it into two steps: retrieving documents ($p(z|x)$) and then conditioning on both the retrieved documents and the input to predict the output ($p(y|z, x)$) [3].
6.  **Fine-tuning for Open-QA**: The pre-trained model is then fine-tuned for the downstream Open-QA task, where the input $x$ is a question and the goal is to output the correct answer string $y$ [1, 3]. This process benefits from the knowledge captured during the MLM pre-training stage [2].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-2-7f240c64641ad3f52fc62e97, chunk_index: 2
[2] source: data/2002.08909v1

### Multi-Agent Answer

In REALM, a masked-language-model (MLM) pre-training objective improves downstream open-domain question answering through the following process:

1.  **Encoding Knowledge via MLM**: During pre-training, the MLM objective requires the model to predict missing tokens within an input text passage [E1]. This process enables the model to encode syntactic, semantic, and world knowledge [E1].
2.  **Unsupervised Retriever Training**: REALM uses the MLM objective as a learning signal to pre-train a latent knowledge retriever in an unsupervised manner [E2]. This is achieved by backpropagating the learning signal through a retrieval step that considers millions of documents [E2].
3.  **Augmenting the Language Model**: While traditional language model pre-training stores knowledge implicitly in neural network parameters [E2], REALM augments the language model with a latent knowledge retriever [E2]. This augmentation allows the model to retrieve and attend over documents from a large corpus, such as Wikipedia, during pre-training, fine-tuning, and inference [E2].

### Metrics

- baseline_latency_seconds: 5.793
- orchestrator_latency_seconds: 41.105
- baseline_total_tokens: 3580
- orchestrator_total_tokens: 24132
- baseline_citation_count: 3
- orchestrator_evidence_count: 8
- fact_check_status_counts: {'unsupported': 4, 'supported': 8}

## Question 13

Type: multi-step reasoning / error analysis

If REALM retrieves an irrelevant document, how would that affect p(z|x), p(y|z,x), and the final answer prediction?

### Baseline Answer

If REALM retrieves an irrelevant document $z$, the effects are as follows:

*   **$p(z|x)$**: This represents the distribution modeled by the neural knowledge retriever [3]. While the provided text does not explicitly state how an irrelevant document affects this specific probability value, it notes that the retriever models $p(z|x)$ as a softmax over relevance scores $f(x, z)$, where $f(x, z)$ is the inner product of the vector embeddings of $x$ and $z$ [3].
*   **$p(y|z,x)$**: A negative Retrieval Utility (RU) can indicate that $z$ is less useful for predicting $y$ than a null document, which "could mean that $z$ is irrelevant to $x$" [1].
*   **Final answer prediction ($p(y|x)$)**: The overall likelihood $p(y|x)$ is obtained by treating $z$ as a latent variable and marginalizing over all possible documents $z$ using the formula $p(y |x) = \sum_{z \in Z} p(y |z, x) p(z |x)$ [3]. Because the marginalized probability of a correct answer increases when REALM retrieves documents containing a related fact, the implication is that retrieval of irrelevant documents would not provide this same increase in probability [2].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-20-58cd33db77feaae8a3f8d036
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-13-8b5179bb43546a69e37d136e
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-3-e027b8ff59e74b51fa7f85b7

### Multi-Agent Answer

The provided evidence does not contain specific mathematical details regarding how an irrelevant document changes the individual values of $p(z|x)$ or $p(y|z,x)$ [E1, E2].

However, the evidence provides the following context regarding these components:

*   **Model Decomposition:** REALM decomposes the learning of the distribution $p(y|x)$ into two steps: retrieving documents $z$ from a knowledge corpus $Z$, modeled as $p(z|x)$, and generating the output $y$ conditioned on both the input and retrieved documents, modeled as $p(y|z, x)$ [E2].
*   **Final Prediction:** The overall likelihood of generating the answer $y$ is calculated by treating $z$ as a latent variable and marginalizing over all possible documents $z$ using the formula $p(y |x) = \sum_{z \in Z} p(y |z, x) p(z |x)$ [E2].
*   **Impact of Irrelevance:** If a retrieved document $z$ is irrelevant to $x$, it may cause a negative Retrieval Utility (RU) [E1]. A negative RU indicates that the retrieved document $z$ is less useful for predicting the target $y$ than a null document $\emptyset$ [E1].

### Metrics

- baseline_latency_seconds: 6.262
- orchestrator_latency_seconds: 44.784
- baseline_total_tokens: 3608
- orchestrator_total_tokens: 22432
- baseline_citation_count: 3
- orchestrator_evidence_count: 6
- fact_check_status_counts: {'unsupported': 1, 'supported': 4}

## Question 14

Type: limitation/uncertainty

What limitations, uncertainties, or missing comparisons should be noted when interpreting REALM's reported results?

### Baseline Answer

When interpreting REALM's reported results, the following limitations, uncertainties, and missing comparisons should be noted:

*   **Unused Data:** Certain data could have benefited REALM but was not utilized in the experiments conducted [1].
*   **Interpretations of Retrieval Utility (RU):** A negative RU indicates that the document $z$ is less useful for predicting $y$ than the null document [2]. However, this outcome is uncertain as it could mean $z$ is irrelevant to $x$, or it could mean that the masked tokens in $x$ do not require world knowledge, or that the required world knowledge is already sufficiently commonplace and "baked into the model's parameters" [2].
*   **Impact of Masking and Training:** The Retrieval Utility (RU) is impacted by the number of pre-training steps and the specific choice of masking used [2].
*   **Comparison to Other Systems:** While ORQA is noted as the most direct comparison because it uses identical fine-tuning setups, hyperparameters, and training data [1], REALM's performance is contrasted with other retrieval-based systems that retrieve between 20 to 80 documents, whereas REALM achieves its results retrieving only 5 documents [1].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[2] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-20-58cd33db77feaae8a3f8d036

### Multi-Agent Answer

When interpreting REALM's reported results, the following limitations, requirements, and information gaps should be noted:

**Technical Requirements and Limitations**
*   The model's performance is sensitive to its components; while both the encoder and retriever benefit from separate training, optimal results require both components to act in unison [E2].
*   The training process can be negatively affected by a stale MIPS index, which necessitates frequent index refreshes [E2].
*   The effectiveness of REALM relies on a salient span masking scheme, a component that has not been shown to be impactful in previous standard BERT training [E2].
*   For Open-QA applications, the model depends on "grounded" memories—where each memory is associated with a specific document—to provide the provenance required for predicted answers to be considered trustworthy [E1, E3].

**Missing Comparisons and Uncertainties**
*   The provided evidence does not include a comprehensive list of comparative performance metrics against other models, beyond a specific probability comparison example involving BERT [E2].
*   The evidence lacks explicit lists of model failures or quantitative error rates [E1, E2, E3].

### Metrics

- baseline_latency_seconds: 6.406
- orchestrator_latency_seconds: 35.536
- baseline_total_tokens: 2093
- orchestrator_total_tokens: 22828
- baseline_citation_count: 3
- orchestrator_evidence_count: 9
- fact_check_status_counts: {'supported': 4, 'unsupported': 2}

## Question 15

Type: citation grounding / uncertainty

Which claims about REALM's performance or mechanism cannot be verified unless the answer cites specific experimental evidence from the paper?

### Baseline Answer

Based on the provided context, the following claims regarding REALM's performance or mechanism require specific experimental evidence from the paper for verification:

*   **Performance relative to ORQA:** The claim that the improvement of REALM over ORQA is "purely due to better pre-training methods" [1].
*   **Performance relative to other retrieval-based systems:** The claim that REALM achieves the "overall best performance" while only retrieving 5 documents, compared to other retrieval-based systems that often retrieve 20 to 80 documents [1].
*   **Applicability of pre-training methods:** The claim that the method of pre-training can be applied to both the "single-corpus setting" and the "separate-corpus setting" [1].
*   **Predictive nature of Retrieval Utility (RU):** The claim that RU is "more predictive of good performance on the downstream task of Open-QA than even the overall log-likelihood" [3].
*   **Behavior of RU during training:** The claim that RU "increases steadily over the course of pre-training" [3].
*   **Adaptability to updated knowledge:** The claim that a REALM model pre-trained on an outdated corpus (2018) is able to retrieve documents from an updated corpus (2020) and generate the correct token [3].

Citations:
[1] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-12-69a8bcd84db848ef23c1fa05
[3] source: data/2002.08909v1.pdf, chunk_id: 2002.08909v1-20-58cd33db77feaae8a3f8d036

### Multi-Agent Answer

Based on the provided evidence, the following claims about REALM's performance or mechanism cannot be verified without specific experimental data or results not included in the notes:

*   **Specific Performance Metrics:** While it is claimed that REALM achieves the "best overall performance" compared to other retrieval-based systems [E1], the provided evidence does not include the specific experimental results, such as exact accuracy scores or F1 scores, required to verify this performance level [E1].
*   **Impact of Model Size:** Although the study measures the impact of model size using a T5 baseline with models ranging up to 11 billion parameters [E5], the specific performance gains or losses attributed to these different model sizes are not detailed in the notes [E5].

### Metrics

- baseline_latency_seconds: 6.261
- orchestrator_latency_seconds: 22.475
- baseline_total_tokens: 2784
- orchestrator_total_tokens: 12196
- baseline_citation_count: 3
- orchestrator_evidence_count: 5
- fact_check_status_counts: {'supported': 7}
