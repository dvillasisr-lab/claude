"""Lámina 19 (ronda 2): pequeños múltiplos por canal (misma escala): cada punto es una campaña de promoción (50 mil o más
entregados): mensajes (x) contra respuesta en veces el mínimo aceptable del canal (y, 1 = justo el mínimo). Azul: debajo."""
import math
from b2base import *

d = load_b()
d = d[d.tipo == 'promocional']
fa = d.groupby(['fam', 'canal']).agg(b=('b', 'sum'), r=('r', 'sum'), env=('envios', 'sum'), costo=('costo', 'sum'), eq=('equipo', 'first'),
                                    gan=('gan', 'first'), aud=('aud', 'first'), last=('m', 'max')).reset_index()
fa['pct'] = 100 * fa.r / fa.b.replace(0, np.nan)
fa['bajo'] = fa.pct < fa.canal.map(MIN)
fa = fa[fa.b >= 5e4].copy()
fa['ix'] = fa.pct / fa.canal.map(MIN)
f = lambda g: pd.Series({'n': len(g), 'nb': g.bajo.sum(), 'env': g.env.sum() / 1e6, 'envb': g[g.bajo].env.sum() / 1e6,
                         'pv': 100 * g[g.bajo].env.sum() / g.env.sum(), 'cb': g[g.bajo].costo.sum() / 1e6})
tot = f(fa); chs = fa.groupby('canal').apply(f); eqs = fa.groupby('eq').apply(f); gn = fa.groupby('gan').apply(f); au = fa.groupby('aud').apply(f)
sep = int((fa.bajo & (fa['last'] == 9)).sum())
print(tot.round(1).to_dict(), 'sept', sep); print(chs.round(1)); print(fa.ix.describe())
CH = [('email', 'Correo', 'mínimo: 3 clics por cada mil'), ('push notification', 'Push', 'mínimo: 7.5 aperturas por cada mil'),
      ('whatsapp', 'WhatsApp', 'mínimo: 6 de cada 10 leídos'), ('in-app', 'In-app', 'mínimo: 1 de cada 10 con clic')]
S = Svg('Cuatro paneles, uno por canal, con la misma escala: cada punto es una campaña de promoción, mensajes contra respuesta en veces el mínimo aceptable; '
        'en azul las que quedan debajo.')
S.circle(5, 14, 5, BLUE, ''); S.t(15, 18, 'Responde menos que el mínimo aceptable', 11.5, INK, w=600)
S.circle(270, 14, 5, G1, ''); S.t(280, 18, 'Llega al mínimo o más', 11.5, TXT)
S.t(430, 18, 'Tamaño: gasto en MXN (correo y WhatsApp)', 10.5, SEC)
PW, PH = 340, 130
POS = [(46, 70), (46 + PW + 34, 70), (46, 70 + PH + 58), (46 + PW + 34, 70 + PH + 58)]
XL, XH = math.log10(5e4), math.log10(4e7)
YL, YH = math.log10(0.05), math.log10(20)
NAMES = {'email': [('Nuevos_RegistradosPay-Tasa0', 'Tasa 0 a registrados sin crédito (Product Growth)'), ('BillPay_Intro', 'Lanzamiento BillPay (Others)')],
         'push notification': [('Anonimos-RescateTasa0', 'Rescate Tasa 0 a anónimos (Marketing)'), ('Marketing-KCash-B0326-Canvas-Leads-ReferralProgram', 'Referidos a leads (Marketing)')],
         'whatsapp': [('Nuevos_NeverActive-InstallmentsNoCash', 'Nunca activaron (Product Growth)')],
         'in-app': [('LanzamientoBillpayments_Onboarding', 'BillPay (Marketing)')]}
