"""Lámina 62 (ronda 2): cada punto es una campaña promocional (100 mil o más enviados), en dos paneles con la misma lógica: correo y push.
Enviados contra respuesta; verde = recordatorio de algo empezado, gris = oferta nueva; mediana de cada grupo y mínimo aceptable del canal.
Tema por el nombre con la regla de la muestra G (E1)."""
from comun import *

e = load_e1(); e['gg'] = e.communication_name.map(gan_g)
p = e[~e.grupo.isin(['cobranza', 'transaccional']) & (e.tipo == 'promocional o lifecycle')]
g = por_campana(p, ('email', 'push notification'))
g['gg'] = g.familia.map(gan_g); g['rec'] = g.gg == 'recordatorio'; g['nom'] = g.familia.map(nombre)
g = g[(g.b >= 1e5) & (g.resp > 0)]
pool = {(c, r): 100 * g[(g.canal == c) & (g.rec == r)].r.sum() / g[(g.canal == c) & (g.rec == r)].b.sum() for c in ('email', 'push notification') for r in (True, False)}
med = g.groupby(['canal', 'rec']).resp.median()
tem = {t: resp(p[(p.gg == t) & (p.canal == 'email')], 'email') for t in ('recordatorio', 'tasa0', 'descuento', 'referidos', 'lanzamiento')}
ia = {t: resp(p[(p.gg == t) & (p.canal == 'in-app')], 'in-app') for t in ('referidos',)}
print(g.groupby(['canal', 'rec']).size().to_dict(), med.round(2).to_dict(), {k: round(v, 2) for k, v in pool.items()}, {k: round(v, 2) for k, v in tem.items()}, ia)

s = SVG('Cada punto es una campaña promocional: enviados contra respuesta, en correo y en push; recordatorios en verde, ofertas en gris')
s.legend([(GREEN, 'Recordatorio de algo empezado', 'dot'), (M1, 'Oferta nueva: Tasa 0, referidos, descuentos, lanzamientos', 'dot')], 0, 4, size=11)
PAN = [('email', 'Correo: clic por campaña', 0, 0.3), ('push notification', 'Push: apertura por campaña', 400, 0.75)]
Y0, Y1 = 50, 362
ys = logmap(0.02, 30, Y1, Y0)
LB = {'email': {'Verificar identidad': (10, -18, 'start'), 'Pagar compra a meses': (-10, -34, 'end'), 'Tasa 0 a registrados': (-10, 26, 'end'),
                'Lanzamiento BillPay': (-10, 22, 'end'), 'Referidos a leads': (-14, 30, 'end')},
      'push notification': {'Verificar identidad': (10, -14, 'start'), 'Pagar compra a meses': (-10, -14, 'end'), 'Tasa 0 a registrados': (-40, 34, 'end'),
                            'Rescate Tasa 0 a anónimos': (-20, 56, 'end')}}
for ch, h, x0, mn in PAN:
    X0, X1 = x0 + 40, x0 + 372
    xs = logmap(1e5, 4e7, X0, X1)
    s.t(x0, 36, h, 12, INK, w=600)
    for v in (0.03, 0.1, 0.3, 1, 3, 10, 30):
        s.line(X0, ys(v), X1, ys(v)); s.t(X0 - 5, ys(v) + 4, f'{fmt(v)} %', 10.5, SEC, 'end')
    for v, lab in ((1e5, '100 mil'), (1e6, '1 M'), (1e7, '10 M')):
        s.line(xs(v), Y0, xs(v), Y1); s.t(xs(v), Y1 + 15, lab, 10.5, SEC, 'middle')
    s.t(X1, Y1 + 30, 'Enviados en nueve meses', 10.5, SEC, 'end')
    d = g[g.canal == ch]
    for _, q in d.sort_values('rec').iterrows():
        s.circle(xs(q.b), ys(q.resp), 3.6 if q.rec else 3, GREEN if q.rec else M1, ring=q.rec, extra='' if q.rec else ' fill-opacity="0.7"')
    s.line(X0, ys(mn), X1, ys(mn), INK, 1); s.t(X1, ys(mn) + 13, f'mínimo {mn:g} %', 10.5, INK, 'end', halo=True)
    for r, col in ((True, GREEN), (False, SEC)):
        y = ys(med[(ch, r)]); s.line(X0, y, X1, y, col, 1.4)
        s.t(X0 + 3, y - 4, f'mediana {med[(ch, r)]:.2f} %', 10.5, col, 'start', 600, halo=True)
    for n, (dx, dy, an) in LB[ch].items():
        c = d[d.nom == n]
        if not len(c): continue
        q = c.sort_values('b').iloc[-1]
        etiqueta(s, xs(q.b), ys(q.resp), n, dx, dy, an)
s.t(0, 414, 'Campañas promocionales con 100 mil o más enviados. Escalas logarítmicas. Clic sobre entregados; apertura sobre enviados.', 10.5, SEC)

write(62, dict(
    titulo='La gente responde cuando le recordamos lo que dejó a medias, no cuando le ofrecemos algo nuevo',
    que='Recordatorios: terminar el registro, pagar la compra a meses. Ofertas: Tasa 0, referidos.',
    quien='Recordatorios de Marketing, Acquisition y Product Growth; ofertas de todos los equipos.',
    a_quien='Recordatorios a quien empezó algo; ofertas a listas completas de leads y clientes.',
    lecturas=[
        f'Por correo el recordatorio responde {tem["recordatorio"]:.2f} %; las ofertas, de {min(v for k, v in tem.items() if k != "recordatorio"):.2f} a {max(v for k, v in tem.items() if k != "recordatorio"):.2f} %.',
        f'Por push, la mediana del recordatorio abre {med[("push notification", True)]:.1f} % y la de la oferta {med[("push notification", False)]:.1f} %.',
        f'Referidos no funciona por correo ({tem["referidos"]:.2f} %) pero sí en la app: {ia["referidos"]:.0f} % de clic en in-app.',
    ],
    causa='Las campañas nacen de lo que queremos vender este mes, no de lo que cada persona dejó a medias.',
    sowhat='El gancho es lo que la persona dejó a medias; Tasa 0 y novedades solo a un grupo claro.',
    fuente='Fuente: Braze, envíos por campaña, mes y canal (E1), enero a septiembre 2026, sin cobranza ni avisos. Tema por el nombre (regla de la muestra G).',
    svg=s.svg()))
