"""Lámina 30 (ronda 2): ficha de Collections. Gráfica común en ficha2.py."""
from ficha2 import *
x = e1(); t = x[(x.equipo == 'Collections') & (x.canal != 'banner')]
def toques(z):
    g = t[(t.familia == z.familia) & (t.canal == z.canal)].groupby('mes').agg(e=('envios', 'sum'), u=('usuarios_aprox', 'sum'))
    return f"{(g.e / g.u).mean():.1f} por persona al mes"
CASOS = [('Precobranza de KCash', 'KCash-T000-CANVAS-Precobranza-ecosystem', 'email', 'b', -12, -30),
         ('La misma precobranza por push', 'KCash-T000-CANVAS-Precobranza-ecosystem', 'push notification', 'b', -12, -10),
         ('Atraso menor (BKT1) por push', 'KCash-T000-CANVAS-BKT1', 'push notification', 'b', 12, -26),
         ('Atraso mayor (BKT3) por correo', 'KCash-T000-CANVAS-BKT3', 'email', 'w', -12, 66, toques),
         ('Atraso mayor (BKT2) por correo', 'KCash-T000-CANVAS-BKT2', 'email', 'w', -12, 30, toques),
         ('Atraso menor (BKT1) por correo', 'KCash-T000-CANVAS-BKT1', 'email', 'w', -12, -24, toques)]
svg, d, det = build('Collections', CASOS)
for k, z in det.items(): print(k, z.canal, round(z.env / 1e6, 2), round(z.resp_pct, 2), round(z.vs_min, 2))
save(30, dict(kind='grafica',
  titulo='Collections enseña a escribir con una razón y una fecha; puede mejorar la cobranza avanzada por correo',
  que='Precobranza antes del vencimiento y cobranza por etapa de atraso (BKT1 a BKT6).',
  quien='Collections: 35 campañas por canal, 45 M mensajes (7 %), 1.6 M MXN. No usa WhatsApp.',
  a_quien='Personas con un préstamo y un pago por vencer o vencido.',
  lecturas=[
   'Precobranza de KCash: 4.3 % de clic en correo y 5.3 % de apertura en push, con millones de envíos.',
   'BKT2 a BKT6 de KCash: 12.1 M correos con 1.1 a 1.8 clics por cada mil, 4 a 6 por persona al mes.',
   'El mismo BKT1 responde casi ocho veces más por push (3.1 %) que por correo (0.41 %).'],
  causa='Funciona porque cada mensaje tiene una razón con fecha y va a la persona exacta; en atraso mayor repite el correo.',
  sowhat='Su regla (razón, fecha, persona exacta) sirve a las ofertas; su ajuste es pasar la cobranza avanzada a push.',
  fuente='Fuente: Braze, envíos por campaña, mes y canal, enero a septiembre 2026; campañas con 50 mil o más entregados. El pago por canal no está en Braze.',
  svg=svg))
check(30)
