# Lámina 2 (Diagnóstico): equipo x audiencia x respuesta x volumen.
# Recalcula desde E1 con la misma lógica de v6parts/p2work (base.py, t2.py, t5.py) y escribe s2.json.
import sys, json, math
sys.path.insert(0, '/tmp/claude-0/-home-user-claude/e114ba4f-39d4-57f8-9f24-b0f0c0cbef51/scratchpad/v6parts/p2work')
from base import *  # load, agg, MIN, pd, np

OUT = '/tmp/claude-0/-home-user-claude/e114ba4f-39d4-57f8-9f24-b0f0c0cbef51/scratchpad/muestras/'

# ---------- datos (t2 + t5) ----------
e1, c = load()
x = e1[e1.canal != 'banner']
f = agg(x, ['equipo', 'familia', 'canal', 'tema', 'seg'])
f['vs_min'] = f.resp_pct / f.canal.map(MIN)
f = f[(f.base >= 50000) & f.canal.isin(MIN.keys())].copy()
REC = {'Leads en registro', 'Clientes activos y recurrentes', 'Cartera en cobranza', 'Evento (transaccional)', 'Leads recientes'}
f['con'] = f.seg.isin(REC)
f['pasa'] = f.vs_min >= 1

def pct_pasa(d): return 100 * d[d.pasa].env.sum() / d.env.sum() if d.env.sum() else float('nan')

TOT_ENV = f.env.sum()
TOT_CON = pct_pasa(f[f.con]); TOT_SIN = pct_pasa(f[~f.con])
SIN_ENV = f[~f.con].env.sum()

# Nombres limpios de las campañas que se etiquetan (clave = familia, canal)
NOMBRE = {
 'KCash-B0211-Nuevos_RegistradosPay-Tasa0': 'Tasa 0 a registrados sin crédito',
 'KCash-B0301-Active-Retargeting_Installments_SP': 'Installments a activos',
 'KCash-B0171-Anonimos-RescateTasa0': 'Rescate Tasa 0 a anónimos',
 'KCash-B0000-Leads_LeftFunnel-Retargeting_Veriff': 'Recordatorio de Veriff',
 'Kueski-T0000-E-Portfolio_BillPay_Intro_Full_Rollout': 'Lanzamiento BillPay a todos',
 'Transaccional-KPay-Mail-Payment-Confirmation-20240821': 'Confirmación de pago KPay',
 'KPay-B0335-Recurrentes_PortafolioActivoEInactivo-PromocionesMe': 'Promos a todo el portafolio',
 'KPay-B0493-Recurrentes-HotSaleKUESKIPROMOEnterprise': 'Hot Sale a recurrentes',
 'KCash-T000-BKT3-NA': 'Cobranza BKT3, atraso mayor',
 'KCash-T000-BKT1-NA': 'Cobranza BKT1',
}
CANAL = {'email': ('email', 'clic'), 'push notification': ('push', 'apertura'), 'whatsapp': ('WhatsApp', 'lectura'), 'in-app': ('in-app', 'clic')}
def short_key(fam):
    for k in NOMBRE:
        if fam.startswith(k) or fam.replace('-CANVAS-', '-').replace('-N/A', '').find(k.split('-', 1)[1][:30]) >= 0:
            return k
    return None

def fmt(v, d=1): return f'{v:.{d}f}'
def pct_txt(v): return f'{v:.2f}'.rstrip('0').rstrip('.') if v < 10 else f'{v:.1f}'

