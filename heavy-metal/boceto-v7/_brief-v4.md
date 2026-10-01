# Brief boceto v4 (leer COMPLETO antes de escribir)

Carpeta de trabajo: `/home/user/claude/heavy-metal/boceto-v4/`. Es una copia de v3 ya publicada; la dueña la revisó y mandó feedback. Tú mejoras SOLO tus archivos asignados.

## Leer antes
- `_brief.md` (reglas de v3: siguen vigentes, salvo las rutas: ahora todo vive en boceto-v4).
- `_real-content.md` (contenido real).
- Tus archivos asignados COMPLETOS, más `hm.css` y `hm.js` (sistema compartido, ya actualizado para v4: NO los edites).
- Skim `/home/user/claude/.claude/skills/hallmark/SKILL.md`.

## Cambios globales ya hechos en hm.js/hm.css (no repetir)
- **Ride With The Evil One se eliminó por completo** (la dueña no quiere que los fans pongan su nombre en el tractor). ride.html ya no existe. Quita de tu página CUALQUIER mención, link, tarjeta, precio, FAQ o política de "Ride With", "name on the tractor", "add your name", "ride.html".
- **No habrá SMS.** Quita textos de SMS, TCPA, "text messages", casillas de SMS, "SMS Terms". Hook Alerts es solo email.
- Las tarjetas de producto y las fotitos de categoría ahora usan mockups planos de prenda (`window.hmMock(p)` devuelve un SVG). Si pintas una foto de merch suelta, usa `<span class="ph ph--mock">` + `hmMock(producto)` en lugar del placeholder rayado.
- Footer: Size guide → `sizes.html`, FAQ → `faq.html`. Políticas: privacy, terms, refund, shipping, contact, accessibility, choices, cookies (sin sms ni ride).
- Dirección real: **P.O. Box 42, Waterloo, WI 53594** (úsala donde vaya dirección; email y teléfono siguen pendientes).
- Caballos de fuerza: escribir **"Unknown"** (no "CLASSIFIED").
- La barra amarilla tiene un botón "Ocultar notas": las `.note` son solo para la dueña y NO se ven en el sitio real. Mantén máximo 2 notas por página, cortas.
- Radios y checkboxes ya tienen estilo propio en hm.css (no les pongas accent-color).

## Links oficiales verificados (usar tal cual)
- NTPA: https://ntpapull.com/ · calendario 2026: https://ntpapull.com/pullresults/Schedule/NTPA_ScheduleDynamic.php
- Full Pull LIVE (transmisión oficial NTPA, de pago): https://fullpull.live/ (app Full Pull en iOS y Android)
- Badger State Tractor Pullers (miembro PPL, Wisconsin): https://bstponline.com/ · eventos: https://bstponline.com/events/ · Facebook: https://www.facebook.com/badgerstatetractors/
- PPL ahora es IHRA Pro Pulling Series; transmisiones gratis 2026: https://www.ihra.com/pulling · YouTube: https://www.youtube.com/@ProPullingTV
- Green County Fair (Monroe, WI): https://greencountyfair.net/
- Heavy Metal en Facebook: https://www.facebook.com/heavymetalprostock/ · video Monroe: https://www.youtube.com/watch?v=HfJ5FAJJ5Ac
Links externos con `target="_blank" rel="noopener"` y un indicador visible (flecha ↗ o texto "opens in a new tab" en vh).

## Prueba obligatoria (Playwright)
Anchos 390x844, 1024x768, 1440x900 y **1920x1080** (la dueña usa pantalla grande: en v3 el hero de Story se rompía a lo ancho). Revisa capturas, errores de consola, scrollWidth <= innerWidth, un solo h1, ningún link a ride.html, ninguna "–". Arregla lo que veas antes de terminar.

## Entrega
Responde con: qué cambiaste (lista corta), qué decisiones de diseño tomaste y qué datos faltan. Sin rodeos.
