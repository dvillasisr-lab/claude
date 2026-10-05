# 04 · Auditoría del tema "heavy-metal-tema-v12"

**Sitio:** heavymetalprostock.com (tienda con contraseña, 1 producto de prueba de $1 sin imagen)
**Base:** Dawn + secciones propias `hm-*`
**Archivos auditados:** `/home/user/claude/heavy-metal/analisis/tema/` (todas las rutas de abajo son relativas a esa carpeta)
**Guías aplicadas:** Hallmark (`audit`), redesign-existing-projects, Web Interface Guidelines (Vercel, copia local `guidelines.md`)
**Fecha:** 2026-09-30

> Hallmark · auto-crítica del tema actual (1 a 5): Filosofía 4 · Jerarquía 3 · Ejecución 2 · Especificidad 4 · Contención 2 · Variedad 3
> Conteo Hallmark: **9 críticos · 17 mayores · 12 menores**

---

## 0. Resumen ejecutivo

El tema tiene una idea fuerte y propia: negro + amarillo de pista, Anton/Barlow Condensed, y un hero con "telemetría" (tacómetro, distancia a 300 ft, chip de FULL PULL) que solo podría existir para un tractor de arrastre. Eso ya lo separa del 90 % de las tiendas Shopify. La página del equipo tiene una historia real excelente (2014 en Tomah, el rayo al encender el motor, el primer arrastre fallido) y la ficha técnica estilo plano es distintiva.

Lo que lo frena de verse "de premio":

1. **Placeholders y datos sin confirmar en producción**: `$[X]`, `[STORY: ...]`, `UNKNOWN` (caballos y transmisión), `[YEAR]`, `[EMAIL PENDING]`, bundle sin producto, redes vacías.
2. **Movimiento sin control**: 12 animaciones infinitas, solo 1 respeta `prefers-reduced-motion`; un bucle `requestAnimationFrame` que lee y escribe layout en cada frame, para siempre.
3. **Fotos servidas como assets del tema** (sin `srcset`, sin WebP/AVIF, sin `width/height`), fotos verticales de 1050 px estiradas a banners horizontales de 1440 px o más, y un PNG de 682 KB.
4. **La compra vive en Dawn sin personalizar**: la página de producto usa fondo blanco puro (`scheme-2`), fuente Assistant y el bloque de vendor; rompe la marca justo donde se cobra.
5. **Cero datos estructurados propios** (ni Organization/SportsTeam, ni Event, ni WebSite), `theme-color` vacío, sin favicon, y el `<h1>` del home es solo un SVG.
6. **Afirmaciones que el propio sitio contradice**: "MOST POPULAR" en un tier sin patrocinadores, "10 states", "5,000+ fans", "Next season is loading" mientras el video y la página del equipo hablan de pulls de 2026.

---

## 1. Homepage, sección por sección

Orden en `templates_index.json:166-174`: hero → drop → machine → video → gallery → team → cards. Header y footer vienen de `sections_header-group.json` y `sections_footer-group.json`.

### 1.0 Header (`sections_hm-header.liquid`)

| | |
|---|---|
| Qué hace | Logo SVG a la izquierda, 4 links centrados, carrito + botón "SHOP MERCH" a la derecha. Sticky a 80 px (`assets_hm.css:32`). Burger `<details>` en móvil. |
| Bueno | `aria-current="page"` real (`:7`), `aria-label` en logo, carrito y burger (`:2`, `:12`, `:21`). Sin JS. |
| Débil | Es exactamente el nav por defecto de IA: wordmark izquierda + 4 links + botón derecha + borde de 1 px (Hallmark gate 42). El burger no marca la página actual (`:16`) y no se cierra con Escape. El contador del carrito no se actualiza sin recargar (los formularios `hm-drop` no son AJAX). Los anclajes `#watch`, `#shop`, `#kit` quedan tapados por el header sticky porque no hay `scroll-margin-top` en ningún lado de `assets_hm.css`. |

### 1.1 Hero (`sections_hm-hero.liquid`)

| | |
|---|---|
| Qué hace | Logo cromado como `<h1>` (`:5`), tagline "THE EVIL ONE" (`:6`), 2 CTAs (`:8-9`), panel "LIVE TELEMETRY" con tacómetro SVG y distancia (`:13-25`), pista con tractor SVG animado que cruza la pantalla en bucle de 8 s (`:28-37`) y marquee amarilla (`:40`). |
| Bueno | Es la pieza más original del sitio: la metáfora del arrastre (0 → 300 ft, "FULL PULL!") es específica, memorable y tiene lógica de producto. Los CTAs son claros ("SHOP THE DROP" / "WATCH IT PULL"). Usa `svh` para el alto (`assets_hm.css:48`). |
| Débil | **(a)** El tractor es una ilustración SVG genérica (`snippets_hm-rig.liquid`), no Heavy Metal. Existe `hm-tractor-cutout.png` y fotos con humo negro reales que no aparecen arriba del pliegue. Para un equipo que vende identidad, el hero debería mostrar LA máquina. **(b)** "LIVE TELEMETRY" (`:14`) es falso: son números de una animación. Hallmark gate 46 (contenido inventado). Cambiar a "SIMULATED PULL" o, mejor, usar datos reales de un pull (distancia real del último arrastre). **(c)** El `<h1>` contiene solo `{% render 'hm-logo' %}`; el snippet `hm-logo` no está en la exportación y hay que confirmar que lleva `<title>` o `aria-label`, si no el h1 queda vacío para Google y lectores de pantalla. **(d)** Jerarquía: compiten logo gigante, tacómetro, 18 speed-lines, tractor, bandera y marquee; el ojo no sabe dónde aterrizar. **(e)** El CTA principal va a `shopify://collections/all` (`templates_index.json:17`) con 1 producto de prueba: hoy lleva a una colección casi vacía. |

### 1.2 The Drop (`sections_hm-drop.liquid`)

