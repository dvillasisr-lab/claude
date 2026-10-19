"""Lámina 19 (ronda 3, consistencia): pequeños múltiplos por canal (misma escala). Cada punto es una campaña con 100 mil o más
mensajes: mensajes en el año (x) contra respuesta en veces el mínimo aceptable del canal (y, 1 = justo el mínimo).
Azul: no responde lo mínimo y manda mucho, con la misma regla que b7 (load_c: muestra_c con la lectura de WhatsApp que incluye
las del mes siguiente). Así cuadra con las láminas 66 y 76: 282 M mensajes, 42 %, 16.0 M MXN; 85 campañas en septiembre."""
import math, sys
from b2base import *
sys.path.insert(0, str(HERE.parents[1] / 'b7' / 'src'))
from b7 import load_c, load_e1  # noqa: E402

c = load_c()
e = load_e1()
TOT = c.envios.sum()
no = c[c.senal == 'apagar o rehacer']
p = no[no.tipo == 'promocional o lifecycle']
s9 = e[e.m == 9].groupby(['fam', 'canal']).agg(env9=('envios', 'sum'), c9=('costo', 'sum')).reset_index()
pa = p[p.activo_sep == 1].merge(s9, left_on=['familia', 'canal'], right_on=['fam', 'canal'], how='left')
ch = no.groupby('canal').agg(n=('envios', 'size'), env=('envios', 'sum'), cost=('costo_ent', 'sum'))
cht = c.groupby('canal').envios.sum()
eqn = no.groupby('equipo').envios.sum() / 1e6
tg = no.groupby('tema').envios.sum() / 1e6
print('no', len(no), no.envios.sum() / 1e6, 100 * no.envios.sum() / TOT, no.costo_ent.sum() / 1e6, 'sept', len(pa), pa.env9.sum() / 1e6, pa.c9.sum() / 1e6)
print(ch.assign(env=lambda x: x.env / 1e6, cost=lambda x: x.cost / 1e6).round(2)); print(eqn.round(1).to_dict()); print(tg.sort_values(ascending=False).head(5).round(1).to_dict())
x = c[(c.envios >= 1e5) & c.canal.isin(MIN)].copy()
x['ix'] = x.respuesta_pct / x.canal.map(MIN)
x['no'] = x.senal == 'apagar o rehacer'
print('puntos', len(x), x.no.sum(), x[x.no].envios.sum() / no.envios.sum())
CH = [('email', 'Correo', 'Mínimo: 3 clics por cada mil correos'), ('push notification', 'Push', 'Mínimo: 7.5 aperturas por cada mil push'),
      ('whatsapp', 'WhatsApp', 'Mínimo: 6 de cada 10 leídos'), ('in-app', 'In-app', 'Mínimo: 1 de cada 10 con clic')]
S = Svg('Cuatro paneles, uno por canal, con la misma escala: cada campaña con 100 mil o más mensajes, mensajes contra respuesta en veces el mínimo aceptable; '
        'en azul las que no responden lo mínimo y mandan mucho.')
S.circle(5, 14, 5, BLUE, ''); S.t(15, 18, 'No responde lo mínimo y sigue en septiembre', 11.5, INK, w=600)
S.circle(300, 14, 5, BLUE2, ''); S.t(310, 18, 'No responde y ya se detuvo', 11.5, TXT)
S.circle(482, 14, 5, G2, ''); S.t(492, 18, 'Resto de campañas', 11.5, TXT)
PW, PH = 340, 130
POS = [(46, 70), (46 + PW + 34, 70), (46, 70 + PH + 58), (46 + PW + 34, 70 + PH + 58)]
XL, XH = math.log10(1e5), math.log10(4e7)
YL, YH = math.log10(0.05), math.log10(20)
NAMES = {'email': [('Nuevos_RegistradosPay-Tasa0', 'Tasa 0 a registrados sin crédito (Product Growth)'), ('BillPay_Intro', 'Lanzamiento de BillPay (Others)')],
         'push notification': [('Anonimos-RescateTasa0', 'Rescate Tasa 0 a anónimos (Marketing)'), ('Marketing-KCash-B0326-Canvas-Leads-ReferralProgram', 'Referidos a leads (Marketing)')],
         'whatsapp': [('Nuevos_NeverActive-InstallmentsNoCash', 'Nunca activaron (Product Growth)')],
         'in-app': [('LanzamientoBillpayments_Onboarding', 'Pagos de servicios (Marketing)')]}
