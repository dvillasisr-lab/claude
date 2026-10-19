"""Lámina 57: quien abre compra antes, no siempre más (E9a, muestra_m). Izquierda: veces que convierte más quien abre que quien no
abre, a 7, 30 y 90 días, mediana por canal (campañas promocionales con muestra). Derecha: parte del volumen medido en campañas donde la
ventaja solo adelanta (1.5 veces o más a 7 días y menos de 1.5 a 90), por equipo y por tema."""
from comun import *

c = pd.read_csv(H / 'muestra_c_familias.csv'); tipo = c.groupby('familia').tipo.first()
m = pd.read_csv(H / 'muestra_m_ventanas.csv')
m = m[m.muestra == True].copy()
m['tipo'] = m.familia.map(tipo).fillna('?'); m['tema'] = m.familia.map(gancho_of)
m['eq'] = m.familia.str.split('-').str[0].map(lambda x: TEAM.get(x, x))
m['adel'] = (m.lift_7 >= 1.5) & (m.lift_90 < 1.5)
pm = m[m.tipo == 'promocional o lifecycle'].copy()
N, NA = len(pm), int(pm.adel.sum()); V, VA = pm.envios_usuario_dia.sum(), pm[pm.adel].envios_usuario_dia.sum()
med = pm.groupby('canal')[['lift_7', 'lift_30', 'lift_90']].median()
gro = pm.assign(ga=pm.ca_90 / pm.ca_7, gn=pm.cn_90 / pm.cn_7).groupby('canal')[['ga', 'gn']].median()
def parte(k):
    g = pm.groupby(k).apply(lambda d: pd.Series({'v': d.envios_usuario_dia.sum(), 'a': d[d.adel].envios_usuario_dia.sum(), 'l90': d.lift_90.median(), 'ca90': d.ca_90.median()}))
    g['p'] = 100 * g.a / g.v; return g
eq, te = parte('eq'), parte('tema')
# WhatsApp pagado en campañas que solo adelantan (E1, por entregado)
e1 = load_e1()
adw = set(pm[pm.adel & (pm.canal == 'whatsapp')].familia)
wa_ad = e1[(e1.canal == 'whatsapp') & e1.familia.isin(adw)].whatsapp_delivery.sum()
ex = pm.set_index(['familia', 'canal'])
def X(f, ch): q = ex.loc[(f, ch)]; return q.ca_7, q.cn_7, q.ca_90, q.cn_90
vf = X('Marketing-KCash-B0000-CANVAS-Leads_LeftFunnel-Retargeting_Veriff', 'email')
ins = X('Lending-KCash-B0301-CANVAS-Active-Retargeting_Installments_SP', 'email')
print(med.round(2)); print(gro.round(2)); print(eq.round(2)); print(te.round(2)); print(N, NA, V / 1e6, VA / 1e6, 'wa', wa_ad / 1e6, vf, ins)

s = SVG('Veces que convierte más quien abre que quien no abre, a 7, 30 y 90 días, por canal; y parte del volumen en campañas donde la ventaja solo adelanta la compra, por equipo y tema')
CH = [('push notification', 'Push', BLUE), ('email', 'Email', M1), ('whatsapp', 'WhatsApp', GREEN)]
s.t(0, 16, 'Cuántas veces más convierte quien abre que quien no abre', 12, INK, w=600)
s.t(0, 32, 'Mediana de las campañas promocionales de cada canal', 10.5, SEC)
X0, X1, Y0, Y1 = 40, 300, 62, 350
xs = {7: X0, 30: X0 + (X1 - X0) * 0.4, 90: X1}
ys = lambda v: Y1 - (Y1 - Y0) * (v - 1) / 2.25
for v in (1, 1.5, 2, 2.5, 3):
    s.line(X0, ys(v), X1, ys(v)); s.t(X0 - 8, ys(v) + 4, f'{v:g}', 11, SEC, 'end')
