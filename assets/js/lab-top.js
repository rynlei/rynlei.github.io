// Lab only: a floating back-to-top control that appears once the reader
// has scrolled past the opening screen and returns them to the top.
(function () {
  var btn = document.querySelector('.to-top');
  if (!btn) return;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  var ticking = false;
  function update() {
    ticking = false;
    btn.classList.toggle('is-visible', window.scrollY > window.innerHeight * 0.9);
  }
  function onScroll() {
    if (!ticking) { ticking = true; window.requestAnimationFrame(update); }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  btn.addEventListener('click', function (e) {
    e.preventDefault();
    window.scrollTo({ top: 0, behavior: reduce.matches ? 'auto' : 'smooth' });
    btn.blur();
    if (history.replaceState) history.replaceState(null, '', location.pathname + location.search);
  });
  update();
})();
