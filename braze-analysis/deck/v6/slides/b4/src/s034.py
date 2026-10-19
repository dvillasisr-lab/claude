"""Lámina 34 (ronda 2): dos paneles. Izquierda: una campaña por punto (E8, campaña del día de la baja), correos que llevaba
la persona contra personas que se dieron de baja, nuevos contra base antigua. Derecha: una línea por mes (E6a), campañas el
mismo día contra bajas por mil personas-día."""
import math, pandas as pd, numpy as np
from kit import *
e8 = pd.read_csv(D + 'e8_dias_hasta_baja.csv'); f = e8[e8.bloque == 'familia_dia_baja'].copy()
res = e8[e8.bloque == 'resumen'].set_index('cohorte_limpia')
n8 = e8[(e8.bloque == 'banda_emails') & (e8.cohorte_limpia == 1)].set_index('clave').usuarios
p1 = 100 * n8['01'] / res.loc[1, 'usuarios']
a = pd.read_csv(D + 'e6a_solape_dia_mes.csv'); a['m'] = a.mes.str[5:7].astype(int)
a['r'] = 1000 * a.usuario_dias_con_baja / a.usuario_dias
B6 = ['1', '2', '3 a 4', '5 a 7', '8+']
def per(ms):
    d = a[a.m.isin(ms)].groupby('banda_familias_dia')[['usuario_dias', 'usuario_dias_con_baja']].sum()
    return 1000 * d.usuario_dias_con_baja / d.usuario_dias
em, js = per(range(1, 6)), per(range(7, 10))
e4 = pd.read_csv(D + 'e4b_concentracion_mes.csv'); g4 = e4.groupby('banda_msgs_mes')[['msgs_email', 'usuarios_con_baja_email']].sum()
m_lo = 1000 * g4.loc['01-05'].usuarios_con_baja_email / g4.loc['01-05'].msgs_email
m_hi = 1000 * g4.loc[['41-80', '081-160', '161+']].usuarios_con_baja_email.sum() / g4.loc[['41-80', '081-160', '161+']].msgs_email.sum()
print(p1, res[['usuarios', 'emails_mediana']], em.round(2).to_dict(), js.round(2).to_dict(), m_lo, m_hi)

S = Svg('Dos paneles: campañas desde las que la gente se dio de baja, por correos que llevaba la persona; y bajas por mil personas-día según campañas ese día, una línea por mes')
S.circle(6, 15, 4.5, BLUE); S.t(15, 19, 'Nuevos (primer correo en 2026)', 11, TXT)
S.circle(196, 15, 4.5, G1); S.t(205, 19, 'Base antigua', 11, TXT)
S.line(420, 15, 442, 15, BLUE, 2); S.t(448, 19, 'Junio a septiembre', 11, TXT)
S.line(570, 15, 592, 15, G1, 1.5); S.t(598, 19, 'Enero a mayo', 11, TXT)
# panel izquierdo
X0, X1, Y0, Y1 = 40, 372, 70, 352
lo, hi = math.log10(0.8), math.log10(80)
sx = lambda v: X0 + (X1 - X0) * (math.log10(v) - lo) / (hi - lo); sy = lambda v: Y1 - (Y1 - Y0) * v / 50
S.t(0, 52, 'Por campaña: correos que llevaba al darse de baja', 12, INK, w=700)
for v in (0, 10, 20, 30, 40, 50):
    S.line(X0, sy(v), X1, sy(v)); S.t(X0 - 6, sy(v) + 4, f'{v} mil', 10.5, SEC, 'end')
for v in (1, 3, 10, 30):
    S.line(sx(v), Y1, sx(v), Y1 + 5, SEC); S.t(sx(v), Y1 + 18, f'{v}', 10.5, SEC, 'middle')
S.line(X0, Y1, X1, Y1, SEC); S.t((X0 + X1) / 2, Y1 + 33, 'Correos recibidos al darse de baja, mediana (escala logarítmica)', 10.5, SEC, 'middle')
for c, col in ((0, G1), (1, BLUE)):
    md = res.loc[c, 'emails_mediana']; S.line(sx(md), Y0, sx(md), Y1, col, 1)
    S.t(sx(md) + 4, Y1 - 50 - 14 * c, f'Mediana {"nuevos" if c else "base antigua"}: {md:.0f}', 10.5, col if c else TXT, 'start', 600, halo=True)
for _, q in f.sort_values('cohorte_limpia').iterrows():
    S.circle(sx(max(q.emails_mediana, 0.9)), sy(q.usuarios / 1e3), 4, BLUE if q.cohorte_limpia == 1 else G1, '#FFFFFF', 1)
