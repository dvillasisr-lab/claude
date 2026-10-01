/* Heavy Metal 404: "Pull again" wink. Each press moves the rig a few feet; the fourth always reaches the flag.
   Nothing loads. Respects prefers-reduced-motion. */
(function () {
  'use strict';
  var LINES = ['Gained {n} ft. Still no page out here.', 'Another {n} ft. The page is still a no-show.', '{n} more ft. The crew checked: nothing on the track.', 'Up {n} ft. Almost at the flag.'];

  function Nf(nf) {
    var track = nf.querySelector('[data-nf-track]'), rig = nf.querySelector('[data-nf-rig]');
    var flag = nf.querySelector('[data-nf-flag]'), rail = nf.querySelector('[data-nf-rail]'), ticks = nf.querySelector('[data-nf-ticks]');
    var ftEl = nf.querySelector('[data-nf-ft]'), msg = nf.querySelector('[data-nf-msg]'), btn = nf.querySelector('[data-nf-again]'), btnT = nf.querySelector('[data-nf-again-t]');
    var START = Number(nf.getAttribute('data-start')) || 404, FULL = Number(nf.getAttribute('data-full')) || 440;
    if (FULL <= START) FULL = START + 30;
    var dist = START, pulls = 0, busy = null, rz = null;
    var reduce = matchMedia('(prefers-reduced-motion: reduce)');

    function fitTop() { var t = nf.getBoundingClientRect().top + window.scrollY; nf.style.setProperty('--hdr-top', Math.max(0, Math.round(t)) + 'px'); }
    function geo() { var w = track.clientWidth, padR = Math.max(44, Math.min(140, w * .07)); return { w: w, span: w - padR }; }
    function xOf(ft, g) { return ft / FULL * g.span; }
    function place(instant) {
      var g = geo(), rw = rig.getBoundingClientRect().width || 1;
      if (instant) { rig.classList.add('no-anim'); rail.classList.add('no-anim'); }
      rig.style.setProperty('--x', Math.round(xOf(dist, g) - rw * .996) + 'px');
      var rl = Math.round(xOf(dist, g) - rw * .58);
      rail.style.setProperty('--railw', (rl > 0 ? rl : 0) + 'px');
      flag.style.left = Math.round(xOf(FULL, g)) + 'px';
      var step = g.w < 600 ? 200 : 100, h = '';
      for (var f = step; f < FULL - 20; f += step) h += '<span class="nf__tick" style="left:' + Math.round(xOf(f, g)) + 'px">' + f + ' FT</span>';
      ticks.innerHTML = h;
      if (instant) { rig.getBoundingClientRect(); rail.getBoundingClientRect(); rig.classList.remove('no-anim'); rail.classList.remove('no-anim'); }
    }
    function setBtn() { btnT.textContent = dist >= FULL ? 'Reset to ' + START : 'Pull again'; }
    function onClick() {
      if (busy) return;
      var still = reduce.matches;
      if (dist >= FULL) {
        dist = START; pulls = 0; nf.classList.remove('is-full');
        msg.textContent = 'Back at ' + START + ' ft. Same page, same problem.';
      } else {
        var n = Math.min(FULL - dist, 6 + Math.floor(Math.random() * 7));
        if (pulls >= 3) n = FULL - dist;
        dist += n; pulls++;
        if (dist >= FULL) {
          msg.textContent = nf.getAttribute('data-full-msg') || 'Full pull!';
          if (!still) { nf.classList.remove('is-strike'); void nf.offsetWidth; nf.classList.add('is-strike'); }
          nf.classList.add('is-full');
        } else msg.textContent = LINES[(pulls - 1) % LINES.length].replace('{n}', n);
      }
      ftEl.textContent = dist;
      place(still); setBtn();
      if (!still) { nf.classList.add('is-pulling'); busy = setTimeout(function () { nf.classList.remove('is-pulling'); busy = null; }, 1300); }
    }
    function onResize() { clearTimeout(rz); rz = setTimeout(function () { fitTop(); place(true); }, 120); }
    function onLoad() { fitTop(); place(true); }

    btn.addEventListener('click', onClick);
    window.addEventListener('resize', onResize);
    window.addEventListener('load', onLoad);
    fitTop(); place(true); setBtn();

    this.destroy = function () {
      btn.removeEventListener('click', onClick);
      window.removeEventListener('resize', onResize);
      window.removeEventListener('load', onLoad);
      clearTimeout(rz); clearTimeout(busy);
    };
  }

  var inst = new Map();
  function init(scope) {
    [].forEach.call((scope || document).querySelectorAll('[data-hm-nf]'), function (r) { if (!inst.has(r)) inst.set(r, new Nf(r)); });
  }
  document.addEventListener('shopify:section:load', function (e) { init(e.target); });
  document.addEventListener('shopify:section:unload', function (e) {
    inst.forEach(function (x, r) { if (e.target.contains(r)) { x.destroy(); inst.delete(r); } });
  });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { init(); }); else init();
})();
