"""Ayudas de SVG y salida JSON para el bloque b3 (paleta y tipografía del deck v6)."""
import json, subprocess, pathlib, os
INK, TXT, SEC, MRK, MRK2, GRID = '#0B1220', '#3B4556', '#6B7484', '#A3AAB5', '#C9CED6', '#DDE2EA'
BLUE, BLUEL, GREEN, GREENL = '#1F4FD8', '#8FA8EE', '#127A5B', '#7CC4A8'
FF = 'Inter, system-ui, sans-serif'
W, H = 780, 420
OUT = pathlib.Path('/home/user/claude/braze-analysis/deck/v6/slides/b3')
REV = '/tmp/claude-0/-home-user-claude/e114ba4f-39d4-57f8-9f24-b0f0c0cbef51/scratchpad/rev/'
def esc(s): return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
def n1(v, d=1):
    s = f'{v:,.{d}f}'; return s
class Svg:
    def __init__(self, label):
        self.o = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{esc(label)}" font-family="{FF}">']
    def t(self, x, y, s, size=11.5, fill=TXT, anchor='start', w=400, halo=False):
        h = ' stroke="#FFFFFF" stroke-width="3" paint-order="stroke" stroke-linejoin="round"' if halo else ''
        self.o.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{w}"{h}>{esc(s)}</text>')
    def ts(self, x, y, parts, size=11.5, anchor='start', halo=False):
        """Texto con tramos: parts = [(texto, color, peso), ...]"""
        h = ' stroke="#FFFFFF" stroke-width="3" paint-order="stroke" stroke-linejoin="round"' if halo else ''
        sp = ''.join(f'<tspan fill="{c}" font-weight="{w}">{esc(s)}</tspan>' for s, c, w in parts)
        self.o.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}"{h}>{sp}</text>')
    def r(self, x, y, w, h, fill, rx=0, stroke=None, sw=1):
        st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
        self.o.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w,0):.1f}" height="{max(h,0):.1f}" fill="{fill}" rx="{rx}"{st}/>')
    def l(self, x1, y1, x2, y2, stroke=GRID, sw=1):
        self.o.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"/>')
    def c(self, x, y, r, fill, stroke='#FFFFFF', sw=1.5, op=1):
        o = f' fill-opacity="{op}"' if op != 1 else ''
        self.o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}"{o} stroke="{stroke}" stroke-width="{sw}"/>')
    def raw(self, s): self.o.append(s)
    def done(self): return ''.join(self.o) + '</svg>'
def save(n, d):
    d = dict(n=n, **d)
    p = OUT / f'{n:03d}.json'
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')
    return p
def check(n):
    p = OUT / f'{n:03d}.json'
    subprocess.run(['python3', 'deck_v6_render.py', '--solo', str(p), f'{REV}{n:03d}.html'], cwd='/home/user/claude/braze-analysis/scripts', check=True, capture_output=True)
    r = subprocess.run(['node', 'check.js', f'{REV}{n:03d}.html', f'{REV}{n:03d}.png'], cwd='/home/user/claude/braze-analysis/deck/v6/tools',
                       env={**os.environ, 'NODE_PATH': '/opt/node-tools/node_modules'}, capture_output=True, text=True)
    print(f'[{n:03d}]', r.stdout.strip(), r.stderr.strip()[-400:])
