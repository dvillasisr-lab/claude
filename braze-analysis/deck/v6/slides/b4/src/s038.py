"""Lámina 38: push y correos por persona al mes y apertura de push según antigüedad en la base al momento del envío (E12)."""
import pandas as pd
from kit import *
e = pd.read_csv(D + 'e12_antiguedad.csv')
B = [('0. menos de 1 mes', 'Menos de 1 mes', 1), ('1. 1 a 3 meses', '1 a 3 meses', 2), ('2. 3 a 6 meses', '3 a 6 meses', 3),
     ('3. 6 a 12 meses', '6 a 12 meses', 6), ('4. 1 a 2 años', '1 a 2 años', 9), ('5. más de 2 años', 'Más de 2 años', 9)]
g = e.groupby(['banda_antiguedad', 'canal'])[['envios', 'usuarios_aprox', 'respuestas', 'bajas_email_eventos']].sum()
rows = []
for k, lab, dur in B:
    p, m = g.loc[(k, 'push notification')], g.loc[(k, 'email')]
    rows.append(dict(lab=lab, push=p.envios / p.usuarios_aprox / dur, mail=m.envios / m.usuarios_aprox / dur, ap=100 * p.respuestas / p.envios,
                     bm=1000 * m.bajas_email_eventos / m.envios, pushM=p.envios / 1e6, pers=p.usuarios_aprox))
r = pd.DataFrame(rows); print(r.round(2))
OLD = ['3. 6 a 12 meses', '4. 1 a 2 años', '5. más de 2 años']
sh_all = 100 * e[e.banda_antiguedad.isin(OLD)].envios.sum() / e.envios.sum()
pp = e[e.canal == 'push notification']; sh_push = 100 * pp[pp.banda_antiguedad.isin(OLD)].envios.sum() / pp.envios.sum()
print(sh_all, sh_push)

S = Svg('Push y correos por persona al mes, en barras, y apertura de push, en línea, según antigüedad en la base; con bajas por mil correos')
S.legend([('sq', G1, 'Push por persona al mes'), ('sq', G2, 'Correos por persona al mes'), ('ln', BLUE, 'Apertura de push')], 0, 10)
S.t(0, 40, 'Antigüedad de la persona en la base el día del envío, enero a septiembre 2026', 10.5, SEC)
X0, X1, Y0, Y1 = 52, 724, 92, 340
st = (X1 - X0) / 6; bw = st * 0.26; cx = lambda i: X0 + st * (i + 0.5)
VM, RM = 16, 4
vy = lambda v: Y1 - (Y1 - Y0) * v / VM; ry = lambda v: Y1 - (Y1 - Y0) * v / RM
S.t(X0 - 8, Y0 - 20, 'Mensajes por persona al mes', 11, SEC)
S.t(X1 + 8, Y0 - 20, 'Apertura de push', 11, BLUE, 'end', 600)
for v in (0, 4, 8, 12, 16):
    S.line(X0, vy(v), X1, vy(v)); S.t(X0 - 8, vy(v) + 4, f'{v}', 10.5, SEC, 'end'); S.t(X1 + 8, vy(v) + 4, f'{v/4:.0f} %', 10.5, BLUE)
for i, x in r.iterrows():
    S.rect(cx(i) - bw - 1, vy(x.push), bw, vy(0) - vy(x.push), G1); S.t(cx(i) - bw / 2 - 1, vy(x.push) - 5, f'{x.push:.0f}', 11, INK, 'middle', 600, halo=True)
    S.rect(cx(i) + 1, vy(x.mail), bw, vy(0) - vy(x.mail), G2); S.t(cx(i) + bw / 2 + 1, vy(x.mail) - 5, f'{x.mail:.0f}', 11, TXT, 'middle', 400, halo=True)
    S.t(cx(i), Y1 + 17, x.lab, 11.5, TXT, 'middle')
    S.t(cx(i), Y1 + 34, f'{x.bm:.1f}', 11, SEC, 'middle')
    S.t(cx(i), Y1 + 50, f'{x.pushM:.0f} M push', 11, INK if i == 5 else SEC, 'middle', 600 if i == 5 else 400)
S.t(X0 - 8, Y1 + 34, 'Bajas', 10.5, SEC, 'end'); S.t(X0 - 8, Y1 + 50, 'Total', 10.5, SEC, 'end')
S.t(X1 + 50, Y1 + 34, '', 10.5, SEC)
S.poly([(cx(i), ry(x.ap)) for i, x in r.iterrows()], BLUE, 2.5)
for i, x in r.iterrows():
    S.circle(cx(i), ry(x.ap), 5, BLUE)
    S.t(cx(i) + 9, ry(x.ap) - 9, f'{x.ap:.1f} %', 12, BLUE, 'start', 700, halo=True)
S.t(X1, Y1 + 66, 'Bajas = bajas por cada mil correos. En push no hay registro de quién apaga las notificaciones.', 10.5, SEC, 'end')

write(38, dict(kind='grafica', seccion='IV. La misma persona, demasiadas veces',
 titulo='Después del tercer mes casi nadie abre el push, y le seguimos mandando unos diez al mes',
 que='Push promocional: Comercio del día, Hot Sale, referidos, rescates de fin de semana y Anota y Gana.',
 quien='Push a recurrentes: Sales 44.7 M (abre 1.27 %), Marketing 26.2 M (1.63 %), Product Growth 9.9 M (5.0 %). Push a leads de bases viejas: Marketing 69.9 M (1.03 %).',
 a_quien=f'Personas con más de 6 meses en la base: reciben {sh_all:.0f} % de todos los mensajes y {sh_push:.0f} % del push. Con más de 2 años: {r.pushM[5]:.0f} M push a {r.pers[5]/1e3:.0f} mil personas.',
 lecturas=[
  f'El push casi no cambia con la antigüedad: unos {r.push[0]:.0f} al mes en los primeros 3 meses y {r.push[3]:.0f} a {r.push[5]:.0f} después. Lo que cae es la apertura: {r.ap[0]:.1f} % el primer mes, {r.ap[1]:.1f} % del mes 1 al 3 y {r.ap[3]:.1f} % desde el sexto.',
  f'El correo pega al inicio: {r.mail[0]:.0f} correos el primer mes y menos de 2 al mes después del sexto. Las bajas por mil correos son parecidas en todas las antigüedades ({r.bm.min():.1f} a {r.bm.max():.1f}).',
  'El "siete veces más push" a los antiguos comparaba 9 meses de un antiguo con el único mes de un nuevo; por mes es parecido.',
 ],
 causa='El push se manda por lista (recurrentes, leads de bases viejas) y no según si la persona lo abrió hace poco; nadie lo deja de mandar a quien ya no abre.',
 sowhat='Al antiguo no le mandamos más, le seguimos mandando igual aunque ya no abre: el push debe ir a quien abrió uno en los últimos 90 días.',
 fuente='Fuente: Braze, E12 (antigüedad el día del envío), enero a septiembre 2026. Por mes = mensajes por persona entre los meses que dura la banda dentro del periodo (1, 2, 3, 6, 9 y 9; es un mínimo). Push por equipo y audiencia: E1, según el nombre de la campaña. Mínimo aceptable de push: 7.5 aperturas por cada mil.',
 svg=S.svg()))
