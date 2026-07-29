(function () {
  var MODES = ['light', 'system', 'dark'];

  function systemIsDark() {
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  }

  function applyTheme(mode) {
    var root = document.documentElement;
    var resolved = mode === 'system' ? (systemIsDark() ? 'dark' : 'light') : mode;
    root.setAttribute('data-theme', resolved);
  }

  function updatePill(mode) {
    var pos = MODES.indexOf(mode);
    var indicator = document.getElementById('theme-pill-indicator');
    if (indicator) indicator.setAttribute('data-pos', pos);
    document.querySelectorAll('.theme-pill-btn').forEach(function (btn, i) {
      btn.setAttribute('aria-pressed', i === pos ? 'true' : 'false');
    });
  }

  // Early apply before DOMContentLoaded (runs inline in <head> already for light/dark,
  // this handles system preference on first load)
  var saved = localStorage.getItem('theme') || 'system';
  applyTheme(saved);

  document.addEventListener('DOMContentLoaded', function () {
    if (window.lucide) window.lucide.createIcons();
    updatePill(saved);

    document.querySelectorAll('.theme-pill-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var mode = btn.getAttribute('data-theme-val');
        localStorage.setItem('theme', mode);
        saved = mode;
        applyTheme(mode);
        updatePill(mode);
      });
    });

    // React to OS preference change when mode is system
    if (window.matchMedia) {
      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function () {
        if ((localStorage.getItem('theme') || 'system') === 'system') {
          applyTheme('system');
        }
      });
    }
  });
})();
