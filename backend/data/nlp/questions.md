# Natural Language Processing (NLP) Interview Questions

## Easy

### Q1: What is Natural Language Processing (NLP) and what are its primary core tasks?
**Answer:** Natural Language Processing (NLP) is an interdisciplinary field of computer science, artificial intelligence, and linguistics focused on enabling computers to understand, interpret, manipulate, and generate human language. Traditional and modern NLP systems bridge the gap between unstructured, ambiguous human text and machine-readable numerical representations. Core NLP tasks include text classification (e.g., spam detection and sentiment analysis), information extraction (e.g., named entity recognition and relation extraction), sequence modeling (e.g., part-of-speech tagging and machine translation), and natural language generation (e.g., summarization and dialogue systems). Today, NLP underpins modern search engines, virtual assistants, automated moderation, and enterprise document workflows.
**Key Points:**
- Bridges the semantic gap between ambiguous human language and computational algorithms.
- Core comprehension tasks: Text Classification, Named Entity Recognition (NER), Sentiment Analysis.
- Core sequence tasks: Machine Translation, Part-of-Speech (POS) Tagging, Coreference Resolution.
- Foundational evolution from rule-based/statistical NLP to deep learning and Transformer models.
**Evaluation Criteria:** Candidate should define NLP accurately, enumerate major foundational tasks across classification, extraction, and generation, and mention real-world applications.

### Q2: What is the difference between Stemming and Lemmatization?
**Answer:** Stemming is a crude, rule-based heuristic process that chops off affixes (prefixes and suffixes) from words using algorithmic rules (like the Porter or Snowball stemmer), often resulting in non-words or truncated root forms (e.g., "studying" and "studies" become "studi"). Lemmatization, in contrast, uses vocabulary lookup, morphological analysis, and part-of-speech context to reduce a word to its canonical base or dictionary form, known as the lemma (e.g., "studying" becomes "study", and "better" becomes "good"). While stemming is computationally fast and requires no vocabulary dictionary, lemmatization produces linguistically accurate, valid words at the expense of higher computational complexity.
**Key Points:**
- Stemming: Rule-based suffix stripping (e.g., Porter Stemmer); fast but produces non-dictionary stems (e.g., "troubled" -> "troubl").
- Lemmatization: Morphological and POS-aware reduction to valid dictionary headwords (e.g., "ran" -> "run", "better" -> "good").
- Lemmatization requires lexical databases (e.g., WordNet) and syntactic context.
- Stemming is preferred for fast search indexing; lemmatization is preferred for semantic analysis and language understanding.
**Evaluation Criteria:** Candidate should distinguish between heuristic suffix stripping and dictionary-backed morphological analysis, give concrete examples showing invalid stems vs valid lemmas, and discuss computational trade-offs.

### Q3: What is Stop Word Removal and when should it be avoided?
**Answer:** Stop words are high-frequency words in a language—such as "is", "the", "at", "which", and "on"—that carry minimal discriminative lexical meaning in traditional keyword search and bag-of-words text classification. Removing stop words reduces vocabulary size, eliminates noise, and decreases the memory footprint for classical algorithms like Naive Bayes or TF-IDF. However, stop word removal should be strictly avoided in modern Transformer models (like BERT or GPT), machine translation, question answering, and sentiment analysis where stop words convey critical grammatical, positional, or negation context (e.g., "to be or not to be", or distinguishing "flight to London" from "flight from London").
**Key Points:**
- Filters out frequent functional grammatical words (articles, prepositions, conjunctions) to reduce dimensionality.
- Beneficial for classical sparse models (TF-IDF, BM25) and basic keyword search.
- Harmful for modern Transformer architectures that rely on full sentence context and self-attention.
- Stripping stop words destroys semantic nuance, directional intent, and negation (e.g., "not good").
**Evaluation Criteria:** Look for candidate's awareness of why stop words were traditionally filtered, alongside a clear explanation of why modern Transformer pipelines retain stop words for relational context.

### Q4: What is Part-of-Speech (POS) Tagging and why is it useful?
**Answer:** Part-of-Speech (POS) tagging is the process of labeling each word or token in a text corpus with its corresponding grammatical category—such as noun, verb, adjective, adverb, pronoun, or preposition—based on both its definition and its surrounding syntactic context. For example, in "I will book a flight" vs "I read an interesting book", the word "book" is labeled as a verb in the first sentence and a noun in the second. POS tagging is useful for word sense disambiguation, syntactic parsing, named entity recognition, text-to-speech pronunciation systems, and extracting linguistic features for downstream NLP pipelines.
**Key Points:**
- Assigns grammatical tags (Noun, Verb, Adjective, etc.) using standardized tagsets like Penn Treebank.
- Disambiguates syntactic homonyms based on surrounding sentence context.
- Critical prerequisite for dependency parsing, phrase chunking, and named entity extraction.
- Implemented historically via Hidden Markov Models (HMMs) and CRFs, and today via neural sequence encoders.
**Evaluation Criteria:** Candidate should explain POS tagging with a concrete contextual example (e.g., word functioning as both verb and noun), mention tagsets like Penn Treebank, and describe downstream applications.

