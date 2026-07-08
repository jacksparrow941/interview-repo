"""Performance Engineering & Observability interview questions with full answers."""

_ALL = ["Google","Meta","Amazon","Microsoft","Uber","LinkedIn","Netflix","Databricks","Stripe","Razorpay","CRED","Dream11"]
_G3  = ["Google","Meta","Amazon","Microsoft","Uber","LinkedIn"]

def A(*s):
    parts = [f'<span class="answer-label">{l}</span><br>{c}' for l,c in s]
    return '<div class="answer-section">'+'</div><div class="answer-section" style="margin-top:10px">'.join(parts)+'</div>'

_RAW = [
("perf001","How do you diagnose and fix high API latency?","performance","performance","Hard",
 _ALL, 92, "latency,profiling,p99,flame-graph,bottleneck","System Design Round",
 A(("Systematic Approach",
    "<pre>1. MEASURE: Where is the time going?\n   - Add distributed tracing (Jaeger/Zipkin): see each span's duration\n   - p50/p95/p99 latency (NOT just average — outliers matter)\n   - Breakdown: network + serialization + DB queries + external API + CPU\n\n2. IDENTIFY bottleneck:\n   Common causes:\n   - N+1 queries (add JOIN FETCH or batch)\n   - Missing DB index (check EXPLAIN ANALYZE → seq scan)\n   - Synchronous external API call in critical path (make async / cache)\n   - Lock contention (connection pool exhausted, mutex hotspot)\n   - GC pauses (Java: -XX:+PrintGCDetails, G1/ZGC tuning)\n   - Memory pressure (swap, cache thrashing)\n\n3. FIX:\n   - Caching: Redis in front of slow DB queries\n   - Async: move non-critical work off request path (Kafka)\n   - Parallelism: concurrent DB queries (CompletableFuture/goroutines)\n   - Index: add composite index for slow query\n   - Connection pooling: tune min/max pool size</pre>"),
  ("Key Metrics",
    "<ul><li><b>Latency percentiles:</b> p50=100ms is fine; p99=5s means 1% users wait 5 seconds</li>"
    "<li><b>Throughput:</b> RPS the service can handle without degrading</li>"
    "<li><b>Error rate:</b> 5xx rate as % of total requests</li>"
    "<li><b>Saturation:</b> CPU%, memory%, connection pool utilization, queue depth</li></ul>"),
  ("USE Method",
    "For every resource: <b>Utilization</b> (how busy), <b>Saturation</b> (how much queuing), <b>Errors</b> (error count). "
    "Invented by Brendan Gregg."),
  ("Follow-ups",'<div class="followup">• How do you use flame graphs to identify CPU hotspots?<br>'
    '• What is the difference between tail latency and average latency?<br>'
    '• How do you implement circuit breakers to protect against latency cascades?</div>'))),

("perf002","Explain distributed tracing — how it works","performance","observability","Medium",
 _ALL[:9], 84, "distributed-tracing,opentelemetry,jaeger,zipkin,trace-context","System Design Round",
 A(("How it works",
    "<pre>Request enters Service A → Tracer generates trace_id (128-bit)\nService A calls Service B → propagates trace_id + span_id in HTTP header:\n  traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01\n               version  traceId                    parentSpanId   flags\n\nEach service creates a span:\n  span = {traceId, spanId, parentSpanId, name, startTime, duration,\n          tags: {\"db.type\":\"postgresql\", \"http.status\":200},\n          logs: [{\"event\":\"query\", \"sql\":\"...\"}]}\n\nSpans sent async to collector (Jaeger/Zipkin) → assembled into trace tree</pre>"),
  ("OpenTelemetry (OTel)",
    "<ul><li>Vendor-neutral standard for traces, metrics, logs</li>"
    "<li>SDK instruments your code (auto-instrumentation for popular frameworks)</li>"
    "<li>Exporter sends to Jaeger, Zipkin, Tempo, AWS X-Ray, Datadog</li>"
    "<li><code>OTEL_TRACES_EXPORTER=jaeger OTEL_EXPORTER_JAEGER_ENDPOINT=http://jaeger:14268/api/traces</code></li></ul>"),
  ("Sampling",
    "<ul><li><b>Head sampling:</b> Decision at trace start (before outcome known). Simple. Loses tail errors.</li>"
    "<li><b>Tail sampling:</b> Buffer traces, decide after seeing all spans. Can keep errored/slow traces.</li>"
    "<li><b>Rate:</b> 1% for healthy services, 100% for errors, 10% for slow (p99 &gt; 1s)</li></ul>"),
  ("Follow-ups",'<div class="followup">• What is the W3C Trace Context specification?<br>'
    '• How does continuous profiling (Pyroscope, Parca) complement distributed tracing?<br>'
    '• How do you correlate traces with logs and metrics? (structured logging with trace_id)</div>'))),

("perf003","Cache strategies — cache-aside, read-through, write-through, write-back","performance","caching","Medium",
 _ALL, 88, "caching,redis,cache-aside,write-through,cache-invalidation","Backend Design",
 A(("Cache Strategies",
    "<ul><li><b>Cache-Aside (Lazy loading):</b> App checks cache first; on miss, reads DB, populates cache. "
    "Cache only stores what's actually requested. Risk: thundering herd on cold start.</li>"
    "<li><b>Read-Through:</b> Cache reads from DB automatically on miss (library handles it). "
    "App always reads from cache. DB not directly accessed by app.</li>"
    "<li><b>Write-Through:</b> Write to cache AND DB synchronously. Cache never stale. "
    "High write latency (must wait for both). Good for read-heavy.</li>"
    "<li><b>Write-Back (Write-Behind):</b> Write to cache, return immediately. Write to DB asynchronously. "
    "Fast writes. Risk: data loss if cache crashes before flush.</li></ul>"),
  ("Cache-Aside Pattern (most common)",
    "<pre>def get_user(user_id):\n    # Try cache first\n    user = redis.get(f\"user:{user_id}\")\n    if user:\n        return deserialize(user)  # cache hit\n    \n    # Cache miss — read from DB\n    user = db.query(\"SELECT * FROM users WHERE id=%s\", user_id)\n    \n    # Populate cache with TTL\n    redis.setex(f\"user:{user_id}\", ttl=3600, value=serialize(user))\n    return user\n\ndef update_user(user_id, data):\n    db.execute(\"UPDATE users SET ... WHERE id=%s\", user_id)\n    redis.delete(f\"user:{user_id}\")  # invalidate — don't update!</pre>"),
  ("Cache Eviction Policies",
    "<ul><li><b>LRU:</b> Evict least recently used. Good general-purpose.</li>"
    "<li><b>LFU:</b> Evict least frequently used. Better for skewed access patterns.</li>"
    "<li><b>TTL:</b> Time-based expiry. Always stale by at most TTL seconds.</li>"
    "<li><b>Allkeys-lru (Redis):</b> Apply LRU across all keys when memory full.</li></ul>"),
  ("Follow-ups",'<div class="followup">• What is the thundering herd problem and how do you prevent it? (mutex/lock on cache miss, staggered TTLs)<br>'
    '• How do you handle cache warming after a cold restart?<br>'
    '• What is probabilistic early expiration (PER) and how does it prevent dogpile?</div>'))),

("perf004","Load testing — how to approach and what tools to use","performance","performance","Medium",
 _ALL[:8], 78, "load-testing,k6,gatling,jmeter,stress-test,sla","System Design Round",
 A(("Test Types",
    "<ul><li><b>Load test:</b> Expected normal + peak load. Validate SLAs. Measure p99 latency, throughput, error rate.</li>"
    "<li><b>Stress test:</b> Push beyond expected load until system breaks. Find breaking point. Test recovery.</li>"
    "<li><b>Soak/endurance test:</b> Normal load for extended time (hours/days). Find memory leaks, connection exhaustion, log rotation issues.</li>"
    "<li><b>Spike test:</b> Sudden large traffic burst. Test autoscaling, circuit breakers.</li>"
    "<li><b>Chaos test:</b> Kill instances, inject latency, corrupt network. Test resilience.</li></ul>"),
  ("k6 Example",
    "<pre>import http from 'k6/http';\nimport { check, sleep } from 'k6';\n\nexport const options = {\n  stages: [\n    { duration: '2m', target: 100 },   // ramp up to 100 VUs\n    { duration: '5m', target: 100 },   // hold at 100 VUs\n    { duration: '2m', target: 0 },     // ramp down\n  ],\n  thresholds: {\n    'http_req_duration': ['p(99)&lt;500'],  // 99% requests &lt; 500ms\n    'http_req_failed': ['rate&lt;0.01'],   // &lt;1% error rate\n  },\n};\n\nexport default function() {\n  const r = http.get('https://api.example.com/users');\n  check(r, { 'status 200': (r) =&gt; r.status === 200 });\n  sleep(1);\n}</pre>"),
  ("What to measure",
    "<ul><li>Throughput: requests/sec at saturation</li>"
    "<li>Latency: p50, p95, p99, p999 as load increases</li>"
    "<li>Error rate: 5xx rate, timeout rate</li>"
    "<li>Resource utilization: CPU, memory, disk I/O, network on each tier</li>"
    "<li>Database: connection pool saturation, query latency at load</li></ul>"),
  ("Follow-ups",'<div class="followup">• How do you load test a WebSocket-based chat system?<br>'
    '• What is the difference between vertical and horizontal scaling in response to load tests?<br>'
    '• How do you profile a Java application under production load? (async-profiler, JFR)</div>'))),

("perf005","Observability — metrics, logs, traces — the three pillars","performance","observability","Medium",
 _ALL[:9], 86, "observability,prometheus,grafana,elk,opentelemetry,slo","System Design Round",
 A(("Three Pillars",
    "<ul><li><b>Metrics:</b> Numeric aggregations over time. Low cardinality. Cheap to store. "
    "Tool: Prometheus (pull-based scraping) + Grafana. Counter, Gauge, Histogram, Summary.</li>"
    "<li><b>Logs:</b> Discrete events with context. High volume. Searchable. "
    "Tool: ELK stack (Elasticsearch+Logstash+Kibana) or Loki+Grafana. "
    "Structured JSON logs with trace_id for correlation.</li>"
    "<li><b>Traces:</b> Request journey across services. Tool: Jaeger, Zipkin, Tempo. "
    "Essential for microservices debugging.</li></ul>"),
  ("SLI / SLO / SLA / Error Budget",
    "<pre>SLI (Service Level Indicator): the metric you measure\n  e.g., \"% of requests with latency &lt; 200ms\"\n\nSLO (Service Level Objective): your internal target\n  e.g., \"99.9% of requests &lt; 200ms over rolling 30 days\"\n\nSLA (Service Level Agreement): contractual with customer\n  e.g., \"99.5% uptime or credit applied\"\n\nError Budget: 1 - SLO = allowed unreliability\n  99.9% SLO = 0.1% error budget = 43.8 min downtime/month\n  If budget exhausted: freeze feature work, focus on reliability</pre>"),
  ("RED Method (for services)",
    "<b>R</b>ate (requests/sec), <b>E</b>rror rate (errors/sec), <b>D</b>uration (latency). "
    "Apply to every microservice for quick health check."),
  ("Follow-ups",'<div class="followup">• How do you implement alerting without alert fatigue? (symptom-based not cause-based alerts)<br>'
    '• What is the difference between blackbox and whitebox monitoring?<br>'
    '• How does OpenTelemetry unify metrics, logs, and traces?</div>'))),

("perf006","How does CPU caching work and why does it matter for performance?","performance","performance","Hard",
 ["Google","Meta","Nvidia","Apple","Databricks","Snowflake","VMware","Cisco"], 74,
 "cpu-cache,cache-line,false-sharing,numa,memory-hierarchy","Coding Round",
 A(("Memory Hierarchy",
    "<pre>L1 cache:  ~32KB per core,   ~1ns  latency\nL2 cache: ~256KB per core,   ~4ns  latency\nL3 cache:   ~8MB shared,     ~40ns latency\nRAM:        ~16-64GB,       ~100ns latency\nSSD NVMe:              ~100μs latency\nHDD:                    ~10ms latency</pre>"),
  ("Cache Lines",
    "Data loaded in 64-byte cache lines. Accessing one byte loads entire 64-byte block. "
    "Sequential access (arrays) → excellent cache utilization. "
    "Random access (linked lists) → cache miss per node."),
  ("False Sharing",
    "<pre># Two threads update different variables in same cache line:\n# Thread 1 updates counter_a, Thread 2 updates counter_b\n# If they're adjacent in memory → same cache line → cache coherence traffic\n# Core 1 invalidates Core 2's cache line on every write → performance degrades!\n\n# Fix: padding\nstruct PaddedCounter {\n    alignas(64) std::atomic&lt;int64_t&gt; value;  // 64-byte aligned\n    char padding[64 - sizeof(std::atomic&lt;int64_t&gt;)];  // fill rest of cache line\n};</pre>"),
  ("Practical Impact",
    "<ul><li>Array of structs vs Struct of arrays (SOA): SOA = better cache usage for column-wise processing</li>"
    "<li>Cache-oblivious algorithms (recursive divide) beat sequential for large matrices</li>"
    "<li>Go: sync.Mutex padded to avoid false sharing with adjacent data</li></ul>"),
  ("Follow-ups",'<div class="followup">• What is NUMA (Non-Uniform Memory Access) and how does it affect multi-socket servers?<br>'
    '• How does prefetching work and how can you hint the CPU to prefetch?<br>'
    '• What is the impact of cache misses on a tight loop processing 100M integers?</div>'))),
]

def _to_dict(q):
    return {"id":q[0],"text":q[1],"category":q[2],"subcategory":q[3],"difficulty":q[4],
            "companies":q[5],"frequency":q[6],"tags":q[7].split(","),"round_type":q[8],"answer_hint":q[9]}

QUESTIONS = [_to_dict(q) for q in _RAW]
