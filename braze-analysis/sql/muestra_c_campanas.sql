-- Muestra del lente C (eficiencia por campaña). DuckDB sobre data/e1_comunicacion_mes_canal.csv.
-- Familia = nombre sin la fecha (equipo-producto-ticket-canal-audiencia-oferta-grupo). Las versiones mensuales de una misma Canvas se juntan.
-- La señal se basa en métricas de comunicación (respuesta y bajas), no en conversión. La conversión queda como columna de referencia
-- porque el evento is_converted es poco confiable y solo aplica a Cash.
--
-- Columnas comparables entre canales: apertura (email abiertos / entregados; push abiertos / enviados; whatsapp leídos / entregados) y clic (email clics / entregados; in-app y banner clics / impresiones).
-- Respuesta (la que usa la señal) por canal: email = clic; push = apertura; whatsapp = lectura; in-app = clic.
-- Volumen alto = envíos de la familia >= mediana de envíos de su canal.
-- Señales:
--   apagar o rehacer: volumen alto y respuesta debajo del mínimo (email clic < 0.3 %, push apertura < 0.75 %, whatsapp lectura < 60 %, in-app clic < 10 %).
--   revisar:          volumen alto y respuesta debajo de la mediana del canal (pero arriba del mínimo), o email con 2.5 o más bajas por mil entregados.
--                     La columna motivo dice cuál de las dos.
--   tipo:             'transaccional u operativa' si el nombre no sigue la convención de ticket (B0000, T0000, S0000) o empieza con Transaccional;
--                     'cobranza' si el equipo es Collections. Esas dos no se juzgan igual que las promocionales.
--   proteger:         volumen alto y respuesta al menos 1.5 veces la mediana del canal.
--   escalar:          volumen bajo (pero al menos 1,000 envíos) y respuesta al menos 2 veces la mediana del canal.
--   (vacío):          dentro de lo normal.
-- Ahorro potencial:
--   ahorro_mxn_periodo = costo variable de la familia en los 9 meses, solo si la señal es apagar o rehacer (lo que no se habría gastado).
--   ahorro_mxn_mes     = ese costo entre los meses activos, solo si la familia envió en septiembre (lo que se deja de gastar cada mes si se apaga hoy).
--   msgs_mes_ahorrados = envíos promedio al mes de esas mismas familias (push e in-app no cuestan, pero son mensajes que el usuario deja de recibir).
--   wa_no_entregado_mxn = envíos de WhatsApp no entregados × 1 MXN, en cualquier señal. Se ahorra limpiando la base, sin apagar nada.

