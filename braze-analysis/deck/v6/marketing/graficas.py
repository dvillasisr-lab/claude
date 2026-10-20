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


AMIGO = [('BillPay_Intro', 'Lanzamiento de BillPay'), ('BKT1', 'Cobranza KCash, primer atraso'), ('Mail-Payment', 'Confirmación de pago KPay'),
         ('ReminderRegistroTelefono', 'Prueba QA: recordatorio de teléfono'), ('RegistradosPay-Tasa0', 'Tasa 0 a registrados de KPay'),
         ('CuestaEnero', 'Cuesta de enero'), ('WeeklyRecommendations', 'Recomendaciones semanales'), ('Cumplea', 'Cumpleaños automático'),
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
