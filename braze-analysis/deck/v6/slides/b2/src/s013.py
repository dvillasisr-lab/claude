"""Lámina 13 (ronda 2): mancuernas por campaña de Cash que manda por WhatsApp y por correo: MXN por conversión en cada canal.
Las 20 campañas con más gasto de WhatsApp; en las 50 que usan los dos canales, WhatsApp sale más caro en todas."""
import math
from b2base import *

d = load_b()
c = d[d.product_service == 'Cash']
cpc = lambda g: g.costo.sum() / max(1, g.conversiones_fraccional.sum())
w, e = c[c.canal == 'whatsapp'], c[c.canal == 'email']
TOT = dict(wa=cpc(w), em=cpc(e))
g = c[c.canal.isin(['whatsapp', 'email'])].groupby(['fam', 'canal']).agg(env=('envios', 'sum'), cost=('costo', 'sum'),
                                                                          cv=('conversiones_fraccional', 'sum'), team=('equipo', 'first')).reset_index()
g = g[(g.env >= 3e4) & (g.cv >= 3)]
g['y'] = g.cost / g.cv
p = g.pivot(index='fam', columns='canal', values='y').dropna()
p['r'] = p.whatsapp / p.email
p['cw'] = g[g.canal == 'whatsapp'].set_index('fam').cost.reindex(p.index)
p['team'] = g.drop_duplicates('fam').set_index('fam').team.reindex(p.index)
p = p.sort_values('cw', ascending=False)
NB, NW = len(p), int((p.r > 1).sum())
share = p.cw.sum() / w.costo.sum()
print('total', TOT, TOT['wa'] / TOT['em'], 'campañas', NB, NW, 'mediana', p.r.median(), 'gasto cubierto', share)
NAME = {
    'Leads_BBDDRezagada-NarrativaTasa0-N/A': 'Tasa 0 a leads rezagados',
    'Leads_BBDDRezagada-RescateTasa0-N/A': 'Rescate Tasa 0 a leads rezagados',
    'Recurrentes_ClienteKCashCompraKCash-ReferralProgram': 'Referidos a clientes de KCash',
    'Recurrentes_Inactivos-DescuentoDirecto': 'Descuento a clientes inactivos',
    'Leads-BBDDHotLeadsW1RescateTasa0': 'Rescate Tasa 0 a leads recientes, semana 1',
    'Canvas-Leads-ReferralProgram-N/A': 'Referidos a leads',
    'Leads_BBDDHotLeadsW1-RescateTasa0': 'Rescate Tasa 0 a leads recientes, semana 1 (v2)',
    'Nuevos_NeverActive-InstallmentsNoCash': 'Registrados que nunca activaron',
    'B0301-CANVAS-Active-Retargeting_Installments_SP': 'Recordatorio de Installments a activos',
    'Recurrentes_Dormants-ReferralProgram': 'Referidos a ex clientes',
    'Leads-BBDDHotLeadsW2RescateTasa0': 'Rescate Tasa 0 a leads recientes, semana 2',
    'Nuevos_MPNeverCash-Tasa0-N/A': 'Tasa 0 a registrados sin préstamo',
    'Active-RecurrentesRetargeting_Installments': 'Recordatorio de Installments a recurrentes',
    'Leads_1erLoanKCash-ReferralProgram': 'Referidos tras el primer préstamo',
    'Leads_Todos-ReferralProgram': 'Referidos a todos los leads',
    'Recurrentes_Eligibles-CuestaEnero': 'Cuesta de enero a clientes elegibles',
    'SeQuedanStepOffering': 'Quien se quedó en la oferta',
    'Marketing-KCash-B0301-CANVAS-Active-NuevosRetargeting': 'Recordatorio de Installments a nuevos',
    'Leads_BBDDRezagada-Tasa0-N/A': 'Tasa 0 a leads rezagados (v2)',
    'Leads_BBDDHotLeadsW2-RescateTasa0': 'Rescate Tasa 0 a leads recientes, semana 2 (v2)',
}
def nm(f):
    for k, v in NAME.items():
        if k in f:
            return v
    return None
top = p.head(20).copy()
top['nm'] = [nm(f) for f in top.index]
assert top.nm.notna().all(), top[top.nm.isna()].index.tolist()
print(top[['nm', 'whatsapp', 'email', 'r', 'cw', 'team']].round(1).to_string())

