"""Lámina 17: WhatsApp no entregado por equipo, partido por audiencia, con la entrega de cada tramo;
a la derecha, entrega mensual contra 80 % (mínimo) y 90 % (estándar)."""
from b2base import *

d = load_b()
w = d[d.canal == 'whatsapp'].copy()
w['nod'] = w.whatsapp_send - w.whatsapp_delivery
AUD = [('frios', 'Bases frías', BLUE), ('leads', 'Leads', BLUE2), ('activos', 'Clientes activos', G1), ('otro', 'Otros', G2)]
w['a4'] = np.where(w.aud.isin(['frios', 'leads', 'activos']), w.aud, 'otro')
EQ = ['Marketing', 'Product Growth', 'Sales', 'Others']
nod = w.pivot_table(index='equipo', columns='a4', values='nod', aggfunc='sum').fillna(0).loc[EQ] / 1e6
snd = w.pivot_table(index='equipo', columns='a4', values='whatsapp_send', aggfunc='sum').fillna(0).loc[EQ]
dlv = w.pivot_table(index='equipo', columns='a4', values='whatsapp_delivery', aggfunc='sum').fillna(0).loc[EQ]
ent = 100 * dlv / snd.replace(0, np.nan)
NT, ST = w.nod.sum() / 1e6, w.whatsapp_send.sum() / 1e6
na = w.groupby('a4').nod.sum() / 1e6
ne = w.groupby('equipo').nod.sum() / 1e6
ee = w.groupby('equipo').apply(lambda g: 100 * g.whatsapp_delivery.sum() / g.whatsapp_send.sum())
mm = w.groupby('m').apply(lambda g: 100 * g.whatsapp_delivery.sum() / g.whatsapp_send.sum())
gt = 100 * w.groupby('gan').nod.sum() / w.nod.sum()
fam = w.groupby('fam').agg(nod=('nod', 'sum'), s=('whatsapp_send', 'sum'), dl=('whatsapp_delivery', 'sum'))
fam['ent'] = 100 * fam.dl / fam.s
top10 = fam.nod.nlargest(10).sum() / fam.nod.sum()
print(nod.round(2)); print(ent.round(1)); print('total', NT, ST, NT / ST, 'aud', (100 * na / NT).round(1).to_dict(), 'eq', ne.round(2).to_dict(), (100 * ne / NT).round(0).to_dict())
print('entrega eq', ee.round(1).to_dict(), 'mes', mm.round(1).to_dict(), 'tema', gt.round(0).to_dict(), 'top10', top10)
k = lambda s: fam.loc[[i for i in fam.index if s in i]].sort_values('nod').iloc[-1]
resc = k('Leads_BBDDRezagada-RescateTasa0'); nev = k('Nuevos_NeverActive'); ina = k('Recurrentes_Inactivos-DescuentoDirecto'); dor = k('Recurrentes_Dormants-ReferralProgram')
print('ej', resc.nod / 1e6, resc.ent, nev.ent, ina.ent, dor.ent)
e9 = pd.read_csv('/home/user/claude/braze-analysis/data/e7b_patron_respuesta.csv')
nr = e9[(e9.resp_email == 0) & (e9.resp_push == 0) & (e9.resp_wa == 0) & (e9.resp_inapp == 0)]
ent_nr = 100 * nr.msgs_wa_entregados.sum() / nr.msgs_wa.sum()
print('entrega a quien nunca responde', ent_nr)

S = Svg('Izquierda: millones de WhatsApp no entregados por equipo y audiencia, con la entrega de cada tramo. '
        'Derecha: entrega mensual de WhatsApp contra 80 % y 90 %.')
S.t(0, 16, 'WhatsApp que no llegaron, millones, enero a septiembre', 12, INK, w=600)
lx = 0
for a, lab, col in AUD:
    S.rect(lx, 25, 10, 10, col)
    txt = f'{lab} {na.get(a, 0):.1f} M'
    S.t(lx + 14, 34, txt, 11, INK if a == 'frios' else TXT, w=600 if a == 'frios' else 400)
    lx += 14 + tw(txt, 11) + 8
S.t(0, 52, 'Dentro de la barra: de cada cien WhatsApp enviados a ese grupo, cuántos llegaron.', 10.5, SEC)
BX0, BX1 = 104, 372
VM = 9
sx = lambda v: BX0 + (BX1 - BX0) * v / VM
for v in range(0, 10, 2):
    S.line(sx(v), 70, sx(v), 336, GRID)
    S.t(sx(v), 350, f'{v} M', 10.5, SEC, 'middle')
for i, eq in enumerate(EQ):
    y = 84 + i * 64
    hi = eq in ('Marketing', 'Product Growth')
    S.t(BX0 - 8, y + 19, eq, 11.5, INK if hi else TXT, 'end', 600 if hi else 400)
    x = BX0
    for a, lab, col in AUD:
        v = nod.loc[eq].get(a, 0)
        ww = sx(v) - BX0
        if ww <= 0.3:
            continue
        S.rect(x, y, ww - (1.5 if ww > 3 else 0), 28, col)
        if ww >= 34:
            S.t(x + ww / 2, y + 18.5, f'{ent.loc[eq, a]:.0f} %', 10.5, '#FFFFFF' if col == BLUE else INK, 'middle', 600)
        x += ww
    S.t(x + 6, y + 13, f'{ne[eq]:.1f} M · {100*ne[eq]/NT:.0f} %', 11.5, INK if hi else TXT, 'start', 600 if hi else 400)
    S.t(x + 6, y + 27, f'llega {ee[eq]:.0f} %', 10.5, SEC)
