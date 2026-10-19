"""Lámina 21: Mekko equipo x tema. Alto de la franja = mensajes del equipo; ancho del bloque = parte del tema;
parte azul = mensajes a gente sin acción reciente; etiqueta = gasto del tema en MXN. Campañas con 50 mil o más entregados."""
from datos import *
from svgk import *
f = fam()
x = e1(); x = x[x.canal != 'banner']
TEMA = {'Tasa 0 y rescate de leads': 'Tasa 0', 'Referidos': 'Referidos', 'Promos de comercios KPay': 'Promos KPay',
        'Oferta de crédito e Installments': 'Crédito e Installments', 'Recuperar inactivos y churn': 'Recuperar inactivos',
        'Temporada y concursos': 'Concursos', 'Recordatorio de registro': 'Registro',
        'Lanzamiento BillPay y recargas': 'Lanzamiento BillPay', 'Boletín y contenido': 'Boletín', 'Aviso transaccional': 'Avisos de pago y cuenta',
        'Cobranza': 'Cobranza'}
ORD = ['Marketing', 'Product Growth', 'Others', 'Sales', 'Collections']
TOT = f.env.sum()
rows = []
for t in ORD:
    d = f[f.equipo == t]
    g = d.groupby('tema').apply(lambda z: pd.Series({'env': z.env.sum(), 'sin': z[~z.con].env.sum(), 'costo': z.costo.sum(), 'convf': z.convf.sum()})).reset_index()
    g['sh'] = g.env / g.env.sum()
    big = g[(g.sh >= 0.06) & g.tema.isin(TEMA)].sort_values('env', ascending=False)
    rest = g[~g.index.isin(big.index)]
    bl = [dict(tema=TEMA[r.tema], env=r.env, sin=r.sin, costo=r.costo) for r in big.itertuples()]
    if rest.env.sum() > 0: bl.append(dict(tema='Otros', env=rest.env.sum(), sin=rest.sin.sum(), costo=rest.costo.sum()))
    rows.append(dict(eq=t, env=d.env.sum(), sin=d[~d.con].env.sum(), costo=d.costo.sum(), bl=bl))
    print(t, round(d.env.sum() / 1e6, 1), [(b['tema'], round(100 * b['env'] / d.env.sum()), round(100 * b['sin'] / b['env']), round(b['costo'] / 1e6, 1)) for b in bl])
S = Svg('Mensajes de cada equipo por tema y parte que va a gente que no ha hecho nada reciente, con el gasto de cada tema')
S.t(0, 16, 'Mensajes de enero a septiembre por equipo y tema', 12.5, INK, w=600)
S.r(0, 29, 10, 10, BLUE); S.t(15, 38, 'A gente que no ha hecho nada reciente', 11.5)
S.r(250, 29, 10, 10, MRK2); S.t(265, 38, 'A quien hizo algo hace poco', 11.5)
S.t(0, 56, 'Alto de cada franja: mensajes del equipo. Ancho de cada bloque: parte del tema. Debajo del tema, su gasto en nueve meses.', 10.5, SEC)
X0, X1, Y0, Y1, GAP = 150, 778, 68, 392, 7
hp = (Y1 - Y0 - GAP * (len(rows) - 1)) / TOT
y = Y0
def tw(s, size): return 0.56 * size * len(s)
for r in rows:
    h = r['env'] * hp
    nm, sub = r['eq'], f"{r['env']/1e6:.0f} M mensajes · {r['costo']/1e6:.1f} M MXN"
    if h >= 34:
        S.t(0, y + 14, nm, 12.5, INK, w=600); S.t(0, y + 29, f"{r['env']/1e6:.0f} M mensajes ({100*r['env']/TOT:.0f} %)", 11, SEC)
        S.t(0, y + 43, f"{100*r['sin']/r['env']:.0f} % no ha hecho nada", 11, SEC) if h >= 48 else None
    else:
        S.ts(0, y + h / 2 + 4, [(nm, INK, 600), (f"  {r['env']/1e6:.0f} M ({100*r['env']/TOT:.0f} %)", SEC, 400)], 11.5)
    xx = X0
    for b in r['bl']:
        w = (X1 - X0) * b['env'] / r['env']
        ws = w * b['sin'] / b['env']
        if ws > 0.5: S.r(xx, y, max(ws - (2 if ws >= w - 0.5 else 0), 0.5), h, BLUE)
        if w - ws > 0.5: S.r(xx + ws, y, max(w - ws - 2, 0.5), h, MRK2)
        l1 = b['tema']
        l2 = f"{100*b['env']/r['env']:.0f} % · " + (f"{b['costo']/1e6:.1f} M MXN" if b['costo'] >= 0.05e6 else 'sin costo')
        one = h < 34
        if one: l1 = l1 + ' ' + l2
        need = max(tw(l1, 11), tw(l2, 10.5))
        if ws >= need + 8: lx, col = xx + 5, '#FFFFFF'
        elif (w - ws) >= need + 8: lx, col = xx + ws + 5, INK
        else:
            l1 = b['tema'] if tw(b['tema'], 11) < max(ws, w - ws) - 8 else ''
            sp = max(ws, w - ws) - 8
            l2 = f"{100*b['env']/r['env']:.0f} %" if l1 and not one else ''
            lx, col = (xx + 5, '#FFFFFF') if ws >= w - ws else (xx + ws + 5, INK)
        if l1:
            if one: S.t(lx, y + h / 2 + 4, l1, 11, col, w=600)
            else:
                S.t(lx, y + 15, l1, 11, col, w=600)
                if l2: S.t(lx, y + 29, l2, 10.5, col)
        xx += w
    y += h + GAP
