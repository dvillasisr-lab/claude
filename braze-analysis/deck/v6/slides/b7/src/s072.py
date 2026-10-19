"""Lámina 72 (forma de la lámina 36 del v5): dispersión de cada correo y cada push (versión de campaña con 200 mil o más) por tamaño (x, log)
contra respuesta (y); en verde los que responden bien (15 clics por mil correos; 30 aperturas por mil push). Debajo, cuántos pasan por tamaño.
Fuente: E1 agregado por communication_id."""
import math
from b7 import *

e = load_e1()
GOOD = {"email": 15, "push notification": 30}
D_ = {}
for canal in GOOD:
    b, r = RESP[canal]
    x = e[e.canal == canal].groupby("communication_id").agg(name=("communication_name", "first"), base=(b, "sum"), resp=(r, "sum"), equipo=("equipo", "first"))
    x = x[x.base >= 200000].copy(); x["pm"] = 1000 * x.resp / x.base; x["g"] = x.pm >= GOOD[canal]; x["tema"] = x.name.map(tema)
    x["band"] = pd.cut(x.base, [2e5, 1e6, 5e6, 1e9], labels=["200 mil a 1 M", "1 a 5 M", "más de 5 M"])
    D_[canal] = x
    print(canal, len(x), x.g.sum(), (x.pm >= 10 * MIN[canal]).sum())
xe, xp = D_["email"], D_["push notification"]
tg = xe[xe.g].tema.value_counts(); tn = xe.tema.value_counts()
below = xe[xe.pm < 3]
S = SVG("Cada correo y cada push grande según su tamaño y su respuesta; en verde los que responden bien")
S.legend([("Responde bien", GREEN, "ci"), ("Responde menos", MARK, "ci")], 0, 14, 18)
S.t(780, 14, "Cada punto es una versión de una campaña con 200 mil mensajes o más", 10.5, SEC, "end")
LBL = {"email": [("Retargeting_Veriff", "Recordatorio Veriff", "start", -6), ("Payment-Confirmation", "Confirmación de pago", "end", -6), ("Collections-KCash-20250819-T000-CANVAS-Precobranza", "Precobranza KCash", "end", -6)],
       "push notification": [("Payment Received - Push", "Pago recibido", "end", 14), ("Active-Retargeting_Installments_SP", "Meses sin intereses a activos", "start", -6), ("Anonimos-RescateTasa0", "Rescate Tasa 0 a anónimos", "end", -10)]}
