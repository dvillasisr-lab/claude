"""Lámina 5a (oculta, de respaldo): las campañas que se llevan la mitad del gasto, una por fila.
Mismo universo y orden que la lámina 5 (E1 con base_p1, campañas que mandaron algo, de mayor a menor gasto)."""
import json, re
from comun import load, OUT, FUENTE_E1

d = load()
f = d.groupby('fam').agg(cost=('costo', 'sum'), conv=('conversiones_fraccional', 'sum'), sol=('solicitudes_filas', 'sum'),
                         env=('envios', 'sum'), equ=('equipo', 'first'))
f = f[f.env > 0].sort_values(['cost', 'env'], ascending=False)
f['cc'] = f.cost.cumsum() / f.cost.sum()
n50 = int((f.cc < 0.5).sum()) + 1
wa = d[d.canal == 'whatsapp'].groupby('fam').costo.sum()
top = f.iloc[:n50].copy()
top['wa'] = (wa.reindex(top.index).fillna(0) / top.cost).fillna(0)

NOM = {
    'Marketing-KCash-B0171-CANVAS-Leads_BBDDRezagada-NarrativaTasa0-N/A': 'Narrativa Tasa 0 a leads rezagados',
    'Marketing-KCash-B0171-CANVAS-Leads_BBDDRezagada-RescateTasa0-N/A': 'Rescate Tasa 0 a leads rezagados',
    'Lending-KCash-B0209-CANVAS-Recurrentes_Inactivos-DescuentoDirecto-N/A': 'Descuento directo a clientes inactivos',
    'Lending-KPay-B0333-CANVAS-Churn_12MesesInactividad-ConSinOferta-N/A': 'Ex clientes KPay con 12 meses sin uso',
    'Lending-KCash-B0211-CANVAS-Nuevos_RegistradosPay-Tasa0-N/A': 'Tasa 0 a registrados de KPay',
    'Marketing-KCash-B0326-Canvas-Leads-ReferralProgram-N/A': 'Referidos a leads',
    'Lending-KCash-B0223-CANVAS-Nuevos_NeverActive-InstallmentsNoCash-N/A': 'Installments a quien nunca activó',
    'Marketing-KCash-B0326-Canvas-Recurrentes_ClienteKCashCompraKCash-ReferralProgram-N/A': 'Referidos a clientes KCash',
    'Marketing-KCash-B0171-CANVAS-Leads-BBDDHotLeadsW1RescateTasa0-N/A': 'Rescate Tasa 0 a leads recientes',
    'Marketing-KCash-B0171-CANVAS-Leads_BBDDHotLeadsW1-RescateTasa0-N/A': 'Rescate Tasa 0 a leads recientes (otro nombre)',
    'Marketing-KPay-B0326-Canvas-Recurrentes_ClienteKPayCompraKPay-ReferralProgram-N/A': 'Referidos a clientes KPay',
    'Lending-KCash-B0301-CANVAS-Active-Retargeting_Installments_SP': 'Installments a clientes activos',
    'Marketing-KCash-B0326-Canvas-Recurrentes_Dormants-ReferralProgram-N/A': 'Referidos a ex clientes KCash',
    'NewProducts-Kueski-T0000-E-Portfolio_BillPay_Intro_Full_Rollout': 'Lanzamiento de BillPay a toda la base',
    'Marketing-KPay-B0326-Canvas-Recurrentes_Dormants-ReferralProgram-N/A': 'Referidos a ex clientes KPay',
    'Sales-KPay-B0368-CANVAS-Recurrentes-TemuFebrero-N/A': 'Temu en febrero a clientes KPay',
    'Lending-KPay-B0332-CANVAS-HardInactive_6MesesInactividad-ConSinOferta-N/A': 'Ex clientes KPay con 6 meses sin uso',
    'Collections-KCash-T000-CANVAS-BKT1-NA': 'Cobranza KCash, primeros días de atraso',
    'Compliance-Ecosistema-T2778-CANVAS-Recurrentes_InsigniaAdultosMayores-ComunicarMejoresPracticas-N/A': 'Buenas prácticas a adultos mayores',
    'Lending-KCash-B0337-CANVAS-Recurrentes_Eligibles-CuestaEnero-N/A': 'Cuesta de enero a clientes elegibles',
    'Lending-KCash-B0210-CANVAS-Nuevos_MPNeverCash-Tasa0-N/A': 'Tasa 0 a quien usa KPay y nunca usó Cash',
    'Marketing-KCash-B0000-CANVAS-Leads_LeftFunnel-Retargeting_Veriff': 'Verificar identidad a leads que no terminaron',
}
EQ = {'Others': 'Others', 'Collections': 'Others'}


