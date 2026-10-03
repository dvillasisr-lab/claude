# Copy estilo dbrand: qué cambió

Fecha: 2 de octubre de 2026. Tema de trabajo: HM v14.1 (188584198223). El tema publicado no se tocó.

Cada fila es un texto que ve el cliente. Si alguna línea no te gusta, dime cuál y la regreso a como estaba (columna “Antes”).

## Resumen

- **Info kit eliminado.** Ya no se ofrece ni se menciona ningún “info kit”, “sponsor kit” ni PDF. La opción “Not sure yet” del formulario de Sponsors ahora es una pregunta abierta al equipo (“Not sure yet, I have questions”) y no promete ningún documento. Solo se promete la respuesta “within 2 business days” que ya existía.
- **Voz dbrand.** Frases cortas, seguras y con chiste, sin relleno corporativo. Precios, envíos, tallas, fechas y textos legales siguen igual. Lo que ya tenía ese tono (The Evil List, 404, Why are you here, Feed The Beast) se dejó.
- **No se tocaron:** políticas (solo la línea del kit en el archivo local), textos de consentimiento, etiquetas y errores de formularios, datos de metaobjetos que son hechos (especificaciones, crew, paquetes), botones obvios (Add to cart, Checkout) y la franja amarilla.

## Textos del tema

### Todo el sitio (barra de anuncios, menú, footer)

| Dónde | Antes | Ahora |
|---|---|---|
| `sections/footer-group.json`, `sections/hm-footer.liquid` | You're on the list. Check your inbox to confirm. | You’re in. Check your inbox to confirm. Yes, really. |
| `sections/footer-group.json`, `sections/hm-footer.liquid`, `sections/hm-schedule.liquid`, `templates/page.schedule.json` | Enter a valid email to join The Evil List. | That email looks off. Fix it and you’re in. |
| `sections/footer-group.json`, `sections/hm-footer.liquid` | You are on the sign up page. | You’re already on the sign up page. It’s right up there. |
| `sections/footer-group.json`, `sections/hm-sponsor-strip.liquid` | Your logo could be here | Your logo, right here |
| `sections/header-group.json`, `sections/hm-announcement.liquid` | Testing season [season]: join The Evil List | Testing season [season]. Get on The Evil List |
| `sections/header-group.json` | Free US shipping on orders of [free_shipping] or more | Free US shipping on [free_shipping] or more. You’re welcome. |
| `sections/hm-announcement.liquid` | Free US shipping on orders over [free_shipping] | Free US shipping over [free_shipping]. You’re welcome. |
| `sections/header-group.json`, `sections/hm-header.liquid` | Long read, in our own words | Long read. Grab a coffee. |
| `sections/header-group.json`, `sections/hm-header.liquid` | New tees and hoodies, designed by the crew in Waterloo, WI. | New tees and hoodies. Designed by the crew, not a committee. |

### Home

| Dónde | Antes | Ahora |
|---|---|---|
| `sections/hm-home-sponsor.liquid` | Pick a package, then pick your spot on the tractor. The sponsor info kit (packages, decal map, real photos) is free and comes within 2 business days. | Pick a package. Pick your spot on the tractor. Then watch your logo disappear into black smoke all season. |
| `sections/hm-home-sponsor.liquid`, `templates/index.json` | Partner with “The Evil One” | Put your name on “The Evil One” |
| `sections/hm-hero.liquid`, `templates/index.json` | “The Evil One” is a Pro Stock pulling tractor out of Waterloo, Wisconsin. Merch designed by the crew. | “The Evil One” is a Pro Stock pulling tractor out of Waterloo, Wisconsin. Merch by the crew that built it. |
| `sections/hm-home-machine.liquid`, `templates/index.json` | A Cat 3208 V8, reverse flow, in a Pro Stock tractor. A setup you won't find on any other tractor on the track. Everything on it is custom-built. | A Cat 3208 V8, reverse flow, in a Pro Stock tractor. Nobody else on the track runs this setup. Probably for a reason. Everything on it is custom-built. |

### Tienda, colección y avisos de “Notify me”

