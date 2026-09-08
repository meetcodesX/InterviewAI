# Generative AI Interview Questions

## Easy

### Q1: What is Generative AI and how does it differ from Discriminative AI?
**Answer:** Generative AI refers to artificial intelligence models capable of generating new, synthetic data such as text, images, audio, or code that resembles human-generated content. In contrast, discriminative AI models focus on classifying, predicting, or finding boundaries between existing data points based on conditional probability P(Y|X). While a discriminative model might identify whether an image contains a cat, a generative model models the underlying data distribution P(X) or joint distribution P(X, Y) to create a completely new image of a cat. Generative AI relies heavily on foundational deep learning architectures like Transformers, Diffusion models, and GANs.
**Key Points:**
- Generative AI produces novel content across modalities (text, code, images, audio).
- Discriminative AI models conditional probability P(Y|X) for classification and regression tasks.
- Generative AI models data distribution P(X) or joint distribution P(X, Y) to synthesize new samples.
- Fundamental shift from recognition/classification to creation/synthesis.
**Evaluation Criteria:** Candidate should clearly state the mathematical/conceptual distinction between P(Y|X) and P(X) or P(X, Y), provide practical examples of both types, and identify modern generative architectures.

### Q2: What is the Transformer architecture and why did it replace RNNs/LSTMs in NLP?
**Answer:** The Transformer is a deep learning architecture introduced in the 2017 paper "Attention Is All You Need" that relies entirely on self-attention mechanisms instead of recurrent or convolutional layers. Recurrent neural networks (RNNs and LSTMs) process sequences sequentially token-by-token, which creates a computational bottleneck preventing parallelization across GPU clusters and leads to vanishing gradients over long context lengths. Transformers eliminate recurrence by processing all tokens simultaneously and using positional encodings to preserve sequence order. This parallel processing capability allows models to scale up efficiently on massive datasets and capture long-range contextual relationships far more effectively.
**Key Points:**
- Replaces sequential recurrent processing with multi-head self-attention.
- Eliminates the O(n) sequential execution bottleneck, enabling full GPU parallel training.
- Solves vanishing and exploding gradient problems across long token contexts.
- Uses positional encodings to inject token order information into parallelized representations.
**Evaluation Criteria:** Look for mentions of sequential processing limitations in RNNs, parallelization benefits during training, self-attention replacing recurrence, and how positional encoding is required.

### Q3: What is the Self-Attention mechanism and how does it work conceptually?
**Answer:** Self-attention allows an input sequence of tokens to dynamically attend to and weigh the importance of every other token in the same sequence when computing representations. For each token, the model projects its input embedding into three distinct vectors: Query (Q), Key (K), and Value (V). The compatibility score between the Query of a target token and the Keys of all other tokens is computed using scaled dot products, normalized via softmax to produce attention weights, and then used to compute a weighted sum of the Values. This mechanism allows words with ambiguous meanings to incorporate context directly from related words elsewhere in the sentence regardless of distance.
**Key Points:**
- Projects token embeddings into Query (Q), Key (K), and Value (V) representations.
- Computes attention scores using the formula: Softmax((Q * K^T) / sqrt(d_k)) * V.
- The scaling factor sqrt(d_k) prevents dot-product values from growing too large and pushing softmax into vanishing gradient regions.
- Enables direct pairwise context interaction without relying on intermediate steps.
**Evaluation Criteria:** Candidate should articulate the roles of Queries, Keys, and Values, explain why the scaling factor sqrt(d_k) is necessary, and describe how the attention distribution weights the values.

### Q4: What is the difference between Encoder-only, Decoder-only, and Encoder-Decoder architectures?
**Answer:** Encoder-only models, such as BERT, process the entire input bidirectionally, making them ideal for understanding tasks like classification, named entity recognition, and sentiment analysis. Decoder-only models, such as the GPT family, use causal masking to restrict attention to preceding tokens, making them autoregressive and optimized for next-token prediction and open-ended text generation. Encoder-Decoder models, such as T5 and BART, combine both: the bidirectional encoder encodes the full input sequence while the autoregressive decoder generates output tokens conditioned on both previous outputs and encoder representations, which is well-suited for translation and summarization.
**Key Points:**
- Encoder-only (e.g., BERT): Bidirectional attention, designed for sequence classification and feature extraction.
- Decoder-only (e.g., GPT, Llama): Causal/autoregressive attention, designed for text generation and prompt completion.
- Encoder-Decoder (e.g., T5, BART): Separate source encoding and target generation, standard for sequence-to-sequence translation.
- Architectural design determines the masking strategy applied to the attention matrix.
**Evaluation Criteria:** Candidate should name representative models for each category, describe their attention masking properties (bidirectional vs causal), and identify their typical use cases.

