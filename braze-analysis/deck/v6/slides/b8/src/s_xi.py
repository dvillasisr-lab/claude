# Sección XI (medición y gobierno): láminas 86 a 90. Uso: python3 s_xi.py (desde cualquier carpeta).
import re, pandas as pd, numpy as np
from kit import *
import datos, sin_dueno
D = datos.ROOT + 'data/'

# ------------------------------------------------------------------ 86. Grupo de control
e13 = pd.read_csv(D + 'e13_lift_control.csv')
n_canvas = e13.canvas_id.nunique()
ctl = e13[e13.grupo == 'control'].groupby('canvas_id').usuarios.sum()
n_ctl = len(ctl); n_acc = int((ctl < 1000).sum()); acc_max = int(ctl[ctl < 1000].max())
real = e13[e13.canvas_id == ctl.idxmax()].set_index('grupo')
rc, rt = real.loc['control'], real.loc['test']
sh_ctl = rc.usuarios / (rc.usuarios + rt.usuarios)
k = lambda r, col: 100 * r[col] / r.usuarios
gasto9 = datos.e1().costo.sum()
print('86', n_canvas, n_ctl, n_acc, acc_max, rc.usuarios, rt.usuarios, round(sh_ctl * 100, 1), [round(k(r, c_), 1) for r in (rc, rt) for c_ in ('usuarios_abrieron', 'usuarios_solicitaron', 'usuarios_convirtieron')], m(gasto9, 1))

o = svg_open(f'Uno de {n_canvas:,} Canvas tuvo grupo de control de tamaño real. En ese caso el grupo sin mensaje convirtió {k(rc, "usuarios_convirtieron"):.1f} % y quien recibió {k(rt, "usuarios_convirtieron"):.1f} %.')
o.append(t(0, 52, '1', 56, INK, 700) + t(36, 52, f'de {n_canvas:,}', 30, INK, 600))
o.append(t(0, 84, 'Canvas con un grupo de control', 12.5, TXT))
o.append(t(0, 100, 'de tamaño suficiente para medir', 12.5, TXT))
o.append(t(0, 116, 'en nueve meses', 12.5, TXT))
# tabla dibujada
TX = [258, 450, 512]
o.append(t(TX[0], 22, 'TAMAÑO DEL GRUPO DE CONTROL', 10.5, SEC, 600))
o.append(t(TX[1] + 40, 22, 'CANVAS', 10.5, SEC, 600, 'end'))
o.append(t(TX[2], 22, 'QUÉ SE PUEDE CONCLUIR', 10.5, SEC, 600))
o.append(f'<line x1="{TX[0]}" y1="30" x2="780" y2="30" stroke="{INK}" stroke-width="1.2"/>')
filas = [('Sin grupo de control', f'{n_canvas - n_ctl:,}', 'Nada: la conversión mezcla a quien', 'iba a comprar de todos modos', TXT),
         (f'1 a {acc_max} personas', f'{n_acc}', 'Nada: son personas marcadas', 'por accidente, no una medición', TXT),
         (f'{rc.usuarios / 1e3:.1f} mil personas ({sh_ctl * 100:.0f} %)', '1', 'Cuánto vendió el mensaje:', 'el único caso que se puede leer', BLUE)]
for i, (a, b, c1, c2, col) in enumerate(filas):
    y = 50 + i * 40
    w = 600 if col == BLUE else 400
    o.append(t(TX[0], y, a, 12.5, INK if col == BLUE else TXT, w))
    o.append(t(TX[1] + 40, y, b, 13, col if col == BLUE else INK, 600, 'end'))
    o.append(t(TX[2], y, c1, 12, TXT) + t(TX[2], y + 15, c2, 12, TXT))
    o.append(f'<line x1="{TX[0]}" y1="{y + 23}" x2="780" y2="{y + 23}" stroke="{GRID}" stroke-width="1"/>')
