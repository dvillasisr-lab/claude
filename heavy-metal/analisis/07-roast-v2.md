# 07 · Roast del boceto v2 (Heavy Metal "The Evil One")

Fecha: 01/10/2026 · Archivos revisados: `heavy-metal/boceto-v2/` (index, shop, product, machine, story, schedule, sponsors, hm.css, hm.js, _brief.md) contra el tema real en `analisis/tema/` y las fotos de `capturas/`.

Método: lectura completa del código, render con Playwright (Chromium, fuentes de Google bloqueadas) a 1440x900 y 390x844, pruebas de clic (mega menú, carrito, anclas, filtros, menú móvil) y medición de alturas de sección, tamaños de títulos, ids duplicados y enlaces muertos. Reglas aplicadas: Hallmark (modo audit), Web Interface Guidelines (Vercel), CRO y SEO audit de la biblioteca de marketing.

Nota: lo legal de este documento es una lista de lo que una tienda de EE. UU. suele necesitar, no asesoría legal. Validar con un abogado antes de publicar.

---

## Veredicto en corto

El v2 resolvió lo que pidió la dueña la vez pasada (tienda clara, multipágina, muchos productos), pero lo hizo con una plantilla genérica de "tienda de moda" que ignora casi todo lo real que ya existe: 13 personas del equipo con nombre y rol, 10 fotos reales, un video de YouTube de una jalada real, precios reales de patrocinio, la animación del tractor y la promesa "Ships in 5 days". En su lugar puso placeholders, inventó beneficios de patrocinio y escondió la información detrás de títulos de 112 px. Además trae bugs que en vivo costarían ventas: el carrito vacío no dice que está vacío en Shop, "Quick add" mete talla M sin preguntar, "Ride With The Evil One" pierde el nombre que escribe el fan y el footer no tiene ni una sola política legal que funcione.

Puntuación Hallmark (1 a 5): Filosofía 3 · Jerarquía 2 · Ejecución 3 · Especificidad 2 · Contención 2 · Variedad 2. El sello de cada página dice `P4 H4 E4 S4 R5 V4` (index.html:6, shop.html:6): **el sello miente** (hallazgo crítico de Hallmark).

Conteo: **19 críticos · 30 mayores · 22 menores** (más la verificación de los 23 puntos de la dueña).

---

## Parte A · Los 23 puntos de la dueña, verificados