rows = []
for t, d in f.groupby('equipo'):
    con, sin = d[d.con], d[~d.con]
    worst = d[~d.pasa].sort_values('env', ascending=False).iloc[0]           # más volumen debajo del piso
    best = con[con.pasa].sort_values('env', ascending=False).iloc[0]          # más volumen arriba del piso, con acción reciente
    def lab(r):
        k = short_key(r.familia)
        ch, m = CANAL[r.canal]
        return dict(nombre=NOMBRE.get(k, r.familia), familia=r.familia, canal=r.canal, con=bool(r.con),
                    linea=f'{ch} {fmt(r.env/1e6)} M · {r.resp_pct:.2f} % {m}', env=r.env, resp=r.resp_pct)
    rows.append(dict(equipo=t, env=d.env.sum(), env_con=con.env.sum(), env_sin=sin.env.sum(),
                     share_sin=100 * sin.env.sum() / d.env.sum(), pasa_con=pct_pasa(con), pasa_sin=pct_pasa(sin),
                     prob=sin[~sin.pasa].env.sum(), falla=lab(worst), acierta=lab(best)))
rows.sort(key=lambda r: -r['prob'])   # tamaño del problema: volumen sin acción reciente debajo del piso
for r in rows:
    print(f"{r['equipo']:15s} env {r['env']/1e6:6.1f} M  sin {r['share_sin']:5.1f}%  pasa con {r['pasa_con']:5.1f}  sin {r['pasa_sin']:5.1f}  problema {r['prob']/1e6:5.1f} M")
    print('   falla  ', r['falla']['nombre'], '|', r['falla']['linea'], '| con' if r['falla']['con'] else '| sin')
    print('   acierta', r['acierta']['nombre'], '|', r['acierta']['linea'])
print(f'Total {TOT_ENV/1e6:.1f} M; con acción pasa {TOT_CON:.1f} %, sin {TOT_SIN:.1f} %; sin acción {SIN_ENV/1e6:.1f} M')

# ---------- SVG ----------
INK, TXT, SEC, MRK, GRID = '#0B1220', '#3B4556', '#6B7484', '#A3AAB5', '#DDE2EA'
BLUE, GREEN = '#1F4FD8', '#127A5B'
FF = 'Inter, system-ui, sans-serif'
W, H = 780, 420
X0, X1 = 168, 378            # eje 0 a 100 %
CF, CA = 396, 602            # columnas de etiquetas
TOP, ROWH = 62, 60
MAXENV = max(max(r['env_con'], r['env_sin']) for r in rows)
RMAX, RMIN = 13.0, 4.0
def xp(v): return X0 + (X1 - X0) * v / 100
def rad(env): return max(RMIN, RMAX * math.sqrt(env / MAXENV))
def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;')
def T(x, y, s, size=12, fill=TXT, w=400, anchor='start'):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" font-weight="{w}" text-anchor="{anchor}">{esc(s)}</text>'

o = []
o.append(f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" font-family="{FF}" xmlns="http://www.w3.org/2000/svg" '
         f'aria-label="Por equipo, parte del volumen que pasa el piso de respuesta cuando va a gente con acción reciente y cuando va a gente sin acción reciente. '
         f'En total {TOT_CON:.0f} % contra {TOT_SIN:.0f} %. Product Growth manda {rows[0]["share_sin"]:.0f} % de su volumen a gente sin acción reciente y ahí pasa {rows[0]["pasa_sin"]:.0f} %.">')
