"""Lámina 6: promociones contra avisos de servicio y cobranza. Izquierda: parte de cada tipo en mensajes, gasto y conversiones.
Derecha: respuesta de cada tipo (pequeños múltiplos, cada grupo con su escala). Tipo por la regla del Sheets (base_p1)."""
from comun import load, write, Svg, INK, TXT, SEC, BLUE, GREEN, G1, GRID, FUENTE_E1, COSTO

d = load()
TIP = [('promocional', 'Promoción', BLUE), ('transaccional', 'Aviso de servicio', GREEN), ('cobranza', 'Cobranza', G1)]
t = d.groupby('tipo').agg(env=('envios', 'sum'), cost=('costo', 'sum'), conv=('conversiones_fraccional', 'sum'),
                          ed=('email_delivery', 'sum'), ec=('email_click', 'sum'), ps=('pn_send', 'sum'), po=('pn_open', 'sum'),
                          eu=('email_unsubscribe', 'sum'))
sh = t[['env', 'cost', 'conv']] / t[['env', 'cost', 'conv']].sum()
m = {'clic': 1000 * t.ec / t.ed, 'push': 1000 * t.po / t.ps, 'conv': 1000 * t.conv / t.env, 'baja': 1000 * t.eu / t.ed}
p = d[d.tipo == 'promocional']
gan = p.groupby('gan').envios.sum() / p.envios.sum()
peq = p.groupby('equipo').envios.sum() / p.envios.sum()
pau = p.groupby('aud').envios.sum() / p.envios.sum(); pauc = p.groupby('aud').costo.sum() / p.costo.sum()
wa99 = d[(d.canal == 'whatsapp')].groupby('tipo').envios.sum(); wa99 = wa99['promocional'] / wa99.sum()
ia99 = d[(d.canal == 'in-app')].groupby('tipo').envios.sum(); ia99 = ia99['promocional'] / ia99.sum()
print(sh.round(3), {k: v.round(1).to_dict() for k, v in m.items()}, gan.round(3).to_dict(), peq.round(3).to_dict(), pau.round(3).to_dict(), pauc.round(3).to_dict(), wa99, ia99)

S = Svg('Parte de promociones, avisos de servicio y cobranza en mensajes, gasto y conversiones atribuidas, y la respuesta de cada tipo')
x = 0
for k, lab, col in TIP:
    S.rect(x, 4, 10, 10, col); S.t(x + 15, 13, lab, 11.5, TXT); x += 15 + len(lab) * 6.3 + 20
# --- izquierda: barras al 100 %
S.t(0, 44, 'Parte de cada tipo de mensaje', 11.5, INK, w=600)
Y0, Y1 = 64, 372; BW = 62
COLS = [('env', 'Mensajes'), ('cost', 'Gasto en MXN'), ('conv', 'Conversiones'), ]
for i, (k, lab) in enumerate(COLS):
    x0 = 8 + i * 110; top = Y0; small = []
    for tk, tl, col in TIP:
        v = sh.loc[tk, k]; h = (Y1 - Y0) * v
        S.rect(x0, top, BW, h - 2, col)
        if h > 20:
            S.t(x0 + BW / 2, top + h / 2 + 4, f'{v * 100:.0f} %', 11.5 if tk != 'promocional' else 13, '#FFFFFF' if tk != 'cobranza' else INK, 'middle', 600)
        else:
            small.append([top + h / 2 + 4, f'{v * 100:.0f} %'])
        top += h
    for j in range(len(small) - 2, -1, -1):  # separa etiquetas chicas de abajo hacia arriba
        small[j][0] = min(small[j][0], small[j + 1][0] - 13)
    for yy, s_ in small:
        S.t(x0 + BW + 5, yy, s_, 10.5, SEC, 'start')
    S.t(x0 + BW / 2, Y1 + 18, lab, 11.5, INK if k == 'cost' else TXT, 'middle', 600 if k == 'cost' else 400)
S.t(8 + 2 * 110 + BW / 2, Y1 + 33, 'atribuidas', 11.5, TXT, 'middle')
# --- derecha: respuesta por tipo, cada grupo con su escala
X0, XW = 372, 350
S.t(X0, 44, 'Respuesta de cada tipo de mensaje', 11.5, INK, w=600)
GR = [('clic', 'Clics por cada mil correos entregados', 1), ('push', 'Aperturas por cada mil push', 1),
      ('conv', 'Conversiones atribuidas por cada mil mensajes', 1), ('baja', 'Bajas por cada mil correos entregados', 1)]
