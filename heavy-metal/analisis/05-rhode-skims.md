# 05 · Patrones de compra: rhode y SKIMS aplicados a Heavy Metal

Fecha: 30 sep 2026. Fuentes: HTML y CSS descargados de rhodeskin.com (tema Liquid, `theme.css`) y skims.com (Hydrogen/Oxygen + Tailwind), más lectura de home, colección y producto.
Marcas: **[V]** verificado en HTML/CSS hoy · **[C]** conocimiento previo o inferencia (el grid de SKIMS se pinta con JS, así que partes del card vienen de memoria).
Objetivo: copiar la mecánica de compra, no la marca (ni fuentes con licencia, ni fotos, ni copy).

---

## 1. Header

| | rhode | SKIMS |
|---|---|---|
| Barra de anuncio | 2 mensajes rotando: "GET A HIGHLIGHT MILK SAMPLE IN YOUR ORDER" / "free US shipping on orders over $45" [V] | "Free Shipping on Domestic Orders $75+" + "Sign Up for Email & SMS" + selector USD [V]; segunda línea "Join SKIMS Rewards for Free Returns" [V] |
| Logo | Wordmark en minúscula, centrado [V por fetch, C en detalle] | Wordmark a la izquierda [V] |
| Nav | Solo 3: SHOP / ABOUT / FUTURES [V] | 9 ítems: New, NikeSKIMS, Best Sellers, Collections, Clothing, Bras, Underwear, Shapewear, Mens, Accessories, Sale [V] |
| Iconos | **Palabras, no iconos**: SEARCH / ACCOUNT / CART (0) [V] | Iconos finos: búsqueda, favoritos, cuenta, bolsa [V] |
| Mega menú | SHOP abre tabs de categoría (Featured, Skin, Lip+Cheek, Sets, On The Go, Award Winners) y debajo **un carrusel de productos con foto, nombre y tagline** (`Header-mega-menu-productsSwiper`) [V] | 3 columnas de texto: Style / Color o Collection / guía (Fabric Guide, Bra Guide) + 1 tarjeta editorial con foto y frase [V] |
| Sticky | Header `transparent` sobre el hero en home, se vuelve sólido al hacer scroll [V clase, C comportamiento] | Sticky sólido blanco, barra de anuncio se va con el scroll [C] |

Patrón a llevar: nav de 3 a 5 palabras + mega menú que **muestra producto**, no listas largas.

## 2. Color

- **rhode [V]**: texto `#67645E` (gris topo cálido, 216 usos en CSS, nunca negro puro), secundario `#84827E`, fondo tarjetas y buybox `#F1F0ED` (hueso), bordes `#DDDEDC` / `#C4C4C4`, blanco `#FFFFFF` de página. Acento casi nulo (marrón `#643A2A` solo en pill de regalo).
- **SKIMS [V]**: texto "onyx" `#2D2A26` (casi negro cálido), fondo `#FFFFFF` y gris cálido `#FAF8F5`, crema `#F7F4F0` / `#F0EBE4` / `#E8E0D5`, borde `#E8E5DF`, acento "sienna" `#986B58` (pulso del carrito), error `#CD2D2D`, verde éxito `#007963`.
- Producto sobre fondo: rhode foto de producto sobre hueso liso, sin sombra; SKIMS foto de modelo a sangre sobre gris cálido de estudio. En ambos la **imagen hace el color**, la UI es neutra [V/C].
- Secciones oscuras: casi no existen. SKIMS usa bloques de campaña a sangre (foto oscura con texto blanco encima) y ese es su único "negro" [C]. rhode, ninguno.

## 3. Tipografía

- **rhode [V]**: sans grotesca "Swiss" para todo + display "Rektorat Heavy" puntual. Nombres de producto en MAYÚSCULAS, tagline en caja normal debajo. Tamaños chicos: 16px, 14px, 13px, 12px dominan. Tracking +0.02 a +0.04em en mayúsculas, -0.02em en titulares grandes.
- **SKIMS [V]**: una sola familia sans ("T-Star", fallback Helvetica), tracking +0.025em casi en todo, mucho uppercase (43 reglas). Nombre de colección en MAYÚSCULA + estilo en minúscula ("FITS EVERYBODY balconette bra") [V].
- Jerarquía de card: nombre 12 a 14px uppercase > tagline o color 12px gris > precio 12 a 14px mismo peso, **sin negrita ni tamaño grande en el precio** [V/C]. Los titulares grandes solo viven en hero y banners.

