(() => {
  const style = document.createElement('style');
  style.textContent = `
    /* Cinematic welcome polish */
    #awais-welcome { background:radial-gradient(circle at 50% 42%,rgba(45,65,95,.22),transparent 44%),#05080d !important; }
    #awais-welcome::after { content:""; position:absolute; inset:0; background:linear-gradient(90deg,rgba(3,6,10,.82) 0%,rgba(3,6,10,.18) 34%,rgba(3,6,10,.05) 54%,rgba(3,6,10,.55) 100%); pointer-events:none; }
    .aw-welcome-inner { width:100% !important; max-width:none !important; }
    .aw-copy { left:7vw !important; right:auto !important; top:21vh !important; width:min(52vw,680px) !important; text-align:left !important; z-index:4 !important; }
    .aw-kicker { font-size:11px !important; letter-spacing:.30em !important; margin-bottom:24px !important; }
    .aw-title { font-size:clamp(42px,5.6vw,78px) !important; line-height:1.02 !important; max-width:680px !important; letter-spacing:-.035em !important; }
    .aw-sub { font-size:clamp(26px,3.4vw,48px) !important; margin-top:12px !important; letter-spacing:-.025em !important; }
    .aw-person { left:52% !important; bottom:-1vh !important; width:min(330px,34vw) !important; max-height:72vh !important; object-fit:cover !important; object-position:50% 18% !important; clip-path:ellipse(44% 53% at 50% 47%) !important; filter:brightness(.80) contrast(1.12) saturate(.86) drop-shadow(0 25px 55px rgba(0,0,0,.72)) !important; opacity:0 !important; animation:aw-person-in-clean 1.1s .15s cubic-bezier(.2,.8,.2,1) forwards !important; z-index:3 !important; }
    .aw-glow { bottom:3vh !important; width:420px !important; height:110px !important; opacity:.65 !important; }
    .aw-hint { right:6vw !important; bottom:30px !important; z-index:5 !important; }
    @keyframes aw-person-in-clean { 0%{opacity:0;transform:translate(-50%,40px) scale(.97)} 100%{opacity:1;transform:translate(-50%,0) scale(1)} }
    @media (max-width:900px){
      .aw-copy { left:6vw !important; top:15vh !important; width:58vw !important; }
      .aw-title { font-size:clamp(38px,7vw,62px) !important; }
      .aw-sub { font-size:clamp(22px,4vw,38px) !important; }
      .aw-person { left:66% !important; width:min(280px,38vw) !important; }
    }
    @media (max-width:600px){
      #awais-welcome::after { background:linear-gradient(180deg,rgba(3,6,10,.78) 0%,rgba(3,6,10,.22) 42%,rgba(3,6,10,.65) 100%); }
      .aw-copy { left:22px !important; top:12vh !important; width:calc(100% - 44px) !important; text-align:center !important; }
      .aw-kicker { font-size:8px !important; letter-spacing:.22em !important; }
      .aw-title { font-size:clamp(33px,10vw,48px) !important; }
      .aw-sub { font-size:clamp(22px,7vw,32px) !important; }
      .aw-person { left:50% !important; bottom:-2vh !important; width:min(280px,72vw) !important; max-height:55vh !important; }
      .aw-hint { left:50% !important; right:auto !important; transform:translateX(-50%) !important; bottom:20px !important; white-space:nowrap !important; font-size:8px !important; }
    }
  `;
  document.head.appendChild(style);
})();
