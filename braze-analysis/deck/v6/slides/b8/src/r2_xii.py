# Ronda 2, sección XII (láminas 91 a 97): gráficas granulares y menos texto. La 92 conserva su SVG aprobado.
import json, math, random, pandas as pd, numpy as np
from kit import *
from plot import *
import datos
D = datos.ROOT + 'data/'
c = datos.load_c(); S3 = datos.load_s3(); R = S3['R']; DUP = datos.dup_mes()
TOT, SEG, MED = R['total'], R['seguro'], R['medir']
c['seg'] = c.b_desp + c.b_cortar + c.b_pref
FU = 'Fuente: E1 de septiembre 2026, acciones del Sheets v4, E9b, E7a y E6b; WhatsApp a 1.00 MXN por entregado, email a 0.05 por enviado.'
NOM = {('B0333', 'whatsapp'): 'Ex clientes KPay, 12 meses', ('B0211', 'email'): 'Tasa 0 a registrados', ('B0332', 'whatsapp'): 'Ex clientes KPay, 6 meses',
       ('B0223', 'email'): 'Installments a registrados', ('B0223', 'whatsapp'): 'Installments a registrados', ('B0619', 'whatsapp'): 'Venta cruzada KPay a Cash',
       ('B0620', 'whatsapp'): 'Venta cruzada a leads KPay', ('B0331', 'whatsapp'): 'Ex clientes KPay, 3 meses', ('B0000', 'email'): 'Recordatorio de verificación',
       ('B0209', 'email'): 'Descuento a inactivos de Cash', ('B0301', 'whatsapp'): 'Cash a plazos a activos', ('B0335', 'email'): 'Promociones de comercios',
       ('B0603', 'email'): 'Cuponera', ('B0598', 'email'): 'Privalia', ('S0004', 'email'): 'Recomendaciones Shopping', ('B0615', 'whatsapp'): 'Comercio del día',
       ('T2778', 'whatsapp'): 'Aviso a adultos mayores', ('B0541', 'email'): 'Amazon', ('B0337', 'email'): 'Cuesta de enero'}
def nombre(f, cn):
    tk = datos.ticket(f)
    if tk == 'B0326': return 'Referidos a dormants ' + ('KPay' if '-KPay-' in f else 'KCash') if 'Dormant' in f else 'Referidos a leads'
    if tk == 'B0171': return 'Rescate Tasa 0 a leads ' + ('rezagados' if 'Rezagada' in f else 'calientes')
    return NOM.get((tk, cn), tk)
CN = {'email': 'correo', 'whatsapp': 'WhatsApp'}

# ------------------------------------------------------------------ 91. Divisor
save(91, dict(kind='divisor', acto='Acto 3 · Cómo lo resolvemos',
    titulo=f'Corregirlo vale hasta {m(TOT)} M MXN al mes: limpiar en 30 días, configurar en 60 y medir en 90',
    subtitulo=f'{m(SEG)} M MXN al mes se quitan ya sin perder ventas. Los otros {m(MED)} M son ex clientes y personas sin respuesta: se quitan solo si un grupo sin mensajes muestra que no recuperan.'))

# ------------------------------------------------------------------ 92. Aprobada: mismo SVG, menos texto
p92 = OUT + '092.json'; d92 = json.load(open(p92))
d92.update(
    titulo='Podemos gastar hasta 2.34 M MXN menos al mes en mensajes, y 1.48 M se quita ya sin perder ventas',
    que='Mensajes a bloqueados, repetidos, pruebas y campañas que nadie responde; cobranza no',
    quien='Product Growth 67 %, Marketing 21 %, Sales 8 %, Others 2 %',
    a_quien='Leads y registrados sin crédito, ex clientes, bloqueados y quien no responde',
    lecturas=['2.34 M MXN al mes: 55 % de lo que gastamos en septiembre (4.23 M) y 28 M MXN al año.',
              '1.48 M se quita ya; lo más grande es apagar correo y WhatsApp a leads que no responden (0.76 M).',
              '0.85 M son ex clientes y gente sin respuesta: se quita solo si un grupo sin mensajes compra igual.'],
    causa='Nadie fija cuánto debe responder una campaña para seguir activa ni prueba si vende con un grupo sin mensajes.',
    sowhat='Aprobar hoy 1.48 M MXN al mes y decidir en dos meses los 0.85 M con el grupo sin mensajes.',
    fuente=FU)
