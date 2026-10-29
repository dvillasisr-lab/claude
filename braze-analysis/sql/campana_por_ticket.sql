-- Databricks notebook source
-- MAGIC %md
-- MAGIC # Toda la data de una campaña por su ticket
-- MAGIC Dialecto: Databricks SQL con Unity Catalog. Cada celda es una query independiente; córrelas en orden.
-- MAGIC
-- MAGIC **Cómo usarlo:** reemplaza `B0625` por el ticket que quieras (buscar y reemplazar en todo el archivo) y, si hace falta, las fechas `2026-01-01` y `2026-10-31`.
-- MAGIC Una comunicación entra si su campo de ticket es ese ticket **o** si el ticket aparece en el nombre (`-B0625-`), porque muchas tienen el ticket solo en el nombre.
-- MAGIC
-- MAGIC Reglas, iguales a la auditoría (sql/extraccion.sql):
-- MAGIC - La tabla de envíos trae duplicados por usuario × comunicación × día × canal; se colapsan con MAX.
-- MAGIC - Costo: correo 0.05 MXN por enviado, WhatsApp 1.00 MXN por entregado, push e in-app sin costo.
-- MAGIC - Conversión = crédito otorgado (`is_converted`) el día del mensaje. "Fraccional" reparte esa conversión entre todas las comunicaciones que le llegaron a la persona ese día, para no contarla dos veces.
-- MAGIC - La lectura de WhatsApp se registra el día que se lee: para septiembre, sumar las lecturas de octubre.

-- COMMAND ----------

-- 1a. Catálogo: campañas sueltas del ticket, con todos sus campos
SELECT c.*
FROM analytics_engineering_production.braze._dim_braze_campaign c
WHERE c.ticket_number = 'B0625' OR c.campaign_name LIKE '%-B0625-%';

-- COMMAND ----------

-- 1b. Catálogo: Canvas del ticket, con todos sus campos
SELECT v.*
FROM analytics_engineering_production.braze._dim_braze_canvas v
WHERE v.ticket_number = 'B0625' OR v.canvas_name LIKE '%-B0625-%';

-- COMMAND ----------

-- 2. Pasos de los Canvas del ticket (qué mensaje sale en cada paso, y cuándo salió el primero y el último)
SELECT v.canvas_name, s.*
FROM analytics_engineering_production.braze._dim_braze_canvas_step s
JOIN analytics_engineering_production.braze._dim_braze_canvas v ON v.canvas_id = s.canvas_id
WHERE v.ticket_number = 'B0625' OR v.canvas_name LIKE '%-B0625-%'
ORDER BY v.canvas_name, s.first_sent;

-- COMMAND ----------

