"""Lámina 49: escalera de recuperación por tiempo sin usar el producto. Izquierda: MXN por conversión del mismo día (E1).
Derecha: % que convirtió en los 90 días siguientes, quien abrió contra quien no (E9a, muestra_m; correo, push y WhatsApp).
Grupo sin mensajes: E13."""
from b5_svg import *
import pandas as pd

P = D['prog']; C = D['control']; A = D['abre']; X = D['ex_email_noabre']
# parte del gasto de 12 meses que es WhatsApp
e1 = pd.read_csv('/home/user/claude/braze-analysis/data/e1_comunicacion_mes_canal.csv')
q = e1[e1.communication_name.fillna('').str.contains('-B0333-|-B0207-')]
wa12 = 100 * q.whatsapp_delivery.sum() / (q.whatsapp_delivery.sum() + 0.05 * q.email_sent.sum())

SECS = [('Ex clientes, por tiempo sin usar KCash o KPay', ['30a90', '3m', '6m', '12m'], BLUE),
        ('Ex clientes sin plazo definido', ['inact', 'dorm'], BLUEL),
        ('Leads que nunca activaron', ['b0171', 'b0223'], MARK2)]
LAB = {'30a90': '30 a 90 días', '3m': '3 meses', '6m': '6 meses', '12m': '12 meses o más', 'inact': 'Inactivos (descuento directo)',
       'dorm': 'Dormants (referidos)', 'b0171': 'Rescate con Tasa 0', 'b0223': 'Installments a never active'}
S = Svg('Por programa de recuperación: pesos por conversión del mismo día y porcentaje que convirtió en los 90 días siguientes entre quien abrió y quien no abrió el mensaje.')
BX0, BX1, BMAX = 196, 400, 700
bx = lambda v: BX0 + (BX1 - BX0) * min(v, BMAX) / BMAX
DX0, DX1, DMAX = 470, 752, 50
dx = lambda v: DX0 + (DX1 - DX0) * v / DMAX
S.t(BX0, 14, 'MXN por conversión del mismo día', 12, INK, w=600)
S.t(DX0, 14, '% que convirtió en los 90 días siguientes', 12, INK, w=600)
S.circle(DX0 + 5, 30, 5, INK); S.t(DX0 + 15, 34, 'Abrió el mensaje', 11, TXT)
S.circle(DX0 + 135, 30, 5, MARK); S.t(DX0 + 145, 34, 'No lo abrió', 11, TXT)
y = 52; RH = 35
rows_y = []
for head, ks, col in SECS:
    S.t(0, y + 10, head, 11, SEC, w=600)
    y += 17
    for k in ks:
        p = P[k]; yc = y + RH / 2 - 3
        S.t(0, yc - 1, LAB[k], 12, INK, w=600)
        S.t(0, yc + 13, f'{p["equipo"]} · {M(p["env"])} M mensajes', 10.5, SEC)
        bw = bx(p['mxn_conv']) - BX0
        S.rect(BX0, yc - 7, bw, 14, col)
        if p['mxn_conv'] > BMAX:  # barra cortada
            S.raw(f'<path d="M{BX1 - 22:.1f} {yc + 9:.1f} l6 -18 M{BX1 - 15:.1f} {yc + 9:.1f} l6 -18" stroke="#FFFFFF" stroke-width="3"/>')
        if p['mxn_conv'] > BMAX: S.t(BX1 - 28, yc + 4, fmt(p['mxn_conv']), 12, INK, 'end', 600, halo=True)
        else: S.t(BX0 + bw + 6, yc + 4, fmt(p['mxn_conv']), 12, INK, w=600)
        a, b = p['ca90'], p['cn90']
        S.line(dx(b), yc, dx(a), yc, GRID, 3)
        S.circle(dx(b), yc, 5, MARK); S.circle(dx(a), yc, 5, INK)
        S.t(dx(a) + 9, yc + 4, f'{a:.0f} %' if a >= 1 else f'{a:.1f} %', 11, INK, w=600)
        S.t(dx(b) - 9, yc + 4, f'{b:.0f} %' if b >= 1 else f'{b:.1f} %', 11, SEC, 'end')
        rows_y.append(yc)
        y += RH
    y += 2
