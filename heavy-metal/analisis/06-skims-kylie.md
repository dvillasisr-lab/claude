# 06 · SKIMS México + Kylie Cosmetics: spec replicable

Medido el 2026-10-01 con Chromium headless (1440x900 escritorio, 390x844 móvil), leyendo estilos computados y CSS del tema.
[V] = medido en el sitio. [C] = inferencia o conocimiento previo. Se copian patrones, no marcas, fotos ni fuentes con licencia.
Ojo: en skims-mexico.com 1rem = 16px (no 10px como en Dawn normal). Tema: Dawn modificado (`acf.css`). Kylie: tema propio con Vue + Algolia.

## 1. SKIMS home (https://www.skims-mexico.com/)

### Barra de anuncios [V]
- Alto 48px escritorio, 36px móvil. Fondo blanco, texto #2D2A26.
- Texto 12px Inter 400, line-height 16px; si es link va subrayado (offset 3px).
- Rota 3 mensajes cada 4s (slider con autoplay) + botón pausa a la derecha (x=1398). En móvil el texto se alinea a la izquierda.
- Clave: en escritorio el LOGO vive en esta fila (izquierda, x=24, 108x24px) y el mensaje va centrado. Es una fila de marca, no una tira de promo.

### Header [V]
- Segunda fila de 48px, sticky (`top:0`). Arriba del todo suman 96px (48 anuncio + 48 menú).
- Escritorio: menú a la IZQUIERDA desde x=24: New, (logo colab), Swim, Best Sellers, Clothing, Bras, Underwear, Shapewear, Mens, Sale. 14px Inter 600, alto de click 40px, separación ~16px.
- Iconos a la derecha, 24x24 cada 32px: buscar, cuenta, wishlist, carrito.
- En home el header es transparente sobre el hero, con texto blanco; al pasar el mouse por el menú se vuelve blanco con texto oscuro. El ítem activo se subraya en tono taupe.
- Móvil: logo izquierda (x=16, 108x24); a la derecha un buscador tipo píldora con lupa + "SEARCH" subrayado (82x27), wishlist, carrito y hamburguesa (28px) al final.

### Mega menú [V]
- Panel blanco a todo el ancho, se abre debajo del header (y=95), alto ~450px (varía con el contenido).
- Columna 1 (x=24): links grandes 14px/700 ("All Clothing", "All Loungewear", "Two Piece & Matching Sets"), cada 36px.
- Columna 2 (x=272): título 12px/700 ("Style") + 9 links 12px/400, cada 36px.
- Columna 3 (x=464): tarjeta promo con imagen cuadrada 178x178, título 12px/700 y texto 12px de 4 líneas.
- El resto del ancho queda vacío: mucho aire y alineado a la izquierda.

### Tipografía [V]
- Display: T-Star (condensada, se ve en mayúsculas), 400. Texto: Inter 400/600/700. letter-spacing del body: 0.04em.
- Hero H2 (`.h1`): 48px / 56px, ls 1.2px escritorio · 30px / 36px móvil.
- Texto manifiesto (`.h0`): 36px / 48px, centrado, máx. 768px de ancho.
- H1 de colección/página: 30px / 36px, ls 0.75px.
- Títulos de tarjeta de categoría (H3): 16px Inter 700 en mayúsculas.
- Párrafo del hero: 16px / 24px escritorio · 14px / 20px móvil. Link CTA "Compra aquí": 14px/700 subrayado.
- Microcopy (footer, legales, menú): 12px.

### Secciones del home (8 secciones, 0px de separación entre ellas) [V]
| # | Sección | Alto escritorio | Alto móvil |
|---|---|---|---|
| 1 | Hero video/foto (New Arrivals) | 100vh (900 en 900, 700 en 700, 1000 en 1000) | 100svh menos 36px (808) |
| 2 | Multicolumna 4 categorías | 535 | 600 |
| 3 | Banner Best Sellers | 672 (42rem fijo) | 448 (28rem) |
| 4 | Banner colab/campaña | 896 (56rem fijo) | 544 (34rem) |
| 5 | Texto manifiesto centrado | 304 | 310 |
| 6 | Marquee de beneficios (envío, devoluciones, 3 a 5 días) | 154 | 154 |
| 7 | Footer | 674 | 996 |

