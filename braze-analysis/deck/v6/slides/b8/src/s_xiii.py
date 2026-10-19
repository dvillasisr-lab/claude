# Sección XIII (plan): láminas 98 a 103.
import pandas as pd, numpy as np
from kit import *
import datos
D = datos.ROOT + 'data/'
c = datos.load_c(); S3 = datos.load_s3(); R = S3['R']; DUP = datos.dup_mes()
TOT, SEG, MED = R['total'], R['seguro'], R['medir']
V = dict(desp=c.b_desp.sum() + DUP, cortar=c.b_cortar.sum(), pref=c.b_pref.sum(), medir=c.b_medir.sum())
S1 = V['desp'] + V['cortar']; S2 = S1 + V['pref']
EQ = c.groupby('equipo').tot.sum()
COSTOS = 'WhatsApp a 1.00 MXN por entregado, email a 0.05 por enviado, push e in-app 0'
FUENTE_AH = f'Ahorro de la lámina 92 (E1 de septiembre 2026, acciones del Sheets v4, E9b, E7a, E6b; {COSTOS}).'
print('98', {k: round(v / 1e6, 3) for k, v in V.items()}, round(S1 / 1e6, 2), round(S2 / 1e6, 2), (EQ / 1e6).round(3).to_dict())

# ------------------------------------------------------------------ 98. Gantt
o = svg_open('Plan a 90 días por frente y semana, con el equipo responsable y el ahorro al mes que libera cada hito.')
X0, X1 = 214, 780; wk = (X1 - X0) / 12; sx = lambda w: X0 + wk * w
for i, lab in enumerate(['Mes 1: limpiar y cortar', 'Mes 2: configurar', 'Mes 3: medir']):
    o.append(t(sx(4 * i) + 6, 16, lab, 12.5, INK, 600))
for w in range(13):
    o.append(f'<line x1="{sx(w):.1f}" y1="{24 if w % 4 == 0 else 30}" x2="{sx(w):.1f}" y2="372" stroke="{MARK if w % 4 == 0 else GRID}" stroke-width="1"/>')
for w in range(12):
    o.append(t(sx(w) + wk / 2, 42, f'S{w + 1}', 11, SEC, 400, 'middle'))
o.append(f'<line x1="0" y1="50" x2="780" y2="50" stroke="{INK}" stroke-width="1.2"/>')
FR = [('Limpiar', 'MarTech, Legal y Riesgo', 0, 2, BLUE, 'Bloqueados, pruebas, duplicados'),
      ('Cortar', 'Cada equipo', 0, 4, BLUE, 'Correo y WhatsApp sin respuesta'),
      ('Configurar', 'MarTech y Datos', 4, 8, BLUE, 'Canal preferido, límites, silencio'),
      ('Medir', 'CRM y Product Growth', 2, 10, GREEN_L, 'Ex clientes, 10 % sin mensajes'),
      ('Decidir', 'Comité de CRM', 10, 12, GREEN_L, 'Cortar lo que no recupera'),
      ('Gobierno', 'CRM, cada 15 días', 2, 12, MARK2, 'Calendario común')]
for i, (fr, eq, a, b, col, txt) in enumerate(FR):
    y = 62 + i * 51
    o.append(t(0, y + 14, fr, 13, INK, 600) + t(0, y + 30, eq, 11.5, SEC))
    if col == GREEN_L:
        o.append(f'<rect x="{sx(a) + 2.75:.1f}" y="{y + 2.75}" width="{sx(b) - sx(a) - 5.5:.1f}" height="16.5" rx="2" fill="{col}" stroke="{GREEN}" stroke-width="1.5"/>')
    else:
        o.append(f'<rect x="{sx(a) + 2:.1f}" y="{y + 2}" width="{sx(b) - sx(a) - 4:.1f}" height="18" rx="2" fill="{col}"/>')
    if fr == 'Gobierno':
        for w in range(2, 12, 2):
            o.append(f'<rect x="{sx(w + 1) - 4:.1f}" y="{y + 7}" width="8" height="8" transform="rotate(45 {sx(w + 1):.1f} {y + 11})" fill="{INK}"/>')
    o.append(t(sx(b) - 4, y + 36, txt, 11.5, TXT, 400, 'end') if b == 12 and a >= 8 else t(sx(a) + 4, y + 36, txt, 11.5, TXT))
