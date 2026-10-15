-- Queries de extracción. Correr UNA a la vez en Databricks SQL, descargar el resultado como CSV y subirlo al chat.
-- Periodo 2026-01-01 a 2026-09-30. Deduplicación según data/mapeo.md sección 11.
-- Warehouse recomendado: Medium o más grande. E1 puede tardar 10 a 20 minutos.

-- ===================== E1. Agregado por comunicación × mes × canal (base de casi todo el análisis) =====================
-- Resultado esperado: 30 mil a 50 mil filas. Descargar CSV completo como e1_comunicacion_mes_canal.csv
WITH base AS (
  -- Una fila por usuario × comunicación × día × canal. Los duplicados se colapsan con MAX.
  SELECT user_id, communication_id, event_date, category,
    MAX(communication_name) AS communication_name, MAX(team) AS team, MAX(product_service) AS product_service,
    MAX(ticket_number) AS ticket_number, MAX(`group`) AS grp,
    MAX(CAST(was_send AS INT)) AS was_send, MAX(CAST(was_opened AS INT)) AS was_opened,
    MAX(CAST(email_sent AS INT)) AS email_sent, MAX(CAST(email_delivery AS INT)) AS email_delivery,
    MAX(CAST(email_open AS INT)) AS email_open, MAX(CAST(email_click AS INT)) AS email_click,
    MAX(CAST(email_unsubscribe AS INT)) AS email_unsubscribe,
    MAX(CAST(pn_send AS INT)) AS pn_send, MAX(CAST(pn_open AS INT)) AS pn_open,
    MAX(CAST(whatsapp_send AS INT)) AS whatsapp_send, MAX(CAST(whatsapp_delivery AS INT)) AS whatsapp_delivery,
    MAX(CAST(whatsapp_read AS INT)) AS whatsapp_read,
    MAX(CAST(in_app_impression AS INT)) AS in_app_impression, MAX(CAST(in_app_click AS INT)) AS in_app_click,
    MAX(CAST(banner_impression AS INT)) AS banner_impression, MAX(CAST(banner_click AS INT)) AS banner_click,
    MAX(CAST(applied_for_loan AS INT)) AS applied, MAX(CAST(is_converted AS INT)) AS conv, MAX(gross_amount) AS monto
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
  GROUP BY user_id, communication_id, event_date, category
),
con_dia AS (
  -- Cuántas comunicaciones enviadas tocaron al usuario ese día, y si convirtió ese día (una sola vez)
  SELECT *,
    SUM(was_send) OVER (PARTITION BY user_id, event_date) AS comms_enviadas_dia,
    MAX(conv)     OVER (PARTITION BY user_id, event_date) AS conv_dia,
    MAX(monto)    OVER (PARTITION BY user_id, event_date) AS monto_dia
  FROM base
)
SELECT
  communication_id, communication_name, team, product_service, ticket_number, grp AS grupo, category AS canal,
  DATE_TRUNC('month', event_date) AS mes,
  COUNT(*)                                   AS filas_audiencia,
  SUM(was_send)                              AS envios,
  APPROX_COUNT_DISTINCT(CASE WHEN was_send = 1 THEN user_id END) AS usuarios_aprox,
  SUM(was_opened)                            AS abiertos,
  SUM(email_sent) AS email_sent, SUM(email_delivery) AS email_delivery, SUM(email_open) AS email_open,
  SUM(email_click) AS email_click, SUM(email_unsubscribe) AS email_unsubscribe,
  SUM(pn_send) AS pn_send, SUM(pn_open) AS pn_open,
  SUM(whatsapp_send) AS whatsapp_send, SUM(whatsapp_delivery) AS whatsapp_delivery, SUM(whatsapp_read) AS whatsapp_read,
  SUM(in_app_impression) AS in_app_impression, SUM(in_app_click) AS in_app_click,
  SUM(banner_impression) AS banner_impression, SUM(banner_click) AS banner_click,
  SUM(applied)                               AS solicitudes_filas,
  SUM(conv)                                  AS conversiones_filas,
  ROUND(SUM(monto), 0)                       AS monto_filas,
  -- Atribución fraccional: la conversión única del usuario-día se reparte entre las comunicaciones que le llegaron ese día
  ROUND(SUM(CASE WHEN was_send = 1 AND conv_dia = 1 THEN 1.0 / comms_enviadas_dia ELSE 0 END), 2)       AS conversiones_fraccional,
  ROUND(SUM(CASE WHEN was_send = 1 AND conv_dia = 1 THEN monto_dia / comms_enviadas_dia ELSE 0 END), 0)  AS monto_fraccional,
  -- Costo variable MXN
  ROUND(SUM(email_sent) * 0.05 + SUM(whatsapp_send) * 1.00, 2) AS costo_mxn
FROM con_dia
GROUP BY communication_id, communication_name, team, product_service, ticket_number, grp, category, DATE_TRUNC('month', event_date)
ORDER BY envios DESC;


-- ===================== E2. Catálogo limpio de campañas y Canvas =====================
-- Resultado esperado: unas 6 mil filas. Descargar como e2_catalogo.csv
WITH piezas AS (
  SELECT 'campaign' AS tipo_pieza, campaign_id AS communication_id, campaign_name AS nombre, team, product, `date` AS fecha_codigo,
         ticket_number, channel AS canal_codigo, audience, offer, `group` AS grupo, archived, first_sent, last_sent,
         campaign_created_at AS created_at, channel_email, channel_in_app_message, channel_webhook, channel_push_notification,
         channel_whatsapp, channel_banner
  FROM analytics_engineering_production.braze._dim_braze_campaign
  UNION ALL
  SELECT 'canvas', canvas_id, canvas_name, team, product, `date`, ticket_number, channel, audience, offer, `group`,
         archived, first_sent, last_sent, canvas_created_at, channel_email, channel_in_app_message, channel_webhook,
         channel_push_notification, channel_whatsapp, FALSE
  FROM analytics_engineering_production.braze._dim_braze_canvas
)
SELECT *,
  -- Equipo limpio: pruebas y copias se separan
  CASE WHEN LOWER(team) RLIKE 'qa|test|prueb|check|copy|master|configuracion|leti|marisol|sam$|bren' THEN 'QA/Test'
       WHEN team IS NULL OR team = '' THEN 'Sin equipo'
       WHEN LOWER(team) IN ('marketing','maketing','markrting','markerting','11marketing') THEN 'Marketing'
       WHEN LOWER(team) IN ('productgrowth','productogrowth','productgrowht','producto') THEN 'ProductGrowth'
       ELSE team END AS team_limpio,
  CASE WHEN ticket_number IS NULL OR ticket_number = '' OR ticket_number = 'Not Tracked' THEN 0 ELSE 1 END AS tiene_ticket,
  CASE WHEN canal_codigo RLIKE '^(E|Email|Mail|CANVAS|Canvas|CANVA|CANVASPN|CANVASM|PN|Push|PushNotification|PushiOSAndroid|IA|InApp|WA|Whatsapp|B|Banner|WH)$'
       THEN 1 ELSE 0 END AS nombre_sigue_convencion,
  CASE WHEN archived THEN 'archivada'
       WHEN last_sent >= DATE_SUB(DATE '2026-09-30', 90) THEN 'activa'
       WHEN last_sent IS NULL THEN 'nunca_enviada'
       ELSE 'zombi' END AS estado,
  DATEDIFF(last_sent, first_sent) AS dias_vida,
  CAST(channel_email AS INT) + CAST(channel_in_app_message AS INT) + CAST(channel_webhook AS INT)
    + CAST(channel_push_notification AS INT) + CAST(channel_whatsapp AS INT) + CAST(channel_banner AS INT) AS n_canales,
  CASE
    WHEN LOWER(offer) LIKE '%recordatorio%' OR LOWER(audience) LIKE '%constancia%'    THEN 'operativo'
    WHEN LOWER(offer) LIKE '%retargeting%'  OR LOWER(audience) LIKE '%retargeting%'   THEN 'retargeting'
    WHEN LOWER(offer) LIKE '%onboarding%'   OR LOWER(audience) LIKE '%onboarding%' OR LOWER(audience) LIKE '%sicompra%' THEN 'onboarding'
    WHEN LOWER(audience) LIKE '%lead%' OR LOWER(audience) LIKE '%leftfunnel%' OR LOWER(audience) LIKE '%registrad%' OR LOWER(audience) LIKE '%prospect%' THEN 'adquisicion'
    WHEN LOWER(audience) LIKE '%active%' OR LOWER(audience) LIKE '%recurrente%'       THEN 'recurrencia'
    WHEN LOWER(offer) LIKE '%tasa0%'                                                  THEN 'promocion_tasa'
    ELSE 'sin_clasificar' END AS tipo_comunicacion
