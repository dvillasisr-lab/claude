"""Lámina 64: los nuevos son los que más responden y los que más rápido se van. Izquierda: por grupo de audiencia (por el nombre de la
campaña, E1) clic del correo contra bajas por cada mil entregados, tamaño = correos. Derecha: nuevos que se dieron de baja (E8, muestra L),
por equipo: días hasta la baja (mediana) contra parte de las bajas. E12: bajas por antigüedad."""
import math
from tramos import *

e = load_e1()
em = e[e.canal == 'email']
G = [('nuevos', 'Nuevos'), ('leads', 'Leads y registrados recientes'), ('activos', 'Activos y recurrentes'), ('nunca activaron', 'Leads que nunca activaron'), ('ex clientes', 'Ex clientes inactivos')]
gr = em.groupby('grupo').agg(env=('envios', 'sum'), d=('email_delivery', 'sum'), c=('email_click', 'sum'), u=('email_unsubscribe', 'sum'))
gr['clic'] = 100 * gr.c / gr.d; gr['baja'] = 1000 * gr.u / gr.d
bd, res, l = datos(1)
tot = res.usuarios
tm = l.groupby('team').apply(lambda d: pd.Series({'p': 100 * d.usuarios.sum() / tot, 'dia': wmed(d), 'u': d.usuarios.sum()}))
reg = l[l.clave.str.contains(r'LeftFunnel|AccountCreation|NIPconCupon|FaltaVeriff|RequestInfo')]
preg = 100 * reg.usuarios.sum() / tot
e12 = pd.read_csv(D / 'e12_antiguedad.csv')
a = e12[(e12.canal == 'email') & ~e12.banda_antiguedad.str.startswith('0. alta')].groupby('banda_antiguedad')[['envios', 'bajas_email_eventos', 'respuestas']].sum()
a['b'] = 1000 * a.bajas_email_eventos / a.envios; a['r'] = 100 * a.respuestas / a.envios
b301 = l.set_index('clave').loc['Marketing-KCash-B0301-CANVAS-Active-NuevosRetargeting_Installments_SP']
p301 = resp(e[(e.familia == 'Marketing-KCash-B0301-CANVAS-Active-NuevosRetargeting_Installments_SP') & (e.canal == 'push notification')], 'push notification')
print(gr.round(2)); print(tm.round(1)); print(preg, a.round(2), b301.usuarios, b301.dias_mediana, p301)

s = SVG('Por grupo de audiencia, clic del correo contra bajas por cada mil correos; y para los nuevos, días hasta la baja contra parte de las bajas, por equipo')
s.t(0, 16, 'Correo por grupo de audiencia, enero a septiembre', 12, INK, w=600)
s.t(0, 32, 'Tamaño: correos enviados al grupo', 10.5, SEC)
X0, X1, Y0, Y1 = 44, 400, 60, 340
xs = lambda v: X0 + (X1 - X0) * v / 1.4
ys = lambda v: Y1 - (Y1 - Y0) * v / 8
for v in (0, 2, 4, 6, 8):
    s.line(X0, ys(v), X1, ys(v)); s.t(X0 - 6, ys(v) + 4, f'{v}', 11, SEC, 'end')
for v in (0, 0.4, 0.8, 1.2):
    s.line(xs(v), Y0, xs(v), Y1); s.t(xs(v), Y1 + 16, f'{v:.1f} %', 11, SEC, 'middle')
s.t(X0 - 30, Y0 - 10, 'Bajas por cada mil correos', 11, SEC)
s.t(X1, Y1 + 32, 'Clic del correo', 11, SEC, 'end')
vmax = gr.loc[[g for g, _ in G], 'env'].max()
POS = {'nuevos': (-16, -12, 'end'), 'leads': (16, -4, 'start'), 'activos': (16, 6, 'start'), 'nunca activaron': (-12, -14, 'end'), 'ex clientes': (0, 30, 'middle')}
for g, name in G:
    q = gr.loc[g]; r = max(5, 26 * math.sqrt(q.env / vmax)); x, y = xs(q.clic), ys(q.baja)
    s.circle(x, y, r, BLUE if g == 'nuevos' else M1)
    dx, dy, an = POS[g]
    s.t(x + dx, y + dy, name, 11.5, INK, an, 600, halo=True)
    s.t(x + dx, y + dy + 13, f'{q.clic:.2f} % · {q.baja:.1f} bajas · {q.env/1e6:.0f} M', 10.5, SEC, an, halo=True)
