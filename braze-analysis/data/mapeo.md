# Mapeo de tablas y traducción de métricas

Paso 0 del plan. Hecho con los campos y la fila de ejemplo que me pasaste, sin acceso a la data. Lo que digo "a confirmar" se valida con una query cuando corramos.

Contexto que leo de los datos: fintech en México (teléfonos +52), productos KCash (préstamos) y KPay (pagos). La conversión que Braze mide es solicitar un préstamo (`applied_for_loan`) y que se otorgue (`is_converted`) con un monto (`gross_amount`).

---

## 1. Inventario de tablas

| # | Tabla | Qué es | Una fila es | Para qué la usamos |
|---|---|---|---|---|
| 1 | `braze._dim_braze_canvas` | Catálogo de Canvas (flujos automatizados multi paso) | Un Canvas | Inventario, dueño, canales, estado |
| 2 | `braze._dim_braze_canvas_step` | Catálogo de pasos de Canvas | Un paso de un Canvas | Qué mensaje concreto se envió dentro del flujo y por qué canal |
| 3 | `braze._dim_braze_campaign` | Catálogo de campañas (envíos sueltos o programados) | Una campaña | Inventario, dueño, canales, estado |
| 4 | `braze._dim_braze_device` | Dispositivos | Un dispositivo | Mix iOS y Android. Hoy sin llave visible para unirla (ver dudas) |
| 5 | `braze._dim_braze_users` | Usuarios en Braze | Un usuario | Suscripción actual a email y push, antigüedad, atribución de instalación |
| 6 | `xplore._dim_braze_users_and_communications` | **Tabla principal de hechos.** Aunque se llama dim, es un hecho | Un usuario × una comunicación × una fecha, con banderas de qué pasó (enviado, entregado, abierto, clic, baja, conversión) | Casi todas las métricas: volumen, embudo, eficiencia, frecuencia, vista por usuario |
| 7 | `xplore._fct_braze_canvas_user_engagement` | Engagement por paso de Canvas, con experimentos y grupo de control | Un usuario × un paso de Canvas × una fecha | Eficiencia por paso, lift contra grupo control, resultados de A/B |
| 8 | `braze_semantic_layer._fct_braze_canvas_user_engagement` | Copia de la 7 en la capa semántica. Mismas columnas | Igual que 7 | Usar solo una de las dos (ver dudas) |
| 9 | `product.customer_golden_dataset.dim_braze_filters` | Filtros de contactabilidad y riesgo por cliente | Un cliente | Si se puede contactar, por qué canal, si está dado de baja por canal, etapa del ciclo de vida, riesgo |

Lo que **no** hay y afecta el plan:

- No hay tabla de costos ni tarifas. La lente de gasto necesita que me pases tarifas.
- No hay rebotes ni marcas de spam. La salud de lista se mide solo con bajas.
- No hay historial de cambios de suscripción. Solo el estado actual (tabla 5 y 9) y el evento `email_unsubscribe` con fecha (tabla 6).
- No hay SMS. Los canales son email, push, WhatsApp, in-app, banner y webhook.
- No hay `dispatch_id`. La tabla 6 ya viene resumida por usuario, comunicación y día, con banderas verdadero/falso. Eso simplifica y también limita (no vemos reenvíos el mismo día).

---

## 2. Cómo se unen las tablas

| De | Columna | A | Columna | Relación | Confianza |
|---|---|---|---|---|---|
| 6 comunicaciones | `communication_id` | 3 campañas | `campaign_id` | muchos a uno | alta |
| 6 comunicaciones | `communication_id` | 1 canvas | `canvas_id` | muchos a uno | alta. La columna `channel` = "Canvas" dice cuál de las dos |
| 7 engagement canvas | `canvas_id` | 1 canvas | `canvas_id` | muchos a uno | alta |
| 7 engagement canvas | `canvas_step_id` | 2 pasos | `canvas_step_id` | muchos a uno | alta |
| 2 pasos | `canvas_id` | 1 canvas | `canvas_id` | muchos a uno | alta |
| 6 y 7 | `user_id` | 5 usuarios | `user_id` | muchos a uno | alta |
| 5 usuarios | `user_id` | 9 filtros | `customer_id` | uno a uno | **a confirmar**: mismo formato de id de 24 caracteres, parece el mismo |
| 4 dispositivos | `device_id` | ? | ? | | **sin llave**: ninguna tabla trae `device_id` |

