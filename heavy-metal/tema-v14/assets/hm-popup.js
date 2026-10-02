/* HM v14 · The Evil List pop-up with a scratch-off code (snippets/hm-popup.liquid).
   Opens once per visit after the delay, at 50% scroll, or on exit intent (desktop), whichever comes first.
   Closed: hidden for N days (localStorage). Signed up: never again. Storage is optional (try/catch). */
(function () {
  var pop = document.querySelector('[data-hm-pop]');
  if (!pop || pop.hmInit) return;
  pop.hmInit = true;

  var scrim = document.querySelector('[data-hm-pop-scrim]');
  var form = pop.querySelector('form[data-hm-pop-form]');
  var email = pop.querySelector('#hm-pop-email');
  var err = pop.querySelector('[data-hm-pop-err]');
  var msg = pop.querySelector('[data-hm-pop-msg]');
  var codeEl = pop.querySelector('[data-hm-pop-code]');
  var code = codeEl ? codeEl.textContent.trim() : '';
  var KEY_CLOSED = 'hm_pop_closed', KEY_JOINED = 'hm_pop_joined';
  var DAY = 86400000;
  var days = parseInt(pop.getAttribute('data-days'), 10) || 14;
  var delay = (parseInt(pop.getAttribute('data-delay'), 10) || 10) * 1000;
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia && matchMedia('(hover: hover) and (pointer: fine)').matches;
  var isOpen = false, triggered = false, lastFocus = null, timer = null, revealed = false;

  function get(k) { try { return window.localStorage.getItem(k); } catch (e) { return null; } }
  function set(k, v) { try { window.localStorage.setItem(k, v); } catch (e) {} }

  function step(name) {
    [].forEach.call(pop.querySelectorAll('[data-hm-pop-step]'), function (s) { s.hidden = s.getAttribute('data-hm-pop-step') !== name; });
    pop.setAttribute('aria-labelledby', name === 'scratch' ? 'hm-pop-t2' : 'hm-pop-t');
    if (name === 'scratch') { pop.removeAttribute('aria-describedby'); }
  }

  function focusables() {
    return [].filter.call(pop.querySelectorAll('a[href], button:not([disabled]), input:not([type="hidden"]):not([disabled]), [tabindex]:not([tabindex="-1"])'), function (el) {
      return el.offsetParent !== null || el.getClientRects().length > 0;
    });
  }

  /* another dialog or drawer is open, or the visitor is typing: try again later */
  function busy() {
    var a = document.activeElement;
    if (a && /^(INPUT|TEXTAREA|SELECT)$/.test(a.tagName) && !pop.contains(a)) return true;
    var others = document.querySelectorAll('[role="dialog"], [aria-modal="true"], .drawer, .mnav, .search');
    for (var i = 0; i < others.length; i++) {
      var o = others[i];
      if (o === pop || pop.contains(o) || o.hidden) continue;
      if (o.getClientRects().length && getComputedStyle(o).visibility !== 'hidden' && getComputedStyle(o).display !== 'none') return true;
    }
    return false;
  }

  function open(which) {
    if (isOpen) return;
    isOpen = true;
    stopTriggers();
    step(which || 'join');
    lastFocus = document.activeElement;
    pop.hidden = false;
    if (scrim) scrim.hidden = false;
    document.documentElement.style.overflow = 'hidden';
    document.addEventListener('keydown', onKey, true);
    if (which === 'scratch') { showScratch(true); return; }
    var target = finePointer && email ? email : pop;
    setTimeout(function () { target.focus({ preventScroll: true }); }, 30);
  }

  function close() {
    if (!isOpen) return;
    isOpen = false;
    pop.hidden = true;
    if (scrim) scrim.hidden = true;
    document.documentElement.style.overflow = '';
    document.removeEventListener('keydown', onKey, true);
    if (!get(KEY_JOINED)) set(KEY_CLOSED, String(Date.now()));
    if (lastFocus && document.contains(lastFocus) && lastFocus.focus) lastFocus.focus({ preventScroll: true });
  }

  function onKey(e) {
    if (!isOpen) return;
    if (e.key === 'Escape') { e.preventDefault(); e.stopPropagation(); close(); return; }
    if (e.key !== 'Tab') return;
    var f = focusables(); if (!f.length) { e.preventDefault(); pop.focus(); return; }
    var first = f[0], last = f[f.length - 1];
    if (e.shiftKey && (document.activeElement === first || document.activeElement === pop)) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    else if (!pop.contains(document.activeElement)) { e.preventDefault(); first.focus(); }
  }

  pop.addEventListener('click', function (e) {
    if (e.target.closest('[data-hm-pop-close]')) close();
    else if (e.target.closest('[data-hm-pop-reveal]')) reveal(true);
    else if (e.target.closest('[data-hm-pop-copy]')) copy();
  });
  if (scrim) scrim.addEventListener('click', close);

  /* ---------- triggers ---------- */
  function fire() {
    if (triggered || isOpen) return;
    if (busy()) { clearTimeout(timer); timer = setTimeout(fire, 4000); return; }
    triggered = true;
    open('join');
  }
  function onScroll() {
    var max = document.documentElement.scrollHeight - window.innerHeight;
    if (max > 200 && window.scrollY / max >= 0.5) fire();
  }
  function onOut(e) { if (!e.relatedTarget && e.clientY <= 0) fire(); }
  function stopTriggers() {
    clearTimeout(timer);
    window.removeEventListener('scroll', onScroll);
    document.removeEventListener('mouseout', onOut);
  }
  function startTriggers() {
    timer = setTimeout(fire, delay);
    window.addEventListener('scroll', onScroll, { passive: true });
    if (finePointer && window.innerWidth > 760) document.addEventListener('mouseout', onOut);
  }

  /* ---------- signup ---------- */
  function joined() {
    set(KEY_JOINED, '1');
    step('scratch');
    showScratch(false);
  }
  function showError(t) {
    if (err) err.textContent = t;
    if (email) { email.setAttribute('aria-invalid', 'true'); email.focus(); }
  }

  if (form) form.addEventListener('submit', function (e) {
    var ok = email && email.value.trim() !== '' && email.checkValidity();
    if (!ok) { e.preventDefault(); showError('That email looks off. Fix it and you’re in.'); return; }
    if (!window.fetch || !window.FormData) return; /* normal post, handled after reload */
    e.preventDefault();
    email.setAttribute('aria-invalid', 'false');
    if (err) err.textContent = '';
    var btn = form.querySelector('[data-hm-pop-submit]');
    if (btn) btn.setAttribute('aria-busy', 'true');
    fetch(form.action, { method: 'POST', body: new FormData(form), credentials: 'same-origin', headers: { Accept: 'text/html' } })
      .then(function (r) {
        if (/\/challenge/.test(r.url)) { set(KEY_CLOSED, ''); form.submit(); return null; }
        if (/customer_posted=true/.test(r.url)) return { ok: true };
        return r.text().then(function (html) {
          var doc = new DOMParser().parseFromString(html, 'text/html');
          var same = doc.getElementById('HmPopupForm');
          var m = same && same.querySelector('[data-hm-pop-err]');
          var t = m ? m.textContent.trim() : '';
          if (t && /taken|already/i.test(t)) return { ok: true };
          return { ok: !t && r.ok && !(same && same.querySelector('[data-hm-pop-failed]')), msg: t || 'Something went wrong. Try again.' };
        });
      })
      .then(function (res) {
        if (btn) btn.removeAttribute('aria-busy');
        if (!res) return;
        if (res.ok) joined(); else showError(res.msg);
      })
      .catch(function () {
        if (btn) btn.removeAttribute('aria-busy');
        showError('Something went wrong. Check your connection and try again.');
      });
  });

  /* ---------- scratch card ---------- */
  var box = pop.querySelector('[data-hm-scratch]');
  var canvas = pop.querySelector('[data-hm-scratch-canvas]');
  var under = pop.querySelector('[data-hm-scratch-under]');
  var ctx = null, dpr = 1, moves = 0, drawing = false, lastPt = null;

  function css(name, fb) { var v = getComputedStyle(document.documentElement).getPropertyValue(name).trim(); return v || fb; }

  function paintCover() {
    if (!canvas || !canvas.getContext) return false;
    var w = box.clientWidth, h = box.clientHeight;
    if (!w || !h) return false;
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr);
    ctx = canvas.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.globalCompositeOperation = 'source-over';
    ctx.fillStyle = css('--ink', '#1C1B19');
    ctx.fillRect(0, 0, w, h);
    ctx.strokeStyle = 'rgba(255,255,255,.05)'; ctx.lineWidth = 1;
    for (var x = -h; x < w; x += 12) { ctx.beginPath(); ctx.moveTo(x, h); ctx.lineTo(x + h, 0); ctx.stroke(); }
    ctx.fillStyle = css('--night-ink', '#F2F0E9');
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.font = '700 18px Archivo, "Arial Narrow", Arial, sans-serif';
    ctx.fillText('SCRATCH HERE', w / 2, h / 2 - 8);
    ctx.font = '400 12px Archivo, Arial, sans-serif';
    ctx.fillStyle = 'rgba(242,240,233,.7)';
    ctx.fillText('Drag your finger or mouse', w / 2, h / 2 + 16);
    ctx.globalCompositeOperation = 'destination-out';
    return true;
  }

  function pt(e) { var r = canvas.getBoundingClientRect(); return { x: e.clientX - r.left, y: e.clientY - r.top }; }
  function scratchTo(p) {
    if (!ctx) return;
    ctx.lineWidth = 34; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    ctx.beginPath();
    var a = lastPt || p;
    ctx.moveTo(a.x, a.y); ctx.lineTo(p.x + 0.01, p.y);
    ctx.stroke();
    lastPt = p;
    if (++moves % 10 === 0) check();
  }
  function check() {
    try {
      var d = ctx.getImageData(0, 0, canvas.width, canvas.height).data, clear = 0, n = 0;
      for (var i = 3; i < d.length; i += 64) { n++; if (d[i] < 128) clear++; }
      if (n && clear / n > 0.45) reveal(false);
    } catch (e) { reveal(false); }
  }

  if (canvas) {
    canvas.addEventListener('pointerdown', function (e) {
      if (revealed) return;
      drawing = true; lastPt = null;
      try { canvas.setPointerCapture(e.pointerId); } catch (x) {}
      scratchTo(pt(e));
      e.preventDefault();
    });
    canvas.addEventListener('pointermove', function (e) { if (drawing && !revealed) scratchTo(pt(e)); });
    ['pointerup', 'pointercancel', 'pointerleave'].forEach(function (t) {
      canvas.addEventListener(t, function () { if (drawing) { drawing = false; lastPt = null; check(); } });
    });
  }

  function showScratch(fromReload) {
    revealed = false; moves = 0;
    if (box) box.classList.remove('is-done');
    var h2 = pop.querySelector('#hm-pop-t2');
    requestAnimationFrame(function () {
      if (!paintCover()) reveal(false);
      if (h2) h2.focus({ preventScroll: true });
    });
    if (fromReload && msg) msg.textContent = '';
  }

  function reveal(byButton) {
    if (revealed) return;
    revealed = true;
    if (box) box.classList.add('is-done');
    if (under) under.removeAttribute('aria-hidden');
    var rb = pop.querySelector('[data-hm-pop-reveal]'), cb = pop.querySelector('[data-hm-pop-copy]'), sh = pop.querySelector('[data-hm-pop-shop]');
    if (rb) rb.hidden = true;
    if (cb) cb.hidden = false;
    if (sh) sh.hidden = false;
    if (msg) msg.textContent = 'Your code: ' + code + '. Confirm your email first, then it works.';
    if (cb && (byButton || reduce)) cb.focus({ preventScroll: true });
    else if (cb && document.activeElement && pop.contains(document.activeElement) && document.activeElement.hidden) cb.focus({ preventScroll: true });
  }

  function copied(ok) { if (msg) msg.textContent = ok ? 'Copied. Go spend it.' : 'Copy failed. The code is ' + code + '.'; }
  function copy() {
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(code).then(function () { copied(true); }, function () { copied(legacyCopy()); });
    } else copied(legacyCopy());
  }
  function legacyCopy() {
    try {
      var t = document.createElement('textarea');
      t.value = code; t.setAttribute('readonly', ''); t.style.position = 'fixed'; t.style.opacity = '0';
      pop.appendChild(t); t.select();
      var ok = document.execCommand('copy');
      pop.removeChild(t);
      return ok;
    } catch (e) { return false; }
  }

  /* ---------- start ---------- */
  var cameBack = location.hash === '#HmPopupForm';
  if (cameBack && pop.querySelector('[data-hm-pop-posted]')) {
    set(KEY_JOINED, '1');
    try { history.replaceState(null, '', location.pathname); } catch (e) {}
    open('scratch');
  } else if (cameBack && pop.querySelector('[data-hm-pop-failed]')) {
    open('join');
    if (email) email.setAttribute('aria-invalid', 'true');
  } else {
    var closedAt = parseInt(get(KEY_CLOSED), 10);
    var snoozed = closedAt && Date.now() - closedAt < days * DAY;
    if (!get(KEY_JOINED) && !snoozed) startTriggers();
  }

  window.HMPopup = { open: function () { open('join'); }, close: close };
})();
