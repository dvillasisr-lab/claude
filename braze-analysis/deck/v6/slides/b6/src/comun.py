"""Base común del bloque b6 (láminas 56 a 65, sección VII: comportamiento del usuario).
Lee solo CSV del repo (data/ y hallazgos/). Paleta, ayudante de SVG y escritura del JSON de cada lámina.
Costo: email 0.05 MXN por enviado, WhatsApp 1.00 MXN por entregado, push e in-app 0."""
import json, pathlib, re, sys
import numpy as np
import pandas as pd

R = pathlib.Path('/home/user/claude/braze-analysis')
D, H = R / 'data', R / 'hallazgos'
OUT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(R / 'scripts'))
from deck_data import gancho_of  # noqa: E402  (regla de tema por el nombre usada en el guion)

SECCION = 'La gente responde a lo que ya empezó y se va cuando insistimos'
INK, TXT, SEC, M1, M2, GRID = '#0B1220', '#3B4556', '#6B7484', '#A3AAB5', '#C9CED6', '#DDE2EA'
BLUE, BLUEL, GREEN, GREENL = '#1F4FD8', '#8FA8EE', '#127A5B', '#7CC4A8'
FF = 'Inter, system-ui, sans-serif'
RESP = {'email': ('email_delivery', 'email_click'), 'push notification': ('pn_send', 'pn_open'),
        'whatsapp': ('whatsapp_delivery', 'whatsapp_read'), 'in-app': ('in_app_impression', 'in_app_click')}
TEAM = {'Lending': 'Product Growth', 'NewProducts': 'Others', 'Shopping': 'Others', 'QA': 'Others'}


def grupo(n):
    """Grupo de audiencia por el nombre de la campaña (regla de p4_calc.py, notas de la parte 4)."""
    s = str(n).lower()
    if s.startswith('collections') or 'cobranza' in s or 'bkt' in s: return 'cobranza'
    if s.startswith('transaccional') or 'payment' in s or 'contracts' in s or 'disbursed' in s: return 'transaccional'
    if 'mpnevercash' in s or 'portafolioactivoeinactivo' in s: return 'activos'
    if re.search(r'dormant|inactiv|churn|lazaro|softnactive', s): return 'ex clientes'
    if re.search(r'rezagad|never|anonim|hotlead', s): return 'nunca activaron'
    if re.search(r'leads|registrad|prospect|leftfunnel', s): return 'leads'
    if re.search(r'nuevos|onboarding|1er|1ra|welcome', s): return 'nuevos'
    if re.search(r'recurrente|active|activo|cliente', s): return 'activos'
    return 'otros'


GAN_G = [('tasa0', r'(Tasa0|Tasa 0)'), ('descuento', r'(Descuento|Cupon|Cupón|Oferta)'), ('referidos', r'(Referral|AnotayGana)'),
         ('recordatorio', r'(Retargeting|Rescate|Recordatorio|Reminder)'), ('lanzamiento', r'(Lanzamiento|Intro|Newsletter|Recommendations)'),
         ('xsell', r'(XSell|Cross)')]


def gan_g(n):
    """Tema por el nombre, regla de la muestra G (sql/muestra_g_buenas_practicas.sql)."""
    for lab, rx in GAN_G:
        if re.search(rx, str(n), re.I): return lab
    return 'otros'


def fam(s):
    return re.sub(r'-\d{8,9}-', '-', str(s))


def load_e1():
    e = pd.read_csv(D / 'e1_comunicacion_mes_canal.csv')
    e['communication_name'] = e.communication_name.fillna('(sin nombre)')
    e['familia'] = e.communication_name.map(fam)
    for c in ['envios', 'usuarios_aprox', 'email_sent', 'email_delivery', 'email_open', 'email_click', 'email_unsubscribe', 'pn_send', 'pn_open',
              'whatsapp_send', 'whatsapp_delivery', 'whatsapp_read', 'in_app_impression', 'in_app_click', 'conversiones_fraccional']:
        e[c] = pd.to_numeric(e[c], errors='coerce').fillna(0)
    e['costo'] = e.email_sent * 0.05 + e.whatsapp_delivery * 1.0
    e['grupo'] = e.communication_name.map(grupo)
    e['equipo'] = e.team.map(lambda t: TEAM.get(t, t))
    tipo = pd.read_csv(H / 'muestra_c_familias.csv').groupby('familia').tipo.first()
    e['tipo'] = e.familia.map(tipo)
    return e


def resp(g, canal):
    b, r = RESP[canal]
    return 100 * g[r].sum() / g[b].sum() if g[b].sum() else np.nan


def mil(v):
    """Personas: 158520 -> '159 mil'; 1585599 -> '1.6 M'."""
    return f'{v/1e6:.1f} M' if v >= 1e6 else f'{v/1e3:.0f} mil'


class SVG:
    def __init__(self, label, w=780, h=420):
        self.w, self.h = w, h
        self.o = [f'<svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="{label}" font-family="{FF}">']

    def t(self, x, y, s, size=11.5, fill=TXT, anchor='start', w=400, halo=False):
        hl = ' stroke="#FFFFFF" stroke-width="4" stroke-linejoin="round" paint-order="stroke"' if halo else ''
        self.o.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{w}"{hl}>{s}</text>')

    def rect(self, x, y, w, h, fill, extra=''):
        if w <= 0 or h <= 0: return
        self.o.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}"{extra}/>')

    def line(self, x1, y1, x2, y2, stroke=GRID, sw=1, extra=''):
        self.o.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{extra}/>')

    def circle(self, cx, cy, r, fill, ring=True, extra=''):
        st = ' stroke="#FFFFFF" stroke-width="2"' if ring else ''
        self.o.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}"{st}{extra}/>')

    def raw(self, s):
        self.o.append(s)

    def legend(self, items, x=0, y=12, gap=16, size=11.5):
        """items: (color, texto, forma) con forma 'rect', 'dot' o 'line'. Una fila."""
        for col, lab, shape in items:
            if shape == 'dot': self.circle(x + 5, y + 5, 5, col, ring=False)
            elif shape == 'line': self.line(x, y + 5, x + 18, y + 5, col, 2.5); x += 8
            else: self.rect(x, y, 10, 10, col)
            self.t(x + 15, y + 9, lab, size, TXT)
            x += 15 + len(lab) * size * 0.53 + gap
        return x

    def svg(self):
        return ''.join(self.o) + '</svg>'


def write(n, d):
    d = {'n': n, 'kind': d.pop('kind', 'grafica'), 'seccion': SECCION, **d}
    p = OUT / f'{n:03d}.json'
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')
    print('escrito', p)
