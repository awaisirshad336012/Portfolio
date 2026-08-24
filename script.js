const btn=document.getElementById("enterBtn");
btn?.addEventListener("click",()=>document.getElementById("home").scrollIntoView({behavior:"smooth"}));
const observer=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting)e.target.classList.add("reveal")}),{threshold:.08});
document.querySelectorAll("section,.project-grid article,.reason-grid div").forEach(x=>observer.observe(x));
document.querySelectorAll(".nav nav a").forEach(a=>a.addEventListener("click",()=>document.querySelector(".nav .active")?.classList.remove("active")));
