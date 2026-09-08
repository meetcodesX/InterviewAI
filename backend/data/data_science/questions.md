# Data Science Interview Questions

## Easy

### Q1: What is the difference between the mean and the median, and when should you prefer one over the other?
**Answer:** The mean is the arithmetic average of all data points, calculated by dividing the sum of values by the total count, making it highly sensitive to extreme outliers. The median is the middle value when data is sorted in order, representing the 50th percentile, which makes it robust against skewed distributions. In symmetric distributions without anomalies, the mean provides a mathematically convenient summary that incorporates all data points. However, when working with skewed data such as household income or real estate prices, the median gives a much more representative measure of central tendency.
**Key Points:**
- Mean includes all values and is sensitive to outliers.
- Median is the 50th percentile and is resistant to outliers.
- Mean equals median in perfectly symmetrical distributions.
- Use median for skewed distributions (e.g., salaries, house prices).
**Evaluation Criteria:** Look for a clear distinction between calculation methods, understanding of sensitivity to outliers, and concrete real-world examples of when to prefer the median.

### Q2: What is Exploratory Data Analysis (EDA) and why is it a critical step in a data science project?
**Answer:** Exploratory Data Analysis (EDA) is the initial process of analyzing, summarizing, and visualizing datasets to discover patterns, spot anomalies, test hypotheses, and verify assumptions before formal modeling. It helps data scientists understand data distributions, feature correlations, and structural flaws such as missing values or duplicate records. Performing EDA prevents the "garbage-in, garbage-out" pitfall by validating data quality early in the lifecycle. Ultimately, insights gained during EDA guide appropriate feature engineering, data preprocessing, and model selection.
**Key Points:**
- Summarizes main characteristics using statistical and visual techniques.
- Identifies anomalies, outliers, patterns, and missing values.
- Validates underlying domain assumptions and data integrity.
- Informs subsequent feature engineering and model selection.
**Evaluation Criteria:** Assess whether the candidate explains both descriptive and visual components of EDA and articulates why skipping EDA leads to flawed downstream models.

### Q3: How do you identify and handle missing values in a Pandas DataFrame?
**Answer:** In Pandas, missing values are typically represented as `NaN` or `None` and can be identified using functions like `df.isna().sum()` or `df.isnull().sum()`. Handling strategies depend on the nature and proportion of the missing data: rows or columns can be dropped using `df.dropna()` if the missingness is minimal or uninformative. Alternatively, values can be imputed using `df.fillna()` with measures such as mean, median, mode, forward/backward fill, or model-based imputation like KNN. Understanding whether data is Missing Completely at Random (MCAR) or Missing Not at Random (MNAR) is essential before applying any fix.
**Key Points:**
- Detection with `isna()`, `isnull()`, and heatmap visualizations.
- Deletion strategies (`dropna`) when data volume permits and missingness is unbiased.
- Imputation strategies (`fillna`) using statistical summaries (mean, median, mode) or algorithms.
- Consideration of missing data mechanisms (MCAR, MAR, MNAR).
**Evaluation Criteria:** Check if candidate mentions both identification tools and multiple remediation approaches, including the trade-offs of dropping vs. imputing.

### Q4: What are the primary differences between Python lists and NumPy arrays?
**Answer:** Python lists are general-purpose dynamic arrays that store pointers to arbitrary objects, which introduces significant memory overhead and cache misses due to non-contiguous memory storage. NumPy arrays (`ndarray`) are homogeneous, fixed-size data buffers stored in contiguous blocks of memory, allowing for highly efficient CPU cache utilization and SIMD vectorization. Mathematical operations on Python lists require explicit loops or list comprehensions, whereas NumPy supports element-wise vectorization executed in compiled C code. Consequently, NumPy arrays are substantially faster and use far less memory for numerical computations.
**Key Points:**
- Homogeneity: NumPy arrays require single data types; Python lists accept mixed types.
- Memory layout: NumPy arrays use contiguous memory blocks; Python lists store pointers.
- Performance: NumPy leverages vectorized C-level operations and SIMD instructions.
- Usability: NumPy provides multidimensional indexing, slicing, and broadcasting.
**Evaluation Criteria:** Look for technical explanations regarding memory layout, contiguous memory vs. pointer dereferencing, and vectorized performance differences.

