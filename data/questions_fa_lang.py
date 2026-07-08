"""Full answers for C++, Java, Go questions from questions_other.py."""

def A(*s):
    parts = [f'<span class="answer-label">{l}</span><br>{c}' for l,c in s]
    return '<div class="answer-section">'+'</div><div class="answer-section" style="margin-top:10px">'.join(parts)+'</div>'

FULL_ANSWERS_LANG = {

# ===== C++ =====

"cpp001": A(("Smart Pointer Types",
    "<ul><li><b>unique_ptr:</b> Exclusive ownership. Non-copyable, move-only. Zero overhead vs raw pointer. "
    "Use as default for heap objects.</li>"
    "<li><b>shared_ptr:</b> Shared ownership via reference count. Thread-safe refcount (atomic). "
    "Overhead: control block allocation + atomic ops.</li>"
    "<li><b>weak_ptr:</b> Non-owning observer of shared_ptr. Breaks circular references. "
    "Must <code>lock()</code> before use — returns shared_ptr (empty if object deleted).</li></ul>"),
  ("Code Examples",
    "<pre>auto up = std::make_unique&lt;Widget&gt;();     // unique_ptr\nauto sp = std::make_shared&lt;Widget&gt;();     // shared_ptr (single allocation)\nstd::weak_ptr&lt;Widget&gt; wp = sp;             // weak_ptr\nif (auto spt = wp.lock()) { spt-&gt;use(); } // safe access\n\n// Cycle breaking:\nstruct Node { std::weak_ptr&lt;Node&gt; parent; std::shared_ptr&lt;Node&gt; children; };</pre>"),
  ("Custom Deleter", "<code>unique_ptr&lt;FILE, decltype(&fclose)&gt; f(fopen(\"x\",\"r\"), fclose);</code>"),
  ("Follow-ups",'<div class="followup">• Why prefer make_shared over shared_ptr(new T)? (single allocation for object+control block)<br>'
    '• What is enable_shared_from_this and when do you need it?<br>'
    '• When would you still use a raw pointer?</div>')),

"cpp002": A(("RAII — Resource Acquisition Is Initialization",
    "Resource lifetime is bound to object lifetime. Acquire in constructor, release in destructor. "
    "Guarantees release even on exceptions (stack unwinding calls destructors)."),
  ("Examples",
    "<pre>class FileGuard {\n    FILE* f;\npublic:\n    explicit FileGuard(const char* path) : f(fopen(path, \"r\")) {\n        if (!f) throw std::runtime_error(\"open failed\");\n    }\n    ~FileGuard() { if (f) fclose(f); }  // always runs\n    // Delete copy; use move only\n    FileGuard(const FileGuard&) = delete;\n    FileGuard& operator=(const FileGuard&) = delete;\n};\n\n// RAII wrappers: lock_guard, unique_lock, ifstream, unique_ptr, jthread</pre>"),
  ("Why it matters",
    "Without RAII: every error path must manually release resources → leak-prone. "
    "With RAII: destructor always called → exception-safe, leak-free."),
  ("Follow-ups",'<div class="followup">• How does RAII differ from finally blocks in Java/Python?<br>'
    '• What is the ScopeGuard pattern?<br>'
    '• How does RAII interact with noexcept?</div>')),

"cpp003": A(("Move Semantics",
    "C++11 introduces rvalue references (<code>T&&</code>). Move constructor/assignment <b>steals</b> resources from temporaries "
    "instead of copying. Enables zero-cost transfer of ownership."),
  ("Rvalue References",
    "<pre>class Buffer {\n    int* data; size_t size;\npublic:\n    Buffer(Buffer&& other) noexcept :  // move constructor\n        data(other.data), size(other.size) {\n        other.data = nullptr; other.size = 0;  // leave source valid but empty\n    }\n    Buffer& operator=(Buffer&& other) noexcept {\n        if (this != &other) {\n            delete[] data;          // free own resource\n            data = other.data; size = other.size;\n            other.data = nullptr; other.size = 0;\n        } return *this;\n    }\n};\n\nvoid process(Buffer&& b) { Buffer local = std::move(b); } // move, not copy\nBuffer create() { Buffer b(1024); return b; }  // NRVO: no copy at all!</pre>"),
  ("std::move vs std::forward",
    "<code>std::move(x)</code>: unconditional cast to rvalue. "
    "<code>std::forward&lt;T&gt;(x)</code>: conditional — preserves lvalue/rvalue category in template (perfect forwarding)."),
  ("Follow-ups",'<div class="followup">• When should a move constructor be noexcept? (essential for vector reallocation to use moves)<br>'
    '• What is the moved-from state guarantee?<br>'
    '• What is the difference between universal reference and rvalue reference?</div>')),

"cpp005": A(("vtable Mechanism",
    "For each class with virtual functions, compiler generates a <b>vtable</b> — a static array of function pointers. "
    "Each object has a hidden <b>vptr</b> pointing to its class's vtable (set in constructor)."),
  ("Virtual Dispatch",
    "<pre>class Animal {\npublic:\n    virtual void sound() { printf(\"...\"); }\n    virtual ~Animal() {}\n};\n// vtable_Animal = { &Animal::sound, &Animal::~Animal }\n\nclass Dog : public Animal {\n    void sound() override { printf(\"Bark\"); }\n};\n// vtable_Dog = { &Dog::sound, &Dog::~Dog }\n\nAnimal* a = new Dog();\na-&gt;sound();  // a-&gt;vptr -&gt; vtable_Dog[0] = Dog::sound() → \"Bark\"</pre>"),
  ("Costs",
    "<ul><li>Memory: 1 vptr per object (8 bytes on 64-bit)</li>"
    "<li>Time: extra pointer indirection per call (cache miss possible)</li>"
    "<li>No inlining: compiler can't inline virtual calls (mostly)</li>"
    "<li>Final keyword: hints compiler to devirtualize</li></ul>"),
  ("Follow-ups",'<div class="followup">• What is devirtualization and when does the compiler perform it?<br>'
    '• How does CRTP achieve static polymorphism without vtable overhead?<br>'
    '• Why is virtual destructor needed in base classes?</div>')),

"cpp006": A(("std::atomic",
    "Guarantees atomic read-modify-write without undefined behavior. No data races. Hardware CAS instructions."),
  ("Memory Ordering",
    "<ul><li><b>relaxed:</b> No ordering guarantees. Only atomicity. Cheapest. Use for counters.</li>"
    "<li><b>acquire:</b> All subsequent reads see writes before the release on same var. (read fence)</li>"
    "<li><b>release:</b> All preceding writes visible to acquire on same var. (write fence)</li>"
    "<li><b>acq_rel:</b> Both acquire + release. Used for RMW operations.</li>"
    "<li><b>seq_cst:</b> Total global order. Strongest guarantee. Default for atomic ops.</li></ul>"),
  ("Usage",
    "<pre>std::atomic&lt;int&gt; counter{0};\ncounter.fetch_add(1, std::memory_order_relaxed);  // fast counter\n\nstd::atomic&lt;bool&gt; ready{false};\n// Thread 1:\ndata = 42;\nready.store(true, std::memory_order_release);\n// Thread 2:\nwhile (!ready.load(std::memory_order_acquire));  // guaranteed to see data=42</pre>"),
  ("Follow-ups",'<div class="followup">• What is a data race vs a race condition?<br>'
    '• When is relaxed ordering safe?<br>'
    '• What is the ABA problem in CAS-based algorithms?</div>')),

"cpp012": A(("std::vector Growth",
    "When capacity is exceeded, vector allocates new buffer (typically 2× current capacity), "
    "moves all elements, then deallocates old buffer. Amortized O(1) push_back."),
  ("Internals",
    "<pre>struct vector_internals {\n    T* begin;    // pointer to first element\n    T* end;      // pointer past last element (size)\n    T* cap_end;  // pointer to end of allocation (capacity)\n};\n// size() = end - begin\n// capacity() = cap_end - begin</pre>"),
  ("Important APIs",
    "<ul><li><code>reserve(n)</code>: pre-allocate without changing size. Prevents reallocations.</li>"
    "<li><code>shrink_to_fit()</code>: release excess capacity (non-binding request).</li>"
    "<li><code>emplace_back(args)</code>: construct in-place, avoids extra copy/move.</li></ul>"),
  ("Follow-ups",'<div class="followup">• Why does push_back invalidate iterators? (reallocation moves all elements)<br>'
    '• What is the growth factor trade-off (2x vs 1.5x)?<br>'
    '• How does vector differ from deque in terms of memory layout?</div>')),

# ===== JAVA =====

"j001": A(("JVM Memory Areas",
    "<ul><li><b>Heap:</b> All objects (new). Divided into Young (Eden + 2 Survivors) + Old/Tenured. GC managed.</li>"
    "<li><b>Stack:</b> Per-thread. Holds stack frames: local variables, operand stack, method calls. Fixed size (typically 512KB-1MB). StackOverflowError if exceeded.</li>"
    "<li><b>Metaspace (Java 8+):</b> Class metadata (class bytecode, method data). Native memory, grows dynamically. "
    "Replaced PermGen which had fixed max size.</li>"
    "<li><b>Code Cache:</b> JIT-compiled native code.</li>"
    "<li><b>Direct Memory:</b> Off-heap via NIO ByteBuffer.allocateDirect(). Not GC'd, must be freed explicitly.</li></ul>"),
  ("Tuning Flags",
    "<pre>-Xms512m -Xmx4g       # initial and max heap\n-XX:MetaspaceSize=256m # initial metaspace\n-XX:MaxMetaspaceSize=512m\n-Xss512k               # thread stack size</pre>"),
  ("Follow-ups",'<div class="followup">• What causes OutOfMemoryError in heap vs metaspace vs direct memory?<br>'
    '• What is object header size in JVM? (12-16 bytes: mark word + klass pointer)<br>'
    '• How does compressed OOPs affect memory usage?</div>')),

"j003": A(("HashMap Internals",
    "<pre>// Java 8+ structure:\n// Node&lt;K,V&gt;[] table  (array of buckets, power of 2 size)\n// Each bucket: null | Node (linked list) | TreeNode (red-black tree)\n\n// Hash calculation:\nstatic int hash(Object key) {\n    int h;\n    return (key == null) ? 0 : (h = key.hashCode()) ^ (h &gt;&gt;&gt; 16);\n    // XOR high bits into low bits — better distribution\n}\n// Bucket index: (n-1) &amp; hash  (n = table length, power of 2)</pre>"),
  ("Thresholds",
    "<ul><li><b>TREEIFY_THRESHOLD = 8:</b> Bucket with &gt;8 nodes → convert to red-black tree (O(log n) per op)</li>"
    "<li><b>UNTREEIFY_THRESHOLD = 6:</b> Tree shrinks back to list on removal</li>"
    "<li><b>LOAD_FACTOR = 0.75:</b> Resize (double) when size/capacity &gt; 0.75</li></ul>"),
  ("Thread Safety", "HashMap is NOT thread-safe. Use ConcurrentHashMap (lock-striping, CAS) or Collections.synchronizedMap() (coarse lock)."),
  ("Follow-ups",'<div class="followup">• What is the time complexity of get() in worst case? O(log n) with tree buckets<br>'
    '• Why XOR high bits into low bits in hash()? (prevents collision when table size is small)<br>'
    '• What is the difference between HashMap.keySet() and EntrySet iteration performance?</div>')),

"j005": A(("Java Memory Model (JMM) Happens-Before",
    "If action A happens-before B, then A's writes are visible to B. Established by:<br>"
    "<ul><li>Monitor unlock happens-before lock by any thread</li>"
    "<li>volatile write happens-before volatile read of same field</li>"
    "<li>Thread.start() happens-before all actions in started thread</li>"
    "<li>Thread.join() happens-before all actions after join returns</li>"
    "<li>Program order within single thread</li></ul>"),
  ("volatile vs synchronized",
    "<ul><li><b>volatile:</b> Visibility + ordering for single variable. No atomicity for compound ops (i++ is not atomic).</li>"
    "<li><b>synchronized:</b> Mutual exclusion + full memory visibility. Heavier.</li>"
    "<li><b>Atomic classes:</b> CAS-based, lock-free, best for single variable atomic operations.</li></ul>"),
  ("Follow-ups",'<div class="followup">• Why does double-checked locking need volatile? (prevents reordering of new T() allocation vs pointer assignment)<br>'
    '• What is a publication failure and how does final field guarantee prevent it?<br>'
    '• What is memory_order in C++ and how does it map to JMM concepts?</div>')),

"j007": A(("CompletableFuture vs Future",
    "<ul><li><b>Future.get():</b> Blocking. No composition. No exception handling except checked exceptions.</li>"
    "<li><b>CompletableFuture:</b> Non-blocking. Rich composition API. Exception handling. Async pipelines.</li></ul>"),
  ("Key APIs",
    "<pre>CompletableFuture.supplyAsync(() -&gt; fetchUser(id))     // run async\n    .thenApplyAsync(user -&gt; fetchOrders(user))          // chain\n    .thenCombine(fetchInventory(), (orders, inv) -&gt; merge(orders, inv)) // combine 2\n    .exceptionally(ex -&gt; defaultOrders())              // handle error\n    .thenAccept(result -&gt; render(result))               // consume\n    .orTimeout(5, TimeUnit.SECONDS)                     // timeout\n    .get();\n\n// Wait for all:\nCompletableFuture.allOf(cf1, cf2, cf3).join();\n// First to complete:\nCompletableFuture.anyOf(cf1, cf2, cf3).join();</pre>"),
  ("Thread Pool",
    "Uses ForkJoinPool.commonPool() by default. Pass custom executor for IO-heavy tasks: "
    "<code>supplyAsync(() -&gt; ..., ioThreadPool)</code>"),
  ("Follow-ups",'<div class="followup">• What is the difference between thenApply vs thenApplyAsync?<br>'
    '• How does CompletableFuture handle exceptions in chained stages?<br>'
    '• How does Project Loom virtual threads change CompletableFuture usage?</div>')),

"j013": A(("ExecutorService Types",
    "<pre>Executors.newFixedThreadPool(10)       // fixed N threads, unbounded queue (DANGEROUS!)\nExecutors.newCachedThreadPool()        // grows/shrinks, no queue — risky under load\nExecutors.newSingleThreadExecutor()    // 1 thread, sequential, unbounded queue\nExecutors.newScheduledThreadPool(2)    // for delayed / periodic tasks\nForkJoinPool.commonPool()             // work-stealing, for parallel streams\n\n// RECOMMENDED:\nnew ThreadPoolExecutor(core, max, keepAlive, unit, new ArrayBlockingQueue&lt;&gt;(1000),\n    new ThreadPoolExecutor.CallerRunsPolicy());  // bounded queue + backpressure</pre>"),
  ("Lifecycle",
    "<pre>ExecutorService ex = Executors.newFixedThreadPool(4);\ntry {\n    ex.submit(task1); ex.submit(task2);\n} finally {\n    ex.shutdown();                          // stop accepting new tasks\n    if (!ex.awaitTermination(60, SECONDS))\n        ex.shutdownNow();                   // cancel running tasks\n}</pre>"),
  ("Follow-ups",'<div class="followup">• Why is newFixedThreadPool dangerous? (unbounded LinkedBlockingQueue can OOM)<br>'
    '• What is the difference between submit() and execute()?<br>'
    '• How does ForkJoinPool differ from ThreadPoolExecutor?</div>')),

# ===== GO =====

"g001": A(("Goroutines vs OS Threads",
    "<ul><li><b>Goroutine:</b> ~2KB initial stack (grows dynamically to hundreds of MB if needed). "
    "M:N threading — N goroutines multiplexed onto M OS threads. Scheduled by Go runtime.</li>"
    "<li><b>OS Thread:</b> ~1MB stack (fixed at creation). 1:1 with kernel thread. Expensive context switch (μs).</li>"
    "<li>Can run millions of goroutines. Thousands of OS threads = OOM.</li></ul>"),
  ("GMP Model (brief)",
    "<ul><li><b>G:</b> Goroutine (the task)</li>"
    "<li><b>M:</b> OS thread (the runner)</li>"
    "<li><b>P:</b> Processor/scheduler context (GOMAXPROCS Ps). Each P has local run queue.</li>"
    "<li>When G blocks on syscall → M + G detach from P → P gets another M to continue work</li></ul>"),
  ("Follow-ups",'<div class="followup">• What is goroutine stack growth mechanism? (segmented stacks → copying stacks since Go 1.4)<br>'
    '• What is GOMAXPROCS and when would you change it?<br>'
    '• How do goroutines avoid the 10K thread problem?</div>')),

"g003": A(("Buffered vs Unbuffered Channels",
    "<ul><li><b>Unbuffered <code>make(chan T)</code>:</b> Sender blocks until receiver is ready. "
    "Receiver blocks until sender sends. Strict synchronization point (rendezvous).</li>"
    "<li><b>Buffered <code>make(chan T, n)</code>:</b> Sender blocks only when buffer full. "
    "Receiver blocks only when buffer empty. Decouples send and receive timing.</li></ul>"),
  ("Usage Patterns",
    "<pre>// Semaphore (limit concurrency to 5):\nsem := make(chan struct{}, 5)\nfor _, job := range jobs {\n    sem &lt;- struct{}{}  // acquire\n    go func(j Job) {\n        defer func() { &lt;-sem }()  // release\n        process(j)\n    }(job)\n}\n\n// Signal (done channel):\ndone := make(chan struct{})\ngo func() { defer close(done); doWork() }()\n&lt;-done  // wait for completion</pre>"),
  ("Closing Channels","Only sender should close. Closing a closed channel panics. "
    "Reading from closed channel returns zero value + false: <code>v, ok := &lt;-ch; if !ok { // closed }</code>"),
  ("Follow-ups",'<div class="followup">• What happens if you send to a nil channel? (blocks forever)<br>'
    '• How do you implement a timeout using select?<br>'
    '• What is the difference between closing a channel and sending a sentinel value?</div>')),

"g005": A(("context.Context Usage",
    "<pre>// HTTP server: request context already has deadline\nfunc handleRequest(w http.ResponseWriter, r *http.Request) {\n    ctx := r.Context()  // already has connection lifetime context\n    ctx, cancel := context.WithTimeout(ctx, 5*time.Second)\n    defer cancel()  // ALWAYS defer cancel to free resources\n    \n    result, err := db.QueryContext(ctx, query)  // cancelled if handler times out\n    ...\n}</pre>"),
  ("WithValue Best Practices",
    "<pre>type contextKey struct{}  // unexported type prevents collisions\ntype userKey struct{}\n\nctx = context.WithValue(ctx, userKey{}, &amp;User{ID: 42})\n\n// Retrieve:\nif user, ok := ctx.Value(userKey{}).(*User); ok {\n    // use user\n}</pre>"),
  ("Propagation","Always pass ctx as first parameter. Never store context in struct fields. "
    "Never pass nil context (use context.TODO() or context.Background() as root)."),
  ("Follow-ups",'<div class="followup">• What is the difference between context.Background() and context.TODO()?<br>'
    '• What happens when a parent context is cancelled? (all child contexts are also cancelled)<br>'
    '• How do you implement a context-aware sleep?</div>')),

"g008": A(("sync.Mutex vs sync.RWMutex",
    "<ul><li><b>sync.Mutex:</b> Exclusive lock. One goroutine at a time (readers OR writer).</li>"
    "<li><b>sync.RWMutex:</b> Multiple concurrent readers OR one exclusive writer. "
    "Writers must wait for all readers. Readers don't block each other. "
    "Great for read-heavy workloads (config, caches).</li></ul>"),
  ("Code",
    "<pre>type SafeMap struct {\n    mu   sync.RWMutex\n    data map[string]string\n}\nfunc (m *SafeMap) Get(key string) string {\n    m.mu.RLock()         // shared read lock\n    defer m.mu.RUnlock()\n    return m.data[key]\n}\nfunc (m *SafeMap) Set(key, val string) {\n    m.mu.Lock()          // exclusive write lock\n    defer m.mu.Unlock()\n    m.data[key] = val\n}</pre>"),
  ("When RWMutex hurts","RWMutex adds overhead for writer starvation prevention. "
    "If writes are frequent, plain Mutex is faster. Profile before switching."),
  ("Follow-ups",'<div class="followup">• What is writer starvation in RWMutex and how does Go prevent it?<br>'
    '• How does sync.Map differ from RWMutex-protected map? (optimized for append-only + stable key sets)<br>'
    '• What is the copy-on-write pattern for read-heavy data structures?</div>')),

"g009": A(("Go Interfaces",
    "Interfaces are <b>implicitly satisfied</b> — no <code>implements</code> keyword. "
    "Any type implementing all methods of an interface satisfies it automatically."),
  ("Interface Internal Representation",
    "<pre>// Interface value = (type pointer, value pointer)\nvar w io.Writer                 // nil interface: (nil, nil)\nw = os.Stdout                  // (*os.File, ptr to Stdout)\n\n// nil trap:\nvar f *os.File = nil\nvar r io.Reader = f            // (type=*os.File, value=nil) ← NOT nil interface!\nfmt.Println(r == nil)          // false! Type is set.\n\n// Fix:\nif f == nil { var r io.Reader = nil }  // assign nil interface explicitly</pre>"),
  ("Empty Interface", "<code>interface{}</code> or <code>any</code> (Go 1.18+) holds any value. "
    "Use type assertions (<code>v.(string)</code>) or type switch to extract."),
  ("Follow-ups",'<div class="followup">• What is the difference between nil pointer and nil interface?<br>'
    '• How does type assertion differ from type switch?<br>'
    '• What is interface pollution and how do you avoid it? (accept interfaces, return concrete types)</div>')),
}
