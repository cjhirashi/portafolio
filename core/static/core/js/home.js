(function () {
  var DURATION = 1100;

  function animateCount(el) {
    var to = parseFloat(el.dataset.countTo);
    var suffix = el.dataset.countSuffix || '';
    var start = Date.now();

    function tick() {
      var elapsed = Date.now() - start;
      var progress = Math.min(elapsed / DURATION, 1);
      var value = Math.floor(to * progress);
      el.textContent = value + suffix;
      if (progress < 1) requestAnimationFrame(tick);
    }

    requestAnimationFrame(tick);
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-count-to]').forEach(animateCount);
  });
})();
