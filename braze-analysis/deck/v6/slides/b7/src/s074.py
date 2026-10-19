"""Lámina 74: campañas con más versiones nuevas en 2026: por mes, cuántas versiones nuevas salieron (círculo) y cuántos mensajes mandó
la campaña (barra gris). Fuente: E2 (catálogo, primer envío) y E1 (mensajes por mes). Campaña = nombre sin fecha."""
from b7 import *

c2 = pd.read_csv(D + "e2_catalogo.csv", low_memory=False)
c2["fam"] = c2.nombre.fillna("").map(fam_of); c2["equipo"] = c2.team_limpio.map(team_of)
c2["fs"] = pd.to_datetime(c2.first_sent, errors="coerce")
v = c2[(c2.fs >= "2026-01-01") & (c2.fs < "2026-10-01")].copy(); v["m"] = v.fs.dt.month
g = v.groupby("fam").agg(n=("communication_id", "nunique"), equipo=("equipo", "first"))
G = g[g.n >= 5]
e = load_e1(); fe = e[e.envios > 0]
envG = e[e.fam.isin(G.index)]
sp = fe[fe.m == 9].groupby("fam").communication_id.nunique()
eqG = G.groupby("equipo").agg(f=("n", "size"), v=("n", "sum"))
print(len(G), G.n.sum(), v.communication_id.nunique(), envG.envios.sum() / 1e6, (sp >= 2).sum(), sp[sp >= 2].sum()); print(eqG)
print(envG.groupby("canal").envios.sum() / 1e6)
G2 = G.copy(); G2["tema"] = G2.index.map(tema); print(G2.groupby("tema").agg(f=("n", "size"), v=("n", "sum")).sort_values("v", ascending=False).head(6))
top = G.sort_values("n", ascending=False).head(10)
NOM = {"B0210": "Tasa 0 a registrados que nunca usaron KCash", "T2778": "Buenas prácticas para adultos mayores", "B0337": "Cuesta de Enero a clientes elegibles",
       "B0223": "Crédito en plazos a quien nunca lo activó", "Leads_BBDDRezagada-RescateTasa0": "Rescate Tasa 0 a leads rezagados", "B0333": "Oferta a ex clientes KPay, 12 meses sin compra",
       "B0291": "50 % de descuento a clientes recurrentes", "B0212": "Invitación sin oferta a nuevos de Temu", "B0493": "Hot Sale a clientes recurrentes de KPay",
       "HotLeadsW1RescateTasa0": "Rescate Tasa 0 a leads recientes"}
def nom(f): return [vv for k, vv in NOM.items() if k in f][0]
S = SVG("Campañas con más versiones nuevas en 2026: versiones que salieron cada mes y mensajes que mandó cada campaña")
S.legend([("Versiones nuevas que salieron ese mes (número)", BLUE, "ci"), ("Mensajes de la campaña ese mes", MARK2, "sq")], 0, 14, 18)
X0, CW, TOP, RH = 292, 40, 56, 33
BMAX = 4e6
for j, mm in enumerate(MESES):
    S.t(X0 + CW * j + CW / 2, TOP - 8, mm, 11, SEC, "middle")
S.t(780, TOP - 8, "Versiones · mensajes", 11, SEC, "end", 600)
S.t(0, TOP - 8, "Campaña · equipo", 11, SEC, w=600)
for i, (f, r) in enumerate(top.iterrows()):
    y = TOP + RH * i
    S.line(0, y + RH - 4, 780, y + RH - 4, GRID)
    S.t(0, y + 12, nom(f), 11.5, INK, w=600); S.t(0, y + 25, r.equipo, 10.5, SEC)
    mm = e[e.fam == f].groupby("m").envios.sum()
    nv = v[v.fam == f].groupby("m").communication_id.nunique()
    for j in range(9):
        m = j + 1; cx = X0 + CW * j + CW / 2
        h = 11 * min(mm.get(m, 0), BMAX) / BMAX
        if h > 0: S.rect(cx - 14, y + 29 - h, 28, max(h, 1), MARK2)
        k = nv.get(m, 0)
        if k:
            S.circle(cx, y + 9, 5 + 1.3 * k ** 0.5, BLUE, "#FFFFFF", 1.2)
            S.t(cx, y + 13, f"{k}", 10.5, "#FFFFFF", "middle", 700)
    S.t(780, y + 18, f"{int(r.n)} · {mm.sum()/1e6:.1f} M", 11.5, INK, "end", 700)
yy = TOP + RH * 10 + 12
S.t(0, yy, f"Barra gris: de 0 a {BMAX/1e6:.0f} M mensajes al mes (más se dibuja al tope).", 10.5, SEC)
S.t(0, yy + 15, "Cada versión es una copia con otra fecha en el nombre; casi todas son Canvas que mandan por varios canales.", 10.5, SEC)
J = dict(
    titulo=f"En vez de medir una campaña la copiamos cada mes: {len(G)} campañas sacaron cinco o más versiones",
    que="Tasa 0, ofertas para volver, comercios KPay y referidos.",
    quien=f"Product Growth {eqG.loc['Product Growth','f']} campañas, Marketing {eqG.loc['Marketing','f']}, Sales {eqG.loc['Sales','f']} y Others {eqG.loc['Others','f']}.",
    a_quien="Registrados sin crédito, leads, ex clientes y recurrentes.",
    lecturas=[
        f"Sacaron {G.n.sum()} versiones nuevas en 2026 y mandaron {envG.envios.sum()/1e6:.0f} M mensajes, {100*envG.envios.sum()/e.envios.sum():.0f} % del año.",
        f"En septiembre {(sp>=2).sum()} campañas tenían dos o más versiones enviando a la vez ({sp[sp>=2].sum()} versiones).",
        "Tasa 0 a quien nunca usó KCash sacó una o dos versiones cada mes; nadie compara la nueva con la anterior.",
    ],
    causa="Duplicar un Canvas y cambiar la fecha es más fácil que leer cómo le fue al anterior.",
    sowhat="Una sola versión viva por campaña, y comparar contra la anterior antes de copiar.",
    fuente="Fuente: Braze, catálogo (primer envío en 2026) y envíos por comunicación y mes, ene a sep 2026. Campaña = nombre sin fecha; versión = cada copia con su fecha.",
    svg=S.out())
write(74, J)
