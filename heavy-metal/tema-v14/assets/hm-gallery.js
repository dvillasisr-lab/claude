/* HM v14 · Gallery (sections/hm-gallery.liquid) and album page (sections/hm-album.liquid).
   - Gallery: reads the album JSON printed by Liquid, builds the wall (400 px thumbs, lazy), the Filter / Events
     panel, the All / Photos / Videos switch, chips, Load more and ?event= / ?year= / ?kind= / ?type= in the URL.
   - Viewer: one shared dialog. It loads the large photo only when it opens (plus the two neighbours).
     Keys: Left / Right, Home / End, Escape. Focus stays inside and returns to the tile on close.
     Slideshow every 4 s with a Pause button (and it stops on any manual move).
   - Re-inits on shopify:section:load and cleans up on shopify:section:unload. */
(function () {
  'use strict';

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var PLAY = '<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2 1l9 5-9 5z"/></svg>';
  var CAM = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h3l2-2h6l2 2h3v12H4Z M12 10a3 3 0 1 0 0 6 3 3 0 0 0 0-6Z" fill-rule="evenodd"/></svg>';
  var ZOOM = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/></svg>';
  var X = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 5l14 14M19 5 5 19"/></svg>';

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function plural(n, w) { return n + ' ' + w + (n === 1 ? '' : 's'); }
  function longDate(iso, short) {
    var p = String(iso).split('-');
    return new Date(+p[0], +p[1] - 1, +p[2] || 1).toLocaleDateString('en-US', { month: short ? 'short' : 'long', day: 'numeric', year: 'numeric' });
  }
  function ytId(url) {
    var m = String(url).match(/(?:v=|youtu\.be\/|\/shorts\/|\/embed\/|\/live\/)([A-Za-z0-9_-]{6,})/);
    return m ? m[1] : '';
  }
  function poster(a, v) {
    if (a.cover) return a.cover;
    var id = ytId(v.url);
    if (id) return 'https://i.ytimg.com/vi/' + id + '/hqdefault.jpg';
    return a.photos.length ? a.photos[0].t : '';
  }
  function whenShort(a) { return a.date ? longDate(a.date, true) : String(a.year); }
  function whenLong(a) { return a.date ? longDate(a.date) : String(a.year); }

  /* ---------------------------------------------------------------- viewer */
  var LB = null;
  function lightbox() {
    if (LB) return LB;
    var el = document.createElement('div');
    el.className = 'lb';
    el.setAttribute('role', 'dialog');
    el.setAttribute('aria-modal', 'true');
    el.setAttribute('aria-labelledby', 'hm-lb-title');
    el.hidden = true;
    el.innerHTML =
      '<div class="lb__top"><div class="lb__tt"><p class="lb__t" id="hm-lb-title"></p><p class="lb__n" aria-live="polite"></p></div>' +
      '<button class="lb__tool" type="button" data-lb-ev aria-pressed="false" hidden></button>' +
      '<button class="lb__tool" type="button" data-lb-play aria-pressed="false">' + PLAY + '<span class="tl">Slideshow</span><span class="vh"> (a new photo every 4 seconds)</span></button>' +
      '<button class="icon-btn" type="button" data-lb-close aria-label="Close photo viewer">' + X + '</button></div>' +
      '<div class="lb__stage" data-lb-stage><img class="lb__img" alt="" data-lb-img>' +
      '<button class="lb__arw lb__arw--prev" type="button" data-lb-prev aria-label="Previous photo"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg></button>' +
      '<button class="lb__arw lb__arw--next" type="button" data-lb-next aria-label="Next photo"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg></button></div>' +
      '<div class="lb__bot"><p class="lb__cap"></p><ul class="lb__thumbs" aria-label="All photos in this view"></ul></div>';
    document.body.appendChild(el);

    var q = function (s) { return el.querySelector(s); };
    var img = q('[data-lb-img]'), title = q('.lb__t'), count = q('.lb__n'), cap = q('.lb__cap'), thumbs = q('.lb__thumbs');
    var bPlay = q('[data-lb-play]'), bEv = q('[data-lb-ev]'), bPrev = q('[data-lb-prev]'), bNext = q('[data-lb-next]');
    var seq = [], base = null, i = 0, from = null, timer = null, thumbKey = '';

    function stop() {
      if (timer) clearInterval(timer);
      timer = null;
      bPlay.setAttribute('aria-pressed', 'false');
      bPlay.querySelector('.tl').textContent = 'Slideshow';
    }
    function evMode(on) {
      var it = seq[i];
      var a = it && it.a;
      bEv.setAttribute('aria-pressed', String(on));
      if (!a) { bEv.hidden = true; return; }
      var n = a.photos.length;
      bEv.innerHTML = on
        ? (base ? '<span>Back to all photos</span>' : '<span>Event · ' + plural(n, 'photo') + '</span>')
        : CAM + '<span><span class="tl">All from this event</span><span class="vh"> (' + plural(n, 'photo') + ')</span></span>';
      bEv.hidden = !on && (n < 2 || seq.length === n);
      bEv.disabled = on && !base;
    }
    function show() {
      var it = seq[i], a = it.a, p = it.p, n = seq.length;
      img.classList.add('is-loading');
      img.onload = function () { img.classList.remove('is-loading'); };
      img.width = p.w || 1050;
      img.height = p.h || 1400;
      img.alt = p.alt || '';
      img.src = p.l;
      if (img.complete) img.classList.remove('is-loading');
      title.textContent = a.event;
      count.textContent = (i + 1) + ' / ' + n;
      count.setAttribute('aria-label', 'Photo ' + (i + 1) + ' of ' + n);
      cap.innerHTML = '<b>' + esc(p.alt) + '</b><br>' + [whenLong(a), a.city, a.league].filter(Boolean).map(esc).join(' · ');
      bPrev.hidden = bNext.hidden = bPlay.hidden = n < 2;
      if (bEv.getAttribute('aria-pressed') !== 'true') evMode(false);
      var key = n + '|' + seq[0].p.t;
      if (key !== thumbKey) {
        thumbKey = key;
        thumbs.innerHTML = n < 2 ? '' : seq.map(function (x, k) {
          return '<li><button type="button" data-k="' + k + '" aria-label="Photo ' + (k + 1) + ' of ' + n + '"><img src="' + esc(x.p.t) + '" alt="" loading="lazy" width="44" height="58"></button></li>';
        }).join('');
      }
      Array.prototype.forEach.call(thumbs.querySelectorAll('button'), function (b, k) {
        b.setAttribute('aria-current', String(k === i));
        if (k === i) {
          var li = b.parentNode;
          thumbs.scrollLeft = li.offsetLeft - thumbs.clientWidth / 2 + li.offsetWidth / 2 - thumbs.offsetLeft;
        }
      });
      [i - 1, i + 1].forEach(function (k) {
        var nb = seq[(k + n) % n];
        if (nb && n > 1) { var pre = new Image(); pre.src = nb.p.l; }
      });
    }
    function go(d, keep) {
      var n = seq.length;
      if (n < 2) return;
      if (!keep) stop();
      i = (i + d + n) % n;
      show();
    }
    function close() {
      if (el.hidden) return;
      stop();
      el.hidden = true;
      document.documentElement.style.overflow = '';
      img.removeAttribute('src');
      if (from && document.contains(from)) from.focus();
      from = null;
    }
    function open(list, start, fromEl, eventOnly) {
      if (!list.length) return;
      seq = list;
      i = Math.max(0, start);
      from = fromEl || null;
      base = eventOnly ? null : { list: list };
      thumbKey = '';
      el.hidden = false;
      document.documentElement.style.overflow = 'hidden';
      evMode(!!eventOnly);
      show();
      q('[data-lb-close]').focus();
    }
    function seqOf(a) { return a.photos.map(function (p, k) { return { a: a, p: p, k: k }; }); }

    q('[data-lb-close]').addEventListener('click', close);
    bPrev.addEventListener('click', function () { go(-1); });
    bNext.addEventListener('click', function () { go(1); });
    thumbs.addEventListener('click', function (e) {
      var b = e.target.closest('button[data-k]');
      if (b) { stop(); i = +b.getAttribute('data-k'); show(); }
    });
    bEv.addEventListener('click', function () {
      var on = bEv.getAttribute('aria-pressed') === 'true', cur = seq[i];
      stop();
      if (!on) { seq = seqOf(cur.a); i = cur.k; evMode(true); }
      else if (base) {
        seq = base.list;
        i = 0;
        for (var k = 0; k < seq.length; k++) if (seq[k].a === cur.a && seq[k].k === cur.k) { i = k; break; }
        evMode(false);
      }
      thumbKey = '';
      show();
    });
    bPlay.addEventListener('click', function () {
      if (timer) { stop(); return; }
      bPlay.setAttribute('aria-pressed', 'true');
      bPlay.querySelector('.tl').textContent = 'Pause';
      timer = setInterval(function () { go(1, true); }, 4000);
    });
    var swiped = false, x0 = null, y0 = null, stage = q('[data-lb-stage]');
    stage.addEventListener('click', function (e) {
      if (swiped) { swiped = false; return; }
      if (e.target === stage) close();
    });
    stage.addEventListener('pointerdown', function (e) {
      if (e.target.closest('button')) return;
      x0 = e.clientX; y0 = e.clientY;
    });
    stage.addEventListener('pointerup', function (e) {
      if (x0 == null) return;
      var dx = e.clientX - x0, dy = e.clientY - y0;
      x0 = null;
      if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy)) {
        swiped = true;
        setTimeout(function () { swiped = false; }, 300);
        go(dx < 0 ? 1 : -1);
      }
    });
    stage.addEventListener('pointercancel', function () { x0 = null; });
    el.addEventListener('keydown', function (e) {
      var k = e.key;
      if (k === 'Escape') { e.preventDefault(); close(); return; }
      if (k === 'ArrowRight') { e.preventDefault(); go(1); return; }
      if (k === 'ArrowLeft') { e.preventDefault(); go(-1); return; }
      if (k === 'Home') { e.preventDefault(); stop(); i = 0; show(); return; }
      if (k === 'End') { e.preventDefault(); stop(); i = seq.length - 1; show(); return; }
      if (k === 'Tab') {
        var f = Array.prototype.filter.call(el.querySelectorAll('button'), function (b) { return !b.hidden && !b.disabled && b.offsetParent !== null; });
        var at = f.indexOf(document.activeElement);
        if (e.shiftKey && at <= 0) { e.preventDefault(); f[f.length - 1].focus(); }
        else if (!e.shiftKey && (at === f.length - 1 || at < 0)) { e.preventDefault(); f[0].focus(); }
      }
    });

    LB = { open: open, close: close, seqOf: seqOf, el: el };
    return LB;
  }

  /* ---------------------------------------------------------------- wall layout */
  function colsFor(w) { return w < 600 ? 2 : w < 900 ? 3 : w < 1240 ? 4 : w < 1640 ? 5 : 6; }
  function place(sizes, cols) {
    var grid = [], pos = [], rows = 0;
    function free(r, c, w, h) {
      if (c + w > cols) return false;
      for (var y = r; y < r + h; y++) for (var x = c; x < c + w; x++) if (grid[y] && grid[y][x]) return false;
      return true;
    }
    for (var i = 0; i < sizes.length; i++) {
      var w = Math.min(sizes[i][0], cols), h = sizes[i][1], done = false;
      for (var r = 0; !done; r++) for (var c = 0; c < cols && !done; c++) if (free(r, c, w, h)) {
        for (var y = r; y < r + h; y++) { grid[y] = grid[y] || []; for (var x = c; x < c + w; x++) grid[y][x] = i + 1; }
        pos.push([r, c, w, h]); rows = Math.max(rows, r + h); done = true;
      }
    }
    var holes = 0;
    for (var y2 = 0; y2 < rows; y2++) for (var x2 = 0; x2 < cols; x2++) if (!(grid[y2] && grid[y2][x2])) holes++;
    return { pos: pos, holes: holes, rows: rows, grid: grid };
  }
  /* tries big-tile combinations until no hole is left; otherwise the last row stretches to close it */
  function layout(items, cols) {
    var n = items.length, photoIdx = [], vidIdx = [];
    items.forEach(function (it, i) { (it.kind === 'photo' ? photoIdx : vidIdx).push(i); });
    var vOpts = cols <= 4 ? [[2, 2]] : [[3, 2], [2, 2], [4, 2]];
    var np = photoIdx.length;
    var target = cols < 3 ? Math.round(np / 6) : Math.max(np >= 5 ? 1 : 0, Math.round(np / 6));
    var maxB = Math.floor(np * 0.4), nbs = [];
    for (var b = 0; b <= maxB; b++) nbs.push(b);
    nbs.sort(function (x, y) { return Math.abs(x - target) - Math.abs(y - target) || y - x; });
    for (var vi = 0; vi < vOpts.length; vi++) for (var bi = 0; bi < nbs.length; bi++) {
      var nb = nbs[bi];
      var area = n - vidIdx.length + vidIdx.length * vOpts[vi][0] * vOpts[vi][1] + nb * 3;
      if (area % cols) continue;
      for (var off = 0; off < Math.min(np, 14) || off === 0; off++) {
        var sizes = items.map(function (it) { return it.kind === 'video' ? vOpts[vi] : [1, 1]; });
        for (var k = 0; k < nb; k++) sizes[photoIdx[(Math.floor((k + 0.5) * np / nb) + off) % np]] = [2, 2];
        var res = place(sizes, cols);
        if (!res.holes) return res;
      }
    }
    var baseSizes = items.map(function (it) { return it.kind === 'video' ? vOpts[0] : [1, 1]; });
    for (var k2 = 0; k2 < Math.min(target, np); k2++) baseSizes[photoIdx[Math.floor((k2 + 0.5) * np / Math.max(target, 1))]] = [2, 2];
    var best = place(baseSizes, cols);
    var last = best.rows - 1, guard = 0, grew = true;
    while (best.holes && grew && guard++ < 40) {
      grew = false;
      for (var i = best.pos.length - 1; i >= 0; i--) {
        var p = best.pos[i];
        if (p[0] + p[3] - 1 !== last) continue;
        var rc = p[1] + p[2], okR = rc < cols;
        for (var y = p[0]; okR && y < p[0] + p[3]; y++) if (best.grid[y] && best.grid[y][rc]) okR = false;
        if (okR) {
          for (var y3 = p[0]; y3 < p[0] + p[3]; y3++) best.grid[y3][rc] = i + 1;
          p[2]++; best.holes -= p[3]; grew = true;
        }
      }
    }
    return best;
  }

  /* ---------------------------------------------------------------- gallery app */
  function Gallery(root) {
    this.root = root;
    var self = this;
    var q = function (s) { return root.querySelector(s); };
    var data = [];
    root.querySelectorAll('[data-g-data]').forEach(function (s) {
      try { data = data.concat(JSON.parse(s.textContent)); } catch (e) { /* bad JSON: show empty state */ }
    });
    var SEASON = +root.getAttribute('data-season') || new Date().getFullYear();
    var PAGE = +root.getAttribute('data-page') || 24;
    var TYPES = ['all', 'photos', 'videos'];
    var KINDS = [['all', 'All'], ['Competition', 'Competition'], ['Exhibition', 'Exhibition'], ['Test', 'Test']];
    var ALBUMS = data.filter(function (a) { return a && a.id; }).map(function (a) {
      a.photos = a.photos || []; a.videos = a.videos || []; a.year = +a.year || SEASON; return a;
    });
    var url = new URLSearchParams(location.search);
    var st = { year: url.get('year') === 'all' ? 'all' : (+url.get('year') || SEASON), type: url.get('type') || 'all', kind: 'all', event: url.get('event') || '', shown: PAGE };
    KINDS.forEach(function (k) { if (k[0] !== 'all' && k[0].toLowerCase() === String(url.get('kind') || '').toLowerCase()) st.kind = k[0]; });
    if (TYPES.indexOf(st.type) < 0) st.type = 'all';
    function byEvent(id) { for (var i = 0; i < ALBUMS.length; i++) if (ALBUMS[i].id === id) return ALBUMS[i]; return null; }
    var ev0 = st.event && byEvent(st.event);
    if (ev0) { st.year = ev0.year; st.type = 'all'; if (st.kind !== ev0.kind) st.kind = 'all'; }

    function sortKey(a) { return a.year * 1e7 + (a.date ? +a.date.replace(/-/g, '').slice(4) : 0) * 1000 + (+a.seq || 0); }
    function sorted(list) { return list.slice().sort(function (a, b) { return sortKey(b) - sortKey(a); }); }
    function years() {
      var y = [SEASON];
      ALBUMS.forEach(function (a) { if (y.indexOf(a.year) < 0) y.push(a.year); });
      return y.sort(function (a, b) { return b - a; });
    }
    function inYear(a) { return st.year === 'all' || a.year === st.year; }
    function inKind(a) { return st.kind === 'all' || a.kind === st.kind; }
    function inPool(a) { return inYear(a) && inKind(a); }
    function counts(a) {
      var c = [];
      if (a.photos.length) c.push(plural(a.photos.length, 'photo'));
      if (a.videos.length) c.push(plural(a.videos.length, 'video'));
      return c.join(' · ');
    }
    function itemsOf(list) {
      var out = [];
      sorted(list).forEach(function (a) {
        if (st.type !== 'photos') a.videos.forEach(function (v, k) { out.push({ a: a, kind: 'video', v: v, k: k }); });
        if (st.type !== 'videos') a.photos.forEach(function (p, k) { out.push({ a: a, kind: 'photo', p: p, k: k }); });
      });
      return out;
    }
    function yearLabel(y) { return y === 'all' ? 'All seasons' : String(y); }
    function cover(a) { return a.photos.length ? a.photos[0].t : a.videos.length ? poster(a, a.videos[0]) : a.cover; }
    function nItems() {
      if (st.event) { var ev = byEvent(st.event); return ev ? itemsOf([ev]).length : 0; }
      return itemsOf(ALBUMS.filter(inPool)).length;
    }

    /* header, bar, chips */
    function renderTop() {
      var newest = ALBUMS.reduce(function (m, a) { return a.date && a.date > m ? a.date : m; }, '');
      q('[data-g-updwrap]').hidden = !newest;
      if (newest) q('[data-g-updated]').textContent = longDate(newest);
      var n = nItems(), ev = st.event && byEvent(st.event);
      var what = st.type === 'photos' ? 'photo' : st.type === 'videos' ? 'video' : 'item';
      var bw = q('[data-g-barwrap]'); if (bw) bw.hidden = !ALBUMS.length;
      q('[data-g-count]').textContent = !ALBUMS.length ? SEASON + ' season' : plural(n, what) + (ev ? ' · ' + ev.event : st.year === SEASON && st.kind === 'all' ? ' · ' + SEASON : '');
      q('[data-g-view]').textContent = 'View ' + plural(n, what);
      q('[data-g-dsub]').textContent = plural(n, what) + (ev ? ' in ' + ev.event : '');
      var nf = (st.year !== SEASON ? 1 : 0) + (st.kind !== 'all' ? 1 : 0);
      q('[data-g-filter-v]').textContent = nf ? '(' + nf + ')' : '';
      q('[data-g-filter]').setAttribute('aria-label', 'Filter by season and event type' + (nf ? ', ' + plural(nf, 'filter') + ' on' : ''));
      q('[data-g-events-v]').textContent = ev ? ev.event : '';
      q('[data-g-events]').setAttribute('aria-label', 'Events' + (ev ? ', showing ' + ev.event : ', choose or search an event'));
      root.querySelectorAll('.g-media [data-type]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-type') === st.type)); });
      var chips = [];
      if (st.year !== SEASON) chips.push('<button type="button" class="g-chip" data-year="' + SEASON + '" aria-label="Remove filter: ' + esc(yearLabel(st.year)) + '">' + esc(yearLabel(st.year)) + X + '</button>');
      if (st.kind !== 'all') chips.push('<button type="button" class="g-chip" data-kind="all" aria-label="Remove filter: ' + esc(st.kind) + '">' + esc(st.kind) + X + '</button>');
      if (chips.length > 1) chips.push('<button type="button" class="g-chips__clear" data-year="' + SEASON + '" data-kind="all">Clear all</button>');
      var box = q('[data-g-chips]');
      box.innerHTML = chips.join('');
      box.hidden = !chips.length || !!st.event;
    }
    var uid = 'g' + Math.random().toString(36).slice(2, 7);
    function seg(name, list, cur) {
      return list.map(function (o, i) {
        var id = uid + name + i;
        return '<label for="' + id + '"><input type="radio" name="' + uid + name + '" data-name="' + name + '" id="' + id + '" value="' + esc(o[0]) + '"' + (String(cur) === String(o[0]) ? ' checked' : '') + '><span>' + esc(o[1]) + '</span></label>';
      }).join('');
    }
    var find = q('[data-g-find]');
    function norm(s) { return String(s).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, ''); }
    function hay(a) { return norm([a.event, a.kind, a.city, a.league, a.year, a.date ? longDate(a.date) : ''].join(' ')); }
    function mark(s, w) {
      var e = esc(s);
      if (!w) return e;
      var i = norm(s).indexOf(w);
      return i < 0 ? e : esc(s.slice(0, i)) + '<mark>' + esc(s.slice(i, i + w.length)) + '</mark>' + esc(s.slice(i + w.length));
    }
    function evOpt(id, img, title, sub) {
      var k = uid + 'ev' + (id || 'all').replace(/[^A-Za-z0-9_-]/g, '');
      return '<label for="' + k + '"><input type="radio" name="' + uid + 'ev" data-name="ev" id="' + k + '" value="' + esc(id) + '"' + (st.event === id ? ' checked' : '') + '><span>' + img + '<span><b>' + title + '</b><small>' + sub + '</small></span></span></label>';
    }
    function thumbImg(src) { return src ? '<img src="' + esc(src) + '" alt="" loading="lazy" width="34" height="44">' : ''; }
    function renderEvents() {
      var raw = find.value.trim(), words = norm(raw).split(/\s+/).filter(Boolean);
      var list = words.length
        ? sorted(ALBUMS).filter(function (a) { var h = hay(a); return words.every(function (w) { return h.indexOf(w) > -1; }); })
        : sorted(ALBUMS.filter(inPool));
      var cur = st.event && byEvent(st.event);
      if (!words.length && cur && list.indexOf(cur) < 0) list.unshift(cur);
      q('[data-g-evh]').textContent = words.length
        ? (list.length ? list.length + (list.length === 1 ? ' match' : ' matches') + ' in every season' : '')
        : plural(list.length, 'event') + ' · ' + yearLabel(st.year) + (st.kind === 'all' ? '' : ', ' + st.kind) + ', newest first';
      var html = '';
      if (!words.length) {
        var pics = [];
        ALBUMS.filter(inPool).forEach(function (a) { var c = cover(a); if (c && pics.length < 4) pics.push(c); });
        html += evOpt('', '<span class="g-evl__all" aria-hidden="true">' + pics.map(function (src) { return '<i>' + thumbImg(src) + '</i>'; }).join('') + '</span>', 'All events', esc(yearLabel(st.year)));
      }
      html += list.map(function (a) {
        return evOpt(a.id, '<span class="g-evl__img" aria-hidden="true">' + thumbImg(cover(a)) + '</span>', mark(a.event, words[0] || ''),
          esc([a.kind, whenShort(a), a.city].filter(Boolean).join(' · ') + ' · ' + (counts(a) || 'no media yet')));
      }).join('');
      if (words.length && !list.length) html = '<p class="g-evl__none">No events match “' + esc(raw) + '”. Try a town, a year or “exhibition”.</p>';
      q('[data-g-evl]').innerHTML = html;
    }
    function renderFilters() {
      q('[data-g-year]').innerHTML = seg('year', years().map(function (y) { return [y, String(y)]; }).concat([['all', 'All']]), st.year);
      q('[data-g-kind]').innerHTML = seg('kind', KINDS, st.kind);
      renderEvents();
    }

    /* wall */
    var WALLS = [];
    function tile(it, wallNo, i, few, colW) {
      var a = it.a, where = esc([whenShort(a), a.city].filter(Boolean).join(' · '));
      if (it.kind === 'video') {
        var v = it.v, src = poster(a, v);
        return '<li data-i="' + i + '"><a class="g-t g-t--vid" href="' + esc(v.url) + '" target="_blank" rel="noopener">' +
          (few && src ? '<img class="bg" src="' + esc(src) + '" alt="" aria-hidden="true" loading="lazy">' : '') +
          (src ? '<img class="photo" src="' + esc(src) + '" alt="" width="480" height="360" loading="lazy">' : '') +
          '<span class="badge g-kind" aria-hidden="true">Video</span><span class="g-play" aria-hidden="true">' + PLAY + '</span>' +
          '<span class="g-cap" aria-hidden="true"><b>' + esc(a.event) + '</b><span>' + where + ' · Watch the run ↗</span></span>' +
          '<span class="vh">' + esc(a.event) + ': watch the video (opens in a new tab)</span></a></li>';
      }
      var p = it.p;
      return '<li data-i="' + i + '"><button type="button" class="g-t" data-wall="' + wallNo + '" data-i="' + i + '" aria-label="' + esc('Open photo: ' + p.alt + '. ' + a.event + ', ' + whenShort(a)) + '">' +
        (few ? '<img class="bg" src="' + esc(p.t) + '" alt="" aria-hidden="true" loading="lazy">' : '') +
        '<img class="photo" src="' + esc(p.t) + '" srcset="' + esc(p.t) + ' 400w, ' + esc(p.m) + ' 800w" sizes="' + colW + 'px" alt="" width="' + (p.w || 1050) + '" height="' + (p.h || 1400) + '" loading="lazy">' +
        '<span class="g-zoom" aria-hidden="true">' + ZOOM + '</span>' +
        '<span class="g-cap" aria-hidden="true"><b>' + esc(a.event) + '</b><span>' + where + '</span></span></button></li>';
    }
    function paint(el, items, wallNo, limit) {
      WALLS[wallNo] = items;
      var shown = items.slice(0, limit);
      var w = el.parentNode.clientWidth || window.innerWidth, cols = colsFor(w), few = shown.length > 0 && shown.length <= 3;
      var areaMax = shown.reduce(function (s, it) { return s + (it.kind === 'video' ? 4 : 1); }, 0);
      if (!few && areaMax < cols * 2 && shown.length >= 2) cols = Math.max(2, Math.min(cols, shown.length));
      var colW = Math.round(w / (few ? shown.length || 1 : cols));
      el.classList.toggle('g-wall--few', few);
      el.style.setProperty('--cols', few ? shown.length : cols);
      el.innerHTML = shown.map(function (it, i) { return tile(it, wallNo, i, few, colW); }).join('');
      if (few) return shown.length;
      var res = layout(shown, cols), lis = el.children;
      res.pos.forEach(function (p, i) {
        lis[i].style.gridArea = (p[0] + 1) + ' / ' + (p[1] + 1) + ' / span ' + p[3] + ' / span ' + p[2];
        if (p[2] > 1) {
          var im = lis[i].querySelector('img.photo');
          if (im && im.getAttribute('srcset')) im.setAttribute('sizes', colW * p[2] + 'px');
        }
      });
      return shown.length;
    }
    function moreBtn(shown, total) {
      var left = total - shown;
      q('[data-g-more]').innerHTML = total > PAGE
        ? '<p>' + shown + ' of ' + total + '</p><span class="g-meter" aria-hidden="true"><span style="width:' + Math.round(shown / total * 100) + '%"></span></span>' +
          (left > 0 ? '<button type="button" class="btn btn--ghost" data-g-load>Load more<span class="vh">, ' + Math.min(PAGE, left) + ' of ' + left + ' left</span></button>'
                    : '<button type="button" class="btn btn--ghost btn--sm" data-g-top>Back to top</button>')
        : '';
    }
    function renderWalls(focusFrom) {
      var ev = st.event ? byEvent(st.event) : null, pool = ALBUMS.filter(inPool);
      var yl = (st.year === 'all' ? 'all seasons' : String(st.year)) + (st.kind === 'all' ? '' : ', ' + st.kind.toLowerCase());
      var wall = q('[data-g-wall]'), head = q('[data-g-evhead]'), rest = q('[data-g-rest]');
      rest.innerHTML = ''; head.innerHTML = '';
      if (st.event && !ev) {
        wall.innerHTML = ''; wall.className = 'g-wall';
        head.innerHTML = '<div class="g-empty"><p class="h3">No photos from this event yet</p><p>The crew posts photos and video after each pull. Check back soon, or browse every event.</p><button type="button" class="btn btn--ghost btn--sm" data-ev="">Show all events</button></div>';
        q('[data-g-more]').innerHTML = '';
        return;
      }
      if (ev) {
        var nPh = ev.photos.length, links = [];
        if (nPh > 1) links.push('<button type="button" class="btn btn--sm" data-playev="' + esc(ev.id) + '">' + CAM + 'View all ' + plural(nPh, 'photo') + '</button>');
        if (ev.url) links.push('<a href="' + esc(ev.url) + '">Album page<span class="vh"> for ' + esc(ev.event) + '</span></a>');
        if (ev.log) links.push('<a href="' + esc(ev.log) + '">Pit Log<span class="vh"> for ' + esc(ev.event) + '</span></a>');
        links.push('<button type="button" class="linklike" data-ev="">All events</button>');
        var where = [ev.city, ev.league].filter(Boolean).map(esc).join(' · ');
        head.innerHTML = '<div class="g-ev"><div><p class="g-ev__k">' + esc(whenLong(ev)) + ' · ' + esc(ev.kind) + '</p><h2 class="h2" tabindex="-1" data-g-evt>' + esc(ev.event) + '</h2>' +
          '<p class="g-ev__m">' + [where, esc(counts(ev))].filter(Boolean).join(' · ') + '</p></div><div class="g-ev__a">' + links.join('') + '</div></div>';
        var evItems = itemsOf([ev]);
        paint(wall, evItems, 0, evItems.length);
        var others = itemsOf(pool.filter(function (a) { return a !== ev; }));
        if (others.length) {
          rest.innerHTML = '<div class="g-sub"><h2 class="h3">More from ' + esc(yl) + '</h2><button type="button" class="linklike" data-ev="">See all events</button></div><div class="g-wallw"><ul class="g-wall" data-g-wall2></ul></div>';
          var s2 = paint(q('[data-g-wall2]'), others, 1, st.shown);
          moreBtn(s2, others.length);
        } else q('[data-g-more]').innerHTML = '';
        return;
      }
      var items = itemsOf(pool);
      if (!ALBUMS.length) {
        wall.innerHTML = ''; wall.className = 'g-wall';
        var sched = root.getAttribute('data-schedule');
        head.innerHTML = '<div class="g-empty"><p class="h3">The first photos land after the next pull</p><p>The crew posts photos and video from every pull, exhibition and test day of the ' + esc(String(SEASON)) + ' season right here.</p>' +
          (sched ? '<a class="link" href="' + esc(sched) + '">See where we pull next</a>' : '') + '</div>';
        q('[data-g-more]').innerHTML = '';
        return;
      }
      if (!items.length) {
        wall.innerHTML = ''; wall.className = 'g-wall';
        head.innerHTML = '<div class="g-empty"><p class="h3">Nothing here yet</p><p>No ' + esc(st.type === 'all' ? 'photos or videos' : st.type) + ' for ' + esc(yl) + '. Try another season or event type, or show everything.</p>' +
          (ALBUMS.length ? '<button type="button" class="btn btn--ghost btn--sm" data-year="all" data-type="all" data-kind="all">Show everything</button>' : '') + '</div>';
        q('[data-g-more]').innerHTML = '';
        return;
      }
      var s = paint(wall, items, 0, st.shown);
      moreBtn(s, items.length);
      if (focusFrom != null) {
        var f = wall.querySelector('li[data-i="' + focusFrom + '"] .g-t');
        if (f) f.focus();
      }
    }
    function writeURL() {
      var p = new URLSearchParams(location.search);
      ['event', 'year', 'kind', 'type'].forEach(function (k) { p.delete(k); });
      if (st.event) p.set('event', st.event);
      else {
        if (st.year !== SEASON) p.set('year', st.year);
        if (st.kind !== 'all') p.set('kind', st.kind.toLowerCase());
        if (st.type !== 'all') p.set('type', st.type);
      }
      var qs = p.toString();
      try { history.replaceState(null, '', location.pathname + (qs ? '?' + qs : '') + location.hash); } catch (e) { /* ignore */ }
    }
    function render() { st.shown = PAGE; renderTop(); renderFilters(); renderWalls(); writeURL(); }
    function barTop() {
      var bar = q('[data-g-barwrap]');
      if (bar && bar.getBoundingClientRect().top < 0) { bar.scrollIntoView({ block: 'start' }); window.scrollBy(0, -70); }
    }
    function goEvent(id) {
      st.event = id || '';
      var a = st.event && byEvent(st.event);
      if (a) { st.type = 'all'; st.year = a.year; if (!inKind(a)) st.kind = 'all'; }
      render();
      if (drawer.hidden) barTop();
    }

    /* drawer */
    var drawer = q('[data-g-drawer]'), scrim = q('[data-g-scrim]'), lastBtn = null;
    function openDrawer(key, btn) {
      lastBtn = btn;
      find.value = '';
      renderFilters();
      drawer.hidden = false; scrim.hidden = false;
      document.documentElement.style.overflow = 'hidden';
      btn.setAttribute('aria-expanded', 'true');
      q('[data-g-dbody]').scrollTop = 0;
      if (key === 'event') { q('[data-g-secev]').scrollIntoView({ block: 'start' }); find.focus(); }
      else {
        var c = q('[data-g-year] input:checked') || q('[data-g-year] input');
        if (c) c.focus();
      }
    }
    function closeDrawer() {
      if (drawer.hidden) return;
      drawer.hidden = true; scrim.hidden = true;
      document.documentElement.style.overflow = '';
      q('[data-g-filter]').setAttribute('aria-expanded', 'false');
      q('[data-g-events]').setAttribute('aria-expanded', 'false');
      barTop();
      if (lastBtn) lastBtn.focus();
    }
    function onDrawerKey(e) {
      if (e.key === 'Escape') {
        if (e.target === find && find.value) { e.preventDefault(); find.value = ''; renderEvents(); return; }
        e.preventDefault(); closeDrawer(); return;
      }
      if (e.key !== 'Tab') return;
      var f = Array.prototype.filter.call(drawer.querySelectorAll('button, input'), function (el) {
        if (el.offsetParent === null) return false;
        if (el.type === 'radio' && !el.checked && drawer.querySelector('input[name="' + el.name + '"]:checked')) return false;
        return true;
      });
      if (!f.length) return;
      if (e.shiftKey && document.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
      else if (!e.shiftKey && document.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
    }
    function onFindKey(e) {
      var r = q('[data-g-evl]').querySelectorAll('input');
      if (e.key === 'ArrowDown' && r.length) { e.preventDefault(); (q('[data-g-evl] input:checked') || r[0]).focus(); }
      else if (e.key === 'Enter') {
        e.preventDefault();
        var first = Array.prototype.filter.call(r, function (x) { return x.value; })[0];
        if (first && find.value.trim()) {
          goEvent(first.value);
          find.value = '';
          renderEvents();
          var c = q('[data-g-evl] input:checked');
          if (c) c.focus();
        }
      }
    }
    function onDrawerChange(e) {
      var t = e.target, name = t.getAttribute('data-name'), id = t.id;
      if (name === 'year') { st.year = t.value === 'all' ? 'all' : +t.value; st.event = ''; render(); }
      else if (name === 'kind') { st.kind = t.value; st.event = ''; render(); }
      else if (name === 'ev') goEvent(t.value);
      else return;
      var el = id && document.getElementById(id);
      if (el) el.focus();
    }

    /* clicks inside the section */
    function onClick(e) {
      var t = e.target;
      var open = t.closest('[data-open]');
      if (open && root.contains(open)) { openDrawer(open.getAttribute('data-open'), open); return; }
      if (t.closest('[data-g-close]') || t.closest('[data-g-view]') || t === scrim) { closeDrawer(); return; }
      if (t.closest('[data-g-clear]')) {
        st.year = SEASON; st.kind = 'all'; st.event = ''; find.value = '';
        render();
        var y0 = q('[data-g-year] input');
        if (y0) y0.focus();
        return;
      }
      if (t.closest('[data-g-load]')) {
        var from = st.shown;
        st.shown += PAGE;
        if (st.event) {
          renderWalls();
          var w2 = q('[data-g-wall2]'), f2 = w2 && w2.querySelector('li[data-i="' + from + '"] .g-t');
          if (f2) f2.focus();
        } else renderWalls(from);
        return;
      }
      if (t.closest('[data-g-top]')) {
        window.scrollTo(0, root.getBoundingClientRect().top + window.scrollY - 80);
        q('[data-g-filter]').focus({ preventScroll: true });
        return;
      }
      var pe = t.closest('[data-playev]');
      if (pe) {
        var evA = byEvent(pe.getAttribute('data-playev'));
        if (evA) { var lb = lightbox(); lb.open(lb.seqOf(evA), 0, pe, true); }
        return;
      }
      var tl = t.closest('.g-t[data-wall]');
      if (tl) {
        var list = WALLS[+tl.getAttribute('data-wall')] || [], it = list[+tl.getAttribute('data-i')];
        var photos = list.filter(function (x) { return x.kind === 'photo'; });
        lightbox().open(photos, photos.indexOf(it), tl, false);
        return;
      }
      var evb = t.closest('[data-ev]');
      if (evb) {
        goEvent(evb.getAttribute('data-ev'));
        if (!st.event) q('[data-g-events]').focus({ preventScroll: true });
        else { var h = q('[data-g-evt]'); if (h) h.focus({ preventScroll: true }); }
        return;
      }
      var b = t.closest('[data-year],[data-type],[data-kind]');
      if (!b || !t.closest('.g-bar, .g-empty, .g-chips')) return;
      st.event = '';
      if (b.hasAttribute('data-year')) { var y = b.getAttribute('data-year'); st.year = y === 'all' ? 'all' : +y; }
      if (b.hasAttribute('data-type')) st.type = b.getAttribute('data-type');
      if (b.hasAttribute('data-kind')) st.kind = b.getAttribute('data-kind');
      render();
      var fb = (b.hasAttribute('data-type') && q('.g-media [data-type="' + st.type + '"]')) || q('[data-g-chips] button') || q('[data-g-filter]');
      if (fb) fb.focus();
    }

    var rz = null, lastW = window.innerWidth;
    function onResize() {
      clearTimeout(rz);
      rz = setTimeout(function () { if (window.innerWidth !== lastW) { lastW = window.innerWidth; renderWalls(); } }, 150);
    }

    root.addEventListener('click', onClick);
    drawer.addEventListener('keydown', onDrawerKey);
    drawer.addEventListener('change', onDrawerChange);
    find.addEventListener('input', renderEvents);
    find.addEventListener('keydown', onFindKey);
    window.addEventListener('resize', onResize);
    render();

    this.destroy = function () {
      root.removeEventListener('click', onClick);
      window.removeEventListener('resize', onResize);
      clearTimeout(rz);
      if (!drawer.hidden) document.documentElement.style.overflow = '';
      if (LB) LB.close();
      self.root = null;
    };
  }

  /* ---------------------------------------------------------------- album page */
  function Album(root) {
    var a = null;
    try { a = JSON.parse(root.querySelector('[data-album-data]').textContent); } catch (e) { a = null; }
    if (!a) { this.destroy = function () {}; return; }
    a.photos = a.photos || [];
    function onClick(e) {
      var b = e.target.closest('[data-album-k], [data-album-all]');
      if (!b) return;
      var lb = lightbox();
      lb.open(lb.seqOf(a), b.hasAttribute('data-album-k') ? +b.getAttribute('data-album-k') : 0, b, true);
    }
    root.addEventListener('click', onClick);
    this.destroy = function () {
      root.removeEventListener('click', onClick);
      if (LB) LB.close();
    };
  }

  /* ---------------------------------------------------------------- init */
  var live = [];
  function initAll(scope) {
    (scope || document).querySelectorAll('[data-hm-gallery]').forEach(function (r) {
      if (r.dataset.ready) return;
      r.dataset.ready = '1';
      live.push({ root: r, app: new Gallery(r) });
    });
    (scope || document).querySelectorAll('[data-hm-album]').forEach(function (r) {
      if (r.dataset.ready) return;
      r.dataset.ready = '1';
      live.push({ root: r, app: new Album(r) });
    });
  }
  document.addEventListener('shopify:section:load', function (e) { initAll(e.target); });
  document.addEventListener('shopify:section:unload', function (e) {
    live = live.filter(function (x) {
      if (e.target.contains(x.root)) { x.app.destroy(); return false; }
      return true;
    });
  });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { initAll(); });
  else initAll();
})();
