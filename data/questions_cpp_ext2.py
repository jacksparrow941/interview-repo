"""C++ Extended Part 2 — Rule of 0/3/5, CRTP, constexpr, allocators, virtual inheritance, fold expressions."""

_CPP = ["Google","Meta","Nvidia","Apple","Databricks","VMware","Cisco","Stripe","Snowflake"]

def A(*s):
    parts = [f'<span class="answer-label">{l}</span><br>{c}' for l,c in s]
    return '<div class="answer-section">'+'</div><div class="answer-section" style="margin-top:10px">'.join(parts)+'</div>'

CPP2 = [
  ("cpx013","Rule of 0, Rule of 3, Rule of 5 — explain with examples","cpp","oop","Hard",_CPP,82,
   "rule-of-3,rule-of-5,move,destructor,copy","Coding Round",
   A(("Rule of 3 (pre-C++11)","If you define any of: <b>destructor</b>, <b>copy constructor</b>, <b>copy assignment</b>, "
      "you should define all three. (Managing raw resource → need custom copy + destructor)"),
     ("Rule of 5 (C++11+)","Add <b>move constructor</b> + <b>move assignment</b>. Without them, moves fall back to copies (expensive).<br>"
      "<pre>class Buffer {\n    char* data; size_t sz;\npublic:\n    Buffer(size_t n) : data(new char[n]), sz(n) {}\n    ~Buffer() { delete[] data; }               // 1: destructor\n    Buffer(const Buffer&amp; o)                   // 2: copy ctor\n        : data(new char[o.sz]), sz(o.sz) { memcpy(data,o.data,sz); }\n    Buffer&amp; operator=(const Buffer&amp; o) {       // 3: copy assign\n        if(this==&amp;o) return *this;\n        delete[] data; sz=o.sz; data=new char[sz]; memcpy(data,o.data,sz); return *this;\n    }\n    Buffer(Buffer&amp;&amp; o) noexcept                // 4: move ctor\n        : data(o.data), sz(o.sz) { o.data=nullptr; o.sz=0; }\n    Buffer&amp; operator=(Buffer&amp;&amp; o) noexcept {   // 5: move assign\n        if(this==&amp;o) return *this;\n        delete[] data; data=o.data; sz=o.sz; o.data=nullptr; return *this;\n    }\n};</pre>"),
     ("Rule of 0","Best practice: design classes to own no raw resources. Use RAII wrappers "
      "(<code>unique_ptr</code>, <code>vector</code>, <code>string</code>). Then you need ZERO custom special members — compiler generates correct ones."),
     ("Follow-ups",'<div class="followup">• What does <code>=default</code> and <code>=delete</code> do?<br>'
      '• What is the copy-and-swap idiom?<br>• When is a move constructor marked noexcept important?</div>'))),

  ("cpx014","CRTP — Curiously Recurring Template Pattern","cpp","templates","Hard",["Google","Meta","Nvidia","Databricks"],70,
   "crtp,static-polymorphism,mixin","Coding Round",
   A(("What is CRTP","Base class templated on its derived class. Enables <b>static polymorphism</b> (compile-time virtual dispatch) — zero vtable overhead."),
     ("Example: Static Polymorphism",
      "<pre>template&lt;typename Derived&gt;\nstruct Shape {\n    double area() const {\n        return static_cast&lt;const Derived*&gt;(this)-&gt;area_impl();\n    }\n};\nstruct Circle : Shape&lt;Circle&gt; {\n    double r;\n    double area_impl() const { return 3.14*r*r; }\n};\nstruct Square : Shape&lt;Square&gt; {\n    double s;\n    double area_impl() const { return s*s; }\n};\n// Caller (template function, not virtual):\ntemplate&lt;typename S&gt; void print(const Shape&lt;S&gt;&amp; s) { std::cout &lt;&lt; s.area(); }</pre>"),
     ("CRTP for Mixins",
      "<pre>template&lt;typename T&gt;\nstruct Comparable {\n    bool operator!=(const T&amp; o) const { return !(static_cast&lt;const T&amp;&gt;(*this)==o); }\n    bool operator&gt; (const T&amp; o) const { return o &lt; static_cast&lt;const T&amp;&gt;(*this); }\n    // Derived only implements operator== and operator&lt;\n};\nstruct Point : Comparable&lt;Point&gt; {\n    int x,y;\n    bool operator==(const Point&amp; o) const { return x==o.x &amp;&amp; y==o.y; }\n    bool operator&lt; (const Point&amp; o) const { return x&lt;o.x || (x==o.x &amp;&amp; y&lt;o.y); }\n};</pre>"),
     ("CRTP vs Concepts (C++20)","CRTP: complex syntax, but works pre-C++20 with zero runtime cost. "
      "C++20 Concepts: cleaner constraints but still need virtual for runtime polymorphism."),
     ("Follow-ups",'<div class="followup">• What is the difference between CRTP and policy-based design?<br>'
      '• How does CRTP avoid object slicing?<br>• What are the limitations of CRTP vs virtual?</div>'))),

  ("cpx015","constexpr vs consteval vs constinit (C++20)","cpp","language","Medium",["Google","Meta","Nvidia","Databricks","Snowflake"],72,
   "constexpr,consteval,constinit,compile-time","Coding Round",
   A(("constexpr","Can run at compile time OR runtime. Compiler decides.<br>"
      "<pre>constexpr int square(int x) { return x*x; }\nconstexpr int s = square(5);  // compile-time\nint n = 7; int r = square(n);  // runtime — also valid</pre>"),
     ("consteval (C++20)","<b>Must</b> be evaluated at compile time. Immediate function. Compile error if runtime call attempted.<br>"
      "<pre>consteval int cube(int x) { return x*x*x; }\nconsteval auto getCube = cube(3);  // OK: 27 at compile time\nint n=5; cube(n);                  // ERROR: n not constant</pre>"),
     ("constinit (C++20)","Variable <b>must</b> be initialized at compile time (no static initialization order fiasco). "
      "Unlike constexpr, the variable itself can still be modified at runtime.<br>"
      "<pre>constinit int counter = 0;  // initialized at compile time\ncounter++;                  // runtime modification OK</pre>"),
     ("When to use","<ul><li><code>constexpr</code>: functions/variables that should work at both compile and runtime</li>"
      "<li><code>consteval</code>: guaranteed compile-time (type traits, code generation, DSLs)</li>"
      "<li><code>constinit</code>: global/static variables to avoid init-order issues</li></ul>"),
     ("Follow-ups",'<div class="followup">• What is the static initialization order fiasco?<br>'
      '• Can constexpr functions have loops, recursion? (Yes, since C++14)<br>'
      '• What is std::is_constant_evaluated()?</div>'))),

  ("cpx016","Virtual inheritance and the diamond problem","cpp","oop","Hard",["Google","Meta","Nvidia","VMware","Cisco"],72,
   "virtual-inheritance,diamond,multiple-inheritance,vtable","Coding Round",
   A(("Diamond Problem",
      "<pre>struct A { int x; };\nstruct B : A {};\nstruct C : A {};\nstruct D : B, C {};   // D has TWO copies of A!\nD d;\nd.x = 5;              // Error: ambiguous — B::A::x or C::A::x?</pre>"),
     ("Virtual Inheritance Fix",
      "<pre>struct A { int x; };\nstruct B : virtual A {};\nstruct C : virtual A {};\nstruct D : B, C {};   // Only ONE shared A\nD d; d.x = 5;         // OK: unambiguous</pre>"),
     ("How it works","With virtual inheritance, B and C each store a <b>virtual base pointer</b> (vbptr) pointing to "
      "the shared A subobject. D's constructor directly initializes A."),
     ("Cost","Extra pointer per virtual base. More complex object layout. "
      "<code>dynamic_cast</code> needed for cross-casting. Avoid in performance-critical code."),
     ("Follow-ups",'<div class="followup">• Who initializes the virtual base in the most-derived class?<br>'
      '• What is object slicing in virtual inheritance?<br>'
      '• How does virtual inheritance affect sizeof?</div>'))),

  ("cpx017","Fold expressions (C++17) and variadic templates","cpp","templates","Hard",["Google","Meta","Nvidia","Databricks"],68,
   "fold-expressions,variadic,parameter-pack","Coding Round",
   A(("Variadic Templates",
      "<pre>template&lt;typename... Args&gt;\nvoid print(Args... args) {\n    (std::cout &lt;&lt; ... &lt;&lt; args) &lt;&lt; '\\n';  // fold expression\n}</pre>"),
     ("Fold Expression Syntax",
      "<ul><li><b>Unary left fold:</b> <code>(... op pack)</code> → <code>((a op b) op c)</code></li>"
      "<li><b>Unary right fold:</b> <code>(pack op ...)</code> → <code>(a op (b op c))</code></li>"
      "<li><b>Binary left fold:</b> <code>(init op ... op pack)</code></li></ul>"
      "<pre>// Sum of any number of args:\ntemplate&lt;typename... T&gt;\nauto sum(T... args) { return (args + ...); }\n\n// All conditions true:\ntemplate&lt;typename... T&gt;\nbool all_true(T... vals) { return (... &amp;&amp; vals); }</pre>"),
     ("Before C++17 (recursive)","Needed base case + recursive templates. Fold expressions replace this with a single expression."),
     ("Follow-ups",'<div class="followup">• How do you iterate over a parameter pack without fold?<br>'
      '• What is std::apply and how does it use parameter packs?<br>'
      '• How do you get the count of pack elements? (sizeof...(pack))</div>'))),

  ("cpx018","std::condition_variable — producer-consumer pattern","cpp","concurrency","Medium",_CPP,78,
   "condition-variable,mutex,notify,wait","Concurrency Round",
   A(("Full Producer-Consumer",
      "<pre>#include &lt;mutex&gt;\n#include &lt;condition_variable&gt;\n#include &lt;queue&gt;\n\nstd::mutex mtx;\nstd::condition_variable cv;\nstd::queue&lt;int&gt; q;\nbool done = false;\n\nvoid producer() {\n    for(int i=0;i&lt;10;i++) {\n        std::unique_lock lock(mtx);\n        q.push(i);\n        cv.notify_one();  // wake one consumer\n    }\n    { std::lock_guard lock(mtx); done=true; }\n    cv.notify_all();\n}\n\nvoid consumer() {\n    while(true) {\n        std::unique_lock lock(mtx);\n        cv.wait(lock, []{ return !q.empty() || done; });  // predicate prevents spurious wakeup\n        while(!q.empty()) { process(q.front()); q.pop(); }\n        if(done) break;\n    }\n}</pre>"),
     ("Spurious Wakeups","Always use <code>cv.wait(lock, predicate)</code> — without predicate, spurious wakeups cause bugs. "
      "Equivalent to: <code>while(!pred()) cv.wait(lock);</code>"),
     ("notify_one vs notify_all","<code>notify_one</code>: wake 1 waiter (use for single-consumer or rotating consumers). "
      "<code>notify_all</code>: wake all waiters (use for broadcast events like shutdown)."),
     ("Follow-ups",'<div class="followup">• What is std::condition_variable_any?<br>'
      '• Why must you always hold the mutex when calling notify?<br>'
      '• How would you implement a bounded buffer (semaphore-like)?</div>'))),

  ("cpx019","unique_lock vs lock_guard vs scoped_lock","cpp","concurrency","Medium",_CPP,76,
   "lock-guard,unique-lock,scoped-lock,mutex","Concurrency Round",
   A(("lock_guard (C++11)","Simplest RAII wrapper. Locks on construction, unlocks on destruction. "
      "Cannot be unlocked/relocked. Cannot be moved. Use when you need a simple lock for a scope.<br>"
      "<code>std::lock_guard&lt;std::mutex&gt; lock(m);</code>"),
     ("unique_lock (C++11)","More flexible. Can unlock/relock, deferred locking, timed locking. Required for <code>condition_variable</code>.<br>"
      "<pre>std::unique_lock lock(m, std::defer_lock);  // don't lock yet\nlock.lock();        // lock later\nlock.unlock();      // unlock early\nbool got = lock.try_lock_for(100ms);  // timed</pre>"),
     ("scoped_lock (C++17)","Locks <b>multiple mutexes atomically</b> without deadlock (uses deadlock-free algorithm). "
      "Replaces <code>std::lock(m1,m2) + lock_guard(adopt)</code> pattern.<br>"
      "<code>std::scoped_lock lock(m1, m2, m3);  // all or nothing</code>"),
     ("When to use","<ul><li><code>lock_guard</code>: simple scope lock, no condition_variable</li>"
      "<li><code>unique_lock</code>: condition_variable, deferred/timed locking, early unlock</li>"
      "<li><code>scoped_lock</code>: locking 2+ mutexes, avoiding deadlock</li></ul>"),
     ("Follow-ups",'<div class="followup">• How does scoped_lock prevent deadlock? (std::lock uses try-lock backoff)<br>'
      '• What is std::adopt_lock and std::defer_lock?<br>'
      '• When would you use a recursive_mutex?</div>'))),

  ("cpx020","Custom allocators in C++ — std::allocator, pmr","cpp","performance","Hard",["Google","Meta","Nvidia","Databricks","Snowflake"],66,
   "allocator,pmr,memory-pool,arena","Coding Round",
   A(("Why Custom Allocators","Default <code>new</code>/<code>delete</code>: thread-safe but expensive (lock, fragmentation). "
      "Custom allocators: pool allocation, arena, stack allocation, no fragmentation, cache-friendly."),
     ("std::pmr (C++17 — Polymorphic Memory Resources)",
      "<pre>#include &lt;memory_resource&gt;\n\n// Stack-based pool: zero heap allocation\nchar buf[4096];\nstd::pmr::monotonic_buffer_resource pool(buf, sizeof(buf));\nstd::pmr::vector&lt;int&gt; v(&amp;pool);  // uses pool\nv.push_back(42);  // no malloc!\n// When pool exhausted → falls back to upstream allocator</pre>"),
     ("Common pmr Resources",
      "<ul><li><code>monotonic_buffer_resource</code>: bump allocator, no deallocation (free all at once)</li>"
      "<li><code>synchronized_pool_resource</code>: thread-safe pool</li>"
      "<li><code>unsynchronized_pool_resource</code>: fast, single-threaded</li></ul>"),
     ("Use Cases","Hot-path allocations, game engines, parsers, per-request arenas in servers "
      "(allocate all request data in arena, free entire arena at end of request)."),
     ("Follow-ups",'<div class="followup">• How do you write a custom allocator that satisfies the Allocator concept?<br>'
      '• What is placement new and how is it related to custom allocators?<br>'
      '• How does jemalloc/tcmalloc differ from std::allocator?</div>'))),

  ("cpx021","std::async — launch policies, futures, shared_future","cpp","concurrency","Medium",_CPP,74,
   "async,future,promise,launch-policy","Concurrency Round",
   A(("std::async",
      "<pre>// async: launch policy = async (new thread) or deferred (lazy, same thread)\nauto fut = std::async(std::launch::async, []{\n    return heavyCompute();\n});\n// ... do other work ...\nint result = fut.get();  // blocks until ready</pre>"),
     ("Launch Policies",
      "<ul><li><code>std::launch::async</code>: spawn new thread immediately</li>"
      "<li><code>std::launch::deferred</code>: run lazily when <code>.get()</code> or <code>.wait()</code> is called (same thread)</li>"
      "<li><code>std::launch::async | std::launch::deferred</code> (default): implementation chooses — <b>dangerous</b>, may never run</li></ul>"),
     ("Promise/Future",
      "<pre>std::promise&lt;int&gt; prom;\nstd::future&lt;int&gt; fut = prom.get_future();\n\nstd::thread t([&amp;]{ prom.set_value(42); });\nstd::cout &lt;&lt; fut.get();  // blocks until set_value\nt.join();</pre>"),
     ("shared_future","Multiple threads can wait on the same result. "
      "<code>std::shared_future&lt;T&gt; sf = fut.share();</code> — can be copied, each can call <code>.get()</code>."),
     ("Follow-ups",'<div class="followup">• What happens if an exception is thrown in async task?<br>'
      '• How do you implement a thread pool with futures?<br>'
      '• Why is the default launch policy dangerous?</div>'))),

  ("cpx022","Structured bindings (C++17) and std::tie","cpp","language","Easy",_CPP,76,
   "structured-bindings,tuple,tie,decomposition","Coding Round",
   A(("Structured Bindings (C++17)",
      "<pre>// Decompose pair\nauto [key, val] = std::make_pair(\"name\", 42);\n\n// Decompose struct\nstruct Point { int x, y; };\nPoint p{3, 4};\nauto [x, y] = p;\n\n// Decompose map iteration\nstd::map&lt;std::string,int&gt; m = {{\"a\",1},{\"b\",2}};\nfor (auto&amp; [key, value] : m) {\n    std::cout &lt;&lt; key &lt;&lt; \":\" &lt;&lt; value &lt;&lt; \"\\n\";\n}\n\n// Decompose array\nint arr[3] = {1,2,3};\nauto [a,b,c] = arr;</pre>"),
     ("std::tie (pre-C++17)","Bind to existing variables (not declarations):<br>"
      "<pre>int x, y;\nstd::tie(x, y) = std::make_pair(10, 20);\n\n// Ignore elements:\nstd::tie(x, std::ignore) = returnPair();</pre>"),
     ("Multiple return values",
      "<pre>auto [min, max] = std::minmax({5,2,8,1});\nauto [it, inserted] = myMap.emplace(\"key\", 99);  // map::emplace returns pair</pre>"),
     ("Follow-ups",'<div class="followup">• Can you use structured bindings with custom types? (yes, via get&lt;N&gt; specialization)<br>'
      '• What is std::get&lt;N&gt; and how does it relate to structured bindings?<br>'
      '• How do structured bindings handle by-reference vs by-value?</div>'))),

  ("cpx023","Move semantics — rvalue references, std::move, std::forward","cpp","language","Hard",_CPP,86,
   "move-semantics,rvalue,forward,perfect-forward","Coding Round",
   A(("Rvalue References",
      "<pre>int&amp;&amp; r = 42;           // rvalue reference: binds to temporaries\nvoid take(std::string&amp;&amp; s); // accepts rvalue (temporary)\n\nstd::string s = \"hello\";\ntake(std::move(s));    // cast to rvalue (s is now valid-but-unspecified)\ntake(\"world\");         // temporary: OK</pre>"),
     ("std::move","<b>Cast</b> to rvalue reference — enables move constructor/assignment to be called. "
      "After move, source is in valid but unspecified state. Do NOT use moved-from object except to assign or destroy."),
     ("std::forward — Perfect Forwarding",
      "<pre>// Forward preserves value category (lvalue stays lvalue, rvalue stays rvalue)\ntemplate&lt;typename T, typename... Args&gt;\nT* create(Args&amp;&amp;... args) {\n    return new T(std::forward&lt;Args&gt;(args)...);\n}\n// If passed lvalue → forwards as lvalue\n// If passed rvalue → forwards as rvalue</pre>"),
     ("Universal Reference","<code>T&amp;&amp;</code> in a template (deduced context) is a <b>universal/forwarding reference</b>, "
      "not an rvalue reference. With <code>T=int&amp;</code>, <code>T&amp;&amp;</code> collapses to <code>int&amp;</code> (reference collapsing)."),
     ("Follow-ups",'<div class="followup">• What is reference collapsing? (T&amp;&amp; + T=int&amp; → int&amp;)<br>'
      '• When is a move more expensive than a copy? (std::array, trivial types)<br>'
      '• How does return value optimization (RVO/NRVO) interact with moves?</div>'))),
]

def _to_dict(q):
    return {"id":q[0],"text":q[1],"category":q[2],"subcategory":q[3],"difficulty":q[4],
            "companies":q[5],"frequency":q[6],"tags":q[7].split(","),"round_type":q[8],"answer_hint":q[9]}

QUESTIONS = [_to_dict(q) for q in CPP2]
