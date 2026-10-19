"""Lámina 52: correos promocionales que siguen llegando después de darse de baja (E5b), por campaña, equipo, tema y meses.
Arriba: los 1.42 M correos después de la baja partidos en cobranza, avisos y promociones."""
import re
import pandas as pd
from b5_svg import *

R = '/home/user/claude/braze-analysis/'
c = pd.read_csv(R + 'hallazgos/muestra_c_familias.csv'); tipo = c.groupby('familia').tipo.first()
b = pd.read_csv(R + 'data/e5b_comms_despues_baja.csv')
b['f'] = b.familia.map(lambda s: re.sub(r'-\d{8,9}-', '-', s)); b['tipo'] = b.f.map(tipo)
p = b[b.tipo == 'promocional o lifecycle'].copy()
PROGS = [('B0171.*Leads_BBDDRezagada-RescateTasa0', 'Rescate con Tasa 0 a leads rezagados', 'Tasa 0'),
         ('B0326.*Leads-ReferralProgram', 'Referidos a leads', 'Referidos'),
         ('B0171.*HotLeadsW1', 'Rescate con Tasa 0 a hot leads', 'Tasa 0'),
         ('B0211', 'Tasa 0 a registrados de Pay', 'Tasa 0'),
         ('Newsletter', 'Newsletters', 'Lanzamientos y novedades'),
         ('Veriff$', 'Recordatorio de verificar identidad (Veriff)', 'Terminar el registro'),
         ('BillPay', 'Lanzamiento de BillPay', 'Lanzamiento'),
         ('B0392', 'Cuponera de descuentos de marzo', 'Descuentos'),
         ('WeeklyRecommendations', 'Recomendaciones semanales de Shopping', 'Recomendaciones')]
def prog(f):
    for rx, lab, _ in PROGS:
        if re.search(rx, f): return lab
    return 'Resto (31 campañas)'
p['prog'] = p.f.map(prog)
g = p.groupby('prog').agg(e=('emails_despues_de_baja', 'sum'), meses=('meses', 'sum'), eq=('equipo', 'first'), n=('f', 'size'))
g['meses'] = g.meses.clip(upper=9)
TEMA = {lab: t for _, lab, t in PROGS}
orden = [lab for _, lab, _ in PROGS]
orden = sorted(orden, key=lambda k: -g.loc[k, 'e']) + ['Resto (31 campañas)']
nresto = int(g.loc['Resto (31 campañas)', 'n'])
g = g.rename(index={'Resto (31 campañas)': f'Resto ({nresto} campañas)'}); orden[-1] = f'Resto ({nresto} campañas)'
TOT = b.emails_despues_de_baja.sum(); TIP = b.groupby('tipo').emails_despues_de_baja.sum()
promo = TIP['promocional o lifecycle']; cob = TIP['cobranza']; tra = TIP['transaccional u operativa']
eqs = p.groupby('equipo').emails_despues_de_baja.sum()
S = Svg('Correos que llegaron después de darse de baja: arriba, partidos en cobranza, avisos y promociones; abajo, las campañas promocionales con más correos, por equipo, tema y meses.')
S.t(0, 14, f'{M(TOT, 2)} M correos llegaron a gente que ya se había dado de baja', 12, INK, w=600)
x = 0
for v, col, lab in [(cob, MARK2, 'Cobranza'), (tra, MARK2, 'Avisos de pago y contratos'), (promo, BLUE, 'Promociones')]:
    w = W * v / TOT
    S.rect(x, 22, w - 2, 22, col)
    if lab != 'Promociones': S.t(x + 6, 37, f'{lab}: {mil(v)} mil ({100*v/TOT:.0f} %)', 11, INK)
    x += w
