(function () {
  function renderIcons() {
    if (window.lucide) window.lucide.createIcons();
  }

  document.addEventListener('DOMContentLoaded', function () {
    renderIcons();

    var toggle = document.getElementById('theme-toggle');
    if (!toggle) return;

    toggle.addEventListener('click', function () {
      var root = document.documentElement;
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      localStorage.setItem('theme', next);
    });
  });
})();
