"""Extended Go questions with full answers."""

_GO = ["Google","Uber","Razorpay","Swiggy","Zomato","CRED","Dream11","Coinbase","BrowserStack"]

def A(*sections):
    parts = []
    for label, content in sections:
        parts.append(f'<span class="answer-label">{label}</span><br>{content}')
    return '<div class="answer-section">' + '</div><div class="answer-section" style="margin-top:10px">'.join(parts) + '</div>'

GO_EXT = [
  ("gex001","How does Go's memory allocator work? (mcache, mcentral, mheap)","go","runtime","Hard",
   ["Google","Uber","Razorpay","CRED"],72,"memory-allocator,mcache,mheap,tcmalloc","Coding Round",
   A(("Architecture (inspired by TCMalloc)","<ul>"
      "<li><b>mcache:</b> Per-P (logical processor) cache of small object spans. Lock-free allocation for objects &lt;32KB.</li>"
      "<li><b>mcentral:</b> Per-size-class central lists. Replenishes mcache when empty.</li>"
      "<li><b>mheap:</b> Global heap of OS memory. Allocates large objects (&gt;32KB) directly.</li></ul>"),
     ("Size Classes","Objects grouped into ~70 size classes (8B, 16B, 24B, ... 32KB). "
      "Reduces fragmentation. Large objects go directly to mheap."),
     ("Stack Allocation","Go prefers stack allocation (escape analysis). "
      "Objects that don't escape the function go on stack — zero GC pressure."),
     ("Practical Impact",
      "<pre>// Stack allocated (no GC)\nfunc sum(a, b int) int { return a + b }\n\n// Heap allocated (escapes via interface)\nfunc boxed(x int) interface{} { return x }  // x escapes!\n\n// Check escape: go build -gcflags='-m' ./...</pre>"),
     ("Follow-ups",'<div class="followup">• What is sync.Pool and how does it interact with GC?<br>'
      '• When does a slice backing array escape to heap?<br>'
      '• How does -gcflags=-m help optimize memory?</div>'))),

  ("gex002","goroutine leak — how to detect and prevent","go","concurrency","Medium",
   _GO, 86, "goroutine-leak,context,done-channel,pprof","Coding Round",
   A(("What is a goroutine leak","Goroutines that are started but never terminate. "
      "They consume memory (~2KB initial stack, can grow), CPU for scheduling, and keep referenced objects alive."),
     ("Common Causes",
      "<ul><li>Blocked channel read/write with no one to unblock</li>"
      "<li>Not passing/checking <code>context.Context</code></li>"
      "<li>Infinite loops without exit condition</li>"
      "<li>Forgotten goroutines in tests</li></ul>"),
     ("Prevention Pattern",
      "<pre>func worker(ctx context.Context, jobs &lt;-chan Job) {\n    for {\n        select {\n        case &lt;-ctx.Done():\n            return  // clean exit\n        case job, ok := &lt;-jobs:\n            if !ok { return }  // channel closed\n            process(job)\n        }\n    }\n}</pre>"),
     ("Detection with pprof",
      "<pre>import _ \"net/http/pprof\"\n// curl http://localhost:6060/debug/pprof/goroutine?debug=2\n// Lists all goroutine stacks — look for blocked goroutines\n\n// In tests: goleak\nfunc TestWorker(t *testing.T) {\n    defer goleak.VerifyNone(t)  // fails if goroutines leak\n    ...\n}</pre>"),
     ("Follow-ups",'<div class="followup">• What is the goleak library?<br>'
      '• How do you profile goroutine count over time?<br>'
      '• What happens to a goroutine blocked on a closed channel?</div>'))),

  ("gex003","Go interfaces — nil interface trap, empty interface","go","language","Medium",
   _GO, 84, "interface,nil,empty-interface,type-assertion","Coding Round",
   A(("Interface internals","A Go interface value has <b>two words</b>: (type, pointer). "
      "An interface is nil only when <b>both</b> type and pointer are nil."),
     ("The Nil Trap",
      "<pre>type MyError struct{ msg string }\nfunc (e *MyError) Error() string { return e.msg }\n\nfunc getError() error {\n    var err *MyError = nil\n    return err  // TRAP: returns (type=*MyError, ptr=nil) — NOT nil interface!\n}\n\nif err := getError(); err != nil {\n    fmt.Println(\"This prints!\")  // Bug!\n}\n\n// Fix: return nil explicitly\nfunc getError() error {\n    var err *MyError\n    if conditionFailed { return err }  // still buggy\n    return nil  // correct\n}</pre>"),
     ("Type Assertions & Switches",
      "<pre>var i interface{} = \"hello\"\n\n// Type assertion\ns, ok := i.(string)  // ok=true, s=\"hello\"\n\n// Type switch\nswitch v := i.(type) {\ncase string:  fmt.Println(\"string:\", v)\ncase int:     fmt.Println(\"int:\", v)\ndefault:      fmt.Println(\"other\")\n}</pre>"),
     ("any (Go 1.18)","<code>any</code> is an alias for <code>interface{}</code>. Prefer <code>any</code> in new code."),
     ("Follow-ups",'<div class="followup">• How does interface satisfaction work at compile time?<br>'
      '• What is the reflect package and when do you need it?<br>'
      '• How are generics better than interface{} for type safety?</div>'))),

  ("gex004","Go error handling — errors.Is, errors.As, wrapping","go","language","Medium",
   _GO, 88, "errors,wrapping,sentinel,errors-as","Coding Round",
   A(("Error Wrapping (Go 1.13+)","Wrap errors with context using <code>fmt.Errorf(\"%w\", err)</code>. "
      "This creates an error chain. The original error is retrievable."),
     ("errors.Is and errors.As",
      "<pre>var ErrNotFound = errors.New(\"not found\")  // sentinel\n\n// Wrapping\nfunc getUser(id int) error {\n    return fmt.Errorf(\"getUser %d: %w\", id, ErrNotFound)\n}\n\nerr := getUser(42)\n// errors.Is: checks entire chain\nif errors.Is(err, ErrNotFound) {\n    // handles wrapped ErrNotFound\n}\n\n// errors.As: extract concrete type from chain\nvar dbErr *DBError\nif errors.As(err, &amp;dbErr) {\n    fmt.Println(dbErr.Code)\n}</pre>"),
     ("Custom Error Types",
      "<pre>type ValidationError struct {\n    Field   string\n    Message string\n}\nfunc (e *ValidationError) Error() string {\n    return fmt.Sprintf(\"validation error: %s — %s\", e.Field, e.Message)\n}\n\n// Callers use errors.As to get the typed error</pre>"),
     ("Best Practices",
      "<ul><li>Always wrap with context: <code>fmt.Errorf(\"operation X: %w\", err)</code></li>"
      "<li>Use sentinel errors for known conditions (<code>io.EOF</code>, <code>sql.ErrNoRows</code>)</li>"
      "<li>Use typed errors when callers need to inspect fields</li>"
      "<li>At service boundary: log + translate to user-facing error</li></ul>"),
     ("Follow-ups",'<div class="followup">• When would you use panic vs return error?<br>'
      '• How does errors.Join (Go 1.20) work?<br>'
      '• How does the errors package handle multiple wrapped errors?</div>'))),

  ("gex005","Go testing — table-driven tests, benchmarks, fuzz testing","go","testing","Medium",
   _GO + ["Google","Stripe","Atlassian"],80,"testing,benchmark,fuzz,table-driven","Coding Round",
   A(("Table-Driven Tests",
      "<pre>func TestAdd(t *testing.T) {\n    tests := []struct {\n        name string; a, b, want int\n    }{\n        {\"positive\", 2, 3, 5},\n        {\"negative\", -1, 1, 0},\n        {\"zeros\", 0, 0, 0},\n    }\n    for _, tc := range tests {\n        t.Run(tc.name, func(t *testing.T) {\n            if got := Add(tc.a, tc.b); got != tc.want {\n                t.Errorf(\"Add(%d,%d)=%d, want %d\", tc.a, tc.b, got, tc.want)\n            }\n        })\n    }\n}</pre>"),
     ("Benchmarks",
      "<pre>func BenchmarkAdd(b *testing.B) {\n    for i := 0; i &lt; b.N; i++ {\n        Add(42, 58)\n    }\n}\n// go test -bench=. -benchmem -count=5</pre>"),
     ("Fuzz Testing (Go 1.18+)",
      "<pre>func FuzzReverse(f *testing.F) {\n    f.Add(\"hello\")  // seed corpus\n    f.Fuzz(func(t *testing.T, s string) {\n        rev := Reverse(s)\n        if Reverse(rev) != s {\n            t.Errorf(\"double reverse != original\")\n        }\n    })\n}\n// go test -fuzz=FuzzReverse -fuzztime=30s</pre>"),
     ("Useful Flags","<pre>go test -run=TestName -v          # run specific test\ngo test -race ./...               # race detector\ngo test -coverprofile=c.out ./... # coverage\ngo tool cover -html=c.out         # view coverage</pre>"),
     ("Follow-ups",'<div class="followup">• What is testify and when is it useful?<br>'
      '• How do you mock dependencies in Go tests?<br>'
      '• What is httptest.NewServer for HTTP handler testing?</div>'))),

  ("gex006","errgroup — coordinating concurrent goroutines with error handling","go","concurrency","Medium",
   ["Google","Uber","Razorpay","CRED","Stripe"],78,"errgroup,concurrent,wait-group,context","Coding Round",
   A(("Problem","<code>sync.WaitGroup</code> doesn't propagate errors. Manual error collection is error-prone."),
     ("errgroup solution",
      "<pre>import \"golang.org/x/sync/errgroup\"\n\nfunc fetchAll(ctx context.Context, ids []int) ([]User, error) {\n    g, ctx := errgroup.WithContext(ctx)\n    results := make([]User, len(ids))\n\n    for i, id := range ids {\n        i, id := i, id  // capture loop vars\n        g.Go(func() error {\n            user, err := fetchUser(ctx, id)\n            if err != nil { return err }\n            results[i] = user\n            return nil\n        })\n    }\n\n    if err := g.Wait(); err != nil {\n        return nil, fmt.Errorf(\"fetchAll: %w\", err)\n    }\n    return results, nil\n}</pre>"),
     ("Key behaviours",
      "<ul><li>First error cancels derived context (<code>ctx.Done()</code> triggers)</li>"
      "<li><code>g.Wait()</code> blocks until all goroutines finish, returns first error</li>"
      "<li>Limit concurrency: <code>g.SetLimit(10)</code> (Go 1.20+)</li></ul>"),
     ("Follow-ups",'<div class="followup">• How do you collect ALL errors instead of just the first?<br>'
      '• How does errgroup differ from sync.WaitGroup?<br>'
      '• What is semaphore.Weighted for concurrency limiting?</div>'))),

  ("gex007","Go profiling with pprof — CPU, memory, goroutines","go","performance","Medium",
   ["Google","Uber","Razorpay","CRED"],76,"pprof,profiling,cpu,heap,goroutine","Coding Round",
   A(("Enable pprof HTTP endpoint",
      "<pre>import _ \"net/http/pprof\"\ngo func() { http.ListenAndServe(\":6060\", nil) }()</pre>"),
     ("Profile Types",
      "<ul><li><b>CPU:</b> <code>/debug/pprof/profile?seconds=30</code> — sample what's using CPU</li>"
      "<li><b>Heap:</b> <code>/debug/pprof/heap</code> — memory allocations and retained objects</li>"
      "<li><b>Goroutines:</b> <code>/debug/pprof/goroutine?debug=2</code> — all goroutine stacks</li>"
      "<li><b>Trace:</b> <code>/debug/pprof/trace?seconds=5</code> — execution trace (scheduler, GC)</li>"
      "<li><b>Block/Mutex:</b> contention profiling</li></ul>"),
     ("Analysis with go tool pprof",
      "<pre>go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30\n# Inside pprof:\n(pprof) top10       # top CPU consumers\n(pprof) web         # flame graph in browser\n(pprof) list myFunc # line-level annotation</pre>"),
     ("async-profiler / Flamegraph","For production: <b>continuous profiling</b> (Pyroscope, Google Cloud Profiler). "
      "Flamegraph: x-axis = CPU time, width = time spent, y-axis = call stack."),
     ("Follow-ups",'<div class="followup">• How do you reduce allocations found in heap profile?<br>'
      '• What is the difference between inuse_space and alloc_space?<br>'
      '• How does GODEBUG=gctrace=1 help?</div>'))),

  ("gex008","sync.Once, sync.Map — when and how to use","go","concurrency","Medium",
   _GO, 78, "sync-once,sync-map,concurrent","Concurrency Round",
   A(("sync.Once","Guarantees a function runs <b>exactly once</b>, even if called concurrently. "
      "Perfect for lazy initialization."),
     ("sync.Once Example",
      "<pre>var (\n    instance *DB\n    once     sync.Once\n)\n\nfunc GetDB() *DB {\n    once.Do(func() {\n        instance = connectDB()  // runs exactly once\n    })\n    return instance\n}\n// Thread-safe singleton. Once completes, all goroutines see instance.</pre>"),
     ("sync.Map","Concurrent map without external locking. Optimized for two use cases: "
      "(1) write once, read many; (2) different goroutines write different keys."),
     ("sync.Map Example",
      "<pre>var m sync.Map\nm.Store(\"key\", \"value\")\nv, ok := m.Load(\"key\")\nm.Delete(\"key\")\nm.Range(func(k, v any) bool {\n    fmt.Println(k, v)\n    return true  // continue iteration\n})</pre>"),
     ("sync.Map vs map+RWMutex","<ul><li><code>sync.Map</code>: better for high-read, diverse-keys workloads</li>"
      "<li><code>map+RWMutex</code>: better for small maps or when you need atomic multi-op</li></ul>"),
     ("Follow-ups",'<div class="followup">• Why is sync.Once better than an atomic boolean flag?<br>'
      '• What happens if the function passed to Once panics?<br>'
      '• How is sync.Map implemented internally? (dirty + read maps)</div>'))),

  ("gex009","Go generics (type parameters) — real-world patterns","go","generics","Medium",
   ["Google","Uber","Razorpay","CRED"],74,"generics,type-parameters,constraints,slice","Coding Round",
   A(("Basic Syntax",
      "<pre>// Generic Min function\nfunc Min[T constraints.Ordered](a, b T) T {\n    if a &lt; b { return a }\n    return b\n}\n\nMin(3, 5)        // int\nMin(3.14, 2.72)  // float64\nMin(\"a\", \"b\")    // string</pre>"),
     ("Generic Map/Filter/Reduce",
      "<pre>func Map[T, U any](slice []T, f func(T) U) []U {\n    result := make([]U, len(slice))\n    for i, v := range slice {\n        result[i] = f(v)\n    }\n    return result\n}\n\nnums := []int{1,2,3,4,5}\ndoubled := Map(nums, func(x int) int { return x * 2 })\n// [2 4 6 8 10]</pre>"),
     ("Type Constraints",
      "<pre>// Interface as constraint\ntype Number interface { ~int | ~float64 }\n\nfunc Sum[T Number](nums []T) T {\n    var total T\n    for _, n := range nums { total += n }\n    return total\n}</pre>"),
     ("Limitations","<ul><li>No generic methods on types (only functions and type params on struct)</li>"
      "<li>No operator overloading — use constraints</li>"
      "<li>Type inference works in most cases</li></ul>"),
     ("Follow-ups",'<div class="followup">• What is the ~ tilde operator in constraints?<br>'
      '• When should you use generics vs interface{}?<br>'
      '• How does Go generics compare to Java generics (type erasure)?</div>'))),

  ("gex010","HTTP server patterns in Go — graceful shutdown, middleware","go","patterns","Medium",
   _GO + ["Stripe","Atlassian"],80,"http-server,middleware,graceful-shutdown,handler","Coding Round",
   A(("Standard HTTP Server",
      "<pre>mux := http.NewServeMux()\nmux.HandleFunc(\"/health\", healthHandler)\nmux.Handle(\"/api/\", apiRouter)\n\nsrv := &amp;http.Server{\n    Addr:         \":8080\",\n    Handler:      mux,\n    ReadTimeout:  5 * time.Second,\n    WriteTimeout: 10 * time.Second,\n    IdleTimeout:  120 * time.Second,\n}</pre>"),
     ("Graceful Shutdown",
      "<pre>go func() { srv.ListenAndServe() }()\n\nquit := make(chan os.Signal, 1)\nsignal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)\n&lt;-quit\n\nctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)\ndefer cancel()\nif err := srv.Shutdown(ctx); err != nil {\n    log.Fatal(\"forced shutdown:\", err)\n}\n// In-flight requests complete, new requests rejected</pre>"),
     ("Middleware Pattern",
      "<pre>type Middleware func(http.Handler) http.Handler\n\nfunc Logger(next http.Handler) http.Handler {\n    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {\n        start := time.Now()\n        next.ServeHTTP(w, r)\n        log.Printf(\"%s %s %v\", r.Method, r.URL.Path, time.Since(start))\n    })\n}\n\n// Chain: Logger(Auth(RateLimit(mux)))</pre>"),
     ("Popular routers","chi (lightweight), gorilla/mux (feature-rich), gin (fast, opinionated), fiber (Express-like)."),
     ("Follow-ups",'<div class="followup">• How do you implement request timeout per handler?<br>'
      '• What is http.ResponseController (Go 1.20)?<br>'
      '• How does context propagation work through HTTP handlers?</div>'))),
]

def _to_dict(q):
    return {
        "id": q[0], "text": q[1], "category": q[2], "subcategory": q[3],
        "difficulty": q[4], "companies": q[5], "frequency": q[6],
        "tags": q[7].split(","), "round_type": q[8], "answer_hint": q[9]
    }

QUESTIONS = [_to_dict(q) for q in GO_EXT]