def panel(x0, w, canal, title, unit, YM):
    x = D_[canal]; y0, h = 70, 250
    L0, L1 = math.log10(2e5), math.log10(2e7)
    X = lambda v: x0 + w * (math.log10(v) - L0) / (L1 - L0)
    Y = lambda v: y0 + h - h * min(v, YM) / YM
    S.t(x0, y0 - 22, title, 12, INK, w=700)
    S.t(x0, y0 - 8, f"En verde, los {int(x.g.sum())} de {len(x)} que llegan a {GOOD[canal]} {unit} por mil", 10.5, GREEN, w=600)
    for v in range(0, YM + 1, YM // 4):
        S.line(x0, Y(v), x0 + w, Y(v), GRID); S.t(x0 - 6, Y(v) + 4, f"{v}", 10.5, SEC, "end")
    for v, l, an in ((2e5, "200 mil", "start"), (1e6, "1 M", "middle"), (5e6, "5 M", "middle"), (2e7, "20 M", "end")):
        S.t(X(v), y0 + h + 14, l, 10.5, SEC, an)
    S.t(x0 + w / 2, y0 + h + 28, f"{'Correos entregados' if canal == 'email' else 'Push enviados'} (escala que multiplica)", 10.5, SEC, "middle")
    S.line(x0, Y(GOOD[canal]), x0 + w, Y(GOOD[canal]), GREEN, 1.2)
    S.line(x0, Y(10 * MIN[canal]), x0 + w, Y(10 * MIN[canal]), INK, 1, ' stroke-dasharray="4 4" opacity="0.6"')
    for _, q in x[~x.g].iterrows(): S.circle(X(q.base), Y(q.pm), 2.8, MARK2, sw=0.6)
    for _, q in x[x.g].iterrows(): S.circle(X(q.base), Y(q.pm), 3.6, GREEN, "#FFFFFF", 1)
    S.t(x0 + w, Y(10 * MIN[canal]) - 4, f"Mínimo: {10*MIN[canal]:g}", 10.5, INK, "end", 600, halo=True)
    S.t(x0 + w, Y(GOOD[canal]) - 4, f"Responde bien: {GOOD[canal]}", 10.5, GREEN, "end", 600, halo=True)
    for k, lab, an, dy in LBL[canal]:
        q = x[x.name.str.contains(k, regex=False)].sort_values("base", ascending=False).iloc[0]
        S.t(X(q.base) + (6 if an == "start" else -6), Y(q.pm) + dy, lab, 10.5, INK, an, 600, halo=True)
    b = x.groupby("band", observed=True).agg(n=("g", "size"), b=("g", "sum"))
    S.t(x0, y0 + h + 48, "Responden bien, por tamaño:", 10.5, INK, w=600)
    S.t(x0, y0 + h + 63, "; ".join(f"{i}: {int(q.b)} de {int(q.n)}" for i, q in b.iterrows()), 10.5, TXT)
    S.t(x0 - 30, y0 - 38, f"{unit.capitalize()} por cada mil", 10.5, SEC)
panel(36, 330, "email", "Email: clics por cada mil correos", "clics", 60)
panel(442, 330, "push notification", "Push: aperturas por cada mil push", "aperturas", 160)
S.t(0, 414, "Arriba de 60 clics o de 160 aperturas por mil se dibuja en el borde superior.", 10.5, SEC)
J = dict(
    titulo="Solo uno de cada ocho correos grandes responde bien, y los hay de todos los tamaños: los separa el motivo del envío, no el tamaño",
    que=f"Todo el email y el push con volumen: {len(xe)} correos y {len(xp)} push de 200 mil o más (cada versión de una campaña con su fecha).",
    quien=f"De los {int(xe.g.sum())} correos que responden bien: Others (avisos de pago) {int((xe.g & (xe.equipo=='Others')).sum())}, Marketing {int((xe.g & (xe.equipo=='Marketing')).sum())} (recordatorios de registro), Collections {int((xe.g & (xe.equipo=='Collections')).sum())}, Product Growth {int((xe.g & (xe.equipo=='Product Growth')).sum())} y Sales {int((xe.g & (xe.equipo=='Sales')).sum())}.",
    a_quien="Los que responden bien van a quien está a la mitad de algo: empezó su registro, tiene un pago por vencer o acaba de pagar. Los demás, a listas de leads, registrados o clientes de KPay.",
    lecturas=[
        f"{int(xe.g.sum())} de {len(xe)} correos reciben 15 clics por mil o más (cinco veces lo mínimo); en push, {int(xp.g.sum())} de {len(xp)} llegan a 30 aperturas por mil. Hay buenos y malos de 200 mil y de varios millones.",
        f"Los que responden bien son avisos de pago ({tg.get('Transaccional',0)}), recordatorios de registro ({tg.get('Recordatorio de registro',0)} de {tn.get('Recordatorio de registro',0)}), cobranza ({tg.get('Cobranza',0)}) y crédito a clientes activos ({tg.get('Uso y recompra del crédito',0)}). De {tn.get('Promociones de comercios KPay',0)} promociones de comercios KPay y {tn.get('Referidos',0)} de referidos, ninguno.",
        f"{len(below)} correos ni siquiera llegan a lo mínimo (3 clics por mil): son {100*below.base.sum()/xe.base.sum():.0f} % de estos correos y {100*below.resp.sum()/xe.resp.sum():.0f} % de sus clics.",
    ],
    causa="La gente responde al mensaje que tiene que ver con algo que está haciendo; la promoción que le llega porque está en una lista la ignora, sea la lista chica o grande.",
    sowhat="Para que un correo responda no hay que hacerlo más chico: hay que mandarlo por una razón de la persona.",
    fuente="Fuente: Braze, envíos por comunicación, mes y canal, enero a septiembre 2026; versiones de email y push con 200 mil mensajes o más. Clics sobre correos entregados; aperturas sobre push enviados. Responde bien: 15 clics por mil correos o 30 aperturas por mil push (cuatro a cinco veces lo mínimo). Tema por el nombre de la campaña.",
    svg=S.out())
write(72, J)
