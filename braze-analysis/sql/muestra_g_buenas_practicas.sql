-- Muestra del lente G (buenas prácticas). DuckDB sobre data/e1_comunicacion_mes_canal.csv y data/e3_usuarios_distribucion.csv.
-- Clasifica cada comunicación por audiencia y gancho a partir del nombre, y compara respuesta, bajas y conversión de referencia.

-- Q0. Clasificación por nombre
CREATE TABLE a AS SELECT *,
 CASE WHEN communication_name ILIKE 'Collections%' OR communication_name ILIKE '%cobranza%' OR communication_name ILIKE '%BKT%' THEN 'cobranza'
      WHEN communication_name ILIKE 'Transaccional%' OR communication_name ILIKE '%payment%' OR communication_name ILIKE '%Contracts%' OR communication_name ILIKE '%disbursed%' THEN 'transaccional'
      WHEN communication_name ILIKE '%Dormant%' OR communication_name ILIKE '%Inactiv%' OR communication_name ILIKE '%Churn%' OR communication_name ILIKE '%Rezagad%' OR communication_name ILIKE '%Never%' THEN 'fríos: dormants, inactivos, rezagados, never active'
      WHEN communication_name ILIKE '%Leads%' OR communication_name ILIKE '%Anonim%' OR communication_name ILIKE '%Anónim%' OR communication_name ILIKE '%Registrad%' THEN 'leads y registrados sin crédito'
      WHEN communication_name ILIKE '%Nuevos%' OR communication_name ILIKE '%Onboarding%' OR communication_name ILIKE '%1er%' OR communication_name ILIKE '%1ra%' OR communication_name ILIKE '%Welcome%' THEN 'nuevos y onboarding'
      WHEN communication_name ILIKE '%Recurrente%' OR communication_name ILIKE '%Active%' OR communication_name ILIKE '%Activo%' OR communication_name ILIKE '%Cliente%' THEN 'clientes activos y recurrentes'
      ELSE 'otros' END audiencia,
 CASE WHEN communication_name ILIKE '%Tasa0%' OR communication_name ILIKE '%Tasa 0%' THEN 'tasa 0'
      WHEN communication_name ILIKE '%Descuento%' OR communication_name ILIKE '%Cupon%' OR communication_name ILIKE '%Cupón%' OR communication_name ILIKE '%Oferta%' THEN 'descuento, cupón u oferta'
      WHEN communication_name ILIKE '%Referral%' OR communication_name ILIKE '%AnotayGana%' THEN 'referidos'
      WHEN communication_name ILIKE '%Retargeting%' OR communication_name ILIKE '%Rescate%' OR communication_name ILIKE '%Recordatorio%' OR communication_name ILIKE '%Reminder%' THEN 'retargeting o recordatorio'
      WHEN communication_name ILIKE '%Lanzamiento%' OR communication_name ILIKE '%Intro%' OR communication_name ILIKE '%Newsletter%' OR communication_name ILIKE '%Recommendations%' THEN 'lanzamiento, novedades, newsletter'
      WHEN communication_name ILIKE '%XSell%' OR communication_name ILIKE '%Cross%' THEN 'cross sell'
      ELSE 'otros' END oferta
FROM e1;

-- Respuesta por canal (se repite en cada query)
--   CASE canal WHEN 'email' THEN 100.0*sum(email_click)/sum(email_delivery) WHEN 'push notification' THEN 100.0*sum(pn_open)/sum(pn_send)
--              WHEN 'whatsapp' THEN 100.0*sum(whatsapp_read)/sum(whatsapp_delivery) WHEN 'in-app' THEN 100.0*sum(in_app_click)/sum(in_app_impression) END

-- Q1. Fatiga por usuario (E3): eventos de baja de email por 100 usuarios según banda de mensajes
SELECT banda_msgs, sum(usuarios) usuarios, round(100.0*sum(usuarios)/(SELECT sum(usuarios) FROM e3),1) pct_usuarios, round(sum(msgs)/sum(usuarios),1) msgs_por_usuario,
  round(100.0*sum(bajas_email)/sum(usuarios),2) eventos_baja_por_100, round(100.0*sum(usuarios_con_conversion)/sum(usuarios),2) pct_conv, round(sum(costo_mxn)/sum(usuarios),1) costo_por_usuario
FROM e3 GROUP BY 1 ORDER BY min(msgs_p50);

-- Q2. Intensidad: mensajes de la misma comunicación por usuario en el mes vs respuesta (email y push)
SELECT canal, CASE WHEN envios/usuarios_aprox < 1.5 THEN '1' WHEN envios/usuarios_aprox < 2.5 THEN '2' WHEN envios/usuarios_aprox < 4.5 THEN '3 a 4' ELSE '5+' END toques_por_usuario_mes,
  count(*) comm_meses, sum(envios) envios,
  round(CASE canal WHEN 'email' THEN 100.0*sum(email_click)/sum(email_delivery) WHEN 'push notification' THEN 100.0*sum(pn_open)/sum(pn_send) END,2) respuesta,
  round(100.0*sum(email_open)/NULLIF(sum(email_delivery),0),1) apertura_email, round(1000.0*sum(email_unsubscribe)/NULLIF(sum(email_delivery),0),2) bajas_por_mil