| | |
|---|---|
| Qué hace | Barra de 4 promesas (`:2`), título "WEAR THE METAL" (`:4`), grid de 3 productos con talla y ADD TO CART directo (`:7-43`), nota "More drops coming" (`:44`) y banner Crew Pack (`:45-54`). |
| Bueno | Añadir al carrito desde el home con selector de talla es excelente para merch de evento. Los radios usan `fieldset` + `legend` (`:24`), deshabilitan tallas agotadas (`:26`) y el tachado visual existe (`assets_hm.css:117`). Etiquetas `badge:` desde tags (`:12`) es buen sistema. |
| Débil | **Placeholder vivo:** "On orders over $[X]" (`templates_index.json:30`). **Bundle roto:** `bundle_product` vacío (`templates_index.json:42`), así que no hay precio y "GET THE BUNDLE" lleva a `/collections/all` (`:51`) mientras el texto promete "together and save": promesa sin cumplir. **Colección:** con 1 producto sin imagen el grid muestra 1 tarjeta con el título como placeholder (`:15`) y 2 huecos. **Fallback de demo** filtra "Can Sleeve (by Printify)" (`:36`), revela al proveedor. **Precio:** `product.price` sin "desde" cuando hay variantes con distinto precio y sin `compare_at_price` (`:18`). **Copy fijo:** "SHOP ALL GEAR →" (`:5`) y "More drops coming..." (`:44`) no son editables, y `:44` usa estilo en línea con hex. **Tallas** de 28 px de alto (`assets_hm.css:115`), objetivo táctil chico. **Sin feedback** al añadir: el form hace POST normal y redirige a `/cart`. |

### 1.3 The Machine (`sections_hm-machine.liquid`)

| | |
|---|---|
| Qué hace | Banner con foto de grada y Ken Burns (`:3`), título "FULL PULL / OR NOTHING" con outline (`:6`), botón a la ficha (`:7`), mosaico motor + lateral (`:11-16`) y 6 specs (`:17-21`). |
| Bueno | El solape de `margin-top:-120px` (`assets_hm.css:137`) da profundidad; la rejilla de specs con líneas finas se lee como hoja técnica. Buen link a la ficha completa. |
| Débil | **"HORSEPOWER: UNKNOWN"** (`templates_index.json:71`) en el bloque que debería vender potencia: se lee como descuido. Mejor quitar la fila o poner un dato real ("680 CU IN", "REVERSE-FLOW", "SINGLE TURBO", que sí están en la ficha). Ninguna imagen está elegida en el editor (no hay `banner/engine/side` en `templates_index.json:108-115`), todo usa fallbacks de assets sin `srcset`. El `<h2>` lleva `font-size` en línea (`:6`). El texto blanco sobre foto depende de un `text-shadow` (`assets_hm.css:132`). |

### 1.4 Video (`sections_hm-video.liquid`)

| | |
|---|---|
| Qué hace | Póster con botón play que al hacer clic inyecta el iframe de YouTube (`:7-19`, `assets_hm.js:40-47`). |
| Bueno | Facade correcto: YouTube no carga hasta el clic (ahorro grande de JS). El botón tiene `aria-label` (`:7`). El póster sí usa `shopify://shop_images` (`templates_index.json:125`), así que pasa por `image_url` con `srcset`. |
| Débil | El iframe usa `youtube.com` y no `youtube-nocookie.com` (`:17`). La URL guardada trae `&themeRefresh=1` (`templates_index.json:124`), basura de copiar y pegar. El caption dice "Green County Fall Nationals 2026" (`templates_index.json:126`) mientras la sección de calendario dice "Next season is loading": contradicción. Tras el clic el foco se pierde (el botón se reemplaza y no se mueve el foco al iframe, `assets_hm.js:45`). |

### 1.5 Gallery (`sections_hm-gallery.liquid`)

| | |
|---|---|
| Qué hace | "TAG #HEAVYMETALPULLING" + tira infinita de 6 fotos x2 inclinadas (`:9-17`). |
| Bueno | La inclinación de -6° y el hover con zoom tienen energía de motor. Duplica la tira con `aria-hidden` en la copia (`:12`, `:14`). |
| Débil | **Instagram y Facebook vacíos** (`templates_index.json:134-135`): la sección pide etiquetar un hashtag pero no hay a dónde ir ni botón de seguir. Sin bloques, se cargan 6 JPG completos de 1050x1400 como assets (`:14`), con el mismo alt "Heavy Metal at the pull" 6 veces. El texto del hashtag usa color en línea (`:3`). La tira se mueve siempre y solo se pausa con hover (`assets_hm.css:161-162`): falla WCAG 2.2.2 para teclado y táctil. |

### 1.6 Team (`sections_hm-team.liquid`)

| | |
|---|---|
| Qué hace | Foto del equipo con recorte diagonal + título + historia + 2 botones. |
| Bueno | El `clip-path` diagonal (`assets_hm.css:169`) rompe la caja; buen par de CTAs (conocer equipo / comprar). |
| Débil | **Placeholder vivo:** `[STORY: 2 or 3 sentences...]` (`templates_index.json:144`). La historia real ya existe en `templates_page.about.json` (story_text: "It started in 2014 in Tomah, Wisconsin..."): basta copiar 2 frases. |

### 1.7 Schedule + Sponsors (`sections_hm-cta-cards.liquid`)

| | |
|---|---|
| Qué hace | Tarjeta amarilla con captura de email etiquetada `newsletter,pull-schedule` (`:4-10`) y tarjeta de patrocinio con foto (`:12-19`). |
| Bueno | Formulario `customer` nativo con `label`, `type="email"`, `autocomplete="email"`, `required` (`:8`) y mensaje de éxito sobrio (`:6`). Etiquetas para segmentar en Shopify Email. |
| Débil | "NEXT SEASON IS LOADING" (`templates_index.json:155`) contradice el resto del sitio (hay pulls 2026). Sin incentivo (10 % en la primera compra, sticker gratis) ni opción SMS. El error se muestra con `default_errors` sin `aria-live` (`:8`). La tarjeta amarilla ocupa mucho más del 5 % de acento del viewport (Hallmark gate 23). |

