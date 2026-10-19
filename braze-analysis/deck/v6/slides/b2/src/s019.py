"""Lámina 19: matriz equipo x canal con la parte del volumen de promoción en campañas que no llegan a lo mínimo aceptable
(y cuántas campañas son); a la derecha, el mismo corte por tema y por audiencia en barras 100 %."""
from b2base import *

d = load_b()
d = d[d.tipo == 'promocional']
fa = d.groupby(['fam', 'canal']).agg(b=('b', 'sum'), r=('r', 'sum'), env=('envios', 'sum'), costo=('costo', 'sum'), eq=('equipo', 'first'),
                                    gan=('gan', 'first'), aud=('aud', 'first'), last=('m', 'max')).reset_index()
fa['pct'] = 100 * fa.r / fa.b.replace(0, np.nan)
fa['bajo'] = fa.pct < fa.canal.map(MIN)
fa = fa[fa.b >= 5e4]
f = lambda g: pd.Series({'n': len(g), 'nb': g.bajo.sum(), 'pc': 100 * g.bajo.mean(), 'env': g.env.sum() / 1e6, 'envb': g[g.bajo].env.sum() / 1e6,
                         'pv': 100 * g[g.bajo].env.sum() / g.env.sum(), 'cb': g[g.bajo].costo.sum() / 1e6})
tot = f(fa)
ec = fa.groupby(['eq', 'canal']).apply(f)
eqs = fa.groupby('eq').apply(f)
chs = fa.groupby('canal').apply(f)
gn = fa.groupby('gan').apply(f)
au = fa.groupby('aud').apply(f)
sep = (fa.bajo & (fa['last'] == 9)).sum()
print('total', tot.round(1).to_dict(), 'sept', sep)
print(ec.round(1)); print(eqs.round(1)); print(chs.round(1)); print(gn.round(1)); print(au.round(1))
big = fa[fa.bajo].sort_values('env', ascending=False).head(6)
print(big[['fam', 'canal', 'eq', 'env', 'pct']].assign(env=lambda x: x.env / 1e6).round(2).to_string())

S = Svg('Matriz equipo por canal: parte del volumen de promoción en campañas que no llegan a lo mínimo aceptable y cuántas campañas son. '
        'A la derecha, el mismo corte por tema y por audiencia.')
S.t(0, 16, 'Parte del volumen de promoción en campañas que no llegan a lo mínimo aceptable', 12, INK, w=600)
S.t(0, 33, 'Mínimo: 3 clics por cada mil correos, 7.5 aperturas por cada mil push, 6 de cada 10 WhatsApp leídos, 1 de cada 10 in-app con clic.', 10.5, SEC)
CH = [('email', 'Correo'), ('push notification', 'Push'), ('whatsapp', 'WhatsApp'), ('in-app', 'In-app')]
EQ = ['Marketing', 'Product Growth', 'Sales', 'Others']
CX0, CW_, RH, Y0 = 128, 74, 56, 76
for j, (_, cl) in enumerate(CH + [('', 'Todos')]):
    S.t(CX0 + CW_ * j + CW_ / 2 + (8 if j == 4 else 0), Y0 - 10, cl, 11.5, INK, 'middle', 600)
def col(p):
    t = min(1, max(0, p / 85))
    a_, b_ = (0xF3, 0xF5, 0xF8), (0x1F, 0x4F, 0xD8)
    return '#%02X%02X%02X' % tuple(round(a_[k] + (b_[k] - a_[k]) * t) for k in range(3)), t > 0.5
def cell(x, y, g, bold=False):
    c_, dark = col(g.pv)
    S.rect(x, y + 1, CW_ - 2, RH - 2, c_)
    S.t(x + CW_ / 2 - 1, y + 24, f'{g.pv:.0f} %', 13, '#FFFFFF' if dark else INK, 'middle', 700)
    S.t(x + CW_ / 2 - 1, y + 40, f'{g.envb:.0f} de {g.env:.0f} M', 10.5, '#FFFFFF' if dark else TXT, 'middle')
for i, e_ in enumerate(EQ):
    y = Y0 + RH * i
    S.t(CX0 - 8, y + 26, e_, 11.5, INK, 'end', 600)
    S.t(CX0 - 8, y + 40, f'{int(eqs.loc[e_, "nb"])} de {int(eqs.loc[e_, "n"])} campañas', 10.5, SEC, 'end')
    for j, (c, _) in enumerate(CH):
        if (e_, c) in ec.index and ec.loc[(e_, c), 'env'] > 0.5:
            cell(CX0 + CW_ * j, y, ec.loc[(e_, c)])
        else:
            S.rect(CX0 + CW_ * j, y + 1, CW_ - 2, RH - 2, '#FFFFFF', f' stroke="{GRID}"')
            S.t(CX0 + CW_ * j + CW_ / 2 - 1, y + 32, 'poco', 10.5, SEC, 'middle')
    cell(CX0 + CW_ * 4 + 8, y, eqs.loc[e_])
y = Y0 + RH * 4 + 8
S.t(CX0 - 8, y + 26, 'Todos', 11.5, INK, 'end', 700)
S.t(CX0 - 8, y + 40, f'{int(tot.nb)} de {int(tot.n)} campañas', 10.5, SEC, 'end')
for j, (c, _) in enumerate(CH):
    cell(CX0 + CW_ * j, y, chs.loc[c])
