-- Queries de verificación. Responden las dudas de data/mapeo.md sección 9 con data real.
-- Correr ANTES de lanzar los analistas. Pegar resultados en data/verificaciones_resultado.md.

-- V1. ¿user_id de Braze cruza con customer_id del golden dataset? Esperado: > 90 %
SELECT
  COUNT(DISTINCT c.user_id)                                         AS usuarios_con_envios,
  COUNT(DISTINCT CASE WHEN f.customer_id IS NOT NULL THEN c.user_id END) AS cruzan,
  ROUND(100.0 * COUNT(DISTINCT CASE WHEN f.customer_id IS NOT NULL THEN c.user_id END) / COUNT(DISTINCT c.user_id), 1) AS pct_cruce
FROM analytics_engineering_production.xplore._dim_braze_users_and_communications c
LEFT JOIN product.customer_golden_dataset.dim_braze_filters f ON f.customer_id = c.user_id
WHERE c.event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30';

-- V2. ¿xplore y semantic_layer son la misma tabla? Esperado: filas y sumas iguales
SELECT 'xplore' AS fuente, COUNT(*) filas, COUNT(DISTINCT user_id) usuarios, SUM(CASE WHEN is_converted THEN 1 ELSE 0 END) conv, SUM(gross_amount) monto, MIN(event_date) desde, MAX(event_date) hasta
FROM analytics_engineering_production.xplore._fct_braze_canvas_user_engagement
UNION ALL
SELECT 'semantic_layer', COUNT(*), COUNT(DISTINCT user_id), SUM(CASE WHEN is_converted THEN 1 ELSE 0 END), SUM(gross_amount), MIN(event_date), MAX(event_date)
FROM analytics_engineering_production.braze_semantic_layer._fct_braze_canvas_user_engagement;

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

-- V3b. Lo mismo en Canvas con in_control_group
SELECT in_control_group, COUNT(*) filas,
       SUM(CASE WHEN is_converted THEN 1 ELSE 0 END) conversiones,
       ROUND(100.0 * SUM(CASE WHEN is_converted THEN 1 ELSE 0 END) / COUNT(*), 2) pct_conv
FROM analytics_engineering_production.braze_semantic_layer._fct_braze_canvas_user_engagement
WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
GROUP BY in_control_group;

-- V4. ¿Hay conversiones en filas sin envío? Si sí, la fila representa "elegible", no "enviado"
SELECT was_send, COUNT(*) filas,
       SUM(CASE WHEN is_converted THEN 1 ELSE 0 END) conversiones,
       SUM(CASE WHEN applied_for_loan THEN 1 ELSE 0 END) solicitudes
FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
GROUP BY was_send;

-- V5. ¿La conversión se repite en varias filas del mismo usuario y día?
SELECT repeticiones, COUNT(*) casos FROM (
  SELECT user_id, event_date, COUNT(*) repeticiones
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE is_converted AND event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
  GROUP BY user_id, event_date
) t GROUP BY repeticiones ORDER BY repeticiones;

-- V5b. ¿Un mismo usuario convierte en varios días distintos? (préstamos repetidos)
SELECT dias_con_conversion, COUNT(*) usuarios FROM (
  SELECT user_id, COUNT(DISTINCT event_date) dias_con_conversion
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE is_converted AND event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
  GROUP BY user_id
) t GROUP BY 1 ORDER BY 1;

-- V6. Códigos de canal reales
SELECT channel, category, COUNT(*) filas, SUM(CASE WHEN was_send THEN 1 ELSE 0 END) envios
FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
GROUP BY channel, category ORDER BY filas DESC;

SELECT 'campaign' tipo, channel, COUNT(*) FROM analytics_engineering_production.braze._dim_braze_campaign GROUP BY channel
UNION ALL
SELECT 'canvas', channel, COUNT(*) FROM analytics_engineering_production.braze._dim_braze_canvas GROUP BY channel;

-- V6b. ¿was_send es la unión de las banderas por canal?
SELECT
  SUM(CASE WHEN was_send AND NOT (email_sent OR pn_send OR whatsapp_send OR in_app_impression OR banner_impression) THEN 1 ELSE 0 END) AS send_sin_canal,
  SUM(CASE WHEN NOT was_send AND (email_sent OR pn_send OR whatsapp_send OR in_app_impression OR banner_impression) THEN 1 ELSE 0 END) AS canal_sin_send
FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30';

-- V7. Prefijo de ticket contra equipo
SELECT SUBSTR(ticket_number,1,1) prefijo, team, COUNT(*) piezas
FROM (SELECT ticket_number, team FROM analytics_engineering_production.braze._dim_braze_campaign
      UNION ALL SELECT ticket_number, team FROM analytics_engineering_production.braze._dim_braze_canvas) t
GROUP BY 1,2 ORDER BY 1,3 DESC;

-- V8. ¿gross_amount solo existe cuando is_converted?
SELECT is_converted, applied_for_loan,
       COUNT(*) filas, SUM(CASE WHEN gross_amount IS NOT NULL THEN 1 ELSE 0 END) con_monto,
       AVG(gross_amount) monto_promedio, MIN(gross_amount) minimo, MAX(gross_amount) maximo
FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
GROUP BY 1,2;

-- V9. Cobertura por mes. ¿Hay meses vacíos o parciales?
SELECT DATE_TRUNC('month', event_date) mes, COUNT(*) filas, SUM(CASE WHEN was_send THEN 1 ELSE 0 END) envios, COUNT(DISTINCT user_id) usuarios
FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
WHERE event_date >= DATE '2026-01-01'
GROUP BY 1 ORDER BY 1;

-- V10. Duplicados en el grano usuario x comunicación x día x canal
SELECT COUNT(*) grupos_duplicados, SUM(n - 1) filas_extra FROM (
  SELECT user_id, communication_id, event_date, category, COUNT(*) n
  FROM analytics_engineering_production.xplore._dim_braze_users_and_communications
  WHERE event_date BETWEEN DATE '2026-01-01' AND DATE '2026-09-30'
  GROUP BY 1,2,3,4 HAVING COUNT(*) > 1
) t;

-- V11. ¿La tabla de dispositivos se une con algo? Buscar device_id en otras tablas (revisar con el equipo de datos)
-- Sin query posible: ninguna tabla recibida trae device_id.

-- V12. Clasificación de tipo: cuántas piezas quedan sin clasificar con la regla de v_piezas
-- (correr después de crear v_piezas)
-- SELECT tipo_comunicacion, COUNT(*) FROM v_piezas GROUP BY 1 ORDER BY 2 DESC;
-- SELECT nombre FROM v_piezas WHERE tipo_comunicacion = 'sin_clasificar' LIMIT 50;
