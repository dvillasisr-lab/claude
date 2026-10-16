"""Lámina 1 de muestra (sección I, panorama): volumen, respuesta y gasto por mes.

Datos: braze-analysis/data/e1_comunicacion_mes_canal.csv, cargado con scratchpad/v6parts/p1/base.py
(mismas reglas que el guion v6: equipo, tema, costo con WhatsApp a 1.00 MXN por entregado y email a 0.05 por enviado).
Respuesta = clic email + apertura push + lectura WhatsApp + clic in-app, sobre mensajes enviados (columna envios).
Las lecturas de WhatsApp registradas el mes siguiente al envío cuentan (filas con envíos en 0 y lecturas > 0 se suman en su mes).
"""
import sys, json, math
sys.path.insert(0, '/tmp/claude-0/-home-user-claude/e114ba4f-39d4-57f8-9f24-b0f0c0cbef51/scratchpad/v6parts/p1')
from base import load, pd
OUT = '/tmp/claude-0/-home-user-claude/e114ba4f-39d4-57f8-9f24-b0f0c0cbef51/scratchpad/muestras/'

d = load()
d['respu'] = d.email_click + d.pn_open + d.whatsapp_read + d.in_app_click
g = d.groupby('m').agg(env=('envios', 'sum'), r=('respu', 'sum'), c=('costo', 'sum'))
g['rpm'] = 1000 * g.r / g.env
g['envM'] = g.env / 1e6
g['cM'] = g.c / 1e6

# Mezcla de canales contra respuesta de cada canal (descomposición simétrica enero contra septiembre)
c = d.groupby(['m', 'canal']).agg(env=('envios', 'sum'), r=('respu', 'sum'))
R = (c.r / c.env).unstack().fillna(0)
M = (c.env / c.groupby(level=0).env.transform('sum')).unstack().fillna(0)
f = lambda mm, rr: 1000 * (M.loc[mm] * R.loc[rr]).sum()
mix_eff = ((f(1, 1) - f(9, 1)) + (f(1, 9) - f(9, 9))) / 2
rate_eff = ((f(1, 1) - f(1, 9)) + (f(9, 1) - f(9, 9))) / 2
caida = g.rpm[1] - g.rpm[9]
share = lambda m, ch: 100 * M.loc[m, ch]
tasa = {ch: (100 * R.loc[1, ch], 100 * R.loc[9, ch]) for ch in R.columns}
# tasas por canal con la base de cada canal (como el guion: email clic/entregado, WA lectura/entregado)
RESP = {'email': ('email_delivery', 'email_click'), 'push notification': ('pn_send', 'pn_open'),
        'whatsapp': ('whatsapp_delivery', 'whatsapp_read'), 'in-app': ('in_app_impression', 'in_app_click')}
def tasa_canal(m, ch):
    x = d[(d.m == m) & (d.canal == ch)]; b, r = RESP[ch]
    return 100 * x[r].sum() / x[b].sum()

# Pico de junio contra enero: por equipo, por tema y BillPay
eq = (d[d.m == 6].groupby('equipo').envios.sum().sub(d[d.m == 1].groupby('equipo').envios.sum(), fill_value=0)) / 1e6
eqch = (d[d.m == 6].groupby(['equipo', 'canal']).envios.sum().sub(d[d.m == 1].groupby(['equipo', 'canal']).envios.sum(), fill_value=0)) / 1e6
gan = (d[d.m == 6].groupby('gan').envios.sum().sub(d[d.m == 1].groupby('gan').envios.sum(), fill_value=0)) / 1e6
gan6 = d[d.m == 6].groupby('gan').envios.sum() / 1e6
gan1 = d[d.m == 1].groupby('gan').envios.sum() / 1e6
bp = d[d.fam.str.contains('billpay', case=False)]
bp6 = bp[bp.m == 6].envios.sum() / 1e6
bp1 = bp[bp.m == 1].envios.sum() / 1e6
bpi = d[(d.m == 6) & d.fam.str.contains('BillPay_Intro_Full_Rollout') & (d.canal == 'email')]
bpi_env, bpi_users = bpi.envios.sum() / 1e6, bpi.usuarios_aprox.sum() / 1e6
bpi_clic = 100 * bpi.email_click.sum() / bpi.email_delivery.sum()
fam = lambda pat, ch: d[(d.m == 6) & d.fam.str.contains(pat) & (d.canal == ch)].envios.sum() / 1e6 - d[(d.m == 1) & d.fam.str.contains(pat) & (d.canal == ch)].envios.sum() / 1e6
mundial, padre, comercio, anota = fam('BAUMundial', 'push notification'), fam('DiaPadres', 'push notification'), fam('Comerciodeldia', 'push notification'), fam('AnotayGana', 'push notification')
delta_tot = g.envM[6] - g.envM[1]
e3 = pd.read_csv('/home/user/claude/braze-analysis/data/e3_usuarios_distribucion.csv')
personas = e3[e3.msgs > 0].usuarios.sum() / 1e6   # personas con al menos un mensaje en nueve meses