Diagrama simple:

```
dim_braze_filters (9) ──customer_id = user_id── dim_braze_users (5)
                                                      │ user_id
                        ┌─────────────────────────────┤
                        │                             │
   users_and_communications (6)          fct_canvas_user_engagement (7 u 8)
        │ communication_id                      │ canvas_id, canvas_step_id
        ├── dim_braze_campaign (3)              ├── dim_braze_canvas (1)
        └── dim_braze_canvas (1)                └── dim_braze_canvas_step (2) ── canvas_id ── (1)
```

---

## 3. La convención de nombres es oro

Cada campaña y Canvas se llama así:

`Equipo-Producto-Fecha-Ticket-Canal-Audiencia-Oferta-Grupo`

Ejemplo: `Lending-KCash-20260501-B0301-CANVAS-Active-NuevosRetargeting_Installments_SP-Not Tracked`

Las tablas 1 y 3 ya traen cada pieza en su propia columna. Eso resuelve tres cosas del plan de golpe:

| Pregunta del plan | De dónde sale | Columna |
|---|---|---|
| Quién lo manda | Equipo | `team` (Lending, B2B, Marketing, Product Growth) |
| Qué ticket lo pidió | Número de ticket | `ticket_number` (B0301, T840). Prefijo B o T parece distinguir equipos o sistemas. A confirmar |
| A quién va | Audiencia | `audience` (Active, Nuevos, Recurrentes, Leads_LeftFunnel) |
| Qué ofrece | Oferta | `offer` (Tasa0, Recordatorio, Retargeting_Offering) |
| Por qué canal | Canal | `channel` (CANVAS, E). Falta confirmar el resto de códigos |

Códigos de canal que veo y que supongo:

| Código | Supongo | Confirmar |
|---|---|---|
| E | Email | sí |
| CANVAS | Flujo multi paso, el canal real está en cada paso | sí |
| PN | Push | a confirmar |
| WA | WhatsApp | a confirmar |
| IAM | In-app | a confirmar |
| B | Banner | a confirmar |
| WH | Webhook | a confirmar |

En la tabla 6 además hay `category` (email, push...) que ya dice el canal real de cada fila. Es la que usaremos para el canal.

---

## 4. Clasificación de tipo de comunicación

Aquí no hay mensajes transaccionales clásicos (recibos, OTP). Todo es marketing o ciclo de vida. Propongo clasificar por `audience` y `offer`:

| Tipo | Regla | Ejemplos |
|---|---|---|
| Adquisición | audiencia Leads, LeftFunnel, Registrados, Prospects | Leads_LeftFunnel, Nuevos_RegistradosPay |
| Onboarding | oferta u audiencia con Onboarding, Nuevos, SiCompra | Nuevos-Onboarding_SiCompra |
| Retargeting | oferta con Retargeting | NuevosRetargeting_Installments, Retargeting_Offering |
| Recurrencia y uso | audiencia Active, Recurrentes | Active, Recurrentes_Comercios |
| Operativo y cumplimiento | oferta Recordatorio con tema regulatorio | Recurrentes_ComerciosActualizarConstancia-Recordatorio |
| Promoción de tasa | oferta Tasa0 | Tasa0 |

El analista A registra la regla final y los casos ambiguos. Tú puedes corregir la tabla antes de arrancar.

---

## 5. Traducción de métricas

Grano base: en la tabla 6, una fila = usuario × comunicación × fecha. Un "envío" es una fila con `was_send = true`. Por canal se usan las banderas específicas.

