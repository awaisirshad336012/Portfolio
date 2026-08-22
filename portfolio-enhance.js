(() => {
  const build = () => {
    const old = document.getElementById('awaisWelcome');
    const source = old?.querySelector('img')?.src || old?.querySelector('image')?.getAttribute('href');
    if (!source) return;

    old.remove();
    const style = document.createElement('style');
    style.textContent = `
      html.welcome-lock, html.welcome-lock body { overflow: hidden !important; }
      #awaisWelcome { position: fixed; inset: 0; z-index: 99999; background: #02060a; cursor: pointer; opacity: 1; transition: opacity .9s ease, transform 1s cubic-bezier(.2,.8,.2,1); }
      #awaisWelcome .aw-bg { position:absolute; inset:0; background: #02060a url("${source}") center/cover no-repeat; transform:scale(1.01); animation: aw-breathe 7s ease-out forwards; }
      #awaisWelcome::after { content:''; position:absolute; inset:0; background:linear-gradient(to bottom,rgba(2,6,10,.02),rgba(2,6,10,.15) 72%,rgba(2,6,10,.36)); pointer-events:none; }
      #awaisWelcome .aw-enter { position:absolute; left:50%; bottom:30px; transform:translateX(-50%); z-index:2; border:0; background:rgba(2,6,10,.18); color:rgba(245,248,255,.9); font:700 10px/1 'DM Sans',sans-serif; letter-spacing:.32em; text-transform:uppercase; padding:14px 18px 12px; cursor:pointer; white-space:nowrap; }
      #awaisWelcome .aw-enter::after { content:''; position:absolute; left:50%; bottom:0; transform:translateX(-50%); width:120px; height:1px; background:linear-gradient(90deg,transparent,#63a9ff,transparent); box-shadow:0 0 14px rgba(99,169,255,.75); }
      #awaisWelcome .aw-enter b { margin-left:9px; color:#6bb0ff; animation:aw-arrow 1.5s ease-in-out infinite; }
      #awaisWelcome:hover .aw-enter { color:#fff; }
      #awaisWelcome.is-leaving { opacity:0; transform:scale(1.02); pointer-events:none; }
      @keyframes aw-breathe { from {transform:scale(1.01)} to {transform:scale(1.055)} }
      @keyframes aw-arrow { 0%,100%{transform:translateY(0);opacity:.7} 50%{transform:translateY(4px);opacity:1} }
      @media(max-width:700px){#awaisWelcome .aw-bg{background-position:center center}#awaisWelcome .aw-enter{bottom:20px;font-size:8px;letter-spacing:.2em}}
    `;
    document.head.appendChild(style);
    const overlay = document.createElement('div');
    overlay.id = 'awaisWelcome';
    overlay.innerHTML = `<div class="aw-bg" aria-hidden="true"></div><button class="aw-enter" type="button">CLICK ANYWHERE TO ENTER <b>↓</b></button>`;
    document.body.appendChild(overlay);
    document.documentElement.classList.add('welcome-lock');

    const enter = () => {
      if (overlay.classList.contains('is-leaving')) return;
      overlay.classList.add('is-leaving');
      document.documentElement.classList.remove('welcome-lock');
      setTimeout(() => { overlay.remove(); style.remove(); }, 950);
    };
    overlay.addEventListener('click', enter);
    setTimeout(enter, 6500);
  };

  setTimeout(build, 500);
})();
