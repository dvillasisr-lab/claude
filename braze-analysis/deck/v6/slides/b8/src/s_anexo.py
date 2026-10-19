# Anexo: láminas 104 a 110.
import os, pandas as pd, numpy as np
from kit import *
import datos
ROOT = datos.ROOT; D = ROOT + 'data/'
c = datos.load_c(); S3 = datos.load_s3(); R = S3['R']; DUP = datos.dup_mes()
d1 = datos.e1()
COSTOS = 'WhatsApp a 1.00 MXN por entregado, email a 0.05 por enviado, push e in-app 0'
NUM = lambda s: f'<td class="num">{s}</td>'

# ------------------------------------------------------------------ 104. Método y fuentes
filas = lambda f: sum(1 for _ in open(D + f)) - 1
EX = [('E1', ['e1_comunicacion_mes_canal.csv'], 'Envíos, entregas, respuesta, bajas, conversión y costo', 'comunicación, mes y canal'),
      ('E2', ['e2_catalogo.csv'], 'Catálogo: equipo, ticket, canal, estado y fechas', 'comunicación'),
      ('E3', ['e3_usuarios_distribucion.csv'], 'Personas por cuántos mensajes reciben y suscripción', 'grupo de personas'),
      ('E4a, E4b', ['e4a_serie_semana_mes_canal.csv', 'e4b_concentracion_mes.csv'], 'Serie semanal y mensual por canal; mensajes por persona', 'semana o mes y canal'),
      ('E5, E5b', ['e5_cohorte_baja.csv', 'e5b_comms_despues_baja.csv'], 'Personas que se dan de baja y qué reciben después', 'mes de baja; comunicación'),
      ('E6a, E6b', ['e6a_solape_dia_mes.csv', 'e6b_pares_familias.csv'], 'Varias campañas el mismo día; pares de campañas', 'persona y día; par'),
      ('E7a, E7b, E7c', ['e7a_familia_canal_etapa.csv', 'e7b_patron_respuesta.csv', 'e7c_abren_vs_no_abren.csv'], 'Etapa del cliente; canal al que responde; abren contra no abren', 'campaña y etapa; patrón'),
      ('E8', ['e8_dias_hasta_baja.csv'], 'Días y correos hasta la baja', 'grupo de personas'),
      ('E9a, E9b', ['e9a_abren_vs_no_abren_ventanas.csv', 'e9b_patron_respuesta_90d.csv'], 'Conversión a 7, 30 y 90 días; respuesta en 90 días', 'campaña; patrón'),
      ('E10, E11, E12', ['e10_dia_semana.csv', 'e11_segmentacion.csv', 'e12_antiguedad.csv'], 'Día de la semana; segmentos de Braze; antigüedad', 'día, segmento, antigüedad'),
      ('E13, E14, E15', ['e13_lift_control.csv', 'e14_experimentos.csv', 'e15_embudo_pasos.csv'], 'Grupos de control; variantes; pasos de cada Canvas', 'Canvas'),
      ('E16, E17, E18b', ['e16_sin_respuesta.csv', 'e17_contactable.csv', 'e18b_llave_dispositivo.csv'], 'Sin respuesta; canal contactable y banderas; dispositivo', 'mes, canal y bandera')]
ver = pd.read_excel(ROOT + 'sheets/braze_auditoria_v4.xlsx', 'Verificación')
n_ver = len(ver)
n_files = sum(len(f) for _, f, _, _ in EX)
n_com = int((d1.groupby('communication_id').envios.sum() > 0).sum())
print('104', n_com, n_files, n_ver, d1.envios.sum(), d1.communication_id.nunique())
h = ['<table><tr><th style="width:12%">Extracción</th><th style="width:44%">Qué trae</th><th style="width:26%">Una fila por</th><th class="num" style="width:18%">Filas</th></tr>']
for e, fs, q, g in EX:
    h.append(f'<tr><td><b>{e}</b></td><td>{q}</td><td>{g}</td>' + NUM(' + '.join(f'{filas(f):,}' for f in fs)) + '</tr>')
