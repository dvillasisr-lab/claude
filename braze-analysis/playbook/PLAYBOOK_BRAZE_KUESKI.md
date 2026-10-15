# Playbook de Braze para Kueski

Versión 2. 15 de octubre de 2026. Reglas sacadas de nueve meses de envíos (enero a septiembre de 2026, 3,439 comunicaciones). Cada regla trae el dato que la sostiene. Los números completos están en el anexo y en el Sheets `braze_auditoria_v3`.

## Cómo usar este documento

- **Vas a crear algo nuevo:** ve a la sección 6 y sigue los 9 pasos. Antes de activar, pasa el checklist de la sección 7.
- **Quieres mejorar algo que ya existe:** busca la pieza en la pestaña Campañas del Sheets, lee su acción y aplica la sección 8.
- **Vas a poner orden en Braze:** secciones 1 (nombres), 2 (a quién no se le escribe) y 3 (cuántas veces). Se configuran una vez.

## Las 10 reglas en una página

1. **Una pieza se llama** `Ticket-Producto-Audiencia-Gancho`. Sin ticket no se activa.
2. **No se le escribe** a lista negra, REUS o ARCO, tarjeta KPay congelada, dados de baja, números de WhatsApp que fallaron 3 veces ni a quien no respondió nada en 90 días.
3. **Máximo 2 toques** de la misma pieza al mes. El segundo solo a quien no abrió el primero.
4. **Máximo 5 mensajes promocionales por semana** por usuario, 2 piezas al día y 1 push al día.
5. **Se manda por el canal al que el usuario responde.** Hoy 59 % de los mensajes van a un canal que el usuario nunca abrió.
6. **WhatsApp solo a quien ya dio señal** (abrió un push, un email o la app) o a clientes activos. Nunca a bases frías.
7. **Nada a toda la base.** Más de 1 millón de usuarios obliga a prueba al 10 % y a un segmento.
8. **Un recordatorio de algo que el usuario empezó** responde 5 a 10 veces más que una oferta nueva. Ese es el gancho principal.
9. **Referidos, lanzamientos y novedades van en in-app**, no por email. En in-app responden 43 a 55 %; por email 0.2 %.
10. **A las 4 semanas se revisa.** Si no llega al mínimo del canal, se apaga o se rehace. Sin discusión.

---

# 1. Cómo se nombra cada cosa

## 1.1 Piezas (campañas y Canvas)

Cuatro partes separadas por guion:

`Ticket-Producto-Audiencia-Gancho`

```
S0600-KPay-Recurrentes-BuenFin
L0301-KCash-Activos-Retargeting_Installments
C0012-KCash-BKT1-Cobranza
M0610-KCash-Leads_LeftFunnel-Retargeting_Veriff
```

| Parte | Qué va | Lista permitida |
|---|---|---|
| Ticket | Letra del equipo y número del ticket | M Marketing, L Lending (Product Growth), S Sales, C Collections, A Acquisition, P Producto y transaccional, K Compliance y legal |
| Producto | El producto del que habla la pieza | KCash, KPay, KPayB2B, BillPay, Installments, Ecosistema, Kueski (solo corporativo) |
| Audiencia | El segmento maestro (sección 1.3) | Anonimos, Leads, Registrados, Nuevos, Activos, Recurrentes, Inactivos, Dormants, Churn, Comercios, Todos. Cobranza: BKT1, BKT2, BKT3, Precobranza |
| Gancho | Qué le ofreces o le recuerdas | Tasa0, Descuento, Cupon, Cashback, Referidos, Retargeting, Recordatorio, Lanzamiento, Newsletter, CrossSell, Encuesta, Informativo, Cobranza, Transaccional, o el nombre del evento: HotSale, BuenFin, CuestaEnero, BackToSchool, DiaMadres |

Reglas:

- **Detalle con guion bajo.** Si necesitas precisar, una palabra después del guion bajo: `Leads_LeftFunnel`, `Retargeting_Veriff`, `BuenFin_Preventa`, `Cobranza_Dia5`.
- **Varias piezas del mismo ticket** se distinguen por el detalle. Si dos quedarían con el mismo nombre, o es la misma pieza (se queda una) o es una versión nueva.
- **Versión nueva:** sufijo `-v2`, `-v3`. Al activar la nueva se archiva la anterior el mismo día. Nunca dos versiones activas.
- **Campañas de un solo canal con el mismo contenido:** canal al final: `C0012-KCash-BKT1-Cobranza_Dia5-WA`. En un Canvas no hace falta, el canal va en el paso.
- **Pruebas:** prefijo `TEST-` y audiencia de prueba (`SEG-Interno-QA`). Se archivan a los 7 días. Nunca a un segmento real.
- **Prohibido:** espacios, acentos, "Copy of", "N/A", "Not Tracked", "Blast", nombres de personas, fechas en el nombre.
- Anota el nombre y el `communication_id` en el ticket.

Ejemplos de hoy y cómo quedarían:

| Hoy | Queda |
|---|---|
| `Marketing-KCash-20260501-B0391-CANVAS-Leads_BDDMarketing-RescateFinesDeSemana-N/A` | `M0391-KCash-Leads-Tasa0_FinDeSemana` |
| `Sales-KPay-20260518-B0493-CANVAS-Recurrentes-HotSaleKUESKIPROMOEnterprise-N/A` | `S0493-KPay-Recurrentes-HotSale` |
| `Copy of Lending-KPay-20260706-B0332 HardInactive` | `L0332-KPay-Inactivos-Descuento-v2` |
| `QA-KPay-20260811-B001 ReminderRegistroTelefono` | `TEST-A0001-KPay-Registrados-Recordatorio_Telefono` (o su nombre real si es producción) |
| `Collections-KCash-T000-CANVAS-BKT1-NA` | `C0012-KCash-BKT1-Cobranza` |

