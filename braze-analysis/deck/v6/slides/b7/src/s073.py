"""Lámina 73: el Canvas más largo del programa de recuperación de KPay (B0332, 6 meses sin compra, 120 pasos): mensajes distintos por
semana y canal con personas y respuesta (E15); a la derecha, respuesta del programa completo por canal contra lo mínimo aceptable (E1)."""
from b7 import *

s = pd.read_csv(D + "e15_embudo_pasos.csv", low_memory=False)
pc = s.groupby("canvas_id").agg(p=("canvas_step_id", "nunique"), nm=("canvas_name", "first"), st=("canvas_step_name", "first"), team=("team", "first"))
L = pc[pc.p > 20].copy(); L["n"] = L.nm.where(L.nm.notna() & (L.nm != "null"), L.st)
L["prog"] = L.n.str.contains("B0331|B0332|B0333") & L.n.str.contains("KPay")
cid = L.sort_values("p", ascending=False).index[0]; NAME = L.loc[cid, "n"]
k = s[s.canvas_id == cid].copy()
k["wk"] = k.canvas_step_name.str.extract(r"Week(\d)")[0].astype(int)
k["ab"] = np.minimum(k.usuarios_abrieron, k.usuarios)
G = k.groupby(["wk", "canal"]).agg(n=("canvas_step_id", "nunique"), u=("usuarios", "sum"), ab=("ab", "sum")); G["p"] = 100 * G.ab / G.u
print(NAME, L.loc[cid, "p"], k.canal.value_counts().to_dict(), k.usuarios.max()); print(G.round(2))
e = load_e1(); f = e[e.fam.str.contains("B0331|B0332|B0333") & e.fam.str.contains("KPay")]
P = f.groupby("canal").agg(b=("base", "sum"), r=("resp", "sum"), env=("envios", "sum"), c=("costo", "sum")); P["p"] = 100 * P.r / P.b; P["x"] = P.p / pd.Series(MIN)
g = f.groupby(["fam", "m"]).agg(env=("envios", "sum"), usu=("usuarios_aprox", "max")); tpm = (g.env / g.usu)
print(P.round(3)); print("envios", f.envios.sum() / 1e6, "costo", f.costo.sum() / 1e6, "largos", len(L), "prog", L.prog.sum(), (L.team == "Lending").sum())

S = SVG("Mensajes distintos del Canvas de recuperación de KPay por semana y canal, con personas y respuesta, y respuesta del programa completo por canal contra lo mínimo aceptable")
CH = [("push notification", "Push", "abrió"), ("in-app", "In-app", "hizo clic"), ("email", "Email", "abrió"), ("whatsapp", "WhatsApp", "leyó")]
S.t(0, 14, "Un Canvas: oferta a ex clientes KPay con 6 meses sin compra (marzo a septiembre)", 12, INK, w=600)
S.t(0, 30, "Cada celda: cuántos mensajes distintos hay (una versión por oferta), a cuántas personas llegaron y cuántas respondieron", 10.5, SEC)
X0, CW, TOP, RHh = 70, 104, 64, 70
for j, (c, lab, verb) in enumerate(CH):
    S.t(X0 + CW * j + CW / 2, TOP - 8, lab, 12, INK, "middle", 700)
for i in range(1, 5):
    y = TOP + RHh * (i - 1)
    S.t(0, y + 38, f"Semana {i}", 11.5, INK, w=600)
    for j, (c, lab, verb) in enumerate(CH):
        x = X0 + CW * j
        if (i, c) in G.index:
            q = G.loc[(i, c)]
            low = False
            S.rect(x + 2, y + 2, CW - 4, RHh - 4, "#E8EDFB" if low else "#F1F3F6")
            S.t(x + CW / 2, y + 26, f"{int(q.n)} mensajes", 12.5, INK, "middle", 700)
            S.t(x + CW / 2, y + 43, f"{q.u/1e3:.0f} mil personas", 10.5, TXT, "middle")
            S.t(x + CW / 2, y + 58, f"{q.p:.1f} % {verb}", 11, BLUE if low else TXT, "middle", 700 if low else 400)
        else:
            S.t(x + CW / 2, y + 38, "sin mensaje", 10.5, MARK, "middle")