d92.pop('n', None); d92.pop('kind', None); d92.pop('svg', None) if False else None
save(92, dict(kind='grafica', **{k_: v for k_, v in d92.items() if k_ not in ('n', 'kind')}))

# ------------------------------------------------------------------ 93. Pareto: campañas ordenadas por ahorro, se quita ya contra a medir
o = svg_open('Ahorro acumulado por campaña en un canal, ordenadas de mayor a menor, por separado lo que se quita ya y lo que se mide.')
X0, X1, Y0, Y1 = 60, 640, 30, 372
sx = logs(1, 200, X0, X1); sy = lin(0, 1.6e6, Y1, Y0)
xaxis(o, sx, [1, 3, 10, 30, 100], Y0, Y1, fmt=lambda v: f'{v:g}', title='Campañas en un canal, de la de más ahorro a la de menos (escala logarítmica)', title_y=404, x_mid=(X0 + X1) / 2)
yaxis(o, sy, [0, 0.4e6, 0.8e6, 1.2e6, 1.6e6], X0, X1, fmt=lambda v: f'{v / 1e6:.1f} M' if v else '0')
o.append(t(X0 + 4, Y0 - 12, 'MXN al mes, acumulado', 11, SEC, 600))
stats = {}
for k_, col, lab in (('seg', BLUE, 'Se quita ya'), ('b_medir', GREEN, 'Se mide antes de cortar')):
    s = c[c[k_] > 0].sort_values(k_, ascending=False).reset_index(drop=True)
    cs = s[k_].cumsum()
    pts = ' '.join(f'{sx(i + 1):.1f},{sy(v):.1f}' for i, v in enumerate(cs) if i < 200)
    o.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2"/>')
    for i, v in enumerate(cs[:200]):
        dot(o, sx(i + 1), sy(v), 2.6 if i >= 10 else 3.6, col, '#fff', None, 0.8)
    stats[k_] = (len(s), cs.iloc[-1], cs.iloc[9] / cs.iloc[-1], s)
    o.append(t(sx(len(s)) + 8, sy(cs.iloc[-1]) + 4, f'{lab}', 12, col, 700))
    o.append(t(sx(len(s)) + 8, sy(cs.iloc[-1]) + 19, f'{m(cs.iloc[-1])} M en {len(s)} campañas', 11, SEC))
    if k_ == 'seg': o.append(t(sx(len(s)) + 8, sy(cs.iloc[-1]) + 33, f'más {DUP / 1e6:.2f} M de duplicados', 11, SEC) + t(sx(len(s)) + 8, sy(cs.iloc[-1]) + 47, f'= {m(SEG)} M', 11, BLUE, 700))
    o.append(f'<line x1="{sx(10):.1f}" y1="{sy(cs.iloc[9]):.1f}" x2="{sx(10):.1f}" y2="{Y1}" stroke="{col}" stroke-width="0.8"/>')
