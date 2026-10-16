"""Lámina 2 v2: por equipo, millones de mensajes partidos en cuatro: a quién se le escribe (hizo algo hace poco o no) y si responde
lo mínimo aceptable. Misma lógica que s2.py (base_p2: E1, campañas con 50 mil o más entregados). Actualiza s2.json."""
import json, pathlib, sys
H = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(H))
from base_p2 import load, agg, MIN
e1, c = load()
x = e1[e1.canal != 'banner']
f = agg(x, ['equipo', 'familia', 'canal', 'tema', 'seg'])
f['vs_min'] = f.resp_pct / f.canal.map(MIN)
f = f[(f.base >= 50000) & f.canal.isin(MIN.keys())].copy()
REC = {'Leads en registro', 'Clientes activos y recurrentes', 'Cartera en cobranza', 'Evento (transaccional)', 'Leads recientes'}
f['con'] = f.seg.isin(REC); f['pasa'] = f.vs_min >= 1
NOMBRE = {'KCash-B0211-Nuevos_RegistradosPay-Tasa0': 'Tasa 0 a registrados sin crédito', 'KCash-B0301-Active-Retargeting_Installments_SP': 'Meses sin intereses a clientes activos',
 'KCash-B0171-Anonimos-RescateTasa0': 'Rescate Tasa 0 a anónimos', 'KCash-B0000-Leads_LeftFunnel-Retargeting_Veriff': 'Recordatorio de terminar registro (Veriff)',
 'Kueski-T0000-E-Portfolio_BillPay_Intro_Full_Rollout': 'Lanzamiento de BillPay a todos', 'Transaccional-KPay-Mail-Payment-Confirmation-20240821': 'Confirmación de pago KPay',
 'KPay-B0335-Recurrentes_PortafolioActivoEInactivo-PromocionesMe': 'Promos KPay a todo el portafolio', 'KPay-B0493-Recurrentes-HotSaleKUESKIPROMOEnterprise': 'Hot Sale a clientes recurrentes',
 'KCash-T000-BKT3-NA': 'Cobranza con atraso mayor (BKT3)', 'KCash-T000-BKT1-NA': 'Cobranza con atraso menor (BKT1)'}
CAN = {'email': ('email', 'clic'), 'push notification': ('push', 'apertura'), 'whatsapp': ('WhatsApp', 'lectura'), 'in-app': ('in-app', 'clic')}
def nombre(fam):
    for k, v in NOMBRE.items():
        if fam.startswith(k) or fam.replace('-CANVAS-', '-').replace('-N/A', '').find(k.split('-', 1)[1][:30]) >= 0: return v
    return fam
def lab(r):
    ch, m = CAN[r.canal]; return nombre(r.familia), f'{ch} · {r.env/1e6:.1f} M mensajes · {r.resp_pct:.2f} % de {m}'
rows = []
for t, d in f.groupby('equipo'):
    seg = dict(sin_no=d[~d.con & ~d.pasa].env.sum(), sin_si=d[~d.con & d.pasa].env.sum(), con_no=d[d.con & ~d.pasa].env.sum(), con_si=d[d.con & d.pasa].env.sum())
    w = d[~d.pasa].sort_values('env', ascending=False).iloc[0]; b = d[d.con & d.pasa].sort_values('env', ascending=False).iloc[0]
    rows.append(dict(equipo=t, tot=d.env.sum(), falla=lab(w), acierta=lab(b), **seg))
rows.sort(key=lambda r: -r['sin_no'])
INK, TXT, SEC, GRID, BLUE, BLUEL, GREEN, GREENL = '#0B1220', '#3B4556', '#6B7484', '#DDE2EA', '#1F4FD8', '#8FA8EE', '#127A5B', '#7CC4A8'
SEGS = [('sin_no', BLUE, 'No ha hecho nada reciente y no responde'), ('sin_si', BLUEL, 'No ha hecho nada reciente y sí responde'),
        ('con_no', GREENL, 'Hizo algo hace poco y no responde'), ('con_si', GREEN, 'Hizo algo hace poco y sí responde')]
FF = 'Inter, system-ui, sans-serif'; W, Hh = 780, 420
X0, X1 = 112, 420; VMAX = 260
xs = lambda v: X0 + (X1 - X0) * (v / 1e6) / VMAX
TOP, RH, BH = 106, 54, 20; CX = 444
o = [f'<svg viewBox="0 0 {W} {Hh}" width="100%" role="img" aria-label="Mensajes de cada equipo según a quién se escribe y si responde, con la campaña que más falla y la que más acierta" font-family="{FF}">']
t = lambda x, y, s, size=11.5, fill=TXT, anchor='start', w=400: o.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{w}">{s}</text>')
t(0, 18, 'Mensajes de enero a septiembre, en millones', 12.5, INK, w=600)
for i, (k, col, lab_) in enumerate(SEGS):
    lx, ly = (0 if i % 2 == 0 else 300), 38 + 18 * (i // 2)
    o.append(f'<rect x="{lx}" y="{ly - 9}" width="10" height="10" fill="{col}"/>'); t(lx + 15, ly, lab_, 11.5, TXT)
t(CX, 86, 'La campaña con más mensajes que no responde', 11.5, SEC, w=600)
for v in (0, 100, 200):
    o.append(f'<line x1="{xs(v * 1e6):.1f}" x2="{xs(v * 1e6):.1f}" y1="{TOP - 14}" y2="{TOP + RH * len(rows) - 18}" stroke="{GRID}"/>')
    t(xs(v * 1e6), TOP + RH * len(rows) - 4, f'{v} M', 11, SEC, 'middle')
for i, r in enumerate(rows):
    y = TOP + RH * i
    t(0, y + 9, r['equipo'], 12.5, INK, w=600); t(0, y + 24, f"{r['tot']/1e6:.0f} M mensajes", 11, SEC)
    x = X0
    for k, col, _ in SEGS:
        v = r[k]; wv = xs(v) - X0
        if wv > 0.4: o.append(f'<rect x="{x:.1f}" y="{y}" width="{max(wv - 1.5, 0.6):.1f}" height="{BH}" fill="{col}"/>')
        x += wv
    if r['sin_no'] > 0:
        pv = 100 * r['sin_no'] / r['tot']
        lx = xs(r['sin_no'])
        txt = f"{r['sin_no']/1e6:.0f} M ({pv:.0f} %)"
        if lx - X0 > 78: t(X0 + 6, y + 14.5, txt, 11.5, '#FFFFFF', w=600)
        else: t(x + 6, y + 14.5, txt, 11.5, INK, w=600)
    n1, l1 = r['falla']; t(CX, y + 9, n1, 12, INK, w=600); t(CX, y + 24, l1, 11, SEC)
t(0, Hh - 22, 'Responde lo mínimo aceptable: 3 clics por cada mil emails, 7.5 aperturas por cada mil push, 6 de cada 10 WhatsApp leídos o 1 de cada 10 in-app con clic.', 10.5, SEC)
t(0, Hh - 8, 'Hizo algo hace poco: dejó el registro a medias, es cliente activo o recurrente, tiene un pago por vencer o recibe un aviso de algo que hizo.', 10.5, SEC)
o.append('</svg>')
J = json.loads((H / 's2.json').read_text(encoding='utf-8')); J['svg'] = ''.join(o)
(H / 's2.json').write_text(json.dumps(J, ensure_ascii=False, indent=1), encoding='utf-8')
for r in rows: print(r['equipo'], {k: round(r[k] / 1e6, 1) for k in ('tot', 'sin_no', 'sin_si', 'con_no', 'con_si')}, r['falla'][0], '|', r['acierta'][0])
