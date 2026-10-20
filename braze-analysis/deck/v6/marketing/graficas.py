"""Gráficas SVG de las láminas propias del deck de Marketing (resumen, manejo de Braze y a quién no deberíamos escribirle).
Datos: E1, E2 y b5_datos.json (bloqueados y bajas, mismas reglas que las láminas 51 y 52)."""
import json, pathlib
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[3]
DATA = ROOT / 'data'
INK, TXT, SEC, GRID = '#0B1220', '#3B4556', '#6B7484', '#DDE2EA'
BLUE, BLUE2, GREEN, G1 = '#1F4FD8', '#8FA8EE', '#127A5B', '#A3AAB5'
FF = 'Inter, system-ui, sans-serif'


class Svg:
    def __init__(self, w, h, label):
        self.o = [f'<svg viewBox="0 0 {w} {h}" width="100%" style="display:block;height:auto;max-height:none" role="img" aria-label="{label}" font-family="{FF}">']

    def t(self, x, y, s, size=12, fill=TXT, anchor='start', w=400):
        self.o.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{w}">{s}</text>')

    def r(self, x, y, w, h, fill, rx=0):
        self.o.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w, 0):.1f}" height="{max(h, 0):.1f}" fill="{fill}" rx="{rx}"/>')

    def l(self, x1, y1, x2, y2, c=GRID, sw=1, extra=''):
        self.o.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{sw}"{extra}/>')

    def c(self, x, y, r, fill):
        self.o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="#FFFFFF" stroke-width="1.5"/>')

    def done(self):
        return ''.join(self.o) + '</svg>'


def equipo(t):
    t = str(t)
    if t.startswith('Marketing'):
        return 'Marketing'
    if t in ('Lending', 'ProductGrowth', 'Product Growth') or t.startswith('ProductoGrowth'):
        return 'Product Growth'
    if t.startswith('Sales'):
        return 'Sales'
    if t.startswith('Collections'):
        return 'Collections'
    return 'Others'


import math, re, hashlib

HA = ROOT / 'hallazgos'
fam = lambda x: re.sub(r'-\d{8,9}-', '-', str(x))


AMIGO = [('BBDDRezagada-RescateTasa0', 'Rescate Tasa 0 a rezagados'), ('HotLeads', 'Rescate Tasa 0 a leads recientes'),
         ('InsigniaAdultosMayores', 'Adultos mayores'), ('MPNeverCash', 'Tasa 0 a KPay sin Cash'), ('NeverActive-InstallmentsNoCash', 'Installments, nunca activó'),
         ('Churn_12Meses', 'Ex clientes KPay 12 meses'), ('HardInactive_6Meses', 'Ex clientes KPay 6 meses'), ('MPTemuCashi', 'Usuarios Temu y Cashi'),
         ('50%descuento', '50 % de descuento'), ('HotSale', 'Hot Sale'), ('Inactivos-DescuentoDirecto', 'Descuento a inactivos'),
         ('InstallmentsSíCash', 'Monto preaprobado Installments'), ('BillPay_Intro', 'Lanzamiento de BillPay'), ('BKT1', 'Cobranza KCash, primer atraso'), ('Mail-Payment', 'Confirmación de pago KPay'),
         ('ReminderRegistroTelefono', 'Prueba QA: recordatorio de teléfono'), ('RegistradosPay-Tasa0', 'Tasa 0 a registrados de KPay'),
         ('CuestaEnero', 'Cuesta de enero'), ('PortafolioActivoEInactivo', 'Comercios a todo el portafolio'), ('WeeklyRecommendations', 'Recomendaciones semanales'), ('Cumplea', 'Cumpleaños automático'),
         ('NarrativaTasa0', 'Tasa 0 a leads rezagados'), ('RescateTasa0', 'Rescate Tasa 0'), ('ReferralProgram', 'Referidos')]


def nice(f, n=40):
    for k, v in AMIGO:
        if k.lower() in str(f).lower():
            return v
    f = re.sub(r'^(Copy of )+', '', str(f))
    p = f.split('-')
    k = next((i for i, x in enumerate(p) if x.upper() in ('CANVAS', 'E', 'PUSH', 'IA', 'CANVA')), None)
    t = ' '.join(p[k + 1:]) if k is not None and k + 1 < len(p) else f
    t = re.sub(r'\bN/?A\b', '', t.replace('_', ' ')).strip()
    return t if len(t) <= n else t[:n - 1] + '…'


def mm(v):
    return f'{v / 1e6:.1f} M' if v >= 1e6 else f'{v / 1e3:.0f} mil' if v >= 1e3 else f'{v:.0f}'


def _jit(key, n=1.0):
    h = int(hashlib.md5(str(key).encode()).hexdigest()[:8], 16)
    return (h / 0xFFFFFFFF - 0.5) * n


