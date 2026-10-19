"""Utilidades comunes del bloque 1 (láminas 1 a 10): carga de E1 con las reglas de base_p1, paleta y ayudas de SVG."""
import json, pathlib, sys
H = pathlib.Path(__file__).resolve().parent
OUT = H.parent
ROOT = pathlib.Path('/home/user/claude/braze-analysis')
sys.path.insert(0, str(ROOT / 'deck' / 'v6' / 'muestras'))
from base_p1 import load  # noqa: E402  (E1 con equipo, tipo, audiencia, tema y costo por entregado)

INK, TXT, SEC = '#0B1220', '#3B4556', '#6B7484'
G1, G2, GRID = '#A3AAB5', '#C9CED6', '#DDE2EA'
BLUE, BLUE2, GREEN, GREEN2 = '#1F4FD8', '#8FA8EE', '#127A5B', '#7CC4A8'
FF = 'Inter, system-ui, sans-serif'
MES = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep']
FUENTE_E1 = 'Fuente: Braze, envíos por comunicación, mes y canal, enero a septiembre 2026'
COSTO = 'WhatsApp a 1.00 MXN por entregado, email a 0.05 MXN por enviado, push e in-app sin costo'


class Svg:
    def __init__(self, label, w=780, h=420):
        self.o = [f'<svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="{label}" font-family="{FF}">']

    def t(self, x, y, s, size=11.5, fill=TXT, anchor='start', w=400, halo=False):
        h = ' stroke="#FFFFFF" stroke-width="4" stroke-linejoin="round" paint-order="stroke"' if halo else ''
        self.o.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{w}"{h}>{s}</text>')

    def rect(self, x, y, w, h, fill, extra=''):
        self.o.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(0, w):.1f}" height="{max(0, h):.1f}" fill="{fill}"{extra}/>')

    def line(self, x1, y1, x2, y2, stroke=GRID, sw=1, extra=''):
        self.o.append(f'<line x1="{x1:.1f}" x2="{x2:.1f}" y1="{y1:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{extra}/>')

    def circle(self, x, y, r, fill):
        self.o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="#fff" stroke-width="2"/>')

    def poly(self, pts, stroke=INK, sw=2):
        p = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)
        self.o.append(f'<polyline points="{p}" fill="none" stroke="{stroke}" stroke-width="{sw}"/>')

    def done(self):
        return ''.join(self.o) + '</svg>'


def write(n, d):
    d = {'n': n, **d}
    p = OUT / f'{n:03d}.json'
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')
    print('escrito', p)


def fmt(v, dec=1):
    """Número con punto decimal y coma de miles (estilo del deck)."""
    return f'{v:,.{dec}f}'
