"""Lámina 78 (forma de la lámina 41 del v5): campañas que siguieron mandando después de responder menos de lo mínimo. Seis paneles:
respuesta mensual contra lo mínimo, mes en que cayó debajo marcado, sombreado lo que mandó después. Regla insisten() de b7.py (E1)."""
from b7 import *

e = load_e1()
R = insisten(e)
X = R[~R.tema.isin(["Cobranza", "Transaccional"]) & (R.after > 0)].copy()
TOT = e.envios.sum()
top = X.sort_values("after", ascending=False).head(5)
wa = X[(X.canal == "whatsapp") & ~X.index.isin(top.index)].sort_values("acost", ascending=False).head(1)
cells = pd.concat([top, wa])
eqx = X.groupby("equipo").agg(a=("after", "sum"), c=("acost", "sum"))
eqt = e.groupby("equipo").envios.sum()
cx = X.groupby("canal").agg(a=("after", "sum"), c=("acost", "sum"))
tx = X.groupby("tema").after.sum().sort_values(ascending=False)
ex_ = X.groupby("etapa").agg(a=("after", "sum"), c=("acost", "sum"))
print(R.after.sum() / 1e6, R.acost.sum() / 1e6, X.after.sum() / 1e6, X.acost.sum() / 1e6, X.after2.sum() / 1e6, X.acost2.sum() / 1e6, (X.lastm == 9).sum())
print(cells[["fam", "canal", "equipo", "fail", "after", "acost", "am"]])
NOM = {"B0211-CANVAS-Nuevos_RegistradosPay": "Tasa 0 a registrados de KPay sin crédito", "B0223": "Crédito en plazos a quien nunca lo activó",
       "Anonimos-RescateTasa0": "Rescate Tasa 0 a anónimos", "Recurrentes_Dormants-ReferralProgram": "Referidos a ex clientes inactivos",
       "S0004": "Recomendaciones semanales de Shopping", "B0209": "Descuento directo a clientes KCash inactivos", "B0333": "Oferta a ex clientes KPay, 12 meses",
       "B0171-CANVAS-Leads_BBDDRezagada": "Rescate Tasa 0 a leads rezagados", "B0210": "Tasa 0 a quien nunca usó KCash"}
def nom(f): return [v for k, v in NOM.items() if k in f][0]
UNI = {"email": ("clics por mil", 10, "Email"), "push notification": ("aperturas por mil", 10, "Push"), "whatsapp": ("% leídos", 1, "WhatsApp"), "in-app": ("% con clic", 1, "In-app")}
S = SVG("Seis campañas que siguieron mandando después de responder menos de lo mínimo: respuesta por mes, mes en que cayeron debajo y mensajes enviados después")
S.legend([("Respuesta del mes", INK, "ln"), ("Mes en que cayó debajo de lo mínimo", BLUE, "ci"), ("Lo que mandó después", "#E3E9FA", "sq")], 0, 14, 18)
CW, CH = 262, 186
for i, (_, c) in enumerate(cells.iterrows()):
    x0 = 18 + (i % 3) * CW; y0 = 70 + (i // 3) * CH; w, h = CW - 50, 82
    b, r = RESP[c.canal]; un, k, cl = UNI[c.canal]
    g = e[(e.fam == c.fam) & (e.canal == c.canal)].groupby("m").agg(b=(b, "sum"), r=(r, "sum"), env=("envios", "sum"))
    g = g[g.b > 0]; rate = k * 100 * g.r / g.b
    mn = k * MIN[c.canal]
    S.t(x0 - 12, y0 - 28, nom(c.fam), 11.5, INK, w=700)
    S.t(x0 - 12, y0 - 14, f"{c.equipo} · {cl} · {g.env.sum()/1e6:.1f} M mensajes", 10.5, SEC)
    hi = max(rate.max(), mn * 1.4) * 1.15
    Y = lambda v: y0 + h - h * v / hi
    slot = w / 9; X_ = lambda m: x0 + (m - 0.5) * slot
    xf = X_(c.fail)
    S.rect(xf, y0, x0 + w - xf, h, "#E3E9FA")
    S.line(x0, Y(mn), x0 + w, Y(mn), INK, 1, ' stroke-dasharray="4 4" opacity="0.6"')
    pts = [(X_(m), Y(v)) for m, v in rate.items()]
    S.raw('<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f'" fill="none" stroke="{INK}" stroke-width="2"/>')
    for m, v in rate.items():
        S.circle(X_(m), Y(v), 5 if m == c.fail else 2.6, BLUE if m == c.fail else INK, "#FFFFFF", 1.2)
    vf = rate.get(c.fail); ml = rate.index.max()
    S.t(X_(c.fail), Y(vf) - 9, f"{vf:.1f}" if vf < 10 else f"{vf:.0f}", 10.5, BLUE, "middle", 700, halo=True)
    if ml != c.fail: S.t(X_(ml), Y(rate[ml]) - 9, f"{rate[ml]:.1f}" if rate[ml] < 10 else f"{rate[ml]:.0f}", 10.5, INK, "middle", 600, halo=True)
    for m in range(1, 10):
        if m % 2 == 1 or m == 9: S.t(X_(m), y0 + h + 13, MESES[m - 1], 10.5, SEC, "middle")
    S.t(x0 - 12, y0 + h + 31, f"{c.after/1e6:.1f} M mensajes después" + (f" · {c.acost/1e6:.1f} M MXN" if c.acost > 5e4 else ""), 11, BLUE, w=700)
    S.t(x0 - 12, y0 + h + 45, f"{un}; punteada: mínimo {mn:g}", 10.5, SEC)
J = dict(
    titulo="Uno de cada cinco mensajes salió de campañas que un mes antes ya respondían menos de lo mínimo",
    que="Tasa 0, referidos, ofertas para volver y crédito en plazos.",
    quien=f"Product Growth {eqx.loc['Product Growth','a']/1e6:.0f} M mensajes, Marketing {eqx.loc['Marketing','a']/1e6:.0f} M, Others y Sales menos.",
    a_quien="Registrados sin crédito, leads y ex clientes inactivos.",
    lecturas=[
        f"{X.after.sum()/1e6:.0f} M mensajes ({100*X.after.sum()/TOT:.0f} % del año) y {X.acost.sum()/1e6:.1f} M MXN salieron ya debajo de lo mínimo.",
        "Tasa 0 a registrados de KPay cayó debajo en febrero y siguió siete meses casi igual.",
        f"Con salida a los dos meses se evitaban {X.after2.sum()/1e6:.0f} M mensajes y {X.acost2.sum()/1e6:.1f} M MXN.",
    ],
    causa="Las campañas se apagan cuando acaba la promoción, no cuando dejan de responder.",
    sowhat="La campaña que no responde no se detiene sola: dos meses debajo de lo mínimo y se rehace o apaga.",
    fuente="Fuente: Braze, envíos por campaña, canal y mes, ene a sep 2026. Cae debajo: primer mes con 50 mil personas o más bajo lo mínimo. Sin cobranza ni avisos. WhatsApp a 1.00 MXN por entregado.",
    svg=S.out())
write(78, J)