# hitos de ahorro
o.append(f'<line x1="0" y1="374" x2="780" y2="374" stroke="{INK}" stroke-width="1.2"/>')
o.append(t(0, 396, 'Ahorro al mes que', 11.5, SEC) + t(0, 410, 'queda liberado', 11.5, SEC))
for w, v, lab, col in ((4, S1, '', BLUE), (8, S2, '', BLUE), (12, TOT, 'hasta ', GREEN)):
    o.append(f'<circle cx="{sx(w):.1f}" cy="374" r="5" fill="{col}" stroke="#fff" stroke-width="2"/>')
    o.append(t(sx(w) - 8, 398, f'{lab}{m(v)} M MXN', 13, col, 700, 'end'))
o.append('</svg>')
save(98, dict(kind='html',
    titulo='Plan a 90 días: limpiar y cortar en 30, configurar en 60 y medir en 90, con un dueño por frente',
    que='Las campañas promocionales que el plan toca; cobranza y avisos quedan fuera',
    quien='Cada equipo; MarTech configura, CRM lleva el comité, Datos mide',
    a_quien='Bloqueados, registrados sin crédito, leads, ex clientes',
    lecturas=[f'Mes 1: {m(S1)} M MXN al mes. MarTech limpia bloqueados y pruebas; cada equipo apaga lo que no responde.',
              f'Mes 2: {m(V["pref"])} M más. MarTech y Datos configuran canal preferido, límites y horas de silencio.',
              f'Mes 3: hasta {m(V["medir"])} M más. Se corta solo la recuperación que no trae clientes de vuelta.'],
    causa='Hoy cada equipo activa, mide y apaga por su cuenta; nadie coordina.',
    sowhat='El ahorro empieza en la semana 1; lo que arriesga clientes se decide con datos al final.',
    fuente='Fuente: ahorro de la lámina 92 (E1 de septiembre 2026, Sheets v4, E9b, E7a, E6b). S = semana.',
    html=''.join(o)))

# ------------------------------------------------------------------ 99. Qué hacer con cada campaña
A = c.groupby('accion').agg(n=('fam', 'size'), act=('activo', 'sum'), env=('env_sep', 'sum'), cs=('c_sep', 'sum'))
ACC = [('Apagar', 'Apagar', 'Quitar el canal que no responde ni vende', 'Tasa 0 a registrados, correo (B0211)'),
       ('Limpiar base de WhatsApp', 'Limpiar WhatsApp', 'Quitar números que no reciben o no leen', 'Ex clientes KPay de 3 meses (B0331)'),
       ('Rehacer o re-segmentar', 'Rehacer', 'Otra audiencia o solo a quien respondió', 'Comercio del día por push (B0615)'),
       ('Bajar frecuencia', 'Bajar frecuencia', 'Menos mensajes por persona', 'Recordatorio de verificación (B0000)'),
       ('Confirmar apagado', 'Confirmar apagada', 'Ya no manda; que no vuelva sin revisar', 'Lanzamiento de BillPay por correo'),
       ('Proteger', 'Proteger', 'Responde bien; no saturar', 'Registro de línea por in-app'),
       ('Escalar', 'Ampliar', 'Responde el doble con poco volumen', 'Oferta a quien canceló, push (B0001)'),
       ('No tocar', 'No tocar', 'Cobranza y avisos de servicio', 'Cobranza BKT1, confirmación de pago'),
       ('Seguir igual', 'Seguir igual', 'Sin problema claro', 'Descuento a inactivos de Cash (B0209)')]
