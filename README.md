# ⚡ Interview Repository — Backend SDE-1/2 Prep Hub

A complete static HTML website with **201+ curated interview questions** across **50 companies** and **8 company tiers**, targeted at SDE-1 / SDE-2 Backend Engineering roles in **C++, Java, and Go**.

## 📦 Project Structure

```
InterViewQuestionScraper/
├── generate_site.py          # Main generator — run this to build the site
├── data/
│   ├── companies.json        # All 50 companies across 8 tiers with metadata
│   ├── questions_coding.py   # 80 DSA/Coding questions (arrays, strings, trees, graphs, DP...)
│   └── questions_other.py    # 121 questions (Backend, C++, Java, Go, System Design, DB, OS, Net)
├── assets/
│   ├── css/style.css         # Dark theme responsive CSS
│   └── js/main.js            # Search, tabs, filters, animations
└── InterviewRepository/      # Generated output (open index.html here)
    ├── index.html
    ├── tier-1-elite/         google.html, meta.html, openai.html, stripe.html ...
    ├── tier-2-top-product/   uber.html, airbnb.html, linkedin.html, microsoft.html ...
    ├── tier-3-strong-product/
    ├── tier-4-upper-product/
    ├── tier-5-indian-unicorn/
    ├── tier-6-large-product/
    ├── tier-7-midsize-tech/
    ├── tier-8-service-based/
    ├── common/               top-coding.html, top-system-design.html, top-cpp.html ...
    ├── search-index.json     # Full-text search index (1100+ entries)
    ├── questions-meta.json   # All questions with metadata
    └── companies-meta.json   # All companies with metadata
```

## 🚀 Quick Start

### Build the site
```bash
python generate_site.py
```

### Serve locally
```bash
# Python (built-in)
cd InterviewRepository
python -m http.server 8080

# Then open: http://localhost:8080
```

### Rebuild after changes
```bash
rebuild.bat          # Windows
python generate_site.py  # Any platform
```

## 🏢 Companies Covered (50 total)

| Tier | Label | Companies |
|------|-------|-----------|
| 1 | Elite | Google, Meta, OpenAI, Stripe, Databricks, Snowflake |
| 2 | Top Product | Uber, Airbnb, LinkedIn, Microsoft, Apple, Netflix |
| 3 | Strong Product | Amazon, Atlassian, Adobe, Salesforce, Coinbase, Nvidia |
| 4 | Upper Product | Walmart, PayPal, Oracle, Cisco, VMware, ServiceNow |
| 5 | Indian Unicorn | Razorpay, PhonePe, Swiggy, Zomato, Meesho, Groww, CRED |
| 6 | Large Product | Expedia, InMobi, Freshworks, Zoho, Dream11, BrowserStack |
| 7 | Midsize Tech | Persistent, LTIMindtree, GlobalLogic, EPAM, Nagarro |
| 8 | Service Based | TCS, Infosys, Wipro, Cognizant, Accenture, HCL, Tech Mahindra, Capgemini |

## 📚 Question Categories

| Category | Count | Topics |
|----------|-------|--------|
| Coding / DSA | 80 | Arrays, Strings, Trees, Graphs, DP, Heap, Backtracking, Binary Search, Design |
| Backend | 20 | REST/gRPC/GraphQL, Kafka, Rate Limiting, Distributed Systems, OAuth |
| C++ | 20 | Smart Pointers, RAII, Move Semantics, vtable, lock-free, templates |
| Java | 15 | JVM, GC, HashMap internals, ConcurrentHashMap, Spring, JPA |
| Go | 15 | Goroutines, GMP scheduler, Channels, Context, sync primitives |
| System Design | 15 | URL Shortener, Chat, Feed, Cache, Rate Limiter, Payments, Kafka |
| Database | 10 | ACID, Isolation Levels, B+Tree, CAP, Sharding, MVCC, WAL |
| OS | 8 | Process/Thread, Context Switch, Virtual Memory, Deadlock, Mutex |
| Networking | 8 | TCP/UDP, TLS, HTTP/2, DNS, WebSocket, CDN |
| Concurrency | 10 | Race conditions, Deadlock, CAS, ABA, Memory barriers |

## ✨ Features

- **Dark theme** responsive UI with Inter font
- **Full-text search** across all questions (Ctrl+K)
- **Company pages** with: difficulty rating, round breakdown, top-5 most asked, tabbed question browser
- **Filter by difficulty** (Easy / Medium / Hard) and subcategory
- **Tier navigation**: Home → Tier → Company → Questions
- **Question accordion** — click any question to reveal the answer hint
- **Frequency scores** — questions ranked by how often they appear in real interviews
- **10 category pages** — browse all questions by topic
- **JSON exports** — `search-index.json`, `questions-meta.json`, `companies-meta.json`

## 🔧 Adding More Questions

Edit `data/questions_coding.py` or `data/questions_other.py`. Each question is a tuple:

```python
("id", "Question Text", "category", "subcategory", "difficulty",
 ["Company1", "Company2"], frequency_int, "tag1,tag2", "Round Type", "Answer hint")
```

Then run `python generate_site.py` to rebuild.

## 🏗️ Target Roles

- SDE-1 Backend Engineer (3–5 YoE)
- SDE-2 Backend Engineer (4–7 YoE)
- Senior Software Engineer Backend
- Distributed Systems Engineer
- Backend Platform Engineer

## 📝 Data Sources

Questions curated from:
- LeetCode Discuss & Interview Experiences
- Glassdoor Interview Reviews
- Blind Community Posts
- Reddit r/cscareerquestions, r/ExperiencedDevs
- GeeksforGeeks Interview Experiences
- Coding Ninjas
- AmbitionBox
- Medium & Dev.to Engineering Blogs
- Public GitHub interview prep repositories
