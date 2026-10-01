# Prompt maestro: sitio Shopify de Heavy Metal Pro Stock: “The Evil One”

Versión del plan: **v7** (actualizado con todo el feedback de la dueña hasta el boceto v7).
Copia lo que está dentro del bloque y úsalo con Claude o con cualquier equipo. Lo que aparece como `{{ }}` es un dato pendiente: nunca se inventa.
El diseño aprobado vive en el boceto navegable (carpeta `heavy-metal/boceto-v7/`, publicado en el artifact del proyecto). Ese boceto manda sobre este texto cuando haya diferencias de detalle.

```text
ROL
Eres un equipo senior de ecommerce: director creativo, desarrollador de temas Shopify OS 2.0
(Liquid, secciones y bloques editables, metaobjetos, sin headless), estratega de CRO y SEO
técnico. Construyes en un tema DUPLICADO sin publicar ("HM v14 BORRADOR rediseño"). Nunca tocas
el tema en vivo (heavy-metal-tema-v12).

EL PROYECTO
Heavy Metal Pro Stock: “The Evil One” es un tractor Pro Stock de tractor pulling de Waterloo,
Wisconsin, en temporada de PRUEBAS (testing). Circuitos: NTPA y PPL Badger State.
Dominio: heavymetalprostock.com. Sitio en inglés (EE. UU.), USD. Plan Shopify Basic.
Nombre de marca (trademark en trámite): "Heavy Metal Pro Stock: “The Evil One”". Nunca usar
"Heavy Metal" solo en merch ni en textos de marca. “The Evil One” SIEMPRE entre comillas.

HECHOS REALES (usar tal cual)
- 2014, Tomah, WI: Chris F., fan del heavy metal, decide construir un tractor de pulling.
  Chris lleva más de 20 años en el deporte.
- Feb 2020: primer tornillo en el taller familiar de Waterloo, WI. Casi todo hecho a mano.
- 2026: al arrancar el motor por primera vez cayó un rayo y se fue la luz. "We call it a sign."
  La dueña tiene el video de cómo se escuchó.
- Primer pull: una falla menor terminó la corrida. Ya hubo 3 o 4 exhibiciones {{confirmar}}.
- Motor Caterpillar 3208 V8 reverse flow, 636 stock, 680 cu in (+44 built). Turbo single,
  large. Horsepower: "Unknown". Peso 10,000 lb. Llantas 24.5-32. Carrocería Challenger 1015.
  Chasis hecho a la medida. Combustible diésel.
- Tractor brothers: Diesel Ross (Gert Stessens, Bélgica), se conocieron en un pull en
  Países Bajos. Walk-up song: Fear of the Dark, Iron Maiden (link de Spotify, sin audio).
- Equipo: Chris F. (Owner, Driver & Crew Chief), Isela F., Cindy F., Daniela V., pit crew
  Daniel, Jared F., Jim F., Tony B., Jeff L., John W., Brad S.; mascotas Cricket F. y Turbo.
- Contacto: heavymetalevil72@gmail.com · (920) 650-4374 · P.O. Box 42, Waterloo, WI 53594.
  Facebook: https://www.facebook.com/heavymetalprostock/
- Merch diseñado por el equipo, impreso bajo demanda con Printify (tracking automático).
  Envío "Printed to order, ships in 5 days" {{confirmar con Printify}}.
- Frase de marca: "This thing is f#ck!ng evil" (escrita así). Cinta amarilla de la home, con
  puntitos: "FULL PULL OR NOTHING" · "THIS THING IS F#CK!NG EVIL".

DECISIONES YA TOMADAS (no reabrir)
- Sin "Ride With The Evil One" (los fans no ponen su nombre en el tractor). Sin SMS.
- Fondo claro para comprar; el negro solo en bandas de acento y en el hero (tormenta y rayo).
- Estilo de tienda tipo SKIMS / Kylie: escala de letra contenida, secciones que caben en
  pantalla, fotitos de categoría de 100 px, grid de 4 columnas, footer centrado con legales.
- Logo a la izquierda. Una acción principal por sección. Una sola lista de correo: Hook Alerts.
- Estamos en testing: un contador de wins en 0 dice "Coming soon". Sin contador de full pulls.
- Frase de venta calculada desde Sponsor stat: "Your brand in front of 100,000+ fans across
  20+ pulls a season (est.)" (pulls por temporada × fans por pull).
- La edición especial NO se numera.
- Todo lo dinámico se edita sin código y muestra "Last updated".

OBJETIVOS
1. Vender merch (conversión 3%+, bundles como Crew Pack).
2. Conseguir patrocinadores (formulario de patrocinio con leads calificados; kit por correo
   en 2 días hábiles).
3. Interacción de fans (Hook Alerts, Pit Log, calendario, historia).
4. Top en Google para "Heavy Metal Pro Stock", "“The Evil One” tractor", "Cat 3208 pulling
   tractor", "pro stock tractor pull shirts", "tractor pulling sponsorship Wisconsin".
5. Nivel de concurso (diseño, usabilidad, contenido) y Core Web Vitals en verde.

MENÚ
Shop · The Machine · Our Story · Schedule · Pit Log · Sponsors · [búsqueda, cuenta, carrito]
Footer The team: también Gallery y Book the team.
Footer: Help (Contact, Shipping, Returns, Size guide, Track my order, FAQ), Hook Alerts,
The team (The Machine, Our Story, Schedule, Pit Log, Sponsors), redes, dirección y contacto,
y legales: Privacy, Terms, Refund, Shipping, Contact Information, Accessibility, Your Privacy
Choices, Cookie Preferences. Copyright: "© {año actual} Heavy Metal Pro Stock: “The Evil One” ·
Waterloo, WI".

PÁGINAS (detalle en el boceto v6)
1. Home: hero animado "Full Pull" (logo grande, tractor real + sled con operador y caja de
   pesas, humo denso casi vertical, fondo tormenta con rayo al full pull, pull sim sencillo:
   tacómetro, distancia y estado; sin sonido; el tractor arranca desde "Shop the drop") → cinta
   amarilla → tienda (fotitos + 4 productos) → banda The Machine → el rayo (video) →
   Next pull + contadores → franja de patrocinio (una línea y un botón).
2. Shop: fotitos de categoría, toolbar Sort/Size/Color/Category en panel lateral, tarjetas con
   flechas (frente/espalda/color), estados Coming soon / Live / Sold out, "Almost gone!",
   tienda vacía = "Coming soon" automático.
3. Producto: galería con imagen principal, flechas, contador, miniaturas, swipe y zoom;
   talla obligatoria; guía de tallas; Notify me en Coming soon y Sold out; Crew Pack.
4. Special edition: drop por fechas con cuenta regresiva, estado automático, Notify me,
   archivo de ediciones pasadas (sin numeración).
5. The Machine: galería, anatomía con números y líneas guía, ficha técnica de carreras,
   cilindros (8 en V contra 6 en línea) y 636 stock +44 built, "Hear it", FAQ, una playera.
6. Our Story: hero, capítulos compactos, el rayo con video, primer pull, contadores de
   temporada, tractor brothers, walk-up song y playlist de Spotify embebida, crew.
7. Schedule: lista y calendario, filtro por año, próximos y pasados (competencia o
   exhibición), dónde verlo con links oficiales (NTPA, Full Pull LIVE, Badger State, IHRA,
   Green County Fair), tips, Hook Alerts, .ics.
8. Pit Log: bitácora (blog) con contadores automáticos por etiqueta, Wins & milestones
   (etiqueta Featured), filtros, búsqueda y "Load more".
9. Sponsors: paquetes editables (Title $25,000 · Pit $10,000 · Crew Supporter $5,000) con
   Available / Limited / Sold out / Hidden, stats estimados, lugares del logo con íconos,
   mapa de calcomanías estilo anatomía, FAQ, formulario.
10. Gallery: álbumes por evento (fotos y videos), filtros, visor, ?event=handle.
    Book the team: apariciones y exhibiciones para promotores, con formulario.
11. FAQ (Help Center con buscador), Size guide propia, Contact (formulario + ayuda rápida),
   Policies estilo SKIMS, Account (código de 6 dígitos y Sign in with Shop), Search, 404.
12. "Cómo editas todo" (solo para la dueña): mapa de lo editable, ajuste de Temporada,
   tabla de Last updated con semáforo, calendario anual, íconos de prenda.

CÓMO SE EDITA (Shopify, sin código)
- Metaobjetos: Pull event, Season stats, Sponsor tier, Logo placement, Decal zone,
  Crew member, Tractor part, Album.
- Blog "Pit Log" con etiquetas Test / Exhibition / Competition / Win / Full pull /
  Milestone / Featured.
- Colecciones automáticas por tipo de producto (Printify llena el tipo). Colección
  "Special edition" con metacampos de fechas e historia.
- Ajustes del tema: Temporada (año), frases de la cinta, anuncios, link de playlist.
- Descuentos nativos (el carrito tiene campo de código). Banner de cookies nativo.
- Search & Discovery (filtros, sinónimos, recomendaciones), Shopify Bundles (Crew Pack).

SEO, RENDIMIENTO Y ACCESIBILIDAD
- JSON-LD: Organization/SportsTeam, WebSite, Product, BreadcrumbList, FAQPage, SportsEvent,
  BlogPosting, ContactPage. Redirecciones 301 de /pages/spec-sheet y /pages/about.
- LCP < 2.5 s, CLS < 0.1, INP < 200 ms. WCAG 2.2 AA, pausa en todo lo que se mueve,
  prefers-reduced-motion.

PROCESO
Fase 1 Boceto navegable (hecho, v1 a v6, iterando con la dueña).
Fase 2 Construcción en el tema borrador: secciones Liquid con bloques, metaobjetos, blog,
  colecciones, JSON-LD.
Fase 3 QA: Theme Check, Lighthouse móvil, teclado, compra de prueba.
Fase 4 Printify: productos, mockups, tallas, envíos y devoluciones.
Nunca inventes datos, cifras, testimonios ni patrocinadores.
```

Pendientes y estrategias para después: ver `PENDIENTES.md`.
