"""Lámina 50 (ronda 2). Arriba: 3 cifras del WhatsApp a bases frías. Gráfica: cada punto es una campaña de WhatsApp (50 mil o más
entregados, más de 5 conversiones); x = WhatsApp entregados (log), y = MXN por conversión del mismo día (log); azul = ex clientes y
leads que nunca activaron; líneas = mediana de cada lado (E1). WhatsApp a 1.00 MXN por entregado."""
import pandas as pd
from b5_svg import *

GC = D['gc']; T = D['tot']
t = pd.read_csv(H / 'b5_camp.csv')
w = t[(t.canal == 'whatsapp') & (t.base >= 50000) & (t.conv > 5)].copy()
w['fr'] = w.g.isin(['ex', 'nunca'])
wa_fr = GC['ex|whatsapp']['costo'] + GC['nunca|whatsapp']['costo']
conv_fr = GC['ex|whatsapp']['conv'] + GC['nunca|whatsapp']['conv']
mf, mr = med(list(w[w.fr].mxn_conv)), med(list(w[~w.fr].mxn_conv))
ma = med(list(w[w.g == 'activos'].mxn_conv))
# MXN por solicitud registrada (no viene repartida); campaña sin solicitudes = costo infinito por solicitud
w['ms'] = w.mxn_sol.fillna(float('inf'))
sf, sa = med(list(w[w.fr].ms)), med(list(w[w.g == 'activos'].ms))
S = Svg('Arriba, tres cifras del WhatsApp a ex clientes y leads que nunca activaron. Abajo, cada punto es una campaña de WhatsApp: mensajes entregados contra pesos por conversión, con la mediana de cada grupo.')
kpis(S, [(f'{100*wa_fr/T["wa"]:.0f} %', 'del gasto de WhatsApp va', 'a ex clientes y leads fríos'),
          (f'{M(wa_fr)} M', 'MXN en nueve meses,', 'por mensaje entregado'),
          (f'{100*conv_fr/T["conv"]:.1f} %', 'de las conversiones', 'sale de ahí')])

S.t(0, 72, 'MXN por conversión; cada punto es una campaña de WhatsApp', 12, INK, w=600)
S.circle(W - 320, 68, 5, BLUE, '#FFFFFF', 1); S.t(W - 310, 72, 'Ex clientes y nunca activaron', 11, TXT)
S.circle(W - 138, 68, 5, GREEN, '#FFFFFF', 1); S.t(W - 128, 72, 'Activos', 11, TXT)
S.circle(W - 68, 68, 5, MARK, '#FFFFFF', 1); S.t(W - 58, 72, 'Resto', 11, TXT)
X0, X1, Y0, Y1 = 50, 760, 90, 372
sx = logx(50000, 20e6, X0, X1); sy = logx(10, 10000, Y1, Y0)
for v in (10, 100, 1000, 10000):
    S.line(X0, sy(v), X1, sy(v)); S.t(X0 - 6, sy(v) + 4, fmt(v), 10.5, SEC, 'end')
for v, lab in [(1e5, '100 mil'), (1e6, '1 M'), (1e7, '10 M')]:
    S.line(sx(v), Y0, sx(v), Y1); S.t(sx(v), Y1 + 15, lab, 10.5, SEC, 'middle')
S.t(X1, Y1 + 30, 'WhatsApp entregados por campaña (escala log)', 10.5, SEC, 'end')
for q in w.sort_values('fr').itertuples():
    S.circle(sx(q.base), sy(q.mxn_conv), 4.5 if q.fr else 3.5, BLUE if q.fr else (GREEN if q.g == 'activos' else MARK), '#FFFFFF', 1)
for m_, col, lab, dy in [(mf, BLUE, f'Mediana ex clientes y nunca activaron: {fmt(mf)} MXN', -6), (ma, GREEN, f'Mediana activos: {fmt(ma)} MXN', 14)]:
    S.line(X0, sy(m_), X1, sy(m_), col, 1.5)
    S.t(X0 + 4, sy(m_) + dy, lab, 11, INK, w=600, halo=True)
NAMED = {('Marketing-KCash-B0171-CANVAS-Leads_BBDDRezagada-RescateTasa0-N/A'): (-8, -8, 'end'),
         ('Lending-KPay-B0333-CANVAS-Churn_12MesesInactividad-ConSinOferta-N/A'): (8, -6, 'start'),
         ('Lending-KCash-B0209-CANVAS-Recurrentes_Inactivos-DescuentoDirecto-N/A'): (8, 14, 'start'),
         ('Lending-KCash-B0223-CANVAS-Nuevos_NeverActive-InstallmentsNoCash-N/A'): (8, 4, 'start'),
         ('Marketing-KCash-B0171-CANVAS-Leads_BBDDRezagada-NarrativaTasa0-N/A'): (8, 14, 'start')}
for q in w.itertuples():
    if q.familia in NAMED:
        dx, dy, an = NAMED[q.familia]
        S.t(sx(q.base) + dx, sy(q.mxn_conv) + dy, f'{nombre(q.familia)}: {fmt(q.mxn_conv)}', 10.5, INK, an, 600, halo=True)
top_act = w[w.g == 'activos'].sort_values('base', ascending=False).iloc[0]
S.t(sx(top_act.base) + 8, sy(top_act.mxn_conv) + 14, f'{nombre(top_act.familia)}: {fmt(top_act.mxn_conv)}', 10.5, INK, 'start', 600, halo=True)
SVG = S.done()

guarda(50, dict(
    kind='grafica',
    titulo='Casi la mitad del WhatsApp se gasta en recuperar a quien ya no nos usa, donde cada conversión cuesta más',
    que='Rescate con Tasa 0, "con o sin oferta", descuento a inactivos y referidos a dormants',
    quien='Marketing (rescate Tasa 0 a leads) y Product Growth (inactivos y churn)',
    a_quien='Ex clientes que dejaron KCash o KPay y leads que se registraron y nunca tomaron crédito',
    lecturas=[
        f'Mediana por campaña: {fmt(mf)} MXN por conversión en bases frías y {fmt(ma)} en activos; {sf:.0f} y {sa:.0f} por solicitud.',
        f'Rescate Tasa 0 a rezagados (Marketing): {M(w[w.familia == "Marketing-KCash-B0171-CANVAS-Leads_BBDDRezagada-RescateTasa0-N/A"].base.sum())} M WhatsApp entregados a {fmt(w[w.familia=="Marketing-KCash-B0171-CANVAS-Leads_BBDDRezagada-RescateTasa0-N/A"].mxn_conv.iloc[0])} MXN por conversión.',
        f'Ex clientes: {GC["ex|email"]["mxn_conv"]:.0f} MXN por conversión por correo contra {GC["ex|whatsapp"]["mxn_conv"]:.0f} por WhatsApp; {GC["ex|email"]["mxn_sol"]:.0f} contra {GC["ex|whatsapp"]["mxn_sol"]:.0f} por solicitud.',
    ],
    causa='WhatsApp es lo que más se lee y se usa para insistir; en bases frías la lectura casi no se vuelve préstamo.',
    sowhat='WhatsApp para recuperar solo a quien leyó uno en 90 días; al resto, correo, push o in-app.',
    fuente='Fuente: Braze E1 (campaña, canal y mes), ene a sep 2026. WhatsApp a 1.00 MXN por entregado. Solicitud: solicitudes registradas. Campañas con 50 mil o más entregados. Ex clientes sin Sales B0335 (promos a todo el portafolio).',
    svg=SVG,
))
print(mf, mr, ma, sf, sa, len(w), w.fr.sum())