# barras pareadas del único caso real
o.append(t(0, 205, 'El único caso real: Cash a plazos a clientes activos (B0301), febrero a septiembre', 13, INK, 600))
o.append(f'<rect x="0" y="219" width="11" height="11" rx="2" fill="{BLUE}"/>' + t(17, 229, f'Grupo de control: {rc.usuarios / 1e3:.1f} mil personas sin el mensaje', 12, TXT))
o.append(f'<rect x="340" y="219" width="11" height="11" rx="2" fill="{MARK}"/>' + t(357, 229, f'Recibieron el mensaje: {rt.usuarios / 1e3:.1f} mil', 12, TXT))
X0, X1 = 230, 690; sx = lambda v: X0 + (X1 - X0) * v / 100
for v in range(0, 101, 20):
    o.append(f'<line x1="{sx(v):.1f}" y1="244" x2="{sx(v):.1f}" y2="392" stroke="{GRID}" stroke-width="1"/>')
    o.append(t(sx(v), 408, f'{v} %', 11, SEC, 400, 'middle'))
mets = [('Abrió algún mensaje de Kueski', 'usuarios_abrieron'), ('Pidió un crédito', 'usuarios_solicitaron'), ('Recibió el crédito (convirtió)', 'usuarios_convirtieron')]
for i, (lab, col) in enumerate(mets):
    y = 252 + i * 48
    o.append(t(X0 - 10, y + 17, lab, 12.5, INK if i == 2 else TXT, 600 if i == 2 else 400, 'end'))
    for j, (r, fill) in enumerate(((rc, BLUE), (rt, MARK))):
        v = k(r, col); yy = y + j * 17
        o.append(f'<rect x="{X0}" y="{yy}" width="{sx(v) - X0:.1f}" height="14" rx="2" fill="{fill}"/>')
        o.append(t(sx(v) + 6, yy + 11.5, f'{v:.1f} %', 12, INK, 600 if j == 0 else 400))
o.append('</svg>')
save(86, dict(kind='grafica',
    titulo=f'Solo uno de {n_canvas:,} Canvas tuvo un grupo de control de verdad: sin él, nadie puede decir cuánto vende Braze',
    que='Toda la promoción: Tasa 0, referidos, recordatorios de terminar el registro, cross sell de KPay a Cash y reactivación. Nada se compara contra un grupo que no lo recibe.',
    quien='Todos los equipos. El único control real es de Product Growth (en el nombre aparece como Lending).',
    a_quien='En el único caso medido, clientes activos de Cash a los que se les recordó tomar Cash a plazos (B0301).',
    lecturas=[f'Grupo de control: se aparta al azar 5 a 10 % de la audiencia y no se le manda nada. Lo que convierte quien recibió menos lo que convierte ese grupo es lo que vendió el mensaje.',
              f'{n_ctl} Canvas tienen personas en control, pero {n_acc} tienen de 1 a {acc_max}: son marcas por accidente. Solo B0301 apartó {rc.usuarios / 1e3:.1f} mil personas ({sh_ctl * 100:.0f} %).',
              f'En B0301 el control convirtió {k(rc, "usuarios_convirtieron"):.1f} % y quien recibió {k(rt, "usuarios_convirtieron"):.1f} %. Un caso no prueba que el mensaje no venda, pero no podemos dar por hecho que vende.'],
    causa=f'El grupo de control no es obligatorio y nadie es dueño de medir. Además, {k(rc, "usuarios_abrieron"):.0f} % del control abrió otros mensajes de Kueski: ni ese grupo quedó limpio.',
    sowhat=f'Ninguna venta atribuida a Braze se puede defender hoy ({m(gasto9, 1)} M MXN gastados en nueve meses). Primero se prende el grupo de control nativo de Braze en toda promoción.',
    fuente='Fuente: Braze, Canvas por grupo de prueba y de control (E13), enero a septiembre 2026; gasto de E1 con WhatsApp a 1.00 MXN por entregado y email a 0.05 por enviado. Convirtió = recibió crédito en la ventana del Canvas. "Abrió algún mensaje" es de cualquier mensaje de Kueski en el periodo.',
    svg=''.join(o)))

