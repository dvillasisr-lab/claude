-- Databricks notebook source
-- MAGIC %md
-- MAGIC # Verificaciones de la auditoría de Braze
-- MAGIC Importar este archivo como notebook (File > Import) y correr todas las celdas. Cada celda muestra su resultado.
-- MAGIC Dialecto: Databricks SQL con Unity Catalog. Periodo: 2026-01-01 a 2026-09-30.

-- COMMAND ----------

-- V1. ¿user_id de Braze cruza con customer_id del golden dataset? Esperado: > 90 %
SELECT
  COUNT(DISTINCT c.user_id)                                         AS usuarios_con_envios,
  COUNT(DISTINCT CASE WHEN f.customer_id IS NOT NULL THEN c.user_id END) AS cruzan,
  ROUND(100.0 * COUNT(DISTINCT CASE WHEN f.customer_id IS NOT NULL THEN c.user_id END) / COUNT(DISTINCT c.user_id), 1) AS pct_cruce
FROM analytics_engineering_production.xplore._dim_braze_users_and_communications c
LEFT JOIN product.customer_golden_dataset.dim_braze_filters f ON f.customer_id = c.user_id
WHERE c.event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30';

-- COMMAND ----------

-- V2. ¿xplore y semantic_layer son la misma tabla? Esperado: filas y sumas iguales
SELECT 'xplore' AS fuente, COUNT(*) filas, COUNT(DISTINCT user_id) usuarios, SUM(CASE WHEN is_converted THEN 1 ELSE 0 END) conv, SUM(gross_amount) monto, MIN(event_date) desde, MAX(event_date) hasta
FROM analytics_engineering_production.xplore._fct_braze_canvas_user_engagement
UNION ALL
SELECT 'semantic_layer', COUNT(*), COUNT(DISTINCT user_id), SUM(CASE WHEN is_converted THEN 1 ELSE 0 END), SUM(gross_amount), MIN(event_date), MAX(event_date)
FROM analytics_engineering_production.braze_semantic_layer._fct_braze_canvas_user_engagement;

-- COMMAND ----------

-- V3. ¿Qué valores toma control_group y cómo se comporta cada uno?
SELECT control_group,
       COUNT(*) filas,
       SUM(CASE WHEN was_send THEN 1 ELSE 0 END) envios,
       SUM(CASE WHEN applied_for_loan THEN 1 ELSE 0 END) solicitudes,
       SUM(CASE WHEN is_converted THEN 1 ELSE 0 END) conversiones,
       ROUND(100.0 * SUM(CASE WHEN is_converted THEN 1 ELSE 0 END) / COUNT(*), 2) pct_conv
FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
GROUP BY control_group ORDER BY filas DESC;

-- COMMAND ----------

-- V3b. Lo mismo en Canvas con in_control_group
SELECT in_control_group, COUNT(*) filas,
       SUM(CASE WHEN is_converted THEN 1 ELSE 0 END) conversiones,
       ROUND(100.0 * SUM(CASE WHEN is_converted THEN 1 ELSE 0 END) / COUNT(*), 2) pct_conv
FROM analytics_engineering_production.braze_semantic_layer._fct_braze_canvas_user_engagement
WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
GROUP BY in_control_group;

-- COMMAND ----------

-- V4. ¿Hay conversiones en filas sin envío? Si sí, la fila representa "elegible", no "enviado"
SELECT was_send, COUNT(*) filas,
       SUM(CASE WHEN is_converted THEN 1 ELSE 0 END) conversiones,
       SUM(CASE WHEN applied_for_loan THEN 1 ELSE 0 END) solicitudes
FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
GROUP BY was_send;

-- COMMAND ----------

-- V5. ¿La conversión se repite en varias filas del mismo usuario y día?
SELECT repeticiones, COUNT(*) casos FROM (
  SELECT user_id, event_date, COUNT(*) repeticiones
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE is_converted AND event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
  GROUP BY user_id, event_date
) t GROUP BY repeticiones ORDER BY repeticiones;

-- COMMAND ----------

-- V5b. ¿Un mismo usuario convierte en varios días distintos? (préstamos repetidos)
SELECT dias_con_conversion, COUNT(*) usuarios FROM (
  SELECT user_id, COUNT(DISTINCT event_date) dias_con_conversion
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE is_converted AND event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
  GROUP BY user_id
) t GROUP BY 1 ORDER BY 1;

-- COMMAND ----------

-- V6. Códigos de canal reales
SELECT channel, category, COUNT(*) filas, SUM(CASE WHEN was_send THEN 1 ELSE 0 END) envios
FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
GROUP BY channel, category ORDER BY filas DESC;

SELECT 'campaign' tipo, channel, COUNT(*) FROM analytics_engineering_production.braze._dim_braze_campaign GROUP BY channel
UNION ALL
SELECT 'canvas', channel, COUNT(*) FROM analytics_engineering_production.braze._dim_braze_canvas GROUP BY channel;

