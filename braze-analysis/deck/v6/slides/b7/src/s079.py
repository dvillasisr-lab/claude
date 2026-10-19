"""Lámina 79: recordatorio de terminar el registro. Izquierda: % que abrió cada correo según los días desde que la persona se quedó
en un paso (Canvas de Acquisition KPay T2706/T2727/T2728, E15). Derecha: personas nuevas que se dieron de baja el día que recibieron cada campaña
(muestra L, cohorte de nuevos). Volumen, clics y bajas de E1; conversión de quien abre contra quien no abre de muestra_c."""
import re
from b7 import *

s = pd.read_csv(D + "e15_embudo_pasos.csv", low_memory=False)
s["nm"] = s.canvas_step_name.fillna("")
k = s[s.nm.str.contains("T2727|T2728") & (s.canal == "email")].copy()
k["tipo"] = np.where(k.nm.str.contains("AccountCreation"), "Crear la cuenta", np.where(k.nm.str.contains("PersonalInformation"), "Datos personales", "Verificar identidad"))
def dia(n):
    m = re.search(r"_(\d+)\s?(mins|day|days)ago", n)
    if not m: return None
    return 0 if m.group(2) == "mins" else int(m.group(1))
k["dia"] = k.nm.map(dia); k = k[k.dia.notna()]
k["ab"] = np.minimum(k.usuarios_abrieron, k.usuarios)
G = k.groupby(["tipo", "dia"]).agg(u=("usuarios", "sum"), ab=("ab", "sum")); G["p"] = 100 * G.ab / G.u
print(G.round(1))
e = load_e1()
rec = e[e.fam.str.contains("LeftFunnel|T2706|T2713|T2727|T2728")]
re_ = rec[rec.canal == "email"]
byq = re_.groupby("fam").agg(d=("email_delivery", "sum"), c=("email_click", "sum"), u=("email_unsubscribe", "sum"), eq=("equipo", "first")); byq["cpm"] = 1000 * byq.c / byq.d
print(rec.groupby("equipo").envios.sum() / 1e6, re_.email_delivery.sum() / 1e6, re_.email_unsubscribe.sum()); print(byq.sort_values("d", ascending=False).head(6))
l = pd.read_csv(H + "muestra_l_familias_baja.csv"); ln = l[(l.bloque == "familia_dia_baja") & (l.cohorte_limpia == 1)].copy()
NT = ln.usuarios.sum()
ln["rec"] = ln.clave.str.contains("LeftFunnel|T2706|T2713|T2727|T2728")
ln["k"] = ln.clave.str.replace(r"[^A-Za-z0-9]", "", regex=True)
ln = ln.sort_values("usuarios", ascending=False)
ln = ln.groupby("k", sort=False).agg(clave=("clave", "first"), usuarios=("usuarios", "sum"), dias_mediana=("dias_mediana", "first"), emails_mediana=("emails_mediana", "first"), rec=("rec", "first")).reset_index()
top = ln.sort_values("usuarios", ascending=False).head(8)
c = load_c(); vz = c[(c.canal == "email") & c.familia.str.contains("Retargeting_Veriff") & c.familia.str.startswith("Marketing")].iloc[0]
kc = ln[ln.clave.str.contains("LeftFunnel-Retargeting_(?:Veriff|PersonalInfo|NIP)$")]
print(NT, kc.usuarios.sum(), 100 * kc.usuarios.sum() / NT, vz.conv_abren_pct, vz.conv_no_abren_pct, vz.toques_usuario_mes)
NOM = {"BillPay_Intro": "Lanzamiento de BillPay (una vez)", "Retargeting_Veriff": "Recordatorio: verificar identidad", "Retargeting_PersonalInfo": "Recordatorio: datos personales",
       "B0211": "Tasa 0 a registrados de KPay", "FraudRisk": "Aviso de rechazo por riesgo", "Retargeting_NIP": "Recordatorio: NIP", "HotLeadsW1": "Rescate Tasa 0 a leads recientes",
       "BBDDRezagada-RescateTasa0": "Rescate Tasa 0 a rezagados", "T2728": "Recordatorio KPay: NIP con cupón", "T2706": "Recordatorio KPay: crear cuenta", "Installments_SP": "Meses sin intereses a nuevos"}
def nom(f): return [v for kk, v in NOM.items() if kk in f][0]
S = SVG("Apertura del correo de recordatorio de registro según los días desde que la persona se quedó en un paso, y personas nuevas que se dieron de baja el día de cada campaña")
S.t(0, 14, "Recordatorio de KPay: % que abrió cada correo", 12, INK, w=700)
S.t(0, 30, "Días desde que la persona se quedó en el paso", 10.5, SEC)
DAYS = [0, 1, 3, 7, 10, 15, 30]; X0, W0, Y0, HH = 36, 300, 56, 230
xs = lambda d: X0 + W0 * DAYS.index(d) / (len(DAYS) - 1)
ys = lambda v: Y0 + HH - HH * v / 40
for v in (0, 10, 20, 30, 40):
    S.line(X0, ys(v), X0 + W0, ys(v), GRID); S.t(X0 - 6, ys(v) + 4, f"{v} %", 10.5, SEC, "end")
