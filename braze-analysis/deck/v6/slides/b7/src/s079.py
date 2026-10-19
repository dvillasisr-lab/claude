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
S = SVG("Apertura de cada correo del recordatorio de registro de KPay según los días desde que la persona se quedó en un paso; una línea por Canvas")
S.legend([("Un Canvas (versión)", MARK2, "ln"), ("Promedio ponderado por personas", BLUE, "ln")], 0, 14, 18)
DAYS = [0, 1, 3, 7, 10, 15, 30]
TIP = [("Crear la cuenta", "T2706 y T2727"), ("Verificar identidad", "T2727"), ("Datos personales", "T2728")]
CW = 262; Y0, HH = 70, 290
ys = lambda v: Y0 + HH - HH * min(v, 40) / 40
for j, (t, cod) in enumerate(TIP):
    x0 = 40 + CW * j; w = CW - 56
    xs = lambda d, x0=x0, w=w: x0 + w * DAYS.index(d) / (len(DAYS) - 1)
    S.t(x0 - 30, Y0 - 26, t, 12, INK, w=700); S.t(x0 - 30, Y0 - 12, f"Acquisition KPay {cod}", 10.5, SEC)
    for v in (0, 10, 20, 30, 40):
        S.line(x0, ys(v), x0 + w, ys(v), GRID)
        if j == 0 and v > 0: S.t(x0 - 6, ys(v) + 4, f"{v} %", 10.5, SEC, "end")
    for d in DAYS: S.t(xs(d), Y0 + HH + 15, "5 min" if d == 0 else f"{d}", 10.5, SEC, "start" if d == 0 else "middle")
    kk = k[k.tipo == t]
    for cid, gg in kk.groupby("canvas_id"):
        gg = gg.groupby("dia").agg(u=("usuarios", "sum"), ab=("ab", "sum"))
        gg = gg[gg.u >= 1000]
        if len(gg) < 3: continue
        pts = [(xs(d), ys(100 * gg.loc[d, "ab"] / gg.loc[d, "u"])) for d in DAYS if d in gg.index]
        S.raw('<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f'" fill="none" stroke="{MARK2}" stroke-width="1.2"/>')
    g = G.loc[t]
    pts = [(xs(d), ys(g.loc[d, "p"])) for d in DAYS if d in g.index]
    S.raw('<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f'" fill="none" stroke="{BLUE}" stroke-width="2.6"/>')
    for d in DAYS: S.circle(xs(d), ys(g.loc[d, "p"]), 3.5, BLUE, "#FFFFFF", 1.2)
    S.t(xs(0) + 5, ys(g.loc[0, "p"]) - 8, f"{g.loc[0,'p']:.0f} %", 11, BLUE, "start", 700, halo=True)
    S.t(xs(7), ys(g.loc[7, "p"]) + 16, f"{g.loc[7,'p']:.0f} %", 11, BLUE, "middle", 700, halo=True)
S.t(780, Y0 + HH + 30, "Días desde que la persona se quedó en el paso", 10.5, SEC, "end")
S.t(0, 410, "Los recordatorios de KCash (Marketing) no traen sus pasos en el embudo; la cadencia mostrada es la de KPay.", 10.5, SEC)
ac = G.loc["Crear la cuenta"]
V = byq[byq.index.str.endswith("Retargeting_Veriff")].sort_values("d").iloc[-1]; PI = byq.loc[[f for f in byq.index if f.endswith("Retargeting_PersonalInfo")][0]]; NIP = byq.loc[[f for f in byq.index if f.endswith("Retargeting_NIP")][0]]
J = dict(
    titulo="El recordatorio de registro sí funciona, pero llega tantas veces que causa una de cada cinco bajas de nuevos",
    que="Recordatorios de terminar el registro: verificar identidad, datos, NIP, dirección.",
    quien=f"Marketing en KCash ({rec[rec.equipo=='Marketing'].envios.sum()/1e6:.0f} M mensajes) y Acquisition en KPay (Others).",
    a_quien="Quien empezó a pedir su crédito o su cuenta y se quedó en un paso.",
    lecturas=[
        f"Veriff recibe {V.cpm:.0f} clics por mil correos y NIP {NIP.cpm:.0f}; quien abre Veriff convierte {vz.conv_abren_pct:.1f} % contra {vz.conv_no_abren_pct:.1f} %.",
        f"En KPay el correo de los 5 minutos lo abre {ac.loc[0,'p']:.0f} % y el del día 7 solo {ac.loc[7,'p']:.0f} %.",
        f"Veriff, datos y NIP causan {kc.usuarios.sum()/1e3:.0f} mil bajas de nuevos ({100*kc.usuarios.sum()/NT:.0f} %), a los 3 o 4 días.",
    ],
    causa="Cada paso pendiente manda siete correos en 30 días y no hay límite de mensajes por persona.",
    sowhat="Dejar los dos primeros correos, pasar el resto a push o in-app y limitar a tres la primera semana.",
    fuente="Fuente: Braze, embudo por paso de Canvas (Acquisition KPay), envíos por campaña y día de la baja de cada persona nueva, ene a sep 2026. Líneas con mil personas o más por paso.",
    svg=S.out())
write(79, J)
