"""Lámina 56: patrón de respuesta por persona (E7b, muestra J). Dispersión: % que convirtió (eje x, escala x10) contra % que se dio
de baja del email (eje y), tamaño = personas, color = número de canales por los que responde. Tabla al lado por número de canales."""
import math
from comun import *

j = pd.read_csv(H / 'muestra_j_patron_respuesta.csv')
j['n'] = j[['resp_email', 'resp_push', 'resp_wa', 'resp_inapp']].sum(axis=1)
T, TC, TB, TM, TK = j.usuarios.sum(), j.usuarios_con_conversion.sum(), j.usuarios_con_baja_email.sum(), j.msgs.sum(), j.costo.sum()
NOM = {(0, 0, 0, 0): 'No responde a nada', (0, 0, 1, 0): 'Solo WhatsApp', (0, 0, 0, 1): 'Solo in-app', (1, 0, 0, 0): 'Solo email',
       (1, 0, 1, 0): 'Email y WhatsApp', (1, 1, 1, 1): 'Los cuatro canales', (0, 1, 1, 1): 'Push, WhatsApp e in-app',
       (0, 0, 1, 1): 'WhatsApp e in-app', (1, 0, 0, 1): 'Email e in-app'}
j['nom'] = [NOM.get(k) for k in zip(j.resp_email, j.resp_push, j.resp_wa, j.resp_inapp)]
g = j.groupby('n').agg(u=('usuarios', 'sum'), c=('usuarios_con_conversion', 'sum'), b=('usuarios_con_baja_email', 'sum'), m=('msgs', 'sum'), k=('costo', 'sum'))
g['conv'] = 100 * g.c / g.u; g['mpu'] = g.m / g.u; g['kpu'] = g.k / g.u
dos = g.loc[2:]
p2u, p2c, p2m = 100 * dos.u.sum() / T, 100 * dos.c.sum() / TC, 100 * dos.m.sum() / TM
em = j[j.resp_email == 1]; pem_u, pem_b = 100 * em.usuarios.sum() / T, 100 * em.usuarios_con_baja_email.sum() / TB
r = {k: j[j.nom == k].iloc[0] for k in NOM.values()}
print(g.round(2)); print('2+', round(p2u, 1), round(p2c, 1), round(p2m, 1), 'email', round(pem_u, 1), round(pem_b, 1))

COL = {0: M2, 1: M1, 2: BLUEL, 3: BLUE, 4: BLUE}
s = SVG('Patrones de respuesta por persona: porcentaje que convirtió contra porcentaje que se dio de baja del email, tamaño según personas y color según número de canales')
s.legend([(M2, 'Ninguno', 'dot'), (M1, '1 canal', 'dot'), (BLUEL, '2 canales', 'dot'), (BLUE, '3 o 4 canales', 'dot')], 0, 4)
s.t(0, 32, 'Cada punto es una forma de responder; su tamaño, las personas que la tienen.', 10.5, SEC)
X0, X1, Y0, Y1 = 46, 455, 66, 352
lx = lambda v: X0 + (X1 - X0) * (math.log10(max(v, 0.06)) - math.log10(0.05)) / (math.log10(100) - math.log10(0.05))
ly = lambda v: Y1 - (Y1 - Y0) * v / 20
for v in (0, 5, 10, 15, 20):
    s.line(X0, ly(v), X1, ly(v)); s.t(X0 - 6, ly(v) + 4, f'{v} %', 11, SEC, 'end')
for v, lab in ((0.1, '0.1 %'), (1, '1 %'), (10, '10 %'), (100, '100 %')):
    s.line(lx(v), Y0, lx(v), Y1); s.t(lx(v), Y1 + 19, lab, 11, SEC, 'middle')
s.t(X0 - 40, Y0 - 12, '% que se dio de baja del email', 11, SEC)
s.t(X1, Y1 + 35, '% de personas que convirtió (cada marca, diez veces más)', 11, SEC, 'end')
rad = lambda u: max(4.5, 22 * math.sqrt(u / j.usuarios.max()))
for _, q in j.sort_values('usuarios', ascending=False).iterrows():
    s.circle(lx(q.convierten_pct), ly(q.baja_pct), rad(q.usuarios), COL[q.n])
# etiquetas directas: (nombre, dx, dy, ancla)
LAB = [('No responde a nada', 28, -4, 'start'), ('Solo WhatsApp', -14, -8, 'end'),
       ('Solo email', 0, -24, 'middle'), ('Email y WhatsApp', -10, 16, 'end'), ('Los cuatro canales', -4, -18, 'end')]
for k, dx, dy, an in LAB:
    q = r[k]; x, y = lx(q.convierten_pct), ly(q.baja_pct)
    s.t(x + dx, y + dy, k, 11.5, INK, an, 600, halo=True)
    s.t(x + dx, y + dy + 13, f'{mil(q.usuarios)} · {q.baja_pct:.1f} % baja', 10.5, SEC, an, halo=True)