FROM piezas;


-- ===================== E3. Distribución por usuario: cuántos mensajes recibe cada quién y si está suscrito =====================
-- Resultado esperado: menos de 2 mil filas. Descargar como e3_usuarios_distribucion.csv
-- Versión 2 (15 oct): agrega msgs_whatsapp_entregados y quita costo_mxn. El costo se calcula solo en el Sheets a partir de los parámetros.
WITH por_usuario AS (
  SELECT user_id,
    SUM(CASE WHEN was_send THEN 1 ELSE 0 END)                                 AS msgs,
    SUM(CASE WHEN email_sent THEN 1 ELSE 0 END)                               AS msgs_email,
    SUM(CASE WHEN pn_send THEN 1 ELSE 0 END)                                  AS msgs_push,
    SUM(CASE WHEN whatsapp_send THEN 1 ELSE 0 END)                            AS msgs_whatsapp,
    SUM(CASE WHEN whatsapp_delivery THEN 1 ELSE 0 END)                        AS msgs_whatsapp_entregados,
    SUM(CASE WHEN in_app_impression THEN 1 ELSE 0 END)                        AS msgs_inapp,
    SUM(CASE WHEN email_unsubscribe THEN 1 ELSE 0 END)                        AS bajas_email,
    APPROX_COUNT_DISTINCT(CASE WHEN was_send THEN communication_id END)       AS comms_distintas,
    APPROX_COUNT_DISTINCT(CASE WHEN was_send THEN event_date END)             AS dias_con_envio,
    APPROX_COUNT_DISTINCT(CASE WHEN is_converted THEN event_date END)         AS dias_con_conversion
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
  GROUP BY user_id
),
con_estado AS (
  SELECT p.*,
    COALESCE(CAST(u.email_subscribe AS STRING), 'desconocido') AS email_subscribe,
    COALESCE(CAST(u.push_subscribe AS STRING), 'desconocido')  AS push_subscribe,
    CASE WHEN f.customer_id IS NULL THEN 'sin_golden' ELSE COALESCE(f.step, 'sin_etapa') END AS etapa,
    COALESCE(f.mkt_contactable_channel, 'n/a') AS canal_contactable,
    CASE WHEN f.email_unsubscribed OR f.push_unsubscribed OR f.wa_unsubscribed THEN 1 ELSE 0 END AS baja_algun_canal,
    CASE WHEN f.is_arco OR f.is_blacklist OR f.charge_off_pay OR f.charge_off_cash OR f.par_60_179 THEN 1 ELSE 0 END AS no_contactable_riesgo,
    CASE WHEN p.msgs = 0 THEN '00'
         WHEN p.msgs <= 5 THEN '01-05' WHEN p.msgs <= 10 THEN '06-10' WHEN p.msgs <= 20 THEN '11-20'
         WHEN p.msgs <= 40 THEN '21-40' WHEN p.msgs <= 80 THEN '41-80' WHEN p.msgs <= 160 THEN '081-160'
         WHEN p.msgs <= 320 THEN '161-320' ELSE '321+' END AS banda_msgs
  FROM por_usuario p
  LEFT JOIN analytics_engineering_production.braze._dim_braze_users u ON u.user_id = p.user_id
  LEFT JOIN product.customer_golden_dataset.dim_braze_filters f ON f.customer_id = p.user_id
)
SELECT banda_msgs, email_subscribe, push_subscribe, etapa, canal_contactable, baja_algun_canal, no_contactable_riesgo,
  COUNT(*) AS usuarios,
  SUM(msgs) AS msgs, SUM(msgs_email) AS msgs_email, SUM(msgs_push) AS msgs_push, SUM(msgs_whatsapp) AS msgs_whatsapp, SUM(msgs_whatsapp_entregados) AS msgs_whatsapp_entregados, SUM(msgs_inapp) AS msgs_inapp,
  SUM(bajas_email) AS bajas_email,
  ROUND(AVG(comms_distintas), 1) AS comms_distintas_prom, ROUND(AVG(dias_con_envio), 1) AS dias_con_envio_prom,
  SUM(CASE WHEN dias_con_conversion > 0 THEN 1 ELSE 0 END) AS usuarios_con_conversion,
  SUM(dias_con_conversion) AS dias_con_conversion,
  PERCENTILE_APPROX(msgs, 0.5) AS msgs_p50, PERCENTILE_APPROX(msgs, 0.9) AS msgs_p90, PERCENTILE_APPROX(msgs, 0.99) AS msgs_p99, MAX(msgs) AS msgs_max
FROM con_estado
GROUP BY banda_msgs, email_subscribe, push_subscribe, etapa, canal_contactable, baja_algun_canal, no_contactable_riesgo
ORDER BY banda_msgs, usuarios DESC;


-- ===================== E4a. Serie por semana y por mes × canal (vista de tablero) =====================
-- Misma base deduplicada que E1. Trae mix, costo, entrega, apertura, lectura, clic y bajas (eventos y usuarios únicos).
-- Resultado esperado: unas 250 filas (39 semanas + 9 meses, por 5 canales). Descargar como e4a_serie_semana_mes_canal.csv
WITH base AS (
  SELECT user_id, communication_id, event_date, category,
    MAX(CAST(was_send AS INT)) AS was_send,
    MAX(CAST(email_sent AS INT)) AS email_sent, MAX(CAST(email_delivery AS INT)) AS email_delivery,
    MAX(CAST(email_open AS INT)) AS email_open, MAX(CAST(email_click AS INT)) AS email_click,
    MAX(CAST(email_unsubscribe AS INT)) AS email_unsubscribe,
    MAX(CAST(pn_send AS INT)) AS pn_send, MAX(CAST(pn_open AS INT)) AS pn_open,
    MAX(CAST(whatsapp_send AS INT)) AS whatsapp_send, MAX(CAST(whatsapp_delivery AS INT)) AS whatsapp_delivery,
    MAX(CAST(whatsapp_read AS INT)) AS whatsapp_read,
    MAX(CAST(in_app_impression AS INT)) AS in_app_impression, MAX(CAST(in_app_click AS INT)) AS in_app_click,
    MAX(CAST(banner_impression AS INT)) AS banner_impression, MAX(CAST(banner_click AS INT)) AS banner_click,
    MAX(CAST(is_converted AS INT)) AS conv
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
  GROUP BY user_id, communication_id, event_date, category
),
periodos AS (
  SELECT 'semana' AS grano, DATE_TRUNC('week', event_date) AS periodo, * FROM base
  UNION ALL
  SELECT 'mes' AS grano, DATE_TRUNC('month', event_date) AS periodo, * FROM base
)
SELECT grano, periodo, category AS canal,
  SUM(was_send)                                                        AS envios,
  APPROX_COUNT_DISTINCT(CASE WHEN was_send = 1 THEN user_id END)       AS usuarios_aprox,
  APPROX_COUNT_DISTINCT(CASE WHEN was_send = 1 THEN communication_id END) AS comunicaciones,
  SUM(email_sent) AS email_sent, SUM(email_delivery) AS email_delivery, SUM(email_open) AS email_open, SUM(email_click) AS email_click,
  SUM(email_unsubscribe)                                               AS bajas_email_eventos,
  APPROX_COUNT_DISTINCT(CASE WHEN email_unsubscribe = 1 THEN user_id END) AS bajas_email_usuarios,
  APPROX_COUNT_DISTINCT(CASE WHEN email_delivery = 1 THEN user_id END) AS usuarios_email_entregado,
  SUM(pn_send) AS pn_send, SUM(pn_open) AS pn_open,
  SUM(whatsapp_send) AS whatsapp_send, SUM(whatsapp_delivery) AS whatsapp_delivery, SUM(whatsapp_read) AS whatsapp_read,
  SUM(in_app_impression) AS in_app_impression, SUM(in_app_click) AS in_app_click,
  SUM(banner_impression) AS banner_impression, SUM(banner_click) AS banner_click,
  SUM(conv)                                                            AS conversiones_filas,
  ROUND(SUM(email_sent) * 0.05 + SUM(whatsapp_send) * 1.00, 2)         AS costo_mxn
