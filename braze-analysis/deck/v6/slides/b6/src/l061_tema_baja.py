"""Lámina 61: tema del correo que llegó el día de la baja (E8, muestra L), nuevos a la izquierda y base vieja a la derecha.
Tipo (promocional, transaccional, cobranza) del catálogo de campañas; tema por el nombre. Una baja cuenta en dos campañas si ese día llegaron dos."""
from tramos import *

def tema(r):
    c = r.clave
    if pd.isna(r.tipo): return 'Sin nombre'
    if r.tipo == 'cobranza': return 'Cobranza'
    if r.tipo != 'promocional o lifecycle': return 'Avisos de pago y de servicio'
    if re.search('BillPay', c): return 'Lanzamiento de BillPay'
    if re.search(r'LeftFunnel|AccountCreation|NIPconCupon|FaltaVeriff|RequestInfo', c): return 'Recordatorio de registro'
    if re.search(r'Tasa0', c, re.I): return 'Tasa 0'
    if re.search(r'Referral|AnotayGana', c): return 'Referidos'
    if gancho_of(c) == 'Descuento, cupón u oferta': return 'Descuentos y cupones'
    return 'Otras promociones'
ORD = ['Lanzamiento de BillPay', 'Recordatorio de registro', 'Tasa 0', 'Referidos', 'Descuentos y cupones', 'Otras promociones', 'Avisos de pago y de servicio', 'Cobranza']
co = {}
for k in (1, 0):
    bd, res, l = datos(k)
    l['tema'] = l.apply(tema, axis=1)
    tot = res.usuarios
    g = l.groupby('tema').usuarios.sum() / tot * 100
    tm = l.groupby(['tema', 'team']).usuarios.sum().reset_index().sort_values('usuarios', ascending=False).drop_duplicates('tema').set_index('tema')
    tm['p'] = 100 * tm.usuarios / l.groupby('tema').usuarios.sum()
    tipo = l.groupby('tipo').usuarios.sum() / tot * 100
    cash = 100 * l[l.producto == 'Cash'].usuarios.sum() / tot
    co[k] = dict(g=g, tm=tm, tipo=tipo, tot=tot, l=l, cash=cash)
    print(k, g.round(1).to_dict(), tipo.round(1).to_dict(), round(cash, 1))

s = SVG('Tema del correo que llegó el día de la baja: nuevos a la izquierda, base vieja a la derecha, en porcentaje de las bajas de cada grupo, con el equipo que más pesa')
CX0, CX1 = 300, 480           # columna central de nombres
L0, R0 = CX0 - 8, CX1 + 8     # inicio de barras
SC = 5.0                      # px por punto porcentual
s.t(L0, 16, f'Nuevos: {co[1]["tot"]/1e3:.0f} mil bajas', 12.5, INK, 'end', 600)
s.t(R0, 16, f'Base vieja: {co[0]["tot"]/1e3:.0f} mil bajas', 12.5, INK, 'start', 600)
s.t(L0, 32, 'primer correo de febrero en adelante', 10.5, SEC, 'end'); s.t(R0, 32, 'ya recibía correo en enero', 10.5, SEC)
s.legend([(BLUE, 'Correo promocional', 'rect'), (M1, 'Aviso o cobranza', 'rect')], 280, 44, size=11)
s.t(390, 76, '% de las bajas de cada grupo y equipo que más pesa', 10.5, SEC, 'middle')
TOP, RH = 96, 36
for i, t_ in enumerate(ORD):
    y = TOP + RH * i
    if i == 6: s.line(0, y - 10, 780, y - 10, M1)
    col = BLUE if i < 6 else M1
    s.t(390, y + 12, t_, 11.5, INK, 'middle', 600)
    for k, side in ((1, -1), (0, 1)):
        v = co[k]['g'].get(t_, 0); w = v * SC
        x0 = L0 - w if side < 0 else R0
        s.rect(x0, y, w, 16, col)
        tm = co[k]['tm'].loc[t_] if t_ in co[k]['tm'].index else None
        lab = f'{v:.0f} %' if v >= 1 else f'{v:.1f} %'
        tx = (L0 - w - 6) if side < 0 else (R0 + w + 6)
        an = 'end' if side < 0 else 'start'
        s.t(tx, y + 12, lab, 11.5, INK, an, 600)
        if tm is not None:
            s.t(tx + (-34 if side < 0 else 34), y + 12, f'{tm.team} {tm.p:.0f} %', 10.5, SEC, an)
