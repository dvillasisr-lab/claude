"""Lámina 81 (tabla): mensajes que salen porque la persona hizo algo, por motivo, contra los que salen a una lista. Motivo inferido
por el nombre de la campaña (regla de p5/s78.py). Se excluyen avisos de pago y cobranza salvo precobranza. Fuente: E1."""
import re
from b7 import *

e = load_e1(); e["tema"] = e.communication_name.map(tema)
TRIG = [
 ("Empezó su registro y se quedó a medias", r"leftfunnel|accountcreation|faltaveriff|requestinfo|registrolinea", "Recordatorio Veriff (Marketing)"),
 ("Tiene un pago por vencer", r"precobranza", "Precobranza (Collections)"),
 ("Acaba de comprar o usar su crédito", r"retargeting_installments|compra(kcash|kpay)|sicompletocompra|completocompra|increaseutilization", "Meses sin intereses a activos (Product Growth)"),
 ("Canceló o abandonó una oferta", r"cancel|abandon", "Oferta a quien canceló (Marketing)"),
 ("Se registró hace poco", r"onboarding|welcome", "Bienvenida KCash y KPay"),
 ("Lleva 45 días sin volver a pedir", r"tardan45", "Tardan 45 días (Product Growth)"),
 ("Cumple años de cuenta", r"aniversario", "Aniversario KPay (Product Growth)"),
 ("Compró en un comercio con KPay", r"compraentemu|compraen", "Compró en Temu o tiendas (Product Growth)"),
]
def trig(n):
    n = (n if isinstance(n, str) else "").lower()
    if re.search(r"bkt|billpay|billpayment|^transaccional-|privalia", n): return None
    for t, p, _ in TRIG:
        if re.search(p, n): return t
    return None
e["trig"] = e.communication_name.map(trig)
P = e[~e.tema.isin(["Cobranza", "Transaccional"]) | e.trig.notna()].copy()
P["g"] = P.trig.fillna("Sin motivo")
P["ev"] = np.where(P.trig.notna(), "Con motivo", "Sin motivo")
R = {}
for col in ("g", "ev"):
    for canal, (b, r) in RESP.items():
        x = P[P.canal == canal].groupby(col).agg(base=(b, "sum"), resp=(r, "sum"))
        for k, q in x.iterrows(): R[(k, canal)] = (100 * q.resp / q.base if q.base > 0 else np.nan, q.resp)
vol = P.groupby("g").envios.sum(); volev = P.groupby("ev").envios.sum()
clk_share = R[("Con motivo", "email")][1] / (R[("Con motivo", "email")][1] + R[("Sin motivo", "email")][1])
print(volev / 1e6, 100 * volev / volev.sum(), clk_share, {k: round(v[0], 2) for k, v in R.items() if k[0] in ("Con motivo", "Sin motivo")})
import math
F = {}
for canal in ("email", "push notification"):
    b_, r_ = RESP[canal]
    f = P[P.canal == canal].groupby(["fam", "ev"]).agg(base=(b_, "sum"), resp=(r_, "sum"), env=("envios", "sum"), eq=("equipo", "first")).reset_index()
    f = f[f.base >= 50000].copy(); f["pm"] = 1000 * f.resp / f.base
    F[canal] = f
    print(canal, f.groupby("ev").pm.median().to_dict(), f.ev.value_counts().to_dict())
S = SVG("Campañas promocionales de email y de push: mensajes contra respuesta; en verde las que salen porque la persona hizo algo")
S.legend([("Sale porque la persona hizo algo", GREEN, "ci"), ("Sale a una lista", MARK2, "ci"), ("Mediana de cada grupo", INK, "ln")], 0, 14, 16)
LBL = {"email": [("Leads_LeftFunnel-Retargeting_Veriff", "Recordatorio Veriff", -8), ("Precobranza-ecosystem", "Precobranza KCash", -8), ("Active-Retargeting_Installments_SP", "Meses sin intereses a activos", 16)],
       "push notification": [("RetargetingOffering-Canceló", "Oferta a quien canceló", -99), ("Active-Retargeting_Installments_SP", "Meses sin intereses a activos", -8), ("Precobranza-ecosystem", "Precobranza KCash", 16)]}
