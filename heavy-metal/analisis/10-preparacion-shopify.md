# QA 05 · Port del boceto v27 a Shopify OS 2.0

Tema destino: **"HM v14 BORRADOR rediseño"** (duplicado sin publicar). Tema en vivo **heavy-metal-tema-v12**: no se toca.
Fuente revisada: las 23 páginas de `boceto-v27/`, `hm.js`, `hm.css`, `hero.js`, `hero.css`, todas las notas `<p class="note">` (incluidas las que pinta `hm.js`: carrito, búsqueda, franja de patrocinadores), los comentarios HTML con "En Shopify", `PENDIENTES.md`, `PROMPT-MAESTRO.md` (v7, desactualizado) y el dump del tema en vivo en `analisis/tema/`.
Este documento es solo reporte: no se editó ningún archivo.

Leyenda de tipo:
- **NAT** = nativo Shopify (Liquid, settings y bloques, objetos estándar).
- **MO** = requiere metaobjeto o metacampo.
- **APP** = requiere app.
- **JS** = requiere JS a medida (además de lo anterior cuando aplica).

Punto de partida técnico: el tema en vivo es **Dawn reskineado** (`global.js`, `main-product`, `predictive-search`, `cart-drawer`, más secciones `hm-*`). Recomendación: conservar el núcleo de Dawn (formulario de producto, carrito AJAX, búsqueda predictiva, facetas, cuentas) y reemplazar su piel con el `hm.css` del boceto. Así no se reescribe lógica de compra que ya funciona.

---

## 1. Inventario por página

### 1.0 Global (layout y grupos de secciones, sale en todas las páginas)

| Parte del boceto | Sección / snippet propuesto | Bloques y settings | Datos | Tipo |
|---|---|---|---|---|
| Barra de anuncios rotativa con pausa | `sections/hm-announcement.liquid` (header-group) | Bloque "Message" (richtext, máx. 3). Setting: segundos por mensaje | Settings del tema. `[season]` se reemplaza por el ajuste Temporada | NAT + JS (rotación y botón pausa) |
| Header: logo, menú, mega menú con fotitos de categoría, menú móvil, búsqueda, cuenta, carrito | `sections/hm-header.liquid` + `snippets/hm-mega.liquid` | Settings: logo (image_picker o SVG en snippet), menú principal (link_list), menú de categorías (link_list), mostrar fotitos | Menú `main-menu-v14` (nuevo, no tocar el del vivo). Fotito = `collection.image` de cada link | NAT + JS (mega por clic/foco/hover, cajón móvil) |
| Búsqueda predictiva (Trending, recientes, sugerencias) | Reusar `predictive-search` de Dawn, reskin | Setting: colección "Best sellers" para Trending | API `/search/suggest` (nativa). Trending = colección automática ordenada por más vendidos. Recientes = localStorage | NAT + JS |
| Franja de patrocinadores antes del footer ("Backed by" / "Your logo here") | `sections/hm-sponsor-strip.liquid` (footer-group). Se oculta en 404, 3208 y Sponsors con setting por plantilla o `template.suffix` | Settings: título con y sin patrocinadores, texto del CTA, velocidad | Metaobjeto **Sponsor** (activos, orden por paquete y por `order`) | MO + JS (botón de pausa obligatorio, ver 5) |
| Footer: Help, The Evil List, The team, redes, copyright, legales | `sections/hm-footer.liquid` | Settings: menús `footer-help`, `footer-team`, `footer-legal`; Facebook, Instagram (vacío = no sale); texto de consentimiento | Menús nativos. Copyright con `'now' \| date: '%Y'` | NAT |
| Formulario The Evil List del footer | dentro de `hm-footer` | `{% form 'customer' %}` con `contact[tags]=evil-list` | Clientes con consentimiento de marketing | NAT |
| Carrito lateral: barra de envío gratis con escalones, "Add to your order", upgrade a Crew Pack, Feed The Beast, código de descuento, nota | `snippets/hm-cart-drawer.liquid` (reemplaza `cart-drawer` de Dawn) + `assets/hm-cart.js` | Settings del tema: monto envío gratis, monto regalo (sticker), producto regalo, producto Feed The Beast, producto Crew Pack, fuente de add-ons (colección "Cart add-ons" o recomendaciones complementarias de Search & Discovery) | Carrito AJAX nativo (`/cart/add.js`, `/cart/update.js` con `discount`) | NAT + JS (ver 3) |
| Selector rápido de talla (bottom sheet) | `snippets/hm-quick-add.liquid` | Ninguno | Variantes del producto vía Section Rendering API | JS |
| Ventana "Notify me" | `snippets/hm-notify-modal.liquid` | Texto, aviso de privacidad | `{% form 'customer' %}` con etiquetas `notify, notify-<handle>` o app de reposición | NAT o APP (ver 3) |
| Esqueleto de carga | `snippets/hm-skeleton.liquid` + CSS | Ninguno | Ninguno | NAT (CSS) |
| Tarjeta de producto (flechas frente/espalda/color, badges, Almost gone!, Coming soon, Sold out, Add to cart con talla) | `snippets/hm-card.liquid` | Ninguno | `product.media`, `product.tags` (`coming-soon`, `new`, `best-seller`), inventario de variantes, metacampo `custom.card_note` (ya existe en el vivo) | NAT + JS (flechas) |
| Banner de cookies | Nativo (Configuración > Privacidad del cliente) | Ninguno en tema; el link "Cookie Preferences" llama a `window.Shopify.customerPrivacy` / `privacyBanner.showPreferences()` | Nativo | NAT + JS mínimo |
| Skip link, `lang="en"`, JSON-LD Organization/SportsTeam y WebSite | `layout/theme.liquid` + `snippets/hm-jsonld-org.liquid` | Settings: redes, logo | Settings | NAT |

### 1.1 Home (`index.html` → `templates/index.json`)

| Sección del boceto | Sección Liquid | Bloques / settings | Datos | Tipo |
|---|---|---|---|---|
| Hero "Full Pull" (logo grande, tractor real + sled, humo, tormenta, rayo, pull sim, Pause / Resume / Pull again) | `hm-hero.liquid` + `snippets/hm-rig.liquid` (ya existe en vivo) + `assets/hm-hero.js` + `assets/hm-hero.css` | Settings: logo (SVG), recorte del tractor (image_picker, PNG/WebP transparente), fondo de tormenta, distancia de full pull (300 ft), botones 1 y 2 (texto + link), texto bajo el título | Settings de sección | JS (animación) |
| Cinta amarilla | Dentro de `hm-hero` | Bloque "Tape phrase" (text), máx. 3 | Settings | NAT + CSS |
| Shop: fotitos de categoría + una fila de 4 productos | `hm-shop-home.liquid` | Settings: menú de categorías, colección destacada, cantidad (4), título "“The Evil One” Drop", link | Colecciones automáticas | NAT |
| Banda The Machine (única banda oscura) | `hm-machine-band.liquid` | Settings: título, texto, foto x2, link. Bloques "Chip" (dato) | Settings | NAT |
| First fire (video de la dueña con rayo) | `hm-first-fire.liquid` | Settings: video (`video` setting, archivo de Shopify) o URL de YouTube, póster, duración "0:XX", texto | Contenido > Archivos | NAT (+ fachada de YouTube JS) |
| Next pull + contadores de temporada | `hm-next-pull.liquid` | Settings: texto sin fecha ("date TBA"), link a Facebook | Metaobjetos **Pull event** (próximo con fecha futura) y **Season stats** (temporada del ajuste global) | MO + JS (la fecha "futura" se decide en el navegador, ver 3) |
| Franja de patrocinio (frase de venta calculada + botón) | `hm-sponsor-cta.liquid` | Settings: plantilla de frase con `{fans}` y `{pulls}`, botón | Metaobjeto **Sponsor stats** (pulls × fans por pull; vacío = "XX") | MO |

### 1.2 Shop (`shop.html` → `templates/collection.json`, también `/collections/all`)

| Sección | Sección Liquid | Bloques / settings | Datos | Tipo |
|---|---|---|---|---|
| Encabezado: título, frase, fotitos de categoría, toolbar Sort / Filter + conteo | `hm-collection-head.liquid` | Settings: menú de categorías, mostrar descripción | `collection.title`, `collection.description`, menú | NAT |
| Panel lateral de filtros (talla, color, categoría) y orden | `hm-collection-grid.liquid` (sobre `main-collection-product-grid` de Dawn) | Settings: productos por página, columnas (4) | Filtros de **Search & Discovery** (`collection.filters`), `sort_by` | NAT + APP gratis (S&D) + JS (cajón) |
| Grid de tarjetas con estados | `hm-card` | Ninguno | Productos de la colección | NAT |
| "Nothing matches these filters" | Dentro de la grid | Texto | Nativo | NAT |
| Tienda vacía "Coming soon" con aviso por email | `snippets/hm-coming-soon.liquid` | Texto, formulario | `collection.products_count == 0` / sin productos disponibles | NAT |