def strip(rows, xlab, ticks, lo, hi, w=760, rh=46, lw=200, right=None, label_fmt=None, title=''):
    """Franja de puntos con escala log: rows = [(etiqueta, df con columnas x, s (tamaño), hl (bool), nom)].
    Cada punto es una unidad granular; raya negra = mediana; nombra los casos de 'nom'. right = texto por fila."""
    rw = 150 if right else 20
    H = 30 + rh * len(rows) + 38
    S = Svg(w, H, title)
    X0, X1 = lw, w - rw
    sx = lambda v: X0 + (X1 - X0) * (math.log10(max(v, lo)) - math.log10(lo)) / (math.log10(hi) - math.log10(lo))
    Y0 = 26
    for t in ticks:
        S.l(sx(t), Y0, sx(t), Y0 + rh * len(rows), GRID); S.t(sx(t), Y0 + rh * len(rows) + 16, label_fmt(t) if label_fmt else f'{t:,}', 11, SEC, 'middle')
    S.t(X1, Y0 + rh * len(rows) + 31, xlab, 10.5, SEC, 'end')
    if right:
        S.t(w - 4, 16, right[0], 10.5, SEC, 'end', 600)
    for i, (lab, d) in enumerate(rows):
        yc = Y0 + rh * i + rh / 2
        if i:
            S.l(X0 - 190, Y0 + rh * i, w, Y0 + rh * i, '#EEF1F5')
        S.t(X0 - 12, yc + 4, lab, 12, INK, 'end', 600)
        smax = d.s.max() if len(d) else 1
        for r in d.sort_values('s', ascending=False).itertuples():
            rr = 2.2 + 6.5 * math.sqrt(r.s / smax)
            S.o.append(f'<circle cx="{sx(r.x):.1f}" cy="{yc + _jit(r.Index, rh * 0.62):.1f}" r="{rr:.1f}" fill="{BLUE if r.hl else G1}" '
                       f'fill-opacity="{0.85 if r.hl else 0.55}" stroke="#FFFFFF" stroke-width="0.8"/>')
        if len(d):
            m = d.x.median()
            S.l(sx(m), yc - rh * 0.4, sx(m), yc + rh * 0.4, INK, 2.2)
        for r in d[d.nom.astype(bool)].itertuples():
            x = sx(r.x)
            anc = 'end' if x > X0 + (X1 - X0) * 0.6 else 'start'
            S.o.append(f'<text x="{x + (-8 if anc == "end" else 8):.1f}" y="{yc - rh * 0.3:.1f}" font-size="10.5" fill="{INK}" text-anchor="{anc}" '
                       f'font-weight="700" stroke="#FFFFFF" stroke-width="3.5" stroke-linejoin="round" paint-order="stroke">{r.nom}</text>')
        if right:
            S.t(w - 4, yc + 4, right[1][i], 11, INK, 'end', 600)
    return S.done()


def costo_campanas():
    """Lámina 2: cada punto es una campaña (todas sus versiones y canales) con 20 mil MXN o más de gasto;
    x = MXN por conversión (crédito otorgado en 7 días); una fila por equipo; raya = mediana."""
    import sys
    sys.path.insert(0, str(ROOT / 'deck' / 'v6' / 'slides' / 'b2' / 'src'))
    from b2base import load_b
    d = load_b()
    g = d.groupby('fam').agg(c=('costo', 'sum'), v=('conversiones_fraccional', 'sum'), equ=('equipo', 'first')).reset_index()
    g = g[(g.c >= 20000) & (g.v >= 1)].copy()
    g['x'] = g.c / g.v; g['s'] = g.c; g['hl'] = g.equ == 'Marketing'
    NOM = {'Marketing-KCash-B0171-CANVAS-Leads_BBDDRezagada-NarrativaTasa0-N/A': 'Tasa 0 a leads rezagados',
           'Lending-KCash-B0223-CANVAS-Nuevos_NeverActive-InstallmentsNoCash-N/A': 'Installments a quien nunca activó'}
    g['nom'] = g.fam.map(lambda f: NOM.get(f, ''))
    for f in NOM:
        if f in set(g.fam):
            r = g[g.fam == f].iloc[0]; g.loc[g.fam == f, 'nom'] = f'{NOM[f]}: {r.x:,.0f}'
    orden = ['Marketing', 'Product Growth', 'Sales', 'Others', 'Collections']
    rows, right = [], []
    for e in orden:
        q = g[g.equ == e].set_index('fam')
        rows.append((e, q)); right.append(f'{len(q)} · mediana {q.x.median():,.0f}')
    svg = strip(rows, 'MXN por conversión (crédito otorgado en 7 días), escala que crece por múltiplos', [1, 3, 10, 30, 100, 300, 1000, 3000],
                1, 6000, rh=44, lw=130, right=('Campañas · mediana MXN', right),
                title='Cada punto es una campaña con 20 mil MXN o más de gasto: MXN por conversión, por equipo; raya = mediana; tamaño = gasto')
    return svg, g