FROM periodos
GROUP BY grano, periodo, category
ORDER BY grano, periodo, canal;


-- ===================== E4b. Concentración de mensajes por mes: usuarios por banda de mensajes =====================
-- Resultado esperado: unas 80 filas (9 meses × 9 bandas). Descargar como e4b_concentracion_mes.csv
-- Versión 2 (15 oct): agrega msgs_whatsapp_entregados y quita costo_mxn.
WITH por_usuario_mes AS (
  SELECT user_id, DATE_TRUNC('month', event_date) AS mes,
    SUM(CASE WHEN was_send THEN 1 ELSE 0 END) AS msgs,
    SUM(CASE WHEN email_sent THEN 1 ELSE 0 END) AS msgs_email,
    SUM(CASE WHEN pn_send THEN 1 ELSE 0 END) AS msgs_push,
    SUM(CASE WHEN whatsapp_send THEN 1 ELSE 0 END) AS msgs_whatsapp,
    SUM(CASE WHEN whatsapp_delivery THEN 1 ELSE 0 END) AS msgs_whatsapp_entregados,
    SUM(CASE WHEN in_app_impression THEN 1 ELSE 0 END) AS msgs_inapp,
    SUM(CASE WHEN email_unsubscribe THEN 1 ELSE 0 END) AS bajas_email
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
  GROUP BY user_id, DATE_TRUNC('month', event_date)
)
SELECT mes,
  CASE WHEN msgs = 0 THEN '00' WHEN msgs <= 5 THEN '01-05' WHEN msgs <= 10 THEN '06-10' WHEN msgs <= 20 THEN '11-20'
       WHEN msgs <= 40 THEN '21-40' WHEN msgs <= 80 THEN '41-80' WHEN msgs <= 160 THEN '081-160' ELSE '161+' END AS banda_msgs_mes,
  COUNT(*) AS usuarios,
  SUM(msgs) AS msgs, SUM(msgs_email) AS msgs_email, SUM(msgs_push) AS msgs_push, SUM(msgs_whatsapp) AS msgs_whatsapp, SUM(msgs_whatsapp_entregados) AS msgs_whatsapp_entregados, SUM(msgs_inapp) AS msgs_inapp,
  SUM(CASE WHEN bajas_email > 0 THEN 1 ELSE 0 END) AS usuarios_con_baja_email,
  PERCENTILE_APPROX(msgs, 0.5) AS msgs_p50, PERCENTILE_APPROX(msgs, 0.9) AS msgs_p90, MAX(msgs) AS msgs_max
FROM por_usuario_mes
GROUP BY mes, 2
ORDER BY mes, banda_msgs_mes;


-- ===================== E5. Cohorte de baja: usuarios que se dan de baja de email y siguen recibiendo email después =====================
-- Resultado esperado: 9 filas (una por mes de baja). Descargar como e5_cohorte_baja.csv
-- Correr también esta línea aparte y anotar el número: es el denominador del acumulado de bajas.
--   SELECT APPROX_COUNT_DISTINCT(user_id) AS usuarios_con_email FROM analytics_engineering_production.xplore._dim_braze_users_and_communications WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30' AND email_sent;
-- Nota: un usuario dado de baja puede recibir email transaccional de forma legítima. El resultado se cruza con el tipo de comunicación en el análisis.
WITH primera_baja AS (
  SELECT user_id, MIN(DATE_TRUNC('month', event_date)) AS mes_baja
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30' AND email_unsubscribe
  GROUP BY user_id
),
despues AS (
  SELECT b.user_id, b.mes_baja, DATE_TRUNC('month', t.event_date) AS mes_envio,
    SUM(CASE WHEN t.email_sent THEN 1 ELSE 0 END) AS emails,
    SUM(CASE WHEN t.email_open THEN 1 ELSE 0 END) AS abiertos,
    SUM(CASE WHEN t.email_unsubscribe THEN 1 ELSE 0 END) AS bajas_otra_vez
  FROM primera_baja b
  JOIN analytics_engineering_production.xplore._dim_braze_users_and_communications t ON t.user_id = b.user_id
  WHERE t.event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
    AND DATE_TRUNC('month', t.event_date) > b.mes_baja
  GROUP BY b.user_id, b.mes_baja, DATE_TRUNC('month', t.event_date)
)
SELECT b.mes_baja,
  COUNT(DISTINCT b.user_id)                                                                        AS usuarios_baja,
  COUNT(DISTINCT CASE WHEN d.mes_envio = ADD_MONTHS(b.mes_baja, 1) AND d.emails > 0 THEN d.user_id END) AS reciben_email_m1,
  SUM(CASE WHEN d.mes_envio = ADD_MONTHS(b.mes_baja, 1) THEN d.emails ELSE 0 END)                 AS emails_m1,
  COUNT(DISTINCT CASE WHEN d.mes_envio = ADD_MONTHS(b.mes_baja, 2) AND d.emails > 0 THEN d.user_id END) AS reciben_email_m2,
  SUM(CASE WHEN d.mes_envio = ADD_MONTHS(b.mes_baja, 2) THEN d.emails ELSE 0 END)                 AS emails_m2,
  COUNT(DISTINCT CASE WHEN d.mes_envio = ADD_MONTHS(b.mes_baja, 3) AND d.emails > 0 THEN d.user_id END) AS reciben_email_m3,
  SUM(CASE WHEN d.mes_envio = ADD_MONTHS(b.mes_baja, 3) THEN d.emails ELSE 0 END)                 AS emails_m3,
  COUNT(DISTINCT CASE WHEN d.emails > 0 THEN d.user_id END)                                       AS reciben_email_despues_total,
  SUM(COALESCE(d.emails, 0))                                                                      AS emails_despues_total,
  SUM(COALESCE(d.abiertos, 0))                                                                    AS abiertos_despues_total,
  COUNT(DISTINCT CASE WHEN d.bajas_otra_vez > 0 THEN d.user_id END)                               AS se_dan_de_baja_otra_vez
FROM primera_baja b
LEFT JOIN despues d ON d.user_id = b.user_id
GROUP BY b.mes_baja
ORDER BY b.mes_baja;


-- Nota (14 oct): en Databricks el regexp_replace con '\d' no quitó la fecha del nombre. Usar '-\\d{8}-' (doble barra) en Spark SQL.
-- ===================== E6. Solapamiento: a qué usuarios les llegan varias cosas parecidas =====================
-- Sin identificadores de usuario en el resultado. Todo sale agregado.
-- Familia = communication_name sin la fecha, para que las versiones mensuales de una Canvas cuenten como la misma idea.
-- Audiencia = quinto bloque del nombre (Leads, Recurrentes_Dormants, Nuevos_NeverActive...). Si el nombre no sigue la convención, queda 'sin_audiencia'.

-- E6a. Cuántas comunicaciones distintas recibe un usuario en un día, por mes.
-- Resultado esperado: unas 45 filas (9 meses × 5 bandas). Descargar como e6a_solape_dia_mes.csv
WITH envios AS (
  SELECT DISTINCT c.user_id, c.event_date, c.category AS canal,
    regexp_replace(c.communication_name, '-\d{8}-', '-') AS familia
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications c
  WHERE c.event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30' AND c.was_send
),
usuario_dia AS (
  SELECT user_id, event_date, DATE_TRUNC('month', event_date) AS mes,
    COUNT(DISTINCT familia) AS familias_dia, COUNT(DISTINCT canal) AS canales_dia, COUNT(*) AS msgs_dia
  FROM envios GROUP BY user_id, event_date
),
resultado_dia AS (
  SELECT user_id, event_date,
    MAX(CASE WHEN email_unsubscribe THEN 1 ELSE 0 END) AS baja_email,
    MAX(CASE WHEN is_converted THEN 1 ELSE 0 END) AS conv,
    MAX(CASE WHEN email_click OR pn_open OR whatsapp_read OR in_app_click THEN 1 ELSE 0 END) AS respondio
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
  GROUP BY user_id, event_date
)
SELECT u.mes,
  CASE WHEN u.familias_dia = 1 THEN '1' WHEN u.familias_dia = 2 THEN '2' WHEN u.familias_dia <= 4 THEN '3 a 4' WHEN u.familias_dia <= 7 THEN '5 a 7' ELSE '8+' END AS banda_familias_dia,
  COUNT(*)                                   AS usuario_dias,
  APPROX_COUNT_DISTINCT(u.user_id)           AS usuarios_aprox,
  SUM(u.msgs_dia)                            AS msgs,
  AVG(u.canales_dia)                         AS canales_prom,
  SUM(r.respondio)                           AS usuario_dias_con_respuesta,
  SUM(r.conv)                                AS usuario_dias_con_conversion,
  SUM(r.baja_email)                          AS usuario_dias_con_baja
