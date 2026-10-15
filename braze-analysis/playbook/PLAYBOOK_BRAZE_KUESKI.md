# Playbook de Braze para Kueski

Versión 1. 15 de octubre de 2026. Periodo analizado: enero a septiembre de 2026 (9 meses, 729 M filas de envío, 3,439 comunicaciones, 1,821 familias).

## Para qué sirve este documento

Dice, en concreto, cómo se usa Braze en Kueski: cómo se nombra cada cosa, qué segmentos existen, a quién no se le escribe, cuántas veces se puede escribir, por qué canal, con qué gancho, cuándo, cómo se mide y cuándo se apaga. Las reglas no salen de la industria: salen de comparar nuestras propias comunicaciones entre sí durante nueve meses. Cada regla trae la cifra que la justifica y la celda del Sheets `braze_auditoria_v3` donde se puede volver a ver.

Se usa de tres maneras:

- **Voy a crear algo nuevo.** Ir a la Parte D, sección D1 (guía paso a paso) y a la Parte C para la dimensión que aplique (equipo, canal, audiencia, gancho).
- **Quiero mejorar algo que ya existe.** Buscar la familia en la pestaña Campañas del Sheets, leer su acción, y aplicar la receta de D2.
- **Quiero poner orden.** Parte A (nomenclatura, segmentos, tags, grupos de suscripción, limpieza) y Parte B (reglas globales que se configuran una vez en Braze).

Convenciones del documento: respuesta = clic en email, apertura en push, lectura en WhatsApp, clic en in-app. Conversión solo como referencia (`is_converted` a 7 días), salvo en "convierten los que abren contra los que no abren". Costos con los parámetros default del Sheets: email 0.05 MXN por enviado, WhatsApp 1.00 MXN por entregado, push e in-app 0. "Familia" = comunicación sin la fecha del nombre. Todo es agregado, sin identificadores de usuario.

## Lo que este documento todavía no puede decir

| Dimensión pedida | Estado | Por qué y qué sigue |
|---|---|---|
| Tags de Braze | Sin dato | Los catálogos de Databricks (`_dim_braze_campaign`, `_dim_braze_canvas`) no traen tags. La regla de tags de A5 es de diseño, no de diagnóstico. Si alguien del equipo de Braze exporta la lista de campañas con tags (un CSV desde el admin), se audita en una hora. |
| Tipo de celular (iOS, Android) | Bloqueada | `_dim_braze_device` no tiene llave hacia la tabla de envíos. No se puede cruzar. |
| Hora del día | Bloqueada | La tabla de envíos solo trae fecha, no hora. |
| Región o estado | No disponible | Ninguna tabla trae geografía. |
| Día de la semana | Pendiente de correr | Query E10 en `sql/extraccion.sql` (archivo esperado `e10_dia_semana.csv`). |
| Segmentación real de Braze (segment, subsegment, group) | Pendiente de correr | Query E11 (`e11_segmentacion.csv`). Hoy la segmentación se lee por el nombre de la comunicación. |
| Antigüedad del usuario | Pendiente de correr | Query E12 (`e12_antiguedad.csv`); requiere confirmar la columna de fecha de alta en `_dim_braze_users`. |

Cuando lleguen E10, E11 y E12, se agregan las secciones C10 a C12 y se corrige lo que cambie.

---

# Parte A. Cómo está armado Braze hoy y cómo debe quedar

## A1. Diagnóstico de orden (lo que vimos en el catálogo)

Fuente: `data/e2_catalogo.csv` (6,144 piezas: 5,173 Canvas y 971 campañas; 5,958 archivadas y 186 activas) y la tabla de envíos.

| Problema | Cifra | Efecto |
|---|---|---|
| Piezas sin ticket en el nombre | 749 de 6,144 (12 %). En la operación activa: 87.4 % de los envíos sí traen ticket, pero Others solo 48.7 % (Estándares, fila 24) | No se sabe quién pidió qué ni para qué |
| Nombres fuera de convención | 1,053 (17.1 %) | La columna `team` del catálogo tiene 60 valores: "Maketing", "Copy of Copy of Marketing", nombres de personas, "CONFIGURACION" |
| Valores distintos de audiencia en el nombre | 731 | La misma audiencia se escribe de 10 formas ("Recurrentes", "Recurrentes_Todos", "Recurentes_...", "NuevosRecurrentes") |
| Valores distintos de oferta o gancho | 1,050 | "Tasa0", "Tasa0Blast", "RescateTasa0", "Tasa0BlastEnero" son el mismo gancho |
| Posición "grupo" sin uso | 1,604 piezas con "Not Tracked" | La posición pensada para control o variante se usa para cualquier cosa ("MultitestEmailBDDDaniMata", 73 piezas) |
| Piezas de prueba o copia | 657 con QA, Test, Prueba, Check o "Copy of" en el nombre; 171 enviaron en el periodo: 7.26 M envíos a 5.9 M usuarios reales | Un Canvas `QA-KPay-B001 ReminderRegistroTelefono` mandó 1.87 M push con 0.01 % de apertura |
| Versiones de la misma familia | Promedio 1.8 versiones por familia, máximo 17; 15 familias con 10 o más | Varias versiones activas a la vez se pisan (dos emails de desembolso, 20240821 y 20251110, llegaron juntos a 600 mil usuarios) |
| Duplicados activos | 109 piezas activas en 13 combinaciones iguales de equipo + producto + audiencia + oferta; 79 de ellas sin ningún dato en el nombre | Dos piezas vivas haciendo lo mismo, sin saber cuál manda |
| Control group | La columna `control_group` dice "Lead" en 99.99 % de las filas; `in_control_group` solo existe en 15 % de las filas de Canvas | Hoy no se puede medir lift con grupo de control |

Conclusión: la convención existe y es buena (`Equipo-Producto-Fecha-Ticket-Canal-Audiencia-Oferta-Grupo`), y las tablas de Databricks ya la parten en columnas. Lo que falta es cerrar los vocabularios de cada posición y que nadie lance sin cumplirla. No hay que inventar otra convención: hay que hacer cumplir la que hay.

## A2. Nomenclatura de campañas y Canvas

Se conserva el orden actual de 8 posiciones separadas por guion, porque los catálogos de Databricks lo leen así y cambiarlo rompería la medición. Cada posición pasa a tener una lista cerrada.

`Equipo-Producto-AAAAMMDD-Ticket-Tipo-Audiencia-Gancho-Grupo`

| Posición | Lista cerrada | Regla |
|---|---|---|
| 1. Equipo | Marketing, Lending, Sales, Collections, Acquisition, Producto, Compliance, CX | Un equipo por pieza. "Lending" es el nombre en Braze del equipo Product Growth. Nada de "Copy of", iniciales ni nombres de personas. B2B va como Sales con producto KPay_B2B. |
| 2. Producto | KCash, KPay, KPay_B2B, BillPay, Installments, Ecosistema, Kueski | "Kueski" solo para comunicación corporativa (aviso de privacidad, NPS). Nunca "Marketing", "Lending" ni "Multiproducto" como producto: si cubre dos productos, se parte en dos piezas o se usa Ecosistema. |
| 3. Fecha | AAAAMMDD de la versión | Es la fecha en que esta versión se activó. Al crear una versión nueva, la anterior se archiva el mismo día. Nunca dos versiones activas de la misma familia. |
| 4. Ticket | B#### (negocio), T#### (tecnología o producto), S#### (shopping), C#### (cobranza), L#### (legal o compliance) | Obligatorio. Sin ticket no se activa. "T000", "T0000" y "B0000" dejan de existir: cada iniciativa abre su ticket. Collections hoy usa T000 en todo; abre un C#### por flujo (BKT1, BKT2, BKT3, Precobranza). |
| 5. Tipo | CANVAS, CAMP_EMAIL, CAMP_PUSH, CAMP_WA, CAMP_INAPP, CAMP_BANNER | Una campaña es de un solo canal; el Canvas lleva el canal en cada paso (A3). Desaparecen "CANVA", "E", "IA", "Mail", "PushiOSAndroid". |
| 6. Audiencia | Anonimos, Leads, Registrados, Nuevos, Activos, Recurrentes, Inactivos, Dormants, Churn, Comercios, Todos, y para cobranza BKT1, BKT2, BKT3, Precobranza | Es el segmento maestro de A4. Un detalle se agrega con guion bajo y una sola palabra: `Leads_LeftFunnel`, `Recurrentes_KPay`. "Todos" obliga a prueba al 10 % (B6). |
| 7. Gancho | Tasa0, Descuento, Cupon, Cashback, Referidos, Retargeting, Recordatorio, Lanzamiento, Newsletter, CrossSell, Evento, Encuesta, Informativo, Cobranza, Transaccional | Un gancho por pieza. "Tasa0Blast", "RescateTasa0", "NarrativaTasa0" son Tasa0; el matiz va en el detalle con guion bajo: `Tasa0_Rescate`. Evento cubre HotSale, BuenFin, CuestaEnero, BackToSchool: `Evento_HotSale`. |
| 8. Grupo | Control, A, B, C, NA | Solo para pruebas. "NA" cuando no hay prueba. Prohibido "Not Tracked", "N/A" y cualquier texto libre. |

Ejemplos:

- `Lending-KCash-20261101-B0301-CANVAS-Activos-Retargeting_Installments-NA`
- `Sales-KPay-20261115-B0600-CAMP_PUSH-Recurrentes-Evento_BuenFin-A`
- `Collections-KCash-20261101-C0012-CANVAS-BKT1-Cobranza-NA`
- `Marketing-KCash-20261020-B0610-CANVAS-Leads_LeftFunnel-Retargeting_Veriff-Control`

Reglas adicionales:

- Sin espacios, sin acentos, sin "N/A". Guion solo entre posiciones; dentro de una posición, guion bajo.
- Pruebas: prefijo `TEST-` delante del nombre completo, audiencia de prueba (segmento `SEG-Interno-QA`) y archivo a los 7 días. Una pieza con `TEST-`, `QA`, `Prueba` o `Copy of` en el nombre nunca apunta a un segmento real. Hoy 7 piezas activas incumplen esto.
- "Copy of" se renombra antes de activar. Una copia que conserva el nombre no se activa.
- El nombre de la pieza en Braze y el `communication_id` se anotan en el ticket. Es lo que permite cruzar Databricks con la petición de negocio.

