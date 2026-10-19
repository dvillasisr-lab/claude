"""Láminas 1 a 4: portada, resumen ejecutivo, cuatro decisiones y divisor del Acto 1.
Cifras de E1 (base_p1), E3, E7b, E13 y muestra_c_familias; ahorros del caso de negocio aprobado (muestras/s3, s3_datos.json)."""
import json, pathlib
import pandas as pd
from comun import load, write, ROOT, BLUE, GREEN, INK, SEC

d = load()
d['respu'] = d.email_click + d.pn_open + d.whatsapp_read + d.in_app_click
env = d.envios.sum(); costo = d.costo.sum(); mes = costo / 9
g = d.groupby('m').agg(env=('envios', 'sum'), r=('respu', 'sum'))
rpm = (1000 * g.r / g.env).round(0)
promo = d[d.tipo == 'promocional'].envios.sum() / env
eq = d.groupby('equipo').envios.sum() / env
mkpg = eq['Marketing'] + eq['Product Growth']
wa = d[d.canal == 'whatsapp']
wa_mkpg = wa[wa.equipo.isin(['Marketing', 'Product Growth'])].costo.sum() / wa.costo.sum()
wa_env = wa.envios.sum() / env; wa_cost = wa.costo.sum() / costo
fams = d.fam.nunique()
# E3: personas y la banda de 321 o más
e3 = pd.read_csv(ROOT / 'data/e3_usuarios_distribucion.csv')
pers = e3.usuarios.sum()
b = e3[e3.banda_msgs == '321+']; b_u = b.usuarios.sum(); b_mpp = b.msgs.sum() / b_u
# E7b: mensajes a un canal al que la persona nunca respondió
e7 = pd.read_csv(ROOT / 'data/e7b_patron_respuesta.csv')
mudo = (e7.msgs_email * (e7.resp_email == 0) + e7.msgs_push * (e7.resp_push == 0) + e7.msgs_wa * (e7.resp_wa == 0) + e7.msgs_inapp * (e7.resp_inapp == 0)).sum()
mudo_pct = mudo / (e7.msgs_email + e7.msgs_push + e7.msgs_wa + e7.msgs_inapp).sum()
# Bloqueados: promocional a etapas 3, 4 y 6 (muestra_c_familias, columna envios_etapa_bloqueada)
c = pd.read_csv(ROOT / 'hallazgos/muestra_c_familias.csv')
bloq = c[c.tipo == 'promocional o lifecycle'].envios_etapa_bloqueada.sum()
# E13: Canvas con grupo de control
e13 = pd.read_csv(ROOT / 'data/e13_lift_control.csv')
canv = e13.canvas_id.nunique(); ctl = e13[e13.grupo == 'control']; ctl_n = ctl.canvas_id.nunique(); ctl_big = int((ctl.usuarios > 1000).sum())
# Ahorros (caso de negocio aprobado). s3_datos.json lo escribe muestras/s3_datos.py.
SD = pathlib.Path('/tmp/claude-0/-home-user-claude/e114ba4f-39d4-57f8-9f24-b0f0c0cbef51/scratchpad/muestras/s3_datos.json')
S = json.loads(SD.read_text(encoding='utf-8'))
T = {r['k']: r['mxn'] / 1e6 for r in S['T']}; R = S['R']
d1 = T['bloqueados'] + T['duplicados'] + T['pruebas']
d2 = T['ap_act'] + T['rehacer_em'] + T['limpiar_wa'] + T['canal_preferido']
d3 = T['ap_rec'] + T['sin_respuesta_90d']
tot, seg, med = R['total'] / 1e6, R['seguro'] / 1e6, R['medir'] / 1e6
print(dict(env=env / 1e6, mes=mes / 1e6, rpm1=rpm[1], rpm9=rpm[9], promo=promo, mkpg=mkpg, wa_mkpg=wa_mkpg, wa_env=wa_env, wa_cost=wa_cost,
           fams=fams, pers=pers, b_u=b_u, b_mpp=b_mpp, mudo=mudo / 1e6, mudo_pct=mudo_pct, bloq=bloq / 1e6, canv=canv, ctl_n=ctl_n, ctl_big=ctl_big,
           d1=d1, d2=d2, d3=d3, tot=tot, seg=seg, med=med, pct_avg=R['pct_avg'], pct_sep=R['pct_sep'], anual=R['anual'] / 1e6))
M = lambda v, dec=1: f'{v:.{dec}f}'

# ---------------- 1. Portada
write(1, dict(kind='portada', titulo='Menos mensajes, mejor dirigidos: Braze en Kueski',
              subtitulo='Auditoría de enero a septiembre 2026: qué está pasando con los mensajes que mandamos, por qué pasa y qué proponemos.',
              meta=f'{env / 1e6:.0f} M mensajes, {pers / 1e6:.1f} M personas y unas {round(fams, -2):,.0f} campañas revisadas · Octubre 2026'))