### Volumen y embudo

| Métrica | Tabla | Columnas | En palabras | SQL |
|---|---|---|---|---|
| Envíos | 6 | `was_send` | Filas donde se envió algo | `SUM(CASE WHEN was_send THEN 1 ELSE 0 END)` |
| Envíos por canal | 6 | `email_sent`, `pn_send`, `whatsapp_send`, `in_app_impression`, `banner_impression` | Una bandera por canal. In-app y banner no se "envían", se muestran | `SUM(CASE WHEN email_sent THEN 1 END)` etc. |
| Entregados email | 6 | `email_delivery` | Emails que llegaron | `SUM(CASE WHEN email_delivery THEN 1 END)` |
| Tasa de entrega email | 6 | `email_delivery`, `email_sent` | Llegaron entre enviados | `delivered / sent` |
| Apertura email | 6 | `email_open`, `email_delivery` | Abrieron entre los que les llegó | `opens / delivered` |
| Clic email | 6 | `email_click`, `email_delivery` | Hicieron clic entre los que les llegó | `clicks / delivered` |
| CTOR email | 6 | `email_click`, `email_open` | Clic entre los que abrieron | `clicks / opens` |
| Baja email | 6 | `email_unsubscribe`, `email_delivery` | Se dieron de baja entre los que les llegó | `unsubs / delivered` |
| Apertura push | 6 | `pn_open`, `pn_send` | Abrieron entre enviados | `pn_open / pn_send` |
| Entrega WhatsApp | 6 | `whatsapp_delivery`, `whatsapp_send` | | `wa_delivery / wa_send` |
| Lectura WhatsApp | 6 | `whatsapp_read`, `whatsapp_delivery` | Leyeron entre entregados | `wa_read / wa_delivery` |
| Clic in-app | 6 | `in_app_click`, `in_app_impression` | Clic entre vistas | `click / impression` |
| Clic banner | 6 | `banner_click`, `banner_impression` | | `click / impression` |
| Apertura total | 6 | `was_opened`, `was_send` | Cualquier canal | `was_opened / was_send` |

Nota: `was_send` y `was_opened` parecen resumir las banderas por canal. Confirmar que `was_send = email_sent OR pn_send OR whatsapp_send OR in_app_impression OR banner_impression`.

### Eficiencia y conversión

| Métrica | Tabla | Columnas | En palabras | SQL |
|---|---|---|---|---|
| Tasa de solicitud | 6 | `applied_for_loan`, `was_send` | Pidieron préstamo entre los que recibieron | `applied / sent` |
| Tasa de conversión | 6 | `is_converted`, `was_send` | Se les otorgó entre los que recibieron | `converted / sent` |
| Monto por 1,000 envíos | 6 | `gross_amount`, `was_send` | Dinero colocado por cada mil mensajes | `SUM(gross_amount) / sent * 1000` |
| Ticket promedio | 6 | `gross_amount`, `is_converted` | Monto promedio por conversión | `SUM(gross_amount) / converted` |
| **Lift vs control** | 6 | `control_group`, `applied_for_loan` | Cuánto más convierte quien recibió el mensaje contra quien no lo recibió a propósito | `rate(test) - rate(control)` y `rate(test) / rate(control)` |
| Lift por paso de Canvas | 7 | `in_control_group`, `applied_for_loan`, `is_converted` | Lo mismo pero paso por paso | agrupar por `canvas_step_id, in_control_group` |
| Ganador A/B | 7 | `experiment_split_name`, `canvas_variation_name`, `is_converted` | Qué variante convierte más y si la diferencia es real | tasa por variante + test de proporciones |

**Esto es lo más valioso de tus datos.** Tienen grupo de control. Eso permite decir cuánto vende Braze de verdad (incremental), no solo cuánto se atribuye. Pocas empresas pueden.

Dudas sobre atribución:

