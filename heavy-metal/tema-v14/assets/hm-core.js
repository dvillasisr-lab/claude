/* HM v14 core: shared helpers for every page.
   - window.HM.open(el, opts) / HM.close() / HM.current(): one dialog at a time (scrim, scroll lock,
     focus trap, Escape, focus return). Used by the phone menu, search and the cart drawer.
   - Announcement rotation with pause, header menus (mega + compact dropdowns), phone side drawer,
     predictive search (/search/suggest.json), sponsor strip controls, footer accordions and sign up,
     Cookie Preferences, horizontal strip edge fades.
   - Cart contract: clicking [data-hm-cart-open] dispatches "hm:cart:open" (cancelable, detail { trigger }) on
     document. hm-cart.js handles it and calls preventDefault(); if nobody does, HM opens [data-hm-cart] as a
     dialog. Anyone may dispatch "hm:cart:open" / "hm:cart:close". Dispatch "hm:cart:updated" with detail
     { count } (preferred, excludes the tip), { item_count } or { cart } to refresh [data-hm-cart-count].
   - Re-inits on shopify:section:load and cleans timers/listeners on shopify:section:unload. */
(function () {
  'use strict';
  var HM = (window.HM = window.HM || {});
  var doc = document;
  var root = doc.documentElement;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');

  /* ---------- focus helpers ---------- */
  var FOCUSABLE =
    'a[href],area[href],button:not([disabled]),input:not([disabled]):not([type="hidden"]),select:not([disabled]),textarea:not([disabled]),summary,iframe,[tabindex]:not([tabindex="-1"]),[contenteditable="true"]';
  HM.focusables = function (container) {
    return Array.prototype.filter.call(container.querySelectorAll(FOCUSABLE), function (el) {
      if (el.closest('[hidden],[inert]')) return false;
      if (!el.getClientRects().length) return false;
      var closedDetails = el.closest('details:not([open])');
      if (closedDetails && el.tagName !== 'SUMMARY' && !el.closest('summary')) return false;
      return true;
    });
  };
  HM.trapFocus = function (container, e) {
    var f = HM.focusables(container);
    if (!f.length) {
      e.preventDefault();
      return;
    }
    var first = f[0];
    var last = f[f.length - 1];
    var active = doc.activeElement;
    var inside = container.contains(active);
    if (e.shiftKey && (active === first || !inside)) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && (active === last || !inside)) {
      e.preventDefault();
      first.focus();
    }
  };

  /* ---------- dialogs: one at a time ----------
     HM.open(el, { trigger, returnFocus, focus, scrim, onClose })
       scrim: omitted = the header scrim [data-hm-scrim]; an element = that scrim; false = none.
       onClose: called once when this dialog closes (by HM.close, Escape, scrim, or another dialog opening).
     Opening a dialog closes the one already open (menu, search, cart, quick add, notify, filters).
     window.HMOverlay is a thin alias kept for the commerce scripts. */
  var current = null; /* { el, returnFocus, trigger, scrim, onClose } */
  var lastReturn = null; /* return target of a dialog that was replaced, reused by the next one */
  function scrimEl() {
    return doc.querySelector('[data-hm-scrim]');
  }
  function usableReturn(x, el) {
    return !!(x && x.focus && x !== doc.body && doc.contains(x) && !el.contains(x) && !x.closest('[hidden],[inert]'));
  }
  HM.current = function () {
    return current ? current.el : null;
  };
  HM.isOpen = function (el) {
    return !!(current && el && current.el === el);
  };
  HM.open = function (el, opts) {
    if (!el) return;
    opts = opts || {};
    if (current && current.el === el) {
      if (opts.focus !== false) focusInto(el, opts.focus);
      return;
    }
    var active = doc.activeElement;
    var prevReturn = current ? current.returnFocus : null;
    if (current) HM.close({ restore: false, silent: true });
    closeMenus();
    var returnFocus = null;
    [opts.returnFocus, prevReturn, lastReturn, active].some(function (x) {
      if (usableReturn(x, el)) {
        returnFocus = x;
        return true;
      }
      return false;
    });
    el.hidden = false;
    var scrim = opts.scrim === false ? null : opts.scrim && opts.scrim.nodeType === 1 ? opts.scrim : scrimEl();
    if (scrim) scrim.hidden = false;
    root.classList.add('hm-locked');
    current = { el: el, returnFocus: returnFocus, trigger: opts.trigger || null, scrim: scrim, onClose: opts.onClose || null };
    lastReturn = null;
    if (current.trigger) current.trigger.setAttribute('aria-expanded', 'true');
    if (opts.focus !== false) focusInto(el, opts.focus);
    el.dispatchEvent(new CustomEvent('hm:dialog:open', { bubbles: true }));
  };
  function focusInto(el, target) {
    var t = target && target.focus ? target : el.querySelector('[autofocus],[data-hm-autofocus]') || HM.focusables(el)[0] || el;
    if (t) {
      try {
        t.focus({ preventScroll: true });
      } catch (err) {
        t.focus();
      }
    }
  }
  /* HM.close(opts) closes the open dialog. opts.el: only if that element is the open one. opts.restore: false keeps focus where it is. */
  HM.close = function (opts) {
    opts = opts || {};
    if (!current) return;
    if (opts.el && current.el !== opts.el) return;
    var c = current;
    current = null;
    c.el.hidden = true;
    if (c.scrim) c.scrim.hidden = true;
    root.classList.remove('hm-locked');
    if (c.trigger) c.trigger.setAttribute('aria-expanded', 'false');
    if (c.onClose) {
      try {
        c.onClose();
      } catch (err) {}
    }
    c.el.dispatchEvent(new CustomEvent('hm:dialog:close', { bubbles: true }));
    if (opts.restore !== false && c.returnFocus && c.returnFocus.focus && doc.contains(c.returnFocus)) {
      c.returnFocus.focus({ preventScroll: true });
    } else if (opts.restore === false) {
      lastReturn = c.returnFocus;
    }
  };
  /* alias for hm-cart.js, hm-quick-add.js, hm-collection.js (same API they were built against) */
  window.HMOverlay = {
    open: function (el, opts) {
      opts = opts || {};
      HM.open(el, { scrim: opts.scrim || false, focus: opts.focus, returnFocus: opts.returnFocus, trigger: opts.trigger, onClose: opts.onClose });
    },
    close: function (el, keepFocus) {
      HM.close({ el: el, restore: !keepFocus });
    },
    isOpen: HM.isOpen,
    top: function () {
      return current ? { el: current.el } : undefined;
    }
  };

  /* ---------- header menus (mega + dropdowns): only one open ---------- */
  var menus = []; /* { trigger, panel, wrap, open(), close(refocus) } */
  var openMenu = null;
  function closeMenus(except) {
    menus.forEach(function (m) {
      if (m !== except) m.close(false);
    });
  }

  doc.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' || e.key === 'Esc') {
      if (openMenu) {
        var m = openMenu;
        m.close(m.wrap.contains(doc.activeElement));
        return;
      }
      if (current) {
        e.preventDefault();
        HM.close();
      }
      return;
    }
    if (e.key === 'Tab' && current) HM.trapFocus(current.el, e);
  });

  doc.addEventListener('click', function (e) {
    var t = e.target;
    if (t.closest('[data-hm-scrim]') || (current && current.scrim && current.scrim.contains(t))) {
      HM.close();
      return;
    }
    if (current && t.closest('[data-hm-close]') && current.el.contains(t)) {
      HM.close();
      return;
    }
    if (openMenu && !openMenu.wrap.contains(t)) openMenu.close(false);
  });

  function makeMenu(trigger, panel, wrap, hoverArea) {
    var closeTimer = null;
    var m = {
      trigger: trigger,
      panel: panel,
      wrap: wrap,
      open: function () {
        clearTimeout(closeTimer);
        if (openMenu === m) return;
        closeMenus(m);
        panel.hidden = false;
        trigger.setAttribute('aria-expanded', 'true');
        openMenu = m;
      },
      close: function (refocus) {
        clearTimeout(closeTimer);
        if (panel.hidden) return;
        panel.hidden = true;
        trigger.setAttribute('aria-expanded', 'false');
        if (openMenu === m) openMenu = null;
        if (refocus) {
          m.skipFocusOpen = true;
          trigger.focus();
          m.skipFocusOpen = false;
        }
      },
      later: function () {
        clearTimeout(closeTimer);
        closeTimer = setTimeout(function () {
          var a = doc.activeElement;
          if (!(a && wrap.contains(a) && a.matches(':focus-visible'))) m.close(false);
        }, 150);
      }
    };
    var offs = [];
    function on(el, ev, fn) {
      el.addEventListener(ev, fn);
      offs.push(function () {
        el.removeEventListener(ev, fn);
      });
    }
    (hoverArea || [wrap]).forEach(function (area) {
      on(area, 'pointerenter', function (e) {
        if (e.pointerType === 'mouse') m.open();
      });
      on(area, 'pointerleave', function (e) {
        if (e.pointerType === 'mouse') m.later();
      });
    });
    on(trigger, 'click', function (e) {
      /* first click or tap opens, the second one follows the link */
      if (panel.hidden) {
        e.preventDefault();
        m.open();
      }
    });
    on(trigger, 'focus', function () {
      if (!m.skipFocusOpen && trigger.matches(':focus-visible')) m.open();
    });
    on(trigger, 'keydown', function (e) {
      var items;
      if (e.key === ' ' || e.key === 'Spacebar') {
        e.preventDefault();
        if (panel.hidden) m.open();
        else m.close(false);
      } else if (e.key === 'Enter' && panel.hidden) {
        e.preventDefault();
        m.open();
      } else if (e.key === 'ArrowDown') {
        e.preventDefault();
        m.open();
        items = panel.querySelectorAll('a[href]');
        if (items[0]) items[0].focus();
      }
    });
    on(panel, 'keydown', function (e) {
      if (e.key !== 'ArrowDown' && e.key !== 'ArrowUp') return;
      var items = Array.prototype.slice.call(panel.querySelectorAll('a[href]'));
      var i = items.indexOf(doc.activeElement);
      if (i < 0) return;
      e.preventDefault();
      if (e.key === 'ArrowDown') items[Math.min(i + 1, items.length - 1)].focus();
      else if (i === 0) trigger.focus();
      else items[i - 1].focus();
    });
    on(wrap, 'focusout', function (e) {
      if (!e.relatedTarget || !wrap.contains(e.relatedTarget)) m.close(false);
    });
    m.destroy = function () {
      clearTimeout(closeTimer);
      offs.forEach(function (f) {
        f();
      });
      var i = menus.indexOf(m);
      if (i > -1) menus.splice(i, 1);
      if (openMenu === m) openMenu = null;
    };
    menus.push(m);
    return m;
  }

  /* ---------- header ---------- */
  function initHeader(hdr) {
    var cleanups = [];
    var sectionRoot = hdr.closest('.shopify-section') || doc;

    /* mega menu: hover region is the trigger plus the panel */
    var mt = hdr.querySelector('[data-hm-mega-trigger]');
    var mp = hdr.querySelector('[data-hm-mega]');
    if (mt && mp) {
      var megaWrap = {
        contains: function (n) {
          return !!n && (mt.contains(n) || mp.contains(n));
        },
        addEventListener: function (ev, fn) {
          mt.addEventListener(ev, fn);
          mp.addEventListener(ev, fn);
        },
        removeEventListener: function (ev, fn) {
          mt.removeEventListener(ev, fn);
          mp.removeEventListener(ev, fn);
        }
      };
      var mega = makeMenu(mt, mp, megaWrap, [mt, mp]);
      cleanups.push(mega.destroy);
    }

    /* compact dropdowns */
    hdr.querySelectorAll('[data-hm-dd]').forEach(function (dd) {
      var t = dd.querySelector('[data-hm-dd-trigger]');
      var p = dd.querySelector('[data-hm-dd-panel]');
      if (t && p) cleanups.push(makeMenu(t, p, dd).destroy);
    });

    /* phone side drawer */
    var openBtn = hdr.querySelector('[data-hm-menu-open]');
    var mnav = sectionRoot.querySelector('[data-hm-mnav]');
    if (openBtn && mnav) {
      var hoverTimer = null;
      var leaveTimer = null;
      var onClick = function () {
        HM.open(mnav, { trigger: openBtn, returnFocus: openBtn });
      };
      openBtn.addEventListener('click', onClick);
      cleanups.push(function () {
        openBtn.removeEventListener('click', onClick);
      });
      if (finePointer.matches) {
        /* mouse: opens after a short hover on the burger, with a click shield so the following click does not hit a link */
        var enter = function () {
          clearTimeout(leaveTimer);
          hoverTimer = setTimeout(function () {
            if (!mnav.hidden) return;
            HM.open(mnav, { trigger: openBtn, returnFocus: openBtn, focus: false });
            mnav.style.pointerEvents = 'none';
            setTimeout(function () {
              mnav.style.pointerEvents = '';
            }, 450);
          }, 160);
        };
        var leaveBtn = function () {
          clearTimeout(hoverTimer);
        };
        var navEnter = function () {
          clearTimeout(leaveTimer);
        };
        var navLeave = function () {
          leaveTimer = setTimeout(function () {
            if (!mnav.hidden && !mnav.contains(doc.activeElement) && HM.current() === mnav) HM.close({ restore: false });
          }, 300);
        };
        openBtn.addEventListener('mouseenter', enter);
        openBtn.addEventListener('mouseleave', leaveBtn);
        mnav.addEventListener('mouseenter', navEnter);
        mnav.addEventListener('mouseleave', navLeave);
        cleanups.push(function () {
          clearTimeout(hoverTimer);
          clearTimeout(leaveTimer);
          openBtn.removeEventListener('mouseenter', enter);
          openBtn.removeEventListener('mouseleave', leaveBtn);
          mnav.removeEventListener('mouseenter', navEnter);
          mnav.removeEventListener('mouseleave', navLeave);
        });
      }
    }

    /* predictive search */
    var sBtn = hdr.querySelector('[data-hm-search-open]');
    var sDlg = sectionRoot.querySelector('[data-hm-search]');
    if (sBtn && sDlg) cleanups.push(initSearch(sBtn, sDlg));

    return function () {
      cleanups.forEach(function (f) {
        f();
      });
      if (current && sectionRoot.contains(current.el)) HM.close({ restore: false });
    };
  }

  /* ---------- predictive search ---------- */
  var RECENT_KEY = 'hm-recent';
  function recents() {
    try {
      var r = JSON.parse(localStorage.getItem(RECENT_KEY) || '[]');
      return Array.isArray(r) ? r : [];
    } catch (e) {
      return [];
    }
  }
  function saveRecent(q) {
    q = (q || '').trim();
    if (!q) return;
    var r = recents().filter(function (x) {
      return x.toLowerCase() !== q.toLowerCase();
    });
    r.unshift(q);
    try {
      localStorage.setItem(RECENT_KEY, JSON.stringify(r.slice(0, 4)));
    } catch (e) {}
  }
  function esc(t) {
    return String(t == null ? '' : t).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function sizedImg(url, w) {
    if (!url) return '';
    try {
      var u = new URL(url, location.href);
      u.searchParams.set('width', w);
      return u.toString();
    } catch (e) {
      return url;
    }
  }

  function initSearch(btn, dlg) {
    var input = dlg.querySelector('[data-hm-search-input]');
    var form = dlg.querySelector('[data-hm-search-form]');
    var sugg = dlg.querySelector('[data-hm-sugg]');
    var suggH = dlg.querySelector('[data-hm-sugg-h]');
    var pages = dlg.querySelector('[data-hm-pages]');
    var res = dlg.querySelector('[data-hm-search-res]');
    var head = dlg.querySelector('[data-hm-search-h]');
    var all = dlg.querySelector('[data-hm-search-all]');
    var recentWrap = dlg.querySelector('[data-hm-recent-wrap]');
    var recentUl = dlg.querySelector('[data-hm-recent]');
    var suggestUrl = dlg.getAttribute('data-suggest-url') || '/search/suggest.json';
    var searchUrl = dlg.getAttribute('data-search-url') || '/search';
    var currency = dlg.getAttribute('data-currency') || 'USD';
    var locale = dlg.getAttribute('data-locale') || 'en';
    var defaults = {
      sugg: sugg ? sugg.innerHTML : '',
      suggH: suggH ? suggH.getAttribute('data-default') || suggH.textContent : '',
      pages: pages ? pages.innerHTML : '',
      res: res ? res.innerHTML : '',
      head: head ? head.textContent : ''
    };
    var timer = null;
    var ctrl = null;
    var money;
    try {
      money = new Intl.NumberFormat(locale, { style: 'currency', currency: currency });
    } catch (e) {
      money = { format: function (n) { return '$' + Number(n).toFixed(2); } };
    }
    function searchHref(q) {
      return searchUrl + '?q=' + encodeURIComponent(q) + '&options%5Bprefix%5D=last';
    }
    function li(text, href) {
      return '<li><a href="' + esc(href) + '">' + esc(text) + '</a></li>';
    }
    function renderRecent(q) {
      if (!recentWrap) return;
      var r = recents();
      recentWrap.hidden = !!q || !r.length;
      recentUl.innerHTML = r
        .map(function (w) {
          return li(w, searchHref(w));
        })
        .join('');
    }
    function reset() {
      if (ctrl) ctrl.abort();
      if (sugg) sugg.innerHTML = defaults.sugg;
      if (suggH) {
        suggH.textContent = defaults.suggH;
        suggH.hidden = !defaults.sugg.trim();
      }
      if (pages) pages.innerHTML = defaults.pages;
      if (res) res.innerHTML = defaults.res;
      if (head) head.textContent = defaults.head;
      if (all) all.hidden = true;
      renderRecent('');
    }
    function card(p) {
      var img = p.featured_image && p.featured_image.url ? p.featured_image.url : p.image;
      var price = p.price != null ? money.format(Number(p.price)) : '';
      var from = p.price_max && p.price_min && Number(p.price_max) !== Number(p.price_min) ? 'From ' : '';
      return (
        '<a class="sres" href="' + esc(p.url) + '"><span class="thumb">' +
        (img
          ? '<img src="' + esc(sizedImg(img, 360)) + '" srcset="' + esc(sizedImg(img, 180)) + ' 180w, ' + esc(sizedImg(img, 360)) + ' 360w, ' + esc(sizedImg(img, 540)) + ' 540w" sizes="(min-width: 761px) 22vw, 45vw" width="360" height="450" alt="" loading="lazy">'
          : '') +
        '</span><span class="sres__n">' + esc(p.title) + '</span>' +
        (price ? '<span class="sres__p num">' + from + esc(price) + '</span>' : '') +
        '</a>'
      );
    }
    function run(q) {
      if (ctrl) ctrl.abort();
      ctrl = 'AbortController' in window ? new AbortController() : null;
      var url =
        suggestUrl +
        '?q=' + encodeURIComponent(q) +
        '&resources[type]=product,page,article,query&resources[limit]=4&resources[limit_scope]=each&resources[options][unavailable_products]=last';
      fetch(url, { signal: ctrl ? ctrl.signal : undefined, headers: { Accept: 'application/json' } })
        .then(function (r) {
          if (!r.ok) throw new Error('search ' + r.status);
          return r.json();
        })
        .then(function (data) {
          if ((input.value || '').trim() !== q) return;
          var R = (data && data.resources && data.resources.results) || {};
          var products = R.products || [];
          var queries = R.queries || [];
          var pg = (R.pages || []).concat(R.articles || []);
          if (suggH) {
            suggH.textContent = 'Suggestions';
            suggH.hidden = !queries.length;
          }
          if (sugg)
            sugg.innerHTML = queries
              .slice(0, 5)
              .map(function (x) {
                return li(x.text, x.url || searchHref(x.text));
              })
              .join('');
          if (pages)
            pages.innerHTML = pg.length
              ? pg
                  .slice(0, 5)
                  .map(function (x) {
                    return li(x.title, x.url);
                  })
                  .join('')
              : defaults.pages;
          if (head)
            head.textContent = products.length
              ? products.length + (products.length === 1 ? ' product' : ' products') + ' for “' + q + '”'
              : 'No products for “' + q + '”';
          if (res)
            res.innerHTML = products.length
              ? products.map(card).join('')
              : '<p class="muted search__empty">Try "tee", "hoodie" or "kids". Or browse <a href="/collections/all">Shop all</a>.</p>';
          if (all) {
            all.hidden = !products.length;
            var a = all.querySelector('a');
            if (a) a.href = searchHref(q);
          }
        })
        .catch(function (err) {
          if (err && err.name === 'AbortError') return;
          if (head) head.textContent = 'Press Enter to see results for “' + q + '”';
        });
    }
    function onInput() {
      var q = (input.value || '').trim();
      clearTimeout(timer);
      renderRecent(q);
      if (!q) {
        reset();
        return;
      }
      timer = setTimeout(function () {
        run(q);
      }, 220);
    }
    function onOpen() {
      reset();
      HM.open(dlg, { trigger: btn, returnFocus: btn, focus: input });
      if (input.value) onInput();
    }
    function onSubmit(e) {
      var q = (input.value || '').trim();
      if (!q) {
        e.preventDefault();
        input.focus();
        return;
      }
      saveRecent(q);
    }
    function onLinkClick(e) {
      var a = e.target.closest('a[href]');
      if (!a) return;
      var q = (input.value || '').trim();
      if (q) saveRecent(q);
    }
    btn.addEventListener('click', onOpen);
    input.addEventListener('input', onInput);
    form.addEventListener('submit', onSubmit);
    dlg.addEventListener('click', onLinkClick);
    if (suggH) suggH.hidden = !defaults.sugg.trim();
    return function () {
      clearTimeout(timer);
      if (ctrl) ctrl.abort();
      btn.removeEventListener('click', onOpen);
      input.removeEventListener('input', onInput);
      form.removeEventListener('submit', onSubmit);
      dlg.removeEventListener('click', onLinkClick);
    };
  }

  /* ---------- cart: open/close events and count ---------- */
  function cartDrawer() {
    return doc.querySelector('[data-hm-cart],[data-hm-cart-drawer]');
  }
  doc.addEventListener('click', function (e) {
    var b = e.target.closest('[data-hm-cart-open]');
    if (!b || !cartDrawer()) return; /* no drawer: the link goes to /cart */
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.button > 0) return;
    e.preventDefault();
    doc.dispatchEvent(new CustomEvent('hm:cart:open', { cancelable: true, detail: { trigger: b } }));
  });
  doc.addEventListener('hm:cart:open', function (e) {
    var ev = e;
    var run = function () {
      if (ev.defaultPrevented) return;
      var d = cartDrawer();
      if (!d) return;
      var trig = (ev.detail && ev.detail.trigger) || doc.querySelector('[data-hm-cart-open]');
      HM.open(d, { trigger: trig, returnFocus: (ev.detail && ev.detail.trigger) || doc.activeElement });
    };
    if (window.queueMicrotask) queueMicrotask(run);
    else setTimeout(run, 0);
  });
  doc.addEventListener('hm:cart:close', function () {
    var d = cartDrawer();
    if (d && HM.current() === d) HM.close();
  });
  HM.setCartCount = function (n) {
    n = Math.max(0, parseInt(n, 10) || 0);
    doc.querySelectorAll('[data-hm-cart-count]').forEach(function (c) {
      c.textContent = n;
      c.setAttribute('data-n', n);
    });
    doc.querySelectorAll('[data-hm-cart-open]').forEach(function (b) {
      b.setAttribute('aria-label', 'Cart, ' + n + (n === 1 ? ' item' : ' items'));
    });
  };
  doc.addEventListener('hm:cart:updated', function (e) {
    var d = e.detail || {};
    /* detail.count (hm-cart.js) leaves the Feed The Beast tip out, so it wins over cart.item_count */
    var n = d.count != null ? d.count : d.item_count != null ? d.item_count : d.cart && d.cart.item_count;
    if (n != null) HM.setCartCount(n);
  });

  /* ---------- announcement rotation ---------- */
  function initAnnounce(el) {
    var msgs = el.querySelectorAll('[data-hm-announce-msg]');
    var btn = el.querySelector('[data-hm-announce-toggle]');
    if (msgs.length < 2) return function () {};
    var interval = Math.max(3000, parseInt(el.getAttribute('data-interval'), 10) || 4000);
    var i = 0;
    var playing = !reduceMotion.matches;
    var paused = false; /* hover or focus inside */
    var timer = null;
    function show(n) {
      msgs.forEach(function (m, k) {
        m.hidden = k !== n;
      });
    }
    function tick() {
      if (!playing || paused || doc.hidden) return;
      i = (i + 1) % msgs.length;
      show(i);
    }
    function setBtn() {
      if (!btn) return;
      btn.setAttribute('aria-label', btn.getAttribute(playing ? 'data-label-pause' : 'data-label-play'));
      var p = btn.querySelector('[data-icon-pause]');
      var pl = btn.querySelector('[data-icon-play]');
      if (p) p.hidden = !playing;
      if (pl) pl.hidden = playing;
    }
    function toggle() {
      playing = !playing;
      setBtn();
    }
    function hoverIn() {
      paused = true;
    }
    function hoverOut() {
      paused = el.contains(doc.activeElement);
    }
    timer = setInterval(tick, interval);
    setBtn();
    if (btn) btn.addEventListener('click', toggle);
    el.addEventListener('mouseenter', hoverIn);
    el.addEventListener('mouseleave', hoverOut);
    el.addEventListener('focusin', hoverIn);
    el.addEventListener('focusout', hoverOut);
    return function () {
      clearInterval(timer);
      if (btn) btn.removeEventListener('click', toggle);
      el.removeEventListener('mouseenter', hoverIn);
      el.removeEventListener('mouseleave', hoverOut);
      el.removeEventListener('focusin', hoverIn);
      el.removeEventListener('focusout', hoverOut);
    };
  }

  /* ---------- sponsor strip ---------- */
  function initSponsors(el) {
    var btn = el.querySelector('[data-hm-spx-toggle]');
    var track = el.querySelector('[data-hm-spx-track]');
    function toggle() {
      var on = btn.getAttribute('aria-pressed') !== 'true';
      btn.setAttribute('aria-pressed', on ? 'true' : 'false');
      var label = btn.querySelector('[data-hm-spx-label]');
      if (label) label.textContent = on ? 'Play' : 'Pause';
      var p = btn.querySelector('[data-icon-pause]');
      var pl = btn.querySelector('[data-icon-play]');
      if (p) p.hidden = on;
      if (pl) pl.hidden = !on;
      el.classList.toggle('is-paused', on);
    }
    /* a logo with keyboard focus stops the belt and turns it into a scrollable row */
    function fin() {
      el.classList.add('is-focus');
    }
    function fout(e) {
      if (!e.relatedTarget || !track.contains(e.relatedTarget)) el.classList.remove('is-focus');
    }
    if (btn) btn.addEventListener('click', toggle);
    if (track) {
      track.addEventListener('focusin', fin);
      track.addEventListener('focusout', fout);
    }
    return function () {
      if (btn) btn.removeEventListener('click', toggle);
      if (track) {
        track.removeEventListener('focusin', fin);
        track.removeEventListener('focusout', fout);
      }
    };
  }

  /* ---------- footer ---------- */
  function initFooter(el) {
    var mq = window.matchMedia('(max-width: 860px)');
    var accs = el.querySelectorAll('[data-hm-acc]');
    function sync() {
      accs.forEach(function (d) {
        d.open = !mq.matches;
      });
    }
    if (mq.matches) sync();
    var onMq = function () {
      sync();
    };
    if (mq.addEventListener) mq.addEventListener('change', onMq);

    var form = el.querySelector('form');
    var email = el.querySelector('[data-hm-news-email]');
    var msg = el.querySelector('[data-hm-news-msg]');
    function onSubmit(e) {
      if (!email) return;
      var v = (email.value || '').trim();
      email.value = v;
      if (!v || !email.checkValidity()) {
        e.preventDefault();
        email.setAttribute('aria-invalid', 'true');
        if (msg) {
          msg.textContent = msg.getAttribute('data-error') || 'Enter a valid email.';
          msg.classList.add('form-msg--error');
        }
        email.focus();
        return;
      }
      email.removeAttribute('aria-invalid');
    }
    function onInput() {
      if (email.getAttribute('aria-invalid') === 'true' && email.checkValidity()) {
        email.removeAttribute('aria-invalid');
        if (msg) {
          msg.textContent = '';
          msg.classList.remove('form-msg--error');
        }
      }
    }
    if (form && email) {
      form.addEventListener('submit', onSubmit);
      email.addEventListener('input', onInput);
    }
    var year = el.querySelector('[data-hm-year]');
    if (year) year.textContent = String(new Date().getFullYear());
    return function () {
      if (mq.removeEventListener) mq.removeEventListener('change', onMq);
      if (form && email) {
        form.removeEventListener('submit', onSubmit);
        email.removeEventListener('input', onInput);
      }
    };
  }

  /* Cookie Preferences: Shopify's native privacy banner */
  doc.addEventListener('click', function (e) {
    var b = e.target.closest('[data-hm-cookie-prefs]');
    if (!b) return;
    e.preventDefault();
    var pb = window.privacyBanner;
    if (pb && typeof pb.showPreferences === 'function') {
      pb.showPreferences();
      return;
    }
    if (window.Shopify && typeof window.Shopify.loadFeatures === 'function') {
      window.Shopify.loadFeatures([{ name: 'consent-tracking-api', version: '0.1' }], function (err) {
        var p = window.privacyBanner;
        if (!err && p && typeof p.showPreferences === 'function') p.showPreferences();
        else location.href = b.getAttribute('data-fallback') || '/policies/privacy-policy';
      });
      return;
    }
    location.href = b.getAttribute('data-fallback') || '/policies/privacy-policy';
  });

  /* ---------- horizontal strips: fade the edge that has more content ---------- */
  function hsUpdate(el) {
    var max = el.scrollWidth - el.clientWidth;
    el.classList.toggle('hm-hs--l', max > 2 && el.scrollLeft > 4);
    el.classList.toggle('hm-hs--r', max > 2 && el.scrollLeft < max - 4);
  }
  function hsScan() {
    doc.querySelectorAll('[data-hm-hs], .cats, .addons__row, main [data-hm-strip]').forEach(function (el) {
      if (el.closest('[data-no-fade]')) return;
      if (!el.hmHs) {
        el.hmHs = true;
        el.addEventListener('scroll', function () {
          hsUpdate(el);
        }, { passive: true });
      }
      hsUpdate(el);
    });
  }
  HM.refreshStrips = hsScan;
  var hsTimer;
  window.addEventListener('resize', function () {
    clearTimeout(hsTimer);
    hsTimer = setTimeout(hsScan, 150);
  });
  doc.addEventListener('hm:dialog:open', function () {
    setTimeout(hsScan, 30);
  });

  /* ---------- init and theme editor support ---------- */
  var registry = new WeakMap();
  var MODULES = [
    ['[data-hm-header]', initHeader],
    ['[data-hm-announce]', initAnnounce],
    ['[data-hm-spx]', initSponsors],
    ['[data-hm-footer]', initFooter]
  ];
  function initIn(scope) {
    MODULES.forEach(function (mod) {
      var list = [];
      if (scope.matches && scope.matches(mod[0])) list.push(scope);
      scope.querySelectorAll(mod[0]).forEach(function (n) {
        list.push(n);
      });
      list.forEach(function (n) {
        if (registry.has(n)) return;
        registry.set(n, mod[1](n) || function () {});
      });
    });
    hsScan();
  }
  function destroyIn(scope) {
    MODULES.forEach(function (mod) {
      scope.querySelectorAll(mod[0]).forEach(function (n) {
        var off = registry.get(n);
        if (off) {
          off();
          registry.delete(n);
        }
      });
    });
    if (current && scope.contains(current.el)) HM.close({ restore: false });
    if (openMenu && scope.contains(openMenu.trigger)) openMenu.close(false);
  }
  HM.init = initIn;

  function boot() {
    initIn(doc);
  }
  if (doc.readyState === 'loading') doc.addEventListener('DOMContentLoaded', boot);
  else boot();
  window.addEventListener('load', hsScan);

  doc.addEventListener('shopify:section:load', function (e) {
    initIn(e.target);
  });
  doc.addEventListener('shopify:section:unload', function (e) {
    destroyIn(e.target);
  });
  /* editor: selecting a header block or the drawer shows it */
  doc.addEventListener('shopify:section:deselect', function (e) {
    if (current && e.target.contains(current.el)) HM.close({ restore: false });
  });
})();
