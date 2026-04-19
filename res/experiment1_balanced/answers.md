# experiment1: balanced multi-agent config

## Agent Configuration

- top_k: 5
- orchestrator_model: gpt-4.1-mini
- search_model: gpt-4.1-mini
- summarization_model: gpt-4.1-mini
- fact_check_model: gpt-4.1-mini
- final_synthesis_model: gpt-4.1-mini

## Question 1

What is REALM and how does it differ from traditional language models like BERT in terms of knowledge storage and retrieval?

### Baseline Answer

REALM (Retrieval-Augmented Language Model) is a novel framework that augments language model pre-training with a learned textual knowledge retriever. Unlike traditional language models like BERT, which store knowledge within their model parameters, REALM explicitly separates the storage and retrieval of world knowledge. It allows the model to retrieve relevant textual knowledge dynamically during inference rather than relying solely on the knowledge encoded in the parameters. This approach makes the role of external knowledge explicit and facilitates more effective use of up-to-date or large-scale textual information beyond what is statically encoded in the model's weights [1][2][3][4][5].

Citations:  
[1][2][3][4][5] data/2002.08909v1.pdf

### Multi-Agent Answer

REALM (Retrieval-Augmented Language Model) is a novel pre-training framework that enhances traditional language model pre-training by integrating a learned textual knowledge retriever. Unlike conventional models such as BERT, which store world knowledge implicitly and solely within their neural network parameters, REALM explicitly exposes this knowledge by requiring the model to retrieve relevant textual information from an external corpus—such as Wikipedia—during pre-training, fine-tuning, and inference [E1–E17]. 

This retrieval mechanism allows REALM to access and incorporate up-to-date and extensive information beyond what can be feasibly stored in model parameters, making the incorporation of world knowledge more interpretable and modular compared to traditional parameter-only approaches [E7, E9]. Furthermore, REALM’s knowledge retriever is trained in an unsupervised manner using masked language modeling as the learning signal, with backpropagation performed through a retrieval step that considers millions of documents. This contrasts with traditional language models that rely solely on parameter storage of knowledge without explicit retrieval [E7]. 

In summary, REALM differs from models like BERT by explicitly integrating an external knowledge retrieval step into language model pre-training, shifting from implicit knowledge stored in parameters to an explicit, retriever-based access to textual world knowledge [E1–E17].

No conflicting evidence was found, and details on specific implementation or performance metrics beyond those cited here are not provided in the supplied evidence.

### Metrics

- baseline_latency_seconds: 2.606
- orchestrator_latency_seconds: 62.617
- baseline_total_tokens: 942
- orchestrator_total_tokens: 24955
- baseline_citation_count: 5
- orchestrator_evidence_count: 18
- fact_check_status_counts: {'weakly_supported': 6, 'supported': 2}

## Question 2

Explain how the retrieve-then-predict framework works in REALM, including the role of the latent variable z and backpropagation through the retriever.

### Baseline Answer

The retrieve-then-predict framework in REALM works by decomposing the probability of generating an output \( y \) given an input \( x \) into two sequential steps involving a latent variable \( z \), which represents documents retrieved from a knowledge corpus \( Z \).

1. **Retrieval Step:**
   Given an input \( x \) (which can be a masked sentence during pre-training or a question during fine-tuning), REALM first samples or retrieves relevant documents \( z \) from the corpus \( Z \) according to a learned retrieval distribution \( p(z | x) \). This distribution is modeled via a neural knowledge retriever that computes a relevance score \( f(x, z) \) between \( x \) and each document \( z \) using dense vector embeddings and softmax normalization:

   \[
   p(z | x) = \frac{\exp f(x, z)}{\sum_{z'} \exp f(x, z')}
   \]

   where the relevance score \( f(x, z) \) is computed as the inner product of embedding vectors derived from BERT-style Transformers for both the input \( x \) and the document \( z \). Hence:

   \[
   f(x, z) = \text{Embed}_{\text{input}}(x)^\top \text{Embed}_{\text{doc}}(z)
   \]

2. **Prediction Step:**
   Conditioning on both the retrieved documents \( z \) and the original input \( x \), REALM predicts the output \( y \) with probability \( p(y | z, x) \).

3. **Latent Variable Marginalization:**
   Because multiple possible documents \( z \) could be relevant, \( z \) is treated as a latent variable, and the overall likelihood of generating \( y \) given \( x \) is marginalized over all documents:

   \[
   p(y | x) = \sum_{z \in Z} p(y | z, x) p(z | x)
   \]

The latent variable \( z \) thus represents the retrieved knowledge document influencing the prediction.