### Q5: What is Tokenization and why is it necessary for Large Language Models?
**Answer:** Tokenization is the preprocessing step that breaks down raw textual strings into discrete numerical IDs that a neural network can process mathematically. Because neural networks cannot directly ingest variable-length strings, text must be mapped to discrete integer indices corresponding to rows in an embedding lookup table. Modern LLMs use subword tokenization algorithms such as Byte-Pair Encoding (BPE), WordPiece, or SentencePiece, which balance vocabulary size and sequence length by keeping frequent words intact while decomposing rare or unseen words into subword units. This approach prevents out-of-vocabulary (OOV) errors while keeping the vocabulary computationally manageable (e.g., 32k to 128k tokens).
**Key Points:**
- Maps textual characters or words into discrete integer token IDs for embedding lookup.
- Balances vocabulary size against context window consumption using subword algorithms (BPE, WordPiece, SentencePiece).
- Solves out-of-vocabulary (OOV) errors by falling back to character or byte-level chunks.
- Token boundaries directly impact arithmetic, code syntax, and multilingual performance.
**Evaluation Criteria:** Check for understanding of subword algorithms (BPE/WordPiece), why word-level and character-level tokenization have flaws, and how tokenization affects context length and vocabulary size.

### Q6: What are Word and Token Embeddings in LLMs?
**Answer:** Embeddings are high-dimensional continuous vector representations where semantic and syntactic relationships between words or tokens are captured as geometric distances and directions. In LLMs, an initial token embedding matrix maps discrete token IDs into dense vectors of dimension d_model (e.g., 4096 dimensions). As tokens pass through transformer layers, contextual embeddings are constructed, meaning a word's representation shifts dynamically based on its surrounding context. Semantic similarity is often quantified using cosine similarity or Euclidean distance between these continuous vectors in the latent space.
**Key Points:**
- Converts discrete token integers into continuous dense vectors in latent space.
- Initial static lookup table maps token IDs; transformer layers convert them into contextual representations.
- Distance metrics (cosine similarity, dot product) correspond to semantic relatedness.
- Dimensionality reflects model capacity (e.g., 768 for BERT-base, 4096+ for modern frontier LLMs).
**Evaluation Criteria:** Candidate should explain the transition from one-hot vectors to dense representations, distinguish between static lookup embeddings and contextual embeddings, and mention similarity metrics.

### Q7: What is Prompt Engineering and what are common techniques like Zero-shot and Few-shot prompting?
**Answer:** Prompt engineering is the practice of structuring, phrasing, and designing input prompts to steer generative language models toward producing desired, accurate, and structured outputs without modifying model weights. Zero-shot prompting involves presenting a task directly to the model with instructions but no demonstrations or prior examples. Few-shot prompting (in-context learning) includes a small number of input-output demonstrations within the prompt, establishing an implicit pattern and formatting standard for the model to follow. By providing context and examples, few-shot prompting dramatically improves performance on complex reasoning, categorization, and formatting tasks.
**Key Points:**
- Steers pretrained model behavior purely through natural language input context without weight updates.
- Zero-shot relies on pretrained world knowledge and instruction-following capability without examples.
- Few-shot provides exemplar pairs (Input -> Output) to prime the model for tone, format, and reasoning paths.
- Relies on the in-context learning emergence observed in large transformer models.
**Evaluation Criteria:** Candidate should accurately describe zero-shot vs few-shot prompting, explain how in-context learning works without gradient descent, and provide clear practical examples.

### Q8: What is Temperature in LLM sampling and how does it affect generation?
**Answer:** Temperature is a hyperparameter applied to the logits output by an LLM before passing them through the softmax function to compute token selection probabilities. Mathematically, each logit z_i is divided by temperature T: softmax(z_i / T). When T is low (e.g., 0.1 to 0.3), differences between logits are amplified, making the model deterministic, focused, and prone to picking the highest-probability tokens. When T is high (e.g., 0.8 to 1.5), the probability distribution becomes flatter and more uniform, encouraging diverse, creative, and varied token sampling at the risk of incoherence or hallucinations.
**Key Points:**
- Scales pre-softmax logits: P(token_i) = exp(z_i / T) / sum(exp(z_j / T)).
- Low temperature (approaching 0) produces greedy, deterministic, and conservative outputs.
- High temperature (> 1.0) flattens distributions, increasing entropy, creativity, and stochasticity.
- T=0 is equivalent to greedy decoding (selecting argmax logit).
**Evaluation Criteria:** The candidate should state the exact formula location (pre-softmax logit scaling), describe the effect on the probability distribution curve, and give appropriate use cases (e.g., coding vs creative writing).

### Q9: What is Hallucination in Large Language Models and why does it occur?
**Answer:** Hallucination occurs when an LLM generates text that sounds confident, authoritative, and fluent but is factually incorrect, nonsensical, or ungrounded in real-world truth or provided source material. It arises fundamentally because autoregressive LLMs are trained to maximize token likelihood given prior context—acting as statistical pattern matchers—rather than executing factual truth verification. Factors contributing to hallucinations include noisy or conflicting training data, catastrophic forgetting, memorization limits, and over-extrapolation when prompted outside the model's knowledge distribution. Mitigation strategies include Retrieval-Augmented Generation (RAG), strict system prompting, grounded citation requirements, and chain-of-thought verification.
**Key Points:**
- Generation of factually false or ungrounded claims with high linguistic confidence.
- Root cause: Models optimize statistical next-token probability, not formal truth conditions.
- Aggravated by out-of-distribution prompts, noisy pretraining corpora, and parametric knowledge decay.
- Mitigated by external retrieval (RAG), tool use, fact-checking verifiers, and low temperature.
**Evaluation Criteria:** Assess whether the candidate understands that LLMs lack an internal truth-verification engine, explains next-token probability optimization, and suggests realistic mitigation strategies.

