# Prompt maestro: sitio Shopify de Heavy Metal "The Evil One"

Copia todo lo que está dentro del bloque y úsalo con Claude (o con cualquier equipo). Los campos entre `{{ }}` son datos que faltan confirmar; no se deben inventar.

```text
ROL
Eres un equipo senior de ecommerce: director creativo (nivel Awwwards), desarrollador de temas
Shopify OS 2.0 (Liquid, metaobjetos, sin headless), estratega de CRO y especialista en SEO técnico
y búsqueda con IA. Trabajas en el tema existente "heavy-metal-tema-v12" (base Dawn con secciones
hm-*). Conservas lo que funciona y rehaces lo que no.

EL PROYECTO
Heavy Metal, apodado "The Evil One", es un tractor Pro Stock de tractor pulling de Waterloo,
Wisconsin. Compite en NTPA y PPL Badger State, unas 20 competencias por temporada.
Dominio: heavymetalprostock.com. Idioma del sitio: inglés (EE.UU.). Moneda USD.

HECHOS DE MARCA (usar tal cual, son reales)
- Nació en 2014 en Tomah, Wisconsin. Chris, fan del heavy metal, decidió construir un tractor
  de pulling y el nombre nunca estuvo en discusión.
- 12 años de construcción de noches y fines de semana, en un taller familiar en Waterloo, WI.
  Casi todo es hecho a mano, nada es de catálogo.
- 2026: al arrancar el motor por primera vez cayó un rayo y se fue la luz. "Some would call it
  a coincidence. We call it a sign."
- Primer pull: un problema menor terminó la corrida antes de tiempo. Meta de la temporada:
  el primer full pull.
- Motor: Caterpillar 3208 V8 reverse flow, de 636 a 680 pulgadas cúbicas. El único Cat V8
  en una clase dominada por John Deere de 6 en línea.
- Peso 10,000 lb, llantas 24.5-32. Carrocería Challenger negro mate, humo negro.
- Hermano en Europa: Diesel Ross, Pro Stock de Gert Stessens (Bélgica).
- Canción de entrada: Fear of the Dark, Iron Maiden.
- Datos por confirmar: piloto {{PILOTO}}, caballos {{HP}}, redes {{REDES}},
  calendario {{CALENDARIO}}, resultados {{RESULTADOS}}, envío gratis desde {{MONTO}}.

OBJETIVOS (en este orden) Y CÓMO SE MIDEN
1. Vender merch: tasa de conversión objetivo 3% o más, ticket promedio con bundles.
2. Conseguir patrocinadores: formulario de media kit con leads calificados cada mes.
3. Interacción de fans: suscriptores de "Hook Alert" (correo y SMS), micro patrocinios,
   participación en el juego de predicción, tiempo en sitio.
4. Ser #1 en Google y citado por IA para: "Heavy Metal The Evil One", "Heavy Metal pro stock
   tractor", "Cat 3208 pulling tractor", "pro stock tractor pull shirts",
   "tractor pulling team sponsorship Wisconsin", y "<evento> tractor pull <año>".
5. Nivel para concursos (Awwwards, CSS Design Awards, Shopify): diseño, usabilidad,
   creatividad y contenido de 8 o más; Core Web Vitals en verde.

DIRECCIÓN DE DISEÑO
- Concepto: "Black Smoke Telemetry". El tractor es el héroe: negro mate, humo, tierra, acero.
  Estética de pantalla de carrera y ficha técnica industrial, no "granja" ni plantilla Dawn.
- Paleta: negro carbón, gris acero, blanco hueso y un solo acento (amarillo casco o naranja
  señal; elegir uno y usarlo solo para acciones y datos en vivo). Contraste AA en todo.
- Tipografía: Anton o similar condensada para titulares enormes; Barlow / Barlow Condensed para
  texto y datos; números tabulares para cifras. Máximo 2 familias, autoalojadas por Shopify.
- Movimiento con propósito: el scroll "jala" el tractor por la pista (barra de distancia en
  pies hasta 300 ft), cifras que cuentan hacia arriba, humo sutil. Solo CSS moderno
  (scroll-driven animations, view transitions) y JS mínimo. Todo con prefers-reduced-motion.
- Fotografía real únicamente. Nada de IA ni stock. Recortes del tractor, detalles del motor,
  el equipo con las manos sucias. Horizontales para banners, verticales para móvil.
- Voz: corta, segura, con humor oscuro de heavy metal, respetuosa con el público de campo y
  con patrocinadores. Sin groserías en páginas de patrocinio.
- Evitar: carruseles en el héroe, popups inmediatos, datos inventados ("live telemetry" falsa,
  "5,000+ fans" sin fuente), placeholders visibles, más de 3 apps con script.

ARQUITECTURA (menú principal)
SHOP · THE MACHINE · SCHEDULE · THE TEAM · SPONSORS · [carrito]
Footer: Hook Alert (correo y SMS), redes, políticas, contacto, patrocinadores.

PÁGINAS Y SECCIONES
1. HOME
   a. Hero: video real del pull en loop (fachada con póster, sin autoplay de YouTube pesado),
      h1 en texto: "HEAVY METAL" + "The Evil One · Pro Stock Tractor · Wisconsin".
      CTA 1 "Shop the Drop", CTA 2 "Sponsor the Machine". Barra con el próximo pull y
      cuenta regresiva (desde metaobjeto).
   b. Drop actual: 3 o 4 productos, stock limitado real, contador si hay fecha, bundle con
      ahorro real calculado.
   c. "Lightning Strike": historia en scroll en 4 momentos (2014, 12 años, el rayo, 680 ci).
   d. The Machine teaser: tractor recortado con 4 hotspots y cifras grandes.
   e. Watch it pull: video destacado + lista de clips.
   f. Ride With The Evil One: micro patrocinio con muro de nombres.
   g. Fans en la pista: galería UGC con #HEAVYMETALPULLING (con botón de pausa).
   h. Patrocinadores actuales + CTA a SPONSORS.
   i. Hook Alert: suscripción correo y SMS "Know before we hook."
2. THE MACHINE (spec sheet): tractor interactivo con hotspots (motor Cat 3208, turbo, llantas,
   peso, chasis). Cada hotspot: dato, foto de detalle y, si aplica, el patrocinador de esa
   parte. Tabla de specs, comparación "Cat V8 vs John Deere 6 en línea", FAQ.
3. SCHEDULE: metaobjeto "pull_event" (nombre, fecha, ciudad, liga, clase, link de boletos,
   stream, resultado en pies, posición, fotos). Próximo evento arriba, temporada en línea
   de tiempo, una URL por evento con schema SportsEvent. Botón "Add to calendar".
4. THE TEAM: historia completa, crew, Diesel Ross, timeline, fotos del taller.
5. SPONSORS: cifras reales, por qué pulling (streaming Full Pull Live 500,000+, ESPN2, fans
   rurales con alto poder de compra en maquinaria), mapa del tractor con zonas de calcomanía
   disponibles o tomadas, 4 niveles (Full Pull, Hook, Pit Crew, Hometown) con entregables,
   reporte de ejemplo post evento, FAQ, formulario "Get the media kit" que capture empresa,
   presupuesto e interés.
6. SHOP / colección: filtros simples, tarjetas con segunda imagen al pasar, etiquetas
   "Limited", "Event drop".
7. PRODUCTO: galería por variante, guía de tallas, compra fija en móvil, envío y tiempos
   claros, "Every order keeps us pulling", reseñas, cross sell del bundle.
8. Carrito drawer con barra de envío gratis, página de contraseña y 404 con la marca.

MECÁNICAS DE INTERACCIÓN
- Micro patrocinio "Ride With The Evil One" como producto: variantes Crew, Crew + Merch,
  Big Name (cupo limitado), In Memory Of. Nombre por line item properties; Shopify Flow
  crea la entrada en el metaobjeto del muro con moderación.
- "How many feet?": predicción del pull de cada evento; premio en merch.
- Drops por evento con cuenta regresiva y límite por cliente.
- Hook Alert antes de cada pull (Shopify Email / SMS).

SEO Y BÚSQUEDA CON IA
- Quitar la contraseña al lanzar; conectar Search Console y Bing; enviar sitemap.
- Plantillas de title y meta por tipo de página; alt descriptivo en todas las imágenes.
- JSON-LD: Organization + SportsTeam (memberOf NTPA y PPL Badger State), WebSite,
  SportsEvent por pull, Product, BreadcrumbList, FAQPage, BlogPosting.
- Contenido: blog "The Build" (motor, turbo, peso, cada pull), una página por evento y año,
  FAQ de pulling y del Cat 3208. Respuestas cortas y citables para IA.
- Enlaces: BSTP, NTPA, patrocinadores, ferias (Jefferson, Dodge, Green County, Tomah),
  medios locales, Beer Money y Diesel Ross.

RENDIMIENTO Y ACCESIBILIDAD (criterios duros)
- LCP menor a 2.5 s en móvil 4G, CLS menor a 0.1, INP menor a 200 ms.
- Imágenes con image_url + image_tag (srcset, WebP, width y height); héroe sin lazy load.
- Una sola carga de fuentes; sin bucles rAF infinitos; JS por sección y diferido.
- WCAG 2.2 AA: contraste, foco visible, pausa en todo lo que se mueve, aria-live en
  formularios, scroll-margin para header fijo.

PROCESO Y ENTREGABLES
Fase 1 Boceto: moodboard, wireframes de HOME, THE MACHINE, SPONSORS y PRODUCTO en desktop y
  móvil, como HTML navegable. Aprobar antes de seguir.
Fase 2 Diseño a detalle: tokens (color, tipo, espacio, movimiento), componentes y copy final.
Fase 3 Construcción: secciones Liquid con settings y bloques editables, metaobjetos,
  producto de micro patrocinio, JSON-LD, en un tema duplicado (nunca el publicado).
Fase 4 QA: Theme Check, Lighthouse móvil, prueba de teclado, prueba de compra.
Nunca inventes datos, cifras, testimonios ni patrocinadores. Si falta un dato, deja el
bloque oculto hasta que exista, nunca un placeholder visible.
```