sg, md = stats['seg'][3], stats['b_medir'][3]
cs_s, cs_m = sg.seg.cumsum(), md.b_medir.cumsum()
note(o, sx(1), sy(cs_s[0]), sx(1) + 14, sy(cs_s[0]) - 110, f'{nombre(sg.fam[0], sg.canal[0])}, {CN.get(sg.canal[0])}', 'start', 11.5, BLUE, 700, sub=f'{m(sg.seg[0])} M')
note(o, sx(2), sy(cs_s[1]), sx(2) + 16, sy(cs_s[1]) - 30, f'{nombre(sg.fam[1], sg.canal[1])}, {CN.get(sg.canal[1])}', 'start', 11.5, BLUE, 400)
note(o, sx(1), sy(cs_m[0]), sx(1) + 14, sy(cs_m[0]) + 26, f'{nombre(md.fam[0], md.canal[0])}, {CN.get(md.canal[0])}', 'start', 11.5, GREEN, 700, sub=f'{m(md.b_medir[0])} M')
note(o, sx(2), sy(cs_m[1]), sx(2) + 16, sy(cs_m[1]) + 34, f'{nombre(md.fam[1], md.canal[1])}, {CN.get(md.canal[1])}', 'start', 11.5, GREEN, 400)
o.append(t(sx(10) + 5, Y1 - 8, f'10 campañas: {stats["seg"][2] * 100:.0f} % y {stats["b_medir"][2] * 100:.0f} %', 11, INK, 600, 'start', True))
o.append('</svg>')
print('93', {k_: (v[0], round(v[1] / 1e6, 3), round(v[2], 2)) for k_, v in stats.items()})
save(93, dict(kind='grafica',
    titulo='Casi dos tercios del ahorro se quita ya sin perder ventas, y diez campañas son más de la mitad',
    que='Promoción de activación, ofertas a ex clientes y promoción a bloqueados o de prueba',
    quien='Product Growth en el corte y en la recuperación; Marketing en el canal preferido',
    a_quien='Leads y registrados sin crédito, contra ex clientes con historial',
    lecturas=[f'Se quita ya: {m(SEG)} M MXN al mes; las 10 campañas más grandes son {stats["seg"][2] * 100:.0f} % (Tasa 0 a registrados, la primera).',
              f'Se mide: {m(MED)} M; dos ofertas a ex clientes de KPay por WhatsApp son {(md.b_medir[0] + md.b_medir[1]) / stats["b_medir"][1] * 100:.0f} %.',
              'La recuperación no se apaga: canal barato, 3 mensajes en 30 días y 10 % sin mensajes 8 semanas.'],
    causa='Hoy se trata igual a quien nunca fue cliente que a quien ya compró: los dos reciben WhatsApp y correo.',
    sowhat=f'Aprobar hoy {m(SEG)} M MXN al mes empezando por 10 campañas; los {m(MED)} M se deciden en dos meses.',
    fuente=FU + f' Sin duplicados del mismo día ({DUP / 1e6:.2f} M), que no se asignan a una campaña.',
    svg=''.join(o)))

# ------------------------------------------------------------------ 94. Franja por equipo: ahorro por campaña
EQS = ['Product Growth', 'Marketing', 'Sales', 'Others']
x = c[(c.tot >= 1000) & c.equipo.isin(EQS)].copy()
x['col'] = np.where(x.seg >= x.b_medir, BLUE, GREEN)
o = svg_open('Ahorro al mes por campaña en un canal, una fila por equipo; azul se quita ya, verde se mide.')
dot(o, 6, 12, 5, BLUE, None); o.append(t(16, 16.5, 'Sobre todo se quita ya', 11.5, TXT))
dot(o, 186, 12, 5, GREEN, None); o.append(t(196, 16.5, 'Sobre todo se mide', 11.5, TXT))
o.append(f'<line x1="346" y1="6" x2="346" y2="18" stroke="{INK}" stroke-width="2"/>' + t(354, 16.5, 'Mediana', 11.5, TXT))
X0, X1 = 118, 668; sx = logs(1e3, 5e5, X0, X1)
xaxis(o, sx, [1e3, 1e4, 1e5, 5e5], 34, 372, title='MXN al mes por campaña en un canal (escala logarítmica)', title_y=404, x_mid=(X0 + X1) / 2)
o.append(t(780, 44, 'Total del equipo', 11, SEC, 600, 'end'))
rnd = random.Random(3)
for i, eq in enumerate(EQS):
    yc = 84 + i * 80
    g = x[x.equipo == eq].sort_values('tot', ascending=False)
    o.append(t(0, yc - 2, eq, 12.5, INK, 700) + t(0, yc + 13, f'{len(g)} campañas', 11, SEC))
    o.append(f'<line x1="{X0}" y1="{yc}" x2="{X1}" y2="{yc}" stroke="{GRID}" stroke-width="1"/>')
    r_y = {}
    for ix, r in g.iterrows():
        r_y[ix] = yc + rnd.uniform(-13, 13)
        dot(o, sx(r.tot), r_y[ix], 4.2, r.col, '#fff', None, 1)
    md_ = median(list(g.tot))
    o.append(f'<line x1="{sx(md_):.1f}" y1="{yc - 18}" x2="{sx(md_):.1f}" y2="{yc + 18}" stroke="{INK}" stroke-width="2"/>')
    te = c[c.equipo == eq].tot.sum()
    o.append(t(780, yc + 4, f'{m(te)} M MXN', 13, INK, 700, 'end') + t(780, yc + 19, f'{te / TOT * 100:.0f} % del ahorro', 11, SEC, 400, 'end'))
    for j in range(min(2 if eq in ('Product Growth', 'Marketing') else 1, len(g))):
        r = g.iloc[j]
        px = sx(r.tot); py = r_y[r.name]
        an = 'end' if px > 520 else 'start'
        note(o, px, py, px + (6 if an == 'end' else -6), yc - 24 if j == 0 else yc + 34, f'{nombre(r.fam, r.canal)}, {CN.get(r.canal, r.canal)}', an, 11, r.col, 700)
