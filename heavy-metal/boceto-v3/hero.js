/* HERO "Full Pull": una pasada de ~6.5 s del tractor real por la pista. Calcula todo desde el tiempo
   (no lee layout en cada frame), se pausa fuera de pantalla, termina en FULL PULL! y se puede repetir. */
(function () {
  var root = document.querySelector('[data-fp]'); if (!root) return;
  var rig = root.querySelector('.fp__rig'), rail = root.querySelector('.fp__rail'), track = root.querySelector('.fp__track');
  var fill = root.querySelector('.fp__rail-fill'), dist = root.querySelector('[data-fp-dist]'), chip = root.querySelector('[data-fp-chip]');
  var needle = root.querySelector('.fp__needle'), rpm = root.querySelector('[data-fp-rpm]'), ctrl = root.querySelector('[data-fp-ctrl]');
  var tractor = root.querySelector('.fp__tractor');
  var TARGET = parseInt(root.getAttribute('data-target') || '300', 10), DUR = 6500;
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var geo = {}, t0 = 0, elapsed = 0, raf = 0, running = false, visible = true;

  function measure() {
    var tr = track.getBoundingClientRect(), rr = rail.getBoundingClientRect(), rw = rig.getBoundingClientRect().width;
    /* la trompa del tractor es el borde derecho del rig: arranca fuera a la izquierda y termina en la meta */
    geo = { start: -rw, railL: rr.left - tr.left, railW: rr.width, rigW: rw, end: rr.left - tr.left + rr.width - rw };
    root.style.setProperty('--x-end', geo.end + 'px');
  }
  function ease(t) { return t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; }
  function paint(k) {
    var x = geo.start + (geo.end - geo.start) * ease(k);
    rig.style.setProperty('--x', x + 'px');
    var front = x + geo.rigW, prog = Math.max(0, Math.min(1, (front - geo.railL) / geo.railW));
    fill.style.setProperty('--p', prog.toFixed(3));
    dist.textContent = String(Math.round(prog * TARGET)).padStart(3, '0');
    var r = k >= 1 ? 1100 : prog > 0 ? Math.min(7000, 6200 + Math.round(Math.sin(k * 40) * 250 + prog * 500)) : 4800;
    needle.style.transform = 'rotate(' + (-120 + (r / 7000) * 240).toFixed(1) + 'deg)';
    rpm.textContent = r;
    root.querySelector('.fp__sled').style.setProperty('--box', (prog * 40).toFixed(1) + '%');
    tractor.classList.toggle('is-up', prog > .05 && prog < .95 && Math.sin(k * 18) > .6);
    var full = k >= 1;
    chip.textContent = full ? 'Full pull!' : prog > 0 ? 'Pulling' : 'Hooked';
    chip.classList.toggle('is-full', full);
  }
  function tick(now) {
    if (!t0) t0 = now - elapsed;
    elapsed = now - t0;
    var k = Math.min(1, elapsed / DUR);
    paint(k);
    if (k < 1 && running && visible) raf = requestAnimationFrame(tick);
    else if (k >= 1) stop(true);
  }
  function start() { cancelAnimationFrame(raf); running = true; t0 = 0; root.classList.add('is-running'); ctrl.textContent = 'Pause'; raf = requestAnimationFrame(tick); }
  function stop(done) { running = false; cancelAnimationFrame(raf); root.classList.remove('is-running'); ctrl.textContent = done ? 'Pull again' : 'Resume'; if (done) elapsed = 0; }

  measure();
  if (reduce) { paint(1); ctrl.textContent = 'Pull again'; }
  else start();
  ctrl.addEventListener('click', function () {
    if (running) { stop(false); return; }
    if (ctrl.textContent === 'Pull again') elapsed = 0;
    start();
  });
  new IntersectionObserver(function (e) {
    visible = e[0].isIntersecting;
    if (visible && running) { t0 = 0; raf = requestAnimationFrame(tick); }
  }).observe(root);
  addEventListener('resize', function () { measure(); if (!running) paint(elapsed ? Math.min(1, elapsed / DUR) : 1); });
})();
