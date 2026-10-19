"""Lámina 12 (ronda 2): cada punto es una campaña de WhatsApp: gasto (x, escala por múltiplos) contra MXN por conversión
(y, escala por múltiplos), color por audiencia; líneas del costo promedio de clientes activos y de bases frías; campañas nombradas."""
import math
from b2base import *

d = load_b()
w = d[d.canal == 'whatsapp']
e = d[d.canal == 'email']
cpc = lambda g: g.costo.sum() / max(1, g.conversiones_fraccional.sum())
A = {a: cpc(w[w.aud == a]) for a in ('activos', 'leads', 'frios')}
fr = w[w.aud == 'frios']
ex = fr[fr.fam.str.contains('Dormant|Inactiv|Churn', case=False)]
eex = e[(e.aud == 'frios') & e.fam.str.contains('Dormant|Inactiv|Churn', case=False)]
fa = w.groupby('fam').agg(c=('costo', 'sum'), cv=('conversiones_fraccional', 'sum'), aud=('aud', 'first'), team=('equipo', 'first'),
                          s=('whatsapp_send', 'sum'), dl=('whatsapp_delivery', 'sum')).reset_index()
fa = fa[(fa.c >= 5e4) & (fa.cv >= 1)].copy()
fa['y'] = fa.c / fa.cv
fa['ent'] = 100 * fa.dl / fa.s
fa['a3'] = np.where(fa.aud.isin(['activos', 'frios']), fa.aud, 'otro')
print('A', A, 'n', len(fa), fa.c.sum() / w.costo.sum(), 'ex', cpc(ex), 'email ex', cpc(eex))
print(fa.groupby('a3').y.median().round(0).to_dict(), fa.groupby('a3').size().to_dict())
COL = {'activos': GREEN, 'frios': BLUE, 'otro': G2}
S = Svg('Cada punto es una campaña de WhatsApp: gasto contra MXN por conversión. Las de clientes activos cuestan 48 MXN por conversión '
        'en promedio y las de bases frías 629.')
lx = 0
for k, lab in (('frios', 'Bases frías (ex clientes y leads que nunca activaron)'), ('activos', 'Clientes activos'), ('otro', 'Leads y otros')):
    S.circle(lx + 5, 14, 5, COL[k], '')
    S.t(lx + 14, 18, lab, 11.5, INK if k != 'otro' else TXT, w=600 if k != 'otro' else 400)
    lx += 14 + tw(lab, 11.5, 600) + 18
X0, X1, Y0, Y1 = 56, 760, 50, 362
XL, XH = math.log10(0.05), math.log10(5)
YL, YH = math.log10(5), math.log10(12000)
sx = lambda v: X0 + (X1 - X0) * (math.log10(v) - XL) / (XH - XL)
sy = lambda v: Y1 - (Y1 - Y0) * (math.log10(min(max(v, 5), 12000)) - YL) / (YH - YL)
for v in (10, 30, 100, 300, 1000, 3000, 10000):
    S.line(X0, sy(v), X1, sy(v), GRID)
    S.t(X0 - 8, sy(v) + 4, f'{v:,}', 11, SEC, 'end')
for v in (0.05, 0.1, 0.3, 1, 3, 5):
    S.line(sx(v), Y1, sx(v), Y1 + 4, G1)
    S.t(sx(v), Y1 + 17, f'{v:g}', 11, SEC, 'middle')
S.t(X0 - 40, Y0 - 10, 'MXN por conversión', 11, SEC)
S.t(X1, Y1 + 34, 'Gasto de la campaña en nueve meses, M MXN (las dos escalas crecen por múltiplos)', 10.5, SEC, 'end')
for q in fa.sort_values('c', ascending=False).itertuples():
    r = 2.6 + 2.2 * math.sqrt(q.c / 1e6)
    S.circle(sx(q.c / 1e6), sy(q.y), r, COL[q.a3], ' fill-opacity="0.8" stroke="#FFFFFF" stroke-width="1"')
for k, lab in (('activos', 'Clientes activos'), ('frios', 'Bases frías')):
    y = sy(A[k])
    S.line(X0, y, X1, y, COL[k], 1.4, ' stroke-dasharray="5 4"')
    S.t(X0 + 6, y - 6, f'{lab}: {A[k]:.0f} MXN por conversión en promedio', 11.5, COL[k], 'start', 700, halo=True)
NAMES = [('ClienteKPayCompraKPay-ReferralProgram', 'Referidos a clientes KPay (Marketing)', 12, 14, 'start'),
         ('ClienteKCashCompraKCash-ReferralProgram', 'Referidos a clientes KCash (Marketing)', -12, 16, 'end'),
         ('Active-Retargeting_Installments_SP', 'Recordatorio de Installments (Product Growth)', -12, 16, 'end'),
         ('Leads_BBDDRezagada-RescateTasa0-N/A', 'Rescate Tasa 0 a rezagados (Marketing)', -12, -14, 'end'),
         ('Leads_BBDDRezagada-NarrativaTasa0-N/A', 'Tasa 0 a leads rezagados (Marketing)', -14, 22, 'end'),
         ('Churn_12MesesInactividad-ConSinOferta-N/A', 'Ex clientes de un año (Product Growth)', -12, -10, 'end'),
         ('Nuevos_NeverActive-InstallmentsNoCash', 'Registrados que nunca activaron (Product Growth)', -12, 4, 'end')]
for key, lab, dx, dy, an in NAMES:
    q = fa[fa.fam.str.contains(key, regex=False)].sort_values('c').iloc[-1]
    x, y = sx(q.c / 1e6), sy(q.y)
    S.line(x, y, x + dx * 0.7, y + dy * 0.6, INK, 0.7)
    S.t(x + dx, y + dy + 4, f'{lab}: {q.y:,.0f}', 11, INK, an, 600, halo=True)
    print(lab, round(q.c / 1e6, 2), round(q.y), round(q.ent))
svg = S.done()
e9 = pd.read_csv('/home/user/claude/braze-analysis/data/e9b_patron_respuesta_90d.csv')
wa90 = e9[e9.resp_wa == 0].msgs_wa_entregados.sum() / 1e6
save(12, dict(
    kind='grafica',
    titulo=f'WhatsApp paga con clientes activos y referidos; con bases frías cada conversión cuesta {A["frios"]/A["activos"]:.0f} veces más',
    que='Referidos y recordatorios a clientes; rescates de Tasa 0 y descuentos a bases frías.',
    quien='Marketing y Product Growth en las dos puntas; Sales solo a clientes y leads de KPay.',
    a_quien='Bases frías: ex clientes (dormants, inactivos, churn) y leads que nunca activaron.',
    lecturas=[
        f'{A["activos"]:.0f} MXN por conversión con clientes activos y {A["frios"]:.0f} con bases frías, donde se fueron {fr.costo.sum()/1e6:.1f} M MXN.',
        f'A ex clientes el correo recupera más barato: {cpc(eex):.0f} MXN por conversión contra {cpc(ex):.0f} por WhatsApp.',
        f'De julio a septiembre, {wa90:.1f} M MXN de WhatsApp llegaron a quien no leyó ninguno en 90 días.',
    ],
    causa='WhatsApp se usa para buscar en volumen a quien ya no lo lee: no hay regla de lectura reciente ni presupuesto con límite.',
    sowhat='A ex clientes, primero correo y app; WhatsApp solo a quien lo leyó en 90 días, con límite y grupo sin envío.',
    fuente=f'{FUENTE_E1}; E9b. {len(fa)} campañas con 50 mil MXN o más. Conversión a 7 días repartida entre los mensajes del día; no prueba causa.',
    svg=svg,
))
