"""Lámina 14: in-app trae más conversiones por mensaje en cada tema (mapa de calor tema x canal) y ningún equipo
le da más de 5 % de sus mensajes (barras 100 % por equipo y canal, con el clic de in-app de cada equipo)."""
import math
from b2base import *

d = load_b()
CH = [('email', 'Correo'), ('push notification', 'Push'), ('whatsapp', 'WhatsApp'), ('in-app', 'In-app')]
TEM = [('recordatorio', 'Recordatorios'), ('referidos', 'Referidos'), ('lanzamiento', 'Lanzamientos'), ('descuento', 'Descuentos'), ('tasa0', 'Tasa 0')]
cpm = lambda g: 1000 * g.conversiones_fraccional.sum() / g.envios.sum()
M = {}
for k, lab in TEM:
    for c, cl in CH:
        M[(lab, cl)] = cpm(d[(d.gan == k) & (d.canal == c)])
for c, cl in CH:
    M[('Todo el canal', cl)] = cpm(d[d.canal == c])
i = d[d.canal == 'in-app']
iv = i.in_app_impression.sum()
vt = 100 * i.groupby('gan').in_app_impression.sum() / iv
ve = 100 * i.groupby('equipo').in_app_impression.sum() / iv
va = 100 * i.groupby('aud').in_app_impression.sum() / iv
vtipo = 100 * i.groupby('tipo').in_app_impression.sum() / iv
clic_eq = i.groupby('equipo').apply(lambda g: 100 * g.in_app_click.sum() / g.in_app_impression.sum())
conv_eq = i.groupby('equipo').apply(lambda g: 1000 * g.conversiones_fraccional.sum() / g.in_app_impression.sum())
mix = d.groupby(['equipo', 'canal']).envios.sum().unstack().fillna(0)
mix = 100 * mix.div(mix.sum(axis=1), axis=0)
clic = lambda k, c: 100 * d[(d.gan == k) & (d.canal == c)].r.sum() / d[(d.gan == k) & (d.canal == c)].b.sum()
ref_e, ref_i = clic('referidos', 'email'), clic('referidos', 'in-app')
lan_e, lan_i = clic('lanzamiento', 'email'), clic('lanzamiento', 'in-app')
print({k: round(v, 1) for k, v in M.items()})
print('vistas', iv / 1e6, 'clics', i.in_app_click.sum() / 1e6, 'tipo', vtipo.round(1).to_dict())
print('tema', vt.round(1).to_dict(), 'equipo', ve.round(1).to_dict(), 'aud', va.round(1).to_dict())
print('clic eq', clic_eq.round(1).to_dict(), 'conv eq', conv_eq.round(1).to_dict())
print('mix in-app', mix['in-app'].round(1).to_dict())
print('ref', ref_e, ref_i, 'lan', lan_e, lan_i)

S = Svg('Izquierda: conversiones por cada mil mensajes por tema y canal; in-app es el más alto en cada fila. '
        'Derecha: reparto de los mensajes de cada equipo por canal; in-app es 5 % o menos en todos.')
# ===== mapa de calor
S.t(0, 16, 'Conversiones por cada mil mensajes, por tema y canal', 12, INK, w=600)
S.t(0, 33, 'Enero a septiembre; el color más oscuro es más conversión.', 10.5, SEC)
RX0, CW, RH, Y0 = 112, 76, 40, 70
rows = [lab for _, lab in TEM] + ['Todo el canal']
for j, (c, cl) in enumerate(CH):
    S.t(RX0 + CW * j + CW / 2, Y0 - 8, cl, 11.5, INK if cl == 'In-app' else TXT, 'middle', 700 if cl == 'In-app' else 400)
ramp = lambda v: min(1, max(0, (math.log10(max(v, 0.2)) - math.log10(0.2)) / (math.log10(40) - math.log10(0.2))))
def mix_col(t):
    # de blanco azulado a azul #1F4FD8
    a = (0xEE, 0xF2, 0xFC); b = (0x1F, 0x4F, 0xD8)
    return '#%02X%02X%02X' % tuple(round(a[k] + (b[k] - a[k]) * t) for k in range(3))
for ii, lab in enumerate(rows):
    y = Y0 + RH * ii + (10 if lab == 'Todo el canal' else 0)
    tot = lab == 'Todo el canal'
    S.t(RX0 - 8, y + RH / 2 + 4, lab, 11.5, INK if tot else TXT, 'end', 600 if tot else 400)
    for j, (c, cl) in enumerate(CH):
        v = M[(lab, cl)]
        t = ramp(v)
        S.rect(RX0 + CW * j, y, CW - 2, RH - 2, mix_col(t))
        S.t(RX0 + CW * j + CW / 2 - 1, y + RH / 2 + 4, f'{v:.1f}', 12 if cl == 'In-app' else 11.5, '#FFFFFF' if t > 0.55 else INK, 'middle', 700 if cl == 'In-app' else 400)
