"""Lámina 9: junio. Izquierda: millones de mensajes por mes y equipo (Marketing y Others resaltados).
Derecha: pequeños múltiplos de respuesta por canal y mes, con enero y junio marcados. E1 con base_p1."""
from comun import load, write, Svg, INK, TXT, SEC, GRID, BLUE, GREEN, G2, MES, FUENTE_E1

d = load()
t = d.groupby(['m', 'equipo']).envios.sum().unstack().fillna(0) / 1e6
t['Resto'] = t[['Product Growth', 'Sales', 'Collections']].sum(axis=1)
dif = t.loc[6] - t.loc[1]; tot = t[['Marketing', 'Others', 'Resto']].sum(axis=1)
mk = d[d.equipo == 'Marketing'].groupby(['m', 'canal']).envios.sum().unstack().fillna(0) / 1e6
bp = d[d.fam.str.contains('billpay', case=False) & (d.m == 6)].envios.sum() / 1e6
bi = d[d.fam.str.contains('BillPay_Intro_Full_Rollout') & (d.canal == 'email')].agg({'email_click': 'sum', 'email_delivery': 'sum', 'usuarios_aprox': 'sum', 'envios': 'sum'})
bi_clic = 1000 * bi.email_click / bi.email_delivery
import pandas as pd
from comun import ROOT
e4 = pd.read_csv(ROOT / 'data/e4a_serie_semana_mes_canal.csv'); e4 = e4[(e4.grano == 'mes') & (e4.canal == 'email')]
bu = e4.set_index(e4.periodo.str[5:7].astype(int)).bajas_email_usuarios
RC = {'email': ('email_delivery', 'email_click', 1000, 'Correo: clics por cada mil'), 'push notification': ('pn_send', 'pn_open', 1000, 'Push: aperturas por cada mil'),
      'whatsapp': ('whatsapp_delivery', 'whatsapp_read', 100, 'WhatsApp: leídos de cada 100'), 'in-app': ('in_app_impression', 'in_app_click', 100, 'In-app: clics de cada 100 vistas')}
rr = {}
for c, (b, r, k, _) in RC.items():
    g = d.groupby('m')[[b, r]].sum(); rr[c] = k * g[r] / g[b]
baj = d.groupby('m').email_unsubscribe.sum()
f = d.groupby(['fam', 'canal', 'equipo', 'm']).envios.sum().unstack().fillna(0); f['dif'] = (f[6] - f[1]) / 1e6
topc = f.sort_values('dif', ascending=False).head(6)
print(t.round(1), dif.round(1).to_dict(), tot.round(1).to_dict(), (mk.loc[6] - mk.loc[1]).round(1).to_dict(), bp, {c: v.round(2).to_dict() for c, v in rr.items()}, baj.to_dict(), topc.dif.round(2))

S = Svg('Millones de mensajes por mes y equipo, y respuesta por canal y mes, enero a septiembre 2026')
SER = [('Marketing', 'Marketing', BLUE), ('Others', 'Others (BillPay y avisos)', GREEN), ('Resto', 'Product Growth, Sales y Collections', G2)]  # Marketing abajo
lx = 0
for k, lab, col in SER:
    S.rect(lx, 12, 10, 10, col); S.t(lx + 15, 21, lab, 11.5, TXT); lx += 15 + len(lab) * 6.2 + 16
X0, X1, Y0, Y1 = 46, 470, 70, 366
step = (X1 - X0) / 9; bw = step * 0.62
cx = lambda i: X0 + step * (i + 0.5)
VMAX = 120
vy = lambda v: Y1 - (Y1 - Y0) * v / VMAX
S.t(X0 - 6, Y0 - 16, 'Millones de mensajes', 11, SEC)
for v in (0, 40, 80, 120):
    S.line(X0, vy(v), X1, vy(v), GRID); S.t(X0 - 6, vy(v) + 4, f'{v} M', 11, SEC, 'end')
for i in range(9):
    m = i + 1; base = 0; hi = m in (1, 6)
    for k, lab, col in SER:
        v = t.loc[m, k]; S.rect(cx(i) - bw / 2, vy(base + v), bw, max(0, vy(base) - vy(base + v) - 1.5), col); base += v
    S.t(cx(i), vy(base) - 6, f'{base:.0f} M', 12 if hi else 11, INK if hi else SEC, 'middle', 700 if hi else 400)
    S.t(cx(i), Y1 + 17, MES[i], 11.5, INK if hi else TXT, 'middle', 600 if hi else 400)