for (cc, lab, mn), (px, py) in zip(CH, POS):
    sx = lambda v: px + PW * (math.log10(min(max(v, 1e5), 4e7)) - XL) / (XH - XL)
    sy = lambda v: py + PH - PH * (math.log10(min(max(v, 0.05), 20)) - YL) / (YH - YL)
    g = x[x.canal == cc].sort_values('no')
    k = ch.loc[cc]
    S.t(px, py - 18, f'{lab}: {int(k.n)} campañas, {k.env/1e6:.0f} M mensajes ({100*k.env/cht[cc]:.0f} % del canal)', 11.5, INK, w=700)
    S.t(px, py - 5, mn, 10.5, BLUE, 'start', 600)
    S.rect(px, sy(1), PW, py + PH - sy(1), BLUE, ' opacity="0.05"')
    for v in (0.1, 1, 10):
        S.line(px, sy(v), px + PW, sy(v), GRID if v != 1 else BLUE, 1 if v != 1 else 1.2, '' if v != 1 else ' stroke-dasharray="4 3"')
        S.t(px - 6, sy(v) + 4, f'{v:g}', 10.5, SEC if v != 1 else BLUE, 'end', 400 if v != 1 else 700)
    for v, t in ((1e5, '100 mil'), (1e6, '1 M'), (1e7, '10 M')):
        S.line(sx(v), py + PH, sx(v), py + PH + 4, G1)
        S.t(sx(v), py + PH + 15, t, 10.5, SEC, 'middle')
    S.line(px, py + PH, px + PW, py + PH, G1)
    for q in g.itertuples():
        col = (BLUE if q.activo_sep == 1 else BLUE2) if q.no else G2
        S.circle(sx(q.envios), sy(q.ix), 2.6 if q.no else 2.2, col, ' fill-opacity="0.85" stroke="#FFFFFF" stroke-width="0.6"')
    for j, (key, nm) in enumerate(NAMES.get(cc, [])):
        q = g[g.familia.str.contains(key, regex=False)].sort_values('envios').iloc[-1]
        xx, yy = sx(q.envios), sy(q.ix)
        ty = py + PH - 26 - 14 * j
        right = cc == 'in-app'
        S.line(xx, yy, xx + (10 if right else -10), ty + 2, INK, 0.6)
        S.t(xx + (12 if right else -12), ty + 4, nm, 10.5, INK, 'start' if right else 'end', 600, halo=True)
        print(cc, nm, round(q.envios / 1e6, 1), round(q.respuesta_pct, 2), q.senal, q.activo_sep)
S.t(46, 416, 'Eje vertical: respuesta en veces el mínimo aceptable del canal (1 = justo el mínimo), escala por múltiplos. Horizontal: mensajes de la campaña.', 10.5, SEC)
svg = S.done()
em = ch.loc['email']
save(19, dict(
    kind='grafica',
    titulo=f'Cuatro de cada diez mensajes salen de campañas que no responden lo mínimo, y casi dos tercios son correos',
    que='Comercios de KPay, Tasa 0, referidos y el lanzamiento de BillPay.',
    quien=f'Marketing {eqn["Marketing"]:.0f} M mensajes y Product Growth {eqn["Product Growth"]:.0f} M; Others {eqn["Others"]:.0f} M y Sales {eqn["Sales"]:.0f} M.',
    a_quien='Leads, registrados sin crédito, ex clientes inactivos y toda la base.',
    lecturas=[
        f'{no.envios.sum()/1e6:.0f} M mensajes ({100*no.envios.sum()/TOT:.0f} % del año) y {no.costo_ent.sum()/1e6:.1f} M MXN en campañas que no responden lo mínimo.',
        f'Correo: {int(em.n)} campañas y {em.env/1e6:.0f} M mensajes, {100*em.env/no.envios.sum():.0f} % de ese volumen.',
        f'{len(pa)} campañas de promoción seguían en septiembre: {pa.env9.sum()/1e6:.0f} M mensajes y {pa.c9.sum()/1e6:.1f} M MXN ese mes.',
    ],
    causa='Nadie mide cada campaña contra un mínimo común: sigue saliendo mes tras mes aunque casi nadie le responda.',
    sowhat='Revisar cada mes contra el mínimo: rehacer o quitar; a ex clientes, primero probar con un grupo sin envío.',
    fuente='Fuente: Braze, envíos por campaña, ene a sep 2026; misma regla que la lámina 66 (WhatsApp leído con el mes siguiente, por entregado). Puntos: 100 mil o más mensajes.',
    svg=svg,
))
