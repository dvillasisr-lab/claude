-- Queries de la muestra del lente B (canales), corridas con DuckDB sobre los CSV de data/.
-- Periodo: meses enero a septiembre 2026 (9 meses completos). Semanas: solo las 38 completas, del 5 de enero al 27 de septiembre.

-- Q1. Mix, costo y tasas por canal, todo el periodo
SELECT canal, SUM(envios) AS envios, ROUND(100.0*SUM(envios)/SUM(SUM(envios)) OVER (),1) AS pct_envios,
  SUM(costo_mxn) AS costo_mxn, ROUND(100.0*SUM(costo_mxn)/SUM(SUM(costo_mxn)) OVER (),1) AS pct_costo,
  SUM(conversiones_fraccional) AS conv, ROUND(SUM(costo_mxn)/NULLIF(SUM(conversiones_fraccional),0),2) AS costo_por_conv,
  ROUND(1000.0*SUM(conversiones_fraccional)/SUM(envios),2) AS conv_por_mil
FROM e1 WHERE envios > 0 GROUP BY canal ORDER BY envios DESC;

-- Q2. Serie mensual por canal con tasas
SELECT periodo, canal, envios, usuarios_aprox, costo_mxn,
  ROUND(100.0*email_delivery/NULLIF(email_sent,0),1) AS entrega_email,
  ROUND(100.0*email_open/NULLIF(email_delivery,0),1) AS apertura_email,
  ROUND(100.0*email_click/NULLIF(email_delivery,0),2) AS clic_email,
  ROUND(100.0*bajas_email_usuarios/NULLIF(usuarios_email_entregado,0),2) AS baja_email_usuarios,
  ROUND(100.0*pn_open/NULLIF(pn_send,0),2) AS apertura_push,
  ROUND(100.0*whatsapp_delivery/NULLIF(whatsapp_send,0),1) AS entrega_wa,
  ROUND(100.0*whatsapp_read/NULLIF(whatsapp_delivery,0),1) AS lectura_wa,
  ROUND(100.0*in_app_click/NULLIF(in_app_impression,0),1) AS clic_inapp
FROM e4a WHERE grano='mes' ORDER BY periodo, canal;

-- Q3. Serie semanal total (semanas completas)
SELECT periodo, SUM(envios) AS envios, SUM(costo_mxn) AS costo_mxn,
  SUM(CASE WHEN canal='email' THEN envios END) AS email, SUM(CASE WHEN canal='push notification' THEN envios END) AS push,
  SUM(CASE WHEN canal='whatsapp' THEN envios END) AS whatsapp, SUM(CASE WHEN canal='in-app' THEN envios END) AS inapp,
  SUM(bajas_email_usuarios) AS bajas_usuarios
FROM e4a WHERE grano='semana' AND periodo BETWEEN DATE '2026-01-05' AND DATE '2026-09-21' GROUP BY periodo ORDER BY periodo;

-- Q4. Concentración mensual: % de mensajes que reciben los usuarios con 41 o más al mes
SELECT mes, SUM(usuarios) AS usuarios, SUM(msgs) AS msgs,
  ROUND(100.0*SUM(CASE WHEN banda_msgs_mes IN ('41-80','081-160','161+') THEN usuarios END)/SUM(usuarios),1) AS pct_usuarios_41mas,
  ROUND(100.0*SUM(CASE WHEN banda_msgs_mes IN ('41-80','081-160','161+') THEN msgs END)/SUM(msgs),1) AS pct_msgs_41mas,
  SUM(CASE WHEN banda_msgs_mes IN ('41-80','081-160','161+') THEN usuarios END) AS usuarios_41mas
FROM e4b GROUP BY mes ORDER BY mes;

-- Q5. WhatsApp: costo de lo que no se entrega
SELECT SUM(whatsapp_send) AS enviados, SUM(whatsapp_delivery) AS entregados, SUM(whatsapp_send)-SUM(whatsapp_delivery) AS no_entregados,
  ROUND(100.0*(SUM(whatsapp_send)-SUM(whatsapp_delivery))/SUM(whatsapp_send),1) AS pct_no_entregado,
  (SUM(whatsapp_send)-SUM(whatsapp_delivery))*1.00 AS costo_no_entregado_mxn
FROM e1 WHERE canal='whatsapp';

-- Q6. WhatsApp por mes: entrega
SELECT periodo, whatsapp_send, whatsapp_delivery, ROUND(100.0*whatsapp_delivery/whatsapp_send,1) AS entrega, (whatsapp_send-whatsapp_delivery)*1.0 AS costo_perdido
FROM e4a WHERE grano='mes' AND canal='whatsapp' ORDER BY periodo;

-- Q7. Email junio: el envío de BillPay contra el resto del mes
SELECT CASE WHEN communication_name LIKE '%BillPay_Intro%' THEN 'BillPay intro' ELSE 'Resto email junio' END AS grupo,
  SUM(envios) AS envios, SUM(email_delivery) AS entregados, ROUND(100.0*SUM(email_open)/SUM(email_delivery),1) AS apertura,
  ROUND(100.0*SUM(email_click)/SUM(email_delivery),2) AS clic, SUM(email_unsubscribe) AS bajas_eventos, SUM(costo_mxn) AS costo_mxn,
  ROUND(1000.0*SUM(email_unsubscribe)/SUM(envios),2) AS bajas_por_mil
FROM e1 WHERE canal='email' AND CAST(mes AS DATE) = DATE '2026-06-01' GROUP BY 1;

-- Q8. Push: comunicaciones con más de 1 M de envíos y apertura menor a 1 %
SELECT communication_name, team, product_service, SUM(envios) AS envios, ROUND(100.0*SUM(pn_open)/SUM(envios),2) AS apertura
FROM e1 WHERE canal='push notification' GROUP BY 1,2,3 HAVING SUM(envios) > 1000000 AND SUM(pn_open)/SUM(envios) < 0.01 ORDER BY envios DESC LIMIT 15;

-- Q9. Push total: % de envíos en comunicaciones con apertura < 1 %
WITH c AS (SELECT communication_id, SUM(envios) e, SUM(pn_open) o FROM e1 WHERE canal='push notification' GROUP BY 1)
SELECT SUM(e) AS envios, SUM(CASE WHEN o/e < 0.01 THEN e END) AS envios_apertura_menor_1, ROUND(100.0*SUM(CASE WHEN o/e < 0.01 THEN e END)/SUM(e),1) AS pct FROM c WHERE e>0;

-- Q10. Costo por conversión por canal, solo Cash (donde hay conversión)
SELECT canal, SUM(envios) AS envios, SUM(costo_mxn) AS costo_mxn, ROUND(SUM(conversiones_fraccional)) AS conv,
  ROUND(SUM(costo_mxn)/NULLIF(SUM(conversiones_fraccional),0),2) AS costo_por_conv, ROUND(SUM(monto_fraccional)/1e6,1) AS monto_mdp
FROM e1 WHERE product_service='Cash' AND envios>0 GROUP BY canal ORDER BY envios DESC;
