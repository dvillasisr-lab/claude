"""Lámina 53 (ronda 2). Pequeños múltiplos, un panel por canal con la misma escala. Cada punto es una campaña en ese canal (100 mil o
más mensajes con respuesta medible). x = respuesta en veces el mínimo aceptable del canal (log); y = conversiones del mismo día por cada
mil mensajes (log). Verde = activos; azul = ex clientes y leads que nunca activaron; gris = resto. Rayas = mediana de conversión (E1)."""
import pandas as pd
from b5_svg import *

MIN = {'email': 0.3, 'push notification': 0.75, 'whatsapp': 60.0, 'in-app': 10.0}
t = pd.read_csv(H / 'b5_camp.csv')
t = t[t.canal.isin(MIN) & (t.base >= 100000)].copy()
t['x'] = t.resp / t.canal.map(MIN)
t['cl'] = ['act' if g == 'activos' else ('frio' if g in ('ex', 'nunca') else 'resto') for g in t.g]
COL = {'act': GREEN, 'frio': BLUE, 'resto': MARK2}
S = Svg('Cuatro paneles, uno por canal. Cada punto es una campaña: respuesta en veces el mínimo aceptable contra conversiones por cada mil mensajes, con la mediana de activos y de ex clientes y leads fríos.')
for lx, k, lab in [(0, 'act', 'Activos y recurrentes'), (150, 'frio', 'Ex clientes y leads que nunca activaron'), (390, 'resto', 'Resto')]:
    S.circle(lx + 5, 10, 5, COL[k], '#FFFFFF', 1); S.t(lx + 15, 14, lab, 11, TXT)
S.t(W, 14, 'Raya a la derecha: mediana del grupo', 10.5, SEC, 'end')
PAN = [('email', 'Correo (clic)'), ('push notification', 'Push (apertura)'), ('whatsapp', 'WhatsApp (lectura)'), ('in-app', 'In-app (clic)')]
PW, PH = 300, 132
POS = [(48, 46), (432, 46), (48, 236), (432, 236)]
MED = {}
NAMED = {('Lending-KCash-B0223-CANVAS-Nuevos_NeverActive-InstallmentsNoCash-N/A', 'email'): (0, 1, -8, 'middle'),
         ('Lending-KCash-B0301-CANVAS-Active-Retargeting_Installments_SP', 'email'): (0, 1, -8, 'middle'),
         ('Lending-KPay-B0333-CANVAS-Churn_12MesesInactividad-ConSinOferta-N/A', 'whatsapp'): (0, 10, 4, 'start'),
         ('Marketing-KCash-B0171-CANVAS-Anonimos-RescateTasa0-N/A', 'push notification'): (0, -8, 12, 'end')}
for (c, tit), (px, py) in zip(PAN, POS):
    sx = logx(0.05, 20, px, px + PW); sy = logx(0.01, 100, py + PH, py)
    d = t[t.canal == c]
    S.t(px, py - 8, f'{tit}: {len(d)} campañas', 11.5, INK, w=600)
    for v, lab in [(0.01, '0.01'), (0.1, '0.1'), (1, '1'), (10, '10'), (100, '100')]:
        S.line(px, sy(v), px + PW, sy(v)); S.t(px - 5, sy(v) + 4, lab, 10.5, SEC, 'end')
    for v, lab in [(0.1, '0.1×'), (1, 'mínimo'), (10, '10×')]:
        S.line(sx(v), py, sx(v), py + PH, MARK if v == 1 else GRID, 1.2 if v == 1 else 1)
        S.t(sx(v), py + PH + 13, lab, 10.5, INK if v == 1 else SEC, 'middle', 600 if v == 1 else 400)
    for q in d.sort_values('cl', key=lambda s: s.map({'resto': 0, 'act': 1, 'frio': 2})).itertuples():
        S.circle(sx(q.x), sy(max(q.conv_mil, 0.011)), 3.2, COL[q.cl], '#FFFFFF', 0.8)
    MED[c] = {}
    for q in d.itertuples():
        nm = NAMED.get((q.familia, c))
        if nm: S.t(sx(q.x) + nm[1], sy(max(q.conv_mil, 0.011)) + nm[2], nombre(q.familia), 10.5, INK, nm[3], 600, halo=True)
    ms = {k: med(list(d[d.cl == k].conv_mil)) for k in ('act', 'frio')}; MED[c] = ms
    close = abs(sy(ms['act']) - sy(ms['frio'])) < 14
    for k, dy in (('act', -4), ('frio', 12)):
        m = ms[k]
        S.line(px + PW + 3, sy(m), px + PW + 15, sy(m), COL[k], 3)
        S.t(px + PW + 18, sy(m) + (dy if close else 4), f'{m:.1f}', 11, INK, 'start', 600)
S.t(48, HH - 4, 'Horizontal: respuesta en veces el mínimo aceptable del canal (log). Vertical: conversiones del mismo día por cada mil mensajes (log).', 10.5, SEC)
SVG = S.done()

e, w_, i_ = MED['email'], MED['whatsapp'], MED['in-app']
guarda(53, dict(
    kind='grafica',
    titulo=f'Ex clientes y leads fríos responden casi como los activos, pero convierten {e["act"]/e["frio"]:.0f} veces menos por correo',
    que='Promociones y recordatorios por correo, push, WhatsApp e in-app',
    quien='Marketing y Product Growth a leads y ex clientes; Sales, Marketing y PG a activos',
    a_quien='Activos y recurrentes contra ex clientes y leads que nunca activaron',
    lecturas=[
        f'Correo: mediana de {e["act"]:.1f} conversiones por mil mensajes en activos y {e["frio"]:.1f} en ex clientes y leads fríos.',
        f'WhatsApp: los fríos lo leen igual, pero convierten {w_["frio"]:.1f} por mil contra {w_["act"]:.1f} de los activos.',
        f'In-app: los fríos convierten casi igual ({i_["frio"]:.1f} contra {i_["act"]:.1f} por mil), pero solo lo ve quien tiene la app.',
    ],
    causa='Cada equipo usa su canal de costumbre; Braze no guarda la última respuesta por canal ni si la persona tiene la app.',
    sowhat='El canal se elige por grupo: a los fríos, in-app y push si tienen app; correo si no; WhatsApp casi nunca.',
    fuente='Fuente: Braze E1 (campaña, canal y mes), enero a septiembre 2026. Mínimo: 3 clics por mil correos, 7.5 aperturas por mil push, 6 de 10 WhatsApp leídos, 1 de 10 in-app con clic.',
    svg=SVG,
))
print(MED)
