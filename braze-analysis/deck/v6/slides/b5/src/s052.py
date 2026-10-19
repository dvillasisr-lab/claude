"""Lámina 52 (ronda 2). Arriba: 3 cifras de correos después de la baja (E5b). Gráfica: franja por tipo y equipo; cada punto es una
campaña (Canvas con fecha) que mandó correos a gente ya dada de baja; x = correos después de la baja (log). Gris = cobranza y avisos,
que sí proceden; azul = promociones (Marketing en azul fuerte)."""
import re
import pandas as pd
from b5_svg import *

R = '/home/user/claude/braze-analysis/'
c = pd.read_csv(R + 'hallazgos/muestra_c_familias.csv'); tipo = c.groupby('familia').tipo.first()
b = pd.read_csv(R + 'data/e5b_comms_despues_baja.csv')
b['f'] = b.familia.map(lambda s: re.sub(r'-\d{8,9}-', '-', s)); b['tipo'] = b.f.map(tipo).fillna('?')
b['eq'] = b.equipo.replace({'Acquisition': 'Others'})
TOT = b.emails_despues_de_baja.sum(); TIP = b.groupby('tipo').emails_despues_de_baja.sum()
promo = TIP['promocional o lifecycle']; cob, tra = TIP['cobranza'], TIP['transaccional u operativa']
pb = b[b.tipo == 'promocional o lifecycle']; eqs = pb.groupby('eq').emails_despues_de_baja.sum()
ROWS = [('Cobranza', b[b.tipo == 'cobranza'], MARK), ('Avisos de pago y contratos', b[b.tipo == 'transaccional u operativa'], MARK),
        ('Promos de Marketing', pb[pb['eq'] == 'Marketing'], BLUE), ('Promos de Product Growth', pb[pb['eq'] == 'Product Growth'], BLUEL),
        ('Promos de Sales', pb[pb['eq'] == 'Sales'], BLUEL), ('Promos de Others', pb[pb['eq'] == 'Others'], BLUEL)]
S = Svg('Arriba, tres cifras de los correos que llegan después de darse de baja. Abajo, cada punto es una campaña: correos que mandó a gente ya dada de baja, por tipo de mensaje y equipo.')
kpis(S, [(f'{M(TOT, 2)} M', 'correos llegaron después', 'de darse de baja'),
         (f'{100*(cob+tra)/TOT:.0f} %', 'son cobranza y avisos:', 'esos sí proceden'),
         (f'{mil(promo)} mil', f'promociones; {mil(eqs["Marketing"])} mil', 'de Marketing')])
S.t(0, 72, 'Correos después de la baja; cada punto es una campaña', 12, INK, w=600)
X0, X1 = 170, 650
sx = logx(100, 300000, X0, X1)
TOP, RH = 96, 46
for v, lab in [(100, '100'), (1000, '1 mil'), (10000, '10 mil'), (100000, '100 mil')]:
    S.line(sx(v), TOP - 8, sx(v), TOP + RH * len(ROWS) - 14); S.t(sx(v), TOP + RH * len(ROWS), lab, 10.5, SEC, 'middle')
S.t(W, TOP - 10, 'Total', 10.5, SEC, 'end')
NAMED = {'B0171-CANVAS-Leads_BBDDRezagada-RescateTasa0': ('Rescate Tasa 0 a rezagados', 8, -9, 'start'), 'Retargeting_Veriff': ('Veriff, 9 meses seguidos', -8, 22, 'end'),
         'Portfolio_BillPay_Intro': ('Lanzamiento de BillPay', 8, -9, 'start'), 'B0211': ('Tasa 0 a registrados', 8, -9, 'start'), 'BKT1': ('Cobranza de atraso menor', -8, -9, 'end')}
done = set()
for i, (lab, d, col) in enumerate(ROWS):
    yc = TOP + RH * i + 12
    S.t(X0 - 10, yc + 4, lab, 11.5, INK, 'end', 600 if col == BLUE else 400)
    S.t(X0 - 10, yc + 18, f'{len(d)} campañas', 10.5, SEC, 'end')
    d = d.sort_values('emails_despues_de_baja')
    offs = swarm([sx(v) for v in d.emails_despues_de_baja], 3.6, 15)
    for q, o in zip(d.itertuples(), offs):
        S.circle(sx(q.emails_despues_de_baja), yc + o, 3.6, col, '#FFFFFF', 0.8)
    tot = d.emails_despues_de_baja.sum()
    S.t(W, yc + 4, f'{tot/1e3:,.0f} mil', 12, INK, 'end', 600)
    for q in d.sort_values('emails_despues_de_baja', ascending=False).itertuples():
        for k, n in NAMED.items():
            if k in q.f and k not in done:
                done.add(k); nm, dx, dy, an = n
                S.t(sx(q.emails_despues_de_baja) + dx, yc + dy, nm, 10.5, INK, an, 600, halo=True)
SVG = S.done()

guarda(52, dict(
    kind='grafica',
    titulo='A quien se dio de baja le siguen llegando promociones de Tasa 0 y referidos, casi todas de Marketing',
    que='Correo promocional: Tasa 0, newsletters, referidos, cupones y recordatorio de registro',
    quien=f'Marketing ({mil(eqs["Marketing"])} de {mil(promo)} mil), Product Growth, Sales y Others',
    a_quien=f'{mil(pb.usuarios_aprox.sum())} mil personas que ya se habían dado de baja del correo',
    lecturas=[
        f'{100*(cob+tra)/TOT:.0f} % de lo que llega tras la baja es cobranza y avisos de pago: eso sí procede.',
        f'{mil(promo)} mil promociones; la mayor, rescate con Tasa 0 a leads rezagados (Marketing), {pb[pb.f.str.contains("Leads_BBDDRezagada-RescateTasa0")].emails_despues_de_baja.sum()/1e3:.1f} mil.',
        'El recordatorio de Veriff siguió llegando nueve meses seguidos a quien ya se había dado de baja.',
    ],
    causa='El filtro de suscripción está en la entrada del Canvas y no en cada paso de correo (lo más probable).',
    sowhat='Ajuste de configuración, no de negocio: filtro de suscripción en cada paso de correo, en una semana.',
    fuente='Fuente: Braze E5b (correos después de la baja), enero a septiembre 2026; tipo de mensaje del catálogo de campañas (muestra C). Cada punto es un Canvas con su fecha.',
    svg=SVG,
))
print(len(b), {lab: len(d) for lab, d, _ in ROWS})