S.rect(RX0 + CW * 3 - 1, Y0 - 1, CW, RH * 5 + 0.5, 'none', f' stroke="{INK}" stroke-width="1.5"')
S.rect(RX0 + CW * 3 - 1, Y0 + RH * 5 + 9, CW, RH + 0.5, 'none', f' stroke="{INK}" stroke-width="1.5"')
yb = Y0 + RH * 6 + 30
S.t(0, yb, f'Clics por cada cien: referidos {ref_e:.2f} por correo y {ref_i:.0f} en in-app;', 11, TXT)
S.t(0, yb + 16, f'lanzamientos {lan_e:.2f} por correo y {lan_i:.0f} en in-app.', 11, TXT)
S.line(434, 8, 434, 404, GRID)
# ===== barras por equipo
X0 = 450
S.t(X0, 16, 'Mensajes de cada equipo, por canal', 12, INK, w=600)
ORD = [('in-app', 'In-app', BLUE), ('whatsapp', 'WhatsApp', GREEN2), ('push notification', 'Push', G1), ('email', 'Correo', G2)]
lx = X0
for c, cl, col in ORD:
    S.rect(lx, 25, 10, 10, col)
    S.t(lx + 14, 34, cl, 11, INK if c == 'in-app' else TXT, w=600 if c == 'in-app' else 400)
    lx += 14 + tw(cl, 11) + 14
EQ = ['Marketing', 'Product Growth', 'Sales', 'Others', 'Collections']
BX0, BX1 = X0, 700
S.t(BX1 + 8, 58, 'Clic en', 10.5, SEC)
S.t(BX1 + 8, 70, 'in-app', 10.5, SEC)
for k, eq in enumerate(EQ):
    y = 90 + k * 58
    S.t(BX0, y - 6, eq, 11.5, INK, w=600)
    S.t(BX0 + tw(eq, 11.5, 600) + 8, y - 6, f'in-app {mix.loc[eq]["in-app"]:.1f} %', 11.5, BLUE, w=700)
    x = BX0
    for c, cl, col in ORD:
        ww = (BX1 - BX0) * mix.loc[eq].get(c, 0) / 100
        S.rect(x, y, ww - (1.5 if ww > 3 else 0), 22, col)
        x += ww
    S.t(BX1 + 8, y + 15, f'{clic_eq[eq]:.0f} %', 11.5, INK, w=600)
S.t(X0, 392, 'In-app es 5 % o menos de los mensajes de cada equipo.', 11, INK, w=600)
svg = S.done()

save(14, dict(
    kind='grafica',
    titulo='In-app es el canal que más conversiones trae por mensaje y no cuesta, y ningún equipo le da más de 5 % de sus mensajes',
    que=f'Casi pura promoción ({vtipo["promocional"]:.0f} % de las vistas): referidos {vt["referidos"]:.0f} %, lanzamientos {vt["lanzamiento"]:.0f} %, recordatorios de algo que la persona empezó {vt["recordatorio"]:.0f} %, descuentos {vt["descuento"]:.0f} % y Tasa 0 {vt["tasa0"]:.0f} %.',
    quien=f'Marketing {ve["Marketing"]:.0f} % de las vistas, Product Growth {ve["Product Growth"]:.0f} %, Sales {ve["Sales"]:.0f} % y Others {ve["Others"]:.0f} %. Clic: Product Growth {clic_eq["Product Growth"]:.0f} % y Sales {clic_eq["Sales"]:.0f} %.',
    a_quien=f'Solo a quien abre la app: clientes activos {va["activos"]:.0f} % de las vistas, leads {va["leads"]:.0f} %, bases frías {va["frios"]:.0f} %. Sin app no hay in-app.',
    lecturas=[
        f'In-app trae {M[("Todo el canal","In-app")]:.0f} conversiones por cada mil mensajes; WhatsApp {M[("Todo el canal","WhatsApp")]:.1f}, correo {M[("Todo el canal","Correo")]:.1f} y push {M[("Todo el canal","Push")]:.1f}. Gana en cada tema y no cuesta.',
        f'Son {iv/1e6:.1f} M vistas con {i.in_app_click.sum()/1e6:.1f} M clics. El registro de línea de celular de Marketing: 2.2 M vistas y 87 % de clic; BillPay de Others: 85 % en in-app y 0.11 % por correo.',
        'Ojo: in-app solo llega a quien abre la app, que ya está más cerca de comprar. La diferencia real es menor, pero el orden se sostiene.',
    ],
    causa='In-app no es el canal de costumbre de ningún equipo y solo llega a quien abre la app, así que las campañas se arman primero para push y correo.',
    sowhat='Para quien usa la app, in-app primero y push de respaldo. Quien no tiene la app (ex clientes, rezagados que solo usan la web) va por correo.',
    fuente=f'{FUENTE_E1}. Conversión: préstamo o compra en los 7 días después del mensaje, repartida entre los mensajes del día; no prueba causa. Vistas = impresiones de in-app. Tema según el nombre de la campaña.',
    svg=svg,
))
