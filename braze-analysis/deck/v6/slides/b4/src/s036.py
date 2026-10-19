"""Lámina 36: choques promocionales por pareja de equipos y nombre de audiencia (E6b, 1,000 pares más frecuentes)."""
import pandas as pd
from kit import *
from e6b import load
p = load(); pp = p[p.promo2].copy(); P = pp.usuario_dias_juntas.sum()
pp['same_aud'] = pp.ag_a == pp.ag_b
g = pp.groupby('pair').apply(lambda d: pd.Series({'M': d.usuario_dias_juntas.sum() / 1e6,
        'same': 100 * d[d.same_aud].usuario_dias_juntas.sum() / d.usuario_dias_juntas.sum()}))
cross = pp[pp.ta != pp.tb].usuario_dias_juntas.sum()
print(g.round(1), cross / 1e6, 100 * cross / P)
TEAMS = ['Marketing', 'Sales', 'Product Growth', 'Others']
TEMA = {  # tema principal de cada pareja, leído de los pares de E6b
 'Marketing + Marketing': ['Comercio', 'del día y', 'registro'], 'Sales + Sales': ['Comercio', 'del día y', 'Hot Sale'],
 'Product Growth + Product Growth': ['Tasa 0,', 'inactivos y', 'temporada'], 'Others + Others': ['Comercios', 'con pruebas', 'de QA'],
 'Marketing + Sales': ['Hot Sale con', 'Hot Sale'], 'Marketing + Product Growth': ['Inactivos con', 'referidos;', 'Tasa 0'],
 'Marketing + Others': ['BillPay con', 'prueba de QA'], 'Product Growth + Sales': ['Comercios con', 'temporada'],
 'Others + Product Growth': ['Anota y Gana', 'con BillPay'], 'Others + Sales': ['Hot Sale con', 'BillPay']}
S = Svg('Matriz de equipos con millones de personas-día de choque promocional y tema principal; y parte de los choques entre equipos con el mismo nombre de audiencia')
S.t(0, 16, 'Millones de personas-día con dos promociones a la vez, por pareja de equipos', 11.5, INK, w=600)
S.t(0, 32, 'Tema principal escrito en cada celda. Color más intenso, más choques.', 10.5, SEC)
LX, CW, RH, Y0 = 100, 92, 74, 66
SHORT = {'Marketing': 'Marketing', 'Sales': 'Sales', 'Product Growth': 'Product Growth', 'Others': 'Others'}
for j, t in enumerate(TEAMS):
    S.t(LX + CW * (j + 0.5), Y0 - 8, SHORT[t], 11, TXT, 'middle', 600)
for i, ti in enumerate(TEAMS):
    S.t(LX - 8, Y0 + RH * (i + 0.5) + 4, SHORT[ti], 11, TXT, 'end', 600)
    for j, tj in enumerate(TEAMS):
        x, y = LX + CW * j, Y0 + RH * i
        if j < i:
            S.rect(x + 1, y + 1, CW - 2, RH - 2, '#F4F6F9'); continue
        k = ' + '.join(sorted([ti, tj])); v = g.loc[k, 'M']
        op = 0.10 + 0.85 * v / g.M.max()
        S.raw(f'<rect x="{x+1:.1f}" y="{y+1:.1f}" width="{CW-2:.1f}" height="{RH-2:.1f}" fill="{BLUE}" fill-opacity="{op:.2f}"/>')
        col = '#FFFFFF' if op > 0.5 else INK
        S.t(x + 8, y + 20, f'{v:.1f} M', 13, col, 'start', 700)
        for n, l in enumerate(TEMA[k]):
            S.t(x + 8, y + 36 + 13.5 * n, l, 10.5, col if op > 0.5 else TXT)
