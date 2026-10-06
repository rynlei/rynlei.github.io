// Wide screens: once the reader scrolls past the top of the page the
// header row condenses into a floating pill (see lab.css .nav-compact).
// Also drives the "More" menu, as a small panel or a full-width sheet.
(function () {
  var root = document.documentElement;
  var ticking = false, compact = false;
  // Section highlighting: the row link (or "More") for the section the
  // reader is in carries .is-current. Styled per page in CSS.
  var navLinks = Array.prototype.slice.call(document.querySelectorAll('.site-nav a[href^="#"]'));
  var moreBtn = document.querySelector('.site-nav-more-btn');
  var moreIds = Array.prototype.map.call(document.querySelectorAll('.mega a[href^="#"], .site-nav-panel a[href^="#"]'), function (a) { return a.getAttribute('href').slice(1); });
  var sections = navLinks.map(function (a) { return a.getAttribute('href').slice(1); }).concat(moreIds)
    .map(function (id) { return document.getElementById(id); }).filter(Boolean)
    .sort(function (p, q) { return p.offsetTop - q.offsetTop; });
  var currentId = null;
  function highlight() {
    if (!sections.length) return;
    var line = window.scrollY + Math.min(window.innerHeight * 0.33, 240);
    var cur = null;
    for (var i = 0; i < sections.length; i++) { if (sections[i].offsetTop <= line) cur = sections[i]; }
    var id = cur ? cur.id : null;
    if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 2) id = sections[sections.length - 1].id;
    if (id === currentId) return;
    currentId = id;
    navLinks.forEach(function (a) { a.classList.toggle('is-current', a.getAttribute('href') === '#' + id); });
    if (moreBtn) moreBtn.classList.toggle('is-current', moreIds.indexOf(id) >= 0);
  }
  // Hysteresis: condense once the reader is clearly past the top, and only
  // widen again close to it, so the header never flickers near the line.
  function update() {
    ticking = false;
    var y = window.scrollY;
    if (!compact && y > 96) compact = true;
    else if (compact && y < 12) compact = false;
    root.classList.toggle('nav-compact', compact);
    highlight();
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
    btn.addEventListener('mouseenter', function () { if (!wide()) return; clearTimeout(hoverTimer); hoverTimer = setTimeout(function () { setOpen(true); }, 320); });  // the pointer has to rest on More, not just cross it
    btn.addEventListener('mouseleave', function () { clearTimeout(hoverTimer); });
    [header, mega].forEach(function (el) {
      el.addEventListener('mouseleave', function () { if (isOpen()) armClose(); });
      el.addEventListener('mouseenter', cancelClose);
    });
    if (scrim) scrim.addEventListener('mouseenter', function () { if (isOpen()) armClose(); });
    document.addEventListener('scroll', function () { if (isOpen() && mega) setOpen(false); }, { passive: true });
  }
})();