Nota para datos: el parser de Databricks que llena `team`, `product`, `audience`, `offer` y `ticket_number` hay que ajustarlo a este orden (ticket, producto, audiencia, gancho; `team` sale de la letra del ticket; `familia` = nombre sin `-vN` y sin canal). Las piezas viejas se siguen leyendo con el formato anterior.

## 1.2 Pasos de un Canvas

`NN-Canal-Proposito-Toque`

```
01-Email-Oferta-T1
02-Espera-48h
03-Decision-AbrioEmail
04-Push-Recordatorio-T2
05-Salida-SinRespuesta
```

- `NN` es el orden. Canal: Email, Push, WA, InApp, Espera, Decision, Salida.
- `T1`, `T2` es el toque. Máximo T2 en promocional.
- Antes de un paso de WhatsApp siempre hay un paso de Decision: solo pasa quien abrió algo antes.
- Cada paso de email lleva el filtro de suscripción (1.5). Hoy 80 mil emails llegaron a gente dada de baja porque el filtro estaba solo a la entrada.
- Todo Canvas termina en un paso de Salida con el motivo. Si no, el usuario sigue recibiendo pasos aunque ya haya convertido.
- El grupo de control (10 %) se configura dentro del Canvas o la campaña, no en el nombre.

## 1.3 Segmentos: pocos, con dueño

Hoy la audiencia se escribe de 731 formas distintas y dos equipos trabajan la misma base con ofertas distintas (Lending y Marketing sobre inactivos; Lending y Marketing con Tasa 0 al mismo usuario el mismo día).

Nombre: `SEG-Producto-Audiencia_Detalle`. Máximo 30 segmentos maestros en total.

| Familia | Segmentos | Dueño |
|---|---|---|
| Embudo de registro | `SEG-KCash-Anonimos`, `SEG-KCash-Leads_SinRegistro`, `SEG-KCash-Registrados_SinSolicitud`, `SEG-KCash-Registrados_FaltaVeriff`, `SEG-KPay-Registrados_FaltaVeriff` | Marketing (KCash), Acquisition (KPay) |
| Nuevos | `SEG-KCash-Nuevos_30d`, `SEG-KPay-Nuevos_30d` | Lending, Sales |
| Activos | `SEG-KCash-Activos`, `SEG-KCash-Recurrentes`, `SEG-KPay-Recurrentes_90d` | Lending, Sales |
| Fríos | `SEG-KCash-Inactivos_90a180d`, `SEG-KCash-Dormants_180a360d`, `SEG-KPay-Churn_12m`, `SEG-KCash-NeverActive` | Solo Lending. Marketing no crea segmentos fríos. |
| Cobranza | `SEG-KCash-BKT1`, `SEG-KCash-BKT2`, `SEG-KCash-BKT3`, `SEG-KCash-Precobranza` | Collections |
| Comercios | `SEG-KPayB2B-Comercios_Activos`, `SEG-KPayB2B-Comercios_Inactivos` | Sales |
| Exclusión | `EXC-Blacklist`, `EXC-REUS_ARCO`, `EXC-KPay_CCFreeze`, `EXC-BajaEmail`, `EXC-WA_SinEntrega3`, `EXC-SinRespuesta90d`, `EXC-Empleados` | MarTech (con Legal y Riesgo) |
| Interno | `SEG-Interno-QA` | MarTech |

Reglas:

- Las piezas usan el segmento maestro y afinan con un filtro adentro del Canvas ("y abrió un push en 60 días"). No se crea un segmento por campaña.
- Un segmento nuevo se pide en el ticket y lo aprueba el dueño de la familia.
- Cada trimestre se archivan los segmentos sin uso en 90 días.

## 1.4 Tags

Los tags no están en Databricks, así que no sabemos cómo se usan hoy. Regla para adelante: cuatro tags obligatorios por pieza, de lista cerrada, en minúsculas.

| Tag | Valores |
|---|---|
| `tipo:` | promocional, lifecycle, transaccional, cobranza, interno |
| `equipo:` | marketing, lending, sales, collections, acquisition, producto, compliance |
| `prod:` | kcash, kpay, billpay, ecosistema, kueski |
| `q:` | trimestre en que se activó: 2026q4, 2027q1 |

Opcional: `gancho:` con el mismo valor que el nombre, y `estado:revision` para lo que está en el Plan_accion. Nadie crea tags fuera de la lista.

## 1.5 Grupos de suscripción

| Grupo | Se puede dar de baja | Quién lo usa |
|---|---|---|
| KCash Promociones | Sí | Marketing, Lending |
| KPay Promociones y comercios | Sí | Sales, Marketing |
| Novedades Kueski | Sí | Producto, Marketing |
| Referidos | Sí | Marketing |
| Encuestas | Sí | CX |
| Avisos de cuenta y pagos | No | Producto |
| Cobranza | No | Collections |

Cada paso de email promocional filtra por su grupo. El pie del email ofrece la baja del grupo y la baja total.

## 1.6 Lo demás

- **Plantillas:** `TPL-Canal-Uso-vN` (`TPL-Email-Promo-v3`). Bloques compartidos para encabezado y pie legal. Nadie edita el pie dentro de una campaña.
- **Atributos de usuario que hacen falta:** `canal_preferido_90d` (último canal al que respondió), `ultima_respuesta`, `wa_fallos_seguidos`, `etapa_golden`, `producto_activo`, `fecha_alta`. En minúsculas con guion bajo.
- **Evento de conversión:** uno por pieza, ventana de 7 días. Lending: `solicitud_enviada`. KPay: `compra_kpay`. Embudo: el siguiente paso. Cobranza: `pago_recibido`.
- **UTMs:** `utm_source=braze`, `utm_medium=email|push|whatsapp|inapp`, `utm_campaign=<ticket>`, `utm_content=<paso>`.
- **Archivo:** sin envíos en 90 días se archiva. Una sola versión activa por pieza.
- **Permisos:** activar a un segmento real lo hace el dueño del segmento más MarTech. Más de 1 M de usuarios o "Todos": también CRM. Exclusiones: MarTech con Legal o Riesgo.

