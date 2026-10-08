-- UNA sola query con todas las verificaciones. Databricks SQL. Pegar completa, correr, copiar la tabla de resultado.
-- Columnas: verificacion | clave | n1 | n2 | n3 | n4. Qué significa cada n está en el comentario de cada bloque.
WITH t AS (
  SELECT * FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
),
dup AS (
  SELECT user_id, communication_id, event_date, category, COUNT(*) AS n,
    COUNT(DISTINCT CONCAT_WS('|', CAST(email_sent AS STRING), CAST(email_delivery AS STRING), CAST(email_open AS STRING),
      CAST(email_click AS STRING), CAST(email_unsubscribe AS STRING), CAST(in_app_impression AS STRING), CAST(in_app_click AS STRING),
      CAST(banner_impression AS STRING), CAST(banner_click AS STRING), CAST(pn_send AS STRING), CAST(pn_open AS STRING),
      CAST(whatsapp_send AS STRING), CAST(whatsapp_delivery AS STRING), CAST(whatsapp_read AS STRING), CAST(was_send AS STRING),
      CAST(was_opened AS STRING), CAST(applied_for_loan AS STRING), CAST(is_converted AS STRING), CAST(gross_amount AS STRING),
      COALESCE(control_group,''), COALESCE(segment,''), COALESCE(subsegment,''), COALESCE(team,''), COALESCE(`group`,''),
      COALESCE(ticket_number,''), COALESCE(communication_name,''), COALESCE(product_service,''))) AS versiones,
    COUNT(DISTINCT segment) ds, COUNT(DISTINCT subsegment) dss, COUNT(DISTINCT team) dt, COUNT(DISTINCT `group`) dg,
    COUNT(DISTINCT ticket_number) dtk, COUNT(DISTINCT control_group) dcg, COUNT(DISTINCT communication_name) dcn,
    COUNT(DISTINCT product_service) dps, COUNT(DISTINCT channel) dch,
    COUNT(DISTINCT CAST(was_send AS INT)) dws, COUNT(DISTINCT CAST(email_sent AS INT)) des, COUNT(DISTINCT CAST(email_delivery AS INT)) ded,
    COUNT(DISTINCT CAST(email_open AS INT)) deo, COUNT(DISTINCT CAST(email_click AS INT)) dec, COUNT(DISTINCT CAST(pn_send AS INT)) dpn,
    COUNT(DISTINCT CAST(whatsapp_send AS INT)) dwa, COUNT(DISTINCT CAST(in_app_impression AS INT)) dia,
    COUNT(DISTINCT CAST(applied_for_loan AS INT)) dap, COUNT(DISTINCT CAST(is_converted AS INT)) dic, COUNT(DISTINCT gross_amount) dga
  FROM t GROUP BY 1,2,3,4 HAVING COUNT(*) > 1
)
-- V13 totales del periodo: n1 filas, n2 usuarios, n3 comunicaciones, n4 filas con envio
SELECT 'V13_totales' verificacion, 'periodo' clave, CAST(COUNT(*) AS DOUBLE) n1, CAST(COUNT(DISTINCT user_id) AS DOUBLE) n2,
       CAST(COUNT(DISTINCT communication_id) AS DOUBLE) n3, CAST(SUM(CASE WHEN was_send THEN 1 ELSE 0 END) AS DOUBLE) n4 FROM t
UNION ALL
-- V1 cruce de ids: n1 usuarios con envios, n2 cruzan con golden dataset, n3 porcentaje
SELECT 'V1_cruce_ids', 'user_id=customer_id', COUNT(DISTINCT t.user_id), COUNT(DISTINCT f.customer_id),
       ROUND(100.0 * COUNT(DISTINCT f.customer_id) / COUNT(DISTINCT t.user_id), 1), NULL
FROM t LEFT JOIN product.customer_golden_dataset.dim_braze_filters f ON f.customer_id = t.user_id
UNION ALL
-- V2 las dos tablas de canvas: n1 filas, n2 usuarios, n3 conversiones, n4 monto
SELECT 'V2_tablas_canvas', 'xplore', COUNT(*), COUNT(DISTINCT user_id), SUM(CASE WHEN is_converted THEN 1 ELSE 0 END), SUM(gross_amount)
FROM analytics_engineering_production.xplore._fct_braze_canvas_user_engagement
UNION ALL
SELECT 'V2_tablas_canvas', 'semantic_layer', COUNT(*), COUNT(DISTINCT user_id), SUM(CASE WHEN is_converted THEN 1 ELSE 0 END), SUM(gross_amount)
FROM analytics_engineering_production.braze_semantic_layer._fct_braze_canvas_user_engagement
UNION ALL
-- V3 valores de control_group: n1 filas, n2 envios, n3 conversiones, n4 % conversion
SELECT 'V3_control_group', COALESCE(control_group,'NULL'), COUNT(*), SUM(CASE WHEN was_send THEN 1 ELSE 0 END),
       SUM(CASE WHEN is_converted THEN 1 ELSE 0 END), ROUND(100.0 * SUM(CASE WHEN is_converted THEN 1 ELSE 0 END) / COUNT(*), 3)
