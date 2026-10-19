# Ayudas de dibujo para las gráficas granulares de la ronda 2 (escalas log, ejes, etiquetas con línea guía).
import math
from kit import *

def lin(lo, hi, p0, p1):
    return lambda v: p0 + (p1 - p0) * (v - lo) / (hi - lo)

def logs(lo, hi, p0, p1):
    a, b = math.log10(lo), math.log10(hi)
    return lambda v: p0 + (p1 - p0) * (math.log10(max(v, lo)) - a) / (b - a)

def fmt_n(v):
    if v >= 1e6: return f'{v / 1e6:g} M'
    if v >= 1e3: return f'{v / 1e3:g} mil'
    return f'{v:g}'

def xaxis(o, sx, ticks, y0, y1, fmt=fmt_n, title=None, title_y=None, x_mid=None, size=11):
    for v in ticks:
        x = sx(v)
        o.append(f'<line x1="{x:.1f}" y1="{y0}" x2="{x:.1f}" y2="{y1}" stroke="{GRID}" stroke-width="1"/>')
        o.append(t(x, y1 + 14, fmt(v), size, SEC, 400, 'middle'))
    if title:
        o.append(t(x_mid, title_y or y1 + 30, title, 11, SEC, 400, 'middle'))

def yaxis(o, sy, ticks, x0, x1, fmt=fmt_n, size=11):
    for v in ticks:
        y = sy(v)
        o.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="{GRID}" stroke-width="1"/>')
        o.append(t(x0 - 5, y + 4, fmt(v), size, SEC, 400, 'end'))

def dot(o, x, y, r=3, fill=MARK, stroke='#fff', op=None, sw=1):
    oo = f' fill-opacity="{op}"' if op is not None else ''
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}"{oo}{st}/>')

def note(o, x, y, tx, ty, text, anchor='start', size=11.5, fill=INK, w=600, line=True, sub=None):
    if line:
        ex = tx - 3 if anchor == 'start' else tx + 3 if anchor == 'end' else tx
        o.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{ex:.1f}" y2="{ty - 4:.1f}" stroke="{MARK}" stroke-width="0.8"/>')
    o.append(t(tx, ty, text, size, fill, w, anchor, True))
    if sub:
        o.append(t(tx, ty + size + 2, sub, size - 1, SEC, 400, anchor, True))

def ols(xs, ys):
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n
    sxx = sum((a - mx) ** 2 for a in xs); sxy = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    syy = sum((b - my) ** 2 for b in ys)
    b = sxy / sxx; a = my - b * mx; r2 = sxy * sxy / (sxx * syy) if syy else 0
    return a, b, r2

def median(v):
    v = sorted(v); n = len(v)
    return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2
