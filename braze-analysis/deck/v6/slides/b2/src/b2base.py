"""Base común del bloque b2 (láminas 11 a 20, sección II): datos de E1 con las reglas de base_p1 y utilidades SVG."""
import json, pathlib, sys
import numpy as np, pandas as pd
HERE = pathlib.Path(__file__).resolve().parent
OUTDIR = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / 'muestras'))
from base_p1 import load, RESP, wagg  # noqa: E402,F401

SECCION = 'Pagamos el canal más caro y desaprovechamos el que más responde'
INK, TXT, SEC = '#0B1220', '#3B4556', '#6B7484'
G1, G2, GRID = '#A3AAB5', '#C9CED6', '#DDE2EA'
BLUE, BLUE2, GREEN, GREEN2 = '#1F4FD8', '#8FA8EE', '#127A5B', '#7CC4A8'
FF = 'Inter, system-ui, sans-serif'
MIN = {'email': 0.3, 'push notification': 0.75, 'whatsapp': 60.0, 'in-app': 10.0}
BASE = {'email': 'email_delivery', 'push notification': 'pn_send', 'whatsapp': 'whatsapp_delivery', 'in-app': 'in_app_impression'}
RESPC = {'email': 'email_click', 'push notification': 'pn_open', 'whatsapp': 'whatsapp_read', 'in-app': 'in_app_click'}
FUENTE_E1 = 'Fuente: Braze, envíos por campaña, mes y canal, enero a septiembre 2026'


def load_b():
    """E1 con columnas b (base de respuesta del canal) y r (respuesta del canal)."""
    d = load()
    d = d[d.canal != 'banner'].copy()
    d['b'] = 0.0
    d['r'] = 0.0
    for c in BASE:
        k = d.canal == c
        d.loc[k, 'b'] = d.loc[k, BASE[c]]
        d.loc[k, 'r'] = d.loc[k, RESPC[c]]
    return d


class Svg:
    def __init__(self, label, w=780, h=420):
        self.o = [f'<svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="{label}" font-family="{FF}">']

    def t(self, x, y, s, size=11.5, fill=TXT, anchor='start', w=400, halo=False, extra=''):
        h = ' stroke="#FFFFFF" stroke-width="4" stroke-linejoin="round" paint-order="stroke"' if halo else ''
        self.o.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{w}"{h}{extra}>{s}</text>')

    def rect(self, x, y, w, h, fill, extra=''):
        self.o.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(0, w):.1f}" height="{max(0, h):.1f}" fill="{fill}"{extra}/>')

    def line(self, x1, y1, x2, y2, stroke=GRID, sw=1, extra=''):
        self.o.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{extra}/>')

    def circle(self, cx, cy, r, fill, extra=' stroke="#FFFFFF" stroke-width="1.5"'):
        self.o.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}"{extra}/>')

    def raw(self, s):
        self.o.append(s)

    def done(self):
        return ''.join(self.o) + '</svg>'


def tw(s, size=11.5, w=400):
    """Ancho aproximado de un texto en Inter (px)."""
    k = 0.56 if w < 600 else 0.6
    return len(s) * size * k


def fmt(v, nd=1):
    s = f'{v:,.{nd}f}'
    return s


def save(n, d):
    d = {'n': n, 'seccion': SECCION, **d}
    p = OUTDIR / f'{n:03d}.json'
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')
    print('escrito', p)
