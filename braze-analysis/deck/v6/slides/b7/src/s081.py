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
CH = [("email", 10, "clics por mil correos"), ("push notification", 10, "aperturas por mil push"), ("in-app", 1, "% in-app con clic"), ("whatsapp", 1, "% WhatsApp leídos")]
def cell(g, canal, k):
    v = R.get((g, canal), (np.nan, 0))[0]
    if np.isnan(v): return '<td class="num" style="color:#A3AAB5">sin envío</td>'
    base = R[("Sin motivo", canal)][0]; ratio = v / base
    sty = "color:#127A5B;font-weight:700" if ratio >= 2 else ("color:#6B7484" if ratio < 1 else "")
    val = k * v
    return f'<td class="num" style="{sty}">{val:.1f}</td>' if val < 10 else f'<td class="num" style="{sty}">{val:.0f}</td>'
rows = []
for t, _, ex in TRIG:
    rows.append(f'<tr><td><b>{t}</b></td><td style="color:#6B7484">{ex}</td><td class="num">{vol[t]/1e6:.1f} M</td>' + "".join(cell(t, c, k) for c, k, _ in CH) + "</tr>")
sumrow = (f'<tr style="background:#E9F4EF"><td colspan="2"><b>Todos los que salen porque la persona hizo algo</b> ({100*volev["Con motivo"]/volev.sum():.0f} % del volumen; {100*clk_share:.0f} % de los clics de correo)</td><td class="num"><b>{volev["Con motivo"]/1e6:.0f} M</b></td>' + "".join(cell("Con motivo", c, k) for c, k, _ in CH) + "</tr>")
basrow = (f'<tr style="background:#F1F3F6"><td colspan="2"><b>Sin motivo: le llega porque está en una lista</b></td><td class="num"><b>{volev["Sin motivo"]/1e6:.0f} M</b></td>' + "".join(f'<td class="num"><b>{(k*R[("Sin motivo", c)][0]):.1f}</b></td>' if k * R[("Sin motivo", c)][0] < 10 else f'<td class="num"><b>{(k*R[("Sin motivo", c)][0]):.0f}</b></td>' for c, k, _ in CH) + "</tr>")
html = ('<table style="font-size:.95cqi"><tr><th>Qué hizo la persona</th><th>Campaña de ejemplo</th><th class="num">Mensajes</th><th class="num">Email: clics por mil</th><th class="num">Push: aperturas por mil</th><th class="num">In-app: % con clic</th><th class="num">WhatsApp: % leído</th></tr>'
        + "".join(rows) + sumrow + basrow + '</table><div style="margin-top:.4cqi;font-size:.8cqi;color:#6B7484">En verde: dos veces o más la respuesta de lo que sale a una lista; en gris: menos que eso.</div>')
em = R[("Con motivo", "email")][0] / R[("Sin motivo", "email")][0]
J = dict(
    kind="html", ancho_completo=True,
    titulo="Los mensajes que salen porque la persona hizo algo responden siete veces más en correo que los que salen a una lista, y hoy son la minoría",
    que="Recordatorios de algo empezado, aviso de pago por vencer, sugerencias después de una compra, oferta a quien canceló, bienvenida, aniversario y regreso a los 45 días.",
    quien="Marketing (recordatorio de registro, oferta a quien canceló), Product Growth (meses sin intereses a activos, 45 días, Temu, aniversario, bienvenida KPay) y Collections (precobranza).",
    a_quien="Personas en un momento concreto: se registró, compró, tiene un pago, canceló o lleva un tiempo sin volver.",
    lecturas=[
        f"Con {100*volev['Con motivo']/volev.sum():.0f} % de los mensajes se llevan {100*clk_share:.0f} % de los clics de correo: {10*R[('Con motivo','email')][0]:.0f} clics por mil contra {10*R[('Sin motivo','email')][0]:.1f} ({em:.1f} veces). En push, {10*R[('Con motivo','push notification')][0]:.0f} aperturas por mil contra {10*R[('Sin motivo','push notification')][0]:.0f}.",
        "Fuera de los avisos de pago, la precobranza y los meses sin intereses a clientes activos son las campañas grandes que mejor responden en Braze.",
        "No todo motivo funciona igual: el aniversario y la compra en un comercio responden poco por correo. El WhatsApp se lee igual con o sin motivo.",
    ],
    causa="La mayoría de las promociones nace de una lista (todos los registrados, toda la base) y no de algo que la persona hizo; por eso 88 % del volumen responde como lista.",
    sowhat=f"Con {100*volev['Con motivo']/volev.sum():.0f} % del volumen se llevan {100*clk_share:.0f} % de los clics de correo. Cada promoción nueva debe nacer de algo que hizo la persona, no de una lista.",
    fuente="Fuente: Braze, envíos por campaña, mes y canal, enero a septiembre 2026. El motivo se infiere del nombre de la campaña (no tenemos el evento de entrada del Canvas). Sin avisos de pago, BillPay ni cobranza salvo precobranza. Quien recibe por algo que hizo ya es más activo: la diferencia no prueba cuánto vende el mensaje sin un grupo sin mensajes.",
    html=html)
write(81, J)