# ------------------------------------------------------------------ 87. Veriff
e7 = pd.read_csv(D + 'e7c_abren_vs_no_abren.csv'); e9 = pd.read_csv(D + 'e9a_abren_vs_no_abren_ventanas.csv')
def conv(df, pat, canal, w):
    r = df[df.familia.str.contains(pat, regex=False) & (df.canal == canal)].iloc[0]
    ab, no = (r.abrieron_y_convirtieron, r.no_abrieron_y_convirtieron) if w == 'e7' else (r['ab_conv_' + w], r['no_conv_' + w])
    return 100 * ab / r.abrieron, 100 * no / (r.envios_usuario_dia - r.abrieron)
V = 'B0000-CANVAS-Leads_LeftFunnel-Retargeting_Veriff'; T27 = 'Acquisition-KPay-T2727-CANVAS-Prospect_FaltaVeriff-RetargetingVeriff-Prod'
rows = [('Cifra que compartió el equipo', 'definición sin documentar', (22.0, 17.0), True),
        ('Marketing B0000, correo', 'a 7 días', conv(e9, V, 'email', '7'), False),
        ('Marketing B0000, correo', 'a 90 días', conv(e9, V, 'email', '90'), False),
        ('Marketing B0000, push', 'a 7 días', conv(e9, V, 'push notification', '7'), False),
        ('Marketing B0000, push', 'a 90 días', conv(e9, V, 'push notification', '90'), False),
        ('Acquisition T2727, correo', 'a 7 días', conv(e9, T27, 'email', '7'), False),
        ('Acquisition T2727, correo', 'a 90 días', conv(e9, T27, 'email', '90'), False)]
print('87', [(a, b, round(x[0], 1), round(x[1], 1), round(x[0] / x[1], 2)) for a, b, x, _ in rows])
c = datos.load_c()
ve = c[c.fam.str.contains(V, regex=False) & (c.canal == 'email')].iloc[0]
lb = pd.read_csv(datos.ROOT + 'hallazgos/muestra_l_familias_baja.csv')
nuevos = lb[(lb.clave.str.contains(V, regex=False)) & (lb.cohorte_limpia == 1)].usuarios.sum()
print('87 veriff email', ve.env, ve.resp, ve.bajas_mil, nuevos)

o = svg_open('Conversión de quien abre contra quien no abre el recordatorio de terminar la verificación, por fuente y ventana.')
o.append(f'<circle cx="6" cy="12" r="5.5" fill="{MARK}"/>' + t(17, 16.5, 'No abrió el mensaje', 12, TXT))
o.append(f'<circle cx="176" cy="12" r="5.5" fill="{BLUE}"/>' + t(187, 16.5, 'Abrió el mensaje', 12, TXT))
o.append(t(780, 16.5, 'Quien abre convierte', 11.5, SEC, 400, 'end'))
X0, X1 = 250, 640; sx = lambda v: X0 + (X1 - X0) * v / 25
AX = 392
for v in range(0, 26, 5):
    o.append(f'<line x1="{sx(v):.1f}" y1="34" x2="{sx(v):.1f}" y2="{AX}" stroke="{GRID}" stroke-width="1"/>')
    o.append(t(sx(v), AX + 15, f'{v} %', 11, SEC, 400, 'middle'))
o.append(t(X1, AX + 15, '', 11, SEC))
o.append(t(450, 418, 'Conversión: personas que recibieron crédito de Cash por cada 100 que recibieron el mensaje', 11, SEC, 400, 'middle'))
RH = 50
for i, (a, b, (ab, no), team) in enumerate(rows):
    yc = 52 + i * RH - (0 if i == 0 else 8) + (0 if i < 1 else 0)
    if i >= 1: yc = 52 + 58 + (i - 1) * 46
    o.append(t(X0 - 14, yc - 2, a, 12.5, INK, 600 if team else 400, 'end'))
    o.append(t(X0 - 14, yc + 13, b, 11.5, SEC, 400, 'end'))
    o.append(f'<line x1="{sx(no):.1f}" y1="{yc + 4}" x2="{sx(ab):.1f}" y2="{yc + 4}" stroke="{MARK2}" stroke-width="3"/>')
    o.append(f'<circle cx="{sx(no):.1f}" cy="{yc + 4}" r="6" fill="{MARK}" stroke="#fff" stroke-width="2"/>')
    o.append(f'<circle cx="{sx(ab):.1f}" cy="{yc + 4}" r="6" fill="{INK if team else BLUE}" stroke="#fff" stroke-width="2"/>')
    o.append(t(sx(no) - 10, yc + 8.5, f'{no:.1f}', 11.5, TXT, 400, 'end', True))
    o.append(t(sx(ab) + 10, yc + 8.5, f'{ab:.1f}', 11.5, INK, 600, 'start', True))
    o.append(t(780, yc + 8.5, f'{ab / no:.1f} veces', 12.5, INK if team else BLUE, 600, 'end'))
    if i == 0:
        o.append(f'<line x1="0" y1="{yc + 29}" x2="780" y2="{yc + 29}" stroke="{GRID}" stroke-width="1"/>')
