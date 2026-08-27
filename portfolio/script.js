const boot=document.getElementById('boot');
const enter=document.getElementById('enter');
const voiceIntro=document.getElementById('voiceIntro');
const voiceToggle=document.getElementById('voiceToggle');
const chatVoice=document.getElementById('chatVoice');
const status=document.getElementById('agentStatus');
let voiceEnabled=false;let introDone=false;

/* Cinematic welcome-screen redesign */
if(boot){
  boot.innerHTML=`
    <div class="welcome-atmosphere"><span class="welcome-orb"></span><span class="welcome-ring ring-one"></span><span class="welcome-ring ring-two"></span><span class="welcome-particle p-one"></span><span class="welcome-particle p-two"></span><span class="welcome-particle p-three"></span></div>
    <div class="welcome-line line-one"></div><div class="welcome-line line-two"></div>
    <div class="welcome-copy">
      <div class="welcome-kicker"><span></span> WELCOME TO</div>
      <h1 class="welcome-name"><span>A W A I S</span><span>I R S H A D</span></h1>
      <div class="welcome-portfolio">PORTFOLIO</div>
      <p class="welcome-manifesto">I TURN DATA INTO <strong>INTELLIGENCE.</strong></p>
      <div class="welcome-actions">
        <button id="enter" type="button"><span>EXPLORE MY WORK</span><b>↗</b></button>
        <button id="voiceIntro" class="voice-intro" type="button">◉ HEAR INTRODUCTION</button>
      </div>
    </div>
    <div class="welcome-footer"><span>AI / ML ENGINEER</span><span>PYTHON · AI · AUTOMATION</span></div>`;

  const style=document.createElement('style');
  style.textContent=`
  #boot{background:#050505;color:#f4f2ec;transition:opacity 1s,visibility 1s,transform 1.15s;}
  #boot.exit{opacity:0;visibility:hidden;pointer-events:none;transform:scale(1.025)}
  .welcome-atmosphere{position:absolute;inset:0;overflow:hidden;pointer-events:none;background:radial-gradient(circle at 50% 48%,#c8ff3d0b,transparent 27%),radial-gradient(circle at 18% 78%,#c8ff3d06,transparent 28%)}
  .welcome-atmosphere:after{content:"";position:absolute;inset:0;background:radial-gradient(circle at center,transparent 25%,#050505 78%);}
  .welcome-orb{position:absolute;left:50%;top:48%;width:230px;height:230px;transform:translate(-50%,-50%);border-radius:50%;background:radial-gradient(circle,#c8ff3d1d 0%,#c8ff3d08 30%,transparent 68%);filter:blur(2px);animation:welcomePulse 4s ease-in-out infinite}
  .welcome-ring{position:absolute;left:50%;top:48%;border:1px solid #c8ff3d20;border-radius:50%;transform:translate(-50%,-50%);animation:welcomeSpin 18s linear infinite}
  .ring-one{width:min(65vw,720px);height:min(65vw,720px)}.ring-two{width:min(38vw,430px);height:min(38vw,430px);border-style:dashed;animation-duration:12s;animation-direction:reverse}
  .welcome-particle{position:absolute;width:4px;height:4px;border-radius:50%;background:#c8ff3d;box-shadow:0 0 18px #c8ff3d;opacity:.55;animation:welcomeFloat 7s ease-in-out infinite}.p-one{left:22%;top:28%}.p-two{right:19%;top:34%;animation-delay:2s}.p-three{left:70%;bottom:21%;animation-delay:4s}
  .welcome-line{position:absolute;height:1px;background:linear-gradient(90deg,transparent,#c8ff3d55,transparent);opacity:.45;animation:welcomeScan 7s ease-in-out infinite}.line-one{width:62%;left:19%;top:36%}.line-two{width:48%;left:26%;top:64%;animation-delay:2s}
  .welcome-copy{position:relative;z-index:2;width:min(1100px,92%);text-align:center;display:flex;align-items:center;flex-direction:column}
  .welcome-kicker{font:500 10px 'DM Mono';letter-spacing:6px;color:#a7aa9e;margin-bottom:26px;animation:welcomeUp .9s .1s both}.welcome-kicker span{display:inline-block;width:5px;height:5px;background:#c8ff3d;border-radius:50%;box-shadow:0 0 14px #c8ff3d;margin-right:8px}
  .welcome-name{font:700 clamp(58px,11vw,142px)/.78 'Space Grotesk';letter-spacing:-7px;margin:0;color:#f4f2ec;display:flex;flex-direction:column;animation:welcomeName 1.3s .25s cubic-bezier(.16,1,.3,1) both}.welcome-name span:last-child{color:#c8ff3d}
  .welcome-portfolio{font:500 clamp(16px,2.3vw,26px) 'DM Mono';letter-spacing:13px;margin:25px 0 28px;color:#d7d5cc;animation:welcomeUp .9s .55s both}
  .welcome-manifesto{font:500 clamp(11px,1.2vw,14px) 'DM Mono';letter-spacing:2.5px;color:#85877e;margin:0;animation:welcomeUp .9s .7s both}.welcome-manifesto strong{color:#f4f2ec;font-weight:500}
  .welcome-actions{margin-top:38px;display:flex;align-items:center;gap:20px;animation:welcomeUp .9s .85s both}.welcome-actions #enter{margin:0;border:1px solid #c8ff3d;background:#c8ff3d;color:#080a06;border-radius:999px;padding:14px 20px;font:700 9px 'DM Mono';letter-spacing:1.5px;cursor:pointer;box-shadow:0 0 35px #c8ff3d1c;transition:.3s}.welcome-actions #enter:hover{transform:translateY(-3px);box-shadow:0 0 55px #c8ff3d45}.welcome-actions #enter b{font-size:13px;margin-left:8px}.welcome-actions .voice-intro{background:none;border:0;color:#74776d;font:9px 'DM Mono';letter-spacing:1px;cursor:pointer}.welcome-actions .voice-intro:hover{color:#c8ff3d}
  .welcome-footer{position:absolute;z-index:2;left:28px;right:28px;bottom:25px;display:flex;justify-content:space-between;color:#4f534b;font:8px 'DM Mono';letter-spacing:2px}.welcome-footer span:last-child{color:#62675d}
  @keyframes welcomePulse{50%{transform:translate(-50%,-50%) scale(1.13);opacity:.65}}@keyframes welcomeSpin{to{transform:translate(-50%,-50%) rotate(360deg)}}@keyframes welcomeFloat{50%{transform:translate(18px,-22px);opacity:.9}}@keyframes welcomeScan{50%{transform:scaleX(.55);opacity:.15}}@keyframes welcomeUp{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}@keyframes welcomeName{from{opacity:0;transform:scale(.88);filter:blur(10px);letter-spacing:8px}to{opacity:1;transform:none;filter:none;letter-spacing:-7px}}
  @media(max-width:600px){.welcome-name{letter-spacing:-4px}.welcome-portfolio{letter-spacing:7px}.welcome-actions{flex-direction:column;gap:14px}.welcome-footer{left:18px;right:18px}.welcome-footer span:last-child{display:none}.ring-one{width:110vw;height:110vw}.ring-two{width:75vw;height:75vw}}
  `;
  document.head.appendChild(style);
}

