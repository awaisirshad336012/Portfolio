/* Final welcome: starts at a blinking star; no numbered story labels. */
(function(){
  const boot=document.getElementById('boot');
  if(!boot)return;
  boot.innerHTML=`
    <div class="final-stars"></div>
    <div class="final-rain"></div>
    <div class="final-star" aria-hidden="true"></div>
    <div class="final-ripples" aria-hidden="true"></div>
    <div class="final-words" aria-hidden="true">
      <span class="w-data">DATA</span><span class="w-ai">AI</span><span class="w-python">PYTHON</span><span class="w-rag">RAG</span><span class="w-automation">AUTOMATION</span><span class="w-ml">MACHINE LEARNING</span>
    </div>
    <div class="final-ai" aria-hidden="true"><div class="head"></div><i></i><i></i><b></b></div>
    <div class="final-copy">
      <p class="kicker">WELCOME TO</p>
      <h1><span>AWAIS</span><span>IRSHAD</span></h1>
      <div class="portfolio">PORTFOLIO</div>
      <p class="manifesto">I TURN DATA INTO <strong>INTELLIGENCE.</strong></p>
      <a class="cta" href="#home" id="finalEnter">EXPLORE MY WORK&nbsp; ↗</a>
      <span class="voice">AWA​IS AI · VOICE GUIDE READY</span>
    </div>`;
  boot.classList.add('final-welcome');
  const enter=document.getElementById('finalEnter');
  const go=()=>{boot.classList.add('exit');document.body.classList.remove('lock');setTimeout(()=>boot.remove(),950);setTimeout(()=>{if(typeof speak==='function'&&typeof voiceEnabled!=='undefined'&&voiceEnabled)speak(introText)},500)};
  enter?.addEventListener('click',e=>{e.preventDefault();go()});
  /* Give the cinematic reveal enough time to finish; visitor can enter sooner. */
  setTimeout(()=>{if(document.body.contains(boot)&&!boot.classList.contains('exit'))go()},12500);
})();
