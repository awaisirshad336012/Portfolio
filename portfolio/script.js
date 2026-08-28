const boot=document.getElementById('boot');
const voiceToggle=document.getElementById('voiceToggle');
const chatVoice=document.getElementById('chatVoice');
const status=document.getElementById('agentStatus');
let voiceEnabled=true,introDone=false;

/* =========================================================
   CINEMATIC 01 → 08 WELCOME EXPERIENCE
   ========================================================= */
if(boot){
  boot.innerHTML=`
    <div class="welcome-atmosphere"><span class="welcome-orb"></span><span class="welcome-ring ring-one"></span><span class="welcome-ring ring-two"></span><span class="welcome-particle p-one"></span><span class="welcome-particle p-two"></span><span class="welcome-particle p-three"></span></div>
    <div class="welcome-line line-one"></div><div class="welcome-line line-two"></div>
    <div class="welcome-story" aria-label="Welcome sequence">
      <div class="story-stage active" data-stage="01"><small>01</small><b>A POINT APPEARS</b><span>It all begins with a single spark.</span></div>
      <div class="story-stage" data-stage="02"><small>02</small><b>AI GREETS YOU</b><span>Hello. I've been waiting for you.</span></div>
      <div class="story-stage" data-stage="03"><small>03</small><b>DATA FORMS</b><span>Everything starts with data.</span><strong>DATA</strong></div>
      <div class="story-stage" data-stage="04"><small>04</small><b>DATA TRANSFORMS</b><span>Patterns become possibilities.</span><strong>DATA →</strong></div>
      <div class="story-stage" data-stage="05"><small>05</small><b>INTELLIGENCE EMERGES</b><span>Data becomes useful when it becomes intelligence.</span><strong>INTELLIGENCE</strong></div>
      <div class="story-stage" data-stage="06"><small>06</small><b>IDENTITY REVEALED</b><span>A passion. A purpose. An engineer.</span><strong>AWAIS</strong></div>
      <div class="story-stage" data-stage="07"><small>07</small><b>THE MISSION</b><span>I turn data into intelligence.</span><strong>BUILD · LEARN · AUTOMATE</strong></div>
      <div class="story-stage" data-stage="08"><small>08</small><b>LET'S BEGIN</b><span>Let me show you what Awais builds.</span></div>
    </div>
    <div class="welcome-copy">
      <div class="welcome-kicker"><span></span> WELCOME TO</div>
      <h1 class="welcome-name"><span>AWAIS</span><span>IRSHAD</span></h1>
      <div class="welcome-portfolio">PORTFOLIO</div>
      <p class="welcome-manifesto">I TURN DATA INTO <strong>INTELLIGENCE.</strong></p>
      <div class="welcome-actions"><button id="enter" type="button"><span>EXPLORE MY WORK</span><b>↗</b></button><button id="voiceIntro" class="voice-intro" type="button">◉ VOICE INTRO ON</button></div>
      <div class="voice-note">Awais AI will welcome you</div>
    </div>
    <div class="welcome-footer"><span>AI / ML ENGINEER</span><span>PYTHON · AI · AUTOMATION</span></div>`;

  const s=document.createElement('style');s.textContent=`
  .welcome-story{position:absolute;left:5%;right:5%;bottom:82px;height:82px;display:grid;grid-template-columns:repeat(8,1fr);border-top:1px solid rgba(121,191,232,.14);border-bottom:1px solid rgba(121,191,232,.08);z-index:3;overflow:hidden}
  .story-stage{position:relative;padding:12px 12px 8px;border-right:1px solid rgba(121,191,232,.10);opacity:.22;transform:translateY(8px);transition:opacity .6s,transform .6s,background .6s;overflow:hidden}
  .story-stage:last-child{border-right:0}.story-stage.active{opacity:1;transform:none;background:linear-gradient(180deg,rgba(121,191,232,.07),transparent)}
  .story-stage small{display:block;font:700 11px 'DM Mono';color:#d8aa68;margin-bottom:6px}.story-stage b{display:block;font:700 7px 'DM Mono';letter-spacing:.7px;color:#e9e5dd;white-space:nowrap}.story-stage span{display:block;font:7px/1.45 'Inter';color:#778187;margin-top:5px;max-width:135px}.story-stage strong{display:block;font:600 15px 'Cormorant Garamond';letter-spacing:1px;color:#79bfe8;margin-top:5px;white-space:nowrap}.story-stage[data-stage="01"]:before{content:"";position:absolute;width:5px;height:5px;border-radius:50%;left:50%;top:45%;background:#79bfe8;box-shadow:0 0 22px #79bfe8;animation:storySpark 1.8s ease-in-out infinite}.story-stage[data-stage="02"]:before{content:"◉";position:absolute;right:12px;top:10px;color:#79bfe8;font-size:16px}.story-stage[data-stage="04"] strong{color:#d8aa68}.story-stage[data-stage="06"] strong{font-size:19px;color:#f2eee6}.welcome-copy{z-index:5!important}.welcome-name span:last-child{color:#eee8dd!important}
  @keyframes storySpark{50%{transform:scale(3);opacity:.35}}
  @media(max-width:900px){.welcome-story{grid-template-columns:repeat(4,1fr);height:150px;bottom:70px}.story-stage:nth-child(n+5){display:none}.story-stage span{font-size:6px}.welcome-copy{transform:translateY(-55px)}}
  @media(max-width:600px){.welcome-story{left:16px;right:16px;grid-template-columns:repeat(2,1fr);height:145px}.story-stage{padding:8px}.story-stage:nth-child(n+5){display:block}.story-stage small{font-size:9px}.welcome-copy{transform:translateY(-65px)}.welcome-footer{bottom:14px!important}}
  `;document.head.appendChild(s);

  const stages=[...document.querySelectorAll('.story-stage')];
  let stageIndex=0;
  const advance=()=>{stages.forEach((x,i)=>x.classList.toggle('active',i===stageIndex));stageIndex=(stageIndex+1)%stages.length};
  const stageTimer=setInterval(advance,900);
  setTimeout(()=>{clearInterval(stageTimer);stages.forEach(x=>x.classList.remove('active'));stages[7]?.classList.add('active')},7200);

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