const speak=(text)=>{if(!voiceEnabled||!('speechSynthesis'in window))return;window.speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(text);u.rate=.95;u.pitch=1.02;u.volume=.9;window.speechSynthesis.speak(u)};
const launch=()=>{if(introDone)return;introDone=true;boot?.classList.add('exit');document.body.classList.remove('lock');if(status)status.textContent='Welcome — explore Awais\'s work';if(voiceEnabled)speak('Welcome to Awais Irshad portfolio. I am Awais AI Agent. Let me show you what Awais builds.');setTimeout(()=>boot?.remove(),1100)};
document.getElementById('enter')?.addEventListener('click',launch);
document.getElementById('voiceIntro')?.addEventListener('click',()=>{voiceEnabled=true;const b=document.getElementById('voiceIntro');if(b){b.textContent='✓ VOICE ENABLED';b.style.color='#c8ff3d'}speak('Hi, welcome to Awais Irshad portfolio. I am Awais AI Agent, your portfolio guide. Let me show you what Awais builds.');});
voiceToggle?.addEventListener('click',()=>{voiceEnabled=!voiceEnabled;voiceToggle.textContent=voiceEnabled?'◉ VOICE ON':'◉ VOICE';voiceToggle.style.color=voiceEnabled?'#c8ff3d':'';if(!voiceEnabled)window.speechSynthesis?.cancel();else speak('Voice assistant is now on.');});
setTimeout(launch,8500);

/* Add the latest confirmed projects without touching their project folders. */
const projectGrid=document.querySelector('.project-grid');
if(projectGrid){
  const latest=[
    {no:'04',type:'RAG / GENERATIVE AI',name:'InsightDoc',desc:'RAG-based document Q&A system that lets users ask questions about PDF/TXT files and receive source-cited answers with file and page references.',tags:['Python','RAG','ChromaDB','Streamlit','OpenRouter'],url:'https://github.com/awaisirshad336012/Portfolio/tree/main/InsightDoc',featured:true},
    {no:'05',type:'WEB SCRAPING / ML',name:'E-commerce Price Intelligence',desc:'End-to-end price intelligence pipeline for product scraping, historical tracking, ML price prediction and Buy/Wait recommendations through a Streamlit dashboard.',tags:['Selenium','BeautifulSoup','Scikit-learn','SQLite','Streamlit'],url:'https://github.com/awaisirshad336012/Portfolio/tree/main/ecommerce-price-intelligence'}
  ];
  latest.forEach(p=>{const card=document.createElement('article');card.className='project'+(p.featured?' featured':'');card.innerHTML=`<div class="project-no">${p.no}</div><div class="project-type">${p.type}</div><h4>${p.name}</h4><p>${p.desc}</p><div class="tags">${p.tags.map(t=>`<span>${t}</span>`).join('')}</div><a href="${p.url}" target="_blank" rel="noreferrer">View repository <b>↗</b></a>`;projectGrid.appendChild(card)});
}