o.append('</svg>')
save(87, dict(kind='grafica',
    titulo='La conversión del recordatorio de verificación que usa el equipo no sale en los datos: cambia la definición, no el resultado',
    que='Recordatorio de terminar el registro: correos y push a quien empezó a registrarse y no terminó la verificación de identidad (Veriff).',
    quien='Marketing (B0000) y Acquisition (T2727), que en los datos cae en Others.',
    a_quien='Leads que dejaron el registro a medias y prospectos de KPay que no terminaron la verificación.',
    lecturas=[f'El equipo compartió que quien abre convierte 22 % y quien no 17 %. En los datos, por correo sale {rows[1][2][0]:.1f} % contra {rows[1][2][1]:.1f} % a 7 días y {rows[2][2][0]:.1f} % contra {rows[2][2][1]:.1f} % a 90 días.',
              f'Quien abre convierte {rows[1][2][0] / rows[1][2][1]:.1f} veces más por correo y {rows[3][2][0] / rows[3][2][1]:.1f} veces por push; en la cifra del equipo, 1.3 veces. Cambia el nivel, no la ventaja de abrir.',
              f'El recordatorio sí funciona: {ve.resp * 1000:.0f} clics por cada mil correos, pero manda hasta dos correos al día y {nuevos / 1e3:.1f} mil personas nuevas se dieron de baja con él.'],
    causa='No hay una definición única de conversión: aquí es crédito otorgado en 7 días por día de envío; la del equipo probablemente es terminar la verificación o una ventana más larga.',
    sowhat='Fijar con Datos una sola definición de conversión (qué paso y en cuántos días) antes de comparar campañas; si no, dos equipos llegan a conclusiones opuestas.',
    fuente=f'Fuente: Braze, abren contra no abren por campaña (E7c) y por ventana de 7 a 90 días (E9a), enero a septiembre 2026; bajas de personas nuevas de la muestra L. La cifra de 22 % contra 17 % no está en ninguna extracción: viene de la conversación con el equipo. Quien abre ya venía más interesado: la diferencia no es efecto del mensaje.',
    svg=''.join(o)))

# ------------------------------------------------------------------ 88. Sin dueño ni ticket
g, tot = sin_dueno.datos()
tm = g.groupby('tema').agg(n=('env', 'size'), env=('env', 'sum'), c=('c', 'sum'))
print('88', tot, tm)
OR = ['Transaccional KPay', 'NewProducts (BillPay, TopUps)', 'KCash (desembolso, rechazo)', 'Shopping', 'QA y pruebas', 'Otros sin dueño']
LAB = {'Transaccional KPay': 'Avisos de pago y contrato KPay', 'NewProducts (BillPay, TopUps)': 'Lanzamientos BillPay y TopUps',
       'KCash (desembolso, rechazo)': 'Avisos de KCash', 'Shopping': 'Recomendaciones de Shopping', 'QA y pruebas': 'Pruebas internas',
       'Otros sin dueño': 'Otros sin nombre de equipo'}
TEM = [('promocional', BLUE, 'Promoción'), ('transaccional y operativa', MARK, 'Transaccional y operativa'), ('pruebas internas', MARK2, 'Pruebas internas')]
ct = pd.crosstab(g.orig, g.tema, values=g.env, aggfunc='sum').fillna(0).reindex(OR)
cn = g.groupby('orig').size().reindex(OR)
o = svg_open(f'Mensajes de comunicaciones sin equipo dueño ni ticket por origen y tema: {m(tot["env"], 1)} M mensajes; {m(tm.loc["promocional", "env"], 1)} M son promoción.')
x = 0
for key, col, lab in TEM:
    o.append(f'<rect x="{x}" y="6" width="12" height="12" rx="2" fill="{col}"/>' + t(x + 18, 16.5, f'{lab} {m(tm.loc[key, "env"], 1)} M', 12, INK, 600 if key == 'promocional' else 400))
    x += {'promocional': 160, 'transaccional y operativa': 245, 'pruebas internas': 0}[key]
