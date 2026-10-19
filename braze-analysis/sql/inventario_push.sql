-- Databricks notebook source
-- MAGIC %md
-- MAGIC # Inventario de push: todos los que existen y cuáles están prendidos hoy
-- MAGIC Dialecto: Databricks SQL con Unity Catalog.
-- MAGIC
-- MAGIC Los catálogos de Braze en Databricks no traen un campo de "prendida en el panel".
-- MAGIC Por eso "prendida" se infiere: no archivada y con al menos un push enviado en los últimos 7 días.
-- MAGIC La fecha de corte es el último día con datos en la tabla de envíos, no la fecha de hoy, para que un retraso de carga no apague todo.
-- MAGIC
-- MAGIC Query 1: una fila por campaña o Canvas que tiene push (en el catálogo o porque mandó push).
-- MAGIC Query 2: resumen por estado y equipo.
-- MAGIC Query 3: detalle por paso de Canvas, para ver qué push concreto sigue saliendo.

-- COMMAND ----------

-- Antes de correr: revisar si el catálogo trae algún campo de estado (draft, enabled, status, schedule).
-- Si aparece, se usa en lugar de la regla de 7 días.
DESCRIBE TABLE analytics_engineering_production.braze._dim_braze_campaign;

-- COMMAND ----------

-- ---------------------------------------------------------------
-- Query 1. Inventario de push por campaña y Canvas
-- ---------------------------------------------------------------
WITH corte AS (
  SELECT MAX(event_date) AS fecha_corte
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE event_date >= DATE_SUB(CURRENT_DATE(), 30)
),
catalogo AS (
  SELECT 'campaña' AS tipo, campaign_id AS communication_id, campaign_name AS nombre,
         team, product, audience, offer, ticket_number, archived,
         campaign_created_at AS creada, first_sent, last_sent,
         channel_push_notification AS push_en_catalogo
  FROM analytics_engineering_production.braze._dim_braze_campaign
  UNION ALL
  SELECT 'canvas', canvas_id, canvas_name,
         team, product, audience, offer, ticket_number, archived,
         canvas_created_at, first_sent, last_sent,
         channel_push_notification
  FROM analytics_engineering_production.braze._dim_braze_canvas
),
envios_push AS (
  -- Una fila de la tabla es usuario x comunicación x día x canal
  SELECT
    e.communication_id,
    MAX(e.communication_name)                                                     AS nombre_envios,
    MAX(e.team)                                                                   AS team_envios,
    MIN(e.event_date)                                                             AS primer_push,
    MAX(e.event_date)                                                             AS ultimo_push,
    COUNT(*)                                                                      AS push_desde_2025,
    SUM(CASE WHEN e.event_date > DATE_SUB(c.fecha_corte, 30) THEN 1 ELSE 0 END)   AS push_30d,
    COUNT(DISTINCT CASE WHEN e.event_date > DATE_SUB(c.fecha_corte, 30) THEN e.user_id END) AS personas_30d,
    SUM(CASE WHEN e.event_date > DATE_SUB(c.fecha_corte, 30) AND e.pn_open THEN 1 ELSE 0 END) AS abiertos_30d,
    SUM(CASE WHEN e.event_date > DATE_SUB(c.fecha_corte, 7) THEN 1 ELSE 0 END)    AS push_7d
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications e
  CROSS JOIN corte c
  WHERE e.category = 'push notification'
    AND e.pn_send
    AND e.event_date >= DATE '2025-01-01'
  GROUP BY e.communication_id
)
SELECT
  COALESCE(k.tipo, 'sin catálogo')                AS tipo,
  COALESCE(k.communication_id, p.communication_id) AS communication_id,
  COALESCE(k.nombre, p.nombre_envios)             AS nombre,
  COALESCE(k.team, p.team_envios)                 AS team,
  k.product, k.audience, k.offer, k.ticket_number,
  k.archived, k.creada,
  k.push_en_catalogo,
  p.primer_push, p.ultimo_push,
  COALESCE(p.push_desde_2025, 0)                  AS push_desde_2025,
  COALESCE(p.push_30d, 0)                         AS push_30d,
  COALESCE(p.personas_30d, 0)                     AS personas_30d,
  COALESCE(p.abiertos_30d, 0)                     AS abiertos_30d,
  ROUND(1000 * p.abiertos_30d / NULLIF(p.push_30d, 0), 1) AS aperturas_por_mil_30d,
  CASE
    WHEN k.archived                                   THEN 'archivada'
    WHEN COALESCE(p.push_7d, 0) > 0                   THEN 'prendida (push en 7 días)'
    WHEN COALESCE(p.push_30d, 0) > 0                  THEN 'reciente (push en 8 a 30 días)'
    WHEN p.ultimo_push IS NOT NULL                    THEN 'dormida (push hace más de 30 días)'
    ELSE 'nunca mandó push (solo en catálogo)'
  END AS estado_push,
  (SELECT fecha_corte FROM corte)                 AS fecha_corte