S.t(LX, Y0 + RH * 4 + 18, 'Debajo de la diagonal, la misma pareja.', 10.5, SEC)
# panel derecho: mismo nombre de audiencia
PX = 500
S.t(PX, 16, 'Choques entre equipos distintos:', 11.5, INK, w=600)
S.t(PX, 32, '¿le dan el mismo nombre a la audiencia?', 11.5, INK, w=600)
S.rect(PX, 46, 10, 10, BLUE); S.t(PX + 14, 55, 'Mismo nombre', 10.5, TXT); S.rect(PX + 104, 46, 10, 10, G2); S.t(PX + 118, 55, 'Nombre distinto', 10.5, TXT)
BX0, BX1 = PX, 770; y = 78
for k, lab in [('Marketing + Sales', 'Marketing con Sales'), ('Marketing + Product Growth', 'Marketing con Product Growth'),
               ('Marketing + Others', 'Marketing con Others'), ('Product Growth + Sales', 'Product Growth con Sales'),
               ('Others + Product Growth', 'Product Growth con Others')]:
    v, M = g.loc[k, 'same'], g.loc[k, 'M']
    S.t(BX0, y + 10, lab, 11, INK, 'start', 600); S.t(BX1, y + 10, f'{M:.1f} M personas-día', 10.5, SEC, 'end')
    w = (BX1 - BX0) * v / 100
    S.rect(BX0, y + 16, max(w - 1, 0), 18, BLUE); S.rect(BX0 + w + 1, y + 16, BX1 - BX0 - w - 1, 18, G2)
    if w > 40: S.t(BX0 + w - 5, y + 29.5, f'{v:.0f} %', 11, '#FFFFFF', 'end', 700)
    else: S.t(BX0 + w + 5, y + 29.5, f'{v:.0f} %', 11, INK, 'start', 700)
    y += 52
S.t(PX, y + 8, 'Nombre distinto, misma gente: los "anónimos" de', 10.5, SEC)
S.t(PX, y + 22, 'Marketing son los "registrados" de Product Growth;', 10.5, SEC)
S.t(PX, y + 36, 'los "dormants" de uno son los "inactivos" del otro.', 10.5, SEC)

write(36, dict(kind='grafica', seccion='IV. La misma persona, demasiadas veces',
 titulo='Marketing, Sales y Product Growth le escriben a la misma gente, pero cada equipo le pone otro nombre a la audiencia',
 que='Marketing con Sales: Hot Sale, Comercio del día y cashback para KPay. Marketing con Product Growth: Tasa 0, descuentos y referidos para KCash. Product Growth con Sales: Anota y Gana contra Hot Sale. Todo promocional.',
 quien='Marketing, Sales, Product Growth y NewProducts (en Others), con el lanzamiento de BillPay.',
 a_quien='Recurrentes y activos de KPay (Marketing y Sales). Registrados, anónimos, inactivos y dormants de KCash (Product Growth y Marketing).',
 lecturas=[
  f'{100*cross/P:.0f} % del choque promocional es entre equipos distintos: {cross/1e6:.0f} M de {P/1e6:.0f} M personas-día. El más grande es Marketing con Sales ({g.loc["Marketing + Sales","M"]:.1f} M).',
  f'Marketing y Sales usan el mismo nombre de audiencia en {g.loc["Marketing + Sales","same"]:.0f} % de sus choques: los recurrentes de KPay. Marketing y Product Growth, solo en {g.loc["Marketing + Product Growth","same"]:.0f} %, aunque es la misma gente.',
  'En agosto, Tasa 0 a registrados (Product Growth) y Rescate Tasa 0 a anónimos (Marketing) le llegaron por push a las mismas 124 mil personas el mismo día, unos cuatro días cada una.',
 ],
 causa='Cada equipo arma y nombra su audiencia por su cuenta y nadie excluye a quien ya recibió la campaña de otro equipo; el nombre esconde que es la misma persona.',
 sowhat='Hace falta un dueño por audiencia y exclusiones entre equipos para que una persona no reciba la misma oferta de dos equipos.',
 fuente='Fuente: Braze, E6b (1,000 pares de campañas más frecuentes el mismo día, enero a septiembre 2026; muestra, no universo). Audiencia tomada del nombre de la campaña y agrupada; la columna misma_audiencia de E6b no se usa porque compara el tipo de campaña, no la audiencia.',
 svg=S.svg()))
