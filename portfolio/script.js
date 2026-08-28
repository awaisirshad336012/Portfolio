const boot=document.getElementById('boot');
const voiceToggle=document.getElementById('voiceToggle');
const chatVoice=document.getElementById('chatVoice');
const status=document.getElementById('agentStatus');
let voiceEnabled=true,introDone=false;

/* =========================================================
   CLEAN CINEMATIC WELCOME — visual story, no numbered labels
   ========================================================= */
if(boot){
  boot.innerHTML=`
    <div class="welcome-atmosphere" aria-hidden="true">
      <span class="welcome-orb"></span>
      <span class="welcome-ring ring-one"></span><span class="welcome-ring ring-two"></span>
      <span class="welcome-particle p-one"></span><span class="welcome-particle p-two"></span><span class="welcome-particle p-three"></span>
      <span class="welcome-particle p-four"></span><span class="welcome-particle p-five"></span>
      <span class="welcome-spark spark-one"></span><span class="welcome-spark spark-two"></span>
    </div>
    <div class="welcome-line line-one"></div><div class="welcome-line line-two"></div>
    <div class="welcome-data-word" aria-hidden="true">DATA</div>
    <div class="welcome-intelligence-word" aria-hidden="true">INTELLIGENCE</div>
    <div class="welcome-copy">
      <div class="welcome-kicker"><span></span> WELCOME TO</div>
      <h1 class="welcome-name"><span>AWAIS</span><span>IRSHAD</span></h1>
      <div class="welcome-portfolio">PORTFOLIO</div>
      <p class="welcome-manifesto">I TURN DATA INTO <strong>INTELLIGENCE.</strong></p>
      <div class="welcome-actions"><button id="enter" type="button"><span>EXPLORE MY WORK</span><b>↗</b></button><button id="voiceIntro" class="voice-intro" type="button">◉ VOICE INTRO ON</button></div>
      <div class="voice-note">Awais AI will welcome you</div>
    </div>
    <div class="welcome-ai-presence" aria-hidden="true"><div class="ai-core"></div><div class="ai-face"><i></i><i></i><b></b></div></div>
    <div class="welcome-footer"><span>AI / ML ENGINEER</span><span>PYTHON · AI · AUTOMATION</span></div>`;

  const s=document.createElement('style');s.textContent=`
  #boot{overflow:hidden!important;background:#040506!important}
  .welcome-atmosphere{position:absolute;inset:0;z-index:1;pointer-events:none;overflow:hidden}
  .welcome-orb{position:absolute;width:28vw;height:28vw;min-width:280px;min-height:280px;right:12%;top:18%;border-radius:50%;background:radial-gradient(circle,rgba(121,191,232,.13) 0,rgba(121,191,232,.055) 24%,rgba(216,170,104,.025) 48%,transparent 70%);filter:blur(4px);animation:orbBreathe 5s ease-in-out infinite}
  .welcome-ring{position:absolute;border:1px solid rgba(121,191,232,.12);border-radius:50%;right:13%;top:18%;transform-origin:center;animation:ringDrift 12s linear infinite}
  .ring-one{width:27vw;height:27vw;min-width:270px;min-height:270px}.ring-two{width:39vw;height:15vw;min-width:390px;min-height:150px;transform:rotate(-28deg);border-color:rgba(216,170,104,.10);animation-duration:18s;animation-direction:reverse}
  .welcome-particle,.welcome-spark{position:absolute;border-radius:50%;background:#79bfe8;box-shadow:0 0 18px rgba(121,191,232,.75);opacity:0;animation:particleFloat 5s ease-in-out infinite}
  .welcome-particle{width:3px;height:3px}.p-one{right:30%;top:28%;animation-delay:.2s}.p-two{right:19%;top:48%;animation-delay:1.2s}.p-three{right:35%;top:63%;animation-delay:2.1s}.p-four{right:55%;top:30%;animation-delay:3s}.p-five{right:10%;top:25%;animation-delay:3.8s}.welcome-spark{width:5px;height:5px;background:#d8aa68;box-shadow:0 0 26px rgba(216,170,104,.85)}.spark-one{left:23%;top:36%;animation:singleSpark 4.5s ease-in-out infinite}.spark-two{left:63%;top:70%;animation:singleSpark 5.5s 1s ease-in-out infinite}
  .welcome-line{position:absolute;height:1px;z-index:2;transform-origin:left center;background:linear-gradient(90deg,transparent,rgba(121,191,232,.4),transparent);opacity:.35}.line-one{width:42vw;left:7%;top:37%;transform:rotate(-9deg);animation:lineSweep 7s ease-in-out infinite}.line-two{width:34vw;right:4%;bottom:27%;transform:rotate(14deg);background:linear-gradient(90deg,transparent,rgba(216,170,104,.35),transparent);animation:lineSweep 9s 1s ease-in-out infinite reverse}
  .welcome-data-word,.welcome-intelligence-word{position:absolute;z-index:2;font:500 clamp(4rem,11vw,10rem)/1 'Space Grotesk';letter-spacing:-.06em;pointer-events:none;opacity:0;white-space:nowrap}.welcome-data-word{left:7%;top:22%;color:rgba(121,191,232,.035);animation:dataGhost 7.5s ease-in-out forwards}.welcome-intelligence-word{right:4%;bottom:17%;font-size:clamp(3rem,8vw,7rem);color:rgba(216,170,104,.035);animation:intelGhost 7.5s 2s ease-in-out forwards}
  .welcome-ai-presence{position:absolute;z-index:3;right:19%;top:27%;width:18vw;height:24vw;min-width:180px;min-height:240px;opacity:.72;animation:aiPresence 6s ease-in-out infinite;pointer-events:none}.ai-core{position:absolute;inset:12%;border-radius:50%;background:radial-gradient(circle,rgba(121,191,232,.16),rgba(121,191,232,.025) 48%,transparent 70%);filter:blur(8px)}.ai-face{position:absolute;left:25%;top:18%;width:50%;height:55%;border:1px solid rgba(121,191,232,.24);border-radius:48% 48% 44% 44%;background:linear-gradient(150deg,rgba(121,191,232,.035),rgba(216,170,104,.018));box-shadow:inset 0 0 40px rgba(121,191,232,.04),0 0 60px rgba(121,191,232,.07)}.ai-face i{position:absolute;top:42%;width:10px;height:3px;border-radius:50%;background:#79bfe8;box-shadow:0 0 12px #79bfe8}.ai-face i:first-child{left:28%}.ai-face i:nth-child(2){right:28%}.ai-face b{position:absolute;left:38%;right:38%;bottom:24%;height:1px;background:rgba(216,170,104,.55);box-shadow:0 0 12px rgba(216,170,104,.5)}
  .welcome-copy{z-index:5!important}.welcome-name span:last-child{color:#eee8dd!important}.welcome-portfolio{color:#79bfe8!important}.welcome-manifesto strong{color:#d8aa68!important}
  @keyframes orbBreathe{50%{transform:scale(1.08);opacity:.8}}@keyframes ringDrift{to{transform:rotate(360deg)}}@keyframes particleFloat{0%,100%{opacity:0;transform:translate(0,12px) scale(.5)}35%,65%{opacity:.8}50%{transform:translate(-18px,-28px) scale(1.3)}}@keyframes singleSpark{0%,100%{opacity:0;transform:scale(.3)}30%{opacity:1}55%{opacity:.3;transform:scale(2.8)}75%{opacity:0;transform:translate(45px,-35px) scale(.2)}}@keyframes lineSweep{0%,100%{opacity:0;transform:scaleX(.4) rotate(-9deg)}45%{opacity:.5;transform:scaleX(1) rotate(-9deg)}70%{opacity:.12}}@keyframes dataGhost{0%{opacity:0;transform:translateX(-20px)}25%{opacity:1;transform:none}65%{opacity:.15}100%{opacity:0;transform:translateX(35px)}}@keyframes intelGhost{0%{opacity:0;transform:translateX(30px)}25%{opacity:.8;transform:none}65%{opacity:.1}100%{opacity:0;transform:translateX(-30px)}}@keyframes aiPresence{0%,100%{transform:translateY(8px) scale(.98);opacity:.45}50%{transform:translateY(-8px) scale(1.02);opacity:.78}}
  @media(max-width:900px){.welcome-ai-presence{right:8%;top:23%;width:25vw;height:32vw}.welcome-data-word{left:3%;top:17%}.welcome-intelligence-word{right:-4%;bottom:13%}}
  @media(max-width:600px){.welcome-ai-presence{right:8%;top:17%;width:32vw;height:40vw;opacity:.5}.welcome-data-word{font-size:4rem;top:14%}.welcome-intelligence-word{font-size:3rem;bottom:12%}.welcome-line{opacity:.18}}
  `;document.head.appendChild(s);

  const enter=document.getElementById('enter');
  const voiceIntro=document.getElementById('voiceIntro');
  const launch=()=>{if(introDone)return;introDone=true;boot.classList.add('exit');document.body.classList.remove('lock');if(status)status.textContent='Welcome — Awais AI is guiding you';if(voiceEnabled)setTimeout(()=>speak(introText),420);setTimeout(()=>boot.remove(),1150)};
  enter?.addEventListener('click',()=>{voiceEnabled=true;launch()});
  voiceIntro?.addEventListener('click',()=>{voiceEnabled=true;voiceIntro.textContent='✓ VOICE INTRO ENABLED';voiceIntro.style.color='#d8aa68';speak(introText)});
  setTimeout(launch,9000);
}

