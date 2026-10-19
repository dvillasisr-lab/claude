"""Gráfica común de las fichas de equipo (láminas 27 a 31). Misma estructura para los cinco equipos:
izquierda, matriz tema x canal (círculo = mensajes, color = responde o no lo mínimo aceptable del canal, número = respuesta);
columna de gasto por tema; derecha, sus mejores y peores campañas con mensajes, respuesta y costo."""
import math
from datos import *
from svgk import *
CANALES = [('email', 'Correo', 'clic'), ('push notification', 'Push', 'apertura'), ('whatsapp', 'WhatsApp', 'lectura'), ('in-app', 'In-app', 'clic')]
CN = {c: (n, m) for c, n, m in CANALES}
VMAX, RMAX = 48e6, 20.0
def rad(v): return max(3.0, RMAX * math.sqrt(min(v, VMAX) / VMAX))
def pct(v): return f'{v:.2f}' if v < 10 else f'{v:.0f}'
def camp(f, eq, pat, canal):
    d = f[(f.equipo == eq) & f.familia.str.contains(pat, regex=True) & (f.canal == canal)]
    if not len(d): raise SystemExit(f'sin campaña {eq} {pat} {canal}')
    r = d.sort_values('env', ascending=False).iloc[0]
    return dict(familia=r.familia, canal=canal, env=r.env, resp=r.resp_pct, costo=r.costo, convf=r.convf, bajas=r.bajas_mil, pasa=r.vs_min >= 1,
                entrega=100 * r.wdel / r.wsend if r.wsend else float('nan'))
def linea(c):
    n, m = CN[c['canal']]
    return f"{n.lower() if n != 'WhatsApp' else n} · {pct(c['resp'])} % de {m} · {c['env']/1e6:.1f} M mensajes"