S.t(0, 380, f'{NT:.1f} M de {ST:.1f} M WhatsApp no llegaron ({100*NT/ST:.0f} %); {100*na["frios"]/NT:.0f} % iban a bases frías.', 11.5, INK, w=600)
S.t(0, 398, 'No cuesta: Meta cobra solo el entregado. Sí dice que esos números ya no sirven.', 11, TXT)
S.line(458, 8, 458, 404, GRID)
# ===== entrega mensual
X0, X1, Y0, Y1 = 500, 770, 70, 330
LOY, HIY = 60, 95
sxm = lambda i: X0 + (X1 - X0) * i / 8
sym = lambda v: Y1 - (Y1 - Y0) * (v - LOY) / (HIY - LOY)
S.t(474, 16, 'De cada cien enviados, cuántos llegaron', 12, INK, w=600)
S.t(474, 34, 'Por mes', 10.5, SEC)
for v in (60, 70, 80, 90):
    S.line(X0, sym(v), X1, sym(v), GRID)
    S.t(X0 - 6, sym(v) + 4, f'{v} %', 10.5, SEC, 'end')
S.line(X0, sym(90), X1, sym(90), GREEN, 1.2, ' stroke-dasharray="4 4"')
S.t(X1, sym(90) - 6, 'Estándar: 90 %', 10.5, GREEN, 'end', 600, halo=True)
S.line(X0, sym(80), X1, sym(80), INK, 1, ' stroke-dasharray="4 4" opacity="0.6"')
S.t(X1, sym(80) - 6, 'Mínimo: 80 %', 10.5, INK, 'end', 600, halo=True)
MES = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep']
pts = ' '.join(f'{sxm(i):.1f},{sym(mm[i+1]):.1f}' for i in range(9))
S.raw(f'<polyline points="{pts}" fill="none" stroke="{BLUE}" stroke-width="2.2"/>')
for i in range(9):
    v = mm[i + 1]
    hi = i + 1 in (1, 4, 5, 9)
    S.circle(sxm(i), sym(v), 4.5 if hi else 3.5, BLUE, ' stroke="#FFFFFF" stroke-width="1.5"')
    if hi:
        S.t(sxm(i), sym(v) + 17, f'{v:.0f}', 11, BLUE, 'middle', 700, halo=True)
    S.t(sxm(i), Y1 + 16, MES[i], 10.5, TXT, 'middle')
S.t(474, 380, f'Tocó fondo en abril y mayo ({mm[4]:.0f} % y {mm[5]:.0f} %)', 11, INK, w=600)
S.t(474, 398, f'y aun así salieron {w[w.m==4].whatsapp_send.sum()/1e6:.1f} M y {w[w.m==5].whatsapp_send.sum()/1e6:.1f} M WhatsApp.', 11, TXT)
svg = S.done()

save(17, dict(
    kind='grafica',
    titulo='Uno de cada cuatro WhatsApp no llega, y la mitad de los que no llegan iban a ex clientes y a leads que nunca activaron',
    que=f'Lo que no llega es sobre todo Tasa 0 ({gt["tasa0"]:.0f} % de lo no entregado), descuentos ({gt["descuento"]:.0f} %) y referidos ({gt["referidos"]:.0f} %).',
    quien=f'Marketing {ne["Marketing"]:.1f} M no entregados ({100*ne["Marketing"]/NT:.0f} %), Product Growth {ne["Product Growth"]:.1f} M ({100*ne["Product Growth"]/NT:.0f} %), Sales {ne["Sales"]:.1f} M ({100*ne["Sales"]/NT:.0f} %). Llega: Sales {ee["Sales"]:.0f} %, Marketing {ee["Marketing"]:.0f} %, Product Growth {ee["Product Growth"]:.0f} %.',
    a_quien=f'Pesa más la base que el equipo: Marketing entrega {ent.loc["Marketing","frios"]:.0f} % a bases frías y {ent.loc["Marketing","activos"]:.0f} % a clientes activos; Sales {ent.loc["Sales","leads"]:.0f} % a leads y {ent.loc["Sales","activos"]:.0f} % a activos.',
    lecturas=[
        f'{NT:.1f} M de {ST:.1f} M WhatsApp no llegaron: {100*NT/ST:.0f} %. Diez campañas explican {100*top10:.0f} %; la mayor es el rescate de Tasa 0 a leads rezagados de Marketing, {resc.nod/1e6:.1f} M sin llegar.',
        f'A quien nunca responde por ningún canal solo le llega {ent_nr:.0f} % de los WhatsApp. Registrados que nunca activaron (Product Growth): {nev.ent:.0f} %.',
        'No cuesta dinero, pero dice que la base está sucia: números que ya no existen, sin WhatsApp o que nos bloquearon. Hoy no sabemos cuántos son bloqueos.',
    ],
    causa='Las listas de ex clientes y leads viejos no se limpian: se manda a números que dejaron de existir o de usar WhatsApp, y nadie revisa la entrega antes de volver a mandar.',
    sowhat='Limpiar la base de WhatsApp de ex clientes y leads viejos antes de mandar más: quitar a quien no recibió en 90 días.',
    fuente=f'{FUENTE_E1}; personas por respuesta en nueve meses. No entregado = enviado menos entregado. El motivo (número inválido, sin WhatsApp, bloqueo) y la calidad del número ante Meta necesitan el evento de falla con su razón, que no está en los datos.',
    svg=svg,
))
