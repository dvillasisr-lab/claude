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
def wq(v, w, q):
    o = np.argsort(v.values); v = v.values[o]; w = w.values[o]; c = np.cumsum(w) / w.sum(); return v[np.searchsorted(c, q)]
CASOS = [('B0171-CANVAS-Leads_BBDDRezagada-NarrativaTasa0', '2026-01', 'Narrativa Tasa 0, enero'),
         ('B0341-CANVAS-Todos_LeadsyRecurrentesKCash-Newsletter', '2026-01', 'Boletín a toda la base, enero'),
         ('B0000-CANVAS-Leads_LeftFunnel-Retargeting_Veriff', '2026-09', 'Recordatorio de Veriff, septiembre'),
         ('BillPay_Intro_Full_Rollout', '2026-06', 'Lanzamiento de BillPay, junio'),
        ]
S = Svg('Bajas por mil correos por campaña y mes según a quién se escribe')
S.t(0, 16, 'Bajas por cada mil correos entregados; cada punto es una campaña en un mes', 12.5, INK, w=600)
S.c(6, 34, 5, BLUE, stroke='none', op=0.55); S.t(15, 38, 'No ha hecho nada reciente', 11.5)
S.c(176, 34, 5, GREEN, stroke='none', op=0.55); S.t(185, 38, 'Hizo algo hace poco', 11.5)
S.r(318, 29, 22, 11, '#E4EAFB'); S.t(345, 38, 'mitad central de los correos', 11.5)
S.r(520, 28, 2.5, 12, INK); S.t(528, 38, 'promedio del grupo', 11.5)
X0, X1 = 160, 770; VM = 10
xs = lambda v: X0 + (X1 - X0) * min(v, VM) / VM
TOP, RH = 62, 27
YB = TOP + RH * len(g)
for v in (0, 2, 4, 6, 8, 10):
    S.l(xs(v), TOP - 8, xs(v), YB - 6, GRID); S.t(xs(v), YB + 6, f'{v}' + (' o más' if v == 10 else ''), 10.5, SEC, 'end' if v == 10 else 'middle')
rmax = 8; vmax = 4e6
rad = lambda v: max(1.8, rmax * math.sqrt(min(v, vmax) / vmax))
for i, r in enumerate(g.itertuples()):
    cy = TOP + RH * i + 6
    con = r.seg in REC
    S.t(X0 - 10, cy + 4, SEGN.get(r.seg, r.seg), 11, INK, 'end', w=600 if r.bpm > 3 else 400)
    d = m[m.seg == r.seg]
    q1, q3 = wq(d.bpm, d.edel, 0.25), wq(d.bpm, d.edel, 0.75)
    S.r(xs(q1), cy - 9, max(xs(q3) - xs(q1), 1.5), 18, '#E4EAFB')
    for z in d.itertuples():
        S.c(xs(z.bpm), cy, rad(z.edel), GREEN if con else BLUE, stroke='#FFFFFF', sw=0.6, op=0.45)
    S.r(xs(r.bpm) - 1.25, cy - 9, 2.5, 18, INK)
    S.t(xs(r.bpm) + 4, cy - 9, f'{r.bpm:.2f}' if r.bpm < 1 else f'{r.bpm:.1f}', 10.5, INK, 'start', w=600, halo=True)
    for pat, mes, nm in CASOS:
        z = d[d.familia.str.contains(pat) & d.mes.str.startswith(mes)]
        if len(z):
            z = z.sort_values('edel', ascending=False).iloc[0]
            x = xs(z.bpm)
            S.c(x, cy, max(rad(z.edel), 4), GREEN if con else BLUE, op=1)
            if 'Boletín' in nm: S.t(x + 6, cy - 9, f'{nm}: {z.bpm:.1f}', 10.5, INK, 'start', w=600, halo=True)
            else: S.t(x + max(rad(z.edel), 4) + 5, cy + 4, f'{nm}: {z.bpm:.1f}', 10.5, INK, 'start', w=600, halo=True)
            print(nm, round(z.bpm, 2), round(z.edel / 1e6, 1))
S.t(X1, YB + 20, 'Bajas por mil correos entregados en el mes', 10.5, SEC, 'end')
svg = S.done()
save(25, dict(kind='grafica',
  titulo='Lo que más explica las bajas es a quién le escribimos y con qué oferta, no cuántas veces llega la campaña',
  que='Más bajas: recordatorio de registro, Tasa 0, BillPay, referidos. Menos: avisos y cobranza.',
  quien='Marketing (2.6 bajas por mil) y Product Growth (1.5) suman 73 % de las bajas medidas.',
  a_quien='Registro a medias y leads fríos se van más; clientes, avisos y cobranza, menos.',
  lecturas=[
   f"A quién se escribe explica {ETA['seg']*100:.0f} % de la diferencia en bajas entre campañas; el tema {ETA['tema']*100:.0f} %.",
   f"Las veces que la misma campaña llega en el mes explican solo {ETA['tq_b']*100:.0f} %, y el equipo {ETA['equipo']*100:.0f} %.",
   'Registro a medias: 4.1 bajas por mil correos; cobranza: 0.25, aunque recibe muchos correos.'],
  causa='Mandamos ofertas a gente sin relación reciente o recién registrada, que no las pidió.',
  sowhat='Para perder menos gente hay que cambiar a quién y qué se manda; el límite ayuda en el primer mes.',
  fuente='Fuente: Braze, correo por campaña y mes (E1), 866 campañas por mes con 20 mil o más entregados, enero a septiembre 2026. Diferencia explicada: varianza ponderada por entregados.',
  svg=svg))
check(25)