def build(eq, filas, mejores, peores, titulo_graf, resto_lab='Resto'):
    """filas: [(etiqueta, función familia->bool)]; mejores/peores: [(nombre, patrón, canal, extra(c)->str o None)]"""
    f = fam()
    d = f[f.equipo == eq].copy()
    asign = pd.Series('Resto', index=d.index)
    for lab, fn in reversed(filas):
        asign[d.familia.map(fn)] = lab
    d['fila'] = asign
    resto = d[d.fila == 'Resto'].env.sum()
    d.loc[d.fila == 'Resto', 'fila'] = resto_lab
    labs = [l for l, _ in filas] + ([resto_lab] if resto >= 0.03 * d.env.sum() else [])
    print('Resto %.1f M (%.1f %%)%s' % (resto / 1e6, 100 * resto / d.env.sum(), '' if resto_lab in labs else ' fuera de la matriz'))
    cel = d.groupby(['fila', 'canal']).agg(env=('env', 'sum'), base=('base', 'sum'), resp=('resp', 'sum'), costo=('costo', 'sum')).reset_index()
    cel['r'] = 100 * cel.resp / cel.base; cel['pasa'] = cel.r >= cel.canal.map(MIN)
    tot = d.groupby('fila').agg(env=('env', 'sum'), costo=('costo', 'sum'))
    S = Svg(f'{eq}: mensajes y respuesta por tema y canal, con sus mejores y peores campañas')
    S.t(0, 16, titulo_graf, 12.5, INK, w=600)
    S.c(6, 34, 5.5, GREEN, stroke='none'); S.t(15, 38, 'Responde lo mínimo aceptable', 11.5)
    S.c(200, 34, 5.5, BLUE, stroke='none'); S.t(209, 38, 'No lo responde', 11.5)
    S.t(320, 38, 'Círculo: mensajes de enero a septiembre', 11.5, SEC)
    LX, CW, TOP = 120, 74, 72
    nrow = len(labs); RH = min(58, (372 - TOP) / nrow)
    for j, (c, n, m) in enumerate(CANALES):
        S.t(LX + CW * j + CW / 2, TOP - 8, n, 11, SEC, 'middle', w=600)
    GX = LX + CW * 4 + 4
    S.t(GX + 40, TOP - 8, 'Gasto', 11, SEC, 'middle', w=600)
    for i, lab in enumerate(labs):
        y0 = TOP + RH * i
        S.l(0, y0, GX + 76, y0, GRID)
        words = lab.split(' '); lines, cur = [], ''
        for w_ in words:
            if len(cur + ' ' + w_) > 17 and cur: lines.append(cur); cur = w_
            else: cur = (cur + ' ' + w_).strip()
        lines.append(cur)
        if len(lines) > 2: raise SystemExit('etiqueta larga: ' + lab)
        for q, ln in enumerate(lines): S.t(0, y0 + 15 + 13 * q, ln, 11, INK, w=600)
        S.t(0, y0 + 15 + 13 * len(lines), f"{tot.loc[lab, 'env']/1e6:.1f} M mensajes", 10.5, SEC)
        cy = y0 + RH / 2 - 5
        for j, (c, n, m) in enumerate(CANALES):
            z = cel[(cel.fila == lab) & (cel.canal == c)]
            cx = LX + CW * j + CW / 2
            if not len(z) or z.env.iloc[0] < 50000:
                S.t(cx, cy + 4, '·', 11, MRK2, 'middle'); continue
            z = z.iloc[0]
            S.c(cx, cy, rad(z.env), GREEN if z.pasa else BLUE, op=0.9)
            S.t(cx, y0 + RH - 6, f'{pct(z.r)} %', 10.5, INK, 'middle', w=600, halo=True)
        cst = tot.loc[lab, 'costo']
        S.t(GX + 40, cy + 4, f'{cst/1e6:.1f} M MXN' if cst >= 0.05e6 else 'casi 0', 10.5, INK, 'middle', w=600)
    S.l(0, TOP + RH * nrow, GX + 76, TOP + RH * nrow, GRID)
    # panel derecho
    PX = 528
    S.l(PX - 12, 52, PX - 12, 400, GRID)
    y = 64
    detalle = {}
    for tit, lista, col in [('Sus mejores campañas', mejores, GREEN), ('Sus peores campañas', peores, BLUE)]:
        S.t(PX, y, tit, 11.5, col, w=600); y += 16
        for nm, pat, canal, extra in lista:
            c = camp(f, eq, pat, canal); detalle[nm + ' ' + canal] = c
            S.r(PX, y - 9, 3, 26 + (13 if extra else 0), col)
            S.t(PX + 9, y, nm, 11, INK, w=600)
            S.t(PX + 9, y + 13, linea(c), 10.5, TXT)
            ex = extra(c) if extra else None
            if ex: S.t(PX + 9, y + 26, ex, 10.5, SEC); y += 13
            y += 34
        y += 6
    S.t(PX, 384, 'Tamaño', 10.5, SEC)
    lx = PX + 44
    for v, lab in [(1e6, '1 M'), (10e6, '10 M'), (40e6, '40 M')]:
        S.c(lx + rad(v), 380, rad(v), '#FFFFFF', stroke=MRK, sw=1); S.t(lx + 2 * rad(v) + 4, 384, lab, 10.5, SEC); lx += 2 * rad(v) + 34
    S.t(0, 412, 'Número: respuesta (clic, apertura o lectura). Mínimo aceptable: 0.3 % en correo, 0.75 % en push, 60 % en WhatsApp, 10 % en in-app.', 10.5, SEC)
    return S.done(), cel, tot, detalle, d
def mxn_conv(c):
    return f"{c['costo']/1e6:.2f} M MXN · {c['costo']/c['convf']:,.0f} MXN por préstamo" if c['convf'] > 0 and c['costo'] > 0 else None
def mxn_wa(c):
    return f"{c['costo']/1e6:.2f} M MXN · llega {c['entrega']:.0f} % de los WhatsApp"
