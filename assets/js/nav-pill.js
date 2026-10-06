// Wide screens: once the reader scrolls past the top of the page the
// header row condenses into a floating pill (see lab.css .nav-compact).
// Also drives the "More" menu for tap and keyboard; hover is CSS.
(function () {
  var root = document.documentElement;
  var ticking = false;
  function update() {
    ticking = false;
    root.classList.toggle('nav-compact', window.scrollY > 48);
  }
  function onScroll() { if (!ticking) { ticking = true; window.requestAnimationFrame(update); } }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  update();

  var more = document.querySelector('.site-nav-more');
  var btn = more && more.querySelector('.site-nav-more-btn');
  if (!btn) return;
  function setOpen(open) {
    more.classList.toggle('is-open', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  }
  btn.addEventListener('click', function (e) { e.stopPropagation(); setOpen(!more.classList.contains('is-open')); });
  more.addEventListener('click', function (e) { if (e.target.closest('.site-nav-panel a')) setOpen(false); });
  document.addEventListener('click', function (e) { if (!more.contains(e.target)) setOpen(false); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && more.classList.contains('is-open')) { setOpen(false); btn.focus(); }
  });
})();
