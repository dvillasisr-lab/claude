"""Lámina 34: bajas según el periodo de medición (E3 nueve meses, E4b un mes, E6a un día) y nuevos por número de correo (E8)."""
import pandas as pd
from kit import *
# 9 meses (E3): bajas son eventos
e3 = pd.read_csv(D + 'e3_usuarios_distribucion.csv')
g3 = e3.groupby('banda_msgs')[['usuarios', 'msgs_email', 'bajas_email']].sum()
B3 = [('1 a 5', ['01-05']), ('6 a 20', ['06-10', '11-20']), ('21 a 80', ['21-40', '41-80']), ('81 a 320', ['081-160', '161-320']), ('321 o más', ['321+'])]
p3 = [(l, 1000 * g3.loc[k].bajas_email.sum() / g3.loc[k].msgs_email.sum(), 100 * g3.loc[k].bajas_email.sum() / g3.loc[k].usuarios.sum()) for l, k in B3]
# 1 mes (E4b): personas
e4 = pd.read_csv(D + 'e4b_concentracion_mes.csv')
g4 = e4.groupby('banda_msgs_mes')[['usuarios', 'msgs_email', 'usuarios_con_baja_email']].sum()
B4 = [('1 a 5', ['01-05']), ('6 a 10', ['06-10']), ('11 a 20', ['11-20']), ('21 a 40', ['21-40']), ('41 o más', ['41-80', '081-160', '161+'])]
p4 = [(l, 1000 * g4.loc[k].usuarios_con_baja_email.sum() / g4.loc[k].msgs_email.sum(), 100 * g4.loc[k].usuarios_con_baja_email.sum() / g4.loc[k].usuarios.sum()) for l, k in B4]
# 1 día (E6a): personas-día
a = pd.read_csv(D + 'e6a_solape_dia_mes.csv'); a['m'] = a.mes.str[5:7].astype(int)
def per(ms):
    d = a[a.m.isin(ms)].groupby('banda_familias_dia')[['usuario_dias', 'usuario_dias_con_baja']].sum()
    return 1000 * d.usuario_dias_con_baja / d.usuario_dias
em, js = per(range(1, 6)), per(range(7, 10))
B6 = ['1', '2', '3 a 4', '5 a 7', '8+']; B6L = ['1', '2', '3 a 4', '5 a 7', '8 o más']
# nuevos (E8, cohorte limpia = primer correo dentro del periodo)
e8 = pd.read_csv(D + 'e8_dias_hasta_baja.csv')
n8 = e8[(e8.bloque == 'banda_emails') & (e8.cohorte_limpia == 1)].set_index('clave').usuarios
tot_n = e8[(e8.bloque == 'resumen') & (e8.cohorte_limpia == 1)].usuarios.sum(); tot_v = e8[(e8.bloque == 'resumen') & (e8.cohorte_limpia == 0)].usuarios.sum()
B8 = [('1', '01'), ('2 a 3', '02 a 3'), ('4 a 10', '04 a 10'), ('11 a 30', '11 a 30'), ('31 o más', '31+')]
p8 = [(l, 100 * n8[k] / tot_n) for l, k in B8]
print(p3, p4, em.round(2).to_dict(), js.round(2).to_dict(), p8, tot_n, tot_v, sep='\n')

S = Svg('Cuatro paneles: bajas por mil correos según mensajes en nueve meses y en un mes; bajas por mil personas-día según campañas el mismo día; y nuevos que se dan de baja según cuántos correos llevaban')
PW, PH = 360, 140
def panel(x0, y0, title, sub, cats, series, vmax, fmtv, ticks, unit):
    S.t(x0, y0, title, 12, INK, w=700); S.t(x0, y0 + 15, sub, 10.5, SEC)
    X0, X1, Y1 = x0 + 30, x0 + PW, y0 + 30 + PH - 22
    Y0 = y0 + 40
    vy = lambda v: Y1 - (Y1 - Y0) * v / vmax
    for tk in ticks:
        S.line(X0, vy(tk), X1, vy(tk)); S.t(X0 - 5, vy(tk) + 3.5, f'{tk:g}', 10.5, SEC, 'end')
    st = (X1 - X0) / len(cats); ns = len(series); bw = st * (0.56 if ns == 1 else 0.36)
    for i, c in enumerate(cats):
        cx = X0 + st * (i + 0.5)
        for j, (vals, col) in enumerate(series):
            v = vals[i]; x = cx - (ns * bw) / 2 + j * bw + (1 if j else 0)
            S.rect(x, vy(v), bw - (2 if ns > 1 else 0), vy(0) - vy(v), col[i] if isinstance(col, list) else col)
            S.t(x + bw / 2 - (1 if ns > 1 else 0), vy(v) - 4, fmtv(v), 10.5, INK, 'middle', 600)
        S.t(cx, Y1 + 14, c, 10.5, TXT, 'middle')
    pass