- `applied_for_loan`, `is_converted` y `gross_amount` están en la fila del envío. ¿Con qué ventana se atribuyen? ¿7 días? ¿30? ¿Último mensaje?
- En la fila de ejemplo, `control_group = "Lead"`. Esperaba verdadero/falso. ¿Qué valores toma? ¿"Lead" es el nombre del grupo de control o del segmento?
- Si un usuario recibió 3 mensajes y convirtió una vez, ¿la conversión aparece en las 3 filas? Si sí, hay que deduplicar por usuario y periodo antes de sumar `gross_amount`.

### Frecuencia y vista por usuario

| Métrica | Tabla | Columnas | En palabras | SQL |
|---|---|---|---|---|
| Mensajes por usuario | 6 | `user_id`, `was_send` | Cuántos recibió cada quien en el periodo | `GROUP BY user_id` |
| Mensajes por usuario por semana | 6 | `event_date` | Lo anterior entre semanas del periodo | `/ semanas` |
| Por canal y por tipo | 6 + 3/1 | `category`, tipo derivado de `audience`/`offer` | | pivot |
| Comunicaciones distintas | 6 | `communication_id` | Cuántas campañas distintas tocaron al usuario | `COUNT(DISTINCT communication_id)` |
| Solapamiento | 6 | `user_id`, `event_date`, `communication_id` | Días con 3 o más comunicaciones al mismo usuario | `HAVING COUNT(DISTINCT communication_id) >= 3` |
| Fatiga | 6 | decil de mensajes, `email_unsubscribe` | Tasa de baja por decil de frecuencia | `NTILE(10)` |
| Usuarios sin contacto | 5 menos 6 | `user_id` | Usuarios en Braze que no recibieron nada | `LEFT JOIN ... WHERE 6.user_id IS NULL` |

### Suscripción y contactabilidad

| Métrica | Tabla | Columnas | En palabras | SQL |
|---|---|---|---|---|
| Estado actual email y push | 5 | `email_subscribe`, `push_subscribe` | Si hoy está suscrito | directo |
| Baja por canal | 9 | `email_unsubscribed`, `push_unsubscribed`, `wa_unsubscribed` | Si está dado de baja por canal | directo |
| Canal contactable | 9 | `mkt_contactable_channel` | Por qué canal se le puede hablar ("Only Email") | directo |
| No contactable por riesgo o ley | 9 | `is_blacklist`, `is_arco`, `charge_off_*`, `par_60_179`, `cc_freeze` | Gente a la que no debería llegarle marketing | banderas |
| Fecha de baja email | 6 | `email_unsubscribe`, `event_date` | El día que se dio de baja | `MIN(event_date) WHERE email_unsubscribe` |
| **Envíos a dados de baja** | 6 + 9 | `was_send`, `*_unsubscribed` | Mensajes que llegaron a quien pidió no recibir | join y contar. Debe ser cero |
| **Envíos a no contactables** | 6 + 9 | `was_send`, `is_arco`, `is_blacklist`, `charge_off_*` | Mensajes a gente excluida por riesgo o derechos ARCO | join y contar. Debe ser cero |
| Envíos después de la baja | 6 | `email_unsubscribe`, `email_sent`, `event_date` | Emails enviados después del día de baja | `event_date > fecha_baja` |

Límite: tablas 5 y 9 son una foto de hoy. Si alguien se dio de baja en agosto, no sabemos cómo estaba en julio. Lo marcamos como "estado al cierre".

### Inventario y gobernanza

