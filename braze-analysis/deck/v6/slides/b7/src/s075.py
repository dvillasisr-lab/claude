"""Lámina 75 (cifra grande): inventario de Braze. Fuente: E2 (catálogo: tipo, estado, primer y último envío al 7 de octubre)
y E1 (comunicaciones con algún mensaje enviado por mes y canal)."""
from b7 import *

c2 = pd.read_csv(D + "e2_catalogo.csv", low_memory=False)
c2["ls"] = pd.to_datetime(c2.last_sent, errors="coerce"); c2["fs"] = pd.to_datetime(c2.first_sent, errors="coerce")
c2["cr"] = pd.to_datetime(c2.created_at.str[:10], errors="coerce")
e = load_e1()
e["an"] = e[["envios", "email_sent", "pn_send", "whatsapp_send", "in_app_impression", "banner_impression"]].fillna(0).sum(axis=1) > 0
fe = e[e.an]
ids, ids9 = set(fe.communication_id), set(fe[fe.m == 9].communication_id)
c2["per"] = c2.communication_id.isin(ids); c2["sep"] = c2.communication_id.isin(ids9)
c2["na"] = c2.estado == "activa"; ref = pd.Timestamp("2026-10-07")
pat = r"(?i)prueba|test|\bqa\b|qa_|copy of|copia|dummy|demo"
c2["pr"] = c2.nombre.fillna("").str.contains(pat)
N = len(c2); tp = c2.tipo_pieza.value_counts()
nper, nsep = len(ids), len(ids9); fper, fsep = fe.fam.nunique(), fe[fe.m == 9].fam.nunique()
cre = int(((c2.fs >= "2026-01-01") & (c2.fs < "2026-10-01")).sum()); cre_c = int((c2.cr >= "2026-01-01").sum())
cre_per = int((c2.per & (c2.fs >= "2026-01-01")).sum())
sin90 = int((c2.na & (c2.ls.isna() | (c2.ls < ref - pd.Timedelta(days=90)))).sum())
arch9 = int((~c2.na & c2.sep).sum())
pr, prp = int(c2.pr.sum()), int((c2.pr & c2.per).sum())
ch = fe.groupby("canal").communication_id.nunique(); ch9 = fe[fe.m == 9].groupby("canal").communication_id.nunique()
eq = fe.groupby("equipo").communication_id.nunique(); eq9 = fe[fe.m == 9].groupby("equipo").communication_id.nunique()
print("estrenadas que mandaron", cre_per); print(N, tp.to_dict(), nper, fper, nsep, fsep, cre, cre_c, c2.na.sum(), sin90, arch9, pr, prp, e.communication_id.nunique())
n = lambda v: f"{int(v):,}"
CARDS = [(n(N), "comunicaciones guardadas", f"{n(tp['canvas'])} Canvas y {n(tp['campaign'])} campañas sueltas", "#0B1220"),
         (n(nper), "mandaron algo en 2026", f"son {n(fper)} campañas sin contar la fecha del nombre", "#0B1220"),
         (n(nsep), "mandaron algo en septiembre", f"{n(fsep)} campañas; una de cada 18 guardadas", "#1F4FD8"),
         (n(arch9), "archivadas que siguen enviando", "mandaron en septiembre aunque dicen archivada", "#1F4FD8")]
html = ('<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:2.2cqi 2.4cqi;margin-top:1cqi">' +
        "".join(f'<div style="border-top:2px solid {col};padding-top:.8cqi"><div class="big" style="color:{col}">{v}</div><div style="font-size:1.15cqi;font-weight:600;color:#0B1220;margin-top:.4cqi">{t1}</div><div class="bigl">{t2}</div></div>' for v, t1, t2, col in CARDS) + '</div>')
J = dict(
    kind="html",
    titulo=f"Braze tiene {n(N)} comunicaciones guardadas, pero en septiembre solo {n(nsep)} mandaron algo",
    que="Comunicación = cada Canvas o campaña suelta guardada en Braze.",
    quien=f"En septiembre: Product Growth {n(eq9['Product Growth'])}, Others {n(eq9['Others'])}, Marketing {n(eq9['Marketing'])}, Sales {n(eq9['Sales'])}.",
    a_quien="No aplica: es el inventario de Braze.",
    lecturas=[
        f"{n(cre)} comunicaciones se estrenaron de enero a septiembre, unas {cre/9:.0f} al mes.",
        f"{arch9} marcadas como archivadas mandaron en septiembre: el estado no dice qué sigue vivo.",
        f"{pr} tienen nombre de prueba o copia; {prp} mandaron mensajes reales en 2026.",
    ],
    causa="Cada mes se copia en vez de editar, nadie depura el catálogo y el nombre no sigue una regla.",
    sowhat="Limpiar el catálogo, archivar lo que no manda y nombrar con una regla es trabajo de una vez.",
    fuente="Fuente: Braze, catálogo al 7 de octubre 2026 y envíos por comunicación y canal, ene a sep 2026. Mandó algo = al menos un mensaje enviado.",
    html=html)
write(75, J)