S = Svg(f'Mancuernas: MXN por conversión de Cash por WhatsApp y por correo en las 20 campañas con más gasto de WhatsApp que usan los dos canales; '
        f'WhatsApp cuesta más en las {NW} de {NB}.')
S.circle(5, 14, 5.5, BLUE, ''); S.t(15, 18, 'WhatsApp', 11.5, INK, w=600)
S.circle(95, 14, 5.5, GREEN, ''); S.t(105, 18, 'Correo', 11.5, INK, w=600)
S.t(170, 18, 'MXN por conversión de Cash en la misma campaña (escala que crece por múltiplos)', 11, SEC)
NX, X0, X1 = 258, 270, 628
LO, HI = math.log10(1), math.log10(10000)
sx = lambda v: X0 + (X1 - X0) * (math.log10(min(max(v, 1), 10000)) - LO) / (HI - LO)
C1, C2 = 690, 778
Y0, RH = 56, 15.2
S.t(C1, Y0 - 8, 'WhatsApp / correo', 10.5, SEC, 'end')
S.t(C2, Y0 - 8, 'Gasto WhatsApp', 10.5, SEC, 'end')
YB = Y0 + RH * len(top)
for v in (1, 10, 100, 1000, 10000):
    S.line(sx(v), Y0 - 2, sx(v), YB, GRID)
    S.t(sx(v), YB + 14, f'{v:,}', 10.5, SEC, 'middle')
COLT = {'Marketing': INK, 'Product Growth': INK}
for i, (f, q) in enumerate(top.iterrows()):
    y = Y0 + RH * i + RH / 2
    S.t(NX, y + 3.8, q.nm, 10.5, INK if q.team == 'Marketing' else TXT, 'end')
    S.line(sx(q.email), y, sx(q.whatsapp), y, G2, 2.5)
    S.circle(sx(q.email), y, 4.2, GREEN, ' stroke="#FFFFFF" stroke-width="1.2"')
    S.circle(sx(q.whatsapp), y, 4.2, BLUE, ' stroke="#FFFFFF" stroke-width="1.2"')
    S.t(C1, y + 3.8, f'{q.r:.1f} veces', 10.5, INK, 'end', 600 if q.r >= 5 else 400)
    S.t(C2, y + 3.8, f'{q.cw/1e6:.2f} M MXN', 10.5, TXT, 'end')
S.t(0, YB + 14, 'Negro: Marketing. Gris: Product Growth.', 10.5, SEC)
S.t(0, YB + 34, f'En las {NB} campañas de Cash que usan los dos canales, WhatsApp sale más caro en {NW}; la mitad, más de {p.r.median():.0f} veces.',
    11.5, BLUE, 'start', 700)
svg = S.done()
save(13, dict(
    kind='grafica',
    titulo=f'En la misma campaña de Cash, la conversión por WhatsApp cuesta más que por correo en {NW} de {NB}',
    que='Tasa 0, referidos, descuentos y recordatorios de Cash (préstamo personal).',
    quien='Marketing pone 73 % del WhatsApp de Cash y Product Growth 27 %.',
    a_quien='Leads rezagados y recientes, ex clientes, registrados sin préstamo y clientes activos.',
    lecturas=[
        f'Todo Cash: {TOT["wa"]:.0f} MXN por conversión en WhatsApp y {TOT["em"]:.0f} en correo, {TOT["wa"]/TOT["em"]:.1f} veces.',
        f'Campaña por campaña la mitad cuesta más de {p.r.median():.0f} veces; Tasa 0 a rezagados: {top.iloc[0].whatsapp:.0f} contra {top.iloc[0].email:.0f} MXN.',
        f'El recordatorio de Installments a activos: {top[top.nm.str.startswith("Recordatorio de Installments a activos")].iloc[0].r:.0f} veces; ahí el correo basta.',
    ],
    causa='WhatsApp es el canal por defecto para Cash aun con quien responde al correo; nadie compara costo por conversión entre canales.',
    sowhat='Para Cash, primero correo, push e in-app; WhatsApp solo donde esos no llegan o el préstamo lo paga.',
    fuente=f'{FUENTE_E1}; producto Cash. Campañas con 30 mil o más mensajes en cada canal. Conversión a 7 días repartida; no prueba causa.',
    svg=svg,
))
