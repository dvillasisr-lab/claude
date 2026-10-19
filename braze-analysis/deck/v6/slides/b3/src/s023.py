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
S = Svg('Respuesta de cada campaña frente al mínimo aceptable de su canal, por equipo, con el par que más cambia del mismo producto')
X0, X1 = 150, 770
LO, HI = math.log10(0.05), math.log10(100)
xs = lambda v: X0 + (X1 - X0) * (math.log10(min(max(v, 0.05), 100)) - LO) / (HI - LO)
S.t(0, 16, 'Cada punto es una campaña en un canal; tamaño = mensajes de enero a septiembre', 12.5, INK, w=600)
S.c(8, 34, 5.5, GREEN); S.t(18, 38, 'La que más responde del par', 11.5)
S.c(198, 34, 5.5, BLUE); S.t(208, 38, 'La que menos responde', 11.5)
S.c(358, 34, 5.5, MRK, stroke='none', op=0.5); S.t(368, 38, 'Resto de sus campañas. Cada par es el mismo producto o tema.', 11.5)
TOP, RH = 56, 64
rmax = 11.0; vmax = 20e6
rad = lambda v: max(2.2, rmax * math.sqrt(min(v, vmax) / vmax))
YB = TOP + RH * len(PARES)
for v, lab in [(0.1, '0.1'), (0.3, '0.3'), (1, '1 = mínimo'), (3, '3'), (10, '10'), (30, '30'), (100, '100')]:
    S.l(xs(v), TOP, xs(v), YB - 4, MRK if v == 1 else GRID, 1.2 if v == 1 else 1)
    S.t(xs(v), YB + 9, lab, 10.5, INK if v == 1 else SEC, 'middle', w=600 if v == 1 else 400)
S.t(X1, YB + 24, 'Respuesta en veces el mínimo aceptable de su canal (escala logarítmica)', 10.5, SEC, 'end')
for i, (eq, (nb, b), (nw, w)) in enumerate(PARES):
    y0 = TOP + RH * i; cy = y0 + 44
    d = f[f.equipo == eq].sort_values('env', ascending=False)
    if i: S.l(0, y0, X1, y0, GRID)
    S.t(0, y0 + 20, eq, 12.5, INK, w=600)
    S.t(0, y0 + 35, f'{len(d)} campañas por canal', 10.5, SEC)
    S.ts(0, y0 + 51, [(f'{b.vs_min / w.vs_min:.0f} veces', INK, 600), (' entre el par', SEC, 400)], 10.5)
    for r in d.itertuples():
        S.c(xs(r.vs_min), cy, rad(r.env), MRK, stroke='#FFFFFF', sw=0.8, op=0.5)
    S.l(xs(w.vs_min), cy, xs(b.vs_min), cy, INK, 1)
    for (nm, r, col, anc) in [(nw, w, BLUE, 'end'), (nb, b, GREEN, 'start')]:
        S.c(xs(r.vs_min), cy, max(rad(r.env), 5), col, sw=1.5)
        ch, m = CAN[r.canal]
        rp = f'{r.resp_pct:.2f}' if r.resp_pct < 10 else f'{r.resp_pct:.0f}'
        x = xs(r.vs_min) + (6 if anc == 'start' else -6)
        S.t(x, y0 + 13, nm, 11, INK, anc, w=600, halo=True)
        S.t(x, y0 + 26, f'{ch} · {rp} % de {m} · {r.env/1e6:.1f} M', 10.5, TXT, anc, halo=True)
svg = S.done()
save(23, dict(kind='grafica',
  titulo='Dentro de cada equipo, a quién y por qué canal se manda hace que el mismo producto responda hasta 32 veces más',
  que='El mismo producto o la misma oferta a personas distintas o por canales distintos: Installments, cobranza, referidos, promociones de KPay y el lanzamiento de BillPay.',
  quien='Los cinco equipos. Others es BillPay (NewProducts), avisos de KPay y KCash, recomendaciones de Shopping y pruebas de QA.',
  a_quien='La campaña que responde va a quien ya empezó algo (un préstamo, un pago por vencer, una compra) o llega por in-app; la que no, a toda la base o a quien no ha hecho nada.',
  lecturas=[
   'Mismo producto, otra persona: Installments responde 2.78 % de clic en correo a quien ya lo empezó y 0.10 % a registrados que nunca activaron. Precobranza 4.3 % contra 0.14 % de la cobranza con atraso mayor.',
   'Mismo mensaje, otro canal: el lanzamiento de BillPay tuvo 85 % de clic en in-app y 0.11 % por correo. Anota y gana: 76 % en in-app y 0.19 % por correo.',
   'Entre campañas de correo, saber a quién va explica 54 % de la diferencia de respuesta y el tema 52 %; saber qué equipo la manda, solo 12 %.'],
  causa='Cada equipo usa la misma lista y el mismo canal para casi todos sus temas. El resultado lo decide a quién se le escribe y por dónde, no el equipo que lo manda.',
  sowhat='No hace falta cambiar de dueño las campañas: hay que llevar cada tema a la persona y al canal donde ya responde.',
  fuente='Fuente: Braze, envíos por campaña, mes y canal, enero a septiembre 2026; campañas con 50 mil o más mensajes entregados. Mínimo aceptable: 3 clics por cada mil correos, 7.5 aperturas por cada mil push, 6 de cada 10 WhatsApp leídos, 1 de cada 10 in-app con clic. Diferencia explicada: varianza ponderada por entregados en 303 campañas de correo; los factores se traslapan.',
  svg=svg))
check(23)
