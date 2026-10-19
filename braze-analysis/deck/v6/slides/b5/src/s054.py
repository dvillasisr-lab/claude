"""Lámina 54: quién tiene la app. Cifra grande (piso: abrió un push o hizo clic en un in-app en nueve meses, E7b) con piso y techo
(E7b, E9b, E4a) y, por grupo, cuántos de cada 100 que reciben el correo de una campaña reciben su push, ven su in-app y abren el push (E1).
with_app y app_uninstall del golden dataset: E17."""
import pandas as pd
from b5_svg import *

E7, E9, E4, AL = D['e7b'], D['e9b'], D['e4a'], D['alcance']
e17 = pd.read_csv('/home/user/claude/braze-analysis/data/e17_contactable.csv'); p17 = e17[e17.canal == 'push notification']
ap_un = {k: 100 * g.respuestas.sum() / g.envios.sum() for k, g in p17.groupby('app_uninstall')}
rng = lambda c, excl=(): (min(v for m, v in E4[c].items() if m not in excl), max(v for m, v in E4[c].items() if m not in excl))
push_r, inapp_r, mail_r = rng('push notification'), rng('in-app'), rng('email', ('06',))
tot = E7['tot']['usuarios']; tot9 = E9['tot']['usuarios']
S = Svg('Piso de personas con la app: 3.2 millones abrieron un push o hicieron clic en un in-app en nueve meses. Piso y techo por periodo, y por grupo cuántos de cada 100 que reciben el correo de una campaña reciben su push, ven su in-app y abren el push.')
# ---------- izquierda: cifra grande y piso / techo ----------
S.t(0, 50, f'{M(E7["push_o_inapp"])} M', 50, INK, w=700)
S.t(0, 74, f'personas abrieron un push o hicieron clic en un in-app', 12, INK, w=600)
S.t(0, 90, f'en nueve meses: {100*E7["push_o_inapp"]/tot:.0f} % de las {M(tot)} M que recibieron algo', 12, TXT)
S.line(0, 108, 330, 108, GRID)
S.t(0, 128, 'Piso y techo de quién tiene la app, M personas', 11.5, INK, w=600)
X0, X1, VM = 150, 290, 6
sx = lambda v: X0 + (X1 - X0) * (v / 1e6 if v > 100 else v) / VM
ROWS = [('Piso, 9 meses', [('Abrió un push', E7['abre_push'], None, BLUEL), ('Abrió push o clic in-app', E7['push_o_inapp'], None, BLUE)]),
        ('Piso, últimos 90 días', [('Abrió un push', E9['abre_push'], None, BLUEL), ('Abrió push o clic in-app', E9['push_o_inapp'], None, BLUE)]),
        ('Techo, cada mes', [('Le llega un push', push_r[0], push_r[1], MARK), ('Ve un in-app', inapp_r[0], inapp_r[1], MARK), ('Recibe un correo', mail_r[0], mail_r[1], MARK2)])]
for v in (0, 2, 4, 6):
    S.line(sx(v), 150, sx(v), 146 + 3 * 18 + 7 * 19 - 8, GRID)
y = 146
for head, items in ROWS:
    S.t(0, y + 4, head, 10.5, SEC, w=600); y += 10
    for lab, a, b, col in items:
        S.t(X0 - 8, y + 11, lab, 10.5, TXT, 'end')
        if b is None:
            S.rect(X0, y + 2, sx(a) - X0, 12, col); S.t(sx(a) + 5, y + 12, f'{a/1e6:.2f} M' if a < 1.5e6 else f'{a/1e6:.1f} M', 10.5, INK, w=600, halo=True)
        else:
            S.rect(sx(a), y + 2, sx(b) - sx(a), 12, col); S.t(sx(b) + 5, y + 12, f'{a/1e6:.1f} a {b/1e6:.1f} M', 10.5, INK, w=600, halo=True)
        y += 19
    y += 8
for v in (0, 2, 4, 6):
    S.t(sx(v), y + 4, f'{v} M' if v else '0', 10.5, SEC, 'middle')
# ---------- derecha: por grupo ----------
RX = 372
S.line(RX - 20, 10, RX - 20, 410, GRID)
S.t(RX, 18, 'De cada 100 personas que reciben el correo de una campaña', 12, INK, w=600)
lx = RX
for lab, col in [('Le llega su push', BLUEL), ('Ve su in-app', BLUE), ('Abre el push', GREEN)]:
    S.rect(lx, 30, 10, 10, col); S.t(lx + 14, 39, lab, 11, TXT); lx += 14 + len(lab) * 6.2 + 16