## 1.7 Limpieza que hay que hacer hoy

| Qué | Cuánto |
|---|---|
| Piezas activas duplicadas (mismo equipo, producto, audiencia y gancho) | 109 piezas en 13 combinaciones. Se queda una por combinación. |
| Piezas con 10 o más versiones | 15 familias. Se consolidan en una. |
| Pruebas y copias que mandan a usuarios reales | 171 comunicaciones, 7.26 M envíos. Se pausan hoy. La más grande: `QA-KPay-B001 ReminderRegistroTelefono`, 1.87 M push con 0.01 % de apertura. |
| Dos versiones del email de desembolso activas | 20240821 y 20251110 llegan juntas a 600 mil usuarios. Se apaga la de 2024. |
| Piezas sin ticket | 749. Others solo tiene ticket en 49 % de sus envíos. |
| Collections con ticket T000 en todo | Un ticket C por bucket. |

---

# 2. A quién no se le escribe

Siete exclusiones. Se ponen una vez como filtro negativo en todo lo promocional y lifecycle.

| Excluir a | Por qué | Cuánto se manda hoy |
|---|---|---|
| Lista negra | Riesgo | 146 mil envíos promocionales |
| REUS o ARCO | Pidieron no recibir publicidad. Queja potencial ante Condusef. | 249 mil promocionales (57 mil de Shopping, 47 mil de Lending Churn) |
| Tarjeta KPay congelada (para promociones de KPay) | No pueden pagar con KPay | 43.4 M promocionales |
| Dados de baja de email | Siguen recibiendo por el filtro mal puesto | 80 mil emails, 59 mil de Marketing |
| WhatsApp que falló 3 veces seguidas | El número no existe. Se paga y castiga la calidad del número de la empresa | 1 de cada 4 WhatsApp no se entrega: 14.2 M MXN en 9 meses |
| Sin respuesta en 90 días en ningún canal | 36 % de los mensajes, 0.37 % de conversión | 4.1 M usuarios |
| Empleados y cuentas de prueba | | |

Cobranza y transaccional solo excluyen lista negra. Legal decide si cobranza también excluye REUS y ARCO (hoy 61 mil envíos).

---

# 3. Cuántas veces

| Regla | Límite | Por qué |
|---|---|---|
| Misma pieza al mismo usuario en el mes | 2 toques. El segundo solo a quien no abrió | Con 2 toques el clic sube de 0.8 % a 1.8 %. Con 3 o 4 cae a 0.5 % |
| Promocionales por semana (todo junto) | 5 | Las bajas se disparan a partir del sexto mensaje |
| Piezas promocionales distintas al día | 2 | La baja se duplica cuando llegan 3 o más el mismo día |
| Push promocional al día | 1 | Marketing y Sales mandan dos push el mismo día a 1.5 M de usuarios |
| Separación entre promocionales | 24 horas | |
| WhatsApp promocional al mes | 1 | |
| Onboarding (retargeting de registro) | 1 email al día, máximo 3 la primera semana. El resto por push o in-app | Hoy manda 2 al día y causa 22 % de las bajas de usuarios nuevos |
| Usuario nuevo | Una sola secuencia de bienvenida. Nada más hasta que termine | 33 % se da de baja con el primer email. Antes de irse recibe 4 piezas distintas |
| Reactivación de quien no responde | 3 toques en 30 días, un canal, un gancho. Si no responde, fuera | 73 % de los usuarios no respondió nada en 9 meses |

Se configura con el frequency capping de Braze (global por tipo y canal) y con el tope del Canvas.

---

# 4. Por qué canal

## 4.1 Según a quién le escribes

| Audiencia | Canal | No usar | Dato |
|---|---|---|---|
| Nuevos (0 a 30 días) | Email de bienvenida, push, in-app | WhatsApp como primer toque | Responden más que nadie (clic 1.3 %, push 3.2 %) pero se dan de baja más (6.9 por mil). Cuida la frecuencia, no el mensaje |
| Leads y registrados sin crédito | Push, in-app. Email solo para recordar el paso que dejaron | Email masivo, WhatsApp | Email a prospectos: 0.27 % de clic en 167 M envíos. Es el 28 % de todo lo que se manda |
| Activos y recurrentes | Cualquiera. WhatsApp si la pieza vale más de 1 MXN por mensaje. In-app para novedades | | WhatsApp se entrega 82 % y se lee 70 % |
| Fríos (inactivos, dormants, churn) | Push barato primero. WhatsApp solo a quien reaccionó | WhatsApp masivo | Responden la mitad, un tercio de sus WhatsApp no llega y se llevan 23 M MXN del canal |
| Comercios | Email, WhatsApp | | |
| Cobranza | El del proceso | | No aplica frecuencia promocional |

## 4.2 Según qué le dices

| Gancho | Canal | Dato |
|---|---|---|
| Recordar algo que empezó (retargeting) | Email y push | Clic 3.1 % en email, 2.2 % en push. Lo único que funciona bien por email |
| Referidos | In-app, luego push a activos | In-app 43 %. Email 0.2 % |
| Lanzamiento, novedad, newsletter | In-app | In-app 55 %. Email 0.2 % y las bajas más altas (5.6 por mil) |
| Tasa 0 | Push a quien abrió un push en 60 días. WhatsApp solo detrás de esa señal | Email 0.5 %. Quien abre el push convierte 6 a 18 veces más, pero abre menos del 1 % |
| Descuento, cupón, evento (KPay) | Push y WhatsApp a recurrentes | Es lo que le funciona a Sales (78 % de lectura). Email 0.2 % |
| Encuesta, aviso legal | In-app. Email una vez | |
| Transaccional | El del proceso | Clic 2.7 %. No se toca |

