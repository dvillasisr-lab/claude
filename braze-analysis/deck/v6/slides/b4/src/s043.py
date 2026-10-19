"""Lámina 43: semana del 1 de junio. Correos por semana (E4a) con BillPay Intro aparte (E1), clic semanal con y sin BillPay Intro."""
import pandas as pd
from kit import *
e = pd.read_csv(D + 'e4a_serie_semana_mes_canal.csv')
w = e[(e.grano == 'semana') & (e.canal == 'email') & (e.periodo >= '2026-04-27') & (e.periodo <= '2026-07-27')].set_index('periodo')
mo = e[(e.grano == 'mes') & (e.canal == 'email')].set_index('periodo')
pu = e[(e.grano == 'semana') & (e.canal == 'push notification')].set_index('periodo')
e1 = pd.read_csv(D + 'e1_comunicacion_mes_canal.csv')
bi = e1[(e1.canal == 'email') & e1.communication_name.str.contains('BillPay_Intro') & e1.mes.str.startswith('2026-06')].iloc[0]
B = '2026-06-01'
clic = 100 * w.email_click / w.email_delivery
sin = clic.copy(); sin[B] = 100 * (w.loc[B, 'email_click'] - bi.email_click) / (w.loc[B, 'email_delivery'] - bi.email_delivery)
share = 100 * bi.envios / w.loc[B, 'email_sent']
cm = 100 * mo.email_click / mo.email_delivery
em6 = e1[(e1.canal == 'email') & e1.mes.str.startswith('2026-06')]
jun_sin = 100 * (em6.email_click.sum() - bi.email_click) / (em6.email_delivery.sum() - bi.email_delivery)
costo = 0.05 * bi.envios / 1e6
po = 100 * pu.pn_open / pu.pn_send
print(clic.round(2).to_dict(), sin[B], share, cm.round(2).to_dict(), jun_sin, costo, 100 * bi.email_open / bi.email_delivery, 100 * bi.email_click / bi.email_delivery, po['2026-06-08'], po['2026-06-15'])
wks = list(w.index)
S = Svg('Correos por semana, en barras, con BillPay Intro aparte, y clic de email por semana con y sin BillPay Intro, mayo a julio 2026')
S.legend([('sq', G2, 'Otros correos'), ('sq', GREEN, 'BillPay Intro (NewProducts)'), ('ln', INK, 'Clic de la semana'), ('ln', BLUE, 'Clic sin BillPay Intro')], 0, 10, 11)
X0, X1, Y0, Y1 = 46, 724, 80, 350
n = len(wks); st = (X1 - X0) / n; bw = st * 0.6; cx = lambda i: X0 + st * (i + 0.5)
VM, RM = 30, 1.5
vy = lambda v: Y1 - (Y1 - Y0) * v / VM; ry = lambda v: Y1 - (Y1 - Y0) * v / RM
S.t(X0 - 6, Y0 - 16, 'Millones de correos enviados', 11, SEC)
S.t(X1 + 6, Y0 - 16, 'Clic', 11, INK, 'end', 600)
for v in (0, 10, 20, 30):
    S.line(X0, vy(v), X1, vy(v)); S.t(X0 - 6, vy(v) + 4, f'{v}', 10.5, SEC, 'end'); S.t(X1 + 6, vy(v) + 4, f'{v / 20:.1f} %', 10.5, INK)
MES = {'04': 'abr', '05': 'may', '06': 'jun', '07': 'jul'}
for i, wk in enumerate(wks):
    tot = w.loc[wk, 'email_sent'] / 1e6; b = bi.envios / 1e6 if wk == B else 0
    S.rect(cx(i) - bw / 2, vy(tot - b), bw, vy(0) - vy(tot - b), G2)
    if b: S.rect(cx(i) - bw / 2, vy(tot), bw, vy(tot - b) - vy(tot) - 1.5, GREEN); S.t(cx(i), vy(tot) - 6, f'{share:.0f} % del correo de la semana', 10.5, GREEN, 'middle', 700, halo=True)
    S.t(cx(i), Y1 + 16, f'{int(wk[8:])} {MES[wk[5:7]]}', 10.5, INK if wk == B else TXT, 'middle', 700 if wk == B else 400)
