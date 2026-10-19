"""Lámina 11: WhatsApp es 8 % de los mensajes y 71 % del gasto; dentro de WhatsApp, gasto por equipo y tema.
Izquierda: dos columnas 100 % (mensajes contra gasto) por canal. Derecha: barras apiladas de gasto de WhatsApp por equipo y tema."""
from b2base import *

d = load_b()
# ---- canal: parte de mensajes y de gasto
v = d.groupby('canal').envios.sum()
c = d.groupby('canal').costo.sum()
VT, CT = v.sum(), c.sum()
grp = {'whatsapp': 'WhatsApp', 'email': 'Email', 'push notification': 'Push e in-app', 'in-app': 'Push e in-app'}
vs = v.groupby(v.index.map(grp)).sum() / VT * 100
cs = c.groupby(c.index.map(grp)).sum() / CT * 100
cm = c.groupby(c.index.map(grp)).sum() / 1e6
# ---- WhatsApp por equipo y tema
w = d[d.canal == 'whatsapp']
TEMA = {'tasa0': 'Tasa 0', 'referidos': 'Referidos', 'descuento': 'Descuentos', 'recordatorio': 'Recordatorios',
        'otros': 'Otras ofertas de comercios', 'lanzamiento': 'Lanzamientos', 'xsell': 'Lanzamientos'}
w = w.assign(tema=w.gan.map(TEMA))
ct = pd.crosstab(w.equipo, w.tema, values=w.costo, aggfunc='sum').fillna(0) / 1e6
EQ = ['Marketing', 'Product Growth', 'Sales', 'Others']
ct = ct.loc[EQ]
WT = w.costo.sum() / 1e6
ve = d.groupby(['equipo', 'canal']).envios.sum().unstack().fillna(0)
ce = d.groupby(['equipo', 'canal']).costo.sum().unstack().fillna(0)
wa_msgs = 100 * ve.whatsapp / ve.sum(axis=1)
wa_cost = 100 * ce.whatsapp / ce.sum(axis=1)
tema_pct = 100 * w.groupby('tema').costo.sum() / w.costo.sum()
mkpg = ct.loc[['Marketing', 'Product Growth']].sum().sum()
au_ = w.groupby('aud').costo.sum() / 1e6
print('canal msgs %', vs.round(1).to_dict(), 'gasto %', cs.round(1).to_dict(), 'M MXN', cm.round(1).to_dict())
print(ct.round(2)); print('total WA', round(WT, 1), 'MK+PG', round(mkpg, 1), round(100 * mkpg / WT, 1))
print('WA en mensajes del equipo', wa_msgs.round(1).to_dict(), 'en gasto', wa_cost.round(1).to_dict())
print('tema %', tema_pct.round(1).to_dict())
print('frios', w[w.aud == 'frios'].costo.sum() / 1e6, 'activos', w[w.aud == 'activos'].costo.sum() / 1e6, 'leads', w[w.aud == 'leads'].costo.sum() / 1e6)

S = Svg('A la izquierda, parte de cada canal en los mensajes y en el gasto: WhatsApp es 8 % de los mensajes y 71 % del gasto. '
        'A la derecha, gasto de WhatsApp por equipo y tema, en millones de MXN.')
# ===== panel izquierdo
S.t(0, 16, 'Parte de cada canal, enero a septiembre', 12, INK, w=600)
Y0, Y1 = 66, 372
H = Y1 - Y0
cols = [('Mensajes', vs, f'{VT/1e6:.0f} M mensajes', 18), ('Gasto', cs, f'{CT/1e6:.1f} M MXN', 132)]
ORD = [('WhatsApp', BLUE), ('Email', G1), ('Push e in-app', G2)]
BW = 66
segs = {}
for name, s, tot, x in cols:
    S.t(x + BW / 2, Y0 - 24, name, 11.5, INK, 'middle', 600)
    S.t(x + BW / 2, Y0 - 9, tot, 11, SEC, 'middle')
    yy = Y0
    for lab, col in ORD:
        hh = H * s.get(lab, 0) / 100
        S.rect(x, yy, BW, hh - (1.5 if hh > 2 else 0), col)
        segs[(name, lab)] = (yy, yy + hh)
        yy += hh
