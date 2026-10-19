"""Lámina 5: cuánto cuesta Braze en mensajes (cifra grande) y el embudo por canal con su gasto. E1 con base_p1; personas de E3."""
import pandas as pd
from comun import load, write, ROOT, BLUE, INK, SEC, FUENTE_E1, COSTO

d = load()
s = d[['email_sent', 'email_delivery', 'email_open', 'email_click', 'pn_send', 'pn_open', 'whatsapp_send', 'whatsapp_delivery',
       'whatsapp_read', 'in_app_impression', 'in_app_click', 'envios', 'costo', 'conversiones_fraccional']].sum() / 1e6
cv = d.groupby('canal').conversiones_fraccional.sum() / 1e6
cs = d.groupby('canal').costo.sum() / 1e6
ce = d.groupby('canal').envios.sum() / d.envios.sum()
eq = (d.groupby('equipo').envios.sum() / d.envios.sum()).sort_values(ascending=False)
fams, comms = d.fam.nunique(), d.communication_id.nunique()
e3 = pd.read_csv(ROOT / 'data/e3_usuarios_distribucion.csv'); pers = e3.usuarios.sum()
p15 = e3[e3.banda_msgs == '01-05'].usuarios.sum() / pers
mes = s.costo / 9
print(s.round(2).to_dict(), cv.round(3).to_dict(), cs.round(2).to_dict(), eq.round(3).to_dict(), fams, comms, pers, p15)

def barras():
    """Tres barras al 100 %: parte de cada canal en mensajes, gasto y conversiones atribuidas."""
    from comun import Svg, TXT, GREEN, GREEN2, G2
    ORD = [('email', 'Correo', G2), ('push notification', 'Push', BLUE), ('whatsapp', 'WhatsApp', GREEN), ('in-app', 'In-app', GREEN2)]
    env = d.groupby('canal').envios.sum(); env = env / env.sum()
    gas = cs / cs.sum(); con = cv / cv.sum()
    S = Svg('Parte de cada canal en los mensajes, el gasto y las conversiones atribuidas', 780, 106)
    x = 0
    for k, lab, col in ORD:
        S.rect(x, 2, 10, 10, col); S.t(x + 15, 11, lab, 11.5, TXT); x += 15 + len(lab) * 6.6 + 18
    X0, X1 = 170, 776
    for i, (lab, ser) in enumerate([('Mensajes', env), ('Gasto en MXN', gas), ('Conversiones atribuidas', con)]):
        y = 24 + i * 28; base = X0
        S.t(X0 - 10, y + 14, lab, 11.5, INK if i == 1 else TXT, 'end', 600 if i == 1 else 400)
        for k, _, col in ORD:
            v = float(ser.get(k, 0)); w = (X1 - X0) * v
            if w <= 0: continue
            S.rect(base, y, w - 2, 20, col)
            if w > 34:
                S.t(base + w / 2, y + 14, f'{v * 100:.0f} %', 11.5, '#FFFFFF' if col in (BLUE, GREEN) else INK, 'middle', 600)
            base += w
    return S.done().replace('<svg ', '<svg style="height:auto;width:100%;margin-top:.7cqi" ', 1)

M = lambda v: f'{v:.1f} M'
NA = f'<span style="color:{SEC}">no aplica</span>'
ND = f'<span style="color:{SEC}">sin dato</span>'
def tr(c, cells, bold=False):
    st = ' style="font-weight:700"' if bold else ''
    return f'<tr{st}><td>{c}</td>' + ''.join(f'<td class="num">{x}</td>' for x in cells) + '</tr>'
