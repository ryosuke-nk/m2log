(function(){

  /* ── NAV ── */
  var nav = document.getElementById('nav');
  var isTop = !window.location.pathname.includes('/pages/');

  if(nav){
    if(isTop){
      nav.classList.add('dark-nav');
      window.addEventListener('scroll', function(){
        nav.classList.toggle('dark-nav', window.scrollY < window.innerHeight * 0.85);
      }, {passive: true});
    }
    var ham = document.getElementById('navHam');
    var mob = document.getElementById('navMobile');
    if(ham && mob){
      ham.addEventListener('click', function(e){
        e.stopPropagation();
        mob.classList.toggle('open');
      });
      document.addEventListener('click', function(e){
        if(!nav.contains(e.target)) mob.classList.remove('open');
      });
    }
  }

  /* ── SCROLL REVEAL ── */
  var reveals = document.querySelectorAll('.reveal');
  if(reveals.length){
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if(e.isIntersecting){ e.target.classList.add('visible'); io.unobserve(e.target); }
      });
    }, { threshold: 0.08 });
    reveals.forEach(function(el){ io.observe(el); });
  }

  /* ── CUSTOM CURSOR ── */
  var cursor = document.createElement('div');
  cursor.id = 'custom-cursor';
  cursor.style.cssText = 'position:fixed;width:10px;height:10px;background:#F47920;border-radius:50%;pointer-events:none;z-index:9999;transform:translate(-50%,-50%);transition:width 0.2s ease,height 0.2s ease,background 0.2s ease;opacity:0;will-change:transform';
  document.body.appendChild(cursor);

  var cx = 0, cy = 0, tx = 0, ty = 0, visible = false;
  document.addEventListener('mousemove', function(e){
    tx = e.clientX; ty = e.clientY;
    if(!visible){ cursor.style.opacity = '1'; visible = true; }
  }, {passive: true});
  document.addEventListener('mouseleave', function(){ cursor.style.opacity = '0'; visible = false; });

  document.addEventListener('mouseover', function(e){
    if(e.target.closest('a,button')){
      cursor.style.width = '32px'; cursor.style.height = '32px';
      cursor.style.background = 'rgba(244,121,32,0.3)';
    }
  });
  document.addEventListener('mouseout', function(e){
    if(e.target.closest('a,button')){
      cursor.style.width = '10px'; cursor.style.height = '10px';
      cursor.style.background = '#F47920';
    }
  });

  (function animCursor(){
    cx += (tx - cx) * 0.15;
    cy += (ty - cy) * 0.15;
    cursor.style.left = cx + 'px';
    cursor.style.top  = cy + 'px';
    requestAnimationFrame(animCursor);
  })();

  /* ── HERO SLIDESHOW ── */
  var slides = document.querySelectorAll('.hero-slide');
  if(slides.length > 1){
    var cur = 0;
    slides[0].classList.add('active');
    setInterval(function(){
      slides[cur].classList.remove('active');
      cur = (cur + 1) % slides.length;
      slides[cur].classList.add('active');
    }, 4500);
  }

  /* ── AUTO SCENE SCROLL ── */
  var origTrack = document.querySelector('.scene-scroll-track');
  if(origTrack){
    var wrap = origTrack.parentElement;
    // クローンを1つだけ追加してシームレスループ
    var clone = origTrack.cloneNode(true);
    wrap.appendChild(clone);

    var speed = 0.55;
    var pos = 0;
    var paused = false;

    wrap.addEventListener('mouseenter', function(){ paused = true; }, {passive: true});
    wrap.addEventListener('mouseleave', function(){ paused = false; }, {passive: true});
    wrap.addEventListener('touchstart', function(){ paused = !paused; }, {passive: true});

    (function scroll(){
      if(!paused){
        pos += speed;
        // 元のトラック幅 + gap を超えたらリセット
        var trackW = origTrack.offsetWidth + 16;
        if(pos >= trackW) pos = 0;
        wrap.scrollLeft = pos;
      }
      requestAnimationFrame(scroll);
    })();
  }

})();
