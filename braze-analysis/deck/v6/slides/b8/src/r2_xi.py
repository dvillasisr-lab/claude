# Ronda 2, sección XI (láminas 86 a 90): gráficas granulares y menos texto.
import random, pandas as pd, numpy as np
from kit import *
from plot import *
import datos, sin_dueno
D = datos.ROOT + 'data/'
gasto9 = datos.e1().costo.sum()

# ------------------------------------------------------------------ 86. Un punto por Canvas: audiencia contra grupo de control
e13 = pd.read_csv(D + 'e13_lift_control.csv')
pv = e13.pivot_table(index=['canvas_id'], columns='grupo', values='usuarios', aggfunc='sum').fillna(0)
nm = e13.groupby('canvas_id').canvas_name.first()
n_can = len(pv); con = pv[pv.control > 0]; n_ctl = len(con); n_acc = int((con.control < 1000).sum()); acc_max = int(con[con.control < 1000].control.max())
real = e13[(e13.canvas_id == con.control.idxmax())].set_index('grupo')
rc, rt = real.loc['control'], real.loc['test']
k = lambda r, c_: 100 * r[c_] / r.usuarios
sh = rc.usuarios / (rc.usuarios + rt.usuarios)
o = svg_open(f'Un punto por Canvas: personas que recibieron contra personas en grupo de control. {n_can - n_ctl:,} sin control, {n_acc} con 1 a {acc_max} personas, uno con {rc.usuarios:,}.')
X0, X1, Y0, Y1 = 66, 770, 14, 318
sx = logs(1, 3e6, X0, X1); sy = logs(1, 3e5, Y1, Y0)
xaxis(o, sx, [1, 10, 100, 1e3, 1e4, 1e5, 1e6], Y0, 392, title='Personas que recibieron el Canvas (escala logarítmica)', title_y=420, x_mid=(X0 + X1) / 2)
yaxis(o, sy, [1, 10, 100, 1e3, 1e4, 1e5], X0, X1)
o.append(t(X0 - 5, 12, 'En control', 11, SEC, 600, 'end'))
# referencias: control = 10 % y 1 % de la audiencia
for p, lab in ((0.10, '10 % de la audiencia'), (0.01, '1 %')):
    xa, xb = max(1, 1 / p), 3e6
    o.append(f'<line x1="{sx(xa):.1f}" y1="{sy(xa * p):.1f}" x2="{sx(xb):.1f}" y2="{sy(xb * p):.1f}" stroke="{GREEN}" stroke-width="1"/>')
o.append(t(sx(600) + 6, sy(60) + 16, 'control = 10 % de la audiencia', 11, GREEN, 600, 'start', True))
o.append(t(sx(2.6e6), sy(2.6e4) + 16, '1 %', 11, GREEN, 600, 'end', True))
# banda de sin control
BY0, BY1 = 336, 384
o.append(f'<rect x="{X0}" y="{BY0}" width="{X1 - X0}" height="{BY1 - BY0}" fill="#F4F6F9"/>')
o.append(t(X0 - 5, (BY0 + BY1) / 2 + 4, '0', 11, SEC, 400, 'end'))
rnd = random.Random(7)
for cid, r in pv[pv.control == 0].iterrows():
    dot(o, sx(max(r.test, 1)), rnd.uniform(BY0 + 4, BY1 - 4), 1.8, MARK, None, 0.45)
o.append(t(X0 + 8, BY0 + 14, f'{n_can - n_ctl:,} Canvas sin grupo de control', 12, INK, 600, 'start', True))
for cid, r in con.iterrows():
    if r.control == con.control.max(): continue
    dot(o, sx(max(r.test, 1)), sy(r.control), 3.4, INK if False else TXT)
bx, by = sx(rt.usuarios), sy(rc.usuarios)
dot(o, bx, by, 6, BLUE, '#fff', None, 2)
note(o, bx, by, bx - 14, by - 26, 'Cash a plazos a clientes activos (B0301)', 'end', 12, BLUE, 700,
     sub=f'{rc.usuarios / 1e3:.1f} mil en control ({sh * 100:.0f} %): convirtió {k(rc, "usuarios_convirtieron"):.1f} % contra {k(rt, "usuarios_convirtieron"):.1f} %')
