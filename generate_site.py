#!/usr/bin/env python3
"""
Interview Repository Static Site Generator
Generates a complete static HTML website from question and company data.
"""
import json, os, sys, shutil
from pathlib import Path
from datetime import date

# ─── PATH SETUP ──────────────────────────────────────────────────
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
OUT = ROOT / "InterviewRepository"

# ─── SEO CONFIGURATION ────────────────────────────────────────────
# Update SITE_URL to your actual deployed URL (Netlify / GitHub Pages)
SITE_URL = os.environ.get("SITE_URL", "https://devinterviewvault.netlify.app").rstrip("/")
OG_IMAGE  = f"{SITE_URL}/assets/og-image.png"  # create a preview image if desired
BUILD_DATE = date.today().isoformat()

# Google Search Console verification
# Paste the code Google gives you (just the alphanumeric part, e.g. "1a2b3c4d5e6f7890")
# Leave empty ("") to skip generating the verification file
GOOGLE_VERIFY_CODE = os.environ.get("GOOGLE_VERIFY_CODE", "a8bdedb3bc5f858c")

from data.questions_all import ALL_QUESTIONS
with open(ROOT / "data" / "companies.json", encoding="utf-8") as f:
    COMPANY_DATA = json.load(f)

TIERS = COMPANY_DATA["tiers"]
ALL_COMPANIES = [c for t in TIERS for c in t["companies"]]
COMPANY_MAP = {c["name"]: {**c, "tier_id": t["id"], "tier_name": t["name"],
                            "tier_slug": t["slug"], "tier_color": t["color"]}
               for t in TIERS for c in t["companies"]}

# ─── HELPERS ─────────────────────────────────────────────────────
def freq_class(f):
    if f >= 80: return "freq-high"
    if f >= 60: return "freq-med"
    return "freq-low"

def diff_class(d):
    d = d.lower().replace("-","").replace(" ","")
    if "veryhard" in d: return "diff-very-hard"
    if "hard" in d: return "diff-hard"
    if "medium" in d: return "diff-medium"
    return "diff-easy"

def slug(name):
    return name.lower().replace(" ","").replace(".","").replace("/","").replace("&","and")

def get_company_questions(company_name, category=None):
    qs = [q for q in ALL_QUESTIONS if company_name in q["companies"]]
    if category:
        qs = [q for q in qs if q["category"] == category]
    return sorted(qs, key=lambda q: -q["frequency"])

def categories_for_company(company):
    """Return all categories that have questions for this company (always show primary first)."""
    name = company["name"]
    primary = company.get("primary_categories", ["coding","backend","system_design","database"])
    # Find all additional categories with questions
    all_cats_with_qs = sorted(
        set(q["category"] for q in ALL_QUESTIONS if name in q["companies"]),
        key=lambda c: primary.index(c) if c in primary else 99
    )
    # Merge OS + networking into one tab entry for readability
    result = [c for c in all_cats_with_qs]
    return result if result else primary

def depth_prefix(depth):
    return "../" * depth

# ─── HTML SHELL ──────────────────────────────────────────────────
def html_shell(title, body, depth=0, extra_head="", description="", page_url="", jsonld=None):
    pfx = depth_prefix(depth)
    desc = description or f"SDE-1/2 Backend Interview Questions for C++, Java, Go, System Design — {title}"
    canonical = f"{SITE_URL}/{page_url}" if page_url else SITE_URL
    # Open Graph + Twitter Card
    og = f"""
  <meta property="og:type"        content="website">
  <meta property="og:site_name"   content="InterviewRepo — Backend SDE Prep">
  <meta property="og:title"       content="{title} | InterviewRepo">
  <meta property="og:description" content="{desc}">
  <meta property="og:url"         content="{canonical}">
  <meta property="og:image"       content="{OG_IMAGE}">
  <meta name="twitter:card"       content="summary_large_image">
  <meta name="twitter:title"      content="{title} | InterviewRepo">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image"      content="{OG_IMAGE}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{canonical}">
  {f'<meta name="google-site-verification" content="{GOOGLE_VERIFY_CODE}">' if GOOGLE_VERIFY_CODE else ''}"""
    # JSON-LD structured data
    ld = json.dumps(jsonld, ensure_ascii=False) if jsonld else json.dumps({
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "description": desc,
        "url": canonical,
        "publisher": {"@type": "Organization", "name": "InterviewRepo"}
    })
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | InterviewRepo — Backend SDE Interview Prep</title>
  <meta name="description" content="{desc}">
  <meta name="keywords" content="backend interview questions, SDE interview prep, system design, DSA, C++ interview, Java interview, Go interview, {title.lower()}">
  <meta name="author" content="InterviewRepo">{og}
  <script type="application/ld+json">{ld}</script>
  <link rel="stylesheet" href="{pfx}assets/css/style.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  {extra_head}
