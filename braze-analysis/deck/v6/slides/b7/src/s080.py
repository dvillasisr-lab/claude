"""Lámina 80: comunicaciones con nombre de prueba o copia que mandaron mensajes. Tres grupos: push sin aperturas (casi solo push, menos de
1 apertura por mil), envío real (mil personas o más y respuesta normal) y prueba chica (menos de mil personas). Fuente: E1; riesgo de E5b y E7a."""
from b7 import *

e = load_e1()
pat = r"(?i)prueba|test|\bqa\b|qa_|copy of|copia|dummy|demo"
p = e[e.communication_name.str.contains(pat) & (e.envios > 0)].copy()
g = p.groupby("communication_id").agg(name=("communication_name", "first"), env=("envios", "sum"), usu=("usuarios_aprox", "max"), pn=("pn_send", "sum"), pno=("pn_open", "sum"),
                                      ed=("email_delivery", "sum"), ec=("email_click", "sum"), wd=("whatsapp_delivery", "sum"), wr=("whatsapp_read", "sum"), costo=("costo", "sum"),
                                      conv=("conversiones_filas", "sum"), team=("team", "first"))
g["po"] = 1000 * g.pno / g.pn.replace(0, np.nan)
def cl(r):
    if r.usu < 1000: return "chica"
    if r.pn >= 0.9 * r.env and (np.isnan(r.po) or r.po < 1): return "push"
    return "real"
g["cl"] = g.apply(cl, axis=1)
G = g.groupby("cl").agg(n=("env", "size"), env=("env", "sum"), usu=("usu", "sum"), costo=("costo", "sum"), conv=("conv", "sum"), pn=("pn", "sum"), pno=("pno", "sum"), ed=("ed", "sum"), ec=("ec", "sum"))
print(len(g), g.env.sum() / 1e6); print(G)
b = pd.read_csv(D + "e5b_comms_despues_baja.csv"); pb = b[b.familia.str.contains("PRUEBA_", na=False)].emails_despues_de_baja.sum()
a = pd.read_csv(D + "e7a_familia_canal_etapa.csv"); qa = a[a.familia.str.contains("QA-KPay-20260811-B001", na=False)].groupby("etapa").envios.sum()
print(pb, qa.to_dict())
TEAMN = lambda t, n: "Collections" if t == "Collections" else ("Sales" if t == "Sales" else ("Marketing" if t == "Marketing" else "Others"))
def clean(n):
    m = {"QA-KPay-20260811-B001": "QA-KPay: recordatorio por teléfono", "QA_CC-More3k": "QA_CC (más de 3 mil)", "QA_CC": "QA_CC",
         "Copy of QA-Sales-KPay-20260518-B0490": "Copia QA: Amazon Pre Hot Sale", "Copy of Marketing-KPay-20260121-Recurrentes-Performance": "Copia de Performance KPay (Marketing)",
         "Copy of Lending-KPay-20260706-B0332": "Copia: ex clientes KPay, 6 meses", "Copy of Acquisition-KPay-20241112-T2727": "Copia: recordatorio Veriff de KPay",
         "Copy of Sales-KPay-20260216-B0317-CANVAS-Recurrentes": "Copia: lanzamiento Iberia (Sales)", "PRUEBA_Collections-KCash-20230531-T000-CANVAS-BKT1": "PRUEBA_ cobranza BKT1 (Collections)",
         "PRUEBA_Collections-KCash-20250819": "PRUEBA_ precobranza (Collections)"}
    for k, v in m.items():
        if n.startswith(k): return v
    import re as _re
    return _re.sub(r"-\d{8,9}|-CANVAS|-N/A|-NA$", "", n)
S = SVG("Comunicaciones con nombre de prueba o copia: mensajes, personas y respuesta en tres grupos, con los casos más grandes")
GR = [("push", "Push que casi nadie abrió", "Probablemente técnicos o silenciosos"), ("real", "Campañas reales mal nombradas", "La operación normal, con nombre de prueba"),
      ("chica", "Pruebas de verdad", "Menos de mil personas cada una")]
