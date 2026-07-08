"""Networking Extended — TCP details, TLS 1.3, HTTP/2, HTTP/3, QUIC, WebSocket, DNS, CORS, CDN."""

_NET = ["Google","Meta","Amazon","Microsoft","Uber","LinkedIn","Stripe","Razorpay","Cloudflare","Coinbase"]
_IND = ["Razorpay","PhonePe","Swiggy","Zomato","CRED","Dream11"]

def A(*s):
    parts = [f'<span class="answer-label">{l}</span><br>{c}' for l,c in s]
    return '<div class="answer-section">'+'</div><div class="answer-section" style="margin-top:10px">'.join(parts)+'</div>'

NET_EXT = [
  ("netx001","TCP 3-way handshake, 4-way termination, TIME_WAIT","networking","tcp","Medium",
   _NET + _IND, 92, "tcp,handshake,syn,syn-ack,time-wait","Networking Round",
   A(("3-Way Handshake (Connection Setup)",
      "<pre>Client ----- SYN (seq=x) --------&gt; Server\nClient &lt;---- SYN-ACK (seq=y,ack=x+1)- Server\nClient ----- ACK (ack=y+1) -------&gt; Server\n[Connection ESTABLISHED]\n\nSYN_SENT → SYN_RECEIVED → ESTABLISHED</pre>"
      "Purpose: synchronize initial sequence numbers, agree on connection parameters."),
     ("4-Way Termination",
      "<pre>Active  --- FIN ---&gt; Passive   (ACTIVE: FIN_WAIT_1)\nActive  &lt;-- ACK --- Passive   (ACTIVE: FIN_WAIT_2)\nActive  &lt;-- FIN --- Passive   (PASSIVE: sends own FIN)\nActive  --- ACK --&gt; Passive   (ACTIVE: TIME_WAIT → CLOSED after 2×MSL)\n</pre>"),
     ("TIME_WAIT (2×MSL ≈ 60s-4min)","<ul><li>Ensures last ACK reaches passive closer</li>"
      "<li>Prevents old duplicate packets from confusing new connection on same port</li>"
      "<li>Causes: Cannot reuse port immediately. <code>SO_REUSEADDR</code> allows reuse in server context.</li></ul>"),
     ("Follow-ups",'<div class="followup">• Why does the client go into TIME_WAIT, not the server?<br>'
      '• What is SYN flood attack and how is SYN cookies a defense?<br>'
      '• What is TCP Fast Open (TFO)?</div>'))),

  ("netx002","TCP flow control (receive window) vs congestion control (CWND)","networking","tcp","Hard",
   _NET, 82, "tcp,flow-control,congestion,cwnd,rwnd","Networking Round",
   A(("Flow Control (Receiver-side)","Prevents sender from overwhelming receiver's buffer.<br>"
      "Receiver advertises <b>receive window (rwnd)</b> in ACK headers. "
      "Sender must not have more than rwnd unacknowledged bytes in flight."),
     ("Congestion Control (Network-side)","Prevents sender from overwhelming the network (routers/links).<br>"
      "Sender maintains <b>congestion window (cwnd)</b>. Effective window = min(cwnd, rwnd)."),
     ("Congestion Control Phases",
      "<ul><li><b>Slow Start:</b> cwnd=1 MSS → doubles each RTT until ssthresh or packet loss</li>"
      "<li><b>Congestion Avoidance:</b> cwnd grows +1 MSS per RTT (linear)</li>"
      "<li><b>Fast Retransmit:</b> 3 duplicate ACKs → retransmit lost segment immediately (don't wait for timeout)</li>"
      "<li><b>Fast Recovery (CUBIC, BBR):</b> On loss: ssthresh = cwnd/2, cwnd = ssthresh (not back to 1)</li></ul>"),
     ("BBR (Google)","Model-based congestion control. Estimates bottleneck bandwidth and RTT. "
      "Less reactive to loss, better for high-bandwidth long-distance links. Used in YouTube, cloud networking."),
     ("Follow-ups",'<div class="followup">• What is buffer bloat and how does it cause high latency?<br>'
      '• What is ECN (Explicit Congestion Notification)?<br>'
      '• How does QUIC handle congestion control differently from TCP?</div>'))),

  ("netx003","TLS 1.3 handshake — 1-RTT and 0-RTT","networking","tls","Hard",
   _NET + _IND, 86, "tls,tls1.3,handshake,ecdhe,session-ticket","Networking Round",
   A(("TLS 1.3 Full Handshake (1-RTT)",
      "<pre>Client → Server: ClientHello + key_share (ECDHE public key) + supported ciphers\nServer → Client: ServerHello + key_share (server ECDHE public key)\n                  + Certificate + CertificateVerify + Finished\n[Both derive session keys immediately from shared ECDHE secret]\nClient → Server: Finished + HTTP request\n[TLS 1.2 needed 2-RTT; TLS 1.3 = 1-RTT]</pre>"),
     ("0-RTT Session Resumption","Client stores <b>session ticket</b> from previous connection. "
      "On reconnect, sends early data in first packet — zero round trips before HTTP request. "
      "<b>Risk:</b> replay attacks (early data not protected against replay). Mitigate: use only for idempotent requests."),
     ("Key Improvements over TLS 1.2",
      "<ul><li>1-RTT instead of 2-RTT for new connections</li>"
      "<li>Forward secrecy mandatory: ECDHE always used (ephemeral keys)</li>"
      "<li>Removed weak algorithms: RSA key exchange, RC4, SHA-1, MD5</li>"
      "<li>Encrypted handshake: Certificate encrypted (hidden from observers)</li></ul>"),
     ("Certificate Verification","Client verifies server cert chain up to trusted CA root. "
      "CT (Certificate Transparency) logs prevent mis-issuance. OCSP stapling for revocation."),
     ("Follow-ups",'<div class="followup">• What is perfect forward secrecy and why does ECDHE provide it?<br>'
      '• How does mTLS (mutual TLS) work for service-to-service auth?<br>'
      '• What is certificate pinning and when is it used?</div>'))),

  ("netx004","HTTP/2 vs HTTP/3 (QUIC) — feature comparison","networking","http","Hard",
   _NET + _IND, 88, "http2,http3,quic,multiplexing,head-of-line","Networking Round",
   A(("HTTP/2 Features",
      "<ul><li><b>Multiplexing:</b> Multiple streams over one TCP connection. No request queuing.</li>"
      "<li><b>Header compression (HPACK):</b> Reduce redundant headers (cookies, user-agent)</li>"
      "<li><b>Server push:</b> Server proactively sends resources before client requests</li>"
      "<li><b>Binary framing:</b> Efficient parsing vs text-based HTTP/1.1</li>"
      "<li><b>Stream priority:</b> Weighted dependency tree</li>"
      "<li><b>Problem:</b> TCP head-of-line blocking — one lost packet blocks ALL streams</li></ul>"),
     ("HTTP/3 / QUIC",
      "<ul><li>Runs over <b>UDP</b>, not TCP. Implements reliable delivery in userspace.</li>"
      "<li><b>Stream-level reliability:</b> Lost packet blocks only affected stream, not all</li>"
      "<li><b>0-RTT connection setup:</b> QUIC + TLS 1.3 combined handshake (1-RTT new, 0-RTT resume)</li>"
      "<li><b>Connection migration:</b> Connection ID-based, survives IP change (WiFi → 4G)</li>"
      "<li><b>QPACK:</b> Header compression without HOL blocking (vs HPACK)</li></ul>"),
     ("When HTTP/3 helps","High latency (mobile), packet loss, many parallel requests, "
      "clients switching networks. Major adopters: Google, Meta, Cloudflare, YouTube."),
     ("Follow-ups",'<div class="followup">• What is head-of-line blocking at TCP level?<br>'
      '• Why does QUIC run over UDP instead of redesigning TCP?<br>'
      '• How does server push in HTTP/2 compare to HTTP/103 Early Hints?</div>'))),

  ("netx005","WebSocket — upgrade, framing, use cases vs SSE vs long polling","networking","websockets","Medium",
   _NET + _IND, 86, "websocket,sse,long-polling,upgrade,full-duplex","Networking Round",
   A(("WebSocket Upgrade",
      "<pre>Client Request:\nGET /chat HTTP/1.1\nConnection: Upgrade\nUpgrade: websocket\nSec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\n\nServer Response:\nHTTP/1.1 101 Switching Protocols\nUpgrade: websocket\nConnection: Upgrade\nSec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=\n[TCP connection stays open — full duplex from now]</pre>"),
     ("WebSocket Frame","Binary or text frames. Control frames: ping/pong/close. "
      "Low overhead: 2-14 byte header vs HTTP's ~500 byte headers per request."),
     ("Comparison",
      "<ul><li><b>WebSocket:</b> Full-duplex, persistent, binary/text. Chat, gaming, trading, collaboration.</li>"
      "<li><b>SSE (Server-Sent Events):</b> Server→client only, over HTTP/1.1, auto-reconnect. Dashboards, notifications. Simpler than WS.</li>"
      "<li><b>Long Polling:</b> Client holds HTTP request open until server has data. Fallback. High latency, wasteful.</li></ul>"),
     ("Scaling WebSockets","Stateful — connection pinned to server. Use:<br>"
      "<ul><li>Sticky sessions (HAProxy/Nginx)</li>"
      "<li>Message broker for fan-out: Pub/Sub via Redis, Kafka, or NATS</li>"
      "<li>Socket.IO: WS with fallback to long-polling</li></ul>"),
     ("Follow-ups",'<div class="followup">• How do you handle WebSocket reconnection with message replay?<br>'
      '• What is a WebSocket subprotocol?<br>'
      '• How does HTTP/2 server push compare to WebSocket for server→client messaging?</div>'))),

  ("netx006","DNS resolution — full chain from browser to authoritative server","networking","dns","Medium",
   _NET + _IND, 88, "dns,resolver,authoritative,recursive,ttl","Networking Round",
   A(("Full Resolution Chain",
      "<pre>1. Browser cache (TTL based)\n2. OS cache / /etc/hosts\n3. Stub Resolver → Recursive Resolver (ISP or 8.8.8.8)\n4. Recursive Resolver cache\n5. Root Name Server (\".\" zone) → returns NS for .com\n6. TLD Name Server (.com zone) → returns NS for google.com\n7. Authoritative Name Server (google.com zone) → returns A record\n8. Recursive Resolver caches result (TTL seconds)\n9. Returns to client → browser connects</pre>"),
     ("Record Types",
      "<ul><li><b>A:</b> Domain → IPv4</li><li><b>AAAA:</b> Domain → IPv6</li>"
      "<li><b>CNAME:</b> Alias → canonical name (followed recursively)</li>"
      "<li><b>MX:</b> Mail exchange server</li><li><b>TXT:</b> SPF, DKIM, domain verification</li>"
      "<li><b>NS:</b> Authoritative name servers for domain</li>"
      "<li><b>SRV:</b> Service discovery (host + port + priority)</li></ul>"),
     ("DNS in Kubernetes","CoreDNS runs as a pod. Service DNS: <code>&lt;service&gt;.&lt;namespace&gt;.svc.cluster.local</code>. "
      "Pods: <code>&lt;pod-ip&gt;.&lt;namespace&gt;.pod.cluster.local</code>."),
     ("Follow-ups",'<div class="followup">• What is DNSSEC and what does it protect against?<br>'
      '• How does DNS-based load balancing work? (multiple A records, low TTL)<br>'
      '• What is negative caching (NXDOMAIN) and its TTL?</div>'))),

  ("netx007","Load balancer algorithms — round-robin, least-connections, consistent hashing","networking","load-balancing","Medium",
   _NET + _IND, 90, "load-balancer,round-robin,consistent-hashing,least-conn","Networking Round",
   A(("Algorithms",
      "<ul><li><b>Round Robin:</b> Requests distributed evenly in rotation. Simple, ignores server load.</li>"
      "<li><b>Weighted Round Robin:</b> Servers with higher weight get more requests. For heterogeneous servers.</li>"
      "<li><b>Least Connections:</b> Route to server with fewest active connections. Better for varying request durations.</li>"
      "<li><b>Least Response Time:</b> Combines active connections + response latency.</li>"
      "<li><b>IP Hash:</b> Hash client IP → fixed server. Session stickiness (but unbalanced if some IPs dominate).</li>"
      "<li><b>Random with 2 Choices (Power of Two):</b> Pick 2 random servers, choose less loaded. Near-optimal, simple.</li></ul>"),
     ("Consistent Hashing","Used for stateful routing (cache sharding, WebSocket servers).<br>"
      "Hash ring: servers placed on ring. Request hashed → clockwise to nearest server. "
      "Adding/removing server only remaps 1/N of keys (vs modulo hashing remaps all)."),
     ("L4 vs L7 Load Balancer",
      "<ul><li><b>L4 (Transport):</b> Routes by TCP/UDP (IP + port). Faster, less overhead. No content awareness.</li>"
      "<li><b>L7 (Application):</b> Routes by HTTP headers, URL, cookies. Content-based routing, SSL termination, retries.</li></ul>"),
     ("Follow-ups",'<div class="followup">• How does HAProxy differ from Nginx as a load balancer?<br>'
      '• What are virtual nodes in consistent hashing and why are they needed?<br>'
      '• How does a global load balancer (Anycast, GeoDNS) work?</div>'))),

  ("netx008","REST vs gRPC vs GraphQL vs WebSocket — when to use each","networking","api","Medium",
   _NET + _IND, 90, "rest,grpc,graphql,websocket,api-design","System Design Round",
   A(("REST","HTTP/1.1 or 2, JSON/XML. Stateless, simple, widely supported. "
      "Cacheable (GET), intuitive with HTTP verbs. "
      "Cons: over-fetching/under-fetching, multiple round trips for related data. "
      "Best for: public APIs, simple CRUD, browser-to-server."),
     ("gRPC","HTTP/2 + Protocol Buffers. Binary, strongly typed, multiplexed. 5-10x smaller payload than JSON. "
      "Bidirectional streaming, connection reuse. Generated client/server code. "
      "Cons: not human-readable, no native browser support (grpc-web workaround). "
      "Best for: internal microservice communication, real-time streaming, polyglot services."),
     ("GraphQL","Single endpoint, client specifies exact data shape. Eliminates over-fetching. "
      "Subscriptions for real-time. Schema as contract. "
      "Cons: N+1 problem (use DataLoader), complex caching (no HTTP cache headers), schema overhead. "
      "Best for: complex UIs with diverse data needs (mobile apps, dashboards)."),
     ("WebSocket","Full-duplex, persistent TCP connection. Low-latency bidirectional. "
      "Best for: chat, live collaboration, gaming, stock tickers, notifications."),
     ("Quick Decision",
      "<ul><li>Public CRUD API → REST</li><li>Microservice-to-microservice → gRPC</li>"
      "<li>Complex queries, mobile app → GraphQL</li>"
      "<li>Real-time bidirectional → WebSocket</li><li>Server→client notifications → SSE</li></ul>"),
     ("Follow-ups",'<div class="followup">• How does gRPC handle service discovery?<br>'
      '• What is the N+1 problem in GraphQL and how does DataLoader solve it?<br>'
      '• How do you version a REST API vs a GraphQL API?</div>'))),

  ("netx009","CDN architecture — how content is cached and served","networking","cdn","Medium",
   _NET + _IND, 84, "cdn,edge,pop,cache-control,anycast","System Design Round",
   A(("CDN Architecture","<b>Points of Presence (PoPs):</b> Edge servers distributed globally (Cloudflare: 300+ PoPs, Akamai: 4000+). "
      "User request routed to nearest PoP via <b>Anycast</b> (same IP, BGP routes to nearest datacenter) or GeoDNS."),
     ("Cache Flow",
      "<pre>User → CDN Edge (PoP)\n  → Cache HIT: return immediately (&lt;5ms)\n  → Cache MISS: fetch from origin (100-300ms), cache response, serve\n\nSubsequent users at same PoP → cache HIT\nUsers at different PoP → may still be cache MISS (PoP-local cache)</pre>"),
     ("Cache Control Headers",
      "<pre>Cache-Control: max-age=31536000, immutable     # 1 year, static assets\nCache-Control: max-age=60, stale-while-revalidate=30  # 1min fresh, serve stale while revalidating\nCache-Control: no-store                         # never cache (auth pages)\nSurrogate-Control: max-age=3600                 # CDN-only hint (Varnish/Fastly)\nVary: Accept-Encoding                           # different cache per encoding</pre>"),
     ("Dynamic Content","Not all content is cacheable. Edge computing (Cloudflare Workers, Lambda@Edge) "
      "runs logic at edge. For personalized content: cache fragment (Edge Side Includes) or stream-stitch."),
     ("Follow-ups",'<div class="followup">• How do you purge CDN cache? (cache invalidation API, cache tags)<br>'
      '• What is cache stampede / thundering herd and how to prevent it?<br>'
      '• How does TLS termination at CDN edge work?</div>'))),

  ("netx010","CORS — same-origin policy, preflight, headers","networking","web-security","Medium",
   _NET + _IND, 86, "cors,same-origin,preflight,access-control","Networking Round",
   A(("Same-Origin Policy","Browser blocks cross-origin requests by default. "
      "Origin = scheme + host + port. <code>https://api.com:443</code> ≠ <code>http://api.com:80</code>."),
     ("Simple vs Preflight Requests","<b>Simple:</b> GET/POST/HEAD with safe headers → no preflight. "
      "Browser sends request with <code>Origin</code> header; server must return <code>Access-Control-Allow-Origin</code>.<br><br>"
      "<b>Preflight (OPTIONS):</b> Triggered for: non-simple methods (PUT/DELETE/PATCH), custom headers, content-type=application/json.<br>"
      "<pre>OPTIONS /api/data HTTP/1.1\nOrigin: https://app.example.com\nAccess-Control-Request-Method: DELETE\nAccess-Control-Request-Headers: Authorization\n\n--- Server response:\nAccess-Control-Allow-Origin: https://app.example.com\nAccess-Control-Allow-Methods: GET, POST, DELETE\nAccess-Control-Allow-Headers: Authorization\nAccess-Control-Max-Age: 86400  # cache preflight for 1 day</pre>"),
     ("Credentialed Requests","Cookies/auth headers in cross-origin require:<br>"
      "<code>Access-Control-Allow-Credentials: true</code> AND <code>Access-Control-Allow-Origin</code> must be specific (not *)."),
     ("Follow-ups",'<div class="followup">• Does CORS prevent all cross-origin attacks? (No — doesn\'t protect server from CSRF)<br>'
      '• What is CSRF and how is it different from what CORS prevents?<br>'
      '• How does a wildcard origin (*) work with credentials?</div>'))),

  ("netx011","OAuth 2.0 flows — Authorization Code, Client Credentials, PKCE","networking","auth","Hard",
   _NET + _IND, 86, "oauth2,authorization-code,pkce,client-credentials","Networking Round",
   A(("Authorization Code Flow (Web Apps)",
      "<pre>1. User clicks 'Login with Google'\n2. App redirects to Google: /auth?client_id=..&amp;redirect_uri=..&amp;scope=email&amp;state=random\n3. User logs in on Google, grants consent\n4. Google redirects to app with ?code=AUTH_CODE&amp;state=...\n5. App server exchanges code for tokens: POST /token {code, client_secret}\n6. Gets: access_token (short-lived), refresh_token (long-lived)\n7. App uses access_token to call APIs on user's behalf</pre>"),
     ("PKCE (Proof Key for Code Exchange)","For mobile/SPA apps that can't store client_secret securely.<br>"
      "<ul><li>App generates <code>code_verifier</code> (random), <code>code_challenge = SHA256(verifier)</code></li>"
      "<li>Sends challenge in auth request, sends verifier in token exchange</li>"
      "<li>Server verifies: SHA256(verifier) == challenge → prevents auth code interception</li></ul>"),
     ("Client Credentials (Machine-to-Machine)",
      "<pre>POST /token\nclient_id=svc1&amp;client_secret=secret&amp;grant_type=client_credentials\n→ access_token (no user context)\n# Used for: microservice-to-microservice, background jobs</pre>"),
     ("JWT Access Token","Access tokens are often JWTs: <code>header.payload.signature</code>. "
      "Resource servers validate signature without calling authorization server. "
      "Payload contains: sub (user), iat, exp, scope, aud."),
     ("Follow-ups",'<div class="followup">• What is the difference between OAuth 2.0 and OpenID Connect (OIDC)?<br>'
      '• How do you revoke an access token before expiry?<br>'
      '• What is the device authorization grant flow?</div>'))),
]

def _to_dict(q):
    return {"id":q[0],"text":q[1],"category":q[2],"subcategory":q[3],"difficulty":q[4],
            "companies":q[5],"frequency":q[6],"tags":q[7].split(","),"round_type":q[8],"answer_hint":q[9]}

QUESTIONS = [_to_dict(q) for q in NET_EXT]