o.append('</svg>')
pg = c[c.equipo == 'Product Growth']; mk = c[c.equipo == 'Marketing']
print('94', x.groupby('equipo').size().to_dict())
save(94, dict(kind='grafica',
    titulo='Dos de cada tres pesos del ahorro están en Product Growth, en pocas campañas grandes de correo y WhatsApp',
    que='Tasa 0 e Installments a registrados, ofertas a ex clientes, referidos, rescate a leads',
    quien=f'Product Growth {m(pg.tot.sum())} M MXN al mes; Marketing {m(mk.tot.sum())} M; Sales y Others, el resto',
    a_quien='Registrados sin crédito, ex clientes de KPay, leads y dormants',
    lecturas=[f'Product Growth: sus 2 campañas más grandes valen {m(pg.tot.nlargest(2).sum())} M de sus {m(pg.tot.sum())} M MXN al mes.',
              f'Marketing: {len(x[x.equipo == "Marketing"])} campañas medianas; su ahorro es sobre todo canal preferido y medir recuperación.',
              'Sales y Others: campañas de menos de 25 mil MXN al mes cada una; se rehacen, no se apagan.'],
    causa='Product Growth escribe en volumen a quien nunca respondió y a ex clientes por WhatsApp, sin grupo sin mensajes.',
    sowhat='Empezar por Tasa 0 e Installments a registrados y por las ofertas a ex clientes de KPay.',
    fuente=FU + ' Campañas con mil MXN al mes de ahorro o más.',
    svg=''.join(o)))

# ------------------------------------------------------------------ 95. Segmentos: envíos contra respuesta, correo | push
e7 = pd.read_csv(D + 'e7b_patron_respuesta.csv'); anyr = (e7.resp_email + e7.resp_push + e7.resp_wa + e7.resp_inapp) > 0
N = e7[~anyr].sum(); NT = sum(N[k_] for k_ in ('msgs_email', 'msgs_push', 'msgs_wa', 'msgs_inapp'))
e11 = pd.read_csv(D + 'e11_segmentacion.csv'); e11['r'] = 100 * e11.respuestas / e11.envios
SUB = {'Tasa0': 'Tasa 0', 'ReferralProgram': 'Referidos', 'InstallmentsNoCash': 'Installments', 'RescateTasa0': 'Rescate Tasa 0',
       'RescateFinesDeSemana': 'Rescate de fin de semana', 'Retargeting_Veriff': 'Recordatorio de verificación', 'CuestaEnero': 'Cuesta de enero',
       'Comerciodeldia': 'Comercio del día', 'ComercioDelDia': 'Comercio del día'}