h.append('</table>')
save(104, dict(kind='html',
    titulo=f'Método y fuentes: 18 extracciones agregadas de Databricks y {n_ver} verificaciones de los totales',
    lecturas=[f'{m(d1.envios.sum(), 1)} M mensajes de {n_com:,} comunicaciones que mandaron algo, enero a septiembre de 2026.',
              f'Las 18 extracciones están en {n_files} archivos y se pegaron en el Sheets v4 con fórmulas vivas.',
              f'{n_ver} comprobaciones cruzan cada total del Sheets con el mismo cálculo hecho aparte.'],
    causa='Equipo, audiencia y mensaje se leen del nombre de la campaña: Braze no los guarda como campos.',
    sowhat='Cualquiera puede rehacer cada cifra con estos archivos, sin acceso a Braze.',
    fuente=f'Fuente: carpeta data (E1 a E18b) y Sheets braze_auditoria_v4, pestaña Verificación ({n_ver} comprobaciones). Sin datos personales. App: no hay dato; se aproxima con quien abrió un push o un in-app.',
    html=''.join(h)))

# ------------------------------------------------------------------ 105. Definiciones
DEF = [('Responder', 'Clic en correo, abrir push, leer WhatsApp o clic en in-app'),
       ('Lo mínimo aceptable', '3 clics por mil correos, 7.5 aperturas por mil push, 6 de 10 WhatsApp leídos, 1 de 10 in-app'),
       ('Canal sin respuesta', 'Canal al que la persona nunca respondió, aunque responda por otro'),
       ('Nunca respondió', 'Ningún canal en nueve meses: 14.2 M de personas'),
       ('Campaña con todas sus versiones', 'La comunicación con sus versiones de cada mes; en un canal hay 1,913'),
       ('Bloqueados', 'Tarjeta KPay congelada, REUS o ARCO y lista negra'),
       ('Ex clientes', 'Churn, dormants e inactivos: se buscan recuperar, no se apagan'),
       ('Leads y registrados', 'Personas que nunca tomaron crédito'),
       ('Conversión', 'Métrica principal: crédito otorgado en 7 días, repartido entre los mensajes del día; referencia, no prueba de venta'),
       ('Solicitud', 'También se muestra el costo por solicitud registrada; no viene repartida y puede contar en varias campañas'),
       ('Grupo de control', '5 a 10 % de la audiencia al azar que no recibe el mensaje')]
h = ['<table><tr><th style="width:24%">Término</th><th>Qué significa en este deck</th></tr>']
for a, b in DEF:
    h.append(f'<tr><td><b>{a}</b></td><td>{b}</td></tr>')
h.append('</table>')
save(105, dict(kind='html', ancho_completo=True,
    titulo='Definiciones: responder, canal sin respuesta, campaña con todas sus versiones, bloqueados y conversión',
    sowhat='Con estas definiciones, dos equipos que miran la misma campaña llegan a la misma cifra.',
    fuente='Fuente: definiciones del análisis (Sheets v4, Léeme y Parámetros); audiencia según el nombre de la campaña. Solicitud: solicitudes registradas en E1.',
    html=''.join(h)))

