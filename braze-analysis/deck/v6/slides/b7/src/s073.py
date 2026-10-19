"""Lámina 73 (forma de la lámina 27 del v5): franja de cada paso de push de Canvas con 5 mil personas o más, por posición del paso,
aperturas por cada mil push (escala log); en azul los pasos del programa de recuperación de KPay (B0331, B0332, B0333). Barra = promedio ponderado.
Fuente: E15 (embudo por paso) y E1 (respuesta del programa por canal)."""
import math
from b7 import *

s = pd.read_csv(D + "e15_embudo_pasos.csv", low_memory=False)
s["nm"] = s.canvas_step_name.fillna("")
s["prog"] = s.nm.str.contains("B0331|B0332|B0333") & s.nm.str.contains("KPay")
s["ab"] = np.minimum(s.usuarios_abrieron, s.usuarios); s["pm"] = 1000 * s.ab / s.usuarios
pc = s.groupby("canvas_id").agg(p=("canvas_step_id", "nunique"), nm=("canvas_name", "first"), st=("canvas_step_name", "first"), team=("team", "first"))
L = pc[pc.p > 20].copy(); L["n"] = L.nm.where(L.nm.notna() & (L.nm != "null"), L.st)
L["prog"] = L.n.str.contains("B0331|B0332|B0333") & L.n.str.contains("KPay")
big = pc.sort_values("p", ascending=False).iloc[0]; kb = s[s.canvas_id == pc.sort_values("p", ascending=False).index[0]]
print("canvas mas largo", big.p, kb.canal.value_counts().to_dict())
p = s[(s.canal == "push notification") & (s.usuarios >= 5000)].copy()
p["band"] = pd.cut(p.orden_aprox, [0, 1, 2, 4, 1000], labels=["Paso 1", "Paso 2", "Pasos 3 y 4", "Paso 5 o más"])
MINP = 7.5
B = p.groupby("band", observed=True).apply(lambda d: pd.Series({"n": len(d), "w": 1000 * d.ab.sum() / d.usuarios.sum(), "bajo": (d.pm < MINP).sum(),
                                                                  "np": d.prog.sum(), "bp": (d.prog & (d.pm < MINP)).sum()}))
pp = p[p.prog]; po = p[~p.prog]
print(B); print("prog", len(pp), (pp.pm < MINP).sum(), 1000 * pp.ab.sum() / pp.usuarios.sum(), "otros", len(po), (po.pm < MINP).sum(), 1000 * po.ab.sum() / po.usuarios.sum())
e = load_e1(); f = e[e.fam.str.contains("B0331|B0332|B0333") & e.fam.str.contains("KPay")]
P = f.groupby("canal").agg(b=("base", "sum"), r=("resp", "sum"), env=("envios", "sum"), c=("costo", "sum")); P["pm"] = 1000 * P.r / P.b
print(P)

S = SVG("Aperturas por cada mil push de cada paso de Canvas, por posición del paso; en azul los pasos del programa de recuperación de KPay")
S.legend([(f"Paso de push del programa de recuperación de KPay ({len(pp)})", BLUE, "ci"), (f"Paso de push de otros Canvas ({len(po)})", MARK2, "ci"), ("Promedio de la fila", INK, "ln")], 0, 14, 16)
S.t(0, 32, "Cada punto es un paso de push con 5 mil personas o más; el tamaño es cuántas personas lo recibieron", 10.5, SEC)
X0, X1 = 150, 770
L0, L1 = math.log10(0.5), math.log10(400)
xs = lambda v: X0 + (X1 - X0) * (math.log10(max(v, 0.5)) - L0) / (L1 - L0)
TOP, RH = 70, 66
rows = list(B.index)
Yb = TOP + RH * len(rows)
for v in (1, 3, 10, 30, 100, 300):
    S.line(xs(v), TOP - 8, xs(v), Yb - 6, GRID)
    S.t(xs(v), Yb + 8, f"{v}", 10.5, SEC, "middle")