K = dict(
    ene_env=g.envM[1], ene_rpm=g.rpm[1], ene_c=g.cM[1],
    mar_env=g.envM[3], mar_rpm=g.rpm[3], mar_c=g.cM[3],
    jun_env=g.envM[6], jun_rpm=g.rpm[6], jun_c=g.cM[6],
    sep_env=g.envM[9], sep_rpm=g.rpm[9], sep_c=g.cM[9],
    sep_vs_ene_vol=100 * (g.envM[9] / g.envM[1] - 1), sep_vs_ene_rpm=100 * (1 - g.rpm[9] / g.rpm[1]),
    jun_sep_baja=g.envM[6] - g.envM[9],
    mix_eff=mix_eff, rate_eff=rate_eff, caida=caida, mix_pct=100 * mix_eff / caida,
    wa_sh=(share(1, 'whatsapp'), share(9, 'whatsapp')), push_sh=(share(1, 'push notification'), share(9, 'push notification')),
    email_t=(tasa_canal(1, 'email'), tasa_canal(9, 'email')), wa_t=(tasa_canal(1, 'whatsapp'), tasa_canal(9, 'whatsapp')),
    push_t=(tasa_canal(1, 'push notification'), tasa_canal(9, 'push notification')), inapp_t=(tasa_canal(1, 'in-app'), tasa_canal(9, 'in-app')),
    delta_tot=delta_tot, eq=eq.round(2).to_dict(), mkt_push=eqch.loc[('Marketing', 'push notification')],
    oth_email=eqch.loc[('Others', 'email')], gan=gan.round(2).to_dict(), lanz=(gan1['lanzamiento'], gan6['lanzamiento']),
    bp6=bp6, bp1=bp1, bpi=(bpi_env, bpi_users, bpi_clic), mundial=mundial, padre=padre, comercio=comercio, anota=anota,
)
for k, v in K.items(): print(k, v)
print(g.round(2))

# ---------------- SVG ----------------
W, H = 780, 420
X0, X1, Y0, Y1 = 66, 756, 46, 362           # área de trazo
XD, YD = (50, 115), (40, 110)
XT, YT = [50, 60, 70, 80, 90, 100, 110], [40, 50, 60, 70, 80, 90, 100, 110]
sx = lambda v: X0 + (v - XD[0]) / (XD[1] - XD[0]) * (X1 - X0)
sy = lambda v: Y1 - (v - YD[0]) / (YD[1] - YD[0]) * (Y1 - Y0)
INK, TXT, SEC, MARK, GRID, BLUE, BLUE_L = '#0B1220', '#3B4556', '#6B7484', '#A3AAB5', '#DDE2EA', '#1F4FD8', '#8FA8EE'
FONT = 'Inter, system-ui, sans-serif'
rad = lambda cm: 2.45 * math.sqrt(cm)        # área del punto proporcional al gasto; 4.2 M MXN da r=5 (10 px)
MES = ['', 'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep']
MESL = ['', 'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre']
fm = lambda v: f'{v:.1f}'
# etiqueta: (dx, dy, anchor, con gasto)
LAB = {1: (0, -14, 'middle', True), 2: (12, 4, 'start', False), 3: (13, 5, 'start', True), 4: (-11, -4, 'end', False),
       5: (0, -13, 'middle', False), 6: (0, -15, 'middle', True), 7: (0, -13, 'middle', False), 8: (11, 14, 'start', False),
       9: (-12, 14, 'end', True)}
HL = {6, 9}

s = []
a = s.append
a(f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" xmlns="http://www.w3.org/2000/svg" font-family="{FONT}" '
  f'aria-label="Dispersión conectada por mes, enero a septiembre 2026: mensajes enviados contra respuestas por cada mil mensajes; '
  f'el tamaño del punto es el gasto del mes. Enero {fm(K["ene_env"])} M mensajes y {K["ene_rpm"]:.0f} respuestas por mil; '
  f'junio {fm(K["jun_env"])} M y {K["jun_rpm"]:.0f}; septiembre {fm(K["sep_env"])} M y {K["sep_rpm"]:.0f}.">')