m743 = con[con.control == acc_max].iloc[0]; m96 = con[con.control == 96].iloc[0]
note(o, sx(m743.test), sy(acc_max), sx(m743.test) - 16, sy(acc_max) - 14, f'Misma campaña en mayo: {acc_max} personas', 'end', 11.5, TXT, 400)
note(o, sx(m96.test), sy(96), sx(m96.test) - 16, sy(96) - 12, 'Rescate Tasa 0 a leads (B0171): 96', 'end', 11.5, TXT, 400)
o.append(t(sx(30), sy(2.4) - 2, f'{n_acc - 2} Canvas más con 1 a 14 personas: marcas por accidente', 11.5, SEC, 400, 'start', True))
o.append('</svg>')
save(86, dict(kind='grafica',
    titulo=f'Solo uno de {n_can:,} Canvas apartó un grupo de control de verdad: nadie puede decir cuánto vende Braze',
    que='Toda la promoción: Tasa 0, referidos, recordatorios de registro, venta cruzada, reactivación',
    quien='Todos los equipos; el único control real es de Product Growth',
    a_quien='En el único caso medido, clientes activos de Cash (B0301)',
    lecturas=[f'{n_can - n_ctl:,} Canvas no apartaron a nadie; {n_acc} marcaron de 1 a {acc_max} personas por accidente.',
              f'Solo B0301 apartó {rc.usuarios / 1e3:.1f} mil personas: el control convirtió {k(rc, "usuarios_convirtieron"):.1f} % y quien recibió {k(rt, "usuarios_convirtieron"):.1f} %.',
              f'{m(gasto9, 1)} M MXN gastados en nueve meses sin poder decir cuántas ventas causaron.'],
    causa=f'El control no es obligatorio y nadie es dueño de medir; {k(rc, "usuarios_abrieron"):.0f} % del control de B0301 abrió otros mensajes.',
    sowhat='Prender el grupo de control nativo de Braze en toda promoción antes de atribuir ventas.',
    fuente='Fuente: Braze, grupos de prueba y control (E13), 2026. 3,228 = Canvas con personas que entraron en 2026, aunque no hayan enviado mensaje. Gasto de E1.',
    svg=''.join(o)))

# ------------------------------------------------------------------ 87. Un punto por campaña: conversión de quien no abre contra quien abre
a = pd.read_csv(D + 'e9a_abren_vs_no_abren_ventanas.csv'); a['familia'] = a.familia.fillna(''); a['no'] = a.envios_usuario_dia - a.abrieron
a = a[(a.abrieron >= 2000) & (a.no >= 2000) & a.canal.isin(['email', 'push notification'])].copy()
a['ca'] = 100 * a.ab_conv_7 / a.abrieron; a['cn'] = 100 * a.no_conv_7 / a.no
a = a[(a.ca > 0) & (a.cn > 0)]
med = {cn: median(list(g.ca / g.cn)) for cn, g in a.groupby('canal')}
V = 'B0000-CANVAS-Leads_LeftFunnel-Retargeting_Veriff'; T27 = 'T2727-CANVAS-Prospect_FaltaVeriff-RetargetingVeriff-Prod'
print('87', a.groupby('canal').size().to_dict(), {k_: round(v, 2) for k_, v in med.items()})
o = svg_open('Un punto por campaña: conversión a 7 días de quien no abrió contra quien abrió, correo y push, con la cifra que compartió el equipo.')
PW = 318
for j, (cn, lab) in enumerate((('email', 'Correo'), ('push notification', 'Push'))):
    x0 = 56 + j * (PW + 74); x1 = x0 + PW; Y0, Y1 = 36, 372
    sx = logs(0.1, 100, x0, x1); sy = logs(0.1, 100, Y1, Y0)
    o.append(t(x0, 18, f'{lab}: {len(a[a.canal == cn])} campañas', 13, INK, 700))
    tk = [0.1, 1, 10, 100]; fm = lambda v: f'{v:g} %'
    xaxis(o, sx, tk[1:-1], Y0, Y1, fm); yaxis(o, sy, tk, x0, x1, fm)
    o.append(f'<line x1="{sx(0.1):.1f}" y1="{sy(0.1):.1f}" x2="{sx(100):.1f}" y2="{sy(100):.1f}" stroke="{MARK}" stroke-width="1"/>')
    r = med[cn]
    o.append(f'<line x1="{sx(0.1):.1f}" y1="{sy(0.1 * r):.1f}" x2="{sx(100 / r):.1f}" y2="{sy(100):.1f}" stroke="{BLUE}" stroke-width="1.2"/>')
    o.append(t(sx(0.13), sy(0.13 * r) - 8, f'Mediana: {r:.1f} veces', 11, BLUE, 600, 'start', True))
    o.append(t(sx(1.2), sy(1.2) + 16, 'convierten igual', 11, SEC, 400, 'start', True))
    g = a[a.canal == cn]
    for _, rr in g.iterrows():
        if V in rr.familia or T27 in rr.familia: continue
        dot(o, sx(rr.cn), sy(rr.ca), 2.4, MARK, None, 0.6)
    for pat, lb, dx in ((V, 'Veriff de Marketing (B0000)', 1), (T27, 'Veriff de Acquisition (T2727)', 1)):
        h = g[g.familia.str.contains(pat, regex=False)]
        if len(h):
            rr = h.iloc[0]; px, py = sx(rr.cn), sy(rr.ca)
            dot(o, px, py, 5, BLUE, '#fff', None, 1.5)
            if cn != 'email': tx, ty, an, lb = px - 12, py + 34, 'end', 'Veriff (B0000)'
            elif 'T2727' in lb: tx, ty, an = px + 16, py + 34, 'start'
            else: tx, ty, an = px + 16, py - 34, 'start'
            note(o, px, py, tx, ty, lb, an, 11.5, BLUE, 700, sub=f'{rr.ca:.1f} % contra {rr.cn:.1f} %')
    if cn == 'email':
        px, py = sx(17), sy(22)
        o.append(f'<rect x="{px - 5:.1f}" y="{py - 5:.1f}" width="10" height="10" transform="rotate(45 {px:.1f} {py:.1f})" fill="{INK}"/>')
        note(o, px, py, px - 14, py - 18, 'Cifra del equipo', 'end', 11.5, INK, 700, sub='22 % contra 17 %')
