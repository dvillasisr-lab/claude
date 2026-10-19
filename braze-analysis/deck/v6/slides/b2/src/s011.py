"""Lámina 11 (ronda 2): Pareto de las 342 campañas de WhatsApp ordenadas por gasto: acumulado del gasto contra acumulado de
conversiones. Cada punto es una campaña, color por equipo; las más caras van nombradas."""
import math
from b2base import *

d = load_b()
w = d[d.canal == 'whatsapp']
CT, WT = d.costo.sum() / 1e6, w.costo.sum() / 1e6
VT, WV = d.envios.sum(), w.envios.sum()
fa = w.groupby('fam').agg(c=('costo', 'sum'), team=('equipo', 'first'), gan=('gan', 'first'), aud=('aud', 'first'),
                          conv=('conversiones_fraccional', 'sum')).sort_values('c', ascending=False).reset_index()
fa['cum'] = 100 * fa.c.cumsum() / fa.c.sum()
fa['cumv'] = 100 * fa.conv.cumsum() / fa.conv.sum()
fa['rk'] = np.arange(1, len(fa) + 1)
N50 = int((fa.cum < 50).sum() + 1)
top = fa.head(N50)
teams50 = top.team.value_counts()
eqc = w.groupby('equipo').costo.sum() / 1e6
mkpg = 100 * (eqc['Marketing'] + eqc['Product Growth']) / WT
print('WA', WT, CT, 100 * WT / CT, 'msgs', 100 * WV / VT, 'N50', N50, teams50.to_dict(), 'conv en esas', top.cumv.iloc[-1], 'mk+pg', mkpg)
print(top[['fam', 'c', 'team', 'gan', 'aud', 'cum', 'cumv']].assign(c=lambda x: x.c / 1e6).round(2).to_string())
r10 = fa.iloc[9]
print('top10', r10.cum, r10.cumv)

COL = {'Marketing': BLUE, 'Product Growth': GREEN, 'Sales': G1, 'Others': G1}
S = Svg(f'Curva de Pareto de las {len(fa)} campañas de WhatsApp ordenadas por gasto: acumulado del gasto contra acumulado de conversiones; '
        f'{N50} campañas suman la mitad del gasto.')
lx = 0
for lab, col in (('Marketing', BLUE), ('Product Growth', GREEN), ('Sales y Others', G1)):
    S.circle(lx + 5, 14, 5, col, '')
    S.t(lx + 14, 18, lab, 11.5, INK if col != G1 else TXT, w=600 if col != G1 else 400)
    lx += 14 + tw(lab, 11.5, 600) + 18
S.line(lx + 4, 14, lx + 26, 14, INK, 2)
S.t(lx + 32, 18, '% acumulado del gasto', 11.5, INK, w=600)
lx += 32 + tw('% acumulado del gasto', 11.5, 600) + 16
S.line(lx, 14, lx + 22, 14, G1, 2, ' stroke-dasharray="4 3"')
S.t(lx + 28, 18, '% acumulado de conversiones', 11.5, TXT)
X0, X1, Y0, Y1 = 50, 760, 50, 370
LO, HI = 0, math.log10(len(fa))
sx = lambda r: X0 + (X1 - X0) * (math.log10(r) - LO) / (HI - LO)
sy = lambda v: Y1 - (Y1 - Y0) * v / 100
for v in (0, 25, 50, 75, 100):
    S.line(X0, sy(v), X1, sy(v), GRID)
    S.t(X0 - 8, sy(v) + 4, f'{v} %', 11, SEC, 'end')
for r in (1, 3, 10, 30, 100, 300):
    S.line(sx(r), Y1, sx(r), Y1 + 4, G1)
    S.t(sx(r), Y1 + 17, f'{r}', 11, SEC, 'middle')
