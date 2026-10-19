"""Lámina 63: mensajes de la misma campaña por persona en el mes (envíos entre personas de cada campaña y mes, E1) contra respuesta y
bajas. Ofertas = campañas promocionales que no son recordatorio de algo empezado (tipo del catálogo, tema por el nombre, regla G)."""
from comun import *

e = load_e1(); e['gg'] = e.communication_name.map(gan_g)
BANDS = ['1', '2', '3 a 4', '5+']
def prep(ch):
    x = e[(e.canal == ch) & (e.usuarios_aprox > 1000)].copy(); t = x.envios / x.usuarios_aprox
    x['toq'] = np.select([t < 1.5, t < 2.5, t < 4.5], BANDS[:3], '5+')
    x['k'] = np.where(x.tipo != 'promocional o lifecycle', 'aviso', np.where(x.gg == 'recordatorio', 'rec', 'oferta'))
    x['tam'] = np.select([x.usuarios_aprox < 1e4, x.usuarios_aprox < 1e5, x.usuarios_aprox < 1e6], ['<10k', '10-100k', '100k-1M'], '1M+')
    return x
em, pu = prep('email'), prep('push notification')
def f(g, b, r):
    return pd.Series({'env': g.envios.sum(), 'resp': 1000 * g[r].sum() / g[b].sum(), 'bmp': 1000 * g.email_unsubscribe.sum() / g.usuarios_aprox.sum()})
oe = em[em.k == 'oferta'].groupby('toq').apply(f, 'email_delivery', 'email_click')
re_ = em[em.k == 'rec'].groupby('toq').apply(f, 'email_delivery', 'email_click')
op = pu[pu.k == 'oferta'].groupby('toq').apply(f, 'pn_send', 'pn_open')
allm = em.groupby('toq').apply(f, 'email_delivery', 'email_click')
tam = em[(em.k == 'oferta') & (em.toq == '1')].groupby('tam').apply(f, 'email_delivery', 'email_click')
def ex(fm, mes, ch):
    x = e[(e.familia == fm) & (e.canal == ch) & e.mes.str.startswith(mes)]; return x.envios.sum() / x.usuarios_aprox.sum(), resp(x, ch)
b585 = ex('Sales-KPay-B0585-CANVAS-Recurrentes-ComerciodeldiaAgosto-N/A', '2026-08', 'push notification')
b561 = ex('Marketing-KPay-B0561-CANVAS-Leads-Comerciodeldia-N/A', '2026-07', 'push notification')
vf = ex('Marketing-KCash-B0000-CANVAS-Leads_LeftFunnel-Retargeting_Veriff', '2026-08', 'email')
print(oe.round(2)); print(re_.round(2)); print(op.round(2)); print(allm.round(2)); print(tam.round(2)); print(b585, b561, vf)

s = SVG('Ofertas por correo y push según cuántos mensajes de la misma campaña recibe cada persona en el mes: clics por cada mil correos, bajas por cada mil personas y aperturas por cada mil push')
s.t(0, 16, 'Ofertas, según mensajes de la misma campaña por persona en el mes', 12.5, INK, w=600)
s.legend([(M2, 'Uno', 'rect'), (BLUE, 'Dos', 'rect'), (M1, 'Tres o más', 'rect')], 0, 26, size=11)
COL = {'1': M2, '2': BLUE, '3 a 4': M1, '5+': M1}
P = [('Clics por cada mil correos', oe, 'resp', 6), ('Bajas del email por cada mil personas', oe, 'bmp', 7), ('Aperturas por cada mil push', op, 'resp', 15)]
PW, GAP, Y0, Y1 = 236, 36, 78, 262
for k, (h, d, col, mx) in enumerate(P):
    x0 = k * (PW + GAP)
    s.t(x0, Y0 - 14, h, 11.5, INK, w=600)
    bw = PW / 4
    s.line(x0, Y1, x0 + PW, Y1, M1)
    for i, b in enumerate(BANDS):
        v = d.loc[b, col]; hgt = (Y1 - Y0 - 22) * v / mx; cx = x0 + bw * (i + 0.5)
        s.rect(cx - bw * 0.32, Y1 - hgt, bw * 0.64, hgt, COL[b])
        s.t(cx, Y1 - hgt - 6, f'{v:.1f}', 12, INK, 'middle', 600)
        s.t(cx, Y1 + 15, b, 11.5, TXT, 'middle', 600)
        s.t(cx, Y1 + 30, f'{d.loc[b,"env"]/1e6:.0f} M', 11, SEC, 'middle')
    s.t(x0, Y1 + 46, 'mensajes al mes · enviados' if k != 1 else 'mensajes al mes · correos enviados', 10.5, SEC)