def higiene():
    """Lámina 12: cada punto es una comunicación que mandó algo en 2026; x = mensajes del año; una fila por problema de
    orden en Braze (una comunicación puede estar en varias). A la derecha, cuántas y qué parte de los mensajes."""
    c = pd.read_csv(DATA / 'e2_catalogo.csv')
    e = pd.read_csv(DATA / 'e1_comunicacion_mes_canal.csv')
    v = e.groupby('communication_id').envios.sum()
    sep = set(e[(e.envios > 0) & e.mes.str.startswith('2026-09')].communication_id)
    c['x'] = c.communication_id.map(v).fillna(0)
    c = c[c.x > 0].copy()
    c['s'] = c.x
    f15 = pd.read_csv(DATA / 'e15_embudo_pasos.csv')
    pasos = f15.groupby('canvas_id').canvas_step_id.nunique()
    t = c.ticket_number.astype(str)
    n = c.nombre.astype(str)
    crit = [('Equipo "Not Tracked"', c.team.astype(str).eq('Not Tracked')),
            ('Sin ticket o ticket comodín', t.str.fullmatch(r'[BT]0+|Not Tracked|nan|N/A|NA', case=False) | (c.tiene_ticket == 0)),
            ('Nombre fuera de la convención', c.nombre_sigue_convencion == 0),
            ('Nombre de prueba o copia', n.str.lower().str.contains(r'copy of|test|prueba|qa[_ -]|^qa|demo')),
            ('Archivada y mandó en septiembre', c.archived.astype(bool) & c.communication_id.isin(sep)),
            ('Canvas con 20 pasos o más', c.communication_id.map(pasos).fillna(0) >= 20)]
    tot = c.x.sum()
    rows, right = [], []
    malo = pd.Series(False, index=c.index)
    usados = set()
    for lab, m in crit:
        q = c[m].copy(); malo |= m
        q['hl'] = True
        q['nom'] = ''
        top = q[~q.nombre.map(lambda z: nice(fam(z))).isin(usados)].sort_values('x', ascending=False).head(1)
        if len(top):
            nm = nice(fam(top.nombre.iloc[0]), 34); usados.add(nice(fam(top.nombre.iloc[0])))
            q.loc[top.index, 'nom'] = f'{nm}: {mm(top.x.iloc[0])}'
        rows.append((lab, q)); right.append(f'{len(q):,} · {100 * q.x.sum() / tot:.0f} % de los mensajes')
    ok = c[~malo].copy(); ok['hl'] = False; ok['nom'] = ''
    rows.append(('En orden', ok)); right.append(f'{len(ok):,} · {100 * ok.x.sum() / tot:.0f} % de los mensajes')
    svg = strip(rows, 'Mensajes de la comunicación en 2026, escala que crece por múltiplos', [100, 1000, 10000, 100000, 1000000, 10000000],
                30, 4e7, rh=36, lw=210, right=('Comunicaciones · parte de los mensajes', right),
                label_fmt=lambda t: {100: '100', 1000: '1 mil', 10000: '10 mil', 100000: '100 mil', 1000000: '1 M', 10000000: '10 M'}[t],
                title='Cada punto es una comunicación que mandó algo en 2026, por problema de orden; tamaño = mensajes; raya = mediana')
    return svg, dict(n=len(c), ok=len(ok), ok_pct=100 * ok.x.sum() / tot)


