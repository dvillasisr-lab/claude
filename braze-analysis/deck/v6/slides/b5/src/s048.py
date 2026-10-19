"""Lámina 48: tres de cada cuatro personas no respondieron en nueve meses; por el nombre de la campaña sabemos a qué grupo se le escribe,
pero no a qué grupo pertenece quien no responde. Izquierda: parte de mensajes, gasto y conversiones por grupo (E1).
Derecha: 19.5 M personas partidas en quien respondió y quien no, y su perfil (E7b)."""
from b5_svg import *

G = D['grupos']; E = D['e7b']; no, si, tot = E['no'], E['si'], E['tot']
ORD = ['nunca', 'ex', 'leads', 'activos', 'todos', 'cobranza', 'transaccional', 'nuevos']
LAB = {'nunca': 'Leads que nunca activaron', 'ex': 'Ex clientes inactivos', 'leads': 'Leads y registrados', 'activos': 'Activos y recurrentes',
       'todos': 'Todos y otros', 'cobranza': 'Cobranza', 'transaccional': 'Avisos transaccionales', 'nuevos': 'Nuevos y onboarding'}
S = Svg('Izquierda: parte de los mensajes, del gasto y de las conversiones del mismo día por grupo de audiencia. Derecha: 19.5 millones de personas, 73 por ciento sin respuesta en nueve meses, y su perfil contra quien sí responde.')
# ---------- panel izquierdo ----------
S.t(0, 14, 'A quién se le escribe, según el nombre de la campaña', 12.5, INK, w=600)
S.t(0, 30, '% de los mensajes, del gasto y de las conversiones del mismo día', 10.5, SEC)
MS = [('p_env', MARK2, 'Mensajes'), ('p_costo', BLUE, 'Gasto'), ('p_conv', GREEN, 'Conversiones')]
lx = 0
for k, col, lab in MS:
    S.rect(lx, 40, 10, 10, col); S.t(lx + 14, 49, lab, 11, TXT); lx += 14 + len(lab) * 6.2 + 16
X0, X1, VMAX = 160, 372, 50
sx = lambda v: X0 + (X1 - X0) * v / VMAX
TOP, RH, BH = 70, 36, 7.5
for v in (0, 25, 50):
    S.line(sx(v), TOP - 6, sx(v), TOP + RH * len(ORD) - 6)
    S.t(sx(v), TOP + RH * len(ORD) + 6, f'{v} %', 10.5, SEC, 'middle')
for i, g in enumerate(ORD):
    y = TOP + RH * i
    cold = g in ('nunca', 'ex')
    S.t(X0 - 8, y + 14, LAB[g], 11, INK if cold else TXT, 'end', 600 if cold else 400)
    for j, (k, col, _) in enumerate(MS):
        v = G[g][k]; yy = y + j * (BH + 2)
        S.rect(X0, yy, max(sx(v) - X0, 1), BH, col)
        if cold or (g in ('activos', 'leads') and k == 'p_conv'):
            S.t(sx(v) + 4, yy + 7.3, f'{v:.0f} %' if v >= 1 else f'{v:.1f} %', 10.5, INK if cold else SEC, w=600 if cold else 400)
# llave de los dos grupos fríos
fr_env = G['nunca']['p_env'] + G['ex']['p_env']; fr_c = G['nunca']['p_costo'] + G['ex']['p_costo']; fr_cv = G['nunca']['p_conv'] + G['ex']['p_conv']
# ---------- panel derecho ----------
RX = 436
pno = 100 * no['usuarios'] / tot['usuarios']
S.t(RX, 14, f'{M(tot["usuarios"])} M personas recibieron algo en nueve meses', 12.5, INK, w=600)
BW = W - RX
S.rect(RX, 24, BW * pno / 100 - 1, 26, BLUE); S.rect(RX + BW * pno / 100 + 1, 24, BW * (100 - pno) / 100 - 1, 26, MARK)
S.t(RX + 8, 41.5, f'No respondieron: {M(no["usuarios"])} M ({pno:.0f} %)', 11.5, '#FFFFFF', w=600)
S.t(W - 6, 41.5, f'Sí: {M(si["usuarios"])} M', 11.5, '#FFFFFF', 'end', 600)
S.t(RX, 68, 'Cómo son, por persona, en nueve meses', 11.5, SEC, w=600)
S.rect(RX, 76, 10, 10, BLUE); S.t(RX + 14, 85, 'No respondieron', 11, TXT)
S.rect(RX + 120, 76, 10, 10, MARK); S.t(RX + 134, 85, 'Sí respondieron', 11, TXT)
pp = lambda d, k: d[k] / d['usuarios']
MET = [('Mensajes recibidos por persona', pp(no, 'msgs'), pp(si, 'msgs'), lambda v: f'{v:.0f}'),
       ('Push recibidos por persona', pp(no, 'push'), pp(si, 'push'), lambda v: f'{v:.0f}'),
       ('Veces que vieron un in-app', pp(no, 'inapp'), pp(si, 'inapp'), lambda v: f'{v:.2f}' if v < 0.1 else f'{v:.1f}'),
       ('WhatsApp que sí les llega', 100 * no['wa_ent'] / no['wa'], 100 * si['wa_ent'] / si['wa'], lambda v: f'{v:.0f} %'),
       ('Personas con conversión', 100 * no['conv'] / no['usuarios'], 100 * si['conv'] / si['usuarios'], lambda v: f'{v:.2f} %' if v < 1 else f'{v:.0f} %')]
