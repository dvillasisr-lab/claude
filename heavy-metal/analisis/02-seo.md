# 02. Estrategia SEO: Heavy Metal Prostock (heavymetalprostock.com)

Fecha: 30 de septiembre de 2026. Marco usado: skills `seo-audit` (prioridad: rastreo, técnico, on-page, contenido, autoridad), `schema` (JSON-LD fiel al contenido visible, validar siempre) y `ai-seo` (estructura extraíble, autoridad citable, presencia en terceros).

---

## 0. Resumen ejecutivo

1. **Hoy el sitio no existe para Google.** `https://heavymetalprostock.com/` redirige a `/password` (HTTP 200), con canonical a `/password`, `<title>` "Heavy Metal Prostock" y `meta description` vacía. El `og:description` sí está bien escrito ("Official merch of Heavy Metal "The Evil One", a Prostock pulling tractor from Waterloo, WI. Cat 3208 V8 power. Competing in NTPA and PPL Badger State."). El `robots.txt` que genera Shopify permite todo (`User-agent: * Allow: /`), así que al quitar la contraseña no hay bloqueo técnico.
2. **La marca casi no tiene huella web propia.** No encontré ninguna página indexada que relacione "Heavy Metal" + "The Evil One" + Waterloo + Cat 3208. Lo único cercano son dos clips de TikTok de Beer Money Pulling Team que mencionan un Pro Stock "Heavy Metal" en eventos de Badger State Tractor Pullers (uno en Highland, WI). No confirmé que sea este tractor. Esto es una oportunidad: la SERP de marca está vacía y se puede ganar rápido.
3. **El nicho es chico y de baja competencia SEO**, pero las SERP genéricas ("tractor pull shirts", "tractor pulling merch") las dominan marketplaces (Amazon, Etsy, Redbubble, Zazzle, TeePublic) y tiendas agregadoras (BAD Gear, Angry Duck). Las SERP informativas ("pro stock tractor pulling", "NTPA pro stock") las dominan ligas (ntpapull.com, propulling.com, bstponline.com), Wikipedia y medios (Drivingline, Engine Builder). Un equipo individual no va a ganar esas genéricas a corto plazo; debe ganar **marca + long tail local/evento + nicho técnico (Cat 3208 en Pro Stock)**.
4. **El motor Cat 3208 V8 es el diferenciador de contenido.** Las fuentes coinciden en que el Pro Stock lo dominan los John Deere de 6 cilindros en línea y que hay "muy pocos V8". Una página de especificaciones y un blog de la construcción sobre un V8 Caterpillar en Pro Stock es contenido único, citable por IA y enlazable por foros.
5. **Backlinks realistas y de alta relevancia:** Badger State Tractor Pullers (bstponline.com, miembro PPL), NTPA, fairs de Wisconsin (Jefferson, Dodge, Green County), Beer Money Pulling Team, The Monroe Times, Travel Wisconsin, patrocinadores locales de Waterloo/Jefferson County.

---

## 1. Quién rankea hoy (búsquedas del 30/09/2026)

Nota metodológica: resultados de WebSearch (EE. UU.). No tengo datos de volumen de herramientas (Ahrefs/Semrush); las estimaciones de volumen e intención de la sección 4 son cualitativas.