# conectores de WhatsApp entre columnas
a0, a1 = segs[('Mensajes', 'WhatsApp')]
b0, b1 = segs[('Gasto', 'WhatsApp')]
S.raw(f'<path d="M{18+BW},{a0} L132,{b0} L132,{b1-1.5} L{18+BW},{a1-1.5} Z" fill="{BLUE}" opacity="0.12"/>')
# etiquetas
for name, s, tot, x in cols:
    for lab, col in ORD:
        y0, y1 = segs[(name, lab)]
        pct = s.get(lab, 0)
        if y1 - y0 >= 30:
            fill = '#FFFFFF' if col == BLUE else INK
            S.t(x + BW / 2, (y0 + y1) / 2 - 2, lab if lab != 'Push e in-app' else 'Push e', 11, fill, 'middle', 600)
            S.t(x + BW / 2, (y0 + y1) / 2 + 12, f'{pct:.0f} %' if lab != 'Push e in-app' else f'in-app {pct:.0f} %', 11, fill, 'middle')
        elif y1 - y0 >= 16:
            fill = '#FFFFFF' if col == BLUE else INK
            S.t(x + BW / 2, (y0 + y1) / 2 + 4, f'{pct:.0f} %', 11, fill, 'middle', 600)
S.t(132 + BW / 2, Y1 + 16, 'Push e in-app: 0 MXN', 10.5, SEC, 'middle')
S.t(132 + BW + 6, (b0 + b1) / 2 + 4, f'{cm["WhatsApp"]:.1f} M', 11, BLUE, 'start', 600)
S.t(132 + BW + 6, (b0 + b1) / 2 + 18, 'MXN', 11, BLUE, 'start', 600)
S.t(132 + BW + 6, (segs[('Gasto', 'Email')][0] + segs[('Gasto', 'Email')][1]) / 2 + 4, f'{cm["Email"]:.1f} M', 11, SEC)
S.t(132 + BW + 6, (segs[('Gasto', 'Email')][0] + segs[('Gasto', 'Email')][1]) / 2 + 18, 'MXN', 11, SEC)
S.line(256, 8, 256, 404, GRID)

# ===== panel derecho
X0 = 272
S.t(X0, 16, 'Gasto de WhatsApp por equipo y tema, millones de MXN', 12, INK, w=600)
TORD = [('Tasa 0', BLUE), ('Referidos', BLUE2), ('Descuentos', GREEN), ('Recordatorios', GREEN2),
        ('Otras ofertas de comercios', G1), ('Lanzamientos', G2)]
# leyenda en dos filas dentro del panel
lx, ly = X0, 34
for i, (lab, col) in enumerate(TORD):
    if i == 3:
        lx, ly = X0, 52
    S.rect(lx, ly - 9, 10, 10, col)
    txt = f'{lab} · {tema_pct[lab]:.0f} %'
    S.t(lx + 15, ly, txt, 11, TXT)
    lx += 15 + tw(txt, 11) + 10
BX0, BX1 = X0 + 104, 612
VMAX = 24
sx = lambda val: BX0 + (BX1 - BX0) * val / VMAX
for vv in (0, 5, 10, 15, 20):
    S.line(sx(vv), 82, sx(vv), 336, GRID)
    S.t(sx(vv), 350, f'{vv}', 10.5, SEC, 'middle')
S.t(BX1, 350, 'M MXN', 10.5, SEC, 'start')
RY = [92, 154, 216, 278]
BH = 28
for eq, y in zip(EQ, RY):
    hi = eq in ('Marketing', 'Product Growth')
    S.t(BX0 - 8, y + BH / 2 + 4, eq, 11.5, INK if hi else TXT, 'end', 600 if hi else 400)
    x = BX0
    for lab, col in TORD:
        val = ct.loc[eq].get(lab, 0)
        ww = sx(val) - BX0
        if ww <= 0:
            continue
        S.rect(x, y, ww - (1.5 if ww > 3 else 0), BH, col)
        if ww >= 30:
            S.t(x + ww / 2, y + BH / 2 + 4, f'{val:.1f}', 10.5, '#FFFFFF' if col in (BLUE, GREEN) else INK, 'middle', 600)
        x += ww
    tot = ct.loc[eq].sum()
    S.t(x + 6, y + BH / 2 + 4, f'{tot:.1f} M MXN · {100*tot/WT:.0f} %', 11.5, INK if hi else TXT, 'start', 600 if hi else 400)
    S.t(BX0, y + BH + 14, f'WhatsApp es {wa_msgs[eq]:.0f} % de sus mensajes y {wa_cost[eq]:.0f} % de su gasto', 10.5, SEC, halo=True)