## A3. Pasos de Canvas

Cada paso se nombra `NN-Canal-Proposito-Toque`:

- `NN` = orden con dos dígitos (01, 02).
- Canal = Email, Push, WA, InApp, Banner, Espera, Decision, Salida.
- Propósito = una palabra: Bienvenida, Recordatorio, Oferta, Ultimo, Confirmacion.
- Toque = T1, T2 (número de toque al usuario dentro del Canvas). Permite contar toques desde `_dim_braze_canvas_step`.

Ejemplos: `01-Email-Oferta-T1`, `02-Espera-48h`, `03-Decision-AbrioEmail`, `04-Push-Recordatorio-T2`, `05-Salida-SinRespuesta`.

Reglas de estructura:

- Máximo 2 toques promocionales por Canvas por usuario al mes (B2). El segundo toque entra solo por la rama "no abrió" o "no hizo clic".
- Un paso de Decision antes de cualquier WhatsApp: solo pasa quien abrió o hizo clic en un paso previo de email, push o in-app (B5).
- Cada paso de email lleva el filtro de suscripción del grupo correspondiente (A6). Hoy 79,994 emails promocionales llegaron a usuarios ya dados de baja porque el filtro estaba solo a la entrada del Canvas (Estándares, fila 21).
- Todo Canvas promocional termina en un paso de Salida con el motivo (SinRespuesta, Convirtio, Baja). Sin salida, el usuario se queda dentro y recibe los pasos que faltan aunque ya haya convertido.

## A4. Segmentos: maestros, uno por audiencia, con dueño

Problema que resuelve: 731 formas de escribir la audiencia en el nombre y dos equipos trabajando la misma base con ofertas distintas (Lending B0209, B0333 y B0332 contra Marketing B0326 sobre inactivos y dormants; Lending B0211 y Marketing B0171 con Tasa 0 al mismo usuario, 120 mil coincidencias el mismo día).

Nomenclatura: `SEG-Producto-Audiencia-Condicion`. Ejemplos: `SEG-KCash-Nuevos-Sin1erCredito`, `SEG-KPay-Recurrentes-Compra90d`, `SEG-KCash-Inactivos-180a360d`.

Segmentos maestros (entre 20 y 30 en total, no más). Propuesta inicial:

| Familia | Segmentos | Definición base | Dueño |
|---|---|---|---|
| Embudo de registro | `SEG-KCash-Anonimos`, `SEG-KCash-Leads-SinRegistro`, `SEG-KCash-Registrados-SinSolicitud`, `SEG-KCash-Registrados-FaltaVeriff`, `SEG-KPay-Prospect-FaltaVeriff` | Paso del embudo en que se quedó, con fecha del último paso | Acquisition (KPay), Marketing (KCash) |
| Nuevos | `SEG-KCash-Nuevos-0a30d`, `SEG-KPay-Nuevos-0a30d` | Primer crédito o primera compra en los últimos 30 días | Lending (KCash), Sales (KPay) |
| Activos y recurrentes | `SEG-KCash-Activos`, `SEG-KCash-Recurrentes-2masCreditos`, `SEG-KPay-Recurrentes-Compra90d` | Con producto vivo o uso en 90 días | Lending, Sales |
| Fríos | `SEG-KCash-Inactivos-90a180d`, `SEG-KCash-Dormants-180a360d`, `SEG-KPay-Churn-12m`, `SEG-KCash-NeverActive` | Sin uso en la ventana; NeverActive = aprobado sin disponer | Un solo dueño para toda la familia: Lending. Marketing no crea segmentos fríos propios. |
| Cobranza | `SEG-KCash-BKT1`, `SEG-KCash-BKT2`, `SEG-KCash-BKT3`, `SEG-KCash-Precobranza` | Días de atraso | Collections |
| Comercios | `SEG-KPayB2B-Comercios-Activos`, `SEG-KPayB2B-Comercios-Inactivos` | | Sales |
| Exclusión (se aplican a todo lo promocional) | `EXC-Global-Blacklist`, `EXC-Global-REUS_ARCO`, `EXC-KPay-CCFreeze`, `EXC-Global-BajaEmail`, `EXC-WA-SinEntrega3`, `EXC-Global-SinRespuesta90d`, `EXC-Interno-Empleados` | Ver B1 | CRM o MarTech, con Legal para REUS y ARCO |
| Interno | `SEG-Interno-QA` | Cuentas de prueba del equipo | MarTech |

Reglas:

- Los segmentos maestros los crea y mantiene un solo dueño por familia. Las campañas usan el maestro y afinan con filtros dentro del Canvas (por ejemplo "y abrió un push en 60 días"); no crean un segmento nuevo para cada campaña.
- Un segmento nuevo se justifica solo si ningún maestro más un filtro lo cubre. Se pide en el ticket y lo aprueba el dueño de la familia.
- Revisión trimestral: se archivan los segmentos sin uso en 90 días. Los segmentos con nombre fuera de `SEG-` o `EXC-` se renombran o se archivan.
- Los atributos que alimentan las etapas (`etapa_golden`, `dias_sin_uso`, `producto_activo`) vienen del golden dataset vía la sincronización a Braze (A7); el segmento no recalcula la lógica.

## A5. Tags: lista cerrada y obligatoria

Los tags no están en Databricks, así que no se pudo auditar cómo se usan hoy. La regla es de diseño y se audita con una exportación del admin de Braze.

Cuatro dimensiones, un tag de cada una, máximo 6 tags por pieza:

| Dimensión | Valores |
|---|---|
| Tipo | `tipo:promocional`, `tipo:lifecycle`, `tipo:transaccional`, `tipo:cobranza`, `tipo:interno` |
| Equipo | `equipo:marketing`, `equipo:lending`, `equipo:sales`, `equipo:collections`, `equipo:acquisition`, `equipo:producto`, `equipo:compliance` |
| Producto | `prod:kcash`, `prod:kpay`, `prod:billpay`, `prod:ecosistema`, `prod:kueski` |
| Trimestre de activación | `q:2026Q4`, `q:2027Q1` |
| Opcionales | `gancho:tasa0`, `gancho:referidos`, ... (mismos valores que la posición 7 del nombre); `estado:pausada_revision` para lo que está en revisión del Plan_accion |

Reglas: minúsculas, prefijo con dos puntos, sin espacios. Nadie crea tags nuevos fuera de la lista; la lista la cambia MarTech una vez al trimestre. Los tags sirven para filtrar en el admin de Braze y en los reportes del admin; la medición de Databricks sigue saliendo del nombre.

## A6. Grupos de suscripción

Un grupo por producto y tema, para que la baja sea granular y para poder filtrar por paso:

| Grupo | Tipo | Quién lo usa |
|---|---|---|
| `KCash Promociones` | Opcional | Marketing, Lending |
| `KPay Promociones y comercios` | Opcional | Sales, Marketing KPay |
| `Novedades Kueski y lanzamientos` | Opcional | Producto, Marketing |
| `Programa de referidos` | Opcional | Marketing |
| `Encuestas` | Opcional | CX, Research |
| `Avisos de cuenta y pagos` | No opcional (transaccional) | Producto, Transaccional |
| `Cobranza` | No opcional | Collections |

Reglas: todo paso de email promocional filtra por "suscrito u opt-in" en su grupo, en el paso y no solo a la entrada del Canvas. El pie de página promocional ofrece la baja del grupo y, aparte, la baja global. Transaccional y cobranza no salen por baja de marketing (es correcto: 94 % de los emails a dados de baja son de estos dos tipos y son legítimos).

## A7. Atributos y eventos personalizados: diccionario

Nombres en minúsculas con guion bajo. Prefijo del dueño: `k_` para los que vienen del golden dataset o del backend, `brz_` para los que calcula Braze.

Atributos que este análisis necesita y que hoy no existen o no se usan:

| Atributo | Fuente | Para qué |
|---|---|---|
| `brz_canal_preferido_90d` | Braze (último canal con clic, toque o lectura en 90 días) | Regla B3: mandar por el canal que sí responde. 59 % de los mensajes del periodo fueron a un canal al que el usuario nunca respondió. |
| `brz_ultima_respuesta_fecha` | Braze | Salida de lo promocional a los 90 días sin respuesta (B4) |
| `brz_wa_fallos_consecutivos` | Braze (webhook de entrega) | `EXC-WA-SinEntrega3`: 25.8 % de los WhatsApp no se entregan (14.2 M MXN en 9 meses) |
| `k_etapa_golden` | golden dataset (`dim_braze_filters.step`) | Exclusiones Blacklist, REUS/ARCO, CC Freeze (B1) |
| `k_producto_activo` | golden dataset | No ofrecer KPay a quien tiene la tarjeta congelada; no ofrecer Tasa 0 a quien ya tiene crédito vivo |
| `k_dias_sin_uso` | golden dataset | Segmentos fríos de A4 |
| `k_fecha_alta` | golden dataset | Antigüedad (E12) y secuencia única de bienvenida (C8) |

Eventos de conversión estándar (A9) y eventos de embudo (`registro_completado`, `veriff_completado`, `solicitud_enviada`, `credito_dispuesto`, `compra_kpay`) con el mismo nombre en todas las piezas.

## A8. Plantillas y bloques de contenido

`TPL-Canal-Uso-vN`: `TPL-Email-Promo-v3`, `TPL-Email-Transaccional-v2`, `TPL-Push-Oferta-v1`, `TPL-WA-Recordatorio-v1`. Bloques de contenido compartidos para encabezado, pie legal y pie de baja (`BLK-Email-PieLegal-v2`). Una versión nueva de plantilla archiva la anterior; nadie edita el HTML del pie dentro de una campaña.

## A9. Evento de conversión estándar y ventana

Cada pieza declara en Braze un evento de conversión primario según su objetivo, con ventana de 7 días:

