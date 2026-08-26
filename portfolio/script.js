const revealItems=document.querySelectorAll('.reveal');
const observer=new IntersectionObserver((entries)=>{entries.forEach((entry)=>{if(entry.isIntersecting){entry.target.classList.add('visible');observer.unobserve(entry.target)}})},{threshold:.08});
revealItems.forEach((item)=>observer.observe(item));
