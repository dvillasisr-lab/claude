/* HERO "Full Pull" v5: el tractor real jala el trineo (caja de pesas que avanza sobre rieles) hasta 300 FT.
   Una pasada de ~6.7 s (0.7 s enganchado + 6 s de jalón) que termina en FULL PULL!, con pausa y "Pull again".
   Todo se calcula desde el tiempo; el layout solo se mide al cargar y al cambiar de tamaño.
   El humo son partículas en el mismo SVG del rig: se quedan en el aire donde salieron (columna que sube por
   encima del texto) y se disipan. pointer-events: none en toda la pista, así no bloquean clics. */
(function () {
  /* Cinta amarilla. En Shopify: un bloque de texto por frase dentro de la sección del hero. */
  var MARQUEE = ['Full pull or nothing', 'F#ckin’ evil', 'Pro Stock · Waterloo, WI', 'Cat V8 · 680 ci', 'Horsepower: Unknown', 'Get hooked'];
  var mq = document.querySelector('[data-fp-marquee] .fp-marquee__track');
  if (mq) {
    var esc = function (t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
    var run = MARQUEE.map(function (t) { return esc(t) + '<i></i>'; }).join('');
    mq.innerHTML = '<span>' + run + run + '</span><span>' + run + run + '</span>';
    var setDur = function () { mq.style.setProperty('--mq-dur', Math.max(20, mq.scrollWidth / 2 / 70) + 's'); };
    setDur(); addEventListener('resize', setDur);
  }

  var root = document.querySelector('[data-fp]'); if (!root) return;
  var $ = function (s) { return root.querySelector(s); };
  var brand = $('.fp__brand'), rig = $('.fp__rig'), track = $('.fp__track'), top = $('.fp__top'), rail = $('[data-fp-rail]'), flag = $('[data-fp-flag]');
  var fill = $('.fp__rail-fill'), dist = $('[data-fp-dist]'), chip = $('[data-fp-chip]'), needle = $('.fp__needle'), rpm = $('[data-fp-rpm]');
  var ctrl = $('[data-fp-ctrl]'), box = $('.fp__box'), pile = $('.fp__pile'), wheelie = $('.fp__wheelie'), smokeG = $('.fp__smoke');
  var dusk = $('.fp__dusk'), sun = $('.fp__sun');
  var wheels = [].slice.call(root.querySelectorAll('.fp__sw'));
  var TARGET = parseInt(root.getAttribute('data-target') || '300', 10);
  var HOOK = 700, PULL = 6000, DUR = HOOK + PULL;
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var NS = 'http://www.w3.org/2000/svg';

  /* rig en unidades del viewBox (2240 x 576): trompa del tractor, chimenea, caja, punto de apoyo del wheelie */
  var U = { w: 2240, nose: 2222, stackX: 1655, stackY: 40, boxTravel: 580, pivot: '1320 548' };

  /* ---------- fondo (A sky / B print / C storm). En Shopify: ajuste de la sección. ---------- */
  var BGS = ['sky', 'print', 'storm'];
  var bg = root.getAttribute('data-bg') || 'sky';
  try { var q = new URLSearchParams(location.search).get('bg'), s = sessionStorage.getItem('hm-fp-bg'); bg = BGS.indexOf(q) > -1 ? q : BGS.indexOf(s) > -1 ? s : bg; } catch (e) {}
  var picks = [].slice.call(document.querySelectorAll('.fp-bgpick [data-bg]'));
  function setBg(v) {
    bg = v; root.setAttribute('data-bg', v);
    picks.forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-bg') === v ? 'true' : 'false'); });
    var meta = document.querySelector('meta[name="theme-color"]'); if (meta) meta.content = v === 'storm' ? '#1A1D22' : v === 'print' ? '#F5C400' : '#F6F5F2';
  }
  picks.forEach(function (b) { b.addEventListener('click', function () { setBg(b.getAttribute('data-bg')); try { sessionStorage.setItem('hm-fp-bg', bg); } catch (e) {} restart(); }); });
  setBg(bg);

  /* ---------- medidas (solo al cargar y en resize) ---------- */
  var G = {};
  function measure() {
    var tr = track.getBoundingClientRect(), rr = root.getBoundingClientRect(), tp = top.getBoundingClientRect(), cs = getComputedStyle(top);
    var rigW = rig.getBoundingClientRect().width, scale = rigW / U.w, narrow = matchMedia('(max-width:860px)').matches;
    var left, right;
    if (narrow) { left = brand.getBoundingClientRect().left - tr.left; right = tr.width - left; }
    else { left = tp.left - tr.left + parseFloat(cs.paddingLeft); right = tp.right - tr.left - parseFloat(cs.paddingRight); }
    var flagW = flag.getBoundingClientRect().width + Math.max(22, rigW * .045);
    var finish = right - flagW, startNose = left + rigW * (narrow ? .47 : .6);
    if (finish - startNose < 140) startNose = Math.max(left + rigW * .3, finish - 140);
    G = { scale: scale, noseOff: U.nose * scale, start: startNose, finish: finish,
      riseU: (tr.top - rr.top) / scale + U.stackY + 180, finalR: Math.max(90, Math.min(250, innerWidth * .13)) / scale,
      sunTravel: rr.height * .62 };
    rail.style.left = startNose + 'px'; rail.style.width = (finish - startNose) + 'px';
    flag.style.left = finish + 4 + 'px';
    root.style.setProperty('--edge', (tr.width - right) + 'px');
    rail.querySelectorAll('.fp__tick').forEach(function (t) { t.remove(); });
    [0, 1 / 3, 2 / 3, 1].forEach(function (f, i) {
      var t = document.createElement('span');
      t.className = 'fp__tick' + (i === 0 ? ' fp__tick--first' : i === 3 ? ' fp__tick--last' : '');
      t.style.left = (f * 100) + '%';
      t.textContent = i === 0 ? '0 FT' : i === 3 ? TARGET + ' FT' : Math.round(TARGET * f);
      rail.appendChild(t);
    });
  }

  /* ---------- tiempo → progreso ---------- */
  function progress(ms) {
    if (ms <= HOOK) return 0;
    var t = Math.min(1, (ms - HOOK) / PULL);
    var a = t < .1 ? 5 * t * t : t - .05; a /= .95;           /* arranque suave */
    return Math.min(1, a * (1.35 - .35 * a));                  /* y se frena al final: la caja ya está adelante */
  }

  /* ---------- humo ---------- */
  var P = [], POOL = reduce ? 0 : 70, alive = 0;
  for (var i = 0; i < POOL; i++) {
    var c = document.createElementNS(NS, 'circle'); c.setAttribute('r', '40'); c.setAttribute('fill', 'url(#fpPuff)'); c.style.opacity = '0';
    smokeG.appendChild(c); P.push({ el: c, on: false });
  }
  var nextPuff = 0;
  function emit(clock, rigX, big) {
    for (var i = 0; i < P.length; i++) if (!P[i].on) {
      var p = P[i]; p.on = true; alive++;
      p.t0 = clock; p.rx = rigX; p.big = big;
      p.life = (big ? 2600 : 1500) + Math.random() * 900;
      p.x0 = U.stackX + (Math.random() * 30 - 15); p.y0 = U.stackY; p.vr = .75 + Math.random() * .45;
      p.drift = -(120 + Math.random() * 420); p.wob = Math.random() * 6.28;
      p.size = big ? .8 + Math.random() * .7 : .3 + Math.random() * .2;
      return;
    }
  }
  function smoke(clock, rigX) {
    for (var i = 0; i < P.length; i++) {
      var p = P[i]; if (!p.on) continue;
      var a = (clock - p.t0) / p.life;
      if (a >= 1) { p.on = false; alive--; p.el.style.opacity = '0'; continue; }
      var rise = (p.big ? G.riseU * p.vr : G.riseU * .35) * (1 - Math.pow(1 - a, 1.7));
      var x = p.x0 + p.drift * a + Math.sin(a * 4 + p.wob) * 40 - (rigX - p.rx) / G.scale; /* se queda en el aire: no viaja con el tractor */
      var y = p.y0 - rise;
      var sc = (1 + (G.finalR / 40 - 1) * Math.pow(a, .65)) * p.size;
      var op = (a < .06 ? a / .06 : 1) * Math.pow(1 - a, 1.1) * (p.big ? .95 : .7);
      p.el.setAttribute('transform', 'translate(' + x.toFixed(1) + ' ' + y.toFixed(1) + ') scale(' + sc.toFixed(3) + ')');
      p.el.style.opacity = op.toFixed(3);
    }
  }

  /* ---------- pintar un instante ---------- */
  var lastX = 0;
  function paint(ms, clock) {
    var k = Math.min(1, ms / DUR), prog = progress(ms), full = k >= 1;
    var nose = G.start + (G.finish - G.start) * prog, x = nose - G.noseOff;
    lastX = x;
    rig.style.transform = 'translate3d(' + x.toFixed(1) + 'px,0,0)';
    fill.style.setProperty('--p', prog.toFixed(4));
    dist.textContent = String(Math.round(prog * TARGET)).padStart(3, '0');
    var r = full ? 1100 : ms < HOOK ? Math.round(1400 + (ms / HOOK) * 3800) : Math.min(7000, Math.round(6100 + Math.sin(ms / 60) * 280 + prog * 600));
    needle.style.transform = 'rotate(' + (-120 + (r / 7000) * 240).toFixed(1) + 'deg)';
    rpm.textContent = r;
    box.setAttribute('transform', 'translate(' + (prog * U.boxTravel).toFixed(1) + ' 0)');
    pile.setAttribute('transform', 'translate(1030 550) scale(' + (.15 + prog * 1.1).toFixed(3) + ') translate(-1030 -550)');
    var travelled = (nose - G.start) / G.scale;
    wheels.forEach(function (w) { w.setAttribute('transform', 'rotate(' + (travelled / 60 * 57.3 % 360).toFixed(1) + ' ' + w.getAttribute('data-c') + ')'); });
    var lift = !full && prog > .02 && prog < .97 ? 1.2 + 2.6 * Math.max(0, Math.sin(ms / 340)) * (1 - prog * .5) : 0;
    wheelie.setAttribute('transform', 'rotate(' + (-lift).toFixed(2) + ' ' + U.pivot + ')');
    if (bg === 'sky') { dusk.style.opacity = (Math.pow(prog, 1.2) * .92).toFixed(3); sun.style.transform = 'translate3d(0,' + (prog * G.sunTravel).toFixed(1) + 'px,0)'; }
    chip.textContent = full ? 'Full pull!' : prog > 0 ? 'Pulling' : 'Hooked';
    chip.classList.toggle('is-full', full);
    root.classList.toggle('is-full', full);
    root.classList.toggle('is-pulling', prog > 0 && !full && state === 'run');
    /* humo: al enganchar, bocanadas cortas; al jalar, columna densa; al terminar, deja de salir y se disipa */
    if (P.length && state === 'run' && clock >= nextPuff) {
      var pulling = ms >= HOOK;
      emit(clock, x, pulling);
      if (pulling && ms - HOOK < 120) { emit(clock, x, true); emit(clock, x, true); }
      nextPuff = clock + (pulling ? 45 : 240);
    }
    if (P.length) smoke(clock, x);
  }

  /* ---------- reloj ---------- */
  var state = 'run', ms = 0, clock = 0, last = 0, raf = 0, visible = true;
  function loop(now) {
    var dt = last ? Math.min(64, now - last) : 16; last = now;
    if (state !== 'paused') clock += dt;
    if (state === 'run') ms += dt;
    paint(Math.min(ms, DUR), clock);
    if (state === 'run' && ms >= DUR) finish();
    if (visible && (state === 'run' || (state === 'done' && alive > 0))) raf = requestAnimationFrame(loop);
    else { raf = 0; last = 0; }
  }
  function kick() { if (!raf && visible) { last = 0; raf = requestAnimationFrame(loop); } }
  function finish() {
    state = 'done'; root.classList.remove('is-running', 'is-pulling'); ctrl.textContent = 'Pull again';
    if (bg === 'storm' && !reduce) { root.classList.remove('is-strike'); void root.offsetWidth; root.classList.add('is-strike'); }
  }
  function restart() {
    if (reduce) { paint(DUR, 0); return; }
    ms = 0; state = 'run'; nextPuff = 0; root.classList.remove('is-strike', 'is-full'); root.classList.add('is-running');
    if (bg !== 'sky') { dusk.style.opacity = '0'; sun.style.transform = ''; }
    ctrl.textContent = 'Pause'; kick();
  }
  ctrl.addEventListener('click', function () {
    if (reduce) return;
    if (state === 'run') { state = 'paused'; root.classList.remove('is-running', 'is-pulling'); ctrl.textContent = 'Resume'; return; }
    if (state === 'paused') { state = 'run'; root.classList.add('is-running'); ctrl.textContent = 'Pause'; kick(); return; }
    restart();
  });

  measure();
  if (reduce) { state = 'done'; ctrl.hidden = true; paint(DUR, 0); }
  else restart();
  if ('IntersectionObserver' in window) new IntersectionObserver(function (e) { visible = e[0].isIntersecting; if (visible) kick(); }).observe(root);
  var rt; addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(function () { measure(); paint(Math.min(ms, DUR), clock); }, 80); });
})();