# anotaciones de junio
j = 5; bm = t.loc[6, 'Resto']
bm = 0
ya = vy(tot[6]) - 24
S.t(cx(j) - 6, ya, f'Marketing {dif["Marketing"]:.0f} M más', 11.5, BLUE, 'end', 700, halo=True)
S.t(cx(j) + 6, ya, f'Others {dif["Others"]:.0f} M más', 11.5, GREEN, 'start', 700, halo=True)
S.t(cx(j), ya - 15, 'Junio contra enero:', 10.5, SEC, 'middle', halo=True)
# pequeños múltiplos
PX0, PX1 = 540, 760
S.line(512, Y0 - 20, 512, Y1 + 20, GRID)
S.t(PX0 - 14, Y0 - 16, 'Respuesta por canal', 11.5, INK, 'start', 600)
H = 66; gap = 8
for n, (c, (_, _, k, lab)) in enumerate(RC.items()):
    top = Y0 + n * (H + gap) + 2
    S.t(PX0 - 14, top + 6, lab, 11, TXT, 'start', 600)
    ser = rr[c]; lo, hi_ = ser.min(), ser.max(); pad = (hi_ - lo) * 0.15
    yy = lambda v: top + H - 8 - (H - 30) * (v - lo + pad) / (hi_ - lo + 2 * pad)
    xx = lambda i: PX0 + (PX1 - PX0) * i / 8
    S.line(PX0, top + H - 4, PX1, top + H - 4, GRID)
    S.poly([(xx(i), yy(ser[i + 1])) for i in range(9)], G2 if False else '#A3AAB5', 1.8)
    for i in (0, 5):
        S.circle(xx(i), yy(ser[i + 1]), 4.5 if i == 5 else 4, BLUE if i == 5 else INK)
        val = f'{ser[i + 1]:.1f}'
        S.t(xx(i) + (7 if i == 0 else 0), yy(ser[i + 1]) - 8 if i == 5 else yy(ser[i + 1]) - 7, val, 11, BLUE if i == 5 else INK, 'start' if i == 0 else 'middle', 700, halo=True)
    S.circle(xx(8), yy(ser[9]), 3.5, '#A3AAB5')
    S.t(xx(8), yy(ser[9]) - 8, f'{ser[9]:.1f}', 10.5, SEC, 'end', 400, halo=True)
S.t(PX0, Y1 + 17, 'Ene', 11, TXT, 'middle'); S.t(PX0 + (PX1 - PX0) * 5 / 8, Y1 + 17, 'Jun', 11, BLUE, 'middle', 600); S.t(PX1, Y1 + 17, 'Sep', 11, TXT, 'middle')

write(9, dict(kind='grafica',
    titulo=f'Junio casi duplicó los mensajes de enero por BillPay y los push de Marketing, y la respuesta cayó en los cuatro canales',
    que=f'El lanzamiento de BillPay (pago de servicios) y sus recordatorios: {bp:.0f} M mensajes en junio. Push nuevos de Marketing: Mundial, Comercio del día y el lanzamiento de BillPay en la app.',
    quien=(f'De los {tot[6] - tot[1]:.0f} M mensajes de más contra enero: Marketing {dif["Marketing"]:.0f} M ({mk.loc[6, "push notification"] - mk.loc[1, "push notification"]:.0f} M de push) y Others {dif["Others"]:.0f} M. '
           f'Collections sumó {dif["Collections"]:.0f} M; Product Growth mandó {-dif["Product Growth"]:.0f} M menos y Sales {-dif["Sales"]:.0f} M menos.'),
    a_quien=f'A casi toda la base: el correo de presentación de BillPay llegó a {bi.usuarios_aprox / 1e6:.0f} M personas y varios push decían "Todos" en la audiencia.',
    lecturas=[
        f'Junio mandó {tot[6]:.0f} M mensajes contra {tot[1]:.0f} M en enero. Marketing pasó de {t.loc[1, "Marketing"]:.0f} M a {t.loc[6, "Marketing"]:.0f} M y Others de {t.loc[1, "Others"]:.0f} M a {t.loc[6, "Others"]:.0f} M.',
        f'En junio, contra enero: correo de {rr["email"][1]:.1f} a {rr["email"][6]:.1f} clics por cada mil; push de {rr["push notification"][1]:.1f} a {rr["push notification"][6]:.1f} aperturas por cada mil; WhatsApp de {rr["whatsapp"][1]:.0f} a {rr["whatsapp"][6]:.0f} leídos de cada 100. Solo el push de septiembre superó a enero.',
        f'El correo de presentación de BillPay fue a {bi.envios / 1e6:.0f} M correos con {bi_clic:.0f} clic por cada mil. En junio se dieron de baja del correo {bu[6] / 1e3:.0f} mil personas; enero tuvo más ({bu[1] / 1e3:.0f} mil).'],
    causa='No hay un calendario común entre equipos ni un límite de mensajes por persona a la semana: tres equipos sumaron envíos a casi toda la base el mismo mes y nadie veía el total.',
    sowhat='Sin calendario común ni límite semanal, un lanzamiento grande arrastra la respuesta de todos los canales.',
    fuente=(f'{FUENTE_E1}. Respuesta: clics de correo por cada mil entregados, aperturas de push por cada mil enviados, WhatsApp leídos de cada 100 entregados (incluye lecturas registradas el mes siguiente) '
            'y clics in-app de cada 100 vistas. Bajas = personas que se dieron de baja del correo en el mes (E4a). Others = BillPay de NewProducts, avisos de KPay y KCash, recomendaciones de Shopping y pruebas de QA.'),
    svg=S.done()))
