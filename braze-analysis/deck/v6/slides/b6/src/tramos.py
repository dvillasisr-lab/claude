"""Gráfica común de las láminas 59 y 60 (E8, muestra L): cuándo se da de baja del email cada cohorte y con qué campaña.
Arriba: personas que se dieron de baja por tramo de días desde su primer correo, con los correos que habían recibido (promedio).
Abajo: por equipo y tramo, bajas de las campañas que llegaron el día de la baja; cada campaña va al tramo de su mediana de días."""
from comun import *

TRAMOS = [('0 mismo día', 'Mismo día', 0, 0), ('1 a 7', '1 a 7 días', 1, 7), ('08 a 30', '8 a 30', 8, 30), ('31 a 90', '31 a 90', 31, 90),
          ('91 a 180', '91 a 180', 91, 180), ('181+', 'Más de 180', 181, 9999)]
CORTO = [(r'BillPay', 'Lanzamiento BillPay'), (r'Retargeting_Veriff', 'Verificar identidad'), (r'PersonalInfo', 'Completar datos'),
         (r'Retargeting_NIP$', 'Poner NIP'), (r'NIPconCupon', 'NIP con cupón'), (r'AccountCreation', 'Crear cuenta KPay'),
         (r'B0211', 'Tasa 0 a registrados'), (r'FraudRisk', 'Rechazo por fraude'), (r'B0171.*RescateTasa0', 'Rescate Tasa 0'),
         (r'NarrativaTasa0', 'Tasa 0 a leads'), (r'ValueProp', 'Beneficios a leads'), (r'Installments_SP', 'Compra a meses'),
         (r'Dormants-Referral', 'Referidos a dormants'), (r'Referral', 'Referidos'), (r'AnotayGana', 'AnotayGana'),
         (r'B0223', 'Meses sin Cash'), (r'CuestaEnero', 'Cuesta de enero'), (r'B0209', 'Descuento a inactivos'),
         (r'Newsletter', 'Boletín'), (r'Payment-Confirmation', 'Confirmación de pago'), (r'WeeklyRecommendations', 'Recomendaciones'),
         (r'B0335', 'Promos de comercios'), (r'Christmas', 'Navidad'), (r'B0333', 'Recuperar churn'), (r'Precobranza', 'Precobranza'),
         (r'BKT', 'Cobranza'), (r'late_fees', 'Aviso de cargos'), (r'TodayPaymentReminder', 'Aviso de pago hoy'),
         (r'DD advance payment', 'Aviso de saldo'), (r'B0208', 'Inactivos'), (r'Temu', 'Promo Temu'),
         (r'Cuponera', 'Cuponera'), (r'B0185', 'Oferta abandonada')]


def corto(c):
    for rx, n in CORTO:
        if re.search(rx, c): return n
    m = re.search(r'-([BTS]\d{3,4})-', c)
    return m.group(1) if m else c[:18]


def tramo(d):
    for k, _, a, b in TRAMOS:
        if a <= d <= b: return k


def datos(coh):
    e8 = pd.read_csv(D / 'e8_dias_hasta_baja.csv')
    bd = e8[(e8.bloque == 'banda_dias') & (e8.cohorte_limpia == coh)].set_index('clave')
    res = e8[(e8.bloque == 'resumen') & (e8.cohorte_limpia == coh)].iloc[0]
    l = pd.read_csv(H / 'muestra_l_familias_baja.csv')
    l = l[l.cohorte_limpia == coh].copy(); l['clave'] = l.clave.fillna('(sin nombre)')
    l['tramo'] = l.dias_mediana.map(tramo); l['corto'] = l.clave.map(corto)
    return bd, res, l


def wmed(d):
    d = d.sort_values('dias_mediana'); c = d.usuarios.cumsum()
    return d.dias_mediana[c >= d.usuarios.sum() / 2].iloc[0]


def grafica(coh, equipos, resalta, label, nota_tramo, sub='Personas que se dieron de baja, por días desde su primer correo'):
    """resalta(clave) -> True si la campaña es de lo que prueba el título (azul)."""
    bd, res, l = datos(coh)
    tot = res.usuarios
    s = SVG(label)
    X0, X1 = 118, 780
    cw = (X1 - X0) / len(TRAMOS)
    cx = lambda i: X0 + cw * (i + 0.5)
    # panel de arriba
    s.t(0, 14, sub, 12, INK, w=600)
    vmax = max(bd.usuarios) * 1.12
    YB, YT = 128, 34
    vy = lambda v: YB - (YB - YT) * v / vmax
    for i, (k, lab, a, b) in enumerate(TRAMOS):
        q = bd.loc[k]; p = 100 * q.usuarios / tot
        col = BLUE if nota_tramo(i) else M2
        s.rect(cx(i) - cw * 0.3, vy(q.usuarios), cw * 0.6, YB - vy(q.usuarios), col)
        s.t(cx(i), vy(q.usuarios) - 6, f'{q.usuarios/1e3:.0f} mil · {p:.0f} %', 11.5, INK, 'middle', 600)
        s.t(cx(i), YB + 15, lab, 11.5, TXT, 'middle', 600)
        s.t(cx(i), YB + 30, f'{q.emails_prom:.1f} correos', 11, SEC, 'middle')
    s.line(X0, YB, X1, YB, M1)
    s.t(0, YB + 15, 'Días', 11, SEC); s.t(0, YB + 30, 'Recibidos antes', 11, SEC)
    # panel de abajo: equipo x tramo
    YT2 = 186
    s.t(0, YT2 - 8, 'Campaña que llegó el día de la baja, por equipo (tamaño: personas que se dieron de baja)', 12, INK, w=600)
    RH = (398 - YT2) / len(equipos)
    rmax = max(l.groupby(['team', 'tramo']).usuarios.sum())
    rad = lambda u: max(3.5, 15 * (u / rmax) ** 0.5)
    for j, eqn in enumerate(equipos):
        y = YT2 + RH * (j + 0.5)
        le = l[l.team == eqn]
        s.t(0, y - 8, eqn, 12, INK, w=600)
        s.t(0, y + 7, f'{100*le.usuarios.sum()/tot:.0f} % de las bajas', 11, SEC)
        s.t(0, y + 21, f'mediana: día {wmed(le):.0f}', 11, SEC)
        s.line(X0, y + RH / 2, X1, y + RH / 2, GRID)
        for i, (k, *_r) in enumerate(TRAMOS):
            c = le[le.tramo == k]
            if not len(c): continue
            u = c.usuarios.sum(); top = c.sort_values('usuarios', ascending=False).iloc[0]
            col = BLUE if resalta(top.clave) else M1
            x0 = X0 + cw * i
            s.circle(x0 + 18, y - 6, rad(u), col, ring=False)
            s.t(x0 + 38, y - 2, f'{u/1e3:.1f} mil' if u < 1e4 else f'{u/1e3:.0f} mil', 11.5, INK, w=600)
            s.t(x0 + 3, y + 21, top.corto, 10.5, TXT)
    return s, bd, res, l
