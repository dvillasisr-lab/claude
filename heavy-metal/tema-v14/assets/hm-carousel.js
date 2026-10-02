/* HM Carousel (sections/hm-carousel.liquid): coverflow with autoplay, arrows, swipe, keyboard and dots.
   Reduced motion or fewer than 3 products: stays the plain scroll-snap row from the CSS (nothing moves on its own). */
(function () {
  'use strict';
  if (window.HMCarousel) return;
  var rm = window.matchMedia('(prefers-reduced-motion: reduce)');

  function Cf(root) {
    this.root = root;
    this.slides = [].slice.call(root.querySelectorAll('[data-cf-slide]'));
    this.n = this.slides.length;
    this.cur = 0;
    this.offs = [];
    this.userPaused = false;
    this.hold = { hover: false, focus: false, hidden: false, out: false, drag: false };
    this.interval = Math.max(2500, Number(root.getAttribute('data-interval')) || 5000);
    this.auto = root.getAttribute('data-autoplay') === 'true';
    if (this.n < 3 || rm.matches) return;
    this.build();
  }

  Cf.prototype.on = function (el, ev, fn, o) { if (!el) return; el.addEventListener(ev, fn, o); this.offs.push(function () { el.removeEventListener(ev, fn, o); }); };

  Cf.prototype.build = function () {
    var self = this, r = this.root;
    r.classList.add('is-3d');
    this.stage = r.querySelector('[data-cf-stage]');
    this.live = r.querySelector('[data-cf-live]');
    this.dots = [].slice.call(r.querySelectorAll('[data-cf-dots] button'));
    this.pauseBtn = r.querySelector('[data-cf-pause]');
    var prev = r.querySelector('[data-cf-prev]'), next = r.querySelector('[data-cf-next]'), ctrl = r.querySelector('[data-cf-ctrl]');
    prev.hidden = false; next.hidden = false; ctrl.hidden = false;
    if (!this.auto && this.pauseBtn) this.pauseBtn.hidden = true;

    this.on(prev, 'click', function () { self.go(self.cur - 1, true); });
    this.on(next, 'click', function () { self.go(self.cur + 1, true); });
    this.dots.forEach(function (b, i) { self.on(b, 'click', function () { self.go(i, true); }); });
    this.on(this.pauseBtn, 'click', function () { self.userPaused = !self.userPaused; self.sync(); });

    /* a side card: the first click brings it to the center instead of opening it */
    this.slides.forEach(function (s, i) {
      self.on(s, 'click', function (e) {
        if (self.moved) { e.preventDefault(); e.stopPropagation(); return; }
        if (i !== self.cur) { e.preventDefault(); e.stopPropagation(); self.go(i, true); }
      }, true);
    });

    /* keyboard: arrow keys anywhere inside the carousel */
    this.on(r, 'keydown', function (e) {
      if (e.target.closest('input,textarea,select')) return;
      if (e.key === 'ArrowLeft') { e.preventDefault(); self.go(self.cur - 1, true, true); }
      else if (e.key === 'ArrowRight') { e.preventDefault(); self.go(self.cur + 1, true, true); }
    });

    /* swipe and mouse drag */
    var x0 = null, y0 = 0, id = null;
    this.on(this.stage, 'pointerdown', function (e) {
      if (e.button !== 0 || e.target.closest('button')) return;
      x0 = e.clientX; y0 = e.clientY; id = e.pointerId; self.moved = false;
    });
    this.on(this.stage, 'pointermove', function (e) {
      if (x0 === null || e.pointerId !== id) return;
      var dx = e.clientX - x0;
      if (!self.moved && Math.abs(dx) > 8 && Math.abs(dx) > Math.abs(e.clientY - y0)) {
        self.moved = true; self.hold.drag = true; self.sync();
        try { self.stage.setPointerCapture(id); } catch (er) {}
      }
    });
    function end(e) {
      if (x0 === null || e.pointerId !== id) return;
      var dx = e.clientX - x0; x0 = null;
      if (self.moved && Math.abs(dx) > 40) self.go(self.cur + (dx < 0 ? 1 : -1), true);
      self.hold.drag = false; self.sync();
      setTimeout(function () { self.moved = false; }, 0);
    }
    this.on(this.stage, 'pointerup', end);
    this.on(this.stage, 'pointercancel', function (e) { x0 = null; self.moved = false; self.hold.drag = false; self.sync(); });
    this.on(this.stage, 'dragstart', function (e) { e.preventDefault(); });

    /* pause on hover / focus, when the tab is hidden, and when scrolled out of view */
    this.on(r, 'mouseenter', function () { self.hold.hover = true; self.sync(); });
    this.on(r, 'mouseleave', function () { self.hold.hover = false; self.sync(); });
    this.on(r, 'focusin', function (e) {
      self.hold.focus = true; self.sync();
      var s = e.target.closest('[data-cf-slide]'), i = self.slides.indexOf(s);
      if (i > -1 && i !== self.cur) self.go(i, true);
    });
    this.on(r, 'focusout', function (e) { if (!r.contains(e.relatedTarget)) { self.hold.focus = false; self.sync(); } });
    this.on(document, 'visibilitychange', function () { self.hold.hidden = document.hidden; self.sync(); });
    if ('IntersectionObserver' in window) {
      this.io = new IntersectionObserver(function (en) { self.hold.out = !en[0].isIntersecting; self.sync(); }, { threshold: 0.25 });
      this.io.observe(r);
    }
    this.on(rm, 'change', function () { if (rm.matches) self.destroy(true); });

    this.place();
    this.sync();
  };

  Cf.prototype.place = function () {
    var n = this.n, c = this.cur;
    this.slides.forEach(function (s, i) {
      var d = i - c;
      if (d > n / 2) d -= n; else if (d < -n / 2) d += n;
      var ad = Math.min(Math.abs(d), 3);
      s.style.setProperty('--d', d);
      s.style.setProperty('--ad', ad);
      s.style.setProperty('--r', Math.max(-1, Math.min(1, d)));
      s.style.zIndex = String(10 - ad);
      s.classList.toggle('is-on', d === 0);
      s.classList.toggle('is-far', Math.abs(d) > 2);
      s.setAttribute('aria-hidden', d === 0 ? 'false' : 'true');
      [].forEach.call(s.querySelectorAll('a,button'), function (a) {
        if (!a.hasAttribute('data-cf-tab')) a.setAttribute('data-cf-tab', a.getAttribute('tabindex') || '');
        var orig = a.getAttribute('data-cf-tab');
        if (d === 0) { if (orig) a.setAttribute('tabindex', orig); else a.removeAttribute('tabindex'); }
        else a.setAttribute('tabindex', '-1');
      });
    });
    var cur = this.cur;
    this.dots.forEach(function (b, i) { b.setAttribute('aria-current', i === cur ? 'true' : 'false'); });
  };

  Cf.prototype.go = function (i, user, announce) {
    this.cur = ((i % this.n) + this.n) % this.n;
    this.place();
    if (user) { this.restart(); }
    if (announce && this.live) {
      var t = this.slides[this.cur].querySelector('.cf__name');
      this.live.textContent = (this.cur + 1) + ' of ' + this.n + ': ' + (t ? t.textContent.trim() : '');
    }
  };

  Cf.prototype.running = function () {
    var h = this.hold;
    return this.auto && !this.userPaused && !h.hover && !h.focus && !h.hidden && !h.out && !h.drag;
  };
  Cf.prototype.restart = function () { clearInterval(this.t); this.t = null; this.sync(); };
  Cf.prototype.sync = function () {
    var self = this;
    if (this.pauseBtn) {
      this.pauseBtn.setAttribute('aria-pressed', String(this.userPaused));
      var l = this.pauseBtn.querySelector('[data-cf-pause-label]'); if (l) l.textContent = this.userPaused ? 'Play' : 'Pause';
    }
    if (this.running()) {
      if (!this.t) this.t = setInterval(function () { self.go(self.cur + 1); }, this.interval);
    } else if (this.t) { clearInterval(this.t); this.t = null; }
  };

  Cf.prototype.destroy = function (flat) {
    clearInterval(this.t); this.t = null;
    this.offs.forEach(function (f) { f(); }); this.offs = [];
    if (this.io) this.io.disconnect();
    if (flat) {
      var r = this.root;
      r.classList.remove('is-3d');
      ['[data-cf-prev]', '[data-cf-next]', '[data-cf-ctrl]'].forEach(function (s) { var el = r.querySelector(s); if (el) el.hidden = true; });
      this.slides.forEach(function (s) {
        s.removeAttribute('aria-hidden'); s.style.zIndex = '';
        s.classList.remove('is-on', 'is-far');
        [].forEach.call(s.querySelectorAll('[data-cf-tab]'), function (a) {
          var o = a.getAttribute('data-cf-tab'); if (o) a.setAttribute('tabindex', o); else a.removeAttribute('tabindex');
        });
      });
    }
  };

  var inst = new Map();
  function init(scope) {
    [].forEach.call((scope || document).querySelectorAll('[data-hm-cf]'), function (r) { if (!inst.has(r)) inst.set(r, new Cf(r)); });
  }
  window.HMCarousel = { init: init };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { init(); }); else init();
  document.addEventListener('shopify:section:load', function (e) { init(e.target); });
  document.addEventListener('shopify:section:unload', function (e) {
    inst.forEach(function (c, r) { if (e.target.contains(r)) { c.destroy(); inst.delete(r); } });
  });
})();