Si el usuario ya tiene `canal_preferido_90d`, ese canal manda. Empate: in-app, push, email, WhatsApp, en ese orden (del más barato al más caro).

---

# 5. Qué funciona y qué no

Cada punto: dato, y la regla que sale de ahí. Los números completos están en el anexo.

## 5.1 En general

- **Funciona:** in-app (38 % de clic), WhatsApp cuando llega (69 % de lectura), recordar algo empezado, 2 toques, audiencias de 10 a 100 mil con un criterio.
- **No funciona:** email masivo a prospectos, push a bases frías (0.8 %), WhatsApp a bases frías, enviar a toda la base, 3 o más toques, dos equipos sobre la misma gente el mismo día.
- **Regla:** antes de agregar un mensaje, quita uno. El problema no es mandar mejor, es mandar menos y a quien sí.

## 5.2 Por equipo

**Marketing.** El que más manda (39 %), más gasta (47 %) y más bajas genera (4.95 por mil, el doble del estándar).

- Funciona: retargeting de Veriff (email 3.0 %, push 5.8 %), referidos a clientes KCash por push (2.4 %), in-app de registro de línea (87 %).
- No funciona: rescates por push a anónimos y leads (0.6 a 0.8 % en 22 M envíos), referidos por email a leads y dormants (0.1 a 0.2 % en 15 M emails), onboarding con 2 emails al día.
- Regla: referidos y lanzamientos salen del email y van a in-app. Rescates por push solo a quien abrió un push en 60 días. Onboarding a 1 email al día.

**Product Growth (Lending).** Donde está el ahorro más grande: 1.3 M MXN al mes.

- Funciona: retargeting de Installments a activos (email 2.8 %, push 11 %), descuento directo a inactivos (0.55 %), in-app (46 %).
- No funciona: Tasa 0 por email a registrados (B0211: 35 M emails, 0.28 % de clic, y ni quien abre convierte), NeverActive por email (13 M, 0.10 %), insistir 3 meses (pierde al usuario a los 92 a 128 días y 17 a 31 emails).
- Regla: Tasa 0 solo con señal y 2 toques al mes. B0211 y B0223 se apagan por email y se dejan en push acotado. Lending es el único dueño de las bases frías.

**Sales.** Peor email de todos (0.21 %) y mejor WhatsApp (80 % de entrega, 78 % de lectura).

- Funciona: push y WhatsApp a recurrentes de KPay (Quincenas sin intereses 4.2 %, Primavera 2.2 %, Comercio del día 1.1 a 1.8 %). Sus ventas a recurrentes sí sostienen la conversión a 90 días.
- No funciona: promociones de comercios por email a todo el portafolio (6.4 M, 0.22 %), el mismo evento por dos canales el mismo día, promoción a tarjetas congeladas (13 M envíos).
- Regla: Sales manda por push y WhatsApp a recurrentes, no por email. Un evento = una pieza por canal y calendario con Marketing.

**Collections.** No entra a las reglas promocionales. Precobranza es la pieza que mejor responde de toda la empresa (email 4.3 %, push 5.3 %): protegerla. Pendientes: un ticket por bucket, pausar los Canvas `PRUEBA_` que llegaron a 5 mil usuarios reales, y Legal decide sobre REUS y ARCO.

**Others (transaccional, BillPay, Shopping, Compliance).** Lo transaccional funciona (Payment Confirmation 3.8 %). Lo que no: BillPay Intro (16 M emails, 0.11 %, causó 31 % de las bajas de usuarios nuevos del año) y Shopping WeeklyRecommendations (7 M, 0.12 %, 57 mil a REUS). Regla: BillPay y Shopping entran a las reglas de todos. Lo transaccional se nombra con ticket.

## 5.3 Por canal

| Canal | Hoy | Mínimo para seguir | Funciona | No funciona |
|---|---|---|---|---|
| Email | 0.92 % de clic, 3.1 bajas por mil | 0.3 % de clic, 2.5 bajas por mil | Transaccional, retargeting, nuevos, 2 toques | Tasa 0, referidos, newsletters, bases frías, más de 1 M |
| Push | 1.5 % de apertura | 0.75 % | Cobranza, nuevos, retargeting, recurrentes | Leads, anónimos, fríos, lanzamientos |
| WhatsApp | 74 % de entrega, 69 % de lectura | 80 % de entrega, 60 % de lectura | Activos, recurrentes de KPay | Bases frías, repetir el mismo WhatsApp a los 2 a 6 días |
| In-app | 38 % de clic | 10 % | Casi todo: referidos, lanzamientos, retargeting, onboarding | Ofertas genéricas (14 %) |

- Email: no es el asunto (abren 24 %), es que no hay qué hacer adentro. Un solo llamado a la acción.
- Push: es el canal de señal. Primero push, y el resto solo a quien lo abrió. Septiembre tuvo el mejor push del año (2.1 %) con el menor volumen desde marzo: menos push, más apertura.
- WhatsApp: 8 % de los envíos y 77 % del costo. Nunca como primer toque.
- In-app: gratis y es el que más responde. Lo que sea informativo va ahí primero.

## 5.4 Por mes

- **Junio fue el peor mes:** 109 M envíos (el doble de enero), clic 0.67 %, push 1.05 %, 63 mil bajas. Fue el mes del email de BillPay a 16 M usuarios encima de Hot Sale. Más volumen no trajo más respuesta.
- **Enero:** el mejor clic (1.2 %) y las bajas más altas (69 mil). Muchas piezas nuevas sobre bases que no recibían en diciembre.
- **Marzo:** el más caro (12.2 M MXN) por 10 M de WhatsApp.
- **Abril y mayo:** la entrega de WhatsApp tocó piso (69 % y 67 %). Se siguió mandando. Se recuperó a 78 % cuando bajó el volumen.
- **Mayo, junio y agosto:** los meses donde más gente recibe 3 o más piezas el mismo día (Hot Sale, BillPay, regreso a clases).

