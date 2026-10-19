"""Lámina 77: matriz de ocho malas prácticas por equipo (millones de mensajes), con qué se hace mal, quién lo hace más,
con qué campaña y por qué cuesta. Las prácticas se traslapan: no se suman.
Fuentes: E1 (envíos, costo, respuesta), E2 (versiones y ticket), E7a (etapa del usuario: tarjeta KPay congelada, lista negra, REUS o ARCO),
E15 (pasos de Canvas), regla insisten() de b7.py."""
from b7 import *

e = load_e1(); e["tema"] = e.communication_name.map(tema)
promo = ~e.tema.isin(["Cobranza", "Transaccional"])
P = {}
def put(k, df):
    t = df.groupby("equipo").agg(msgs=("envios", "sum"), mxn=("costo", "sum"))
    top = df.groupby("fam").agg(msgs=("envios", "sum"), mxn=("costo", "sum"), eq=("equipo", "first")).sort_values("msgs", ascending=False)
    P[k] = dict(t=t, top=top, msgs=df.envios.sum(), mxn=df.costo.sum())
put("masivo", e[promo & (e.usuarios_aprox >= 1_000_000)])
R = insisten(e); RI = R[~R.tema.isin(["Cobranza", "Transaccional"]) & (R.after > 0)]
put("insiste", RI.rename(columns={"after": "envios", "acost": "costo"}))
w = e[e.canal == "whatsapp"].groupby("fam").agg(d=("whatsapp_delivery", "sum"), r=("whatsapp_read", "sum"), equipo=("equipo", "first"), envios=("envios", "sum"), costo=("costo", "sum"))
w = w[(w.d >= 20000) & (100 * w.r / w.d < 60)].reset_index(); put("wa", w)
c2 = pd.read_csv(D + "e2_catalogo.csv", low_memory=False); c2["fam"] = c2.nombre.fillna("").map(fam_of); c2["fs"] = pd.to_datetime(c2.first_sent, errors="coerce")
vv = c2[(c2.fs >= "2026-01-01") & (c2.fs < "2026-10-01")].groupby("fam").communication_id.nunique(); F5 = set(vv[vv >= 5].index)
put("copiar", e[e.fam.isin(F5)])
pat = r"(?i)prueba|test|\bqa\b|qa_|copy of|copia|dummy|demo"
put("pruebas", e[e.communication_name.str.contains(pat)])
a = pd.read_csv(D + "e7a_familia_canal_etapa.csv"); a["familia"] = a.familia.fillna(""); a["fam"] = a.familia.map(fam_of); a["tema"] = a.familia.map(tema); a["equipo"] = a.equipo.fillna("").map(team_of)
a = a[a.etapa.isin(["3.Blacklist", "4.Kpay CC Freeze", "6.Reus or Arco"]) & ~a.tema.isin(["Cobranza", "Transaccional"])].copy()
wd = e[e.canal == "whatsapp"].groupby("fam").apply(lambda g: g.whatsapp_delivery.sum() / max(1, g.whatsapp_send.sum()), include_groups=False)
a["costo"] = np.where(a.canal == "whatsapp", a.envios * a.fam.map(wd).fillna(0.75), np.where(a.canal == "email", 0.05 * a.envios, 0))
put("bloq", a)
s = pd.read_csv(D + "e15_embudo_pasos.csv", low_memory=False); pc = s.groupby("canvas_id").canvas_step_id.nunique(); ids = set(pc[pc > 20].index)
put("largos", e[e.communication_id.isin(ids)])
c2["sin"] = c2.tiene_ticket.astype(str) != "1"; st = set(c2[c2.sin].communication_id)
put("ticket", e[e.communication_id.isin(st) & promo])
# datos del "por qué"
bp = e[e.fam.str.contains("BillPay_Intro") & (e.canal == "email")]; bp_cpm = 1000 * bp.email_click.sum() / bp.email_delivery.sum(); bp_uns = bp.email_unsubscribe.sum()
b211 = RI[RI.fam.str.contains("B0211-CANVAS-Nuevos_RegistradosPay") & (RI.canal == "email")].iloc[0]
b333 = e[e.fam == "Lending-KPay-B0333-CANVAS-Churn_12MesesInactividad-ConSinOferta-N/A"].groupby("canal").agg(c=("costo", "sum"), v=("conversiones_fraccional", "sum"))
b333w, b333e = b333.loc["whatsapp", "c"] / b333.loc["whatsapp", "v"], b333.loc["email", "c"] / b333.loc["email", "v"]
qa = e[e.fam.str.startswith("QA-KPay-B001")]; qa_o = 1000 * qa.pn_open.sum() / qa.pn_send.sum()
r326 = a[a.fam.str.contains("B0326-Canvas-Recurrentes_Dormants")]
ab = a.groupby("etapa").envios.sum()
print({k: (round(v["msgs"] / 1e6, 1), round(v["mxn"] / 1e6, 2)) for k, v in P.items()})
print(bp_cpm, bp_uns, b211.fail, b211.frate, b211.after, b333w, b333e, qa_o, qa.envios.sum(), r326.envios.sum(), ab.to_dict(), vv.max())
import math
NAMES = [
 ("masivo", "A más de un millón al mes", "BillPay a toda la base", f"{bp_cpm:.0f} clic por mil y {bp_uns/1e3:.0f} mil bajas"),
 ("insiste", "Seguir con lo que no responde", "Tasa 0 a registrados sin crédito", f"debajo desde febrero; {b211.after/1e6:.0f} M correos más"),
 ("wa", "WhatsApp a quien no lo lee", "Ex clientes KPay, 12 meses", f"{b333w:,.0f} MXN por conversión contra {b333e:.0f} por email"),
 ("copiar", "Copiar en vez de medir", "Rescate Tasa 0 a leads rezagados", f"{vv.get('Marketing-KCash-B0171-CANVAS-Leads_BBDDRezagada-RescateTasa0-N/A', 0)} versiones; la vieja sigue enviando"),
 ("pruebas", "Pruebas y copias a clientes", "QA-KPay recordatorio", f"{qa.envios.sum()/1e6:.1f} M push, {qa_o:.1f} aperturas por mil"),
 ("bloq", "Promociones a bloqueados", "Referidos a ex clientes KPay", f"{ab.get('4.Kpay CC Freeze',0)/1e6:.0f} M a tarjetas congeladas"),
 ("largos", "Canvas de más de 20 pasos", "Recuperación KPay, Cuesta de Enero", "hasta 120 mensajes distintos"),
 ("ticket", "Promociones sin ticket ni dueño", "BillPay y Shopping semanal", "nadie las revisa ni las apaga"),
]
S = SVG("Ocho malas prácticas: cada punto es una campaña en esa práctica según sus mensajes; en azul las del equipo que más pesa")
S.legend([("Campaña del equipo que más pesa en la práctica", BLUE, "ci"), ("Campaña de otro equipo", MARK2, "ci")], 0, 14, 16)
X0, X1 = 196, 500
L0, L1 = math.log10(1e4), math.log10(5e7)
xs = lambda v: X0 + (X1 - X0) * (math.log10(min(max(v, 1e4), 5e7)) - L0) / (L1 - L0)
TOP, RH = 62, 45
Yb = TOP + RH * len(NAMES) - 14
S.t((X0 + X1) / 2, 34, "Mensajes de cada campaña (escala que multiplica)", 10.5, SEC, "middle", 600)
for v, l in ((1e4, "10 mil"), (1e5, "100 mil"), (1e6, "1 M"), (1e7, "10 M")):
    S.line(xs(v), TOP - 12, xs(v), Yb, GRID); S.t(xs(v), TOP - 16, l, 10.5, SEC, "middle")