X0, X1 = 222, 640; VM = 32e6; sx = lambda v: X0 + (X1 - X0) * v / VM
o.append(t(X0 - 10, 50, 'Origen, según el nombre', 11, SEC, 600, 'end'))
o.append(t(780, 50, 'Comunicaciones', 11, SEC, 600, 'end'))
AX = 382
for v in range(0, 31, 10):
    o.append(f'<line x1="{sx(v * 1e6):.1f}" y1="58" x2="{sx(v * 1e6):.1f}" y2="{AX}" stroke="{GRID}" stroke-width="1"/>')
    o.append(t(sx(v * 1e6), AX + 15, f'{v} M' if v else '0', 11, SEC, 400, 'middle'))
o.append(t(X1, AX + 32, 'mensajes enviados de enero a septiembre de 2026', 11, SEC, 400, 'end'))
for i, orig in enumerate(OR):
    yc = 80 + i * 52; x = X0
    o.append(t(X0 - 10, yc + 4.5, LAB[orig], 12.5, TXT, 400, 'end'))
    for key, col, lab in TEM:
        v = ct.loc[orig].get(key, 0)
        if v <= 0: continue
        w = sx(v) - X0
        o.append(f'<rect x="{x:.1f}" y="{yc - 10}" width="{max(w - 1.5, 1):.1f}" height="20" rx="2" fill="{col}"/>')
        x += w
    totv = ct.loc[orig].sum()
    o.append(t(x + 6, yc + 4.5, f'{m(totv, 1)} M', 12, INK, 600))
    o.append(t(780, yc + 4.5, f'{cn[orig]}', 12.5, INK, 400, 'end'))
o.append('</svg>')
promo_bp = g[g.communication_name.str.contains('BillPay_Intro_Full_Rollout') & g.communication_name.str.contains('-E-')].env.sum()
bp_bajas = datos.e1().pipe(lambda d: d[d.communication_name.str.contains('BillPay_Intro_Full_Rollout') & d.communication_name.str.contains('-E-')].email_unsubscribe.sum())
save(88, dict(kind='grafica',
    titulo=f'Uno de cada ocho mensajes sale de comunicaciones sin equipo dueño ni ticket, y casi la mitad de ese volumen es promoción',
    que='Avisos de pago, contratos, estados de cuenta, desembolsos y rechazos; promoción de BillPay y TopUps, recomendaciones de Shopping e invitaciones B2C; pruebas internas.',
    quien='Nadie: en Braze el equipo dice "Not Tracked". Por el nombre se reconoce a NewProducts, Shopping, avisos de KPay y KCash y QA (en el deck, Others).',
    a_quien='Clientes de KPay y Cash para los avisos; casi toda la base en los lanzamientos de BillPay.',
    lecturas=[f'Dueño es el equipo que responde por la comunicación en Braze; ticket es el código en el nombre (B0211, T2727) que dice quién la pidió y cómo se mide. {tot["nt"]} no tienen ninguno.',
              f'{tot["activas"]} de ellas mandaron algo en 2026: {m(tot["env"], 1)} M mensajes ({100 * tot["env"] / tot["env_e1"]:.1f} % del total) y {m(tot["c"], 1)} M MXN. Promoción: {tm.loc["promocional", "n"]} comunicaciones, {m(tm.loc["promocional", "env"], 1)} M mensajes y {m(tm.loc["promocional", "c"], 1)} M MXN.',
              f'El correo de lanzamiento de BillPay salió una vez a {m(promo_bp, 1)} M personas y nadie respondió por sus {bp_bajas / 1e3:.0f} mil bajas de correo.'],
    causa='Activar una comunicación no exige equipo ni ticket. Lo transaccional sin dueño es un riesgo (nadie revisa si deja de llegar); lo promocional sin dueño es dinero sin responsable.',
    sowhat='Equipo y ticket obligatorios para activar: sin ellos nadie puede apagar, corregir ni medir lo que más pesa.',
    fuente='Fuente: Braze, catálogo de comunicaciones (E2: equipo y ticket) cruzado con envíos por comunicación, mes y canal (E1), enero a septiembre 2026; WhatsApp a 1.00 MXN por entregado, email a 0.05 por enviado. Tema y origen asignados por el nombre (el guion tenía 88, 41 y 82 comunicaciones por tema; con esta clasificación salen 84, 39 y 87). Bajas de BillPay = eventos de baja de email en E1.',
    svg=''.join(o)))

