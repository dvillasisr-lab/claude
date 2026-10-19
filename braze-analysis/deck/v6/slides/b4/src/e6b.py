"""Pares de campañas el mismo día a la misma persona (E6b, 1,000 pares más grandes). Tipo, tema y audiencia del nombre."""
import re, pandas as pd
from kit import D, team, tipo, fam
TEMAS = [
 ('Pruebas y QA', r'^qa|copy of|prueba|test'),
 ('Lanzamiento BillPay', r'billpay|bill_pay|billpayment'),
 ('Hot Sale', r'hotsale|hot_sale|amazon|cuponera'),
 ('Recordatorio de registro', r'veriff|personalinfo|leftfunnel|\bnip\b|-nip|reminderregistro|registrotelefono'),
 ('Tasa 0', r'tasa.?0|tasacero|sinintereses'),
 ('Referidos', r'referral|referid'),
 ('Temporada', r'diapadres|dia.?del|mundial|christmas|navidad|cuestaenero|regresoaclases|buenfin|madres'),
 ('Anota y Gana', r'anotaygana'),
 ('Comercio del día y comercios', r'comercio|merchant|ventaazul|soriana|cashback|promociones'),
 ('Cobranza', r'cobranza|bkt|mora|collection'),
 ('Pagos y desembolso', r'payment|pago|disburs|desembolso|autopay|balance|advance'),
 ('Inactivos y churn', r'inactiv|dormant|churn|neveractive|hardinactive|descuentodirecto'),
 ('Rescate de leads', r'rescate|rezagad|narrativa|valueprop'),
 ('Newsletter', r'newsletter|weekly|recommend'),
]
def tema(n):
    n = str(n).lower()
    for t, p in TEMAS:
        if re.search(p, n): return t
    return 'Otro'
def parts(n):
    s = str(n).split('-')
    if len(s) >= 7 and re.fullmatch(r'\d{8}', s[2]): return dict(tick=s[3], aud=s[5])
    return dict(tick=None, aud=None)
def aud_grupo(n):
    a = (parts(n)['aud'] or '').lower()
    if not a: return 'Sin audiencia en el nombre'
    for k, lab in [('todos', 'Todos'), ('rezagad', 'Leads rezagados'), ('churn', 'Churn'), ('dormant', 'Dormants'), ('inactiv', 'Inactivos y nunca activos'),
                   ('neveractive', 'Inactivos y nunca activos'), ('anonim', 'Anónimos'), ('lead', 'Leads'), ('nuevo', 'Nuevos y registrados'),
                   ('registrad', 'Nuevos y registrados'), ('recurrent', 'Recurrentes y activos'), ('active', 'Recurrentes y activos'),
                   ('cliente', 'Recurrentes y activos'), ('eligib', 'Elegibles')]:
        if k in a: return lab
    return 'Otra: ' + a
def load():
    p = pd.read_csv(D + 'e6b_pares_familias.csv')
    p['ta'] = p.equipo_a.map(team); p['tb'] = p.equipo_b.map(team)
    for s in 'ab':
        f = p['familia_' + s]
        p['ty_' + s] = [tipo(x, t) for x, t in zip(f, p['t' + s])]
        p['tm_' + s] = f.map(tema); p['ag_' + s] = f.map(aud_grupo); p['fam_' + s] = f.map(fam)
        p['tick_' + s] = f.map(lambda n: parts(n)['tick'])
    p['promo2'] = (p.ty_a == 'promocional') & (p.ty_b == 'promocional')
    p['pair'] = [' + '.join(sorted([a, b])) for a, b in zip(p.ta, p.tb)]
    return p
