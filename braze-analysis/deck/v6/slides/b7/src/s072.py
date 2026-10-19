"""Lámina 72: cada correo (versión de una campaña) con 200 mil o más entregados, por tema: clics por cada mil correos (escala logarítmica),
tamaño = correos; en verde los que responden bien (15 clics por mil o más). Columna: cuántos responden bien por tema. Fuente: E1 por communication_id."""
import math
from b7 import *

e = load_e1()
x = e[e.canal == "email"].groupby("communication_id").agg(name=("communication_name", "first"), base=("email_delivery", "sum"), resp=("email_click", "sum"), equipo=("equipo", "first"))
x = x[x.base >= 200000].copy(); x["cpm"] = 1000 * x.resp / x.base; x["tema"] = x.name.map(tema)
GOOD, MINE = 15, 3
x["good"] = x.cpm >= GOOD
REN = {"Otro": "Otros temas", "Prueba o copia": "Otros temas", "Venta cruzada KPay y KCash": "Otros temas", "BillPay y recargas": "Otros temas",
       "Transaccional": "Avisos de pago y de cuenta", "Uso y recompra del crédito": "Crédito en plazos y recompra", "Oferta para volver": "Ofertas para que vuelva el ex cliente",
       "Novedades y recomendaciones": "Boletines y recomendaciones"}
x["g"] = x.tema.map(lambda t: REN.get(t, t))
g = x.groupby("g").agg(n=("cpm", "size"), b=("good", "sum"), vol=("base", "sum")); g["p"] = g.b / g.n
g = g.sort_values(["p", "n"], ascending=[False, True])
x["band"] = pd.cut(x.base, [2e5, 5e5, 1e6, 3e6, 1e9], labels=["200 a 500 mil", "0.5 a 1 M", "1 a 3 M", "más de 3 M"])
bd = x.groupby("band", observed=True).agg(n=("cpm", "size"), b=("good", "sum"))
eqg = x.groupby("equipo").agg(n=("cpm", "size"), b=("good", "sum"))
print(len(x), x.good.sum(), (x.cpm >= MINE).sum()); print(g); print(bd); print(eqg)
below = x[x.cpm < MINE]
print("debajo del mínimo: volumen", below.base.sum() / x.base.sum(), "clics", below.resp.sum() / x.resp.sum())
S = SVG("Cada correo grande por tema según sus clics por cada mil correos; en verde los que responden bien")
S.legend([("Responde bien: 15 clics por mil o más", GREEN, "ci"), ("Responde menos", MARK, "ci")], 0, 14, 18)
S.t(780, 14, "El tamaño del punto es el número de correos", 10.5, SEC, "end")
X0, X1 = 232, 650
L0, L1 = math.log10(0.1), math.log10(200)
xs = lambda v: X0 + (X1 - X0) * (math.log10(max(v, 0.1)) - L0) / (L1 - L0)
TOP, RH = 58, 25
rows = list(g.index)
Yb = TOP + RH * len(rows) - 8
for v, l in ((0.1, "0.1"), (1, "1"), (3, "3"), (10, "10"), (15, ""), (30, "30"), (100, "100")):
    if l: S.t(xs(v), Yb + 16, l, 11, SEC, "middle")