S.t(X1, Y1 + 34, f'Campañas de WhatsApp ordenadas de mayor a menor gasto ({len(fa)} en total, escala que crece por múltiplos)', 10.5, SEC, 'end')
# zona entre curvas para las N50
S.line(sx(N50), sy(0), sx(N50), sy(50), INK, 1, ' stroke-dasharray="3 3" opacity="0.6"')
S.line(X0, sy(50), sx(N50), sy(50), INK, 1, ' stroke-dasharray="3 3" opacity="0.6"')
pc = ' '.join(f'{sx(r):.1f},{sy(v):.1f}' for r, v in zip(fa.rk, fa.cumv))
S.raw(f'<polyline points="{pc}" fill="none" stroke="{G1}" stroke-width="2" stroke-dasharray="4 3"/>')
pg = ' '.join(f'{sx(r):.1f},{sy(v):.1f}' for r, v in zip(fa.rk, fa.cum))
S.raw(f'<polyline points="{pg}" fill="none" stroke="{INK}" stroke-width="1.6"/>')
for q in fa.itertuples():
    S.circle(sx(q.rk), sy(q.cum), 4.2 if q.rk <= N50 else 2.4, COL[q.team], ' stroke="#FFFFFF" stroke-width="1"')
S.t(sx(N50) + 8, sy(50) + 18, f'{N50} campañas: 50 % del gasto', 11.5, INK, w=700, halo=True)
S.t(sx(N50) + 8, sy(50) + 33, f'y {top.cumv.iloc[-1]:.0f} % de las conversiones', 11.5, TXT, halo=True)
NAMES = {0: 'Tasa 0 a leads rezagados (Marketing), 4.0 M MXN', 1: 'Rescate Tasa 0 a rezagados (Marketing), 3.3 M MXN',
         2: 'Ex clientes de un año (Product Growth), 1.7 M MXN'}
for i, lab in NAMES.items():
    q = fa.iloc[i]
    x, y = sx(q.rk), sy(q.cum)
    ty = 92 + i * 30
    S.line(x, y - 5, x + 26, ty + 4, INK, 0.7)
    S.t(x + 30, ty + 8, f'{i+1}. {lab}', 11, INK, w=600, halo=True)
S.t(X1, sy(100) + 30, f'WhatsApp: {100*WV/VT:.0f} % de los mensajes y {100*WT/CT:.0f} % del gasto ({WT:.1f} M MXN)', 11.5, BLUE, 'end', 700, halo=True)
svg = S.done()
# confirma los nombres con las cifras
for i in NAMES:
    print(NAMES[i], fa.iloc[i].fam, round(fa.iloc[i].c / 1e6, 2))

save(11, dict(
    kind='grafica',
    titulo=f'Siete de cada diez pesos van a WhatsApp, y la mitad de ese gasto se concentra en {N50} campañas',
    que='Promociones: Tasa 0, referidos, descuentos y ofertas de comercios de KPay.',
    quien=f'Marketing y Product Growth ponen {mkpg:.0f} % del gasto de WhatsApp; Sales el resto.',
    a_quien='Leads rezagados, ex clientes, leads recientes y clientes activos de KPay y KCash.',
    lecturas=[
        f'{100*WT/CT:.0f} % del gasto ({WT:.1f} M MXN) por {100*WV/VT:.0f} % de los mensajes: un WhatsApp cuesta 20 veces un correo.',
        f'{N50} campañas suman la mitad del gasto y solo {top.cumv.iloc[-1]:.0f} % de las conversiones; {teams50.get("Marketing",0)+teams50.get("Product Growth",0)} son de Marketing o Product Growth.',
        f'Las dos más caras son Tasa 0 a leads rezagados de Marketing: {(fa.c.iloc[0]+fa.c.iloc[1])/1e6:.1f} M MXN en nueve meses.',
    ],
    causa='Cada equipo manda por WhatsApp sus promociones grandes porque se lee más, sin presupuesto con límite ni regla de a quién.',
    sowhat='El gasto se decide en pocas campañas: revisar esas primero (siguiente lámina: a quién van).',
    fuente=f'{FUENTE_E1}. WhatsApp a 1.00 MXN por entregado, correo a 0.05 MXN por enviado. Conversión atribuida por Braze a 7 días.',
    svg=svg,
))
