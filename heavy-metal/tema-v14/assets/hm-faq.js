/* HM FAQ: search with result count and highlight, per-topic counts, current topic, Last updated date. */
(function () {
  'use strict';

  function fmtDate(v) {
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(v || '');
    if (!m) return v;
    return new Date(+m[1], +m[2] - 1, +m[3], 12).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
  }
  function esc(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
  function html(s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function reduced() { return window.matchMedia('(prefers-reduced-motion: reduce)').matches; }

  function init(root) {
    if (!root || root._hmFaq) return;
    var q = root.querySelector('[data-hc-q]');
    var form = root.querySelector('[data-hc-form]');
    var clear = root.querySelector('[data-hc-clear]');
    var count = root.querySelector('[data-hc-count]');
    var empty = root.querySelector('[data-hc-empty]');
    var term = root.querySelector('[data-hc-term]');
    var list = root.querySelector('[data-hc-list]');
    var cats = [].slice.call(root.querySelectorAll('[data-hc-cat]'));
    var items = [].slice.call(root.querySelectorAll('[data-hc-qa]'));
    var links = [].slice.call(root.querySelectorAll('[data-hc-link]'));
    var raf = 0;

    var lu = root.querySelector('[data-hc-lu]');
    if (lu) lu.textContent = fmtDate(lu.getAttribute('datetime'));

    function catFor(a) { return root.querySelector('[data-hc-cat][id="' + a.getAttribute('href').slice(1) + '"]'); }

    /* per-topic counts; hide topics with no questions */
    links.forEach(function (a) {
      var c = catFor(a);
      var n = c ? c.querySelectorAll('[data-hc-qa]').length : 0;
      if (!n) { a.parentNode.hidden = true; if (c) c.hidden = true; return; }
      var s = document.createElement('span');
      s.className = 'n'; s.setAttribute('aria-hidden', 'true'); s.textContent = n;
      a.appendChild(s);
    });
    cats = cats.filter(function (c) { return !c.hidden; });

    items.forEach(function (d) {
      var s = d.querySelector('summary');
      d._q = s.textContent.trim();
      s.innerHTML = '<span class="q"></span>';
      s.firstChild.textContent = d._q;
      d._text = (d._q + ' ' + d.querySelector('.a').textContent).toLowerCase();
    });

    function headerH() {
      var v = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--header'), 10);
      return isNaN(v) ? 56 : v;
    }

    function spy() {
      var off = headerH() + (window.innerWidth <= 860 ? 90 : 40);
      var cur = null;
      cats.forEach(function (c) { if (!c.hidden && c.getBoundingClientRect().top <= off) cur = c.id; });
      if (!cur) { var f = cats.filter(function (c) { return !c.hidden; })[0]; cur = f && f.id; }
      links.forEach(function (a) {
        if (a.getAttribute('href') === '#' + cur) {
          if (a.getAttribute('aria-current') !== 'true') {
            a.setAttribute('aria-current', 'true');
            if (list && list.scrollWidth > list.clientWidth) list.scrollLeft = a.parentNode.offsetLeft - 16;
          }
        } else a.removeAttribute('aria-current');
      });
    }

    function filter() {
      var raw = q.value.trim(), words = raw.toLowerCase().split(/\s+/).filter(Boolean), shown = 0;
      clear.hidden = !raw;
      items.forEach(function (d) {
        var s = d.querySelector('summary .q');
        var ok = words.every(function (w) { return d._text.indexOf(w) > -1; });
        d.hidden = !ok; if (ok) shown++;
        s.textContent = d._q;
        if (ok && words.length) {
          var re = new RegExp('(' + words.map(function (w) { return esc(html(w)); }).join('|') + ')', 'gi');
          s.innerHTML = html(d._q).replace(re, '<mark>$1</mark>');
        }
      });
      var few = words.length && shown <= 4;
      if (words.length) items.forEach(function (d) { d.open = few && !d.hidden; });
      cats.forEach(function (c) { c.hidden = !c.querySelector('[data-hc-qa]:not([hidden])'); });
      links.forEach(function (a) { var c = catFor(a); if (c && c.querySelector('[data-hc-qa]')) a.parentNode.hidden = c.hidden; });
      if (empty) empty.hidden = shown > 0 || !items.length;
      if (term) term.textContent = raw;
      count.textContent = words.length ? (shown === 1 ? '1 answer' : shown + ' answers') + ' for “' + raw + '”' : '';
      spy();
    }

    function onInput() { filter(); }
    function onSubmit(e) {
      e.preventDefault();
      var f = root.querySelector('[data-hc-qa]:not([hidden]) summary');
      if (f) f.focus();
    }
    function onClear() {
      q.value = '';
      items.forEach(function (d) { d.open = false; });
      filter(); q.focus();
    }
    function onScroll() {
      if (raf) return;
      raf = requestAnimationFrame(function () { raf = 0; spy(); });
    }
    function onLink(e) {
      var a = e.target.closest('[data-hc-link]');
      if (!a) return;
      var c = catFor(a);
      if (!c) return;
      e.preventDefault();
      c.scrollIntoView({ behavior: reduced() ? 'auto' : 'smooth' });
      history.replaceState(null, '', '#' + c.id);
      var s = c.querySelector('[data-hc-qa]:not([hidden]) summary');
      if (s) s.focus({ preventScroll: true });
    }

    q.addEventListener('input', onInput);
    form.addEventListener('submit', onSubmit);
    clear.addEventListener('click', onClear);
    if (list) list.addEventListener('click', onLink);
    window.addEventListener('scroll', onScroll, { passive: true });

    /* deep link to a question topic or ?q= search */
    var pq = new URLSearchParams(location.search).get('q');
    if (pq) { q.value = pq; filter(); } else spy();

    root._hmFaq = function () {
      q.removeEventListener('input', onInput);
      form.removeEventListener('submit', onSubmit);
      clear.removeEventListener('click', onClear);
      if (list) list.removeEventListener('click', onLink);
      window.removeEventListener('scroll', onScroll);
      if (raf) cancelAnimationFrame(raf);
      root._hmFaq = null;
    };
  }

  function initAll(scope) { [].forEach.call((scope || document).querySelectorAll('[data-hm-faq]'), init); }
  function destroyAll(scope) { [].forEach.call((scope || document).querySelectorAll('[data-hm-faq]'), function (r) { if (r._hmFaq) r._hmFaq(); }); }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { initAll(); });
  else initAll();
  document.addEventListener('shopify:section:load', function (e) { initAll(e.target); });
  document.addEventListener('shopify:section:unload', function (e) { destroyAll(e.target); });
})();
