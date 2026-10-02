/* Heavy Metal product page: gallery (arrows, counter, thumbs, dots, swipe, keyboard, zoom lightbox),
   options with required size (no preselection), quantity, AJAX add that opens the cart drawer,
   size guide dialog and the sticky add bar on phones. */
(function () {
  'use strict';

  /* same output as Liquid money_without_trailing_zeros: $25, not $25.00 */
  function money(cents, fmt) {
    var s = window.HMCart && window.HMCart.money ? window.HMCart.money(cents)
      : (fmt || '${{amount}}').replace(/\{\{\s*\w+\s*\}\}/, (cents / 100).toFixed(2));
    return String(s).replace(/([.,])00(?!\d)/, '');
  }

  function Pdp(root) {
    this.root = root;
    this.handlers = [];
    this.clears = [];
    this.state = root.getAttribute('data-state');
    this.needsSize = root.getAttribute('data-needs-size') === 'true';
    this.sizePos = Number(root.getAttribute('data-size-pos')) || 0;
    this.fmt = root.getAttribute('data-money-format');
    try { this.variants = JSON.parse(root.querySelector('[data-hm-variants]').textContent); } catch (e) { this.variants = []; }
    this.form = root.querySelector('[data-hm-pdp-form]');
    this.atc = root.querySelector('[data-hm-atc]');
    this.initGallery();
    this.initOptions();
    this.initDialogs();
    this.initSticky();
  }

  Pdp.prototype.on = function (el, ev, fn, opt) { if (!el) return; el.addEventListener(ev, fn, opt); this.handlers.push([el, ev, fn, opt]); };
  Pdp.prototype.q = function (s) { return this.root.querySelector(s); };
  Pdp.prototype.qa = function (s) { return [].slice.call(this.root.querySelectorAll(s)); };

  /* ---------------- gallery ---------------- */
  Pdp.prototype.initGallery = function () {
    var self = this, track = this.q('[data-pg-track]'); if (!track) return;
    var slides = [].slice.call(track.querySelectorAll('.pg__slide'));
    var thumbs = this.q('[data-pg-thumbs]'), dots = this.q('[data-pg-dots]');
    var n = slides.length, many = n > 1, cur = 0, aim = null, aimT, st;
    var smooth = matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth';
    this.slides = slides;

    function mark(i) {
      cur = i; self.cur = i;
      var c = self.q('[data-pg-count]'); if (c) c.textContent = (i + 1) + ' / ' + n;
      var live = self.q('[data-pg-live]'); if (live && many) live.textContent = 'Image ' + (i + 1) + ' of ' + n;
      if (thumbs) [].forEach.call(thumbs.querySelectorAll('button'), function (b, j) { b.setAttribute('aria-current', j === i ? 'true' : 'false'); });
      if (dots) [].forEach.call(dots.children, function (b, j) { b.setAttribute('aria-current', j === i ? 'true' : 'false'); });
      var t = thumbs && thumbs.children[i];
      if (t && thumbs.offsetParent) {
        var l = t.offsetLeft - thumbs.offsetLeft, w = t.offsetWidth;
        if (l < thumbs.scrollLeft || l + w > thumbs.scrollLeft + thumbs.clientWidth) thumbs.scrollTo({ left: l - (thumbs.clientWidth - w) / 2, behavior: smooth });
      }
    }
    function go(i, instant) {
      if (!n) return;
      i = (i + n) % n;
      aim = i; clearTimeout(aimT); aimT = setTimeout(function () { aim = null; }, 1200);
      track.scrollTo({ left: i * track.clientWidth, behavior: instant ? 'auto' : smooth });
      mark(i);
    }
    this.go = go;
    this.clears.push(function () { clearTimeout(aimT); clearTimeout(st); });
    ['pointerdown', 'touchstart', 'wheel'].forEach(function (ev) { self.on(track, ev, function () { aim = null; }, { passive: true }); });
    this.on(this.q('[data-pg-prev]'), 'click', function () { go(cur - 1); });
    this.on(this.q('[data-pg-next]'), 'click', function () { go(cur + 1); });
    this.on(thumbs, 'click', function (e) { var b = e.target.closest('[data-i]'); if (b) go(Number(b.getAttribute('data-i'))); });
    this.on(dots, 'click', function (e) { var b = e.target.closest('[data-i]'); if (b) go(Number(b.getAttribute('data-i'))); });
    this.on(track, 'scroll', function () {
      clearTimeout(st);
      st = setTimeout(function () {
        var i = Math.max(0, Math.min(n - 1, Math.round(track.scrollLeft / Math.max(1, track.clientWidth))));
        if (aim !== null) { if (i === aim) { aim = null; clearTimeout(aimT); } return; }
        if (i !== cur) mark(i);
      }, 60);
    }, { passive: true });
    this.on(window, 'resize', function () { track.scrollTo({ left: cur * track.clientWidth }); });
    this.on(this.q('[data-hm-pg]'), 'keydown', function (e) {
      if (self.lb && self.lb.open) return;
      if (e.target.closest('video, iframe, model-viewer')) return; /* media keep their own arrow keys */
      if ((e.key === 'ArrowLeft' || e.key === 'ArrowRight') && many) {
        e.preventDefault(); go(cur + (e.key === 'ArrowRight' ? 1 : -1));
        if (e.target.closest('.pg__thumb')) thumbs.querySelectorAll('button')[cur].focus({ preventScroll: true });
      } else if (e.key === 'Home' && e.target === track) { e.preventDefault(); go(0); }
      else if (e.key === 'End' && e.target === track) { e.preventDefault(); go(n - 1); }
      else if (e.key === 'Enter' && e.target === track && self.openLB) { e.preventDefault(); self.openLB(); }
    });
    mark(0);

    /* lightbox with zoom (images only) */
    var lb = this.q('[data-lb]'); this.lb = lb;
    if (!lb) return;
    var lbImg = lb.querySelector('[data-lb-img]'), lastFocus = null, sx = null, swiped = false;
    var zoomable = function (i) { return slides[i] && slides[i].getAttribute('data-zoom'); };
    function render() {
      lbImg.classList.remove('is-zoom');
      var s = slides[cur];
      var img = document.createElement('img');
      img.src = s.getAttribute('data-zoom'); img.alt = s.getAttribute('data-alt') || '';
      lbImg.replaceChildren(img);
      lb.querySelector('[data-lb-count]').textContent = (cur + 1) + ' / ' + n;
    }
    function step(d) {
      for (var k = 1; k <= n; k++) { var i = (cur + d * k + n * k) % n; if (zoomable(i)) { go(i, true); render(); return; } }
    }
    this.openLB = function () {
      if (!zoomable(cur)) return;
      lastFocus = document.activeElement; render();
      if (!lb.open) lb.showModal();
      lb.querySelector('[data-lb-close]').focus();
      document.documentElement.style.overflow = 'hidden';
    };
    this.on(lb, 'close', function () { document.documentElement.style.overflow = ''; if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true }); });
    this.on(lb.querySelector('[data-lb-close]'), 'click', function () { lb.close(); });
    this.on(lb.querySelector('[data-lb-prev]'), 'click', function () { step(-1); });
    this.on(lb.querySelector('[data-lb-next]'), 'click', function () { step(1); });
    this.on(lb, 'keydown', function (e) {
      if (e.key === 'ArrowLeft' && many) { e.preventDefault(); step(-1); }
      else if (e.key === 'ArrowRight' && many) { e.preventDefault(); step(1); }
    });
    function origin(e) { var r = lbImg.getBoundingClientRect(); lbImg.style.setProperty('--ox', ((e.clientX - r.left) / r.width * 100).toFixed(1) + '%'); lbImg.style.setProperty('--oy', ((e.clientY - r.top) / r.height * 100).toFixed(1) + '%'); }
    this.on(lbImg, 'pointerdown', function (e) { sx = e.clientX; swiped = false; });
    this.on(lbImg, 'pointerup', function (e) {
      if (sx != null && !lbImg.classList.contains('is-zoom') && many && Math.abs(e.clientX - sx) > 40) { swiped = true; step(e.clientX < sx ? 1 : -1); }
      sx = null;
    });
    this.on(lbImg, 'click', function (e) { if (swiped) return; origin(e); lbImg.classList.toggle('is-zoom'); });
    this.on(lbImg, 'pointermove', function (e) { if (lbImg.classList.contains('is-zoom') && (e.pointerType === 'mouse' || sx != null)) origin(e); });
    this.on(lb, 'click', function (e) { if (e.target === lb || e.target.classList.contains('lb__fig')) lb.close(); });
    this.on(track, 'click', function (e) { if (e.target.closest('.pg__slide[data-zoom]')) self.openLB(); });
    this.on(this.q('[data-pg-zoom]'), 'click', function () { self.openLB(); });
  };

  /* ---------------- options and add to cart ---------------- */
  Pdp.prototype.chosen = function () {
    return this.qa('[data-hm-opt]').map(function (fs) {
      var c = fs.querySelector('input:checked'); return c ? c.value : null;
    });
  };
  Pdp.prototype.find = function (vals) {
    return this.variants.filter(function (v) { return vals.every(function (x, i) { return x == null || v.options[i] === x; }); });
  };
  Pdp.prototype.current = function () {
    var vals = this.chosen();
    if (vals.some(function (x) { return x == null; })) return null;
    return this.find(vals)[0] || null;
  };
  Pdp.prototype.qty = function (d) {
    var i = this.q('[data-hm-qty]'); if (!i) return 1;
    var max = Number(i.max) || 99;
    return Math.min(max, Math.max(1, (parseInt(i.value, 10) || 1) + (d || 0)));
  };
  Pdp.prototype.ready = function () { return this.state === 'live' && !!this.current(); };

  Pdp.prototype.initOptions = function () {
    var self = this;
    this.qa('[data-hm-opt]').forEach(function (fs) {
      self.on(fs, 'change', function (e) {
        fs.classList.remove('is-error');
        var m = self.q('[data-hm-size-msg]'); if (m && fs.getAttribute('data-kind') === 'size') m.textContent = '';
        self.update(fs.getAttribute('data-kind') === 'color');
      });
    });
    this.qa('[data-qty]').forEach(function (b) {
      self.on(b, 'click', function () {
        var i = self.q('[data-hm-qty]'); if (!i) return;
        i.value = self.qty(Number(b.getAttribute('data-qty')));
      });
    });
    var qi = this.q('[data-hm-qty]');
    this.on(qi, 'change', function () { qi.value = self.qty(0); });
    if (this.form) {
      this.on(this.form, 'submit', function (e) { self.submit(e); });
    }
    var dyn = this.q('[data-hm-dyn]');
    if (dyn) this.on(dyn, 'click', function (e) {
      if (self.ready()) return;
      e.preventDefault(); e.stopPropagation(); self.needSize();
    }, true);
    this.update(false, true);
  };

  Pdp.prototype.update = function (colorChanged, first) {
    var self = this, vals = this.chosen();
    /* size buttons: disable sizes sold out in the chosen color */
    if (this.sizePos) {
      var si = this.sizePos - 1, sold = [];
      var fs = this.q('[data-hm-opt="' + this.sizePos + '"]');
      if (fs) [].forEach.call(fs.querySelectorAll('input'), function (inp) {
        var test = vals.slice(); test[si] = inp.value;
        var v = self.find(test.map(function (x, i) { return i === si ? x : x; })).filter(function (x) { return x.available; })[0];
        var off = !v;
        inp.disabled = off;
        var lab = fs.querySelector('label[for="' + inp.id + '"]');
        if (lab) { var sr = lab.querySelector('.vh'); if (off && !sr) lab.insertAdjacentHTML('beforeend', '<span class="vh">, sold out</span>'); if (!off && sr) sr.remove(); }
        if (off) { sold.push(inp.value); if (inp.checked) inp.checked = false; }
      });
      var sw = this.q('[data-hm-sold]');
      if (sw) { sw.hidden = !sold.length || this.state !== 'live'; this.q('[data-hm-sold-list]').textContent = sold.join(', '); }
      vals = this.chosen();
    }
    /* labels */
    this.qa('[data-hm-opt]').forEach(function (fs, i) {
      var l = fs.querySelector('[data-hm-opt-label]');
      if (l) l.textContent = vals[i] != null ? vals[i] : 'Select a ' + (fs.querySelector('legend span').firstChild.textContent.replace(':', '').trim().toLowerCase());
    });
    var v = this.current(), idInput = this.q('[data-hm-variant-id]');
    if (idInput) idInput.value = v ? v.id : '';
    /* price */
    var priceV = v || this.find(vals).filter(function (x) { return x.available; })[0] || this.find(vals)[0];
    var pe = this.q('[data-hm-price]');
    if (pe && priceV && !first) {
      pe.innerHTML = priceV.compare > priceV.price
        ? '<span class="vh">Sale price </span>' + money(priceV.price, this.fmt) + ' <s class="muted">' + money(priceV.compare, this.fmt) + '</s>'
        : money(priceV.price, this.fmt);
    }
    /* button */
    var label = this.state !== 'live' ? 'Notify me' : !v ? 'Select a size' : v.available ? 'Add to cart · ' + money(v.price, this.fmt) : 'Sold out';
    if (this.atc) { this.atc.textContent = label; this.atc.disabled = !!(v && !v.available); }
    var sb = this.q('[data-satc-btn]'); if (sb) sb.textContent = this.state !== 'live' ? 'Notify me' : !v ? 'Select a size' : v.available ? 'Add · ' + money(v.price, this.fmt) : 'Sold out';
    var sv = this.q('[data-satc-var]');
    if (sv && this.state === 'live') sv.textContent = vals.map(function (x) { return x == null ? 'Select a size' : x; }).join(' · ') || 'One size';
    var dyn = this.q('[data-hm-dyn]'); if (dyn) dyn.classList.toggle('is-locked', !this.ready());
    /* URL and photo for the variant */
    if (!first && v) { try { var u = new URL(location.href); u.searchParams.set('variant', v.id); history.replaceState(null, '', u.toString()); } catch (e) {} }
    if (colorChanged && this.go && this.slides) {
      var mv = (v && v.media) || (this.find(vals).filter(function (x) { return x.media; })[0] || {}).media;
      if (mv) { var idx = this.slides.map(function (s) { return s.getAttribute('data-media-id'); }).indexOf(String(mv)); if (idx > -1) this.go(idx); }
    }
  };

  Pdp.prototype.needSize = function () {
    var fs = this.sizePos ? this.q('[data-hm-opt="' + this.sizePos + '"]') : null;
    var m = this.q('[data-hm-size-msg]');
    if (fs) {
      fs.classList.add('is-error');
      if (m) m.textContent = 'Select a size to continue.';
      fs.scrollIntoView({ block: 'center', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
      var f = fs.querySelector('input:not(:disabled)'); if (f) f.focus({ preventScroll: true });
    }
  };

  Pdp.prototype.submit = function (e) {
    var self = this, msg = this.q('[data-hm-atc-msg]');
    if (msg) msg.textContent = '';
    if (this.state !== 'live') { e.preventDefault(); return; }
    var v = this.current();
    if (!v) { e.preventDefault(); this.needSize(); return; }
    if (!v.available) { e.preventDefault(); return; }
    var qty = this.qty(0), qi = this.q('[data-hm-qty]'); if (qi) qi.value = qty;
    if (!window.HMCart) return; /* no drawer: classic form post to /cart/add */
    e.preventDefault();
    var btn = this.atc, old = btn.textContent;
    btn.setAttribute('aria-busy', 'true'); btn.textContent = 'Adding…';
    window.HMCart.add([{ id: v.id, quantity: qty }], { returnFocus: btn }).then(function () {
      btn.removeAttribute('aria-busy'); btn.textContent = old;
    }).catch(function (err) {
      btn.removeAttribute('aria-busy'); btn.textContent = old;
      if (msg) msg.textContent = err.message;
    });
  };

  /* ---------------- size guide ---------------- */
  Pdp.prototype.initDialogs = function () {
    var self = this, sg = this.q('[data-sg]'); if (!sg) return;
    var last = null;
    this.qa('[data-sg-open]').forEach(function (b) {
      self.on(b, 'click', function () { last = b; sg.showModal(); sg.querySelector('[data-sg-close]').focus(); });
    });
    this.on(sg.querySelector('[data-sg-close]'), 'click', function () { sg.close(); });
    this.on(sg, 'click', function (e) { if (e.target === sg) sg.close(); });
    this.on(sg, 'close', function () { if (last) last.focus(); });
  };

  /* ---------------- sticky bar (phones) ---------------- */
  Pdp.prototype.initSticky = function () {
    var self = this, bar = this.q('[data-satc]'); if (!bar) return;
    var target = this.state === 'live' ? this.atc : this.q('[data-hm-nbox]');
    if (!target || !('IntersectionObserver' in window)) return;
    function set(on) {
      bar.classList.toggle('is-on', on); bar.setAttribute('aria-hidden', String(!on));
      var b = bar.querySelector('[data-satc-btn]'); if (b) b.tabIndex = on ? 0 : -1;
    }
    this.io = new IntersectionObserver(function (en) {
      en.forEach(function (x) { set(!x.isIntersecting && x.boundingClientRect.top < 0); });
    });
    this.io.observe(target);
    this.on(bar.querySelector('[data-satc-btn]'), 'click', function () {
      if (self.state !== 'live') {
        var nb = self.q('[data-hm-nbox]'); if (nb) { nb.scrollIntoView({ block: 'center' }); var em = nb.querySelector('input[type="email"]'); if (em) em.focus({ preventScroll: true }); }
        return;
      }
      if (!self.current()) { self.needSize(); return; }
      if (self.form.requestSubmit) self.form.requestSubmit(self.atc); else self.atc.click();
    });
  };

  Pdp.prototype.destroy = function () {
    this.handlers.forEach(function (h) { h[0].removeEventListener(h[1], h[2], h[3]); });
    this.clears.forEach(function (f) { f(); });
    if (this.io) this.io.disconnect();
    if (this.lb && this.lb.open) this.lb.close();
  };

  var inst = new Map();
  function init(scope) {
    [].forEach.call((scope || document).querySelectorAll('[data-hm-pdp]'), function (r) { if (!inst.has(r)) inst.set(r, new Pdp(r)); });
  }
  document.addEventListener('shopify:section:load', function (e) { init(e.target); });
  document.addEventListener('shopify:section:unload', function (e) {
    inst.forEach(function (p, r) { if (e.target.contains(r)) { p.destroy(); inst.delete(r); } });
  });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { init(); }); else init();
})();