### 1.8 Footer (`sections_hm-footer.liquid`)

| | |
|---|---|
| Bueno | Enlaces a políticas (`:17`), año dinámico (`:25`), columnas con fallback útil si no hay menú. |
| Débil | Es el "AI footer" de 4 columnas + marca (Hallmark gate 43). Sin email signup, sin redes (todas vacías en `config_settings_data.json:111-119`), el link "Crew Pack bundle" (`:11`) lleva a un bundle que no existe. Las 3 columnas sin menú dependen de que el título sea exactamente "SPONSOR"/"TEAM"/"HELP" (`:9-17`): frágil si alguien cambia el texto. |

---

## 2. Diseño visual

### 2.1 Tipografía

- **Pareja correcta para el género:** Anton (display condensada) + Barlow Condensed (etiquetas) + Barlow (texto) encaja con motorsport y rotulación de tráiler. Bien.
- **Tres familias, más una cuarta invisible:** Dawn sigue cargando Assistant (`config_settings_data.json:13,15`; `layout_theme.liquid:81-85`, precargas `:300` y `:305`) y la usa en producto, carrito y búsqueda. El sitio cambia de voz tipográfica en la página que cobra.
- **Cursivas falsas:** `.hm-marquee__track` pide `font-style:italic` sobre Anton (`assets_hm.css:93`), que no tiene cursiva: el navegador la sintetiza.
- **Todo inclinado:** `skewX(-8deg)` en `.hm-h2`, specs, bundle, h1 de páginas (`assets_hm.css:15,122,149,192,219`). Es una decisión de marca válida (velocidad), pero aplicada a TODO pierde fuerza; Hallmark lo trata como "italic headers" (gate 38a). Reservarla para 1 o 2 momentos (hero y el "FULL PULL").
- **Mayúsculas con `line-height:.9`** en h1/h2 (`assets_hm.css:15,192`): con 2 líneas se tocan los topes (Hallmark gate 55). Subir a 0.95 o 1.
- **Sin `text-wrap:balance`** en ningún título y sin `overflow-wrap:anywhere` en display (gates 51 y Vercel "Typography").
- **Sin `font-variant-numeric:tabular-nums`**: el contador de distancia y las RPM (`assets_hm.css:70`) bailan de ancho con cada número.
- Letter-spacing de 3 a 8 px en casi todo (`assets_hm.css:14,56`), todo en mayúsculas: sin respiro para el ojo. Faltan párrafos en caja normal con medida de 60 a 70 caracteres.

### 2.2 Color

- Paleta comprometida y bien tokenizada en `:root` (`assets_hm.css:2-7`): negro tintado `#0B0B0A` (no negro puro, bien), crema `#F2F0E9`, amarillo `#F5C400`.
- **Fuga de tokens:** decenas de hex en línea fuera de los tokens en `sections_hm-sponsor-body.liquid:4,5,10,15,16,21-23`, `sections_hm-spec-sheet.liquid:30-66`, `sections_hm-team-page.liquid` (todo el `<style>` y los inline), `sections_hm-schedule-page.liquid`, `sections_hm-contact-page.liquid`, y `font-family:'Anton'...` en línea en muchas páginas. Hallmark gate 48.
- **Gradiente "cromado" animado en texto** (`.hm-chrome`, `assets_hm.css:17`): es el tell número 1 de Hallmark (gradient headline). Aquí tiene excusa temática (metal pulido), pero se usa en 9 lugares. Dejarlo solo en el logo.
- **Dos universos de color:** `scheme-2` blanco puro `#ffffff` en producto y cards (`config_settings_data.json:182-190`, `templates_product.json:71,100`) contra un sitio 100 % oscuro, y `scheme-5` azul `#334fb4` de Dawn sin uso. La ficha técnica usa navy `#1A2230` (`sections_hm-spec-sheet.liquid:3`), que funciona como "plano", ok.
- Falta textura: el sitio es plano. Un grano sutil o fotos con tratamiento duotono negro/amarillo darían el "tactile" que pide el género.

### 2.3 Espaciado y layout

- Escala informal: 14, 18, 22, 28, 36, 56, 64, 72, 90, 100, 110 px repartidos a mano (`assets_hm.css:96,152,160,168,175`). Sin escala de tokens `--space-*`.
- Estructura del home = plantilla IA con cambio de color: hero → barra de 4 promesas → 3 tarjetas → banner → video → galería → split texto/imagen → 2 tarjetas CTA → footer 4 columnas (Hallmark gate 8).
- **Eyebrow numerado en cada sección** ("01 / THE DROP" ... "07 / SPONSORS", `templates_index.json:37,109,120,132,139,154,158`): tell "Eyebrow on every section". En la página del equipo la numeración salta 01, 02, rayo, 04, 05 (`sections_hm-team-page.liquid:84,85,129,145`).
- Tres columnas iguales repetidas: productos (`assets_hm.css:104`), placements y tiers (`:200,205`), "proudest moments" (`sections_hm-team-page.liquid:137-139`).
- Bueno: `minmax(0,1fr)` en casi todas las rejillas con imagen (gate 50 ok), `svh` en hero, solapes y `clip-path` que rompen la caja.

### 2.4 Movimiento

- Inventario de animaciones infinitas: `hmDrive`, `hmSpeed` x18, `hmSpin`, `hmWheelie`, `hmSmoke`, `hmDirt`, `hmShake`, `hmMarquee` x2, `hmChrome`, `hmPulse`, `hmFlash`, `hmKb`, `hmKb2` (`assets_hm.css:237-251`).
- **Solo `hmShimmer` respeta `prefers-reduced-motion`** (`assets_hm.css:252`). Todo lo demás corre siempre. Hallmark gate 27 y WCAG 2.3.3.
- `hmFlash` parpadea 2 veces por segundo (`assets_hm.css:74`) cuando llega a FULL PULL: por debajo del umbral de 3/s, pero agresivo.
- La animación no cuenta nada: el tractor cruza cada 8 s sin relación con el scroll ni con el usuario. La versión premio sería **ligar el arrastre al scroll** (el visitante "empuja" el trineo hasta 300 ft bajando la página), con el tacómetro reaccionando.
- Transiciones bien acotadas (`transition: filter`, `transform`), sin `transition: all`. Bien.