# llave Marketing + Product Growth
S.line(X0 + 2, RY[0], X0 + 2, RY[1] + BH + 18, INK, 1.5)
S.line(X0 + 2, RY[0], X0 + 8, RY[0], INK, 1.5)
S.line(X0 + 2, RY[1] + BH + 18, X0 + 8, RY[1] + BH + 18, INK, 1.5)
S.t(X0, 378, f'Marketing y Product Growth: {mkpg:.1f} M MXN, {100*mkpg/WT:.0f} % del gasto de WhatsApp.', 11.5, INK, w=600)
S.t(X0, 396, f'El bloque más grande: Tasa 0 de Marketing, {ct.loc["Marketing","Tasa 0"]:.1f} M MXN, todo a leads.', 11, TXT)
svg = S.done()

save(11, dict(
    kind='grafica',
    titulo='Siete de cada diez pesos del gasto en mensajes se van en WhatsApp, y Marketing y Product Growth ponen casi todo en promociones',
    que='Casi solo promociones (99.5 % del gasto de WhatsApp): Tasa 0, ofertas de comercios de KPay, referidos y descuentos. Recordatorios de algo que la persona empezó: 5 %.',
    quien=f'Marketing {ct.loc["Marketing"].sum():.1f} M MXN, Product Growth {ct.loc["Product Growth"].sum():.1f} M MXN, Sales {ct.loc["Sales"].sum():.1f} M MXN y Others {ct.loc["Others"].sum():.1f} M MXN en nueve meses. Collections no usa WhatsApp.',
    a_quien=f'Ex clientes y leads que nunca activaron (bases frías) {au_["frios"]:.1f} M MXN, {100*au_["frios"]/WT:.0f} % del gasto de WhatsApp; clientes activos {au_["activos"]:.1f} M MXN ({100*au_["activos"]/WT:.0f} %); leads {au_["leads"]:.1f} M MXN ({100*au_["leads"]/WT:.0f} %).',
    lecturas=[
        f'Un WhatsApp entregado cuesta 1.00 MXN y un correo 0.05 MXN, veinte veces menos. Por eso WhatsApp es {vs["WhatsApp"]:.0f} % de los mensajes y {cs["WhatsApp"]:.0f} % del gasto: {WT:.1f} M de {CT/1e6:.1f} M MXN.',
        f'Marketing y Product Growth ponen {mkpg:.1f} M MXN, {100*mkpg/WT:.0f} % del gasto de WhatsApp. El bloque más grande es Tasa 0 de Marketing, {ct.loc["Marketing","Tasa 0"]:.1f} M MXN, todo a leads que no han pedido crédito.',
        f'En cada equipo WhatsApp es una parte chica de los mensajes y la mayor parte del gasto: en Marketing {wa_msgs["Marketing"]:.0f} % de sus mensajes y {wa_cost["Marketing"]:.0f} % de su gasto.',
    ],
    causa='Cada equipo manda por WhatsApp sus promociones más importantes porque es el canal que más se lee, sin un presupuesto con límite ni una regla de a quién vale la pena mandárselo.',
    sowhat='La pregunta no es si WhatsApp sirve, sino a quién se lo mandamos: con clientes activos paga, con ex clientes y leads viejos no (siguiente lámina).',
    fuente=f'{FUENTE_E1}. Gasto: WhatsApp a 1.00 MXN por entregado, email a 0.05 MXN por enviado, push e in-app sin costo; sin licencia de Braze. Tema y audiencia según el nombre de la campaña; lanzamientos incluye venta cruzada.',
    svg=svg,
))