SEGN = {'New': 'nuevos', 'Recurrent': 'recurrentes', 'Leads': 'leads', 'Anonimos': 'anónimos', 'Todos': 'todos'}
o = svg_open('Un punto por segmento de Braze, equipo y canal: envíos contra respuesta, con el mínimo aceptable de cada canal.')
under = {}
for j, (cn, lab, mn, lo, hi, tks, mnl) in enumerate((('email', 'Correo', 0.3, 0.03, 10, [0.03, 0.1, 0.3, 1, 3, 10], '3 clics por mil'), ('push notification', 'Push', 0.75, 0.1, 15, [0.1, 0.3, 1, 3, 10], '7.5 aperturas por mil'))):
    x0 = 52 + j * 392; x1 = x0 + 330; Y0, Y1 = 36, 372
    g = e11[(e11.canal == cn) & (e11.envios >= 1e5) & (e11.segment != 'Not Tracked')]
    sx = logs(1e5, 5e7, x0, x1); sy = logs(lo, hi, Y1, Y0)
    o.append(t(x0, 18, f'{lab}: {len(g)} segmentos', 13, INK, 700))
    xaxis(o, sx, [1e6, 1e7], Y0, Y1)
    yaxis(o, sy, tks, x0, x1, fmt=lambda v: f'{v:g} %')
    o.append(f'<line x1="{x0}" y1="{sy(mn):.1f}" x2="{x1}" y2="{sy(mn):.1f}" stroke="{GREEN}" stroke-width="1.2"/>')
    o.append(t(x1, sy(mn) - 6, f'Mínimo: {mnl}', 11, GREEN, 600, 'end', True))
    bad = (g.r < mn)
    under[cn] = g[bad].envios.sum() / g.envios.sum()
    for _, r in g.iterrows():
        big_bad = r.r < mn and r.envios >= 2e6
        dot(o, sx(r.envios), sy(min(max(r.r, lo), hi)), 4 if big_bad else 2.8, BLUE if big_bad else MARK, '#fff', None, 0.8)
    lab_ = g[(g.r < mn)].sort_values('envios', ascending=False).head(4)
    for i, (_, r) in enumerate(lab_.iterrows()):
        px, py = sx(r.envios), sy(r.r)
        nm_ = f'{SUB.get(r.subsegment, r.subsegment)} a {SEGN.get(r.segment, r.segment)}'
        ty = sy(mn) + 28 + i * 31
        note(o, px, py, px - 8 if px > x0 + 200 else px + 8, ty, nm_, 'end' if px > x0 + 200 else 'start', 11, BLUE, 700, sub=f'{m(r.envios, 1)} M, {r.r:.2f} %')
o.append(t(400, 404, 'Envíos de enero a septiembre por segmento, equipo y canal (escala logarítmica); respuesta = clic en correo, apertura en push', 11, SEC, 400, 'middle'))
o.append('</svg>')
print('95', {k_: round(v, 3) for k_, v in under.items()})
save(95, dict(kind='grafica',
    titulo='Nunca respondieron 14.2 M de personas, y los segmentos de correo más grandes quedan debajo del mínimo',
    que=f'Sobre todo correo: {N.msgs_email / NT * 100:.0f} de cada 100 mensajes que reciben quienes nunca responden',
    quien='Sobre todo Marketing y Product Growth; el cruce exacto por equipo no existe',
    a_quien='Leads, nuevos registrados, Todos y anónimos',
    lecturas=[f'{m(N.usuarios, 1)} M de {m(e7.usuarios.sum(), 1)} M personas no respondieron por ningún canal en nueve meses.',
              f'{under["email"] * 100:.0f} % del correo por segmento va a segmentos debajo de 3 clics por mil, como Tasa 0 a nuevos.',
              f'Les escribimos {m(NT, 1)} M mensajes ({N.msgs_email * 0.05 / 1e6 + N.msgs_wa_entregados / 1e6:.1f} M MXN) y cuentan para el costo fijo de Braze.'],
    causa='Las listas se arman por etapa (lead, registrado, todos), no por si la persona responde.',
    sowhat=f'Su ahorro ({m(c.sin_respuesta_90d.sum())} M MXN al mes) ya está en la lámina 92, como recuperación a medir.',
    fuente='Fuente: Braze, personas por canal al que responden (E7b) y segmentos (E11), enero a septiembre 2026; segmentos con 100 mil envíos o más.',
    svg=''.join(o)))

