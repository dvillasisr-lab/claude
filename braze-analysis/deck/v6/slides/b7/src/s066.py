"""Lámina 66: campañas que no responden lo mínimo, por tema y equipo (burbujas), con lo que sigue enviando en septiembre y el gasto.
Fuente: hallazgos/muestra_c_familias.csv (señal por campaña y canal) con WhatsApp por entregado; E1 para septiembre."""
from b7 import *

c = load_c(); e = load_e1()
TOT, TOTC = c.envios.sum(), c.costo_ent.sum()
seg = c.groupby(c.senal.fillna("normal")).agg(env=("envios", "sum"), costo=("costo_ent", "sum"), n=("familia", "size"))
a = c[c.senal == "apagar o rehacer"]
p = a[a.tipo == "promocional o lifecycle"].copy()
# septiembre (E1) de las promocionales activas
s9 = e[e.m == 9].groupby(["fam", "canal"]).agg(env9=("envios", "sum"), c9=("costo", "sum")).reset_index()
pa = p[p.activo_sep == 1].merge(s9, left_on=["familia", "canal"], right_on=["fam", "canal"], how="left")
print("no responde", seg.loc["apagar o rehacer"].to_dict(), "promo", len(p), p.envios.sum() / 1e6, p.costo_ent.sum() / 1e6)
print("activas sep", len(pa), pa.env9.sum() / 1e6, pa.c9.sum() / 1e6, "volumen anual activas", pa.envios.sum() / 1e6)
eq = p.groupby("equipo").agg(env=("envios", "sum"), c=("costo_ent", "sum")); eq["pe"] = 100 * eq.env / eq.env.sum(); eq["pc"] = 100 * eq.c / eq.c.sum(); print(eq)
et = p.groupby("etapa").agg(env=("envios", "sum"), c=("costo_ent", "sum")); et["pe"] = 100 * et.env / et.env.sum(); et["pc"] = 100 * et.c / et.c.sum(); print(et)

GR = {"Tasa 0": "Tasa 0", "Promociones de comercios KPay": "Promociones de comercios KPay", "Referidos": "Referidos (invita a un amigo)",
      "BillPay y recargas": "Lanzamiento de BillPay y recargas", "Oferta para volver": "Ofertas para que vuelva el ex cliente",
      "Uso y recompra del crédito": "Crédito en plazos y recompra", "Fechas y temporadas": "Fechas, temporadas y sorteos",
      "Sorteos y concursos": "Fechas, temporadas y sorteos", "Novedades y recomendaciones": "Novedades y recomendaciones"}
p["g"] = p.tema.map(GR).fillna("Otros temas")
ROWS = list(p.groupby("g").envios.sum().sort_values(ascending=False).index)
ROWS = [r for r in ROWS if r != "Otros temas"] + ["Otros temas"]
COLS = ["Marketing", "Product Growth", "Sales", "Others"]
tot = p.groupby(["g", "equipo"]).envios.sum(); act = p[p.activo_sep == 1].groupby(["g", "equipo"]).envios.sum()
rg = p.groupby("g").agg(env=("envios", "sum"), c=("costo_ent", "sum")); rga = p[p.activo_sep == 1].groupby("g").envios.sum()
print(rg.assign(act=rga).div(1e6).round(2))

S = SVG("Mensajes de campañas promocionales que no responden lo mínimo, por tema y equipo, con la parte que sigue enviando en septiembre y el gasto en MXN por tema")
# franja superior: los 667 M por respuesta
S.t(0, 13, f"Los {TOT/1e6:.0f} M mensajes del año según cuánto responde la campaña que los mandó", 12, INK, w=600)
SEGS = [("apagar o rehacer", "No responde lo mínimo y manda mucho", BLUE), ("revisar", "Responde poco o con bajas", BLUEL),
        ("normal", "Responde normal", MARK2), ("proteger", "Responde bien", GREEN), ("escalar", "", GREENL)]
