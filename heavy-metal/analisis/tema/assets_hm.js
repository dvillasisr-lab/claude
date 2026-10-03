(function () {
  function initHero(root) {
    var rig = root.querySelector('.hm-rig');
    var rail = root.querySelector('.hm-rail');
    var fill = root.querySelector('.hm-rail__fill');
    var dist = root.querySelector('[data-hm-distance]');
    var chip = root.querySelector('[data-hm-chip]');
    var needle = root.querySelector('.hm-needle');
    var rpmText = root.querySelector('.hm-rpm');
    var target = parseInt(root.getAttribute('data-target') || '300', 10);
    if (!rig || !rail) return;
    var wasFull = false;
    function frame(now) {
      var r = rig.getBoundingClientRect();
      var railR = rail.getBoundingClientRect();
      // front of the tractor sits ~1% in from the right edge of the rig drawing
      var front = r.right - r.width * 0.013;
      var prog = (front - railR.left) / railR.width;
      prog = Math.max(0, Math.min(1, prog));
      var ft = Math.round(prog * target);
      var running = front > railR.left - r.width * 0.2 && front < railR.right + 4;
      var rpm;
      if (prog <= 0) rpm = running ? 5200 : 900;
      else if (prog < 1) rpm = Math.min(7000, Math.round(6500 + Math.sin(now / 90) * 150 + prog * 300));
      else rpm = Math.max(900, Math.round(6800 - Math.min(1, (front - railR.right) / (window.innerWidth * 0.6)) * 5900));
      if (fill) fill.style.width = (prog * 100).toFixed(2) + '%';
      if (dist) dist.textContent = String(ft).padStart(3, '0');
      if (needle) needle.style.transform = 'rotate(' + (-120 + (rpm / 7000) * 240).toFixed(1) + 'deg)';
      if (rpmText) rpmText.textContent = rpm;
      var full = prog >= 1;
      if (chip && full !== wasFull) {
        chip.textContent = full ? chip.getAttribute('data-full') : chip.getAttribute('data-pulling');
        chip.classList.toggle('is-full', full);
        wasFull = full;
      }
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }
  function initVideo(root) {
    var btn = root.querySelector('.hm-video__poster');
    var tpl = root.querySelector('template');
    if (!btn || !tpl) return;
    btn.addEventListener('click', function () {
      btn.replaceWith(tpl.content.cloneNode(true));
    });
  }
  function boot() {
    document.querySelectorAll('[data-hm-hero]').forEach(initHero);
    document.querySelectorAll('[data-hm-video]').forEach(initVideo);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
  document.addEventListener('shopify:section:load', boot);
})();