# ------------------------------------------------------------------ 96. KCash | KPay: gasto de septiembre contra ahorro como % del gasto
pr = c.tipo == 'promocional o lifecycle'; psep = c[pr].groupby('p2').c_sep.sum()
o = svg_open('Un punto por campaña en un canal: ahorro al mes por tipo de acción, KCash y KPay en paneles con la misma escala.')
BK = [('b_desp', 'Bloqueados y pruebas', 'semana 1', BLUE), ('b_cortar', 'Cortar', 'en 30 días', BLUE), ('b_pref', 'Canal preferido', 'en 60 días', BLUE), ('b_medir', 'Recuperar clientes', 'se mide', GREEN)]
LX = 128; PW = 300; GAP = 22
pk = {}
rnd = random.Random(5)
for j, p in enumerate(('KCash', 'KPay')):
    x0 = LX + j * (PW + GAP); x1 = x0 + PW
    sx = logs(1e3, 5e5, x0, x1 - 52)
    tp = c[c.p2 == p].tot.sum(); pk[p] = (tp, c[c.p2 == p].b_cortar.sum(), c[c.p2 == p].b_medir.sum())
    o.append(t(x0, 18, f'{p}: {m(tp)} M MXN al mes', 13, INK, 700))
    o.append(t(x0, 34, f'{tp / psep[p] * 100:.0f} % de su promoción de septiembre', 11, SEC))
    xaxis(o, sx, [1e3, 1e4, 1e5], 46, 372)
    for i, (k_, lab, when, col) in enumerate(BK):
        yc = 84 + i * 80
        if j == 0:
            o.append(t(0, yc - 2, lab, 12.5, INK, 700) + t(0, yc + 13, when, 11, GREEN if col == GREEN else SEC, 600 if col == GREEN else 400))
        o.append(f'<line x1="{x0}" y1="{yc}" x2="{x1 - 52}" y2="{yc}" stroke="{GRID}" stroke-width="1"/>')
        g = c[(c.p2 == p) & (c[k_] >= 1000)].sort_values(k_, ascending=False)
        for _, r in g.iterrows():
            dot(o, sx(r[k_]), yc + rnd.uniform(-12, 12), 4, col, '#fff', None, 1)
        v = c[c.p2 == p][k_].sum()
        big = (p == 'KCash' and k_ == 'b_cortar') or (p == 'KPay' and k_ == 'b_medir')
        o.append(t(x1, yc + 4, f'{m(v)} M', 13 if big else 12, col if big else INK, 700 if big else 400, 'end'))
        if big:
            r = g.iloc[0]
            note(o, sx(r[k_]), yc, sx(r[k_]) - 4, yc - 22, f'{nombre(r.fam, r.canal)}, {CN.get(r.canal, r.canal)}', 'end', 11, col, 700)
o.append(t(LX + PW + GAP / 2, 404, 'MXN al mes de ahorro por campaña en un canal (escala logarítmica); a la derecha, total del producto', 11, SEC, 400, 'middle'))
o.append('</svg>')
blq = c.groupby('p2').bloqueados.sum()
print('96', {p: tuple(round(v / 1e6, 3) for v in t_) for p, t_ in pk.items()})
save(96, dict(kind='grafica',
    titulo='KCash y KPay ahorran casi lo mismo por razones distintas: en KCash se corta, en KPay hay que medir',
    que='KCash: Tasa 0 e Installments a registrados. KPay: ofertas a ex clientes, comercios',
    quien='Product Growth en los dos; Marketing pesa más en KCash y Sales solo en KPay',
    a_quien='KCash: leads y registrados. KPay: ex clientes y tarjetas congeladas',
    lecturas=[f'KCash: {m(pk["KCash"][1])} M de su ahorro se quita en 30 días; lo mayor, Tasa 0 a registrados por correo.',
              f'KPay: {m(pk["KPay"][2])} M es recuperación por WhatsApp a ex clientes; se mide antes de cortar.',
              f'KPay manda más promoción a bloqueados: {m(blq["KPay"])} M contra {m(blq["KCash"])} M MXN al mes en KCash.'],
    causa='Cada producto arma sus listas por su lado y ninguno mide si sus mensajes traen de vuelta al cliente.',
    sowhat='Con KCash, apagar lo que no responde; con KPay, probar con un grupo sin mensajes antes de cortar.',
    fuente=FU + ' Producto por el segundo campo del nombre; campañas con mil MXN o más de ahorro.',
    svg=''.join(o)))