# ------------------------------------------------------------------ 89. Bajas solo en email
d1 = datos.e1()
vol = d1.groupby('canal').envios.sum()
e17 = pd.read_csv(D + 'e17_contactable.csv')
wa_baja = e17[(e17.canal == 'whatsapp') & (e17.wa_unsubscribed == True)].envios.sum()
push_off = e17[(e17.canal == 'push notification') & (e17.notifications_enabled == False)].envios.sum()
push_baja = e17[(e17.canal == 'push notification') & (e17.push_unsubscribed == True)].envios.sum()
e4 = pd.read_csv(D + 'e4a_serie_semana_mes_canal.csv'); bm = e4[(e4.grano == 'mes') & (e4.canal == 'email')]
baja_unicas = pd.read_csv(D + 'e5_cohorte_baja.csv').usuarios_baja.sum()
print('89', (vol / 1e6).round(1).to_dict(), wa_baja, push_off, push_baja, bm.bajas_email_usuarios.sum())
SI, NO, PAR = f'<b style="color:{GREEN}">Sí</b>', f'<b style="color:{INK}">No</b>', f'<span style="color:{SEC}">Solo bandera</span>'
tb = [('Email', vol['email'], SI, SI, 'Clic', SI, SI),
      ('Push', vol['push notification'], SI, f'<span style="color:{SEC}">No aplica</span>', 'Apertura', NO, PAR),
      ('WhatsApp', vol['whatsapp'], SI, SI, 'Lectura', NO, PAR),
      ('In-app', vol['in-app'], f'<span style="color:{SEC}">Impresión</span>', f'<span style="color:{SEC}">No aplica</span>', 'Clic', NO, f'<span style="color:{SEC}">No aplica</span>')]
h = ['<table><tr><th>Canal</th><th class="num">Mensajes, 9 meses</th><th>Enviado</th><th>Entregado</th><th>Respuesta</th><th>Baja con fecha y campaña</th><th>Estado de suscripción hoy</th></tr>']
for r in tb:
    h.append(f'<tr><td><b>{r[0]}</b></td><td class="num">{m(r[1], 1)} M</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td><td>{r[6]}</td></tr>')
h.append('</table>')
h.append(f'<div style="margin-top:1.6cqi;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2cqi">'
         f'<div><div class="big" style="font-size:3cqi">{baja_unicas / 1e3:.0f} mil</div><div class="bigl">personas que se dieron de baja del email en nueve meses: lo único que podemos contar</div></div>'
         f'<div><div class="big" style="font-size:3cqi;color:{BLUE}">{m(wa_baja, 1)} M</div><div class="bigl">WhatsApp mandados a personas que la bandera marca como dadas de baja de WhatsApp</div></div>'
         f'<div><div class="big" style="font-size:3cqi;color:{MARK}">Sin dato</div><div class="bigl">personas que apagaron las notificaciones o bloquearon el WhatsApp por una campaña</div></div></div>')