| # | Lo que dijo | ¿Se confirma? | Evidencia | Fix para v3 |
|---|---|---|---|---|
| 1 | Títulos y elementos muy grandes | Sí | `--t-hero: clamp(2.75rem,8vw,7rem)` (hm.css:23) = **112 px** en el h1 de Machine, Story, Schedule y Sponsors a 1440; `.h1` 64 px; cada `.h2` 40 px (medido). Captura schedule 1440: la palabra "SCHEDULE" ocupa medio viewport | Escala tipo SKIMS: h1 de página 28 a 40 px, h2 de sección 20 a 28 px, etiquetas 11 a 12 px. Borrar `.h-hero` de páginas internas; solo el hero de la home puede pasar de 48 px |
| 2 | Secciones se cortan y desperdician espacio | Sí | `--sect: clamp(48px,7vw,96px)` (hm.css:28) da 96 px arriba y abajo a TODAS las secciones; la cabecera apilada (barra boceto + anuncio + header) mide 131 px en desktop y 191 px en móvil. Home: 4,962 px de alto en desktop y 6,165 px en móvil | Módulos de alto fijo: cada sección de home cabe en `100svh - header` o en media pantalla. Padding de sección 40 a 56 px. Anuncio de 32 px y header de 56 a 60 px |
| 3 | Logo a la IZQUIERDA | Sí | `.hdr__in` usa `minmax(0,1fr) auto minmax(0,1fr)` (hm.css:91): el logo queda centrado (x = 628 px a 1440). En móvil queda entre hamburguesa y carrito | Grid `auto 1fr auto`: logo a la izquierda, menú junto al logo o centrado, iconos a la derecha (patrón skims-mexico) |
| 4 | Hero sin la animación del tractor | Sí | index.html:59-68 es un placeholder estático 4:3. El tema tiene `sections_hm-hero.liquid` (speedlines, tacómetro, contador de pies, riel 0 a 300 ft, bandera) y `snippets_hm-rig.liquid` (tractor y sled en SVG con humo, llantas girando y wheelie) | Ver Crítico C1 |
| 5 | Categorías y best sellers en una sola sección del alto de la pantalla | Sí | "Shop by category" mide 501 px y "Best sellers" 850 px = 1,351 px, contra 769 px útiles (900 menos 131 de cabecera) | Un solo módulo: fila de miniaturas de categoría tipo kyliecosmetics (círculos o cuadros de 96 a 120 px con nombre debajo) y debajo UNA fila de 4 best sellers con foto 4:5 más baja. Meta: cabe completo a 1440x900 |
| 6 | La home salta de tema y tiene demasiado merch | Sí | Orden real: categorías (index.html:73) → best sellers (84) → banda de la máquina (129) → new drop (141) → Ride (185) → More (203). Son 8 productos más 6 categorías, con la banda oscura partiendo dos filas de producto | Home v3: Hero animado → Shop (categorías + 1 fila) → La máquina (banda) → Video real → Ride/Patrocinio (bloque compacto) → Hook Alerts. Una sola fila de producto en toda la home |
| 7 | "Ride With The Evil One" muy grande | Sí | Sección de 606 px (desktop) y 735 px (móvil), foto 4:3 a media pantalla, h2 de 40 px (index.html:185-201) | Tarjeta horizontal de 180 a 220 px de alto, o tarjeta dentro de la fila de producto (ya es un producto). Su detalle vive en su propia ficha |
| 8 | Footer sin políticas legales | Sí | hm.js:81: columna Help con Shipping, Returns, Size guide y Contact, todos `href="#"`. No hay Privacy, Terms, Refund, Accessibility ni "Your privacy choices". El tema real sí enlazaba Privacy, Shipping y Returns (`sections_hm-footer.liquid`, bloque HELP) | Ver Crítico C5 |
| 9 | Copyright exacto | Sí | hm.js:83 dice `© 2026 Heavy Metal Pro Stock · Waterloo, WI` | `© 2026 Heavy Metal Pro Stock: The Evil One · Waterloo, WI`, con el año de `{{ 'now' \| date: '%Y' }}` |
| 10 | New drop, categorías y best sellers mandan a la home | Sí (causa distinta en local) | Todos son anclas `shop.html#new`, `#best`, `#tees` (index.html:64,72-79,86,143; hm.js:48-50). `fromHash()` solo filtra categorías (shop.html:257 y 303): `#new` y `#best` NO filtran, caen en "Shop all" con 14 productos y bajan 325 px. En el artifact publicado el visor solo pasa anclas simples, así que el enlace cae en la página base | Cada destino es una URL real de colección: `/collections/new-drop`, `/collections/best-sellers`, `/collections/tees`, etc. Nada de anclas entre páginas |
| 11 | Dos fotos del mega menú | Justificada la duda | hm.js:50-51: una repite "New drop" (mismo destino que el link de al lado) y la otra va a `index.html#ride`, que no es un producto. Ocupan 2/3 del panel con placeholders | Quitar las dos fotos grandes. Mega menú tipo SKIMS: columnas de texto + una fila de 5 o 6 miniaturas de categoría (kylie). Máximo UNA tarjeta promocional editable (bloque) |
| 12 | Referencias SKIMS / Kylie | Pendiente | El v2 tomó el grid pero no la escala tipográfica, el logo a la izquierda, el footer con políticas ni las miniaturas de categoría | Ver Parte C (patrones a copiar) |
| 13 | "Our Story" no convence | Sí | 6 tarjetas "Crew member (placeholder)" (story.html:245 en adelante), video placeholder (story.html:182), dos capítulos ocupan 1,453 px; 7,654 px de alto total | Ver Mayor M14 |
| 14 | Al hacer clic la página no abre arriba | Sí | 18 enlaces entre páginas llevan ancla (`grep` en index, hm.js, machine, story, sponsors); `html{scroll-behavior:smooth}` (hm.css:32) más `[id]{scroll-margin-top}` (hm.css:39). Prueba: clic en "Tees" desde la home abre Shop en `scrollY = 325` con h1 "Shop all" | URLs reales sin ancla; `scroll-behavior:smooth` solo dentro de la página (TOC de Story); en Shopify se navega con páginas completas y abre arriba |
| 15 | Schedule: mucho espacio, letra enorme, falta información | Sí | h1 112 px (schedule.html:92), 4,871 px de alto en desktop y 6,500 en móvil para decir "no dates yet"; 3 tarjetas de ejemplo con XX ocupan 779 px (schedule.html:185-209) | Ver Crítico C9 |
| 16 | Demasiados CTA, confunde | Sí | La home tiene 12 botones visibles; existen DOS listas distintas: "Join" del footer (hm.js:78, "drops and Hook Alerts") y "Hook Alerts" (schedule.html:133), más el anuncio (hm.js:33), Ride en home, Ride en carrito y Sponsors. Schedule repite "Follow on Facebook" dos veces | Una sola lista ("Hook Alerts & drops") con un solo formulario reutilizable; un CTA primario por página (Ver Mayor M1) |
| 17 | Falta aviso de cookies | Sí | No existe banner ni enlace de preferencias en ningún archivo | Ver Crítico C6 |
| 18 | Schedule editable sin código | No resuelto | Solo una nota (schedule.html, nota de "metaobjeto") | Metaobjeto `pull_event` (Crítico C10) |
| 19 | Sponsors tarda en llegar a la info | Sí | 9 secciones; el formulario empieza en 6,597 px (desktop) y 9,572 px (móvil, de 11,544 px totales). Los niveles están en 3,330 px | Ver Crítico C11 |
| 20 | Search manda a Shop all | Sí | hm.js:42 `href="shop.html"`; y en móvil Search ni existe (hm.css:102 lo oculta y el menú móvil no lo tiene) | Ícono de lupa siempre visible que abre buscador predictivo (Shopify Predictive Search) y página `/search` con resultados |
| 21 | El orden (Sort) podría ser mejor | Sí | shop.html:77: solo Featured, Best selling, Newest, A to Z. Falta precio. Los filtros duplican las píldoras (la categoría está en píldoras Y en el panel) y el estado no queda en la URL | Sort: Featured, Best selling, Newest, Price low to high, Price high to low. Panel con Size, Color, Price, Availability (Search & Discovery). Estado en la URL (`?filter.v.option.size=L`) |
| 22 | ¿Qué va en Account? | Sin definir | hm.js:43 `href="#"`; oculto en móvil | Ver Mayor M9 |
| 23 | Carrito bien, pero podría tener banners y bundles | Sí, y tiene bugs | Barra de envío fija al 40 % aun con carrito vacío (hm.js:63), el único upsell es Ride siempre (hm.js:66), sin cantidad ni quitar, Checkout no hace nada (hm.js:68) | Ver Crítico C3 y Mayor M7 |

---

## Parte B · Checklist priorizado

Formato: `[ ]` pendiente · **Dónde** · **Fix v3**.

### CRÍTICO (bloquea lanzamiento o rompe compra / ley)

