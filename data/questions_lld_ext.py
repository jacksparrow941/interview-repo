"""LLD Extended — Circuit Breaker, Distributed ID, Observer, Message Queue, Bloom Filter, Inventory."""

_G3 = ["Google","Meta","Amazon","Microsoft","Uber","LinkedIn"]
_IND = ["Razorpay","PhonePe","Swiggy","Zomato","CRED","Dream11","Groww"]

def A(*s):
    parts = [f'<span class="answer-label">{l}</span><br>{c}' for l,c in s]
    return '<div class="answer-section">'+'</div><div class="answer-section" style="margin-top:10px">'.join(parts)+'</div>'

LLD_EXT = [
  ("lldx001","Design a Circuit Breaker","lld","machine_coding","Hard",
   _G3[:4] + ["Stripe","Razorpay","CRED","PhonePe"], 86, "circuit-breaker,state-machine,resilience","LLD Round",
   A(("States","<b>CLOSED</b> → calls go through. <b>OPEN</b> → calls fail-fast (no downstream). "
      "<b>HALF_OPEN</b> → probe call, if succeeds → CLOSED, else → OPEN."),
     ("Full Implementation",
      "<pre>enum State { CLOSED, OPEN, HALF_OPEN }\n\nclass CircuitBreaker {\n    State state = CLOSED;\n    int failCount = 0, successCount = 0;\n    final int failThreshold = 5;\n    final int successThreshold = 2;\n    Instant openedAt;\n    final Duration timeout = Duration.ofSeconds(30);\n    final ReentrantLock lock = new ReentrantLock();\n\n    &lt;T&gt; T call(Supplier&lt;T&gt; fn) {\n        lock.lock(); try {\n            if (state == OPEN) {\n                if (Duration.between(openedAt, Instant.now()).compareTo(timeout) &gt; 0)\n                    state = HALF_OPEN;\n                else throw new CircuitOpenException();\n            }\n        } finally { lock.unlock(); }\n\n        try {\n            T result = fn.get();\n            onSuccess(); return result;\n        } catch (Exception e) { onFailure(); throw e; }\n    }\n\n    void onSuccess() {\n        lock.lock(); try {\n            if (state == HALF_OPEN &amp;&amp; ++successCount &gt;= successThreshold) {\n                state = CLOSED; failCount = 0; successCount = 0;\n            }\n        } finally { lock.unlock(); }\n    }\n\n    void onFailure() {\n        lock.lock(); try {\n            if (++failCount &gt;= failThreshold || state == HALF_OPEN) {\n                state = OPEN; openedAt = Instant.now(); successCount = 0;\n            }\n        } finally { lock.unlock(); }\n    }\n}</pre>"),
     ("Cross-questions","<ul><li>How do you make the thresholds configurable at runtime?</li>"
      "<li>How do you implement per-endpoint circuit breakers?</li>"
      "<li>How does Resilience4j implement circuit breaker differently? (sliding window: count/time based)</li>"
      "<li>How do you expose circuit breaker state via metrics/health endpoint?</li></ul>"),
     ("Follow-ups",'<div class="followup">• What is the difference between circuit breaker and retry with backoff?<br>'
      '• How does Hystrix compare to Resilience4j?<br>'
      '• How would you implement bulkhead pattern alongside circuit breaker?</div>'))),

  ("lldx002","Design a Snowflake-style Distributed ID Generator","lld","machine_coding","Hard",
   _G3 + _IND + ["Stripe","Coinbase"], 88, "snowflake,distributed-id,epoch,machine-id","LLD Round",
   A(("Twitter Snowflake Structure (64-bit)",
      "<pre>| 1 bit sign | 41 bits timestamp (ms) | 10 bits machine ID | 12 bits sequence |\n\n- Timestamp: ms since custom epoch (Jan 1, 2010)\n  → supports 2^41 ms ≈ 69 years\n- Machine ID: 10 bits → 1024 machines\n- Sequence: 12 bits → 4096 IDs/ms/machine\n\nTotal: ~4 million IDs/second per machine, globally unique, sortable!</pre>"),
     ("Implementation",
      "<pre>class SnowflakeIdGenerator {\n    private final long EPOCH = 1288834974657L;  // Nov 4, 2010\n    private final long MACHINE_ID;              // 0-1023\n    private long sequence = 0;\n    private long lastTs = -1;\n\n    synchronized long nextId() {\n        long ts = System.currentTimeMillis();\n        if (ts == lastTs) {\n            sequence = (sequence + 1) &amp; 0xFFF;  // 12-bit mask\n            if (sequence == 0) ts = waitNextMs(lastTs);  // sequence exhausted\n        } else { sequence = 0; }\n        lastTs = ts;\n        return ((ts - EPOCH) &lt;&lt; 22) | (MACHINE_ID &lt;&lt; 12) | sequence;\n    }\n\n    private long waitNextMs(long ts) {\n        long now = System.currentTimeMillis();\n        while (now &lt;= ts) now = System.currentTimeMillis();\n        return now;\n    }\n}</pre>"),
     ("Cross-questions","<ul><li>What happens if system clock goes backwards? (NTP clock skew) → block until clock catches up</li>"
      "<li>How do you assign machine IDs in a dynamic cloud environment? (ZooKeeper ephemeral node, Redis INCR)</li>"
      "<li>How would you make it monotonic across machines? (ULIDs)</li>"
      "<li>Why is UUID v4 not a good database primary key? (random → B+tree fragmentation)</li></ul>"),
     ("Follow-ups",'<div class="followup">• What is ULID and how does it improve on UUID?<br>'
      '• How does Instagram\'s ID generation work? (PostgreSQL function + shard ID)<br>'
      '• What is the trade-off between centralized vs decentralized ID generation?</div>'))),

  ("lldx003","Design an in-memory Message Queue (pub/sub + queuing)","lld","machine_coding","Hard",
   _G3 + ["Stripe","Razorpay","CRED"], 84, "message-queue,pub-sub,topic,consumer-group","LLD Round",
   A(("Requirements","Push/pull delivery, topic-based routing, consumer groups, at-least-once delivery, "
      "offset tracking, TTL for messages."),
     ("Design",
      "<pre>class Message { String id, topicName, payload; long timestamp; }\n\nclass Topic {\n    String name;\n    List&lt;Message&gt; messages = new CopyOnWriteArrayList&lt;&gt;();\n    // Consumer group → offset\n    Map&lt;String, AtomicLong&gt; groupOffsets = new ConcurrentHashMap&lt;&gt;();\n\n    void publish(Message msg) { messages.add(msg); notifySubscribers(); }\n\n    List&lt;Message&gt; poll(String group, int maxMsgs) {\n        long offset = groupOffsets.computeIfAbsent(group, k-&gt; new AtomicLong(0)).get();\n        List&lt;Message&gt; batch = messages.subList(\n            (int)offset, Math.min((int)offset + maxMsgs, messages.size()));\n        groupOffsets.get(group).addAndGet(batch.size());\n        return batch;\n    }\n}\n\nclass MessageBroker {\n    Map&lt;String, Topic&gt; topics = new ConcurrentHashMap&lt;&gt;();\n    // Subscribe with push callback:\n    void subscribe(String topic, String group, Consumer&lt;Message&gt; handler) { ... }\n    void publish(String topic, String payload) { ... }\n}</pre>"),
     ("Cross-questions","<ul><li>How do you implement exactly-once delivery? (idempotency key + deduplication store)</li>"
      "<li>How does acknowledgement work? (mark offset committed only after processing)</li>"
      "<li>How do you handle slow consumers? (max lag threshold, dead-letter queue)</li>"
      "<li>How would you persist messages to disk? (WAL/append-only log)</li></ul>"),
     ("Follow-ups",'<div class="followup">• How does Kafka differ from RabbitMQ in delivery semantics?<br>'
      '• What is a dead letter queue (DLQ)?<br>'
      '• How do you implement message ordering within a partition?</div>'))),

  ("lldx004","Design a Bloom Filter","lld","machine_coding","Hard",
   _G3[:4] + ["Stripe","Databricks","Coinbase"], 82, "bloom-filter,probabilistic,bitarray,hash","LLD Round",
   A(("What is a Bloom Filter","Space-efficient probabilistic data structure. "
      "Answers: 'definitely not in set' OR 'probably in set'. No false negatives, configurable false positive rate."),
     ("Implementation",
      "<pre>class BloomFilter {\n    private final BitSet bits;\n    private final int numBits;\n    private final int numHashFunctions;\n\n    BloomFilter(int expectedItems, double falsePositiveRate) {\n        // Optimal bit count: -n*ln(p) / (ln2)^2\n        numBits = (int)(-expectedItems * Math.log(falsePositiveRate) / (Math.log(2)*Math.log(2)));\n        // Optimal hash count: (m/n) * ln2\n        numHashFunctions = (int)(numBits * 1.0 / expectedItems * Math.log(2));\n        bits = new BitSet(numBits);\n    }\n\n    void add(String item) {\n        for (int i = 0; i &lt; numHashFunctions; i++)\n            bits.set(Math.abs(hash(item, i)) % numBits);\n    }\n\n    boolean mightContain(String item) {\n        for (int i = 0; i &lt; numHashFunctions; i++)\n            if (!bits.get(Math.abs(hash(item, i)) % numBits)) return false;  // Definitely not\n        return true;  // Probably yes\n    }\n\n    private int hash(String s, int seed) {\n        return Objects.hash(s, seed);\n    }\n}</pre>"),
     ("Cross-questions","<ul><li>How do you calculate false positive rate given n items and m bits? (1 - e^(-kn/m))^k</li>"
      "<li>Can you delete from a Bloom filter? (No — use Counting Bloom Filter instead)</li>"
      "<li>What is Cuckoo filter and how does it improve on Bloom? (supports deletion, better lookup perf)</li>"
      "<li>How does Cassandra use Bloom filters? (before SSTable disk lookup)</li></ul>"),
     ("Follow-ups",'<div class="followup">• What is a scalable Bloom filter?<br>'
      '• How does Redis implement Bloom filter? (RedisBloom module)<br>'
      '• What is HyperLogLog and how does it differ from Bloom filter?</div>'))),

  ("lldx005","Design a Job/Task Scheduler","lld","machine_coding","Hard",
   _G3 + ["Stripe","Razorpay","CRED","Dream11"], 86, "scheduler,priority-queue,cron,delayed-execution","LLD Round",
   A(("Requirements","One-time delayed jobs, recurring (cron-like) jobs, priority, retry on failure, cancellation, status tracking."),
     ("Core Design",
      "<pre>class Job {\n    String id; Runnable task; JobStatus status;\n    long scheduledAt;  // epoch ms\n    int priority, maxRetries, retryCount;\n    String cronExpr;   // null for one-time jobs\n}\n\nclass Scheduler {\n    // Min-heap by scheduledAt\n    PriorityQueue&lt;Job&gt; queue = new PriorityQueue&lt;&gt;(\n        Comparator.comparingLong((Job j) -&gt; j.scheduledAt)\n                  .thenComparing(j -&gt; -j.priority));\n    ScheduledExecutorService executor = Executors.newScheduledThreadPool(4);\n    Map&lt;String, ScheduledFuture&lt;?&gt;&gt; running = new ConcurrentHashMap&lt;&gt;();\n\n    String schedule(Runnable task, long delayMs, int priority) {\n        Job job = new Job(UUID.randomUUID().toString(), task, \n                          System.currentTimeMillis() + delayMs, priority);\n        queue.offer(job);\n        return job.id;\n    }\n\n    void processJobs() {\n        while (!Thread.currentThread().isInterrupted()) {\n            Job job = queue.peek();\n            if (job == null || job.scheduledAt &gt; System.currentTimeMillis()) {\n                Thread.sleep(10); continue;\n            }\n            queue.poll();\n            executor.submit(() -&gt; executeWithRetry(job));\n        }\n    }\n\n    void executeWithRetry(Job job) {\n        try { job.task.run(); job.status = COMPLETED; }\n        catch (Exception e) {\n            if (job.retryCount++ &lt; job.maxRetries) {\n                job.scheduledAt = System.currentTimeMillis() + backoff(job.retryCount);\n                queue.offer(job);\n            } else { job.status = FAILED; }\n        }\n    }\n}</pre>"),
     ("Cross-questions","<ul><li>How do you implement cron expression parsing? (Quartz CronExpression)</li>"
      "<li>How do you make the scheduler distributed? (database-backed queue, leader election)</li>"
      "<li>How do you prevent duplicate job execution in distributed scheduler? (pessimistic lock on job row)</li>"
      "<li>How does exponential backoff work? (delay = base × 2^retryCount + jitter)</li></ul>"),
     ("Follow-ups",'<div class="followup">• How does Quartz Scheduler handle clustering?<br>'
      '• What is the difference between at-most-once and at-least-once job execution?<br>'
      '• How would you implement a workflow engine (job dependencies)?</div>'))),

  ("lldx006","Design an Inventory Management System","lld","machine_coding","Hard",
   ["Amazon","Flipkart","Walmart","Meesho","CRED","Razorpay"], 84, "inventory,oop,concurrency,event-sourcing","LLD Round",
   A(("Entities",
      "<pre>class Product { String id, name, category; double price; }\n\nclass InventoryItem {\n    Product product; int availableQty, reservedQty, soldQty;\n    String warehouseId;\n}\n\nclass Order { String id; Map&lt;String,Integer&gt; items; OrderStatus status; }\n\nclass Warehouse { String id, location; Map&lt;String,InventoryItem&gt; inventory; }</pre>"),
     ("Thread-safe Reserve + Fulfill",
      "<pre>class InventoryService {\n    Map&lt;String, ReentrantLock&gt; productLocks = new ConcurrentHashMap&lt;&gt;();\n    Map&lt;String, InventoryItem&gt; inventory = new ConcurrentHashMap&lt;&gt;();\n\n    boolean reserve(String productId, int qty) {\n        ReentrantLock lock = productLocks.computeIfAbsent(productId, k -&gt; new ReentrantLock());\n        lock.lock();\n        try {\n            InventoryItem item = inventory.get(productId);\n            if (item.availableQty &lt; qty) return false;  // insufficient stock\n            item.availableQty -= qty;\n            item.reservedQty += qty;\n            return true;\n        } finally { lock.unlock(); }\n    }\n\n    void fulfill(String productId, int qty) { // on order shipped\n        // lock, reservedQty -= qty, soldQty += qty\n    }\n\n    void release(String productId, int qty) { // on order cancel\n        // lock, reservedQty -= qty, availableQty += qty\n    }\n}</pre>"),
     ("Cross-questions","<ul><li>How do you prevent overselling in high-concurrency flash sales? (DB-level lock with FOR UPDATE SKIP LOCKED)</li>"
      "<li>How do you handle inventory across multiple warehouses? (routing strategy: nearest, FIFO)</li>"
      "<li>How would you implement inventory events for audit log? (Event Sourcing pattern)</li>"
      "<li>How do you handle partial reservation? (saga pattern: reserve each item, rollback all on failure)</li></ul>"),
     ("Follow-ups",'<div class="followup">• What is the saga pattern and how does it apply to multi-item orders?<br>'
      '• How would you implement low-stock alerts? (observer pattern + threshold)<br>'
      '• How does Amazon handle inventory reservation at massive scale?</div>'))),

  ("lldx007","Design a Sliding Window Rate Limiter (code-level)","lld","machine_coding","Hard",
   _G3 + _IND + ["Stripe","Coinbase"], 90, "rate-limiter,sliding-window,redis,concurrent","LLD Round",
   A(("Sliding Window Log Algorithm","Store timestamps of each request in a sorted set. On each request: "
      "remove old entries, count remaining, allow if below limit."),
     ("In-Memory Thread-Safe",
      "<pre>class SlidingWindowRateLimiter {\n    private final int maxRequests;\n    private final long windowMs;\n    private final Map&lt;String, Deque&lt;Long&gt;&gt; windows = new ConcurrentHashMap&lt;&gt;();\n\n    boolean allow(String clientId) {\n        long now = System.currentTimeMillis();\n        long cutoff = now - windowMs;\n\n        Deque&lt;Long&gt; timestamps = windows.computeIfAbsent(clientId, k -&gt; new ArrayDeque&lt;&gt;());\n\n        synchronized (timestamps) {\n            // Remove expired\n            while (!timestamps.isEmpty() &amp;&amp; timestamps.peekFirst() &lt;= cutoff)\n                timestamps.pollFirst();\n            if (timestamps.size() &gt;= maxRequests) return false;\n            timestamps.addLast(now);\n            return true;\n        }\n    }\n}</pre>"),
     ("Redis-based (Distributed)",
      "<pre>MULTI\nZREMRANGEBYSCORE rate:user1 0 {window_start}\nZCARD rate:user1\nZADD rate:user1 {now} {request_uuid}\nEXPIRE rate:user1 {window_seconds}\nEXEC\n-- Check count from ZCARD result &lt; limit</pre>"),
     ("Cross-questions","<ul><li>How does sliding window differ from fixed window? (fixed window: burst at boundary)</li>"
      "<li>How do you implement per-route limits vs global user limits?</li>"
      "<li>What is the token bucket trade-off vs sliding window? (token bucket allows bursting)</li>"
      "<li>How do you handle distributed rate limiting across 10 API servers?</li></ul>"),
     ("Follow-ups",'<div class="followup">• What is the leaky bucket algorithm?<br>'
      '• How do you rate-limit by user + endpoint combination?<br>'
      '• What is cell-based rate limiting (GCRA)?</div>'))),
]

def _to_dict(q):
    return {"id":q[0],"text":q[1],"category":q[2],"subcategory":q[3],"difficulty":q[4],
            "companies":q[5],"frequency":q[6],"tags":q[7].split(","),"round_type":q[8],"answer_hint":q[9]}

QUESTIONS = [_to_dict(q) for q in LLD_EXT]