/* =========================================================
   VOICE GUIDE
   ========================================================= */
const pickVoice=()=>{if(!('speechSynthesis'in window))return null;const voices=window.speechSynthesis.getVoices();return voices.find(v=>/en-US/i.test(v.lang)&&/Microsoft|Google|Samantha|Daniel|Natural/i.test(v.name))||voices.find(v=>/^en-US/i.test(v.lang))||voices.find(v=>/^en/i.test(v.lang))||voices[0]||null};
const speak=(text)=>{if(!voiceEnabled||!('speechSynthesis'in window))return false;window.speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(text),v=pickVoice();if(v)u.voice=v;u.rate=.92;u.pitch=.98;u.volume=1;window.speechSynthesis.speak(u);return true};
const introText='Welcome to Awais Irshad portfolio. I am Awais AI, your personal portfolio guide. Awais is an AI and machine learning engineer focused on Python, generative AI, intelligent automation, and practical AI applications. Let me introduce you to his work.';
voiceToggle?.addEventListener('click',()=>{voiceEnabled=!voiceEnabled;voiceToggle.textContent=voiceEnabled?'◉ VOICE ON':'◉ VOICE';voiceToggle.style.color=voiceEnabled?'#d8aa68':'';if(!voiceEnabled)window.speechSynthesis?.cancel();else speak('Voice assistant is now on.')});