</head>
<body>
{navbar(pfx)}
{body}
{footer(pfx)}
<button id="back-to-top" title="Back to top">↑</button>
<script src="{pfx}assets/js/main.js"></script>
</body>
</html>"""

def navbar(pfx=""):
    return f"""<nav class="navbar">
  <a class="navbar-brand" href="{pfx}index.html">
    <span class="logo-icon">⚡</span>
    <span>InterviewRepo</span>
  </a>
  <div class="search-bar">
    <span class="search-icon">🔍</span>
    <input type="text" id="search-input" placeholder="Search questions… (Ctrl+K)" autocomplete="off">
    <div id="search-results"></div>
  </div>
  <nav class="navbar-nav">
    <a href="{pfx}index.html">Home</a>
    <a href="{pfx}common/top-coding.html">Top DSA</a>
    <a href="{pfx}common/top-system-design.html">System Design</a>
    <a href="{pfx}common/top-backend.html">Backend</a>
    <a href="{pfx}common/top-cpp.html">C++</a>
    <a href="{pfx}cpp-handbook/index.html">&#x1F4D8; Handbook</a>
    <a href="{pfx}common/top-java.html">Java</a>
    <a href="{pfx}common/top-go.html">Go</a>
    <a href="{pfx}mcq-quiz.html" style="background:linear-gradient(90deg,#6366f1,#8b5cf6);color:#fff;padding:.3rem .75rem;border-radius:.4rem;font-weight:600">🎯 MCQ Quiz</a>
  </nav>
</nav>"""

def footer(pfx=""):
    return f"""<footer class="footer">
  <div class="container">
    <div class="footer-links">
      <a href="{pfx}common/top-coding.html">Top Coding</a>
      <a href="{pfx}common/top-system-design.html">System Design</a>
      <a href="{pfx}common/top-backend.html">Backend</a>
      <a href="{pfx}common/top-cpp.html">C++</a>
    <a href="{pfx}cpp-handbook/index.html">&#x1F4D8; Handbook</a>
      <a href="{pfx}common/top-java.html">Java</a>
      <a href="{pfx}common/top-go.html">Go</a>
      <a href="{pfx}common/top-database.html">Database</a>
      <a href="{pfx}common/top-concurrency.html">Concurrency</a>
      <a href="{pfx}common/top-os.html">OS</a>
      <a href="{pfx}common/top-networking.html">Networking</a>
      <a href="{pfx}common/top-lld.html">LLD</a>
      <a href="{pfx}common/top-cicd.html">CI/CD</a>
      <a href="{pfx}common/top-security.html">Security</a>
      <a href="{pfx}common/top-ml.html">ML Systems</a>
      <a href="{pfx}common/top-perf.html">Performance</a>
      <a href="{pfx}mcq-quiz.html">MCQ Quiz</a>
    </div>
    <p>Built for SDE-1 &amp; SDE-2 Backend Engineers | C++ · Java · Go · Distributed Systems</p>
    <p style="margin-top:8px;font-size:12px;opacity:.5">Data sourced from LeetCode, Glassdoor, Blind, Reddit &amp; public interview experiences</p>
  </div>
