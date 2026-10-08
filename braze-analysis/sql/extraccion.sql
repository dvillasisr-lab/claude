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
