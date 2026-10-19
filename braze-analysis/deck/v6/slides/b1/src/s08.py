"""Lámina 8: mensajes por persona en nueve meses (bandas de E3). Barras apiladas = millones de mensajes por canal en cada banda
(eje izquierdo); línea = porcentaje de personas con al menos una conversión (eje derecho). Debajo, personas y mensajes por persona."""
import pandas as pd
from comun import load, write, Svg, ROOT, INK, TXT, SEC, GRID, BLUE, GREEN, GREEN2, G2

e = pd.read_csv(ROOT / 'data/e3_usuarios_distribucion.csv')
e['cw'] = e.comms_distintas_prom * e.usuarios; e['dw'] = e.dias_con_envio_prom * e.usuarios
g = e.groupby('banda_msgs').agg(u=('usuarios', 'sum'), m=('msgs', 'sum'), em=('msgs_email', 'sum'), pu=('msgs_push', 'sum'), wa=('msgs_whatsapp', 'sum'),
                                ia=('msgs_inapp', 'sum'), b=('bajas_email', 'sum'), conv=('usuarios_con_conversion', 'sum'), cw=('cw', 'sum'), dw=('dw', 'sum'))
U, MS = g.u.sum(), g.m.sum()
B = ['01-05', '06-10', '11-20', '21-40', '41-80', '081-160', '161-320', '321+']
LAB = ['1 a 5', '6 a 10', '11 a 20', '21 a 40', '41 a 80', '81 a 160', '161 a 320', '321 o más']
g = g.loc[B]
g['conv_pct'] = 100 * g.conv / g.u; g['mpp'] = g.m / g.u; g['baja100'] = 100 * g.b / g.u; g['comms'] = g.cw / g.u; g['dias'] = g.dw / g.u
top = g.loc['321+']
etapa = e[e.banda_msgs == '321+'].groupby('etapa').usuarios.sum(); pros = etapa.get('7.Prospects', 0) / etapa.sum()
# Equipos: envíos con 3 o más mensajes a la misma persona en un mes (E1, filas con 10 mil o más personas)
d = load(); x = d[d.usuarios_aprox >= 10000]; x = x[x.envios / x.usuarios_aprox >= 3]
tq = x.groupby('equipo').envios.sum() / 1e6
f = d[d.usuarios_aprox >= 10000].groupby(['fam', 'canal']).agg(e=('envios', 'sum'), u=('usuarios_aprox', 'sum')); f['tpp'] = f.e / f.u
ej = lambda pat, can: f[f.index.get_level_values(0).str.contains(pat) & (f.index.get_level_values(1) == can)].sort_values('e').tpp.iloc[-1]
ej_com, ej_t0, ej_ver = ej('Comerciodeldia', 'push notification'), ej('Nuevos_RegistradosPay', 'email'), ej('Retargeting_Veriff', 'email')
print(g[['u', 'm', 'mpp', 'conv_pct', 'baja100', 'comms', 'dias']].round(2), U, MS, pros, tq.round(1).to_dict(), ej_com, ej_t0, ej_ver)

ORD = [('pu', 'Push', BLUE), ('em', 'Correo', G2), ('wa', 'WhatsApp', GREEN), ('ia', 'In-app', GREEN2)]
S = Svg('Millones de mensajes por canal según cuántos mensajes recibió cada persona en nueve meses, y porcentaje de personas con una conversión')
lx = 0
for k, lab, col in ORD:
    S.rect(lx, 12, 10, 10, col); S.t(lx + 15, 21, lab, 11.5, TXT); lx += 15 + len(lab) * 6.5 + 16
S.line(lx, 17, lx + 22, 17, INK, 2); S.circle(lx + 11, 17, 4, INK); S.t(lx + 28, 21, 'Personas con al menos una conversión', 11.5, INK, w=600)
S.t(0, 40, 'Cada columna junta a las personas según cuántos mensajes recibieron de enero a septiembre.', 10.5, SEC)
X0, X1, Y0, Y1 = 112, 724, 84, 330
step = (X1 - X0) / len(B); bw = step * 0.56
cx = lambda i: X0 + step * (i + 0.5)
VMAX, RMAX = 180, 90
vy = lambda v: Y1 - (Y1 - Y0) * v / VMAX
ry = lambda v: Y1 - (Y1 - Y0) * v / RMAX
S.t(X0 - 8, Y0 - 20, 'Millones de mensajes', 11, SEC)
S.t(X1 + 8, Y0 - 20, '% de personas', 11, INK, 'end', 600)
for v, r in zip((0, 60, 120, 180), (0, 30, 60, 90)):
    S.line(X0, vy(v), X1, vy(v), GRID)
    S.t(X0 - 8, vy(v) + 4, f'{v} M', 11, SEC, 'end'); S.t(X1 + 8, vy(v) + 4, f'{r} %', 11, INK)
