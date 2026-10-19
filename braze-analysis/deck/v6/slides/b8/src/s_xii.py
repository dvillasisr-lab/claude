# Sección XII (caso de negocio): láminas 91 y 93 a 97 (la 92 es la muestra aprobada s3.json).
import math, pandas as pd, numpy as np
from kit import *
import datos
D = datos.ROOT + 'data/'
c = datos.load_c(); S3 = datos.load_s3(); R = S3['R']
DUP = datos.dup_mes()
SEP = R['sep']; TOT = R['total']; SEG = R['seguro']; MED = R['medir']
MINIMO = 'Mínimo aceptable por canal: 3 clics por cada mil correos, 7.5 aperturas por cada mil push, 6 de cada 10 WhatsApp leídos o 1 de cada 10 in-app con clic.'
COSTOS = 'WhatsApp a 1.00 MXN por entregado, email a 0.05 por enviado, push e in-app 0'

# ------------------------------------------------------------------ 91. Divisor
save(91, dict(kind='divisor', acto='Acto 3 · Cómo lo resolvemos',
    titulo=f'Corregirlo vale hasta {m(TOT, 1)} M MXN al mes: limpiar en 30 días, configurar en 60 y medir en 90',
    subtitulo=f'Con WhatsApp cobrado por entregado y septiembre como mes base, {m(SEG)} M MXN al mes se quitan ya sin perder ventas. '
              f'Los otros {m(MED)} M son mensajes para recuperar clientes: se quitan solo si no los recuperan, y primero se prueba dejando a un grupo sin mensajes.'))

# ------------------------------------------------------------------ 93. Matriz certeza por tiempo
B = [dict(k='desp', col=0, row=0, lab='Lo que no debería salir', v=c.b_desp.sum() + DUP, mm=c.bm_desp.sum(), ej='Bloqueados, duplicados y pruebas'),
     dict(k='cortar', col=1, row=0, lab='Quitar correo o WhatsApp', v=c.b_cortar.sum(), mm=c.bm_cortar.sum(), ej='Tasa 0 y Installments a registrados'),
     dict(k='pref', col=2, row=0, lab='Canal preferido', v=c.b_pref.sum(), mm=c.bm_pref.sum(), ej='Solo el canal al que responde'),
     dict(k='medir', col=3, row=1, lab='Recuperar ex clientes', v=c.b_medir.sum(), mm=c.bm_medir.sum(), ej='Ex clientes KPay por WhatsApp')]
for b in B:
    by = c.groupby('equipo')['b_' + b['k']].sum()
    if b['k'] == 'desp': by['Product Growth'] += DUP
    b['eq'] = by.idxmax(); b['eqsh'] = by.max() / by.sum()
print('93', [(b['k'], round(b['v'] / 1e6, 3), round(b['mm'] / 1e6, 2), b['eq'], round(b['eqsh'], 2)) for b in B])
o = svg_open(f'Ahorro por certeza y por plazo: {m(SEG)} M MXN al mes se quitan ya en 1 a 60 días; {m(MED)} M se deciden midiendo con grupo de control a 90 días.')
CX = [150, 307, 464, 621]; CW = 157
heads = ['Semana 1', 'En 30 días', 'En 60 días', 'A 90 días, medido']
for i, h_ in enumerate(heads):
    o.append(t(CX[i] + CW / 2, 18, h_, 12.5, INK, 600, 'middle'))
o.append(f'<line x1="150" y1="28" x2="780" y2="28" stroke="{INK}" stroke-width="1.2"/>')
RY = [(34, 222), (230, 418)]
rowlab = [('Se quita ya', 'sin perder ventas', BLUE), ('Se quita solo si', 'no recupera clientes', GREEN)]
for r, (y0, y1) in enumerate(RY):
    o.append(f'<rect x="0" y="{y0}" width="780" height="{y1 - y0}" fill="{"#F4F6F9" if r == 0 else "#FFFFFF"}"/>')
    o.append(t(0, y0 + 22, rowlab[r][0], 13, rowlab[r][2], 700) + t(0, y0 + 38, rowlab[r][1], 13, rowlab[r][2], 700))
    tot_r = SEG if r == 0 else MED
    o.append(t(0, y0 + 62, f'{m(tot_r)} M MXN', 13, INK, 600) + t(0, y0 + 77, 'al mes', 12, TXT))
for x in CX[1:]:
    o.append(f'<line x1="{x}" y1="28" x2="{x}" y2="418" stroke="{GRID}" stroke-width="1"/>')
