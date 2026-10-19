"""Lámina 38 (ronda 2, forma de v5 lámina 7): pequeños múltiplos por canal, misma escala. Eje: antigüedad en la base el día
del envío (E12). Dos índices (primer mes = 100): mensajes por persona al mes y respuesta sobre enviados."""
import pandas as pd
from kit import *
e = pd.read_csv(D + 'e12_antiguedad.csv')
B = ['0. menos de 1 mes', '1. 1 a 3 meses', '2. 3 a 6 meses', '3. 6 a 12 meses', '4. 1 a 2 años', '5. más de 2 años']; DUR = [1, 2, 3, 6, 9, 9]
BL = ['<1 m', '1-3 m', '3-6 m', '6-12 m', '1-2 a', '>2 a']
g = e.groupby(['canal', 'banda_antiguedad'])[['envios', 'usuarios_aprox', 'respuestas', 'bajas_email_eventos']].sum()
CH = [('push notification', 'Push', 'apertura'), ('email', 'Correo', 'clic'), ('whatsapp', 'WhatsApp', 'lectura'), ('in-app', 'In-app', 'clic')]
DAT = {}
for c, *_ in CH:
    pm = [g.loc[(c, b)].envios / g.loc[(c, b)].usuarios_aprox / d for b, d in zip(B, DUR)]
    r = [100 * g.loc[(c, b)].respuestas / g.loc[(c, b)].envios for b in B]
    DAT[c] = (pm, r, [100 * v / pm[0] for v in pm], [100 * v / r[0] for v in r])
OLD = ['3. 6 a 12 meses', '4. 1 a 2 años', '5. más de 2 años']
sh_push = 100 * e[(e.canal == 'push notification') & e.banda_antiguedad.isin(OLD)].envios.sum() / e[e.canal == 'push notification'].envios.sum()
em = g.loc['email']; bm = [1000 * em.loc[b].bajas_email_eventos / em.loc[b].envios for b in B]
print({c: ([round(x, 1) for x in v[0]], [round(x, 2) for x in v[1]]) for c, v in DAT.items()}, sh_push, [round(x, 1) for x in bm])
S = Svg('Cuatro paneles por canal: según antigüedad en la base, índice de mensajes por persona al mes y de respuesta, primer mes = 100')
S.line(0, 15, 22, 15, BLUE, 2.2); S.t(28, 19, 'Mensajes por persona al mes', 11, TXT)
S.line(210, 15, 232, 15, INK, 1.6); S.t(238, 19, 'Respuesta (apertura, clic o lectura)', 11, TXT)
S.t(0, 38, 'Índice: personas con menos de 1 mes en la base = 100. Antigüedad el día del envío.', 10.5, SEC)
PW, PH = 360, 160
def cell(x0, y0, c, name, rlab, hi):
    pm, r, ipm, ir = DAT[c]
    X0, X1, Y0, Y1 = x0 + 34, x0 + PW - 70, y0 + 22, y0 + PH - 22
    sx = lambda i: X0 + (X1 - X0) * i / 5; sy = lambda v: Y1 - (Y1 - Y0) * min(v, 130) / 130
    S.t(x0, y0 + 8, name, 12, INK if hi else TXT, w=700)
    for v in (0, 50, 100):
        S.line(X0, sy(v), X1, sy(v), G2 if v == 100 else GRID); S.t(X0 - 5, sy(v) + 4, f'{v}', 10.5, SEC, 'end')
    for i, l in enumerate(BL): S.t(sx(i), Y1 + 15, l, 10.5, SEC, 'middle')
    S.poly([(sx(i), sy(v)) for i, v in enumerate(ipm)], BLUE if hi else BLUE2, 2.4 if hi else 1.6)
    S.poly([(sx(i), sy(v)) for i, v in enumerate(ir)], INK if hi else G1, 2 if hi else 1.4)
    for v, col, lab_ in ((ipm, BLUE if hi else BLUE2, f'{pm[5]:.0f} al mes' if pm[5] >= 2 else f'{pm[5]:.1f} al mes'), (ir, INK if hi else G1, f'{r[5]:.2f} %' if r[5] < 10 else f'{r[5]:.0f} %')):
        S.circle(sx(5), sy(v[5]), 3.5, col)
    dy = 0 if abs(ipm[5] - ir[5]) > 12 else 7
    S.t(sx(5) + 7, sy(ipm[5]) + 4 - (dy if ipm[5] >= ir[5] else -dy), f'{pm[5]:.0f} al mes' if pm[5] >= 2 else f'{pm[5]:.1f} al mes', 10.5, BLUE if hi else TXT, 'start', 700 if hi else 400)
    S.t(sx(5) + 7, sy(ir[5]) + 4 + (dy if ipm[5] >= ir[5] else -dy), f'{rlab} {r[5]:.2f} %' if r[5] < 10 else f'{rlab} {r[5]:.0f} %', 10.5, INK if hi else TXT, 'start', 700 if hi else 400)
    S.t(sx(0) + 4, sy(100) - 6, f'{pm[0]:.0f} al mes, {r[0]:.2f} %' if r[0] < 10 else f'{pm[0]:.0f} al mes, {r[0]:.0f} %', 10.5, TXT, 'start', 400, halo=True)
cell(0, 50, 'push notification', 'Push', 'abre', True); cell(410, 50, 'email', 'Correo', 'clic', False)
cell(0, 222, 'whatsapp', 'WhatsApp', 'lee', False); cell(410, 222, 'in-app', 'In-app', 'clic', False)
pm, r, *_ = DAT['push notification']
write(38, dict(kind='grafica', seccion='IV. La misma persona, demasiadas veces',
 titulo='Después del tercer mes casi nadie abre el push, y le seguimos mandando unos diez al mes',
 que='Push promocional: Comercio del día, Hot Sale, referidos y rescates de fin de semana',
 quien='Sales y Marketing a recurrentes de KPay; Marketing a leads de bases viejas',
 a_quien=f'Personas con más de 6 meses en la base: reciben {sh_push:.0f} % del push',
 lecturas=[
  f'Push: {pm[0]:.0f} al mes y {r[0]:.1f} % de apertura el primer mes; después del sexto, {pm[3]:.0f} a {pm[5]:.0f} al mes y {r[5]:.1f} %.',
  f'Correo sí baja con la antigüedad: {DAT["email"][0][0]:.0f} al mes el primer mes, menos de 2 después del sexto.',
  f'Las bajas de correo son parecidas en todas las antigüedades: {min(bm):.1f} a {max(bm):.1f} por mil correos.',
 ],
 causa='El push se manda por lista (recurrentes, bases viejas) y no según si la persona lo abrió hace poco.',
 sowhat='El push debe ir a quien abrió uno en los últimos 90 días.',
 fuente='Fuente: Braze, E12 (antigüedad el día del envío), enero a septiembre 2026. Por mes = mensajes por persona entre los meses que dura la banda (1, 2, 3, 6, 9 y 9); respuesta sobre enviados.',
 svg=S.svg()))
