"""Lámina 8: concentración de mensajes por persona (curva acumulada, Pareto). Grupos de E3 (banda × suscripción × etapa × canal
contactable) ordenados de más a menos mensajes por persona; eje x = % acumulado de personas (escala logarítmica); líneas =
% acumulado de mensajes, de personas con conversión y de bajas de correo. Marca la banda de 321 o más."""
import numpy as np, pandas as pd
from comun import Svg, write, ROOT, INK, TXT, SEC, GRID, BLUE, GREEN, G1, G2

e = pd.read_csv(ROOT / 'data/e3_usuarios_distribucion.csv')
U_all, M_all = e.usuarios.sum(), e.msgs.sum()
top = e[e.banda_msgs == '321+']; tu, tm = top.usuarios.sum(), top.msgs.sum()
cw = (top.comms_distintas_prom * top.usuarios).sum() / tu; dw = (top.dias_con_envio_prom * top.usuarios).sum() / tu
tconv = top.usuarios_con_conversion.sum() / tu
b15 = e[e.banda_msgs == '01-05']; b15_u = b15.usuarios.sum()
x = e[e.msgs > 0].copy(); x['mpp'] = x.msgs / x.usuarios; x = x.sort_values('mpp', ascending=False)
cu = np.r_[0, (x.usuarios.cumsum() / x.usuarios.sum()).values]
SER = [('msgs', 'Mensajes', BLUE, 2.6), ('usuarios_con_conversion', 'Personas con una conversión', GREEN, 2.2), ('bajas_email', 'Bajas de correo', G1, 1.8)]
cc = {k: np.r_[0, (x[k].cumsum() / x[k].sum()).values] for k, *_ in SER}
at = lambda k, p: float(np.interp(p, cu, cc[k]))
p_top = tu / x.usuarios.sum()
v_top = {k: at(k, p_top) for k, *_ in SER}; v10 = {k: at(k, 0.10) for k, *_ in SER}
# inicio de cada banda en el eje de personas
bands = x.groupby('banda_msgs').usuarios.sum().reindex(['321+', '161-320', '081-160', '41-80', '21-40', '11-20', '06-10', '01-05'])
bstart = (bands.cumsum() - bands) / x.usuarios.sum()
print(p_top, v_top, v10, tu, tm / 1e6, tm / tu, cw, dw, tconv, b15_u / U_all, M_all / U_all)

S = Svg('Porcentaje acumulado de mensajes, de personas con conversión y de bajas de correo según el porcentaje de personas que más mensajes recibe')
lx = 0
for k, lab, col, w in SER:
    S.line(lx, 14, lx + 20, 14, col, 2.5); S.t(lx + 26, 18, lab, 11.5, TXT); lx += 26 + len(lab) * 6.3 + 22
S.line(lx, 14, lx + 20, 14, G2, 1.5); S.t(lx + 26, 18, 'Reparto parejo', 11.5, SEC)
X0, X1, Y0, Y1 = 46, 760, 66, 360
LO = -3
xx = lambda p: X0 + (X1 - X0) * (np.log10(max(p, 1e-3)) - LO) / (0 - LO)
yy = lambda v: Y1 - (Y1 - Y0) * v
for v in (0, .25, .5, .75, 1):
    S.line(X0, yy(v), X1, yy(v), GRID); S.t(X0 - 6, yy(v) + 4, f'{v * 100:.0f} %', 11, SEC, 'end')
for p, lab in ((0.001, '0.1 %'), (0.01, '1 %'), (0.1, '10 %'), (1, '100 %')):
    S.line(xx(p), Y1, xx(p), Y1 + 4, G1); S.t(xx(p), Y1 + 17, lab, 11, SEC, 'middle')