/* Latest projects — presentation only; project folders remain untouched. */
const projectGrid=document.querySelector('.project-grid');
if(projectGrid){
 const latest=[
  {no:'04',type:'RAG / GENERATIVE AI',name:'InsightDoc',desc:'RAG-based document Q&A system for PDF/TXT files with source and page citations.',tags:['Python','RAG','ChromaDB','Streamlit','OpenRouter'],url:'https://github.com/awaisirshad336012/Portfolio/tree/main/InsightDoc',featured:true},
  {no:'05',type:'WEB SCRAPING / ML',name:'E-commerce Price Intelligence',desc:'Product scraping, historical price tracking, ML price prediction and Buy/Wait recommendations.',tags:['Selenium','BeautifulSoup','Scikit-learn','SQLite','Streamlit'],url:'https://github.com/awaisirshad336012/Portfolio/tree/main/ecommerce-price-intelligence'}
 ];latest.forEach(p=>{const card=document.createElement('article');card.className='project'+(p.featured?' featured':'');card.innerHTML=`<div class="project-no">${p.no}</div><div class="project-type">${p.type}</div><h4>${p.name}</h4><p>${p.desc}</p><div class="tags">${p.tags.map(t=>`<span>${t}</span>`).join('')}</div><a href="${p.url}" target="_blank" rel="noreferrer">View repository <b>↗</b></a>`;projectGrid.appendChild(card)})
}