</footer>"""

# ─── QUESTION LIST HTML ───────────────────────────────────────────
def question_list_html(questions, show_difficulty=True):
    if not questions:
        return '<p style="color:var(--text-muted);padding:20px 0;">No questions found for this category.</p>'
    items = []
    for i, q in enumerate(questions, 1):
        tags_html = "".join(f'<span class="q-tag">{t}</span>' for t in q["tags"][:3])
        diff = q.get("difficulty","Medium")
        diff_badge = f'<span class="difficulty-badge {diff_class(diff)}" style="font-size:11px">{diff}</span>' if show_difficulty else ""
        answer = q.get("answer_hint","")
        companies_str = ', '.join(q['companies'][:6]) + ('...' if len(q['companies'])>6 else '')
        items.append(f"""<div class="q-wrapper">
  <div class="question-item" data-difficulty="{diff.lower()}" data-subcategory="{q.get('subcategory','')}">
    <span class="q-index">{i}</span>
    <span class="q-text">{q['text']}</span>
    <div class="q-tags">{tags_html}</div>
    {diff_badge}
    <span class="q-freq {freq_class(q['frequency'])}">{q['frequency']}%</span>
  </div>
  <div class="question-expand">
    <div class="q-answer">{answer}</div>
    <div class="q-meta-row">
      <span class="q-meta-chip">🗓 {q.get('round_type','Coding Round')}</span>
      <span class="q-meta-chip">🏢 {companies_str}</span>
    </div>
  </div>
</div>""")
        i = i  # suppress unused var warning
    return "\n".join(items)

# ─── TABS HTML ────────────────────────────────────────────────────
CAT_LABELS = {
    "coding": "💻 DSA",
    "backend": "🔧 Backend",
    "cpp": "⚙️ C++",
    "java": "☕ Java",
    "go": "🐹 Go",
    "system_design": "🏗️ System Design",
    "database": "🗄️ Database",
    "os": "🖥️ OS",
    "networking": "🌐 Networking",
    "concurrency": "⚡ Concurrency",
    "lld": "📐 LLD",
    "behavioral": "💬 Behavioral",
    "cicd": "🚀 CI/CD & DevOps",
    "security": "🔒 Security",
    "ml_systems": "🤖 ML Systems",
    "performance": "⚡ Performance",
}

def top_asked_cards(company_name, n=5):
    """Render top N most-frequent questions as quick-access summary cards."""
    top = get_company_questions(company_name)[:n]
    if not top: return ""
    cards = "".join(f"""<div style="background:var(--bg2);border:1px solid var(--border);border-radius:10px;padding:14px 18px;display:flex;gap:12px;align-items:flex-start">
  <span style="font-size:20px;flex-shrink:0">{'🔥' if q['frequency']>=85 else '⭐'}</span>
  <div>
    <div style="font-size:14px;font-weight:600;margin-bottom:4px">{q['text']}</div>
    <div style="font-size:12px;color:var(--text-muted)">{q['category'].replace('_',' ').title()} · {q['difficulty']} · {q['frequency']}% frequency</div>
  </div>
</div>""" for q in top)
    return f"""<div class="container" style="padding:24px 24px 0">
  <h2 style="font-size:20px;font-weight:700;margin-bottom:14px">🔥 Most Frequently Asked</h2>
  <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:10px;margin-bottom:8px">{cards}</div>
</div>"""

def company_tabs_html(company_name, cats):
    tabs = []
    panels = []
    all_qs = get_company_questions(company_name)
    first_active = True
    for cat in cats:
        cat_qs = [q for q in all_qs if q["category"] == cat]
        if not cat_qs: continue
        label = CAT_LABELS.get(cat, cat.title())
        is_active = first_active
        first_active = False
        tabs.append(f'<button class="tab-btn{" active" if is_active else ""}" data-tab="{cat}">{label} <span style="opacity:.5;font-size:11px">({len(cat_qs)})</span></button>')
        active = " active" if is_active else ""
        panels.append(f"""<div class="tab-panel{active}" id="tab-{cat}">
  <div class="questions-header">
    <h3>{label}</h3>
    <span class="q-count">{len(cat_qs)} questions</span>
  </div>
  {question_list_html(cat_qs)}
</div>""")
    tabs_html = "\n".join(tabs)
    panels_html = "\n".join(panels)
    return f"""<div class="tabs-bar"><div class="tabs-inner">{tabs_html}</div></div>
