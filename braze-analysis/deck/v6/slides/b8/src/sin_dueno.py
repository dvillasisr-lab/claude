# Lámina 88: comunicaciones sin equipo dueño ni ticket (E2 team 'Not Tracked') cruzadas con E1 (2026).
# Uso: python3 sin_dueno.py  (imprime y devuelve la tabla por tema y por origen)
import re, pandas as pd
D = '/home/user/claude/braze-analysis/data/'
PRU = re.compile(r'(\bQA|^QA|QA_|test|prueba|copy ?of|copia|dummy|demo|^CONFIGURACION|^New (Canvas|Campaign))', re.I)
TRX = re.compile(r'(ControlGroupSplit|Mantenimiento|unlinked|debt_sale|Saldo a favor|^INC-|CCrejected|Research|Transaccional|Payment|Contract|Statement|disburs|Rechazo|Reembolso|^CR |Autopay|Subscription|Credit Balance|late_fees|Late Fees|failed|Cancellation|Rejection|Domic|account linked|Collections|CHARGEOFF|Respuesta|Desembols|Pago|Balance|Reminder ?Ecosystem|PaymentReminder|Contrato|Estado de cuenta|Cobranza|BKT)', re.I)
def tema(n):
    if PRU.search(n): return 'pruebas internas'
    if TRX.search(n): return 'transaccional y operativa'
    return 'promocional'
ORIG = [('NewProducts (BillPay, TopUps)', r'^NewProducts'), ('Shopping', r'^Shopping'), ('QA y pruebas', r'(^QA|test|copy of|prueba)'),
        ('Transaccional KPay', r'(^Transaccional|^CR |Payment|Autopay|Domic|Credit Balance|debit card)'), ('KCash (desembolso, rechazo)', r'(^KCash|Rechazo|Reembolso)')]
def origen(n):
    for lab, rx in ORIG:
        if re.search(rx, n, re.I): return lab
    return 'Otros sin dueño'
def datos():
    e = pd.read_csv(D + 'e2_catalogo.csv'); nt = e[e.team == 'Not Tracked']
    e1 = pd.read_csv(D + 'e1_comunicacion_mes_canal.csv'); e1['costo'] = e1.email_sent * 0.05 + e1.whatsapp_delivery * 1.0
    j = e1[e1.communication_id.isin(nt.communication_id)].copy(); j['communication_name'] = j.communication_name.astype(str)
    g = j.groupby(['communication_id', 'communication_name']).agg(env=('envios', 'sum'), c=('costo', 'sum')).reset_index()
    g = g[g.env > 0].copy(); g['tema'] = g.communication_name.map(tema); g['orig'] = g.communication_name.map(origen)
    tot = dict(nt=len(nt), sin_ticket=int((e.tiene_ticket == 0).sum()), activas=len(g), env=g.env.sum(), c=g.c.sum(), env_e1=e1.envios.sum(), c_e1=e1.costo.sum())
    return g, tot
if __name__ == '__main__':
    g, tot = datos(); print(tot, tot['env'] / tot['env_e1'])
    print(g.groupby('tema').agg(n=('env', 'size'), env=('env', 'sum'), c=('c', 'sum')).assign(env=lambda d: d.env / 1e6, c=lambda d: d.c / 1e6).round(2))
    print(pd.crosstab(g.orig, g.tema, values=g.env, aggfunc='sum').div(1e6).round(2))
    print(pd.crosstab(g.orig, g.tema))
    pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 90)
    for t in ['promocional', 'pruebas internas']:
        print(t); print(g[g.tema == t].sort_values('env', ascending=False).head(25)[['communication_name', 'env', 'orig']].to_string())