S.t(0, 412, 'Gasto: correo a 0.05 MXN por enviado y WhatsApp a 1.00 MXN por entregado; push e in-app no cuestan.', 10.5, SEC)
svg = S.done()
# Cifras para el texto (E1 completo para gasto y conversión por equipo)
mp = f[f.equipo.isin(['Marketing', 'Product Growth'])]
print('MP env %.1f %% sin %.1f %%' % (100 * mp.env.sum() / TOT, 100 * mp[~mp.con].env.sum() / mp.env.sum()))
c = x.groupby('equipo').costo.sum(); print('costo E1', (c / 1e6).round(2).to_dict(), 'MP %.1f %%' % (100 * (c['Marketing'] + c['Product Growth']) / c.sum()))
for t in ['Marketing', 'Product Growth']:
    d = f[f.equipo == t]; print(t, 'debajo %.2f M' % (d[~d.pasa].costo.sum() / 1e6))
mk = x[(x.equipo == 'Marketing')]; g = mk.groupby('tema').agg(c=('costo', 'sum'), v=('conversiones_fraccional', 'sum'))
print('Mkt MXN/conv', (g.c / g.v).round(1).to_dict(), 'equipo', round(mk.costo.sum() / mk.conversiones_fraccional.sum(), 1))
save(21, dict(kind='grafica',
  titulo='Marketing y Product Growth ponen dos de cada tres mensajes, y siete de cada diez van a gente que no ha hecho nada reciente',
  que='Marketing: Tasa 0 a leads, referidos y promociones de comercios que aceptan KPay (Comercio del día, Amazon, Hot Sale). Product Growth: oferta de crédito e Installments, Tasa 0 a registrados, recuperar inactivos y concursos.',
  quien='Marketing y Product Growth (en Braze aparece como Lending) juntos: 77 % del gasto en mensajes, 44.5 M MXN en nueve meses (Marketing 27.2 M, Product Growth 17.3 M).',
  a_quien='Marketing: leads, leads fríos (rezagados y anónimos) y clientes. Product Growth: registrados que nunca pidieron crédito, clientes, ex clientes inactivos y envíos a toda la base.',
  lecturas=[
   'Marketing (259 M mensajes) y Product Growth (173 M) suman 66 % de los mensajes; 70 % de lo que mandan va a gente que no ha hecho nada reciente.',
   'Los dos mandan Tasa 0: Marketing a leads (13.6 M MXN, su tema más caro) y Product Growth a registrados sin crédito. Marketing además manda las mismas promociones de KPay que Sales.',
   'Product Growth gasta 9.9 M MXN (57 % de su gasto) en campañas que no responden lo mínimo aceptable. Marketing sí responde, pero su Tasa 0 cuesta 158 MXN por cada préstamo o solicitud de Cash.'],
  causa='Cada equipo arma ofertas para su lista completa (todos los leads, todos los registrados) y nadie es dueño de la gente que no ha hecho nada: por eso dos equipos le escriben a la misma.',
  sowhat='El volumen y el gasto están en dos equipos que ofrecen lo mismo a las mismas personas: ahí empieza el ajuste y la coordinación.',
  fuente='Fuente: Braze, envíos por campaña, mes y canal, enero a septiembre 2026; campañas con 50 mil o más mensajes entregados (657 M mensajes). Tema y a quién, según el nombre de la campaña. Gasto por equipo de todos los envíos. Préstamo o solicitud de Cash en 7 días: referencia, no prueba de venta.',
  svg=svg))
check(21)