| Métrica | Tabla | Columnas | En palabras | SQL |
|---|---|---|---|---|
| Campañas y Canvas totales | 3, 1 | `campaign_id`, `canvas_id` | Cuántos existen | `COUNT(*)` |
| Activos | 3, 1 | `archived`, `last_sent` | No archivados y con envío en últimos 90 días | `archived = false AND last_sent >= hoy - 90` |
| Zombis | 3, 1 | `archived`, `last_sent` | No archivados pero sin envío en 90 días | `archived = false AND last_sent < hoy - 90` |
| Vida de una campaña | 3, 1 | `first_sent`, `last_sent` | Cuántos días estuvo activa | `DATEDIFF` |
| Multicanal | 1, 3 | `channel_*` | Cuántos canales usa cada una | suma de banderas |
| Envíos por equipo | 6 | `team`, `was_send` | Quién manda cuánto | `GROUP BY team` |
| Concentración | 6 | `team` | % de envíos de los 3 equipos con más volumen | top 3 / total |
| Tickets por equipo | 3, 1 | `team`, `ticket_number` | Cuántas piezas pide cada equipo | `COUNT(DISTINCT ticket_number)` |
| Sin grupo o sin seguimiento | 1, 3 | `group` | Campañas con "Not Tracked" o "N/A" | contar |
| Duplicadas en intención | 1, 3 | `team`, `product`, `audience`, `offer` | Misma audiencia y oferta en más de una pieza activa | `GROUP BY ... HAVING COUNT(*) > 1` |

### Costo y gasto

Hoy no se puede calcular. Necesito:

| Dato | Para qué |
|---|---|
| Tarifa WhatsApp por mensaje (marketing y utility) | Gasto variable del canal más caro |
| Tarifa email por envío, si el proveedor cobra por volumen | Gasto variable email |
| Costo mensual del contrato Braze | Costo fijo a prorratear por envío o por usuario activo |
| Costo de otros proveedores (envío de WhatsApp, SMS si lo hubiera) | Gasto total |

Con esto: gasto por canal, por equipo, por campaña, costo por solicitud, costo por conversión, y gasto en campañas que no generan lift.

---

## 6. Lo que no se puede calcular con estas tablas

| Qué | Por qué | Qué haría falta |
|---|---|---|
| Rebotes y spam | No hay columnas | Tablas de bounce y markasspam de Currents |
| Historial de suscripción | Solo estado actual | `subscription_globalstatechange` o snapshot diario |
| Costo y gasto | No hay tarifas | Tarifas y contrato |
| Reenvíos el mismo día | Grano es por día | Nivel `dispatch_id` |
| Mix de dispositivos | Tabla 4 no tiene llave | Columna `device_id` en usuarios o en hechos |
| Hora de envío | Solo fecha | Timestamp del envío |
| Clic en WhatsApp | No hay columna | Evento `shortlinkclick` |

---

## 7. Preguntas para ti (con lo que asumo si no respondes)

| # | Pregunta | Si no respondes, asumo |
|---|---|---|
| 1 | ¿`user_id` de Braze es el mismo que `customer_id` del golden dataset? | Sí |
| 2 | ¿Usamos `xplore._fct...` o `braze_semantic_layer._fct...`? ¿Cuál es la oficial? | La capa semántica |
| 3 | ¿Qué valores toma `control_group` en la tabla 6? ¿Qué significa "Lead"? | Es el nombre del grupo de test y hay otro valor para control |
| 4 | ¿Con qué ventana se atribuye `applied_for_loan` e `is_converted` al mensaje? | 7 días, y lo marco como supuesto |
| 5 | Si un usuario recibe varios mensajes y convierte una vez, ¿la conversión se repite en cada fila? | Sí, y deduplico por usuario y día de conversión |
| 6 | ¿Qué significan los códigos de canal además de E y CANVAS? | PN push, WA WhatsApp, IAM in-app, B banner, WH webhook |
| 7 | ¿Los tickets B y T son de equipos o sistemas distintos? | B = Business, T = Tech o Marketing. Lo trato solo como identificador |
| 8 | ¿`gross_amount` es monto otorgado, monto solicitado o ingreso? | Monto otorgado del préstamo. Para ingreso hace falta tasa o margen |
| 9 | ¿Periodo a analizar? | Últimos 6 meses cerrados: 2026-04-01 a 2026-09-30 |
| 10 | ¿Tienen tarifas de WhatsApp, email y el costo de Braze? | No. La lente de costo queda como estimación con tarifas de lista de Meta y se marca así |