### Q10: What is Responsible AI and what are its main pillars in Generative AI?
**Answer:** Responsible AI is a framework of governance, engineering practices, and ethical principles designed to ensure generative models are developed and deployed safely, fairly, and reliably. Its core pillars include fairness and bias mitigation (ensuring equitable treatment across demographic groups), safety and toxicity prevention (guarding against hate speech, self-harm, and weapons synthesis), privacy and copyright protection (preventing data leakage and intellectual property infringement), and transparency and explainability (disclosing AI identity and watermarking synthetic outputs). Implementing Responsible AI involves red-teaming, reinforcement learning from human feedback, guardrail filters, and differential privacy during data curation.
**Key Points:**
- Core pillars: Fairness, Safety/Harmlessness, Privacy/Security, Reliability, and Transparency.
- Prevents toxic, illegal, discriminatory, or IP-infringing generations.
- Involves both pre-training curation and post-training guardrails (e.g., Llama Guard, NeMo Guardrails).
- Includes watermarking and provenance tracking to combat disinformation.
**Evaluation Criteria:** Look for a comprehensive breakdown of key safety tenets (bias, toxicity, IP, privacy), along with concrete engineering interventions like guardrails and red-teaming.

---

## Medium

### Q1: Explain Multi-Head Attention and why multiple heads are superior to a single attention head.
**Answer:** Multi-Head Attention extends the basic self-attention mechanism by projecting the Query, Key, and Value vectors h times into different lower-dimensional subspaces using learned linear projections. Each "head" computes scaled dot-product attention independently across these projected dimensions (d_k = d_model / h), allowing the model to simultaneously focus on information from different representation subspaces at different positions. For example, one attention head might track syntactic dependencies (like subject-verb agreement), while another captures semantic relations or positional proximity. Finally, the outputs of all attention heads are concatenated and linearly projected back to the original model dimension d_model.
**Key Points:**
- Projects Q, K, and V into h parallel subspaces of dimension d_k = d_model / h.
- Computes attention concurrently across heads: MultiHead(Q,K,V) = Concat(head_1, ..., head_h) * W_O.
- Allows simultaneous attention to diverse relational patterns (syntactic, semantic, positional).
- Keeps total computational complexity comparable to a single full-dimensional head.
**Evaluation Criteria:** Candidate should explain why single-head attention averages out nuanced signals, detail the concatenation and projection step, and explain how dimensionality per head preserves computational efficiency.

### Q2: What is the difference between Pre-training, Fine-Tuning, and Instruction Tuning?
**Answer:** Pre-training is the self-supervised phase where a base model learns general language patterns, syntax, and factual knowledge by predicting masked or next tokens across trillions of tokens of unlabelled web text. Fine-tuning adapts this pre-trained foundation model to a specific domain or downstream task by training on a curated, labeled dataset with a lower learning rate. Instruction tuning is a specific subtype of fine-tuning where the training dataset consists of paired instruction prompts and high-quality responses across hundreds of diverse tasks. Instruction tuning bridges the gap between raw statistical text continuation and practical, helpful assistant behavior.
**Key Points:**
- Pre-training: Self-supervised learning on massive unlabeled corpora (trillions of tokens); computationally intensive.
- Fine-Tuning: Supervised adaptation of model weights on task-specific or domain-specific datasets.
- Instruction Tuning: Supervised fine-tuning (SFT) specifically formatted as instruction-response pairs to train conversational alignment.
- Shifts model behavior from raw autoregressive text completion to executing user intent.
**Evaluation Criteria:** Candidate should clearly delineate dataset requirements, training objectives, and computational scale between the three stages, highlighting how instruction tuning transforms a raw base model into an assistant.

### Q3: How does Reinforcement Learning from Human Feedback (RLHF) work?
**Answer:** RLHF aligns a pre-trained, instruction-tuned LLM with human values (helpfulness, honesty, harmlessness) through a three-step process. First, human annotators rank multiple model-generated candidate responses to diverse prompts from best to worst. Second, a separate Reward Model is trained using pairwise ranking loss to output a scalar reward score reflecting human preference for any given prompt-response pair. Third, the policy (the target LLM) is optimized using reinforcement learning algorithms like Proximal Policy Optimization (PPO) to maximize the expected reward score, while incorporating a KL-divergence penalty against the original reference model to prevent the policy from degenerating or mode-collapsing (reward hacking).
**Key Points:**
- Step 1: Supervised fine-tuning (SFT) to establish base conversational ability.
- Step 2: Training a Reward Model on human-annotated comparative preference rankings.
- Step 3: Policy optimization via PPO or Direct Preference Optimization (DPO) to maximize reward.
- Uses a KL-divergence penalty between current policy and reference model to prevent policy drift and reward hacking.
**Evaluation Criteria:** Candidate must walk through the three distinct stages (SFT, Reward Modeling, RL fine-tuning with PPO), explain the reward signal, and explain why the KL penalty is necessary.

