-- Databricks notebook source
-- MAGIC %md
-- MAGIC # ¿Existe un push que confirme el préstamo?
-- MAGIC Busca por nombre todas las comunicaciones y pasos de Canvas que hablan de préstamo aprobado,
-- MAGIC dispersado o confirmado, y dice por qué canal salieron en los últimos 90 días.
-- MAGIC En las extracciones de enero a septiembre 2026 la confirmación de KCash solo sale por correo:
-- MAGIC KCash-Loan-Application-disbursed_20251110 y su versión _late_fees_. Ninguna tiene push.

-- COMMAND ----------

-- 1. Campañas y Canvas: canal real de envío en los últimos 90 días
WITH corte AS (
  SELECT MAX(event_date) AS fecha_corte
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE event_date >= DATE_SUB(CURRENT_DATE(), 30)
)
SELECT
  e.communication_id, e.communication_name, e.category AS canal,
  MIN(e.event_date) AS primer_envio, MAX(e.event_date) AS ultimo_envio,
  COUNT(*) AS envios_90d, COUNT(DISTINCT e.user_id) AS personas_90d
FROM analytics_engineering_production.xplore._dim_braze_users_and_communications e
CROSS JOIN corte c
WHERE e.event_date > DATE_SUB(c.fecha_corte, 90)
  AND e.was_send
  AND LOWER(e.communication_name) RLIKE
      'disburs|dispers|desembols|approv|aprob|otorg|confirm|deposit|loan.?(created|granted|success)|prestamo|préstamo|tu credito|tu crédito'
GROUP BY e.communication_id, e.communication_name, e.category
ORDER BY envios_90d DESC;

-- COMMAND ----------

-- 2. Pasos de Canvas con push cuyo nombre de Canvas o de paso habla del préstamo
SELECT
  s.canvas_id, cv.canvas_name, s.canvas_step_id, s.canvas_step_name,
  s.first_sent, s.last_sent, cv.archived
FROM analytics_engineering_production.braze._dim_braze_canvas_step s
JOIN analytics_engineering_production.braze._dim_braze_canvas cv ON cv.canvas_id = s.canvas_id
WHERE LOWER(CONCAT_WS(' ', cv.canvas_name, s.canvas_step_name)) RLIKE
      'disburs|dispers|desembols|approv|aprob|otorg|confirm|deposit|loan.?(created|granted|success)|prestamo|préstamo'
ORDER BY s.last_sent DESC;