def no_deberiamos():
    """Lámina 13: cada punto es una campaña que mandó promociones a un grupo que no debería recibirlas; x = mensajes a ese grupo;
    azul = Marketing; una fila por grupo; raya = mediana."""
    tipo = pd.read_csv(HA / 'muestra_c_familias.csv').groupby('familia').tipo.first()
    a = pd.read_csv(DATA / 'e7a_familia_canal_etapa.csv')
    a['familia'] = a.familia.fillna('(sin nombre)').map(fam)
    a['tipo'] = a.familia.map(tipo)
    a = a[a.tipo == 'promocional o lifecycle']
    b = pd.read_csv(DATA / 'e5b_comms_despues_baja.csv')
    b['familia'] = b.familia.map(fam); b['tipo'] = b.familia.map(tipo)
    b = b[b.tipo == 'promocional o lifecycle']
    eqf = lambda f: equipo(re.sub(r'^Copy of ', '', f).split('-')[0].replace('Lending', 'Product Growth'))
    grupos = []
    for lab, et in (('KPay congelado', '4.Kpay CC Freeze'), ('REUS o ARCO', '6.Reus or Arco'), ('Lista negra', '3.Blacklist')):
        q = a[a.etapa == et].groupby('familia').envios.sum().reset_index().rename(columns={'envios': 'x'})
        grupos.append((lab, q))
    q = b.groupby('familia').emails_despues_de_baja.sum().reset_index().rename(columns={'emails_despues_de_baja': 'x'})
    grupos.append(('Ya dados de baja del correo', q))
    NOMS = {'Marketing-KCash-B0171-CANVAS-Leads_BBDDRezagada-RescateTasa0-N/A': 'Rescate Tasa 0 a rezagados',
            'Marketing-KCash-B0326-Canvas-Leads-ReferralProgram-N/A': 'Referidos a leads',
            'Marketing-KPay-B0326-Canvas-Recurrentes_Dormants-ReferralProgram-N/A': 'Referidos KPay a ex clientes'}
    rows, right = [], []
    for lab, q in grupos:
        q = q[q.x > 0].copy()
        q['equ'] = q.familia.map(eqf); q['hl'] = q.equ == 'Marketing'; q['s'] = q.x
        top = q.sort_values('x', ascending=False).head(1)
        q['nom'] = ''
        if len(top):
            f = top.familia.iloc[0]
            nm = NOMS.get(f, nice(f, 30))
            q.loc[top.index, 'nom'] = f'{nm} ({top.equ.iloc[0]}): {mm(top.x.iloc[0])}'
        mk = q[q.hl].x.sum() / q.x.sum() * 100 if q.x.sum() else 0
        rows.append((lab, q.set_index('familia'))); right.append(f'{len(q)} · Marketing {mk:.0f} %')
    svg = strip(rows, 'Promociones de la campaña a ese grupo en nueve meses, escala que crece por múltiplos', [10, 100, 1000, 10000, 100000, 1000000, 10000000],
                5, 2e7, rh=46, lw=190, right=('Campañas · parte de Marketing', right),
                label_fmt=lambda t: {10: '10', 100: '100', 1000: '1 mil', 10000: '10 mil', 100000: '100 mil', 1000000: '1 M', 10000000: '10 M'}[t],
                title='Cada punto es una campaña que mandó promociones a un grupo que no debería recibirlas; azul = Marketing; raya = mediana')
    return svg


if __name__ == '__main__':
    print(costo_campanas()[1].groupby('equ').x.median().round(0))
    print(higiene()[1])


def _log(v, lo, hi, a, b):
    return a + (b - a) * (math.log10(max(v, lo)) - math.log10(lo)) / (math.log10(hi) - math.log10(lo))


