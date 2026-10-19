"""Lámina 62: respuesta por tema y canal (E1, promocionales; tema por el nombre con la regla de la muestra G). Filas = tema, columnas =
millones de correos, clic del correo, apertura del push y clic del in-app; dos campañas de ejemplo por tema."""
from comun import *

e = load_e1()
e['gg'] = e.communication_name.map(gan_g)
p = e[~e.grupo.isin(['cobranza', 'transaccional'])]
T = [('recordatorio', 'Recordatorio de algo empezado'), ('tasa0', 'Tasa 0'), ('descuento', 'Descuentos y cupones'), ('referidos', 'Referidos'), ('lanzamiento', 'Lanzamientos y boletines')]
CH = [('email', 'Clic del correo'), ('push notification', 'Apertura del push'), ('in-app', 'Clic del in-app')]
MIN = {'email': 0.3, 'push notification': 0.75, 'in-app': 10}
val = {(g, c): resp(p[(p.gg == g) & (p.canal == c)], c) for g, _ in T for c, _ in CH}
vol = {g: p[(p.gg == g) & (p.canal == 'email')].envios.sum() / 1e6 for g, _ in T}
def fr(f, c):
    x = e[(e.familia == f) & (e.canal == c)]; return resp(x, c)
EX = {'recordatorio': [('Verificar identidad (Marketing)', 'Marketing-KCash-B0000-CANVAS-Leads_LeftFunnel-Retargeting_Veriff'),
                       ('Pagar compra a meses (Product Growth)', 'Lending-KCash-B0301-CANVAS-Active-Retargeting_Installments_SP')],
      'tasa0': [('Tasa 0 a registrados sin crédito (B0211)', 'Lending-KCash-B0211-CANVAS-Nuevos_RegistradosPay-Tasa0-N/A')],
      'descuento': [('Descuento a inactivos (B0209)', 'Lending-KCash-B0209-CANVAS-Recurrentes_Inactivos-DescuentoDirecto-N/A'),
                    ('Cuponera de Sales a leads (B0392)', None)],
      'referidos': [('Referidos a leads (B0326)', 'Marketing-KCash-B0326-Canvas-Leads-ReferralProgram-N/A'),
                    ('Referidos a dormants (B0326)', 'Marketing-KCash-B0326-Canvas-Recurrentes_Dormants-ReferralProgram-N/A')],
      'lanzamiento': [('Lanzamiento de BillPay a toda la base', 'NewProducts-Kueski-T0000-E-Portfolio_BillPay_Intro_Full_Rollout')]}
b392 = e[e.familia.str.contains('Sales-KPay-B0392-CANVAS-Leads-Cuponera') & (e.canal == 'email')]
exs = {}
for g, lst in EX.items():
    out = []
    for lab, f in lst:
        if f is None: out.append((lab, resp(b392, 'email'), None)); continue
        out.append((lab, fr(f, 'email'), fr(f, 'push notification') if e[(e.familia == f) & (e.canal == 'push notification')].pn_send.sum() > 1e5 else None))
    exs[g] = out
print({k: round(v, 2) for k, v in val.items()}, vol, exs)

s = SVG('Respuesta por tema del mensaje: millones de correos, clic del correo, apertura del push y clic del in-app; recordatorio de algo empezado contra ofertas nuevas')
COLS = [(232, 330, 'Correos enviados', 'M', 60), (352, 480, 'Clic del correo', '%', 3.4), (502, 630, 'Apertura del push', '%', 2.5), (652, 772, 'Clic del in-app', '%', 65)]
for x0, x1, h, u, mx in COLS:
    s.t(x0, 16, h, 12, INK, w=600)
    s.t(x0, 31, 'millones, enero a septiembre' if u == 'M' else 'por cada 100 enviados', 10.5, SEC)