Colecciones necesarias (todas automáticas): Tees, Sweatshirts, Hats, Kids, Stickers & gear, Bundles, New drop (etiqueta `new`), Special edition (etiqueta `special-edition`), Best sellers (todas, orden más vendidos), Cart add-ons (opcional).

### 1.3 Producto (`product.html` → `templates/product.json` + `product.bundle.json`)

| Sección | Sección Liquid | Bloques / settings | Datos | Tipo |
|---|---|---|---|---|
| Breadcrumb | `hm-main-product` (bloque) | | `collection` o `product.type` | NAT |
| Galería (imagen grande, flechas, contador, miniaturas, swipe, zoom/lightbox) | `hm-main-product` + `assets/hm-gallery-pdp.js` | Setting: zoom sí/no | `product.media` (orden que la dueña arrastra) | NAT + JS |
| Título, estrellas, precio, descripción corta | Bloques `title`, `rating` (app block Judge.me), `price`, `text` | | Producto, Judge.me | NAT + APP |
| Color y talla obligatoria, tallas agotadas deshabilitadas, "Select a size" | Bloque `variant_picker` | Setting: exigir talla (sin preselección) | Opciones de Printify ("Color", "Size") | NAT + JS (no preseleccionar talla) |
| Cantidad, Add to cart, Shop Pay | Bloques `quantity`, `buy_buttons` | | Nativo | NAT |
| Caja Notify me (Coming soon / Sold out) | Bloque `notify` | Texto | Formulario de cliente con etiqueta o app | NAT o APP |
| "Printed to order · ships in 5 days. Free US shipping over $XX." | Bloque `text` con variables | Usa setting global de monto de envío gratis | Settings | NAT |
| Black Smoke Guarantee con sustantivo adaptado ("this hoodie") | Bloque `guarantee` | Link a política `#bsg` | Metacampo `custom.guarantee_noun` con respaldo por `product.type` | MO |
| Acordeones: Details, Design story, Shipping & returns | Bloques `collapsible` | Contenido por bloque | Details: metacampo `custom.details` (lista) o descripción de Printify. Story: `custom.design_story`. Shipping: setting global | MO |
| Sticky Add to cart | Dentro de `hm-main-product` | | | JS |
| Guía de tallas (dialog) | Bloque `size_guide` + `snippets/hm-size-table.liquid` | | Metacampo `custom.size_chart` → metaobjeto **Size chart** | MO |
| Complete the look (Crew Pack) | `hm-complete-look.liquid` | Setting: producto (o metacampo) | `custom.complete_the_look` (product_reference) o complementarios de S&D | MO |
| Reviews (promedio, barras, fit, fotos, Verified buyer, Write a review) | App block **Judge.me** | | Judge.me | APP |
| You may also like | `hm-related.liquid` | Cantidad | Product Recommendations API (`/recommendations/products`) | NAT + JS (carga diferida) |
| Esqueleto de carga | CSS | | | NAT |
| JSON-LD Product + BreadcrumbList | `snippets/hm-jsonld-product.liquid` | | Producto + Judge.me (rating) | NAT |

### 1.4 Edición especial (`limited.html` → `templates/collection.special-edition.json` + `templates/product.special-edition.json`)

| Sección | Sección Liquid | Bloques / settings | Datos | Tipo |
|---|---|---|---|---|
| El drop: foto, nombre, "Limited run of XX", cuenta regresiva, estado automático (Coming soon / Live / Sold out), unidades que quedan, Add to cart, Notify me, hechos ("One run only") | `hm-drop.liquid` (existe uno en el vivo, se rehace) | Bloques "Fact" (ícono + texto). Settings: textos de cada estado | Producto de la colección Special edition con metacampos `start_date`, `end_date`, `run_size`, `story`, `updated`; inventario | MO + JS (contador y cambio de estado en el navegador) |
| Past editions con filtro por año | `hm-past-editions.liquid` | Setting: texto de archivo vacío | Productos con `end_date` pasado o inventario 0 | MO + JS (filtro por año y decisión de fecha en cliente) |
| JSON-LD Product | snippet | | | NAT |

### 1.5 The Machine (`machine.html` → `templates/page.the-machine.json`)

| Sección | Sección Liquid | Bloques / settings | Datos | Tipo |
|---|---|---|---|---|
| Hero + galería real | `hm-machine-hero.liquid` | Bloques "Photo" (imagen, alt, posición) | Settings | NAT |
| Anatomía interactiva (números, líneas guía, panel con foto) | `hm-anatomy.liquid` + `assets/hm-anatomy.js` (mismo patrón que el mapa de calcomanías) | Setting: recorte del tractor (1120x576) | Metaobjeto **Tractor part** | MO + JS |
| Spec sheet de carreras + "Last updated" | `hm-spec-sheet.liquid` (existe en vivo, se rehace) | Bloques "Row" (label, value; vacío = no sale). Setting: fecha Last updated | Settings | NAT |
| Hear it (video del arranque) | Dentro de spec sheet o `hm-video.liquid` | Setting: video / YouTube, póster | Archivos | NAT |
| Cat V8 vs the field (8 en V contra 6 en línea; 636 stock +44 built) | `hm-v8-compare.liquid` | Settings de texto; dibujo fijo en SVG | Settings | NAT |
| FAQ "Questions from the fence line" (8 preguntas) | `hm-faq.liquid` reutilizable | Bloques "Question" o lista de **FAQ item** filtrada por página | Settings o metaobjeto | NAT / MO |
| The spec sheet, on a tee (una playera, se oculta si no está publicada) | `hm-spec-tee.liquid` | Setting: producto | Producto (si Sold out o Coming soon el botón dice Notify me) | NAT |

### 1.6 Our Story (`story.html` → `templates/page.our-story.json`)

| Sección | Sección Liquid | Bloques / settings | Datos | Tipo |
|---|---|---|---|---|
| Hero compacto | `hm-story-hero.liquid` | Imagen x2, título, texto | Settings | NAT |
| Hitos (2014, Feb 2020, 2026...) | `hm-milestones.liquid` | Bloques "Milestone" (año, título, texto) | Settings | NAT |
| Capítulos en 3 columnas (carrusel en móvil) | `hm-chapters.liquid` | Bloques "Chapter" (foto, título, texto) | Settings | NAT + CSS scroll-snap |
| Entrada a la historia completa | `hm-read-cta.liquid` | Página destino, texto | Settings | NAT |
| El rayo con video | `hm-bolt.liquid` | Video, póster, duración, texto | Archivos / YouTube | NAT + JS (fachada) |
| Primer pull + contadores con selector de año | `hm-season-stats.liquid` (reutilizable en home y Book) | Settings: textos | Metaobjeto **Season stats** (todas las entradas, selector de año) | MO + JS (selector) |
| Tractor brothers (Diesel Ross) | `hm-brothers.liquid` | Foto, texto, link | Settings | NAT |
| Walk-up song + playlist Spotify | `hm-walkup.liquid` | Settings: "Playlist link", fecha Last updated | URL de Spotify → iframe `open.spotify.com/embed/...` | NAT + JS (cargar al hacer clic) |
| Crew (iniciales si no hay foto, mascotas) | `hm-crew.liquid` | Setting: título | Metaobjeto **Crew member** | MO |
| CTA final | `hm-cta.liquid` (reutilizable) | Título, texto, botón | Settings | NAT |

### 1.7 The full story (`the-full-story.html` → `templates/page.full-story.json`)

| Sección | Sección Liquid | Bloques / settings | Datos | Tipo |
|---|---|---|---|---|
| Hero a sangre + tiempo de lectura | `hm-longread-hero.liquid` | Imagen, título | `page.title`, tiempo = palabras de `page.content` / 230 (Liquid) | NAT |
| Cuerpo tipo álbum (h2 con nota de año en el margen, fotos como copias impresas que salen al margen, una cita con marcador) | `hm-longread.liquid` | **Recomendado: bloques** "Heading" (texto + año), "Paragraph" (richtext), "Photo" (imagen + posición izquierda/derecha/ancho), "Quote" | Settings. Si se usa `page.content`, la dueña no puede poner las clases de posición de cada foto | NAT |
| CTA a sponsors | `hm-cta` | | | NAT |

### 1.8 Schedule (`schedule.html` → `templates/page.schedule.json`, mismo handle que el vivo)

