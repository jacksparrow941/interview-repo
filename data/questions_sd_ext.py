"""System Design Extended — Twitter feed, WhatsApp, Netflix, Uber dispatch, Redis Cluster, Search Engine."""

_ALL = ["Google","Meta","Amazon","Microsoft","Uber","LinkedIn","Stripe","Razorpay","CRED","Swiggy","Dream11","Coinbase"]
_G3 = ["Google","Meta","Amazon","Microsoft","Uber","LinkedIn"]

def A(*s):
    parts = [f'<span class="answer-label">{l}</span><br>{c}' for l,c in s]
    return '<div class="answer-section">'+'</div><div class="answer-section" style="margin-top:10px">'.join(parts)+'</div>'

SD_EXT = [
  ("sdx001","Design Twitter/X timeline — fan-out on write vs fan-out on read","system_design","social","Hard",
   _G3 + ["Razorpay","CRED"], 92, "twitter,timeline,fan-out,news-feed,redis","System Design Round",
   A(("Approaches",
      "<ul><li><b>Fan-out on Write (Push):</b> When user tweets, push tweet ID to all followers' home timeline caches (Redis sorted sets). "
      "Read is fast (O(1) from cache). Write is expensive for users with millions of followers (celebrities).</li>"
      "<li><b>Fan-out on Read (Pull):</b> On timeline load, fetch tweets from all followed users, merge, sort. "
      "Write is O(1). Read is expensive (100 follows = 100 DB queries).</li>"
      "<li><b>Hybrid (Twitter's actual approach):</b> Fan-out on write for users with &lt;10K followers. "
      "Fan-out on read for celebrities (Lady Gaga: 100M followers — can't write to 100M caches per tweet).</li></ul>"),
     ("Storage Architecture",
      "<pre>Tweet Service:\n  - MySQL: tweet metadata (id, user_id, text, created_at)\n  - Blob store (S3): media files\n  - Redis: home timeline cache per user (sorted set by tweet_id)\n\nTimeline Service:\n  - Read from Redis cache\n  - For celebrities: merge from DB query on read\n  - Ranked feed: ML model scores tweets, inserted in order</pre>"),
     ("Key Design Decisions",
      "<ul><li>Tweet ID as Snowflake (time-sortable → no ORDER BY timestamp needed)</li>"
      "<li>Timeline cache: Redis ZSET with tweet_id as score, cap at 800 entries</li>"
      "<li>Notifications: Kafka topics per user for async fan-out workers</li>"
      "<li>Search: Elasticsearch for full-text search, Earlybird for real-time tweet index</li></ul>"),
     ("Cross-questions","<ul><li>How do you handle a celebrity tweet without overloading fan-out workers?</li>"
      "<li>How do you implement the ranking algorithm without recomputing for every read?</li>"
      "<li>How does Twitter handle timeline when you follow 5000 accounts?</li></ul>"),
     ("Follow-ups",'<div class="followup">• How does Instagram feed differ from Twitter feed architecture?<br>'
      '• What is the Thundering Herd problem in feed generation?<br>'
      '• How do you implement "who to follow" recommendations?</div>'))),

  ("sdx002","Design WhatsApp — messaging, delivery receipts, group chat","system_design","messaging","Hard",
   _G3 + ["Razorpay","CRED","PhonePe"], 90, "whatsapp,messaging,websocket,delivery-receipt,group-chat","System Design Round",
   A(("Core Architecture",
      "<pre>Client ←→ WebSocket/XMPP ←→ Chat Server → Message Queue (Kafka)\n                                        ↓\n                              Message Store (Cassandra)\n                              Delivery Service → Notification (FCM/APNs)\n</pre>"),
     ("Message Flow",
      "<pre>1. Sender connects via WebSocket to Chat Server (sticky session)\n2. Sends message → Chat Server stores in Cassandra:\n   (conversation_id, message_id [Snowflake], sender, content, ts, status=SENT)\n3. Delivery: if recipient online (same/different server)\n   → Use presence service / Redis pub-sub for server routing\n   → Forward via WebSocket → recipient sends ACK → status=DELIVERED\n4. Read receipt: recipient opens chat → status=READ\n5. Offline: store message in Cassandra, push via FCM/APNs on reconnect sync</pre>"),
     ("Group Chat (256 members)","<ul><li>Small groups (&lt;256): Fan-out message to all member connections. Store once, deliver to all.</li>"
      "<li>Very large groups: Store one copy, each member fetches on demand (cursor-based pagination)</li>"
      "<li>Last-seen / delivery tracking: Redis set per message_id of delivered user_ids</li></ul>"),
     ("End-to-End Encryption","Signal Protocol: each message encrypted with recipient's public key. "
      "Server stores only encrypted blobs. Key exchange via identity/one-time prekeys."),
     ("Cross-questions","<ul><li>How do you scale to 2 billion users? (horizontal sharding by user_id)</li>"
      "<li>How does WhatsApp handle message ordering? (Snowflake IDs, logical clocks)</li>"
      "<li>How do you implement message deletion for everyone?</li></ul>"),
     ("Follow-ups",'<div class="followup">• How does the Signal protocol handle forward secrecy?<br>'
      '• How does WhatsApp implement efficient status delivery at scale?<br>'
      '• How would you design an unread message count feature?</div>'))),

  ("sdx003","Design Netflix video streaming — upload, encoding, CDN delivery","system_design","streaming","Hard",
   _G3 + ["Razorpay"], 88, "netflix,video-streaming,cdn,encoding,adaptive-bitrate","System Design Round",
   A(("Upload & Processing Pipeline",
      "<pre>Studio → S3 (raw video)\n       → Encoding Service (transcoding workers):\n           - Multiple resolutions: 480p, 720p, 1080p, 4K\n           - Multiple formats: H.264, H.265/HEVC, AV1\n           - Audio tracks, subtitles\n       → Split into 2-10 second chunks (MPEG-DASH or HLS)\n       → CDN origin (S3) → global CDN edge nodes (Open Connect)</pre>"),
     ("Adaptive Bitrate (ABR)","Client player monitors bandwidth continuously. "
      "Switches between quality levels per chunk. If bandwidth drops: serve lower quality chunk seamlessly. "
      "Protocols: HLS (Apple), MPEG-DASH (Netflix/YouTube). Manifest file (.m3u8 / .mpd) lists all variants."),
     ("Netflix Open Connect","Netflix's own CDN. ISP-embedded appliances. "
      "Popular content pre-positioned to edge during off-peak hours. 95%+ of traffic served from edge. "
      "Remaining 5%: pull from Netflix cloud on cache miss."),
     ("Recommendation Engine","Two-phase: (1) Candidate generation (matrix factorization, collaborative filtering), "
      "(2) Ranking (DNN on user features + item features). A/B test artwork/thumbnails per user."),
     ("Cross-questions","<ul><li>How does Netflix handle the long tail of content? (CDN eviction, tiered storage)</li>"
      "<li>How do you measure streaming quality? (rebuffering ratio, start-play time, bitrate)</li>"
      "<li>How does DRM (Widevine, FairPlay) work?</li></ul>"),
     ("Follow-ups",'<div class="followup">• How does YouTube differ from Netflix in delivery? (user-generated, live streaming)<br>'
      '• What is the DASH manifest and how does the player use it?<br>'
      '• How do you implement resume-play across devices?</div>'))),

  ("sdx004","Design Uber dispatch system — matching drivers to riders","system_design","geospatial","Hard",
   ["Uber","Swiggy","Zomato","CRED","Ola"], 92, "uber,dispatch,geospatial,matching,websocket","System Design Round",
   A(("Components",
      "<pre>Rider App → API Gateway → Ride Request Service\n                             ↓\n                    Location Service (driver positions)\n                    Matching Service (find nearest drivers)\n                    ETA Service (maps API)\n                    Surge Pricing Service\n                    Notification Service (WebSocket/FCM)\n</pre>"),
     ("Location Service","Driver apps send GPS every 4-5 seconds. "
      "Store in Redis geospatial index (<code>GEOADD</code>). "
      "Query: <code>GEORADIUS 37.7749 -122.4194 1 km ASC COUNT 5</code> → nearest 5 drivers within 1km. "
      "Google S2 geometry library for complex polygon queries."),
     ("Matching Algorithm","<pre>On ride request:\n1. GEORADIUS → candidate drivers in 500m-2km\n2. Filter: available (not on trip), accepts request type, car type matches\n3. Score each: ETA + acceptance rate + rating\n4. Offer to top driver (timeout 10s) → if rejected, next driver\n5. On accept: create trip in DB, notify rider</pre>"),
     ("Surge Pricing","Supply (available drivers) vs demand (open requests) per H3 hexagon. "
      "If demand/supply &gt; threshold → surge multiplier. Displayed to rider before booking."),
     ("Cross-questions","<ul><li>How do you handle the case where no drivers are nearby?</li>"
      "<li>How does ETA get calculated accurately? (ML model on historical trip data)</li>"
      "<li>How do you prevent double-booking a driver?</li></ul>"),
     ("Follow-ups",'<div class="followup">• How does Uber handle driver location at city scale? (1M drivers = 1M location updates/5s)<br>'
      '• What is H3 hexagonal grid and why does Uber use it?<br>'
      '• How do you design the driver earnings and settlement system?</div>'))),

  ("sdx005","Design a distributed key-value store (like Redis/DynamoDB)","system_design","distributed","Hard",
   _G3 + ["Stripe","Razorpay","Databricks","Coinbase"], 88, "distributed-kv,consistent-hashing,replication,dynamo","System Design Round",
   A(("Architecture",
      "<pre>Client → Load Balancer → Coordinator Node\n                            ↓ (consistent hash ring)\n                        Partition 0 → Replica A, B, C\n                        Partition 1 → Replica D, E, F\n                        ...\n</pre>"),
     ("Data Distribution","Consistent hashing: keys mapped to ring. Each node owns a range. "
      "Virtual nodes (vnodes): each physical node = 100-200 vnodes for even distribution. "
      "Adding/removing node: only adjacent vnodes affected."),
     ("Replication","Each key replicated to N nodes (typically N=3, DynamoDB style). "
      "Coordinator writes to all N. Quorum: W=2 (write), R=2 (read) → W+R&gt;N = strong consistency. "
      "W=1, R=1 → eventual consistency, highest availability."),
     ("Conflict Resolution","Vector clocks track causality. On divergent versions (network partition): "
      "return both to client (DynamoDB shopping cart), or last-write-wins (LWW) for simpler cases."),
     ("Storage Engine","LSM Tree (write-optimized): MemTable → immutable SSTable → compaction. "
      "B+Tree (read-optimized): InnoDB, LMDB. LSM preferred for KV stores: "
      "fast sequential writes, compaction amortizes cost."),
     ("Cross-questions","<ul><li>How do you handle hot keys? (request sharding, local cache)</li>"
      "<li>How does gossip protocol maintain cluster membership?</li>"
      "<li>How does hinted handoff handle temporary node failure?</li></ul>"),
     ("Follow-ups",'<div class="followup">• What is sloppy quorum and hinted handoff in DynamoDB?<br>'
      '• How does Redis Cluster implement hash slots? (16384 slots)<br>'
      '• Compare DynamoDB vs Cassandra vs Redis Cluster architecture.</div>'))),

  ("sdx006","Design a Search Engine (web-scale)","system_design","search","Hard",
   _G3 + ["Razorpay"], 84, "search-engine,inverted-index,crawling,ranking,elasticsearch","System Design Round",
   A(("Components",
      "<pre>1. Crawler: Fetch web pages (BFS from seed URLs)\n2. Parser: Extract text, links, metadata\n3. Indexer: Build inverted index\n4. Ranker: Score results (TF-IDF, PageRank, ML)\n5. Searcher: Query processing, retrieve, rank, return\n6. Cache: Query result cache, bloom filter for crawled URLs</pre>"),
     ("Inverted Index","Maps term → list of (document_id, positions, frequency). "
      "Query 'distributed systems' → intersect posting lists → ranked by TF-IDF × PageRank.<br>"
      "<pre>Index: { 'distributed': [(doc1, [3,7], 2), (doc4, [1], 1)],\n         'systems':     [(doc1, [4,8], 2), (doc2, [5], 1)] }\nQuery 'distributed systems': doc1 (both terms, high freq) ranks highest</pre>"),
     ("Elasticsearch","Distributed search based on Lucene. "
      "Shard data across nodes. Each shard = independent Lucene index. "
      "Replicas for read scaling + fault tolerance. "
      "Inverted index + doc_values (column store for aggregations) + BKD trees (numeric/geo ranges)."),
     ("PageRank","Iterative algorithm: rank(A) = (1-d) + d × Σ(rank(B)/outlinks(B)) for all B→A. "
      "Pages with many quality inbound links rank higher."),
     ("Cross-questions","<ul><li>How do you handle indexing 100B web pages? (MapReduce / Spark, distributed inverted index)</li>"
      "<li>How do you update the index for real-time news? (incremental indexing, Kafka → Elasticsearch)</li>"
      "<li>How do you implement spell correction? (n-gram index, edit distance)</li></ul>"),
     ("Follow-ups",'<div class="followup">• What is BM25 and how does it improve on TF-IDF?<br>'
      '• How does vector search (ANN) work for semantic search? (FAISS, HNSW)<br>'
      '• How does Google handle query expansion and synonyms?</div>'))),

  ("sdx007","Design a payment system — processing, idempotency, reconciliation","system_design","fintech","Hard",
   ["Stripe","Razorpay","PhonePe","PayPal","CRED","Coinbase","Google","Amazon"], 92,
   "payments,idempotency,saga,reconciliation,pci","System Design Round",
   A(("Payment Flow",
      "<pre>Customer → Payment Gateway → Razorpay/Stripe\n                              ↓\n                    Payment Processor → Card Network (Visa/Mastercard)\n                                          ↓\n                                  Issuing Bank (authorize)\n                                          ↓ (approve/decline)\n                    Settlement Service (T+1 or T+2 days)\n                    Ledger Service (double-entry bookkeeping)</pre>"),
     ("Idempotency","Critical: if client retries payment request, must not double-charge.<br>"
      "<pre>Client sends: POST /payments\n              Idempotency-Key: uuid-v4-from-client\n\nServer: INSERT INTO payments (idempotency_key, ...)\n        ON CONFLICT (idempotency_key) DO NOTHING\n        RETURNING *;\n// If key exists → return stored result (no double processing)</pre>"),
     ("Saga Pattern for Distributed Payment",
      "<pre>1. Reserve inventory\n2. Debit customer account\n3. Credit merchant account\n4. Fulfill order\nOn failure at step 3: compensate (refund), release inventory</pre>"),
     ("Ledger / Double-Entry","Every transaction = two entries: debit one account, credit another. "
      "Prevents money creation/destruction. Immutable append-only ledger. "
      "Balance = sum(credits) - sum(debits) from ledger."),
     ("Cross-questions","<ul><li>How do you handle partial captures and refunds?</li>"
      "<li>How does 3D Secure (3DS) work for fraud prevention?</li>"
      "<li>How do you implement end-of-day reconciliation?</li></ul>"),
     ("Follow-ups",'<div class="followup">• What is PCI-DSS and what are its key requirements?<br>'
      '• How does a payment gateway differ from a payment processor?<br>'
      '• What is the two-phase commit problem in distributed payments?</div>'))),

  ("sdx008","Design a CDN from scratch","system_design","infrastructure","Hard",
   _G3 + ["Stripe","Cloudflare"], 82, "cdn,edge,pop,routing,cache-invalidation","System Design Round",
   A(("Global Architecture",
      "<pre>Origin Server (S3 / API)\n    ↑ Cache Miss (Origin Pull)\nEdge PoPs (Points of Presence):\n  - 200+ cities globally\n  - Each: SSD cache (hot), object store (warm), scrubber\n  - Anycast BGP routing → client reaches nearest PoP\n  - PoP cache miss → Regional cache (shield) → origin</pre>"),
     ("Routing","<b>Anycast:</b> Multiple PoPs announce same IP via BGP. Client's ISP routes to nearest by BGP path. "
      "Latency: 20-30ms to nearest edge vs 150-300ms to origin.<br>"
      "<b>GeoDNS fallback:</b> Different IP per region when anycast not available."),
     ("Cache Hierarchy",
      "<pre>Client → L1 Edge (city) → L2 Shield (regional aggregator) → Origin\n         Hot: SSD 1-2TB      Warm: NVMe 50-100TB       Cold: S3\n         Miss rate: 5-15%    Miss rate: 0.1-2%</pre>"),
     ("Cache Invalidation","<ul><li>URL-based purge: <code>CDN.purge('https://example.com/logo.png')</code></li>"
      "<li>Tag-based purge: tag all product page assets with product_id → invalidate on update</li>"
      "<li>Surrogate-Control: <code>s-maxage=3600</code> (CDN TTL separate from browser)</li></ul>"),
     ("Security at Edge","<ul><li>TLS termination at edge (no TLS to origin for static assets)</li>"
      "<li>DDoS mitigation: rate limiting, IP reputation, challenge page</li>"
      "<li>WAF (Web Application Firewall): block OWASP top 10, SQL injection, XSS</li></ul>"),
     ("Cross-questions","<ul><li>How do you handle cache stampede on popular content expiry?</li>"
      "<li>How does Cloudflare Tiered Cache reduce origin load?</li>"
      "<li>How would you implement edge computing (Cloudflare Workers)?</li></ul>"),
     ("Follow-ups",'<div class="followup">• How does a CDN handle HTTPS and certificate management at scale?<br>'
      '• What is BGP anycast and how does it differ from GeoDNS?<br>'
      '• How do you handle dynamic personalized content at the edge?</div>'))),
]

def _to_dict(q):
    return {"id":q[0],"text":q[1],"category":q[2],"subcategory":q[3],"difficulty":q[4],
            "companies":q[5],"frequency":q[6],"tags":q[7].split(","),"round_type":q[8],"answer_hint":q[9]}

QUESTIONS = [_to_dict(q) for q in SD_EXT]
