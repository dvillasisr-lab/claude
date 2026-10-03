# Brief boceto v5 (leer COMPLETO antes de escribir)

Carpeta: `/home/user/claude/heavy-metal/boceto-v5/` (copia de v4). Tú mejoras SOLO tus archivos asignados. Lee también `_brief-v4.md` y `_brief.md` (reglas que siguen vigentes; donde digan boceto-v4 o v3, entiende boceto-v5), `_real-content.md` (al final hay "Datos nuevos (v5)"), y `hm.css` + `hm.js` completos (sistema compartido: NO los edites).

## Cambios globales ya hechos en hm.js/hm.css
- Nav: Shop, The Machine, Our Story, Schedule, **Pit Log** (log.html, página nueva), Sponsors. Barra de boceto con link a **editar.html** ("Cómo editas todo", página nueva solo para la dueña).
- Producto nuevo de **edición especial**: `lightning-night-tee` (cat 'limited', página `limited.html`). Categoría "Special edition" en las fotitos.
- `window.HM_SEASON` = 2026. En Shopify el año de temporada será UN ajuste global del tema; en tu JS usa `HM_SEASON` en vez de escribir 2026 cuando sea "la temporada actual" (fechas históricas como "Feb 2020" se quedan fijas).
- Mockups de prenda ahora genéricos, sin logo ni texto (la dueña no quiere íconos que digan "Heavy Metal"). Set descargable en `img/icons/` (tee, hoodie, cap, beanie, sticker, koozie × black/gray/bone).
- Footer con email heavymetalevil72@gmail.com y teléfono (920) 650-4374, y "The Evil One" entre comillas.
- Búsquedas populares automáticas (Trending = best sellers, sugerencias mientras escribe, búsquedas recientes del cliente).

## Reglas nuevas de la dueña (obligatorias)
- **“The Evil One” SIEMPRE entre comillas tipográficas** en todo texto visible, títulos, alt, meta y JSON-LD de tus archivos.
- Datos reales nuevos: email, teléfono, P.O. Box (ya en _real-content), Chris +20 años en el deporte, **ya hubo 3 o 4 exhibiciones** (nunca decir "no exhibitions"), Spotify de Fear of the Dark.
- Todo lo dinámico (pulls, wins, exhibiciones, contadores, paquetes, lugares del logo, ediciones especiales, bitácora) debe verse **editable sin código**: cada lista se pinta desde un array JS que simula su metaobjeto o blog de Shopify, y una `.note` corta dice dónde se edita (Contenido > Metaobjetos > X, o Contenido > Blog posts). Máximo 2 notas por página.
- Piensa en el futuro: donde haya historial (schedule, pit log, wins) agrega **filtro por año**.
- Sin "–" (en dash). Copy del sitio en inglés.

## Prueba obligatoria
Playwright a 390x844, 1024x768, 1440x900 y 1920x1080 (chromium `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`, `import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs'`, bloquea fonts.googleapis/gstatic). Revisa capturas (míralas de verdad), errores de consola, scrollWidth <= innerWidth, un solo h1, ninguna "–", "The Evil One" siempre entre comillas. Carpeta temporal propia en /tmp/claude-0/<tu-tarea>/.

## Entrega
Lista corta de qué cambiaste, decisiones y datos que faltan.