for (c, lab, mn), (px, py) in zip(CH, POS):
    sx = lambda v: px + PW * (math.log10(min(max(v, 5e4), 4e7)) - XL) / (XH - XL)
    sy = lambda v: py + PH - PH * (math.log10(min(max(v, 0.05), 20)) - YL) / (YH - YL)
    g = fa[fa.canal == c].sort_values('env', ascending=False)
    k = chs.loc[c]
    S.t(px, py - 18, f'{lab}: {int(k.nb)} de {int(k.n)} campañas debajo, {k.pv:.0f} % de sus mensajes', 11.5, INK, w=700)
    S.rect(px, sy(1), PW, py + PH - sy(1), BLUE, ' opacity="0.05"')
    for v in (0.1, 1, 10):
        S.line(px, sy(v), px + PW, sy(v), GRID if v != 1 else BLUE, 1 if v != 1 else 1.2, '' if v != 1 else ' stroke-dasharray="4 3"')
        S.t(px - 6, sy(v) + 4, f'{v:g}', 10.5, SEC if v != 1 else BLUE, 'end', 400 if v != 1 else 700)
    S.t(px, py - 5, mn[0].upper() + mn[1:], 10.5, BLUE, 'start', 600)
    for v, t in ((1e5, '100 mil'), (1e6, '1 M'), (1e7, '10 M')):
        S.line(sx(v), py + PH, sx(v), py + PH + 4, G1)
        S.t(sx(v), py + PH + 15, t, 10.5, SEC, 'middle')
    S.line(px, py + PH, px + PW, py + PH, G1)
    for q in g.itertuples():
        rr = 2.0 + 2.4 * math.sqrt(q.costo / 1e6) if c in ('email', 'whatsapp') else 2.4
        S.circle(sx(q.env), sy(q.ix), rr, BLUE if q.bajo else G1, ' fill-opacity="0.75" stroke="#FFFFFF" stroke-width="0.7"')
    for j, (key, nm) in enumerate(NAMES.get(c, [])):
        q = g[g.fam.str.contains(key, regex=False)].iloc[0]
        x, y = sx(q.env), sy(q.ix)
        ty = py + PH - 26 - 14 * j
        right = c == 'in-app'
        S.line(x, y, x + (10 if right else -10), ty + 2, INK, 0.6)
        S.t(x + (12 if right else -12), ty + 4, nm, 10.5, INK, 'start' if right else 'end', 600, halo=True)
        print(c, nm, round(q.env / 1e6, 1), round(q.pct, 2))
S.t(46, 416, 'Eje vertical: respuesta en veces el mínimo aceptable del canal (1 = justo el mínimo), escala por múltiplos. Horizontal: mensajes de la campaña.', 10.5, SEC)
svg = S.done()
save(19, dict(
    kind='grafica',
    titulo='Casi la mitad del volumen de promoción sale en campañas que no responden ni lo mínimo aceptable',
    que=f'Lanzamientos ({gn.loc["lanzamiento","pv"]:.0f} % de su volumen), Tasa 0 ({gn.loc["tasa0","pv"]:.0f} %), referidos ({gn.loc["referidos","pv"]:.0f} %).',
    quien=f'Others {eqs.loc["Others","pv"]:.0f} % de su promoción, Product Growth {eqs.loc["Product Growth","pv"]:.0f} %, Marketing {eqs.loc["Marketing","pv"]:.0f} %, Sales {eqs.loc["Sales","pv"]:.0f} %.',
    a_quien=f'Leads ({au.loc["leads","pv"]:.0f} % de su volumen) y bases frías ({au.loc["frios","pv"]:.0f} %); clientes activos {au.loc["activos","pv"]:.0f} %.',
    lecturas=[
        f'{int(tot.nb)} de {int(tot.n)} campañas no llegan al mínimo: {tot.envb:.0f} M mensajes ({tot.pv:.0f} %) y {tot.cb:.1f} M MXN.',
        f'El correo es el peor: {chs.loc["email","pv"]:.0f} % de sus mensajes de promoción van en campañas debajo del mínimo.',
        f'{sep} de esas campañas seguían saliendo en septiembre.',
    ],
    causa='Nadie mide cada campaña contra un mínimo común: sigue saliendo mes tras mes aunque casi nadie le responda.',
    sowhat='Revisar cada mes contra el mínimo: rehacer o quitar; a ex clientes, primero probar con un grupo sin envío.',
    fuente=f'{FUENTE_E1}. {int(tot.n)} campañas de promoción por canal con 50 mil o más mensajes entregados o vistos. Gasto con WhatsApp por entregado.',
    svg=svg,
))
