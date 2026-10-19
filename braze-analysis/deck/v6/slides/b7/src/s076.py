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
        f"Casi la mitad de los mensajes del año ({no.envios.sum()/1e6:.0f} M mensajes) salió de campañas que no responden lo mínimo, con {no.costo_ent.sum()/1e6:.1f} M MXN de gasto.",
        f"Son promociones a listas grandes (Tasa 0, comercios KPay, referidos, BillPay) dirigidas a leads, registrados sin crédito y ex clientes; Product Growth y Marketing ponen {100*share_pm:.0f} % de ese volumen.",
        "Nadie revisa si una campaña responde: se detiene cuando termina la promoción, no cuando deja de funcionar.",
        f"Cuando una campaña no funciona se copia con otra fecha: {(vv>=5).sum()} campañas sacaron cinco o más versiones y en septiembre {(sp>=2).sum()} tenían versiones viejas enviando a la vez.",
        "Causa raíz: las campañas se juzgan por cuántos mensajes salen y no por cuánta gente responde, y nadie es dueño de ese número ni de la decisión de apagar.",
    ],
    hipotesis={
        "A": f"Si cada campaña se compara contra lo mínimo de su canal, {len(a)} campañas promocionales activas quedan debajo y concentran {a.c9.sum()/1e6:.1f} M MXN al mes; las que salen por algo que hizo la persona responden hasta siete veces más.",
        "O": "Duplicar un Canvas y cambiarle la fecha es más rápido que leer cómo le fue al anterior, y la versión vieja se queda encendida.",
        "G": "No hay una revisión mensual de volumen contra respuesta ni una regla que diga quién apaga una campaña que no responde.",
    },
    como=[
        "Semana 1: CRM publica un tablero con las 20 campañas con más mensajes contra lo mínimo de su canal, por equipo. Métrica: % de mensajes en campañas que responden lo mínimo.",
        "Semana 2: Product Growth y Marketing rehacen o detienen las campañas que llevan dos meses debajo de lo mínimo; en Braze, al lanzar una versión nueva se archiva la anterior.",
        "Semana 3: los programas para recuperar ex clientes pasan a email o in-app primero, WhatsApp solo a quien leyó uno en 90 días, presupuesto mensual con límite y 10 % sin mensajes. Métrica: MXN por conversión.",
        "Mes 2 en adelante: revisión mensual con los dueños de cada campaña; si no responde lo mínimo dos meses seguidos, se rehace o se apaga.",
    ],
    impacto=f"Las {len(a)} campañas promocionales activas que no responden mandaron {a.env9.sum()/1e6:.0f} M mensajes y costaron {a.c9.sum()/1e6:.1f} M MXN en septiembre. Rehacerlas o detenerlas recorta ese gasto; en las de recuperación, solo si el grupo sin mensajes muestra que no recuperan.",
    sowhat="Medir antes de copiar: una revisión mensual de volumen contra respuesta, una sola versión viva por campaña y una regla para apagar lo que no responde.",
    fuente="Fuente: láminas 66 a 75. Braze, envíos por campaña, mes y canal y catálogo de comunicaciones, enero a septiembre 2026. WhatsApp a 1.00 MXN por entregado; email a 0.05 por enviado.",
)
write(76, J)
