/* Schedule: reads the Pull event JSON printed by sections/hm-schedule.liquid and builds
   List (Upcoming / Past results tabs) and Calendar views, the season select and an .ics file per pull.
   Upcoming vs past is decided here with today's date (never in Liquid, so the page cache can't freeze it).
   Editor safe: one instance per section, rebuilt on shopify:section:load, cleaned on unload. */
(function () {
  if (window.hmSchedule) return;

  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  var DAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  var DAYS_L = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function ext(href, label, extra) { return '<a href="' + esc(href) + '" target="_blank" rel="noopener">' + label + '<span class="sc-ext" aria-hidden="true">↗</span><span class="vh">' + esc(extra || '') + ' (opens in a new tab)</span></a>'; }
  function pad(n) { return String(n).padStart(2, '0'); }
  function key(y, m, d) { return y + '-' + pad(m + 1) + '-' + pad(d); }
  function isoOf(dt) { return key(dt.getFullYear(), dt.getMonth(), dt.getDate()); }
  function dObj(iso) { return new Date(iso + 'T12:00:00'); }
  function fmtDate(iso, long) { return dObj(iso).toLocaleDateString('en-US', long ? { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' } : { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' }); }
  function cap(s) { s = String(s || ''); return s.charAt(0).toUpperCase() + s.slice(1); }

  function Schedule(root) {
    var dataEl = root.querySelector('[data-sc-data]');
    if (!dataEl) return;
    var DATA;
    try { DATA = JSON.parse(dataEl.textContent); } catch (err) { return; }
    var SEASON = +DATA.season || new Date().getFullYear();
    var TODAY = new Date(); TODAY.setHours(12, 0, 0, 0);
    var TODAY_K = isoOf(TODAY);
    var EVENTS = (DATA.events || []).filter(function (e) { return e.status !== 'hidden'; });
    EVENTS.forEach(function (e, i) { e.i = i; });

    var $ = function (sel) { return root.querySelector(sel); };
    var bar = $('[data-sc-bar]'), tabs = [$('[data-tab="up"]'), $('[data-tab="past"]')];
    var panelUp = $('[data-panel="up"]'), panelPast = $('[data-panel="past"]');
    var viewList = $('[data-sc-view-list]'), viewCal = $('[data-sc-view-cal]');
    var yearSel = $('[data-sc-year]'), calTitle = $('[data-cal-title]'), calGrid = $('[data-cal-grid]'), calSide = $('[data-cal-side]');
    var prevBtn = $('[data-cal-move="-1"]'), nextBtn = $('[data-cal-move="1"]');
    bar.hidden = false;

    function yearOf(e) { return e.date ? +e.date.slice(0, 4) : (+e.season || SEASON); }
    function isExh(e) { return e.type === 'exhibition'; }
    function typeName(e) { return cap(e.type || 'competition'); }
    /* upcoming = dated today or later (or undated with status Upcoming), and not Done */
    function isUp(e) {
      if (e.status === 'done') return false;
      if (e.date) return e.date >= TODAY_K;
      return e.status === 'upcoming';
    }
    function isWin(e) { return e.status === 'done' && +e.place === 1; }
    function shortOf(e) { return e.short || (e.event || 'Pull').split(/\s+/)[0]; }
    function dateText(e) { return e.date ? fmtDate(e.date) : 'Date TBA'; }
    function linksOf(e) {
      var up = isUp(e), l = [];
      if (!up && e.status === 'done' && e.gallery) l.push('<a href="' + esc(e.gallery) + '">Photos &amp; video<span class="vh"> from ' + esc(e.event) + '</span></a>');
      if (e.video) l.push(ext(e.video, 'Video of the run', ' of ' + e.event));
      if (e.website) l.push(ext(e.website, up ? 'Tickets and info' : 'Event site', ' for ' + e.event));
      return l;
    }
    function resultHtml(e) {
      if (e.status === 'cancelled') return '<span class="badge badge--ink">Cancelled</span>';
      var p = [];
      if (e.distance !== '' && e.distance != null) p.push('<span class="dist num">' + esc(e.distance) + ' ft</span>');
      if (e.result) p.push('<span>' + esc(e.result) + '</span>');
      if (e.full) p.push('<span class="badge">Full pull</span>');
      if (!p.length) return e.status === 'done' ? '<span class="badge badge--line">Result pending</span>' : '<span class="sc-dash">-</span>';
      return '<span class="sc-res">' + p.join('') + '</span>';
    }
    function eventCell(e) { return '<b>' + esc(e.event || 'Pull') + '</b><span class="sc-s">' + esc(e.city) + (e.time ? ' · ' + esc(e.time) : '') + '</span>'; }
    function icsBtn(e) { return '<button class="sc-linkbtn sc-ics" type="button" data-ics="' + e.i + '">Add to calendar<span class="vh">: ' + esc(e.event) + '</span></button>'; }

    var HEAD_UP = '<thead><tr><th scope="col">Date</th><th scope="col">Event</th><th scope="col">Type</th><th scope="col">League</th><th scope="col">Links</th><th scope="col">Calendar</th></tr></thead>';
    var HEAD_PAST = '<thead><tr><th scope="col">Date</th><th scope="col">Event</th><th scope="col">Type</th><th scope="col">League</th><th scope="col">Result</th><th scope="col">Video, photos</th></tr></thead>';
    function rowUp(e) {
      var l = linksOf(e);
      var calCell = e.status === 'cancelled' ? '<span class="badge badge--ink">Cancelled</span>' : e.date ? icsBtn(e) : '<span class="sc-dash">Date TBA</span>';
      return '<tr><td data-label="Date"><span class="num">' + esc(dateText(e)) + '</span></td>' +
        '<td data-label="Event" class="wide">' + eventCell(e) + '</td>' +
        '<td data-label="Type"><span class="sc-tt">' + esc(typeName(e)) + '</span></td>' +
        '<td data-label="League">' + esc(e.league) + '</td>' +
        '<td data-label="Links">' + (l.length ? '<span class="sc-links">' + l.join('') + '</span>' : '<span class="sc-dash">TBA</span>') + '</td>' +
        '<td data-label="Calendar">' + calCell + '</td></tr>';
    }
    function rowPast(e) {
      var l = linksOf(e);
      return '<tr><td data-label="Date"><span class="num">' + esc(dateText(e)) + '</span>' + (e.date ? '' : '<span class="sc-s">Season ' + yearOf(e) + '</span>') + '</td>' +
        '<td data-label="Event" class="wide">' + eventCell(e) + '</td>' +
        '<td data-label="Type"><span class="sc-tt">' + esc(typeName(e)) + '</span></td>' +
        '<td data-label="League">' + esc(e.league) + '</td>' +
        '<td data-label="Result">' + resultHtml(e) + '</td>' +
        '<td data-label="Video, photos">' + (l.length ? '<span class="sc-links">' + l.join('') + '</span>' : '<span class="sc-dash">' + (e.status === 'cancelled' ? '-' : 'Coming soon') + '</span>') + '</td></tr>';
    }

    var S = { year: SEASON, view: 'list', tab: 'up', month: TODAY.getMonth(), sel: null };
    function live() { return EVENTS.filter(function (e) { return yearOf(e) === S.year; }); }
    function dated() { return live().filter(function (e) { return e.date; }); }
    function inMonth(m) { return dated().filter(function (e) { return +e.date.slice(5, 7) === m + 1; }); }
    function byDateAsc(a, b) { var x = a.date || '9999', y = b.date || '9999'; return x < y ? -1 : x > y ? 1 : 0; }
    function byDateDesc(a, b) { if (!a.date && !b.date) return 0; if (!a.date) return 1; if (!b.date) return -1; return a.date < b.date ? 1 : a.date > b.date ? -1 : 0; }

    function bestMonth() {
      var c = {}, ref = S.year === TODAY.getFullYear() ? TODAY.getMonth() : 11, best = null;
      dated().forEach(function (e) { var m = +e.date.slice(5, 7) - 1; c[m] = (c[m] || 0) + 1; });
      Object.keys(c).forEach(function (k) {
        var m = +k;
        if (best === null || c[m] > c[best] || (c[m] === c[best] && Math.abs(m - ref) < Math.abs(best - ref))) best = m;
      });
      return best === null ? (S.year === TODAY.getFullYear() ? TODAY.getMonth() : 0) : best;
    }
    function bestDay(m) {
      var L = inMonth(m);
      var up = L.filter(isUp).sort(byDateAsc);
      if (up.length) return up[0].date;
      L.sort(byDateDesc); return L.length ? L[0].date : null;
    }
    function openCal() {
      if (!inMonth(S.month).length) S.month = bestMonth();
      if (!S.sel) { var d = bestDay(S.month); if (d) S.sel = { day: d }; }
    }

    function fillYears() {
      var ys = [SEASON];
      EVENTS.forEach(function (e) { var y = yearOf(e); if (ys.indexOf(y) < 0) ys.push(y); });
      ys.sort(function (a, b) { return b - a; });
      yearSel.innerHTML = ys.map(function (y) { return '<option value="' + y + '"' + (y === S.year ? ' selected' : '') + '>' + y + '</option>'; }).join('');
      yearSel.closest('.sc-year').hidden = ys.length < 2;
    }

    function stat(label, n) { return '<span>' + label + ' <b>' + n + '</b></span>'; }
    function renderList() {
      var L = live();
      var up = L.filter(isUp).sort(byDateAsc);
      var past = L.filter(function (e) { return !isUp(e); }).sort(byDateDesc);
      tabs[0].querySelector('[data-n-up]').textContent = '(' + up.length + ')';
      tabs[1].querySelector('[data-n-past]').textContent = '(' + past.length + ')';
      var cur = S.year === SEASON;
      var fb = DATA.facebook ? ' and on ' + ext(DATA.facebook, 'Facebook') : '';
      var list = DATA.evilList ? ' <a href="' + esc(DATA.evilList) + '">Join The Evil List</a> to hear before every pull.' : '';
      panelUp.innerHTML = up.length
        ? '<table class="sc-table">' + HEAD_UP + '<tbody>' + up.map(rowUp).join('') + '</tbody></table>'
        : '<table class="sc-table"><tbody><tr class="sc-empty"><td colspan="6"><b>' + (cur ? 'Dates coming soon' : 'No upcoming pulls in ' + S.year) + '</b>' +
          (cur ? 'New ' + SEASON + ' dates go here' + fb + ' first.' + list : '') +
          (past.length ? '<span class="sc-s" style="margin-top:6px">' + past.length + ' past pull' + (past.length > 1 ? 's' : '') + ' in ' + S.year + '. <button type="button" class="sc-linkbtn" data-go-past>See past results</button></span>' : '') + '</td></tr></tbody></table>';
      var done = past.filter(function (e) { return e.status === 'done'; });
      var nC = done.filter(function (e) { return !isExh(e); }).length;
      var nE = done.filter(isExh).length;
      var nW = done.filter(isWin).length;
      /* Season stats (metaobject) win when they are higher: they count pulls that are not listed */
      var st = (DATA.stats || {})[S.year];
      if (st) { nC = Math.max(nC, st.c || 0); nE = Math.max(nE, st.e || 0); nW = Math.max(nW, st.w || 0); }
      panelPast.innerHTML = past.length
        ? '<p class="sc-sum"><span>' + S.year + (cur ? ' so far:' : ':') + '</span>' + stat('Competitions', nC) + stat('Exhibitions', nE) + stat('Wins', nW || 'Coming soon') + '</p>' +
          '<div class="sc-table-wrap"><table class="sc-table">' + HEAD_PAST + '<tbody>' + past.map(rowPast).join('') + '</tbody></table></div>'
        : '<div class="sc-table-wrap"><table class="sc-table"><tbody><tr class="sc-empty"><td colspan="6">No past pulls in ' + S.year + '.</td></tr></tbody></table></div>';
    }

    function evLabel(e) { var up = isUp(e); return esc(e.event) + ', ' + esc(typeName(e)) + (e.status === 'cancelled' ? ', cancelled' : up ? ', upcoming' : ''); }
    function chip(e) {
      var up = isUp(e), x = e.status === 'cancelled';
      return '<span class="sc-ev ' + (isExh(e) ? 'sc-ev--e' : 'sc-ev--c') + (up ? ' sc-ev--up' : '') + (x ? ' sc-ev--x' : '') + '" aria-hidden="true">' +
        esc(shortOf(e)) + (x ? '<small>Cancelled</small>' : up ? '<small>Upcoming</small>' : '<small>' + esc(typeName(e)) + '</small>') + '</span>';
    }
    function renderCal() {
      var y = S.year, m = S.month;
      calTitle.textContent = MONTHS[m] + ' ' + y;
      prevBtn.disabled = m === 0; nextBtn.disabled = m === 11;
      prevBtn.querySelector('.vh').textContent = m === 0 ? 'Previous month' : 'Previous month, ' + MONTHS[m - 1];
      nextBtn.querySelector('.vh').textContent = m === 11 ? 'Next month' : 'Next month, ' + MONTHS[m + 1];
      var map = {};
      dated().forEach(function (e) { (map[e.date] = map[e.date] || []).push(e); });
      var first = new Date(y, m, 1).getDay(), days = new Date(y, m + 1, 0).getDate();
      var h = '<table class="sc-cal" aria-labelledby="' + calTitle.id + '"><thead><tr>' + DAYS.map(function (d, i) {
        return '<th scope="col"><abbr title="' + DAYS_L[i] + '" style="text-decoration:none">' + d + '</abbr></th>'; }).join('') + '</tr></thead><tbody><tr>';
      var cells = 0;
      for (var i = 0; i < first; i++) { h += '<td class="out"></td>'; cells++; }
      for (var d = 1; d <= days; d++) {
        var k = key(y, m, d), list = map[k], cls = [], on = S.sel && S.sel.day === k;
        if (k === TODAY_K) cls.push('today');
        if (list) cls.push('has');
        if (on) cls.push('sel');
        h += '<td' + (cls.length ? ' class="' + cls.join(' ') + '"' : '') + '>';
        if (list) {
          var lab = fmtDate(k, true) + ': ' + list.length + ' pull' + (list.length > 1 ? 's' : '') + ', ' + list.map(evLabel).join('; ') + (k === TODAY_K ? ' (today)' : '');
          h += '<button type="button" class="day" data-day="' + k + '" aria-label="' + lab + '" aria-pressed="' + (on ? 'true' : 'false') + '"><span class="d" aria-hidden="true">' + d + '</span>' + list.map(chip).join('') + '</button>';
        } else {
          h += '<span class="d"' + (k === TODAY_K ? ' aria-label="' + d + ', today"' : '') + '>' + d + '</span>';
        }
        h += '</td>'; cells++;
        if (cells % 7 === 0 && d < days) h += '</tr><tr>';
      }
      while (cells % 7) { h += '<td class="out"></td>'; cells++; }
      calGrid.innerHTML = h + '</tr></tbody></table>';
      renderSide(map);
    }
    function detail(e) {
      var l = linksOf(e), up = isUp(e);
      return '<article class="sc-pd"><div class="sc-pd__top"><span class="badge' + (isExh(e) ? '' : ' badge--ink') + '">' + esc(typeName(e)) + '</span>' + (up && e.status !== 'cancelled' ? '<span class="badge badge--line">Upcoming</span>' : '') + '</div>' +
        '<h4 class="h3">' + esc(e.event) + '</h4>' +
        '<dl><dt>Date</dt><dd class="num">' + esc(e.date ? fmtDate(e.date, true) : dateText(e)) + (e.time ? ' · ' + esc(e.time) : '') + '</dd>' +
        '<dt>Place</dt><dd>' + esc(e.city || '-') + '</dd><dt>League</dt><dd>' + esc(e.league || '-') + '</dd>' +
        (up && e.status !== 'cancelled' ? '' : '<dt>Result</dt><dd>' + resultHtml(e) + '</dd>') +
        (l.length ? '<dt>Links</dt><dd><span class="sc-links">' + l.join('') + '</span></dd>' : '') + '</dl>' +
        (up && e.date && e.status !== 'cancelled' ? '<div>' + icsBtn(e) + '</div>' : '') + '</article>';
    }
    function sideItem(e, attr) {
      var dt = e.date ? dObj(e.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) : 'TBA';
      return '<li><button type="button" class="sc-side-item" ' + attr + '><span class="sc-side-dt num">' + esc(dt) + '</span><span><span class="sc-side-n">' + esc(e.event) + '</span><span class="sc-s">' + esc(typeName(e)) + (isUp(e) ? ' · Upcoming' : '') + (e.city ? ' · ' + esc(e.city) : '') + '</span></span></button></li>';
    }
    function renderSide(map) {
      var L = live(), y = S.year, m = S.month, h = '';
      if (S.sel) {
        var list = S.sel.day ? map[S.sel.day] || [] : [EVENTS[S.sel.i]];
        h += '<p class="sc-side-h"><span class="label">' + (S.sel.day ? esc(fmtDate(S.sel.day, true)) : 'Date TBA') + '</span><button type="button" class="sc-linkbtn small" data-back>All of ' + MONTHS[m] + '</button></p>' + list.map(detail).join('');
      } else {
        var ms = inMonth(m).sort(byDateAsc);
        h += '<p class="sc-side-h"><span class="label">' + MONTHS[m] + ' ' + y + '</span><span class="small muted">' + ms.length + ' pull' + (ms.length === 1 ? '' : 's') + '</span></p>';
        if (ms.length) h += '<ul class="sc-side-list">' + ms.map(function (e) { return sideItem(e, 'data-day="' + e.date + '"'); }).join('') + '</ul>';
        else {
          h += '<p class="sc-side-empty">No pulls marked in ' + MONTHS[m] + '.</p>';
          var mm = []; dated().forEach(function (e) { var x = +e.date.slice(5, 7) - 1; if (mm.indexOf(x) < 0) mm.push(x); });
          mm.sort(function (a, b) { return a - b; });
          if (mm.length) h += '<div><p class="sc-side-sub">Months with pulls</p><div class="sc-side-months">' + mm.map(function (x) { return '<button type="button" class="btn btn--ghost btn--sm" data-month="' + x + '">' + MONTHS[x].slice(0, 3) + '<span class="vh">' + MONTHS[x].slice(3) + '</span></button>'; }).join('') + '</div></div>';
        }
      }
      var pend = L.filter(function (e) { return !e.date; });
      if (pend.length && !(S.sel && S.sel.i != null)) h += '<div><p class="sc-side-sub">' + y + ' · date TBA (' + pend.length + ')</p><ul class="sc-side-list">' + pend.map(function (e) { return sideItem(e, 'data-ev="' + e.i + '"'); }).join('') + '</ul></div>';
      calSide.innerHTML = h;
    }

    function pickTab() { S.tab = live().some(isUp) ? 'up' : 'past'; }
    function selectTab(t, focus) {
      tabs.forEach(function (x) {
        var on = x === t;
        x.setAttribute('aria-selected', on ? 'true' : 'false');
        x.tabIndex = on ? 0 : -1;
      });
      panelUp.hidden = t !== tabs[0]; panelPast.hidden = t !== tabs[1];
      S.tab = t === tabs[0] ? 'up' : 'past';
      if (focus) t.focus();
    }
    function render() {
      if (S.view === 'cal') openCal();
      renderList(); selectTab(S.tab === 'up' ? tabs[0] : tabs[1]);
      renderCal();
      viewList.hidden = S.view !== 'list'; viewCal.hidden = S.view !== 'cal';
      $('[data-sc-tabs]').hidden = S.view !== 'list';
      root.querySelectorAll('[data-view]').forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-view') === S.view ? 'true' : 'false'); });
    }
    function moveMonth(dir) { var n = S.month + dir; if (n < 0 || n > 11) return; S.month = n; S.sel = null; renderCal(); }

    /* .ics: all-day event, built in the browser */
    function icsTxt(s) { return String(s || '').replace(/\\/g, '\\\\').replace(/\n/g, '\\n').replace(/([,;])/g, '\\$1'); }
    function ics(e) {
      var d = e.date.replace(/-/g, '');
      var next = dObj(e.date); next.setDate(next.getDate() + 1);
      var d2 = isoOf(next).replace(/-/g, '');
      var desc = icsTxt('“The Evil One” · Pro Stock · ' + typeName(e) + (e.league ? ' · ' + e.league : '') + (e.time ? ' · ' + e.time : '')) + (e.website ? '\\n' + icsTxt('Info: ' + e.website) : '');
      return ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Heavy Metal Pro Stock The Evil One//Schedule//EN', 'CALSCALE:GREGORIAN', 'BEGIN:VEVENT',
        'UID:' + d + '-' + (e.id || 'pull') + '@heavymetalprostock',
        'DTSTAMP:' + new Date().toISOString().replace(/[-:]/g, '').slice(0, 15) + 'Z',
        'DTSTART;VALUE=DATE:' + d, 'DTEND;VALUE=DATE:' + d2,
        'SUMMARY:' + icsTxt((e.event || 'Tractor pull') + ' · “The Evil One”'), 'LOCATION:' + icsTxt(e.city), 'DESCRIPTION:' + desc,
        'END:VEVENT', 'END:VCALENDAR'].join('\r\n');
    }
    function download(e) {
      var a = document.createElement('a');
      a.href = URL.createObjectURL(new Blob([ics(e)], { type: 'text/calendar;charset=utf-8' }));
      a.download = (e.event || 'pull').replace(/\W+/g, '-').toLowerCase() + '.ics';
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 4000);
    }

    function onClick(ev) {
      var t = ev.target;
      var ic = t.closest('[data-ics]'); if (ic) { var e = EVENTS[+ic.getAttribute('data-ics')]; if (e && e.date) download(e); return; }
      var tb = t.closest('[data-tab]'); if (tb) { selectTab(tb); return; }
      var vw = t.closest('[data-view]'); if (vw) { S.view = vw.getAttribute('data-view'); render(); return; }
      var mv = t.closest('[data-cal-move]'); if (mv) { moveMonth(+mv.getAttribute('data-cal-move')); return; }
      if (t.closest('[data-go-past]')) { selectTab(tabs[1], true); return; }
      var dy = t.closest('[data-day]');
      if (dy) { var k = dy.getAttribute('data-day'); S.month = +k.slice(5, 7) - 1; S.sel = { day: k }; renderCal(); calSide.focus(); return; }
      var ei = t.closest('[data-ev]'); if (ei) { S.sel = { i: +ei.getAttribute('data-ev') }; renderCal(); calSide.focus(); return; }
      var mo = t.closest('[data-month]'); if (mo) { S.month = +mo.getAttribute('data-month'); S.sel = null; renderCal(); calSide.focus(); return; }
      if (t.closest('[data-back]')) {
        var back = S.sel && S.sel.day; S.sel = null; renderCal();
        var b = back && calGrid.querySelector('[data-day="' + back + '"]'); (b || calSide).focus();
      }
    }
    function onKey(ev) {
      var t = ev.target;
      if (t.matches && t.matches('[data-tab]')) {
        var i = tabs.indexOf(t);
        var j = ev.key === 'ArrowRight' ? i + 1 : ev.key === 'ArrowLeft' ? i - 1 : ev.key === 'Home' ? 0 : ev.key === 'End' ? tabs.length - 1 : null;
        if (j === null) return; ev.preventDefault(); selectTab(tabs[(j + tabs.length) % tabs.length], true); return;
      }
      if ((ev.key === 'PageUp' || ev.key === 'PageDown') && viewCal.contains(t)) {
        ev.preventDefault(); moveMonth(ev.key === 'PageUp' ? -1 : 1);
        var b = ev.key === 'PageUp' ? prevBtn : nextBtn; (b.disabled ? (b === prevBtn ? nextBtn : prevBtn) : b).focus();
      }
    }
    function onYear() { S.year = +yearSel.value; S.month = bestMonth(); S.sel = null; pickTab(); render(); }

    root.addEventListener('click', onClick);
    root.addEventListener('keydown', onKey);
    yearSel.addEventListener('change', onYear);
    fillYears(); S.month = bestMonth(); pickTab(); render();

    this.destroy = function () {
      root.removeEventListener('click', onClick);
      root.removeEventListener('keydown', onKey);
      yearSel.removeEventListener('change', onYear);
    };
  }

  function initAll(scope) {
    (scope || document).querySelectorAll('[data-hm-schedule]').forEach(function (r) {
      if (!r.hmSchedule) r.hmSchedule = new Schedule(r);
    });
  }
  document.addEventListener('shopify:section:load', function (e) { initAll(e.target); });
  document.addEventListener('shopify:section:unload', function (e) {
    e.target.querySelectorAll('[data-hm-schedule]').forEach(function (r) { if (r.hmSchedule && r.hmSchedule.destroy) r.hmSchedule.destroy(); r.hmSchedule = null; });
  });
  window.hmSchedule = { init: initAll };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { initAll(); });
  else initAll();
})();
