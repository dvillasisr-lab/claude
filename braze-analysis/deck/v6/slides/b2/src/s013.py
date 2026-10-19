"""Lámina 13: Cash, MXN por conversión por WhatsApp contra correo, por audiencia y por tema (mancuernas, eje logarítmico),
con cuántas veces más cuesta WhatsApp y su gasto."""
import math
from b2base import *

d = load_b()
c = d[d.product_service == 'Cash']
cpc = lambda g: g.costo.sum() / max(1, g.conversiones_fraccional.sum())
w, e = c[c.canal == 'whatsapp'], c[c.canal == 'email']
pa = c[c.canal.isin(['push notification', 'in-app'])]
TOT = dict(wa=cpc(w), em=cpc(e), wc=w.costo.sum() / 1e6, ec=e.costo.sum() / 1e6, wk=w.conversiones_fraccional.sum() / 1e3, ek=e.conversiones_fraccional.sum() / 1e3)
print('total', {k: round(v, 1) for k, v in TOT.items()}, 'veces', TOT['wa'] / TOT['em'], 'push+inapp conv', pa.conversiones_fraccional.sum())
AUD = [('activos', 'Clientes activos'), ('leads', 'Leads'), ('nuevos', 'Registrados nuevos'), ('frios', 'Bases frías')]
TEM = [('tasa0', 'Tasa 0'), ('referidos', 'Referidos'), ('recordatorio', 'Recordatorios'), ('descuento', 'Descuentos'), ('otros', 'Otras ofertas')]
rows = []
for key, col, lst in (('aud', 'Por audiencia', AUD), ('gan', 'Por tema', TEM)):
    rows.append(('h', col))
    for k, lab in lst:
        ww, ee = w[w[key] == k], e[e[key] == k]
        rows.append(('r', lab, cpc(ww), cpc(ee), ww.costo.sum() / 1e6, 100 * ww.costo.sum() / w.costo.sum()))
for r in rows:
    print(r if r[0] == 'h' else (r[1], round(r[2], 1), round(r[3], 1), round(r[2] / r[3], 1), round(r[4], 1), round(r[5], 0)))
eqw = w.groupby('equipo').costo.sum() / w.costo.sum() * 100
eqe = e.groupby('equipo').costo.sum() / e.costo.sum() * 100
print('equipo WA', eqw.round(0).to_dict(), 'email', eqe.round(1).to_dict())
fam = w.groupby('fam').apply(lambda g: pd.Series({'c': g.costo.sum() / 1e6, 'cpc': cpc(g)}))
resc = fam.loc[[i for i in fam.index if 'Leads_BBDDRezagada-RescateTasa0-N/A' in i]].iloc[0]
print('rescate', resc.to_dict())

S = Svg('Mancuernas: MXN por conversión de Cash por WhatsApp y por correo, por audiencia y por tema; WhatsApp cuesta más en todas las filas.')
X0, X1 = 150, 560
LO, HI = math.log10(2), math.log10(1000)
sx = lambda v: X0 + (X1 - X0) * (math.log10(v) - LO) / (HI - LO)
# leyenda
S.circle(5, 14, 5.5, BLUE, '')
S.t(15, 18, 'WhatsApp', 11.5, INK, w=600)
S.circle(95, 14, 5.5, GREEN, '')
S.t(105, 18, 'Correo', 11.5, INK, w=600)
S.t(170, 18, 'MXN por cada conversión de Cash, en escala que crece por múltiplos', 11, SEC)
C1, C2 = 640, 752
S.t(C1, 44, 'WhatsApp cuesta', 10.5, SEC, 'end')
S.t(C1, 57, 'más que el correo', 10.5, SEC, 'end')
S.t(C2, 44, 'Gasto WhatsApp', 10.5, SEC, 'end')
S.t(C2, 57, 'M MXN', 10.5, SEC, 'end')
YT = 66
# fila total
yy = 86
S.rect(0, yy - 15, 780, 26, '#F3F5F8')
S.t(0, yy + 2, 'Todo Cash', 11.5, INK, w=700)
S.line(sx(TOT['em']), yy - 2, sx(TOT['wa']), yy - 2, G2, 3)
S.circle(sx(TOT['em']), yy - 2, 6, GREEN, ' stroke="#FFFFFF" stroke-width="2"')
S.circle(sx(TOT['wa']), yy - 2, 6, BLUE, ' stroke="#FFFFFF" stroke-width="2"')
S.t(sx(TOT['em']) - 10, yy + 2, f'{TOT["em"]:.0f}', 11, GREEN, 'end', 700, halo=True)
S.t(sx(TOT['wa']) + 10, yy + 2, f'{TOT["wa"]:.0f}', 11, BLUE, 'start', 700, halo=True)
S.t(C1, yy + 2, f'{TOT["wa"]/TOT["em"]:.1f} veces', 11.5, INK, 'end', 700)
S.t(C2, yy + 2, f'{TOT["wc"]:.1f}', 11.5, INK, 'end', 700)
yy += 30
top = yy
# primera pasada: posiciones
pos = []
for r in rows:
    if r[0] == 'h':
        yy += 8; pos.append(yy); yy += 24
    else:
        pos.append(yy); yy += 25