print('99', A.assign(env=A.env / 1e6, cs=A.cs / 1e6).round(2).to_dict('index'))
h = ['<table><tr><th style="width:14%">Acción</th><th style="width:27%">Qué significa</th><th class="num" style="width:8%">Campañas</th><th class="num" style="width:9%">Activas en sept.</th>'
     '<th class="num" style="width:9%">Mensajes en sept.</th><th class="num" style="width:10%">Gasto en sept.</th><th style="width:23%;padding-left:1.5cqi">Ejemplo</th></tr>']
for k, lab, q, ej in ACC:
    r = A.loc[k]; strong = k in ('Apagar', 'Limpiar base de WhatsApp', 'Rehacer o re-segmentar', 'Bajar frecuencia')
    env = f'{r.env / 1e6:.1f} M' if r.env > 0 else '0'
    cs = f'{r.cs / 1e6:.2f} M MXN' if r.cs >= 5000 else '0'
    h.append(f'<tr><td><b>{lab}</b></td><td>{q}</td><td class="num">{int(r.n):,}</td><td class="num">{int(r.act)}</td><td class="num">{env}</td><td class="num">{"<b>" + cs + "</b>" if strong else cs}</td><td style="padding-left:1.5cqi">{ej}</td></tr>')
h.append('</table>')
cost4 = A.loc[['Apagar', 'Limpiar base de WhatsApp', 'Rehacer o re-segmentar', 'Bajar frecuencia']].cs.sum()
save(99, dict(kind='html', ancho_completo=True,
    titulo=f'Cada campaña tiene una acción, y cuatro acciones concentran {m(cost4, 1)} M MXN del gasto de septiembre',
    que=f'Las {len(c):,} campañas en un canal que mandaron algo en 2026',
    quien='Cada equipo recibe su lista con la acción',
    a_quien='Apagar quita solo el canal que no responde; los demás se quedan',
    sowhat=f'El ahorro realista es {m(TOT)} M MXN al mes: solo cuenta lo que va a quien no responde.',
    fuente='Fuente: pestaña Campañas del Sheets v4 recalculada con E1, septiembre 2026. Gasto = costo de la campaña, no ahorro.',
    html=''.join(h)))

