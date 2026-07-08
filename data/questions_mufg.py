"""
MUFG Global Services — Senior Java Fullstack (5 YOE) Interview Questions
Sources: AmbitionBox, LockedIn AI, Glassdoor, LinkedIn JDs.
Topics: Java 8+, Spring Boot, Hibernate/JPA, Kafka/IBM MQ, Angular,
        Microservices, Banking Domain, OpenShift, Security, CI/CD, Behavioral.
"""

_MUFG = ["MUFG Global Services"]

def A(*sections):
    parts = [f'<span class="answer-label">{l}</span><br>{c}' for l,c in sections]
    return '<div class="answer-section">'+'</div><div class="answer-section" style="margin-top:10px">'.join(parts)+'</div>'

MUFG_Q = [

  ("mufg001","HashMap vs ConcurrentHashMap — thread safety and internal differences",
   "java","collections","Medium",_MUFG,95,"hashmap,concurrenthashmap,thread-safety,banking","Technical Round",
   A(("HashMap (Not Thread-Safe)",
      "Array of <code>Node&lt;K,V&gt;</code> buckets. Hash → bucket via <code>(n-1)&amp;hash</code>. "
      "Collisions: linked list → red-black tree at TREEIFY_THRESHOLD=8. Resizes (doubles) at 75% load. "
      "<b>Multi-threaded writes: race on resize, data loss, infinite loop (Java 7).</b>"),
     ("ConcurrentHashMap (Thread-Safe)",
      "Java 8+: CAS + synchronized per bucket (not the whole map). Reads are lock-free (volatile). "
      "No null keys/values (unlike HashMap). Iteration is weakly consistent — no ConcurrentModificationException."),
     ("Code",
      "<pre>Map&lt;String,Integer&gt; cmap = new ConcurrentHashMap&lt;&gt;();\ncmap.put(\"TXN-001\", 5000);\ncmap.putIfAbsent(\"TXN-001\", 3000);         // atomic\ncmap.compute(\"TXN-001\", (k,v)-&gt; v+1);      // atomic increment\n// Banking: CHM used for dedup cache (idempotency key → status)</pre>"),
     ("Key Differences",
      "<ul><li>Null key/val: HashMap ✓, CHM ✗</li>"
      "<li>Locking: none vs per-bucket CAS/sync</li>"
      "<li>size(): exact vs approximate (sumCount)</li>"
      "<li>CHM >> Collections.synchronizedMap() under contention</li></ul>"),
     ("Follow-ups",
      '<div class="followup">• putIfAbsent vs computeIfAbsent — difference?<br>'
      '• Why is CopyOnWriteArrayList useful for rarely-written lists?<br>'
      '• How does CHM handle resize concurrently?</div>'))),

  ("mufg002","How to use a POJO as a key in HashMap — hashCode/equals contract",
   "java","collections","Medium",_MUFG,92,"hashmap,pojo,hashcode,equals,contract","Technical Round",
   A(("The Problem",
      "HashMap uses <code>hashCode()</code> to find the bucket, <code>equals()</code> to match the key. "
      "Without overriding both, default Object identity is used — two logically equal POJOs go to different buckets."),
     ("Contract",
      "<ul><li>If <code>a.equals(b)</code> → <code>a.hashCode()==b.hashCode()</code> (mandatory)</li>"
      "<li>Reverse not required (collision allowed)</li>"
      "<li><b>Never mutate fields used in hashCode while object is a map key</b></li></ul>"),
     ("Correct Implementation",
      "<pre>public final class TradeKey {          // final fields = safe as key\n    private final String tradeId;\n    private final String bookId;\n\n    @Override public boolean equals(Object o) {\n        if (!(o instanceof TradeKey)) return false;\n        TradeKey k = (TradeKey) o;\n        return Objects.equals(tradeId, k.tradeId)\n            &amp;&amp; Objects.equals(bookId, k.bookId);\n    }\n    @Override public int hashCode() {\n        return Objects.hash(tradeId, bookId);\n    }\n}\n// Map.get(new TradeKey(\"TXN-001\",\"BOOK-A\")) — finds the entry correctly</pre>"),
     ("Follow-ups",
      '<div class="followup">• What if hashCode always returns 0? (all keys in one bucket → O(n))<br>'
      '• Can an enum be a safe HashMap key? (yes — identity-based equals + stable hashCode)<br>'
      '• Lombok @Data generates hashCode/equals — pitfall with mutable fields?</div>'))),

  ("mufg003","Multiple primary keys in Hibernate — @IdClass vs @EmbeddedId composite keys",
   "java","jpa","Medium",_MUFG,90,"hibernate,composite-key,idclass,embeddedid,jpa","Technical Round",
   A(("@IdClass Approach",
      "<pre>// PK class — must be Serializable, public no-arg ctor, equals, hashCode\npublic class TradePK implements Serializable {\n    private String tradeId;\n    private String bookId;\n    // no-arg ctor + equals + hashCode\n}\n\n@Entity @IdClass(TradePK.class)\npublic class Trade {\n    @Id private String tradeId;\n    @Id private String bookId;\n    private BigDecimal amount;\n}\n// JPQL: WHERE t.tradeId = :id   (direct field names)</pre>"),
     ("@EmbeddedId Approach",
      "<pre>@Embeddable\npublic class TradePK implements Serializable {\n    private String tradeId;\n    private String bookId;   // + equals, hashCode\n}\n\n@Entity public class Trade {\n    @EmbeddedId private TradePK id;\n    private BigDecimal amount;\n}\n// JPQL: WHERE t.id.tradeId = :id  (nested navigation)</pre>"),
     ("Which to Choose",
      "<ul><li><b>@IdClass:</b> Simpler JPQL, fields at entity level, less OO</li>"
      "<li><b>@EmbeddedId:</b> Better encapsulation, PK as domain object</li>"
      "<li>Both: PK class must be Serializable, have no-arg ctor, equals, hashCode</li></ul>"),
     ("Follow-ups",
      '<div class="followup">• Can you use @GeneratedValue with composite keys? (No — natural keys only)<br>'
      '• How do OneToMany relations work from an entity with @EmbeddedId?<br>'
      '• What is @MapsId?</div>'))),

  ("mufg004","Spring Bean lifecycle — @PostConstruct, @PreDestroy, graceful shutdown",
   "java","spring","Medium",_MUFG,88,"spring,bean-lifecycle,postconstruct,predestroy,graceful-shutdown","Technical Round",
   A(("Lifecycle Steps",
      "<ol><li>Instantiate (constructor)</li><li>Inject dependencies</li>"
      "<li>BeanNameAware / ApplicationContextAware callbacks</li>"
      "<li><b>@PostConstruct</b> — bean is ready</li>"
      "<li>Bean in use</li>"
      "<li>On shutdown: <b>@PreDestroy</b> — cleanup</li></ol>"),
     ("Code",
      "<pre>@Component\npublic class KafkaTradeConsumer {\n    @PostConstruct\n    public void init() {\n        consumer.subscribe(List.of(\"trades.raw\"));\n    }\n\n    @PreDestroy\n    public void shutdown() {\n        accepting = false;           // stop accepting new trades\n        consumer.wakeup();           // unblock poll()\n        consumer.close(Duration.ofSeconds(5));\n    }\n}</pre>"),
     ("Ensuring In-Flight Completion (MUFG question)",
      "Use <code>volatile boolean accepting</code> + <code>AtomicInteger activeTrades</code>. "
      "In <code>@PreDestroy</code>: set accepting=false, wait until activeTrades==0, then close. "
      "<b>Or use Spring's SmartLifecycle</b> interface — <code>stop(Runnable callback)</code> signals "
      "Spring that shutdown can proceed only after in-flight ops finish."),
     ("Follow-ups",
      '<div class="followup">• @PostConstruct vs InitializingBean.afterPropertiesSet() — difference?<br>'
      '• What is BeanPostProcessor?<br>'
      '• Spring Boot server.shutdown=graceful — what does it do?</div>'))),

  ("mufg005","Java 8 Streams, Lambdas, Functional Interfaces — banking use cases",
   "java","java8","Medium",_MUFG,86,"java8,lambda,streams,functional-interface,optional","Technical Round",
   A(("Functional Interfaces",
      "<ul><li><code>Predicate&lt;T&gt;</code> — boolean test(T t) — filtering</li>"
      "<li><code>Function&lt;T,R&gt;</code> — R apply(T t) — transform</li>"
      "<li><code>Consumer&lt;T&gt;</code> — void accept(T t) — side effects</li>"
      "<li><code>Supplier&lt;T&gt;</code> — T get() — lazy supply</li></ul>"),
     ("Banking Stream Examples",
      "<pre>List&lt;Trade&gt; trades = fetchTrades();\n\n// High-value trades\nList&lt;Trade&gt; highValue = trades.stream()\n    .filter(t -&gt; t.getAmount().compareTo(ONE_MILLION) &gt; 0)\n    .collect(Collectors.toList());\n\n// Group by currency\nMap&lt;String,List&lt;Trade&gt;&gt; byCcy = trades.stream()\n    .collect(Collectors.groupingBy(Trade::getCurrency));\n\n// Sum per book\nMap&lt;String,BigDecimal&gt; totals = trades.stream()\n    .collect(Collectors.groupingBy(Trade::getBookId,\n        Collectors.reducing(ZERO, Trade::getAmount, BigDecimal::add)));\n\n// First pending or throw\nTrade p = trades.stream()\n    .filter(t-&gt;\"PENDING\".equals(t.getStatus()))\n    .findFirst().orElseThrow(TradeNotFoundException::new);</pre>"),
     ("Follow-ups",
      '<div class="followup">• map() vs flatMap() — difference?<br>'
      '• How to handle checked exceptions inside a lambda?<br>'
      '• When does parallel stream hurt performance? (small lists, stateful ops)</div>'))),

  ("mufg006","Merge two sorted arrays — coding problem (actually asked at MUFG)",
   "coding","arrays","Easy",_MUFG,82,"arrays,merge,two-pointer,sorted","Coding Test",
   A(("Two-Pointer O(m+n)",
      "<pre>public int[] merge(int[] a, int[] b) {\n    int i=0, j=0, k=0;\n    int[] res = new int[a.length+b.length];\n    while (i&lt;a.length &amp;&amp; j&lt;b.length)\n        res[k++] = a[i]&lt;=b[j] ? a[i++] : b[j++];\n    while (i&lt;a.length) res[k++]=a[i++];\n    while (j&lt;b.length) res[k++]=b[j++];\n    return res;\n}</pre>"),
     ("In-Place (LeetCode 88)",
      "<pre>// nums1 has m elements, then n zeros; nums2 has n elements\npublic void merge(int[] nums1, int m, int[] nums2, int n) {\n    int i=m-1, j=n-1, k=m+n-1;\n    while (i&gt;=0 &amp;&amp; j&gt;=0)\n        nums1[k--] = nums1[i]&gt;nums2[j] ? nums1[i--] : nums2[j--];\n    while (j&gt;=0) nums1[k--]=nums2[j--];\n}</pre>"),
     ("Banking Context","Used in trade reconciliation — merging sorted trade lists from two feeds for match detection."),
     ("Follow-ups",
      '<div class="followup">• Merge K sorted arrays? (min-heap, O(N log K))<br>'
      '• Java Arrays.sort() internals? (dual-pivot quicksort for primitives, Timsort for objects)</div>'))),

  ("mufg007","Microservices patterns for banking — Saga, Circuit Breaker, Strangler Fig",
   "backend","microservices","Hard",_MUFG,85,"saga,circuit-breaker,strangler-fig,resilience4j","System Design Round",
   A(("Saga — Distributed Transactions",
      "At MUFG: Trade → Position → Risk Service. 2PC too slow. Saga uses local txns + compensating actions.<br>"
      "<b>Orchestration:</b> Central TradeOrchestrator calls each service step; on failure triggers rollbacks.<br>"
      "<b>Choreography:</b> Each service emits events; downstream reacts and compensates on failure."),
     ("Circuit Breaker with Resilience4j",
      "<pre>@CircuitBreaker(name=\"riskService\", fallbackMethod=\"cachedRisk\")\npublic RiskResult checkRisk(Trade t) {\n    return riskClient.evaluate(t);\n}\npublic RiskResult cachedRisk(Trade t, Exception e) {\n    return RiskResult.fromCache(t.getBookId());\n}\n\n# application.yml\nresilience4j.circuitbreaker.instances.riskService:\n  slidingWindowSize: 10\n  failureRateThreshold: 50\n  waitDurationInOpenState: 10s</pre>"),
     ("Strangler Fig","Legacy COBOL/Struts systems at MUFG are replaced gradually. "
      "API Gateway routes new features to microservices; old routes stay on legacy. "
      "Over time, all routes are 'strangled' away from legacy."),
     ("Follow-ups",
      '<div class="followup">• Choreography vs Orchestration — when to prefer each?<br>'
      '• How do you implement idempotency in Saga compensating transactions?<br>'
      '• How does Istio replace Resilience4j circuit breaker?</div>'))),

  ("mufg008","Kafka trade booking — consumer groups, idempotency, exactly-once semantics",
   "backend","messaging","Hard",_MUFG,88,"kafka,trade-booking,idempotency,exactly-once,consumer-groups","System Design Round",
   A(("Architecture",
      "<pre>Upstream Systems → Kafka [trades.raw] (partitioned by bookId)\n  → Consumer Group [trade-booker] (instances = partitions)\n  → Idempotency check (trade_id UPSERT on Oracle)\n  → REST API for downstream</pre>"),
     ("Idempotent Consumer",
      "<pre>@KafkaListener(topics=\"trades.raw\", groupId=\"trade-booker\")\n@Transactional\npublic void onTrade(TradeEvent e) {\n    // INSERT ... ON CONFLICT DO NOTHING (PostgreSQL)\n    // or existence check before insert\n    if (!tradeRepo.existsByTradeId(e.getTradeId())) {\n        tradeRepo.save(mapToTrade(e));\n        kafkaTemplate.send(\"trade.booked\", e.getTradeId(), booked);\n    }\n    // Offset committed after DB write (at-least-once delivery)\n}</pre>"),
     ("Exactly-Once (EOS)",
      "<pre>spring.kafka.producer.transaction-id-prefix=booker-\nspring.kafka.consumer.isolation-level=read_committed\n\n@Transactional(\"kafkaTransactionManager\")\npublic void processEOS(ConsumerRecord&lt;String,TradeEvent&gt; r) {\n    tradeRepo.save(mapToTrade(r.value()));\n    kafkaTemplate.send(\"trade.booked\", r.value().getId(), booked);\n    // offset + DB + produce committed atomically\n}</pre>"),
     ("Follow-ups",
      '<div class="followup">• Kafka partition strategy for ordering? (partition by bookId)<br>'
      '• IBM MQ vs Kafka at MUFG? (IBM MQ for SWIFT/legacy; Kafka for internal event bus)<br>'
      '• What is the Outbox pattern and why does MUFG use it?</div>'))),

  ("mufg009","Spring Boot REST API — validation, idempotency, global exception handling",
   "java","spring","Medium",_MUFG,84,"spring-boot,rest,validation,exception-handler,idempotency","Technical Round",
   A(("Controller + Validation",
      "<pre>@RestController @RequestMapping(\"/api/v1/trades\")\npublic class TradeController {\n    @PostMapping\n    public ResponseEntity&lt;TradeDto&gt; book(\n            @RequestBody @Valid BookTradeRequest req,\n            @RequestHeader(\"Idempotency-Key\") String key) {\n        return ResponseEntity.status(201).body(tradeService.book(req, key));\n    }\n    @GetMapping(\"/{id}\")\n    public TradeDto get(@PathVariable @NotBlank String id) {\n        return tradeService.findById(id)\n            .orElseThrow(() -&gt; new TradeNotFoundException(id));\n    }\n}\n\npublic class BookTradeRequest {\n    @NotBlank private String tradeId;\n    @NotNull @DecimalMin(\"0.01\") private BigDecimal amount;\n    @Size(min=3,max=3) private String currency;\n}</pre>"),
     ("Global Exception Handler",
      "<pre>@RestControllerAdvice\npublic class GlobalExHandler {\n    @ExceptionHandler(TradeNotFoundException.class)\n    public ResponseEntity&lt;ErrorResponse&gt; notFound(TradeNotFoundException ex) {\n        return ResponseEntity.status(404)\n            .body(new ErrorResponse(\"TRADE_NOT_FOUND\", ex.getMessage()));\n    }\n    @ExceptionHandler(MethodArgumentNotValidException.class)\n    public ResponseEntity&lt;ErrorResponse&gt; validation(MethodArgumentNotValidException ex) {\n        String msg = ex.getBindingResult().getFieldErrors().stream()\n            .map(e -&gt; e.getField()+\": \"+e.getDefaultMessage())\n            .collect(joining(\", \"));\n        return ResponseEntity.badRequest().body(new ErrorResponse(\"VALIDATION_FAILED\",msg));\n    }\n}</pre>"),
     ("Idempotency Key Pattern",
      "Client sends <code>Idempotency-Key: UUID</code> header. Server stores (key → response) in Redis (TTL 24h). "
      "On retry with same key → return cached response. Prevents double booking."),
     ("Follow-ups",
      '<div class="followup">• REST API versioning strategies? (URL path vs Accept header)<br>'
      '• @RequestBody vs @ModelAttribute?<br>'
      '• Spring Actuator health endpoints for K8s probes?</div>'))),

  ("mufg010","Design a real-time transaction processing system — reliability, idempotency, scale",
   "system_design","fintech","Hard",_MUFG,90,"transaction-processing,kafka,idempotency,reliability,banking","System Design Round",
   A(("Requirements",
      "<b>Functional:</b> Accept trades from upstream, validate, book, expose via API. 10k trades/sec peak.<br>"
      "<b>Non-functional:</b> Exactly-one booking, 99.99% uptime, &lt;50ms p99 reads, full audit trail."),
     ("Architecture",
      "<pre>Upstream (FIX/SWIFT) → Kafka [trades.raw] (partitioned by bookId)\n  → Trade Booking Pods (OpenShift, count = Kafka partitions)\n    ├── Redis (idempotency cache: tradeId → result, 24h TTL)\n    ├── Oracle RAC (trades table, audit log)\n    └── Kafka [trade.booked] (downstream: Risk, Reporting)\n  → Read API (Spring Boot + HikariCP + Redis L1 cache)</pre>"),
     ("Idempotency + Distributed Lock",
      "<pre>public TradeResult book(TradeEvent e) {\n    String cached = redis.get(e.getTradeId());\n    if (cached != null) return deserialize(cached);\n    try (Lock lock = redisLock.acquire(\"lock:\"+e.getTradeId(), 5s)) {\n        cached = redis.get(e.getTradeId());  // double-check\n        if (cached != null) return deserialize(cached);\n        Trade t = tradeRepo.save(mapToTrade(e));\n        TradeResult res = TradeResult.booked(t);\n        redis.setex(e.getTradeId(), 86400, serialize(res));\n        return res;\n    }\n}</pre>"),
     ("Reliability",
      "<ul><li>Kafka RF=3, min.insync.replicas=2. Offset committed after DB write.</li>"
      "<li>Circuit Breaker on Risk/Notification calls (Resilience4j).</li>"
      "<li>Dead Letter Queue after 3 retries.</li>"
      "<li>HPA scales pods on CPU and Kafka consumer lag.</li></ul>"),
     ("Follow-ups",
      '<div class="followup">• What is the Outbox pattern and how does it solve dual-write?<br>'
      '• How do you implement end-to-end trade reconciliation (internal vs SWIFT)?<br>'
      '• What is ISO 20022 and why is MUFG migrating to it?</div>'))),

  ("mufg011","IBM MQ vs Kafka vs RabbitMQ — messaging in banking systems",
   "backend","messaging","Medium",_MUFG,80,"ibm-mq,kafka,rabbitmq,swift,messaging,banking","System Design Round",
   A(("IBM MQ — Legacy Banking Backbone",
      "Used for SWIFT FIN/XML (ISO 15022/20022), mainframe integration, guaranteed delivery.<br>"
      "<pre>@JmsListener(destination=\"TRADE.IN.QUEUE\")\n@Transactional\npublic void onSWIFT(TextMessage msg) throws JMSException {\n    Trade t = iso20022Parser.parse(msg.getText());\n    tradeService.book(t);\n    // ACK on tx commit\n}</pre>"),
     ("Kafka — High-Throughput Streaming","Internal microservices event bus, replay, regulatory audit trail. "
      "Millions of events/sec. Consumer groups for horizontal scaling."),
     ("RabbitMQ — Flexible Routing","AMQP with topic/fanout/direct exchanges. "
      "Used for async work queues (reports, notifications)."),
     ("Decision Matrix",
      "<ul><li><b>IBM MQ:</b> SWIFT integration, legacy, exactly-once, moderate throughput</li>"
      "<li><b>Kafka:</b> Internal events, high throughput, replay, event sourcing</li>"
      "<li><b>RabbitMQ:</b> Async tasks, complex routing, moderate throughput</li></ul>"),
     ("Follow-ups",
      '<div class="followup">• Spring Integration — how does it abstract multiple messaging systems?<br>'
      '• How do you monitor Kafka consumer lag? (Burrow, Prometheus, Kafka Manager)<br>'
      '• ActiveMQ Artemis vs RabbitMQ?</div>'))),

  ("mufg012","Banking data formats — ISO 20022, NACHA, BAI2 parsing in Java",
   "backend","banking-domain","Medium",_MUFG,78,"iso20022,nacha,bai2,swift,banking-formats","System Design Round",
   A(("ISO 20022 (SWIFT Replacement)",
      "XML-based. pacs.008=credit transfer, camt.053=statement, tsmt=trade.<br>"
      "<pre>// JAXB parsing\nJAXBContext ctx = JAXBContext.newInstance(Document.class);\nDocument doc = (Document) ctx.createUnmarshaller().unmarshal(xmlStream);\nString msgId = doc.getFIToFICstmrCdtTrf().getGrpHdr().getMsgId();</pre>"),
     ("NACHA — US ACH Payments","Fixed-width flat file. Record types: 1=FileHeader, 5=BatchHeader, "
      "6=EntryDetail, 8=BatchControl, 9=FileControl.<br>"
      "<pre>String line = reader.readLine();\nif (line.charAt(0)=='6') {  // Entry Detail\n    String routing = line.substring(3,11);\n    BigDecimal amt = new BigDecimal(line.substring(29,39)).movePointLeft(2);\n}</pre>"),
     ("BAI2 — Bank Statements","Comma-delimited balance/transaction file used in cash management and reconciliation.<br>"
      "<code>03,ACC001,USD,015,1000000,,,/</code> → account ACC001, opening balance $1M."),
     ("Follow-ups",
      '<div class="followup">• FIX Protocol vs SWIFT — where is each used?<br>'
      '• How would you build a reconciliation engine matching BAI2 against internal trade records?<br>'
      '• What is SWIFT gpi and why does it matter for MUFG cross-border payments?</div>'))),

  ("mufg013","ReactJS core — components, JSX, props vs state, lifecycle hooks",
   "java","reactjs","Medium",_MUFG,92,"react,jsx,props,state,hooks,usestate,useeffect","Technical Round",
   A(("Functional Components + Hooks (modern React)",
      "<pre>// Functional component with useState + useEffect\nimport React, { useState, useEffect } from 'react';\n\nconst TradeDashboard = () =&gt; {\n  const [trades, setTrades] = useState([]);      // state\n  const [loading, setLoading] = useState(true);\n  const [filter, setFilter] = useState('');\n\n  useEffect(() =&gt; {\n    // Runs after mount (and when deps change)\n    fetch('/api/v1/trades')\n      .then(r =&gt; r.json())\n      .then(data =&gt; { setTrades(data); setLoading(false); })\n      .catch(err =&gt; console.error(err));\n\n    return () =&gt; { /* cleanup on unmount */ };\n  }, []);  // empty deps = run once on mount\n\n  const filtered = trades.filter(t =&gt;\n    t.id.toLowerCase().includes(filter.toLowerCase()));\n\n  if (loading) return &lt;div&gt;Loading...&lt;/div&gt;;\n\n  return (\n    &lt;div&gt;\n      &lt;input value={filter} onChange={e =&gt; setFilter(e.target.value)}\n             placeholder=\"Search trades\" /&gt;\n      {filtered.map(t =&gt; (\n        &lt;TradeRow key={t.id} trade={t} /&gt;  // key required for lists!\n      ))}\n    &lt;/div&gt;\n  );\n};</pre>"),
     ("Props vs State",
      "<ul><li><b>Props:</b> Read-only data passed from parent to child. Child cannot modify props.</li>"
      "<li><b>State:</b> Mutable data local to a component. Managed via <code>useState</code>.</li>"
      "<li>Changing either causes a re-render. State updates are <b>asynchronous and batched</b>.</li></ul>"
      "<pre>// Child receives trade as prop — read-only\nconst TradeRow = ({ trade }) =&gt; (\n  &lt;tr className={trade.status === 'PENDING' ? 'pending' : ''}&gt;\n    &lt;td&gt;{trade.id}&lt;/td&gt;\n    &lt;td&gt;{new Intl.NumberFormat('en-US',{style:'currency',currency:trade.currency})\n           .format(trade.amount)}&lt;/td&gt;\n    &lt;td&gt;{trade.status}&lt;/td&gt;\n  &lt;/tr&gt;\n);</pre>"),
     ("Key Hooks",
      "<ul><li><code>useState(init)</code> — local state</li>"
      "<li><code>useEffect(fn, deps)</code> — side effects (API calls, subscriptions, timers)</li>"
      "<li><code>useCallback(fn, deps)</code> — memoize function reference (avoid child re-renders)</li>"
      "<li><code>useMemo(fn, deps)</code> — memoize expensive computation</li>"
      "<li><code>useRef(init)</code> — mutable ref that does NOT trigger re-render (DOM refs, timers)</li>"
      "<li><code>useContext(ctx)</code> — consume React Context without prop drilling</li>"
      "<li><code>useReducer(reducer, init)</code> — complex state logic, like mini-Redux</li></ul>"),
     ("Common Pitfalls",
      "<ul><li>Missing <code>key</code> prop in lists → React can't efficiently reconcile DOM</li>"
      "<li>Stale closure in <code>useEffect</code> — capture state that never updates</li>"
      "<li>Infinite loop: <code>useEffect(() =&gt; { setState(...) })</code> with no deps array</li>"
      "<li>Mutating state directly: <code>trades.push(t)</code> — use <code>setTrades([...trades, t])</code></li></ul>"),
     ("Cross-Questions &amp; Follow-ups",
      '<div class="followup">• What is React reconciliation and the Virtual DOM?<br>'
      '• Class component lifecycle vs hooks equivalents (componentDidMount = useEffect([]))?<br>'
      '• When would you use useReducer over useState?<br>'
      '• How does React.memo() prevent unnecessary re-renders?<br>'
      '• What is the difference between controlled and uncontrolled components?</div>'))),

  ("mufg014","Spring @Transactional — isolation levels, propagation, ACID in banking",
   "database","transactions","Hard",_MUFG,86,"spring,transactional,acid,isolation,propagation","Database Round",
   A(("@Transactional Usage",
      "<pre>@Transactional  // REQUIRED, isolation=DEFAULT, rollback on RuntimeException\npublic Trade bookTrade(BookRequest req) {\n    Trade t = tradeRepo.save(mapToTrade(req));\n    positionService.update(t);   // same transaction\n    notify(t);\n    return t;  // COMMIT all; RuntimeException → ROLLBACK all\n}\n\n@Transactional(readOnly=true)  // DB optimization: no undo log\npublic Optional&lt;Trade&gt; find(String id) { return tradeRepo.findById(id); }\n\n@Transactional(propagation=Propagation.REQUIRES_NEW,\n               isolation=Isolation.SERIALIZABLE)\npublic void auditLog(Trade t) { auditRepo.save(AuditEntry.from(t)); }</pre>"),
     ("Isolation Levels",
      "<ul><li>READ_UNCOMMITTED — dirty reads possible (never in banking)</li>"
      "<li>READ_COMMITTED (default) — no dirty reads, non-repeatable possible</li>"
      "<li>REPEATABLE_READ — no non-repeatable reads, phantom possible</li>"
      "<li>SERIALIZABLE — fully isolated, slowest (use for audit/regulatory)</li></ul>"),
     ("Self-Invocation Pitfall",
      "<pre>// WRONG: this.auditLog() bypasses Spring proxy → @Transactional ignored!\npublic void bookTrade() { this.auditLog(); }\n// FIX: inject self via @Autowired or use ApplicationContext.getBean()</pre>"),
     ("Follow-ups",
      '<div class="followup">• @Version (optimistic) vs SELECT FOR UPDATE (pessimistic)?<br>'
      '• rollbackFor=Exception.class — why needed for checked exceptions?<br>'
      '• Distributed txns across Oracle + Kafka — Saga vs XA?</div>'))),

  ("mufg015","SQL optimization and JDBC for high-volume banking queries",
   "database","sql","Medium",_MUFG,82,"sql,jdbc,index,connection-pool,hikari,oracle","Database Round",
   A(("Common Optimizations",
      "<pre>-- BAD: function on indexed column = full scan\nSELECT * FROM trades WHERE UPPER(currency)='USD';\n-- GOOD:\nSELECT trade_id, amount, currency FROM trades WHERE currency='USD';\n\n-- Composite index for common filter\nCREATE INDEX idx_trades_book_status ON trades(book_id, status, trade_date DESC);\n\n-- Partial index (PostgreSQL)\nCREATE INDEX idx_pending ON trades(trade_date) WHERE status='PENDING';</pre>"),
     ("HikariCP Config",
      "<pre>spring.datasource.hikari:\n  maximum-pool-size: 20\n  connection-timeout: 3000   # fail fast\n  idle-timeout: 600000\n  leak-detection-threshold: 5000  # warn if held > 5s</pre>"),
     ("JDBC Batch Insert",
      "<pre>conn.setAutoCommit(false);\nPreparedStatement ps = conn.prepareStatement(\n    \"INSERT INTO trades(id,amount,currency,status) VALUES(?,?,?,?)\");\nfor (Trade t : trades) {\n    ps.setString(1,t.getId()); ps.setBigDecimal(2,t.getAmount());\n    ps.setString(3,t.getCurrency()); ps.setString(4,\"BOOKED\");\n    ps.addBatch();\n    if (++count%1000==0) ps.executeBatch();\n}\nps.executeBatch(); conn.commit();</pre>"),
     ("Follow-ups",
      '<div class="followup">• How to read EXPLAIN ANALYZE output?<br>'
      '• Clustered vs non-clustered index?<br>'
      '• Materialized view vs regular view for regulatory reporting?</div>'))),

  ("mufg016","Banking security — IAM, JWT RS256, OAuth2, Veracode SAST in Jenkins",
   "security","banking-security","Hard",_MUFG,84,"iam,jwt,oauth2,veracode,sast,spring-security","Technical Round",
   A(("IAM at MUFG",
      "LDAP/Active Directory for employee identity. RBAC (Trader, Risk Manager, Compliance, Admin) roles. "
      "Keycloak/Azure AD as OAuth2/OIDC Identity Provider for service-to-service auth. "
      "CyberArk for PAM — DB credential and API key rotation."),
     ("JWT Filter (RS256)",
      "<pre>@Component\npublic class JwtAuthFilter extends OncePerRequestFilter {\n    protected void doFilterInternal(HttpServletRequest req, ...) {\n        String token = extractBearer(req);\n        if (token == null) { filterChain.doFilter(req,res); return; }\n        try {\n            Claims claims = Jwts.parserBuilder()\n                .setSigningKey(rsaPublicKey)  // RS256 asymmetric\n                .build().parseClaimsJws(token).getBody();\n            SecurityContextHolder.getContext().setAuthentication(\n                new UsernamePasswordAuthenticationToken(\n                    claims.getSubject(), null,\n                    toAuthorities(claims.get(\"roles\",List.class))));\n        } catch (JwtException e) { res.sendError(401); return; }\n        filterChain.doFilter(req, res);\n    }\n}</pre>"),
     ("Veracode in Jenkins",
      "<pre>stage('Veracode SAST') {\n    steps {\n        withCredentials([usernamePassword(credentialsId:'veracode-api',\n                usernameVariable:'VID', passwordVariable:'VKEY')]) {\n            sh 'java -jar veracode-wrapper.jar -vid $VID -vkey $VKEY \\\\\n                -action UploadAndScan -appname TradeBooking \\\\\n                -filepath target/*.jar -scantimeout 60'\n        }\n    }\n}</pre>"
      "Detects: SQL injection, XSS, insecure deserialization, hardcoded secrets, weak crypto."),
     ("Follow-ups",
      '<div class="followup">• DAST vs SAST — which finds runtime vulnerabilities?<br>'
      '• How to rotate DB secrets in K8s? (HashiCorp Vault, K8s Secrets, CyberArk)<br>'
      '• JWT localStorage vs HttpOnly cookie — security implications?</div>'))),

  ("mufg017","Jenkins CI/CD pipeline — Build, Test, Veracode, Docker, OpenShift deploy",
   "cicd","jenkins","Medium",_MUFG,82,"jenkins,cicd,openshift,docker,veracode,splunk","CI/CD Round",
   A(("Tech Stack at MUFG",
      "BitBucket → Jenkins → Nexus/Artifactory → Veracode → Docker Registry → OpenShift → Splunk"),
     ("Jenkinsfile",
      "<pre>pipeline {\n  agent { label 'java-agent' }\n  stages {\n    stage('Build&amp;Test') {\n      steps {\n        sh 'mvn clean verify'\n        junit 'target/surefire-reports/*.xml'\n      }\n    }\n    stage('Veracode') {\n      steps { veracode applicationName:'TradeBooking', filepath:'target/*.jar' }\n    }\n    stage('Docker') {\n      steps {\n        sh \"docker build -t registry.mufg.com/trade-booking:${GIT_COMMIT} .\"\n        sh \"docker push registry.mufg.com/trade-booking:${GIT_COMMIT}\"\n      }\n    }\n    stage('Deploy OpenShift') {\n      steps {\n        sh \"oc set image deployment/trade-booking \\\\\n            trade-booking=registry.mufg.com/trade-booking:${GIT_COMMIT} -n mufg-prod\"\n        sh 'oc rollout status deployment/trade-booking -n mufg-prod --timeout=5m'\n      }\n    }\n  }\n  post { failure { slackSend '#trade-alerts', \"Build FAILED\" } }\n}</pre>"),
     ("Multi-Stage Dockerfile",
      "<pre>FROM eclipse-temurin:17-jdk AS build\nWORKDIR /app\nCOPY pom.xml . &amp;&amp; mvn dependency:go-offline -q\nCOPY src ./src &amp;&amp; mvn package -DskipTests\n\nFROM eclipse-temurin:17-jre-alpine\nWORKDIR /app\nCOPY --from=build /app/target/trade-booking-*.jar app.jar\nUSER 1001\nENTRYPOINT [\"java\",\"-XX:+UseZGC\",\"-jar\",\"app.jar\"]</pre>"),
     ("Follow-ups",
      '<div class="followup">• Blue-green vs canary on OpenShift?<br>'
      '• Helm for OpenShift — what does a values.yaml look like?<br>'
      '• How to implement Jenkins pipeline rollback on failed deploy?</div>'))),

  ("mufg018","Kubernetes/OpenShift — Deployment, Probes, HPA, ConfigMap for banking services",
   "cicd","kubernetes","Hard",_MUFG,80,"kubernetes,openshift,hpa,probes,configmap,liveness","CI/CD Round",
   A(("Deployment YAML",
      "<pre>apiVersion: apps/v1\nkind: Deployment\nmetadata: { name: trade-booking, namespace: mufg-prod }\nspec:\n  replicas: 3\n  template:\n    spec:\n      containers:\n      - name: trade-booking\n        image: registry.mufg.com/trade-booking:v1.2.3\n        env:\n        - name: DB_PASSWORD\n          valueFrom: { secretKeyRef: {name: oracle-secret, key: password} }\n        resources:\n          requests: { cpu: 500m, memory: 512Mi }\n          limits:   { cpu: 2, memory: 2Gi }\n        livenessProbe:\n          httpGet: { path: /actuator/health/liveness, port: 8080 }\n          initialDelaySeconds: 30\n        readinessProbe:\n          httpGet: { path: /actuator/health/readiness, port: 8080 }\n          initialDelaySeconds: 20</pre>"),
     ("HPA with Custom Kafka Lag Metric",
      "<pre>apiVersion: autoscaling/v2\nkind: HorizontalPodAutoscaler\nspec:\n  scaleTargetRef: { kind: Deployment, name: trade-booking }\n  minReplicas: 3\n  maxReplicas: 20\n  metrics:\n  - type: Resource\n    resource: { name: cpu, target: { type: Utilization, averageUtilization: 70 } }\n  - type: External\n    external:\n      metric: { name: kafka_consumer_lag }\n      target: { type: AverageValue, averageValue: 1000 }</pre>"),
     ("Spring Boot Actuator for Probes",
      "<pre># application.yml\nmanagement.endpoint.health.probes.enabled: true\nmanagement.health.livenessState.enabled: true\nmanagement.health.readinessState.enabled: true</pre>"),
     ("Follow-ups",
      '<div class="followup">• Liveness vs readiness vs startup probes — when to use each?<br>'
      '• PodDisruptionBudget — critical for banking availability?<br>'
      '• How to handle connection pool sizing with HPA?</div>'))),

  ("mufg019","Java concurrency — synchronized vs ReentrantLock, ExecutorService for trade processing",
   "concurrency","locking","Hard",_MUFG,78,"synchronized,reentrantlock,executorservice,thread-safety","Concurrency Round",
   A(("synchronized vs ReentrantLock",
      "<pre>// synchronized — simple, no tryLock\npublic synchronized void updatePosition(String book, BigDecimal delta) {\n    positions.merge(book, delta, BigDecimal::add);\n}\n\n// ReentrantReadWriteLock — multiple readers OR one writer\nReentrantReadWriteLock rwl = new ReentrantReadWriteLock();\npublic void update(String book, BigDecimal d) {\n    rwl.writeLock().lock();\n    try { positions.merge(book, d, BigDecimal::add); }\n    finally { rwl.writeLock().unlock(); }\n}\npublic BigDecimal get(String book) {\n    rwl.readLock().lock();\n    try { return positions.getOrDefault(book, ZERO); }\n    finally { rwl.readLock().unlock(); }\n}</pre>"),
     ("Trade Processing ThreadPool",
      "<pre>ExecutorService pool = new ThreadPoolExecutor(\n    10, 50, 60L, SECONDS,\n    new ArrayBlockingQueue&lt;&gt;(10000),   // bounded = backpressure\n    new ThreadFactoryBuilder().setNameFormat(\"trade-worker-%d\").build(),\n    new CallerRunsPolicy());            // natural backpressure on caller\n\npool.submit(() -&gt; tradeService.process(event));</pre>"),
     ("Avoiding Deadlock",
      "<ul><li>Always acquire locks in the same order across all threads</li>"
      "<li>Use <code>tryLock(timeout)</code> to avoid indefinite blocking</li>"
      "<li>Prefer <code>ConcurrentHashMap</code> + atomic ops over coarse synchronized</li></ul>"),
     ("Follow-ups",
      '<div class="followup">• Why is Executors.newFixedThreadPool() dangerous? (unbounded LinkedBlockingQueue)<br>'
      '• What is StampedLock and when is it better than RRW Lock?<br>'
      '• How do virtual threads (Java 21) change concurrency in banking services?</div>'))),

  ("mufg020","Behavioral — STAR format: challenging project, conflict resolution, teamwork",
   "behavioral","situational","Easy",_MUFG,85,"behavioral,star,conflict,teamwork,banking","HR Round",
   A(("Design a Real-Time Reconciliation System (Challenge STAR)",
      "<b>Situation:</b> Legacy nightly batch reconciliation took 8 hours — breaches weren't caught until next morning.<br>"
      "<b>Task:</b> Redesign as near-real-time with &lt;15 min breach detection window.<br>"
      "<b>Action:</b> Replaced batch SQL with Kafka consumer comparing SWIFT confirmations vs internal bookings. "
      "Used ConcurrentHashMap for in-memory position cache, Spring Batch for EOD reporting, Splunk alerting.<br>"
      "<b>Result:</b> Reconciliation latency reduced from 8 hours to 12 minutes. Breach detection SLA met. "
      "Zero production incidents in 6 months post-launch."),
     ("Stakeholder Conflict (STAR)",
      "<b>Situation:</b> Business wanted a new trade amendment feature in 2 weeks; security team required Veracode scan which takes 5 days.<br>"
      "<b>Task:</b> Balance delivery speed with security compliance.<br>"
      "<b>Action:</b> Proposed incremental approach — baseline feature with Veracode scan done in parallel (not blocking). "
      "Set up automated Veracode in Jenkins so future features are scanned continuously, not as a gate.<br>"
      "<b>Result:</b> Feature delivered in 2 weeks, security scans embedded in pipeline permanently."),
     ("Why MUFG / Banking",
      "MUFG's mission to be the world's most trusted financial group aligns with building high-integrity systems. "
      "Banking requires the highest standards of reliability, security, and audit — challenges that drive "
      "engineering excellence in distributed systems, concurrency, and data integrity."),
     ("Follow-ups",
      '<div class="followup">• Tell me about a time you had to learn a new technology quickly.<br>'
      '• How do you prioritize when multiple high-priority issues come simultaneously?<br>'
      '• Describe a time you disagreed with your manager — how did you handle it?</div>'))),

]

def _to_dict(q):
    return {"id":q[0],"text":q[1],"category":q[2],"subcategory":q[3],"difficulty":q[4],
            "companies":q[5],"frequency":q[6],"tags":q[7].split(","),"round_type":q[8],"answer_hint":q[9]}

QUESTIONS = [_to_dict(q) for q in MUFG_Q]
