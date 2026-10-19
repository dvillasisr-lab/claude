"""Lámina 33: concentración. E3 (9 meses, personas por banda de mensajes recibidos). Escribe 033.json."""
import pandas as pd
from kit import *
e3 = pd.read_csv(D + 'e3_usuarios_distribucion.csv')
e3['costo'] = 0.05 * e3.msgs_email + 1.0 * e3.msgs_whatsapp_entregados
g = e3.groupby('banda_msgs')[['usuarios', 'msgs', 'msgs_email', 'msgs_push', 'msgs_whatsapp_entregados', 'costo', 'bajas_email', 'usuarios_con_conversion']].sum()
HI = ['41-80', '081-160', '161-320', '321+']
top = g.loc[HI].sum(); tot = g.sum()
sh = {c: 100 * top[c] / tot[c] for c in g.columns}
print({k: round(v, 1) for k, v in sh.items()}, 'personas M', top.usuarios / 1e6, 'costo M', top.costo / 1e6, tot.costo / 1e6)
print('por persona 9m', top.msgs / top.usuarios, 'al mes', top.msgs / top.usuarios / 9)
BANDS = [('01-05', '1 a 5'), ('06-10', '6 a 10'), ('11-20', '11 a 20'), ('21-40', '21 a 40'), ('41-80', '41 a 80'), ('081-160', '81 a 160'), ('161-320', '161 a 320'), ('321+', '321 o más')]
b = g.loc[[k for k, _ in BANDS]].copy()
b['pp'] = b.msgs / b.usuarios; b['bmil'] = 1000 * b.bajas_email / b.msgs_email; b['cpp'] = b.costo / b.usuarios
print(b[['usuarios', 'pp', 'bmil', 'cpp']].round(2))
# mensual (E4b)
e4 = pd.read_csv(D + 'e4b_concentracion_mes.csv'); e4 = e4[e4.banda_msgs_mes != '00']
h4 = e4[e4.banda_msgs_mes.isin(['41-80', '081-160', '161+'])]
mu, mm = 100 * h4.usuarios.sum() / e4.usuarios.sum(), 100 * h4.msgs.sum() / e4.msgs.sum()
print('mensual', mu, mm)

S = Svg('Parte de personas, mensajes, push, WhatsApp, gasto, compras y bajas que se lleva quien recibe 41 o más mensajes en nueve meses; y bajas por mil correos por banda de mensajes')
S.legend([('sq', BLUE, 'Reciben 41 o más mensajes en 9 meses'), ('sq', GREEN, 'Mismo grupo, en compras'), ('sq', G2, 'Reciben 40 o menos')], 0, 10)
S.t(0, 42, 'Parte del total que se lleva cada grupo, enero a septiembre 2026', 10.5, SEC)
ROWS = [('Personas', 'usuarios', BLUE), ('Mensajes', 'msgs', BLUE), ('Push', 'msgs_push', BLUE), ('WhatsApp entregado', 'msgs_whatsapp_entregados', BLUE),
        ('Gasto en mensajes', 'costo', BLUE), ('Personas que compraron', 'usuarios_con_conversion', GREEN), ('Bajas de email', 'bajas_email', G1)]
X0, X1 = 150, 455; y = 66; bh = 26; gap = 14
for lab, c, col in ROWS:
    v = sh[c]; w = (X1 - X0) * v / 100
    S.t(X0 - 10, y + bh / 2 + 4, lab, 11.5, INK if c in ('usuarios', 'msgs') else TXT, 'end', 600 if c in ('usuarios', 'msgs') else 400)
    S.rect(X0, y, w - 1, bh, col); S.rect(X0 + w + 1, y, X1 - X0 - w - 1, bh, G2)
    lc = '#FFFFFF' if col != G1 else INK
    if w > 46: S.t(X0 + w - 6, y + bh / 2 + 4.5, f'{v:.0f} %', 12, lc, 'end', 700)
    else: S.t(X0 + w + 6, y + bh / 2 + 4.5, f'{v:.0f} %', 12, INK, 'start', 700)
    y += bh + gap
