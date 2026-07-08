"""Security & Authentication interview questions with full answers."""

_ALL = ["Google","Meta","Amazon","Microsoft","Stripe","PayPal","Razorpay","PhonePe","CRED","Coinbase","LinkedIn","Uber"]
_FIN = ["Stripe","PayPal","Razorpay","PhonePe","CRED","Groww","Coinbase","Amazon"]

def A(*s):
    parts = [f'<span class="answer-label">{l}</span><br>{c}' for l,c in s]
    return '<div class="answer-section">'+'</div><div class="answer-section" style="margin-top:10px">'.join(parts)+'</div>'

_RAW = [
("sec001","OWASP Top 10 — explain and how to prevent each","security","appsec","Medium",
 _ALL, 88, "owasp,sql-injection,xss,csrf,security","Security Round",
 A(("Top 10 Vulnerabilities",
    "<ol><li><b>Injection (SQL/NoSQL/LDAP):</b> Use parameterized queries / prepared statements. Never concatenate user input.</li>"
    "<li><b>Broken Authentication:</b> Secure sessions, MFA, bcrypt passwords, account lockout after N failures.</li>"
    "<li><b>Sensitive Data Exposure:</b> TLS everywhere, encrypt PII at rest (AES-256), don't log sensitive data.</li>"
    "<li><b>XXE (XML External Entity):</b> Disable DTD processing in XML parsers.</li>"
    "<li><b>Broken Access Control:</b> Server-side authorization checks, deny by default, principle of least privilege.</li>"
    "<li><b>Security Misconfiguration:</b> Disable default credentials, disable directory listing, update dependencies.</li>"
    "<li><b>XSS (Cross-Site Scripting):</b> Escape output (HTMLEncode), Content-Security-Policy header.</li>"
    "<li><b>Insecure Deserialization:</b> Validate type/integrity before deserialization. Avoid Java native serialization.</li>"
    "<li><b>Vulnerable Components:</b> Dependency scanning (Snyk, Dependabot), SCA in CI pipeline.</li>"
    "<li><b>Insufficient Logging:</b> Log auth events, access control failures. Alert on anomalies. Protect log integrity.</li></ol>"),
  ("Follow-ups",'<div class="followup">• What is the difference between XSS and CSRF?<br>'
    '• How does a Content Security Policy (CSP) mitigate XSS?<br>'
    '• What is SSRF (Server-Side Request Forgery) and why is it critical in cloud environments?</div>'))),

("sec002","SQL Injection — how it works and prevention","security","appsec","Easy",
 _ALL[:8]+["TCS","Infosys","Wipro"], 92, "sql-injection,prepared-statements,parameterized","Security Round",
 A(("How it works",
    "<pre># Vulnerable code:\nquery = \"SELECT * FROM users WHERE name='\" + username + \"' AND pwd='\" + password + \"'\";\n\n# Attacker input: username = admin' --\n# Resulting query:\nSELECT * FROM users WHERE name='admin' --' AND pwd='anything'\n# -- comments out the password check → logged in as admin!\n\n# Even worse:\nusername = \"'; DROP TABLE users; --\"\n# Drops the entire users table!</pre>"),
  ("Prevention",
    "<pre># Java PreparedStatement:\nPreparedStatement stmt = conn.prepareStatement(\n    \"SELECT * FROM users WHERE name=? AND pwd=?\");\nstmt.setString(1, username);\nstmt.setString(2, hashedPassword);\n\n# Python SQLAlchemy:\nresult = db.execute(\"SELECT * FROM users WHERE name=:n\", {\"n\": username})\n\n# ORM (Hibernate/JPA): inherently parameterized\nUser user = em.createQuery(\"FROM User WHERE name=:n\", User.class)\n    .setParameter(\"n\", username).getSingleResult();</pre>"),
  ("Defense in depth",
    "<ul><li>Least privilege DB user (SELECT only for read, no DROP)</li>"
    "<li>WAF (Web Application Firewall) to detect patterns</li>"
    "<li>Input validation (whitelist expected characters)</li>"
    "<li>Error messages: never expose DB error details to client</li></ul>"),
  ("Follow-ups",'<div class="followup">• What is second-order SQL injection?<br>'
    '• How does NoSQL injection work in MongoDB? ($where, $regex)<br>'
    '• What is blind SQL injection and how do time-based blind attacks work?</div>'))),

("sec003","JWT — structure, validation, vulnerabilities","security","appsec","Medium",
 _ALL, 90, "jwt,rs256,alg-none,security,refresh-token","Security Round",
 A(("JWT Structure",
    "<pre>header.payload.signature\n\nHeader: {\"alg\": \"RS256\", \"typ\": \"JWT\"}\nPayload: {\"sub\": \"user123\", \"role\": \"admin\", \"exp\": 1700000000, \"iat\": 1699996400}\nSignature: RS256(base64url(header)+\".\"+base64url(payload), privateKey)\n\nVerification: RS256(received_header+\".\"+payload, publicKey) == received_signature</pre>"),
  ("Critical Vulnerabilities",
    "<ul><li><b>alg:none attack:</b> Attacker sets alg to 'none', removes signature. Old libraries accept it. "
    "Fix: whitelist allowed algorithms explicitly — NEVER accept alg from token.</li>"
    "<li><b>HS256 with public key:</b> If server uses RS256, attacker changes alg to HS256 and signs with the PUBLIC key. "
    "Server uses public key to verify HS256 = accepts! Fix: separate verify logic per algorithm.</li>"
    "<li><b>Weak secret (HS256):</b> Brute-force offline if secret is short. Use 256-bit+ random secrets.</li>"
    "<li><b>Missing expiry check:</b> Always validate exp claim.</li>"
    "<li><b>Sensitive data in payload:</b> JWT is base64 NOT encrypted. Anyone can decode it.</li></ul>"),
  ("Best Practices",
    "<ul><li>Use RS256 (asymmetric): private key signs, public key verifies — microservices can verify without shared secret</li>"
    "<li>Short access token TTL (15min) + refresh token (7-30 days in HttpOnly cookie)</li>"
    "<li>Store refresh tokens server-side for revocation capability</li>"
    "<li>Refresh token rotation: each use issues a new refresh token</li></ul>"),
  ("Follow-ups",'<div class="followup">• How do you revoke a JWT before it expires? (blocklist with Redis, or short TTL + refresh)<br>'
    '• What is the difference between JWS, JWE, and JWT?<br>'
    '• When would you use opaque tokens instead of JWT?</div>'))),

("sec004","HTTPS / TLS — how the handshake works","security","appsec","Medium",
 _ALL[:8]+["Cisco"], 88, "tls,certificate,handshake,pki,https","Networking Round",
 A(("TLS 1.3 Handshake (1-RTT)",
    "<pre>Client                          Server\n  |--ClientHello(suites,key_share)--&gt;|\n  |&lt;--ServerHello(suite,key_share,cert,verify,finished)--|\n  |  (key derived here — data flows!)    |\n  |--Finished-----------------------&gt;|\n  |==Encrypted Application Data========&gt;|</pre>"),
  ("Certificate Validation Chain",
    "<ul><li>Server presents certificate signed by Intermediate CA</li>"
    "<li>Intermediate CA cert signed by Root CA</li>"
    "<li>Root CA is pre-installed in OS/browser trust store</li>"
    "<li>Client verifies: signature chain, hostname (CN/SAN), not expired, not revoked (OCSP)</li></ul>"),
  ("Common Attacks & Defenses",
    "<ul><li><b>Man-in-the-Middle:</b> Prevented by certificate chain validation</li>"
    "<li><b>Downgrade attack:</b> Force TLS 1.0. Prevented by TLS_FALLBACK_SCSV</li>"
    "<li><b>Certificate pinning:</b> App expects specific cert/public key — HPKP or mobile pinning</li>"
    "<li><b>HSTS:</b> HTTP Strict Transport Security — browser always uses HTTPS for this domain</li></ul>"),
  ("Follow-ups",'<div class="followup">• What is mTLS (mutual TLS) and when is it used? (service-to-service auth)<br>'
    '• What is OCSP stapling and why does it improve performance?<br>'
    '• What is the difference between TLS 1.2 and TLS 1.3?</div>'))),

("sec005","Password hashing — bcrypt vs Argon2 vs PBKDF2","security","appsec","Medium",
 _FIN+["Google","Meta","Amazon"], 82, "bcrypt,argon2,password-hashing,salt,key-stretching","Security Round",
 A(("Why not MD5/SHA?",
    "MD5/SHA are fast → GPU can try billions/sec. Rainbow table: precompute hash for common passwords."),
  ("Password Hashing Algorithms",
    "<ul><li><b>bcrypt:</b> Work factor (cost). Each increment doubles computation. Built-in 128-bit salt. "
    "Memory-light (can be GPU-accelerated). Widely supported.</li>"
    "<li><b>Argon2 (winner of Password Hashing Competition 2015):</b> Memory-hard. Three variants: "
    "Argon2i (side-channel resistant), Argon2d (GPU-resistant), Argon2id (recommended — hybrid). "
    "Parameters: time, memory, parallelism.</li>"
    "<li><b>PBKDF2:</b> NIST/FIPS approved. Iterations + HMAC. Less memory-hard than Argon2. "
    "Required for some compliance frameworks.</li>"
    "<li><b>scrypt:</b> Memory-hard. Used by Litecoin. Harder to tune than Argon2.</li></ul>"),
  ("Best Practices",
    "<pre># Python — Argon2\nfrom argon2 import PasswordHasher\nph = PasswordHasher(time_cost=2, memory_cost=65536, parallelism=2)\nhash = ph.hash(\"user_password\")      # store this\nph.verify(hash, \"input_password\")    # True/False\n\n# Spring Security (bcrypt strength 12):\nPasswordEncoder encoder = new BCryptPasswordEncoder(12);\nString hash = encoder.encode(rawPassword);\nencoder.matches(rawPassword, hash);  // timing-safe comparison</pre>"),
  ("Follow-ups",'<div class="followup">• What is a timing attack on password comparison and how does constant-time comparison prevent it?<br>'
    '• How do you handle password migration from MD5 to bcrypt? (rehash on next login)<br>'
    '• What is credential stuffing and how does rate limiting + MFA prevent it?</div>'))),

("sec006","CSRF — Cross-Site Request Forgery attack and prevention","security","appsec","Medium",
 _ALL[:8], 84, "csrf,samesite,double-submit,token","Security Round",
 A(("How CSRF works",
    "<pre>1. User logs into bank.com (session cookie stored)\n2. User visits malicious.com\n3. malicious.com has hidden form:\n   &lt;form action=\"https://bank.com/transfer\" method=\"POST\"&gt;\n     &lt;input name=\"to\" value=\"attacker\"/&gt;\n     &lt;input name=\"amount\" value=\"10000\"/&gt;\n   &lt;/form&gt;\n   &lt;script&gt;document.forms[0].submit();&lt;/script&gt;\n4. Browser sends POST to bank.com with session cookie\n5. Bank.com sees valid session → transfers money!</pre>"),
  ("Prevention",
    "<ul><li><b>SameSite cookie attribute:</b> <code>SameSite=Strict</code> (never cross-site) or "
    "<code>SameSite=Lax</code> (top-level GET allowed). Modern browsers default to Lax.</li>"
    "<li><b>CSRF Token:</b> Server generates random token per session. Client includes in all state-changing requests. "
    "Server validates. Attacker can't read token from different origin.</li>"
    "<li><b>Double-Submit Cookie:</b> Token in both cookie and request body/header. Server checks they match.</li>"
    "<li><b>Custom Request Header:</b> <code>X-Requested-With: XMLHttpRequest</code>. Cross-origin forms can't set custom headers.</li></ul>"),
  ("CSRF vs XSS","XSS: inject script into target site. CSRF: trick user's browser to make authenticated request. "
    "XSS bypasses CSRF protection (can read CSRF token)."),
  ("Follow-ups",'<div class="followup">• Why don\'t APIs using Bearer tokens need CSRF protection? (browser doesn\'t auto-send Authorization header)<br>'
    '• What is clickjacking and how does X-Frame-Options prevent it?<br>'
    '• How does SameSite=None differ from SameSite=Lax?</div>'))),

("sec007","Role-based (RBAC) vs Attribute-based (ABAC) access control","security","appsec","Medium",
 ["Google","Meta","Amazon","Microsoft","LinkedIn","Stripe","Salesforce","Oracle"], 80,
 "rbac,abac,authorization,permissions","Security Round",
 A(("RBAC — Role-Based Access Control",
    "<pre>User → assigned Roles → Roles have Permissions\n\nRoles: ADMIN, EDITOR, VIEWER, BILLING\nPermissions: read:posts, write:posts, delete:posts, view:billing\n\nUser Alice: [EDITOR] → can read:posts + write:posts\nUser Bob:   [VIEWER] → can only read:posts\n\nSimple, performant, easy to audit. Rigid: can't express context-based rules.</pre>"),
  ("ABAC — Attribute-Based Access Control",
    "<pre>Policy: user.department == resource.department AND resource.classification &lt;= user.clearance\n\nRequest evaluated at runtime against policy engine (OPA — Open Policy Agent)\n\nAttributes:\n  Subject: {role, department, clearance, location}\n  Resource: {classification, owner, department, sensitivity}\n  Action: {read, write, delete}\n  Environment: {time, IP, MFA_verified}\n\nMore expressive but complex. Used in enterprise, healthcare, government.</pre>"),
  ("Implementation with OPA",
    "<pre># Rego policy (OPA):\nallow { input.user.role == \"admin\" }\nallow {\n    input.action == \"read\"\n    input.resource.owner == input.user.id\n}</pre>"),
  ("Follow-ups",'<div class="followup">• What is ReBAC (Relationship-Based Access Control) — Google Zanzibar?<br>'
    '• How do you implement row-level security in PostgreSQL?<br>'
    '• What is the principle of least privilege and how do you enforce it?</div>'))),

("sec008","Secrets management — best practices","security","appsec","Medium",
 _ALL[:8]+["Databricks","Snowflake","Coinbase"], 84, "secrets,vault,env-vars,rotation,hsm","Security Round",
 A(("Anti-patterns",
    "<ul><li>Hardcoded secrets in code → leaked to Git history forever</li>"
    "<li>Secrets in environment variables → visible in process list, crash dumps, logs</li>"
    "<li>Secrets in docker-compose.yml committed to repo</li>"
    "<li>Secrets passed as command-line args → visible in ps output</li></ul>"),
  ("HashiCorp Vault",
    "<pre># Dynamic secrets — Vault generates short-lived DB credentials per request\nvault read database/creds/my-role\n# Returns: {username: \"v-app-XyZ\", password: \"...\", lease_duration: \"1h\"}\n# Automatically revoked after 1h — no long-lived DB passwords!\n\n# App integration:\nVaultClient vault = new VaultClient(\"https://vault.internal\");\nString secret = vault.read(\"secret/data/db-password\").get(\"value\");</pre>"),
  ("Best Practices",
    "<ul><li><b>Vault / AWS Secrets Manager / GCP Secret Manager:</b> Centralized, audit-logged, auto-rotation</li>"
    "<li><b>Secret rotation:</b> Automatic rotation without app restart (blue-green credential rotation)</li>"
    "<li><b>Just-in-time secrets:</b> Request credential when needed, revoke immediately after</li>"
    "<li><b>Kubernetes:</b> Use external-secrets operator to sync from Vault/SM into K8s Secrets</li>"
    "<li><b>Git scanning:</b> TruffleHog, GitGuardian pre-commit hooks to prevent secret commits</li></ul>"),
  ("Follow-ups",'<div class="followup">• What is envelope encryption and how does AWS KMS implement it?<br>'
    '• How do you handle secret rotation without downtime?<br>'
    '• What is SPIFFE/SPIRE for workload identity?</div>'))),
]

def _to_dict(q):
    return {"id":q[0],"text":q[1],"category":q[2],"subcategory":q[3],"difficulty":q[4],
            "companies":q[5],"frequency":q[6],"tags":q[7].split(","),"round_type":q[8],"answer_hint":q[9]}

QUESTIONS = [_to_dict(q) for q in _RAW]