### Q4: Compare LoRA (Low-Rank Adaptation) and Full Fine-Tuning. Why is LoRA efficient?
**Answer:** Full fine-tuning updates all parameters of an LLM during backpropagation, requiring massive GPU VRAM to store optimizer states (e.g., Adam stores 8 bytes per parameter for momentum and variance) and generating huge checkpoints for each domain. LoRA freezes the pre-trained model weights W_0 and injects trainable rank-decomposition matrices A and B into selected transformer layers (typically attention projection matrices), such that W = W_0 + (B * A) * (alpha / r), where r << min(d_in, d_out). This drastically reduces trainable parameters by 99% or more, reduces memory footprints during training by avoiding optimizer state overhead for frozen weights, and allows serving multiple fine-tuned models on a single base model by swapping small adapter weights at inference.
**Key Points:**
- LoRA decomposes weight updates: Delta_W = B * A, where B is (d x r) and A is (r x k) with rank r << d.
- Freezes base model weights W_0, dramatically reducing memory needed for gradients and optimizer states.
- Decreases storage requirements from tens of gigabytes per model to megabytes per adapter.
- Incurs zero inference latency penalty when adapter matrices are merged back into base weights: W = W_0 + Delta_W.
**Evaluation Criteria:** The candidate must explain the rank decomposition equation (B*A), discuss memory reduction via frozen optimizer states, and explain the inference merge capability.

### Q5: What is Chain-of-Thought (CoT) prompting and how does it improve complex reasoning?
**Answer:** Chain-of-Thought (CoT) prompting is an in-context prompting technique that encourages large language models to generate a series of intermediate reasoning steps before arriving at a final answer. By explicitly decomposing multi-step mathematical, logical, or symbolic reasoning problems into discrete sub-problems, the model allocates more compute (tokens) to "think" sequentially. In standard prompting, the model must jump directly to the final answer in a single forward pass, which often fails for complex deductions; CoT provides an autoregressive scratchpad where each intermediate deduction becomes context for subsequent calculations. It can be elicited via few-shot demonstrations or zero-shot prompts like "Let's think step by step."
**Key Points:**
- Elicits step-by-step intermediate reasoning paths prior to final answer generation.
- Zero-shot CoT uses trigger phrases like "Think step-by-step"; Few-shot CoT provides explicit worked reasoning examples.
- Expands test-time compute by allowing intermediate tokens to act as a working memory scratchpad.
- Significantly boosts accuracy on multi-step arithmetic, commonsense, and symbolic logic tasks.
**Evaluation Criteria:** Candidate should explain why single-step decoding fails on complex reasoning, how generating intermediate tokens serves as working memory, and mention both zero-shot and few-shot variants.

### Q6: How do Top-k and Top-p (Nucleus) sampling mechanisms work during text generation?
**Answer:** Top-k and Top-p sampling are decoding techniques used to truncate the tail of low-probability tokens before sampling to prevent unnatural or nonsensical generations. Top-k sampling restricts the candidate pool to the fixed k highest-probability tokens, redistributing probability mass among them via softmax, but it fails when the probability distribution is either very flat (excluding good candidates) or very peaked (including bad tail candidates). Top-p (nucleus) sampling solves this by dynamically selecting the smallest set of tokens whose cumulative probability exceeds threshold p (e.g., 0.90). This dynamically expands the candidate set when uncertainty is high and contracts it to one or two tokens when the next token is obvious.
**Key Points:**
- Top-k: Filters candidate tokens to a static number k of top-probability choices.
- Top-p (Nucleus): Filters to a dynamic minimal set whose cumulative probability mass sums to >= p.
- Top-p dynamically adapts to the distribution's entropy (narrow for confident contexts, wide for creative contexts).
- Often combined with temperature to control both distribution flatness and tail truncation.
**Evaluation Criteria:** Look for clear mathematical intuition behind cumulative probability mass versus static count, limitations of Top-k in dynamic contexts, and how Top-p provides adaptive candidate selection.

