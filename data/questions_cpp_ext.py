"""Extended C++ questions with full answers."""

_CPP = ["Google","Meta","Nvidia","Apple","Databricks","Snowflake","VMware","Cisco","Stripe"]

def A(*sections):
    parts = []
    for label, content in sections:
        parts.append(f'<span class="answer-label">{label}</span><br>{content}')
    return '<div class="answer-section">' + '</div><div class="answer-section" style="margin-top:10px">'.join(parts) + '</div>'

CPP_EXT = [
  ("cpx001","What is SFINAE and how is it used?","cpp","templates","Hard",_CPP,72,"sfinae,enable_if,type_traits","Coding Round",
   A(("Answer","<b>SFINAE</b> = Substitution Failure Is Not An Error. When template argument substitution fails during overload resolution, "
      "the compiler removes that candidate instead of throwing an error.<br>Used with <code>std::enable_if</code> to conditionally enable functions."),
     ("Example",
      "<pre>template&lt;typename T,\n         typename = std::enable_if_t&lt;std::is_integral_v&lt;T&gt;&gt;&gt;\nvoid process(T val) { /* integers only */ }\n\n"
      "// C++20 cleaner with concepts:\ntemplate&lt;std::integral T&gt;\nvoid process(T val) { }</pre>"),
     ("Use Cases","<ul><li>Tag dispatch based on type properties</li>"
      "<li>Selecting different implementations for trivial vs non-trivial types</li>"
      "<li>Building type traits</li></ul>"),
     ("Follow-ups",'<div class="followup">• What replaced SFINAE in C++20? (Concepts)<br>'
      '• Explain <code>std::void_t</code> and detection idiom.<br>• What is <code>std::conditional_t</code>?</div>'))),

  ("cpx002","C++ Coroutines (C++20) — co_await, co_yield, co_return","cpp","language","Hard",["Google","Meta","Nvidia","Databricks"],68,
   "coroutines,co_await,co_yield,async","Coding Round",
   A(("What are Coroutines","Functions that can be <b>suspended and resumed</b>. "
      "A coroutine is a function containing <code>co_await</code>, <code>co_yield</code>, or <code>co_return</code>."),
     ("Key Keywords",
      "<ul><li><code>co_await expr</code> — suspend until expr completes</li>"
      "<li><code>co_yield val</code> — yield a value and suspend (generator pattern)</li>"
      "<li><code>co_return val</code> — complete the coroutine</li></ul>"),
     ("Generator Example",
      "<pre>Generator&lt;int&gt; fibonacci() {\n    int a = 0, b = 1;\n    while (true) {\n        co_yield a;\n        auto c = a + b; a = b; b = c;\n    }\n}\n\nfor (int x : fibonacci() | take(10)) std::cout &lt;&lt; x;</pre>"),
     ("Coroutine Frame","Coroutine state is heap-allocated (coroutine frame). "
      "Coroutine handle manages lifetime. Promise object customizes behaviour."),
     ("Follow-ups",'<div class="followup">• How do coroutines compare to threads? (single-threaded cooperative vs preemptive)<br>'
      '• What is <code>std::generator</code> (C++23)?<br>• Explain symmetric vs asymmetric coroutines.</div>'))),

  ("cpx003","std::variant, std::optional, std::any — when to use each","cpp","language","Medium",_CPP,74,
   "variant,optional,any,type-safe","Coding Round",
   A(("std::optional&lt;T&gt;","Represents a value that <b>may or may not be present</b>. "
      "Replaces nullable pointers and sentinel values.<br>"
      "<pre>std::optional&lt;User&gt; findUser(int id);\nauto u = findUser(42);\nif (u) { std::cout &lt;&lt; u-&gt;name; }</pre>"),
     ("std::variant&lt;T1,T2,...&gt;","Type-safe union. Holds exactly one of a fixed set of types.<br>"
      "<pre>std::variant&lt;int, double, std::string&gt; v = 42;\nstd::visit(overloaded{\n    [](int i)   { cout &lt;&lt; \"int: \" &lt;&lt; i; },\n    [](double d){ cout &lt;&lt; \"double: \" &lt;&lt; d; },\n    [](auto&amp; s) { cout &lt;&lt; \"str: \" &lt;&lt; s; }\n}, v);</pre>"),
     ("std::any","Holds <b>any type</b> at runtime (type-erased). Use <code>std::any_cast</code>. "
      "Performance overhead: heap allocation for large objects. Use sparingly."),
     ("When to use","<ul><li><b>optional:</b> Function may fail or return nothing</li>"
      "<li><b>variant:</b> Known set of alternatives (Result type, AST nodes, event types)</li>"
      "<li><b>any:</b> Truly unknown type at compile time (config maps, plugin systems)</li></ul>"),
     ("Follow-ups",'<div class="followup">• How do you implement a Result&lt;T,E&gt; type using variant?<br>'
      '• What is std::expected (C++23)?<br>• Performance of variant vs virtual dispatch?</div>'))),

  ("cpx004","Memory model — happens-before, acquire/release semantics","cpp","concurrency","Hard",["Google","Meta","Nvidia","Databricks"],70,
   "memory-model,acquire,release,happens-before","Coding Round",
   A(("C++ Memory Orderings","<ul>"
      "<li><code>memory_order_relaxed</code> — no synchronization, only atomicity</li>"
      "<li><code>memory_order_acquire</code> — no loads/stores can move before this load</li>"
      "<li><code>memory_order_release</code> — no loads/stores can move after this store</li>"
      "<li><code>memory_order_acq_rel</code> — both acquire and release</li>"
      "<li><code>memory_order_seq_cst</code> — total ordering (default, most expensive)</li></ul>"),
     ("Acquire-Release Pattern",
      "<pre>// Producer\ndata.store(42, relaxed);\nready.store(true, memory_order_release);  // store is visible\n\n"
      "// Consumer\nwhile (!ready.load(memory_order_acquire));  // wait until acquire sees release\nuse(data.load(relaxed));  // guaranteed to see 42</pre>"),
     ("Happens-before","A <b>happens-before</b> relationship guarantees that all writes before a release are visible "
      "after the corresponding acquire. Essential for lock-free programming."),
     ("Follow-ups",'<div class="followup">• Why is sequentially consistent ordering expensive on ARM?<br>'
      '• What is a data race? (concurrent access, at least one write, no sync)<br>'
      '• How does std::mutex establish happens-before?</div>'))),

  ("cpx005","What are C++20 Concepts?","cpp","templates","Hard",["Google","Meta","Nvidia","Databricks","Snowflake"],72,
   "concepts,constraints,requires","Coding Round",
   A(("What are Concepts","Named sets of <b>compile-time constraints</b> on template parameters. "
      "Replaced SFINAE with readable syntax. Enable better error messages."),
     ("Syntax",
      "<pre>// Define a concept\ntemplate&lt;typename T&gt;\nconcept Addable = requires(T a, T b) { a + b; };\n\n"
      "// Use in function template\ntemplate&lt;Addable T&gt;\nT sum(T a, T b) { return a + b; }\n\n"
      "// Or with abbreviated template:\nAuto sum(Addable auto a, Addable auto b) { return a + b; }</pre>"),
     ("Standard Library Concepts","<code>std::integral</code>, <code>std::floating_point</code>, "
      "<code>std::same_as</code>, <code>std::convertible_to</code>, <code>std::ranges::range</code>, "
      "<code>std::invocable</code>"),
     ("Benefits","<ul><li>Readable error messages instead of template substitution walls</li>"
      "<li>Enables function overloading based on concept constraints</li>"
      "<li>Self-documenting templates</li></ul>"),
     ("Follow-ups",'<div class="followup">• What is the <code>requires</code> clause vs <code>requires</code> expression?<br>'
      '• How do concepts interact with overload resolution?<br>'
      '• What is a subsumption relationship between concepts?</div>'))),

  ("cpx006","Implement a thread-safe LRU Cache in C++","cpp","design","Hard",["Google","Meta","Nvidia","Databricks","Snowflake","Stripe"],88,
   "lru,thread-safe,unordered_map,list","Coding Round",
   A(("Design","<code>std::list</code> (doubly-linked list) + <code>std::unordered_map&lt;K, list::iterator&gt;</code>.<br>"
      "Most recently used at front. On access: move node to front. On eviction: remove from back."),
     ("Implementation",
      "<pre>template&lt;typename K, typename V&gt;\nclass LRUCache {\n    int cap;\n    std::list&lt;std::pair&lt;K,V&gt;&gt; lst;\n    std::unordered_map&lt;K, decltype(lst.begin())&gt; mp;\n    std::mutex mu;\npublic:\n    LRUCache(int cap) : cap(cap) {}\n\n    std::optional&lt;V&gt; get(const K&amp; key) {\n        std::lock_guard lock(mu);\n        auto it = mp.find(key);\n        if (it == mp.end()) return {};\n        lst.splice(lst.begin(), lst, it-&gt;second);  // move to front\n        return it-&gt;second-&gt;second;\n    }\n\n    void put(const K&amp; key, V val) {\n        std::lock_guard lock(mu);\n        if (mp.count(key)) lst.erase(mp[key]);\n        else if ((int)lst.size() == cap) {\n            mp.erase(lst.back().first);\n            lst.pop_back();\n        }\n        lst.push_front({key, val});\n        mp[key] = lst.begin();\n    }\n};</pre>"),
     ("Complexity","get/put: O(1) average. Thread-safe with a single mutex. "
      "For higher concurrency: use reader-writer lock or shard by key hash."),
     ("Follow-ups",'<div class="followup">• How would you implement LFU instead?<br>'
      '• How would you shard the cache for better concurrency?<br>'
      '• What is RCU (Read-Copy-Update) for lock-free reads?</div>'))),

  ("cpx007","What is the PIMPL idiom and why use it?","cpp","patterns","Medium",["Google","Meta","Apple","Cisco","VMware"],72,
   "pimpl,compilation-firewall,binary-compatibility","Coding Round",
   A(("PIMPL = Pointer to IMPLementation","Hide implementation details behind a pointer. "
      "Reduces compilation dependencies and enables ABI stability."),
     ("Example",
      "<pre>// widget.h (public header)\nclass Widget {\n    struct Impl;  // forward declaration\n    std::unique_ptr&lt;Impl&gt; pImpl;\npublic:\n    Widget();\n    ~Widget();  // must be defined where Impl is complete\n    void draw();\n};\n\n// widget.cpp\nstruct Widget::Impl { /* all private data here */ int x, y; SDL_Surface* surf; };\nWidget::Widget() : pImpl(std::make_unique&lt;Impl&gt;()) {}\nvoid Widget::draw() { /* use pImpl-&gt;x */ }</pre>"),
     ("Benefits","<ul><li><b>Compilation firewall:</b> header changes don't propagate to all users</li>"
      "<li><b>ABI stability:</b> adding private members doesn't break binary compatibility</li>"
      "<li><b>Encapsulation:</b> private data truly hidden</li></ul>"),
     ("Costs","Extra heap allocation, one level of indirection, requires explicit dtor definition."),
     ("Follow-ups",'<div class="followup">• How does PIMPL affect move semantics?<br>'
      '• What is the fast PIMPL (in-place storage)?<br>'
      '• Compare to using abstract interface (pure virtual).</div>'))),

  ("cpx008","std::string_view vs std::string — performance implications","cpp","language","Easy",_CPP,75,
   "string-view,non-owning,zero-copy","Coding Round",
   A(("std::string_view","A <b>non-owning, read-only view</b> into a character sequence. "
      "No heap allocation. Just a pointer + length. O(1) construction from any string-like object."),
     ("Performance Comparison",
      "<pre>// Bad: copies string for each call\nvoid log(std::string msg);\n\n// Good: zero-copy read\nvoid log(std::string_view msg);\n\n// Works with: string, const char*, string literals, substrings\nlog(\"hello\");         // no alloc\nlog(user_string);    // no alloc\nlog(str.substr(0,5)); // DANGER: substr returns string, but view is valid\n\n// Safe substring (zero-copy):\nlog(std::string_view(str).substr(0, 5));</pre>"),
     ("Dangers","<ul><li>Dangling reference if underlying string is destroyed</li>"
      "<li>Not null-terminated (can't pass to C APIs directly)</li>"
      "<li>Don't store string_view as a class member if source may outlive it</li></ul>"),
     ("Follow-ups",'<div class="followup">• What is std::span (C++20)?<br>'
      '• When must you use std::string over string_view?<br>'
      '• How does string_view enable SSO (Small String Optimization)?</div>'))),

  ("cpx009","What is EBO (Empty Base Optimization)?","cpp","optimization","Hard",["Google","Meta","Nvidia","Databricks"],64,
   "ebo,empty-base,sizeof,layout","Coding Round",
   A(("The Problem","C++ requires each complete object to have a unique address, so empty classes have size >= 1. "
      "But storing an empty allocator/comparator as a member wastes space:<br>"
      "<pre>struct Allocator {};  // sizeof = 1\nstruct MyContainer {\n    Allocator alloc;  // 1 byte (but likely padded to 8!)\n    size_t size;      // 8 bytes\n    // Total: 16 bytes instead of 8\n};</pre>"),
     ("EBO Solution","Inherit from the empty base instead of storing as member:<br>"
      "<pre>struct MyContainer : private Allocator {\n    size_t size;  // Allocator takes 0 bytes here!\n    // Total: 8 bytes\n};</pre>"),
     ("C++20 [[no_unique_address]]","Attribute that tells compiler it's OK for member to share address:<br>"
      "<pre>struct MyContainer {\n    [[no_unique_address]] Allocator alloc;\n    size_t size;  // 8 bytes total if Allocator is empty\n};</pre>"),
     ("Where it matters","std::vector, std::unique_ptr with stateless deleters, std::map with stateless comparators."),
     ("Follow-ups",'<div class="followup">• How does std::tuple implement EBO?<br>'
      '• What is compressed_pair? (Boost, LLVM)<br>'
      '• What is the standard layout requirement?</div>'))),

  ("cpx010","Implement a lock-free stack using CAS","cpp","concurrency","Hard",["Google","Meta","Nvidia","Databricks"],72,
   "lock-free,cas,atomic,stack","Coding Round",
   A(("Design","Use <code>std::atomic&lt;Node*&gt;</code> for head. CAS in a loop for push/pop."),
     ("Implementation",
      "<pre>template&lt;typename T&gt;\nclass LockFreeStack {\n    struct Node { T data; Node* next; };\n    std::atomic&lt;Node*&gt; head{nullptr};\npublic:\n    void push(T val) {\n        Node* n = new Node{std::move(val), nullptr};\n        n-&gt;next = head.load(std::memory_order_relaxed);\n        while (!head.compare_exchange_weak(n-&gt;next, n,\n               std::memory_order_release, std::memory_order_relaxed));\n    }\n    std::optional&lt;T&gt; pop() {\n        Node* old = head.load(std::memory_order_acquire);\n        while (old &amp;&amp; !head.compare_exchange_weak(old, old-&gt;next,\n               std::memory_order_release, std::memory_order_acquire));\n        if (!old) return {};\n        T val = std::move(old-&gt;data);\n        // DANGER: delete old  ← ABA problem / use-after-free with concurrent pops\n        return val;\n    }\n};</pre>"),
     ("ABA Problem","After loading <code>old = A</code>, another thread pops A, pushes B, pushes A back. "
      "CAS sees A and succeeds but <code>old-&gt;next</code> points to stale node. "
      "Fix: <b>tagged pointers</b> (version counter) or <b>hazard pointers</b> for safe memory reclamation."),
     ("Follow-ups",'<div class="followup">• What is the Michael-Scott lock-free queue?<br>'
      '• How do hazard pointers prevent use-after-free?<br>'
      '• When does lock-free actually outperform mutex? (high contention, many cores)</div>'))),

  ("cpx011","What are C++ ranges (C++20)?","cpp","language","Medium",["Google","Meta","Databricks","Snowflake"],68,
   "ranges,views,pipelines,lazy","Coding Round",
   A(("Ranges","C++20 Ranges provides <b>composable, lazy view pipelines</b> over sequences.<br>"
      "Key header: <code>&lt;ranges&gt;</code>, <code>&lt;algorithm&gt;</code> (constrained algorithms)"),
     ("Example",
      "<pre>#include &lt;ranges&gt;\n#include &lt;vector&gt;\n\nstd::vector&lt;int&gt; v = {1,2,3,4,5,6};\n\n// Lazy pipeline: filter evens, square them, take first 3\nauto result = v\n    | std::views::filter([](int x){ return x % 2 == 0; })\n    | std::views::transform([](int x){ return x * x; })\n    | std::views::take(3);\n\nfor (int x : result) std::cout &lt;&lt; x; // 4 16 36</pre>"),
     ("Key Views","<code>views::filter</code>, <code>views::transform</code>, <code>views::take</code>, "
      "<code>views::drop</code>, <code>views::reverse</code>, <code>views::iota</code>, <code>views::split</code>, <code>views::zip</code> (C++23)"),
     ("Lazy Evaluation","Views are <b>not evaluated until iterated</b>. No intermediate containers. "
      "Composing 5 views = single pass over data."),
     ("Follow-ups",'<div class="followup">• What is a range vs a view?<br>'
      '• What is std::ranges::to (C++23)?<br>'
      '• How do ranges enable better algorithm composition than iterators?</div>'))),

  ("cpx012","std::jthread vs std::thread (C++20)","cpp","concurrency","Medium",["Google","Meta","Nvidia"],68,
   "jthread,stop_token,thread","Concurrency Round",
   A(("Problem with std::thread","<code>std::thread</code> must be explicitly joined or detached before destruction. "
      "Forgetting calls <code>std::terminate()</code>. No built-in cooperative cancellation."),
     ("std::jthread","C++20 improvement: <b>automatically joins on destruction</b> (RAII). "
      "Built-in <b>cooperative cancellation</b> via <code>std::stop_token</code>."),
     ("Example",
      "<pre>std::jthread t([](std::stop_token st) {\n    while (!st.stop_requested()) {\n        do_work();\n        std::this_thread::sleep_for(100ms);\n    }\n    std::cout &lt;&lt; \"Stopping cleanly\\n\";\n});\n\nt.request_stop();  // signal cancellation\n// t.join() called automatically in destructor</pre>"),
     ("stop_source / stop_token","<code>stop_source</code> owns the stop state. "
      "<code>stop_token</code> is a read-only handle passed to threads. Multiple tokens from one source."),
     ("Follow-ups",'<div class="followup">• How does jthread compare to Golang goroutines with context?<br>'
      '• What is std::stop_callback?<br>'
      '• How do you implement a thread pool with jthread?</div>'))),
]

def _to_dict(q):
    return {
        "id": q[0], "text": q[1], "category": q[2], "subcategory": q[3],
        "difficulty": q[4], "companies": q[5], "frequency": q[6],
        "tags": q[7].split(","), "round_type": q[8], "answer_hint": q[9]
    }

QUESTIONS = [_to_dict(q) for q in CPP_EXT]