S.t(0, y + 6, f'{top.usuarios/1e6:.1f} M personas reciben {top.msgs/top.usuarios:.0f} mensajes cada una, unos {top.msgs/top.usuarios/9:.0f} al mes.', 11, TXT)
S.t(0, y + 22, f'Gasto: {top.costo/1e6:.1f} de {tot.costo/1e6:.1f} M MXN en 9 meses (WhatsApp por entregado y email).', 11, TXT)
# panel derecho: bajas por mil correos por banda, barras horizontales
PX0, LX, BX0, BX1 = 520, 590, 598, 748
S.t(PX0 - 4, 66, 'Bajas por cada mil correos, según cuántos', 11.5, INK, w=600)
S.t(PX0 - 4, 81, 'mensajes recibió la persona en 9 meses', 11.5, INK, w=600)
VM = 15; bx = lambda v: BX0 + (BX1 - BX0) * v / VM
yy = 100; rh = 27
for i, (k, lab) in enumerate(BANDS):
    v = b.loc[k, 'bmil']; hi = k in HI
    S.t(LX, yy + rh / 2 + 3, lab, 11, TXT, 'end')
    S.rect(BX0, yy + 4, bx(v) - BX0, rh - 10, BLUE if hi else G1)
    S.t(bx(v) + 5, yy + rh / 2 + 3.5, f'{v:.1f}', 11, INK, 'start', 600)
    yy += rh
S.line(BX0, 98, BX0, yy, SEC, 1)
S.t(PX0 - 4, yy + 16, 'Azul: el grupo de 41 o más mensajes.', 10.5, SEC)
S.t(PX0 - 4, yy + 31, 'Gasto por persona en 9 meses:', 10.5, SEC)
S.t(PX0 - 4, yy + 45, f'{b.loc["01-05","cpp"]:.2f} MXN (1 a 5); {b.loc["321+","cpp"]:.0f} MXN (321 o más)', 10.5, SEC)

write(33, dict(kind='grafica', seccion='IV. La misma persona, demasiadas veces',
 titulo='Una cuarta parte de la base recibe 86 % de los mensajes y es la que más compra: hay que quitar lo que ignora, no a la persona',
 que='Mezcla de promocional y operativo: cobranza diaria, Comercio del día, recordatorio de terminar el registro, rescates por push y Tasa 0. En este grupo, 46 % son correos, 42 % push, 8 % WhatsApp y 4 % in-app.',
 quien='Marketing (Comercio del día, Rescate fines de semana, Rescate Tasa 0, recordatorio de registro), Product Growth (Tasa 0 a registrados, nunca activos, inactivos), Collections (cobranza) y Others (recomendaciones de Shopping).',
 a_quien=f'{top.usuarios/1e6:.1f} M personas con 41 o más mensajes en 9 meses. Incluye 631 mil prospectos que aún no son clientes, con 303 mensajes cada uno, y 272 mil con tarjeta KPay congelada.',
 lecturas=[
  f'{sh["usuarios"]:.0f} % de las personas recibe {sh["msgs"]:.0f} % de los mensajes, {sh["msgs_push"]:.0f} % del push y {sh["costo"]:.0f} % del gasto: {top.costo/1e6:.1f} M MXN en 9 meses. Por mes se repite: {mu:.0f} % de las personas recibe 41 o más y se lleva {mm:.0f} % del volumen.',
  f'Es también la base que compra: {sh["usuarios_con_conversion"]:.0f} % de las personas que compraron está en este grupo.',
  f'Por correo se dan de baja menos: {b.loc["321+","bmil"]:.1f} a {b.loc["41-80","bmil"]:.1f} bajas por mil correos, contra {b.loc["01-05","bmil"]:.1f} en quien recibe 1 a 5.',
 ],
 causa='Lo que sobra no es la persona sino lo que ya ignora: push de Rescate fines de semana (Marketing, 13.4 M push, 0.76 % los abre), Rescate Tasa 0 a anónimos (0.56 %) y WhatsApp a bases que no responden.',
 sowhat='Cortar parejo a quien recibe mucho le pega a quien compra: hay que quitar las campañas que esa persona ya no abre.',
 fuente='Fuente: Braze, mensajes por persona en enero a septiembre 2026 (E3) y por mes (E4b). Gasto: WhatsApp a 1.00 MXN por entregado y email a 0.05 MXN por enviado. Bajas de E3 son eventos. Aperturas por campaña: E1. Prospectos según la tabla de filtros de cliente.',
 svg=S.svg()))