o.append(t(400, 404, 'Convierte quien no abrió (eje horizontal) contra quien abrió (vertical), a 7 días, escala logarítmica', 11, SEC, 400, 'middle'))
o.append('</svg>')
ve = a[a.familia.str.contains(V, regex=False) & (a.canal == 'email')].iloc[0]
save(87, dict(kind='grafica',
    titulo='La cifra de Veriff del equipo (22 % contra 17 %) no sale en los datos: cambia la definición, no el resultado',
    que='Recordatorio de terminar la verificación de identidad (Veriff), por correo y push',
    quien='Marketing (B0000) y Acquisition (T2727, que cae en Others)',
    a_quien='Leads que dejaron el registro a medias; prospectos de KPay sin verificar',
    lecturas=[f'En la campaña típica quien abre convierte {med["email"]:.1f} veces más por correo y {med["push notification"]:.1f} por push.',
              f'Veriff por correo: {ve.ca:.1f} % contra {ve.cn:.1f} % a 7 días; la cifra del equipo da 1.3 veces.',
              'El nivel cambia por la definición: aquí es crédito otorgado en 7 días por día de envío.'],
    causa='No hay una definición única de conversión: cada equipo mide otro paso u otra ventana.',
    sowhat='Fijar con Datos una sola definición (qué paso y en cuántos días) antes de comparar campañas.',
    fuente='Fuente: Braze, abren contra no abren por campaña a 7 días (E9a), enero a septiembre 2026; campañas con 2 mil o más personas en cada grupo. 22 contra 17 viene del equipo.',
    svg=''.join(o)))

# ------------------------------------------------------------------ 88. Un punto por comunicación sin dueño
g, tot = sin_dueno.datos()
d = datos.e1(); d['r'] = d.email_click + d.pn_open + d.whatsapp_read + d.in_app_click
rr_ = d.groupby('communication_id').r.sum()
g['rpm'] = 1000 * g.communication_id.map(rr_) / g.env
tm = g.groupby('tema').agg(n=('env', 'size'), env=('env', 'sum'))
gg = g[g.env >= 1000]
COL = {'promocional': BLUE, 'transaccional y operativa': MARK, 'pruebas internas': MARK2}
o = svg_open(f'Un punto por comunicación sin equipo ni ticket: mensajes en 2026 contra respuestas por cada mil mensajes.')
x0 = 0
for key, lab in (('promocional', 'Promoción'), ('transaccional y operativa', 'Avisos de servicio'), ('pruebas internas', 'Pruebas internas')):
    dot(o, x0 + 6, 12, 5, COL[key], None)
    o.append(t(x0 + 15, 16.5, f'{lab}: {tm.loc[key, "n"]}, {m(tm.loc[key, "env"], 1)} M mensajes', 11.5, INK, 600 if key == 'promocional' else 400))
    x0 += {'promocional': 230, 'transaccional y operativa': 265}.get(key, 0)
