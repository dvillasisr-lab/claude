"""Lámina 24: campaña que llegó el día de la baja (E8 v3, muestra_l_familias_baja.csv). x = días desde el primer correo hasta la baja
(mediana), y = correos recibidos antes de irse (promedio), tamaño = personas que se dieron de baja, color = equipo, relleno = nuevos o base vieja.
Una baja cuenta en dos campañas si ese día le llegaron dos."""
import math
from datos import *
from svgk import *
l = pd.read_csv(R + 'hallazgos/muestra_l_familias_baja.csv')
l = l[l.bloque == 'familia_dia_baja'].copy()
l['eq'] = l.team.fillna('?').map(team_of)
e8 = pd.read_csv(R + 'data/e8_dias_hasta_baja.csv'); coh = e8[e8.bloque == 'banda_dias'].groupby('cohorte_limpia').usuarios.sum()
print('cohortes E8', coh.to_dict())
def wmed(v, w):
    o = np.argsort(v.values); v = v.values[o]; w = w.values[o]; c = np.cumsum(w); return v[np.searchsorted(c, c[-1] / 2)]
RES = {}
for (e, c), d in l.groupby(['eq', 'cohorte_limpia']):
    RES[(e, c)] = (d.usuarios.sum(), wmed(d.dias_mediana, d.usuarios), np.average(d.emails_prom, weights=d.usuarios))
    print(e, c, d.usuarios.sum(), '%.0f %%' % (100 * d.usuarios.sum() / coh[c]), 'dias', RES[(e, c)][1], 'correos %.1f' % RES[(e, c)][2])
d = l[(l['eq'] == 'Marketing') & (l.cohorte_limpia == 1)].copy(); d['tema'] = [tema_of(a, b) for a, b in zip(d.clave, d.tipo)]
print('Mkt nuevos por tema (mil)', (d.groupby('tema').usuarios.sum() / 1e3).round(1).sort_values(ascending=False).head(4).to_dict())
NOM = {('KCash-B0000-CANVAS-Leads_LeftFunnel-Retargeting_Veriff', 1): ('Recordatorio de Veriff', 'r'),
       ('B0000-CANVAS-Leads_LeftFunnel-Retargeting_PersonalInfo', 1): ('Recordatorio de datos personales', 'b'),
       ('BillPay_Intro_Full_Rollout', 1): ('Lanzamiento de BillPay', 'l'),
       ('KCash-B0171-CANVAS-Leads-BBDDHotLeadsW1RescateTasa0', 1): ('Rescate de Tasa 0', 'r'),
       ('B0211-CANVAS-Nuevos_RegistradosPay-Tasa0', 0): ('Tasa 0 a registrados', 'l'),
       ('B0223-CANVAS-Nuevos_NeverActive', 0): ('Installments a quien nunca activó', 'tl'),
       ('KCash-B0326-Canvas-Leads-ReferralProgram', 0): ('Referidos a leads', 'l'),
       ('B0171-CANVAS-Leads_BBDDRezagada-NarrativaTasa0', 0): ('Tasa 0 a leads rezagados', 'b'),
}
COL = {'Marketing': BLUE, 'Product Growth': GREEN}
S = Svg('Días y correos hasta la baja por campaña que llegó ese día, por equipo, en usuarios nuevos y base vieja')
S.t(0, 16, 'Campaña que llegó el día de la baja; tamaño = personas que se dieron de baja', 12.5, INK, w=600)
x = 0
for col, nm in [(BLUE, 'Marketing'), (GREEN, 'Product Growth'), (MRK, 'Otros equipos')]:
    S.c(x + 6, 35, 5.5, col, stroke='none'); S.t(x + 15, 39, nm, 11.5); x += 15 + len(nm) * 6.6 + 18

