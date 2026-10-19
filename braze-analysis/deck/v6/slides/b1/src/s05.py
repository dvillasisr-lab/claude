"""Lámina 5: cuánto cuesta Braze en mensajes. Pareto de campañas (todas sus versiones y canales) ordenadas de mayor a menor gasto:
gasto, conversiones atribuidas y mensajes acumulados. Arriba, tres cifras grandes. E1 con base_p1."""
import numpy as np
from comun import load, write, Svg, INK, TXT, SEC, GRID, BLUE, GREEN, G1, FUENTE_E1

d = load()
f = d.groupby('fam').agg(cost=('costo', 'sum'), conv=('conversiones_fraccional', 'sum'), env=('envios', 'sum'), eq=('equipo', 'first'))
f = f[f.env > 0].sort_values(['cost', 'env'], ascending=False)  # solo campañas que mandaron algo (CANON: unas 1,070)
f['cc'] = f.cost.cumsum() / f.cost.sum(); f['cv'] = f.conv.cumsum() / f.conv.sum(); f['ce'] = f.env.cumsum() / f.env.sum()
N = len(f); NR = int(round(N, -1)); n50 = int((f.cc < 0.5).sum()) + 1; npay = int((f.cost > 0).sum())
wa2 = d[d.fam.isin(f.index[:2]) & (d.canal == 'whatsapp')].costo.sum()
mes = d.costo.sum() / 9; wa = d[d.canal == 'whatsapp'].costo.sum() / d.costo.sum()
r50 = f.iloc[n50 - 1]
print(N, n50, npay, r50.cc, r50.cv, r50.ce, mes, wa)
NOM = {'Marketing-KCash-B0171-CANVAS-Leads_BBDDRezagada-NarrativaTasa0-N/A': 'Tasa 0 a leads rezagados (Marketing)',
       'Marketing-KCash-B0171-CANVAS-Leads_BBDDRezagada-RescateTasa0-N/A': 'Rescate Tasa 0 a leads rezagados (Marketing)',
       'Lending-KCash-B0209-CANVAS-Recurrentes_Inactivos-DescuentoDirecto-N/A': 'Descuento a inactivos (Product Growth)'}

S = Svg('Campañas ordenadas de mayor a menor gasto: porcentaje acumulado del gasto, de las conversiones atribuidas y de los mensajes')
# cifras grandes
STATS = [(f'{mes / 1e6:.1f} M MXN', 'al mes en mensajes, sin licencia'), (f'{n50} campañas', f'de unas {NR:,} se llevan la mitad del gasto'),
         (f'{r50.cv * 100:.0f} %', f'de las conversiones vienen de esas {n50}')]
for i, (b, l) in enumerate(STATS):
    x = i * 262
    S.t(x, 30, b, 26, BLUE if i == 1 else INK, 'start', 700); S.t(x, 50, l, 11.5, TXT)
# leyenda
SER = [('cc', 'Gasto en MXN', BLUE, 2.6), ('cv', 'Conversiones atribuidas', GREEN, 2.2), ('ce', 'Mensajes', G1, 1.8)]
lx = 0
for k, lab, col, w in SER:
    S.line(lx, 80, lx + 20, 80, col, 2.5); S.t(lx + 26, 84, lab, 11.5, TXT); lx += 26 + len(lab) * 6.3 + 22
S.t(780, 84, '% acumulado', 11, SEC, 'end')
X0, X1, Y0, Y1 = 40, 770, 100, 372
lmax = np.log10(N)
xx = lambda i: X0 + (X1 - X0) * np.log10(i) / lmax
yy = lambda v: Y1 - (Y1 - Y0) * v
for v in (0, .25, .5, .75, 1):
    S.line(X0, yy(v), X1, yy(v), GRID); S.t(X0 - 6, yy(v) + 4, f'{v * 100:.0f} %', 11, SEC, 'end')
for t in (1, 3, 10, 30, 100, 300, 1000):
    S.line(xx(t), Y1, xx(t), Y1 + 4, G1); S.t(xx(t), Y1 + 17, f'{t:,}', 11, SEC, 'middle')
S.t(X1, Y1 + 33, f'Campañas que mandaron algo, de mayor a menor gasto ({N:,}; escala logarítmica)', 10.5, SEC, 'end')
idx = np.unique(np.round(np.logspace(0, lmax, 400)).astype(int))
for k, lab, col, w in SER[::-1]:
    S.poly([(xx(i), yy(f[k].iloc[i - 1])) for i in idx], col, w)
# corte en la mitad del gasto
S.line(xx(n50), Y0, xx(n50), Y1, INK, 1, ' stroke-dasharray="3 3"')
S.circle(xx(n50), yy(r50.cc), 4.5, BLUE); S.circle(xx(n50), yy(r50.cv), 4.5, GREEN)
S.t(xx(n50) + 8, yy(r50.cc) - 6, f'{n50} campañas: {r50.cc * 100:.0f} % del gasto', 11.5, BLUE, 'start', 700, halo=True)
S.t(xx(n50) + 8, yy(r50.cv) + 16, f'y {r50.cv * 100:.0f} % de las conversiones', 11.5, GREEN, 'start', 700, halo=True)
# las tres que más gastan
for i in range(3):
    r = f.iloc[i]
    S.circle(xx(i + 1), yy(r.cc), 3.5, BLUE)
    S.t(xx(1) + 4, Y0 + 14 + i * 15, f'{i + 1}. {NOM[f.index[i]]}: {r.cost / 1e6:.1f} M MXN', 11, INK if i == 0 else TXT, 'start', 600 if i == 0 else 400)
for i in range(3):
    S.t(xx(i + 1), yy(f.iloc[i].cc) + 16, f'{i + 1}', 10.5, SEC, 'middle', 600, halo=True)
S.t(xx(npay) - 4, yy(1) + 16, f'Desde la {npay}: solo push e in-app, sin costo', 10.5, SEC, 'end', 400, halo=True)

write(5, dict(kind='grafica',
    titulo=f'Braze nos cuesta {mes / 1e6:.1f} M MXN al mes solo en mensajes, y la mitad se va en {n50} campañas, sobre todo de WhatsApp',
    que='Rescates de Tasa 0, descuentos a inactivos y referidos, casi todo por WhatsApp.',
    quien='Marketing y Product Growth: son dueños de las campañas que más gastan.',
    a_quien='Leads rezagados, ex clientes inactivos y registrados sin crédito.',
    lecturas=[
        f'{n50} de unas {NR:,} campañas se llevan {r50.cc * 100:.0f} % del gasto y traen {r50.cv * 100:.0f} % de las conversiones atribuidas.',
        f'Las dos de Tasa 0 a leads rezagados de Marketing suman {(f.cost.iloc[0] + f.cost.iloc[1]) / 1e6:.1f} M MXN en nueve meses, {wa2 / 1e6:.1f} M de ellos por WhatsApp.',
        f'WhatsApp es {wa * 100:.0f} % del gasto. Desde la campaña {npay} todo es push e in-app, sin costo.'],
    causa='No hay presupuesto de mensajes por equipo ni por campaña: cada equipo ve sus clics, nadie ve el gasto total.',
    sowhat='Revisar unas 20 campañas mueve la mitad del gasto: ahí empieza el plan.',
    fuente=f'{FUENTE_E1}. Campaña = nombre sin fecha, todos sus canales. Conversión atribuida = fraccional. WhatsApp 1.00 MXN por entregado, email 0.05 MXN.',
    svg=S.done()))
