/* HM Hero "Full Pull" (port 1:1 de boceto-v28/hero.js).
   - El tractor real jala el sled de 0 FT (borde izquierdo del logo) hasta la bandera: HOOK 500 ms + PULL 5000 ms = 5.5 s,
     termina en FULL PULL! con rayo. Pause / Resume / Pull again = solo el icono (flecha) junto al poste, en el cielo gris.
   - En escritorio la pista se coloca para que el rig completo pase DEBAJO de los links del hero.
   - prefers-reduced-motion: se pinta el ultimo cuadro, sin humo ni animacion. Fuera de pantalla se detiene.
   - Editor de temas: shopify:section:load / unload inician y limpian (requestAnimationFrame, timers y listeners). */
(function () {
  if (window.HMHero) return;
  var NS = 'http://www.w3.org/2000/svg';
  /* rig en unidades del viewBox (2700 x 576) */
  var U = { w: 2700, nose: 2680, rear: 1602, stackX: 2115, stackY: 38, boxTravel: 720, px: 1780, py: 548, wheelR: 84, sledTop: 159, cabTop: 22 };
  var HOOK = 500, PULL = 5000, DUR = HOOK + PULL, GAP = 24;

  function progress(ms) {
    if (ms <= HOOK) return 0;
    var t = Math.min(1, (ms - HOOK) / PULL);
    var a = t < .1 ? 5 * t * t : t - .05; a /= .95;
    return Math.min(1, a * (1.35 - .35 * a));
  }

  function init(root) {
    if (!root || root.__hmHero) return;
    var $ = function (s) { return root.querySelector(s); };
    var brand = $('.fp__brand'), rig = $('.fp__rig'), track = $('.fp__track'), top = $('.fp__top'), rail = $('[data-fp-rail]'), flag = $('[data-fp-flag]');
    var fill = $('.fp__rail-fill'), dist = $('[data-fp-dist]'), chip = $('[data-fp-chip]'), needle = $('.fp__needle'), rpm = $('[data-fp-rpm]');
    var ctrl = $('[data-fp-ctrl]'), ctrlTxt = $('[data-fp-ctrl-txt]');
    var box = $('.fp__box'), pile = $('.fp__pile'), wheelie = $('.fp__wheelie'), smokeG = $('.fp__smoke');
    var tele = $('.fp__tele'), btnRow = $('.fp__brand .btn-row'), logo = $('.fp__logo'), dirt = $('.fp__dirt');
    if (!rig || !track || !ctrl || !brand || !logo) return;
    var wheels = [].slice.call(root.querySelectorAll('.fp__sw'));
    var TARGET = parseInt(root.getAttribute('data-target') || '300', 10) || 300;
    var PUFF = root.getAttribute('data-fp-puff') || 'fpPuff';
    var rmq = matchMedia('(prefers-reduced-motion: reduce)'), reduce = rmq.matches;
    var nmq = matchMedia('(max-width:860px)');
    var dead = false, timers = [], io = null;
    var L = { again: ctrl.getAttribute('data-l-again') || 'Pull again', pause: ctrl.getAttribute('data-l-pause') || 'Pause', play: ctrl.getAttribute('data-l-play') || 'Resume' };
    var C = { hooked: chip.getAttribute('data-l-hooked') || 'Hooked', pulling: chip.getAttribute('data-l-pulling') || 'Pulling', full: chip.getAttribute('data-l-full') || 'Full pull!' };

    function setCtrl(mode) {
      ctrl.setAttribute('data-mode', mode);
      ctrlTxt.textContent = mode === 'pause' ? L.pause : mode === 'play' ? L.play : L.again;
      ctrl.title = ctrlTxt.textContent;
      ctrl.setAttribute('aria-label', ctrlTxt.textContent);
    }

    /* ---------- medidas (solo al cargar y en resize) ---------- */
    var G = {};
    function measure() {
      var narrow = nmq.matches;
      if (narrow) { root.style.removeProperty('--tuck'); flag.style.height = ''; }
      else if (btnRow) {
        root.style.setProperty('--tuck', '0px');
        var tr0 = track.getBoundingClientRect(), b0 = btnRow.getBoundingClientRect();
        var dirtH0 = dirt.getBoundingClientRect().height, s0 = rig.getBoundingClientRect().width / U.w;
        var dirtTop0 = tr0.bottom - dirtH0, want = b0.bottom + 10 + 5 + (U.py - U.cabTop + 8) * s0;
        root.style.setProperty('--tuck', Math.max(0, Math.round(dirtTop0 - want)) + 'px');
      }
      var tr = track.getBoundingClientRect(), rr = root.getBoundingClientRect(), tp = top.getBoundingClientRect(), cs = getComputedStyle(top);
      var rg = rig.getBoundingClientRect(), rigW = rg.width, scale = rigW / U.w;
      /* 0 FT = borde izquierdo del logo HEAVY METAL */
      var left = logo.getBoundingClientRect().left - tr.left;
      var right = narrow ? tr.width - (brand.getBoundingClientRect().left - tr.left) : tp.right - tr.left - parseFloat(cs.paddingRight);
      var flagW = flag.getBoundingClientRect().width + Math.max(22, rigW * .04);
      var finish = right - flagW;
      var poleW = flag.getBoundingClientRect().width || 6, CTRL = 44, M = 8;
      finish = Math.min(finish, tr.width - (M + CTRL + 8 + poleW + 4));
      var zero = left, startNose = zero + (U.nose - U.rear) * scale;
      if (finish - startNose < 60) startNose = finish - 60;
      G = { scale: scale, noseOff: U.nose * scale, start: startNose, finish: finish, rigTop: rg.top - rr.top,
        R: Math.max(40, Math.min(170, rigW * .1)), rise: (rg.top - rr.top) + U.stackY * scale + 60, rigW: rigW };
      rail.style.left = zero + 'px'; rail.style.width = (finish - zero) + 'px';
      flag.style.left = finish + 4 + 'px';
      var dirtH = dirt.getBoundingClientRect().height;
      if (!narrow && tele) flag.style.height = Math.max(40, tr.bottom - dirtH - tele.getBoundingClientRect().bottom - GAP) + 'px';
      root.style.setProperty('--edge', (tr.width - right) + 'px');
      /* Pause / Pull again: solo la flecha, a la derecha del poste, en lo gris justo arriba de la tierra */
      var rr2 = root.getBoundingClientRect();
      var cx = Math.min(tr.left - rr2.left + finish + 4 + poleW + 8, rr2.width - M - CTRL), avail = rr2.width - cx - M;
      ctrl.style.left = cx + 'px'; ctrl.style.right = 'auto'; ctrl.style.bottom = (rr2.bottom - tr.bottom + dirtH + 4) + 'px';
      ctrl.style.maxWidth = Math.max(44, avail) + 'px'; ctrl.classList.remove('is-stack'); ctrl.classList.add('is-icon');
      [].slice.call(rail.querySelectorAll('.fp__tick')).forEach(function (t) { t.remove(); });
      [0, 1 / 3, 2 / 3, 1].forEach(function (f, i) {
        if ((i === 1 || i === 2) && finish - zero < 280) return;
        var t = document.createElement('span');
        t.className = 'fp__tick' + (i === 0 ? ' fp__tick--first' : i === 3 ? ' fp__tick--last' : '');
        t.style.left = (f * 100) + '%';
        t.textContent = i === 0 ? '0 FT' : i === 3 ? TARGET + ' FT' : Math.round(TARGET * f);
        rail.appendChild(t);
      });
    }

    /* ---------- humo ---------- */
    var P = [], POOL = reduce ? 0 : 200, alive = 0, INHERIT = .6;
    function makePool() {
      if (!smokeG) return;
      for (var i = P.length; i < POOL; i++) {
        var c = document.createElementNS(NS, 'circle'); c.setAttribute('r', '50'); c.setAttribute('fill', 'url(#' + PUFF + (i % 3) + ')'); c.style.opacity = '0';
        smokeG.appendChild(c); P.push({ el: c, on: false });
      }
    }
    makePool();
    function stackPoint(rigX, lift) {
      var th = -lift * Math.PI / 180, dx = U.stackX - U.px, dy = U.stackY - U.py;
      var sx = U.px + dx * Math.cos(th) - dy * Math.sin(th), sy = U.py + dx * Math.sin(th) + dy * Math.cos(th);
      return [rigX + sx * G.scale, G.rigTop + sy * G.scale];
    }
    var nextPuff = 0;
    function emit(clk, rigX, sp, big) {
      for (var i = 0; i < P.length; i++) if (!P[i].on) {
        var p = P[i]; p.on = true; alive++;
        p.t0 = clk; p.rx = rigX; p.big = big;
        p.life = big ? 2300 + Math.random() * 900 : 1100 + Math.random() * 500;
        p.x0 = sp[0] + (Math.random() - .5) * G.R * .12; p.y0 = sp[1];
        p.vr = big ? .82 + Math.random() * .3 : .22 + Math.random() * .1;
        p.drift = -G.rigW * (.008 + Math.random() * .03); p.wob = Math.random() * 6.28;
        p.size = big ? .75 + Math.random() * .5 : .35 + Math.random() * .15;
        return;
      }
    }
    function preroll(clk, rigX) {
      var sp = stackPoint(rigX, 0);
      for (var t = -2600; t < 0; t += 30) emit(clk + t, rigX, sp, true);
    }
    function smoke(clk, rigX) {
      for (var i = 0; i < P.length; i++) {
        var p = P[i]; if (!p.on) continue;
        var a = (clk - p.t0) / p.life;
        if (a >= 1) { p.on = false; alive--; p.el.style.opacity = '0'; continue; }
        var rise = G.rise * p.vr * (1 - Math.pow(1 - a, 2.1));
        var x = p.x0 + (rigX - p.rx) * INHERIT + p.drift * a + Math.sin(a * 3 + p.wob) * G.R * .18 * a;
        var y = p.y0 - rise;
        var sc = G.R * p.size * (.22 + .78 * Math.pow(a, .55)) / 50;
        var op = (a < .05 ? a / .05 : 1) * (a < .5 ? 1 : 1 - Math.pow((a - .5) / .5, 1.4)) * (p.big ? 1 : .8);
        p.el.setAttribute('transform', 'translate(' + x.toFixed(1) + ' ' + y.toFixed(1) + ') scale(' + sc.toFixed(3) + ')');
        p.el.style.opacity = op.toFixed(3);
      }
    }
    function clearSmoke() { P.forEach(function (p) { p.on = false; p.el.style.opacity = '0'; }); alive = 0; }

    /* ---------- pintar un instante ---------- */
    var state = 'run', ms = 0, clock = 0, last = 0, raf = 0, visible = true, idleUntil = 0, ready = false;
    function paint(t, clk) {
      var k = Math.min(1, t / DUR), prog = progress(t), full = k >= 1;
      var nose = G.start + (G.finish - G.start) * prog, x = nose - G.noseOff;
      rig.style.transform = 'translate3d(' + x.toFixed(1) + 'px,0,0)';
      fill.style.setProperty('--p', prog.toFixed(4));
      dist.textContent = String(Math.round(prog * TARGET)).padStart(3, '0');
      var r = full ? 1100 : t < HOOK ? Math.round(1400 + (t / HOOK) * 3800) : Math.min(7000, Math.round(6100 + Math.sin(t / 60) * 280 + prog * 600));
      if (needle) needle.style.transform = 'rotate(' + (-120 + (r / 7000) * 240).toFixed(1) + 'deg)';
      if (rpm) rpm.textContent = r;
      if (box) box.setAttribute('transform', 'translate(' + (prog * U.boxTravel).toFixed(1) + ' 0)');
      if (pile) pile.setAttribute('transform', 'translate(1452 550) scale(' + (.15 + prog * 1.1).toFixed(3) + ') translate(-1452 -550)');
      var travelled = (nose - G.start) / G.scale;
      wheels.forEach(function (w) { w.setAttribute('transform', 'rotate(' + (travelled / U.wheelR * 57.3 % 360).toFixed(1) + ' ' + w.getAttribute('data-c') + ')'); });
      var lift = !full && prog > .02 && prog < .97 ? 1.2 + 2.4 * Math.max(0, Math.sin(t / 340)) * (1 - prog * .5) : 0;
      if (wheelie) wheelie.setAttribute('transform', 'rotate(' + (-lift).toFixed(2) + ' ' + U.px + ' ' + U.py + ')');
      chip.textContent = full ? C.full : prog > 0 ? C.pulling : C.hooked;
      chip.classList.toggle('is-full', full);
      root.classList.toggle('is-full', full);
      root.classList.toggle('is-pulling', prog > 0 && !full && state === 'run');
      if (P.length && state === 'run' && clk >= nextPuff) {
        var pulling = t >= HOOK, sp = stackPoint(x, lift);
        emit(clk, x, sp, pulling);
        if (pulling) emit(clk, x, sp, true);
        if (pulling && t - HOOK < 150) { emit(clk, x, sp, true); emit(clk, x, sp, true); }
        nextPuff = clk + (pulling ? 30 : 200);
      }
      if (P.length) smoke(clk, x);
    }

    /* ---------- reloj ---------- */
    function loop(now) {
      if (dead) return;
      var dt = last ? Math.min(64, now - last) : 16; last = now;
      if (state !== 'paused') clock += dt;
      if (state === 'run') ms += dt;
      paint(Math.min(ms, DUR), clock);
      if (state === 'run' && ms >= DUR) finish();
      if (visible && (state === 'run' || (state === 'done' && (alive > 0 || clock < idleUntil)))) raf = requestAnimationFrame(loop);
      else { raf = 0; last = 0; }
    }
    function kick() { if (!dead && !reduce && ready && !raf && visible) { last = 0; raf = requestAnimationFrame(loop); } }
    function stop() { if (raf) cancelAnimationFrame(raf); raf = 0; last = 0; }
    function finish() {
      state = 'done'; idleUntil = clock; root.classList.remove('is-running', 'is-pulling'); setCtrl('again');
      if (!reduce) { root.classList.remove('is-strike'); void root.offsetWidth; root.classList.add('is-strike'); }
    }
    function restart() {
      if (reduce) { paint(DUR, 0); return; }
      ms = 0; state = 'run'; nextPuff = 0; idleUntil = 0; root.classList.remove('is-strike', 'is-full'); root.classList.add('is-running');
      if (P.length) preroll(clock, G.start - G.noseOff);
      setCtrl('pause'); kick();
    }
    function onCtrl() {
      if (reduce) return;
      if (state === 'run') { state = 'paused'; root.classList.remove('is-running', 'is-pulling'); setCtrl('play'); return; }
      if (state === 'paused') { state = 'run'; root.classList.add('is-running'); setCtrl('pause'); kick(); return; }
      restart();
    }
    ctrl.addEventListener('click', onCtrl);
    function applyReduce() {
      ctrl.hidden = reduce;
      if (reduce) { stop(); clearSmoke(); state = 'done'; ms = DUR; root.classList.remove('is-running', 'is-pulling', 'is-strike'); paint(DUR, 0); }
    }
    var onRm = function (e) { reduce = e.matches; if (!reduce) { POOL = 200; makePool(); applyReduce(); restart(); } else applyReduce(); };
    if (rmq.addEventListener) rmq.addEventListener('change', onRm); else if (rmq.addListener) rmq.addListener(onRm);

    measure();
    ctrl.hidden = reduce;
    if (reduce) { ready = true; applyReduce(); }
    else {
      /* cuadro 0 quieto hasta que carga el recorte del tractor (max. 2.5 s): nunca arranca "ya avanzado" */
      restart(); paint(0, clock);
      var go = function () { if (ready || dead) return; ready = true; last = 0; kick(); };
      var imgEl = rig.querySelector('image'), src = imgEl && (imgEl.getAttribute('href') || imgEl.getAttributeNS('http://www.w3.org/1999/xlink', 'href'));
      if (src) { var im = new Image(); im.onload = im.onerror = go; im.src = src; if (im.complete) go(); }
      else go();
      timers.push(setTimeout(go, 2500));
    }
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { if (dead) return; measure(); paint(Math.min(ms, DUR), clock); });
    if ('IntersectionObserver' in window) {
      io = new IntersectionObserver(function (e) { visible = e[0].isIntersecting; if (visible) kick(); else stop(); });
      io.observe(root);
    }
    var rt = 0;
    var onResize = function () { clearTimeout(rt); rt = setTimeout(function () { if (dead) return; measure(); paint(Math.min(ms, DUR), clock); }, 80); };
    window.addEventListener('resize', onResize);

    root.__hmHero = {
      destroy: function () {
        dead = true; stop(); clearTimeout(rt); timers.forEach(clearTimeout);
        window.removeEventListener('resize', onResize);
        ctrl.removeEventListener('click', onCtrl);
        if (rmq.removeEventListener) rmq.removeEventListener('change', onRm); else if (rmq.removeListener) rmq.removeListener(onRm);
        if (io) io.disconnect();
        root.__hmHero = null;
      }
    };
  }

  function destroy(root) { if (root && root.__hmHero) root.__hmHero.destroy(); }
  function initAll(scope) { [].slice.call((scope || document).querySelectorAll('[data-fp]')).forEach(init); }

  window.HMHero = { init: init, destroy: destroy };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { initAll(); });
  else initAll();
  document.addEventListener('shopify:section:load', function (e) { initAll(e.target); });
  document.addEventListener('shopify:section:unload', function (e) { [].slice.call(e.target.querySelectorAll('[data-fp]')).forEach(destroy); });
})();