FROM usuario_dia u LEFT JOIN resultado_dia r ON r.user_id = u.user_id AND r.event_date = u.event_date
GROUP BY 1, 2 ORDER BY 1, 2;

-- E6b. Qué pares de familias le llegan al mismo usuario el mismo día, y si son parecidas (mismo producto o misma audiencia).
-- Resultado esperado: hasta 1,000 filas. Descargar como e6b_pares_familias.csv
WITH envios AS (
  SELECT DISTINCT c.user_id, c.event_date,
    regexp_replace(c.communication_name, '-\d{8}-', '-') AS familia,
    c.category AS canal
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications c
  WHERE c.event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30' AND c.was_send
),
pares AS (
  SELECT a.user_id, a.event_date, a.familia AS familia_a, b.familia AS familia_b, a.canal AS canal_a, b.canal AS canal_b
  FROM envios a JOIN envios b ON a.user_id = b.user_id AND a.event_date = b.event_date AND a.familia < b.familia
)
SELECT familia_a, familia_b, canal_a, canal_b,
  split_part(familia_a, '-', 1) AS equipo_a, split_part(familia_b, '-', 1) AS equipo_b,
  CASE WHEN split_part(familia_a, '-', 2) = split_part(familia_b, '-', 2) THEN 1 ELSE 0 END AS mismo_producto,
  CASE WHEN split_part(familia_a, '-', 5) = split_part(familia_b, '-', 5) THEN 1 ELSE 0 END AS misma_audiencia,
  COUNT(*)                          AS usuario_dias_juntas,
  APPROX_COUNT_DISTINCT(user_id)    AS usuarios_aprox,
  COUNT(DISTINCT DATE_TRUNC('month', event_date)) AS meses
FROM pares
GROUP BY 1, 2, 3, 4, 5, 6, 7, 8
HAVING COUNT(*) >= 10000
ORDER BY usuario_dias_juntas DESC
LIMIT 1000;


-- ===================== E7. Segmentación: a quién le funciona qué =====================
-- Sin identificadores. Dos cortes: por etapa del golden record y por audiencia del nombre (E7a), y por patrón de respuesta del usuario (E7b).

-- E7a. Familia × canal × etapa del usuario: envíos, respuesta, conversión y bajas.
-- La etapa viene de product.customer_golden_dataset.dim_braze_filters (cubre ~7 % de usuarios; el resto queda en 'sin_golden').
-- Resultado esperado: 10 a 20 mil filas. Descargar como e7a_familia_canal_etapa.csv
WITH base AS (
  SELECT c.user_id, c.event_date, c.category AS canal,
    regexp_replace(c.communication_name, '-\d{8}-', '-') AS familia,
    MAX(CAST(c.was_send AS INT)) AS envio,
    MAX(CASE WHEN c.email_click OR c.pn_open OR c.whatsapp_read OR c.in_app_click THEN 1 ELSE 0 END) AS respondio,
    MAX(CAST(c.email_unsubscribe AS INT)) AS baja_email,
    MAX(CAST(c.is_converted AS INT)) AS conv,
    MAX(COALESCE(c.gross_amount, 0)) AS monto
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications c
  WHERE c.event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
  GROUP BY c.user_id, c.event_date, c.category, 4
)
SELECT b.familia, split_part(b.familia, '-', 1) AS equipo, split_part(b.familia, '-', 2) AS producto, split_part(b.familia, '-', 5) AS audiencia, b.canal,
  CASE WHEN f.customer_id IS NULL THEN 'sin_golden' ELSE COALESCE(f.step, 'sin_etapa') END AS etapa,
  SUM(b.envio)                       AS envios,
  APPROX_COUNT_DISTINCT(b.user_id)   AS usuarios_aprox,
  SUM(b.respondio)                   AS respuestas,
  SUM(b.conv)                        AS conversiones_filas,
  SUM(b.monto)                       AS monto_filas,
  SUM(b.baja_email)                  AS bajas_email_eventos
FROM base b
LEFT JOIN product.customer_golden_dataset.dim_braze_filters f ON f.customer_id = b.user_id
GROUP BY 1, 2, 3, 4, 5, 6
HAVING SUM(b.envio) >= 1000
ORDER BY envios DESC;

-- E7b. Patrón de respuesta por usuario: a qué canal responde cada quien, y cuánto le mandamos por cada canal.
-- Responder = clic en email, apertura de push, lectura de WhatsApp o clic en in-app, al menos una vez en el periodo.
-- Resultado esperado: 16 filas (una por combinación de canales a los que responde). Descargar como e7b_patron_respuesta.csv
-- Versión 2 (15 oct): agrega msgs_wa_entregados y quita costo_mxn.
WITH por_usuario AS (
  SELECT user_id,
    SUM(CASE WHEN email_sent THEN 1 ELSE 0 END)    AS msgs_email,
    SUM(CASE WHEN pn_send THEN 1 ELSE 0 END)       AS msgs_push,
    SUM(CASE WHEN whatsapp_send THEN 1 ELSE 0 END) AS msgs_wa,
    SUM(CASE WHEN whatsapp_delivery THEN 1 ELSE 0 END) AS msgs_wa_entregados,
    SUM(CASE WHEN in_app_impression THEN 1 ELSE 0 END) AS msgs_inapp,
    MAX(CASE WHEN email_click THEN 1 ELSE 0 END)   AS resp_email,
    MAX(CASE WHEN pn_open THEN 1 ELSE 0 END)       AS resp_push,
    MAX(CASE WHEN whatsapp_read THEN 1 ELSE 0 END) AS resp_wa,
    MAX(CASE WHEN in_app_click THEN 1 ELSE 0 END)  AS resp_inapp,
    MAX(CASE WHEN is_converted THEN 1 ELSE 0 END)  AS convirtio,
    MAX(CASE WHEN email_unsubscribe THEN 1 ELSE 0 END) AS baja_email
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
  GROUP BY user_id
)
SELECT resp_email, resp_push, resp_wa, resp_inapp,
  COUNT(*)            AS usuarios,
  SUM(msgs_email)     AS msgs_email, SUM(msgs_push) AS msgs_push, SUM(msgs_wa) AS msgs_wa, SUM(msgs_wa_entregados) AS msgs_wa_entregados, SUM(msgs_inapp) AS msgs_inapp,
  SUM(convirtio)      AS usuarios_con_conversion,
  SUM(baja_email)     AS usuarios_con_baja_email
FROM por_usuario
GROUP BY 1, 2, 3, 4
ORDER BY usuarios DESC;


-- ===================== E5b. Qué comunicaciones le llegan a un usuario después de darse de baja de email =====================
-- Complementa E5: 17 % de los que se dan de baja vuelven a recibir email. Esto dice cuáles son (familia, equipo, tipo) para ver si son transaccionales o promocionales.
-- Sin identificadores. Resultado esperado: 200 a 500 filas. Descargar como e5b_comms_despues_baja.csv
WITH primera_baja AS (
  SELECT user_id, MIN(event_date) AS fecha_baja
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30' AND email_unsubscribe
  GROUP BY user_id
),
despues AS (
  SELECT DISTINCT c.user_id, c.event_date, c.communication_id, c.communication_name, c.team,
    CAST(c.email_open AS INT) AS abierto, CAST(c.email_click AS INT) AS clic
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications c
  JOIN primera_baja b ON b.user_id = c.user_id
  WHERE c.event_date > b.fecha_baja AND c.event_date <= DATE '2026-09-30' AND c.email_sent
)
SELECT regexp_replace(communication_name, '-\d{8}-', '-') AS familia, MAX(team) AS equipo,
  COUNT(*)                          AS emails_despues_de_baja,
  APPROX_COUNT_DISTINCT(user_id)    AS usuarios_aprox,
  SUM(abierto)                      AS abiertos,
  SUM(clic)                         AS clics,
  COUNT(DISTINCT DATE_TRUNC('month', event_date)) AS meses