# ---------------- 2. Resumen ejecutivo
td = lambda s: f'<td>{s}</td>'
row = lambda a, b_, c_: f'<tr>{td(a)}{td(b_)}{td(c_)}</tr>'
html2 = (
    '<table style="table-layout:fixed">'
    '<tr><th style="width:36%">Qué pasa</th><th style="width:32%">Por qué pasa</th><th style="width:32%">Qué hacemos</th></tr>'
    + row(f'<b>Mandamos más y nos responden menos.</b> {env / 1e6:.0f} M mensajes en nueve meses; cada mil mensajes traían {rpm[1]:.0f} respuestas en enero y {rpm[9]:.0f} en septiembre.',
          f'No hay límite de mensajes por persona a la semana: {b_u / 1e3:.0f} mil personas recibieron {b_mpp:.0f} mensajes cada una, casi dos al día.',
          'Límite de 5 promociones por persona a la semana. Avisos de servicio y cobranza quedan fuera del límite.')
    + row(f'<b>Pagamos el canal que cuesta, no el que responde.</b> {mes / 1e6:.1f} M MXN al mes en mensajes; WhatsApp es {wa_env * 100:.0f} % de los mensajes y {wa_cost * 100:.0f} % del gasto.',
          f'Cada equipo elige el canal por costumbre: {mudo_pct * 100:.0f} % de los mensajes van a un canal al que esa persona nunca respondió.',
          'Cada persona por el canal al que responde. WhatsApp solo a quien lo lee o con presupuesto mensual con límite.')
    + row(f'<b>Escribimos a quien no debe recibir promociones.</b> {bloq / 1e6:.0f} M envíos promocionales a personas con tarjeta KPay congelada, en lista negra o que pidieron no recibir publicidad.',
          'No hay una exclusión común en Braze: cada campaña arma su propia audiencia.',
          'Una exclusión común en toda campaña promocional, y separar al ex cliente del lead que nunca activó.')
    + row(f'<b>No sabemos qué vende.</b> De {canv:,} Canvas, solo {ctl_big} tiene un grupo de más de mil personas que no recibe mensajes para comparar.',
          'Cada equipo mide su campaña sola, con conversión atribuida, que no prueba venta, y sin calendario común.',
          'Grupo sin mensajes de 5 a 10 % en toda campaña, un dueño por segmento y un calendario común.')
    + '</table>'
    f'<div style="display:flex;gap:2cqi;align-items:center;margin-top:1.1cqi;padding:.8cqi 1.1cqi;background:#E4F2EC">'
    f'<div class="big" style="color:{GREEN};flex:0 0 auto">{tot:.2f} M MXN</div>'
    f'<div class="bigl" style="margin:0;color:{INK}"><b>al mes es lo que podemos dejar de gastar ({R["anual"] / 1e6:.0f} M MXN al año, {R["pct_avg"] * 100:.0f} % del gasto mensual promedio).</b> '
    f'{seg:.2f} M se quita ya sin perder ventas; {med:.2f} M se quita solo si no recupera clientes (primero se prueba dejando a un grupo sin mensajes).</div></div>')
write(2, dict(kind='html', ancho_completo=True,
              titulo=f'Mandamos más y nos responden menos; cuatro decisiones bajan el gasto hasta {tot:.2f} M MXN al mes sin dejar de buscar a quien queremos recuperar',
              que=f'{promo * 100:.0f} % de los mensajes son promociones: Tasa 0, referidos, descuentos, rescates y lanzamientos como BillPay. El resto son avisos de servicio y cobranza.',
              quien=f'Marketing y Product Growth mandan {mkpg * 100:.0f} % de los mensajes y ponen {wa_mkpg * 100:.0f} % del gasto de WhatsApp. Sales, Collections y Others mandan el resto.',
              a_quien=f'{pers / 1e6:.1f} M personas: leads y registrados sin crédito, ex clientes que queremos recuperar (dormants, inactivos, churn) y clientes activos.',
              html=html2,
              sowhat='El problema es la forma de operar, no una campaña: se corrige con reglas comunes y no apagando todo. A los ex clientes se les sigue buscando, por el canal más barato y midiendo si regresan.',
              fuente=(f'Fuente: Braze, enero a septiembre 2026: envíos por comunicación, mes y canal (E1); mensajes por persona (E3); respuesta por canal y persona (E7b); grupos de control por Canvas (E13); '
                      f'etapas bloqueadas por campaña (Sheets v4). Respuesta = clic de email, apertura de push, lectura de WhatsApp y clic in-app. Ahorro sobre el gasto de septiembre ({R["sep"] / 1e6:.2f} M MXN), del caso de negocio. {"WhatsApp a 1.00 MXN por entregado, email a 0.05 MXN por enviado."}')))

