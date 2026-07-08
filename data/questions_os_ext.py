"""OS Extended — virtual memory, paging, copy-on-write, I/O models, epoll, NUMA, file systems."""

_OS = ["Google","Meta","Amazon","Microsoft","Nvidia","Apple","Databricks","Uber"]
_IND = ["Razorpay","PhonePe","Swiggy","Zomato","CRED"]

def A(*s):
    parts = [f'<span class="answer-label">{l}</span><br>{c}' for l,c in s]
    return '<div class="answer-section">'+'</div><div class="answer-section" style="margin-top:10px">'.join(parts)+'</div>'

OS_EXT = [
  ("osx001","Virtual memory — paging, page tables, TLB","os","memory","Hard",
   _OS + _IND, 88, "virtual-memory,paging,page-table,tlb","Coding Round",
   A(("Virtual Memory","Each process has its own virtual address space (e.g., 0 to 2^48 on 64-bit). "
      "OS maps virtual pages → physical frames via <b>page table</b>. "
      "Allows: isolation between processes, overcommit memory, memory-mapped files, copy-on-write."),
     ("Multi-level Page Tables","64-bit systems use 4-level (x86-64) or 5-level page tables to reduce space. "
      "Each level is a 4KB page of 512 8-byte entries. Virtual address split:<br>"
      "<pre>[sign ext | L4 (9) | L3 (9) | L2 (9) | L1 (9) | Offset (12)]</pre>"),
     ("TLB (Translation Lookaside Buffer)","Hardware cache for recent virtual→physical translations. "
      "TLB hit: 1 cycle. TLB miss: walk page table (several cycles + memory accesses). "
      "TLB flushed on context switch (unless ASID used). Huge pages (2MB/1GB) reduce TLB misses."),
     ("Page Fault","<ul><li><b>Minor:</b> Page in memory but not mapped (memory-mapped file, copy-on-write) → map it</li>"
      "<li><b>Major:</b> Page not in memory → read from disk (swap). Expensive (~ms)</li>"
      "<li><b>Invalid:</b> Access to unmapped address → SIGSEGV</li></ul>"),
     ("Follow-ups",'<div class="followup">• What is demand paging and how does it relate to exec()?<br>'
      '• What is transparent huge pages (THP) and when is it harmful? (database workloads)<br>'
      '• How does mmap() differ from malloc()?</div>'))),

  ("osx002","Copy-on-Write (COW) in fork() — how it works","os","memory","Medium",
   _OS, 84, "copy-on-write,fork,page-table,linux-kernel","Coding Round",
   A(("fork() without COW","Old approach: fork duplicates entire parent address space immediately. "
      "Expensive for large processes — most forked children exec() immediately, wasting the copy."),
     ("COW Optimization","After fork(), parent and child share the same physical pages (marked read-only). "
      "On first write by either process → page fault → OS copies only that page → independent copy.<br>"
      "<pre>fork()\n  → Page tables copied (cheap)\n  → Physical pages marked read-only + copy-on-write\n\nChild writes to variable x:\n  → Page fault (read-only violation)\n  → OS copies page → child gets private copy\n  → Child's page marked writable\n  → Parent still sees original</pre>"),
     ("Where COW is used","<ul><li>fork() in Unix/Linux</li>"
      "<li>mmap(MAP_PRIVATE): shared initially, COW on write</li>"
      "<li>Container images: layers are shared via COW (OverlayFS)</li>"
      "<li>Redis persistence: BGSAVE forks → COW allows snapshot without blocking writes</li></ul>"),
     ("Follow-ups",'<div class="followup">• What is vfork() and how does it differ from COW fork()?<br>'
      '• How does Redis BGSAVE use COW for non-blocking snapshots?<br>'
      '• What is the transparent huge page and COW interaction?</div>'))),

  ("osx003","I/O models — blocking, non-blocking, I/O multiplexing, async, signals","os","io","Hard",
   _OS + _IND, 90, "io-models,blocking,epoll,async-io,non-blocking","Coding Round",
   A(("5 I/O Models",
      "<ul><li><b>Blocking I/O:</b> Thread blocks until data ready. Simple. Scales poorly (1 thread/connection).</li>"
      "<li><b>Non-blocking I/O:</b> Returns EAGAIN immediately if no data. Polling loop wastes CPU.</li>"
      "<li><b>I/O Multiplexing (select/poll/epoll):</b> One thread watches many fds. Blocks on select, "
      "wakes when any fd ready. Efficient for many connections.</li>"
      "<li><b>Signal-driven I/O (SIGIO):</b> Signal when data ready. Complex, rarely used.</li>"
      "<li><b>Async I/O (AIO, io_uring):</b> Kernel does I/O, notifies completion. True async. "
      "io_uring (Linux 5.1+): submission/completion queues in shared memory, no syscall overhead.</li></ul>"),
     ("epoll vs select vs poll",
      "<ul><li><b>select:</b> fd_set bitmap, max 1024 fds, O(n) scan, copies fd_set each call</li>"
      "<li><b>poll:</b> array of pollfd, no 1024 limit, still O(n) scan</li>"
      "<li><b>epoll:</b> O(1) event notification. Register fds once (<code>epoll_ctl</code>), wait (<code>epoll_wait</code>) returns only ready fds. "
      "Kernel red-black tree for O(log n) add/remove. Level-triggered or edge-triggered modes.</li></ul>"),
     ("io_uring (Modern Linux)","Fully async: app submits I/O requests to SQ ring, kernel processes, "
      "posts completions to CQ ring. Zero syscall on fast path. Used in: Tokio (Rust), QEMU, PostgreSQL, Nginx."),
     ("Follow-ups",'<div class="followup">• What is edge-triggered vs level-triggered epoll?<br>'
      '• How does Node.js use libuv to implement the event loop?<br>'
      '• What is O_DIRECT and when would you use it?</div>'))),

  ("osx004","Deadlock — conditions, prevention, avoidance, detection","os","concurrency","Hard",
   _OS + _IND, 88, "deadlock,coffman,banker,prevention","Concurrency Round",
   A(("Coffman's Four Necessary Conditions",
      "<ul><li><b>Mutual Exclusion:</b> Resources not sharable</li>"
      "<li><b>Hold and Wait:</b> Process holds resource while waiting for another</li>"
      "<li><b>No Preemption:</b> Resources can't be forcibly taken</li>"
      "<li><b>Circular Wait:</b> T1→waits for T2→waits for T3→waits for T1</li></ul>"
      "Breaking <b>any one</b> prevents deadlock."),
     ("Prevention",
      "<ul><li><b>Eliminate Hold and Wait:</b> Request all resources at once before starting</li>"
      "<li><b>Allow Preemption:</b> If waiting, release held resources (costly)</li>"
      "<li><b>Eliminate Circular Wait:</b> Global ordering of resources (always lock in same order)</li></ul>"),
     ("Avoidance — Banker's Algorithm","Each process declares max resource claim. "
      "System checks if granting a request leaves system in <b>safe state</b> (all processes can complete). "
      "If unsafe → deny and wait. Used in theory; impractical for dynamic systems."),
     ("Detection and Recovery","Allow deadlocks to occur. Periodically run deadlock detector (wait-for graph cycle detection). "
      "Recovery: kill one victim process, or preempt + rollback resources."),
     ("Follow-ups",'<div class="followup">• How does Linux kernel handle deadlocks? (lockdep detector in debug build)<br>'
      '• What is a livelock vs deadlock?<br>'
      '• How does optimistic concurrency (OCC) avoid deadlocks?</div>'))),

  ("osx005","Process scheduling — CFS (Completely Fair Scheduler) in Linux","os","scheduling","Hard",
   _OS, 78, "cfs,scheduler,vruntime,red-black-tree,nice","Coding Round",
   A(("CFS Algorithm","CFS maintains a <b>virtual runtime (vruntime)</b> per process — "
      "time the process has run, weighted by priority (nice value). "
      "Always picks the process with <b>minimum vruntime</b> (leftmost node in red-black tree)."),
     ("vruntime Update",
      "<pre>vruntime += actual_runtime × (NICE_0_WEIGHT / task_weight)\n# Low-priority (high nice) tasks: vruntime increases faster → scheduled less\n# High-priority (low nice): vruntime increases slower → scheduled more</pre>"),
     ("Time Slice","No fixed time slice in CFS. Scheduling period (default 6ms) divided proportionally by weights. "
      "Minimum granularity: 0.75ms. Prevents starvation."),
     ("Priority Inheritance","When high-priority task blocks on mutex held by low-priority task → "
      "boost low-priority task's priority temporarily to prevent priority inversion (critical in RT systems)."),
     ("Follow-ups",'<div class="followup">• What is the difference between CFS and O(1) scheduler?<br>'
      '• What is nice value range and how does it map to weight?<br>'
      '• How does SCHED_FIFO differ from SCHED_OTHER (CFS)?</div>'))),

  ("osx006","Memory-mapped files (mmap) — mechanics and use cases","os","memory","Medium",
   _OS, 78, "mmap,memory-mapped,file-io,shared-memory","Coding Round",
   A(("How mmap works","<code>mmap()</code> maps a file or device into virtual address space. "
      "OS does NOT read file immediately — uses demand paging. "
      "Reading page triggers major page fault → kernel reads from file into physical page → mapped."),
     ("mmap vs read()/write()","<ul><li><b>read():</b> Kernel copies file data → kernel buffer → user buffer. Double copy.</li>"
      "<li><b>mmap():</b> Maps kernel page cache directly into user address space. Zero copy on access. "
      "Better for large files with random access.</li></ul>"),
     ("Shared Memory via mmap",
      "<pre>// Process A:\nint fd = open(\"/tmp/shm\", O_CREAT|O_RDWR, 0666);\nftruncate(fd, 4096);\nvoid* ptr = mmap(0, 4096, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0);\n\n// Process B: same mmap call — both map same physical pages\n// Writes by A immediately visible to B</pre>"),
     ("Use Cases","<ul><li>Databases: InnoDB buffer pool, SQLite, LMDB use mmap for zero-copy I/O</li>"
      "<li>Shared memory IPC: multiple processes sharing data structures</li>"
      "<li>Executable loading: kernel mmaps ELF segments — text, data, BSS</li>"
      "<li>io_uring: submission/completion queues mapped into user space</li></ul>"),
     ("Follow-ups",'<div class="followup">• What is the difference between MAP_SHARED and MAP_PRIVATE?<br>'
      '• What is msync() and when do you need it?<br>'
      '• How does mmap interact with the page cache?</div>'))),

  ("osx007","Spinlock vs Mutex vs Semaphore — detailed comparison","os","concurrency","Hard",
   _OS, 84, "spinlock,mutex,semaphore,busy-wait","Concurrency Round",
   A(("Spinlock","Thread loops (busy-waits) until lock is free. No OS involvement for uncontended case.<br>"
      "<b>Pros:</b> Near-zero overhead for very short critical sections, no context switch.<br>"
      "<b>Cons:</b> Wastes CPU if lock held long, terrible on uniprocessor, can cause priority inversion.<br>"
      "<b>Use when:</b> Critical section &lt;~100ns (kernel code, interrupt handlers, lock-free structures)."),
     ("Mutex","Thread puts itself to sleep if lock unavailable. OS wakes it when lock released.<br>"
      "<b>Pros:</b> No CPU waste while waiting, works with long critical sections.<br>"
      "<b>Cons:</b> Context switch overhead (~1-10μs), kernel involvement.<br>"
      "<b>Adaptive Mutex (Linux futex):</b> Spin briefly, then sleep. Best of both worlds."),
     ("Semaphore","Generalized mutex: can allow N concurrent holders (counting semaphore). "
      "Binary semaphore = mutex but can be released by different thread (unlike mutex, which must be released by owner). "
      "Use for: resource pools, producer-consumer signaling."),
     ("futex (Linux fast userspace mutex)","Check lock in userspace (atomic). "
      "Only make syscall when contended (wait/wake). Foundation of pthread_mutex, Java synchronized."),
     ("Follow-ups",'<div class="followup">• What is the difference between mutex and binary semaphore?<br>'
      '• What is priority inversion and how does priority inheritance solve it? (Mars Pathfinder bug)<br>'
      '• What are reader-writer locks and when do they help?</div>'))),

  ("osx008","Linux file system internals — inode, dentry, VFS, page cache","os","filesystem","Hard",
   _OS, 76, "inode,dentry,vfs,page-cache,ext4","Coding Round",
   A(("VFS (Virtual File System)","Abstraction layer. Provides uniform API (open/read/write/close) for all file systems "
      "(ext4, XFS, btrfs, tmpfs, NFS, procfs). Drivers implement VFS operations."),
     ("Inode","Fixed-size metadata structure for each file:<br>"
      "<ul><li>File type, permissions, owner (UID/GID)</li>"
      "<li>Size, timestamps (atime/mtime/ctime)</li>"
      "<li>Block pointers (direct, indirect, double-indirect)</li>"
      "<li>Link count (hard links)</li>"
      "<li><b>NOT:</b> file name (stored in directory entry)</li></ul>"),
     ("Dentry (Directory Entry)","Cache of name → inode mappings. "
      "Path lookup: <code>/home/user/file.txt</code> → traverse dentries: root dentry → home dentry → user dentry → file inode. "
      "Dentry cache (dcache) avoids repeated disk lookups."),
     ("Page Cache","Buffer for file data. read() → kernel checks page cache first. "
      "On miss: read from disk, cache page. write() → write to page cache (writeback=async), "
      "or writethrough, or direct I/O (O_DIRECT bypasses cache). "
      "<code>free</code> command: 'cached' = page cache using RAM (can be reclaimed)."),
     ("Follow-ups",'<div class="followup">• What is the difference between hard link and soft (symbolic) link?<br>'
      '• How does journaling (ext4) protect against filesystem corruption on crash?<br>'
      '• What is a union filesystem and how is it used in Docker?</div>'))),

  ("osx009","NUMA (Non-Uniform Memory Access) — impact on performance","os","hardware","Hard",
   ["Google","Meta","Nvidia","Databricks","Snowflake","Apple"],72,"numa,memory-locality,cpu-affinity","Coding Round",
   A(("NUMA Architecture","Multi-socket servers: each CPU socket has its own local DRAM. "
      "Accessing local memory: fast (~80ns). Accessing remote memory (other socket's DRAM): slow (~150ns, ~2x). "
      "OS/hardware provides NUMA node topology."),
     ("NUMA Problems","<ul><li>Thread on node 0 allocates, migrated to node 1 → remote memory access</li>"
      "<li>False sharing: different threads on different NUMA nodes modify same cache line → cache coherence traffic</li>"
      "<li>Memory-intensive apps (databases, ML) severely impacted</li></ul>"),
     ("Mitigation",
      "<ul><li><code>numactl --membind=0 --cpubind=0 ./app</code> — bind to single NUMA node</li>"
      "<li><code>numactl --interleave=all</code> — round-robin allocation across nodes (reduces hot-spots)</li>"
      "<li>NUMA-aware memory allocators (jemalloc, tcmalloc have NUMA support)</li>"
      "<li>Database NUMA awareness: MySQL/PostgreSQL can bind buffer pool per node</li></ul>"),
     ("Cache Hierarchy","L1 (4 cycles, 32KB per core) → L2 (12 cycles, 256KB per core) → "
      "L3 (30-50 cycles, shared per socket, 32-64MB) → DRAM (~200 cycles) → "
      "Remote DRAM (~400 cycles) → NVMe SSD (~100μs) → HDD (~10ms)."),
     ("Follow-ups",'<div class="followup">• What is cache line size and how does false sharing occur?<br>'
      '• How does CPU affinity (<code>taskset</code>) help performance?<br>'
      '• What is NUMA balancing in Linux?</div>'))),

  ("osx010","Context switching — cost, what is saved/restored","os","process","Medium",
   _OS + _IND, 86, "context-switch,registers,tlb-flush,process-vs-thread","Coding Round",
   A(("What is Context Switch","OS saving state of running process/thread and restoring another's. "
      "Triggered by: timer interrupt (preemption), syscall, I/O wait, voluntary yield."),
     ("Saved State",
      "<ul><li>CPU registers: PC (instruction pointer), SP (stack pointer), general-purpose registers, EFLAGS</li>"
      "<li>FPU/SIMD state (optional, lazy)</li>"
      "<li>TLB entries (or flush TLB on switch — expensive on older hardware)</li>"
      "<li>Process: page table base register (CR3 on x86) → TLB flush → 100s of ns extra</li>"
      "<li>Thread (same process): no page table switch → cheaper (~1-10μs vs ~10-100μs)</li></ul>"),
     ("Cost","Process switch: ~1-100μs depending on TLB state, cache warmth, address space size. "
      "Thread switch (same process): ~1-10μs. "
      "Goroutine/coroutine switch: ~100ns (no kernel, no TLB flush — all in userspace)."),
     ("Reducing Context Switches","<ul><li>Thread pools (avoid creation overhead)</li>"
      "<li>Async I/O / event loops (fewer threads, less switching)</li>"
      "<li>CPU affinity (keep thread on same core → warm L1/L2 cache)</li>"
      "<li>Lock-free algorithms (avoid blocking)</li></ul>"),
     ("Follow-ups",'<div class="followup">• What is ASID (Address Space ID) and how does it reduce TLB flushing?<br>'
      '• How does the Linux scheduler decide when to preempt? (timer interrupt + vruntime)<br>'
      '• What is voluntary vs involuntary context switch? (cs vs nvcswch in /proc/PID/status)</div>'))),
]

def _to_dict(q):
    return {"id":q[0],"text":q[1],"category":q[2],"subcategory":q[3],"difficulty":q[4],
            "companies":q[5],"frequency":q[6],"tags":q[7].split(","),"round_type":q[8],"answer_hint":q[9]}

QUESTIONS = [_to_dict(q) for q in OS_EXT]
