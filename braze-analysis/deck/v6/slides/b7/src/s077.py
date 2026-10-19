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
b333 = e[e.fam == "Lending-KPay-B0333-CANVAS-Churn_12MesesInactividad-ConSinOferta-N/A"].groupby("canal").agg(c=("costo", "sum"), v=("conversiones_filas", "sum"))
b333w, b333e = b333.loc["whatsapp", "c"] / b333.loc["whatsapp", "v"], b333.loc["email", "c"] / b333.loc["email", "v"]
qa = e[e.fam.str.startswith("QA-KPay-B001")]; qa_o = 1000 * qa.pn_open.sum() / qa.pn_send.sum()
r326 = a[a.fam.str.contains("B0326-Canvas-Recurrentes_Dormants")]
ab = a.groupby("etapa").envios.sum()
print({k: (round(v["msgs"] / 1e6, 1), round(v["mxn"] / 1e6, 2)) for k, v in P.items()})
print(bp_cpm, bp_uns, b211.fail, b211.frate, b211.after, b333w, b333e, qa_o, qa.envios.sum(), r326.envios.sum(), ab.to_dict(), vv.max())
TEAMC = ["Product Growth", "Marketing", "Sales", "Others", "Collections"]
TL = {"Product Growth": "Product Growth", "Marketing": "Marketing", "Sales": "Sales", "Others": "Others", "Collections": "Collec&shy;tions"}
NAMES = [
 ("masivo", "Mandar la misma promoción a más de un millón de personas al mes", "Lanzamiento de BillPay a toda la base", f"{bp_cpm:.0f} clic por mil correos y {bp_uns/1e3:.0f} mil bajas"),
 ("insiste", "Seguir mandando lo que ya no respondió lo mínimo", "Tasa 0 a registrados de KPay sin crédito", f"Debajo de lo mínimo desde febrero y {b211.after/1e6:.0f} M correos más"),
 ("wa", "Mandar WhatsApp (1 MXN cada uno) a quien no lo lee", "Oferta a ex clientes KPay, 12 meses sin compra", f"{b333w:,.0f} MXN por conversión contra {b333e:.0f} por correo"),
 ("copiar", "Copiar la campaña cada mes en vez de medir la anterior", f"Tasa 0 a quien nunca usó KCash ({vv.max()} versiones)", "La copia vieja sigue enviando; nadie sabe cuál funciona"),
 ("pruebas", "Probar con clientes o dejar copias con nombre de prueba", "Recordatorio de registro QA-KPay", f"{qa.envios.sum()/1e6:.1f} M push con {qa_o:.1f} aperturas por mil"),
 ("bloq", "Promociones a tarjeta KPay congelada, lista negra o a quien pidió no recibir", "Referidos a ex clientes de KPay", f"{ab.get('4.Kpay CC Freeze',0)/1e6:.0f} M a tarjetas que no pueden comprar; riesgo legal"),
 ("largos", "Canvas de más de 20 pasos, una rama por oferta y canal", "Recuperación de ex clientes KPay y Cuesta de Enero", "Hasta 120 mensajes distintos; la mitad del push bajo lo mínimo"),
 ("ticket", "Promociones sin ticket, sin un dueño que responda", "BillPay y recomendaciones semanales de Shopping", "Nadie las revisa ni las apaga"),
]
fm = lambda v: "" if v < 0.05e6 else f"{v/1e6:.1f} M"
rows = []
for i, (k, que, quien, porque) in enumerate(NAMES, 1):
    t = P[k]["t"].msgs; lead = t.idxmax()
    cells = "".join(f'<td class="num" style="{"background:#1F4FD8;color:#FFFFFF;font-weight:700" if tm == lead else "color:#3B4556"}">{fm(t.get(tm, 0))}</td>' for tm in TEAMC)
    rows.append(f'<tr><td style="width:25%"><b>{i}.</b> {que}</td><td class="num" style="width:12%;white-space:nowrap"><b>{P[k]["msgs"]/1e6:.0f} M</b> · {P[k]["mxn"]/1e6:.1f} M MXN</td>{cells}'
                f'<td style="width:18%">{quien}</td><td style="width:20%;color:#3B4556">{porque}</td></tr>')
html = ('<table style="font-size:.9cqi"><tr><th>Qué se hace mal</th><th class="num">Mensajes · gasto</th>' + "".join(f'<th class="num" style="width:5%">{TL[tm]}</th>' for tm in TEAMC) +
        '<th>Campaña que más pesa</th><th>Por qué cuesta</th></tr>' + "".join(rows) + '</table>'
        '')
J = dict(
    kind="html", ancho_completo=True,
    titulo="Ocho hábitos que cuestan dinero y clientes: Product Growth y Marketing encabezan cinco, y Others los envíos a toda la base, las pruebas y lo que no tiene dueño",
    que="Promociones en las ocho prácticas; cobranza y avisos de pago no se cuentan.",
    quien="Product Growth en insistir, WhatsApp que no se lee y Canvas largos; Marketing en copiar y en promociones a bloqueados; Others en envíos a toda la base, pruebas y sin ticket.",
    a_quien="Leads, registrados sin crédito, ex clientes inactivos, toda la base y gente que no puede o no quiere recibir promociones.",
    sowhat="No es una campaña mala: son hábitos que se repiten en los mismos equipos, y cada uno tiene un dueño que puede corregirlo.",
    fuente="Celdas: millones de mensajes de cada equipo; en azul, el que más pesa. Las prácticas se traslapan: no se suman. Fuente: Braze, envíos por comunicación, mes y canal, catálogo, etapa del usuario (golden dataset, 37 % de los envíos) y pasos de Canvas, enero a septiembre 2026. WhatsApp a 1.00 MXN por entregado; email a 0.05 por enviado.",
    html=html)
write(77, J)
