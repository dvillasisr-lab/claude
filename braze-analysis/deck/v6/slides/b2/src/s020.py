"""Lámina 20: cierre de la sección II (canales). Las cifras salen de los mismos cálculos de las láminas 11 a 19."""
from b2base import *

d = load_b()
w = d[d.canal == 'whatsapp']
WT, CT = w.costo.sum() / 1e6, d.costo.sum() / 1e6
fr = w[w.aud == 'frios']
cpc = lambda g: g.costo.sum() / max(1, g.conversiones_fraccional.sum())
mix = d.groupby(['equipo', 'canal']).envios.sum().unstack().fillna(0)
inapp_max = (100 * mix['in-app'] / mix.sum(axis=1)).max()
# promoción debajo del mínimo
p = d[d.tipo == 'promocional']
fa = p.groupby(['fam', 'canal']).agg(b=('b', 'sum'), r=('r', 'sum'), env=('envios', 'sum')).reset_index()
fa = fa[fa.b >= 5e4]
fa['bajo'] = 100 * fa.r / fa.b < fa.canal.map(MIN)
pv = 100 * fa[fa.bajo].env.sum() / fa.env.sum()
# canal sin respuesta (E7b / E9b)
R = '/home/user/claude/braze-analysis/data/'
def otro(path):
    e = pd.read_csv(R + path)
    msgs = e[['msgs_email', 'msgs_push', 'msgs_wa', 'msgs_inapp']].sum(axis=1)
    ot = (1 - e.resp_email) * e.msgs_email + (1 - e.resp_push) * e.msgs_push + (1 - e.resp_wa) * e.msgs_wa + (1 - e.resp_inapp) * e.msgs_inapp
    oc = (1 - e.resp_email) * e.msgs_email * 0.05 + (1 - e.resp_wa) * e.msgs_wa_entregados
    some = e[['resp_email', 'resp_push', 'resp_wa', 'resp_inapp']].sum(axis=1) > 0
    return e, msgs, ot, oc, some
e7, m7, o7, c7, s7 = otro('e7b_patron_respuesta.csv')
e9, m9, o9, c9, s9 = otro('e9b_patron_respuesta_90d.csv')
pct_otro = 100 * o7.sum() / m7.sum()
q_msgs, q_mxn = o9[s9].sum() / 1e6, c9[s9].sum() / 1e6
wa90 = e9[e9.resp_wa == 0].msgs_wa_entregados.sum() / 1e6
ent = 100 * w.whatsapp_delivery.sum() / w.whatsapp_send.sum()
print('WA', WT, 100 * WT / CT, 'frios %', 100 * fr.costo.sum() / 1e6 / WT, cpc(fr), 'inapp max', inapp_max, 'promo bajo', pv,
      'otro', pct_otro, 'trimestre', q_msgs, q_mxn, 'wa90', wa90, 'entrega', ent)

save(20, dict(
    kind='cierre',
    titulo='Por qué pasa: el canal se elige por equipo y por costumbre, no por quién responde ni por cuánto cuesta cada respuesta',
    porques=[
        f'WhatsApp se lleva {WT:.1f} M MXN en nueve meses, {100*WT/CT:.0f} % del gasto, y {100*fr.costo.sum()/1e6/WT:.0f} % va a ex clientes y leads que nunca activaron, donde cada conversión cuesta {cpc(fr):.0f} MXN.',
        f'{pct_otro:.0f} % de los mensajes salen por un canal al que esa persona nunca respondió, y {pv:.0f} % del volumen de promoción no llega a lo mínimo aceptable.',
        f'Cada equipo usa el canal que acostumbra: WhatsApp para rescates, push para ofertas porque no cuesta, correo para todo. In-app, que más conversiones trae, no pasa de {inapp_max:.0f} % de los mensajes de ningún equipo.',
        'Nadie compara cuánto cuesta cada conversión en cada canal ni mide cada campaña contra un mínimo común; cada equipo ve solo su campaña.',
        'Causa raíz: Braze no guarda por qué canal responde cada persona y no hay una regla de canal por costo, así que nadie puede elegir el canal por persona.',
    ],
    hipotesis={
        'A': 'Si cada persona recibe los mensajes por el canal al que respondió en 90 días, suben las respuestas por cada mil mensajes y baja el gasto sin perder conversiones. Se prueba con un grupo que sigue igual.',
        'O': 'Si WhatsApp solo sale a quien lo leyó en 90 días, con presupuesto mensual con límite por equipo, y push solo a quien abrió uno en 60 días, dejamos de pagar y de mandar mensajes que nadie lee.',
        'G': 'Si un responsable de canales revisa cada mes las campañas contra el mínimo aceptable y el costo por conversión, las que no llegan se rehacen o se quitan en lugar de repetirse.',
    },
    como=[
        'Semanas 1 y 2: en Braze, atributo de canal preferido (última respuesta en 90 días) y segmentos de quien leyó WhatsApp en 90 días o abrió push en 60. Marketing con el equipo de datos. Métrica: personas con canal.',
        'Semana 3: en los Canvas de Marketing y Product Growth, WhatsApp solo a ese segmento, con presupuesto con límite y 10 % sin mensajes. Métrica: MXN por conversión.',
        'Semanas 3 y 4: referidos, lanzamientos y recordatorios primero por in-app; sin app, por correo. Métrica: conversiones por cada mil mensajes.',
        f'Semana 4: quitar de WhatsApp los números que no recibieron en 90 días. Métrica: entrega arriba de 80 % (hoy {ent:.0f} %).',
        f'Cada mes: tablero de campañas contra el mínimo; dos meses sin llegar, se rehacen o se quitan. Métrica: promoción debajo del mínimo (hoy {pv:.0f} %).',
    ],
    impacto=f'Canal por persona: {q_msgs:.0f} M mensajes y {q_mxn:.1f} M MXN menos por trimestre. WhatsApp solo a quien lo leyó: hasta {wa90:.1f} M MXN por trimestre. Se traslapan; caben en el ahorro total de hasta 2.34 M MXN al mes.',
    sowhat='Elegir el canal por persona y por costo por respuesta baja el gasto sin dejar de buscar a nadie: a los ex clientes se les sigue escribiendo por el canal más barato que sí usan, con un grupo sin mensajes para medir.',
    fuente='Fuente: láminas 11 a 19; Braze, envíos por campaña, mes y canal, y mensajes y respuesta por persona, enero a septiembre 2026. Los ahorros se traslapan y no se suman. Falta saber quién tiene la app (token de push o inicio de sesión por persona).',
))