# tabla por número de canales
TX = 490
s.t(TX, 56, 'Según por cuántos canales responde', 12, INK, w=600)
cols = [(TX, 'Canales', 'start'), (TX + 145, 'Personas', 'end'), (TX + 200, 'Convirtió', 'end'), (TX + 258, 'Mensajes', 'end'), (TX + 290, 'MXN', 'end')]
for x, h, a in cols: s.t(x, 80, h, 10.5, SEC, a, 600)
s.line(TX, 88, 780, 88, INK, 1)
NOMN = {0: 'Ninguno', 1: 'Uno', 2: 'Dos', 3: 'Tres', 4: 'Los cuatro'}
for i, (n, q) in enumerate(g.iterrows()):
    y = 108 + 24 * i; hi = n >= 2
    s.circle(TX + 5, y - 4, 4.5, COL[n], ring=False)
    s.t(TX + 15, y, NOMN[n], 11.5, INK, w=600 if hi else 400)
    s.t(TX + 145, y, mil(q.u), 11.5, TXT, 'end')
    s.t(TX + 200, y, f'{q.conv:.0f} %' if q.conv >= 1 else f'{q.conv:.1f} %', 11.5, INK if hi else TXT, 'end', 600 if hi else 400)
    s.t(TX + 258, y, f'{q.mpu:.0f}', 11.5, TXT, 'end')
    s.t(TX + 290, y, f'{q.kpu:.1f}', 11.5, TXT, 'end')
    s.line(TX, y + 8, 780, y + 8)
s.t(TX, 236, 'Mensajes y MXN: por persona, en nueve meses.', 10.5, SEC)
y = 250
s.rect(TX, y, 290, 98, '#EEF2FC')
s.t(TX + 12, y + 22, f'Dos o más canales', 12, BLUE, w=600)
for i, ln in enumerate([f'{p2u:.0f} % de las personas ({mil(dos.u.sum())})', f'{p2c:.0f} % de quienes convirtieron', f'{p2m:.0f} % de los mensajes']):
    s.t(TX + 12, y + 42 + 17 * i, ln, 11.5, INK)
s.t(TX, 372, f'Quien responde al email es {pem_u:.0f} % de las personas', 11, TXT)
s.t(TX, 387, f'y {pem_b:.0f} % de quienes se dieron de baja.', 11, TXT)
s.t(0, 414, 'Responder: clic en email, abrir push, leer WhatsApp o clic en in-app, de enero a septiembre. Convirtió: Braze registró un crédito otorgado.', 10.5, SEC)

n4, n3, wa, ne, ewa, nada = r['Los cuatro canales'], g.loc[3], r['Solo WhatsApp'], r['Solo email'], r['Email y WhatsApp'], r['No responde a nada']
write(56, dict(
    titulo='Quien responde por varios canales es el cliente activo; quien solo lee el correo es el que más se da de baja',
    que='Todo lo que mandamos. Lo que más abre quien usa varios canales: el recordatorio de pagar su compra a meses (push 11.0 % de apertura) y el aviso de pago recibido (push 14.2 %).',
    quien='Todos los equipos. Others es BillPay de NewProducts, avisos de KPay y KCash, recomendaciones de Shopping y pruebas de QA.',
    a_quien=f'19.5 M personas que recibieron algo en nueve meses, según por qué canales responden: {mil(dos.u.sum())} por dos o más, {mil(ne.usuarios)} solo por email y {mil(wa.usuarios)} solo por WhatsApp.',
    lecturas=[
        f'Quien responde por los cuatro canales ({mil(n4.usuarios)}) convirtió {n4.convierten_pct:.0f} % y solo {n4.baja_pct:.1f} % se dio de baja del email. Son clientes que usan la app.',
        f'Quien solo responde al email ({mil(ne.usuarios)}) convirtió {ne.convierten_pct:.0f} % y {ne.baja_pct:.1f} % se dio de baja; con email y WhatsApp, {ewa.baja_pct:.1f} %. Es el lector de correo que se cansa.',
        f'Solo WhatsApp: {mil(wa.usuarios)} personas, {wa.convierten_pct:.0f} % convirtió, {wa.msgs_por_usuario:.0f} mensajes por persona y {wa.pct_costo:.0f} % del gasto.',
    ],
    causa='Mandamos los mismos mensajes por todos los canales a todos, sin mirar por cuál responde cada persona. Por eso el lector de correo recibe correo de más y quien solo lee WhatsApp lo recibe aunque no compre.',
    sowhat='Un trato por patrón: al que responde por varios canales, pocos mensajes y bien elegidos; al lector de correo, menos correos; al que solo lee WhatsApp, pasarlo a push o in-app si tiene la app.',
    fuente=f'Fuente: Braze, patrón de respuesta por persona (E7b), enero a septiembre 2026: {T/1e6:.1f} M personas, {TB/1e3:.0f} mil se dieron de baja del email. Gasto: WhatsApp a 1.00 MXN por entregado, email a 0.05 MXN por enviado. No hay cruce de tema por patrón; se pide en la extracción E7d.',
    svg=s.svg()))
