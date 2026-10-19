"""Lámina 35: días con tres o más campañas por mes (E6a) y equipos presentes en los choques promocionales (E6b)."""
import pandas as pd
from kit import *
from e6b import load
a = pd.read_csv(D + 'e6a_solape_dia_mes.csv'); a['m'] = a.mes.str[5:7].astype(int)
BANDS = [('3 a 4', BLUE2, '3 a 4 campañas'), ('5 a 7', BLUE, '5 a 7'), ('8+', INK, '8 o más')]
pv = a.pivot_table(index='m', columns='banda_familias_dia', values='usuarios_aprox', aggfunc='sum') / 1e6
hi = a[a.banda_familias_dia.isin(['3 a 4', '5 a 7', '8+'])]
shm = 100 * hi.groupby('m').msgs.sum() / a.groupby('m').msgs.sum()
pers = pv[['3 a 4', '5 a 7', '8+']].sum(axis=1)
print(pers.round(2).to_dict(), shm.round(1).to_dict())
sh_ud = 100 * hi.usuario_dias.sum() / a.usuario_dias.sum(); sh_m = 100 * hi.msgs.sum() / a.msgs.sum()
p = load(); pp = p[p.promo2]; P = pp.usuario_dias_juntas.sum()
inv = {t: 100 * pp[(pp.ta == t) | (pp.tb == t)].usuario_dias_juntas.sum() / P for t in ['Marketing', 'Sales', 'Product Growth', 'Others', 'Collections']}
pair = (pp.groupby('pair').usuario_dias_juntas.sum() / 1e6).sort_values(ascending=False)
print(inv, pair.head(3).round(1).to_dict(), P / 1e6, 100 * P / p.usuario_dias_juntas.sum())

S = Svg('Personas con al menos un día de tres o más campañas, por mes, y parte de los mensajes del mes que sale en esos días; y equipos presentes en los choques promocionales')
S.legend([('sq', BLUE2, '3 a 4 campañas el mismo día'), ('sq', BLUE, '5 a 7'), ('sq', INK, '8 o más')], 0, 10, 11)
S.t(0, 40, 'Personas con al menos un día así en el mes (una persona puede contar en dos grupos)', 10.5, SEC)
X0, X1, Y0, Y1 = 46, 468, 84, 352
MES = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep']
st = (X1 - X0) / 9; bw = st * 0.56; cx = lambda i: X0 + st * (i + 0.5)
VM, RM = 2.5, 50
vy = lambda v: Y1 - (Y1 - Y0) * v / VM; ry = lambda v: Y1 - (Y1 - Y0) * v / RM
S.t(X0 - 6, Y0 - 22, 'Millones de personas', 11, SEC)
for v in (0, 0.5, 1, 1.5, 2, 2.5):
    S.line(X0, vy(v), X1, vy(v)); S.t(X0 - 6, vy(v) + 4, f'{v:g} M', 10.5, SEC, 'end')
for i, m in enumerate(range(1, 10)):
    base = 0
    for k, col, _ in BANDS:
        v = pv.loc[m, k]; S.rect(cx(i) - bw / 2, vy(base + v), bw, max(0, vy(base) - vy(base + v) - 1.5), col); base += v
    big = m in (1, 6, 8, 9)
    S.t(cx(i), vy(base) - 6, f'{base:.2f}' if big else f'{base:.1f}', 11 if big else 10.5, INK, 'middle', 700 if big else 400, halo=True)
    S.t(cx(i), Y1 + 16, MES[i], 11, TXT, 'middle')
S.t(X0 - 6, Y1 + 34, '% msj.', 10.5, SEC, 'end')
for i, m in enumerate(range(1, 10)):
    S.t(cx(i), Y1 + 34, f'{shm[m]:.0f} %', 11, INK if m == 5 else TXT, 'middle', 700 if m == 5 else 400)
