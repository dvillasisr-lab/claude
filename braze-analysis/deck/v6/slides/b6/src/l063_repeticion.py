"""Lámina 63 (ronda 2): cada punto es una campaña promocional de correo en un mes (E1, más de mil personas). Mensajes de la misma campaña
por persona en el mes contra clic (panel 1) y contra bajas por cada mil personas (panel 2), misma escala horizontal. Gris = ofertas,
verde = recordatorios de algo empezado; línea negra = mediana de las ofertas por tramo (1, 2, 3 a 4, 5 o más) y recta con R²."""
from comun import *

e = load_e1(); e['gg'] = e.communication_name.map(gan_g)
x = e[(e.canal == 'email') & (e.usuarios_aprox > 1000) & (e.tipo == 'promocional o lifecycle') & (e.email_delivery > 0)].copy()
x['t'] = x.envios / x.usuarios_aprox; x['clic'] = 100 * x.email_click / x.email_delivery; x['bmp'] = 1000 * x.email_unsubscribe / x.usuarios_aprox
x['rec'] = x.gg == 'recordatorio'; x['nom'] = x.familia.map(nombre)
x['band'] = np.select([x.t < 1.5, x.t < 2.5, x.t < 4.5], ['1', '2', '3 a 4'], '5 o más')
o = x[~x.rec]
BANDS = [('1', 1), ('2', 2), ('3 a 4', 3.4), ('5 o más', 5.6)]
md = o.groupby('band')[['clic', 'bmp']].median()
oo = o[(o.clic > 0) & (o.bmp > 0)]
fc = recta(np.log10(oo.t), np.log10(oo.clic)); fb = recta(np.log10(oo.t), np.log10(oo.bmp))
mr = x[x.rec].groupby('band')[['clic', 'bmp']].median()
def ex(fm, mes):
    q = x[(x.familia == fm) & x.mes.str.startswith(mes)]; return q.t.iloc[0], q.clic.iloc[0], q.bmp.iloc[0]
print(len(o), len(x) - len(o), md.round(2).to_dict(), fc, fb, mr.round(2).to_dict())

s = SVG('Cada punto es una campaña de correo en un mes: mensajes por persona contra clic y contra bajas por cada mil personas')
s.legend([(M1, f'Oferta ({len(o)} campaña-mes)', 'dot'), (GREEN, f'Recordatorio de algo empezado ({len(x)-len(o)})', 'dot'), (INK, 'Mediana de las ofertas', 'line')], 0, 4, size=11)
PAN = [('clic', 'Clic del correo', logmap(0.01, 20, 362, 56), (0.01, 0.03, 0.1, 0.3, 1, 3, 10), ' %', fc, 0),
       ('bmp', 'Bajas por cada mil personas', logmap(0.05, 100, 362, 56), (0.1, 0.3, 1, 3, 10, 30, 100), '', fb, 400)]
for col, h, ys, ticks, u, fit, x0 in PAN:
    X0, X1 = x0 + 40, x0 + 372
    xs = logmap(0.85, 8, X0, X1)
    s.t(x0, 36, h, 12, INK, w=600)
    s.t(X1, 36, f'R² = {fit[2]:.2f}', 11, SEC, 'end')
    for v in ticks:
        s.line(X0, ys(v), X1, ys(v)); s.t(X0 - 5, ys(v) + 4, f'{fmt(v)}{u}', 10.5, SEC, 'end')
    for v in (1, 2, 3, 5, 8):
        s.line(xs(v), 56, xs(v), 362); s.t(xs(v), 377, f'{v}', 10.5, SEC, 'middle')
    s.t(X1, 392, 'Mensajes de la campaña por persona en el mes', 10.5, SEC, 'end')
    rng = np.random.default_rng(3)
    for _, q in x.sort_values('rec').iterrows():
        v = q[col]
        if v <= 0: continue
        s.circle(xs(q.t * rng.uniform(0.985, 1.015)), ys(v), 3.2 if q.rec else 2.4, GREEN if q.rec else M1, ring=False, extra=' fill-opacity="0.7"')
    pts = ' '.join(f'{xs(c):.1f},{ys(md.loc[b, col]):.1f}' for b, c in BANDS)
    s.raw(f'<polyline points="{pts}" fill="none" stroke="{INK}" stroke-width="2.5"/>')
    for b, c in BANDS:
        v = md.loc[b, col]; s.circle(xs(c), ys(v), 4, INK)
        s.t(xs(c), ys(v) - 9, f'{v:.2f}{u}' if col == 'clic' else f'{v:.1f}', 11, INK, 'middle', 700, halo=True)
    q = x[x.nom == 'Verificar identidad'].sort_values('t').iloc[-1]
    etiqueta(s, xs(q.t), ys(q[col]), 'Verificar identidad', -12, -22 if col == 'clic' else 26, 'end', sub=f'{q.t:.1f} al mes')
s.t(0, 414, 'Mensajes al mes: envíos de la campaña en el mes entre personas que la recibieron. Escalas logarítmicas.', 10.5, SEC)

write(63, dict(
    titulo='Repetir una oferta en el mes no sube el clic, pero con cinco o más correos las bajas por persona se triplican',
    que='Promociones repetidas en el mes: Tasa 0, referidos, Comercio del día, rescates.',
    quien='Marketing y Product Growth en correo; Sales y Marketing con Comercio del día en push.',
    a_quien='Leads, registrados y clientes recurrentes de KPay.',
    lecturas=[
        f'Clic mediano de la oferta: {md.loc["1","clic"]:.2f} % con un correo al mes, {md.loc["2","clic"]:.2f} % con dos y {md.loc["5 o más","clic"]:.2f} % con cinco o más.',
        f'Bajas por cada mil personas: {md.loc["1","bmp"]:.1f} con un correo, {md.loc["2","bmp"]:.1f} con dos y {md.loc["5 o más","bmp"]:.1f} con cinco o más.',
        f'El recordatorio de verificar identidad llega {q.t:.1f} veces al mes: {q.bmp:.0f} bajas por cada mil personas.',
    ],
    causa='No hay límite de mensajes por persona por campaña: cada equipo repite su oferta sin ver si abrió la anterior.',
    sowhat='Máximo dos mensajes por campaña al mes, y el segundo solo a quien no abrió el primero.',
    fuente='Fuente: Braze, envíos por campaña, mes y canal (E1), enero a septiembre 2026; campañas promocionales de correo con más de mil personas en el mes.',
    svg=s.svg()))