o.append(f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>')
# encabezados de columna
o.append(T(0, 14, 'Equipo y volumen', 11.5, SEC, 600))
o.append(T(X0, 14, '% del volumen que pasa el piso', 11.5, SEC, 600))
o.append(T(CF, 14, 'Más volumen debajo del piso', 11.5, SEC, 600))
o.append(T(CA, 14, 'Más volumen arriba del piso', 11.5, SEC, 600))
# claves de color (etiqueta directa de las dos series)
ky = 34
o.append(f'<circle cx="{X0+5}" cy="{ky-4}" r="5" fill="{GREEN}"/>' + T(X0 + 14, ky, 'con acción reciente', 12, TXT))
o.append(f'<circle cx="{X0+148}" cy="{ky-4}" r="5" fill="{BLUE}"/>' + T(X0 + 157, ky, 'sin acción reciente', 12, TXT))
o.append(f'<line x1="0" y1="44" x2="{W}" y2="44" stroke="{GRID}" stroke-width="1"/>')
# rejilla vertical
yb = TOP + ROWH * len(rows) - 14
for v in (0, 25, 50, 75, 100):
    o.append(f'<line x1="{xp(v):.1f}" y1="48" x2="{xp(v):.1f}" y2="{yb:.1f}" stroke="{GRID}" stroke-width="1"/>')
    o.append(T(xp(v), yb + 14, f'{v} %', 11.5, SEC, 400, 'middle'))

for i, r in enumerate(rows):
    yc = TOP + ROWH * i + 14            # centro de la fila (puntos)
    # columna equipo
    o.append(T(0, yc - 8, r['equipo'], 13, INK, 600))
    bw = 120; bs = bw * r['share_sin'] / 100
    if bs >= 1:
        o.append(f'<rect x="0" y="{yc-1}" width="{bs:.1f}" height="6" fill="{BLUE}"/>')
    o.append(f'<rect x="{bs + (2 if bs >= 1 else 0):.1f}" y="{yc-1}" width="{bw - bs - (2 if bs >= 1 else 0):.1f}" height="6" fill="{GREEN}"/>')
    sh = r['share_sin']
    sh_txt = f'{sh:.0f} %' if sh >= 1 else f'{sh:.1f} %'
    o.append(T(0, yc + 20, f'{r["env"]/1e6:.0f} M; {sh_txt} sin acción', 11.5, SEC))
    # pesas
    pts = [('con', r['pasa_con'], r['env_con'], GREEN)]
    if r['share_sin'] >= 1:
        pts.append(('sin', r['pasa_sin'], r['env_sin'], BLUE))
        o.append(f'<line x1="{xp(r["pasa_sin"]):.1f}" y1="{yc}" x2="{xp(r["pasa_con"]):.1f}" y2="{yc}" stroke="{MRK}" stroke-width="2"/>')
    for g, v, env, col in sorted(pts, key=lambda p: -p[2]):
        rr = rad(env)
        o.append(f'<circle cx="{xp(v):.1f}" cy="{yc}" r="{rr:.1f}" fill="{col}" stroke="#FFFFFF" stroke-width="2"/>')
    for g, v, env, col in pts:
        rr = rad(env)
        o.append(T(xp(v), yc - rr - 5, f'{v:.0f} %', 12, INK, 600, 'middle'))
    # etiquetas de campaña
    for cx, k in ((CF, 'falla'), (CA, 'acierta')):
        L = r[k]
        col = GREEN if L['con'] else BLUE
        o.append(f'<circle cx="{cx+4}" cy="{yc-12}" r="4" fill="{col}"/>')
        o.append(T(cx + 13, yc - 8, L['nombre'], 12, INK, 500))
        o.append(T(cx + 13, yc + 8, L['linea'], 11.5, SEC))
    if i < len(rows) - 1:
        o.append(f'<line x1="0" y1="{yc+ROWH-28}" x2="120" y2="{yc+ROWH-28}" stroke="{GRID}" stroke-width="1"/>')
        o.append(f'<line x1="{CF}" y1="{yc+ROWH-28}" x2="{W}" y2="{yc+ROWH-28}" stroke="{GRID}" stroke-width="1"/>')

# nota al pie
fy = yb + 36
o.append(f'<line x1="0" y1="{fy-14}" x2="{W}" y2="{fy-14}" stroke="{GRID}" stroke-width="1"/>')
o.append(T(0, fy, 'Piso de respuesta por canal: email 0.3 % de clic, push 0.75 % de apertura, WhatsApp 60 % de lectura, in-app 10 % de clic.', 11.5, SEC))
o.append(T(0, fy + 16, f'Pasa: campaña y canal arriba del piso en los nueve meses. Tamaño del punto = envíos del grupo (el mayor, {MAXENV/1e6:.0f} M).', 11.5, SEC))
o.append('</svg>')
svg = ''.join(o)

# ---------- texto ----------
R = {r['equipo']: r for r in rows}
pg, mk, ot, sa, co = (R[k] for k in ['Product Growth', 'Marketing', 'Others', 'Sales', 'Collections'])
mk_wa = f[(f.equipo == 'Marketing') & ~f.con & (f.canal == 'whatsapp')]
mk_em_push = f[(f.equipo == 'Marketing') & ~f.con & f.canal.isin(['email', 'push notification'])]
pg_sin_email = f[(f.equipo == 'Product Growth') & ~f.con & (f.canal == 'email')]
print('MK sin WA pasa', pct_pasa(mk_wa), 'email+push', pct_pasa(mk_em_push), '; PG sin email', pg_sin_email.env.sum()/1e6, pct_pasa(pg_sin_email))

J = {
 'seccion': 'Diagnóstico',
 'titulo': f'Los equipos aciertan con quien acaba de actuar y chocan en las bases frías, donde solo {TOT_SIN:.0f} % del volumen pasa el piso',
 'que': f'Ofertas (Tasa 0, Installments, referidos, promos KPay, BillPay), recordatorios, cobranza y avisos: {TOT_ENV/1e6:.0f} M envíos de campañas con 50 mil o más entregados.',
 'quien': 'Los cinco equipos: Product Growth, Marketing, Sales, Collections y Others.',
 'a_quien': 'Con acción reciente: registro a medias, clientes activos, pago por vencer o aviso de algo que hizo. Sin acción: leads fríos, registrados sin crédito, inactivos, churn y masivos a todos.',
 'lecturas': [
   f'Product Growth manda {pg["share_sin"]:.0f} % de su volumen ({pg["env_sin"]/1e6:.0f} M) a gente sin acción reciente y ahí solo pasa el piso {pg["pasa_sin"]:.0f} %; con quien ya empezó algo, {pg["pasa_con"]:.0f} %. '
   f'El mayor golpe: {pg["falla"]["nombre"]}, {pg["falla"]["env"]/1e6:.1f} M correos a {pg["falla"]["resp"]:.2f} % de clic.',
   f'Marketing manda {mk["share_sin"]:.0f} % ({mk["env_sin"]/1e6:.0f} M) sin acción reciente y pasa {mk["pasa_sin"]:.0f} % gracias al WhatsApp, que se lee: ahí pasa {pct_pasa(mk_wa):.0f} %, '
   f'contra {pct_pasa(mk_em_push):.0f} % en email y push. Su recordatorio de Veriff a quien dejó el registro a medias da {mk["acierta"]["resp"]:.2f} % de clic.',
   f'Others y Sales repiten el patrón: con acción reciente pasan {ot["pasa_con"]:.0f} % y {sa["pasa_con"]:.0f} %, sin ella {ot["pasa_sin"]:.0f} % y {sa["pasa_sin"]:.0f} % '
   f'(BillPay a todos, {ot["falla"]["env"]/1e6:.1f} M correos a {ot["falla"]["resp"]:.2f} %). Collections casi no escribe a bases frías; lo que le falla es la cobranza BKT3.',
 ],
 'causa': 'Las campañas se arman por producto y se mandan a bases enteras, no a partir de algo que la persona acaba de hacer: quien empezó algo espera el mensaje, quien lleva meses sin actuar lo ignora.',
 'sowhat': f'Recortar los {pg["prob"]/1e6:.0f} M de Product Growth y los {mk["prob"]/1e6:.0f} M de Marketing que van a bases frías y no pasan el piso, y pasar ese esfuerzo a disparadores por acción reciente.',
 'fuente': f'Fuente: Braze, E1 por campaña, mes y canal, enero a septiembre de 2026; {TOT_ENV/1e6:.0f} M envíos de campañas con 50 mil o más entregados; audiencia según el nombre de la campaña; lecturas de WhatsApp del mes siguiente incluidas; WhatsApp a 1.00 MXN por entregado, email a 0.05 por enviado.',
 'svg': svg,
}
json.dump(J, open(OUT + 's2.json', 'w'), ensure_ascii=False, indent=1)
open(OUT + 's2.svg', 'w').write(svg)
print(json.dumps({k: v for k, v in J.items() if k != 'svg'}, ensure_ascii=False, indent=1))
