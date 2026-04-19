# experiment01: architecture control, all small models, top_k=5

## Agent Configuration

- family: architecture_control
- control_variable: agent_architecture
- top_k: 5
- max_evidence_chunks: 5
- baseline_model: gpt-4.1-mini
- orchestrator_model: gpt-4.1-mini
- search_model: gpt-4.1-mini
- summarization_model: gpt-4.1-mini
- fact_check_model: gpt-4.1-mini
- final_synthesis_model: gpt-4.1-mini

## Question 1

Type: easy lookup

What external knowledge source or corpus does REALM retrieve from, and how is it used by the model?

### Baseline Answer

The REALM (Retrieval-Augmented Language Model) retrieves from a textual knowledge source or corpus, which is explicitly accessed by a learned textual knowledge retriever incorporated into the pre-training algorithm. Instead of storing knowledge solely in the model parameters, REALM explicitly uses this external knowledge retriever to access world knowledge during training and inference. This approach exposes the role of world knowledge to the model by asking it to retrieve relevant textual information, which it then uses to augment language model pre-training and improve its understanding and generation capabilities [1][2][3][4][5].

Citations:  
[1][2][3][4][5] - data/2002.08909v1.pdf, chunks 84.0, 85.0, 96.0, 120.0, and 115.0

### Multi-Agent Answer

The provided evidence notes consistently state that REALM enhances language model pre-training by incorporating a learned textual knowledge retriever [E1][E2][E3][E4][E5]. Unlike models that store knowledge solely within their parameters, REALM explicitly leverages world knowledge by retrieving relevant texts from an external source during training [E1][E2][E3]. However, the evidence does not specify the exact external knowledge source or corpus from which REALM retrieves information [E1][E2][E3][E4][E5]. Additionally, the notes do not detail how the retrieved knowledge is used by the model beyond this general retrieval role [E1][E2][E3][E4][E5]. Therefore, information about the precise external knowledge source or corpus and the detailed usage of the retrieved knowledge by REALM is missing from the supplied evidence.

### Metrics

- baseline_latency_seconds: 2.816
- orchestrator_latency_seconds: 49.436
- baseline_total_tokens: 932
- orchestrator_total_tokens: 12519
- baseline_citation_count: 5
- orchestrator_evidence_count: 23
- fact_check_status_counts: {'supported': 4, 'unsupported': 1}

## Question 2

Type: easy lookup

Which downstream tasks or benchmarks does the paper use to evaluate REALM?

### Baseline Answer

The provided context does not contain information about which downstream tasks or benchmarks the paper uses to evaluate REALM. The text mainly discusses reporting metrics related to the retriever's performance, such as how often the gold answer appears in the top-5 retrievals before fine-tuning, but it does not specify the downstream tasks or benchmarks used for evaluation.

Citations:  
No relevant citations available in the provided context.

### Multi-Agent Answer

The paper evaluates REALM by reporting end-to-end results on downstream tasks as well as measuring how often the gold answer appears in the top-5 retrieved documents before any fine-tuning is applied [E6][E7]. This top-5 retrieval accuracy metric is used to isolate the contribution of improving the retriever component during pre-training, separate from the effects of fine-tuning [E6][E8]. However, the exact downstream tasks or benchmarks used for the end-to-end evaluation are not specified in the provided evidence notes, so details on which specific benchmarks REALM is evaluated on are missing [E6][E9].

### Metrics

- baseline_latency_seconds: 2.123
- orchestrator_latency_seconds: 21.750
- baseline_total_tokens: 876
- orchestrator_total_tokens: 7596
- baseline_citation_count: 5
- orchestrator_evidence_count: 11
- fact_check_status_counts: {'supported': 3}

## Question 3

Type: definition

What is REALM, and what does the paper mean by retrieval-augmented language model pre-training?

### Baseline Answer

REALM stands for Retrieval-Augmented Language Model pre-training. It is a novel framework that enhances language model pre-training algorithms by incorporating a learned textual knowledge retriever. Unlike traditional language models that store knowledge solely within their parameters, REALM explicitly incorporates world knowledge by enabling the model to access and retrieve relevant textual information during pre-training. This approach exposes the role of external knowledge more directly, augmenting the model’s understanding by leveraging retrieved text rather than relying exclusively on internal parameter storage of knowledge [1][2][3][4][5].

Citations:  
[1][2][3][4][5] data/2002.08909v1.pdf

### Multi-Agent Answer

