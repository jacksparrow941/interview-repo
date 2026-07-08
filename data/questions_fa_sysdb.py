"""Full answers for System Design, Database, OS, Networking, Concurrency questions from questions_other.py."""

def A(*s):
    parts = [f'<span class="answer-label">{l}</span><br>{c}' for l,c in s]
    return '<div class="answer-section">'+'</div><div class="answer-section" style="margin-top:10px">'.join(parts)+'</div>'

FULL_ANSWERS_SYSDB = {

# ===== SYSTEM DESIGN =====

"sd001": A(("Design URL Shortener — Architecture",
    "<pre>Client → Load Balancer → App Server (stateless) → Cache (Redis) → Database\n                                                     ↓ on miss\n                                               Consistent Hash ID Gen</pre>"),
  ("Core Components",
    "<ul><li><b>ID Generation:</b> Snowflake ID → Base62 encode → 7-char short code</li>"
    "<li><b>Storage:</b> MySQL/PostgreSQL for persistence; Redis for read cache (TTL = URL TTL)</li>"
    "<li><b>Redirect:</b> 301 (browser caches) vs 302 (always hits server — better for analytics)</li>"
    "<li><b>Scale:</b> 100M URLs/day = ~1160 URLs/sec write, 10× reads → cache hit rate 99%</li></ul>"),
  ("DB Schema",
    "<pre>CREATE TABLE urls (\n    id BIGINT PRIMARY KEY,           -- Snowflake ID\n    short_code VARCHAR(8) UNIQUE,\n    long_url TEXT NOT NULL,\n    user_id BIGINT,\n    created_at TIMESTAMP,\n    expires_at TIMESTAMP,\n    click_count BIGINT DEFAULT 0\n);</pre>"),
  ("Follow-ups",'<div class="followup">• How do you prevent abuse (phishing URLs)? (URL reputation API, blacklist)<br>'
    '• How do you implement analytics? (Kafka + ClickHouse for click stream)<br>'
    '• How would you support custom vanity URLs?</div>')),

"sd002": A(("Design a Scalable Key-Value Store",
    "Like DynamoDB/Redis Cluster. Key decisions: partitioning, replication, consistency."),
  ("Architecture",
    "<ul><li><b>Consistent hashing ring</b> with virtual nodes for partitioning</li>"
    "<li><b>Replication:</b> N=3. Coordinator writes to 3 nodes.</li>"
    "<li><b>Quorum:</b> W=2, R=2. W+R&gt;N → strong consistency. W=1,R=1 → eventual.</li>"
    "<li><b>Storage engine:</b> LSM-tree (RocksDB) for write optimization</li>"
    "<li><b>Gossip protocol</b> for cluster membership/failure detection</li></ul>"),
  ("Data Flow",
    "<pre>PUT key=A value=X:\n  1. Client → any node (coordinator)\n  2. Hash(A) → ring position → 3 responsible nodes\n  3. Coordinator writes to all 3, waits for W=2 acks\n  4. Returns success\n\nGET key=A:\n  1. Coordinator queries R=2 nodes\n  2. Returns latest version (by timestamp or vector clock)\n  3. Read repair: update stale replica asynchronously</pre>"),
  ("Follow-ups",'<div class="followup">• How does hinted handoff handle temporarily unavailable nodes?<br>'
    '• What is sloppy quorum vs strict quorum?<br>'
    '• How do you handle hot keys? (request sharding, local cache)</div>')),

"sd003": A(("Design a Search Autocomplete System",
    "Target: &lt;100ms response for top-10 suggestions as user types."),
  ("Trie + Top-K",
    "<pre>TrieNode:\n    children: Map&lt;char, TrieNode&gt;\n    topK: List&lt;String&gt;  // cached top-10 completions at each node\n\nSearch(prefix):\n    traverse to prefix node → return node.topK (O(p) where p=prefix length)\n\nUpdate:\n    insert/increment frequency → update topK at each ancestor node</pre>"),
  ("At Scale",
    "<ul><li><b>Data collection:</b> Log all searches → Kafka → aggregation job → frequency table</li>"
    "<li><b>Trie storage:</b> Serialize trie → Redis (sorted sets per prefix: ZADD prefix:ca 100 'cat' 95 'cafe')</li>"
    "<li><b>Updates:</b> Weekly trie rebuild from aggregated frequencies; hot data cache TTL=1h</li>"
    "<li><b>Read:</b> API → Redis ZREVRANGE prefix:ca 0 9 → top 10 suggestions</li></ul>"),
  ("Follow-ups",'<div class="followup">• How do you handle personalized suggestions? (user history weighted blend)<br>'
    '• How do you handle multiple languages and Unicode?<br>'
    '• How do you prevent malicious/offensive suggestions?</div>')),

"sd004": A(("Design a Notification System",
    "Send Email/SMS/Push notifications reliably at scale (millions/day)."),
  ("Architecture",
    "<pre>API Server → Notification Service → Priority Queue (Kafka) → Workers per channel\n                                                                  → Email (SES/SendGrid)\n                                                                  → SMS (Twilio)\n                                                                  → Push (FCM/APNs)\n                                        ↓\n                              User Preferences Service → filter by opt-in\n                              Rate Limiter → throttle per user</pre>"),
  ("Reliability",
    "<ul><li><b>At-least-once:</b> Kafka with manual offset commit after successful send</li>"
    "<li><b>Idempotency:</b> Deduplicate on notification_id to prevent duplicates on retry</li>"
    "<li><b>Dead Letter Queue:</b> Failed after N retries → DLQ → alert, manual review</li>"
    "<li><b>Template Engine:</b> Handlebars/Mustache for personalized content; stored in DB</li></ul>"),
  ("Follow-ups",'<div class="followup">• How do you implement priority queues? (push notifications &gt; email newsletters)<br>'
    '• How do you handle notification preferences and quiet hours?<br>'
    '• How do you track open rates and click-through rates?</div>')),

# ===== DATABASE =====

"db001": A(("Indexes — Types and Internals",
    "<ul><li><b>B+ Tree:</b> Default in PostgreSQL/MySQL. O(log n) for equality and range queries. "
    "Leaf nodes form linked list for range scans.</li>"
    "<li><b>Hash Index:</b> O(1) for equality only. No range queries. Used in memory engines (MEMORY in MySQL).</li>"
    "<li><b>GiST/GIN:</b> PostgreSQL generalized indexes for full-text search, JSONB, arrays.</li>"
    "<li><b>Bitmap Index:</b> Low-cardinality columns. Efficient AND/OR on multiple conditions.</li></ul>"),
  ("Clustered vs Secondary",
    "<ul><li><b>Clustered (InnoDB Primary Key):</b> Data physically stored in index order. "
    "Range scans very fast. Only 1 per table.</li>"
    "<li><b>Secondary:</b> Leaf stores primary key value → extra lookup for full row. "
    "Covering index eliminates this lookup.</li></ul>"),
  ("Index Design Tips",
    "<ul><li>Composite index: equality columns first, range columns last, ORDER BY columns last</li>"
    "<li>Cover frequently queried columns with INCLUDE</li>"
    "<li>Partial index for low-cardinality: <code>WHERE status='PENDING'</code></li>"
    "<li>Avoid index on frequently updated columns (write overhead)</li></ul>"),
  ("Follow-ups",'<div class="followup">• What is an index scan vs bitmap heap scan in PostgreSQL?<br>'
    '• How does an index affect INSERT/UPDATE/DELETE performance?<br>'
    '• When would you use a partial index?</div>')),

"db002": A(("ACID Properties",
    "<ul><li><b>Atomicity:</b> All operations in transaction succeed or all are rolled back. No partial updates.</li>"
    "<li><b>Consistency:</b> Transaction brings DB from one valid state to another. Constraints never violated.</li>"
    "<li><b>Isolation:</b> Concurrent transactions behave as if sequential. Anomalies depend on isolation level.</li>"
    "<li><b>Durability:</b> Committed transactions survive crashes. Guaranteed by WAL.</li></ul>"),
  ("Isolation Levels & Anomalies",
    "<pre>READ UNCOMMITTED: dirty read allowed (see uncommitted data)\nREAD COMMITTED:  no dirty read | phantom read possible\nREPEATABLE READ: no dirty/non-repeatable read | phantom possible (MySQL: solved by gap locks)\nSERIALIZABLE:   full isolation, slowest — SSI (PostgreSQL) or locking (MySQL)</pre>"),
  ("How Implemented",
    "PostgreSQL: MVCC for Repeatable Read and below. Serializable: SSI (Serializable Snapshot Isolation). "
    "MySQL InnoDB: row-level locking + MVCC + gap locks for Repeatable Read."),
  ("Follow-ups",'<div class="followup">• What is a phantom read and how do gap locks prevent it?<br>'
    '• What is lost update anomaly?<br>'
    '• How does SELECT FOR UPDATE work and what lock does it take?</div>')),

"db003": A(("SQL vs NoSQL Trade-offs",
    "<ul><li><b>SQL:</b> ACID, relational, structured schema, powerful joins, vertical scaling + read replicas. "
    "Best for: financial data, complex queries, strong consistency.</li>"
    "<li><b>NoSQL:</b> BASE, flexible schema, horizontal scaling. Different models:<br>"
    "&nbsp;&nbsp;• Document (MongoDB): JSON-like docs, rich queries<br>"
    "&nbsp;&nbsp;• Key-Value (Redis, DynamoDB): O(1) lookup<br>"
    "&nbsp;&nbsp;• Wide-Column (Cassandra, HBase): write-optimized, time-series<br>"
    "&nbsp;&nbsp;• Graph (Neo4j): relationship-heavy queries</li></ul>"),
  ("When to choose",
    "<ul><li>Complex joins + transactions → SQL</li>"
    "<li>Massive write throughput, unstructured data → Cassandra</li>"
    "<li>Fast KV lookup, caching → Redis/DynamoDB</li>"
    "<li>Flexible schema, document queries → MongoDB</li>"
    "<li>Social graph, recommendations → Neo4j</li></ul>"),
  ("Follow-ups",'<div class="followup">• When is PostgreSQL JSONB a good alternative to MongoDB?<br>'
    '• What is NewSQL (CockroachDB, Spanner) and when does it make sense?<br>'
    '• How do you handle schema migrations in NoSQL?</div>')),

# ===== OS =====

"os001": A(("Processes vs Threads",
    "<ul><li><b>Process:</b> Independent address space, separate heap/stack/code/data. "
    "Isolated — one process crash doesn't affect others. IPC needed (pipes, sockets, shared memory).</li>"
    "<li><b>Thread:</b> Shares address space (heap, code, global data) with other threads in same process. "
    "Has own stack + registers. Cheaper to create/switch than process. Direct memory sharing.</li></ul>"),
  ("Context Switch Cost",
    "<ul><li>Process switch: save/restore full CPU state + page table switch (TLB flush) → ~100μs</li>"
    "<li>Thread switch (same process): save/restore registers, stack pointer. No TLB flush → ~1-10μs</li>"
    "<li>Goroutine/fiber switch: userspace, ~100ns</li></ul>"),
  ("Linux Internals","Both processes and threads are <code>task_struct</code> in Linux kernel. "
    "Threads created with <code>CLONE_VM</code> flag — share address space. <code>fork()</code> creates new address space."),
  ("Follow-ups",'<div class="followup">• What is a zombie process?<br>'
    '• What is the difference between fork() and vfork()?<br>'
    '• How do Python GIL and threads interact?</div>')),

"os002": A(("Scheduling Algorithms",
    "<ul><li><b>FCFS:</b> Non-preemptive. Convoy effect (short jobs wait behind long ones).</li>"
    "<li><b>SJF:</b> Shortest job first. Optimal average wait time. Requires knowing burst time.</li>"
    "<li><b>Round Robin:</b> Time quantum (10-100ms). Fair. High throughput for interactive tasks.</li>"
    "<li><b>Priority Scheduling:</b> Highest priority runs first. Risk of starvation (aging fixes this).</li>"
    "<li><b>CFS (Linux):</b> Virtual runtime. Always runs goroutine with minimum vruntime. Weighted fair sharing.</li>"
    "<li><b>MLFQ:</b> Multiple queues with decreasing priority + aging. Adapts to CPU vs I/O bound behavior.</li></ul>"),
  ("Preemptive vs Non-Preemptive",
    "Preemptive: OS can force context switch (timer interrupt). Necessary for interactive systems. "
    "Non-preemptive: process runs until done or blocks. Simpler but poor interactivity."),
  ("Follow-ups",'<div class="followup">• What is starvation and how does aging solve it?<br>'
    '• How does Linux CFS handle I/O-bound vs CPU-bound processes?<br>'
    '• What is the difference between preemptive priority scheduling and non-preemptive?</div>')),

"os003": A(("Page Replacement Algorithms",
    "<ul><li><b>OPT (Optimal):</b> Replace page that won't be used for longest time. Theoretical baseline.</li>"
    "<li><b>FIFO:</b> Evict oldest loaded page. Simple. Belady's anomaly (more frames → more faults).</li>"
    "<li><b>LRU:</b> Evict least recently used. Approximates OPT well. Expensive exact tracking.</li>"
    "<li><b>Clock (LRU approximation):</b> Circular list. Reference bit: on access set to 1, on clock hand pass clear to 0, evict when 0. Linux uses clock-PRO.</li>"
    "<li><b>LFU:</b> Evict least frequently used. Doesn't adapt to recent access pattern changes.</li></ul>"),
  ("Working Set","Set of pages currently needed by process. If working set &gt; available frames → thrashing "
    "(process spends more time swapping than executing). OS monitors WSS, suspends processes if needed."),
  ("Follow-ups",'<div class="followup">• What is Belady\'s anomaly? (FIFO gets more page faults with more frames)<br>'
    '• How does Linux implement page replacement? (kswapd, active/inactive lists)<br>'
    '• What is the difference between paging and segmentation?</div>')),

# ===== NETWORKING =====

"net001": A(("OSI Model",
    "<pre>7. Application  — HTTP, HTTPS, DNS, FTP, SMTP, WebSocket\n6. Presentation — TLS/SSL, compression, encoding\n5. Session      — session management (rarely separate in practice)\n4. Transport    — TCP, UDP, QUIC\n3. Network      — IP, ICMP, routing\n2. Data Link    — Ethernet, Wi-Fi (MAC addresses)\n1. Physical     — cables, signals, bits</pre>"),
  ("TCP/IP Model (practical)",
    "<ul><li>Application (HTTP, DNS, SMTP)</li>"
    "<li>Transport (TCP, UDP)</li>"
    "<li>Internet (IP)</li>"
    "<li>Network Access (Ethernet, Wi-Fi)</li></ul>"),
  ("Key Protocols per Layer",
    "<ul><li>How does a web request flow through OSI? Browser → TCP connect → TLS → HTTP → response</li>"
    "<li>DNS operates at Application layer, uses UDP port 53 (TCP for large responses)</li>"
    "<li>ICMP operates at Network layer (ping, traceroute)</li></ul>"),
  ("Follow-ups",'<div class="followup">• What layer does a load balancer operate at? (L4 or L7)<br>'
    '• What is the difference between TCP and UDP? When to use UDP?<br>'
    '• Why does HTTP/3 use UDP instead of TCP?</div>')),

"net002": A(("HTTP Status Codes",
    "<ul><li><b>2xx Success:</b> 200 OK, 201 Created, 204 No Content, 206 Partial Content</li>"
    "<li><b>3xx Redirect:</b> 301 Moved Permanently (browser caches), 302 Found (temp, no cache), "
    "304 Not Modified (cache validation), 307/308 (preserve method)</li>"
    "<li><b>4xx Client Error:</b> 400 Bad Request, 401 Unauthorized (not authed), "
    "403 Forbidden (authed but no permission), 404 Not Found, 409 Conflict, "
    "422 Unprocessable Entity, 429 Too Many Requests</li>"
    "<li><b>5xx Server Error:</b> 500 Internal Server Error, 502 Bad Gateway, "
    "503 Service Unavailable, 504 Gateway Timeout</li></ul>"),
  ("Cache Headers",
    "<pre>Cache-Control: max-age=3600, public    # cache for 1 hour\nCache-Control: no-cache               # must revalidate before using\nCache-Control: no-store               # don't cache at all\nETag: \"33a64df5\"                       # fingerprint for conditional GET\nIf-None-Match: \"33a64df5\"              # conditional: return 304 if unchanged\nLast-Modified: Wed, 21 Oct 2015 ...    # time-based validation</pre>"),
  ("Follow-ups",'<div class="followup">• What is the difference between 401 and 403?<br>'
    '• When would you return 202 Accepted vs 200 OK?<br>'
    '• What is idempotent status code usage for DELETE? (returns 200 or 204)</div>')),

# ===== CONCURRENCY =====

"con001": A(("Race Condition vs Deadlock vs Livelock",
    "<ul><li><b>Race Condition:</b> Two threads access shared data concurrently without synchronization. "
    "Result depends on execution order. Fix: mutex, atomic ops.</li>"
    "<li><b>Deadlock:</b> Two+ threads each hold a lock the other needs → circular wait. "
    "Fix: lock ordering, timeout, tryLock().</li>"
    "<li><b>Livelock:</b> Threads keep responding to each other without making progress. "
    "Like two people in a corridor each stepping aside for the other. "
    "Fix: random backoff, designated winner.</li>"
    "<li><b>Starvation:</b> Thread never gets CPU or lock because others always get priority. "
    "Fix: fair locks (ReentrantLock(fair=true)), aging.</li></ul>"),
  ("Detection",
    "<ul><li>Race: thread sanitizer (TSAN), Go race detector (<code>-race</code> flag)</li>"
    "<li>Deadlock: jstack/jconsole (Java), wait-for-graph</li></ul>"),
  ("Follow-ups",'<div class="followup">• What are the Coffman conditions for deadlock?<br>'
    '• How does the Go race detector work? (shadow memory tracking)<br>'
    '• What is the dining philosophers problem and its solutions?</div>')),

"con002": A(("Producer-Consumer Pattern",
    "Classic concurrency pattern. Producer generates data, consumer processes it. "
    "Decouple production rate from consumption rate using a bounded buffer."),
  ("Java BlockingQueue",
    "<pre>BlockingQueue&lt;Task&gt; queue = new LinkedBlockingQueue&lt;&gt;(100);  // capacity=100\n\n// Producer:\nnew Thread(() -&gt; {\n    while (true) {\n        Task t = generateTask();\n        queue.put(t);  // blocks if full (backpressure!)\n    }\n}).start();\n\n// Consumer:\nnew Thread(() -&gt; {\n    while (true) {\n        Task t = queue.take();  // blocks if empty\n        process(t);\n    }\n}).start();</pre>"),
  ("Go Channel",
    "<pre>ch := make(chan Task, 100)  // buffered = bounded buffer\n\ngo func() {  // producer\n    for task := range generateTasks() {\n        ch &lt;- task  // blocks if full\n    }\n    close(ch)\n}()\n\nfor task := range ch { process(task) }  // consumer, exits when ch closed</pre>"),
  ("Follow-ups",'<div class="followup">• How do you handle multiple producers and consumers?<br>'
    '• What is the difference between bounded and unbounded queues for backpressure?<br>'
    '• How does the Disruptor pattern improve on BlockingQueue for ultra-low latency?</div>')),

"con003": A(("Thread-Safe Singleton Patterns",
    "<ul><li><b>Eager initialization:</b> Static field initialized at class load time. Thread-safe by JVM spec.</li>"
    "<li><b>Holder pattern (best):</b> Lazy initialization, no synchronization overhead.</li>"
    "<li><b>Double-checked locking with volatile:</b> Works in Java 5+ with volatile.</li></ul>"),
  ("Code Examples",
    "<pre>// 1. Holder (recommended)\nclass Singleton {\n    private Singleton() {}\n    private static class Holder {\n        static final Singleton INSTANCE = new Singleton();  // lazy init, thread-safe\n    }\n    public static Singleton get() { return Holder.INSTANCE; }\n}\n\n// 2. Enum singleton (Josh Bloch's recommendation)\nenum Singleton { INSTANCE; }\n\n// 3. Double-checked locking\nclass Singleton {\n    private volatile static Singleton instance;\n    public static Singleton get() {\n        if (instance == null) {\n            synchronized (Singleton.class) {\n                if (instance == null) instance = new Singleton();\n            }\n        }\n        return instance;\n    }\n}</pre>"),
  ("Follow-ups",'<div class="followup">• Why is enum-based singleton serialization-safe?<br>'
    '• How do you test a singleton? (dependency injection, not true singleton in tests)<br>'
    '• How does Spring @Bean handle singleton scope?</div>')),
}