y = 70
for gk, glab, dec in GR:
    S.t(X0, y, glab, 11, TXT if gk != 'baja' else SEC, w=600 if gk in ('clic', 'push') else 400)
    vmax = max(m[gk]); y += 8
    for tk, tl, col in TIP:
        v = m[gk][tk]; w = XW * v / vmax
        S.rect(X0, y, w, 13, col)
        S.t(X0 + w + 6, y + 11, f'{v:.{dec}f}', 11, INK if tk == 'promocional' else SEC, 'start', 700 if tk == 'promocional' else 400)
        y += 16
    y += 30
S.line(X0, 56, X0, 368, GRID)

r_clic = m['clic']['transaccional'] / m['clic']['promocional']; r_push = m['push']['transaccional'] / m['push']['promocional']
print('veces', r_clic, r_push, m['conv']['transaccional'] / m['conv']['promocional'])
write(6, dict(kind='grafica',
    titulo='Nueve de cada diez pesos se van en promociones, que por correo y push responden casi cinco veces menos que los avisos de servicio',
    que=(f'Promoción: Tasa 0 ({gan["tasa0"] * 100:.0f} % del volumen promocional), referidos ({gan["referidos"] * 100:.0f} %), recordatorios de algo empezado ({gan["recordatorio"] * 100:.0f} %), '
         f'descuentos ({gan["descuento"] * 100:.0f} %) y lanzamientos ({gan["lanzamiento"] * 100:.0f} %). Avisos: confirmación de pago, contratos, desembolso. Cobranza: antes y después del vencimiento.'),
    quien=(f'Promoción: Marketing {peq["Marketing"] * 100:.0f} % del volumen promocional, Product Growth {peq["Product Growth"] * 100:.0f} %, Sales {peq["Sales"] * 100:.0f} % y Others {peq["Others"] * 100:.0f} %. '
           'Avisos de servicio: Others (avisos de KPay y KCash). Cobranza: Collections.'),
    a_quien=(f'Promoción: leads {pau["leads"] * 100:.0f} % del volumen promocional, clientes activos {pau["activos"] * 100:.0f} %, ex clientes y leads que nunca activaron '
             f'{pau["frios"] * 100:.0f} % (pero {pauc["frios"] * 100:.0f} % del gasto promocional).'),
    lecturas=[
        f'Las promociones son {sh.loc["promocional", "env"] * 100:.0f} % de los mensajes y {sh.loc["promocional", "cost"] * 100:.0f} % del gasto ({t.cost["promocional"] / 1e6:.1f} M MXN en nueve meses), pero traen {sh.loc["promocional", "conv"] * 100:.0f} % de las conversiones. Los avisos son {sh.loc["transaccional", "env"] * 100:.0f} % de los mensajes y traen {sh.loc["transaccional", "conv"] * 100:.0f} %.',
        f'Por correo, una promoción tiene {m["clic"]["promocional"]:.0f} clics por cada mil correos y un aviso {m["clic"]["transaccional"]:.0f}. Por push, {m["push"]["promocional"]:.0f} aperturas por cada mil contra {m["push"]["transaccional"]:.0f}. El aviso de pago de KPay tiene 38 clics por cada mil correos.',
        f'Las promociones también provocan más bajas: {m["baja"]["promocional"]:.1f} por cada mil correos contra {m["baja"]["transaccional"]:.1f} de los avisos. Casi todo el WhatsApp y el in-app ({min(wa99, ia99) * 100:.0f} %) es promoción.'],
    causa='Las promociones salen a listas grandes aunque la persona no haya hecho nada; los avisos salen porque hizo algo (pagó, firmó, recibió su préstamo) y por eso los espera y los abre.',
    sowhat='El gasto y la mejora están en las promociones; los avisos de servicio y la cobranza quedan fuera del límite de mensajes por persona.',
    fuente=(f'{FUENTE_E1}. Tipo por la regla del Sheets: Collections = cobranza; nombre que empieza con "Transaccional" o sin ticket = aviso; lo demás, promoción (algunas sin ticket no son avisos). '
            f'Conversión atribuida = conversiones fraccionales de E1. {COSTO}.'),
    svg=S.done()))
