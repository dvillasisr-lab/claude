"""Lámina 50: casi la mitad del gasto de WhatsApp va a recuperar ex clientes y leads que nunca activaron, donde cada conversión cuesta más.
Izquierda: gasto de WhatsApp entregado por grupo (M MXN y % del canal). Derecha: MXN por conversión del mismo día, WhatsApp contra correo (E1)."""
from b5_svg import *

GC = D['gc']; G = D['grupos']; T = D['tot']; WP = D['wa_prog']; FE = D['frio_equipo']
ORD = ['nunca', 'ex', 'activos', 'leads', 'todos', 'nuevos', 'transaccional']
LAB = {'nunca': 'Leads que nunca activaron', 'ex': 'Ex clientes inactivos', 'activos': 'Activos y recurrentes', 'leads': 'Leads y registrados',
       'todos': 'Todos y otros', 'nuevos': 'Nuevos y onboarding', 'transaccional': 'Avisos transaccionales'}
S = Svg('Por grupo de audiencia: gasto en WhatsApp entregado en millones de pesos, y pesos por conversión del mismo día por WhatsApp y por correo.')
BX0, BX1, BMAX = 182, 372, 15
bx = lambda v: BX0 + (BX1 - BX0) * v / BMAX
DX0, DX1, DMAX = 452, 742, 600
dx = lambda v: DX0 + (DX1 - DX0) * v / DMAX
S.t(BX0, 14, 'Gasto en WhatsApp entregado', 12, INK, w=600)
S.t(BX0, 30, 'M MXN, enero a septiembre', 10.5, SEC)
S.t(DX0, 14, 'MXN por conversión del mismo día', 12, INK, w=600)
S.circle(DX0 + 5, 26, 5, BLUE); S.t(DX0 + 15, 30, 'WhatsApp', 11, TXT)
S.circle(DX0 + 95, 26, 5, MARK); S.t(DX0 + 105, 30, 'Correo', 11, TXT)
TOP, RH = 56, 46
for i, g in enumerate(ORD):
    yc = TOP + RH * i + 14
    w, e = GC[f'{g}|whatsapp'], GC[f'{g}|email']
    cold = g in ('nunca', 'ex')
    S.t(0, yc - 2, LAB[g], 12, INK, w=600 if cold else 400)
    S.t(0, yc + 13, f'Llega {w["entrega"]:.0f} % del WhatsApp', 10.5, SEC)
    S.rect(BX0, yc - 8, max(bx(w['costo'] / 1e6) - BX0, 1.5), 16, BLUE if cold else MARK2)
    S.t(bx(w['costo'] / 1e6) + 6, yc + 4, f'{M(w["costo"])} M ({100 * w["costo"] / T["wa"]:.0f} %)', 11.5, INK if cold else SEC, w=600 if cold else 400)
    a, b = w['mxn_conv'], e['mxn_conv']
    S.line(dx(b), yc, dx(a), yc, GRID, 3)
    S.circle(dx(b), yc, 5, MARK); S.circle(dx(a), yc, 5.5, BLUE if cold else BLUEL)
    S.t(dx(a) + 9, yc + 4, fmt(a), 11.5, INK, w=600 if cold else 400)
    if dx(a) - dx(b) > 34:
        S.t(dx(b) - 9, yc + 4, fmt(b), 11, SEC, 'end') if dx(b) - DX0 > 22 else S.t(dx(b), yc + 19, fmt(b), 11, SEC, 'middle')
AX = TOP + RH * len(ORD)
for v in (0, 200, 400, 600):
    S.line(dx(v), 42, dx(v), AX - 12)
    S.t(dx(v), AX + 2, f'{v}', 10.5, SEC, 'middle')
for v in (0, 5, 10, 15):
    S.t(bx(v), AX + 2, f'{v} M' if v else '0', 10.5, SEC, 'middle')
S.line(BX0, 42, BX0, AX - 12, MARK)
SVG = S.done()

wa_fr = GC['ex|whatsapp']['costo'] + GC['nunca|whatsapp']['costo']
conv_fr_wa = GC['ex|whatsapp']['conv'] + GC['nunca|whatsapp']['conv']
pi_ex = GC['ex|push notification']['conv'] + GC['ex|in-app']['conv']
mk = FE['ex|Marketing']['costo'] + FE['nunca|Marketing']['costo']; pg = FE['ex|Product Growth']['costo'] + FE['nunca|Product Growth']['costo']
guarda(50, dict(
    kind='grafica',
    titulo='Casi la mitad del WhatsApp se gasta en recuperar a quien ya no nos usa, justo donde cada conversión cuesta más',
    que='Rescate con Tasa 0 a leads rezagados, descuento directo y "con o sin oferta" a inactivos y churn, referidos a dormants e Installments a never active. Todo promocional.',
    quien=f'Marketing pone {M(mk)} M MXN en esta recuperación, {M(WP["b0171"]["costo"])} M solo en el WhatsApp del rescate con Tasa 0. Product Growth pone {M(pg)} M MXN.',
    a_quien='Dos bases frías distintas: ex clientes que dejaron de usar KCash o KPay (inactivos de 1 a 12 meses, dormants, churn) y leads que se registraron y nunca tomaron crédito.',
    lecturas=[
        f'Leads que nunca activaron y ex clientes se llevan {M(wa_fr)} M MXN de WhatsApp entregado, {100*wa_fr/T["wa"]:.0f} % del canal, y traen {100*conv_fr_wa/T["conv"]:.1f} % de las conversiones del mismo día.',
        f'En ex clientes cada conversión cuesta {GC["ex|whatsapp"]["mxn_conv"]:.0f} MXN por WhatsApp y {GC["ex|email"]["mxn_conv"]:.0f} por correo; push e in-app no cuestan y traen {mil(pi_ex)} mil conversiones. En leads que nunca activaron, {GC["nunca|whatsapp"]["mxn_conv"]:.0f} y {GC["nunca|email"]["mxn_conv"]:.0f} MXN.',
        f'En activos el WhatsApp sí rinde: {GC["activos|whatsapp"]["conv_mil"]:.1f} conversiones por cada mil mensajes, contra {GC["ex|whatsapp"]["conv_mil"]:.1f} en ex clientes y {GC["nunca|whatsapp"]["conv_mil"]:.1f} en leads que nunca activaron.',
    ],
    causa='WhatsApp es el canal que más se lee, por eso se usa para insistir. Pero en estas bases la lectura casi no se vuelve préstamo, a uno de cada tres ya no le llega y ningún programa tiene un límite de gasto.',
    sowhat='WhatsApp para recuperar solo a quien leyó uno en los últimos 90 días; al resto, primero correo, push o in-app, con un grupo sin mensajes para medir.',
    fuente=f'Fuente: Braze E1 (campaña, canal y mes), enero a septiembre 2026. WhatsApp a 1.00 MXN por entregado, correo a 0.05 MXN por enviado. Ejemplos: WhatsApp del rescate Tasa 0 (B0171) {M(WP["b0171"]["send"])} M enviados y {WP["b0171"]["mxn"]:.0f} MXN por conversión; de churn 12 meses (B0333) {fmt(WP["b0333"]["mxn"])}. La versión anterior decía 23 M MXN y un tercio del WhatsApp porque cobraba por enviado.',
    svg=SVG,
))