### Q5: What is the difference between a histogram, a box plot, and a scatter plot, and when would you use each?
**Answer:** A histogram visualizes the probability distribution of a single continuous variable by binning data and displaying frequency counts as bar heights. A box plot summarizes a continuous variable across quartiles, clearly highlighting the median, interquartile range (IQR), and potential outliers via whiskers. A scatter plot displays pairs of continuous variables across Cartesian coordinates to uncover relationships, correlations, and clusters between two features. Choosing among them depends on whether you are analyzing univariate distributions, summary dispersion, or bivariate associations.
**Key Points:**
- Histogram: Univariate distribution, modality, and shape (skewness, peaks).
- Box plot: Five-number summary (Min, Q1, Median, Q3, Max) and outlier identification.
- Scatter plot: Bivariate relationships, correlation trends, and cluster identification.
- Appropriate selection based on analytical objective.
**Evaluation Criteria:** Candidate should clearly state the dimensionality (univariate vs. bivariate) and specific analytical goals best served by each chart type.

### Q6: What is the difference between independent events and mutually exclusive events in probability?
**Answer:** Two events are mutually exclusive if they cannot occur at the same time; the occurrence of one prevents the occurrence of the other, meaning their intersection probability $P(A \cap B) = 0$. In contrast, two events are independent if the occurrence of one does not affect the probability of the other occurring, satisfying the condition $P(A \cap B) = P(A) \times P(B)$. For example, rolling a 2 and rolling a 5 on a single die roll are mutually exclusive. Rolling a 2 on a first die and a 5 on a second die are independent events.
**Key Points:**
- Mutually exclusive: Cannot co-occur; $P(A \cap B) = 0$.
- Independent: One event provides no information about the other; $P(A|B) = P(A)$ and $P(A \cap B) = P(A)P(B)$.
- Mutually exclusive events with non-zero probability are inherently dependent.
- Clear illustrative examples (e.g., coin tosses, dice rolls).
**Evaluation Criteria:** Candidate should provide both mathematical definitions and clear real-world examples showing they do not conflate independence with mutual exclusivity.

### Q7: Explain the concept of "correlation does not imply causation" with a concrete example.
**Answer:** Correlation measures the statistical association or co-movement between two variables, but it does not establish that changes in one variable directly cause changes in the other. A high correlation often arises due to a lurking or confounding variable that influences both observed factors simultaneously. For example, ice cream sales and drowning incidents correlate strongly during summer months, but ice cream consumption does not cause drowning; hot weather is the confounding variable driving both. Establishing true causation requires controlled experiments, A/B tests, or robust causal inference techniques.
**Key Points:**
- Correlation indicates association, not directional mechanism.
- Confounding/lurking variables frequently create spurious correlations.
- Directionality problem: unable to discern if A causes B or B causes A from correlation alone.
- Causation requires randomized controlled trials or causal graphs (DAGs).
**Evaluation Criteria:** Evaluate whether the candidate articulates confounding variables, reverse causation, and the experimental requirements to establish true causality.

### Q8: What are common data cleaning tasks performed before modeling?
**Answer:** Common data cleaning tasks include handling missing values through removal or imputation, deduplicating records, and detecting and treating anomalous outliers. It also involves correcting inconsistent data types, standardizing categorical text representations (e.g., stripping whitespace, uniform casing), and parsing datetime objects. Furthermore, cleaning includes filtering out invalid domain values, reconciling data across disparate sources, and checking for data leakage. Preparing clean data ensures that models learn legitimate signal rather than noise or systemic recording errors.
**Key Points:**
- Missing value imputation or removal.
- Deduplication and string standardization.
- Outlier detection and resolution.
- Data type casting and datetime normalization.
- Domain integrity checks and data validation.
**Evaluation Criteria:** Look for a structured sequence of preprocessing steps and an appreciation for domain-specific integrity checks beyond just standard null-checking.

### Q9: What is NumPy broadcasting and how does it work?
**Answer:** NumPy broadcasting describes how NumPy treats arrays with different shapes during arithmetic operations without making unnecessary copies of data in memory. To be compatible for broadcasting, the trailing dimensions of the two arrays must either be equal or one of them must be 1. NumPy automatically stretches or replicates the dimension of size 1 across the larger array's corresponding dimension during calculation. This mechanism enables expressive, highly optimized vector operations while keeping memory consumption minimal.
**Key Points:**
- Allows arithmetic operations between arrays of differing shapes without explicit copying.
- Rule: Starting from trailing dimensions, axes must match or one must be 1.
- Operates at compiled C speed, saving memory and compute cycles.
- Essential foundation for vectorized operations in scientific Python.
**Evaluation Criteria:** The candidate must explain the specific dimension-matching rule (working backwards from trailing dimensions) and highlight memory efficiency.

