"""Go Extended Part 2 — scheduler deep dive, defer/panic/recover, channels, functional options, atomic."""

_GO = ["Google","Uber","Razorpay","Swiggy","Zomato","CRED","Dream11","Coinbase","BrowserStack","Stripe"]

def A(*s):
    parts = [f'<span class="answer-label">{l}</span><br>{c}' for l,c in s]
    return '<div class="answer-section">'+'</div><div class="answer-section" style="margin-top:10px">'.join(parts)+'</div>'

GO2 = [
  ("gex011","Go GMP scheduler — deep dive (G, M, P, work stealing)","go","runtime","Hard",
   ["Google","Uber","Razorpay","CRED"],74,"gmp,scheduler,goroutine,work-stealing","Coding Round",
   A(("GMP Model",
      "<ul><li><b>G (Goroutine):</b> Lightweight coroutine. ~2KB initial stack, grows dynamically. Millions possible.</li>"
      "<li><b>M (Machine/Thread):</b> OS thread. One M executes one G at a time. Limited by GOMAXPROCS for Go code; "
      "more Ms created for blocking syscalls.</li>"
      "<li><b>P (Processor):</b> Scheduling context. GOMAXPROCS Ps (default = CPU cores). Each P has a local run queue (LRQ) of Gs.</li></ul>"),
     ("Scheduling Flow",
      "<pre>1. goroutine created → added to P's LRQ\n2. P pops G from LRQ, assigns to M → runs\n3. G blocks on syscall → M + G detached from P\n   → P finds idle M (or creates new) → continues running other Gs\n4. Syscall completes → G goes back to global run queue (GRQ)\n5. Work stealing: idle P steals half of busy P's LRQ → balanced load</pre>"),
     ("Preemption","Go uses cooperative preemption (yield at function calls) + async preemption (sysmon thread "
      "sends SIGURG after 10ms to interrupt G). Long CPU-bound goroutines preempted automatically."),
     ("GOMAXPROCS","Number of OS threads for Go code = number of Ps. "
      "<code>runtime.GOMAXPROCS(n)</code> or <code>GOMAXPROCS=n</code> env var."),
     ("Follow-ups",'<div class="followup">• What is the global run queue and why is it checked periodically?<br>'
      '• How does network I/O avoid blocking M? (netpoller + epoll)<br>'
      '• What is sysmon goroutine and what does it do?</div>'))),

  ("gex012","defer, panic, recover — full semantics and patterns","go","language","Medium",
   _GO, 88, "defer,panic,recover,error-handling","Coding Round",
   A(("defer","Deferred call runs when surrounding function returns (normal or panic). "
      "Arguments evaluated immediately; call deferred. LIFO order.<br>"
      "<pre>func processFile(path string) (err error) {\n    f, err := os.Open(path)\n    if err != nil { return }\n    defer f.Close()           // runs even on early return/panic\n    defer func() {            // named return: modify err on cleanup failure\n        if cerr := f.Close(); cerr != nil &amp;&amp; err == nil {\n            err = cerr\n        }\n    }()\n    // ... process f\n    return\n}</pre>"),
     ("panic / recover",
      "<pre>func safeDiv(a, b int) (result int, err error) {\n    defer func() {\n        if r := recover(); r != nil {     // recover() catches panic\n            err = fmt.Errorf(\"panic: %v\", r)\n        }\n    }()\n    return a / b, nil  // panics if b==0\n}\n\n// recover() returns nil if no panic, or the panic value\n// ONLY works inside a deferred function</pre>"),
     ("Rules",
      "<ul><li><code>recover()</code> only stops a panic if called directly from a deferred function</li>"
      "<li>Panic unwinds stack, running deferred functions</li>"
      "<li>Use panic for truly unrecoverable states (programming errors), not business logic</li>"
      "<li>HTTP handlers should recover panics to avoid crashing the whole server</li></ul>"),
     ("Follow-ups",'<div class="followup">• What is the difference between os.Exit and panic?<br>'
      '• Can you defer a method call? (yes)<br>'
      '• What is the defer overhead? (small but measurable in hot loops)</div>'))),

  ("gex013","Channel patterns — fan-out, fan-in, pipeline, done channel","go","concurrency","Hard",
   _GO, 84, "channels,pipeline,fan-out,fan-in,done","Concurrency Round",
   A(("Pipeline",
      "<pre>func gen(nums ...int) &lt;-chan int {\n    out := make(chan int)\n    go func() {\n        defer close(out)\n        for _, n := range nums { out &lt;- n }\n    }()\n    return out\n}\nfunc sq(in &lt;-chan int) &lt;-chan int {\n    out := make(chan int)\n    go func() { defer close(out); for n := range in { out &lt;- n*n } }()\n    return out\n}\n// Usage: for v := range sq(sq(gen(2,3,4))) { fmt.Println(v) }</pre>"),
     ("Fan-Out",
      "<pre>func fanOut(in &lt;-chan int, workers int) []&lt;-chan int {\n    outs := make([]&lt;-chan int, workers)\n    for i := range outs {\n        outs[i] = sq(in)  // each worker reads from same input\n    }\n    return outs\n}</pre>"),
     ("Fan-In (Merge)",
      "<pre>func merge(cs ...&lt;-chan int) &lt;-chan int {\n    var wg sync.WaitGroup\n    out := make(chan int)\n    output := func(c &lt;-chan int) {\n        defer wg.Done()\n        for v := range c { out &lt;- v }\n    }\n    wg.Add(len(cs))\n    for _, c := range cs { go output(c) }\n    go func() { wg.Wait(); close(out) }()\n    return out\n}</pre>"),
     ("Done Channel (Cancellation)",
      "<pre>func sq(done &lt;-chan struct{}, in &lt;-chan int) &lt;-chan int {\n    out := make(chan int)\n    go func() {\n        defer close(out)\n        for n := range in {\n            select {\n            case out &lt;- n*n:\n            case &lt;-done: return  // cancelled\n            }\n        }\n    }()\n    return out\n}\n// Use context.Context in production instead of done channel</pre>"),
     ("Follow-ups",'<div class="followup">• How does context.Context replace the done channel pattern?<br>'
      '• What is channel direction (&lt;-chan vs chan&lt;-) and why does it matter?<br>'
      '• How do you implement a timeout with select?</div>'))),

  ("gex014","Functional options pattern in Go","go","patterns","Medium",
   _GO, 80, "functional-options,design-pattern,configuration","Coding Round",
   A(("Problem","How to provide optional configuration to a constructor without breaking API as options grow? "
      "Config structs are verbose; many parameters are messy."),
     ("Functional Options Pattern",
      "<pre>type Server struct {\n    host    string\n    port    int\n    timeout time.Duration\n    maxConn int\n}\n\ntype Option func(*Server)\n\nfunc WithPort(p int) Option      { return func(s *Server) { s.port = p } }\nfunc WithTimeout(d time.Duration) Option { return func(s *Server) { s.timeout = d } }\nfunc WithMaxConn(n int) Option   { return func(s *Server) { s.maxConn = n } }\n\nfunc NewServer(host string, opts ...Option) *Server {\n    s := &amp;Server{host: host, port: 8080, timeout: 30*time.Second, maxConn: 100}  // defaults\n    for _, opt := range opts { opt(s) }\n    return s\n}\n\n// Usage (clean, readable, extensible):\nsrv := NewServer(\"localhost\",\n    WithPort(9090),\n    WithTimeout(5*time.Second),\n)</pre>"),
     ("Advantages","<ul><li>Backward compatible — add new options without changing signature</li>"
      "<li>Self-documenting call sites</li>"
      "<li>Easy to set sensible defaults</li>"
      "<li>Options are first-class values — can be composed, stored, passed around</li></ul>"),
     ("Follow-ups",'<div class="followup">• How does this pattern compare to Builder pattern?<br>'
      '• What is the Rob Pike option pattern variation?<br>'
      '• How would you validate option values?</div>'))),

  ("gex015","sync/atomic — atomic operations and lock-free patterns","go","concurrency","Hard",
   ["Google","Uber","Razorpay","CRED","Stripe"],76,"atomic,lock-free,cas,atomic-value","Concurrency Round",
   A(("Basic Operations",
      "<pre>var counter int64\natomic.AddInt64(&amp;counter, 1)         // atomic increment\nval := atomic.LoadInt64(&amp;counter)    // atomic read\natomic.StoreInt64(&amp;counter, 100)     // atomic write\n\n// Compare-and-swap: set if current == expected\nold := atomic.LoadInt64(&amp;counter)\nswapped := atomic.CompareAndSwapInt64(&amp;counter, old, old+1)</pre>"),
     ("atomic.Value — lock-free config reload",
      "<pre>var config atomic.Value  // stores any comparable type\n\n// Writer (rare):\nconfig.Store(&amp;Config{MaxConns: 100, Timeout: 5*time.Second})\n\n// Readers (concurrent, zero contention):\ncfg := config.Load().(*Config)\n// cfg is safe to use — immutable snapshot</pre>"),
     ("Lock-free counter",
      "<pre>type Counter struct { n int64 }\nfunc (c *Counter) Inc() { atomic.AddInt64(&amp;c.n, 1) }\nfunc (c *Counter) Get() int64 { return atomic.LoadInt64(&amp;c.n) }\n// 10x faster than mutex for simple counter</pre>"),
     ("When to use","<ul><li>Single shared counter/flag with simple reads/writes → atomic</li>"
      "<li>Immutable config reload → atomic.Value</li>"
      "<li>Complex invariants across multiple fields → mutex</li></ul>"),
     ("Follow-ups",'<div class="followup">• What is the ABA problem in CAS-based algorithms?<br>'
      '• How does atomic.Pointer (Go 1.19) differ from atomic.Value?<br>'
      '• Why can\'t you use atomic for structs with multiple fields?</div>'))),

  ("gex016","Go interface composition and embedding","go","language","Medium",
   _GO, 80, "interface,embedding,composition,mixin","Coding Round",
   A(("Interface Composition",
      "<pre>type Reader interface { Read(p []byte) (n int, err error) }\ntype Writer interface { Write(p []byte) (n int, err error) }\ntype Closer interface { Close() error }\n\n// Compose interfaces:\ntype ReadWriter interface { Reader; Writer }  // embeds both\ntype ReadWriteCloser interface { ReadWriter; Closer }\n\n// io.ReadWriteCloser = standard library example\n// os.File implements ReadWriteCloser</pre>"),
     ("Struct Embedding",
      "<pre>type Animal struct { Name string }\nfunc (a Animal) Speak() string { return a.Name + \" speaks\" }\n\ntype Dog struct {\n    Animal          // embedded — promotes fields and methods\n    Breed string\n}\n\nd := Dog{Animal{\"Rex\"}, \"Labrador\"}\nfmt.Println(d.Speak())  // promoted method: Dog.Speak() = Animal.Speak()\nfmt.Println(d.Name)     // promoted field</pre>"),
     ("Override via Shadowing",
      "<pre>func (d Dog) Speak() string { return d.Name + \" barks\" }  // shadows Animal.Speak\nd.Speak()         // calls Dog.Speak\nd.Animal.Speak()  // explicitly call embedded method</pre>"),
     ("Interface Satisfaction","A type satisfies an interface if it implements all its methods. "
      "Embedding helps: if Dog embeds Animal, Dog gets Animal's methods → may satisfy interfaces automatically."),
     ("Follow-ups",'<div class="followup">• What is the difference between embedding and inheritance?<br>'
      '• Can you embed interfaces in structs? (yes — useful for partial mocking in tests)<br>'
      '• What happens if two embedded types have the same method name?</div>'))),

  ("gex017","Go context package — propagation, timeout, cancellation","go","patterns","Medium",
   _GO, 90, "context,cancellation,timeout,propagation","Coding Round",
   A(("Context Tree",
      "<pre>// Root\nctx := context.Background()\n\n// Cancellable\nctx, cancel := context.WithCancel(ctx)\ndefer cancel()  // always call cancel to free resources\n\n// With timeout\nctx, cancel = context.WithTimeout(ctx, 5*time.Second)\ndefer cancel()\n\n// With deadline\nctx, cancel = context.WithDeadline(ctx, time.Now().Add(5*time.Second))\n\n// With value (carry request-scoped data)\nctx = context.WithValue(ctx, userKey{}, user)</pre>"),
     ("Checking cancellation",
      "<pre>func doWork(ctx context.Context) error {\n    for {\n        select {\n        case &lt;-ctx.Done():\n            return ctx.Err()  // context.Canceled or DeadlineExceeded\n        case result := &lt;-workChan:\n            process(result)\n        }\n    }\n}</pre>"),
     ("Propagation","Always pass context as <b>first parameter</b>. Context propagates cancellation to all child contexts automatically."),
     ("context.Value best practices","<ul><li>Use only for request-scoped data: traceID, userID, auth token</li>"
      "<li>Use unexported key types to avoid collisions: <code>type ctxKey struct{}</code></li>"
      "<li>Never store mutable data in context values</li></ul>"),
     ("Follow-ups",'<div class="followup">• What is context.TODO() vs context.Background()?<br>'
      '• How does HTTP server set request context with timeout?<br>'
      '• What happens if you cancel a parent context?</div>'))),

  ("gex018","Go memory escape analysis and optimization","go","performance","Hard",
   ["Google","Uber","Razorpay","CRED"],74,"escape-analysis,stack,heap,allocation","Coding Round",
   A(("Escape Analysis","Go compiler determines at compile time whether a variable can live on the stack "
      "(cheap, GC-free) or must escape to the heap (GC pressure, slower).<br>"
      "<code>go build -gcflags='-m -m' ./...</code> shows escape decisions."),
     ("Common Escape Causes",
      "<ul><li>Variable address taken and returned: <code>return &amp;x</code> — x escapes</li>"
      "<li>Stored in interface: <code>var i interface{} = x</code> — x escapes (if not pointer-sized)</li>"
      "<li>Closure captures variable: <code>go func(){ use(x) }()</code> — x may escape</li>"
      "<li>Slice/map of large type — backing array on heap</li></ul>"),
     ("Avoiding Escapes",
      "<pre>// Bad: escapes to heap\nfunc newPoint(x,y int) *Point { return &amp;Point{x,y} }\n\n// Good: caller allocates on stack\nfunc initPoint(p *Point, x,y int) { p.X,p.Y = x,y }\nvar p Point; initPoint(&amp;p, 3, 4)  // stays on stack\n\n// Bad: interface boxing causes escape\nfunc log(msg interface{}) { fmt.Println(msg) }  // allocates\n// Good:\nfunc log(msg string) { fmt.Println(msg) }  // no alloc</pre>"),
     ("sync.Pool","Reuse heap-allocated objects across goroutines to reduce GC pressure.<br>"
      "<code>pool := sync.Pool{New: func() any { return &amp;Buffer{} }}</code>"),
     ("Follow-ups",'<div class="followup">• What is the cost of a heap allocation vs stack? (~ns vs ~100ns + GC)<br>'
      '• How does sync.Pool interact with GC? (cleared on each GC cycle)<br>'
      '• How does -race detector affect performance?</div>'))),
]

def _to_dict(q):
    return {"id":q[0],"text":q[1],"category":q[2],"subcategory":q[3],"difficulty":q[4],
            "companies":q[5],"frequency":q[6],"tags":q[7].split(","),"round_type":q[8],"answer_hint":q[9]}

QUESTIONS = [_to_dict(q) for q in GO2]
