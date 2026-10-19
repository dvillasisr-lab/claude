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
FR = [('Limpiar', 'MarTech con Legal y Riesgo', 0, 2, BLUE, 'Excluir bloqueados, archivar pruebas, quitar duplicados'),
      ('Cortar', 'Cada equipo con su lista', 0, 4, BLUE, 'Apagar correo y WhatsApp sin respuesta, con 10 % sin mensajes'),
      ('Configurar', 'MarTech y Datos', 4, 8, BLUE, 'Canal preferido, límites por semana y día, horas de silencio'),
      ('Medir recuperación', 'CRM con Product Growth y Marketing', 2, 10, GREEN_L, '8 semanas con 10 % sin mensajes en ex clientes'),
      ('Decidir', 'Comité de CRM', 10, 12, GREEN_L, 'Se corta solo lo que no recupera'),
      ('Gobierno', 'CRM, comité quincenal', 2, 12, MARK2, 'Calendario común; equipo y ticket para activar')]
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
    titulo='Plan a 90 días: limpiar y cortar en 30, configurar en 60 y medir en 90, con un equipo dueño de cada frente',
    que='Las campañas promocionales que el plan toca. Cobranza y avisos de servicio quedan fuera, salvo sus pruebas internas.',
    quien='Cada equipo con sus campañas; MarTech (administra Braze) configura; CRM lleva calendario y comité; Datos, el canal preferido y la medición; Legal y Riesgo validan exclusiones.',
    a_quien='Personas bloqueadas, registrados sin crédito, leads, ex clientes y quien no responde por un canal.',
    lecturas=[f'Semanas 1 a 4: MarTech excluye bloqueados y archiva pruebas; cada equipo apaga el correo o WhatsApp de sus campañas sin respuesta. Libera {m(S1)} M MXN al mes.',
              f'Mes 2: MarTech y Datos configuran canal preferido, límite de mensajes por persona a la semana y al día, horas de silencio y nombre con ticket. Suma {m(V["pref"])} M.',
              f'Mes 3: la recuperación de ex clientes corre 8 semanas con 10 % sin mensajes; se corta solo lo que no recupera. Hasta {m(V["medir"])} M más.'],
    causa='Hoy nadie coordina: cada equipo activa, mide y apaga por su cuenta. El plan pone un dueño, una fecha y una métrica a cada frente.',
    sowhat='El ahorro empieza en la semana 1 sin configurar nada; lo que tiene riesgo de perder clientes se decide con datos al final.',
    fuente='Fuente: ' + FUENTE_AH + ' Los equipos de soporte (MarTech, CRM, Datos, Legal y Riesgo) son los que usa el deck; no se nombran personas. S = semana.',
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
    titulo=f'Cada una de las {len(c):,} campañas en un canal tiene una acción: cuatro de ellas concentran {m(cost4, 1)} M MXN del gasto de septiembre',
    que=f'Las {len(c):,} campañas en un canal que mandaron algo en 2026 (una campaña con todas sus versiones, en un canal).',
    quien='Cada equipo dueño recibe su lista con la acción y el porqué.',
    a_quien='Según la campaña. Apagar es solo el canal que no responde: si la misma campaña responde por in-app o push, ese canal se queda.',
    sowhat=f'Apagar, limpiar WhatsApp, rehacer y bajar frecuencia cuestan {m(cost4)} M MXN en septiembre; el ahorro realista es menor ({m(TOT)} M al mes, lámina 92) porque solo cuenta lo que va a quien no responde.',
    fuente='Fuente: clasificación de la pestaña Campañas del Sheets v4, recalculada con E1 (incluye lecturas de WhatsApp registradas el mes siguiente); gasto de septiembre con ' + COSTOS + '. Gasto = costo de la campaña, no ahorro. Ejemplos de E1, enero a septiembre 2026.',
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
for sub, rr in ((1, range(0, 6)), (2, range(6, 12))):
    h = ['<table><tr><th style="width:3%">#</th><th style="width:37%">Regla</th><th style="width:28%">Dato que la respalda</th><th style="width:20%">Dónde vive en Braze</th><th style="width:12%">Equipo</th></tr>']
    for i in rr:
        a, b, c_, d = REG[i]
        h.append(f'<tr><td><b>{i + 1}</b></td><td><b>{a}</b></td><td>{b}</td><td>{c_}</td><td>{d}</td></tr>')
    h.append('</table>')
    save(100, dict(kind='html', ancho_completo=True,
        titulo='Doce reglas comunes para todos los equipos: se cargan en Braze una vez y protegen las 1,913 campañas sin revisarlas una por una' if sub == 1 else 'Doce reglas comunes para todos los equipos (continuación): medir, revisar a las 4 semanas y no mandar a toda la base',
        que='Todo lo promocional. Cobranza y avisos de servicio solo excluyen lista negra.',
        quien='MarTech las carga en Braze; cada equipo las cumple; el comité de CRM revisa excepciones.',
        a_quien='Toda la base. La recuperación de ex clientes no se excluye: va por el canal más barato, con límite de mensajes y grupo sin mensajes.',
        sowhat='Las reglas que viven en Braze (exclusiones, límites, grupo de control) no dependen de que cada equipo se acuerde: se configuran una vez.' if sub == 1 else 'Con grupo de control y revisión a las 4 semanas, ninguna campaña sigue activa solo porque nadie la miró.',
        fuente=f'Fuente: Playbook de Braze para Kueski (12 reglas, secciones 2, 3 y 11); datos de E1, E2, E7b y E13, enero a septiembre 2026; {COSTOS}. Las cifras marcadas "playbook" vienen de ese documento.',
        html=''.join(h)), sub=sub)