# fila 1
panel(0, 14, 'Nueve meses: quien recibe mucho se va menos por correo', 'Bajas por mil correos, según mensajes recibidos en 9 meses',
      [l for l, *_ in p3], [([v for _, v, _ in p3], G1)], 16, lambda v: f'{v:.1f}', (0, 5, 10, 15), 'Mensajes en 9 meses')
panel(410, 14, 'Un mes: igual, quien recibe poco se va más', 'Bajas por mil correos, según mensajes recibidos en el mes',
      [l for l, *_ in p4], [([v for _, v, _ in p4], G1)], 4, lambda v: f'{v:.1f}', (0, 1, 2, 3, 4), 'Mensajes en el mes')
# fila 2
S.rect(0, 222, 10, 10, G1); S.t(14, 231, 'Enero a mayo', 10.5, TXT); S.rect(96, 222, 10, 10, BLUE); S.t(110, 231, 'Julio a septiembre', 10.5, TXT)
panel(0, 214 + 34, 'Un día: desde junio, el día saturado sí trae bajas', 'Bajas por mil personas-día, según campañas distintas ese día',
      B6L, [([em[k] for k in B6], G1), ([js[k] for k in B6], BLUE)], 1.2, lambda v: f'{v:.2f}', (0, 0.4, 0.8, 1.2), 'Campañas el mismo día')
panel(410, 214 + 34, 'Nuevos: uno de cada tres se va con el primer correo', '% de los nuevos que se dieron de baja, según correos que llevaban',
      [l for l, _ in p8], [([v for _, v in p8], [BLUE] + [G1] * 4)], 40, lambda v: f'{v:.0f} %', (0, 10, 20, 30, 40), 'Correos recibidos al darse de baja')
svg = S.svg()

write(34, dict(kind='grafica', seccion='IV. La misma persona, demasiadas veces',
 titulo='Las bajas vienen del primer correo a quien no nos conoce y del día saturado, no del total de mensajes',
 que='Correos promocionales: lanzamiento de BillPay, recordatorio de terminar el registro, Tasa 0 y referidos. Solo el correo registra bajas; en push no sabemos quién apaga las notificaciones.',
 quien='Nuevos: NewProducts (BillPay Intro, 31 % de sus bajas) y Marketing (recordatorio de registro, 22 %). Base antigua: Marketing 39 % y Product Growth 36 % de las bajas.',
 a_quien=f'Nuevos: {tot_n/1e3:.0f} mil personas que recibieron su primer correo dentro del periodo y se dieron de baja. Base antigua: {tot_v/1e3:.0f} mil que ya recibían correos antes de enero.',
 lecturas=[
  f'En 9 meses y en un mes pasa lo mismo: quien recibe poco se da de baja más por correo ({p3[0][1]:.1f} bajas por mil correos con 1 a 5 mensajes, {p3[-1][1]:.1f} con 321 o más). El total acumulado no explica las bajas.',
  f'Por día sí hay saturación, pero solo desde junio: de julio a septiembre, el día con 8 o más campañas trae {js["8+"]:.2f} bajas por mil personas contra {js["1"]:.2f} con una. De enero a mayo no hay diferencia ({em["1"]:.2f} contra {em["8+"]:.2f}).',
  f'{p8[0][1]:.0f} % de los nuevos que se van lo hace con el primer correo; BillPay Intro explica 31 % de esas bajas.',
 ],
 causa='Escribimos igual a quien no nos conoce que a quien ya es cliente, y en los días de lanzamientos se juntan varias campañas sobre la misma persona sin que nadie lo vea.',
 sowhat='El límite que sí tiene datos es por día y para el nuevo: máximo dos promocionales al día y una sola serie de bienvenida.',
 fuente='Fuente: Braze, enero a septiembre 2026. Nueve meses: E3 (bajas en eventos); un mes: E4b (personas); un día: E6a (personas-día); nuevos y base antigua: E8 (campaña del día de la baja). El salto "de cinco a seis mensajes" era de nueve meses y no sostiene un límite semanal.',
 svg=svg))
