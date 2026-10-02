# Correos de Shopify: cómo instalarlos

Diez plantillas de notificación para Heavy Metal Pro Stock: “The Evil One”, con el diseño aprobado en `boceto-v29/correos.html`. Los correos van en inglés (son para clientes). Cada archivo `.liquid` se pega completo en una notificación de Shopify. No hace falta tocar el tema ni instalar apps.

## Qué es cada archivo

| Archivo | Notificación en Shopify | Cuándo sale | Asunto sugerido (copiar en "Subject") |
|---|---|---|---|
| `order-confirmation.liquid` | Order confirmation | Al hacer un pedido | `Order {{ order_name }} is locked in` |
| `shipping-confirmation.liquid` | Shipping confirmation | Al marcar el pedido como enviado | `Your gear just left the shop` |
| `shipping-update.liquid` | Shipping update | Si cambia la guía o la paquetería | `New tracking info for order {{ order_name }}` |
| `out-for-delivery.liquid` | Out for delivery | Cuando la paquetería dice "en reparto" | `Your gear is out for delivery` |
| `delivered.liquid` | Delivered | Cuando la paquetería dice "entregado" | `Delivered. Go get it.` |
| `abandoned-checkout.liquid` | Abandoned checkout | Cuando alguien deja el checkout sin pagar | `You left gear in the pits` |
| `gift-card-created.liquid` | Gift card created | Al comprar una Gift Evil (le llega a quien la recibe) | `{% if gift_card.recipient %}You got {{ gift_card.initial_value \| money_without_trailing_zeros }} of evil{% else %}Your Gift Evil card is here{% endif %}` (sin la `\` antes de la barra) |
| `customer-account-invite.liquid` | Customer account invite | Si invitas a un cliente desde el admin | `Your pit pass is ready` |
| `customer-account-welcome.liquid` | Customer account welcome | Cuando un cliente activa su cuenta | `You’re in` |
| `customer-marketing-confirmation.liquid` | Customer marketing confirmation | Doble confirmación al unirse a The Evil List | `One click and you’re on The Evil List` |

Extras en esta carpeta:
- `logo-email.png`: el logo para correos (PNG, porque muchos correos bloquean SVG). Ya trae "Pro Stock · “The Evil One”" debajo, así nunca dice "Heavy Metal" solo.
- `vista-previa/`: capturas de cada correo con datos de ejemplo, a 600 px (computadora) y 375 px (celular).

Qué trae cada correo:
- **Order confirmation**: productos con foto, variante, cantidad y precio; descuentos por producto y de pedido; subtotal, envío (dice "Free" si es $0), impuestos, propina de Feed The Beast si la dejaron, total y pago con tarjeta de regalo; línea de tiempo "Printed when you order" (impreso en 5 días hábiles, Standard 2 a 5, Express 2 a 3); dirección y método de envío; botón "View my order" a la página de estado del pedido. Si el pedido es solo una Gift Evil, se esconden la línea de tiempo y la dirección.
- **Shipping confirmation**: barra de avance, paquetería, número de guía con link, fecha estimada si Shopify la tiene, aviso si el envío es parcial, botón "Track my package" y lo que va en esa caja.
- **Shipping update, Out for delivery, Delivered**: cortos, con la guía y un botón.
- **Abandoned checkout**: lo que dejó en el carrito, sin prisa falsa ni descuento, botón "Back to my cart".
- **Gift card created**: tarjeta Gift Evil con el monto, nota de quien la manda (si escribió una), código, saldo, vencimiento ("Never"), botón "Shop now" y link a la página de la tarjeta.
- **Account invite / welcome**: solo importan si usas cuentas clásicas (ver abajo).
- **Marketing confirmation**: el clic para confirmar The Evil List.

Todos los correos: un solo botón, contacto solo por el formulario (https://heavymetalprostock.com/pages/contact), firma “The Evil One” · Cat 3208 · Waterloo, WI.

## Paso 1. Logo, color y nombre del remitente (una sola vez)

1. Admin de Shopify > **Settings** (Configuración) > **Notifications** (Notificaciones).
2. Entra a **Customer notifications** (Notificaciones al cliente) y arriba a la derecha haz clic en **Customize email templates** (Personalizar plantillas de correo).
3. **Logo**: sube `logo-email.png` de esta carpeta. **Logo width** (ancho): `200` px.
4. **Accent color** (color de acento): `#1C1B19` (negro mate). Ojo: no pongas el amarillo. Este color solo lo usan los correos de Shopify que **no** reemplazamos (reembolsos, cancelaciones, etc.) para sus botones con letra blanca, y el amarillo con letra blanca no se lee. Nuestros correos ya traen el amarillo donde va.
5. **Save** (Guardar).
6. En Settings > Notifications revisa **Sender email** / nombre del remitente: que diga `Heavy Metal Pro Stock: “The Evil One”`.

## Paso 2. Pegar cada plantilla

Repite esto para cada fila de la tabla:

1. Settings > Notifications > **Customer notifications**.
2. Haz clic en la notificación (por ejemplo **Order confirmation**).
3. Clic en **Edit code** (Editar código).
4. En **Subject** (Asunto) borra lo que hay y pega el asunto sugerido de la tabla.
5. En **Email body (HTML)** selecciona todo (Ctrl+A o Cmd+A), bórralo y pega el contenido **completo** del archivo `.liquid` (abre el archivo con un editor de texto, selecciona todo y copia). El bloque `{% comment %}` del principio puede quedarse; no se ve en el correo.
6. Clic en **Save**. Arriba se ve la vista previa con datos de ejemplo de Shopify.
7. Si algo sale mal: el botón **Revert to default** (Restablecer predeterminado) deja la versión original de Shopify.

Notas por correo:
- **Out for delivery** y **Delivered** salen solo si el pedido tiene número de guía y la paquetería lo reporta. Revisa que estén activadas (hay un interruptor en cada una).
- **Abandoned checkout**: hoy Shopify manda el carrito abandonado desde **Marketing > Automations** (Automatizaciones). Si usas esa automatización de Shopify Email, ese correo se edita allá y este archivo no se usa (el texto sirve igual para copiarlo). Si usas la notificación clásica, pega este archivo y activa el envío automático en Settings > Checkout > **Abandoned checkouts** (envío a "subscribed customers" si quieres que solo le llegue a quien aceptó correos).
- **Customer marketing confirmation**: solo sale si activas la doble confirmación de The Evil List (en Settings > Notifications > Customer notifications, sección de marketing por correo, opción de pedir confirmación). Recomendado: activarla.
- **Account invite / welcome**: si la tienda usa las **cuentas de cliente nuevas** (entrar con código, sin contraseña), Shopify casi no manda estos dos. Pegarlos no hace daño y quedan listos si algún día los usa.

## Paso 3. Mandarte una prueba

1. En el editor de cada notificación (después de guardar) clic en **Send test email** (Enviar correo de prueba). Llega al correo de la cuenta de la tienda con datos de ejemplo.
2. Ábrelo en el celular y en la computadora. Revisa logo, botón y que se vean los productos.
3. Prueba completa (recomendado): haz un pedido de prueba con un código de descuento del 100% y una dirección tuya. Así ves la confirmación real; luego márcalo como enviado con un número de guía para ver Shipping confirmation. Para la Gift Evil, compra una de prueba enviada a tu propio correo.

## Lo que tienes que decidir

1. **Voz**: en el boceto el tractor habla en primera persona ("I"). Donde el texto explica cómo se imprime usé "We print every item when you order it", como pediste. Si prefieres todo en "I", se cambia esa frase.
2. **Barra de avance**: el boceto decía Ordered / Packed / Shipped / Delivered. Puse **Printed** en lugar de Packed para que cuadre con "Printed when you order". Si prefieres Packed, es un cambio de una palabra.
3. **Responder al correo**: el boceto del carrito decía "Just hit reply". Lo cambié por el link al formulario de contacto, porque el contacto es solo por formulario.
4. **Carrito abandonado**: ¿notificación clásica o automatización de Shopify Email? ¿Con descuento o sin descuento? (hoy va sin descuento, como en el boceto).
5. **Pista 3208**: el "P.S. People who dig find page 3208." va en Order confirmation, Shipping confirmation y Delivered. Si la página 3208 no está publicada todavía, quítalo o publícala antes.
6. **Logo**: si cambias el ancho en Customize email templates, 200 px se ve bien; menos de 160 hace la línea "Pro Stock" muy chica.
