"""Lámina 42 (ronda 2, forma de v5 lámina 41): pequeños múltiplos, una campaña por panel, misma escala. Bajas de correo por mes
desde esa campaña (eventos, E1); punto lleno = la campaña mandó correos ese mes, hueco = bajas que siguen llegando sin envío.
Personas que se dan de baja por mes: E4a."""
import pandas as pd
from kit import *
e = pd.read_csv(D + 'e4a_serie_semana_mes_canal.csv'); mm = e[(e.grano == 'mes') & (e.canal == 'email')].copy()
mm['m'] = mm.periodo.str[5:7].astype(int); pers = mm.set_index('m').bajas_email_usuarios / 1e3; prom = pers.sum() / 9
e1 = pd.read_csv(D + 'e1_comunicacion_mes_canal.csv'); em = e1[e1.canal == 'email'].copy()
em['m'] = em.mes.str[5:7].astype(int); em['f'] = em.communication_name.map(fam)
tot = em.groupby('m').email_unsubscribe.sum()
e8 = pd.read_csv(D + 'e8_dias_hasta_baja.csv'); bi_p = e8[(e8.bloque == 'familia_dia_baja') & e8.clave.str.contains('BillPay_Intro')].usuarios.sum()
PAN = [('BillPay_Intro_Full_Rollout', 'BillPay Intro', 'NewProducts, a toda la base', GREEN),
       ('B0308-CANVAS-Todos_BBDDAn', 'No Tasa 0', 'Marketing, salió en diciembre', BLUE),
       ('B0312-CANVAS-Nuevos_Eligibles-Christmas', 'Christmas', 'Product Growth', BLUE),
       ('B0337-CANVAS-Leads_Eligibles-CuestaEnero', 'Cuesta de enero', 'Product Growth', BLUE),
       ('B0211-CANVAS-Nuevos_RegistradosPay-Tasa0', 'Tasa 0 a registrados', 'Product Growth', G1),
       ('B0171-CANVAS-Leads_BBDDRezagada-NarrativaTasa0', 'Narrativa Tasa 0', 'Marketing, base rezagada', G1),
       ('B0326-Canvas-Leads-ReferralProgram', 'Referidos a leads', 'Marketing', G1),
       ('B0440-CANVAS-Todos-AnotayGana', 'Anota y Gana', 'Product Growth, a todos', G1)]
DAT = {}
for k, *_ in PAN:
    d = em[em.f.str.contains(k)].groupby('m')[['email_unsubscribe', 'envios']].sum().reindex(range(1, 10)).fillna(0)
    DAT[k] = d; print(k, (d.email_unsubscribe / 1e3).round(1).tolist(), (d.envios > 0).astype(int).tolist())
print(pers.round(1).to_dict(), prom, bi_p)
S = Svg('Ocho paneles, una campaña cada uno, misma escala: bajas de correo por mes desde esa campaña, enero a septiembre 2026')
S.circle(6, 15, 4, INK); S.t(15, 19, 'Mes con envío', 11, TXT)
S.circle(116, 15, 4, '#FFFFFF', INK, 1.5); S.t(125, 19, 'Mes sin envío: las bajas siguen llegando', 11, TXT)
S.t(0, 38, 'Miles de bajas de correo por mes desde cada campaña (eventos). Azul: temporada de enero; verde: BillPay.', 10.5, SEC)
PW, PH = 195, 170; MES = 'EFMAMJJAS'
for j, (k, name, sub, col) in enumerate(PAN):
    x0, y0 = (j % 4) * PW, 54 + (j // 4) * PH
    X0, X1, Y0, Y1 = x0 + 30, x0 + PW - 14, y0 + 36, y0 + PH - 26
    sx = lambda i: X0 + (X1 - X0) * i / 8; sy = lambda v: Y1 - (Y1 - Y0) * v / 40
    S.t(x0, y0 + 10, name, 11.5, INK if col != G1 else TXT, w=700); S.t(x0, y0 + 24, sub, 10.5, SEC)
    for v in (0, 20, 40):
        S.line(X0, sy(v), X1, sy(v)); S.t(X0 - 5, sy(v) + 4, f'{v}', 10.5, SEC, 'end')
    for i in range(9): S.t(sx(i), Y1 + 14, MES[i], 10.5, SEC, 'middle')
    d = DAT[k]; v = (d.email_unsubscribe / 1e3).tolist(); sent = (d.envios > 0).tolist()
    lc = col if col != G1 else SEC
    S.poly([(sx(i), sy(x)) for i, x in enumerate(v)], lc, 2 if col != G1 else 1.4)
    for i, x in enumerate(v):
        if x > 0.05 or sent[i]: S.circle(sx(i), sy(x), 3.2, lc if sent[i] else '#FFFFFF', '#FFFFFF' if sent[i] else lc, 1 if sent[i] else 1.4)
    i = max(range(9), key=lambda i: v[i])
    S.t(sx(i) + (6 if i < 6 else -6), sy(v[i]) + 4, f'{v[i]:.0f} mil, {"ene feb mar abr may jun jul ago sep".split()[i]}', 10.5, INK, 'start' if i < 6 else 'end', 700, halo=True)
write(42, dict(kind='grafica', seccion='V. El ritmo lo marcan los lanzamientos, no el cliente',
 titulo='Las bajas suben con las temporadas de ofertas: Navidad y Tasa 0 en enero, el lanzamiento de BillPay en junio',
 que='Tasa 0, Navidad, Reyes, Cuesta de enero, BillPay, referidos y Anota y Gana',
 quien='Marketing y Product Growth en enero; NewProducts, Marketing y Product Growth en junio',
 a_quien='Base rezagada, anónimos, registrados y elegibles; en junio, toda la base con correo',
 lecturas=[
  f'Enero: {pers[1]:.0f} mil personas se dieron de baja; junio: {pers[6]:.0f} mil. El mes promedio, {prom:.0f} mil.',
  'Enero es la cola de diciembre: No Tasa 0 dejó 18 mil bajas en enero sin mandar correos ese mes.',
  f'BillPay Intro salió una vez y siguió sumando bajas en julio y agosto: {bi_p/1e3:.0f} mil personas en total.',
 ],
 causa='Las temporadas y los lanzamientos salen a toda la base sin límite de audiencia ni de toques.',
 sowhat='Las temporadas y los lanzamientos necesitan un límite de audiencia y de toques, no solo una fecha.',
 fuente='Fuente: Braze, enero a septiembre 2026. Bajas por campaña y mes: E1 (eventos; cuentan bajas que llegan después del envío). Personas por mes: E4a. Personas desde BillPay Intro: E8.',
 svg=S.svg()))
