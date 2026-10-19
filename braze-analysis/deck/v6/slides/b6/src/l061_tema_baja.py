"""Lámina 61 (ronda 2): cada punto es una campaña de correo (50 mil o más enviados, E1): correos enviados contra bajas por cada mil
correos, color por tipo (promocional contra aviso o cobranza), con la mediana de cada tipo. Parte de las bajas por tipo del día de la
baja: E8 (muestra L)."""
from tramos import *

e = load_e1()
g = por_campana(e, ('email',)); g = g[(g.env >= 50000) & (g.dl > 0) & g.tipo.notna()].copy()
g['promo'] = g.tipo == 'promocional o lifecycle'
med = g.groupby('promo').baja.median()
pu = g.groupby('promo').u.sum(); pshare = 100 * pu[True] / pu.sum()
co = {}
for k in (1, 0):
    _, res, l = datos(k)
    co[k] = 100 * l.groupby('tipo').usuarios.sum() / res.usuarios
print(len(g), med.round(2).to_dict(), round(pshare, 1), {k: v.round(1).to_dict() for k, v in co.items()})

s = SVG('Cada punto es una campaña de correo: correos enviados contra bajas por cada mil correos; promociones en azul, avisos y cobranza en gris')
s.t(0, 14, f'Bajas por cada mil correos, por campaña de correo ({len(g)} campañas con 50 mil o más enviados)', 12, INK, w=600)
s.legend([(BLUE, 'Promoción', 'dot'), (M1, 'Aviso de pago, de servicio o cobranza', 'dot')], 0, 24, size=11)
X0, X1, Y0, Y1 = 46, 770, 56, 362
xs = logmap(5e4, 4e7, X0, X1); ys = logmap(0.02, 60, Y1, Y0)
for v in (0.03, 0.1, 0.3, 1, 3, 10, 30):
    s.line(X0, ys(v), X1, ys(v)); s.t(X0 - 6, ys(v) + 4, fmt(v), 11, SEC, 'end')
for v, lab in ((1e5, '100 mil'), (3e5, '300 mil'), (1e6, '1 M'), (3e6, '3 M'), (1e7, '10 M'), (3e7, '30 M')):
    s.line(xs(v), Y0, xs(v), Y1); s.t(xs(v), Y1 + 16, lab, 11, SEC, 'middle')
s.t(X1, Y1 + 32, 'Correos enviados por la campaña en nueve meses (escala logarítmica)', 11, SEC, 'end')
rad = lambda u: 2.5 + 9 * math.sqrt(u / g.u.max())
for _, q in g.sort_values('promo').iterrows():
    s.circle(xs(q.env), ys(q.baja), rad(q.u), BLUE if q.promo else M1, extra=' fill-opacity="0.75"')
for pr, col, lab in ((True, BLUE, 'Mediana de las promociones'), (False, SEC, 'Mediana de avisos y cobranza')):
    y = ys(med[pr]); s.line(X0, y, X1, y, col, 1.2)
    s.t(X0 + 4, y - 5, f'{lab}: {med[pr]:.1f}', 11, col, 'start', 600, halo=True)
LB = {'Lanzamiento BillPay': (0, -44, 'middle'), 'Tasa 0 a registrados': (-30, 40, 'end'), 'Referidos a leads': (-30, -62, 'end'),
      'Tasa 0 a leads rezagados': (-40, -30, 'end'), 'Verificar identidad': (10, 44, 'start'), 'Confirmación de pago': (-12, 22, 'end'),
      'Cobranza BKT1': (-12, 20, 'end'), 'Rechazo por fraude': (-10, -18, 'end')}
g['nom'] = g.familia.map(nombre)
for n, (dx, dy, an) in LB.items():
    q = g[g.nom == n].sort_values('env').iloc[-1]
    etiqueta(s, xs(q.env), ys(q.baja), n, dx, dy, an, col=INK)
s.t(0, 414, 'Bajas registradas en el correo de cada campaña. Escalas logarítmicas. Tamaño del punto: bajas.', 10.5, SEC)

write(61, dict(
    titulo='Nueve de cada diez bajas llegan con un correo promocional; los avisos de pago casi no causan bajas',
    que='Lanzamiento de BillPay, recordatorios de registro, Tasa 0, referidos y descuentos.',
    quien='Marketing y Product Growth; Others con BillPay de NewProducts.',
    a_quien='Toda persona que recibe correo; 439 mil se dieron de baja en nueve meses.',
    lecturas=[
        f'{co[1]["promocional o lifecycle"]:.0f} % de las bajas de nuevos y {co[0]["promocional o lifecycle"]:.0f} % de la base vieja llegan el día de una promoción.',
        f'Una promoción típica pierde {med[True]:.1f} personas por cada mil correos; un aviso o cobranza, {med[False]:.1f}.',
        'BillPay a toda la base perdió 80 mil personas; la confirmación de pago, con 9 M correos, 3 mil.',
    ],
    causa='Las promociones salen a listas completas y se repiten sin límite; los avisos llegan solo a quien hizo algo.',
    sowhat='La baja se decide en las promociones: ahí van el límite por persona y la salida si no abre en 90 días.',
    fuente='Fuente: Braze, envíos por campaña, mes y canal (E1) y campaña del día de la baja (E8), enero a septiembre 2026. Tipo según el catálogo de campañas.',
    svg=s.svg()))
