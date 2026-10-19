"""Lámina 44 (base v5 lámina 29): clic de email según tamaño de envío por campaña, por día y equipo (E10 vía deck_data.regresion_dia);
recta de Product Growth, Marketing y Sales sobre el logaritmo del tamaño; lunes de Others con y sin BillPay Intro (E1)."""
import sys, math, pandas as pd
from kit import *
sys.path.insert(0, R + 'scripts')
import deck_data as dd
r = dd.regresion_dia(); fit = r['fit']
e = pd.read_csv(D + 'e10_dia_semana.csv'); e['T'] = e.team.map(team); em = e[e.canal == 'email']
d = em.groupby('dia_semana')[['email_entregados', 'respuestas']].sum(); d['clic'] = 100 * d.respuestas / d.email_entregados
d['sh'] = 100 * d.email_entregados / d.email_entregados.sum()
e1 = pd.read_csv(D + 'e1_comunicacion_mes_canal.csv')
bi = e1[(e1.canal == 'email') & e1.communication_name.str.contains('BillPay_Intro') & e1.mes.str.startswith('2026-06')].iloc[0]
mon = d.loc['Monday']; lun_sin = 100 * (mon.respuestas - bi.email_click) / (mon.email_entregados - bi.email_delivery)
sh_sin = 100 * (mon.email_entregados - bi.email_delivery) / (d.email_entregados.sum() - bi.email_delivery)
bi_sh = 100 * bi.email_delivery / mon.email_entregados
om = em[(em.dia_semana == 'Monday') & (em['T'] == 'Others')][['envios', 'comunicaciones', 'email_entregados', 'respuestas']].sum()
o_x = (om.envios - bi.envios) / (om.comunicaciones - 1); o_y = 100 * (om.respuestas - bi.email_click) / (om.email_entregados - bi.email_delivery)
mt = em[em.dia_semana == 'Monday'].groupby('T')[['email_entregados', 'respuestas']].sum(); mt['sh'] = 100 * mt.email_entregados / mt.email_entregados.sum(); mt['clic'] = 100 * mt.respuestas / mt.email_entregados
pg = {q['dia']: q for q in r['pts'] if q['g'] == 'Product Growth'}
pg_rest = em[(em['T'] == 'Product Growth') & (em.dia_semana != 'Monday')][['envios', 'comunicaciones', 'email_entregados', 'respuestas']].sum()
print(round(fit['r2'], 3), fit['n'], d.round(2).to_string(), lun_sin, sh_sin, bi_sh, o_x, o_y, mt.round(2).to_string(),
      pg_rest.envios / pg_rest.comunicaciones, 100 * pg_rest.respuestas / pg_rest.email_entregados, sep='\n')
COL = {'Product Growth': BLUE, 'Marketing': GREEN, 'Sales': INK, 'Collections': G1, 'Others': BLUE2}
S = Svg('Dispersión: clic de email según envíos por campaña, por día de la semana y equipo, escala logarítmica; rombos sábado y domingo; recta de Product Growth, Marketing y Sales; lunes de Others con y sin BillPay Intro')
lx = 0
for t in ['Product Growth', 'Marketing', 'Sales', 'Collections', 'Others']:
    S.circle(lx + 5, 15, 4.5, COL[t], '#FFFFFF', 1); S.t(lx + 13, 19, t, 11, TXT); lx += 22 + len(t) * 6.2
S.raw(f'<path d="M {lx+5} 10 L {lx+10} 15 L {lx+5} 20 L {lx} 15 Z" fill="{G1}"/>'); S.t(lx + 15, 19, 'sábado y domingo', 11, TXT)
S.t(0, 40, 'Cada punto es un día de la semana de un equipo (celdas con 50 mil o más correos entregados en 9 meses).', 10.5, SEC)
X0, X1, Y0, Y1 = 44, 770, 66, 362
lo, hi = math.log10(3000), math.log10(300000)
sx = lambda v: X0 + (X1 - X0) * (math.log10(v) - lo) / (hi - lo); sy = lambda v: Y1 - (Y1 - Y0) * v / 3.5
for v in (0, 1, 2, 3):
    S.line(X0, sy(v), X1, sy(v)); S.t(X0 - 6, sy(v) + 4, f'{v} %', 10.5, SEC, 'end')
for v, lab in ((5000, '5 mil'), (10000, '10 mil'), (25000, '25 mil'), (50000, '50 mil'), (100000, '100 mil'), (250000, '250 mil')):
    S.line(sx(v), Y1, sx(v), Y1 + 5, SEC); S.t(sx(v), Y1 + 18, lab, 10.5, SEC, 'middle')