| Objetivo | Evento primario | Ventana |
|---|---|---|
| Lending KCash | `solicitud_enviada` (equivale a `applied_for_loan`) | 7 días |
| Disposición | `credito_dispuesto` | 7 días |
| KPay compra | `compra_kpay` | 7 días |
| Embudo de registro | el siguiente paso del embudo (`veriff_completado`, etc.) | 3 días |
| Cobranza | `pago_recibido` | 7 días |

Los 7 días son la ventana que ya usa el equipo para "convierten los que abren contra los que no abren" y la que mide si la pieza mueve a corto plazo. A 90 días la ventaja de quienes abren cae a la mitad (email de 2.3 a 1.6 veces; push de 3.0 a 1.9; WhatsApp de 2.1 a 1.5): sirve para saber si la pieza cambió el resultado o solo lo adelantó.

## A10. UTMs y enlaces

Todo enlace saliente lleva: `utm_source=braze`, `utm_medium=email|push|whatsapp|inapp`, `utm_campaign=<ticket>`, `utm_content=<posición del paso, ej. 01-email-oferta-t1>`. Con el ticket en `utm_campaign` la analítica web cruza con Databricks sin leer nombres.

## A11. Archivo, versiones e higiene

- Una pieza sin envío en 90 días se archiva. Hoy hay 186 activas y 5,958 archivadas: la proporción está bien, el problema son las activas que duplican.
- Una familia tiene una sola versión activa. Al activar la nueva, se archiva la anterior el mismo día. Las 15 familias con 10 o más versiones se consolidan en una.
- Las 109 piezas activas en 13 combinaciones duplicadas (A1) se revisan una por una: se queda una, se archivan las demás. Las 79 sin ningún dato en el nombre se renombran o se archivan.
- `TEST-`, `QA`, `Prueba`, `Copy of` con envíos reales: se pausan hoy y se revisan (171 comunicaciones, 7.26 M envíos en el periodo). La más grande, `QA-KPay-B001 ReminderRegistroTelefono` (1.87 M push, 0.01 % de apertura), o se renombra como producción o se apaga.
- Las dos versiones del email de desembolso (`KCash-Loan-Application-disbursed` 20240821 y 20251110) coinciden el mismo día en 600 mil usuarios: se apaga la de 2024.
- Revisión mensual de higiene en el ciclo de D4, con la pestaña Catálogo del Sheets como lista.

## A12. Permisos y aprobación

- Crear y editar: cualquier persona del equipo dueño.
- Activar una pieza a un segmento real: solo el dueño del segmento maestro (A4) más una persona de MarTech, que revisa el checklist de D3.
- Crear segmentos maestros, tags, grupos de suscripción y plantillas: solo MarTech.
- Envíos a `Todos` o a más de 1 M de usuarios: además, aprobación del responsable de CRM y prueba previa al 10 % (B6).
- Cambiar una exclusión global: MarTech con Legal (REUS y ARCO) o con Riesgo (Blacklist, CC Freeze).

---

# Parte B. Reglas de envío que se configuran una vez

Son reglas globales en Braze (segmentos de exclusión, frequency capping, filtros por paso). Cambian la operación sin tocar cada campaña.

## B1. Exclusiones globales para todo lo promocional y lifecycle

| Exclusión | Cifra hoy | Celda del Sheets |
|---|---|---|
| Blacklist (`k_etapa_golden` = 3) | 426 mil envíos, 146 mil promocionales a 69 mil usuarios | Estándares, fila 19 |
| REUS o ARCO (etapa 6) | 490 mil envíos, 249 mil promocionales a 104 mil usuarios. Un WhatsApp promocional a alguien en REUS es una queja potencial ante Condusef | Estándares, fila 19 |
| Tarjeta KPay congelada (etapa 4), para promociones de KPay | 56.6 M envíos, 43.4 M promocionales. Son promociones de KPay a quien no puede pagar con KPay | Estándares, fila 19 |
| Total promocional a etapas bloqueadas | 43.78 M envíos (Marketing 16.5 M, Sales 13.0 M, Product Growth 11.4 M, Others 2.8 M). En WhatsApp, 3.8 M MXN del periodo | Estándares, fila 19 y columnas por equipo |
| Dados de baja de email que siguen recibiendo promocional | 79,994 emails en 33 familias (Marketing 58,988) | Estándares, fila 21 |
| WhatsApp sin entrega en los últimos 3 envíos | Entre quienes nunca responden solo se entrega 34 % de sus WhatsApp; en total 25.8 % sin entrega, 14.2 M MXN pagados por mensajes que no llegaron | Canales, WhatsApp |
| Sin respuesta en 90 días en ningún canal (después de la reactivación de B4) | 4.10 M usuarios (58 % de los que recibieron algo en el trimestre), 36 % de los mensajes, 0.37 % de conversión | Insights, "nunca respondieron" |

Regla: los siete segmentos `EXC-` se agregan como filtro negativo en la entrada de todo Canvas promocional y lifecycle, y además en cada paso de email (suscripción) y de WhatsApp (entrega). Cobranza y transaccional solo aplican Blacklist según indique Legal (hoy 61 mil envíos de cobranza a REUS y ARCO pendientes de revisar con Legal).

## B2. Frecuencia

| Regla | Valor | Cifra que la sostiene |
|---|---|---|
| Toques de la misma comunicación al usuario en el mes (promocional) | Máximo 2; el segundo solo a quien no abrió el primero | Con 2 toques el clic de email sube de 0.76 % a 1.76 % y el push de 1.18 % a 2.52 %; con 3 a 4 el clic cae a 0.48 % (Insights, toques) |
| Mensajes promocionales por usuario por semana (todas las comunicaciones, todos los canales) | Máximo 5 | METRICAS.md; el salto de bajas está entre 5 y 6 mensajes en 9 meses (de 1.3 a 9.7 eventos de baja por 100 usuarios). Hoy 5.3 % de los usuarios recibe 41 o más mensajes en el periodo, debajo del estándar (Estándares, fila 11) |
| Familias promocionales distintas por usuario al día | Máximo 2 | La baja por usuario-día sube de 0.36 a 0.70 por mil entre 1 y 8 o más campañas en el día; 9 % de los usuario-días con 3 o más campañas concentra 24 % de los mensajes (Estándares, fila 12) |
| Push promocional por usuario al día | Máximo 1 | Los pares que más se pisan son push + push de Marketing y Sales el mismo día (1.54 M, 1.45 M, 1.23 M usuarios) |
| Separación entre dos promocionales al mismo usuario | 24 horas | Mismo dato |
| Onboarding (retargeting de registro: Veriff, PersonalInfo, NIP) | 1 email al día, máximo 3 en la primera semana; el resto por push o in-app | Hoy manda hasta 2 al día y explica 22 % de las bajas de usuarios nuevos, con mediana de 3 a 4 días hasta la baja |
| Email a usuario nuevo | Una sola secuencia de bienvenida; nada más entra hasta que termina | 33 % de los nuevos se da de baja con el primer email; antes de irse recibieron 4.2 familias distintas |

Cómo se configura: frequency capping global en Braze por tipo (promocional) y canal; los límites por comunicación con el paso de Decision y el tope del Canvas; el onboarding con el tope del Canvas de bienvenida.

## B3. Canal por usuario: el que responde

- Atributo `brz_canal_preferido_90d` (A7). Lo promocional se manda por ese canal y no por los demás. Si el usuario respondió a dos, se usa el más barato (in-app, push, email, WhatsApp en ese orden).
- Cifra: 394 M mensajes (59 %) fueron a un canal al que el usuario nunca respondió, 18.7 M MXN. Quitando a quienes no responden a nada, 235 M mensajes y 10.7 M MXN a canales mudos de gente que sí responde por otro lado. Con ventana de 90 días son 75 M mensajes y 3.1 M MXN por trimestre (Estándares, fila 14; Insights, canal mudo).
- 149 M emails fueron a 3.9 M usuarios que responden a otro canal pero nunca hicieron clic en un email (7.5 M MXN). 3.2 M WhatsApp entregados (3.2 M MXN) a quien nunca leyó uno. 80 M push a quien nunca abrió uno.
- Excepción: transaccional y cobranza van por el canal que define el proceso, no por el preferido.

## B4. Reactivación y salida

- Quien no respondió a nada en 90 días entra a una sola secuencia de reactivación: 3 toques en 30 días, un solo canal (el más barato contactable), un solo gancho (lo que dejó a medias). Si no responde, pasa a `EXC-Global-SinRespuesta90d` y sale de todo lo promocional hasta que vuelva a dar señal (abre la app, abre un email, un push).
- Regla de los 5 emails para nuevos: si un usuario nuevo no abrió ninguno de sus primeros 5 emails, se pausa lo promocional por email (la mediana de emails antes de la baja es 5).
- Cifra: 14.2 M usuarios (73 %) no respondieron a nada en 9 meses y se llevaron 24 % de los mensajes y 14 % del costo con 0.08 % de conversión (Insights).

## B5. WhatsApp

- Solo a `SEG` de activos, recurrentes o nuevos, o a quien reaccionó a un paso previo de push, email o in-app. Nunca WhatsApp masivo a bases frías: las bases frías se llevan 23 M MXN (un tercio del gasto del canal) con 68.5 % de entrega y 1.1 conversiones de referencia por mil contra 17 en activos.
- Exclusión `EXC-WA-SinEntrega3`. Meta cobra el entregado, pero un número que falla tres veces no existe y además castiga la calidad del número de la empresa.
- Mínimo de entrega para que una pieza siga: 80 %. Hoy la operación está en 74.2 % (Estándares, fila 7). Marketing 74.2 %, Product Growth 71.9 %, Others 71.4 %, Sales 79.9 %.
- Un WhatsApp al mes por usuario como tope promocional.

## B6. Tamaño y pruebas

- Envío a más de 1 M de usuarios: prueba previa al 10 %, criterio de segmento (etapa, última acción o canal donde respondió) y aprobación de CRM. Un envío a más de 1 M responde 7 veces menos por email (0.16 % contra 1.15 % en 10 a 100 mil) y genera más bajas (2.5 contra 2.0 por mil).
- Envío a `Todos`: prohibido sin filtro de respuesta en 90 días. El email de BillPay de junio (16.1 M usuarios, 0.8 M MXN) abrió 7.7 %, hizo clic 0.10 % y se llevó 58 mil usuarios en un día, el 31 % de las bajas de usuarios nuevos del año.
- Entre 100 mil y 1 M: prueba al 5 % con lectura de bajas por mil a las 48 horas contra el promedio del canal (3.13 por mil hoy).

