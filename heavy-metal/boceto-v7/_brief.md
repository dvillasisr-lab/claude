# Brief boceto v3 (leer COMPLETO antes de escribir)

## Feedback de la dueña sobre v2 (todo es obligatorio)
- Letras y bloques demasiado grandes; secciones que se cortan o desperdician espacio. → Usar la escala de hm.css (títulos 24 a 30px, hero 48px máx, texto 14 a 16px). NINGUNA sección más alta que una pantalla de laptop (máx. ~ 100svh menos el header). Padding de sección var(--sect) (40 a 64px), nada de 120px.
- Logo a la IZQUIERDA (ya en hm.js).
- Categorías y producto juntos en UNA sección que quepa en pantalla.
- Menos merch en la home (una sola fila de producto) y un orden lógico sin brincos de tema.
- "Ride With The Evil One" más chico.
- Footer con todas las políticas (ya en hm.js). Copyright: "© 2026 Heavy Metal Pro Stock: The Evil One · Waterloo, WI".
- Los links NO deben mandar a la home ni a mitad de página: usar URLs reales (shop.html?cat=tees, product.html?p=id, ride.html, policies.html?p=privacy). Nada de anclas entre páginas. hm.js ya fuerza que cada página abra arriba.
- Pocos llamados a la acción: UNA acción principal por página. Una sola lista de correo ("Hook Alerts", en el footer y en Schedule); el patrocinio solo en Sponsors.
- Le gustan: skims-mexico.com (secciones que no se cortan, banner, menú, tamaño de letra, footer), el grid de skims-mexico.com/collections/swim, las fotitos de categoría de kyliecosmetics.com, y la página de términos de SKIMS (lista lateral de políticas + texto).
- Usar la información y fotos REALES (ver _real-content.md). Placeholders solo para fotos de merch.

## Leer antes
- `/home/user/claude/heavy-metal/boceto-v3/_real-content.md` (contenido real: fotos, historia, equipo, patrocinio, ficha).
- `/home/user/claude/heavy-metal/analisis/06-skims-kylie.md` (medidas de SKIMS y Kylie).
- `/home/user/claude/heavy-metal/analisis/07-roast-v2.md` (roast; aplica lo que toque a tus páginas, sobre todo Parte B y C).
- `hm.css` y `hm.js` de esta carpeta (sistema compartido: no los edites; si necesitas algo, CSS local en tu página).
- Skim `/home/user/claude/.claude/skills/hallmark/SKILL.md`.

## Componentes que ya existen (usar, no rehacer)
- Header (logo izquierda, menú, búsqueda, cuenta, carrito), anuncio rotativo, mega menú, menú móvil, buscador predictivo, carrito con promos, selector rápido de talla, footer SKIMS con legales, banner de cookies: todo lo inyecta hm.js.
- `window.HM_CATALOG` (14 productos de ejemplo), `window.hmCard(p)` devuelve la tarjeta de producto (SKIMS + botón Kylie, abre selector de talla), `window.hmCats(actual)` devuelve las fotitos de categoría de 100px. Úsalos con un pequeño script después de hm.js para pintar grids, así todo es idéntico.
- `window.hmAdd(nombre, variante, precio)` agrega al carrito y lo abre.
- Clases: .wrap .sect .sect--white .sect--night .h-hero .h1 .h2 .h3 .label .lede .body .small .btn .btn--ghost .btn--light .link .badge .ph .ph--dark .photo .pgrid .card .cats .spec .field .input .consent .note .sect-head .grid .g2 .g3 .g4.
- Fotos reales: `<img class="photo" src="img/hm-xxx.webp" alt="descripción" loading="lazy" width height>` dentro de un contenedor con aspect-ratio. Todas son verticales 3:4 (1050x1400) salvo el recorte. Diseña para fotos verticales (columnas, dípticos), no para bandas 21:9.

## Esqueleto de página
`index.html` (página principal; se envuelve al publicar, SIN doctype/html/head/body):
```
<title>Heavy Metal · The Evil One</title>
<meta name="description" content="...">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&display=swap">
<link rel="stylesheet" href="hm.css">
<style>/* CSS local con variables de hm.css */</style>
<div data-hm-header data-current="home"></div>
<main id="main">...</main>
<div data-hm-footer></div>
<script src="hm.js"></script>
<script>/* JS local */</script>
```
Las demás páginas: documento completo (`<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><title>…</title><meta name="description" …>` + mismos links `</head><body>` + lo mismo). `data-current`: shop | machine | story | schedule | sponsors | account | policies | contact (o vacío).
Cada página: title y meta description propios, un solo h1, `<main id="main">`.

## Reglas
- Copy del sitio en inglés, corto, claro. Notas `.note` en español, máximo 2 por página.
- Nunca inventar cifras, fechas, reseñas, patrocinadores ni beneficios. Lo que falte: placeholder visible tipo "$XX" o una nota.
- Responsive a 390px sin scroll horizontal; foco visible; ids y labels; prefers-reduced-motion; sin emoji; sin el carácter "–".
- Pruébala con Playwright: chromium en `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`, `import { chromium } from '<npm root -g>/playwright/index.mjs'`, bloquea rutas de fonts.googleapis/gstatic, 1440x900 y 390x844, revisa capturas, errores de consola y scrollWidth. Para index.html envuélvelo en un archivo temporal con doctype y bórralo al final. Usa tu propia carpeta temporal (`/tmp/claude-0/<tu-página>/`), no compartas scripts con otros agentes.
- No edites archivos de otras páginas.
