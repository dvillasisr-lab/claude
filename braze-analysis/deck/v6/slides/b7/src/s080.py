"""Lámina 80: comunicaciones con nombre de prueba o copia que mandaron mensajes. Tres grupos: push sin aperturas (casi solo push, menos de
1 apertura por mil), envío real (mil personas o más y respuesta normal) y prueba chica (menos de mil personas). Fuente: E1; riesgo de E5b y E7a."""
from b7 import *

e = load_e1()
pat = r"(?i)prueba|test|\bqa\b|qa_|copy of|copia|dummy|demo"
p = e[e.communication_name.str.contains(pat) & (e.envios > 0)].copy()
g = p.groupby("communication_id").agg(name=("communication_name", "first"), env=("envios", "sum"), usu=("usuarios_aprox", "max"), pn=("pn_send", "sum"), pno=("pn_open", "sum"),
                                      ed=("email_delivery", "sum"), ec=("email_click", "sum"), wd=("whatsapp_delivery", "sum"), wr=("whatsapp_read", "sum"), costo=("costo", "sum"),
                                      conv=("conversiones_fraccional", "sum"), team=("team", "first"))
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
import math
def vmin(r):
    best = None
    for ch, base, rr in (("email", r.ed, r.ec), ("push notification", r.pn, r.pno), ("whatsapp", r.wd, r.wr)):
        if base > 0 and (best is None or base > best[1]): best = (ch, base, rr)
    if best is None: return np.nan
    return (100 * best[2] / best[1]) / MIN[best[0]]
g["vx"] = g.apply(vmin, axis=1)
S = SVG("Comunicaciones con nombre de prueba o copia: personas alcanzadas contra respuesta en veces lo mínimo, en tres grupos")
COLS = {"push": (MARK, f"Push que casi nadie abrió ({int(G.loc['push','n'])})"), "real": (BLUE, f"Campaña real mal nombrada ({int(G.loc['real','n'])})"), "chica": (GREENL, f"Prueba chica ({int(G.loc['chica','n'])})")}
S.legend([(v[1], v[0], "ci") for v in COLS.values()], 0, 14, 16)
X0, X1, Y0, Y1 = 44, 770, 44, 360
L0, L1 = 0, math.log10(3e6); YL0, YL1 = math.log10(0.003), math.log10(30)
xs = lambda v: X0 + (X1 - X0) * (math.log10(max(v, 1)) - L0) / (L1 - L0)
ys = lambda v: Y1 - (Y1 - Y0) * (math.log10(min(max(v, 0.003), 30)) - YL0) / (YL1 - YL0)
for v, l in ((0.003, "0"), (0.01, "0.01"), (0.1, "0.1"), (1, "1"), (10, "10")):
    S.line(X0, ys(v), X1, ys(v), GRID); S.t(X0 - 6, ys(v) + 4, l, 10.5, SEC, "end")
for v, l in ((1, "1"), (100, "100"), (1e3, "mil"), (1e4, "10 mil"), (1e5, "100 mil"), (1e6, "1 M")):
    S.t(xs(v), Y1 + 14, l, 10.5, SEC, "middle" if v > 1 else "start")
S.t(X1, Y1 + 30, "Personas que la recibieron en su mes más grande (escala que multiplica)", 10.5, SEC, "end")
S.t(X0 + 4, Y0 - 6, "Respuesta en veces lo mínimo de su canal principal", 10.5, SEC)
S.line(X0, ys(1), X1, ys(1), INK, 1.2, ' stroke-dasharray="4 4"')
S.t(X0 + 4, ys(1) - 5, "Lo mínimo aceptable", 10.5, INK, w=600, halo=True)
S.line(xs(1000), Y0, xs(1000), Y1, MARK, 1)
S.t(xs(1000) - 5, Y0 + 12, "prueba chica", 10.5, SEC, "end", halo=True); S.t(xs(1000) + 5, Y0 + 12, "llegó a clientes", 10.5, SEC, "start", halo=True)
for k in ("chica", "push", "real"):
    for _, r in g[g.cl == k].iterrows():
        S.circle(xs(r.usu), ys(r.vx if not np.isnan(r.vx) else 0.003), 3.2 if k != "real" else 4.5, COLS[k][0], "#FFFFFF", 0.8)
LAB = [("QA-KPay-20260811-B001", "QA-KPay recordatorio: 1.9 M push · Others", 740, 300, "end"),
       ("Copy of Lending-KPay-20260706-B0332", "Copia de ex clientes KPay, 6 meses · Product Growth", 740, 140, "end"),
       ("Copy of Acquisition-KPay-20241112-T2727", "Copia del recordatorio Veriff KPay · Acquisition", 560, 92, "end"),
       ("PRUEBA_Collections-KCash-20250819", "PRUEBA_ precobranza · Collections", 740, 112, "end"),
       ("Copy of Sales-KPay-20260216-B0317-CANVAS-Recurrentes", "Copia de lanzamiento Iberia · Sales", 740, 196, "end")]
for kname, lab, lx, ly, an in LAB:
    r = g[g["name"].str.startswith(kname)].sort_values("env").iloc[-1]
    S.line(xs(r.usu), ys(r.vx if not np.isnan(r.vx) else 0.003), lx + 3, ly - 4, MARK, 1)
for kname, lab, lx, ly, an in LAB:
    S.t(lx, ly, lab, 10.5, INK, an, 600, halo=True)
S.t(X1, Y1 - 6, f"Riesgo: PRUEBA_ de cobranza mandó {pb/1e3:.1f} mil correos a gente dada de baja", 10.5, BLUE, "end", 600, halo=True)
J = dict(
    titulo="Lo que parecían pruebas a clientes son sobre todo push que nadie abrió y campañas reales mal nombradas",
    que="Comunicaciones con QA, Test, Prueba o 'Copy of' en el nombre que sí mandaron.",
    quien="Others (QA, Acquisition, Compliance) casi todo; Sales y Collections, poco.",
    a_quien="Clientes reales: hasta 1.9 M push en un solo envío.",
    lecturas=[
        f"{int(G.loc['push','n'])} push mandaron {G.loc['push','env']/1e6:.1f} M mensajes con menos de 1 apertura por mil; varios son silenciosos.",
        f"{int(G.loc['real','n'])} campañas reales mal nombradas mandaron {G.loc['real','env']/1e6:.1f} M mensajes y responden como cualquier campaña.",
        f"Las pruebas de verdad son {int(G.loc['chica','n'])} envíos a menos de mil personas: {G.loc['chica','env']/1e3:.0f} mil mensajes.",
    ],
    causa="Al copiar un Canvas, Braze le pone 'Copy of' y nadie lo renombra antes de usarlo con clientes.",
    sowhat="El problema no es probar con clientes: es que el nombre no dice qué es. Renombrar antes de activar.",
    fuente=f"Fuente: Braze, envíos por comunicación y canal, ene a sep 2026; {len(g)} comunicaciones con nombre de prueba o copia. Falta el tipo de push para confirmar si era silencioso.",
    svg=S.out())
write(80, J)