s.line(X0, ys(1), X1, ys(1), M1, 1)
s.t(X1, ys(1) - 6, '1 = quien abre compra igual que quien no', 10.5, SEC, 'end')
for d, x in xs.items(): s.t(x, Y1 + 18, f'{d} días', 11.5, TXT, 'middle')
for key, lab, col in CH:
    v = [med.loc[key, f'lift_{d}'] for d in (7, 30, 90)]
    pts = ' '.join(f'{xs[d]:.1f},{ys(q):.1f}' for d, q in zip((7, 30, 90), v))
    s.raw(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2.5"/>')
    for d, q in zip((7, 30, 90), v): s.circle(xs[d], ys(q), 4.5, col)
    s.t(xs[7] - 0 + 10, ys(v[0]) - 8, f'{v[0]:.1f}', 11.5, INK, 'start', 600, halo=True)
    s.t(xs[90] + 9, ys(v[2]) + 4, f'{v[2]:.1f}  {lab}', 11.5, INK, 'start', 600, halo=True)
# panel derecho: barras 100 % por equipo y tema
PX, PW = 420, 300
s.t(PX, 16, 'Volumen medido en campañas donde la ventaja solo adelanta', 12, INK, w=600)
s.legend([(BLUE, 'Solo adelanta la compra', 'rect'), (M2, 'La ventaja se sostiene', 'rect')], PX, 24, size=11)
rows = [('Por equipo', None)] + [(n, eq.loc[k]) for k, n in (('Sales', 'Sales'), ('Marketing', 'Marketing'), ('Product Growth', 'Product Growth'))] + \
       [('Por tema', None)] + [(n, te.loc[k]) for k, n in (('Recordatorio de algo empezado', 'Recordatorio de algo empezado'), ('Referidos', 'Referidos'),
                                                         ('Descuento, cupón u oferta', 'Descuentos y cupones'), ('Tasa 0', 'Tasa 0'))]
y = 62
for name, q in rows:
    if q is None:
        s.t(PX, y + 8, name, 11, SEC, w=600); y += 16; continue
    s.t(PX, y + 10, name, 11.5, INK, w=600)
    s.t(780, y + 10, f'{q.v/1e6:.0f} M', 11, SEC, 'end')
    by = y + 16; wa = PW * q.a / q.v
    s.rect(PX, by, wa, 14, BLUE); s.rect(PX + wa + (1.5 if wa > 0 else 0), by, PW - wa - (1.5 if wa > 0 else 0), 14, M2)
    s.t(PX + wa + 6 if wa < 60 else PX + 6, by + 11, f'{q.p:.0f} %', 11.5, INK if wa < 60 else '#FFFFFF', w=600)
    y += 40
s.t(780, 52, 'Volumen', 10.5, SEC, 'end')
s.t(0, 400, f'Ventaja: conversión de quien abre entre la de quien no abre. {N} campañas promocionales por canal con al menos 1,000 personas por lado.', 10.5, SEC)
s.t(0, 414, f'Solo adelanta: 1.5 veces o más a 7 días y menos de 1.5 a 90 ({NA} campañas). Volumen: millones de envíos por persona y día.', 10.5, SEC)

write(57, dict(
    titulo='Quien abre compra antes, pero no siempre más: a 90 días su ventaja sobre quien no abre se reduce a la mitad',
    que='Recordatorios de algo empezado (verificar identidad, pagar la compra a meses), promociones de comercios de Sales a sus clientes recurrentes y referidos a clientes.',
    quien=f'Sales ({eq.loc["Sales","p"]:.0f} % de su volumen está en campañas que solo adelantan), Marketing ({eq.loc["Marketing","p"]:.0f} %) y Product Growth ({eq.loc["Product Growth","p"]:.0f} %).',
    a_quien='Clientes y registrados que ya iban a comprar o a terminar su registro.',
    lecturas=[
        f'La ventaja de quien abre baja de {med.loc["email","lift_7"]:.1f} a {med.loc["email","lift_90"]:.1f} veces en email, de {med.loc["push notification","lift_7"]:.1f} a {med.loc["push notification","lift_90"]:.1f} en push y de {med.loc["whatsapp","lift_7"]:.1f} a {med.loc["whatsapp","lift_90"]:.1f} en WhatsApp.',
        f'Se achica porque quien no abrió también compra después: de 7 a 90 días su conversión se multiplica por {gro.gn.min():.1f} a {gro.gn.max():.1f}, y la de quien abrió por {gro.ga.min():.1f} a {gro.ga.max():.1f}. El mensaje movió la fecha, no la decisión.',
        f'Lo que más adelanta son los recordatorios: {te.loc["Recordatorio de algo empezado","p"]:.0f} % de su volumen. Ejemplo: verificar identidad por email (Marketing), {vf[0]:.1f} % contra {vf[1]:.1f} % a 7 días y {vf[2]:.1f} % contra {vf[3]:.1f} % a 90. Por WhatsApp esas campañas costaron {wa_ad/1e6:.1f} M MXN en nueve meses.',
    ],
    causa='Juzgamos cada campaña por cuánto compra quien la abre, sin un grupo que no reciba nada. Quien abre ya iba a comprar, así que el mensaje parece vender más de lo que vende.',
    sowhat='Solo un grupo sin mensajes dice cuánto suma una campaña; mientras tanto, lo que solo adelanta la compra va por push e in-app, que no cuestan.',
    fuente=f'Fuente: Braze, quien abre contra quien no abre a 7, 30 y 90 días por campaña y canal (E9a), enero a septiembre 2026. En {NA} de {N} campañas promocionales por canal la ventaja casi desaparece a 90 días: {VA/1e6:.0f} M de {V/1e6:.0f} M envíos medidos. WhatsApp a 1.00 MXN por entregado (E1).',
    svg=s.svg()))