html = (
    f'<div style="display:flex;align-items:baseline;gap:1.4cqi;margin-bottom:.6cqi"><div class="big">{mes:.1f} M MXN</div>'
    f'<div class="bigl" style="margin:0">al mes solo en mensajes, sin contar la licencia de Braze.<br>{s.costo:.1f} M MXN de enero a septiembre.</div></div>'
    '<table><tr><th>Canal</th><th class="num">Enviados</th><th class="num">Entregados</th><th class="num">Abiertos, leídos o vistos</th>'
    '<th class="num">Clics</th><th class="num">Conversiones atribuidas</th><th class="num">Gasto en 9 meses</th></tr>'
    + tr('Correo', [M(s.email_sent), M(s.email_delivery), M(s.email_open), M(s.email_click), f'{cv["email"]:.2f} M', f'{cs["email"]:.1f} M MXN'])
    + tr('Push', [M(s.pn_send), ND, M(s.pn_open), NA, f'{cv["push notification"]:.2f} M', '0 MXN'])
    + tr('WhatsApp', [M(s.whatsapp_send), M(s.whatsapp_delivery), M(s.whatsapp_read), NA, f'{cv["whatsapp"]:.2f} M',
                      f'<span style="color:{BLUE};font-weight:700">{cs["whatsapp"]:.1f} M MXN</span>'])
    + tr('In-app', [M(s.in_app_impression), NA, M(s.in_app_impression), M(s.in_app_click), f'{cv["in-app"]:.2f} M', '0 MXN'])
    + tr('Total', [M(s.envios), '', '', '', f'{s.conversiones_fraccional:.2f} M', f'{s.costo:.1f} M MXN'], bold=True)
    + '</table>'
    + barras())

write(5, dict(kind='html',
    titulo=f'Braze nos cuesta {mes:.1f} M MXN al mes solo en mensajes, sin contar la licencia, y la mayor parte se va en WhatsApp',
    que=f'{s.envios:.0f} M mensajes en nueve meses: {ce["email"] * 100:.0f} % correo, {ce["push notification"] * 100:.0f} % push, {ce["whatsapp"] * 100:.0f} % WhatsApp y {ce["in-app"] * 100:.0f} % in-app.',
    quien=(f'Cinco equipos desde unas {round(fams, -2):,.0f} campañas con todas sus versiones ({comms:,} si cada versión mensual cuenta aparte). '
           f'Marketing manda {eq["Marketing"] * 100:.0f} %, Product Growth {eq["Product Growth"] * 100:.0f} %, Others {eq["Others"] * 100:.0f} %, Sales {eq["Sales"] * 100:.0f} % y Collections {eq["Collections"] * 100:.0f} %.'),
    a_quien=f'{pers / 1e6:.1f} M personas recibieron al menos un mensaje; {p15 * 100:.0f} % de ellas recibió de 1 a 5 en nueve meses.',
    html=html,
    lecturas=[
        f'WhatsApp es {ce["whatsapp"] * 100:.0f} % de los mensajes y {cs["whatsapp"] / s.costo * 100:.0f} % del gasto: {cs["whatsapp"]:.1f} M MXN por {s.whatsapp_delivery:.0f} M mensajes entregados. El correo pone el resto, {cs["email"]:.1f} M MXN.',
        f'De cada mil correos entregados, {1000 * s.email_open / s.email_delivery:.0f} se abren y {1000 * s.email_click / s.email_delivery:.0f} tienen clic. De cada mil push se abren {1000 * s.pn_open / s.pn_send:.0f}. In-app no cuesta y {100 * s.in_app_click / s.in_app_impression:.0f} de cada 100 vistas tienen clic.',
        f'{s.conversiones_fraccional:.1f} M conversiones atribuidas: solicitud o préstamo en los 7 días siguientes, repartida entre los mensajes de ese día. Sirve de referencia, no prueba que el mensaje vendió.'],
    causa=f'El gasto se reparte entre cinco equipos y unas {round(fams, -2):,.0f} campañas, y no hay presupuesto de mensajes por equipo: cada quien ve su campaña y nadie ve el total.',
    sowhat='Es un gasto del tamaño de una línea de negocio y nadie lo ve completo: necesita un dueño y un presupuesto por equipo.',
    fuente=f'{FUENTE_E1} (E1); personas de E3. {COSTO}. Conversión atribuida = conversiones fraccionales de E1. El costo fijo de Braze (licencia) no está incluido. Campañas = nombre sin la fecha. Tabla en millones de mensajes salvo el gasto; push no reporta entregados; el total incluye 0.2 M de banners.'))