# ---------------- 3. Cuatro decisiones
cell = lambda v, sub, col: f'<td class="num"><div style="font-size:1.9cqi;font-weight:700;color:{col};line-height:1.05">{v}</div><div style="font-size:.82cqi;line-height:1.2;color:{SEC}">{sub}</div></td>'
html3 = (
    '<table style="table-layout:fixed">'
    '<tr><th style="width:17%">Decisión</th><th style="width:31%">Qué cambia en Braze</th><th style="width:15%">Quién lo hace</th><th style="width:21%">A quién toca</th><th class="num" style="width:16%">Gasto que mueve</th></tr>'
    f'<tr><td><b>1. A quién le escribimos</b></td><td>Una exclusión común en toda promoción: tarjeta KPay congelada, lista negra, quien pidió no recibir publicidad y dados de baja. Sin duplicados del mismo día ni pruebas a clientes.</td>'
    f'<td>MarTech la configura; aplica a todos los equipos.</td><td>{bloq / 1e6:.0f} M envíos promocionales en nueve meses a personas bloqueadas (Marketing 38 %, Sales 30 %, Product Growth 26 %).</td>'
    + cell(f'{d1:.2f} M', 'MXN al mes; se quita ya sin perder ventas', BLUE) + '</tr>'
    f'<tr><td><b>2. Por qué canal y cuántas veces</b></td><td>Cada persona por el canal al que respondió en 90 días; WhatsApp solo a quien lo lee o con presupuesto con límite; máximo 5 promociones por persona a la semana.</td>'
    f'<td>Marketing y Product Growth; MarTech pone el límite.</td><td>Leads y registrados sin crédito, y quien responde por otro canal ({mudo_pct * 100:.0f} % de los mensajes va a un canal que esa persona nunca usó).</td>'
    + cell(f'{d2:.2f} M', 'MXN al mes; se quita ya sin perder ventas', BLUE) + '</tr>'
    f'<tr><td><b>3. Cómo medimos</b></td><td>Un grupo de 5 a 10 % que no recibe mensajes en toda campaña promocional, empezando por la recuperación de ex clientes y por WhatsApp.</td>'
    f'<td>CRM define el grupo; cada equipo lo respeta.</td><td>Ex clientes (dormants, inactivos, churn) y quien no responde en 90 días: se les sigue escribiendo por el canal más barato.</td>'
    + cell(f'{d3:.2f} M', 'MXN al mes; se quita solo si no recupera clientes', GREEN) + '</tr>'
    f'<tr><td><b>4. Quién decide</b></td><td>Un dueño por segmento, un calendario común entre equipos y un catálogo de campañas activas.</td>'
    f'<td>CRM, con los cinco equipos.</td><td>Todos: evita otro junio, cuando tres equipos sumaron envíos a casi toda la base el mismo mes.</td>'
    + f'<td class="num"><div style="font-size:1.05cqi;font-weight:600;color:{SEC}">Sin monto propio</div><div style="font-size:.82cqi;color:{SEC}">sostiene las otras tres</div></td>' + '</tr>'
    f'<tr><td colspan="4" style="border-bottom:0;font-weight:600">Total del plan. Los montos no se traslapan: se calcularon en cadena sobre el gasto de septiembre.</td>'
    + cell(f'{tot:.2f} M', f'MXN al mes; {R["anual"] / 1e6:.0f} M MXN al año', INK).replace('<td class="num">', '<td class="num" style="border-bottom:0">') + '</tr>'
    '</table>')
write(3, dict(kind='html', ancho_completo=True,
              titulo='Cuatro decisiones ordenan a quién, por dónde y cuántas veces escribimos, y nos dejan medir qué vende',
              que='Sobre todo promociones. Avisos de servicio y cobranza quedan fuera del límite de mensajes por persona.',
              quien='Todos los equipos; Marketing y Product Growth concentran el cambio. MarTech configura Braze y CRM lleva el calendario y la medición.',
              a_quien='Bloqueados y dados de baja: fuera. Ex clientes y leads que nunca activaron: plan de recuperación con presupuesto con límite. Clientes activos: por su canal.',
              html=html3,
              sowhat='Ninguna decisión corta el contacto con quien queremos recuperar: cambian el canal, la frecuencia y la forma de medir.',
              fuente=(f'Fuente: caso de negocio sobre el gasto de septiembre 2026 ({R["sep"] / 1e6:.2f} M MXN, con lecturas de WhatsApp registradas el mes siguiente); bloqueados del Sheets v4 (etapas 3, 4 y 6); '
                      f'canal sin respuesta de E7b. Decisión 1 = bloqueados, duplicados y pruebas; 2 = canal que cuesta a leads, rehacer email, limpiar WhatsApp y canal preferido; 3 = ex clientes y sin respuesta en 90 días. WhatsApp a 1.00 MXN por entregado, email a 0.05 por enviado.')))

# ---------------- 4. Divisor del Acto 1
write(4, dict(kind='divisor', acto='Acto 1 · Qué pasa hoy', titulo='Mandamos mucho y nos responden cada vez menos',
              subtitulo='Primero el tamaño: cuánto mandamos, qué mandamos, cuánto cuesta y qué obtenemos. Después, por qué cada mensaje responde menos que en enero y cuánto margen tenemos para mejorar.'))
