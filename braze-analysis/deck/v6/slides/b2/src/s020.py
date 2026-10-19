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
    titulo='Por qué pasa: el canal lo elige cada equipo por costumbre, no por quién responde ni por lo que cuesta',
    porques=[
        f'WhatsApp es {100*WT/CT:.0f} % del gasto y la mitad va a bases frías, a {cpc(fr):.0f} MXN por conversión.',
        f'{pct_otro:.0f} % de los mensajes van por un canal al que esa persona nunca respondió.',
        f'In-app es el que más convierte y ningún equipo le da más de {inapp_max:.0f} % de sus mensajes.',
        'Nadie compara costo por conversión entre canales ni mide cada campaña contra un mínimo.',
        'Causa raíz: Braze no guarda el canal al que responde cada persona ni hay regla por costo.',
    ],
    hipotesis={
        'A': 'Mandar por el canal al que cada quien respondió en 90 días sube la respuesta y baja el gasto.',
        'O': 'WhatsApp solo a quien lo leyó en 90 días y push a quien abrió en 60 dejan de pagar lo que nadie lee.',
        'G': 'Un responsable revisa cada mes campañas contra el mínimo y costo por conversión.',
    },
    como=[
        'Semanas 1 y 2: atributo de canal preferido y segmentos por lectura reciente en Braze; Marketing.',
        'Semana 3: en los Canvas, WhatsApp solo a ese segmento, con límite y 10 % sin envío.',
        f'Semana 4: quitar números de WhatsApp sin entrega en 90 días; meta de entrega 80 % (hoy {ent:.0f} %).',
        'Cada mes: rehacer o quitar campañas debajo del mínimo; hoy son 4 de cada 10 mensajes del año.',
    ],
    impacto=f'Canal por persona: {q_msgs:.0f} M mensajes menos por trimestre y 0.34 M MXN al mes, parte de los 2.34 M MXN del plan.',
    sowhat='Elegir el canal por persona y por costo baja el gasto sin dejar de buscar a los ex clientes.',
    fuente='Fuente: láminas 11 a 19; Braze, envíos por campaña y respuesta por persona, enero a septiembre 2026. Los ahorros se traslapan y no se suman.',
))