for v in (3, 10, 30, 100, 300, 1000):
    S.line(sx(v), top, sx(v), yy - 8, GRID)
    S.t(sx(v), yy + 8, f'{v:,}', 10.5, SEC, 'middle')
for r, yy in zip(rows, pos):
    if r[0] == 'h':
        S.t(0, yy + 2, r[1], 10.5, SEC, w=600)
        S.line(0, yy + 8, 780, yy + 8, GRID)
        continue
    _, lab, wa, em, gc, gp = r
    big = gp >= 15
    S.t(0, yy + 2, lab, 11.5, INK if big else TXT, w=600 if big else 400)
    S.line(sx(em), yy - 2, sx(wa), yy - 2, G2, 3)
    S.circle(sx(em), yy - 2, 5.5, GREEN, ' stroke="#FFFFFF" stroke-width="2"')
    S.circle(sx(wa), yy - 2, 5.5, BLUE, ' stroke="#FFFFFF" stroke-width="2"')
    S.t(sx(em) - 9, yy + 2, f'{em:.0f}' if em >= 10 else f'{em:.1f}', 11, GREEN, 'end', 600, halo=True)
    S.t(sx(wa) + 9, yy + 2, f'{wa:,.0f}', 11, BLUE, 'start', 600, halo=True)
    S.t(C1, yy + 2, f'{wa/em:.1f} veces', 11.5, INK if big else TXT, 'end', 600 if big else 400)
    S.t(C2, yy + 2, f'{gc:.1f}', 11.5, INK if big else TXT, 'end', 600 if big else 400)
print('alto final', yy + 24)
svg = S.done()
R = dict((r[1], r) for r in rows if r[0] == 'r')
save(13, dict(
    kind='grafica',
    titulo='Una conversión de Cash por WhatsApp cuesta más de siete veces lo que cuesta por correo, y pasa con todas las audiencias',
    que=f'Por WhatsApp a Cash: Tasa 0 ({R["Tasa 0"][5]:.0f} % del gasto), referidos ({R["Referidos"][5]:.0f} %) y recordatorios ({R["Recordatorios"][5]:.0f} %). Por correo: ofertas, Tasa 0, recordatorios y cobranza.',
    quien=f'WhatsApp de Cash: Marketing {eqw["Marketing"]:.0f} % del gasto y Product Growth {eqw["Product Growth"]:.0f} %. Correo de Cash: Product Growth {eqe["Product Growth"]:.0f} %, Marketing {eqe["Marketing"]:.0f} %, Collections {eqe["Collections"]:.0f} %.',
    a_quien='Clientes activos, leads, registrados nuevos y bases frías (ex clientes y leads que nunca activaron) con producto Cash (préstamo personal).',
    lecturas=[
        f'Todo Cash: WhatsApp {TOT["wc"]:.1f} M MXN y {TOT["wk"]:.0f} mil conversiones, {TOT["wa"]:.0f} MXN cada una. Correo {TOT["ec"]:.1f} M MXN y {TOT["ek"]:.0f} mil, {TOT["em"]:.0f} MXN cada una.',
        f'Con la misma audiencia WhatsApp cuesta de {R["Leads"][2]/R["Leads"][3]:.0f} a {R["Clientes activos"][2]/R["Clientes activos"][3]:.0f} veces más: clientes activos {R["Clientes activos"][2]:.0f} contra {R["Clientes activos"][3]:.1f} MXN; bases frías {R["Bases frías"][2]:.0f} contra {R["Bases frías"][3]:.0f}.',
        f'Tasa 0 es lo más caro en los dos canales: {R["Tasa 0"][2]:.0f} MXN por WhatsApp y {R["Tasa 0"][3]:.0f} por correo. Push e in-app traen {pa.conversiones_fraccional.sum()/1e3:.0f} mil conversiones de Cash sin costo.',
    ],
    causa='WhatsApp es el canal por defecto para vender Cash, aun con quien responde al correo o a la app, porque nadie compara cuánto cuesta cada conversión en cada canal.',
    sowhat='Para Cash, primero correo, push e in-app; WhatsApp solo donde esos no llegan o donde el monto del préstamo lo paga.',
    fuente=f'{FUENTE_E1}; producto Cash. Conversión: préstamo de Cash en los 7 días después del mensaje, repartido entre los mensajes que la persona recibió ese día; no prueba que el mensaje lo causó. WhatsApp a 1.00 MXN por entregado, email a 0.05 MXN por enviado, sin licencia de Braze.',
    svg=svg,
))