TOP, RH = 62, 64
for i, (g, name) in enumerate(T):
    y = TOP + RH * i; col = GREEN if g == 'recordatorio' else M1
    s.t(0, y + 12, name, 12, INK, w=600)
    for j, (lab, em, pu) in enumerate(exs[g][:2]):
        txt = f'{lab}: correo {em:.2f} %' + (f', push {pu:.1f} %' if pu is not None and pu >= 1 else (f', push {pu:.2f} %' if pu is not None else ''))
        s.t(0, y + 28 + 13 * j, txt, 10.5, SEC)
    s.line(0, y + RH - 10, 780, y + RH - 10, GRID)
    for k, (x0, x1, h, u, mx) in enumerate(COLS):
        v = vol[g] if k == 0 else val[(g, CH[k - 1][0])]
        w = (x1 - x0 - 34) * v / mx
        s.rect(x0, y + 2, w, 14, col)
        s.t(x0 + w + 5, y + 13, f'{v:.0f} M' if k == 0 else (f'{v:.1f} %' if v >= 1 else f'{v:.2f} %'), 11.5, INK, w=600)
for k, (x0, x1, h, u, mx) in enumerate(COLS[1:]):
    m = MIN[CH[k][0]]; xm = x0 + (x1 - x0 - 34) * m / mx
    s.line(xm, 42, xm, TOP + RH * 5 - 10, INK, 1)
    s.t(xm + 3, 51, f'mínimo {m:g} %', 10.5, INK)
s.t(0, 400, 'Tema según el nombre de la campaña; sin cobranza ni avisos. La línea negra marca lo mínimo aceptable de cada canal: 3 clics por cada mil correos,', 10.5, SEC)
s.t(0, 414, '7.5 aperturas por cada mil push y 1 de cada 10 in-app con clic.', 10.5, SEC)

ofe = [val[(g, 'email')] for g, _ in T[1:]]
write(62, dict(
    titulo='La gente responde cuando le recordamos lo que dejó a medias, no cuando le ofrecemos algo nuevo',
    que='Recordatorio: algo que la persona ya empezó y no terminó (verificar identidad, completar datos, poner NIP, crear cuenta, pagar su compra a meses). Oferta nueva: algo que no pidió (Tasa 0, referidos, lanzamientos, cupones).',
    quien='Recordatorios: Marketing (registro de KCash), Acquisition (registro de KPay) y Product Growth (compras a meses). Ofertas: todos los equipos.',
    a_quien='Recordatorios a quien empezó su registro o tiene una compra en curso; ofertas a listas completas de leads, registrados y clientes.',
    lecturas=[
        f'Por correo el recordatorio responde {val[("recordatorio","email")]:.2f} % y las ofertas {min(ofe):.2f} a {max(ofe):.2f} %: entre {val[("recordatorio","email")]/max(ofe):.0f} y {val[("recordatorio","email")]/min(ofe):.0f} veces menos. Tasa 0 es el tema con más correos ({vol["tasa0"]:.0f} M).',
        f'Por push el recordatorio abre {val[("recordatorio","push notification")]:.2f} % en promedio y hasta {exs["recordatorio"][1][2]:.0f} % en la compra a meses; la Tasa 0, {val[("tasa0","push notification")]:.2f} %.',
        f'Referidos no funciona por correo ({val[("referidos","email")]:.2f} %) pero sí dentro de la app ({val[("referidos","in-app")]:.0f} % de clic en in-app): el tema sirve donde la persona ya está. Ojo: el recordatorio adelanta más de lo que suma (lámina 57).',
    ],
    causa='Las campañas nacen de lo que queremos vender este mes, no de lo que cada persona dejó a medias; Braze no tiene a la mano esa información para la mayoría de los equipos.',
    sowhat='El gancho principal es lo que la persona dejó a medias; Tasa 0 y novedades solo con un grupo claro de personas, y referidos dentro de la app.',
    fuente='Fuente: Braze, envíos por campaña, mes y canal (E1), enero a septiembre 2026, sin cobranza ni avisos. Tema por el nombre (regla de la muestra G). El deck anterior decía 3.09 % para el recordatorio con otra clasificación; con esta regla da 2.99 %.',
    svg=s.svg()))