<div class="container">{panels_html}</div>"""

# ─── ROUND BREAKDOWN ──────────────────────────────────────────────
ROUND_TEMPLATES = {
    "Very Hard": ["Online Assessment (90 min)","Technical Phone Screen","Coding Round 1","Coding Round 2","System Design","Hiring Manager","Bar Raiser"],
    "Hard":      ["Online Assessment (90 min)","Technical Phone Screen","Coding Round 1","System Design / LLD","Hiring Manager","HR"],
    "Medium-Hard":["Online Assessment (60 min)","Technical Screen","Coding Round","LLD / HLD","Hiring Manager","HR"],
    "Medium":    ["Online Assessment","Technical Screen","Coding Round","System Design","HR"],
    "Easy-Medium":["Online Test","Technical Interview","HR Round"],
}

def rounds_html(company):
    diff = company.get("difficulty","Medium")
    rounds = ROUND_TEMPLATES.get(diff, ROUND_TEMPLATES["Medium"])
    cards = []
    for i, r in enumerate(rounds, 1):
        duration = "45-60 min" if "Assessment" not in r else "60-90 min"
        if "HR" in r: duration = "30-45 min"
        cards.append(f"""<div class="round-card">
  <div class="round-number">Round {i}</div>
  <div class="round-name">{r}</div>
  <div class="round-duration">{duration}</div>
</div>""")
    return f'<div class="rounds-grid">{"".join(cards)}</div>'

# ─── GENERATE COMPANY PAGE ────────────────────────────────────────
def generate_company_page(company, tier, depth=2):
    name = company["name"]
    diff = company.get("difficulty","Medium")
    roles_str = ", ".join(company.get("roles",[]))
    focus_str = " · ".join(company.get("focus",[]))
    known_for = company.get("known_for","")
    avg_rounds = company.get("avg_rounds", 4)
    all_qs = get_company_questions(name)
    primary_cats = categories_for_company(company)

    header = f"""<div class="company-header">
  <div class="container">
    <div class="breadcrumb">
      <a href="../../index.html">Home</a>
      <span class="breadcrumb-sep">›</span>
      <a href="../index.html">Tier {tier['id']}: {tier['name']}</a>
      <span class="breadcrumb-sep">›</span>
      <span>{name}</span>
    </div>
    <div class="company-header-inner">
      <div class="company-logo-placeholder">{name[0]}</div>
      <div class="company-info">
        <div style="margin-bottom:8px">
          <span class="tier-badge" data-tier="{tier['id']}" style="--tier-color:{tier['color']}">Tier {tier['id']}: {tier['name']}</span>
          <span class="difficulty-badge {diff_class(diff)}" style="margin-left:8px">{diff}</span>
        </div>
        <h1>{name}</h1>
        <p style="color:var(--text-muted);margin-top:8px">{known_for}</p>
        <div class="company-info-meta">
          <span class="info-chip"><strong>HQ:</strong> {company.get('hq','—')}</span>
          <span class="info-chip"><strong>Roles:</strong> {roles_str}</span>
          <span class="info-chip"><strong>Focus:</strong> {focus_str}</span>
          <span class="info-chip"><strong>Interview:</strong> {company.get('interview_style','—')}</span>
        </div>
        <div class="company-stats">
          <div class="stat-item"><div class="stat-value">{len(all_qs)}</div><div class="stat-label">Questions</div></div>
          <div class="stat-item"><div class="stat-value">{avg_rounds}</div><div class="stat-label">Avg Rounds</div></div>
          <div class="stat-item"><div class="stat-value">{company.get('difficulty_score','—')}/5</div><div class="stat-label">Difficulty</div></div>
          <div class="stat-item"><div class="stat-value">{len(primary_cats)}</div><div class="stat-label">Categories</div></div>
        </div>
      </div>
    </div>
  </div>
</div>"""

    rounds_section = f"""<div class="container" style="padding:32px 24px 0">
  <h2 style="font-size:22px;font-weight:700;margin-bottom:16px">📋 Interview Rounds</h2>
  {rounds_html(company)}
