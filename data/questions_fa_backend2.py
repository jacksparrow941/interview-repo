"""Full answers for sysdesign, db, os, networking, concurrency from questions_other.py."""

def A(*s):
    parts = [f'<span class="answer-label">{l}</span><br>{c}' for l,c in s]
    return '<div class="answer-section">'+'</div><div class="answer-section" style="margin-top:10px">'.join(parts)+'</div>'

FULL_ANSWERS_BACKEND2 = {

# ===== SYSTEM DESIGN (sd001-sd015) =====

"sd005": A(("Architecture",
    "<pre>Client → API Gateway → Notification Service\n                              ↓\n                      User Preferences → filter by opt-in/out\n                              ↓\n                      Kafka Topics (push / email / sms)\n                              ↓\n                      Workers → FCM(Android) / APNs(iOS) / SES / Twilio</pre>"),
  ("Reliability Patterns",
    "<ul><li><b>Idempotency:</b> notification_id deduplicates retries</li>"
    "<li><b>Dead Letter Queue:</b> permanently failed → DLQ → alert + manual review</li>"
    "<li><b>Exponential backoff:</b> retry after 1s, 2s, 4s, 8s, 16s</li>"
    "<li><b>Rate limiting:</b> max 5 SMS / 10 push per user per hour</li>"
    "<li><b>Priority queues:</b> transactional (OTP) &gt; activity &gt; marketing</li></ul>"),
  ("Follow-ups",'<div class="followup">• How do you implement quiet hours (no marketing notifications at night)?<br>'
    '• How do you track notification open rates?<br>'
    '• How do you handle failed FCM tokens? (device changed, app uninstalled)</div>')),

"sd009": A(("Uber-like Ride Sharing Design",
    "<pre>Driver App → Location Service (WebSocket) → Location DB (Redis GeoHash)\n                    ↓ every 5s\n               Geospatial Index (H3 hexagons)\n\nRider App → Trip Request → Matching Service\n                               ↓\n                    Query nearby drivers (H3 ring search)\n                               ↓\n                    ETA estimation (ML model on road graph)\n                               ↓\n                    Offer to best driver → accept/reject\n                               ↓ \n                    Trip State Machine (via Kafka + Trip Service)</pre>"),
  ("Geospatial Indexing",
    "<ul><li>H3 (Uber's hexagonal grid): each driver hashed to H3 cell. Ring search expands rings until N drivers found.</li>"
    "<li>Redis GEOADD / GEORADIUS for simple cases</li>"
    "<li>Quadtree: divide space into quads, query bounding box</li></ul>"),
  ("Surge Pricing",
    "Real-time supply/demand ratio per H3 cell. Demand &gt; Supply × threshold → surge multiplier. "
    "Event-driven: Kafka → surge calculator → price service → show to rider before booking."),
  ("Follow-ups",'<div class="followup">• How do you handle driver location updates at scale? (100K drivers, 5s updates = 20K writes/sec)<br>'
    '• How does Uber match multiple riders for pool rides?<br>'
    '• How do you estimate ETA accurately? (historical + real-time road graph)</div>')),

"sd013": A(("Snowflake ID — 64-bit Layout",
    "<pre>0 | 41 bits timestamp (ms) | 10 bits worker ID | 12 bits sequence\n↑ unused                    ↑ datacenter(5)+machine(5)\n\nTimestamp: ms since custom epoch (e.g., Jan 1 2015)\nWorker ID: unique per service instance (assigned from ZK or env var)\nSequence:  0-4095 per millisecond per worker; resets each ms</pre>"),
  ("Clock Skew Handling",
    "<pre>if currentTime &lt; lastTimestamp:\n    # clock moved backwards!\n    wait until currentTime >= lastTimestamp  # wait up to a few ms\n    # OR: raise error and fail fast\n    # OR: use sequence from future slots of last timestamp</pre>"),
  ("Monotonicity", "IDs are roughly time-sortable (within clock skew tolerance). No sort needed for recent data. "
    "Avoids random B-tree page writes = better index write performance."),
  ("Follow-ups",'<div class="followup">• What is the maximum QPS per worker? (4096/ms = ~4M/s per machine)<br>'
    '• How does Twitter Snowflake differ from Instagram ID generation?<br>'
    '• How do you handle the epoch overflow in 2079?</div>')),

# ===== DATABASE (db001-db010) =====

"db004": A(("CAP Theorem",
    "In a distributed system under network <b>Partition</b>: choose Consistency OR Availability.<br>"
    "<ul><li><b>CP systems:</b> Refuse to respond if cannot guarantee consistency. "
    "etcd, ZooKeeper, HBase, MongoDB (primary read). Good for: leader election, config stores.</li>"
    "<li><b>AP systems:</b> Respond with potentially stale data. "
    "Cassandra, CouchDB, DynamoDB (default), Riak. Good for: user profiles, social feeds.</li></ul>"),
  ("PACELC Extension",
    "Even without partition: latency vs consistency trade-off.<br>"
    "Cassandra: HIGH availability + LOW latency but eventual consistency.<br>"
    "Spanner: HIGH consistency but HIGHER latency (TrueTime atomic clocks, Paxos)."),
  ("Follow-ups",'<div class="followup">• Why can\'t we have all 3 of CAP?<br>'
    '• How does DynamoDB implement strong consistency? (quorum reads)<br>'
    '• What is linearizability vs sequential consistency?</div>')),

"db005": A(("Sharding Strategies",
    "<ul><li><b>Range-based:</b> Shard by range (A-G, H-P, Q-Z). Simple routing. Risk: hot spots on recent data (time-based IDs all go to last shard).</li>"
    "<li><b>Hash-based:</b> shard = hash(key) % N. Even distribution. No range queries across shards. Resharding = move all data.</li>"
    "<li><b>Consistent Hashing:</b> Virtual nodes on ring. Minimal data movement on resharding. Used by Cassandra, DynamoDB.</li>"
    "<li><b>Directory-based:</b> Lookup table maps key → shard. Flexible but single point of failure.</li></ul>"),
  ("Cross-Shard Challenges",
    "<ul><li>Joins: must scatter-gather or denormalize</li>"
    "<li>Transactions: 2PC expensive; use Saga instead</li>"
    "<li>Global aggregations: fan out to all shards, merge in application</li>"
    "<li>Hot key: add random suffix to key, fan out writes, merge reads</li></ul>"),
  ("Follow-ups",'<div class="followup">• How does Instagram shard their Cassandra cluster?<br>'
    '• What is the difference between horizontal and vertical partitioning?<br>'
    '• How do you rebalance shards with zero downtime?</div>')),

"db007": A(("PostgreSQL MVCC Internals",
    "Each row version has <b>xmin</b> (created by txn) and <b>xmax</b> (deleted by txn, 0 if alive).<br>"
    "A txn sees a row if: <code>xmin committed AND xmin &lt;= txn_snapshot AND (xmax=0 OR xmax &gt; txn_snapshot OR xmax not committed)</code>"),
  ("How it enables isolation",
    "<ul><li>Readers never block writers (different row versions)</li>"
    "<li>Writers never block readers</li>"
    "<li>REPEATABLE READ: txn gets a snapshot at start, sees consistent view throughout</li>"
    "<li>No shared read locks needed — eliminates reader-writer contention</li></ul>"),
  ("VACUUM","Dead tuples (old xmax'd versions) accumulate. VACUUM marks them as free space. "
    "AUTOVACUUM: background process. Bloat: table grows with dead tuples. "
    "VACUUM ANALYZE: also updates planner statistics."),
  ("Follow-ups",'<div class="followup">• What is table bloat and how does pg_repack help?<br>'
    '• How does VACUUM FULL differ from regular VACUUM?<br>'
    '• What is the visibility map and how does it speed up vacuum?</div>')),

"db008": A(("EXPLAIN ANALYZE Output",
    "<pre>EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 42 AND status = 'PENDING';\n\nSeq Scan on orders (cost=0.00..18240.00 rows=1 width=128) (actual time=0.15..234.52 rows=47 loops=1)\n  Filter: ((user_id = 42) AND (status = 'PENDING'::text))\n  Rows Removed by Filter: 1200000\nPlanning Time: 0.3ms\nExecution Time: 234.6ms\n\n-- FIX: create composite index\nCREATE INDEX idx_orders_user_status ON orders(user_id, status);\n\nIndex Scan using idx_orders_user_status on orders (cost=0.43..8.45 rows=47 width=128)\n  (actual time=0.05..0.12 rows=47 loops=1)\nExecution Time: 0.2ms  -- 1000x faster!</pre>"),
  ("Join Algorithms",
    "<ul><li><b>Nested Loop:</b> For small outer table + indexed inner. O(n*log m)</li>"
    "<li><b>Hash Join:</b> Build hash table on smaller relation. O(n+m). Default for large joins.</li>"
    "<li><b>Merge Join:</b> Requires sorted inputs. O(n+m). Fast for already-sorted data.</li></ul>"),
  ("Follow-ups",'<div class="followup">• What does a Bitmap Heap Scan mean in EXPLAIN output?<br>'
    '• How do you force an index when the planner chooses a seq scan? (SET enable_seqscan=off — for testing only)<br>'
    '• What is the difference between EXPLAIN and EXPLAIN ANALYZE?</div>')),

# ===== OS (os001-os008) =====

"os004": A(("Coffman Conditions for Deadlock",
    "ALL 4 must hold simultaneously for deadlock:<br>"
    "<ul><li><b>Mutual Exclusion:</b> Resource can only be held by one process</li>"
    "<li><b>Hold and Wait:</b> Process holds resources while waiting for more</li>"
    "<li><b>No Preemption:</b> Resources can't be forcibly taken away</li>"
    "<li><b>Circular Wait:</b> Chain of processes each waiting for next in chain</li></ul>"),
  ("Prevention Strategies",
    "<ul><li>Break <b>Hold and Wait</b>: request all resources at once (but reduces concurrency)</li>"
    "<li>Break <b>Circular Wait</b>: impose total ordering on lock acquisition (always lock A before B)</li>"
    "<li>Allow <b>Preemption</b>: rollback and retry (used in databases)</li>"
    "<li><b>Detection + Recovery:</b> build wait-for graph, detect cycles, kill one process</li></ul>"),
  ("Banker's Algorithm","Safe state check: simulate allocation, see if all processes can eventually complete. "
    "Grant request only if system remains in safe state. O(n²×m) too slow for real OS but used in theory."),
  ("Follow-ups",'<div class="followup">• How does MySQL InnoDB detect deadlocks? (wait-for graph, automatic rollback of youngest txn)<br>'
    '• What is the difference between deadlock avoidance and deadlock prevention?<br>'
    '• What is a safe state in the Banker\'s Algorithm?</div>')),

"os005": A(("Synchronization Primitives",
    "<ul><li><b>Mutex (Mutual Exclusion):</b> Binary lock. Owner must release. "
    "Sleeping lock — blocked thread sleeps, woken by OS. Priority inversion risk.</li>"
    "<li><b>Semaphore:</b> Counter (0..N). Binary semaphore ≈ mutex but no ownership. "
    "Counting semaphore for resource pools (N available resources).</li>"
    "<li><b>Spinlock:</b> Busy-wait loop checking flag. No context switch. "
    "Great for very short critical sections (kernel code). Wastes CPU if held long.</li>"
    "<li><b>Condition Variable:</b> Wait + signal pattern. Used WITH mutex (monitor). "
    "Always use predicate loop (spurious wakeups).</li></ul>"),
  ("Futex (Linux)",
    "Fast Userspace muTEX. Fast path: atomic CAS in userspace (no syscall). "
    "Slow path (contended): syscall to sleep. Basis for pthreads mutex and Java's synchronized."),
  ("Follow-ups",'<div class="followup">• What is priority inversion and how does Mars Pathfinder demonstrate it?<br>'
    '• What is a recursive mutex and when do you need it?<br>'
    '• How does Go sync.Mutex use futex internally?</div>')),

"os008": A(("Copy-on-Write — How it works",
    "On <code>fork()</code>, parent and child share the same physical pages. Pages are marked read-only. "
    "On first write by either process → page fault → kernel copies the page → each gets their own copy. "
    "Non-written pages are shared forever."),
  ("Benefits",
    "<ul><li>fork() is extremely fast (O(1) instead of O(n) for copying all pages)</li>"
    "<li>Shell: fork() then exec() — exec replaces address space, no copy needed at all</li>"
    "<li>Redis BGSAVE: fork to get a consistent snapshot. CoW means writes during save only copy modified pages</li>"
    "<li>Kubernetes container image layers: read-only base + CoW overlay for each container</li></ul>"),
  ("Follow-ups",'<div class="followup">• What is the overhead of CoW when writes are frequent? (many page faults + copies)<br>'
    '• How does Python multiprocessing leverage CoW? (shared parent memory until mutation)<br>'
    '• What is ZRAM and how does it compress swap using CoW?</div>')),

# ===== NETWORKING (n001-n008) =====

"n001": A(("TCP vs UDP",
    "<ul><li><b>TCP:</b> Connection-oriented (3-way handshake). Reliable (ACKs, retransmit). Ordered. "
    "Flow + congestion control. ~20-60byte headers. Higher latency.</li>"
    "<li><b>UDP:</b> Connectionless. No guarantees. No ordering. No congestion control. "
    "~8byte header. Lower latency. Can multicast.</li></ul>"),
  ("When to use UDP",
    "<ul><li><b>Gaming / VoIP / video calls:</b> stale data worse than loss. TCP retransmit would cause jitter.</li>"
    "<li><b>DNS:</b> single request-response, small payload. Retry at app layer if timeout.</li>"
    "<li><b>DHCP, TFTP, SNMP:</b> simple protocols where TCP overhead isn't worth it.</li>"
    "<li><b>HTTP/3 (QUIC):</b> UDP + built-in reliability at QUIC layer — gets benefits of both.</li></ul>"),
  ("Follow-ups",'<div class="followup">• What is QUIC and why does it use UDP?<br>'
    '• How do game engines handle packet loss with UDP? (delta compression, interpolation)<br>'
    '• What is the difference between TCP TIME_WAIT and CLOSE_WAIT?</div>')),

"n002": A(("TCP Handshake",
    "<pre>Client          Server\n  |---SYN(seq=x)----&gt;|  Client: CLOSED→SYN_SENT\n  |&lt;--SYN-ACK(seq=y,ack=x+1)---|\n  |---ACK(ack=y+1)--&gt;|  Both: ESTABLISHED\n\nTeardown (4-way):\n  |---FIN-----------&gt;|  Client: ESTABLISHED→FIN_WAIT_1\n  |&lt;--ACK-----------|\n  |&lt;--FIN-----------|\n  |---ACK-----------&gt;|  Client: TIME_WAIT (2×MSL = 60-120s)\n                       Server: CLOSED</pre>"),
  ("TIME_WAIT purpose",
    "Ensures delayed packets from old connection don't confuse new connection on same 4-tuple. "
    "2×MSL (Maximum Segment Lifetime). Can cause port exhaustion on high-traffic servers. "
    "Fix: SO_REUSEADDR, SO_REUSEPORT, or increase local port range."),
  ("SYN Flood", "Attacker sends many SYN packets, never completes handshake. "
    "Server holds half-open connections (SYN_RCVD state). "
    "Defense: SYN cookies — encode state in ISN, allocate resources only after ACK."),
  ("Follow-ups",'<div class="followup">• Why is teardown 4-way but handshake is 3-way?<br>'
    '• What is TCP Fast Open (TFO) and how does it reduce latency?<br>'
    '• What is the maximum number of connections per IP:port pair?</div>')),

"n005": A(("DNS Resolution Chain",
    "<pre>Browser → Check browser cache (TTL)\n       → Check OS resolver cache (/etc/hosts, nscd)\n       → Recursive Resolver (ISP or 8.8.8.8)\n             → Root Name Server (.) → returns TLD server\n             → TLD Server (.com) → returns authoritative NS\n             → Authoritative NS (ns1.example.com) → returns IP\n       → Cache at each level with TTL\n       → Return IP to browser</pre>"),
  ("Record Types",
    "<ul><li><b>A:</b> hostname → IPv4</li>"
    "<li><b>AAAA:</b> hostname → IPv6</li>"
    "<li><b>CNAME:</b> alias → canonical name (CDN, subdomains)</li>"
    "<li><b>MX:</b> mail exchange server</li>"
    "<li><b>TXT:</b> arbitrary text (SPF, DKIM, DMARC, domain verification)</li>"
    "<li><b>NS:</b> name server for domain</li>"
    "<li><b>SOA:</b> Start of Authority (zone info, serial number)</li></ul>"),
  ("Follow-ups",'<div class="followup">• What is DNS propagation delay and how does TTL control it?<br>'
    '• How does DNS-based load balancing work? (round-robin A records)<br>'
    '• What is DNSSEC and what attack does it prevent? (cache poisoning)</div>')),

"n007": A(("CDN Architecture",
    "<ul><li><b>Edge PoPs (Points of Presence):</b> Hundreds of locations near users</li>"
    "<li><b>Anycast routing:</b> Same IP announced from multiple locations, BGP routes to nearest</li>"
    "<li><b>Cache hierarchy:</b> Edge → Regional → Origin</li></ul>"),
  ("Cache Invalidation",
    "<ul><li><b>TTL-based:</b> Simple. Stale content during TTL window.</li>"
    "<li><b>Purge API:</b> CloudFront invalidation, Fastly instant purge. On deploy.</li>"
    "<li><b>Versioned URLs:</b> /static/app.v5.js — never expires. Best for static assets.</li>"
    "<li><b>Cache-Control:</b> <code>max-age=31536000, immutable</code> for fingerprinted assets</li></ul>"),
  ("Pull vs Push CDN",
    "<ul><li><b>Pull:</b> CDN fetches from origin on first request (cache miss). Simple. Good for dynamic content.</li>"
    "<li><b>Push:</b> You upload content to CDN proactively. Good for large files, predictable access patterns.</li></ul>"),
  ("Follow-ups",'<div class="followup">• How does Cloudflare Workers extend CDN to edge compute?<br>'
    '• How do you handle geo-restricted content on CDN?<br>'
    '• What is the difference between Anycast and unicast routing?</div>')),

# ===== CONCURRENCY (conc001-conc010) =====

"conc001": A(("Race Condition",
    "Two or more threads access shared mutable state without synchronization. "
    "Result depends on thread scheduling (timing). Non-deterministic bugs."),
  ("Examples and Fixes",
    "<pre># Python — unsafe counter (GIL helps here but not in C/Java)\ncounter = 0\ndef increment():\n    global counter\n    counter += 1  # NOT atomic in Java/C: read, add, write — 3 ops\n\n# Java fix:\nAtomicInteger counter = new AtomicInteger(0);\ncounter.incrementAndGet();  // single atomic CAS instruction\n\n# OR use synchronized:\nsynchronized void increment() { counter++; }\n\n# Go: use atomic\nvar counter int64\natomic.AddInt64(&amp;counter, 1)\n# OR: go run -race ./...  (built-in race detector)</pre>"),
  ("Detection","Go: <code>go run -race</code>. Java: ThreadSanitizer (TSAN) in native, FindBugs for JVM. "
    "Helgrind (Valgrind) for C/C++."),
  ("Follow-ups",'<div class="followup">• What is a benign data race and when is it acceptable?<br>'
    '• How does the Go race detector work? (shadow memory — 4 words per memory location tracking last 4 accesses)<br>'
    '• What is the difference between a race condition and a data race?</div>')),

"conc005": A(("ABA Problem",
    "Thread 1 reads value A. Thread 2 changes A→B→A. Thread 1 does CAS: sees A, thinks nothing changed — succeeds. "
    "But the state HAS changed (e.g., a node was removed and re-inserted in a lock-free list)."),
  ("Solution — Tagged Pointers",
    "<pre>// 64-bit pointer: high bits = ABA counter (version)\nstruct TaggedPointer {\n    Node* ptr;\n    uint64_t tag;  // monotonically increasing\n};\n\n// CAS on BOTH ptr and tag:\nexpected = { nodeA, 5 };\nif (CAS(&amp;head, expected, { nodeB, 6 })) { /* won */ }\n// Even if ptr went A→B→A, tag goes 5→6→7 — never same tagged value</pre>"),
  ("Alternative: Hazard Pointers","Before accessing a node, register its pointer in per-thread hazard pointer array. "
    "Reclaimer checks all hazard pointers before freeing memory. Used in folly::ConcurrentLinkedList."),
  ("Follow-ups",'<div class="followup">• What is the IBM S/390 double-word CAS and how does it enable tagged pointers natively?<br>'
    '• How does Java AtomicStampedReference solve ABA?<br>'
    '• Why is lock-free code harder to reason about than mutex-based code?</div>')),

"conc007": A(("Thread Pool Sizing Formula",
    "<ul><li><b>CPU-bound tasks:</b> N_threads = N_CPU (or N+1 to hide memory stall)</li>"
    "<li><b>I/O-bound tasks:</b> N = N_CPU × (1 + wait_time / service_time)<br>"
    "Example: DB query takes 50ms, processing takes 5ms → ratio = 10 → 10 × N_CPU threads</li>"
    "<li><b>Mixed:</b> Use two pools — CPU pool + IO pool. Don't block CPU pool with IO.</li></ul>"),
  ("Queue Sizing",
    "<ul><li>Bounded queue = backpressure. If queue full → caller blocked or rejected (CallerRunsPolicy).</li>"
    "<li>Unbounded queue (LinkedBlockingQueue): can OOM. Never use in production without monitoring.</li>"
    "<li>Queue length monitoring: if growing → pool too small or tasks too slow → alert.</li></ul>"),
  ("Follow-ups",'<div class="followup">• What is Little\'s Law and how does it apply to thread pool sizing?<br>'
    '• How do virtual threads (Java 21 Loom) change pool sizing strategy? (pool not needed — 1 VT per request)<br>'
    '• How do you detect thread pool exhaustion in production?</div>')),

"conc008": A(("Compare-And-Swap (CAS)",
    "Atomic hardware instruction: <code>CAS(addr, expected, new) → bool</code>. "
    "If *addr == expected, atomically set *addr = new and return true. Else return false."),
  ("Lock-free Stack with CAS",
    "<pre>class LockFreeStack&lt;T&gt; {\n    AtomicReference&lt;Node&lt;T&gt;&gt; top = new AtomicReference&lt;&gt;();\n    \n    void push(T val) {\n        Node&lt;T&gt; newNode = new Node&lt;&gt;(val);\n        do {\n            newNode.next = top.get();  // read current top\n        } while (!top.compareAndSet(newNode.next, newNode));  // retry if top changed\n    }\n    \n    T pop() {\n        Node&lt;T&gt; old;\n        do {\n            old = top.get();\n            if (old == null) return null;\n        } while (!top.compareAndSet(old, old.next));\n        return old.val;\n    }\n}</pre>"),
  ("CAS vs Mutex",
    "CAS: no sleep, no context switch, no kernel call. But: retry loop wastes CPU under high contention. "
    "Best for: low contention, short operations. Use mutex for long critical sections."),
  ("Follow-ups",'<div class="followup">• What is the difference between CAS and test-and-set?<br>'
    '• What is CMPXCHG in x86 and LDXR/STXR in ARM?<br>'
    '• What is the CAS-based implementation of a concurrent queue (Michael-Scott queue)?</div>')),
}