| Sección | Sección Liquid | Bloques / settings | Datos | Tipo |
|---|---|---|---|---|
| Título con temporada, resumen (competencias, exhibiciones, wins "Coming soon"), barra List / Calendar, temporada, Upcoming / Past | `hm-schedule.liquid` + `assets/hm-schedule.js` | Settings: fecha Last updated, link a Facebook | Metaobjeto **Pull event** (todas las entradas no Hidden, impresas como JSON en la página) | MO + JS |
| Vista lista: próximos e historial con resultado, distancia, video, "Photos & video", "Add to calendar" (.ics) | Igual | | Pull event + referencia a **Album** | MO + JS (.ics con Blob) |
| Vista calendario (mes, navegación, detalle) | Igual | | Pull event | JS |
| Where to watch (NTPA, Full Pull LIVE, Badger State, IHRA Pro Pulling, Green County Fair) | `hm-watch.liquid` | Bloques "League" (nombre, nota) y "Link" (texto, URL, nota Free/Paid) | Settings | NAT |
| First time at a pull? | `hm-tips.liquid` | Bloques "Tip" | Settings | NAT |
| The Evil List (única acción) | `hm-evil-cta.liquid` (reutilizable) | Textos | `{% form 'customer' %}` | NAT |
| JSON-LD SportsEvent por pull | snippet | | Pull event | NAT |

### 1.9 Pit Log (`log.html` → `templates/blog.pit-log.json` + `templates/article.json`)

| Sección | Sección Liquid | Bloques / settings | Datos | Tipo |
|---|---|---|---|---|
| Título, Last updated (entrada más nueva), contadores de temporada | `hm-log-head.liquid` | Setting: fuente de contadores | `blog.articles.first.published_at`. Contadores: ver decisión en 4 (Season stats recomendado) | NAT / MO |
| Wins & milestones (Featured + Win o Milestone, máx. 6, flechas si son más de 3) | `hm-log-featured.liquid` | Setting: máximo (6) | Artículos con etiquetas | NAT + JS (carrusel) |
| Bitácora: 10 por página, Load more, filtros por tipo, buscador solo en Pit Log, "Photos & video" a la Galería, foto por tipo si no hay imagen destacada | `hm-log-list.liquid` | Settings: imagen por tipo (Test, Exhibition, Competition, Win), orden de prioridad | `paginate blog.articles by 10`, `/blogs/pit-log/tagged/<tag>`, `article.image`, metacampo `custom.gallery_album` | NAT + JS (Load more por Section Rendering API, buscador) |
| CTA "New entries hit Facebook first" | `hm-cta` | | | NAT |
| Plantilla de artículo | `hm-article.liquid` | | Artículo + metacampos | NAT |
| JSON-LD BlogPosting | snippet | | | NAT |

### 1.10 Sponsors (`sponsors.html` → `templates/page.sponsors.json`, mismo handle que el vivo)

| Sección | Sección Liquid | Bloques / settings | Datos | Tipo |
|---|---|---|---|---|
| Banda oscura: título, cifra de fans calculada (gancho), "How we count it" | `hm-sponsor-hero.liquid` (existe en vivo, se rehace) | Foto de la grada, textos | **Sponsor stats** | MO |
| "Why are you here?" (selector compacto, 4 opciones) | `hm-sponsor-intent.liquid` | Bloques "Intent" (texto, subtexto, link). La dueña aún no confirma si se queda | Settings | NAT |
| Pestañas dentro de la página | `hm-sponsor-tabs.liquid` | Bloques "Tab" (texto, ancla) | Settings | NAT + JS (marca la visible) |
| They already back "The Evil One" (o "No sponsors yet") | `hm-sponsor-board.liquid` | Textos | **Sponsor** activos agrupados por **Sponsor tier** | MO |
| Paquetes (Title $25,000, Pit $10,000, Crew $5,000; Available / Limited / Sold out / Hidden; destacado) | `hm-sponsor-tiers.liquid` | Setting: fecha Last updated automática (la más nueva) | **Sponsor tier** | MO |
| The season in numbers (est.) | `hm-sponsor-stats.liquid` | | **Sponsor stats** | MO |
| Where your logo goes (íconos, chips por paquete) | `hm-logo-placements.liquid` | | **Logo placement** + referencias a Sponsor tier | MO |
| Decal map (anatomía con zonas) | `hm-decal-map.liquid` + `assets/hm-anatomy.js` | Recorte del tractor | **Decal zone** | MO + JS |
| FAQ (7) | `hm-faq` | | Bloques o FAQ item | NAT / MO |
| Request a package (formulario, paquete en select) | `hm-sponsor-form.liquid` | Textos, aviso "within 2 business days" | `{% form 'contact' %}`; opciones del select desde Sponsor tier (Sold out = "Waitlist") | NAT |
| Meta description y JSON-LD con la cifra calculada | snippet | | Sponsor stats | NAT |

### 1.11 Gallery (`gallery.html` → `templates/page.gallery.json` + `templates/metaobject/album.json`)

| Sección | Sección Liquid | Bloques / settings | Datos | Tipo |
|---|---|---|---|---|
| Título, conteo, barra All / Photos / Videos, Filter y Events | `hm-gallery.liquid` + `assets/hm-gallery.js` | Settings: cuadros por tanda (24) | Metaobjeto **Album** (todas las entradas) | MO + JS |
| Panel lateral: Season, Event type, Event | Igual | | Album | JS |
| Mosaico a todo lo ancho + Load more | Igual | | Fotos y videos de cada Album | MO + JS |
| Visor (flechas, swipe, teclado, contador, miniaturas, presentación) | Igual | | | JS |
| `?event=<handle>` desde Schedule y Pit Log | Igual (filtro en el navegador) **y** página propia por álbum con metaobject web pages (`/pages/album/<handle>`) para SEO | | Album | MO + JS |
| CTA "Shot “The Evil One” at a pull? #HEAVYMETALPULLING" | `hm-cta` | | | NAT |

### 1.12 Book the team (`book.html` → `templates/page.book.json`)

| Sección | Sección Liquid | Bloques / settings | Datos | Tipo |
|---|---|---|---|---|
| Título, prueba (exhibiciones, 20+ años, Waterloo) y foto | `hm-book-hero.liquid` | Settings: años en el deporte, foto | Exhibiciones desde **Season stats** (0 = no sale) | MO |
| What we bring (tarjetas marcables, sin precios) | `hm-book-options.liquid` | | **Booking option** | MO + JS (marcar tarjeta = marcar casilla del formulario) |
| How it works + What we need from you | `hm-book-how.liquid` | Bloques "Step" y "Requirement" (label, valor; vacío = no sale, nunca "[pending]" en vivo) | Settings | NAT |
| Ask for a quote (formulario) | `hm-book-form.liquid` | Textos, fecha mínima | `{% form 'contact' %}` con campos `contact[...]` | NAT + JS (validación) |

### 1.13 The Evil List (`evil-list.html` → `templates/page.evil-list.json`)

| Sección | Sección Liquid | Bloques / settings | Datos | Tipo |
|---|---|---|---|---|
| Hero oscuro con formulario | `hm-evil-hero.liquid` | Textos, frecuencia | `{% form 'customer' %}` con `contact[tags]=evil-list`, nombre opcional; doble confirmación | NAT |
| Muestra de correo | Dentro del hero o `hm-image-text` | Imagen | Settings | NAT |
| What you get | `hm-evil-perks.liquid` | Bloques "Perk" (ícono de lista, título, texto) | Settings | NAT |
| Questions (3) | `hm-faq` | Bloques | Settings | NAT |

### 1.14 FAQ (`faq.html` → `templates/page.faq.json`)

| Sección | Sección Liquid | Bloques / settings | Datos | Tipo |
|---|---|---|---|---|
| Título, línea, buscador | `hm-faq-head.liquid` | | | NAT + JS (filtra en la página) |
| 12 categorías, **62 preguntas** | **Una sección `hm-faq` por categoría** (12 secciones, bajo el límite de 25) o metaobjeto **FAQ item** | Bloques "Question" (máx. 50 por sección; con 62 en una sola sección no cabe) | Settings o MO | NAT / MO |
| Still need help? | `hm-help-aside.liquid` | Links | | NAT |
| Last updated + JSON-LD FAQPage | snippet | Setting fecha | | NAT |

### 1.15 Size guide (`sizes.html` → `templates/page.sizes.json`)

| Sección | Sección Liquid | Datos | Tipo |
|---|---|---|---|
| Tablas por estilo (tee, long sleeve, hoodie, crewneck, kids, gorra, beanie) | `hm-size-guide.liquid` | Metaobjeto **Size chart** (misma fuente que el dialog de producto) | MO |
| How to measure | Bloques de texto | Settings | NAT |

### 1.16 Contact (`contact.html` → `templates/page.contact.json`)

| Sección | Sección Liquid | Datos | Tipo |
|---|---|---|---|
| Formulario (Topic, Name, Email, Order number, Message) | `hm-contact.liquid` (existe en vivo, se rehace) | `{% form 'contact' %}`, `contact[topic]` | NAT |
| Quick help + Reach the team (Facebook, Instagram [pending]) | Bloques "Help link" | Settings; Instagram vacío = no sale | NAT |

