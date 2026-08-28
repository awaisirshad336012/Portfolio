/* AWAIS IRSHAD — cinematic storyboard welcome. Visual story only, no numbered captions. */
(function(){
  const boot=document.getElementById('boot');
  if(!boot)return;
  boot.innerHTML=`
    <div class="world-stars"></div><div class="world-dust"></div><div class="world-horizon"></div>
    <div class="world-planet" aria-hidden="true"><div class="planet-glow"></div><div class="planet-surface"></div><div class="planet-ring r1"></div><div class="planet-ring r2"></div></div>
    <div class="world-star" aria-hidden="true"><span></span></div><div class="world-beam" aria-hidden="true"></div>
    <div class="world-ripples" aria-hidden="true"><i></i><i></i><i></i><i></i></div><div class="world-trails" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>
    <div class="world-words" aria-hidden="true"></div>
    <div class="story-data" aria-hidden="true">
      <span class="data-word">DATA</span><span class="intel-word">INTELLIGENCE</span>
      <i class="stream"></i><i class="stream"></i><i class="stream"></i><i class="stream"></i><b class="core"></b>
      <i class="particle p1"></i><i class="particle p2"></i><i class="particle p3"></i><i class="particle p4"></i><i class="particle p5"></i><i class="particle p6"></i>
    </div>
    <div class="awakening" aria-hidden="true"><div class="neural"></div><div class="face"></div><i class="node n1"></i><i class="node n2"></i><i class="node n3"></i><i class="node n4"></i><i class="node n5"></i></div>
    <div class="world-ai" aria-hidden="true"><div class="ai-head"><i></i><i></i><b></b></div><div class="ai-core"></div></div>
    <div class="final-copy">
      <div class="final-ai" aria-hidden="true">
        <div class="final-ai-glow"></div><div class="final-ai-rings"><i></i><i></i><i></i></div>
        <div class="final-ai-face"><i class="eye e1"></i><i class="eye e2"></i><i class="ai-line l1"></i><i class="ai-line l2"></i><i class="ai-line l3"></i></div>
        <span class="ai-node an1"></span><span class="ai-node an2"></span><span class="ai-node an3"></span><span class="ai-node an4"></span>
      </div>
      <div class="final-copy-text"><p class="kicker">WELCOME TO</p><h1><span>AWAIS</span><span>IRSHAD</span></h1><div class="portfolio">PORTFOLIO</div><p class="manifesto">I TURN DATA INTO <strong>INTELLIGENCE.</strong></p><a class="cta" href="#home" id="finalEnter">EXPLORE MY WORK&nbsp; ↗</a></div>
    </div>`;
  boot.classList.add('final-welcome');
  const enter=document.getElementById('finalEnter');
  const go=()=>{boot.classList.add('exit');document.body.classList.remove('lock');setTimeout(()=>boot.remove(),1100);setTimeout(()=>{if(typeof speak==='function'&&typeof voiceEnabled!=='undefined'&&voiceEnabled)speak(introText)},550)};
  enter?.addEventListener('click',e=>{e.preventDefault();go()});
  setTimeout(()=>{if(document.body.contains(boot)&&!boot.classList.contains('exit'))go()},15000);
})();
