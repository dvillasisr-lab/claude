/* Heavy Metal cart drawer (needs hm-core.js for HM.open/close): AJAX cart (/cart.js, /cart/add.js, /cart/change.js, /cart/update.js).
   Free shipping tiers, Add to your order, Crew Pack upgrade, Feed The Beast tip, discount code, order note.
   Public API: window.HMCart.add(items) / .refresh() / .open() / .close() ; events: hm:cart:open, hm:cart:updated. */
(function () {
  'use strict';
  if (window.HMCart) return;

  /* overlays: window.HMOverlay is the alias of HM.open/close from hm-core.js (one dialog at a time) */
  var OV = {
    open: function (el, o) { if (window.HMOverlay) window.HMOverlay.open(el, o); },
    close: function (el, k) { if (window.HMOverlay) window.HMOverlay.close(el, k); },
    isOpen: function (el) { return !!(el && window.HMOverlay && window.HMOverlay.isOpen(el)); }
  };

  var drawer, scrim, state = { cart: null, busy: false };
  var $ = function (sel, root) { return (root || drawer).querySelector(sel); };
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }

  /* ---------- money ---------- */
  function money(cents) {
    var fmt = (drawer && drawer.getAttribute('data-money-format')) || '${{amount}}';
    cents = Math.round(Number(cents) || 0);
    function delim(n, prec, th, dec) {
      var parts = (n / 100).toFixed(prec).split('.');
      return parts[0].replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1' + th) + (parts[1] ? dec + parts[1] : '');
    }
    return fmt.replace(/\{\{\s*(\w+)\s*\}\}/, function (m, k) {
      if (k === 'amount_no_decimals') return delim(cents, 0, ',', '.');
      if (k === 'amount_with_comma_separator') return delim(cents, 2, '.', ',');
      if (k === 'amount_no_decimals_with_comma_separator') return delim(cents, 0, '.', ',');
      if (k === 'amount_with_apostrophe_separator') return delim(cents, 2, "'", '.');
      return delim(cents, 2, ',', '.');
    }).replace(/\.00(?!\d)/, '');
  }
  function rate() { var r = window.Shopify && Shopify.currency && parseFloat(Shopify.currency.rate); return r > 0 ? r : 1; }
  function threshold(attr) { var v = parseFloat(drawer.getAttribute(attr)); return v > 0 ? Math.round(v * 100 * rate()) : 0; }
  function root() { var r = drawer.getAttribute('data-root') || '/'; return r.replace(/\/$/, ''); }
  function url(path) { return root() + path; }

  /* ---------- requests ---------- */
  function req(path, body) {
    return fetch(url(path), {
      method: body ? 'POST' : 'GET',
      headers: body ? { 'Content-Type': 'application/json', Accept: 'application/json' } : { Accept: 'application/json' },
      body: body ? JSON.stringify(body) : undefined,
      credentials: 'same-origin'
    }).then(function (r) {
      return r.json().catch(function () {
        /* not JSON: a bot check, the password page or an outage. Never show the parser error. */
        var e = new Error('Something went wrong. Try again.'); e.notJson = true; e.status = r.status; throw e;
      }).then(function (j) {
        if (!r.ok || j.status) throw new Error(j.description || j.message || 'Something went wrong. Try again.');
        return j;
      });
    });
  }
  function getCart() { return req('/cart.js'); }

  /* ---------- helpers on cart data ---------- */
  function tipId() { return Number(drawer.getAttribute('data-tip-product')) || 0; }
  function isTip(item) { return tipId() && item.product_id === tipId(); }
  function products(cart) { return cart.items.filter(function (i) { return !isTip(i); }); }
  function itemCount(cart) { return products(cart).reduce(function (n, i) { return n + i.quantity; }, 0); }
  function img(src, w) { if (!src) return ''; return src + (src.indexOf('?') > -1 ? '&' : '?') + 'width=' + w; }
  function isTee(i) { var t = (i.product_type || '') + ' ' + (i.product_title || ''); return /\btee\b|t-shirt|\bshirt\b/i.test(t) && !/sweat/i.test(t); }

  /* ---------- render ---------- */
  function render(cart) {
    state.cart = cart;
    var n = itemCount(cart), list = $('[data-hm-lines]');
    var tip = cart.items.filter(isTip)[0];

    /* count in header and drawer */
    [].forEach.call(document.querySelectorAll('[data-hm-cart-count]'), function (c) { c.textContent = n; c.setAttribute('data-n', n); c.hidden = false; });
    [].forEach.call(document.querySelectorAll('[data-hm-cart-open]'), function (b) { b.setAttribute('aria-label', 'Cart, ' + n + (n === 1 ? ' item' : ' items')); });
    $('[data-hm-cart-drawer-count]').textContent = n;

    /* lines */
    list.innerHTML = cart.items.map(function (i) {
      if (isTip(i)) {
        return '<li class="line" data-key="' + esc(i.key) + '" data-tip-line>' +
          '<span class="thumb beast__can" aria-hidden="true"><svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M6 7h10l3 3v10H6z"/><path d="M9 7V4h4v3M9 12l6 5M15 12l-6 5"/></svg></span>' +
          '<div><p class="line__n">Feed The Beast</p><p class="line__v">Fuel tip for the crew</p><button type="button" class="line__rm" data-rm>Remove<span class="vh"> fuel tip</span></button></div>' +
          '<p class="num line__price">' + money(i.final_line_price) + '</p></li>';
      }
      var variant = i.product_has_only_default_variant ? '' : (i.variant_title || '');
      var props = i.properties ? Object.keys(i.properties).filter(function (k) { return k.charAt(0) !== '_' && i.properties[k]; }).map(function (k) { return esc(k) + ': ' + esc(i.properties[k]); }).join('<br>') : '';
      var disc = (i.line_level_discount_allocations || []).map(function (d) { return esc(d.discount_application.title) + ' (−' + money(d.amount) + ')'; }).join('<br>');
      var orig = i.original_line_price > i.final_line_price ? '<s>' + money(i.original_line_price) + '</s>' : '';
      return '<li class="line" data-key="' + esc(i.key) + '" data-product="' + i.product_id + '">' +
        '<a class="thumb" href="' + esc(i.url) + '" tabindex="-1" aria-hidden="true">' + (i.image ? '<img class="photo" src="' + esc(img(i.image, 160)) + '" alt="" width="72" height="90" loading="lazy">' : '') + '</a>' +
        '<div><p class="line__n"><a href="' + esc(i.url) + '" style="text-decoration:none">' + esc(i.product_title) + '</a></p>' +
        (variant ? '<p class="line__v">' + esc(variant) + '</p>' : '<p class="line__v"></p>') +
        (props ? '<p class="line__disc">' + props + '</p>' : '') + (disc ? '<p class="line__disc">' + disc + '</p>' : '') +
        '<div class="qty" role="group" aria-label="Quantity of ' + esc(i.product_title) + '"><button type="button" data-q="-1" aria-label="Decrease quantity">−</button><span class="num" aria-live="polite">' + i.quantity + '</span><button type="button" data-q="1" aria-label="Increase quantity">+</button></div>' +
        '<button type="button" class="line__rm" data-rm>Remove<span class="vh"> ' + esc(i.product_title) + '</span></button></div>' +
        '<p class="num line__price">' + orig + money(i.final_line_price) + '</p></li>';
    }).join('');

    $('[data-hm-cart-empty]').hidden = n > 0;
    $('[data-hm-cart-foot]').hidden = n === 0;
    $('[data-hm-discount-wrap]').hidden = n === 0;
    $('[data-hm-note-wrap]').hidden = n === 0;
    var note = $('[data-hm-note]'); if (note && document.activeElement !== note) note.value = cart.note || '';

    /* totals and cart discounts */
    $('[data-hm-cart-total]').textContent = money(cart.total_price);
    $('[data-hm-cart-discounts]').innerHTML = (cart.cart_level_discount_applications || []).map(function (d) {
      return '<p class="hm-cart__disc"><span>' + esc(d.title) + '</span><span class="num">−' + money(d.total_allocated_amount) + '</span></p>';
    }).join('');
    $('[data-hm-codes]').innerHTML = (cart.discount_codes || []).filter(function (c) { return c.applicable; }).map(function (c) {
      return '<li><button type="button" data-rm-code="' + esc(c.code) + '" aria-label="Remove discount ' + esc(c.code) + '">' + esc(c.code) + ' <span aria-hidden="true">×</span></button></li>';
    }).join('');

    /* free shipping tiers */
    var free = threshold('data-free'), gift = threshold('data-gift'), total = cart.total_price;
    var tiers = $('[data-hm-tiers]');
    if (tiers) {
      tiers.hidden = n === 0 || !free;
      var max = gift > free ? gift : free;
      var stopFree = $('[data-hm-stop="free"]');
      if (stopFree) stopFree.style.left = (gift > free ? Math.round(free / max * 100) : 100) + '%';
      $('[data-hm-tiers-fill]').style.width = Math.min(100, max ? total / max * 100 : 0) + '%';
      var label = (drawer.getAttribute('data-gift-label') || 'Free sticker').toLowerCase();
      var msg;
      if (total < free) msg = 'You are <b>' + money(free - total) + '</b> away from <b>free US shipping</b>';
      else if (gift > free && total < gift) msg = 'Free US shipping unlocked. <b>' + money(gift - total) + '</b> more for a <b>' + esc(label) + '</b>';
      else msg = '<b>You unlocked free US shipping' + (gift > free ? ' and a ' + esc(label) : '') + '.</b>';
      $('[data-hm-tiers-msg]').innerHTML = msg;
    }

    /* Crew Pack upgrade: a tee is in the cart and the cap (or the pack) is not */
    var up = $('[data-hm-upgrade]');
    if (up) {
      var capId = Number(drawer.getAttribute('data-cap-product')), packId = Number(drawer.getAttribute('data-pack-product'));
      var items = products(cart);
      var hasTee = items.some(isTee), hasCap = items.some(function (i) { return i.product_id === capId || i.product_id === packId; });
      up.hidden = !hasTee || hasCap;
    }

    /* Add to your order: never suggest what is already in the cart; hidden with an empty cart */
    var ad = $('[data-hm-addons]');
    if (ad) {
      var inCart = cart.items.map(function (i) { return String(i.product_id); }), vis = 0;
      [].forEach.call(ad.querySelectorAll('[data-addon-product]'), function (a) {
        var hide = inCart.indexOf(a.getAttribute('data-addon-product')) > -1; a.hidden = hide; if (!hide) vis++;
      });
      ad.hidden = n === 0 || vis === 0;
    }

    /* Feed The Beast: only with products in the cart and still below free shipping (or a tip already chosen) */
    var beast = $('[data-hm-beast]');
    if (beast) {
      var below = free && (total - (tip ? tip.final_line_price : 0)) < free;
      beast.hidden = n === 0 || !(below || tip);
      [].forEach.call(beast.querySelectorAll('[data-tip]'), function (b) {
        b.setAttribute('aria-pressed', tip && String(tip.variant_id) === b.getAttribute('data-tip') ? 'true' : 'false');
      });
    }

    document.dispatchEvent(new CustomEvent('hm:cart:updated', { detail: { cart: cart, count: n } }));
    return cart;
  }

  /* the tip never stays alone: if no products remain, remove it */
  function sweep(cart) {
    var tips = cart.items.filter(isTip);
    if (tips.length && !products(cart).length) {
      var updates = {}; tips.forEach(function (t) { updates[t.key] = 0; });
      return req('/cart/update.js', { updates: updates });
    }
    return Promise.resolve(cart);
  }

  function refresh() { return getCart().then(sweep).then(render); }
  function setErr(t) { var e = $('[data-hm-cart-error]'); if (e) e.textContent = t || ''; }
  function say(t) { var s = $('[data-hm-cart-status]'); if (s) { s.textContent = ''; setTimeout(function () { s.textContent = t; }, 50); } }

  /* ---------- open / close ---------- */
  function open(opts) {
    if (!drawer) return;
    opts = opts || {};
    if (!OV.isOpen(drawer)) OV.open(drawer, { scrim: scrim, focus: $('[data-hm-cart-close]'), returnFocus: opts.returnFocus || opts.trigger, trigger: opts.trigger });
  }
  function close() { if (drawer) OV.close(drawer); }

  /* ---------- add ---------- */
  function add(items, opts) {
    opts = opts || {};
    var body = Array.isArray(items) ? { items: items } : items;
    setErr('');
    return req('/cart/add.js', body).then(function () {
      /* added; if the cart can't be read back, show the cart page instead of an error */
      return refresh().catch(function () { location.href = url('/cart'); return new Promise(function () {}); });
    }).then(function (cart) {
      if (opts.open !== false) open({ returnFocus: opts.returnFocus });
      var n = itemCount(cart);
      say('Added to cart. Cart has ' + n + (n === 1 ? ' item.' : ' items.'));
      return cart;
    }).catch(function (e) {
      if (opts.showError) { setErr(e.message); open({ returnFocus: opts.returnFocus }); }
      throw e;
    });
  }

  function change(key, qty) {
    var li = drawer.querySelector('.line[data-key="' + (window.CSS && CSS.escape ? CSS.escape(key) : key) + '"]');
    if (li) li.classList.add('is-busy');
    setErr('');
    return req('/cart/change.js', { id: key, quantity: qty }).then(sweep).then(render).then(function (cart) {
      say(qty === 0 ? 'Item removed.' : 'Quantity updated.');
      var f = drawer.querySelector('[data-hm-lines] button') || $('[data-hm-cart-close]');
      if (qty === 0 && f) f.focus();
      return cart;
    }).catch(function (e) { setErr(e.message); if (li) li.classList.remove('is-busy'); });
  }

  /* ---------- Feed The Beast ---------- */
  function tipClick(btn) {
    var vid = Number(btn.getAttribute('data-tip')), cart = state.cart, updates = {}, same = false;
    cart.items.filter(isTip).forEach(function (t) { if (t.variant_id === vid) same = true; updates[t.key] = 0; });
    var p = Object.keys(updates).length ? req('/cart/update.js', { updates: updates }) : Promise.resolve();
    p.then(function () { return same ? null : req('/cart/add.js', { items: [{ id: vid, quantity: 1 }] }); })
      .then(refresh)
      .then(function () {
        say(same ? 'Fuel tip removed.' : 'Fuel tip added. Thank you.');
        var b = drawer.querySelector('[data-tip="' + vid + '"]'); if (b) b.focus();
      })
      .catch(function (e) { setErr(e.message); });
  }

  /* ---------- discount codes ---------- */
  function applyCodes(codes, tried) {
    var msg = $('[data-hm-discount-msg]');
    msg.textContent = 'Checking…';
    return req('/cart/update.js', { discount: codes.join(',') }).then(render).then(function (cart) {
      if (!tried) { msg.textContent = 'Code removed.'; return; }
      var hit = (cart.discount_codes || []).filter(function (c) { return c.code.toUpperCase() === tried.toUpperCase(); })[0];
      if (hit && hit.applicable) msg.textContent = hit.code.toUpperCase() + ' applied. ' + (cart.total_discount ? 'You save ' + money(cart.total_discount) + '.' : '');
      else if (hit) msg.textContent = tried.toUpperCase() + ' can’t be used on this cart yet.';
      else msg.textContent = 'That code isn’t valid. Check the spelling and try again.';
      /* keep only applicable codes in the cart */
      if (hit && !hit.applicable) {
        var keep = (cart.discount_codes || []).filter(function (c) { return c.applicable; }).map(function (c) { return c.code; });
        return req('/cart/update.js', { discount: keep.join(',') }).then(render);
      }
    }).catch(function (e) { msg.textContent = e.message; });
  }

  /* ---------- note ---------- */
  var noteT;
  function saveNote(v) { clearTimeout(noteT); noteT = setTimeout(function () { req('/cart/update.js', { note: v }).catch(function () {}); }, 400); }

  /* ---------- init ---------- */
  function init() {
    drawer = document.querySelector('[data-hm-cart]');
    if (!drawer || drawer.hmReady) return;
    drawer.hmReady = true;
    scrim = document.querySelector('[data-hm-cart-scrim]');

    var json = drawer.querySelector('[data-hm-cart-json]');
    try { render(JSON.parse(json.textContent)); } catch (e) { refresh(); }
    if (state.cart) sweep(state.cart).then(function (c) { if (c !== state.cart) render(c); });

    drawer.addEventListener('click', function (e) {
      if (e.target.closest('[data-hm-cart-close]')) { close(); return; }
      var li = e.target.closest('.line');
      if (li) {
        var key = li.getAttribute('data-key');
        if (e.target.closest('[data-rm]')) { change(key, 0); return; }
        var q = e.target.closest('[data-q]');
        if (q) {
          var item = state.cart.items.filter(function (i) { return i.key === key; })[0];
          if (item) change(key, Math.max(0, item.quantity + Number(q.getAttribute('data-q'))));
          return;
        }
      }
      var t = e.target.closest('[data-tip]'); if (t) { tipClick(t); return; }
      var rc = e.target.closest('[data-rm-code]');
      if (rc) {
        var drop = rc.getAttribute('data-rm-code');
        var keep = (state.cart.discount_codes || []).filter(function (c) { return c.applicable && c.code !== drop; }).map(function (c) { return c.code; });
        applyCodes(keep, null);
      }
    });
    drawer.querySelector('[data-hm-discount-form]').addEventListener('submit', function (e) {
      e.preventDefault();
      var input = this.querySelector('input'), v = input.value.trim();
      if (!v) { $('[data-hm-discount-msg]').textContent = 'Enter a code.'; input.focus(); return; }
      var codes = (state.cart.discount_codes || []).filter(function (c) { return c.applicable; }).map(function (c) { return c.code; });
      if (codes.map(function (c) { return c.toUpperCase(); }).indexOf(v.toUpperCase()) < 0) codes.push(v);
      applyCodes(codes, v).then(function () { input.value = ''; });
    });
    var note = drawer.querySelector('[data-hm-note]');
    if (note) note.addEventListener('input', function () { saveNote(note.value); });
    if (scrim) scrim.addEventListener('click', close);
  }

  /* hm-core.js turns clicks on [data-hm-cart-open] into "hm:cart:open"; this drawer handles it */
  document.addEventListener('hm:cart:open', function (e) {
    if (!drawer) init();
    if (!drawer) return;
    if (e.cancelable) e.preventDefault();
    open(e.detail || {});
  });
  document.addEventListener('hm:cart:close', function () { close(); });
  document.addEventListener('hm:cart:refresh', function () { refresh(); });
  /* back/forward cache: the cart may have changed in another tab */
  window.addEventListener('pageshow', function (e) { if (e.persisted && drawer) refresh(); });

  window.HMCart = { add: add, refresh: refresh, open: open, close: close, money: money, get cart() { return state.cart; } };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