S.t(0, TOP - 16, "Qué se hace mal", 10.5, SEC, w=600)
S.t(516, TOP - 16, "Quién más pesa · peor caso · por qué", 10.5, SEC, w=600)
for i, (k, que, caso, porque) in enumerate(NAMES):
    yc = TOP + RH * i + 8
    t = P[k]["t"].msgs; lead = t.idxmax(); tp = P[k]["top"]
    S.t(0, yc + 2, f"{i+1}. {que}", 11, INK, w=700)
    S.t(0, yc + 16, f"{P[k]['msgs']/1e6:.0f} M mensajes · {P[k]['mxn']/1e6:.1f} M MXN", 10.5, SEC)
    d = tp[tp.msgs > 0]
    for j, (f, r) in enumerate(d.sort_values("msgs").iterrows()):
        jy = ((j * 7) % 9 - 4) * 2.2
        S.circle(xs(r.msgs), yc + 6 + jy, 2.8, BLUE if r["eq"] == lead else MARK2, "#FFFFFF", 0.5, ' fill-opacity="0.85"')
    w0 = d.iloc[0]
    S.circle(xs(w0.msgs), yc + 6, 5, BLUE if w0["eq"] == lead else MARK, "#FFFFFF", 1.4)
    S.tspans(516, yc - 4, [(f"{lead} {t.max()/1e6:.0f} M", BLUE, 700), (f" de {P[k]['msgs']/1e6:.0f} M", SEC, 400)], 11)
    S.t(516, yc + 9, caso, 10.5, INK, w=600)
    S.t(516, yc + 22, porque, 10.5, TXT)
    if i < len(NAMES) - 1: S.line(0, yc + 29, 780, yc + 29, GRID)
J = dict(
    titulo="Ocho hábitos cuestan dinero y clientes; Product Growth y Marketing encabezan cinco de ellos",
    que="Promociones en las ocho prácticas; cobranza y avisos de pago no se cuentan.",
    quien="Product Growth y Marketing encabezan cinco; Others, las otras tres.",
    a_quien="Leads, registrados sin crédito, ex clientes, toda la base y bloqueados.",
    lecturas=[
        f"Seguir con lo que no responde: {P['insiste']['msgs']/1e6:.0f} M mensajes y {P['insiste']['mxn']/1e6:.1f} M MXN; Product Growth pone la mitad.",
        f"WhatsApp a quien no lo lee: {P['wa']['msgs']/1e6:.0f} M mensajes pero {P['wa']['mxn']/1e6:.1f} M MXN, casi todo de Product Growth.",
        f"Others encabeza envíos a toda la base, pruebas y promociones sin ticket, sobre todo BillPay.",
    ],
    causa="Nadie revisa respuesta contra volumen por campaña, y las reglas de envío no existen o no se cumplen.",
    sowhat="No es una campaña mala: son hábitos que se repiten en los mismos equipos y tienen dueño.",
    fuente="Fuente: Braze, envíos, catálogo, etapa del usuario (golden dataset) y pasos de Canvas, ene a sep 2026. Las prácticas se traslapan: no se suman. WhatsApp a 1.00 MXN por entregado.",
    svg=S.out())
write(77, J)
