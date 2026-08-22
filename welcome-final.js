(() => {
  const image = 'data:image/webp;base64,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';

  if (document.getElementById('awais-welcome')) return;

  const style = document.createElement('style');
  style.textContent = `
    body.welcome-lock { overflow:hidden; }
    #awais-welcome { position:fixed; inset:0; z-index:999999; background:#05070b; color:#fff; overflow:hidden; font-family:'Space Grotesk','DM Sans',sans-serif; opacity:1; transition:opacity .8s ease, visibility .8s ease; cursor:pointer; }
    #awais-welcome.hide { opacity:0; visibility:hidden; pointer-events:none; }
    #awais-welcome::before { content:''; position:absolute; width:72vmin; height:72vmin; border-radius:50%; border:1px solid rgba(155,190,240,.12); left:50%; top:47%; transform:translate(-50%,-50%); box-shadow:0 0 80px rgba(80,120,190,.08) inset; }
    .aw-floor { position:absolute; left:8%; right:8%; bottom:8%; height:1px; background:linear-gradient(90deg,transparent,rgba(150,180,230,.3),transparent); box-shadow:0 -1px 80px rgba(120,160,230,.12); }
    .aw-copy { position:absolute; left:7vw; top:18vh; max-width:560px; z-index:3; }
    .aw-kicker { font-size:12px; letter-spacing:.35em; text-transform:uppercase; color:rgba(230,235,245,.58); margin-bottom:28px; }
    .aw-title { margin:0; font-size:clamp(46px,6vw,92px); line-height:.98; font-weight:500; letter-spacing:-.04em; color:#eef4ff; }
    .aw-title span { color:#9dc7ff; }
    .aw-sub { margin-top:22px; font-size:clamp(28px,3.2vw,52px); letter-spacing:-.035em; font-weight:500; }
    .aw-sub span { color:#9fc8ff; }
    .aw-person { position:absolute; z-index:2; left:50%; bottom:2vh; transform:translateX(-50%); width:min(300px,29vw); max-height:68vh; object-fit:contain; object-position:center bottom; filter:drop-shadow(0 28px 45px rgba(0,0,0,.65)); opacity:0; animation:personIn 1.1s .2s ease forwards, bow 1.4s 1.05s ease both; }
    .aw-glow { position:absolute; left:50%; bottom:6vh; width:360px; height:90px; transform:translateX(-50%); background:rgba(110,150,220,.15); filter:blur(35px); border-radius:50%; }
    .aw-hint { position:absolute; right:6vw; bottom:7vh; z-index:4; font-size:11px; letter-spacing:.28em; text-transform:uppercase; color:rgba(230,235,245,.48); }
    @keyframes personIn { from { opacity:0; transform:translate(-50%,30px) scale(.98); } to { opacity:1; transform:translate(-50%,0) scale(1); } }
    @keyframes bow { 0%,100% { transform:translateX(-50%) rotate(0deg); } 35% { transform:translateX(-50%) rotate(7deg); } 68% { transform:translateX(-50%) rotate(-2deg); } }
    @media (max-width:800px) {
      .aw-copy { left:7vw; right:7vw; top:12vh; text-align:center; max-width:none; }
      .aw-title { font-size:clamp(40px,9vw,64px); }
      .aw-sub { font-size:clamp(24px,6vw,34px); }
      .aw-person { width:min(250px,52vw); bottom:7vh; }
      .aw-hint { right:50%; transform:translateX(50%); bottom:3.5vh; white-space:nowrap; }
    }
  `;
  document.head.appendChild(style);

  const overlay = document.createElement('div');
  overlay.id = 'awais-welcome';
  overlay.setAttribute('role','button');
  overlay.setAttribute('aria-label','Enter portfolio');
  overlay.innerHTML = `
    <div class="aw-copy">
      <div class="aw-kicker">AI ENGINEER · BUILDER · PROBLEM SOLVER</div>
      <h1 class="aw-title">WELCOME TO WHAT'S <span>NEXT.</span></h1>
      <div class="aw-sub">WELCOME TO <span>AWAIS.</span></div>
    </div>
    <div class="aw-glow"></div>
    <img class="aw-person" src="${image}" alt="Awais welcome portrait" />
    <div class="aw-floor"></div>
    <div class="aw-hint">Click anywhere to enter</div>
  `;

  document.body.classList.add('welcome-lock');
  document.body.appendChild(overlay);

  const enter = () => {
    overlay.classList.add('hide');
    document.body.classList.remove('welcome-lock');
    setTimeout(() => overlay.remove(), 900);
  };

  overlay.addEventListener('click', enter, { once:true });
  window.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === 'Escape') enter(); }, { once:true });
  setTimeout(enter, 7000);
})();