# ------------------------------------------------------------------ 101. Matriz 2x2 de ajustes
e17 = pd.read_csv(D + 'e17_contactable.csv')
push_off = e17[(e17.canal == 'push notification') & (e17.notifications_enabled == False)].envios.sum()
wa_no = d1.whatsapp_send.sum() - d1.whatsapp_delivery.sum()
bajas_mil = d1.email_unsubscribe.sum() / d1.email_delivery.sum() * 1000
Q = {('alto', 'bajo'): [('Límite global de mensajes', '5 a la semana, 2 al día, 1 push'), ('Grupo de control nativo', 'hoy 1 de 3,228 Canvas'),
                        ('Horas de silencio', '21:00 a 9:00'), ('Salida del Canvas al convertir', ''), ('Reentrada apagada en ofertas', 'hoy hasta 17 a 31 veces'),
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
    titulo='Dieciocho ajustes de Braze se configuran una vez y protegen todas las campañas: siete son de alto impacto y poco esfuerzo',
    que='Configuración de la cuenta de Braze, no campañas.',
    quien='MarTech, con Datos (atributos y Currents) y Legal (grupos de suscripción y exclusiones).',
    a_quien='Toda la base.',
    lecturas=['Hacer ya: límite global de mensajes por persona, grupo de control nativo, horas de silencio, salida del Canvas al convertir y reentrada apagada. Ninguno de los 18 está activo hoy.',
              f'Junto con ellos se cargan una vez las exclusiones globales ({m(c.bloqueados.sum())} M MXN al mes) y el canal preferido ({m(c.canal_preferido.sum())} M) sin tocar ninguna campaña.',
              'Más esfuerzo: calidad del número de WhatsApp, Currents a Databricks y centro de preferencias. Sin Currents no hay hora, dispositivo ni bajas de push.'],
    causa='Cada equipo configura sus campañas por separado y nadie administra la cuenta: las protecciones que Braze trae de fábrica están apagadas.',
    sowhat='MarTech configura los siete de alto impacto en el mes 1 y los cinco de más esfuerzo en el mes 2; desde ahí protegen toda campaña nueva.',
    fuente=f'Fuente: Playbook de Braze para Kueski, sección 11 (18 ajustes; posición en la matriz: criterio del análisis). Cifras de E1, E2, E13 y E17, enero a septiembre 2026 (sin entregar = WhatsApp enviados no entregados); "17 a 31 veces" del playbook.',
    html=''.join(o)))

# ------------------------------------------------------------------ 102. Qué hace cada equipo en 4 semanas
TT = [('Product Growth', ['Apaga el correo de Tasa 0 (B0211) e Installments (B0223) a registrados', 'Ex clientes KPay (B0333, B0332) al canal barato, 10 % sin mensajes', 'Rehace el cross sell (B0619, B0620) sin WhatsApp a quien no lee', 'Primera lectura de respuesta y bajas con CRM'], EQ['Product Growth']),
      ('Marketing', ['Referidos a dormants (B0326) pasan a in-app', 'Recordatorio de verificación (B0000): máximo un correo al día', 'Rescate Tasa 0 (B0171) solo a quien leyó WhatsApp en 90 días', 'Primera lectura con CRM'], EQ['Marketing']),
      ('Sales', ['Arma su lista de campañas a rehacer', 'Correos a recurrentes solo para quien hizo clic en 90 días', 'Une Comercio del día con Marketing', 'Primera lectura con CRM'], EQ['Sales']),
      ('Others', ['Equipo y ticket a sus 39 comunicaciones de promoción', 'BillPay y Shopping: prueba al 10 % antes de más de 1 M', '', ''], EQ['Others']),
      ('Collections', ['Archiva los Canvas de prueba que llegaron a clientes', 'Cobranza y avisos de servicio no se tocan', '', ''], EQ['Collections']),
      ('MarTech', ['Exclusión global de bloqueados; pausa de pruebas', 'Grupo de control nativo; sin ticket no se activa', 'Límite global de mensajes y horas de silencio', 'Reentrada apagada; salida al convertir'], None),
      ('CRM y Datos', ['Datos: una sola definición de conversión', 'Datos: atributo de último canal con respuesta', 'CRM: primer comité, calendario de noviembre', 'CRM: tablero de respuesta, bajas y control'], None)]
