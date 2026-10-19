"""Lámina 41 (base v5 lámina 7): índice semanal por canal (volumen y respuesta, enero = 100; E4a vía deck_data)
y push nuevo de junio por equipo (campañas que no mandaron push en mayo; E1)."""
import sys, pandas as pd
from kit import *
sys.path.insert(0, R + 'scripts')
import deck_data as dd
IC = dd.semanas_indexadas_canal(); cats = IC['cats']
cj = dd.culpables_push_junio(12)
# apertura del push nuevo por equipo (misma regla que culpables_push_junio)
e1 = pd.read_csv(D + 'e1_comunicacion_mes_canal.csv'); p = e1[e1.canal == 'push notification'].copy()
p['m'] = p.mes.str[5:7].astype(int); p['T'] = p.team.map(team)
may = set(map(tuple, p[(p.m == 5) & (p.pn_send > 0)][['communication_name', 'team']].values))
j = p[p.m == 6].copy(); j['nuevo'] = [(n, t) not in may for n, t in zip(j.communication_name, j.team)]
jn = j[j.nuevo].groupby('T')[['pn_send', 'pn_open']].sum(); jn['ap'] = 100 * jn.pn_open / jn.pn_send
print(jn.round(2), cj['new_env'] / 1e6, cj['new_open'], cj['old_env'] / 1e6, cj['old_open'], cj['jun'] / 1e6, cj['may'] / 1e6, cj['open_mes'][6])
bp = j[j.communication_name.str.contains('BillPay|Billpayments', case=False)].groupby('T').pn_send.sum() / 1e6; print('BillPay push junio', bp.round(2).to_dict(), bp.sum())
cells = {c['title']: c for c in IC['cells']}
for k, c in cells.items(): print(k, round(c['vmax']), cats[c['vmax_i']], round(c['rmin']), cats[c['rmin_i']])

S = Svg('Índice semanal de volumen y respuesta por canal, enero = 100, en cuatro paneles; y push nuevo de junio por equipo con su apertura')
S.line(0, 15, 22, 15, BLUE, 2); S.t(28, 19, 'Volumen', 11, TXT)
S.line(96, 15, 118, 15, INK, 1.5); S.t(124, 19, 'Respuesta (clic, apertura o lectura)', 11, TXT)
S.t(0, 38, 'Índice: promedio de las semanas de enero = 100, por canal; 38 semanas', 10.5, SEC)
PW, PH = 228, 158
def cell(x0, y0, c, hi):
    X0, X1, Y0, Y1 = x0 + 28, x0 + PW, y0 + 20, y0 + 20 + PH - 30
    n = len(cats); sx = lambda i: X0 + (X1 - X0) * i / (n - 1); sy = lambda v: Y1 - (Y1 - Y0) * min(v, 360) / 360
    S.t(x0, y0 + 8, {'Email': 'Correo'}.get(c['title'], c['title']), 11.5, INK if hi else TXT, w=700)
    for v in (0, 100, 200, 300):
        S.line(X0, sy(v), X1, sy(v), GRID if v != 100 else G2); S.t(X0 - 4, sy(v) + 3.5, f'{v}', 10.5, SEC, 'end')
    S.poly([(sx(i), sy(v)) for i, v in enumerate(c['resp'])], INK if hi else G1, 1.3)
    S.poly([(sx(i), sy(v)) for i, v in enumerate(c['vol'])], BLUE if hi else BLUE2, 2 if hi else 1.5)
    i = c['vmax_i']; S.circle(sx(i), sy(c['vmax']), 3.5, BLUE if hi else BLUE2)
    S.t(sx(i) + (6 if i < n * 0.6 else -6), sy(c['vmax']) + 4, f'{c["vmax"]:.0f}, {int(cats[i][3:])} {["","ene","feb","mar","abr","may","jun","jul","ago","sep"][int(cats[i][:2])]}', 10.5, BLUE if hi else TXT, 'start' if i < n * 0.6 else 'end', 700 if hi else 400, halo=True)
    i = c['rmin_i']; S.circle(sx(i), sy(c['rmin']), 3, INK if hi else G1)
    S.t(sx(i) + 6, sy(c['rmin']) + 2, f'{c["rmin"]:.0f}', 10.5, INK if hi else TXT, 'start', 700 if hi else 400, halo=True)
    for k, lab in ((0, 'Ene'), (cats.index('06/01'), 'Jun'), (n - 1, 'Sep')):
        S.t(sx(k), Y1 + 15, lab, 10.5, SEC, 'start' if k == 0 else ('end' if k == n - 1 else 'middle'))