y = TOP + RH * 8 + 4
for k, x, an in ((1, L0, 'end'), (0, R0, 'start')):
    tp = co[k]['tipo']
    s.t(x, y, f'Promocional {tp.get("promocional o lifecycle",0):.0f} % · avisos {tp.get("transaccional u operativa",0):.0f} % · cobranza {tp.get("cobranza",0):.0f} %', 11.5, INK, an, 600)
s.t(390, y, 'Total', 11, SEC, 'middle')
s.t(0, 414, 'Una baja cuenta en dos campañas si ese día llegaron dos: los porcentajes suman un poco más de 100. Equipo: el que más bajas tiene en ese tema.', 10.5, SEC)

n, v = co[1], co[0]
fr = n['l'].set_index('clave').loc['KCash Rechazo transaccional FraudRisk']
write(61, dict(
    titulo='Nueve de cada diez bajas llegan el día de un correo promocional; los avisos de pago casi no causan bajas',
    que='Lanzamiento de BillPay, recordatorios de registro, Tasa 0, referidos y descuentos.',
    quien=f'Nuevos: Marketing {100*n["l"][n["l"].team=="Marketing"].usuarios.sum()/n["tot"]:.0f} %, Others (BillPay de NewProducts) {100*n["l"][n["l"].team=="Others"].usuarios.sum()/n["tot"]:.0f} %, Product Growth {100*n["l"][n["l"].team=="Product Growth"].usuarios.sum()/n["tot"]:.0f} %. Base vieja: Marketing {100*v["l"][v["l"].team=="Marketing"].usuarios.sum()/v["tot"]:.0f} %, Product Growth {100*v["l"][v["l"].team=="Product Growth"].usuarios.sum()/v["tot"]:.0f} %, Others {100*v["l"][v["l"].team=="Others"].usuarios.sum()/v["tot"]:.0f} %.',
    a_quien=f'{(n["tot"]+v["tot"])/1e3:.0f} mil personas que se dieron de baja del email entre enero y septiembre (91 % de todas las bajas).',
    lecturas=[
        f'{n["tipo"]["promocional o lifecycle"]:.0f} % de las bajas de nuevos y {v["tipo"]["promocional o lifecycle"]:.0f} % de la base vieja caen el día de un correo promocional; los avisos explican {v["tipo"]["transaccional u operativa"]:.0f} a {n["tipo"]["transaccional u operativa"]:.0f} % y la cobranza {v["tipo"]["cobranza"]:.0f} a {n["tipo"]["cobranza"]:.0f} %.',
        f'Al nuevo lo pierden BillPay ({n["g"]["Lanzamiento de BillPay"]:.0f} %) y el recordatorio de registro ({n["g"]["Recordatorio de registro"]:.0f} %); a la base vieja, la Tasa 0 ({v["g"]["Tasa 0"]:.0f} %) y los referidos ({v["g"]["Referidos"]:.0f} %). Cash pesa más: {n["cash"]:.0f} % y {v["cash"]:.0f} % de las bajas llegan con un correo de KCash.',
        f'Un aviso sí aparece: el rechazo por riesgo de fraude de KCash, {fr.usuarios/1e3:.1f} mil bajas de nuevos al día {fr.dias_mediana}.',
    ],
    causa='Las promociones salen a listas completas y se repiten sin límite por persona; los avisos solo llegan a quien hizo algo y casi nadie se da de baja por ellos.',
    sowhat='La baja se decide en las promociones: ahí van el límite de correos por persona y la salida de la campaña si no abre en 90 días.',
    fuente='Fuente: Braze, campaña que llegó el día de la baja del email por persona (E8), enero a septiembre 2026. Tipo de correo según el catálogo de campañas; tema por el nombre. Campañas con 500 o más bajas.',
    svg=s.svg()))
