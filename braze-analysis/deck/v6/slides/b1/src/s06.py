"""Lámina 6: promociones contra avisos de servicio y cobranza. Franja de puntos: cada punto es una campaña (todas sus versiones)
con 100 mil o más entregados; panel de correo (clic) y de push (apertura) con la misma escala logarítmica; barra = promedio ponderado,
línea punteada = mediana. Tipo por la regla del Sheets (base_p1)."""
import zlib
import numpy as np
from comun import load, write, Svg, INK, TXT, SEC, GRID, BLUE, BLUE2, GREEN, GREEN2, G1, G2, FUENTE_E1

d = load()
TIP = [('promocional', 'Promoción', BLUE2, BLUE), ('transaccional', 'Aviso de servicio', GREEN2, GREEN), ('cobranza', 'Cobranza', G2, INK)]
CAN = [('email', 'Correo: clic de cada 100 correos entregados', 'email_delivery', 'email_click'),
       ('push notification', 'Push: apertura de cada 100 push enviados', 'pn_send', 'pn_open')]
NOM = {('email', 'Lending-KCash-B0211-CANVAS-Nuevos_RegistradosPay-Tasa0-N/A'): 'Tasa 0 a nuevos registrados',
       ('email', 'NewProducts-Kueski-T0000-E-Portfolio_BillPay_Intro_Full_Rollout'): 'Presentación de BillPay',
       ('email', 'Transaccional-KPay-Mail-Payment-Confirmation-20240821'): 'Confirmación de pago KPay',
       ('push notification', 'Marketing-KCash-B0391-CANVAS-Leads_BDDMarketing-RescateFinesDeSemana-N/A'): 'Rescate de fin de semana a leads',
       ('push notification', 'Payment Received - Push'): 'Pago recibido',
       ('push notification', 'Collections-KCash-T000-CANVAS-Precobranza-ecosystem'): 'Precobranza'}
t = d.groupby('tipo').agg(env=('envios', 'sum'), cost=('costo', 'sum'), conv=('conversiones_fraccional', 'sum'))
sh = t / t.sum()
P = {}
for c, _, b, r in CAN:
    g = d[d.canal == c].groupby(['fam', 'tipo']).agg(b=(b, 'sum'), r=(r, 'sum')).reset_index()
    g = g[g.b >= 100000].copy(); g['rr'] = 100 * g.r / g.b
    w = d[d.canal == c].groupby('tipo')[[b, r]].sum(); w = 100 * w[r] / w[b]
    P[c] = (g, w)
ratio = {c: P[c][1]['transaccional'] / P[c][1]['promocional'] for c in P}
print(sh.round(3), ratio, {c: P[c][0].groupby('tipo').rr.agg(['count', 'median']).round(2).to_dict() for c in P})

S = Svg('Respuesta de cada campaña por tipo de mensaje, correo y push, en escala logarítmica')
S.t(0, 14, 'Cada punto es una campaña con 100 mil o más entregados (tamaño = entregados).', 11, TXT)
S.rect(470, 4, 3, 13, INK); S.t(478, 14, 'promedio ponderado', 11, TXT)
S.line(600, 4, 600, 17, INK, 1.2, ' stroke-dasharray="2 2"'); S.t(606, 14, 'mediana', 11, TXT)
XL, XR = 132, 700
LO, HI = -2, np.log10(20)
xx = lambda v: XL + (XR - XL) * (np.log10(max(v, 0.01)) - LO) / (HI - LO)
ROWH = 47
y = 34
for c, ctit, _, _ in CAN:
    g, w = P[c]
    S.t(0, y + 12, ctit, 12, INK, 'start', 600)
    y0 = y + 22
    for i, (tk, tl, cp, cb) in enumerate(TIP):
        yc = y0 + i * ROWH + ROWH / 2
        S.line(XL, yc, XR, yc, GRID)
        gg = g[g.tipo == tk]
        S.t(XL - 10, yc - 1, tl, 11.5, INK if tk == 'promocional' else TXT, 'end', 600 if tk == 'promocional' else 400)
        S.t(XL - 10, yc + 12, f'{len(gg)} campañas', 10.5, SEC, 'end')
        for _, z in gg.sort_values('b', ascending=False).iterrows():
            j = (zlib.crc32(z.fam.encode()) % 1000) / 1000 - 0.5
            rad = 1.8 + 5.5 * np.sqrt(z.b / 35e6)
            S.o.append(f'<circle cx="{xx(z.rr):.1f}" cy="{yc + j * 22:.1f}" r="{rad:.1f}" fill="{cp}" fill-opacity="0.75" stroke="#fff" stroke-width="0.6"/>')
        med = gg.rr.median(); S.line(xx(med), yc - 15, xx(med), yc + 15, INK, 1.2, ' stroke-dasharray="2 2"')
        S.rect(xx(w[tk]) - 1.5, yc - 15, 3, 30, cb)
        S.t(XR + 8, yc + 4, f'{w[tk]:.2f} %', 12 if tk != 'cobranza' else 11.5, cb, 'start', 700)
        for (cc, fam), nm in NOM.items():
            if cc == c and fam in set(gg.fam):
                z = gg[gg.fam == fam].iloc[0]; px = xx(z.rr)
                anchor = 'end' if px > 560 else 'start'
                dy = -14
                if nm == 'Presentación de BillPay': anchor = 'end'
                S.t(px + (-8 if anchor == 'end' else 8), yc + dy, f'{nm} {z.rr:.2f} %' if z.rr < 1 else f'{nm} {z.rr:.1f} %', 10.5, INK, anchor, 600, halo=True)
    y = y0 + 3 * ROWH + 6
    for v, lab in ((0.01, '0.01 %'), (0.1, '0.1 %'), (1, '1 %'), (10, '10 %')):
        S.t(xx(v), y + 6, lab, 10.5, SEC, 'middle')
    y += 18
S.t(XR + 8, 30, 'Ponderado', 10.5, SEC, 'start', 600)

e = P['email'][1]; p = P['push notification'][1]
write(6, dict(kind='grafica',
    titulo='Las promociones responden casi cinco veces menos que los avisos por correo y push, y son casi todo el gasto',
    que='Promoción: Tasa 0, referidos, descuentos. Aviso: pago, contrato, desembolso.',
    quien='Promociones: Marketing y Product Growth. Avisos: Others. Cobranza: Collections.',
    a_quien='Promociones a leads, registrados y ex clientes; avisos a quien hizo algo.',
    lecturas=[
        f'Promociones: {sh.loc["promocional", "env"] * 100:.0f} % de los mensajes, {sh.loc["promocional", "cost"] * 100:.0f} % del gasto y {sh.loc["promocional", "conv"] * 100:.0f} % de las conversiones.',
        f'Correo: promoción {e["promocional"]:.2f} % de clic contra {e["transaccional"]:.2f} % del aviso. Push: {p["promocional"]:.2f} % contra {p["transaccional"]:.2f} %.',
        'Tasa 0 a nuevos registrados: 33 M correos con 0.28 % de clic, debajo de casi todos los avisos.'],
    causa='Las promociones salen a listas grandes sin que la persona haya hecho nada; el aviso sale porque pagó o firmó, y lo espera.',
    sowhat='La mejora está en las promociones; avisos y cobranza quedan fuera del límite de mensajes por persona.',
    fuente=f'{FUENTE_E1}. Tipo por regla del Sheets: Collections = cobranza; "Transaccional" o sin ticket = aviso; lo demás, promoción. Clic sobre entregados.',
    svg=S.done()))