# derecha: nuevos por equipo
PX0, PX1 = 470, 760
s.t(PX0 - 30, 16, 'Nuevos que se dieron de baja, por equipo', 12, INK, w=600)
s.t(PX0 - 30, 32, 'Días hasta la baja (mediana) y parte de las bajas', 10.5, SEC)
px = lambda d: PX0 + (PX1 - PX0) * math.log10(max(d, 1)) / 2.1
py = lambda p: Y1 - (Y1 - Y0) * p / 50
for v in (0, 10, 20, 30, 40, 50):
    s.line(PX0, py(v), PX1, py(v)); s.t(PX0 - 6, py(v) + 4, f'{v} %', 11, SEC, 'end')
for d in (1, 3, 10, 30, 100):
    s.line(px(d), Y0, px(d), Y1); s.t(px(d), Y1 + 16, f'{d}', 11, SEC, 'middle')
s.t(PX1, Y1 + 32, 'Días desde el primer correo', 11, SEC, 'end')
TP = {'Acquisition': (10, 4, 'start'), 'Marketing': (0, -14, 'middle'), 'Others': (0, 22, 'middle'), 'Product Growth': (-12, -8, 'end'), 'Collections': (0, -12, 'middle')}
for t_, (dx, dy, an) in TP.items():
    q = tm.loc[t_]; x, y = px(q.dia), py(q.p)
    s.circle(x, y, 6.5, BLUE if t_ in ('Acquisition', 'Marketing') else M1)
    s.t(x + dx, y + dy, f'{t_} {q.p:.0f} %, día {q.dia:.0f}', 11.5, INK, an, 600, halo=True)
s.t(0, 400, 'Grupo según el nombre de la campaña. Nuevos: primer correo de febrero en adelante. Bajas por cada mil correos entregados.', 10.5, SEC)
s.t(0, 414, 'Azul a la derecha: equipos que pierden al nuevo en la primera semana, con sus campañas de registro.', 10.5, SEC)

n, ld, ac = gr.loc['nuevos'], gr.loc['leads'], gr.loc['activos']
write(64, dict(
    titulo='Los nuevos son los que más responden y los que más rápido se van: el quiebre está en las campañas de registro',
    que='Bienvenida, recordatorios para terminar el registro y compras a meses a nuevos.',
    quien='Marketing (registro de KCash), Acquisition (crear cuenta de KPay), NewProducts (BillPay) y Product Growth (Tasa 0 a registrados).',
    a_quien='Nuevos y personas en registro: su primer correo llegó de febrero en adelante.',
    lecturas=[
        f'Campañas a nuevos: {n.clic:.2f} % de clic y {n.baja:.1f} bajas por cada mil correos; a leads y registrados, {ld.clic:.2f} % y {ld.baja:.1f}; a activos, {ac.clic:.2f} % y {ac.baja:.1f}.',
        f'Lo que coincide es el registro: verificar identidad, completar datos, poner NIP y crear cuenta suman {preg:.0f} % de las bajas de nuevos, en la primera semana. Acquisition los pierde al día {tm.loc["Acquisition","dia"]:.0f} y Marketing al {tm.loc["Marketing","dia"]:.0f}; Product Growth, al {tm.loc["Product Growth","dia"]:.0f}.',
        f'Por antigüedad la baja es pareja ({a.b.min():.1f} a {a.b.max():.1f} por cada mil correos) aunque el clic baja de {a.r.iloc[0]:.1f} % a {a.r.iloc[-1]:.2f} %: lo que sube la baja es estar en una campaña de registro, no ser nuevo.',
    ],
    causa=f'Marketing y Acquisition tienen cada uno su propia secuencia de registro y no hay una bienvenida única. Antes de irse, el nuevo ya recibió correos de {res.familias_prom:.1f} campañas distintas, y las de registro llegan uno o dos al día.',
    sowhat='Una sola secuencia de registro para KCash y KPay, con un dueño y máximo un correo al día.',
    fuente=f'Fuente: Braze, E1 (correo por campaña y mes), E8 (días hasta la baja de nuevos) y E12 (antigüedad), enero a septiembre 2026. Ejemplo: compras a meses a nuevos de Marketing (B0301), {p301:.1f} % de apertura del push pero {b301.usuarios/1e3:.0f} mil bajas al día {b301.dias_mediana}.',
    svg=s.svg()))
