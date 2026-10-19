"""Lámina 49 (ronda 2). Dos paneles iguales (correo | WhatsApp). Cada punto es una campaña de recuperación (ex clientes o leads que nunca
activaron; 100 mil o más mensajes en el canal; con muestra de E9a). x = % de quienes NO abrieron que convirtió en los 90 días siguientes
(qué tan cerca está la base de volver sola); y = MXN por conversión del mismo día (E1). Escalas log; recta por mínimos cuadrados sobre log10."""
import math, re
import pandas as pd
from b5_svg import *

t = pd.read_csv(H / 'b5_camp.csv')
r = t[t.g.isin(['ex', 'nunca']) & t.canal.isin(['email', 'whatsapp']) & (t.muestra == True) & (t.env >= 100000) & (t.conv > 20)].copy()
REC = r'B0208|B0331|B0332|B0206|202600903'
r['cl'] = [('rec' if re.search(REC, f) else 'ex') if g == 'ex' else 'nunca' for f, g in zip(r.familia, r.g)]
COL = {'rec': BLUE, 'ex': BLUEL, 'nunca': MARK}
C = D['control']; P = D['prog']
S = Svg('Dos paneles, correo y WhatsApp. Cada punto es una campaña de recuperación: porcentaje de quienes no abrieron que convirtió en 90 días contra pesos por conversión, con recta y R cuadrada.')
lx = 0
for k, lab in [('rec', 'Ex clientes de hasta 6 meses'), ('ex', 'Ex clientes de 12 meses o sin plazo'), ('nunca', 'Leads que nunca activaron')]:
    S.circle(lx + 5, 12, 5, COL[k], '#FFFFFF', 1); S.t(lx + 15, 16, lab, 11, TXT); lx += 15 + len(lab) * 6.1 + 18
S.t(W, 16, 'Tamaño: mensajes', 10.5, SEC, 'end')
PAN = [('email', 'Correo', 40, 370), ('whatsapp', 'WhatsApp', 420, 750)]
Y0, Y1 = 58, 362
sy = logx(5, 10000, Y1, Y0)
LAB = {'Lending-KCash-B0208-CANVAS-Recurrentes_Inactivos30a90dias-SinYConDescuentoEscalonado-N/A|email': (8, -8, 'start'),
       'Lending-KCash-B0223-CANVAS-Nuevos_NeverActive-InstallmentsNoCash-N/A|email': (10, 4, 'start'),
       'Lending-KCash-B0209-CANVAS-Recurrentes_Inactivos-DescuentoDirecto-N/A|email': (10, 12, 'start'),
       'Lending-KPay-B0333-CANVAS-Churn_12MesesInactividad-ConSinOferta-N/A|whatsapp': (10, 4, 'start'),
       'Lending-KCash-B0223-CANVAS-Nuevos_NeverActive-InstallmentsNoCash-N/A|whatsapp': (10, 4, 'start'),
       'Lending-KPay-B0332-CANVAS-HardInactive_6MesesInactividad-ConSinOferta-N/A|whatsapp': (-10, -8, 'end'),
       'Lending-KCash-B0209-CANVAS-Recurrentes_Inactivos-DescuentoDirecto-N/A|whatsapp': (-10, 14, 'end')}
