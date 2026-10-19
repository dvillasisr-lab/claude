"""Lámina 14 (ronda 2): franjas de puntos por canal: cada campaña (con 50 mil o más mensajes) por sus conversiones por cada mil
mensajes (escala por múltiplos), tamaño = mensajes; mediana y mitad central de cada canal; campañas nombradas."""
import math
from b2base import *

d = load_b()
fa = d.groupby(['fam', 'canal']).agg(env=('envios', 'sum'), cv=('conversiones_fraccional', 'sum'), team=('equipo', 'first')).reset_index()
fa = fa[fa.env >= 5e4].copy()
fa['y'] = 1000 * fa.cv / fa.env
st = fa.groupby('canal').y.describe(percentiles=[.25, .5, .75])
mix = d.groupby(['equipo', 'canal']).envios.sum().unstack().fillna(0)
mix = 100 * mix['in-app'] / mix.sum(axis=1)
i = d[d.canal == 'in-app']
print(st.round(2)); print('mix', mix.round(1).to_dict())
CH = [('email', 'Correo'), ('push notification', 'Push'), ('whatsapp', 'WhatsApp'), ('in-app', 'In-app')]
S = Svg('Cada punto es una campaña: conversiones por cada mil mensajes, por canal. La mediana de in-app es 15 y la de correo y push 1.8.')
S.circle(5, 14, 5, BLUE, ''); S.t(15, 18, 'Campaña de in-app', 11.5, INK, w=600)
S.circle(150, 14, 5, G1, ''); S.t(160, 18, 'Campaña de otro canal', 11.5, TXT)
S.rect(318, 8, 22, 12, '#E6ECFB'); S.line(329, 6, 329, 22, INK, 2)
S.t(346, 18, 'Mitad central de las campañas y mediana', 11.5, TXT)
S.t(0, 36, 'Tamaño: mensajes de la campaña. Campañas con 50 mil o más mensajes en nueve meses.', 10.5, SEC)
X0, X1 = 92, 640
LO, HI = math.log10(0.05), math.log10(100)
sx = lambda v: X0 + (X1 - X0) * (math.log10(min(max(v, 0.05), 100)) - LO) / (HI - LO)
Y0, RH = 64, 74
YB = Y0 + RH * 4
for v in (0.05, 0.1, 0.3, 1, 3, 10, 30, 100):
    S.line(sx(v), Y0 - 6, sx(v), YB - 6, GRID)
    S.t(sx(v), YB + 8, '0.05 o menos' if v == 0.05 else f'{v:g}', 11, SEC, 'middle')
S.t(X1, YB + 26, 'Conversiones por cada mil mensajes (escala que crece por múltiplos)', 11, SEC, 'end')
C1 = 778
S.t(C1, Y0 - 12, 'Mediana', 10.5, SEC, 'end')
rng = np.random.default_rng(3)
for k, (c, lab) in enumerate(CH):
    yc = Y0 + RH * k + RH / 2 - 6
    hi = c == 'in-app'
    S.t(X0 - 12, yc + 4, lab, 12, INK if hi else TXT, 'end', 700 if hi else 400)
    q1, md, q3 = st.loc[c, '25%'], st.loc[c, '50%'], st.loc[c, '75%']
    S.rect(sx(q1), yc - 22, sx(q3) - sx(q1), 44, '#E6ECFB' if hi else '#EEF0F3')
    g = fa[fa.canal == c].sort_values('env', ascending=False)
    for q in g.itertuples():
        S.circle(sx(q.y), yc + rng.uniform(-17, 17), 1.6 + 1.5 * math.sqrt(q.env / 1e6), BLUE if hi else G1,
                 ' fill-opacity="0.75" stroke="#FFFFFF" stroke-width="0.7"')
    S.line(sx(md), yc - 26, sx(md), yc + 26, INK, 2.2)
    S.t(C1, yc + 5, f'{md:.1f}', 13, BLUE if hi else INK, 'end', 700)
    S.t(C1, yc + 19, f'{len(g)} campañas', 10.5, SEC, 'end')
def name(key, c, txt, dy, an='start', dx=8):
    q = fa[(fa.canal == c) & fa.fam.str.contains(key, regex=False)].sort_values('env').iloc[-1]
    k = [x for x, _ in CH].index(c)
    yc = Y0 + RH * k + RH / 2 - 6
    S.t(sx(q.y) + dx, yc + dy, f'{txt}: {q.y:.1f}', 10.5, INK, an, 600, halo=True)
    print(txt, round(q.y, 1), round(q.env / 1e6, 2))
    return q
b_e = name('BillPay_Intro', 'email', 'Lanzamiento de BillPay', -24, 'start', 6)
b_i = name('BillPay_Intro', 'in-app', 'Lanzamiento de BillPay', 32, 'end', 0)
a_i = name('Active-Retargeting_Installments_SP', 'in-app', 'Recordatorio de Installments', -26, 'end', 0)
S.t(0, 410, f'Parte de sus mensajes que va por in-app: Marketing {mix["Marketing"]:.1f} %, Product Growth {mix["Product Growth"]:.1f} %, '
            f'Sales {mix["Sales"]:.1f} %, Others {mix["Others"]:.1f} %, Collections {mix["Collections"]:.1f} %.', 11, INK, w=600)
svg = S.done()
md = st['50%']
save(14, dict(
    kind='grafica',
    titulo=f'In-app trae {md["in-app"]/md["email"]:.0f} veces más conversiones por mensaje que el correo o el push, y casi no se usa',
    que='Referidos, lanzamientos, recordatorios de algo empezado y descuentos.',
    quien='Marketing y Product Growth hacen 79 % de las vistas, con 5 % de sus mensajes.',
    a_quien='Solo quien abre la app: sobre todo clientes activos y leads recientes.',
    lecturas=[
        f'Mediana por campaña: in-app {md["in-app"]:.1f} conversiones por cada mil mensajes; WhatsApp {md["whatsapp"]:.1f}, correo {md["email"]:.1f}, push {md["push notification"]:.1f}.',
        f'La peor campaña de in-app ({st.loc["in-app","min"]:.1f}) supera a la mitad de las de correo, push y WhatsApp.',
        f'Lanzamiento de BillPay: {b_i.y:.1f} por mil en in-app y {b_e.y:.1f} por correo. In-app solo llega a quien abre la app.',
    ],
    causa='In-app no es el canal de costumbre de ningún equipo y solo llega a quien abre la app; las campañas se arman para push y correo.',
    sowhat='Para quien usa la app, in-app primero y push de respaldo; quien no tiene la app, por correo.',
    fuente=f'{FUENTE_E1}. Mensajes: enviados o vistas de in-app. Conversión a 7 días repartida entre los mensajes del día; no prueba causa.',
    svg=svg,
))
