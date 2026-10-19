"""Lámina 12: MXN por conversión de WhatsApp por equipo y audiencia (dispersión, eje y logarítmico) contra gasto de WhatsApp.
Línea de referencia: costo por conversión del email. A la derecha, campañas que muestran el patrón."""
import math
from b2base import *

d = load_b()
w = d[d.canal == 'whatsapp']
e = d[d.canal == 'email']
cpc = lambda g: g.costo.sum() / max(1, g.conversiones_fraccional.sum())
AUDS = {'activos': ('Clientes activos', GREEN), 'leads': ('Leads', G1), 'frios': ('Bases frías', BLUE)}
pts = []
for (eq, au), g in w[w.aud.isin(AUDS)].groupby(['equipo', 'aud']):
    if g.costo.sum() < 1e6:
        continue
    pts.append(dict(team=eq, au=au, x=g.costo.sum() / 1e6, y=cpc(g), conv=g.conversiones_fraccional.sum()))
P = pd.DataFrame(pts)
py = lambda t, a: P[(P.team == t) & (P.au == a)].y.iloc[0]
print(P.round(1))
A = {a: cpc(w[w.aud == a]) for a in AUDS}
E = {a: cpc(e[e.aud == a]) for a in AUDS}
EMAIL = cpc(e)
fr = w[w.aud == 'frios']
ex = fr[fr.fam.str.contains('Dormant|Inactiv|Churn', case=False)]
nv = fr[fr.fam.str.contains('Rezagad|Never', case=False)]
efr = e[e.aud == 'frios']
eex = efr[efr.fam.str.contains('Dormant|Inactiv|Churn', case=False)]
env_ = efr[efr.fam.str.contains('Rezagad|Never', case=False)]
fam = w.groupby('fam').apply(lambda g: pd.Series({'c': g.costo.sum() / 1e6, 'cpc': cpc(g), 'ent': 100 * g.whatsapp_delivery.sum() / g.whatsapp_send.sum()}))
k = lambda s: fam.loc[[i for i in fam.index if s in i]].sort_values('c').iloc[-1]
ref = k('ClienteKPayCompraKPay-ReferralProgram'); ref2 = k('ClienteKCashCompraKCash-ReferralProgram')
ins = k('Active-Retargeting_Installments'); nev = k('Nuevos_NeverActive'); chu = k('Churn_12MesesInactividad-ConSinOferta')
resc = k('Leads_BBDDRezagada-RescateTasa0')
e9 = pd.read_csv('/home/user/claude/braze-analysis/data/e9b_patron_respuesta_90d.csv')
wa90 = e9[e9.resp_wa == 0].msgs_wa_entregados.sum() / 1e6
wa90t = e9.msgs_wa_entregados.sum() / 1e6
print('activos', A, 'email', E, 'email total', EMAIL)
print('ex', cpc(ex), ex.costo.sum() / 1e6, 'email ex', cpc(eex), 'nunca', cpc(nv), nv.costo.sum() / 1e6, 'email nunca', cpc(env_))
print('frios conv', fr.conversiones_fraccional.sum(), 100 * fr.conversiones_fraccional.sum() / w.conversiones_fraccional.sum())
print('campañas', ref.round(1).to_dict(), ref2.round(1).to_dict(), ins.round(1).to_dict(), nev.round(1).to_dict(), chu.round(1).to_dict(), resc.round(1).to_dict())
print('E9b WA entregado sin lectura 90d', wa90, wa90t, wa90 / wa90t)
ent = {a: 100 * w[w.aud == a].whatsapp_delivery.sum() / w[w.aud == a].whatsapp_send.sum() for a in AUDS}

S = Svg('Dispersión: gasto de WhatsApp en millones de MXN contra MXN por conversión, por equipo y audiencia; '
        'los clientes activos cuestan 41 a 63 MXN por conversión y las bases frías 579 a 676.')
X0, X1, Y0, Y1 = 58, 520, 80, 360
XM = 10
YL, YH = math.log10(8), math.log10(1300)
sx = lambda v: X0 + (X1 - X0) * v / XM
sy = lambda v: Y1 - (Y1 - Y0) * (math.log10(v) - YL) / (YH - YL)
# leyenda
lx = 0
for a in ('frios', 'leads', 'activos'):
    lab, col = AUDS[a]
    S.circle(lx + 5, 14, 5, col, '')
    txt = f'{lab}: {A[a]:.0f} MXN por conversión'
    S.t(lx + 15, 18, txt, 11.5, INK if a != 'leads' else TXT, w=600 if a != 'leads' else 400)
    lx += 15 + tw(txt, 11.5, 600) + 18
S.t(0, 38, 'Cada punto es un equipo con una audiencia. Bases frías: ex clientes y leads que nunca activaron.', 10.5, SEC)
S.t(X0 - 30, Y0 - 16, 'MXN por conversión (escala que crece por múltiplos)', 11, SEC)
for v in (10, 30, 100, 300, 1000):
    S.line(X0, sy(v), X1, sy(v), GRID)
    S.t(X0 - 8, sy(v) + 4, f'{v:,}', 11, SEC, 'end')
for v in range(0, 11, 2):
    S.line(sx(v), Y1, sx(v), Y1 + 4, G1)
    S.t(sx(v), Y1 + 18, f'{v}', 11, SEC, 'middle')
