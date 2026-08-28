/* AWAIS IRSHAD — immersive storyboard welcome. No numbered captions. */
(function(){
  const boot=document.getElementById('boot');
  if(!boot)return;
  boot.innerHTML=`
    <div class="world-stars"></div>
    <div class="world-dust"></div>
    <div class="world-horizon"></div>
    <div class="world-planet" aria-hidden="true"><div class="planet-glow"></div><div class="planet-surface"></div><div class="planet-ring r1"></div><div class="planet-ring r2"></div></div>
    <div class="world-star" aria-hidden="true"><span></span></div>
    <div class="world-beam" aria-hidden="true"></div>
    <div class="world-ripples" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
    <div class="world-trails" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>
    <div class="world-words" aria-hidden="true">
      <span class="wd1">DATA</span><span class="wd2">AI</span><span class="wd3">PYTHON</span><span class="wd4">RAG</span><span class="wd5">AUTOMATION</span><span class="wd6">MACHINE LEARNING</span><span class="wd7">GENERATIVE AI</span><span class="wd8">AGENTS</span>
    </div>
    <div class="world-ai" aria-hidden="true"><div class="ai-head"><i></i><i></i><b></b></div><div class="ai-core"></div></div>
    <div class="final-copy">
      <p class="kicker">WELCOME TO</p>
      <h1><span>AWAIS</span><span>IRSHAD</span></h1>
      <div class="portfolio">PORTFOLIO</div>
      <p class="manifesto">I TURN DATA INTO <strong>INTELLIGENCE.</strong></p>
      <a class="cta" href="#home" id="finalEnter">EXPLORE MY WORK&nbsp; ↗</a>
    </div>`;
  boot.classList.add('final-welcome');
  const enter=document.getElementById('finalEnter');
  const go=()=>{boot.classList.add('exit');document.body.classList.remove('lock');setTimeout(()=>boot.remove(),1100);setTimeout(()=>{if(typeof speak==='function'&&typeof voiceEnabled!=='undefined'&&voiceEnabled)speak(introText)},550)};
  enter?.addEventListener('click',e=>{e.preventDefault();go()});
  setTimeout(()=>{if(document.body.contains(boot)&&!boot.classList.contains('exit'))go()},15000);
})();
