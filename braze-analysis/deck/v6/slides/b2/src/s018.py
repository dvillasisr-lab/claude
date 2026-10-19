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
a = a.sort_values('msgs', ascending=False).reset_index(drop=True)
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

S = Svg('Mancuernas por patrón de respuesta de la persona: mensajes por un canal al que responde contra mensajes totales; '
        'la distancia son mensajes por un canal al que nunca respondió.')
S.circle(5, 14, 5.5, GREEN, ''); S.t(15, 18, 'Mensajes por un canal al que esa persona sí responde', 11.5, INK, w=600)
S.circle(345, 14, 5.5, BLUE, ''); S.t(355, 18, 'Total de mensajes', 11.5, INK, w=600)
S.rect(490, 9, 24, 10, '#C7D4F6'); S.t(520, 18, 'Por un canal sin respuesta', 11.5, TXT)
S.t(0, 36, 'Una fila por patrón: por qué canales respondió la persona alguna vez (clic, apertura o lectura), enero a septiembre.', 10.5, SEC)
LX, X0, X1 = 186, 196, 590
VM = 170
sx = lambda v: X0 + (X1 - X0) * v / VM
Y0, RH = 64, 18.6
rows = a.copy()
rows['ok'] = rows.msgs - rows.otro
YB = Y0 + RH * len(rows)
for v in range(0, 171, 40):
    S.line(sx(v), Y0 - 4, sx(v), YB, GRID)
    S.t(sx(v), YB + 14, f'{v} M', 10.5, SEC, 'middle')
S.t(X1, YB + 30, 'Millones de mensajes en nueve meses', 10.5, SEC, 'end')
K1, K2 = 668, 778
S.t(K1, Y0 - 8, 'Personas', 10.5, SEC, 'end')
S.t(K2, Y0 - 20, 'Por canal', 10.5, SEC, 'end')
S.t(K2, Y0 - 8, 'sin respuesta', 10.5, SEC, 'end')
for i, r in enumerate(rows.itertuples()):
    y = Y0 + RH * i + RH / 2
    big = r.lab in ('Ningún canal', 'Solo WhatsApp')
    S.t(LX, y + 4, r.lab, 10.5, INK if big else TXT, 'end', 600 if big else 400)
    S.rect(sx(r.ok / 1e6), y - 4, sx(r.msgs / 1e6) - sx(r.ok / 1e6), 8, '#C7D4F6')
    S.circle(sx(r.ok / 1e6), y, 4.5, GREEN, ' stroke="#FFFFFF" stroke-width="1.2"')
    S.circle(sx(r.msgs / 1e6), y, 4.5, BLUE, ' stroke="#FFFFFF" stroke-width="1.2"')
    if r.msgs / 1e6 >= 25:
        S.t(sx(r.msgs / 1e6) + 8, y + 4, f'{r.msgs/1e6:.0f} M', 10.5, INK, 'start', 600 if big else 400)
    S.t(K1, y + 4, f'{r.usuarios/1e6:.2f} M' if r.usuarios >= 1e5 else f'{r.usuarios/1e3:.0f} mil', 10.5, TXT, 'end')
    S.t(K2, y + 4, f'{100*r.otro/r.msgs:.0f} %', 10.5, BLUE if r.otro / r.msgs >= 0.5 else TXT, 'end', 700 if big else 400)
S.t(0, YB + 46, f'Total: {a.otro.sum()/1e6:.0f} M de {M/1e6:.0f} M mensajes ({100*a.otro.sum()/M:.0f} %) por un canal sin respuesta de esa persona; '
    f'julio a septiembre: {100*b.otro.sum()/b.msgs.sum():.0f} %.', 11.5, BLUE, 'start', 700)
print('alto', YB + 46)
svg = S.done()

ning = a[a.nresp == 0].iloc[0]
save(18, dict(
    kind='grafica',
    titulo='Seis de cada diez mensajes van por un canal al que esa persona nunca ha respondido',
    que='Sobre todo correo y push con promociones.',
    quien='Todos los equipos; el dato por persona no trae equipo ni campaña.',
    a_quien=f'{resp.usuarios.sum()/1e6:.1f} M personas que responden por algún canal y {ning.usuarios/1e6:.1f} M que no responden por ninguno.',
    lecturas=[
        f'{a.otro.sum()/1e6:.0f} M de {M/1e6:.0f} M mensajes ({100*a.otro.sum()/M:.0f} %) por un canal sin respuesta: {a.otro_costo.sum()/1e6:.1f} M MXN.',
        f'Quien solo lee WhatsApp recibió {sw.msgs_email/1e6:.0f} M correos y {sw.msgs_push/1e6:.0f} M push que nunca abrió.',
        f'Mandar solo por el canal de los últimos 90 días quita {br.otro.sum()/1e6:.0f} M mensajes y {br.otro_costo.sum()/1e6:.1f} M MXN por trimestre.',
    ],
    causa='Braze no guarda por qué canal responde cada persona, así que cada equipo manda por el canal que acostumbra.',
    sowhat='Guardar en Braze el canal al que cada persona respondió en 90 días y mandar por ese.',
    fuente='Fuente: Braze, mensajes y respuesta por persona, enero a septiembre y julio a septiembre 2026. Mensajes enviados; WhatsApp a 1.00 MXN por entregado.',
    svg=svg,
))
