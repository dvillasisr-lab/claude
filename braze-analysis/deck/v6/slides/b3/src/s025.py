"""Lámina 25: bajas por mil correos entregados por campaña y mes (E1, correo, 20 mil o más entregados en el mes), por segmento;
panel lateral: parte de la diferencia en bajas que explica cada factor (varianza ponderada por entregados). Misma lógica que p2work/t3.py."""
import math
from datos import *
from svgk import *
x = e1()
m = x[(x.canal == 'email') & (x.email_delivery >= 20000)].copy()
m = m.groupby(['familia', 'mes', 'equipo', 'tema', 'seg', 'tipo']).agg(edel=('email_delivery', 'sum'), bajas=('email_unsubscribe', 'sum'),
     usr=('usuarios_aprox', 'sum'), env=('envios', 'sum')).reset_index()
m['toques'] = m.env / m.usr; m['bpm'] = 1000 * m.bajas / m.edel
m['tq_b'] = pd.cut(m.toques, [0, 1.05, 2, 3, 5, 8, 100], labels=['1', '1-2', '2-3', '3-5', '5-8', '8+'])
m['size_b'] = pd.cut(m.usr, [0, 1e5, 5e5, 1e6, 3e6, 1e9], labels=['a', 'b', 'c', 'd', 'e'])
w = m.edel; mu = np.average(m.bpm, weights=w); sst = np.sum(w * (m.bpm - mu) ** 2)
ETA = {}
for k in ['seg', 'tema', 'equipo', 'size_b', 'tq_b']:
    gm = m.groupby(k, observed=True).apply(lambda d: np.average(d.bpm, weights=d.edel))
    ETA[k] = np.sum(w * (m[k].map(gm).astype(float) - mu) ** 2) / sst
print(len(m), {k: round(v, 3) for k, v in ETA.items()})
g = m.groupby('seg').agg(edel=('edel', 'sum'), bajas=('bajas', 'sum')).reset_index(); g['bpm'] = 1000 * g.bajas / g.edel
g = g.sort_values('bpm', ascending=False); print(g.round(2).to_string())
t = m.groupby('tema').agg(edel=('edel', 'sum'), bajas=('bajas', 'sum')); print((1000 * t.bajas / t.edel).round(2).sort_values().to_dict())
q = m.groupby('tq_b', observed=True).agg(edel=('edel', 'sum'), bajas=('bajas', 'sum')); print((1000 * q.bajas / q.edel).round(2).to_dict())
p = m.groupby('tipo').agg(edel=('edel', 'sum'), bajas=('bajas', 'sum')); print((100 * p / p.sum()).round(1))
SEGN = {'Leads en registro': 'Dejó el registro a medias', 'Leads fríos (rezagados, anónimos)': 'Leads fríos', 'Leads': 'Leads',
        'Leads recientes': 'Leads recientes', 'Todos (masivo)': 'Toda la base', 'Evento o sin segmento': 'Sin segmento',
        'Clientes activos y recurrentes': 'Clientes activos', 'Churn (12 meses sin uso)': 'Ex clientes (churn)',
        'Inactivos y dormants': 'Inactivos y dormidos', 'Registrados sin crédito': 'Registrados sin crédito',
        'Evento (transaccional)': 'Avisos de pago y cuenta', 'Cartera en cobranza': 'Cobranza'}
S = Svg('Bajas por mil correos por campaña y mes según a quién se escribe, y qué parte de la diferencia explica cada factor')
S.t(0, 16, 'Bajas por cada mil correos entregados; cada punto es una campaña en un mes', 12.5, INK, w=600)
S.c(6, 34, 5, BLUE, stroke='none', op=0.55); S.t(15, 38, 'No ha hecho nada reciente', 11.5)
S.c(176, 34, 5, GREEN, stroke='none', op=0.55); S.t(185, 38, 'Hizo algo hace poco', 11.5)
S.r(318, 28, 2.5, 12, INK); S.t(326, 38, 'Promedio del grupo', 11.5)
X0, X1 = 150, 470; VM = 12
xs = lambda v: X0 + (X1 - X0) * min(v, VM) / VM
TOP, RH = 62, 26.5
YB = TOP + RH * len(g)
for v in (0, 3, 6, 9, 12):
    S.l(xs(v), TOP - 8, xs(v), YB - 6, GRID); S.t(xs(v), YB + 6, f'{v}' + (' o más' if v == 12 else ''), 10.5, SEC, 'middle')