# ------------------------------------------------------------------ 100. Doce reglas
pg_blq = c.bloqueados.sum()
e7 = pd.read_csv(D + 'e7b_patron_respuesta.csv'); anyr = (e7.resp_email + e7.resp_push + e7.resp_wa + e7.resp_inapp) > 0
wa_ent_n = e7[~anyr].msgs_wa_entregados.sum() / e7[~anyr].msgs_wa.sum()
e2 = pd.read_csv(D + 'e2_catalogo.csv'); sin_t = int((e2.tiene_ticket == 0).sum())
d1 = datos.e1()
bp = d1[d1.communication_name.str.contains('BillPay_Intro_Full_Rollout') & d1.communication_name.str.contains('-E-')]
REG = [('Nombre con equipo, producto, ticket, audiencia y mensaje. Sin ticket no se activa.', f'{sin_t} comunicaciones sin ticket; 748 sin equipo', 'Nombre y etiquetas obligatorios; el que crea no activa', 'MarTech'),
       ('No se manda promoción a lista negra, REUS o ARCO, tarjeta congelada, dados de baja ni a WhatsApp no entregado 3 veces seguidas.', f'{m(pg_blq)} M MXN al mes en promoción a bloqueados', 'Segmento de exclusión global en todo lo promocional', 'MarTech con Legal y Riesgo'),
       ('Máximo 2 mensajes de la misma campaña al mes; el segundo, solo a quien no abrió el primero.', 'Con 2 envíos el clic sube de 0.8 % a 1.8 %; con 3 o 4 cae a 0.5 % (playbook)', 'Límite de reentrada del Canvas', 'Cada equipo'),
       ('Límite por persona: 5 promocionales a la semana, 2 campañas al día y 1 push al día.', '9 % de los días por persona reciben 3 o más campañas: 24 % de los mensajes (playbook)', 'Límite global de frecuencia de la cuenta', 'MarTech'),
       ('Se manda por el canal al que la persona responde.', f'{m(c.canal_preferido.sum())} M MXN al mes en el canal al que no responde', 'Atributo de último canal con respuesta en 90 días', 'Datos y MarTech'),
       ('WhatsApp solo a quien ya respondió algo o a clientes activos, nunca a toda la base. A ex clientes, por el canal más barato que usan.', f'A quien nunca respondió solo le llega {wa_ent_n * 100:.0f} % de los WhatsApp', 'Filtro de audiencia en cada WhatsApp', 'Cada equipo'),
       ('Nada a toda la base: más de 1 M de personas, primero una prueba al 10 % y un segmento.', f'Lanzamiento de BillPay: {m(bp.envios.sum(), 1)} M correos, {bp.email_click.sum() / bp.email_delivery.sum() * 1000:.1f} clics por cada mil y {bp.email_unsubscribe.sum() / 1e3:.0f} mil bajas', 'Aprobación de MarTech para más de 1 M de personas', 'MarTech y CRM'),
       ('El mensaje principal recuerda algo que la persona empezó.', 'Recordatorio de verificación: 30 clics por cada mil correos; Tasa 0 a registrados: 2.8', 'Plantilla de solicitud de campaña', 'Cada equipo'),
       ('Referidos, lanzamientos y novedades van en in-app, no por correo.', 'Referidos por correo a leads: 2.3 clics por cada mil; por in-app, 43 de cada 100 (playbook)', 'Canal del Canvas', 'Marketing'),
       ('A las 4 semanas se revisa: si no responde lo mínimo aceptable, se apaga o se rehace.', f'{int(A.loc["Apagar"].act)} campañas por apagar seguían activas en septiembre ({A.loc["Apagar"].env / 1e6:.1f} M mensajes)', 'Tablero mensual por campaña', 'CRM'),
       ('Toda campaña promocional lleva 10 % de grupo de control (5 % si pasa de 1 M de personas).', 'Hoy, 1 de 3,228 Canvas', 'Grupo de control nativo de Braze', 'MarTech; CRM lee el resultado'),
       ('Un Canvas tiene máximo 8 pasos y la persona entra una sola vez.', 'Una persona recibe la misma campaña hasta 17 a 31 veces (playbook)', 'Entrada única del Canvas', 'MarTech')]
REGC = [('Sin ticket no se activa', f'{sin_t} comunicaciones sin ticket', 'Nombre obligatorio', 'MarTech'),
        ('Nada de promoción a bloqueados ni dados de baja', f'{m(pg_blq)} M MXN al mes a bloqueados', 'Exclusión global', 'MarTech y Legal'),
        ('2 mensajes de la misma campaña al mes', 'Con 3 o más cae el clic (playbook)', 'Reentrada del Canvas', 'Cada equipo'),
        ('5 promocionales a la semana, 1 push al día', '9 % de días con 3 o más campañas (playbook)', 'Límite global', 'MarTech'),
        ('Por el canal al que la persona responde', f'{m(c.canal_preferido.sum())} M MXN al mes en otro canal', 'Atributo de canal', 'Datos y MarTech'),
        ('WhatsApp solo a quien ya respondió', f'A quien nunca responde le llega {wa_ent_n * 100:.0f} %', 'Filtro de audiencia', 'Cada equipo'),
        ('Más de 1 M de personas: prueba al 10 %', f'BillPay: {bp.email_unsubscribe.sum() / 1e3:.0f} mil bajas en un envío', 'Aprobación de MarTech', 'MarTech y CRM'),
        ('Recordar algo que la persona empezó', 'Verificación: 30 clics por mil; Tasa 0: 2.8', 'Solicitud de campaña', 'Cada equipo'),
        ('Referidos y lanzamientos por in-app', 'Referidos por correo: 2.3 clics por mil', 'Canal del Canvas', 'Marketing'),
        ('A las 4 semanas: apagar o rehacer', f'{int(A.loc["Apagar"].act)} campañas por apagar seguían activas', 'Tablero mensual', 'CRM'),
        ('10 % de grupo de control en toda promoción', 'Hoy, 1 de 3,228 Canvas', 'Control nativo', 'MarTech y CRM'),
        ('Máximo 8 pasos; se entra una vez', 'Misma campaña hasta 17 a 31 veces (playbook)', 'Entrada del Canvas', 'MarTech')]