# ------------------------------------------------------------------ 106. Los 24 estándares
est = pd.read_excel(ROOT + 'sheets/braze_auditoria_v4.xlsx', 'Estándares', header=4)
STD = [(1, 'Entrega', 'Correos que llegan a la bandeja', '95 % o más', 'Referencia de la industria'),
       (2, 'Correo', 'Correos abiertos', '15 % o más', 'Industria, 15 a 25 %; inflada por aperturas automáticas'),
       (3, 'Correo', 'Clic en correos entregados', '1.5 % o más', 'Industria, 1.5 a 3 %; el mínimo interno es 0.3 %'),
       (4, 'Correo', 'Bajas por cada mil correos entregados', '2.5 o menos', 'Parámetro interno; la industria, menos de 3'),
       (5, 'Push', 'Push abiertos', '3 % o más', 'Industria, 3 a 10 %; el mínimo interno es 0.75 %'),
       (6, 'WhatsApp', 'WhatsApp entregados', '90 % o más', 'Referencia de la industria'),
       (7, 'WhatsApp', 'WhatsApp entregados que se leen', '70 % o más', 'Industria, 70 a 90 %; el mínimo interno es 60 %'),
       (8, 'In-app', 'Clic en in-app mostrados', '5 % o más', 'Parámetro interno; la industria, 5 a 20 %'),
       (9, 'Frecuencia', 'Mensajes de la misma campaña por persona al mes', '2 o menos', 'Interno: con 3 o más cae la respuesta y suben las bajas'),
       (10, 'Frecuencia', 'Mensajes por persona al mes, todos los canales', '20 o menos', 'Interno: unos 5 promocionales a la semana'),
       (11, 'Frecuencia', 'Personas con 41 o más mensajes al mes', '5 % o menos', 'Propuesta interna'),
       (12, 'Mismo día', 'Días en que una persona recibe 3 o más campañas', '10 % o menos', 'Interno: máximo 2 campañas por persona al día'),
       (13, 'Bajas', 'Días hasta la baja de una persona nueva (mediana)', '90 o más', 'Propuesta interna'),
       (14, 'Bajas', 'Correos antes de la baja, persona nueva (mediana)', '10 o más', 'Interno: si se va antes, es el contenido o la audiencia'),
       (15, 'Bajas', 'Personas nuevas que se van el día del primer correo', '5 % o menos', 'Propuesta interna'),
       (16, 'Canal', 'Mensajes por un canal al que la persona nunca respondió', '20 % o menos', 'Propuesta interna'),
       (17, 'Canal', 'Personas que nunca respondieron a nada', '50 % o menos', 'Propuesta interna'),
       (18, 'Audiencia', 'Promoción a bloqueados', '0', 'Regla de negocio'),
       (19, 'Audiencia', 'Correos promocionales a dados de baja', '0', 'Regla de negocio y de Braze'),
       (20, 'Audiencia', 'Dados de baja que vuelven a recibir correo', '10 % o menos', 'Interno: solo cobranza y avisos de servicio'),
       (21, 'Toda la base', 'Campañas de correo activas a 1 M o más de personas por envío', '0', 'Interno: antes, prueba al 10 % con control'),
       (22, 'Toda la base', 'Campañas activas que no responden lo mínimo aceptable', '0', 'Regla interna del Sheets'),
       (23, 'Medición', 'Campañas promocionales con grupo de control', '10 % de la audiencia', 'Práctica estándar de Braze'),
       (24, 'Nombres', 'Comunicaciones con ticket', '100 %', 'Regla interna de nombres')]
assert len(est) == 24 and list(est['#'].astype(int)) == [s[0] for s in STD]
FE = dict(zip(est['#'].astype(int), est['fuente (E)'].fillna('').astype(str)))
for sub, rr in ((1, STD[:12]), (2, STD[12:])):
    h = ['<table><tr><th style="width:3%">#</th><th style="width:10%">Tema</th><th style="width:36%">Indicador</th><th style="width:12%">Estándar</th><th style="width:29%">De dónde sale</th><th style="width:10%">Dato</th></tr>']
    for n, tm, ind, st, src in rr:
        fe = FE[n] if FE[n] and FE[n] != 'nan' else 'sin dato'
        fe = 'E13: hoy 1 de 3,228' if n == 23 else (fe[:4] if len(fe) < 6 else 'sin dato')
        h.append(f'<tr><td>{n}</td><td>{tm}</td><td><b>{ind}</b></td><td><b>{st}</b></td><td>{src}</td><td>{fe}</td></tr>')
    h.append('</table>')
    save(106, dict(kind='html', ancho_completo=True,
        titulo='Los 24 estándares y su fuente: ocho son de canal y seis vienen de la industria' if sub == 1 else 'Los 24 estándares y su fuente (continuación): bajas, audiencia, medición y nombres',
        sowhat='Son el mínimo de la industria o una regla interna, no una meta de Kueski.' if sub == 1 else 'Grupo de control (23): hoy 1 de 3,228; se mide en Braze en cuanto se prenda.',
        fuente='Fuente: Sheets braze_auditoria_v4, pestaña Estándares; la columna Dato dice de qué extracción sale cada cifra.',
        html=''.join(h)), sub=sub)