S.line(X0, Y1, X1, Y1, G1)
S.t(X1, Y1 + 36, 'Gasto de WhatsApp en nueve meses, M MXN', 11, SEC, 'end')
# referencia email
S.line(X0, sy(EMAIL), X1, sy(EMAIL), INK, 1, ' stroke-dasharray="4 4" opacity="0.6"')
S.t(X0 + 6, sy(EMAIL) - 6, f'Correo, todas las audiencias: {EMAIL:.0f} MXN por conversión', 11, INK, halo=True)
# puntos
NAME = {'Marketing': 'Marketing', 'Product Growth': 'Product Growth', 'Sales': 'Sales', 'Others': 'Others'}
OFF = {('Marketing', 'activos'): (10, -4, 'start'), ('Sales', 'activos'): (-10, 14, 'end'), ('Product Growth', 'activos'): (10, 4, 'start'),
       ('Marketing', 'frios'): (-10, -10, 'end'), ('Product Growth', 'frios'): (10, 14, 'start'), ('Marketing', 'leads'): (-10, 4, 'end'),
       ('Sales', 'leads'): (10, 4, 'start'), ('Product Growth', 'leads'): (10, 4, 'start'), ('Others', 'activos'): (10, 4, 'start')}
for r in P.itertuples():
    lab, col = AUDS[r.au]
    S.circle(sx(r.x), sy(r.y), 7, col, ' stroke="#FFFFFF" stroke-width="2"')
for r in P.itertuples():
    dx, dy, an = OFF.get((r.team, r.au), (10, 4, 'start'))
    hi = r.au != 'leads'
    S.t(sx(r.x) + dx, sy(r.y) + dy, f'{NAME[r.team]} · {r.y:,.0f}', 11, INK if hi else TXT, an, 600 if hi else 400, halo=True)
# bloque de ejemplos
RX = 548
S.line(RX - 12, 58, RX - 12, 400, GRID)
S.t(RX, 70, 'Campañas, MXN por conversión', 11.5, INK, w=600)
ej = [('Paga', GREEN, [(f'Referidos a clientes KPay', f'{ref.cpc:.0f}', 'Marketing'),
                       (f'Referidos a clientes KCash', f'{ref2.cpc:.0f}', 'Marketing'),
                       (f'Recordatorio de Installments', f'{ins.cpc:.0f}', 'Product Growth')]),
      ('No paga', BLUE, [(f'Rescate Tasa 0 a rezagados', f'{resc.cpc:,.0f}', 'Marketing'),
                         (f'Ex clientes de un año', f'{chu.cpc:,.0f}', 'Product Growth'),
                         (f'Registrados que nunca activaron', f'{nev.cpc:,.0f}', f'Product Growth, {nev.ent:.0f} % de entrega')])]
yy = 96
for head, col, rows in ej:
    S.t(RX, yy, head, 11, col, w=600)
    yy += 18
    for name, val, who in rows:
        S.t(RX, yy, name, 11, INK)
        S.t(780, yy, val, 11, INK, 'end', 600)
        S.t(RX, yy + 14, who, 10.5, SEC)
        yy += 36
    yy += 10
svg = S.done()

save(12, dict(
    kind='grafica',
    titulo=f'WhatsApp paga con clientes activos y referidos; con ex clientes y leads que nunca activaron cada conversión cuesta {A["frios"]/A["activos"]:.0f} veces más',
    que='A clientes activos: invitar a un amigo (referidos), recordatorios de pagos a meses y ofertas de comercios de KPay. A bases frías: rescates de Tasa 0 y descuentos para que vuelvan.',
    quien=f'Con clientes activos: Sales {py("Sales","activos"):.0f} MXN por conversión, Marketing {py("Marketing","activos"):.0f} y Product Growth {py("Product Growth","activos"):.0f}. Con bases frías: Marketing {py("Marketing","frios"):.0f} y Product Growth {py("Product Growth","frios"):.0f}.',
    a_quien=f'Bases frías: ex clientes (dormants, inactivos, churn), {cpc(ex):.0f} MXN por conversión, y leads que nunca activaron, {cpc(nv):.0f}. Les llega {ent["frios"]:.1f} % de los WhatsApp; a clientes activos, {ent["activos"]:.1f} %.',
    lecturas=[
        f'Clientes activos: {A["activos"]:.0f} MXN por conversión. Bases frías: {A["frios"]:.0f} MXN. Ahí se fueron {fr.costo.sum()/1e6:.1f} M MXN por solo {fr.conversiones_fraccional.sum()/1e3:.0f} mil conversiones, {100*fr.conversiones_fraccional.sum()/w.conversiones_fraccional.sum():.0f} % de las de WhatsApp.',
        f'A ex clientes el correo recupera más barato: {cpc(eex):.0f} MXN por conversión contra {cpc(ex):.0f} por WhatsApp. Push e in-app no cuestan, si la persona tiene la app.',
        f'De julio a septiembre, {wa90:.1f} M MXN de WhatsApp ({100*wa90/wa90t:.0f} % del trimestre) se entregaron a personas que no leyeron ningún WhatsApp en 90 días.',
    ],
    causa='WhatsApp se usa para buscar en volumen a quien ya no lo lee, porque no hay una regla que lo limite a quien lo leyó hace poco ni un presupuesto con límite por equipo.',
    sowhat='Seguir buscando a los ex clientes, pero primero por correo, push e in-app; WhatsApp solo a quien lo leyó en 90 días, con presupuesto con límite y un grupo sin mensajes para medir.',
    fuente=f'{FUENTE_E1}; personas sin lectura de WhatsApp en 90 días de julio a septiembre. Conversión: préstamo o compra en los 7 días después del mensaje, repartida entre los mensajes que la persona recibió ese día; no prueba que el mensaje la causó. WhatsApp a 1.00 MXN por entregado, email a 0.05 MXN por enviado. Puntos con 1 M MXN o más de gasto.',
    svg=svg,
))