X0, X1 = 0, 780; x = X0
for k, lab, col in SEGS:
    w = (X1 - X0) * seg.loc[k, "env"] / TOT
    S.rect(x, 22, w - 1.5, 16, col)
    if k == "apagar o rehacer":
        S.t(x + 6, 34, f"{seg.loc[k,'env']/1e6:.0f} M mensajes ({100*seg.loc[k,'env']/TOT:.0f} %) y {seg.loc[k,'costo']/1e6:.1f} M MXN", 11.5, "#FFFFFF", w=600)
    if lab:
        S.t(x, 52, lab if k != "apagar o rehacer" else "", 10.5, SEC)
        if k != "apagar o rehacer": S.t(x, 65, f"{seg.loc[k,'env']/1e6:.0f} M", 10.5, INK, w=600)
    x += w
S.t(0, 52, "Abajo, solo esta parte, sin cobranza ni avisos:", 10.5, BLUE, w=600)
S.t(0, 65, f"{len(p)} campañas promocionales, {p.envios.sum()/1e6:.0f} M mensajes", 10.5, INK, w=600)

# matriz
TOP, RH = 116, 29.5; CX = {k: 272 + 84 * i for i, k in enumerate(COLS)}
RMAX, VMAX = 14.5, 45e6
r_of = lambda v: RMAX * (v / VMAX) ** 0.5
S.t(0, TOP - 26, "Tema de la campaña", 11, SEC, w=600)
for k in COLS:
    S.t(CX[k], TOP - 26, k, 11, INK, "middle", 600)
BX0, BX1, BV = 612, 708, 7e6
S.t(BX0, TOP - 26, "M MXN en el año", 11, SEC, w=600)
S.t(780, TOP - 26, "Sigue en sep.", 11, SEC, "end", 600)
for i, g in enumerate(ROWS):
    y = TOP + RH * i
    hi = g in ("Tasa 0", "Promociones de comercios KPay", "Referidos (invita a un amigo)")
    S.line(0, y + RH / 2, 780, y + RH / 2, GRID)
    S.t(0, y + 4, g, 11.5, INK if hi else TXT, w=600 if hi else 400)
    for k in COLS:
        v = tot.get((g, k), 0); va = act.get((g, k), 0)
        if v < 0.05e6: continue
        S.circle(CX[k], y, r_of(v), BLUEL, sw=0)
        if va > 0.05e6: S.circle(CX[k], y, r_of(va), BLUE, sw=0)
        if v >= 4e6: S.t(CX[k] + r_of(v) + 4, y + 4, f"{v/1e6:.0f}", 11, INK, w=600 if hi else 400, halo=True)
    cv = rg.loc[g, "c"]
    S.rect(BX0, y - 6, (BX1 - BX0) * cv / BV, 12, BLUE if hi or g.startswith("Ofertas") else MARK)
    S.t(BX0 + (BX1 - BX0) * cv / BV + 5, y + 4, f"{cv/1e6:.1f}", 11, INK, w=600 if hi else 400)
    S.t(780, y + 4, f"{100*rga.get(g,0)/rg.loc[g,'env']:.0f} %", 11, INK if hi else SEC, "end", 600 if hi else 400)