def panel(x0, w, canal, title, unit, ymin, ymax):
    f = F[canal]; y0, h = 64, 270
    L0, L1 = math.log10(5e4), math.log10(5e7)
    X = lambda v: x0 + w * (math.log10(min(v, 5e7)) - L0) / (L1 - L0)
    Y = lambda v: y0 + h - h * (math.log10(min(max(v, ymin), ymax)) - math.log10(ymin)) / (math.log10(ymax) - math.log10(ymin))
    S.t(x0, y0 - 16, title, 12, INK, w=700)
    for v in (0.1, 1, 10, 100):
        if ymin <= v <= ymax: S.line(x0, Y(v), x0 + w, Y(v), GRID); S.t(x0 - 6, Y(v) + 4, f"{v:g}", 10.5, SEC, "end")
    for v, l, an in ((5e4, "50 mil", "start"), (1e6, "1 M", "middle"), (1e7, "10 M", "middle")):
        S.t(X(v), y0 + h + 14, l, 10.5, SEC, an)
    for _, q in f[f.ev == "Sin motivo"].iterrows(): S.circle(X(q.env), Y(q.pm), 2.4, MARK2, sw=0)
    for _, q in f[f.ev == "Con motivo"].iterrows(): S.circle(X(q.env), Y(q.pm), 3.4, GREEN, "#FFFFFF", 0.8)
    for ev, col in (("Con motivo", GREEN), ("Sin motivo", INK)):
        md = f[f.ev == ev].pm.median()
        S.line(x0, Y(md), x0 + w, Y(md), col, 1.5, ' stroke-dasharray="5 3"')
        S.t(x0 + w, Y(md) - 4, f"mediana {md:.1f}" if md < 10 else f"mediana {md:.0f}", 10.5, col, "end", 700, halo=True)
    for k, lab, dy in LBL[canal]:
        q = f[f.fam.str.contains(k, regex=False)].sort_values("env").iloc[-1]
        if dy == -99: S.t(X(q.env) + 6, Y(q.pm) + 4, lab, 10.5, INK, "start", 600, halo=True)
        else: S.t(X(q.env) - 5, Y(q.pm) + dy, lab, 10.5, INK, "end", 600, halo=True)
    S.t(x0 + w / 2, y0 + h + 28, f"Mensajes de la campaña (escala que multiplica)", 10.5, SEC, "middle")
panel(40, 330, "email", "Email: clics por cada mil correos", "Clics", 0.1, 100)
panel(446, 330, "push notification", "Push: aperturas por cada mil push", "Aperturas", 1, 300)
S.t(0, 410, "Campañas promocionales con 50 mil mensajes o más; sin avisos de pago ni cobranza salvo precobranza.", 10.5, SEC)
J = dict(
    titulo="Los mensajes que salen porque la persona hizo algo responden siete veces más en correo que los de una lista",
    que="Recordatorios, precobranza, ofertas tras comprar o cancelar, bienvenida y 45 días.",
    quien="Marketing, Product Growth y Collections (precobranza).",
    a_quien="Quien se registró, compró, tiene un pago, canceló o lleva tiempo sin volver.",
    lecturas=[
        f"Son {100*volev['Con motivo']/volev.sum():.0f} % de los mensajes y {100*clk_share:.0f} % de los clics de correo.",
        f"Correo: {10*R[('Con motivo','email')][0]:.0f} clics por mil contra {10*R[('Sin motivo','email')][0]:.1f}; push: {10*R[('Con motivo','push notification')][0]:.0f} aperturas por mil contra {10*R[('Sin motivo','push notification')][0]:.0f}.",
        "No todo motivo funciona igual: aniversario y compra en comercio responden poco por correo.",
    ],
    causa="La mayoría de las promociones nace de una lista y no de algo que hizo la persona.",
    sowhat="Cada promoción nueva debe nacer de algo que hizo la persona, no de una lista.",
    fuente="Fuente: Braze, envíos por campaña y canal, ene a sep 2026. Motivo inferido del nombre de la campaña. Quien hizo algo ya es más activo: sin grupo sin mensajes no se sabe cuánto vende.",
    svg=S.out())
write(81, J)
