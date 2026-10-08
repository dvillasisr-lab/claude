-- Databricks notebook source
-- MAGIC %md
-- MAGIC # Vistas base de la auditoría de Braze
-- MAGIC Dialecto: Databricks SQL con Unity Catalog.
-- MAGIC Son vistas TEMPORALES: viven solo en la sesión del notebook. Así no choca Unity Catalog con Hive Metastore.
-- MAGIC Si quieres vistas permanentes, pide un esquema propio en Unity Catalog (ej. `analytics_engineering_production.sandbox_braze`) y cambia `TEMPORARY VIEW v_x` por `VIEW catalogo.esquema.v_x`.
-- MAGIC Definiciones: braze-analysis/METRICAS.md y data/mapeo.md.
-- MAGIC
-- MAGIC Nota sobre duplicados: la verificación V10 encontró 1.97 millones de grupos repetidos en el grano usuario x comunicación x día x canal.
-- MAGIC v_envios los colapsa con MAX por bandera. Eso es correcto si son copias o eventos de la misma pieza; se revisa con V10b y V10c.

-- COMMAND ----------

-- ---------------------------------------------------------------
-- 1. Dimensión de piezas: campañas y Canvas en una sola tabla
-- ---------------------------------------------------------------
CREATE OR REPLACE TEMPORARY VIEW v_piezas AS
WITH base AS (
  SELECT
    'campaign'            AS tipo_pieza,
    campaign_id           AS communication_id,
    campaign_name         AS nombre,
    team, product, `date` AS fecha_codigo, ticket_number,
    channel               AS canal_codigo,
    audience, offer, `group` AS grupo,
    archived, first_sent, last_sent,
    campaign_created_at   AS created_at,
    channel_email, channel_in_app_message, channel_webhook,
    channel_push_notification, channel_whatsapp, channel_banner
  FROM analytics_engineering_production.braze._dim_braze_campaign
  UNION ALL
  SELECT
    'canvas', canvas_id, canvas_name,
    team, product, `date`, ticket_number,
    channel, audience, offer, `group`,
    archived, first_sent, last_sent, canvas_created_at,
    channel_email, channel_in_app_message, channel_webhook,
    channel_push_notification, channel_whatsapp, FALSE
  FROM analytics_engineering_production.braze._dim_braze_canvas
)
SELECT
  b.*,
  -- Tipo de comunicación según la regla de data/mapeo.md sección 4
  CASE
    WHEN LOWER(offer) LIKE '%recordatorio%' OR LOWER(audience) LIKE '%constancia%'      THEN 'operativo'
    WHEN LOWER(offer) LIKE '%retargeting%'  OR LOWER(audience) LIKE '%retargeting%'     THEN 'retargeting'
    WHEN LOWER(offer) LIKE '%onboarding%'   OR LOWER(audience) LIKE '%onboarding%'
      OR LOWER(audience) LIKE '%sicompra%'                                              THEN 'onboarding'
    WHEN LOWER(audience) LIKE '%lead%' OR LOWER(audience) LIKE '%leftfunnel%'
      OR LOWER(audience) LIKE '%registrad%' OR LOWER(audience) LIKE '%prospect%'        THEN 'adquisicion'
    WHEN LOWER(audience) LIKE '%active%' OR LOWER(audience) LIKE '%recurrente%'         THEN 'recurrencia'
    WHEN LOWER(offer) LIKE '%tasa0%'                                                    THEN 'promocion_tasa'
    ELSE 'sin_clasificar'
  END AS tipo_comunicacion,
  -- Estado operativo
  CASE
    WHEN archived THEN 'archivada'
    WHEN last_sent >= DATE_SUB(DATE '2026-09-30', 90) THEN 'activa'
    ELSE 'zombi'
  END AS estado,
  DATEDIFF(last_sent, first_sent) AS dias_vida,
  CAST(channel_email AS INT) + CAST(channel_in_app_message AS INT) + CAST(channel_webhook AS INT)
    + CAST(channel_push_notification AS INT) + CAST(channel_whatsapp AS INT) + CAST(channel_banner AS INT)
    AS n_canales,
  SUBSTR(ticket_number, 1, 1) AS ticket_prefijo
FROM base b;

-- COMMAND ----------