a(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#FFFFFF"/>')
# rejilla y ticks
for v in YT:
    a(f'<line x1="{X0}" x2="{X1}" y1="{sy(v):.1f}" y2="{sy(v):.1f}" stroke="{GRID}" stroke-width="1"/>')
    a(f'<text x="{X0-8}" y="{sy(v)+4:.1f}" text-anchor="end" font-size="11.5" fill="{SEC}">{v}</text>')
for v in XT:
    a(f'<line x1="{sx(v):.1f}" x2="{sx(v):.1f}" y1="{Y1}" y2="{Y1+4}" stroke="{MARK}" stroke-width="1"/>')
    a(f'<text x="{sx(v):.1f}" y="{Y1+18}" text-anchor="middle" font-size="11.5" fill="{SEC}">{v}</text>')
a(f'<line x1="{X0}" x2="{X1}" y1="{Y1}" y2="{Y1}" stroke="{MARK}" stroke-width="1"/>')
a(f'<text x="{X0-8}" y="20" font-size="11.5" fill="{TXT}" font-weight="600">Respuestas por cada mil mensajes</text>')
a(f'<text x="{X1}" y="{Y1+40}" text-anchor="end" font-size="11.5" fill="{TXT}" font-weight="600">Mensajes enviados en el mes (millones)</text>')
# referencia: nivel de enero
yr = sy(K['ene_rpm'])
a(f'<line x1="{X0}" x2="{X1}" y1="{yr:.1f}" y2="{yr:.1f}" stroke="{SEC}" stroke-width="1"/>')
a(f'<text x="{X1}" y="{yr-6:.1f}" text-anchor="end" font-size="12" fill="{TXT}">Nivel de enero: {K["ene_rpm"]:.0f} respuestas por mil</text>')
# trayectoria
pts = {m: (sx(g.envM[m]), sy(g.rpm[m])) for m in range(1, 10)}
p1 = ' '.join(f'{pts[m][0]:.1f},{pts[m][1]:.1f}' for m in range(1, 7))
p2 = ' '.join(f'{pts[m][0]:.1f},{pts[m][1]:.1f}' for m in range(6, 10))
a(f'<polyline points="{p1}" fill="none" stroke="{MARK}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')
a(f'<polyline points="{p2}" fill="none" stroke="{BLUE_L}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')
# puntos
for m in range(1, 10):
    x, y = pts[m]; col = BLUE if m in HL else MARK
    a(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad(g.cM[m]):.1f}" fill="{col}" stroke="#FFFFFF" stroke-width="2">'
      f'<title>{MESL[m].capitalize()}: {fm(g.envM[m])} M mensajes, {g.rpm[m]:.0f} respuestas por mil, gasto {fm(g.cM[m])} M MXN</title></circle>')
# etiquetas
for m in range(1, 10):
    x, y = pts[m]; dx, dy, anc, cost = LAB[m]
    w = '600' if (m in HL or m == 1) else '400'
    col = INK if (m in HL or m == 1) else TXT
    t = f'<tspan font-weight="{w}" fill="{col}">{MES[m]}</tspan>'
    if cost:
        t += f'<tspan fill="{SEC}"> · {fm(g.cM[m])} M MXN</tspan>'
    a(f'<text x="{x+dx:.1f}" y="{y+dy:.1f}" text-anchor="{anc}" font-size="13">{t}</text>')
# anotación de la trayectoria de junio a septiembre
ax, ay = sx(84), sy(47.3)
a(f'<text x="{ax:.1f}" y="{ay:.1f}" font-size="12" fill="{TXT}">'
  f'<tspan x="{ax:.1f}">De junio a septiembre mandamos {K["jun_sep_baja"]:.0f} M mensajes menos</tspan>'
  f'<tspan x="{ax:.1f}" dy="16">y la respuesta no volvió: {K["jun_rpm"]:.0f}, {g.rpm[7]:.0f}, {g.rpm[8]:.0f} y {K["sep_rpm"]:.0f} por mil.</tspan></text>')
