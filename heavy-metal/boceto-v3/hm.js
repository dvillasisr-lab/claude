/* Heavy Metal boceto v3: header, mega menú, menú móvil, búsqueda, selector de talla, carrito,
   footer, banner de cookies. Cada página pone:
   <div data-hm-header data-current="home|shop|machine|story|schedule|sponsors|account|policies|contact"></div>
   <div data-hm-footer></div>  y carga <script src="hm.js"></script> al final del body. */
(function () {
  /* cada página abre arriba (en el visor el scroll se conservaba entre páginas) */
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
  if (!location.hash) window.scrollTo(0, 0);

  var I = {
    search: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg>',
    user: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/></svg>',
    bag: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 8h14l-1 13H6L5 8Z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg>',
    menu: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 7h18M3 12h18M3 17h18"/></svg>',
    close: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 5l14 14M19 5 5 19"/></svg>',
    arrow: '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    pause: '<svg viewBox="0 0 12 12" aria-hidden="true"><rect x="2" y="1" width="3" height="10"/><rect x="7" y="1" width="3" height="10"/></svg>',
    play: '<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2 1l9 5-9 5z"/></svg>',
    fb: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 8h3V4h-3c-2.8 0-4.5 1.8-4.5 4.6V11H7v4h2.5v9h4v-9h3l.5-4h-3.5V9c0-.6.4-1 1-1Z"/></svg>',
    ig: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 7.3A4.7 4.7 0 1 0 12 16.7 4.7 4.7 0 0 0 12 7.3Zm0 7.7a3 3 0 1 1 0-6 3 3 0 0 1 0 6Zm4.9-8.9a1.1 1.1 0 1 1 0 2.2 1.1 1.1 0 0 1 0-2.2ZM12 3c2.4 0 2.7 0 3.7.1 2.5.1 3.6 1.3 3.7 3.7.1.9.1 1.2.1 3.7v3c0 2.4 0 2.7-.1 3.7-.1 2.4-1.2 3.6-3.7 3.7-.9.1-1.2.1-3.7.1h-3c-2.4 0-2.7 0-3.7-.1-2.5-.1-3.6-1.3-3.7-3.7C1.5 16.2 1.5 15.9 1.5 13.5v-3c0-2.5 0-2.8.1-3.7C1.7 4.4 2.8 3.2 5.3 3.1 6.2 3 6.5 3 9 3h3Z"/></svg>',
    yt: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M23 7.2a3 3 0 0 0-2.1-2.1C19 4.6 12 4.6 12 4.6s-7 0-8.9.5A3 3 0 0 0 1 7.2 31 31 0 0 0 .5 12a31 31 0 0 0 .5 4.8 3 3 0 0 0 2.1 2.1c1.9.5 8.9.5 8.9.5s7 0 8.9-.5a3 3 0 0 0 2.1-2.1 31 31 0 0 0 .5-4.8 31 31 0 0 0-.5-4.8ZM9.8 15.1V8.9L15.6 12l-5.8 3.1Z"/></svg>',
    tt: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16.6 2h-3.4v13.2a2.9 2.9 0 1 1-2.9-2.9c.3 0 .6 0 .9.1V8.9a6.4 6.4 0 1 0 5.4 6.3V8.6a8.1 8.1 0 0 0 4.4 1.3V6.5a4.6 4.6 0 0 1-4.4-4.5Z"/></svg>'
  };

  /* catálogo de ejemplo (nombres de ejemplo, precios $XX). sizes vacío = talla única */
  var TEE = ['S', 'M', 'L', 'XL', '2XL', '3XL'];
  var CAT = window.HM_CATALOG = [
    { id: 'evil-one-tee', name: 'Evil One Tee', sub: 'Front logo tee', cat: 'tees', colors: ['Matte Black', 'Smoke Gray'], sizes: TEE, sold: ['3XL'], tag: 'best' },
    { id: 'lightning-strike-tee', name: 'Lightning Strike Tee', sub: 'First fire graphic', cat: 'tees', colors: ['Matte Black'], sizes: TEE, tag: 'new' },
    { id: 'full-pull-ls', name: 'Full Pull or Nothing Long Sleeve', sub: 'Back print', cat: 'tees', colors: ['Matte Black', 'Bone'], sizes: TEE },
    { id: 'cat-v8-spec-tee', name: 'Cat V8 Spec Tee', sub: 'Spec sheet print', cat: 'tees', colors: ['Smoke Gray'], sizes: TEE },
    { id: '680-ci-hoodie', name: '680 CI Hoodie', sub: 'Pullover hoodie', cat: 'sweats', colors: ['Matte Black', 'Smoke Gray'], sizes: TEE, tag: 'best' },
    { id: 'evil-one-crewneck', name: 'The Evil One Crewneck', sub: 'Crewneck sweatshirt', cat: 'sweats', colors: ['Bone'], sizes: TEE, tag: 'new' },
    { id: 'crew-cap', name: 'Crew Cap', sub: 'Structured cap', cat: 'hats', colors: ['Black'], sizes: [], tag: 'best' },
    { id: 'evil-one-beanie', name: 'Evil One Beanie', sub: 'Cuffed knit', cat: 'hats', colors: ['Black', 'Safety Yellow'], sizes: [], tag: 'new' },
    { id: 'little-evil-one-tee', name: 'Little Evil One Kids Tee', sub: 'Youth sizes', cat: 'kids', colors: ['Matte Black'], sizes: ['YS', 'YM', 'YL', 'YXL'] },
    { id: 'kids-hoodie', name: 'Kids Hoodie', sub: 'Youth pullover', cat: 'kids', colors: ['Smoke Gray'], sizes: ['YS', 'YM', 'YL', 'YXL'] },
    { id: 'sticker-pack', name: 'Sticker Pack', sub: 'Die cut set', cat: 'gear', colors: [], sizes: [] },
    { id: 'hook-alert-koozie', name: 'Hook Alert Koozie', sub: 'Keep it cold', cat: 'gear', colors: [], sizes: [] },
    { id: 'crew-pack', name: 'Crew Pack Bundle', sub: 'Tee plus cap', cat: 'bundles', colors: [], sizes: TEE, tag: 'bundle' },
    { id: 'ride-with-the-evil-one', name: 'Ride With The Evil One', sub: 'Your name on the tractor', cat: 'ride', colors: [], sizes: [], tag: 'limited', page: 'ride.html' }
  ];
  var CATS = [
    ['all', 'Shop all'], ['new', 'New drop'], ['tees', 'Tees'], ['sweats', 'Sweatshirts'], ['hats', 'Hats'],
    ['kids', 'Kids'], ['gear', 'Stickers & gear'], ['bundles', 'Bundles'], ['ride', 'Ride with us']
  ];
  var SW = { 'Matte Black': 'var(--ink)', 'Black': 'var(--ink)', 'Smoke Gray': '#8C8A82', 'Bone': '#E9E6DC', 'Safety Yellow': 'var(--accent)' };
  window.HM_SW = SW;
  function href(p) { return p.page || 'product.html?p=' + p.id; }
  function thumb(label, dark) { return '<span class="thumb"><span class="ph' + (dark ? ' ph--dark' : '') + '"><span class="ph__tag"><b>Foto</b>' + label + '</span></span></span>'; }

  /* tarjeta reutilizable: window.hmCard(producto) */
  window.hmCard = function (p) {
    var badge = p.tag === 'best' ? '<span class="badge">Best seller</span>' : p.tag === 'new' ? '<span class="badge badge--ink">New</span>' :
      p.tag === 'bundle' ? '<span class="badge badge--line">Save $X</span>' : p.tag === 'limited' ? '<span class="badge badge--ink">Limited</span>' : '';
    var sw = p.colors.map(function (c) { return '<span class="swatch" style="--sw:' + SW[c] + '" title="' + c + '"></span>'; }).join('');
    var btn = p.page ? '<a class="btn card__add" href="' + p.page + '">Add your name · $XX</a>' :
      '<button class="btn card__add" type="button" data-quick="' + p.id + '">Add to cart · $XX<span class="vh"> ' + p.name + '</span></button>';
    return '<article class="card" data-cat="' + p.cat + '" data-tag="' + (p.tag || '') + '" data-colors="' + p.colors.join('|') + '" data-sizes="' + p.sizes.join('|') + '">' +
      '<div class="card__media"><a href="' + href(p) + '" tabindex="-1" aria-hidden="true"><span class="ph' + (p.cat === 'ride' ? ' ph--dark' : '') + '"><span class="ph__tag"><b>Foto · 4:5</b>' + p.name + (p.cat === 'ride' ? ', nombres en el panel del tractor' : ', foto de producto sobre fondo liso') + '</span></span></a>' +
      (badge ? '<div class="card__badges">' + badge + '</div>' : '') + btn + '</div>' +
      '<div class="card__txt"><h3 class="card__name"><a href="' + href(p) + '">' + p.name + '</a></h3><p class="card__sub">' + p.sub + '</p>' +
      '<div class="card__meta"><span class="num">$XX</span><span class="swatches">' + sw + '</span></div></div></article>';
  };
  /* fotitos de categoría: window.hmCats(actual) */
  window.hmCats = function (cur) {
    return '<ul class="cats" aria-label="Shop by category">' + CATS.map(function (c) {
      return '<li><a class="cat" href="shop.html?cat=' + c[0] + '"' + (c[0] === cur ? ' aria-current="true"' : '') + '>' + thumb(c[1], c[0] === 'ride') + '<span>' + c[1] + '</span></a></li>';
    }).join('') + '</ul>';
  };

  var PAGES = [['shop', 'shop.html', 'Shop'], ['machine', 'machine.html', 'The Machine'], ['story', 'story.html', 'Our Story'], ['schedule', 'schedule.html', 'Schedule'], ['sponsors', 'sponsors.html', 'Sponsors']];
  var MSGS = [
    'Testing season 2026: <a href="schedule.html">get Hook Alerts</a>',
    'Free US shipping on orders over $XX',
    'Printed to order · ships in 5 days'
  ];

  var h = document.querySelector('[data-hm-header]');
  if (h) {
    var cur = h.getAttribute('data-current') || '';
    var nav = PAGES.map(function (p) {
      return '<a href="' + p[1] + '"' + (p[0] === cur ? ' aria-current="page"' : '') + (p[0] === 'shop' ? ' id="mega-trigger" aria-haspopup="true" aria-expanded="false" aria-controls="mega"' : '') + '>' + p[2] + '</a>';
    }).join('');
    h.outerHTML =
      '<a class="skip" href="#main">Skip to content</a>' +
      '<div class="draftbar"><span>Boceto v3 · no es el sitio en vivo</span><a href="index.html">Home</a><a href="shop.html">Shop</a><a href="product.html">Producto</a><a href="ride.html">Ride</a><a href="machine.html">Machine</a><a href="story.html">Story</a><a href="schedule.html">Schedule</a><a href="sponsors.html">Sponsors</a><a href="account.html">Account</a><a href="policies.html">Policies</a><a href="contact.html">Contact</a><a href="404.html">404</a></div>' +
      '<div class="announce" role="region" aria-label="Announcements"><p class="announce__msg" id="ann" aria-live="off">' + MSGS[0] + '</p><button class="announce__pause" type="button" id="ann-pause" aria-label="Pause announcements">' + I.pause + '</button></div>' +
      '<header class="hdr" id="hdr"><div class="wrap hdr__in">' +
        '<button class="icon-btn menu-btn" type="button" id="menu-open" aria-label="Open menu">' + I.menu + '</button>' +
        '<a class="hdr__logo" href="index.html"><img src="img/logo-ink.svg" alt="Heavy Metal home" width="138" height="20"></a>' +
        '<nav class="hdr__nav" aria-label="Main">' + nav + '</nav>' +
        '<div class="hdr__icons">' +
          '<button class="icon-btn" type="button" id="search-open" aria-label="Search">' + I.search + '</button>' +
          '<a class="icon-btn" href="account.html" aria-label="Account">' + I.user + '</a>' +
          '<button class="icon-btn" type="button" id="cart-open" aria-label="Cart, 0 items">' + I.bag + '<span class="cart-count" id="cart-count" data-n="0">0</span></button>' +
        '</div>' +
      '</div>' +
      '<div class="mega" id="mega" hidden><div class="wrap mega__in">' +
        '<ul class="mega__big"><li><a href="shop.html?cat=all">Shop all</a></li><li><a href="shop.html?cat=new">New drop</a></li><li><a href="shop.html?cat=all&amp;sort=best">Best sellers</a></li><li><a href="shop.html?cat=bundles">Bundles</a></li><li><a href="ride.html">Ride with the Evil One</a></li></ul>' +
        '<div><p class="label">Category</p><ul class="mega__small"><li><a href="shop.html?cat=tees">Tees</a></li><li><a href="shop.html?cat=sweats">Sweatshirts</a></li><li><a href="shop.html?cat=hats">Hats</a></li><li><a href="shop.html?cat=kids">Kids</a></li><li><a href="shop.html?cat=gear">Stickers &amp; gear</a></li></ul></div>' +
        '<div class="mega__thumbs">' + ['tees', 'sweats', 'hats', 'kids', 'gear', 'bundles'].map(function (k) { var c = CATS.filter(function (x) { return x[0] === k; })[0]; return '<a href="shop.html?cat=' + k + '">' + thumb(c[1]) + '<span>' + c[1] + '</span></a>'; }).join('') + '</div>' +
        '<a class="mega__card" href="shop.html?cat=new"><span class="thumb"><img class="photo" src="img/hm-front-smoke.webp" alt="" loading="lazy"></span><span><span class="label">The Evil One Drop</span><p style="margin-top:6px">New tees and hoodies, designed by the crew in Waterloo, WI.</p><span class="link" style="display:inline-block;margin-top:8px;text-decoration:underline">Shop the drop</span></span></a>' +
      '</div></div>' +
      '</header>' +
      '<div class="mnav" id="mnav" hidden role="dialog" aria-modal="true" aria-label="Menu">' +
        '<div class="mnav__top"><img src="img/logo-ink.svg" alt="Heavy Metal" height="18" style="height:18px;width:auto"><button class="icon-btn" type="button" id="menu-close" aria-label="Close menu">' + I.close + '</button></div>' +
        '<div class="mnav__thumbs">' + CATS.map(function (c) { return '<a href="shop.html?cat=' + c[0] + '">' + thumb(c[1], c[0] === 'ride') + '<span>' + c[1] + '</span></a>'; }).join('') + '</div>' +
        PAGES.map(function (p) { return '<a class="mnav__link" href="' + p[1] + '">' + p[2] + I.arrow + '</a>'; }).join('') +
        '<div class="mnav__sub"><a href="account.html">Account</a><a href="contact.html">Contact</a><a href="policies.html?p=shipping">Shipping &amp; returns</a><a href="https://www.facebook.com/heavymetalprostock/">Facebook</a></div>' +
      '</div>' +
      '<div class="scrim" id="scrim" hidden></div>' +
      '<div class="search" id="search" hidden role="dialog" aria-modal="true" aria-label="Search">' +
        '<div class="wrap"><form class="search__bar" action="search.html" role="search"><span aria-hidden="true">' + I.search + '</span><label class="vh" for="q">Search the store</label><input id="q" name="q" type="search" placeholder="Search tees, hoodies, the machine..." autocomplete="off"><button class="icon-btn" type="button" id="search-close" aria-label="Close search">' + I.close + '</button></form>' +
        '<div class="search__body"><div><p class="label muted">Popular</p><ul><li><a href="search.html?q=hoodie">hoodie</a></li><li><a href="search.html?q=evil%20one">evil one</a></li><li><a href="search.html?q=kids">kids</a></li><li><a href="ride.html">name on the tractor</a></li></ul><p class="label muted" style="margin-top:20px">Pages</p><ul id="search-pages"><li><a href="machine.html">The Machine</a></li><li><a href="schedule.html">Schedule</a></li><li><a href="sponsors.html">Sponsors</a></li><li><a href="policies.html?p=shipping">Shipping &amp; returns</a></li></ul></div>' +
        '<div><p class="label muted" id="search-h">Best sellers</p><div class="search__res" id="search-res" style="margin-top:12px"></div><p id="search-all" style="margin:16px 0 0" hidden><a class="link" href="search.html">See all results</a></p></div></div></div>' +
      '</div>' +
      '<aside class="drawer" id="drawer" role="dialog" aria-modal="true" aria-labelledby="drawer-t" hidden>' +
        '<div class="drawer__head"><p class="h3" id="drawer-t">Cart (<span id="drawer-count">0</span>)</p><button class="icon-btn" type="button" id="cart-close" aria-label="Close cart">' + I.close + '</button></div>' +
        '<div class="drawer__body">' +
          '<div id="ship-bar" hidden style="display:grid;gap:6px"><p style="margin:0;font-size:var(--t-xs)"><b>$XX</b> away from free US shipping</p><div class="meter" style="--fill:45%"><span></span></div></div>' +
          '<div id="cart-empty" style="display:grid;gap:12px"><p style="margin:0">Your cart is empty.</p><div class="btn-row"><a class="btn" href="shop.html?cat=new">Shop the drop</a><a class="btn btn--ghost" href="shop.html?cat=all">Shop all</a></div></div>' +
          '<ul id="lines" style="list-style:none;margin:0;padding:0;display:grid;gap:14px"></ul>' +
          '<a class="promo" href="product.html?p=crew-pack" style="text-decoration:none"><span class="ph" style="--ar:1/1"></span><span><b class="label">Crew Pack</b><br>Tee plus cap. Save $X.</span><span class="link" style="text-decoration:underline">View</span></a>' +
          '<div><p class="label" style="margin-bottom:8px">Complete the look</p><div class="recs"><a href="product.html?p=crew-cap"><span class="ph" style="--ar:1/1"></span>Crew Cap · $XX</a><a href="product.html?p=sticker-pack"><span class="ph" style="--ar:1/1"></span>Sticker Pack · $XX</a></div></div>' +
          '<a class="promo" href="ride.html" style="text-decoration:none;background:var(--night);color:var(--night-ink)"><img src="img/hm-front-smoke.webp" alt="" style="width:56px;height:56px;object-fit:cover"><span><b class="label" style="color:var(--accent)">Ride With The Evil One</b><br>Put your name on the tractor.</span><span class="link" style="text-decoration:underline">Add</span></a>' +
        '</div>' +
        '<div class="drawer__foot"><p style="display:flex;justify-content:space-between;margin:0;font-weight:700;font-size:var(--t-sm)"><span>Subtotal</span><span class="num">$XX</span></p><p class="small muted" style="margin:0">Taxes and shipping at checkout. Printed to order, ships in 5 days.</p><a class="btn btn--block" href="#" id="checkout">Checkout</a><p class="small muted" style="margin:0;text-align:center">Shop Pay · Apple Pay · Google Pay · Cards</p></div>' +
      '</aside>' +
      '<div class="qsheet" id="qsheet" hidden role="dialog" aria-modal="true" aria-labelledby="qs-name"><div style="display:flex;justify-content:space-between;align-items:start;gap:12px"><div><p class="h3" id="qs-name"></p><p class="small muted" style="margin:2px 0 0">$XX · <span id="qs-color"></span></p></div><button class="icon-btn" type="button" id="qs-close" aria-label="Close">' + I.close + '</button></div><p class="label">Select a size</p><div class="qsheet__sizes" id="qs-sizes"></div><a class="link" id="qs-more" href="#" style="text-decoration:underline">View full details</a></div>';
  }

  var f = document.querySelector('[data-hm-footer]');
  if (f) {
    function acc(title, links) {
      return '<details class="ftr__acc" open><summary><h2 class="ftr__h">' + title + '</h2></summary><ul class="ftr__list">' +
        links.map(function (l) { return '<li><a href="' + l[1] + '">' + l[0] + '</a></li>'; }).join('') + '</ul></details>';
    }
    f.outerHTML =
      '<footer class="ftr"><div class="wrap">' +
        '<div class="ftr__cols">' +
          acc('Help', [['Contact us', 'contact.html'], ['Shipping', 'policies.html?p=shipping'], ['Returns &amp; exchanges', 'policies.html?p=refund'], ['Size guide', 'product.html#size-guide'], ['Track my order', 'account.html'], ['FAQ', 'contact.html#faq']]) +
          '<div class="ftr__news"><h2 class="ftr__h">Hook Alerts</h2><p style="margin:0" class="muted">New drops and a heads up before every pull. One list, no spam.</p>' +
            '<form class="ftr__form" id="ftr-form" novalidate><label class="vh" for="ftr-email">Email</label><input class="input" id="ftr-email" type="email" required placeholder="Email address" autocomplete="email"><button type="submit" aria-label="Sign up">' + I.arrow + '</button></form>' +
            '<p class="consent" id="ftr-msg">By signing up you agree to receive marketing emails. Unsubscribe anytime. See our <a href="policies.html?p=privacy">Privacy Policy</a>.</p></div>' +
          acc('The team', [['The Machine', 'machine.html'], ['Our Story', 'story.html'], ['Schedule', 'schedule.html'], ['Sponsors', 'sponsors.html'], ['Ride With The Evil One', 'ride.html']]) +
        '</div>' +
        '<div class="ftr__social"><a href="https://www.facebook.com/heavymetalprostock/" aria-label="Facebook">' + I.fb + '</a><a href="#" aria-label="Instagram (pending)">' + I.ig + '</a><a href="#" aria-label="TikTok (pending)">' + I.tt + '</a><a href="https://www.youtube.com/watch?v=HfJ5FAJJ5Ac" aria-label="YouTube">' + I.yt + '</a></div>' +
        '<p class="ftr__biz">© 2026 Heavy Metal Pro Stock: The Evil One · Waterloo, WI</p>' +
        '<nav class="ftr__legal" aria-label="Legal"><a href="policies.html?p=privacy">Privacy Policy</a><a href="policies.html?p=terms">Terms of Service</a><a href="policies.html?p=refund">Refund Policy</a><a href="policies.html?p=shipping">Shipping Policy</a><a href="policies.html?p=contact">Contact Information</a><a href="policies.html?p=accessibility">Accessibility</a><a href="policies.html?p=sms">SMS Terms</a><a href="policies.html?p=ride">Ride With Rules</a><a href="policies.html?p=choices">Your Privacy Choices</a><a href="#" id="cookie-prefs">Cookie Preferences</a></nav>' +
      '</div></footer>' +
      '<div class="cookie" id="cookie" role="region" aria-label="Cookie consent" hidden><p class="h3">We use cookies</p><p>We use cookies to run the store, remember your cart and, if you allow it, to measure ads. You can change this anytime in Cookie Preferences. <a href="policies.html?p=privacy">Privacy Policy</a> · <a href="policies.html?p=choices">Your Privacy Choices</a></p><div class="btn-row"><button class="btn" type="button" data-cookie="accept">Accept</button><button class="btn btn--ghost" type="button" data-cookie="decline">Decline</button><button class="btn btn--ghost" type="button" data-cookie="manage">Manage</button></div></div>';
  }

  var $ = function (id) { return document.getElementById(id); };
  var count = 0, last = null;

  /* anuncio rotativo con pausa */
  var ann = $('ann');
  if (ann) {
    var ai = 0, playing = !matchMedia('(prefers-reduced-motion: reduce)').matches;
    var timer = setInterval(function () { if (!playing) return; ai = (ai + 1) % MSGS.length; ann.innerHTML = MSGS[ai]; }, 4000);
    var pb = $('ann-pause');
    if (!playing) { pb.innerHTML = I.play; pb.setAttribute('aria-label', 'Play announcements'); }
    pb.addEventListener('click', function () {
      playing = !playing; pb.innerHTML = playing ? I.pause : I.play;
      pb.setAttribute('aria-label', playing ? 'Pause announcements' : 'Play announcements');
    });
  }

  /* overlays: uno a la vez */
  var scrim = $('scrim');
  var open = null;
  function show(el, focus) { hideAll(); last = document.activeElement; el.hidden = false; if (scrim) scrim.hidden = false; document.body.style.overflow = 'hidden'; open = el; if (focus) focus.focus(); }
  function hideAll() { ['mnav', 'search', 'drawer', 'qsheet'].forEach(function (id) { var e = $(id); if (e) e.hidden = true; }); if (scrim) scrim.hidden = true; document.body.style.overflow = ''; if (open && last && last.focus) last.focus(); open = null; }
  if (scrim) scrim.addEventListener('click', hideAll);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { hideAll(); closeMega(); } });

  /* mega menú: clic, foco o hover (funciona en tablet) */
  var trig = $('mega-trigger'), mega = $('mega'), hdr = $('hdr'), mt;
  function openMega() { clearTimeout(mt); mega.hidden = false; trig.setAttribute('aria-expanded', 'true'); }
  function closeMega() { if (!mega) return; mega.hidden = true; trig && trig.setAttribute('aria-expanded', 'false'); }
  if (trig && mega) {
    trig.addEventListener('mouseenter', openMega);
    trig.addEventListener('click', function (e) { if (mega.hidden) { e.preventDefault(); openMega(); } });
    hdr.addEventListener('mouseleave', function () { mt = setTimeout(closeMega, 150); });
    mega.addEventListener('mouseenter', openMega);
    mega.addEventListener('focusout', function (e) { if (!mega.contains(e.relatedTarget) && e.relatedTarget !== trig) closeMega(); });
  }

  /* menú móvil */
  if ($('menu-open')) {
    $('menu-open').addEventListener('click', function () { show($('mnav'), $('menu-close')); });
    $('menu-close').addEventListener('click', hideAll);
  }

  /* búsqueda predictiva sobre el catálogo */
  function renderSearch(q) {
    q = (q || '').trim().toLowerCase();
    var list = q ? CAT.filter(function (p) { return (p.name + ' ' + p.sub + ' ' + p.cat).toLowerCase().indexOf(q) > -1; }) : CAT.filter(function (p) { return p.tag === 'best'; });
    $('search-h').textContent = q ? (list.length ? list.length + ' products for "' + q + '"' : 'No products for "' + q + '"') : 'Best sellers';
    $('search-res').innerHTML = list.slice(0, 4).map(window.hmCard).join('') || '<p class="muted" style="grid-column:1/-1;margin:0">Try "tee", "hoodie" or "kids". Or browse <a href="shop.html?cat=all">Shop all</a>.</p>';
    var all = $('search-all'); all.hidden = !q || !list.length; all.firstChild.href = 'search.html?q=' + encodeURIComponent(q);
  }
  if ($('search-open')) {
    $('search-open').addEventListener('click', function () { show($('search'), $('q')); renderSearch(''); });
    $('search-close').addEventListener('click', hideAll);
    $('q').addEventListener('input', function () { renderSearch(this.value); });
  }

  /* carrito */
  function setCount(n) {
    count = n;
    var c = $('cart-count'); if (!c) return;
    c.textContent = n; c.setAttribute('data-n', n); $('drawer-count').textContent = n;
    $('cart-open').setAttribute('aria-label', 'Cart, ' + n + ' items');
    $('cart-empty').hidden = n > 0; $('ship-bar').hidden = n === 0;
  }
  function openCart() { show($('drawer'), $('cart-close')); }
  if ($('cart-open')) {
    $('cart-open').addEventListener('click', openCart);
    $('cart-close').addEventListener('click', hideAll);
    $('checkout').addEventListener('click', function (e) { e.preventDefault(); this.textContent = 'Boceto: aquí abre el checkout de Shopify'; });
    setCount(0);
  }
  window.hmAdd = function (name, variant, price) {
    var li = document.createElement('li'); li.className = 'line';
    li.innerHTML = '<span class="ph" style="--ar:4/5"></span><div><p style="margin:0;font-weight:700;text-transform:uppercase;letter-spacing:.04em">' + name + '</p><p style="margin:2px 0 0;color:var(--mute)">' + (variant || '') + '</p></div><p class="num" style="margin:0">' + (price || '$XX') + '</p>';
    $('lines').appendChild(li); setCount(count + 1); openCart();
  };

  /* selector rápido de talla: Add to cart en tarjetas nunca elige talla por el cliente */
  var qp = null;
  function quick(id) {
    var p = CAT.filter(function (x) { return x.id === id; })[0]; if (!p) return;
    var color = p.colors[0] || '';
    if (!p.sizes.length) { window.hmAdd(p.name, color || 'One size', '$XX'); return; }
    qp = p; $('qs-name').textContent = p.name; $('qs-color').textContent = color || 'One color';
    $('qs-more').href = href(p);
    $('qs-sizes').innerHTML = p.sizes.map(function (s) { var out = (p.sold || []).indexOf(s) > -1; return '<button type="button" data-size="' + s + '"' + (out ? ' disabled aria-label="' + s + ', sold out"' : '') + '>' + s + '</button>'; }).join('');
    show($('qsheet'), $('qs-sizes').querySelector('button:not(:disabled)'));
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-quick]'); if (b) { e.preventDefault(); quick(b.getAttribute('data-quick')); return; }
    var s = e.target.closest('[data-size]'); if (s && qp) { var p = qp; hideAll(); window.hmAdd(p.name, (p.colors[0] ? p.colors[0] + ' / ' : '') + s.getAttribute('data-size'), '$XX'); qp = null; }
  });
  if ($('qs-close')) $('qs-close').addEventListener('click', hideAll);

  /* footer: una sola lista (Hook Alerts) */
  var ff = $('ftr-form');
  if (ff) ff.addEventListener('submit', function (e) {
    e.preventDefault(); var em = $('ftr-email');
    if (!em.value || !em.checkValidity()) { $('ftr-msg').textContent = 'Enter a valid email to join Hook Alerts.'; em.focus(); return; }
    $('ftr-msg').textContent = "You're on the list. Check your inbox to confirm.";
  });

  /* banner de cookies: se muestra una vez por visita del boceto */
  var ck = $('cookie');
  if (ck) {
    var seen = false; try { seen = sessionStorage.getItem('hm-cookie') === '1'; } catch (e) {}
    ck.hidden = seen;
    ck.addEventListener('click', function (e) {
      var b = e.target.closest('[data-cookie]'); if (!b) return;
      if (b.getAttribute('data-cookie') === 'manage') { location.href = 'policies.html?p=choices'; return; }
      ck.hidden = true; try { sessionStorage.setItem('hm-cookie', '1'); } catch (err) {}
    });
    $('cookie-prefs').addEventListener('click', function (e) { e.preventDefault(); ck.hidden = false; });
  }
})();