# ------------------------------------------------------------------ 107. Detalle mensual, semanal y por día
d1['respu'] = d1.email_click + d1.pn_open + d1.whatsapp_read + d1.in_app_click
mon = d1.groupby('mes').agg(env=('envios', 'sum'), r=('respu', 'sum'), cost=('costo', 'sum'))
ch = d1.groupby(['mes', 'canal']).envios.sum().unstack().fillna(0)
e4 = pd.read_csv(D + 'e4a_serie_semana_mes_canal.csv')
bm = e4[(e4.grano == 'mes') & (e4.canal == 'email')].set_index(e4[(e4.grano == 'mes') & (e4.canal == 'email')].periodo.str[:7]).bajas_email_usuarios
MN = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre']
h = ['<table><tr><th>Mes de 2026</th><th class="num">Mensajes</th><th class="num">Correo</th><th class="num">Push</th><th class="num">WhatsApp</th><th class="num">In-app</th>'
     '<th class="num">Respuestas por cada mil mensajes</th><th class="num">Gasto</th><th class="num">Personas con baja de correo</th></tr>']
for i, mm in enumerate(mon.index):
    r = mon.loc[mm]
    h.append(f'<tr><td><b>{MN[i]}</b></td>' + NUM(f'{r.env / 1e6:.1f} M') + ''.join(NUM(f'{ch.loc[mm].get(k, 0) / 1e6:.1f} M') for k in ('email', 'push notification', 'whatsapp', 'in-app'))
             + NUM(f'{1000 * r.r / r.env:.0f}') + NUM(f'{r.cost / 1e6:.2f} M MXN') + NUM(f'{bm.get(mm[:7], 0) / 1e3:.1f} mil') + '</tr>')
tt = mon.sum()
h.append(f'<tr><td><b>Total</b></td>' + NUM(f'<b>{tt.env / 1e6:.1f} M</b>') + ''.join(NUM(f'{ch[k].sum() / 1e6:.1f} M') for k in ('email', 'push notification', 'whatsapp', 'in-app'))
         + NUM(f'{1000 * tt.r / tt.env:.0f}') + NUM(f'<b>{tt.cost / 1e6:.1f} M MXN</b>') + NUM(f'{pd.read_csv(D + "e5_cohorte_baja.csv").usuarios_baja.sum() / 1e3:.0f} mil únicas') + '</tr></table>')
print('107 mes', (mon.env / 1e6).round(1).to_dict(), (1000 * mon.r / mon.env).round(0).to_dict(), (mon.cost / 1e6).round(2).to_dict())
save(107, dict(kind='html', ancho_completo=True,
    titulo=f'Detalle mensual: junio fue el mes con más mensajes ({mon.env.max() / 1e6:.0f} M) y septiembre el más barato',
    sowhat='Septiembre es el mes base del ahorro por ser el más reciente y el más barato.',
    fuente='Fuente: E1 por mes y canal; personas con baja por mes (E4a) y únicas (E5), enero a septiembre 2026. Respuesta: clic, apertura, lectura y clic in-app.',
    html=''.join(h)), sub=1)
# por día de la semana
e10 = pd.read_csv(D + 'e10_dia_semana.csv')
dw = e10.groupby(['dia_semana_num', 'dia_semana']).agg(env=('envios', 'sum'), r=('respuestas', 'sum'), ee=('email_entregados', 'sum'), b=('bajas_email_eventos', 'sum'), wa=('wa_entregados', 'sum'), cv=('conversiones_filas', 'sum')).reset_index()
ES = {'Sunday': 'Domingo', 'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miércoles', 'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sábado'}
dw['ord'] = dw.dia_semana_num.map(lambda x: (x - 2) % 7); dw = dw.sort_values('ord')
h = ['<table><tr><th>Día</th><th class="num">Mensajes en nueve meses</th><th class="num">De cada 100 mensajes de la semana</th><th class="num">Respuestas por cada mil mensajes</th>'
     '<th class="num">Bajas por cada mil correos entregados</th><th class="num">WhatsApp entregados</th></tr>']
for _, r in dw.iterrows():
    h.append(f'<tr><td><b>{ES[r.dia_semana]}</b></td>' + NUM(f'{r.env / 1e6:.1f} M') + NUM(f'{100 * r.env / dw.env.sum():.0f}') + NUM(f'{1000 * r.r / r.env:.0f}') + NUM(f'{1000 * r.b / r.ee:.1f}') + NUM(f'{r.wa / 1e6:.1f} M') + '</tr>')