-- COMMAND ----------

-- V6b. ¿was_send es la unión de las banderas por canal?
SELECT
  SUM(CASE WHEN was_send AND NOT (email_sent OR pn_send OR whatsapp_send OR in_app_impression OR banner_impression) THEN 1 ELSE 0 END) AS send_sin_canal,
  SUM(CASE WHEN NOT was_send AND (email_sent OR pn_send OR whatsapp_send OR in_app_impression OR banner_impression) THEN 1 ELSE 0 END) AS canal_sin_send
FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30';

-- COMMAND ----------

-- V7. Prefijo de ticket contra equipo
SELECT SUBSTR(ticket_number,1,1) prefijo, team, COUNT(*) piezas
FROM (SELECT ticket_number, team FROM analytics_engineering_production.braze._dim_braze_campaign
      UNION ALL SELECT ticket_number, team FROM analytics_engineering_production.braze._dim_braze_canvas) t
GROUP BY 1,2 ORDER BY 1,3 DESC;

-- COMMAND ----------

-- V8. ¿gross_amount solo existe cuando is_converted?
SELECT is_converted, applied_for_loan,
       COUNT(*) filas, SUM(CASE WHEN gross_amount IS NOT NULL THEN 1 ELSE 0 END) con_monto,
       AVG(gross_amount) monto_promedio, MIN(gross_amount) minimo, MAX(gross_amount) maximo
FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
GROUP BY 1,2;

-- COMMAND ----------

-- V9. Cobertura por mes. ¿Hay meses vacíos o parciales?
SELECT DATE_TRUNC('month', event_date) mes, COUNT(*) filas, SUM(CASE WHEN was_send THEN 1 ELSE 0 END) envios, COUNT(DISTINCT user_id) usuarios
FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
WHERE event_date >= DATE '2026-01-01'
GROUP BY 1 ORDER BY 1;

-- COMMAND ----------

-- V10. Duplicados en el grano usuario x comunicación x día x canal
SELECT COUNT(*) grupos_duplicados, SUM(n - 1) filas_extra FROM (
  SELECT user_id, communication_id, event_date, category, COUNT(*) n
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
  GROUP BY 1,2,3,4 HAVING COUNT(*) > 1
) t;

-- COMMAND ----------

-- V10b. ¿Los duplicados son filas idénticas o difieren en algo?
-- Si son idénticas: deduplicar con MAX es correcto.
-- Si difieren: ver V10c para saber en qué columna.
WITH g AS (
  SELECT user_id, communication_id, event_date, category,
         COUNT(*) AS n,
         COUNT(DISTINCT CONCAT_WS('|',
           CAST(email_sent AS STRING), CAST(email_delivery AS STRING), CAST(email_open AS STRING), CAST(email_click AS STRING),
           CAST(email_unsubscribe AS STRING), CAST(in_app_impression AS STRING), CAST(in_app_click AS STRING),
           CAST(banner_impression AS STRING), CAST(banner_click AS STRING), CAST(pn_send AS STRING), CAST(pn_open AS STRING),
           CAST(whatsapp_send AS STRING), CAST(whatsapp_delivery AS STRING), CAST(whatsapp_read AS STRING),
           CAST(was_send AS STRING), CAST(was_opened AS STRING), CAST(applied_for_loan AS STRING), CAST(is_converted AS STRING),
           CAST(gross_amount AS STRING), COALESCE(control_group,''), COALESCE(segment,''), COALESCE(subsegment,''),
           COALESCE(team,''), COALESCE(`group`,''), COALESCE(ticket_number,''), COALESCE(communication_name,''), COALESCE(product_service,''))) AS versiones
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
  GROUP BY 1,2,3,4 HAVING COUNT(*) > 1
)
SELECT CASE WHEN versiones = 1 THEN 'identicas' ELSE 'difieren' END AS tipo,
       COUNT(*) AS grupos, SUM(n - 1) AS filas_extra
FROM g GROUP BY 1;

-- COMMAND ----------

