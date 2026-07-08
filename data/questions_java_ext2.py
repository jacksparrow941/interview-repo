"""Java Extended Part 2 — ThreadPoolExecutor, NIO, Stream internals, ClassLoader, Concurrency utilities."""

_JAVA = ["Amazon","Google","LinkedIn","Microsoft","Meta","PayPal","Oracle","Salesforce","Infosys","TCS"]

def A(*s):
    parts = [f'<span class="answer-label">{l}</span><br>{c}' for l,c in s]
    return '<div class="answer-section">'+'</div><div class="answer-section" style="margin-top:10px">'.join(parts)+'</div>'

JAVA2 = [
  ("jex011","ThreadPoolExecutor — all 7 parameters explained","java","concurrency","Hard",
   ["Amazon","Google","LinkedIn","Microsoft","Meta","PayPal"],88,"thread-pool,executor,queue,rejection","Concurrency Round",
   A(("Constructor Parameters",
      "<pre>new ThreadPoolExecutor(\n    int corePoolSize,      // threads always alive\n    int maximumPoolSize,   // max threads under load\n    long keepAliveTime,    // idle non-core thread timeout\n    TimeUnit unit,\n    BlockingQueue&lt;Runnable&gt; workQueue,  // task buffer\n    ThreadFactory threadFactory,         // name/daemon threads\n    RejectedExecutionHandler handler     // queue full policy\n);</pre>"),
     ("Sizing Strategy",
      "<ul><li><b>CPU-bound:</b> core = max = N_CPU + 1</li>"
      "<li><b>I/O-bound:</b> core = N_CPU × (1 + wait/compute). Use virtual threads (Java 21) instead.</li>"
      "<li><b>Queue type:</b> <code>LinkedBlockingQueue</code> (unbounded, dangerous), "
      "<code>ArrayBlockingQueue</code> (bounded, triggers max threads), <code>SynchronousQueue</code> (handoff, always spawns threads)</li></ul>"),
     ("Rejection Policies",
      "<ul><li><code>AbortPolicy</code>: throw RejectedExecutionException (default)</li>"
      "<li><code>CallerRunsPolicy</code>: run task in caller thread (natural backpressure)</li>"
      "<li><code>DiscardPolicy</code>: silently drop task</li>"
      "<li><code>DiscardOldestPolicy</code>: drop oldest queued task</li></ul>"),
     ("Thread Lifecycle","core threads → fill queue → spawn non-core threads to maxPoolSize → reject"),
     ("Follow-ups",'<div class="followup">• When do non-core threads get created? (queue full, &lt; maxPoolSize)<br>'
      '• How do you monitor thread pool health? (getActiveCount, getQueue().size())<br>'
      '• Why is Executors.newFixedThreadPool() dangerous? (unbounded LinkedBlockingQueue)</div>'))),

  ("jex012","Java NIO — Channels, Buffers, Selectors (non-blocking I/O)","java","nio","Hard",
   ["Amazon","Google","LinkedIn","Oracle"],74,"nio,channel,buffer,selector,non-blocking","Coding Round",
   A(("NIO vs Old IO",
      "<ul><li><b>Old IO (java.io):</b> Stream-based, blocking, thread-per-connection</li>"
      "<li><b>NIO (java.nio):</b> Buffer-based, non-blocking, multiplexed via Selector</li></ul>"),
     ("Key Components",
      "<ul><li><b>Buffer:</b> Fixed-size data container (ByteBuffer, IntBuffer). Has position, limit, capacity.</li>"
      "<li><b>Channel:</b> Bidirectional, non-blocking I/O endpoint (SocketChannel, FileChannel, ServerSocketChannel)</li>"
      "<li><b>Selector:</b> Monitors multiple channels on one thread. OS epoll/kqueue underneath.</li></ul>"),
     ("Non-blocking Server Skeleton",
      "<pre>Selector selector = Selector.open();\nServerSocketChannel ssc = ServerSocketChannel.open();\nssc.configureBlocking(false);\nssc.bind(new InetSocketAddress(8080));\nssc.register(selector, SelectionKey.OP_ACCEPT);\n\nwhile (true) {\n    selector.select();  // blocks until event\n    Set&lt;SelectionKey&gt; keys = selector.selectedKeys();\n    for (SelectionKey key : keys) {\n        if (key.isAcceptable()) { accept(key); }\n        else if (key.isReadable()) { read(key); }\n    }\n    keys.clear();\n}</pre>"),
     ("ByteBuffer","<code>flip()</code> switches from write to read mode. <code>clear()</code> resets for writing. "
      "<code>compact()</code> keeps unread bytes, moves to front."),
     ("Follow-ups",'<div class="followup">• What is NIO.2 (java.nio.file)? (Path, Files, WatchService)<br>'
      '• How does Netty build on NIO? (EventLoop, ChannelPipeline)<br>'
      '• When would you choose NIO over virtual threads?</div>'))),

  ("jex013","Java ClassLoader hierarchy and how class loading works","java","jvm","Hard",
   ["Amazon","Google","Oracle","LinkedIn","TCS","Infosys"],76,"classloader,bootstrap,delegation,hotswap","Coding Round",
   A(("ClassLoader Hierarchy",
      "<ul><li><b>Bootstrap ClassLoader:</b> Loads JDK core classes (java.lang, java.util) from rt.jar/modules. C++ code, no Java object.</li>"
      "<li><b>Platform ClassLoader (was Extension):</b> Loads java.se, java.xml etc.</li>"
      "<li><b>Application ClassLoader:</b> Loads from classpath (your app + third-party JARs).</li>"
      "<li>Custom ClassLoaders: hot-deploy, OSGi, isolation (one classloader per plugin).</li></ul>"),
     ("Delegation Model","When loading class X: check cache → delegate to parent → parent delegates to its parent → "
      "reach Bootstrap → if not found, child tries to load itself → ClassNotFoundException if all fail."),
     ("Class Identity","Same class name loaded by different ClassLoaders = <b>different classes</b>. "
      "ClassCastException when assigning across loaders. Root of hot-deploy complexity."),
     ("Custom ClassLoader",
      "<pre>class HotLoader extends ClassLoader {\n    @Override\n    protected Class&lt;?&gt; findClass(String name) throws ClassNotFoundException {\n        byte[] bytes = readBytesFromFile(name);\n        return defineClass(name, bytes, 0, bytes.length);\n    }\n}</pre>"),
     ("Follow-ups",'<div class="followup">• What is the ClassLoader leak in application servers?<br>'
      '• How does OSGi use ClassLoaders for module isolation?<br>'
      '• What is --add-opens in Java 9+ and why is it needed?</div>'))),

  ("jex014","CountDownLatch vs CyclicBarrier vs Semaphore vs Phaser","java","concurrency","Medium",
   ["Amazon","Google","LinkedIn","Microsoft","PayPal"],82,"countdown-latch,barrier,semaphore,phaser","Concurrency Round",
   A(("CountDownLatch","One-time gate. Threads <code>await()</code> until count reaches 0 via <code>countDown()</code>. Cannot be reset.<br>"
      "<pre>CountDownLatch latch = new CountDownLatch(3);\n// 3 workers call latch.countDown() when done\nlatch.await();  // main thread blocks until all 3 done</pre>"),
     ("CyclicBarrier","Reusable rendezvous point. All N threads call <code>await()</code> and block until all arrive. Then all proceed.<br>"
      "<pre>CyclicBarrier barrier = new CyclicBarrier(3, () -&gt; System.out.println(\"phase done\"));\n// Each thread calls barrier.await() — blocked until 3 threads reach barrier</pre>"),
     ("Semaphore","Controls access to N permits. <code>acquire()</code> blocks if 0 permits. <code>release()</code> returns one.<br>"
      "<pre>Semaphore sem = new Semaphore(5);  // max 5 concurrent threads\nsem.acquire();  // blocks if 5 already running\ntry { doWork(); } finally { sem.release(); }</pre>"),
     ("Phaser (Java 7+)","Most flexible: dynamic party count, multiple phases, tree structure for scaling.<br>"
      "<code>phaser.arriveAndAwaitAdvance()</code> — arrive + wait for next phase."),
     ("When to use","<ul><li><code>CountDownLatch</code>: wait for N events (startup, test setup)</li>"
      "<li><code>CyclicBarrier</code>: parallel computation phases (map-reduce stages)</li>"
      "<li><code>Semaphore</code>: connection pool, rate limiting, bounded resource access</li>"
      "<li><code>Phaser</code>: complex multi-phase parallel algorithms</li></ul>"),
     ("Follow-ups",'<div class="followup">• How would you implement a CountDownLatch using Semaphore?<br>'
      '• What is Exchanger and when is it used?<br>'
      '• How does CyclicBarrier handle thread interruption?</div>'))),

  ("jex015","Java Stream API internals — lazy evaluation, spliterator","java","streams","Hard",
   ["Amazon","Google","LinkedIn","Meta","Microsoft"],78,"streams,lazy,spliterator,parallel","Coding Round",
   A(("Lazy Evaluation","Intermediate operations (<code>filter</code>, <code>map</code>, <code>flatMap</code>) return a new Stream — <b>nothing executes</b>. "
      "Terminal operations (<code>collect</code>, <code>forEach</code>, <code>reduce</code>) trigger the pipeline. "
      "Short-circuit ops (<code>findFirst</code>, <code>limit</code>) stop early."),
     ("Pipeline Example",
      "<pre>List&lt;String&gt; result = list.stream()\n    .filter(s -&gt; s.length() &gt; 3)   // lazy: creates filter stage\n    .map(String::toUpperCase)         // lazy: creates map stage\n    .sorted()                          // stateful: must see all elements!\n    .limit(5)                          // short-circuit terminal\n    .collect(Collectors.toList());     // triggers whole pipeline</pre>"),
     ("Spliterator","The engine behind parallel streams. Splits data into chunks for ForkJoinPool. "
      "Characteristics: SIZED, ORDERED, DISTINCT, SORTED, IMMUTABLE, CONCURRENT."),
     ("Parallel Streams",
      "<pre>long count = LongStream.rangeClosed(1, 1_000_000)\n    .parallel()\n    .filter(n -&gt; isPrime(n))\n    .count();\n// Uses ForkJoinPool.commonPool()\n// Custom pool: submit to ForkJoinPool explicitly</pre>"),
     ("Common Collectors",
      "<pre>Collectors.toList()          // ArrayList\nCollectors.toUnmodifiableList() // immutable\nCollectors.groupingBy(key)   // Map&lt;K,List&lt;T&gt;&gt;\nCollectors.counting()\nCollectors.joining(\", \", \"[\", \"]\")\nCollectors.teeing(c1, c2, merger)  // Java 12+</pre>"),
     ("Follow-ups",'<div class="followup">• When does sorted() break stream laziness?<br>'
      '• How do you create a custom Collector?<br>'
      '• When is parallel stream harmful? (overhead > benefit for small lists)</div>'))),

  ("jex016","ReentrantReadWriteLock vs StampedLock","java","concurrency","Hard",
   ["Amazon","Google","LinkedIn","Meta"],72,"rwlock,stampedlock,optimistic,readwrite","Concurrency Round",
   A(("ReentrantReadWriteLock","Multiple concurrent readers OR one exclusive writer. "
      "Writer starvation risk if readers never release.<br>"
      "<pre>ReadWriteLock rwl = new ReentrantReadWriteLock();\nLock rl = rwl.readLock();\nLock wl = rwl.writeLock();\n\n// Read\nrl.lock(); try { return value; } finally { rl.unlock(); }\n// Write\nwl.lock(); try { value = newVal; } finally { wl.unlock(); }</pre>"),
     ("StampedLock (Java 8)","Better throughput via <b>optimistic reads</b> — no lock acquisition for reads if no writer active.<br>"
      "<pre>StampedLock sl = new StampedLock();\n\n// Optimistic read (no blocking):\nlong stamp = sl.tryOptimisticRead();\nint val = value;                      // read without lock\nif (!sl.validate(stamp)) {            // check if writer intervened\n    stamp = sl.readLock();            // fallback to real read lock\n    try { val = value; } finally { sl.unlockRead(stamp); }\n}\n\n// Write:\nlong ws = sl.writeLock();\ntry { value = newVal; } finally { sl.unlockWrite(ws); }</pre>"),
     ("When to use","<ul><li><code>RRW Lock</code>: read-heavy, need reentrant locking</li>"
      "<li><code>StampedLock</code>: read-heavy, max throughput, no reentrancy needed</li>"
      "<li>Avoid StampedLock if writes are frequent (optimistic reads will always fail)</li></ul>"),
     ("Follow-ups",'<div class="followup">• Why is StampedLock not reentrant?<br>'
      '• What is lock downgrading (write → read) in ReentrantRWLock?<br>'
      '• How does StampedLock compare to ConcurrentHashMap for thread safety?</div>'))),

  ("jex017","Java Memory Model — happens-before, volatile, final","java","jvm","Hard",
   ["Amazon","Google","LinkedIn","Meta","Microsoft"],78,"java-memory-model,happens-before,volatile","Coding Round",
   A(("Happens-Before Rules","If A happens-before B, A's writes are visible to B.<br>"
      "<ul><li>Program order: actions in a thread</li>"
      "<li>Monitor unlock HB lock by any thread</li>"
      "<li>volatile write HB volatile read of same field</li>"
      "<li>Thread.start() HB all actions in started thread</li>"
      "<li>Thread.join() HB actions after join returns</li>"
      "<li>Static initializer HB first use of class</li></ul>"),
     ("volatile","Guarantees: (1) reads/writes are atomic for long/double, (2) no caching in registers, "
      "(3) volatile write HB volatile read. Does NOT guarantee atomicity of compound operations (i++ is not atomic even on volatile).<br>"
      "<pre>volatile boolean running = true;\nvoid stop() { running = false; }  // immediately visible to reader thread</pre>"),
     ("Double-Checked Locking — Safe with volatile",
      "<pre>class Singleton {\n    private volatile static Singleton instance;\n    public static Singleton get() {\n        if (instance == null) {           // first check (no lock)\n            synchronized (Singleton.class) {\n                if (instance == null)     // second check (locked)\n                    instance = new Singleton();\n            }\n        }\n        return instance;\n    }\n}  // volatile prevents reordering of: alloc → init → assign</pre>"),
     ("Follow-ups",'<div class="followup">• Why was double-checked locking broken before Java 5?<br>'
      '• What is the difference between volatile and synchronized?<br>'
      '• How does final field guarantee visibility?</div>'))),

  ("jex018","HashMap vs LinkedHashMap vs TreeMap internals","java","collections","Medium",
   ["Amazon","Google","LinkedIn","Microsoft","TCS","Infosys","Oracle"],84,"hashmap,linkedhashmap,treemap,internals","Coding Round",
   A(("HashMap","Array of Node&lt;K,V&gt; buckets. Hash → index via <code>(n-1) &amp; hash</code>. "
      "Collision: linked list, then treeify at threshold 8 (TREEIFY_THRESHOLD). "
      "Resize (double) at 75% load factor. Java 8: balanced BST (TreeNode) for long chains."),
     ("LinkedHashMap","Extends HashMap. Adds doubly-linked list through all entries maintaining <b>insertion order</b>. "
      "Can be configured for <b>access order</b> (LRU behaviour) with constructor parameter.<br>"
      "<pre>// LRU Cache using LinkedHashMap\nMap&lt;K,V&gt; lru = new LinkedHashMap&lt;&gt;(16, 0.75f, true) {  // accessOrder=true\n    protected boolean removeEldestEntry(Map.Entry&lt;K,V&gt; e) {\n        return size() &gt; capacity;\n    }\n};</pre>"),
     ("TreeMap","Red-Black tree. Keys always <b>sorted</b> (natural order or Comparator). "
      "O(log n) get/put/remove. Extra operations: <code>floorKey</code>, <code>ceilingKey</code>, <code>headMap</code>, <code>tailMap</code>, <code>subMap</code>."),
     ("Quick Comparison",
      "<ul><li><b>HashMap:</b> O(1) avg, unordered, null key/values allowed</li>"
      "<li><b>LinkedHashMap:</b> O(1) avg, insertion/access ordered, LRU capable</li>"
      "<li><b>TreeMap:</b> O(log n), sorted, no null key</li></ul>"),
     ("Follow-ups",'<div class="followup">• What is HashMap\'s initial capacity and load factor trade-off?<br>'
      '• Why is String a good HashMap key? (immutable, cached hashCode)<br>'
      '• What causes ConcurrentModificationException?</div>'))),

  ("jex019","Spring Security — JWT authentication flow","java","spring","Hard",
   ["Amazon","LinkedIn","PayPal","Salesforce","Razorpay","CRED","PhonePe"],82,"spring-security,jwt,oauth2,authentication","Coding Round",
   A(("JWT Flow",
      "<pre>1. POST /login {username, password}\n2. Server validates credentials\n3. Server signs JWT: header.payload.signature (HMAC-SHA256 or RS256)\n4. Client stores JWT (HttpOnly cookie or memory — NOT localStorage)\n5. Client sends: Authorization: Bearer &lt;token&gt;\n6. Server: JwtFilter extracts token → validate signature + expiry\n          → set SecurityContextHolder with authentication\n7. Request proceeds to controller</pre>"),
     ("JWT Filter",
      "<pre>@Component\nclass JwtAuthFilter extends OncePerRequestFilter {\n    @Override\n    protected void doFilterInternal(HttpServletRequest req, ...) {\n        String token = extractToken(req);\n        if (token != null &amp;&amp; jwtUtil.validate(token)) {\n            UsernamePasswordAuthenticationToken auth =\n                new UsernamePasswordAuthenticationToken(\n                    jwtUtil.getUser(token), null,\n                    jwtUtil.getAuthorities(token));\n            SecurityContextHolder.getContext().setAuthentication(auth);\n        }\n        filterChain.doFilter(req, res);\n    }\n}</pre>"),
     ("JWT vs Sessions","<ul><li><b>JWT:</b> Stateless, scalable, no server-side storage. Con: can't invalidate before expiry.</li>"
      "<li><b>Session:</b> Server stores state, easy to invalidate. Con: sticky sessions or distributed session store needed.</li></ul>"),
     ("Refresh Tokens","Short-lived access token (15min) + long-lived refresh token (7d) stored in HttpOnly cookie. "
      "Refresh endpoint issues new access token without re-login."),
     ("Follow-ups",'<div class="followup">• How do you implement token blacklisting for logout?<br>'
      '• What is the difference between OAuth2 and JWT?<br>'
      '• What are the security risks of storing JWT in localStorage?</div>'))),

  ("jex020","Java GC algorithms — Mark-Sweep, Mark-Compact, Copying, Generational","java","jvm","Hard",
   ["Google","Amazon","Oracle","LinkedIn","Meta"],76,"gc-algorithms,mark-sweep,generational,gc","Coding Round",
   A(("Mark-Sweep","<b>Mark:</b> traverse GC roots, mark all reachable objects. "
      "<b>Sweep:</b> scan heap, free unmarked objects. Problem: <b>fragmentation</b> — free spaces scattered."),
     ("Mark-Compact","Mark phase same. Compact phase: slide all live objects to one end. No fragmentation. "
      "Slower than sweep (extra copy). G1GC uses this for selected regions."),
     ("Copying Collection","Divide heap into From/To spaces. Copy live objects to To, flip spaces. "
      "No fragmentation, fast allocation (bump pointer). Wastes 50% of heap. Used for young generation."),
     ("Generational Hypothesis","Most objects die young. Java heap split:<br>"
      "<ul><li><b>Young (Eden + 2 Survivors):</b> Minor GC — fast, copying collector</li>"
      "<li><b>Old (Tenured):</b> Major/Full GC — mark-compact or concurrent marking</li></ul>"
      "Promotion: object surviving N minor GCs (default 15) moves to Old gen."),
     ("G1GC","Divides heap into equal regions (~1-32MB). Marks concurrently. "
      "Selects regions with most garbage (Garbage-First) for collection. "
      "Pause target: <code>-XX:MaxGCPauseMillis=200</code>."),
     ("Follow-ups",'<div class="followup">• What triggers a Full GC and why is it bad?<br>'
      '• How does G1GC concurrent marking work alongside application threads?<br>'
      '• What is humongous object in G1GC?</div>'))),
]

def _to_dict(q):
    return {"id":q[0],"text":q[1],"category":q[2],"subcategory":q[3],"difficulty":q[4],
            "companies":q[5],"frequency":q[6],"tags":q[7].split(","),"round_type":q[8],"answer_hint":q[9]}

QUESTIONS = [_to_dict(q) for q in JAVA2]