o.append(f'<line x1="150" y1="226" x2="780" y2="226" stroke="{GRID}" stroke-width="1"/>')
SMAX = 112
for b in B:
    s = SMAX * math.sqrt(b['v'] / max(x['v'] for x in B))
    x0 = CX[b['col']] + 12; y0 = RY[b['row']][0] + 10
    fill, stroke = (BLUE, None) if b['row'] == 0 else (GREEN_L, GREEN)
    if stroke:
        o.append(f'<rect x="{x0 + .75:.1f}" y="{y0 + .75:.1f}" width="{s - 1.5:.1f}" height="{s - 1.5:.1f}" rx="3" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
    else:
        o.append(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{s:.1f}" height="{s:.1f}" rx="3" fill="{fill}"/>')
    ty = y0 + SMAX + 20
    o.append(t(x0, ty, f'{m(b["v"])} M MXN al mes', 13, INK, 700))
    o.append(t(x0, ty + 16, f'{m(b["mm"], 1)} M mensajes al mes', 12, TXT))
    o.append(t(x0, ty + 32, f'{b["eq"]} {b["eqsh"] * 100:.0f} %', 12, TXT))
    o.append(t(x0, ty + 48, b['lab'], 11.5, SEC))
o.append('</svg>')
save(93, dict(kind='grafica',
    titulo='Casi dos tercios del ahorro se quita ya sin perder ventas; el resto es recuperar clientes y se decide midiendo',
    que='Promoción de activación (Tasa 0, cross sell, recordatorios a leads), ofertas para recuperar ex clientes y cualquier promoción a personas bloqueadas o de prueba.',
    quien=f'Product Growth concentra el corte en 30 días ({m(c[c.equipo == "Product Growth"].b_cortar.sum())} de {m(B[1]["v"])} M MXN al mes) y la recuperación ({m(c[c.equipo == "Product Growth"].b_medir.sum())} de {m(B[3]["v"])} M); Marketing, el canal preferido.',
    a_quien='Leads y registrados que nunca tomaron crédito, por un lado; ex clientes con historial (churn, dormants, inactivos), que a veces solo usan la web y no tienen app, por el otro.',
    lecturas=[f'Semana 1: {m(B[0]["v"])} M MXN al mes en mensajes que no deberían salir: personas bloqueadas, duplicados del mismo día y pruebas internas que llegaron a clientes.',
              f'En 30 días: {m(B[1]["v"])} M. Campañas a leads y registrados que no responden lo mínimo aceptable: se quita solo el correo o el WhatsApp y se deja push o in-app, con 10 % sin mensajes.',
              f'Recuperación: {m(B[3]["v"])} M. No se apaga: pasa al canal más barato que usan, 3 mensajes en 30 días, presupuesto con límite y 10 % sin mensajes durante 8 semanas.'],
    causa='Hoy se trata igual a quien nunca fue cliente que a quien ya compró: los dos reciben WhatsApp y correo sin saber si responden ni si el mensaje los trae de vuelta.',
    sowhat=f'Aprobar hoy {m(SEG)} M MXN al mes que no tocan la recuperación de clientes; los {m(MED)} M restantes se deciden con datos en dos meses.',
    fuente=f'Fuente: E1 por campaña, canal y mes (septiembre 2026), acciones del Sheets v4, E9b, E7a y E6b; {COSTOS}. Área del cuadro proporcional a MXN al mes; % = equipo que más aporta. {MINIMO}',
    svg=''.join(o)))

# ------------------------------------------------------------------ 94. Equipo por canal
EQS = ['Product Growth', 'Marketing', 'Sales', 'Others']
CAN = [('email', 'Correo'), ('whatsapp', 'WhatsApp')]
c['seg'] = c.b_desp + c.b_cortar + c.b_pref
NOM = {'B0211': 'Tasa 0 a registrados (B0211)', 'B0333': 'Ex clientes KPay, 12 meses (B0333)', 'B0326': 'Referidos a dormants (B0326)',
       'B0171': 'Rescate Tasa 0 a leads (B0171)', 'B0335': 'Promociones de comercios (B0335)', 'B0615': 'Comercio del día (B0615)',
       'S0004': 'Recomendaciones Shopping (S0004)', 'T2778': 'Aviso a adultos mayores (T2778)'}
o = svg_open('Ahorro al mes por equipo y canal, separado en lo que se quita ya y lo que se decide midiendo, con la campaña más grande de cada barra.')
o.append(f'<rect x="0" y="6" width="12" height="12" rx="2" fill="{BLUE}"/>' + t(18, 16.5, 'Se quita ya sin perder ventas', 12, INK, 600))
o.append(f'<rect x="230.75" y="6.75" width="10.5" height="10.5" rx="2" fill="{GREEN_L}" stroke="{GREEN}" stroke-width="1.5"/>' + t(248, 16.5, 'Se quita solo si no recupera clientes', 12, INK, 600))
o.append(t(780, 44, 'Campaña con más ahorro, M MXN al mes', 11, SEC, 600, 'end'))
X0, X1, VM = 196, 520, 1.0e6; sx = lambda v: X0 + (X1 - X0) * v / VM
AX = 400
for v in (0, .25, .5, .75, 1):
    o.append(f'<line x1="{sx(v * 1e6):.1f}" y1="52" x2="{sx(v * 1e6):.1f}" y2="{AX}" stroke="{GRID}" stroke-width="1"/>')
    o.append(t(sx(v * 1e6), AX + 14, f'{v:.2f} M'.replace('0.00 M', '0').replace('1.00 M', '1 M'), 11, SEC, 400, 'middle'))
o.append(t(780, AX + 14, 'MXN al mes', 11, SEC, 400, 'end'))
y = 60; rows94 = []
for eq in EQS:
    tot_eq = c[c.equipo == eq].tot.sum()
    o.append(t(0, y + 14, eq, 13, INK, 600) + t(0, y + 30, f'{m(tot_eq)} M MXN', 12, TXT))
    for k_, (cn, cl) in enumerate(CAN):
        g = c[(c.equipo == eq) & (c.canal == cn)]
        sv, mv = g.seg.sum(), g.b_medir.sum()
        yy = y + k_ * 26
        o.append(t(X0 - 10, yy + 12.5, cl, 12, TXT, 400, 'end'))
        if sv > 0: o.append(f'<rect x="{X0}" y="{yy}" width="{max(sx(sv) - X0 - 1, 1):.1f}" height="17" rx="2" fill="{BLUE}"/>')
        if mv > 0: o.append(f'<rect x="{sx(sv) + .75:.1f}" y="{yy + .75}" width="{max(sx(sv + mv) - sx(sv) - 1.5, 1):.1f}" height="15.5" rx="2" fill="{GREEN_L}" stroke="{GREEN}" stroke-width="1.5"/>')
        o.append(t(sx(sv + mv) + 6, yy + 12.5, f'{m(sv + mv)}', 12, INK, 600))
        top = g.sort_values('tot', ascending=False).iloc[0]
        tk = datos.ticket(top.fam)
        if g.tot.sum() > 5000:
            o.append(t(780, yy + 12.5, f'{NOM.get(tk, tk)} {top.tot / 1e6:.2f}', 11.5, TXT, 400, 'end'))
        rows94.append((eq, cn, round(sv / 1e6, 3), round(mv / 1e6, 3), top.fam, round(top.tot / 1e6, 3)))
    y += 84
o.append('</svg>')
print('94', rows94)
pg = c[c.equipo == 'Product Growth']; mk = c[c.equipo == 'Marketing']
save(94, dict(kind='grafica',
    titulo='Dos de cada tres pesos del ahorro están en Product Growth: Tasa 0 por correo a registrados y WhatsApp a clientes que dejaron de comprar',
    que='Product Growth: Tasa 0 de Cash a registrados, Installments a quien nunca activó, ofertas a ex clientes de KPay, cross sell. Marketing: referidos, recordatorio de verificación, rescate Tasa 0 a leads.',
    quien=f'Product Growth {m(pg.tot.sum())} M MXN al mes ({pg.tot.sum() / TOT * 100:.0f} %), Marketing {m(mk.tot.sum())} M ({mk.tot.sum() / TOT * 100:.0f} %), Sales {m(c[c.equipo == "Sales"].tot.sum())} M y Others {m(c[c.equipo == "Others"].tot.sum())} M.',
    a_quien='Product Growth: registrados sin crédito y ex clientes de KPay. Marketing: leads y dormants. Sales: clientes recurrentes de KPay.',
    lecturas=[f'Product Growth: {m(pg[pg.canal == "whatsapp"].tot.sum())} M en WhatsApp y {m(pg[pg.canal == "email"].tot.sum())} M en correo. Se quita ya {m(pg.seg.sum())} M y se mide {m(pg.b_medir.sum())} M (ex clientes de KPay por WhatsApp).',
              f'Marketing: casi todo es canal preferido ({m(mk.b_pref.sum())} M) y recuperación o leads sin respuesta en 90 días ({m(mk.b_medir.sum())} M). Su problema es a quién y por qué canal, no qué manda.',
              'Sales: correo a recurrentes de KPay con 0.6 a 2.3 clics por cada mil; se rehace para quien hizo clic en 90 días. Sus WhatsApp sí se leen. Cobranza no se toca.'],
    causa='Product Growth escribe en volumen a quien nunca respondió y a ex clientes por el canal que se cobra (WhatsApp a 1 MXN), sin límite de mensajes ni grupo sin mensajes.',
    sowhat='Con dos equipos y diez campañas se captura la mayor parte del ahorro: empezar por Tasa 0 (B0211) e Installments (B0223) a registrados, y por los ex clientes de KPay (B0333 y B0332).',
    fuente=f'Fuente: E1 por campaña, canal y mes (septiembre 2026), acciones del Sheets v4, E9b, E7a; {COSTOS}. Sin duplicados del mismo día ({DUP / 1e6:.2f} M, Product Growth). Collections solo aporta pruebas internas ({m(c[c.equipo == "Collections"].tot.sum())} M).',
    svg=''.join(o)))

# ------------------------------------------------------------------ 95. Personas que nunca respondieron
e7 = pd.read_csv(D + 'e7b_patron_respuesta.csv')
anyr = (e7.resp_email + e7.resp_push + e7.resp_wa + e7.resp_inapp) > 0
N, Y = e7[~anyr].sum(), e7[anyr].sum()
CH = [('msgs_email', 'Correo', BLUE), ('msgs_push', 'Push', MARK), ('msgs_wa', 'WhatsApp', MARK2), ('msgs_inapp', 'In-app', GRID)]
tm = lambda r: sum(r[k_] for k_, _, _ in CH)
cost_n = N.msgs_email * 0.05 + N.msgs_wa_entregados * 1.0
print('95', N.usuarios, e7.usuarios.sum(), tm(N), tm(Y), cost_n, N.usuarios_con_conversion / N.usuarios, N.usuarios_con_baja_email, N.msgs_wa_entregados / N.msgs_wa)
o = svg_open(f'{m(N.usuarios, 1)} M de {m(e7.usuarios.sum(), 1)} M personas nunca respondieron; recibieron {m(tm(N), 1)} M mensajes, {N.msgs_email / tm(N) * 100:.0f} % por correo.')
o.append(t(0, 56, f'{m(N.usuarios, 1)} M', 56, INK, 700))
o.append(t(0, 82, f'de {m(e7.usuarios.sum(), 1)} M personas que recibieron algo', 13, TXT))
o.append(t(0, 98, 'nunca respondieron en nueve meses', 13, TXT))
stats = [(f'{cost_n / 1e6:.1f} M MXN', 'gastados en mensajes', 'a estas personas'), (f'{N.usuarios_con_conversion / N.usuarios * 100:.2f} %', 'tomó un crédito', 'en nueve meses'),
         (f'{N.usuarios_con_baja_email / 1e3:.0f} mil', 'se dieron de baja', 'del correo')]
for i, (a, b_, c_) in enumerate(stats):
    x = 330 + i * 152
    o.append(f'<line x1="{x - 14}" y1="30" x2="{x - 14}" y2="100" stroke="{GRID}" stroke-width="1"/>')
    o.append(t(x, 56, a, 22, INK, 700) + t(x, 76, b_, 12, TXT) + t(x, 91, c_, 12, TXT))
o.append(t(0, 150, 'Con qué canal les escribimos: mensajes por canal, de cada 100', 13, INK, 600))
x = 0
for k_, lab, col in CH:
    o.append(f'<rect x="{x}" y="164" width="12" height="12" rx="2" fill="{col}"/>' + t(x + 18, 174.5, lab, 12, TXT))
    x += 30 + len(lab) * 7.5
X0, X1 = 196, 780
grp = [('Nunca respondieron', f'{m(N.usuarios, 1)} M personas, {tm(N) / N.usuarios:.0f} mensajes c/u', N),
       ('Respondieron alguna vez', f'{m(Y.usuarios, 1)} M personas, {tm(Y) / Y.usuarios:.0f} mensajes c/u', Y)]
for i, (a, b_, r) in enumerate(grp):
    y = 200 + i * 92
    o.append(t(X0 - 12, y + 22, a, 13, INK, 600, 'end') + t(X0 - 12, y + 38, b_, 11.5, SEC, 400, 'end'))
    o.append(t(X0, y - 4 + 0, f'{m(tm(r), 1)} M mensajes', 11.5, SEC))
    x = X0; T_ = tm(r)
    for k_, lab, col in CH:
        w = (X1 - X0) * r[k_] / T_
        o.append(f'<rect x="{x:.1f}" y="{y + 6}" width="{max(w - 2, .5):.1f}" height="40" fill="{col}"/>')
        if w > 46:
            fc = '#FFFFFF' if col in (BLUE,) else INK
            o.append(t(x + 7, y + 25, f'{r[k_] / T_ * 100:.0f}', 15, fc, 700) + t(x + 7, y + 40, f'{m(r[k_], 1)} M', 11, fc))
        x += w
o.append(t(0, 395, f'Solo {N.msgs_wa_entregados / N.msgs_wa * 100:.0f} % de los WhatsApp que se les mandan llega a su teléfono, contra {Y.msgs_wa_entregados / Y.msgs_wa * 100:.0f} % en quien sí responde.', 12, TXT))
o.append('</svg>')
save(95, dict(kind='grafica',
    titulo=f'Los {m(N.usuarios, 1)} M de personas que nunca respondieron reciben sobre todo correo, y aun así cuentan para lo que Braze cobra',
    que=f'Sobre todo promoción por correo: {m(N.msgs_email, 1)} M correos, dos de cada tres mensajes que reciben. Además {m(N.msgs_push, 1)} M push y {m(N.msgs_wa, 1)} M WhatsApp enviados ({m(N.msgs_wa_entregados, 1)} M entregados).',
    quien='Sobre todo Marketing y Product Growth, que escriben a leads y registrados. El cruce exacto por equipo no existe en los datos.',
    a_quien='Tres de cada cuatro personas que recibieron algo. Con más volumen y menos respuesta: Leads (201 M mensajes), New (2.3 clics por cada mil correos), Todos (2.0) y Anónimos.',
    lecturas=['Responder es hacer clic en un correo, abrir un push, leer un WhatsApp o hacer clic en un in-app. Estas personas no lo hicieron ni una vez en nueve meses.',
              f'Les escribimos {tm(N) / N.usuarios:.0f} mensajes a cada una; {N.msgs_email / tm(N) * 100:.0f} de cada 100 por correo. Quien sí responde recibe más push e in-app.',
              'Braze cobra un costo fijo por usuarios activos y datos: cada persona a la que le escribimos cuenta, aunque nunca responda. El monto depende del contrato (supuesto X).'],
    causa='Las listas se arman por etapa (lead, registrado, todos) y no por si la persona responde; nadie las limpia de quien lleva meses sin reaccionar.',
    sowhat=f'Escribirle a quien nunca responde cuesta mensajes, bajas y factura fija de Braze. Su ahorro ({m(c.sin_respuesta_90d.sum())} M MXN al mes) ya está en la lámina 92 como recuperación a medir.',
    fuente=f'Fuente: Braze, personas por canal al que responden (E7b) y segmentos (E11), enero a septiembre 2026; {COSTOS}. E16 da otra cifra con otra definición; se usa E7b. Costo fijo de Braze: 7,020 USD al mes y 32,474 créditos sin explicar, queda como X.',
    svg=''.join(o)))

# ------------------------------------------------------------------ 96. KCash contra KPay
pr = c.tipo == 'promocional o lifecycle'
psep = c[pr].groupby('p2').c_sep.sum()
BK = [('b_desp', 'No debería salir', 'semana 1'), ('b_cortar', 'Cortar en 30 días', 'correo o WhatsApp'),
      ('b_pref', 'Canal preferido', '60 días'), ('b_medir', 'Recuperar clientes', 'se mide')]
PRODS = ['KCash', 'KPay']
tab = {(p, b, cn): c[(c.p2 == p) & (c.canal == cn)][b].sum() for p in PRODS for b, _, _ in BK for cn in ('email', 'whatsapp')}
tp = {p: c[c.p2 == p].tot.sum() for p in PRODS}
print('96', {k_: round(v / 1e6, 3) for k_, v in tab.items()}, {p: round(tp[p] / 1e6, 3) for p in PRODS}, (psep / 1e6).round(3).to_dict(), (c.groupby('p2').bloqueados.sum() / 1e6).round(3).to_dict())
o = svg_open('Ahorro al mes de KCash y KPay por tipo de acción y canal.')
o.append(f'<rect x="0" y="6" width="12" height="12" rx="2" fill="{BLUE}"/>' + t(18, 16.5, 'Correo', 12, TXT))
o.append(f'<rect x="90" y="6" width="12" height="12" rx="2" fill="{BLUE_L}"/>' + t(108, 16.5, 'WhatsApp', 12, TXT))
o.append(t(780, 16.5, 'MXN al mes', 11.5, SEC, 400, 'end'))
LX = 150; PW = 300; GAP = 30; VM = 0.7e6
for j, p in enumerate(PRODS):
    x0 = LX + j * (PW + GAP); sx = lambda v, x0=x0: x0 + PW * v / VM
    o.append(t(x0, 52, f'{p}: {m(tp[p])} M MXN al mes', 14, INK, 700))
    o.append(t(x0, 70, f'{tp[p] / psep[p] * 100:.0f} % de su promoción de septiembre', 11.5, SEC))
    for v in (0, .2, .4, .6):
        o.append(f'<line x1="{sx(v * 1e6):.1f}" y1="84" x2="{sx(v * 1e6):.1f}" y2="388" stroke="{GRID}" stroke-width="1"/>')
        o.append(t(sx(v * 1e6), 404, f'{v:.1f} M' if v else '0', 11, SEC, 400, 'middle'))
    for i, (b, lab, when) in enumerate(BK):
        y = 104 + i * 74 + (14 if i == 3 else 0)
        ve, vw = tab[(p, b, 'email')], tab[(p, b, 'whatsapp')]
        o.append(f'<rect x="{x0}" y="{y}" width="{max(sx(ve) - x0 - 1, .5):.1f}" height="26" rx="2" fill="{BLUE}"/>')
        o.append(f'<rect x="{sx(ve) + 1:.1f}" y="{y}" width="{max(sx(ve + vw) - sx(ve) - 1, .5):.1f}" height="26" rx="2" fill="{BLUE_L}"/>')
        big = (p == 'KCash' and b == 'b_cortar') or (p == 'KPay' and b == 'b_medir')
        o.append(t(sx(ve + vw) + 6, y + 18, f'{m(ve + vw)}', 13 if big else 12, INK, 700 if big else 400))
for i, (b, lab, when) in enumerate(BK):
    y = 104 + i * 74 + (14 if i == 3 else 0)
    o.append(t(0, y + 11, lab, 12.5, INK, 600) + t(0, y + 27, when, 11.5, GREEN if b == 'b_medir' else SEC, 600 if b == 'b_medir' else 400))
o.append(f'<line x1="0" y1="{104 + 3 * 74 - 6}" x2="780" y2="{104 + 3 * 74 - 6}" stroke="{MARK}" stroke-width="1"/>')
o.append('</svg>')
blq = c.groupby('p2').bloqueados.sum()
kc_cut = tab[('KCash', 'b_cortar', 'email')] + tab[('KCash', 'b_cortar', 'whatsapp')]
kp_med = tab[('KPay', 'b_medir', 'email')] + tab[('KPay', 'b_medir', 'whatsapp')]
save(96, dict(kind='grafica',
    titulo='KCash y KPay ahorran casi lo mismo por razones distintas: en KCash se corta, en KPay hay que medir si recupera clientes',
    que='KCash: Tasa 0 e Installments a registrados que nunca tomaron Cash, rescate a leads. KPay: ofertas a clientes que dejaron de comprar, promociones de comercios y cross sell a Cash.',
    quien='Product Growth en los dos; Marketing pesa más en KCash y Sales solo en KPay.',
    a_quien='KCash: leads y registrados sin crédito. KPay: ex clientes sin compra en 12 o en 6 meses, y clientes con la tarjeta congelada.',
    lecturas=[f'KCash: {m(kc_cut)} M de su ahorro es quitar en 30 días correos y WhatsApp a registrados que no responden (Tasa 0 B0211 e Installments B0223). Poco riesgo.',
              f'KPay: {m(kp_med)} M es recuperación por WhatsApp a ex clientes (B0333 y B0332). No se apaga: se prueba dejando a un grupo sin mensajes.',
              f'KPay manda más promoción a bloqueados: {m(blq["KPay"])} M contra {m(blq["KCash"])} M en KCash. Son ofertas a personas con la tarjeta congelada, que no la pueden usar.'],
    causa='Cada producto arma sus listas por su lado: KCash insiste a registrados que nunca activaron y KPay escribe por WhatsApp a ex clientes, sin medir si regresan.',
    sowhat='Con KCash la conversación es apagar lo que no responde; con KPay, probar con un grupo sin mensajes si la recuperación trae clientes antes de cortar.',
    fuente=f'Fuente: E1 por campaña, canal y mes (septiembre 2026), acciones del Sheets v4, E9b, E7a; {COSTOS}. Producto por el segundo campo del nombre; otros productos suman {m(c[c.p2 == "Otro"].tot.sum())} M. Sin duplicados del mismo día ({DUP / 1e6:.2f} M).',
    svg=''.join(o)))

# ------------------------------------------------------------------ 97. Lo que cuesta esperar
g1 = datos.load_g1()
x = g1[g1.canal == 'email'].merge(c[['fam', 'canal', 'accion']], on=['fam', 'canal'], how='left')
PL = {'Apagar': 'apaga', 'Bajar frecuencia': 'baja frecuencia', 'Rehacer o re-segmentar': 'rehace'}
x['grp'] = x.accion.map(lambda a: PL.get(a, 'resto'))
bt = pd.crosstab(x.mes, x.grp, values=x.eu, aggfunc='sum').fillna(0)
bt['plan'] = bt[['apaga', 'baja frecuencia', 'rehace']].sum(axis=1)
sep_sh = bt.loc['2026-09', 'plan'] / bt.loc['2026-09'][['plan', 'resto']].sum()
sh3 = {k_: bt.loc['2026-09', k_] / bt.loc['2026-09'][['plan', 'resto']].sum() for k_ in PL.values()}
e5 = pd.read_csv(D + 'e5_cohorte_baja.csv'); uniq = e5.usuarios_baja.sum()
e4 = pd.read_csv(D + 'e4a_serie_semana_mes_canal.csv'); sep_u = e4[(e4.grano == 'mes') & (e4.canal == 'email') & (e4.periodo == '2026-09-01')].bajas_email_usuarios.sum()
S1 = B[0]['v'] + B[1]['v']; S2 = S1 + B[2]['v']
cum = {'sin': [], 'seg': [], 'tod': []}; a = b_ = d_ = 0
for k_ in range(12):
    a += SEP; b_ += SEP - (S1 if k_ == 0 else S2); d_ += SEP - (S1 if k_ == 0 else S2 if k_ == 1 else TOT)
    cum['sin'].append(a); cum['seg'].append(b_); cum['tod'].append(d_)
print('97', (bt / 1e3).round(1).to_dict('index'), round(sep_sh, 3), {k_: round(v, 3) for k_, v in sh3.items()}, uniq, sep_u, [round(cum[k_][-1] / 1e6, 1) for k_ in cum])
o = svg_open('Izquierda: gasto acumulado en 12 meses desde octubre, sin plan y con plan. Derecha: bajas de correo por mes, separadas en campañas que el plan corrige y el resto.')
# panel izquierdo
o.append(t(0, 16, 'Gasto acumulado en mensajes desde octubre', 13, INK, 600))
o.append(t(0, 32, 'millones de MXN, al ritmo de septiembre', 11.5, SEC))
LX0, LX1, LY0, LY1, VM = 34, 310, 52, 372, 55e6
sx = lambda i: LX0 + (LX1 - LX0) * i / 11; sy = lambda v: LY1 - (LY1 - LY0) * v / VM
for v in range(0, 51, 10):
    o.append(f'<line x1="{LX0}" y1="{sy(v * 1e6):.1f}" x2="{LX1}" y2="{sy(v * 1e6):.1f}" stroke="{GRID}" stroke-width="1"/>')
    o.append(t(LX0 - 6, sy(v * 1e6) + 4, f'{v}', 11, SEC, 400, 'end'))
MES = ['oct', 'nov', 'dic', 'ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep']
for i in (0, 3, 6, 9, 11):
    o.append(t(sx(i), LY1 + 16, MES[i], 11, SEC, 400, 'middle'))
o.append(t((LX0 + LX1) / 2, LY1 + 32, '2026 a 2027', 11, SEC, 400, 'middle'))
for k_, col, wd, lab in (('sin', MARK, 2, 'Sin plan'), ('seg', BLUE_L, 2.5, 'Solo lo que se quita ya'), ('tod', BLUE, 2.5, 'Con todo el plan')):
    pts = ' '.join(f'{sx(i):.1f},{sy(v):.1f}' for i, v in enumerate(cum[k_]))
    o.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{wd}"/>')
ends = [('sin', 'Sin plan', MARK), ('seg', 'Solo lo seguro', BLUE_L), ('tod', 'Todo el plan', BLUE)]
for k_, lab, col in ends:
    v = cum[k_][-1]; o.append(f'<circle cx="{sx(11):.1f}" cy="{sy(v):.1f}" r="3.5" fill="{col}"/>')
for k_, lab, col, w_ in (('sin', 'Sin plan', SEC, 400), ('seg', 'Solo lo', BLUE_L, 600), ('tod', 'Todo el', BLUE, 600)):
    yv = sy(cum[k_][-1])
    l2 = {'sin': '', 'seg': 'seguro', 'tod': 'plan'}[k_]
    o.append(t(sx(11) + 8, yv - 2, lab + (' ' + f'{cum[k_][-1] / 1e6:.1f}' if not l2 else ''), 11.5, INK if k_ == 'sin' else col, w_))
    if l2: o.append(t(sx(11) + 8, yv + 12, f'{l2} {cum[k_][-1] / 1e6:.1f}', 11.5, col, w_))
# panel derecho
RX0, RX1, RY0, RY1, VMB = 430, 780, 52, 372, 180e3
o.append(t(400, 16, 'Bajas de correo por mes, 2026', 13, INK, 600))
o.append(t(400, 32, 'miles de bajas registradas', 11.5, SEC))
ry = lambda v: RY1 - (RY1 - RY0) * v / VMB
for v in range(0, 181, 40):
    o.append(f'<line x1="{RX0}" y1="{ry(v * 1e3):.1f}" x2="{RX1}" y2="{ry(v * 1e3):.1f}" stroke="{GRID}" stroke-width="1"/>')
    o.append(t(RX0 - 6, ry(v * 1e3) + 4, f'{v}', 11, SEC, 400, 'end'))
MS = list(bt.index); bw = (RX1 - RX0) / len(MS)
mn = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep']
for i, mm in enumerate(MS):
    xb = RX0 + i * bw + 5; p_, r_ = bt.loc[mm, 'plan'], bt.loc[mm, 'resto']
    o.append(f'<rect x="{xb:.1f}" y="{ry(p_):.1f}" width="{bw - 10:.1f}" height="{RY1 - ry(p_):.1f}" fill="{BLUE}"/>')
    o.append(f'<rect x="{xb:.1f}" y="{ry(p_ + r_):.1f}" width="{bw - 10:.1f}" height="{ry(p_) - ry(p_ + r_) - 2:.1f}" fill="{MARK2}"/>')
    o.append(t(xb + (bw - 10) / 2, RY1 + 16, mn[i], 11, SEC, 400, 'middle'))
o.append(f'<rect x="{RX0}" y="{RY1 + 26}" width="11" height="11" rx="2" fill="{BLUE}"/>' + t(RX0 + 16, RY1 + 36, 'Campañas que el plan corrige', 11.5, TXT))
o.append(f'<rect x="{RX0 + 196}" y="{RY1 + 26}" width="11" height="11" rx="2" fill="{MARK2}"/>' + t(RX0 + 212, RY1 + 36, 'Resto', 11.5, TXT))
lp = bt.loc['2026-09', 'plan']
o.append(t(RX1 - bw / 2, ry(bt.loc['2026-09'][['plan', 'resto']].sum()) - 8, f'{sep_sh * 100:.0f} %', 12, BLUE, 700, 'middle', True))
o.append('</svg>')
save(97, dict(kind='grafica',
    titulo=f'Esperar cuesta {m(TOT, 1)} M MXN cada mes ({TOT * 12 / 1e6:.0f} M al año), y en septiembre {sep_u / 1e3:.1f} mil personas más dejaron de recibir nuestros correos',
    que='Las campañas que el plan apaga, rehace o a las que les baja la frecuencia: Tasa 0, referidos, lanzamientos y el recordatorio de terminar el registro.',
    quien='Product Growth y Marketing, sobre todo.',
    a_quien='Registrados, leads y dormants por correo. Ejemplos: recordatorio de verificación B0000 (3.9 bajas por cada mil correos) y referidos a leads B0326 (6.7).',
    lecturas=[f'Sin plan, al ritmo de septiembre, gastamos {cum["sin"][-1] / 1e6:.1f} M MXN en 12 meses. Con el plan desde octubre, {(cum["sin"][-1] - cum["seg"][-1]) / 1e6:.1f} M menos seguros y hasta {(cum["sin"][-1] - cum["tod"][-1]) / 1e6:.1f} M si la recuperación no recupera.',
              'Quien se da de baja ya no recibe correos de Kueski. Volver a escribirle por WhatsApp cuesta 20 veces más (1 MXN contra 0.05) o no hay forma.',
              f'{uniq / 1e3:.0f} mil personas se dieron de baja en nueve meses. En septiembre, {sep_sh * 100:.0f} % de las bajas salió de campañas que el plan apaga ({sh3["apaga"] * 100:.0f} %), modera ({sh3["baja frecuencia"] * 100:.0f} %) o rehace ({sh3["rehace"] * 100:.0f} %).'],
    causa='Las campañas que más bajas generan siguen activas porque nadie revisa cada mes cuánto responden ni cuántas personas se dan de baja por ellas.',
    sowhat='Cada mes sin actuar son 2.3 M MXN y miles de personas que ya no podremos contactar por correo. Cuántas bajas se evitan lo dirá el grupo sin mensajes; por eso no se les pone precio.',
    fuente=f'Fuente: E1 por campaña, canal y mes; E5 (personas con baja, únicas) y E4a (personas con baja en septiembre); acciones del Sheets v4; {COSTOS}. Con plan: mes 1 {m(S1)} M, mes 2 {m(S2)} M y desde el mes 3 {m(TOT)} M de ahorro. Bajas = eventos de baja de email por campaña; el guion decía 77 %.',
    svg=''.join(o)))
print('ok XII')
