/* Heavy Metal Pro Stock: “The Evil One” · coupon ticket (snippets/hm-coupon.liquid).
   Shows the ticket only inside its start/end window (visitor's clock) and copies the code. */
(function () {
  'use strict';
  if (window.HMCoupon) return;

  /* "2026-10-10" = local midnight (end: 23:59:59 that day); "2026-10-10T09:00" = local time; anything with a zone is honored */
  function parse(s, end) {
    if (!s) return null;
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(s.trim());
    if (m) return end ? new Date(+m[1], m[2] - 1, +m[3], 23, 59, 59, 999) : new Date(+m[1], m[2] - 1, +m[3]);
    var d = new Date(s.trim());
    return isNaN(d.getTime()) ? null : d;
  }
  function inWindow(el, now) {
    var a = parse(el.getAttribute('data-start'), false), b = parse(el.getAttribute('data-end'), true);
    now = now || new Date();
    return !(a && now < a) && !(b && now > b);
  }
  function copy(text) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text);
    return new Promise(function (ok, ko) {
      var t = document.createElement('textarea');
      t.value = text; t.setAttribute('readonly', ''); t.style.position = 'fixed'; t.style.opacity = '0';
      document.body.appendChild(t); t.select();
      try { document.execCommand('copy') ? ok() : ko(); } catch (e) { ko(e); }
      t.remove();
    });
  }

  function init(scope) {
    [].forEach.call((scope || document).querySelectorAll('[data-hm-coupon]'), function (el) {
      if (!el.hasAttribute('data-start') && !el.hasAttribute('data-end')) return;
      var ok = inWindow(el), design = !!(window.Shopify && window.Shopify.designMode);
      /* theme editor: keep it visible but faded, so the owner can still find and edit it */
      el.hidden = !ok && !design;
      el.classList.toggle('is-out', !ok);
    });
  }

  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-cpn-copy]'); if (!b) return;
    var box = b.closest('[data-hm-coupon]'), code = box && box.querySelector('[data-cpn-code]');
    if (!code) return;
    var label = b.querySelector('[data-cpn-label]'), st = box.querySelector('[data-cpn-status]');
    function done(ok) {
      if (label) label.textContent = ok ? 'Copied' : 'Select it';
      if (st) st.textContent = ok ? 'Code copied. Paste it at checkout.' : 'Could not copy. Select the code and copy it.';
      b.classList.toggle('is-done', ok);
      if (!ok) { var r = document.createRange(); r.selectNodeContents(code); var s = getSelection(); s.removeAllRanges(); s.addRange(r); }
      clearTimeout(b._t);
      b._t = setTimeout(function () { if (label) label.textContent = 'Copy'; b.classList.remove('is-done'); if (st) st.textContent = ''; }, 2400);
    }
    copy(code.textContent.trim()).then(function () { done(true); }, function () { done(false); });
  });

  window.HMCoupon = { init: init, inWindow: inWindow };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { init(); }); else init();
  document.addEventListener('shopify:section:load', function (e) { init(e.target); });
})();
