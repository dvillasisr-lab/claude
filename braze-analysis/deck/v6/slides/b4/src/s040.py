"""Lámina 40: volumen semanal y clic de email (E4a), semanas pico con sus lanzamientos (E1 con E2) y regresión (deck_data)."""
import sys, pandas as pd
from kit import *
sys.path.insert(0, R + 'scripts')
import deck_data as dd
e = pd.read_csv(D + 'e4a_serie_semana_mes_canal.csv'); w = e[(e.grano == 'semana') & (e.periodo >= '2026-01-05') & (e.periodo <= '2026-09-21')]
tot = w.groupby('periodo').envios.sum() / 1e6
em = w[w.canal == 'email'].set_index('periodo'); clic = 100 * em.email_click / em.email_delivery
pu = w[w.canal == 'push notification'].set_index('periodo'); po = 100 * pu.pn_open / pu.pn_send
wks = list(tot.index)
reg = dd.regresion_semana()
def sinjun(c):
    pts = [p for p in reg[c]['pts'] if not p['lab'].startswith('06')]
    return dd._ols([p['x'] for p in pts], [p['y'] for p in pts])
fe, fp, fw = reg['email']['fit'], reg['push notification']['fit'], reg['whatsapp']['fit']; fe2 = sinjun('email')
print({k: round(v, 3) for k, v in fe.items()}, {k: round(v, 3) for k, v in fe2.items()}, {k: round(v, 3) for k, v in fp.items()}, round(fw['r2'], 3))
mid = tot[(tot >= 12) & (tot <= 18)]; print('semanas 12 a 18 M', len(mid), 'de', len(tot), 'mediana', tot.median())
PEAKS = {'2026-06-01': ('1', 'correo de BillPay Intro a 16.1 M (NewProducts) y Hot Sale'),
         '2026-05-25': ('2', 'Hot Sale de Sales y Referidos de Marketing'),
         '2026-06-15': ('3', 'Billpayments, Día del Padre y Mundial (Marketing)'),
         '2026-08-10': ('4', 'prueba de QA que salió a clientes y Billpayments'),
         '2026-07-20': ('5', 'Comercio del día por push de Marketing, 6.6 M')}
PK = list(PEAKS)
def resp(d, r, b): return 100 * d[r].sum() / d[b].sum()
pk_p, ot_p = resp(pu.loc[PK], 'pn_open', 'pn_send'), resp(pu.drop(PK), 'pn_open', 'pn_send')
pk_e, ot_e = resp(em.loc[PK], 'email_click', 'email_delivery'), resp(em.drop(PK), 'email_click', 'email_delivery')
wa = w[w.canal == 'whatsapp'].set_index('periodo')
pk_w, ot_w = resp(wa.loc[PK], 'whatsapp_read', 'whatsapp_delivery'), resp(wa.drop(PK), 'whatsapp_read', 'whatsapp_delivery')
print(pk_p, ot_p, pk_e, ot_e, pk_w, ot_w)
S = Svg('Mensajes por semana, en barras, y apertura de push, en línea, enero a septiembre 2026; semanas pico numeradas con su lanzamiento')
S.legend([('sq', BLUE, 'Semana con lanzamiento a toda la base'), ('sq', G2, 'Resto de las semanas'), ('ln', INK, 'Apertura de push')], 0, 10, 11)
X0, X1, Y0, Y1 = 40, 724, 70, 296
n = len(wks); st = (X1 - X0) / n; bw = st * 0.66; cx = lambda i: X0 + st * (i + 0.5)
VM, RM = 40, 4
vy = lambda v: Y1 - (Y1 - Y0) * v / VM; ry = lambda v: Y1 - (Y1 - Y0) * v / RM
S.t(X0 - 6, Y0 - 14, 'Millones de mensajes', 11, SEC)
S.t(X1 + 6, Y0 - 14, 'Apertura de push', 11, INK, 'end', 600)
for v in (0, 10, 20, 30, 40):
    S.line(X0, vy(v), X1, vy(v)); S.t(X0 - 6, vy(v) + 4, f'{v}', 10.5, SEC, 'end'); S.t(X1 + 6, vy(v) + 4, f'{v // 10} %', 10.5, INK)
for i, wk in enumerate(wks):
    pk = wk in PEAKS
    S.rect(cx(i) - bw / 2, vy(tot[wk]), bw, vy(0) - vy(tot[wk]), BLUE if pk else G2)
