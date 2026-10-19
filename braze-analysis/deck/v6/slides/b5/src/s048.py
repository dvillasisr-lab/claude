"""Lámina 48 (ronda 2). Arriba: 3 cifras de quien no respondió en nueve meses (E7b). Gráfica: franja de puntos por grupo de audiencia;
cada punto es una campaña con 100 mil o más mensajes (todos sus canales), x = conversiones del mismo día por cada mil mensajes (escala log),
tamaño = mensajes, raya = mediana del grupo (E1). Cobranza y avisos fuera: no buscan un préstamo nuevo."""
import pandas as pd
from b5_svg import *

E = D['e7b']; no, si, tot = E['no'], E['si'], E['tot']
a = pd.read_csv(H / 'b5_camp_todo.csv'); a = a[a.env >= 100000]
ORD = [('activos', 'Activos y recurrentes'), ('nuevos', 'Nuevos y onboarding'), ('todos', 'Todos y otros'),
       ('leads', 'Leads y registrados'), ('ex', 'Ex clientes inactivos'), ('nunca', 'Leads que nunca activaron')]
# campaña: (dx, dy, ancla) de la etiqueta respecto del punto
NAMED = {'Lending-KCash-B0209-CANVAS-Recurrentes_Inactivos-DescuentoDirecto-N/A': (12, 4, 'start'), 'Lending-KPay-B0333-CANVAS-Churn_12MesesInactividad-ConSinOferta-N/A': (-12, 4, 'end'),
         'Lending-KCash-B0223-CANVAS-Nuevos_NeverActive-InstallmentsNoCash-N/A': (2, 22, 'middle'), 'Marketing-KCash-B0171-CANVAS-Leads_BBDDRezagada-RescateTasa0-N/A': (14, 16, 'start'),
         'Lending-KCash-B0301-CANVAS-Active-Retargeting_Installments_SP': (0, 22, 'middle')}
S = Svg('Arriba, tres cifras de quien no respondió en nueve meses. Abajo, cada punto es una campaña: conversiones del mismo día por cada mil mensajes, por grupo de audiencia, con la mediana de cada grupo.')
# franja de cifras
kpis(S, [(f'{100*no["usuarios"]/tot["usuarios"]:.0f} %', f'de {M(tot["usuarios"])} M personas no', 'respondió en nueve meses'),
          (f'{100*no["conv"]/no["usuarios"]:.2f} %', 'de quienes no', 'respondieron convirtió'),
          (f'{no["inapp"]/no["usuarios"]:.2f}', 'vistas de in-app por persona;', f'{si["inapp"]/si["usuarios"]:.1f} en quien sí responde')])

S.t(0, 70, 'Conversiones del mismo día por cada mil mensajes; cada punto es una campaña', 12, INK, w=600)
S.t(W, 70, 'Tamaño: mensajes', 10.5, SEC, 'end')
X0, X1 = 160, 690
sx = logx(0.01, 100, X0, X1)
TOP, RH = 92, 46
for v, lab in [(0.01, '0.01'), (0.1, '0.1'), (1, '1'), (10, '10'), (100, '100')]:
    S.line(sx(v), TOP - 6, sx(v), TOP + RH * len(ORD) - 6)
    S.t(sx(v), TOP + RH * len(ORD) + 8, lab, 10.5, SEC, 'middle')
S.t(W, TOP - 8, 'Campañas', 10.5, SEC, 'end')
for i, (g, lab) in enumerate(ORD):
    yc = TOP + RH * i + 16
    cold = g in ('ex', 'nunca')
    d = a[a.g == g].sort_values('env', ascending=False)
    S.t(X0 - 10, yc + 4, lab, 11.5, INK, 'end', 600 if cold else 400)
    offs = swarm([sx(max(v, 0.011)) for v in d.conv_mil], 3, 17)
    for r, o in zip(d.itertuples(), offs):
        rr = 2.2 + 7 * (r.env / 16e6) ** 0.5
        S.circle(sx(max(r.conv_mil, 0.011)), yc + o, rr, BLUE if cold else MARK, '#FFFFFF', 0.8)
    m = med(list(d.conv_mil))
    S.line(sx(m), yc - 15, sx(m), yc + 15, INK, 2.5)
    S.t(sx(m), yc - 18, f'mediana {m:.1f}', 10.5, INK, 'middle', 600, halo=True)
    S.t(W, yc + 4, f'{len(d)}', 11, SEC, 'end')
    for r in d.itertuples():
        if r.familia in NAMED:
            dx, dy, an = NAMED[r.familia]
            S.t(sx(r.conv_mil) + dx, yc + dy, nombre(r.familia), 10.5, INK, an, 600, halo=True)
SVG = S.done()

G = D['grupos']
mex, mnu, mac = (med(list(a[a.g == g].conv_mil)) for g in ('ex', 'nunca', 'activos'))
guarda(48, dict(
    kind='grafica',
    titulo='Tres de cada cuatro personas no respondieron en nueve meses, y no sabemos cuántas son ex clientes',
    que='Tasa 0, referidos, descuentos y lanzamientos, sobre todo por correo y push',
    quien='Todos los equipos; ningún dato liga a quien no responde con quien le escribe',
    a_quien='Por el nombre de la campaña: leads, activos, ex clientes y leads que nunca activaron',
    lecturas=[
        f'{M(no["usuarios"])} M de {M(tot["usuarios"])} M personas no respondieron: recibieron {M(no["msgs"], 0)} M mensajes y {M(no["costo"])} M MXN.',
        f'Mediana por campaña: activos {mac:.1f} conversiones por mil mensajes; ex clientes {mex:.1f}; leads que nunca activaron {mnu:.1f}.',
        'Ningún dato liga a la persona que no responde con su segmento: no sabemos cuántos son ex clientes.',
    ],
    causa='Braze no guarda el segmento de cada persona: solo el nombre de la campaña dice a quién se le escribe.',
    sowhat='Para recuperar hay que saber a quién: ex cliente y lead que nunca activó piden canal y presupuesto distintos.',
    fuente='Fuente: Braze E7b (respuesta por persona) y E1 (campaña, canal y mes), enero a septiembre 2026. Campañas con 100 mil o más mensajes; cobranza y avisos fuera. Conversión del mismo día, repartida.',
    svg=SVG,
))
print(mac, mex, mnu)