---

## 8. Ajustes al plan por lo que vi

- La lente **I Costo** depende de las tarifas. Sin ellas se entrega como estimación.
- La lente **F Salud de lista** se reduce a bajas y a envíos indebidos (dados de baja, ARCO, blacklist, cartera castigada). Eso último es un hallazgo de cumplimiento, no solo de eficiencia, y va al resumen ejecutivo si sale distinto de cero.
- Agrego a la lente **C Eficiencia** el análisis de **lift incremental contra grupo control** y de **experimentos A/B** por paso de Canvas. Es la métrica que un VP va a querer ver primero.
- Agrego a la lente **G Audiencias** el cruce con `step` (etapa del ciclo de vida) y `days_on_book` (antigüedad) para ver a quién le hablamos y a quién no.
- La tabla 4 de dispositivos queda fuera salvo que aparezca una llave.

Siguiente paso: respondes las 10 preguntas (o dices "asume todo") y escribo las vistas base en SQL y arrancan los analistas.

---

## 9. Decisiones tomadas (8 de octubre de 2026)

Con tus respuestas. Donde dijiste "no sé", aplico el default y agrego una query en `sql/verificaciones.sql` para que la data lo confirme antes de analizar.

| # | Decisión | Cómo se verifica con data |
|---|---|---|
| 1 | `user_id` = `customer_id` | % de usuarios de la tabla 6 que cruzan con la 9. Si es menor a 90 %, se revisa |
| 2 | Uso `braze_semantic_layer._fct_braze_canvas_user_engagement` | Comparo conteos y sumas de las dos tablas. Si son iguales, da igual. Si no, te aviso cuál difiere |
| 3 | `control_group`: la data dice qué valores hay | `SELECT DISTINCT control_group` con conteo y tasa de conversión por valor. El valor con conversión más baja y sin envíos es el control |
| 4 | Atribución: la que ya trae la tabla, sin recalcular. Se reporta como "según Braze" | Reviso si hay conversiones en filas sin envío (`was_send = false AND is_converted = true`) |
| 5 | La conversión puede repetirse en varias filas. Deduplico por usuario y día al sumar montos | Cuento usuarios con `is_converted` en más de una fila el mismo día |
| 6 | Códigos de canal: la data los lista | `SELECT DISTINCT channel, category` |
| 7 | `ticket_number` es solo identificador | Cruce prefijo (B, T) contra `team` para ver si hay patrón |
| 8 | `gross_amount` = monto otorgado. Sin tasa ni margen, no se convierte en ingreso. Se reporta como "monto colocado" | Reviso que `gross_amount` sea nulo cuando `is_converted = false` |
| 9 | Periodo: **2026-01-01 a 2026-09-30** (meses cerrados de este año). Octubre se muestra aparte como parcial | Filas por mes para ver cobertura |
| 10 | Tarifas en MXN: **email 0.05, WhatsApp 1.00, in-app 0, push 0, banner 0**. Costo fijo de Braze: pendiente | Nada que verificar. Si consigues el costo mensual de Braze, se prorratea |

Con estas decisiones el gasto variable se calcula así:

`costo_fila = email_sent × 0.05 + whatsapp_send × 1.00`

Push, in-app y banner cuestan cero variable. Si hay costo fijo de Braze, se prorratea por envío del mes.

---

## 10. Lo que aprendimos al correr las primeras queries (8 de octubre de 2026)

**El warehouse es Databricks con Unity Catalog.** Eso cambia dos cosas:

- Las vistas se crean como temporales dentro del notebook. Un `CREATE VIEW` sin catálogo intenta ir a Hive Metastore y Unity Catalog lo rechaza.
- Los archivos `sql/verificaciones.sql` y `sql/vistas_base.sql` ahora son notebooks de Databricks. Se importan con File > Import y cada query corre en su propia celda. Si se pegan como un solo archivo en el editor SQL, solo se ve el resultado de la última query.