FROM catalogo k
FULL OUTER JOIN envios_push p ON p.communication_id = k.communication_id
WHERE COALESCE(k.push_en_catalogo, FALSE) OR p.communication_id IS NOT NULL
ORDER BY
  CASE WHEN COALESCE(p.push_7d, 0) > 0 AND NOT COALESCE(k.archived, FALSE) THEN 0 ELSE 1 END,
  push_30d DESC;

-- COMMAND ----------

-- ---------------------------------------------------------------
-- Query 2. Resumen: cuántos push hay por estado y equipo
-- Correr después de guardar la Query 1 como vista temporal:
--   CREATE OR REPLACE TEMPORARY VIEW v_inventario_push AS <Query 1 sin ORDER BY>;
-- ---------------------------------------------------------------
SELECT
  estado_push, team,
  COUNT(*)                        AS comunicaciones,
  SUM(push_30d)                   AS push_30d,
  SUM(personas_30d)               AS personas_30d_suma,
  ROUND(1000 * SUM(abiertos_30d) / NULLIF(SUM(push_30d), 0), 1) AS aperturas_por_mil_30d
FROM v_inventario_push
GROUP BY estado_push, team
ORDER BY estado_push, push_30d DESC;

-- COMMAND ----------

-- ---------------------------------------------------------------
-- Query 3. Pasos de Canvas que mandaron push en los últimos 30 días
-- ---------------------------------------------------------------
WITH corte AS (
  SELECT MAX(event_date) AS fecha_corte
  FROM analytics_engineering_production.braze_semantic_layer._fct_braze_canvas_user_engagement
  WHERE event_date >= DATE_SUB(CURRENT_DATE(), 30)
)
SELECT
  e.canvas_id, MAX(e.canvas_name) AS canvas_name, MAX(e.team) AS team,
  e.canvas_step_id, MAX(e.canvas_step_name) AS paso,
  MIN(e.event_date) AS primer_push_30d, MAX(e.event_date) AS ultimo_push,
  COUNT(*)                                   AS push_30d,
  COUNT(DISTINCT e.user_id)                  AS personas_30d,
  ROUND(1000 * SUM(CASE WHEN e.was_opened THEN 1 ELSE 0 END) / COUNT(*), 1) AS aperturas_por_mil,
  SUM(CASE WHEN e.in_control_group THEN 1 ELSE 0 END) AS filas_grupo_control,
  CASE WHEN MAX(e.event_date) > DATE_SUB(MAX(c.fecha_corte), 7) THEN 'prendido' ELSE 'reciente' END AS estado_paso
FROM analytics_engineering_production.braze_semantic_layer._fct_braze_canvas_user_engagement e
CROSS JOIN corte c
WHERE e.category = 'push notification'
  AND e.event_date > DATE_SUB(c.fecha_corte, 30)
GROUP BY e.canvas_id, e.canvas_step_id
ORDER BY push_30d DESC;
