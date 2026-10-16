"""Lámina 1 v3 (pedido del usuario): una sola gráfica combinada. Barras apiladas = millones de mensajes por canal (eje izquierdo);
línea = respuestas por cada mil mensajes (eje derecho, con valores escritos en cada punto). Actualiza el svg de s1.json."""
import json, pathlib, sys
H = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(H))
from base_p1 import load
d = load()
d['respu'] = d.email_click + d.pn_open + d.whatsapp_read + d.in_app_click
g = d.groupby('m').agg(env=('envios', 'sum'), r=('respu', 'sum'))
rpm = (1000 * g.r / g.env).round(0)
ch = d.groupby(['m', 'canal']).envios.sum().unstack().fillna(0) / 1e6
s1 = 100 * ch.loc[1] / ch.loc[1].sum(); s9 = 100 * ch.loc[9] / ch.loc[9].sum()
MES = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep']
ORD = [('whatsapp', 'WhatsApp', '#127A5B'), ('push notification', 'Push', '#1F4FD8'), ('email', 'Email', '#C9CED6'), ('in-app', 'In-app', '#7CC4A8')]
INK, TXT, SEC, GRID = '#0B1220', '#3B4556', '#6B7484', '#DDE2EA'
FF = 'Inter, system-ui, sans-serif'
W, Hh = 780, 420
X0, X1 = 52, 724
Y0, Y1 = 84, 362
step = (X1 - X0) / 9; bw = step * 0.54
cx = lambda i: X0 + step * (i + 0.5)
VMAX, RMAX = 120, 120
vy = lambda v: Y1 - (Y1 - Y0) * v / VMAX
ry = lambda v: Y1 - (Y1 - Y0) * v / RMAX
o = [f'<svg viewBox="0 0 {W} {Hh}" width="100%" role="img" aria-label="Mensajes enviados por mes y canal, en barras, y respuestas por cada mil mensajes, en línea, enero a septiembre 2026" font-family="{FF}">']
def t(x, y, s, size=11.5, fill=TXT, anchor='start', w=400, halo=False):
    h = ' stroke="#FFFFFF" stroke-width="4" stroke-linejoin="round" paint-order="stroke"' if halo else ''
    o.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{w}"{h}>{s}</text>')
# leyenda en una fila
lx = 0
for key, lab, col in ORD:
    o.append(f'<rect x="{lx}" y="12" width="10" height="10" fill="{col}"/>')
    txt = f'{lab} {s1[key]:.0f} % a {s9[key]:.0f} %'; t(lx + 15, 21, txt, 11.5, TXT); lx += 15 + len(txt) * 6.1 + 14
o.append(f'<line x1="{lx}" x2="{lx + 22}" y1="17" y2="17" stroke="{INK}" stroke-width="2"/><circle cx="{lx + 11}" cy="17" r="4" fill="{INK}" stroke="#fff" stroke-width="2"/>')
t(lx + 28, 21, 'Respuestas por mil', 11.5, INK, w=600)
t(0, 40, 'Parte de cada canal en el total de mensajes, de enero a septiembre.', 10.5, SEC)
# ejes
t(X0 - 8, Y0 - 20, 'Millones de mensajes', 11, SEC, 'start')
t(X1 + 8, Y0 - 20, 'Respuestas por mil', 11, INK, 'end', 600)
for v in (0, 40, 80, 120):
    o.append(f'<line x1="{X0}" x2="{X1}" y1="{vy(v):.1f}" y2="{vy(v):.1f}" stroke="{GRID}" stroke-width="1"/>')
    t(X0 - 8, vy(v) + 4, f'{v} M', 11, SEC, 'end')
    t(X1 + 8, ry(v) + 4, f'{v}', 11, INK, 'start')
# barras
tops = {}
for i, m in enumerate(range(1, 10)):
    base = 0
    for key, lab, col in ORD:
        v = ch.loc[m].get(key, 0); y1, y0 = vy(base + v), vy(base)
        o.append(f'<rect x="{cx(i) - bw/2:.1f}" y="{y1:.1f}" width="{bw:.1f}" height="{max(0, y0 - y1 - 1.5):.1f}" fill="{col}"/>')
        base += v
    tops[m] = base
# referencia de enero y línea
o.append(f'<line x1="{X0}" x2="{X1}" y1="{ry(rpm[1]):.1f}" y2="{ry(rpm[1]):.1f}" stroke="{INK}" stroke-width="1" stroke-dasharray="4 4" opacity="0.6"/>')
t(X1 - 2, ry(rpm[1]) - 6, f'Nivel de enero: {rpm[1]:.0f} respuestas por mil', 11, INK, 'end', halo=True)
pts = ' '.join(f'{cx(i):.1f},{ry(rpm[m]):.1f}' for i, m in enumerate(range(1, 10)))
o.append(f'<polyline points="{pts}" fill="none" stroke="{INK}" stroke-width="2.5"/>')
for i, m in enumerate(range(1, 10)):
    hi = m in (6, 9)
    o.append(f'<circle cx="{cx(i):.1f}" cy="{ry(rpm[m]):.1f}" r="{5.5 if hi else 4.5}" fill="{INK}" stroke="#fff" stroke-width="2"/>')
    t(cx(i), ry(rpm[m]) + 18, f'{rpm[m]:.0f}', 12.5 if hi else 11.5, INK, 'middle', 700 if hi else 600, halo=True)
for i, mm in enumerate(MES):
    m = i + 1; hi = m in (1, 6, 9)
    t(cx(i), Y1 + 17, mm, 11.5, TXT, 'middle')
    t(cx(i), Y1 + 33, f'{tops[m]:.0f} M', 11.5, INK if hi else SEC, 'middle', 600 if hi else 400)
t(X0 - 8, Y1 + 33, 'Total', 11, SEC, 'end')
o.append('</svg>')
J = json.loads((H / 's1.json').read_text(encoding='utf-8'))
J['svg'] = ''.join(o)
(H / 's1.json').write_text(json.dumps(J, ensure_ascii=False, indent=1), encoding='utf-8')
print(rpm.to_dict(), {m: round(v, 1) for m, v in tops.items()})