-- 3. Resultados por comunicación × canal × mes: envíos, entrega, respuesta, bajas, solicitudes, créditos, monto y costo
CREATE OR REPLACE TEMPORARY VIEW v_ticket_base AS
WITH ids AS (
  SELECT campaign_id AS communication_id FROM analytics_engineering_production.braze._dim_braze_campaign
  WHERE ticket_number = 'B0625' OR campaign_name LIKE '%-B0625-%'
  UNION
  SELECT canvas_id FROM analytics_engineering_production.braze._dim_braze_canvas
  WHERE ticket_number = 'B0625' OR canvas_name LIKE '%-B0625-%'
),
usuarios AS (
  -- Solo las personas que recibieron algo del ticket, para que la atribución fraccional vea todo lo que les llegó ese día
  SELECT DISTINCT e.user_id
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications e
  WHERE e.event_date BETWEEN DATE '2026-01-01' AND DATE '2026-10-31'
    AND (e.communication_id IN (SELECT communication_id FROM ids) OR e.ticket_number = 'B0625' OR e.communication_name LIKE '%-B0625-%')
),
base AS (
  SELECT e.user_id, e.communication_id, e.event_date, e.category,
    MAX(e.communication_name) AS communication_name, MAX(e.team) AS team, MAX(e.product_service) AS product_service,
    MAX(e.ticket_number) AS ticket_number, MAX(e.`group`) AS grupo, MAX(e.segment) AS segment, MAX(e.subsegment) AS subsegment,
    MAX(CAST(e.was_send AS INT)) AS was_send, MAX(CAST(e.was_opened AS INT)) AS was_opened,
    MAX(CAST(e.email_sent AS INT)) AS email_sent, MAX(CAST(e.email_delivery AS INT)) AS email_delivery,
    MAX(CAST(e.email_open AS INT)) AS email_open, MAX(CAST(e.email_click AS INT)) AS email_click,
    MAX(CAST(e.email_unsubscribe AS INT)) AS email_unsubscribe,
    MAX(CAST(e.pn_send AS INT)) AS pn_send, MAX(CAST(e.pn_open AS INT)) AS pn_open,
    MAX(CAST(e.whatsapp_send AS INT)) AS whatsapp_send, MAX(CAST(e.whatsapp_delivery AS INT)) AS whatsapp_delivery,
    MAX(CAST(e.whatsapp_read AS INT)) AS whatsapp_read,
    MAX(CAST(e.in_app_impression AS INT)) AS in_app_impression, MAX(CAST(e.in_app_click AS INT)) AS in_app_click,
    MAX(CAST(e.banner_impression AS INT)) AS banner_impression, MAX(CAST(e.banner_click AS INT)) AS banner_click,
    MAX(CAST(e.applied_for_loan AS INT)) AS solicito, MAX(CAST(e.is_converted AS INT)) AS convirtio, MAX(e.gross_amount) AS monto,
    MAX(e.control_group) AS control_group
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications e
  JOIN usuarios u ON u.user_id = e.user_id
  WHERE e.event_date BETWEEN DATE '2026-01-01' AND DATE '2026-10-31'
  GROUP BY e.user_id, e.communication_id, e.event_date, e.category
),
con_dia AS (
  SELECT *,
    SUM(was_send) OVER (PARTITION BY user_id, event_date)   AS comms_enviadas_dia,
    MAX(convirtio) OVER (PARTITION BY user_id, event_date)  AS conv_dia,
    MAX(monto) OVER (PARTITION BY user_id, event_date)      AS monto_dia
  FROM base
)
SELECT * FROM con_dia
WHERE communication_id IN (SELECT communication_id FROM ids) OR ticket_number = 'B0625' OR communication_name LIKE '%-B0625-%';

