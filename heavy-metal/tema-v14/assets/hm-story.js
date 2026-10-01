/* Our Story: milestone jumps into the chapter carousel, lightning flicker, video facade (file or YouTube/Vimeo),
   Spotify facade (iframe only after a click) and the season select. Editor safe (section load/unload). */
(function () {
  if (window.hmStory) return;
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var observers = [];

  function embedUrl(type, id) {
    if (type === 'vimeo') return 'https://player.vimeo.com/video/' + encodeURIComponent(id) + '?autoplay=1';
    return 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(id) + '?autoplay=1&rel=0&playsinline=1';
  }

  function onClick(e) {
    var t = e.target;

    /* video facade */
    var soon = t.closest('[data-video-soon]');
    if (soon) {
      var fig = soon.closest('figure');
      var msg = fig && fig.querySelector('[data-video-msg]');
      if (msg) msg.textContent = soon.getAttribute('data-video-soon');
      return;
    }
    var play = t.closest('[data-video-play]');
    if (play && play.closest('.st-vid')) {
      var box = play.closest('[data-video-box]');
      var el;
      if (play.getAttribute('data-video-type') === 'file') {
        var tpl = box.querySelector('template[data-video-tpl]');
        if (!tpl) return;
        el = tpl.content.firstElementChild.cloneNode(true);
      } else {
        el = document.createElement('iframe');
        el.src = embedUrl(play.getAttribute('data-video-type'), play.getAttribute('data-video-id'));
        el.title = play.getAttribute('data-video-title') || 'Video';
        el.setAttribute('allow', 'autoplay; encrypted-media; fullscreen; picture-in-picture');
        el.setAttribute('allowfullscreen', '');
      }
      box.classList.add('is-playing');
      play.remove();
      box.appendChild(el);
      if (el.play) { try { el.play(); } catch (err) {} }
      el.setAttribute('tabindex', '-1');
      el.focus();
      return;
    }

    /* Spotify facade */
    var sp = t.closest('[data-spotify-load]');
    if (sp) {
      var spBox = sp.closest('[data-spotify-box]');
      var f = document.createElement('iframe');
      f.src = 'https://open.spotify.com/embed/playlist/' + encodeURIComponent(sp.getAttribute('data-spotify-load')) + '?utm_source=generator';
      f.title = 'Spotify player: ' + (sp.getAttribute('data-spotify-title') || 'playlist');
      f.setAttribute('allow', 'autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture');
      f.setAttribute('loading', 'lazy');
      spBox.innerHTML = '';
      spBox.appendChild(f);
      f.focus();
      return;
    }

    /* milestones: scroll to the chapter and, in the phone carousel, slide to the card */
    var a = t.closest('a[data-st-jump]');
    if (a) {
      var id = (a.getAttribute('href') || '').replace(/^#/, '');
      var card = id && document.getElementById(id);
      if (!card) return;
      e.preventDefault();
      var hdr = document.querySelector('.hdr, header');
      var off = (hdr ? hdr.getBoundingClientRect().height : 56) + 12;
      var behavior = reduce ? 'auto' : 'smooth';
      window.scrollTo({ top: card.getBoundingClientRect().top + window.scrollY - off, behavior: behavior });
      var chs = card.closest('.st-chs');
      if (chs) {
        if (chs.scrollWidth > chs.clientWidth) chs.scrollTo({ left: card.offsetLeft - chs.offsetLeft - parseFloat(getComputedStyle(chs).paddingLeft || 0), behavior: behavior });
        Array.prototype.forEach.call(chs.children, function (c) { c.classList.toggle('is-hit', c === card); });
      }
      if (history.replaceState) history.replaceState(null, '', '#' + id);
      card.setAttribute('tabindex', '-1');
      card.focus({ preventScroll: true });
    }
  }

  function onChange(e) {
    var s = e.target.closest('[data-st-season-select]');
    if (!s) return;
    var band = s.closest('[data-st-season]');
    band.querySelectorAll('[data-season]').forEach(function (d) { d.hidden = d.getAttribute('data-season') !== s.value; });
  }

  function init(scope) {
    (scope || document).querySelectorAll('[data-st-bolt]').forEach(function (s) {
      if (reduce || !('IntersectionObserver' in window) || s.hmIo) return;
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (en) { if (en.isIntersecting) { s.classList.add('is-on'); io.disconnect(); } });
      }, { threshold: 0.45 });
      io.observe(s);
      s.hmIo = io;
      observers.push(io);
    });
  }

  document.addEventListener('click', onClick);
  document.addEventListener('change', onChange);
  document.addEventListener('shopify:section:load', function (e) { init(e.target); });
  document.addEventListener('shopify:section:unload', function (e) {
    e.target.querySelectorAll('[data-st-bolt]').forEach(function (s) { if (s.hmIo) { s.hmIo.disconnect(); s.hmIo = null; } });
  });
  window.hmStory = { init: init };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { init(); });
  else init();
})();