def card(i, a, b, c_, d):
    return (f'<div style="border-top:2px solid {BLUE};padding-top:.7cqi"><div style="font-size:1.7cqi;font-weight:700;color:{BLUE};line-height:1">{i}</div>'
            f'<div style="font-size:1.12cqi;font-weight:600;color:{INK};margin-top:.4cqi;line-height:1.25">{a}</div>'
            f'<div style="font-size:.98cqi;color:{TXT};margin-top:.3cqi">{b}</div>'
            f'<div style="font-size:.85cqi;color:{SEC};margin-top:.25cqi">{c_} · {d}</div></div>')
for sub, rr in ((1, range(0, 6)), (2, range(6, 12))):
    h = '<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2.2cqi 2.6cqi">' + ''.join(card(i + 1, *REGC[i]) for i in rr) + '</div>'
    save(100, dict(kind='html', ancho_completo=True,
        titulo='Doce reglas comunes: las seis primeras se cargan en Braze una vez y protegen todas las campañas' if sub == 1 else 'Doce reglas comunes (continuación): probar, medir y revisar a las 4 semanas',
        que='Todo lo promocional; cobranza y avisos solo excluyen lista negra',
        quien='MarTech las carga en Braze; cada equipo las cumple',
        a_quien='Toda la base; ex clientes por el canal más barato, con grupo sin mensajes',
        sowhat='Las reglas que viven en Braze no dependen de que cada equipo se acuerde.' if sub == 1 else 'Con control y revisión a las 4 semanas, nada sigue activo solo porque nadie lo miró.',
        fuente='Fuente: Playbook de Braze para Kueski (12 reglas); E1, E2, E7b y E13, enero a septiembre 2026. "Playbook": cifra de ese documento.',
        html=h), sub=sub)

# ------------------------------------------------------------------ 101. Matriz 2x2 de ajustes
e17 = pd.read_csv(D + 'e17_contactable.csv')
push_off = e17[(e17.canal == 'push notification') & (e17.notifications_enabled == False)].envios.sum()
wa_no = d1.whatsapp_send.sum() - d1.whatsapp_delivery.sum()
bajas_mil = d1.email_unsubscribe.sum() / d1.email_delivery.sum() * 1000
Q = {('alto', 'bajo'): [('Límite global de mensajes', '5 a la semana, 2 al día, 1 push'), ('Grupo de control nativo', 'hoy 1 de 3,228 Canvas'),
                        ('Horas de silencio', '21:00 a 9:00'), ('Salida del Canvas al convertir', ''), ('Reentrada apagada en ofertas', ''),
                        ('Nombre y etiquetas obligatorios', f'{sin_t} sin ticket'), ('Roles: quien crea no activa', '')],
     ('alto', 'alto'): [('Calidad del número de WhatsApp', f'{m(wa_no, 1)} M sin entregar'), ('Currents a Databricks', 'hora, dispositivo y rebotes'),
                        ('Centro de preferencias de correo', f'{bajas_mil:.1f} bajas por cada mil'), ('Permiso de notificaciones', f'{m(push_off, 1)} M push sin permiso'),
                        ('Catálogos de comercios y cupones', '')],
     ('bajo', 'bajo'): [('Caducidad del push', '24 horas en promoción'), ('Campos con valor por defecto', ''), ('Una in-app por sesión', ''),
                        ('Revisar usuarios activos contra contrato', '')],
     ('bajo', 'alto'): [('Dominio de correo separado', 'promoción y avisos'), ('Hora y canal inteligentes de Braze', 'solo con prueba')]}
