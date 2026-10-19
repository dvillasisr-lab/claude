"""Lámina 40 (base v5 lámina 6): regresión semanal, volumen del canal en la semana contra su respuesta; email y push (E4a, deck_data).
Semanas de junio en rombo azul; semanas de lanzamiento etiquetadas con lo que salió (E1 con primer y último envío de E2)."""
import sys, pandas as pd
from kit import *
sys.path.insert(0, R + 'scripts')
import deck_data as dd
reg = dd.regresion_semana()
def sinjun(c):
    pts = [p for p in reg[c]['pts'] if not p['lab'].startswith('06')]
    return dd._ols([p['x'] for p in pts], [p['y'] for p in pts])
fe, fp, fw = reg['email']['fit'], reg['push notification']['fit'], reg['whatsapp']['fit']; fe2, fp2 = sinjun('email'), sinjun('push notification')
# respuesta en las semanas de lanzamiento contra el resto (E4a)
e = pd.read_csv(D + 'e4a_serie_semana_mes_canal.csv'); w = e[(e.grano == 'semana') & (e.periodo >= '2026-01-05') & (e.periodo <= '2026-09-21')]
PK = ['2026-05-25', '2026-06-01', '2026-06-15', '2026-07-20', '2026-08-10']
def resp(c, r, b):
    d = w[w.canal == c]; k = d.periodo.isin(PK)
    return 100 * d[k][r].sum() / d[k][b].sum(), 100 * d[~k][r].sum() / d[~k][b].sum()
pk_p, ot_p = resp('push notification', 'pn_open', 'pn_send'); pk_e, ot_e = resp('email', 'email_click', 'email_delivery')
print({k: round(v, 3) for k, v in fe.items()}, {k: round(v, 3) for k, v in fe2.items()}, {k: round(v, 3) for k, v in fp.items()}, round(fw['r2'], 3), pk_p, ot_p, pk_e, ot_e)

S = Svg('Dos paneles de dispersión semanal con recta: millones de correos en la semana contra clic, y millones de push en la semana contra apertura; semanas de junio en rombo')
S.raw(f'<circle cx="6" cy="15" r="4" fill="{G1}"/>'); S.t(15, 19, 'Semana de enero a septiembre', 11, TXT)
S.raw(f'<path d="M 190 10 L 195 15 L 190 20 L 185 15 Z" fill="{BLUE}"/>'); S.t(200, 19, 'Semana de junio', 11, TXT)
S.line(300, 15, 322, 15, INK, 1.8); S.t(328, 19, 'Recta de mínimos cuadrados (38 semanas)', 11, INK, w=600)

def panel(x0, c, fit, fit2, xmax, xt, ymax, yt, title, xlab, labels):
    X0, X1, Y0, Y1 = x0 + 38, x0 + 362, 78, 350
    sx = lambda v: X0 + (X1 - X0) * v / xmax; sy = lambda v: Y1 - (Y1 - Y0) * v / ymax
    S.t(x0, 46, title, 12, INK, w=700)
    S.t(x0, 62, f'Cada millón más en la semana: {fit["b"]:.2f} puntos. R² {fit["r2"]:.2f}; sin junio, R² {fit2["r2"]:.2f}', 10.5, SEC)
    for v in yt:
        S.line(X0, sy(v), X1, sy(v)); S.t(X0 - 6, sy(v) + 4, f'{v:g} %', 10.5, SEC, 'end')
    for v in xt:
        S.line(sx(v), Y1, sx(v), Y1 + 5, SEC); S.t(sx(v), Y1 + 18, f'{v} M', 10.5, SEC, 'middle')
    S.line(X0, Y1, X1, Y1, SEC)
    S.t((X0 + X1) / 2, Y1 + 34, xlab, 10.5, SEC, 'middle')
    xa, xb = 0.5, xmax * 0.98
    ya, yb = fit['a'] + fit['b'] * xa, fit['a'] + fit['b'] * xb
    if yb < 0: xb = -fit['a'] / fit['b']; yb = 0
    S.line(sx(xa), sy(ya), sx(xb), sy(yb), INK, 1.8)
    for q in sorted(reg[c]['pts'], key=lambda q: q['lab'].startswith('06')):
        x, y = sx(q['x']), sy(q['y'])
        if q['lab'].startswith('06'):
            S.raw(f'<path d="M {x:.1f} {y-6:.1f} L {x+6:.1f} {y:.1f} L {x:.1f} {y+6:.1f} L {x-6:.1f} {y:.1f} Z" fill="{BLUE}" stroke="#FFFFFF" stroke-width="1.5"/>')
        else:
            S.circle(x, y, 4, G1, '#FFFFFF', 1.5)
    for lab, dx, dy, anchor, l1, l2 in labels:
        q = next(p for p in reg[c]['pts'] if p['lab'] == lab); x, y = sx(q['x']), sy(q['y'])
        S.t(x + dx, y + dy, l1, 10.5, INK, anchor, 700, halo=True)
        if l2: S.t(x + dx, y + dy + 13, l2, 10.5, TXT, anchor, 400, halo=True)

