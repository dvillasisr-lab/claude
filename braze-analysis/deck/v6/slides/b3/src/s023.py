"""Lámina 23: franjas de puntos por equipo. Cada punto = campaña en un canal (50 mil o más entregados, nueve meses);
x = respuesta en veces el mínimo aceptable de su canal (escala logarítmica); tamaño = mensajes. Se marca un par por equipo
con el mismo producto o tema: el que responde (verde) y el que no (azul)."""
import math
from datos import *
from svgk import *
f = fam()
def pick(eq, pat, canal):
    d = f[(f.equipo == eq) & f.familia.str.contains(pat, regex=True) & (f.canal == canal)].sort_values('env', ascending=False)
    return d.iloc[0]
CAN = {'email': ('correo', 'clic'), 'push notification': ('push', 'apertura'), 'whatsapp': ('WhatsApp', 'lectura'), 'in-app': ('in-app', 'clic')}
PARES = [
 ('Collections', ('Precobranza de KCash', pick('Collections', 'KCash-T000-CANVAS-Precobranza-ecosystem', 'email')),
                 ('Cobranza con atraso mayor (BKT3)', pick('Collections', 'KCash-T000-CANVAS-BKT3', 'email'))),
 ('Product Growth', ('Installments a quien ya lo empezó', pick('Product Growth', 'B0301-CANVAS-Active-Retargeting_Installments', 'email')),
                    ('Installments a quien nunca activó', pick('Product Growth', 'B0223-CANVAS-Nuevos_NeverActive', 'email'))),
 ('Others', ('Lanzamiento de BillPay', pick('Others', 'BillPay_Intro_Full', 'in-app')),
            ('El mismo lanzamiento', pick('Others', 'BillPay_Intro_Full', 'email'))),
 ('Marketing', ('Referidos a clientes que ya compraron', pick('Marketing', 'Recurrentes_ClienteKCashCompraKCash', 'email')),
               ('Referidos a ex clientes dormidos', pick('Marketing', 'KCash-B0326-Canvas-Recurrentes_Dormants', 'email'))),
 ('Sales', ('Amazon a clientes recurrentes', pick('Sales', 'B0415-CANVAS-Recurrentes-Amazon', 'push notification')),
           ('Comercio del día de septiembre', pick('Sales', 'ComerciodeldiaSeptiembre', 'push notification'))),
]
for eq, (nb, b), (nw, w) in PARES:
    print(eq, nb, b.canal, round(b.resp_pct, 2), round(b.env / 1e6, 2), '|', nw, w.canal, round(w.resp_pct, 2), round(w.env / 1e6, 2), 'x', round(b.vs_min / w.vs_min, 1))
import random
rnd = random.Random(7)
def wq(v, w, q):
    o = np.argsort(v.values); v = v.values[o]; w = w.values[o]; c = np.cumsum(w) / w.sum(); return v[np.searchsorted(c, q)]
S = Svg('Respuesta de cada campaña frente al mínimo aceptable de su canal, por equipo: rango, mediana y el par del mismo producto que más cambia')
X0, X1 = 150, 688
LO, HI = math.log10(0.05), math.log10(100)
xs = lambda v: X0 + (X1 - X0) * (math.log10(min(max(v, 0.05), 100)) - LO) / (HI - LO)
S.t(0, 16, 'Respuesta de cada campaña en cada canal, en veces el mínimo aceptable de ese canal', 12.5, INK, w=600)
S.c(5, 34, 3, MRK, stroke='none', op=0.7); S.t(12, 38, 'una campaña', 11, SEC)
S.r(92, 29, 22, 11, '#E4EAFB'); S.t(119, 38, 'mitad central de los mensajes', 11, SEC)
S.l(290, 28, 290, 41, INK, 2.5); S.t(296, 38, 'mediana', 11, SEC)
S.c(358, 34, 5, GREEN); S.t(367, 38, 'la que más responde del par', 11, SEC)
S.c(530, 34, 5, BLUE); S.t(539, 38, 'la que menos (mismo producto o tema)', 11, SEC)
TOP, RH = 54, 66
YB = TOP + RH * len(PARES)
for v, lab in [(0.1, '0.1'), (0.3, '0.3'), (1, '1 = mínimo'), (3, '3'), (10, '10'), (30, '30'), (100, '100')]:
    S.l(xs(v), TOP, xs(v), YB - 2, MRK if v == 1 else GRID, 1.2 if v == 1 else 1)
    S.t(xs(v), YB + 11, lab, 10.5, INK if v == 1 else SEC, 'middle', w=600 if v == 1 else 400)
