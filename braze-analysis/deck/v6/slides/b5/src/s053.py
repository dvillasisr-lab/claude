"""Lámina 53: grupo de audiencia x canal. Color = responde o no lo mínimo aceptable; números = respuesta y MXN por conversión del mismo día
(o conversiones por mil mensajes en push e in-app, que no cuestan). Columna izquierda: mensajes y parte de las conversiones. Fuente E1."""
from b5_svg import *

GC = D['gc']; G = D['grupos']
MIN = {'email': 0.3, 'push notification': 0.75, 'whatsapp': 60.0, 'in-app': 10.0}
CH = [('email', 'Correo', 'clic'), ('push notification', 'Push', 'abre'), ('whatsapp', 'WhatsApp', 'leído'), ('in-app', 'In-app', 'clic')]
ORD = ['activos', 'leads', 'nunca', 'ex', 'nuevos', 'cobranza', 'transaccional']
LAB = {'activos': 'Activos y recurrentes', 'leads': 'Leads y registrados', 'nunca': 'Leads que nunca activaron', 'ex': 'Ex clientes inactivos',
       'nuevos': 'Nuevos y onboarding', 'cobranza': 'Cobranza', 'transaccional': 'Avisos transaccionales'}
REC = {'activos': ['Push e in-app primero;', 'el WhatsApp sí rinde'], 'leads': ['Correo y push;', 'WhatsApp solo a quien lo lee'],
       'nunca': ['Un intento corto por correo o push;', 'si no responde, sin promociones'], 'ex': ['Correo y, si tiene app, push e in-app;', 'WhatsApp solo si leyó uno en 90 días'],
       'nuevos': ['Responde en todos;', 'in-app y correo primero'], 'cobranza': ['Correo y push;', 'ya responde'], 'transaccional': ['Correo y push;', 'ya responde']}
S = Svg('Matriz de grupo de audiencia por canal: si responde lo mínimo aceptable, la respuesta y los pesos por conversión del mismo día, con el canal recomendado para cada grupo.')
CX0, CW, TOP, RH = 168, 96, 50, 45
RX = CX0 + CW * 4 + 12
S.rect(0, 2, 12, 12, GREENL, ' fill-opacity="0.55"'); S.t(17, 12, 'Responde lo mínimo aceptable', 11, TXT)
S.rect(200, 2, 12, 12, MARK2, ' fill-opacity="0.45"'); S.t(217, 12, 'No llega al mínimo', 11, TXT)
S.t(360, 12, 'Arriba: respuesta. Abajo: MXN por conversión del mismo día.', 10.5, SEC)
S.t(0, TOP - 10, 'Grupo y mensajes', 10.5, SEC, w=600)
for j, (c, lab, _) in enumerate(CH):
    S.t(CX0 + CW * j + CW / 2, TOP - 10, lab, 11.5, INK, 'middle', 600)
S.t(RX, TOP - 10, 'Por dónde llegarle', 11.5, INK, w=600)
for i, g in enumerate(ORD):
    y = TOP + RH * i
    cold = g in ('ex', 'nunca')
    S.t(0, y + 18, LAB[g], 11.5, INK, w=600)
    S.t(0, y + 33, f'{M(G[g]["env"], 0)} M mensajes · {G[g]["p_conv"]:.0f} % de conv.' if G[g]['p_conv'] >= 1 else f'{M(G[g]["env"], 0)} M mensajes · {G[g]["p_conv"]:.1f} %', 10.5, SEC)
    for j, (c, lab, verb) in enumerate(CH):
        x = CX0 + CW * j
        k = f'{g}|{c}'
        if k not in GC or GC[k]['base'] < 50000:
            S.t(x + CW / 2, y + RH / 2 + 4, 'no se usa', 10.5, SEC, 'middle'); continue
        d = GC[k]; ok = d['resp'] >= MIN[c]
        S.rect(x + 2, y + 2, CW - 4, RH - 4, GREENL if ok else MARK2, f' fill-opacity="{0.55 if ok else 0.45}"')
        r = d['resp']; rs = f'{r:.2f} %' if r < 10 else f'{r:.0f} %'
        S.t(x + CW / 2, y + 19, f'{rs} {verb}', 11.5, INK, 'middle', 600)
        if c in ('email', 'whatsapp'):
            S.t(x + CW / 2, y + 34, f'{fmt(d["mxn_conv"])} MXN', 10.5, TXT, 'middle')
        else:
            S.t(x + CW / 2, y + 34, f'{d["conv_mil"]:.1f} conv. por mil', 10.5, TXT, 'middle')
    S.t(RX, y + 18, REC[g][0], 11, INK if cold else TXT, w=600 if cold else 400)
    S.t(RX, y + 33, REC[g][1], 11, INK if cold else TXT, w=600 if cold else 400)
    if i: S.line(0, y, CX0 - 6, y, GRID)
