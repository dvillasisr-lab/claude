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
g['mpd'] = g.msgs / g.ud; g['bpm'] = 1000 * g.baja / g.ud; print(g.round(3))
import math, random
for s_ in 'ab': pr['tm_' + s_] = [tema_of(z) for z in pr['f_' + s_]]
bt = pr[pr.eq_a != pr.eq_b].copy()
bt['par'] = [' + '.join(sorted([u, v])) for u, v in zip(bt.eq_a, bt.eq_b)]
bt['same'] = bt.tm_a == bt.tm_b
PARS = (bt.groupby('par').usuario_dias_juntas.sum().sort_values(ascending=False)).index.tolist()
NOMB = {'Product Growth + Sales': 'Product Growth y Sales', 'Marketing + Product Growth': 'Marketing y Product Growth', 'Marketing + Sales': 'Marketing y Sales',
        'Marketing + Others': 'Marketing y Others', 'Others + Sales': 'Others y Sales', 'Others + Product Growth': 'Others y Product Growth'}
CASOS = [('B0211-CANVAS-Nuevos_RegistradosPay', 'B0171-CANVAS-Anonimos-RescateTasa0', 'push notification', 'Tasa 0 de los dos, por push'),
         ('B0209-CANVAS-Recurrentes_Inactivos', 'B0326-Canvas-Recurrentes_Dormants', 'email', 'Descuento y referidos al mismo ex cliente'),
         ('B0492-CANVAS-Recurrentes-HotSale', 'B0493-CANVAS-Recurrentes-HotSaleKUESKI', 'push notification', 'Hot Sale de los dos, por push'),
         ('B0440-CANVAS-Todos-AnotayGana', 'BillPay_Intro_Full', 'push notification', 'Anota y Gana y BillPay el mismo día')]
rnd = random.Random(5)
S = Svg('Pares de campañas de dos equipos que le llegan a la misma persona el mismo día, por par de equipos')
S.t(0, 16, 'Cada punto es un par de promociones de dos equipos que llegan a la misma persona el mismo día', 12.5, INK, w=600)
S.c(6, 34, 4.5, BLUE, stroke='none'); S.t(15, 38, 'Las dos con el mismo tema u oferta', 11.5)
S.c(232, 34, 4.5, MRK, stroke='none'); S.t(241, 38, 'Temas distintos', 11.5)
X0, X1 = 150, 650
LO, HI = math.log10(2e4), math.log10(2e6)
xs = lambda v: X0 + (X1 - X0) * (math.log10(min(max(v, 2e4), 2e6)) - LO) / (HI - LO)
TOP, RH = 62, 52
YB = TOP + RH * len(PARS)
for v, lab in [(3e4, '30 mil'), (1e5, '100 mil'), (3e5, '300 mil'), (1e6, '1 M')]:
    S.l(xs(v), TOP - 4, xs(v), YB - 4, GRID); S.t(xs(v), YB + 10, lab, 10.5, SEC, 'middle')
S.t(X1, YB + 24, 'Personas que reciben las dos el mismo día (escala logarítmica)', 10.5, SEC, 'end')
S.t(780, TOP - 8, 'Personas por día · mismo tema', 10.5, SEC, 'end')
for i, pp in enumerate(PARS):
    d = bt[bt.par == pp]
    y0 = TOP + RH * i; cy = y0 + 32
    if i: S.l(0, y0, 780, y0, GRID)
    S.t(0, cy - 2, NOMB.get(pp, pp), 11.5, INK, w=600); S.t(0, cy + 12, f'{len(d)} pares', 10.5, SEC)
    for r in d.sort_values('same').itertuples():
        S.c(xs(r.usuarios_aprox), cy + rnd.uniform(-9, 9), 3.2, BLUE if r.same else MRK, stroke='#FFFFFF', sw=0.6, op=0.8)
    ud = d.usuario_dias_juntas.sum(); sm = d[d.same].usuario_dias_juntas.sum()
    S.t(780, cy - 2, f'{ud/1e6:.1f} M', 12, INK, 'end', w=600)
    S.t(780, cy + 12, f'{100*sm/ud:.0f} % mismo tema', 10.5, BLUE if sm / ud > 0.3 else SEC, 'end', w=600)
    for pa, pb, ch, nm in CASOS:
        z = d[(d.f_a.str.contains(pa) & d.f_b.str.contains(pb)) | (d.f_a.str.contains(pb) & d.f_b.str.contains(pa))]
        z = z[(z.canal_a == ch) | (z.canal_b == ch)]
        if len(z):
            z = z.sort_values('usuarios_aprox', ascending=False).iloc[0]
            x = xs(z.usuarios_aprox)
            S.c(x, cy, 5, BLUE if z.same else INK, sw=1.5)
            anc = 'end' if (x > 420 or 'Tasa 0' in nm) else 'start'
            S.t(x + (-8 if anc == 'end' else 8), y0 + 13, (f'{nm}: {z.usuarios_aprox/1e6:.1f} M' if z.usuarios_aprox >= 1e6 else f'{nm}: {z.usuarios_aprox/1e3:.0f} mil'), 10.5, INK, anc, w=600, halo=True)
            print(pp, nm, z.usuarios_aprox, z.same)
svg = S.done()
ms = bt[bt.par == 'Marketing + Sales']; msame = 100 * ms[ms.same].usuario_dias_juntas.sum() / ms.usuario_dias_juntas.sum()
save(26, dict(kind='grafica',
  titulo='Dos equipos mandan la misma oferta a la misma persona el mismo día: Tasa 0, descuentos y promociones de KPay',
  que='Tasa 0 de dos equipos, descuento y referidos al mismo ex cliente, promociones de KPay.',
  quien='Marketing con Sales y con Product Growth, sobre todo.',
  a_quien='Registrados y anónimos, ex clientes dormidos, clientes recurrentes de KPay.',
  lecturas=[
   f'{100*BTW/TOT:.0f} % de las veces que alguien recibe dos promociones el mismo día vienen de dos equipos distintos.',
   f'Marketing y Sales: {M[("Marketing","Sales")]/1e6:.1f} M personas por día, {msame:.0f} % con promociones de KPay en las dos campañas.',
   f'Con una campaña al día se dan de baja {g.loc["1","bpm"]:.2f} por cada mil personas por día; con ocho o más, {g.loc["8+","bpm"]:.2f}.'],
  causa='Nadie es dueño de la gente que no ha hecho nada ni de las promociones de KPay, y no hay calendario común.',
  sowhat='Un dueño por oferta y por grupo de personas, y un calendario que impida dos promociones el mismo día.',
  fuente='Fuente: Braze, pares de campañas que coinciden el mismo día (E6b, los mil pares con más coincidencias) y campañas por persona y día (E6a), enero a septiembre 2026.',
  svg=svg))
check(26)