# franja de recordatorios
y = 334
s.rect(0, y - 18, 780, 58, '#EEF6F2')
s.t(12, y, 'Recordatorios de algo empezado, por correo (otra razón para responder)', 11.5, GREEN, w=600)
s.t(12, y + 18, 'Clics por cada mil correos: ' + ', '.join(f'{re_.loc[b,"resp"]:.0f}' for b in BANDS) + ' con 1, 2, 3 a 4 y 5 o más al mes.', 11, INK)
s.t(12, y + 33, 'Bajas por cada mil personas: ' + ', '.join(f'{re_.loc[b,"bmp"]:.1f}' for b in BANDS) + f'. Con 5 o más al mes se dan de baja tres veces más.', 11, INK)
s.t(0, 400, 'En push la apertura de las ofertas se sostiene hasta cuatro al mes y cae con cinco o más.', 10.5, SEC)
s.t(0, 414, 'Mensajes al mes: envíos de la campaña en el mes entre personas que la recibieron. Campañas y meses con más de mil personas.', 10.5, SEC)

write(63, dict(
    titulo='En las ofertas, el segundo correo del mes todavía suma; del tercero en adelante cada correo responde menos y las bajas siguen subiendo',
    que='Promociones repetidas dentro del mes: Comercio del día por push, rescate de fin de semana, Tasa 0 y referidos.',
    quien='Sales y Marketing con Comercio del día por push; Marketing con el rescate de fin de semana y el recordatorio de verificar identidad.',
    a_quien='Clientes recurrentes de KPay, leads y registrados.',
    lecturas=[
        f'Por correo, la oferta responde {oe.loc["1","resp"]:.1f} clics por cada mil con un correo al mes, {oe.loc["2","resp"]:.1f} con dos, {oe.loc["3 a 4","resp"]:.1f} con tres o cuatro y {oe.loc["5+","resp"]:.1f} con cinco o más.',
        f'Las bajas por persona sí se acumulan: {oe.loc["1","bmp"]:.1f} por cada mil personas con un correo, {oe.loc["2","bmp"]:.1f} con dos y {oe.loc["5+","bmp"]:.1f} con cinco o más.',
        f'Pesa más el tamaño que la repetición: con un correo al mes, a grupos de 10 a 100 mil personas la oferta tiene {tam.loc["10-100k","resp"]:.1f} clics por cada mil; a más de un millón, {tam.loc["1M+","resp"]:.1f}. Sales manda {b585[0]:.1f} push al mes del Comercio del día con {b585[1]:.1f} % de apertura.',
    ],
    causa='No hay límite de mensajes por persona por campaña: cada equipo repite su oferta en el mes sin ver si la persona abrió la anterior.',
    sowhat='Máximo dos mensajes por campaña al mes, y el segundo solo a quien no abrió el primero; los recordatorios también con límite diario.',
    fuente=f'Fuente: Braze, envíos por campaña, mes y canal (E1), enero a septiembre 2026. Con todos los correos (incluidos avisos y cobranza) sale 0.75 % de clic con uno, 1.76 % con dos y 0.48 % con tres o cuatro, pero esa subida la explican los avisos, que se mandan dos veces y responden más.',
    svg=s.svg()))
