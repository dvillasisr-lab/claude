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
SD = pathlib.Path('/home/user/claude/braze-analysis/deck/v6/muestras/s3_datos.json')
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


# ---------------- estilos en línea comunes (paleta del deck)
BLUE_SOFT, GREEN_SOFT, PAPER2 = '#E8EEFC', '#E4F2EC', '#F4F6F9'
def tile(big, line, col, bg):
    return (f'<div style="background:{bg};padding:1.6cqi 1.5cqi;display:flex;flex-direction:column;gap:.7cqi">'
            f'<div class="big" style="color:{col};font-size:4.2cqi">{big}</div>'
            f'<div style="font-size:1.25cqi;line-height:1.35;color:{INK}">{line}</div></div>')

# ---------------- 2. Resumen ejecutivo: tres cifras grandes y cuatro frases cortas
tiles = (
    '<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1.4cqi">'
    + tile(f'{rpm[9]:.0f}', f'respuestas por cada mil mensajes en septiembre; en enero eran {rpm[1]:.0f}', INK, PAPER2)
    + tile(f'{mes / 1e6:.1f} M MXN', f'al mes en mensajes, sin la licencia de Braze; {wa_cost * 100:.0f} % es WhatsApp', INK, PAPER2)
    + tile(f'{tot:.2f} M MXN', f'al mes de ahorro: {seg:.2f} M se quita ya sin perder ventas y {med:.2f} M solo si no recupera clientes', GREEN, GREEN_SOFT)
    + '</div>')
def frase(n, lab, prob, acc):
    return (f'<div style="display:flex;gap:.9cqi;align-items:flex-start;border-top:1px solid #DDE2EA;padding-top:1.1cqi">'
            f'<div style="flex:0 0 auto;width:1.9cqi;height:1.9cqi;border-radius:50%;background:{BLUE_SOFT};color:{BLUE};font-weight:700;font-size:1cqi;display:flex;align-items:center;justify-content:center">{n}</div>'
            f'<div style="font-size:1.3cqi;line-height:1.4;color:{INK}"><b>{lab}.</b> {prob}<br><span style="color:{GREEN};font-weight:600">{acc}</span></div></div>')
frases = (
    '<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1.6cqi 2.4cqi;margin-top:2.4cqi">'
    + frase(1, 'A quién', f'{bloq / 1e6:.0f} M promociones fueron a personas bloqueadas.', 'Una exclusión común en toda campaña promocional.')
    + frase(2, 'Por dónde', f'{mudo_pct * 100:.0f} % de los mensajes va a un canal que esa persona nunca usó.', 'Cada persona por el canal al que responde.')
    + frase(3, 'Cuántas veces', f'{b_u / 1e3:.0f} mil personas reciben casi dos mensajes al día.', 'Máximo 5 promociones por persona a la semana.')
    + frase(4, 'Cómo medimos', f'Solo {ctl_big} de {canv:,} Canvas tiene un grupo grande sin mensajes.', 'Un grupo sin mensajes de 5 a 10 % en toda campaña.')
    + '</div>')
write(2, dict(kind='html', ancho_completo=True,
              titulo='Mandamos más y nos responden menos; cuatro reglas bajan el gasto sin dejar de buscar a quien recuperamos',
              que='Sobre todo promociones: Tasa 0, referidos, descuentos, rescates y lanzamientos.',
              quien='Marketing y Product Growth mandan dos de cada tres mensajes.',
              a_quien='Leads, registrados sin crédito, ex clientes y clientes activos.',
              html=tiles + frases,
              sowhat='El problema es la forma de operar, no una campaña: se corrige con reglas comunes, no apagando todo.',
              fuente='Fuente: Braze, enero a septiembre 2026 (E1, E3, E7b, E13; bloqueados del Sheets v4). Ahorro sobre el gasto de septiembre, del caso de negocio. WhatsApp a 1.00 MXN por entregado.'))

# ---------------- 3. Cuatro decisiones: cuatro tarjetas
def card(n, tit, line, big, sub, col, bg):
    return (f'<div style="background:{bg};padding:1.2cqi 1.2cqi 1.1cqi;display:flex;flex-direction:column;gap:.7cqi;min-height:0">'
            f'<div style="font-size:.85cqi;letter-spacing:.1em;text-transform:uppercase;color:{SEC};font-weight:600">Decisión {n}</div>'
            f'<div style="font-size:1.45cqi;font-weight:700;line-height:1.2;color:{INK}">{tit}</div>'
            f'<div style="font-size:1.08cqi;line-height:1.35;color:#3B4556;flex:1">{line}</div>'
            f'<div style="border-top:1px solid #DDE2EA;padding-top:.7cqi"><div class="big" style="color:{col};font-size:2.8cqi">{big}</div>'
            f'<div style="font-size:.95cqi;line-height:1.3;color:{SEC};margin-top:.3cqi">{sub}</div></div></div>')
cards = (
    '<div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1.2cqi;height:82%">'
    + card(1, 'A quién le escribimos', 'Una exclusión común en toda promoción: tarjeta KPay congelada, lista negra, quien pidió no recibir publicidad y dados de baja.',
           f'{d1:.2f} M', 'MXN al mes; se quita ya sin perder ventas', BLUE, PAPER2)
    + card(2, 'Por qué canal y cuántas veces', 'Cada persona por el canal al que respondió en 90 días; WhatsApp solo a quien lo lee; máximo 5 promociones a la semana.',
           f'{d2:.2f} M', 'MXN al mes; se quita ya sin perder ventas', BLUE, PAPER2)
    + card(3, 'Cómo medimos', 'Un grupo de 5 a 10 % sin mensajes en toda campaña, empezando por la recuperación de ex clientes.',
           f'{d3:.2f} M', 'MXN al mes; se quita solo si no recupera clientes', GREEN, GREEN_SOFT)
    + card(4, 'Quién decide', 'Un dueño por segmento, un calendario común entre equipos y un catálogo de campañas activas.',
           'Sostiene', 'las otras tres decisiones; no tiene monto propio', SEC, PAPER2)
    + '</div>'
    f'<div style="margin-top:1.2cqi;display:flex;align-items:baseline;gap:1.2cqi"><div class="big" style="font-size:2.6cqi">{tot:.2f} M MXN al mes</div>'
    f'<div class="bigl" style="margin:0">en total ({R["anual"] / 1e6:.0f} M MXN al año). Los montos no se traslapan: salen en cadena del gasto de septiembre.</div></div>')
write(3, dict(kind='html', ancho_completo=True,
              titulo='Cuatro decisiones ordenan a quién, por dónde y cuántas veces escribimos, y nos dejan medir qué vende',
              que='Promociones; avisos de servicio y cobranza quedan fuera del límite.',
              quien='Todos los equipos; MarTech configura Braze y CRM lleva calendario y medición.',
              a_quien='Bloqueados fuera; ex clientes con plan de recuperación; activos por su canal.',
              html=cards,
              sowhat='Ninguna decisión corta el contacto con quien queremos recuperar: cambian canal, frecuencia y medición.',
              fuente='Fuente: caso de negocio sobre el gasto de septiembre 2026 (4.23 M MXN). 1 = bloqueados, duplicados y pruebas; 2 = canal, email y WhatsApp; 3 = ex clientes y sin respuesta en 90 días.'))

# ---------------- 4. Divisor del Acto 1
write(4, dict(kind='divisor', acto='Acto 1 · Qué pasa hoy', titulo='Mandamos mucho y nos responden cada vez menos',
              subtitulo='Cuánto mandamos, cuánto cuesta y por qué cada mensaje responde menos que en enero.'))
