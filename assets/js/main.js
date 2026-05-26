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