cell(0, 52, cells['Push'], True); cell(250, 52, cells['Email'], False)
cell(0, 232, cells['WhatsApp'], False); cell(250, 232, cells['In-app'], False)
# panel derecho
PX = 520
S.t(PX, 60, 'Push nuevo de junio, por equipo', 11.5, INK, w=600)
S.t(PX, 75, 'Campañas que no mandaron push en mayo', 10.5, SEC)
BX0, BX1 = PX + 92, 690; y = 92; mx = jn.pn_send.max() / 1e6
for t in ['Marketing', 'Others', 'Product Growth', 'Sales']:
    v = jn.loc[t, 'pn_send'] / 1e6; w = (BX1 - BX0) * v / mx
    S.t(BX0 - 6, y + 13, {'Others': 'NewProducts', 'Product Growth': 'Prod. Growth'}.get(t, t), 11, INK, 'end', 600 if t == 'Marketing' else 400)
    S.rect(BX0, y + 2, w, 16, BLUE)
    S.t(BX0 + w + 5, y + 14, f'{v:.1f} M', 11, INK, 'start', 700)
    S.t(BX0 + w + 5, y + 28, f'abre {jn.loc[t, "ap"]:.2f} %', 10.5, TXT)
    y += 40
S.line(PX, y + 4, 776, y + 4, GRID)
S.t(PX, y + 24, f'Push nuevo: {cj["new_env"]/1e6:.0f} M, abre {cj["new_open"]:.2f} %', 11, INK, 'start', 700)
S.t(PX, y + 40, f'Push que ya existía: {cj["old_env"]/1e6:.1f} M, abre {cj["old_open"]:.2f} %', 11, TXT)
S.t(PX, y + 60, f'Apertura de push del mes: {cj["open_mes"][6]:.2f} %,', 10.5, SEC)
S.t(PX, y + 74, f'la más baja del año (mayo {cj["open_mes"][5]:.2f} %).', 10.5, SEC)

bpt = bp.sum()
write(41, dict(kind='grafica', seccion='V. El ritmo lo marcan los lanzamientos, no el cliente',
 titulo=f'Junio sumó {cj["new_env"]/1e6:.0f} M push nuevos de cuatro equipos y casi nadie los abrió: {cj["new_open"]:.2f} %',
 que='BillPay y sus recordatorios, TopUps, Anota y Gana, Mundial, Día del Padre, Hot Sale',
 quien='Marketing, NewProducts, Product Growth y Sales',
 a_quien='Toda la base y leads: cada push llegó a entre 1.2 y 3.2 M personas',
 lecturas=[
  f'Semana del 15 de junio: push a {cells["Push"]["vmax"]:.0f} (3.4 veces enero) y apertura a {cells["Push"]["rmin"]:.0f}.',
  f'El push que ya existía abrió {cj["old_open"]:.2f} %; el nuevo, {cj["new_open"]:.2f} %.',
  f'BillPay sumó {bpt:.1f} M push en junio entre NewProducts y Marketing.',
 ],
 causa='Cada equipo lanzó su campaña de junio sin ver las de los demás; BillPay salió por dos equipos.',
 sowhat='Un lanzamiento debe tener un solo dueño y una sola secuencia, no cuatro push en un mes.',
 fuente='Fuente: Braze, E4a por semana y canal (índice: semanas de enero = 100) y E1 por campaña y mes, 2026. Push nuevo = la campaña no mandó push en mayo.',
 svg=S.svg()))