Reglas de calendario:

- Un calendario único para los meses con evento (Hot Sale, regreso a clases, Buen Fin, Cuesta de enero): una pieza por equipo y canal.
- Ningún lanzamiento a toda la base en el mismo mes que un evento comercial.
- Si la entrega de WhatsApp baja de 75 % un mes, el siguiente no sube el volumen.
- El push de un mes no supera 1.3 veces el promedio de los tres anteriores sin aprobación de CRM.
- Día de la semana y hora: pendientes (ver anexo C).

## 5.5 Por producto

- **KCash:** 48 % de los envíos, 58 % del costo. Responde el doble que KPay. Su problema es la insistencia (Tasa 0 a registrados) y dos equipos sobre la misma base. Regla: un dueño por audiencia, una pieza de Tasa 0 por audiencia.
- **KPay:** casi el doble de piezas que KCash (985) para menos volumen: muchas piezas chicas y repetidas (Comercio del día por mes). Menor respuesta en email (0.44 %) y push (1.1 %). Regla: Comercio del día es una sola pieza con versiones, no una por mes. Canal: push y WhatsApp a recurrentes.
- **Ecosistema:** piezas a "Todos", bajas más altas (3.9 por mil), clic más bajo (0.37 %). Regla: nada a Todos sin pasar por in-app primero.
- **Installments:** responde bien (1.4 % de clic, 0.5 bajas por mil) con poco volumen. Regla: escalar con segmento.
- Una pieza no cubre dos productos. Se parte en dos.

## 5.6 Por tamaño y por toques

- 10 a 100 mil usuarios: clic 1.2 %. 100 mil a 1 M: 0.6 %. Más de 1 M: 0.16 %. Regla: el tamaño ideal es 10 a 100 mil con un criterio. Más de 1 M obliga a prueba al 10 %.
- 1 toque: 0.8 % de clic. 2 toques: 1.8 %. 3 a 4: 0.5 %. Regla: 2 toques y se acabó.

## 5.7 Usuarios nuevos

- 33 % se da de baja con el primer email. La mitad se va en el primer mes. Antes de irse recibieron 5 emails de 4 piezas distintas.
- Las causas: el email masivo de BillPay (31 % de las bajas de nuevos), el retargeting de registro de Marketing con 2 emails al día (22 %), los rescates de Tasa 0 (8.5 %).
- Regla: un nuevo entra a una sola secuencia de bienvenida. 1 email al día, 3 la primera semana. Si no abrió ninguno de sus primeros 5 emails, se pausa lo promocional por email. Ningún envío masivo incluye a usuarios con menos de 30 días.

## 5.8 Cómo saber si una pieza sirve: abren contra no abren

Por cada pieza se compara cuánto convierten los que abrieron contra los que no, a 7 días. Lo normal: quien abre convierte 2 a 3 veces más (email 8 % contra 4 %; push 20 % contra 7 %; WhatsApp 6 % contra 3 %).

- Si quienes abren convierten menos de la mitad de lo normal del canal: no hay a quién acotar. Se apaga.
- Si quienes abren convierten igual que quienes no (menos de 1.5 veces): el mensaje no cambia nada. Se rehace o se apaga.
- Si quienes abren convierten mucho más pero abren pocos: la pieza está bien, la base no. Se acota a quien abrió algo en 60 días.
- Para saber de verdad si el mensaje causa la conversión hace falta grupo de control (sección 6, paso 7).

---

# 6. Crear algo nuevo en 9 pasos

1. **Qué quieres que pase.** Un evento de conversión (sección 1.6) y el tipo: promocional, lifecycle, transaccional o cobranza. El tipo decide qué reglas aplican.
2. **A quién.** Un segmento maestro (1.3) más un filtro si hace falta. Nunca "Todos" sin filtro de respuesta en 90 días. Revisa en Catálogo que no exista ya una pieza viva con la misma audiencia y gancho: si existe, se mejora esa.
3. **Por qué canal.** Tablas 4.1 y 4.2. Si el usuario tiene canal preferido, ese.
4. **Cuántas veces.** Máximo 2 toques al mes, el segundo solo a quien no abrió. Revisa que la audiencia no esté ya en el tope semanal (sección 3).
5. **Cuándo.** Revisa el calendario único. No en la misma semana que un evento de otro equipo a la misma gente. No a toda la base en mayo, junio ni agosto.
6. **Cómo se llama.** Sección 1.1. Pasos con 1.2. Tags con 1.4. Grupo de suscripción en cada paso de email. UTMs con ticket.
7. **Cómo se prueba.** Grupo de control del 10 % (5 % si pasa de 1 M). Más de 1 M: primero al 10 % durante 48 horas y lees bajas por mil y respuesta contra el mínimo del canal. 100 mil a 1 M: al 5 %.
8. **Cómo se mide.** A las 4 semanas: respuesta contra el mínimo del canal (5.3), bajas por mil (menos de 2.5), abren contra no abren (5.8), lift contra el control. Aparece sola en el Sheets el mes siguiente.
9. **Cómo termina.** Fecha de revisión en el ticket. Si a las 4 semanas no cumple, se apaga o se rehace. Si cumple, revisión mensual. Sin envíos en 90 días, se archiva.

---

# 7. Checklist antes de activar

Lo firma el dueño del segmento y MarTech. Si falta una, no se activa.

