const voiceToggle=document.getElementById('voiceToggle');
const chatVoice=document.getElementById('chatVoice');
const status=document.getElementById('agentStatus');
let voiceEnabled=true;
let introDone=false;

/* =========================================================
   VOICE GUIDE — used by the cinematic welcome and assistant
   ========================================================= */
const pickVoice=()=>{
  if(!('speechSynthesis' in window)) return null;
  const voices=window.speechSynthesis.getVoices();
  return voices.find(v=>/en-US/i.test(v.lang)&&/Microsoft|Google|Samantha|Daniel|Natural/i.test(v.name))
    || voices.find(v=>/^en-US/i.test(v.lang))
    || voices.find(v=>/^en/i.test(v.lang))
    || voices[0] || null;
};
const speak=(text)=>{
  if(!voiceEnabled||!('speechSynthesis' in window)) return false;
  window.speechSynthesis.cancel();
  const u=new SpeechSynthesisUtterance(text),v=pickVoice();
  if(v) u.voice=v;
  u.rate=.92; u.pitch=.98; u.volume=1;
  window.speechSynthesis.speak(u);
  return true;
};
const introText='Welcome to Awais Irshad portfolio. I am Awais AI, your personal portfolio guide. Awais is an AI and machine learning engineer focused on Python, generative AI, intelligent automation, and practical AI applications. Let me introduce you to his work.';
window.speechSynthesis?.addEventListener('voiceschanged',()=>pickVoice());

voiceToggle?.addEventListener('click',()=>{
  voiceEnabled=!voiceEnabled;
  voiceToggle.textContent=voiceEnabled?'◉ VOICE ON':'◉ VOICE';
  voiceToggle.style.color=voiceEnabled?'#d8aa68':'';
  if(!voiceEnabled) window.speechSynthesis?.cancel();
  else speak('Voice assistant is now on.');
});

/* =========================================================
   Latest projects — presentation only; project folders remain untouched.
   ========================================================= */
const projectGrid=document.querySelector('.project-grid');
if(projectGrid){
  const latest=[
    {no:'04',type:'RAG / GENERATIVE AI',name:'InsightDoc',desc:'RAG-based document Q&A system for PDF/TXT files with source and page citations.',tags:['Python','RAG','ChromaDB','Streamlit','OpenRouter'],url:'https://github.com/awaisirshad336012/Portfolio/tree/main/InsightDoc',featured:true},
    {no:'05',type:'WEB SCRAPING / ML',name:'E-commerce Price Intelligence',desc:'Product scraping, historical price tracking, ML price prediction and Buy/Wait recommendations.',tags:['Selenium','BeautifulSoup','Scikit-learn','SQLite','Streamlit'],url:'https://github.com/awaisirshad336012/Portfolio/tree/main/ecommerce-price-intelligence'}
  ];
  latest.forEach(p=>{
    const card=document.createElement('article');
    card.className='project'+(p.featured?' featured':'');
    card.innerHTML=`<div class="project-no">${p.no}</div><div class="project-type">${p.type}</div><h4>${p.name}</h4><p>${p.desc}</p><div class="tags">${p.tags.map(t=>`<span>${t}</span>`).join('')}</div><a href="${p.url}" target="_blank" rel="noreferrer">View repository <b>↗</b></a>`;
    projectGrid.appendChild(card);
  });
}

/* Mobile menu */
const menu=document.getElementById('menu'),nav=document.querySelector('nav');
menu?.addEventListener('click',()=>{
  const open=nav.dataset.open==='1';
  nav.dataset.open=open?'0':'1';
  nav.style.display=open?'':'flex';
  if(!open) Object.assign(nav.style,{position:'absolute',top:'64px',left:'0',right:'0',padding:'20px',background:'#050607',flexDirection:'column',borderBottom:'1px solid rgba(216,170,104,.2)'});
});
document.querySelectorAll('nav a').forEach(a=>a.addEventListener('click',()=>{
  if(innerWidth<=850){nav.style.display='';nav.dataset.open='0';}
}));

/* =========================================================
   Portfolio assistant
   ========================================================= */
const responses={
  about:'Awais Irshad is an AI/ML Engineer focused on Python, machine learning, generative AI, backend development and automation.',
  projects:'Awais has built LedgerIQ AI, InsightDoc, E-commerce Price Intelligence, Todo App and Sky Briefing.',
  tech:'His stack includes Python, NumPy, Pandas, Scikit-learn, LLM applications, RAG, ChromaDB, OpenRouter, Django, APIs, SQLite, Selenium, BeautifulSoup, n8n, Docker, Streamlit and GitHub.',
  contact:'You can contact Awais through WhatsApp at +92 341 2850260, email at awaisirshad336012@gmail.com, or LinkedIn.'
};
function answer(q){
  const s=q.toLowerCase();
  if(/contact|whatsapp|email|linkedin/.test(s)) return responses.contact;
  if(/project|build|work|insightdoc|price/.test(s)) return responses.projects;
  if(/tech|skill|stack|use/.test(s)) return responses.tech;
  if(/who|about|awais/.test(s)) return responses.about;
  return 'I can tell you about Awais, his projects, technologies, or contact details.';
}
const log=document.getElementById('chatLog'),form=document.getElementById('chatForm'),input=document.getElementById('chatInput');
function sendQuestion(q){
  if(!q||!log)return;
  const u=document.createElement('div');u.className='msg user-msg';u.textContent=q;log.appendChild(u);
  const a=document.createElement('div');a.className='msg agent-msg';const text=answer(q);a.textContent=text;log.appendChild(a);
  log.scrollTop=log.scrollHeight;speak(text);
}
form?.addEventListener('submit',e=>{e.preventDefault();const q=input.value.trim();input.value='';sendQuestion(q);});
document.querySelectorAll('.quick-questions button').forEach(b=>b.addEventListener('click',()=>sendQuestion(b.dataset.question)));
chatVoice?.addEventListener('click',()=>{
  voiceEnabled=!voiceEnabled;
  chatVoice.textContent=voiceEnabled?'VOICE ON':'VOICE OFF';
  if(voiceEnabled)speak('Voice mode is on. Ask me anything about Awais.');
  else window.speechSynthesis?.cancel();
});

/* Browser speech input */
const SpeechRecognition=window.SpeechRecognition||window.webkitSpeechRecognition;
if(SpeechRecognition&&input){
  const mic=document.createElement('button');
  mic.type='button';mic.textContent='🎙';mic.title='Speak to Awais AI';
  mic.style.cssText='width:42px;background:#080b0d;color:#d8aa68;border:0;border-left:1px solid rgba(121,191,232,.14);cursor:pointer';
  form.insertBefore(mic,form.lastElementChild);
  const rec=new SpeechRecognition();rec.lang='en-US';rec.interimResults=false;
  mic.onclick=()=>{rec.start();mic.textContent='…';};
  rec.onresult=e=>{input.value=e.results[0][0].transcript;mic.textContent='🎙';form.requestSubmit();};
  rec.onerror=()=>mic.textContent='🎙';rec.onend=()=>mic.textContent='🎙';
}

/* Keep status available for the AI welcome */
if(status) status.textContent='Awais AI ready';