def costo_dispersion():
    """Lámina 2: cada punto es una campaña con 20 mil MXN o más de gasto; x = gasto en nueve meses, y = MXN por conversión
    (crédito otorgado en 7 días). Azul = Marketing. Recta en escala log y R²; rayas = mediana de Marketing y del resto."""
    import numpy as np
    _, g = costo_campanas()
    W, H = 640, 256
    X0, X1, Y0, Y1 = 58, 620, 34, 214
    sx = lambda v: _log(v, 2e4, 6e6, X0, X1)
    sy = lambda v: _log(v, 1, 1e4, Y1, Y0)
    S = Svg(W, H, 'Cada punto es una campaña: gasto contra MXN por conversión; azul = Marketing; recta y R²')
    S.c(X1 - 196, 12, 5, BLUE); S.t(X1 - 186, 16, 'Marketing', 12, INK, w=600)
    S.c(X1 - 92, 12, 5, G1); S.t(X1 - 82, 16, 'Otros equipos', 12, TXT)
    for v, l in ((1, '1'), (10, '10'), (100, '100'), (1000, '1,000'), (10000, '10,000')):
        S.l(X0, sy(v), X1, sy(v), GRID); S.t(X0 - 6, sy(v) + 4, l, 11, SEC, 'end')
    for v, l in ((2e4, '20 mil'), (1e5, '100 mil'), (1e6, '1 M'), (5e6, '5 M')):
        S.l(sx(v), Y0, sx(v), Y1, GRID); S.t(sx(v), Y1 + 16, l, 11, SEC, 'middle')
    S.t(X1, Y1 + 34, 'Gasto de la campaña en nueve meses, MXN (escala que crece por múltiplos)', 10.5, SEC, 'end')
    S.t(X0 - 50, 16, 'MXN por conversión', 10.5, SEC)
    for r in g.sort_values('hl').itertuples():
        S.o.append(f'<circle cx="{sx(r.s):.1f}" cy="{sy(r.x):.1f}" r="{4.2 if r.hl else 3.4}" fill="{BLUE if r.hl else G1}" '
                   f'fill-opacity="{0.85 if r.hl else 0.6}" stroke="#FFFFFF" stroke-width="0.8"/>')
    lx, ly = np.log10(g.s), np.log10(g.x)
    b, a = np.polyfit(lx, ly, 1)
    r2 = np.corrcoef(lx, ly)[0, 1] ** 2
    S.l(sx(2e4), sy(10 ** (a + b * math.log10(2e4))), sx(6e6), sy(10 ** (a + b * math.log10(6e6))), INK, 1.4, ' stroke-dasharray="5 4"')
    S.t(X1 - 4, Y0 + 14, f'Recta: R² = {r2:.2f}, gastar más no abarata', 11, INK, 'end', 600)
    for lab, m, col in (('Mediana Marketing', g[g.hl].x.median(), BLUE), ('Mediana del resto', g[~g.hl].x.median(), SEC)):
        S.l(X0, sy(m), X1, sy(m), col, 1.2, ' stroke-dasharray="2 3"')
        S.o.append(f'<text x="{X1 - 4:.1f}" y="{sy(m) + (-5 if col == BLUE else 13):.1f}" font-size="10.5" font-weight="700" fill="{col}" text-anchor="end" '
                   f'stroke="#FFFFFF" stroke-width="3.5" stroke-linejoin="round" paint-order="stroke">{lab}: {m:,.0f}</text>')
    NOMS = {'Marketing-KCash-B0171-CANVAS-Leads_BBDDRezagada-NarrativaTasa0-N/A': 'Tasa 0 a leads rezagados',
            'Lending-KCash-B0223-CANVAS-Nuevos_NeverActive-InstallmentsNoCash-N/A': 'Installments a quien nunca activó',
            'Marketing-KCash-B0000-CANVAS-Leads_LeftFunnel-Retargeting_Veriff': 'Recordatorio de registro',
            'Marketing-KCash-B0326-Canvas-Recurrentes_ClienteKCashCompraKCash-ReferralProgram-N/A': 'Referidos a clientes KCash'}
    for f, nm in NOMS.items():
        q = g[g.fam == f]
        if len(q):
            r = q.iloc[0]; x, y = sx(r.s), sy(r.x)
            anc = 'end' if x > X0 + (X1 - X0) * 0.55 else 'start'
            S.o.append(f'<text x="{x + (-9 if anc == "end" else 9):.1f}" y="{y + 4:.1f}" font-size="10.5" font-weight="700" fill="{INK}" '
                       f'text-anchor="{anc}" stroke="#FFFFFF" stroke-width="3.5" stroke-linejoin="round" paint-order="stroke">{nm}: {r.x:,.0f}</text>')
    return S.done(), dict(r2=r2, mk=g[g.hl].x.median(), resto=g[~g.hl].x.median())