for i, b in enumerate(B):
    base = 0
    for k, lab, col in ORD:
        v = g.loc[b, k] / 1e6; S.rect(cx(i) - bw / 2, vy(base + v), bw, max(0, vy(base) - vy(base + v) - 1.5), col); base += v
    hi = b == '321+'
    S.t(cx(i), vy(base) - 6, f'{base:.0f} M', 11.5 if hi else 11, INK if hi else SEC, 'middle', 700 if hi else 400, halo=True)
pts = [(cx(i), ry(g.loc[b, 'conv_pct'])) for i, b in enumerate(B)]
S.poly(pts, INK, 2.5)
for i, b in enumerate(B):
    hi = b == '321+'; v = g.loc[b, 'conv_pct']
    S.circle(pts[i][0], pts[i][1], 5.5 if hi else 4.5, INK)
    lab = f'{v:.0f} %' if v >= 1 else (f'{v:.1f} %' if v >= 0.1 else f'{v:.2f} %')
    S.t(pts[i][0] - 10, pts[i][1] - 8, lab, 12.5 if hi else 11.5, INK, 'end', 700 if hi else 600, halo=True)
# filas bajo el eje
S.t(X0 - 8, Y1 + 17, 'Mensajes recibidos', 11, SEC, 'end')
S.t(X0 - 8, Y1 + 33, 'Personas', 11, SEC, 'end')
S.t(X0 - 8, Y1 + 49, 'Por persona', 11, SEC, 'end')
S.t(X0 - 8, Y1 + 65, 'Bajas por cien', 11, SEC, 'end')
for i, b in enumerate(B):
    hi = b == '321+'; c_, w_ = (INK, 700) if hi else (TXT, 400)
    S.t(cx(i), Y1 + 17, LAB[i], 11.5, c_, 'middle', 600 if hi else 400)
    u = g.loc[b, 'u']
    S.t(cx(i), Y1 + 33, f'{u / 1e6:.1f} M' if u >= 1e6 else f'{u / 1e3:.0f} mil', 11, c_, 'middle', w_)
    S.t(cx(i), Y1 + 49, f'{g.loc[b, "mpp"]:.0f}', 11, c_, 'middle', w_)
    S.t(cx(i), Y1 + 65, f'{g.loc[b, "baja100"]:.1f}', 11, c_, 'middle', w_)

pct = lambda a: f'{a * 100:.0f} %'
write(8, dict(kind='grafica',
    titulo=f'El promedio esconde a {top.u / 1e3:.0f} mil personas que reciben casi dos mensajes al día, y son las que más convierten',
    que=(f'Sobre todo push ({pct(top.pu / top.m)} de lo que recibe la banda de 321 o más). Lo que más se repite al mes: push Comercio del día de Marketing ({ej_com:.1f} por persona) '
         f'y correo Tasa 0 a nuevos registrados de Product Growth ({ej_t0:.1f}).'),
    quien=(f'Envíos con 3 o más mensajes a la misma persona en un mes: Marketing {tq["Marketing"]:.0f} M, Product Growth {tq["Product Growth"]:.0f} M, Collections {tq["Collections"]:.0f} M '
           f'(cobranza, procede), Sales {tq["Sales"]:.0f} M y Others {tq["Others"]:.0f} M.'),
    a_quien=(f'A las personas más activas: {top.conv_pct:.0f} % de la banda de 321 o más tuvo una conversión; {pct(pros)} aparece en Braze como registrada sin crédito '
             '(etapa por confirmar).'),
    lecturas=[
        f'{pct(g.loc["01-05", "u"] / U)} de las personas ({g.loc["01-05", "u"] / 1e6:.1f} M) recibe de 1 a 5 mensajes en nueve meses. El promedio, {MS / U:.0f} mensajes por persona, lo jalan las columnas de la derecha.',
        f'La banda de 321 o más: {top.u / 1e3:.0f} mil personas ({pct(top.u / U)} de la base) reciben {top.m / 1e6:.0f} M mensajes ({pct(top.m / MS)} del total), {top.mpp:.0f} cada una. Entran a {top.comms:.0f} campañas distintas y reciben algo {top.dias:.0f} de los 273 días.',
        f'Son las que más convierten y las que más se cansan: {top.baja100:.1f} bajas de correo por cada 100 personas, contra {g.loc["01-05", "baja100"]:.1f} en la banda de 1 a 5.'],
    causa='Cada campaña decide sola a quién entra y no hay límite de mensajes por persona a la semana: quien más usa la app cumple las condiciones de muchas campañas a la vez y le llegan todas. Push domina porque no cuesta y nadie lo limita.',
    sowhat='Estamos saturando a los mejores clientes: un límite de 5 promociones por persona a la semana los protege sin dejar de escribirles.',
    fuente=(f'Fuente: Braze, mensajes por persona y banda (E3), enero a septiembre 2026: {U / 1e6:.1f} M personas y {MS / 1e6:.0f} M mensajes (E3 cuenta duplicados del mismo día que E1 quita). '
            'Conversión = persona con al menos una solicitud o préstamo atribuido; bajas = eventos de baja de correo por cada 100 personas. Equipos con E1 (filas con 10 mil o más personas): E3 no trae equipo.'),
    svg=S.done()))
