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


# ---------- ronda 2: ejes log, dispersión, franjas y nombres limpios ----------
import math, re as _re


def logx(v0, v1, p0, p1):
    """Escala logarítmica de [v0, v1] a [p0, p1]."""
    a, b = math.log10(v0), math.log10(v1)
    return lambda v: p0 + (p1 - p0) * (math.log10(min(max(v, v0), v1)) - a) / (b - a)


def jit(i, n=7, amp=1.0):
    """Desplazamiento determinista para franjas de puntos (sin azar)."""
    return amp * (((i * 37) % n) / (n - 1) - 0.5)


def fit(xs, ys):
    """Recta por mínimos cuadrados y R²."""
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs); sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys)); syy = sum((y - my) ** 2 for y in ys)
    b = sxy / sxx; a = my - b * mx
    return a, b, sxy * sxy / (sxx * syy)


def med(v):
    s = sorted(v); n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


NOMBRES = [(r'B0171.*Anonim', 'Rescate Tasa 0 a anónimos'), (r'B0171.*Narrativa', 'Tasa 0 a rezagados, narrativa'),
           (r'B0171.*HotLead', 'Rescate Tasa 0 a leads recientes'), (r'B0171', 'Rescate Tasa 0 a rezagados'),
           (r'B0209', 'Descuento a inactivos'), (r'B0326.*Dormant', 'Referidos a dormants'), (r'B0326.*Leads', 'Referidos a leads'),
           (r'B0326', 'Referidos a clientes'), (r'B0333|B0207', 'Churn 12 meses'), (r'B0332|B0206', 'Inactivos 6 meses'),
           (r'B0331', 'Inactivos 3 meses'), (r'B0208', 'Inactivos 30 a 90 días'), (r'B0223', 'Installments a quien nunca activó'),
           (r'B0211', 'Tasa 0 a registrados de Pay'), (r'B0224', 'Segunda oportunidad'), (r'B0335', 'Promos de comercios a todo el portafolio'),
           (r'Comerciodel', 'Comercio del día'), (r'S0004', 'Recomendaciones semanales'), (r'B0301', 'Installments a activos'),
           (r'B0391', 'Rescate de fin de semana a leads'), (r'B0493', 'Hot Sale'), (r'BillPay', 'BillPay'), (r'Veriff', 'Recordatorio Veriff'),
           (r'B0440|AnotayGana', 'AnotayGana'), (r'B0205', 'Cupón a dormants'), (r'B0152', 'Cumpleaños'), (r'Newsletter', 'Newsletter'),
           (r'B0368|Temu', 'Temu'), (r'B0619', 'Fiestas Patrias a inactivos')]


def nombre(f):
    for rx, n in NOMBRES:
        if _re.search(rx, f): return n
    p = f.split('-')
    return (p[5] if len(p) > 5 else p[-1])[:28]


def kpis(S, items, y=30):
    """Franja de 3 cifras: items = [(cifra, línea 1, línea 2)], cada una en un tercio del ancho."""
    for i, (n_, l1, l2) in enumerate(items):
        x = i * W / 3
        wn = sum(7 if ch in ' .,' else (22 if ch in 'MW%' else (8 if ch in 'il' else 15)) for ch in n_)
        S.t(x, y, n_, 24, BLUE, w=700); S.t(x + wn + 8, y - 8, l1, 10.5, TXT); S.t(x + wn + 8, y + 5, l2, 10.5, TXT)
    S.line(0, y + 20, W, y + 20, GRID)


def swarm(xs, r, maxoff):
    """Desplazamiento vertical tipo beeswarm: cada punto en el primer hueco libre (0, +d, -d, +2d...) sin encimarse."""
    placed, out = [], []
    d = 2 * r + 0.6
    for x in xs:
        for k in range(0, 60):
            off = ((k + 1) // 2) * (r * 1.05) * (1 if k % 2 else -1)
            if abs(off) > maxoff: off = None; break
            if all((x - px) ** 2 + (off - py) ** 2 >= d * d for px, py in placed if abs(px - x) < d): break
        if off is None: off = maxoff * (1 if len(out) % 2 else -1)
        placed.append((x, off)); out.append(off)
    return out