### Q10: What is vectorization in Pandas and NumPy, and why is it preferred over Python `for` loops?
**Answer:** Vectorization is the execution of operations on entire arrays or Series at once rather than iterating through elements one-by-one using native Python loops. Under the hood, vectorized code delegates computation to pre-compiled, highly optimized C, Fortran, or Cython routines. This approach bypasses Python's dynamic type checking, pointer dereferencing, and interpreter overhead on every iteration, while enabling CPU cache locality and SIMD parallelization. As a result, vectorized operations routinely achieve performance gains of two to three orders of magnitude over standard loops.
**Key Points:**
- Executes operations across entire arrays at the C level.
- Eliminates Python interpreter overhead and dynamic type checking per element.
- Leverages CPU vector instructions (SIMD) and contiguous memory caching.
- Leads to cleaner, more declarative, and drastically faster code.
**Evaluation Criteria:** Candidate should contrast Python interpreter overhead with compiled C execution and mention hardware-level benefits such as SIMD or memory locality.

---

## Medium

### Q1: What is a p-value, what does the significance level ($\alpha$) represent, and how do you interpret them in hypothesis testing?
**Answer:** A p-value is the probability of observing test results at least as extreme as the actual observed data, assuming that the null hypothesis ($H_0$) is strictly true. The significance level ($\alpha$), commonly set at 0.05, represents the predefined threshold for the probability of committing a Type I error (rejecting a true null hypothesis). If the computed p-value is less than or equal to $\alpha$, we reject the null hypothesis in favor of the alternative hypothesis, concluding the effect is statistically significant. A common misconception is that the p-value represents the probability that the null hypothesis is true; it is strictly a conditional probability of data given $H_0$.
**Key Points:**
- P-value definition: $P(\text{Data as extreme or more} \mid H_0 \text{ is true})$.
- Significance level ($\alpha$): Pre-experiment error budget for false positives.
- Decision rule: Reject $H_0$ if $p \le \alpha$; fail to reject otherwise.
- Common pitfall: p-value is not $P(H_0 \mid \text{Data})$ nor the magnitude of effect size.
**Evaluation Criteria:** Must accurately define p-value as conditional on $H_0$ being true and avoid the common fallacy that it measures the probability that the null hypothesis is correct.

### Q2: Differentiate between Type I and Type II errors. How are their probabilities denoted, and how do they trade off?
**Answer:** A Type I error occurs when we incorrectly reject a true null hypothesis, commonly known as a false positive, and its probability is denoted by $\alpha$. A Type II error occurs when we fail to reject a false null hypothesis, known as a false negative, and its probability is denoted by $\beta$. Statistical power is defined as $1 - \beta$, representing the probability of correctly detecting an effect when one genuinely exists. There is an inherent trade-off: lowering $\alpha$ to be more conservative increases $\beta$ unless sample size is increased or variance is reduced.
**Key Points:**
- Type I error ($\alpha$): False positive (e.g., convicting an innocent person).
- Type II error ($\beta$): False negative (e.g., acquitting a guilty person).
- Statistical Power ($1 - \beta$): Probability of correctly rejecting a false null hypothesis.
- Inverse relationship: Reducing one error rate typically increases the other at fixed sample size.
**Evaluation Criteria:** Check for correct Greek notations ($\alpha$ and $\beta$), connection to statistical power ($1 - \beta$), and a clear understanding of the trade-off mechanics.

### Q3: How do you determine the required sample size and duration for an A/B test before launch?
**Answer:** Sample size determination requires specifying four parameters: the baseline conversion rate, the Minimum Detectable Effect (MDE), the significance level ($\alpha$, usually 5%), and the desired statistical power ($1 - \beta$, usually 80%). Power analysis formulas use these values to calculate the minimum number of samples needed per variant to detect the specified lift reliably. Once sample size is established, the test duration is determined by dividing the total required sample size by daily traffic. The experiment should typically run for full business cycles (e.g., 1–2 full weeks) to account for day-of-week seasonality and novelty effects.
**Key Points:**
- Four core inputs: Baseline conversion rate, MDE, significance level ($\alpha$), and power ($1 - \beta$).
- Inverse relationship with MDE: Smaller effects require quadratically larger sample sizes.
- Duration = Required Sample Size / Daily Active Traffic.
- Guarding against seasonality, day-of-week effects, and user novelty bias.
**Evaluation Criteria:** Candidate should enumerate all four mathematical inputs, explain the impact of MDE on sample size, and address practical business considerations like seasonality.

