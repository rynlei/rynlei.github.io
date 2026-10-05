/* Lab: the menu sheet grows out of the header pill. Before the open/close
   class flips, record the pill's position so the sheet's clip-path can
   start (or end) exactly on it. Runs in the capture phase so it precedes
   site.js's own click handler. */
(function () {
  var drawer = document.getElementById('site-drawer');
  var pill = document.querySelector('.site-header-inner');
  if (!drawer || !pill) return;
  function measure() {
    var r = pill.getBoundingClientRect();
    drawer.style.setProperty('--pt', r.top + 'px');
    drawer.style.setProperty('--pl', r.left + 'px');
    drawer.style.setProperty('--pr', Math.max(0, window.innerWidth - r.right) + 'px');
    drawer.style.setProperty('--pb', Math.max(0, window.innerHeight - r.bottom) + 'px');
  }
  measure();
  document.addEventListener('click', function (e) {
    if (e.target.closest('.menu-toggle, .drawer-scrim, #site-drawer a')) measure();
  }, true);
  window.addEventListener('resize', measure);
})();
