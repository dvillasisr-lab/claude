/* HM Size guide: tabs (?s=key) and in/cm toggle computed from the stored values. */
(function () {
  'use strict';
  var KEY = 'hm-unit';
  var NUM = /\d+(?:\.\d+)?/g;

  function convert(text, from, to) {
    if (from === to) return text;
    return text.replace(NUM, function (n) {
      var v = parseFloat(n);
      if (to === 'cm') return String(Math.round(v * 2.54 * 2) / 2);
      return String(Math.round((v / 2.54) * 4) / 4);
    });
  }

  function init(root) {
    if (!root || root._hmSizes) return;
    var docs = [].slice.call(root.querySelectorAll('.sz-doc'));
    var links = [].slice.call(root.querySelectorAll('[data-sz-list] a[data-s]'));
    var list = root.querySelector('[data-sz-list]');
    var body = root.querySelector('[data-sz-main]');
    var crumb = root.querySelector('[data-sz-crumb]');
    var baseTitle = document.title;
    var unit = 'in';
    try { unit = localStorage.getItem(KEY) === 'cm' ? 'cm' : 'in'; } catch (e) {}

    /* unit label on every header column that has numbers */
    [].forEach.call(root.querySelectorAll('[data-sz-table]'), function (t) {
      var heads = t.querySelectorAll('thead th');
      [].forEach.call(heads, function (th, i) {
        if (i === 0) return;
        var numeric = [].some.call(t.querySelectorAll('tbody tr'), function (tr) {
          var c = tr.children[i];
          return c && c.hasAttribute('data-v') && /\d/.test(c.getAttribute('data-v'));
        });
        if (numeric) { var s = document.createElement('span'); s.className = 'u'; s.setAttribute('data-u', ''); th.appendChild(document.createTextNode(' ')); th.appendChild(s); }
      });
    });

    function setUnit(u) {
      unit = u;
      try { localStorage.setItem(KEY, u); } catch (e) {}
      [].forEach.call(root.querySelectorAll('[data-sz-units] input'), function (r) { r.checked = r.value === u; });
      [].forEach.call(root.querySelectorAll('[data-u]'), function (s) { s.textContent = '(' + u + ')'; });
      [].forEach.call(root.querySelectorAll('[data-sz-table]'), function (t) {
        var from = t.getAttribute('data-unit') === 'cm' ? 'cm' : 'in';
        [].forEach.call(t.querySelectorAll('td[data-v]'), function (td) { td.textContent = convert(td.getAttribute('data-v'), from, u); });
      });
    }

    function show(s, fromClick) {
      var known = docs.some(function (d) { return d.getAttribute('data-s') === s; });
      if (!known) s = root.getAttribute('data-default') || (docs[0] && docs[0].getAttribute('data-s'));
      var name = '';
      docs.forEach(function (d) {
        var on = d.getAttribute('data-s') === s;
        d.hidden = !on;
        if (on) name = d.getAttribute('data-name') || '';
      });
      links.forEach(function (a) {
        var on = a.getAttribute('data-s') === s;
        if (on) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
        if (on && list && list.scrollWidth > list.clientWidth) list.scrollLeft = a.parentNode.offsetLeft - 16;
      });
      if (crumb) crumb.textContent = name;
      if (name) document.title = name + ' · ' + baseTitle;
      if (fromClick) {
        var url = new URL(location.href); url.searchParams.set('s', s); url.hash = '';
        history.replaceState(null, '', url.pathname + url.search);
        var nav = root.querySelector('.sz-nav');
        var hh = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--header'), 10) || 56;
        var off = hh + (window.innerWidth <= 860 && nav ? nav.offsetHeight : 0) + 12;
        var top = body.getBoundingClientRect().top;
        if (top < off) window.scrollBy(0, top - off);
        body.focus({ preventScroll: true });
      }
    }

    function onChange(e) { if (e.target.closest('[data-sz-units]')) setUnit(e.target.value); }
    function onClick(e) {
      var a = e.target.closest('a[data-s]');
      if (!a || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      e.preventDefault();
      show(a.getAttribute('data-s'), true);
    }
    root.addEventListener('change', onChange);
    root.addEventListener('click', onClick);
    setUnit(unit);
    show(new URLSearchParams(location.search).get('s'), false);

    root._hmSizes = function () {
      root.removeEventListener('change', onChange);
      root.removeEventListener('click', onClick);
      document.title = baseTitle;
      root._hmSizes = null;
    };
  }

  function each(scope, fn) { [].forEach.call((scope || document).querySelectorAll('[data-hm-sizes]'), fn); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { each(null, init); });
  else each(null, init);
  document.addEventListener('shopify:section:load', function (e) { each(e.target, init); });
  document.addEventListener('shopify:section:unload', function (e) { each(e.target, function (r) { if (r._hmSizes) r._hmSizes(); }); });
})();
