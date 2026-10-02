/* HM Policies: tabs (?p=key), anchors (#bsg), "On this page" rail, Last updated,
   and Shopify Customer Privacy API actions (opt-out switch, reopen cookie preferences). */
(function () {
  'use strict';

  function fmtDate(v) {
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(v || '');
    if (!m) return v || '';
    return new Date(+m[1], +m[2] - 1, +m[3], 12).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
  }
  function headerH() {
    var v = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--header'), 10);
    return isNaN(v) ? 56 : v;
  }

  /* Shopify Customer Privacy API, loaded on demand */
  function withPrivacy(cb) {
    var S = window.Shopify;
    if (S && S.customerPrivacy) { cb(S.customerPrivacy); return; }
    if (S && typeof S.loadFeatures === 'function') {
      S.loadFeatures([{ name: 'consent-tracking-api', version: '0.1' }], function (err) {
        cb(!err && window.Shopify.customerPrivacy ? window.Shopify.customerPrivacy : null);
      });
      return;
    }
    cb(null);
  }

  function initOptOut(box) {
    var input = box.querySelector('[data-optout-input]');
    var save = box.querySelector('[data-optout-save]');
    var status = box.querySelector('[data-status]');
    var gpcEl = box.querySelector('[data-gpc]');
    var gpc = navigator.globalPrivacyControl === true;
    if (gpc) {
      input.checked = true; input.disabled = true;
      if (gpcEl) gpcEl.textContent = gpcEl.getAttribute('data-on');
    }
    withPrivacy(function (cp) {
      if (cp && !gpc && typeof cp.saleOfDataAllowed === 'function') input.checked = !cp.saleOfDataAllowed();
    });
    function onSave() {
      var out = gpc || input.checked;
      withPrivacy(function (cp) {
        if (!cp || typeof cp.setTrackingConsent !== 'function') { status.textContent = status.getAttribute('data-unavailable'); return; }
        var consent = { sale_of_data: !out };
        if (out) consent.marketing = false;
        cp.setTrackingConsent(consent, function (res) {
          if (res && res.error) { status.textContent = status.getAttribute('data-unavailable'); return; }
          status.textContent = out ? status.getAttribute('data-saved-on') : status.getAttribute('data-saved-off');
        });
      });
    }
    save.addEventListener('click', onSave);
    return function () { save.removeEventListener('click', onSave); };
  }

  function initCookies(box) {
    var btn = box.querySelector('[data-cookie-open]');
    var status = box.querySelector('[data-status]');
    function onOpen() {
      status.textContent = '';
      var pb = window.privacyBanner;
      if (pb && typeof pb.showPreferences === 'function') { pb.showPreferences(); return; }
      withPrivacy(function () {
        var p = window.privacyBanner;
        if (p && typeof p.showPreferences === 'function') p.showPreferences();
        else status.textContent = status.getAttribute('data-unavailable');
      });
    }
    btn.addEventListener('click', onOpen);
    return function () { btn.removeEventListener('click', onOpen); };
  }

  function init(root) {
    if (!root || root._hmPolicies) return;
    var docs = [].slice.call(root.querySelectorAll('.pol-doc'));
    var links = [].slice.call(root.querySelectorAll('[data-pol-list] a[data-p]'));
    var list = root.querySelector('[data-pol-list]');
    var body = root.querySelector('[data-pol-main]');
    var crumb = root.querySelector('[data-pol-crumb]');
    var toc = root.querySelector('[data-pol-toc]');
    var tocList = root.querySelector('[data-pol-toc-list]');
    var railLuWrap = root.querySelector('[data-pol-rail-lu-wrap]');
    var railLu = root.querySelector('[data-pol-rail-lu]');
    var baseTitle = document.title;
    var cleanups = [];
    var raf = 0;

    docs.forEach(function (d) {
      var key = d.getAttribute('data-p');
      var lu = d.querySelector('[data-pol-lu]');
      var time = lu && lu.querySelector('time');
      var text = d.querySelector('[data-pol-text]');

      /* Last updated: block setting, or the "Last updated: ..." line at the top of the policy text */
      if (time && time.getAttribute('datetime')) {
        time.textContent = fmtDate(time.getAttribute('datetime'));
        lu.hidden = false;
      } else if (text && time) {
        var line = [].filter.call(text.querySelectorAll('p'), function (p) { return /^\s*last updated\s*:/i.test(p.textContent); })[0];
        if (line) {
          time.textContent = line.textContent.replace(/^\s*last updated\s*:\s*/i, '').trim();
          time.removeAttribute('datetime');
          line.parentNode.removeChild(line);
          lu.hidden = false;
        }
      }

      /* headings get ids for the rail; the Black Smoke Guarantee keeps #bsg */
      if (text) {
        /* theme rich text has no headings: a paragraph that is only "<strong>1. Title</strong>" becomes an h3 */
        [].forEach.call(text.querySelectorAll('p'), function (p) {
          var s = p.firstElementChild;
          if (!s || p.children.length !== 1 || !/^(STRONG|B)$/.test(s.tagName)) return;
          if (p.textContent.trim() !== s.textContent.trim() || !/^\d+\.\s/.test(s.textContent.trim())) return;
          var h = document.createElement('h3');
          h.textContent = s.textContent.trim();
          p.parentNode.replaceChild(h, p);
        });
        /* Shopify policy bodies often repeat the policy name as their first heading ("1. Refund policy"): drop it */
        var norm = function (s) { return (s || '').replace(/^\s*\d+\.\s*/, '').replace(/\s+/g, ' ').trim().toLowerCase(); };
        var firstH = text.querySelector('h1, h2, h3, h4');
        if (firstH && norm(firstH.textContent) === norm(d.getAttribute('data-name'))) firstH.parentNode.removeChild(firstH);
        /* plain-text subheads ("Lost packages"): a short line with no punctuation, followed by a longer paragraph */
        [].forEach.call(text.querySelectorAll(':scope > p'), function (p) {
          var t = p.textContent.trim();
          var next = p.nextElementSibling;
          if (!t || t.length > 60 || /[.:;!?,]$/.test(t) || t.indexOf(':') !== -1 || p.querySelector('a')) return;
          if (!next || next.tagName !== 'P' || next.textContent.trim().length < 80) return;
          var h = document.createElement('h3');
          h.textContent = t;
          p.parentNode.replaceChild(h, p);
        });
        [].forEach.call(text.querySelectorAll('h2, h3'), function (h, i) {
          if (!h.id && /black smoke guarantee/i.test(h.textContent) && !document.getElementById('bsg')) h.id = 'bsg';
          if (!h.id) h.id = key + '-' + (i + 1);
        });
      }

      var opt = d.querySelector('[data-pol-optout]');
      if (opt) cleanups.push(initOptOut(opt));
      var ck = d.querySelector('[data-pol-cookies]');
      if (ck) cleanups.push(initCookies(ck));
    });

    function rail(d) {
      var text = d.querySelector('[data-pol-text]');
      var hs = text ? text.querySelectorAll('h2, h3') : [];
      if (toc) toc.hidden = hs.length < 3;
      if (tocList) {
        tocList.textContent = '';
        [].forEach.call(hs, function (h) {
          var li = document.createElement('li');
          var a = document.createElement('a');
          a.href = '#' + h.id;
          a.textContent = h.textContent.replace(/\[[^\]]*\]/g, '').trim();
          li.appendChild(a); tocList.appendChild(li);
        });
      }
      var lu = d.querySelector('[data-pol-lu]:not([hidden]) time');
      if (railLuWrap) railLuWrap.hidden = !lu;
      if (railLu) railLu.textContent = lu ? lu.textContent : '';
    }

    function show(p, fromClick) {
      var target = docs.filter(function (d) { return d.getAttribute('data-p') === p; })[0];
      if (!target) {
        var def = root.getAttribute('data-default');
        target = docs.filter(function (d) { return d.getAttribute('data-p') === def; })[0] || docs[0];
      }
      if (!target) return;
      p = target.getAttribute('data-p');
      docs.forEach(function (d) { d.hidden = d !== target; });
      links.forEach(function (a) {
        var on = a.getAttribute('data-p') === p;
        if (on) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
        if (on && list && list.scrollWidth > list.clientWidth) list.scrollLeft = a.parentNode.offsetLeft - 16;
      });
      var name = target.getAttribute('data-name') || '';
      if (crumb) crumb.textContent = name;
      if (name) document.title = name + ' · ' + baseTitle;
      rail(target);
      if (fromClick) {
        var url = new URL(location.href); url.searchParams.set('p', p); url.hash = '';
        history.replaceState(null, '', url.pathname + url.search);
        var nav = root.querySelector('.pol-nav');
        var off = headerH() + (window.innerWidth <= 860 && nav ? nav.offsetHeight : 0) + 12;
        var top = body.getBoundingClientRect().top;
        if (top < off) window.scrollBy(0, top - off);
        body.focus({ preventScroll: true });
      }
    }

    /* links to another tab of this page (?p=key), from the nav or inside a policy text */
    function onClick(e) {
      var a = e.target.closest('a[href]');
      if (!a || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      var url;
      try { url = new URL(a.href, location.href); } catch (err) { return; }
      if (url.origin !== location.origin || url.pathname !== location.pathname) return;
      var p = url.searchParams.get('p');
      if (!p) return;
      e.preventDefault();
      show(p, true);
      if (url.hash.length > 1) jump(url.hash.slice(1));
    }

    function jump(id) {
      var el = document.getElementById(id);
      if (!el || !root.contains(el) || el.closest('[hidden]')) return;
      raf = requestAnimationFrame(function () {
        raf = 0;
        el.scrollIntoView({ block: 'start' });
        if (!el.hasAttribute('tabindex')) el.setAttribute('tabindex', '-1');
        el.focus({ preventScroll: true });
      });
    }

    root.addEventListener('click', onClick);
    var start = new URLSearchParams(location.search).get('p');
    var hash = location.hash.length > 1 ? decodeURIComponent(location.hash.slice(1)) : '';
    /* a bare #bsg (no ?p=) opens the tab that holds it */
    if (!start && hash) {
      var holder = document.getElementById(hash);
      var doc = holder && holder.closest('.pol-doc');
      if (doc && root.contains(doc)) start = doc.getAttribute('data-p');
    }
    show(start, false);
    if (hash) jump(hash);

    root._hmPolicies = function () {
      root.removeEventListener('click', onClick);
      cleanups.forEach(function (fn) { fn(); });
      if (raf) cancelAnimationFrame(raf);
      document.title = baseTitle;
      root._hmPolicies = null;
    };
  }

  function each(scope, fn) { [].forEach.call((scope || document).querySelectorAll('[data-hm-policies]'), fn); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { each(null, init); });
  else each(null, init);
  document.addEventListener('shopify:section:load', function (e) { each(e.target, init); });
  document.addEventListener('shopify:section:unload', function (e) { each(e.target, function (r) { if (r._hmPolicies) r._hmPolicies(); }); });
})();
