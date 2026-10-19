"""Lámina 11a (oculta, de respaldo): las campañas de WhatsApp que se llevan la mitad del gasto de WhatsApp, una por fila.
Mismo universo y orden que la lámina 11 (load_b, solo canal WhatsApp, de mayor a menor gasto)."""
import json, re
from b2base import load_b, OUTDIR as OUT

d = load_b()
w = d[d.canal == 'whatsapp']
fa = w.groupby('fam').agg(c=('costo', 'sum'), equ=('equipo', 'first'), aud=('aud', 'first'), ent=('whatsapp_delivery', 'sum'),
                          leido=('whatsapp_read', 'sum'), conv=('conversiones_fraccional', 'sum'),
                          sol=('solicitudes_filas', 'sum')).sort_values('c', ascending=False)
fa['cum'] = fa.c.cumsum() / fa.c.sum()
N50 = int((fa.cum < 0.5).sum()) + 1
top = fa.iloc[:N50]

NOM = {
    'Marketing-KCash-B0171-CANVAS-Leads_BBDDRezagada-NarrativaTasa0-N/A': 'Narrativa Tasa 0 a leads rezagados',
    'Marketing-KCash-B0171-CANVAS-Leads_BBDDRezagada-RescateTasa0-N/A': 'Rescate Tasa 0 a leads rezagados',
    'Lending-KPay-B0333-CANVAS-Churn_12MesesInactividad-ConSinOferta-N/A': 'Ex clientes KPay con 12 meses sin uso',
    'Marketing-KCash-B0326-Canvas-Recurrentes_ClienteKCashCompraKCash-ReferralProgram-N/A': 'Referidos a clientes KCash',
    'Lending-KCash-B0209-CANVAS-Recurrentes_Inactivos-DescuentoDirecto-N/A': 'Descuento directo a clientes inactivos',
    'Marketing-KCash-B0171-CANVAS-Leads-BBDDHotLeadsW1RescateTasa0-N/A': 'Rescate Tasa 0 a leads recientes',
    'Marketing-KCash-B0326-Canvas-Leads-ReferralProgram-N/A': 'Referidos a leads',
    'Marketing-KCash-B0171-CANVAS-Leads_BBDDHotLeadsW1-RescateTasa0-N/A': 'Rescate Tasa 0 a leads recientes (otro nombre)',
    'Marketing-KPay-B0326-Canvas-Recurrentes_ClienteKPayCompraKPay-ReferralProgram-N/A': 'Referidos a clientes KPay',
    'Lending-KCash-B0223-CANVAS-Nuevos_NeverActive-InstallmentsNoCash-N/A': 'Installments a quien nunca activó',
    'Lending-KCash-B0301-CANVAS-Active-Retargeting_Installments_SP': 'Installments a clientes activos',
    'Sales-KPay-B0368-CANVAS-Recurrentes-TemuFebrero-N/A': 'Temu en febrero a clientes KPay',
    'Marketing-KCash-B0326-Canvas-Recurrentes_Dormants-ReferralProgram-N/A': 'Referidos a ex clientes KCash',
    'Lending-KPay-B0332-CANVAS-HardInactive_6MesesInactividad-ConSinOferta-N/A': 'Ex clientes KPay con 6 meses sin uso',
    'Marketing-KPay-B0252-CANVAS-Recurrentes-LanzamientoPalaciodeHierro-N/A': 'Palacio de Hierro a clientes KPay',
}
AUD = {'frios': 'Base fría', 'activos': 'Clientes activos', 'leads': 'Leads'}


def nombre(fam):
    return NOM.get(fam, ' '.join(fam.split('-')[-2:]).replace('_', ' '))


def ticket(fam):
    m = re.search(r'-([BT]\d{3,4})-', fam)
    return m.group(1) if m else ''


def n0(v):
    return f'{v:,.0f}'


