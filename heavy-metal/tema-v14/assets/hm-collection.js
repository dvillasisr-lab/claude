/* Heavy Metal shop grid: filter and sort drawer (GET form, live update with the Section Rendering API),
   Load more, and The Evil List tile when the last row is not full. */
(function () {
  'use strict';
  /* overlays: window.HMOverlay is the alias of HM.open/close from hm-core.js (one dialog at a time) */
  var OV = {
    open: function (el, o) { if (window.HMOverlay) window.HMOverlay.open(el, o); },
    close: function (el, k) { if (window.HMOverlay) window.HMOverlay.close(el, k); },
    isOpen: function (el) { return !!(el && window.HMOverlay && window.HMOverlay.isOpen(el)); }
  };

  function sectionUrl(url, id) {
    var u = new URL(url, location.href);
    u.searchParams.set('section_id', id);
    return u.toString();
  }
  function cleanUrl(url) { var u = new URL(url, location.href); u.searchParams.delete('section_id'); return u.pathname + u.search; }

  function Plp(root) {
    this.root = root;
    this.id = root.getAttribute('data-section-id');
    this.drawer = root.querySelector('[data-plp-drawer]');
    this.scrim = root.querySelector('[data-plp-scrim]');
    this.form = root.querySelector('[data-hm-filter-form]');
    this.timer = null; this.req = 0;
    var self0 = this, rt;
    this.onResize = function () { clearTimeout(rt); rt = setTimeout(function () { self0.promo(); }, 150); };
    this.bind();
    this.promo();
  }

  Plp.prototype.$ = function (s) { return this.root.querySelector(s); };

  Plp.prototype.bind = function () {
    var self = this;
    this.onClick = function (e) {
      var op = e.target.closest('[data-plp-open]');
      if (op && self.root.contains(op)) { self.open(op.getAttribute('data-plp-open'), op); return; }
      if (e.target.closest('[data-plp-close]') || e.target === self.scrim) { self.close(); return; }
      var acc = e.target.closest('[data-acc]');
      if (acc && self.drawer && self.drawer.contains(acc)) {
        var ex = acc.getAttribute('aria-expanded') === 'true';
        acc.setAttribute('aria-expanded', String(!ex));
        var p = document.getElementById(acc.getAttribute('aria-controls')); if (p) p.hidden = ex;
        return;
      }
      var more = e.target.closest('[data-hm-more]');
      if (more && self.root.contains(more)) { e.preventDefault(); self.loadMore(more); }
    };
    this.root.addEventListener('click', this.onClick);
    if (this.form) {
      this.form.addEventListener('change', function (e) {
        if (e.target.type === 'number') return;
        self.schedule(e.target.id);
      });
      this.form.addEventListener('input', function (e) { if (e.target.type === 'number') self.schedule(e.target.id, 700); });
      this.form.addEventListener('submit', function (e) { e.preventDefault(); self.apply(null, true); });
    }
    window.addEventListener('resize', this.onResize);
  };

  Plp.prototype.open = function (key, btn) {
    if (!this.drawer) return;
    [].forEach.call(this.drawer.querySelectorAll('[data-acc]'), function (b) {
      var on = b.getAttribute('data-acc') === key;
      b.setAttribute('aria-expanded', String(on));
      var p = document.getElementById(b.getAttribute('aria-controls')); if (p) p.hidden = !on;
    });
    [].forEach.call(this.root.querySelectorAll('[data-plp-open]'), function (b) { b.setAttribute('aria-expanded', String(b === btn)); });
    var accBtn = this.drawer.querySelector('[data-acc="' + key + '"]');
    var panel = accBtn && document.getElementById(accBtn.getAttribute('aria-controls'));
    var f = panel && (panel.querySelector('input:checked:not(:disabled)') || panel.querySelector('input:not(:disabled), a'));
    var self = this;
    OV.open(this.drawer, {
      scrim: this.scrim,
      focus: f || this.drawer.querySelector('[data-plp-close]'),
      returnFocus: btn,
      onClose: function () { [].forEach.call(self.root.querySelectorAll('[data-plp-open]'), function (b) { b.setAttribute('aria-expanded', 'false'); }); }
    });
    if (accBtn) accBtn.scrollIntoView({ block: 'nearest' });
  };
  Plp.prototype.close = function () { if (this.drawer && OV.isOpen(this.drawer)) OV.close(this.drawer); };

  Plp.prototype.schedule = function (focusId, wait) {
    var self = this; clearTimeout(this.timer);
    this.timer = setTimeout(function () { self.apply(focusId, false); }, wait || 250);
  };

  Plp.prototype.query = function () {
    var fd = new FormData(this.form), q = new URLSearchParams();
    fd.forEach(function (v, k) { if (v !== '') q.append(k, v); });
    return q.toString();
  };

  Plp.prototype.apply = function (focusId, closeAfter) {
    var self = this, url = this.form.getAttribute('action') + '?' + this.query(), n = ++this.req;
    var res = this.$('[data-hm-region="results"]'); if (res) res.setAttribute('aria-busy', 'true');
    fetch(sectionUrl(url, this.id)).then(function (r) { return r.text(); }).then(function (html) {
      if (n !== self.req) return;
      self.swap(html, focusId);
      try { history.replaceState(null, '', cleanUrl(url)); } catch (e) {}
      if (closeAfter) self.close();
    }).catch(function () { location.href = url; });
  };

  Plp.prototype.swap = function (html, focusId) {
    var doc = new DOMParser().parseFromString(html, 'text/html');
    var open = {}, body = this.$('[data-hm-region="drawer"]'), top = body ? body.scrollTop : 0;
    if (body) [].forEach.call(body.querySelectorAll('[data-acc]'), function (b) { open[b.getAttribute('data-acc')] = b.getAttribute('aria-expanded') === 'true'; });
    var self = this;
    ['bar', 'chips', 'results', 'status', 'drawer', 'view'].forEach(function (k) {
      var cur = self.$('[data-hm-region="' + k + '"]'), nxt = doc.querySelector('[data-hm-region="' + k + '"]');
      if (cur && nxt) cur.innerHTML = nxt.innerHTML;
      if (cur && k === 'results') cur.removeAttribute('aria-busy');
    });
    body = this.$('[data-hm-region="drawer"]');
    if (body) {
      [].forEach.call(body.querySelectorAll('[data-acc]'), function (b) {
        var on = !!open[b.getAttribute('data-acc')];
        b.setAttribute('aria-expanded', String(on));
        var p = document.getElementById(b.getAttribute('aria-controls')); if (p) p.hidden = !on;
      });
      body.scrollTop = top;
    }
    if (focusId) { var el = document.getElementById(focusId); if (el) el.focus({ preventScroll: true }); }
    this.promo();
  };

  Plp.prototype.loadMore = function (a) {
    var self = this;
    a.setAttribute('aria-busy', 'true'); a.textContent = 'Loading…';
    fetch(sectionUrl(a.href, this.id)).then(function (r) { return r.text(); }).then(function (html) {
      var doc = new DOMParser().parseFromString(html, 'text/html');
      var grid = self.$('[data-hm-grid]'), nextGrid = doc.querySelector('[data-hm-grid]');
      var old = grid && grid.querySelector('.plp-promo'); if (old) old.remove();
      var firstNew = null;
      if (grid && nextGrid) [].slice.call(nextGrid.children).forEach(function (c) { var n = document.importNode(c, true); if (!firstNew) firstNew = n; grid.appendChild(n); });
      var foot = self.$('[data-hm-foot]'), nf = doc.querySelector('[data-hm-foot]'); if (foot && nf) foot.innerHTML = nf.innerHTML;
      var last = self.$('[data-hm-last-page]'), nl = doc.querySelector('[data-hm-last-page]'); if (last && nl) last.setAttribute('data-hm-last-page', nl.getAttribute('data-hm-last-page'));
      var link = firstNew && firstNew.querySelector('.card__name a'); if (link) link.focus({ preventScroll: true });
      self.promo();
    }).catch(function () { location.href = a.href; });
  };

  /* last row not full: The Evil List tile fills the gap (needs at least 2 empty columns) */
  Plp.prototype.promo = function () {
    var grid = this.$('[data-hm-grid]'); if (!grid) return;
    var old = grid.querySelector('.plp-promo'); if (old) old.remove();
    var last = this.$('[data-hm-last-page]'); if (!last || last.getAttribute('data-hm-last-page') !== 'true') return;
    var tpl = this.$('template[data-hm-promo]'); if (!tpl) return;
    var n = grid.querySelectorAll('[data-hm-card]').length; if (!n) return;
    var cols = getComputedStyle(grid).gridTemplateColumns.split(' ').filter(Boolean).length, rest = n % cols;
    /* v14.1: only once the shop fills at least one full row; with 1 to 3 products the tile looked like an empty box */
    if (n < cols || !rest || cols - rest < 2) return;
    var node = tpl.content.firstElementChild.cloneNode(true);
    node.style.gridColumn = 'span ' + (cols - rest);
    if (cols - rest > 2) node.setAttribute('data-wide', '');
    grid.appendChild(node);
  };

  Plp.prototype.destroy = function () {
    this.close();
    this.root.removeEventListener('click', this.onClick);
    window.removeEventListener('resize', this.onResize);
    clearTimeout(this.timer);
  };

  var inst = new Map();
  function init(scope) {
    [].forEach.call((scope || document).querySelectorAll('[data-hm-plp]'), function (r) { if (!inst.has(r)) inst.set(r, new Plp(r)); });
  }
  document.addEventListener('shopify:section:load', function (e) { init(e.target); });
  document.addEventListener('shopify:section:unload', function (e) {
    inst.forEach(function (p, r) { if (e.target.contains(r)) { p.destroy(); inst.delete(r); } });
  });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { init(); }); else init();
})();