# marca del reporte mensual
iR = wks.index('2026-07-06'); xr = cx(iR) - st / 2
S.line(xr, Y0 - 4, xr, Y1, SEC, 1)
S.t(xr + 5, Y0 + 8, 'Aquí el reporte mensual', 10.5, TXT, 'start', 600)
S.t(xr + 5, Y0 + 21, f'mostró junio: {cm["2026-06-01"]:.2f} %', 10.5, TXT)
S.poly([(cx(i), ry(sin[wk])) for i, wk in enumerate(wks)], BLUE, 2)
S.poly([(cx(i), ry(clic[wk])) for i, wk in enumerate(wks)], INK, 2.5)
for i, wk in enumerate(wks):
    S.circle(cx(i), ry(clic[wk]), 4, INK)
iB = wks.index(B)
S.circle(cx(iB), ry(sin[B]), 5, BLUE)
S.t(cx(iB) - 9, ry(sin[B]) - 8, f'Sin BillPay: {sin[B]:.2f} %', 11.5, BLUE, 'end', 700, halo=True)
S.t(cx(iB) + 9, ry(clic[B]) + 4, f'{clic[B]:.2f} %', 12, INK, 'start', 700, halo=True)
i8 = wks.index('2026-06-08'); S.t(cx(i8) + 2, ry(clic['2026-06-08']) - 10, f'{clic["2026-06-08"]:.2f} %', 11, INK, 'middle', 700, halo=True)
iM = wks.index('2026-05-25'); S.t(cx(iM) - 8, ry(clic['2026-05-25']) + 16, f'{clic["2026-05-25"]:.2f} %', 11, TXT, 'middle', 400, halo=True)

write(43, dict(kind='grafica', seccion='V. El ritmo lo marcan los lanzamientos, no el cliente',
 titulo='Un solo correo hundió la semana: con BillPay Intro el clic cayó a un tercio y a la semana siguiente volvió a lo normal',
 que='BillPay Intro: lanzamiento de BillPay (pago de servicios) por correo a toda la base. Promocional.',
 quien='NewProducts (en Others).',
 a_quien=f'{bi.envios/1e6:.1f} M personas, casi toda la base con correo, incluidas las que nunca habían respondido.',
 lecturas=[
  f'BillPay Intro salió el lunes 1 de junio: {share:.0f} % de los correos de esa semana, apertura {100*bi.email_open/bi.email_delivery:.1f} %, clic {100*bi.email_click/bi.email_delivery:.2f} % y {costo:.1f} M MXN de costo.',
  f'Semana del 1 de junio: {clic[B]:.2f} % de clic contra {clic["2026-06-08"]:.2f} % la siguiente; sin BillPay habría tenido {sin[B]:.2f} %. Sin ese correo, junio hizo {jun_sin:.2f} % de clic, igual o mejor que mayo ({cm["2026-05-01"]:.2f} %).',
  f'Medir por mes promedia el golpe y llega cuatro semanas tarde: junio cerró en {cm["2026-06-01"]:.2f} % y se leyó en julio, con los recordatorios de BillPay por push ya enviados. En push pasó igual: las semanas del 8 y 15 de junio abrieron {po["2026-06-08"]:.2f} % y {po["2026-06-15"]:.2f} %.',
 ],
 causa='No hay una lectura semanal por campaña ni una regla que frene un envío a toda la base cuando su primera semana no responde.',
 sowhat='Hace falta una lectura semanal por campaña: si un envío de más de 1 M de personas no llega a 3 clics por cada mil correos (o 7.5 aperturas por cada mil push) en su primera semana, se frena lo que sigue.',
 fuente='Fuente: Braze, E4a por semana y mes (correo) y E1 (BillPay Intro: envíos, entregados, aperturas y clics de junio), 2026. Supone que BillPay Intro salió completo la semana del 1 de junio (primer envío ese día). Clic sobre correos entregados; costo a 0.05 MXN por correo enviado. Junio sin BillPay Intro da 0.92 % (el guion decía 0.89 %) y mayo 0.86 % (decía 0.84 %).',
 svg=S.svg()))
