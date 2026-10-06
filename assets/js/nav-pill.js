// Wide screens: once the reader scrolls past the top of the page the
// header row condenses into a floating pill (see lab.css .nav-compact).
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
})();