S.t(X0, Y1 + 50, 'Fila de abajo: parte de los mensajes del mes que salió en días de tres o más campañas.', 10.5, SEC)
# panel de equipos
PX = 540
S.t(PX - 30, 76, 'Equipo presente en el choque promocional', 11.5, INK, w=600)
S.t(PX - 30, 91, '% de personas-día con dos promociones a la vez', 10.5, SEC)
BX0, BX1 = PX + 70, 740; y = 112
for t, lab in [('Marketing', 'Marketing'), ('Sales', 'Sales'), ('Product Growth', 'Product Growth'), ('Others', 'Others'), ('Collections', 'Collections')]:
    v = inv[t]; w = (BX1 - BX0) * v / 100
    S.t(BX0 - 8, y + 13, lab, 11, INK if t == 'Marketing' else TXT, 'end', 600 if t == 'Marketing' else 400)
    S.rect(BX0, y + 2, w, 16, BLUE if t == 'Marketing' else G1)
    S.t(BX0 + w + 6, y + 14.5, f'{v:.0f} %', 11, INK, 'start', 700 if t == 'Marketing' else 400)
    y += 30
S.t(PX - 30, y + 14, 'Un choque cuenta para los dos equipos.', 10.5, SEC)
S.t(PX - 30, y + 38, 'Parejas más grandes, millones de personas-día:', 11, INK, w=600)
yy = y + 56
for k, lab in [('Marketing + Marketing', 'Marketing con Marketing'), ('Sales + Sales', 'Sales con Sales'), ('Marketing + Sales', 'Marketing con Sales')]:
    S.t(PX - 30, yy, lab, 11, TXT); S.t(776, yy, f'{pair[k]:.1f} M', 11, INK, 'end', 600); yy += 17

write(35, dict(kind='grafica', seccion='IV. La misma persona, demasiadas veces',
 titulo=f'Cada mes hasta {pers.max():.1f} M personas reciben tres o más campañas el mismo día, casi siempre con Marketing en el choque',
 que=f'Dos o más promociones el mismo día a la misma persona: Hot Sale, Comercio del día, lanzamiento de BillPay, Anota y Gana, Mundial y Día del Padre, Tasa 0. {100*P/p.usuario_dias_juntas.sum():.0f} % de los choques medidos es promoción con promoción.',
 quien=f'Marketing está en {inv["Marketing"]:.0f} % de los choques promocionales, Sales en {inv["Sales"]:.0f} %, Product Growth en {inv["Product Growth"]:.0f} % y Others (NewProducts, QA, Shopping) en {inv["Others"]:.0f} %. Collections no aparece.',
 a_quien='Recurrentes y activos de KPay, leads y envíos a toda la base. Mayo, junio y agosto son los meses con más choques (Hot Sale, BillPay, regreso a clases).',
 lecturas=[
  f'Personas con un día de tres o más campañas: {pers[1]:.2f} M en enero, {pers[6]:.2f} M en junio, {pers[8]:.2f} M en agosto y {pers[9]:.2f} M en septiembre.',
  f'Esos días son {sh_ud:.0f} % de las personas-día y llevan {sh_m:.0f} % de los mensajes; en mayo, {shm[5]:.0f} %.',
  f'21 de junio: Marketing mandó dos push el mismo día a 1.54 M personas (Felicitación Día del Padre y Onboarding de Billpayments). 11 de agosto: una prueba de QA (recordatorio de registro de teléfono) salió a clientes junto con un push de Marketing, a 1.45 M.',
 ],
 causa='Nadie administra el calendario y el límite global de mensajes por persona de Braze está apagado: cada equipo suma su campaña sin ver las de los demás.',
 sowhat='Hace falta un límite de mensajes por persona al día y un dueño del calendario que vea todas las campañas.',
 fuente=f'Fuente: Braze, enero a septiembre 2026. Personas y días: E6a (campañas distintas por persona y día). Equipos: E6b, solo los 1,000 pares más frecuentes ({p.usuario_dias_juntas.sum()/1e6:.0f} M personas-día; es muestra, no universo). Promocional = nombre con ticket y equipo distinto de Collections.',
 svg=S.svg()))