S.line(X0, Y1, X1, Y1, SEC)
S.t((X0 + X1) / 2, Y1 + 34, 'Correos enviados por campaña ese día (escala logarítmica)', 10.5, SEC, 'middle')
S.t(X0 + 4, Y0 - 4, 'Clic de email', 11, SEC)
xa, xb = 4000, 55000
S.line(sx(xa), sy(fit['a'] + fit['b'] * math.log10(xa)), sx(xb), sy(fit['a'] + fit['b'] * math.log10(xb)), INK, 1.6)
S.t(sx(3300), sy(0.12), f'Recta de Product Growth, Marketing y Sales: R² {fit["r2"]:.2f}', 10.5, INK, 'start', 600, halo=True)
for q in sorted(r['pts'], key=lambda q: q['dia'] == 'Lun'):
    x, y = sx(q['x']), sy(min(q['y'], 3.45)); c = COL[q['g']]
    if q['mk'] == 'd':
        S.raw(f'<path d="M {x:.1f} {y-6:.1f} L {x+6:.1f} {y:.1f} L {x:.1f} {y+6:.1f} L {x-6:.1f} {y:.1f} Z" fill="{c}" stroke="#FFFFFF" stroke-width="1.5"/>')
    else:
        S.circle(x, y, 6 if q['dia'] == 'Lun' else 4.5, c, '#FFFFFF', 1.5)
# etiquetas de lunes
P = {(q['dia'], q['g']): q for q in r['pts']}
def lab2(dia, g, tx, ty, l1, l2=None, anchor='start'):
    import kit as K; q = P[(dia, g)]; K.lab(S, sx(q['x']), sy(q['y']), sx(tx), sy(ty), l1, l2, anchor)
lab2('Lun', 'Product Growth', 290000, 0.2, f'Lun Product Growth: {P[("Lun","Product Growth")]["y"]:.2f} %', f'{P[("Lun","Product Growth")]["x"]/1e3:.0f} mil por campaña', 'end')
lab2('Lun', 'Marketing', 3300, 3.3, f'Lun Marketing: {P[("Lun","Marketing")]["y"]:.2f} %', f'{P[("Lun","Marketing")]["x"]/1e3:.0f} mil por campaña')
lab2('Lun', 'Others', 290000, 0.62, f'Lun Others con BillPay: {P[("Lun","Others")]["y"]:.2f} %', f'{P[("Lun","Others")]["x"]/1e3:.0f} mil por campaña', 'end')
lab2('Dom', 'Product Growth', 3300, 2.6, f'Dom Product Growth: {P[("Dom","Product Growth")]["y"]:.2f} %', f'{P[("Dom","Product Growth")]["x"]/1e3:.0f} mil por campaña')
# lunes de Others sin BillPay
x2, y2 = sx(o_x), sy(o_y); x1, y1 = sx(P[('Lun', 'Others')]['x']), sy(P[('Lun', 'Others')]['y'])
S.line(x1, y1, x2, y2, BLUE2, 1.2)
S.circle(x2, y2, 6, '#FFFFFF', BLUE, 2)
S.t(x2 + 9, y2 - 6, f'Lun Others sin BillPay: {o_x/1e3:.0f} mil, {o_y:.2f} %', 10.5, BLUE, 'start', 700, halo=True)

write(44, dict(kind='grafica', seccion='V. El ritmo lo marcan los lanzamientos, no el cliente',
 titulo='El lunes no responde peor por ser lunes: sin el correo de BillPay, su clic es igual al de cualquier día',
 que='BillPay Intro y los correos más grandes de Product Growth (Tasa 0, inactivos)',
 quien='Product Growth, NewProducts (Others), Marketing, Collections y Sales',
 a_quien='Registrados sin crédito, inactivos, nunca activos y toda la base',
 lecturas=[
  f'Lunes: {d.loc["Monday","clic"]:.2f} % de clic; sin BillPay Intro, {lun_sin:.2f} %, como el martes ({d.loc["Tuesday","clic"]:.2f} %).',
  f'El tamaño de cada envío explica {100*fit["r2"]:.0f} % del clic en Product Growth, Marketing y Sales.',
  f'Product Growth manda el lunes {P[("Lun","Product Growth")]["x"]/1e3:.0f} mil por campaña y su clic baja a {P[("Lun","Product Growth")]["y"]:.2f} %.',
 ],
 causa='Lo que hunde al lunes es un envío a toda la base y el tamaño de los envíos, no el día.',
 sowhat='La regla no es "no mandar en lunes" sino "no mandar a toda la base sin probar antes".',
 fuente='Fuente: Braze, E10 (correo por día y equipo, enero a septiembre 2026) y E1. Recta sobre el log del tamaño, solo Product Growth, Marketing y Sales; con todos los equipos R² 0.02.',
 svg=S.svg()))
