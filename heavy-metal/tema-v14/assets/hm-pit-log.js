/* Pit Log: Load more and type filters through the Section Rendering API, season filter by published year
   (loads more pages when needed), search through the store search (articles only, this blog only),
   and arrows for the Wins & milestones strip. Editor safe (section load/unload). */
(function () {
  if (window.hmPitLog) return;
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function withSection(url, id) { return url + (url.indexOf('?') > -1 ? '&' : '?') + 'section_id=' + encodeURIComponent(id); }
  function fetchSection(url, id) {
    return fetch(withSection(url, id), { credentials: 'same-origin' }).then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.text();
    }).then(function (html) { return new DOMParser().parseFromString(html, 'text/html'); });
  }
  function handleize(s) { return String(s || '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, ''); }

  function PitLog(root) {
    var log = root.querySelector('[data-pl-log]');
    if (!log) return;
    var id = log.getAttribute('data-section-id');
    var blogHandle = log.getAttribute('data-blog-handle');
    var searchUrl = log.getAttribute('data-search-url') || '/search/suggest';
    var fullSearch = log.getAttribute('data-full-search') || '/search';
    var state = { year: 'all', q: '', saved: null, busy: false };
    var qt = 0, ctrl = null;

    function main() { return log.querySelector('[data-pl-main]'); }
    function list() { return log.querySelector('[data-pl-list]'); }
    function countEl() { return log.querySelector('[data-pl-count]'); }
    function moreLink() { return log.querySelector('[data-pl-load]'); }

    /* ---------- season filter (published year) ---------- */
    function applyYear() {
      var items = list() ? list().querySelectorAll('.pl-entry') : [];
      var shown = 0, oldest = null;
      Array.prototype.forEach.call(items, function (li) {
        var y = li.getAttribute('data-year');
        var ok = state.year === 'all' || y === state.year;
        li.hidden = !ok;
        if (ok) shown++;
        if (y) oldest = y;
      });
      var empty = list() && list().querySelector('[data-pl-year-empty]');
      if (empty) empty.remove();
      if (state.year !== 'all') {
        var c = countEl();
        if (c) c.textContent = shown + (shown === 1 ? ' entry' : ' entries') + ' from ' + state.year + (moreLink() ? ' so far' : '');
        /* newest first: keep loading while this page may still hold older entries of the chosen year */
        if (shown < 10 && moreLink() && oldest && oldest >= state.year && !state.busy) { loadMore(false); return; }
        if (!shown && list()) list().insertAdjacentHTML('beforeend', '<li class="pl-empty" data-pl-year-empty><p class="h3">Nothing logged in ' + esc(state.year) + '</p><p>Try another season or type.</p></li>');
      }
    }

    /* ---------- load more ---------- */
    function loadMore(focus) {
      var a = moreLink();
      if (!a || state.busy) return;
      state.busy = true;
      a.setAttribute('aria-busy', 'true');
      var firstNew = list().children.length;
      fetchSection(a.getAttribute('href'), id).then(function (doc) {
        var newList = doc.querySelector('[data-pl-list]');
        var newMore = doc.querySelector('[data-pl-more]');
        var newCount = doc.querySelector('[data-pl-count]');
        if (newList) Array.prototype.forEach.call(newList.querySelectorAll('.pl-entry'), function (li) { list().appendChild(document.importNode(li, true)); });
        var more = log.querySelector('[data-pl-more]');
        if (more && newMore) more.innerHTML = newMore.innerHTML;
        if (countEl() && newCount) countEl().textContent = newCount.textContent;
        state.busy = false;
        applyYear();
        if (focus) {
          var li = list().children[firstNew];
          var card = li && !li.hidden && li.querySelector('.pl-card');
          if (card) card.focus();
        }
      }).catch(function () {
        state.busy = false;
        window.location.href = a.getAttribute('href');
      });
    }

    /* ---------- type filter (tag pages) ---------- */
    function loadType(a) {
      var url = a.getAttribute('href');
      fetchSection(url, id).then(function (doc) {
        var m = doc.querySelector('[data-pl-main]');
        if (m && main()) main().innerHTML = m.innerHTML;
        log.querySelectorAll('[data-pl-type]').forEach(function (x) { x.setAttribute('aria-current', x === a ? 'true' : 'false'); });
        try { history.replaceState(null, '', url); } catch (e) {}
        state.saved = null;
        var input = log.querySelector('[data-pl-search] input[name="q"]');
        if (input) input.value = '';
        state.q = '';
        applyYear();
        a.focus();
      }).catch(function () { window.location.href = url; });
    }

    /* ---------- search (store search, articles of this blog only) ---------- */
    function hl(s, q) {
      var out = esc(s);
      q.trim().split(/\s+/).filter(function (w) { return w.length > 1; }).forEach(function (w) {
        var re = new RegExp('(' + esc(w).replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')(?![^<]*>)', 'ig');
        out = out.replace(re, '<mark>$1</mark>');
      });
      return out;
    }
    function typeOf(tags) {
      var t = (tags || []).map(function (x) { return String(x).toLowerCase(); });
      return t.indexOf('win') > -1 ? 'Win' : t.indexOf('competition') > -1 ? 'Competition' : t.indexOf('exhibition') > -1 ? 'Exhibition' : 'Test';
    }
    function typePhoto(type) {
      var tpl = log.querySelector('template[data-pl-type-photos]');
      var el = tpl && tpl.content.querySelector('[data-type="' + type + '"]');
      return el ? el.innerHTML : '';
    }
    function entryHtml(a, q) {
      var d = a.published_at ? new Date(a.published_at) : null;
      var tags = (a.tags || []).filter(function (t) { return String(t).toLowerCase() !== 'featured'; });
      var lower = (a.tags || []).map(function (t) { return String(t).toLowerCase(); });
      var cls = (lower.indexOf('win') > -1 ? ' is-win' : '') + (lower.indexOf('milestone') > -1 ? ' is-mile' : '');
      var img = a.image ? '<img class="photo" src="' + esc(a.image) + (a.image.indexOf('?') > -1 ? '&' : '?') + 'width=400" alt="" loading="lazy" width="400" height="300">' : typePhoto(typeOf(a.tags));
      var text = String(a.summary_html || a.body || '').replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim().split(' ').slice(0, 32).join(' ');
      return '<li class="pl-entry' + cls + '" data-year="' + (d ? d.getFullYear() : '') + '"><div class="pl-when">' +
        (d ? '<b>' + d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) + '</b><span>' + d.getFullYear() + '</span>' : '') + '</div>' +
        '<article class="pl-card" tabindex="-1"><div class="pl-card__pic">' + img + '</div><div class="pl-card__body"><div class="pl-tags">' +
        tags.map(function (t) { return '<span class="badge pl-t-' + handleize(t) + '">' + esc(t) + '</span>'; }).join('') + '</div>' +
        '<h3 class="h3"><a href="' + esc(a.url) + '">' + hl(a.title, q) + '<span class="arw" aria-hidden="true">→</span></a></h3><p>' + hl(text, q) + '</p></div></article></li>';
    }
    function restore() {
      if (!state.saved) return;
      main().innerHTML = '';
      main().appendChild(state.saved);
      state.saved = null;
      applyYear();
    }
    function search(q) {
      state.q = q;
      if (q.trim().length < 2) { restore(); return; }
      if (ctrl && ctrl.abort) ctrl.abort();
      ctrl = window.AbortController ? new AbortController() : null;
      var url = searchUrl + '.json?q=' + encodeURIComponent(q.trim()) + '&resources[type]=article&resources[limit]=10&resources[options][prefix]=last&resources[options][fields]=title,body,tag';
      fetch(url, { credentials: 'same-origin', signal: ctrl ? ctrl.signal : undefined }).then(function (r) { return r.json(); }).then(function (json) {
        var arts = (json && json.resources && json.resources.results && json.resources.results.articles) || [];
        arts = arts.filter(function (a) { return String(a.url || '').indexOf('/blogs/' + blogHandle + '/') > -1; });
        if (!state.saved) {
          state.saved = document.createDocumentFragment();
          while (main().firstChild) state.saved.appendChild(main().firstChild);
        }
        var all = fullSearch + '?type=article&q=' + encodeURIComponent(q.trim());
        main().innerHTML = '<p class="pl-count" role="status" aria-live="polite">' + arts.length + (arts.length === 1 ? ' entry' : ' entries') + ' match “' + esc(q.trim()) + '”</p>' +
          (arts.length ? '<ol class="pl-list">' + arts.map(function (a) { return entryHtml(a, q); }).join('') + '</ol>' +
            '<div class="pl-more"><a class="link" href="' + esc(all) + '">See every result</a><button type="button" class="btn btn--ghost btn--sm" data-pl-clear>Clear search</button></div>'
          : '<div class="pl-empty"><p class="h3">No entries match “' + esc(q.trim()) + '”</p><p>Check the spelling or try one word.</p><div class="btn-row"><button type="button" class="btn btn--ghost btn--sm" data-pl-clear>Clear search</button></div></div>');
      }).catch(function (e) { if (e && e.name === 'AbortError') return; });
    }

    /* ---------- featured strip ---------- */
    function track() { return root.querySelector('[data-wm-track]'); }
    function arrowsState() {
      var tr = track(), arws = root.querySelector('[data-wm-arws]');
      if (!arws) return;
      if (!tr) { arws.hidden = true; return; }
      arws.hidden = +tr.getAttribute('data-count') <= 3 && tr.scrollWidth <= tr.clientWidth + 2;
      var b = arws.querySelectorAll('[data-wm-move]');
      b[0].disabled = tr.scrollLeft < 4;
      b[1].disabled = tr.scrollLeft + tr.clientWidth >= tr.scrollWidth - 4;
    }
    function slide(dir) {
      var tr = track(); if (!tr) return;
      var card = tr.querySelector('.pl-mile'), step = card ? card.getBoundingClientRect().width + 4 : tr.clientWidth;
      var per = Math.max(1, Math.round(tr.clientWidth / step));
      tr.scrollBy({ left: dir * step * per, behavior: reduce ? 'auto' : 'smooth' });
    }
    var wmWrap = root.querySelector('[data-wm-src]');
    if (wmWrap) {
      fetchSection(wmWrap.getAttribute('data-wm-src'), id).then(function (doc) {
        var w = doc.querySelector('[data-wm-wrap]');
        if (w) { wmWrap.innerHTML = w.innerHTML; bindTrack(); arrowsState(); }
      }).catch(function () {});
    }
    function bindTrack() { var tr = track(); if (tr && !tr.hmBound) { tr.addEventListener('scroll', arrowsState, { passive: true }); tr.hmBound = true; } }
    bindTrack();
    arrowsState();

    /* ---------- events ---------- */
    function onClick(e) {
      var t = e.target;
      var mv = t.closest('[data-wm-move]'); if (mv) { slide(+mv.getAttribute('data-wm-move')); return; }
      var lm = t.closest('[data-pl-load]'); if (lm) { e.preventDefault(); loadMore(true); return; }
      var ty = t.closest('a[data-pl-type]'); if (ty && log.contains(ty)) { e.preventDefault(); loadType(ty); return; }
      var yr = t.closest('[data-year]');
      if (yr && yr.classList.contains('chip')) {
        state.year = yr.getAttribute('data-year');
        log.querySelectorAll('[data-pl-years] [data-year]').forEach(function (b) { b.setAttribute('aria-pressed', b === yr ? 'true' : 'false'); });
        if (state.saved) restore();
        applyYear();
        return;
      }
      if (t.closest('[data-pl-clear]')) {
        var input = log.querySelector('[data-pl-search] input[name="q"]');
        if (input) { input.value = ''; input.focus(); }
        state.q = ''; restore();
      }
    }
    function onInput(e) {
      if (!e.target.matches('[data-pl-search] input[name="q"]')) return;
      var v = e.target.value;
      clearTimeout(qt);
      qt = setTimeout(function () { search(v); }, 250);
    }
    function onSubmit(e) {
      var f = e.target.closest('[data-pl-search]'); if (!f) return;
      e.preventDefault();
      clearTimeout(qt);
      search(f.querySelector('input[name="q"]').value);
    }
    function onKey(e) {
      if (!e.target.matches || !e.target.matches('[data-wm-track]')) return;
      if (e.key === 'ArrowRight') { e.preventDefault(); slide(1); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); slide(-1); }
    }
    root.addEventListener('click', onClick);
    root.addEventListener('input', onInput);
    root.addEventListener('submit', onSubmit);
    root.addEventListener('keydown', onKey);
    window.addEventListener('resize', arrowsState);

    this.destroy = function () {
      clearTimeout(qt);
      if (ctrl && ctrl.abort) ctrl.abort();
      root.removeEventListener('click', onClick);
      root.removeEventListener('input', onInput);
      root.removeEventListener('submit', onSubmit);
      root.removeEventListener('keydown', onKey);
      window.removeEventListener('resize', arrowsState);
    };
  }

  function rootsIn(scope) {
    var out = [];
    (scope || document).querySelectorAll('[data-pl-log]').forEach(function (l) {
      var r = l.closest('.shopify-section') || l.parentNode;
      if (out.indexOf(r) < 0) out.push(r);
    });
    return out;
  }
  function initAll(scope) { rootsIn(scope).forEach(function (r) { if (!r.hmPitLog) r.hmPitLog = new PitLog(r); }); }
  document.addEventListener('shopify:section:load', function (e) { initAll(e.target); });
  document.addEventListener('shopify:section:unload', function (e) {
    rootsIn(e.target).forEach(function (r) { if (r.hmPitLog && r.hmPitLog.destroy) r.hmPitLog.destroy(); r.hmPitLog = null; });
  });
  window.hmPitLog = { init: initAll };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { initAll(); });
  else initAll();
})();
