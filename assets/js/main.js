/* ─── SEARCH ──────────────────────────────────────────────────── */
let searchIndex = [];

async function loadSearchIndex() {
  try {
    const depth = (window.location.pathname.match(/\//g) || []).length;
    const prefix = depth <= 2 ? './' : '../'.repeat(depth - 2);
    const res = await fetch(prefix + 'search-index.json');
    searchIndex = await res.json();
  } catch (e) { searchIndex = []; }
}

function doSearch(query) {
  if (!query || query.length < 2) return [];
  const q = query.toLowerCase();
  return searchIndex.filter(item =>
    item.question.toLowerCase().includes(q) ||
    item.company.toLowerCase().includes(q) ||
    item.category.toLowerCase().includes(q) ||
    (item.tags && item.tags.toLowerCase().includes(q))
  ).slice(0, 15);
}

function renderSearchResults(results, query) {
  const box = document.getElementById('search-results');
  if (!box) return;
  if (!results.length) {
    box.innerHTML = `<div style="padding:20px;text-align:center;color:var(--text-muted)">No results for "<strong>${query}</strong>"</div>`;
  } else {
    box.innerHTML = results.map(r => `
      <a class="search-result-item" href="${r.url}">
        <div class="search-result-company">${r.company} · ${r.category}</div>
        <div class="search-result-text">${highlight(r.question, query)}</div>
      </a>`).join('');
  }
  box.classList.add('active');
}

function highlight(text, query) {
  const re = new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')})`, 'gi');
  return text.replace(re, '<mark style="background:rgba(59,130,246,0.3);color:inherit;border-radius:2px">$1</mark>');
}

function initSearch() {
  const input = document.getElementById('search-input');
  const box = document.getElementById('search-results');
  if (!input || !box) return;

  let timer;
  input.addEventListener('input', e => {
    clearTimeout(timer);
    const q = e.target.value.trim();
    if (!q) { box.classList.remove('active'); return; }
    timer = setTimeout(() => {
      const results = doSearch(q);
      renderSearchResults(results, q);
    }, 200);
  });

  input.addEventListener('keydown', e => {
    if (e.key === 'Escape') { box.classList.remove('active'); input.value = ''; }
  });

  document.addEventListener('click', e => {
    if (!e.target.closest('.search-bar')) box.classList.remove('active');
  });
}

/* ─── TABS ────────────────────────────────────────────────────── */
function initTabs() {
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.dataset.tab;
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      const panel = document.getElementById('tab-' + target);
      if (panel) panel.classList.add('active');
      history.replaceState(null, '', '#' + target);
    });
  });

  // Restore tab from URL hash
  const hash = location.hash.slice(1);
  if (hash) {
    const btn = document.querySelector(`.tab-btn[data-tab="${hash}"]`);
    if (btn) btn.click();
  }
}

/* ─── QUESTION ACCORDION ──────────────────────────────────────── */
function initQuestionAccordion() {
  document.querySelectorAll('.question-item').forEach(item => {
    item.addEventListener('click', () => {
      item.classList.toggle('open');
    });
  });
}

/* ─── FILTERS ─────────────────────────────────────────────────── */
function initFilters() {
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const group = btn.dataset.group || 'default';
      document.querySelectorAll(`.filter-btn[data-group="${group}"]`).forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      filterQuestions(btn.dataset.filter, group);
    });
  });
}

function filterQuestions(filterVal, group) {
  const items = document.querySelectorAll('.question-item[data-difficulty], .question-item[data-subcategory]');
  items.forEach(item => {
    if (!filterVal || filterVal === 'all') {
      item.closest('.q-wrapper') ? item.closest('.q-wrapper').style.display = '' : item.style.display = '';
    } else {
      const match = item.dataset.difficulty === filterVal || item.dataset.subcategory === filterVal;
      const wrapper = item.closest('.q-wrapper');
      if (wrapper) wrapper.style.display = match ? '' : 'none';
      else item.style.display = match ? '' : 'none';
    }
  });
  updateCounts();
}

function updateCounts() {
  document.querySelectorAll('.tab-panel').forEach(panel => {
    const visible = panel.querySelectorAll('.question-item:not([style*="none"])').length;
    const counter = panel.querySelector('.q-count');
    if (counter) counter.textContent = visible + ' questions';
  });
}

/* ─── BACK TO TOP ─────────────────────────────────────────────── */
function initBackToTop() {
  const btn = document.getElementById('back-to-top');
  if (!btn) return;
  window.addEventListener('scroll', () => {
    btn.classList.toggle('visible', window.scrollY > 400);
  });
  btn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
}

/* ─── COPY QUESTION ───────────────────────────────────────────── */
function copyQuestion(text) {
  navigator.clipboard.writeText(text).then(() => {
    const el = event.currentTarget;
    const orig = el.innerHTML;
    el.innerHTML = '✓';
    setTimeout(() => el.innerHTML = orig, 1200);
  });
}

/* ─── KEYBOARD SHORTCUT ───────────────────────────────────────── */
function initKeyboard() {
  document.addEventListener('keydown', e => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      const input = document.getElementById('search-input');
      if (input) { input.focus(); input.select(); }
    }
  });
}

/* ─── TIER CARD COLORS ────────────────────────────────────────── */
function applyTierColors() {
  const colors = ['#FFD700','#C0C0C0','#CD7F32','#4169E1','#FF6B35','#9B59B6','#1ABC9C','#95A5A6'];
  document.querySelectorAll('[data-tier]').forEach(el => {
    const tier = parseInt(el.dataset.tier) - 1;
    if (colors[tier]) el.style.setProperty('--tier-color', colors[tier]);
  });
}

/* ─── ANIMATE ON SCROLL ───────────────────────────────────────── */
function initScrollAnimations() {
  if (!('IntersectionObserver' in window)) return;
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.style.opacity = '1'; e.target.style.transform = 'none'; obs.unobserve(e.target); }
    });
  }, { threshold: 0.1 });
  document.querySelectorAll('.tier-card, .company-card').forEach((el, i) => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(16px)';
    el.style.transition = `opacity .4s ease ${i * 0.05}s, transform .4s ease ${i * 0.05}s`;
    obs.observe(el);
  });
}

/* ─── INIT ────────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  loadSearchIndex();
  initSearch();
  initTabs();
  initQuestionAccordion();
  initFilters();
  initBackToTop();
  initKeyboard();
  applyTierColors();
  initScrollAnimations();

  // Activate first tab by default if no hash
  if (!location.hash) {
    const firstTab = document.querySelector('.tab-btn');
    if (firstTab) firstTab.click();
  }
});