1. Tipo declarado y tag `tipo:` puesto.
2. Ticket con letra de equipo. Nombre con las 4 partes y listas permitidas. Sin "Copy of", "TEST", "N/A", fechas.
3. Audiencia = segmento maestro. Si es "Todos" o más de 1 M: aprobación de CRM y prueba al 10 %.
4. Las 7 exclusiones como filtro negativo.
5. Filtro de suscripción en cada paso de email.
6. Canal según la sección 4. WhatsApp solo detrás de una señal y con `EXC-WA_SinEntrega3`.
7. Máximo 2 toques, el segundo con Decision "no abrió". Paso de Salida con motivo.
8. Dentro del tope semanal, diario y de push.
9. Grupo de control del 10 % y evento de conversión a 7 días.
10. Plantilla vigente, UTMs con ticket, un solo llamado a la acción.
11. Calendario revisado: nadie más le manda lo mismo a esa audiencia esa semana.
12. Fecha de revisión a 4 semanas en el ticket y versión anterior archivada.

---

# 8. Mejorar algo que ya existe

Busca la pieza en la pestaña Campañas del Sheets (una fila por pieza y canal). La columna acción dice qué hacer:

| Acción | Qué significa | Qué haces en Braze |
|---|---|---|
| Apagar | Mucho volumen, poca respuesta, y ni quien abre convierte | Archivar en ese canal. Si en otro canal sí funciona, dejar solo ese acotado a quien abrió en 60 días |
| Confirmar apagado | Debajo del mínimo y ya sin envíos | Confirmar que está archivada, no pausada |
| Bajar frecuencia | Responde, pero se da de baja arriba de 2.5 por mil o manda 3 o más toques | Tope de 2 toques con Decision "no abrió". Quitar pasos 3 en adelante. Filtro de suscripción en cada paso |
| Rehacer o re-segmentar | Poca respuesta pero quien abre sí convierte, o más de 1 M sin criterio | Cambiar al segmento maestro más filtro de señal. Cambiar el gancho si es Tasa 0 o novedades por email. Relanzar como v2 con control |
| Limpiar base de WhatsApp | Entrega debajo de 80 % | Aplicar `EXC-WA_SinEntrega3`. Pausar hasta que una prueba al 5 % pase de 80 % |
| Escalar | Buena respuesta con audiencia chica | Ampliar al siguiente segmento maestro de la misma familia, con control. No tocar el mensaje |
| Proteger | Mucho volumen y buena respuesta | No tocar. Vigilar bajas y toques. Es la referencia para rehacer las demás |
| Seguir igual | Cumple | Revisión mensual |
| No tocar | Transaccional o cobranza | Solo nombre, ticket y una versión activa |

Hoy hay 85 piezas activas debajo del mínimo. El ahorro por acción está en Plan_accion y por equipo en Vista_equipo.

---

# 9. Cada mes

| Semana | Qué | Quién |
|---|---|---|
| 1 | Actualizar las extracciones y generar el Sheets del mes como archivo nuevo | Datos |
| 1 | Leer Estándares: qué indicador se movió y qué equipo lo mueve | CRM |
| 2 | Ejecutar Plan_accion: Apagar, Confirmar apagado y Limpiar WhatsApp se hacen; Rehacer y Bajar frecuencia se asignan con ticket | Cada equipo con MarTech |
| 2 | Limpieza: piezas sin envío en 90 días, versiones duplicadas, pruebas activas, nombres fuera de regla | MarTech |
| 3 | Calendario del mes siguiente: una pieza por equipo, canal y audiencia | Marketing, Lending, Sales con CRM |
| 4 | Piezas nuevas pasan el checklist y se activan con control | Dueños y MarTech |
| Cada trimestre | Revisar segmentos, tags, grupos de suscripción, plantillas. Archivar lo sin uso. Actualizar este playbook | MarTech y CRM |

Gobierno:

- **Dueños.** Un dueño por familia de segmentos. Un dueño por pieza (el ticket). MarTech es dueño de nombres, tags, suscripciones, plantillas, exclusiones y frequency cap. CRM es dueño del calendario y de los estándares.
- **Calendario único.** Una vista compartida con fecha, equipo, pieza, audiencia, canal, gancho y tamaño. Nada promocional se activa sin estar ahí.
- **Comité quincenal de 30 minutos.** Conflictos de calendario, piezas a Todos, cambios a exclusiones, y piezas en Apagar que un equipo quiera defender (con grupo de control, no con opinión).
- **Excepciones** se piden en el ticket, se aprueban en el comité y tienen fecha de fin.
- Un indicador en rojo dos meses seguidos abre un ticket al equipo que lo mueve.

---

# 10. Glosario

- **Pieza:** una campaña o un Canvas.
- **Familia:** la pieza con todas sus versiones.
- **Respuesta:** clic en email, apertura en push, lectura en WhatsApp, clic en in-app. Abrir un email no cuenta.
- **Toque:** un mensaje de la misma pieza al mismo usuario en el mes.
- **Canal mudo:** canal al que el usuario nunca respondió aunque sí respondió a otro.
- **Base fría:** inactivos, dormants, churn, never active, rezagados.
- **Señal:** el usuario abrió un push, hizo clic en un email o in-app, o leyó un WhatsApp en los últimos 60 a 90 días.
- **Mínimo del canal:** respuesta debajo de la cual una pieza se apaga: email 0.3 %, push 0.75 %, WhatsApp 60 % de lectura, in-app 10 %.
- **Etapa bloqueada:** lista negra, REUS o ARCO, tarjeta KPay congelada.
- **Grupo de control:** el 10 % de la audiencia que no recibe el mensaje, para medir si el mensaje mueve algo.
- **Segmento maestro:** segmento `SEG-` con dueño, que usan todas las piezas de esa audiencia.

---

# Anexo A. Cifras de apoyo

## A1. Estándares de hoy (Estándares del Sheets)

