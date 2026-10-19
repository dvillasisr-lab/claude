"""Lámina 35 (ronda 2): franja de puntos por equipo. Cada punto es una pareja de campañas promocionales que le llegó el mismo
día a la misma persona (E6b, 1,000 pares más frecuentes); x = personas que recibieron las dos. Cifras por mes: E6a."""
import math, pandas as pd, numpy as np
from kit import *
from e6b import load
a = pd.read_csv(D + 'e6a_solape_dia_mes.csv'); a['m'] = a.mes.str[5:7].astype(int)
hi = a[a.banda_familias_dia.isin(['3 a 4', '5 a 7', '8+'])]
pers = hi.groupby('m').usuarios_aprox.sum() / 1e6
sh_ud = 100 * hi.usuario_dias.sum() / a.usuario_dias.sum(); sh_m = 100 * hi.msgs.sum() / a.msgs.sum()
p = load(); pp = p[p.promo2].copy(); P = pp.usuario_dias_juntas.sum()
TEAMS = ['Marketing', 'Sales', 'Product Growth', 'Others', 'Collections']
inv = {t: 100 * pp[(pp.ta == t) | (pp.tb == t)].usuario_dias_juntas.sum() / P for t in TEAMS}
cnt = {t: int(((pp.ta == t) | (pp.tb == t)).sum()) for t in TEAMS}
print(pers.round(2).to_dict(), sh_ud, sh_m, inv, cnt, len(pp))
S = Svg('Franja de puntos por equipo: cada punto es una pareja de campañas promocionales que llegó el mismo día a la misma persona; eje horizontal, personas que recibieron las dos')
S.t(0, 16, 'Cada punto: dos campañas promocionales el mismo día a la misma persona', 11.5, INK, w=600)
S.t(0, 32, f'{len(pp)} parejas; un choque cuenta en los dos equipos. A la derecha: parte de las personas-día con choque.', 10.5, SEC)
X0, X1 = 120, 640
lo, hi_ = math.log10(15000), math.log10(2e6)
sx = lambda v: X0 + (X1 - X0) * (math.log10(v) - lo) / (hi_ - lo)
RY, RH = 64, 58
for v, l in ((20000, '20 mil'), (50000, '50 mil'), (100000, '100 mil'), (250000, '250 mil'), (500000, '500 mil'), (1000000, '1 M')):
    S.line(sx(v), RY - 6, sx(v), RY + RH * 5, GRID); S.t(sx(v), RY + RH * 5 + 16, l, 10.5, SEC, 'middle')
S.t((X0 + X1) / 2, RY + RH * 5 + 32, 'Personas que recibieron las dos campañas el mismo día (escala logarítmica)', 10.5, SEC, 'middle')
rng = np.random.default_rng(7)
for i, t in enumerate(TEAMS):
    yc = RY + RH * i + RH / 2; d = pp[(pp.ta == t) | (pp.tb == t)]
    S.t(X0 - 12, yc + 4, t, 11.5, INK if t == 'Marketing' else TXT, 'end', 700 if t == 'Marketing' else 400)
    S.line(X0, yc + RH / 2, X1, yc + RH / 2, GRID)
    for _, q in d.iterrows():
        S.circle(sx(q.usuarios_aprox), yc + rng.uniform(-17, 17), 2.6, BLUE if t == 'Marketing' else G1, '#FFFFFF', 0.6)
    S.t(X1 + 14, yc - 2, f'{inv[t]:.0f} %', 15, BLUE if t == 'Marketing' else INK, 'start', 700)
    S.t(X1 + 14, yc + 13, f'{cnt[t]} parejas', 10.5, SEC)
S.t(X1 + 14, RY - 10, '% personas-día', 10.5, SEC)
def nm(k1, k2, row, tx, ty, l1, l2, anc='end'):
    q = pp[(pp.familia_a.str.contains(k1) & pp.familia_b.str.contains(k2)) | (pp.familia_b.str.contains(k1) & pp.familia_a.str.contains(k2))].sort_values('usuarios_aprox').iloc[-1]
    yc = RY + RH * row + RH / 2
    S.circle(sx(q.usuarios_aprox), yc, 4.5, BLUE if row == 0 else INK, '#FFFFFF', 1.5)
    lab(S, sx(q.usuarios_aprox), yc, tx, ty, l1, l2, anc)
nm('PushFelicitiacionDiaPadres', 'B00527', 0, 640, 52, '21 jun: Día del Padre y Billpayments', f'Marketing con Marketing, 1.54 M personas')
nm('B001-CANVAS-Todos-ReminderRegistroTelefono', 'B00527', 3, 640, RY + RH * 3 + 8, '11 ago: prueba de QA y Billpayments', 'Others con Marketing, 1.45 M')
write(35, dict(kind='grafica', seccion='IV. La misma persona, demasiadas veces',
 titulo=f'Cada mes hasta {pers.max():.1f} M personas reciben tres o más campañas el mismo día, casi siempre con Marketing',
 que='Hot Sale, Comercio del día, BillPay, Anota y Gana, Mundial, Día del Padre y Tasa 0',
 quien='Marketing, Sales, Product Growth y Others (NewProducts, QA); Collections no aparece',
 a_quien='Recurrentes y activos de KPay, leads y envíos a toda la base',
 lecturas=[
  f'{pers[6]:.2f} M personas tuvieron en junio al menos un día con tres o más campañas; {pers[1]:.2f} M en enero.',
  f'Esos días son {sh_ud:.0f} % de las personas-día y llevan {sh_m:.0f} % de los mensajes.',
  f'Marketing está en {inv["Marketing"]:.0f} % de los choques promocionales; Sales en {inv["Sales"]:.0f} % y Product Growth en {inv["Product Growth"]:.0f} %.',
 ],
 causa='Nadie administra el calendario y el límite global de mensajes por persona de Braze está apagado.',
 sowhat='Hace falta un límite de mensajes por persona al día y un dueño del calendario.',
 fuente='Fuente: Braze, enero a septiembre 2026. Personas por mes: E6a. Parejas: E6b, 1,000 pares más frecuentes (muestra, no universo); promocional = nombre con ticket y equipo distinto de Collections.',
 svg=S.svg()))
