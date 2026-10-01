/* Heavy Metal boceto v6: header, mega menú, menú móvil, búsqueda, selector de talla, carrito,
   footer, banner de cookies. Cada página pone:
   <div data-hm-header data-current="home|shop|machine|story|schedule|sponsors|account|policies|contact"></div>
   <div data-hm-footer></div>  y carga <script src="hm.js"></script> al final del body. */
(function () {
  /* cada página abre arriba (en el visor el scroll se conservaba entre páginas) */
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
  function toTop() { if (!location.hash) { window.scrollTo(0, 0); document.documentElement.scrollTop = 0; document.body && (document.body.scrollTop = 0); } }
  toTop(); window.addEventListener('DOMContentLoaded', toTop); window.addEventListener('load', function () { toTop(); setTimeout(toTop, 50); });
  window.addEventListener('pageshow', toTop);

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
    /* status: 'live' (default) | 'soon' (Coming soon) | 'soldout'. left: unidades; 5 o menos = "Almost gone!" */
    { id: 'evil-one-tee', name: 'Evil One Tee', sub: 'Front logo tee', cat: 'tees', colors: ['Matte Black', 'Smoke Gray'], sizes: TEE, sold: ['3XL'], tag: 'best', left: 4 },
    { id: 'lightning-strike-tee', name: 'Lightning Strike Tee', sub: 'First fire graphic', cat: 'tees', colors: ['Matte Black'], sizes: TEE, tag: 'new' },
    { id: 'full-pull-ls', name: 'Full Pull or Nothing Long Sleeve', sub: 'Back print', cat: 'tees', colors: ['Matte Black', 'Bone'], sizes: TEE, status: 'soldout' },
    { id: 'cat-v8-spec-tee', name: 'Cat V8 Spec Tee', sub: 'Spec sheet print', cat: 'tees', colors: ['Smoke Gray'], sizes: TEE },
    { id: '680-ci-hoodie', name: '680 CI Hoodie', sub: 'Pullover hoodie', cat: 'sweats', colors: ['Matte Black', 'Smoke Gray'], sizes: TEE, tag: 'best' },
    { id: 'evil-one-crewneck', name: '“The Evil One” Crewneck', sub: 'Crewneck sweatshirt', cat: 'sweats', colors: ['Bone'], sizes: TEE, tag: 'new' },
    { id: 'crew-cap', name: 'Crew Cap', sub: 'Structured cap', cat: 'hats', colors: ['Black'], sizes: [], tag: 'best' },
    { id: 'evil-one-beanie', name: 'Evil One Beanie', sub: 'Cuffed knit', cat: 'hats', colors: ['Black', 'Safety Yellow'], sizes: [], tag: 'new', status: 'soon' },
    { id: 'little-evil-one-tee', name: 'Little Evil One Kids Tee', sub: 'Youth sizes', cat: 'kids', colors: ['Matte Black'], sizes: ['YS', 'YM', 'YL', 'YXL'] },
    { id: 'kids-hoodie', name: 'Kids Hoodie', sub: 'Youth pullover', cat: 'kids', colors: ['Smoke Gray'], sizes: ['YS', 'YM', 'YL', 'YXL'] },
    { id: 'sticker-pack', name: 'Sticker Pack', sub: 'Die cut set', cat: 'gear', colors: [], sizes: [] },
    { id: 'hook-alert-koozie', name: 'Full Pull Koozie', sub: 'Keep it cold', cat: 'gear', colors: [], sizes: [] },
    { id: 'crew-pack', name: 'Crew Pack Bundle', sub: 'Tee plus cap', cat: 'bundles', colors: [], sizes: TEE, tag: 'bundle' },
    { id: 'lightning-night-tee', name: 'Lightning Night Tee', sub: 'Special edition', cat: 'limited', colors: ['Matte Black'], sizes: TEE, tag: 'limited', status: 'soon', page: 'limited.html' }
  ];
  /* boceto: ?empty=1 simula la tienda sin merch (estado "Coming soon") */
  if (/[?&]empty=1/.test(location.search)) { CAT.length = 0; }
  CAT.forEach(function (p) { p.status = p.status || 'live'; });
  var CATS = [
    ['all', 'Shop all'], ['new', 'New drop'], ['tees', 'Tees'], ['sweats', 'Sweatshirts'], ['hats', 'Hats'],
    ['kids', 'Kids'], ['gear', 'Stickers & gear'], ['bundles', 'Bundles'], ['limited', 'Special edition']
  ];
  var SW = { 'Matte Black': 'var(--ink)', 'Black': 'var(--ink)', 'Smoke Gray': '#8C8A82', 'Bone': '#E9E6DC', 'Safety Yellow': 'var(--accent)' };
  window.HM_SW = SW;
  function href(p) { return p.page || 'product.html?p=' + p.id; }
  function catHref(k) { return k === 'limited' ? 'limited.html' : 'shop.html?cat=' + k; }
  /* temporada: en Shopify es un ajuste global del tema (Personalizar > Ajustes del tema > Temporada) */
  /* last-updated: season */
  var SEASON = window.HM_SEASON = 2026;
  /* mockups planos de prenda mientras no hay fotos de producto (en Shopify: la foto real de Printify) */
  var SHAPE = {
    tee: 'M34 18 18 26l-10 18 14 6 6-10v52h44V40l6 10 14-6-10-18-16-8c-2 6-8 10-16 10s-14-4-16-10Z',
    hood: 'M40 22c0-6 4-10 10-10s10 4 10 10l18 6 12 40-12 4-8-22v46H30V50l-8 22-12-4 12-40Z',
    cap: 'M20 62c0-20 13-34 30-34s30 14 30 34Zm-4 2h70c4 0 6 6 2 8-10 4-30 4-44 2H16c-4 0-4-10 0-10Z',
    beanie: 'M24 70c0-26 11-44 26-44s26 18 26 44Zm-4 2h60v12H20Z M46 20a4 4 0 1 0 8 0 4 4 0 0 0-8 0Z',
    sticker: 'M50 12 61 36l26 3-19 18 5 26-23-13-23 13 5-26-19-18 26-3Z',
    koozie: 'M30 26h40v56c0 4-4 6-20 6s-20-2-20-6Z'
  };
  function shapeFor(p) { return p.cat === 'sweats' || p.id === 'kids-hoodie' ? 'hood' : p.cat === 'hats' ? (p.id === 'evil-one-beanie' ? 'beanie' : 'cap') : p.id === 'sticker-pack' ? 'sticker' : p.id === 'hook-alert-koozie' ? 'koozie' : 'tee'; }
  function mock(p, size, view, colorName) {
    var col = colorName || p.colors[0] || 'Matte Black', fill = SW[col] || 'var(--ink)', light = col === 'Bone' || col === 'Safety Yellow';
    var k = shapeFor(p), small = p.cat === 'kids' ? ' transform="translate(50 54) scale(.82) translate(-50 -54)"' : '';
    var extra = p.cat === 'bundles' ? '<path d="' + SHAPE.cap + '" transform="translate(52 52) scale(.42)" fill="' + fill + '" stroke="var(--tile)" stroke-width="3"/>' : '';
    /* ícono genérico, sin logo ni texto: sirve de placeholder en la tienda (img/icons/) */
    /* estampado: el nombre en registro "HEAVY METAL PRO STOCK" / "“THE EVIL ONE”" (nunca "Heavy Metal" solo) */
    /* frente: el logo HEAVY METAL al tamaño del primer diseño y abajo PRO STOCK / “THE EVIL ONE” chico */
    var ink = light ? '#1C1B19' : '#ECEAE5', lg = 'img/' + (light ? 'logo-ink' : 'logo-bone') + '.svg', y0 = k === 'hood' ? 40 : 38;
    var txt = function (y, fs, t, ls) { return '<text x="50" y="' + y + '" font-size="' + fs + '"' + (ls ? ' letter-spacing="' + ls + '"' : '') + '>' + t + '</text>'; };
    var logo = (k === 'tee' || k === 'hood') ? (view === 'back' ?
      '<image href="' + lg + '" x="29" y="' + (y0 + 2) + '" width="42" height="6.1"/><g fill="' + ink + '" font-family="Archivo,Arial,sans-serif" font-weight="800" text-anchor="middle">' + txt(y0 + 13, 3.4, 'PRO STOCK', '.4') + txt(y0 + 20, 4.4, '“THE EVIL ONE”') + '</g>' :
      '<image href="' + lg + '" x="36" y="' + y0 + '" width="28" height="4.1"/><g fill="' + ink + '" font-family="Archivo,Arial,sans-serif" font-weight="800" text-anchor="middle">' + txt(y0 + 7.2, 2.4, 'PRO STOCK', '.3') + txt(y0 + 10.4, 2.3, '“THE EVIL ONE”') + '</g>') : '';
    /* sudadera: abertura del capuchón y bolsa canguro */
    if (k === 'hood') logo = '<path d="M43 22c2 4 4 6 7 6s5-2 7-6" fill="none" stroke="' + ink + '" stroke-width=".9" opacity=".5"/><path d="M38 76h24l-3 10H41Z" fill="none" stroke="' + ink + '" stroke-width=".9" opacity=".45"/>' + logo;
    var edge = light ? ' stroke="#9E9B94" stroke-width=".8"' : '';
    return '<svg class="mock" viewBox="0 0 100 100" aria-hidden="true"' + (size ? ' style="width:' + size + '"' : '') + '><g' + small + '><path d="' + SHAPE[k] + '" fill="' + fill + '"' + edge + '/>' + logo + '</g>' + extra + '</svg>';
  }
  window.hmMock = mock;
  var CAT_MOCK = { all: 'evil-one-tee', 'new': 'lightning-strike-tee', tees: 'cat-v8-spec-tee', sweats: '680-ci-hoodie', hats: 'crew-cap', kids: 'little-evil-one-tee', gear: 'sticker-pack', bundles: 'crew-pack', limited: 'lightning-night-tee' };
  function thumb(label, key) {
    var p = CAT.filter(function (x) { return x.id === CAT_MOCK[key]; })[0];
    return '<span class="thumb thumb--mock">' + (p ? mock(p) : '') + (key === 'new' ? '<span class="thumb__new">New</span>' : key === 'limited' ? '<span class="thumb__new thumb__new--ink">Ltd</span>' : '') + '</span>';
  }

  /* tarjeta reutilizable: window.hmCard(producto) */
  window.hmCard = function (p) {
    var badge = p.tag === 'best' ? '<span class="badge">Best seller</span>' : p.tag === 'new' ? '<span class="badge badge--ink">New</span>' :
      p.tag === 'bundle' ? '<span class="badge badge--line">Save $X</span>' : p.tag === 'limited' ? '<span class="badge badge--ink">Special edition</span>' : '';
    var sw = p.colors.map(function (c) { return '<span class="swatch" style="--sw:' + SW[c] + '" title="' + c + '"></span>'; }).join('');
    /* el estado se suma a "Special edition" (no lo reemplaza) */
    var keep = p.tag === 'limited' ? badge : '';
    if (p.status === 'soon') badge = keep + '<span class="badge badge--line">Coming soon</span>';
    else if (p.status === 'soldout') badge = keep + '<span class="badge badge--line">Sold out</span>';
    else if (p.left && p.left <= 5) badge = '<span class="badge badge--alert">Almost gone!</span>' + badge;
    var btn = p.status === 'soon' ? '<a class="btn card__add" href="' + href(p) + '#notify">Notify me<span class="vh"> when ' + p.name + ' drops</span></a>' :
      p.status === 'soldout' ? '<a class="btn card__add" href="' + href(p) + '#notify">Sold out · Notify me<span class="vh"> about ' + p.name + '</span></a>' :
      '<button class="btn card__add" type="button" data-quick="' + p.id + '">Add to cart · $XX<span class="vh"> ' + p.name + '</span></button>';
    /* vistas de la tarjeta: frente, espalda y otro color (en Shopify: las fotos del producto) */
    var views = [mock(p)];
    if (p.cat === 'tees' || p.cat === 'sweats' || p.cat === 'kids' || p.cat === 'limited') views.push(mock(p, '', 'back'));
    if (p.colors[1]) views.push(mock(p, '', '', p.colors[1]));
    var slides = views.map(function (v, i) { return '<span class="ph ph--mock card__slide"' + (i ? ' hidden' : '') + '>' + v + '</span>'; }).join('');
    var arrows = views.length > 1 ? '<button type="button" class="card__arw card__arw--prev" data-arw="-1" aria-label="Previous image of ' + p.name + '">‹</button><button type="button" class="card__arw card__arw--next" data-arw="1" aria-label="Next image of ' + p.name + '">›</button><span class="card__dots" aria-hidden="true">' + views.map(function (v, i) { return '<i' + (i ? '' : ' class="on"') + '></i>'; }).join('') + '</span>' : '';
    return '<article class="card' + (p.status !== 'live' ? ' card--' + p.status : '') + '" data-status="' + p.status + '" data-cat="' + p.cat + '" data-tag="' + (p.tag || '') + '" data-colors="' + p.colors.join('|') + '" data-sizes="' + p.sizes.join('|') + '">' +
      '<div class="card__media"><a href="' + href(p) + '" tabindex="-1" aria-hidden="true">' + slides + '</a>' + arrows +
      (badge ? '<div class="card__badges">' + badge + '</div>' : '') + btn + '</div>' +
      '<div class="card__txt"><h3 class="card__name"><a href="' + href(p) + '">' + p.name + '</a></h3><p class="card__sub">' + p.sub + '</p>' +
      '<div class="card__meta"><span class="num">$XX</span><span class="swatches">' + sw + '</span></div></div></article>';
  };
  /* tienda vacía: window.hmComingSoon() (en Shopify sale solo cuando la colección no tiene productos activos) */
  window.hmComingSoon = function () {
    return '<div class="soon"><span class="soon__bolt" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M13 2 4 14h7l-1 8 9-12h-7z"/></svg></span><p class="label">Merch</p><p class="h2">Coming soon</p><p class="muted">The first drop from the crew behind “The Evil One” is on its way. Get a heads up when it lands.</p>' +
      '<form class="soon__form" data-soon><label class="vh" for="soon-email">Email</label><input class="input" id="soon-email" type="email" required placeholder="Email address" autocomplete="email"><button class="btn" type="submit">Notify me</button></form></div>';
  };
  document.addEventListener('submit', function (e) {
    var f = e.target.closest('[data-soon]'); if (!f) return; e.preventDefault();
    if (!f.querySelector('input').checkValidity()) { f.querySelector('input').focus(); return; }
    f.outerHTML = '<p role="status" style="margin:0"><b>You are on the list.</b> We will email you when the drop goes live.</p>';
  });
  /* flechas en las tarjetas */
  document.addEventListener('click', function (e) {
    var a = e.target.closest('[data-arw]'); if (!a) return;
    e.preventDefault();
    var card = a.closest('.card'), sl = card.querySelectorAll('.card__slide'), dots = card.querySelectorAll('.card__dots i'), cur = 0;
    sl.forEach(function (x, i) { if (!x.hidden) cur = i; });
    var n = (cur + +a.getAttribute('data-arw') + sl.length) % sl.length;
    sl.forEach(function (x, i) { x.hidden = i !== n; }); dots.forEach(function (d, i) { d.className = i === n ? 'on' : ''; });
  });
  /* fotitos de categoría: window.hmCats(actual) */
  window.hmCats = function (cur) {
    return '<ul class="cats" aria-label="Shop by category">' + CATS.map(function (c) {
      return '<li><a class="cat" href="shop.html?cat=' + c[0] + '"' + (c[0] === cur ? ' aria-current="true"' : '') + '>' + thumb(c[1], c[0]) + '<span>' + c[1] + '</span></a></li>';
    }).join('') + '</ul>';
  };

  var PAGES = [['shop', 'shop.html', 'Shop'], ['machine', 'machine.html', 'The Machine'], ['story', 'story.html', 'Our Story'], ['schedule', 'schedule.html', 'Schedule'], ['log', 'log.html', 'Pit Log'], ['gallery', 'gallery.html', 'Gallery'], ['sponsors', 'sponsors.html', 'Sponsors']];
  /* last-updated: announcements (Personalizar > Encabezado > Barra de anuncios) */
  var MSGS = [
    'Testing season ' + SEASON + ': <a href="schedule.html">join The Evil List</a>',
    'Free US shipping on orders over $XX',
    'Printed to order · ships in 5 days'
  ];

  function byId(id) { return CAT.filter(function (x) { return x.id === id; })[0]; }
  /* "Add to your order": solo productos que existen y están a la venta */
  var ADDONS = ['sticker-pack', 'hook-alert-koozie', 'crew-cap', 'kids-hoodie'].map(byId).filter(function (p) { return p && p.status === 'live'; });
  var h = document.querySelector('[data-hm-header]');
  if (h) {
    var cur = h.getAttribute('data-current') || '';
    var nav = PAGES.map(function (p) {
      return '<a href="' + p[1] + '"' + (p[0] === cur ? ' aria-current="page"' : '') + (p[0] === 'shop' ? ' id="mega-trigger" aria-haspopup="true" aria-expanded="false" aria-controls="mega"' : '') + '>' + p[2] + '</a>';
    }).join('');
    h.outerHTML =
      '<a class="skip" href="#main">Skip to content</a>' +
      '<div class="draftbar"><span>Boceto v8 · no es el sitio en vivo</span><a href="editar.html">Cómo editas todo</a><a href="index.html">Home</a><a href="shop.html">Shop</a><a href="product.html">Producto</a><a href="limited.html">Edición especial</a><a href="log.html">Pit Log</a><a href="gallery.html">Galería</a><a href="book.html">Book us</a><a href="machine.html">Machine</a><a href="story.html">Story</a><a href="schedule.html">Schedule</a><a href="sponsors.html">Sponsors</a><a href="faq.html">FAQ</a><a href="sizes.html">Sizes</a><a href="account.html">Account</a><a href="policies.html">Policies</a><a href="contact.html">Contact</a><a href="404.html">404</a><button type="button" id="notes-toggle" aria-pressed="false">Ocultar notas</button></div>' +
      '<div class="announce" role="region" aria-label="Announcements"><p class="announce__msg" id="ann" aria-live="off">' + MSGS[0] + '</p><button class="announce__pause" type="button" id="ann-pause" aria-label="Pause announcements">' + I.pause + '</button></div>' +
      '<header class="hdr" id="hdr"><div class="wrap hdr__in">' +
        '<button class="icon-btn menu-btn" type="button" id="menu-open" aria-label="Open menu">' + I.menu + '</button>' +
        '<a class="hdr__logo" href="index.html"><img src="img/logo-ink.svg" alt="Heavy Metal Pro Stock home" width="138" height="20"></a>' +
        '<nav class="hdr__nav" aria-label="Main">' + nav + '</nav>' +
        '<div class="hdr__icons">' +
          '<button class="icon-btn" type="button" id="search-open" aria-label="Search">' + I.search + '</button>' +
          '<a class="icon-btn" href="account.html" aria-label="Account">' + I.user + '</a>' +
          '<button class="icon-btn" type="button" id="cart-open" aria-label="Cart, 0 items">' + I.bag + '<span class="cart-count" id="cart-count" data-n="0">0</span></button>' +
        '</div>' +
      '</div>' +
      '<div class="mega" id="mega" hidden><div class="wrap mega__in">' +
        '<ul class="mega__big"><li><a href="shop.html?cat=all">Shop all</a></li><li><a href="shop.html?cat=new">New drop</a></li><li><a href="shop.html?cat=all&amp;sort=best">Best sellers</a></li><li><a href="shop.html?cat=bundles">Bundles</a></li><li><a href="limited.html">Special edition</a></li></ul>' +
        '<div><p class="label">Category</p><ul class="mega__small"><li><a href="shop.html?cat=tees">Tees</a></li><li><a href="shop.html?cat=sweats">Sweatshirts</a></li><li><a href="shop.html?cat=hats">Hats</a></li><li><a href="shop.html?cat=kids">Kids</a></li><li><a href="shop.html?cat=gear">Stickers &amp; gear</a></li></ul></div>' +
        '<div class="mega__thumbs">' + ['tees', 'sweats', 'hats', 'kids', 'gear', 'bundles'].map(function (k) { var c = CATS.filter(function (x) { return x[0] === k; })[0]; return '<a href="shop.html?cat=' + k + '">' + thumb(c[1], k) + '<span>' + c[1] + '</span></a>'; }).join('') + '</div>' +
        '<a class="mega__card" href="shop.html?cat=new"><span class="thumb"><img class="photo" src="img/hm-front-smoke.webp" alt="" loading="lazy"></span><span><span class="label">“The Evil One” Drop</span><p style="margin-top:6px">New tees and hoodies, designed by the crew in Waterloo, WI.</p><span class="link" style="display:inline-block;margin-top:8px;text-decoration:underline">Shop the drop</span></span></a>' +
      '</div></div>' +
      '</header>' +
      '<div class="mnav" id="mnav" hidden role="dialog" aria-modal="true" aria-label="Menu">' +
        '<div class="mnav__top"><img src="img/logo-ink.svg" alt="Heavy Metal Pro Stock" height="18" style="height:18px;width:auto"><button class="icon-btn" type="button" id="menu-close" aria-label="Close menu">' + I.close + '</button></div>' +
        '<div class="mnav__thumbs">' + CATS.map(function (c) { return '<a href="' + catHref(c[0]) + '">' + thumb(c[1], c[0]) + '<span>' + c[1] + '</span></a>'; }).join('') + '</div>' +
        PAGES.map(function (p) { return '<a class="mnav__link" href="' + p[1] + '">' + p[2] + I.arrow + '</a>'; }).join('') +
        '<div class="mnav__sub"><a href="book.html">Book the team</a><a href="account.html">Account</a><a href="contact.html">Contact</a><a href="faq.html">FAQ</a><a href="policies.html?p=shipping">Shipping &amp; returns</a><a href="https://www.facebook.com/heavymetalprostock/" target="_blank" rel="noopener">Facebook ↗<span class="vh"> (opens in a new tab)</span></a></div>' +
      '</div>' +
      '<div class="scrim" id="scrim" hidden></div>' +
      '<div class="search" id="search" hidden role="dialog" aria-modal="true" aria-label="Search">' +
        '<div class="wrap"><form class="search__bar" action="search.html" role="search"><span aria-hidden="true">' + I.search + '</span><label class="vh" for="q">Search the store</label><input id="q" name="q" type="search" placeholder="Search tees, hoodies, the machine..." autocomplete="off"><button class="icon-btn" type="button" id="search-close" aria-label="Close search">' + I.close + '</button></form>' +
        '<div class="search__body"><div><div id="recent-wrap" hidden><p class="label muted">Your recent searches</p><ul id="recent"></ul></div><p class="label muted" id="sugg-h">Trending</p><ul id="sugg"></ul><p class="label muted" style="margin-top:20px">Pages</p><ul id="search-pages"><li><a href="machine.html">The Machine</a></li><li><a href="schedule.html">Schedule</a></li><li><a href="sponsors.html">Sponsors</a></li><li><a href="faq.html">FAQ</a></li></ul><p class="note">Ya no las escribes tú: "Trending" sale solo de los productos más vendidos, mientras escriben Shopify sugiere búsquedas automáticas (Predictive Search, en inglés) y "recent searches" se guarda en el navegador de cada cliente.</p></div>' +
        '<div><p class="label muted" id="search-h">Best sellers</p><div class="search__res" id="search-res" style="margin-top:12px"></div><p id="search-all" style="margin:16px 0 0" hidden><a class="link" href="search.html">See all results</a></p></div></div></div>' +
      '</div>' +
      '<aside class="drawer" id="drawer" role="dialog" aria-modal="true" aria-labelledby="drawer-t" hidden>' +
        '<div class="drawer__head"><p class="h3" id="drawer-t">Cart (<span id="drawer-count">0</span>)</p><button class="icon-btn" type="button" id="cart-close" aria-label="Close cart">' + I.close + '</button></div>' +
        '<div class="tiers" id="ship-bar" hidden><p class="tiers__msg" id="tiers-msg">You are <b>$XX</b> away from <b>free US shipping</b></p><div class="tiers__track"><span class="tiers__fill" id="tiers-fill"></span><span class="tiers__stop" style="left:60%"><i></i>Free shipping</span><span class="tiers__stop" style="left:100%"><i></i>Free sticker</span></div></div>' +
        '<div class="drawer__body">' +
          '<div id="cart-empty" class="cempty"><p style="margin:0">Your cart is empty.</p><div class="btn-row"><a class="btn" href="shop.html?cat=new">Shop the drop</a><a class="btn btn--ghost" href="shop.html?cat=all&amp;sort=best">Best sellers</a></div></div>' +
          '<ul id="lines" class="lines"></ul>' +
          (byId('crew-pack') && byId('crew-cap') ? '<div class="upgrade" id="upgrade" hidden><span class="thumb thumb--mock">' + mock(byId('crew-pack')) + '</span><span><b>Make it a Crew Pack</b><br><span class="muted">Add the Crew Cap and save $X.</span></span><button class="btn btn--ghost btn--sm" type="button" data-quick="crew-cap">Add · $XX</button></div>' : '<div id="upgrade" hidden></div>') +
          (ADDONS.length ? '<div class="addons"><p class="label">Add to your order</p><div class="addons__row">' +
            ADDONS.map(function (p) { return '<div class="addon"><a href="' + href(p) + '" class="thumb thumb--mock">' + mock(p) + '</a><a href="' + href(p) + '" class="addon__n">' + p.name + '</a><span class="num">$XX</span><button class="btn btn--ghost btn--sm" type="button" data-quick="' + p.id + '">+ Add</button></div>'; }).join('') +
          '</div></div>' : '') +
          '<details class="giftnote"><summary>Discount code</summary><form class="coupon" id="coupon-form"><label class="vh" for="coupon">Discount code</label><input class="input" id="coupon" autocomplete="off" placeholder="Enter code"><button class="btn btn--ghost btn--sm" type="submit">Apply</button></form><p class="small muted" id="coupon-msg" style="margin:6px 0 0"></p></details>' +
          '<details class="giftnote"><summary>Add a note or gift message</summary><label class="vh" for="cart-note">Order note</label><textarea class="input" id="cart-note" rows="3" maxlength="200" placeholder="Gift message, or a note for the crew"></textarea></details>' +
          '<p class="note">Carrito nativo del tema, sin apps de pago: barra de envío gratis con escalones (ajustes del tema), "Add to your order" con productos complementarios de Search &amp; Discovery, Crew Pack con Shopify Bundles y nota del pedido nativa. Si después quieres reglas automáticas (regalo al llegar a $XX, upsell después del pago), las apps de carrito más usadas son UpCart, Rebuy o AfterSell; cuestan de $15 a $99 al mes.</p>' +
        '</div>' +
        '<div class="drawer__foot"><p class="drawer__sub"><span>Subtotal</span><span class="num">$XX</span></p><p class="small muted" style="margin:0">Printed to order. Ships in 5 days. Taxes and shipping at checkout.</p><a class="btn btn--block" href="#" id="checkout">Checkout</a><div class="paybadges" aria-label="Payment methods"><span>Shop Pay</span><span>Apple Pay</span><span>Google Pay</span><span>PayPal</span><span>Visa</span><span>Mastercard</span></div><p class="small muted" style="margin:0;text-align:center">Secure checkout by Shopify</p></div>' +
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
          acc('Help', [['Contact us', 'contact.html'], ['Shipping', 'policies.html?p=shipping'], ['Returns &amp; exchanges', 'policies.html?p=refund'], ['Size guide', 'sizes.html'], ['Track my order', 'account.html'], ['FAQ', 'faq.html']]) +
          '<div class="ftr__news"><h2 class="ftr__h">The Evil List</h2><p style="margin:0" class="muted">New drops and a heads up before every pull. One list, no spam.</p>' +
            '<form class="ftr__form" id="ftr-form" novalidate><label class="vh" for="ftr-email">Email</label><input class="input" id="ftr-email" type="email" required placeholder="Email address" autocomplete="email"><button type="submit" aria-label="Sign up">' + I.arrow + '</button></form>' +
            '<p class="consent" id="ftr-msg">By signing up you agree to receive marketing emails. Unsubscribe anytime. See our <a href="policies.html?p=privacy">Privacy Policy</a>.</p></div>' +
          acc('The team', [['The Machine', 'machine.html'], ['Our Story', 'story.html'], ['Schedule', 'schedule.html'], ['Pit Log', 'log.html'], ['Gallery', 'gallery.html'], ['Sponsors', 'sponsors.html'], ['Book the team', 'book.html']]) +
        '</div>' +
        '<div class="ftr__social"><a href="https://www.facebook.com/heavymetalprostock/" target="_blank" rel="noopener" aria-label="Facebook (opens in a new tab)">' + I.fb + '</a><a href="#" aria-label="Instagram (pending)">' + I.ig + '</a><a href="#" aria-label="TikTok (pending)">' + I.tt + '</a><a href="#" aria-label="YouTube (pending)">' + I.yt + '</a></div>' +
        '<p class="ftr__biz">© ' + new Date().getFullYear() + ' Heavy Metal Pro Stock: “The Evil One” · Waterloo, WI<br><span class="muted">P.O. Box 42, Waterloo, WI 53594 · <a href="mailto:heavymetalevil72@gmail.com">heavymetalevil72@gmail.com</a> · <a href="tel:+19206504374">(920) 650-4374</a></span></p>' +
        '<nav class="ftr__legal" aria-label="Legal"><a href="policies.html?p=privacy">Privacy Policy</a><a href="policies.html?p=terms">Terms of Service</a><a href="policies.html?p=refund">Refund Policy</a><a href="policies.html?p=shipping">Shipping Policy</a><a href="policies.html?p=contact">Contact Information</a><a href="policies.html?p=accessibility">Accessibility</a><a href="policies.html?p=choices">Your Privacy Choices</a><a href="#" id="cookie-prefs">Cookie Preferences</a></nav>' +
      '</div></footer>' +
      '<div class="cookie" id="cookie" role="region" aria-label="Cookie consent" hidden><p class="h3">We use cookies</p><p>We use cookies to run the store, remember your cart and, if you allow it, to measure ads. You can change this anytime in Cookie Preferences. <a href="policies.html?p=privacy">Privacy Policy</a> · <a href="policies.html?p=choices">Your Privacy Choices</a></p><div class="cookie__prefs" id="cookie-prefs-panel" hidden><label class="tgl"><input type="checkbox" checked disabled><span><b>Necessary</b><br>Cart, checkout and security. Always on.</span></label><label class="tgl"><input type="checkbox" id="ck-an"><span><b>Analytics</b><br>Helps us see which pages work.</span></label><label class="tgl"><input type="checkbox" id="ck-mk"><span><b>Marketing</b><br>Facebook and Google ads.</span></label><label class="tgl"><input type="checkbox" id="ck-pf"><span><b>Preferences</b><br>Remembers your choices.</span></label></div><div class="btn-row"><button class="btn" type="button" data-cookie="accept">Accept all</button><button class="btn btn--ghost" type="button" data-cookie="decline">Decline</button><button class="btn btn--ghost" type="button" data-cookie="manage" id="ck-manage">Manage</button></div></div>';
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
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { hideAll(); closeMega(); return; }
    /* aria-modal: el Tab se queda dentro del panel abierto */
    if (e.key !== 'Tab' || !open) return;
    var f = [].filter.call(open.querySelectorAll('a[href],button:not([disabled]),input:not([disabled]),textarea,select,summary,[tabindex]:not([tabindex="-1"])'), function (x) { return x.getClientRects().length && !x.closest('[hidden]') && !(x.closest('details:not([open])') && x.tagName !== 'SUMMARY' && !x.closest('summary')); });
    if (!f.length) return;
    var i = f.indexOf(document.activeElement);
    if (e.shiftKey && (i <= 0)) { e.preventDefault(); f[f.length - 1].focus(); }
    else if (!e.shiftKey && (i === f.length - 1 || i < 0)) { e.preventDefault(); f[0].focus(); }
  });

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
  function escH(t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function recents() { try { return JSON.parse(localStorage.getItem('hm-recent') || '[]'); } catch (e) { return []; } }
  function renderSugg(q) {
    var ul = $('sugg'); if (!ul) return;
    var words = [];
    if (q) {
      CAT.forEach(function (p) { (p.name + ' ' + p.sub).toLowerCase().split(/[^a-z0-9]+/).forEach(function (w) { if (w.length > 2 && w.indexOf(q.split(' ').pop()) === 0 && words.indexOf(w) < 0) words.push(w); }); });
      words = words.slice(0, 5).map(function (w) { return q.split(' ').slice(0, -1).concat(w).join(' '); });
      $('sugg-h').textContent = 'Suggestions';
    } else {
      words = CAT.filter(function (p) { return p.tag === 'best'; }).map(function (p) { return p.name.toLowerCase().replace(/ tee$| cap$/, ''); }).slice(0, 4);
      $('sugg-h').textContent = 'Trending';
    }
    ul.innerHTML = words.map(function (w) { return '<li><a href="search.html?q=' + encodeURIComponent(w) + '">' + escH(w) + '</a></li>'; }).join('');
    var r = recents(), rw = $('recent-wrap');
    rw.hidden = !!q || !r.length;
    $('recent').innerHTML = r.map(function (w) { return '<li><a href="search.html?q=' + encodeURIComponent(w) + '">' + escH(w) + '</a></li>'; }).join('');
  }
  function renderSearch(q) {
    q = (q || '').trim().toLowerCase(); renderSugg(q);
    var list = q ? CAT.filter(function (p) { return (p.name + ' ' + p.sub + ' ' + p.cat).toLowerCase().indexOf(q) > -1; }) : CAT.filter(function (p) { return p.tag === 'best'; });
    $('search-h').textContent = q ? (list.length ? list.length + ' products for "' + q + '"' : 'No products for "' + q + '"') : 'Best sellers';
    $('search-res').innerHTML = list.slice(0, 4).map(window.hmCard).join('') || '<p class="muted" style="grid-column:1/-1;margin:0">Try "tee", "hoodie" or "kids". Or browse <a href="shop.html?cat=all">Shop all</a>.</p>';
    var all = $('search-all'); all.hidden = !q || !list.length; all.firstChild.href = 'search.html?q=' + encodeURIComponent(q);
  }
  if ($('search-open')) {
    $('search-open').addEventListener('click', function () { show($('search'), $('q')); renderSearch(''); });
    $('search-close').addEventListener('click', hideAll);
    $('q').addEventListener('input', function () { renderSearch(this.value); });
    $('q').form.addEventListener('submit', function () { var v = $('q').value.trim(); if (!v) return; var r = recents().filter(function (x) { return x !== v; }); r.unshift(v); try { localStorage.setItem('hm-recent', JSON.stringify(r.slice(0, 4))); } catch (e) {} });
  }

  /* carrito */
  function setCount(n) {
    count = n;
    var c = $('cart-count'); if (!c) return;
    c.textContent = n; c.setAttribute('data-n', n); $('drawer-count').textContent = n;
    $('cart-open').setAttribute('aria-label', 'Cart, ' + n + ' items');
    $('cart-empty').hidden = n > 0; $('ship-bar').hidden = n === 0;
    var pct = Math.min(100, n * 30); $('tiers-fill').style.width = pct + '%';
    $('tiers-msg').innerHTML = pct >= 100 ? '<b>You unlocked free shipping and a free sticker.</b>' : pct >= 60 ? 'Free US shipping unlocked. <b>$XX</b> more for a <b>free sticker</b>' : 'You are <b>$XX</b> away from <b>free US shipping</b>';
    var hasTee = [].some.call($('lines').querySelectorAll('[data-cat]'), function (l) { return l.getAttribute('data-cat') === 'tees'; });
    var hasCap = !!$('lines').querySelector('[data-id="crew-cap"]');
    $('upgrade').hidden = !hasTee || hasCap;
  }
  function openCart() { show($('drawer'), $('cart-close')); }
  if ($('cart-open')) {
    $('cart-open').addEventListener('click', openCart);
    $('cart-close').addEventListener('click', hideAll);
    $('checkout').addEventListener('click', function (e) { e.preventDefault(); this.textContent = 'Boceto: aquí abre el checkout de Shopify'; });
    setCount(0);
  }
  window.hmAdd = function (name, variant, price, qty) {
    qty = Math.max(1, parseInt(qty, 10) || 1);
    var p = CAT.filter(function (x) { return x.name === name; })[0] || { id: '', name: name, cat: 'tees', colors: [], sizes: [] };
    var li = document.createElement('li'); li.className = 'line'; li.setAttribute('data-cat', p.cat); li.setAttribute('data-id', p.id);
    li.innerHTML = '<span class="thumb thumb--mock">' + mock(p) + '</span><div><p class="line__n">' + name + '</p><p class="line__v">' + (variant || '') + '</p>' +
      '<div class="qty"><button type="button" data-q="-1" aria-label="Decrease quantity">−</button><span class="num" aria-live="polite">' + qty + '</span><button type="button" data-q="1" aria-label="Increase quantity">+</button></div><button type="button" class="line__rm" data-rm>Remove</button></div><p class="num" style="margin:0">' + (price || '$XX') + '</p>';
    $('lines').appendChild(li); setCount(count + qty); openCart();
  };
  if ($('lines')) $('lines').addEventListener('click', function (e) {
    var li = e.target.closest('.line'); if (!li) return;
    var q = e.target.closest('[data-q]'), n = li.querySelector('.qty .num');
    if (q) { var v = Math.max(1, +n.textContent + +q.getAttribute('data-q')); setCount(count + v - +n.textContent); n.textContent = v; }
    if (e.target.closest('[data-rm]')) { setCount(count - +n.textContent); li.remove(); setCount(count); }
  });

  /* selector rápido de talla: Add to cart en tarjetas nunca elige talla por el cliente */
  var qp = null;
  function quick(id) {
    var p = CAT.filter(function (x) { return x.id === id; })[0]; if (!p) return;
    if (p.status !== 'live') { location.href = href(p) + '#notify'; return; }
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

  /* cupón: en Shopify los códigos se crean en Descuentos y el tema los aplica en el carrito (sin app) */
  var cf = $('coupon-form');
  if (cf) cf.addEventListener('submit', function (e) { e.preventDefault(); var v = $('coupon').value.trim().toUpperCase(); $('coupon-msg').textContent = v ? 'Boceto: aquí Shopify valida "' + v + '" y muestra el descuento en el subtotal.' : 'Enter a code.'; });

  /* redes pendientes (Instagram, TikTok, YouTube): el link "#" no salta arriba */
  [].forEach.call(document.querySelectorAll('.ftr__social a[href="#"]'), function (a) { a.addEventListener('click', function (e) { e.preventDefault(); }); });
  /* footer: una sola lista (The Evil List) */
  var ff = $('ftr-form');
  if (ff) ff.addEventListener('submit', function (e) {
    e.preventDefault(); var em = $('ftr-email');
    if (!em.value || !em.checkValidity()) { $('ftr-msg').textContent = 'Enter a valid email to join The Evil List.'; em.focus(); return; }
    $('ftr-msg').textContent = "You're on the list. Check your inbox to confirm.";
  });

  /* mostrar u ocultar notas de boceto (para ver la página como la verá el cliente) */
  var nt = $('notes-toggle');
  if (nt) {
    var hideN = false; try { hideN = sessionStorage.getItem('hm-notes') === '0'; } catch (e) {}
    var applyN = function () { document.documentElement.classList.toggle('no-notes', hideN); nt.textContent = hideN ? 'Mostrar notas' : 'Ocultar notas'; nt.setAttribute('aria-pressed', hideN ? 'true' : 'false'); };
    applyN();
    nt.addEventListener('click', function () { hideN = !hideN; try { sessionStorage.setItem('hm-notes', hideN ? '0' : '1'); } catch (e) {} applyN(); });
  }

  /* banner de cookies: se muestra una vez por visita del boceto */
  var ck = $('cookie');
  if (ck) {
    var seen = false; try { seen = sessionStorage.getItem('hm-cookie') === '1'; } catch (e) {}
    ck.hidden = seen;
    ck.addEventListener('click', function (e) {
      var b = e.target.closest('[data-cookie]'); if (!b) return;
      if (b.getAttribute('data-cookie') === 'manage') {
        var pp = $('cookie-prefs-panel');
        if (pp.hidden) { pp.hidden = false; b.textContent = 'Save choices'; return; }
      }
      ck.hidden = true; try { sessionStorage.setItem('hm-cookie', '1'); } catch (err) {}
    });
    $('cookie-prefs').addEventListener('click', function (e) { e.preventDefault(); ck.hidden = false; var fb = ck.querySelector('[data-cookie]'); if (fb) fb.focus(); });
  }
})();