SELECT
  communication_id, communication_name, team, product_service, category AS canal,
  DATE_TRUNC('month', event_date) AS mes,
  SUM(was_send)                                                   AS envios,
  COUNT(DISTINCT CASE WHEN was_send = 1 THEN user_id END)         AS personas,
  SUM(email_sent) AS email_enviados, SUM(email_delivery) AS email_entregados, SUM(email_open) AS email_abiertos,
  SUM(email_click) AS email_clics, SUM(email_unsubscribe) AS email_bajas,
  ROUND(100 * SUM(email_open) / NULLIF(SUM(email_delivery), 0), 2)  AS pct_apertura_email,
  ROUND(100 * SUM(email_click) / NULLIF(SUM(email_delivery), 0), 2) AS pct_clic_email,
  ROUND(1000 * SUM(email_unsubscribe) / NULLIF(SUM(email_delivery), 0), 2) AS bajas_por_mil_correos,
  SUM(pn_send) AS push_enviados, SUM(pn_open) AS push_abiertos,
  ROUND(100 * SUM(pn_open) / NULLIF(SUM(pn_send), 0), 2)            AS pct_apertura_push,
  SUM(whatsapp_send) AS wa_enviados, SUM(whatsapp_delivery) AS wa_entregados, SUM(whatsapp_read) AS wa_leidos,
  ROUND(100 * SUM(whatsapp_delivery) / NULLIF(SUM(whatsapp_send), 0), 1)  AS pct_entrega_wa,
  ROUND(100 * SUM(whatsapp_read) / NULLIF(SUM(whatsapp_delivery), 0), 1)  AS pct_lectura_wa,
  SUM(in_app_impression) AS inapp_vistos, SUM(in_app_click) AS inapp_clics,
  ROUND(100 * SUM(in_app_click) / NULLIF(SUM(in_app_impression), 0), 1)   AS pct_clic_inapp,
  SUM(banner_impression) AS banner_vistos, SUM(banner_click) AS banner_clics,
  SUM(solicito)                                                   AS solicitudes_filas,
  SUM(convirtio)                                                  AS creditos_filas,
  ROUND(SUM(CASE WHEN was_send = 1 AND conv_dia = 1 THEN 1.0 / comms_enviadas_dia ELSE 0 END), 1)      AS creditos_fraccional,
  ROUND(SUM(CASE WHEN was_send = 1 AND conv_dia = 1 THEN monto_dia / comms_enviadas_dia ELSE 0 END), 0) AS monto_fraccional_mxn,
  ROUND(SUM(email_sent) * 0.05 + SUM(whatsapp_delivery) * 1.00, 0)  AS costo_mxn,
  ROUND((SUM(email_sent) * 0.05 + SUM(whatsapp_delivery) * 1.00)
        / NULLIF(SUM(CASE WHEN was_send = 1 AND conv_dia = 1 THEN 1.0 / comms_enviadas_dia ELSE 0 END), 0), 1) AS mxn_por_credito,
  ROUND((SUM(email_sent) * 0.05 + SUM(whatsapp_delivery) * 1.00) / NULLIF(SUM(solicito), 0), 1)            AS mxn_por_solicitud
FROM v_ticket_base
GROUP BY communication_id, communication_name, team, product_service, category, DATE_TRUNC('month', event_date)
ORDER BY mes, envios DESC;

-- COMMAND ----------

-- 4. Totales del ticket por canal (una fila por canal, todo el periodo)
SELECT
  category AS canal,
  COUNT(DISTINCT communication_id)                                AS comunicaciones,
  MIN(event_date) AS primer_envio, MAX(event_date) AS ultimo_envio,
  SUM(was_send) AS envios, COUNT(DISTINCT CASE WHEN was_send = 1 THEN user_id END) AS personas,
  ROUND(SUM(was_send) / NULLIF(COUNT(DISTINCT CASE WHEN was_send = 1 THEN user_id END), 0), 1) AS mensajes_por_persona,
  ROUND(100 * SUM(email_click) / NULLIF(SUM(email_delivery), 0), 2)       AS pct_clic_email,
  ROUND(100 * SUM(pn_open) / NULLIF(SUM(pn_send), 0), 2)                  AS pct_apertura_push,
  ROUND(100 * SUM(whatsapp_read) / NULLIF(SUM(whatsapp_delivery), 0), 1)  AS pct_lectura_wa,
  ROUND(100 * SUM(in_app_click) / NULLIF(SUM(in_app_impression), 0), 1)   AS pct_clic_inapp,
  SUM(email_unsubscribe)                                          AS bajas_email,
  ROUND(SUM(CASE WHEN was_send = 1 AND conv_dia = 1 THEN 1.0 / comms_enviadas_dia ELSE 0 END), 1)      AS creditos_fraccional,
  ROUND(SUM(CASE WHEN was_send = 1 AND conv_dia = 1 THEN monto_dia / comms_enviadas_dia ELSE 0 END), 0) AS monto_fraccional_mxn,
  ROUND(SUM(email_sent) * 0.05 + SUM(whatsapp_delivery) * 1.00, 0)  AS costo_mxn
FROM v_ticket_base
GROUP BY category
ORDER BY envios DESC;

-- COMMAND ----------