### Q4: Explain the Central Limit Theorem (CLT) and its practical importance in statistical modeling.
**Answer:** The Central Limit Theorem states that the distribution of the sample mean of independent, identically distributed (i.i.d.) random variables approaches a normal distribution as the sample size becomes sufficiently large, regardless of the underlying population's distribution. Typically, a sample size of $n \ge 30$ is considered adequate for moderately skewed populations, though heavily skewed distributions require larger $n$. This theorem is foundational because it permits the use of normal-distribution-based parametric tests (such as z-tests and t-tests) and confidence intervals on sample means without requiring the underlying population to be normally distributed.
**Key Points:**
- Sample means of i.i.d. variables converge to normal distribution as $n \to \infty$.
- Applies regardless of the underlying population distribution shape (provided finite variance).
- Justifies parametric statistical tests, confidence intervals, and hypothesis testing in practice.
- Crucial distinction: applies to sample means, not raw individual data observations.
**Evaluation Criteria:** Ensure candidate specifies that the theorem applies to the sampling distribution of the *mean* (not the data itself) and explains its practical relevance to inferential statistics.

### Q5: What methods can be used to detect and handle outliers in a dataset, and what are their trade-offs?
**Answer:** Outliers can be detected using parametric methods like Z-scores (flagging points with $|Z| > 3$ assuming normality) or non-parametric methods such as the Interquartile Range (IQR rule: below $Q_1 - 1.5 \times \text{IQR}$ or above $Q_3 + 1.5 \times \text{IQR}$). Multivariate techniques include Isolation Forests, Local Outlier Factor (LOF), and Mahalanobis distance. Handling approaches include trimming/dropping if caused by data entry errors, winsorization (capping at percentiles), or applying robust transformations (logarithmic, Box-Cox). Simply deleting outliers is risky because extreme values may carry vital business signals, such as fraudulent transactions.
**Key Points:**
- Parametric detection (Z-score) vs. Non-parametric detection (IQR method).
- Multivariate algorithms: Isolation Forest, Local Outlier Factor.
- Remediation: Removal, Winsorization (capping), transformation, or using robust algorithms.
- Critical evaluation: Distinguishing measurement error from genuine anomalies (e.g., fraud).
**Evaluation Criteria:** Candidate should contrast univariate vs. multivariate detection methods and defend handling decisions based on business context rather than blindly dropping outliers.

### Q6: What is stationarity in a time series, and how do you test for and achieve it?
**Answer:** A time series is strictly stationary if its statistical properties—specifically mean, variance, and autocovariance—do not change over time. Stationarity is a fundamental prerequisite for models like ARIMA because forecasting models assume that the underlying generating process remains invariant across time horizons. It can be formally evaluated using the Augmented Dickey-Fuller (ADF) test, where a p-value $< 0.05$ indicates rejection of the unit-root null hypothesis, signaling stationarity. If non-stationary, it can be transformed using differencing to remove trends, log transformations to stabilize variance, or seasonal decomposition.
**Key Points:**
- Constant mean, constant variance, and time-invariant autocovariance.
- Statistical testing using Augmented Dickey-Fuller (ADF) or KPSS test.
- Transformation methods: First-order differencing, seasonal differencing, log transformation.
- Essential for autoregressive models to ensure reliable parameter estimation.
**Evaluation Criteria:** Assess candidate's definition of stationary properties (mean, variance, covariance), familiarity with the ADF test, and techniques to transform non-stationary series.