- [ ] **C1. Hero de la home sin la animación del tractor.** index.html:59-68 (placeholder estático). El activo existe: `analisis/tema/sections_hm-hero.liquid` y `snippets_hm-rig.liquid`, con distancia objetivo editable (`target`, 150 a 400 ft).
  **Fix v3:** hero claro de ancho completo, ~70 a 80 vh: a la izquierda logo/titular corto ("The Evil One · Full Pull or Nothing") + 1 CTA primario "Shop the drop" + 1 secundario "Watch it pull"; a lo ancho, la pista con el rig SVG avanzando, el riel de pies (0 / 100 / 200 / 300 FT) y el chip "PULLING… / FULL PULL!". Mejoras sobre el original: versión clara (tierra y negro mate sobre fondo concreto), usar la silueta real `capturas/hm-tractor-cutout.png` como referencia del perfil, una sola pasada de ~6 s y queda quieto en "FULL PULL!" (WCAG 2.2.2: todo lo que se mueve más de 5 s necesita pausa), botón de pausa, versión estática con `prefers-reduced-motion`, sin parpadeo del tacómetro, todo en CSS `transform` (nada de JS por frame). Editable en el tema: tagline, CTAs, distancia, marquee on/off.

- [ ] **C2. "Ride With The Evil One" pierde el nombre del fan.** index.html:195-196: el `data-add` está en el botón de submit; el listener global de hm.js hace `preventDefault()` y agrega el texto literal "Crew name", no lo que escribió el usuario. El upsell del carrito (hm.js:66) agrega el producto sin pedir nombre.
  **Fix v3:** ficha propia `/products/ride-with-the-evil-one` con campo obligatorio de "line item property" (`properties[Name on panel]`, máximo 24 caracteres, vista previa en el panel), checkbox de aceptación de reglas de moderación, y producto sin envío ("This is a service, nothing ships"). El carrito y el upsell mandan a la ficha, nunca agregan directo. Política propia: qué pasa si el nombre se rechaza (reembolso completo), cuánto dura (temporada 2026), foto de prueba, y que **no es donativo deducible**.

- [ ] **C3. Carrito vacío roto en Shop por id duplicado.** `id="empty"` existe en el drawer (hm.js:65) y en Shop (shop.html:212). El `render()` de Shop oculta el primero que encuentra, que es el del carrito: prueba Playwright con 0 artículos, el drawer no muestra "Your cart is empty" (captura `drawer-shop-empty`). Además la barra dice "$XX away from free US shipping" al 40 % con el carrito vacío.
  **Fix v3:** ids únicos con prefijo (`cart-empty`, `plp-empty`); estado vacío real del carrito (mensaje + 3 categorías + best seller); barra de envío calculada con el subtotal y oculta si el carrito está vacío.

- [ ] **C4. "Quick add" compra la talla M sin preguntar.** Todas las tarjetas: `data-add="Evil One Tee|Matte Black / M|$XX"` (index.html:92 y siguientes, shop.html:85 y siguientes). En pantallas táctiles el botón ni existe (hm.css:138).
  **Fix v3:** Quick add abre un mini selector de talla (desktop: chips de talla sobre la foto; móvil: hoja inferior con tallas y color). Productos de talla única sí pueden agregar directo. Esto evita devoluciones por talla en un negocio de impresión bajo demanda, donde devolver es caro.

- [ ] **C5. Footer sin ninguna política legal y con enlaces muertos.** hm.js:81 (`href="#"` en Shipping, Returns, Size guide, Contact), hm.js:83 (copyright incorrecto). El tema actual sí tenía `shop.privacy_policy.url`, `shop.refund_policy.url`, `shop.shipping_policy.url`.
  **Fix v3:** franja legal inferior (patrón SKIMS) con: Privacy Policy · Terms of Service · Refund Policy · Shipping Policy · Contact Information · Accessibility · Your Privacy Choices · Cookie preferences. Las primeras cinco se generan en Shopify (Settings > Policies) y se enlazan con `shop.*_policy.url`; Accessibility es una página. Copyright: `© 2026 Heavy Metal Pro Stock: The Evil One · Waterloo, WI`. Íconos de pago (`shop.enabled_payment_types`).

- [ ] **C6. Sin aviso de cookies ni "Your privacy choices".** No hay banner en ningún archivo.
  **Fix v3:** activar el banner nativo de Shopify (Settings > Customer privacy) para EE. UU. con opción de exclusión ("opt out of sale/sharing") y respeto de la señal GPC; enlace "Your privacy choices" en el footer que abre la página de preferencias. El banner se ve en el boceto como franja inferior compacta (no modal que tape la tienda), con "Accept", "Decline" y "Manage". Si se usan Meta Pixel o Google Ads, el banner es lo que permite hacerlo sin riesgo en California y en los estados con ley de privacidad.

- [ ] **C7. No hay Privacy Policy aunque el sitio recoge emails y teléfonos.** Formularios: footer (hm.js:78), Hook Alerts (schedule.html:133), Sponsors (sponsors.html:472), "Notify me" (product.html). El aviso SMS enlaza a "Privacy Policy" y "SMS Terms" con `href="#"` (schedule.html:163). La ley de California (CalOPPA) exige política de privacidad visible a cualquier sitio que recoja datos de residentes de California, sin importar el tamaño.
  **Fix v3:** Privacy Policy de Shopify adaptada (qué datos, para qué: pedidos, Hook Alerts, patrocinio; con quién se comparten: impresión bajo demanda, Klaviyo/Shopify Messaging), página "SMS Terms" y enlaces reales en cada formulario.

- [ ] **C8. SMS sin consentimiento completo y sin validación.** schedule.html:159-163: el checkbox está bien (desmarcado y "not a condition of purchase"), pero se puede marcar SMS sin teléfono y no hay validación; el footer pide email sin aviso de consentimiento ni enlace a privacidad y acepta el campo vacío (hm.js:78, el input no es `required`).
  **Fix v3:** un solo componente "Hook Alerts" con: email obligatorio, teléfono obligatorio solo si marca SMS, texto TCPA completo (nombre de la marca, frecuencia "about 1 per pull", "Msg & data rates may apply", STOP/HELP, enlaces a SMS Terms y Privacy), doble opt-in por SMS desde la herramienta (Shopify Messaging o Klaviyo) y registro del consentimiento. Los correos de marketing deben llevar dirección postal física (CAN-SPAM): pedir a la dueña dirección o apartado postal.