S.poly([(cx(i), ry(po[wk])) for i, wk in enumerate(wks)], INK, 1.8)
for i, wk in enumerate(wks):
    if wk in PEAKS:
        S.circle(cx(i), ry(po[wk]), 3.5, INK)
        if wk == '2026-05-25': S.t(cx(i) - 6, ry(po[wk]) + 4, f'{po[wk]:.2f} %', 10.5, INK, 'end', 700, halo=True)
        else: S.t(cx(i) + 5, ry(po[wk]) + 15, f'{po[wk]:.2f} %', 10.5, INK, 'middle', 700, halo=True)
        S.circle(cx(i), vy(tot[wk]) - 11, 8, '#FFFFFF', BLUE, 1.5); S.t(cx(i), vy(tot[wk]) - 7, PEAKS[wk][0], 10.5, BLUE, 'middle', 700)
MES = {'01': 'Ene', '02': 'Feb', '03': 'Mar', '04': 'Abr', '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Ago', '09': 'Sep'}
seen = set()
for i, wk in enumerate(wks):
    m = wk[5:7]
    if m not in seen:
        seen.add(m); S.line(cx(i) - st / 2, Y1, cx(i) - st / 2, Y1 + 6, SEC); S.t(cx(i) - st / 2 + 3, Y1 + 17, MES[m], 11, TXT)
# promedios
S.t(X1, Y0 - 34, f'Apertura de push en las 5 semanas pico: {pk_p:.2f} %; en el resto: {ot_p:.2f} %', 11, INK, 'end', 600)
# llave de picos en dos columnas
ky = Y1 + 40
for j, wk in enumerate(PK):
    num, txt = PEAKS[wk]; col = j // 3; row = j % 3
    x = 0 if col == 0 else 425; y = ky + row * 20
    S.circle(x + 8, y - 4, 8, '#FFFFFF', BLUE, 1.5); S.t(x + 8, y, num, 10.5, BLUE, 'middle', 700)
    S.t(x + 22, y, f'{int(wk[8:])} {MES[wk[5:7]].lower()}, {tot[wk]:.1f} M:', 10.5, INK, 'start', 600)
    S.t(x + 112, y, txt, 10.5, TXT)
S.t(425, ky + 40, 'Feb 16 (20.7 M): sin lanzamiento corto que la explique.', 10.5, SEC)

write(40, dict(kind='grafica', seccion='V. El ritmo lo marcan los lanzamientos, no el cliente',
 titulo='Las semanas con más mensajes son semanas de lanzamientos, y en ellas la respuesta cae',
 que='Lanzamientos y campañas de temporada a casi toda la base: BillPay, Hot Sale, Comercio del día, Mundial y Día del Padre, Anota y Gana y regreso a clases. Promocional.',
 quien='Marketing está en las cinco semanas pico y NewProducts explica la más grande; Sales en Hot Sale y regreso a clases. Junio tuvo 44 M mensajes más que el promedio de enero a abril: 26 M de NewProducts y 20 M de Marketing.',
 a_quien='Envíos a toda la base, leads y recurrentes de KPay.',
 lecturas=[
  f'En las cinco semanas pico el push abrió {pk_p:.2f} % contra {ot_p:.2f} % el resto; el clic de email fue {pk_e:.2f} % contra {ot_e:.2f} %. La mayoría de las semanas lleva entre 12 y 18 M mensajes.',
  f'Cada millón extra de correos en la semana baja el clic {abs(fe["b"]):.2f} puntos (R² {fe["r2"]:.2f}); sin junio, {abs(fe2["b"]):.2f} puntos (R² {fe2["r2"]:.2f}): no es solo BillPay. En push, {abs(fp["b"]):.2f} puntos de apertura por millón (R² {fp["r2"]:.2f}).',
  f'En WhatsApp el volumen no mueve la lectura (R² {fw["r2"]:.2f}). En las semanas pico entra gente que casi nunca responde: es volumen más audiencia fría.',
 ],
 causa='Cada equipo fija la fecha de su lanzamiento sin ver la de los demás, y los lanzamientos salen a toda la base el mismo día.',
 sowhat='El volumen no se decide semana a semana: se acumula porque nadie ve el calendario completo de lanzamientos.',
 fuente='Fuente: Braze, E4a por semana y canal, enero a septiembre 2026; regresión semanal de volumen del canal contra su respuesta (38 semanas). Campañas detrás de cada pico: E1 con primer y último envío de E2, solo campañas que duran 10 días o menos (16 % del volumen); BillPay Intro por correo: E1.',
 svg=S.svg()))
