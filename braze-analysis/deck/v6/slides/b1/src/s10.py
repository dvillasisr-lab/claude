"""Lámina 10: cada campaña (todas sus versiones, 100 mil o más entregados) por tamaño y respuesta, en correo y push, contra el mínimo
de la industria (clic de correo 1.5 %, apertura de push 3 %; METRICAS y Estándares del Sheets v4). Lo que ganaríamos al llegar al mínimo,
por regla de tres sobre los totales del canal (E1)."""
import numpy as np
from comun import load, write, Svg, INK, TXT, SEC, GRID, GREEN, G1, G2, FUENTE_E1

d = load()
s = d[['email_sent', 'email_delivery', 'email_click', 'pn_send', 'pn_open']].sum()
clic_mas = s.email_delivery * 0.015 - s.email_click
email_menos = s.email_sent * (1 - (s.email_click / s.email_delivery) / 0.015)
push_mas = s.pn_send * 0.03 - s.pn_open
resp_mas = clic_mas + push_mas
CAN = [('email', 'Correo: clic de cada 100 entregados', 'email_delivery', 'email_click', 1.5, 4.0, 'Correos entregados por campaña'),
       ('push notification', 'Push: apertura de cada 100 enviados', 'pn_send', 'pn_open', 3.0, 8.0, 'Push enviados por campaña')]
NOM = {'email': {'Lending-KCash-B0211-CANVAS-Nuevos_RegistradosPay-Tasa0-N/A': ('Tasa 0 a nuevos registrados', 'end', -10),
                 'NewProducts-Kueski-T0000-E-Portfolio_BillPay_Intro_Full_Rollout': ('Presentación de BillPay', 'end', 4),
                 'Marketing-KCash-B0000-CANVAS-Leads_LeftFunnel-Retargeting_Veriff': ('Terminar la verificación', 'end', -6),
                 'Transaccional-KPay-Mail-Payment-Confirmation-20240821': ('Confirmación de pago', 'end', -6)},
       'push notification': {'Marketing-KCash-B0391-CANVAS-Leads_BDDMarketing-RescateFinesDeSemana-N/A': ('Rescate de fin de semana', 'end', -6),
                 'Payment Received - Push': ('Pago recibido', 'start', 14),
                 'Collections-KCash-T000-CANVAS-Precobranza-ecosystem': ('Precobranza', 'start', -6)}}
ST = {}
S = Svg('Respuesta de cada campaña contra su tamaño, en correo y push, con el mínimo de la industria')
S.o.append(f'<circle cx="5" cy="11" r="4" fill="{GREEN}"/>'); S.t(14, 15, 'Llega al mínimo de la industria', 11.5, TXT)
S.o.append(f'<circle cx="215" cy="11" r="4" fill="{G2}"/>'); S.t(224, 15, 'No llega', 11.5, TXT)
S.t(780, 15, 'Cada punto es una campaña con 100 mil o más entregados', 11, SEC, 'end')
for n, (c, tit, b, r, mn, cap, xl) in enumerate(CAN):
    g = d[d.canal == c].groupby('fam').agg(b=(b, 'sum'), r=(r, 'sum')).reset_index()
    g = g[g.b >= 100000].copy(); g['rr'] = 100 * g.r / g.b; g['ok'] = g.rr >= mn
    ST[c] = dict(n=len(g), ok=int(g.ok.sum()), vol_no=g[~g.ok].b.sum() / g.b.sum())
    px, PW, top, bot = 44 + n * 402, 330, 58, 330
    LO, HI = 4.75, np.log10(40e6)
    xx = lambda v: px + PW * (np.log10(v) - LO) / (HI - LO)
    yy = lambda v: bot - (bot - top) * min(v, cap) / cap
    S.t(px, top - 14, tit, 12, INK, 'start', 700)
    for k in range(5):
        v = cap * k / 4; S.line(px, yy(v), px + PW, yy(v), GRID); S.t(px - 5, yy(v) + 4, f'{v:g} %', 10.5, SEC, 'end')
    for v, lab in ((1e5, '100 mil'), (1e6, '1 M'), (1e7, '10 M')):
        S.t(xx(v), bot + 14, lab, 10.5, SEC, 'middle')
    S.t(px + PW, bot + 28, xl + ' (escala log)', 10.5, SEC, 'end')
    for _, z in g.sort_values('ok').iterrows():
        S.o.append(f'<circle cx="{xx(z.b):.1f}" cy="{yy(z.rr):.1f}" r="{3.2 if z.ok else 2.6}" fill="{GREEN if z.ok else G2}" fill-opacity="{0.95 if z.ok else 0.8}" stroke="#fff" stroke-width="0.5"/>')
    S.line(px, yy(mn), px + PW, yy(mn), INK, 1, ' stroke-dasharray="4 3"')
    S.t(px + PW, yy(mn) - 5, f'Mínimo {mn:g} %', 11, INK, 'end', 600, halo=True)
    for fam, (nm, anchor, dy) in NOM[c].items():
        z = g[g.fam == fam]
        if len(z):
            z = z.iloc[0]; x0, y0 = xx(z.b), yy(z.rr)
            S.circle(x0, y0, 3.8, GREEN if z.ok else G1)
            val = f'{z.rr:.2f} %' if z.rr < 1 else f'{z.rr:.1f} %'
            S.t(x0 + (-7 if anchor == 'end' else 7), y0 + dy, f'{nm} {val}', 10.5, INK, anchor, 600, halo=True)
    S.t(px, bot + 48, f'{ST[c]["ok"]} de {ST[c]["n"]} llegan; las que no son {ST[c]["vol_no"] * 100:.0f} % del volumen', 11.5, INK, 'start', 600)
print(ST, clic_mas / 1e6, push_mas / 1e6, email_menos / 1e6, resp_mas / 1e6)

e, p = ST['email'], ST['push notification']
write(10, dict(kind='grafica',
    titulo=f'Si correo y push respondieran lo mínimo de la industria, tendríamos {resp_mas / 1e6:.1f} M respuestas más con igual volumen',
    que='Todo lo que sale por correo y push, sobre todo promociones.',
    quien='Todos los equipos; Marketing y Product Growth ponen la mayor parte del volumen.',
    a_quien='Toda la base: 19.5 M personas.',
    lecturas=[
        f'Correo: {e["ok"]} de {e["n"]} campañas llegan a 1.5 % de clic; las que no llegan son {e["vol_no"] * 100:.0f} % de los correos.',
        f'Push: {p["ok"]} de {p["n"]} llegan a 3 % de apertura; las que no llegan son {p["vol_no"] * 100:.0f} % de los push.',
        f'Al mínimo: {clic_mas / 1e6:.1f} M clics y {push_mas / 1e6:.1f} M aperturas más, o los mismos clics con {email_menos / 1e6:.0f} M correos menos.'],
    causa='Nadie revisa cada campaña contra un mínimo: la que responde poco sigue saliendo mes tras mes.',
    sowhat='Hay margen sin gastar más: está en a quién y qué mandamos, no en mandar más.',
    fuente='Fuente: Braze, E1, enero a septiembre 2026; campañas con 100 mil o más entregados. Mínimo de la industria (METRICAS): clic 1.5 %, apertura 3 %. Lo que pasa de la escala va en el borde.',
    svg=S.done()))