/* Mobile menu */
const menu=document.getElementById('menu'),nav=document.querySelector('nav');menu?.addEventListener('click',()=>{const open=nav.dataset.open==='1';nav.dataset.open=open?'0':'1';nav.style.display=open?'':'flex';if(!open)Object.assign(nav.style,{position:'absolute',top:'64px',left:'0',right:'0',padding:'20px',background:'#050607',flexDirection:'column',borderBottom:'1px solid rgba(216,170,104,.2)'})});
document.querySelectorAll('nav a').forEach(a=>a.addEventListener('click',()=>{if(innerWidth<=850){nav.style.display='';nav.dataset.open='0'}}));

/* Portfolio assistant */
const responses={about:'Awais Irshad is an AI/ML Engineer focused on Python, machine learning, generative AI, backend development and automation.',projects:'Awais has built LedgerIQ AI, InsightDoc, E-commerce Price Intelligence, Todo App and Sky Briefing.',tech:'His stack includes Python, NumPy, Pandas, Scikit-learn, LLM applications, RAG, ChromaDB, OpenRouter, Django, APIs, SQLite, Selenium, BeautifulSoup, n8n, Docker, Streamlit and GitHub.',contact:'You can contact Awais through WhatsApp at +92 341 2850260, email at awaisirshad336012@gmail.com, or LinkedIn.'};
function answer(q){const s=q.toLowerCase();if(/contact|whatsapp|email|linkedin/.test(s))return responses.contact;if(/project|build|work|insightdoc|price/.test(s))return responses.projects;if(/tech|skill|stack|use/.test(s))return responses.tech;if(/who|about|awais/.test(s))return responses.about;return 'I can tell you about Awais, his projects, technologies, or contact details.'}
const log=document.getElementById('chatLog'),form=document.getElementById('chatForm'),input=document.getElementById('chatInput');
function sendQuestion(q){if(!q||!log)return;const u=document.createElement('div');u.className='msg user-msg';u.textContent=q;log.appendChild(u);const a=document.createElement('div');a.className='msg agent-msg';const text=answer(q);a.textContent=text;log.appendChild(a);log.scrollTop=log.scrollHeight;speak(text)}
form?.addEventListener('submit',e=>{e.preventDefault();const q=input.value.trim();input.value='';sendQuestion(q)});document.querySelectorAll('.quick-questions button').forEach(b=>b.addEventListener('click',()=>sendQuestion(b.dataset.question)));
chatVoice?.addEventListener('click',()=>{voiceEnabled=!voiceEnabled;chatVoice.textContent=voiceEnabled?'VOICE ON':'VOICE OFF';if(voiceEnabled)speak('Voice mode is on. Ask me anything about Awais.');else window.speechSynthesis?.cancel()});
const SpeechRecognition=window.SpeechRecognition||window.webkitSpeechRecognition;if(SpeechRecognition&&input){const mic=document.createElement('button');mic.type='button';mic.textContent='🎙';mic.title='Speak to Awais AI';mic.style.cssText='width:42px;background:#080b0d;color:#d8aa68;border:0;border-left:1px solid rgba(121,191,232,.14);cursor:pointer';form.insertBefore(mic,form.lastElementChild);const rec=new SpeechRecognition();rec.lang='en-US';rec.interimResults=false;mic.onclick=()=>{rec.start();mic.textContent='…'};rec.onresult=e=>{input.value=e.results[0][0].transcript;mic.textContent='🎙';form.requestSubmit()};rec.onerror=()=>mic.textContent='🎙';rec.onend=()=>mic.textContent='🎙'}