S.t(X1, YB + 25, 'Veces el mínimo aceptable de su canal (escala logarítmica)', 10.5, SEC, 'end')
S.t(780, TOP - 2, 'Mediana', 10.5, SEC, 'end')
for i, (eq, (nb, b), (nw, w)) in enumerate(PARES):
    y0 = TOP + RH * i; cy = y0 + 46
    d = f[f.equipo == eq].sort_values('env', ascending=False)
    q1, med, q3 = (wq(d.vs_min, d.env, q) for q in (0.25, 0.5, 0.75))
    print(eq, 'q1 %.2f med %.2f q3 %.2f' % (q1, med, q3))
    if i: S.l(0, y0, 780, y0, GRID)
    S.t(0, y0 + 30, eq, 12.5, INK, w=600)
    S.t(0, y0 + 45, f'{len(d)} campañas por canal', 10.5, SEC)
    S.r(xs(q1), cy - 11, xs(q3) - xs(q1), 22, '#E4EAFB')
    for r in d.itertuples():
        S.c(xs(r.vs_min), cy + rnd.uniform(-8, 8), 3.2 if r.env > 1e6 else 2.3, MRK, stroke='none', op=0.7)
    S.l(xs(med), cy - 13, xs(med), cy + 13, INK, 2.5)
    S.l(xs(w.vs_min), cy, xs(b.vs_min), cy, INK, 1)
    for (nm, r, col, anc) in [(nw, w, BLUE, 'end'), (nb, b, GREEN, 'start')]:
        S.c(xs(r.vs_min), cy, 5.5, col, sw=1.5)
        ch, m = CAN[r.canal]
        rp = f'{r.resp_pct:.2f}' if r.resp_pct < 10 else f'{r.resp_pct:.0f}'
        x = xs(r.vs_min) + (5 if anc == 'start' else -5)
        S.t(x, y0 + 13, nm, 11, INK, anc, w=600, halo=True)
        S.t(x, y0 + 26, f'{ch} · {rp} % de {m} · {r.env/1e6:.1f} M', 10.5, TXT, anc, halo=True)
    S.t(780, cy - 2, f'{med:.1f} veces', 11, INK, 'end', w=600)
    S.t(780, cy + 12, f'par: {b.vs_min / w.vs_min:.0f} veces', 10.5, SEC, 'end')
svg = S.done()
save(23, dict(kind='grafica',
  titulo='Dentro de cada equipo, a quién y por qué canal se manda hace que el mismo producto responda hasta 32 veces más',
  que='El mismo producto a otra gente o por otro canal: Installments, cobranza, BillPay.',
  quien='Los cinco equipos.',
  a_quien='La que responde va a quien ya empezó algo o llega por in-app; la otra, a toda la base.',
  lecturas=[
   'Installments: 2.78 % de clic a quien ya lo empezó y 0.10 % a quien nunca activó, en el mismo correo.',
   'BillPay: 85 % de clic por in-app y 0.11 % por correo. Anota y gana: 76 % y 0.19 %.',
   'A quién va explica 54 % de la diferencia de respuesta entre correos; el equipo que lo manda, 12 %.'],
  causa='Cada equipo usa la misma lista y el mismo canal para casi todo; el resultado lo decide a quién y por dónde.',
  sowhat='No hace falta cambiar de dueño las campañas: hay que llevar cada tema a quien y por donde ya responde.',
  fuente='Fuente: Braze, envíos por campaña, mes y canal, enero a septiembre 2026; campañas con 50 mil o más entregados. Diferencia explicada: varianza ponderada en 303 campañas de correo.',
  svg=svg))
check(23)