</div>"""

    top_cards = top_asked_cards(name)
    tabs = company_tabs_html(name, primary_cats)
    body = header + rounds_section + top_cards + tabs
    return html_shell(name, body, depth=depth)

# ─── GENERATE TIER PAGE ───────────────────────────────────────────
def generate_tier_page(tier, depth=1):
    companies = tier["companies"]
    cards = []
    for c in companies:
        all_qs = get_company_questions(c["name"])
        q_count = len(all_qs)
        roles_str = ", ".join(c.get("roles", [])[:2])
        cards.append(f"""<a href="{c['slug']}.html" class="company-card" style="display:block;text-decoration:none">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px">
    <div class="company-name">{c['name']}</div>
    <span class="difficulty-badge {diff_class(c.get('difficulty','Medium'))}">{c.get('difficulty','Medium')}</span>
  </div>
  <div class="company-meta">{c.get('hq','—')} · {roles_str}</div>
  <div class="company-meta" style="margin-bottom:12px">{c.get('known_for','')[:80]}{'…' if len(c.get('known_for',''))>80 else ''}</div>
  <div style="display:flex;justify-content:space-between;align-items:center">
    <span style="font-size:13px;color:var(--text-muted)">{q_count} questions</span>
    <span style="font-size:13px;font-weight:600;color:var(--accent)">View →</span>
  </div>
</a>""")
    grid = f'<div class="company-grid">{"".join(cards)}</div>'
    body = f"""<div class="tier-index-header" style="background:linear-gradient(135deg,rgba({_hex_to_rgb(tier['color'])},0.1) 0%,transparent 60%);border-bottom:1px solid var(--border)">
  <div class="container">
    <div class="breadcrumb"><a href="../index.html">Home</a><span class="breadcrumb-sep">›</span><span>Tier {tier['id']}</span></div>
    <div style="display:inline-flex;align-items:center;gap:10px;margin-bottom:12px">
      <span style="width:16px;height:16px;border-radius:50%;background:{tier['color']};display:inline-block"></span>
      <span style="font-size:12px;font-weight:700;color:{tier['color']};text-transform:uppercase;letter-spacing:1px">Tier {tier['id']}</span>
    </div>
    <h1>{tier['name']}</h1>
    <p style="color:var(--text-muted);max-width:600px;margin-top:8px">{tier['description']}</p>
    <p style="color:var(--text-muted);font-size:14px;margin-top:12px">{len(companies)} Companies</p>
  </div>
</div>
<div class="container section">{grid}</div>"""
    return html_shell(f"Tier {tier['id']}: {tier['name']}", body, depth=depth)

def _hex_to_rgb(hex_color):
    h = hex_color.lstrip('#')
    if len(h) == 3: h = ''.join(c*2 for c in h)
    return ','.join(str(int(h[i:i+2],16)) for i in (0,2,4))

# ─── GENERATE HOMEPAGE ────────────────────────────────────────────
def generate_index():
    total_q = len(ALL_QUESTIONS)
    total_companies = len(ALL_COMPANIES)
    tier_cards = []
    for t in TIERS:
        color = t["color"]
        companies_preview = ", ".join(c["name"] for c in t["companies"][:4])
        if len(t["companies"]) > 4: companies_preview += f" +{len(t['companies'])-4} more"
        tier_cards.append(f"""<a href="{t['slug']}/index.html" class="tier-card" data-tier="{t['id']}" style="text-decoration:none">
  <div class="tier-badge">Tier {t['id']}</div>
  <div class="tier-card-title">{t['name']}</div>
  <div class="tier-card-desc">{t['description'][:120]}…</div>
  <div class="company-pills">{"".join(f'<span class="company-pill">{c["name"]}</span>' for c in t["companies"][:5])}</div>
  <div class="tier-card-footer">
    <span class="company-count">{len(t['companies'])} companies · Tier {t['id']}</span>
    <span class="view-btn">Explore →</span>
  </div>
</a>""")

    common_links = [
        ("💻","Top Coding / DSA","common/top-coding.html"),
        ("🏗️","System Design","common/top-system-design.html"),
        ("🔧","Backend Engineering","common/top-backend.html"),
        ("⚙️","C++ Questions","common/top-cpp.html"),
        ("☕","Java Questions","common/top-java.html"),
        ("🐹","Go Questions","common/top-go.html"),
        ("�️","Database","common/top-database.html"),
        ("⚡","Concurrency","common/top-concurrency.html"),
        ("�️","OS Questions","common/top-os.html"),
        ("🌐","Networking","common/top-networking.html"),
        ("📐","LLD / Machine Coding","common/top-lld.html"),
        ("🚀","CI/CD & DevOps","common/top-cicd.html"),
        ("🔒","Security","common/top-security.html"),
        ("🤖","ML Systems","common/top-ml.html"),
        ("⚡","Performance & Observability","common/top-perf.html"),
        ("🎯","MCQ Quiz — Java/Go Backend","mcq-quiz.html"),
    ]
    common_cards = "".join(f"""<a href="{url}" style="background:var(--bg2);border:1px solid var(--border);border-radius:10px;padding:16px 20px;display:flex;align-items:center;gap:12px;transition:border-color .2s;text-decoration:none" onmouseover="this.style.borderColor='var(--accent)'" onmouseout="this.style.borderColor='var(--border)'">
  <span style="font-size:24px">{icon}</span>
  <span style="font-size:15px;font-weight:600;color:var(--text)">{label}</span>
  <span style="margin-left:auto;color:var(--accent)">→</span>
