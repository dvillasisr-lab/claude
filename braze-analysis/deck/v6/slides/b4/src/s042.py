"""Lámina 42: bajas de email por mes. Barras = eventos de baja por tema del correo (E1); línea = personas que se dan de baja (E4a)."""
import pandas as pd
from kit import *
from e6b import tema
e = pd.read_csv(D + 'e4a_serie_semana_mes_canal.csv'); mm = e[(e.grano == 'mes') & (e.canal == 'email')].copy()
mm['m'] = mm.periodo.str[5:7].astype(int); pers = mm.set_index('m').bajas_email_usuarios / 1e3
prom = pers.sum() / 9
e1 = pd.read_csv(D + 'e1_comunicacion_mes_canal.csv'); em = e1[e1.canal == 'email'].copy()
em['m'] = em.mes.str[5:7].astype(int); em['T'] = em.team.map(team); em['tema'] = em.communication_name.map(tema)
GR = {'Tasa 0': 'Tasa 0', 'Temporada': 'Temporada (Navidad, Reyes, Cuesta de enero)', 'Lanzamiento BillPay': 'Lanzamiento de BillPay',
      'Referidos': 'Referidos y Anota y Gana', 'Anota y Gana': 'Referidos y Anota y Gana'}
em['g'] = em.tema.map(GR).fillna('Otros temas')
pv = em.pivot_table(index='m', columns='g', values='email_unsubscribe', aggfunc='sum').fillna(0) / 1e3
sh = 100 * pv.div(pv.sum(axis=1), axis=0)
pt = em.pivot_table(index='m', columns='T', values='email_unsubscribe', aggfunc='sum').fillna(0); pt = 100 * pt.div(pt.sum(axis=1), axis=0)
tm = em.pivot_table(index='m', columns='tema', values='email_unsubscribe', aggfunc='sum').fillna(0); tm = 100 * tm.div(tm.sum(axis=1), axis=0)
bi = em[em.communication_name.str.contains('BillPay_Intro')].groupby('m').email_unsubscribe.sum()
e8 = pd.read_csv(D + 'e8_dias_hasta_baja.csv'); bi_p = e8[(e8.bloque == 'familia_dia_baja') & e8.clave.str.contains('BillPay_Intro')].usuarios.sum()
print(pers.round(1).to_dict(), prom, sh.round(0).to_string(), pt.round(0).to_string(), bi.to_dict(), bi_p, sep='\n')
ORD = [('Tasa 0', BLUE), ('Temporada (Navidad, Reyes, Cuesta de enero)', BLUE2), ('Lanzamiento de BillPay', GREEN), ('Referidos y Anota y Gana', G1), ('Otros temas', G2)]
S = Svg('Eventos de baja de email por mes según el tema del correo, en barras apiladas, y personas que se dieron de baja, en línea, enero a septiembre 2026')
S.legend([('sq', BLUE, 'Tasa 0'), ('sq', BLUE2, 'Navidad, Reyes y Cuesta de enero'), ('sq', GREEN, 'Lanzamiento de BillPay')], 0, 10, 11)
S.legend([('sq', G1, 'Referidos y Anota y Gana'), ('sq', G2, 'Otros temas'), ('ln', INK, 'Personas que se dieron de baja')], 0, 30, 11)
X0, X1, Y0, Y1 = 52, 724, 92, 360
st = (X1 - X0) / 9; bw = st * 0.56; cx = lambda i: X0 + st * (i + 0.5)
VM, RM = 200, 100
vy = lambda v: Y1 - (Y1 - Y0) * v / VM; ry = lambda v: Y1 - (Y1 - Y0) * v / RM
S.t(X0 - 8, Y0 - 18, 'Mil bajas (eventos), por tema', 11, SEC)
S.t(X1 + 8, Y0 - 18, 'Mil personas', 11, INK, 'end', 600)
for v in (0, 50, 100, 150, 200):
    S.line(X0, vy(v), X1, vy(v)); S.t(X0 - 8, vy(v) + 4, f'{v}', 10.5, SEC, 'end'); S.t(X1 + 8, vy(v) + 4, f'{v // 2}', 10.5, INK)