FROM despues
GROUP BY 1
HAVING COUNT(*) >= 500
ORDER BY emails_despues_de_baja DESC;


-- ===================== E7c. Convierten los que abren vs los que no abren, por familia y canal =====================
-- Es el método que ya usa el equipo para decidir si un email aporta: si los que abren convierten igual que los que no, el email no está moviendo nada.
-- Conversión = is_converted en los 7 días siguientes al envío, por usuario. Sin identificadores en el resultado.
-- Resultado esperado: 1 a 3 mil filas. Descargar como e7c_abren_vs_no_abren.csv
WITH envio AS (
  SELECT user_id, event_date, category AS canal, regexp_replace(communication_name, '-\d{8}-', '-') AS familia,
    MAX(CASE WHEN email_open OR pn_open OR whatsapp_read OR in_app_impression THEN 1 ELSE 0 END) AS abrio,
    MAX(CASE WHEN email_click OR in_app_click THEN 1 ELSE 0 END) AS clic
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30' AND was_send
  GROUP BY user_id, event_date, category, 4
),
conv AS (
  SELECT DISTINCT user_id, event_date AS fecha_conv
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-10-07' AND is_converted
),
envio_conv AS (
  SELECT e.*, MAX(CASE WHEN c.user_id IS NOT NULL THEN 1 ELSE 0 END) AS convirtio_7d
  FROM envio e
  LEFT JOIN conv c ON c.user_id = e.user_id AND c.fecha_conv BETWEEN e.event_date AND e.event_date + INTERVAL 7 DAYS
  GROUP BY ALL
)
SELECT familia, canal,
  COUNT(*)                                          AS envios_usuario_dia,
  SUM(abrio)                                        AS abrieron,
  SUM(CASE WHEN abrio = 1 THEN convirtio_7d END)    AS abrieron_y_convirtieron,
  SUM(CASE WHEN abrio = 0 THEN convirtio_7d END)    AS no_abrieron_y_convirtieron,
  SUM(clic)                                         AS hicieron_clic,
  SUM(CASE WHEN clic = 1 THEN convirtio_7d END)     AS clic_y_convirtieron
FROM envio_conv
GROUP BY familia, canal
HAVING COUNT(*) >= 10000
ORDER BY envios_usuario_dia DESC;


-- ===================== E8. Cuántos días pasan entre el primer email y la baja, y cuántos emails recibió antes =====================
-- Responde "¿en cuántos días se desuscriben?": promedio, mediana y p90 de días entre el primer email entregado y la primera baja,
-- emails y familias distintas que recibió antes de darse de baja, y qué familia le llegó el día de la baja.
-- Todo agregado, sin identificadores. Ojo: la historia empieza el 1 de enero, así que quien ya recibía email antes aparece con menos
-- días de los reales (censura por la izquierda). cohorte_limpia = 1 marca a quien recibió su primer email de febrero en adelante;
-- esa es la cifra buena para "días hasta la baja". En Spark el \d del regexp va con doble barra (\\d).
-- Resultado esperado: 4 bloques, menos de 150 filas. Descargar como e8_dias_hasta_baja.csv
-- Versión 3 (15 oct): sin subquery correlacionada. Versión 2: la primera versión pedía email_delivery en la misma fila de la baja y solo encontró 115 mil de las 457 mil bajas.
-- Ahora la fecha de baja se toma de cualquier fila con email_unsubscribe, y los emails entregados se cuentan aparte.
WITH emails AS (
  SELECT user_id, event_date, regexp_replace(communication_name, '-\\d{8}-', '-') AS familia
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30' AND category = 'email' AND email_delivery
),
bajas AS (
  SELECT user_id, MIN(event_date) AS fecha_baja
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30' AND email_unsubscribe
  GROUP BY user_id
),
usuario AS (
  SELECT e.user_id, MIN(e.event_date) AS primer_email, MAX(b.fecha_baja) AS fecha_baja
  FROM emails e JOIN bajas b ON b.user_id = e.user_id
  GROUP BY e.user_id
),
antes AS (
  SELECT e.user_id, COUNT(*) AS emails_antes, COUNT(DISTINCT e.familia) AS familias_antes
  FROM emails e JOIN usuario u ON u.user_id = e.user_id AND e.event_date <= u.fecha_baja
  GROUP BY e.user_id
),
base AS (
  SELECT u.user_id, datediff(u.fecha_baja, u.primer_email) AS dias, a.emails_antes, a.familias_antes,
         CASE WHEN u.primer_email >= DATE '2026-02-01' THEN 1 ELSE 0 END AS cohorte_limpia
  FROM usuario u JOIN antes a ON a.user_id = u.user_id
  WHERE u.fecha_baja IS NOT NULL
),
ultimo AS (
  -- fecha del último email entregado el día de la baja o antes (Spark no acepta subquery correlacionada en el JOIN)
  SELECT e.user_id, MAX(e.event_date) AS fecha_ultimo
  FROM emails e JOIN usuario u ON u.user_id = e.user_id AND e.event_date <= u.fecha_baja
  GROUP BY e.user_id
),
dia_baja AS (
  -- familia que le llegó el día de la baja o, si ese día no hubo entrega, la última que recibió antes
  SELECT b.*, e.familia
  FROM base b JOIN ultimo l ON l.user_id = b.user_id
  JOIN emails e ON e.user_id = b.user_id AND e.event_date = l.fecha_ultimo
)
SELECT 'resumen' AS bloque, 'todos' AS clave, cohorte_limpia, COUNT(*) AS usuarios,
  AVG(dias) AS dias_prom, percentile_approx(dias, 0.5) AS dias_mediana, percentile_approx(dias, 0.9) AS dias_p90,
  AVG(emails_antes) AS emails_prom, percentile_approx(emails_antes, 0.5) AS emails_mediana, AVG(familias_antes) AS familias_prom
FROM base GROUP BY cohorte_limpia
UNION ALL
SELECT 'banda_dias',
  CASE WHEN dias = 0 THEN '0 mismo día' WHEN dias <= 7 THEN '1 a 7' WHEN dias <= 30 THEN '08 a 30' WHEN dias <= 90 THEN '31 a 90'
       WHEN dias <= 180 THEN '91 a 180' ELSE '181+' END,
  cohorte_limpia, COUNT(*), AVG(dias), percentile_approx(dias, 0.5), percentile_approx(dias, 0.9),
  AVG(emails_antes), percentile_approx(emails_antes, 0.5), AVG(familias_antes)
FROM base GROUP BY 2, 3
UNION ALL
SELECT 'banda_emails',
  CASE WHEN emails_antes = 1 THEN '01' WHEN emails_antes <= 3 THEN '02 a 3' WHEN emails_antes <= 10 THEN '04 a 10'
       WHEN emails_antes <= 30 THEN '11 a 30' ELSE '31+' END,
  cohorte_limpia, COUNT(*), AVG(dias), percentile_approx(dias, 0.5), percentile_approx(dias, 0.9),
  AVG(emails_antes), percentile_approx(emails_antes, 0.5), AVG(familias_antes)
FROM base GROUP BY 2, 3
UNION ALL
SELECT 'familia_dia_baja', familia, cohorte_limpia, COUNT(*), AVG(dias), percentile_approx(dias, 0.5), percentile_approx(dias, 0.9),
  AVG(emails_antes), percentile_approx(emails_antes, 0.5), AVG(familias_antes)
FROM dia_baja GROUP BY 2, 3 HAVING COUNT(*) >= 500
ORDER BY bloque, usuarios DESC;



