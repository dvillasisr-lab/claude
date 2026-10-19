"""Lámina 51 (ronda 2). Arriba: 3 cifras de bloqueados (E3, E7a). Gráfica: franja por equipo; cada punto es una campaña promocional
que mandó 10 mil o más mensajes a personas con la línea KPay congelada (E7a); x = esos mensajes (log); azul = ofrece KPay."""
import pandas as pd
from b5_svg import *
from b5_datos import a  # E7a con familia limpia, tipo, equipo y producto

B = D['bloq']; F = B['freeze']; RE = B['reus']; NE = B['negra']; E3 = D['e3']
p = a[(a.etapa == '4.Kpay CC Freeze') & (a.tipo == 'promocional o lifecycle')]
f = p.groupby(['familia', 'eq', 'prod']).envios.sum().reset_index()
f = f[f.envios >= 10000]
EQS = ['Marketing', 'Sales', 'Product Growth', 'Others']
S = Svg('Arriba, tres cifras de promociones a personas bloqueadas. Abajo, cada punto es una campaña que mandó promociones a personas con la línea KPay congelada, por equipo; azul si ofrece KPay.')
u = E3['4.Kpay CC Freeze']
kpis(S, [(f'{mil(u["u"])} mil', 'personas con KPay', 'congelado'),
          (f'{M(F["prod"]["kpay"])} M', 'promociones de KPay', 'les llegaron'),
          (f'{mil(RE["promo"])} mil', 'promociones a quien pidió', 'no recibir publicidad')])
S.t(0, 72, 'Promociones a personas con KPay congelado; cada punto es una campaña', 12, INK, w=600)
S.circle(W - 175, 68, 5, BLUE, '#FFFFFF', 1); S.t(W - 165, 72, 'Ofrece KPay', 11, TXT)
S.circle(W - 80, 68, 5, MARK, '#FFFFFF', 1); S.t(W - 70, 72, 'Otro', 11, TXT)
X0, X1 = 120, 640
sx = logx(10000, 3e6, X0, X1)
TOP, RH = 96, 64
for v, lab in [(1e4, '10 mil'), (1e5, '100 mil'), (1e6, '1 M'), (3e6, '3 M')]:
    S.line(sx(v), TOP - 8, sx(v), TOP + RH * 4 - 14); S.t(sx(v), TOP + RH * 4, lab, 10.5, SEC, 'middle')
S.t(W, TOP - 10, 'Total del equipo', 10.5, SEC, 'end')
NAMED = {'Marketing-KPay-B0326-Canvas-Recurrentes_Dormants-ReferralProgram-N/A': 'Referidos KPay a dormants',
         'Sales-KPay-B0335-CANVAS-Recurrentes_PortafolioActivoEInactivo-PromocionesMerchantsAmplificacion-N/A': 'Promos de comercios',
         'Lending-KPay-B0333-CANVAS-Churn_12MesesInactividad-ConSinOferta-N/A': 'Churn 12 meses',
         'Shopping-KPay-S0004-CAMPAIGN-WeeklyRecommendations': 'Recomendaciones semanales'}
for i, e in enumerate(EQS):
    yc = TOP + RH * i + 16
    d = f[f['eq'] == e].sort_values('envios')
    S.t(X0 - 10, yc + 4, e, 12, INK, 'end', 600)
    S.t(X0 - 10, yc + 18, f'{len(d)} campañas', 10.5, SEC, 'end')
    offs = swarm([sx(v) for v in d.envios], 3.4, 22)
    for q, o in zip(d.itertuples(), offs):
        S.circle(sx(q.envios), yc + o, 3.4, BLUE if q.prod == 'kpay' else MARK, '#FFFFFF', 0.8)
    m = med(list(d.envios))
    S.line(sx(m), yc - 17, sx(m), yc + 17, INK, 2.5)
    S.t(sx(m), yc - 20, f'mediana {mil(m)} mil', 10.5, INK, 'middle', 600, halo=True)
    kp = 100 * F['eq_prod'].get(f'{e}|kpay', 0) / F['eq'][e]
    S.t(W, yc + 2, f'{M(F["eq"][e])} M', 12, INK, 'end', 600); S.t(W, yc + 16, f'{kp:.0f} % de KPay', 10.5, SEC, 'end')
    for q in d.itertuples():
        if q.familia in NAMED:
            S.t(sx(q.envios), yc + 30, NAMED[q.familia], 10.5, INK, 'end' if q.envios > 1e6 else 'middle', 600, halo=True)
SVG = S.done()

ex_all = F['promo'] + RE['promo'] + NE['promo']
guarda(51, dict(
    kind='grafica',
    titulo='Le mandamos promociones a quien no puede comprar con KPay y a quien pidió no recibir publicidad',
    que='Descuentos, referidos, Comercio del día, Hot Sale y promociones de comercios',
    quien='Marketing, Sales y Product Growth; Others es Shopping, BillPay de NewProducts y QA',
    a_quien='Línea KPay congelada, REUS o ARCO (pidió no recibir publicidad) y lista negra',
    lecturas=[
        f'{M(F["promo"])} M promociones a personas con KPay congelado; {M(F["prod"]["kpay"])} M ofrecen justo KPay.',
        f'Referidos KPay a dormants (Marketing) mandó {M(f[f.familia.str.contains("KPay-B0326-Canvas-Recurrentes_Dormants")].envios.sum())} M; promos de comercios (Sales), {M(f[f.familia.str.contains("B0335")].envios.sum())} M.',
        f'REUS o ARCO: {mil(RE["promo"])} mil promociones, {mil(RE["canal"]["whatsapp"])} mil por WhatsApp; lista negra: {mil(NE["promo"])} mil.',
    ],
    causa='No hay exclusiones de cuenta en Braze: cada equipo arma su segmento y nadie quita a los bloqueados.',
    sowhat=f'Excluir una vez en Braze: quita {M(D["excl_min"])} M promociones sin tocar campañas; Riesgo decide KCash.',
    fuente=f'Fuente: Braze E7a (campaña, canal y etapa del golden dataset) y E3, enero a septiembre 2026. La etapa cubre 37 % de los envíos: es lo mínimo. Toda promoción a bloqueados: {M(ex_all)} M.',
    svg=SVG,
))
print(len(f), f.groupby('eq').size().to_dict())
