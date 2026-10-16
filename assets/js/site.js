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
})();