- [ ] **C9. Schedule sin información útil y sin el evento real que ya existe.** schedule.html:92 (h1 112 px), 185-209 (3 tarjetas falsas con XX). El tema tiene el video real `youtube.com/watch?v=HfJ5FAJJ5Ac` con el texto "Badger State Tractor Pullers 2026: Green County Fall Nationals in Monroe, WI!" (`templates_index.json`, sección video): eso ya es una jalada pasada de 2026.
  **Fix v3:** arriba del pliegue: estado ("Testing season 2026"), próxima jalada o "Next pull: TBA", formulario corto de Hook Alerts en línea. Debajo, lista compacta (tabla en desktop, lista en móvil) de "Upcoming" y "Past pulls" con: fecha, hora (CT), evento, ciudad y estado, liga, clase, enlace a boletos o al fair, cómo verlo (stream), resultado (pies o "DNF / ended early") y video. Primera fila real: Green County Fall Nationals, Monroe, WI, con el video (confirmar con la dueña la fecha exacta y que el video es de The Evil One). Botón "Add to calendar" (.ics) por evento. Sin tarjetas de ejemplo en vivo.

- [ ] **C10. Schedule no editable sin código.** Solo hay una nota.
  **Fix v3:** metaobjeto `pull_event` con campos: `date` (fecha), `start_time` (texto), `event_name`, `fair_or_venue`, `city`, `state`, `league` (lista: NTPA, PPL Badger State, Other), `class` (Pro Stock), `tickets_url`, `stream_url`, `result_ft` (decimal), `result_note` (Full pull, DNF, Ended early), `video_url`, `photo`, `status` (Upcoming, Done, Cancelled). La sección ordena por fecha y separa próximos y pasados sola. La dueña agrega una jalada en Content > Metaobjects, sin tocar el tema. Bonus: marcado `SportsEvent` automático por cada entrada.

- [ ] **C11. Sponsors: la información está a 7 a 11 pantallas de distancia y los niveles reales se reemplazaron por inventados.** Formulario en 6,597 px (desktop) y 9,572 px (móvil). El tema real (`templates_page.sponsors.json`) trae: TITLE PARTNER $25,000, PIT PARTNER $10,000, CREW SUPPORTER $5,000 con beneficios, "5,000+ fans in the stands" y 6 lugares de logo. El v2 inventó 4 niveles "Contact us" (sponsors.html:320-363) y beneficios que nadie aprobó: "Hospitality day at 2 events", "Tractor on display at your dealership, twice a year" (sponsors.html:327-328), cupones, reportes con KPIs. Eso rompe la regla de la casa "nunca inventar" y crea promesas contractuales.
  **Fix v3:** primera pantalla = h1 corto + 3 niveles reales en columnas con precio (o "From $5,000" si la dueña prefiere no publicar el monto exacto) + botón "Get the media kit" que abre el formulario en un panel o lo deja a la derecha (sticky en desktop). Segunda pantalla = mapa de calcomanías con la silueta real. Tercera = FAQ y formulario. Máximo 4 secciones. Todo lo inventado se borra o queda marcado como "por confirmar" fuera del sitio en vivo.

- [ ] **C12. Ninguna foto real; los placeholders piden fotos que no existen.** `capturas/` tiene 10 fotos reales (crew, driver, driver-crew, engine, front-smoke, front-white, grandstand, hero, rear, side) y el recorte `hm-tractor-cutout.png`. Todas son verticales 3:4 (1050x1400) de día en ferias. El v2 pide "fondo negro de estudio, 21:9" (machine.html:115), bandas 16:9 y "sin mostrar el turbo" (machine.html:168) cuando `hm-engine.jpg` ya muestra el motor.
  **Fix v3:** diseñar las bandas para fotos verticales (columnas 3:4 o 4:5, o dípticos), asignar cada foto real a su lugar (ver Parte D) y dejar placeholders solo para fotos de producto, que sí faltan.

- [ ] **C13. Search no busca.** hm.js:42 y oculto en móvil (hm.css:102).
  **Fix v3:** lupa en header siempre visible (también en móvil), panel de búsqueda predictiva (productos, colecciones, páginas) y plantilla `/search` con resultados, filtros y estado "No results for…" con sugerencias.

- [ ] **C14. Enlaces que no llevan a donde dicen.** Ver punto 10 de la Parte A. También "Put your name on the tractor" del mega menú y de Sponsors van a `index.html#ride` (hm.js:51, sponsors.html:432), no a un producto.
  **Fix v3:** mapa de URLs final (Parte C) y cero anclas entre páginas.

- [ ] **C15. Las URLs del sitio actual se pierden.** El tema actual usa `/pages/spec-sheet` (Machine) y `/pages/about` (Team) (`sections_header-group.json`); el v2 los renombra a "machine" y "story".
  **Fix v3:** o conservar esos handles, o crear redirecciones 301 en Navigation > URL redirects (`/pages/spec-sheet` → `/pages/the-machine`, `/pages/about` → `/pages/our-story`). Ya hay estrategia en `02-seo.md` 5.2.

- [ ] **C16. "Buy it now" no compra.** product.html:431: hace lo mismo que Add to cart.
  **Fix v3:** botón de pago dinámico de Shopify (Shop Pay / Apple Pay / Google Pay) que va directo a checkout.

- [ ] **C17. Promesas de envío y devolución sin base y contradictorias.** "Easy returns and exchanges within XX days" (product.html:221) y "ships in X to X business days" (hm.js:68), cuando el tema real dice "SHIPS IN 5 DAYS · Printed to order in the USA" (`templates_index.json`, trust_2). La regla de pedidos por correo de la FTC exige tener base razonable para el plazo prometido y avisar si se retrasa. En impresión bajo demanda normalmente NO se aceptan cambios por talla.
  **Fix v3:** confirmar con el proveedor de impresión y escribir UNA promesa en todos lados: tiempo de producción + tránsito, y la regla real de devoluciones (por ejemplo: "defects and misprints replaced free; no returns for size, check the size guide"). Decir "Printed in the USA" solo si es verdad; nunca "Made in USA" si la prenda viene de fuera (regla FTC).

