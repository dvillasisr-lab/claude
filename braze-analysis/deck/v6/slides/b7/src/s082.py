"""Lámina 82: campañas promocionales por canal: mensajes (x, log) contra respuesta en veces la típica de su canal (y, log).
Verde: chicas que responden el doble o más (señal 'escalar' de muestra_c: envíos debajo de la mediana del canal, al menos mil, respuesta al doble
de la mediana o más). Fuente: hallazgos/muestra_c_familias.csv."""
import math
from b7 import *

c = load_c()
p = c[(c.tipo == "promocional o lifecycle") & (c.envios >= 1000) & c.canal.isin(MIN.keys())].copy()
p["vt"] = p.respuesta_pct / p.mediana_canal_resp
s = p[p.senal == "escalar"]
eq = s.groupby("equipo").size(); et = s.groupby("etapa").size()
print(len(s), s.envios.sum() / 1e6, s.activo_sep.sum(), eq.to_dict(), et.to_dict(), c.envios.sum())
S = SVG("Campañas promocionales: mensajes contra respuesta en veces la típica de su canal; en verde las chicas que responden el doble o más")
S.legend([("Chica y responde el doble o más, sigue en septiembre", GREEN, "ci"), ("Igual, ya se detuvo", GREENL, "ci"), ("Resto de campañas", MARK2, "ci")], 0, 14, 16)
X0, X1, Y0, Y1 = 44, 770, 44, 366
L0, L1 = math.log10(1e3), math.log10(5e7); YL0, YL1 = math.log10(0.02), math.log10(30)
xs = lambda v: X0 + (X1 - X0) * (math.log10(v) - L0) / (L1 - L0)
ys = lambda v: Y1 - (Y1 - Y0) * (math.log10(min(max(v, 0.02), 30)) - YL0) / (YL1 - YL0)
for v, l in ((0.02, "0.02"), (0.1, "0.1"), (1, "1"), (2, "2"), (10, "10")):
    S.line(X0, ys(v), X1, ys(v), GRID); S.t(X0 - 6, ys(v) + 4, l, 10.5, SEC, "end")
for v, l in ((1e3, "mil"), (1e4, "10 mil"), (1e5, "100 mil"), (1e6, "1 M"), (1e7, "10 M")):
    S.t(xs(v), Y1 + 14, l, 10.5, SEC, "middle" if v > 1e3 else "start")
S.t(X1, Y1 + 30, "Mensajes de la campaña en el año (escala que multiplica)", 10.5, SEC, "end")
S.t(X0 + 4, Y0 - 6, "Respuesta en veces la campaña típica de su canal", 10.5, SEC)
S.line(X0, ys(1), X1, ys(1), INK, 1, ' stroke-dasharray="4 4" opacity="0.6"'); S.t(X1 - 4, ys(1) - 5, "la típica", 10.5, INK, "end", halo=True)
S.line(X0, ys(2), X1, ys(2), GREEN, 1.2); S.t(X1 - 4, ys(2) - 5, "el doble", 10.5, GREEN, "end", 600, halo=True)
for _, q in p[p.senal != "escalar"].iterrows(): S.circle(xs(q.envios), ys(q.vt), 2.3, MARK2, sw=0)
for _, q in s.sort_values("activo_sep").iterrows(): S.circle(xs(q.envios), ys(q.vt), 3.6, GREEN if q.activo_sep == 1 else GREENL, "#FFFFFF", 0.8)
LAB = [("RetargetingOffering-Canceló", "push notification", "Oferta a quien canceló · Marketing", 330, 64),
       ("Tardan45díasrecurrir-CampañasBAU", "email", "Regreso a los 45 días · Product Growth", 560, 88),
       ("T2853-CANVAS-Nuevos-Onboarding", "email", "Bienvenida KPay · Product Growth", 330, 104),
       ("CompraEnTemuyLeadKCash", "push notification", "Compró en Temu, oferta de KCash · Product Growth", 480, 126)]
for k, ch, lab, lx, ly in LAB:
    q = p[p.familia.str.contains(k, regex=False) & (p.canal == ch)].sort_values("envios").iloc[-1]
    S.line(xs(q.envios), ys(q.vt), lx + 3, ly + 3, MARK, 1)
for k, ch, lab, lx, ly in LAB: S.t(lx, ly, lab, 10.5, INK, "start", 600, halo=True)
S.t(X1 - 4, Y1 - 8, f"Verde: {len(s)} campañas, {s.envios.sum()/1e6:.1f} M mensajes ({100*s.envios.sum()/c.envios.sum():.1f} % del año)", 11, GREEN, "end", 700, halo=True)
qc = p[p.familia.str.contains("RetargetingOffering-Canceló") & (p.canal == "push notification")].iloc[0]
J = dict(
    titulo=f"Hay {len(s)} campañas chicas que responden el doble de lo normal y valdría la pena ampliar",
    que="Oferta a quien canceló, regreso a los 45 días, bienvenida, Temu y aniversario.",
    quien=f"Product Growth {eq.get('Product Growth',0)}, Marketing {eq.get('Marketing',0)}, Others {eq.get('Others',0)} y Sales {eq.get('Sales',0)}.",
    a_quien=f"Clientes activos ({et.get('Clientes activos y recurrentes',0)}) y leads que acaban de hacer algo ({et.get('Leads (no terminaron registro)',0)}).",
    lecturas=[
        f"Suman {s.envios.sum()/1e6:.1f} M mensajes, {100*s.envios.sum()/c.envios.sum():.1f} % del año; {int(s.activo_sep.sum())} siguen activas en septiembre.",
        f"Oferta a quien canceló: {10*qc.respuesta_pct:.0f} aperturas por cada mil push, {qc.vt:.0f} veces el push típico.",
        "Casi todas salen por algo que hizo la persona: cancelar, comprar, cumplir 45 días sin volver.",
    ],
    causa="Lo que funciona nació chico y nadie lo escala: no hay revisión que busque a los mejores.",
    sowhat="Ampliar no es mandar a toda la base: es usar el mismo motivo en más productos, con 10 % sin mensajes.",
    fuente="Fuente: Braze, envíos por campaña y canal, ene a sep 2026; promociones con mil mensajes o más. Chica: debajo de la mediana de mensajes de su canal. Típica: mediana de respuesta del canal.",
    svg=S.out())
write(82, J)
