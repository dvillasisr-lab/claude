/* The full story: places the print and year-note blocks next to the matching H2 of the page content,
   adds the quote credit, computes the reading time (words / 200) and drives the reading progress bar.
   Editor safe: re-runs on shopify:section:load, removes listeners and cancels rAF on unload. */
(function () {
  if (window.hmFullStory) return;

  function setup(root) {
    if (!root || root.hmFs) return;
    var body = root.querySelector('[data-fs-body]');
    var parts = root.querySelector('[data-fs-parts]');
    if (!body) return;
    var h2s = Array.prototype.slice.call(body.querySelectorAll('h2'));

    /* year notes: inside the heading, first child (CSS moves it to the left margin on desktop) */
    if (parts) {
      parts.querySelectorAll('[data-fs-note]').forEach(function (n) {
        var h = h2s[(+n.getAttribute('data-h') || 1) - 1];
        if (h) h.insertBefore(n, h.firstChild);
      });
      /* prints: after the heading, or after its 1st / 2nd paragraph */
      parts.querySelectorAll('[data-fs-print]').forEach(function (f) {
        var h = h2s[(+f.getAttribute('data-h') || 1) - 1];
        if (!h) return;
        var at = f.getAttribute('data-at');
        var want = at === 'p2' ? 2 : at === 'p1' ? 1 : 0;
        var ref = h, seen = 0, el = h.nextElementSibling;
        while (seen < want && el && el.tagName !== 'H2') {
          if (el.tagName === 'P') { seen++; ref = el; }
          el = el.nextElementSibling;
        }
        ref.parentNode.insertBefore(f, ref.nextSibling);
      });
      if (!parts.querySelector('[data-fs-print], [data-fs-note]')) parts.hidden = true;
    }

    /* quote credit under the first quote */
    var credit = root.getAttribute('data-quote-credit');
    var bq = body.querySelector('blockquote');
    if (credit && bq && !bq.querySelector('footer')) {
      var ft = document.createElement('footer');
      ft.textContent = credit;
      bq.appendChild(ft);
    }

    /* reading time */
    var rt = root.querySelector('[data-fs-rt]');
    if (rt) {
      var words = (body.innerText || body.textContent || '').split(/\s+/).filter(Boolean).length;
      var min = Math.max(1, Math.round(words / 200));
      rt.textContent = (rt.textContent.indexOf('[min]') > -1 ? rt.textContent : '[min] min read').replace('[min]', min);
      rt.hidden = false;
    }

    /* reading progress */
    var bar = root.querySelector('[data-fs-bar]');
    var raf = 0;
    function prog() {
      raf = 0;
      var r = body.getBoundingClientRect(), total = r.height - window.innerHeight * 0.6;
      var p = Math.min(1, Math.max(0, -r.top / (total > 0 ? total : 1)));
      if (bar) bar.style.transform = 'scaleX(' + p.toFixed(4) + ')';
    }
    function onScroll() { if (!raf) raf = requestAnimationFrame(prog); }
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    prog();

    root.hmFs = function () {
      window.removeEventListener('scroll', onScroll);
      window.removeEventListener('resize', onScroll);
      if (raf) cancelAnimationFrame(raf);
      root.hmFs = null;
    };
  }

  function initAll(scope) { (scope || document).querySelectorAll('[data-fs]').forEach(setup); }

  document.addEventListener('shopify:section:load', function (e) { initAll(e.target); });
  document.addEventListener('shopify:section:unload', function (e) {
    e.target.querySelectorAll('[data-fs]').forEach(function (r) { if (r.hmFs) r.hmFs(); });
  });
  window.hmFullStory = { init: initAll };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { initAll(); });
  else initAll();
})();
