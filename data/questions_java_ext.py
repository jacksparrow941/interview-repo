"""Extended Java questions with full answers."""

_JAVA = ["Google","Amazon","LinkedIn","Microsoft","Meta","PayPal","Oracle","Salesforce","Infosys","TCS","Wipro"]

def A(*sections):
    parts = []
    for label, content in sections:
        parts.append(f'<span class="answer-label">{label}</span><br>{content}')
    return '<div class="answer-section">' + '</div><div class="answer-section" style="margin-top:10px">'.join(parts) + '</div>'

JAVA_EXT = [
  ("jex001","Java Virtual Threads (Project Loom, Java 21)","java","virtual-threads","Hard",
   ["Google","Amazon","LinkedIn","Microsoft","Meta","PayPal"],78,"virtual-threads,loom,project-loom","Coding Round",
   A(("Problem with Platform Threads","Java platform thread = OS thread. Creating 10,000 threads = 10,000 OS threads. "
      "Each uses ~1MB stack. I/O blocking wastes the OS thread."),
     ("Virtual Threads","Java 21 GA. Virtual threads are <b>JVM-managed, lightweight</b>. "
      "Mounted on platform threads (carrier threads) from a pool. "
      "On blocking I/O: JVM <b>unmounts</b> virtual thread, frees the carrier for others. Millions of VTs are feasible."),
     ("Usage",
      "<pre>// Simple\nThread.ofVirtual().start(() -> handleRequest());\n\n"
      "// With ExecutorService\ntry (var exec = Executors.newVirtualThreadPerTaskExecutor()) {\n"
      "    for (int i = 0; i &lt; 1_000_000; i++) {\n        exec.submit(this::handleRequest);\n    }\n}</pre>"),
     ("When to use","I/O-bound workloads (HTTP servers, DB queries). "
      "CPU-bound: still use platform threads or ForkJoinPool. "
      "Don't use <code>synchronized</code> blocks (causes carrier pinning) — use <code>ReentrantLock</code>."),
     ("Follow-ups",'<div class="followup">• What is thread pinning in virtual threads?<br>'
      '• How do structured concurrency (StructuredTaskScope) and virtual threads interact?<br>'
      '• Compare virtual threads to Kotlin coroutines and Go goroutines.</div>'))),

  ("jex002","Java Records — what are they and when to use?","java","java-records","Easy",
   ["Amazon","LinkedIn","Microsoft","Google","Meta","PayPal"],78,"records,immutable,data-classes","Coding Round",
   A(("Records (Java 16+)","Compact syntax for <b>immutable data carriers</b>. "
      "Compiler auto-generates: all-args constructor, getters, <code>equals()</code>, <code>hashCode()</code>, <code>toString()</code>."),
     ("Example",
      "<pre>// Old way (12 lines)\npublic final class Point {\n    private final int x, y;\n    public Point(int x, int y) { this.x=x; this.y=y; }\n    public int x() { return x; } public int y() { return y; }\n    // + equals, hashCode, toString...\n}\n\n// Record way (1 line!)\npublic record Point(int x, int y) {}\n\n// Usage\nPoint p = new Point(3, 4);\nSystem.out.println(p.x());  // 3\nSystem.out.println(p);      // Point[x=3, y=4]</pre>"),
     ("Restrictions","<ul><li>Fields are implicitly final (immutable)</li>"
      "<li>Cannot extend other classes (implicitly extends Record)</li>"
      "<li>Can implement interfaces</li>"
      "<li>Can add compact constructors, static methods, instance methods</li></ul>"),
     ("Use Cases","DTOs, value objects, API response/request types, configuration classes."),
     ("Follow-ups",'<div class="followup">• What is a compact constructor in records?<br>'
      '• How do records work with pattern matching (Java 21)?<br>'
      '• Records vs Lombok @Data — when to prefer which?</div>'))),

  ("jex003","Java Sealed Classes and Pattern Matching","java","language","Medium",
   ["Google","Amazon","LinkedIn","Meta"],72,"sealed,pattern-matching,switch","Coding Round",
   A(("Sealed Classes (Java 17+)","Restrict which classes can extend/implement a sealed class/interface. "
      "Enables exhaustive pattern matching in <code>switch</code>."),
     ("Example",
      "<pre>// Sealed hierarchy\npublic sealed interface Shape\n    permits Circle, Rectangle, Triangle {}\n\npublic record Circle(double radius) implements Shape {}\npublic record Rectangle(double w, double h) implements Shape {}\npublic record Triangle(double base, double height) implements Shape {}\n\n// Pattern matching switch (Java 21)\ndouble area = switch (shape) {\n    case Circle c -&gt; Math.PI * c.radius() * c.radius();\n    case Rectangle r -&gt; r.w() * r.h();\n    case Triangle t -&gt; 0.5 * t.base() * t.height();\n    // Compiler checks exhaustiveness — no default needed!\n};</pre>"),
     ("Benefits","<ul><li>Compiler ensures exhaustive handling (like Scala/Kotlin sealed)</li>"
      "<li>Eliminates <code>instanceof</code> chains</li>"
      "<li>ADT (Algebraic Data Type) support in Java</li></ul>"),
     ("Follow-ups",'<div class="followup">• How do sealed classes work with records?<br>'
      '• What is a guarded pattern? (<code>case Circle c when c.radius() &gt; 10</code>)<br>'
      '• Compare to Kotlin sealed classes.</div>'))),

  ("jex004","Spring WebFlux and Project Reactor — reactive programming","java","spring","Hard",
   ["Amazon","LinkedIn","PayPal","Oracle","Salesforce"],74,"webflux,reactor,mono,flux,reactive","Coding Round",
   A(("What is Reactive Programming","Non-blocking, event-driven programming with <b>backpressure</b>. "
      "Publisher emits data only as fast as subscriber can consume."),
     ("Project Reactor Types",
      "<ul><li><code>Mono&lt;T&gt;</code> — 0 or 1 element (like CompletableFuture)</li>"
      "<li><code>Flux&lt;T&gt;</code> — 0 to N elements (stream)</li></ul>"),
     ("Example",
      "<pre>// Blocking (Spring MVC)\n@GetMapping(\"/user/{id}\")\npublic User getUser(@PathVariable Long id) {\n    return userService.findById(id);  // blocks thread!\n}\n\n// Reactive (Spring WebFlux)\n@GetMapping(\"/user/{id}\")\npublic Mono&lt;User&gt; getUser(@PathVariable Long id) {\n    return userService.findById(id)  // non-blocking Mono\n        .map(UserDto::from)\n        .switchIfEmpty(Mono.error(new NotFoundException()));\n}</pre>"),
     ("When to use WebFlux",
      "<ul><li>High-concurrency I/O bound workloads (thousands of concurrent connections)</li>"
      "<li>Streaming data (SSE, WebSocket)</li>"
      "<li>Avoid: CPU-bound work, blocking libraries (use bounded elastic scheduler)</li></ul>"),
     ("Follow-ups",'<div class="followup">• What is the difference between publishOn and subscribeOn?<br>'
      '• How do you handle backpressure in Flux?<br>'
      '• When would you choose WebFlux over virtual threads (Java 21)?</div>'))),

  ("jex005","Hibernate L1 and L2 cache — how they work","java","jpa","Medium",
   ["Amazon","LinkedIn","PayPal","Oracle","Salesforce","Infosys"],76,"hibernate,cache,l1,l2,second-level","Database Round",
   A(("L1 Cache (Session Cache)","<b>Default, always on.</b> Scoped to a single <code>Session</code> (transaction). "
      "Within a session, the same entity loaded twice returns the same object (identity map). "
      "Cleared on <code>session.close()</code> or <code>session.clear()</code>."),
     ("L2 Cache (Shared Cache)","<b>Optional, cross-session.</b> Shared across all sessions in a SessionFactory. "
      "Must be explicitly configured. Providers: <b>Ehcache, Caffeine, Infinispan, Redis</b>."),
     ("L2 Setup",
      "<pre># application.properties\nspring.jpa.properties.hibernate.cache.use_second_level_cache=true\nspring.jpa.properties.hibernate.cache.region.factory_class=\\\n    org.hibernate.cache.jcache.JCacheRegionFactory\n\n# Entity\n@Entity\n@Cache(usage = CacheConcurrencyStrategy.READ_WRITE)\npublic class Product { ... }</pre>"),
     ("Query Cache","Cache for JPQL/HQL query results. Must also have L2 enabled. "
      "Stores primary keys, not entities. Invalidated when any entity in result changes."),
     ("Cache Strategies","READ_ONLY, NONSTRICT_READ_WRITE, READ_WRITE, TRANSACTIONAL"),
     ("Follow-ups",'<div class="followup">• When should you NOT use L2 cache?<br>'
      '• How does L2 cache handle cluster environments?<br>'
      '• What is the N+1 problem and how does @EntityGraph solve it?</div>'))),

  ("jex006","Java GC tuning — G1GC flags and when to use ZGC/Shenandoah","java","jvm","Hard",
   ["Google","Amazon","LinkedIn","Meta","Oracle"],74,"gc,g1gc,zgc,shenandoah,tuning","Coding Round",
   A(("G1GC (Default Java 9+)","Region-based collector. Divides heap into equal regions (~1-32MB). "
      "Concurrent marking + stop-the-world compaction of selected regions. "
      "Target: balance throughput with pause goals."),
     ("Key G1GC Flags",
      "<pre>-XX:+UseG1GC\n-Xms4g -Xmx4g              # fix heap size\n-XX:MaxGCPauseMillis=200   # target pause (default 200ms)\n-XX:G1HeapRegionSize=16m   # region size\n-XX:G1NewSizePercent=20    # young gen min %\n-XX:G1MaxNewSizePercent=40 # young gen max %\n-Xlog:gc*:file=gc.log      # GC logging</pre>"),
     ("ZGC (Java 21 — production ready)","Concurrent, scalable, <b>&lt;1ms pauses</b> regardless of heap size (even TBs). "
      "Uses colored pointers + load barriers. Ideal for latency-sensitive workloads.<br>"
      "<code>-XX:+UseZGC -XX:SoftMaxHeapSize=8g</code>"),
     ("Shenandoah","Similar to ZGC. Concurrent compaction. Used in OpenJDK builds.<br>"
      "<code>-XX:+UseShenandoahGC</code>"),
     ("When to choose",
      "<ul><li><b>G1GC:</b> Default, good balance, 100-200ms pauses acceptable</li>"
      "<li><b>ZGC/Shenandoah:</b> Latency-critical services (trading, real-time), &lt;10ms p99</li>"
      "<li><b>ParallelGC:</b> Batch processing, maximize throughput, pauses OK</li></ul>"),
     ("Follow-ups",'<div class="followup">• How do you identify GC pressure? (GC logs, JVM metrics)<br>'
      '• What is heap fragmentation and how does G1 handle it?<br>'
      '• What is GraalVM native image and how does it change GC?</div>'))),

  ("jex007","Java modules system (JPMS — Java 9+)","java","jvm","Medium",
   ["Google","Oracle","Amazon","LinkedIn"],68,"jpms,modules,module-info,encapsulation","Coding Round",
   A(("What is JPMS","Java Platform Module System (Java 9). Introduces strong encapsulation at the package level. "
      "Replaces classpath with modulepath. Eliminates split packages, illegal access."),
     ("module-info.java",
      "<pre>// com.myapp.service module\nmodule com.myapp.service {\n    requires java.net.http;       // depend on module\n    requires com.myapp.model;\n    exports com.myapp.service.api; // expose this package\n    exports com.myapp.service.impl to com.myapp.web; // targeted export\n    provides com.myapp.spi.Parser  // service provider\n        with com.myapp.service.impl.JsonParser;\n}</pre>"),
     ("Benefits","<ul><li>Strong encapsulation: internal packages hidden by default</li>"
      "<li>Reliable configuration: missing dependencies fail at startup, not runtime</li>"
      "<li>Smaller JVM images with <code>jlink</code></li></ul>"),
     ("Classpath vs Modulepath","Classpath: no encapsulation, all public APIs accessible. "
      "Modulepath: only exported packages visible. Automatic modules for legacy JARs."),
     ("Follow-ups",'<div class="followup">• What is <code>--add-opens</code> and when is it needed?<br>'
      '• How does jlink create a custom JRE?<br>'
      '• How do Spring Boot apps handle JPMS?</div>'))),

  ("jex008","CompletableFuture — common patterns and pitfalls","java","concurrency","Hard",
   ["Amazon","Google","LinkedIn","Microsoft","Meta","PayPal"],82,"completablefuture,async,compose,allof","Coding Round",
   A(("Key Methods",
      "<pre>// Chain\nCompletableFuture.supplyAsync(() -&gt; fetchUser(id))    // async supplier\n    .thenApply(user -&gt; enrichUser(user))              // transform (same thread)\n    .thenCompose(user -&gt; fetchOrders(user.id()))      // flatMap (new CF)\n    .thenAccept(System.out::println)                  // consume result\n    .exceptionally(ex -&gt; { log(ex); return null; })  // error handling</pre>"),
     ("Parallel execution",
      "<pre>var cfA = CompletableFuture.supplyAsync(() -&gt; callServiceA());\nvar cfB = CompletableFuture.supplyAsync(() -&gt; callServiceB());\n\n// Wait for both\nCompletableFuture.allOf(cfA, cfB).join();\n\n// Combine results\nvar result = cfA.thenCombine(cfB, (a, b) -&gt; merge(a, b));</pre>"),
     ("Common Pitfalls",
      "<ul><li><b>Default executor</b> is ForkJoinPool.commonPool() — shared, avoid for blocking I/O</li>"
      "<li>Always provide custom executor: <code>supplyAsync(() -&gt; ..., myExecutor)</code></li>"
      "<li>Unhandled exceptions in async chain silently swallowed — always add <code>exceptionally</code></li>"
      "<li><code>join()</code> vs <code>get()</code>: join throws unchecked, get throws checked</li></ul>"),
     ("Follow-ups",'<div class="followup">• Difference between thenApply, thenApplyAsync, thenCompose?<br>'
      '• How do you implement timeout in CompletableFuture?<br>'
      '• How does CompletableFuture compare to Mono/Flux?</div>'))),

  ("jex009","Spring Boot auto-configuration internals deep dive","java","spring","Hard",
   ["Amazon","LinkedIn","PayPal","Oracle","Salesforce"],76,"spring-boot,auto-config,conditional,bean","Coding Round",
   A(("How it works","<code>@SpringBootApplication</code> includes <code>@EnableAutoConfiguration</code>.<br>"
      "Spring Boot reads <code>META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports</code> "
      "(or legacy <code>spring.factories</code>) to find all <code>@AutoConfiguration</code> classes."),
     ("Conditional Annotations",
      "<ul><li><code>@ConditionalOnClass(DataSource.class)</code> — only if DataSource on classpath</li>"
      "<li><code>@ConditionalOnMissingBean</code> — only if no user-defined bean of that type</li>"
      "<li><code>@ConditionalOnProperty(\"spring.datasource.url\")</code> — only if property set</li>"
      "<li><code>@ConditionalOnWebApplication</code> — only in web context</li></ul>"),
     ("Example: DataSource auto-config",
      "<pre>@AutoConfiguration\n@ConditionalOnClass(DataSource.class)\n@ConditionalOnMissingBean(DataSource.class)\npublic class DataSourceAutoConfiguration {\n    @Bean\n    @ConditionalOnProperty(\"spring.datasource.url\")\n    public DataSource dataSource(DataSourceProperties props) {\n        return props.initializeDataSourceBuilder().build();\n    }\n}</pre>"),
     ("Debugging","<code>--debug</code> flag prints auto-config report: POSITIVE (matched) and NEGATIVE (not matched) conditions."),
     ("Follow-ups",'<div class="followup">• How do you exclude an auto-configuration?<br>'
      '• What is @ConfigurationProperties vs @Value?<br>'
      '• How does Spring Boot 3 change auto-configuration imports?</div>'))),

  ("jex010","Java Memory Leaks — common causes and detection","java","jvm","Medium",
   ["Amazon","Google","LinkedIn","Microsoft","Meta","TCS","Infosys"],80,"memory-leak,heap,jvm,profiling","Coding Round",
   A(("Common Causes",
      "<ul><li><b>Static references:</b> Static fields holding large objects or collections never GC'd</li>"
      "<li><b>ThreadLocal leak:</b> In thread pools, ThreadLocal not removed → memory leak per thread</li>"
      "<li><b>Listeners/callbacks:</b> Registered but never removed (event listeners, MBean)</li>"
      "<li><b>Unclosed resources:</b> Connection pools, file handles (use try-with-resources)</li>"
      "<li><b>Cache without eviction:</b> Unbounded HashMap growing forever</li>"
      "<li><b>ClassLoader leak:</b> Hot deployment in app servers — classloader + all loaded classes retained</li></ul>"),
     ("Detection Tools",
      "<ul><li><b>jmap -histo &lt;pid&gt;</b> — histogram of heap objects</li>"
      "<li><b>jmap -dump:format=b,file=heap.hprof &lt;pid&gt;</b> — heap dump</li>"
      "<li><b>Eclipse MAT / VisualVM</b> — analyze heap dump, find GC roots</li>"
      "<li><b>Java Flight Recorder (JFR) + JMC</b> — low-overhead production profiling</li>"
      "<li><b>async-profiler</b> — CPU and allocation profiling</li></ul>"),
     ("ThreadLocal Fix",
      "<pre>private static final ThreadLocal&lt;Context&gt; ctx = new ThreadLocal&lt;&gt;();\n\ntry {\n    ctx.set(new Context());\n    doWork();\n} finally {\n    ctx.remove();  // CRITICAL in thread pools!\n}</pre>"),
     ("Follow-ups",'<div class="followup">• What is a WeakHashMap and when does it help?<br>'
      '• How do you find the GC root of a retained object in MAT?<br>'
      '• What is heap fragmentation in old generation?</div>'))),
]

def _to_dict(q):
    return {
        "id": q[0], "text": q[1], "category": q[2], "subcategory": q[3],
        "difficulty": q[4], "companies": q[5], "frequency": q[6],
        "tags": q[7].split(","), "round_type": q[8], "answer_hint": q[9]
    }

QUESTIONS = [_to_dict(q) for q in JAVA_EXT]