def nm(key, c, tx, ty, l1, l2, anc='start'):
    q = f[f.clave.str.contains(key) & (f.cohorte_limpia == c)].iloc[0]
    lab(S, sx(max(q.emails_mediana, 0.9)), sy(q.usuarios / 1e3), sx(tx), sy(ty), f'{l1}: {q.usuarios/1e3:.0f} mil', l2, anc)
nm('BillPay_Intro', 1, 1.6, 47, 'BillPay Intro', 'NewProducts, 1 correo recibido')
nm('Retargeting_Veriff', 1, 1.6, 36, 'Recordatorio de registro', 'Marketing, al 6.º correo')
nm('B0211-CANVAS-Nuevos_RegistradosPay-Tasa0', 0, 75, 39, 'Tasa 0 a registrados', 'Product Growth, al 26.º', 'end')
nm('B0326-Canvas-Leads-ReferralProgram', 0, 75, 20, 'Referidos', 'Marketing, al 18.º', 'end')
# panel derecho
X0, X1, Y0, Y1 = 446, 750, 70, 352
sx2 = lambda i: X0 + (X1 - X0) * i / 4; sy2 = lambda v: Y1 - (Y1 - Y0) * v / 1.4
S.t(406, 52, 'Por día: bajas según campañas ese día', 12, INK, w=700)
for v in (0, 0.4, 0.8, 1.2):
    S.line(X0, sy2(v), X1, sy2(v)); S.t(X0 - 6, sy2(v) + 4, f'{v:.1f}', 10.5, SEC, 'end')
S.t(X0 - 6, Y0 - 6, 'Bajas por mil personas-día', 10.5, SEC, 'start')
for i, k in enumerate(['1', '2', '3 a 4', '5 a 7', '8 o más']):
    S.t(sx2(i), Y1 + 18, k, 10.5, SEC, 'middle')
S.line(X0, Y1, X1, Y1, SEC); S.t((X0 + X1) / 2, Y1 + 33, 'Campañas distintas que recibió la persona ese día', 10.5, SEC, 'middle')
for m in sorted(a.m.unique(), key=lambda m: m >= 6):
    r = a[a.m == m].set_index('banda_familias_dia').r.reindex(B6)
    S.poly([(sx2(i), sy2(v)) for i, v in enumerate(r)], BLUE if m >= 6 else G1, 1.8 if m >= 6 else 1.2)
for i, k in enumerate(B6):
    pass
S.t(sx2(4) - 6, sy2(js['8+']) - 30, f'Julio a sept.: {js["1"]:.2f} con una,', 10.5, BLUE, 'end', 700, halo=True)
S.t(sx2(4) - 6, sy2(js['8+']) - 17, f'{js["8+"]:.2f} con 8 o más', 10.5, BLUE, 'end', 700, halo=True)
S.t(sx2(1), sy2(em['1']) + 40, f'Enero a mayo: {em["1"]:.2f} con una y {em["8+"]:.2f} con 8 o más', 10.5, TXT, 'start', 600, halo=True)

write(34, dict(kind='grafica', seccion='IV. La misma persona, demasiadas veces',
 titulo='Las bajas vienen del primer correo a quien no nos conoce y del día saturado, no del total de mensajes',
 que='Correos promocionales: BillPay, recordatorio de registro, Tasa 0 y referidos',
 quien='NewProducts y Marketing en los nuevos; Marketing y Product Growth en la base antigua',
 a_quien=f'{res.loc[1,"usuarios"]/1e3:.0f} mil nuevos y {res.loc[0,"usuarios"]/1e3:.0f} mil de la base antigua que se dieron de baja',
 lecturas=[
  f'{p1:.0f} % de los nuevos que se van recibió un solo correo; el lanzamiento de BillPay se llevó 49 mil así.',
  f'Por día: de julio a septiembre, 8 o más campañas traen {js["8+"]:.2f} bajas por mil contra {js["1"]:.2f} con una.',
  f'En el mes también: {m_lo:.1f} bajas por mil correos con 1 a 5 mensajes al mes, {m_hi:.1f} con 41 o más.',
 ],
 causa='Escribimos igual a quien no nos conoce que al cliente, y en días de lanzamiento se juntan campañas sin que nadie lo vea.',
 sowhat='El límite con datos es por día y para el nuevo: dos promocionales al día y una sola serie de bienvenida.',
 fuente='Fuente: Braze, enero a septiembre 2026. Campañas: E8 (campaña del día de la baja; nuevos = primer correo en el periodo). Día: E6a. Mes: E4b. Todas en personas.',
 svg=S.svg()))