Y0, Y1 = 84, 368
PAN = [(1, 'Nuevos: primer correo de febrero en adelante', 34, 374), (0, 'Base vieja: ya recibían correo en enero', 434, 774)]
ly = lambda v: Y1 - (Y1 - Y0) * math.log10(max(v, 1)) / math.log10(100)
rmax = 16; umax = 50000
rad = lambda u: max(3, rmax * math.sqrt(u / umax))
for c, tit, X0, X1 in PAN:
    lx = lambda v, X0=X0, X1=X1: X0 + (X1 - X0) * math.log10(max(v, 1)) / math.log10(250)
    S.t(X0 - 30, 66, tit, 11.5, INK, w=600)
    for v in (1, 3, 10, 30, 100):
        S.l(X0, ly(v), X1, ly(v), GRID); S.t(X0 - 5, ly(v) + 4, str(v), 10.5, SEC, 'end')
    for v in (1, 7, 30, 90, 180):
        S.l(lx(v), Y0, lx(v), Y1, GRID); S.t(lx(v), Y1 + 15, f'{v}', 10.5, SEC, 'middle')
    for k in (1, 1 / 7):
        xa, xb = 1, 250
        ya, yb = xa * k, xb * k
        if ya < 1: xa = 1 / k; ya = 1
        if yb > 100: xb = 100 / k; yb = 100
        S.l(lx(xa), ly(ya), lx(xb), ly(yb), MRK, 1)
        if c == 1:
            xt = 70 if k == 1 else 240
            S.t(lx(xt) - 4, ly(xt * k) - 6, 'un correo al día' if k == 1 else 'uno a la semana', 10.5, SEC, 'end')
    p = l[(l.usuarios >= 4000) & (l.cohorte_limpia == c)].sort_values('usuarios', ascending=False)
    for r in p.itertuples():
        S.c(lx(r.dias_mediana), ly(r.emails_prom), rad(r.usuarios), COL.get(r.eq, MRK), op=0.85)
    for r in p.itertuples():
        for (k, cc), (nm, pos) in NOM.items():
            if k in r.clave and cc == c:
                cx, cy, rr = lx(r.dias_mediana), ly(r.emails_prom), rad(r.usuarios)
                sub = f'{r.usuarios/1e3:.1f} mil · {r.dias_mediana} días · {r.emails_prom:.0f} correos'
                if pos == 'r': ax, ay, an = cx + rr + 4, cy - 2, 'start'
                elif pos == 'l': ax, ay, an = cx - rr - 4, cy - 2, 'end'
                elif pos == 'b': ax, ay, an = cx, cy + rr + 12, 'middle'
                elif pos == 'bl': ax, ay, an = cx - 4, cy + rr + 12, 'end'
                else: ax, ay, an = cx + 4, cy - rr - 16, 'end'
                S.t(ax, ay, nm, 11, INK, an, w=600, halo=True); S.t(ax, ay + 13, sub, 10.5, TXT, an, halo=True)
S.t(0, 400, 'Alto: correos recibidos antes de irse (promedio, escala logarítmica)', 10.5, SEC)
S.t(774, 400, 'Ancho: días desde su primer correo hasta la baja (mediana)', 10.5, SEC, 'end')
svg = S.done()
mn, mv, pv = RES[('Marketing', 1)], RES[('Marketing', 0)], RES[('Product Growth', 0)]
save(24, dict(kind='grafica',
  titulo='Marketing pierde a los usuarios nuevos en días; Product Growth pierde a la base vieja en meses',
  que='Nuevos: recordatorio de registro, Tasa 0, BillPay. Base vieja: Tasa 0, referidos.',
  quien='Marketing y Product Growth; Others por un solo correo de BillPay.',
  a_quien='Nuevos: primer correo desde febrero (158.5 mil bajas). Base vieja: enero (242.3 mil).',
  lecturas=[
   f'Nuevos: Marketing pierde {mn[0]/1e3:.0f} mil en {mn[1]} días con {mn[2]:.0f} correos; la mitad con el recordatorio de registro.',
   f'Base vieja: Product Growth pierde {pv[0]/1e3:.1f} mil en {pv[1]} días con {pv[2]:.0f} correos, unos dos por semana.',
   'El lanzamiento de BillPay se llevó 49 mil nuevos con un solo correo: casi un tercio de sus bajas.'],
  causa='Marketing junta recordatorios diarios sobre el recién llegado; Product Growth repite ofertas de crédito durante meses.',
  sowhat='Nuevo: un correo al día y tres la primera semana. Base vieja: menos ofertas de crédito no pedidas.',
  fuente='Fuente: Braze, días y correos hasta la baja (E8 v3) por campaña que llegó ese día; 400.8 mil bajas, enero a septiembre 2026. Días: mediana; correos: promedio.',
  svg=svg))
check(24)