# ------------------------------------------------------------------ 97. Pareto de bajas de correo por campaña
em = c[(c.canal == 'email') & (c.es > 0)].copy().sort_values('eu', ascending=False).reset_index(drop=True)
em['pl'] = em.accion.isin(['Apagar', 'Bajar frecuencia', 'Rehacer o re-segmentar', 'Confirmar apagado'])
em['cb'] = 100 * em.eu.cumsum() / em.eu.sum(); em['ce'] = 100 * em.es.cumsum() / em.es.sum()
n10b, n10e, n10p = em.cb[9], em.ce[9], int(em.pl[:10].sum())
o = svg_open('Campañas de correo ordenadas por bajas: porcentaje acumulado de bajas y de correos enviados.')
X0, X1, Y0, Y1 = 52, 770, 30, 372
sx = logs(1, len(em), X0, X1); sy = lin(0, 100, Y1, Y0)
xaxis(o, sx, [1, 3, 10, 30, 100, 300], Y0, Y1, fmt=lambda v: f'{v:g}', title=f'Campañas de correo, de la que más bajas dejó a la que menos ({len(em)} en total, escala logarítmica)', title_y=404, x_mid=(X0 + X1) / 2)
yaxis(o, sy, [0, 25, 50, 75, 100], X0, X1, fmt=lambda v: f'{v:g} %')
for k_, col, lab in (('ce', MARK, 'Correos enviados'), ('cb', BLUE, 'Bajas de correo')):
    pts = ' '.join(f'{sx(i + 1):.1f},{sy(v):.1f}' for i, v in enumerate(em[k_]))
    o.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2"/>')
for i in range(10):
    dot(o, sx(i + 1), sy(em.cb[i]), 4, BLUE if em.pl[i] else MARK, '#fff', None, 1)
o.append(f'<line x1="{sx(10):.1f}" y1="{Y0}" x2="{sx(10):.1f}" y2="{Y1}" stroke="{INK}" stroke-width="0.8"/>')
o.append(t(sx(10) + 6, sy(n10b) - 8, f'10 campañas: {n10b:.0f} % de las bajas', 12, BLUE, 700, 'start', True))
o.append(t(sx(10) + 6, sy(n10e) + 18, f'con {n10e:.0f} % de los correos', 12, SEC, 600, 'start', True))
LBL = {0: 'Lanzamiento de BillPay', 1: 'Tasa 0 a registrados', 2: 'Referidos a leads', 3: 'Narrativa Tasa 0 a leads', 4: 'Recordatorio de verificación'}
for i, lb in LBL.items():
    px, py = sx(i + 1), sy(em.cb[i])
    o.append(t(px, py - 9, f'{i + 1}', 11, BLUE, 700, 'middle', True))
    o.append(t(X0 + 12, Y0 + 14 + i * 19, f'{i + 1}', 11, BLUE, 700) + t(X0 + 26, Y0 + 14 + i * 19, f'{lb}: {em.eu[i] / 1e3:.0f} mil bajas', 11, INK, 400))
o.append(t(sx(len(em)) - 4, sy(100) + 18, 'Bajas', 12, BLUE, 700, 'end', True))
o.append(t(sx(100) + 4, sy(em.ce[99]) + 18, 'Correos enviados', 12, SEC, 700, 'start', True))
o.append('</svg>')
print('97', round(n10b, 1), round(n10e, 1), n10p, em.eu[:5].tolist())
uniq = pd.read_csv(D + 'e5_cohorte_baja.csv').usuarios_baja.sum()
save(97, dict(kind='grafica',
    titulo=f'Esperar cuesta {m(TOT)} M MXN al mes, y las 10 campañas con más bajas de correo están todas en el plan',
    que='Tasa 0, referidos, lanzamientos y el recordatorio de terminar el registro',
    quien='Product Growth, Marketing y NewProducts (Others)',
    a_quien='Registrados, leads y casi toda la base en BillPay',
    lecturas=[f'Las 10 campañas con más bajas dejan {n10b:.0f} % de ellas con {n10e:.0f} % de los correos; el plan las apaga, modera o rehace.',
              f'{uniq / 1e3:.0f} mil personas se dieron de baja del correo en nueve meses; ya no podemos escribirles por ahí.',
              f'Cada mes sin actuar son {m(TOT)} M MXN: {TOT * 12 / 1e6:.0f} M al año.'],
    causa='Las campañas que más bajas dejan siguen activas porque nadie revisa cada mes respuesta y bajas.',
    sowhat='Corregir esas 10 campañas primero: frenan las bajas y el gasto al mismo tiempo.',
    fuente='Fuente: E1 por campaña de correo, enero a septiembre 2026 (eventos de baja); E5 (personas únicas); acciones del Sheets v4.',
    svg=''.join(o)))
print('ok r2 XII')