### Q7: What are KV Caching and FlashAttention, and how do they optimize LLM inference and training?
**Answer:** KV Caching accelerates autoregressive inference by storing the Key and Value projection vectors of previous tokens in GPU memory so they do not need to be recomputed for every new generated token. Without KV caching, generating token N requires recomputing attention over all N-1 preceding tokens, resulting in O(N^2) complexity instead of O(N) per step. FlashAttention is an exact, IO-aware attention algorithm that speeds up both training and inference by tiling the computation to fit into fast GPU SRAM rather than making repeated, memory-bandwidth-bound roundtrips to high-bandwidth memory (HBM). FlashAttention reduces memory reads/writes from quadratic to linear with respect to sequence length, yielding substantial speedups without numerical approximation.
**Key Points:**
- KV Caching avoids redundant O(N^2) attention recomputations during generation by caching past keys and values.
- KV Cache growth scales with batch size, context length, and hidden dimension, creating a major GPU memory bottleneck.
- FlashAttention optimizes GPU memory hierarchy utilization (SRAM vs HBM) via mathematical tiling and online softmax.
- FlashAttention computes exact attention faster while lowering peak memory overhead from O(N^2) to O(N).
**Evaluation Criteria:** Candidate should distinguish between KV caching (inference optimization avoiding redundant computation) and FlashAttention (hardware-aware memory IO tiling for GPU SRAM), explaining their respective trade-offs.

### Q8: How do you evaluate Large Language Models both quantitatively and qualitatively?
**Answer:** LLM evaluation requires a combination of automated benchmarks, LLM-as-a-Judge frameworks, and human evaluation. Quantitative evaluations use standardized benchmarks like MMLU (multitask knowledge), GSM8k (mathematical reasoning), HumanEval (code generation), and MT-Bench (multi-turn conversation). For open-ended generation where exact match or BLEU/ROUGE metrics fail, LLM-as-a-Judge utilizes frontier models (like GPT-4) with strict rubric prompts to score coherence, relevance, and accuracy against ground truth. Qualitative evaluation relies on human blind A/B testing (Elo rating systems like LMSYS Chatbot Arena) to measure genuine user preference and detect subtle issues like sycophancy, bias, and tone.
**Key Points:**
- Standardized benchmarks: MMLU, GSM8K, HumanEval, ARC for specific domain and reasoning capabilities.
- N-gram overlap metrics (BLEU, ROUGE) are inadequate for open-ended semantic reasoning.
- LLM-as-a-Judge: Automated evaluation with structured rubrics and reference comparisons; requires mitigation of position and length bias.
- Human Evaluation / Elo Arena: Gold standard for subjective alignment and conversational quality.
**Evaluation Criteria:** Candidate should point out the shortcomings of classical NLP metrics (BLEU/ROUGE) for LLMs, explain benchmark evaluation, describe LLM-as-a-Judge along with its known biases (verbosity, position), and mention human Elo ratings.

### Q9: What is Direct Preference Optimization (DPO) and how does it compare to PPO-based RLHF?
**Answer:** Direct Preference Optimization (DPO) is an alignment algorithm that eliminates the need to train a separate reward model or sample from the policy during training using reinforcement learning. DPO mathematically derives an exact closed-form expression that reparameterizes the reward function directly in terms of the language model policy: r(x, y) proportional to log(pi_theta(y|x) / pi_ref(y|x)). By substituting this relationship directly into the Bradley-Terry preference objective, DPO optimizes the LLM parameters using a simple binary cross-entropy loss over pairs of chosen and rejected responses. This makes DPO substantially more stable, computationally efficient, and easier to train than PPO, which requires four separate models (policy, value, reward, reference) in GPU memory.
**Key Points:**
- Bypasses explicit reward model training and complex PPO policy actor-critic updates.
- Reparameterizes Bradley-Terry preference model directly with implicit reward based on policy log ratios.
- Uses a simple binary cross-entropy loss over chosen vs rejected response pairs.
- Drastically reduces GPU memory requirements and hyperparameter instability compared to PPO.
**Evaluation Criteria:** Look for understanding of why PPO is complex (multi-model memory overhead, actor-critic instability) and how DPO mathematically optimizes the policy directly on preference pairs.

### Q10: What are Guardrails in Generative AI applications and how do you implement them?
**Answer:** Guardrails are protective validation layers deployed around an LLM to enforce safety, security, brand compliance, and structural integrity on both user inputs and model outputs. Input guardrails sanitize prompts before reaching the LLM, detecting prompt injection attacks, jailbreaks, toxicity, and sensitive PII (personally identifiable information) via regex, vector similarity against known adversarial databases, or specialized classifier models. Output guardrails inspect the generated text before returning it to the user, verifying factual consistency (hallucination detection), filtering toxic content, redacting accidental secrets, and validating syntax (such as enforcing valid JSON schemas via constrained decoding tools like Instructor or Outlines).
**Key Points:**
- Bidirectional protection: Input guardrails (prompt injection, jailbreaks, PII) and output guardrails (toxicity, hallucination, schema enforcement).
- Implemented using specialized small models (e.g., Llama Guard), semantic classifiers, and regex/heuristics.
- Constrained decoding (Outlines, Guidance) guarantees syntactically valid structural outputs (e.g., JSON/regex).
- Balances safety filtering against latency overhead and false refusal rates.
**Evaluation Criteria:** Candidate should separate input from output guardrails, discuss specific attack vectors (prompt injection/jailbreaking), mention structured output enforcement, and discuss latency trade-offs.