h.append('</table>')
best = dw.assign(rpm=1000 * dw.r / dw.env).sort_values('rpm', ascending=False).iloc[0]
print('107 dia', dw.assign(rpm=(1000 * dw.r / dw.env).round(0), bm=(1000 * dw.b / dw.ee).round(2))[['dia_semana', 'env', 'rpm', 'bm']].to_string())
save(107, dict(kind='html', ancho_completo=True,
    titulo=f'Detalle por día: el {ES[best.dia_semana].lower()} trae más respuestas ({1000 * best.r / best.env:.0f} por mil mensajes); el fin de semana se manda la mitad',
    sowhat='El día importa menos que a quién y por qué canal se escribe.',
    fuente='Fuente: Braze, envíos por día de la semana, canal y equipo (E10), enero a septiembre 2026; bajas = eventos de baja de correo.',
    html=''.join(h)), sub=2)
# semanal
wk = e4[e4.grano == 'semana'].copy()
wk['r'] = wk.email_click + wk.pn_open + wk.whatsapp_read + wk.in_app_click
ws = wk.groupby('periodo').agg(env=('envios', 'sum'), r=('r', 'sum'), b=('bajas_email_usuarios', 'sum')).reset_index()
ws = ws[ws.env > 0].reset_index(drop=True)
MS = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']
lab = lambda p: f'{int(p[8:10])} {MS[int(p[5:7]) - 1]}' + (' 2025' if p.startswith('2025') else '')
K = int(np.ceil(len(ws) / 3))
h = ['<table><tr>' + ''.join('<th>Semana del</th><th class="num">Mensajes</th><th class="num" style="padding-right:2cqi">Resp. por mil</th>' for _ in range(3)) + '</tr>']
for i in range(K):
    row = '<tr>'
    for j in range(3):
        k = i + j * K
        if k < len(ws):
            r = ws.loc[k]
            row += f'<td>{lab(r.periodo)}</td>' + NUM(f'{r.env / 1e6:.1f} M') + f'<td class="num" style="padding-right:2cqi">{1000 * r.r / r.env:.0f}</td>'
        else:
            row += '<td></td><td></td><td></td>'
    h.append(row + '</tr>')
h.append('</table>')
top = ws.sort_values('env', ascending=False).iloc[0]
print('107 sem', len(ws), lab(top.periodo), top.env)
save(107, dict(kind='html', ancho_completo=True,
    titulo=f'Detalle semanal: la semana del {lab(top.periodo).replace(" ", " de ", 1).replace("jun", "junio")} tuvo más mensajes ({top.env / 1e6:.0f} M), por BillPay',
    sowhat='Las semanas con más volumen no traen más respuestas por cada mil mensajes.',
    fuente='Fuente: serie semanal por canal (E4a), enero a septiembre 2026; la primera y la última semana están incompletas.',
    html=''.join(h)), sub=3)

# ------------------------------------------------------------------ 108. Fichas de 15 campañas
NOMB = {('B0333', 'whatsapp'): 'Oferta a clientes KPay sin compra en un año', ('B0211', 'email'): 'Tasa 0 a registrados de KPay sin Cash',
        ('B0332', 'whatsapp'): 'Oferta a clientes KPay sin compra en 6 meses', ('B0223', 'email'): 'Installments a registrados que nunca activaron',
        ('B0223', 'whatsapp'): 'Installments a registrados que nunca activaron', ('B0619', 'whatsapp'): 'Venta cruzada de KPay a Cash, Fiestas Patrias',
        ('B0620', 'whatsapp'): 'Venta cruzada de Cash a leads de KPay', ('B0331', 'whatsapp'): 'Oferta a clientes KPay poco activos',
        ('B0000', 'email'): 'Recordatorio de terminar la verificación', ('B0209', 'email'): 'Descuento a clientes inactivos de Cash',
        ('B0301', 'whatsapp'): 'Cash a plazos a clientes activos'}
def nombre(f, cn):
    tk = datos.ticket(f)
    if tk == 'B0326': return 'Referidos a dormants de ' + ('KPay' if '-KPay-' in f else 'KCash')
    if tk == 'B0171': return 'Rescate Tasa 0 a leads ' + ('rezagados' if 'Rezagada' in f else 'calientes')
    return NOMB.get((tk, cn), f)