panel(0, 'email', fe, fe2, 27, (5, 10, 15, 20, 25), 1.6, (0, 0.5, 1, 1.5), 'Correo: enviados en la semana contra clic',
      'Millones de correos enviados en la semana', [
       ('06/01', -8, -26, 'end', '1 jun: 25 M correos, 0.36 %', 'BillPay Intro a 16.1 M'),
       ('05/25', 4, 22, 'start', '25 may: 0.73 %', 'Hot Sale y Referidos')])
panel(400, 'push notification', fp, fp2, 14, (2, 4, 6, 8, 10, 12), 3.0, (0, 1, 2, 3), 'Push: enviados en la semana contra apertura',
      'Millones de push enviados en la semana', [
       ('06/15', -4, -40, 'end', '15 jun: 13 M push, 0.92 %', 'Billpayments, Día del Padre'),
       ('07/20', -6, 26, 'end', '20 jul: 1.35 %', 'Comercio del día'),
       ('08/10', 4, -22, 'start', '10 ago:', 'prueba de QA')])

write(40, dict(kind='grafica', seccion='V. El ritmo lo marcan los lanzamientos, no el cliente',
 titulo=f'Las semanas con más mensajes son semanas de lanzamientos, y en ellas la respuesta cae: cada millón de correos de más baja el clic {abs(fe["b"]):.2f} puntos',
 que='Lanzamientos y campañas de temporada a casi toda la base: BillPay, Hot Sale, Comercio del día, Mundial y Día del Padre, Anota y Gana y regreso a clases. Promocional.',
 quien='Marketing está en las cinco semanas pico y NewProducts explica la más grande (BillPay Intro); Sales en Hot Sale y regreso a clases. Junio tuvo 44 M mensajes más que el promedio de enero a abril: 26 M de NewProducts y 20 M de Marketing.',
 a_quien='Envíos a toda la base, leads y recurrentes de KPay.',
 lecturas=[
  f'Con 5 M correos en la semana se espera {fe["a"]+fe["b"]*5:.2f} % de clic; con 25 M, {fe["a"]+fe["b"]*25:.2f} %. Sin las semanas de junio la relación se mantiene (R² {fe2["r2"]:.2f}): no es solo BillPay.',
  f'En las cinco semanas de lanzamientos el push abrió {pk_p:.2f} % contra {ot_p:.2f} % el resto, y el clic de correo fue {pk_e:.2f} % contra {ot_e:.2f} %.',
  f'En WhatsApp el volumen no mueve la lectura (R² {fw["r2"]:.2f}). En las semanas pico entra gente que casi nunca responde: es volumen más audiencia fría.',
 ],
 causa='Cada equipo fija la fecha de su lanzamiento sin ver la de los demás, y los lanzamientos salen a toda la base la misma semana.',
 sowhat='El volumen no se decide semana a semana: se acumula porque nadie ve el calendario completo de lanzamientos.',
 fuente='Fuente: Braze, E4a por semana y canal, 38 semanas completas (5 de enero a 21 de septiembre 2026); clic sobre correos entregados y apertura sobre push enviados. Es correlación, no un experimento. Campañas de cada semana: E1 con primer y último envío de E2 (campañas que duran 10 días o menos).',
 svg=S.svg()))
