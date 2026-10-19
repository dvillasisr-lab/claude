"""Lámina 33 (ronda 2): concentración (E3) en cifras y, como gráfica, una campaña por punto (E1, 9 meses):
mensajes por persona al mes contra respuesta, correo | push, con la línea del mínimo aceptable."""
import math, pandas as pd, numpy as np
from kit import *
e3 = pd.read_csv(D + 'e3_usuarios_distribucion.csv')
e3['costo'] = 0.05 * e3.msgs_email + 1.0 * e3.msgs_whatsapp_entregados
g = e3.groupby('banda_msgs')[['usuarios', 'msgs', 'msgs_push', 'costo', 'bajas_email', 'msgs_email', 'usuarios_con_conversion']].sum()
HI = ['41-80', '081-160', '161-320', '321+']; top, tot = g.loc[HI].sum(), g.sum()
sh = {c: 100 * top[c] / tot[c] for c in g.columns}
bm_hi = 1000 * top.bajas_email / top.msgs_email; bm_lo = 1000 * g.loc['01-05'].bajas_email / g.loc['01-05'].msgs_email
e1 = pd.read_csv(D + 'e1_comunicacion_mes_canal.csv'); e1['f'] = e1.communication_name.map(fam); e1['T'] = e1.team.map(team)
CH = {'email': ('email_delivery', 'email_click', 0.3, 4.0), 'push notification': ('pn_send', 'pn_open', 0.75, 6.0)}
P = {}
for c, (b, r, mn, ym) in CH.items():
    d = e1[e1.canal == c].groupby(['f', 'T']).agg(env=('envios', 'sum'), us=('usuarios_aprox', 'sum'), b=(b, 'sum'), r=(r, 'sum')).reset_index()
    d = d[d.env >= 500e3].copy(); d['tq'] = d.env / d.us; d['resp'] = 100 * d.r / d.b
    d['hi'] = d.tq >= 4; d['bajo'] = d.resp < mn
    P[c] = (d, ols(np.log10(d.tq), d.resp), mn, ym)
    x = d[d.hi]; print(c, len(d), 'r2', round(P[c][1]['r2'], 3), 'hi', len(x), 'bajo', int(x.bajo.sum()), 'env hi bajo M', x[x.bajo].env.sum() / 1e6)
print({k: round(v, 1) for k, v in sh.items()}, top.usuarios / 1e6, bm_hi, bm_lo)

S = Svg('Dos paneles, correo y push: una campaña por punto, mensajes por persona al mes contra respuesta, con la línea del mínimo aceptable')
S.circle(6, 15, 4.5, BLUE); S.t(15, 19, '4 o más al mes por persona y debajo del mínimo', 11, TXT)
S.circle(296, 15, 4.5, GREEN); S.t(305, 19, '4 o más al mes y pasa el mínimo', 11, TXT)
S.circle(500, 15, 4.5, G2); S.t(509, 19, 'Resto de campañas', 11, TXT)
S.t(0, 38, 'Una campaña por punto (500 mil o más mensajes en 9 meses); tamaño = mensajes. R² cerca de 0: mandar más seguido no predice la respuesta.', 10.5, SEC)
NAMES = {'email': [('B0000-CANVAS-Leads_LeftFunnel-Retargeting_Veriff', 'Recordatorio de registro', 'Marketing', 9.5, 3.75, 'end'),
                   ('B0211-CANVAS-Nuevos_RegistradosPay-Tasa0', 'Tasa 0 a registrados', 'Product Growth', 9.5, 2.45, 'end'),
                   ('T000-CANVAS-BKT1', 'Cobranza BKT1', 'Collections', 9.5, 1.6, 'end')],
         'push notification': [('T000-CANVAS-BKT1', 'Cobranza BKT1', 'Collections', 9.5, 5.6, 'end'),
                               ('B0211-CANVAS-Nuevos_RegistradosPay-Tasa0', 'Tasa 0 a registrados', 'Product Growth', 9.5, 4.6, 'end'),
                               ('B0171-CANVAS-Anonimos-RescateTasa0', 'Rescate Tasa 0 a anónimos', 'Marketing', 9.5, 3.6, 'end'),
                               ('B0561-CANVAS-Leads-Comerciodeldia', 'Comercio del día a leads', 'Marketing', 9.5, 2.6, 'end')]}