## B7. Grupo de control

- Toda pieza promocional nueva reserva un grupo de control del 10 % (5 % si la audiencia pasa de 1 M) en la posición 8 del nombre y en la configuración de Canvas. Es la única forma de separar "el mensaje mueve" de "quien abre ya iba a convertir". Hoy la columna de control group no sirve (A1).
- Se lee a 7 y a 90 días con el evento de A9.

## B8. Cuándo se apaga o se rehace una pieza

Revisión a las 4 semanas de activada y después cada mes (D4):

| Señal | Umbral | Acción |
|---|---|---|
| Respuesta debajo del mínimo del canal | Email clic 0.3 %, push apertura 0.75 %, WhatsApp lectura 60 %, in-app clic 10 % | Apagar o rehacer |
| Bajas de email | Más de 2.5 por mil entregados | Bajar frecuencia o re-segmentar; si repite al mes, apagar |
| Convierten quienes abren | Menos de la mitad de lo normal del canal a 7 días (email 8.3 %, push 19.9 %, WhatsApp 6.1 %) | Apagar el canal: no hay a quién acotar |
| Veces (abren contra no abren) | Menos de 1.5 con muestra suficiente, en promocional | El mensaje no cambia nada: rehacer el mensaje o apagar |
| Entrega de WhatsApp | Debajo de 80 % | Limpiar base antes de seguir |
| Audiencia | Más de 1 M sin segmento | Re-segmentar |

Las acciones ya están calculadas por familia y canal en la pestaña Campañas (columna acción) y se resumen en Plan_accion. Hoy: 85 campañas activas debajo del mínimo (Estándares, fila 22); por canal, en email hay 12 por apagar, 79 por confirmar apagado, 82 por bajar frecuencia y 28 por rehacer; en push 15, 90, 2 y 89; en WhatsApp 56 por limpiar base.

## B9. Aprobación antes de activar

Nadie activa a un segmento real sin el checklist de D3 firmado por el dueño del segmento y MarTech. Para Todos o más de 1 M, también CRM.

---

# Parte C. Qué funciona y qué no, por dimensión

Cada sección trae las cifras de hoy (y dónde están en el Sheets), qué funciona, qué no, y la regla que sale de ahí. Promocional y lifecycle salvo que se diga otra cosa; cobranza y transaccional se comparan aparte porque responden por otra razón.

## C1. General (toda la operación)

Cifras (Estándares, columna "valor actual"):

| Indicador | Hoy | Estándar | Estado |
|---|---|---|---|
| Entrega de email | 95.1 % | 95 % o más | Cumple |
| Apertura de email | 23.6 % | 15 a 25 % | Cumple (inflada por Apple MPP; no decidir con ella) |
| Clic de email | 0.92 % (mediana por familia 0.52 %) | 1.5 % o más | Debajo, en los 4 equipos promocionales |
| Bajas de email por mil entregados | 3.13 | 2.5 o menos | Debajo |
| Apertura de push | 1.53 % (mediana 1.08 %) | 3 % o más | Debajo |
| Entrega de WhatsApp | 74.2 % | 90 % o más | Debajo |
| Lectura de WhatsApp | 68.8 % | 70 % o más | Debajo por poco |
| Clic de in-app | 38.2 % | 5 a 20 % | Cumple de sobra |
| Toques por comunicación y usuario al mes | 1.71 | 2 o menos | Cumple (Collections 3.86) |
| Mensajes por usuario al mes | 10.4 | | Cumple en promedio; 5.3 % de los usuarios con 41 o más en el periodo |
| Usuario-días con 3 o más campañas | 9.0 % | 10 % o menos | Cumple, pero concentra 24 % de los mensajes |
| Mensajes a canal mudo | 58.9 % | | Debajo |
| Usuarios que nunca respondieron (9 meses) | 72.9 % | | Debajo |
| Promocional a etapas bloqueadas | 43.78 M envíos | 0 | Debajo |
| Promocional a dados de baja | 79,994 emails | 0 | Debajo |
| Campañas activas debajo del mínimo del canal | 85 | 0 | Debajo |
| Envíos con ticket en el nombre | 87.4 % | 100 % | Debajo (Others 48.7 %) |

Qué funciona: in-app (38 % de clic) y WhatsApp cuando se entrega (69 % de lectura). Recordar algo que el usuario empezó. Dos toques en vez de uno. Audiencias de 10 a 100 mil con un criterio claro.

Qué no funciona: email masivo a prospectos (0.27 % de clic en 167 M envíos), push a bases frías (0.77 %), WhatsApp a bases frías (un tercio sin entrega), envíos a toda la base, tres o más toques, dos equipos sobre la misma audiencia el mismo día.

Regla general: antes de agregar un mensaje, quitar uno. El 59 % de lo que se manda va a un canal al que el usuario no responde y el 73 % de los usuarios nunca respondió a nada. La eficiencia de Braze en Kueski no está en mandar mejor, está en mandar menos y a quien sí.

## C2. Por equipo

Cifras del periodo (Vista_equipo con el equipo en B2; Equipos):

| Equipo | Familias | Envíos | % envíos | Costo MXN | % costo | Email clic | Bajas por mil | Push apertura | WA entrega | WA lectura | In-app clic | Toques | Ahorro estimado al mes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Marketing | 368 | 262.3 M | 39.3 % | 27.2 M | 47.2 % | 0.93 % | 4.95 | 1.09 % | 74.2 % | 70.6 % | 34.3 % | 1.77 | 160,647 |
| Product Growth (Lending) | 184 | 177.2 M | 26.5 % | 17.3 M | 29.9 % | 0.45 % | 3.02 | 2.10 % | 71.9 % | 60.5 % | 46.3 % | 1.86 | 1,296,806 |
| Sales | 205 | 85.3 M | 12.8 % | 7.1 M | 12.3 % | 0.21 % | 3.71 | 1.23 % | 79.9 % | 77.7 % | 8.1 % | 1.34 | 102,271 |
| Collections | 23 | 44.7 M | 6.7 % | 1.6 M | 2.8 % | 1.09 % | 0.25 | 3.61 % | | | 13.4 % | 3.86 | 0 (no se toca) |
| Others (*) | 283 | 98.0 M | 14.7 % | 4.4 M | 7.7 % | 1.83 % | 2.20 | 2.76 % | 71.4 % | 69.1 % | 80.1 % | 1.35 | 38,639 |

(*) Others agrupa transaccional, NewProducts (BillPay), Shopping, Compliance, CX y lo que no trae equipo en el nombre.

**Marketing.** Es el equipo con más envíos, más costo y más bajas por mil (4.95, el doble del estándar). Su patrón: Canvas grandes de "rescate" a leads y anónimos por push (RescateFinesDeSemana 13.4 M envíos con 0.76 % de apertura; Anonimos RescateTasa0 8.9 M con 0.56 %) y referidos por email a leads y dormants (8.5 M con 0.23 % y 7.0 M con 0.07 %). Lo que sí funciona en Marketing: el retargeting de Veriff (email 9.7 M con 3.04 % de clic; push 2.9 M con 5.8 %), el referido a clientes KCash por push (2.4 %) y el in-app de registro de línea MX (86.6 % de clic). Marketing también genera 58,988 de los 79,994 emails promocionales a dados de baja y 44 % de las bajas de usuarios nuevos (mediana 5 días, 10 emails) por el onboarding de registro. Acciones en Campañas: apagar 23, confirmar apagado 109, bajar frecuencia 51, rehacer 54, limpiar WhatsApp 23, proteger 45, escalar 63.

Regla para Marketing: referidos y lanzamientos salen de email masivo y van a in-app o push a clientes activos. Los rescates por push a anónimos y leads se acotan a quienes abrieron algún push en 60 días (el push está bien: quien abre convierte 6 a 7 veces más, pero abre menos del 1 %). Onboarding a 1 email al día. Filtro de suscripción en cada paso.

**Product Growth (Lending).** Tiene el ahorro más grande (1.3 M MXN al mes) porque concentra los emails de volumen que no responden: B0211 Nuevos Registrados Tasa 0 (34.9 M emails, 0.28 % de clic, 0.47 % de conversión entre quienes abren contra 8.3 % normal en email), B0223 NeverActive Installments (13.5 M, 0.10 %), B0337 CuestaEnero (7.4 M, 0.19 %), B0440 AnotayGana (7.2 M, 0.19 %). También pierde al usuario a los tres meses por insistencia (mediana 92 a 128 días y 17 a 31 emails antes de la baja). Lo que funciona: Retargeting Installments a activos (email 2.78 % y 2.14 %; push 11.0 %), B0209 Inactivos DescuentoDirecto se sostiene (0.55 %), y el in-app (46 %). Su WhatsApp es el que peor se lee (60.5 %) y de los que peor se entregan (71.9 %).

Regla para Product Growth: Tasa 0 y ofertas a registrados sin crédito solo con segmento de señal (abrió algo en 90 días) y tope de 2 toques al mes; B0211 y B0223 se apagan por email y se dejan en push acotado. Un solo dueño de los segmentos fríos (A4) para dejar de pisarse con Marketing B0326.

**Sales.** El clic de email más bajo de todos (0.21 %) y el in-app más bajo (8.1 %), pero el mejor WhatsApp (79.9 % de entrega, 77.7 % de lectura) y un push aceptable en recurrentes (Comercio del día 1.1 a 1.8 %; QuincenasSinIntereses 4.2 %; KUESKIPRIMAVERA 2.2 %). Lo que no funciona: promociones de comercios por email a todo el portafolio (B0335, 6.4 M emails, 0.22 %) y el mismo evento repetido por dos canales el mismo día (HotSale push + push y push + WhatsApp a 450 mil usuarios). Sus ventas a recurrentes sí sostienen la diferencia abren contra no abren a 90 días (2 a 2.5 veces, 27 a 39 % de conversión entre quienes abren): son las que vale la pena re-segmentar en vez de apagar.

