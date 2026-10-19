"""Lámina 21 (ronda 2): franja de puntos por equipo. Cada punto = campaña en un canal (50 mil o más entregados, nueve meses);
x = mensajes de la campaña (escala log), color = a quién va (azul: gente que no ha hecho nada reciente; gris: hizo algo hace poco).
Derecha: mensajes del equipo y parte a gente sin acción reciente. Casos grandes nombrados."""
import math, random
from datos import *
from svgk import *
f = fam(); TOT = f.env.sum()
ORD = ['Marketing', 'Product Growth', 'Others', 'Sales', 'Collections']
NOM = {('B0391-CANVAS-Leads_BDDMarketing-RescateFinesDeSemana', 'push notification'): ('Rescate de fin de semana a leads', 'push'),
       ('B0000-CANVAS-Leads_LeftFunnel-Retargeting_Veriff', 'email'): ('Recordatorio de registro', 'correo'),
       ('B0211-CANVAS-Nuevos_RegistradosPay-Tasa0', 'email'): ('Tasa 0 a registrados sin crédito', 'correo'),
       ('B0223-CANVAS-Nuevos_NeverActive', 'email'): ('Installments a quien nunca activó', 'correo'),
       ('BillPay_Intro_Full_Rollout', 'email'): ('Lanzamiento de BillPay a toda la base', 'correo'),
       ('B0335-CANVAS-Recurrentes_PortafolioActivo', 'email'): ('Promociones a todo el portafolio', 'correo'),
       ('KCash-T000-CANVAS-BKT1', 'email'): ('Cobranza con atraso menor', 'correo')}
rnd = random.Random(3)
USED = set()
S = Svg('Mensajes por campaña de cada equipo según a quién van, con el total del equipo y la parte que va a gente que no ha hecho nada reciente')
S.t(0, 16, 'Cada punto es una campaña en un canal: mensajes de enero a septiembre', 12.5, INK, w=600)
S.c(6, 34, 4.5, BLUE, stroke='none'); S.t(15, 38, 'A gente que no ha hecho nada reciente', 11.5)
S.c(262, 34, 4.5, MRK, stroke='none'); S.t(271, 38, 'A quien hizo algo hace poco', 11.5)
X0, X1 = 112, 640
LO, HI = math.log10(5e4), math.log10(4e7)
xs = lambda v: X0 + (X1 - X0) * (math.log10(min(max(v, 5e4), 4e7)) - LO) / (HI - LO)
TOP, RH = 62, 64
YB = TOP + RH * len(ORD)
for v, lab in [(1e5, '100 mil'), (1e6, '1 M'), (1e7, '10 M'), (3e7, '30 M')]:
    S.l(xs(v), TOP - 4, xs(v), YB - 4, GRID); S.t(xs(v), YB + 10, lab, 10.5, SEC, 'middle')
S.t(X1, YB + 24, 'Mensajes de la campaña en nueve meses (escala logarítmica)', 10.5, SEC, 'end')
S.t(780, TOP - 8, 'Mensajes y parte a quien no hizo nada', 10.5, SEC, 'end')
for i, t in enumerate(ORD):
    d = f[f.equipo == t].sort_values('env')
    y0 = TOP + RH * i; cy = y0 + 38
    if i: S.l(0, y0, 780, y0, GRID)
    S.t(0, cy - 2, t, 12.5, INK, w=600); S.t(0, cy + 13, f'{len(d)} campañas', 10.5, SEC)
    for r in d.itertuples():
        rr = 2.4 if r.env < 1e6 else (3.4 if r.env < 5e6 else 5)
        S.c(xs(r.env), cy + rnd.uniform(-14, 14), rr, MRK if r.con else BLUE, stroke='#FFFFFF', sw=0.6, op=0.75)
    sin = d[~d.con].env.sum()
    S.t(780, cy - 2, f'{d.env.sum()/1e6:.0f} M ({100*d.env.sum()/TOT:.0f} %)', 12, INK, 'end', w=600)
    S.t(780, cy + 13, f'{100*sin/d.env.sum():.0f} % no hizo nada', 10.5, BLUE if sin / d.env.sum() > 0.5 else SEC, 'end', w=600)
    k = 0
    for r in d.sort_values('env', ascending=False).itertuples():
        for (pat, ch), (nm, cn) in NOM.items():
            if pat in r.familia and ch == r.canal and pat not in USED:
                USED.add(pat)
                x = xs(r.env); ly = y0 + 12 if k == 0 else y0 + 12
                anc = 'end' if x > 380 else 'start'
                lx = x - 6 if anc == 'end' else x + 6
                if k == 1: ly = y0 + 24
                S.l(x, cy - 5, x, ly + 3, MRK, 0.8)
                S.t(lx, ly, f'{nm} · {cn} · {r.env/1e6:.1f} M', 10.5, INK, anc, w=600, halo=True)
                k += 1
svg = S.done()
mp = f[f.equipo.isin(['Marketing', 'Product Growth'])]
print('MP %.1f %%, sin %.1f %%' % (100 * mp.env.sum() / TOT, 100 * mp[~mp.con].env.sum() / mp.env.sum()))
save(21, dict(kind='grafica',
  titulo='Marketing y Product Growth ponen dos de cada tres mensajes, y la mayoría a gente que no ha hecho nada reciente',
  que='Tasa 0, referidos, promociones de KPay, crédito e Installments, concursos.',
  quien='Marketing y Product Growth (Lending en Braze): 77 % del gasto, 44.5 M MXN.',
  a_quien='Leads, leads fríos, registrados sin crédito, ex clientes inactivos y toda la base.',
  lecturas=[
   '432 M de 657 M mensajes son de Marketing y Product Growth; 70 % va a gente que no ha hecho nada reciente.',
   'Sus campañas más grandes son de ese tipo: Tasa 0 a registrados, 34.9 M correos; rescate de fin de semana, 13.4 M push.',
   'Collections y Sales escriben casi siempre a quien hizo algo hace poco: 0 % y 25 % va a gente que no ha hecho nada.'],
  causa='Cada equipo arma ofertas para su lista completa y nadie es dueño de la gente que no ha hecho nada.',
  sowhat='El volumen está en dos equipos que ofrecen lo mismo a las mismas personas: ahí empieza el ajuste.',
  fuente='Fuente: Braze, envíos por campaña, mes y canal, enero a septiembre 2026; campañas con 50 mil o más entregados (657 M mensajes). A quién, según el nombre de la campaña.',
  svg=svg))
check(21)
