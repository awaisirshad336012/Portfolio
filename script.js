const observer = new IntersectionObserver((entries) => { entries.forEach(entry => { if (entry.isIntersecting) entry.target.classList.add('visible'); }); }, { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

const menu = document.querySelector('.menu-btn');
const links = document.querySelector('.nav-links');
menu?.addEventListener('click', () => {
  const open = links.dataset.open === 'true';
  links.dataset.open = String(!open);
  links.style.display = open ? '' : 'flex';
  if (!open) {
    links.style.position = 'absolute'; links.style.top = '76px'; links.style.left = '0'; links.style.right = '0';
    links.style.padding = '22px'; links.style.background = 'rgba(7,9,13,.96)'; links.style.borderBottom = '1px solid #1b2330';
    links.style.flexDirection = 'column'; links.style.gap = '18px';
  }
});

document.querySelectorAll('a[href^="#"]').forEach(a => a.addEventListener('click', () => {
  if (window.innerWidth <= 850 && links) { links.style.display = ''; links.dataset.open = 'false'; }
}));
