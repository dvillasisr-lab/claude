"""Lámina 29: ficha de Sales (incluye B2B)."""
import re
from ficha import *
x = e1(); t = x[(x.equipo == 'Sales') & (x.canal != 'banner')]
R_ = lambda p: (lambda n: bool(re.search(p, n.lower())))
FILAS = [('Comercio del día', R_('comerciodel')),
         ('Hot Sale y códigos KUESKI', R_('hotsale|kueskipromo|codigo|kueski30|nuevo30')),
         ('Amazon y Temu', R_('amazon|temu')),
         ('Lanzamientos de comercios', R_('palacio|huawei|granvia|gran_via|lanzamiento')),
         ('Todo el portafolio', R_('portafolioactivo'))]
def toques(c):
    z = t[(t.familia == c['familia']) & (t.canal == c['canal'])]
    return f"{(z.envios.sum() / z.usuarios_aprox.sum()):.0f} push por persona en el mes"
MEJ = [('Amazon a clientes recurrentes', 'B0415-CANVAS-Recurrentes-Amazon', 'push notification', None),
       ('Quincenas sin intereses', 'B0345-CANVAS-Recurrentes-Quincenas', 'push notification', None),
       ('Flash Sale de Amazon por WhatsApp', 'B0416-CANVAS-Recurrentes-FlashSaleAmazon', 'whatsapp', mxn_wa)]
PEO = [('Promociones a todo el portafolio', 'B0335-CANVAS-Recurrentes_PortafolioActivo', 'email', lambda c: f"{c['costo']/1e6:.2f} M MXN en correos"),
       ('Temu de febrero a recurrentes', 'B0368-CANVAS-Recurrentes-TemuFebrero', 'email', None),
       ('Comercio del día de septiembre', 'ComerciodeldiaSeptiembre', 'push notification', toques)]
svg, cel, tot, det, d = build('Sales', FILAS, MEJ, PEO, 'Sales: qué manda, por qué canal y cuánto le responden', 'Otros comercios')
print(tot.assign(env=tot.env / 1e6, costo=tot.costo / 1e6).round(2))
print(cel.assign(env=cel.env / 1e6).round(2)[['fila', 'canal', 'env', 'r']].to_string())
for k, c in det.items(): print(k, round(c['env'] / 1e6, 2), round(c['resp'], 2), round(c['costo'] / 1e6, 2), 'entrega', round(c['entrega'], 1))
for eq in ['Sales', 'Marketing', 'Product Growth', 'Others', 'Collections']:
    z = x[x.equipo == eq]; em = z[z.canal == 'email']; wa = z[z.canal == 'whatsapp']
    print(eq, 'email clic %.2f' % (100 * em.email_click.sum() / em.email_delivery.sum()), 'WA lect %.1f entrega %.1f' % (100 * wa.whatsapp_read.sum() / max(wa.whatsapp_delivery.sum(), 1), 100 * wa.whatsapp_delivery.sum() / max(wa.whatsapp_send.sum(), 1)))
print('Sales bajas/mil %.2f; WA %% costo %.0f' % (1000 * t.email_unsubscribe.sum() / t.email_delivery.sum(), 100 * t.whatsapp_delivery.sum() / t.costo.sum()))
save(29, dict(kind='grafica',
  titulo='Sales manda promociones de comercios de KPay a sus clientes: funcionan por push y WhatsApp y no por correo',
  que='Casi todo (96 %) promociones de comercios que aceptan KPay: Comercio del día, Hot Sale y códigos de descuento KUESKI, Amazon, Temu, lanzamientos de tiendas (Palacio de Hierro, Huawei) y promociones a todo el portafolio.',
  quien='Sales (incluye B2B): 206 campañas con todas sus versiones, 30 activas en septiembre. 85 M mensajes (13 % del total) y 7.1 M MXN (12 % del gasto); 83 % de su gasto es WhatsApp.',
  a_quien='Clientes recurrentes de KPay 74 %, leads 15 % y ex clientes inactivos del portafolio 8 %.',
  lecturas=[
   'Su push y su WhatsApp a clientes recurrentes funcionan: Amazon abre 5.5 % en push y su WhatsApp es el que más se lee (78 %) y más se entrega (80 %) de los cinco equipos.',
   'Su correo no: 0.21 % de clic en 23.8 M correos, el más bajo de los cinco equipos. Por promoción va de 0.07 % (Hot Sale y códigos KUESKI) a 0.32 % (Comercio del día).',
   'Comercio del día llega 7 a 9 veces por persona al mes por push, y Marketing manda el mismo Comercio del día (17.7 M envíos contra 13.1 M de Sales), Hot Sale y Amazon.'],
  causa='El correo sigue siendo el canal por defecto para promociones que su gente ve en el celular, y Comercio del día sale casi a diario sin límite de mensajes por persona ni acuerdo con Marketing.',
  sowhat='Sales ya sabe a quién escribirle: le sobra el correo y le falta un límite al push diario (dos por semana a quien abrió uno en 60 días) y un solo calendario con Marketing.',
  fuente='Fuente: Braze, envíos por campaña, mes y canal, enero a septiembre 2026; campañas con 50 mil o más mensajes entregados. No medimos compras con KPay: falta extraer compra con KPay a 7 y 30 días por persona y campaña. Lectura de WhatsApp incluye las del mes siguiente.',
  svg=svg))
check(29)