FY = TOP + RH * len(ORD) + 16
S.t(0, FY, 'Mínimo aceptable: 3 clics por cada mil correos, 7.5 aperturas por cada mil push, 6 de cada 10 WhatsApp leídos o 1 de cada 10 in-app con clic.', 10.5, SEC)
S.t(0, FY + 15, 'Push e in-app no cuestan (0 MXN): abajo van sus conversiones del mismo día por cada mil mensajes. Solo llegan a quien tiene la app.', 10.5, SEC)
SVG = S.done()

g = GC
guarda(53, dict(
    kind='grafica',
    titulo='Leads y registrados reciben más mensajes que nadie y casi no convierten; a cada grupo le conviene un canal distinto',
    que='Promociones y recordatorios por los cuatro canales: correo, push, WhatsApp e in-app.',
    quien='A leads y registrados: Marketing y Product Growth. A ex clientes: Product Growth y Marketing. A activos: Sales, Marketing y Product Growth.',
    a_quien='Siete grupos según el nombre de la campaña: activos y recurrentes, leads y registrados, leads que nunca activaron, ex clientes inactivos, nuevos, cobranza y avisos transaccionales.',
    lecturas=[
        f'Leads y registrados reciben {G["leads"]["p_env"]:.0f} % de los mensajes y traen {G["leads"]["p_conv"]:.0f} % de las conversiones del mismo día; activos y recurrentes reciben {G["activos"]["p_env"]:.0f} % y traen {G["activos"]["p_conv"]:.0f} %.',
        f'Ex clientes: el correo queda abajo del mínimo ({g["ex|email"]["resp"]:.2f} % de clic) pero cuesta {g["ex|email"]["mxn_conv"]:.0f} MXN por conversión, contra {g["ex|whatsapp"]["mxn_conv"]:.0f} por WhatsApp. Push e in-app sí responden, pero solo a quien tiene la app.',
        f'Leads que nunca activaron: el correo tiene clics ({g["nunca|email"]["resp"]:.2f} %) pero casi no convierte, {g["nunca|email"]["mxn_conv"]:.0f} MXN por conversión, y WhatsApp {g["nunca|whatsapp"]["mxn_conv"]:.0f}. Su push abre {g["nunca|push notification"]["resp"]:.2f} %, debajo del mínimo.',
    ],
    causa='Cada equipo usa el canal que acostumbra para su campaña y no el que cada grupo sí usa, porque Braze no guarda la última respuesta de la persona en cada canal ni si tiene la app.',
    sowhat='El canal se decide por grupo y por costo por conversión, no por costumbre del equipo: el más barato que ese grupo sí usa.',
    fuente='Fuente: Braze E1 (campaña, canal y mes), enero a septiembre 2026; grupos por el nombre de la campaña. Correo 0.05 MXN por enviado, WhatsApp 1.00 MXN por entregado. Conversión del mismo día: se reparte entre los mensajes del día; es referencia. Se dejó de usar la etapa "Prospects" del golden dataset porque 42 % de esas personas convirtió en el periodo.',
    svg=SVG,
))
