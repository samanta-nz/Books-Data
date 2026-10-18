/* LOCKED FILE — DO NOT EDIT (humans-only). Section: floater + eye-care + progress + scroll-spy */
(function(){
  'use strict';
  var d=document,root=d.documentElement;
  var fa=function(v){return String(v).replace(/[0-9]/g,function(x){return '۰۱۲۳۴۵۶۷۸۹'[+x];});};
  var store={get:function(k){try{return localStorage.getItem(k);}catch(e){return null;}},set:function(k,v){try{localStorage.setItem(k,v);}catch(e){}}};

  /* ---- eye-care (default level 2 = strong) ---- */
  var KEY='lesson-eye-level';
  function setEye(l){
    root.setAttribute('data-eye',l);store.set(KEY,l);
    d.querySelectorAll('[data-eye-set]').forEach(function(b){b.setAttribute('aria-pressed',String(b.getAttribute('data-eye-set')===String(l)));});
  }
  var saved=store.get(KEY);setEye(/^[0-3]$/.test(saved||'')?saved:'2');
  d.querySelectorAll('[data-eye-set]').forEach(function(b){b.addEventListener('click',function(){setEye(b.getAttribute('data-eye-set'));});});

  /* ---- floater open/close ---- */
  var wrap=d.getElementById('fab'),btn=d.getElementById('fab-btn'),panel=d.getElementById('fab-panel');
  function open(v){wrap.classList.toggle('open',v);btn.setAttribute('aria-expanded',String(v));btn.setAttribute('aria-label',v?'بستن فهرست':'باز کردن فهرست و ابزارها');}
  btn.addEventListener('click',function(e){e.stopPropagation();open(!wrap.classList.contains('open'));});
  d.addEventListener('click',function(e){if(wrap.classList.contains('open')&&!wrap.contains(e.target))open(false);});
  d.addEventListener('keydown',function(e){if(e.key==='Escape'&&wrap.classList.contains('open')){open(false);btn.focus();}});
  panel.querySelectorAll('.fab-toc a').forEach(function(a){a.addEventListener('click',function(){open(false);});});
  var top=d.getElementById('go-top');
  if(top)top.addEventListener('click',function(){window.scrollTo({top:0,behavior:'smooth'});open(false);});

  /* ---- progress ring + percent + scroll-spy ---- */
  var links=[].slice.call(d.querySelectorAll('.fab-toc a')),pct=d.getElementById('fab-pct');
  var targets=links.map(function(a){return d.querySelector(a.getAttribute('href'));});
  var tick=false;
  function update(){
    tick=false;
    var h=root.scrollHeight-window.innerHeight,p=h>0?Math.min(100,Math.max(0,Math.round(window.scrollY/h*100))):0;
    wrap.style.setProperty('--p',p);if(pct)pct.textContent=fa(p)+'٪';
    var cur=-1,line=window.innerHeight*0.35;
    targets.forEach(function(t,i){if(t&&t.getBoundingClientRect().top<=line)cur=i;});
    links.forEach(function(a,i){if(i===cur)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current');});
  }
  window.addEventListener('scroll',function(){if(!tick){tick=true;requestAnimationFrame(update);}},{passive:true});
  window.addEventListener('resize',update);update();
})();
