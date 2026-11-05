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

  // works: silent preview loops while on screen; tap for the full film with sound
  var clips = [].slice.call(document.querySelectorAll('.clip'));
  var calm = (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) ||
             (navigator.connection && navigator.connection.saveData);
  var startPreview = function (v) {
    if (v.dataset.mode === 'full') return;
    if (!v.dataset.mode) { v.src = v.dataset.preview; v.dataset.mode = 'preview'; }
    var p = v.play(); if (p && p.catch) p.catch(function () {});
  };
  if (!calm && 'IntersectionObserver' in window) {
    var vio = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        var v = e.target;
        if (v.dataset.mode === 'full') return;
        if (e.isIntersecting) startPreview(v); else if (!v.paused) v.pause();
      });
    }, { threshold: 0.35 });
    clips.forEach(function (c) { var v = c.querySelector('video'); if (v && v.dataset.preview) vio.observe(v); });
  }
  clips.forEach(function (clip) {
    var v = clip.querySelector('video');
    var b = clip.querySelector('.clip-play');
    if (!v || !b) return;
    b.addEventListener('click', function () {
      clips.forEach(function (c) {
        var o = c.querySelector('video');
        if (o && o !== v && o.dataset.mode === 'full' && !o.paused) o.pause();
      });
      if (v.dataset.full && v.dataset.mode !== 'full') { v.src = v.dataset.full; v.dataset.mode = 'full'; v.loop = false; }
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
      var works = document.getElementById('works');
      var from = works ? works.offsetTop + works.offsetHeight - window.innerHeight * .6 : 560;
      var on = window.scrollY > Math.max(560, from) && !endVisible;
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

// contact: site-native form that posts to the existing Google Form
(function () {
  var f = document.getElementById('cform');
  if (!f) return;
  var done = document.getElementById('cform-done');
  var err = f.querySelector('.f-error');
  var btn = f.querySelector('.f-submit');
  var topic = document.getElementById('f-topic');
  function check() {
    var bad = [];
    [].forEach.call(f.querySelectorAll('input[required]'), function (i) {
      var ok = i.value.trim() !== '' && (i.type !== 'email' || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(i.value.trim()));
      i.setAttribute('aria-invalid', ok ? 'false' : 'true');
      if (!ok) bad.push(i);
    });
    var picked = f.querySelectorAll('input[type=checkbox]:checked').length > 0;
    topic.setAttribute('aria-invalid', picked ? 'false' : 'true');
    if (!picked) bad.push(topic.querySelector('input'));
    return bad;
  }
  f.addEventListener('input', function (e) { if (e.target.getAttribute('aria-invalid') === 'true' || topic.getAttribute('aria-invalid') === 'true') check(); });
  f.addEventListener('change', function () { if (topic.getAttribute('aria-invalid') === 'true') check(); });
  f.addEventListener('submit', function (e) {
    e.preventDefault();
    var bad = check();
    if (bad.length) {
      err.textContent = '入力されていない項目があります。赤くなっている項目をご確認ください。';
      err.hidden = false; bad[0].focus(); return;
    }
    err.hidden = true; btn.disabled = true; btn.textContent = '送信しています…';
    var data = new URLSearchParams(new FormData(f));
    fetch(f.action, { method: 'POST', mode: 'no-cors', body: data })
      .then(function () {
        f.hidden = true; done.hidden = false; done.focus();
        done.scrollIntoView({ block: 'center', behavior: 'smooth' });
        if (window.gtag) gtag('event', 'generate_lead', { form: 'contact' });
      })
      .catch(function () {
        btn.disabled = false; btn.textContent = '送信する';
        err.textContent = '送信できませんでした。通信環境をご確認のうえ、もう一度お試しいただくか、n.ryosuke@m2log.jp まで直接ご連絡ください。';
        err.hidden = false;
      });
  });
})();
