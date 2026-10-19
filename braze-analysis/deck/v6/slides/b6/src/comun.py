"""Base común del bloque b6 (láminas 56 a 65, sección VII: comportamiento del usuario).
Lee solo CSV del repo (data/ y hallazgos/). Paleta, ayudante de SVG y escritura del JSON de cada lámina.
Costo: email 0.05 MXN por enviado, WhatsApp 1.00 MXN por entregado, push e in-app 0."""
import json, math, pathlib, re, sys
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


def por_campana(e, canales=('email', 'push notification', 'whatsapp', 'in-app')):
    """Una fila por campaña (familia sin fecha) y canal: envíos, base, respuesta, bajas, personas aproximadas."""
    x = e[e.canal.isin(canales)].copy()
    x['b'] = np.select([x.canal.eq(c) for c in RESP], [x[RESP[c][0]] for c in RESP], 0)
    x['r'] = np.select([x.canal.eq(c) for c in RESP], [x[RESP[c][1]] for c in RESP], 0)
    g = x.groupby(['familia', 'canal']).agg(env=('envios', 'sum'), b=('b', 'sum'), r=('r', 'sum'), u=('email_unsubscribe', 'sum'),
                                             dl=('email_delivery', 'sum'), usr=('usuarios_aprox', 'sum'), costo=('costo', 'sum'),
                                             equipo=('equipo', 'first'), grupo=('grupo', 'first'), tipo=('tipo', 'first')).reset_index()
    g['resp'] = 100 * g.r / g.b.replace(0, np.nan)
    g['baja'] = 1000 * g.u / g.dl.replace(0, np.nan)
    return g


def recta(x, y, w=None):
    """Mínimos cuadrados y R²."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    b, a = np.polyfit(x, y, 1, w=None if w is None else np.sqrt(w))
    yh = a + b * x; r2 = 1 - ((y - yh) ** 2).sum() / ((y - y.mean()) ** 2).sum()
    return a, b, r2


def logmap(v0, v1, p0, p1):
    """Escala logarítmica de [v0, v1] a [p0, p1]."""
    a, b = math.log10(v0), math.log10(v1)
    return lambda v: p0 + (p1 - p0) * (math.log10(min(max(v, v0), v1)) - a) / (b - a)


def fmt(v):
    return f'{v:g}' if v >= 1 else f'{v:.2g}'


NOMBRES = [(r'BillPay_Intro', 'Lanzamiento BillPay'), (r'LeftFunnel-Retargeting_Veriff', 'Verificar identidad'),
           (r'LeftFunnel-Retargeting_PersonalInfo', 'Completar datos'), (r'LeftFunnel-Retargeting_NIP$', 'Poner NIP'),
           (r'AccountCreation', 'Crear cuenta KPay'), (r'NIPconCupon', 'NIP con cupón KPay'),
           (r'B0211-CANVAS-Nuevos_RegistradosPay', 'Tasa 0 a registrados'), (r'B0171-CANVAS-Anonimos-RescateTasa0', 'Rescate Tasa 0 a anónimos'),
           (r'B0171-CANVAS-Leads_BBDDRezagada-NarrativaTasa0', 'Tasa 0 a leads rezagados'),
           (r'B0171-CANVAS-Leads_BBDDRezagada-RescateTasa0', 'Rescate Tasa 0 a rezagados'),
           (r'Lending-KCash-B0301-CANVAS-Active-Retargeting_Installments', 'Pagar compra a meses'),
           (r'Marketing-KCash-B0301-CANVAS-Active-NuevosRetargeting', 'Compra a meses a nuevos'),
           (r'KCash-B0326-Canvas-Leads-ReferralProgram', 'Referidos a leads'), (r'KCash-B0326-Canvas-Recurrentes_Dormants', 'Referidos a dormants'),
           (r'B0223', 'Meses a quien nunca activó'), (r'B0209', 'Descuento a inactivos'), (r'B0333', 'Recuperar churn 12 meses'),
           (r'Payment-Confirmation', 'Confirmación de pago'), (r'Collections-KCash-T000-CANVAS-BKT1', 'Cobranza BKT1'),
           (r'FraudRisk', 'Rechazo por fraude'), (r'B0335', 'Promos de comercios'), (r'B0337', 'Cuesta de enero'),
           (r'B0440', 'AnotayGana'), (r'B0312', 'Navidad a elegibles'), (r'Payment Received', 'Pago recibido'),
           (r'Sales-KPay-B0585-CANVAS-Recurrentes-Comerciodeldia', 'Comercio del día (Sales)'),
           (r'Marketing-KPay-B0561-CANVAS-Leads-Comerciodeldia', 'Comercio del día a leads')]


def nombre(f):
    for rx, n in NOMBRES:
        if re.search(rx, str(f)): return n
    return None


def etiqueta(s, x, y, txt, dx, dy, anchor='start', sub=None, col=INK):
    """Nombre sobre la gráfica con línea guía corta al punto."""
    tx, ty = x + dx, y + dy
    if abs(dx) > 8 or abs(dy) > 10:
        s.line(x, y, tx - (3 if anchor == 'start' else -3 if anchor == 'end' else 0), ty - 4, M1, 0.8)
    s.t(tx, ty, txt, 11, col, anchor, 600, halo=True)
    if sub: s.t(tx, ty + 12, sub, 10.5, SEC, anchor, halo=True)
