"""Lámina 69 (pequeños múltiplos): programa de recuperación de KPay (B0331, B0332, B0333). Conversiones por cada mil personas
según oferta, en tres paneles por tiempo sin compra; cuarto panel: MXN por conversión de WhatsApp según a quién va.
Fuente: E15 (embudo por paso, oferta tomada del nombre del paso) y E1 (WhatsApp entregado entre conversiones)."""
from b7 import *

s = pd.read_csv(D + "e15_embudo_pasos.csv", low_memory=False)
k = s[s.canvas_step_name.fillna("").str.contains("B0331|B0332|B0333") & s.canvas_step_name.str.contains("KPay")].copy()
k["st"] = k.canvas_step_name.str.extract(r"(B033\d)")[0]
k["of"] = k.canvas_step_name.str.extract(r"_([A-Za-z]+?)(?:OnlyAmazon)?-Week")[0]
g = k.groupby(["st", "of"]).agg(u=("usuarios", "sum"), c=("usuarios_convirtieron", "sum")); g["pm"] = 1000 * g.c / g.u
gs = k.groupby("st").agg(u=("usuarios", "sum"), c=("usuarios_convirtieron", "sum")); gs["pm"] = 1000 * gs.c / gs.u
print(g.round(2)); print(gs.round(2))
e = load_e1()
w = e[e.canal == "whatsapp"].copy(); w["et"] = w.fam.map(etapa)
gw = w.groupby("et").agg(d=("whatsapp_delivery", "sum"), conv=("conversiones_filas", "sum")); gw["cpc"] = gw.d / gw.conv
f = e[e.fam.str.contains("B0331|B0332|B0333") & e.fam.str.contains("KPay")]
print(gw.round(1), f.envios.sum() / 1e6, f.costo.sum() / 1e6)

import math
k = k[k.usuarios >= 1000].copy(); k["pm"] = 1000 * k.usuarios_convirtieron / k.usuarios; k["con"] = k.of != "SinOferta"
PAN = [("B0331", "3 meses sin compra"), ("B0332", "6 meses sin compra"), ("B0333", "12 meses sin compra")]
S = SVG("Conversiones por cada mil personas de cada paso del programa de recuperación de KPay, por meses sin compra y con o sin oferta")
S.legend([("Paso con oferta (cupón, descuento o plazos)", BLUE, "ci"), ("Paso sin oferta", MARK, "ci"), ("Mediana", INK, "ln")], 0, 14, 16)
S.t(0, 32, "Cada punto es un paso de un Canvas (semana, canal y oferta) con mil personas o más", 10.5, SEC)
X0, X1 = 200, 760
L0, L1 = math.log10(0.1), math.log10(40)
xs = lambda v: X0 + (X1 - X0) * (math.log10(max(v, 0.1)) - L0) / (L1 - L0)
TOP, RH, SH = 62, 104, 40
Yb = TOP + RH * 3 - 12
for v, l in ((0.1, "0"), (0.3, "0.3"), (1, "1"), (3, "3"), (10, "10"), (30, "30")):
    S.line(xs(v), TOP - 6, xs(v), Yb, GRID); S.t(xs(v), Yb + 14, l, 10.5, SEC, "middle")
S.t(X1, Yb + 30, "Conversiones por cada mil personas del paso (escala que multiplica; sin conversiones, a la izquierda)", 10.5, SEC, "end")
for i, (st, nm) in enumerate(PAN):
    y0 = TOP + RH * i
    S.t(0, y0 + 22, nm, 12, INK, w=700)
    S.t(0, y0 + 38, f"{gs.loc[st,'pm']:.1f} conversiones por mil", 10.5, BLUE if st != "B0333" else SEC, w=600)
    S.t(0, y0 + 52, f"{int((k.st==st).sum())} pasos", 10.5, SEC)
    for j, con in enumerate([True, False]):
        yc = y0 + 18 + SH * j
        d = k[(k.st == st) & (k.con == con)]
        S.t(X0 - 8, yc + 4, "con oferta" if con else "sin oferta", 10.5, TXT, "end")
        for n_, (_, r) in enumerate(d.iterrows()):
            jy = ((n_ * 7) % 11 - 5) * 2.2
            S.circle(xs(r.pm), yc + jy, 2.4, BLUE if con else MARK, "#FFFFFF", 0.5, ' fill-opacity="0.75"')
        md = d.pm.median()
        S.line(xs(md), yc - 15, xs(md), yc + 15, INK, 3)
        S.t(xs(md) + 5, yc - 9, f"{md:.1f}", 11, INK, "start", 700, halo=True)
    if i < 2: S.line(0, y0 + RH - 6, 780, y0 + RH - 6, GRID)
r3, r12 = gs.loc["B0331", "pm"], gs.loc["B0333", "pm"]
J = dict(
    titulo=f"Recuperar sí vale, con medida: a 12 meses sin compra se convierte {r3/r12:.0f} veces menos que a 3, con o sin oferta",
    que="Recuperación de KPay: mismo Canvas con y sin oferta (cupón, descuento, plazos).",
    quien="Product Growth (B0331, B0332 y B0333).",
    a_quien="Ex clientes KPay con 3, 6 y 12 meses sin compra.",
    lecturas=[
        f"A 3 meses convierten {r3:.1f} de cada mil; a 6, {gs.loc['B0332','pm']:.1f}; a 12, {r12:.1f}.",
        f"Mediana por paso a 3 meses: {k[(k.st=='B0331')&k.con].pm.median():.1f} por mil con oferta y {k[(k.st=='B0331')&~k.con].pm.median():.1f} sin oferta.",
        f"Por WhatsApp, una conversión cuesta {gw.loc['Clientes activos y recurrentes','cpc']:.0f} MXN con activos y {gw.loc['Ex clientes inactivos','cpc']:.0f} MXN con ex clientes.",
    ],
    causa="Se manda la misma secuencia sin importar cuánto lleva la persona sin comprar, y sin grupo sin mensajes.",
    sowhat="Más esfuerzo a 3 meses; a 6 y 12, canal barato, pocos toques y presupuesto con límite.",
    fuente=f"Fuente: Braze, embudo por paso de Canvas (B0331 a B0333) y envíos por canal, ene a sep 2026. Conversión: solicitud o préstamo, sobre todo de KCash; no mide la compra en KPay.",
    svg=S.out())
write(69, J)