-- V10c. ¿En qué columnas difieren los duplicados?
-- Cada columna dice en cuántos grupos duplicados ese campo tiene más de un valor.
WITH g AS (
  SELECT user_id, communication_id, event_date, category,
         COUNT(DISTINCT segment) ds, COUNT(DISTINCT subsegment) dss, COUNT(DISTINCT team) dt,
         COUNT(DISTINCT `group`) dg, COUNT(DISTINCT ticket_number) dtk, COUNT(DISTINCT control_group) dcg,
         COUNT(DISTINCT communication_name) dcn, COUNT(DISTINCT product_service) dps, COUNT(DISTINCT channel) dch,
         COUNT(DISTINCT CAST(was_send AS INT)) dws, COUNT(DISTINCT CAST(email_sent AS INT)) des,
         COUNT(DISTINCT CAST(email_delivery AS INT)) ded, COUNT(DISTINCT CAST(email_open AS INT)) deo,
         COUNT(DISTINCT CAST(email_click AS INT)) dec, COUNT(DISTINCT CAST(pn_send AS INT)) dpn,
         COUNT(DISTINCT CAST(whatsapp_send AS INT)) dwa, COUNT(DISTINCT CAST(in_app_impression AS INT)) dia,
         COUNT(DISTINCT CAST(applied_for_loan AS INT)) dap, COUNT(DISTINCT CAST(is_converted AS INT)) dic,
         COUNT(DISTINCT gross_amount) dga
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
  GROUP BY 1,2,3,4 HAVING COUNT(*) > 1
)
SELECT COUNT(*) AS grupos_duplicados,
  SUM(CASE WHEN ds>1  THEN 1 ELSE 0 END) AS varia_segment,
  SUM(CASE WHEN dss>1 THEN 1 ELSE 0 END) AS varia_subsegment,
  SUM(CASE WHEN dt>1  THEN 1 ELSE 0 END) AS varia_team,
  SUM(CASE WHEN dg>1  THEN 1 ELSE 0 END) AS varia_group,
  SUM(CASE WHEN dtk>1 THEN 1 ELSE 0 END) AS varia_ticket,
  SUM(CASE WHEN dcg>1 THEN 1 ELSE 0 END) AS varia_control_group,
  SUM(CASE WHEN dcn>1 THEN 1 ELSE 0 END) AS varia_communication_name,
  SUM(CASE WHEN dps>1 THEN 1 ELSE 0 END) AS varia_product_service,
  SUM(CASE WHEN dch>1 THEN 1 ELSE 0 END) AS varia_channel,
  SUM(CASE WHEN dws>1 THEN 1 ELSE 0 END) AS varia_was_send,
  SUM(CASE WHEN des>1 THEN 1 ELSE 0 END) AS varia_email_sent,
  SUM(CASE WHEN ded>1 THEN 1 ELSE 0 END) AS varia_email_delivery,
  SUM(CASE WHEN deo>1 THEN 1 ELSE 0 END) AS varia_email_open,
  SUM(CASE WHEN dec>1 THEN 1 ELSE 0 END) AS varia_email_click,
  SUM(CASE WHEN dpn>1 THEN 1 ELSE 0 END) AS varia_pn_send,
  SUM(CASE WHEN dwa>1 THEN 1 ELSE 0 END) AS varia_whatsapp_send,
  SUM(CASE WHEN dia>1 THEN 1 ELSE 0 END) AS varia_in_app_impression,
  SUM(CASE WHEN dap>1 THEN 1 ELSE 0 END) AS varia_applied,
  SUM(CASE WHEN dic>1 THEN 1 ELSE 0 END) AS varia_converted,
  SUM(CASE WHEN dga>1 THEN 1 ELSE 0 END) AS varia_gross_amount
FROM g;

-- COMMAND ----------

-- V10d. Cuántas filas tiene cada grupo duplicado (2, 3, 4...)
SELECT n AS filas_por_grupo, COUNT(*) AS grupos FROM (
  SELECT user_id, communication_id, event_date, category, COUNT(*) n
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
  GROUP BY 1,2,3,4 HAVING COUNT(*) > 1
) t GROUP BY n ORDER BY n;

-- COMMAND ----------

-- V10e. Ver con los ojos un grupo duplicado completo (todas sus filas)
WITH uno AS (
  SELECT user_id, communication_id, event_date, category
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
  GROUP BY 1,2,3,4 HAVING COUNT(*) >= 3
  LIMIT 1
)
SELECT c.* FROM analytics_engineering_production.xplore._dim_braze_users_and_communications c
JOIN uno ON uno.user_id = c.user_id AND uno.communication_id = c.communication_id
        AND uno.event_date = c.event_date AND uno.category = c.category
ORDER BY c.user_id;

-- COMMAND ----------

-- V11. ¿La tabla de dispositivos se une con algo? Buscar device_id en otras tablas (revisar con el equipo de datos)
-- Sin query posible: ninguna tabla recibida trae device_id.

-- COMMAND ----------

-- V12. Clasificación de tipo: cuántas piezas quedan sin clasificar con la regla de v_piezas
-- (correr después de crear v_piezas)
-- SELECT tipo_comunicacion, COUNT(*) FROM v_piezas GROUP BY 1 ORDER BY 2 DESC;
-- SELECT nombre FROM v_piezas WHERE tipo_comunicacion = 'sin_clasificar' LIMIT 50;

-- COMMAND ----------

-- V13. Total de filas y usuarios del periodo, para dimensionar los duplicados
SELECT COUNT(*) filas, COUNT(DISTINCT user_id) usuarios, COUNT(DISTINCT communication_id) comunicaciones,
       SUM(CASE WHEN was_send THEN 1 ELSE 0 END) filas_con_envio
FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30';
