/* Heavy Metal quick add + card helpers + Notify me.
   - [data-arw] on product cards: front / back / color views.
   - [data-quick="handle"]: adds the only variant, or opens the size sheet built from /products/<handle>.js.
   - [data-notify="handle"]: opens the Notify me dialog (form 'customer', tags notify,notify-<handle>).
   - form[data-hm-notify-form]: any notify / Evil List customer form is sent in the background with fetch. */
(function () {
  'use strict';
  if (window.HMQuickAdd) return;

  /* overlays: window.HMOverlay is the alias of HM.open/close from hm-core.js (one dialog at a time) */
  var OV = {
    open: function (el, o) { if (window.HMOverlay) window.HMOverlay.open(el, o); },
    close: function (el, k) { if (window.HMOverlay) window.HMOverlay.close(el, k); },
    isOpen: function (el) { return !!(el && window.HMOverlay && window.HMOverlay.isOpen(el)); }
  };

  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function sheet() { return document.querySelector('[data-hm-qsheet]'); }
  function root() { var s = sheet(), r = (s && s.getAttribute('data-root')) || '/'; return r.replace(/\/$/, ''); }
  function money(c) { return window.HMCart ? window.HMCart.money(c) : '$' + (c / 100).toFixed(2).replace(/\.00$/, ''); }

  function addToCart(items, trigger, showError) {
    if (window.HMCart) return window.HMCart.add(items, { returnFocus: trigger, showError: showError });
    /* cart drawer missing: classic add, then go to the cart page */
    return fetch(root() + '/cart/add.js', { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify({ items: items }) })
      .then(function (r) { return r.json().then(function (j) { if (!r.ok || j.status) throw new Error(j.description || 'Could not add it. Try again.'); location.href = root() + '/cart'; }); });
  }

  /* ---------- card arrows ---------- */
  document.addEventListener('click', function (e) {
    var a = e.target.closest('[data-arw]'); if (!a) return;
    e.preventDefault();
    var card = a.closest('[data-hm-card], .card'); if (!card) return;
    var sl = card.querySelectorAll('.card__slide'), dots = card.querySelectorAll('.card__dots i'), cur = 0;
    [].forEach.call(sl, function (x, i) { if (!x.hidden) cur = i; });
    var n = (cur + Number(a.getAttribute('data-arw')) + sl.length) % sl.length;
    [].forEach.call(sl, function (x, i) { x.hidden = i !== n; });
    [].forEach.call(dots, function (d, i) { d.className = i === n ? 'on' : ''; });
  });

  /* ---------- quick add ---------- */
  var current = null, trigger = null, cache = {};
  function getProduct(handle) {
    if (cache[handle]) return Promise.resolve(cache[handle]);
    return fetch(root() + '/products/' + encodeURIComponent(handle) + '.js', { headers: { Accept: 'application/json' } })
      .then(function (r) { if (!r.ok) throw new Error('Could not load sizes.'); return r.json(); })
      .then(function (p) { cache[handle] = p; return p; });
  }
  function optName(o) { return (typeof o === 'string' ? o : o.name) || ''; }

  function fill(p) {
    var s = sheet();
    var names = (p.options || []).map(optName);
    var si = -1, ci = -1;
    names.forEach(function (n, i) { if (/size/i.test(n)) si = i; else if (/colou?r/i.test(n)) ci = i; });
    var base = p.variants.filter(function (v) { return v.available; })[0] || p.variants[0];
    var label = s.querySelector('#hm-qs-label');
    s.querySelector('#hm-qs-name').textContent = p.title;
    s.querySelector('[data-hm-qs-price]').textContent = p.price_varies ? 'From ' + money(p.price_min) : money(p.price);
    s.querySelector('[data-hm-qs-color]').textContent = ci > -1 ? base.options[ci] : 'One color';
    s.querySelector('[data-hm-qs-more]').href = (p.url || root() + '/products/' + p.handle);
    var buttons;
    if (si > -1) {
      label.textContent = 'Select a size';
      var values = (p.options[si].values || []).slice();
      if (!values.length) p.variants.forEach(function (v) { if (values.indexOf(v.options[si]) < 0) values.push(v.options[si]); });
      buttons = values.map(function (val) {
        var v = p.variants.filter(function (x) {
          return x.options.every(function (o, i) { return i === si ? o === val : o === base.options[i]; });
        })[0];
        var off = !v || !v.available;
        return '<button type="button" data-qs-variant="' + (v ? v.id : '') + '"' + (off ? ' disabled aria-label="' + esc(val) + ', sold out"' : '') + '>' + esc(val) + '</button>';
      });
    } else {
      label.textContent = 'Select an option';
      buttons = p.variants.map(function (v) {
        return '<button type="button" data-qs-variant="' + v.id + '"' + (v.available ? '' : ' disabled aria-label="' + esc(v.title) + ', sold out"') + '>' + esc(v.title) + '</button>';
      });
    }
    var box = s.querySelector('[data-hm-qs-sizes]');
    box.innerHTML = buttons.join('');
    box.removeAttribute('aria-busy');
    return box.querySelector('button:not(:disabled)');
  }

  function openSheet(handle, btn) {
    var s = sheet(); if (!s) { if (btn.getAttribute('data-url')) location.href = btn.getAttribute('data-url'); return; }
    trigger = btn; current = handle;
    s.querySelector('[data-hm-qs-err]').textContent = '';
    btn.setAttribute('aria-busy', 'true');
    getProduct(handle).then(function (p) {
      btn.removeAttribute('aria-busy');
      if (current !== handle) return;
      var first = fill(p);
      OV.open(s, { scrim: document.querySelector('[data-hm-qs-scrim]'), focus: first || s.querySelector('[data-hm-qs-close]'), returnFocus: btn });
    }).catch(function () {
      btn.removeAttribute('aria-busy');
      if (btn.getAttribute('data-url')) location.href = btn.getAttribute('data-url');
    });
  }
  function closeSheet(keepFocus) { var s = sheet(); if (s) OV.close(s, keepFocus); }

  document.addEventListener('click', function (e) {
    var q = e.target.closest('[data-quick]');
    if (q) {
      e.preventDefault();
      var vid = q.getAttribute('data-variant-id');
      if (vid) {
        if (q.getAttribute('aria-busy') === 'true') return;
        q.setAttribute('aria-busy', 'true');
        addToCart([{ id: Number(vid), quantity: 1 }], q, true)
          .catch(function () {})
          .then(function () { q.removeAttribute('aria-busy'); });
      } else openSheet(q.getAttribute('data-quick'), q);
      return;
    }
    var s = sheet(); if (!s) return;
    if (e.target.closest('[data-hm-qs-close]') || e.target.closest('[data-hm-qs-scrim]')) { closeSheet(); return; }
    var b = e.target.closest('[data-qs-variant]');
    if (b && s.contains(b) && !b.disabled) {
      var id = Number(b.getAttribute('data-qs-variant'));
      [].forEach.call(s.querySelectorAll('[data-qs-variant]'), function (x) { x.disabled = true; });
      b.setAttribute('aria-busy', 'true');
      var ret = trigger;
      addToCart([{ id: id, quantity: 1 }], ret).then(function () {
        closeSheet(true);
        var drawer = document.querySelector('[data-hm-cart]');
        var open = drawer && !drawer.hidden;
        var usable = ret && document.contains(ret) && ret.getClientRects().length && !ret.closest('[hidden]');
        if (usable && (!open || drawer.contains(ret))) ret.focus({ preventScroll: true });
        else if (open) { var c = drawer.querySelector('[data-hm-cart-close]'); if (c) c.focus(); }
      }).catch(function (err) {
        s.querySelector('[data-hm-qs-err]').textContent = err.message;
        b.removeAttribute('aria-busy');
        delete cache[current];
        getProduct(current).then(fill);
      });
    }
  });

  /* ---------- Notify me dialog ---------- */
  function nfy() { return document.querySelector('[data-hm-nfy]'); }
  document.addEventListener('click', function (e) {
    var n = e.target.closest('[data-notify]');
    var m = nfy();
    if (n && m) {
      e.preventDefault();
      var handle = n.getAttribute('data-notify'), st = n.getAttribute('data-notify-state') || 'soon';
      var name = n.getAttribute('data-name') || '';
      m.querySelector('[data-hm-nfy-k]').textContent = st === 'soldout' ? 'Sold out' : 'Coming soon';
      m.querySelector('#hm-nfy-t').textContent = name;
      m.querySelector('[data-hm-nfy-d]').textContent = st === 'soldout' ? 'We will email you if it comes back. One email, no spam.' : 'We will email you the moment it drops. One email, no spam.';
      m.querySelector('[data-hm-nfy-tags]').value = 'notify,notify-' + handle;
      var more = m.querySelector('[data-hm-nfy-more]'); if (n.getAttribute('data-url')) { more.href = n.getAttribute('data-url'); more.hidden = false; } else more.hidden = true;
      resetForm(m.querySelector('form'));
      if (OV.isOpen(sheet())) closeSheet(true);
      OV.open(m, { scrim: document.querySelector('[data-hm-nfy-scrim]'), focus: m.querySelector('input[type="email"]'), returnFocus: n });
      return;
    }
    if (m && (e.target.closest('[data-hm-nfy-close]') || e.target.closest('[data-hm-nfy-scrim]'))) OV.close(m);
  });

  /* ---------- background submit for notify / Evil List forms ---------- */
  function resetForm(form) {
    if (!form) return;
    var f = form.querySelector('[data-hm-form-fields]'), ok = form.querySelector('[data-hm-form-ok]'), er = form.querySelector('[data-hm-form-errors]');
    if (f) f.hidden = false; if (ok) ok.hidden = true; if (er) er.textContent = '';
    var em = form.querySelector('input[type="email"]'); if (em) { em.value = ''; em.removeAttribute('aria-invalid'); }
  }
  document.addEventListener('submit', function (e) {
    var form = e.target.closest('form[data-hm-notify-form]'); if (!form) return;
    var em = form.querySelector('input[type="email"]'), er = form.querySelector('[data-hm-form-errors]'), ok = form.querySelector('[data-hm-form-ok]');
    var valid = em && em.value.trim() !== '' && em.checkValidity();
    if (!valid) {
      e.preventDefault();
      if (em) { em.setAttribute('aria-invalid', 'true'); em.focus(); }
      if (er) er.textContent = 'Enter a valid email so we can let you know.';
      return;
    }
    if (!window.fetch || !window.FormData) return;
    e.preventDefault();
    em.setAttribute('aria-invalid', 'false');
    var btn = form.querySelector('[type="submit"]'); if (btn) btn.setAttribute('aria-busy', 'true');
    if (er) er.textContent = '';
    fetch(form.action, { method: 'POST', body: new FormData(form), credentials: 'same-origin', headers: { Accept: 'text/html' } })
      .then(function (r) {
        if (/\/challenge/.test(r.url)) { form.removeAttribute('data-hm-notify-form'); form.submit(); return null; }
        if (/customer_posted=true/.test(r.url)) return { ok: true };
        return r.text().then(function (html) {
          var doc = new DOMParser().parseFromString(html, 'text/html');
          var same = form.id && doc.getElementById(form.id);
          var msg = same && same.querySelector('[data-hm-form-errors]');
          var t = msg ? msg.textContent.trim() : '';
          return { ok: !t && r.ok && !same, msg: t || 'Something went wrong. Try again.' };
        });
      })
      .then(function (res) {
        if (btn) btn.removeAttribute('aria-busy');
        if (!res) return;
        if (res.ok) {
          var f = form.querySelector('[data-hm-form-fields]'); if (f) f.hidden = true;
          if (ok) { ok.hidden = false; ok.setAttribute('tabindex', '-1'); ok.focus(); }
        } else if (er) { er.textContent = res.msg; em.focus(); }
      })
      .catch(function () { if (btn) btn.removeAttribute('aria-busy'); if (er) er.textContent = 'Something went wrong. Check your connection and try again.'; });
  });

  window.HMQuickAdd = { open: openSheet, close: closeSheet };
})();