S.line(xs(MINE), TOP - 14, xs(MINE), Yb, INK, 1, ' stroke-dasharray="4 4" opacity="0.6"')
S.line(xs(GOOD), TOP - 14, xs(GOOD), Yb, GREEN, 1.5)
S.t(xs(MINE) - 4, TOP - 18, "Mínimo aceptable: 3", 10.5, INK, "end")
S.t(xs(GOOD) + 4, TOP - 18, "Responde bien: 15", 10.5, GREEN, "start", 600)
S.t(X1, Yb + 32, "Clics por cada mil correos (escala que multiplica)", 11, SEC, "end")
S.t(780, TOP - 18, "Responden bien", 11, SEC, "end", 600)
for i, k in enumerate(rows):
    y = TOP + RH * i
    hi = g.loc[k, "p"] >= 0.3
    S.line(0, y + RH / 2 - 1, 780, y + RH / 2 - 1, GRID)
    S.t(0, y + 4, k, 11.5, INK if hi else TXT, w=600 if hi else 400)
    d = x[x.g == k].sort_values("base", ascending=False)
    for j, (_, q) in enumerate(d.iterrows()):
        jy = ((j * 7) % 11 - 5) * 0.9
        S.circle(xs(q.cpm), y + jy, 2 + 6 * (q.base / 10e6) ** 0.5, GREEN if q.good else MARK, "#FFFFFF", 0.8, ' fill-opacity="0.85"')
    S.t(780, y + 4, f"{int(g.loc[k,'b'])} de {int(g.loc[k,'n'])}", 11.5, GREEN if hi else SEC, "end", 700 if hi else 400)
yy = Yb + 52
S.tspans(0, yy, [("Responden bien, según el tamaño del envío: ", INK, 600), ("; ".join(f"{b} correos, {100*q.b/q.n:.0f} %" if i == 0 else f"{b}, {100*q.b/q.n:.0f} %" for i, (b, q) in enumerate(bd.iterrows())), TXT, 400)], 11)
J = dict(
    titulo="Solo uno de cada ocho correos grandes responde bien, sobre todo recordatorios, cobranza y avisos de pago: los separa el tema, no el tamaño",
    que=f"Todo el email con volumen: {len(x)} correos de 200 mil entregados o más (cada versión de una campaña con su fecha).",
    quien=f"Responden bien: Others (avisos) {int(eqg.loc['Others','b'])} de {int(eqg.loc['Others','n'])}, Collections {int(eqg.loc['Collections','b'])} de {int(eqg.loc['Collections','n'])}, Marketing {int(eqg.loc['Marketing','b'])} de {int(eqg.loc['Marketing','n'])}, Product Growth {int(eqg.loc['Product Growth','b'])} de {int(eqg.loc['Product Growth','n'])} y Sales {int(eqg.loc['Sales','b'])} de {int(eqg.loc['Sales','n'])}.",
    a_quien="Los que responden bien van a quien está a la mitad de algo: empezó su registro, tiene un pago por vencer o acaba de pagar. Los que no, a listas de leads, registrados o clientes de KPay.",
    lecturas=[
        f"{int(x.good.sum())} de {len(x)} correos responden bien (15 clics por mil o más). Los diez recordatorios de registro lo logran; de {int(g.loc['Promociones de comercios KPay','n'])} promociones de comercios KPay y {int(g.loc['Referidos','n'])} de referidos, ninguno.",
        f"El tamaño no lo explica: responden bien {100*bd.iloc[0].b/bd.iloc[0].n:.0f} % de los de 200 a 500 mil correos y {100*bd.iloc[-1].b/bd.iloc[-1].n:.0f} % de los de más de 3 M. Achicar la lista no basta.",
        f"{len(x)-int((x.cpm>=MINE).sum())} correos ni siquiera llegan a lo mínimo aceptable (3 clics por mil): son {100*below.base.sum()/x.base.sum():.0f} % de estos correos y {100*below.resp.sum()/x.resp.sum():.0f} % de sus clics.",
    ],
    causa="La gente abre el correo que tiene que ver con algo que está haciendo; la promoción que le llega porque está en una lista la ignora, sea la lista chica o grande.",
    sowhat="Para que un correo responda no hay que hacerlo más chico: hay que mandarlo por una razón de la persona.",
    fuente="Fuente: Braze, envíos por comunicación, mes y canal, enero a septiembre 2026; versiones de email con 200 mil correos entregados o más. Clics sobre correos entregados. Tema por el nombre de la campaña. Responde bien = 15 clics por mil, cinco veces lo mínimo aceptable.",
    svg=S.out())
write(72, J)