X0, X1, Y0, Y1 = 60, 770, 40, 352
sx = logs(1e3, 3e7, X0, X1); sy = logs(0.3, 1000, Y1, Y0)
xaxis(o, sx, [1e3, 1e4, 1e5, 1e6, 1e7], Y0, 380, title='Mensajes enviados en 2026, por comunicación (escala logarítmica)', title_y=410, x_mid=(X0 + X1) / 2)
yaxis(o, sy, [1, 10, 100, 1000], X0, X1)
o.append(t(X0 + 4, 34, 'Respuestas por cada mil mensajes', 11, SEC, 600, 'start', True))
o.append(f'<rect x="{X0}" y="358" width="{X1 - X0}" height="18" fill="#F4F6F9"/>' + t(X0 - 5, 371, '0', 11, SEC, 400, 'end'))
for key in ('pruebas internas', 'transaccional y operativa', 'promocional'):
    for _, r in gg[gg.tema == key].iterrows():
        y = sy(r.rpm) if r.rpm >= 0.3 else 367
        dot(o, sx(r.env), y, 4 if key == 'promocional' else 3.2, COL[key])
def pick(p):
    return gg[gg.communication_name.str.contains(p, regex=False)].sort_values('env', ascending=False).iloc[0]
LB = [('BillPay_Intro_Full_Rollout', 'Lanzamiento de BillPay por correo', -10, 34, 'end', BLUE),
      ('WeeklyRecommendations', 'Recomendaciones de Shopping', -30, -46, 'end', BLUE),
      ('Portfolio_BillPay_Reminder_Full_Rollout', 'Recordatorio de BillPay por push', -14, -30, 'end', BLUE),
      ('Payment-Confirmation', 'Confirmación de pago KPay', -16, -20, 'end', TXT),
      ('Payment Received - Push', 'Pago recibido, push', -16, -14, 'end', TXT)]
for p, lab, dx, dy, an, col in LB:
    r = pick(p); px, py = sx(r.env), sy(r.rpm)
    note(o, px, py, px + dx, py + dy, lab, an, 11.5, col, 700 if col == BLUE else 400, sub=f'{m(r.env, 1)} M mensajes, {r.rpm:.0f} por mil')
o.append('</svg>')
bp = d[d.communication_name.str.contains('BillPay_Intro_Full_Rollout') & d.communication_name.str.contains('-E-')]
print('88', tm.to_dict(), len(gg))
save(88, dict(kind='grafica',
    titulo='Uno de cada ocho mensajes sale de comunicaciones sin equipo dueño ni ticket; casi la mitad es promoción',
    que='Avisos de pago y desembolso, lanzamientos de BillPay, recomendaciones de Shopping',
    quien='Nadie: sin equipo (Not Tracked en Braze); por el nombre, NewProducts, Shopping, QA',
    a_quien='Clientes de KPay y Cash en avisos; casi toda la base en BillPay',
    lecturas=[f'{tot["nt"]} comunicaciones no tienen equipo ni ticket; {tot["activas"]} mandaron {m(tot["env"], 1)} M mensajes en 2026.',
              f'Lanzamiento de BillPay: {m(bp.envios.sum(), 1)} M correos, 1 clic por mil y {bp.email_unsubscribe.sum() / 1e3:.0f} mil bajas registradas (jun a sep).',
              f'Los avisos sin dueño ({m(tm.loc["transaccional y operativa", "env"], 1)} M mensajes) son un riesgo: nadie revisa si dejan de llegar.'],
    causa='Activar una comunicación no exige equipo ni ticket, así que nadie responde por ella.',
    sowhat='Equipo y ticket obligatorios para activar: sin ellos nadie apaga, corrige ni mide.',
    fuente='Fuente: catálogo de Braze (E2: equipo y ticket) cruzado con E1, enero a septiembre 2026; comunicaciones con mil mensajes o más. Tema según el nombre.',
    svg=''.join(o)))

# ------------------------------------------------------------------ 89. Tabla de bajas por canal (texto corto)
vol = d.groupby('canal').envios.sum()
e17 = pd.read_csv(D + 'e17_contactable.csv'); wa_baja = e17[(e17.canal == 'whatsapp') & (e17.wa_unsubscribed == True)].envios.sum()
uniq = pd.read_csv(D + 'e5_cohorte_baja.csv').usuarios_baja.sum()
SI, NO, PAR = f'<b style="color:{GREEN}">Sí</b>', f'<b style="color:{INK}">No</b>', f'<span style="color:{SEC}">Solo bandera</span>'
NA = f'<span style="color:{SEC}">No aplica</span>'
tb = [('Correo', vol['email'], SI, SI, SI), ('Push', vol['push notification'], SI, NO, PAR), ('WhatsApp', vol['whatsapp'], SI, NO, PAR), ('In-app', vol['in-app'], f'<span style="color:{SEC}">Impresión</span>', NO, NA)]
h = ['<table><tr><th>Canal</th><th class="num">Mensajes, 9 meses</th><th>Envío y respuesta</th><th>Baja con fecha y campaña</th><th>Suscripción hoy</th></tr>']
for r in tb:
    h.append(f'<tr><td><b>{r[0]}</b></td><td class="num">{m(r[1], 1)} M</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td></tr>')
