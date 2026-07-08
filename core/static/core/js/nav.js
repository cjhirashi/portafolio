(function () {
  var MOBILE_BREAKPOINT = 768;

  document.addEventListener('DOMContentLoaded', function () {
    var toggle = document.getElementById('nav-toggle');
    var nav = document.getElementById('site-nav');
    if (!toggle || !nav) return;

    function setOpen(open) {
      toggle.setAttribute('aria-expanded', String(open));
      nav.classList.toggle('is-open', open);
    }

    toggle.addEventListener('click', function () {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });

    window.addEventListener('resize', function () {
      if (window.innerWidth > MOBILE_BREAKPOINT) setOpen(false);
    });
  });
})();
