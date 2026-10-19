"""Lámina 76: cierre de la sección VIII. Cifras recalculadas aquí (mismas reglas que 66, 68 y 74)."""
from b7 import *

c = load_c(); e = load_e1()
no = c[c.senal == "apagar o rehacer"]
s9 = e[e.m == 9].groupby(["fam", "canal"]).agg(env9=("envios", "sum"), c9=("costo", "sum")).reset_index()
a = no[(no.tipo == "promocional o lifecycle") & (no.activo_sep == 1)].merge(s9, left_on=["familia", "canal"], right_on=["fam", "canal"], how="left")
pe = no[no.tipo == "promocional o lifecycle"]
share_pm = pe[pe.equipo.isin(["Product Growth", "Marketing"])].envios.sum() / pe.envios.sum()
c2 = pd.read_csv(D + "e2_catalogo.csv", low_memory=False); c2["fam"] = c2.nombre.fillna("").map(fam_of)
c2["fs"] = pd.to_datetime(c2.first_sent, errors="coerce")
vv = c2[(c2.fs >= "2026-01-01") & (c2.fs < "2026-10-01")].groupby("fam").communication_id.nunique()
fe = e[e.envios > 0]; sp = fe[fe.m == 9].groupby("fam").communication_id.nunique()
print(no.envios.sum() / 1e6, no.costo_ent.sum() / 1e6, len(a), a.env9.sum() / 1e6, a.c9.sum() / 1e6, share_pm, (vv >= 5).sum(), (sp >= 2).sum())
J = dict(
    kind="cierre",
    titulo="Por qué pasa: nadie compara volumen contra respuesta, y copiar una campaña es más fácil que medirla",
    porques=[
        f"{no.envios.sum()/1e6:.0f} M mensajes, casi la mitad del año, salieron de campañas que no responden lo mínimo.",
        f"Son promociones a listas grandes; Product Growth y Marketing ponen {100*share_pm:.0f} % de ese volumen.",
        "Una campaña se detiene cuando acaba la promoción, no cuando deja de responder.",
        f"Si no funciona, se copia con otra fecha: {(vv>=5).sum()} campañas sacaron cinco o más versiones.",
        "Causa raíz: se juzga cuánto sale y no cuánto responde, y nadie es dueño de ese número.",
    ],
    hipotesis={
        "A": f"{len(a)} campañas activas no responden lo mínimo y gastan {a.c9.sum()/1e6:.1f} M MXN al mes.",
        "O": "Duplicar un Canvas es más rápido que leer cómo le fue, y la versión vieja sigue encendida.",
        "G": "No hay revisión mensual de respuesta ni una regla que diga quién apaga.",
    },
    como=[
        "Semana 1: CRM publica las 20 campañas más grandes contra lo mínimo de su canal, por equipo.",
        "Semana 2: Product Growth y Marketing rehacen o detienen las que llevan dos meses debajo.",
        "Semana 3: en Braze, al lanzar una versión nueva se archiva la anterior.",
        "Cada mes: revisión con dueños; dos meses debajo de lo mínimo, se rehace o se apaga.",
    ],
    impacto=f"Las {len(a)} campañas activas que no responden costaron {a.c9.sum()/1e6:.1f} M MXN y {a.env9.sum()/1e6:.0f} M mensajes en septiembre.",
    sowhat="Medir antes de copiar: revisión mensual, una versión viva por campaña y regla de apagado.",
    fuente="Fuente: láminas 66 a 75. Braze, envíos por campaña, mes y canal y catálogo, ene a sep 2026. WhatsApp a 1.00 MXN por entregado.",
)
write(76, J)
