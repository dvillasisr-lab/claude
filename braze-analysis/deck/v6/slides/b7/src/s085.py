"""Lámina 85 (decisiones): seis preguntas antes de lanzar una campaña y una regla para apagarla, en tarjetas con la cifra de Kueski
que respalda cada una. Cifras recalculadas aquí: motivo (regla de s081), WhatsApp por etapa (s069), correos por persona al mes (E1),
versiones simultáneas (s074), grupo sin mensajes (E13), promociones sin ticket (s077)."""
import re
from b7 import *

e = load_e1(); e["tema"] = e.communication_name.map(tema)
# 1. motivo (misma regla que s081)
TRIG = [r"leftfunnel|accountcreation|faltaveriff|requestinfo|registrolinea", r"precobranza",
        r"retargeting_installments|compra(kcash|kpay)|sicompletocompra|completocompra|increaseutilization", r"cancel|abandon", r"onboarding|welcome",
        r"tardan45", r"aniversario", r"compraentemu|compraen"]
def trig(n):
    n = (n if isinstance(n, str) else "").lower()
    if re.search(r"bkt|billpay|billpayment|^transaccional-|privalia", n): return False
    return any(re.search(p, n) for p in TRIG)
e["trig"] = e.communication_name.map(trig)
Pm = e[(e.canal == "email") & (~e.tema.isin(["Cobranza", "Transaccional"]) | e.trig)]
gm = Pm.groupby("trig").agg(d=("email_delivery", "sum"), c=("email_click", "sum"))
cm, sm = 1000 * gm.loc[True, "c"] / gm.loc[True, "d"], 1000 * gm.loc[False, "c"] / gm.loc[False, "d"]
# 2. WhatsApp por etapa
w = e[e.canal == "whatsapp"].copy(); w["et"] = w.fam.map(etapa)
gw = w.groupby("et").agg(d=("whatsapp_delivery", "sum"), conv=("conversiones_fraccional", "sum")); gw["cpc"] = gw.d / gw.conv
# 3. correos por persona al mes
x = e[(e.canal == "email") & (e.usuarios_aprox > 0) & (e.email_delivery > 0)].copy(); x["t"] = x.email_sent / x.usuarios_aprox
x["b"] = pd.cut(x.t, [0, 1.5, 2.5, 4.5, 1e9], labels=["1", "2", "3 a 4", "5+"])
gt = x.groupby("b", observed=True).agg(d=("email_delivery", "sum"), c=("email_click", "sum")); gt["pm"] = 1000 * gt.c / gt.d
# 4. versiones a la vez
fe = e[e.envios > 0]; sp = fe[fe.m == 9].groupby("fam").communication_id.nunique()
# 5. grupo sin mensajes
lc = pd.read_csv(D + "e13_lift_control.csv"); ncv = lc.canvas_id.nunique(); nctl = lc[(lc.grupo == "control") & (lc.usuarios >= 1000)].canvas_id.nunique()
# 6. sin ticket
c2 = pd.read_csv(D + "e2_catalogo.csv", low_memory=False); st = set(c2[c2.tiene_ticket.astype(str) != "1"].communication_id)
promo = ~e.tema.isin(["Cobranza", "Transaccional"]); sinT = e[e.communication_id.isin(st) & promo].envios.sum()
print(cm, sm, gw.cpc.round(0).to_dict(), gt.pm.round(1).to_dict(), (sp >= 2).sum(), ncv, nctl, sinT / 1e6)
CARDS = [
 ("1", "¿Qué hizo la persona para recibirla?", "Registro, compra, pago, cancelación o días sin volver.", f"{cm:.0f} contra {sm:.1f}", "clics por mil correos, con motivo y sin motivo"),
 ("2", "¿Va por el canal que usa y cuesta menos?", "WhatsApp solo a quien leyó uno en 90 días.", f"{gw.loc['Clientes activos y recurrentes','cpc']:.0f} contra {gw.loc['Ex clientes inactivos','cpc']:.0f}", "MXN por conversión por WhatsApp: activos contra ex clientes"),
 ("3", "¿Cuántos mensajes le llegan?", "Máximo dos al mes; el segundo solo a quien no abrió.", f"{gt.loc['2','pm']:.1f} contra {gt.loc['3 a 4','pm']:.1f}", "clics por mil correos con 2 al mes y con 3 o 4"),
 ("4", "¿Le llega otra versión o campaña el mismo día?", "Revisar el calendario común antes de activar.", f"{(sp>=2).sum()}", "campañas con dos versiones a la vez en septiembre"),
 ("5", "¿Tiene un grupo sin mensajes?", "10 %; si va a más de un millón, prueba al 10 % antes.", f"{nctl} de {ncv:,}", "Canvas con grupo sin mensajes de mil personas o más"),
 ("6", "¿Tiene dueño, ticket y una sola versión viva?", "Al lanzar la nueva se archiva la anterior.", f"{sinT/1e6:.0f} M", "mensajes de promociones sin ticket en el año"),
]
card = lambda n, q, l, v, u: (f'<div style="border-top:2px solid #1F4FD8;padding-top:.6cqi"><div style="font-size:1.12cqi;font-weight:700;color:#0B1220">{n}. {q}</div>'
                              f'<div style="font-size:.95cqi;color:#3B4556;margin-top:.25cqi">{l}</div><div style="font-size:2.3cqi;font-weight:700;color:#1F4FD8;margin-top:.5cqi;line-height:1">{v}</div>'
                              f'<div style="font-size:.88cqi;color:#6B7484;margin-top:.2cqi">{u}</div></div>')
html = ('<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2.6cqi 2cqi;margin-top:.6cqi">' + "".join(card(*c) for c in CARDS) + '</div>'
        '<div style="margin-top:1.4cqi;background:#E9F4EF;padding:.7cqi 1cqi;font-size:1.02cqi;color:#0B1220"><b style="color:#127A5B">Regla para apagarla:</b> '
        'si en dos meses no llega a lo mínimo (3 clics por mil correos, 7.5 aperturas por mil push, 60 % de WhatsApp leídos o 10 % de in-app con clic) '
        'o causa más de 2.5 bajas por mil correos, se rehace o se apaga.</div>')
J = dict(
    kind="html", ancho_completo=True,
    titulo="Antes de lanzar una campaña: seis preguntas y una regla para apagarla",
    que="Toda promoción nueva o relanzada; no cobranza ni avisos de pago.",
    quien="El equipo dueño la llena; CRM la revisa antes de activar.",
    a_quien="Todos los segmentos; ex clientes con presupuesto con límite y grupo sin mensajes.",
    sowhat="Seis preguntas antes de activar y una regla para apagar evitan casi todo lo que vimos.",
    fuente="Fuente: láminas 69, 74, 77 y 81; Braze, envíos por campaña, canal y mes, y grupos de control por Canvas, ene a sep 2026.",
    html=html)
write(85, J)
