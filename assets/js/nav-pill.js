// Wide screens: once the reader scrolls past the top of the page the
// header row condenses into a floating pill (see lab.css .nav-compact).
// Also drives the "More" menu, as a small panel or a full-width sheet.
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
  var mega = document.getElementById('site-mega');
  var scrim = document.querySelector('.mega-scrim');
  var hoverTimer = 0;
  function isOpen() { return mega ? root.classList.contains('more-open') : more.classList.contains('is-open'); }
  function setOpen(open) {
    if (mega) { root.classList.toggle('more-open', open); mega.setAttribute('aria-hidden', open ? 'false' : 'true'); }
    else more.classList.toggle('is-open', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  }
  function wide() { return getComputedStyle(btn).display !== 'none'; }

  btn.addEventListener('click', function (e) { e.stopPropagation(); setOpen(!isOpen()); });
  document.addEventListener('click', function (e) {
    if (!isOpen()) return;
    if (more.contains(e.target) || (mega && mega.contains(e.target))) { if (e.target.closest('a')) setOpen(false); return; }
    setOpen(false);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && isOpen()) { setOpen(false); btn.focus(); }
  });

  // Hover for the sheet: open when the pointer rests on "More", close
  // when it leaves both the header and the sheet.
  if (mega) {
    var header = document.querySelector('.site-header');
    function armClose() { clearTimeout(hoverTimer); hoverTimer = setTimeout(function () { setOpen(false); }, 180); }
    function cancelClose() { clearTimeout(hoverTimer); }
    btn.addEventListener('mouseenter', function () { if (!wide()) return; clearTimeout(hoverTimer); hoverTimer = setTimeout(function () { setOpen(true); }, 120); });
    btn.addEventListener('mouseleave', function () { clearTimeout(hoverTimer); });
    [header, mega].forEach(function (el) {
      el.addEventListener('mouseleave', function () { if (isOpen()) armClose(); });
      el.addEventListener('mouseenter', cancelClose);
    });
    if (scrim) scrim.addEventListener('mouseenter', function () { if (isOpen()) armClose(); });
    document.addEventListener('scroll', function () { if (isOpen() && mega) setOpen(false); }, { passive: true });
  }
})();
