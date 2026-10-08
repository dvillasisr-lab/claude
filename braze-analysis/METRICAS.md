# Definiciones de métricas

Todos los agentes usan estas fórmulas y estos defaults. Si una tabla no permite calcular algo, se dice y se propone proxy marcado como tal.

## Deduplicación antes de cualquier conteo

- Envíos: una fila por `dispatch_id` + `user_id` (si no hay `dispatch_id`, por `send_id` + `user_id` + `time` redondeado al minuto).
- Eventos (open, click, bounce, etc.): una fila por `id` del evento. Para tasas "únicas" se cuenta un usuario una vez por envío.
- Canvas: un mensaje es un `canvas_step_id` + `dispatch_id` + `user_id`. No sumar entradas al Canvas como mensajes.

## Clasificación de tipo de comunicación

| Tipo | Regla por defecto |
|---|---|
| Transaccional | Nombre o tag contiene: order, pedido, confirm, otp, password, recibo, factura, envío, shipping, ticket; o `schedule_type` = API triggered con conversión nula y volumen diario estable |
| Lifecycle | Nombre o tag contiene: welcome, bienvenida, onboarding, winback, reactivación, abandon, carrito, cumpleaños, aniversario; o es Canvas con entrada por evento |
| Promocional | Todo lo demás con schedule programado o one-shot a segmento grande |
| Operativo | Webhooks y mensajes internos |

El analista registra la regla aplicada y las campañas que quedaron ambiguas.

## Métricas por campaña y canal

| Métrica | Fórmula | Denominador |
|---|---|---|
| Envíos | count distinct envíos | |
| Entregados | envíos con evento delivery (email, SMS, WhatsApp) o envíos menos bounces (push) | |
| Tasa de entrega | entregados / envíos | envíos |
| Tasa de apertura única | usuarios con open / entregados | entregados |
| Tasa de clic única | usuarios con click / entregados | entregados |
| CTOR | usuarios con click / usuarios con open | abiertos |
| Tasa de conversión | conversiones atribuidas / envíos | envíos |
| Ingreso por 1,000 envíos | suma de ingreso atribuido / envíos × 1000 | envíos |
| Tasa de baja | unsubscribes / entregados | entregados |
| Tasa de rebote duro | hard bounces / envíos | envíos |
| Tasa de spam | marcas de spam / entregados | entregados |
| Bajas por 1,000 envíos | unsubscribes / envíos × 1000 | envíos |

Atribución de conversión: la que trae Braze en `users_campaigns_conversion` y `users_canvas_conversion`. Si no existe, último clic en 72 h y marcar como proxy.

Push: la apertura es `pushnotification_open`. `influencedopen` se reporta aparte, nunca sumado.

## Benchmarks de referencia por canal (para semáforo, no para juicio final)

| Canal | Apertura | Clic | Baja | Comentario |
|---|---|---|---|---|
| Email promocional | 15 a 25 % | 1.5 a 3 % | < 0.3 % | Apertura inflada por Apple MPP, usar clic como señal principal |
| Email transaccional | 40 a 60 % | 5 a 15 % | < 0.1 % | |
| Push | 3 a 10 % directo | n/a | n/a | Varía mucho por OS y permisos |
| SMS | n/a | 5 a 15 % clic en link | < 1 % opt-out | |
| WhatsApp | 70 a 90 % read | 10 a 30 % | < 1 % | |
| In-app | n/a | 5 a 20 % | n/a | Sobre impresiones |
| Content Card | n/a | 2 a 10 % | n/a | Sobre impresiones |

Semáforo: verde dentro o arriba del rango, amarillo hasta 30 % debajo, rojo más abajo.

## Cuadrantes de eficiencia

Eje X: envíos (mediana como corte). Eje Y: conversión o ingreso por 1,000 envíos (mediana como corte).