GR = [('activos', 'Activos y recurrentes'), ('leads', 'Leads y registrados'), ('ex', 'Ex clientes inactivos'), ('nunca', 'Leads que nunca activaron'), ('nuevos', 'Nuevos y onboarding')]
GX0, GX1, GM = RX + 2, W - 40, 70
gx = lambda v: GX0 + (GX1 - GX0) * v / GM
y = 60
for g, lab in GR:
    cold = g in ('ex', 'nunca')
    S.t(RX, y + 10, lab, 11.5, INK, w=600 if cold else 400)
    for j, (k, col) in enumerate([('push', BLUEL), ('inapp', BLUE), ('abre', GREEN)]):
        v = AL[g][k]; yy = y + 17 + j * 13
        S.rect(GX0, yy, max(gx(v) - GX0, 1.5), 10, col)
        S.t(gx(v) + 5, yy + 9, f'{v:.0f}' if v >= 1.95 else f'{v:.1f}', 10.5, INK if cold else TXT, w=600 if cold else 400)
    y += 66
S.t(RX, HH - 20, 'Solo campañas con correo y push el mismo mes. Personas sumadas', 10.5, SEC)
S.t(RX, HH - 6, 'entre campañas: sirve como proporción, no como conteo.', 10.5, SEC)
SVG = S.done()

pi_conv = 100 * E7['push_o_inapp_conv'] / E7['tot']['conv']
b9, b23 = D['alc_fam']['b0209'], D['alc_fam']['b0223']; an = D['b0171_anon_push']
guarda(54, dict(
    kind='grafica',
    titulo='Solo una de cada seis personas abrió un push o un in-app en nueve meses: es el piso de quién tiene la app',
    que='Push e in-app, de recuperación y de promociones: los canales que no cuestan. Sin app no hay push ni in-app; a esas personas solo les llega correo o WhatsApp.',
    quien=f'Todos los equipos. Marketing manda los push de oferta más grandes: el rescate con Tasa 0 a anónimos mandó {M(an["env"])} M push a {M(an["usr"])} M personas y abre {an["ap"]:.2f} %.',
    a_quien=f'Activos, leads, ex clientes y leads que nunca activaron. El push del descuento a inactivos (B0209) llega a {b9["push"]:.0f} de cada 100 que reciben su correo; el de Installments a never active (B0223), a {b23["push"]:.0f}.',
    lecturas=[
        f'Piso: {M(E7["abre_push"], 2)} M personas abrieron al menos un push en nueve meses ({100*E7["abre_push"]/tot:.1f} %). Con quien hizo clic en un in-app, que solo se ve dentro de la app: {M(E7["push_o_inapp"])} M; en 90 días, {M(E9["push_o_inapp"])} M ({100*E9["push_o_inapp"]/tot9:.0f} %). Son {pi_conv:.0f} % de quienes convirtieron.',
        f'Techo: Braze solo manda push a quien tiene la app registrada. Cada mes le llega un push a {push_r[0]/1e6:.1f} a {push_r[1]/1e6:.1f} M personas y ve un in-app {inapp_r[0]/1e6:.1f} a {inapp_r[1]/1e6:.1f} M, contra {mail_r[0]/1e6:.1f} a {mail_r[1]/1e6:.1f} M que reciben correo.',
        f'De cada 100 que reciben el correo de una campaña, en activos {AL["activos"]["push"]:.0f} reciben su push y {AL["activos"]["inapp"]:.0f} ven su in-app; en ex clientes {AL["ex"]["push"]:.0f} y {AL["ex"]["inapp"]:.0f}; en leads que nunca activaron {AL["nunca"]["push"]:.0f} y {AL["nunca"]["inapp"]:.0f}.',
    ],
    causa=f'Braze no tiene un dato confiable de quién tiene la app. with_app y app_uninstall del golden dataset no sirven: el push a quien aparece con la app desinstalada abre {ap_un[True]:.2f} %, casi igual que el resto ({ap_un[False]:.2f} %).',
    sowhat='Pedir a Datos tres atributos diarios en Braze: tiene la app, entró a la app en los últimos 30 días y tiene el push activado. Con eso se elige el canal de cada persona.',
    fuente='Fuente: Braze E7b y E9b (respuesta por persona en nueve meses y en 90 días), E4a (personas por canal al mes; junio fuera del correo por el envío de BillPay a toda la base), E1 (personas por campaña, canal y mes) y E17 (banderas del golden dataset), enero a septiembre 2026. Es una estimación: el piso cuenta solo a quien respondió y el techo a quien tiene la app registrada.',
    svg=SVG,
))
print(push_r, inapp_r, mail_r, ap_un, pi_conv)
