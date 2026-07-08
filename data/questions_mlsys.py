"""ML Systems / MLOps interview questions with full answers."""

_ML = ["Google","Meta","Amazon","Microsoft","Netflix","Uber","LinkedIn","Databricks","Razorpay","CRED","Dream11","Groww","Coinbase"]
_G3 = ["Google","Meta","Amazon","Microsoft","LinkedIn","Uber"]

def A(*s):
    parts = [f'<span class="answer-label">{l}</span><br>{c}' for l,c in s]
    return '<div class="answer-section">'+'</div><div class="answer-section" style="margin-top:10px">'.join(parts)+'</div>'

_RAW = [
("ml001","Design a ML feature store — what is it and why?","ml_systems","ml_systems","Hard",
 _G3+["Netflix","Databricks","Razorpay"], 82, "feature-store,ml,feast,training,serving","System Design Round",
 A(("What is a Feature Store?",
    "Centralized repository for ML features. Solves two problems:<br>"
    "<ul><li><b>Training-serving skew:</b> Feature computed differently at training vs inference → model underperforms in production</li>"
    "<li><b>Feature reuse:</b> Team A computes user_30d_spend, Team B recomputes it separately → wasted effort</li></ul>"),
  ("Architecture",
    "<pre>Data Sources (events, DB, streams)\n    ↓\nFeature Engineering (Spark/Flink job)\n    ↓ write\n┌────────────────────────────────────┐\n│ Feature Store (Feast / Tecton)     │\n│  Offline Store: S3/BigQuery/Hive   │ ← batch training data\n│  Online Store:  Redis/DynamoDB     │ ← low-latency serving\n└────────────────────────────────────┘\n    ↑ read at training time          ↑ read at inference time (&lt;10ms)\n    Training Job                     Inference Service</pre>"),
  ("Key Concepts",
    "<ul><li><b>Point-in-time correct joins:</b> Feature store returns the feature value as it was at prediction time (prevents data leakage)</li>"
    "<li><b>Feature versioning:</b> Rollback features if model performance degrades</li>"
    "<li><b>Feature monitoring:</b> Drift detection — alert if feature distribution changes significantly</li></ul>"),
  ("Follow-ups",'<div class="followup">• How do you handle feature freshness requirements? (real-time vs hourly vs daily features)<br>'
    '• What is training-serving skew and how does a feature store prevent it?<br>'
    '• How does Uber Michelangelo implement feature serving?</div>'))),

("ml002","Design a recommendation system (Netflix/YouTube)","ml_systems","ml_systems","Hard",
 _G3+["Netflix","Amazon","Dream11","Razorpay"], 88, "recommendation,collaborative-filtering,embedding,two-tower","System Design Round",
 A(("Architecture Layers",
    "<pre>Request → Candidate Generation → Scoring → Re-ranking → Response\n           (retrieval)            (ML model)   (business rules)\n           millions→hundreds      hundreds→50  50→10 (diversity, freshness, ads)</pre>"),
  ("Candidate Generation",
    "<ul><li><b>Collaborative Filtering:</b> Users who watched A also watched B. Matrix factorization (SVD). "
    "Doesn't require item features. Cold-start problem for new items.</li>"
    "<li><b>Content-Based:</b> Item embeddings from metadata (genre, actors, tags). Works for new items.</li>"
    "<li><b>Two-Tower Model:</b> Separate user-tower + item-tower → embeddings → ANN search (FAISS). "
    "Pre-compute item embeddings, compute user embedding at request time. YouTube's approach.</li></ul>"),
  ("Scoring & Ranking",
    "<pre>Input: [user_embedding, item_embedding, context_features]\nModel: Deep neural network → predicted CTR / watch_time\nANN Search: FAISS HNSW index → top-K candidates in &lt;10ms for 100M items</pre>"),
  ("A/B Testing",
    "Split traffic by user ID hash. Primary metric: engagement (watch time, CTR). "
    "Guard metrics: don't harm diversity, churn rate. Run for statistical significance."),
  ("Follow-ups",'<div class="followup">• How do you handle the explore-exploit trade-off in recommendations? (contextual bandit, epsilon-greedy)<br>'
    '• How do you prevent filter bubbles in recommendations?<br>'
    '• How does YouTube handle the position bias in training data?</div>'))),

("ml003","How do you detect and handle model drift?","ml_systems","ml_systems","Hard",
 _G3+["Netflix","Databricks","Razorpay","CRED"], 78, "model-drift,data-drift,monitoring,retraining","ML Round",
 A(("Types of Drift",
    "<ul><li><b>Data drift (covariate shift):</b> Input feature distribution changes. User behavior changed, "
    "new user segment, seasonality. Model predictions become unreliable.</li>"
    "<li><b>Concept drift:</b> Relationship between features and label changes. E.g., 'fraud' patterns evolve.</li>"
    "<li><b>Label drift:</b> Output distribution changes. E.g., more fraudulent transactions in new season.</li></ul>"),
  ("Detection Methods",
    "<ul><li><b>Statistical tests:</b> KS-test, PSI (Population Stability Index), Chi-squared for categorical features</li>"
    "<li><b>Model performance metrics:</b> Track AUC, precision, recall on labeled samples in production</li>"
    "<li><b>Shadow deployment:</b> Run new model in shadow, compare predictions vs current model</li>"
    "<li><b>Outlier detection:</b> Flag inputs far from training distribution (z-score, isolation forest)</li></ul>"),
  ("Response Strategy",
    "<ul><li><b>Auto-retrain trigger:</b> PSI &gt; 0.2 → trigger retraining pipeline in MLflow/SageMaker</li>"
    "<li><b>Continuous training:</b> Retrain on rolling window of recent data (online learning for fast-moving data)</li>"
    "<li><b>Canary deployment:</b> New model serves 5% traffic, compare metrics before full rollout</li></ul>"),
  ("Follow-ups",'<div class="followup">• What is PSI (Population Stability Index) and what thresholds indicate drift?<br>'
    '• How do you maintain a training data pipeline that is always fresh?<br>'
    '• What is the difference between online and batch retraining?</div>'))),

("ml004","What is the difference between batch inference and online inference?","ml_systems","ml_systems","Medium",
 _ML[:8], 80, "batch-inference,online-inference,real-time-ml,latency","ML Round",
 A(("Batch Inference",
    "<pre>Trigger: scheduled (hourly/daily)\nInput:   entire dataset (all users)\nOutput:  precomputed predictions stored in DB/cache\nLatency: hours (acceptable)\nUse cases: email recommendations, next-day demand forecast,\n           weekly personalization, offline reporting\n\nStack: Spark/EMR → run model → write to S3 → load to serving DB</pre>"),
  ("Online (Real-time) Inference",
    "<pre>Trigger: user action (click, search, checkout)\nInput:   single request features\nOutput:  prediction within SLA (p99 &lt; 100ms)\nLatency: milliseconds\nUse cases: fraud detection, search ranking, ad bidding, chatbot\n\nStack: REST/gRPC → Feature store (Redis, &lt;5ms) → Model server (TorchServe/TFServing) → Cache</pre>"),
  ("Hybrid Approach",
    "Pre-compute slow features (batch) + compute fast features (online) → merge at serving time. "
    "E.g., Netflix: batch compute user long-term embeddings + online compute session context → real-time ranking."),
  ("Follow-ups",'<div class="followup">• How do you optimize model inference latency? (quantization, ONNX runtime, model pruning)<br>'
    '• What is model serving and how does TorchServe handle batching?<br>'
    '• When would you choose a rule-based system over a ML model?</div>'))),

("ml005","Design an A/B testing platform","ml_systems","ml_systems","Hard",
 _G3+["Netflix","Airbnb","Uber","Razorpay","CRED"], 85, "ab-testing,experimentation,statistics,p-value","System Design Round",
 A(("Core Components",
    "<pre>Experiment Config Service → stores experiment definition\n  (variants, allocation %, targeting rules, metrics)\n\nAssignment Service → deterministic bucketing by user_id\n  hash(user_id + experiment_id) % 100 &lt; allocation%\n  → same user always in same bucket (sticky assignment)\n  → results cached in Redis\n\nEvent Tracking → user actions logged with experiment_id + variant\n  → Kafka → Data Warehouse (Clickhouse/BigQuery)\n\nAnalysis Service → daily/real-time stats computation\n  → t-test / z-test for significance\n  → dashboard with p-value, confidence interval, lift %</pre>"),
  ("Statistical Concepts",
    "<ul><li><b>p-value &lt; 0.05:</b> Less than 5% chance result is due to random variation</li>"
    "<li><b>Statistical power:</b> Probability of detecting a real effect. Usually target 80%.</li>"
    "<li><b>MDE (Minimum Detectable Effect):</b> Smallest effect worth detecting → determines sample size</li>"
    "<li><b>Sample size calculator:</b> n = 16σ²/δ² (for 80% power, 5% significance)</li>"
    "<li><b>Multiple testing problem:</b> 20 experiments at 5% significance → 1 false positive on average. Fix: Bonferroni correction or FDR.</li></ul>"),
  ("Common Pitfalls",
    "<ul><li><b>Novelty effect:</b> New feature gets engagement just because it's new — run longer</li>"
    "<li><b>Network effect:</b> Treating control and treatment users who interact with each other — cluster randomization</li>"
    "<li><b>Peeking:</b> Stopping early when p &lt; 0.05 inflates false positive rate — use sequential testing</li></ul>"),
  ("Follow-ups",'<div class="followup">• What is a holdout group and why is it important?<br>'
    '• How do you handle metric tradeoffs? (CTR increases but conversion decreases)<br>'
    '• What is Bayesian A/B testing and how does it differ from frequentist?</div>'))),

("ml006","How does a fraud detection system work?","ml_systems","ml_systems","Hard",
 ["Stripe","PayPal","Razorpay","PhonePe","CRED","Groww","Coinbase","Amazon","Google","Meta"], 87,
 "fraud-detection,real-time,rules-engine,ml,velocity","System Design Round",
 A(("Layered Defense Architecture",
    "<pre>Transaction Request\n    ↓ (sync, &lt;200ms)\n1. Rules Engine (hard rules, fast)\n   - Deny if: card stolen (blocklist), impossible geography, country blocked\n   - Flag if: unusual amount, new device\n    ↓\n2. ML Model (gradient boosting / neural net, &lt;50ms)\n   - Features: velocity (5 txns in 1min), device fingerprint, merchant category,\n               user history embedding, IP reputation, network graph features\n   - Output: fraud probability score 0-1\n    ↓\n3. Decision: score &lt; 0.3 → approve | 0.3-0.7 → 3DS challenge | &gt; 0.7 → decline\n    ↓ (async, post-transaction)\n4. Chargeback feedback → retrain loop</pre>"),
  ("Key Features",
    "<ul><li><b>Velocity features:</b> count(txns) per user/card/device in last 1m/5m/1h/24h using Redis sliding window</li>"
    "<li><b>Device fingerprinting:</b> browser/app fingerprint, cookie, canvas fingerprint</li>"
    "<li><b>Network graph:</b> card linked to account linked to device → graph neural network for collusion</li>"
    "<li><b>Geospatial:</b> impossible travel (transaction in Mumbai then London in 30min)</li></ul>"),
  ("Class Imbalance",
    "Fraud rate: 0.1-1%. Training: oversample fraud (SMOTE), undersample legitimate, or use class weights. "
    "Evaluation metric: precision@threshold, recall, AUC-ROC. NOT accuracy (99% accuracy by saying everything is legitimate)."),
  ("Follow-ups",'<div class="followup">• How do you handle false positives? (customer friction vs loss prevention tradeoff)<br>'
    '• How do you use graph neural networks for fraud ring detection?<br>'
    '• How do you evaluate a fraud model when labels arrive weeks later via chargebacks?</div>'))),

("ml007","Explain transformer architecture and attention mechanism","ml_systems","ml_systems","Hard",
 ["Google","Meta","Microsoft","Amazon","OpenAI","Databricks","Coinbase"], 82,
 "transformer,attention,self-attention,llm,bert,gpt","ML Round",
 A(("Self-Attention Mechanism",
    "<pre>Input: sequence of tokens → embeddings (d_model=768 for BERT-base)\n\nFor each token, compute:\n  Q (query) = embedding × W_Q\n  K (key)   = embedding × W_K\n  V (value) = embedding × W_V\n\nAttention weights = softmax(Q × K^T / sqrt(d_k))\nOutput = Attention_weights × V\n\n# Each token attends to all other tokens — captures long-range dependencies\n# Multi-head: run h parallel attention heads, concat, project</pre>"),
  ("Transformer Architecture",
    "<ul><li><b>Encoder (BERT):</b> Bidirectional. Sees full context. Used for classification, NER, embeddings.</li>"
    "<li><b>Decoder (GPT):</b> Autoregressive. Each token attends only to previous tokens (causal mask). Used for generation.</li>"
    "<li><b>Encoder-Decoder (T5, BART):</b> Seq2seq tasks: translation, summarization, QA.</li></ul>"),
  ("Why Transformers replaced RNNs",
    "<ul><li>RNN: sequential computation → no parallelism. Gradient vanishing for long sequences.</li>"
    "<li>Transformer: parallel over all positions. Self-attention = O(n²d) but parallelizable on GPU.</li>"
    "<li>Position encoding: sinusoidal or learned — since attention is permutation-invariant, positional info must be added explicitly.</li></ul>"),
  ("Follow-ups",'<div class="followup">• What is the computational complexity of self-attention and how does sparse attention solve it?<br>'
    '• What is RLHF (Reinforcement Learning from Human Feedback) and how is it used to train ChatGPT?<br>'
    '• What is the difference between fine-tuning and prompt engineering vs RAG?</div>'))),

("ml008","Design a search ranking system","ml_systems","ml_systems","Hard",
 _G3+["Airbnb","Razorpay","Swiggy","Zomato"], 85, "search-ranking,elasticsearch,learning-to-rank,bm25","System Design Round",
 A(("Search Stack",
    "<pre>User Query\n    ↓\nQuery Understanding: spell check, tokenization, synonym expansion, intent classification\n    ↓\nRetrieval (Elasticsearch / Lucene):\n  BM25 score: TF-IDF with length normalization\n  → top-1000 candidates in &lt;50ms\n    ↓\nLearning-to-Rank (LTR) Model:\n  Features: BM25 score, query-doc semantic similarity,\n            user click history, item popularity, freshness, location\n  Model: LightGBM / BERT cross-encoder\n  → rerank top-1000 to top-10\n    ↓\nBusiness Rules: boost paid listings, filter unavailable items\n    ↓ \nResponse</pre>"),
  ("Elasticsearch Internals",
    "<ul><li><b>Inverted index:</b> term → [doc_id, positions]. Builds at index time.</li>"
    "<li><b>Sharding:</b> index split into shards. Search parallelized across shards.</li>"
    "<li><b>Analyzers:</b> tokenizer + filters (lowercase, stemming, stopwords) at index + query time</li>"
    "<li><b>Boosting:</b> <code>title^3 body^1</code> — title matches worth 3x body matches</li></ul>"),
  ("Learning-to-Rank",
    "<ul><li><b>Pointwise:</b> Independent regression/classification per document</li>"
    "<li><b>Pairwise (RankNet):</b> Prefer doc A over B → binary classification</li>"
    "<li><b>Listwise (LambdaMART):</b> Optimize NDCG directly. Best quality.</li></ul>"),
  ("Follow-ups",'<div class="followup">• How do you handle cold-start for new items with no click data?<br>'
    '• What is NDCG (Normalized Discounted Cumulative Gain) and how do you compute it?<br>'
    '• How does Airbnb use neural network for search ranking? (listing embeddings)</div>'))),
]

def _to_dict(q):
    return {"id":q[0],"text":q[1],"category":q[2],"subcategory":q[3],"difficulty":q[4],
            "companies":q[5],"frequency":q[6],"tags":q[7].split(","),"round_type":q[8],"answer_hint":q[9]}

QUESTIONS = [_to_dict(q) for q in _RAW]
