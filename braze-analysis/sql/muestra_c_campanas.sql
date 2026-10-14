-- Muestra del lente C (eficiencia por campaña). DuckDB sobre data/e1_comunicacion_mes_canal.csv.
-- Familia = nombre sin la fecha (equipo-producto-ticket-canal-audiencia-oferta-grupo). Las versiones mensuales de una misma Canvas se juntan.

-- Q1. Familias por canal con volumen, costo, resultado y señal de eficiencia
WITH c AS (
  SELECT regexp_replace(communication_name, '-\d{8}-', '-') AS familia, MAX(team) team, MAX(product_service) producto, canal,
    SUM(envios) envios, SUM(costo_mxn) costo, SUM(conversiones_fraccional) conv, SUM(monto_fraccional) monto,
    SUM(email_delivery) ed, SUM(email_open) eo, SUM(email_click) ec, SUM(email_unsubscribe) eu,
    SUM(pn_send) ps, SUM(pn_open) po, SUM(whatsapp_delivery) wd, SUM(whatsapp_read) wr, SUM(in_app_impression) ii, SUM(in_app_click) ic,
    COUNT(DISTINCT mes) meses, MAX(mes) ultimo_mes, COUNT(DISTINCT communication_id) versiones
  FROM e1 WHERE envios > 0 GROUP BY 1, canal
),
med AS (SELECT canal, quantile_cont(envios, 0.5) p50_env, quantile_cont(1000.0*conv/envios, 0.5) p50_conv FROM c GROUP BY canal)
SELECT c.familia, c.team, c.producto, c.canal, c.envios, ROUND(c.costo) costo_mxn, ROUND(c.conv) conv, ROUND(1000.0*c.conv/c.envios, 2) conv_por_mil,
  ROUND(c.costo/NULLIF(c.conv,0), 1) costo_por_conv,
  CASE c.canal WHEN 'email' THEN ROUND(100.0*c.ec/NULLIF(c.ed,0), 2) WHEN 'push notification' THEN ROUND(100.0*c.po/NULLIF(c.ps,0), 2)
       WHEN 'whatsapp' THEN ROUND(100.0*c.wr/NULLIF(c.wd,0), 1) WHEN 'in-app' THEN ROUND(100.0*c.ic/NULLIF(c.ii,0), 1) END AS respuesta_pct,
  ROUND(1000.0*c.eu/NULLIF(c.ed,0), 2) bajas_por_mil, c.meses, c.versiones, strftime(c.ultimo_mes, '%Y-%m') ultimo_mes,
  CASE WHEN c.envios >= m.p50_env AND 1000.0*c.conv/c.envios < m.p50_conv
        AND ((c.canal='email' AND c.ec/NULLIF(c.ed,0) < 0.005) OR (c.canal='push notification' AND c.po/NULLIF(c.ps,0) < 0.01) OR (c.canal='whatsapp' AND c.wr/NULLIF(c.wd,0) < 0.6) OR (c.canal='in-app' AND c.ic/NULLIF(c.ii,0) < 0.1))
       THEN 'apagar o rehacer'
       WHEN c.envios >= m.p50_env AND 1000.0*c.conv/c.envios < m.p50_conv THEN 'revisar'
       WHEN c.envios < m.p50_env AND 1000.0*c.conv/c.envios >= 2*m.p50_conv THEN 'escalar'
       ELSE '' END AS senal
FROM c JOIN med m ON m.canal = c.canal
ORDER BY c.costo DESC, c.envios DESC;