FROM e1 WHERE canal IN ('email','push notification') AND usuarios_aprox > 1000 GROUP BY 1,2 ORDER BY 1,2;

-- Q3. Audiencia por canal
SELECT audiencia, canal, sum(envios) envios, round(sum(costo_mxn)) costo,
  round(CASE canal WHEN 'email' THEN 100.0*sum(email_click)/sum(email_delivery) WHEN 'push notification' THEN 100.0*sum(pn_open)/sum(pn_send) WHEN 'whatsapp' THEN 100.0*sum(whatsapp_read)/sum(whatsapp_delivery) WHEN 'in-app' THEN 100.0*sum(in_app_click)/sum(in_app_impression) END,2) respuesta,
  round(CASE canal WHEN 'email' THEN 100.0*sum(email_delivery)/sum(email_sent) WHEN 'whatsapp' THEN 100.0*sum(whatsapp_delivery)/sum(whatsapp_send) END,1) entrega,
  round(CASE canal WHEN 'email' THEN 1000.0*sum(email_unsubscribe)/sum(email_delivery) END,2) bajas_por_mil, round(1000.0*sum(conversiones_fraccional)/sum(envios),2) conv_por_mil_ref
FROM a WHERE canal IN ('email','push notification','whatsapp','in-app') GROUP BY 1,2 HAVING sum(envios) > 100000 ORDER BY canal, envios DESC;

-- Q4. Gancho por canal (promocionales)
SELECT oferta, canal, sum(envios) envios,
  round(CASE canal WHEN 'email' THEN 100.0*sum(email_click)/sum(email_delivery) WHEN 'push notification' THEN 100.0*sum(pn_open)/sum(pn_send) WHEN 'whatsapp' THEN 100.0*sum(whatsapp_read)/sum(whatsapp_delivery) WHEN 'in-app' THEN 100.0*sum(in_app_click)/sum(in_app_impression) END,2) respuesta,
  round(CASE canal WHEN 'email' THEN 1000.0*sum(email_unsubscribe)/sum(email_delivery) END,2) bajas_por_mil, round(1000.0*sum(conversiones_fraccional)/sum(envios),2) conv_por_mil_ref
FROM a WHERE canal IN ('email','push notification','whatsapp','in-app') AND audiencia NOT IN ('cobranza','transaccional') GROUP BY 1,2 HAVING sum(envios) > 100000 ORDER BY canal, envios DESC;

-- Q5. Tamaño de audiencia por envío vs respuesta (promocionales)
SELECT canal, CASE WHEN usuarios_aprox < 10000 THEN '<10 mil' WHEN usuarios_aprox < 100000 THEN '10 a 100 mil' WHEN usuarios_aprox < 1000000 THEN '100 mil a 1 M' ELSE '1 M+' END tamano, count(*) comm_meses, sum(envios) envios,
  round(CASE canal WHEN 'email' THEN 100.0*sum(email_click)/sum(email_delivery) WHEN 'push notification' THEN 100.0*sum(pn_open)/sum(pn_send) WHEN 'whatsapp' THEN 100.0*sum(whatsapp_read)/sum(whatsapp_delivery) END,2) respuesta,
  round(CASE canal WHEN 'email' THEN 1000.0*sum(email_unsubscribe)/sum(email_delivery) END,2) bajas_por_mil
FROM a WHERE canal IN ('email','push notification','whatsapp') AND audiencia NOT IN ('cobranza','transaccional') GROUP BY 1,2 ORDER BY 1,2;

-- Q6. Misma idea en un canal vs en varios (promocionales)
WITH fam AS (SELECT regexp_replace(communication_name,'-\d{8}-','-') familia, count(DISTINCT canal) canales FROM e1 WHERE envios > 0 GROUP BY 1)
SELECT e.canal, CASE WHEN f.canales = 1 THEN '1 canal' WHEN f.canales = 2 THEN '2 canales' ELSE '3+ canales' END canales, sum(envios) envios,
  round(CASE e.canal WHEN 'email' THEN 100.0*sum(email_click)/sum(email_delivery) WHEN 'push notification' THEN 100.0*sum(pn_open)/sum(pn_send) WHEN 'whatsapp' THEN 100.0*sum(whatsapp_read)/sum(whatsapp_delivery) WHEN 'in-app' THEN 100.0*sum(in_app_click)/sum(in_app_impression) END,2) respuesta,
  round(1000.0*sum(conversiones_fraccional)/sum(envios),2) conv_por_mil_ref
FROM a e JOIN fam f ON f.familia = regexp_replace(e.communication_name,'-\d{8}-','-')
WHERE e.canal IN ('email','push notification','whatsapp','in-app') AND audiencia NOT IN ('cobranza','transaccional') GROUP BY 1,2 ORDER BY 1,2;