### 1.17 Policies (`policies.html` → `templates/page.policies.json`)

| Sección | Sección Liquid | Datos | Tipo |
|---|---|---|---|
| Una página con pestañas: Privacy, Terms, Refund, Shipping, Contact Information, Accessibility, Your Privacy Choices, Cookie Preferences; Last updated por política | `hm-policies.liquid` + JS de pestañas | `shop.policies` (Configuración > Políticas) + páginas normales para Accessibility; "Your Privacy Choices" la crea Shopify desde Privacidad del cliente; Cookie Preferences reabre el banner nativo. Fechas: bloque por política con fecha | NAT + JS |
| Black Smoke Guarantee (#bsg) dentro de Refund | Texto en la política | Configuración > Políticas | NAT |

Nota: las URLs nativas `/policies/refund-policy` etc. siguen existiendo (las enlaza el checkout) y no se pueden diseñar con plantilla propia; solo heredan el layout.

### 1.18 Account (`account.html`)

| Parte | Solución | Tipo |
|---|---|---|
| Sign in con código de 6 dígitos y Shop | **Nuevas cuentas de cliente** (Configuración > Cuentas de clientes). Las páginas las sirve Shopify en `shopify.com/<id>/account`, **no son plantillas del tema** | NAT (config) |
| "Hi, Jane", pedidos, dialog de pedido, direcciones, switch de The Evil List | Lo pinta Shopify. Solo se personaliza marca (logo, colores, tipografía) en el editor de checkout y cuentas. **El diseño del boceto no se puede portar tal cual** | NAT (limitado) |
| Track a package without an account | No hay buscador de pedidos de invitado nativo con cuentas nuevas. El link de rastreo llega en "Shipping confirmation" y en la página de estado del pedido. En el tema: bloque de texto con esa explicación + link a Contact | NAT |
| Ícono de cuenta en el header | `routes.account_url`, `customer` | NAT |

### 1.19 Search (`search.html` → `templates/search.json`)

| Sección | Sección Liquid | Datos | Tipo |
|---|---|---|---|
| Buscador, Products, Pages, filtros iguales a Shop | `hm-search.liquid` (sobre `main-search` de Dawn) | `search.results`, `search.filters` (S&D), sinónimos en S&D | NAT + APP gratis |
| Sin resultados: sugerencias + Best sellers | Igual | Colección Best sellers | NAT |
| Tienda sin merch: Coming soon | `hm-coming-soon` | | NAT |

### 1.20 404 (`404.html` → `templates/404.json`)

| Sección | Sección Liquid | Datos | Tipo |
|---|---|---|---|
| "Pull ended at 404 ft", buscador, 4 salidas, "Pull again", línea de la voz del tractor, "Psst... 3208" | `hm-404.liquid` + recorte del tractor + rig | Settings y bloques "Exit" (4) | NAT + JS (guiño "Pull again") |

### 1.21 Página 3208 (`3208.html` → `templates/page.3208.json`)

| Sección | Sección Liquid | Datos | Tipo |
|---|---|---|---|
| "You found the V8", código EVIL3208 con botón copiar, XX% off | `hm-egg.liquid` | Settings: código, texto del descuento. Página con metacampo `seo.hidden = 1` (fuera de buscador y sitemap) + `noindex` | NAT + JS (copiar) |

### 1.22 Correos (`correos.html`): no es página del sitio

| Pieza | Dónde vive en Shopify | Tipo |
|---|---|---|
| Carrito abandonado con voz del tractor | Marketing > Automatizaciones > Shopify Email "Abandoned checkout" | NAT (Shopify Email) |
| Nota impresa del paquete | Configuración > Envío y entrega > Hojas de embalaje. **Ojo: Printify no usa la hoja de embalaje de Shopify** (ver 3) | NAT, probablemente inútil con Printify |
| Confirmación de envío | Configuración > Notificaciones > Shipping confirmation (Liquid editable) | NAT |

### 1.23 Cómo editas todo (`editar.html`): no es página del sitio

Es el manual de la dueña. Se entrega como documento aparte (doc o PDF) y se actualiza con los nombres reales de metaobjetos y secciones al terminar. Su lista de tipos de metaobjeto está incompleta: le faltan **Sponsor, Booking option y Album** (y los nuevos FAQ item y Size chart si se aprueban).

---

## 2. Metaobjetos y metacampos (definitiva)

Reglas para todas las definiciones: acceso de **Storefront activado** (para leerlas en Liquid); campo `display_name` claro; `order` entero para ordenar; fechas "Updated" explícitas, porque Liquid no expone la fecha de edición de una entrada de metaobjeto. Nombres de tipo en inglés y snake_case. Se crean por Admin GraphQL (`metaobjectDefinitionCreate`, `metafieldDefinitionCreate`) en un script versionado, para poder repetirlo.

Advertencia: metaobjetos, metacampos, colecciones, blog, páginas y menús son **datos de la tienda, no del tema**. Crearlos no rompe el tema en vivo, pero las páginas y el blog quedan visibles en el sitio en vivo con su plantilla actual si se publican (ver 5).

### 2.1 Metaobjetos

**Pull event** (`pull_event`)
| Campo | Tipo | Notas |
|---|---|---|
| event_name | single_line_text (requerido) | "Green County Fall Nationals" |
| date | date | Vacío = "Date TBA" |
| start_time | single_line_text o date_time | "all times Central"; opcional |
| season | number_integer | Necesario para pulls sin fecha ("sin fecha cuenta en la temporada actual") |
| calendar_label | single_line_text (máx. 12) | Etiqueta corta del calendario |
| city | single_line_text | "Monroe, WI" |
| league | single_line_text con opciones | NTPA · Badger State Tractor Pullers · IHRA Pro Pulling (PPL) · Other |
| type | single_line_text con opciones | Competition · Exhibition |
| status | single_line_text con opciones | Upcoming · Done · Cancelled · Hidden |
| result | single_line_text | Texto libre para mostrar |
| place | number_integer | Recomendado en vez de leer "1st place" del texto: 1 = suma un win |
| full_pull | boolean | Recomendado en vez de leer "Full pull" del texto: saca la etiqueta amarilla |
| distance_ft | number_decimal | |
| video | url | YouTube |
| website | url | Sitio del evento |
| gallery_album | metaobject_reference → Album | "Photos & video" |

**Season stats** (`season_stats`)
| Campo | Tipo | Notas |
|---|---|---|
| season | number_integer (requerido, único) | Una entrada por año |
| competitions | number_integer | |
| competitions_note | single_line_text | Opcional |
| exhibitions | number_integer | 3 o 4 por confirmar |
| wins | number_integer | 0 = "Coming soon" |
| updated | date | Last updated |

**Sponsor tier** (`sponsor_tier`)
| Campo | Tipo | Notas |
|---|---|---|
| name | single_line_text | Title Partner, Pit Partner, Crew Supporter |
| key | single_line_text con opciones | title · pit · crew (para chips y orden) |
| price | number_integer (USD) | 25000 / 10000 / 5000 |
| tagline | single_line_text | |
| benefits | list.single_line_text | |
| featured | boolean | Pit = true |
| status | single_line_text con opciones | available · limited · soldout · hidden |
| spots_left | number_integer | Solo con limited |
| order | number_integer | |
| updated | date | |

**Sponsor** (`sponsor`)
| Campo | Tipo | Notas |
|---|---|---|
| name | single_line_text (requerido) | |
| logo | file_reference (imagen; SVG o PNG transparente) | |
| tier | metaobject_reference → Sponsor tier | Orden y tamaño en la franja |
| shape | single_line_text con opciones | round · square · wide |
| link | url | Abre su sitio |
| active | boolean | Desactivar sin borrar |
| order | number_integer | Orden dentro del paquete |
| season | number_integer | Opcional, para historial |

**Sponsor stats** (`sponsor_stats`): **recomendado como entrada única con campos fijos**, no una entrada por cifra, para que la frase calculada no se rompa por un nombre mal escrito.
| Campo | Tipo | Notas |
|---|---|---|
| pulls_per_season | number_integer | 20 |
| states | number_integer | 10 |
| fans_per_pull | number_integer | 5000. **Confirmar si es por pull o por temporada** |
| social_text | single_line_text | "Growing" |
| show_plus | boolean | "+" |
| estimated | boolean | "(est.)" |
| updated | date | |
Alcance calculado en Liquid: `pulls_per_season × fans_per_pull` (vacío = "XX").

**Logo placement** (`logo_placement`)
| Campo | Tipo | Notas |
|---|---|---|
| name | single_line_text | |
| icon | single_line_text con opciones | tractor · trailer · shirt · web · social · mic · pass |
| description | multi_line_text | |
| packages | list.metaobject_reference → Sponsor tier | |
| package_details | list.single_line_text | Una línea por paquete: "pit: shirt sleeve" |
| status | single_line_text con opciones | active · hidden |
| order | number_integer | |
| updated | date | |

**Decal zone** (`decal_zone`)
| Campo | Tipo | Notas |
|---|---|---|
| name | single_line_text | Rear fender, Roll cage, Hood... |
| x, y | number_integer | Píxeles sobre el recorte 1120x576 |
| label_x | number_integer | Posición de la etiqueta |
| row | single_line_text con opciones | top · bottom |
| size | single_line_text | "XX x XX in" por confirmar |
| tier | metaobject_reference → Sponsor tier | Vacío = "To confirm" |
| status | single_line_text con opciones | available · sold |
| description | multi_line_text | |
| order | number_integer | |
| updated | date | |

**Tractor part** (`tractor_part`)
| Campo | Tipo | Notas |
|---|---|---|
| name | single_line_text | Engine, Displacement, Turbo, Body, Weight, Tires |
| value | single_line_text | "Cat 3208 V8" |
| text | multi_line_text | Panel |
| image | file_reference (imagen) | Alt desde el archivo |
| image_position | single_line_text | "50% 55%" |
| x, y, label_x | number_integer | Sobre el recorte |
| row | single_line_text con opciones | top · bottom |
| order | number_integer | |

**Album** (`album`) con **web pages** activadas (plantilla `metaobject/album.json`)
| Campo | Tipo | Notas |
|---|---|---|
| event_name | single_line_text | |
| date | date | Vacío = se ordena por `order` |
| season | number_integer | |
| kind | single_line_text con opciones | Competition · Exhibition · Test |
| city | single_line_text | |
| league | single_line_text | |
| cover | file_reference | Portada de la tira de eventos |
| photos | list.file_reference (imágenes) | En el orden arrastrado; alt desde Archivos |
| videos | list.url | YouTube |
| video_files | list.file_reference (video) | Opcional, videos subidos |
| pull_event | metaobject_reference → Pull event | |
| pit_log_url | url | Link al artículo (no hay referencia nativa a artículo confiable) |
| order | number_integer | |

**Booking option** (`booking_option`)
| Campo | Tipo |
|---|---|
| name | single_line_text |
| icon | single_line_text con opciones (display · pull · meet · social) |
| text | multi_line_text |
| needs | single_line_text |
| order | number_integer |

**Crew member** (`crew_member`)
| Campo | Tipo | Notas |
|---|---|---|
| name | single_line_text | |
| role | single_line_text | "Owner, Driver & Crew Chief" |
| group | single_line_text con opciones | Driver · Team · Pit crew · Mascot |
| photo | file_reference | Sin foto = iniciales |
| note | single_line_text | "white", "black" en mascotas |
| bio | multi_line_text | Opcional (Chris F.: 20+ años) |
| order | number_integer | |

**Recomendados nuevos (no están en la lista de la dueña pero el boceto los necesita):**
- **Size chart** (`size_chart`): style (opciones tee, long sleeve, hoodie, crewneck, kids, cap, beanie), unit (in), columns (list.single_line_text), rows (list.single_line_text, "S | 18 | 28 | 8"), note. Lo leen `sizes.html` y el dialog de producto.
- **FAQ item** (`faq_item`): question, answer (rich_text), category (opciones de las 12), pages (list con opciones faq · machine · sponsors · evil-list), order. Evita el límite de 50 bloques y reutiliza preguntas.

### 2.2 Metacampos de producto (`custom.*`)

| Metacampo | Tipo | Uso |
|---|---|---|
| guarantee_noun | single_line_text | "this hoodie". Respaldo automático por `product.type` |
| design_story | rich_text o multi_line_text | Acordeón Design story |
| details | list.single_line_text | Fabric "XX% cotton, XX oz", fit, cuidado. Si no, la descripción de Printify |
| size_chart | metaobject_reference → Size chart | |
| complete_the_look | product_reference | Crew Pack u otro |
| card_note | single_line_text | Ya existe en el tema en vivo |
| bundle_savings | number_integer o money | "Save $X" del Crew Pack |
| drop_date | date_time | Opcional: "Drops Oct 17" en Coming soon |
| **Special edition:** start_date | date_time | Hora de Wisconsin |
| end_date | date_time | |
| run_size | number_integer | Sin número de edición (no se numera) |
| story | rich_text | |
| updated | date | Last updated |

Estado por etiquetas (decisión del boceto): `coming-soon`, `new`, `best-seller`, `special-edition`, `bundle`. "Almost gone!" = inventario total de 5 o menos. Sold out = inventario 0 con "Seguir vendiendo" apagado.

### 2.3 Otros metacampos

| Dueño | Metacampo | Tipo | Uso |
|---|---|---|---|
| Artículo (Pit Log) | custom.gallery_album | metaobject_reference → Album | "Photos & video" |
| Artículo | custom.pull_event | metaobject_reference → Pull event | Opcional |
| Artículo | custom.distance_ft | number_decimal | Opcional |
| Página 3208 | seo.hidden | number_integer = 1 | Fuera de búsqueda y sitemap |
| Producto Feed The Beast | seo.hidden | number_integer = 1 | Además de estado "Unlisted" |

### 2.4 Ajustes del tema (settings_schema)

Temporada (año), monto de envío gratis, monto y producto de regalo, producto Feed The Beast y montos, producto Crew Pack, colección Best sellers, colección de add-ons, redes (Facebook, Instagram), datos de contacto (solo para políticas), frase de marca, imágenes por tipo del Pit Log (o en la sección), fuentes.

---

## 3. Funciones que necesitan algo especial o no son posibles tal cual

| Función del boceto | Problema en Shopify | Solución recomendada | Tipo | Costo |
|---|---|---|---|---|
| **Feed The Beast** (propina de $1, $2 o $5 en el carrito para completar envío gratis) | No hay "propina en carrito" nativa. La propina nativa (Configuración > Checkout > Propinas) sale solo en el checkout y no cuenta para el envío gratis | Producto propio (no de Printify) con 3 variantes, estado **Unlisted**, `seo.hidden`, "requiere envío" apagado, impuestos según contador. El tema lo agrega por AJAX. Flow: pedido creado con ese SKU → etiqueta `tip`. Probar que Printify ignore esa línea y no frene el pedido. Texto legal: propina al equipo, no donativo ni deducible | NAT + JS | $0 |
| **Cupón EVIL3208** | Ninguno técnico. El código es público, cualquiera lo puede usar | Descuentos > Código, "una vez por cliente", % pendiente (#31), con fecha de fin. Decidir si combina con otros descuentos y con envío gratis | NAT | $0 |
| **Página 3208 oculta** | Las páginas salen en la búsqueda de la tienda y en el sitemap | Plantilla `page.3208`, `seo.hidden = 1`, `<meta name="robots" content="noindex">` por `template.suffix`, fuera de menús | NAT | $0 |
| **Notify me / back in stock** | Shopify no manda avisos de reposición. El formulario de cliente marca al cliente como **suscriptor de marketing**, lo que mezcla "avísame de esta prenda" con la lista general | Opción A (gratis, manual): `form 'customer'` con etiquetas `notify` y `notify-<handle>`, aviso de consentimiento claro, envío manual con Shopify Email a ese segmento; Flow: inventario pasa de 0 a más de 0 → correo interno a la dueña. Opción B (recomendada cuando haya ventas): app de reposición (Notify Me! Back in Stock, Appikon Back in Stock, o Klaviyo) | NAT o APP | A: $0. B: plan gratis con límite; de pago aprox. US$10 a 20 al mes (verificar precio vigente) |
| **Coming soon** | Si el producto está activo, alguien puede comprarlo por URL `/cart/add` aunque el tema oculte el botón | Etiqueta `coming-soon` + inventario 0 sin "Seguir vendiendo" (o publicación programada en el canal Tienda online) | NAT | $0 |
| **Sold out y Almost gone! con Printify** | Printify publica productos **sin control de inventario** (siempre disponibles). Así nunca habría Sold out ni "Almost gone!" | Para la merch normal: no mostrar "Almost gone!" (o activar control de inventario a mano solo en piezas limitadas). Para Special edition: control de inventario = run size. **Probar que Printify no sobrescriba el inventario** | NAT (config) | $0 |
| **Special edition: cuenta regresiva y cambio automático de estado** | Las páginas de Shopify se guardan en caché: `'now'` en Liquid no es la hora real del visitante. Y la venta no se abre ni se cierra sola | Liquid imprime fechas en `data-*`; el estado y el reloj los calcula JS. Apertura: publicación programada. Cierre: Flow con disparador programado diario → producto con `end_date` pasada → ocultar del canal o inventario 0 (verificar acción disponible en Flow). Sin Flow, la dueña lo apaga a mano | MO + JS + Flow | $0 (Flow incluido en Basic) |
| **Next pull "el primero con fecha futura"** | Mismo problema de caché | Liquid imprime los pulls Upcoming como JSON; JS elige el próximo según la fecha del visitante | MO + JS | $0 |
| **.ics "Add to calendar"** | Shopify no puede servir `text/calendar` (todas las plantillas salen como HTML) | Generarlo en el navegador con Blob (como el boceto) + link alternativo a Google Calendar | JS | $0 |
| **Filtros Search & Discovery** | Los filtros de talla y color dependen de que Printify use siempre los mismos nombres de opción ("Color", "Size") y valores | App S&D (gratis): filtros por opción, tipo, disponibilidad; sinónimos (hoodie = sweatshirt, hat = cap); complementarios para "Add to your order" | APP | $0 |
| **Búsqueda predictiva con Trending y recientes** | No hay "trending" nativo | Trending = colección Best sellers; recientes = localStorage; sugerencias = API predictiva nativa | NAT + JS | $0 |
| **Reseñas Judge.me** (estrellas, fotos, Verified buyer, fit y talla, Helpful) | Las preguntas de fit/talla son formularios personalizados del plan de pago | Judge.me Free: reseñas con foto, correo de solicitud, moderación, estrellas en Google. Fit y talla: plan Awesome. Borrar las reseñas de ejemplo; nunca importar reseñas falsas | APP | Free $0; Awesome aprox. US$15 al mes (verificar) |
| **Cuenta con código** | Las nuevas cuentas no son parte del tema; el diseño del boceto no se aplica | Activar cuentas nuevas; marca en el editor de checkout y cuentas. Ajustar la página Account del boceto a lo que Shopify permite | NAT (limitado) | $0 |
| **Track my order sin cuenta** | No hay buscador de pedidos de invitado | Link del correo "Shipping confirmation" y página de estado del pedido; texto + Contact. App de rastreo solo si hace falta después | NAT | $0 |
| **Bundles (Crew Pack)** | Shopify Bundles crea un producto padre con componentes; **la compatibilidad con Printify no está garantizada** (Printify debe recibir los productos componentes) | Recomendado: Crew Pack como **descuento automático nativo** (comprar tee + cap = $X menos), con página de producto que agrega los dos artículos. Si se usa Shopify Bundles, hacer pedido de prueba con Printify antes | NAT + JS | $0 |
| **Barra de envío gratis con escalones y sticker de regalo** | Liquid no puede leer el monto de la tarifa de envío gratis: se repite en un ajuste del tema y hay que mantenerlos iguales. El regalo no se agrega solo | Ajuste del tema con el monto; tarifa de envío gratis en Envío y entrega; regalo = descuento automático "Compra X obtén Y" con compra mínima + JS que agrega el sticker al llegar al monto | NAT + JS | $0 (apps de carrito UpCart, Rebuy, AfterSell: US$15 a 99 al mes, solo si después hace falta) |
| **Countdown** | Ver Special edition | JS | JS | $0 |
| **Cookie banner** | El banner nativo permite cambiar textos, colores y posición, no el diseño exacto del boceto (Necessary, Analytics, Marketing, Preferences sí existen en "Manage") | Banner nativo; "Cookie Preferences" del footer reabre el panel con la API de privacidad. Quitar el banner del boceto | NAT + JS mínimo | $0 |
| **Franja de patrocinadores en movimiento** | WCAG 2.2.2: algo que se mueve más de 5 s necesita **botón de pausa visible**; pausar al pasar el mouse no basta | Metaobjeto Sponsor + CSS; agregar botón Pause; reduce-motion = fila estática | MO + JS | $0 |
| **Correos con voz del tractor** | Shopify Email (carrito abandonado) y Notificaciones (Liquid) sí se editan. **La nota del paquete no**: Printify imprime y empaca desde su proveedor; la hoja de embalaje de Shopify solo sale si la tienda imprime y empaca | Carrito abandonado y Shipping confirmation: sí, con voz del tractor y pie con pista "3208". Nota del paquete: confirmar con Printify si permite inserto o nota personalizada; si no, quitar la promesa de la página 3208 y del pendiente #30 | NAT | Shopify Email: 10,000 correos al mes gratis, luego aprox. US$1 por cada 1,000 (verificar) |
| **The Evil List con doble confirmación** | Ninguno | Formulario de cliente con etiqueta `evil-list`; doble confirmación en Notificaciones de clientes; segmento en Shopify Email | NAT | $0 |
| **Formularios Sponsors, Book y Contact** | Todos llegan como correo al correo del remitente de la tienda (hoy Gmail). Sin archivos adjuntos. Spam | `form 'contact'` con campos extra y asunto distinto por formulario; hCaptcha nativo; cambiar el correo cuando exista el del dominio. El kit de patrocinio "within 2 business days" es manual (pendiente #2) | NAT | $0 |
| **Pit Log: contadores por etiqueta, Load more, buscador solo del Pit Log, 200 entradas** | Liquid no puede contar etiquetas sobre cientos de artículos en una sola carga; la búsqueda nativa busca en todos los blogs | Contadores desde **Season stats** (una fuente, ver 4). Filtros = `/blogs/pit-log/tagged/<tag>`. Load more = Section Rendering API de la página siguiente. Buscador: `/search?type=article&q=` y filtrar en el resultado por blog | NAT + JS | $0 |
| **Galería `?event=handle`** | Liquid no lee parámetros de la URL | Filtro en JS + páginas propias por álbum (metaobject web pages) para SEO | MO + JS | $0 |
| **Spotify y YouTube** | Iframes de terceros pesan y ponen cookies | Fachada: imagen + botón; el iframe carga al hacer clic | JS | $0 |
| **Last updated en todo** | No hay fecha automática de edición de metaobjetos ni de settings | Campo `updated` en cada metaobjeto y setting de fecha en cada sección; las que sí son automáticas: Pit Log (artículo más nuevo) y Galería (álbum más nuevo por fecha) | MO | $0 |
| **Temporada en un solo ajuste** | Ninguno | Setting global `season`; los textos usan `[season]` reemplazado en Liquid | NAT | $0 |
| **FAQ con 62 preguntas** | Límite de 50 bloques por sección | Una sección por categoría o metaobjeto FAQ item | NAT / MO | $0 |
| **Texto largo con fotos al margen** | El editor de texto enriquecido no deja asignar clases a cada foto | Sección con bloques (párrafo, foto con posición, cita, título con año) | NAT | $0 |
| **Tienda vacía "Coming soon"** | Ninguno | Condición en Liquid | NAT | $0 |
| **Shopify Flow** (sin skill: se diseñan como disparador, condiciones, acciones) | | 1) Feed The Beast: Pedido creado → línea con SKU BEAST → etiqueta `tip` al pedido. 2) Reposición: Inventario de variante cambió → antes 0 y ahora más de 0 → correo interno a la dueña con el handle (para mandar el aviso a `notify-<handle>`). 3) Cierre de Special edition: Programado diario → productos con etiqueta `special-edition` y `end_date` pasada → ocultar del canal o inventario 0 + correo interno. 4) Stock bajo en ediciones con inventario: Inventario de variante 5 o menos → correo interno | NAT (Flow) | $0 |