nT = int(G.n.sum())
S.t(X0, TOP + RHh * 4 + 18, f"{nT} mensajes distintos: {', '.join(f'{int(G.xs(c, level=1).n.sum())} {lab.lower() if lab!="WhatsApp" else lab}' for c, lab, _ in CH)}.", 11, INK, w=600)
S.t(X0, TOP + RHh * 4 + 34, "Cada persona recibe solo la rama de su oferta: unos 5 a 10 mensajes al mes.", 10.5, SEC)
# panel derecho: programa completo
PX0, PX1, VM = 560, 740, 1.5
xs = lambda v: PX0 + (PX1 - PX0) * v / VM
S.line(510, 44, 510, 380, GRID)
S.t(530, 64, "Programa completo de recuperación", 12, INK, w=700)
S.t(530, 80, "Respuesta en veces lo mínimo aceptable", 10.5, SEC)
S.line(xs(1), 96, xs(1), 340, INK, 1, ' stroke-dasharray="4 4" opacity="0.6"')
S.t(xs(1), 352, "Lo mínimo", 10.5, INK, "middle")
UN = {"push notification": ("aperturas por mil", 10), "in-app": ("clics por mil", 10), "email": ("clics por mil", 10), "whatsapp": ("leídos por mil", 10)}
for j, (c, lab, _) in enumerate(CH):
    y = 104 + 58 * j; q = P.loc[c]; ok = q.x >= 1
    S.t(530, y + 10, lab, 11.5, INK, w=600)
    S.rect(PX0, y + 18, xs(q.x) - PX0, 14, GREEN if ok else BLUE)
    S.t(xs(q.x) + 5, y + 29, f"{q.x:.2f}", 11, INK, w=700)
    S.t(530, y + 46, f"{10*q.p:.1f} {UN[c][0]} (mínimo {10*MIN[c]:g})" if q.p < 10 else f"{10*q.p:.0f} {UN[c][0]} (mínimo {10*MIN[c]:g})", 10.5, SEC, halo=True)
S.t(530, 372, f"{P.env.sum()/1e6:.1f} M mensajes y {P.c.sum()/1e6:.1f} M MXN en el año", 11, INK, w=600)
S.t(0, 410, "Ex clientes KPay pueden no tener la app, y sin app no reciben push ni in-app. Email y push en la cuadrícula: personas que abrieron.", 10.5, SEC)
J = dict(
    titulo="Los Canvas para recuperar clientes de KPay tienen hasta 120 mensajes distintos, y tres de sus cuatro canales responden menos de lo mínimo",
    que="Promoción para recuperar clientes de KPay: cuatro semanas de mensajes por cuatro canales, con cinco ofertas (sin oferta, cupón, descuento en tasa, y combinaciones), cada una también solo para Amazon.",
    quien=f"Product Growth: {(L.team=='Lending').sum()} de los {len(L)} Canvas con más de 20 pasos (el otro es una copia de uno de ellos); {int(L.prog.sum())} son este programa.",
    a_quien="Ex clientes KPay con 3, 6 y 12 meses sin compra. Se les escribe para recuperarlos; muchos pueden no tener la app.",
    lecturas=[
        "Los 120 pasos no son 120 mensajes a la misma persona: son 120 mensajes distintos (semana por canal por oferta). Cada quien recibe la rama de su oferta.",
        f"En el programa completo el email recibe {10*P.loc['email','p']:.1f} clics por cada mil correos (lo mínimo es 3), el WhatsApp se lee {P.loc['whatsapp','p']:.0f} % y el in-app {10*P.loc['in-app','p']:.0f} clics por mil. Solo el push pasa, con {10*P.loc['push notification','p']:.1f} aperturas por mil.",
        f"Los otros Canvas largos son ofertas sin intereses a clientes activos de KPay, meses sin intereses a activos, Tasa 0, Lázaro, Cuesta de Enero y AnotayGana; todos de Product Growth.",
    ],
    causa="Cada oferta nueva se agrega como otra rama del mismo Canvas, por los cuatro canales y cuatro semanas, sin quitar las que no responden ni medir contra un grupo sin mensajes.",
    sowhat="Más ramas no recuperan más: el programa necesita dos o tres ofertas, el canal que la persona sí usa y un grupo sin mensajes que diga cuánto recupera.",
    fuente=f"Fuente: Braze, embudo por paso de Canvas ({NAME}, 120 pasos) y envíos por campaña y canal de B0331, B0332 y B0333, enero a septiembre 2026. Mínimo: 3 clics por mil correos, 7.5 aperturas por mil push, 6 de cada 10 WhatsApp leídos, 1 de cada 10 in-app con clic. WhatsApp a 1.00 MXN por entregado.",
    svg=S.out())
write(73, J)