FROM t GROUP BY control_group
UNION ALL
-- V3b in_control_group en canvas: n1 filas, n2 conversiones, n3 % conversion
SELECT 'V3b_in_control_group', COALESCE(CAST(in_control_group AS STRING),'NULL'), COUNT(*),
       SUM(CASE WHEN is_converted THEN 1 ELSE 0 END), ROUND(100.0 * SUM(CASE WHEN is_converted THEN 1 ELSE 0 END) / COUNT(*), 3), NULL
FROM analytics_engineering_production.braze_semantic_layer._fct_braze_canvas_user_engagement
WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30' GROUP BY in_control_group
UNION ALL
-- V4 conversiones segun was_send: n1 filas, n2 conversiones, n3 solicitudes
SELECT 'V4_conv_por_was_send', CAST(was_send AS STRING), COUNT(*), SUM(CASE WHEN is_converted THEN 1 ELSE 0 END),
       SUM(CASE WHEN applied_for_loan THEN 1 ELSE 0 END), NULL FROM t GROUP BY was_send
UNION ALL
-- V5 repeticion de conversion mismo usuario y dia: clave = filas con conversion ese dia, n1 casos
SELECT 'V5_conv_repetida_dia', CAST(repeticiones AS STRING), COUNT(*), NULL, NULL, NULL FROM (
  SELECT user_id, event_date, COUNT(*) repeticiones FROM t WHERE is_converted GROUP BY 1,2) x GROUP BY repeticiones
UNION ALL
-- V5b dias distintos con conversion por usuario: clave = dias, n1 usuarios
SELECT 'V5b_dias_conv_por_usuario', CAST(dias AS STRING), COUNT(*), NULL, NULL, NULL FROM (
  SELECT user_id, COUNT(DISTINCT event_date) dias FROM t WHERE is_converted GROUP BY 1) x GROUP BY dias
UNION ALL
-- V6 canal y categoria: n1 filas, n2 envios
SELECT 'V6_canal_categoria', CONCAT(COALESCE(channel,'NULL'), ' / ', COALESCE(category,'NULL')), COUNT(*),
       SUM(CASE WHEN was_send THEN 1 ELSE 0 END), NULL, NULL FROM t GROUP BY channel, category
UNION ALL
-- V6a codigos de canal en los catalogos: n1 piezas
SELECT 'V6a_codigo_canal_catalogo', CONCAT('campaign / ', COALESCE(channel,'NULL')), COUNT(*), NULL, NULL, NULL
FROM analytics_engineering_production.braze._dim_braze_campaign GROUP BY channel
UNION ALL
SELECT 'V6a_codigo_canal_catalogo', CONCAT('canvas / ', COALESCE(channel,'NULL')), COUNT(*), NULL, NULL, NULL
FROM analytics_engineering_production.braze._dim_braze_canvas GROUP BY channel
UNION ALL
-- V6b consistencia de was_send: n1 filas con was_send sin bandera de canal, n2 filas con bandera de canal sin was_send
SELECT 'V6b_consistencia_was_send', 'ambos deben ser 0',
       SUM(CASE WHEN was_send AND NOT (email_sent OR pn_send OR whatsapp_send OR in_app_impression OR banner_impression) THEN 1 ELSE 0 END),
       SUM(CASE WHEN NOT was_send AND (email_sent OR pn_send OR whatsapp_send OR in_app_impression OR banner_impression) THEN 1 ELSE 0 END),
       NULL, NULL FROM t
UNION ALL
-- V7 prefijo de ticket por equipo: n1 piezas
SELECT 'V7_ticket_vs_team', CONCAT(SUBSTR(ticket_number,1,1), ' / ', COALESCE(team,'NULL')), COUNT(*), NULL, NULL, NULL FROM (
  SELECT ticket_number, team FROM analytics_engineering_production.braze._dim_braze_campaign
  UNION ALL SELECT ticket_number, team FROM analytics_engineering_production.braze._dim_braze_canvas) x