# clave de tamaño
kx, ky = 540, 30
a(f'<text x="{kx}" y="{ky-10}" font-size="11.5" fill="{TXT}" font-weight="600">Tamaño del punto: gasto del mes en MXN</text>')
for i, v in enumerate([4, 6, 9]):
    cx = kx + 8 + i * 58
    a(f'<circle cx="{cx}" cy="{ky+8}" r="{rad(v):.1f}" fill="none" stroke="{MARK}" stroke-width="1.5"/>')
    a(f'<text x="{cx+rad(v)+5:.1f}" y="{ky+12}" font-size="11.5" fill="{SEC}">{v} M</text>')
a('</svg>')
svg = ''.join(s)

J = {
    "seccion": "Una operación grande que nos responde cada vez menos",
    "titulo": "Desde junio mandamos menos, pero cada mensaje rinde un tercio menos que en enero",
    "que": (f"Los masivos de junio: el lanzamiento de BillPay (pago de servicios) con sus recordatorios, {bp6:.0f} M mensajes "
            f"(un solo email de BillPay fue a {bpi_users:.1f} M personas con {bpi_clic:.2f} % de clic); push promocionales nuevos de "
            f"Mundial, Día del Padre y Comercio del día, y AnotayGana (referidos). Los lanzamientos pasaron de {gan1['lanzamiento']:.1f} M en enero a {gan6['lanzamiento']:.0f} M en junio."),
    "quien": (f"De los {delta_tot:.0f} M mensajes de más en junio contra enero, Marketing sumó {eq['Marketing']:.0f} M "
              f"({K['mkt_push']:.0f} M en push) y Others {eq['Others']:.0f} M (BillPay, {K['oth_email']:.0f} M en email); Collections {eq['Collections']:.0f} M. "
              f"Product Growth mandó {abs(eq['Product Growth']):.0f} M menos y Sales {abs(eq['Sales']):.0f} M menos."),
    "a_quien": (f"A casi toda la base: el email de BillPay llegó a {bpi_users:.0f} M de las {personas:.1f} M personas que recibieron algo en nueve meses; "
                f"varios push de junio tenían 'Todos' como audiencia."),
    "lecturas": [
        f"Septiembre mandó {fm(K['sep_env'])} M mensajes, {K['sep_vs_ene_vol']:.0f} % más que enero ({fm(K['ene_env'])} M), y cada mil trajeron "
        f"{K['sep_rpm']:.0f} respuestas contra {K['ene_rpm']:.0f}. Con casi el mismo volumen, cada mensaje rinde {K['sep_vs_ene_rpm']:.0f} % menos.",
        f"Junio fue el pico: {K['jun_env']:.0f} M mensajes y {fm(K['jun_c'])} M MXN de gasto, con {K['jun_rpm']:.0f} respuestas por mil. "
        f"Al bajar {K['jun_sep_baja']:.0f} M mensajes hacia septiembre la respuesta no regresó: siguió en {g.rpm[7]:.0f}, {g.rpm[8]:.0f} y {K['sep_rpm']:.0f}.",
        f"Dos tercios de la caída vienen de la mezcla: WhatsApp, el que más se lee, bajó de {K['wa_sh'][0]:.1f} % a {K['wa_sh'][1]:.1f} % "
        f"de los mensajes y push, que casi nadie abre, subió de {K['push_sh'][0]:.0f} % a {K['push_sh'][1]:.0f} %. El otro tercio: email, WhatsApp "
        f"e in-app responden menos (lectura de WhatsApp {K['wa_t'][0]:.0f} % a {K['wa_t'][1]:.0f} %).",
    ],
    "causa": ("Sumamos volumen con push y email masivos a toda la base, que casi no se responden, "
              "y no hay tope por persona ni calendario común que frene el desgaste."),
    "sowhat": ("Bajar volumen no basta para recuperar la respuesta: hay que elegir a quién le escribimos, por el canal al que responde, "
               "y poner tope y calendario a los masivos."),
    "fuente": ("Fuente: Braze, envíos por comunicación, mes y canal, enero a septiembre 2026. Respuesta = clic de email, apertura de push, "
               "lectura de WhatsApp (incluye lecturas registradas el mes siguiente) y clic in-app, por cada mil mensajes enviados; "
               "WhatsApp a 1.00 MXN por entregado, email a 0.05 por enviado."),
    "svg": svg,
}
json.dump(J, open(OUT + 's1.json', 'w'), ensure_ascii=False, indent=1)
open(OUT + 's1.svg', 'w').write(svg)
print(json.dumps({k: v for k, v in J.items() if k != 'svg'}, ensure_ascii=False, indent=1))
