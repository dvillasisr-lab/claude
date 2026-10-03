/* Heavy Metal boceto v2: header, mega menú, menú móvil, carrito y footer compartidos.
   Cada página pone <div data-hm-header data-current="home|shop|machine|story|schedule|sponsors"></div>
   arriba y <div data-hm-footer></div> abajo, y carga este archivo con defer. */
(function () {
  var I = {
    search: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg>',
    user: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/></svg>',
    bag: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 8h14l-1 13H6L5 8Z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg>',
    menu: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 7h18M3 12h18M3 17h18"/></svg>',
    close: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 5l14 14M19 5 5 19"/></svg>'
  };
  var PAGES = [
    ['shop', 'shop.html', 'Shop'],
    ['machine', 'machine.html', 'The Machine'],
    ['story', 'story.html', 'Our Story'],
    ['schedule', 'schedule.html', 'Schedule'],
    ['sponsors', 'sponsors.html', 'Sponsors']
  ];
  function nav(cur, list) {
    return list.map(function (p) {
      return '<a href="' + p[1] + '"' + (p[0] === cur ? ' aria-current="page"' : '') +
        (p[0] === 'shop' ? ' data-mega-trigger aria-haspopup="true" aria-expanded="false"' : '') + '>' + p[2] + '</a>';
    }).join('');
  }

  var h = document.querySelector('[data-hm-header]');
  if (h) {
    var cur = h.getAttribute('data-current') || '';
    h.outerHTML =
      '<div class="draftbar"><span>Boceto v2 · no es el sitio en vivo</span>' +
      '<a href="index.html">Home</a><a href="shop.html">Shop</a><a href="product.html">Producto</a>' +
      '<a href="machine.html">Machine</a><a href="story.html">Story</a><a href="schedule.html">Schedule</a><a href="sponsors.html">Sponsors</a></div>' +
      '<p class="announce">Testing season: <a href="schedule.html#alerts">get Hook Alerts</a> · Free US shipping over $XX</p>' +
      '<header class="hdr" id="hdr"><div class="wrap hdr__in">' +
        '<div style="display:flex;align-items:center;gap:8px">' +
          '<button class="icon-btn menu-btn" type="button" id="menu-open" aria-label="Open menu">' + I.menu + '</button>' +
          '<nav class="hdr__nav" aria-label="Main">' + nav(cur, PAGES.slice(0, 3)) + '</nav>' +
        '</div>' +
        '<a class="logo" href="index.html" aria-label="Heavy Metal home">Heavy Metal</a>' +
        '<div class="hdr__right">' +
          '<nav class="hdr__nav" aria-label="More">' + nav(cur, PAGES.slice(3)) + '</nav>' +
          '<a class="hdr__word hdr__word--hide" href="shop.html">Search</a>' +
          '<a class="hdr__word hdr__word--hide" href="#">Account</a>' +
          '<button class="hdr__word" type="button" id="cart-open" aria-label="Cart, 0 items">Cart (<span id="cart-count">0</span>)</button>' +
        '</div>' +
      '</div>' +
      '<div class="mega" id="mega" hidden><div class="wrap mega__in">' +
        '<div><p class="label muted">Shop</p><ul><li><a href="shop.html">Shop all</a></li><li><a href="shop.html#new">New drop</a></li><li><a href="shop.html#best">Best sellers</a></li><li><a href="product.html">Crew Pack bundle</a></li></ul></div>' +
        '<div><p class="label muted">Category</p><ul><li><a href="shop.html#tees">Tees</a></li><li><a href="shop.html#sweats">Sweatshirts</a></li><li><a href="shop.html#hats">Hats</a></li><li><a href="shop.html#kids">Kids</a></li><li><a href="shop.html#gear">Stickers &amp; gear</a></li></ul></div>' +
        '<a class="mega__card" href="shop.html#new"><div class="ph" style="--ar:4/3"><div class="ph__tag"><b>Foto · 4:3</b>Drop actual en modelo junto al tractor</div></div><span class="label">The new drop</span></a>' +
        '<a class="mega__card" href="index.html#ride"><div class="ph ph--dark" style="--ar:4/3"><div class="ph__tag"><b>Foto · 4:3</b>Nombres de fans en el panel del tractor</div></div><span class="label">Put your name on the tractor</span></a>' +
      '</div></div>' +
      '</header>' +
      '<div class="mnav" id="mnav" hidden role="dialog" aria-modal="true" aria-label="Menu">' +
        '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px"><span class="logo">Heavy Metal</span><button class="icon-btn" type="button" id="menu-close" aria-label="Close menu">' + I.close + '</button></div>' +
        '<a href="index.html">Home</a>' + nav(cur, PAGES) +
        '<a href="shop.html#tees" style="font-size:var(--t-md);font-weight:500">Tees</a><a href="shop.html#sweats" style="font-size:var(--t-md);font-weight:500">Sweatshirts</a><a href="shop.html#hats" style="font-size:var(--t-md);font-weight:500">Hats</a><a href="shop.html#kids" style="font-size:var(--t-md);font-weight:500">Kids</a>' +
      '</div>' +
      '<div class="scrim" id="scrim" hidden></div>' +
      '<aside class="drawer" id="drawer" role="dialog" aria-modal="true" aria-labelledby="drawer-t" hidden>' +
        '<div class="drawer__head"><p class="label" id="drawer-t">Your cart (<span id="drawer-count">0</span>)</p><button class="icon-btn" type="button" id="cart-close" aria-label="Close cart">' + I.close + '</button></div>' +
        '<div class="drawer__body">' +
          '<div style="display:grid;gap:8px"><p style="margin:0;font-size:var(--t-sm)"><b>$XX</b> away from free US shipping</p><div class="meter" style="--fill:40%"><span></span></div></div>' +
          '<ul id="lines" style="list-style:none;margin:0;padding:0;display:grid;gap:16px"></ul>' +
          '<p id="empty" style="margin:0;color:var(--mute)">Your cart is empty. <a href="shop.html">Shop the drop</a></p>' +
          '<div class="upsell"><p class="label">Ride With The Evil One</p><p style="margin:0;font-weight:600">Put your name on the tractor · $XX</p><p style="margin:0;font-size:var(--t-sm);color:var(--soft)">Your name rides on the crew panel all season. We check every name before it goes on.</p><button class="btn btn--ghost" type="button" data-add="Ride With The Evil One|Crew name|$XX">Add my name</button></div>' +
        '</div>' +
        '<div class="drawer__foot"><p style="display:flex;justify-content:space-between;margin:0;font-weight:600"><span>Subtotal</span><span class="num">$XX</span></p><p style="margin:0;font-size:var(--t-xs);color:var(--mute)">Taxes and shipping at checkout. Printed on demand, ships in X to X business days.</p><button class="btn btn--block" type="button">Checkout</button></div>' +
      '</aside>';
  }

  var f = document.querySelector('[data-hm-footer]');
  if (f) {
    f.outerHTML =
      '<footer class="ftr"><div class="wrap">' +
        '<div class="ftr__top">' +
          '<div><span class="logo" style="color:var(--surface)">Heavy Metal</span><p style="margin:12px 0 0;max-width:34ch">The Evil One. Pro Stock pulling tractor from Waterloo, Wisconsin. Merch designed by the team.</p>' +
            '<form class="ftr__news" onsubmit="event.preventDefault();this.querySelector(\'button\').textContent=\'You\\\'re in\'"><label class="vh" for="ftr-email">Email</label><input class="input" id="ftr-email" type="email" placeholder="Email for drops and Hook Alerts"><button class="btn" type="submit">Join</button></form></div>' +
          '<div><p class="label">Shop</p><ul><li><a href="shop.html">Shop all</a></li><li><a href="shop.html#tees">Tees</a></li><li><a href="shop.html#sweats">Sweatshirts</a></li><li><a href="shop.html#hats">Hats</a></li><li><a href="shop.html#kids">Kids</a></li></ul></div>' +
          '<div><p class="label">The team</p><ul><li><a href="machine.html">The Machine</a></li><li><a href="story.html">Our Story</a></li><li><a href="schedule.html">Schedule</a></li><li><a href="sponsors.html">Sponsors</a></li><li><a href="https://www.facebook.com/heavymetalprostock/">Facebook</a></li></ul></div>' +
          '<div><p class="label">Help</p><ul><li><a href="#">Shipping</a></li><li><a href="#">Returns</a></li><li><a href="#">Size guide</a></li><li><a href="#">Contact</a></li></ul></div>' +
        '</div>' +
        '<div class="ftr__bottom"><span>© 2026 Heavy Metal Pro Stock · Waterloo, WI</span><span>NTPA · PPL Badger State</span></div>' +
      '</div></footer>';
  }

  var $ = function (id) { return document.getElementById(id); };
  var count = 0, last = null;

  /* mega menú: hover o clic en Shop (desktop) */
  var trig = document.querySelector('[data-mega-trigger]'), mega = $('mega'), hdr = $('hdr');
  if (trig && mega) {
    var t;
    var show = function () { clearTimeout(t); mega.hidden = false; trig.setAttribute('aria-expanded', 'true'); };
    var hide = function () { t = setTimeout(function () { mega.hidden = true; trig.setAttribute('aria-expanded', 'false'); }, 120); };
    trig.addEventListener('mouseenter', show);
    trig.addEventListener('focus', show);
    hdr.addEventListener('mouseleave', hide);
    mega.addEventListener('mouseenter', show);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { mega.hidden = true; trig.setAttribute('aria-expanded', 'false'); } });
  }

  /* menú móvil */
  var mnav = $('mnav');
  if (mnav) {
    $('menu-open').addEventListener('click', function () { mnav.hidden = false; document.body.style.overflow = 'hidden'; $('menu-close').focus(); });
    $('menu-close').addEventListener('click', function () { mnav.hidden = true; document.body.style.overflow = ''; $('menu-open').focus(); });
  }

  /* carrito */
  var drawer = $('drawer'), scrim = $('scrim');
  function setCount(n) {
    count = n;
    $('cart-count').textContent = n; $('drawer-count').textContent = n;
    $('cart-open').setAttribute('aria-label', 'Cart, ' + n + ' items');
    $('empty').hidden = n > 0;
  }
  function openCart() { last = document.activeElement; drawer.hidden = scrim.hidden = false; document.body.style.overflow = 'hidden'; $('cart-close').focus(); }
  function closeCart() { drawer.hidden = scrim.hidden = true; document.body.style.overflow = ''; if (last && last.focus) last.focus(); }
  if (drawer) {
    $('cart-open').addEventListener('click', openCart);
    $('cart-close').addEventListener('click', closeCart);
    scrim.addEventListener('click', closeCart);
    drawer.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeCart(); });
  }
  /* cualquier botón con data-add="Nombre|Variante|$XX" agrega una línea y abre el carrito */
  window.hmAdd = function (spec) {
    var p = spec.split('|');
    var li = document.createElement('li'); li.className = 'line';
    li.innerHTML = '<div class="ph" style="--ar:4/5"></div><div><p style="margin:0;font-weight:600;font-size:var(--t-sm);text-transform:uppercase;letter-spacing:.06em">' + p[0] + '</p><p style="margin:2px 0 0;font-size:var(--t-sm);color:var(--mute)">' + (p[1] || '') + '</p></div><p class="num" style="margin:0">' + (p[2] || '$XX') + '</p>';
    $('lines').appendChild(li); setCount(count + 1); openCart();
  };
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-add]'); if (!b) return;
    e.preventDefault(); window.hmAdd(b.getAttribute('data-add'));
  });
  if (drawer) setCount(0);
})();