### Q5: What is Named Entity Recognition (NER) and what types of entities does it extract?
**Answer:** Named Entity Recognition (NER) is an information extraction subtask that identifies, segments, and classifies mentions of rigid designators or real-world entities within unstructured text into predefined semantic categories. Typical entity categories include Person (PER), Organization (ORG), Location (LOC), Date/Time, Monetary Values, and Geopolitical Entities (GPE). In domain-specific applications, NER extracts specialized entities like genes, proteins, diseases, or legal statutes. NER models typically frame this as a token-level sequence classification problem using BIO (Beginning, Inside, Outside) or BILOU tagging schemes to mark multi-token entity boundaries accurately.
**Key Points:**
- Identifies and categorizes real-world entities (Persons, Organizations, Locations, Dates, Quantities).
- Critical for knowledge graph construction, enterprise search, and automated data entry.
- Uses sequence labeling tagsets like BIO (e.g., B-PER, I-PER, O) to demarcate multi-word entity boundaries.
- Models range from classical CRFs with hand-crafted features to fine-tuned BERT and LLM zero-shot extractors.
**Evaluation Criteria:** Candidate should define NER, list standard entity categories (PER, ORG, LOC), explain the BIO tagging scheme for boundary resolution, and cite modern modeling approaches.

### Q6: What is Sentiment Analysis and how is it typically modeled?
**Answer:** Sentiment analysis is the computational classification of opinions, sentiments, emotions, and subjectivities expressed in text toward specific topics, products, or services. It is typically modeled at different granularities: document-level (overall tone of an entire article), sentence-level, or aspect-level (identifying sentiment toward specific entity features, e.g., "the food was great but service was slow"). Standard formulations frame sentiment analysis as a supervised classification task where text is mapped to discrete classes (Positive, Negative, Neutral) or continuous polarity and subjectivity scores, using algorithms ranging from logistic regression and Naive Bayes over n-grams to fine-tuned Transformer classifiers.
**Key Points:**
- Classifies subjective polarity (Positive, Negative, Neutral) or emotional states from text.
- Granularity levels: Document-level, Sentence-level, and Aspect-Based Sentiment Analysis (ABSA).
- Modeled as a supervised multiclass classification or ordinal regression problem.
- Challenges include detecting sarcasm, irony, domain-dependent jargon, and negations.
**Evaluation Criteria:** Candidate should explain classification granularities (document, sentence, aspect), describe the modeling approach (supervised learning), and mention practical challenges like sarcasm and negation.

### Q7: What is the Bag-of-Words (BoW) model and what are its main limitations?
**Answer:** The Bag-of-Words (BoW) model is a classical text representation technique that converts text into a fixed-length numerical feature vector by counting the occurrence frequency of each word in a document according to a predefined vocabulary dictionary. It completely disregards grammar, word order, syntax, and sentence structure, treating the document as an unordered collection ("bag") of independent tokens. Its primary limitations are severe sparsity (vectors are mostly zeros across large vocabularies), extreme high dimensionality, inability to capture semantic similarity (e.g., "car" and "automobile" have orthogonal representations), and total loss of contextual meaning (e.g., "not bad, very good" and "not good, very bad" produce identical BoW representations).
**Key Points:**
- Represents documents as frequency vectors over a fixed vocabulary dictionary.
- Ignores word order, syntax, and grammatical structures completely.
- High dimensionality and extreme sparsity as vocabulary size grows.
- Vocabulary mismatch: Cannot identify semantic synonyms; sensitive to word choice differences.
- Fails on word order inversions and negations ("not great" vs "great, not").
**Evaluation Criteria:** Candidate should describe the frequency vector representation, identify sparsity and dimensionality issues, and clearly articulate the failure to capture word order and semantic equivalence.

### Q8: What is TF-IDF (Term Frequency - Inverse Document Frequency) and how does it weigh words?
**Answer:** TF-IDF is a statistical weighting metric that evaluates how important a word is to a specific document within a broader collection or corpus. Term Frequency (TF) measures how often a word appears in a target document: TF(t, d) = count(t, d) / total_words(d), reflecting localized topical relevance. Inverse Document Frequency (IDF) measures how rare or common the word is across all documents in the corpus: IDF(t, D) = log(total_documents / (documents_containing_t + 1)), penalizing universal words like "the" or "is" while boosting distinct, domain-specific keywords like "photosynthesis" or "kubernetes". The product TF * IDF yields high weights for words that appear frequently within a document but rarely across the general corpus.
**Key Points:**
- Combines local document relevance (TF) with global corpus rarity (IDF).
- Mathematical formulation: TF-IDF(t, d, D) = TF(t, d) * IDF(t, D).
- IDF logarithmically penalizes common corpus words and elevates distinctive content terms.
- Serves as the mathematical backbone for classical search engines (e.g., BM25) and sparse feature extraction.
**Evaluation Criteria:** Candidate should write or describe both the TF and IDF components, explain the mathematical intuition behind the logarithmic IDF penalty, and state what types of words receive high weights.

### Q9: What is Word2Vec and how does it represent word meanings compared to one-hot encoding?
**Answer:** Word2Vec is a pioneering neural embedding framework introduced by Mikolov et al. in 2013 that learns dense, low-dimensional, continuous vector representations of words based on the distributional hypothesis: words occurring in similar contexts share similar meanings. In contrast to one-hot encoding—which produces high-dimensional, sparse vectors where all words are equidistant and completely orthogonal—Word2Vec embeds words into a compact continuous space (e.g., 300 dimensions) where geometric proximity reflects semantic relatedness. Furthermore, Word2Vec captures linear algebraic relationships between words, enabling famous vector arithmetic such as vector("King") - vector("Man") + vector("Woman") approximately equals vector("Queen").
**Key Points:**
- Founded on the Distributional Hypothesis: "You shall know a word by the company it keeps" (J.R. Firth).
- Dense, low-dimensional vectors (e.g., 100-300D) versus sparse, orthogonal one-hot vectors.
- Captures semantic and syntactic relationships geometrically via cosine distance.
- Exhibits linear compositional properties (e.g., analogical vector arithmetic).
**Evaluation Criteria:** Candidate should contrast sparse one-hot encoding with dense continuous embeddings, reference the distributional hypothesis, and mention geometric vector properties like analogies.

