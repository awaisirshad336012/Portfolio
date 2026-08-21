const observer = new IntersectionObserver((entries) => { entries.forEach(entry => { if (entry.isIntersecting) entry.target.classList.add('visible'); }); }, { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

/* Hero V3: stronger personal-brand composition */
const heroCopy = document.querySelector('.hero-copy');
if (heroCopy) {
  heroCopy.innerHTML = `
    <div class="eyebrow"><span class="pulse"></span> AI ENGINEER · PYTHON · AI AUTOMATION</div>
    <div class="hero-kicker">BUILDING INTELLIGENT PRODUCTS FROM REAL PROBLEMS.</div>
    <h1>Turning ideas into<br><span class="hero-gradient">working intelligence.</span></h1>
    <p class="hero-text">I design and build AI applications, automation workflows, and backend systems that make complex work simpler.</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="#work">See what I build <span>↓</span></a>
      <a class="btn btn-ghost" href="https://www.linkedin.com/in/m-awais-irshad-b93783323" target="_blank" rel="noreferrer">Let's connect <span>↗</span></a>
    </div>
    <div class="hero-proof"><span>Python</span><i></i><span>LLM + RAG</span><i></i><span>Automation</span><i></i><span>Backend</span></div>`;
}

const heroVisual = document.querySelector('.hero-visual');
if (heroVisual) {
  heroVisual.innerHTML = `
    <div class="ai-orbit"><div class="orbit-ring ring-one"></div><div class="orbit-ring ring-two"></div><div class="core"><span>AI</span><small>ENGINE</small></div><div class="node node-a">PY</div><div class="node node-b">LLM</div><div class="node node-c">RAG</div><div class="node node-d">API</div></div>
    <div class="system-card"><div><span class="status-dot"></span> SYSTEM STATUS</div><strong>Building intelligent<br>software.</strong><small>Python / AI / Automation</small></div>`;
}

const menu = document.querySelector('.menu-btn');
const links = document.querySelector('.nav-links');
menu?.addEventListener('click', () => {
  const open = links.dataset.open === 'true';
  links.dataset.open = String(!open);
  links.style.display = open ? '' : 'flex';
  if (!open) {
    links.style.position = 'absolute'; links.style.top = '76px'; links.style.left = '0'; links.style.right = '0';
    links.style.padding = '22px'; links.style.background = 'rgba(7,9,13,.96)'; links.style.borderBottom = '1px solid #1b2330';
    links.style.flexDirection = 'column'; links.style.gap = '18px';
  }
});

document.querySelectorAll('a[href^="#"]').forEach(a => a.addEventListener('click', () => {
  if (window.innerWidth <= 850 && links) { links.style.display = ''; links.dataset.open = 'false'; }
}));
