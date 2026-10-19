"""Lámina 18: mapa de calor patrón de respuesta de la persona (filas) por canal enviado (columnas): millones de mensajes,
azul si esa persona nunca respondió por ese canal, verde si sí. A la derecha: personas, parte de sus mensajes por otro canal y gasto.
Nueve meses (E7b) y, abajo, julio a septiembre (E9b)."""
from b2base import *

R = '/home/user/claude/braze-analysis/data/'
CE, CW = 0.05, 1.00
CHS = [('email', 'msgs_email', 'Correo'), ('push', 'msgs_push', 'Push'), ('wa', 'msgs_wa', 'WhatsApp'), ('inapp', 'msgs_inapp', 'In-app')]
NM = {'resp_email': 'correo', 'resp_push': 'push', 'resp_wa': 'WhatsApp', 'resp_inapp': 'in-app'}


def prep(path):
    d = pd.read_csv(path)
    d['msgs'] = d[['msgs_email', 'msgs_push', 'msgs_wa', 'msgs_inapp']].sum(axis=1)
    d['costo'] = d.msgs_email * CE + d.msgs_wa_entregados * CW
    d['otro'] = sum((1 - d['resp_' + c]) * d[m] for c, m, _ in CHS)
    d['otro_costo'] = (1 - d.resp_email) * d.msgs_email * CE + (1 - d.resp_wa) * d.msgs_wa_entregados * CW
    d['nresp'] = d[['resp_email', 'resp_push', 'resp_wa', 'resp_inapp']].sum(axis=1)
    return d


a, b = prep(R + 'e7b_patron_respuesta.csv'), prep(R + 'e9b_patron_respuesta_90d.csv')
def lab(r):
    ch = [NM[c] for c in NM if r[c] == 1]
    if not ch:
        return 'Ningún canal'
    if len(ch) == 4:
        return 'Los cuatro canales'
    if len(ch) == 1:
        return 'Solo ' + ch[0]
    return ', '.join(ch[:-1]) + ' e ' + ch[-1] if ch[-1].startswith('in') else ', '.join(ch[:-1]) + ' y ' + ch[-1]
a['lab'] = a.apply(lab, axis=1).map(lambda x: x[0].upper() + x[1:])
a = a.sort_values('msgs', ascending=False)
TOP = a.head(8)
REST = a.iloc[8:]
M, C = a.msgs.sum(), a.costo.sum()
for d_, nm in ((a, 'nueve meses'), (b, '90 días')):
    print(nm, 'msgs', d_.msgs.sum() / 1e6, 'otro', d_.otro.sum() / 1e6, d_.otro.sum() / d_.msgs.sum(), 'otro_costo', d_.otro_costo.sum() / 1e6, 'costo', d_.costo.sum() / 1e6)
resp = a[a.nresp > 0]
e_otro = resp[resp.resp_email == 0]
p_otro = resp[resp.resp_push == 0]
w_otro = resp[resp.resp_wa == 0]
sw = a[a.lab == 'Solo WhatsApp'].iloc[0]
br = b[b.nresp > 0]
print('emails a quien responde por otro', e_otro.msgs_email.sum() / 1e6, e_otro.usuarios.sum() / 1e6, 'push', p_otro.msgs_push.sum() / 1e6, 'wa ent', w_otro.msgs_wa_entregados.sum() / 1e6)
print('solo WA', sw.usuarios / a.usuarios.sum(), sw.msgs_email / 1e6, sw.msgs_push / 1e6, sw.costo / C)
print('90d sin ningún: otro', br.otro.sum() / 1e6, br.otro_costo.sum() / 1e6)
print(TOP[['lab', 'usuarios', 'msgs', 'otro', 'costo']].assign(msgs=lambda x: x.msgs / 1e6).round(2).to_string())
print('rest', REST.usuarios.sum(), REST.msgs.sum() / 1e6)

