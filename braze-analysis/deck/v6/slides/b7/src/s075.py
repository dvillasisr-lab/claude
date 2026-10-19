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
bar = lambda v, mx, col: f'<div style="height:.7cqi;width:{max(0.3, 100*v/mx):.1f}%;background:{col}"></div>'
rows = [(f"Guardadas en Braze ({n(tp['canvas'])} Canvas y {n(tp['campaign'])} campañas)", N, MARK),
        (f"Mandaron al menos un mensaje en 2026 ({n(fper)} campañas)", nper, MARK),
        (f"Con nombre de prueba o copia ({n(prp)} mandaron en 2026)", pr, MARK),
        (f"Mandaron algo en septiembre ({n(fsep)} campañas)", nsep, BLUE)]
t1 = "".join(f'<tr><td style="width:58%">{a}</td><td class="num" style="width:12%;font-weight:700;color:{"#1F4FD8" if col == BLUE else "#0B1220"}">{n(b)}</td><td style="vertical-align:middle">{bar(b, N, col)}</td></tr>' for a, b, col in rows)
CH = [("email", "Email"), ("push notification", "Push"), ("in-app", "In-app"), ("whatsapp", "WhatsApp")]
t2 = "".join(f'<tr><td>{lab}</td><td class="num">{n(ch.get(k,0))}</td><td class="num"><b>{n(ch9.get(k,0))}</b></td></tr>' for k, lab in CH)
t3 = "".join(f'<tr><td>{t}</td><td class="num">{n(eq.get(t,0))}</td><td class="num"><b>{n(eq9.get(t,0))}</b></td></tr>' for t in ["Product Growth", "Others", "Marketing", "Sales", "Collections"])
html = (f'<div style="display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr);gap:2cqi">'
        f'<div><div class="big">{n(N)} <span style="color:#6B7484;font-weight:400">contra</span> <span style="color:#1F4FD8">{n(nsep)}</span></div>'
        f'<div class="bigl">comunicaciones guardadas en Braze contra las que mandaron algo en septiembre</div>'
        f'<table style="margin-top:1cqi"><tr><th>Del catálogo a lo que sí manda</th><th class="num">Comunicaciones</th><th></th></tr>{t1}</table></div>'
        f'<div><table><tr><th>Por canal</th><th class="num">En el año</th><th class="num">En sep.</th></tr>{t2}</table>'
        f'<table style="margin-top:1cqi"><tr><th>Por equipo</th><th class="num">En el año</th><th class="num">En sep.</th></tr>{t3}</table>'
        f'<div style="margin-top:.6cqi;color:#6B7484;font-size:.85cqi">Un Canvas puede mandar por varios canales: la suma por canal es mayor que el total.</div></div></div>')
J = dict(
    kind="html",
    titulo=f"Braze tiene {n(N)} comunicaciones guardadas, pero en septiembre solo {n(nsep)} mandaron algo",
    que=f"Comunicación = cada campaña suelta o Canvas guardado en Braze ({n(tp['canvas'])} Canvas y {n(tp['campaign'])} campañas). Un Canvas puede mandar por varios canales.",
    quien=f"Con envío en el año: Marketing {n(eq['Marketing'])}, Product Growth {n(eq['Product Growth'])}, Sales {n(eq['Sales'])}, Others {n(eq['Others'])}, Collections {n(eq['Collections'])}. En septiembre: Product Growth {n(eq9['Product Growth'])}, Others {n(eq9['Others'])}, Marketing {n(eq9['Marketing'])}.",
    a_quien="No aplica: es el inventario de lo que está guardado y de lo que sí mandó mensajes.",
    lecturas=[
        f"Entre enero y septiembre se estrenaron {n(cre)} comunicaciones, unas {cre/9:.0f} al mes; de las {n(nper)} que mandaron mensajes en el año, {100*cre_per/nper:.0f} % son nuevas de 2026.",
        f"El estado 'archivada' no dice qué sigue vivo: {arch9} comunicaciones marcadas como archivadas mandaron en septiembre. Las {c2.na.sum()} sin archivar mandaron algo en los últimos 90 días.",
        f"{pr} tienen nombre de prueba o copia; {prp} de ellas mandaron mensajes reales en 2026 (lámina 80).",
    ],
    causa="Cada mes se crea una copia nueva en vez de editar la anterior, nadie depura el catálogo y el nombre no sigue una regla, así que el estado de Braze no dice qué está vivo.",
    sowhat="El catálogo está lleno de copias viejas: limpiarlo, archivar lo que no manda y nombrar con una regla es un trabajo de una sola vez.",
    fuente=f"Fuente: Braze, catálogo de comunicaciones al 7 de octubre 2026 y envíos por comunicación, mes y canal, enero a septiembre 2026. 'Mandaron algo' = al menos un mensaje enviado en el periodo; el guion contaba {n(e.communication_id.nunique())} porque incluía comunicaciones que solo registraron bajas o lecturas de envíos anteriores.",
    html=html)
write(75, J)
