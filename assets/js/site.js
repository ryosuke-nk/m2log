(function () {
  // header: border once scrolled, mobile menu
  var hd = document.querySelector('.hd');
  if (hd) {
    var onScroll = function () { hd.classList.toggle('is-scrolled', window.scrollY > 8); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    var btn = hd.querySelector('.hd-menu');
    var nav = hd.querySelector('.hd-nav');
    if (btn && nav) {
      btn.addEventListener('click', function () {
        var open = btn.getAttribute('aria-expanded') !== 'true';
        btn.setAttribute('aria-expanded', open);
        btn.setAttribute('aria-label', open ? 'メニューを閉じる' : 'メニューを開く');
        nav.classList.toggle('is-open', open);
      });
      nav.addEventListener('click', function (e) {
        if (e.target.closest('a')) { btn.setAttribute('aria-expanded', 'false'); nav.classList.remove('is-open'); }
      });
    }
  }

  // works: tap to play with sound and controls; only one clip plays at a time
  var clips = [].slice.call(document.querySelectorAll('.clip'));
  clips.forEach(function (clip) {
    var v = clip.querySelector('video');
    var b = clip.querySelector('.clip-play');
    if (!v || !b) return;
    b.addEventListener('click', function () {
      clips.forEach(function (c) {
        var o = c.querySelector('video');
        if (o && o !== v && !o.paused) o.pause();
      });
      v.controls = true;
      v.muted = false;
      clip.classList.add('is-playing');
      var p = v.play();
      if (p && p.catch) p.catch(function () { v.muted = true; v.play(); });
    });
  });

  // mobile: consult bar appears after the hero, steps aside near the closing CTA and on the contact page
  var bar = document.querySelector('.mcta');
  if (bar && !/\/contact(\.html)?$/.test(location.pathname)) {
    document.body.classList.add('has-mcta');
    var ends = [].slice.call(document.querySelectorAll('.cta, .ft'));
    var seen = new Set();
    var endVisible = false;
    if (ends.length && 'IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) seen.add(e.target); else seen.delete(e.target); });
        endVisible = seen.size > 0; update();
      });
      ends.forEach(function (el) { io.observe(el); });
    }
    var update = function () {
      var on = window.scrollY > 560 && !endVisible;
      bar.classList.toggle('is-on', on);
      bar.setAttribute('aria-hidden', on ? 'false' : 'true');
      var a = bar.querySelector('a'); if (a) a.tabIndex = on ? 0 : -1;
    };
    window.addEventListener('scroll', update, { passive: true });
    update();
  } else if (bar) { bar.remove(); }

  // plans: A/B switcher for the swipeable cards on phones
  var grid = document.querySelector('.plan-grid');
  var sw = [].slice.call(document.querySelectorAll('.plan-switch button'));
  if (grid && sw.length) {
    var cards = [].slice.call(grid.querySelectorAll('.plan'));
    sw.forEach(function (b) {
      b.addEventListener('click', function () {
        var c = cards[+b.dataset.plan]; if (!c) return;
        grid.scrollTo({ left: c.offsetLeft - grid.offsetLeft - parseFloat(getComputedStyle(grid).paddingLeft || 0), behavior: 'smooth' });
        var top = grid.getBoundingClientRect().top + window.scrollY - 150;
        if (window.scrollY > top) window.scrollTo({ top: top, behavior: 'smooth' });
      });
    });
    grid.addEventListener('scroll', function () {
      var i = grid.scrollLeft > (cards[1] ? cards[1].offsetLeft - grid.offsetLeft : 9e9) / 2 ? 1 : 0;
      sw.forEach(function (b, k) { b.setAttribute('aria-pressed', k === i); });
    }, { passive: true });
  }
})();
