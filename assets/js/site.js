/* Site behaviour: hamburger drawer navigation and scroll reveal. */
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
    var a = e.target.closest('a');
    if (!a) return;
    // Same-page section links: close the menu first, then scroll once the
    // page's scroll lock has lifted. Letting the browser jump in the same
    // instant as the close loses the jump on iOS Safari now and then.
    var hash = a.getAttribute('href') || '';
    var target = hash.charAt(0) === '#' && hash.length > 1 ? document.getElementById(hash.slice(1)) : null;
    setOpen(false);
    if (!target) return;
    e.preventDefault();
    setTimeout(function () {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      if (history.pushState) history.pushState(null, '', hash);
    }, 60);
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

/* Scroll reveal. Blocks get .reveal, grouped items inside them get
   .reveal-child with a small stagger. Once a block has finished
   animating its reveal classes are removed so hover effects and
   layout behave exactly as they would without the animation. */
(function () {
  var root = document.documentElement;
  // Project and publication cards reveal on their own as each one enters
  // the view; smaller items reveal with their section, staggered.
  var BLOCKS = '.hero, .section, .project-card, .project-hero, .colophon, .project-figure';
  var ITEMS = '.highlight-item, .news-item, #skills .interests-list li, .index-row';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var blocks = Array.prototype.slice.call(document.querySelectorAll(BLOCKS));
  if (!blocks.length || !root.classList.contains('js')) return;
  if (reduce || !('IntersectionObserver' in window)) { root.classList.add('reveal-all'); return; }
  window.__revealReady = true;

  blocks.forEach(function (b) {
    b.classList.add('reveal');
    Array.prototype.forEach.call(b.querySelectorAll(ITEMS), function (el, i) {
      el.classList.add('reveal-child');
      el.style.transitionDelay = Math.min(i, 8) * 120 + 'ms';
    });
  });

  function settle(b) {
    b.classList.remove('reveal', 'is-visible');
    b.style.transitionDelay = '';
    Array.prototype.forEach.call(b.querySelectorAll('.reveal-child'), function (el) {
      el.classList.remove('reveal-child');
      el.style.transitionDelay = '';
    });
  }

  var pending = blocks.slice();

  function show(b, instant, delay) {
    pending.splice(pending.indexOf(b), 1);
    io.unobserve(b);
    if (instant) { settle(b); return; }
    b.style.transitionDelay = delay ? delay + 'ms' : '';
    b.classList.add('is-visible');
    setTimeout(function () { settle(b); }, 3000);
  }

  var io = new IntersectionObserver(function (entries) {
    // Blocks that enter together (a section and its first card, or two
    // cards side by side) arrive top to bottom with a short stagger.
    var incoming = [];
    entries.forEach(function (e) {
      if (pending.indexOf(e.target) < 0) return;
      if (e.isIntersecting) incoming.push(e);
      else if (e.boundingClientRect.bottom < 0) show(e.target, true);
    });
    incoming.sort(function (a, b) { return a.boundingClientRect.top - b.boundingClientRect.top; });
    incoming.forEach(function (e, i) { show(e.target, false, Math.min(i, 8) * 120); });
  }, { rootMargin: '0px 0px -12% 0px', threshold: 0 });

  blocks.forEach(function (b) { io.observe(b); });

  // A jump (anchor link, hash on load, fast fling) can carry a block from
  // below the view to above it without it ever intersecting. Anything that
  // ends up above the view is shown at once, so nothing is left blank.
  window.addEventListener('scroll', function () {
    if (!pending.length) return;
    pending.slice().forEach(function (b) {
      if (b.getBoundingClientRect().bottom < 0) show(b, true);
    });
  }, { passive: true });
})();
