"""gen_mcqs.py — Generates backend_mcqs.html (standalone) and mcq-quiz.html (site-integrated)."""
import json, os

QUESTIONS = []  # populated by q_data files below

# Quiz-specific CSS (compatible with both standalone and site versions)
QUIZ_STYLES = """
.mcq-hero{background:linear-gradient(135deg,rgba(99,102,241,.12),transparent 60%);border-bottom:1px solid var(--border,#334155);padding:2rem 1.5rem;text-align:center}
.mcq-hero h1{font-size:1.7rem;font-weight:800;margin-bottom:.4rem}
.mcq-hero p{color:var(--text-muted,#94a3b8);font-size:.95rem}
.mcq-controls{background:var(--bg2,#1e293b);padding:.85rem 1.5rem;display:flex;gap:.65rem;flex-wrap:wrap;align-items:center;border-bottom:1px solid var(--border,#334155);position:sticky;top:60px;z-index:90}
.mcq-controls input{background:var(--bg,#0f172a);border:1px solid var(--border,#334155);color:var(--text,#e2e8f0);padding:.45rem .85rem;border-radius:.5rem;font-size:.9rem;flex:1;min-width:180px;outline:none}
.mcq-controls input:focus{border-color:#6366f1}
.mcq-filter-btn{background:var(--bg2,#1e293b);border:1px solid var(--border,#334155);color:var(--text-muted,#94a3b8);padding:.4rem .8rem;border-radius:.5rem;cursor:pointer;font-size:.8rem;transition:all .2s;white-space:nowrap}
.mcq-filter-btn.active{background:#6366f1;border-color:#6366f1;color:#fff}
.mcq-stats{background:var(--bg2,#1e293b);padding:.5rem 1.5rem;display:flex;gap:1.5rem;flex-wrap:wrap;border-bottom:1px solid var(--border,#334155);font-size:.82rem;color:var(--text-muted,#94a3b8)}
.mcq-stats span b{color:var(--text,#e2e8f0)}
.mcq-list{max-width:880px;margin:0 auto;padding:1.5rem 1rem}
.mcq-card{background:var(--bg2,#1e293b);border:1px solid var(--border,#334155);border-radius:.75rem;margin-bottom:1rem;overflow:hidden;transition:border-color .2s}
.mcq-card:hover{border-color:#6366f1}
.mcq-qhead{padding:1rem 1.25rem .75rem;display:flex;gap:.65rem;align-items:flex-start}
.mcq-num{background:var(--bg,#0f172a);border:1px solid var(--border,#334155);border-radius:.35rem;padding:.15rem .5rem;font-size:.76rem;color:var(--text-muted,#94a3b8);white-space:nowrap;margin-top:.1rem}
.mcq-badge{padding:.18rem .55rem;border-radius:9999px;font-size:.7rem;font-weight:600;white-space:nowrap;margin-top:.1rem}
.mcq-qtext{font-size:.96rem;font-weight:500;line-height:1.55;color:var(--text,#e2e8f0);flex:1}
.mcq-options{padding:0 1.25rem .75rem;display:flex;flex-direction:column;gap:.35rem}
.mcq-opt{background:var(--bg,#0f172a);border:1px solid var(--border,#334155);border-radius:.4rem;padding:.5rem .8rem;font-size:.87rem;cursor:pointer;transition:all .2s;color:var(--text-muted,#cbd5e1)}
.mcq-opt:hover{border-color:#6366f1;color:var(--text,#e2e8f0)}
.mcq-opt.correct{border-color:#10b981;background:#022c22;color:#6ee7b7}
.mcq-opt.wrong{border-color:#ef4444;background:#1c0a0a;color:#fca5a5}
.mcq-actions{padding:0 1.25rem .85rem;display:flex;gap:.55rem}
.mcq-btn-show{background:#6366f1;color:#fff;border:none;padding:.4rem .95rem;border-radius:.4rem;cursor:pointer;font-size:.84rem;font-weight:600;transition:background .2s}
.mcq-btn-show:hover{background:#4f46e5}
.mcq-btn-reset{background:transparent;color:var(--text-muted,#94a3b8);border:1px solid var(--border,#334155);padding:.4rem .8rem;border-radius:.4rem;cursor:pointer;font-size:.8rem}
.mcq-answer{padding:.85rem 1.25rem;background:var(--bg,#020617);border-top:1px solid var(--border,#334155);display:none;animation:mcqFadeIn .22s ease}
@keyframes mcqFadeIn{from{opacity:0;transform:translateY(-5px)}to{opacity:1;transform:translateY(0)}}
.mcq-answer-label{font-size:.74rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#10b981;margin-bottom:.5rem}
.mcq-answer .mcq-exp{font-size:.89rem;line-height:1.75;color:var(--text-muted,#cbd5e1)}
.mcq-answer .mcq-exp b{color:var(--text,#f1f5f9)}
.mcq-answer .mcq-exp code{background:var(--bg2,#1e293b);padding:.12rem .32rem;border-radius:.3rem;font-family:'Courier New',monospace;font-size:.84em;color:#7dd3fc}
.mcq-answer.open{display:block}
.mcq-no-results{text-align:center;padding:3rem;color:#64748b}
.mcq-btn-resetall{background:#1e293b;border:1px solid #475569;color:#94a3b8;padding:.4rem .9rem;border-radius:.4rem;cursor:pointer;font-size:.82rem;font-weight:600;margin-left:auto;transition:all .2s}
.mcq-btn-resetall:hover{background:#ef4444;border-color:#ef4444;color:#fff}
"""

