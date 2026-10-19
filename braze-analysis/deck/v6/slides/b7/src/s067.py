"""Lámina 67: las 10 campañas de email con más correos entregados: parte del email contra parte de los clics. Panel de push en lecturas.
Fuente: E1, email (clic sobre entregados) y push (apertura sobre enviados), campaña = nombre sin fecha."""
from b7 import *

e = load_e1()
res = {}
for canal in ["email", "push notification"]:
    b, r = RESP[canal]
    x = e[e.canal == canal].groupby("fam").agg(base=(b, "sum"), resp=(r, "sum"), equipo=("equipo", "first"))
    x = x.sort_values("base", ascending=False); TB, TR = x.base.sum(), x.resp.sum()
    x["rate"] = 100 * x.resp / x.base; x["pb"] = 100 * x.base / TB; x["pr"] = 100 * x.resp / TR
    res[canal] = (x, TB, TR)
x, TB, TR = res["email"]; t = x.head(10).copy()
xp, TBp, TRp = res["push notification"]
NOM = {"B0211": ("Tasa 0 a registrados de KPay sin crédito", "registrados que nunca tomaron crédito", "promo"),
       "BillPay_Intro": ("Lanzamiento de BillPay", "toda la base", "promo"),
       "B0223": ("Crédito en plazos a quien nunca lo activó", "registrados que nunca tomaron crédito", "promo"),
       "BKT1": ("Cobranza de atraso menor (BKT1)", "clientes con pago atrasado", "cobranza"),
       "Retargeting_Veriff": ("Recordatorio de verificar identidad (Veriff)", "dejaron el registro a medias", "bueno"),
       "Payment-Confirmation": ("Confirmación de pago KPay", "acaban de pagar", "bueno"),
       "B0326": ("Referidos: invita a un amigo", "leads", "promo"),
       "B0209": ("Descuento directo para que vuelva", "ex clientes inactivos", "promo"),
       "AnotayGana": ("Sorteo AnotayGana", "toda la base", "promo"),
       "WeeklyRecommendations": ("Recomendaciones semanales de Shopping", "usuarios de Shopping", "promo")}
def nom(f):
    for k, v in NOM.items():
        if k in f: return v
    raise KeyError(f)
t["nom"], t["aq"], t["cl"] = zip(*t.index.map(nom))
P = t[t.cl == "promo"]
print(t[["equipo", "nom", "rate", "pb", "pr"]].round(2).to_string())
print("top10", t.pb.sum(), t.pr.sum(), "promo", len(P), P.pb.sum(), P.pr.sum(), "prom email", 100 * TR / TB, "campañas", len(x))
xp, TBp, TRp = res["push notification"]; tp = xp.head(10)
print("push top10", tp.pb.sum(), tp.pr.sum(), tp.equipo.value_counts().to_dict())

