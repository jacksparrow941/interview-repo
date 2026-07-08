"""Full answers for all BACKEND_QUESTIONS (b001-b020) from questions_other.py."""

def A(*s):
    parts = [f'<span class="answer-label">{l}</span><br>{c}' for l,c in s]
    return '<div class="answer-section">'+'</div><div class="answer-section" style="margin-top:10px">'.join(parts)+'</div>'

FULL_ANSWERS_BACKEND = {

"b001": A(("REST vs GraphQL vs gRPC",
    "<ul><li><b>REST:</b> Stateless, resource-based (nouns), HTTP verbs. Cacheable, universally supported. "
    "Over-fetching (get entire user object for just the name) / under-fetching (need 3 calls for related data).</li>"
    "<li><b>GraphQL:</b> Single endpoint. Client specifies exact fields. Eliminates over/under-fetching. "
    "Schema as contract. N+1 problem (use DataLoader). Good for complex UIs, mobile (save bandwidth).</li>"
    "<li><b>gRPC:</b> HTTP/2 + Protocol Buffers. Binary, strongly typed, 5-10x smaller than JSON. "
    "Bidirectional streaming. Generated client/server stubs. Best for internal microservices.</li></ul>"),
  ("Decision Matrix",
    "<ul><li>Public API / browser-to-server → <b>REST</b></li>"
    "<li>Complex UI with diverse data needs → <b>GraphQL</b></li>"
    "<li>Internal microservice-to-microservice → <b>gRPC</b></li>"
    "<li>Real-time bidirectional → <b>WebSocket</b></li></ul>"),
  ("Follow-ups", '<div class="followup">• How does gRPC handle service discovery?<br>'
    '• What is the N+1 problem in GraphQL and how does DataLoader solve it? (batching + caching)<br>'
    '• How do you version a REST API? (/v1/users vs Accept header versioning)</div>')),

"b002": A(("Rate Limiter Algorithms",
    "<ul><li><b>Token Bucket:</b> Bucket holds max N tokens. Refilled at rate R/sec. Request consumes 1 token. "
    "Allows bursting up to N. Most commonly implemented.</li>"
    "<li><b>Sliding Window Log:</b> Store timestamps of each request. Count within window. Accurate but memory-heavy.</li>"
    "<li><b>Sliding Window Counter:</b> Fix window divided into slots. Weighted count of previous window. Good balance.</li>"
    "<li><b>Fixed Window:</b> Simple counter per window. Burst possible at window boundary.</li></ul>"),
  ("Distributed Implementation",
    "<pre># Redis atomic Lua script — token bucket\nlocal tokens = tonumber(redis.call('GET', KEYS[1]) or ARGV[1])\nif tokens &gt; 0 then\n    redis.call('DECR', KEYS[1])\n    return 1  -- allowed\nend\nreturn 0  -- rate limited</pre>"),
  ("Response Headers",
    "<code>X-RateLimit-Limit: 100</code>, <code>X-RateLimit-Remaining: 45</code>, <code>Retry-After: 3600</code>"),
  ("Follow-ups", '<div class="followup">• How do you implement per-user AND per-endpoint limits simultaneously?<br>'
    '• How does Stripe implement rate limiting? (per API key, per endpoint)<br>'
    '• What is cell-based rate limiting (GCRA — Generic Cell Rate Algorithm)?</div>')),

"b003": A(("Consistent Hashing",
    "Problem with naive modulo hashing: adding/removing 1 server remaps N/S keys (massive cache miss storm).<br><br>"
    "<b>Ring approach:</b> Hash servers and keys to same circular space (0 to 2^32). "
    "A key is assigned to the first server found clockwise from its hash position."),
  ("Virtual Nodes",
    "Each physical server = 100-200 virtual nodes on the ring → even distribution even with few servers. "
    "Fewer hot spots. When server added/removed: only 1/N keys remapped.<br>"
    "<pre>class ConsistentHash:\n    def __init__(self, replicas=150):\n        self.ring = {}\n        self.sorted_keys = []\n        self.replicas = replicas\n\n    def add_server(self, server):\n        for i in range(self.replicas):\n            key = hash(f'{server}:{i}')\n            self.ring[key] = server\n        self.sorted_keys = sorted(self.ring)\n\n    def get_server(self, item):\n        h = hash(item)\n        for k in self.sorted_keys:\n            if h &lt;= k: return self.ring[k]\n        return self.ring[self.sorted_keys[0]]  # wrap around</pre>"),
  ("Follow-ups", '<div class="followup">• How does Amazon DynamoDB use consistent hashing?<br>'
    '• What is the difference between consistent hashing and rendezvous hashing?<br>'
    '• How does virtual node count affect distribution quality?</div>')),

"b004": A(("Circuit Breaker States",
    "<ul><li><b>CLOSED:</b> Normal operation. Failure counter tracks errors. If failures &gt; threshold → OPEN.</li>"
    "<li><b>OPEN:</b> All calls fail immediately (fail-fast). No downstream load. After timeout → HALF_OPEN.</li>"
    "<li><b>HALF_OPEN:</b> Allow one probe request. If succeeds → CLOSED. If fails → OPEN again.</li></ul>"),
  ("Why it matters",
    "Without circuit breaker: one slow service causes thread pool exhaustion in caller → cascading failure across the system. "
    "Circuit breaker prevents this by failing fast and giving downstream service recovery time."),
  ("Libraries", "<ul><li>Resilience4j (Java): sliding window (count/time based), bulkhead pattern</li>"
    "<li>Hystrix (deprecated): used at Netflix, pioneered the pattern</li>"
    "<li>Go: sony/gobreaker, mercadolibre/go-breakers</li></ul>"),
  ("Follow-ups", '<div class="followup">• What is the bulkhead pattern and how does it complement circuit breaker?<br>'
    '• How do you set the right failure threshold to avoid flapping?<br>'
    '• What is the difference between circuit breaker and retry with exponential backoff?</div>')),

"b005": A(("Kafka Architecture",
    "<ul><li><b>Topic:</b> Named category. Divided into <b>partitions</b> (immutable ordered log).</li>"
    "<li><b>Producer:</b> Writes to partition (by key hash or round-robin). Acks: 0/1/all.</li>"
    "<li><b>Consumer Group:</b> Each partition consumed by exactly 1 consumer in group. Multiple groups = independent reads.</li>"
    "<li><b>Broker:</b> Stores partition log. Replication: 1 leader + N-1 followers. ISR = in-sync replicas.</li>"
    "<li><b>ZooKeeper / KRaft:</b> Cluster metadata, leader election (KRaft = ZK-free since Kafka 3.x).</li></ul>"),
  ("Internals",
    "<ul><li>Messages appended to segment files. Retention by time or size.</li>"
    "<li>Consumer tracks offset in <code>__consumer_offsets</code> topic.</li>"
    "<li>Exactly-once: idempotent producer + transactional API.</li>"
    "<li>Page cache: Kafka relies on OS page cache for near-disk-speed throughput.</li></ul>"),
  ("Follow-ups", '<div class="followup">• What is the difference between at-least-once and exactly-once in Kafka?<br>'
    '• How does Kafka achieve 1M+ messages/second? (sequential disk I/O, zero-copy sendfile(), batching)<br>'
    '• What is consumer group rebalancing and how does it cause pauses?</div>')),

"b006": A(("Monolith vs Microservices Trade-offs",
    "<ul><li><b>Monolith pros:</b> Simple deployment, no network latency for inter-module calls, easier debugging, "
    "one codebase, great for small teams and early stage.</li>"
    "<li><b>Monolith cons:</b> Hard to scale individual components, tech lock-in, long build/deploy cycles, "
    "large blast radius on failure.</li>"
    "<li><b>Microservices pros:</b> Independent scale/deploy per service, tech diversity, fault isolation, "
    "team autonomy (Conway's Law).</li>"
    "<li><b>Microservices cons:</b> Distributed system complexity (network failures, eventual consistency), "
    "service discovery, distributed tracing, operational overhead (K8s, service mesh).</li></ul>"),
  ("When to migrate", "Only when: you have scaling problems a monolith can't solve, team is large enough "
    "(2-pizza rule), you have operational maturity (CI/CD, observability). "
    "Don't start with microservices (Martin Fowler: 'don't start with a microservices architecture')."),
  ("Follow-ups", '<div class="followup">• What is a strangler fig pattern for migrating monolith to microservices?<br>'
    '• What is a modular monolith and when is it better than microservices?<br>'
    '• How do you handle data ownership between microservices? (one DB per service)</div>')),

"b008": A(("2PC — Two-Phase Commit",
    "<b>Phase 1 (Prepare):</b> Coordinator sends PREPARE to all participants. Each votes YES (prepared, locked) or NO.<br>"
    "<b>Phase 2 (Commit/Abort):</b> If all YES → send COMMIT; if any NO → send ABORT.<br>"
    "<b>Problems:</b> Coordinator failure in phase 2 → participants stuck holding locks. Blocking protocol. "
    "Network partition → split brain possible."),
  ("Saga Pattern",
    "<b>Choreography:</b> Each service publishes event → next service reacts. No central coordinator. "
    "Decoupled but hard to trace.<br>"
    "<b>Orchestration:</b> Saga Orchestrator sends commands to each service, receives replies. "
    "Easier to manage state.<br>"
    "<b>Compensating transactions:</b> On failure, execute rollback steps in reverse order."),
  ("Example: E-commerce order",
    "<pre>1. Reserve inventory → 2. Debit payment → 3. Assign delivery → 4. Confirm order\nFailure at step 3: Release payment (compensate) → Release inventory (compensate)</pre>"),
  ("Follow-ups", '<div class="followup">• What is the ACID vs BASE trade-off in distributed transactions?<br>'
    '• How does the Outbox Pattern ensure reliable event publishing with Saga?<br>'
    '• What is TCC (Try-Confirm-Cancel) pattern?</div>')),

"b009": A(("Idempotency",
    "An operation is <b>idempotent</b> if performing it multiple times has the same effect as performing it once. "
    "Critical for retry logic in distributed systems (network timeouts, retries)."),
  ("Implementation",
    "<pre># Client sends unique idempotency key\nPOST /payments\nIdempotency-Key: client-generated-uuid-v4\n{\n  \"amount\": 1000,\n  \"currency\": \"INR\"\n}\n\n# Server:\nINSERT INTO payments (idempotency_key, status, result)\nVALUES ('uuid', 'PROCESSING', NULL)\nON CONFLICT (idempotency_key) DO NOTHING\nRETURNING *;\n\n# If conflict → return stored result (same response for same key)</pre>"),
  ("HTTP Methods", "<ul><li><b>Idempotent by nature:</b> GET, PUT, DELETE, HEAD, OPTIONS</li>"
    "<li><b>NOT idempotent:</b> POST (each call creates new resource)</li>"
    "<li>Make POST idempotent with idempotency key header</li></ul>"),
  ("Follow-ups", '<div class="followup">• How long should an idempotency key be stored? (request TTL + processing time + buffer)<br>'
    '• How does Stripe implement idempotency? (48-hour window, stripe-idempotency-key header)<br>'
    '• What is the exactly-once message processing guarantee in Kafka?</div>')),

"b012": A(("Strong Consistency",
    "All nodes see the same data at the same time. After a write completes, all reads return the new value. "
    "Requires synchronous replication. Used in: financial systems, leader election (etcd, ZooKeeper)."),
  ("Eventual Consistency",
    "Given no new updates, all replicas will eventually converge. Reads may return stale data temporarily. "
    "Higher availability and partition tolerance. Used in: DNS, S3, DynamoDB (default), Cassandra."),
  ("CAP Theorem",
    "In presence of network Partition, choose Consistency OR Availability:<br>"
    "<ul><li><b>CP:</b> HBase, MongoDB (primary), etcd, ZooKeeper — prefer consistency over availability</li>"
    "<li><b>AP:</b> Cassandra, DynamoDB, CouchDB — prefer availability over consistency</li>"
    "<li>CA systems only work without partitions (single node databases)</li></ul>"),
  ("PACELC", "Extension of CAP: Even without partitions, trade-off exists between Latency and Consistency."),
  ("Follow-ups", '<div class="followup">• What is monotonic read consistency and how do you achieve it in a distributed system?<br>'
    '• How does DynamoDB implement strong consistency? (quorum reads with ConsistentRead=true)<br>'
    '• What is linearizability vs serializability?</div>')),

"b013": A(("Distributed Locks",
    "<b>Requirements:</b> Mutual exclusion, no deadlock, fault tolerance, lock expiry."),
  ("Redis SET NX EX (simple)",
    "<pre>SET resource_key unique_token NX EX 30  # NX: only if not exists, EX: expire 30s\n# Release: Lua script to check token before delete (atomic)\nif redis.call('GET', key) == token then\n    redis.call('DEL', key)\nend</pre>"),
  ("Redlock (HA Redis)",
    "Acquire lock on N/2+1 independent Redis nodes. If majority acquired within validity time → lock granted. "
    "Release on all nodes. Controversial: Martin Kleppmann argues it's unsafe with clock drift."),
  ("ZooKeeper Ephemeral Nodes",
    "Create sequential ephemeral node. Lock acquired if lowest sequence number. "
    "On disconnect: ZK auto-deletes ephemeral node → no zombie locks. More reliable than Redis."),
  ("Fencing Tokens",
    "Lock returns a monotonically increasing token. Storage layer rejects requests with stale token. "
    "Prevents GC pauses or clock drift from causing split-brain."),
  ("Follow-ups", '<div class="followup">• Why does Redlock fail under process pauses? (Martin Kleppmann paper)<br>'
    '• What is the difference between pessimistic and optimistic locking?<br>'
    '• How does etcd implement distributed locks? (lease + watch)</div>')),

"b015": A(("CQRS — Command Query Responsibility Segregation",
    "Separate <b>write model</b> (commands: create, update, delete) from <b>read model</b> (queries: optimized for reads). "
    "Read model can be denormalized, use different database (e.g., Elasticsearch for search, Redis for fast reads). "
    "Scales independently."),
  ("Event Sourcing",
    "State is derived from a <b>sequence of immutable events</b>, not current state snapshot. "
    "Events are appended to an event store (log). State reconstructed by replaying events.<br>"
    "<pre>Events: OrderPlaced → ItemAdded → PaymentProcessed → OrderShipped\nCurrent state: replay all events → Order{status=SHIPPED, items=[...], payment=PAID}</pre>"),
  ("Benefits and Costs",
    "<ul><li><b>Benefits:</b> Full audit log, time travel (replay to any point), event-driven integration</li>"
    "<li><b>Costs:</b> Eventual consistency between command and query model, complex querying, "
    "schema evolution of events, snapshot needed for long histories</li></ul>"),
  ("Follow-ups", '<div class="followup">• How do you handle schema evolution of events in Event Sourcing?<br>'
    '• What is a projection in Event Sourcing?<br>'
    '• What is the Outbox Pattern and how does it prevent dual-write problems?</div>')),

"b017": A(("Deployment Strategies",
    "<ul><li><b>Blue-Green:</b> Two identical environments. New version deployed to 'green'. "
    "Switch traffic instantly. Easy rollback: flip back to 'blue'. Requires 2x infrastructure.</li>"
    "<li><b>Canary:</b> Route small % of traffic (1-5%) to new version. Monitor error rates / latency. "
    "Gradually increase if healthy. Slow, but minimizes blast radius.</li>"
    "<li><b>Rolling:</b> Replace instances one at a time (or in batches). Both versions run simultaneously. "
    "No extra infrastructure. Standard Kubernetes Deployment behavior.</li>"
    "<li><b>Feature Flags:</b> Deploy code disabled; enable per-user/segment at runtime. "
    "Decouple deploy from release.</li></ul>"),
  ("In Kubernetes",
    "<pre># Canary with Argo Rollouts:\napiVersion: argoproj.io/v1alpha1\nkind: Rollout\nspec:\n  strategy:\n    canary:\n      steps:\n      - setWeight: 5    # 5% traffic to new\n      - pause: {duration: 10m}\n      - setWeight: 50\n      - pause: {duration: 10m}\n      - setWeight: 100</pre>"),
  ("Follow-ups", '<div class="followup">• How do you implement A/B testing alongside a canary deployment?<br>'
    '• How does shadow deployment (dark launch) work?<br>'
    '• What metrics determine if a canary should be promoted vs rolled back?</div>')),
}