AUD = {'recup': 'Ex clientes', 'activ': 'Leads y registrados', 'clien': 'Clientes activos', 'otros': 'Clientes KPay'}
QUE = {'b_cortar': 'Se quita ya', 'b_medir': 'Se mide antes de cortar', 'b_pref': 'Solo a quien responde por este canal', 'b_desp': 'Excluir bloqueados'}
top = c.sort_values('tot', ascending=False).head(15).reset_index(drop=True)
def que(r):
    ya = r.b_desp + r.b_cortar + r.b_pref
    if r.accion == 'Bajar frecuencia': return f'Bajar frecuencia; {r.b_pref / 1e3:.0f} mil por canal preferido'
    if ya >= 0.1 * r.tot and r.b_medir >= 0.1 * r.tot: return f'{r.b_medir / 1e3:.0f} mil se miden; {ya / 1e3:.0f} mil se quitan ya'
    if r.accion == 'Limpiar base de WhatsApp' and r.main == 'b_cortar': return 'Solo a quien lee WhatsApp'
    return QUE[r.main]
top['main'] = top[['b_desp', 'b_cortar', 'b_pref', 'b_medir']].idxmax(axis=1)
sh15 = top.tot.sum() / R['total']
print('108', [(nombre(r.fam, r.canal), r.canal, round(r.tot)) for _, r in top.iterrows()], round(sh15, 3))
for sub, rr in ((1, range(0, 8)), (2, range(8, 15))):
    h = ['<table><tr><th style="width:3%">#</th><th style="width:24%">Campaña</th><th style="width:10%">Equipo</th><th style="width:7%">Canal</th><th style="width:10%">A quién</th>'
         '<th class="num" style="width:8%">Mensajes en sept.</th><th class="num" style="width:11%">Respuesta</th><th class="num" style="width:9%">Ahorro al mes</th><th style="width:18%;padding-left:1.2cqi">Qué se hace</th></tr>']
    for i in rr:
        r = top.loc[i]
        resp = f'{r.resp * 1000:.1f} clics por mil' if r.canal == 'email' else f'{r.resp * 100:.0f} de cada 100 leídos'
        h.append(f'<tr><td>{i + 1}</td><td><b>{nombre(r.fam, r.canal)}</b> ({datos.ticket(r.fam)})</td><td>{r.equipo}</td><td>{"Correo" if r.canal == "email" else "WhatsApp"}</td>'
                 f'<td>{AUD[r.aud[:5]]}</td>' + NUM(f'{r.env_sep / 1e6:.2f} M') + NUM(resp) + NUM(f'<b>{r.tot / 1e3:.0f} mil MXN</b>') + f'<td style="padding-left:1.2cqi">{que(r)}</td></tr>')
    h.append('</table>')
    save(108, dict(kind='html', ancho_completo=True,
        titulo=f'Fichas de las 15 campañas con más ahorro: juntas suman {m(top.tot.sum())} M MXN al mes, {sh15 * 100:.0f} % del total' if sub == 1 else 'Fichas de las 15 campañas con más ahorro (continuación): Marketing aparece por canal y recuperación',
        sowhat='Empezar por las tres primeras: dos ofertas a ex clientes de KPay y Tasa 0 a registrados.' if sub == 1 else 'En Marketing el ahorro es de canal y de recuperación, no de apagar.',
        fuente='Fuente: E1 por campaña y canal, septiembre 2026; Sheets v4, E9b y E7a. Ahorro = palancas de la lámina 92; respuesta de enero a septiembre.',
        html=''.join(h)), sub=sub)

