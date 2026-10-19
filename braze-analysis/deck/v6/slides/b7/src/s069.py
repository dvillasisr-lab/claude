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

OF = [("SinOferta", "Sin oferta"), ("Cupon", "Cupón"), ("DtoTasa", "Descuento en tasa"), ("CuponDtoTasa", "Cupón y descuento en tasa"), ("CuponPlazosConIntereses", "Cupón y plazos con interés")]
PAN = [("B0331", "3 meses sin compra"), ("B0332", "6 meses sin compra"), ("B0333", "12 meses sin compra")]
S = SVG("Conversiones por cada mil personas en el programa de recuperación de KPay, por oferta y por meses sin compra, y costo por conversión de WhatsApp según a quién va")
LX, PW, PG = 172, 110, 12
TOP, RH = 92, 40
VM = 8.0
S.t(0, 14, "Conversiones por cada mil personas que recibieron el paso, según la oferta", 12, INK, w=600)
S.t(0, 30, "Programa de recuperación de KPay de Product Growth: mismo Canvas, distinta rama de oferta", 10.5, SEC)
for j, (st, nm) in enumerate(PAN):
    x0 = LX + j * (PW + PG); xs = lambda v, x0=x0: x0 + PW * v / VM
    S.t(x0, TOP - 30, nm, 12, INK, w=700)
    S.t(x0, TOP - 16, f"Total {gs.loc[st,'pm']:.1f} por mil", 11, BLUE if st != "B0333" else INK, w=600)
    for v in (0, 4, 8):
        S.line(xs(v), TOP - 6, xs(v), TOP + RH * len(OF) - 10, GRID)
        S.t(xs(v), TOP + RH * len(OF) + 4, f"{v}", 10.5, SEC, "middle")
    for i, (key, lab) in enumerate(OF):
        y = TOP + RH * i
        v = g.loc[(st, key), "pm"]
        S.rect(x0, y, xs(v) - x0, 16, MARK if key == "SinOferta" else BLUE)
        S.t(xs(v) + 4, y + 12, f"{v:.1f}", 11, INK, w=600)
for i, (key, lab) in enumerate(OF):
    y = TOP + RH * i
    S.t(0, y + 12, lab, 11.5, INK if key == "SinOferta" else TXT, w=600 if key == "SinOferta" else 400)
S.t(LX, TOP + RH * len(OF) + 18, "por cada mil personas", 10.5, SEC)
# cuarto panel
P4 = 600; P4W = 120; VM4 = 200
xs4 = lambda v: P4 + P4W * v / VM4
S.line(P4 - 18, 44, P4 - 18, 330, GRID)
S.t(P4 - 4, TOP - 30, "MXN por conversión", 12, INK, w=700)
S.t(P4 - 4, TOP - 16, "de WhatsApp, según a quién va", 11, SEC)
ST = [("Clientes activos y recurrentes", "Activos"), ("Leads (no terminaron registro)", "Leads"), ("Registrados sin crédito o nuevos", "Registrados sin crédito"), ("Ex clientes inactivos", "Ex clientes inactivos")]
for i, (key, lab) in enumerate(ST):
    y = TOP + 50 * i
    v = gw.loc[key, "cpc"]
    S.t(P4 - 4, y + 4, lab, 11.5, INK, w=600)
    S.rect(P4 - 4, y + 10, xs4(v) - P4, 14, BLUE if key == "Ex clientes inactivos" else MARK)
    S.t(xs4(v) - 4 + 5, y + 21, f"{v:.0f}", 11.5, INK, w=700)
S.t(0, 376, "Conversión de referencia: solicitud o préstamo, sobre todo de KCash; no mide la compra en KPay.", 10.5, SEC)
S.t(0, 392, "La rama sin oferta compara ofertas entre sí, no mensaje contra no mandar nada.", 10.5, SEC)
S.t(0, 408, "Ex clientes KPay pueden no tener la app: sin app no reciben push ni in-app.", 10.5, SEC)
r3, r12 = gs.loc["B0331", "pm"], gs.loc["B0333", "pm"]
J = dict(
    titulo=f"Recuperar clientes sí vale, pero con medida: a 12 meses sin compra se convierte {r3/r12:.0f} veces menos que a 3, y la oferta casi no cambia el resultado",
    que="Promoción para recuperar clientes de KPay: el mismo Canvas con ramas sin oferta, con cupón, con descuento en tasa y con plazos con intereses, algunas solo para Amazon.",
    quien="Product Growth: oferta a ex clientes KPay con 3, 6 y 12 meses sin compra (B0331, B0332 y B0333, con y sin oferta).",
    a_quien="Ex clientes KPay: 3 meses sin compra, 6 meses y 12 meses (churn). Se les escribe para recuperarlos.",
    lecturas=[
        f"A 3 meses sin compra convierten {r3:.1f} de cada mil; a 6, {gs.loc['B0332','pm']:.1f}; a 12, {r12:.1f}. El tiempo sin comprar pesa mucho más que la oferta.",
        f"Sin oferta convierte casi igual que con oferta: a 3 meses {g.loc[('B0331','SinOferta'),'pm']:.1f} por mil contra {g.loc['B0331'].drop('SinOferta').pm.min():.1f} a {g.loc['B0331'].pm.max():.1f} con oferta; a 12 meses {g.loc[('B0333','SinOferta'),'pm']:.1f} contra {g.loc['B0333'].drop('SinOferta').pm.min():.1f} a {g.loc['B0333'].pm.max():.1f}.",
        f"Por WhatsApp, cada conversión cuesta {gw.loc['Clientes activos y recurrentes','cpc']:.0f} MXN con clientes activos y {gw.loc['Ex clientes inactivos','cpc']:.0f} MXN con ex clientes inactivos: once veces más.",
    ],
    causa="El programa manda la misma secuencia larga, por los cuatro canales y con WhatsApp, sin importar cuánto lleva la persona sin comprar, y no hay un grupo sin mensajes para saber cuánto recupera.",
    sowhat="Gastar más donde todavía se recupera (3 meses) y, a 6 y 12 meses, email o in-app con uno o dos toques al mes, WhatsApp solo a quien lee, presupuesto con límite y 10 % sin mensajes.",
    fuente=f"Fuente: Braze, embudo por paso de Canvas (B0331, B0332 y B0333, 45 Canvas) y envíos por campaña, enero a septiembre 2026. El programa mandó {f.envios.sum()/1e6:.1f} M mensajes y costó {f.costo.sum()/1e6:.1f} M MXN. WhatsApp a 1.00 MXN por entregado. Etapa por el nombre de la campaña.",
    svg=S.out())
write(69, J)