S = Svg('Mapa de calor: millones de mensajes por patrón de respuesta de la persona y canal enviado; en azul, mensajes por un canal al que esa persona nunca respondió.')
S.rect(0, 6, 12, 12, '#DCE5FB'); S.rect(2, 8, 8, 8, BLUE)
S.t(18, 16, 'Por un canal al que esa persona nunca respondió', 11.5, INK, w=600)
S.rect(330, 6, 12, 12, '#DDF0E8'); S.rect(332, 8, 8, 8, GREEN)
S.t(348, 16, 'Por un canal al que sí respondió', 11.5, TXT)
S.t(0, 34, 'Millones de mensajes de enero a septiembre, según por qué canal respondió cada persona alguna vez (clic, apertura o lectura).', 10.5, SEC)
LX, CX0, CW_, RH, Y0 = 0, 150, 70, 30, 72
S.t(LX, Y0 - 10, 'Responde por', 10.5, SEC, w=600)
for j, (_, _, cl) in enumerate(CHS):
    S.t(CX0 + CW_ * j + CW_ / 2, Y0 - 10, cl, 11, INK, 'middle', 600)
K1, K2, K3 = 520, 632, 720
S.t(K1, Y0 - 22, 'Personas', 10.5, SEC, 'end'); S.t(K1, Y0 - 10, 'millones', 10.5, SEC, 'end')
S.t(K2, Y0 - 22, 'Mensajes por canal', 10.5, SEC, 'end'); S.t(K2, Y0 - 10, 'sin respuesta', 10.5, SEC, 'end')
S.t(K3 + 56, Y0 - 22, 'Gasto', 10.5, SEC, 'end'); S.t(K3 + 56, Y0 - 10, 'M MXN', 10.5, SEC, 'end')
rows = [(r.lab, r) for r in TOP.itertuples()]
for i, (lb, r) in enumerate(rows):
    y = Y0 + RH * i
    big = r.lab in ('Ningún canal', 'Solo WhatsApp')
    S.t(LX, y + RH / 2 + 4, lb, 11, INK if big else TXT, w=600 if big else 400)
    for j, (c, m, cl) in enumerate(CHS):
        v = getattr(r, m) / 1e6
        ok = getattr(r, 'resp_' + c) == 1
        S.rect(CX0 + CW_ * j, y + 1, CW_ - 2, RH - 2, '#DDF0E8' if ok else '#DCE5FB')
        S.t(CX0 + CW_ * j + CW_ / 2 - 1, y + RH / 2 + 4, f'{v:.1f}', 11, GREEN if ok else BLUE, 'middle', 600 if v >= 10 else 400)
    S.t(K1, y + RH / 2 + 4, f'{r.usuarios/1e6:.2f}', 11, INK if big else TXT, 'end')
    S.t(K2, y + RH / 2 + 4, f'{100*r.otro/r.msgs:.0f} %', 11, INK if big else TXT, 'end', 600 if big else 400)
    S.t(K3 + 56, y + RH / 2 + 4, f'{r.costo/1e6:.1f}', 11, INK if big else TXT, 'end', 600 if big else 400)
y = Y0 + RH * len(rows)
S.t(LX, y + RH / 2 + 4, f'Otras 8 combinaciones', 11, TXT)
for j, (c, m, cl) in enumerate(CHS):
    v = REST[m].sum() / 1e6
    no = (REST[m] * (1 - REST['resp_' + c])).sum() / 1e6
    S.rect(CX0 + CW_ * j, y + 1, CW_ - 2, RH - 2, '#F3F5F8')
    S.t(CX0 + CW_ * j + CW_ / 2 - 1, y + RH / 2 + 4, f'{v:.1f}', 11, TXT, 'middle')
S.t(K1, y + RH / 2 + 4, f'{REST.usuarios.sum()/1e6:.2f}', 11, TXT, 'end')
S.t(K2, y + RH / 2 + 4, f'{100*REST.otro.sum()/REST.msgs.sum():.0f} %', 11, TXT, 'end')
S.t(K3 + 56, y + RH / 2 + 4, f'{REST.costo.sum()/1e6:.1f}', 11, TXT, 'end')
y += RH + 4
S.line(0, y, 780, y, INK, 1)
y += 4
S.t(LX, y + RH / 2 + 4, 'Total nueve meses', 11.5, INK, w=700)
for j, (c, m, cl) in enumerate(CHS):
    S.t(CX0 + CW_ * j + CW_ / 2 - 1, y + RH / 2 + 4, f'{a[m].sum()/1e6:.0f}', 11, INK, 'middle', 600)