o = svg_open('Matriz de impacto contra esfuerzo con los 18 ajustes de la cuenta de Braze.')
QX = {'bajo': (34, 400), 'alto': (410, 780)}; QY = {'alto': (6, 214), 'bajo': (222, 400)}
for (imp, esf), items in Q.items():
    x0, x1 = QX[esf]; y0, y1 = QY[imp]
    hi = imp == 'alto' and esf == 'bajo'
    o.append(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="{"#E8EEFC" if hi else "#F4F6F9"}"/>')
    ttl = {('alto', 'bajo'): 'Hacer ya', ('alto', 'alto'): 'Planear en el mes 2', ('bajo', 'bajo'): 'Hacer de paso', ('bajo', 'alto'): 'Después, con prueba'}[(imp, esf)]
    o.append(t(x0 + 12, y0 + 20, f'{ttl} ({len(items)})', 13, BLUE if hi else INK, 700))
    for i, (a, b) in enumerate(items):
        y = y0 + 42 + i * 23.5
        o.append(f'<circle cx="{x0 + 17}" cy="{y - 4}" r="3.5" fill="{BLUE if hi else MARK}"/>')
        o.append(t(x0 + 28, y, a, 12, INK, 600 if hi else 400) + (t(x1 - 10, y, b, 11, SEC, 400, 'end') if b else ''))
o.append(t(18, 110, 'Más impacto', 11.5, SEC, 600, 'middle', extra=' transform="rotate(-90 18 110)"'))
o.append(t(18, 311, 'Menos impacto', 11.5, SEC, 600, 'middle', extra=' transform="rotate(-90 18 311)"'))
o.append(t(217, 416, 'Menos esfuerzo', 11.5, SEC, 600, 'middle') + t(595, 416, 'Más esfuerzo', 11.5, SEC, 600, 'middle'))
o.append('</svg>')
save(101, dict(kind='html',
    titulo='Dieciocho ajustes de Braze se configuran una vez; siete son de alto impacto y poco esfuerzo',
    que='Configuración de la cuenta de Braze, no campañas',
    quien='MarTech, con Datos y Legal',
    a_quien='Toda la base',
    lecturas=['Ninguno de los 18 está activo hoy; los siete de arriba a la izquierda se hacen en el mes 1.',
              f'Con ellos se cargan las exclusiones ({m(c.bloqueados.sum())} M MXN al mes) y el canal preferido ({m(c.canal_preferido.sum())} M).',
              'Sin Currents a Databricks no hay hora de envío, dispositivo ni bajas de push.'],
    causa='Nadie administra la cuenta: las protecciones que Braze trae de fábrica están apagadas.',
    sowhat='MarTech configura siete ajustes en el mes 1 y cinco en el mes 2.',
    fuente='Fuente: Playbook de Braze para Kueski, sección 11 (posición: criterio del análisis); E1, E2, E13 y E17, enero a septiembre 2026.',
    html=''.join(o)))

# ------------------------------------------------------------------ 102. Qué hace cada equipo en 4 semanas
TT = [('Product Growth', ['Apaga correo de Tasa 0 e Installments', 'Ex clientes KPay: canal barato y control', 'Cross sell sin WhatsApp a quien no lee', 'Primera lectura con CRM'], EQ['Product Growth']),
      ('Marketing', ['Referidos a dormants por in-app', 'Verificación: un correo al día', 'Rescate Tasa 0 solo a quien lee', 'Primera lectura con CRM'], EQ['Marketing']),
      ('Sales', ['Lista de campañas a rehacer', 'Correo solo a quien hizo clic', 'Comercio del día con Marketing', 'Primera lectura con CRM'], EQ['Sales']),
      ('Others', ['Equipo y ticket a 39 promociones', 'BillPay y Shopping: prueba al 10 %', '', ''], EQ['Others']),
      ('Collections', ['Archiva Canvas de prueba', 'Cobranza no se toca', '', ''], EQ['Collections']),
      ('MarTech', ['Excluye bloqueados; pausa pruebas', 'Control nativo; ticket obligatorio', 'Límites y horas de silencio', 'Reentrada apagada'], None),
      ('CRM y Datos', ['Datos: definición de conversión', 'Datos: atributo de canal', 'CRM: primer comité', 'CRM: tablero de control'], None)]
h = ['<table><tr><th style="width:11%">Equipo</th><th style="width:20%">Semana 1</th><th style="width:20%">Semana 2</th><th style="width:20%">Semana 3</th><th style="width:19%">Semana 4</th><th class="num" style="width:10%">Ahorro al mes</th></tr>']
for eq, ws, v in TT:
    vv = f'<b>{m(v)} M MXN</b>' if v is not None else '<span style="color:#6B7484">Habilita</span>'
    h.append(f'<tr><td><b>{eq}</b></td>' + ''.join(f'<td>{w}</td>' for w in ws) + f'<td class="num">{vv}</td></tr>')
h.append('</table>')
save(102, dict(kind='html', ancho_completo=True,
    titulo=f'Qué hace cada equipo en cuatro semanas: Product Growth y Marketing mueven {m(EQ["Product Growth"] + EQ["Marketing"])} M MXN al mes',
    que='Las campañas de cada equipo con acción en el plan',
    quien='Los cinco equipos; MarTech, CRM y Datos como soporte',
    a_quien='Registrados sin crédito, leads, ex clientes y recurrentes',
    sowhat='Cada equipo sale con su lista, su semana y su métrica; el comité revisa en la semana 3.',
    fuente='Fuente: ahorro de la lámina 92 por equipo, incluida su parte a medir. MarTech, CRM y Datos no tienen ahorro propio: lo habilitan.',
    html=''.join(h)))

# ------------------------------------------------------------------ 103. Lo que no sabemos
app_push = e7[e7.resp_push == 1].usuarios.sum(); app_any = e7[(e7.resp_push == 1) | (e7.resp_inapp == 1)].usuarios.sum()
UN = [('¿La recuperación trae clientes?', f'Decide hasta {m(V["medir"])} M MXN al mes', '10 % sin mensajes, 8 semanas', 'CRM y Product Growth'),
      ('¿Quién tiene la app?', f'Solo {m(app_any, 1)} M de personas respondieron a push o in-app', 'Bandera de app con fecha', 'Datos'),
      ('¿Cuánto cuesta Braze fijo?', 'Saber si baja al escribir a menos gente', 'Contrato', 'Finanzas'),
      ('¿Qué reciben los 14.2 M de personas sin respuesta?', 'Saber qué apagar primero', 'Extracción por campaña y segmento', 'Datos'),
      ('¿Qué es conversión?', 'Dos equipos concluyen lo contrario', 'Una definición: paso y días', 'Datos'),
      ('¿Hora, teléfono y bajas de push?', 'Silencio, canal preferido, calidad', 'Currents a Databricks', 'Datos y MarTech')]
h = ['<table><tr><th style="width:30%">Lo que no sabemos</th><th style="width:30%">Por qué importa</th><th style="width:25%">Dato que lo resuelve</th><th style="width:15%">Equipo</th></tr>']
for r in UN:
    h.append('<tr>' + ''.join(f'<td>{"<b>" + x + "</b>" if i == 0 else x}</td>' for i, x in enumerate(r)) + '</tr>')
h.append('</table>')
save(103, dict(kind='html', ancho_completo=True,
    titulo=f'Lo que todavía no sabemos y qué dato lo resuelve: la primera pregunta decide hasta {m(V["medir"])} M MXN al mes',
    que='Preguntas abiertas del análisis',
    quien='Datos, Finanzas, MarTech y CRM',
    a_quien='Ex clientes, personas sin respuesta y quien tiene la app',
    sowhat='Ninguna frena lo que se quita ya; todas se resuelven en 90 días con un dueño.',
    fuente='Fuente: E7b, E13, E16 y E17, enero a septiembre 2026. Costo fijo de Braze: 7,020 USD al mes y 32,474 créditos sin explicar (X).',
    html=''.join(h)))
print('ok XIII')
