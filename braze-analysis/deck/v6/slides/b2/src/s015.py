"""Lámina 15: campañas de correo con 1 M o más envíos: apertura (x) contra clics por cada cien que abren (y), tamaño = envíos,
color = promoción contra recordatorio de algo empezado contra avisos y cobranza."""
import math
from b2base import *

d = load_b()
e = d[d.canal == 'email']
f = lambda g: pd.Series({'env': g.email_sent.sum() / 1e6, 'ab': 100 * g.email_open.sum() / g.email_delivery.sum(),
                         'ctor': 100 * g.email_click.sum() / max(1, g.email_open.sum()), 'clic': 100 * g.email_click.sum() / g.email_delivery.sum(),
                         'baj': 1000 * g.email_unsubscribe.sum() / g.email_delivery.sum()})
e = e.assign(cl=np.where(e.tipo != 'promocional', 'aviso', np.where(e.gan == 'recordatorio', 'record', 'promo')))
tot = f(e); bytipo = e.groupby('tipo').apply(f); bycl = e.groupby('cl').apply(f)
byeq = e.groupby('equipo').apply(f); byaud = e.groupby('aud').apply(f)
pr = e[e.tipo == 'promocional']; bygan = pr.groupby('gan').apply(f)
fa = e.groupby(['fam', 'equipo', 'cl']).apply(f).reset_index()
fa = fa[fa.env >= 1].sort_values('env', ascending=False)
print('total', tot.round(2).to_dict()); print(bytipo.round(2)); print(bycl.round(2)); print(byeq.round(2)); print(bygan.round(2))
print(len(fa), fa.env.sum(), (fa.groupby('cl').env.sum()).round(1).to_dict())
promo_fa = fa[fa.cl == 'promo']
print('promo campañas con 1M+: ctor<3', (promo_fa.ctor < 3).sum(), 'de', len(promo_fa), 'envíos', promo_fa[promo_fa.ctor < 3].env.sum())
# tamaño de envío
# tamaño = personas que recibieron ese envío en el mes (comunicación por mes)
def bucket(u):
    return '10 a 100 mil' if 1e4 <= u < 1e5 else ('más de 1 M' if u >= 1e6 else ('100 mil a 1 M' if u >= 1e5 else 'menos'))
bk = e.assign(bk=e.usuarios_aprox.map(bucket)).groupby('bk').apply(lambda g: 100 * g.email_click.sum() / g.email_open.sum())
print('por tamaño', bk.round(1).to_dict())

COL = {'promo': BLUE, 'record': GREEN, 'aviso': G1}
LAB = {'promo': 'Promociones', 'record': 'Recordatorios de algo que la persona empezó', 'aviso': 'Avisos de servicio y cobranza'}
S = Svg('Dispersión de campañas de correo con un millón o más de envíos: apertura contra clics por cada cien personas que abren. '
        'Las promociones se abren pero casi no tienen clic; los recordatorios y avisos sí.')
lx = 0
for k in ('promo', 'record', 'aviso'):
    S.circle(lx + 5, 14, 5, COL[k], '')
    txt = LAB[k]
    S.t(lx + 14, 18, txt, 11, INK if k != 'aviso' else TXT, w=600 if k != 'aviso' else 400)
    lx += 14 + tw(txt, 11, 600) + 14
S.t(0, 36, 'Cada punto es una campaña con todas sus versiones; el tamaño es el número de correos enviados.', 10.5, SEC)
X0, X1, Y0, Y1 = 50, 486, 72, 360
XM = 80
LO, HI = math.log10(0.15), math.log10(25)
sx = lambda v: X0 + (X1 - X0) * v / XM
sy = lambda v: Y1 - (Y1 - Y0) * (math.log10(min(max(v, 0.15), 25)) - LO) / (HI - LO)
for v in (0.3, 1, 3, 10):
    S.line(X0, sy(v), X1, sy(v), GRID)
    S.t(X0 - 8, sy(v) + 4, f'{v:g}', 11, SEC, 'end')
for v in range(0, 81, 20):
    S.line(sx(v), Y1, sx(v), Y1 + 4, G1)
    S.t(sx(v), Y1 + 18, f'{v} %', 11, SEC, 'middle')
S.line(X0, Y1, X1, Y1, G1)
S.t(X0 - 30, Y0 - 14, 'Clics por cada cien personas que abren (escala que crece por múltiplos)', 11, SEC)
S.t(X1, Y1 + 36, 'Abren de cada cien que reciben el correo', 11, SEC, 'end')
# zona "se abre y no se usa": menos de 3 clics por cada cien que abren
S.rect(X0, sy(3), X1 - X0, Y1 - sy(3), BLUE, ' opacity="0.06"')
S.line(X0, sy(3), X1, sy(3), BLUE, 1, ' stroke-dasharray="4 4"')
S.t(X0 + 4, Y1 - 6, 'Zona: menos de 3 clics por cada cien que abren', 10.5, BLUE, 'start', 600, halo=True)
MED = fa.groupby('cl').ctor.median()
print('medianas', MED.round(2).to_dict(), fa.groupby('cl').size().to_dict())
for k in ('promo', 'record'):
    S.line(X0, sy(MED[k]), X1, sy(MED[k]), COL[k], 1.6)
    S.t(X1 - 4, sy(MED[k]) - 5, f'Mediana de {"promociones" if k == "promo" else "recordatorios"}: {MED[k]:.1f}', 10.5, COL[k], 'end', 700, halo=True)
