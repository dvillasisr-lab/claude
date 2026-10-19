"""Lámina 28: ficha de Marketing."""
from ficha import *
x = e1(); t = x[(x.equipo == 'Marketing') & (x.canal != 'banner')]
T = lambda n: tema_of(n)
FILAS = [('Tasa 0 y rescate de leads', lambda n: T(n) == 'Tasa 0 y rescate de leads'),
         ('Referidos', lambda n: T(n) == 'Referidos'),
         ('Promociones de KPay', lambda n: T(n) == 'Promos de comercios KPay'),
         ('Recordatorio de registro', lambda n: T(n) == 'Recordatorio de registro')]
MEJ = [('Recordatorio de Veriff (registro)', 'B0000-CANVAS-Leads_LeftFunnel-Retargeting_Veriff', 'email', mxn_conv),
       ('El mismo recordatorio por push', 'B0000-CANVAS-Leads_LeftFunnel-Retargeting_Veriff', 'push notification', None),
       ('Referidos a quien ya compró con KCash', 'Recurrentes_ClienteKCashCompraKCash', 'email', mxn_conv)]
PEO = [('Narrativa Tasa 0 a leads rezagados', 'B0171-CANVAS-Leads_BBDDRezagada-NarrativaTasa0', 'whatsapp', mxn_conv),
       ('Rescate Tasa 0 a leads rezagados', 'B0171-CANVAS-Leads_BBDDRezagada-RescateTasa0', 'whatsapp', mxn_conv),
       ('Referidos a ex clientes dormidos', 'KCash-B0326-Canvas-Recurrentes_Dormants', 'email', lambda c: f"{c['costo']/1e6:.2f} M MXN · {c['bajas']:.1f} bajas por cada mil correos")]
svg, cel, tot, det, d = build('Marketing', FILAS, MEJ, PEO, 'Marketing: qué manda, por qué canal y cuánto le responden', 'Concursos, boletín y otros')
print(tot.assign(env=tot.env / 1e6, costo=tot.costo / 1e6, sh=100 * tot.costo / tot.costo.sum()).round(2))
print(cel.assign(env=cel.env / 1e6, costo=cel.costo / 1e6).round(2)[['fila', 'canal', 'env', 'r', 'costo']].to_string())
for k, c in det.items(): print(k, round(c['env'] / 1e6, 2), round(c['resp'], 2), round(c['costo'] / 1e6, 2), round(c['costo'] / max(c['convf'], 1), 1), 'entrega', round(c['entrega'], 1))
o = x[(x.equipo != 'Marketing') & (x.canal == 'email')]
print('bajas/mil Mkt %.2f resto %.2f' % (1000 * t.email_unsubscribe.sum() / t.email_delivery.sum(), 1000 * o.email_unsubscribe.sum() / o.email_delivery.sum()))
g = t.groupby('tema').agg(c=('costo', 'sum'), v=('conversiones_fraccional', 'sum'), u=('email_unsubscribe', 'sum'), e=('email_delivery', 'sum'))
print((g.c / g.v).round(1).to_dict()); print((1000 * g.u / g.e).round(2).to_dict())
print('WA %.1f M MXN (%.0f %%), conv %.0f, MXN/conv %.1f' % (t.whatsapp_delivery.sum() / 1e6, 100 * t.whatsapp_delivery.sum() / t.costo.sum(), t.conversiones_fraccional.sum(), t.costo.sum() / t.conversiones_fraccional.sum()))
save(28, dict(kind='grafica',
  titulo='Marketing gana con el recordatorio de registro y gasta la mitad de su dinero en Tasa 0 para leads que casi no convierten',
  que='Todo ofertas: Tasa 0 y rescate de leads (32 % de sus mensajes), referidos (26 %), promociones de comercios que aceptan KPay (25 %) y el recordatorio de terminar el registro (7 %); el resto, concursos, boletín y BillPay.',
  quien='Marketing: 372 campañas con todas sus versiones, 70 activas en septiembre. 262 M mensajes (39 % del total) y 27.2 M MXN (47 % del gasto) en nueve meses.',
  a_quien='Leads 28 %, leads fríos (rezagados y anónimos) 25 %, clientes activos y recurrentes 19 %, ex clientes dormidos 7 %, quien dejó el registro a medias 7 % y envíos a toda la base 6 %.',
  lecturas=[
   'Lo que le funciona: el recordatorio de terminar el registro (Veriff) tiene 3.04 % de clic en 9.7 M correos y 5.83 % de apertura en push, a 21 MXN por préstamo o solicitud de Cash.',
   'Tasa 0 a leads se lleva 51 % de su gasto (13.6 M MXN), casi todo en WhatsApp. Se lee (70 %), pero cada préstamo o solicitud cuesta 158 MXN, contra 22 de referidos y 14 del recordatorio.',
   'Pierde suscriptores: 5.9 bajas por cada mil correos, más del doble que el resto de los equipos (2.6); su Tasa 0 por correo llega a 8.8 bajas por mil.'],
  causa='Mide si el mensaje se lee o se abre, no cuánto cuesta cada préstamo que trae: el WhatsApp a leads fríos se lee y por eso sigue saliendo, aunque casi no convierta.',
  sowhat='Marketing no necesita mandar más: necesita mover su gasto de WhatsApp a leads fríos hacia el recordatorio de registro y los referidos a clientes, que ya le regresan.',
  fuente='Fuente: Braze, envíos por campaña, mes y canal, enero a septiembre 2026; campañas con 50 mil o más mensajes entregados. Préstamo o solicitud de Cash en 7 días: referencia, solo Cash (no mide KPay ni altas por referido) y sin grupo de control. Lectura de WhatsApp incluye las del mes siguiente (Rescate Tasa 0: 57.7 % sin ellas).',
  svg=svg))
check(28)
