"""Lámina 70: campañas de email con 300 mil o más correos entregados: correos (x, escala logarítmica) contra bajas por cada mil (y),
tamaño = bajas; las ocho con más bajas en color según clics. Fuente: E1 (email_unsubscribe = eventos de baja atribuidos a la campaña)."""
import math
from b7 import *

e = load_e1()
x = e[e.canal == "email"].groupby("fam").agg(deliv=("email_delivery", "sum"), clk=("email_click", "sum"), uns=("email_unsubscribe", "sum"), equipo=("equipo", "first"))
T = x.uns.sum(); x["bpm"] = 1000 * x.uns / x.deliv; x["cpm"] = 1000 * x.clk / x.deliv; x["pct"] = 100 * x.uns / T
big = x[x.deliv >= 300000].copy(); MED = big.bpm.median()
t8 = big.sort_values("uns", ascending=False).head(8)
print("eventos", T, "n", len(big), "mediana", MED, "top8", t8.uns.sum(), t8.pct.sum(), "bajo 10 clics por mil", (t8.cpm < 10).sum())
print(t8.groupby("equipo").uns.sum())
NOM = {"BillPay_Intro": ("Lanzamiento de BillPay", "a toda la base"), "B0211": ("Tasa 0", "a registrados de KPay sin crédito"),
       "B0326": ("Referidos", "a leads"), "NarrativaTasa0": ("Tasa 0 contada como historia", "a leads rezagados"),
       "Retargeting_Veriff": ("Recordatorio de verificar identidad", "a quien dejó el registro"), "AnotayGana": ("Sorteo AnotayGana", "a toda la base"),
       "CuestaEnero": ("Cuesta de Enero", "a leads"), "B0223": ("Crédito en plazos", "a quien nunca lo activó")}
def nom(f): return [v for k, v in NOM.items() if k in f][0]
POS = {"NarrativaTasa0": (430, 80, "end"), "B0326": (430, 125, "end"), "AnotayGana": (430, 170, "end"), "CuestaEnero": (430, 215, "end"),
       "Retargeting_Veriff": (430, 312, "end"), "B0223": (430, 346, "end"), "BillPay_Intro": (770, 140, "end"), "B0211": (770, 336, "end")}
S = SVG("Campañas de email: correos entregados contra bajas por cada mil correos; las ocho con más bajas, en color según cuántos clics reciben")
S.legend([("Menos de 10 clics por cada mil correos", BLUE, "ci"), ("10 clics por mil o más", GREEN, "ci"), (f"Otras {len(big)-8} campañas de 300 mil correos o más", MARK2, "ci")], 0, 14, 18)
X0, X1, Y0, Y1 = 52, 760, 52, 360
LX0, LX1 = math.log10(0.3e6), math.log10(40e6)
xs = lambda v: X0 + (X1 - X0) * (math.log10(v) - LX0) / (LX1 - LX0)
YM = 12
ys = lambda v: Y1 - (Y1 - Y0) * min(v, YM) / YM
for v in (0, 3, 6, 9, 12):
    S.line(X0, ys(v), X1, ys(v), GRID); S.t(X0 - 8, ys(v) + 4, f"{v}", 11, SEC, "end")
for v, l in ((0.3e6, "0.3 M"), (1e6, "1 M"), (3e6, "3 M"), (10e6, "10 M"), (30e6, "30 M")):
    S.line(xs(v), Y1, xs(v), Y1 + 4, MARK); S.t(xs(v), Y1 + 17, l, 11, SEC, "middle")
S.t(X1, Y1 + 32, "Correos entregados en el año (escala que multiplica)", 11, SEC, "end")
S.t(X0 - 44, Y0 - 14, "Bajas por cada mil correos", 11, SEC)
S.line(X0, ys(MED), X1, ys(MED), INK, 1, ' stroke-dasharray="4 4" opacity="0.6"')
S.t(X0 + 4, ys(MED) + 14, f"Mediana de las campañas, con todas sus bajas: {MED:.1f} por mil", 11, INK, "start", halo=True)
rr = lambda u: 3 + 15 * (u / 80000) ** 0.5
for f, r in big.drop(t8.index).iterrows():
    S.circle(xs(r.deliv), ys(r.bpm), 3, MARK2, sw=0)
for f, r in t8.iterrows():
    k = [k for k in POS if k in f][0]; lx, ly, an = POS[k]
    S.line(lx + (4 if an == "end" else 0), ly - 4 if an == "end" else ly + 18, xs(r.deliv), ys(r.bpm), MARK, 1)
for f, r in t8.iterrows():
    col = BLUE if r.cpm < 10 else GREEN
    S.circle(xs(r.deliv), ys(r.bpm), rr(r.uns), col, "#FFFFFF", 1.5, ' fill-opacity="0.85"')
for f, r in t8.iterrows():
    k = [k for k in POS if k in f][0]; xx, yy, an = POS[k]; n1, n2 = nom(f)
    S.t(xx, yy, f"{n1} · {r.equipo}", 11, INK, an, 600, halo=True)
    S.t(xx, yy + 13, f"{n2} · {r.uns/1e3:.0f} mil bajas · {r.cpm:.0f} {'clic' if round(r.cpm)==1 else 'clics'} por mil", 10.5, TXT, an, halo=True)
S.t(0, 408, f"Tamaño del círculo = bajas en el año. Más de {YM} bajas por mil se dibuja en {YM}.", 10.5, SEC)
pg = t8[t8.equipo == "Product Growth"]; mk = t8[t8.equipo == "Marketing"]
bp6 = e[e.fam.str.contains("BillPay_Intro") & (e.canal == "email") & (e.m == 6)].email_unsubscribe.sum()
J = dict(
    titulo="Ocho campañas de email causan un tercio de las bajas del correo, y seis casi no reciben clics",
    que="BillPay, Tasa 0, referidos, AnotayGana, Cuesta de Enero, crédito en plazos y Veriff.",
    quien=f"Product Growth {len(pg)} campañas, Marketing {len(mk)} y Others 1 (BillPay).",
    a_quien="Toda la base, leads y registrados que nunca tomaron crédito.",
    lecturas=[
        f"Las ocho suman {t8.uns.sum()/1e3:.0f} mil de {T/1e6:.2f} M bajas ({t8.pct.sum():.0f} %); seis reciben menos de 10 clics por mil.",
        f"Tasa 0 contada como historia a rezagados: {t8.loc[[i for i in t8.index if 'NarrativaTasa0' in i][0],'bpm']:.0f} bajas por mil correos; la mediana, {MED:.1f}.",
        f"El lanzamiento de BillPay salió una vez y sumó {t8.loc[[i for i in t8.index if 'BillPay' in i][0],'uns']/1e3:.0f} mil bajas registradas ({bp6/1e3:.0f} mil en junio).",
    ],
    causa="Se manda la misma promoción a listas enteras sin ver si abren; a quien no le interesa, se da de baja.",
    sowhat="Quien se da de baja ya no recibe correos: achicar estos ocho envíos protege el contacto.",
    fuente=f"Fuente: Braze, envíos por campaña y canal, ene a sep 2026; {len(big)} campañas de email con 300 mil correos o más. Bajas = eventos atribuidos a la campaña, no personas.",
    svg=S.out())
write(70, J)