LX0, LX1 = RX + 4, W - 46
RY, RRH = 104, 57
for i, (lab, a, b, f) in enumerate(MET):
    y = RY + RRH * i
    S.t(RX, y + 9, lab, 11.5, INK, w=600)
    mx = max(a, b)
    for j, (v, col) in enumerate([(a, BLUE), (b, MARK)]):
        yy = y + 16 + j * 13
        wv = max((LX1 - LX0) * v / mx, 1.5)
        S.rect(LX0, yy, wv, 10, col)
        S.t(LX0 + wv + 5, yy + 9, f(v), 11, INK if j == 0 else SEC, w=600 if j == 0 else 400)
S.line(RX - 18, 6, RX - 18, 410, GRID)
SVG = S.done()

c_fr = (G['nunca']['costo'] + G['ex']['costo'])
guarda(48, dict(
    kind='grafica',
    titulo='Tres de cada cuatro personas no respondieron en nueve meses, y hoy no sabemos cuántas son ex clientes y cuántas nunca activaron',
    que=f'De todo, casi todo promocional: Tasa 0, referidos, descuentos y lanzamientos. A las {M(no["usuarios"])} M personas que no respondieron les llegaron {M(no["msgs"])} M mensajes: {100*no["email"]/no["msgs"]:.0f} % correos, {100*no["push"]/no["msgs"]:.0f} % push y {100*no["wa"]/no["msgs"]:.0f} % WhatsApp.',
    quien='Todos los equipos. Ningún dato liga a la persona que no responde con el equipo que le escribe.',
    a_quien=f'Por el nombre de la campaña: leads y registrados recientes reciben {G["leads"]["p_env"]:.0f} % de los mensajes, activos y recurrentes {G["activos"]["p_env"]:.0f} %, leads que nunca activaron {G["nunca"]["p_env"]:.0f} % y ex clientes inactivos {G["ex"]["p_env"]:.0f} %. La persona que no responde no trae su segmento.',
    lecturas=[
        f'{M(no["usuarios"])} M de {M(tot["usuarios"])} M personas no abrieron un push, no leyeron un WhatsApp ni hicieron clic en un correo o in-app en nueve meses. Recibieron {M(no["msgs"])} M mensajes que costaron {M(no["costo"])} M MXN, y solo {fmt(no["conv"])} convirtieron ({100*no["conv"]/no["usuarios"]:.2f} %).',
        f'Casi no usan la app: {pp(no,"inapp"):.2f} vistas de in-app y {pp(no,"push"):.0f} push por persona, contra {pp(si,"inapp"):.1f} y {pp(si,"push"):.0f} de quien responde. Y a muchos ya no les llega el WhatsApp: {100*no["wa_ent"]/no["wa"]:.0f} % de entrega contra {100*si["wa_ent"]/si["wa"]:.0f} %.',
        f'Por el nombre de la campaña, {fr_env:.0f} % de los mensajes busca a dos grupos distintos: leads que nunca activaron ({M(G["nunca"]["env"])} M mensajes) y ex clientes ({M(G["ex"]["env"])} M). Cuestan {M(c_fr)} M MXN, {fr_c:.0f} % del gasto, y traen {fr_cv:.1f} % de las conversiones.',
    ],
    causa='Braze no guarda el segmento de cada persona: el grupo solo se ve en el nombre de la campaña. Por eso no podemos separar, entre quienes no responden, al ex cliente que vale la pena recuperar del lead que nunca activó.',
    sowhat='Para recuperar hay que saber a quién: el ex cliente con historial y el lead que nunca activó necesitan canal, presupuesto y número de mensajes distintos.',
    fuente=f'Fuente: Braze E7b (respuesta por persona) y E1 (campaña, canal y mes), enero a septiembre 2026. Responder = clic en correo, abrir push, leer WhatsApp o clic en in-app. En los últimos 90 días no responde {100*D["e9b"]["no"]["usuarios"]/D["e9b"]["tot"]["usuarios"]:.0f} % (E9b). Conversión del mismo día: se reparte entre los mensajes que la persona recibió ese día. Correo 0.05 MXN por enviado, WhatsApp 1.00 MXN por entregado.',
    svg=SVG,
))