REALM, or Retrieval-Augmented Language Model, is a pre-training method that enhances language model pre-training algorithms by incorporating a learned textual knowledge retriever [E1]. Unlike traditional models that store knowledge solely within their parameters, REALM explicitly exposes the role of world knowledge through retrieval mechanisms integrated into the training process [E2]. Specifically, during pre-training, REALM prompts the model to retrieve relevant textual information from an external source, thereby integrating external knowledge instead of embedding all knowledge internally [E3]. This retrieval-augmented language model pre-training framework augments standard language model training by requiring the model to access and use external knowledge dynamically [E4][E5].

### Metrics

- baseline_latency_seconds: 3.394
- orchestrator_latency_seconds: 28.547
- baseline_total_tokens: 918
- orchestrator_total_tokens: 7191
- baseline_citation_count: 5
- orchestrator_evidence_count: 16
- fact_check_status_counts: {'supported': 4}

## Question 4

Type: definition

How does REALM differ from a standard parametric language model such as BERT in where knowledge is stored and accessed?

### Baseline Answer

REALM differs from a standard parametric language model such as BERT in the way knowledge is stored and accessed. While models like BERT store knowledge directly in their parameters, REALM augments language model pre-training algorithms with a learned textual knowledge retriever. This means that instead of embedding all knowledge within the model's parameters, REALM explicitly exposes and accesses world knowledge via an external retrieval mechanism, allowing it to retrieve relevant textual information dynamically during inference rather than relying solely on stored parameter knowledge [1][2][3][4][5].

Citations:  
[1] data/2002.08909v1.pdf chunk 113.0  
[2] data/2002.08909v1.pdf chunk 114.0  
[3] data/2002.08909v1.pdf chunk 108.0  
[4] data/2002.08909v1.pdf chunk 122.0  
[5] data/2002.08909v1.pdf chunk 123.0

### Multi-Agent Answer

REALM differs from a standard parametric language model such as BERT in where and how knowledge is stored and accessed by augmenting the language model pre-training with a learned textual knowledge retriever, instead of embedding all knowledge implicitly within the model parameters [E15][E16]. While traditional language models like BERT store knowledge implicitly inside their neural network parameters—requiring increasingly large models to cover more facts—REALM explicitly exposes and accesses world knowledge by retrieving relevant information from a large external document corpus, such as Wikipedia, during pre-training, fine-tuning, and inference [E17][E19]. This retrieval-augmented design allows REALM to attend to and incorporate external documents directly, making knowledge access more modular and interpretable compared to the implicit parameter storage in models like BERT [E17][E18]. Additionally, REALM’s knowledge retriever is trained in an unsupervised manner using masked language modeling with backpropagation through the retrieval step, enabling it to efficiently leverage millions of documents as part of its knowledge source [E17].

### Metrics

- baseline_latency_seconds: 3.420
- orchestrator_latency_seconds: 26.847
- baseline_total_tokens: 961
- orchestrator_total_tokens: 10723
- baseline_citation_count: 5
- orchestrator_evidence_count: 21
- fact_check_status_counts: {'supported': 4}

## Question 5

Type: method/mechanism

How does REALM's retrieve-then-predict framework work, including the role of the latent document variable z?

### Baseline Answer

REALM's retrieve-then-predict framework works by decomposing the task of generating an output \( y \) given an input \( x \) into two steps involving a latent document variable \( z \) drawn from a knowledge corpus \( Z \). Specifically, given \( x \) (which could be a masked sentence in pre-training or a question in fine-tuning), the model first retrieves potentially relevant documents \( z \) from the corpus using a distribution \( p(z|x) \). This is the "retrieve" step.

The framework then conditions on both the input \( x \) and the retrieved document(s) \( z \) to predict the output \( y \), modeling this conditional distribution as \( p(y|z,x) \). Since the document \( z \) is latent (not directly observed), the overall likelihood of predicting \( y \) is obtained by marginalizing over all possible documents \( z \) in the corpus:

\[
p(y|x) = \sum_{z \in Z} p(y|z,x) p(z|x).
\]

Thus, \( z \) serves as a latent variable representing knowledge residing in documents, which the model can attend to when generating \( y \) [1].

In terms of model architecture, the knowledge retriever models \( p(z|x) \) as a softmax over relevance scores computed by a dense inner product between embeddings of \( x \) and \( z \):

\[
p(z|x) = \frac{\exp f(x,z)}{\sum_{z'} \exp f(x,z')}, \quad f(x,z) = \text{Embed}_{input}(x)^\top \text{Embed}_{doc}(z),
\]

where both embedding functions are implemented with BERT-style Transformers that project inputs and documents into a suitable embedding space [1].

During training, the retrieval function \( p(z|x) \) is learned to maximize the likelihood of the output \( y \) by encouraging the retrieval of documents \( z \) that increase the prediction accuracy \( p(y|z,x) \). The gradient of the objective with respect to the retrieval score \( f(x,z) \) is proportional to the difference between the conditional prediction probability \( p(y|z,x) \) and the expected prediction \( p(y|x) \), weighted by \( p(z|x) \):