</a>""" for icon,label,url in common_links)

    body = f"""<section class="hero">
  <div class="container">
    <h1 class="hero-title animate-fade-up">
      Master Backend Engineering<br>
      <span class="gradient-text">Interview Preparation Hub</span>
    </h1>
    <p class="hero-sub animate-fade-up delay-1">
      {total_q}+ curated questions for SDE-1 &amp; SDE-2 Backend roles across {total_companies} companies.
      C++ · Java · Go · Distributed Systems · System Design.
    </p>
    <div class="hero-stats animate-fade-up delay-2">
      <div><span class="hero-stat-value">{total_q}+</span><div class="hero-stat-label">Questions</div></div>
      <div><span class="hero-stat-value">{total_companies}</span><div class="hero-stat-label">Companies</div></div>
      <div><span class="hero-stat-value">8</span><div class="hero-stat-label">Tiers</div></div>
      <div><span class="hero-stat-value">10</span><div class="hero-stat-label">Categories</div></div>
    </div>
  </div>
</section>

<div class="container section">
  <h2 class="section-title">📚 Question Banks</h2>
  <p class="section-sub">Browse curated question lists by technology and topic</p>
  <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px;margin-bottom:64px">
    {common_cards}
  </div>

  <h2 class="section-title">🏢 Companies by Tier</h2>
  <p class="section-sub">Click a tier to browse companies and their interview questions</p>
  <div class="tier-grid">{"".join(tier_cards)}</div>
</div>"""
    return html_shell("Home — Interview Repository", body, depth=0)

# ─── GENERATE COMMON PAGES ────────────────────────────────────────
def generate_common_page(title, category, icon, description, depth=1):
    qs = sorted([q for q in ALL_QUESTIONS if q["category"] == category],
                key=lambda q: -q["frequency"])
    subcats = sorted(set(q.get("subcategory","") for q in qs))
    filter_btns = '<button class="filter-btn active" data-filter="all" data-group="sub">All</button>'
    filter_btns += "".join(f'<button class="filter-btn" data-filter="{s}" data-group="sub">{s.replace("_"," ").title()}</button>' for s in subcats if s)
    diff_btns = '<button class="filter-btn active" data-filter="all" data-group="diff">All Difficulty</button>'
    for d in ["Easy","Medium","Hard"]:
        diff_btns += f'<button class="filter-btn" data-filter="{d.lower()}" data-group="diff">{d}</button>'

    body = f"""<div class="top-list-header">
  <div class="container">
    <div class="breadcrumb"><a href="../index.html">Home</a><span class="breadcrumb-sep">›</span><span>{title}</span></div>
    <h1 style="font-size:36px;font-weight:800;margin-bottom:8px">{icon} {title}</h1>
    <p style="color:var(--text-muted);font-size:16px">{description}</p>
    <p style="color:var(--text-muted);font-size:14px;margin-top:8px">{len(qs)} questions</p>
  </div>
</div>
<div class="container section">
  <div class="filters-bar">{filter_btns}</div>
  <div class="filters-bar">{diff_btns}</div>
  <div class="question-list">{question_list_html(qs)}</div>