def panel(x0, c, title):
    d, fit, mn, ym = P[c]
    X0, X1, Y0, Y1 = x0 + 36, x0 + 368, 76, 352
    lo, hi = math.log10(0.8), math.log10(10)
    sx = lambda v: X0 + (X1 - X0) * (math.log10(v) - lo) / (hi - lo); sy = lambda v: Y1 - (Y1 - Y0) * min(v, ym) / ym
    S.t(x0, 60, f'{title} (R² {fit["r2"]:.2f})', 12, INK, w=700)
    for v in np.arange(0, ym + 0.01, 1 if ym <= 4 else 2):
        S.line(X0, sy(v), X1, sy(v)); S.t(X0 - 6, sy(v) + 4, f'{v:g} %', 10.5, SEC, 'end')
    for v in (1, 2, 4, 8):
        S.line(sx(v), Y1, sx(v), Y1 + 5, SEC); S.t(sx(v), Y1 + 18, f'{v}', 10.5, SEC, 'middle')
    S.line(X0, Y1, X1, Y1, SEC); S.t((X0 + X1) / 2, Y1 + 33, 'Mensajes por persona al mes (escala logarítmica)', 10.5, SEC, 'middle')
    S.line(sx(4), Y0, sx(4), Y1, G2, 1)
    S.line(X0, sy(mn), X1, sy(mn), GREEN, 1.2)
    S.t(sx(3.8), sy(mn) - 5, f'Mínimo: {mn:g} %', 10.5, GREEN, 'end', 700, halo=True)
    for _, q in d.sort_values('env', ascending=False).iterrows():
        col = (BLUE if q.bajo else GREEN) if q.hi else G2
        S.circle(sx(q.tq), sy(q.resp), 2.5 + 7 * math.sqrt(q.env / 35e6), col, '#FFFFFF', 1)
    for key, l1, l2, tx, ty, anc in NAMES[c]:
        q = d[d.f.str.contains(key)].sort_values('env').iloc[-1]
        lab(S, sx(q.tq), sy(q.resp), sx(tx), sy(ty), f'{l1}: {q.resp:.2f} %', f'{l2}, {q.tq:.1f} al mes', anc)
panel(0, 'email', 'Correo: clic por campaña')
panel(400, 'push notification', 'Push: apertura por campaña')
dE, dP = P['email'][0], P['push notification'][0]
nb = int(dE[dE.hi].bajo.sum() + dP[dP.hi].bajo.sum()); nh = int(dE.hi.sum() + dP.hi.sum())
write(33, dict(kind='grafica', seccion='IV. La misma persona, demasiadas veces',
 titulo='Una cuarta parte de la base recibe 86 % de los mensajes; sobra lo que ignora, no la persona',
 que='Cobranza, Comercio del día, recordatorio de registro, rescates por push y Tasa 0',
 quien='Marketing, Product Growth, Collections y Others (Shopping)',
 a_quien=f'{top.usuarios/1e6:.1f} M personas con 41 o más mensajes en 9 meses, unos 14 al mes',
 lecturas=[
  f'{sh["usuarios"]:.0f} % de las personas recibe {sh["msgs"]:.0f} % de los mensajes y {sh["costo"]:.0f} % del gasto, y es {sh["usuarios_con_conversion"]:.0f} % de quienes compraron.',
  f'Por correo se dan de baja menos: {bm_hi:.1f} bajas por mil correos, contra {bm_lo:.1f} en quien recibe 1 a 5.',
  f'{nb} de {nh} campañas que mandan 4 o más al mes por persona no llegan al mínimo: Rescate Tasa 0, Tasa 0 a registrados.',
 ],
 causa='Se corta por lista y no por respuesta: la misma persona recibe campañas que abre y otras que ignora desde hace meses.',
 sowhat='No cortar parejo a quien recibe mucho: quitar las campañas que esa persona ya no abre.',
 fuente='Fuente: Braze, enero a septiembre 2026. Concentración y bajas: E3 (bajas en eventos). Puntos: E1, campañas con 500 mil o más mensajes; mensajes por persona al mes = enviados entre personas por mes.',
 svg=S.svg()))