-- 5. Serie diaria por canal (para ver picos, días de envío y caída de respuesta)
SELECT event_date, category AS canal,
  SUM(was_send) AS envios, COUNT(DISTINCT CASE WHEN was_send = 1 THEN user_id END) AS personas,
  SUM(email_click) AS email_clics, SUM(pn_open) AS push_abiertos, SUM(whatsapp_read) AS wa_leidos, SUM(in_app_click) AS inapp_clics,
  SUM(email_unsubscribe) AS bajas_email, SUM(solicito) AS solicitudes, SUM(convirtio) AS creditos_filas
FROM v_ticket_base
GROUP BY event_date, category
ORDER BY event_date, canal;

-- COMMAND ----------

-- 6. Por segmento, subsegmento y grupo (a quién le llegó y cómo respondió cada audiencia)
SELECT segment, subsegment, grupo, category AS canal,
  SUM(was_send) AS envios, COUNT(DISTINCT CASE WHEN was_send = 1 THEN user_id END) AS personas,
  ROUND(100 * SUM(email_click) / NULLIF(SUM(email_delivery), 0), 2)       AS pct_clic_email,
  ROUND(100 * SUM(pn_open) / NULLIF(SUM(pn_send), 0), 2)                  AS pct_apertura_push,
  ROUND(100 * SUM(whatsapp_read) / NULLIF(SUM(whatsapp_delivery), 0), 1)  AS pct_lectura_wa,
  ROUND(100 * SUM(in_app_click) / NULLIF(SUM(in_app_impression), 0), 1)   AS pct_clic_inapp,
  SUM(email_unsubscribe) AS bajas_email,
  ROUND(SUM(CASE WHEN was_send = 1 AND conv_dia = 1 THEN 1.0 / comms_enviadas_dia ELSE 0 END), 1) AS creditos_fraccional
FROM v_ticket_base
GROUP BY segment, subsegment, grupo, category
ORDER BY envios DESC;

-- COMMAND ----------

-- 7. Cuántos mensajes del ticket recibió cada persona (distribución) y cuántas convirtieron en cada banda
WITH p AS (
  SELECT user_id, SUM(was_send) AS msgs, MAX(convirtio) AS convirtio, MAX(email_unsubscribe) AS baja
  FROM v_ticket_base GROUP BY user_id
)
SELECT CASE WHEN msgs = 0 THEN '0' WHEN msgs = 1 THEN '1' WHEN msgs <= 3 THEN '2 a 3' WHEN msgs <= 5 THEN '4 a 5'
            WHEN msgs <= 10 THEN '6 a 10' WHEN msgs <= 20 THEN '11 a 20' ELSE '21 o más' END AS mensajes_del_ticket,
  COUNT(*) AS personas, SUM(msgs) AS mensajes,
  ROUND(100 * AVG(convirtio), 2) AS pct_con_credito, ROUND(100 * AVG(baja), 2) AS pct_se_dio_de_baja
FROM p
GROUP BY 1
ORDER BY MIN(msgs);

-- COMMAND ----------

-- 8. Embudo por paso de Canvas, con variantes y grupo de control
SELECT e.canvas_name, e.canvas_step_name, e.category AS canal,
  e.canvas_variation_name, e.experiment_split_name, e.in_control_group,
  MIN(e.event_date) AS primer_dia, MAX(e.event_date) AS ultimo_dia,
  COUNT(DISTINCT e.user_id) AS personas,
  COUNT(DISTINCT CASE WHEN CAST(e.was_opened AS INT) = 1 THEN e.user_id END)       AS abrieron,
  COUNT(DISTINCT CASE WHEN CAST(e.applied_for_loan AS INT) = 1 THEN e.user_id END) AS solicitaron,
  COUNT(DISTINCT CASE WHEN CAST(e.is_converted AS INT) = 1 THEN e.user_id END)     AS con_credito,
  ROUND(SUM(e.gross_amount), 0) AS monto
