"""Lámina 28 (ronda 2): ficha de Marketing. Gráfica común en ficha2.py."""
from ficha2 import *
CASOS = [('Recordatorio de Veriff (registro)', 'B0000-CANVAS-Leads_LeftFunnel-Retargeting_Veriff', 'email', 'b', -5, -48, porpres),
         ('El mismo recordatorio por push', 'B0000-CANVAS-Leads_LeftFunnel-Retargeting_Veriff', 'push notification', 'b', -12, -34),
         ('Referidos a quien ya compró con KCash', 'Recurrentes_ClienteKCashCompraKCash', 'push notification', 'b', -12, -12),
         ('Rescate Tasa 0 a leads rezagados', 'B0171-CANVAS-Leads_BBDDRezagada-RescateTasa0', 'whatsapp', 'w', -20, 40, porpres),
         ('Narrativa Tasa 0 a leads rezagados', 'B0171-CANVAS-Leads_BBDDRezagada-NarrativaTasa0', 'whatsapp', 'w', -24, -16, porpres),
         ('Referidos a ex clientes dormidos', 'KCash-B0326-Canvas-Recurrentes_Dormants', 'email', 'w', -20, 30)]
svg, d, det = build('Marketing', CASOS)
for k, z in det.items(): print(k, z.canal, round(z.env / 1e6, 2), round(z.resp_pct, 2), round(z.vs_min, 2), round(z.costo / 1e6, 2), round(z.costo / max(z.convf, 1), 0))
save(28, dict(kind='grafica',
  titulo='Marketing gana con el recordatorio de registro y gasta la mitad de su dinero en Tasa 0 que casi no convierte',
  que='Tasa 0 y rescate de leads, referidos, promociones de KPay, recordatorio de registro.',
  quien='Marketing: 372 campañas, 262 M mensajes (39 %) y 27.2 M MXN (47 % del gasto).',
  a_quien='Leads 28 %, leads fríos 25 %, clientes 19 %, dormidos 7 %, registro a medias 7 %.',
  lecturas=[
   'Recordatorio de Veriff: 3.04 % de clic en 9.7 M correos y 5.83 % en push, a 21 MXN por préstamo o solicitud de Cash.',
   'Tasa 0 a leads: 51 % de su gasto (13.6 M MXN). Su WhatsApp se lee, pero cuesta 694 a 844 MXN por préstamo.',
   'Pierde suscriptores: 5.9 bajas por cada mil correos, más del doble que el resto de los equipos (2.6).'],
  causa='Mide si el mensaje se lee, no cuánto cuesta cada préstamo: el WhatsApp a leads fríos se lee y sigue saliendo.',
  sowhat='Mover el gasto de WhatsApp a leads fríos hacia el recordatorio de registro y los referidos a clientes.',
  fuente='Fuente: Braze, envíos por campaña, mes y canal, enero a septiembre 2026; campañas con 50 mil o más entregados. Préstamo o solicitud de Cash en 7 días: referencia, sin KPay.',
  svg=svg))
check(28)