---

## 4. Lo que falta antes de construir (bloqueadores)

Prioridad: **P0** bloquea construir o probar; **P1** bloquea publicar; **P2** se puede llenar después de publicar.

| # | Prioridad | Qué falta | Dónde aparece | Quién lo da |
|---|---|---|---|---|
| 1 | P0 | **Productos reales en Printify**: nombres, diseños, mockups, tipos de producto (para colecciones automáticas), nombres de opción iguales ("Color", "Size"), precios. Todo el catálogo del boceto es de ejemplo y todos los precios dicen $XX | Shop, producto, home, carrito, búsqueda, limited, machine | Dueña + equipo (montaje en Printify, pendiente #12) |
| 2 | P0 | **Monto de envío gratis y escalones** (envío gratis, sticker de regalo) y revisar que nunca cuadre justo (#13, #27) | Anuncio, carrito, producto, FAQ, políticas | Dueña |
| 3 | P0 | **Confirmaciones de Printify**: "ships in 5 days", "printed in the USA", devoluciones (misprints 30 días), si incluye nota o inserto en el paquete, si se puede llevar inventario para run size, compatibilidad con bundles | Producto, FAQ, políticas, correos, limited | Dueña con Printify |
| 4 | P0 | **Sponsor stats: ¿5,000+ fans es por pull o por temporada?** Si es por temporada, la frase "100,000+ fans" está mal en home, Sponsors, Story y full story | Home, Sponsors, Story, the-full-story | Chris |
| 5 | P0 | **Decidir una sola fuente para los contadores** (hoy hay tres: Season stats en home y Story, etiquetas del Pit Log en log, Pull events en Schedule; pueden no coincidir). Recomendación: Season stats manda | Home, Story, Pit Log, Schedule, Book | Dueña (decisión) |
| 6 | P0 | **Crew Pack**: ¿dos playeras o playera + gorra? (el boceto dice "Tee plus cap") y el ahorro "$X" | Producto, carrito, shop | Dueña |
| 7 | P0 | **Feed The Beast**: montos ($1, $2, $5 en la nota del carrito; "$1 a $5" en pendientes) y texto legal; tratamiento fiscal | Carrito | Dueña + contador |
| 8 | P0 | **Medidas reales por estilo** (todas en XX) y tela por prenda ("XX% cotton, XX oz") | Size guide, dialog de producto, Details | Equipo desde el catálogo de Printify |
| 9 | P1 | **Exhibiciones: ¿3 o 4?** Fecha, lugar, liga, resultado, fotos y video de cada una (#24) | Schedule, Pit Log, Gallery, Story, Book, the-full-story | Dueña |
| 10 | P1 | **Monroe**: fecha, resultado y si fue el primer pull (si sí, una sola entrada) | Schedule, Pit Log, Gallery | Dueña / Chris |
| 11 | P1 | **Fecha del primer pull** (la historia larga dice agosto de 2026) y números reales de Season stats (2 competencias, 3 exhibiciones puestos de prueba) | Story, Pit Log, home | Dueña |
| 12 | P1 | **Black Smoke Guarantee**: plazo (12 meses propuesto), qué cubre el proveedor y quién paga después de 30 días, términos (`[terms pending]`) | Producto, FAQ, Refund policy | Dueña + abogado |
| 13 | P1 | **Revisión legal de todas las políticas**; nombre legal del negocio (¿LLC?) (`[name pending]` en Policies) | Policies, footer, checkout | Dueña + abogado |
| 14 | P1 | **Proveedor de correo** en Privacy (`[name pending]`): si es Shopify Email, decirlo | Policies | Dueña (decisión) |
| 15 | P1 | **Correo con dominio propio** (#23) y autenticación del dominio (SPF/DKIM) para Shopify Email; luego cambiar correo del remitente, políticas y notificaciones | Políticas, notificaciones, formularios | Dueña + quien maneje el dominio |
| 16 | P1 | **Porcentaje de EVIL3208** (#31) y si combina con otros descuentos | 3208, correos | Dueña |
| 17 | P1 | **Spec sheet [pending]**: Front tires, Wheelbase, Rear axle, Clutch, Build hours; confirmar "most Pro Stock tractors run an inline six" | The Machine, FAQ | Chris |
| 18 | P1 | **Decal zones**: tamaño de cada zona ("XX x XX in") y paquete de cada una ("To confirm"); reglas de NTPA y PPL sobre zonas reservadas | Sponsors | Chris |
| 19 | P1 | **Book the team [pending]**: espacio, acceso del tráiler, anticipación, si cobran viaje | Book | Chris |
| 20 | P1 | **Videos**: el del rayo (y su duración real "0:XX") y el del arranque ("Hear it") | Home, Story, Machine | Dueña |
| 21 | P1 | **Link de Instagram** (TikTok y YouTube no existen: no se muestran) | Footer, Contact | Dueña / Daniela V. |
| 22 | P1 | **Fotos faltantes**: Diesel Ross, Monroe, exhibiciones, merch real, imagen de cada colección (fotitos), fondo de tormenta en buena resolución, PNG limpio del recorte (sin árbol ni gente al fondo) | Story, Gallery, Shop, hero | Dueña |
| 23 | P1 | **Link de la playlist de Spotify** | Story | Dueña |
| 24 | P1 | **Decisión de reseñas** (instalar Judge.me, plan, moderación) y **app de reposición** (sí o no) | Producto | Dueña |
| 25 | P1 | **"Why are you here?" en Sponsors**: ¿se queda? (la nota lo pregunta) | Sponsors | Dueña |
| 26 | P1 | **Nombre del menú**: "Book us" (barra del boceto y menú) contra "Book the team" (footer y página) | Header, footer | Dueña |
| 27 | P1 | **Texto de Accessibility** y de Your Privacy Choices | Policies | Dueña + abogado |
| 28 | P1 | **Handles y redirecciones 301**: `/pages/spec-sheet` → The Machine, `/pages/about` → Our Story, página del team → Story#crew; mantener `/pages/schedule`, `/pages/sponsors`, `/pages/contact` | SEO | Equipo (con visto bueno de la dueña) |
| 29 | P2 | Estrategia de correos: tiempos y descuento del carrito abandonado, segunda vuelta (#1, #29) | Correos | Dueña |
| 30 | P2 | Kit de patrocinio PDF (#2), kit de prensa (#16) | Sponsors | Dueña |
| 31 | P2 | Pop up de descuento (#15), suscripción (#3), blog de SEO (#4), modelo 3D (#11) | No bloquean | Dueña |
| 32 | P2 | Apps de carrito (#26) cuando haya ventas | Carrito | Dueña |

Inconsistencias de texto detectadas al cruzar fuentes (resolver antes de cargar contenido):
- `PROMPT-MAESTRO.md` (v7) todavía dice "Hook Alerts", "Horsepower" y "No exhibitions"; manda `PENDIENTES.md`: The Evil List, "Unknown", y ya hubo exhibiciones.
- `_brief-v7.md` dice "This is f#cking evil"; el boceto y las decisiones usan "This thing is f#ck!ng evil" (6 veces, consistente). Queda esta última.
- `_real-content.md` dice Horsepower "CLASSIFIED"; la decisión es "Unknown".
- La nota de `editar.html` lista los tipos de metaobjeto sin Sponsor, Booking option ni Album.
- La nota del carrito dice "Crew Pack con Shopify Bundles"; ver riesgo con Printify en 3.

---

## 5. Riesgos técnicos y de rendimiento, y orden de construcción

### 5.1 Riesgos

**Seguridad del tema en vivo y de la tienda**
- Trabajar solo con `shopify theme dev --theme <id del borrador>` y `shopify theme push --theme <id>`; nunca `--live` ni `--allow-live`. Confirmar el ID antes de cada push.
- **Lo que no es del tema afecta al sitio en vivo de inmediato**: banner de cookies, cuentas nuevas, notificaciones, envío gratis, descuentos, políticas, marca del checkout, apps con app embed, páginas y blog publicados. Las páginas nuevas (`/pages/gallery`, `/pages/3208`, `/blogs/pit-log`) quedan visibles en el vivo con la plantilla por defecto del tema actual. Plan: crear páginas y blog al final o con visibilidad oculta hasta el lanzamiento, menús nuevos (`main-menu-v14`) sin tocar los del vivo, y todos los cambios de configuración en una lista para el día de publicación.
- Printify vuelve a publicar títulos y descripciones al editar en su panel; lo propio del sitio va en metacampos.

**Imágenes**
- Las 11 fotos del boceto pesan 69 a 252 KB cada una (1.9 MB la carpeta); en Shopify la dueña subirá originales pesados. Siempre `image_url` con `widths` y `sizes`, `loading="lazy"` fuera de la primera pantalla, `fetchpriority="high"` solo en el LCP. Shopify sirve WebP/AVIF solo.
- Galería con cientos de fotos: miniaturas de 400 px, tandas de 24, visor que pide el tamaño grande solo al abrir.
- Logos SVG de 28 KB cada uno (tres): pasar por SVGO; el del hero es candidato a LCP.
- Recorte del tractor: exportar el PNG limpio (sin árbol ni gente, como pide el comentario del hero).

**Hero animado**
- `hero.js` 16.6 KB + `hero.css` 14.8 KB + rig SVG en línea (9.7 KB). Cargar solo en la home (`{% if template.name == 'index' %}` o con la sección), `defer`.
- La animación espera hasta 2.5 s al recorte: no debe retrasar el LCP (el LCP debe ser el logo o el título, pintado sin JS).
- En el editor de temas las secciones se vuelven a pintar: el JS debe escuchar `shopify:section:load` y `shopify:section:unload` y limpiar `requestAnimationFrame`, si no, se duplican animaciones.
- Ya respeta `prefers-reduced-motion`, pausa fuera de pantalla y tiene botón Pause: conservarlo.

**JS por página**
- `hm.js` pesa 58.8 KB y mezcla de todo: catálogo de ejemplo, generador de playeras SVG, barra del boceto, demo de patrocinadores, banner de cookies falso. En Shopify se parte: `hm-core.js` (header, cajones, anuncios, foco) global y uno por función (`hm-cart.js`, `hm-pdp.js`, `hm-schedule.js`, `hm-gallery.js`, `hm-anatomy.js`, `hm-hero.js`), cada uno cargado solo por su sección.
- El CSS de cada página está en línea en el HTML (por eso product.html pesa 86 KB). Pasar a `{% stylesheet %}` de cada sección o a un asset por sección.

**Core Web Vitals (meta: LCP menor a 2.5 s, CLS menor a 0.1, INP menor a 200 ms en móvil)**
- Tipografía: el boceto usa **Archivo variable con eje de ancho** desde Google Fonts; el tema en vivo usa Anton y Barlow. Autohospedar Archivo en `assets/` como WOFF2 con subconjunto latino, `preload` de una sola variante y `font-display: swap` con métricas de respaldo para evitar CLS.
- Scripts de apps (Judge.me, reposición): cargar diferido; revisar su peso en Lighthouse.
- Spotify y YouTube con fachada.
- CLS: alturas fijas para la barra de anuncios rotativa, el esqueleto, la franja de patrocinadores y el reloj de Special edition.
- Caché: todo lo que depende de "hoy" se decide en el navegador (próximo pull, estados de la edición especial, Last updated con semáforo).
- Liquid: los bucles sobre metaobjetos y artículos tienen límite por página; con muchas entradas (Pit Log con 200, galerías grandes) paginar y cargar por Section Rendering API.

**Accesibilidad (WCAG 2.2 AA)**
- Botón de pausa visible en la franja de patrocinadores (falta en el boceto) y en la cinta amarilla si dura más de 5 s.
- Foco atrapado y devuelto en carrito, menú móvil, quick add, Notify me, dialogs de talla y visor (Dawn ya trae base).
- Anatomía y mapa de calcomanías operables con teclado y con texto equivalente (lista).
- Calendario del Schedule con semántica de tabla o grid y alternativa en lista (ya existe).
- Contraste del amarillo de seguridad con texto y de los textos "muted".
- Área táctil mínima de 24 px (criterio 2.5.8 de 2.2) en puntos de carrusel, flechas de tarjeta y chips.
- Errores de formularios anunciados (`aria-live`), etiquetas visibles.
- El widget de Judge.me y el banner nativo de cookies se revisan con axe al final.

**Límites del editor de temas**
- 25 secciones por plantilla y 50 bloques por sección (por eso el FAQ se parte). Esquemas JSON grandes hacen lento el editor: preferir metaobjetos para listas largas.

### 5.2 Orden de construcción por fases

| Fase | Qué se hace | Criterio de aceptación |
|---|---|---|
| **F0 Preparación** | Confirmar ID del borrador; repo git con el tema descargado; Theme Check; script de definiciones de metaobjetos y metacampos | `shopify theme list` muestra el borrador sin publicar; ningún comando usa `--live`; Theme Check sin errores en la base |
| **F1 Base visual** | `layout/theme.liquid`, tokens y `hm.css` limpio (sin barra del boceto ni notas), fuentes autohospedadas, header, anuncios, mega menú, menú móvil, búsqueda predictiva, footer, carrito con descuento, tarjeta de producto | Navegación completa con teclado; carrito AJAX suma, quita y aplica un código real; Lighthouse móvil de una página vacía 90+ en rendimiento y 100 en accesibilidad |
| **F2 Datos** | Crear definiciones (sección 2), colecciones automáticas, blog Pit Log con etiquetas, menús v14, páginas en oculto, cargar entradas reales que ya existen (crew, tiers, placements, partes, Monroe) | Cada metaobjeto tiene acceso de Storefront; una entrada nueva aparece en el tema sin tocar código; nada nuevo es visible en el sitio en vivo |
| **F3 Tienda** | Shop (colección + filtros S&D), producto (galería, talla obligatoria, guía, Notify me, garantía, acordeones, relacionados), Special edition, search, tienda vacía, 404 | Compra de prueba con código de 100% y con Shop Pay en modo prueba; producto Coming soon no se puede comprar ni por URL; tienda vacía muestra Coming soon; filtros de talla y color funcionan con productos reales de Printify |
| **F4 Equipo y contenido** | Home con hero, The Machine, Our Story, full story, Schedule (lista, calendario, .ics), Pit Log (Featured, Load more, filtros), Gallery (álbumes y visor) | El hero pasa Lighthouse móvil (LCP menor a 2.5 s, CLS menor a 0.1) y se pausa; el próximo pull cambia solo al pasar la fecha; .ics abre en Google, Apple y Outlook; 200 artículos de prueba no rompen el Pit Log |
| **F5 Patrocinio y contacto** | Sponsors (todas las secciones, franja global), Book, The Evil List, Contact, FAQ, Size guide, Policies, 3208 | Agregar un Sponsor lo muestra en Sponsors y en la franja; los tres formularios llegan al correo correcto con todos los campos; 3208 no aparece en búsqueda ni sitemap; FAQPage válido en la prueba de resultados enriquecidos |
| **F6 Configuración (lista para el día de lanzamiento)** | Cuentas nuevas, banner de cookies, notificaciones con voz del tractor, Shopify Email (carrito abandonado, Evil List), envíos y envío gratis, impuestos, políticas, descuentos (EVIL3208, Crew Pack), Judge.me, app de reposición si se aprueba, Flows | Pedido de prueba real con Printify: llega el correo de envío con guía; el banner aparece en EE. UU.; Cookie Preferences lo reabre |
| **F7 QA** | Theme Check, Lighthouse móvil por plantilla, axe, teclado, celulares reales (iOS y Android), editor de temas (agregar, ocultar y mover bloques), JSON-LD, redirecciones 301, sitemap | Cero errores de Theme Check; todas las plantillas con CWV en verde; sin "[pending]", "XX", "Example" ni "Ejemplo" visibles; redirecciones probadas |
| **F8 Publicación** | Revisión legal firmada, publicar el borrador, aplicar la lista de F6, Search Console | El tema anterior queda como respaldo sin borrar; monitoreo de pedidos y Search Console la primera semana |

---

## 6. Cosas del boceto que NO van al sitio

- **Barra amarilla superior** ("Boceto v27 · no es el sitio en vivo" con links a todas las páginas, "Ver esqueleto" y "Ocultar notas").
- **Todas las notas** `<p class="note">`, `.sp-owner`, `.st-ctl` y la sección `g-how` de la Galería.
- **Paneles "Solo para la dueña"** de Schedule y Pit Log (formularios `adm-form` que simulan el admin).
- **Toggles y controles de demo**: estado de la edición especial (Coming soon / Live / Sold out), botones +/− de contadores en Story, mostrar/esconder lugares y marcar Title / Pit / Crew en Sponsors, Available / Limited / Sold out / Hidden de Pit Partner, "Ver con ejemplos / Ver vacío" de patrocinadores, selector de foto por tipo del Pit Log, "Probar tienda vacía" (`?empty=1`), "Ver esqueleto lento" (`?loading=slow`), `?next=1`, `?imgs=3`, `?imgs=1`, "Probar con 200 entradas", "producto sin reseñas / con reseñas", "Coming soon · Sold out · Only 4 left".
- **Datos de ejemplo**: catálogo completo de `hm.js` (nombres, "$XX", "Save $X"), reseñas de ejemplo (Evil One Tee 4.8 con 23, etc.), patrocinadores "Example Title Co." y demás, cuenta de "Jane" con pedidos y "123 Example St", fechas de muestra del calendario, pulls "County fair pull" y "Season finale pull", entradas "Example" y "Test day" del Pit Log, álbum "Test days" de muestra, edición "Edition name" del archivo, entrada de ejemplo "Pit passes" de Logo placement, la muestra de correo de The Evil List si no se reemplaza por una real.
- **Mockups SVG de prendas** generados por `hmMock` (sirven solo como marcador; en el sitio van fotos de Printify o, mientras tanto, los íconos de `img/icons` subidos como imagen temporal, como dice editar.html).
- **Simulaciones**: banner de cookies propio (se usa el nativo), validación falsa del cupón, botón de checkout que dice "Boceto: aquí abre el checkout", barra de envío que avanza 30% por artículo, guardado en localStorage de "Ya lo actualicé" y del calendario anual.
- **Marcadores visibles**: "[pending]", "[name pending]", "[terms pending]", "XX", "0:XX", "$XX", "Example", "Ejemplo", "Foto por tipo", "Photo soon" (en el sitio, una fila sin dato no sale y una foto faltante usa respaldo).
- **Páginas internas**: `editar.html` (va como manual de la dueña) y `correos.html` (va como configuración en el admin).
- **Archivos de trabajo**: `_brief*.md`, `_real-content.md`, `_story-original.txt`, `_story-v25.md`, `_rig.svg` (su contenido ya vive en `snippets/hm-rig.liquid`), y los comentarios "Hallmark · pre-emit critique".
- **Google Fonts por CDN** del boceto (se autohospeda).
