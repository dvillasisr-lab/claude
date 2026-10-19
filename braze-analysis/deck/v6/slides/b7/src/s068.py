"""Lámina 68: cascada del gasto de septiembre de las campañas promocionales que no responden lo mínimo y siguen activas;
las cinco con más gasto en el año, con canal, lectura, entrega y costo por conversión de referencia por email contra WhatsApp.
Fuente: muestra_c_familias.csv (señal) y E1 (septiembre y conversiones). WhatsApp por entregado."""
from b7 import *

e = load_e1(); c = load_c()
s9 = e[e.m == 9].groupby(["fam", "canal"]).agg(env9=("envios", "sum"), c9=("costo", "sum")).reset_index()
no = c[c.senal == "apagar o rehacer"]
a = no[(no.tipo == "promocional o lifecycle") & (no.activo_sep == 1)].merge(s9, left_on=["familia", "canal"], right_on=["fam", "canal"], how="left")
top = no.sort_values("costo_ent", ascending=False).head(5).merge(s9, left_on=["familia", "canal"], right_on=["fam", "canal"], how="left")
T9 = a.c9.sum(); TA = no.costo_ent.sum()
print("sep activas", len(a), T9, "top5 sep", top.c9.sum(), "top5 año", top.costo_ent.sum(), TA)
NOM = {"B0171": ("Rescate Tasa 0 a leads rezagados", "Marketing", "leads que no terminaron registro"),
       "B0211": ("Tasa 0 a registrados de KPay sin crédito", "Product Growth", "registrados sin crédito"),
       "B0333": ("Oferta a ex clientes KPay, 12 meses", "Product Growth", "ex clientes (churn)"),
       "B0209": ("Descuento a clientes KCash inactivos", "Product Growth", "ex clientes inactivos"),
       "B0223": ("Crédito en plazos a quien nunca lo activó", "Product Growth", "registrados sin crédito"),
       "BillPay_Intro": ("Lanzamiento de BillPay", "Others", "toda la base")}
rows = []
for _, r in top.iterrows():
    k = [k for k in NOM if k in r.familia][0]
    f = e[e.fam == r.familia].groupby("canal").agg(costo=("costo", "sum"), conv=("conversiones_filas", "sum"), ws=("whatsapp_send", "sum"), wd=("whatsapp_delivery", "sum"), wr=("whatsapp_read", "sum"))
    cpc = (f.costo / f.conv).to_dict()
    w = f.loc["whatsapp"] if "whatsapp" in f.index else None
    rows.append(dict(k=k, nom=NOM[k][0], eq=NOM[k][1], aq=NOM[k][2], canal=r.canal, anual=r.costo_ent, sep=r.c9 if r.c9 == r.c9 else 0,
                     cpe=cpc.get("email"), cpw=cpc.get("whatsapp"), ent=100 * w.wd / w.ws if w is not None else None, lec=100 * w.wr / w.wd if w is not None else None))
    print(k, r.canal, round(r.costo_ent), round(r.c9 if r.c9 == r.c9 else 0), {kk: round(v, 1) for kk, v in cpc.items()}, rows[-1]["ent"], rows[-1]["lec"])
otras9 = T9 - top.c9.sum(); print("otras sep", otras9)

import math
S = SVG("Pareto del gasto en campañas que no responden lo mínimo: porcentaje acumulado del gasto del año, de la campaña más cara a la más barata")
S.legend([("% acumulado del gasto", BLUE, "ln"), ("WhatsApp", BLUE, "ci"), ("Email", MARK, "ci")], 0, 14, 18)
nos = no.sort_values("costo_ent", ascending=False).reset_index(drop=True)
cum = 100 * nos.costo_ent.cumsum() / nos.costo_ent.sum(); N = len(nos)
X0, X1, Y0, Y1 = 46, 470, 44, 370
X = lambda i: X0 + (X1 - X0) * math.log10(i) / math.log10(N)
Y = lambda v: Y1 - (Y1 - Y0) * v / 100
for v in (0, 25, 50, 75, 100):
    S.line(X0, Y(v), X1, Y(v), GRID); S.t(X0 - 6, Y(v) + 4, f"{v} %", 10.5, SEC, "end")