MES = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep']
for i, m in enumerate(range(1, 10)):
    base = 0
    for k, col in ORD:
        v = pv.loc[m].get(k, 0); y1, y0 = vy(base + v), vy(base)
        S.rect(cx(i) - bw / 2, y1, bw, max(0, y0 - y1 - 1.5), col)
        if k in ('Tasa 0', 'Lanzamiento de BillPay', 'Temporada (Navidad, Reyes, Cuesta de enero)') and sh.loc[m].get(k, 0) >= 15:
            S.t(cx(i), (y0 + y1) / 2 + 4, f'{sh.loc[m, k]:.0f} %', 10.5, '#FFFFFF' if col != BLUE2 else INK, 'middle', 700)
        base += v
    S.t(cx(i), Y1 + 16, MES[i], 11.5, TXT, 'middle')
S.line(X0, ry(prom), X1, ry(prom), INK, 1, ' opacity="0.5"')
S.t((cx(3) + cx(4)) / 2, ry(prom) - 6, f'Mes promedio: {prom:.0f} mil personas', 10.5, INK, 'middle', halo=True)
S.poly([(cx(i), ry(pers[m])) for i, m in enumerate(range(1, 10))], INK, 2.5)
for i, m in enumerate(range(1, 10)):
    hi = m in (1, 6)
    S.circle(cx(i), ry(pers[m]), 5.5 if hi else 4.5, INK)
    S.t(cx(i), ry(pers[m]) - 10, f'{pers[m]:.0f} mil', 12 if hi else 11, INK, 'middle', 700 if hi else 500, halo=True)
S.t(X0, Y1 + 36, 'Barras: eventos de baja según el correo desde el que se dieron de baja (llegan aunque el correo saliera antes). % = parte del mes.', 10.5, SEC)

write(42, dict(kind='grafica', seccion='V. El ritmo lo marcan los lanzamientos, no el cliente',
 titulo='Las bajas suben con las temporadas de ofertas: Navidad y Tasa 0 en enero, el lanzamiento de BillPay en junio',
 que=f'Enero: Tasa 0 ({tm.loc[1,"Tasa 0"]:.0f} % de las bajas del mes), Navidad, Reyes y Cuesta de enero ({tm.loc[1,"Temporada"]:.0f} %) y newsletter ({tm.loc[1,"Newsletter"]:.0f} %). Junio: lanzamiento de BillPay ({tm.loc[6,"Lanzamiento BillPay"]:.0f} %), Tasa 0 ({tm.loc[6,"Tasa 0"]:.0f} %) y Anota y Gana ({tm.loc[6,"Anota y Gana"]:.0f} %). Promocional.',
 quien=f'Enero: Marketing {pt.loc[1,"Marketing"]:.0f} % y Product Growth {pt.loc[1,"Product Growth"]:.0f} % de las bajas del mes. Junio: NewProducts {pt.loc[6,"Others"]:.0f} %, Marketing {pt.loc[6,"Marketing"]:.0f} % y Product Growth {pt.loc[6,"Product Growth"]:.0f} %.',
 a_quien='Enero: base rezagada y anónimos (Marketing), registrados y elegibles (Product Growth). Junio: toda la base con correo.',
 lecturas=[
  'Enero no tiene un solo correo detrás: es la cola de diciembre (No Tasa 0 de Marketing dejó 18 mil bajas en enero sin enviar ese mes) más Christmas de Product Growth (2.5 M correos, 5.8 bajas por mil) y Tasa 0.',
  'Junio sí es un solo correo: BillPay Intro de NewProducts, a 16.1 M personas con 0.10 % de clic, 30 % de las bajas del mes.',
  f'El daño no se ve completo en su mes: BillPay Intro siguió sumando bajas en julio y agosto, {bi_p/1e3:.0f} mil personas en total; por eso julio también salió alto ({pers[7]:.0f} mil).',
 ],
 causa='Las temporadas y los lanzamientos salen a toda la base con correos que esa gente no pidió, sin límite de audiencia ni de toques.',
 sowhat='Las temporadas y los lanzamientos necesitan un límite de audiencia y de toques, no solo una fecha.',
 fuente=f'Fuente: Braze, enero a septiembre 2026. Personas por mes: E4a (enero {pers[1]*1e3:,.0f}; junio {pers[6]*1e3:,.0f}; mes promedio = {pers.sum()*1e3:,.0f} entre 9). Reparto por tema y equipo: eventos de baja de E1, que cuentan bajas que llegan después del envío. Personas que se dieron de baja desde BillPay Intro: E8.',
 svg=S.svg()))