- Alto volumen, bajo resultado: candidata a apagar, re-segmentar o rehacer.
- Alto volumen, alto resultado: proteger.
- Bajo volumen, alto resultado: escalar audiencia.
- Bajo volumen, bajo resultado: revisar si vale mantener.

## Frecuencia y presión

- Mensajes por usuario por semana = envíos al usuario / semanas con al menos un envío en el periodo. Reportar también sobre semanas totales del periodo.
- Umbral de presión por defecto: 5 mensajes por semana promocional+lifecycle. Transaccional no cuenta.
- Solapamiento: días en que un usuario recibe 3 o más campañas distintas.
- Fatiga: tasa de baja por decil de frecuencia. Si el decil 10 tiene baja 2 veces o más que el decil 5, hay fatiga.

## Vista por usuario (lente H)

Una fila por `external_user_id` (o `user_id` si no hay externo) con:

| Columna | Definición |
|---|---|
| msgs_total | envíos dedup en el periodo |
| msgs_email, msgs_push, msgs_sms, msgs_whatsapp, msgs_inapp, msgs_contentcard | por canal |
| msgs_transaccional, msgs_lifecycle, msgs_promocional | por tipo |
| msgs_por_semana | msgs_total / semanas del periodo |
| campanas_distintas | count distinct campaign_id + canvas_id |
| primer_envio, ultimo_envio | min y max de time |
| email_sub, push_sub | estado global al cierre del periodo: opted_in, subscribed, unsubscribed, desconocido |
| grupos_sub_in, grupos_sub_out | grupos de suscripción en los que está dentro y fuera |
| fecha_baja | último cambio a unsubscribed si existe |
| promos_despues_de_baja | envíos promocionales con time > fecha_baja. Debe ser 0. |
| opens, clicks, conversiones, ingreso | agregados del usuario |

Estado de suscripción: se toma el último `users_behaviors_subscription_globalstatechange` por usuario y canal antes del cierre del periodo. Si no hay tabla de cambios, usar el export de usuarios y marcar la fecha del snapshot.

Cortes para el análisis: distribución de msgs_total (percentiles 50, 90, 99), por estado de suscripción, por país o segmento si existe, top 100 usuarios más contactados, usuarios suscritos con 0 mensajes.

## Costo y gasto (lente I)

| Concepto | Cálculo |
|---|---|
| Costo variable por envío | SMS y WhatsApp: tarifa por país del proveedor × envíos. Email: tarifa por envío si el proveedor cobra por volumen, si no 0. Push, in-app, Content Card: 0 variable. |
| Costo fijo prorrateado | Contrato Braze mensual / envíos del mes, o / MAU del mes, se reportan ambos. |
| Gasto por campaña | suma costo variable + fijo prorrateado de sus envíos |
| Costo por conversión | gasto / conversiones atribuidas |
| Costo por 1,000 envíos | gasto / envíos × 1000 |
| Ingreso neto | ingreso atribuido menos gasto |
| Gasto desperdiciado | gasto en campañas del cuadrante alto volumen y bajo resultado, más gasto en envíos a usuarios dados de baja o con rebote duro previo |

Si no hay tarifas reales, usar tarifas de lista del proveedor y marcar cada cifra como estimación con el supuesto al lado.

## Gobernanza (lente D)

- Owner = `teams` del export, si no `tags`, si no prefijo del nombre, si no "sin owner". Registrar la fuente.
- Concentración = % de envíos de los 3 equipos con más volumen.
- Campañas huérfanas = sin team, sin tag y sin prefijo reconocible.
- Duplicadas en intención = mismo tipo, mismo canal, audiencia con solapamiento > 50 % y ventana de envío que coincide.

## Formato de cada hallazgo

```
### H-x. Afirmación en una frase
Cifra: ...   Periodo: ...   Denominador: ...
Query: (bloque SQL o código)
Confianza: alta | media | baja   Motivo: ...
Implicación: qué hacer con esto
```
