"""Full answers for LLD questions (lld001-lld025) and behavioral (beh001-beh010)."""

def A(*s):
    parts = [f'<span class="answer-label">{l}</span><br>{c}' for l,c in s]
    return '<div class="answer-section">'+'</div><div class="answer-section" style="margin-top:10px">'.join(parts)+'</div>'

FULL_ANSWERS_LLD = {

"lld001": A(("Entities & Design",
    "<ul><li><b>ParkingLot:</b> Singleton. Has multiple floors.</li>"
    "<li><b>ParkingFloor:</b> Has spots of different sizes (SMALL, MEDIUM, LARGE).</li>"
    "<li><b>ParkingSpot:</b> spotNumber, spotType, isAvailable, parkedVehicle.</li>"
    "<li><b>Vehicle:</b> Abstract. Subtypes: Car, Bike, Truck. Has licensePlate, vehicleType.</li>"
    "<li><b>Ticket:</b> ticketId, entryTime, spot. Links vehicle to spot.</li>"
    "<li><b>ParkingDisplayBoard:</b> Observer — updates on spot change.</li></ul>"),
  ("Key Patterns",
    "<ul><li><b>Strategy:</b> PricingStrategy — hourly, daily, per-spot-type</li>"
    "<li><b>Observer:</b> DisplayBoard observes spot availability changes</li>"
    "<li><b>Singleton:</b> ParkingLot instance</li>"
    "<li><b>Factory:</b> VehicleFactory.create(type)</li></ul>"),
  ("Concurrency",
    "<pre>// Thread-safe spot assignment\npublic synchronized Ticket park(Vehicle v) {\n    ParkingSpot spot = findAvailableSpot(v.getType());\n    if (spot == null) throw new ParkingFullException();\n    spot.setOccupied(true);\n    return new Ticket(v, spot, LocalDateTime.now());\n}</pre>"),
  ("Cross-questions", "<ul><li>How do you handle multiple entry/exit gates concurrently?</li>"
    "<li>How do you implement reserved spots for subscribers?</li>"
    "<li>How do you calculate the fee for partial hours?</li></ul>"),
  ("Follow-ups",'<div class="followup">• How would you add electric vehicle charging spots?<br>'
    '• How would you implement a monthly pass feature?<br>'
    '• How do you find the nearest available spot to a given entrance gate?</div>')),

"lld003": A(("State Machine",
    "<pre>States: IDLE → CARD_INSERTED → PIN_AUTHENTICATING → SELECTING → DISPENSING → EJECTING\n\nclass ATM {\n    ATMState currentState;\n    void insertCard()  { currentState.insertCard(); }\n    void enterPin(int pin) { currentState.enterPin(pin); }\n    void withdraw(int amount) { currentState.withdraw(amount); }\n    void ejectCard() { currentState.ejectCard(); }\n}</pre>"),
  ("Key Classes",
    "<ul><li><b>ATMState (interface):</b> insertCard, enterPin, withdraw, ejectCard</li>"
    "<li><b>IdleState, CardInsertedState, AuthenticatingState, DispensingState:</b> each implements ATMState</li>"
    "<li><b>CashDispenser:</b> tracks cash level, notifies when low</li>"
    "<li><b>BankService:</b> validates PIN, processes debit</li></ul>"),
  ("Cross-questions","<ul><li>How do you handle PIN retry limit (3 attempts → card blocked)?</li>"
    "<li>How do you handle network failure during transaction?</li>"
    "<li>How do you implement multi-currency dispensing?</li></ul>"),
  ("Follow-ups",'<div class="followup">• How would you add UPI/contactless payment?<br>'
    '• How do you handle transaction timeout?<br>'
    '• How does the State pattern compare to enum-based state management?</div>')),

"lld005": A(("State Machine",
    "<pre>TripState: REQUESTED → DRIVER_ACCEPTED → DRIVER_ARRIVED → IN_PROGRESS → COMPLETED / CANCELLED\n\nclass Trip {\n    String tripId; Driver driver; Rider rider;\n    TripState state; Location pickup, dropoff;\n    double fare;\n    void accept(Driver d) { this.driver=d; state=DRIVER_ACCEPTED; notify(); }\n    void start() { state=IN_PROGRESS; startTime=now(); }\n    void complete() { state=COMPLETED; fare=calculateFare(); }\n}</pre>"),
  ("Key Entities",
    "<ul><li><b>Driver:</b> id, currentLocation, status (AVAILABLE/ON_TRIP/OFFLINE), rating</li>"
    "<li><b>Rider:</b> id, paymentMethod, currentLocation</li>"
    "<li><b>MatchingService:</b> finds nearest available driver (Strategy: nearest, highest-rated)</li>"
    "<li><b>FareCalculator:</b> Strategy — base + per-km + surge multiplier</li>"
    "<li><b>NotificationService:</b> Observer — alerts driver and rider on state changes</li></ul>"),
  ("Cross-questions","<ul><li>How do you handle driver rejection (offer to next driver)?</li>"
    "<li>How do you implement pool rides (multiple riders)?</li>"
    "<li>How do you track real-time location? (polling every 5s vs WebSocket push)</li></ul>"),
  ("Follow-ups",'<div class="followup">• How would you extend to auto-rickshaw, bikes, taxis (different vehicle types)?<br>'
    '• How does surge pricing affect driver dispatch?<br>'
    '• How do you handle split payment between riders in a pool?</div>')),

"lld006": A(("Scheduling Strategies",
    "<ul><li><b>SCAN (Elevator algorithm):</b> Go in one direction, serve all requests, reverse. Minimizes total travel.</li>"
    "<li><b>LOOK:</b> Like SCAN but reverses when no more requests in current direction (doesn't go to end).</li>"
    "<li><b>FCFS:</b> First come first served. Simple but suboptimal.</li></ul>"),
  ("Design",
    "<pre>class Elevator {\n    int currentFloor; Direction dir; ElevatorState state;\n    List&lt;Request&gt; queue;  // sorted by floor\n    void addRequest(Request r) { queue.add(r); processNext(); }\n    void processNext() {\n        Request next = schedulingStrategy.pickNext(queue, currentFloor, dir);\n        moveTo(next.floor);\n    }\n}\nclass ElevatorSystem {\n    List&lt;Elevator&gt; elevators;\n    void requestElevator(int floor, Direction d) {\n        Elevator best = findOptimalElevator(floor, d);  // least-travel heuristic\n        best.addRequest(new Request(floor, d));\n    }\n}</pre>"),
  ("Cross-questions","<ul><li>How do you handle emergency (fire) — all elevators to ground floor?</li>"
    "<li>How do you optimize for a building with VIP floors?</li>"
    "<li>How do you handle overweight detection?</li></ul>"),
  ("Follow-ups",'<div class="followup">• How does this system scale to a 100-floor building with 20 elevators?<br>'
    '• What is the SSTF (Shortest Seek Time First) strategy and what is its starvation problem?<br>'
    '• How would you add a dispatch algorithm that minimizes average wait time?</div>')),

"lld010": A(("Entities",
    "<ul><li><b>Theatre, Screen, Show, Seat, Booking:</b> core entities</li>"
    "<li><b>Seat states:</b> AVAILABLE, LOCKED (temp reserved), BOOKED</li></ul>"),
  ("Concurrency — Seat Reservation",
    "<pre>// Optimistic locking with version field\n@Entity\nclass Seat {\n    Long id; SeatStatus status; int version;  // JPA @Version\n}\n\n// Service\n@Transactional\npublic Booking reserveSeats(List&lt;Long&gt; seatIds, User user) {\n    List&lt;Seat&gt; seats = seatRepo.findAllById(seatIds);\n    for (Seat s : seats) {\n        if (s.getStatus() != AVAILABLE)\n            throw new SeatNotAvailableException(s.getId());\n        s.setStatus(LOCKED);  // version bumped by JPA\n    }\n    // Confirmed after payment\n    return new Booking(seats, user, LocalDateTime.now());\n}  // On version conflict: OptimisticLockException → retry or fail</pre>"),
  ("TTL-based Lock Release",
    "If payment not completed in 10 minutes → scheduled job releases LOCKED → back to AVAILABLE."),
  ("Cross-questions","<ul><li>How do you prevent two users from booking the same seat simultaneously?</li>"
    "<li>How do you implement seat selection UI with real-time availability?</li>"
    "<li>How do you handle partial refunds?</li></ul>"),
  ("Follow-ups",'<div class="followup">• SELECT FOR UPDATE SKIP LOCKED — how does it prevent double booking at DB level?<br>'
    '• How would you design this for millions of users (BookMyShow scale)?<br>'
    '• How does the saga pattern apply to booking + payment flow?</div>')),

"lld013": A(("Observer Pattern",
    "<pre>interface NotificationObserver { void update(Event event); }\n\nclass EmailNotifier implements NotificationObserver {\n    public void update(Event e) { emailService.send(e.getUserEmail(), e.getMessage()); }\n}\nclass SMSNotifier implements NotificationObserver { ... }\nclass PushNotifier implements NotificationObserver { ... }\n\nclass NotificationService {\n    Map&lt;EventType, List&lt;NotificationObserver&gt;&gt; subscribers = new HashMap&lt;&gt;();\n    void subscribe(EventType t, NotificationObserver o) { subscribers.get(t).add(o); }\n    void notify(Event e) {\n        for (NotificationObserver o : subscribers.get(e.getType()))\n            executorService.submit(() -&gt; o.update(e));  // async\n    }\n}</pre>"),
  ("Chain of Responsibility (Fallback)",
    "EmailHandler → SMSHandler → PushHandler. If email fails, try SMS, etc."),
  ("Cross-questions","<ul><li>How do you handle notification templates? (Template Method pattern)</li>"
    "<li>How do you add rate limiting per user per channel?</li>"
    "<li>How do you ensure at-least-once delivery?</li></ul>"),
  ("Follow-ups",'<div class="followup">• How do you implement notification preferences per user?<br>'
    '• How do you handle bounced emails or undeliverable SMS?<br>'
    '• How does this extend to a distributed notification system at scale?</div>')),

"lld014": A(("LRU Cache",
    "<pre>class LRUCache&lt;K,V&gt; {\n    int capacity;\n    LinkedHashMap&lt;K,V&gt; cache;\n    LRUCache(int cap) {\n        capacity = cap;\n        cache = new LinkedHashMap&lt;&gt;(16, 0.75f, true) {  // accessOrder=true\n            protected boolean removeEldestEntry(Map.Entry&lt;K,V&gt; e) {\n                return size() &gt; capacity;\n            }\n        };\n    }\n    public synchronized V get(K key) { return cache.getOrDefault(key, null); }\n    public synchronized void put(K key, V val) { cache.put(key, val); }\n}</pre>"),
  ("LFU Cache",
    "<pre>class LFUCache {\n    Map&lt;Integer,Integer&gt; vals = new HashMap&lt;&gt;();\n    Map&lt;Integer,Integer&gt; counts = new HashMap&lt;&gt;();\n    Map&lt;Integer, LinkedHashSet&lt;Integer&gt;&gt; freqMap = new HashMap&lt;&gt;();\n    int minFreq, cap;\n    // On get: increment freq, move to higher freq bucket\n    // On put: if cap exceeded, evict from minFreq bucket (oldest entry)\n}</pre>"),
  ("Strategy Pattern","Pluggable eviction: <code>EvictionPolicy</code> interface with <code>LRU</code>, <code>LFU</code>, <code>FIFO</code> implementations."),
  ("Cross-questions","<ul><li>How do you make LRU thread-safe without a global lock? (shard by key hash)</li>"
    "<li>How do you implement TTL-based expiry alongside LRU eviction?</li>"
    "<li>How does Redis implement LRU? (approximate LRU — sample 5 keys, evict oldest)</li></ul>"),
  ("Follow-ups",'<div class="followup">• What is the time complexity of LFU vs LRU? (both O(1) with right structures)<br>'
    '• How does Caffeine (Java) implement W-TinyLFU?<br>'
    '• What is a 2Q (Two-Queue) cache?</div>')),

"lld016": A(("Token Bucket Implementation",
    "<pre>class TokenBucketRateLimiter {\n    private final long capacity;\n    private final double refillRatePerMs;\n    private double tokens;\n    private long lastRefillTime;\n\n    public TokenBucketRateLimiter(long capacity, long refillPerSecond) {\n        this.capacity = capacity;\n        this.refillRatePerMs = refillPerSecond / 1000.0;\n        this.tokens = capacity;\n        this.lastRefillTime = System.currentTimeMillis();\n    }\n\n    public synchronized boolean allowRequest() {\n        refill();\n        if (tokens &gt;= 1) { tokens--; return true; }\n        return false;\n    }\n\n    private void refill() {\n        long now = System.currentTimeMillis();\n        double toAdd = (now - lastRefillTime) * refillRatePerMs;\n        tokens = Math.min(capacity, tokens + toAdd);\n        lastRefillTime = now;\n    }\n}</pre>"),
  ("Per-Key Rate Limiter",
    "<pre>class RateLimiterService {\n    ConcurrentHashMap&lt;String, TokenBucketRateLimiter&gt; limiters = new ConcurrentHashMap&lt;&gt;();\n    boolean allow(String key) {\n        return limiters.computeIfAbsent(key,\n            k -&gt; new TokenBucketRateLimiter(100, 10)).allowRequest();\n    }\n}</pre>"),
  ("Cross-questions","<ul><li>How do you handle distributed rate limiting across 10 servers? (Redis Lua + ZADD sliding window)</li>"
    "<li>How do you implement rate limiting by IP + endpoint combination?</li>"
    "<li>How do you return the exact wait time to client? (time until next token available)</li></ul>"),
  ("Follow-ups",'<div class="followup">• What is the difference between token bucket and leaky bucket?<br>'
    '• How does Guava RateLimiter implement token bucket?<br>'
    '• How do you handle burst traffic legitimately? (pre-warm tokens)</div>')),

"lld021": A(("Design",
    "<pre>class URLShortener {\n    static final String CHARS = \"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ\";\n    AtomicLong counter = new AtomicLong(1);\n    ConcurrentHashMap&lt;String, URLEntry&gt; store = new ConcurrentHashMap&lt;&gt;();\n\n    String shorten(String url, int expiryDays) {\n        long id = counter.getAndIncrement();\n        String code = toBase62(id);\n        store.put(code, new URLEntry(url, Instant.now().plusSeconds(86400L*expiryDays)));\n        return \"https://sho.rt/\" + code;\n    }\n\n    String expand(String code) {\n        URLEntry e = store.get(code);\n        if (e == null || e.isExpired()) throw new NotFoundException();\n        return e.originalUrl;\n    }\n\n    private String toBase62(long n) {\n        StringBuilder sb = new StringBuilder();\n        while (n &gt; 0) { sb.insert(0, CHARS.charAt((int)(n%62))); n/=62; }\n        return sb.toString();\n    }\n}</pre>"),
  ("Distributed Design",
    "<ul><li>Counter: distributed ID generator (Snowflake or Redis INCR) instead of AtomicLong</li>"
    "<li>Store: Redis (fast reads) + database (durable) with write-through cache</li>"
    "<li>Custom aliases: check uniqueness, reject if taken</li>"
    "<li>Analytics: Kafka event per click → ClickHouse for aggregation</li></ul>"),
  ("Cross-questions","<ul><li>How do you prevent collision if counter is shared across servers?</li>"
    "<li>How do you implement custom vanity URLs (/my-brand)?</li>"
    "<li>How do you handle 301 vs 302 redirect? (301: browser caches, 302: server always consulted)</li></ul>"),
  ("Follow-ups",'<div class="followup">• How do you design URL shortener for 100M requests/day?<br>'
    '• How do you implement link preview (OG tags)?<br>'
    '• How do you detect and block malicious URLs?</div>')),

"lld024": A(("Architecture",
    "<ul><li><b>MemTable:</b> In-memory sorted tree (TreeMap). Writes go here first.</li>"
    "<li><b>WAL (Write-Ahead Log):</b> Append-only log for crash recovery.</li>"
    "<li><b>SSTable:</b> Immutable sorted file flushed from MemTable when full.</li>"
    "<li><b>Compaction:</b> Background merge of SSTables (remove tombstones, deduplicate).</li>"
    "<li><b>Bloom Filter:</b> Per-SSTable to skip files that don't contain a key (fast miss detection).</li></ul>"),
  ("Core Operations",
    "<pre>class KVStore {\n    TreeMap&lt;String,String&gt; memTable = new TreeMap&lt;&gt;();\n    List&lt;SSTable&gt; ssTables = new ArrayList&lt;&gt;();\n    WriteAheadLog wal;\n    final int MEM_TABLE_LIMIT = 1_000_000;\n\n    synchronized void put(String key, String value) {\n        wal.append(key, value);\n        memTable.put(key, value);\n        if (memTable.size() &gt;= MEM_TABLE_LIMIT) flush();\n    }\n\n    String get(String key) {\n        if (memTable.containsKey(key)) return memTable.get(key);\n        for (int i = ssTables.size()-1; i &gt;= 0; i--) {\n            if (ssTables.get(i).bloomFilter.mightContain(key))\n                return ssTables.get(i).get(key);  // binary search in sorted file\n        }\n        return null;\n    }\n}</pre>"),
  ("Cross-questions","<ul><li>How do you implement TTL (key expiry)?</li>"
    "<li>How does compaction prevent unbounded disk growth?</li>"
    "<li>How do you implement range queries efficiently?</li></ul>"),
  ("Follow-ups",'<div class="followup">• How does RocksDB differ from a simple LSM implementation?<br>'
    '• What is leveled vs size-tiered compaction strategy?<br>'
    '• How do you implement atomic multi-key transactions?</div>')),

"lld025": A(("Implementation",
    "<pre>class ConnectionPool {\n    BlockingDeque&lt;Connection&gt; pool;\n    AtomicInteger totalCreated;\n    int maxSize, minIdle;\n    long acquireTimeoutMs;\n\n    Connection borrow() throws Exception {\n        Connection conn = pool.pollFirst(acquireTimeoutMs, MILLISECONDS);\n        if (conn == null) {\n            if (totalCreated.get() &lt; maxSize) {\n                conn = createConnection(); totalCreated.incrementAndGet();\n            } else throw new TimeoutException(\"Pool exhausted\");\n        }\n        if (!conn.isValid()) { conn.close(); return borrow(); }  // retry\n        return conn;\n    }\n\n    void release(Connection conn) {\n        if (conn.isValid()) pool.offerFirst(conn);\n        else { conn.close(); totalCreated.decrementAndGet(); }\n    }\n\n    // Health check thread: periodically validate idle connections\n    void startHealthCheck() {\n        scheduler.scheduleAtFixedRate(() -&gt; {\n            pool.forEach(c -&gt; { if (!c.isValid()) { pool.remove(c); totalCreated.decrementAndGet(); } });\n            while (pool.size() &lt; minIdle) pool.add(createConnection());\n        }, 30, 30, SECONDS);\n    }\n}</pre>"),
  ("Cross-questions","<ul><li>How do you handle connection leaks? (track borrow time, log if not returned in N seconds)</li>"
    "<li>How do you implement maximum lifetime for connections? (stale connections cause issues)</li>"
    "<li>How does HikariCP achieve better performance than c3p0?</li></ul>"),
  ("Follow-ups",'<div class="followup">• What is the difference between connection pool and thread pool?<br>'
    '• How do you size a connection pool? (active_threads × avg_hold_time / avg_query_time)<br>'
    '• How do you handle connection pool exhaustion gracefully?</div>')),

# Behavioral full answers
"beh001": A(("STAR Framework",
    "<b>Structure your answer:</b><br>"
    "<ul><li><b>Situation:</b> Brief context — what system, what was at risk, time pressure</li>"
    "<li><b>Task:</b> Your specific responsibility in the incident</li>"
    "<li><b>Action:</b> Exactly what you did — detection, triage, mitigation, communication</li>"
    "<li><b>Result:</b> MTTR, impact scope, what was prevented, what was learned</li></ul>"),
  ("Strong Answer Structure",
    "<pre>1. Detection: How did you find out? (alert, customer report, PagerDuty)\n2. First 5 min: Who did you loop in? What did you check first? (dashboards, logs, traces)\n3. Hypothesis & Diagnosis: What did you suspect? How did you confirm?\n4. Mitigation: Feature flag off? Rollback? Traffic diversion? Hotfix?\n5. Communication: Status page, stakeholder updates, runbook\n6. RCA: 5-whys, timeline reconstruction\n7. Prevention: Monitoring gap fixed, test added, runbook updated</pre>"),
  ("What interviewers look for",
    "<ul><li>Ownership — you stayed until it was resolved, didn't blame others</li>"
    "<li>Clear thinking under pressure — systematic, not panicked</li>"
    "<li>Communication — proactive updates to stakeholders</li>"
    "<li>Learning mindset — concrete prevention actions, not just 'we'll be more careful'</li></ul>"),
  ("Follow-ups",'<div class="followup">• What was your MTTR and how does it compare to industry standards?<br>'
    '• What monitoring would you add to catch this faster next time?<br>'
    '• How did you communicate with non-technical stakeholders during the incident?</div>')),

"beh007": A(("How to Answer a Failure Question",
    "Interviewers want to see: <b>genuine reflection</b>, not a humble-brag. "
    "Choose a real technical failure with real impact. Do NOT say 'I work too hard' or choose trivial failures."),
  ("Strong Answer Framework",
    "<pre>1. Context: What was the failure? (missed deadline, data loss, wrong architecture choice)\n2. My specific contribution to the failure\n3. What happened when it went wrong (measurable impact)\n4. How I responded (owned it, fixed it)\n5. What I CONCRETELY changed afterward (new process, test added, design review)\n6. What I would do differently today</pre>"),
  ("Example Angles",
    "<ul><li>Chose wrong tech stack → had to migrate → cost N weeks. Learned: POC + load test before committing.</li>"
    "<li>Missed an edge case in prod → data corruption for 500 users. Learned: chaos testing, invariant checks.</li>"
    "<li>Ignored a code reviewer's concern → led to security issue. Learned: never dismiss security feedback without data.</li></ul>"),
  ("Follow-ups",'<div class="followup">• How have you changed your approach to prevent similar failures?<br>'
    '• How did your team react to the failure?<br>'
    '• What would you tell a junior engineer who just made the same mistake?</div>')),
}
