/* Heavy Metal Pro Stock: “The Evil One” · delivery timeline (snippets/hm-delivery.liquid).
   Counts business days (Monday to Friday) from today in the visitor's own time zone.
   Past the cut off hour, or on a weekend, the clock starts on the next business day. */
(function () {
  'use strict';
  if (window.HMDelivery) return;

  function num(el, k, d) { var n = parseInt(el.getAttribute(k), 10); return isNaN(n) ? d : n; }
  function isWeekend(d) { var w = d.getDay(); return w === 0 || w === 6; }
  function addBiz(from, n) {
    var d = new Date(from.getFullYear(), from.getMonth(), from.getDate());
    while (n > 0) { d.setDate(d.getDate() + 1); if (!isWeekend(d)) n--; }
    return d;
  }
  function fmt(d, now) {
    var o = { month: 'short', day: 'numeric' };
    if (d.getFullYear() !== now.getFullYear()) o.year = 'numeric';
    return d.toLocaleDateString('en-US', o);
  }

  function render(el, now) {
    now = now || new Date();
    var pmin = num(el, 'data-prod-min', 2), pmax = Math.max(pmin, num(el, 'data-prod-max', 5));
    var smin = num(el, 'data-ship-min', 2), smax = Math.max(smin, num(el, 'data-ship-max', 5));
    var cut = num(el, 'data-cutoff', 0);
    var late = cut > 0 && now.getHours() >= cut;
    /* weekend or past the cut off: production starts on the next business day (adds one day to the count) */
    var extra = (late && !isWeekend(now)) ? 1 : 0;
    var start = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    var a = addBiz(start, pmin + smin + extra), b = addBiz(start, pmax + smax + extra);
    var range = fmt(a, now) === fmt(b, now) ? fmt(a, now) : fmt(a, now) + ' to ' + fmt(b, now);

    var o = el.querySelector('[data-dlv-order]');
    if (o) o.textContent = 'Today, ' + fmt(now, now);
    var r = el.querySelector('[data-dlv-range]');
    if (r) r.textContent = range;
    var eta = el.querySelector('[data-dlv-eta]');
    if (eta) eta.textContent = range;
    var note = el.querySelector('[data-dlv-note]');
    if (note) {
      var msg = '';
      if (isWeekend(now)) msg = 'Weekend order. The printers clock in Monday.';
      else if (late) msg = 'Ordered after ' + (cut % 12 || 12) + (cut < 12 ? ' AM' : ' PM') + '? Printing starts the next business day.';
      else if (cut > 0) msg = 'Order before ' + (cut % 12 || 12) + (cut < 12 ? ' AM' : ' PM') + ' and the clock starts today.';
      note.textContent = msg;
      note.hidden = !msg;
    }
  }

  function init(scope) {
    [].forEach.call((scope || document).querySelectorAll('[data-hm-delivery]'), function (el) { render(el); });
  }
  window.HMDelivery = { init: init, render: render, addBiz: addBiz };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { init(); }); else init();
  document.addEventListener('shopify:section:load', function (e) { init(e.target); });
  document.addEventListener('shopify:block:select', function (e) { init(e.target.parentNode || document); });
})();
