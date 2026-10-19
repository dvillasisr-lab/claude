"""Lámina 45 (ronda 2, misma forma que 44): WhatsApp, un punto por día de la semana y equipo (E10, celdas con 50 mil o más
entregados): envíos por campaña ese día contra lectura sobre entregados; rombos sábado y domingo; recta sobre el log del tamaño."""
import math, pandas as pd, numpy as np
from kit import *
e = pd.read_csv(D + 'e10_dia_semana.csv'); e['T'] = e.team.map(team); w = e[e.canal == 'whatsapp']
d = w.groupby(['dia_semana', 'T'])[['envios', 'wa_entregados', 'respuestas', 'comunicaciones']].sum().reset_index()
d = d[d.wa_entregados >= 50e3].copy(); d['x'] = d.envios / d.comunicaciones; d['lec'] = 100 * d.respuestas / d.wa_entregados
k = d[d.lec <= 100]; fit = ols(np.log10(k.x), k.lec)
al = w.groupby('dia_semana')[['envios', 'wa_entregados', 'respuestas']].sum(); tot = al.envios.sum()
al['ent'] = 100 * al.wa_entregados / al.envios; al['lec'] = 100 * al.respuestas / al.wa_entregados
print(fit, al.round(1).to_string(), 100 * al.loc['Sunday', 'envios'] / tot)
DL = {'Monday': 'Lun', 'Tuesday': 'Mar', 'Wednesday': 'Mié', 'Thursday': 'Jue', 'Friday': 'Vie', 'Saturday': 'Sáb', 'Sunday': 'Dom'}
COL = {'Product Growth': BLUE, 'Marketing': GREEN, 'Sales': INK, 'Others': BLUE2}
S = Svg('Dispersión: lectura de WhatsApp según envíos por campaña, por día de la semana y equipo, escala logarítmica; rombos sábado y domingo; recta')
lx = 0
for t in ['Product Growth', 'Marketing', 'Sales', 'Others']:
    S.circle(lx + 5, 15, 4.5, COL[t], '#FFFFFF', 1); S.t(lx + 13, 19, t, 11, TXT); lx += 22 + len(t) * 6.2
diamond(S, lx + 5, 15, 5, G1); S.t(lx + 15, 19, 'sábado y domingo', 11, TXT)
S.t(0, 40, 'Un punto por día de la semana y equipo (50 mil o más WhatsApp entregados en 9 meses).', 10.5, SEC)
X0, X1, Y0, Y1 = 44, 770, 66, 352
lo, hi = math.log10(1000), math.log10(40000)
sx = lambda v: X0 + (X1 - X0) * (math.log10(v) - lo) / (hi - lo); sy = lambda v: Y1 - (Y1 - Y0) * (min(v, 112) - 40) / 72
for v in (40, 60, 80, 100):
    S.line(X0, sy(v), X1, sy(v), G2 if v == 100 else GRID); S.t(X0 - 6, sy(v) + 4, f'{v} %', 10.5, SEC, 'end')
for v, l in ((1000, '1 mil'), (2500, '2.5 mil'), (5000, '5 mil'), (10000, '10 mil'), (25000, '25 mil')):
    S.line(sx(v), Y1, sx(v), Y1 + 5, SEC); S.t(sx(v), Y1 + 18, l, 10.5, SEC, 'middle')
S.line(X0, Y1, X1, Y1, SEC); S.t((X0 + X1) / 2, Y1 + 33, 'WhatsApp enviados por campaña ese día (escala logarítmica)', 10.5, SEC, 'middle')
S.t(X1, Y0 - 4, 'Lectura sobre entregados', 11, SEC, 'end')
xa, xb = 1500, 35000
S.line(sx(xa), sy(fit['a'] + fit['b'] * math.log10(xa)), sx(xb), sy(fit['a'] + fit['b'] * math.log10(xb)), INK, 1.4)
S.t(sx(xb), sy(fit['a'] + fit['b'] * math.log10(xb)) + 18, f'Recta: R² {fit["r2"]:.2f}', 10.5, INK, 'end', 600, halo=True)
for _, q in d.iterrows():
    x, y = sx(q.x), sy(q.lec); wk = q.dia_semana in ('Saturday', 'Sunday')
    if q.lec > 100:
        S.circle(x, sy(110), 5, '#FFFFFF', SEC, 1.5); continue
    if wk: diamond(S, x, y, 6.5, COL[q['T']])
    else: S.circle(x, y, 5.5 if q.dia_semana == 'Monday' else 4.5, COL[q['T']], '#FFFFFF', 1.2)
def nm(dia, t, tx, ty, l1, l2=None, anc='start'):
    q = d[(d.dia_semana == dia) & (d['T'] == t)].iloc[0]
    lab(S, sx(q.x), sy(min(q.lec, 110)), sx(tx), sy(ty), l1, l2, anc)
q = d[(d.dia_semana == 'Sunday') & (d['T'] == 'Sales')].iloc[0]
nm('Sunday', 'Sales', 1900, 106, f'Dom Sales: {q.lec:.0f} %, imposible', 'suma lecturas de otros días')
q = d[(d.dia_semana == 'Sunday') & (d['T'] == 'Product Growth')].iloc[0]
nm('Sunday', 'Product Growth', 1150, 50, f'Dom Product Growth: {q.lec:.0f} %', f'{q.x/1e3:.1f} mil por campaña', 'start')
q = d[(d.dia_semana == 'Monday') & (d['T'] == 'Product Growth')].iloc[0]
nm('Monday', 'Product Growth', 9000, 45, f'Lun Product Growth: {q.lec:.0f} %', f'{q.x/1e3:.0f} mil por campaña', 'start')
q = d[(d.dia_semana == 'Thursday') & (d['T'] == 'Marketing')].iloc[0]
nm('Thursday', 'Marketing', 30000, 92, f'Jue Marketing: {q.lec:.0f} %', f'{q.x/1e3:.0f} mil por campaña', 'end')
write(45, dict(kind='grafica', seccion='V. El ritmo lo marcan los lanzamientos, no el cliente',
 titulo=f'WhatsApp parece leerse mejor en domingo, pero con {100*al.loc["Sunday","envios"]/tot:.0f} % de los envíos no alcanza para mover el calendario',
 que='WhatsApp promocional: Tasa 0, referidos, churn, inactivos y Hot Sale',
 quien='Marketing (56 %), Product Growth (29 %) y Sales (13 %) del WhatsApp',
 a_quien='Leads rezagados, churn, inactivos y recurrentes',
 lecturas=[
  f'Domingo: {al.loc["Sunday","lec"]:.0f} % de lectura contra {al.loc["Monday","lec"]:.0f} % el lunes, pero con {al.loc["Sunday","envios"]/1e6:.1f} M de {tot/1e6:.0f} M WhatsApp.',
  f'El tamaño del envío explica {100*fit["r2"]:.0f} % de la lectura: el domingo cada campaña manda menos de 5 mil WhatsApp.',
  'Sales marca 175 % el domingo: la lectura se registra el día en que ocurre y suma mensajes de días anteriores.',
 ],
 causa='El domingo son envíos chicos y de seguimiento, y su tasa se infla con lecturas de otros días.',
 sowhat='Antes de mover WhatsApp al domingo, probar la misma campaña en domingo y martes con grupo sin mensajes.',
 fuente='Fuente: Braze, E10 (WhatsApp por día y equipo, enero a septiembre 2026). Lectura sobre entregados, por fecha del evento. Recta por mínimos cuadrados sobre el logaritmo del tamaño, sin celdas arriba de 100 %.',
 svg=S.svg()))
