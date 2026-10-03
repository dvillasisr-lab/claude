# Brief compartido boceto v2 (leer completo)

## Qué pidió la dueña
- NO todo en una sola página: sitio multipágina, cada tema en su página.
- Fondo negro cansa para comprar: tienda CLARA, tipo rhode (rhodeskin.com) y SKIMS.
- "La tienda es muy chiquita": la tienda debe ser protagonista, muchos productos, categorías, fácil de comprar.
- La marca sigue siendo Heavy Metal "The Evil One": las fotos del tractor (negro mate, humo) viven en bandas editoriales oscuras puntuales, no como fondo de todo.

## Archivos compartidos (usar, no duplicar)
- `hm.css`: tokens y clases. Solo sus variables; no inventes colores nuevos.
- `hm.js`: inyecta header con mega menú, menú móvil, carrito drawer y footer. Cualquier botón con `data-add="Nombre|Variante|$XX"` agrega al carrito.
- Análisis de referencia: `/home/user/claude/heavy-metal/analisis/05-rhode-skims.md` (si existe, aplícalo).

## Esqueleto de cada página
Página principal `index.html` (se envuelve al publicar, SIN doctype/html/head/body):
```
<title>Heavy Metal</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Archivo:wdth,wght@62..125,100..900&display=swap">
<link rel="stylesheet" href="hm.css">
<style>/* CSS de la página, solo con variables */</style>
<div data-hm-header data-current="home"></div>
<main>...</main>
<div data-hm-footer></div>
<script src="hm.js"></script>
```
Las demás páginas son documentos completos: `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><title>…</title>` + los mismos links, `</head><body>` + lo mismo, con `<script src="hm.js"></script>` al final del body. `data-current` = shop | machine | story | schedule | sponsors.

## Catálogo de ejemplo (nombres de ejemplo, precios siempre $XX)
| Producto | Categoría (ancla) | Colores | Badge |
|---|---|---|---|
| Evil One Tee | tees | Matte Black, Smoke Gray | Best seller |
| Lightning Strike Tee | tees | Matte Black | New |
| Full Pull or Nothing Long Sleeve | tees | Matte Black, Bone | |
| Cat V8 Spec Tee | tees | Smoke Gray | |
| 680 CI Hoodie | sweats | Matte Black, Smoke Gray | Best seller |
| The Evil One Crewneck | sweats | Bone | New |
| Crew Cap | hats | Black | |
| Evil One Beanie | hats | Black, Safety Yellow | |
| Little Evil One Kids Tee | kids | Matte Black | |
| Kids Hoodie | kids | Smoke Gray | |
| Sticker Pack | gear | | |
| Hook Alert Koozie | gear | | |
| Crew Pack bundle (tee + cap) | bundle | | Save $X |
| Ride With The Evil One (tu nombre en el tractor) | ride | | Limited |
Colores de swatch: Matte Black `var(--ink)`, Smoke Gray `#8C8A82`, Bone `#E9E6DC`, Safety Yellow `var(--accent)` (solo swatch).
Todas las tarjetas enlazan a `product.html`. Usar el componente `.card` de hm.css (foto 4:5 sobre `--tile`, badges arriba a la izquierda, botón "Quick add" que aparece al pasar el mouse con `data-add`, nombre en mayúsculas, precio y swatches).

## Hechos reales (solo estos)
Idea 2014 en Tomah, WI (Chris F, fan del heavy metal). Primer tornillo febrero 2020. Taller familiar en Waterloo, WI; casi todo hecho a mano. 2026 primer arranque: cayó un rayo y se fue la luz ("Some would call it a coincidence. We call it a sign."). Primer pull terminó antes por una falla menor; temporada de pruebas buscando el primer full pull. Cat 3208 V8 reverse flow, 636 a 680 ci, el único Cat V8 en una clase de John Deere de 6 en línea. 10,000 lb. Llantas 24.5-32. Carrocería Challenger negro mate. Caballos: CLASSIFIED (usar clase `.classified`). NTPA y PPL Badger State. Hermano en Europa: Diesel Ross (Gert Stessens, Bélgica). Canción de entrada: Fear of the Dark, Iron Maiden. Facebook: https://www.facebook.com/heavymetalprostock/ . Merch diseñado por el equipo, impreso bajo demanda. Sin calendario ni resultados todavía. Nunca inventar cifras, fechas, reseñas ni patrocinadores.

## Reglas
- Copy del sitio en inglés, corto y claro; notas `.note` en español (2 o 3 por página, máximo).
- Fotos/videos: `.ph` con `--ar` y `.ph__tag` que describe la toma; `.ph--dark` para fotos del tractor en bandas oscuras.
- Responsive hasta 390 px sin scroll horizontal; un solo h1; ids y labels en formularios; foco visible; reduced motion.
- Sin emoji, sin lorem ipsum, sin el carácter "–".
- Ritmo tipo rhode/SKIMS: mucho aire, grids limpios, poco texto, sin cajas con sombra en todo.