### 2.5 ¿Se siente de premio?

**Hoy: no.** Se siente como un tema personalizado con carácter, por encima de la media de Shopify, pero con acabado de borrador. Qué le falta para nivel Awwwards:

1. **Fotografía como protagonista.** Hero con la máquina real (video loop corto de 6 a 8 s con humo negro, muted, con póster) en lugar del SVG caricaturesco.
2. **Una sola idea de interacción ejecutada perfecto:** el pull ligado al scroll, con sonido opcional del motor (toggle explícito, apagado por defecto).
3. **Contención:** 1 acento amarillo por pantalla, la inclinación y el cromado solo en 2 momentos, un solo eyebrow por página.
4. **Sistema tipográfico con cuerpo:** párrafos en caja normal, medida controlada, números tabulares, títulos balanceados.
5. **Estados completos y microinteracciones:** feedback al añadir al carrito (drawer), `:active`, estados de carga en formularios.
6. **Consistencia de extremo a extremo:** producto, carrito y contraseña con el mismo lenguaje que el home.
7. **Cero placeholders.** Un solo `[X]` visible descalifica cualquier jurado.

---

## 3. Conversión

### 3.1 Página de producto (`templates_product.json`)

- Es `main-product` de Dawn sin tocar: bloque **vendor** con `{{ product.vendor }}` (`:15-21`) que puede mostrar "Printify" o el nombre de la tienda; `scheme-2` blanco (`:71`); fuente Assistant; picker de botones pill con radio 40 px (`config_settings_data.json:32`) que choca con los botones rectos inclinados del resto.
- Falta: guía de tallas, "printed to order, ships in X days" junto al botón, bloque de confianza (envío, devoluciones), historia corta de la máquina ("cada compra mantiene a Heavy Metal en la pista"), fotos en contexto (gente en la grada con la playera), y reseñas.
- `show_gift_card_recipient: true` (`:45`) es irrelevante aquí.
- "You may also like" genérico (`:95`) con 1 producto en catálogo mostrará vacío.
- `hide_variants: true` + `media_fit: contain` en blanco: la prenda negra flota en blanco puro.
- **Recomendación:** crear `sections/hm-product.liquid` con el lenguaje `hm-*`, usando `product-form` de Dawn para AJAX y el cart drawer.

### 3.2 Carrito

- `cart_type: "notification"` (`config_settings_data.json:124`), pero los formularios del home (`sections_hm-drop.liquid:19`) no usan el `product-form` de Dawn, así que no disparan la notificación: redirigen a `/cart`, que es Dawn plano.
- Pasar a `cart_type: "drawer"` con estilo `hm-*`, barra de progreso a envío gratis (cuando se defina `$[X]`) y upsell del can sleeve o sticker.

### 3.3 Confianza

- La barra de 4 promesas es buena idea (`sections_hm-drop.liquid:2`), pero 2 de 4 no están verificadas: "$[X]" y "SHIPS IN 5 DAYS" (print on demand suele tardar 2 a 7 días hábiles de producción más envío). Confirmar con Printify antes de prometer.
- Faltan logos de pago reales, políticas visibles cerca del botón y prueba social (fotos de fans, "worn at Green County Fall Nationals").
- El chat Shopify Inbox está activo (`config_settings_data.json:146-167`): suma confianza pero también peso de JS; decidir si alguien lo va a contestar.

### 3.4 Bundle

- Sin producto asignado (`templates_index.json:42`). Crear el producto "Crew Pack" (o usar Shopify Bundles) con `compare_at_price` para que el tachado de `sections_hm-drop.liquid:50` funcione. Hasta entonces, apagar `show_bundle`.

### 3.5 Urgencia

- El concepto "The Drop" pide ediciones limitadas y fechas: hoy no hay contador, ni "edición Green County 2026", ni stock visible. Etiquetas `badge:LIMITED` existen pero no se usan.
- Idea con honestidad: "Pull Day Edition", tiraje por evento, que se cierra al terminar el fin de semana del pull.

### 3.6 Captura de email / SMS

- Un solo punto de captura en el home (`sections_hm-cta-cards.liquid:4-10`). Bien construido, pero:
  - Sin incentivo.
  - Sin SMS (Shopify Messaging o Klaviyo, con casilla de consentimiento TCPA).
  - La página de calendario manda a `/#schedule` (`sections_hm-schedule-page.liquid:19,38`) en vez de tener el formulario ahí mismo: se pierde el visitante de mayor intención.
  - Sin captura en footer.
  - **La página de contraseña** (`templates_password.json:15-49`) es la de Dawn: "Opening soon / Be the first to know when we launch." Mientras la tienda esté cerrada, es la única página pública. Debe tener la marca, una foto de la máquina y el mismo formulario con etiqueta `launch-waitlist`.

### 3.7 Captación de patrocinadores (`sections_hm-sponsor-body.liquid`, `templates_page.sponsors.json`)

- **Bueno:** formulario con `label`, `autocomplete`, `type="email"/"tel"` (`:45-50`); tiers claros con precio y beneficios; estado vacío honesto "NO SPONSORS ON BOARD YET" (`:21-25`), eso sí es buena copia.
- **Débil:**
  - Placeholder vivo "SPONSORSHIP · SEASON [YEAR]" (`sections_hm-sponsor-hero.liquid:22`; el template trae `settings: {}` en `templates_page.sponsors.json:14`).
  - "MOST POPULAR" (`:31`) en un tier cuando el propio sitio dice que no hay patrocinadores: prueba social inventada. Cambiar a "RECOMMENDED" o "BEST VALUE".
  - Stats sin fuente: "20 pulls", "5,000+ fans", "10 states", "NEW on social media" (`templates_page.sponsors.json:22-44`). "10 states" choca con un circuito de Wisconsin (PPL Badger State) más NTPA; "NEW" no es un número. Confirmar o reemplazar por datos verificables (fechas de eventos confirmadas, asistencia publicada por el organizador).
  - "CLAIM THIS SPOT" (`:35`) no preselecciona el tier en el `<select>` (`:49`): siempre queda el destacado.
  - `contact[company]` no es obligatorio; falta presupuesto, ciudad y "¿cómo nos conociste?".
  - Placeholders "Jane Smith" y "(555) 123 4567" (`:45`, `:48`): tell de IA; usar "Your name" y un formato local "(608) ...".
  - Falta un **media kit** descargable (PDF con fotos, calendario, audiencia) a cambio del email, y un render/mockup del logo sobre el tractor y el tráiler: es lo que cierra patrocinios.
  - Sin evento de conversión medible (no hay `form.posted_successfully?` con píxel ni UTM).

