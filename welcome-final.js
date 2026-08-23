(() => {
  if (document.getElementById('awais-welcome')) return;

  const style = document.createElement('style');
  style.textContent = `
    #awais-welcome{position:fixed;inset:0;z-index:99999;background:radial-gradient(circle at 50% 18%,#102440 0%,#050a12 38%,#010409 78%);color:#fff;overflow:hidden;font-family:"Space Grotesk",system-ui,sans-serif;cursor:pointer}
    #awais-welcome *{box-sizing:border-box}
    .aw-stage{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.05),rgba(0,0,0,.45)),radial-gradient(ellipse at 50% 95%,rgba(51,122,220,.18),transparent 42%)}
    .aw-floor{position:absolute;left:7%;right:7%;bottom:8%;height:2px;background:linear-gradient(90deg,transparent,#1d6fd1,transparent);box-shadow:0 0 28px #1269d8}
    .aw-title{position:absolute;left:50%;top:22%;transform:translateX(-50%);width:min(720px,86vw);text-align:center;opacity:0;animation:awTitleIn 1.1s ease .7s forwards}
    .aw-kicker{font-size:12px;letter-spacing:.45em;color:#8e9bad;margin-bottom:25px;text-transform:uppercase}
    .aw-title h1{font-size:clamp(42px,6.7vw,92px);line-height:.95;margin:0;font-weight:600;letter-spacing:.03em;background:linear-gradient(90deg,#dcecff,#7db5ff,#a18bff);-webkit-background-clip:text;background-clip:text;color:transparent}
    .aw-title h2{font-size:clamp(34px,4.7vw,68px);margin:16px 0 0;font-weight:500;letter-spacing:.16em;color:#f0f5ff}
    .aw-sub{margin-top:18px;color:#78879b;font-size:12px;letter-spacing:.35em;text-transform:uppercase}
    .aw-client,.aw-me{position:absolute;bottom:10%;width:210px;height:350px;filter:drop-shadow(0 18px 35px rgba(0,0,0,.6));transition:transform 1.35s cubic-bezier(.16,1,.3,1),opacity .8s ease}
    .aw-client{left:3%;transform:translateX(-180px);opacity:0}
    .aw-me{right:3%;transform:translateX(180px);opacity:0}
    #awais-welcome.ready .aw-client{transform:translateX(0);opacity:1}
    #awais-welcome.ready .aw-me{transform:translateX(0);opacity:1}
    .aw-person{position:absolute;left:50%;bottom:0;transform:translateX(-50%);width:118px;height:285px}
    .aw-head{position:absolute;left:43px;top:0;width:34px;height:45px;border-radius:50%;background:linear-gradient(135deg,#f0c7ad,#b97958);box-shadow:inset -6px -8px 0 rgba(0,0,0,.12)}
    .aw-hair{position:absolute;left:39px;top:-2px;width:42px;height:22px;border-radius:22px 22px 10px 10px;background:#111820;z-index:2}
    .aw-body{position:absolute;left:20px;top:37px;width:80px;height:128px;border-radius:18px 18px 14px 14px;background:linear-gradient(145deg,#243b62,#071222 75%);border:1px solid rgba(150,190,255,.16);box-shadow:inset 0 0 0 1px rgba(255,255,255,.03)}
    .aw-shirt{position:absolute;left:39px;top:40px;width:42px;height:58px;background:#f3f5f7;clip-path:polygon(30% 0,70% 0,100% 100%,0 100%)}
    .aw-arm{position:absolute;top:53px;width:18px;height:104px;border-radius:14px;background:#102340;transform-origin:top center;transition:transform .8s ease 1s}
    .aw-arm.l{left:10px;transform:rotate(12deg)} .aw-arm.r{right:10px;transform:rotate(-12deg)}
    .aw-leg{position:absolute;top:156px;width:25px;height:124px;border-radius:12px;background:linear-gradient(180deg,#0b1629,#07101d)}
    .aw-leg.l{left:32px;transform:rotate(3deg)} .aw-leg.r{right:32px;transform:rotate(-3deg)}
    .aw-shoe{position:absolute;bottom:0;width:48px;height:14px;border-radius:12px 18px 8px 5px;background:#03070d}
    .aw-shoe.l{left:18px}.aw-shoe.r{right:18px}
    .aw-client .aw-person{transform:translateX(-50%) scale(.94)}
    .aw-me .aw-person{transform:translateX(-50%) scale(1.03)}
    #awais-welcome.ready .aw-me .aw-arm.r{transform:rotate(-68deg)}
    .aw-role{position:absolute;bottom:-28px;left:50%;transform:translateX(-50%);white-space:nowrap;color:#6f8196;font-size:10px;letter-spacing:.35em;text-transform:uppercase}
    .aw-enter{position:absolute;left:50%;bottom:7%;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;gap:10px;color:#8190a4;font-size:10px;letter-spacing:.38em;text-transform:uppercase;opacity:0;animation:awEnterIn 1s ease 2.2s forwards}
    .aw-enter .line{width:140px;height:1px;background:linear-gradient(90deg,transparent,#55a4ff,transparent);box-shadow:0 0 15px #2f82ff}
    #awais-welcome.exit{pointer-events:none;opacity:0;transition:opacity .9s ease}
    @keyframes awTitleIn{from{opacity:0;transform:translate(-50%,18px)}to{opacity:1;transform:translate(-50%,0)}}
    @keyframes awEnterIn{from{opacity:0;transform:translate(-50%,10px)}to{opacity:1;transform:translate(-50%,0)}}
    @media(max-width:900px){.aw-client{left:-5%}.aw-me{right:-7%}.aw-title{top:18%}.aw-client,.aw-me{transform:scale(.8) translateX(-120px)}#awais-welcome.ready .aw-client{transform:scale(.8) translateX(0)}#awais-welcome.ready .aw-me{transform:scale(.8) translateX(0)}}
    @media(max-width:650px){.aw-client,.aw-me{opacity:.35}.aw-client{left:-70px}.aw-me{right:-85px}.aw-title{top:20%}.aw-kicker{font-size:9px}.aw-sub{letter-spacing:.18em;font-size:9px}.aw-role{font-size:8px}.aw-enter{bottom:4%;font-size:8px}}
  `;
  document.head.appendChild(style);

  const root = document.createElement('div');
  root.id = 'awais-welcome';
  root.innerHTML = `
    <div class="aw-stage"></div>
    <div class="aw-floor"></div>
    <div class="aw-client">
      <div class="aw-person">
        <div class="aw-hair"></div><div class="aw-head"></div><div class="aw-body"></div><div class="aw-shirt"></div>
        <div class="aw-arm l"></div><div class="aw-arm r"></div><div class="aw-leg l"></div><div class="aw-leg r"></div>
        <div class="aw-shoe l"></div><div class="aw-shoe r"></div>
      </div><div class="aw-role">CLIENT · COMPANY</div>
    </div>
    <div class="aw-me">
      <div class="aw-person">
        <div class="aw-hair"></div><div class="aw-head"></div><div class="aw-body"></div><div class="aw-shirt"></div>
        <div class="aw-arm l"></div><div class="aw-arm r"></div><div class="aw-leg l"></div><div class="aw-leg r"></div>
        <div class="aw-shoe l"></div><div class="aw-shoe r"></div>
      </div><div class="aw-role">AWAIS · AI ENGINEER</div>
    </div>
    <div class="aw-title"><div class="aw-kicker">WELCOME TO WHAT'S NEXT.</div><h1>WELCOME TO</h1><h2>AWAIS<span style="color:#5aa7ff">.</span></h2><div class="aw-sub">AI ENGINEER · BUILDER · PROBLEM SOLVER</div></div>
    <div class="aw-enter"><div class="line"></div><span>CLICK ANYWHERE TO ENTER</span></div>
  `;
  document.body.appendChild(root);
  requestAnimationFrame(() => root.classList.add('ready'));

  let entered = false;
  const enter = () => {
    if (entered) return;
    entered = true;
    root.classList.add('exit');
    setTimeout(() => root.remove(), 950);
  };
  root.addEventListener('click', enter);
  setTimeout(enter, 8000);
})();