### Q10: What is Text Classification and what are common baseline algorithms used for it?
**Answer:** Text classification is the foundational supervised learning task of assigning predefined categorical labels to raw text documents based on their linguistic content. Applications include spam detection, sentiment categorization, support ticket routing, and news topic classification. Common classical baseline algorithms include Multinomial Naive Bayes (which computes class probabilities using Bayes' Theorem under conditional independence assumptions over word frequencies), Logistic Regression, and Support Vector Machines (SVMs) with linear or RBF kernels trained on TF-IDF feature matrices. These classical baselines are fast, lightweight, and explainable, providing strong initial performance benchmarks before deploying heavy neural networks or transformer models.
**Key Points:**
- Supervised mapping of unstructured text strings to discrete target categories.
- Classical baselines: Multinomial Naive Bayes, Logistic Regression, Linear SVM on TF-IDF features.
- Deep learning / Transformer approaches: BiLSTM with attention, BERT, RoBERTa, DistilBERT.
- Baselines provide critical low-latency, interpretable benchmarks with zero GPU requirements.
**Evaluation Criteria:** Candidate should define text classification, list traditional statistical baselines (Naive Bayes, Logistic Regression, SVM) paired with TF-IDF, and explain why establishing baselines is best practice before using transformers.

---

## Medium

### Q1: Contrast Continuous Bag-of-Words (CBOW) and Skip-gram architectures in Word2Vec.
**Answer:** CBOW and Skip-gram are the two complementary shallow two-layer neural architectures introduced in Word2Vec for learning word representations. CBOW predicts a single target center word given its surrounding context words within a sliding window by averaging the context word vectors; it trains much faster and achieves slightly better accuracy on frequent words due to averaging smoothing effects. Skip-gram does the exact opposite: it takes a single center target word as input and attempts to predict the surrounding context words within the window. Skip-gram requires more training time because it generates multiple training pairs per context window, but it performs significantly better at learning rich representations for rare words and fine-grained semantic nuances.
**Key Points:**
- CBOW: Context words -> Predict target center word (averages context representations).
- Skip-gram: Target center word -> Predict surrounding context words.
- Speed: CBOW is computationally faster and scales efficiently on large datasets.
- Rare Words: Skip-gram excels at capturing infrequent words and subtle semantic distinctions.
- Optimization: Both utilize Negative Sampling or Hierarchical Softmax to avoid computing full vocabulary softmaxes.
**Evaluation Criteria:** Candidate should accurately describe the inverted input-output relationship between CBOW and Skip-gram, explain the impact on training speed, and explain why Skip-gram represents rare words better.

### Q2: What is GloVe (Global Vectors for Word Representation) and how does it differ from Word2Vec?
**Answer:** While Word2Vec learns embeddings locally by scanning text using local sliding windows and stochastic gradient descent (ignoring global corpus co-occurrence statistics), GloVe combines the advantages of local context window methods with global matrix factorization. GloVe constructs a global word-word co-occurrence matrix X across the entire corpus, where X_ij counts how often word j appears in the context of word i. The model optimizes a log-bilinear objective: J = sum_(i,j) f(X_ij) * (w_i^T * w_tilde_j + b_i + b_tilde_j - log(X_ij))^2, where f(X_ij) is a weighting function that caps the influence of extremely frequent co-occurrences. By directly modeling the ratio of co-occurrence probabilities between word pairs, GloVe efficiently encodes global statistical information while preserving linear vector substructures.
**Key Points:**
- Unifies global matrix factorization (LSA) with local context window modeling (Word2Vec).
- Operates on a pre-calculated global word co-occurrence matrix X across the entire corpus.
- Objective fits dot products of word vectors to the logarithm of their co-occurrence probability.
- Weighting function f(X_ij) prevents dominant stop-word pairs from overwhelming optimization.
**Evaluation Criteria:** Candidate should explain that Word2Vec relies on local streaming windows while GloVe factors global co-occurrence matrices, and describe the mathematical intuition of modeling co-occurrence ratios.

### Q3: Explain how BERT achieves bidirectional representation and describe its pre-training objectives (MLM and NSP).
**Answer:** Previous language models like GPT (left-to-right causal) or ELMo (shallow concatenation of independent forward and backward LSTMs) lacked true simultaneous bidirectional context. BERT (Bidirectional Encoder Representations from Transformers) achieves deep bidirectionality by utilizing a Transformer encoder where every token can attend to all other tokens in the sequence simultaneously across all attention layers. To train bidirectionally without allowing tokens to trivially "see themselves" in next-token prediction, BERT introduced Masked Language Modeling (MLM): 15% of input tokens are selected, with 80% replaced by `[MASK]`, 10% replaced by a random token, and 10% kept unchanged, forcing the model to predict the masked identity from context. Additionally, BERT used Next Sentence Prediction (NSP), a binary classification task predicting whether Sentence B logically follows Sentence A, to learn inter-sentence relationships.
**Key Points:**
- True deep bidirectionality: Full self-attention across all tokens in all layers simultaneously.
- Solves bidirectional cheating via Masked Language Modeling (MLM) on 15% of tokens.
- 80/10/10 rule for MLM mitigates representation mismatch between pre-training and fine-tuning.
- Next Sentence Prediction (NSP): Binary classification predicting sentence continuity (later found dispensable by RoBERTa).
**Evaluation Criteria:** Candidate should contrast BERT's deep bidirectionality with unidirectional models, explain the MLM masking strategy and 80/10/10 rationale, and describe the NSP objective.

### Q4: How does Subword Tokenization (BPE, WordPiece) overcome the Out-Of-Vocabulary (OOV) bottleneck?
**Answer:** Classical word-level tokenization assigns an ID to every distinct word, which leads to massive vocabulary tables (millions of words) and inevitably produces `[UNK]` (unknown) tokens for unseen words, misspellings, or rare morphological variants. Subword tokenization solves this by iteratively constructing a vocabulary of variable-length character chunks that balance vocabulary size (typically 30k-50k tokens) and sequence length. Byte-Pair Encoding (BPE) begins with individual characters and iteratively merges the most frequently co-occurring byte or character pairs in the training corpus into new tokens until a target vocabulary size is reached. WordPiece operates similarly but chooses merges that maximize the language model likelihood of the training data. This ensures frequent words remain single tokens while rare words are gracefully broken down into known subword morphemes (e.g., "unhappiness" -> "un", "happiness"), completely eliminating OOV errors.
**Key Points:**
- Overcomes the trade-off between massive word vocabularies and character-level sequence bloat.
- BPE: Bottom-up frequency-based merging of most adjacent co-occurring symbol pairs.
- WordPiece: Likelihood-based merging maximizing scoring criteria on training data.
- Decomposes unseen or compound words into recognized subword morphemes, eliminating `[UNK]` tokens.
**Evaluation Criteria:** Candidate should explain why word-level and character-level tokenization fail, describe the iterative merge mechanics of BPE/WordPiece, and show how rare words are decomposed into subwords.

### Q5: How does Transfer Learning work in modern NLP using models like BERT or RoBERTa for downstream classification?
**Answer:** Transfer learning in modern NLP follows a two-phase "pre-train and fine-tune" paradigm. In the pre-training phase, a foundation model (e.g., BERT) learns generalized linguistic features, syntactic structures, semantic associations, and world knowledge by training on massive unlabeled text corpora using self-supervised objectives (like MLM). In the fine-tuning phase, the pre-trained weights are transferred to a target downstream task (such as document classification). A lightweight task-specific classification head (a linear layer mapping the final `[CLS]` token embedding to the number of classes) is initialized on top of the encoder. The entire network is then trained end-to-end on a small labeled dataset with a low learning rate (e.g., 2e-5 to 5e-5), adapting the generalized features to the specific target domain with minimal labeled data.
**Key Points:**
- Phase 1: Self-supervised pre-training on billions of unlabelled tokens to learn general language priors.
- Phase 2: Supervised fine-tuning on a small labeled target dataset for a specific task.
- Architectural adaptation: Adds a linear classification head over the pooled sequence token (`[CLS]`).
- End-to-end backpropagation updates both the pre-trained weights and the task head with a gentle learning rate.
**Evaluation Criteria:** Candidate should clearly delineate the pre-training vs fine-tuning phases, describe how the architecture is adapted (e.g., classification head on `[CLS]`), and discuss data efficiency benefits.

### Q6: What is Sequence Labeling and how do Conditional Random Fields (CRF) improve NER over independent token classification?
**Answer:** Sequence labeling is the NLP task of assigning a categorical tag to every individual token in an input sequence, such as in POS tagging or Named Entity Recognition. If a model predicts each token's label independently using a simple per-token Softmax layer over transformer outputs, it makes local classification decisions that ignore dependencies between adjacent labels. This leads to invalid label transitions in BIO tagging schemes, such as an `I-PER` (Inside Person) tag immediately following an `O` (Outside) tag without an initial `B-PER`. A Conditional Random Field (CRF) layer placed on top of token representations models the entire sequence globally by learning a transition matrix of transition probabilities between label pairs. At inference time, the Viterbi algorithm decodes the globally optimal sequence of labels that maximizes the joint conditional probability, enforcing valid syntactic transitions.
**Key Points:**
- Sequence labeling assigns sequential tags to sequential inputs (e.g., BIO tagging for NER).
- Independent Softmax ignores dependencies between neighboring predictions, producing illegal tag sequences (e.g., O -> I-PER).
- CRF models joint label sequences globally using learned label transition probability matrices.
- The Viterbi algorithm decodes the globally maximum-likelihood path across all tokens in O(T * K^2) time.
**Evaluation Criteria:** Candidate should explain why independent per-token softmax produces invalid label sequences, describe the CRF transition matrix, and mention Viterbi decoding.

### Q7: How do you handle severe class imbalance in text classification datasets?
**Answer:** Severe class imbalance occurs when majority classes drastically outnumber minority classes (e.g., 99% non-spam vs 1% spam), causing standard loss functions to bias predictions toward the majority class. Mitigation strategies span three levels: data, algorithmic, and evaluation. At the data level, techniques include stratified sampling, random or semantic oversampling of minority classes (using back-translation or synonym substitution), and undersampling dominant classes. At the algorithmic level, practitioners utilize Class-Weighted Cross-Entropy Loss (scaling loss inversely proportional to class frequencies) or Focal Loss, which applies a modulating factor (1 - p_t)^gamma to down-weight the loss from easily classified examples and focus training on hard minority cases. At the evaluation level, accuracy must be discarded in favor of Precision, Recall, Macro-F1, and Precision-Recall AUC.
**Key Points:**
- Data level: Stratified splitting, downsampling majority classes, data augmentation (back-translation, synonym insertion).
- Algorithmic level: Cost-sensitive learning (class-weighted cross-entropy) and Focal Loss.
- Focal loss equation: FL(p_t) = -alpha * (1 - p_t)^gamma * log(p_t); suppresses easy negatives.
- Evaluation level: Rely on Macro-F1, Balanced Accuracy, and PR-AUC; never use standard Accuracy.
**Evaluation Criteria:** Candidate should propose solutions across data sampling, loss function modifications (weighted loss, focal loss), and emphasize proper evaluation metrics like Macro-F1 over Accuracy.

### Q8: Explain the difference between Extractive and Abstractive Summarization.
**Answer:** Extractive summarization generates summaries by scoring, selecting, and concatenating verbatim sentences or passages directly from the original source text without modifying the wording. It relies on sentence ranking algorithms (like TextRank or LexRank) or classification models that predict binary inclusion labels for each sentence; it is computationally fast and factually faithful to the source, but often results in disjointed, redundant, or grammatically awkward summaries. Abstractive summarization, in contrast, mimics human summarization by interpreting the underlying meaning and generating entirely new sentences, paraphrases, and condensed vocabulary that may not appear in the source text. Implemented via sequence-to-sequence models (like BART, T5, or modern LLMs), abstractive systems produce fluent, coherent text but risk generating factual hallucinations.
**Key Points:**
- Extractive: Selects and stitches existing sentences verbatim; high factual consistency, lower fluency.
- Abstractive: Synthesizes novel phrasing and paraphrases using encoder-decoder or autoregressive LLMs.
- Extractive algorithms: TextRank, graph centrality, binary sentence classification.
- Abstractive trade-off: Superior narrative fluency and conciseness, but introduces hallucination risks.
**Evaluation Criteria:** Candidate should clearly define both approaches, contrast verbatim selection with generative paraphrasing, and discuss the trade-off between factual faithfulness and narrative fluency.

### Q9: What are N-grams and how do classical language models compute sequence probabilities using n-gram smoothing?
**Answer:** An N-gram is a contiguous sequence of n tokens extracted from a given text (e.g., unigram for 1 token, bigram for 2, trigram for 3). Classical N-gram language models calculate the probability of a word sequence using the chain rule of probability combined with an (n-1)th order Markov assumption: P(w_1, ..., w_m) = prod P(w_i | w_(i-n+1), ..., w_(i-1)). Probabilities are estimated via maximum likelihood counts: Count(w_(i-1), w_i) / Count(w_(i-1)). However, if an n-gram was never observed in training text, its count is zero, assigning a probability of zero to the entire document. Smoothing techniques solve this: Laplace (Add-1) smoothing adds a pseudo-count, while sophisticated algorithms like Kneser-Ney smoothing interpolate lower-order n-grams with higher-order models and calculate the continuation probability of words based on how versatile they are across diverse contexts.
**Key Points:**
- N-gram: Contiguous sequence of n items; applies Markov assumption to truncate conditional history.
- Maximum Likelihood Estimation (MLE) computes conditional frequencies from text corpora.
- Zero-probability problem: Unseen n-grams zero out the entire sequence probability.
- Smoothing solutions: Laplace (Add-k), Good-Turing, and Modified Kneser-Ney interpolation.
**Evaluation Criteria:** Candidate should write or explain the conditional probability formula under Markov assumptions, explain why zero counts break classical models, and explain smoothing techniques like Kneser-Ney.

### Q10: What metrics are used to evaluate text classification models (Precision, Recall, F1-macro vs F1-micro), and how do they differ?
**Answer:** Text classification models are evaluated using Precision (True Positives / (True Positives + False Positives)), Recall (True Positives / (True Positives + False Negatives)), and the harmonic mean of the two, the F1-Score (2 * P * R / (P + R)). In multi-class classification, aggregating F1 across classes is done via Macro or Micro averaging. Macro-F1 calculates the F1-score independently for each class and computes the unweighted arithmetic mean across classes, treating every class equally regardless of sample size; it is sensitive to poor performance on minority classes. Micro-F1 aggregates global True Positives, False Positives, and False Negatives across all classes before calculating F1, which weights every instance equally and is mathematically identical to Accuracy in single-label multi-class problems. For imbalanced datasets, Macro-F1 is the essential metric for revealing whether minority classes are failing.
**Key Points:**
- Precision measures exactness (minimizing false alarms); Recall measures completeness (minimizing misses).
- F1-Score: Harmonic mean balancing precision and recall.
- Macro-F1: Unweighted average of per-class F1 scores; treats all classes equally; highlights minority class failures.
- Micro-F1: Globally aggregated instances; heavily dominated by majority classes; equals accuracy in single-label tasks.
**Evaluation Criteria:** Candidate should provide mathematical formulas for Precision, Recall, and F1, clearly distinguish between Macro and Micro averaging mechanics, and explain why Macro-F1 is mandatory for imbalanced data.

---

## Hard

### Q1: Detail the internal architecture and pre-training innovations of RoBERTa, ALBERT, and DeBERTa over baseline BERT.
**Answer:** Baseline BERT had several design inefficiencies that subsequent models systematically resolved. RoBERTa demonstrated that BERT was severely undertrained: it eliminated the Next Sentence Prediction (NSP) task (showing it degraded performance), introduced dynamic masking (generating new mask patterns every time a sequence is fed to the model), trained with larger mini-batches (8k sequences), used byte-level BPE, and trained on 10x more data for longer. ALBERT tackled BERT's parameter bloat using two parameter-reduction techniques: factorized embedding parameterization (decoupling token embedding dimension E=128 from hidden dimension H=768 via projection, reducing parameter count from V*H to V*E + E*H) and cross-layer parameter sharing (sharing all weights across transformer layers). DeBERTa introduced Disentangled Attention (representing each word using two separate vectors for content and relative position, computing attention matrices across content-to-content, content-to-position, and position-to-content interactions) and an Enhanced Masked Decoder that injects absolute positions during decoding, dramatically improving syntactic and semantic representations.
**Key Points:**
- RoBERTa: Removed NSP, added dynamic masking, larger batch sizes, longer training on 160GB text.
- ALBERT: Factorized embedding layer (V*E + E*H) and universal cross-layer parameter sharing for parameter efficiency.
- DeBERTa: Disentangled attention mechanism (decouples content and relative position vectors) and Enhanced Masked Decoder.
- DeBERTa sets the empirical benchmark for natural language understanding tasks on SuperGLUE.
**Evaluation Criteria:** Candidate should break down specific architectural or training changes for all three models (RoBERTa, ALBERT, DeBERTa), explain factorized embeddings, and describe disentangled attention.

### Q2: Explain the mathematical objective and training dynamics of Masked Language Modeling (MLM) and how the 80/10/10 masking rule works.
**Answer:** The Masked Language Model objective optimizes the cross-entropy loss over a masked subset of tokens Y_masked: L_MLM(theta) = - sum_(i in Y_masked) log P(x_i | X_corrupted; theta). In BERT, 15% of all input tokens are randomly selected for corruption. However, if selected tokens were always replaced with the special `[MASK]` token, the model would suffer from a significant train-test discrepancy, because `[MASK]` tokens never appear in downstream target tasks during fine-tuning or inference. To mitigate this mismatch, the 80/10/10 rule corrupts the selected 15% tokens as follows: 80% of the time they are replaced with `[MASK]`, 10% of the time they are replaced with a random token from the vocabulary, and 10% of the time they remain unchanged. This forces the model to maintain robust contextual representations for every single token—not just `[MASK]` tokens—because the model never knows whether an observed word is authentic or an unmasked target it must verify.
**Key Points:**
- MLM loss: Cross-entropy over the conditional probability of original tokens given corrupted context.
- Selected subset: 15% of sequence tokens chosen uniformly at random.
- 80/10/10 distribution: 80% `[MASK]`, 10% random word replacement, 10% unchanged original word.
- Resolves distribution shift: Prevents model from overfitting strictly to explicit `[MASK]` tokens.
- Forces transformer layers to continuously preserve contextual representations for all token positions.
**Evaluation Criteria:** Candidate must write out the cross-entropy formulation for MLM, explain the distribution discrepancy problem between pre-training and fine-tuning, and justify the 80/10/10 split.

### Q3: How does the Disentangled Attention mechanism in DeBERTa decouple content and position representations?
**Answer:** In traditional transformers, a token's representation is formed by summing its content embedding and position embedding into a single combined vector: x_i = c_i + p_i. Consequently, standard attention Q * K^T mixes content and position in an entangled dot product. DeBERTa disentangles these signals by representing token i with two distinct vectors: content vector c_i and relative position vector p_(i|j). When computing the attention score between token i and token j, the cross-product decomposes into four components: Attention(i, j) = c_i * c_j^T + c_i * p_(j|i)^T + p_(i|j) * c_j^T + p_(i|j) * p_(j|i)^T. DeBERTa drops the relative position-to-position term p * p^T because relative position offsets between two tokens provide no additional discriminative value without content context. The remaining three terms—Content-to-Content, Content-to-Position, and Position-to-Content—are computed using disentangled projection matrices, allowing the model to determine whether words with specific syntactic roles appear at specific relative distances.
**Key Points:**
- Standard transformers sum content and positional embeddings, entangling them in attention dot products.
- DeBERTa maintains separate content vectors c and relative position vectors p.
- Decomposes pairwise attention into 4 terms; discards position-to-position (p*p^T) as redundant.
- Computes Content-to-Content (c_i * c_j), Content-to-Position (c_i * p_(j|i)), and Position-to-Content (p_(i|j) * c_j).
- Greatly enhances sensitivity to syntactic dependencies and relative token displacement.
**Evaluation Criteria:** Candidate should articulate how standard addition entangles features, write out the 4-term decomposition, explain why position-to-position is dropped, and describe the functional benefit.

### Q4: Design an end-to-end production pipeline for Aspect-Based Sentiment Analysis (ABSA) combining span extraction and polarity classification.
**Answer:** Production ABSA requires extracting specific target entity aspects and predicting granular sentiment polarities toward each aspect. The pipeline consists of four orchestrated components. First, a Preprocessing and Chunking service normalizes text, strips noise, and aligns token boundaries. Second, an Aspect Term Extraction (ATE) model—built as a fine-tuned Transformer with a linear-chain CRF head—tags aspect spans using BIO labeling (e.g., extracting "battery life" and "screen resolution" as `B-ASP`, `I-ASP`). Third, an Aspect Polarity Classification (APC) model takes the source sentence concatenated with each extracted aspect span using special segment tokens: `[CLS] Sentence [SEP] Aspect [SEP]`. This allows multi-head self-attention to focus context representations specifically relative to the target aspect, outputting sentiment logits (Positive, Neutral, Negative). Fourth, a post-processing aggregation service consolidates aspect-sentiment tuples `(Aspect, Sentiment, Confidence)` and routes them to an analytical dashboard or database.
**Key Points:**
- Two-stage architecture: Aspect Term Extraction (ATE) followed by Aspect Polarity Classification (APC).
- ATE: Sequence labeling with Transformer-CRF using BIO tagging to extract multi-word target entities.
- APC: Targeted classification using concatenated context prompts (`[CLS] Text [SEP] Aspect [SEP]`).
- Aspect-conditioned attention allows opposite sentiments for different aspects within the same sentence.
- Post-processing: Deduplication, confidence thresholding, and metric logging.
**Evaluation Criteria:** Candidate should delineate the two distinct subtasks (extraction vs classification), show how input sequences are formatted for aspect-conditioned classification, and mention post-processing steps.

### Q5: Analyze the mathematical formulation of the Viterbi algorithm for decoding sequences in linear-chain CRFs for NER.
**Answer:** In a linear-chain CRF for sequence labeling over tokens X = (x_1, ..., x_T) and label sequence Y = (y_1, ..., y_T), the score of a sequence is defined as Score(X, Y) = sum_(t=1)^T P_(t, y_t) + sum_(t=0)^T A_(y_t, y_(t+1)), where P_(t, j) is the emission score of label j at token t (emitted by the neural encoder) and A_(i, j) is the transition score from label i to label j. To find the optimal sequence Y* that maximizes this score without evaluating all K^T exponential combinations, the Viterbi algorithm uses dynamic programming. Let V_t(j) be the maximum score of a label sequence ending in label j at step t: V_t(j) = max_(i in {1..K}) [ V_(t-1)(i) + A_(i, j) ] + P_(t, j). The algorithm also records backpointers: Backpointer_t(j) = argmax_(i in {1..K}) [ V_(t-1)(i) + A_(i, j) ]. The forward pass computes V_t for all t in [1..T] in O(T * K^2) time, and the backpointers are traced backward from argmax_j V_T(j) to reconstruct the exact globally optimal sequence.
**Key Points:**
- Score unifies emission matrix P (from neural backbone) and transition matrix A (CRF parameters).
- Solves exponential search space O(K^T) via dynamic programming in O(T * K^2) time.
- Recurrence relation: V_t(j) = max_i [ V_(t-1)(i) + A_(i, j) ] + P_(t, j).
- Backpointers store the optimal previous state i for each state j at each time step t.
- Global trace-back guarantees finding the exact sequence maximizing joint probability.
**Evaluation Criteria:** Candidate must write the CRF scoring formula (emissions + transitions), formulate the dynamic programming recurrence, state the O(T * K^2) time complexity, and explain the backpointer traceback.

### Q6: Explain Sentence-BERT (SBERT) and why standard BERT is computationally impractical for large-scale semantic search and clustering.
**Answer:** Finding the most similar pair of sentences in a collection of 10,000 sentences using standard BERT requires feeding all n*(n-1)/2 = ~50 million sentence pairs individually into BERT's cross-encoder architecture `[CLS] Sent1 [SEP] Sent2 [SEP]`, taking approximately 65 hours of GPU compute and making real-time search impossible. Standard BERT's individual sentence representations (derived via `[CLS]` token or mean pooling) exhibit severe anisotropy and yield worse cosine similarity scores than naive GloVe embeddings. Sentence-BERT (SBERT) solves this by using a Siamese network architecture with shared weights to embed sentences independently into dense 768-dimensional vectors. SBERT is trained using 3-way softmax classification on NLI datasets or triplet loss: L = max(0, ||s_a - s_p|| - ||s_a - s_n|| + epsilon). Because sentences are embedded into standalone vectors, embeddings can be precomputed and indexed, reducing semantic search across 10,000 sentences from 65 hours to 5 milliseconds using vector dot products.
**Key Points:**
- Standard BERT cross-encoder requires O(N^2) forward passes for pairwise matching, creating massive latency.
- Standalone BERT `[CLS]` and mean embeddings suffer from severe vector anisotropy (poor raw cosine separation).
- SBERT uses Siamese twin networks with tied weights to produce semantically meaningful sentence embeddings.
- Trained using Triplet Loss or classification objectives over NLI (SNLI / MultiNLI) datasets.
- Enables offline pre-computation and sub-millisecond vector indexing via cosine similarity.
**Evaluation Criteria:** Candidate should calculate or explain the O(N^2) cross-encoder bottleneck, discuss BERT's anisotropy failure mode, and explain SBERT's Siamese training and vector precomputation benefits.

### Q7: How do you address catastrophic forgetting when fine-tuning transformer models on sequential specialized domain tasks?
**Answer:** Catastrophic forgetting occurs when an artificial neural network trained sequentially on new domain data overwrites and erases representations learned during pre-training or earlier tasks. In transformer fine-tuning, several robust methodologies prevent this degradation. First, Parameter-Efficient Fine-Tuning (PEFT) techniques like LoRA or prefix tuning completely freeze the base model weights, ensuring base representations remain 100% intact while domain-specific adapters are learned. Second, Regularization techniques like Elastic Weight Consolidation (EWC) calculate the diagonal Fisher Information Matrix to identify parameters critical to previous tasks, applying quadratic penalties when those parameters deviate: L(theta) = L_new(theta) + sum_i (F_i / 2) * (theta_i - theta_i^*)^2. Third, Experience Replay / Continual Rehearsal interleaves a small percentage of generalized pre-training data or synthetic data into domain fine-tuning batches to preserve general language capabilities.
**Key Points:**
- Catastrophic forgetting: Gradient updates for task B overwrite weight circuits essential for task A.
- PEFT/LoRA: Freezes 100% of base parameters; prevents any modification of underlying weights.
- Elastic Weight Consolidation (EWC): Fisher Information Matrix penalizes updates to parameters critical to prior tasks.
- Experience Replay: Blends a small ratio (e.g., 10-20%) of general instruction data into domain fine-tuning batches.
- Learning rate schedules: Employing Discriminative Fine-Tuning and Slanted Triangular Learning Rates (STLR).
**Evaluation Criteria:** Candidate should define catastrophic forgetting mechanistically, explain parameter freezing via LoRA, formulate or describe EWC regularization, and mention data rehearsal.

### Q8: Detail the mechanics of zero-shot text classification using Natural Language Inference (NLI) with cross-encoders.
**Answer:** Zero-shot text classification via Natural Language Inference (NLI) reframes arbitrary classification tasks into an entailment-checking problem without requiring task-specific labeled training data. An NLI cross-encoder model (such as RoBERTa-large-MNLI) is pre-trained to determine whether a hypothesis logically follows from a premise, classifying pairs into Entailment, Contradiction, or Neutral. To classify a text sample (e.g., "The central bank raised rates by 50 bps"), the text serves as the premise, and candidate classes are structured into hypotheses using a verbalizer template (e.g., "This text is about finance", "This text is about sports"). The text and each candidate hypothesis are passed through the cross-encoder: `[CLS] Premise [SEP] Hypothesis [SEP]`. The model calculates the softmax probability over the Entailment logit across all candidate hypotheses; the label generating the highest entailment probability is selected as the predicted class.
**Key Points:**
- Reframes classification into premise-hypothesis pairs evaluated by a pre-trained NLI model.
- Verbalizer template converts candidate label strings into declarative hypotheses ("This text is about {label}").
- Computes Entailment probability: P(Entailment | Premise, Hypothesis_k).
- Normalizes entailment logits across candidate labels via softmax to generate multi-class probability distributions.
- Enables instant multi-class and multi-label classification for arbitrary novel categories without fine-tuning.
**Evaluation Criteria:** Candidate should explain how NLI (Entailment/Contradiction/Neutral) is repurposed, describe the verbalizer hypothesis template, and trace how entailment logits are normalized for zero-shot inference.

### Q9: What is Coreference Resolution and how do end-to-end neural span-ranking architectures resolve entity mentions across documents?
**Answer:** Coreference resolution is the NLP task of identifying all textual spans and expressions in a document that refer to the exact same real-world entity (e.g., linking "Elon Musk", "the CEO", "he", and "his" in an article). Classical approaches relied on rule-based mention detectors followed by heuristic pairing. Modern end-to-end neural coreference models (such as Lee et al.) eliminate hand-crafted pipelines by considering all possible text spans up to a maximum length L. The model scores every candidate span i using bidirectional contextual embeddings, span width features, and head-word attention: s_m(i) = w_m * [x_start, x_end, x_head, phi(size)]. It then computes a pairwise coreference link score between span i and antecedent candidate j: s(i, j) = s_m(i) + s_m(j) + s_c(i, j), where s_c is a scoring function evaluating span vector concatenation and distance features. Spans are pruned aggressively to top-K candidates, and a softmax distribution over antecedents (including a dummy null antecedent for non-entity spans) is optimized via marginal log-likelihood.
**Key Points:**
- Identifies all linguistic mentions referring to identical real-world entities.
- End-to-end span ranking considers all possible spans up to length L without pipeline mention detection.
- Span representations combine boundary embeddings (start, end), attention-based head token, and span length.
- Pairwise score: s(i, j) evaluates mention validity of both spans plus antecedent relational compatibility.
- Pruning heuristics and softmax over antecedent candidate sets enable tractable O(N) scoring.
**Evaluation Criteria:** Candidate should define coreference resolution with examples, explain end-to-end span representation mechanics, describe pairwise antecedent link scoring, and explain how computational pruning prevents combinatorial explosion.

### Q10: Analyze how Word Sense Disambiguation (WSD) is handled in static embeddings (Word2Vec) vs contextual transformer embeddings (BERT), with mathematical latent geometry analysis.
**Answer:** In static embedding models like Word2Vec or GloVe, each unique vocabulary token w is mapped to a single static vector v_w in R^d, regardless of where or how it is used. For polysemous words (words with multiple meanings, like "bank" as a financial institution vs a river edge), the static vector v_bank becomes a linear superposition of its individual semantic senses weighted by their frequencies: v_bank approx sum_k alpha_k * s_k. This causes severe conflation in latent space, pulling unrelated context words ("river" and "money") into mutual proximity and preventing genuine word sense disambiguation. In contrast, Transformer models like BERT generate contextualized token representations h_i^(L) at layer L as a dynamic function of the entire input sequence X: h_i = Transformer(X)_i. Through multi-head self-attention, query and key projections continuously rotate and displace the token vector based on adjacent contextual clues (e.g., attending to "water" vs "investment"). Mathematically, this maps distinct senses of the same lemma into completely different geometric clusters in high-dimensional activation space, enabling unsupervised sense disambiguation via k-means clustering of hidden state activations.
**Key Points:**
- Static embeddings: Single vector per lemma; polysemy represented as an averaged superposition of meanings.
- Conflation problem: Static vectors cannot separate distinct senses, polluting cosine similarity spaces.
- Transformers: Contextualized hidden states h_i = f(w_i, Context) dynamically shift representation based on attention weights.
- Latent geometry: Different senses of identical words occupy distinct, well-separated geometric manifolds across layers.
- Disambiguation capability enables automated polysemy resolution and contextual clustering.
**Evaluation Criteria:** Candidate should contrast the single-vector static assumption with dynamic contextualization, explain the linear superposition problem in static embeddings, and explain how self-attention separates word senses into geometric manifolds.