save(89, dict(kind='html',
    titulo='Solo el email registra quién se da de baja y por qué campaña; en push y WhatsApp no sabemos quién se fue',
    que=f'Todo lo que sale por push y WhatsApp: {m(vol["push notification"], 0)} M push y {m(vol["whatsapp"], 0)} M WhatsApp en nueve meses.',
    quien='Todos los equipos; WhatsApp sobre todo Marketing y Product Growth.',
    a_quien='Toda la base. Ejemplo: rescate Tasa 0 por push a anónimos (Marketing B0171), 8.9 M push con 5.6 aperturas por cada mil: no sabemos cuántos apagaron las notificaciones por él.',
    lecturas=[f'Email registra la baja con fecha y campaña: {baja_unicas / 1e3:.0f} mil personas en nueve meses, {bm.bajas_email_usuarios.iloc[-1] / 1e3:.1f} mil en septiembre.',
              f'Push y WhatsApp solo tienen una bandera del estado de hoy, sin fecha ni campaña, y no coincide con lo que pasa: {m(wa_baja, 1)} M WhatsApp fueron a personas marcadas como dadas de baja de WhatsApp.',
              'Por eso el push se ve gratis: no cuesta por mensaje, pero cada push que nadie abre puede costar el permiso de notificaciones y no lo vemos.'],
    causa='Braze solo manda a Databricks la baja de email. La baja de push y el bloqueo de WhatsApp quedan en el teléfono o en Meta y nadie los pidió como dato.',
    sowhat='Pedir a Datos la baja de push y de WhatsApp con fecha y campaña (Currents de Braze); mientras tanto, no tratar el push como gratis.',
    fuente=f'Fuente: Braze, envíos por canal (E1), personas con baja de email (E5, únicas) y bajas por mes (E4a), banderas del golden dataset (E17); enero a septiembre 2026. La bandera de baja de WhatsApp no es confiable: revisar fecha y fuente con Datos. Push de B0171 de E1.',
    html=''.join(h)))

# ------------------------------------------------------------------ 90. Cierre
save(90, dict(kind='cierre',
    titulo='Por qué pasa: Braze no tiene dueño ni reglas comunes, y cada equipo lo opera a su manera',
    porques=[f'No sabemos cuánto vende Braze: solo 1 de {n_canvas:,} Canvas tuvo grupo de control de verdad.',
             'No hay control porque no es obligatorio y nadie es dueño de la medición; tampoco hay una sola definición de conversión.',
             f'Nadie es dueño porque activar no exige equipo ni ticket: {tot["nt"]} comunicaciones no tienen ninguno.',
             'Y solo el email registra bajas: en push y WhatsApp no vemos a quién perdemos.',
             'Causa raíz: Braze se repartió por equipos sin un administrador central ni reglas comunes de medición y gobierno.'],
    hipotesis={'A': 'Si cada promoción lleva 10 % de grupo de control y una sola definición de conversión, en 8 semanas sabremos qué campañas venden.',
               'O': 'Si activar exige equipo y ticket, las comunicaciones sin dueño bajan de 748 a 0 y cada una tiene a quién preguntar.',
               'G': 'Si un comité quincenal de 30 minutos revisa calendario y resultados, las decisiones se toman con datos y no con opiniones.'},
    como=['Semana 1: MarTech prende el grupo de control nativo de Braze (10 %, 5 % si pasa de 1 M de personas) en toda campaña promocional. Métrica: campañas con control, hoy 0 %, meta 100 % en 90 días.',
          'Semana 2: Datos fija la definición de conversión (crédito otorgado en 7 días) y la publica en el tablero.',
          'Semana 2: MarTech bloquea la activación sin equipo ni ticket en el nombre. Métrica: comunicaciones sin equipo, hoy 748, meta 0.',
          'Semana 3: CRM arranca el comité quincenal con el calendario de todos los equipos; cada equipo es dueño de sus campañas.',
          'Mes 2: Datos pide a Braze (Currents) la baja de push y WhatsApp con fecha y campaña.'],
    impacto=f'Decidir con datos los {m(datos.load_s3()["R"]["medir"])} M MXN al mes que hoy no se pueden probar, y poner dueño a {m(tot["env"], 1)} M mensajes que hoy no tienen responsable.',
    sowhat='Sin dueño y sin grupo de control, cualquier ahorro o inversión en Braze se discute con opiniones; con ellos, en 90 días cada campaña tiene equipo, ticket y resultado medido.',
    fuente='Fuente: E13 (grupos de control), E2 y E1 (equipo, ticket y envíos), E4a y E17 (bajas y banderas), enero a septiembre 2026; ahorro a medir de la lámina 92.'))
print('ok XI')