# leyenda de burbujas
yl = TOP + RH * len(ROWS) - 2
S.circle(6, yl, 6, BLUEL, sw=0); S.t(17, yl + 4, "Millones de mensajes en el año (número junto a la burbuja)", 10.5, TXT)
S.circle(336, yl, 6, BLUE, sw=0); S.t(347, yl + 4, "Parte de campañas que siguen enviando en septiembre", 10.5, TXT)
J = dict(
    titulo="Casi la mitad de los mensajes del año salió de campañas que casi nadie responde: Tasa 0, promociones de comercios y referidos",
    que=f"Promociones: Tasa 0 de KCash ({rg.loc['Tasa 0','env']/1e6:.0f} M mensajes), promociones de comercios KPay ({rg.loc['Promociones de comercios KPay','env']/1e6:.0f} M), referidos ({rg.loc['Referidos (invita a un amigo)','env']/1e6:.0f} M), lanzamiento de BillPay ({rg.loc['Lanzamiento de BillPay y recargas','env']/1e6:.0f} M) y ofertas para que vuelva el ex cliente ({rg.loc['Ofertas para que vuelva el ex cliente','env']/1e6:.0f} M).",
    quien=f"Marketing {eq.loc['Marketing','env']/1e6:.0f} M mensajes ({eq.loc['Marketing','pe']:.0f} %) y Product Growth {eq.loc['Product Growth','env']/1e6:.0f} M ({eq.loc['Product Growth','pe']:.0f} %, pero {eq.loc['Product Growth','pc']:.0f} % del dinero). Others {eq.loc['Others','env']/1e6:.0f} M (BillPay y Shopping) y Sales {eq.loc['Sales','env']/1e6:.0f} M.",
    a_quien=f"Leads que no terminaron su registro ({et.loc['Leads (no terminaron registro)','env']/1e6:.0f} M), registrados que nunca tomaron crédito ({et.loc['Registrados sin crédito o nuevos','env']/1e6:.0f} M), ex clientes inactivos ({et.loc['Ex clientes inactivos','env']/1e6:.0f} M, {et.loc['Ex clientes inactivos','pc']:.0f} % del dinero) y envíos a todos sin segmento ({et.loc['Todos (sin segmento)','env']/1e6:.0f} M).",
    lecturas=[
        f"Tasa 0 es el tema más grande: {rg.loc['Tasa 0','env']/1e6:.0f} M mensajes y {rg.loc['Tasa 0','c']/1e6:.1f} M MXN, y {100*rga['Tasa 0']/rg.loc['Tasa 0','env']:.0f} % sale de campañas que siguen enviando en septiembre. Lo mandan Product Growth ({tot[('Tasa 0','Product Growth')]/1e6:.0f} M) y Marketing ({tot[('Tasa 0','Marketing')]/1e6:.0f} M).",
        f"Promociones de comercios KPay se reparten entre Marketing ({tot[('Promociones de comercios KPay','Marketing')]/1e6:.0f} M) y Sales ({tot[('Promociones de comercios KPay','Sales')]/1e6:.0f} M); referidos es todo de Marketing. BillPay (Others) ya casi se detuvo.",
        f"Las ofertas para que vuelva el ex cliente son pocos mensajes ({rg.loc['Ofertas para que vuelva el ex cliente','env']/1e6:.0f} M) pero {rg.loc['Ofertas para que vuelva el ex cliente','c']/1e6:.1f} M MXN, porque van por WhatsApp. A ellos se les sigue escribiendo para recuperarlos, por un canal más barato.",
    ],
    causa=f"Las promociones se lanzan a listas grandes (leads, registrados sin crédito, toda la base) y nadie revisa si responden: {len(pa)} de estas campañas por canal seguían enviando en septiembre, {pa.env9.sum()/1e6:.0f} M mensajes y {pa.c9.sum()/1e6:.1f} M MXN ese mes.",
    sowhat="El desperdicio no está repartido: está en cinco temas, sobre todo de Marketing y Product Growth, dirigidos a gente que todavía no es cliente o que ya se fue.",
    fuente=f"Fuente: Braze, envíos por campaña y canal, enero a septiembre 2026 (1,918 campañas por canal). No responde lo mínimo y manda mucho: menos de 3 clics por mil correos, 7.5 aperturas por mil push, 6 de cada 10 WhatsApp leídos o 1 de cada 10 in-app, con envíos iguales o mayores a la mediana de su canal. Responde bien: 1.5 veces la campaña típica de su canal o más. Tema por el nombre de la campaña. WhatsApp a 1.00 MXN por entregado, email a 0.05 por enviado.",
    svg=S.out())
write(66, J)