---

## 4. Rendimiento / Core Web Vitals

### 4.1 Fuentes (duplicadas)

| Fuente | Dónde | Problema |
|---|---|---|
| Google Fonts: Anton, Barlow 400/500/600, Barlow Condensed 500/600/700/700i | `layout_theme.liquid:67-69` | Hoja bloqueante, colocada **después** de `content_for_header` (scripts de apps por delante). 3.er origen (googleapis + gstatic). Unas 8 descargas woff2. |
| Shopify Fonts: Assistant (5 `font_face`, 2 precargas del mismo archivo) | `layout_theme.liquid:14-16, 81-85, 298-307` | Se precarga una fuente que el home no usa. Body y header son `assistant_n4`: la misma URL precargada dos veces. |

**Arreglo:** subir Anton + Barlow + Barlow Condensed como woff2 al tema (subset latino), `@font-face` con `font-display:swap` en `hm.css`, precargar solo Anton y Barlow Condensed 700, quitar Google Fonts, y poner `type_body_font`/`type_header_font` en una fuente de sistema (o mapear `--font-body-family` a Barlow) para que Dawn no descargue Assistant.

### 4.2 Imágenes

- Las 11 fotos se sirven como **assets del tema** vía `asset_url` en el fallback de `snippets_hm-img.liquid:5`: sin `srcset`, sin WebP/AVIF automático, sin `width`/`height`, un solo tamaño para móvil y desktop.
- Tamaños en disco: 160 a 306 KB por JPG (`hm-crew.jpg` 304 KB, `hm-front-white.jpg` 306 KB, `hm-rear.jpg` 298 KB) y `hm-tractor-cutout.png` **682 KB** (1120x576 RGBA).
- **Todas las fotos son verticales 1050x1400 o 788x1400** y se usan en banners horizontales: `hm-machine__banner` a 100vw x 560 px (`assets_hm.css:128`), `hm-shero` 560 px, `hm-tm-hero` 560 px. En una pantalla de 1440 px se escala el ancho 137 % y se recorta el 70 % de la altura: foto blanda y encuadre arbitrario.
- La galería sin bloques carga 6 JPG completos (~1.4 MB) para mostrarlos a 300x360 (`sections_hm-gallery.liquid:14`).
- **Arreglo:** subir las fotos a Contenido > Archivos (idealmente originales horizontales de 2400 px o más), elegirlas en cada `image_picker` para que `snippets_hm-img.liquid:3` genere `srcset` 600 a 2000 con WebP/AVIF; añadir `width`/`height` al fallback; convertir el cutout a WebP con alfa (~60 a 90 KB).
- El snippet sí está bien pensado cuando hay imagen (`image_url` + `widths` + `sizes`), solo que casi ninguna sección tiene imagen asignada.

### 4.3 LCP

- **Home:** no hay imagen en el hero; el candidato LCP será texto (tagline o CTA) cuyo pintado depende de la hoja de Google Fonts bloqueante. El SVG del logo no cuenta como candidato. LCP estimado móvil 3G rápida: 2.8 a 3.5 s, dominado por fuentes.
- **Sponsors / Team:** la imagen del hero es LCP, tiene `loading: 'eager'` (`sections_hm-sponsor-hero.liquid:2`, `sections_hm-team-page.liquid:69`) pero es un asset de 250 a 300 KB sin `srcset` ni `fetchpriority="high"`.
- **Schedule / Contact:** la imagen del hero (LCP) queda con `loading="lazy"` por defecto (`snippets_hm-img.liquid:5`; `sections_hm-schedule-page.liquid:12`, `sections_hm-contact-page.liquid:21`): tell "Lazy-loaded LCP" (Hallmark crítico).

### 4.4 JavaScript e INP

- `assets_hm.js:13-38`: bucle `requestAnimationFrame` infinito que en cada frame **lee** `getBoundingClientRect()` dos veces (`:14-15`) y **escribe** `style.width` (`:26`, propiedad de layout), `textContent` y `transform`. Resultado: layout forzado cada frame, 60 veces por segundo, aunque el hero esté fuera de pantalla. Castiga batería en móvil e INP.
- `shopify:section:load` (`:54`) vuelve a llamar `boot()` sobre todos los heros: en el editor se apilan bucles.
- Las animaciones CSS del tractor mueven hijos de `<svg>` (`assets_hm.css:86-91`), que en Chrome corren en el hilo principal, no en el compositor.
- Dawn carga 9 scripts `defer` (`layout_theme.liquid:52-60`) más `animations.js` porque `animations_reveal_on_scroll` está en `true` (`config_settings_data.json:21`, `layout_theme.liquid:62-64`) aunque ninguna sección `hm-*` usa las clases de reveal.
- `hm.css` se carga **antes** que `base.css` (`layout_theme.liquid:70` vs `:287`): las reglas de Dawn con igual especificidad pisan a las propias. Riesgo de regresiones sutiles.
- **Arreglo:** calcular la posición del tractor desde el tiempo de la animación (sin leer layout), `scaleX` en vez de `width`, `IntersectionObserver` para parar fuera de pantalla, salir si `prefers-reduced-motion`, y guardar el id del rAF para cancelarlo en `shopify:section:unload`.

