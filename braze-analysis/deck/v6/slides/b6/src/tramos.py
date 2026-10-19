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
         (r'Dormants-Referral', 'Referidos a dormants'), (r'Referral', 'Referidos'), (r'AnotayGana', 'Anota y Gana'),
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


def grafica(coh, equipos, resalta, label, etiquetas, sub):
    """Franja por equipo: cada punto es una campaña que llegó el día de la baja; x = mediana de días desde el primer correo
    (escala logarítmica de días + 1), tamaño = personas que se dieron de baja. Raya negra = mediana del equipo."""
    bd, res, l = datos(coh)
    tot = res.usuarios
    s = SVG(label)
    s.t(0, 14, sub, 12, INK, w=600)
    X0, X1 = 150, 700
    xs = lambda d: X0 + (X1 - X0) * math.log10(d + 1) / math.log10(301)
    TOP = 64; RH = (352 - TOP) / len(equipos)
    m30 = 100 * bd.loc[['0 mismo día', '1 a 7', '08 a 30'], 'usuarios'].sum() / tot
    s.rect(xs(0), TOP - 10, xs(30) - xs(0), RH * len(equipos), '#EEF2FC')
    s.t(xs(0) + 4, TOP - 14, f'Primer mes: {m30:.0f} % de las bajas', 11, BLUE, 'start', 600)
    for d, lab in ((0, '0'), (1, '1'), (3, '3'), (7, '7'), (30, '30'), (90, '90'), (180, '180'), (300, '300')):
        s.line(xs(d), TOP - 10, xs(d), TOP - 10 + RH * len(equipos)); s.t(xs(d), TOP + RH * len(equipos) + 6, lab, 10.5, SEC, 'middle')
    s.t(X1, TOP + RH * len(equipos) + 21, 'Días desde el primer correo hasta la baja (mediana de cada campaña)', 10.5, SEC, 'end')
    s.t(780, TOP - 14, 'Parte de las bajas', 10.5, SEC, 'end')
    umax = l.usuarios.max()
    for j, eqn in enumerate(equipos):
        yc = TOP + RH * j + RH / 2 - 6
        le = l[l.team == eqn]
        s.t(0, yc - 2, eqn, 12, INK, w=600); s.t(0, yc + 12, f'{len(le)} campañas', 10.5, SEC)
        s.line(0, yc + RH / 2 + 1, 780, yc + RH / 2 + 1, GRID)
        for i, (_, q) in enumerate(le.sort_values('usuarios', ascending=False).iterrows()):
            y = yc + ((i * 7) % 15 - 7)
            s.circle(xs(q.dias_mediana), y, 3 + 13 * math.sqrt(q.usuarios / umax), BLUE if resalta(q.clave) else M1, extra=' fill-opacity="0.85"')
            if q.clave in etiquetas:
                dx, dy, an = etiquetas[q.clave]
                etiqueta(s, xs(q.dias_mediana), y, corto(q.clave), dx, dy, an, sub=f'{q.usuarios/1e3:.0f} mil personas, día {q.dias_mediana}')
        md = wmed(le)
        s.rect(xs(md) - 1.5, yc - 14, 3, 28, INK)
        s.t(780, yc + 4, f'{100*le.usuarios.sum()/tot:.0f} %', 13, INK, 'end', 600)
    return s, bd, res, l