| Dónde | Antes | Ahora |
|---|---|---|
| `sections/hm-main-collection.liquid`, `templates/collection.json` | Every tee, hoodie, hat and sticker from the crew behind “The Evil One”. Printed when you order. | Tees, hoodies, hats and stickers from the crew behind “The Evil One”. Printed when you order it, not before. |
| `sections/hm-main-collection.liquid`, `templates/collection.json` | Out for a short window and a set quantity. When it closes or sells out, it is gone. | Short window. Set quantity. When it closes or sells out, it’s gone. No encores. |
| `sections/hm-home-shop.liquid`, `sections/hm-main-collection.liquid`, `templates/collection.json`, `templates/index.json` | The first drop from the crew behind “The Evil One” is on its way. Get a heads up when it lands. | The first drop from the crew behind “The Evil One” is on its way. Leave your email. We’ll yell when it lands. |
| `hm-home-shop.liquid` (aviso después de dejar el correo) | You are on the list. We will email you when the drop goes live. | You’re on the list. One email when the drop goes live. That’s it. |
| `hm-coming-soon.liquid` (aviso después de dejar el correo) | You are on The Evil List. We will email you when the drop goes live. | You’re on The Evil List. One email when the drop goes live. That’s it. |
| `hm-notify-modal.liquid` (ventana Notify me) | We will email you the moment it drops. One email, no spam. | One email the second it drops. Then we leave you alone. |
| `hm-notify-modal.liquid` (ventana Notify me, después de enviar) | You are on the list. We will email you when it is available. | You’re on the list. One email when it’s ready. Promise. |
| `hm-quick-add.js` (ventana Notify me de producto agotado) | We will email you if it comes back. One email, no spam. | One email if it comes back from the dead. That’s it. |
| `hm-quick-add.js` (ventana Notify me de producto que viene) | We will email you the moment it drops. One email, no spam. | One email the second it drops. Then we leave you alone. |
| `hm-main-collection.liquid` (filtros sin resultados) | Try another size or color, or clear the filters to see everything in this category. | You filtered a little too hard. Try another size or color, or clear the filters. |

### Special edition

| Dónde | Antes | Ahora |
|---|---|---|
| `sections/hm-special-edition.liquid`, `templates/collection.special-edition.json`, `templates/product.special-edition.json` | One run only. When the window closes or the run sells out, it is gone. | One run only. When the window closes or the run sells out, it’s gone. Crying won’t bring it back. |
| `sections/hm-special-edition.liquid`, `templates/collection.special-edition.json`, `templates/product.special-edition.json` | Sold out. Thank you. | Sold out. You animals. Thank you. |
| `sections/hm-special-edition.liquid`, `templates/collection.special-edition.json`, `templates/product.special-edition.json` | When a special edition closes or sells out, it moves here so you can see every run “The Evil One” has done. | When a special edition closes or sells out, it retires here. Look, don’t touch. |

### Carrito

| Dónde | Antes | Ahora |
|---|---|---|
| `hm-main-cart.liquid` y `hm-cart-drawer.liquid` (carrito vacío) | Your cart is empty. | Your cart is empty. Bold strategy. |
| `hm-cart.js` (barra de envío gratis) | You are $X away from free US shipping | You’re $X away from free US shipping. So close. |
| `hm-cart.js` (barra de envío gratis, meta lograda) | You unlocked free US shipping. | Free US shipping unlocked. Look at you. |
| `hm-cart.js` (aviso al agregar la propina Feed The Beast) | Fuel tip added. Thank you. | Fuel tip added. The crew salutes you. |

### Producto

| Dónde | Antes | Ahora |
|---|---|---|
| Descripción del producto “The Evil One” Truck Tee (dato de la tienda) | …heavy-metal graphic [raya larga] complete with a roaring engine, gas mask motif, and explosive backdrop [raya larga] gives the shirt… (dos rayas largas) | …heavy-metal graphic, complete with a roaring engine, gas mask motif, and explosive backdrop, gives the shirt… |

### Our Story (About)

