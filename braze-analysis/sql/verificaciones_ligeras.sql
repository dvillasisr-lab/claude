-- Verificaciones ligeras. 4 queries, correr UNA a la vez. Cada una debe tardar de segundos a pocos minutos.
-- Databricks SQL. Periodo 2026-01-01 a 2026-09-30.

-- ===================== Q1. Básicos en una sola pasada =====================
-- Responde V3 (control_group), V4 (was_send), V6 (canal), V8 (monto), V9 (mes), V13 (total), V6b (consistencia)
SELECT
  CASE WHEN GROUPING(control_group) = 0 THEN 'V3_control_group'
       WHEN GROUPING(was_send) = 0      THEN 'V4_was_send'
       WHEN GROUPING(channel) = 0       THEN 'V6_canal_categoria'
       WHEN GROUPING(mes) = 0           THEN 'V9_mes'
       ELSE 'V13_total' END AS verificacion,
  CASE WHEN GROUPING(control_group) = 0 THEN COALESCE(control_group, 'NULL')
       WHEN GROUPING(was_send) = 0      THEN CAST(was_send AS STRING)
       WHEN GROUPING(channel) = 0       THEN CONCAT(COALESCE(channel,'NULL'), ' / ', COALESCE(category,'NULL'))
       WHEN GROUPING(mes) = 0           THEN CAST(mes AS STRING)
       ELSE 'total' END AS clave,
  COUNT(*)                                                   AS filas,
  APPROX_COUNT_DISTINCT(user_id)                             AS usuarios_aprox,
  SUM(CASE WHEN was_send THEN 1 ELSE 0 END)                  AS envios,
  SUM(CASE WHEN applied_for_loan THEN 1 ELSE 0 END)          AS solicitudes,
  SUM(CASE WHEN is_converted THEN 1 ELSE 0 END)              AS conversiones,
  SUM(CASE WHEN gross_amount IS NOT NULL THEN 1 ELSE 0 END)  AS filas_con_monto,
  SUM(CASE WHEN gross_amount IS NOT NULL AND NOT is_converted THEN 1 ELSE 0 END) AS monto_sin_conversion,
  ROUND(SUM(gross_amount), 0)                                AS monto_total,
  SUM(CASE WHEN was_send AND NOT (email_sent OR pn_send OR whatsapp_send OR in_app_impression OR banner_impression) THEN 1 ELSE 0 END) AS send_sin_canal,
  SUM(CASE WHEN NOT was_send AND (email_sent OR pn_send OR whatsapp_send OR in_app_impression OR banner_impression) THEN 1 ELSE 0 END) AS canal_sin_send
FROM (
  SELECT *, DATE_TRUNC('month', event_date) AS mes
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
)
GROUP BY GROUPING SETS ((control_group), (was_send), (channel, category), (mes), ())
ORDER BY verificacion, clave;


-- ===================== Q2. Conversiones repetidas (solo filas convertidas, es rápida) =====================
WITH c AS (
  SELECT user_id, event_date, COUNT(*) AS n
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE is_converted AND event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
  GROUP BY user_id, event_date
)
SELECT 'V5_filas_con_conv_mismo_usuario_y_dia' AS verificacion, LPAD(CAST(n AS STRING), 3, '0') AS clave, COUNT(*) AS casos FROM c GROUP BY n
UNION ALL
SELECT 'V5b_dias_con_conv_por_usuario', LPAD(CAST(d AS STRING), 3, '0'), COUNT(*)
FROM (SELECT user_id, COUNT(*) AS d FROM c GROUP BY user_id) x GROUP BY d
ORDER BY verificacion, clave;