for d in DAYS: S.t(xs(d), Y0 + HH + 15, "5 min" if d == 0 else f"día {d}", 10.5, SEC, "middle")
COL = {"Crear la cuenta": BLUE, "Verificar identidad": INK, "Datos personales": MARK}
LY = {"Crear la cuenta": 10, "Verificar identidad": -8, "Datos personales": -8}
for t, col in COL.items():
    g = G.loc[t]
    pts = [(xs(d), ys(g.loc[d, "p"])) for d in DAYS if d in g.index]
    S.raw('<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f'" fill="none" stroke="{col}" stroke-width="2.2"/>')
    for d in DAYS:
        if d in g.index: S.circle(xs(d), ys(g.loc[d, "p"]), 3.5, col, "#FFFFFF", 1.2)
    S.t(xs(0) + 6, ys(g.loc[0, "p"]) + (14 if t == "Datos personales" else -7), f"{g.loc[0,'p']:.0f} %", 10.5, col, "start", 700, halo=True)
    S.t(xs(30) + 0, ys(g.loc[30, "p"]) + LY[t] + (0 if LY[t] < 0 else 4), f"{t} · {g.loc[30,'p']:.0f} %", 10.5, col, "end", 600, halo=True)
ac = G.loc["Crear la cuenta"]
# derecha: bajas de nuevos
RX0, RX1, VM = 604, 744, 60000
S.line(400, 8, 400, 330, GRID)
S.t(414, 14, "Personas nuevas que se dieron de baja", 12, INK, w=700)
S.t(414, 30, f"el día que les llegó cada campaña (de {NT/1e3:.0f} mil nuevos con baja)", 10.5, SEC)
for i, (_, r) in enumerate(top.iterrows()):
    y = 52 + 34 * i
    col = BLUE if r.rec else MARK2
    S.t(414, y + 10, nom(r.clave), 10.5, INK, w=600 if r.rec else 400)
    S.t(414, y + 23, f"a los {int(r.dias_mediana)} días, tras {int(r.emails_mediana)} correos" if r.dias_mediana < 60 else f"a los {int(r.dias_mediana)} días", 10.5, SEC)
    S.rect(RX0, y + 4, (RX1 - RX0) * r.usuarios / VM, 14, col)
    S.t(RX0 + (RX1 - RX0) * r.usuarios / VM + 4, y + 15, f"{r.usuarios/1e3:.1f} mil", 10.5, INK, w=600)
S.t(414, 336, "Mediana de días desde el registro y de correos recibidos.", 10.5, SEC)
S.t(0, 360, "Azul a la derecha: recordatorios de registro. Los recordatorios de KCash (Marketing) no traen sus pasos en el embudo; la cadencia es la de KPay.", 10.5, SEC)
V = byq[byq.index.str.endswith("Retargeting_Veriff")].sort_values("d").iloc[-1]; PI = byq.loc[[f for f in byq.index if f.endswith("Retargeting_PersonalInfo")][0]]; NIP = byq.loc[[f for f in byq.index if f.endswith("Retargeting_NIP")][0]]
J = dict(
    titulo="El recordatorio de terminar el registro sí funciona, pero llega tantas veces que causa una de cada cinco bajas de las personas nuevas",
    que="Correos, push e in-app que recuerdan terminar un paso del registro: verificar identidad (Veriff), datos personales, NIP, dirección, crear la cuenta. Es de activación, no una oferta.",
    quien=f"Marketing en KCash ({rec[rec.equipo=='Marketing'].envios.sum()/1e6:.0f} M mensajes) y Acquisition en KPay ({rec[rec.equipo=='Others'].envios.sum()/1e6:.0f} M; cae en Others).",
    a_quien="Personas que empezaron a pedir su crédito KCash o su cuenta KPay y se quedaron en un paso.",
    lecturas=[
        f"Funciona: Veriff recibe {V.cpm:.0f} clics por cada mil correos, datos personales {PI.cpm:.0f} y NIP {NIP.cpm:.0f}, diez veces lo mínimo; quien abre el de Veriff convierte {vz.conv_abren_pct:.1f} % contra {vz.conv_no_abren_pct:.1f} % de quien no lo abre.",
        f"En KPay el correo de los 5 minutos lo abre {ac.loc[0,'p']:.0f} % y del día 3 al 15 solo {ac.loc[[3,7,10,15],'p'].min():.1f} a {ac.loc[[3,7,10,15],'p'].max():.1f} %: los dos primeros correos hacen casi todo el trabajo.",
        f"En KCash cada persona recibe unos {vz.toques_usuario_mes:.0f} correos al mes; los nuevos que se dan de baja lo hacen a los 3 o 4 días, después de 4 a 6 correos. Veriff, datos personales y NIP suman {kc.usuarios.sum()/1e3:.0f} mil bajas, {100*kc.usuarios.sum()/NT:.0f} % de las de nuevos.",
    ],
    causa="Cada paso pendiente dispara su propia secuencia de siete correos en 30 días, y no hay un límite de mensajes por persona a la semana que las coordine.",
    sowhat="No hay que quitar el recordatorio: dejar los dos primeros correos, pasar el resto a push o in-app y poner un límite de tres mensajes en la primera semana.",
    fuente=f"Fuente: Braze, embudo por paso de Canvas (Acquisition KPay T2706, T2727 y T2728), envíos por campaña y canal, y día de la baja de cada persona con la campaña que recibió ese día (cohorte de personas nuevas), enero a septiembre 2026. Correos de recordatorio en el año: {re_.email_delivery.sum()/1e6:.1f} M entregados. Las bajas por campaña son personas, no eventos.",
    svg=S.out())
write(79, J)
