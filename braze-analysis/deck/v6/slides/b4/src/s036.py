"""Lámina 36 (ronda 2): franja de puntos por pareja de equipos distintos. Cada punto es una pareja de campañas promocionales
de dos equipos el mismo día a la misma persona (E6b); azul si las dos usan el mismo nombre de audiencia."""
import math, pandas as pd, numpy as np
from kit import *
from e6b import load
p = load(); pp = p[p.promo2].copy(); P = pp.usuario_dias_juntas.sum()
x = pp[pp.ta != pp.tb].copy(); x['same'] = x.ag_a == x.ag_b; C = x.usuario_dias_juntas.sum()
ROWS = [('Marketing + Sales', 'Marketing con Sales'), ('Marketing + Product Growth', 'Marketing con Product Growth'),
        ('Marketing + Others', 'Marketing con Others'), ('Product Growth + Sales', 'Product Growth con Sales'),
        ('Others + Sales', 'Sales con Others'), ('Others + Product Growth', 'Product Growth con Others')]
st = {k: (100 * x[(x.pair == k) & x.same].usuario_dias_juntas.sum() / x[x.pair == k].usuario_dias_juntas.sum(), x[x.pair == k].usuario_dias_juntas.sum() / 1e6, int((x.pair == k).sum())) for k, _ in ROWS}
print(st, C / 1e6, P / 1e6, 100 * C / P)
S = Svg('Franja de puntos por pareja de equipos: cada punto es una pareja de campañas promocionales de dos equipos el mismo día a la misma persona; azul si usan el mismo nombre de audiencia')
S.circle(6, 15, 4.5, BLUE); S.t(15, 19, 'Las dos campañas usan el mismo nombre de audiencia', 11, TXT)
S.circle(326, 15, 4.5, G1); S.t(335, 19, 'Nombre distinto, misma persona', 11, TXT)
S.t(0, 38, 'Cada punto: dos campañas de equipos distintos el mismo día a la misma persona.', 10.5, SEC)
X0, X1 = 190, 640
lo, hi_ = math.log10(15000), math.log10(2e6)
sx = lambda v: X0 + (X1 - X0) * (math.log10(v) - lo) / (hi_ - lo)
RY, RH = 64, 50
for v, l in ((20000, '20 mil'), (50000, '50 mil'), (100000, '100 mil'), (250000, '250 mil'), (500000, '500 mil'), (1000000, '1 M')):
    S.line(sx(v), RY - 6, sx(v), RY + RH * 6, GRID); S.t(sx(v), RY + RH * 6 + 16, l, 10.5, SEC, 'middle')
S.t((X0 + X1) / 2, RY + RH * 6 + 32, 'Personas que recibieron las dos campañas el mismo día (escala logarítmica)', 10.5, SEC, 'middle')
S.t(X1 + 14, RY - 10, 'Mismo nombre', 10.5, SEC)
rng = np.random.default_rng(3)
for i, (k, l) in enumerate(ROWS):
    yc = RY + RH * i + RH / 2; d = x[x.pair == k]
    S.t(X0 - 12, yc + 4, l, 11, INK, 'end', 600 if i < 2 else 400)
    S.line(X0, yc + RH / 2, X1, yc + RH / 2, GRID)
    for _, q in d.sort_values('same').iterrows():
        S.circle(sx(q.usuarios_aprox), yc + rng.uniform(-14, 14), 2.8, BLUE if q.same else G1, '#FFFFFF', 0.6)
    v, M, n = st[k]
    S.t(X1 + 14, yc + 2, f'{v:.0f} %', 15, BLUE if v >= 50 else INK, 'start', 700)
    S.t(X1 + 14, yc + 16, f'{n} parejas', 10.5, SEC)
q = x[x.familia_a.str.contains('B0211') & x.familia_b.str.contains('B0171-CANVAS-Anonimos')].sort_values('usuarios_aprox').iloc[-1]
yc = RY + RH * 1.5
S.circle(sx(q.usuarios_aprox), yc, 4.5, INK, '#FFFFFF', 1.5)
lab(S, sx(q.usuarios_aprox), yc, sx(1.7e6), yc - 18, 'Tasa 0 a registrados y Rescate Tasa 0', f'a anónimos: {q.usuarios_aprox/1e3:.0f} mil personas, misma oferta', 'end')
write(36, dict(kind='grafica', seccion='IV. La misma persona, demasiadas veces',
 titulo='Marketing, Sales y Product Growth le escriben a la misma gente, pero cada equipo nombra distinto la audiencia',
 que='Hot Sale, Comercio del día, Tasa 0, descuentos, referidos, Anota y Gana y BillPay',
 quien='Marketing, Sales, Product Growth y NewProducts (en Others)',
 a_quien='Recurrentes de KPay; registrados, anónimos, inactivos y dormants de KCash',
 lecturas=[
  f'Marketing y Sales usan el mismo nombre en {st["Marketing + Sales"][0]:.0f} % de sus choques: recurrentes de KPay.',
  f'Marketing y Product Growth, solo {st["Marketing + Product Growth"][0]:.0f} %: "anónimos" de uno son "registrados" del otro.',
  f'Con Others casi nunca coincide el nombre: {st["Marketing + Others"][0]:.0f} % con Marketing y {st["Others + Product Growth"][0]:.0f} % con Product Growth.',
 ],
 causa='Cada equipo arma y nombra su audiencia por su cuenta y nadie excluye a quien ya recibió la campaña de otro equipo.',
 sowhat='Un dueño por audiencia y exclusiones entre equipos para no mandar la misma oferta dos veces.',
 fuente='Fuente: Braze, E6b (1,000 pares más frecuentes el mismo día, enero a septiembre 2026; muestra). Audiencia tomada del nombre de la campaña y agrupada.',
 svg=S.svg()))