-- ===================== Q3. Duplicados: muestra del 1 % de usuarios =====================
-- Una sola fila de resultado. Las proporciones son representativas del total.
WITH s AS (
  SELECT * FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
    AND ABS(HASH(user_id)) % 100 = 0
),
g AS (
  SELECT user_id, communication_id, event_date, category, COUNT(*) AS n,
    COUNT(DISTINCT CONCAT_WS('|', CAST(was_send AS STRING), CAST(email_sent AS STRING), CAST(email_delivery AS STRING),
      CAST(email_open AS STRING), CAST(email_click AS STRING), CAST(pn_send AS STRING), CAST(pn_open AS STRING),
      CAST(whatsapp_send AS STRING), CAST(in_app_impression AS STRING), CAST(applied_for_loan AS STRING),
      CAST(is_converted AS STRING), CAST(gross_amount AS STRING), COALESCE(control_group,''), COALESCE(segment,''),
      COALESCE(subsegment,''), COALESCE(communication_name,''), COALESCE(ticket_number,''), COALESCE(team,''))) AS versiones,
    COUNT(DISTINCT segment) ds, COUNT(DISTINCT subsegment) dss, COUNT(DISTINCT communication_name) dcn,
    COUNT(DISTINCT ticket_number) dtk, COUNT(DISTINCT control_group) dcg, COUNT(DISTINCT team) dt,
    COUNT(DISTINCT was_send) dws, COUNT(DISTINCT email_sent) des, COUNT(DISTINCT email_open) deo,
    COUNT(DISTINCT email_click) dec, COUNT(DISTINCT pn_send) dpn, COUNT(DISTINCT whatsapp_send) dwa,
    COUNT(DISTINCT is_converted) dic, COUNT(DISTINCT gross_amount) dga
  FROM s GROUP BY user_id, communication_id, event_date, category
)
SELECT
  (SELECT COUNT(*) FROM s)                           AS filas_muestra,
  COUNT(*)                                           AS grupos_totales,
  SUM(CASE WHEN n > 1 THEN 1 ELSE 0 END)             AS grupos_duplicados,
  SUM(CASE WHEN n > 1 THEN n - 1 ELSE 0 END)         AS filas_extra,
  SUM(CASE WHEN n > 1 AND versiones = 1 THEN 1 ELSE 0 END) AS dup_identicos,
  SUM(CASE WHEN n > 1 AND versiones > 1 THEN 1 ELSE 0 END) AS dup_difieren,
  SUM(CASE WHEN ds > 1  THEN 1 ELSE 0 END) AS varia_segment,
  SUM(CASE WHEN dss > 1 THEN 1 ELSE 0 END) AS varia_subsegment,
  SUM(CASE WHEN dcn > 1 THEN 1 ELSE 0 END) AS varia_communication_name,
  SUM(CASE WHEN dtk > 1 THEN 1 ELSE 0 END) AS varia_ticket,
  SUM(CASE WHEN dcg > 1 THEN 1 ELSE 0 END) AS varia_control_group,
  SUM(CASE WHEN dt > 1  THEN 1 ELSE 0 END) AS varia_team,
  SUM(CASE WHEN dws > 1 THEN 1 ELSE 0 END) AS varia_was_send,
  SUM(CASE WHEN des > 1 THEN 1 ELSE 0 END) AS varia_email_sent,
  SUM(CASE WHEN deo > 1 THEN 1 ELSE 0 END) AS varia_email_open,
  SUM(CASE WHEN dec > 1 THEN 1 ELSE 0 END) AS varia_email_click,
  SUM(CASE WHEN dpn > 1 THEN 1 ELSE 0 END) AS varia_pn_send,
  SUM(CASE WHEN dwa > 1 THEN 1 ELSE 0 END) AS varia_whatsapp_send,
  SUM(CASE WHEN dic > 1 THEN 1 ELSE 0 END) AS varia_is_converted,
  SUM(CASE WHEN dga > 1 THEN 1 ELSE 0 END) AS varia_gross_amount,
  MAX(n) AS max_filas_en_un_grupo
FROM g;


-- ===================== Q4. Catálogos, cruce de ids (muestra) y tablas de Canvas =====================
SELECT 'V6a_canal_catalogo' AS verificacion, CONCAT('campaign / ', COALESCE(channel,'NULL')) AS clave, COUNT(*) AS n1, NULL AS n2, NULL AS n3
FROM analytics_engineering_production.braze._dim_braze_campaign GROUP BY channel
UNION ALL
SELECT 'V6a_canal_catalogo', CONCAT('canvas / ', COALESCE(channel,'NULL')), COUNT(*), NULL, NULL
FROM analytics_engineering_production.braze._dim_braze_canvas GROUP BY channel
UNION ALL
SELECT 'V7_ticket_vs_team', CONCAT(SUBSTR(ticket_number,1,1), ' / ', COALESCE(team,'NULL')), COUNT(*), NULL, NULL
FROM (SELECT ticket_number, team FROM analytics_engineering_production.braze._dim_braze_campaign
      UNION ALL SELECT ticket_number, team FROM analytics_engineering_production.braze._dim_braze_canvas) x
GROUP BY SUBSTR(ticket_number,1,1), team
UNION ALL
-- V1 cruce de ids sobre muestra del 1 %: n1 usuarios muestra, n2 cruzan, n3 porcentaje
SELECT 'V1_cruce_ids_muestra', 'user_id=customer_id', COUNT(*), SUM(CASE WHEN f.customer_id IS NOT NULL THEN 1 ELSE 0 END),
       ROUND(100.0 * SUM(CASE WHEN f.customer_id IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 1)
FROM (SELECT DISTINCT user_id FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
      WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30' AND ABS(HASH(user_id)) % 100 = 0) u
LEFT JOIN product.customer_golden_dataset.dim_braze_filters f ON f.customer_id = u.user_id
UNION ALL
-- V2 las dos tablas de Canvas: n1 filas, n2 conversiones, n3 monto
SELECT 'V2_tablas_canvas', 'xplore', COUNT(*), SUM(CASE WHEN is_converted THEN 1 ELSE 0 END), ROUND(SUM(gross_amount),0)
FROM analytics_engineering_production.xplore._fct_braze_canvas_user_engagement
UNION ALL
SELECT 'V2_tablas_canvas', 'semantic_layer', COUNT(*), SUM(CASE WHEN is_converted THEN 1 ELSE 0 END), ROUND(SUM(gross_amount),0)
FROM analytics_engineering_production.braze_semantic_layer._fct_braze_canvas_user_engagement
UNION ALL
-- V3b grupo control en Canvas: n1 filas, n2 conversiones
SELECT 'V3b_in_control_group', COALESCE(CAST(in_control_group AS STRING),'NULL'), COUNT(*), SUM(CASE WHEN is_converted THEN 1 ELSE 0 END), NULL
FROM analytics_engineering_production.braze_semantic_layer._fct_braze_canvas_user_engagement
WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30' GROUP BY in_control_group
ORDER BY verificacion, clave;
