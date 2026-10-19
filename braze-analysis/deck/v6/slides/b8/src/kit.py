# Utilidades comunes del bloque b8 (láminas 86 a 110): paleta, texto SVG y escritura de JSON.
import json, os, html as _h
OUT = '/home/user/claude/braze-analysis/deck/v6/slides/b8/'
INK, TXT, SEC, MARK, MARK2, GRID = '#0B1220', '#3B4556', '#6B7484', '#A3AAB5', '#C9CED6', '#DDE2EA'
BLUE, BLUE_L, GREEN, GREEN_L = '#1F4FD8', '#8FA8EE', '#127A5B', '#7CC4A8'
F = 'font-family="Inter, system-ui, sans-serif"'
E = lambda s: _h.escape(str(s), quote=False)

def t(x, y, s, size=12, fill=TXT, w=400, anchor='start', halo=False, extra=''):
    h = ' stroke="#fff" stroke-width="3" paint-order="stroke"' if halo else ''
    return (f'<text x="{x:.1f}" y="{y:.1f}" {F} font-size="{size}" font-weight="{w}" fill="{fill}" '
            f'text-anchor="{anchor}"{h}{extra}>{s}</text>')

def svg_open(label, w=780, h=420):
    return [f'<svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="{E(label)}" xmlns="http://www.w3.org/2000/svg">',
            f'<rect width="{w}" height="{h}" fill="#FFFFFF"/>']

def m(v, d=2):
    return f'{v / 1e6:.{d}f}'

def miles(v):
    return f'{v:,.0f}'

def save(n, d, sub=None):
    o = {'n': n}
    if sub: o['sub'] = sub
    o.update(d)
    for k in ('titulo', 'que', 'quien', 'a_quien', 'causa', 'sowhat', 'fuente', 'impacto'):
        if k in o: o[k] = o[k].replace(' %', '\u00a0%')
    for k in ('lecturas', 'porques', 'como'):
        if k in o: o[k] = [x.replace(' %', '\u00a0%') for x in o[k]]
    if 'hipotesis' in o: o['hipotesis'] = {a: b.replace(' %', '\u00a0%') for a, b in o['hipotesis'].items()}
    name = f'{n:03d}' + (f'_{sub}' if sub else '') + '.json'
    for k in ('titulo', 'que', 'quien', 'a_quien', 'causa', 'sowhat', 'fuente'):
        if k in o and any(ch in str(o[k]) for ch in '—–→'):
            raise ValueError(f'{name}: guion largo o flecha en {k}')
    json.dump(o, open(os.path.join(OUT, name), 'w'), ensure_ascii=False, indent=1)
    return name