AX = y + 2
for v in (0, 25, 50):
    S.line(dx(v), 46, dx(v), AX - 8)
    S.t(dx(v), AX + 6, f'{v} %', 10.5, SEC, 'middle')
S.line(BX0, 46, BX0, AX - 8, MARK)
for v in (0, 350, 700):
    S.t(bx(v), AX + 6, f'{v}', 10.5, SEC, 'middle')
SVG = S.done()

ex, nu = D['grupos']['ex'], D['grupos']['nunca']
fe = D['frio_equipo']
guarda(49, dict(
    kind='grafica',
    titulo='Recuperar al cliente que se fue funciona si llegamos pronto; cada mes de espera encarece la conversión',
    que='Mensajes para recuperar: descuento directo, descuento escalonado, cupón, "con o sin oferta", referidos y Tasa 0, por correo, push, WhatsApp e in-app.',
    quien=f'Product Growth manda casi toda la recuperación de ex clientes ({M(fe["ex|Product Growth"]["env"])} M de {M(ex["env"])} M mensajes). Marketing manda referidos a dormants y el rescate con Tasa 0 a leads ({M(fe["nunca|Marketing"]["env"])} M de {M(nu["env"])} M).',
    a_quien='Ex clientes con 30 a 90 días, 3, 6 o 12 meses sin usar KCash o KPay; dormants; y leads que se registraron y nunca tomaron crédito.',
    lecturas=[
        f'Mientras más reciente la inactividad, más barata la conversión: {P["30a90"]["mxn_conv"]:.0f} MXN a los 30 a 90 días, {P["3m"]["mxn_conv"]:.0f} a los 3 meses, {P["6m"]["mxn_conv"]:.0f} a los 6 y {P["12m"]["mxn_conv"]:.0f} a los 12, donde {wa12:.0f} % del gasto es WhatsApp.',
        f'Quien se fue hace poco vuelve aunque no abra: {P["30a90"]["cn90"]:.0f} % de quienes no abrieron el mensaje convirtió en 90 días; a los 12 meses, {P["12m"]["cn90"]:.1f} %. Quien abre convierte más (correo de inactivos: {A["b0209_email"]["ca90"]:.1f} % contra {A["b0209_email"]["cn90"]:.1f} %).',
        f'Sin un grupo sin mensajes no sabemos cuántos habrían vuelto solos. De {C["canvas"]} Canvas de recuperación, {C["con_control"]} lo tienen, todos del rescate Tasa 0 y con {C["min"]} a {C["max"]} personas. Los de ex clientes, ninguno.',
    ],
    causa=f'La recuperación se arma por oferta y no por el tiempo que la persona lleva sin usar el producto, y ningún programa deja a un grupo sin mensajes. Por eso el programa de 12 meses gasta {M(P["12m"]["costo"])} M MXN, casi todo en WhatsApp, en la conversión más cara.',
    sowhat='No se trata de dejar de buscar a los ex clientes sino de ordenarlo: primero a quien se fue hace poco, con límite de gasto por programa y un grupo sin mensajes que diga cuánto recupera.',
    fuente=f'Fuente: Braze E1 (campaña, canal y mes) y E9a (conversión a 90 días de quien abre contra quien no, correo, push y WhatsApp), enero a septiembre 2026; E13 (grupos de control). Conversión del mismo día: se reparte entre los mensajes del día; es referencia. 6 meses = B0332, B0206 y su variante; 12 meses = B0333 y B0207. El guion decía 673 Canvas de recuperación; con la misma regla de nombres salen {C["canvas"]}.',
    svg=SVG,
))
print({k: (round(p['mxn_conv']), round(p['ca90'], 1), round(p['cn90'], 1)) for k, p in P.items()}, round(wa12))
