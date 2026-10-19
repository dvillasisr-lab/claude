"""Lámina 66: dispersión de campañas por canal con 100 mil mensajes o más: mensajes en el año (x, log) contra respuesta en veces
lo mínimo de su canal (y, log). Azul: no responde lo mínimo y manda mucho (señal de muestra_c), oscuro si sigue enviando en septiembre.
Fuente: hallazgos/muestra_c_familias.csv con WhatsApp por entregado; E1 para septiembre."""
import math
from b7 import *

c = load_c(); e = load_e1()
TOT = c.envios.sum()
no = c[c.senal == "apagar o rehacer"]
p = no[no.tipo == "promocional o lifecycle"]
s9 = e[e.m == 9].groupby(["fam", "canal"]).agg(env9=("envios", "sum"), c9=("costo", "sum")).reset_index()
pa = p[p.activo_sep == 1].merge(s9, left_on=["familia", "canal"], right_on=["fam", "canal"], how="left")
tg = p.groupby("tema").envios.sum()
x = c[c.envios >= 100000].copy(); x["vx"] = (x.respuesta_pct / x.canal.map(MIN)).clip(lower=0.02)
x["no"] = x.senal == "apagar o rehacer"
print(no.envios.sum() / 1e6, no.costo_ent.sum() / 1e6, len(pa), pa.env9.sum() / 1e6, pa.c9.sum() / 1e6, tg.sort_values(ascending=False).head(4) / 1e6)
eq = p.groupby("equipo").agg(env=("envios", "sum"), c=("costo_ent", "sum")); eq["pc"] = 100 * eq.c / eq.c.sum()
S = SVG("Campañas por canal: mensajes en el año contra respuesta en veces lo mínimo; en azul las que no responden lo mínimo y mandan mucho")
S.legend([("No responde lo mínimo y sigue en septiembre", BLUE, "ci"), ("No responde y ya se detuvo", BLUEL, "ci"), ("Resto de campañas", MARK2, "ci")], 0, 14, 16)
X0, X1, Y0, Y1 = 44, 770, 40, 372
L0, L1 = math.log10(1e5), math.log10(5e7)
YL0, YL1 = math.log10(0.03), math.log10(30)
xs = lambda v: X0 + (X1 - X0) * (math.log10(v) - L0) / (L1 - L0)
ys = lambda v: Y1 - (Y1 - Y0) * (math.log10(min(max(v, 0.03), 30)) - YL0) / (YL1 - YL0)
for v, l in ((0.03, "0.03"), (0.1, "0.1"), (0.3, "0.3"), (1, "1"), (3, "3"), (10, "10"), (30, "30")):
    S.line(X0, ys(v), X1, ys(v), GRID); S.t(X0 - 6, ys(v) + 4, l, 10.5, SEC, "end")
for v, l in ((1e5, "100 mil"), (1e6, "1 M"), (1e7, "10 M"), (5e7, "50 M")):
    S.t(xs(v), Y1 + 14, l, 10.5, SEC, "middle" if v not in (1e5, 5e7) else ("start" if v == 1e5 else "end"))
S.t(X1, Y1 + 30, "Mensajes de la campaña en el año (escala que multiplica)", 10.5, SEC, "end")
S.t(X0 + 4, Y0 - 6, "Veces lo mínimo de su canal", 10.5, SEC)
S.rect(X0, ys(1), X1 - X0, Y1 - ys(1), "#F3F6FD")
S.line(X0, ys(1), X1, ys(1), INK, 1.2, ' stroke-dasharray="4 4"')
S.t(X0 + 4, ys(1) + 14, "Lo mínimo aceptable", 10.5, INK, "start", 600, halo=True)
for _, q in x[~x.no].iterrows(): S.circle(xs(q.envios), ys(q.vx), 2.6, MARK2, sw=0)
for _, q in x[x.no].sort_values("activo_sep").iterrows(): S.circle(xs(q.envios), ys(q.vx), 3.4, BLUE if q.activo_sep == 1 else BLUEL, "#FFFFFF", 0.8)
LAB = [("B0211-CANVAS-Nuevos_RegistradosPay", "email", "Tasa 0 a registrados sin crédito · Product Growth", 762, 124),
       ("B0326-Canvas-Leads-ReferralProgram", "email", "Referidos a leads · Marketing", 520, 150),
       ("Anonimos-RescateTasa0", "push notification", "Rescate Tasa 0 a anónimos · Marketing", 520, 176),
       ("BillPay_Intro", "email", "Lanzamiento de BillPay · Others", 762, 300),
       ("B0223-CANVAS-Nuevos_NeverActive", "email", "Crédito en plazos a quien nunca lo activó · Product Growth", 600, 330)]
for k, ch, lab, lx, ly in LAB:
    q = x[x.familia.str.contains(k, regex=False) & (x.canal == ch)].sort_values("envios").iloc[-1]
    px, py = xs(q.envios), ys(q.vx)
    S.line(px, py, lx + 3, ly - 4, MARK, 1)
for k, ch, lab, lx, ly in LAB:
    S.t(lx, ly, lab, 10.5, INK, "end", 600, halo=True)
S.t(X1 - 4, Y0 + 14, "Arriba de la línea: responde lo mínimo o más", 10.5, SEC, "end", halo=True)
S.t(X1 - 4, Y1 - 8, f"Azul: {no.envios.sum()/1e6:.0f} M mensajes ({100*no.envios.sum()/TOT:.0f} % del año) y {no.costo_ent.sum()/1e6:.1f} M MXN", 11, BLUE, "end", 700, halo=True)
J = dict(
    titulo="Cuatro de cada diez mensajes salieron de campañas que no responden lo mínimo: comercios, Tasa 0 y referidos",
    que="Promociones: Tasa 0, comercios KPay, referidos, BillPay y ofertas para volver.",
    quien=f"Marketing y Product Growth ({eq.loc['Product Growth','pc']:.0f} % del gasto); Others y Sales, menos.",
    a_quien="Leads, registrados sin crédito, ex clientes inactivos y toda la base.",
    lecturas=[
        f"Debajo de lo mínimo: comercios KPay {tg['Promociones de comercios KPay']/1e6:.0f} M mensajes, Tasa 0 {tg['Tasa 0']/1e6:.0f} M y referidos {tg['Referidos']/1e6:.0f} M.",
        f"{len(pa)} de estas campañas seguían en septiembre: {pa.env9.sum()/1e6:.0f} M mensajes y {pa.c9.sum()/1e6:.1f} M MXN ese mes.",
        f"Product Growth pone {eq.loc['Product Growth','pc']:.0f} % del gasto, por el WhatsApp a ex clientes y registrados.",
    ],
    causa="Las promociones salen a listas grandes y nadie revisa si responden; se detienen cuando acaba la promoción.",
    sowhat="El desperdicio está en pocas campañas grandes a quien aún no es cliente o ya se fue.",
    fuente="Fuente: Braze, envíos por campaña, ene a sep 2026; campañas de 100 mil mensajes o más; WhatsApp leído con el mes siguiente. Mínimo: 3 clics por mil correos, 7.5 aperturas por mil push, 60 % WhatsApp leído, 10 % in-app.",
    svg=S.out())
write(66, J)