def pareto_no_deberiamos():
    """Lámina 13: campañas ordenadas por las promociones que mandaron a los cuatro grupos (KPay congelado, REUS o ARCO,
    lista negra, dados de baja del correo); acumulado de esas promociones. Cada punto es una campaña; azul = Marketing."""
    tipo = pd.read_csv(HA / 'muestra_c_familias.csv').groupby('familia').tipo.first()
    a = pd.read_csv(DATA / 'e7a_familia_canal_etapa.csv')
    a['familia'] = a.familia.fillna('(sin nombre)').map(fam)
    a = a[(a.familia.map(tipo) == 'promocional o lifecycle') & a.etapa.isin(['4.Kpay CC Freeze', '6.Reus or Arco', '3.Blacklist'])]
    b = pd.read_csv(DATA / 'e5b_comms_despues_baja.csv')
    b['familia'] = b.familia.map(fam)
    b = b[b.familia.map(tipo) == 'promocional o lifecycle']
    t = pd.concat([a.groupby('familia').envios.sum(), b.groupby('familia').emails_despues_de_baja.sum()]).groupby(level=0).sum()
    t = t[t > 0].sort_values(ascending=False)
    eqf = lambda f: equipo(re.sub(r'^Copy of ', '', f).split('-')[0].replace('Lending', 'Product Growth'))
    cum = 100 * t.cumsum() / t.sum()
    N = len(t)
    W, H = 640, 226
    X0, X1, Y0, Y1 = 50, 620, 30, 186
    sx = lambda r: _log(r, 1, N, X0, X1)
    sy = lambda v: Y1 - (Y1 - Y0) * v / 100
    S = Svg(W, H, 'Campañas ordenadas por promociones a quien no debería recibirlas: acumulado; azul = Marketing')
    S.c(X1 - 196, 12, 5, BLUE); S.t(X1 - 186, 16, 'Marketing', 12, INK, w=600)
    S.c(X1 - 92, 12, 5, G1); S.t(X1 - 82, 16, 'Otros equipos', 12, TXT)
    for v in (0, 25, 50, 75, 100):
        S.l(X0, sy(v), X1, sy(v), GRID); S.t(X0 - 6, sy(v) + 4, f'{v} %', 11, SEC, 'end')
    for r in (1, 3, 10, 30, 100, 300):
        if r <= N:
            S.l(sx(r), Y1, sx(r), Y1 + 4, G1); S.t(sx(r), Y1 + 16, f'{r}', 11, SEC, 'middle')
    S.t(X1, Y1 + 34, f'Campañas, de la que más mandó a la que menos ({N}; escala que crece por múltiplos)', 10.5, SEC, 'end')
    pts = ' '.join(f'{sx(i + 1):.1f},{sy(v):.1f}' for i, v in enumerate(cum))
    S.o.append(f'<polyline points="{pts}" fill="none" stroke="{INK}" stroke-width="1.4"/>')
    for i, (f, v) in enumerate(cum.items()):
        mk = eqf(f) == 'Marketing'
        S.o.append(f'<circle cx="{sx(i + 1):.1f}" cy="{sy(v):.1f}" r="{4.6 if i < 10 else 2.6}" fill="{BLUE if mk else G1}" stroke="#FFFFFF" stroke-width="0.8"/>')
    k = 10
    S.l(sx(k), sy(0), sx(k), sy(cum.iloc[k - 1]), INK, 1, ' stroke-dasharray="3 3"')
    S.t(sx(k) + 8, sy(cum.iloc[k - 1]) + 4, f'10 campañas: {cum.iloc[k - 1]:.0f} %', 12, INK, 'start', 700)
    for i in range(3):
        f = t.index[i]
        nm = {'Marketing-KPay-B0326-Canvas-Recurrentes_Dormants-ReferralProgram-N/A': 'Referidos KPay a ex clientes'}.get(f, nice(f, 32))
        S.t(X0 + 10, Y0 + 14 + i * 16, f'{i + 1}. {nm} ({eqf(f)}): {mm(t.iloc[i])}', 10.5, INK, 'start', 600)
        S.t(sx(i + 1), sy(cum.iloc[i]) - 8, f'{i + 1}', 10, INK, 'middle', 700)
    mkp = 100 * t[[eqf(f) == 'Marketing' for f in t.index]].sum() / t.sum()
    return S.done(), dict(n=N, top10=cum.iloc[k - 1], mk=mkp)


def pareto_marketing():
    """Lámina 2: campañas de Marketing ordenadas por gasto; acumulado del gasto (azul) y de las conversiones (verde).
    La distancia entre las dos curvas es dinero que no trae conversiones."""
    import sys
    sys.path.insert(0, str(ROOT / 'deck' / 'v6' / 'slides' / 'b2' / 'src'))
    from b2base import load_b
    d = load_b()
    m = d[d.equipo == 'Marketing']
    g = m.groupby('fam').agg(c=('costo', 'sum'), v=('conversiones_fraccional', 'sum')).sort_values('c', ascending=False)
    g = g[g.c > 0]
    cc = (100 * g.c.cumsum() / g.c.sum()).tolist(); cv = (100 * g.v.cumsum() / g.v.sum()).tolist()
    N = len(g)
    W, H = 640, 256
    X0, X1, Y0, Y1 = 50, 620, 34, 214
    sx = lambda r: _log(r, 1, N, X0, X1)
    sy = lambda v: Y1 - (Y1 - Y0) * v / 100
    S = Svg(W, H, 'Campañas de Marketing ordenadas por gasto: acumulado del gasto y de las conversiones')
    S.l(X1 - 250, 12, X1 - 230, 12, BLUE, 3); S.t(X1 - 224, 16, 'Gasto acumulado', 12, INK, w=600)
    S.l(X1 - 100, 12, X1 - 80, 12, GREEN, 3); S.t(X1 - 74, 16, 'Conversiones', 12, INK, w=600)
    for v in (0, 25, 50, 75, 100):
        S.l(X0, sy(v), X1, sy(v), GRID); S.t(X0 - 6, sy(v) + 4, f'{v} %', 11, SEC, 'end')
    for r in (1, 3, 10, 30, 100, 200):
        if r <= N:
            S.l(sx(r), Y1, sx(r), Y1 + 4, G1); S.t(sx(r), Y1 + 16, f'{r}', 11, SEC, 'middle')
    S.t(X1, Y1 + 34, f'Campañas de Marketing, de la que más gasta a la que menos ({N}; escala que crece por múltiplos)', 10.5, SEC, 'end')
    pa = ' '.join(f'{sx(i + 1):.1f},{sy(v):.1f}' for i, v in enumerate(cc))
    pb = ' '.join(f'{sx(i + 1):.1f},{sy(v):.1f}' for i, v in reversed(list(enumerate(cv))))
    S.o.append(f'<polygon points="{pa} {pb}" fill="{BLUE}" fill-opacity="0.10"/>')
    S.o.append(f'<polyline points="{pa}" fill="none" stroke="{BLUE}" stroke-width="3"/>')
    S.o.append(f'<polyline points="{" ".join(f"{sx(i + 1):.1f},{sy(v):.1f}" for i, v in enumerate(cv))}" fill="none" stroke="{GREEN}" stroke-width="3"/>')
    k = 5
    S.l(sx(k), sy(cv[k - 1]), sx(k), sy(cc[k - 1]), INK, 1.2, ' stroke-dasharray="3 3"')
    S.o.append(f'<text x="{sx(k) - 8:.1f}" y="{sy(cc[k - 1]) - 8:.1f}" font-size="11.5" font-weight="700" fill="{BLUE}" text-anchor="end" '
               f'stroke="#FFFFFF" stroke-width="3.5" stroke-linejoin="round" paint-order="stroke">5 campañas: {cc[k - 1]:.0f} % del gasto</text>')
    S.t(sx(k) + 8, sy(cv[k - 1]) + 14, f'y {cv[k - 1]:.0f} % de las conversiones', 11.5, GREEN, 'start', 700)
    S.t(X0 + 10, Y0 + 14, f'1. Tasa 0 a leads rezagados: {cc[0]:.0f} % del gasto, {cv[0]:.1f} % de las conversiones', 10.5, INK, 'start', 600)
    return S.done(), dict(n=N, k5=(cc[4], cv[4]), k10=(cc[9], cv[9]), top=(cc[0], cv[0]))


