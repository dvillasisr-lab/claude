/* Heavy Metal special edition: state (Coming soon / Live / Sold out) and countdown computed in the browser
   from the product dates (data-start / data-end, unix seconds) and inventory, never in Liquid (page cache).
   Past editions: keeps only closed ones and filters them by year. */
(function () {
  'use strict';
  var LABEL = { soon: 'Coming soon', live: 'Live now', sold: 'Sold out' };
  var TZ = { timeZone: 'America/Chicago' };
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function fmt(d) {
    try {
      return d.toLocaleDateString('en-US', Object.assign({ weekday: 'short', month: 'short', day: 'numeric' }, TZ)) + ', ' +
        d.toLocaleTimeString('en-US', Object.assign({ hour: 'numeric', minute: '2-digit' }, TZ)) + ' CT';
    } catch (e) { return d.toDateString(); }
  }

  function Edition(root) {
    this.root = root;
    this.start = Number(root.getAttribute('data-start')) * 1000 || 0;
    this.end = Number(root.getAttribute('data-end')) * 1000 || 0;
    this.available = root.getAttribute('data-available') === 'true';
    this.run = Number(root.getAttribute('data-run')) || 0;
    this.left = root.getAttribute('data-left') === '' || root.getAttribute('data-left') == null ? null : Number(root.getAttribute('data-left'));
    this.timer = null; this.paused = false; this.flashed = false; this.handlers = [];
    if (root.querySelector('[data-se-badge]')) { this.bind(); this.apply(); }
    this.past();
  }
  Edition.prototype.q = function (s) { return this.root.querySelector(s); };
  Edition.prototype.on = function (el, ev, fn) { if (!el) return; el.addEventListener(ev, fn); this.handlers.push([el, ev, fn]); };

  Edition.prototype.state = function (now) {
    if (!this.available) return 'sold';
    if (this.start && now < this.start) return 'soon';
    if (this.end && now > this.end) return 'sold';
    return 'live';
  };

  Edition.prototype.apply = function () {
    var self = this, now = Date.now(), s = this.state(now);
    this.s = s;
    var badge = this.q('[data-se-badge]'); badge.setAttribute('data-s', s); badge.textContent = LABEL[s];
    clearInterval(this.timer); this.timer = null;
    var row = this.q('[data-se-row]'), done = this.q('[data-se-done]'), when = this.q('[data-se-when]'), l = this.q('[data-se-l]'), pause = this.q('[data-se-pause]');
    var target = s === 'soon' ? this.start : s === 'live' ? this.end : 0;
    done.hidden = s !== 'sold';
    row.hidden = s === 'sold' || !target;
    if (pause) pause.hidden = row.hidden;
    l.textContent = s === 'soon' ? 'Drop opens in' : s === 'live' ? (target ? 'Drop closes in' : 'Live now · while the run lasts') : 'This drop is closed';
    if (s === 'sold') when.textContent = this.end && this.end < now ? 'Closed ' + fmt(new Date(this.end)) + '. Get notified for the next edition.' : 'Get notified for the next edition.';
    else when.textContent = target ? (s === 'soon' ? 'Opens ' : 'Closes ') + fmt(new Date(target)) + '.' : '';
    if (target && s !== 'sold') {
      var tick = function () {
        if (self.paused) return;
        var d = Math.max(0, target - Date.now()), sec = Math.floor(d / 1000);
        self.q('[data-se-d]').textContent = pad(Math.floor(sec / 86400));
        self.q('[data-se-h]').textContent = pad(Math.floor(sec % 86400 / 3600));
        self.q('[data-se-m]').textContent = pad(Math.floor(sec % 3600 / 60));
        self.q('[data-se-s]').textContent = pad(sec % 60);
        if (d <= 0) self.apply();
      };
      this.paused = false; this.tick = tick;
      if (pause) { pause.setAttribute('aria-pressed', 'false'); pause.textContent = 'Pause timer'; }
      tick(); this.timer = setInterval(tick, 1000);
    }

    /* units */
    var bar = this.q('[data-se-bar]');
    if (bar && this.run) {
      var left = s === 'sold' ? 0 : s === 'soon' ? this.run : (this.left == null ? this.run : this.left);
      var fill = Math.round(left / this.run * 100);
      bar.style.setProperty('--fill', fill + '%');
      bar.classList.toggle('is-low', s === 'live' && fill <= 20);
      bar.classList.toggle('is-soon', s === 'soon');
      this.q('[data-se-units]').textContent = left + ' of ' + this.run + ' left';
      this.q('[data-se-units-l]').textContent = s === 'soon' ? 'Full run at launch' : 'Units left';
    }

    /* sizes, add button, notify */
    var on = s === 'live', fs = this.q('[data-se-sizes]');
    if (fs) {
      [].forEach.call(fs.querySelectorAll('input'), function (i) { i.disabled = !on || i.hasAttribute('data-sold'); if (!on) i.checked = false; });
      fs.classList.toggle('is-off', !on);
      var sv = this.q('[data-se-size-v]'); if (sv) sv.textContent = on ? 'Select' : s === 'soon' ? 'Available at launch' : 'Sold out';
    }
    this.q('[data-se-add]').hidden = !on;
    this.q('[data-se-notify]').hidden = on;
    var p = this.q('[data-se-nt-p]'); if (p) p.textContent = p.getAttribute(s === 'sold' ? 'data-ended' : 'data-soon');
    if (on && !this.flashed && !matchMedia('(prefers-reduced-motion: reduce)').matches) { this.q('[data-se-stage]').classList.add('is-flash'); this.flashed = true; }
  };

  Edition.prototype.bind = function () {
    var self = this, form = this.q('[data-se-form]');
    this.on(this.q('[data-se-pause]'), 'click', function () {
      self.paused = !self.paused;
      this.setAttribute('aria-pressed', String(self.paused));
      this.textContent = self.paused ? 'Resume timer' : 'Pause timer';
      if (!self.paused && self.tick) self.tick();
    });
    this.on(this.q('[data-se-sizes]'), 'change', function (e) {
      var v = self.q('[data-se-size-v]'); if (v) v.textContent = e.target.value;
      this.classList.remove('is-error'); self.q('[data-se-msg]').textContent = '';
      self.q('[data-se-id]').value = e.target.getAttribute('data-variant') || '';
    });
    this.on(form, 'submit', function (e) {
      var msg = self.q('[data-se-add-msg]'); msg.textContent = '';
      if (self.state(Date.now()) !== 'live') { e.preventDefault(); self.apply(); return; }
      var fs = self.q('[data-se-sizes]'), id = self.q('[data-se-id]').value;
      if (fs && !fs.querySelector('input:checked')) {
        e.preventDefault();
        fs.classList.add('is-error'); self.q('[data-se-msg]').textContent = 'Select a size to add it to your cart.';
        var f = fs.querySelector('input:not(:disabled)'); if (f) f.focus();
        return;
      }
      if (!id || !window.HMCart) return;
      e.preventDefault();
      var btn = self.q('[data-se-add]'), old = btn.textContent;
      btn.setAttribute('aria-busy', 'true'); btn.textContent = 'Adding…';
      window.HMCart.add([{ id: Number(id), quantity: 1 }], { returnFocus: btn })
        .catch(function (err) { msg.textContent = err.message; })
        .then(function () { btn.removeAttribute('aria-busy'); btn.textContent = old; });
    });
  };

  /* past editions: closed (end date passed) or sold out; year filter */
  Edition.prototype.past = function () {
    var self = this, arch = this.q('[data-se-arch]'); if (!arch) return;
    var now = Date.now();
    var items = [].slice.call(arch.querySelectorAll('[data-ed]')).filter(function (li) {
      var end = Number(li.getAttribute('data-end')) * 1000;
      var closed = li.getAttribute('data-available') === 'false' || (end && end < now);
      if (!closed) li.remove();
      return closed;
    });
    var yrs = this.q('[data-se-yrs]'), years = [];
    items.forEach(function (li) { var y = li.getAttribute('data-year'); if (y && years.indexOf(y) < 0) years.push(y); });
    years.sort(function (a, b) { return b - a; });
    var cur = 'all';
    function render() {
      var shown = items.filter(function (li) { var ok = cur === 'all' || li.getAttribute('data-year') === cur; li.hidden = !ok; return ok; });
      arch.classList.toggle('is-wide', shown.length > 0 && shown.length <= 2);
      arch.classList.toggle('is-two', shown.length === 2);
      self.q('[data-se-empty]').hidden = shown.length > 0;
      self.q('[data-se-past-count]').textContent = items.length ? shown.length + (shown.length === 1 ? ' edition' : ' editions') + ' · ' + (cur === 'all' ? 'all years' : cur) : '';
      if (yrs) {
        yrs.hidden = years.length < 2;
        yrs.innerHTML = years.concat(['all']).map(function (y) {
          var n = y === 'all' ? items.length : items.filter(function (li) { return li.getAttribute('data-year') === y; }).length;
          return '<button type="button" class="chip" data-y="' + y + '" aria-pressed="' + (cur === y) + '">' + (y === 'all' ? 'All' : y) + '<span class="n">' + n + '</span></button>';
        }).join('');
      }
    }
    this.on(yrs, 'click', function (e) {
      var b = e.target.closest('[data-y]'); if (!b) return;
      cur = b.getAttribute('data-y'); render();
      var f = yrs.querySelector('[data-y="' + cur + '"]'); if (f) f.focus();
    });
    render();
  };

  Edition.prototype.destroy = function () {
    clearInterval(this.timer);
    this.handlers.forEach(function (h) { h[0].removeEventListener(h[1], h[2]); });
  };

  var inst = new Map();
  function init(scope) {
    [].forEach.call((scope || document).querySelectorAll('[data-hm-se]'), function (r) { if (!inst.has(r)) inst.set(r, new Edition(r)); });
  }
  document.addEventListener('shopify:section:load', function (e) { init(e.target); });
  document.addEventListener('shopify:section:unload', function (e) {
    inst.forEach(function (x, r) { if (e.target.contains(r)) { x.destroy(); inst.delete(r); } });
  });
  /* back from another tab or bfcache: recompute the state */
  document.addEventListener('visibilitychange', function () { if (!document.hidden) inst.forEach(function (x) { if (x.q('[data-se-badge]')) x.apply(); }); });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { init(); }); else init();
})();