### Q7: Explain how `resample()`, `rolling()`, and `shift()` are used in Pandas for time series feature engineering.
**Answer:** In Pandas, `resample()` is used for frequency conversion and resampling of time series data, acting like a time-based groupby where data can be downsampled (e.g., converting hourly logs to daily averages) or upsampled with interpolation. The `rolling()` function calculates moving window statistics, such as a 7-day rolling mean or rolling standard deviation, which smooths short-term fluctuations and captures temporal trends. The `shift()` function shifts index values forward or backward by a specified number of periods, making it indispensable for creating lag features (e.g., previous day's sales) or lead targets while strictly avoiding lookahead bias.
**Key Points:**
- `resample()`: Time-based aggregation or frequency changes (downsampling/upsampling).
- `rolling()`: Moving window calculations (moving averages, rolling volatility).
- `shift()`: Creating lag features ($t-1$) and forward targets without lookahead bias.
- Critical tools for financial, operational, and demand forecasting feature pipelines.
**Evaluation Criteria:** Candidate should clearly explain the distinct functionality of each method and note the importance of preventing lookahead bias when generating lag features.

### Q8: What is Bayes' Theorem, and how do prior, likelihood, and posterior probabilities relate to each other?
**Answer:** Bayes' Theorem provides a mathematical framework for updating our belief about a hypothesis $H$ given new observed evidence $E$, expressed as $P(H|E) = \frac{P(E|H) \cdot P(H)}{P(E)}$. The prior probability $P(H)$ reflects our initial belief before seeing evidence; the likelihood $P(E|H)$ is the probability of observing the evidence given the hypothesis is true. The marginal probability $P(E)$ acts as a normalizing constant ensuring probabilities sum to one, resulting in the posterior probability $P(H|E)$, which represents our revised belief. This iterative updating process forms the bedrock of Bayesian statistics, spam filtering, and Bayesian A/B testing.
**Key Points:**
- Formula: Posterior = (Likelihood $\times$ Prior) / Marginal Evidence.
- Prior represents domain knowledge or historical belief before new observation.
- Likelihood quantifies the compatibility of the evidence with the hypothesis.
- Posterior reflects updated belief incorporating both prior and fresh empirical evidence.
**Evaluation Criteria:** Look for a clear formulation of the equation, precise verbal definitions of each component, and an understanding of Bayesian belief updating.

### Q9: How do you address extreme class imbalance in a classification problem, and which evaluation metrics should you use?
**Answer:** Extreme class imbalance occurs when one class significantly outnumbers another (e.g., 99:1 in fraud detection), making standard accuracy useless because a naive majority-class classifier appears 99% accurate. To handle this, data-level techniques include oversampling the minority class using SMOTE/ADASYN or undersampling the majority class. Algorithm-level techniques involve cost-sensitive learning via class weights or focal loss, which penalize errors on the minority class more heavily. For evaluation, accuracy must be abandoned in favor of Precision, Recall, F1-score, Precision-Recall AUC (PR-AUC), and Cost-Utility matrices.
**Key Points:**
- Inadequacy of accuracy metric on skewed class distributions.
- Resampling methods: SMOTE, random oversampling, Tomek links undersampling.
- Algorithmic approaches: Balanced class weighting, threshold tuning, focal loss.
- Evaluation metrics: PR-AUC, ROC-AUC, F1-score, confusion matrix costs.
**Evaluation Criteria:** Candidate must recognize why accuracy fails, describe both data-level (SMOTE) and algorithmic (class weighting) remedies, and identify PR-AUC over ROC-AUC for high imbalance.

### Q10: What key principles govern effective data visualization, and how do you prevent misleading representations?
**Answer:** Effective data visualization is governed by the principles of maximizing the data-ink ratio, ensuring high accessibility, and choosing chart types that match data dimensionality and audience intent. Misleading representations frequently arise from truncated y-axes on bar charts, inconsistent bin widths, dual axes with mismatched scales, or using 3D visual effects that distort area perception. Designers should leverage perceptual hierarchies by using color, position, and size deliberately to highlight salient patterns while avoiding chart clutter. Crucially, baseline axes should be preserved when comparing absolute magnitudes, and uncertainty intervals (error bars) should accompany point estimates.
**Key Points:**
- Data-ink ratio (Edward Tufte): remove non-essential decorative elements.
- Avoid misleading practices: non-zero y-axis baselines on bar charts, deceptive dual axes, 3D pie charts.
- Match visualization type to data attributes (e.g., continuous trend vs. discrete comparison).
- Include context, labels, sample sizes, and uncertainty intervals.
**Evaluation Criteria:** Look for awareness of visualization theory (e.g., Tufte's data-ink ratio), common deceptive charting pitfalls, and techniques for honest communication of uncertainty.

---

## Hard

### Q1: Compare Multi-Armed Bandits (MAB) with traditional A/B testing. When would you choose one over the other?
**Answer:** Traditional A/B testing divides traffic into fixed, equal splits between control and variant for the duration of the experiment, emphasizing pure statistical exploration to reach a rigorous hypothesis decision before rolling out the winner. Multi-Armed Bandit algorithms (e.g., Thompson Sampling, Upper Confidence Bound) dynamically allocate traffic toward higher-performing variants in real time, actively balancing exploration and exploitation to minimize regret during the experiment. MAB is superior when opportunity cost is high, sample sizes are limited, or variants have short shelf-lives, such as flash sales or headline optimization. However, traditional A/B testing remains preferable when long-term causal conclusions, secondary metrics, or network and novelty effects must be cleanly isolated.
**Key Points:**
- Exploration vs. Exploitation: A/B testing explores 100% until completion; MAB balances dynamically.
- Regret minimization: MAB minimizes traffic sent to suboptimal arms during the test period.
- Statistical rigor: A/B testing provides cleaner inference, unaffected by adaptive allocation biases.
- Use case selection: MAB for short-lived assets/high cost of regret; A/B for product launches with multiple success metrics.
**Evaluation Criteria:** Look for deep understanding of the exploration-exploitation dilemma, concept of regret, and distinct business scenarios favoring each approach.

### Q2: What is the multiple testing problem in hypothesis testing, and how do Bonferroni correction and the Benjamini-Hochberg procedure address it?
**Answer:** When testing $k$ independent hypotheses at a significance level $\alpha = 0.05$, the probability of committing at least one Type I error across all tests is $1 - (1 - \alpha)^k$, which grows rapidly (e.g., $\approx 40\%$ for $k=10$). The Bonferroni correction controls the Family-Wise Error Rate (FWER) by dividing the nominal alpha by the number of tests ($\alpha_{new} = \alpha / k$), but it is notoriously conservative and inflates Type II error rates. The Benjamini-Hochberg (BH) procedure instead controls the False Discovery Rate (FDR)—the expected proportion of false positives among all rejected hypotheses—by sorting p-values and applying an adaptive step-up threshold. BH offers much greater statistical power than Bonferroni, making it the industry standard for high-throughput genomics, large-scale A/B test platforms, and metric suites.
**Key Points:**
- Multiple testing multiplies overall false positive rate: $FWER = 1 - (1-\alpha)^k$.
- Bonferroni controls FWER: $\alpha / k$; overly conservative when $k$ is large.
- Benjamini-Hochberg controls FDR: ranking p-values and using rank-adjusted thresholds ($p_{(i)} \le \frac{i}{m} Q$).
- BH maximizes statistical power while bounding the proportion of false discoveries.
**Evaluation Criteria:** Candidate should explain why testing many metrics leads to spurious findings, write out the FWER formula, and contrast FWER control (Bonferroni) with FDR control (BH).

### Q3: Contrast Bayesian A/B testing with Frequentist A/B testing regarding decision rules, sample size flexibility, and interpretability.
**Answer:** Frequentist A/B testing relies on p-values and fixed sample sizes, where peering at results prematurely without sample-size adjustments inflates Type I errors. Its output determines whether to reject a null hypothesis, but it cannot express the direct probability that variant B is better than variant A. Bayesian A/B testing calculates a posterior distribution over the lift, allowing practitioners to answer direct business questions like "What is the probability that B is better than A?" and compute expected loss. Furthermore, Bayesian testing allows continuous monitoring and stopping decisions without traditional p-hacking penalties, provided appropriate priors are defined. However, Bayesian methods require careful prior selection and involve greater computational overhead.
**Key Points:**
- Direct interpretability: Bayesian gives $P(B > A \mid \text{data})$; Frequentist gives $P(\text{data} \mid H_0)$.
- Peeking flexibility: Bayesian posteriors allow continuous evaluation; Frequentist requires sequential testing corrections.
- Expected Loss metric: Bayesian frameworks quantify the business risk of making a wrong decision.
- Prior sensitivity: Bayesian results depend on chosen priors; Frequentist requires no prior distribution.
**Evaluation Criteria:** Candidate should contrast the philosophies of probability, address the "peeking problem" in Frequentist testing, and explain how expected loss guides business decisions in Bayesian frameworks.

### Q4: Explain the difference between ARIMA, SARIMAX, and modern structural time series decomposition, and how cointegration applies to multivariate series.
**Answer:** ARIMA models univariate stationary series using autoregressive terms ($p$), differencing order ($d$), and moving average terms ($q$), while SARIMAX extends this framework by incorporating multiplicative seasonal orders $(P, D, Q)_s$ and external exogenous regressors ($X$). Structural time series decomposition decomposes a series into interpretable latent components: trend, seasonality, cycle, and irregular noise using state-space models and Kalman filtering. When dealing with multivariate non-stationary series, cointegration describes a phenomenon where two or more individual non-stationary integrated series of order 1 share a stationary linear combination. This indicates a genuine long-run equilibrium relationship, preventing spurious regression and enabling Error Correction Models (ECM).
**Key Points:**
- SARIMAX accounts for autoregression, moving averages, seasonal cycles, and exogenous predictors.
- State-space models decouple latent trend, seasonality, and noise using Kalman filters.
- Cointegration: Non-stationary series whose linear combination is stationary $I(0)$.
- Error Correction Models (ECM) model short-run adjustments toward long-run equilibrium.
**Evaluation Criteria:** Look for understanding of model parameters, handling of seasonality and covariates, and a mathematically sound explanation of cointegration vs. spurious correlation.

### Q5: What is Simpson's Paradox, how can it lead to completely contradictory conclusions in data analysis, and how do you resolve it?
**Answer:** Simpson's Paradox occurs when a statistical trend or association appears in aggregated data but reverses or disappears when the data is disaggregated into underlying subgroups. It is caused by an unobserved or ignored confounding variable that is strongly associated with both the independent variable and the outcome, accompanied by unequal group sample sizes. For instance, treatment A may show higher overall recovery rates than treatment B, but when partitioned by disease severity, treatment B outperforms treatment A in both mild and severe subgroups because severe patients were disproportionately assigned to A. Resolving it requires constructing Causal Directed Acyclic Graphs (DAGs) and applying causal conditioning (e.g., backdoor criterion) or stratified analysis to control for the confounder.
**Key Points:**
- Aggregated relationship reverses when conditioned on a confounding subgroup.
- Driven by confounding variables and disproportionate sample distribution across groups.
- Classic example: UC Berkeley admissions gender bias case or medical trial drug efficacy.
- Remediation: Causal DAGs, stratification, and propensity score matching to control for confounders.
**Evaluation Criteria:** Candidate should provide a clear concrete scenario where the paradox manifests, identify confounding as the root cause, and explain causal graphical models or stratification as remedies.

### Q6: What is Markov Chain Monte Carlo (MCMC) sampling, why is it necessary in Bayesian inference, and what are common diagnostics for convergence?
**Answer:** In Bayesian inference, calculating the posterior distribution often requires computing an intractable high-dimensional integral in the denominator (the marginal evidence $P(D) = \int P(D|\theta)P(\theta)d\theta$). MCMC solves this by generating samples from the target posterior distribution through a constructed Markov chain whose stationary distribution matches the desired posterior, without needing to compute the denominator. Algorithms like Metropolis-Hastings, Gibbs Sampling, and Hamiltonian Monte Carlo (HMC/NUTS) simulate these paths. Convergence must be validated using diagnostic metrics: trace plots for chain mixing, Gelman-Rubin statistic ($\hat{R} \approx 1.00$), and Effective Sample Size (ESS) to ensure samples are adequately uncorrelated.
**Key Points:**
- Solves intractable integration in Bayesian denominator without calculating the normalizing constant.
- Generates dependent samples whose stationary distribution matches the target posterior.
- Key algorithms: Metropolis-Hastings, Gibbs Sampling, Hamiltonian Monte Carlo / NUTS.
- Convergence diagnostics: $\hat{R}$ (potential scale reduction factor), Effective Sample Size, trace plot visual checks.
**Evaluation Criteria:** Candidate must explain why the analytical integral is intractable, how the stationary distribution property operates, and cite standard convergence metrics ($\hat{R}$, ESS).

### Q7: Explain the "curse of dimensionality" in high-dimensional feature spaces and its effect on distance metrics and model variance.
**Answer:** As the number of dimensions increases, the volume of the feature space grows exponentially, causing available data points to become extremely sparse throughout the space. In high dimensions, the contrast between the distance to the nearest neighbor and the farthest neighbor approaches zero ($\lim_{d \to \infty} \frac{\text{dist}_{max} - \text{dist}_{min}}{\text{dist}_{min}} \to 0$), making distance-based algorithms like KNN, K-Means, and SVMs with RBF kernels lose discriminative power. Additionally, high dimensionality drastically inflates model variance and induces severe overfitting because models can easily fit noise in empty space. Remediation requires dimensionality reduction (PCA, t-SNE, UMAP), feature selection, or regularization ($L_1$/Lasso).
**Key Points:**
- Exponential expansion of volume creates extreme data sparsity.
- Distance metric collapse: ratio between nearest and farthest points converges to zero.
- Model susceptibility to overfitting and high variance due to sparse sampling.
- Mitigation: PCA, autoencoders, feature selection, $L_1$ sparsity constraints.
**Evaluation Criteria:** Candidate should explain geometric expansion, the mathematical behavior of Euclidean distance in high dimensions, and specific algorithmic failure modes.

### Q8: What are Covariate Shift and Concept Drift, how do they differ, and how can they be detected and mitigated in production ML pipelines?
**Answer:** Covariate Shift occurs when the marginal distribution of the input features changes over time ($P(X_{train}) \ne P(X_{prod})$), but the conditional relationship between features and labels remains unchanged ($P(Y|X)$ remains constant). Concept Drift occurs when the underlying relationship between inputs and outputs changes ($P(Y|X_{train}) \ne P(Y|X_{prod})$), even if the input distribution $P(X)$ appears identical. Detection methods include Population Stability Index (PSI), Kolmogorov-Smirnov (KS) tests, Wasserstein distance on feature distributions, and adversarial validation (training a classifier to distinguish training from production data). Mitigation involves importance weighting using density ratios, sliding-window retraining, continuous online learning, and triggered model redeployment.
**Key Points:**
- Covariate Shift: $P(X)$ changes while $P(Y|X)$ stays invariant.
- Concept Drift: $P(Y|X)$ changes (e.g., macroeconomic shock altering consumer behavior).
- Statistical detection: KS-test, PSI, adversarial validation, degradation of ground-truth metrics.
- Mitigation: Density ratio importance weighting, scheduled retraining, dynamic streaming updates.
**Evaluation Criteria:** Candidate must clearly contrast $P(X)$ change vs. $P(Y|X)$ change using formal probability notation and describe both statistical detection tests and remediation strategies.

### Q9: How do you optimize memory consumption and execution time when processing datasets in Pandas that exceed available RAM?
**Answer:** When dealing with datasets larger than RAM, optimization begins with type downcasting: converting `float64` to `float32`, `int64` to `int16`/`int8`, and high-cardinality strings to the `category` dtype or integer dictionary encodings. Next, data should be ingested iteratively in manageable batches using the `chunksize` parameter in `pd.read_csv()`, aggregating intermediate results per chunk before accumulating. Furthermore, querying only necessary columns using `usecols` avoids unnecessary memory allocation. For datasets that fundamentally cannot fit into single-machine memory or require parallelized scaling, transitioning to distributed or out-of-core computing frameworks such as Polars (with streaming mode), Dask, DuckDB, or PySpark is the definitive architectural solution.
**Key Points:**
- Type downcasting: `int64` to smaller integer types, `float64` to `float32`, object to `category`.
- Chunked processing: `pd.read_csv(..., chunksize=N)` with incremental aggregation.
- Selective loading: `usecols` parameter to bypass unneeded feature ingestion.
- Scalable frameworks: Out-of-core engines like DuckDB, Polars (lazy streaming), or distributed Dask/Spark.
**Evaluation Criteria:** Candidate should demonstrate hands-on knowledge of Pandas internals (dtypes, memory usage) and architectural knowledge of out-of-core/distributed tools (DuckDB, Polars, Dask).

### Q10: How do you design an A/B test when there is significant network interference or spillover between control and treatment groups?
**Answer:** Network interference violates the Stable Unit Treatment Value Assumption (SUTVA), which states that one unit's treatment status must not affect another unit's potential outcomes, commonly observed in social networks, ride-sharing marketplaces, or delivery platforms. If a treatment driver or user creates competitive spillover or viral adoption, traditional user-level randomization produces severely biased effect estimates. To solve this, practitioners implement cluster-based randomization (e.g., graph community detection algorithms like Louvain to assign entire social clusters to control or treatment) or spatial/geographic clustering (assigning entire metropolitan areas). Alternatively, two-sided marketplace platforms use switchback experiments (time-based alternation between control and treatment over discrete time blocks) or synthetic control methods to isolate true causal uplift.
**Key Points:**
- Violation of SUTVA: Interference, competition for supply/demand, or social viral spread.
- Cluster Randomization: Partitioning network graphs using community detection algorithms.
- Switchback Experiments: Alternating treatments over time windows across distinct geographic regions.
- Synthetic Controls and Difference-in-Differences to model counterfactual equilibrium.
**Evaluation Criteria:** Candidate must identify SUTVA violation as the core theoretical issue and present concrete alternative designs like cluster-based randomization or switchback testing with their trade-offs.