-- ===================== E9a. Lo mismo que E7c pero con varias ventanas: convierte en 7, 30, 90 días y hasta fin de periodo =====================
-- Para ver si la diferencia entre quienes abren y quienes no se sostiene o se desvanece al abrir la ventana. Si a 90 días convierten
-- casi igual, el mensaje adelantó una conversión que iba a pasar; si la diferencia se mantiene, sí movió algo.
-- Resultado esperado: 1 a 3 mil filas. Descargar como e9a_abren_vs_no_abren_ventanas.csv
WITH envio AS (
  SELECT user_id, event_date, category AS canal, regexp_replace(communication_name, '-\\d{8}-', '-') AS familia,
    MAX(CASE WHEN email_open OR pn_open OR whatsapp_read OR in_app_impression THEN 1 ELSE 0 END) AS abrio
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30' AND was_send
  GROUP BY user_id, event_date, category, 4
),
conv AS (
  SELECT DISTINCT user_id, event_date AS fecha_conv
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-12-29' AND is_converted
),
envio_conv AS (
  SELECT e.user_id, e.event_date, e.canal, e.familia, e.abrio,
    MAX(CASE WHEN datediff(c.fecha_conv, e.event_date) BETWEEN 0 AND 7 THEN 1 ELSE 0 END)  AS conv_7,
    MAX(CASE WHEN datediff(c.fecha_conv, e.event_date) BETWEEN 0 AND 30 THEN 1 ELSE 0 END) AS conv_30,
    MAX(CASE WHEN datediff(c.fecha_conv, e.event_date) BETWEEN 0 AND 90 THEN 1 ELSE 0 END) AS conv_90,
    MAX(CASE WHEN c.fecha_conv >= e.event_date AND c.fecha_conv <= DATE '2026-09-30' THEN 1 ELSE 0 END) AS conv_fin
  FROM envio e
  LEFT JOIN conv c ON c.user_id = e.user_id AND c.fecha_conv BETWEEN e.event_date AND e.event_date + INTERVAL 90 DAYS
  GROUP BY e.user_id, e.event_date, e.canal, e.familia, e.abrio
)
SELECT familia, canal, COUNT(*) AS envios_usuario_dia, SUM(abrio) AS abrieron,
  SUM(CASE WHEN abrio = 1 THEN conv_7 END)   AS ab_conv_7,   SUM(CASE WHEN abrio = 0 THEN conv_7 END)   AS no_conv_7,
  SUM(CASE WHEN abrio = 1 THEN conv_30 END)  AS ab_conv_30,  SUM(CASE WHEN abrio = 0 THEN conv_30 END)  AS no_conv_30,
  SUM(CASE WHEN abrio = 1 THEN conv_90 END)  AS ab_conv_90,  SUM(CASE WHEN abrio = 0 THEN conv_90 END)  AS no_conv_90,
  SUM(CASE WHEN abrio = 1 THEN conv_fin END) AS ab_conv_fin, SUM(CASE WHEN abrio = 0 THEN conv_fin END) AS no_conv_fin
FROM envio_conv
GROUP BY familia, canal
HAVING COUNT(*) >= 10000
ORDER BY envios_usuario_dia DESC;


-- ===================== E9b. Lo mismo que E7b pero con ventana: a qué canal respondió en los últimos 90 días (julio a septiembre) =====================
-- En E7b "respondió" era alguna vez en 9 meses. Aquí se mide sobre julio a septiembre: quién respondió a qué canal en esos 90 días,
-- y cuánto se le mandó por cada canal en esos mismos 90 días. Da la versión fina de "canal mudo".
-- Resultado esperado: 16 filas. Descargar como e9b_patron_respuesta_90d.csv
-- Versión 2 (15 oct): misma definición que E7b (email responde = clic; la versión 1 usaba apertura por error), agrega msgs_wa_entregados y quita costo_mxn. Solo cambia la ventana de fechas.
WITH por_usuario AS (
  SELECT user_id,
    SUM(CASE WHEN email_sent THEN 1 ELSE 0 END)    AS msgs_email,
    SUM(CASE WHEN pn_send THEN 1 ELSE 0 END)       AS msgs_push,
    SUM(CASE WHEN whatsapp_send THEN 1 ELSE 0 END) AS msgs_wa,
    SUM(CASE WHEN whatsapp_delivery THEN 1 ELSE 0 END) AS msgs_wa_entregados,
    SUM(CASE WHEN in_app_impression THEN 1 ELSE 0 END) AS msgs_inapp,
    MAX(CASE WHEN email_click THEN 1 ELSE 0 END)   AS resp_email,
    MAX(CASE WHEN pn_open THEN 1 ELSE 0 END)       AS resp_push,
    MAX(CASE WHEN whatsapp_read THEN 1 ELSE 0 END) AS resp_wa,
    MAX(CASE WHEN in_app_click THEN 1 ELSE 0 END)  AS resp_inapp,
    MAX(CASE WHEN is_converted THEN 1 ELSE 0 END)  AS convirtio,
    MAX(CASE WHEN email_unsubscribe THEN 1 ELSE 0 END) AS baja_email
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE event_date BETWEEN DATE '2026-07-01' AND DATE '2026-09-30'
  GROUP BY user_id
)
SELECT resp_email, resp_push, resp_wa, resp_inapp,
  COUNT(*)            AS usuarios,
  SUM(msgs_email)     AS msgs_email, SUM(msgs_push) AS msgs_push, SUM(msgs_wa) AS msgs_wa, SUM(msgs_wa_entregados) AS msgs_wa_entregados, SUM(msgs_inapp) AS msgs_inapp,
  SUM(convirtio)      AS usuarios_con_conversion,
  SUM(baja_email)     AS usuarios_con_baja_email
FROM por_usuario
GROUP BY 1, 2, 3, 4
ORDER BY usuarios DESC;


-- ===================== E10. Día de la semana × canal × equipo (para la parte "cuándo" del playbook) =====================
-- La tabla solo trae fecha, no hora: se puede día de la semana, no hora del día.
-- Resultado esperado: 7 × 5 canales × ~11 equipos = unas 400 filas. Descargar como e10_dia_semana.csv
WITH base AS (
  SELECT user_id, communication_id, event_date, category AS canal, MAX(team) AS team,
    MAX(CAST(was_send AS INT)) AS envio,
    MAX(CASE WHEN email_click OR pn_open OR whatsapp_read OR in_app_click THEN 1 ELSE 0 END) AS respondio,
    MAX(CAST(email_delivery AS INT)) AS email_entregado, MAX(CAST(whatsapp_delivery AS INT)) AS wa_entregado,
    MAX(CAST(email_unsubscribe AS INT)) AS baja_email,
    MAX(CAST(is_converted AS INT)) AS conv
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
  GROUP BY user_id, communication_id, event_date, category
)
SELECT dayofweek(event_date) AS dia_semana_num, date_format(event_date, 'EEEE') AS dia_semana, canal, team,
  SUM(envio)                        AS envios,
  APPROX_COUNT_DISTINCT(user_id)    AS usuarios_aprox,
  COUNT(DISTINCT communication_id)  AS comunicaciones,
  SUM(email_entregado)              AS email_entregados,
  SUM(wa_entregado)                 AS wa_entregados,
  SUM(respondio)                    AS respuestas,
  SUM(baja_email)                   AS bajas_email_eventos,
  SUM(conv)                         AS conversiones_filas
FROM base
GROUP BY 1, 2, 3, 4
ORDER BY 1, 3, envios DESC;


-- ===================== E11. Inventario de segmentación: qué valores de segment, subsegment y group se usan y cuánto pesan =====================
-- Para medir si la segmentación está repetida (muchos nombres para la misma audiencia) y cuánto volumen lleva cada una.
-- Las columnas segment, subsegment y group son las de la tabla de hechos (ver data/mapeo.md sección 10). Si alguna no existe con ese nombre, quitarla del SELECT y del GROUP BY.
-- Resultado esperado: 500 a 5,000 filas. Descargar como e11_segmentacion.csv
WITH base AS (
  SELECT user_id, communication_id, event_date, category AS canal,
    MAX(segment) AS segment, MAX(subsegment) AS subsegment, MAX(`group`) AS grp, MAX(team) AS team,
    MAX(regexp_replace(communication_name, '-\d{8}-', '-')) AS familia,
    MAX(CAST(was_send AS INT)) AS envio,
    MAX(CASE WHEN email_click OR pn_open OR whatsapp_read OR in_app_click THEN 1 ELSE 0 END) AS respondio,
    MAX(CAST(email_unsubscribe AS INT)) AS baja_email,
    MAX(CAST(is_converted AS INT)) AS conv
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
  GROUP BY user_id, communication_id, event_date, category
)
SELECT COALESCE(segment, 'null') AS segment, COALESCE(subsegment, 'null') AS subsegment, COALESCE(grp, 'null') AS grupo, team, canal,
  COUNT(DISTINCT communication_id) AS comunicaciones,
  COUNT(DISTINCT familia)          AS familias,
  SUM(envio)                       AS envios,
  APPROX_COUNT_DISTINCT(user_id)   AS usuarios_aprox,
  SUM(respondio)                   AS respuestas,
  SUM(baja_email)                  AS bajas_email_eventos,
  SUM(conv)                        AS conversiones_filas