---

## Hard

### Q1: Detail the mathematics of the Scaled Dot-Product Attention mechanism and analyze its computational and memory complexity with respect to sequence length.
**Answer:** Given input representations X of sequence length N, linear projections yield Q = X * W_Q, K = X * W_K, and V = X * W_V, where Q, K, V in R^(N x d_k). The scaled dot-product attention equation is Attention(Q, K, V) = softmax((Q * K^T) / sqrt(d_k)) * V. The matrix product Q * K^T requires multiplying an (N x d_k) matrix by a (d_k x N) matrix, producing an (N x N) attention matrix that takes O(N^2 * d_k) floating-point operations and requires O(N^2) memory to store pre-softmax logits and activation gradients. When multiplying this (N x N) matrix by V (N x d_k), another O(N^2 * d_k) operations are performed. Because both time and spatial memory scale quadratically with sequence length N, processing very long contexts becomes computationally prohibitive without optimizations like linear attention, sliding window attention, or FlashAttention.
**Key Points:**
- Full equation: Attention(Q,K,V) = Softmax((Q * K^T) / sqrt(d_k)) * V.
- Matrix dimensions: Q * K^T yields an (N x N) pairwise compatibility matrix.
- Computational time complexity is O(N^2 * d) operations; memory complexity is O(N^2) storage for attention weights.
- Quadratic dependency on N is the primary bottleneck for scaling context window length in standard Transformers.
**Evaluation Criteria:** Candidate must write out the complete matrix equation, correctly deduce matrix dimensions at each step, and explain why both computation and activation memory scale as O(N^2).

### Q2: Explain Rotary Position Embedding (RoPE) and contrast it with Absolute and Relative Positional Encodings.
**Answer:** Absolute positional encodings (like sinusoidal or learned tables) add a fixed vector to token embeddings at index position m, but they do not naturally generalize to unseen context lengths and fail to encode relative token distances directly. Relative positional encodings modify attention scores based on the scalar offset (m - n), but they introduce custom attention matrix modifications that complicate computational optimization. Rotary Position Embedding (RoPE) resolves this by encoding relative position through a rotation of the Query and Key vectors in the complex plane. RoPE applies an orthogonal rotation matrix R_Theta,m to Q and R_Theta,n to K such that their inner product <R_Theta,m * q_m, R_Theta,n * k_n> depends solely on the relative distance (m - n) and the original vectors. RoPE naturally decays attention at greater distances, preserves vector norm, and enables long-context scaling techniques like YaRN and RoPE interpolation.
**Key Points:**
- RoPE rotates 2D chunks of the Query and Key vectors by angle m*theta_i: q_m' = R_m * q_m.
- The inner product satisfies <q_m', k_n'> = g(q, k, m - n), making self-attention purely a function of relative distance.
- Preserves vector magnitude because rotation matrices are orthogonal.
- Enables context window extension via position interpolation (NTK-aware scaling, YaRN) without retraining from scratch.
**Evaluation Criteria:** Candidate should contrast absolute vs relative encodings, explain how RoPE achieves relative properties through multiplicative orthogonal transformations on Q and K, and discuss its extrapolation properties.

### Q3: How do Grouped-Query Attention (GQA) and Multi-Query Attention (MQA) work, and how do they reduce KV cache memory overhead?
**Answer:** In standard Multi-Head Attention (MHA), each of the H query heads has its own corresponding Key and Value head, requiring H * d_k key and value vectors per token stored in the KV cache during generation. Multi-Query Attention (MQA) collapses this drastically by sharing a single Key head and a single Value head across all H Query heads, slashing KV cache memory by a factor of H, but occasionally degrading model expressiveness and stability. Grouped-Query Attention (GQA) is an optimal compromise that groups the H Query heads into G groups (where 1 < G < H), sharing one Key and Value head per group. This retains near-MHA model quality and reasoning capability while reducing the KV cache memory footprint by a factor of H/G, dramatically increasing inference batch sizes and throughput for models like Llama 2/3 and Mistral.
**Key Points:**
- MHA: H query heads, H key heads, H value heads (1:1:1 ratio).
- MQA: H query heads share exactly 1 key head and 1 value head (H:1:1 ratio); maximum memory savings but slight capacity drop.
- GQA: H query heads divided into G groups, each sharing 1 key and 1 value head (H:G:G ratio).
- KV cache size during generation shrinks from 2 * H * d_k * L * B to 2 * G * d_k * L * B, unlocking larger serving batch sizes.
**Evaluation Criteria:** The candidate should clearly state the head ratios for MHA, MQA, and GQA, articulate why the KV cache is the memory bottleneck in autoregressive decoding, and explain why GQA is the modern standard.

