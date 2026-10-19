"""Lámina 83: cuántas veces convierte más quien abre contra quien no abre, a 7 días (x) y a 90 días (y), por campaña y canal.
Azul: Sales; gris: otros equipos. Diagonal = misma ventaja a 7 y 90 días. Fuente: E9a (campañas con mil o más de cada lado y 100 conversiones)."""
from b7 import *

w = pd.read_csv(D + "e9a_abren_vs_no_abren_ventanas.csv")
w["equipo"] = w.familia.fillna("").map(lambda n: team_of(n.split("-")[0]))
no = w.envios_usuario_dia - w.abrieron
for d in ["7", "90"]: w["l" + d] = (w["ab_conv_" + d] / w.abrieron) / (w["no_conv_" + d] / no)
w = w[(w.abrieron >= 1000) & (no >= 1000) & (w.ab_conv_7 >= 100)].copy()
sa = w[w.equipo == "Sales"]
med = w.groupby("equipo").agg(m7=("l7", "median"), m90=("l90", "median"))
e = load_e1(); se = e[e.equipo == "Sales"]; se_et = se.groupby(se.fam.map(etapa)).envios.sum()
print(len(sa), (sa.l90 >= 2).sum(), med)
S = SVG("Ventaja de conversión de quien abre contra quien no abre, a 7 y a 90 días, por campaña; en azul las de Sales, por canal")
S.legend([("Campaña de Sales", BLUE, "ci"), ("Campaña de otro equipo", MARK2, "ci"), ("Misma ventaja a 7 y 90 días", INK, "ln")], 0, 14, 16)
PAN = [("push notification", "Push"), ("whatsapp", "WhatsApp"), ("email", "Email")]
CW = 262; Y0, HH = 70, 270; VM = 5
LBL = {"push notification": [("B0615", "Comercio del día"), ("B0623", "Privalia aniversario")], "whatsapp": [("B0599", "Venta Azul Aeroméxico")], "email": [("B0335", "Promociones de comercios")]}
for j, (ch, nm) in enumerate(PAN):
    x0 = 40 + CW * j; ww = CW - 60
    X = lambda v, x0=x0, ww=ww: x0 + ww * (min(v, VM) - 1) / (VM - 1)
    Y = lambda v: Y0 + HH - HH * (min(max(v, 1), VM) - 1) / (VM - 1)
    d = w[w.canal == ch]; ds = d[d.equipo == "Sales"]
    S.t(x0 - 28, Y0 - 24, nm, 12, INK, w=700)
    S.t(x0 - 28, Y0 - 10, f"Sales: {len(ds)} campañas; mediana {ds.l7.median():.1f} a 7 días y {ds.l90.median():.1f} a 90", 10.5, BLUE, w=600)
    for v in (1, 2, 3, 4, 5):
        S.line(x0, Y(v), x0 + ww, Y(v), GRID); S.line(X(v), Y0, X(v), Y0 + HH, GRID)
        S.t(X(v), Y0 + HH + 14, f"{v}", 10.5, SEC, "middle")
        if j == 0: S.t(x0 - 6, Y(v) + 4, f"{v}", 10.5, SEC, "end")
    S.line(X(1), Y(1), X(VM), Y(VM), INK, 1, ' opacity="0.6"')
    S.line(x0, Y(2), x0 + ww, Y(2), BLUE, 1, ' stroke-dasharray="4 3"')
    for _, q in d[d.equipo != "Sales"].iterrows(): S.circle(X(q.l7), Y(q.l90), 2.2, MARK2, sw=0)
    for _, q in ds.iterrows(): S.circle(X(q.l7), Y(q.l90), 3.4, BLUE, "#FFFFFF", 0.8)
    for k, lab in LBL[ch]:
        q = ds[ds.familia.str.contains(k)].sort_values("envios_usuario_dia").iloc[-1]
        S.t(X(q.l7) - 5, Y(q.l90) - 7, lab, 10.5, INK, "end", 600, halo=True)
    if j == 0: S.t(x0 + ww, Y(2) - 4, "2 veces a 90 días", 10.5, BLUE, "end", 600, halo=True)
S.t(780, Y0 + HH + 30, "Veces que convierte más quien abre, a 7 días (abajo) y a 90 días (izquierda)", 10.5, SEC, "end")
S.t(0, 412, "Conversión: solicitud o préstamo, sobre todo de KCash; no confirma la compra en el comercio.", 10.5, SEC)
J = dict(
    titulo="Las promociones de comercios a clientes de KPay sí mueven a quien las abre, aunque a 90 días la ventaja se achica",
    que="Comercio del día, Hot Sale, Amazon, Cuponera, Privalia y Venta Azul Aeroméxico.",
    quien=f"Sales: {se.envios.sum()/1e6:.0f} M mensajes en el año, {100*se[se.canal=='push notification'].envios.sum()/se.envios.sum():.0f} % por push.",
    a_quien=f"Clientes recurrentes de KPay ({100*se_et.get('Clientes activos y recurrentes',0)/se.envios.sum():.0f} % de los mensajes) y leads.",
    lecturas=[
        f"En {len(sa)} campañas de Sales, quien abre convierte {med.loc['Sales','m7']:.1f} veces más a 7 días y {med.loc['Sales','m90']:.1f} a 90 (mediana).",
        f"Solo {(sa.l90>=2).sum()} mantienen dos veces o más a 90 días; varias son de agosto y septiembre, aún sin ventana completa.",
        f"Pasa en todos los equipos: Marketing baja de {med.loc['Marketing','m7']:.1f} a {med.loc['Marketing','m90']:.1f}; parte de esas compras iban a pasar igual.",
    ],
    causa="Quien abre ya era más activo; sin un grupo sin mensajes no se sabe cuánto vende la promoción.",
    sowhat="La promoción a quien ya compra parece funcionar; un grupo sin mensajes dirá cuánto vende.",
    fuente="Fuente: Braze y Databricks, conversión de quien abre y de quien no abre a 7 y 90 días, ene a sep 2026; campañas con mil o más de cada lado y 100 conversiones.",
    svg=S.out())
write(83, J)