| Indicador | Hoy | Estándar | Estado |
|---|---|---|---|
| Entrega de email | 95.1 % | 95 % | Cumple |
| Apertura de email | 23.6 % | 15 a 25 % | Cumple (no decidir con ella) |
| Clic de email | 0.92 % | 1.5 % | Debajo en los 4 equipos |
| Bajas de email por mil | 3.13 | 2.5 | Debajo |
| Apertura de push | 1.53 % | 3 % | Debajo |
| Entrega de WhatsApp | 74.2 % | 90 % | Debajo |
| Lectura de WhatsApp | 68.8 % | 70 % | Debajo por poco |
| Clic de in-app | 38.2 % | 5 a 20 % | Cumple |
| Toques por pieza y usuario al mes | 1.71 | 2 | Cumple (Collections 3.86) |
| Usuarios con 41 o más mensajes en el periodo | 5.3 % | | Debajo |
| Usuario-días con 3 o más piezas | 9.0 % | 10 % | Cumple, pero es 24 % de los mensajes |
| Mensajes a canal mudo | 58.9 % | | Debajo |
| Usuarios que nunca respondieron | 72.9 % | | Debajo |
| Promocional a etapas bloqueadas | 43.78 M | 0 | Debajo |
| Promocional a dados de baja | 79,994 | 0 | Debajo |
| Piezas activas debajo del mínimo | 85 | 0 | Debajo |
| Envíos con ticket | 87.4 % | 100 % | Debajo (Others 48.7 %) |

## A2. Por equipo

| Equipo | Familias | Envíos | % envíos | Costo MXN | % costo | Email clic | Bajas por mil | Push | WA entrega | WA lectura | In-app | Ahorro al mes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Marketing | 368 | 262.3 M | 39 % | 27.2 M | 47 % | 0.93 % | 4.95 | 1.09 % | 74 % | 71 % | 34 % | 160,647 |
| Product Growth | 184 | 177.2 M | 27 % | 17.3 M | 30 % | 0.45 % | 3.02 | 2.10 % | 72 % | 61 % | 46 % | 1,296,806 |
| Sales | 205 | 85.3 M | 13 % | 7.1 M | 12 % | 0.21 % | 3.71 | 1.23 % | 80 % | 78 % | 8 % | 102,271 |
| Collections | 23 | 44.7 M | 7 % | 1.6 M | 3 % | 1.09 % | 0.25 | 3.61 % | | | 13 % | 0 |
| Others | 283 | 98.0 M | 15 % | 4.4 M | 8 % | 1.83 % | 2.20 | 2.76 % | 71 % | 69 % | 80 % | 38,639 |

## A3. Por mes

| Mes | Envíos | Email clic | Bajas (usuarios) | Push apertura | WhatsApp enviados | WA entrega | WA lectura | In-app clic | Costo MXN |
|---|---|---|---|---|---|---|---|---|---|
| Ene | 58.7 M | 1.20 % | 69,226 | 1.83 % | 5.6 M | 80 % | 75 % | 48 % | 7.4 M |
| Feb | 67.5 M | 0.88 % | 57,965 | 1.43 % | 7.8 M | 77 % | 73 % | 19 % | 9.5 M |
| Mar | 67.8 M | 1.03 % | 50,413 | 1.81 % | 10.4 M | 74 % | 72 % | 24 % | 12.2 M |
| Abr | 64.3 M | 0.98 % | 38,422 | 1.53 % | 5.9 M | 69 % | 66 % | 36 % | 7.6 M |
| May | 85.0 M | 0.86 % | 38,034 | 1.28 % | 6.1 M | 67 % | 67 % | 47 % | 8.1 M |
| Jun | 109.0 M | 0.67 % | 63,425 | 1.05 % | 7.1 M | 74 % | 67 % | 45 % | 9.7 M |
| Jul | 71.7 M | 1.00 % | 52,912 | 1.77 % | 4.8 M | 73 % | 62 % | 37 % | 6.4 M |
| Ago | 78.0 M | 0.95 % | 50,340 | 1.57 % | 4.4 M | 78 % | 64 % | 42 % | 6.1 M |
| Sep | 65.6 M | 0.92 % | 36,639 | 2.12 % | 3.2 M | 77 % | 64 % | 42 % | 5.0 M |

## A4. Por audiencia y por gancho (según el nombre de la pieza)

| Audiencia | Email clic | Bajas por mil | Push | WA lectura | WA entrega | WA costo MXN |
|---|---|---|---|---|---|---|
| Nuevos y onboarding | 1.25 % | 6.9 | 3.18 % | 68 % | 77 % | 0.8 M |
| Activos y recurrentes | 0.72 % | 3.1 | 1.75 % | 70 % | 82 % | 14.9 M |
| Leads y registrados sin crédito | 0.75 % | 4.6 | 0.94 % | 73 % | 75 % | 15.1 M |
| Fríos | 0.35 % | 4.3 | 0.77 % | 65 % | 68 % | 23.0 M |

| Gancho | Email envíos | Email clic | Bajas por mil | Push | WA lectura | In-app clic |
|---|---|---|---|---|---|---|
| Retargeting o recordatorio | 23.6 M | 3.09 % | 3.8 | 2.16 % | 70 % | 58 % |
| Tasa 0 | 54.3 M | 0.53 % | 4.6 | 0.68 % | 69 % | 22 % |
| Descuento, cupón, oferta | 35.0 M | 0.41 % | 3.4 | 1.38 % | 58 % | 14 % |
| Cross sell | 2.7 M | 0.34 % | 2.0 | 1.69 % | 54 % | 25 % |
| Referidos | 40.8 M | 0.22 % | 4.3 | 1.15 % | 71 % | 43 % |
| Lanzamiento, novedades, newsletter | 33.0 M | 0.22 % | 5.6 | 0.82 % | 73 % | 55 % |

## A5. Por etapa del usuario (golden dataset, cubre 37 % de los envíos)