### 4.5 CLS

- Mayormente contenido: casi todas las fotos viven en cajas de alto fijo con `object-fit:cover`. Riesgos: el fallback sin `width/height` (`snippets_hm-img.liquid:5`) en `.hm-bp__rig`, y el cambio de fuente Impact → Anton en títulos de 88 a 120 px (sin `size-adjust` en el fallback).

---

## 5. SEO técnico en el tema

| Punto | Estado | Detalle |
|---|---|---|
| `<title>` | Ok | Patrón Dawn (`layout_theme.liquid:18-23`). Revisar el título de la home en Preferencias: debe incluir "Pro Stock pulling tractor, Waterloo, Wisconsin". |
| Meta description | Depende del admin | `layout_theme.liquid:25-27`, solo si `page_description` existe. Llenar la de la tienda y de cada página. |
| Open Graph / Twitter | Dawn `meta-tags` (`layout_theme.liquid:29`) | No está en la exportación; usa la imagen social de Preferencias. Subir una imagen 1200x630 de la máquina con humo. |
| Canonical | Ok | `layout_theme.liquid:8`. |
| `theme-color` | Mal | Vacío (`layout_theme.liquid:7`). Poner `#0B0B0A`. |
| Favicon | Falta | No hay `favicon` en `config_settings_data.json`. |
| `color-scheme: dark` | Falta | Ni en `<html>` ni en CSS; los scrollbars y controles nativos salen claros. |
| JSON-LD | Casi nada | Ninguno propio. Solo el de producto de Dawn (si `main-product` conserva `structured_data`). Faltan `SportsTeam`/`Organization` (logo, `sameAs` a redes, `location` Waterloo, WI), `WebSite`, `Event` por cada pull en el calendario, y `BreadcrumbList`. |
| H1 | Riesgo | Home: `<h1>` con solo SVG (`sections_hm-hero.liquid:5`); confirmar texto accesible en `hm-logo` o añadir `<span class="visually-hidden">Heavy Metal Pro Stock pulling tractor</span>`. Resto de páginas: un h1 correcto. |
| Jerarquía | Menor | `h4` tras `h2` sin `h3` (`sections_hm-team-page.liquid:137-139`); en sponsors la primera parte ("WHERE YOUR BRAND SHOWS UP") es un `<p>` (`sections_hm-sponsor-body.liquid:4`), no un título. |
| Alt | Mixto | Buenos alts descriptivos en machine/team; repetido x6 en galería (`sections_hm-gallery.liquid:12,14`); alt = título en productos (`sections_hm-drop.liquid:15`), aceptable. |
| Indexación | Bloqueada | Tienda con contraseña: nada indexa hoy. Preparar todo esto antes de abrir. |
| Contenido | Oportunidad | La historia del equipo y la ficha técnica son contenido único y buscable ("Cat 3208 reverse flow pulling tractor", "Pro Stock Wisconsin"). Falta enlazar la ficha desde el producto y añadir páginas por evento. |

---

## 6. Accesibilidad

### 6.1 Contraste (WCAG 2.1, calculado)

| Par | Ratio | Uso | Resultado |
|---|---|---|---|
| `#8C8A82` sobre `#2E2E2B` (fondo del hero) | 3.94 | `.hm-readout__label`, `.hm-readout__target`, "PRO STOCK · WI" en 12 a 13 px (`assets_hm.css:68,72`; `sections_hm-hero.liquid:14`) | **Falla** AA texto normal (4.5) |
| `#6E6B62` sobre `#2E2E2B` | 2.56 | Borde del chip "PULLING…" (`assets_hm.css:73`) | **Falla** 1.4.11 (3:1) |
| `#45443F` sobre `#0B0B0A` | 2.02 | Bordes de inputs y tallas (`assets_hm.css:115,224`; contacto `:11`) | **Falla** 1.4.11 |
| `#6E6B62` sobre `#0B0B0A` | 3.70 | Tramos del gradiente `.hm-chrome` | Pasa solo como texto grande |
| `#8C8A82` sobre `#0B0B0A` | 5.69 | Textos secundarios | Pasa |
| `#A8A59A` sobre `#121210` | 7.60 | Mute en tarjetas | Pasa |
| `#F5C400` / `#0B0B0A` | 11.98 | Botones y acento | Pasa |
| Texto con `-webkit-text-stroke` transparente sobre foto | n/a | `.hm-outline` en banners (`assets_hm.css:16`) | Riesgo: legibilidad depende de la foto |

### 6.2 Foco

- `:focus-visible` con contorno amarillo en botones, links, inputs y selects dentro de `.hm` (`assets_hm.css:28`), y en tallas (`:118`). Bien.
- El foco del `summary` del burger depende de Dawn `base.css`.
- Sin `scroll-margin-top`: al saltar con teclado a `#kit`, `#tiers`, `#watch`, el header sticky tapa el destino.
- Tras reproducir el video el foco desaparece (`assets_hm.js:45`).

### 6.3 Movimiento reducido

- Solo 1 de 15 animaciones lo respeta (`assets_hm.css:252`). El bucle JS tampoco lo consulta.
- La galería y la marquee se mueven más de 5 s sin control de pausa accesible (WCAG 2.2.2). La galería solo pausa con hover.

### 6.4 Otros

- Tallas y botones pequeños: 28 px (`assets_hm.css:115`) y 44 px (`:29`); objetivo recomendado 44 px mínimo.
- Mensajes de formulario sin `aria-live` (`sections_hm-cta-cards.liquid:8`, `sections_hm-sponsor-body.liquid:50`, `sections_hm-contact-page.liquid:59`).
- El SVG del tractor tiene `role="img"` + `aria-label` (`snippets_hm-rig.liquid:1`) pero vive dentro de `.hm-track` con `aria-hidden="true"`: redundante, no dañino.
- El icono del rayo en la página del equipo (`sections_hm-team-page.liquid`, beat 03) no tiene `aria-hidden`.
- El email de contacto es texto plano, no `mailto:` (`sections_hm-contact-page.liquid:36`), y hoy muestra "[EMAIL PENDING]" (`:73`, template sin settings).
- Skip link presente (`layout_theme.liquid:331-333`). Bien.