</div>"""
    return html_shell(title, body, depth=depth)

# ─── GENERATE SEARCH INDEX ────────────────────────────────────────
def generate_search_index():
    index = []
    for q in ALL_QUESTIONS:
        for company in q["companies"]:
            if company in COMPANY_MAP:
                cm = COMPANY_MAP[company]
                tier_slug = cm["tier_slug"]
                company_slug = cm["slug"]
                url = f"{tier_slug}/{company_slug}.html#{q['category']}"
                index.append({
                    "company": company,
                    "tier": f"Tier {cm['tier_id']}: {cm['tier_name']}",
                    "question": q["text"],
                    "category": q["category"],
                    "subcategory": q.get("subcategory",""),
                    "difficulty": q.get("difficulty",""),
                    "frequency": q["frequency"],
                    "tags": ",".join(q.get("tags",[])),
                    "source": "Curated from LeetCode, Glassdoor, Blind, Reddit",
                    "url": url
                })
    return index

# ─── MAIN BUILD ───────────────────────────────────────────────────
def build():
    # Clean + create output directory (resilient to Windows file locks)
    if OUT.exists():
        try:
            shutil.rmtree(OUT)
        except PermissionError:
            pass  # directory in use (HTTP server); overwrite files instead
    OUT.mkdir(parents=True, exist_ok=True)

    # Copy assets (overwrite existing)
    assets_src = ROOT / "assets"
    assets_dst = OUT / "assets"
    shutil.copytree(assets_src, assets_dst, dirs_exist_ok=True)
    print("✓ Assets copied")

    # Homepage
    (OUT / "index.html").write_text(generate_index(), encoding="utf-8")
    print("✓ index.html")

    # Google Search Console verification file
    if GOOGLE_VERIFY_CODE:
        verify_file = OUT / f"google{GOOGLE_VERIFY_CODE}.html"
        verify_file.write_text(
            f"google-site-verification: google{GOOGLE_VERIFY_CODE}.html",
            encoding="utf-8")
        print(f"✓ google{GOOGLE_VERIFY_CODE}.html (Search Console verification)")
    else:
        print("  (skip) Google verification: set GOOGLE_VERIFY_CODE to enable")

    # robots.txt
    robots = f"""User-agent: *
Allow: /
Sitemap: {SITE_URL}/sitemap.xml

