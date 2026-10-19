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
       "B0333": ("Oferta a ex clientes KPay con 12 meses sin compra", "Product Growth", "ex clientes (churn)"),
       "B0209": ("Descuento directo a clientes KCash inactivos", "Product Growth", "ex clientes inactivos"),
       "B0223": ("Crédito en plazos a quien nunca lo activó", "Product Growth", "registrados sin crédito")}
rows = []
for _, r in top.iterrows():
    k = [k for k in NOM if k in r.familia][0]
    f = e[e.fam == r.familia].groupby("canal").agg(costo=("costo", "sum"), conv=("conversiones_filas", "sum"), ws=("whatsapp_send", "sum"), wd=("whatsapp_delivery", "sum"), wr=("whatsapp_read", "sum"))
    cpc = (f.costo / f.conv).to_dict()
    w = f.loc["whatsapp"] if "whatsapp" in f.index else None
    rows.append(dict(k=k, nom=NOM[k][0], eq=NOM[k][1], aq=NOM[k][2], canal=r.canal, anual=r.costo_ent, sep=r.c9,
                     cpe=cpc.get("email"), cpw=cpc.get("whatsapp"), ent=100 * w.wd / w.ws if w is not None else None, lec=100 * w.wr / w.wd if w is not None else None))
    print(k, r.canal, round(r.costo_ent), round(r.c9), {kk: round(v, 1) for kk, v in cpc.items()}, rows[-1]["ent"], rows[-1]["lec"])
otras9 = T9 - top.c9.sum(); print("otras sep", otras9)

S = SVG("Cascada del gasto de septiembre en campañas promocionales que no responden lo mínimo: cinco campañas son la mitad; cuatro son WhatsApp")
S.legend([("WhatsApp", BLUE, "sq"), ("Email", MARK, "sq"), ("Resto de campañas", MARK2, "sq")], 0, 14, 18)
X0, X1, VM = 292, 520, 2.2e6
xs = lambda v: X0 + (X1 - X0) * v / VM
TOP, RH = 62, 40
S.t(0, TOP - 14, "Campaña · equipo · a quién va", 11, SEC, w=600)
S.t(X0, TOP - 14, "Gasto en septiembre, miles de MXN", 11, SEC, w=600)
S.t(612, TOP - 22, "MXN por conversión", 11, SEC, "middle", 600)
S.t(582, TOP - 8, "email", 11, SEC, "middle"); S.t(642, TOP - 8, "WhatsApp", 11, SEC, "middle")
S.t(728, TOP - 22, "WhatsApp", 11, SEC, "middle", 600); S.t(728, TOP - 8, "entregado · leído", 11, SEC, "middle")
run = 0
allrows = rows + [dict(nom=f"Otras {len(a) - sum(1 for r in rows if r['sep'] > 0)} campañas por canal", eq="", aq="que siguen activas", canal="otras", sep=otras9, anual=None)]
for i, r in enumerate(allrows):
    y = TOP + RH * i
    S.t(0, y + 10, r["nom"], 11.5, INK, w=600)
    S.t(0, y + 24, (r["eq"] + " · " if r["eq"] else "") + r["aq"], 10.5, SEC)
    col = BLUE if r["canal"] == "whatsapp" else (MARK if r["canal"] == "email" else MARK2)
    S.rect(xs(run), y + 4, xs(run + r["sep"]) - xs(run), 18, col)
    if i < len(allrows) - 1: S.line(xs(run + r["sep"]), y + 22, xs(run + r["sep"]), y + RH + 4, MARK, 1)
    S.t(xs(run + r["sep"]) + 5, y + 17, f"{r['sep']/1e3:,.0f}", 11, INK, w=600)
    run += r["sep"]
    if r.get("cpe"): S.t(582, y + 17, f"{r['cpe']:,.0f}", 11.5, TXT, "middle")
    if r.get("cpw"): S.t(642, y + 17, f"{r['cpw']:,.0f}", 11.5, BLUE, "middle", 700)
    if r.get("ent") and r["canal"] == "whatsapp": S.t(728, y + 17, f"{r['ent']:.0f} % · {r['lec']:.0f} %", 11.5, INK, "middle")
