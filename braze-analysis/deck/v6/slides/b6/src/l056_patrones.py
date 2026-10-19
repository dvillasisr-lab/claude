"""Lámina 56 (ronda 2): cada punto es un patrón de respuesta (las 16 combinaciones de canales por los que responde una persona, E7b).
Dos paneles con la misma escala vertical (% que se dio de baja del correo): contra % que convirtió y contra mensajes por persona.
Azul = responde por dos o más canales; gris = por uno o ninguno. Tamaño = personas. Línea = baja promedio de toda la base."""
from comun import *

j = pd.read_csv(H / 'muestra_j_patron_respuesta.csv')
j['n'] = j[['resp_email', 'resp_push', 'resp_wa', 'resp_inapp']].sum(axis=1)
T, TC, TB, TM = j.usuarios.sum(), j.usuarios_con_conversion.sum(), j.usuarios_con_baja_email.sum(), j.msgs.sum()
NOM = {(0, 0, 0, 0): 'No responde a nada', (0, 0, 1, 0): 'Solo WhatsApp', (0, 0, 0, 1): 'Solo in-app', (1, 0, 0, 0): 'Solo correo',
       (1, 0, 1, 0): 'Correo y WhatsApp', (1, 1, 1, 1): 'Los cuatro canales', (0, 1, 1, 1): 'Push, WhatsApp e in-app'}
j['nom'] = [NOM.get(k) for k in zip(j.resp_email, j.resp_push, j.resp_wa, j.resp_inapp)]
dos = j[j.n >= 2]; p2u, p2c, p2m = 100 * dos.usuarios.sum() / T, 100 * dos.usuarios_con_conversion.sum() / TC, 100 * dos.msgs.sum() / TM
avg = 100 * TB / T
r = {k: j[j.nom == k].iloc[0] for k in NOM.values()}
print(round(p2u, 1), round(p2c, 1), round(p2m, 1), round(avg, 2))

s = SVG('Cada punto es una forma de responder: porcentaje que se dio de baja del correo contra porcentaje que convirtió y contra mensajes por persona')
j['lector'] = (j.resp_email == 1) & (j.resp_push == 0) & (j.resp_inapp == 0)
s.legend([(GREEN, 'Lee el correo, sin push ni in-app', 'dot'), (BLUE, 'Dos o más canales', 'dot'), (M1, 'Un canal o ninguno', 'dot'), (INK, f'Baja promedio: {avg:.1f} %', 'line')], 0, 4, size=11)
ys = lambda v: 352 - (352 - 60) * v / 18
rad = lambda u: max(4, 22 * math.sqrt(u / j.usuarios.max()))
PAN = [('convierten_pct', 'Contra % de personas que convirtió', logmap(0.05, 100, 40, 372), ((0.1, '0.1 %'), (1, '1 %'), (10, '10 %'), (100, '100 %')), '% que convirtió (escala logarítmica)', 0),
       ('msgs_por_usuario', 'Contra mensajes por persona en nueve meses', lambda v: 440 + 330 * v / 280, ((0, '0'), (100, '100'), (200, '200')), 'Mensajes recibidos por persona', 400)]
LB = {'convierten_pct': {'No responde a nada': (26, -4, 'start'), 'Solo WhatsApp': (-12, -12, 'end'), 'Solo correo': (0, -14, 'middle'),
                         'Correo y WhatsApp': (10, -12, 'start'), 'Los cuatro canales': (-6, -14, 'end'), 'Push, WhatsApp e in-app': (-10, 20, 'end')},
      'msgs_por_usuario': {'Solo correo': (10, -10, 'start'), 'Correo y WhatsApp': (10, 4, 'start'), 'Solo WhatsApp': (14, -16, 'start'),
                           'Los cuatro canales': (-6, -14, 'end'), 'No responde a nada': (26, -4, 'start')}}
for col, h, xs, ticks, xl, x0 in PAN:
    X0, X1 = x0 + 40, x0 + 372
    s.t(x0, 40, h, 12, INK, w=600)
    for v in (0, 5, 10, 15):
        s.line(X0, ys(v), X1, ys(v)); s.t(X0 - 5, ys(v) + 4, f'{v} %', 10.5, SEC, 'end')
    for v, lab in ticks:
        s.line(xs(v), 60, xs(v), 352); s.t(xs(v), 368, lab, 10.5, SEC, 'middle')
    s.t(X1, 384, xl, 10.5, SEC, 'end')
    s.line(X0, ys(avg), X1, ys(avg), INK, 1)
    for _, q in j.sort_values('usuarios', ascending=False).iterrows():
        s.circle(xs(q[col]), ys(q.baja_pct), rad(q.usuarios), GREEN if q.lector else BLUE if q.n >= 2 else M1, extra=' fill-opacity="0.9"')
    for k, (dx, dy, an) in LB[col].items():
        q = r[k]; etiqueta(s, xs(q[col]), ys(q.baja_pct), k, dx, dy, an, sub=f'{mil(q.usuarios)} · {q.baja_pct:.1f} %')
s.t(0, 400, 'Responder: clic en correo, abrir push, leer WhatsApp o clic en in-app, de enero a septiembre. Tamaño: personas.', 10.5, SEC)
s.t(0, 414, 'Convirtió: Braze registró un crédito otorgado. Eje vertical: % que se dio de baja del correo.', 10.5, SEC)

n4, wa, ne, ewa = r['Los cuatro canales'], r['Solo WhatsApp'], r['Solo correo'], r['Correo y WhatsApp']
write(56, dict(
    titulo='Quien responde por varios canales es el cliente activo; quien solo lee el correo es el que más se da de baja',
    que='Todo lo que mandamos; el multicanal abre sobre todo recordatorios y avisos de pago.',
    quien='Todos los equipos.',
    a_quien=f'{T/1e6:.1f} M personas según por qué canales responden.',
    lecturas=[
        f'Dos o más canales: {p2u:.0f} % de las personas, {p2c:.0f} % de quienes convirtieron y {p2m:.0f} % de los mensajes.',
        f'Solo correo: {mil(ne.usuarios)} personas, {ne.baja_pct:.1f} % se dio de baja con {ne.msgs_por_usuario:.0f} mensajes cada una.',
        f'Solo WhatsApp: {mil(wa.usuarios)} personas, {wa.convierten_pct:.0f} % convirtió y {wa.pct_costo:.0f} % del gasto.',
    ],
    causa='Mandamos lo mismo por todos los canales a todos, sin mirar por cuál responde cada persona.',
    sowhat='Al multicanal, pocos mensajes; al lector de correo, menos correos; al de WhatsApp, push si tiene app.',
    fuente=f'Fuente: Braze, patrón de respuesta por persona (E7b), enero a septiembre 2026: {T/1e6:.1f} M personas, {TB/1e3:.0f} mil se dieron de baja del correo. WhatsApp a 1.00 MXN por entregado.',
    svg=s.svg()))