def mapa_versiones(n=13):
    """Lámina 12: las campañas con más versiones, una fila cada una; cada celda es un mes. Tono = versiones que mandaron ese mes;
    contorno azul = ese mes se estrenó una versión nueva. Muestra que se copia en vez de medir."""
    e = pd.read_csv(DATA / 'e1_comunicacion_mes_canal.csv')
    c = pd.read_csv(DATA / 'e2_catalogo.csv')
    e = e[e.envios > 0].copy()
    e['f'] = e.communication_name.map(fam); e['m'] = e.mes.str[:7]
    cr = c.set_index('communication_id').created_at.astype(str).str[:7]
    tot = e.groupby('f').communication_id.nunique().sort_values(ascending=False).head(n)
    meses = [f'2026-{i:02d}' for i in range(1, 10)]
    MES = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep']
    W, rh = 640, 16
    H = 40 + rh * n + 26
    LW = 260
    cw = (W - LW - 70) / 9
    S = Svg(W, H, 'Las campañas con más versiones: una fila por campaña, una celda por mes; tono = versiones que mandaron ese mes')
    for j, mm_ in enumerate(MES):
        S.t(LW + j * cw + cw / 2, 30, mm_, 11, SEC, 'middle')
    S.t(W - 4, 30, 'Versiones', 11, SEC, 'end', 600)
    tonos = {0: '#F1F3F7', 1: '#C9D6F7', 2: '#8FA8EE', 3: '#4F74E0'}
    for i, (f, nv) in enumerate(tot.items()):
        y = 38 + i * rh
        eq = equipo(re.sub(r'^Copy of ', '', f).split('-')[0].replace('Lending', 'Product Growth'))
        S.t(LW - 10, y + 12, f'{nice(f, 26)} · {eq}', 10.5, INK if eq == 'Marketing' else TXT, 'end', 700 if eq == 'Marketing' else 400)
        q = e[e.f == f]
        for j, m_ in enumerate(meses):
            ids = q[q.m == m_].communication_id.unique()
            k = len(ids)
            fill = tonos.get(min(k, 3), '#1F4FD8') if k < 4 else BLUE
            x = LW + j * cw
            S.r(x + 1.5, y + 1.5, cw - 3, rh - 3, fill, 2)
            if any(cr.get(x_) == m_ for x_ in ids):
                S.o.append(f'<rect x="{x + 1.5:.1f}" y="{y + 1.5:.1f}" width="{cw - 3:.1f}" height="{rh - 3:.1f}" rx="2" fill="none" stroke="{INK}" stroke-width="1.6"/>')
        S.t(W - 4, y + 12, f'{nv}', 11, INK, 'end', 700)
    yl = 38 + n * rh + 16
    lx = LW
    for k, lab in ((1, '1 versión'), (2, '2'), (3, '3 o más')):
        S.r(lx, yl - 9, 14, 11, tonos[k], 2); S.t(lx + 18, yl, lab, 10.5, SEC); lx += 30 + len(lab) * 6
    S.o.append(f'<rect x="{lx + 10:.1f}" y="{yl - 9:.1f}" width="14" height="11" rx="2" fill="none" stroke="{INK}" stroke-width="1.6"/>')
    S.t(lx + 30, yl, 'versión nueva ese mes', 10.5, SEC)
    return S.done()