### Q4: Explain the training objective, reward hacking, and mathematical derivation of the KL divergence penalty in RLHF/PPO.
**Answer:** The RLHF objective is to maximize the expected reward under the learned policy pi_theta while penalizing divergence from the initial reference policy pi_ref: max_theta E_(x~D, y~pi_theta)[ r_phi(x, y) - beta * D_KL(pi_theta(y|x) || pi_ref(y|x)) ]. Without the KL penalty, the policy exploits imperfections in the learned reward model r_phi—a failure mode known as reward hacking—generating repetitive, adversarial, or ungrammatical sequences that score artificially high on the proxy reward metric. The reverse KL divergence term D_KL(pi_theta || pi_ref) = sum pi_theta(y|x) * log(pi_theta(y|x) / pi_ref(y|x)) acts as a per-token penalty: r_penalized(x, y) = r_phi(x, y) - beta * (log pi_theta(y|x) - log pi_ref(y|x)). This ensures the policy remains anchored to the distribution of natural, coherent text established during supervised instruction tuning.
**Key Points:**
- Objective combines reward maximization with reference distribution anchoring.
- Reward hacking occurs when policy exploits proxy reward model blind spots, generating nonsensical high-scoring text.
- Reverse KL penalty provides per-token negative feedback when log-ratio log(pi_theta / pi_ref) grows large.
- Hyperparameter beta controls the exploration-exploitation tradeoff between reward optimization and linguistic collapse.
**Evaluation Criteria:** Candidate must write out the objective function including the KL penalty, define reward hacking with examples, and explain the exact token-level log-probability difference implementation.

### Q5: How do Mixture of Experts (MoE) architectures function, and what are the routing algorithms and load balancing challenges involved?
**Answer:** A Mixture of Experts (MoE) replaces the dense feed-forward network (FFN) layers in a transformer block with multiple independent "expert" FFN networks, using a parameterized gating (router) network to dynamically route each token to a subset of experts (typically top-k, such as top-2 out of 8 or 16). The router computes softmax over linear logits: G(x) = Softmax(TopK(KeepTopK(x * W_g, k))). While total parameter count scales dramatically (e.g., 8x7B = 45B parameters), active compute per token remains equivalent to a much smaller dense model (e.g., 12B active parameters). The critical challenge is router collapse, where a few experts receive all tokens while others starve; this is mitigated by adding auxiliary load balancing losses that penalize variance in token dispatch across experts, along with expert capacity limits that drop overflow tokens during training.
**Key Points:**
- Replaces dense FFN with multiple expert FFNs, keeping self-attention layers shared.
- Router network dynamically computes top-k gating weights for each token.
- High total parameter capacity with low active FLOPs per forward pass.
- Requires auxiliary load-balancing loss to prevent routing collapse and maintain balanced GPU expert distribution.
**Evaluation Criteria:** Candidate should explain the top-k gating mechanism, distinguish total vs active parameters, explain the router collapse failure mode, and explain how auxiliary balancing loss resolves it.

### Q6: Analyze Speculative Decoding: How does it achieve 2-3x latency reduction while preserving exact output distribution?
**Answer:** Speculative decoding accelerates autoregressive generation by pairing a small, fast "draft" model with a large, slow "target" model to generate multiple tokens per forward pass. In each iteration, the draft model autoregressively generates K speculative draft tokens in K fast steps. These K tokens are then processed simultaneously in a single parallel forward pass by the target model. A modified rejection sampling scheme evaluates each draft token sequentially: a token is accepted with probability min(1, p_target(x) / p_draft(x)); if rejected, it is resampled from the rectified distribution max(0, p_target(x) - p_draft(x)), and all subsequent draft tokens are discarded. Because the target model's acceptance criteria mathematically guarantee that the final sampled distribution exactly matches the target model's native distribution, speculative decoding provides a pure speedup with zero quality degradation.
**Key Points:**
- Small draft model proposes K tokens sequentially; large target model verifies all K tokens in a single parallel step.
- Uses modified rejection sampling: accept probability = min(1, P_target(x) / P_draft(x)).
- Resamples rejected tokens from normalized positive residue: max(0, P_target(x) - P_draft(x)).
- Mathematically provable guarantee: Output distribution is 100% identical to running the target model standalone.
**Evaluation Criteria:** Look for the two-model architecture explanation, parallel verification mechanics, rejection sampling probability formula, and the mathematical proof of zero distribution shift.

### Q7: What are the primary attack vectors against LLMs (Prompt Injection, Jailbreaking, Data Extraction) and how can systems be hardened against them?
**Answer:** Prompt injection occurs when untrusted user input overrides developer system instructions, causing the model to hijack control flow or execute unauthorized tool calls; jailbreaking uses adversarial framing, roleplay, or token-level suffixes (e.g., GCG attacks) to bypass safety alignment filters. Training data extraction involves querying models with prefix prompts to reconstruct memorized private training data, exploiting high-frequency memorization. Hardening against these attacks requires multi-layered defense-in-depth: strict separation of instruction and data channels using distinct delimiters or XML tags, dual-LLM architectures (a privileged controller validating outputs of an untrusted processor), input/output guardrail classifiers (such as Llama Guard), automated adversarial red-teaming, and differential privacy during pretraining to bound memorization.
**Key Points:**
- Direct vs Indirect Prompt Injection (malicious payload embedded in external retrieved text or webpages).
- Jailbreaking attacks exploit semantic obfuscation, hypothetical roleplay, and universal adversarial suffixes.
- Data extraction attacks exploit verbatim memorization of low-entropy training subsets.
- Defenses: Delimiter isolation, dual-LLM privileged architecture, adversarial fine-tuning, constrained tool schemas, and differential privacy.
**Evaluation Criteria:** Candidate should differentiate direct prompt injection from indirect prompt injection, explain adversarial jailbreaking mechanisms, and detail robust architectural mitigations beyond basic prompt instructions.

