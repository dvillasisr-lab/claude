"""Lámina 26: choques entre equipos. Izquierda: matriz de usuario-días con dos promociones el mismo día (E6b, mil pares con más
coincidencias; promoción = tipo del catálogo). Derecha arriba: ejemplos de la misma oferta. Derecha abajo: campañas distintas en el día
contra mensajes y bajas por mil usuario-días (E6a)."""
from datos import *
from svgk import *
x = e1(); tip = x.drop_duplicates('familia').set_index('familia').tipo
p = pd.read_csv(R + 'data/e6b_pares_familias.csv')
for s in 'ab':
    p['eq_' + s] = p['equipo_' + s].map(team_of); p['f_' + s] = p['familia_' + s].map(colapsa); p['t_' + s] = p['f_' + s].map(tip)
pr = p[(p.t_a == 'promocional o lifecycle') & (p.t_b == 'promocional o lifecycle')].copy()
TOT = pr.usuario_dias_juntas.sum(); BTW = pr[pr.eq_a != pr.eq_b].usuario_dias_juntas.sum()
print('promo %.1f M, entre equipos %.1f M (%.0f %%)' % (TOT / 1e6, BTW / 1e6, 100 * BTW / TOT))
M = {}
for r in pr.itertuples():
    k = tuple(sorted([r.eq_a, r.eq_b])); M[k] = M.get(k, 0) + r.usuario_dias_juntas
def pair(pa, pb, canal_a=None, canal_b=None):
    d = p[p.f_a.str.contains(pa) & p.f_b.str.contains(pb)]
    if canal_a: d = d[d.canal_a == canal_a]
    if canal_b: d = d[d.canal_b == canal_b]
    return d.sort_values('usuarios_aprox', ascending=False).iloc[0]
t0 = pair('B0211-CANVAS-Nuevos_RegistradosPay', 'B0171-CANVAS-Anonimos-RescateTasa0', 'push notification')
dd = pair('B0209-CANVAS-Recurrentes_Inactivos', 'B0326-Canvas-Recurrentes_Dormants', 'email', 'email')
dw = pair('B0209-CANVAS-Recurrentes_Inactivos', 'B0326-Canvas-Recurrentes_Dormants', 'whatsapp', 'whatsapp')
hs = pair('B0492-CANVAS-Recurrentes-HotSale', 'B0493-CANVAS-Recurrentes-HotSaleKUESKI')
for z in (t0, dd, dw, hs): print(z.f_a[:50], z.canal_a, z.f_b[:50], z.canal_b, z.usuarios_aprox, z.usuario_dias_juntas)
cd = x[x.familia.str.contains('comerciodel', case=False)].groupby('equipo').envios.sum() / 1e6; print(cd.round(1).to_dict())
a = pd.read_csv(R + 'data/e6a_solape_dia_mes.csv')
g = a.groupby('banda_familias_dia').agg(ud=('usuario_dias', 'sum'), msgs=('msgs', 'sum'), baja=('usuario_dias_con_baja', 'sum'))
g['mpd'] = g.msgs / g.ud; g['bpm'] = 1000 * g.baja / g.ud; g['pct'] = 100 * g.ud / g.ud.sum(); print(g.round(3))
S = Svg('Usuario-días con promociones de dos equipos el mismo día, ejemplos de la misma oferta y bajas según campañas recibidas en el día')
S.t(0, 16, 'Personas por día con promociones de dos equipos a la vez', 12.5, INK, w=600)
S.t(0, 32, 'Millones de usuario-días, enero a septiembre', 11, SEC)
TE = ['Marketing', 'Product Growth', 'Sales', 'Others']
CX, CY, CS = 104, 70, 56
VM = max(v for k, v in M.items() if k[0] != k[1])
def mix(c1, c2, t):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]; b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return '#' + ''.join(f'{round(a[i] + (b[i] - a[i]) * t):02X}' for i in range(3))
for j, t in enumerate(TE):
    S.t(CX + CS * j + CS / 2, CY - 6, t if t != 'Product Growth' else 'Product G.', 10.5, SEC, 'middle')
for i, ti in enumerate(TE):
    S.t(CX - 8, CY + CS * i + CS / 2 + 4, ti, 11, INK, 'end', w=600)
    for j, tj in enumerate(TE):
        if j > i: continue
        v = M.get(tuple(sorted([ti, tj])), 0)
        same = i == j
        fill = '#EEF0F4' if same else mix('#FFFFFF', BLUE, 0.12 + 0.88 * v / VM)
        S.r(CX + CS * j + 1, CY + CS * i + 1, CS - 2, CS - 2, fill)
        dark = (not same) and v / VM > 0.45
        S.t(CX + CS * j + CS / 2, CY + CS * i + CS / 2 + 4, f'{v/1e6:.1f}', 12 if not same else 11, '#FFFFFF' if dark else (SEC if same else INK), 'middle', w=600 if not same else 400)