FROM base
GROUP BY 1, 2, 3, 4, 5
HAVING SUM(envio) >= 1000
ORDER BY envios DESC;


-- ===================== E12. Antigüedad del usuario en Braze × canal: a quién le funciona cada canal según cuánto lleva en la base =====================
-- Antigüedad al momento del envío = days_on_book (días en la base al día de hoy) menos los días que han pasado desde el envío. _dim_braze_users no trae fecha de alta, solo days_on_book.
-- Resultado esperado: 7 bandas × 5 canales × 2 (suscrito o no) = unas 70 filas. Descargar como e12_antiguedad.csv
WITH base AS (
  SELECT c.user_id, c.communication_id, c.event_date, c.category AS canal,
    MAX(CAST(c.was_send AS INT)) AS envio,
    MAX(CASE WHEN c.email_click OR c.pn_open OR c.whatsapp_read OR c.in_app_click THEN 1 ELSE 0 END) AS respondio,
    MAX(CAST(c.email_unsubscribe AS INT)) AS baja_email,
    MAX(CAST(c.is_converted AS INT)) AS conv
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications c
  WHERE c.event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
  GROUP BY c.user_id, c.communication_id, c.event_date, c.category
),
con_alta AS (
  SELECT b.*, (u.days_on_book - datediff(current_date(), b.event_date)) / 30.4 AS meses_en_base, u.email_subscribe
  FROM base b LEFT JOIN analytics_engineering_production.braze._dim_braze_users u ON u.user_id = b.user_id
)
SELECT
  CASE WHEN meses_en_base IS NULL THEN 'sin_alta'
       WHEN meses_en_base < 0 THEN '0. alta después del envío (revisar)'
       WHEN meses_en_base < 1 THEN '0. menos de 1 mes'
       WHEN meses_en_base < 3 THEN '1. 1 a 3 meses'
       WHEN meses_en_base < 6 THEN '2. 3 a 6 meses'
       WHEN meses_en_base < 12 THEN '3. 6 a 12 meses'
       WHEN meses_en_base < 24 THEN '4. 1 a 2 años'
       ELSE '5. más de 2 años' END AS banda_antiguedad,
  canal, COALESCE(CAST(email_subscribe AS STRING), 'null') AS email_subscribe,
  SUM(envio)                      AS envios,
  APPROX_COUNT_DISTINCT(user_id)  AS usuarios_aprox,
  SUM(respondio)                  AS respuestas,
  SUM(baja_email)                 AS bajas_email_eventos,
  SUM(conv)                       AS conversiones_filas
FROM con_alta
GROUP BY 1, 2, 3
ORDER BY 1, 2, 3;


-- ===================== E13. Lift contra grupo de control, por Canvas =====================
-- La única medida de cuánto vende Braze de verdad. Usa in_control_group de la tabla de Canvas (la columna control_group de la tabla
-- de hechos no sirve: vale "Lead" en el 99.99 % de las filas, ver data/mapeo.md sección 11).
-- Grano: un usuario cuenta una vez por Canvas y grupo (test o control). Si solicitó o convirtió en cualquier fila, cuenta como que sí.
-- Lift = tasa_test - tasa_control. Se calcula en el Sheets. Solo vale si control tiene 1,000 usuarios o más.
-- Resultado esperado: una fila por Canvas y grupo, menos de 2,000 filas. Descargar como e13_lift_control.csv
WITH por_usuario AS (
  SELECT canvas_id, user_id,
    CASE WHEN in_control_group = TRUE THEN 'control' ELSE 'test' END AS grupo,
    MAX(canvas_name) AS canvas_name, MAX(team) AS team, MAX(product) AS product,
    MAX(audience) AS audience, MAX(offer) AS offer, MAX(ticket_number) AS ticket_number,
    MIN(event_date) AS primer_dia, MAX(event_date) AS ultimo_dia,
    MAX(CAST(was_opened AS INT))      AS abrio,
    MAX(CAST(applied_for_loan AS INT)) AS solicito,
    MAX(CAST(is_converted AS INT))     AS convirtio,
    MAX(gross_amount)                  AS monto
  FROM analytics_engineering_production.braze_semantic_layer._fct_braze_canvas_user_engagement
  WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
  GROUP BY canvas_id, user_id, CASE WHEN in_control_group = TRUE THEN 'control' ELSE 'test' END
)
SELECT canvas_id, canvas_name, team, product, audience, offer, ticket_number, grupo,
  MIN(primer_dia)            AS primer_dia,
  MAX(ultimo_dia)            AS ultimo_dia,
  COUNT(*)                   AS usuarios,
  SUM(abrio)                 AS usuarios_abrieron,
  SUM(solicito)              AS usuarios_solicitaron,
  SUM(convirtio)             AS usuarios_convirtieron,
  ROUND(SUM(monto), 0)       AS monto,
  ROUND(SUM(solicito) * 100.0 / COUNT(*), 3)  AS pct_solicitud,
  ROUND(SUM(convirtio) * 100.0 / COUNT(*), 3) AS pct_conversion
FROM por_usuario
GROUP BY canvas_id, canvas_name, team, product, audience, offer, ticket_number, grupo
ORDER BY canvas_name, grupo;


-- ===================== E14. Experimentos A/B dentro de Canvas: qué variante gana =====================
-- experiment_split_name y canvas_variation_name vienen de la tabla de Canvas. Un Canvas sin experimento trae una sola variante.
-- Grano: un usuario cuenta una vez por Canvas, experimento y variante.
-- Resultado esperado: menos de 3,000 filas. Descargar como e14_experimentos.csv
WITH por_usuario AS (
  SELECT canvas_id, user_id,
    COALESCE(experiment_split_name, 'sin_experimento') AS experimento,
    COALESCE(canvas_variation_name, 'sin_variante')   AS variante,
    CASE WHEN in_control_group = TRUE THEN 'control' ELSE 'test' END AS grupo,
    MAX(canvas_name) AS canvas_name, MAX(team) AS team, MAX(product) AS product,
    MAX(CAST(was_opened AS INT))       AS abrio,
    MAX(CAST(applied_for_loan AS INT)) AS solicito,
    MAX(CAST(is_converted AS INT))     AS convirtio,
    MAX(gross_amount)                  AS monto
  FROM analytics_engineering_production.braze_semantic_layer._fct_braze_canvas_user_engagement
  WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
  GROUP BY canvas_id, user_id, COALESCE(experiment_split_name, 'sin_experimento'), COALESCE(canvas_variation_name, 'sin_variante'),
           CASE WHEN in_control_group = TRUE THEN 'control' ELSE 'test' END
)
SELECT canvas_id, canvas_name, team, product, experimento, variante, grupo,
  COUNT(*)              AS usuarios,
  SUM(abrio)            AS usuarios_abrieron,
  SUM(solicito)         AS usuarios_solicitaron,
  SUM(convirtio)        AS usuarios_convirtieron,
  ROUND(SUM(monto), 0)  AS monto,
  ROUND(SUM(abrio) * 100.0 / COUNT(*), 2)     AS pct_abrio,
  ROUND(SUM(solicito) * 100.0 / COUNT(*), 3)  AS pct_solicitud,
  ROUND(SUM(convirtio) * 100.0 / COUNT(*), 3) AS pct_conversion
FROM por_usuario
GROUP BY canvas_id, canvas_name, team, product, experimento, variante, grupo
ORDER BY canvas_name, experimento, variante, grupo;