- Por qué "nunca se corta": solo el hero usa 100vh; los demás banners tienen alto fijo (672 y 896) menor o igual a una pantalla de laptop. Ningún bloque supera el viewport, así que siempre se ve completo. Regla para replicar: hero = 100svh menos el header; banners = min(56rem, 100svh); sin margen entre secciones.
- Hero: foto o video a sangre, overlay 10%, texto abajo a la izquierda (x=48, ~150px del borde inferior): H2 + 1 o 2 líneas + link subrayado. Controles de video abajo.
- Multicolumna: 4 tarjetas de 345px con 20px de gap, imagen 345x431 (4:5), título debajo a 8px. Sin padding lateral (a sangre).
- Marquee: ítems de 192px con icono 56x56 y texto 16px T-Star color #63574B.

### Footer (lo que más le gusta) [V]
- Fondo blanco, todo CENTRADO. Escritorio 674px de alto, ~65px de padding arriba, contenido a 48px de los lados.
- Fila 1, 3 columnas de 480 | 384 | 480px:
  - Izq. "AYUDA": título 16px T-Star mayúsculas (ls 0.4px) + 7 links 12px Inter, cada 28px.
  - Centro "ENTÉRATE PRIMERO": título 24px T-Star; texto 12px de 2 líneas (con incentivo 15% OFF); input 292x44 con borde 1px y botón cuadrado 44x44 oscuro (#2D2A26) con flecha; debajo consentimiento legal 12px con link en negritas subrayado "Términos y Privacidad".
  - Der. "CONOCE MÁS": Sobre Nosotros, Tiendas.
- Fila 2: redes centradas (Instagram, Facebook, X, YouTube, TikTok), iconos 24px cada 48px.
- Fila 3: razón social 12px centrada (primera línea en negritas: "Tienda Oficial México", luego quién opera).
- Fila 4: línea divisoria 1px, debajo 3 links legales a la DERECHA, 12px, separados ~44px.
- No tiene íconos de pago, ni selector de país o idioma, ni logo en el footer.
- Móvil (996px): primero el newsletter, luego acordeones "AYUDA" y "CONOCE MÁS" (filas de 57px, 16px Inter 700, chevron a la derecha, bordes de 1px arriba y abajo), redes, razón social y links legales apilados y centrados cada 32px.

### Colores [V]
- Texto #2D2A26 · fondo #FFFFFF · crema #EEE6DA · gris cálido #63574B · gris tachado #787572 · rojo oferta #B6263D · cobalto de campaña #334FB4 · divisor #B6B1AD.
- Botones e inputs sin radio (0px), borde 1px. El badge tiene un radio de 1.6px.
- Popup de newsletter (Mailchimp) a los pocos segundos: imagen a la izquierda, panel oscuro a la derecha con botón taupe [V].

## 2. SKIMS colección (/collections/swim) [V]
- Header sólido blanco (no transparente). Encabezado de colección sin imagen, de 100px: H1 30px T-Star + descripción 14px/20px; breadcrumb 12px debajo.
- Toolbar: fila de 66px con líneas 1px arriba y abajo, palabras en mayúsculas 12px bold separadas ~20px: ORDENAR, GENDER, SIZE, STYLE, TYPE, COLOR, COLLECTION, SUPPORT LEVEL, SLEEVE LENGTH. En móvil la fila se desplaza en horizontal.
- La toolbar NO es sticky (solo el header lo es).
- Cualquier palabra abre un DRAWER a la derecha de 450px: "No filters selected" arriba, cerrar X; acordeones de 64px de alto (Sort primero, luego cada filtro) en 16px Inter 600 con chevron; pie fijo con botón oscuro a todo el ancho "VIEW 20 ITEMS" (~52px, T-Star). Overlay gris sobre la página.
- Ordenar (dentro del drawer): Destacado, Más vendidos, Alfabéticamente A-Z y Z-A, Precio menor a mayor y mayor a menor, Fecha.
- Grid escritorio: 4 columnas de 347px, gap de 4px entre columnas y 24px entre filas, padding lateral 20px.
- Grid móvil: 2 columnas de 175px, gap de 1px, 0px entre filas.
- Paginación: scroll infinito de 20 en 20 (`?page=2`). No hay banners dentro del grid. Abajo, un carrusel "featured collection" de 367px.
- Tarjeta (de arriba hacia abajo):
  - Imagen 347x501 (proporción ~0.69, casi 2:3), fondo gris claro, sin radio.
  - Al hover (≥990px) se cambia a la 2a foto con opacidad.
  - Badge abajo a la izquierda sobre la foto: "New" o "50% Off", 10px/700, blanco sobre #2D2A26, 22px de alto.
  - Fila de swatches cuadrados de 14x14 con 6px de gap (con borde si está activo) y corazón de wishlist a la derecha.
  - Categoría 10px Inter 500 mayúsculas (ej. "ICONIC SWIM").
  - Nombre 14px/20px T-Star.
  - Precio 10px Inter 500; en oferta, precio anterior tachado #787572 + precio nuevo #B6263D.
  - "Envío gratis" 11px #B6263D.
  - Texto con 16px de padding lateral. Sin botón de compra rápida.

## 3. Kylie Cosmetics (/en-mx/collections/best-sellers) [V]
- Barra de anuncios ~30px rosa lila, 15px/700 en minúsculas, centrada, con pausa a la derecha.
- Header de 112px: selector de país a la izquierda (texto + moneda en círculo), logo CENTRADO (194x51), iconos a la derecha (wishlist, cuenta, buscar, carrito, ~24px cada 50px). Menú centrado en una segunda línea, 17px en minúsculas, ~36px de separación.
- Fuente de texto: Tt-Chocolate; títulos: Univers Bold. Fondo de página #F8F1F4, texto #393939, malva #8E5F6A.
- Hero de colección: imagen a todo el ancho (~494px) con H1 34px Univers Bold mayúsculas blanco abajo a la izquierda (x=48). En móvil el H1 sale debajo de la imagen, en malva #B3848F, en 2 líneas.
- Navegación con fotitos (`visual-nav-blocks`):
  - Escritorio: CUADRADOS de 100x100 con radio 4px (no círculos), 120px por ítem (gap de 20px), alineados a la izquierda bajo el hero, 24px abajo.
  - Etiqueta centrada debajo (8px de gap): 17px Tt-Chocolate 600 en minúsculas, color malva #8E5F6A; si es larga baja a 2 líneas ("travel / essentials").
  - Breadcrumb 15px a la derecha en la misma fila.
  - Móvil: 60x60, 72px por ítem (gap 12px), etiqueta 12px/600, carrusel horizontal (`overflow-x:auto`, sin snap, sin flechas), el último ítem queda cortado para sugerir scroll.
- Toolbar: "152 products" 17px a la izquierda; a la derecha un select "featured" (173x30, borde 1px, radio 4px, chevron) y un botón "filter" (137x30). No es sticky.
- Grid escritorio: 4 columnas de 321px con gap de 20px, padding lateral 48px. Móvil: 2 columnas de 173.5px con gap de 15px.
- Tarjeta (321x408 en escritorio):
  - Radio 8px, sin sombra; imagen cuadrada 319x319 sobre gris; zona de info blanca con padding 14px arriba y 16px abajo/lados.
  - Badge "new" arriba a la derecha: 13px en minúsculas, píldora clara con radio 4px.
  - Estrellas (Bazaarvoice) ~14px + conteo "(1)" 12px. Si no hay reseñas, las estrellas salen grises.
  - Nombre 17px/600 en minúsculas a la izquierda y precio 17px/600 alineado a la derecha en la misma línea.
  - Subtítulo (tono o notas) 17px/400 en 1 línea con puntos suspensivos.
  - Al hover (escritorio) la info sube y aparecen un stepper de cantidad (110x40: −, 1, +) y un botón con contorno "add to cart - $135" (169x40, borde 1px #393939, radio 4px, 15px).
  - En móvil el botón "add to cart - $28" se ve siempre, a todo el ancho (40px).

## 4. SKIMS políticas (/pages/terms) [V]
- Banner de foto a todo el ancho de 400px arriba.
- H1 30px T-Star a la izquierda con línea de 1px #B6B1AD debajo.
- Dos columnas:
  - Lista lateral (x=20, 296px) con las 7 páginas de AYUDA en 20px T-Star, cada 36px. La activa lleva un subrayado de 2px sólido.
  - Contenido desde x=460, 880px de ancho: texto 12px/16px Inter, secciones numeradas con H3 12px/700 en mayúsculas ("1. DISPOSICIONES GENERALES.") y negritas en términos clave.
- Sin acordeones, sin índice interno y la lista lateral no es sticky. La página es larga (~8,900px).
- Móvil: la lista lateral pasa arriba como menú apilado y debajo va el texto completo (~14px).
- Mejora para HM [C]: índice sticky con anclas y H3 de 14px; 12px es poco legible para textos legales.

### Páginas legales que enlaza SKIMS [V]
- AYUDA (footer y lista lateral):
  - Política de Devoluciones /pages/returns
  - Devolver un Producto (portal externo de devoluciones)
  - Términos y Condiciones /pages/terms
  - Facturación (portal externo de facturas CFDI)
  - Guía de Tallas /pages/size-guides
  - Contacto /pages/contact
  - Promociones /pages/promociones
- CONOCE MÁS: Sobre Nosotros /pages/about · Tiendas /pages/store-finder-skims
- Barra inferior: Política de Privacidad /pages/politica-de-privacidad · Aviso de Privacidad /pages/aviso-de-privacidad · Envíos y Devoluciones /pages/shipping-returns
- En el newsletter: "Términos y Privacidad" (lleva a /pages/terms).
- Para HM en México [C]: Aviso de Privacidad (LFPDPPP), Términos (LFPC y NOM-COE), Envíos, Devoluciones, Facturación y Contacto con razón social.

## 5. Traducción a Heavy Metal "The Evil One" [C]
- Header 48 + 48: logo a la izquierda en la fila del anuncio, menú a la izquierda en 14px/600, iconos a la derecha. Mega menú: 2 columnas de links + 1 tarjeta promo de 178px.
- Escala de texto: 48 / 36 / 30 / 16 / 14 / 12px (móvil 30 / 14). Display condensada en mayúsculas para títulos, sans neutra para el texto.
- Secciones: hero 100svh menos el header, banners de 672 o 896 fijos (móvil 448 o 544) y 0px de margen entre secciones.
- Grid de producto como SKIMS (4 columnas, gap 4/24; móvil 2 columnas, gap 1) con imagen 2:3, hover con 2a foto, badge abajo a la izquierda y swatches de 14px.
- Del card de Kylie tomar: nombre y precio en la misma línea + botón de agregar al carrito visible en móvil.
- Fotitos de categoría estilo Kylie (100px escritorio, 60px móvil, radio 4px) arriba del grid: Playeras, Gorras, Sudaderas, Calcas, Accesorios.
- Footer clon de estructura: 3 columnas centradas (Ayuda | newsletter | Conoce más), redes, razón social, divisor y legales a la derecha; acordeones en móvil.
