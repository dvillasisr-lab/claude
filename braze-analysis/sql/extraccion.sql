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
WITH por_usuario AS (
  SELECT user_id,
    SUM(CASE WHEN was_send THEN 1 ELSE 0 END)                                 AS msgs,
    SUM(CASE WHEN email_sent THEN 1 ELSE 0 END)                               AS msgs_email,
    SUM(CASE WHEN pn_send THEN 1 ELSE 0 END)                                  AS msgs_push,
    SUM(CASE WHEN whatsapp_send THEN 1 ELSE 0 END)                            AS msgs_whatsapp,
    SUM(CASE WHEN in_app_impression THEN 1 ELSE 0 END)                        AS msgs_inapp,
    SUM(CASE WHEN email_unsubscribe THEN 1 ELSE 0 END)                        AS bajas_email,
    APPROX_COUNT_DISTINCT(CASE WHEN was_send THEN communication_id END)       AS comms_distintas,
    APPROX_COUNT_DISTINCT(CASE WHEN was_send THEN event_date END)             AS dias_con_envio,
    APPROX_COUNT_DISTINCT(CASE WHEN is_converted THEN event_date END)         AS dias_con_conversion,
    SUM(CASE WHEN whatsapp_send THEN 1.00 ELSE 0 END) + SUM(CASE WHEN email_sent THEN 0.05 ELSE 0 END) AS costo_mxn
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
  SUM(msgs) AS msgs, SUM(msgs_email) AS msgs_email, SUM(msgs_push) AS msgs_push, SUM(msgs_whatsapp) AS msgs_whatsapp, SUM(msgs_inapp) AS msgs_inapp,
  SUM(bajas_email) AS bajas_email,
  ROUND(AVG(comms_distintas), 1) AS comms_distintas_prom, ROUND(AVG(dias_con_envio), 1) AS dias_con_envio_prom,
  SUM(CASE WHEN dias_con_conversion > 0 THEN 1 ELSE 0 END) AS usuarios_con_conversion,
  SUM(dias_con_conversion) AS dias_con_conversion,
  ROUND(SUM(costo_mxn), 0) AS costo_mxn,
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
WITH por_usuario_mes AS (
  SELECT user_id, DATE_TRUNC('month', event_date) AS mes,
    SUM(CASE WHEN was_send THEN 1 ELSE 0 END) AS msgs,
    SUM(CASE WHEN email_sent THEN 1 ELSE 0 END) AS msgs_email,
    SUM(CASE WHEN pn_send THEN 1 ELSE 0 END) AS msgs_push,
    SUM(CASE WHEN whatsapp_send THEN 1 ELSE 0 END) AS msgs_whatsapp,
    SUM(CASE WHEN in_app_impression THEN 1 ELSE 0 END) AS msgs_inapp,
    SUM(CASE WHEN email_unsubscribe THEN 1 ELSE 0 END) AS bajas_email,
    SUM(CASE WHEN whatsapp_send THEN 1.00 ELSE 0 END) + SUM(CASE WHEN email_sent THEN 0.05 ELSE 0 END) AS costo_mxn
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
  GROUP BY user_id, DATE_TRUNC('month', event_date)
)
SELECT mes,
  CASE WHEN msgs = 0 THEN '00' WHEN msgs <= 5 THEN '01-05' WHEN msgs <= 10 THEN '06-10' WHEN msgs <= 20 THEN '11-20'
       WHEN msgs <= 40 THEN '21-40' WHEN msgs <= 80 THEN '41-80' WHEN msgs <= 160 THEN '081-160' ELSE '161+' END AS banda_msgs_mes,
  COUNT(*) AS usuarios,
  SUM(msgs) AS msgs, SUM(msgs_email) AS msgs_email, SUM(msgs_push) AS msgs_push, SUM(msgs_whatsapp) AS msgs_whatsapp, SUM(msgs_inapp) AS msgs_inapp,
  SUM(CASE WHEN bajas_email > 0 THEN 1 ELSE 0 END) AS usuarios_con_baja_email,
  ROUND(SUM(costo_mxn), 0) AS costo_mxn,
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
WITH por_usuario AS (
  SELECT user_id,
    SUM(CASE WHEN email_sent THEN 1 ELSE 0 END)    AS msgs_email,
    SUM(CASE WHEN pn_send THEN 1 ELSE 0 END)       AS msgs_push,
    SUM(CASE WHEN whatsapp_send THEN 1 ELSE 0 END) AS msgs_wa,
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
  SUM(msgs_email)     AS msgs_email, SUM(msgs_push) AS msgs_push, SUM(msgs_wa) AS msgs_wa, SUM(msgs_inapp) AS msgs_inapp,
  SUM(convirtio)      AS usuarios_con_conversion,
  SUM(baja_email)     AS usuarios_con_baja_email,
  ROUND(SUM(msgs_email) * 0.05 + SUM(msgs_wa) * 1.00, 2) AS costo_mxn
FROM por_usuario
GROUP BY 1, 2, 3, 4
ORDER BY usuarios DESC;