r = lambda env: 2.5 + 2.6 * math.sqrt(env)
for p in fa.itertuples():
    S.circle(sx(p.ab), sy(p.ctor), r(p.env), COL[p.cl], ' fill-opacity="0.85" stroke="#FFFFFF" stroke-width="1.2"')
NOTES = [
    ('Canvas-Leads-ReferralProgram', 'Marketing-KCash', 'Invitar a un amigo, a leads (Marketing)', (-14, -12)),
    ('PromocionesMerchantsAmplificacion', None, 'Ofertas de comercios a la cartera KPay (Sales)', (12, -10)),
    ('Nuevos_RegistradosPay-Tasa0', None, 'Tasa 0 a registrados sin crédito (Product Growth)', (16, -16)),
    ('BillPay_Intro', None, 'Lanzamiento de BillPay (Others)', (-12, -14)),
    ('Retargeting_Veriff', None, 'Terminar la verificación de identidad (Marketing)', (14, -10)),
]
KX, KY = 506, 80
S.t(KX, KY - 4, 'Campañas marcadas', 11, INK, w=600)
for k, (key, pref, lab, (dx, dy)) in enumerate(NOTES, 1):
    q = fa[fa.fam.str.contains(key, regex=False)]
    if pref:
        q = q[q.fam.str.startswith(pref)]
    p = q.iloc[0]
    x, y = sx(p.ab), sy(p.ctor)
    S.line(x, y, x + dx * 0.6, y + dy * 0.6, INK, 0.8)
    S.circle(x + dx, y + dy, 7, '#FFFFFF', f' stroke="{INK}" stroke-width="1"')
    S.t(x + dx, y + dy + 3.8, str(k), 10.5, INK, 'middle', 700)
    yk = KY + 12 + (k - 1) * 52
    S.circle(KX + 7, yk + 4, 7, '#FFFFFF', f' stroke="{INK}" stroke-width="1"')
    S.t(KX + 7, yk + 7.8, str(k), 10.5, INK, 'middle', 700)
    S.t(KX + 20, yk + 2, lab, 10.5, INK, w=600, halo=True)
    S.t(KX + 20, yk + 15, f'{p.env:.1f} M correos, abre {p.ab:.0f} %,', 10.5, TXT)
    S.t(KX + 20, yk + 28, f'{p.ctor:.1f} clics por cada cien que abren', 10.5, TXT)
    print(lab, round(p.env, 1), round(p.ab, 1), round(p.ctor, 2), round(p.clic, 2), round(p.baj, 1))
svg = S.done()
L = lambda s: fa[fa.fam.str.contains(s, regex=False)].iloc[0]
ref = fa[fa.fam.str.contains('Canvas-Leads-ReferralProgram') & fa.fam.str.startswith('Marketing-KCash')].iloc[0]
save(15, dict(
    kind='grafica',
    titulo='El correo se abre pero no se usa: de cada cien personas que abren una promoción, menos de tres hacen clic',
    que='Referidos, Tasa 0, descuentos, lanzamientos y ofertas de comercios.',
    quien=f'Clics por cada cien que abren: Sales {byeq.loc["Sales","ctor"]:.1f}, Product Growth {byeq.loc["Product Growth","ctor"]:.1f}, Marketing {byeq.loc["Marketing","ctor"]:.1f}.',
    a_quien='Leads, registrados sin crédito, ex clientes y toda la cartera de KPay.',
    lecturas=[
        f'{bytipo.loc["promocional","env"]:.0f} M correos de promoción: abre {bytipo.loc["promocional","ab"]:.0f} % y de cada cien que abren, {bytipo.loc["promocional","ctor"]:.1f} hacen clic.',
        f'Recordar algo que la persona empezó: {bycl.loc["record","ctor"]:.0f} clics por cada cien que abren; invitar a un amigo: {bygan.loc["referidos","ctor"]:.1f}.',
        f'Mientras más grande el envío, menos clic: {bk["10 a 100 mil"]:.1f} con 10 a 100 mil personas, {bk["más de 1 M"]:.1f} con más de 1 M.',
    ],
    causa='Se manda la misma oferta a listas enormes que no la pidieron: el asunto atrae la apertura, el contenido no sirve.',
    sowhat='No es el asunto ni la entrega: es lo que ofrece el correo y a quién. Más recordatorios, menos promoción.',
    fuente=f'{FUENTE_E1}; {len(fa)} campañas con 1 M o más de correos. La apertura incluye aperturas automáticas; la de 75 % es dudosa.',
    svg=svg,
))
