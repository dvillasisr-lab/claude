"""Lámina 17 (ronda 2): cada punto es una campaña de WhatsApp: enviados (x, escala por múltiplos) contra % que llegó (y),
color por audiencia; líneas en 80 % (mínimo) y 90 % (estándar); entrega ponderada de bases frías y de activos; campañas nombradas."""
import math
from b2base import *

d = load_b()
w = d[d.canal == 'whatsapp'].copy()
w['nod'] = w.whatsapp_send - w.whatsapp_delivery
NT, ST = w.nod.sum() / 1e6, w.whatsapp_send.sum() / 1e6
na = w.groupby('aud').nod.sum() / w.nod.sum() * 100
ent_a = w.groupby('aud').apply(lambda g: 100 * g.whatsapp_delivery.sum() / g.whatsapp_send.sum())
fa = w.groupby('fam').agg(s=('whatsapp_send', 'sum'), dl=('whatsapp_delivery', 'sum'), nod=('nod', 'sum'), aud=('aud', 'first'), team=('equipo', 'first')).reset_index()
fa['ent'] = 100 * fa.dl / fa.s
top10 = fa.nod.nlargest(10).sum() / fa.nod.sum()
gt3 = 100 * w[w.gan.isin(['tasa0', 'descuento', 'referidos'])].nod.sum() / w.nod.sum()
sel = fa[fa.s >= 2e4].copy()
sel['a3'] = np.where(sel.aud.isin(['frios', 'activos']), sel.aud, 'otro')
mm = w.groupby('m').apply(lambda g: 100 * g.whatsapp_delivery.sum() / g.whatsapp_send.sum())
e7 = pd.read_csv('/home/user/claude/braze-analysis/data/e7b_patron_respuesta.csv')
nr = e7[(e7[['resp_email', 'resp_push', 'resp_wa', 'resp_inapp']].sum(axis=1) == 0)]
ent_nr = 100 * nr.msgs_wa_entregados.sum() / nr.msgs_wa.sum()
print('no llegaron', NT, ST, NT / ST, 'aud %', na.round(1).to_dict(), 'entrega', ent_a.round(1).to_dict(), 'top10', top10, 'n', len(sel), sel.s.sum() / w.whatsapp_send.sum())
print('mes', mm.round(1).to_dict(), 'nr', ent_nr)
COL = {'frios': BLUE, 'activos': GREEN, 'otro': G2}
S = Svg('Cada punto es una campaña de WhatsApp: mensajes enviados contra cuántos de cada cien llegaron; las de bases frías quedan abajo del mínimo de 80 %.')
lx = 0
for k, lab in (('frios', 'Bases frías'), ('activos', 'Clientes activos'), ('otro', 'Leads y otros')):
    S.circle(lx + 5, 14, 5, COL[k], '')
    txt = f'{lab}: llega {ent_a.get(k, 100*w[~w.aud.isin(["frios","activos"])].whatsapp_delivery.sum()/w[~w.aud.isin(["frios","activos"])].whatsapp_send.sum()):.0f} %'
    S.t(lx + 14, 18, txt, 11.5, INK if k != 'otro' else TXT, w=600 if k != 'otro' else 400)
    lx += 14 + tw(txt, 11.5, 600) + 18
S.t(0, 36, 'Cada punto es una campaña con todas sus versiones; el tamaño es lo que no llegó. Campañas con 20 mil o más envíos.', 10.5, SEC)
X0, X1, Y0, Y1 = 50, 760, 58, 364
XL, XH = math.log10(2e4), math.log10(6e6)
sx = lambda v: X0 + (X1 - X0) * (math.log10(v) - XL) / (XH - XL)
YL, YH = 30, 100
sy = lambda v: Y1 - (Y1 - Y0) * (min(max(v, YL), YH) - YL) / (YH - YL)
for v in (30, 40, 50, 60, 70, 80, 90, 100):
    S.line(X0, sy(v), X1, sy(v), GRID)
    S.t(X0 - 8, sy(v) + 4, f'{v} %', 11, SEC, 'end')
