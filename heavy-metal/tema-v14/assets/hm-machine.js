/* The Machine: anatomy hotspots (roving tabindex, arrows, Home/End, prev/next) and the "Hear it" video facade.
   Works with the theme editor: re-inits on shopify:section:load and cleans up on unload. */
(function () {
  if (window.hmMachine) return;

  function pad(n) { return (n < 10 ? '0' : '') + n; }

  function initAnatomy(root) {
    if (!root || root.hmAnat) return;
    var pts = root.querySelector('[data-anat-pts]');
    if (!pts) return;
    var hs = Array.prototype.slice.call(pts.querySelectorAll('.mx-hs'));
    if (!hs.length) return;
    var stage = root.querySelector('.mx-stage');
    var label = root.querySelector('[data-anat-label]');
    var val = root.querySelector('[data-anat-val]');
    var body = root.querySelector('[data-anat-body]');
    var count = root.querySelector('[data-anat-count]');
    var imgs = Array.prototype.slice.call(root.querySelectorAll('.mx-panel__img'));
    var cur = 0;

    function set(i, focus) {
      cur = (i + hs.length) % hs.length;
      var b = hs[cur];
      hs.forEach(function (x, j) {
        x.setAttribute('aria-pressed', j === cur ? 'true' : 'false');
        x.tabIndex = j === cur ? 0 : -1;
      });
      stage.querySelectorAll('.mx-tag, line').forEach(function (e) {
        e.classList.toggle('on', +e.getAttribute('data-i') === cur);
      });
      if (label) label.textContent = pad(cur + 1) + ' · ' + b.getAttribute('data-name');
      if (val) val.textContent = b.getAttribute('data-value');
      if (body) body.textContent = b.getAttribute('data-text');
      if (count) count.textContent = pad(cur + 1) + ' / ' + pad(hs.length);
      imgs.forEach(function (im) { im.hidden = +im.getAttribute('data-i') !== cur; });
      if (focus) b.focus();
    }

    function onClick(e) {
      var t = e.target;
      if (t.closest('[data-anat-prev]')) { set(cur - 1); return; }
      if (t.closest('[data-anat-next]')) { set(cur + 1); return; }
      var p = t.closest('.mx-hs, .mx-tag');
      if (p && stage.contains(p)) set(+p.getAttribute('data-i'), p.classList.contains('mx-hs'));
    }
    function onKey(e) {
      if (!e.target.classList || !e.target.classList.contains('mx-hs')) return;
      var k = e.key;
      if (k === 'Home') { e.preventDefault(); set(0, true); return; }
      if (k === 'End') { e.preventDefault(); set(hs.length - 1, true); return; }
      var d = k === 'ArrowRight' || k === 'ArrowDown' ? 1 : k === 'ArrowLeft' || k === 'ArrowUp' ? -1 : 0;
      if (d) { e.preventDefault(); set(cur + d, true); }
    }
    root.addEventListener('click', onClick);
    pts.addEventListener('keydown', onKey);
    root.hmAnat = function () {
      root.removeEventListener('click', onClick);
      pts.removeEventListener('keydown', onKey);
      root.hmAnat = null;
    };
  }

  /* video facade: the iframe is only created after a click */
  function embedUrl(type, id) {
    if (type === 'vimeo') return 'https://player.vimeo.com/video/' + encodeURIComponent(id) + '?autoplay=1';
    return 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(id) + '?autoplay=1&rel=0&playsinline=1';
  }
  function onVideoClick(e) {
    var b = e.target.closest('[data-video-play]');
    if (!b) return;
    var box = b.closest('[data-video-box]');
    if (!box) return;
    var f = document.createElement('iframe');
    f.src = embedUrl(b.getAttribute('data-video-type'), b.getAttribute('data-video-id'));
    f.title = b.getAttribute('data-video-title') || 'Video';
    f.setAttribute('allow', 'autoplay; encrypted-media; fullscreen; picture-in-picture');
    f.setAttribute('allowfullscreen', '');
    box.classList.add('is-playing');
    b.remove();
    box.appendChild(f);
    f.focus();
  }

  function initAll(scope) {
    (scope || document).querySelectorAll('[data-hm-anatomy]').forEach(initAnatomy);
  }

  document.addEventListener('click', onVideoClick);
  document.addEventListener('shopify:section:load', function (e) { initAll(e.target); });
  document.addEventListener('shopify:section:unload', function (e) {
    e.target.querySelectorAll('[data-hm-anatomy]').forEach(function (r) { if (r.hmAnat) r.hmAnat(); });
  });

  window.hmMachine = { init: initAll };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { initAll(); });
  else initAll();
})();
