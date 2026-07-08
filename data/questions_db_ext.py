"""Database Extended — B+Tree, MVCC, EXPLAIN, partitioning, replication, Redis, deadlocks."""

_DB = ["Google","Meta","Amazon","Microsoft","Uber","LinkedIn","Stripe","Razorpay","PhonePe","PayPal","Oracle"]
_IND = ["Razorpay","PhonePe","Swiggy","Zomato","CRED","Dream11","Groww"]

def A(*s):
    parts = [f'<span class="answer-label">{l}</span><br>{c}' for l,c in s]
    return '<div class="answer-section">'+'</div><div class="answer-section" style="margin-top:10px">'.join(parts)+'</div>'

DB_EXT = [
  ("dbx001","B+ Tree index internals — structure, splits, range queries","database","indexing","Hard",
   _DB, 88, "b-plus-tree,index,range-query,leaf-nodes","Database Round",
   A(("Structure","<ul><li><b>Internal nodes:</b> keys only, no data. Fan-out typically 100-200 keys per node.</li>"
      "<li><b>Leaf nodes:</b> keys + actual row pointers (or clustered data). Linked list for range scans.</li>"
      "<li><b>Height:</b> ~3-4 levels for millions of rows (log_200(1M) ≈ 3). Fits in memory.</li></ul>"),
     ("Why B+ over B-Tree","All data in leaves → range queries traverse leaf linked list without backtracking. "
      "Internal nodes store more keys (no data) → wider fan-out → shallower tree."),
     ("Operations",
      "<ul><li><b>Search:</b> O(log_t n) — traverse from root to leaf</li>"
      "<li><b>Insert:</b> find leaf, insert, split if overflow (cascade up)</li>"
      "<li><b>Delete:</b> find leaf, remove, merge or redistribute if underflow</li>"
      "<li><b>Range scan:</b> find start leaf, traverse linked list → sequential I/O (fast)</li></ul>"),
     ("Clustered vs Secondary","<b>Clustered:</b> Data rows stored in leaf nodes in index order (InnoDB primary key). "
      "One per table.<br><b>Secondary:</b> Leaf stores PK value → extra lookup for row data. Multiple allowed."),
     ("Follow-ups",'<div class="followup">• What is index selectivity and why does it matter?<br>'
      '• How does a covering index eliminate table lookups?<br>'
      '• Why is UUID a bad primary key for InnoDB? (random inserts → page splits)</div>'))),

  ("dbx002","PostgreSQL MVCC — how it achieves non-blocking reads","database","internals","Hard",
   _DB + _IND, 82, "mvcc,postgresql,snapshot,xmin,xmax","Database Round",
   A(("MVCC = Multi-Version Concurrency Control","Each row has hidden columns:<br>"
      "<ul><li><code>xmin</code>: transaction ID that inserted this version</li>"
      "<li><code>xmax</code>: transaction ID that deleted/updated this version (0 = still live)</li></ul>"
      "Reads see a <b>snapshot</b>: only versions where xmin ≤ snapshot_xid &lt; xmax."),
     ("How it works",
      "<pre>T1 (xid=100): UPDATE users SET name='Bob' WHERE id=1\n→ Old row: xmin=50, xmax=100  (now dead to T1)\n→ New row: xmin=100, xmax=0   (live)\n\nT2 (xid=99, started before T1):\n→ Sees old row (xmin=50 &lt;= 99 &lt; xmax=100) ✓\n→ Sees 'Alice' — no blocking!\n\nT3 (xid=101, started after T1 commits):\n→ Old row: xmax=100 &lt;= 101 → dead, skip\n→ New row: xmin=100 &lt;= 101, xmax=0 → live, sees 'Bob' ✓</pre>"),
     ("VACUUM","Dead rows (old versions) accumulate. <b>VACUUM</b> reclaims space. "
      "<b>AUTOVACUUM</b> runs automatically. Transaction ID wraparound prevented by freezing old rows."),
     ("Follow-ups",'<div class="followup">• What is HOT (Heap-Only Tuple) update in PostgreSQL?<br>'
      '• How does MVCC differ between PostgreSQL and MySQL InnoDB?<br>'
      '• What is transaction ID wraparound and why is it catastrophic?</div>'))),

  ("dbx003","EXPLAIN ANALYZE — reading query execution plans","database","query-optimization","Medium",
   _DB + _IND, 86, "explain,query-plan,seq-scan,index-scan,cost","Database Round",
   A(("Key Operations",
      "<ul><li><b>Seq Scan:</b> Full table scan. Fast for small tables / low selectivity.</li>"
      "<li><b>Index Scan:</b> Uses B+ tree index. Best for high selectivity (&lt;10% rows).</li>"
      "<li><b>Index Only Scan:</b> All needed columns in index (covering index). Fastest.</li>"
      "<li><b>Bitmap Heap Scan:</b> Index scan → bitmap of pages → sorted page access. Good for 5-20% rows.</li>"
      "<li><b>Nested Loop:</b> Join — for each outer row, find matching inner. Good for small outer result.</li>"
      "<li><b>Hash Join:</b> Build hash table from smaller table → probe with larger. Good for large unsorted.</li>"
      "<li><b>Merge Join:</b> Both sides sorted. Fast but needs sort step.</li></ul>"),
     ("Reading EXPLAIN",
      "<pre>EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 42;\n\n-&gt; Index Scan using idx_orders_user on orders\n   Index Cond: (user_id = 42)\n   rows=150 (estimated)  rows=143 (actual)\n   Buffers: shared hit=12  (pages from cache)\n   Planning: 0.3ms  Execution: 2.1ms</pre>"),
     ("Tuning Signals","<ul><li>Seq scan on large table with high selectivity → missing index</li>"
      "<li>Estimated rows ≫ actual → stale statistics → run ANALYZE</li>"
      "<li>Sort in plan → add index with ORDER BY columns</li>"
      "<li>Hash join with large table → may need work_mem increase</li></ul>"),
     ("Follow-ups",'<div class="followup">• What is the difference between cost and actual time in EXPLAIN?<br>'
      '• How does pg_stat_statements help identify slow queries?<br>'
      '• What is partial index and when does it help?</div>'))),

  ("dbx004","Database partitioning strategies — range, hash, list","database","scalability","Hard",
   _DB + _IND, 84, "partitioning,range,hash,list,pruning","Database Round",
   A(("Range Partitioning","Divide by value range. Common for time-series data.<br>"
      "<pre>CREATE TABLE orders (id bigint, created_at date, ...)\nPARTITION BY RANGE (created_at);\n\nCREATE TABLE orders_2023 PARTITION OF orders\n    FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');\nCREATE TABLE orders_2024 PARTITION OF orders\n    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');</pre>"
      "Pruning: <code>WHERE created_at &gt;= '2024-01-01'</code> → only scans 2024 partition."),
     ("Hash Partitioning","Distribute evenly by hash of key. Good for write distribution.<br>"
      "<pre>PARTITION BY HASH (user_id);\n-- Partition 0: user_id % 4 = 0\n-- Partition 1: user_id % 4 = 1 ...</pre>"),
     ("List Partitioning","By enumerated values. Good for geographic/categorical data.<br>"
      "<pre>PARTITION BY LIST (region);\n-- India: ('IN'), US: ('US','CA')</pre>"),
     ("Benefits","<ul><li>Partition pruning: query only relevant partition</li>"
      "<li>Faster VACUUM, index maintenance (smaller partitions)</li>"
      "<li>Easy archival: <code>DETACH PARTITION orders_2022</code></li></ul>"),
     ("Partitioning vs Sharding","Partitioning: single database, multiple internal tables. "
      "Sharding: multiple databases, data split across machines. Sharding requires application-level routing."),
     ("Follow-ups",'<div class="followup">• What is sub-partitioning?<br>'
      '• How does partition pruning work? (planner checks constraint exclusion)<br>'
      '• What are the limitations of cross-partition queries?</div>'))),

  ("dbx005","Read replicas — replication lag, use cases, consistency","database","replication","Hard",
   _DB + _IND, 88, "replication,replica-lag,read-replica,binlog","Database Round",
   A(("Replication Mechanics (MySQL binlog / PostgreSQL WAL)","Primary records every write as binary log events. "
      "Replica connects, streams binlog, applies changes. Replication can be:<br>"
      "<ul><li><b>Async (default):</b> Primary doesn't wait for replica. Replica may lag.</li>"
      "<li><b>Semi-sync:</b> Primary waits for at least 1 replica to acknowledge before committing.</li>"
      "<li><b>Sync (PostgreSQL synchronous_commit=on):</b> All replicas acknowledge. Highest durability, slowest.</li></ul>"),
     ("Replication Lag Causes","<ul><li>Large transactions (long to replay)</li>"
      "<li>High write throughput on primary</li>"
      "<li>Network latency between primary and replica</li>"
      "<li>Single-threaded replay (older MySQL — use parallel replication)</li></ul>"),
     ("Handling Lag in Applications","<ul><li>Read-your-own-writes: route reads after writes to primary for 1s, or use session stickiness</li>"
      "<li>For stale-tolerant reads (reports, analytics): use replica</li>"
      "<li>Monitor lag: <code>SHOW REPLICA STATUS</code> → Seconds_Behind_Source</li></ul>"),
     ("Follow-ups",'<div class="followup">• What is GTID-based replication?<br>'
      '• How does logical replication differ from physical replication?<br>'
      '• What is PgBouncer and what problem does it solve?</div>'))),

  ("dbx006","Redis data structures — use each for the right job","database","redis","Medium",
   _DB + _IND, 90, "redis,string,hash,sorted-set,list,hll","Database Round",
   A(("Data Structures",
      "<ul><li><b>String:</b> Simple KV, counters, JSON blobs, session tokens. <code>SET/GET/INCR/EXPIRE</code></li>"
      "<li><b>Hash:</b> Object fields. Better than JSON for partial updates. <code>HSET user:1 name Bob age 30</code></li>"
      "<li><b>List:</b> Task queue (LPUSH/RPOP), activity feed, bounded log. <code>LPUSH/RPOP/BRPOP</code></li>"
      "<li><b>Set:</b> Unique members, tags, online users. <code>SADD/SISMEMBER/SUNION/SINTER</code></li>"
      "<li><b>Sorted Set (ZSet):</b> Leaderboard, priority queue, rate limiting. Score-ordered. <code>ZADD/ZRANGE/ZRANK</code></li>"
      "<li><b>HyperLogLog:</b> Approximate cardinality counting (unique visitors). ~12KB, 0.8% error. <code>PFADD/PFCOUNT</code></li>"
      "<li><b>Streams:</b> Persistent append-only log. Consumer groups. Like Kafka in Redis.</li></ul>"),
     ("Common Patterns",
      "<pre># Rate limiter with sliding window\nZADD ratelimit:user1 {now_ms} {request_id}\nZREMRANGEBYSCORE ratelimit:user1 0 {window_start}\ncount = ZCARD ratelimit:user1\n\n# Leaderboard\nZADD leaderboard {score} {user}\nZREVRANGE leaderboard 0 9 WITHSCORES  # top 10\nZRANK leaderboard {user}               # rank</pre>"),
     ("Follow-ups",'<div class="followup">• What is Redis Cluster and how does slot sharding work?<br>'
      '• How does Redis WAIT command help with consistency?<br>'
      '• What is the difference between Redis persistence AOF vs RDB?</div>'))),

  ("dbx007","Database deadlocks — detection, prevention, resolution","database","concurrency","Hard",
   _DB + _IND, 82, "deadlock,lock,wait-for-graph,timeout","Database Round",
   A(("What is a Deadlock","Two or more transactions each hold a lock the other needs.<br>"
      "<pre>T1: LOCK A → wait for B\nT2: LOCK B → wait for A\n→ Circular wait = deadlock</pre>"),
     ("Deadlock Detection","Most DBs run a background detector (PostgreSQL, MySQL InnoDB).<br>"
      "Builds a <b>wait-for graph</b>: node = transaction, edge = T1 waits for lock held by T2. "
      "Cycle = deadlock → kill victim transaction (least expensive to rollback)."),
     ("Prevention Strategies",
      "<ul><li><b>Lock ordering:</b> Always acquire locks in the same global order (e.g., lower ID first)</li>"
      "<li><b>Timeout:</b> <code>SET lock_timeout = '1s'</code> — transaction aborts if wait too long</li>"
      "<li><b>SELECT FOR UPDATE SKIP LOCKED:</b> Skip locked rows instead of waiting (job queues)</li>"
      "<li><b>Reduce transaction scope:</b> Short transactions hold locks briefly</li></ul>"),
     ("Application-Level Fix",
      "<pre>-- Instead of long transaction:\nBEGIN;\n  UPDATE account SET bal = bal - 100 WHERE id = 1;  -- locks row\n  -- ... complex computation (seconds) ...\n  UPDATE account SET bal = bal + 100 WHERE id = 2;  -- deadlock risk!\nCOMMIT;\n\n-- Better: do computation outside transaction, then short UPDATE</pre>"),
     ("Follow-ups",'<div class="followup">• What is the difference between a deadlock and a livelock?<br>'
      '• How does SELECT FOR UPDATE NOWAIT differ from SKIP LOCKED?<br>'
      '• What is intention locking (IS, IX, S, X)?</div>'))),

  ("dbx008","Write-Ahead Logging (WAL) — how databases ensure durability","database","internals","Hard",
   _DB, 78, "wal,durability,redo-log,checkpoint","Database Round",
   A(("What is WAL","Before modifying data pages in memory (buffer pool), the change is written to the WAL log first. "
      "On crash: replay WAL from last checkpoint to recover committed transactions. "
      "<b>Guarantee:</b> committed data never lost, even on sudden crash."),
     ("Write Flow",
      "<pre>1. Transaction modifies data in buffer pool (in-memory dirty page)\n2. WAL record written to WAL buffer → flushed to disk (fsync)\n   [WAL written BEFORE data page written — Write-Ahead!]\n3. Transaction commits: commit WAL record flushed\n4. Background: dirty pages periodically checkpointed to data files\n5. WAL records before checkpoint can be deleted</pre>"),
     ("PostgreSQL WAL","WAL files in <code>pg_wal/</code>. Controls: <code>fsync=on</code> (durability), "
      "<code>synchronous_commit=on/off</code>. Turning off synchronous_commit: ~10% faster writes, risk of last 100ms of data on crash."),
     ("Uses beyond recovery","<ul><li>Streaming replication: replicas stream WAL from primary</li>"
      "<li>Point-in-time recovery (PITR): replay WAL to any past state</li>"
      "<li>Logical replication: parse WAL for row-level changes (Debezium/CDC)</li></ul>"),
     ("Follow-ups",'<div class="followup">• What is a checkpoint and why is checkpoint distance important?<br>'
      '• How does InnoDB redo log differ from PostgreSQL WAL?<br>'
      '• What is CDC (Change Data Capture) and how does it use WAL?</div>'))),

  ("dbx009","Connection pooling — PgBouncer, HikariCP, patterns","database","performance","Medium",
   _DB + _IND, 84, "connection-pool,pgbouncer,hikaricp,c3p0","Database Round",
   A(("Why Pool Connections","PostgreSQL creates a new OS process per connection (~5-10MB RAM). "
      "Opening connection takes ~30-100ms. 1000 connections = 5-10GB RAM, GC overhead, scheduler pressure."),
     ("PgBouncer","Lightweight connection pooler for PostgreSQL. Sits between app and DB.<br>"
      "<ul><li><b>Session mode:</b> App gets same DB connection for session duration. All features work.</li>"
      "<li><b>Transaction mode:</b> Connection returned to pool after each transaction. "
      "Supports many more app connections (1000s) with few DB connections (50). "
      "Restrictions: no SET, no prepared statements per session.</li>"
      "<li><b>Statement mode:</b> Return after each statement. Most restrictive.</li></ul>"),
     ("HikariCP (Java)","Fast JDBC connection pool.<br>"
      "<pre>HikariConfig cfg = new HikariConfig();\ncfg.setJdbcUrl(\"jdbc:postgresql://host/db\");\ncfg.setMaximumPoolSize(10);\ncfg.setConnectionTimeout(30000);\ncfg.setIdleTimeout(600000);\ncfg.setMaxLifetime(1800000);  // 30min to prevent stale conns\nDataSource ds = new HikariDataSource(cfg);</pre>"),
     ("Sizing","Pool size = (core_count × 2) + effective_spindle_count. Smaller than you think — more connections ≠ more throughput."),
     ("Follow-ups",'<div class="followup">• What is the difference between PgBouncer and pgpool-II?<br>'
      '• How do you handle connection leaks? (maxLifetime, leak detection)<br>'
      '• What is prepared statement caching and how does it interact with pooling?</div>'))),

  ("dbx010","Eventual consistency models — BASE, read-your-writes, monotonic reads","database","consistency","Hard",
   _DB + _IND, 82, "eventual-consistency,base,causal,monotonic","Database Round",
   A(("CAP Theorem Recap","In presence of network partition (P), choose between Consistency (C) or Availability (A). "
      "Most distributed systems choose AP → eventual consistency."),
     ("BASE (Basically Available, Soft state, Eventually consistent)","Contrast to ACID. "
      "<ul><li><b>Basically Available:</b> System works, even during partial failure (stale data OK)</li>"
      "<li><b>Soft State:</b> State may change without input (replication catching up)</li>"
      "<li><b>Eventually Consistent:</b> Given no new updates, all replicas converge to same state</li></ul>"),
     ("Consistency Models (weakest to strongest)",
      "<ul><li><b>Eventual:</b> Converges eventually. DNS, S3.</li>"
      "<li><b>Monotonic Read:</b> Once you read version V, you never see older version. (client stickiness)</li>"
      "<li><b>Read-Your-Writes:</b> You always see your own writes immediately. (session token pinning)</li>"
      "<li><b>Causal:</b> If A caused B, everyone sees A before B. (vector clocks)</li>"
      "<li><b>Sequential:</b> All operations appear in a global order consistent with program order.</li>"
      "<li><b>Linearizable (Strict):</b> Strongest. Operations appear instantaneous. ZooKeeper, etcd.</li></ul>"),
     ("Follow-ups",'<div class="followup">• How does DynamoDB implement eventual consistency vs strong consistency?<br>'
      '• What is quorum read/write (R + W &gt; N)?<br>'
      '• What are vector clocks and how do they enable causal consistency?</div>'))),

  ("dbx011","Time-series databases — InfluxDB, TimescaleDB, architecture","database","specialized","Medium",
   ["Google","Meta","Uber","Swiggy","Dream11","CRED"],74,"time-series,influxdb,timescaledb,retention","Database Round",
   A(("Why Special TSDBs","Regular relational DBs are poor for time-series: "
      "high write throughput, time-ordered data, bulk deletes (retention), time-range queries, downsampling."),
     ("TimescaleDB","PostgreSQL extension. Adds <b>hypertables</b> — automatically partitioned by time. "
      "Transparent to SQL. Best for: SQL queries + time-series. Compression: 90%+ space savings with native compression.<br>"
      "<pre>SELECT time_bucket('1 hour', time) AS hour,\n       avg(temperature)\nFROM metrics\nWHERE time &gt; NOW() - INTERVAL '7 days'\nGROUP BY hour\nORDER BY hour;</pre>"),
     ("InfluxDB","Purpose-built TSDB. Line protocol ingestion. InfluxQL or Flux query language. "
      "TSM (Time-Structured Merge Tree) storage engine optimized for time-ordered writes. "
      "Built-in retention policies, continuous queries (downsampling)."),
     ("LSM Tree for writes","Most TSDBs use LSM (Log-Structured Merge Tree): fast sequential writes, "
      "compaction merges SSTables. Optimized for write-heavy append patterns."),
     ("Follow-ups",'<div class="followup">• How do you implement data downsampling for long-term storage?<br>'
      '• What is Prometheus TSDB and how does it store metrics?<br>'
      '• When would you use ClickHouse over InfluxDB?</div>'))),

  ("dbx012","SQL query optimization — indexes, covering indexes, composite indexes","database","query-optimization","Medium",
   _DB + _IND, 88, "index,covering-index,composite,selectivity","Database Round",
   A(("Composite Index Column Order",
      "<pre>-- Query: WHERE a = 1 AND b &gt; 5 ORDER BY c\n-- Best index: (a, b, c) — leftmost prefix rule\n-- a → equality filter (most selective first)\n-- b → range filter\n-- c → ORDER BY (eliminates sort)\n\n-- Index (b, a) won't use b for range + a for equality efficiently</pre>"),
     ("Covering Index","Index includes all columns needed by query — no heap lookup.<br>"
      "<pre>-- Query:\nSELECT email FROM users WHERE user_id = 42;\n\n-- If index is (user_id, email): Index Only Scan — never touches table!\nCREATE INDEX idx_user_email ON users(user_id) INCLUDE (email);  -- PostgreSQL</pre>"),
     ("Index Selectivity","High selectivity (few rows per value) = good for index. "
      "Low selectivity (boolean, gender) = index often not used. "
      "<code>n_distinct</code> in pg_stats shows estimate. Use partial index for low-selectivity cases:<br>"
      "<code>CREATE INDEX ON orders(status) WHERE status = 'PENDING';</code>"),
     ("Anti-patterns","<ul><li><code>SELECT *</code> prevents covering index</li>"
      "<li>Function on indexed column: <code>WHERE LOWER(email) = ...</code> → can't use index. Use functional index.</li>"
      "<li>Leading % in LIKE: <code>WHERE name LIKE '%Smith'</code> → full scan. Use full-text search or reverse index.</li>"
      "<li>Implicit type cast: <code>WHERE varchar_col = 123</code> → type mismatch → seq scan</li></ul>"),
     ("Follow-ups",'<div class="followup">• What is an index bloat and how do you fix it?<br>'
      '• When does PostgreSQL ignore an index? (planner cost estimate)<br>'
      '• What is a filtered/partial index?</div>'))),
]

def _to_dict(q):
    return {"id":q[0],"text":q[1],"category":q[2],"subcategory":q[3],"difficulty":q[4],
            "companies":q[5],"frequency":q[6],"tags":q[7].split(","),"round_type":q[8],"answer_hint":q[9]}

QUESTIONS = [_to_dict(q) for q in DB_EXT]