GROUP BY SUBSTR(ticket_number,1,1), team
UNION ALL
-- V8 gross_amount segun conversion: clave = is_converted / applied, n1 filas, n2 con monto, n3 monto promedio, n4 monto maximo
SELECT 'V8_gross_amount', CONCAT('conv=', CAST(is_converted AS STRING), ' / applied=', CAST(applied_for_loan AS STRING)),
       COUNT(*), SUM(CASE WHEN gross_amount IS NOT NULL THEN 1 ELSE 0 END), ROUND(AVG(gross_amount),2), MAX(gross_amount)
FROM t GROUP BY is_converted, applied_for_loan
UNION ALL
-- V9 cobertura por mes (incluye octubre): n1 filas, n2 envios, n3 usuarios
SELECT 'V9_cobertura_mes', CAST(DATE_TRUNC('month', event_date) AS STRING), COUNT(*), SUM(CASE WHEN was_send THEN 1 ELSE 0 END),
       COUNT(DISTINCT user_id), NULL
FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
WHERE event_date >= DATE '2026-01-01' GROUP BY DATE_TRUNC('month', event_date)
UNION ALL
-- V10b duplicados identicos o distintos: n1 grupos, n2 filas extra
SELECT 'V10b_duplicados_tipo', CASE WHEN versiones = 1 THEN 'identicas' ELSE 'difieren' END, COUNT(*), SUM(n - 1), NULL, NULL
FROM dup GROUP BY CASE WHEN versiones = 1 THEN 'identicas' ELSE 'difieren' END
UNION ALL
-- V10c en que columna difieren los duplicados: n1 grupos donde esa columna tiene mas de un valor
SELECT 'V10c_columna_que_varia', col, CAST(v AS DOUBLE), NULL, NULL, NULL FROM (
  SELECT
    SUM(CASE WHEN ds>1 THEN 1 ELSE 0 END) segment, SUM(CASE WHEN dss>1 THEN 1 ELSE 0 END) subsegment,
    SUM(CASE WHEN dt>1 THEN 1 ELSE 0 END) team, SUM(CASE WHEN dg>1 THEN 1 ELSE 0 END) grp,
    SUM(CASE WHEN dtk>1 THEN 1 ELSE 0 END) ticket, SUM(CASE WHEN dcg>1 THEN 1 ELSE 0 END) control_group,
    SUM(CASE WHEN dcn>1 THEN 1 ELSE 0 END) communication_name, SUM(CASE WHEN dps>1 THEN 1 ELSE 0 END) product_service,
    SUM(CASE WHEN dch>1 THEN 1 ELSE 0 END) channel, SUM(CASE WHEN dws>1 THEN 1 ELSE 0 END) was_send,
    SUM(CASE WHEN des>1 THEN 1 ELSE 0 END) email_sent, SUM(CASE WHEN ded>1 THEN 1 ELSE 0 END) email_delivery,
    SUM(CASE WHEN deo>1 THEN 1 ELSE 0 END) email_open, SUM(CASE WHEN dec>1 THEN 1 ELSE 0 END) email_click,
    SUM(CASE WHEN dpn>1 THEN 1 ELSE 0 END) pn_send, SUM(CASE WHEN dwa>1 THEN 1 ELSE 0 END) whatsapp_send,
    SUM(CASE WHEN dia>1 THEN 1 ELSE 0 END) in_app_impression, SUM(CASE WHEN dap>1 THEN 1 ELSE 0 END) applied_for_loan,
    SUM(CASE WHEN dic>1 THEN 1 ELSE 0 END) is_converted, SUM(CASE WHEN dga>1 THEN 1 ELSE 0 END) gross_amount
  FROM dup
) w LATERAL VIEW stack(20,
  'segment', segment, 'subsegment', subsegment, 'team', team, 'group', grp, 'ticket', ticket, 'control_group', control_group,
  'communication_name', communication_name, 'product_service', product_service, 'channel', channel, 'was_send', was_send,
  'email_sent', email_sent, 'email_delivery', email_delivery, 'email_open', email_open, 'email_click', email_click,
  'pn_send', pn_send, 'whatsapp_send', whatsapp_send, 'in_app_impression', in_app_impression,
  'applied_for_loan', applied_for_loan, 'is_converted', is_converted, 'gross_amount', gross_amount) s AS col, v
UNION ALL
-- V10d filas por grupo duplicado: clave = filas en el grupo, n1 grupos
SELECT 'V10d_filas_por_grupo', LPAD(CAST(n AS STRING), 3, '0'), COUNT(*), NULL, NULL, NULL FROM dup GROUP BY n
ORDER BY verificacion, clave;