S.t(X1, Y1 + 34, 'Personas ordenadas de más a menos mensajes recibidos, % acumulado (escala logarítmica)', 10.5, SEC, 'end')
# bandas arriba
for bnd, lab in (('321+', '321 o más'), ('161-320', '161 a 320'), ('081-160', '81 a 160'), ('41-80', '41 a 80'), ('21-40', '21 a 40'), ('01-05', '1 a 5')):
    p0 = max(bstart[bnd], 1e-3); S.line(xx(p0), Y0 - 6, xx(p0), Y0, G1)
    S.t(xx(p0) + 3, Y0 - 8, lab, 10.5, INK if bnd == '321+' else SEC, 'start', 600 if bnd == '321+' else 400)
S.t(X0, Y0 - 24, 'Mensajes por persona en nueve meses, desde donde empieza cada grupo:', 10.5, SEC)
grid = np.logspace(LO, 0, 300)
S.poly([(xx(p), yy(p)) for p in grid], G2, 1.5)
for k, lab, col, w in SER[::-1]:
    S.poly([(xx(p), yy(at(k, p))) for p in grid], col, w)
# marca de la banda de 321 o más
S.line(xx(p_top), Y0, xx(p_top), Y1, INK, 1, ' stroke-dasharray="3 3"')
LBL = {'msgs': 'de los mensajes', 'usuarios_con_conversion': 'de las personas con conversión', 'bajas_email': 'de las bajas de correo'}
for k, lab, col, w in SER:
    S.circle(xx(p_top), yy(v_top[k]), 4.5, col)
    S.t(xx(p_top) - 8, yy(v_top[k]) + 4, f'{v_top[k] * 100:.0f} % {LBL[k]}', 11.5, col if k != 'bajas_email' else TXT, 'end', 700, halo=True)
S.t(xx(p_top) + 6, yy(0.95), f'{tu / 1e3:.0f} mil personas', 12, INK, 'start', 700, halo=True)
S.t(xx(p_top) + 6, yy(0.95) + 15, f'({p_top * 100:.1f} % de la base): {tm / tu:.0f} mensajes cada una', 11, INK, 'start', 400, halo=True)
S.circle(xx(0.10), yy(v10['msgs']), 4, BLUE)
S.t(xx(0.10) + 8, yy(v10['msgs']) + 16, f'10 % de las personas: {v10["msgs"] * 100:.0f} % de los mensajes', 11, BLUE, 'start', 600, halo=True)

write(8, dict(kind='grafica',
    titulo=f'El promedio esconde a {tu / 1e3:.0f} mil personas que reciben casi dos mensajes al día, y son las que más convierten',
    que='Sobre todo push: Comercio del día, rescates de Tasa 0, cuponeras y cobranza.',
    quien='Marketing y Product Growth repiten más mensajes a la misma persona en el mes.',
    a_quien=f'Personas activas: {tconv * 100:.0f} % de las que reciben 321 o más tuvo una conversión.',
    lecturas=[
        f'{p_top * 100:.1f} % de las personas recibe {v_top["msgs"] * 100:.0f} % de los mensajes: {tm / tu:.0f} cada una, en {dw:.0f} de los 273 días.',
        f'{b15_u / U_all * 100:.0f} % de las personas recibe de 1 a 5 mensajes; el promedio de {M_all / U_all:.0f} lo jalan los de arriba.',
        f'Ese {p_top * 100:.1f} % entra a {cw:.0f} campañas distintas y pone {v_top["usuarios_con_conversion"] * 100:.0f} % de las personas que convierten.'],
    causa='Cada campaña decide sola a quién entra y no hay límite de mensajes por persona a la semana: al más activo le llegan todas.',
    sowhat='Saturamos a los mejores clientes: un límite de 5 promociones a la semana los protege sin dejar de escribirles.',
    fuente=f'Fuente: Braze, mensajes por persona (E3), enero a septiembre 2026: {U_all / 1e6:.1f} M personas y {M_all / 1e6:.0f} M mensajes. Bajas = eventos de baja de correo. E3 no trae equipo.',
    svg=S.done()))