h = ['<table><tr><th style="width:11%">Equipo</th><th style="width:20%">Semana 1</th><th style="width:20%">Semana 2</th><th style="width:20%">Semana 3</th><th style="width:19%">Semana 4</th><th class="num" style="width:10%">Ahorro al mes</th></tr>']
for eq, ws, v in TT:
    vv = f'<b>{m(v)} M MXN</b>' if v is not None else '<span style="color:#6B7484">Habilita</span>'
    h.append(f'<tr><td><b>{eq}</b></td>' + ''.join(f'<td>{w}</td>' for w in ws) + f'<td class="num">{vv}</td></tr>')
h.append('</table>')
save(102, dict(kind='html', ancho_completo=True,
    titulo=f'Qué hace cada equipo en las próximas cuatro semanas: Product Growth y Marketing mueven {m(EQ["Product Growth"] + EQ["Marketing"])} M de los {m(TOT)} M MXN al mes',
    que='Las campañas de cada equipo con acción en el plan.',
    quien='Product Growth, Marketing, Sales, Others y Collections; MarTech, CRM y Datos como soporte.',
    a_quien='Según la campaña: registrados sin crédito, leads, ex clientes de KPay y clientes recurrentes.',
    sowhat='Cada equipo sale de esta reunión con su lista, su semana y su métrica; el comité de la semana 3 revisa avance y bajas.',
    fuente='Fuente: ' + FUENTE_AH + ' Ahorro por equipo incluye su parte a medir (recuperación); MarTech, CRM y Datos no tienen ahorro propio: lo habilitan.',
    html=''.join(h)))

# ------------------------------------------------------------------ 103. Lo que no sabemos
app_push = e7[e7.resp_push == 1].usuarios.sum(); app_any = e7[(e7.resp_push == 1) | (e7.resp_inapp == 1)].usuarios.sum()
UN = [('¿La recuperación de ex clientes recupera?', f'Decide hasta {m(V["medir"])} M MXN al mes', 'Grupo de control de 10 % durante 8 semanas en B0333 y B0332', 'Braze, control nativo', 'CRM con Product Growth'),
      ('¿Quién tiene la app?', f'Sin app no hay push ni in-app. Hoy solo sabemos que {m(app_push, 2)} M abrieron un push en 9 meses y {m(app_any, 1)} M respondieron a push o in-app', 'Bandera de app instalada con fecha', 'Golden dataset', 'Datos'),
      ('¿Cuánto cuesta Braze fijo y cómo se factura?', 'Saber si baja al dejar de escribir a quien no responde', 'Contrato: usuarios activos y puntos de datos', 'Finanzas', 'Finanzas con MarTech'),
      ('¿A qué campañas y segmentos van los 14.2 M que nunca responden?', 'Saber qué apagar primero', 'Extracción de personas sin respuesta con campaña, segmento y etapa', 'Databricks', 'Datos'),
      ('¿Qué es conversión?', 'Dos equipos miran la misma campaña y concluyen lo contrario', 'Una definición: paso del registro o crédito, y en cuántos días', 'Tablero de CRM', 'Datos'),
      ('¿A qué hora, en qué teléfono y quién se dio de baja de push o WhatsApp?', 'Horas de silencio, canal preferido y calidad del número', 'Currents de Braze a Databricks', 'Braze y Databricks', 'Datos y MarTech')]
h = ['<table><tr><th style="width:24%">Lo que no sabemos</th><th style="width:28%">Por qué importa</th><th style="width:24%">Dato que lo resuelve</th><th style="width:12%">Dónde está</th><th style="width:12%">Equipo</th></tr>']
for r in UN:
    h.append('<tr>' + ''.join(f'<td>{"<b>" + x + "</b>" if i == 0 else x}</td>' for i, x in enumerate(r)) + '</tr>')
h.append('</table>')
save(103, dict(kind='html', ancho_completo=True,
    titulo=f'Lo que todavía no sabemos y qué dato lo resuelve: la primera respuesta decide hasta {m(V["medir"])} M MXN al mes',
    que='No aplica: son preguntas abiertas del análisis.',
    quien='Datos, Finanzas, MarTech y CRM.',
    a_quien='Ex clientes, personas que nunca responden y quien tiene o no la app.',
    sowhat='Ninguna de estas preguntas frena lo que se quita ya; todas se resuelven en 90 días con un dueño y un dato concreto.',
    fuente=f'Fuente: E7b (personas por canal al que responden), E13 (grupos de control), E16 y E17, enero a septiembre 2026. Costo fijo de Braze: 7,020 USD al mes y 32,474 créditos sin explicar, queda como X.',
    html=''.join(h)))
print('ok XIII')
