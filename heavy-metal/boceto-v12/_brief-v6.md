# Brief boceto v6 (leer COMPLETO antes de escribir)

Carpeta: `/home/user/claude/heavy-metal/boceto-v6/` (copia de v5). Edita SOLO tus archivos. Lee `_brief-v5.md` (y lo que referencia), `_real-content.md`, y `hm.css` + `hm.js` completos (NO los edites). La versión anterior de cada página está en `../boceto-v5/` y `../boceto-v4/` por si hay que regresar algo.

## Ya hecho en hm.js/hm.css (no repetir)
- Bugs arreglados: el menú móvil quedaba debajo del fondo oscuro y no se podía picar; el contorno de las fotitos de categoría se cortaba; las páginas no siempre abrían arriba.
- Cada producto tiene `status`: 'live' | 'soon' (Coming soon) | 'soldout', y `left` (unidades; 5 o menos muestra "Almost gone!"). `hmCard` ya pinta badge y botón según el estado ("Notify me" en soon/soldout, liga a `producto#notify`).
- Tarjetas con flechas ‹ › y puntitos para ver frente / espalda / otro color.
- `window.hmComingSoon()` devuelve el bloque "Coming soon" para cuando la tienda no tiene merch. `?empty=1` en la URL simula la tienda vacía (HM_CATALOG queda en []).
- `window.hmMock(p, size, view, colorName)`: view 'back' dibuja la espalda. Las prendas dicen "HEAVY METAL PRO STOCK" / “THE EVIL ONE” (nombre en trámite de registro; nunca "Heavy Metal" solo en merch o textos de marca). La merch color hueso ya tiene contorno para que no se pierda.
- Carrito con campo "Discount code" (nativo de Shopify, sin app).

## Reglas de la dueña (todas obligatorias)
- “The Evil One” siempre entre comillas. Nombre de marca en textos: "Heavy Metal Pro Stock" (no "Heavy Metal" solo) en títulos, meta, JSON-LD y copy de marca; el logo se queda.
- La frase es **"This is f#cking evil"** (así, en cualquier lugar donde aparezca).
- Estamos en **testing**: si un contador de wins está en 0, se muestra **"Coming soon"**, nunca "0".
- **No prometer cifras**: en frases de venta usa "XX+ fans across XX pulls" (valores desde datos editables), no cifras escritas.
- No repetir en una sección información que ya está en otra página.
- La edición especial NO va numerada.
- Todo lo dinámico se pinta desde arrays que simulan metaobjetos/blog, con nota de dónde se edita. Máximo 2 notas por página.
- **"Last updated"**: donde haya información que cambia (schedule, pit log, paquetes, stats, políticas, playlist) muestra "Last updated: <fecha>" desde datos, y regístralo en un comentario `<!-- last-updated: nombre -->` cerca, para que editar.html los liste.
- Sin "–". Copy del sitio en inglés.
- Imagina que cada bug cuesta mil millones: prueba todo con clics reales (botones, tabs, flechas, formularios, menú móvil, teclado).

## Prueba obligatoria
Playwright a 390x844, 1024x768, 1440x900 y 1920x1080 (chromium `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`, `import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs'`, bloquea fonts.googleapis/gstatic). Mira las capturas, errores de consola, scrollWidth <= innerWidth, un solo h1, sin "–", comillas, y haz clic en cada control interactivo de tu página. Carpeta temporal propia en /tmp/claude-0/<tu-tarea>/.

## Entrega
Lista corta de qué cambiaste, decisiones, datos que faltan y bugs que encontraste fuera de tus archivos (no los arregles, repórtalos).