## 4. Home (arriba a abajo)

**rhode** [V] (muy corta, unas 6 pantallas):
1. Hero a sangre (foto + producto + sello de premio), 1 CTA.
2. Fila carrusel "Shop rhode" (5 productos) con card completa y botón BUY.
3. Fila "Shop Skin". 4. Fila "Shop Lip + Cheek". 5. Fila "Shop Sets". 6. Fila "Shop On The Go".
7. Fila "Award Winners" (premio como titular de la card).
8. Footer mínimo (ABOUT, FUTURES, IMPACT, FAQ, ACCOUNT, país).
La home **es el catálogo**: cada fila es una categoría con su enlace "Shop X". Sin UGC, sin blog.

**SKIMS** [V/C]:
1. Hero campaña a sangre (colab/lanzamiento con fecha).
2. Tiles de categoría (Pajamas, Tops, Pants, Matching Sets) en grid de 4 [V].
3. Best Sellers en carrusel.
4. Segundo bloque campaña (NikeSKIMS) + fila de producto.
5. Frase de marca corta. 6. Footer denso (Help, More, redes, newsletter).

## 5. Colección

- **Grid SKIMS [V]**: `grid-cols-2` móvil / `md:grid-cols-4` escritorio, gap horizontal **1px** y vertical 24px: fotos casi pegadas, texto respira. Pills de subcategoría arriba (T-Shirt, Push-Up, Bralettes...) + links "Find Your Size" / "The Bra Guide" + breadcrumb. FAQ SEO al final [V]. Filtros en drawer lateral y sort en dropdown ("Filter", "Sort") [C].
- **Grid rhode [V/C]**: tabs de categoría (las mismas del mega menú) en vez de filtros; sin sort ni facetas (catálogo chico). 4 columnas escritorio, 2 móvil [C].
- **Ratio de imagen**: rhode `aspect-ratio: .78` (≈ 4:5) [V]; SKIMS `4/5` y `9/13` (más alto, para modelo) [V].
- **Anatomía del card**:
  - rhode [V]: badge arriba izq. ("only at rhode", "New", "New Size", "Limited edition", "SOLD OUT") > imagen con **segunda imagen en hover** > NOMBRE > tagline de 3 palabras ("Multipurpose Luminizer") > swatches de tono > botón ancho "BUY [producto] · $20" o "Join the Waitlist".
  - SKIMS [C]: imagen modelo, hover a foto de producto plano; debajo nombre, precio, "N colores" o swatches circulares 12px; quick add con tallas al hover en desktop; badges pequeños texto ("New", "Low Stock", "Best Seller").

## 6. Página de producto

- **Galería**: SKIMS columna vertical de imágenes grandes que scrollea mientras el buybox queda sticky a la derecha [V "vertical gallery", C sticky]. rhode imágenes + video de aplicación, buybox sobre fondo `#F1F0ED` (`--pdp-buybox-bg`) [V].
- **Buybox rhode [V]**: nombre + sello de premio > tagline > "4.5 out of 5 stars · 16,680 reviews" > selector "Shade: ribbon - sheer pink" (limitados arriba, core abajo, agotados marcados) > botón "BUY lip tint - $20.00" (precio **dentro** del botón) > sellos "Cruelty-Free • Vegan • Gluten-Free".
- **Buybox SKIMS [V]**: nombre > precio "$54" > color con nombre ("Onyx") y swatches > selectores de talla > botón que dice "Select a Size" hasta elegir y luego "Add to Bag" > "Free shipping $75+" y "Join SKIMS Rewards for Free Returns" bajo el botón.
- **Guía de tallas**: link junto al selector + calculadora propia en SKIMS [V].
- **Acordeones rhode [V]**: Benefits / Application / Key Ingredients / what's inside / ingredients. SKIMS [C]: Details, Fabric & Care, Size & Fit, Shipping & Returns.
- **Upsell**: rhode "LAYER YOUR LIPS" (rutina de 3 pasos con productos) [V]; SKIMS "Complete the Look" y "You May Also Like" [C].
- **Reviews**: ambos con Okendo [V]; SKIMS agrega barra de ajuste "Runs small / True to size / Runs large" [C].
- **Sticky ATC móvil**: barra inferior con precio y botón al pasar el buybox [C].