| Dónde | Antes | Ahora |
|---|---|---|
| `sections/hm-story-hero.liquid`, `templates/page.about.json` | It started in 2014 with one idea. That idea became a Pro Stock tractor, built by a family in its own shop. And that tractor was nicknamed “The Evil One”. | It started in 2014 with one idea. The idea became a Pro Stock tractor, built by one family in its own shop. Then it got a nickname: “The Evil One”. It earned it. |
| `sections/hm-story-read.liquid`, `templates/page.about.json` | The sketches, the nights and weekends, the family shop, and the night the engine fired and lightning struck. The whole story, the way we tell it. | The sketches, the nights and weekends, the family shop, and the night the engine fired and lightning struck. The whole story. Long, loud, ours. |
| `sections/hm-story-bolt.liquid`, `templates/page.about.json` | Sound on. This is how it sounded in the shop when the engine fired and the lightning hit. | Sound on. Sorry, neighbors. This is the shop the moment the engine fired and the lightning hit. |
| `sections/hm-story-pair.liquid`, `templates/page.about.json` | The song “The Evil One” rolls up to the line with. Turn it up before the next pull. | The song “The Evil One” rolls up to the line with. Turn it up. Louder. No, louder. |
| `sections/hm-story-pair.liquid`, `templates/page.about.json` | What plays in the trailer and the pit | What plays in the trailer and the pit, loud |
| `sections/hm-story-crew.liquid`, `templates/page.about.json` | Family, friends and two mascots. | Family, friends and two mascots. Guess who’s in charge. |
| `sections/hm-story-cta.liquid`, `templates/page.about.json` | Merch designed by the crew. Every order fuels the team. | Merch designed by the crew. Every order keeps the diesel flowing. |

### Pit Log

| Dónde | Antes | Ahora |
|---|---|---|
| `sections/hm-pit-log.liquid`, `templates/blog.pit-log.json` | Every test day, exhibition, pull and win of “The Evil One”, logged by the crew. | Every test day, exhibition, pull and win of “The Evil One”. The good days too. Logged by the crew. |
| `sections/hm-pit-log.liquid`, `templates/blog.pit-log.json` | Big days from the log show up here. | Big days get pinned here. Working on it. |
| `sections/hm-pit-log.liquid`, `templates/blog.pit-log.json` | First pulls, first wins, full pulls: the days worth framing get pinned here. | First pulls, first wins, full pulls. The days worth framing. |
| `sections/hm-pit-log.liquid`, `templates/blog.pit-log.json` | Still chasing the first one. The day it happens, it goes up here first. | Still chasing the first one. When it lands, it goes up here before we stop yelling. |
| `sections/hm-pit-log.liquid`, `templates/blog.pit-log.json` | The first entry from the pit shows up here. | The first entry from the pit lands here. Grease stains optional. |
| `sections/hm-pit-log.liquid`, `templates/blog.pit-log.json` | Photos, video and the day’s notes, straight from the pit. | Photos, video and the day’s notes. Straight from the pit, still smelling like diesel. |

### The Machine (Spec sheet)

| Dónde | Antes | Ahora |
|---|---|---|
| `sections/hm-machine-faq.liquid`, `templates/page.spec-sheet.json` | What’s worth knowing before you watch it pull. | What people ask us at the fence. Usually yelling. |

### Schedule

| Dónde | Antes | Ahora |
|---|---|---|
| `templates/page.schedule.json` | Pro Stock tractors are loud. Ear plugs or muffs for everyone, kids first. | Pro Stock tractors are loud. Like, really loud. Ear plugs or muffs for everyone, kids first. |

### Sponsors