for v, lab in ((2e4, '20 mil'), (1e5, '100 mil'), (3e5, '300 mil'), (1e6, '1 M'), (3e6, '3 M')):
    S.line(sx(v), Y1, sx(v), Y1 + 4, G1)
    S.t(sx(v), Y1 + 17, lab, 11, SEC, 'middle')
S.t(X1, Y1 + 34, 'WhatsApp enviados por campaña en nueve meses (escala que crece por múltiplos)', 10.5, SEC, 'end')
S.t(X0 - 44, Y0 - 10, 'De cada cien enviados, cuántos llegaron', 11, SEC)
S.line(X0, sy(90), X1, sy(90), GREEN, 1.2, ' stroke-dasharray="5 4"')
S.t(X1 - 2, sy(90) - 6, 'Estándar: 90 %', 11, GREEN, 'end', 700, halo=True)
S.line(X0, sy(80), X1, sy(80), INK, 1.2, ' stroke-dasharray="5 4" opacity="0.7"')
S.t(X1 - 2, sy(80) - 6, 'Mínimo: 80 %', 11, INK, 'end', 700, halo=True)
for q in sel.sort_values('nod', ascending=False).itertuples():
    S.circle(sx(q.s), sy(q.ent), 2.2 + 3.2 * math.sqrt(q.nod / 1e6), COL[q.a3], ' fill-opacity="0.8" stroke="#FFFFFF" stroke-width="1"')
NAMES = [('Leads_BBDDRezagada-RescateTasa0-N/A', 'Rescate Tasa 0 a rezagados (Marketing)', -14, 26, 'end'),
         ('Nuevos_NeverActive-InstallmentsNoCash', 'Registrados que nunca activaron (Product Growth)', -14, 6, 'end'),
         ('Recurrentes_Inactivos-DescuentoDirecto', 'Descuento a clientes inactivos (Product Growth)', -14, -18, 'end'),
         ('Recurrentes_ClienteKCashCompraKCash-ReferralProgram', 'Referidos a clientes KCash (Marketing)', -14, -10, 'end')]
for key, lab, dx, dy, an in NAMES:
    q = sel[sel.fam.str.contains(key, regex=False)].sort_values('s').iloc[-1]
    x, y = sx(q.s), sy(q.ent)
    S.line(x, y, x + dx * 0.7, y + dy * 0.7 - 3, INK, 0.7)
    S.t(x + dx, y + dy, f'{lab}: {q.ent:.0f} %', 11, INK, an, 600, halo=True)
    print(lab, round(q.s / 1e6, 2), round(q.ent, 1), round(q.nod / 1e6, 2))
svg = S.done()
resc = sel[sel.fam.str.contains('Leads_BBDDRezagada-RescateTasa0-N/A', regex=False)].iloc[0]
save(17, dict(
    kind='grafica',
    titulo='Uno de cada cuatro WhatsApp no llega, y la mitad de los que no llegan iban a bases frías',
    que=f'Tasa 0, descuentos y referidos: {gt3:.0f} % de lo que no llegó.',
    quien=f'Marketing y Product Growth: 87 % de los WhatsApp que no llegaron.',
    a_quien=f'Bases frías: ex clientes y leads viejos; les llega {ent_a["frios"]:.0f} % contra {ent_a["activos"]:.0f} % a activos.',
    lecturas=[
        f'{NT:.1f} M de {ST:.1f} M WhatsApp no llegaron ({100*NT/ST:.0f} %); {na["frios"]:.0f} % iban a bases frías.',
        f'Diez campañas explican {100*top10:.0f} %; la mayor, rescate Tasa 0 a rezagados: {resc.nod/1e6:.1f} M sin llegar.',
        f'A quien nunca responde por ningún canal le llega {ent_nr:.0f} %. No cuesta (Meta cobra lo entregado), pero la base está sucia.',
    ],
    causa='Las listas de ex clientes y leads viejos no se limpian: se manda a números que ya no existen o no usan WhatsApp.',
    sowhat='Limpiar la base de WhatsApp antes de mandar más: quitar a quien no recibió ninguno en 90 días.',
    fuente=f'{FUENTE_E1}; E7b. No llegó = enviado menos entregado. El motivo (número inválido, sin WhatsApp, bloqueo) no está en los datos.',
    svg=svg,
))
