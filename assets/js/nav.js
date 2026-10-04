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
})();
