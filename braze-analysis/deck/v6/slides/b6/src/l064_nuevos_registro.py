"""Lámina 64 (ronda 2): cada punto es una campaña promocional de correo (50 mil o más enviados, E1): clic contra bajas por cada mil correos.
Azul = campañas de registro (terminar el registro de KCash o crear cuenta de KPay); azul claro = otras campañas a nuevos; gris = el resto.
Líneas = mediana de todas las campañas. E8 para la parte de las bajas de nuevos y E12 para la baja por antigüedad."""
from tramos import *

REG = r'LeftFunnel|AccountCreation|NIPconCupon|FaltaVeriff|RequestInfo'
e = load_e1()
g = por_campana(e, ('email',)); g = g[(g.env >= 5e4) & (g.dl > 0) & (g.tipo == 'promocional o lifecycle') & (g.resp > 0) & (g.baja > 0)].copy()
g['reg'] = g.familia.str.contains(REG); g['nue'] = g.grupo.eq('nuevos') & ~g.reg; g['nom'] = g.familia.map(nombre)
mc, mb = g.resp.median(), g.baja.median()
rg = g[g.reg]; arr = int(((rg.resp > mc) & (rg.baja > mb)).sum())
gr = e[e.canal == 'email'].groupby('grupo').agg(d=('email_delivery', 'sum'), c=('email_click', 'sum'), u=('email_unsubscribe', 'sum'))
gr['clic'] = 100 * gr.c / gr.d; gr['baja'] = 1000 * gr.u / gr.d
_, res, l = datos(1)
kc = l[l.clave.str.contains(r'LeftFunnel-Retargeting_(?:Veriff|PersonalInfo|NIP)$')]  # misma regla que las láminas 59 y 79
preg = 100 * kc.usuarios.sum() / res.usuarios
e12 = pd.read_csv(D / 'e12_antiguedad.csv')
a = e12[(e12.canal == 'email') & ~e12.banda_antiguedad.str.startswith('0. alta')].groupby('banda_antiguedad')[['envios', 'bajas_email_eventos']].sum()
a['b'] = 1000 * a.bajas_email_eventos / a.envios
print(len(g), len(rg), arr, mc, mb, preg, a.b.round(2).to_dict())

s = SVG('Cada punto es una campaña promocional de correo: clic contra bajas por cada mil correos; campañas de registro en azul')
s.t(0, 14, f'Clic contra bajas, por campaña de correo ({len(g)} campañas promocionales)', 12, INK, w=600)
s.legend([(BLUE, f'Registro: terminar registro o crear cuenta ({len(rg)})', 'dot'), (BLUEL, 'Otras campañas a nuevos', 'dot'), (M1, 'Resto', 'dot')], 0, 24, size=11)
X0, X1, Y0, Y1 = 46, 770, 56, 362
xs = logmap(0.02, 12, X0, X1); ys = logmap(0.3, 40, Y1, Y0)
for v in (0.3, 1, 3, 10, 30):
    s.line(X0, ys(v), X1, ys(v)); s.t(X0 - 6, ys(v) + 4, fmt(v), 11, SEC, 'end')
for v in (0.03, 0.1, 0.3, 1, 3, 10):
    s.line(xs(v), Y0, xs(v), Y1); s.t(xs(v), Y1 + 16, f'{fmt(v)} %', 11, SEC, 'middle')
s.t(X1, Y1 + 32, 'Clic del correo (escala logarítmica)', 11, SEC, 'end')
s.t(X0 - 30, Y0 - 8, 'Bajas por cada mil correos', 11, SEC)
s.line(xs(mc), Y0, xs(mc), Y1, INK, 1); s.line(X0, ys(mb), X1, ys(mb), INK, 1)
s.t(xs(mc) + 4, Y1 - 6, f'mediana {mc:.2f} %', 10.5, INK, 'start', 600, halo=True)
s.t(xs(0.12), ys(mb) + 16, f'mediana {mb:.1f} bajas', 10.5, INK, 'end', 600, halo=True)
s.t(X1 - 2, Y0 + 12, 'Responden más y se dan de baja más', 11, BLUE, 'end', 600, halo=True)
for _, q in g.sort_values(['reg', 'nue']).iterrows():
    col = BLUE if q.reg else BLUEL if q.nue else M2
    s.circle(xs(q.resp), ys(q.baja), 2.5 + 8 * math.sqrt(q.env / g.env.max()), col, extra=' fill-opacity="0.85"')
LB = {'Verificar identidad': (24, -40, 'start'), 'Completar datos': (30, 40, 'start'), 'Poner NIP': (-30, -36, 'end'),
      'Crear cuenta KPay': (24, 62, 'start'), 'Compra a meses a nuevos': (-14, 18, 'end'), 'Tasa 0 a registrados': (-12, 18, 'end'), 'Lanzamiento BillPay': (-12, -10, 'end')}
for n, (dx, dy, an) in LB.items():
    c = g[g.nom == n]
    if not len(c): continue
    q = c.sort_values('env').iloc[-1]
    etiqueta(s, xs(q.resp), ys(q.baja), n, dx, dy, an)
s.t(0, 414, 'Campañas promocionales de correo con 50 mil o más enviados. Tamaño: enviados. Escalas logarítmicas.', 10.5, SEC)

n, ld, ac = gr.loc['nuevos'], gr.loc['leads'], gr.loc['activos']
write(64, dict(
    titulo='Los nuevos son los que más responden y los que más rápido se van: el quiebre está en las campañas de registro',
    que='Recordatorios de terminar el registro de KCash y de crear cuenta de KPay; bienvenida.',
    quien='Marketing (registro de KCash) y Acquisition (cuenta de KPay), cada uno por su lado.',
    a_quien='Personas que acaban de registrarse y no terminaron.',
    lecturas=[
        f'A nuevos: {n.clic:.2f} % de clic y {n.baja:.1f} bajas por cada mil correos; a activos, {ac.clic:.2f} % y {ac.baja:.1f}.',
        f'{arr} de {len(rg)} campañas de registro responden y pierden más que la mediana; Veriff, datos y NIP, 1 de cada 5 nuevos.',
        f'Por antigüedad la baja es pareja ({a.b.min():.1f} a {a.b.max():.1f} por mil): pesa la campaña de registro, no ser nuevo.',
    ],
    causa='Marketing y Acquisition tienen cada uno su secuencia de registro, con uno o dos correos al día.',
    sowhat='Una sola secuencia de registro para KCash y KPay, con un dueño y máximo un correo al día.',
    fuente='Fuente: Braze, envíos por campaña, mes y canal (E1), días hasta la baja (E8) y antigüedad (E12), enero a septiembre 2026. Grupo por el nombre.',
    svg=s.svg()))