rmax = 9; vmax = 4e6
rad = lambda v: max(1.8, rmax * math.sqrt(min(v, vmax) / vmax))
for i, r in enumerate(g.itertuples()):
    cy = TOP + RH * i + 6
    con = r.seg in REC
    S.t(X0 - 10, cy + 4, SEGN.get(r.seg, r.seg), 11, INK, 'end', w=600 if r.bpm > 3 else 400)
    d = m[m.seg == r.seg]
    for z in d.itertuples():
        S.c(xs(z.bpm), cy, rad(z.edel), GREEN if con else BLUE, stroke='#FFFFFF', sw=0.6, op=0.45)
    S.r(xs(r.bpm) - 1.25, cy - 8, 2.5, 16, INK)
    S.t(xs(r.bpm) + 5, cy - 3, f'{r.bpm:.2f}' if r.bpm < 1 else f'{r.bpm:.1f}', 10.5, INK, w=600, halo=True)
S.t(X1, YB + 20, 'Bajas por mil correos entregados en el mes', 10.5, SEC, 'end')
# panel lateral
PX0, PX1 = 560, 760
px = lambda v: PX0 + (PX1 - PX0) * v / 0.6
S.t(500, 66, 'Qué parte de la diferencia en bajas', 11.5, INK, w=600)
S.t(500, 80, 'entre campañas explica cada factor', 11.5, INK, w=600)
FAC = [('seg', 'A quién se escribe'), ('tema', 'Tema u oferta'), ('equipo', 'Equipo que lo manda'), ('size_b', 'Tamaño del envío'), ('tq_b', 'Veces que llega en el mes')]
for v in (0, 0.2, 0.4, 0.6):
    S.l(px(v), 98, px(v), 98 + 5 * 44 - 10, GRID); S.t(px(v), 98 + 5 * 44 + 4, f'{v*100:.0f} %', 10.5, SEC, 'middle')
for i, (k, nm) in enumerate(FAC):
    y = 112 + 44 * i
    hi = k in ('seg', 'tema')
    S.t(500, y - 6, nm, 11, INK, w=600 if hi else 400)
    S.l(px(0), y + 8, px(ETA[k]), y + 8, BLUE if hi else MRK, 2)
    S.c(px(ETA[k]), y + 8, 5, BLUE if hi else MRK)
    S.t(px(ETA[k]) + 9, y + 12, f'{ETA[k]*100:.0f} %', 11, INK, w=600)
S.t(500, 340, 'Los factores se traslapan;', 10.5, SEC); S.t(500, 354, 'no suman 100 %.', 10.5, SEC)
svg = S.done()
save(25, dict(kind='grafica',
  titulo='Lo que más explica que la gente se dé de baja es a quién le escribimos y con qué oferta, no cuántas veces llega la campaña',
  que='Las bajas altas vienen de los recordatorios diarios de terminar el registro, el lanzamiento de BillPay a toda la base, referidos, Installments y Tasa 0. Avisos de pago y cobranza casi no generan bajas.',
  quien='Marketing (2.6 bajas por mil correos en sus campañas por mes) y Product Growth (1.5) concentran 73 % de las bajas medidas.',
  a_quien='Más bajas: quien dejó el registro a medias, leads fríos, leads y envíos a toda la base. Menos: clientes activos, avisos de algo que la persona hizo y cobranza.',
  lecturas=[
   f"A quién se le escribe explica {ETA['seg']*100:.0f} % de la diferencia en bajas entre campañas y el tema {ETA['tema']*100:.0f} %; las veces que la misma campaña llega en el mes, solo {ETA['tq_b']*100:.0f} %.",
   'Quien dejó el registro a medias se da de baja 4.1 veces por cada mil correos y los leads fríos 3.5; los avisos de pago 0.65 y la cobranza 0.25, aunque reciben muchos correos.',
   'La frecuencia pesa sobre el recién llegado: quien se va en su primera semana recibió 4.4 correos en 3 días. Solo el correo registra la baja; en push y WhatsApp no sabemos quién se va.'],
  causa='Mandamos ofertas a gente sin relación reciente o recién registrada, que no las pidió. A eso se suman, en los nuevos, uno o dos correos diarios del recordatorio de registro.',
  sowhat='Para perder menos gente hay que cambiar a quién y qué se manda; el límite de mensajes por persona ayuda sobre todo en el primer mes.',
  fuente='Fuente: Braze, correo por campaña y mes (E1), 866 campañas por mes con 20 mil o más entregados, enero a septiembre 2026; bajas del mismo mes sobre entregados. Diferencia explicada: varianza ponderada por entregados. Quedan fuera 458 mil bajas en meses sin entrega de esa campaña. Primera semana: E8.',
  svg=svg))
check(25)
