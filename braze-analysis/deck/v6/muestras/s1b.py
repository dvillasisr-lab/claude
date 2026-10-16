"""Lámina 1 v2: meses en orden. Arriba, mensajes enviados por canal (millones de mensajes); abajo, respuestas por cada mil mensajes.
Datos: data/e1 con base_p1.load() (lecturas de WhatsApp del mes siguiente incluidas). Escribe s1.json (actualiza svg)."""
import json, pathlib, sys
H = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(H))
from base_p1 import load
d = load()
d['respu'] = d.email_click + d.pn_open + d.whatsapp_read + d.in_app_click
g = d.groupby('m').agg(env=('envios', 'sum'), r=('respu', 'sum'))
rpm = (1000 * g.r / g.env).round(0)
ch = d.groupby(['m', 'canal']).envios.sum().unstack().fillna(0) / 1e6
MES = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep']
ORD = [('whatsapp', 'WhatsApp', '#127A5B'), ('push notification', 'Push', '#1F4FD8'), ('email', 'Email', '#A3AAB5'), ('in-app', 'In-app', '#7CC4A8')]
INK, TXT, SEC, GRID = '#0B1220', '#3B4556', '#6B7484', '#DDE2EA'
FF = 'Inter, system-ui, sans-serif'
W, Hh = 780, 420
X0, X1 = 58, 596
step = (X1 - X0) / 9; bw = step * 0.56
cx = lambda i: X0 + step * (i + 0.5)
T0, T1 = 52, 232          # panel de volumen
VMAX = 120
vy = lambda v: T1 - (T1 - T0) * v / VMAX
B0, B1 = 286, 384         # panel de respuesta
RMIN, RMAX = 40, 100
ry = lambda v: B1 - (B1 - B0) * (v - RMIN) / (RMAX - RMIN)
o = [f'<svg viewBox="0 0 {W} {Hh}" width="100%" role="img" aria-label="Mensajes enviados por mes y canal, y respuestas por cada mil mensajes, enero a septiembre 2026" font-family="{FF}">']
t = lambda x, y, s, size=11.5, fill=TXT, anchor='start', w=400: o.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{w}">{s}</text>')
t(X0 - 46, 22, 'Mensajes enviados en el mes, por canal (millones de mensajes)', 12.5, INK, w=600)
for v in (0, 40, 80, 120):
    o.append(f'<line x1="{X0}" x2="{X1}" y1="{vy(v):.1f}" y2="{vy(v):.1f}" stroke="{GRID}" stroke-width="1"/>')
    t(X0 - 8, vy(v) + 4, f'{v}', 11, SEC, 'end')
for i, m in enumerate(range(1, 10)):
    base = 0
    for key, lab, col in ORD:
        v = ch.loc[m].get(key, 0)
        y1, y0 = vy(base + v), vy(base)
        o.append(f'<rect x="{cx(i) - bw/2:.1f}" y="{y1:.1f}" width="{bw:.1f}" height="{max(0, y0 - y1 - 1.5):.1f}" fill="{col}"/>')
        base += v
    hi = m in (1, 6, 9)
    t(cx(i), vy(base) - 6, f'{base:.0f}', 12 if hi else 11, INK if hi else TXT, 'middle', 600 if hi else 400)
# etiquetas directas de canal a la derecha de septiembre, con su parte en enero y septiembre
base = 0; ys = []
for key, lab, col in ORD:
    v = ch.loc[9].get(key, 0); ys.append((vy(base + v / 2), key, lab, col)); base += v
s1 = 100 * ch.loc[1] / ch.loc[1].sum(); s9 = 100 * ch.loc[9] / ch.loc[9].sum()
last = 1e9
for y, key, lab, col in sorted(ys, key=lambda r: r[0]):
    y = max(y, 0) if last == 1e9 else max(y, last + 15); last = y
    o.append(f'<rect x="{X1 + 6}" y="{y - 8:.1f}" width="9" height="9" fill="{col}"/>')
    t(X1 + 20, y, f'{lab}: {s1[key]:.0f} % a {s9[key]:.0f} %', 11.5, TXT)
t(X1 + 6, T0 - 4, 'Parte del total,', 10.5, SEC); t(X1 + 6, T0 + 8, 'enero a septiembre', 10.5, SEC)
# panel de respuesta
t(X0 - 46, B0 - 26, 'Respuestas por cada mil mensajes enviados', 12.5, INK, w=600)
for v in (40, 60, 80, 100):
    o.append(f'<line x1="{X0}" x2="{X1}" y1="{ry(v):.1f}" y2="{ry(v):.1f}" stroke="{GRID}" stroke-width="1"/>')
    t(X0 - 8, ry(v) + 4, f'{v}', 11, SEC, 'end')
o.append(f'<line x1="{X0}" x2="{X1}" y1="{ry(rpm[1]):.1f}" y2="{ry(rpm[1]):.1f}" stroke="{SEC}" stroke-width="1" stroke-dasharray="4 4"/>')
t(X1 + 6, ry(rpm[1]) + 4, f'Nivel de enero: {rpm[1]:.0f}', 11.5, SEC)
pts = ' '.join(f'{cx(i):.1f},{ry(rpm[m]):.1f}' for i, m in enumerate(range(1, 10)))
o.append(f'<polyline points="{pts}" fill="none" stroke="{INK}" stroke-width="2"/>')
for i, m in enumerate(range(1, 10)):
    hi = m in (6, 9)
    o.append(f'<circle cx="{cx(i):.1f}" cy="{ry(rpm[m]):.1f}" r="{5 if hi else 4}" fill="{"#1F4FD8" if hi else INK}" stroke="#fff" stroke-width="2"/>')
    above = rpm[m] < 95
    t(cx(i), ry(rpm[m]) + (-10 if above else 16), f'{rpm[m]:.0f}', 12 if hi else 11, INK if hi else TXT, 'middle', 600 if hi else 400)
for i, mm in enumerate(MES):
    t(cx(i), Hh - 14, mm, 11.5, TXT, 'middle')
o.append('</svg>')
J = json.loads((H / 's1.json').read_text(encoding='utf-8'))
J['svg'] = ''.join(o)
(H / 's1.json').write_text(json.dumps(J, ensure_ascii=False, indent=1), encoding='utf-8')
print(rpm.to_dict()); print(ch.round(1)); print(s1.round(1).to_dict(), s9.round(1).to_dict())
