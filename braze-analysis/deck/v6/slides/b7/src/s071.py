"""Lámina 71: campañas de email con 100 mil o más correos: clics por mil (x) contra bajas por mil (y), tamaño = correos;
resaltadas las 33 que responden más que la mediana pero tienen 2.5 bajas por mil o más; color = correos por persona al mes.
Fuente: hallazgos/muestra_c_familias.csv (bajas por mil contadas en los meses con envío, toques por persona al mes)."""
from b7 import *

c = load_c(); m = c[c.canal == "email"].copy()
m["uns"] = m.bajas_por_mil * m.envios * m.entrega_pct / 100 / 1000
x = m[m.envios >= 100000].copy()
r = m[(m.senal == "revisar") & (m.motivo == "bajas altas")].copy()
MEDC = m.mediana_canal_resp.iloc[0]; MEDB = x.bajas_por_mil.median()
hi = r.toques_usuario_mes >= 2
print(len(x), len(r), r.envios.sum() / 1e6, r.uns.sum(), MEDC, MEDB, hi.sum(), r[hi].uns.sum() / r.uns.sum())
eqr = r.groupby("equipo").agg(n=("familia", "size"), env=("envios", "sum"), uns=("uns", "sum")); eqr["pu"] = 100 * eqr.uns / eqr.uns.sum(); print(eqr)
S = SVG("Campañas de email: clics por cada mil correos contra bajas por cada mil correos; resaltadas las que responden bien pero causan muchas bajas, según cuántos correos recibe cada persona al mes")
S.legend([("2 o más correos por persona al mes", BLUE, "ci"), ("Menos de 2 al mes", BLUEL, "ci"), (f"Resto de campañas de 100 mil correos o más", MARK2, "ci")], 0, 14, 18)
X0, X1, Y0, Y1 = 52, 760, 50, 352
XM, YM = 50, 10
xs = lambda v: X0 + (X1 - X0) * min(v, XM) / XM
ys = lambda v: Y1 - (Y1 - Y0) * min(v, YM) / YM
S.rect(xs(10 * MEDC), Y0, X1 - xs(10 * MEDC), ys(2.5) - Y0, "#EEF2FB")
S.t(X1 - 6, Y0 + 16, "Responde más que la mitad de los correos y causa 2.5 bajas por mil o más", 11, BLUE, "end", 600)
for v in (0, 2.5, 5, 7.5, 10):
    S.line(X0, ys(v), X1, ys(v), GRID); S.t(X0 - 8, ys(v) + 4, f"{v:g}", 11, SEC, "end")
for v in (0, 10, 20, 30, 40, 50):
    S.t(xs(v), Y1 + 16, f"{v}", 11, SEC, "middle")
S.t(X1, Y1 + 32, "Clics por cada mil correos", 11, SEC, "end")
S.t(X0 - 44, Y0 - 12, "Bajas por cada mil correos", 11, SEC)
S.line(X0, ys(MEDB), X1, ys(MEDB), INK, 1, ' stroke-dasharray="4 4" opacity="0.6"')
S.t(X0 + 6, ys(MEDB) + 14, f"Campaña típica: {MEDB:.1f} bajas por mil", 11, INK, "start", halo=True)
rr = lambda v: 2.5 + 11 * (v / 10e6) ** 0.5
for _, q in x[~x.familia.isin(r.familia)].iterrows():
    S.circle(xs(10 * q.clic_pct), ys(q.bajas_por_mil), 2.6, MARK2, sw=0)
for _, q in r.sort_values("envios", ascending=False).iterrows():
    S.circle(xs(10 * q.clic_pct), ys(q.bajas_por_mil), rr(q.envios), BLUE if q.toques_usuario_mes >= 2 else BLUEL, "#FFFFFF", 1.2)
LAB = {"Retargeting_Veriff": ("Verificar identidad (Veriff)", 500, 100, "start"), "Retargeting_PersonalInfo": ("Datos personales", 452, 150, "end"),
       "Retargeting_NIP": ("NIP", 770, 150, "end"), "Leads_BBDDRezagada-NarrativaTasa0": ("Tasa 0 contada como historia a rezagados", 60, 84, "start"),
       "Retargeting_Installments_SP": ("Meses sin intereses a activos", 610, 326, "start")}
pts = []
for _, q in r.iterrows():
    for k, (lab, lx, ly, an) in LAB.items():
        if k in q.familia and q.envios > 500000:
            pts.append((q, lab, lx, ly, an))
for q, lab, lx, ly, an in pts:
    S.line(lx, ly + 17, xs(10 * q.clic_pct), ys(q.bajas_por_mil), MARK, 1)
for q, lab, lx, ly, an in pts:
    S.t(lx, ly, lab, 11, INK, an, 600, halo=True)
    S.t(lx, ly + 13, f"{q.toques_usuario_mes:.1f} correos al mes · {q.equipo}", 10.5, TXT, an, halo=True)
S.t(0, 410, f"Tamaño = correos entregados. Bajas contadas en los meses en que la campaña envió. Más de {XM} clics o {YM} bajas por mil se dibuja en el borde.", 10.5, SEC)
V = r[r.familia.str.contains("Retargeting_Veriff")].iloc[0]
rec = r[r.tema == "Recordatorio de registro"]
J = dict(
    titulo="Hay correos que la gente sí toca pero causan muchas bajas: la mitad viene de recordatorios repetidos",
    que="Recordatorios de registro, Tasa 0 contada como historia, boletines y avisos.",
    quien=f"Marketing {eqr.loc['Marketing','n']:.0f} de {len(r)} campañas, Others {eqr.loc['Others','n']:.0f} y Product Growth {eqr.loc['Product Growth','n']:.0f}.",
    a_quien="Sobre todo leads que acaban de empezar su registro.",
    lecturas=[
        f"{len(r)} campañas reciben {10*(r.clic_pct*r.envios).sum()/r.envios.sum():.0f} clics por mil correos y causan 2.5 bajas por mil o más; la típica, {MEDB:.1f}.",
        f"Las {hi.sum()} que llegan dos o más veces al mes a la misma persona causan {100*r[hi].uns.sum()/r.uns.sum():.0f} % de esas bajas.",
        f"Veriff: {V.toques_usuario_mes:.1f} correos al mes por persona, {10*V.clic_pct:.0f} clics y {V.bajas_por_mil:.1f} bajas por mil.",
    ],
    causa="Cada paso pendiente manda su correo y no hay límite de mensajes por persona a la semana.",
    sowhat="El mensaje sirve; lo que molesta es la repetición: dos correos al mes y no a quien no abre.",
    fuente=f"Fuente: Braze, envíos por campaña y canal, ene a sep 2026; {len(x)} campañas de email con 100 mil correos o más. Bajas en los meses en que la campaña envió.",
    svg=S.out())
write(71, J)