-- ---------------------------------------------------------------
-- 2. Hecho de envíos: una fila por usuario x comunicación x día x canal
--    Deduplicado. Con costo variable por fila.
-- ---------------------------------------------------------------
CREATE OR REPLACE TEMPORARY VIEW v_envios AS
WITH dedup AS (
  SELECT
    user_id, communication_id, communication_name, channel, category,
    product_service, ticket_number, `group` AS grupo, team, segment, subsegment,
    event_date,
    MAX(CAST(email_sent AS INT))          AS email_sent,
    MAX(CAST(email_delivery AS INT))      AS email_delivery,
    MAX(CAST(email_open AS INT))          AS email_open,
    MAX(CAST(email_click AS INT))         AS email_click,
    MAX(CAST(email_unsubscribe AS INT))   AS email_unsubscribe,
    MAX(CAST(in_app_impression AS INT))   AS in_app_impression,
    MAX(CAST(in_app_click AS INT))        AS in_app_click,
    MAX(CAST(banner_impression AS INT))   AS banner_impression,
    MAX(CAST(banner_click AS INT))        AS banner_click,
    MAX(CAST(pn_send AS INT))             AS pn_send,
    MAX(CAST(pn_open AS INT))             AS pn_open,
    MAX(CAST(whatsapp_send AS INT))       AS whatsapp_send,
    MAX(CAST(whatsapp_delivery AS INT))   AS whatsapp_delivery,
    MAX(CAST(whatsapp_read AS INT))       AS whatsapp_read,
    MAX(CAST(was_send AS INT))            AS was_send,
    MAX(CAST(was_opened AS INT))          AS was_opened,
    MAX(CAST(applied_for_loan AS INT))    AS applied_for_loan,
    MAX(CAST(is_converted AS INT))        AS is_converted,
    MAX(gross_amount)                     AS gross_amount,
    MAX(control_group)                    AS control_group
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-10-07'
  GROUP BY user_id, communication_id, communication_name, channel, category,
           product_service, ticket_number, `group`, team, segment, subsegment, event_date
)
SELECT
  d.*,
  DATE_TRUNC('month', d.event_date) AS mes,
  DATE_TRUNC('week',  d.event_date) AS semana,
  CASE WHEN d.event_date <= DATE '2026-09-30' THEN 1 ELSE 0 END AS en_periodo,
  p.tipo_pieza, p.tipo_comunicacion, p.audience, p.offer, p.product, p.estado,
  -- Costo variable MXN (parametros.sql)
  d.email_sent * 0.05 + d.whatsapp_send * 1.00 AS costo_mxn
FROM dedup d
LEFT JOIN v_piezas p ON p.communication_id = d.communication_id;

-- COMMAND ----------

-- ---------------------------------------------------------------
-- 3. Dimensión de usuarios: Braze + filtros de contactabilidad
-- ---------------------------------------------------------------
CREATE OR REPLACE TEMPORARY VIEW v_usuarios AS
SELECT
  u.user_id, u.braze_id, u.days_on_book, u.timezone,
  u.attributed_campaign, u.attributed_source,
  u.email_subscribe, u.push_subscribe,
  f.email_unsubscribed, f.push_unsubscribed, f.wa_unsubscribed,
  f.mkt_contactable_channel, f.step AS etapa,
  f.is_blacklist, f.is_arco, f.cc_freeze, f.is_reus,
  f.charge_off_pay, f.charge_off_cash, f.par_60_179,
  f.app_uninstall, f.with_app, f.notifications_enabled,
  -- Bandera única: no debería recibir marketing
  CASE WHEN f.is_blacklist OR f.is_arco OR f.charge_off_pay OR f.charge_off_cash OR f.par_60_179
       THEN 1 ELSE 0 END AS no_contactable_riesgo,
  CASE WHEN f.customer_id IS NULL THEN 0 ELSE 1 END AS cruza_con_filtros
FROM analytics_engineering_production.braze._dim_braze_users u
LEFT JOIN product.customer_golden_dataset.dim_braze_filters f ON f.customer_id = u.user_id;

-- COMMAND ----------

-- ---------------------------------------------------------------
-- 4. Hecho de pasos de Canvas con experimentos y grupo control
-- ---------------------------------------------------------------
CREATE OR REPLACE TEMPORARY VIEW v_canvas_pasos AS
SELECT
  e.user_id, e.canvas_id, e.canvas_step_id, e.category AS canal,
  e.event_date, DATE_TRUNC('month', e.event_date) AS mes,
  e.was_opened, e.team, e.product, e.audience, e.offer,
  e.canvas_name, e.canvas_step_name,
  e.experiment_split_name, e.in_control_group,
  e.canvas_variation_id, e.canvas_variation_name,
  e.applied_for_loan, e.is_converted, e.gross_amount,
  s.first_sent AS paso_first_sent, s.last_sent AS paso_last_sent
FROM analytics_engineering_production.braze_semantic_layer._fct_braze_canvas_user_engagement e
LEFT JOIN analytics_engineering_production.braze._dim_braze_canvas_step s ON s.canvas_step_id = e.canvas_step_id
WHERE e.event_date BETWEEN DATE '2026-01-01' AND DATE '2026-10-07';

-- COMMAND ----------

