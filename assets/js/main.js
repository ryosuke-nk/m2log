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
  } else if(slides.length === 1){
    slides[0].classList.add('active');
  }

  /* ── AUTO SCENE SCROLL ── */
  var sceneWrap = document.querySelector('[data-scene-scroll]');
  if(sceneWrap){
    var speed = 0.6;
    var pos = 0;
    var paused = false;
    var maxScroll = 0;

    // ロード後に正確なscrollWidthを取得
    function initScroll(){
      maxScroll = sceneWrap.scrollWidth - sceneWrap.clientWidth;
    }
    window.addEventListener('load', initScroll);
    setTimeout(initScroll, 500); // フォールバック

    sceneWrap.addEventListener('mouseenter', function(){ paused = true; }, {passive: true});
    sceneWrap.addEventListener('mouseleave', function(){ paused = false; }, {passive: true});
    sceneWrap.addEventListener('touchstart', function(){ paused = !paused; }, {passive: true});

    (function scroll(){
      if(!paused && maxScroll > 0){
        pos += speed;
        if(pos >= maxScroll) pos = 0;
        sceneWrap.scrollLeft = pos;
      }
      requestAnimationFrame(scroll);
    })();
  }

})();


// ── 計測: 主要アクションのGA4イベント ──
(function(){
  function track(name, params){
    if (typeof gtag === 'function') gtag('event', name, params || {});
  }
  document.addEventListener('click', function(e){
    var a = e.target.closest('a, button');
    if(!a) return;
    var txt = (a.textContent || '').trim().slice(0, 30);
    if (a.classList.contains('btn-p') || a.classList.contains('nav-cta')) {
      track('cta_click', { cta_text: txt, page: location.pathname });
    } else if (a.classList.contains('next-rail')) {
      track('next_rail_click', { to: a.getAttribute('href') });
    } else if (a.closest('.page-anchor')) {
      track('plans_anchor_click', { label: txt });
    } else if (a.classList.contains('stance-photo')) {
      track('about_photo_click', {});
    } else if ((a.getAttribute('href') || '').indexOf('mailto:') === 0) {
      track('email_click', {});
    } else if ((a.getAttribute('href') || '').indexOf('instagram.com') !== -1) {
      track('instagram_click', { page: location.pathname });
    }
  }, { passive: true });

  // Works動画: 初回再生・シーク・音声ON + 排他再生
  var vids = document.querySelectorAll('.work-video');
  vids.forEach(function(v){
    var card = v.closest('.work-card');
    var title = card ? (card.querySelector('.work-cap-jp') || {}).textContent : '';
    var played = false;
    v.addEventListener('play', function(){
      if(!played){ played = true; track('works_play', { title: title }); }
      vids.forEach(function(o){ if(o !== v && !o.paused) o.pause(); });
    });
    var seeked = false;
    var seek = card && card.querySelector('.work-seek');
    if(seek) seek.addEventListener('pointerdown', function(){
      if(!seeked){ seeked = true; track('works_seek', { title: title }); }
    });
    var unmuted = false;
    var btn = card && card.querySelector('.work-sound');
    if(btn) btn.addEventListener('click', function(){
      setTimeout(function(){
        if(!unmuted && v.muted === false){ unmuted = true; track('works_unmute', { title: title }); }
      }, 0);
    });
  });
})();
