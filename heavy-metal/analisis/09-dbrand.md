# 09. dbrand: qué copiar (y qué no) para Heavy Metal "The Evil One"

Fecha de investigación: 1 de octubre de 2026.
Método: lectura directa del sitio (WebFetch y descarga del HTML y CSS de dbrand.com), búsquedas en prensa (WebSearch) sobre campañas, demandas y polémicas. Todas las URLs de dbrand citadas respondieron 200 el 1/10/2026, salvo donde se indica.

---

## 1. Resumen en 5 líneas

1. dbrand vende fundas y skins (commodity puro) con una voz de "robot overlord" que se burla del cliente, de sí misma y de las megamarcas; el chiste vive en titulares, FAQs, 404, SMS y páginas de drops, pero **checkout, carrito, privacidad y soporte técnico se escriben en serio**.
2. "Extortion" es su chiste fundacional: una página real (`/not-extortion`) donde el usuario sube con "+" un monto para pagarles por nada, marca la casilla "I acknowledge that this is not extortion." y pulsa "Extort Me >". Es propina disfrazada de amenaza, y aparece en soporte ("Extortion: Give us money") y en SMS.
3. Las mecánicas que mueven ventas son drops de edición limitada con archivo fechado y lista de espera, garantías absurdas pero reales ("You'll die before it yellows. Guaranteed"), tablas "vs. the world" y transparencia operativa (página de status, avisos de defectos en la ficha).
4. Diseño sobrio: negro, blanco y un solo amarillo (#ffbb00), tipografías de autor (Replica, Diatype Semi-Mono, una propia), contadores animados de specs y muro de prueba social con tweets reales; la irreverencia está en el texto, no en el layout.
5. Riesgos documentados: burla racista a un cliente en 2024 (pagaron 10.000 USD y perdieron a MKBHD un tiempo), culpar al cliente por un defecto en 2025, y provocar a Sony ("Go ahead, sue us") hasta recibir carta de cese; Heavy Metal debe copiar la estructura del humor, no el blanco del chiste.

---

## 2. Contexto de la marca

- Empresa canadiense (Toronto) fundada el 11/11/2011. Más de 20 a 23 millones de clientes según el propio sitio (el carrito dice "Trusted by 20,000,000+", la home dice "Over 23 Million Customers Worldwide": ojo, inconsistencia).
- El personal se llama "robots"; la cuenta de soporte en X es @robot y los sobres llevan arte de robots. El estudio de Dentsu Webchutney lo describe como una cultura de "toxic, edgy robot overlord" que "looks down on us and ridicules us", y la gente pide roasts en la caja de instrucciones especiales del pedido ([Medium, Webchutney](https://webchutney.medium.com/is-dbrand-d-most-de-brand-brand-c07a7d743ee5)).
- No usa Shopify: el front es SvelteKit propio (assets en `cdn.db.io/_app/immutable/`). Algunas microinteracciones requieren trabajo de tema en Dawn, no son de fábrica.

---

## 3. Voz y copy, con ejemplos verificados

### 3.1 Productos (fichas)
Patrón: beneficio técnico real + golpe al lector o a la competencia + remate. El dato técnico nunca se sacrifica por el chiste.

- **Ghost Case 2.0** ([ficha](https://dbrand.com/shop/ghost/iphone-18-pro-max-clear-cases)): "clear cases are boring, featureless slabs of transparent plastic that disappoint you, your wallet & your phone. The Ghost Case is none of these things. Well, aside from transparent." / "You'll die before it yellows. Guaranteed" / "We'd love to tell you more, but it's classified."
- **Grip Case** ([ficha](https://dbrand.com/shop/grip/iphone-17-pro-cases)): "Nobody asked for this. We should clarify: nobody asked Apple for a Camera Control Button." / "Face it: magnets are everything you aren't. They're attractive, they're useful... Once we've figured out how to mold a person into a phone case, you'll finally be 1/3rd as good as magnets." / "The most precise fit on earth.™"
- **Tank Case** ([ficha](https://dbrand.com/shop/tank/iphone-17-pro-cases)): cambia a tono manifiesto oscuro, sin chiste: "They sell you fragility, then sell you fear. ... Anxiety is the business model. If the Tank Case cannot save you, nothing can." / "Smooth plastic isn't design. It's neglect." / "The Tank Case rejects gravity." Firma "Robot(c)4026". Es el registro más cercano a Heavy Metal.
- **Home** ([dbrand.com](https://dbrand.com)): "No hinge. No crease. No "innovation." Just the iPhone everyone actually bought" / "Protect your fruit-themed smartphone ... Don't forget to cancel your AppleCare." / "Checkmate, Tim." / "When we launched the Tank Case, people had many questions, like "when are you making it for my phone?" and "why does it look so ugly?" Naturally, we ignored them". Etiquetas de categoría con adjetivo de marca: "zero-yellowing", "idiot-proof", "ultimate protection".

### 3.2 Drops y ediciones limitadas
- **Teardown** ([página](https://dbrand.com/shop/limited-edition/teardown)): "Designed by Zack. Built by Robots." / "the deal wrote and signed itself - nobody tell Zack." / "A $92,000 printer. For every skin you don't buy, 0.021% of the printer goes unpaid for." / "Who are we kidding? You didn't go to college."
- **Robot** ([página](https://dbrand.com/shop/limited-edition/robot)): "It's not a product. It's the future." / estado "Drop has ended. Request" / lista de espera: "Everyone who bought Robot skins now owns a piece of history. You, on the other hand, do not. Give us your email address and we'll notify you if we ever decide to make more history."
- FAQ del drop Robot, la mejor pieza de copy del sitio: "What does "limited" mean? It means you have two weeks to avoid a lifetime of regret." / "Why is this ... a limited edition? It's called "artificial scarcity" and it makes us tons of money." / "your piece will be unique. Unlike you." / "Make us an offer we can't refuse." / Pregunta "Is dbrand really run by robots?" respondida en binario (Easter egg que felicita a quien la traduce).
- **Archivo** ([/shop/limited-edition](https://dbrand.com/shop/limited-edition)): cada drop con mes y año (Robot sep 2019, Teardown dic 2019, Touch Grass (Again) abr 2026), activos y "Retired". Convierte el pasado en colección.

### 3.3 Botones, carrito y checkout
- Botones de compra estándar: "Add to Cart", "Shop Now", "View all". **No juegan con el CTA principal.**
- Carrito vacío ([/cart](https://dbrand.com/cart)): "Your Cart", "Continue shopping", "Start Shopping", más señales de confianza en claro: "Free shipping on most orders over $65", "Hassle-free returns within 30 days", "Trusted by 20,000,000+ customers" y un incentivo "Free Playing Cards Over $100". Nada de chistes donde se decide la compra.
- La excepción es la página de extorsión, donde el botón sí es el chiste ("Extort Me >").

### 3.4 Soporte, FAQ y políticas
- [Support](https://dbrand.com/support): estructura seria (Order Status, Service Status, Shipping, Installation Guides) con dos guiños en los enlaces rápidos: "Careers: Join the cult" y "Extortion: Give us money".
- FAQ de devoluciones y problemas ([returns](https://dbrand.com/support/faq/returns-and-exchanges), [troubleshooting](https://dbrand.com/support/faq/troubleshooting)): totalmente sobrios y útiles ("Sorry about that. While rare, defects can happen."; "Don't panic."). Lo único con voz es el nombre "Support Robots".
- [Privacy Policy](https://dbrand.com/about/privacy-policy): texto legal estándar (PIPEDA, CASL, GDPR) sin un solo chiste. Lección central: **el humor nunca toca el texto que tiene valor legal**.
- [Status](https://dbrand.com/status): página de estado operativo (fulfillment 1 a 3 días, email support, tiempos por país, "Suspended"/"Unavailable"). Transparencia como valor de marca.

### 3.5 Error 404
URL probada: `https://dbrand.com/asdfqwer-404` (HTTP 404). Copy completo: "404 - Page Not Found / There's no reward for finding it." Botones: "Back to Home Page" y "Complain on Reddit". Corto, una sola línea de humor, salida útil y un segundo botón que manda a la comunidad.

### 3.6 Emails y SMS
- [/sms](https://dbrand.com/sms): "Let's get parasocial." / "Want to trick your peers into thinking you're popular? Give us your number and we'll start blowing up your phone." Botón "Submit" y consentimiento legal completo ("reply "STOP" to cancel") en tono normal.
- Ejemplos de SMS publicados en esa misma página: carrito abandonado "You put some items in your cart. Then you abandoned it. That's two mistakes for the price of none. Finish the checkout or we're escalating to blackmail."; "Congrats, you joined a cult. ... You're ours now."; cambio de número "The feds are onto us."; admitir un fracaso "guys we made a million iphone 16e cases and now it turns out nobody gives a shit about the 16e please help"; política "Thanks to Donald Trump, our SMS messages are now subject to a 25% tariff. Pay your tariff here, please dbrand.com/extortion".
- No pude ver emails reales de dbrand (requieren suscripción); el patrón se infiere de los SMS.

### 3.7 Estados vacíos, confirmaciones, otras páginas
- [Careers](https://dbrand.com/about/careers) abre con un selector: "Why are you here? I'm part of a cult. / I want to work for you. / I want to learn more. / I have no clue." Segmenta y entretiene a la vez.
- [Timeline](https://dbrand.com/about/timeline): historia con hechos verificables y fuentes, cada uno con remate: "dbrand is founded. This date is not made up." / "dbrand reaches the top of r/all on Reddit by telling people not to buy our products." / "dbrand sells empty cardboard boxes for five dollars each. 20,000 people buy them."
- La ficha Ghost muestra un aviso honesto dentro de la compra: el Burgundy salió "slightly more purple than the iPhone 18 Pro Max", así que mandan dos fundas (una ahora y otra corregida en noviembre). Transparencia que genera confianza.

### 3.8 Qué es "extortion" en su marca
- Una página real, [dbrand.com/not-extortion](https://dbrand.com/not-extortion) (antes `/extortion`, que redirige): "Not Extortion. Welcome. Hit the + sign to begin...", contador desde $0.00, casilla "I acknowledge that this is not extortion." y botón "Extort Me >".
- Funciona como propina voluntaria y como broma recurrente: aparece en soporte, en SMS (el arancel de SMS) y en el lenguaje de carrito abandonado ("escalating to blackmail"). Es un "running gag" que premia al fan que lo reconoce.
- Por qué funciona: invierte la relación (la marca "amenaza", el fan paga por el privilegio de seguir el chiste), y el monto lo decide el cliente. Por qué es delicado: en EE. UU. una página de "dame dinero por nada" debe dejar claro que no es donativo deducible ni hay contraprestación oculta.

---

## 4. Mecánicas

| Mecánica | Cómo lo hace dbrand | Evidencia |
|---|---|---|
| Drops limitados | Ventanas cortas ("two weeks"), estado "Drop has ended", lista de espera por email con tipo y dispositivo | [Robot](https://dbrand.com/shop/limited-edition/robot) |
| Archivo de drops | Catálogo fechado desde 2019 con activos y "Retired" | [Limited Edition](https://dbrand.com/shop/limited-edition) |
| Escasez confesada | "It's called "artificial scarcity" and it makes us tons of money." Decir la táctica en voz alta la desarma | Robot FAQ |
| Mascota/persona | Robots numerados, @robot, sobres ilustrados, firma "Robot(c)4026" | Tank, Robot, Webchutney |
| Easter eggs | FAQ en binario; código "R0807" escondido en los scans de Teardown que luego probó la copia de Casetify | [TechCrunch](https://techcrunch.com/2023/11/27/dbrand-is-suing-casetify-over-stolen-designs/) |
| Garantías absurdas pero reales | Reemplazo gratis de por vida si el Ghost amarillea, "No conditions, no fine print. Just an incredible offer that you'll never get to take advantage of." | Ghost |
| Comparativas | Tabla "Ghost vs. the world" (grip, anti-yellowing, protección, grosor, peso, botones, fit) sin nombrar marcas | Ghost |
| Specs animadas | Contadores que arrancan en 0: thin mm, drop protection ft, light g, anti-yellowing pct | Ghost |
| Transparencia | Página de status, avisos de color defectuoso, admitir fracasos por SMS | [Status](https://dbrand.com/status) |
| Comunidad | Muro de tweets y posts de Reddit en la home, botón "Complain on Reddit" en el 404, colabs con creadores (JerryRigEverything, MKBHD, LTT) | Home, Timeline |
| Stunts | Cajas vacías a 5 USD en Boxing Day 2017 (20.000 vendidas en 6 horas, algunas con iPhone X gratis), secuela "Boxing Day Cube" 2019, 50.000 USD en efectivo a un cliente | [Timeline](https://dbrand.com/about/timeline), [Cube](https://dbrand.com/shop/limited-edition/cube), [X](https://x.com/dbrand/status/951233541546889217) |
| Antagonista | Apple, Samsung, Sony, "soulless executives". Darkplates: "Go ahead, sue us." Sony mandó cese y desistimiento; respondieron "Darkplates are dead. Thanks, Sony." y lanzaron Darkplates 2.0 rediseñadas | [TechRadar](https://www.techradar.com/news/dbrand-declares-its-ps5-darkplates-are-dead-after-sony-threatens-legal-action), [Tom's Guide](https://www.tomsguide.com/news/sony-lawyers-killed-ps5-darkplates-but-darkplates-20-are-already-here) |

---

## 5. Diseño

- **Color**: base negro (#000) y blanco (#fff) con un único acento amarillo (#ffbb00 / #fb0, más una escala de 8 tonos de ese amarillo) y un rojo/rosa (#ff2056) para alertas. Paleta disciplinada: todo el ruido lo pone el copy y la foto de producto.
- **Tipografía**: familia propia `dbf-base` (100, 400, 700), Replica (grotesca de Lineto) y Diatype Semi-Mono (Dinamo) para datos y etiquetas. Look técnico, de ficha de ingeniería.
- **Layout**: home en bloques de producto con eyebrow corto ("idiot-proof", "zero-yellowing"), titular, dos líneas de copy con remate y "Shop Now"; carruseles horizontales; grid de "Popular Devices" con una línea de humor por dispositivo; muro de prueba social.
- **Ficha de producto**: selector de dispositivo y color arriba, precio tachado, add-ons (2x screen protectors, skin) en la misma vista, contadores animados de specs, secciones numeradas tipo manifiesto (Tank "01 Tactical Design"), comparativa al final.
- **Navegación**: mínima y funcional (MNML, Ghost, Tank, Cases, Screen Protectors, Limited Edition, Skins, Gaming, Support). Ningún chiste en el menú.
- **Microinteracciones**: contadores de specs, rotación del producto ("Rotate"), botón con spinner, el "+/-" de la extorsión, customizador ("Start Customizer").

---

## 6. Por qué funciona y qué riesgos tiene

**Funciona porque:**
1. El humor está donde no hay fricción (descubrimiento, ficha, drops, 404, SMS) y desaparece donde hay dinero o ley en juego (carrito, checkout, privacidad, devoluciones).
2. Cada chiste va pegado a un dato verificable (12 ft, 13 imanes, 1,8 mm, garantía de por vida). El humor hace creíble la confianza, no la sustituye.
3. Tiene un antagonista grande (Apple, Sony, "soulless executives") que convierte al cliente en cómplice.
4. Los running gags (extorsión, robots, culto) premian la lealtad: el fan viejo entiende más.
5. Confesar la táctica ("artificial scarcity") genera simpatía en un público que odia el marketing.

**Riesgos documentados:**
1. **Burla al nombre de un cliente indio (abril 2024)**: tuit visto más de 7 millones de veces, MKBHD cortó la relación hasta que lo borraran, terminaron pagando 10.000 USD y el CEO lo llamó "severe lapse in judgment" ([Android Central](https://www.androidcentral.com/accessories/dbrand-issues-apology-over-social-media-remark), [Gizmodo](https://gizmodo.com/dbrands-social-media-goes-off-the-deep-end-offers-10k-1851404479)). El "no vamos a parar" de su disculpa empeoró la recepción ([PhoneArena](https://phonearena.com/news/Dbrand-shocks-with-racist-tweet-at-customer-thinks-youll-be-ok-with-it-in-return-for-10000_id157173)).
2. **Culpar al cliente por un defecto (junio 2025)**: Killswitch de Switch 2 soltaba los Joy-Cons; respondieron con 4.000 palabras de "nobody routinely holds their Switch 2 like this", luego admitieron una "spectacularly terrible response" y mandaron grips gratis a todos ([VGC](https://www.videogameschronicle.com/news/dbrand-is-sending-improved-switch-2-grips-to-all-customers-after-spectacularly-terrible-response-to-detaching-claims/), [Android Authority](https://www.androidauthority.com/dbrand-killswitch-switch-2-replacement-3570754/)).
3. **Provocación legal**: "Go ahead, sue us" contra Sony terminó en carta de cese y retiro del producto ([GamesBeat](https://gamesbeat.com/sony-threatens-dbrand-with-cease-and-desist-order-over-ps5-darkplates/)).
4. **Ser copiados**: demandaron a Casetify por 117 diseños de Teardown; los Easter eggs probaron la copia ([TechCrunch](https://techcrunch.com/2023/11/27/dbrand-is-suing-casetify-over-stolen-designs/)). Lección positiva: registrar diseños y esconder firmas propias.
5. **Humor político y groserías**: el SMS sobre Trump y "nobody gives a shit" funcionan con su audiencia global tecnológica; en una audiencia rural de Wisconsin la política divide mitad y mitad.

---

## 7. Tabla de ideas aplicables a Heavy Metal (18)

Esfuerzo: Bajo (copy o ajuste de tema), Medio (sección o app sencilla), Alto (desarrollo a medida o logística). Riesgo: de tono, legal o de ejecución.

| # | Idea (de dbrand) | Copy de ejemplo para Heavy Metal (EN) | Dónde va | Esfuerzo | Riesgo |
|---|---|---|---|---|---|
| 1 | Página "Not Extortion" | Title: "Feed The Beast". Body: "The Evil One drinks diesel like you drink coffee. Hit + to help. This is not extortion. It's fuel." Checkbox: "I acknowledge this is not extortion. It's worse: it's tractor pulling." Button: "Take My Money, Evil One". Fine print: "This is a purchase, not a tax-deductible donation." | Página propia `/pages/feed-the-beast` con producto de precio variable o propina; enlace en footer y soporte | Medio | Legal medio: aclarar que no es donativo; no prometer uso exacto del dinero si no se cumple |
| 2 | 404 de una línea + botón a comunidad | "404. You pulled off the track. No distance, no points." Buttons: "Back to the Pits" / "Tell us on Facebook" | Plantilla 404 del tema | Bajo | Bajo |
| 3 | Garantía absurda pero real | "The Black Smoke Guarantee: if this shirt ever stops being evil, we replace it. Free. No fine print. Nobody has ever claimed it." | Ficha de producto (bloque bajo el precio) y página de políticas en versión seria | Bajo | Legal medio: el texto de política debe definir qué cubre (defectos de impresión, X días) |
| 4 | Ficha con dato real + remate | "Heavyweight 6.5 oz cotton. Built like a sled weight. Washes better than a pit crew after a dirt track." | Descripción de producto | Bajo | Bajo |
| 5 | Contadores animados de specs | "Weight 6.5 oz / Horsepower 0 (it's a shirt) / Evil 100 pct / Cat 3208 cylinders 8" | Ficha de producto, bloque tipo métricas | Medio | Bajo; respetar `prefers-reduced-motion` |
| 6 | Drops con ventana y estado | "Drop 03: Badger State Burnout. Open until the last hook of the season. Then it's gone." / estado cerrado: "Drop has ended. You missed it. The Evil One didn't." | Colección de drops y ficha | Medio | Medio: si se reedita, no haber dicho "never again" (FTC, escasez falsa) |
| 7 | Archivo de drops fechado | "The Evil Archive. Every drop since 2026. Some are still alive. Most are buried." | Página de colección "Archive" | Bajo | Bajo |
| 8 | FAQ del drop con escasez confesada | "What does limited mean? It means once the sled stops, so does this shirt." / "Why limited? Because printing 10,000 shirts for a tractor from Waterloo would be insane. Even for us." | Bloque FAQ en ficha de drop | Bajo | Bajo |
| 9 | Lista de espera irreverente | "Missed it? Get on The Evil List. We'll tell you when The Evil One feels generous. It rarely does." | Formulario en producto agotado (back in stock) | Bajo | Bajo |
| 10 | Signup a la lista de correo | Headline: "Join The Evil List." Body: "Drops, pull dates and results before anyone else. We email when the tractor does something f#ck!ng evil. So, often." Consent in plain English below. | Popup, footer, página de contraseña | Bajo | Legal: CAN-SPAM y TCPA si hay SMS; consentimiento claro, sin chistes en el texto legal |
| 11 | Carrito abandonado con "amenaza" suave | Subject: "You left gear in the pits." Body: "The Evil One noticed. It's not mad. It's disappointed. Finish your order before it starts the engine." | Flujo de Shopify Email / automatización | Bajo | Bajo; evitar "blackmail" o amenazas literales |
| 12 | Persona/mascota | El tractor narra en primera persona y firma "The Evil One, Cat 3208, Waterloo WI". El equipo firma como "Pit Crew #1, #2". | Emails, notas de empaque, soporte, Instagram | Bajo | Bajo; definir una guía de voz para que todos escriban igual |
| 13 | Manifiesto oscuro tipo Tank | "They build tractors to look pretty at the county fair. We built one to break sleds. Shiny paint isn't power. It's decoration." | Home (bloque historia) y página "The Evil One" | Bajo | Bajo; no atacar a otros equipos por nombre |
| 14 | Timeline con hechos reales y remate | "2026: The Evil One gets a website. The cows were not consulted." | Página "History" | Medio | Bajo; cada hecho debe ser cierto |
| 15 | Comparativa "vs. the world" sin marcas | Tabla "Evil Gear vs. gas-station tee": weight, print, fit, evil. "Gas-station tee: 0 pct evil." | Ficha de producto estrella | Medio | Medio: no nombrar marcas ni usar sus logos |
| 16 | Status/transparencia | "Pit Status: Orders print in 2 to 4 days. Ships from Wisconsin. Next pull: Jefferson County Fair." | Página `/pages/pit-status` enlazada desde soporte | Bajo | Bajo; mantenerla actualizada o mata la confianza |
| 17 | Easter egg | Código de descuento escondido en binario o en la foto del motor; o hidden route `/pages/3208` con "You found the V8. Use code EVIL3208." | Página oculta, FAQ, nota de empaque | Bajo | Bajo; poner fecha de vencimiento al código |
| 18 | Selector "Why are you here?" para sponsors | "Why are you here? I want my logo on The Evil One. / I want a shirt. / I'm a pulling fan. / I have no clue." | Página de patrocinios y home | Medio | Bajo |
| 19 | Stunt de temporada | "Canned Black Smoke. Limited edition. 100 pct air from Waterloo. Proceeds go to diesel." | Drop de Black Friday o fin de temporada | Medio | Medio: describir con exactitud que la lata está vacía; no vender tierra de pista (movimiento de suelo puede estar regulado) |
| 20 | Muro de prueba social | "Spotted in the wild: fans wearing evil." Fotos de fans en pulls con permiso. | Home y ficha | Medio | Legal: pedir permiso para usar fotos de terceros |

Regla operativa para todo lo anterior: **botones de compra, checkout, políticas, privacidad y textos de consentimiento quedan en inglés claro y estándar** ("Add to cart", "Checkout"). Si se quiere voz en el botón, va en el subtítulo, no en la etiqueta.

---

## 8. Qué NO copiar

1. **Burlarse de clientes reales**, de su nombre, origen, cuerpo o inteligencia. dbrand pagó 10.000 USD y perdió a MKBHD un tiempo por un solo tuit. En una comunidad chica como el pulling de Wisconsin, todos se conocen: el blanco del chiste siempre es la máquina, el sled, la gravedad o el propio equipo.
2. **Provocar a dueños de marcas registradas.** Nada de "Go ahead, sue us". Para Heavy Metal esto es concreto: **no usar logos ni nombres de Caterpillar, John Deere, NTPA, PPL o Badger State en el merch** sin licencia; "Cat 3208" solo como dato técnico en texto, no como diseño de prenda.
3. **Culpar al cliente cuando algo falla.** La respuesta Killswitch es el antiejemplo. Talla equivocada, impresión mala o envío tarde: disculpa breve, solución, cero chiste.
4. **Escasez falsa o precios tachados inflados.** dbrand puede decir "artificial scarcity" porque cumple sus drops; si Heavy Metal dice "never again" y reimprime, rompe confianza y roza prácticas engañosas de la FTC. Nada de "instead of $79.85" si nunca se vendió a ese precio.
5. **Humor en textos legales.** dbrand no hace chistes en privacidad ni devoluciones. Heavy Metal tampoco: políticas de Shopify en lenguaje claro.
6. **Política, groserías y amenazas literales.** El SMS sobre Trump o "nobody gives a shit" no aplican. Tope de grosería: "f#ck!ng" en el lema. Evitar "blackmail", "we know where you live" y similares en emails o SMS (además de mal tono, en SMS hay reglas TCPA).
7. **Humor sobre accidentes.** El pulling tiene choques, incendios y lesiones reales. Nada de chistes sobre gente herida, fuego o muerte en pista, aunque el registro sea "humor oscuro"; lo oscuro es la estética metal, no la tragedia.
8. **Chistes de países y grupos** ("Unless you live in North Korea"): sobran para un equipo local.
9. **Copiar frases textuales de dbrand** ("Extort Me", "idiot-proof", "Let's get parasocial"). Copiar la estructura, nunca la frase: además de verse derivado, es su propiedad de marca.
10. **Respuestas largas a una polémica.** 4.000 palabras empeoraron todo. Si algo sale mal: tres líneas, disculpa, solución.

---

## 9. Fuentes

Sitio de dbrand (consultado el 1/10/2026):
- https://dbrand.com
- https://dbrand.com/not-extortion
- https://dbrand.com/sms
- https://dbrand.com/support
- https://dbrand.com/support/faq/returns-and-exchanges
- https://dbrand.com/support/faq/troubleshooting
- https://dbrand.com/status
- https://dbrand.com/cart
- https://dbrand.com/about/privacy-policy
- https://dbrand.com/about/careers
- https://dbrand.com/about/timeline
- https://dbrand.com/shop/limited-edition
- https://dbrand.com/shop/limited-edition/robot
- https://dbrand.com/shop/limited-edition/teardown
- https://dbrand.com/shop/limited-edition/cube
- https://dbrand.com/shop/ghost/iphone-18-pro-max-clear-cases
- https://dbrand.com/shop/grip/iphone-17-pro-cases
- https://dbrand.com/shop/tank/iphone-17-pro-cases
- 404 de prueba: https://dbrand.com/asdfqwer-404

Prensa y terceros:
- [Webchutney (Medium): Is dbrand d-most de-brand brand?](https://webchutney.medium.com/is-dbrand-d-most-de-brand-brand-c07a7d743ee5)
- [TechRadar: Darkplates are dead](https://www.techradar.com/news/dbrand-declares-its-ps5-darkplates-are-dead-after-sony-threatens-legal-action)
- [GamesBeat: Sony cease and desist](https://gamesbeat.com/sony-threatens-dbrand-with-cease-and-desist-order-over-ps5-darkplates/)
- [Tom's Guide: Darkplates 2.0](https://www.tomsguide.com/news/sony-lawyers-killed-ps5-darkplates-but-darkplates-20-are-already-here)
- [TechCrunch: dbrand sues Casetify](https://techcrunch.com/2023/11/27/dbrand-is-suing-casetify-over-stolen-designs/)
- [Android Central: apology and 10.000 USD](https://www.androidcentral.com/accessories/dbrand-issues-apology-over-social-media-remark)
- [Gizmodo](https://gizmodo.com/dbrands-social-media-goes-off-the-deep-end-offers-10k-1851404479)
- [PhoneArena](https://phonearena.com/news/Dbrand-shocks-with-racist-tweet-at-customer-thinks-youll-be-ok-with-it-in-return-for-10000_id157173)
- [VGC: Killswitch "spectacularly terrible response"](https://www.videogameschronicle.com/news/dbrand-is-sending-improved-switch-2-grips-to-all-customers-after-spectacularly-terrible-response-to-detaching-claims/)
- [Android Authority: Killswitch replacements](https://www.androidauthority.com/dbrand-killswitch-switch-2-replacement-3570754/)
- [dbrand en X: Boxing Day Boxes shipped](https://x.com/dbrand/status/951233541546889217)