for v in (1, 3, 10, 30, 100, 300):
    if v <= N: S.t(X(v), Y1 + 14, f"{v}", 10.5, SEC, "middle")
S.t(X1, Y1 + 30, f"{N} campañas por canal que no responden, de la más cara a la más barata", 10.5, SEC, "end")
S.raw('<path d="M' + " L".join(f"{X(i+1):.1f},{Y(v):.1f}" for i, v in enumerate(cum)) + f'" fill="none" stroke="{BLUE}" stroke-width="2.5"/>')
S.line(X(5), Y0, X(5), Y1, INK, 1, ' stroke-dasharray="4 4" opacity="0.6"')
S.t(X(5) + 6, Y(cum[4]) + 16, f"Las 5 primeras: {cum[4]:.0f} % del gasto ({nos.costo_ent[:5].sum()/1e6:.1f} M MXN)", 11, BLUE, w=700, halo=True)
for i in range(10):
    S.circle(X(i + 1), Y(cum[i]), 4.5 if i < 5 else 3, BLUE if nos.canal[i] == "whatsapp" else MARK, "#FFFFFF", 1.2)
for i in range(5): S.t(X(i + 1), Y(cum[i]) - 9, f"{i+1}", 10.5, INK, "middle", 700, halo=True)
# lista de las cinco a la derecha
S.t(506, 60, "Las cinco campañas más caras", 12, INK, w=700)
S.t(506, 76, "Gasto del año y MXN por cada conversión", 10.5, SEC)
for i, r in enumerate(rows):
    y = 104 + 52 * i
    col = BLUE if r["canal"] == "whatsapp" else TXT
    S.t(506, y, f"{i+1}. {r['nom']}", 10.5, INK, w=700)
    S.t(506, y + 14, f"{r['eq']} · {'WhatsApp' if r['canal']=='whatsapp' else 'Email'} · {r['anual']/1e6:.1f} M MXN", 10.5, col, w=600)
    if r.get("cpw"): S.t(506, y + 28, f"por conversión: email {r['cpe']:,.0f} · WhatsApp {r['cpw']:,.0f} MXN", 10.5, SEC)
    elif r.get("cpe") and r["cpe"] < 1e6: S.t(506, y + 28, f"por conversión: email {r['cpe']:,.0f} MXN", 10.5, SEC)
    else: S.t(506, y + 28, "sin conversiones registradas", 10.5, SEC)
R = {r["k"]: r for r in rows}
J = dict(
    titulo=f"Cinco campañas son {100*top.costo_ent.sum()/TA:.0f} % del gasto que no responde, y cuatro de ellas son de Product Growth",
    que="Tasa 0, crédito en plazos, oferta a ex clientes KPay y lanzamiento de BillPay.",
    quien="Product Growth (cuatro) y Others (BillPay).",
    a_quien="Registrados sin crédito, ex clientes KPay con 12 meses sin compra y toda la base.",
    lecturas=[
        f"En septiembre las cinco gastaron {top.c9.sum()/1e6:.2f} M MXN de {T9/1e6:.2f} M ({100*top.c9.sum()/T9:.0f} %) entre {len(a)} campañas activas.",
        f"Ex clientes KPay: {R['B0333']['cpw']:,.0f} MXN por conversión por WhatsApp contra {R['B0333']['cpe']:.0f} por email.",
        "Con las lecturas del mes siguiente, el rescate Tasa 0 y el descuento a inactivos llegan a 60 % y salen de la lista.",
    ],
    causa="Se promueve a listas grandes por correo y WhatsApp, sin límite de gasto ni grupo sin mensajes.",
    sowhat="Rehacer estas cinco primero: a ex clientes por email o in-app, y WhatsApp solo a quien lo lee.",
    fuente=f"Fuente: Braze, envíos por campaña y canal, ene a sep 2026; {len(no)} campañas por canal debajo de lo mínimo. WhatsApp a 1.00 MXN por entregado; lectura con las del mes siguiente.",
    svg=S.out())
write(68, J)