-- Q1. Familias por canal con volumen, costo, respuesta, bajas, conversión de referencia, señal y ahorro potencial
WITH c AS (
  SELECT regexp_replace(communication_name, '-\d{8}-', '-') AS familia, MAX(team) team, MAX(product_service) producto, canal,
    SUM(envios) envios, SUM(costo_mxn) costo, SUM(conversiones_fraccional) conv, SUM(monto_fraccional) monto,
    SUM(email_sent) es, SUM(email_delivery) ed, SUM(email_open) eo, SUM(email_click) ec, SUM(email_unsubscribe) eu,
    SUM(pn_send) ps, SUM(pn_open) po, SUM(whatsapp_send) ws, SUM(whatsapp_delivery) wd, SUM(whatsapp_read) wr, SUM(in_app_impression) ii, SUM(in_app_click) ic, SUM(banner_impression) bi, SUM(banner_click) bc,
    COUNT(DISTINCT mes) meses, MAX(mes) ultimo_mes, MIN(mes) primer_mes, COUNT(DISTINCT communication_id) versiones
  FROM e1 WHERE envios > 0 GROUP BY 1, canal
),
r AS (
  SELECT *,
    CASE canal WHEN 'email' THEN 100.0*ec/NULLIF(ed,0) WHEN 'push notification' THEN 100.0*po/NULLIF(ps,0)
         WHEN 'whatsapp' THEN 100.0*wr/NULLIF(wd,0) WHEN 'in-app' THEN 100.0*ic/NULLIF(ii,0) WHEN 'banner' THEN NULL END AS respuesta,
    CASE canal WHEN 'email' THEN 100.0*ed/NULLIF(es,0) WHEN 'whatsapp' THEN 100.0*wd/NULLIF(ws,0) END AS entrega,
    CASE canal WHEN 'email' THEN 100.0*eo/NULLIF(ed,0) WHEN 'push notification' THEN 100.0*po/NULLIF(ps,0) WHEN 'whatsapp' THEN 100.0*wr/NULLIF(wd,0) END AS apertura,
    CASE canal WHEN 'email' THEN 100.0*ec/NULLIF(ed,0) WHEN 'in-app' THEN 100.0*ic/NULLIF(ii,0) WHEN 'banner' THEN 100.0*bc/NULLIF(bi,0) END AS clic,
    CASE canal WHEN 'email' THEN 1000.0*eu/NULLIF(ed,0) END AS bajas_por_mil
  FROM c
),
med AS (SELECT canal, quantile_cont(envios, 0.5) p50_env, quantile_cont(respuesta, 0.5) p50_resp FROM r GROUP BY canal),
s AS (
SELECT r.familia, r.team, r.producto, r.canal,
  split_part(r.familia, '-', 5) AS audiencia,
  r.envios, ROUND(r.envios / r.meses) AS envios_mes_prom, ROUND(r.costo) costo_mxn,
  ROUND(r.entrega, 1) entrega_pct, ROUND(r.apertura, 2) apertura_pct, ROUND(r.clic, 2) clic_pct, ROUND(r.respuesta, 2) respuesta_pct, ROUND(r.bajas_por_mil, 2) bajas_por_mil,
  ROUND(r.conv) conv_ref, ROUND(1000.0*r.conv/r.envios, 2) conv_por_mil_ref, ROUND(r.costo/NULLIF(r.conv,0), 1) costo_por_conv_ref,
  r.meses, r.versiones, strftime(r.primer_mes, '%Y-%m') primer_mes, strftime(r.ultimo_mes, '%Y-%m') ultimo_mes,
  CASE WHEN strftime(r.ultimo_mes, '%Y-%m') = '2026-09' THEN 1 ELSE 0 END AS activo_sep,
  ROUND(m.p50_resp, 2) AS mediana_canal_resp,
  CASE WHEN r.team = 'Collections' THEN 'cobranza'
       WHEN r.familia LIKE 'Transaccional%' OR NOT regexp_matches(r.familia, '-[A-Z]?[BTS]0?\d{3,5}-') THEN 'transaccional u operativa'
       ELSE 'promocional o lifecycle' END AS tipo,
  CASE WHEN r.envios >= m.p50_env AND (
          (r.canal='email' AND r.respuesta < 0.3)
       OR (r.canal='push notification' AND r.respuesta < 0.75)
       OR (r.canal='whatsapp' AND r.respuesta < 60)
       OR (r.canal='in-app' AND r.respuesta < 10)) THEN 'apagar o rehacer'
       WHEN r.envios >= m.p50_env AND (r.respuesta < m.p50_resp OR r.bajas_por_mil >= 2.5) THEN 'revisar'
       WHEN r.envios >= m.p50_env AND r.respuesta >= 1.5*m.p50_resp THEN 'proteger'
       WHEN r.envios < m.p50_env AND r.envios >= 1000 AND r.respuesta >= 2*m.p50_resp THEN 'escalar'
       ELSE '' END AS senal,
  CASE WHEN r.envios >= m.p50_env AND r.bajas_por_mil >= 2.5 AND r.respuesta < m.p50_resp THEN 'respuesta baja y bajas altas'
       WHEN r.envios >= m.p50_env AND r.bajas_por_mil >= 2.5 THEN 'bajas altas'
       WHEN r.envios >= m.p50_env AND r.respuesta < m.p50_resp THEN 'respuesta baja'
       WHEN r.envios >= m.p50_env AND r.respuesta >= 1.5*m.p50_resp THEN 'respuesta alta con volumen'
       WHEN r.envios < m.p50_env AND r.envios >= 1000 AND r.respuesta >= 2*m.p50_resp THEN 'respuesta alta sin volumen'
       ELSE '' END AS motivo,
  CASE WHEN r.canal = 'whatsapp' THEN ROUND(r.ws - r.wd) ELSE 0 END AS wa_no_entregado_mxn
FROM r JOIN med m ON m.canal = r.canal
)
SELECT s.*,
  CASE WHEN senal = 'apagar o rehacer' THEN costo_mxn ELSE 0 END AS ahorro_mxn_periodo,
  CASE WHEN senal = 'apagar o rehacer' AND activo_sep = 1 THEN ROUND(costo_mxn / meses) ELSE 0 END AS ahorro_mxn_mes,
  CASE WHEN senal = 'apagar o rehacer' AND activo_sep = 1 THEN envios_mes_prom ELSE 0 END AS msgs_mes_ahorrados
FROM s
ORDER BY ahorro_mxn_mes DESC, ahorro_mxn_periodo DESC, costo_mxn DESC, envios DESC;
