"""
MUFG Global Services — ByteByteGo-style deep-dive questions
Covers thin sections: system_design, concurrency, coding, database, security, spring
Sources: ByteByteGo, Martin Fowler, Java Concurrency in Practice, AWS docs
"""

_MUFG = ["MUFG Global Services"]

def A(*sections):
    parts = [f'<span class="answer-label">{l}</span><br>{c}' for l,c in sections]
    return '<div class="answer-section">'+'</div><div class="answer-section" style="margin-top:10px">'.join(parts)+'</div>'

MUFG3_Q = [

  ("mufg032","API Gateway pattern — rate limiting, routing, JWT auth, circuit breaker for MUFG microservices",
   "system_design","api_gateway","Hard",_MUFG,92,
   "api-gateway,rate-limit,jwt,circuit-breaker,microservices,banking","System Design Round",
   A(("Architecture Diagram (ByteByteGo style)",
      "<pre>"
      "  ReactJS / Mobile\n"
      "        |\n"
      "  +-----v-----------------------+\n"
      "  |      API GATEWAY            |\n"
      "  |  1. JWT Validation          |\n"
      "  |  2. Rate Limiter (Redis)    |\n"
      "  |  3. Circuit Breaker (R4j)   |\n"
      "  |  4. Request Routing         |\n"
      "  |  5. Load Balancer           |\n"
      "  +---+-------+--------+--------+\n"
      "      |       |        |\n"
      "   Trade   Account   Payment\n"
      "   Svc      Svc       Svc\n"
      "  (8081)   (8082)    (8083)\n"
      "      |       |        |\n"
      "    DB(P)   DB(A)    DB(P)\n"
      "</pre>"),
     ("Spring Cloud Gateway Config",
      "<pre>// application.yml\nspring:\n  cloud:\n    gateway:\n      routes:\n        - id: trade-service\n          uri: lb://TRADE-SERVICE\n          predicates:\n            - Path=/api/v1/trades/**\n          filters:\n            - name: RequestRateLimiter\n              args:\n                redis-rate-limiter.replenishRate: 100\n                redis-rate-limiter.burstCapacity: 200\n                key-resolver: '#{@userKeyResolver}'\n            - name: CircuitBreaker\n              args:\n                name: tradeCircuitBreaker\n                fallbackUri: forward:/fallback/trades\n\n@Component\npublic class JwtAuthFilter extends AbstractGatewayFilterFactory&lt;JwtAuthFilter.Config&gt; {\n    @Override\n    public GatewayFilter apply(Config config) {\n        return (exchange, chain) -&gt; {\n            String token = extractToken(exchange.getRequest());\n            if (!jwtService.isValid(token))\n                return unauthorized(exchange);\n            return chain.filter(exchange);\n        };\n    }\n}</pre>"),
     ("Rate Limiting — Token Bucket (Redis)",
      "<pre>// Token bucket: replenish 100 tokens/sec, burst up to 200\n@Bean\npublic KeyResolver userKeyResolver() {\n    return exchange -&gt; Mono.just(\n        exchange.getRequest().getHeaders().getFirst(\"X-User-Id\")\n    );\n}\n// HTTP 429 Too Many Requests when limit exceeded</pre>"),
     ("Cross-Questions",
      '<div class="followup">'
      '&bull; API Gateway vs Load Balancer — key difference?<br>'
      '&bull; How do you implement idempotency at gateway level? (Idempotency-Key header + Redis dedup)<br>'
      '&bull; What is the Strangler Fig pattern and how does gateway enable it?<br>'
      '&bull; How does service mesh (Istio) differ from API Gateway?<br>'
      '&bull; How do you handle gateway as SPOF? (Multi-region, active-active)'
      '</div>'))),

  ("mufg033","Outbox Pattern — reliable event publishing in MUFG distributed transactions",
   "system_design","distributed_systems","Hard",_MUFG,88,
   "outbox-pattern,distributed-transactions,kafka,at-least-once,consistency","System Design Round",
   A(("The Problem",
      "<b>Double-write problem:</b> Save trade to DB + publish Kafka event — what if DB commits but Kafka fails? "
      "Events lost. What if Kafka publishes but DB fails? Phantom events. "
      "<b>Solution: Transactional Outbox Pattern</b>"),
     ("Architecture Diagram",
      "<pre>"
      "  Trade Service\n"
      "  +----------------------------------+\n"
      "  | BEGIN TRANSACTION                |\n"
      "  |   INSERT trades SET status=BOOKED|\n"
      "  |   INSERT outbox (event JSON)     |\n"
      "  | COMMIT  &lt;-- atomic!             |\n"
      "  +----------------------------------+\n"
      "          |\n"
      "  +-------v-----------+\n"
      "  |  Message Relay     |  (Debezium CDC)\n"
      "  |  polls outbox table|\n"
      "  +-------+-----------+\n"
      "          |\n"
      "  +-------v-----------+\n"
      "  |   Kafka Topic      |\n"
      "  |  trade.booked      |\n"
      "  +--------------------+\n"
      "</pre>"),
     ("Implementation",
      "<pre>// 1. Outbox table\nCREATE TABLE outbox (\n    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),\n    event_type VARCHAR(100) NOT NULL,\n    payload    JSONB NOT NULL,\n    published  BOOLEAN DEFAULT false\n);\n\n// 2. Service writes both atomically\n@Transactional\npublic void bookTrade(TradeRequest req) {\n    Trade t = tradeRepo.save(mapToTrade(req));\n    outboxRepo.save(OutboxEvent.builder()\n        .eventType(\"TRADE_BOOKED\")\n        .payload(objectMapper.writeValueAsString(t))\n        .build());\n}\n\n// 3. Scheduled relay\n@Scheduled(fixedDelay = 500)\npublic void publishPendingEvents() {\n    List&lt;OutboxEvent&gt; events = outboxRepo.findByPublishedFalse();\n    events.forEach(e -&gt; kafkaTemplate.send(e.getEventType(), e.getPayload()));\n    events.forEach(e -&gt; e.setPublished(true));\n    outboxRepo.saveAll(events);\n}</pre>"),
     ("Cross-Questions",
      '<div class="followup">'
      '&bull; Outbox vs Saga pattern — when to use which?<br>'
      '&bull; How does Debezium CDC work? (WAL log tailing in PostgreSQL)<br>'
      '&bull; How do consumers handle duplicate events? (Idempotent consumers + processed_events table)<br>'
      '&bull; What is at-least-once vs exactly-once in Kafka?<br>'
      '&bull; How to handle outbox table growth? (Archive after published + TTL cleanup)'
      '</div>'))),

  ("mufg034","CompletableFuture — async parallel service calls in Java for MUFG trade enrichment",
   "java","concurrency","Hard",_MUFG,90,
   "completablefuture,async,parallel,thenCompose,allOf,banking,java8","Technical Round",
   A(("Use Case — Trade Enrichment",
      "MUFG trade booking: fetch FX rate, counterparty details, limit check <b>in parallel</b>, "
      "then combine results. Sequential = 3 &times; 200ms = 600ms. Parallel = 200ms."),
     ("Architecture Diagram",
      "<pre>"
      "  bookTrade()\n"
      "       |\n"
      "  +----+----+----------+\n"
      "  |         |          |\n"
      " getFxRate  getCP    checkLimit\n"
      " (200ms)  (150ms)   (180ms)\n"
      "  |         |          |\n"
      "  +----+----+----------+\n"
      "       | allOf().join()\n"
      "       v\n"
      "  combineAndSave()\n"
      "  total: ~200ms (not 530ms)\n"
      "</pre>"),
     ("Code",
      "<pre>public TradeBookingResult bookTrade(TradeRequest req) {\n    ExecutorService pool = Executors.newFixedThreadPool(10);\n\n    CompletableFuture&lt;FxRate&gt; fxFuture =\n        CompletableFuture.supplyAsync(() -&gt; fxService.getRate(req.getCurrency()), pool)\n            .orTimeout(500, TimeUnit.MILLISECONDS)\n            .exceptionally(ex -&gt; FxRate.fallback());\n\n    CompletableFuture&lt;Counterparty&gt; cpFuture =\n        CompletableFuture.supplyAsync(() -&gt; cpService.get(req.getCounterpartyId()), pool);\n\n    CompletableFuture&lt;LimitCheck&gt; limitFuture =\n        CompletableFuture.supplyAsync(() -&gt; limitService.check(req), pool);\n\n    CompletableFuture.allOf(fxFuture, cpFuture, limitFuture).join();\n\n    if (!limitFuture.join().isApproved())\n        throw new LimitBreachException();\n\n    return tradeRepo.save(Trade.builder()\n        .amount(req.getAmount().multiply(fxFuture.join().getRate()))\n        .counterparty(cpFuture.join())\n        .build());\n}\n\n// Chain: thenCompose = flatMap (returns another CF)\nCompletableFuture&lt;EnrichedTrade&gt; enriched =\n    CompletableFuture.supplyAsync(() -&gt; tradeRepo.findById(id))\n        .thenCompose(trade -&gt; enrichmentService.enrich(trade));\n\n// Java 21: virtual threads — no pool sizing needed\ntry (var executor = Executors.newVirtualThreadPerTaskExecutor()) {\n    CompletableFuture.supplyAsync(() -&gt; fxService.getRate(cur), executor);\n}</pre>"),
     ("Cross-Questions",
      '<div class="followup">'
      '&bull; thenApply vs thenCompose — key difference? (thenApply=map sync; thenCompose=flatMap async)<br>'
      '&bull; How does exceptionally() differ from handle()?<br>'
      '&bull; What happens to CF if thread pool is exhausted? (submit blocks or RejectedExecutionException)<br>'
      '&bull; When prefer Java 21 virtual threads over CompletableFuture?<br>'
      '&bull; How do you cancel a CompletableFuture? (cancel(true) — does NOT interrupt threads)'
      '</div>'))),

  ("mufg035","Java Memory Model — happens-before, volatile, synchronized in banking concurrency",
   "java","concurrency","Hard",_MUFG,85,
   "jmm,happens-before,volatile,synchronized,visibility,ordering","Technical Round",
   A(("Why JMM Matters in Banking",
      "Without JMM guarantees: Thread A writes trade status=SETTLED, "
      "Thread B reads stale PENDING from CPU cache &rarr; double settlement!"),
     ("Happens-Before Rules",
      "<pre>"
      "  Rule                      | Guarantee\n"
      "  --------------------------+-----------------------------\n"
      "  Program order             | Actions in thread are ordered\n"
      "  Monitor lock (sync block) | unlock HB next lock\n"
      "  volatile write/read       | write HB subsequent read\n"
      "  Thread.start()            | start() HB any action in thread\n"
      "  Thread.join()             | all actions HB join() return\n"
      "</pre>"),
     ("volatile vs synchronized vs AtomicLong",
      "<pre>// volatile: visibility ONLY, no atomicity\nprivate volatile boolean running = true;   // safe for simple flag\nprivate volatile long counter = 0;          // NOT safe for i++!\n\n// synchronized: visibility + atomicity\nprivate long counter = 0;\npublic synchronized void increment() { counter++; }  // safe\n\n// AtomicLong: lock-free CAS — best for high-contention counters\nprivate final AtomicLong tradeCount = new AtomicLong(0);\ntradeCount.incrementAndGet();  // CAS at CPU level\n\n// Double-checked locking — MUST use volatile\nprivate static volatile TradeCache instance;\npublic static TradeCache getInstance() {\n    if (instance == null) {\n        synchronized (TradeCache.class) {\n            if (instance == null)\n                instance = new TradeCache();  // volatile ensures write visible\n        }\n    }\n    return instance;\n}</pre>"),
     ("CPU Cache Visibility Diagram",
      "<pre>"
      "  Thread-1 (Core 1)      Thread-2 (Core 2)\n"
      "  L1 Cache               L1 Cache\n"
      "  status=SETTLED         status=PENDING  &lt;-- STALE!\n"
      "       |\n"
      "  L3 Cache (shared) &lt;-- volatile/sync flushes here\n"
      "       |\n"
      "  Main Memory: SETTLED\n"
      "</pre>"),
     ("Cross-Questions",
      '<div class="followup">'
      '&bull; What is a data race? Give a banking example.<br>'
      '&bull; Why is double-checked locking broken without volatile in Java &lt;5?<br>'
      '&bull; Difference between CAS and mutex?<br>'
      '&bull; How does StampedLock differ from ReentrantReadWriteLock?<br>'
      '&bull; How to detect thread safety issues in production? (ThreadSanitizer, async-profiler)'
      '</div>'))),

  ("mufg036","LRU Cache — implement O(1) get/put using HashMap + DoublyLinkedList",
   "coding","data_structures","Hard",_MUFG,88,
   "lru-cache,hashmap,doubly-linked-list,o1,cache,leetcode-146","Coding Round",
   A(("Problem",
      "Design a cache that evicts the <b>Least Recently Used</b> item when full. "
      "<b>Both get() and put() must be O(1).</b><br>"
      "MUFG use case: Cache FX rates (capacity=1000, evict stale entries on overflow)."),
     ("Design Diagram",
      "<pre>"
      "  HashMap&lt;key, Node&gt;              DoublyLinkedList\n"
      "  +----+--------+              HEAD &lt;-&gt; [A] &lt;-&gt; [B] &lt;-&gt; [C] &lt;-&gt; TAIL\n"
      "  | A  | Node*A |              (MRU)                           (LRU)\n"
      "  | B  | Node*B |\n"
      "  | C  | Node*C |  get(A): move A to HEAD  -- O(1)\n"
      "  +----+--------+  put(D): add D to HEAD, remove TAIL (C) -- O(1)\n"
      "</pre>"),
     ("Java Implementation",
      "<pre>class LRUCache {\n    private final int capacity;\n    private final Map&lt;Integer, Node&gt; map = new HashMap&lt;&gt;();\n    private final Node head = new Node(0,0), tail = new Node(0,0);\n\n    public LRUCache(int capacity) {\n        this.capacity = capacity;\n        head.next = tail; tail.prev = head;\n    }\n\n    public int get(int key) {\n        if (!map.containsKey(key)) return -1;\n        Node n = map.get(key);\n        moveToFront(n);\n        return n.val;\n    }\n\n    public void put(int key, int val) {\n        if (map.containsKey(key)) {\n            map.get(key).val = val;\n            moveToFront(map.get(key));\n        } else {\n            if (map.size() == capacity)\n                map.remove(removeLast());\n            Node n = new Node(key, val);\n            map.put(key, n);\n            addToFront(n);\n        }\n    }\n\n    private void addToFront(Node n) {\n        n.next = head.next; n.prev = head;\n        head.next.prev = n; head.next = n;\n    }\n    private void moveToFront(Node n) { remove(n); addToFront(n); }\n    private void remove(Node n) { n.prev.next = n.next; n.next.prev = n.prev; }\n    private int removeLast() {\n        Node lru = tail.prev; remove(lru); return lru.key;\n    }\n    static class Node { int key, val; Node prev, next; Node(int k, int v){key=k;val=v;} }\n}\n// Java shortcut: LinkedHashMap(capacity, 0.75f, true) with removeEldestEntry</pre>"),
     ("Cross-Questions",
      '<div class="followup">'
      '&bull; How to make this thread-safe? (ConcurrentHashMap + ReentrantReadWriteLock)<br>'
      '&bull; LRU vs LFU — when to prefer LFU? (frequency-based eviction for skewed access)<br>'
      '&bull; How does LinkedHashMap implement LRU? (override removeEldestEntry)<br>'
      '&bull; Time/space complexity? (O(1) all ops, O(capacity) space)<br>'
      '&bull; Distributed LRU? (Redis with eviction policy allkeys-lru + TTL)'
      '</div>'))),

  ("mufg037","Sliding Window — max sum subarray and longest substring without repeating chars",
   "coding","algorithms","Medium",_MUFG,85,
   "sliding-window,two-pointer,subarray,substring,leetcode","Coding Round",
   A(("Pattern Overview",
      "<b>Sliding Window</b>: Maintain a window [left, right]. "
      "Expand right, shrink left when condition violated. "
      "Avoids O(n&sup2;) nested loops &rarr; O(n).<br>"
      "<b>MUFG use case:</b> Max transaction volume in any 5-minute window for anomaly detection."),
     ("Fixed Window — Max Sum of K Elements",
      "<pre>public int maxSum(int[] arr, int k) {\n    int windowSum = 0, maxSum = 0;\n    for (int i = 0; i &lt; k; i++) windowSum += arr[i];  // first window\n    maxSum = windowSum;\n    for (int i = k; i &lt; arr.length; i++) {\n        windowSum += arr[i] - arr[i - k];  // slide: add right, remove left\n        maxSum = Math.max(maxSum, windowSum);\n    }\n    return maxSum;\n}</pre>"),
     ("Variable Window — Longest Substring No Repeats (LC-3)",
      "<pre>public int lengthOfLongestSubstring(String s) {\n    Map&lt;Character, Integer&gt; freq = new HashMap&lt;&gt;();\n    int left = 0, maxLen = 0;\n    for (int right = 0; right &lt; s.length(); right++) {\n        freq.merge(s.charAt(right), 1, Integer::sum);\n        while (freq.get(s.charAt(right)) &gt; 1) {\n            freq.merge(s.charAt(left), -1, Integer::sum);\n            if (freq.get(s.charAt(left)) == 0) freq.remove(s.charAt(left));\n            left++;\n        }\n        maxLen = Math.max(maxLen, right - left + 1);\n    }\n    return maxLen;\n}</pre>"),
     ("Cross-Questions",
      '<div class="followup">'
      '&bull; Sliding window vs Two Pointers — difference?<br>'
      '&bull; How to find minimum window substring? (LC-76 — track missing chars with counter)<br>'
      '&bull; How to find all anagrams in a string? (LC-438 — fixed window + freq match)<br>'
      '&bull; Time/space complexity? O(n) time, O(k) space for freq map<br>'
      '&bull; Apply to fraud detection: max transactions in rolling 1h window?'
      '</div>'))),

  ("mufg038","N+1 Query Problem — detect and fix with JPA/Hibernate in Spring Boot",
   "database","jpa_hibernate","Hard",_MUFG,92,
   "n+1-query,hibernate,jpa,fetch,join-fetch,entitygraph,lazy-loading","Technical Round",
   A(("The Problem",
      "<b>N+1 queries</b>: 1 query to load N parent records + N queries for each child = N+1 DB calls.<br>"
      "MUFG example: Load 100 trades &rarr; 1 query + 100 queries for counterparty = 101 round-trips!"),
     ("How It Happens",
      "<pre>@Entity\npublic class Trade {\n    @ManyToOne(fetch = FetchType.LAZY)  // LAZY is default\n    private Counterparty counterparty;\n}\n\nList&lt;Trade&gt; trades = tradeRepo.findAll(); // 1 SELECT\nfor (Trade t : trades) {\n    t.getCounterparty().getName(); // triggers N SELECTs!\n}\n// Hibernate logs:\n// SELECT * FROM trades;\n// SELECT * FROM counterparty WHERE id=1\n// SELECT * FROM counterparty WHERE id=2  ... x100</pre>"),
     ("Fix 1 — JOIN FETCH",
      "<pre>@Query(\"SELECT t FROM Trade t JOIN FETCH t.counterparty\")\nList&lt;Trade&gt; findAllWithCounterparty();\n// 1 SQL: SELECT t.*, c.* FROM trades t JOIN counterparty c ON t.cp_id=c.id</pre>"),
     ("Fix 2 — @EntityGraph",
      "<pre>@EntityGraph(attributePaths = {\"counterparty\", \"instrument\"})\n@Query(\"SELECT t FROM Trade t\")\nList&lt;Trade&gt; findAllEager();\n// Best for multiple associations — cleaner than FETCH JOIN\n// Avoids Cartesian product with multiple collections</pre>"),
     ("Fix 3 — Batch Size",
      "<pre>@BatchSize(size = 25)\n@ManyToOne(fetch = FetchType.LAZY)\nprivate Counterparty counterparty;\n// 100 trades -&gt; 4 batch queries instead of 100\n// spring.jpa.properties.hibernate.default_batch_fetch_size=25</pre>"),
     ("Detect N+1",
      "<pre># application.properties\nspring.jpa.properties.hibernate.generate_statistics=true\nlogging.level.org.hibernate.stat=DEBUG\n# See: 101 queries for 100 trades -&gt; N+1 confirmed!\n# Tools: p6spy, datasource-proxy, Hypersistence Optimizer</pre>"),
     ("Cross-Questions",
      '<div class="followup">'
      '&bull; EAGER vs LAZY — default for @OneToMany, @ManyToOne?<br>'
      '&bull; What is the Cartesian product problem with multiple JOIN FETCHes?<br>'
      '&bull; How to fix N+1 for @OneToMany? (JOIN FETCH with DISTINCT or @BatchSize)<br>'
      '&bull; How do you page JOIN FETCH results? (use @EntityGraph — JOIN FETCH breaks pagination)<br>'
      '&bull; What is the Open Session in View anti-pattern?'
      '</div>'))),

  ("mufg039","HikariCP Connection Pooling — optimal configuration for MUFG banking throughput",
   "database","connection_pooling","Medium",_MUFG,88,
   "hikaricp,connection-pool,jdbc,throughput,banking,spring-boot","Technical Round",
   A(("Why Connection Pools Matter",
      "Creating a DB connection = TCP handshake + DB auth + memory &asymp; 50-100ms. "
      "At 1000 TPS, creating new connections every time = disaster. "
      "<b>HikariCP</b> pre-creates and reuses connections &rarr; sub-millisecond acquisition."),
     ("Architecture Diagram",
      "<pre>"
      "  Spring Boot App (10 instances)\n"
      "  +---------------------------+\n"
      "  |   HikariCP Pool           |\n"
      "  |  [c1][c2][c3]...[c10]    | max-pool-size=10\n"
      "  |   idle  busy  busy        |\n"
      "  +---------------------------+\n"
      "         | JDBC\n"
      "  +------v-------+\n"
      "  |  PostgreSQL   |  max_connections=100\n"
      "  +--------------+\n"
      "  Rule: pool_per_instance = DB_max / num_instances\n"
      "        = 100 / 10 = 10\n"
      "</pre>"),
     ("Optimal Config",
      "<pre># application.properties\nspring.datasource.hikari.maximum-pool-size=10\nspring.datasource.hikari.minimum-idle=5\nspring.datasource.hikari.connection-timeout=30000\nspring.datasource.hikari.idle-timeout=600000\nspring.datasource.hikari.max-lifetime=1800000\nspring.datasource.hikari.keepalive-time=60000\nspring.datasource.hikari.pool-name=MufgTradePool\n# Leak detection: warn if connection held &gt; 2s\nspring.datasource.hikari.leak-detection-threshold=2000\n# Formula: pool_size = (cores * 2) + spindles = (4*2)+1 = 9</pre>"),
     ("Cross-Questions",
      '<div class="followup">'
      '&bull; What happens when all pool connections are busy? (ConnectionTimeoutException)<br>'
      '&bull; HikariCP vs c3p0/DBCP — why HikariCP wins? (faster, simpler, zero-overhead)<br>'
      '&bull; How to tune pool for read replicas vs primary? (separate DataSource beans)<br>'
      '&bull; What is connection validation? (SELECT 1 ping before use)<br>'
      '&bull; How does HikariCP handle connection leaks? (leak-detection-threshold + stack trace log)'
      '</div>'))),

  ("mufg040","TLS 1.3 Handshake + mTLS — securing MUFG inter-service communication",
   "security","tls_mtls","Hard",_MUFG,86,
   "tls,tls1.3,mtls,certificates,ssl,handshake,zero-trust,banking","Technical Round",
   A(("TLS 1.3 Handshake (1-RTT vs TLS 1.2 2-RTT)",
      "<pre>"
      "  Client                    Server\n"
      "    |--ClientHello---------->|\n"
      "    |  key_share (ECDHE)     |\n"
      "    |                        |\n"
      "    |&lt;-ServerHello+Cert------|\n"
      "    |  server key_share      |\n"
      "    |  [both derive session] |\n"
      "    |--Finished (encrypted)->|\n"
      "    |&lt;-Finished (encrypted)--|\n"
      "    |===Encrypted Data=======|\n"
      "    TLS 1.2: 2 RTT  TLS 1.3: 1 RTT (0-RTT resumption)\n"
      "</pre>"),
     ("mTLS — Mutual Authentication",
      "<pre>"
      "  Trade-Svc              Payment-Svc\n"
      "     |--ClientHello--------->|\n"
      "     |&lt;-ServerHello+Cert-----|\n"
      "     |--Client Cert--------->|  &lt;-- mTLS: client also proves identity!\n"
      "     |&lt;-Verified-------------|\n"
      "     |===Encrypted channel===|\n"
      "  Zero-Trust: every service proves who it is\n"
      "</pre>"),
     ("Spring Boot mTLS Config",
      "<pre># application.properties\nserver.ssl.key-store=classpath:trade-svc-keystore.p12\nserver.ssl.key-store-password=${SSL_KEYSTORE_PASS}\nserver.ssl.trust-store=classpath:mufg-truststore.p12\nserver.ssl.trust-store-password=${SSL_TRUSTSTORE_PASS}\nserver.ssl.client-auth=need   # require client cert (mTLS)\nserver.ssl.enabled-protocols=TLSv1.3\n\n// Outgoing RestTemplate with client cert\n@Bean\npublic RestTemplate secureRestTemplate() throws Exception {\n    SSLContext ssl = SSLContextBuilder.create()\n        .loadKeyMaterial(keyStore, keyPass)\n        .loadTrustMaterial(trustStore)\n        .build();\n    return new RestTemplate(new HttpComponentsClientHttpRequestFactory(\n        HttpClients.custom().setSSLContext(ssl).build()));\n}</pre>"),
     ("Key Concepts",
      "<ul>"
      "<li><b>ECDHE:</b> Ephemeral key exchange &rarr; Perfect Forward Secrecy (PFS)</li>"
      "<li><b>PFS:</b> Each session unique key &rarr; past sessions safe if server key leaked</li>"
      "<li><b>mTLS vs JWT:</b> mTLS = transport identity; JWT = application identity</li>"
      "<li><b>SPIFFE/SPIRE:</b> Kubernetes auto cert rotation for mTLS (used with Istio)</li>"
      "</ul>"),
     ("Cross-Questions",
      '<div class="followup">'
      '&bull; What is Perfect Forward Secrecy and why is it critical in banking?<br>'
      '&bull; How does certificate rotation work without downtime?<br>'
      '&bull; TLS vs HTTPS — difference? (HTTPS = HTTP over TLS)<br>'
      '&bull; What is SNI? (Server Name Indication — multiple certs on same IP)<br>'
      '&bull; How does Istio handle mTLS? (auto cert rotation via SPIFFE/SPIRE)'
      '</div>'))),

  ("mufg041","CQRS Pattern — separating read/write models in MUFG trade reporting",
   "system_design","cqrs","Hard",_MUFG,84,
   "cqrs,command-query,read-model,write-model,event-sourcing,ddd","System Design Round",
   A(("What Is CQRS?",
      "<b>Command Query Responsibility Segregation:</b> Separate the <b>write model</b> (commands, normalized) "
      "from the <b>read model</b> (queries, denormalized).<br>"
      "<b>MUFG:</b> Write = PostgreSQL (ACID). Read = Elasticsearch (fast search/reporting)."),
     ("Architecture Diagram",
      "<pre>"
      "  UI / API\n"
      "   |           |\n"
      "COMMAND      QUERY\n"
      "   |           |\n"
      "Write DB    Read DB\n"
      "(Postgres)  (Elastic)\n"
      " ACID txn    Fast search\n"
      "   |\n"
      " Domain Events (Kafka)\n"
      "   |\n"
      " Event Handler\n"
      " (updates Read DB async)\n"
      "</pre>"),
     ("Spring Boot Implementation",
      "<pre>// Command controller\n@PostMapping(\"/api/v1/trades\")\npublic ResponseEntity&lt;String&gt; bookTrade(@RequestBody BookTradeCommand cmd) {\n    Trade t = tradeCommandService.book(cmd);     // writes PostgreSQL\n    eventBus.publish(new TradeBookedEvent(t));   // publishes Kafka\n    return ResponseEntity.accepted().body(t.getId());\n}\n\n// Query controller\n@GetMapping(\"/api/v1/trades/search\")\npublic List&lt;TradeView&gt; search(@RequestParam String counterparty) {\n    return tradeQueryService.searchByCounterparty(counterparty); // reads Elasticsearch\n}\n\n// Event handler syncs to read model\n@KafkaListener(topics = \"trade.booked\")\npublic void onTradeBooked(TradeBookedEvent event) {\n    elasticRepo.save(TradeView.from(event));  // denormalized view\n}</pre>"),
     ("Cross-Questions",
      '<div class="followup">'
      '&bull; CQRS vs Event Sourcing — same thing? (No, orthogonal but often combined)<br>'
      '&bull; How to handle eventual consistency? (show version/timestamp to user)<br>'
      '&bull; When NOT to use CQRS? (simple CRUD apps — adds complexity)<br>'
      '&bull; What is the read model consistency window? (typically &lt;100ms Kafka+Elastic)<br>'
      '&bull; How to rebuild read model from scratch? (replay all Kafka events from beginning)'
      '</div>'))),

  ("mufg042","Resilience4j Circuit Breaker + Bulkhead — prevent cascade failures in MUFG",
   "spring","resilience","Hard",_MUFG,89,
   "circuit-breaker,resilience4j,fallback,bulkhead,retry,cascade-failure","Technical Round",
   A(("Problem — Cascade Failure",
      "Trade service calls FX service. FX service is slow (DB overloaded). "
      "Trade service threads pile up waiting &rarr; OOM &rarr; cascade failure. "
      "<b>Fix: Circuit Breaker + Bulkhead</b>"),
     ("Circuit Breaker State Machine",
      "<pre>"
      "  +--------+  failures &gt; 50%   +------+\n"
      "  | CLOSED |------------------>| OPEN |\n"
      "  | normal |                   |fail  |\n"
      "  | traffic|                   |fast  |\n"
      "  +--------+                   +--+---+\n"
      "      ^                           |\n"
      "      | success                   | after 30s\n"
      "      +------------------+HALF-OPEN+\n"
      "                         | 3 trial requests |\n"
      "</pre>"),
     ("Resilience4j Config",
      "<pre># application.yml\nresilience4j:\n  circuitbreaker:\n    instances:\n      fxService:\n        failureRateThreshold: 50\n        slowCallDurationThreshold: 2000ms\n        waitDurationInOpenState: 30s\n        permittedNumberOfCallsInHalfOpenState: 3\n        slidingWindowSize: 20\n  retry:\n    instances:\n      fxService:\n        maxAttempts: 3\n        waitDuration: 200ms\n        exponentialBackoffMultiplier: 2\n  bulkhead:\n    instances:\n      fxService:\n        maxConcurrentCalls: 20\n\n@CircuitBreaker(name=\"fxService\", fallbackMethod=\"fxFallback\")\n@Retry(name=\"fxService\")\n@Bulkhead(name=\"fxService\")\npublic FxRate getFxRate(String currency) {\n    return fxClient.getRate(currency);\n}\n\npublic FxRate fxFallback(String currency, Exception ex) {\n    return rateCache.getLastKnownRate(currency);  // graceful degradation\n}</pre>"),
     ("Cross-Questions",
      '<div class="followup">'
      '&bull; CB vs Retry — when to use each? (CB: flapping service; Retry: transient errors)<br>'
      '&bull; What is Bulkhead? (isolate thread pools — FX failure cannot exhaust trade service)<br>'
      '&bull; Monitor CB state? (Actuator /circuitbreakers + Micrometer + Grafana)<br>'
      '&bull; Exponential backoff with jitter? (prevent thundering herd on recovery)<br>'
      '&bull; Resilience4j vs Hystrix? (Hystrix EOL; R4j is functional, lighter)'
      '</div>'))),

  ("mufg043","Kafka Consumer Groups — partition assignment and offset management",
   "system_design","messaging","Hard",_MUFG,87,
   "kafka,consumer-group,partition,offset,rebalance,at-least-once,banking","System Design Round",
   A(("Consumer Group Architecture",
      "<pre>"
      "  Kafka Topic: trade.events (6 partitions)\n"
      "  +----+----+----+----+----+----+\n"
      "  | P0 | P1 | P2 | P3 | P4 | P5 |\n"
      "  +----+----+----+----+----+----+\n"
      "    |    |     |    |     |    |\n"
      "  +------+  +------+  +------+\n"
      "  | C1   |  | C2   |  | C3   |\n"
      "  | P0,P1|  | P2,P3|  | P4,P5|\n"
      "  +------+  +------+  +------+\n"
      "  Group: mufg-settlement-service\n"
      "  Max parallelism = num partitions = 6\n"
      "</pre>"),
     ("Spring Kafka — Manual Offset Commit",
      "<pre>@KafkaListener(\n    topics = \"trade.events\",\n    groupId = \"mufg-settlement-service\",\n    concurrency = \"3\"\n)\npublic void processTradeEvent(\n        @Payload TradeEvent event,\n        Acknowledgment ack) {\n    try {\n        settlementService.process(event);\n        ack.acknowledge();  // commit AFTER processing (at-least-once)\n    } catch (FatalException e) {\n        ack.acknowledge();  // skip poison pill, send to DLT\n        kafkaTemplate.send(\"trade.events.DLT\", event);\n    }\n}\n\n# application.yml\nspring.kafka.consumer.enable-auto-commit: false\nspring.kafka.consumer.auto-offset-reset: earliest\nspring.kafka.listener.ack-mode: manual_immediate</pre>"),
     ("Delivery Semantics",
      "<pre>"
      "  At-most-once:  commit before process (may lose on crash)\n"
      "  At-least-once: commit after process  (may duplicate) &lt;-- MUFG default\n"
      "  Exactly-once:  Kafka Transactions + idempotent consumer\n"
      "  Idempotent consumer: processed_events table with event_id dedup\n"
      "</pre>"),
     ("Cross-Questions",
      '<div class="followup">'
      '&bull; What happens during consumer group rebalance? (partitions redistributed, brief pause)<br>'
      '&bull; How to handle poison pill messages? (Dead Letter Topic + alerting)<br>'
      '&bull; How to achieve exactly-once processing? (Kafka transactions + idempotent consumer)<br>'
      '&bull; What is consumer lag? (offset gap between latest and committed — monitor with Burrow)<br>'
      '&bull; Max consumers per topic group? (= num partitions; extras sit idle)'
      '</div>'))),

]

def _to_dict(q):
    return {"id":q[0],"text":q[1],"category":q[2],"subcategory":q[3],"difficulty":q[4],
            "companies":q[5],"frequency":q[6],"tags":q[7].split(","),"round_type":q[8],"answer_hint":q[9]}

QUESTIONS = [_to_dict(q) for q in MUFG3_Q]
