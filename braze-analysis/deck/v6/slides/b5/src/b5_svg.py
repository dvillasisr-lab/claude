"""Utilidades comunes del bloque 5: paleta, texto SVG y escritura del JSON de cada lámina."""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent
OUTDIR = H.parent
D = json.load(open(H / 'b5_datos.json', encoding='utf-8'))
INK, TXT, SEC, MARK, MARK2, GRID = '#0B1220', '#3B4556', '#6B7484', '#A3AAB5', '#C9CED6', '#DDE2EA'
BLUE, BLUEL, GREEN, GREENL = '#1F4FD8', '#8FA8EE', '#127A5B', '#7CC4A8'
FF = 'Inter, system-ui, sans-serif'
W, HH = 780, 420


class Svg:
    def __init__(self, label):
        self.o = [f'<svg viewBox="0 0 {W} {HH}" width="100%" role="img" aria-label="{label}" font-family="{FF}">']

    def t(self, x, y, s, size=11.5, fill=TXT, anchor='start', w=400, halo=False):
        h = ' stroke="#FFFFFF" stroke-width="4" stroke-linejoin="round" paint-order="stroke"' if halo else ''
        self.o.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{w}"{h}>{s}</text>')

    def rect(self, x, y, w, h, fill, extra=''):
        if w <= 0 or h <= 0: return
        self.o.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}"{extra}/>')

    def line(self, x1, y1, x2, y2, stroke=GRID, sw=1, extra=''):
        self.o.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{extra}/>')

    def circle(self, cx, cy, r, fill, stroke='#FFFFFF', sw=2):
        self.o.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def raw(self, s):
        self.o.append(s)

    def done(self):
        return ''.join(self.o) + '</svg>'


def guarda(n, d):
    d = dict(n=n, **d)
    p = OUTDIR / f'{n:03d}.json'
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')
    print('escrito', p)


def M(v, dec=1):
    return f'{v / 1e6:.{dec}f}'


def mil(v):
    return f'{v / 1e3:.0f}'


def fmt(v):
    """Entero con coma de miles."""
    return f'{v:,.0f}'