def barras_no_deberiamos(k=30):
    """Lámina 13: las 30 campañas que más promociones mandaron a quien no debía recibirlas (barras, azul = Marketing) y,
    encima, el acumulado sobre las 502 campañas (línea)."""
    tipo = pd.read_csv(HA / 'muestra_c_familias.csv').groupby('familia').tipo.first()
    a = pd.read_csv(DATA / 'e7a_familia_canal_etapa.csv')
    a['familia'] = a.familia.fillna('(sin nombre)').map(fam)
    a = a[(a.familia.map(tipo) == 'promocional o lifecycle') & a.etapa.isin(['4.Kpay CC Freeze', '6.Reus or Arco', '3.Blacklist'])]
    b = pd.read_csv(DATA / 'e5b_comms_despues_baja.csv')
    b['familia'] = b.familia.map(fam)
    b = b[b.familia.map(tipo) == 'promocional o lifecycle']
    t = pd.concat([a.groupby('familia').envios.sum(), b.groupby('familia').emails_despues_de_baja.sum()]).groupby(level=0).sum()
    t = t[t > 0].sort_values(ascending=False)
    eqf = lambda f: equipo(re.sub(r'^Copy of ', '', f).split('-')[0].replace('Lending', 'Product Growth'))
    cum = 100 * t.cumsum() / t.sum()
    W, H = 640, 236
    X0, X1, Y0, Y1 = 50, 590, 34, 196
    bw = (X1 - X0) / k
    vmax = t.iloc[0]
    sy = lambda v: Y1 - (Y1 - Y0) * v / vmax
    sp = lambda p: Y1 - (Y1 - Y0) * p / 50
    S = Svg(W, H, f'Las {k} campañas que más promociones mandaron a quien no debía recibirlas; línea = acumulado sobre todas')
    S.r(X1 - 330, 7, 12, 11, BLUE, 2); S.t(X1 - 314, 16, 'Marketing', 12, INK, w=600)
    S.r(X1 - 236, 7, 12, 11, G1, 2); S.t(X1 - 220, 16, 'Otros equipos', 12, TXT)
    S.l(X1 - 116, 12, X1 - 96, 12, INK, 2); S.t(X1 - 90, 16, 'Acumulado', 12, INK, w=600)
    for v in (0, 1e6, 2e6, 3e6):
        if v <= vmax:
            S.l(X0, sy(v), X1, sy(v), GRID); S.t(X0 - 6, sy(v) + 4, mm(v) if v else '0', 11, SEC, 'end')
    for p in (10, 20, 30, 40, 50):
        S.t(X1 + 6, sp(p) + 4, f'{p} %', 10.5, SEC)
    for i, (f, v) in enumerate(t.head(k).items()):
        S.r(X0 + i * bw + 2, sy(v), bw - 4, Y1 - sy(v), BLUE if eqf(f) == 'Marketing' else G1, 2)
    pts = ' '.join(f'{X0 + i * bw + bw / 2:.1f},{sp(cum.iloc[i]):.1f}' for i in range(k))
    S.o.append(f'<polyline points="{pts}" fill="none" stroke="{INK}" stroke-width="2"/>')
    S.t(X0 + (k - 1) * bw + bw / 2, sp(cum.iloc[k - 1]) - 8, f'{k} de {len(t)} campañas: {cum.iloc[k - 1]:.0f} %', 11.5, INK, 'end', 700)
    S.t(X0, Y1 + 18, f'Campañas, de la que más mandó a la que menos (las {k} primeras de {len(t)})', 10.5, SEC)
    for i in range(3):
        f = t.index[i]
        nm = {'Marketing-KPay-B0326-Canvas-Recurrentes_Dormants-ReferralProgram-N/A': 'Referidos KPay a ex clientes'}.get(f, nice(f, 30))
        S.t(X0 + 3 * bw + 8, Y0 + 14 + i * 15, f'{i + 1}. {nm} ({eqf(f)}): {mm(t.iloc[i])}', 10.5, INK, 'start', 600)
        S.t(X0 + i * bw + bw / 2, sy(t.iloc[i]) - 4, f'{i + 1}', 10, INK, 'middle', 700)
    return S.done(), dict(n=len(t), cumk=cum.iloc[k - 1])