CW = 260
VM = 5e6
for j, (k, t1, t2) in enumerate(GR):
    x0 = j * CW + 4; q = G.loc[k]
    col = BLUE if k == "real" else (MARK if k == "push" else GREENL)
    S.t(x0, 16, t1, 12, INK, w=700); S.t(x0, 32, t2, 10.5, SEC)
    S.t(x0, 66, f"{q.env/1e6:.2f} M" if q.env >= 1e5 else f"{q.env/1e3:.0f} mil", 26, INK if k != "real" else BLUE, w=700)
    S.t(x0, 84, f"mensajes, en {int(q.n)} comunicaciones", 10.5, SEC)
    S.rect(x0, 94, (CW - 30) * q.env / VM, 10, col)
    if k == "push": resp = f"{1000*q.pno/q.pn:.2f} aperturas por cada mil push"
    elif k == "real": resp = f"{1000*q.ec/q.ed:.0f} clics por mil correos; {q.conv/1e3:.1f} mil conversiones"
    else: resp = f"{q.usu/1e3:.0f} mil personas en total"
    S.t(x0, 124, resp, 10.5, INK, w=600)
    if k == "real": S.t(x0, 138, f"{q.costo/1e3:.0f} mil MXN de gasto", 10.5, INK, w=600)
    S.line(x0, 152, x0 + CW - 20, 152, GRID)
    S.t(x0, 168, "Casos más grandes", 10.5, SEC, w=600)
    d = g[g.cl == k].sort_values("env", ascending=False).head(4)
    for i, (_, r) in enumerate(d.iterrows()):
        y = 186 + 40 * i
        nm = clean(r["name"])
        if len(nm) > 36: nm = nm[:35] + "…"
        S.t(x0, y, nm, 10.5, INK, w=600)
        if k == "push": det = f"{r.env/1e6:.2f} M push · {r.usu/1e3:.0f} mil personas · {r.po:.1f} por mil"
        elif k == "real":
            det = f"{r.env/1e3:.0f} mil mensajes · " + (f"WhatsApp {100*r.wr/r.wd:.0f} % leído" if r.wd else (f"{1000*r.ec/r.ed:.0f} clics por mil" if r.ed else f"push {r.po:.0f} por mil"))
        else: det = f"{r.env:,.0f} mensajes · {r.usu:,.0f} personas"
        S.t(x0, y + 14, det, 10.5, TXT)
S.line(0, 352, 780, 352, MARK)
S.tspans(0, 372, [("Lo que sí es riesgo: ", INK, 700), (f"las PRUEBA_ de cobranza mandaron {pb/1e3:.1f} mil correos a gente ya dada de baja; ", TXT, 400)], 11)
S.t(0, 388, f"QA-KPay llegó a {qa.get('6.Reus or Arco',0)/1e3:.1f} mil personas que pidieron no recibir publicidad (REUS o ARCO), {qa.get('3.Blacklist',0)/1e3:.1f} mil en lista negra y {qa.get('4.Kpay CC Freeze',0)/1e3:.0f} mil con tarjeta congelada.", 11, TXT)
J = dict(
    titulo="Lo que parecían pruebas a clientes son, sobre todo, push que casi nadie abrió y campañas reales con nombre de prueba",
    que="Comunicaciones con QA, Test, Prueba o 'Copy of' en el nombre que mandaron mensajes: push técnicos, recordatorios, cobranza y promociones reales.",
    quien=f"Others (QA, Acquisition, Compliance) {g[g.team.map(team_of)=='Others'].env.sum()/1e6:.1f} M mensajes; Sales {g[g.team=='Sales'].env.sum()/1e6:.1f} M (copias de Iberia y 4QSI); Collections {g[g.team=='Collections'].env.sum()/1e6:.1f} M (PRUEBA_ de cobranza). Las copias quedan sin equipo y caen en Others.",
    a_quien="Clientes reales: hasta 1.8 M personas en un solo envío.",
    lecturas=[
        f"{int(G.loc['push','n'])} push con {G.loc['push','env']/1e6:.1f} M mensajes tuvieron menos de 1 apertura por cada mil: varios dicen 'Silent_Push' en el nombre. No sabemos si la persona los vio.",
        f"{int(G.loc['real','n'])} campañas reales con nombre de prueba o copia mandaron {G.loc['real','env']/1e6:.1f} M mensajes y responden como cualquier campaña: la copia del programa de ex clientes KPay, el recordatorio Veriff de KPay y la cobranza PRUEBA_.",
        f"Las pruebas de verdad son {int(G.loc['chica','n'])} envíos a menos de mil personas: {G.loc['chica','env']/1e3:.0f} mil mensajes, sin problema.",
    ],
    causa="Al copiar un Canvas para probarlo, Braze le pone 'Copy of' y nadie lo renombra antes de usarlo con clientes; las copias pierden el equipo y el ticket.",
    sowhat="El problema no es probar con clientes: es que el nombre no dice qué es, y así nadie puede auditarlo ni medirlo. Renombrar antes de activar.",
    fuente=f"Fuente: Braze, envíos por comunicación, mes y canal, enero a septiembre 2026; {len(g)} comunicaciones con QA, Test, Prueba, Copy of, copia, dummy o demo en el nombre y algún mensaje enviado. Riesgo: correos después de la baja y etapa del usuario (golden dataset). Para confirmar si un push era silencioso falta el tipo de mensaje del paso.",
    svg=S.out())
write(80, J)