# ------------------------------------------------------------------ 109. Supuestos de costo
nodel = d1.whatsapp_send.sum() - d1.whatsapp_delivery.sum()
c_env = d1.email_sent.sum() * 0.05 + d1.whatsapp_send.sum() * 1.0
g9 = d1.costo.sum(); SEPc = R['sep']; AVG = g9 / 9
e9 = pd.read_csv(D + 'e9b_patron_respuesta_90d.csv')
sh_wa = e9[e9.resp_wa == 0].msgs_wa_entregados.sum() / e9.msgs_wa_entregados.sum(); sh_em = e9[e9.resp_email == 0].msgs_email.sum() / e9.msgs_email.sum()
SUP = [('Correo', '0.05 MXN por enviado', 'Se cobra todo lo que sale'),
       ('WhatsApp', '1.00 MXN por entregado', f'{m(nodel, 1)} M sin entregar no se pagaron'),
       ('Push e in-app', '0 MXN por mensaje', 'Su costo es el permiso, que no se ve'),
       ('Gasto de nueve meses', f'{m(g9, 1)} M MXN', f'{m(c_env, 1)} M MXN si WhatsApp se cobrara por enviado'),
       ('Mes base', f'Septiembre: {m(SEPc)} M MXN', f'Promedio: {m(AVG)} M MXN al mes; ahorro conservador'),
       ('Ahorro por campaña', 'Costo de septiembre', 'Palancas en orden, sin doble conteo'),
       ('Lecturas de WhatsApp', 'Cuentan las del mes siguiente', 'Se suman a la campaña que las mandó'),
       ('A quien no responde', f'{sh_wa * 100:.0f} % del WhatsApp, {sh_em * 100:.0f} % del correo', 'Proporción de E9b en 90 días'),
       ('Costo fijo de Braze', 'X, editable', 'No entra en el gasto ni en el ahorro: solo se cuentan las tarifas por mensaje')]
h = ['<table><tr><th style="width:20%">Supuesto</th><th style="width:26%">Valor</th><th>Qué implica</th></tr>']
for a, b, c_ in SUP:
    h.append(f'<tr><td><b>{a}</b></td><td><b>{b}</b></td><td>{c_}</td></tr>')
h.append('</table>')
print('109', g9, c_env, SEPc, AVG, nodel, sh_wa, sh_em)
save(109, dict(kind='html', ancho_completo=True,
    titulo='Supuestos de costo: WhatsApp por entregado, correo por enviado, septiembre como base y Braze fijo como X',
    sowhat=f'Cobrar WhatsApp por enviado subiría el gasto de nueve meses de {m(g9, 1)} a {m(c_env, 1)} M MXN.',
    fuente=f'Fuente: Braze, envíos por comunicación, mes y canal (E1) y respuesta en 90 días (E9b), enero a septiembre 2026; parámetros del Sheets v4.',
    html=''.join(h)))

# ------------------------------------------------------------------ 110. Puente entre cifras
mc = pd.read_csv(ROOT + 'hallazgos/muestra_c_familias.csv')
mc['ah_ent'] = np.where(mc.canal == 'whatsapp', mc.ahorro_mxn_mes * mc.entrega_pct / 100, mc.ahorro_mxn_mes)
v_c, v_c2 = mc.ahorro_mxn_mes.sum(), mc.ah_ent.sum()
ap = (c.senal == 'apagar o rehacer') & (c.accion != 'No tocar') & (c.activo == 1)
v_deck, v_sep = c[ap].ahorro_mes_ent.sum(), c[ap].c_sep.sum(); in85 = c[ap].tot.sum(); out = c[~ap]
pg_c = mc[(mc.ahorro_mxn_mes > 0) & (mc.team == 'Product Growth')].ahorro_mxn_mes.sum() / v_c
pg_d = c[c.equipo == 'Product Growth'].ahorro_mes_ent.sum() / c.ahorro_mes_ent.sum()
pg_n = c[c.equipo == 'Product Growth'].tot.sum() / R['total']
ST = [('total', 'Nota de campañas', v_c, f'Product Growth {pg_c * 100:.0f} %'),
      ('step', 'Cobrar WhatsApp por entregado', v_c2 - v_c, ''),
      ('step', 'Contar lecturas del mes siguiente', v_deck - v_c2, '4 WhatsApp ya leen 60 % o más'),
      ('total', 'Cifra del deck anterior', v_deck, f'Product Growth {pg_d * 100:.0f} %'),
      ('step', 'Usar el costo de septiembre', v_sep - v_deck, ''),
      ('step', 'Solo lo que va a quien no responde', in85 - v_sep, 'en limpiar WhatsApp y rehacer'),
      ('step', 'Bloqueados en otras campañas', out.bloqueados.sum(), ''),
      ('step', 'Canal preferido', out.canal_preferido.sum(), ''),
      ('step', 'Sin respuesta en 90 días', out.sin_respuesta_90d.sum(), ''),
      ('step', 'Pruebas internas y duplicados', out.pruebas.sum() + DUP, ''),
      ('total', 'Cifra única', in85 + out.tot.sum() + DUP, f'Product Growth {pg_n * 100:.0f} %')]