const menu=document.getElementById('menu'),nav=document.querySelector('nav');menu?.addEventListener('click',()=>{const open=nav.dataset.open==='1';nav.dataset.open=open?'0':'1';nav.style.display=open?'':'flex';if(!open)Object.assign(nav.style,{position:'absolute',top:'64px',left:'0',right:'0',padding:'20px',background:'#050705',flexDirection:'column',borderBottom:'1px solid #252b22'});});
document.querySelectorAll('nav a').forEach(a=>a.addEventListener('click',()=>{if(innerWidth<=850){nav.style.display='';nav.dataset.open='0'}}));

const responses={
 about:'Awais Irshad is an AI/ML Engineer focused on Python, machine learning, generative AI, backend development and automation. He enjoys turning real problems into useful software.',
 projects:'Awais has built LedgerIQ AI, InsightDoc, E-commerce Price Intelligence, Todo App, and Sky Briefing. InsightDoc demonstrates RAG with ChromaDB and source citations; E-commerce Price Intelligence combines web scraping, historical tracking and ML predictions.',
 tech:'His portfolio highlights Python, NumPy, Pandas, Scikit-learn, LLM applications, RAG, ChromaDB, OpenRouter, prompt engineering, Django, APIs, SQLite, Selenium, BeautifulSoup, n8n, Docker, Streamlit and GitHub.',
 contact:'You can contact Awais through WhatsApp, email or LinkedIn. WhatsApp: +92 341 2850260. Email: awaisirshad336012@gmail.com.'
};
function answer(q){const s=q.toLowerCase();if(s.includes('contact')||s.includes('whatsapp')||s.includes('email')||s.includes('linkedin'))return responses.contact;if(s.includes('project')||s.includes('build')||s.includes('work')||s.includes('insightdoc')||s.includes('price'))return responses.projects;if(s.includes('tech')||s.includes('skill')||s.includes('stack')||s.includes('use'))return responses.tech;if(s.includes('who')||s.includes('about')||s.includes('awais'))return responses.about;return 'I can tell you about Awais, his projects, technologies, or contact details. Try asking about his projects or tech stack.';}
const log=document.getElementById('chatLog'),form=document.getElementById('chatForm'),input=document.getElementById('chatInput');
function sendQuestion(q){if(!q||!log)return;const u=document.createElement('div');u.className='msg user-msg';u.textContent=q;log.appendChild(u);const a=document.createElement('div');a.className='msg agent-msg';const text=answer(q);a.textContent=text;log.appendChild(a);log.scrollTop=log.scrollHeight;speak(text);}
form?.addEventListener('submit',e=>{e.preventDefault();const q=input.value.trim();input.value='';sendQuestion(q)});
document.querySelectorAll('.quick-questions button').forEach(b=>b.addEventListener('click',()=>sendQuestion(b.dataset.question)));
chatVoice?.addEventListener('click',()=>{voiceEnabled=!voiceEnabled;chatVoice.textContent=voiceEnabled?'VOICE ON':'VOICE OFF';chatVoice.classList.toggle('off',!voiceEnabled);if(voiceEnabled)speak('Voice mode is on. Ask me anything about Awais.');else window.speechSynthesis?.cancel();});
const SpeechRecognition=window.SpeechRecognition||window.webkitSpeechRecognition;if(SpeechRecognition&&input){const mic=document.createElement('button');mic.type='button';mic.textContent='🎙';mic.title='Speak to Awais AI';mic.style.cssText='width:42px;background:#10140e;color:#c8ff3d;border:0;border-left:1px solid #242a21;cursor:pointer';form.insertBefore(mic,form.lastElementChild);const rec=new SpeechRecognition();rec.lang='en-US';rec.interimResults=false;mic.addEventListener('click',()=>{rec.start();mic.textContent='…'});rec.onresult=e=>{input.value=e.results[0][0].transcript;mic.textContent='🎙';form.requestSubmit()};rec.onerror=()=>mic.textContent='🎙';rec.onend=()=>mic.textContent='🎙'}