Regla para Sales: el canal de Sales es push y WhatsApp a recurrentes de KPay, no email. Un evento (Hot Sale, Buen Fin) = una pieza por canal y un calendario con Marketing para no mandar la misma promoción dos veces (Cuponera HotSale de Marketing y HotSale de Sales coincidieron 5 meses en 530 mil usuarios). Excluir CC Freeze en todo (13.0 M envíos a quien no puede pagar con KPay).

**Collections.** No se toca con las reglas promocionales: es cobranza y su respuesta depende del proceso. Pero sí hay orden que poner: 3.86 toques por usuario al mes (el doble del tope promocional, aceptable en cobranza pero hay que declararlo), todo con ticket T000 (un C#### por bucket), y Canvas `PRUEBA_` de cobranza que llegaron a 5,166 usuarios reales dados de baja. Precobranza es la pieza que mejor responde de toda la empresa en email (4.3 %) y push (5.3 %): protegerla. Pendiente con Legal: 61 mil envíos de cobranza a REUS y ARCO.

**Others.** Mezcla transaccional (que responde bien: Payment Confirmation 3.8 %, DD advance 2.1 %) con dos piezas promocionales de volumen que no responden: BillPay Intro (16.1 M emails, 0.11 % de clic, 31 % de las bajas de usuarios nuevos del año) y Shopping WeeklyRecommendations (7.0 M, 0.12 %, 57 mil envíos a REUS). Solo 48.7 % de sus envíos trae ticket.

Regla para Others: lo transaccional se nombra con la convención y ticket (hoy no lo hace) y se protege. BillPay y Shopping entran a las reglas promocionales como cualquier otro equipo: segmento, prueba al 10 %, tope.

## C3. Por canal

Cifras (Canales):

| Canal | Familias | Activas | Envíos | Costo MXN | Respuesta | Mediana por familia | Mínimo para seguir | Estado |
|---|---|---|---|---|---|---|---|---|
| Email | 523 | 167 | 333.5 M | 16.7 M | 0.92 % clic | 0.52 % | 0.3 % | 185 familias en apagar o rehacer |
| Push | 682 | 155 | 251.1 M | 0 | 1.53 % apertura | 1.08 % | 0.75 % | 330 en apagar o rehacer; 58 % del volumen en piezas con menos de 1 % |
| WhatsApp | 309 | 57 | 55.2 M | 41.0 M (sobre entregados) | 68.8 % lectura | 67.4 % | 60 % lectura, 80 % entrega | 25.8 % sin entrega; 56 familias por limpiar base |
| In-app | 398 | 100 | 27.4 M | 0 | 38.2 % clic | 18.2 % | 10 % | 194 en apagar o rehacer, pero por volumen chico; 70 por proteger |

**Email.** Funciona: transaccional (2.74 % de clic), retargeting de algo que el usuario empezó (2.99 %), dos toques (1.76 %), audiencias de 10 a 100 mil (1.15 %), nuevos (1.25 %). No funciona: tasa 0 a registrados (0.53 %), referidos (0.22 %), newsletters y lanzamientos (0.22 %, y las bajas más altas: 5.6 por mil), bases frías (0.35 %), envíos de más de 1 M (0.16 %). Es el canal que se da de baja: 439 mil usuarios únicos en 9 meses (2.2 % de la base con email). Regla: email para transaccional, retargeting y nuevos; promoción masiva por email solo a quien hizo clic en un email en 90 días. Asunto no es el problema (abren 23.6 %): es que no hay qué hacer dentro. Un solo llamado a la acción.

**Push.** Funciona: cobranza (3.6 %), nuevos (3.2 %), retargeting (2.2 %), recurrentes (1.75 %), dos toques (2.52 %). No funciona: leads y anónimos (0.94 %), bases frías (0.77 %), tasa 0 (0.68 %), lanzamientos (0.82 %). Quien abre un push convierte 3 veces más que quien no (mediana 19.9 % contra 6.6 %): el push es el mejor canal para acotar bases por señal. Regla: push es el canal de señal. Primero push barato, y el resto de la secuencia solo a quien lo abrió. Tope de 1 push promocional al día.

**WhatsApp.** Funciona: activos y recurrentes (70 % de lectura, 82 % de entrega), Sales a recurrentes de KPay (78 %). No funciona: bases frías (65 % de lectura, 68 % de entrega, 23 M MXN), WhatsApp de pago a quien nunca leyó uno (3.2 M MXN), versiones repetidas con 2 a 6 días de diferencia (B0333 Churn). Es el 8 % de los envíos y el 77 % del costo variable. Regla: WhatsApp solo detrás de una señal (abrió push, email o in-app) o a activos, nunca como primer toque a una base fría. Limpiar `EXC-WA-SinEntrega3` antes de cualquier envío. Un WhatsApp promocional al mes por usuario.

**In-app.** Funciona casi todo porque llega a quien ya abrió la app: referidos (42.7 % contra 0.22 % por email), lanzamientos (54.5 %), retargeting (57.9 %), onboarding (63.8 %). No funciona: ofertas y descuentos genéricos (14.4 %), cobranza (13.4 %). Regla: referidos, lanzamientos, novedades y encuestas van en in-app primero. Es gratis y es el canal con más respuesta. El 5.5 % de los usuarios que solo responde a in-app recibe 43 mensajes al año por otros canales que no abre.

**Banner.** Una sola comunicación (217 mil impresiones). Sin reglas propias; se trata como in-app.

## C4. Por mes

Cifras (serie mensual de E4a; Canales y Mensual):

| Mes | Envíos | Email clic | Bajas por mil entregados | Push apertura | WhatsApp enviados | WA entrega | WA lectura | In-app clic | Costo MXN | Comunicaciones activas |
|---|---|---|---|---|---|---|---|---|---|---|
| Ene | 58.7 M | 1.20 % | 2.15 | 1.83 % | 5.6 M | 80.0 % | 74.6 % | 47.6 % | 7.4 M | 511 |
| Feb | 67.5 M | 0.88 % | 1.71 | 1.43 % | 7.8 M | 77.1 % | 73.3 % | 19.1 % | 9.5 M | 548 |
| Mar | 67.8 M | 1.03 % | 1.44 | 1.81 % | 10.4 M | 73.9 % | 72.5 % | 24.0 % | 12.2 M | 475 |
| Abr | 64.3 M | 0.98 % | 1.19 | 1.53 % | 5.9 M | 69.3 % | 65.6 % | 36.0 % | 7.6 M | 605 |
| May | 85.0 M | 0.86 % | 0.99 | 1.28 % | 6.1 M | 67.3 % | 67.1 % | 47.4 % | 8.1 M | 632 |
| Jun | 109.0 M | 0.67 % | 1.34 | 1.05 % | 7.1 M | 74.3 % | 67.4 % | 45.4 % | 9.7 M | 574 |
| Jul | 71.7 M | 1.00 % | 1.71 | 1.77 % | 4.8 M | 72.9 % | 62.5 % | 37.0 % | 6.4 M | 494 |
| Ago | 78.0 M | 0.95 % | 1.51 | 1.57 % | 4.4 M | 78.0 % | 63.6 % | 41.5 % | 6.1 M | 597 |
| Sep | 65.6 M | 0.92 % | 1.09 | 2.12 % | 3.2 M | 77.3 % | 64.1 % | 41.5 % | 5.0 M | 567 |

(Las bajas por mil de esta tabla son usuarios únicos por mes sobre entregados; la cifra 3.13 del estándar es eventos sobre entregados en todo el periodo.)

Qué dice:

- **Junio** es el peor mes: 109 M envíos (el doble de enero), apertura de email 18.1 %, clic 0.67 %, push 1.05 %, 63 mil bajas (13.9 % de las del año). Es el mes del envío de BillPay a 16.1 M usuarios y del lanzamiento con dos equipos pisándose (AnotayGana de Lending y BillPay Intro de NewProducts el mismo día en 1.23 M usuarios). El volumen extra no trajo respuesta extra.
- **Enero** tiene el clic más alto (1.20 %) y también la tasa de bajas más alta (2.15 por mil, 69 mil bajas, 15.1 % del año): arranque de año con muchas piezas nuevas (CuestaEnero, Tasa 0) sobre bases que no habían recibido en diciembre.
- **Marzo** es el mes más caro (12.2 M MXN) por 10.4 M WhatsApp, con la entrega ya cayendo (73.9 %).
- **Abril y mayo** son el piso de entrega de WhatsApp (69 % y 67 %): la base se degradó y se siguió mandando. Se recuperó a 77 a 78 % cuando bajó el volumen (agosto y septiembre, 3 a 4 M).
- **Mayo, junio y agosto** son los meses de más solape (1.9 M, 2.3 M y 2.1 M usuarios con un día de 3 o más campañas): Hot Sale, BillPay y regreso a clases.
- **Septiembre** es el mejor push del año (2.12 %) con el menor volumen de push desde marzo (24 M): menos push, más apertura.
- Las comunicaciones activas van de 475 a 632 al mes. No hay estacionalidad en la cantidad; la hay en el volumen por pieza.

Reglas de calendario:

- Los meses con evento comercial (Hot Sale en mayo, regreso a clases en agosto, Buen Fin en noviembre, Cuesta de enero) se planean con un calendario único (D5): una pieza por equipo y canal, y el tope de 2 familias por usuario al día aplica igual.
- Ningún lanzamiento de producto se manda a toda la base en el mismo mes que un evento comercial. BillPay en junio con Hot Sale encima explica el peor mes del año.
- Cuando la entrega de WhatsApp de un mes baja de 75 %, el mes siguiente no sube el volumen hasta limpiar la base.
- El volumen de push de un mes no debe superar 1.3 veces el promedio de los tres anteriores sin aprobación de CRM. Junio (46.8 M) fue 1.8 veces el promedio.
- El día de la semana y la hora quedan pendientes (E10; la hora no está en las tablas).

## C5. Por producto

Cifras (Campañas filtrada por producto):

| Producto | Familias | Envíos | Costo MXN | Email clic | Bajas por mil | Push apertura | WA lectura | Ahorro estimado al mes |
|---|---|---|---|---|---|---|---|---|
| KCash | 543 | 318.7 M | 33.7 M | 0.82 % | 3.27 | 1.80 % | 68.9 % | 629,234 |
| KPay | 985 | 232.5 M | 19.0 M | 0.44 % | 3.62 | 1.11 % | 68.3 % | 930,490 |
| Ecosistema | 42 | 25.8 M | 1.4 M | 0.37 % | 3.92 | 1.19 % | 70.0 % | 0 |
| Cash Installments | 10 | 2.6 M | 0.08 M | 1.41 % | 0.49 | 2.73 % | | 0 |
| Others (BillPay, transaccional, corporativo) | 333 | 87.9 M | 3.5 M | 1.83 % | 2.11 | 3.11 % | 77.5 % | 38,639 |

- **KCash** se lleva el 48 % de los envíos y el 58 % del costo. Responde el doble que KPay en email y push. Sus problemas son de insistencia (Tasa 0 a registrados, rescates a leads) y de dos equipos sobre la misma base. 52 % de las bajas de usuarios nuevos caen el día de un email de KCash.
- **KPay** tiene casi el doble de familias que KCash (985) para 73 % de su volumen: muchas piezas chicas y repetidas (Comercio del día por mes, Hot Sale por semana). Es el producto con menos respuesta en email (0.44 %) y push (1.11 %) y el que más promoción manda a quien tiene la tarjeta congelada. La baja de KPay en nuevos es la más rápida (mediana 1 a 2 días, retargeting de cuenta y de NIP con cupón).
- **Ecosistema** (AnotayGana, aviso de privacidad, registro de línea): piezas a `Todos`, bajas más altas (3.92 por mil) y clic más bajo (0.37 %). Lo único que funciona ahí es el in-app (86.6 % en registro de línea MX).
- **Installments** responde bien (1.41 % de clic, 0.49 bajas por mil) con poco volumen: candidata a escalar con segmento.

Reglas por producto: KPay pasa de "muchas piezas chicas" a familias recurrentes con versión única (Comercio del día = una familia, no una por mes) y canal push + WhatsApp a recurrentes. KCash concentra Tasa 0 en un solo dueño y una sola familia por audiencia. Ecosistema no manda nada a `Todos` sin pasar por in-app primero. Una pieza no cubre dos productos: se parte.

## C6. Por tipo de comunicación

| Tipo | Familias | Envíos | Costo MXN | Email clic | Bajas por mil | Promocional a bloqueados | Emails a dados de baja |
|---|---|---|---|---|---|---|---|
| Promocional o lifecycle | 1,625 | 571.6 M | 53.7 M | 0.60 % | 3.87 | 43.78 M | 79,994 |
| Transaccional u operativa | 249 | 51.0 M | 2.3 M | 2.74 % | 0.95 | 8.16 M (legítimo salvo Blacklist) | 561,566 (legítimo) |
| Cobranza | 39 | 44.7 M | 1.6 M | 1.09 % | 0.25 | 5.61 M (revisar REUS con Legal) | 783,911 (legítimo) |

- Lo promocional es el 86 % del volumen, el 93 % del costo, el 89 % de las bajas de nuevos y todo el problema. Transaccional y cobranza funcionan y no se tocan con reglas de frecuencia; solo se les aplica nomenclatura, ticket, una versión activa y Blacklist.
- Dentro de promocional, el lifecycle (bienvenida, retargeting de embudo, recordatorio de algo empezado) responde 5 a 10 veces más que la promoción pura (oferta, tasa 0, novedades). El tipo se marca con el tag `tipo:` (A5) para poder separarlos en el admin; en Databricks se sigue infiriendo por el nombre.

Regla: todo lo nuevo se declara promocional, lifecycle, transaccional o cobranza antes de crearse, y eso decide qué reglas de la Parte B le aplican. Un transaccional no lleva oferta (si la lleva, es promocional y entra a las reglas).

## C7. Por segmento

### C7a. Por etapa del usuario (golden dataset, cubre 37 % de los envíos)

| Etapa | Envíos | Promocional | Email clic (promo) | Push apertura (promo) | WA lectura (promo) | In-app clic (promo) | Conversión de referencia por mil |
|---|---|---|---|---|---|---|---|
| Prospectos (sin crédito) | 189.1 M | 167.2 M | 0.27 % | 1.33 % | 54.3 % | 26.8 % | 10.7 |
| Tarjeta KPay congelada | 56.6 M | 43.4 M | 0.38 % | 1.45 % | 51.7 % | 32.9 % | 7.9 |
| REUS o ARCO | 0.49 M | 0.25 M | | | | | 7.9 |
| Blacklist | 0.43 M | 0.15 M | | | | | 5.9 |
| Sin etapa en la tabla | 416.2 M | 356.3 M | 0.67 % | 1.20 % | 49.2 % | 50.9 % | 5.3 |

Regla: prospectos no reciben email promocional masivo (0.27 % de clic, debajo del mínimo de apagado, en el 28 % de todo lo que se manda); se trabajan con push de señal e in-app. Las tres etapas bloqueadas salen por `EXC-` (B1).

### C7b. Por audiencia (según el nombre de la pieza)

| Audiencia | Email clic | Bajas por mil | Push apertura | WA lectura | WA entrega | WA costo MXN |
|---|---|---|---|---|---|---|
| Nuevos y onboarding | 1.25 % | 6.9 | 3.18 % | 67.5 % | 77.4 % | 0.8 M |
| Clientes activos y recurrentes | 0.72 % | 3.1 | 1.75 % | 70.1 % | 81.6 % | 14.9 M |
| Leads y registrados sin crédito | 0.75 % | 4.6 | 0.94 % | 73.4 % | 74.9 % | 15.1 M |
| Fríos (dormants, inactivos, rezagados, never active) | 0.35 % | 4.3 | 0.77 % | 64.6 % | 68.5 % | 23.0 M |

Qué funciona: nuevos responden más en todo (y también se dan de baja más: hay que cuidar la frecuencia, no el mensaje). Activos leen WhatsApp y abren push. Qué no: fríos responden la mitad y se llevan un tercio del gasto de WhatsApp con 1.1 conversiones de referencia por mil contra 17 en activos.

Regla: la audiencia pesa más que el canal. Fríos: primero push o email de bajo costo para detectar señal, WhatsApp solo a quien reaccionó, 3 toques en 30 días y fuera. Nuevos: una secuencia, 1 email al día, tope de 3 la primera semana. Leads: push de señal e in-app; email solo retargeting del paso que dejaron.

### C7c. Por gancho

| Gancho | Email envíos | Email clic | Bajas por mil | Push apertura | WA lectura | In-app clic |
|---|---|---|---|---|---|---|
| Retargeting o recordatorio | 23.6 M | 3.09 % | 3.8 | 2.16 % | 70.3 % | 57.9 % |
| Tasa 0 | 54.3 M | 0.53 % | 4.6 | 0.68 % | 68.8 % | 21.7 % |
| Descuento, cupón u oferta | 35.0 M | 0.41 % | 3.4 | 1.38 % | 57.8 % | 14.4 % |
| Cross sell | 2.7 M | 0.34 % | 2.0 | 1.69 % | 53.8 % | 24.7 % |
| Referidos | 40.8 M | 0.22 % | 4.3 | 1.15 % | 71.4 % | 42.7 % |
| Lanzamiento, novedades, newsletter | 33.0 M | 0.22 % | 5.6 | 0.82 % | 72.8 % | 54.5 % |

Qué funciona: recordar algo que el usuario ya empezó responde 5 a 10 veces más que ofrecer algo nuevo, en todos los canales. Qué no: tasa 0 es el gancho más usado y el que peor abre en push; referidos y lanzamientos no funcionan por email (0.22 %) y sí en in-app (43 % y 55 %): el mensaje está bien, el canal no.

Regla: el gancho principal de email es "lo que dejaste a medias". Referidos, lanzamientos y newsletters van en in-app. Tasa 0 solo con segmento de señal y en push, nunca como email masivo a registrados.

### C7d. Por número de toques (misma comunicación, mismo usuario, mismo mes; todos los tipos)

| Toques | Email clic | Email apertura | Bajas por mil | Push apertura |
|---|---|---|---|---|
| 1 | 0.76 % | 21.7 % | 2.2 | 1.18 % |
| 2 | 1.76 % | 35.3 % | 1.5 | 2.52 % |
| 3 a 4 | 0.48 % | 19.2 % | 1.6 | 1.56 % |
| 5 o más | 0.84 % | 14.1 % | 1.4 | 1.11 % |

Regla: 2 toques, el segundo solo a quien no abrió el primero. El tercero ya no suma.

### C7e. Por tamaño de la audiencia (usuarios por comunicación y mes; todos los tipos. Solo promocional: 1.15 %, 0.57 % y 0.16 % de clic en email)

| Tamaño | Email clic | Bajas por mil | Push apertura | WA lectura |
|---|---|---|---|---|
| Menos de 10 mil | 6.2 % (casi todo transaccional) | | 3.2 % | |
| 10 mil a 100 mil | 1.63 % | 1.7 | 2.24 % | 64.5 % |
| 100 mil a 1 M | 0.86 % | 1.5 | 1.45 % | 65.8 % |
| 1 M o más | 0.16 % | 2.5 | 0.87 % | |

Regla: el tamaño óptimo de una pieza promocional es de 10 a 100 mil usuarios con un criterio. Más de 1 M obliga a prueba al 10 % y segmento (B6).

### C7f. Por patrón de respuesta del usuario (a qué canal responde)

| Responde a | Usuarios | % usuarios | % mensajes | % costo | Mensajes por usuario (9 meses) | Convierten | Baja de email |
|---|---|---|---|---|---|---|---|
| Ninguno | 14.2 M | 72.9 % | 23.8 % | 13.8 % | 11 | 0.08 % | 1.4 % |
| Solo WhatsApp | 1.6 M | 8.1 % | 14.9 % | 34.2 % | 63 | 2.0 % | 3.4 % |
| Solo in-app | 1.1 M | 5.5 % | 6.9 % | 3.7 % | 43 | 8.8 % | 1.7 % |
| WhatsApp + in-app | 511 mil | 2.6 % | 9.2 % | 11.5 % | 120 | 37.3 % | 2.9 % |
| Push + WhatsApp + in-app | 371 mil | 1.9 % | 12.9 % | 10.5 % | 234 | 62.1 % | 2.1 % |
| Solo email | 365 mil | 1.9 % | 1.8 % | 1.2 % | 33 | 5.0 % | 15.8 % |
| Los cuatro canales | 255 mil | 1.3 % | 10.0 % | 8.2 % | 262 | 75.5 % | 5.1 % |

Qué dice: quien responde a varios canales convierte mucho más, pero no porque los canales conviertan, sino porque es cliente activo que usa la app. Sirve para segmentar, no para atribuir. Quien solo responde a WhatsApp es 8 % de los usuarios y 34 % del costo, y recibe 58 M emails y 21 M push que nunca abre. Quien solo responde a email es quien más se da de baja (15.8 %): el lector de email que no usa la app se cansa.

Regla: `brz_canal_preferido_90d` como regla de envío (B3) y el patrón de respuesta como segmentación de valor: a los multicanal (4 % de los usuarios) se les cuida la frecuencia porque son los que convierten; a los "solo WhatsApp" se les quita email y push; a los "ninguno" se les aplica B4.

## C8. Usuarios nuevos (primer email de febrero en adelante)

Cifras (158,520 bajas de nuevos; Insights, bajas):

| | Valor |
|---|---|
| Días hasta la baja (mediana) | 27 |
| Emails antes de la baja (mediana) | 5 |
| Familias distintas antes de la baja | 4.2 |
| Se dan de baja con el primer email | 33 % |
| Se van en la primera semana | 31 % (recibieron 4.4 emails en esos días) |
| Se van en los primeros 30 días | 53 % |
| Se van el mismo día del primer email | 7.4 % (estándar: 5 % o menos) |

Qué causa las bajas de nuevos: un envío masivo sin filtro (BillPay Intro: 31 % de las bajas, 1.8 emails antes), el retargeting de registro de Marketing (Veriff, PersonalInfo, NIP: 22 %, mediana 3 a 4 días, 5 a 8 emails en ese lapso), los rescates de Tasa 0 (8.5 %), B0211 Tasa 0 (4.6 %, a los 92 días y 18 emails), el transaccional FraudRisk (4.1 %, al día 2).

Regla: un usuario nuevo entra a una sola secuencia de bienvenida por producto y nada más hasta que termina (hoy recibe 4.2 familias distintas). Retargeting de registro a 1 email al día y máximo 3 la primera semana; el resto por push e in-app. Si no abrió ninguno de sus primeros 5 emails, se pausa lo promocional por email. Ningún envío masivo incluye a usuarios con menos de 30 días.

## C9. Dimensiones que faltan y qué harán cuando lleguen

- **Día de la semana (E10).** Respuesta y bajas por día de la semana, canal y equipo. Dará la regla de qué día mandar cada canal y si el fin de semana castiga (RescateFinesDeSemana es la pieza de push más grande de Marketing y abre 0.76 %).
- **Segmentación real de Braze (E11).** Las columnas `segment`, `subsegment` y `group` de la tabla de envíos dirán cuántos segmentos distintos están en uso, cuáles se repiten entre equipos y cuántos tienen menos de mil envíos. Es el insumo para cerrar la lista de A4.
- **Antigüedad (E12).** Respuesta y baja por meses desde el alta. Dirá hasta qué antigüedad vale la pena insistir y a partir de cuál la base es fría aunque el nombre diga "recurrentes".
- **Tipo de celular, hora y región.** No salen de Databricks con las tablas actuales. Si hace falta, la hora podría pedirse al equipo de datos como columna nueva (`event_time`); el dispositivo necesitaría una llave de usuario en `_dim_braze_device`.

---

# Parte D. Operación: crear, mejorar, revisar

## D1. Guía para crear algo nuevo

Nueve preguntas, en este orden. Si una no tiene respuesta, la pieza no se crea todavía.

**1. Qué quiero que pase (objetivo y tipo).** Un solo evento de conversión de A9 y una ventana (7 días). Declarar el tipo: promocional, lifecycle, transaccional o cobranza. Eso fija qué reglas de la Parte B aplican.

**2. A quién (audiencia).** Un segmento maestro de A4 más, si hace falta, un filtro dentro del Canvas. Nunca `Todos` sin filtro de respuesta en 90 días. Checar que el dueño del segmento no tenga ya una pieza viva con el mismo gancho (pestaña Catálogo del Sheets, filtrar por audiencia y gancho): si la hay, se mejora esa, no se crea otra.

| Si la audiencia es | Entonces |
|---|---|
| Nuevos (0 a 30 días) | Solo la secuencia de bienvenida de su producto. Si ya existe, la pieza nueva es un paso de esa secuencia, no un Canvas aparte. |
| Leads o registrados sin crédito | Push de señal e in-app. Email solo si es retargeting del paso exacto que dejaron. Nada de WhatsApp como primer toque. |
| Activos y recurrentes | Cualquier canal; WhatsApp permitido si la pieza vale más de 1 MXN por entregado. In-app primero si el mensaje es informativo (novedad, referidos). |
| Fríos (inactivos, dormants, churn, never active) | Dueño único (Lending). 3 toques en 30 días, canal más barato, un solo gancho. WhatsApp solo a quien reaccionó. Después, fuera. |
| Comercios (B2B) | Email y WhatsApp a `SEG-KPayB2B-Comercios-*`; no entra al frequency cap de consumidores pero sí a la nomenclatura. |
| Cobranza | Fuera de las reglas promocionales. Ticket C####, Blacklist según Legal. |

**3. Por qué canal.** Según la audiencia (arriba) y el gancho (abajo). Si el usuario ya tiene `brz_canal_preferido_90d`, ese canal manda. Orden de costo cuando hay empate: in-app, push, email, WhatsApp.

| Si el gancho es | Canal principal | Por qué |
|---|---|---|
| Retargeting o recordatorio de algo empezado | Email y push | 3.09 % de clic en email, 2.16 % en push; es lo único que funciona bien por email |
| Referidos | In-app, luego push a clientes activos | 42.7 % en in-app contra 0.22 % en email |
| Lanzamiento, novedad, newsletter | In-app | 54.5 % contra 0.22 % en email y 5.6 bajas por mil |
| Tasa 0 | Push a quien abrió un push en 60 días; WhatsApp solo detrás de esa señal | 0.53 % en email; quien abre el push convierte 6 a 18 veces más, pero abre menos del 1 % |
| Descuento, cupón, evento comercial (KPay) | Push y WhatsApp a recurrentes de KPay | Es el canal de Sales que funciona (78 % de lectura); email 0.21 % |
| Encuesta, aviso legal | In-app, email una sola vez | |
| Transaccional | El canal del proceso; email con plantilla transaccional | 2.74 % de clic, no se toca |

**4. Cuántas veces (frecuencia).** Máximo 2 toques por mes por esta pieza, el segundo solo a quien no abrió el primero (paso de Decision en A3). La pieza entra al frequency cap global de 5 promocionales por semana, 2 familias al día y 1 push al día: si la audiencia ya está saturada, la pieza espera o reemplaza a otra.

**5. Cuándo.** Revisar el calendario único (D5). No se lanza en la misma semana que un evento comercial de otro equipo a la misma audiencia. No se lanza a toda la base en junio, mayo ni agosto (meses de más solape). Mientras no llegue E10, el día de la semana lo decide la prueba del paso 7.

**6. Cómo se llama.** Nombre con las 8 posiciones de A2 y listas cerradas. Pasos de Canvas con A3. Tags de A5. Grupo de suscripción de A6 en cada paso de email. UTMs de A10. Ticket abierto antes de crear la pieza y `communication_id` anotado en el ticket cuando exista.

**7. Cómo se prueba.** Grupo de control del 10 % (posición 8 = Control). Si la audiencia pasa de 1 M, prueba previa al 10 % durante 48 horas y lectura de bajas por mil y respuesta contra el mínimo del canal antes de abrir al resto. Entre 100 mil y 1 M, prueba al 5 %.

**8. Cómo se mide.** A las 4 semanas: respuesta contra el mínimo del canal (B8), bajas por mil, convierten quienes abren contra quienes no (mínimo la mitad de lo normal del canal y 1.5 veces), lift contra el grupo de control a 7 días. En el Sheets aparece sola en Campañas al mes siguiente, por familia y canal, con su acción.

**9. Cómo termina.** Fecha de revisión en el ticket. Si a las 4 semanas no cumple B8, se apaga o se rehace sin discutir. Si cumple, se revisa cada mes con el ciclo de D4. Una pieza sin envíos 90 días se archiva.

## D2. Cómo hacer más eficiente algo que ya existe

Buscar la familia en la pestaña Campañas (una fila por familia y canal) y leer la columna acción. Cada acción tiene su receta:

| Acción en el Sheets | Qué significa | Qué se hace en Braze |
|---|---|---|
| Apagar | Volumen alto, respuesta debajo del mínimo, y ni quien abre convierte | Archivar la pieza en ese canal. Si el mensaje sirve en otro canal (push de B0211 convierte 18 veces entre quienes abren), dejar solo ese canal acotado a quien abrió en 60 días. |
| Confirmar apagado | Debajo del mínimo pero ya sin envíos recientes | Confirmar que está archivada, no pausada. Si quedó una versión viva, archivarla. |
| Bajar frecuencia | Responde pero se da de baja arriba de 2.5 por mil o manda 3 o más toques | Tope de 2 toques al mes con Decision "no abrió"; quitar pasos 3 en adelante; filtro de suscripción en cada paso. |
| Rehacer o re-segmentar | Responde debajo del mínimo pero quien abre sí convierte, o audiencia de más de 1 M sin criterio | Cambiar el segmento al maestro de A4 más un filtro de señal (abrió algo en 90 días); cambiar el gancho si es tasa 0 o novedades por email; volver a lanzar como versión nueva con control. |
| Limpiar base de WhatsApp | Entrega debajo de 80 % | Aplicar `EXC-WA-SinEntrega3`; pausar hasta que la entrega de prueba al 5 % pase de 80 %. |
| Escalar | Responde arriba del mínimo con audiencia chica | Ampliar la audiencia al siguiente segmento maestro de la misma familia (de Activos a Recurrentes), con control del 10 %; no cambiar el mensaje. |
| Proteger | Alto volumen y buena respuesta | No tocar el mensaje; vigilar bajas y toques; es la referencia para rehacer las demás de su audiencia. |
| Seguir igual | Cumple, sin señal clara | Nada; revisión mensual. |
| No tocar | Transaccional o cobranza | Solo nomenclatura, ticket y una versión activa. |

Las cifras de ahorro por acción están en Plan_accion (P1 por acción, P2 las diez familias que más pesan, P3 por equipo) y el total por equipo en Vista_equipo. El ahorro estimado del plan es por mes y con los parámetros de Parámetros; cambia si cambia el costo de WhatsApp o la definición de respuesta.

## D3. Checklist antes de activar (lo firma el dueño del segmento y MarTech)

1. Tipo declarado (promocional, lifecycle, transaccional, cobranza) y tag `tipo:` puesto.
2. Ticket abierto con prefijo correcto; nombre con las 8 posiciones y listas cerradas; sin "Copy of", "TEST", "N/A" ni "Not Tracked".
3. Audiencia = segmento maestro de A4 (más filtro dentro del Canvas si aplica). Si es `Todos` o más de 1 M, aprobación de CRM y prueba al 10 %.
4. Los 7 segmentos `EXC-` como filtro negativo (promocional y lifecycle). Blacklist en todo.
5. Filtro de suscripción del grupo correcto en cada paso de email, no solo a la entrada.
6. Canal según C7c y `brz_canal_preferido_90d`. Si hay WhatsApp, va detrás de una señal o a activos, y con `EXC-WA-SinEntrega3`.
7. Máximo 2 toques al mes por usuario, el segundo con Decision "no abrió". Paso de Salida con motivo.
8. Frequency cap global respetado (5 promocionales por semana, 2 familias al día, 1 push al día, 24 h entre promocionales).
9. Grupo de control del 10 % y evento de conversión de A9 configurado con ventana de 7 días.
10. Plantilla `TPL-` vigente, UTMs con ticket, un solo llamado a la acción.
11. Calendario único revisado: ninguna otra pieza a la misma audiencia con el mismo gancho esa semana; no coincide con un evento comercial de otro equipo.
12. Fecha de revisión a 4 semanas anotada en el ticket y la versión anterior de la misma familia archivada.

## D4. Ciclo mensual

| Semana | Qué | Quién | Con qué |
|---|---|---|---|
| 1 | Actualizar las extracciones E1 a E9 del mes y regenerar el Sheets como archivo nuevo | Datos | `sql/extraccion.sql`, `scripts/build_sheets_v2.py` |
| 1 | Leer Estándares: qué indicador se movió y qué equipo lo mueve | CRM | Estándares (24 filas, valor por equipo) |
| 2 | Revisar Plan_accion: las familias en Apagar, Confirmar apagado y Limpiar WhatsApp se ejecutan; Rehacer y Bajar frecuencia se asignan con ticket | Cada equipo con MarTech | Plan_accion, Campañas |
| 2 | Higiene: piezas sin envío 90 días, versiones duplicadas, `TEST` y `Copy of` activos, nombres fuera de convención | MarTech | Catálogo |
| 3 | Calendario del mes siguiente: una pieza por equipo, canal y audiencia; eventos comerciales | Marketing, Sales, Lending con CRM | Calendario único (D5) |
| 4 | Nuevas piezas pasan el checklist D3 y se activan con control | Dueños y MarTech | Este playbook |
| Trimestral | Revisar segmentos maestros, lista de tags, grupos de suscripción, plantillas; archivar lo sin uso; actualizar este playbook con E10 a E12 y lo que haya cambiado | MarTech y CRM | |

## D5. Gobierno

- **Dueños.** Un dueño por familia de segmentos (A4). Un dueño por pieza (el ticket lo dice). MarTech es dueño de nomenclatura, tags, grupos de suscripción, plantillas, exclusiones y frequency cap. CRM es dueño del calendario único y de los estándares.
- **Calendario único de envíos promocionales.** Una sola vista compartida (puede ser una pestaña más del Sheets) con fecha, equipo, pieza, audiencia, canal, gancho y tamaño. Nada promocional se activa sin estar ahí. Hoy el 62 % de las coincidencias de dos campañas el mismo día son entre equipos distintos.
- **Comité quincenal de 30 minutos** (Marketing, Lending, Sales, Collections, Producto, MarTech, CRM): conflictos de calendario, piezas nuevas a `Todos`, cambios a exclusiones y frequency cap, familias en Apagar que el equipo quiera defender (con grupo de control, no con opinión).
- **Legal y Riesgo** aprueban cambios a `EXC-Global-REUS_ARCO`, `EXC-Global-Blacklist` y `EXC-KPay-CCFreeze`, y resuelven si cobranza excluye REUS y ARCO.
- **Estándares del mes** se publican en la pestaña Estándares con el valor por equipo. Un indicador en rojo dos meses seguidos abre un ticket al equipo que lo mueve.
- **Excepciones** a cualquier regla de la Parte B se piden en el ticket y se aprueban en el comité, con fecha de fin. Sin fecha de fin no hay excepción.

## D6. Glosario

- **Familia.** Comunicación sin la fecha del nombre; agrupa sus versiones.
- **Respuesta.** Clic en email, apertura en push, lectura en WhatsApp, clic en in-app. Abrir un email no es respuesta.
- **Toque.** Un mensaje de la misma comunicación al mismo usuario en el mes.
- **Canal mudo.** Canal al que el usuario nunca respondió aunque sí respondió a otro.
- **Nunca respondieron.** Usuarios que recibieron algo y no tienen ni una respuesta en ningún canal en el periodo (9 meses) o en 90 días.
- **Etapa bloqueada.** Blacklist, REUS o ARCO, tarjeta KPay congelada (golden dataset).
- **Mínimo del canal.** Respuesta debajo de la cual una pieza se apaga o se rehace: email 0.3 % de clic, push 0.75 %, WhatsApp 60 % de lectura, in-app 10 %.
- **Veces (abren contra no abren).** Conversión de quienes abrieron dividida entre la de quienes no, a 7 días. Menos de 1.5 = el mensaje no cambia el resultado.
- **Lift.** Conversión con mensaje contra grupo de control. Hoy no medible; con B7 lo será.
- **Segmento maestro.** Segmento `SEG-` con dueño, reutilizado por todas las piezas de esa audiencia.
- **Exclusión global.** Segmento `EXC-` aplicado como filtro negativo a todo lo promocional.

## Anexo 1. Mínimos, estándares y metas por canal

| Canal | Indicador | Mínimo para seguir | Estándar | Hoy | Meta a 6 meses |
|---|---|---|---|---|---|
| Email | Entrega | | 95 % | 95.1 % | 97 % |
| Email | Clic sobre entregados | 0.3 % | 1.5 % | 0.92 % | 1.5 % |
| Email | Bajas por mil entregados | | 2.5 | 3.13 | 2.0 |
| Push | Apertura directa | 0.75 % | 3 % | 1.53 % | 2.5 % |
| WhatsApp | Entrega | 80 % | 90 % | 74.2 % | 90 % |
| WhatsApp | Lectura sobre entregados | 60 % | 70 % | 68.8 % | 75 % |
| In-app | Clic sobre impresiones | 10 % | 20 % | 38.2 % | mantener |
| Todos | Mensajes a canal mudo | | | 58.9 % | 30 % |
| Todos | Promocional a etapas bloqueadas | | 0 | 43.78 M en 9 meses | 0 |
| Todos | Promocional a dados de baja | | 0 | 79,994 | 0 |
| Todos | Campañas activas debajo del mínimo | | 0 | 85 | 0 |
| Todos | Envíos con ticket | | 100 % | 87.4 % | 100 % |

## Anexo 2. Dónde está cada cosa en el Sheets `braze_auditoria_v3`

| Pestaña | Qué trae | Para qué regla |
|---|---|---|
| Léeme | Qué es cada pestaña, supuestos, cambios por versión | |
| Parámetros | Costos por canal, mínimos, topes; cambiarlos recalcula todo | B2, B5, B8 |
| Verificación | 419 comprobaciones de que las fórmulas cuadran | |
| Canales | Volumen, respuesta, costo y bajas por canal y mes | C3, C4 |
| Equipos | Lo mismo por equipo | C2 |
| Campañas | Una fila por familia y canal (1,913) con señal y acción | B8, D2 |
| Catálogo | Una fila por familia (1,821): equipo, producto, ticket, audiencia, gancho, estado, versiones | A1, A11, D1 paso 2 |
| Vista_equipo | Todo lo anterior para un equipo (celda B2) | C2, D4 |
| Insights | Hallazgos con cifra, filtrables por equipo y tema | C7, C8 |
| Plan_accion | Ahorro por acción, las diez familias que más pesan, y por equipo | D2, D4 |
| Estándares | 24 indicadores con valor actual, estándar, estado y valor por equipo | C1, D4, D5 |

## Anexo 3. Supuestos y límites de las cifras

- Periodo enero a septiembre de 2026; filas deduplicadas por envío; conversión con MAX por duplicados.
- Respuesta y conversión según las definiciones del glosario; la conversión es referencia, no atribución (no hay grupo de control hoy).
- Costos: email 0.05 MXN por enviado, WhatsApp 1.00 MXN por entregado (Parámetros!B6 permite cambiar a enviado), push e in-app 0. El costo fijo de Braze no está incluido (pendiente del usuario: qué significan los 7,020 USD al mes y 32,474 créditos).
- Audiencia, gancho y tipo se infieren del nombre de la pieza; donde el nombre no sigue la convención (17 %) caen en "otros".
- Las etapas del golden dataset cubren 37 % de los envíos (6.6 % de los usuarios).
- Lectura de WhatsApp subestimada si el usuario tiene apagadas las confirmaciones de lectura.
- Las bajas solo existen para email; push y WhatsApp se dan de baja fuera de Braze.