| Dónde | Antes | Ahora |
|---|---|---|
| `sections/hm-sponsors-hero.liquid` | Not sure yet? Get the info kit | Not sure yet? Ask us anything |
| `sections/hm-sponsors-packages.liquid` | Ask for the info kit and we’ll send you the details first. | Got questions before then? Ask, we don’t bite. |
| `sections/hm-sponsors-packages.liquid`, `sections/hm-sponsors-request.liquid` | Get the info kit | Ask us anything |
| `sections/hm-sponsors-packages.liquid`, `sections/hm-sponsors-request.liquid` | Request the info kit | Ask us anything |
| `sections/hm-sponsors-request.liquid` | Tell us a little about your business and pick a package, or just ask for the info kit. | Tell us about your business and pick a package. Not sure yet? Just ask. |
| `sections/hm-sponsors-request.liquid` | Not sure yet (send me the info kit) | Not sure yet, I have questions |
| `sections/hm-sponsors-request.liquid` | Not sure yet?Pick “Not sure yet” above to request our sponsor info kit: a short PDF with the packages, who sees your logo, the decal map and real photos. We email it within 2 business days. No commitment. | Not sure yet?Pick “Not sure yet” above and ask us anything. Packages, logo spots, the decal map, how loud it gets. No commitment, no pressure. |
| `sections/hm-sponsors-request.liquid` | Thanks, your request is in. | Got it. Your request is in. |
| `sections/hm-sponsors-request.liquid` | We’ll email our sponsor info kit (a short PDF to help you decide, no commitment) within 2 business days. | We reply within 2 business days. Nothing is signed until we agree on it in writing. |
| `sections/hm-sponsors-request.liquid`, `templates/page.sponsors.json` | Title Partner puts your name in the team name and the biggest logo on the tractor. Pit Partner covers the shirt sleeve, the trailer, the website and monthly social posts. Crew Supporter is built for local shops and fans. Not sure? Pick “Not sure yet” in the form and we’ll send you the info kit. | Title Partner puts your name in the team name and the biggest logo on the tractor. Pit Partner covers the shirt sleeve, the trailer, the website and monthly social posts. Crew Supporter is built for local shops and fans. Still stuck? Pick “Not sure yet” in the form and ask us. |
| `sections/hm-sponsors-request.liquid`, `templates/page.sponsors.json` | [pitch], in the stands alone. Streams and social media come on top of that. Current numbers are in our sponsor info kit. | [pitch], in the stands alone. Streams and social media come on top of that. Want the latest numbers? Ask us in the form. |
| `sections/hm-sponsors-request.liquid`, `templates/page.sponsors.json` | If you asked for the sponsor info kit, we email it within 2 business days: a short PDF with the packages, who sees your logo, the decal map and real photos, so you can decide. If you picked a package, we also reply to set up a call. No commitment: nothing is signed until we agree on the terms in writing. | A human reads it and replies within 2 business days. Picked a package? We set up a call. Picked “Not sure yet”? We answer your questions. No commitment: nothing is signed until we agree on the terms in writing. |
| `sections/hm-sponsors-placements.liquid` | What each package gets is listed under each place. | Every spot we’ve got, and which package gets it. |
| `hm-sponsors-request.liquid` (opción del formulario) | Not sure yet: send the info kit | Not sure yet, I have questions |
| `hm-sponsors-request.liquid` (botón con “Not sure yet”) | Request the info kit | Send my question |

### Book the team

| Dónde | Antes | Ahora |
|---|---|---|
| `sections/hm-book.liquid`, `templates/page.book.json` | We confirm the details with you in writing, then haul “The Evil One” in. | We confirm the details in writing, then haul “The Evil One” in. Earplugs recommended. |
| `sections/hm-book.liquid` | Bring a Pro Stock pulling tractor built from scratch in Waterloo, WI, to your event. Put it on display, run it for the crowd where the track allows it, and meet the driver. | A Pro Stock pulling tractor built from scratch in Waterloo, WI, at your event. Park it for show, run it for the crowd where the track allows, and meet the driver. Loud is included. |
| `sections/hm-book.liquid`, `templates/page.book.json` | Send the form below with the date, the place and the kind of event. | Fill in the form below: date, place, kind of event. That’s the hard part. |

### Contact

| Dónde | Antes | Ahora |
|---|---|---|
| `sections/hm-contact.liquid`, `templates/page.contact.json` | Questions about an order, merch or sponsorship? Send us a message and we’ll get back to you within 2 business days. | Order problem, merch question, sponsorship idea? Send it over. A human reads it and replies within 2 business days. |
| `sections/hm-contact.liquid`, `templates/page.contact.json` | How can we help? | What’s up? Order number helps. |
| `sections/hm-contact.liquid`, `templates/page.contact.json` | Thanks. Your message is in. We’ll reply within 2 business days. | Got it. A human reads this, not a bot. We reply within 2 business days. |