4. **Backpropagation Through the Retriever:**
   Training REALM involves maximizing the likelihood \( p(y | x) \). The gradient of the log-likelihood with respect to the retriever’s parameters \(\theta\) is:

   \[
   \nabla \log p(y | x) = \sum_{z \in Z} r

### Multi-Agent Answer

The retrieve-then-predict framework in REALM functions by augmenting standard language model pre-training algorithms with a learned textual knowledge retriever. This setup explicitly incorporates retrieval of relevant world knowledge from an external corpus during processing, contrasting with conventional language models that store knowledge solely within their parameters [E1, E2, E3, E4, E5, E8, E9].

In this framework, a latent variable \( z \) represents the retrieval of a document or textual snippet relevant to the input query \( x \). Although explicit, detailed descriptions of \( z \) as a latent retrieved document are limited in the evidence, the gradient derivations involving \( z \) in the REALM objective support this interpretation. The model’s prediction depends on both the input \( x \) and the sampled latent retrieval \( z \), effectively decomposing the pre-training objective over these latent retrieved documents [E6]. However, the evidence for this decomposition is somewhat indirect and conceptual rather than fully explicit.

A critical aspect of REALM’s training is enabling backpropagation through the retriever. This is achieved by computing the gradient of the pre-training objective with respect to the retriever’s parameters using conditional Bayes’ rule. Specifically, the gradient can be expressed as \(\nabla \log p(y \mid x) = \sum_z [p(z \mid y, x) - p(z \mid x)] \nabla f(x, z)\), where \( y \) is the target output and \( f \) represents the model's scoring function. This formulation allows gradient-based updates to the retriever by comparing the posterior distribution over retrieved documents given the target versus the prior retrieval distribution [E6].

In summary, REALM’s retrieve-then-predict architecture explicitly models retrieval as a latent variable \( z \), conditions predictions on retrieved texts, and trains the retriever end-to-end via backpropagation using conditional Bayes’ rule to effectively integrate retrieval into language model pre-training. The available evidence supports these key mechanisms but lacks a fully detailed step-by-step explanation of \( z \)’s role and the objective’s decomposition, indicating some uncertainty in those details.

### Metrics

- baseline_latency_seconds: 5.982
- orchestrator_latency_seconds: 53.364
- baseline_total_tokens: 3153
- orchestrator_total_tokens: 20694
- baseline_citation_count: 5
- orchestrator_evidence_count: 14
- fact_check_status_counts: {'weakly_supported': 8, 'supported': 4}

## Question 3

What evidence does the paper provide that REALM improves Open-domain Question Answering performance compared to methods like ORQA, and what are the key reasons for this improvement?

### Baseline Answer

The paper provides evidence that REALM improves Open-domain Question Answering (QA) performance by presenting results on the NaturalQuestions-Open dataset, which include ablation studies on critical components of REALM. A key metric reported is the frequency with which the gold answer appears in the top-5 retrieved documents before any fine-tuning is applied. This metric highlights the improvement in the retriever due to pre-training, isolating its contribution to the end-to-end QA performance. This suggests that REALM's stronger retriever, enhanced during pre-training, is a central reason for its improved QA performance compared to prior methods like ORQA [1][2][3][4][5].

Citations:  
[1]-[5] data/2002.08909v1.pdf, chunks 2444.0 to 2448.0

### Multi-Agent Answer

The paper provides evidence that REALM improves Open-domain Question Answering (QA) performance primarily through enhancements to its retriever component via a dedicated pre-training phase. Specifically, the study presents results on the NaturalQuestions-Open dataset where critical components of the REALM model are ablated to assess their impact [E1–E5]. 

Beyond reporting standard end-to-end QA performance, the paper uniquely introduces and emphasizes a metric measuring how often the gold answer appears in the top-5 retrieved passages before any fine-tuning is applied. This pre-fine-tuning metric more directly isolates the effectiveness of the retriever itself, separate from the reader module or joint training effects [E1–E5]. By focusing on this retrieval-level performance, the authors highlight that the pre-training process substantially enhances the retriever’s ability to surface relevant documents containing the answer [E1–E5].

However, while this isolation of retriever improvements is well supported, the evidence does not explicitly provide quantitative comparisons between REALM and methods like ORQA or other prior approaches. Nor does it directly show that REALM’s retriever alone outperforms these baselines before fine-tuning. Thus, claims about superiority relative to ORQA or other methods are only weakly supported by the available evidence and would require additional comparative data.

In summary, the key reasons for REALM’s improved Open-domain QA performance, as evidenced by the paper, are:

- A focused pre-training phase that enhances the retriever’s capability to find relevant documents;

- Reporting and utilizing a pre-fine-tuning "gold answer in top-5 retrievals" metric that isolates retriever contribution;

- Ablation studies confirming the significant role of the retriever component in the overall system’s performance.

The comparative advantage over methods like ORQA is suggested but not explicitly demonstrated in the provided evidence [E1–E5].

### Metrics

- baseline_latency_seconds: 2.741
- orchestrator_latency_seconds: 30.491
- baseline_total_tokens: 1048
- orchestrator_total_tokens: 9035
- baseline_citation_count: 5
- orchestrator_evidence_count: 5
- fact_check_status_counts: {'weakly_supported': 7, 'supported': 1}
