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

S = SVG("Las diez campañas de email con más correos: porcentaje del email entregado y porcentaje de los clics de cada una")
X0, X1, VM = 330, 640, 12
xs = lambda v: X0 + (X1 - X0) * v / VM
S.legend([("% de los correos entregados", MARK2, "sq"), ("% de los clics (promociones)", BLUE, "sq"), ("% de los clics (recordatorio y aviso)", GREEN, "sq"), ("cobranza", MARK, "sq")], 0, 14, 18, 11.5)
TOP, RH = 64, 29
S.t(0, TOP - 14, "Campaña · equipo · a quién va", 11, SEC, w=600)
S.t(780, TOP - 14, "Clics por mil", 11, SEC, "end", 600)
for v in (0, 4, 8, 12):
    S.line(xs(v), TOP - 8, xs(v), TOP + RH * 10 - 4, GRID)
    S.t(xs(v), TOP + RH * 10 + 10, f"{v} %", 11, SEC, "middle")
for i, (f, r) in enumerate(t.iterrows()):
    y = TOP + RH * i
    col = {"promo": BLUE, "bueno": GREEN, "cobranza": MARK}[r.cl]
    S.t(0, y + 7, r.nom, 11.5, INK, w=600)
    S.t(0, y + 20, f"{r.equipo} · {r.aq}", 10.5, SEC)
    S.rect(X0, y - 2, xs(r.pb) - X0, 10, MARK2)
    S.rect(X0, y + 10, max(xs(r.pr) - X0, 1.5), 10, col)
    S.t(xs(r.pb) + 4, y + 7, f"{r.pb:.1f} %", 10.5, SEC)
    S.t(xs(r.pr) + 4, y + 19, f"{r.pr:.1f} %", 10.5, INK, w=600)
    S.t(780, y + 13, f"{10*r.rate:.1f}" if r.rate < 1 else f"{10*r.rate:.0f}", 12, col if r.cl != "cobranza" else TXT, "end", 700)
S.line(0, TOP + RH * 10 + 20, 780, TOP + RH * 10 + 20, MARK)
yy = TOP + RH * 10 + 38
S.tspans(0, yy, [(f"Las siete promociones: ", INK, 600), (f"{P.pb.sum():.0f} % de los correos entregados y {P.pr.sum():.0f} % de los clics. ", BLUE, 600),
                 (f"El correo promedio da {1000*TR/TB:.0f} clics por mil.", TXT, 400)], 11.5)
S.t(0, yy + 16, f"Las diez juntas son {t.pb.sum():.0f} % de los correos y {t.pr.sum():.0f} % de los clics, entre {len(x):,} campañas de email.", 11, SEC)

J = dict(
    titulo=f"Siete de los diez correos con más envíos son promociones a listas grandes: se llevan {P.pb.sum():.0f} % del email y solo {P.pr.sum():.0f} % de los clics",
    que="Promociones: Tasa 0, lanzamiento de BillPay, crédito en plazos, referidos, descuento para volver, sorteo AnotayGana y recomendaciones de Shopping. Además, cobranza, el recordatorio de Veriff y la confirmación de pago.",
    quien=f"Product Growth tiene 4 de las 10 ({t[t.equipo=='Product Growth'].pb.sum():.0f} % del email y {t[t.equipo=='Product Growth'].pr.sum():.0f} % de los clics); Others 3 (BillPay, Shopping, confirmación de pago); Marketing 2 (Veriff y referidos); Collections 1.",
    a_quien="Las siete promociones van a listas: registrados que nunca tomaron crédito, leads, ex clientes inactivos y toda la base. Las dos que responden van a quien acaba de hacer algo.",
    lecturas=[
        f"Tasa 0 a registrados de KPay es {t.iloc[0].pb:.0f} % de todo el email y {t.iloc[0].pr:.0f} % de los clics: {10*t.iloc[0].rate:.1f} clics por cada mil correos, menos de lo mínimo aceptable (3).",
        f"Las dos que sí responden van a alguien que acaba de hacer algo: Veriff ({10*t.loc[[i for i in t.index if 'Veriff' in i][0],'rate']:.0f} clics por mil) a quien dejó el registro a medias y la confirmación de pago ({10*t.loc[[i for i in t.index if 'Payment' in i][0],'rate']:.0f}) a quien acaba de pagar.",
        f"En push pasa lo mismo: las diez con más envíos son {tp.pb.sum():.0f} % del push y {tp.pr.sum():.0f} % de las aperturas; {int((tp.equipo=='Marketing').sum())} son de Marketing a leads (rescate de fin de semana, Tasa 0, referidos, BillPay).",
    ],
    causa="Las campañas más grandes se arman para listas (todos los registrados, toda la base) y no por algo que la persona hizo; como el correo cuesta 5 centavos, nadie pone límite al tamaño.",
    sowhat="Un tercio del email se va en siete promociones que casi nadie abre ni toca: son las primeras que hay que rehacer o achicar.",
    fuente=f"Fuente: Braze, envíos por campaña, mes y canal, enero a septiembre 2026; {len(x):,} campañas de email (campaña = todas sus versiones). Porcentajes sobre correos entregados y clics del año. Push: aperturas sobre push enviados.",
    svg=S.out())
write(67, J)