def nombre(fam):
    if fam in NOM:
        return NOM[fam]
    p = fam.split('-')
    return ' '.join(p[-2:]).replace('_', ' ')


def ticket(fam):
    m = re.search(r'-([BT]\d{3,4})-', fam)
    return m.group(1) if m else ''


def n0(v):
    return f'{v:,.0f}'


TD = 'style="padding:.12cqi .6cqi .12cqi 0;white-space:nowrap"'
NUM = 'class="num" style="padding:.12cqi .6cqi .12cqi 0;white-space:nowrap"'
rows = []
for i, (fam, r) in enumerate(top.iterrows(), 1):
    eq = r.equ if r.equ in ('Marketing', 'Product Growth', 'Sales') else 'Others'
    cpc = n0(r.cost / r.conv) if r.conv >= 1 else 'sin dato'
    cps = n0(r.cost / r.sol) if r.sol >= 1 else 'sin dato'
    rows.append(f'<tr><td {NUM}>{i}</td><td {TD}><b>{nombre(fam)}</b></td><td {TD}><span style="color:#6B7484">{ticket(fam)}</span></td>'
                f'<td {TD}>{eq}</td><td {NUM}>{r.cost / 1e6:.2f}</td><td {NUM}>{r.cc * 100:.0f} %</td>'
                f'<td {NUM}>{r.wa * 100:.0f} %</td><td {NUM}>{r.env / 1e6:.1f}</td>'
                f'<td {NUM}>{n0(r.conv)}</td><td {NUM}>{cpc}</td><td {NUM}>{n0(r.sol)}</td><td {NUM}>{cps}</td></tr>')
T = top.sum(numeric_only=True)
rows.append(f'<tr style="border-top:1.5px solid #0B1220"><td {TD}></td><td {TD}><b>Las {n50} campañas</b></td><td {TD}></td><td {TD}></td>'
            f'<td {NUM}><b>{T.cost / 1e6:.2f}</b></td><td {NUM}><b>{top.cc.iloc[-1] * 100:.0f} %</b></td>'
            f'<td {NUM}><b>{wa.reindex(top.index).fillna(0).sum() / T.cost * 100:.0f} %</b></td><td {NUM}><b>{T.env / 1e6:.1f}</b></td>'
            f'<td {NUM}><b>{n0(T.conv)}</b></td><td {NUM}><b>{n0(T.cost / T.conv)}</b></td><td {NUM}><b>{n0(T.sol)}</b></td>'
            f'<td {NUM}><b>{n0(T.cost / T.sol)}</b></td></tr>')
TH = 'style="padding:.25cqi .6cqi .25cqi 0"'
THN = 'class="num" style="padding:.25cqi .6cqi .25cqi 0"'
head = (f'<tr><th {THN}>#</th><th {TH}>Campaña</th><th {TH}>Ticket</th><th {TH}>Equipo</th><th {THN}>Gasto 9 meses (M MXN)</th>'
        f'<th {THN}>Gasto acumulado</th><th {THN}>Gasto en WhatsApp</th><th {THN}>Mensajes (M)</th>'
        f'<th {THN}>Créditos otorgados</th><th {THN}>MXN por crédito</th><th {THN}>Solicitudes</th><th {THN}>MXN por solicitud</th></tr>')
html = f'<div style="width:91.6cqi;max-width:100%;overflow-x:auto"><table style="font-size:.84cqi;line-height:1.15">{head}{"".join(rows)}</table></div>'

eqs = top.assign(e=top.equ.where(top.equ.isin(['Marketing', 'Product Growth', 'Sales']), 'Others')).groupby('e').cost.sum().sort_values(ascending=False)
mk, pg = (top.equ == 'Marketing').sum(), (top.equ == 'Product Growth').sum()
out = dict(n=5, sub=1, oculta=True, kind='html', ancho_completo=True,
    titulo=f'Respaldo de la lámina 5: las {n50} campañas que se llevan la mitad del gasto en mensajes',
    sowhat=f'Marketing tiene {mk} de las {n50} y {eqs["Marketing"] / 1e6:.1f} de los {T.cost / 1e6:.1f} M MXN; las cuatro que más gastan van casi todo por WhatsApp.',
    fuente=('Fuente: Braze, E1, enero a septiembre 2026. Campaña = nombre sin fecha, todos sus canales. Crédito otorgado en 7 días, '
            'repartido; solicitudes sin repartir. WhatsApp 1.00 MXN por entregado, correo 0.05 MXN.'),
    html=html)
p = OUT / '005_1.json'
p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
print('escrito', p, n50, eqs.round(0).to_dict())