h.append('</table>')
h.append(f'<div style="margin-top:1.8cqi;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2cqi">'
         f'<div><div class="big" style="font-size:3cqi">{uniq / 1e3:.0f} mil</div><div class="bigl">personas con baja de correo: lo único que se cuenta</div></div>'
         f'<div><div class="big" style="font-size:3cqi;color:{BLUE}">{m(wa_baja, 1)} M</div><div class="bigl">WhatsApp a personas marcadas como baja</div></div>'
         f'<div><div class="big" style="font-size:3cqi;color:{MARK}">Sin dato</div><div class="bigl">quién apagó notificaciones o bloqueó WhatsApp</div></div></div>')
save(89, dict(kind='html',
    titulo='Solo el correo registra quién se da de baja y por qué campaña; en push y WhatsApp no lo sabemos',
    que=f'Todo lo que sale por push y WhatsApp: {m(vol["push notification"], 0)} M push y {m(vol["whatsapp"], 0)} M WhatsApp',
    quien='Todos los equipos',
    a_quien='Toda la base',
    lecturas=[f'{uniq / 1e3:.0f} mil personas se dieron de baja del correo en nueve meses, con fecha y campaña.',
              f'Push y WhatsApp solo tienen una bandera de hoy, sin fecha: {m(wa_baja, 1)} M WhatsApp fueron a marcados como baja.',
              'Por eso el push parece gratis: cuesta el permiso de notificaciones y no lo vemos.'],
    causa='Braze solo manda a Databricks la baja de correo; nadie pidió la de push ni la de WhatsApp.',
    sowhat='Pedir a Datos la baja de push y WhatsApp con fecha y campaña (Currents).',
    fuente='Fuente: Braze, envíos por canal (E1), personas con baja de correo (E5) y banderas del golden dataset (E17), enero a septiembre 2026. La bandera de WhatsApp no es confiable.',
    html=''.join(h)))

# ------------------------------------------------------------------ 90. Cierre (texto corto)
save(90, dict(kind='cierre',
    titulo='Por qué pasa: Braze no tiene dueño ni reglas comunes, y cada equipo lo opera a su manera',
    porques=[f'No sabemos cuánto vende Braze: solo 1 de {n_can:,} Canvas tuvo un grupo de control real.',
             'No hay control porque no es obligatorio ni hay una sola definición de conversión.',
             f'Nadie es dueño: activar no exige equipo ni ticket ({tot["nt"]} comunicaciones sin ellos).',
             'Solo el correo registra bajas: en push y WhatsApp no vemos a quién perdemos.',
             'Causa raíz: Braze se repartió por equipos sin un administrador ni reglas comunes.'],
    hipotesis={'A': 'Con 10 % de control y una definición de conversión, en 8 semanas sabremos qué vende.',
               'O': 'Si activar exige equipo y ticket, las comunicaciones sin dueño bajan de 748 a 0.',
               'G': 'Un comité quincenal de 30 minutos decide con datos y no con opiniones.'},
    como=['Semana 2: MarTech prende el control nativo (10 %) en toda promoción. Meta: 100 % en 90 días.',
          'Semana 2: Datos fija la definición de conversión: crédito otorgado en 7 días.',
          'Semana 2: MarTech bloquea activar sin equipo ni ticket. Meta: 0 comunicaciones sin dueño.',
          'Semana 3: CRM arranca el comité quincenal con el calendario de todos los equipos.'],
    impacto=f'Decidir con datos {m(datos.load_s3()["R"]["medir"])} M MXN al mes y poner dueño a {m(tot["env"], 1)} M mensajes.',
    sowhat='Con dueño y grupo de control, en 90 días cada campaña tiene equipo, ticket y resultado medido.',
    fuente='Fuente: E13 (control), E2 y E1 (equipo, ticket y envíos), E5 y E17 (bajas), enero a septiembre 2026.'))
print('ok r2 XI')