---

## 7. Bugs y código riesgoso

| # | Severidad | Dónde | Qué |
|---|---|---|---|
| B1 | Alta | `templates_index.json:30,71,144`; `sections_hm-sponsor-hero.liquid:22`; `sections_hm-contact-page.liquid:73`; `templates_page.spec-sheet.json:18,21` | Placeholders visibles: `$[X]`, `UNKNOWN` x3, `[STORY...]`, `[YEAR]`, `[EMAIL PENDING]`. |
| B2 | Alta | `assets_hm.js:13-38` | rAF infinito con lectura y escritura de layout por frame; sin parada fuera de viewport ni con movimiento reducido. |
| B3 | Alta | `assets_hm.js:54` | Re-boot en `shopify:section:load` sin cancelar bucles previos: se duplican en el editor. |
| B4 | Alta | `sections_hm-drop.liquid:45-54`, `templates_index.json:42` | Bundle sin producto: sin precio, CTA a `/collections/all`, promesa de ahorro falsa. |
| B5 | Media | `sections_hm-sponsor-body.liquid:31` | "MOST POPULAR" sin ningún patrocinador. |
| B6 | Media | `templates_page.spec-sheet.json:30`, `templates_page.about.json` (pull_quote) | "This thing is f#cking evil." en la ficha y en la página del equipo: riesgo con patrocinadores familiares y agrícolas. Decisión consciente o suavizar ("This thing is evil."). |
| B7 | Media | `layout_theme.liquid:70` vs `:287` | `hm.css` antes de `base.css`: Dawn gana en empates de especificidad. |
| B8 | Media | `sections_hm-drop.liquid:19-31` | Form sin AJAX: no activa la notificación del carrito, recarga a `/cart`; el contador del header no se refresca sin recarga. |
| B9 | Media | `sections_hm-drop.liquid:26` | Si todas las variantes están agotadas, el radio marcado puede ser uno `disabled` y el envío falla. |
| B10 | Media | `sections_hm-footer.liquid:9-17` | Fallback del footer depende del texto exacto del título. |
| B11 | Media | `snippets_hm-img.liquid:5` | Fallback sin `width`/`height`/`srcset`; `loading` lazy por defecto incluso en héroes de página. |
| B12 | Baja | `sections_hm-drop.liquid:36` | Fallback de demo menciona "(by Printify)". |
| B13 | Baja | `sections_hm-spec-sheet.liquid:7-8,20-23` | `!important` en cadena y `<style>` por sección; mover a `hm.css` o `{% stylesheet %}`. |
| B14 | Baja | `sections_hm-video.liquid:17` | iframe sin `youtube-nocookie`; URL con `&themeRefresh=1`. |
| B15 | Baja | `sections_hm-sponsor-body.liquid:35,49` | "CLAIM THIS SPOT" no preselecciona el tier. |
| B16 | Baja | `sections_hm-team-page.liquid:84-145` | Numeración de beats 01, 02, (rayo), 04, 05. |
| B17 | Baja | `sections_hm-schedule-page.liquid:16`, `sections_hm-spec-sheet.liquid:58` | `"now" | date` queda congelado en caché de página; aceptable, pero el año del calendario debería ser un setting. |
| B18 | Baja | `config_settings_data.json:21` | Reveal-on-scroll de Dawn activo sin uso: JS muerto. |
| B19 | Baja | `assets_hm.css:291` y `:288` | `.hm-rig{width:120vw}` duplicado; `.hm-hero__logo{width:100%}` duplicado (`:278`, `:280`). |
| B20 | Info | Exportación | Faltan `snippets/hm-logo.liquid`, `snippets/hm-logo-line.liquid` y `snippets/meta-tags.liquid` en el análisis: verificar texto accesible del logo y OG. |

**Coherencia de contenido (no es código, pero rompe confianza):** el video habla de "Green County Fall Nationals 2026" (`templates_index.json:126`), la página del equipo narra el primer pull de 2026, y a la vez el home dice "NEXT SEASON IS LOADING" (`:155`), el calendario dice "COMING SOON / First season, first results" (`sections_hm-schedule-page.liquid:25-33`) y el equipo "BEST RESULTS: TBD" (`sections_hm-team-page.liquid:139`). Elegir una sola línea de tiempo y publicarla.

---

## 8. Lista priorizada: Keep / Fix / Rebuild

Esfuerzo: **S** = menos de 2 h · **M** = medio día a 2 días · **L** = 3 días o más.

### KEEP (conservar y proteger)

| # | Qué | Por qué | Esfuerzo |
|---|---|---|---|
| K1 | Paleta negro tintado + crema + amarillo (`assets_hm.css:2-7`) | Identidad clara, contraste alto, nada genérico. | S |
| K2 | Anton + Barlow Condensed + Barlow | Voz de motorsport correcta. | S |
| K3 | Concepto de telemetría del hero (tacómetro, 0 a 300 ft, FULL PULL) | La idea más original del sitio. Mejorar la ejecución, no la idea. | S |
| K4 | Añadir al carrito con talla desde el home | Reduce clics en merch de evento. | S |
| K5 | Ficha técnica tipo plano | Distintiva y buscable. | S |
| K6 | Historia real de la página del equipo | Mejor activo de copy del sitio. | S |
| K7 | Facade de YouTube, formularios con labels/autocomplete, skip link, `minmax(0,1fr)` | Buenas bases técnicas. | S |
| K8 | Estado vacío honesto de patrocinadores | Copia que convierte sin mentir. | S |

### FIX (arreglar en el tema actual)