## 7. Carrito y detalles de conversión

- Cart drawer lateral derecho (no página) [C], con barra de progreso a envío gratis ($45 / $75) [C, umbral V].
- rhode: muestra de regalo automática ("GET A ... SAMPLE IN YOUR ORDER"), app de regalos por umbral (`freegifts`) [V].
- SKIMS: pulso color sienna al agregar al carrito (`--cart-pulse-color`) [V]; upsell de 1 fila dentro del drawer [C].
- Waitlist en agotados en vez de ocultar el producto [V]. Pago acelerado (Shop Pay/Apple Pay) en PDP y drawer [V css `accelerated-checkout`].
- Early access con login (rhode) y Rewards para devoluciones (SKIMS): el registro tiene un beneficio concreto [V].

## 8. Por qué se sienten premium y fáciles

1. Paleta de 3 neutros cálidos; nunca negro puro ni blanco frío en texto.
2. Tipografía chica, uppercase, con tracking. El producto es lo grande, no el texto.
3. Fotos consistentes: mismo fondo, misma luz, mismo ratio en todo el catálogo.
4. Pocas decisiones: nav de 3 (rhode), tallas con guía al lado, un solo CTA por card.
5. Precio y acción juntos ("BUY · $20"), sin hacer buscar el botón.
6. Todo el copy de card es de 2 a 4 palabras.
7. Aire: márgenes amplios en texto, gap mínimo entre fotos.

---

## Cómo traducirlo a Heavy Metal "The Evil One"

1. **Base clara**: página `#FFFFFF`, cards sobre hueso `#F1F0ED` o gris cálido `#FAF8F5`, texto casi negro cálido `#2D2A26`, gris secundario `#6F6C69`, bordes `#E8E5DF`. Negro mate `#111111` reservado para el tractor, no para la UI.
2. **Header estilo rhode**: barra de anuncio con 2 mensajes rotando (envío gratis desde X / próxima jalada con fecha), logo centrado, nav de 3: TIENDA / EL EQUIPO / CALENDARIO; a la derecha BUSCAR / CUENTA / CARRITO (0) en palabras. Transparente sobre el hero, sólido blanco al bajar.
3. **Mega menú con producto**: tabs Playeras / Gorras / Hoodies / Accesorios / Edición limitada y debajo un carrusel de 5 productos con foto. Nada de listas.
4. **Home corta (5 a 6 pantallas)**: hero a sangre con el tractor en humo (única sección oscura) > fila Best sellers > fila por categoría con "Ver X" > un banner oscuro "The Evil One" con foto de pista > fila "Edición temporada" > footer. Sin UGC ni blog al inicio.
5. **El humo vive en 2 lugares**: hero y un banner editorial a mitad. Nunca detrás de cards, precios o formularios.
6. **Grid**: 4 columnas desktop / 2 móvil, gap horizontal 1 a 4px y vertical 24px, imagen 4:5 sobre fondo hueso liso, producto plano; segunda imagen en hover = foto puesta en pits o pista.
7. **Card**: badge texto arriba izq. ("Nuevo", "Edición limitada", "Solo en pista", "Agotado"), NOMBRE uppercase 13px, tagline de 3 palabras ("Negro lavado, pesada"), swatches 12px, precio mismo tamaño. Quick add de tallas al hover en desktop.
8. **PDP**: galería vertical + buybox sticky; color con nombre ("Negro humo"); tallas en botones; "Guía de tallas" junto al selector; botón que dice "Elige tu talla" y luego "AGREGAR · $450"; bajo el botón envío y cambios; acordeones Detalles / Tela y cuidado / Talla y ajuste / Envíos.
9. **Upsell tipo rutina**: "Arma tu kit de pits" (playera + gorra + calcomanía).
10. **Conversión**: drawer con barra a envío gratis, calcomanía de regalo sobre umbral, waitlist en agotados, pulso de color de acento (rojo óxido o naranja escape, uno solo) al agregar.
11. **Tipografía**: una sans grotesca libre (Inter, Archivo o similar) uppercase con +0.025em; display condensada pesada solo en hero y banner oscuro.
