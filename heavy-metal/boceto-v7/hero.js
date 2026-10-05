/* HERO "Full Pull" v7: el tractor real jala el sled de transferencia de peso (la caja de pesas avanza sobre los rieles
   hacia el pan) hasta la distancia de full pull. Una pasada de ~8.2 s (0.7 s enganchado + 7.5 s de jalón) que termina
   en FULL PULL! con rayo; Pause y "Pull again".
   - Arranque: la trompa del tractor sale a la altura del botón "Shop the drop" (el sled puede quedar fuera de pantalla
     a la izquierda) y recorre hasta la bandera.
   - Todo se calcula desde el tiempo; el layout solo se mide al cargar y al cambiar de tamaño.
   - Humo: capa SVG propia detrás del texto. Bocanadas opacas en tres tonos que salen de la chimenea, suben casi
     rectas (heredan parte del avance del tractor) y se abren al subir.
   - Pull sim sencillo: RPM, distancia en pies y estado (Hooked / Pulling / Full pull!). Sin sonido. */
(function () {
  var esc = function (t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };

  /* ---------- cinta amarilla. En Shopify: un bloque de texto por frase en la sección del hero (máximo 3) ---------- */
  var MARQUEE = ['Full pull or nothing', 'This is f#cking evil'];
  var mq = document.querySelector('[data-fp-marquee] .fp-marquee__track');
  if (mq) {
    var run = MARQUEE.slice(0, 3).map(function (t) { return esc(t) + '<i>·</i>'; }).join('');
    var buildMq = function () {
      mq.innerHTML = '<span>' + run + '</span>';
      var w = mq.firstChild.getBoundingClientRect().width || 600;
      var half = new Array(Math.max(2, Math.ceil(innerWidth * 1.15 / w)) + 1).join(run);
      mq.innerHTML = '<span>' + half + '</span><span>' + half + '</span>';
      mq.style.setProperty('--mq-dur', Math.max(18, mq.scrollWidth / 2 / 60) + 's');
    };
    buildMq();
    var mqw = innerWidth, mt; addEventListener('resize', function () { clearTimeout(mt); mt = setTimeout(function () { if (Math.abs(innerWidth - mqw) > 40) { mqw = innerWidth; buildMq(); } }, 150); });
  }

  var root = document.querySelector('[data-fp]'); if (!root) return;
  var $ = function (s) { return root.querySelector(s); };
  var brand = $('.fp__brand'), rig = $('.fp__rig'), track = $('.fp__track'), top = $('.fp__top'), rail = $('[data-fp-rail]'), flag = $('[data-fp-flag]');
  var fill = $('.fp__rail-fill'), dist = $('[data-fp-dist]'), chip = $('[data-fp-chip]'), needle = $('.fp__needle'), rpm = $('[data-fp-rpm]');
  var ctrl = $('[data-fp-ctrl]'), shopBtn = brand.querySelector('.btn-row .btn');
  var box = $('.fp__box'), pile = $('.fp__pile'), wheelie = $('.fp__wheelie'), smokeG = $('.fp__smoke');
  var wheels = [].slice.call(root.querySelectorAll('.fp__sw'));
  var TARGET = parseInt(root.getAttribute('data-target') || '300', 10);
  var HOOK = 700, PULL = 7500, DUR = HOOK + PULL;
  var rmq = matchMedia('(prefers-reduced-motion: reduce)'), reduce = rmq.matches;
  var NS = 'http://www.w3.org/2000/svg';

  /* rig en unidades del viewBox (2700 x 576): trompa del tractor, chimenea, recorrido de la caja, apoyo del wheelie, radio de las ruedas del sled */
  var U = { w: 2700, nose: 2680, stackX: 2115, stackY: 38, boxTravel: 720, px: 1780, py: 548, wheelR: 105 };

  /* ---------- medidas (solo al cargar y en resize) ---------- */
  var G = {};
  function measure() {
    var tr = track.getBoundingClientRect(), rr = root.getBoundingClientRect(), tp = top.getBoundingClientRect(), cs = getComputedStyle(top);
    var rg = rig.getBoundingClientRect(), rigW = rg.width, scale = rigW / U.w, narrow = matchMedia('(max-width:860px)').matches;
    var left, right;
    if (narrow) { left = brand.getBoundingClientRect().left - tr.left; right = tr.width - left; }
    else { left = tp.left - tr.left + parseFloat(cs.paddingLeft); right = tp.right - tr.left - parseFloat(cs.paddingRight); }
    var flagW = flag.getBoundingClientRect().width + Math.max(22, rigW * .04);
    var noseOff = U.nose * scale, finish = right - flagW;
    /* arranca con la trompa a la altura del botón "Shop the drop" (su orilla derecha) para que el recorrido sea largo;
       el sled queda fuera de pantalla a la izquierda. Si la pista queda corta, arranca más a la izquierda. */
    var sb = shopBtn ? shopBtn.getBoundingClientRect() : null;
    var startNose = sb ? sb.right - tr.left : rigW * .3, minTravel = Math.max(140, tr.width * (narrow ? .38 : .45));
    if (finish - startNose < minTravel) startNose = finish - minTravel;
    G = { scale: scale, noseOff: noseOff, start: startNose, finish: finish, rigTop: rg.top - rr.top,
      R: Math.max(40, Math.min(170, rigW * .1)), rise: (rg.top - rr.top) + U.stackY * scale + 60, rigW: rigW };
    rail.style.left = startNose + 'px'; rail.style.width = (finish - startNose) + 'px';
    flag.style.left = finish + 4 + 'px';
    root.style.setProperty('--edge', (tr.width - right) + 'px');
    rail.querySelectorAll('.fp__tick').forEach(function (t) { t.remove(); });
    [0, 1 / 3, 2 / 3, 1].forEach(function (f, i) {
      if ((i === 1 || i === 2) && finish - startNose < 280) return;   /* pista corta (móvil): solo 0 y la meta */
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

  /* ---------- humo: columna densa y casi vertical ---------- */
  var P = [], POOL = reduce ? 0 : 200, alive = 0, INHERIT = .6;
  function makePool() {
    for (var i = P.length; i < POOL; i++) {
      var c = document.createElementNS(NS, 'circle'); c.setAttribute('r', '50'); c.setAttribute('fill', 'url(#fpPuff' + (i % 3) + ')'); c.style.opacity = '0';
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
  function emit(clock, rigX, sp, big) {
    for (var i = 0; i < P.length; i++) if (!P[i].on) {
      var p = P[i]; p.on = true; alive++;
      p.t0 = clock; p.rx = rigX; p.big = big;
      p.life = big ? 2300 + Math.random() * 900 : 1100 + Math.random() * 500;
      p.x0 = sp[0] + (Math.random() - .5) * G.R * .12; p.y0 = sp[1];
      p.vr = big ? .82 + Math.random() * .3 : .22 + Math.random() * .1;
      p.drift = -G.rigW * (.008 + Math.random() * .03); p.wob = Math.random() * 6.28;
      p.size = big ? .75 + Math.random() * .5 : .35 + Math.random() * .15;
      return;
    }
  }
  function smoke(clock, rigX) {
    for (var i = 0; i < P.length; i++) {
      var p = P[i]; if (!p.on) continue;
      var a = (clock - p.t0) / p.life;
      if (a >= 1) { p.on = false; alive--; p.el.style.opacity = '0'; continue; }
      var rise = G.rise * p.vr * (1 - Math.pow(1 - a, 2.1));                   /* sale con fuerza y se frena arriba */
      var x = p.x0 + (rigX - p.rx) * INHERIT + p.drift * a + Math.sin(a * 3 + p.wob) * G.R * .18 * a;
      var y = p.y0 - rise;
      var sc = G.R * p.size * (.22 + .78 * Math.pow(a, .55)) / 50;
      var op = (a < .05 ? a / .05 : 1) * (a < .5 ? 1 : 1 - Math.pow((a - .5) / .5, 1.4)) * (p.big ? 1 : .8);
      p.el.setAttribute('transform', 'translate(' + x.toFixed(1) + ' ' + y.toFixed(1) + ') scale(' + sc.toFixed(3) + ')');
      p.el.style.opacity = op.toFixed(3);
    }
  }

  /* ---------- pintar un instante ---------- */
  function paint(ms, clock) {
    var k = Math.min(1, ms / DUR), prog = progress(ms), full = k >= 1;
    var nose = G.start + (G.finish - G.start) * prog, x = nose - G.noseOff;
    rig.style.transform = 'translate3d(' + x.toFixed(1) + 'px,0,0)';
    fill.style.setProperty('--p', prog.toFixed(4));
    dist.textContent = String(Math.round(prog * TARGET)).padStart(3, '0');
    var r = full ? 1100 : ms < HOOK ? Math.round(1400 + (ms / HOOK) * 3800) : Math.min(7000, Math.round(6100 + Math.sin(ms / 60) * 280 + prog * 600));
    needle.style.transform = 'rotate(' + (-120 + (r / 7000) * 240).toFixed(1) + 'deg)';
    rpm.textContent = r;
    box.setAttribute('transform', 'translate(' + (prog * U.boxTravel).toFixed(1) + ' 0)');
    pile.setAttribute('transform', 'translate(1452 550) scale(' + (.15 + prog * 1.1).toFixed(3) + ') translate(-1452 -550)');
    var travelled = (nose - G.start) / G.scale;
    wheels.forEach(function (w) { w.setAttribute('transform', 'rotate(' + (travelled / U.wheelR * 57.3 % 360).toFixed(1) + ' ' + w.getAttribute('data-c') + ')'); });
    var lift = !full && prog > .02 && prog < .97 ? 1.2 + 2.4 * Math.max(0, Math.sin(ms / 340)) * (1 - prog * .5) : 0;
    wheelie.setAttribute('transform', 'rotate(' + (-lift).toFixed(2) + ' ' + U.px + ' ' + U.py + ')');
    chip.textContent = full ? 'Full pull!' : prog > 0 ? 'Pulling' : 'Hooked';
    chip.classList.toggle('is-full', full);
    root.classList.toggle('is-full', full);
    root.classList.toggle('is-pulling', prog > 0 && !full && state === 'run');
    /* humo: al enganchar, bocanadas cortas; al jalar, columna densa; al terminar deja de salir y se disipa */
    if (P.length && state === 'run' && clock >= nextPuff) {
      var pulling = ms >= HOOK, sp = stackPoint(x, lift);
      emit(clock, x, sp, pulling);
      if (pulling) emit(clock, x, sp, true);
      if (pulling && ms - HOOK < 150) { emit(clock, x, sp, true); emit(clock, x, sp, true); }
      nextPuff = clock + (pulling ? 30 : 200);
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
  function kick() { if (!reduce && !raf && visible) { last = 0; raf = requestAnimationFrame(loop); } }
  function finish() {
    state = 'done'; root.classList.remove('is-running', 'is-pulling'); ctrl.textContent = 'Pull again';
    if (!reduce) { root.classList.remove('is-strike'); void root.offsetWidth; root.classList.add('is-strike'); }
  }
  function restart() {
    if (reduce) { paint(DUR, 0); return; }
    ms = 0; state = 'run'; nextPuff = 0; root.classList.remove('is-strike', 'is-full'); root.classList.add('is-running');
    ctrl.textContent = 'Pause'; kick();
  }
  ctrl.addEventListener('click', function () {
    if (reduce) return;
    if (state === 'run') { state = 'paused'; root.classList.remove('is-running', 'is-pulling'); ctrl.textContent = 'Resume'; return; }
    if (state === 'paused') { state = 'run'; root.classList.add('is-running'); ctrl.textContent = 'Pause'; kick(); return; }
    restart();
  });
  function applyReduce() {
    ctrl.hidden = reduce;
    if (reduce) { state = 'done'; ms = DUR; root.classList.remove('is-running', 'is-pulling', 'is-strike'); paint(DUR, 0); }
  }
  var onRm = function (e) { reduce = e.matches; if (!reduce) { POOL = 200; makePool(); applyReduce(); restart(); } else applyReduce(); };
  if (rmq.addEventListener) rmq.addEventListener('change', onRm); else if (rmq.addListener) rmq.addListener(onRm);

  measure();
  if (reduce) applyReduce();
  else restart();
  if ('IntersectionObserver' in window) new IntersectionObserver(function (e) { visible = e[0].isIntersecting; if (visible) kick(); }).observe(root);
  var rt; addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(function () { measure(); paint(Math.min(ms, DUR), clock); }, 80); });
})();