### 1.1 "heavy metal pro stock tractor"
| Tipo de página | Ejemplos |
|---|---|
| Descubrimiento de TikTok | [tiktok.com/discover/pro-stock-tractor-pulling](https://www.tiktok.com/discover/pro-stock-tractor-pulling) (incluye clips de @beermoneypullingteam sobre el "Heavy Metal" Pro Stock en Badger State, uno en Highland, WI) |
| Facebook de otro equipo homónimo | [Heavy Metal Tractorpulling Team](https://www.facebook.com/p/Heavy-Metal-Tractorpulling-Team-100057435251653/) (unos 3.083 "me gusta"; no pude ver ubicación ni clase; la grafía "Tractorpulling" sugiere un equipo europeo, sin confirmar) |
| Fotos de stock (ruido semántico) | [iStock](https://www.istockphoto.com/photo/tractor-pulling-heavy-metal-roller-on-dry-field-dust-behind-and-black-smoke-above-gm1023372638-274670657), [Dreamstime](https://www.dreamstime.com/tractor-pulling-heavy-metal-roller-dry-field-dust-behind-tractor-pulling-heavy-metal-roller-dry-field-dust-behind-image117660562) |
| Wikipedia | [Tractor pulling](https://en.wikipedia.org/wiki/Tractor_pulling), [Lucas Oil Pro Pulling League](https://en.wikipedia.org/wiki/Lucas_Oil_Pro_Pulling_League) |

Lectura: SERP débil y ambigua (colisión con "heavy metal" música/metales). Con dominio propio, schema Organization + sameAs y 3-5 menciones externas, el sitio puede ser #1 para la marca en semanas tras indexar.

### 1.2 "pro stock tractor pulling"
- [Wikipedia: Lucas Oil Pro Pulling League](https://en.wikipedia.org/wiki/Lucas_Oil_Pro_Pulling_League)
- [NTPA: Pulling 101](https://ntpapull.com/pulling-101/) (define Pro Stock: 10.000 lb, barra de tiro 20", 680 ci, 1 turbo, llantas 24.5x32, inyección de agua e intercooler permitidos)
- [Drivingline: Anatomy of a Pro Stock Tractor](https://www.drivingline.com/articles/anatomy-of-a-pro-stock-tractor/) (680 ci, más de 3.000 hp, turbos de 130 mm)
- [Performance Racing Industry: Load Warriors](https://www.performanceracing.com/magazine/featured/07-01-2022/load-warriors)
- [propulling.com/classes](https://www.propulling.com/classes/) (dice que la mayoría usa base John Deere de 6 en línea y que hay muy pocos V8)
- [BSTP: Prostock Tractors](https://bstponline.com/prostock-tractors/)
- [BTPA (Reino Unido)](https://tractorpulling.co.uk/competing-tractors/limited-pro-stock)

Tipo de página: informativa (reglamento, anatomía técnica, liga). Intención informacional. Un equipo gana aquí solo con contenido técnico de primera mano (la página "The Machine").

### 1.3 "tractor pulling merch" y 1.4 "tractor pull shirts"
- Marketplaces: [Redbubble](https://www.redbubble.com/shop/tractor+pulling+t-shirts), [Amazon](https://www.amazon.com/tractor-pulling-shirts/s?k=tractor+pulling+shirts), [Etsy](https://www.etsy.com/market/tractor_pulling_t_shirts), [Zazzle](https://www.zazzle.com/tractor+pulling+tshirts), [TeePublic](https://www.teepublic.com/t-shirt/22104548-id-rather-be-tractor-pulling)
- Merch oficial de equipos (agregadores): [BAD Gear, Official Pulling Team Merch](https://bad-gear.com/product-category/official-pulling-team-merch/) (Warpath 10,000 lb Pro Stock, Last Chance Pro Stock, Black Jack Pro Stock; 27,95 a 49,95 USD), [Angry Duck](https://www.shopangryduck.com/collections/tnt-truck-tractor-pulling) (colecciones de Beer Money, Miller Farms, etc.)
- Marcas: [IH Gear, Tractor Pull Division Tee](https://ihgear.com/products/ih-tractor-pull-division-tee-shirt)
- Imprentas custom: [BuyRaceShirts](https://buyraceshirts.com/custom-race-shirts/tractor-pull-shirts/), [Wicked Grafixx](https://www.wickedgrafixx.com/truck-tractor-pulling-t-shirts.html), [Excel Sportswear](https://www.excelsportswear.com/industries/tractor-pulling)

Tipo de página: categoría/listado de marketplace. Intención transaccional genérica. Difícil de ganar; mejor apuntar a "pro stock tractor shirt", "Wisconsin tractor pull shirt", "[nombre] pulling team shirt".

### 1.5 "pulling team sponsorship"
- [NTPA National Series Sponsors](https://ntpapull.com/sponsors/), [NTPA noticia CM Pulling Tires](https://ntpapull.com/cm-pulling-tires-migrates-gn-sponsorship-to-mini-division-for-2025/)
- [Tomah Tractor Pull, Sponsors](https://www.tomahtractorpull.com/sponsors-opportunities/), [WTPA Become a Sponsor](https://www.wtpapull.com/become-a-sponsor/)
- [Fullpull FAQs](https://www.fullpull.us/faqs), [RaceTeams.com pulling](https://raceteams.com/c/pulling), [PullTown](https://www.pulltown.com/)
- Foro: [pulloff.com, "Sponsoring a pulling team"](http://www.pulloff.com/phorum/read.php?2%2C56957%2C57183=) (patrocinio como gasto de publicidad; pide "media packet")

Tipo de página: páginas de patrocinio de ligas y eventos, marketplaces. Casi ningún equipo individual tiene una página de patrocinio bien hecha: oportunidad clara para `/pages/sponsors`.

### 1.6 "NTPA pro stock"
- [NTPA: 4.1 Limited Pro Stock entra al Grand National en 2026](https://ntpapull.com/ntpa-grand-national-circuit-to-add-4-1-limited-pro-stock-class-in-2026/), [Reglas 2025 (PDF)](https://ntpapull.com/wp-content/uploads/2024/12/2025-NTPA-Pulling-Rules-03-14-25.pdf), [Pulling 101](https://ntpapull.com/pulling-101/)
- [Engine Builder: NTPA powerplants](https://www.enginebuildermag.com/2017/03/ntpa-tractor-pulling-powerplants-big-size-big-horses-big-torque/), [AgTalk hilo Pro Stock](https://talk.newagtalk.com/forums/thread-view.asp?tid=111414&DisplayType=flat), [RFD+ NTPA Championship Pulling](https://www.watchrfdtv.com/show/639), [Power Pull Nationals](https://www.powerpullnationals.com/)

Dominado por NTPA. Objetivo: aparecer en listados/resultados de NTPA y enlazar hacia ellos, no competir.

### 1.7 "Pro Pulling League"
- [propulling.com](https://www.propulling.com/) (hoy "Hot Shot's Secret Pro Pulling League", sede Sellersburg, IN, más de 300 eventos), [Facebook](https://www.facebook.com/ProPullingLeague/), [YouTube](https://www.youtube.com/user/ProPullingLeague), [Instagram Pro Pulling TV](https://www.instagram.com/propullingtv/), [Wikipedia](https://en.wikipedia.org/wiki/Lucas_Oil_Pro_Pulling_League), [IHRA Pulling](https://www.ihra.com/pulling), [Full Pull Productions](https://fullpullproductions.com/), [Atlantic Pro Pulling League](https://www.atlanticpropullingllc.com/)

Navegacional hacia la liga. Sin valor directo; úsese como entidad relacionada en schema (`memberOf`) y texto.

### 1.8 "tractor pulling schedule 2026"
- [NTPA 2026 Event Schedule](https://ntpapull.com/pullresults/Schedule/NTPA_ScheduleDynamic.php?currentYear=2026), [PPL schedules](https://www.propulling.com/schedules/), [ITPA](https://www.itpapulling.com/wordpress/2026-pulling-schedule/), [NYTPA](https://www.nytpa.com/schedules/), [Tomah](https://www.tomahtractorpull.com/schedule/), [Southern Pullers](https://thesouthernpullers.com/events.html), [Fully Loaded Pulling](https://fullyloadedpulling.com/schedule/), [DGTP](https://dgtp.org/?page_id=9), [PullTown](https://www.pulltown.com/)

Tipo: calendarios de ligas y asociaciones estatales. Un equipo puede ganar la variante propia y local: "heavy metal pro stock schedule", "Badger State tractor pull schedule [ciudad]", "tractor pull near Waterloo WI".

---

## 2. Presencia web existente de "Heavy Metal" (solo hechos verificables)

| Hecho | Fuente | Estado |
|---|---|---|
| Nombre "Heavy Metal "The Evil One"", Pro Stock, Waterloo, WI, Cat 3208 V8, compite en NTPA y PPL Badger State | `og:description` de la tienda (heavymetalprostock.com) y admin de Shopify (dato del cliente) | Confirmado por el cliente, **sin fuente externa** |
| Clips "The "Heavy Metal" Pro Stock making an awesome run in Highland, WI" y "onboard POV of the Pro Stock sled "Heavy Metal" at Badger State Tractor Pullers" | [@beermoneypullingteam vía TikTok discover](https://www.tiktok.com/discover/pro-stock-tractor-pulling) | Existe, pero **no confirmé** que sea el mismo tractor (un pie de foto dice "sled"). Validar con el equipo |
| Facebook "Heavy Metal Tractorpulling Team" | [facebook.com/p/Heavy-Metal-Tractorpulling-Team-100057435251653](https://www.facebook.com/p/Heavy-Metal-Tractorpulling-Team-100057435251653/) | Página bloqueada por login; **origen y relación desconocidos**. Posible homónimo europeo. Riesgo de confusión de marca |
| Lista de Pro Stock de BSTP (Fuelish Pleasure, Tool Time/Tool Times 2, Stammpede, Red Cattlac, Diehard Deere, Sleipnir, Elsing) | [bstponline.com/prostock-tractors](https://bstponline.com/prostock-tractors/) | **Heavy Metal no aparece.** Pedir a BSTP que lo agregue con enlace |
| Resultados BSTP Green County Fair, Monroe, 17/07/2026: Pro Stock ganó Greg Elsing "T8 Tomcat"; en 9,500 Limited Pro Stock aparece Chris Feller "Wild Buck" JD, **Waterloo** (7.º, 319,444 ft) | [The Monroe Times](https://themonroetimes.com/community/badger-state-tractor-pullers/) | Heavy Metal no aparece en ese evento. El único puller de Waterloo encontrado es otro tractor |
| NTPA | Búsquedas en ntpapull.com | Sin resultados indexados para "Heavy Metal" |
| Handle "heavymetalevil72" | Búsqueda web | Sin resultados públicos |
| "Evil Tractor Pulling Team" | [Facebook](https://www.facebook.com/p/Evil-Tractor-Pulling-Team-100092503404639/) | Equipo del Reino Unido, no relacionado. Otra colisión de nombre |

**Conclusiones para SEO de marca:**
- La entidad "Heavy Metal Prostock" no existe todavía para Google ni para los LLM. Hay que crearla: sitio indexado, schema Organization/SportsTeam con `sameAs`, perfiles sociales con el mismo nombre y enlace al dominio, y listados en BSTP/NTPA.
- Usar siempre el nombre compuesto y consistente: **Heavy Metal "The Evil One" Pro Stock, Waterloo, Wisconsin** para desambiguar de la música y del equipo de Facebook homónimo.
- Pendiente del cliente: nombre del piloto/dueño, marca/modelo de chasis (lámina), año de la construcción, resultados 2025/2026 y URLs de sus redes. Sin eso no se deben publicar datos inventados.

---

## 3. Competidores con sitio web (equipos y tiendas de merch)

| Competidor | Qué es | Fortaleza SEO (cualitativa) |
|---|---|---|
| [Beer Money Pulling Team](https://beermoneypullingteam.com/) | Marca/medio de pulling de Richland Center, WI; en Shopify con blog, tienda, podcast "Let's Grow Pulling", sponsors. Facebook con aprox. 1,6 M seguidores según [su página](https://www.facebook.com/beermoneypullingteam/); [LinkedIn](https://www.linkedin.com/company/beer-money-pulling-team), [YouTube](https://www.youtube.com/@beermoneypullingteam), [X](https://twitter.com/beermoneypull). Merch también en [Angry Duck](https://www.shopangryduck.com/collections/beer-money) | **Alta** para el nicho. Es el referente a imitar (y un aliado: ya grabó a "Heavy Metal") |
| [BAD Gear](https://bad-gear.com/product-category/official-pulling-team-merch/) | Tienda diésel con sección de merch oficial de equipos (Masterson, Warpath, Black Jack, Redweiser) | **Alta** en SERP de "tractor pull shirts". Canal de distribución posible, no solo competidor |
| [Angry Duck](https://www.shopangryduck.com/collections/miller-farms-pulling-team) | Tienda con colecciones de equipos (Miller Farms, Beer Money, Thunderstruck, Short Fused, BOHICA) y eventos (TnT) | Media-alta. Otro canal posible |
| [Roberts Pulling Team](https://en.wikipedia.org/wiki/Roberts_Pulling_Team) | Equipo Super Stock de Ohio (NTPA/PPL/OSTPA) con artículo en Wikipedia y [Wikidata](https://www.wikidata.org/wiki/Q7352040) | Media; su autoridad viene de Wikipedia/Wikidata más que del sitio. Ejemplo de por qué la entidad importa para IA |
| [Judge Pulling Team](https://judgepullingteam.com/) | Sitio propio de equipo | Baja-media (sitio respondió 503 al consultarlo) |
| Equipos BSTP Pro Stock (Fuelish Pleasure, Tool Time, Diehard Deere, T8 Tomcat...) | Aparecen en [bstponline.com](https://bstponline.com/prostock-tractors/) sin enlace a sitio propio | **Muy baja**: casi ninguno tiene web. Heavy Metal puede ser el Pro Stock de Wisconsin con mejor presencia web |
| Marketplaces (Amazon, Etsy, Redbubble, Zazzle, TeePublic) | Diseños genéricos | Dominan lo genérico; no compiten por marca |

Conclusión: el competidor real en SEO de marca local es la ausencia de contenido. El listón de referencia es Beer Money (Shopify + blog + podcast + sponsors). Con 6-8 páginas bien hechas y resultados por evento, Heavy Metal supera a todos los equipos Pro Stock de BSTP en presencia orgánica.

---

## 4. Mapa de palabras clave por página

Intención: N = navegacional, I = informacional, T = transaccional, C = comercial (evaluación, p. ej. patrocinio). Volumen: estimación cualitativa (muy bajo / bajo / medio), sin herramienta de volumen; validar con Google Search Console tras 4-8 semanas y con Keyword Planner.

| Página (URL) | Keyword principal | Secundarias | Long tail | Intención | Volumen est. |
|---|---|---|---|---|---|
| Home `/` | heavy metal pro stock | heavy metal pulling tractor, heavy metal the evil one, heavy metal prostock | heavy metal pro stock tractor waterloo wi, pro stock pulling tractor wisconsin, cat 3208 pro stock tractor | N + I | Muy bajo (marca), crecerá |
| Shop / todas `/collections/all` | heavy metal pro stock merch | pro stock tractor pulling shirts, tractor pulling team merch | official heavy metal pulling team shirt, pro stock tractor pull hoodie | T | Bajo |
| Colección camisetas `/collections/t-shirts` | pro stock tractor pull shirts | tractor pulling t-shirts, pulling tractor shirt | black smoke tractor pull shirt, wisconsin tractor pull shirt, cat v8 pulling tractor shirt | T | Bajo-medio |
| Colección gorras/hoodies `/collections/hats`, `/collections/hoodies` | tractor pulling hats / hoodie | pulling team hat, diesel pulling hoodie | pro stock pulling snapback, tractor pull hoodie wisconsin | T | Bajo |
| Producto `/products/<nombre>` | [nombre producto] heavy metal pro stock | pro stock tractor shirt | ej. "the evil one tractor pull t-shirt black" | T | Muy bajo por página, suma long tail |
| Sponsors `/pages/sponsors` | tractor pulling team sponsorship | sponsor a pulling team, pulling team sponsor wisconsin | sponsor a pro stock tractor, tractor pull sponsorship packages, badger state tractor pull sponsor, waterloo wi business sponsorship motorsport | C | Bajo, pero de alto valor |
| Schedule `/pages/schedule` | heavy metal pro stock schedule | badger state tractor pullers schedule 2027, wisconsin tractor pull schedule | tractor pull near waterloo wi, jefferson county fair tractor pull, dodge county fair tractor pull beaver dam | I + N (local) | Bajo-medio (estacional, pico mayo-agosto) |
| Evento individual `/blogs/events/<evento-año>` | [evento] tractor pull [año] | [ciudad] WI tractor pull, pro stock [evento] | "green county fair tractor pull 2027 pro stock", "tomah tractor pull pro stock" | I + local | Bajo, muy segmentado |
| Resultados `/blogs/results/<evento-año>` | [evento] tractor pull results [año] | badger state tractor pull results, pro stock results | "highland wi tractor pull results pro stock" | I | Bajo, picos post-evento |
| The Machine `/pages/spec-sheet` | cat 3208 pulling tractor | pro stock tractor specs, V8 pro stock tractor | how much horsepower does a pro stock tractor have, cat 3208 v8 pro stock build, pro stock tractor weight 10000 lb | I | Bajo-medio (tema técnico con demanda de foros) |
| The Team `/pages/about` | heavy metal pulling team | waterloo wisconsin pulling team, pro stock team wisconsin | who drives heavy metal pro stock | N + I | Muy bajo |
| Blog build `/blogs/build/...` | pro stock tractor build | cat 3208 pulling engine, pulling tractor turbo setup | "building a pro stock tractor with a caterpillar v8", "how much does a pro stock tractor cost" | I | Bajo-medio |
| FAQ (bloque en home y sponsors) | what is pro stock tractor pulling | pro stock tractor rules | "what is the difference between pro stock and limited pro stock", "how heavy is the sled in a tractor pull" | I | Medio (alto potencial de cita por IA) |

**Reglas anticanibalización:** una sola página por intención. "pro stock tractor specs" solo en The Machine; "sponsorship" solo en Sponsors; cada evento en su propia URL por año; la home no compite por "tractor pull shirts" (lo hace la colección).

---

## 5. Plan técnico SEO para Shopify

### 5.1 Lanzamiento e indexación (prioridad 1)
1. **Quitar la contraseña** en Online Store > Preferences > Password protection al lanzar. Hoy todo canoniza a `/password`.
2. **Dominio**: `heavymetalprostock.com` como dominio principal (Settings > Domains), redirección de `www` y de `*.myshopify.com` al principal. HTTPS lo da Shopify.
3. **Metadatos de la home** (Online Store > Preferences): hoy `meta description` vacía. Propuesta:
   - Title (≤ 60): `Heavy Metal Pro Stock | Pulling Tractor from Waterloo, WI`
   - Description (≤ 155): `Official merch of Heavy Metal "The Evil One", a Cat 3208 V8 Pro Stock pulling tractor from Waterloo, WI. Shirts, hats, schedule and sponsorships.`
   - Imagen social: ya existe `rear-black-smoke...jpg` (1320 px). Mantener.
4. **Search Console**: verificar propiedad de dominio (DNS TXT), enviar `https://heavymetalprostock.com/sitemap.xml` (Shopify lo genera solo), revisar "Páginas" e "Inspección de URL" para la home, sponsors, schedule y spec sheet. Hacer lo mismo en **Bing Webmaster Tools** (alimenta Copilot y, en parte, ChatGPT).
5. **Evitar páginas finas indexadas**: las páginas vacías actuales (`/pages/about`, `/pages/spec-sheet`, `/pages/schedule`, `/pages/sponsors`) y el producto de prueba deben tener contenido o esconderse antes de quitar la contraseña. Borrar el producto de prueba o dejarlo en borrador. Shopify no tiene noindex nativo por página: usar un metafield `seo.hidden = 1` (Shopify lo respeta y excluye del sitemap) para lo que no deba indexarse (p. ej. páginas de agradecimiento).
6. **robots.txt**: el actual permite todo. No bloquear bots de IA (GPTBot, ChatGPT-User, OAI-SearchBot, PerplexityBot, ClaudeBot, Google-Extended, Bingbot). Si se personaliza `robots.txt.liquid`, conservar las reglas por defecto de Shopify (bloqueo de `/cart`, `/checkout`, `/search`, parámetros de filtro).

### 5.2 Estructura de URLs e interlinking
```
/                              Home (marca + tractor + CTA shop/sponsors)
/collections/all               Shop
/collections/t-shirts | hats | hoodies | stickers
/products/<slug>
/pages/about                   The Team
/pages/spec-sheet              The Machine (Cat 3208 V8)
/pages/schedule                Schedule (temporada actual, lista con enlaces)
/pages/sponsors                Sponsors + paquetes + contacto
/pages/faq                     (o bloque FAQ en home/sponsors)
/blogs/events/<evento-año>     Una URL por pull
/blogs/results/<evento-año>    Resultado + fotos + video
/blogs/build/<post>            Diario de construcción
```
- Toda página importante a ≤ 2 clics de la home (menú principal: Shop, The Machine, Schedule, Sponsors, The Team).
- Cada producto enlaza a The Machine ("the tractor on this shirt") y a Schedule ("come see it run"). Cada evento enlaza a su resultado y viceversa, a la colección y a Sponsors. Cada resultado menciona y enlaza a la liga (BSTP/NTPA) y al fair (enlace saliente, genera confianza y reciprocidad).
- Anchors descriptivos ("Cat 3208 V8 Pro Stock specs", no "click here").
- Breadcrumbs visibles en producto, colección y blog (Dawn no los trae por defecto; agregar snippet con BreadcrumbList).

### 5.3 Plantillas de title y meta description
| Plantilla | Title (50-60 caracteres) | Meta description (140-155) |
|---|---|---|
| Producto | `{{ product.title }} | Heavy Metal Pro Stock Merch` | `{{ product.title }}: official Heavy Metal "The Evil One" Pro Stock tractor gear from Waterloo, WI. {{ tipo }} in sizes {{ tallas }}. Ships from Wisconsin.` |
| Colección | `Pro Stock Tractor Pull {{ collection.title }} | Heavy Metal` | `Official Heavy Metal Pro Stock {{ collection.title | downcase }}: tractor pulling gear straight from the pits. Support a Cat V8 Pro Stock team from Wisconsin.` |
| Evento | `{{ Evento }} Tractor Pull {{ año }} | Heavy Metal Pro Stock` | `Heavy Metal "The Evil One" pulls Pro Stock at {{ Evento }}, {{ Ciudad }}, WI on {{ fecha }}. Times, tickets, location and what to expect.` |
| Resultado | `{{ Evento }} {{ año }} Pro Stock Results | Heavy Metal` | `How Heavy Metal ran at {{ Evento }} {{ año }}: distance, placing, video and notes from the {{ liga }} Pro Stock class.` |
| Blog build | `{{ Tema }}: Cat 3208 Pro Stock Build | Heavy Metal` | Resumen de 1 frase con dato concreto (hp, psi, peso). |
| Sponsors | `Sponsor a Pro Stock Pulling Tractor | Heavy Metal, WI` | `Put your brand on Heavy Metal, a Cat V8 Pro Stock pulling tractor competing in NTPA and PPL Badger State. Packages, audience and contact.` |
| Spec sheet | `Cat 3208 V8 Pro Stock Tractor Specs | Heavy Metal` | `Specs of Heavy Metal "The Evil One": Caterpillar 3208 V8, Pro Stock class (10,000 lb, 680 ci max, single turbo). Build details and photos.` |
| Schedule | `2027 Tractor Pull Schedule | Heavy Metal Pro Stock` | `Where to see Heavy Metal pull in 2027: Badger State Tractor Pullers and NTPA dates across Wisconsin, Illinois and Iowa.` |

Un solo H1 por página con la keyword principal; texto de las colecciones (100-200 palabras arriba o abajo de la grilla) para evitar categorías finas.

### 5.4 Schema (JSON-LD)
Principios de la skill: solo marcar lo visible, JSON-LD, validar con [Rich Results Test](https://search.google.com/test/rich-results) y [validator.schema.org](https://validator.schema.org/), y no duplicar lo que Dawn ya emite. Dawn ya genera Product en fichas y datos de organización/website en la home mediante el filtro `structured_data`; revisar el HTML renderizado antes de añadir para no duplicar entidades (la skill `seo-audit` advierte que `curl`/web_fetch no ven JSON-LD inyectado por JS).

**a) Home: Organization + SportsTeam + WebSite (`@graph`)**
```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": ["SportsTeam", "Organization"],
      "@id": "https://heavymetalprostock.com/#team",
      "name": "Heavy Metal Pro Stock",
      "alternateName": ["Heavy Metal \"The Evil One\"", "Heavy Metal Prostock"],
      "sport": "Tractor pulling",
      "url": "https://heavymetalprostock.com/",
      "logo": "https://heavymetalprostock.com/cdn/shop/files/LOGO.png",
      "image": "https://heavymetalprostock.com/cdn/shop/files/rear-black-smoke_d0dd6d3a-3acc-41d8-ad48-a239a9d68f12.jpg",
      "description": "Pro Stock pulling tractor team from Waterloo, Wisconsin, running a Caterpillar 3208 V8 in NTPA and Pro Pulling League Badger State events.",
      "location": {"@type": "Place", "address": {"@type": "PostalAddress", "addressLocality": "Waterloo", "addressRegion": "WI", "addressCountry": "US"}},
      "memberOf": [
        {"@type": "SportsOrganization", "name": "Badger State Tractor Pullers", "url": "https://bstponline.com/"},
        {"@type": "SportsOrganization", "name": "National Tractor Pullers Association", "url": "https://ntpapull.com/"}
      ],
      "sameAs": ["URL_FACEBOOK", "URL_INSTAGRAM", "URL_TIKTOK", "URL_YOUTUBE"],
      "email": "CORREO_PUBLICO"
    },
    {
      "@type": "WebSite",
      "@id": "https://heavymetalprostock.com/#website",
      "name": "Heavy Metal Pro Stock",
      "url": "https://heavymetalprostock.com/",
      "publisher": {"@id": "https://heavymetalprostock.com/#team"}
    }
  ]
}
```
Notas: `SportsTeam` no genera rich result en Google, pero sí ayuda a entender la entidad (knowledge graph y LLM). Rellenar `sameAs`, logo y correo con datos reales; si no hay redes confirmadas, omitir el campo. Agregar `athlete`/`coach` solo cuando el cliente confirme nombres.

**b) Evento: Event (una por pull en `/blogs/events/...`)**
```json
{
  "@context": "https://schema.org",
  "@type": "SportsEvent",
  "name": "Badger State Tractor Pull at the Jefferson County Fair 2027",
  "sport": "Tractor pulling",
  "startDate": "2027-07-XXT19:00:00-05:00",
  "eventStatus": "https://schema.org/EventScheduled",
  "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
  "location": {"@type": "Place", "name": "Jefferson County Fair Park",
    "address": {"@type": "PostalAddress", "streetAddress": "503 N. Jackson Ave.", "addressLocality": "Jefferson", "addressRegion": "WI", "postalCode": "53549", "addressCountry": "US"}},
  "organizer": {"@type": "Organization", "name": "Badger State Tractor Pullers", "url": "https://bstponline.com/"},
  "competitor": {"@id": "https://heavymetalprostock.com/#team"},
  "image": "URL_IMAGEN_EVENTO",
  "description": "Heavy Metal \"The Evil One\" pulls in the Pro Stock class.",
  "offers": {"@type": "Offer", "url": "URL_TICKETS_DEL_FAIR", "availability": "https://schema.org/InStock"}
}
```
La dirección de Jefferson County Fair Park está confirmada en la búsqueda (fair 2026 fue del 8 al 12 de julio, pull de Badger State el 8 de julio a las 7 p.m.). Fechas 2027 pendientes. Event sigue siendo rich result soportado por Google; marcar solo si la página es del evento (no en una página de lista). Si se cancela, actualizar `eventStatus`.

**c) Producto: Product + Offer** (Dawn ya lo emite). Verificar que incluya `brand` ("Heavy Metal Pro Stock"), `sku`, `image`, `offers.price`, `priceCurrency`, `availability`, y si aplica `shippingDetails` y `hasMerchantReturnPolicy` (Google los usa para listados de comerciante). Añadir reseñas solo cuando existan reales.

**d) BreadcrumbList** en producto, colección y blog:
```json
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
 {"@type":"ListItem","position":1,"name":"Home","item":"https://heavymetalprostock.com/"},
 {"@type":"ListItem","position":2,"name":"T-Shirts","item":"https://heavymetalprostock.com/collections/t-shirts"},
 {"@type":"ListItem","position":3,"name":"The Evil One Tee"}]}
```

**e) FAQPage** en `/pages/faq` o en Sponsors/Spec sheet. Desde 2023 Google muestra el rich result de FAQ casi solo a sitios de gobierno y salud, así que no esperar el desplegable en Google; sí sirve para extracción por ChatGPT/Perplexity/Claude. Preguntas sugeridas (respuestas de 40-60 palabras, con datos de reglamento citados a NTPA):
- What is a Pro Stock pulling tractor?
- What engine does Heavy Metal run? (Cat 3208 V8; explicar por qué es raro frente a los John Deere de 6 en línea)
- How much does a Pro Stock tractor weigh? (10,000 lb según [NTPA](https://ntpapull.com/pulling-101/))
- Where can I see Heavy Metal pull?
- How can my business sponsor Heavy Metal?
- Do you ship merch outside Wisconsin?

**f) BlogPosting** en posts de build y resultados (headline, image, datePublished, dateModified, author con nombre real del equipo).

### 5.5 Core Web Vitals en Dawn
Objetivos: LCP < 2,5 s, INP < 200 ms, CLS < 0,1 (medir con [PageSpeed Insights](https://pagespeed.web.dev/) y el informe CWV de Search Console).
- Imagen hero: subir a 2400 px máx., comprimida (el CDN de Shopify sirve WebP/AVIF automáticamente con `image_url` + `image_tag`); no aplicar lazy load al hero (Dawn lo maneja con `fetchpriority="high"` en la primera sección si se usa el bloque correcto).
- Video de humo/pull: no autoplay de MP4 pesado arriba del pliegue; usar póster + reproducir al clic, o subir a YouTube y embeber con fachada (lite embed).
- Máximo 2 familias tipográficas; si se usan fuentes custom, `font-display: swap` y precarga solo del peso del H1.
- Limitar apps: cada app de reseñas, pop-ups o chat agrega JS. Instalar solo lo imprescindible.
- Evitar CLS: dimensiones fijas en banners de anuncio, logos de sponsors con `width/height`.
- Mantener Dawn actualizado (versiones nuevas mejoran rendimiento).

### 5.6 Imágenes y alt
- Nombres de archivo descriptivos: `heavy-metal-pro-stock-cat-3208-v8-waterloo-wi.jpg`, no `IMG_4432.jpg`.
- Alt descriptivo y natural: "Heavy Metal Pro Stock tractor blowing black smoke at the Badger State pull in Highland, WI" (solo si es verdad). En productos: "Black Heavy Metal The Evil One tractor pull t-shirt, front print".
- Fotos propias de pista (E-E-A-T de experiencia); evitar fotos de stock.

### 5.7 Plan de contenido (12 meses, pensando en temporada 2027)
| Mes | Contenido | Objetivo SEO |
|---|---|---|
| Lanzamiento (oct-nov 2026) | Home, The Machine, The Team, Sponsors, Schedule (con "temporada 2027 en preparación"), FAQ, 3-5 productos con descripción única | Indexar entidad y marca |
| Nov-feb | Blog build: 1 post cada 2 semanas (motor Cat 3208 en Pro Stock, turbo, inyección de agua, chasis, costos, lecciones de 2026) | Long tail técnico, enlaces de foros |
| Feb | Post "Why we run a Caterpillar V8 in Pro Stock" + guía "Pro Stock vs Limited Pro Stock vs Light Pro Stock" (con reglas de [NTPA](https://ntpapull.com/ntpa-grand-national-circuit-to-add-4-1-limited-pro-stock-class-in-2026/)) | Contenido citable por IA |
| Mar-abr | Una página por evento 2027 confirmado (BSTP: Sauk Prairie, Jefferson, Baraboo, Monroe, Edgerton, Beaver Dam, Highland, Hillsboro, Green County Fall Nationals, etc.; NTPA: Tomah si aplica) | Local/evento |
| May-sep | Resultado 24-72 h después de cada pull: distancia, puesto, video, foto, cita del piloto, agradecimiento con enlace a sponsors | Frescura, backlinks de sponsors |
| Oct | Resumen de temporada + "Sponsor deck 2028" | Comercial |

Todas las páginas con "Last updated", datos concretos (distancias en pies, peso, hp declarado) y fuente.

### 5.8 SEO local y de eventos
- **Google Business Profile**: solo si el equipo tiene una dirección o área de servicio legítima (p. ej. taller en Waterloo con atención al público o venta en eventos). No crear un perfil falso; si no califica, omitir.
- Mencionar consistentemente "Waterloo, Wisconsin" y "Jefferson County" (NAP coherente en sitio y redes).
- Páginas de evento con ciudad, recinto, dirección y enlace a entradas del fair. Candidatos cercanos a Waterloo según 2026: [Jefferson County Fair](https://jeffcofair.com/schedule/fair-week-schedule/) (Jefferson, WI) y [Dodge County Fair, Beaver Dam](https://www.travelwisconsin.com/events/badger-state-truck-and-tractor-pull); también [Green County Fall Nationals](http://www.greencountyfallnationals.com/) y [Tomah](https://visittomah.com/events/budweiser-dairyland-super-nationals/).
- Enviar los eventos con el nombre del equipo a calendarios locales: [Travel Wisconsin](https://www.travelwisconsin.com/events/badger-state-truck-and-tractor-pull), [Isthmus](https://isthmus.com/events/jefferson-county-fair-annual/), periódicos locales (Daily Union de Fort Atkinson, Watertown Daily Times, Waterloo/Marshall Courier).

### 5.9 Backlinks (orden de facilidad x valor)
1. **Ligas**: pedir a [BSTP](https://bstponline.com/prostock-tractors/) que agregue a Heavy Metal a su directorio Pro Stock con enlace; completar perfil de puller NTPA (enlace si lo permiten).
2. **Sponsors**: cada sponsor enlaza a heavymetalprostock.com desde su web ("Proud sponsor of Heavy Metal Pro Stock"); incluirlo en el paquete de patrocinio como entregable.
3. **Medios del nicho**: Beer Money Pulling Team (ya publicó clips de "Heavy Metal"), [Fullpull](https://www.fullpull.us/), podcast "Inside the NTPA", [PullTown](https://www.pulltown.com/), Diesel World, Drivingline (historia del V8 Caterpillar en Pro Stock es un ángulo noticioso).
4. **Prensa local**: [The Monroe Times](https://themonroetimes.com/community/badger-state-tractor-pullers/) publica resultados BSTP; Daily Union, Watertown Daily Times, WKOW/WMTV Madison. Nota de prensa al lanzar y tras un buen resultado.
5. **Fairs y promotores**: pedir enlace en la página de grandstand/pull del fair ("featured puller").
6. **Proveedores**: fabricantes de piezas usadas (turbo, inyección, llantas) suelen tener páginas de "customers/racers".
7. **Canales de merch**: listar productos en BAD Gear o Angry Duck puede traer enlace de marca y ventas.
Evitar compra de enlaces y directorios basura.

### 5.10 SEO para IA (ChatGPT, Google AI Overviews, Perplexity, Claude)
Marco `ai-seo` en tres pilares:
- **Estructura**: en The Machine y FAQ, bloques de respuesta de 40-60 palabras que funcionen solos ("Heavy Metal "The Evil One" is a Pro Stock pulling tractor from Waterloo, Wisconsin, powered by a Caterpillar 3208 V8..."). Tabla de especificaciones. Tabla comparativa Pro Stock / Limited Pro Stock / Light Pro Stock con fuente NTPA. H2 formulados como preguntas.
- **Autoridad**: citar reglamentos (NTPA, PPL), datos propios (distancias oficiales, peso), citas con nombre del piloto, fecha de actualización visible. No inflar hp ni resultados.
- **Presencia**: los LLM citan más a terceros que al sitio propio. Prioridad a: listados de BSTP/NTPA, Beer Money/Fullpull, prensa local, YouTube con título, descripción, capítulos y subtítulos que digan "Heavy Metal Pro Stock, Cat 3208 V8, Waterloo WI", y perfiles sociales con el mismo nombre y enlace. Wikidata: crear un ítem solo cuando haya al menos 2-3 fuentes independientes publicadas (como tiene [Roberts Pulling Team](https://www.wikidata.org/wiki/Q7352040)).
- **Acceso de bots**: el robots.txt de Shopify ya permite todo y además expone `agents.md` y un endpoint UCP/MCP para agentes de compra (declarados en el robots.txt). No bloquear.
- **llms.txt** opcional: Shopify no permite archivos arbitrarios en la raíz; se puede publicar como página `/pages/llms` o vía redirección de URL (Navigation > URL redirects) de `/llms.txt` a un archivo del CDN. Google dice que no hace falta para AI Overviews; es de bajo costo para los demás motores.
- **Medición**: probar trimestralmente 10-15 consultas ("who runs a Cat V8 in Pro Stock tractor pulling", "Pro Stock tractors in Wisconsin", "heavy metal pro stock") en ChatGPT, Perplexity, Google AI Mode y Gemini; registrar si citan el sitio.

### 5.11 Checklist de lanzamiento
- [ ] Páginas About, Spec sheet, Schedule y Sponsors con contenido real (mínimo 300 palabras las principales)
- [ ] Producto de prueba eliminado; 3+ productos reales con descripción única
- [ ] Title y meta description en home, colecciones, productos y páginas
- [ ] Alt en todas las imágenes; nombres de archivo descriptivos
- [ ] Schema validado (Organization/SportsTeam, Product, BreadcrumbList, FAQ/Event si aplica)
- [ ] Contraseña quitada; dominio principal y redirecciones
- [ ] Search Console + Bing Webmaster; sitemap enviado; inspección de URL de 5 páginas clave
- [ ] PageSpeed móvil de home y producto con CWV en verde
- [ ] Redes sociales con enlace al dominio y mismo nombre de marca
- [ ] Solicitud de enlace a BSTP, NTPA, Beer Money y sponsors actuales

---

## 6. Datos pendientes del cliente (no inventar)
Nombre del piloto y del equipo humano, año de construcción, marca/modelo de la lámina (chasis), hp o boost declarados, resultados oficiales 2025/2026, eventos 2027, URLs de Facebook/Instagram/TikTok/YouTube, confirmar si los clips "Heavy Metal" de Beer Money son de este tractor y si el Facebook "Heavy Metal Tractorpulling Team" es propio o de otro equipo.

## 7. Fuentes principales
- NTPA: [Pulling 101](https://ntpapull.com/pulling-101/), [4.1 Limited Pro Stock 2026](https://ntpapull.com/ntpa-grand-national-circuit-to-add-4-1-limited-pro-stock-class-in-2026/), [Calendario 2026](https://ntpapull.com/pullresults/Schedule/NTPA_ScheduleDynamic.php?currentYear=2026), [Sponsors](https://ntpapull.com/sponsors/), [Resultados](https://ntpapull.com/results-dashboard/), [Tomah 2026](https://ntpapull.com/june-26-28-tomah-wis-50th-budweiser-dairyland-super-nationals/)
- PPL: [propulling.com](https://www.propulling.com/), [Clases](https://www.propulling.com/classes/), [Calendarios](https://www.propulling.com/schedules/), [Wikipedia](https://en.wikipedia.org/wiki/Lucas_Oil_Pro_Pulling_League)
- BSTP: [Home](https://bstponline.com/), [Pro Stock](https://bstponline.com/prostock-tractors/), [Monroe Times resultados 17/07/2026](https://themonroetimes.com/community/badger-state-tractor-pullers/)
- Heavy Metal: [TikTok discover Pro Stock](https://www.tiktok.com/discover/pro-stock-tractor-pulling), [Facebook Heavy Metal Tractorpulling Team](https://www.facebook.com/p/Heavy-Metal-Tractorpulling-Team-100057435251653/)
- Competencia: [Beer Money](https://beermoneypullingteam.com/), [BAD Gear](https://bad-gear.com/product-category/official-pulling-team-merch/), [Angry Duck](https://www.shopangryduck.com/collections/beer-money), [Roberts Pulling Team](https://en.wikipedia.org/wiki/Roberts_Pulling_Team)
- Técnica: [Drivingline](https://www.drivingline.com/articles/anatomy-of-a-pro-stock-tractor/), [Engine Builder](https://www.enginebuildermag.com/2017/03/ntpa-tractor-pulling-powerplants-big-size-big-horses-big-torque/)
- Local: [Jefferson County Fair 2026](https://jeffcofair.com/schedule/fair-week-schedule/), [Travel Wisconsin Badger State pull](https://www.travelwisconsin.com/events/badger-state-truck-and-tractor-pull), [Visit Tomah](https://visittomah.com/events/budweiser-dairyland-super-nationals/)
- Google: [Rich Results Test](https://search.google.com/test/rich-results), [Guía de funciones de IA](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)
