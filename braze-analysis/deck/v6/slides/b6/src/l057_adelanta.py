"""Lámina 57 (ronda 2): pendientes con muchas líneas, un panel por canal con la misma escala. Cada línea es una campaña promocional
(E9a, muestra_m, con muestra suficiente): cuántas veces más convierte quien abre que quien no abre, a 7, 30 y 90 días. Azul = la ventaja
solo adelanta (1.5 veces o más a 7 días y menos de 1.5 a 90); línea negra = mediana del canal."""
from comun import *

c = pd.read_csv(H / 'muestra_c_familias.csv'); tipo = c.groupby('familia').tipo.first()
m = pd.read_csv(H / 'muestra_m_ventanas.csv')
m = m[m.muestra == True].copy()
m['tipo'] = m.familia.map(tipo); m['eq'] = m.familia.str.split('-').str[0].map(lambda x: TEAM.get(x, x))
m['adel'] = (m.lift_7 >= 1.5) & (m.lift_90 < 1.5); m['nom'] = m.familia.map(nombre); m['tema'] = m.familia.map(gancho_of)
pm = m[m.tipo == 'promocional o lifecycle'].copy()
N, NA = len(pm), int(pm.adel.sum()); V, VA = pm.envios_usuario_dia.sum(), pm[pm.adel].envios_usuario_dia.sum()
med = pm.groupby('canal')[['lift_7', 'lift_30', 'lift_90']].median()
gro = pm.assign(ga=pm.ca_90 / pm.ca_7, gn=pm.cn_90 / pm.cn_7).groupby('canal')[['ga', 'gn']].median()
eqp = pm.groupby('eq').apply(lambda d: 100 * d[d.adel].envios_usuario_dia.sum() / d.envios_usuario_dia.sum())
tep = pm.groupby('tema').apply(lambda d: 100 * d[d.adel].envios_usuario_dia.sum() / d.envios_usuario_dia.sum())
print(N, NA, med.round(2), eqp.round(1).to_dict(), tep.round(1).to_dict())

s = SVG('Cada línea es una campaña: cuántas veces más convierte quien abre que quien no abre, a 7, 30 y 90 días, un panel por canal')
s.t(0, 14, 'Cuántas veces más convierte quien abre que quien no abre, por campaña', 12, INK, w=600)
s.legend([(BLUE, f'Solo adelanta la compra ({NA} campañas)', 'line'), (M1, 'La ventaja se sostiene', 'line'), (INK, 'Mediana del canal', 'line')], 0, 24, size=11)
Y0, Y1 = 66, 356
ys = logmap(0.8, 20, Y1, Y0)
PAN = [('email', 'Correo'), ('push notification', 'Push'), ('whatsapp', 'WhatsApp')]
PW = 248
LB = {('email', 'Verificar identidad'): 12, ('email', 'Pagar compra a meses'): 8.5, ('push notification', 'Pagar compra a meses'): 12, ('push notification', 'Verificar identidad'): 8.5}
for k, (ch, h) in enumerate(PAN):
    x0 = 30 + k * (PW + 12); xd = {7: x0 + 6, 30: x0 + 6 + (PW - 80) * 0.42, 90: x0 + PW - 86}
    d = pm[pm.canal == ch]
    s.t(x0, 54, f'{h}: {len(d)} campañas', 11.5, INK, w=600)
    for v in (1, 2, 5, 10, 20):
        s.line(x0, ys(v), xd[90] + 4, ys(v)); s.t(x0 - 4, ys(v) + 4, f'{v}', 10.5, SEC, 'end')
    s.line(x0, ys(1), xd[90] + 4, ys(1), M1, 1)
    for dd, x in xd.items(): s.t(x, Y1 + 16, f'{dd} días', 10.5, TXT, 'middle')
    for adel in (False, True):
        for _, q in d[d.adel == adel].iterrows():
            pts = ' '.join(f'{xd[dd]:.1f},{ys(q[f"lift_{dd}"]):.1f}' for dd in (7, 30, 90))
            s.raw(f'<polyline points="{pts}" fill="none" stroke="{BLUE if adel else M2}" stroke-width="{0.9 if adel else 0.7}" stroke-opacity="{0.55 if adel else 0.6}"/>')
    mv = [med.loc[ch, f'lift_{dd}'] for dd in (7, 30, 90)]
    s.raw(f'<polyline points="{" ".join(f"{xd[dd]:.1f},{ys(v):.1f}" for dd, v in zip((7, 30, 90), mv))}" fill="none" stroke="{INK}" stroke-width="2.5"/>')
    for dd, v in zip((7, 30, 90), mv): s.circle(xd[dd], ys(v), 3.5, INK)
    s.t(xd[7] + 4, ys(mv[0]) - 8, f'{mv[0]:.1f}', 11.5, INK, 'start', 700, halo=True)
    s.t(xd[90] + 8, ys(mv[2]) + 4, f'{mv[2]:.1f}', 11.5, INK, 'start', 700, halo=True)
    gn = gro.loc[ch]
    s.t(xd[90] + 8, ys(mv[2]) + 18, 'no abre', 10.5, SEC, 'start', halo=True)
    s.t(xd[90] + 8, ys(mv[2]) + 30, f'x{gn.gn:.1f}', 10.5, SEC, 'start', halo=True)
    for (cc, n), yl in LB.items():
        if cc != ch: continue
        q = d[d.nom == n]
        if not len(q): continue
        q = q.sort_values('envios_usuario_dia').iloc[-1]
        pts = ' '.join(f'{xd[dd]:.1f},{ys(q[f"lift_{dd}"]):.1f}' for dd in (7, 30, 90))
        s.raw(f'<polyline points="{pts}" fill="none" stroke="{GREEN}" stroke-width="2.2"/>')
        s.line(xd[30], ys(yl) + 3, xd[30], ys(q.lift_30), M1, 0.8)
        s.t(xd[30] - 30, ys(yl), f'{n}: {q.lift_7:.1f} a {q.lift_90:.1f}', 10.5, GREEN, 'start', 600, halo=True)