| # | Qué | Dónde | Esfuerzo |
|---|---|---|---|
| F1 | Eliminar todos los placeholders (B1) y alinear la línea de tiempo 2026 | index, sponsors, contact, spec-sheet, schedule | S |
| F2 | Apagar el bundle hasta crear el producto Crew Pack con `compare_at_price` | `templates_index.json:41-42` | S |
| F3 | Quitar "MOST POPULAR" y "LIVE" falsos; verificar stats de patrocinio | `sections_hm-sponsor-body.liquid:31`, `sections_hm-hero.liquid:14`, `templates_page.sponsors.json:22-44` | S |
| F4 | `prefers-reduced-motion` global: detener rAF, tractor, speed-lines, marquee, galería, Ken Burns, cromado; botón de pausa en galería | `assets_hm.css`, `assets_hm.js` | S |
| F5 | Reescribir el bucle del hero sin lecturas de layout, con `IntersectionObserver` y cancelación | `assets_hm.js` | M |
| F6 | Fuentes: autoalojar woff2, quitar Google Fonts, apagar Assistant | `layout_theme.liquid:14-16,67-69,81-85,298-307`, `config_settings_data.json:13,15` | M |
| F7 | Imágenes: subir a Archivos (horizontales para banners), asignarlas en cada sección; fallback con `width/height`; cutout a WebP; `fetchpriority="high"` y `eager` en el hero de cada página | `snippets_hm-img.liquid`, todas las secciones | M |
| F8 | Cargar `hm.css` después de `base.css`; `theme-color`, `color-scheme: dark`, favicon | `layout_theme.liquid:7,70,287` | S |
| F9 | JSON-LD: `SportsTeam` + `WebSite` en layout, `Event` en calendario | `layout_theme.liquid`, `sections_hm-schedule-page.liquid` | M |
| F10 | Contraste: subir `--hm-dim` en el hero a `#A8A59A`, bordes de inputs a `#6E6B62` o más claro | `assets_hm.css:4,73,115,224` | S |
| F11 | `scroll-margin-top: calc(var(--hm-header) + 16px)` en anclas; `text-wrap:balance` en títulos; `tabular-nums` en telemetría y precios; `line-height` 0.95 a 1 en display | `assets_hm.css` | S |
| F12 | Texto accesible del h1 del home y `aria-live="polite"` en mensajes de formulario | `sections_hm-hero.liquid:5`, formularios | S |
| F13 | Tokens: mover hex y `font-family` en línea a `hm.css` y clases | sponsor-body, spec-sheet, team-page, schedule, contact | M |
| F14 | Captura: formulario en la página de calendario, incentivo, opción SMS con consentimiento, signup en footer | `sections_hm-schedule-page.liquid`, `sections_hm-footer.liquid`, `sections_hm-cta-cards.liquid` | M |
| F15 | Patrocinio: preseleccionar tier desde "CLAIM THIS SPOT", campos de presupuesto, media kit descargable, mockup de logo en tractor | `sections_hm-sponsor-body.liquid` | M |
| F16 | Menos eyebrows numerados y menos inclinación/cromado (reservar a 2 momentos) | `templates_index.json`, `assets_hm.css:15-17` | S |
| F17 | Redes: llenar Instagram/Facebook/TikTok/YouTube en ajustes y en la galería, o esconder la sección | `config_settings_data.json:111-119`, `templates_index.json:134-135` | S |
| F18 | Decidir el "f#cking evil" antes de salir a buscar patrocinio | `templates_page.spec-sheet.json:30`, `templates_page.about.json` | S |

### REBUILD (rehacer)

| # | Qué | Por qué | Esfuerzo |
|---|---|---|---|
| R1 | **Página de producto `hm-product`** con el lenguaje del sitio, `product-form` AJAX, guía de tallas, promesas de envío, historia corta, fotos en contexto | Hoy es Dawn blanco con Assistant: el punto de venta rompe la marca. | L |
| R2 | **Carrito drawer `hm-*`** con barra de envío gratis y upsell | Conectar el ADD TO CART del home con feedback real. | M |
| R3 | **Hero v2**: foto o video loop real de la máquina + telemetría ligada al scroll (el visitante "tira" del trineo hasta 300 ft), sonido opcional, versión estática para movimiento reducido | Es el salto de "tema personalizado" a "sitio de premio". | L |
| R4 | **Página de contraseña de marca** con foto, cuenta atrás al lanzamiento real y waitlist etiquetada | Hoy es la única página pública y es Dawn por defecto. | S |
| R5 | **Calendario real** con eventos como bloques (fecha, lugar, circuito, resultado), JSON-LD `Event`, y "añadir al calendario" | Convierte la página "COMING SOON" en contenido que vuelve a traer visitas. | M |
| R6 | **Ritmo del home**: romper la secuencia plantilla (hero → promesas → 3 tarjetas → banner → video → galería → split → 2 CTAs → footer 4 columnas); p. ej. fusionar máquina + video en una sola historia de scroll y bajar la tienda justo después | Hallmark gate 8 y 42/43. | L |

---

### Anexo: conteo Hallmark

**Críticos (9):** placeholders en producción · métricas/prueba social inventadas ("LIVE", "MOST POPULAR", stats sin fuente) · gradiente en titulares (`.hm-chrome`) · LCP con lazy-load (schedule/contact) · estructura plantilla del home · nav IA · footer IA · movimiento sin reduced-motion · producto fuera del sistema (blanco puro + fuente ajena).
**Mayores (17):** eyebrow en cada sección · inclinación tipo cursiva en todos los títulos · 3 columnas iguales repetidas · tokens improvisados en línea · anclas bajo header sticky · rAF con layout por frame · fuentes duplicadas · imágenes sin srcset · fotos verticales en banners horizontales · contraste en telemetría · contraste de bordes de inputs · galería sin pausa · falta de JSON-LD · h1 solo SVG · placeholders "Jane Smith"/"(555)" · bundle roto · captura sin incentivo ni SMS.
**Menores (12):** sin `text-wrap` · sin tabular-nums · `line-height` < 1 en mayúsculas · cursiva sintetizada en Anton · reglas CSS duplicadas · `!important` en cadena · numeración de beats · `themeRefresh` en URL · nocookie · `theme-color` vacío · sin favicon · animaciones de Dawn sin uso.
