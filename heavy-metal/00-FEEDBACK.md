# Heavy Metal "The Evil One": feedback y plan de mejora

Fecha: 30 sep 2026. Fuentes: Admin API de la tienda, código del tema en vivo (heavy-metal-tema-v12), 4 agentes de investigación. Detalle en `analisis/01` a `04`.

## Veredicto en una línea

La base es mejor que el 95% de los sitios de pulling (identidad oscura, telemetría, historia real), pero hoy **no vende, no rankea y no convence a un patrocinador** porque está cerrada, sin producto, con placeholders a la vista y sin prueba real.

## Lo que ya está bien (conservar)

- Concepto visual: negro mate, tipografía condensada (Anton + Barlow), lenguaje de telemetría y pista. Encaja con el tractor.
- Secciones propias ya hechas: hero, drop, la máquina, video, galería, equipo, patrocinios, spec sheet, schedule, contacto.
- **La historia es excelente y casi no se usa**: 12 años de construcción, el rayo que tumbó la luz al primer arranque, Cat 3208 V8 reverse flow llevado de 636 a 680 pulgadas cúbicas, el "hermano" belga Diesel Ross, entrada con Fear of the Dark de Iron Maiden.
- Fotos reales del tractor: un Challenger negro mate con look "Batmobile" y humo negro. Es la imagen más distintiva de todo el circuito.

## Problemas, por gravedad

### Críticos (bloquean ventas, Google y patrocinios)
1. **Tienda con contraseña**: Google ve solo `/password`, meta description vacía, sin JSON-LD.
2. **Cero catálogo**: 1 producto de prueba de $1 sin foto. El bundle "Crew Pack" no tiene producto y promete un ahorro que no existe.
3. **Placeholders visibles**: "$[X]", "[STORY...]", "HORSEPOWER UNKNOWN", "[YEAR]", "[EMAIL PENDING]", Instagram y Facebook vacíos.
4. **Menú principal** solo tiene Home, Catalog y Contact. THE TEAM, THE MACHINE, SCHEDULE y SPONSORS no se pueden encontrar.
5. **Prueba social sin sustento**: "LIVE TELEMETRY" es una animación, "5,000+ fans" y "10 states" no tienen fuente, "MOST POPULAR" sin patrocinadores. Un patrocinador serio lo nota.

### Mayores (calidad y rendimiento)
6. Fuentes cargadas dos veces (Google Fonts bloqueante + Assistant de Dawn). `hm.css` carga antes que `base.css`.
7. Imágenes como assets del tema, sin srcset, WebP ni medidas. Fotos verticales estiradas en banners horizontales. PNG recortado de 682 KB.
8. `hm.js` con un bucle rAF infinito que lee y escribe layout en cada frame: malo para INP y batería.
9. 15 animaciones y solo 1 respeta `prefers-reduced-motion`. Galería sin pausa (falla WCAG 2.2.2). Contraste del hero 3.94:1 (falla AA).
10. Página de producto, carrito y página de contraseña son Dawn sin tocar (fondo blanco, Assistant). Rompe la experiencia justo donde se paga.
11. El h1 del home es solo un SVG. Sin favicon, sin theme-color.

### Decisiones de marca pendientes
- La frase "This thing is f#cking evil." en spec sheet y equipo: buena para fans, riesgosa para patrocinadores corporativos (Fabick Cat, dealers). Recomiendo moverla a merch y quitarla de páginas de patrocinio.
- Choque de nombre: existe un "Heavy Metal Tractorpulling Team" europeo y la música. La marca SEO debe ser **Heavy Metal "The Evil One"** + **Pro Stock Wisconsin**.

## Qué dice el mercado

- **Nadie en pulling tiene un sitio premium.** Ningún equipo Pro Stock de BSTP tiene una web seria; el mejor es Beer Money (Shopify con blog y sponsors). El nicho está libre.
- Referentes a imitar en patrones, no en estética: Scout Motors (Awwwards E-commerce del año 2025), Bécane Paris, Carhartt WIP, Hoonigan (drops por evento, hub de video), Liquid Death (voz de marca), Gymshark y Ridge (página de producto).
- Argumento para patrocinadores: Full Pull Live (NTPA) reporta 500,000+ espectadores en streaming, especial en ESPN2 desde Tomah. WTPA reporta 50,000+ fans por temporada en Wisconsin.
- Prospectos naturales: **Fabick Cat** (el motor es Cat), Ritchie (Case IH), Hennessey (New Holland), K/M Sales, Renk Seeds, United Cooperative, Schaeffer, negocios de Waterloo y Tomah.
- Diferenciador SEO: **el único Cat 3208 V8 en una clase dominada por John Deere de 6 en línea**. Eso es contenido que Google y ChatGPT citan.

## Qué voy a mejorar

| # | Mejora | Objetivo | Esfuerzo |
|---|---|---|---|
| 1 | Hero v2: video real del pull en loop con fachada ligera, h1 de texto "Heavy Metal: The Evil One, Pro Stock pulling tractor" | Impacto + SEO + LCP | M |
| 2 | Historia "Lightning Strike" en scroll: 2014, 12 años, el rayo, 680 ci | Engagement + premios | M |
| 3 | THE MACHINE interactiva: tractor con hotspots (motor, turbo, llantas, peso) que muestran specs y el patrocinador de cada parte | Premios + patrocinio | M |
| 4 | Drops por evento con contador, stock limitado y límite por cliente | Ventas | S/M |
| 5 | Página de producto propia: galería por variante, guía de tallas, compra fija en móvil, "cada compra mueve el tractor" | Conversión | M |
| 6 | Micro patrocinio "Ride With The Evil One": el fan paga y su nombre va en el tractor y en un muro | Ventas + engagement | S |
| 7 | SPONSORS nivel profesional: cifras reales, mapa de calcomanías disponibles, 4 niveles, media kit, formulario | Patrocinios | M |
| 8 | SCHEDULE vivo con metaobjetos: próximo pull con cuenta regresiva, resultados, una URL por evento | SEO local + engagement | M |
| 9 | Alertas "Hook Alert" por correo y SMS antes de cada pull | Retención | S |
| 10 | Juego "¿Cuántos pies?": predicción del pull por evento, premio en merch | Engagement | M |
| 11 | Limpieza técnica: fuentes, imágenes responsive, JS sin bucle, movimiento reducido, contraste, JSON-LD (SportsTeam, SportsEvent, Product, FAQ) | CWV + SEO + a11y | S/M |
| 12 | Carrito drawer, página de contraseña y 404 con la marca | Consistencia | S |

## Datos confirmados (30 sep 2026)

- Facebook: https://www.facebook.com/heavymetalprostock/ . Dueño y piloto: Chris F.
- Primer tornillo: febrero 2020 (la idea nació en 2014).
- Temporada de pruebas: sin calendario ni resultados todavía.
- Caballos de fuerza: no se publican. Propuesta: mostrar "CLASSIFIED" en vez de "UNKNOWN".
- Merch: diseños propios, impresión bajo demanda con Printly.
- Fotos y videos: placeholders por ahora.

## Pendientes

1. Monto para envío gratis.
2. Instagram, TikTok o YouTube (conviene abrirlos con el mismo nombre).
3. Qué hacer con la frase "f#cking evil" (recomendación: solo en merch).
4. Cifras para patrocinio cuando existan (seguidores, vistas, pulls).
