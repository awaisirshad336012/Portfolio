const observer = new IntersectionObserver((entries) => { entries.forEach(entry => { if (entry.isIntersecting) entry.target.classList.add('visible'); }); }, { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
const menu = document.querySelector('.menu-btn');
const links = document.querySelector('.nav-links');
menu?.addEventListener('click', () => { const open = links.dataset.open === 'true'; links.dataset.open = String(!open); links.style.display = open ? '' : 'flex'; if (!open) Object.assign(links.style, {position:'absolute',top:'76px',left:'0',right:'0',padding:'22px',background:'rgba(7,9,13,.96)',borderBottom:'1px solid #1b2330',flexDirection:'column',gap:'18px'}); });
document.querySelectorAll('a[href^="#"]').forEach(a => a.addEventListener('click', () => { if (window.innerWidth <= 850 && links) { links.style.display = ''; links.dataset.open = 'false'; } }));
setTimeout(() => { const s = document.createElement('script'); s.src = 'portfolio-enhance.js?v=2'; document.body.appendChild(s); }, 700);