yT = TOP + RH * len(allrows)
S.line(0, yT - 6, 780, yT - 6, MARK)
S.rect(X0, yT + 2, xs(T9) - X0, 18, INK)
S.t(0, yT + 15, f"Total de septiembre: {len(a)} campañas por canal", 11.5, INK, w=700)
S.t(xs(T9) + 5, yT + 15, f"{T9/1e6:.2f} M MXN", 11.5, INK, w=700)
pct5 = 100 * top.c9.sum() / T9
S.t(0, yT + 40, f"Las cinco: {top.c9.sum()/1e6:.2f} M MXN en septiembre ({pct5:.0f} %) y {top.costo_ent.sum()/1e6:.1f} M MXN en el año ({100*top.costo_ent.sum()/TA:.0f} % de lo que no responde).", 11, BLUE, w=600)
S.t(0, yT + 58, "Conversión: solicitud o préstamo de KCash en 7 días; en campañas de KPay no mide la compra en KPay.", 10.5, SEC)
R = {r["k"]: r for r in rows}
J = dict(
    titulo=f"Cinco campañas son la mitad de lo que gastamos en septiembre en mensajes que no responden; cuatro son WhatsApp para recuperar a quien se fue o nunca empezó",
    que="Promociones para recuperar: Tasa 0 a leads rezagados, oferta a ex clientes KPay con 12 meses sin compra, descuento directo a clientes KCash inactivos, crédito en plazos a quien nunca lo activó y Tasa 0 por correo a registrados de KPay.",
    quien="Marketing (rescate Tasa 0 a leads rezagados) y Product Growth (las otras cuatro).",
    a_quien="Leads que no terminaron su registro y quedaron rezagados; ex clientes KPay con 12 meses sin compra; clientes KCash inactivos; registrados que nunca tomaron crédito.",
    lecturas=[
        f"Cuatro de las cinco van por WhatsApp a gente que se fue o nunca empezó: de cada 10 WhatsApp se entregan entre {min(r['ent'] for r in rows if r['ent'])/10:.0f} y {max(r['ent'] for r in rows if r['ent'])/10:.0f}, y de lo entregado se lee {min(r['lec'] for r in rows if r['lec']):.0f} a {max(r['lec'] for r in rows if r['lec'] and r['canal']=='whatsapp'):.0f} %, alrededor del mínimo de 6 de cada 10.",
        f"En la misma campaña el correo cuesta mucho menos por conversión: descuento a inactivos {R['B0209']['cpe']:.0f} MXN por email contra {R['B0209']['cpw']:.0f} por WhatsApp; ex clientes KPay {R['B0333']['cpe']:.0f} contra {R['B0333']['cpw']:,.0f}; rescate Tasa 0 {R['B0171']['cpe']:.0f} contra {R['B0171']['cpw']:.0f}.",
        f"En el año, las cinco suman {top.costo_ent.sum()/1e6:.1f} M MXN, {100*top.costo_ent.sum()/TA:.0f} % de los {TA/1e6:.1f} M MXN que se gastaron en campañas que no responden lo mínimo.",
    ],
    causa="Son programas para recuperar clientes que se mandan a toda la lista por WhatsApp, el canal más caro, sin límite de gasto ni un grupo sin mensajes que diga si de verdad recuperan.",
    sowhat="Recuperarlos sí, pero no por WhatsApp a toda la lista: primero email o in-app, WhatsApp solo a quien leyó uno en 90 días, con presupuesto con límite y un grupo sin mensajes.",
    fuente=f"Fuente: Braze, envíos por campaña, canal y mes, enero a septiembre 2026. No responde lo mínimo: menos de 3 clics por mil correos o 6 de cada 10 WhatsApp leídos, con envíos iguales o mayores a la mediana del canal. WhatsApp a 1.00 MXN por entregado; email a 0.05 por enviado. Lectura en la gráfica incluye las registradas el mes siguiente; con ellas, el rescate Tasa 0 y el descuento a inactivos quedan en 62 y 63 %, apenas arriba del mínimo (la clasificación usó solo las del mes del envío). Conversión de referencia: solicitud o préstamo en 7 días.",
    svg=S.out())
write(68, J)