**Hay muchas filas repetidas en la tabla principal.** La verificación V10 dio:

| Grupos repetidos | Filas de más |
|---|---|
| 1,972,276 | 3,557,092 |

Grano revisado: usuario × comunicación × día × canal. Un grupo repetido es una combinación que aparece más de una vez.

Qué puede significar y qué hacemos en cada caso:

| Si los duplicados... | Significa | Qué hacemos |
|---|---|---|
| Son copias exactas | Problema de carga de la tabla | Deduplicar con MAX. Lo que ya hace `v_envios`. Avisar al equipo de datos |
| Difieren solo en segment, subsegment o group | Atributos del usuario tomados en momentos distintos | Deduplicar con MAX. Es el mismo mensaje |
| Difieren en banderas (una fila con sent, otra con open) | Cada fila es un evento, no un envío | Deduplicar con MAX. Une los eventos del mismo envío |
| Difieren en communication_name o ticket | Varios pasos de un Canvas el mismo día | **No** colapsar: son mensajes distintos. Contar envíos desde la tabla 7 de pasos de Canvas |

Las queries V10b, V10c, V10d y V10e del notebook dicen cuál de los cuatro casos es. V13 dice el total de filas para dimensionar.

---

## 11. Resultados de la verificación con data real (8 de octubre de 2026)

Periodo verificado: 1 de enero a 30 de septiembre de 2026, tabla `xplore._dim_braze_users_and_communications`.

### Tamaño

| Qué | Valor |
|---|---|
| Filas | 729.3 millones |
| Usuarios distintos | 19.5 millones |
| Comunicaciones distintas | 3,439 |
| Filas con envío (`was_send`) | 670.4 millones (92 %) |
| Filas sin envío | 58.9 millones (8 %) |

### Decisión por duda

| # | Duda | Qué dijo la data | Decisión |
|---|---|---|---|
| 1 | `user_id` = `customer_id` | Solo 6.6 % de los 19.5 M usuarios cruzan con el golden dataset (1.29 M) | La llave sí funciona pero el golden dataset solo cubre clientes. Suscripción para todos sale de `_dim_braze_users`. Filtros de riesgo y ARCO solo para los 1.29 M. Probar también cruce por `braze_id` |
| 2 | Tabla oficial de Canvas | `xplore` y `semantic_layer` son idénticas: 1,508.9 M filas, mismos totales | Usar `braze_semantic_layer` |
| 3 | `control_group` en tabla 6 | Vale "Lead" en 99.9998 % de filas. "Control" solo 1,635 filas | **No sirve** como grupo control. El control real está en `in_control_group` de la tabla de Canvas: 709 K filas en control, 95.2 M en test, 555.6 M sin experimento |
| 3b | Conversión control vs test en Canvas | Control 6.66 %, test 2.09 %, sin experimento 0.70 % | El control convierte **más** que el test en el agregado. Eso no es "Braze destruye valor": es que los Canvas con experimento tienen audiencias distintas. El lift solo se mide **dentro de cada Canvas**, nunca en el total |
| 4 | Conversiones en filas sin envío | 58.9 M filas sin envío tienen 1.03 M conversiones (1.75 %). Las filas con envío: 0.65 % | Una fila es "usuario entró a la audiencia ese día". `was_send` dice si salió mensaje. Los no enviados convierten más: sesgo de selección, no sirven de control |
| 5 | Conversión repetida | Sí. 5.36 M filas convertidas son unos 3.5 M usuario-día. Hay usuarios con conversión en hasta 141 días distintos | **La conversión se repite en cada envío dentro de la ventana de atribución.** Sumar `is_converted` infla. Regla: conversión única = usuario × día. Pedir la tabla real de préstamos para atribución correcta |
| 6 | Códigos de canal | En tabla 6, `channel` es solo Canvas / Email / In-App / Others. El canal real es `category`: email, push notification, whatsapp, in-app, banner | Usar `category`. Ignorar `channel` de la tabla 6 |
| 6a | Convención de nombres | En los catálogos la columna `channel` trae cientos de valores basura (audiencias, números, tickets). Campañas: 615 con código válido, 237 "Not Tracked", unos 150 basura. Canvas: 4,470 válidos, 511 "Not Tracked", unos 200 basura | La convención se rompe en 15 a 20 % de las piezas. Es un hallazgo de gobernanza. Para el canal real usar `category` de la tabla 6, no el catálogo |
| 7 | Prefijo de ticket | B y T aparecen en todos los equipos. 748 piezas "Not Tracked" sin ticket. Columna `team` contaminada con QA, Test, "Copy of Marketing", nombres de personas | Normalizar `team`: todo lo que contenga QA, Test, Prueba, Check, Copy se marca "QA/Test". Hallazgo: piezas de prueba viven en producción |
| 8 | `gross_amount` | Solo existe cuando `is_converted`. Promedio 2,089 MXN, máximo 26,400. Conversión implica solicitud | Consistente. Es monto de préstamo otorgado |
| 9 | Cobertura | Todos los meses tienen data. Junio es anómalo: 17.4 M usuarios tocados contra 6 M normales | Junio hubo un envío masivo a toda la base. Analizarlo aparte |
| 10 | Duplicados | 1.97 M grupos, 3.56 M filas extra = **0.5 % de las filas**. Difieren solo en `is_converted` (680 K) y `gross_amount` (366 K). Ninguna otra columna cambia | Son el mismo envío con distinta conversión pegada. Deduplicar con MAX. Afecta conversiones, no envíos |