cell(CX0 + CW_ * 4 + 8, y, tot)
S.rect(CX0 + CW_ * 4 + 7, y, CW_, RH, 'none', f' stroke="{INK}" stroke-width="1.5"')
S.t(0, 404, 'En cada celda: millones de mensajes en esas campañas de los millones del grupo.', 10.5, SEC)
# ===== derecha: por tema y audiencia
X0 = 528
S.line(X0 - 14, 46, X0 - 14, 404, GRID)
BX0, BX1 = X0 + 104, 742
TEM = [('lanzamiento', 'Lanzamientos'), ('tasa0', 'Tasa 0'), ('referidos', 'Referidos'), ('descuento', 'Descuentos'), ('recordatorio', 'Recordatorios')]
AUD = [('frios', 'Bases frías'), ('leads', 'Leads'), ('activos', 'Clientes activos')]
yy = 62
for head, lst, src in (('Por tema', TEM, gn), ('Por audiencia', AUD, au)):
    S.t(X0, yy, head, 10.5, SEC, w=600)
    yy += 12
    for k, lab in lst:
        g = src.loc[k]
        hi = g.pv >= 50
        S.t(BX0 - 8, yy + 13, lab, 11, INK if hi else TXT, 'end', 600 if hi else 400)
        wb = (BX1 - BX0) * g.pv / 100
        S.rect(BX0, yy + 2, wb - 1, 16, BLUE if hi else BLUE2)
        S.rect(BX0 + wb, yy + 2, (BX1 - BX0) - wb, 16, '#E9ECF1')
        S.t(BX1 + 6, yy + 14, f'{g.pv:.0f} %', 11, INK if hi else TXT, 'start', 700 if hi else 400)
        yy += 27
    yy += 10
S.line(BX0 + (BX1 - BX0) * 0.5, 70, BX0 + (BX1 - BX0) * 0.5, yy - 12, INK, 1, ' stroke-dasharray="3 3" opacity="0.5"')
S.t(BX0 + (BX1 - BX0) * 0.5, yy, 'mitad', 10.5, SEC, 'middle')
svg = S.done()
pg = big[big.fam.str.contains('Nuevos_RegistradosPay-Tasa0')].iloc[0]
bp = big[big.fam.str.contains('BillPay_Intro')].iloc[0]
save(19, dict(
    kind='grafica',
    titulo='Casi la mitad de los mensajes de promoción salen en campañas que no responden ni lo mínimo aceptable, y muchas siguen saliendo',
    que=f'Debajo del mínimo: lanzamientos ({gn.loc["lanzamiento","pv"]:.0f} % de su volumen), Tasa 0 ({gn.loc["tasa0","pv"]:.0f} %), referidos ({gn.loc["referidos","pv"]:.0f} %), descuentos ({gn.loc["descuento","pv"]:.0f} %). Recordatorios de algo que la persona empezó: solo {gn.loc["recordatorio","pv"]:.0f} %.',
    quien=f'Parte de su volumen de promoción debajo del mínimo: Others {eqs.loc["Others","pv"]:.0f} %, Product Growth {eqs.loc["Product Growth","pv"]:.0f} %, Marketing {eqs.loc["Marketing","pv"]:.0f} %, Sales {eqs.loc["Sales","pv"]:.0f} %. Collections no tiene promociones.',
    a_quien=f'Leads y bases frías: la mitad de sus campañas no llega al mínimo ({au.loc["leads","pv"]:.0f} % y {au.loc["frios","pv"]:.0f} % del volumen). Clientes activos: una de cada cuatro ({au.loc["activos","pv"]:.0f} %).',
    lecturas=[
        f'{int(tot.nb)} de {int(tot.n)} campañas de promoción por canal no llegan al mínimo: {tot.envb:.0f} M mensajes ({tot.pv:.0f} % del volumen) y {tot.cb:.1f} M MXN. {sep} seguían mandando en septiembre.',
        f'El correo es lo peor: {chs.loc["email","pc"]:.0f} % de sus campañas y {chs.loc["email","pv"]:.0f} % de su volumen. Push {chs.loc["push notification","pv"]:.0f} %, in-app {chs.loc["in-app","pv"]:.0f} % y WhatsApp {chs.loc["whatsapp","pv"]:.0f} % del volumen.',
        f'Lo más grande: Tasa 0 por correo a registrados sin crédito de Product Growth ({pg.env/1e6:.0f} M correos, {10*pg.pct:.1f} clics por cada mil) y el lanzamiento de BillPay por correo de Others ({bp.env/1e6:.0f} M correos, {10*bp.pct:.1f} clics por cada mil).',
    ],
    causa='Nadie mide cada campaña contra un mínimo común: una campaña sigue saliendo mes tras mes aunque casi nadie le responda.',
    sowhat='Revisar cada mes las campañas contra el mínimo: las que no llegan se rehacen o se quitan; si van a ex clientes, primero se prueba con un grupo sin mensajes.',
    fuente=f'{FUENTE_E1}. Universo: {int(tot.n)} campañas de promoción por canal (todas sus versiones) con 50 mil o más mensajes entregados o vistos en el periodo. Celdas con menos de 0.5 M mensajes: "poco". Gasto: WhatsApp a 1.00 MXN por entregado, email a 0.05 MXN por enviado.',
    svg=svg,
))