# ── TOPIC METADATA ────────────────────────────────────────────────────────────
TOPICS = {
    "microservices": ("Microservices", "#6366f1"),
    "messaging":     ("Messaging Queues", "#f59e0b"),
    "redis":         ("Redis & Cache", "#ef4444"),
    "databases":     ("Databases", "#10b981"),
    "sysdesign":     ("System Design", "#3b82f6"),
    "java":          ("Java", "#8b5cf6"),
    "golang":        ("Go (Golang)", "#06b6d4"),
}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Backend MCQs — Java/Go (5 YOE) | Product Companies</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Segoe UI',system-ui,sans-serif;background:#0f172a;color:#e2e8f0;min-height:100vh}}
header{{background:linear-gradient(135deg,#1e1b4b,#0f172a);padding:2rem;text-align:center;border-bottom:1px solid #334155}}
header h1{{font-size:1.8rem;font-weight:700;background:linear-gradient(90deg,#818cf8,#38bdf8);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
header p{{color:#94a3b8;margin-top:.4rem;font-size:.95rem}}
.controls{{background:#1e293b;padding:1rem 1.5rem;display:flex;gap:.75rem;flex-wrap:wrap;align-items:center;border-bottom:1px solid #334155;position:sticky;top:0;z-index:100}}
.controls input{{background:#0f172a;border:1px solid #334155;color:#e2e8f0;padding:.5rem .85rem;border-radius:.5rem;font-size:.9rem;flex:1;min-width:200px;outline:none}}
.controls input:focus{{border-color:#6366f1}}
.filter-btn{{background:#1e293b;border:1px solid #334155;color:#94a3b8;padding:.45rem .85rem;border-radius:.5rem;cursor:pointer;font-size:.82rem;transition:all .2s;white-space:nowrap}}
.filter-btn.active{{background:#6366f1;border-color:#6366f1;color:#fff}}
.stats{{background:#1e293b;padding:.6rem 1.5rem;display:flex;gap:1.5rem;flex-wrap:wrap;border-bottom:1px solid #334155;font-size:.82rem;color:#94a3b8}}
.stats span b{{color:#e2e8f0}}
.q-list{{max-width:900px;margin:0 auto;padding:1.5rem 1rem}}
.q-card{{background:#1e293b;border:1px solid #334155;border-radius:.75rem;margin-bottom:1.1rem;overflow:hidden;transition:border-color .2s}}
.q-card:hover{{border-color:#6366f1}}
.q-header{{padding:1rem 1.25rem .75rem;display:flex;gap:.75rem;align-items:flex-start}}
.q-num{{background:#0f172a;border:1px solid #334155;border-radius:.4rem;padding:.2rem .55rem;font-size:.78rem;color:#94a3b8;white-space:nowrap;margin-top:.1rem}}
.q-badge{{padding:.2rem .6rem;border-radius:9999px;font-size:.72rem;font-weight:600;white-space:nowrap;margin-top:.1rem}}
.q-text{{font-size:.97rem;font-weight:500;line-height:1.5;color:#e2e8f0;flex:1}}
.q-options{{padding:0 1.25rem .75rem;display:flex;flex-direction:column;gap:.4rem}}
.q-option{{background:#0f172a;border:1px solid #334155;border-radius:.45rem;padding:.55rem .85rem;font-size:.88rem;cursor:pointer;transition:all .2s;color:#cbd5e1}}
.q-option:hover{{border-color:#6366f1;color:#e2e8f0}}
.q-option.selected{{border-color:#6366f1;background:#1e1b4b;color:#818cf8}}
.q-option.correct{{border-color:#10b981;background:#022c22;color:#6ee7b7}}
.q-option.wrong{{border-color:#ef4444;background:#1c0a0a;color:#fca5a5}}
.q-actions{{padding:0 1.25rem .85rem;display:flex;gap:.6rem}}
.btn-show{{background:#6366f1;color:#fff;border:none;padding:.45rem 1rem;border-radius:.45rem;cursor:pointer;font-size:.85rem;font-weight:600;transition:background .2s}}
.btn-show:hover{{background:#4f46e5}}
.btn-reset{{background:transparent;color:#94a3b8;border:1px solid #334155;padding:.45rem .85rem;border-radius:.45rem;cursor:pointer;font-size:.82rem}}
.q-answer{{padding:.85rem 1.25rem;background:#020617;border-top:1px solid #334155;display:none;animation:fadeIn .25s ease}}
@keyframes fadeIn{{from{{opacity:0;transform:translateY(-6px)}}to{{opacity:1;transform:translateY(0)}}}}
.answer-label{{font-size:.75rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#10b981;margin-bottom:.5rem}}
.q-answer .answer-text{{font-size:.9rem;line-height:1.7;color:#cbd5e1}}
.q-answer .answer-text b{{color:#f1f5f9}}
.q-answer .answer-text code{{background:#1e293b;padding:.15rem .35rem;border-radius:.3rem;font-family:'Courier New',monospace;font-size:.85em;color:#7dd3fc}}
.q-answer.open{{display:block}}
.no-results{{text-align:center;padding:3rem;color:#64748b;font-size:1rem}}
.progress-bar{{height:3px;background:#6366f1;transition:width .3s}}
</style>
</head>
<body>
<header>
  <h1>Backend Engineering MCQs</h1>
  <p>150 Questions · Java &amp; Go · Product Companies · 5 Years Experience</p>
</header>
<div class="controls">
  <input type="text" id="search" placeholder="Search questions…" oninput="filterAll()">
  <button class="filter-btn active" data-topic="all" onclick="setTopic(this)">All (150)</button>
  {TOPIC_BUTTONS}
</div>
<div class="stats">
  <span>Showing <b id="showing">150</b> of 150</span>
  <span>Answered <b id="answered">0</b></span>
  <span>Correct <b id="correct_count">0</b></span>
</div>
<div class="q-list" id="qlist"></div>
<script>
const QUESTIONS = {QUESTIONS_JSON};
const TOPICS = {TOPICS_JSON};
let activeTopic = 'all';
let answered = 0, correct = 0;

function badge(t){{
  const [label,color] = TOPICS[t]||[t,'#64748b'];
  return `<span class="q-badge" style="background:${{color}}22;color:${{color}};border:1px solid ${{color}}44">${{label}}</span>`;
}}

function renderAll(qs){{
  const el = document.getElementById('qlist');
  if(!qs.length){{el.innerHTML='<div class="no-results">No questions found.</div>';return;}}
  el.innerHTML = qs.map(q=>`
  <div class="q-card" id="card-${{q.id}}">
    <div class="q-header">
      <span class="q-num">#${{q.id}}</span>
      ${{badge(q.topic)}}
      <div class="q-text">${{q.q}}</div>
    </div>
    <div class="q-options">${{q.options.map((o,i)=>`
      <div class="q-option" id="opt-${{q.id}}-${{i}}" onclick="choose(${{q.id}},${{i}},'${{q.answer}}')">${{o}}</div>`).join('')}}
    </div>
    <div class="q-actions">
      <button class="btn-show" onclick="toggleAnswer(${{q.id}})">Show Answer</button>
      <button class="btn-reset" onclick="resetCard(${{q.id}})">Reset</button>
    </div>
    <div class="q-answer" id="ans-${{q.id}}">
      <div class="answer-label">✓ Answer: ${{q.answer}}</div>
      <div class="answer-text">${{q.explanation}}</div>
    </div>
  </div>`).join('');
  document.getElementById('showing').textContent = qs.length;
}}

function choose(id,idx,ans){{
  const opts = ['A','B','C','D'];
  const chosen = opts[idx];
  const el = document.getElementById(`opt-${{id}}-${{idx}}`);
  if(el.classList.contains('correct')||el.classList.contains('wrong')) return;
  const isCorrect = chosen===ans;
  el.classList.add(isCorrect?'correct':'wrong');
  el.classList.add('selected');
  if(!isCorrect){{
    const corrIdx = opts.indexOf(ans);
    document.getElementById(`opt-${{id}}-${{corrIdx}}`).classList.add('correct');
  }}
  answered++;
  if(isCorrect) correct++;
  document.getElementById('answered').textContent=answered;
  document.getElementById('correct_count').textContent=correct;
  document.getElementById(`ans-${{id}}`).classList.add('open');
}}

function toggleAnswer(id){{
  const a = document.getElementById(`ans-${{id}}`);
  a.classList.toggle('open');
  const btn = a.previousElementSibling.querySelector('.btn-show');
  btn.textContent = a.classList.contains('open')?'Hide Answer':'Show Answer';
}}

function resetCard(id){{
  ['A','B','C','D'].forEach((_,i)=>{{
    const o = document.getElementById(`opt-${{id}}-${{i}}`);
    if(o) o.className='q-option';
  }});
  document.getElementById(`ans-${{id}}`).classList.remove('open');
}}

function filterAll(){{
  const s = document.getElementById('search').value.toLowerCase();
  const qs = QUESTIONS.filter(q=>
    (activeTopic==='all'||q.topic===activeTopic) &&
    (!s||q.q.toLowerCase().includes(s))
  );
  renderAll(qs);
}}

function setTopic(btn){{
  document.querySelectorAll('.filter-btn').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  activeTopic = btn.dataset.topic;
  filterAll();
}}

renderAll(QUESTIONS);
</script>
</body>
</html>"""

def _quiz_body(all_questions):
    """Return the HTML body fragment + JS for the quiz (no outer html/head/body tags)."""
    topic_counts = {}
    for q in all_questions:
        topic_counts[q["topic"]] = topic_counts.get(q["topic"], 0) + 1

    topic_buttons = "\n  ".join(
        f'<button class="mcq-filter-btn" data-topic="{k}" onclick="mcqSetTopic(this)">{v[0]} ({topic_counts.get(k,0)})</button>'
        for k, v in TOPICS.items()
    )
    q_json  = json.dumps(all_questions, ensure_ascii=False)
    t_json  = json.dumps({k: list(v) for k, v in TOPICS.items()}, ensure_ascii=False)
    total   = len(all_questions)

    return f"""<div class="mcq-hero">
  <h1>🎯 Backend MCQ Quiz</h1>
  <p>{total} Questions &nbsp;·&nbsp; Java &amp; Go &nbsp;·&nbsp; Microservices · Kafka · Redis · Databases · System Design &nbsp;·&nbsp; Product Companies</p>
</div>
<div class="mcq-controls">
  <input type="text" id="mcq-search" placeholder="Search questions…" oninput="mcqFilterAll()">
  <button class="mcq-filter-btn active" data-topic="all" onclick="mcqSetTopic(this)">All ({total})</button>
  {topic_buttons}
</div>
<div class="mcq-stats">
  <span>Showing <b id="mcq-showing">{total}</b> of {total}</span>
  <span>Answered <b id="mcq-answered">0</b></span>
  <span>Correct <b id="mcq-correct">0</b></span>
  <span style="margin-left:auto;font-size:.78rem;opacity:.6">Click an option or &ldquo;Show Answer&rdquo; to reveal</span>
  <button class="mcq-btn-resetall" onclick="mcqResetAll()">&#8635; Reset All</button>
</div>
<div class="mcq-list" id="mcq-qlist"></div>
<script>
(function(){{
const MCQ_Q={q_json};
const MCQ_T={t_json};
let mcqTopic='all', mcqAnswered=0, mcqCorrect=0;

function mcqBadge(t){{
  const [lbl,col]=MCQ_T[t]||[t,'#64748b'];
  return '<span class="mcq-badge" style="background:'+col+'22;color:'+col+';border:1px solid '+col+'44">'+lbl+'</span>';
}}

function mcqRender(qs){{
  const el=document.getElementById('mcq-qlist');
  if(!qs.length){{el.innerHTML='<div class="mcq-no-results">No questions found.</div>';return;}}
  el.innerHTML=qs.map(q=>
    '<div class="mcq-card" id="mcq-card-'+q.id+'">'+
    '<div class="mcq-qhead"><span class="mcq-num">#'+q.id+'</span>'+mcqBadge(q.topic)+
    '<div class="mcq-qtext">'+q.q+'</div></div>'+
    '<div class="mcq-options">'+q.options.map((o,i)=>
      '<div class="mcq-opt" id="mcq-opt-'+q.id+'-'+i+'" onclick="mcqChoose('+q.id+','+i+')">'+o+'</div>'
    ).join('')+'</div>'+
    '<div class="mcq-actions">'+
    '<button class="mcq-btn-show" onclick="mcqToggleAns('+q.id+')">Show Answer</button>'+
    '<button class="mcq-btn-reset" onclick="mcqReset('+q.id+')">Reset</button></div>'+
    '<div class="mcq-answer" id="mcq-ans-'+q.id+'">'+
    '<div class="mcq-answer-label">Correct Answer: '+q.answer+'</div>'+
    '<div class="mcq-exp">'+q.explanation+'</div></div></div>'
  ).join('');
  document.getElementById('mcq-showing').textContent=qs.length;
}}

window.mcqChoose=function(id,idx){{
  const opts=['A','B','C','D'];
  const qObj=MCQ_Q.find(function(x){{return x.id===id;}});
  const ans=qObj?qObj.answer:'A';
  const el=document.getElementById('mcq-opt-'+id+'-'+idx);
  if(el.classList.contains('correct')||el.classList.contains('wrong')) return;
  const ok=opts[idx]===ans;
  el.classList.add(ok?'correct':'wrong');
  if(!ok) document.getElementById('mcq-opt-'+id+'-'+opts.indexOf(ans)).classList.add('correct');
  mcqAnswered++; if(ok) mcqCorrect++;
  document.getElementById('mcq-answered').textContent=mcqAnswered;
  document.getElementById('mcq-correct').textContent=mcqCorrect;
  document.getElementById('mcq-ans-'+id).classList.add('open');
  var allCards=Array.from(document.querySelectorAll('.mcq-card'));
  var cur=document.getElementById('mcq-card-'+id);
  var next=allCards[allCards.indexOf(cur)+1];
  if(next) setTimeout(function(){{var top=next.getBoundingClientRect().top+window.scrollY-130;window.scrollTo({{top:top,behavior:'smooth'}});}},800);
}};

window.mcqToggleAns=function(id){{
  const a=document.getElementById('mcq-ans-'+id);
  a.classList.toggle('open');
  a.previousElementSibling.querySelector('.mcq-btn-show').textContent=
    a.classList.contains('open')?'Hide Answer':'Show Answer';
}};

window.mcqReset=function(id){{
  [0,1,2,3].forEach(i=>{{const o=document.getElementById('mcq-opt-'+id+'-'+i);if(o)o.className='mcq-opt';}});
  document.getElementById('mcq-ans-'+id).classList.remove('open');
}};

window.mcqResetAll=function(){{
  mcqAnswered=0; mcqCorrect=0;
  document.getElementById('mcq-answered').textContent=0;
  document.getElementById('mcq-correct').textContent=0;
  document.querySelectorAll('.mcq-opt').forEach(function(o){{o.className='mcq-opt';}});
  document.querySelectorAll('.mcq-answer').forEach(function(a){{a.classList.remove('open');}});
  document.querySelectorAll('.mcq-btn-show').forEach(function(b){{b.textContent='Show Answer';}});
  window.scrollTo({{top:0,behavior:'smooth'}});
}};

window.mcqFilterAll=function(){{
  const s=document.getElementById('mcq-search').value.toLowerCase();
  mcqRender(MCQ_Q.filter(q=>(mcqTopic==='all'||q.topic===mcqTopic)&&(!s||q.q.toLowerCase().includes(s))));
}};

window.mcqSetTopic=function(btn){{
  document.querySelectorAll('.mcq-filter-btn').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active'); mcqTopic=btn.dataset.topic; mcqFilterAll();
}};

mcqRender(MCQ_Q);
}})();
</script>"""


def build_html():
    """Generate standalone backend_mcqs.html (self-contained, no site dependency)."""
    from q_data import ALL_QUESTIONS
    topic_counts = {}
    for q in ALL_QUESTIONS:
        topic_counts[q["topic"]] = topic_counts.get(q["topic"], 0) + 1

    topic_buttons = "\n  ".join(
        f'<button class="filter-btn" data-topic="{k}" onclick="setTopic(this)">{v[0]} ({topic_counts.get(k,0)})</button>'
        for k, v in TOPICS.items()
    )

    html = HTML_TEMPLATE.replace("{TOPIC_BUTTONS}", topic_buttons)
    html = html.replace("{QUESTIONS_JSON}", json.dumps(ALL_QUESTIONS, ensure_ascii=False))
    html = html.replace("{TOPICS_JSON}", json.dumps({k: list(v) for k, v in TOPICS.items()}, ensure_ascii=False))

    out = os.path.join(os.path.dirname(__file__), "backend_mcqs.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated: {out}  ({len(ALL_QUESTIONS)} questions)")


def build_html_for_site(out_dir, html_shell_fn):
    """Generate InterviewRepository/mcq-quiz.html integrated with the site shell."""
    from q_data import ALL_QUESTIONS
    body = _quiz_body(ALL_QUESTIONS)
    extra_head = f"<style>{QUIZ_STYLES}</style>"
    html = html_shell_fn(
        title="MCQ Quiz — Backend Java/Go (5 YOE)",
        body=body,
        depth=0,
        extra_head=extra_head,
        description="150 MCQs for 5-year backend engineers: Microservices, Kafka, Redis, Databases, System Design, Java & Go — product company interview prep.",
        page_url="mcq-quiz.html",
    )
    out_path = os.path.join(str(out_dir), "mcq-quiz.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ mcq-quiz.html  ({len(ALL_QUESTIONS)} questions)")


if __name__ == "__main__":
    build_html()