FROM analytics_engineering_production.braze_semantic_layer._fct_braze_canvas_user_engagement e
JOIN analytics_engineering_production.braze._dim_braze_canvas v ON v.canvas_id = e.canvas_id
WHERE (v.ticket_number = 'B0625' OR v.canvas_name LIKE '%-B0625-%')
  AND e.event_date BETWEEN DATE '2026-01-01' AND DATE '2026-10-31'
GROUP BY ALL
ORDER BY e.canvas_name, primer_dia, e.canvas_step_name;

-- COMMAND ----------

-- 9. Lift contra el grupo de control: ¿convierte más quien recibió los mensajes que quien no?
-- Si el grupo de control tiene menos de unas mil personas, el resultado no es confiable.
SELECT e.canvas_name,
  CASE WHEN e.in_control_group = TRUE THEN 'control (sin mensajes)' ELSE 'recibió mensajes' END AS grupo,
  COUNT(DISTINCT e.user_id) AS personas,
  ROUND(100 * COUNT(DISTINCT CASE WHEN CAST(e.applied_for_loan AS INT) = 1 THEN e.user_id END) / COUNT(DISTINCT e.user_id), 2) AS pct_solicito,
  ROUND(100 * COUNT(DISTINCT CASE WHEN CAST(e.is_converted AS INT) = 1 THEN e.user_id END) / COUNT(DISTINCT e.user_id), 2)     AS pct_con_credito
FROM analytics_engineering_production.braze_semantic_layer._fct_braze_canvas_user_engagement e
JOIN analytics_engineering_production.braze._dim_braze_canvas v ON v.canvas_id = e.canvas_id
WHERE (v.ticket_number = 'B0625' OR v.canvas_name LIKE '%-B0625-%')
  AND e.event_date BETWEEN DATE '2026-01-01' AND DATE '2026-10-31'
GROUP BY e.canvas_name, 2
ORDER BY e.canvas_name, 2;

-- COMMAND ----------

-- 10. A quién le llegó: etapa del cliente y banderas de contacto (bloqueados, bajas, app)
-- Ojo: los filtros son el estado de HOY de la persona, no el del día del envío.
WITH p AS (
  SELECT user_id, SUM(was_send) AS msgs, MAX(convirtio) AS convirtio FROM v_ticket_base GROUP BY user_id
)
SELECT
  COALESCE(f.step, 'sin dato') AS etapa,
  COALESCE(f.mkt_contactable_channel, 'sin dato') AS canal_contactable,
  f.cc_freeze AS kpay_congelado, f.is_blacklist AS lista_negra, f.is_arco AS arco, f.is_reus AS reus,
  f.email_unsubscribed AS baja_email, f.push_unsubscribed AS baja_push, f.wa_unsubscribed AS baja_wa,
  f.with_app AS tiene_app, f.notifications_enabled AS notificaciones,
  COUNT(*) AS personas, SUM(p.msgs) AS mensajes, ROUND(100 * AVG(p.convirtio), 2) AS pct_con_credito
FROM p
LEFT JOIN product.customer_golden_dataset.dim_braze_filters f ON f.customer_id = p.user_id
GROUP BY ALL
ORDER BY personas DESC;

-- COMMAND ----------

-- 11. Con qué otras campañas chocó: comunicaciones que le llegaron a la misma persona el mismo día
WITH t AS (SELECT DISTINCT user_id, event_date FROM v_ticket_base WHERE was_send = 1)
SELECT e.communication_name, MAX(e.team) AS team, e.category AS canal,
  COUNT(DISTINCT e.user_id || CAST(e.event_date AS STRING)) AS personas_dia_en_comun
FROM analytics_engineering_production.xplore._dim_braze_users_and_communications e
JOIN t ON t.user_id = e.user_id AND t.event_date = e.event_date
WHERE CAST(e.was_send AS INT) = 1
  AND NOT (e.ticket_number = 'B0625' OR e.communication_name LIKE '%-B0625-%')
GROUP BY e.communication_name, e.category
ORDER BY personas_dia_en_comun DESC
LIMIT 30;
