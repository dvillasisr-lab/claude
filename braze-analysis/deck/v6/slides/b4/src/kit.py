"""Utilidades comunes del bloque b4 (láminas 33 a 46): paleta, SVG y escritura del JSON."""
import json, pathlib, re, numpy as np, pandas as pd
SRC = pathlib.Path(__file__).resolve().parent
OUT = SRC.parent
R = '/home/user/claude/braze-analysis/'
D = R + 'data/'
INK, TXT, SEC = '#0B1220', '#3B4556', '#6B7484'
G1, G2, GRID = '#A3AAB5', '#C9CED6', '#DDE2EA'
BLUE, BLUE2, GREEN, GREEN2 = '#1F4FD8', '#8FA8EE', '#127A5B', '#7CC4A8'
FF = 'Inter, system-ui, sans-serif'
TM = {'Lending': 'Product Growth', 'Product Growth': 'Product Growth', 'Marketing': 'Marketing', 'Sales': 'Sales',
      'Collections': 'Collections', 'B2B': 'Sales'}
def team(t): return TM.get(str(t).strip(), 'Others')
TICKET_RE = r'-[A-Z]?[BTS]0?\d{3,5}-'
def tipo(fam, t=None):
    if t == 'Collections' or str(fam).startswith('Collections'): return 'cobranza'
    if str(fam).startswith('Transaccional') or not re.search(TICKET_RE, str(fam)): return 'transaccional'
    return 'promocional'
def fam(name): return re.sub(r'-\d{8}-', '-', str(name))

class Svg:
    def __init__(self, label, w=780, h=420):
        self.o = [f'<svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="{label}" font-family="{FF}">']
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
    def poly(self, pts, stroke=INK, sw=2.5, extra=''):
        p = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)
        self.o.append(f'<polyline points="{p}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"{extra}/>')
    def raw(self, s): self.o.append(s)
    def legend(self, items, x=0, y=12, size=11.5):
        """items: (tipo, color, texto); tipo 'sq' cuadro, 'ln' línea con punto."""
        for kind, col, txt in items:
            if kind == 'sq':
                self.rect(x, y, 10, 10, col); self.t(x + 15, y + 9, txt, size, TXT)
            else:
                self.line(x, y + 5, x + 22, y + 5, col, 2); self.circle(x + 11, y + 5, 4, col)
                self.t(x + 28, y + 9, txt, size, INK, w=600); x += 13
            x += 15 + len(txt) * size * 0.53 + 16
    def svg(self): return ''.join(self.o) + '</svg>'

def fmt(v, d=1):
    s = f'{v:,.{d}f}'
    return s.replace(',', ' ') if d == 0 and v >= 10000 else s.replace(',', '')

def write(n, d):
    d = dict(n=n, **d)
    p = OUT / f'{n:03d}.json'
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')
    for k in ('titulo', 'que', 'quien', 'a_quien', 'causa', 'sowhat', 'fuente', 'impacto'):
        if k in d and re.search('[–—→]', str(d[k])): print('AVISO guion o flecha en', k)
    print('escrito', p)
