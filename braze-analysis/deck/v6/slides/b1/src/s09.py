"""Lámina 9: junio. Pequeños múltiplos por canal con la serie semanal (E4a, 38 semanas completas): índice de volumen y de
respuesta, promedio de las 4 semanas de enero = 100. Misma escala en los cuatro paneles; semana pico nombrada."""
import numpy as np, pandas as pd
from comun import load, write, Svg, ROOT, INK, TXT, SEC, GRID, BLUE, G1, G2

e = pd.read_csv(ROOT / 'data/e4a_serie_semana_mes_canal.csv')
w = e[(e.grano == 'semana') & (e.periodo >= '2026-01-05') & (e.periodo <= '2026-09-21')].copy()
CAN = [('email', 'Correo', 'email_delivery', 'email_click'), ('push notification', 'Push', 'pn_send', 'pn_open'),
       ('whatsapp', 'WhatsApp', 'whatsapp_delivery', 'whatsapp_read'), ('in-app', 'In-app', 'in_app_impression', 'in_app_click')]
SEM = sorted(w.periodo.unique()); NW = len(SEM)
D = {}
for c, lab, b, r in CAN:
    x = w[w.canal == c].set_index('periodo').reindex(SEM)
    vol = x.envios; rr = x[r] / x[b]
    vi = 100 * vol / vol.iloc[:4].mean(); ri = 100 * rr / rr.iloc[:4].mean()
    jun = [i for i, s in enumerate(SEM) if s[5:7] == '06']
    D[c] = dict(vi=vi.values, ri=ri.values, vol=vol.values, pk=int(np.nanargmax(vi.values)), jv=np.nanmean(vi.values[jun]), jr=np.nanmean(ri.values[jun]))
# equipos y campañas de junio (E1 mensual)
d = load()
t = d.groupby(['m', 'equipo']).envios.sum().unstack().fillna(0) / 1e6
dif = t.loc[6] - t.loc[1]; tot = t.sum(axis=1)
bi = d[d.fam.str.contains('BillPay_Intro_Full_Rollout') & (d.canal == 'email')]
mk_push = (d[(d.equipo == 'Marketing') & (d.canal == 'push notification')].groupby('m').envios.sum() / 1e6)
print({c: (SEM[v['pk']], round(v['vi'][v['pk']]), round(v['ri'][v['pk']]), round(v['jv']), round(v['jr'])) for c, v in D.items()}, dif.round(1).to_dict(), tot[1], tot[6], bi.envios.sum() / 1e6, mk_push[1], mk_push[6])

S = Svg('Índice semanal de volumen y de respuesta por canal, enero = 100, del 5 de enero al 21 de septiembre de 2026')
S.line(0, 12, 20, 12, BLUE, 2.4); S.t(26, 16, 'Volumen de la semana', 11.5, TXT)
S.line(170, 12, 190, 12, G1, 2); S.t(196, 16, 'Respuesta de la semana (clic, apertura, lectura)', 11.5, TXT)
S.t(780, 16, 'Índice: promedio de enero = 100', 11, SEC, 'end')
PW, PH = 355, 150
POS = [(30, 40), (420, 40), (30, 238), (420, 238)]
YMAX = 350
mon = {'01': 'Ene', '03': 'Mar', '05': 'May', '07': 'Jul', '09': 'Sep'}
for (c, lab, _, _), (px, py) in zip(CAN, POS):
    v = D[c]; top, bot = py + 22, py + PH
    xx = lambda i: px + PW * i / (NW - 1)
    yy = lambda val: bot - (bot - top) * min(val, YMAX) / YMAX
    S.t(px, py + 10, lab, 12.5, INK, 'start', 700)
    for g in (0, 100, 200, 300):
        S.line(px, yy(g), px + PW, yy(g), GRID if g != 100 else G2, 1)
        if g: S.t(px - 5, yy(g) + 4, f'{g}', 10.5, SEC, 'end')
    # junio sombreado
    jun = [i for i, s in enumerate(SEM) if s[5:7] == '06']
    S.rect(xx(jun[0]) - 3, top, xx(jun[-1]) - xx(jun[0]) + 6, bot - top, '#E8EEFC')
    S.poly([(xx(i), yy(val)) for i, val in enumerate(v['ri'])], G1, 1.8)
    S.poly([(xx(i), yy(val)) for i, val in enumerate(v['vi'])], BLUE, 2.2)
    k = v['pk']; S.circle(xx(k), yy(v['vi'][k]), 4, BLUE)
    S.t(xx(k) + (6 if k < NW - 8 else -6), yy(v['vi'][k]) + 4, f'{v["vi"][k]:.0f}, semana del {int(SEM[k][8:10])} de {["", "ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep"][int(SEM[k][5:7])]}',
        10.5, BLUE, 'start' if k < NW - 8 else 'end', 700, halo=True)
    S.t(px + PW, py + 10, f'Junio: volumen {v["jv"]:.0f}, respuesta {v["jr"]:.0f}', 11, INK, 'end', 600)
    for i, s in enumerate(SEM):
        if s[8:10] <= '07' and s[5:7] in mon:
            S.t(xx(i), bot + 13, mon[s[5:7]], 10.5, SEC, 'middle')

write(9, dict(kind='grafica',
    titulo='Junio casi duplicó los mensajes de enero por BillPay y el push de Marketing, y hundió el clic y la apertura',
    que='Lanzamiento de BillPay y sus recordatorios; push de Mundial y Comercio del día.',
    quien=f'Marketing sumó {dif["Marketing"]:.0f} M mensajes y Others (BillPay) {dif["Others"]:.0f} M contra enero.',
    a_quien='Casi toda la base: varios push decían "Todos" en la audiencia.',
    lecturas=[
        f'Correo: la semana del 1 de junio llegó a {D["email"]["vi"][D["email"]["pk"]]:.0f} (enero = 100), con {bi.envios.sum() / 1e6:.0f} M correos de presentación de BillPay.',
        f'Push: Marketing pasó de {mk_push[1]:.1f} M push en enero a {mk_push[6]:.0f} M en junio; su respuesta en junio fue {D["push notification"]["jr"]:.0f}.',
        f'WhatsApp quedó en {D["whatsapp"]["jr"]:.0f} e in-app en {D["in-app"]["jr"]:.0f}: el golpe fue en correo y push, los canales que se saturaron.'],
    causa='No hay calendario común ni límite de mensajes por persona a la semana: tres equipos sumaron envíos a toda la base el mismo mes.',
    sowhat='Sin calendario ni límite semanal, un lanzamiento grande hunde la respuesta de correo y push.',
    fuente='Fuente: Braze, serie semanal por canal (E4a), 38 semanas completas del 5 de enero al 21 de septiembre 2026; equipos de E1. Respuesta: clic de correo y lectura de WhatsApp sobre entregados.',
    svg=S.done()))