-- ---------------------------------------------------------------
-- 5. Resumen por usuario (lente H). Una fila por usuario.
-- ---------------------------------------------------------------
CREATE OR REPLACE TEMPORARY VIEW v_usuarios_resumen AS
WITH env AS (
  SELECT
    user_id,
    SUM(was_send)                                   AS msgs_total,
    SUM(email_sent)                                 AS msgs_email,
    SUM(pn_send)                                    AS msgs_push,
    SUM(whatsapp_send)                              AS msgs_whatsapp,
    SUM(in_app_impression)                          AS msgs_inapp,
    SUM(banner_impression)                          AS msgs_banner,
    SUM(CASE WHEN tipo_comunicacion='adquisicion'    THEN was_send ELSE 0 END) AS msgs_adquisicion,
    SUM(CASE WHEN tipo_comunicacion='onboarding'     THEN was_send ELSE 0 END) AS msgs_onboarding,
    SUM(CASE WHEN tipo_comunicacion='retargeting'    THEN was_send ELSE 0 END) AS msgs_retargeting,
    SUM(CASE WHEN tipo_comunicacion='recurrencia'    THEN was_send ELSE 0 END) AS msgs_recurrencia,
    SUM(CASE WHEN tipo_comunicacion='operativo'      THEN was_send ELSE 0 END) AS msgs_operativo,
    SUM(CASE WHEN tipo_comunicacion='promocion_tasa' THEN was_send ELSE 0 END) AS msgs_promocion_tasa,
    COUNT(DISTINCT communication_id)                AS comunicaciones_distintas,
    MIN(CASE WHEN was_send=1 THEN event_date END)   AS primer_envio,
    MAX(CASE WHEN was_send=1 THEN event_date END)   AS ultimo_envio,
    SUM(was_opened)                                 AS opens,
    SUM(email_click + in_app_click + banner_click)  AS clicks,
    SUM(applied_for_loan)                           AS solicitudes_filas,
    SUM(is_converted)                               AS conversiones_filas,
    MIN(CASE WHEN email_unsubscribe=1 THEN event_date END) AS fecha_baja_email,
    SUM(costo_mxn)                                  AS costo_mxn
  FROM v_envios
  WHERE en_periodo = 1
  GROUP BY user_id
),
conv AS (
  -- Conversiones deduplicadas por usuario y día (decisión 5)
  SELECT user_id,
         COUNT(DISTINCT CASE WHEN is_converted=1 THEN event_date END) AS conversiones_dias,
         SUM(monto_dia) AS monto_colocado
  FROM (
    SELECT user_id, event_date, MAX(CASE WHEN is_converted=1 THEN gross_amount END) AS monto_dia
    FROM v_envios WHERE en_periodo = 1 GROUP BY user_id, event_date
  ) t GROUP BY user_id
),
post_baja AS (
  SELECT e.user_id, SUM(e.email_sent) AS emails_despues_de_baja
  FROM v_envios e
  JOIN (SELECT user_id, MIN(event_date) AS fecha_baja FROM v_envios WHERE email_unsubscribe=1 GROUP BY user_id) b
    ON b.user_id = e.user_id AND e.event_date > b.fecha_baja
  WHERE e.tipo_comunicacion <> 'operativo'
  GROUP BY e.user_id
)
SELECT
  u.user_id, u.days_on_book, u.etapa, u.mkt_contactable_channel,
  u.email_subscribe, u.push_subscribe,
  u.email_unsubscribed, u.push_unsubscribed, u.wa_unsubscribed,
  u.no_contactable_riesgo, u.is_arco, u.is_blacklist,
  COALESCE(e.msgs_total,0) AS msgs_total,
  ROUND(COALESCE(e.msgs_total,0) / 39.0, 2) AS msgs_por_semana,   -- 39 semanas entre 1 ene y 30 sep 2026
  e.msgs_email, e.msgs_push, e.msgs_whatsapp, e.msgs_inapp, e.msgs_banner,
  e.msgs_adquisicion, e.msgs_onboarding, e.msgs_retargeting, e.msgs_recurrencia, e.msgs_operativo, e.msgs_promocion_tasa,
  e.comunicaciones_distintas, e.primer_envio, e.ultimo_envio,
  e.opens, e.clicks, e.solicitudes_filas,
  c.conversiones_dias, c.monto_colocado,
  e.fecha_baja_email, COALESCE(pb.emails_despues_de_baja,0) AS emails_despues_de_baja,
  e.costo_mxn
FROM v_usuarios u
LEFT JOIN env e  ON e.user_id = u.user_id
LEFT JOIN conv c ON c.user_id = u.user_id
LEFT JOIN post_baja pb ON pb.user_id = u.user_id;

-- COMMAND ----------

-- ---------------------------------------------------------------
-- 6. Conteos de control. Correr después de crear las vistas.
-- ---------------------------------------------------------------
-- SELECT COUNT(*) filas, SUM(was_send) envios, SUM(costo_mxn) costo FROM v_envios WHERE en_periodo=1;
-- SELECT category, SUM(was_send) FROM v_envios WHERE en_periodo=1 GROUP BY 1 ORDER BY 2 DESC;
-- SELECT mes, SUM(was_send) FROM v_envios GROUP BY 1 ORDER BY 1;
-- SELECT team, SUM(was_send) FROM v_envios WHERE en_periodo=1 GROUP BY 1 ORDER BY 2 DESC;
