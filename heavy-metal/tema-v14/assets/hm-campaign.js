/* HM v14 · campaign countdown (sections/hm-campaign-bar.liquid and sections/hm-campaign.liquid).
   layout/theme.liquid writes the start and end (ms) on <html> and sets data-hm-campaign = live | off before paint.
   This file ticks every countdown once a second and flips the state when the campaign starts or ends. */
(function () {
  var root = document.documentElement;
  if (root.hmCampaign) return;
  root.hmCampaign = true;
  var start = parseInt(root.getAttribute('data-hm-camp-start'), 10) || 0;
  var end = parseInt(root.getAttribute('data-hm-camp-end'), 10) || 0;
  if (!end) return;

  function pad(n) { return n < 10 ? '0' + n : String(n); }
  function parts(ms) {
    var s = Math.max(0, Math.floor(ms / 1000));
    return { d: Math.floor(s / 86400), h: Math.floor((s % 86400) / 3600), m: Math.floor((s % 3600) / 60), s: s % 60 };
  }
  function short(p) {
    return 'Ends in ' + (p.d ? p.d + 'd ' : '') + pad(p.h) + 'h ' + pad(p.m) + 'm ' + pad(p.s) + 's';
  }
  function spoken(p) {
    var out = [];
    if (p.d) out.push(p.d + (p.d === 1 ? ' day' : ' days'));
    out.push(p.h + (p.h === 1 ? ' hour' : ' hours'));
    out.push(p.m + (p.m === 1 ? ' minute' : ' minutes'));
    return 'Ends in ' + out.join(', ');
  }

  var timer = null, lastLabel = '';
  function tick() {
    var now = Date.now();
    var live = now < end && (!start || now >= start);
    var state = live ? 'live' : 'off';
    if (root.getAttribute('data-hm-campaign') !== state) {
      root.setAttribute('data-hm-campaign', state);
      document.dispatchEvent(new CustomEvent('hm:campaign', { detail: { state: state } }));
    }
    if (!live) {
      if (now >= end) { clearInterval(timer); return; }
      return; /* not started yet: keep checking */
    }
    var p = parts(end - now);
    var label = spoken(p);
    [].forEach.call(document.querySelectorAll('[data-hm-countdown]'), function (el) {
      if (el.getAttribute('data-format') === 'blocks') {
        ['d', 'h', 'm', 's'].forEach(function (k) {
          var u = el.querySelector('[data-u="' + k + '"]');
          if (u) u.textContent = k === 'd' ? String(p.d) : pad(p[k]);
        });
        if (label !== lastLabel) el.setAttribute('aria-label', label);
      } else {
        el.textContent = short(p);
        if (label !== lastLabel) el.setAttribute('aria-label', label);
      }
    });
    lastLabel = label;
  }
  tick();
  timer = setInterval(tick, 1000);
})();