S.t(CX, CY + CS * 4 + 18, 'Gris: dentro del mismo equipo.', 10.5, SEC)
S.t(CX, CY + CS * 4 + 32, f'Entre equipos: {BTW/1e6:.1f} M de {TOT/1e6:.1f} M ({100*BTW/TOT:.0f} %).', 10.5, SEC)
# ejemplos
EX0 = 372
S.t(EX0, 16, 'La misma oferta a la misma persona el mismo día', 12.5, INK, w=600)
ej = [('Tasa 0', f'Product Growth a registrados y Marketing a anónimos, por push: {t0.usuarios_aprox/1e3:.0f} mil personas en agosto'),
      ('Descuento y referidos', f'a los mismos ex clientes: hasta {dd.usuarios_aprox/1e3:.0f} mil por correo y {dw.usuarios_aprox/1e3:.0f} mil con dos WhatsApp, el mismo día'),
      ('Promociones de KPay', f'Hot Sale de Marketing y de Sales por push a {hs.usuarios_aprox/1e3:.0f} mil clientes; Comercio del día: {cd["Marketing"]:.1f} M y {cd["Sales"]:.1f} M envíos')]
y = 36
import textwrap
for k, (h, txt) in enumerate(ej):
    S.r(EX0, y + 2, 3, 30, BLUE)
    S.t(EX0 + 10, y + 12, h, 11.5, INK, w=600)
    lines = textwrap.wrap(txt, 62)
    for q, ln in enumerate(lines[:2]): S.t(EX0 + 10, y + 26 + 13 * q, ln, 10.5, TXT)
    y += 26 + 13 * min(len(lines), 2) + 8
# escalera
LY0, LY1 = 268, 360; LX0, LX1 = EX0 + 40, 760
S.t(EX0, 236, 'Más campañas el mismo día, más bajas', 12.5, INK, w=600)
S.t(EX0, 252, 'Bajas por cada mil usuario-días, según campañas que recibe en el día', 11, SEC)
BS = ['1', '2', '3 a 4', '5 a 7', '8+']
ys = lambda v: LY1 - (LY1 - LY0) * v / 0.8
for v in (0, 0.4, 0.8):
    S.l(LX0, ys(v), LX1, ys(v), GRID); S.t(LX0 - 6, ys(v) + 4, f'{v:.1f}', 10.5, SEC, 'end')
xb = lambda i: LX0 + 20 + (LX1 - LX0 - 40) * i / 4
pts = [(xb(i), ys(g.loc[b, 'bpm'])) for i, b in enumerate(BS)]
S.raw('<polyline points="' + ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts) + f'" fill="none" stroke="{MRK}" stroke-width="2"/>')
for i, b in enumerate(BS):
    hi = b in ('8+',)
    S.c(pts[i][0], pts[i][1], 5, BLUE if hi else MRK)
    S.t(pts[i][0], pts[i][1] - 9, f"{g.loc[b, 'bpm']:.2f}", 11, INK, 'middle', w=600, halo=True)
    S.t(pts[i][0], LY1 + 15, b, 10.5, INK, 'middle', w=600)
    S.t(pts[i][0], LY1 + 29, f"{g.loc[b, 'mpd']:.1f}", 10.5, SEC, 'middle')
S.t(LX0 - 6, LY1 + 15, 'Campañas', 10.5, SEC, 'end'); S.t(LX0 - 6, LY1 + 29, 'Mensajes', 10.5, SEC, 'end')
S.t(EX0, 412, 'Usuario-día: una persona en un día. Promoción según el tipo del catálogo.', 10.5, SEC)
svg = S.done()
pm = g.loc[['3 a 4', '5 a 7', '8+'], 'pct'].sum()
save(26, dict(kind='grafica',
  titulo='Dos equipos le mandan la misma oferta a la misma persona el mismo día: Tasa 0, descuentos y promociones de KPay',
  que='Tasa 0 de dos equipos; descuento directo y referidos al mismo ex cliente; las mismas promociones de comercios que aceptan KPay (Comercio del día, Hot Sale, Amazon, Cuponera) de Marketing y de Sales.',
  quien='Marketing con Sales y Marketing con Product Growth, sobre todo. Others aparece por el lanzamiento de BillPay a toda la base.',
  a_quien='Registrados sin crédito y anónimos (Tasa 0), ex clientes inactivos y dormidos (descuento y referidos), clientes recurrentes de KPay (promociones).',
  lecturas=[
   f'{100*BTW/TOT:.0f} % de las veces que una persona recibe dos promociones el mismo día, vienen de equipos distintos. Marketing y Sales suman {M[("Marketing","Sales")]/1e6:.1f} M usuario-días; Marketing y Product Growth, {M[("Marketing","Product Growth")]/1e6:.1f} M.',
   f'Con una campaña en el día la persona recibe un mensaje; con tres o cuatro, {g.loc["3 a 4","mpd"]:.1f}; con ocho o más, {g.loc["8+","mpd"]:.0f}. Uno de cada once usuario-días tiene tres o más campañas.',
   f'La baja pasa de {g.loc["1","bpm"]:.2f} por mil usuario-días con una campaña a {g.loc["8+","bpm"]:.2f} con ocho o más, casi el doble. Con dos WhatsApp el mismo día se pagan los dos si se entregan.'],
  causa='Nadie es dueño de la gente que no ha hecho nada ni de las promociones de KPay, y no hay un calendario común: cada equipo programa sus envíos sin ver lo que mandan los demás.',
  sowhat='Un solo dueño por oferta y por grupo de personas, y un calendario común que impida dos promociones el mismo día a la misma persona.',
  fuente='Fuente: Braze, pares de campañas que coinciden el mismo día (E6b, los mil pares con más coincidencias, no el total) y campañas por persona y día (E6a), enero a septiembre 2026. No tenemos la respuesta ni la baja de cada par; la respuesta sube con más campañas porque las reciben los más activos.',
  svg=svg))
check(26)
