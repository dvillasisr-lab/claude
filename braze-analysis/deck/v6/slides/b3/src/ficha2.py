"""Gráfica común de las fichas de equipo, ronda 2 (ESTANDAR.md). Cada punto = una campaña del equipo en un canal (50 mil o más
entregados, nueve meses). x = mensajes (escala log); y = respuesta en veces el mínimo aceptable de su canal (escala log), línea en 1.
Forma = canal; verde = responde lo mínimo, gris = no. Mejores (verde) y peores (azul) nombradas."""
import math
from datos import *
from svgk import *
CN = {'email': ('correo', 'clic'), 'push notification': ('push', 'apertura'), 'whatsapp': ('WhatsApp', 'lectura'), 'in-app': ('in-app', 'clic')}
def pct(v): return f'{v:.2f}' if v < 10 else f'{v:.0f}'
def mark(S, ch, x, y, r, fill, stroke='#FFFFFF', sw=0.7, op=1.0):
    o = f' fill-opacity="{op}"' if op != 1 else ''
    if ch == 'email': S.raw(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}"{o} stroke="{stroke}" stroke-width="{sw}"/>')
    elif ch == 'push notification': S.raw(f'<rect x="{x-r*0.9:.1f}" y="{y-r*0.9:.1f}" width="{1.8*r:.1f}" height="{1.8*r:.1f}" fill="{fill}"{o} stroke="{stroke}" stroke-width="{sw}"/>')
    elif ch == 'whatsapp': S.raw(f'<path d="M{x:.1f},{y-r*1.15:.1f} L{x+r*1.1:.1f},{y+r*0.8:.1f} L{x-r*1.1:.1f},{y+r*0.8:.1f} Z" fill="{fill}"{o} stroke="{stroke}" stroke-width="{sw}"/>')
    else: S.raw(f'<path d="M{x:.1f},{y-r*1.2:.1f} L{x+r*1.2:.1f},{y:.1f} L{x:.1f},{y+r*1.2:.1f} L{x-r*1.2:.1f},{y:.1f} Z" fill="{fill}"{o} stroke="{stroke}" stroke-width="{sw}"/>')
def build(eq, casos):
    """casos: [(nombre, patrón, canal, 'b' o 'w', dx, dy)]: etiqueta desplazada dx, dy desde el punto."""
    f = fam(); d = f[f.equipo == eq].copy()
    S = Svg(f'{eq}: mensajes contra respuesta de cada campaña por canal, con el mínimo aceptable y sus mejores y peores campañas')
    S.t(0, 16, f'{eq}: cada punto es una campaña en un canal', 12.5, INK, w=600)
    x = 0
    for ch, lab in [('email', 'Correo'), ('push notification', 'Push'), ('whatsapp', 'WhatsApp'), ('in-app', 'In-app')]:
        mark(S, ch, x + 6, 34, 4.5, '#FFFFFF', stroke=TXT, sw=1.1); S.t(x + 15, 38, lab, 11.5); x += 15 + len(lab) * 6.8 + 14
    x += 6
    for col, lab in [(GREENL, 'responde lo mínimo'), (MRK2, 'no lo responde'), (GREEN, 'mejores'), (BLUE, 'peores')]:
        mark(S, 'email', x + 6, 34, 4.5, col, stroke='none'); S.t(x + 15, 38, lab, 11.5); x += 15 + len(lab) * 6.3 + 14
    X0, X1, Y0, Y1 = 50, 770, 58, 372
    LX, HX, LY, HY = math.log10(5e4), math.log10(5e7), math.log10(0.02), math.log10(40)
    xs = lambda v: X0 + (X1 - X0) * (math.log10(min(max(v, 5e4), 5e7)) - LX) / (HX - LX)
    ys = lambda v: Y1 - (Y1 - Y0) * (math.log10(min(max(v, 0.02), 40)) - LY) / (HY - LY)
    for v, lab in [(1e5, '100 mil'), (3e5, '300 mil'), (1e6, '1 M'), (3e6, '3 M'), (1e7, '10 M'), (3e7, '30 M')]:
        S.l(xs(v), Y0, xs(v), Y1, GRID); S.t(xs(v), Y1 + 14, lab, 10.5, SEC, 'middle')
    for v, lab in [(0.03, '0.03'), (0.1, '0.1'), (0.3, '0.3'), (1, '1'), (3, '3'), (10, '10'), (30, '30')]:
        S.l(X0, ys(v), X1, ys(v), MRK if v == 1 else GRID, 1.3 if v == 1 else 1); S.t(X0 - 6, ys(v) + 4, lab, 10.5, INK if v == 1 else SEC, 'end', w=600 if v == 1 else 400)
    S.t(X1, Y1 + 30, 'Mensajes de la campaña en nueve meses (escala logarítmica)', 10.5, SEC, 'end')
    S.t(0, Y1 + 30, 'Alto: respuesta en veces el mínimo aceptable de su canal', 10.5, SEC)
    up = d[d.pasa]; dn = d[~d.pasa]
    S.ts(780, 16, [('Responden lo mínimo: ', GREEN, 600), (f'{len(up)} de {len(d)} campañas, {100*up.env.sum()/d.env.sum():.0f} % de los mensajes', INK, 600)], 11.5, 'end')
    S.t(X1 - 2, ys(1) - 5, 'mínimo aceptable', 10.5, SEC, 'end', halo=True)
    for r in d.sort_values('env', ascending=False).itertuples():
        mark(S, r.canal, xs(r.env), ys(r.vs_min), 3.3, GREENL if r.pasa else MRK2, op=0.9)
    det = {}
    for cc in casos:
        nm, pat, ch, kind, dx, dy = cc[:6]; extra = cc[6] if len(cc) > 6 else None
        z = d[d.familia.str.contains(pat, regex=True) & (d.canal == ch)].sort_values('env', ascending=False)
        if not len(z): raise SystemExit(f'sin campaña {eq} {pat} {ch}')
        z = z.iloc[0]; det[nm] = z
        px, py = xs(z.env), ys(z.vs_min)
        mark(S, ch, px, py, 5.2, GREEN if kind == 'b' else BLUE, stroke='#FFFFFF', sw=1.2)
        lx, ly = px + dx, py + dy
        S.l(px, py, lx, ly - 4, MRK, 0.8)
        anc = 'start' if dx >= 0 else 'end'
        c, m = CN[ch]
        S.t(lx + (3 if dx >= 0 else -3), ly, nm, 10.5, INK, anc, w=600, halo=True)
        sub = f'{c} · {pct(z.resp_pct)} % de {m} · {z.env/1e6:.1f} M' + (f' · {extra(z)}' if extra else '')
        S.t(lx + (3 if dx >= 0 else -3), ly + 12, sub, 10.5, TXT, anc, halo=True)
    return S.done(), d, det

def porpres(z): return f"{z.costo/max(z.convf,1):,.0f} MXN por préstamo"
def costo(z): return f"{z.costo/1e6:.2f} M MXN"