S.t(W, 60, f'Promociones: {mil(promo)} mil ({100*promo/TOT:.0f} %)', 11.5, INK, 'end', 600)
S.t(0, 60, 'Cobranza y avisos sí proceden después de la baja. Las promociones no.', 10.5, SEC)
S.line(0, 72, W, 72, GRID)
S.t(0, 92, 'Correos promocionales después de la baja, por campaña', 12, INK, w=600)
S.rect(400, 83, 10, 10, BLUE); S.t(414, 92, 'Marketing', 11, TXT)
S.rect(490, 83, 10, 10, MARK); S.t(504, 92, 'Otros equipos', 11, TXT)
X0, X1 = 250, 520; mx = g.e.max()
for i, k in enumerate(orden):
    r = g.loc[k]; y = 104 + 29 * i
    S.t(X0 - 8, y + 12, k, 11.5, INK if r['eq'] == 'Marketing' else TXT, 'end', 600 if r['eq'] == 'Marketing' else 400)
    w = (X1 - X0) * r.e / mx
    col = BLUE if r['eq'] == 'Marketing' else (MARK2 if k.startswith('Resto') else MARK)
    S.rect(X0, y + 2, w, 15, col)
    eq = r['eq'] if r['eq'] != 'Others' else 'Others'
    extra = '' if k.startswith('Resto') else f' · {TEMA[k]} · {eq}'
    S.t(X0 + w + 6, y + 14, f'{r.e/1e3:.1f} mil', 11.5, INK, w=600)
    S.t(X0 + w + 60, y + 14, (f'{int(r.meses)} meses' if r.meses > 1 else '1 mes') + extra if not k.startswith('Resto') else 'varios equipos', 10.5, SEC)
SVG = S.done()

guarda(52, dict(
    kind='grafica',
    titulo='A quien se dio de baja le siguen llegando promociones de Tasa 0 y referidos, casi todas de Marketing',
    que=f'Correo promocional: Tasa 0 ({mil(D["baja"]["tema"]["Tasa 0"])} mil), lanzamientos y newsletters ({mil(D["baja"]["tema"]["Lanzamiento y novedades"])} mil), referidos ({mil(D["baja"]["tema"]["Referidos"])} mil), descuentos y cupones ({mil(D["baja"]["tema"]["Descuento, cupón u oferta"])} mil) y recordatorio de terminar el registro ({mil(D["baja"]["tema"]["Recordatorio de algo empezado"])} mil).',
    quien=f'Marketing {mil(eqs["Marketing"])} mil, Product Growth {mil(eqs["Product Growth"])} mil, Sales {mil(eqs["Sales"])} mil, Others {mil(eqs["Others"])} mil (BillPay y Shopping) y Acquisition {mil(eqs["Acquisition"])} mil.',
    a_quien=f'{mil(D["baja"]["usuarios"])} mil personas que ya se habían dado de baja del correo, sobre todo leads y registrados que nunca tomaron crédito.',
    lecturas=[
        f'De {M(TOT, 2)} M correos que llegaron después de la baja, {100*(cob+tra)/TOT:.0f} % son cobranza o avisos de pago y contratos, que sí proceden. {mil(promo)} mil son promociones a {mil(D["baja"]["usuarios"])} mil personas.',
        f'{mil(eqs["Marketing"])} de {mil(promo)} mil son de Marketing: rescate con Tasa 0 a leads, referidos y newsletters. El recordatorio de Veriff siguió llegando los nueve meses. Solo {fmt(D["baja"]["clics"])} personas hicieron clic.',
        'Lo más probable: son Canvas largos que revisan la suscripción solo al entrar y no en cada paso, así que quien se da de baja a la mitad recibe los correos que faltan.',
    ],
    causa='El filtro de suscripción está en la entrada del Canvas y no en cada paso de correo. Nadie revisa qué llega después de la baja porque el volumen es chico.',
    sowhat='Es un ajuste de configuración, no una decisión de negocio: poner el filtro de suscripción en cada paso de correo de esos Canvas se corrige en una semana.',
    fuente=f'Fuente: Braze E5b (correos después de la baja), enero a septiembre 2026; tipo de mensaje del catálogo de campañas (muestra C) y tema por el nombre. 79 a 80 mil según se cuenten {fmt(TIP.get("?", 0) if "?" in TIP else 682)} correos sin tipo. Pesa en la reputación del dominio aunque el volumen sea chico.',
    svg=SVG,
))
print(g.sort_values('e', ascending=False))
