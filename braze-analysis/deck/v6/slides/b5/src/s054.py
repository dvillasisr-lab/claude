"""Lámina 54 (ronda 2). Arriba: 3 cifras de quién tiene la app (E7b). Gráfica: dos paneles iguales (push | in-app). Cada punto es una
campaña en un mes (con 20 mil o más personas en su correo y algún push): de cada 100 que reciben su correo, cuántas reciben su push y
cuántas ven su in-app (E1, personas aproximadas). Raya = mediana del grupo. Arriba de 100 se dibuja en 100."""
import pandas as pd
from b5_svg import *
from b5_datos import pv

E7, E9 = D['e7b'], D['e9b']
e17 = pd.read_csv('/home/user/claude/braze-analysis/data/e17_contactable.csv'); p17 = e17[e17.canal == 'push notification']
ap_un = {k: 100 * g.respuestas.sum() / g.envios.sum() for k, g in p17.groupby('app_uninstall')}
b = pv[(pv['email'] >= 20000) & (pv['push notification'] > 0)].copy()
b['rp'] = 100 * b['push notification'] / b.email; b['ri'] = 100 * b['in-app'] / b.email
b = b.reset_index()
ORD = [('activos', 'Activos y recurrentes'), ('nuevos', 'Nuevos y onboarding'), ('leads', 'Leads y registrados'),
       ('ex', 'Ex clientes inactivos'), ('nunca', 'Leads que nunca activaron')]
tot = E7['tot']['usuarios']
S = Svg('Arriba, tres cifras de quién tiene la app. Abajo, dos paneles: cada punto es una campaña en un mes; de cada 100 personas que reciben su correo, cuántas reciben su push y cuántas ven su in-app, por grupo, con la mediana.')
kpis(S, [(f'{M(E7["push_o_inapp"])} M', f'abrieron un push o un in-app:', f'{100*E7["push_o_inapp"]/tot:.0f} % de {M(tot)} M personas'),
         (f'{M(E7["abre_push"], 2)} M', 'abrieron al menos un push', 'en nueve meses'),
         (f'{100*E7["push_o_inapp_conv"]/E7["tot"]["conv"]:.0f} %', 'de quienes convirtieron', 'están entre esos 3.2 M')])
S.t(0, 72, 'De cada 100 que reciben el correo de una campaña; cada punto, una campaña en un mes', 12, INK, w=600)
S.t(W, 72, 'Raya: mediana', 10.5, SEC, 'end')
PAN = [('rp', 'Les llega su push', 172, 455), ('ri', 'Ven su in-app', 485, 766)]
TOP, RH = 104, 54
MED = {}
for k, tit, X0, X1 in PAN:
    sx = lambda v, X0=X0, X1=X1: X0 + (X1 - X0) * min(v, 100) / 100
    S.t(X0, 92, tit, 11.5, INK, w=600)
    for v in (0, 50, 100):
        S.line(sx(v), TOP - 6, sx(v), TOP + RH * len(ORD) - 14)
        S.t(sx(v), TOP + RH * len(ORD), f'{v}', 10.5, SEC, 'middle')
    for i, (g, lab) in enumerate(ORD):
        yc = TOP + RH * i + 14
        cold = g in ('ex', 'nunca')
        d = b[b.g == g].sort_values(k)
        offs = swarm([sx(v) for v in d[k]], 2.8, 16)
        for v, o in zip(d[k], offs):
            S.circle(sx(v), yc + o, 2.8, BLUE if cold else MARK, '#FFFFFF', 0.6)
        m = med(list(d[k])); MED[(g, k)] = m
        S.line(sx(m), yc - 18, sx(m), yc + 18, INK, 2.5)
        S.t(sx(m) + 5, yc - 13, f'{m:.0f}', 11, INK, 'start', 700, halo=True)
for i, (g, lab) in enumerate(ORD):
    yc = TOP + RH * i + 14
    S.t(150, yc + 2, lab, 11.5, INK, 'end', 600 if g in ('ex', 'nunca') else 400)
    S.t(150, yc + 16, f'{(b.g == g).sum()} campañas en un mes', 10.5, SEC, 'end')
SVG = S.done()

guarda(54, dict(
    kind='grafica',
    titulo='Solo una de cada seis personas abrió un push o un in-app en nueve meses: al menos ellas tienen la app',
    que='Push e in-app de recuperación y promociones: los canales que no cuestan',
    quien='Todos los equipos; Marketing manda los push de oferta más grandes',
    a_quien='Activos, leads, ex clientes y leads que nunca activaron; sin app no hay push ni in-app',
    lecturas=[
        f'{M(E7["push_o_inapp"])} M personas es lo mínimo con app; a lo más, el push llega a 1.5 a 2.3 M al mes.',
        f'Ex clientes: de cada 100 con correo, a {MED[("ex","rp")]:.0f} les llega el push y {MED[("ex","ri")]:.0f} ven el in-app (mediana por campaña).',
        f'Leads que nunca activaron: {MED[("nunca","rp")]:.0f} y {MED[("nunca","ri")]:.0f}; activos: {MED[("activos","rp")]:.0f} y {MED[("activos","ri")]:.0f}.',
    ],
    causa=f'No hay dato confiable de app: el push a quien aparece con la app desinstalada abre {ap_un[True]:.2f} %, como el resto.',
    sowhat='Pedir a Datos tres atributos diarios en Braze: tiene app, entró en 30 días y tiene push activado.',
    fuente='Fuente: Braze E7b (respuesta por persona), E4a (personas por canal al mes), E1 (personas por campaña y mes, sumadas: es proporción, no conteo) y E17, enero a septiembre 2026.',
    svg=SVG,
))
print(MED)