S.t(X1, Yb + 24, "Aperturas por cada mil push (escala que multiplica; sin aperturas, en el borde izquierdo)", 10.5, SEC, "end")
S.line(xs(MINP), TOP - 8, xs(MINP), Yb - 6, INK, 1.2, ' stroke-dasharray="4 4"')
S.t(xs(MINP) + 4, TOP - 10, "Mínimo aceptable: 7.5 por mil", 10.5, INK, "start", 600, halo=True)
umax = p.usuarios.max()
for i, b in enumerate(rows):
    yc = TOP + RH * i + RH / 2 - 6
    q = B.loc[b]
    S.t(0, yc - 2, b, 12, INK, w=700)
    S.t(0, yc + 13, f"{int(q.n)} pasos; {int(q.bajo)} bajo lo mínimo", 10.5, SEC)
    S.t(0, yc + 26, f"del programa: {int(q.bp)} de {int(q.np)}" if q.np else "ninguno del programa", 10.5, BLUE if q.np else SEC, w=600 if q.np else 400)
    d = p[p.band == b].sort_values("prog")
    for j, (_, r) in enumerate(d.iterrows()):
        jy = ((j * 7) % 9 - 4) * (RH / 2 - 10) / 4
        S.circle(xs(r.pm), yc + jy, max(2.2, 8 * (r.usuarios / umax) ** 0.5), BLUE if r.prog else MARK2, "#FFFFFF", 0.6, ' fill-opacity="0.8"')
    S.line(xs(q.w), yc - 16, xs(q.w), yc + 16, INK, 3)
    S.t(xs(q.w), yc - 20, f"{q.w:.0f}", 11, INK, "middle", 700, halo=True)
    if i < len(rows) - 1: S.line(0, TOP + RH * (i + 1) - 6, 780, TOP + RH * (i + 1) - 6, GRID)
S.t(0, 412, f"El Canvas más largo del programa tiene {int(big.p)} mensajes distintos: 40 push, 40 in-app, 30 correos y 10 WhatsApp, en cuatro semanas y cinco ofertas.", 10.5, TXT)
J = dict(
    titulo="Los Canvas para recuperar clientes de KPay tienen hasta 120 mensajes distintos, y casi la mitad de sus push no llega a lo mínimo de aperturas",
    que="Promoción para recuperar clientes de KPay: cuatro semanas de mensajes por cuatro canales, con cinco ofertas (sin oferta, cupón, descuento en tasa y combinaciones), cada una también solo para Amazon.",
    quien=f"Product Growth: {(L.team=='Lending').sum()} de los {len(L)} Canvas con más de 20 pasos (el otro es una copia de uno de ellos); {int(L.prog.sum())} son este programa.",
    a_quien="Ex clientes KPay con 3, 6 y 12 meses sin compra. Se les escribe para recuperarlos; muchos pueden no tener la app, y sin app no reciben push.",
    lecturas=[
        f"{int((pp.pm<MINP).sum())} de los {len(pp)} pasos de push del programa abren menos de 7.5 por cada mil; en otros Canvas, {int((po.pm<MINP).sum())} de {len(po)}. En promedio abren {1000*pp.ab.sum()/pp.usuarios.sum():.0f} por mil contra {1000*po.ab.sum()/po.usuarios.sum():.0f}.",
        f"Los 120 pasos no son 120 mensajes a la misma persona: son mensajes distintos por semana, canal y oferta; cada quien recibe su rama, unos 5 a 10 mensajes al mes.",
        f"En el programa completo el correo recibe {P.loc['email','pm']:.1f} clics por cada mil (lo mínimo es 3), el WhatsApp se lee {P.loc['whatsapp','pm']/10:.0f} % y el in-app {P.loc['in-app','pm']:.0f} clics por mil (mínimo 100). El push del programa pasa apenas en promedio ({P.loc['push notification','pm']:.1f} por mil).",
    ],
    causa="Cada oferta nueva se agrega como otra rama del mismo Canvas, por cuatro canales y cuatro semanas, sin quitar los pasos que nadie abre ni medir contra un grupo sin mensajes.",
    sowhat="Más pasos no recuperan más: el programa necesita dos o tres ofertas, el canal que la persona sí usa, quitar los pasos que no llegan a lo mínimo y un grupo sin mensajes.",
    fuente=f"Fuente: Braze, embudo por paso de Canvas (posición del paso aproximada) y envíos por campaña y canal de B0331, B0332 y B0333, enero a septiembre 2026; el programa mandó {f.envios.sum()/1e6:.1f} M mensajes y costó {f.costo.sum()/1e6:.1f} M MXN. Mínimo: 7.5 aperturas por mil push, 3 clics por mil correos, 6 de cada 10 WhatsApp leídos, 1 de cada 10 in-app con clic.",
    svg=S.out())
write(73, J)