| Etapa | Envíos | Promocional | Email clic (promo) | Push (promo) | In-app (promo) |
|---|---|---|---|---|---|
| Prospectos | 189.1 M | 167.2 M | 0.27 % | 1.33 % | 27 % |
| Tarjeta KPay congelada | 56.6 M | 43.4 M | 0.38 % | 1.45 % | 33 % |
| REUS o ARCO | 0.49 M | 0.25 M | | | |
| Lista negra | 0.43 M | 0.15 M | | | |
| Sin etapa | 416.2 M | 356.3 M | 0.67 % | 1.20 % | 51 % |

## A6. A qué canal responde la gente (9 meses)

| Responde a | Usuarios | % usuarios | % mensajes | % costo | Mensajes por usuario | Convierten | Baja de email |
|---|---|---|---|---|---|---|---|
| Ninguno | 14.2 M | 73 % | 24 % | 14 % | 11 | 0.08 % | 1.4 % |
| Solo WhatsApp | 1.6 M | 8 % | 15 % | 34 % | 63 | 2.0 % | 3.4 % |
| Solo in-app | 1.1 M | 6 % | 7 % | 4 % | 43 | 8.8 % | 1.7 % |
| Solo email | 365 mil | 2 % | 2 % | 1 % | 33 | 5.0 % | 15.8 % |
| Varios canales | 2.2 M | 11 % | 52 % | 47 % | 120 a 262 | 30 a 75 % | 2 a 8 % |

Quien responde a varios canales convierte mucho más porque es cliente activo que usa la app. Sirve para segmentar, no para decir que el mensaje convirtió. Quien solo responde a WhatsApp es 8 % de los usuarios y 34 % del costo, y recibe 58 M emails y 21 M push que nunca abre.

## A7. Las piezas que más pesan hoy

| Pieza (nombre actual) | Canal | Envíos | Respuesta | Acción |
|---|---|---|---|---|
| Lending-KCash-B0211 Nuevos_RegistradosPay Tasa0 | email | 34.9 M | 0.28 % | Apagar |
| NewProducts T0000 Portfolio_BillPay_Intro | email | 16.1 M | 0.11 % | Confirmar apagado |
| Lending-KCash-B0223 Nuevos_NeverActive Installments | email | 13.5 M | 0.10 % | Apagar |
| Marketing-KCash-B0391 Leads RescateFinesDeSemana | push | 13.4 M | 0.76 % | Rehacer o re-segmentar |
| Marketing-KCash-B0000 Leads_LeftFunnel Retargeting_Veriff | email | 9.7 M | 3.04 % | Bajar frecuencia |
| Marketing-KCash-B0171 Anonimos RescateTasa0 | push | 8.9 M | 0.56 % | Apagar |
| Marketing-KCash-B0326 Leads ReferralProgram | email | 8.5 M | 0.23 % | Confirmar apagado |
| Marketing-KCash-B0326 Recurrentes_Dormants ReferralProgram | email | 7.0 M | 0.07 % | Apagar |
| Shopping-KPay-S0004 WeeklyRecommendations | email | 7.0 M | 0.12 % | Rehacer o re-segmentar |
| Sales-KPay-B0335 Recurrentes PromocionesMerchants | email | 6.4 M | 0.22 % | Rehacer o re-segmentar |

Las que hay que proteger: Precobranza (email 4.3 %, push 5.3 %), Retargeting Veriff (push 5.8 %), Retargeting Installments a activos (push 11 %), Payment Confirmation (3.8 %), registro de línea MX in-app (87 %), Quincenas sin intereses (push 4.2 %).

# Anexo B. Dónde está cada cosa en el Sheets

| Pestaña | Qué trae | Sirve para |
|---|---|---|
| Parámetros | Costos, mínimos y topes. Cambiarlos recalcula todo | Secciones 3 y 5 |
| Canales | Volumen, respuesta, costo y bajas por canal y mes | 5.3, 5.4 |
| Equipos | Lo mismo por equipo | 5.2 |
| Campañas | Una fila por pieza y canal con señal y acción | Sección 8 |
| Catálogo | Una fila por familia: ticket, audiencia, gancho, estado, versiones | 1.7, paso 2 de la sección 6 |
| Vista_equipo | Todo lo anterior para un equipo (celda B2) | Sección 9 |
| Insights | Hallazgos con cifra, filtrables | Sección 5 |
| Plan_accion | Ahorro por acción, las diez que más pesan, por equipo | Secciones 8 y 9 |
| Estándares | 24 indicadores con valor actual, estándar y estado por equipo | Anexo A1, sección 9 |

# Anexo C. Lo que todavía no sabemos

| Qué | Estado |
|---|---|
| Tags | No están en Databricks. Si alguien exporta la lista de campañas con tags desde Braze, se audita en una hora. |
| Día de la semana | Pendiente: query E10 (`e10_dia_semana.csv`). |
| Segmentos reales de Braze | Pendiente: query E11 (`e11_segmentacion.csv`). Hoy la audiencia se lee del nombre. |
| Antigüedad del usuario | Pendiente: query E12 (`e12_antiguedad.csv`). |
| Tipo de celular | No se puede: la tabla de dispositivos no cruza con la de envíos. |
| Hora del día | No se puede: la tabla solo trae fecha. |
| Región | No está en ninguna tabla. |

# Anexo D. Supuestos

- Periodo enero a septiembre de 2026. Respuesta = clic en email, apertura en push, lectura en WhatsApp, clic en in-app.
- Conversión a 7 días como referencia, no como atribución (no hay grupo de control hoy).
- Costos: email 0.05 MXN por enviado, WhatsApp 1.00 MXN por entregado, push e in-app 0. No incluye el costo fijo de Braze.
- Audiencia, gancho y tipo se leen del nombre de la pieza; el 17 % que no sigue la convención cae en "otros".
- Las etapas del golden dataset cubren 37 % de los envíos.
- Las bajas solo existen para email. Lectura de WhatsApp subestimada si el usuario apagó las confirmaciones.