STATS = {}
for c, tit, X0, X1 in PAN:
    sx = logx(0.1, 50, X0, X1)
    d = r[r.canal == c]
    S.t(X0, 44, f'{tit}: {len(d)} campañas', 12, INK, w=600)
    for v in (10, 100, 1000, 10000):
        S.line(X0, sy(v), X1, sy(v)); S.t(X0 - 4, sy(v) + 4, fmt(v), 10.5, SEC, 'end')
    for v, lab in [(0.1, '0.1 %'), (1, '1 %'), (10, '10 %'), (50, '50 %')]:
        S.line(sx(v), Y0, sx(v), Y1); S.t(sx(v), Y1 + 15, lab, 10.5, SEC, 'middle')
    a0, b0, r2 = fit([math.log10(v) for v in d.cn_90], [math.log10(v) for v in d.mxn_conv])
    STATS[c] = (r2, len(d), b0)
    xa, xb = d.cn_90.min(), d.cn_90.max()
    S.line(sx(xa), sy(10 ** (a0 + b0 * math.log10(xa))), sx(xb), sy(10 ** (a0 + b0 * math.log10(xb))), INK, 1.5)
    S.t(X1, Y0 + 12, f'R² = {r2:.2f}', 11.5, INK, 'end', 600, halo=True)
    for q in d.sort_values('env', ascending=False).itertuples():
        S.circle(sx(q.cn_90), sy(q.mxn_conv), 2.5 + 6 * (q.env / 13.5e6) ** 0.5, COL[q.cl], '#FFFFFF', 1)
    for q in d.itertuples():
        k = f'{q.familia}|{c}'
        if k in LAB:
            dx, dy, an = LAB[k]
            S.t(sx(q.cn_90) + dx, sy(q.mxn_conv) + dy, f'{nombre(q.familia)}: {fmt(q.mxn_conv)}', 10.5, INK, an, 600, halo=True)
S.t(40, Y1 + 32, '% de quienes no abrieron el mensaje que convirtió en los 90 días siguientes (escala log)', 10.5, SEC)
S.t(W, Y1 + 32, 'Vertical: MXN por conversión (log)', 10.5, SEC, 'end')
SVG = S.done()

re_, rw = STATS['email'], STATS['whatsapp']
q8 = r[r.familia.str.contains('B0208') & (r.canal == 'email')].sort_values('env').iloc[-1]
q33 = r[r.familia.str.contains('B0333') & (r.canal == 'whatsapp')].sort_values('env').iloc[-1]
guarda(49, dict(
    kind='grafica',
    titulo='Recuperar sale barato si llegamos pronto: mientras más fría la base, más cara cada conversión',
    que='Descuento directo, descuento escalonado, "con o sin oferta", referidos y Tasa 0',
    quien='Product Growth (ex clientes) y Marketing (referidos a dormants, rescate Tasa 0 a leads)',
    a_quien='Ex clientes con 1 a 12 meses sin usar KCash o KPay, dormants y leads que nunca activaron',
    lecturas=[
        f'Inactivos 30 a 90 días: {q8.cn_90:.0f} % vuelve aunque no abra; por correo, {q8.mxn_conv:.0f} MXN por conversión y {q8.mxn_sol:.1f} por solicitud.',
        f'Churn 12 meses: {q33.cn_90:.0f} % vuelve sin abrir; su WhatsApp cuesta {fmt(q33.mxn_conv)} MXN por conversión y {q33.mxn_sol:.0f} por solicitud.',
        f'Sin grupo sin mensajes no sabemos cuánto recupera el mensaje: de {C["canvas"]} Canvas, ninguno tiene uno de verdad.',
    ],
    causa='La recuperación se arma por oferta, no por meses sin uso, y ningún programa de ex clientes deja un grupo sin mensajes.',
    sowhat='Ordenar, no dejar de buscar: primero quien se fue hace poco, con límite de gasto y un grupo sin mensajes.',
    fuente=f'Fuente: Braze E1 y E9a (conversión a 90 días de quien abre y quien no), E13 (control), enero a septiembre 2026. Solicitud: solicitudes registradas. Recta sobre log10; n = {re_[1]} y {rw[1]}.',
    svg=SVG,
))
print(STATS)
q = r[r.familia.str.contains('B0208') & (r.canal == 'email')].iloc[0]; print('b0208', q.cn_90, q.mxn_conv)
q = r[r.familia.str.contains('B0333') & (r.canal == 'whatsapp')].iloc[0]; print('b0333', q.cn_90, q.mxn_conv)