S.t(K1, y + RH / 2 + 4, f'{a.usuarios.sum()/1e6:.1f}', 11, INK, 'end', 600)
S.t(K2, y + RH / 2 + 4, f'{100*a.otro.sum()/M:.0f} %', 12, BLUE, 'end', 700)
S.t(K3 + 56, y + RH / 2 + 4, f'{C/1e6:.1f}', 11, INK, 'end', 600)
y += RH
S.t(LX, y + RH / 2 + 4, 'Julio a septiembre', 11.5, INK, w=700)
for j, (c, m, cl) in enumerate(CHS):
    S.t(CX0 + CW_ * j + CW_ / 2 - 1, y + RH / 2 + 4, f'{b[m].sum()/1e6:.0f}', 11, INK, 'middle', 600)
S.t(K1, y + RH / 2 + 4, f'{b.usuarios.sum()/1e6:.1f}', 11, INK, 'end', 600)
S.t(K2, y + RH / 2 + 4, f'{100*b.otro.sum()/b.msgs.sum():.0f} %', 12, BLUE, 'end', 700)
S.t(K3 + 56, y + RH / 2 + 4, f'{b.costo.sum()/1e6:.1f}', 11, INK, 'end', 600)
print('alto', y + RH)
svg = S.done()

ning = a[a.nresp == 0].iloc[0]
save(18, dict(
    kind='grafica',
    titulo='Seis de cada diez mensajes van por un canal al que esa persona nunca ha respondido: el canal lo elige el equipo, no la persona',
    que='Sobre todo correo y push con promociones, a personas que responden por otro canal o por ninguno.',
    quien='Todos los equipos. Los datos de respuesta por persona no traen el equipo ni la campaña, así que no se puede repartir por equipo.',
    a_quien=f'{resp.usuarios.sum()/1e6:.1f} M personas responden por algún canal; {e_otro.usuarios.sum()/1e6:.1f} M de ellas nunca dieron clic en un correo. {ning.usuarios/1e6:.1f} M personas no respondieron por ninguno en nueve meses.',
    lecturas=[
        f'{a.otro.sum()/1e6:.0f} M de {M/1e6:.0f} M mensajes ({100*a.otro.sum()/M:.0f} %) fueron por un canal sin respuesta de esa persona, con {a.otro_costo.sum()/1e6:.1f} M MXN. De julio a septiembre ya es {100*b.otro.sum()/b.msgs.sum():.0f} %.',
        f'Quien solo lee WhatsApp ({100*sw.usuarios/a.usuarios.sum():.0f} % de las personas) recibió {sw.msgs_email/1e6:.0f} M correos y {sw.msgs_push/1e6:.0f} M push que nunca abrió, y se lleva {100*sw.costo/C:.0f} % del gasto.',
        f'Mandar a quien sí responde solo por su canal de los últimos 90 días quita {br.otro.sum()/1e6:.0f} M mensajes y {br.otro_costo.sum()/1e6:.1f} M MXN por trimestre.',
    ],
    causa='Braze no guarda por qué canal responde cada persona, así que nadie puede elegirlo: cada equipo manda por el canal que acostumbra.',
    sowhat='Guardar en Braze el canal al que cada persona respondió en 90 días y mandar por ese; elegir el canal por persona, no por equipo.',
    fuente='Fuente: Braze, mensajes y respuesta por persona, enero a septiembre 2026 y julio a septiembre 2026 (90 días). Responder = clic de correo o in-app, apertura de push, lectura de WhatsApp. Mensajes enviados, hayan llegado o no. Gasto: WhatsApp a 1.00 MXN por entregado, correo a 0.05 MXN por enviado.',
    svg=svg,
))
