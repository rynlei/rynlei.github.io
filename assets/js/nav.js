/* Hamburger drawer navigation. */
(function () {
  var root = document.documentElement;
  var btn = document.querySelector('.menu-toggle');
  var drawer = document.getElementById('site-drawer');
  var scrim = document.querySelector('.drawer-scrim');
  if (!btn || !drawer || !scrim) return;

  function setOpen(open) {
    root.classList.toggle('menu-open', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    drawer.setAttribute('aria-hidden', open ? 'false' : 'true');
  }

  btn.addEventListener('click', function () {
    setOpen(!root.classList.contains('menu-open'));
  });
  scrim.addEventListener('click', function () { setOpen(false); });
  drawer.addEventListener('click', function (e) {
    if (e.target.closest('a')) setOpen(false);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && root.classList.contains('menu-open')) {
      setOpen(false);
      btn.focus();
    }
  });
  window.addEventListener('resize', function () {
    if (root.classList.contains('menu-open') && getComputedStyle(btn).display === 'none') {
      setOpen(false);
    }
  });

  // Swipe: a leftward swipe on the open menu closes it; a rightward swipe
  // starting near the left edge opens it. Only horizontal swipes count.
  var startX = 0, startY = 0, tracking = false, fromEdge = false;
  document.addEventListener('touchstart', function (e) {
    tracking = e.touches.length === 1 && getComputedStyle(btn).display !== 'none';
    if (!tracking) return;
    startX = e.touches[0].clientX;
    startY = e.touches[0].clientY;
    fromEdge = startX <= 48;
  }, { passive: true });
  document.addEventListener('touchend', function (e) {
    if (!tracking) return;
    tracking = false;
    var dx = e.changedTouches[0].clientX - startX;
    var dy = e.changedTouches[0].clientY - startY;
    if (Math.abs(dx) < 60 || Math.abs(dx) < Math.abs(dy) * 1.5) return;
    var open = root.classList.contains('menu-open');
    if (open && dx < 0) setOpen(false);
    else if (!open && dx > 0 && fromEdge) setOpen(true);
  }, { passive: true });
})();
