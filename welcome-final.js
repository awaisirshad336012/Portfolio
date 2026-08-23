(() => {
  if (document.getElementById('awais-welcome')) return;

  const scene = 'data:image/webp;base64,UklGRiYTAABXRUJQVlA4IBoTAADwjACdASoTAZQBPp1InEqlpCwpq5PZ+YATiWduvQVZVtp4bv06S6Ln2a5TfGsbPL/w4qqAbp6gw0tt3xoW2zzcbv7ghj5+hyZtGL0jX1MD6wzeHXvARsL1pmjVYA3UQZbwUpz3oEov5ZvSk/fsKPs27vfOlFmzg92wMwP3ZXPiWGi7zZcXyO66RtHG6NWfzS04Xqfhg7qhoat9cjTVjygTjIGnmCKqAQF1YlIe83J6Cfhhd9mhACtmW6NHFEu7EwktTg0pGnwDhVJ9ReY1U5NJdOGoHZi4LK7TrJNKDOOLLceXPk7GmBbnkTYX9HF64FS7g5xUPuvq3qFclvIRq1HP5EuFgp/fQelWnvACzLmltUG9djhsEkYT1abYryU/lnmCypH1zBUAfWn9xBRU4MFbPE620KYWTc7O7dwLYuHzXw1TAQ/iQLR8vm22avglL9YQkdNzbqFyYdhiBKIFBEqC7Is6h8xTn/pM/t1yUnST6MsS6APjzyrFwzetH6108ojSEBi1K9nUC0cxNEFTKTBZdPHkNcg6Y5z27Y568ZL3JVOQaBqM5+tGHJBPeLRsxkTFFfiXR3welaPoSOmVUnHtfGCjNU8h/gCbAE9LRFGcU9kw40XWdq9Uc16ja1HEcl53SOodO1bWFijPJ5sqo3p9jnbKpX7Lt+QvFeZC4Izc46TG/QObUJqSMCsJbpJq2OO431EntC1Nrh1OOQCJ0akJAEAR92hY286S9t9Pva1Dn4/rQHAMDqymI7SHEKJoPQAxIwapAsPqAgdM6QTlQRzBeNR+vAbnZu347ek+IjtB4lrO+qql3vvM/76ilfP1iGuek6OLXboXxnuYtMYQhUPLOt8yD/TRDQANqllGqxjWnpORDsK70bx/XF9sG4SLgPnIIWjWNk3vHm6a/vYxSbKt6uqB/xbMIpLVRtkIgtn+wTB4EyHPyxzkUyLhrP/i9SueFc5Afe5P6oyDwlYM+L6DMR4KQl+NKyZJx6N5IamHwUjGdY3S9D6C7LNZ29COazhxnx305qxUBTJ4svejnBSw4JCmWnlLuh2amPhhFZ4cN003UCX3LadIA/yR4KkXdjIMmVCSUhxQCdVV7i2o7vv3lEGUsL8L6ar7XMjESyJTQgr7a/weO1GFHLlzGheYjyHhdzOmZTfKVNTPgEEe1bIQtBtV+mCSOvOk9Dzb2epuNtq/FvpDiPUScZ/PacoyTP0jcLiV0vohTZY+kvk+SuzKv2EWvEwuru3d/qIezTvNOPkf2pynyVgc/s9dTHL0bVsYmNT6D9U0FWqMnSIT51iJTUMrwtxusk8jFdXpOf9WrRQXrfYEGU5DmLOT3cDtjKlmaowrM7uWb0eRLjUoFd+N/jIwk0p6SgoYXSNR9NB9z/iVXOBu465gBp1Kph2J9Ny6FfiYXbSCCt2KetFWzXR46c9J...';

  const style = document.createElement('style');
  style.textContent = `
    #awais-welcome { position: fixed; inset: 0; z-index: 99999; overflow: hidden; background: #02050b; cursor: pointer; opacity: 1; transition: opacity .9s ease, visibility .9s ease; }
    #awais-welcome.is-leaving { opacity: 0; visibility: hidden; pointer-events: none; }
    #awais-welcome .welcome-scene { position: absolute; inset: -2%; background: radial-gradient(circle at 50% 18%, rgba(51,111,190,.18), transparent 30%), url("${scene}") center center / cover no-repeat; transform: scale(1.035); opacity: 0; clip-path: inset(0 100% 0 0); animation: welcomeReveal 1.85s cubic-bezier(.7,0,.2,1) .15s forwards, welcomeSettle 2.4s ease 1.6s forwards; }
    #awais-welcome .welcome-sheen { position:absolute; inset:0; background:linear-gradient(90deg,rgba(1,4,8,.72) 0%,rgba(1,4,8,.2) 34%,rgba(1,4,8,.05) 56%,rgba(1,4,8,.3) 100%); opacity:.9; animation:sheenFade 1.4s ease 1.7s forwards; pointer-events:none; }
    #awais-welcome .welcome-status { position:absolute; left:50%; bottom:28px; transform:translateX(-50%); display:flex; align-items:center; gap:10px; letter-spacing:.34em; font:600 10px/1 "Space Grotesk",system-ui,sans-serif; color:rgba(235,245,255,.65); text-transform:uppercase; white-space:nowrap; animation:statusIn 1s ease 2.7s both; }
    #awais-welcome .welcome-status span { width:6px;height:6px;border-radius:50%;background:#3a9cff;box-shadow:0 0 16px rgba(58,156,255,.9);animation:pulseDot 1.4s ease-in-out infinite; }
    #awais-welcome .welcome-hint { position:absolute; right:28px; bottom:27px; color:rgba(235,245,255,.45); font:500 10px/1 "Space Grotesk",system-ui,sans-serif; letter-spacing:.25em; text-transform:uppercase; animation:hintIn 1s ease 3s both; }
    #awais-welcome .welcome-hit { position:absolute; left:50%; top:50%; width:min(320px,34vw); aspect-ratio:2.9/1; transform:translate(-50%,-50%); border:0; background:transparent; opacity:.02; cursor:pointer; }
    @keyframes welcomeReveal { from{opacity:0;clip-path:inset(0 100% 0 0)} to{opacity:1;clip-path:inset(0 0 0 0)} }
    @keyframes welcomeSettle { from{transform:scale(1.035) translate3d(1.5%,0,0)} to{transform:scale(1) translate3d(0,0,0)} }
    @keyframes sheenFade { from{opacity:.92} to{opacity:.56} }
    @keyframes statusIn { from{opacity:0;transform:translate(-50%,10px)} to{opacity:1;transform:translate(-50%,0)} }
    @keyframes hintIn { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:translateY(0)} }
    @keyframes pulseDot { 0%,100%{transform:scale(.75);opacity:.65} 50%{transform:scale(1.15);opacity:1} }
    @media (max-width:820px){ #awais-welcome .welcome-scene{background-position:54% center} #awais-welcome .welcome-sheen{background:linear-gradient(90deg,rgba(1,4,8,.55),rgba(1,4,8,.18))} #awais-welcome .welcome-status{bottom:18px;letter-spacing:.22em;font-size:9px} #awais-welcome .welcome-hint{right:16px;bottom:18px;font-size:8px} }
  `;
  document.head.appendChild(style);

  const root = document.createElement('div');
  root.id = 'awais-welcome';
  root.innerHTML = '<div class="welcome-scene" aria-hidden="true"></div><div class="welcome-sheen" aria-hidden="true"></div><div class="welcome-status"><span></span> Entering experience</div><div class="welcome-hint">Click anywhere to enter</div><button class="welcome-hit" type="button" aria-label="Enter Awais portfolio"></button>';
  document.body.prepend(root);
  document.body.style.overflow = 'hidden';

  let closed = false;
  const enter = () => {
    if (closed) return;
    closed = true;
    root.classList.add('is-leaving');
    window.setTimeout(() => { root.remove(); document.body.style.overflow = ''; }, 950);
  };
  root.addEventListener('click', enter);
  window.setTimeout(enter, 8500);
})();