### The Evil List

| Dónde | Antes | Ahora |
|---|---|---|
| `sections/hm-evil-list.liquid`, `templates/page.evil-list.json` | New merch and special editions land in your inbox before anyone else hears about them. | New merch and special editions hit your inbox before the internet finds out. |
| `sections/hm-evil-list.liquid` | One list for everything. Email only. | One list. Everything on it. Email only. |

### Página FAQ

| Dónde | Antes | Ahora |
|---|---|---|
| `sections/hm-faq.liquid`, `templates/page.faq.json` | Orders, shipping, sizing and the tractor. Search or pick a topic. | Orders, shipping, sizing and the tractor. We’ve heard it all. Search or pick a topic. |
| `sections/hm-faq.liquid`, `templates/page.faq.json` | Send us a message and we’ll get back to you within 2 business days. | Ask a human. We reply within 2 business days. |

### Gallery y álbumes

| Dónde | Antes | Ahora |
|---|---|---|
| `sections/hm-gallery.liquid` | Every pull, exhibition and test day of “The Evil One”. | Every pull, exhibition and test day of “The Evil One”. Smoke included. |
| `sections/hm-album.liquid` | The crew posts photos and video after each pull. Check back soon. | The crew posts photos and video after each pull. Once the diesel washes off. |

### Página 404

| Dónde | Antes | Ahora |
|---|---|---|
| `sections/hm-404.liquid`, `templates/404.json` | This pull ended early. The page you want isn’t on the track: it moved, or it never made the run. | This pull ended early. That page isn’t on the track. It moved, or it never made the run. Awkward. |

### Políticas

| Dónde | Antes | Ahora |
|---|---|---|
| `content/policies/privacy.html` (archivo local; la política en vivo es otra, ver nota) | To answer sponsorship requests and send the sponsor kit you asked for. | To answer sponsorship requests. |

### Ajustes del editor (Sponsors) que cambiaron de nombre

| Dónde | Antes | Ahora |
|---|---|---|
| Sponsors: hero · enlace junto al botón | Ajuste “Info kit link” | Ajuste “Not sure yet link” (sigue siendo un enlace subrayado que baja al formulario) |
| Sponsors: FAQ and form · título con “Not sure yet” | Ajuste “Title for Not sure yet” = Request the info kit | Mismo ajuste = Ask us anything |
| Sponsors: FAQ and form · nota | Ajuste “Info kit note” | Ajuste “Not sure yet note” |

## Preguntas frecuentes (metaobjetos FAQ item, ya actualizados en la tienda)

Las preguntas no cambiaron, solo las respuestas. Se ven en FAQ, The Machine, Sponsors y The Evil List según la página de cada una. Los links siguen iguales, salvo “What engine does it run?”, que ahora apunta a /pages/spec-sheet (antes /pages/the-machine).