\[
\nabla \log p(y|x) = \sum_{z \in Z} \left(\

### Multi-Agent Answer

The REALM framework employs a retrieve-then-predict approach in which a learned textual knowledge retriever is integrated into the language model pre-training process [E1]. This framework explicitly exposes the role of world knowledge by asking the model to retrieve relevant external documents rather than storing all knowledge solely within its parameters [E2]. However, the provided evidence does not explicitly describe the retrieved document as a latent variable \( z \), nor detail how the model conditions on such a latent variable to generate predictions [E3][E4][E5]. Therefore, the specific role of the latent document variable \( z \) within REALM’s retrieve-then-predict framework is not supported by the available evidence.

### Metrics

- baseline_latency_seconds: 5.912
- orchestrator_latency_seconds: 28.811
- baseline_total_tokens: 5574
- orchestrator_total_tokens: 7611
- baseline_citation_count: 5
- orchestrator_evidence_count: 20
- fact_check_status_counts: {'supported': 5}

## Question 6

Type: method/mechanism

How does the paper train the retriever when the retrieved document is latent, and how does learning signal flow back to retrieval?

### Baseline Answer

The paper trains the retriever when the retrieved document is latent by optimizing the retriever to reward retrievals that improve the prediction accuracy of the language model. Specifically, for a query \(x\) and document \(z\), the retriever assigns a relevance score \(f(x, z)\) to each document. During training, the gradient of the log-likelihood of the correct output \(y\) with respect to the retriever parameters \(\theta\) involves a term \(r(z)\) defined as:

\[
r(z) = \left[\frac{p(y | z, x)}{p(y | x)} - 1 \right] p(z | x)
\]

This gradient encourages the retriever to increase the score for documents \(z\) that yield a higher probability of correctly predicting \(y\) than the expected probability over all documents, and decrease it otherwise. Hence, learning signals flow back to the retriever based on how much each retrieved document helps improve the prediction, allowing the retriever to learn which documents to prioritize despite the retrieval being latent (i.e., not supervised explicitly) [3].

Additional techniques such as salient span masking focus training on tokens requiring world knowledge, and modeling with a null document accounts for cases where retrieval is not useful. This combination of gradient-based updates to the retriever and those inductive biases guides the retriever toward meaningful document selection during pre-training [3].

Citations:  
[3] data/2002.08909v1.pdf chunk_id: 2002.08909v1-1585-3c15fbe789d5ba47b3398302

### Multi-Agent Answer

The provided evidence does not contain detailed information about how the paper trains the retriever when the retrieved document is latent, nor does it explain how the learning signal flows back to retrieval. Some sources mention improving the retriever during pre-training [E3][E4], but they do not describe the mechanisms or the training procedure related to latent document retrieval or gradient flow. Sources E1 and E2 are fragmentary and do not add clarity on this point [E1][E2]. Therefore, additional text or evidence is needed to fully answer this question.

### Metrics

- baseline_latency_seconds: 5.533
- orchestrator_latency_seconds: 35.000
- baseline_total_tokens: 2161
- orchestrator_total_tokens: 9109
- baseline_citation_count: 5
- orchestrator_evidence_count: 15
- fact_check_status_counts: {'unsupported': 2, 'supported': 1}

## Question 7

Type: method/mechanism / implementation

What approximations or engineering choices does REALM use to make retrieval over a large corpus practical during training and inference?

### Baseline Answer

REALM makes retrieval over a large corpus practical during training and inference by employing several approximations and engineering choices:

1. **Cached and Asynchronously Updated Computation**: The retriever's computation for each document is designed to be cached and asynchronously updated. This allows for efficient handling of the large corpus by avoiding repeated computation for static documents during training [2].

2. **Maximum Inner Product Search (MIPS)**: Document selection is formulated as a Maximum Inner Product Search problem. This enables efficient retrieval by rapidly finding the documents whose embeddings have the highest similarity to the query representation, which is essential for scaling to millions of documents [2].

3. **Limited Number of Retrieved Documents**: Unlike other systems retrieving from a large number of documents (20 to 80), REALM only retrieves 5 candidate documents for each example, reducing the retrieval overhead while still achieving superior performance [1].

4. **Marginalization Over Candidates Including a Null Document**: For each training example, REALM retrieves and marginalizes over 8 candidate documents, including the null document ∅. This helps in efficiently optimizing the retrieval step as a latent variable that contributes to language modeling, without exhaustive search over the entire corpus [1].

5. **Parallelization Across TPUs**: The document embedding step for the MIPS index is parallelized over 16 TPUs, enabling scalable computation of document embeddings during pre-training [1].

Together, these techniques allow REALM to handle large-scale retrieval involving millions of documents efficiently during both pre-training and inference, with the entire model runnable on a single machine with a 12GB GPU [1][2].

### Citations

- [1] data/2002.08909v1.pdf, chunk 2389.0
- [2] data/2002.08909v1.pdf, chunk 401.0

### Multi-Agent Answer

REALM (Retrieval-Augmented Language Model) is a pre-training method that augments language model pre-training algorithms with a learned textual knowledge retriever, explicitly incorporating world knowledge rather than storing it solely in the model parameters [E1][E2][E3][E4]. Evaluation of REALM includes measuring how often the gold answer appears in the top-5 retrievals before any fine-tuning, which helps isolate the retriever’s contribution [E5]. However, the provided evidence does not include any specific details or descriptions of approximations or engineering choices that REALM uses to make retrieval over a large corpus practical during training and inference [E1][E2][E3][E4][E5]. Therefore, the evidence is insufficient to answer the question about the particular engineering methods or approximations REALM employs for efficient large-scale retrieval.

### Metrics

- baseline_latency_seconds: 6.445
- orchestrator_latency_seconds: 44.224
- baseline_total_tokens: 3391
- orchestrator_total_tokens: 13411
- baseline_citation_count: 5
- orchestrator_evidence_count: 19
- fact_check_status_counts: {'supported': 3, 'unsupported': 1}

## Question 8

Type: comparison

How does REALM compare with ORQA or other open-domain QA baselines, and what evidence supports that comparison?

### Baseline Answer

The provided context mentions that results for NaturalQuestions-Open are presented after ablating critical components of REALM, including both end-to-end results and the frequency with which the gold answer appears in the top-5 retrievals before any fine-tuning. This retrieval metric is said to more clearly isolate the contribution of improving the retriever during pre-training. However, the context does not provide a direct comparison between REALM and ORQA or other open-domain QA baselines, nor does it provide specific evidence supporting such comparisons.

Therefore, the information on how REALM compares with ORQA or other baselines, along with supporting evidence, is missing from the supplied context.

Citations:  
[1]–[5] data/2002.08909v1.pdf

### Multi-Agent Answer

REALM significantly outperforms ORQA and other existing open-domain QA baselines on multiple benchmarks, as shown by experimental results [E11]. Specifically, on the NaturalQuestions-Open (NQ) dataset, REALM achieves an exact match accuracy of 39.2% when trained on Wikipedia, compared to ORQA’s 33.3%, with both models having similar parameter sizes of about 330 million [E11]. Similarly, REALM surpasses ORQA on WebQuestions (WQ) and CuratedTREC (CT) benchmarks [E11].

The improvement over ORQA is attributed primarily to REALM’s better pre-training scheme rather than differences in model size or the number of retrieved documents, since both systems retrieve five documents; REALM uses a novel end-to-end pre-training approach that dynamically updates the retrieval index [E11][E1]. Unlike ORQA, which employs a fixed MIPS retrieval index, REALM backpropagates through the MIPS index, enabling the retriever and encoder to co-adapt during training [E1][E10]. This joint optimization strengthens both the retriever and encoder components, as shown by performance drops occurring when either is reset to its baseline during ablation studies [E10].

### Metrics

- baseline_latency_seconds: 2.187
- orchestrator_latency_seconds: 35.561
- baseline_total_tokens: 1011
- orchestrator_total_tokens: 15851
- baseline_citation_count: 5
- orchestrator_evidence_count: 12
- fact_check_status_counts: {'supported': 12}

## Question 9

Type: comparison

How does REALM's retrieval-based approach compare with storing knowledge only in model parameters?

### Baseline Answer

REALM's retrieval-based approach contrasts with models that store knowledge only in their parameters by explicitly exposing the role of world knowledge. Instead of embedding all knowledge implicitly within the model's parameters, REALM augments language model pre-training with a learned textual knowledge retriever, making the knowledge more interpretable and modular. This approach allows the model to access external information dynamically during training or inference rather than relying solely on fixed, internalized knowledge in the model weights [1][2][3][4][5].

Citations:  
[1] data/2002.08909v1.pdf chunk_id: 2002.08909v1-9-cf5025516887ae7c0a6945a4  
[2] data/2002.08909v1.pdf chunk_id: 2002.08909v1-15-8e1ed5ac17f00cdaaea1a1d2  
[3] data/2002.08909v1.pdf chunk_id: 2002.08909v1-12-b2efe934de78a0e6ea461c06  
[4] data/2002.08909v1.pdf chunk_id: 2002.08909v1-13-89d8fa7c34285827b6edef3e  
[5] data/2002.08909v1.pdf chunk_id: 2002.08909v1-228-5889412f467f6c43a91abdcf

### Multi-Agent Answer

REALM’s retrieval-based approach differs from models that store knowledge solely in their parameters by explicitly exposing the role of world knowledge [E2][E4]. Instead of embedding all knowledge implicitly within the model’s parameters, REALM asks the model to access and utilize external knowledge through a learned retrieval mechanism [E2][E4]. This method contrasts with traditional parametric models by making the knowledge retrieval step explicit, thereby separating the stored information from the model’s parameters [E4]. The evidence notes consistently emphasize this explicit exposure of world knowledge as the key distinction, although no specific quantitative comparisons or detailed measurements are provided in the sources [E2][E4].

### Metrics

- baseline_latency_seconds: 3.867
- orchestrator_latency_seconds: 37.884
- baseline_total_tokens: 1129
- orchestrator_total_tokens: 9930
- baseline_citation_count: 5
- orchestrator_evidence_count: 13
- fact_check_status_counts: {'supported': 4}

## Question 10

Type: evidence synthesis / ablation

What ablation or diagnostic evidence shows that retrieval pre-training improves REALM rather than only the reader component?

### Baseline Answer

The ablation or diagnostic evidence showing that retrieval pre-training improves REALM rather than only the reader component comes from reporting how often the gold answer appears in the top-5 retrievals before applying any fine-tuning. This retrieval metric more significantly isolates the contribution of improving the retriever during pre-training. Thus, by examining the frequency of retrieving the correct answer prior to reader fine-tuning, the authors isolate and demonstrate the effect of the retrieval pre-training on REALM's retriever component itself, beyond improvements to the reader [1][2][4][5].

Citations:  
[1] data/2002.08909v1.pdf chunk_id=2002.08909v1-2495-fc317265a32ba367ac785b4c  
[2] data/2002.08909v1.pdf chunk_id=2002.08909v1-2496-9ee7f1349fdc147d78ca9701  
[4] data/2002.08909v1.pdf chunk_id=2002.08909v1-2497-65a990c5ae3fe88ef74eaa38  
[5] data/2002.08909v1.pdf chunk_id=2002.08909v1-2498-ec0ada89ca5c3117380851a0

### Multi-Agent Answer

The REALM approach augments language model pre-training by incorporating a learned textual knowledge retriever, distinguishing it from models that store knowledge solely within their parameters [E1][E2]. This method explicitly exposes the role of world knowledge by requiring the model to access retrieved external information during pre-training, rather than relying only on internal parameter embeddings [E3][E4]. However, the provided evidence notes do not include specific ablation or diagnostic experiments that isolate the contribution of retrieval pre-training from the reader component [E1][E2][E3][E4][E5]. Therefore, based on the reviewed sources, direct ablation or diagnostic evidence demonstrating that retrieval pre-training itself—distinct from improvements in the reader component—leads to better performance is not available [E1][E2][E3][E4][E5].

### Metrics

- baseline_latency_seconds: 4.094
- orchestrator_latency_seconds: 43.007
- baseline_total_tokens: 1920
- orchestrator_total_tokens: 13069
- baseline_citation_count: 5
- orchestrator_evidence_count: 18
- fact_check_status_counts: {'supported': 3, 'unsupported': 1}

## Question 11

Type: evidence synthesis

Synthesize the evidence for why REALM improves open-domain QA performance, including retrieval quality, pre-training, and downstream fine-tuning.

### Baseline Answer

The evidence for why REALM improves open-domain question answering (QA) performance can be synthesized from the ablation results on NaturalQuestions-Open noted in the context. REALM's effectiveness is demonstrated through several interconnected factors:

1. **Retrieval Quality**: The analysis reports how often the gold answer appears in the top-5 retrievals prior to any fine-tuning. This metric isolates the impact of the retriever's quality as improved during pre-training. The fact that this is highlighted suggests that REALM’s retriever is more capable of fetching relevant documents containing the correct answer compared to prior methods, thereby enhancing QA performance directly through better retrieval results [1][2][3][4][5].

2. **Pre-Training Contributions**: The improvement in retrieval performance before fine-tuning indicates that REALM’s pre-training procedure effectively improves the retriever. This pre-training helps the model learn representations that facilitate locating the gold answers in retrieved documents even without task-specific fine-tuning. Thus, pre-training critically enhances both retrieval and downstream QA effectiveness [1][2][3][4][5].

3. **Downstream Fine-Tuning**: Beyond pre-training improvements, the context emphasizes end-to-end results after applying fine-tuning, implying that the full REALM pipeline—retrieval followed by reading and answer extraction—is optimized during task-specific training. This fine-tuning step refines the model’s ability to integrate retrieved information into accurate answers, further boosting performance in open-domain QA [1][2][3][4][5].

In summary, the key contributions to improved open-domain QA performance by REALM come from enhancing retrieval quality during pre-training, supported by a robust retriever that significantly increases the incidence of gold answers in top retrievals, and fine-tuning that optimizes end-to-end answer extraction.

Citations:  
[1][2][3][4][5] from data/2002.08909v1.pdf chunks 2444.0 to 2448.0

### Multi-Agent Answer

REALM improves open-domain question answering (Open-QA) performance by integrating a learned retriever that selects informative documents from a large corpus such as Wikipedia to aid the language model’s predictions [E1]. This retriever is trained end-to-end together with the language model using a performance-based signal derived from unsupervised text, which rewards retrievals that reduce the language model’s perplexity [E1]. Specifically, the retriever optimizes the marginal likelihood within a latent variable language model framework, effectively selecting documents that help predict correct answers [E1].

To manage the vast size of the candidate document corpus—often millions of documents—REALM employs computational strategies including caching, asynchronous retriever updates, and Maximum Inner Product Search (MIPS) to enable efficient retrieval [E1]. This approach contrasts with prior retrieval methods that rely on fixed indices or heuristic retrieval approaches, as REALM’s retriever is learnable and continuously updated through backpropagation, including into the MIPS index [E2].

During pre-training, improvements in the retriever are isolated by measuring how frequently the gold answer appears in the top-5 retrieved documents before any fine-tuning, demonstrating that REALM’s retrieval quality is significantly enhanced prior to downstream task adaptation [E3][E4][E5]. Finally, REALM is fine-tuned on Open-QA benchmarks such as NATURAL QUESTIONS-OPEN, WEB QUESTIONS, and CURATED TREC, achieving 4–16% absolute accuracy improvements over previous state-of-the-art systems, thus showing that retrieval quality, pre-training, and fine-tuning together contribute to substantial downstream Open-QA performance gains [E1].

### Metrics

- baseline_latency_seconds: 4.662
- orchestrator_latency_seconds: 59.035
- baseline_total_tokens: 1276
- orchestrator_total_tokens: 23875
- baseline_citation_count: 5
- orchestrator_evidence_count: 12
- fact_check_status_counts: {'supported': 7, 'unsupported': 1}

## Question 12

Type: multi-step reasoning

Explain step by step how a masked-language-model pre-training objective can improve downstream open-domain QA in REALM.

### Baseline Answer

A masked-language-model (MLM) pre-training objective can improve downstream open-domain question answering (Open-QA) in REALM through the following steps:

1. **Masked Language Modeling Pre-Training**: The MLM pre-training task involves randomly masking tokens in a sentence from a large unlabeled text corpus (like Wikipedia) and training the model to predict the masked tokens based on the surrounding context. This step helps the model learn rich syntactic, semantic, and world knowledge representations [3].

2. **Incorporating Retrieval During Pre-Training**: REALM extends the MLM approach by integrating a retrieval component that retrieves relevant documents from a large knowledge corpus before predicting the masked tokens. For each input with masked tokens, the retriever selects potentially useful documents related to the input text, and the model conditions its prediction on both the input and the retrieved documents [2][5].

3. **Training End-to-End to Improve Retrieval and Encoding**: During MLM pre-training, both the retriever and the language model encoder are trained jointly to maximize the marginal likelihood of correctly predicting the masked tokens, marginalizing over the retrieved documents as latent variables. This end-to-end training enables the retriever to learn to identify documents that actually help to reduce prediction uncertainty and helps the encoder incorporate retrieval-augmented context effectively [2][5].

4. **Salient Span Masking Scheme**: REALM uses a masking scheme that focuses on masking salient spans of text rather than random tokens or spans. This scheme ensures that the retrieval module learns to find documents that specifically help in predicting significant missing spans, improving the consistency and strength of the retrieval-learning signal, which is crucial for performance [1].

5. **Improved Knowledge Access and Prediction**: By retrieving relevant documents and conditioning predictions on them, REALM significantly increases the likelihood of predicting correct tokens for masked spans that require external knowledge, as shown in an example where REALM assigns much higher probability to the correct missing token “Fermat” compared to a standard BERT model which does not use retrieval [1].

6. **Fine-Tuning for Open-Domain QA**: After this pre-training, the model can be fine-tuned on Open-QA tasks where the input is a question and the output is an answer. Because the retrieval-augmented encoder already knows how to leverage retrieved documents effectively, it can better access and use the relevant knowledge corpus to answer questions accurately [2][3][5].

Thus, the MLM pre-training objective in REALM improves downstream Open-QA by jointly optimizing

### Multi-Agent Answer

REALM improves downstream open-domain question answering by augmenting masked-language-model (MLM) pre-training with a learned textual knowledge retriever. 

First, during pre-training, REALM employs a masked language modeling task where the model predicts the original value of each masked token in the input sequence [E5]. This MLM pre-training differs slightly from fine-tuning but fundamentally focuses on reconstructing masked inputs [E5].

Second, unlike traditional language models that store knowledge solely within their parameters, REALM explicitly integrates a learned textual knowledge retriever component into the pre-training process [E1][E2]. This retriever enables the model to actively retrieve relevant external textual information during pre-training rather than relying purely on encoded parameter knowledge [E1].

Third, by requiring the model to retrieve and incorporate relevant external knowledge in the masked token prediction task, REALM explicitly exposes the role of world knowledge, grounding the model’s predictions in actual retrieved documents instead of just parameter memorization [E1][E2][E3][E4].

However, the provided evidence does not directly describe how this MLM pre-training setup translates to improved downstream open-domain question answering performance, so the exact downstream benefit is not documented in these notes.

### Metrics

- baseline_latency_seconds: 6.961
- orchestrator_latency_seconds: 48.213
- baseline_total_tokens: 5359
- orchestrator_total_tokens: 13642
- baseline_citation_count: 5
- orchestrator_evidence_count: 24
- fact_check_status_counts: {'unsupported': 3, 'supported': 5}

## Question 13

Type: multi-step reasoning / error analysis

If REALM retrieves an irrelevant document, how would that affect p(z|x), p(y|z,x), and the final answer prediction?

### Baseline Answer

If REALM retrieves an irrelevant document, this would negatively impact the probabilities and the final prediction in the following way:

1. The retrieval distribution p(z|x) assigns the probability of selecting document z given input x based on a relevance score f(x, z). If a document z is irrelevant, it is less useful or even harmful for predicting the correct output y.

2. The likelihood of predicting the output given that document and input, p(y|z, x), would likely be low for an irrelevant document because the document does not contain helpful information for the prediction.

3. The final answer prediction p(y|x) is computed by marginalizing over all documents z:  
   \[
   p(y|x) = \sum_z p(y|z, x) p(z|x)
   \]
   If an irrelevant document z is retrieved with a nonzero p(z|x), its low p(y|z, x) would contribute little or negatively to the final overall likelihood p(y|x).

4. From the gradient update perspective, the factor \( r(z) = [p(y|z,x)/p(y|x)-1]p(z|x) \) governs how the score f(x, z) is updated. For irrelevant documents, p(y|z, x) < p(y|x), so r(z) is negative. This means the retriever is discouraged from assigning high relevance scores to irrelevant documents, reducing p(z|x) for these documents over training [2].

In summary, retrieving an irrelevant document leads to a lower conditional prediction probability p(y|z, x), and because p(z|x) is modeled to favor documents with better prediction probabilities, the model will down-weight irrelevant documents in p(z|x). This reduces their harmful effect on the final prediction p(y|x), but if irrelevant documents are strongly retrieved, the final answer prediction accuracy can degrade.

Citations:
[1] Appendix A and B from the REALM paper explain the gradient derivation and connection between p(z|x), p(y|z,x), and p(y|x).  
[2] Explains how the retriever learns to increase scores of relevant documents and decrease those of irrelevant ones based on p(y|z,x) vs p(y|x).  
[4] Defines the generative process: p(y|x) = sum over z of p(y|z,x) p(z|x).

### Multi-Agent Answer

If REALM retrieves an irrelevant document, the distribution over retrieved documents p(z|x) would assign some weight to this document based on its retrieval score; the retriever is trained to improve retrieval of relevant documents, thus typically favoring those that help prediction accuracy [E1]. Because the document is irrelevant, the conditional probability p(y|z,x)—which represents the likelihood of the answer y given input x and document z—would likely be less accurate, as the information in z does not support a correct prediction; however, direct evidence on the precise effect on p(y|z,x) is not provided in the notes [E1]. Consequently, the final answer prediction, which integrates over both p(z|x) and p(y|z,x), would be negatively affected, since the quality of retrieval and the correctness of answer extraction from retrieved documents determine overall performance [E1].

### Metrics

- baseline_latency_seconds: 5.513
- orchestrator_latency_seconds: 54.148
- baseline_total_tokens: 4469
- orchestrator_total_tokens: 18852
- baseline_citation_count: 5
- orchestrator_evidence_count: 13
- fact_check_status_counts: {'unsupported': 1, 'supported': 4}

## Question 14

Type: limitation/uncertainty

What limitations, uncertainties, or missing comparisons should be noted when interpreting REALM's reported results?

### Baseline Answer

When interpreting REALM's reported results, it is important to note some limitations and considerations. The reported metric on how often the gold answer appears in the top-5 retrievals is given before any fine-tuning, which helps isolate the retriever's contribution during pre-training. However, this also implies that the effects of fine-tuning on retrieval performance are not captured in this metric, potentially limiting understanding of the end-to-end system's improvements. Additionally, the context does not provide details on comparisons with other retrieval or question-answering systems, leaving a gap in benchmarking REALM's relative effectiveness. Therefore, missing or limited direct comparisons and the distinct stages of evaluation (pre-fine-tuning vs. end-to-end) should be considered when interpreting the reported results [1][2][3][4][5].

Citations:
[1][2][3][4][5] - data/2002.08909v1.pdf, chunks 2505.0, 2506.0, 2507.0, 2515.0, 2516.0

### Multi-Agent Answer

When interpreting REALM’s reported results, several limitations and uncertainties should be noted. The study reports how frequently the gold answer appears in the top-5 retrieved documents before any fine-tuning is applied, which is intended to isolate the contribution of improving the retriever during pre-training [E1][E2]. However, the exact numerical values or percentages for this frequency are not provided in the available evidence, limiting the ability to assess the magnitude of this impact [E5]. Furthermore, while this metric isolates retriever improvement separately from end-to-end fine-tuning results, the evidence does not include comparisons to other retrieval-based models or ablation studies that would contextualize the effectiveness of REALM’s retriever relative to alternatives [E3][E4]. Because of this absence, there is uncertainty regarding how REALM’s retriever performance and its isolated improvements compare with other systems or baselines. Additional information on these comparative or ablation aspects is missing from the provided evidence.

### Metrics

- baseline_latency_seconds: 2.907
- orchestrator_latency_seconds: 47.240
- baseline_total_tokens: 1026
- orchestrator_total_tokens: 13849
- baseline_citation_count: 5
- orchestrator_evidence_count: 17
- fact_check_status_counts: {'supported': 3, 'unsupported': 2}

## Question 15

Type: citation grounding / uncertainty

Which claims about REALM's performance or mechanism cannot be verified unless the answer cites specific experimental evidence from the paper?

### Baseline Answer

Claims about REALM's performance or mechanism that cannot be verified without citing specific experimental evidence from the paper include statements regarding how often the gold answer appears in the top-5 retrievals before applying any fine-tuning and the precise contribution of improving the retriever during pre-training. These claims require concrete experimental results to validate, as noted by the mention that reporting such metrics "more significantly isolates the contribution of improving the retriever during pre-training" [1][2][3][4][5]. Without the experimental data or results sections providing this evidence, these claims remain unverifiable.

Citations:  
[1] data/2002.08909v1.pdf chunk_id: 2002.08909v1-2519-85845dc0e72f4b186049157c  
[2] data/2002.08909v1.pdf chunk_id: 2002.08909v1-2515-ae82d984a290fbec4045dab2  
[3] data/2002.08909v1.pdf chunk_id: 2002.08909v1-2516-3bc1aec1953debf7d09c5193  
[4] data/2002.08909v1.pdf chunk_id: 2002.08909v1-2506-f86a7f4f9c2ce85c860e99f0  
[5] data/2002.08909v1.pdf chunk_id: 2002.08909v1-2507-b35b7c55c3d9e405e35420e5

### Multi-Agent Answer

Claims about REALM’s performance or mechanism—specifically regarding its end-to-end results and how often the gold answer appears in the top-5 retrievals prior to any fine-tuning—cannot be verified without citing specific experimental evidence from the paper [E1][E2]. The frequency of the gold answer appearing in these top-5 retrievals is reported because this metric more significantly isolates the contribution of improving the retriever during pre-training [E1][E2]. While sources emphasize the importance of this retrieval metric for understanding retriever improvements [E3][E4][E5], the explicit necessity of direct experimental data to validate such claims is implied rather than directly stated, indicating some uncertainty in this interpretation [E3][E4]. Therefore, assertions about retrieval frequency and retriever contribution are best supported by direct experimental measurements as presented in the study [E1][E2].

### Metrics

- baseline_latency_seconds: 4.010
- orchestrator_latency_seconds: 42.281
- baseline_total_tokens: 1145
- orchestrator_total_tokens: 13813
- baseline_citation_count: 5
- orchestrator_evidence_count: 11
- fact_check_status_counts: {'supported': 4}