### Volumen por canal (envíos, enero a septiembre)

| Canal | Envíos | % | Costo variable estimado MXN |
|---|---|---|---|
| Email | 334.3 M | 49.9 % | 16.7 M (a 0.05) |
| Push | 251.9 M | 37.6 % | 0 |
| WhatsApp | 55.8 M | 8.3 % | 55.8 M (a 1.00) |
| In-app | 28.2 M | 4.2 % | 0 |
| Banner | 0.2 M | 0.03 % | 0 |
| **Total** | **670.4 M** | | **72.5 M** |

### Equipos reales (piezas en catálogo, limpiando pruebas)

Marketing ~2,100, Lending ~1,160, Not Tracked 748, ProductGrowth ~650, Sales ~415, B2B ~230, NewProducts ~120, Compliance ~96, CX ~90, Research ~40, Collections ~36, Security ~23, Acquisition ~15. Más unas 250 piezas de QA o prueba.

### Insights preliminares (antes de deduplicar, para orientar, no para presentar)

1. **WhatsApp es 8 % de los envíos y 77 % del costo variable.** Unos 55.8 M MXN en 9 meses. Es la primera palanca de ahorro.
2. **Presión alta:** unos 70 M envíos al mes sobre unos 6 M usuarios activos. Promedio 12 mensajes por usuario al mes, 3 por semana.
3. **Junio tuvo un blast a 17.4 M usuarios,** tres veces la base habitual. Hay que ver qué fue y qué dejó.
4. **La conversión reportada está inflada** por la repetición dentro de la ventana de atribución. Cualquier número de "conversiones de Braze" que circule hoy probablemente cuenta el mismo préstamo varias veces.
5. **El grupo control solo existe en 15 % de las filas de Canvas.** La mayoría de las campañas no tiene forma de probar incrementalidad.
6. **Gobernanza:** 748 piezas sin ticket, 15 a 20 % con nombre fuera de convención, y unas 250 piezas de prueba en producción.
7. **Solo 6.6 % de los usuarios de Braze son clientes** en el golden dataset. Braze le habla sobre todo a prospectos.

### Qué falta pedir

- Tabla real de préstamos originados (usuario, fecha, monto) para atribuir bien y medir lift.
- Costo fijo mensual de Braze.
- Confirmar si `braze_id` cruza mejor con el golden dataset.