TD = 'style="padding:.16cqi .6cqi .16cqi 0;white-space:nowrap"'
NUM = 'class="num" style="padding:.16cqi .6cqi .16cqi 0;white-space:nowrap"'
rows = []
for i, (fam, r) in enumerate(top.iterrows(), 1):
    eq = r.equ if r.equ in ('Marketing', 'Product Growth', 'Sales') else 'Others'
    cpc = n0(r.c / r.conv) if r.conv >= 1 else 'sin dato'
    cps = n0(r.c / r.sol) if r.sol >= 1 else 'sin dato'
    rows.append(f'<tr><td {NUM}>{i}</td><td {TD}><b>{nombre(fam)}</b></td><td {TD}><span style="color:#6B7484">{ticket(fam)}</span></td>'
                f'<td {TD}>{eq}</td><td {TD}>{AUD.get(r.aud, "Otros")}</td><td {NUM}>{r.c / 1e6:.2f}</td><td {NUM}>{r.cum * 100:.0f} %</td>'
                f'<td {NUM}>{100 * r.leido / r.ent:.0f}</td>'
                f'<td {NUM}>{n0(r.conv)}</td><td {NUM}>{cpc}</td><td {NUM}>{n0(r.sol)}</td><td {NUM}>{cps}</td></tr>')
T = top.sum(numeric_only=True)
B = 'style="padding:.16cqi .6cqi .16cqi 0;white-space:nowrap;border-top:1.5px solid #0B1220"'
BN = 'class="num" style="padding:.16cqi .6cqi .16cqi 0;white-space:nowrap;border-top:1.5px solid #0B1220"'
rows.append(f'<tr><td {B}></td><td {B}><b>Las {N50} campañas</b></td><td {B}></td><td {B}></td><td {B}></td>'
            f'<td {BN}><b>{T.c / 1e6:.2f}</b></td><td {BN}><b>{top.cum.iloc[-1] * 100:.0f} %</b></td>'
            f'<td {BN}><b>{100 * T.leido / T.ent:.0f}</b></td>'
            f'<td {BN}><b>{n0(T.conv)}</b></td><td {BN}><b>{n0(T.c / T.conv)}</b></td><td {BN}><b>{n0(T.sol)}</b></td>'
            f'<td {BN}><b>{n0(T.c / T.sol)}</b></td></tr>')
TH = 'style="padding:.25cqi .6cqi .25cqi 0"'
THN = 'class="num" style="padding:.25cqi .6cqi .25cqi 0"'
head = (f'<tr><th {THN}>#</th><th {TH}>Campaña</th><th {TH}>Ticket</th><th {TH}>Equipo</th><th {TH}>A quién</th>'
        f'<th {THN}>Gasto WhatsApp = M entregados (M MXN)</th><th {THN}>Gasto acumulado</th>'
        f'<th {THN}>Leídos de cada 100</th><th {THN}>Créditos otorgados</th><th {THN}>MXN por crédito</th>'
        f'<th {THN}>Solicitudes</th><th {THN}>MXN por solicitud</th></tr>')
html = f'<div style="width:91.6cqi;max-width:100%;overflow-x:auto"><table style="font-size:.9cqi;line-height:1.2">{head}{"".join(rows)}</table></div>'

fr = top[top.aud == 'frios']
out = dict(n=11, sub=1, oculta=True, kind='html', ancho_completo=True,
    titulo=f'Respaldo de la lámina 11: las {N50} campañas que se llevan la mitad del gasto de WhatsApp',
    sowhat=(f'{len(fr)} de las {N50} van a bases frías: {fr.c.sum() / 1e6:.1f} M MXN a {n0(fr.c.sum() / fr.conv.sum())} MXN por crédito; '
            f'a activos sale en {n0(top[top.aud == "activos"].c.sum() / top[top.aud == "activos"].conv.sum())} MXN.'),
    fuente=('Fuente: Braze, E1, enero a septiembre 2026, solo WhatsApp. Campaña = nombre sin fecha. 1.00 MXN por entregado. '
            'Crédito otorgado en 7 días, repartido; solicitudes sin repartir.'),
    html=html)
p = OUT / '011_1.json'
p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
print('escrito', p, N50, out['sowhat'])