- [ ] **C18. Sin página de contacto ni datos del negocio.** Footer Contact `href="#"`. El tema ya tiene `sections_hm-contact-page.liquid` (formulario nativo de Shopify, email, redes) con el email aún "[EMAIL PENDING]".
  **Fix v3:** página `/pages/contact` con email real, tiempo de respuesta ("within 2 business days", ya escrito en el tema), formulario con selector de tema (Order, Sponsorship, Ride With, Other), ciudad (Waterloo, WI) y la política "Contact information" de Shopify llena (nombre legal del negocio, email, teléfono o dirección).

- [ ] **C19. El sello de calidad no corresponde a lo que se entregó.** index.html:6 y shop.html:6 dicen `P4 H4 E4 S4 R5 V4`; la jerarquía (títulos de 112 px) y la especificidad (cero activos reales) están en 2.
  **Fix v3:** recalificar después de corregir; no publicar con sello.

### MAYOR (baja conversión, se ve genérico o rompe la experiencia)

- [ ] **M1. Un CTA primario por página.** Home: 12 botones visibles; Schedule duplica "Follow on Facebook"; Story termina con dos CTAs de igual peso.
  **Fix v3:** Home = "Shop the drop" · Shop = agregar al carrito · Producto = Add to cart · Machine = "Shop the machine" · Story = "Shop the drop" · Schedule = "Get Hook Alerts" · Sponsors = "Get the media kit". Lo demás pasa a enlace de texto.

- [ ] **M2. Plantilla repetida en todas las páginas internas** (huella estructural de IA según Hallmark): etiqueta gris + h1 gigante + lede + 2 botones a la izquierda y foto a la derecha en Machine, Story, Schedule y Sponsors; cada sección abre con "label muted + h2 + lede".
  **Fix v3:** cada página con su forma: Machine = foto vertical real con puntos encima y ficha técnica al lado; Story = línea de tiempo con fotos reales y el video; Schedule = tabla de eventos; Sponsors = niveles arriba. Encabezados de sección de una línea.

- [ ] **M3. Header y menú.** Mega menú solo abre con hover o foco (hm.js:96-99): en tablets de 961 a 1100 px, tocar "Shop" navega y el menú nunca aparece. Sin `aria-controls`. Escape del menú móvil no cierra; drawer y menú móvil son `aria-modal` sin trampa de foco.
  **Fix v3:** "Shop" es un botón que abre/cierra el panel en clic y teclado, con enlace "Shop all" dentro; trampa de foco y Escape en drawer, menú móvil y filtros; `overscroll-behavior: contain` en paneles.

- [ ] **M4. Menú móvil pobre.** Captura `mnav`: no tiene buscador, cuenta, Stickers & Gear, Ride, redes ni Hook Alerts; las categorías van debajo de las páginas del equipo.
  **Fix v3:** buscador arriba, luego Shop con miniaturas de categoría (2 columnas), luego The Machine / Our Story / Schedule / Sponsors, luego Account, Contact y redes.

