"""Lámina 84 (forma de la lámina 7 del v5): índice semanal por canal, volumen y respuesta, promedio de enero = 100, pequeños múltiplos.
Fuente: E4a (serie semanal, semanas completas del 5 de enero al 21 de septiembre) y E1 (push por mes y equipo)."""
from b7 import *

d = pd.read_csv(D + "e4a_serie_semana_mes_canal.csv")
w = d[(d.grano == "semana") & (d.periodo >= "2026-01-05") & (d.periodo <= "2026-09-21")].copy()
CH = [("push notification", "Push", "pn_send", "pn_open", "pn_send", "apertura"), ("email", "Email", "email_sent", "email_click", "email_delivery", "clic"),
      ("whatsapp", "WhatsApp", "whatsapp_send", "whatsapp_read", "whatsapp_delivery", "lectura"), ("in-app", "In-app", "in_app_impression", "in_app_click", "in_app_impression", "clic")]
e = load_e1(); p = e[e.canal == "push notification"]
pm = p.groupby("m").agg(s=("pn_send", "sum"), o=("pn_open", "sum")); pm["r"] = 100 * pm.o / pm.s
pt = p.pivot_table(index="equipo", columns="m", values="pn_send", aggfunc="sum").fillna(0)
f = p.pivot_table(index="fam", columns="m", values="pn_send", aggfunc="sum").fillna(0)
cont = f[(f[6] > 100000) & (f[9] > 100000)].index
cc = p[p.fam.isin(cont) & p.m.isin([6, 9])].groupby("m").agg(s=("pn_send", "sum"), o=("pn_open", "sum")); cc["r"] = 100 * cc.o / cc.s
print(pm.round(2)); print((pt[[6, 9]] / 1e6).round(1)); print(len(cont), cc.r.round(2).to_dict())
S = SVG("Índice semanal de volumen y de respuesta por canal, promedio de enero igual a 100")
S.legend([("Volumen de la semana", BLUE, "ln"), ("Respuesta (apertura, clic o lectura)", MARK, "ln"), ("Junio", "#EEF2FB", "sq")], 0, 14, 18)
CW, CHh = 380, 180
YM = 300
for i, (c, nm, vcol, rcol, bcol, rn) in enumerate(CH):
    x0 = 40 + (i % 2) * CW; y0 = 50 + (i // 2) * CHh; ww, hh = CW - 122, 112
    g = w[w.canal == c].sort_values("periodo")
    vol = g[vcol].values; resp = g[rcol].values / np.maximum(g[bcol].values, 1)
    jan = g.periodo.str[5:7] == "01"
    vi = 100 * vol / vol[jan.values].mean(); ri = 100 * resp / resp[jan.values].mean()
    n = len(g); X = lambda k: x0 + ww * k / (n - 1)
    Y = lambda v: y0 + 16 + hh - hh * min(v, YM) / YM
    jun = [k for k, pp in enumerate(g.periodo) if pp[5:7] == "06"]
    S.rect(X(jun[0]) - 3, y0 + 16, X(jun[-1]) - X(jun[0]) + 6, hh, "#EEF2FB")
    S.t(x0, y0 + 6, nm, 12, BLUE if c == "push notification" else INK, w=700)
    for v in (0, 100, 200, 300):
        S.line(x0, Y(v), x0 + ww, Y(v), INK if v == 100 else GRID, 1, ' stroke-dasharray="3 3" opacity="0.5"' if v == 100 else "")
        S.t(x0 - 6, Y(v) + 4, f"{v}", 10.5, SEC, "end")
    for k, pp in enumerate(g.periodo):
        if pp[8:10] <= "07" and pp[5:7] in ("01", "03", "05", "07", "09"): S.t(X(k) + 4, y0 + hh + 33, MESES[int(pp[5:7]) - 1], 10.5, SEC, "middle")
    for vals, col, sw in ((ri, MARK, 1.8), (vi, BLUE if c == "push notification" else INK, 2.4)):
        S.raw('<path d="M' + " L".join(f"{X(k):.1f},{Y(v):.1f}" for k, v in enumerate(vals)) + f'" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linejoin="round"/>')
    ev, er = vi[-1], ri[-1]
    yv, yr = Y(ev), Y(er)
    if abs(yv - yr) < 13: yv, yr = (yv - 7, yr + 7) if yv <= yr else (yv + 7, yr - 7)
    S.t(X(n - 1) + 6, yv + 4, f"Volumen {ev:.0f}", 10.5, BLUE if c == "push notification" else INK, w=700)
    S.t(X(n - 1) + 6, yr + 4, f"Respuesta {er:.0f}", 10.5, SEC, w=600)
    km = int(np.argmax(vi)); S.t(X(km), Y(vi[km]) - 6, f"{vi[km]:.0f}", 10.5, INK, "middle", 700, halo=True)
S.t(40, 412, "Índice: promedio de las semanas de enero = 100, por canal. Más de 300 se dibuja en 300. 38 semanas completas.", 10.5, SEC)
J = dict(
    titulo="Al terminar los envíos de junio a toda la base, el push bajó a la mitad y su apertura se duplicó frente a junio",
    que="Lo que se dejó de mandar: BillPay, Día del Padre, Mundial, AnotayGana y referidos.",
    quien=f"Marketing bajó de {pt.loc['Marketing',6]/1e6:.0f} M push en junio a {pt.loc['Marketing',9]/1e6:.0f} M en septiembre; Others de {pt.loc['Others',6]/1e6:.0f} M a {pt.loc['Others',9]/1e6:.1f} M.",
    a_quien="Toda la base y leads, que recibieron los envíos de junio.",
    lecturas=[
        f"Junio: {pm.loc[6,'s']/1e6:.1f} M push y {pm.loc[6,'r']:.2f} % de apertura; septiembre: {pm.loc[9,'s']/1e6:.1f} M y {pm.loc[9,'r']:.2f} %.",
        f"Abrieron {pm.loc[6,'o']/1e3:.0f} mil push en junio y {pm.loc[9,'o']/1e3:.0f} mil en septiembre: mandar menos no costó aperturas.",
        f"Las {len(cont)} campañas que siguieron de junio a septiembre subieron de {cc.loc[6,'r']:.2f} % a {cc.loc[9,'r']:.2f} % de apertura.",
    ],
    causa="No fue decisión: acabaron los lanzamientos. Sugiere que menos volumen no cuesta aperturas, aunque el push sigue al doble de enero.",
    sowhat="Mandar menos push no costó aperturas: un límite por persona a la semana es seguro.",
    fuente="Fuente: Braze, serie semanal por canal y envíos por campaña y mes, ene a sep 2026. No es un experimento: también cambió la mezcla de campañas.",
    svg=S.out())
write(84, J)
