// Lab only: load the Figma prototype viewer when the poster is pressed,
// so the page stays light until a visitor asks for it.
(function () {
  var box = document.querySelector('.hk-embed');
  if (!box || !box.getAttribute('data-figma')) return;
  var btn = box.querySelector('.hk-embed-poster');
  btn.addEventListener('click', function () {
    var f = document.createElement('iframe');
    f.src = box.getAttribute('data-figma');
    f.setAttribute('allowfullscreen', '');
    f.setAttribute('title', 'Figma prototype');
    f.loading = 'lazy';
    box.appendChild(f);
    btn.remove();
  });
})();
