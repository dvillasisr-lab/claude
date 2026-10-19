"""Lámina 30: ficha de Collections."""
import re
from ficha import *
x = e1(); t = x[(x.equipo == 'Collections') & (x.canal != 'banner')]
R_ = lambda p: (lambda n: bool(re.search(p, n.lower())))
FILAS = [('Precobranza', R_('precobranza')), ('Atraso menor (BKT1)', R_('bkt1')), ('Atraso mayor (BKT2 a BKT6)', R_('bkt[2-6]'))]
def toques(c):
    z = t[(t.familia == c['familia']) & (t.canal == c['canal'])]
    g = z.groupby('mes').agg(e=('envios', 'sum'), u=('usuarios_aprox', 'sum'))
    return f"{(g.e / g.u).mean():.1f} correos por persona al mes"
MEJ = [('Precobranza de KCash', 'KCash-T000-CANVAS-Precobranza-ecosystem', 'email', None),
       ('La misma precobranza por push', 'KCash-T000-CANVAS-Precobranza-ecosystem', 'push notification', None),
       ('Atraso menor (BKT1) por push', 'KCash-T000-CANVAS-BKT1', 'push notification', None)]
PEO = [('Atraso mayor (BKT3) por correo', 'KCash-T000-CANVAS-BKT3', 'email', toques),
       ('Atraso mayor (BKT2) por correo', 'KCash-T000-CANVAS-BKT2', 'email', toques),
       ('Atraso menor (BKT1) por correo', 'KCash-T000-CANVAS-BKT1', 'email', toques)]
svg, cel, tot, det, d = build('Collections', FILAS, MEJ, PEO, 'Collections: qué manda, por qué canal y cuánto le responden', 'Otros')
print(tot.assign(env=tot.env / 1e6, costo=tot.costo / 1e6).round(2))
print(cel.assign(env=cel.env / 1e6).round(2)[['fila', 'canal', 'env', 'r']].to_string())
for k, c in det.items(): print(k, round(c['env'] / 1e6, 2), round(c['resp'], 2))
b = d[d.familia.str.lower().str.contains('bkt[2-6]', regex=True) & (d.canal == 'email')]
print('BKT2-6 email %.1f M, rango %.2f a %.2f' % (b.env.sum() / 1e6, b[b.env > 3e5].resp_pct.min(), b[b.env > 3e5].resp_pct.max()))
tb = t[t.familia.str.lower().str.contains('bkt[2-6]', regex=True) & (t.canal == 'email')].groupby(['familia', 'mes']).agg(e=('envios', 'sum'), u=('usuarios_aprox', 'sum'))
print('toques BKT2-6 %.1f a %.1f' % ((tb.e / tb.u).groupby(level=0).mean().min(), (tb.e / tb.u).groupby(level=0).mean().max()))
print('bajas/mil %.2f' % (1000 * t.email_unsubscribe.sum() / t.email_delivery.sum()))
save(30, dict(kind='grafica',
  titulo='Collections enseña a escribir con una razón y una fecha; lo que puede mejorar es la cobranza avanzada por correo',
  que='Cobranza: precobranza antes del vencimiento y cobranza por etapa de atraso (BKT1 a BKT6) de KCash, KPay e Installments.',
  quien='Collections: 23 campañas, 22 activas en septiembre. 44.7 M mensajes (7 % del total) y 1.6 M MXN (3 % del gasto). No usa WhatsApp.',
  a_quien='Cartera con un pago por vencer o vencido (99.5 % de sus mensajes): personas con un préstamo y una fecha de pago.',
  lecturas=[
   'Escribe por un evento con fecha y solo a quien le aplica: la precobranza de KCash tiene 4.3 % de clic en correo y 5.3 % de apertura en push, de lo mejor de la empresa con millones de envíos.',
   'Lo que puede mejorar es la cobranza avanzada por correo: BKT2 a BKT6 de KCash suman 12.1 M correos con 1.1 a 1.8 clics por cada mil, y le llegan a cada persona 4 a 6 veces al mes.',
   'El mismo BKT1 responde casi ocho veces más por push (3.1 %) que por correo (0.41 %). Casi nadie se da de baja: 0.25 por cada mil correos, 24 veces menos que Marketing.'],
  causa='Funciona porque cada mensaje sale por una razón con fecha (el vencimiento), a la persona exacta y con una acción clara. En atrasos mayores repite el correo aunque la persona ya no lo abra.',
  sowhat='Lo que hace Collections (razón, fecha, persona exacta) es la regla para las ofertas; su ajuste es pasar la cobranza avanzada a push y mandar menos correos por persona.',
  fuente='Fuente: Braze, envíos por campaña, mes y canal, enero a septiembre 2026; campañas con 50 mil o más mensajes entregados. En cobranza el resultado es el pago y no está en Braze: falta la tabla de pagos por canal y etapa. Correos por persona: envíos entre usuarios del mes.',
  svg=svg))
check(30)