s.t(0, 400, 'Veces = conversión de quien abre entre la de quien no abre. Campañas promocionales con 1,000 personas y 100 conversiones por lado.', 10.5, SEC)
s.t(0, 414, 'Escala logarítmica. Solo adelanta: 1.5 veces o más a 7 días y menos de 1.5 a 90. No abre: cuánto crece su compra de 7 a 90 días.', 10.5, SEC)

write(57, dict(
    titulo='Quien abre compra antes, pero no siempre más: a 90 días su ventaja se reduce a la mitad',
    que='Recordatorios de registro y de pago a meses, promociones de comercios y referidos.',
    quien=f'Sales ({eqp["Sales"]:.0f} % de su volumen solo adelanta), Marketing ({eqp["Marketing"]:.0f} %), Product Growth ({eqp["Product Growth"]:.0f} %).',
    a_quien='Clientes y registrados que ya iban a comprar o a terminar su registro.',
    lecturas=[
        f'En correo la ventaja baja de {med.loc["email","lift_7"]:.1f} a {med.loc["email","lift_90"]:.1f} veces; en push, de {med.loc["push notification","lift_7"]:.1f} a {med.loc["push notification","lift_90"]:.1f}; en WhatsApp, de {med.loc["whatsapp","lift_7"]:.1f} a {med.loc["whatsapp","lift_90"]:.1f}.',
        f'Quien no abre también compra después: su conversión crece {gro.gn.min():.1f} a {gro.gn.max():.1f} veces de 7 a 90 días.',
        f'{NA} de {N} campañas solo adelantan; en recordatorios, {tep["Recordatorio de algo empezado"]:.0f} % del volumen.',
    ],
    causa='Juzgamos cada campaña por cuánto compra quien la abre, sin un grupo que no reciba nada.',
    sowhat='Solo un grupo sin mensajes dice cuánto suma; lo que solo adelanta va por push e in-app.',
    fuente=f'Fuente: Braze, quien abre contra quien no abre a 7, 30 y 90 días por campaña y canal (E9a), enero a septiembre 2026. {VA/1e6:.0f} M de {V/1e6:.0f} M envíos medidos solo adelantan.',
    svg=s.svg()))