- [ ] **M5. Ficha de producto sin lo esencial de una tienda grande.** product.html: en móvil el precio no se ve en la primera pantalla (captura `pdp-390-fold`); color no cambia las fotos; tabla de tallas con XX; sin talla del modelo ("Model is 6'0", wears L"); sin cuotas (Shop Pay Installments); sin fecha estimada de entrega; reseñas con "Write a review" `href="#"` (product.html:345); política "See our policy" `href="#"` (product.html:253); 3XL en la ficha pero no en el filtro de Shop.
  **Fix v3:** título, precio y badge sobre la foto en móvil o justo debajo con galería más corta; fotos por variante de color; medidas reales del proveedor; texto de ajuste; "Pay in 4 with Shop Pay" automático; "Order today, ships by [fecha]"; reseñas con app (Judge.me o Shopify Product Reviews) solo con reseñas reales; tallas coherentes entre ficha y filtros; tallas de niños explícitas (YS, YM, YL).

- [ ] **M6. Bundle "Crew Pack" sin selección de talla y sin lógica real.** product.html (Complete the look) agrega "Evil One Tee + Crew Cap" sin talla. El tema real define Crew Pack como "BOTH TEES, ONE PRICE: the Evil One tee and the Team tee" (`templates_index.json`), distinto al v2 (tee + cap).
  **Fix v3:** decidir con la dueña qué es el Crew Pack; implementarlo con Shopify Bundles (app gratis) para que cada pieza pida su talla; descuento automático visible en carrito.

- [ ] **M7. Carrito sin las piezas de una tienda top.** hm.js:60-68: sin cambiar cantidad, sin quitar línea, sin precio por línea, Checkout sin acción, sin íconos de pago, upsell fijo de Ride aunque ya esté en el carrito.
  **Fix v3:** líneas con +/-, quitar y propiedades (talla, color, nombre de Ride); barra de envío gratis real; banner editable arriba (bloque: texto + enlace, por ejemplo "Crew Pack saves $X"); recomendaciones de Shopify ("complementary products") con 2 o 3 artículos baratos (Sticker Pack, Koozie) para llegar al envío gratis; nota "Taxes calculated at checkout"; íconos de pago; botón Shop Pay express.

- [ ] **M8. Shop: filtros y orden.** Ver punto 21. Además "14 products" y el h1 siempre dicen "Shop all" aunque filtres por Tees.
  **Fix v3:** cada categoría es su colección con su h1 ("Tees", "Sweatshirts"…), su descripción corta (SEO) y miniaturas de categoría arriba (kylie). Grid 4/2 se queda; "You've seen 14 of 14" sirve cuando haya paginación.

- [ ] **M9. Account sin definir.** hm.js:43.
  **Fix v3:** usar las cuentas nuevas de Shopify (sin contraseña, código por email): pedidos y rastreo, recompra, direcciones, estado de mi "Ride With The Evil One" (nombre aprobado o no), preferencias de Hook Alerts (email/SMS) y enlace a "Your privacy choices". Visible como ícono en desktop y móvil.

- [ ] **M10. Sin 404 ni páginas de sistema.** No hay `404`, `/search`, `/cart`, páginas de políticas ni de "gracias".
  **Fix v3:** bocetar 404 (mensaje corto con la voz del equipo, buscador, 4 categorías y best sellers), resultados de búsqueda, carrito de página completa (respaldo del drawer) y plantilla de página legal (estilo de términos de SKIMS: índice lateral, texto de 16 px, 70 caracteres de ancho).

- [ ] **M11. SEO: títulos y descripciones.** index.html:1 `<title>Heavy Metal</title>`; index y shop sin `meta description`; ninguna página con Open Graph, canonical ni `theme-color`.
  **Fix v3:** Home: "Heavy Metal Pro Stock · The Evil One Tractor Pulling Team & Merch"; Shop: "Tractor Pulling Shirts, Hoodies & Hats · Heavy Metal Pro Stock"; colecciones con keyword ("Tractor Pull T-Shirts"); descripciones de 140 a 155 caracteres; imagen OG con el tractor real (`hm-hero.jpg`). En Shopify, `page_title` y `page_description` editables desde cada recurso.

- [ ] **M12. SEO: datos estructurados.** Solo FAQPage en Machine y Sponsors.
  **Fix v3:** `Organization`/`SportsTeam` (nombre, logo, Waterloo WI, sameAs a Facebook y demás redes), `WebSite` con SearchAction, `Product` + `Offer` (+ `AggregateRating` solo con reseñas reales) en cada ficha, `BreadcrumbList` en colección y ficha, `VideoObject` para el video de YouTube, `SportsEvent` por cada `pull_event`.

- [ ] **M13. SEO: h1 de colección y textos.** "Shop all" (shop.html:65) no tiene ninguna palabra que alguien busque; ninguna colección tiene texto; machine.html usa `h3` de 40 px para "Cat 3208 V8" e "Inline 6" y sponsors usa un `h2` de 12 px ("The season in numbers").
  **Fix v3:** h1 de Shop "Tractor Pulling Merch"; 1 o 2 líneas de descripción por colección; jerarquía de encabezados por estructura, no por tamaño.

- [ ] **M14. Our Story no convence.** Placeholders de equipo (story.html:228 en adelante), video placeholder (story.html:182), y no usa lo mejor del texto real: "Twelve years in the making", "nights and weekends stolen from work and family", "No exhibitions. Every time it hits the track, it's there to pull." (`templates_page.about.json`).
  **Fix v3:** abrir con una foto real y una frase fuerte, línea de tiempo corta (2014, 2020, 2026 rayo, 2026 primer pull, Monroe WI), el video real a la mitad, el equipo real (13 personas + mascotas Cricket y Turbo) en grid de retratos pequeños tipo "staff" (nombre + rol, 6 por fila en desktop), hermanos (Diesel Ross) y cierre con un solo CTA. Alto objetivo: menos de 4,000 px en desktop.

- [ ] **M15. Machine contradice la ficha real.** Turbo "Classified" (machine.html:206) cuando la ficha real dice "SINGLE, LARGE"; el modelo real es "Challenger 1015" y el v2 dice solo "Challenger"; "Transmission: UNKNOWN" y "Chassis: CUSTOM-BUILT" no aparecen (`templates_page.spec-sheet.json`). 6,704 px de alto con tres secciones que repiten los mismos 4 datos (hero, puntos, ficha).
  **Fix v3:** una sola ficha técnica (datos reales), puntos de la anatomía sobre la foto real lateral (`hm-side.jpg`) o el recorte, comparación Cat V8 vs Inline 6 compacta, FAQ y 3 productos. Confirmar con la dueña si el turbo se publica.

- [ ] **M16. Información duplicada y CTAs repetidos entre páginas.** El mismo bloque de 3 productos aparece en Machine, Schedule y Story; "Hook Alerts" aparece en anuncio, Machine FAQ, Story, Schedule y footer.
  **Fix v3:** un componente de producto por página, elegido por colección (Machine = colección "machine"; Schedule = "pull day").

- [ ] **M17. Hashtag y comunidad ausentes.** El tema tiene `#HEAVYMETALPULLING` (sección gallery) con tira de fotos; el v2 no lo usa en ninguna página.
  **Fix v3:** franja de fotos reales con "Tag #HEAVYMETALPULLING" en la home o en Story, editable con bloques de imagen; enlaces a redes en el footer.

- [ ] **M18. Video real ausente.** El tema tiene el video de YouTube; el v2 tiene `ph--video` vacíos.
  **Fix v3:** sección "Watch it pull" con fachada (foto + botón play; el iframe de YouTube carga solo al hacer clic, como ya hacía el tema), en la home y en Schedule.

- [ ] **M19. Accesibilidad de formularios.** Footer: email sin label visible (solo placeholder), sin `autocomplete="email"` ni `required` (hm.js:78); emails sin `spellcheck="false"`; mensajes de éxito falsos ("You're in") sin validar.
  **Fix v3:** labels visibles o flotantes, `autocomplete`, validación en línea con foco en el primer error, estado "Sending…".

- [ ] **M20. Sin enlace "Skip to content".** Ninguna página (grep `skip` = 0).
  **Fix v3:** primer elemento del body, visible al recibir foco.

- [ ] **M21. Declaración de accesibilidad.** No existe. Las tiendas en EE. UU. reciben demandas por la ADA (Title III).
  **Fix v3:** página `/pages/accessibility` (meta WCAG 2.1 AA, contacto para reportar barreras, fecha de revisión) enlazada en el footer.

- [ ] **M22. Contenido de niños y datos de menores.** Hay colección Kids y "Ride With" acepta nombres.
  **Fix v3:** no pedir datos a menores de 13 años (COPPA): el formulario y el checkout los usa el adulto; regla de moderación que diga "first names or nicknames only for kids".

- [ ] **M23. Mapa de calcomanías con silueta inventada.** sponsors.html:249 dibuja un tractor genérico en SVG.
  **Fix v3:** usar `hm-tractor-cutout.png` (perfil real) como fondo del mapa, con los puntos en % editables por bloque o metaobjeto `decal_zone`.

- [ ] **M24. Cifras placeholder visibles.** sponsors.html:230-231 ("XX,XXX followers", "XXX,XXX views") y el reporte de ejemplo con KPIs XX.
  **Fix v3:** mostrar solo las cifras reales ("~20 events", "5,000+ fans in the stands", ambas en el texto del tema); el bloque de estadística se oculta si el campo está vacío.

- [ ] **M25. Barra de anuncio con dos mensajes y CTA a otra lista.** hm.js:33: "Testing season: get Hook Alerts · Free US shipping over $XX".
  **Fix v3:** barra rotativa de 1 mensaje a la vez, editable por bloques (patrón skims-mexico), con pausa; el mensaje por defecto es comercial (envío gratis); Hook Alerts vive en su sección.

- [ ] **M26. Tipografía de rendimiento.** Se carga Archivo variable con todo el rango `wdth 62..125, wght 100..900` y Anton solo para el logo (todas las páginas).
  **Fix v3:** pedir solo los pesos y anchos usados (por ejemplo `wdth 100..125, wght 400..800`) o usar la librería de fuentes de Shopify; el logo como SVG (el tema tiene `hm-logo` con variantes) y quitar Anton.

- [ ] **M27. Header y footer inyectados por JavaScript.** hm.js crea toda la navegación: sin JS no hay menú y hay salto de contenido al cargar.
  **Fix v3:** es aceptable en el boceto, pero en Shopify deben ser secciones Liquid (`header-group`, `footer-group`) y así se especifica en el handoff.

- [ ] **M28. Estado de filtros fuera de la URL.** shop.html: filtros y orden viven en JS; al compartir o volver atrás se pierden.
  **Fix v3:** Search & Discovery de Shopify ya escribe el estado en la URL.

- [ ] **M29. Promesa de "Free US shipping over $XX" sin monto.** Anuncio, PDP, carrito.
  **Fix v3:** la dueña define el monto (sugerencia: un poco arriba del precio de 1 hoodie para empujar 2 artículos) y se edita en una sola configuración del tema.

- [ ] **M30. "Shop the machine" y "Explore the build" en el hero de Machine llevan a anclas** (`#wear`, `#anatomy`) que saltan 4,000 px.
  **Fix v3:** página más corta; "Shop the machine" a la colección "machine".

### MENOR (detalle, pulido)

- [ ] **m1.** Mega menú y menú móvil escriben estilos en línea (hm.js:35, 57) en vez de clases.
- [ ] **m2.** `.ph__tag` en cada tarjeta compite con el nombre del producto; en v3 de revisión, ocultarlos o hacerlos más discretos para juzgar el ritmo real.
- [ ] **m3.** "Cart (0)" en texto; en móvil ocupa espacio. Ícono de bolsa con contador (ya existe `I.bag` en hm.js y no se usa).
- [ ] **m4.** Sin "Back to top" en páginas de más de 5,000 px (Story 7,654; Sponsors 7,737; Machine 6,704). Mejor acortar; si no, botón discreto.
- [ ] **m5.** Breadcrumbs solo en Shop y Producto; añadir en colecciones y en páginas legales.
- [ ] **m6.** `<meta name="theme-color">`, favicon y `apple-touch-icon` faltan.
- [ ] **m7.** Swatches de tarjetas sin nombre accesible en Machine y Schedule (solo `title`); usar `aria-label` como en Shop.
- [ ] **m8.** `.cart-count` definido en hm.css y nunca usado.
- [ ] **m9.** Placeholders sin "…" ni ejemplo ("Your name" → "e.g. Jake M.").
- [ ] **m10.** `touch-action: manipulation` y `-webkit-tap-highlight-color` no definidos.
- [ ] **m11.** Story: TOC de 7 capítulos para una página que debería tener 4 o 5.
- [ ] **m12.** Schedule: "Where we pull" repite lo del FAQ de Machine; fusionar en una línea dentro de la tabla.
- [ ] **m13.** Sponsors: "Single-event options" y "Results bonus" sin aprobación de la dueña; mover a "por confirmar".
- [ ] **m14.** La frase "We know. The sled knows." aparece tres veces (machine.html: panel de potencia, banda oscura y ficha "Ask the sled").
- [ ] **m15.** `aria-live="polite"` en el contenedor de paneles de Machine anuncia todo el panel al cambiar; anunciar solo el título.
- [ ] **m16.** El badge "Best seller" sin datos de ventas al lanzar; usar "Team pick" hasta tener ventas reales (no inventar).
- [ ] **m17.** Facebook es la única red; Instagram, TikTok y YouTube vacíos en `config_settings_data.json`. Pedirlos a la dueña.
- [ ] **m18.** "Kids Hoodie" y "Little Evil One Kids Tee" con talla "M" por defecto en `data-add` (no existe M de niño).
- [ ] **m19.** La barra amarilla "Boceto v2" duplica la navegación y cambia el alto real del header; en la revisión con la dueña, ponerla como botón flotante pequeño.
- [ ] **m20.** Prop 65 (California): preguntar al proveedor de impresión si alguna prenda o el koozie requiere aviso; si sí, el aviso va en la ficha y en checkout.
- [ ] **m21.** Formato de números: "10,000 LB" y "XXX.XX ft" fijos; en Liquid usar filtros de número y unidades consistentes ("10,000 lb").
- [ ] **m22.** Precios "$XX" en todos lados: en v3 usar precios de referencia realistas marcados como ejemplo para juzgar el diseño (largo real de "$34.00").

---

## Parte C · Qué debe poder editar la dueña sin código (Shopify)

| Qué | Cómo en Shopify | Campos / bloques |
|---|---|---|
| Barra de anuncio | Sección `announcement-bar` con bloques | texto, enlace, rotación on/off |
| Hero animado | Sección `hm-hero` | tagline, CTA 1 y 2, distancia objetivo, marquee on/off y texto, reducir movimiento |
| Categorías (miniaturas) | Sección con bloques "category" | imagen, nombre, colección |
| Fila de producto de la home | Sección "featured collection" | colección (Best sellers / New drop), máximo 4 |
| Banda de la máquina, video, galería #HEAVYMETALPULLING | Secciones con bloques | foto, título, texto, enlace; URL de YouTube; fotos |
| Mega menú | Menú de Navigation + sección header con bloques "promo" | links desde Navigation; 0 o 1 tarjeta promo |
| Footer | `footer-group` con bloques "column" (menús de Navigation) + franja legal automática | blurb, menús, redes desde Theme settings, políticas desde Settings > Policies |
| Políticas | Settings > Policies (Refund, Privacy, Terms, Shipping, Contact information) + página Accessibility y SMS Terms | texto |
| Aviso de cookies | Settings > Customer privacy | región, textos |
| Schedule | Metaobjeto `pull_event` | ver C10 |
| Patrocinio: niveles | Metaobjeto `sponsor_tier` | nombre, precio o "From", beneficios (lista), cupos, destacado sí/no |
| Patrocinio: zonas | Metaobjeto `decal_zone` | nombre, x, y, tamaño, nivel, estado, patrocinador (referencia) |
| Patrocinadores actuales | Metaobjeto `sponsor` | logo, nombre, URL, nivel, parte del tractor |
| Equipo | Metaobjeto `crew_member` | nombre, rol, foto, orden, mascota sí/no |
| Ficha técnica y puntos de Machine | Metaobjeto `spec` o bloques de sección | etiqueta, valor, nota, x/y del punto, foto |
| Ride With The Evil One | Producto + line item property + página de reglas | precio, temporada, reglas, cupo |
| Promesas de tienda (envío gratis, días de envío, devoluciones) | Theme settings globales | monto, días, texto corto (una sola fuente para anuncio, ficha y carrito) |
| Formularios (Hook Alerts, sponsors, contacto) | Shopify Forms o Klaviyo + `form 'contact'` nativo | textos, lista de destino, etiquetas |

Patrones de referencia a copiar (sin copiar marca): skims-mexico (logo a la izquierda, secciones que caben en pantalla, banner de una línea, menú de texto con miniaturas, footer con franja legal), grid de colección de SKIMS (fotos casi pegadas, texto mínimo), miniaturas de categoría de kyliecosmetics (círculos pequeños con nombre), página de términos de SKIMS (índice lateral y texto legible).

---

## Parte D · Contenido real que el v2 ignora

| Activo real | Dónde está | Dónde va en v3 |
|---|---|---|
| Animación del tractor (rig, telemetría, riel) | `tema/sections_hm-hero.liquid`, `tema/snippets_hm-rig.liquid` | Hero de home (C1) |
| 13 miembros del equipo + 2 mascotas con nombre y rol (Chris F., Isela F., Cindy F., Daniel, Daniela V., Jared F., Jim F., Tony B., Jeff L., John W., Brad S., Cricket F., Turbo) | `tema/templates_page.about.json` | Story: The crew (M14) |
| Texto largo de la historia ("Twelve years in the making", primer pull, filosofía "nothing off the shelf", "No exhibitions") | `tema/templates_page.about.json` | Story |
| Video YouTube `HfJ5FAJJ5Ac`, "Green County Fall Nationals in Monroe, WI" | `tema/templates_index.json` (video) | Home, Story, Schedule (pasados) |
| Hashtag `#HEAVYMETALPULLING` | `tema/templates_index.json` (gallery) | Home o Story + footer |
| Niveles $25,000 / $10,000 / $5,000 con beneficios, "5,000+ fans in the stands", 6 lugares de logo | `tema/templates_page.sponsors.json` | Sponsors (C11) |
| Promesas: "Ships in 5 days · Printed to order in the USA", "Cards, Apple Pay, Shop Pay", "Every order keeps us pulling" | `tema/templates_index.json` (drop) | Ficha, carrito, footer (tras confirmar con proveedor) |
| Ficha real: Challenger 1015, turbo "Single, large", transmisión, chasis | `tema/templates_page.spec-sheet.json` | Machine (M15) |
| Lema "FULL PULL OR NOTHING" | marquee del hero | Hero / anuncio |
| Página de contacto con formulario nativo | `tema/sections_hm-contact-page.liquid` | `/pages/contact` (C18) |
| Footer con enlaces a políticas | `tema/sections_hm-footer.liquid` | Footer (C5) |
| Fotos: `hm-hero.jpg` (humo), `hm-front-smoke.jpg`, `hm-rear.jpg`, `hm-side.jpg`, `hm-grandstand.jpg`, `hm-engine.jpg`, `hm-driver.jpg`, `hm-driver-crew.jpg`, `hm-crew.jpg`, `hm-front-white.jpg`, `hm-tractor-cutout.png` | `capturas/` | hero.jpg y front-smoke: banda de home y OG; side.jpg y cutout: Machine (puntos) y mapa de Sponsors; engine.jpg: punto "Engine"; grandstand.jpg: Schedule; driver y crew: Story; rear.jpg: banda de Story o poster del video |

Faltan de la dueña (no inventar): email de contacto, dirección postal para emails y políticas, monto de envío gratis, plazos reales del proveedor, regla de devoluciones, precio de Ride With, decisión de publicar precios de patrocinio, fecha y resultado de Monroe, redes sociales, fotos de producto.