# Crawl-delay for courtesy
Crawl-delay: 1
"""
    (OUT / "robots.txt").write_text(robots, encoding="utf-8")
    print("✓ robots.txt")

    # Tier + company pages
    for tier in TIERS:
        tier_dir = OUT / tier["slug"]
        tier_dir.mkdir(parents=True, exist_ok=True)
        (tier_dir / "index.html").write_text(generate_tier_page(tier, depth=1), encoding="utf-8")
        print(f"  ✓ {tier['slug']}/index.html")

        for company in tier["companies"]:
            fname = f"{company['slug']}.html"
            html = generate_company_page(company, tier, depth=2)
            (tier_dir / fname).write_text(html, encoding="utf-8")
            print(f"    ✓ {tier['slug']}/{fname}")

    # Common pages
    common_dir = OUT / "common"
    common_dir.mkdir(exist_ok=True)
    common_pages = [
        ("top-coding.html",       "Top Coding / DSA Questions",      "coding",        "💻", "Top DSA problems asked in backend SDE-1/2 interviews. Sorted by frequency across all companies."),
        ("top-system-design.html","Top System Design Questions",     "system_design", "🏗️", "Most frequently asked System Design questions for senior backend roles."),
        ("top-backend.html",      "Top Backend Engineering Questions","backend",       "🔧", "Backend design questions on APIs, messaging, distributed systems and resilience."),
        ("top-cpp.html",          "Top C++ Questions",               "cpp",           "⚙️", "Deep C++ questions on memory, templates, concurrency and performance."),
        ("top-java.html",         "Top Java Questions",              "java",          "☕", "Core Java questions on JVM, collections, concurrency and Spring."),
        ("top-go.html",           "Top Go Questions",                "go",            "🐹", "Go-specific questions on goroutines, channels, runtime and patterns."),
        ("top-database.html",     "Top Database Questions",          "database",      "🗄️", "Database questions on ACID, indexing, sharding, replication and query optimization."),
        ("top-concurrency.html",  "Top Concurrency Questions",       "concurrency",   "⚡", "Concurrency patterns, synchronization primitives and lock-free programming questions."),
        ("top-os.html",           "Operating Systems Questions",     "os",            "🖥️", "OS concepts: processes, threads, memory, scheduling and synchronization."),
        ("top-networking.html",   "Networking Questions",            "networking",    "🌐", "Networking fundamentals: TCP/UDP, TLS, HTTP/2, DNS, WebSockets and CDN."),
        ("top-lld.html",           "LLD / Machine Coding Questions",  "lld",           "📐", "Low-Level Design and Machine Coding questions: Parking Lot, ATM, BookMyShow, Chess, Elevator..."),
        ("top-cicd.html",          "CI/CD & DevOps Questions",        "cicd",          "🚀", "CI/CD fundamentals: Docker, Kubernetes, Helm, Terraform, GitHub Actions, Monitoring, GitOps."),
        ("top-security.html",      "Security Engineering Questions",  "security",      "🔒", "Application security: OWASP Top 10, SQL injection, JWT, TLS, CSRF, RBAC, secrets management."),
        ("top-ml.html",            "ML Systems Questions",            "ml_systems",    "🤖", "ML system design: feature stores, recommendation systems, fraud detection, A/B testing, LLMs."),
        ("top-perf.html",          "Performance & Observability",     "performance",   "⚡", "Performance engineering: latency diagnosis, distributed tracing, caching, load testing, observability."),
    ]
    for fname, title, category, icon, desc in common_pages:
        html = generate_common_page(title, category, icon, desc, depth=1)
        (common_dir / fname).write_text(html, encoding="utf-8")
        print(f"  ✓ common/{fname}")

    # Search index
    search_index = generate_search_index()
    (OUT / "search-index.json").write_text(
        json.dumps(search_index, ensure_ascii=False, separators=(',', ':')), encoding="utf-8")
    print(f"✓ search-index.json ({len(search_index)} entries)")

    # sitemap.xml
    sitemap_urls = []
    # Homepage — highest priority
    sitemap_urls.append((f"{SITE_URL}/index.html", BUILD_DATE, "daily", "1.0"))
    # Common question pages
    sitemap_urls.append((f"{SITE_URL}/mcq-quiz.html", BUILD_DATE, "weekly", "0.9"))
    for fname in ["top-coding","top-system-design","top-backend","top-cpp","top-java",
                  "top-go","top-database","top-concurrency","top-os","top-networking",
                  "top-lld","top-cicd","top-security","top-ml","top-perf"]:
        sitemap_urls.append((f"{SITE_URL}/common/{fname}.html", BUILD_DATE, "weekly", "0.9"))
    # Tier pages
    for tier in TIERS:
        sitemap_urls.append((f"{SITE_URL}/{tier['slug']}/index.html", BUILD_DATE, "weekly", "0.8"))
        for company in tier["companies"]:
            sitemap_urls.append((f"{SITE_URL}/{tier['slug']}/{company['slug']}.html", BUILD_DATE, "weekly", "0.7"))
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url, lastmod, changefreq, priority in sitemap_urls:
        sitemap_xml += f'  <url><loc>{url}</loc><lastmod>{lastmod}</lastmod><changefreq>{changefreq}</changefreq><priority>{priority}</priority></url>\n'
    sitemap_xml += '</urlset>'
    (OUT / "sitemap.xml").write_text(sitemap_xml, encoding="utf-8")
    print(f"✓ sitemap.xml ({len(sitemap_urls)} URLs)")

    # Company metadata JSON
    meta = []
    for t in TIERS:
        for c in t["companies"]:
            meta.append({
                "name": c["name"], "slug": c["slug"],
                "tier": t["id"], "tier_name": t["name"],
                "difficulty": c.get("difficulty"), "difficulty_score": c.get("difficulty_score"),
                "avg_rounds": c.get("avg_rounds"), "hq": c.get("hq"),
                "focus": c.get("focus"), "question_count": len(get_company_questions(c["name"]))
            })
    (OUT / "companies-meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✓ companies-meta.json ({len(meta)} companies)")

    # Question metadata JSON
    (OUT / "questions-meta.json").write_text(
        json.dumps(ALL_QUESTIONS, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✓ questions-meta.json ({len(ALL_QUESTIONS)} questions)")

    # MCQ Quiz page
    from gen_mcqs import build_html_for_site
    build_html_for_site(OUT, html_shell)

    print(f"\n🎉 Build complete! Output → {OUT}")
    print(f"   Open: {OUT / 'index.html'}")

if __name__ == "__main__":
    build()