import math
S = SVG("Pareto de campañas de email y de push: porcentaje acumulado de los mensajes contra porcentaje acumulado de las respuestas, de la campaña más grande a la más chica")
S.legend([("% acumulado de los mensajes", BLUE, "ln"), ("% acumulado de las respuestas (clics o aperturas)", GREEN, "ln")], 0, 14, 18)
def panel(x0, w, y0, h, xx, title, sub):
    n = len(xx)
    X = lambda i: x0 + w * math.log10(i) / math.log10(n)
    Y = lambda v: y0 + h - h * v / 100
    cv = 100 * xx.base.cumsum() / xx.base.sum(); cr = 100 * xx.resp.cumsum() / xx.resp.sum()
    S.t(x0, y0 - 22, title, 12, INK, w=700); S.t(x0, y0 - 8, sub, 10.5, SEC)
    for v in (0, 25, 50, 75, 100):
        S.line(x0, Y(v), x0 + w, Y(v), GRID); S.t(x0 - 6, Y(v) + 4, f"{v} %", 10.5, SEC, "end")
    for v in (1, 3, 10, 30, 100, 300, 1000):
        if v <= n: S.t(X(v), y0 + h + 14, f"{v}", 10.5, SEC, "middle")
    pv = [(X(i + 1), Y(v)) for i, v in enumerate(cv)]; pr = [(X(i + 1), Y(v)) for i, v in enumerate(cr)]
    area = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pv) + " L" + " L".join(f"{x:.1f},{y:.1f}" for x, y in reversed(pr)) + " Z"
    S.raw(f'<path d="{area}" fill="{BLUE}" fill-opacity="0.08"/>')
    S.raw('<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in pv) + f'" fill="none" stroke="{BLUE}" stroke-width="2.5"/>')
    S.raw('<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in pr) + f'" fill="none" stroke="{GREEN}" stroke-width="2.5"/>')
    S.line(X(10), y0, X(10), y0 + h, INK, 1, ' stroke-dasharray="4 4" opacity="0.6"')
    S.t(X(10) + 5, Y(cv.iloc[9]) - 8, f"Las 10 primeras: {cv.iloc[9]:.0f} % del volumen", 11, BLUE, w=700, halo=True)
    S.t(X(10) + 5, Y(cr.iloc[9]) + 16, f"{cr.iloc[9]:.0f} % de las respuestas", 11, GREEN, w=700, halo=True)
    for i in range(10):
        pass
    return X, Y, cv, cr
X, Y, cv, cr = panel(44, 330, 64, 170, x, f"Email: {len(x):,} campañas", "De la que más correos mandó a la que menos")
for i, (f, r) in enumerate(t.iterrows()):
    col = BLUE if r.cl == "promo" else (GREEN if r.cl == "bueno" else MARK)
    S.circle(X(i + 1), Y(cv.iloc[i]), 4, col, "#FFFFFF", 1.2)
for i in (0, 1, 2):
    S.t(X(i + 1), Y(cv.iloc[i]) - 8, f"{i+1}", 10.5, INK, "middle", 700, halo=True)
Xp, Yp, cvp, crp = panel(436, 330, 64, 170, xp, f"Push: {len(xp):,} campañas", "De la que más push mandó a la que menos")
for i in range(10):
    S.circle(Xp(i + 1), Yp(cvp.iloc[i]), 4, BLUE if xp.index[i].split("-")[0] == "Marketing" else MARK, "#FFFFFF", 1.2)
S.t(436, 268, f"{int((tp.equipo=='Marketing').sum())} de las 10 más grandes son de Marketing (punto azul).", 10.5, SEC)
# lista de las 10 de email
S.line(0, 284, 780, 284, GRID)
S.t(0, 300, "Las 10 campañas de email con más correos: % de los correos del año y % de los clics", 11, INK, w=600)
for i, (f, r) in enumerate(t.iterrows()):
    col = BLUE if r.cl == "promo" else (GREEN if r.cl == "bueno" else TXT)
    cx, cy = (0 if i < 5 else 396), 318 + 18 * (i % 5)
    S.tspans(cx, cy, [(f"{i+1}. {r.nom}", col, 600), (f" · {r.equipo} · ", SEC, 400), (f"{r.pb:.1f} % / {r.pr:.1f} %", INK, 600)], 10.5)
S.t(0, 412, f"Azul: las siete promociones, {P.pb.sum():.0f} % de los correos y {P.pr.sum():.0f} % de los clics. Verde: recordatorio y aviso de pago. Gris: cobranza.", 10.5, SEC)
J = dict(
    titulo=f"Siete de los diez correos más grandes son promociones a listas: {P.pb.sum():.0f} % del email y solo {P.pr.sum():.0f} % de los clics",
    que="Tasa 0, BillPay, crédito en plazos, referidos, descuentos, AnotayGana y Shopping.",
    quien="Product Growth 4 de las 10, Others 3, Marketing 2 y Collections 1.",
    a_quien="Registrados sin crédito, leads, ex clientes y toda la base.",
    lecturas=[
        f"Tasa 0 a registrados de KPay: {t.iloc[0].pb:.0f} % del email, {t.iloc[0].pr:.0f} % de los clics y {10*t.iloc[0].rate:.1f} clics por mil.",
        f"Veriff ({10*t.loc[[i for i in t.index if 'Veriff' in i][0],'rate']:.0f} clics por mil) y la confirmación de pago ({10*t.loc[[i for i in t.index if 'Payment' in i][0],'rate']:.0f}) van a quien acaba de hacer algo.",
        f"En push, las diez más grandes son {tp.pb.sum():.0f} % del volumen y {tp.pr.sum():.0f} % de las aperturas; {int((tp.equipo=='Marketing').sum())} son de Marketing.",
    ],
    causa="Las campañas grandes salen a listas, no por algo que hizo la persona, y nadie limita su tamaño.",
    sowhat="Un tercio del email se va en siete promociones que casi nadie toca: son las primeras a rehacer.",
    fuente=f"Fuente: Braze, envíos por campaña y canal, ene a sep 2026; {len(x):,} campañas de email y {len(xp)} de push. Clics sobre correos entregados; aperturas sobre push enviados.",
    svg=S.out())
write(67, J)