| Dónde (pregunta) | Antes | Ahora |
|---|---|---|
| Do I need an account to order? | No. You can check out as a guest. If you later sign in with the same email, your past orders show up in your account. | No. Check out as a guest, no strings attached. Sign in later with the same email and your past orders show up in your account. |
| Where is my order confirmation? | We email it right after checkout. If you can’t find it, check your spam or promotions folder, then sign in to your account to see the order. Still nothing? Message us with the email you used. | We email it right after checkout. Can’t find it? Check spam or promotions, the usual suspects. Then sign in to your account to see the order. Still nothing? Message us with the email you used. |
| Can I change or cancel my order? | Every item is printed when you order it, so message us as soon as possible with your order number: pick “Order help” on the contact form. Once an order goes to print we can’t change it, so the sooner you reach us the better. | Move fast. Every item is printed when you order it, so message us right away with your order number: pick “Order help” on the contact form. Once an order goes to print, it’s locked in. Sooner is better. |
| How do I reach you? | Use the contact form and pick a topic. We reply within 2 business days. For other ways to reach us, see our Contact Information policy. | Use the contact form and pick a topic. A human replies within 2 business days. Other ways to reach us are in our Contact Information policy. |
| I entered the wrong shipping address. What now? | Message us right away with your order number and the correct address. If the order hasn’t shipped, we update it. If it already shipped, we’ll work with the carrier, but we can’t promise a reroute. | Typos happen. Message us right away with your order number and the correct address. Not shipped yet? We fix it. Already shipped? We’ll work with the carrier, but we can’t promise a reroute. |
| How long does shipping take? | Printed when you order, ships in 5 days. After that, Standard takes 2 to 5 business days and Express 2 to 3. Details in the Shipping Policy. | Printed when you order, ships in 5 days. After that, Standard takes 2 to 5 business days and Express 2 to 3. The fine print lives in the Shipping Policy. |
| How much is shipping? | Standard shipping starts at $6.99 and is free on orders of $75 or more. Express starts at $12.99. You see the exact cost at checkout before you pay. | Standard starts at $6.99 and is free on orders of $75 or more. Express starts at $12.99. You see the exact cost at checkout before you pay. No surprises. |
| Do you ship outside the US? | Not right now. We ship to US addresses only. | Not right now. US addresses only. Sorry, rest of the planet. |
| How do I track my order? | When your order ships, we email you a tracking link. You can also see it in your account. / You don’t need an account: open the order status page from that email, or go to Account > Orders and use the email you ordered with. | When your order ships, we email you a tracking link. It’s also in your account. / No account? No problem: open the order status page from that email, or go to Account > Orders and use the email you ordered with. |
| My tracking hasn’t updated. Is something wrong? | A label is often created before the carrier scans the package, so tracking can sit still for a bit. If it still hasn’t moved after a few business days, message us with your order number and we’ll check with the carrier. | Probably not. Labels get created before the carrier scans the package, so tracking can sit still for a bit. Annoying, but normal. If it still hasn’t moved after a few business days, message us with your order number and we’ll chase the carrier. |
| My package says delivered, but I don’t have it. | Check around your door, mailbox and with neighbors, and give it one more day: carriers sometimes mark a package delivered early. If it still hasn’t shown up, message us with your order number and we’ll help sort it out with the carrier. | Check around your door, the mailbox and the neighbors, then give it one more day: carriers sometimes mark a package delivered early. Still missing? Message us with your order number and we’ll sort it out with the carrier. |
| Will all my items arrive together? | Not always. Different items can be printed in different places, so they may ship in separate packages. Each package gets its own tracking email. | Not always. Different items can be printed in different places, so they may ship in separate packages. Each package gets its own tracking email. Double the mail, double the fun. |
| Can I return or exchange an item? | Everything is printed when you order it, so returns work differently than a regular store. What’s covered, and for how long, is in the Refund Policy. | Everything is printed when you order it, so returns work differently than at a big-box store. What’s covered, and for how long, is in the Refund Policy. |
| My item arrived damaged or misprinted. | Sorry about that. Send us your order number and a photo of the problem: pick “Returns & exchanges” on the contact form. Next steps follow the Refund Policy. | Not cool. Sorry about that. Send us your order number and a photo of the problem: pick “Returns & exchanges” on the contact form. Next steps follow the Refund Policy. |
| I ordered the wrong size. | Check the Refund Policy for what we can do. Next time, compare the Size guide with a shirt you own before ordering. | Happens to the best of us. Check the Refund Policy for what we can do. Next time, compare the Size guide with a shirt you own before ordering. |
| How do I start a return or exchange? | Message us with your order number on the contact form. Please don’t mail anything back before we reply. | Message us with your order number on the contact form. Please don’t mail anything back before we reply. Surprise packages confuse us. |
| How do I measure myself? | The easiest way is to lay a shirt you like flat and measure it. The Size guide shows where to measure chest, length and sleeve. | Easiest way: lay a shirt you like flat and measure it. The Size guide shows where to measure chest, length and sleeve. Two minutes, tops. |
| How do I wash printed merch? | Turn it inside out and wash cold. · Hang dry. · Don’t iron over the print and skip bleach. / That keeps the print sharp for more seasons. | Turn it inside out and wash cold. · Hang dry. · Don’t iron over the print and skip bleach. / That keeps the print sharp for more seasons. Your dryer is not your friend. |
| Who prints the merch? | We print every item when you order it. That’s why nothing sits in a warehouse and why orders take a few days to ship. | We print every item when you order it. That’s why nothing sits in a warehouse, and why orders take a few days to ship. Worth the wait. |
| The color looks different from the picture. | Screens show color differently, so the printed item can look slightly different. If it looks clearly wrong, send us a photo. | Screens lie a little, so the printed item can look slightly different. If it looks clearly wrong, send us a photo. |
| What does “Coming soon” mean? | The design is done and it drops soon, but it can’t be ordered yet. Tap Notify me on the item and we’ll email you the moment it goes live. Subscribers to The Evil List hear about every drop first. | The design is done, it just can’t be ordered yet. Tap Notify me on the item and we’ll email you the moment it goes live. The Evil List hears about every drop first. |
| How does “Notify me” work? | Enter your email on the item page. We send you one email when it drops or is back in stock. It doesn’t reserve an item for you, and it doesn’t sign you up for anything else. To get every drop and pull day, join The Evil List. | Enter your email on the item page. We send one email when it drops or is back in stock. That’s it. It doesn’t reserve an item, and it doesn’t sign you up for anything else. Want every drop and pull day? Join The Evil List. |
| A size is sold out. Will it come back? | Sometimes, yes. Some items and sizes run in limited numbers. When a product page shows “Almost gone!” or how many are left, that count is real. If a size sells out, tap Notify me on the product page and we’ll email you when it’s back. Special edition pieces don’t come back. | Sometimes, yes. Some items and sizes run in limited numbers. When a product page says “Almost gone!” or shows how many are left, that count is real. No fake urgency here. If a size sells out, tap Notify me on the product page and we’ll email you when it’s back. Special edition pieces don’t come back. |
| What does “Almost gone!” mean? | Only a few pieces are left. When they’re gone, the item switches to Sold out. | Only a few pieces are left. When they’re gone, the item switches to Sold out. Snooze, lose. |
| How does sign-in work? There’s no password. | Right, no password to remember. Enter your email on the Account page, we email you a 6-digit code, and you type it in to sign in. | Right, no password to forget. Enter your email on the Account page, we email you a 6-digit code, and you type it in. Done. |
| What is The Evil List? | Our one email list: new merch drops and a heads-up before every pull. No spam. See what you get on The Evil List. | Our one and only email list: new merch drops and a heads-up before every pull. No spam. We’re too busy wrenching. See what you get on The Evil List. |
| How do I unsubscribe? | Use the unsubscribe link at the bottom of any email from The Evil List, or turn it off in your account. | Use the unsubscribe link at the bottom of any email from The Evil List, or turn it off in your account. No hard feelings. Mostly. |
| How do I sponsor the team? | There are three packages, from Crew Supporter for local shops up to Title Partner. See what each includes and costs on Sponsors, or pick “Sponsorship” on the contact form. / Not sure yet? Request our sponsor info kit on Sponsors: a short PDF with the packages, who sees your logo, the decal map and real photos. We email it within 2 business days. It’s information to help you decide, not a contract. No commitment. | Three packages, from Crew Supporter for local shops up to Title Partner. See what each includes and costs on Sponsors, or pick “Sponsorship” on the contact form. / Not sure yet? Pick “Not sure yet” in the form on Sponsors and ask us anything. We reply within 2 business days. No commitment. |
| When is there a new one? | There’s no fixed calendar. A Special edition drops around a big moment of the season. The Evil List gets the heads-up first: sign up at the bottom of any page. | There’s no fixed calendar. A Special edition drops around a big moment of the season. The Evil List hears first, everyone else hears too late: sign up at the bottom of any page. |
| Will a Special edition come back? | No. When the run sells out, it’s gone. Regular designs stay in the shop. | No. When the run sells out, it’s gone. No encores. Regular designs stay in the shop. |
| Do you post bad runs too? | Yes. We won’t sugarcoat it. Early runs ended short, and the Pit Log says so. | Yes. We won’t sugarcoat it. Early runs ended short, and the Pit Log says so. Bad days are part of the deal. |
| How much horsepower does it make? | Unknown. | Unknown. We’ll let the track answer. |
| What engine does it run? | A Cat 3208 V8, reverse flow, taken from 636 to 680 cubic inches, with a single large turbo. Full specs on The Machine. | A Cat 3208 V8, reverse flow, taken from 636 to 680 cubic inches, with a single large turbo. Full specs on The Machine. |
| What’s the walk-up song? | Fear of the Dark, Iron Maiden. Play it on Spotify | Fear of the Dark, Iron Maiden. Played loud. Play it on Spotify |
| What is a full pull? | Dragging the sled all the way to the end of the track. When more than one tractor goes the distance, those tractors come back for a pull-off. “The Evil One” is still chasing its first one. | Dragging the sled all the way to the end of the track. When more than one tractor goes the distance, those tractors come back for a pull-off. “The Evil One” is still chasing its first one. Working on it. |
| How fast does it go down the track? | We’ll post it once we’ve measured it. | We’ll post it once we’ve measured it. No guessing. |
| Where can I see it, and can I get close in the pits? | Upcoming pulls are on the Schedule. Pit access depends on each event: some pulls open the pits to fans, others need a pit pass. Check with the organizer, and if you find us, come say hi. | Upcoming pulls are on the Schedule. Pit access depends on each event: some pulls open the pits to fans, others need a pit pass. Check with the organizer, and if you find us, come say hi. We don’t bite. |
| Which package fits my business? | Title Partner puts your name in the team name and the biggest logo on the tractor. Pit Partner covers the shirt sleeve, the trailer, the website and monthly social posts. Crew Supporter is built for local shops and fans. Not sure? Pick “Not sure yet” in the form and we’ll send you the info kit. | Title Partner puts your name in the team name and the biggest logo on the tractor. Pit Partner covers the shirt sleeve, the trailer, the website and monthly social posts. Crew Supporter is built for local shops and fans. Still stuck? Pick “Not sure yet” in the form and ask us. |
| How many people will see my brand? | Your brand in front of 100,000+ fans across 20+ pulls a season (est.), in the stands alone. Streams and social media come on top of that. Current numbers are in our sponsor info kit. | Your brand in front of 100,000+ fans across 20+ pulls a season (est.), in the stands alone. Streams and social media come on top of that. Want the latest numbers? Ask us in the form. |
| What happens after I send the form? | If you asked for the sponsor info kit, we email it within 2 business days: a short PDF with the packages, who sees your logo, the decal map and real photos, so you can decide. If you picked a package, we also reply to set up a call. No commitment: nothing is signed until we agree on the terms in writing. | A human reads it and replies within 2 business days. Picked a package? We set up a call. Picked “Not sure yet”? We answer your questions. No commitment: nothing is signed until we agree on the terms in writing. |

## Notas para ti

- **Política de privacidad en vivo.** La que muestra la tienda es la plantilla automática de Shopify, no nuestro archivo. No menciona ningún kit, pero al final dice “Heavy Metal Prostock: The Evil One”. No la toqué porque es texto legal. Si quieres, cambio solo ese nombre a Heavy Metal Pro Stock: “The Evil One”, o subo nuestra versión.
- **Página de contraseña.** No toqué `templates/password.json` porque en el tema de trabajo es distinto a la última versión guardada (puede que lo hayas editado en el personalizador). Tenía pensado: “Still tightening bolts. Be the first to know when we open.” en lugar de “Be the first to know when we launch.”
- **Sponsors en celular.** Arreglé un corte en el hero: la línea de datos (Pro Stock tractor built from scratch · Waterloo, WI · …) no podía partirse y empujaba el título y el enlace “Not sure yet?” fuera de la pantalla. Ahora se acomoda en varias líneas.