print('110', [(a, b, round(v / 1e6, 3)) for a, b, v, _ in ST])
o = svg_open(f'Puente de {m(v_c)} M y {m(v_deck)} M MXN al mes a la cifra única de {m(ST[-1][2])} M.')
o.append(f'<rect x="0" y="6" width="12" height="12" rx="2" fill="{MARK2}"/>' + t(18, 16.5, 'Baja la cifra', 12, TXT))
o.append(f'<rect x="120" y="6" width="12" height="12" rx="2" fill="{BLUE}"/>' + t(138, 16.5, 'Sube la cifra', 12, TXT))
o.append(f'<rect x="240" y="6" width="12" height="12" rx="2" fill="{MARK}"/>' + t(258, 16.5, 'Cifra resultante', 12, TXT))
X0, X1, VM = 236, 560, 3.5e6; sx = lambda v: X0 + (X1 - X0) * v / VM
TOPY, RH, BH = 46, 31.5, 17
AX = TOPY + len(ST) * RH + 2
for v in (0, 1, 2, 3):
    o.append(f'<line x1="{sx(v * 1e6):.1f}" y1="{TOPY - 6}" x2="{sx(v * 1e6):.1f}" y2="{AX}" stroke="{GRID}" stroke-width="1"/>')
    o.append(t(sx(v * 1e6), AX + 14, f'{v} M' if v else '0', 11, SEC, 400, 'middle'))
o.append(t(X1 + 10, AX + 14, 'MXN al mes', 11, SEC))
run = 0; prev = None
for i, (k, lab, v, note) in enumerate(ST):
    yc = TOPY + i * RH + RH / 2; yb = yc - BH / 2
    if k == 'total':
        x0, x1 = sx(0), sx(v); run = v; fill = MARK; val = f'{m(v)} M'; edge = x1
    else:
        a, b = sorted([run, run + v]); x0, x1 = sx(a), sx(b); run += v
        fill = BLUE if v > 0 else MARK2; val = ('más ' if v > 0 else 'menos ') + f'{abs(v) / 1e6:.2f}'; edge = sx(run)
    if x1 - x0 < 2: x0 = x1 - 2
    o.append(t(X0 - 10, yc + 4.3, lab, 12.5, INK if k == 'total' else TXT, 600 if k == 'total' else 400, 'end'))
    o.append(f'<rect x="{x0:.1f}" y="{yb:.1f}" width="{x1 - x0:.1f}" height="{BH}" rx="2" fill="{fill}"/>')
    o.append(t(max(x1, sx(run)) + 6, yc + 4.5, val, 12.5, INK, 600 if k == 'total' else 400))
    if prev is not None:
        o.append(f'<line x1="{prev:.1f}" y1="{yb - (RH - BH):.1f}" x2="{prev:.1f}" y2="{yb:.1f}" stroke="{MARK}" stroke-width="1"/>')
    prev = edge
    if note: o.append(t(780, yc + 4.3, note, 11.5, INK if k == 'total' else SEC, 600 if k == 'total' else 400, 'end'))
o.append('</svg>')
save(110, dict(kind='grafica',
    titulo=f'Por qué había dos cifras de ahorro: de {m(v_c, 1)} y {m(v_deck, 1)} M a una sola de {m(ST[-1][2])} M MXN al mes',
    lecturas=[f'{m(v_c)} M MXN al mes cobraba WhatsApp por enviado y no contaba lecturas tardías: corregido da {m(v_deck)} M.',
              f'Con las lecturas tardías cuatro WhatsApp leen 60 % o más; Product Growth sube a {pg_d * 100:.0f} %.',
              'La cifra única usa septiembre, cuenta solo a quien no responde y suma otras palancas sin doble conteo.'],
    causa='Cada cifra usó supuestos distintos de cobro, de mes y de qué contar; la propuesta los fija una vez.',
    sowhat=f'Usar solo {m(ST[-1][2])} M MXN al mes ({ST[-1][2] * 12 / 1e6:.0f} M al año); las otras dos cifras quedan reemplazadas.',
    fuente=f'Fuente: nota de campañas (muestra C), Sheets v4 y E1 de septiembre 2026. Montos incrementales en el orden de esta cascada; por palanca, ver lámina 92.',
    svg=''.join(o)))
print('ok anexo')