-- ===================== E15. Embudo por paso de Canvas: en qué toque se cae la gente =====================
-- Un usuario cuenta una vez por paso y canal. El orden del paso se aproxima por la fecha en que ese paso se creó.
-- Sirve para confirmar la regla de 2 toques y para ver qué pasos nunca se abren.
-- Resultado esperado: pasos × canal, 2,000 a 6,000 filas. Descargar como e15_embudo_pasos.csv
WITH por_usuario AS (
  SELECT e.canvas_id, e.canvas_step_id, e.category AS canal, e.user_id,
    MAX(e.canvas_name) AS canvas_name, MAX(e.canvas_step_name) AS canvas_step_name,
    MAX(e.team) AS team, MAX(e.product) AS product,
    MAX(CAST(e.was_opened AS INT))       AS abrio,
    MAX(CAST(e.applied_for_loan AS INT)) AS solicito,
    MAX(CAST(e.is_converted AS INT))     AS convirtio
  FROM analytics_engineering_production.braze_semantic_layer._fct_braze_canvas_user_engagement e
  WHERE e.event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
    AND (e.in_control_group IS NULL OR e.in_control_group = FALSE)
  GROUP BY e.canvas_id, e.canvas_step_id, e.category, e.user_id
),
pasos AS (
  SELECT canvas_step_id, canvas_step_created_at, first_sent AS paso_primer_envio, last_sent AS paso_ultimo_envio,
    ROW_NUMBER() OVER (PARTITION BY canvas_id ORDER BY canvas_step_created_at, canvas_step_name) AS orden_aprox
  FROM analytics_engineering_production.braze._dim_braze_canvas_step
)
SELECT u.canvas_id, u.canvas_name, u.team, u.product, u.canvas_step_id, u.canvas_step_name, p.orden_aprox, u.canal,
  p.paso_primer_envio, p.paso_ultimo_envio,
  COUNT(*)          AS usuarios,
  SUM(u.abrio)      AS usuarios_abrieron,
  SUM(u.solicito)   AS usuarios_solicitaron,
  SUM(u.convirtio)  AS usuarios_convirtieron,
  ROUND(SUM(u.abrio) * 100.0 / COUNT(*), 2)     AS pct_abrio,
  ROUND(SUM(u.convirtio) * 100.0 / COUNT(*), 3) AS pct_conversion
FROM por_usuario u
LEFT JOIN pasos p ON p.canvas_step_id = u.canvas_step_id
GROUP BY u.canvas_id, u.canvas_name, u.team, u.product, u.canvas_step_id, u.canvas_step_name, p.orden_aprox, u.canal,
         p.paso_primer_envio, p.paso_ultimo_envio
ORDER BY u.canvas_name, p.orden_aprox, u.canal;


-- ===================== E16. Mensajes a usuarios que nunca respondieron en todo el periodo (lo que se paga en MAU sin retorno) =====================
-- Primero se clasifica a cada usuario con todo el periodo: ¿respondió alguna vez en algún canal? ¿convirtió alguna vez?
-- Después se cuenta, mes por mes, cuántos mensajes y cuánto costo variable fue a cada grupo.
-- Braze cobra por usuario activo al mes; un usuario al que se le manda cuenta aunque nunca responda. Esto dimensiona ese costo.
-- Resultado esperado: 9 meses × 2 × 2 × 5 canales = unas 180 filas. Descargar como e16_sin_respuesta.csv
WITH base AS (
  SELECT user_id, communication_id, event_date, category AS canal,
    MAX(CAST(was_send AS INT)) AS envio,
    MAX(CASE WHEN email_open OR email_click OR pn_open OR whatsapp_read OR in_app_click OR banner_click THEN 1 ELSE 0 END) AS respondio,
    MAX(CAST(email_sent AS INT)) AS email_sent, MAX(CAST(whatsapp_send AS INT)) AS whatsapp_send,
    MAX(CAST(email_unsubscribe AS INT)) AS baja_email,
    MAX(CAST(is_converted AS INT)) AS conv
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
  GROUP BY user_id, communication_id, event_date, category
),
perfil AS (
  SELECT user_id,
    MAX(respondio) AS respondio_alguna_vez,
    MAX(conv)      AS convirtio_alguna_vez,
    SUM(envio)     AS envios_periodo
  FROM base GROUP BY user_id
)
SELECT DATE_TRUNC('month', b.event_date) AS mes, b.canal,
  p.respondio_alguna_vez, p.convirtio_alguna_vez,
  CASE WHEN p.envios_periodo <= 5 THEN '1. 1 a 5' WHEN p.envios_periodo <= 20 THEN '2. 6 a 20'
       WHEN p.envios_periodo <= 80 THEN '3. 21 a 80' ELSE '4. más de 80' END AS banda_msgs_periodo,
  APPROX_COUNT_DISTINCT(CASE WHEN b.envio = 1 THEN b.user_id END) AS usuarios_aprox,
  SUM(b.envio)                                                   AS envios,
  SUM(b.baja_email)                                              AS bajas_email_eventos,
  ROUND(SUM(b.email_sent) * 0.05 + SUM(b.whatsapp_send) * 1.00, 2) AS costo_mxn
FROM base b JOIN perfil p ON p.user_id = b.user_id
GROUP BY 1, 2, 3, 4, 5
ORDER BY 1, 2, 3, 4, 5;


-- ===================== E17. Canal contactable (golden dataset) contra canal por el que de verdad se le escribió =====================
-- Solo cubre el 6.6 % de usuarios que están en el golden dataset (clientes). Mide cuántos push van a gente marcada "Only Email",
-- cuántos WhatsApp a wa_unsubscribed, cuántos push a quien desinstaló la app, etc.
-- Resultado esperado: menos de 1,000 filas. Descargar como e17_contactable.csv
WITH base AS (
  SELECT user_id, communication_id, event_date, category AS canal, MAX(team) AS team,
    MAX(CAST(was_send AS INT)) AS envio,
    MAX(CASE WHEN email_click OR pn_open OR whatsapp_read OR in_app_click THEN 1 ELSE 0 END) AS respondio,
    MAX(CAST(email_unsubscribe AS INT)) AS baja_email,
    MAX(CAST(email_sent AS INT)) AS email_sent, MAX(CAST(whatsapp_send AS INT)) AS whatsapp_send,
    MAX(CAST(is_converted AS INT)) AS conv
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
  GROUP BY user_id, communication_id, event_date, category
)
SELECT b.canal, b.team,
  COALESCE(f.mkt_contactable_channel, 'sin_golden') AS canal_contactable,
  f.step AS etapa,
  CAST(f.email_unsubscribed AS STRING) AS email_unsubscribed,
  CAST(f.push_unsubscribed AS STRING)  AS push_unsubscribed,
  CAST(f.wa_unsubscribed AS STRING)    AS wa_unsubscribed,
  CAST(f.with_app AS STRING)           AS with_app,
  CAST(f.app_uninstall AS STRING)      AS app_uninstall,
  CAST(f.notifications_enabled AS STRING) AS notifications_enabled,
  SUM(b.envio)                       AS envios,
  APPROX_COUNT_DISTINCT(b.user_id)   AS usuarios_aprox,
  SUM(b.respondio)                   AS respuestas,
  SUM(b.baja_email)                  AS bajas_email_eventos,
  SUM(b.conv)                        AS conversiones_filas,
  ROUND(SUM(b.email_sent) * 0.05 + SUM(b.whatsapp_send) * 1.00, 2) AS costo_mxn
FROM base b
LEFT JOIN product.customer_golden_dataset.dim_braze_filters f ON f.customer_id = b.user_id
WHERE f.customer_id IS NOT NULL
GROUP BY 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
HAVING SUM(b.envio) >= 100
ORDER BY envios DESC;


-- ===================== E18. Dispositivos: iOS contra Android =====================
-- _dim_braze_device trae platform, device_model y os_version pero no trae user_id. Sin llave no se puede cruzar con envíos.
-- E18a da el mix de dispositivos por sí solo. E18b busca en el catálogo qué tabla tiene device_id junto con un user_id,
-- para armar el cruce. Si E18b encuentra una, se escribe E18c (push por plataforma).

-- E18a. Mix de plataforma y versión. Resultado esperado: menos de 500 filas. Descargar como e18a_dispositivos.csv
SELECT lower(platform) AS plataforma,
  split_part(os_version, '.', 1) AS os_version_mayor,
  device_model,
  COUNT(*) AS dispositivos
FROM analytics_engineering_production.braze._dim_braze_device
GROUP BY 1, 2, 3
ORDER BY dispositivos DESC;

-- E18b. ¿Dónde más existe device_id o platform? (Unity Catalog). Resultado esperado: decenas de filas. Descargar como e18b_llave_dispositivo.csv
-- Si system.information_schema no está permitido, cambiar por analytics_engineering_production.information_schema.columns
SELECT table_catalog, table_schema, table_name, column_name
FROM system.information_schema.columns
WHERE lower(column_name) IN ('device_id', 'platform', 'device_os', 'os', 'app_platform', 'push_platform')
  AND table_catalog IN ('analytics_engineering_production', 'product', 'braze', 'braze_raw', 'raw')
ORDER BY 1, 2, 3, 4;
