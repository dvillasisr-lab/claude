"""Lámina 58 (ronda 2): franja de puntos por grupo de audiencia; cada punto es una campaña de push (50 mil o más enviados, E1).
Apertura en escala logarítmica; verde = recordatorio de algo empezado, azul = Tasa 0, gris = otras ofertas; raya negra = mediana del grupo.
Al lado de cada grupo, de cada 100 que reciben el correo de la campaña, cuántos reciben su push (campañas con correo y push el mismo mes)."""
from comun import *

e = load_e1(); e['tema'] = e.communication_name.map(gancho_of)
g = por_campana(e, ('push notification',))
g['tema'] = g.familia.map(gancho_of); g['nom'] = g.familia.map(nombre)
g = g[(g.b >= 5e4) & (g.tipo == 'promocional o lifecycle')]
G = [('nuevos', 'Nuevos'), ('activos', 'Activos y recurrentes'), ('leads', 'Leads y registrados'), ('ex clientes', 'Ex clientes inactivos'), ('nunca activaron', 'Leads que nunca activaron')]
x = e[e.canal.isin(['email', 'push notification'])]
pv = x.pivot_table(index=['grupo', 'familia', 'mes'], columns='canal', values='usuarios_aprox', aggfunc='sum').fillna(0)
both = pv[(pv['email'] >= 20000) & (pv['push notification'] > 0)].copy()   # misma regla que la lámina 54: mediana por campaña y mes
both['push'] = 100 * both['push notification'] / both.email
al = both.groupby('grupo')[['push']].median()
pp = e[e.canal == 'push notification'].groupby(['grupo', 'tema']).agg(env=('pn_send', 'sum'), op=('pn_open', 'sum')); pp['ap'] = 100 * pp.op / pp.env
k = pd.read_csv(H / 'muestra_k_abren_vs_no_abren.csv').set_index(['fam', 'canal'])
b211 = k.loc[('Lending-KCash-B0211-CANVAS-Nuevos_RegistradosPay-Tasa0-N/A', 'push notification')]
med = g.groupby('grupo').resp.median()
print(g.groupby('grupo').size().to_dict(), med.round(2).to_dict(), al.push.round(0).to_dict())

s = SVG('Cada punto es una campaña de push: apertura por grupo de audiencia; recordatorios en verde, Tasa 0 en azul, otras ofertas en gris')
s.t(0, 14, 'Apertura de cada campaña de push, por grupo de audiencia', 12, INK, w=600)
s.legend([(GREEN, 'Recordatorio de algo empezado', 'dot'), (BLUE, 'Tasa 0', 'dot'), (M1, 'Otras ofertas', 'dot'), (INK, 'Mediana del grupo', 'rect')], 0, 24, size=11)
X0, X1 = 170, 660
xs = logmap(0.05, 30, X0, X1)
TOP, RH = 74, 60
s.t(780, 62, 'reciben push', 10.5, SEC, 'end'); s.t(780, 50, 'Mediana: de cada 100 con correo,', 10.5, SEC, 'end')
for v in (0.1, 0.3, 1, 3, 10, 30):
    s.line(xs(v), TOP - 8, xs(v), TOP + RH * 5 - 8); s.t(xs(v), TOP + RH * 5 + 8, f'{fmt(v)} %', 11, SEC, 'middle')
s.line(xs(0.75), TOP - 8, xs(0.75), TOP + RH * 5 - 8, INK, 1); s.t(xs(0.75) + 3, TOP - 12, 'mínimo 0.75 %', 10.5, INK)
rng = np.random.default_rng(7)
COLT = lambda t: GREEN if t == 'Recordatorio de algo empezado' else BLUE if t == 'Tasa 0' else M1
LB = {'Compra a meses a nuevos': (0, -16, 'middle'), 'Pagar compra a meses': (0, -16, 'middle'), 'Verificar identidad': (0, -16, 'middle'),
      'Tasa 0 a registrados': (-6, 22, 'end'), 'Rescate Tasa 0 a anónimos': (-8, -16, 'end'), 'Referidos a dormants': (-8, -16, 'end')}
for i, (gk, name) in enumerate(G):
    yc = TOP + RH * i + 18
    d = g[g.grupo == gk]
    s.t(0, yc - 2, name, 12, INK, w=600); s.t(0, yc + 12, f'{len(d)} campañas', 10.5, SEC)
    s.line(0, yc + 32, 780, yc + 32, GRID)
    for _, q in d.sort_values('tema', key=lambda c: c == 'Recordatorio de algo empezado').iterrows():
        y = yc + rng.uniform(-12, 12)
        s.circle(xs(q.resp), y, 2.5 + 7 * math.sqrt(q.b / g.b.max()), COLT(q.tema), ring=True, extra=' fill-opacity="0.85"')
        if q.nom in LB and q.b == d[d.nom == q.nom].b.max():
            dx, dy, an = LB[q.nom]; etiqueta(s, xs(q.resp), y, q.nom, dx, dy, an)
    m = med[gk]; s.rect(xs(m) - 1.5, yc - 15, 3, 30, INK)
    s.t(xs(m) + 5, yc + 26, f'{m:.2f} %', 10.5, INK, 'start', 600, halo=True)
    if gk in al.index: s.t(780, yc + 4, f'{al.loc[gk, "push"]:.0f}', 13, INK, 'end', 600)
s.t(X1, TOP + RH * 5 + 24, 'Apertura del push (escala logarítmica)', 10.5, SEC, 'end')
s.t(0, 414, 'Campañas promocionales de push con 50 mil o más enviados. Tamaño: enviados. Grupo y tema según el nombre de la campaña.', 10.5, SEC)

L, A = pp.loc['leads'], pp.loc['activos']
write(58, dict(
    titulo='El push funciona cuando recuerda algo que la persona empezó; como oferta, casi nadie lo abre',
    que='Ofertas: Tasa 0, referidos, Comercio del día. Recordatorios: registro, pago a meses.',
    quien='Marketing (B0171, B0326, B0000) y Product Growth (B0211, B0301).',
    a_quien='Ofertas a leads y registrados; recordatorios a quien está en registro o paga a meses.',
    lecturas=[
        f'Mismo grupo, otro mensaje: en leads el recordatorio abre {L.loc["Recordatorio de algo empezado","ap"]:.1f} % y la Tasa 0 {L.loc["Tasa 0","ap"]:.2f} %.',
        f'Sin app no hay push: de cada 100 leads que nunca activaron con correo, {al.loc["nunca activaron","push"]:.0f} reciben push; en activos, {al.loc["activos","push"]:.0f}.',
        f'La Tasa 0 a registrados mueve a quien la abre (convierte {b211.conv_abren:.1f} % contra {b211.conv_no_abren:.2f} %); la abre 1 de cada 200.',
    ],
    causa='Usamos el push para ofertas a listas enteras, aunque muchos no tienen la app, y no para recordar lo empezado.',
    sowhat='Push solo a quien tiene la app y como recordatorio de lo empezado, no como oferta repetida.',
    fuente='Fuente: Braze, envíos por campaña, mes y canal (E1) y quien abre contra quien no (E7c), enero a septiembre 2026. Grupo y tema por el nombre.',
    svg=s.svg()))