### Q8: Explain Continuous Batching and PagedAttention as implemented in high-throughput LLM serving engines like vLLM.
**Answer:** Traditional LLM batching requires all sequences in a batch to complete before new requests can be admitted, causing severe GPU underutilization due to dynamic sequence lengths and waiting on long-tail requests. Continuous batching (or iteration-level batching) resolves this by scheduling execution at the individual token generation step: finished sequences are evicted immediately and new requests are injected at each step. PagedAttention solves the physical memory fragmentation of the KV cache by drawing inspiration from virtual memory paging in operating systems. Instead of allocating contiguous VRAM based on maximum possible sequence length, PagedAttention allocates non-contiguous fixed-size memory blocks (pages) on-demand as tokens are generated, reducing memory waste from over 60-80% down to under 4% and enabling 2-4x higher concurrency.
**Key Points:**
- Static batching wastes GPU compute due to padding and variable generation lengths.
- Continuous/iteration-level batching schedules requests dynamically per forward token step.
- PagedAttention divides the KV cache into fixed-size physical blocks linked via a virtual page table.
- Eliminates internal and external memory fragmentation, drastically multiplying concurrent request capacity.
**Evaluation Criteria:** Candidate must explain why static batching is inefficient for autoregressive generation, contrast it with iteration-level scheduling, and detail how PagedAttention mirrors OS virtual memory management.

### Q9: Discuss the mechanics of Contrastive Representation Learning in training modern Text Embedding models (e.g., InfoNCE loss, in-batch negatives, hard negative mining).
**Answer:** Modern text embedding models are trained using contrastive learning to project semantically similar text pairs close together while pushing dissimilar pairs apart in latent space. The standard training objective is the InfoNCE loss: L = -log( exp(sim(q, p^+) / tau) / (exp(sim(q, p^+) / tau) + sum exp(sim(q, p_i^-) / tau)) ), where q is an anchor query, p^+ is a positive document, p_i^- are negative documents, and tau is a temperature parameter. In-batch negatives efficiently reuse other positive pairs in the same GPU mini-batch as negative samples without extra computation, scaling effective negative count with batch size. However, relying purely on random in-batch negatives yields easy negatives; models must incorporate hard negative mining (using BM25 or cross-encoder rerankers to select lexically similar but semantically irrelevant documents) to force the embedding model to learn fine-grained semantic nuances.
**Key Points:**
- Contrastive objective optimizes InfoNCE loss over cosine similarity metric scaled by temperature tau.
- In-batch negatives utilize all other batch elements as negative pairs at zero additional FLOP cost.
- Hard negative mining extracts false positives (high lexical overlap, zero relevance) via BM25 or dense retrievers.
- High batch sizes (thousands of pairs across distributed GPUs) are critical for robust contrastive latent clustering.
**Evaluation Criteria:** Candidate should write or describe the InfoNCE loss function, explain how in-batch negatives scale negative candidate sets, and justify why hard negative mining is essential for preventing trivial shortcut learning.

### Q10: Analyze the phenomena of Grokking and Double Descent in Deep Learning and their implications for LLM pre-training.
**Answer:** Double descent is a learning phenomenon where model test error initially decreases with capacity, spikes near the interpolation threshold (where model parameters equal the number of training data points), and then systematically decreases again in the overparameterized regime as implicit inductive biases guide gradient descent toward minimum-norm solutions. Grokking is a delayed generalization phenomenon where a model reaches near-100% training accuracy through rote memorization, and long after training loss has plateaued near zero, the validation performance suddenly jumps from random chance to near-perfect generalization. This occurs because weight decay and continuous optimization gradually compress the internal representation, discovering structured, low-complexity algorithmic circuits over memorization circuits. In LLM pretraining, these phenomena highlight that overparameterization combined with extended training far past convergence yields superior, generalized cognitive representations.
**Key Points:**
- Double descent: Generalization error spikes at the interpolation boundary before declining in the overparameterized regime.
- Grokking: Generalization occurs thousands of optimization steps after training loss has hit near-zero memorization.
- Driven by implicit regularization and weight decay favoring structured representations over memorized lookup tables.
- Demonstrates that training models beyond the empirical "point of zero training loss" continues to refine internal circuit representations.
**Evaluation Criteria:** Candidate should explain both regimes of the double descent curve, define grokking as delayed generalization past training convergence, and discuss how regularization (weight decay) drives the phase transition.
