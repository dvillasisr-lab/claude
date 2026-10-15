# -*- coding: utf-8 -*-
"""Exhibits de las gráficas rediseñadas (sin barras): cada función arma el dict que renderiza build_deck.

Los datos salen de deck_data; aquí solo se decide qué variables, qué dimensiones y qué se resalta.
"""
import deck_data as DD

TEAMS = DD.TEAMS
MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep"]
RED = "#B5342B"
CAN = {"email": "Email", "push notification": "Push", "whatsapp": "WhatsApp", "in-app": "In-app"}


def _top(pts, k, key="size", pred=None):
    sel = [q for q in pts if pred is None or pred(q)]
    return sorted(sel, key=lambda q: -q[key])[:k]


# 4. Mekko: envíos y costo por canal, apilado por equipo ---------------------------------------------------------
def ex_mekko_canal_equipo():
    ce = DD.canal_equipo()
    return {"type": "mekko", "segments": ce["teams"],
            "panels": [{"title": "Envíos por canal y equipo (ancho = peso del canal, M mensajes)", "cats": ce["cats"], "rows": ce["env"], "fmt": "M"},
                       {"title": "Costo por canal y equipo (ancho = peso del canal, M MXN)", "cats": ce["cats"], "rows": ce["cost"], "fmt": "MXN",
                        "note": f"WhatsApp es {100*sum(ce['env'][2])/sum(map(sum, ce['env'])):.0f} % de los envíos y {100*sum(ce['cost'][2])/sum(map(sum, ce['cost'])):.0f} % del costo; Marketing y Product Growth concentran el gasto."}]}


# 5. Dispersión conectada: volumen contra respuesta, mes a mes, por canal -----------------------------------------
def ex_conn_canales():
    cm = DD.canales_mes()
    panels = []
    for c, yfmt, ylab in (("email", "pct2", "clic / entregado"), ("push notification", "pct2", "apertura / enviado"), ("whatsapp", "pct0", "lectura / entregado"), ("in-app", "pct0", "clic / impresión")):
        d = cm[c]
        pts = [{"x": v, "y": r, "lab": MESES[i]} for i, (v, r) in enumerate(zip(d["vol"], d["resp"]))]
        panels.append({"title": f"{CAN[c]}: {ylab}", "pts": pts, "xfmt": "int", "yfmt": yfmt, "xlab": "Envíos del mes (M)", "hl": [0, 5, 8]})
    return {"type": "connscatter", "panels": panels, "ncol": 4,
            "note": "Cada punto es un mes, de enero (claro) a septiembre (oscuro), unido en orden. Cuando el punto se mueve a la derecha (más volumen) baja (menos respuesta): junio en email y push."}


# 8. Burbujas: push de junio, familias nuevas contra familias que ya existían --------------------------------------
def ex_bubble_push_junio():
    pts = DD.push_junio_scatter()
    for q in pts:
        q["dim"] = not q["new"]
    labels = _top(pts, 7, pred=lambda q: q["new"]) + _top(pts, 2, pred=lambda q: not q["new"])
    return {"type": "bubble", "groups": TEAMS, "size_label": "push enviados en junio",
            "panels": [{"title": "Push de junio: 65 familias; las 37 nuevas (color) contra las que ya existían (gris)", "pts": pts, "xmin": 5e4, "xmax": 1e7, "ymax": 6,
                        "fmt": "pct1", "xlab": "Push enviados en junio (escala logarítmica)", "ref": (0.75, "mínimo push 0.75 %"), "labels": labels}],
            "note": "Las familias nuevas de junio concentran el volumen y quedan debajo del mínimo; las que ya existían abren más."}


# 9. Pendientes: lectura de WhatsApp, enero a junio contra julio a septiembre --------------------------------------
def ex_slope_wa():
    ws = DD.wa_slope()
    def items(lst):
        return [{"name": q["name"], "a": q["a"], "b": q["b"], "w": q["va"] + q["vb"], "sub": f"{q['va']+q['vb']:.0f} M"} for q in lst]
    return {"type": "slope", "panels": [
        {"title": "Lectura de WhatsApp por grupo de audiencia", "cols": ("Ene a Jun", "Jul a Sep"), "items": items(ws["grupos"]), "fmt": "pct0", "ref": (60, "mínimo 60 %"), "drop": 4, "ymin": 50, "ymax": 85},
        {"title": "Lectura de WhatsApp por equipo", "cols": ("Ene a Jun", "Jul a Sep"), "items": items(ws["equipos"]), "fmt": "pct0", "ref": (60, "mínimo 60 %"), "drop": 4, "ymin": 50, "ymax": 85}],
        "note": "Rojo: cae 4 puntos o más. Grosor de la línea: WhatsApp entregados. Todos los grupos y equipos pierden lectura en el segundo tramo."}


# 13. Paralelas: tres grupos de usuarios en cuatro medidas ---------------------------------------------------------
def ex_parallel_usuarios():
    u = DD.usuarios_cascada()
    tot_u, tot_m, tot_c = u["tot"], sum(u["msgs"].values()), u["conv_tot"]
    lines = []
    for k, name in (("none", "No respondió a nada"), ("one", "Respondió en un canal"), ("multi", "Respondió en dos o más")):
        lines.append({"name": name, "vals": [100 * (u[k] if k != "none" else u["none"]) / tot_u, 100 * u["msgs"][k] / tot_m, 100 * u["conv"][k] / tot_c, u["msgs"][k] / u[k]]})
    return {"type": "parallel", "label": "Cada línea es un grupo de usuarios; cada eje, su peso en una medida",
            "axes": [{"name": "% de los usuarios", "fmt": "pct0", "lo": 0, "hi": 100, "sub": ""}, {"name": "% de los mensajes", "fmt": "pct0", "lo": 0, "hi": 100, "sub": ""},
                     {"name": "% de las conversiones", "fmt": "pct0", "lo": 0, "hi": 100, "sub": ""}, {"name": "Mensajes por usuario", "fmt": "int", "lo": 0, "sub": "en 9 meses"}],
            "lines": lines, "emph": ["No respondió a nada", "Respondió en dos o más"], "colors": {"No respondió a nada": RED, "Respondió en un canal": "#A3AAB5", "Respondió en dos o más": "#1F9E89"},
            "note": "73 % de los usuarios recibe 24 % de los mensajes y aporta 1 % de las conversiones; 11 % recibe 52 % y aporta 86 %."}


# 15. Mapa de calor con tinte: patrón de respuesta por usuario contra mensajes por canal ---------------------------
def ex_heat_patron():
    pm = DD.patron_matrix()
    return {"type": "heatmap", "rows": pm["rows"], "cols": pm["cols"], "matrix": pm["matrix"], "tint": pm["tint"], "row_share": pm["row_share"],
            "share_label": "% de los usuarios", "fmt": "int", "label": "M mensajes por canal (columnas) según lo que el usuario respondió alguna vez (filas)", "labw": 160, "col_scale": True}


# 16. Áreas + acumulado: mensajes a usuarios que nunca respondieron, por canal, y costo acumulado -----------------
def ex_areacum_mudos():
    m = DD.mudos_mes_canal()
    return {"type": "areacum", "cats": m["cats"], "series": m["series"], "label": "M mensajes al mes a usuarios que nunca respondieron en ningún canal", "fmt": "M",
            "highlight": [5], "cum": m["cum_cost"], "cum_label": "Costo acumulado de esos mensajes (M MXN)", "cum_fmt": "MXN",
            "note": f"{m['tot']:.0f} M mensajes en 9 meses a 14.2 M usuarios mudos; junio triplica el email a mudos (16.8 M)."}


# 18. Burbujas: familias promocionales que llegan a usuarios bloqueados --------------------------------------------
def ex_bubble_bloqueados():
    b = DD.bloqueados_familias()
    labels = _top(b["pts"], 8)
    return {"type": "bubble", "groups": TEAMS, "size_label": "envíos a bloqueados",
            "panels": [{"title": "Familias promocionales: envíos totales contra % que fue a usuarios bloqueados", "pts": b["pts"], "xmin": 1e5, "xmax": 5e7, "ymax": 70, "ymin": 0,
                        "fmt": "pct0", "xlab": "Envíos de la familia en 9 meses (escala logarítmica)", "ref": (20, "1 de cada 5"), "labels": labels}],
            "note": f"{b['tot']:.1f} M envíos promocionales a bloqueados: Marketing {b['by_team'].get('Marketing',0):.1f} M, Sales {b['by_team'].get('Sales',0):.1f} M, Product Growth {b['by_team'].get('Product Growth',0):.1f} M."}


# 20. Combo de líneas: entrega de email y de WhatsApp por equipo y mes ----------------------------------------------
def ex_combo_entrega():
    e = DD.entrega_equipo_mes()
    cols = {t: i for i, t in enumerate(TEAMS)}
    def ser(lst):
        lst = sorted(lst, key=lambda q: cols.get(q[0], 9))
        return [(t, v) for t, v in lst], [DD_PAL[cols.get(t, 4)] for t, _ in lst]
    se, ce = ser(e["email"]); sw, cw = ser(e["wa"])
    return {"type": "combo", "H": 330, "panels": [
        {"kind": "line", "title": "Email entregado / enviado, por equipo", "cats": MESES, "series": se, "cols": ce, "fmt": "pct0", "ymin": 85, "ymax": 100, "legend": True, "ref": (95, "mínimo 95 %"), "xlab": ""},
        {"kind": "line", "title": "WhatsApp entregado / enviado, por equipo", "cats": MESES, "series": sw, "cols": cw, "fmt": "pct0", "ymin": 55, "ymax": 95, "legend": True, "ref": (85, "mínimo 85 %"), "xlab": ""}],
        "note": "Email entrega 94 a 97 % y es estable. WhatsApp entrega 61 a 89 %: Product Growth y Others van debajo de 75 % casi todos los meses y cada no entregado se paga."}


DD_PAL = ["#1F4FD8", "#B5342B", "#1F9E89", "#A8720F", "#7C5CC4"]


# 22. Lorenz: concentración de mensajes, bajas y conversiones -------------------------------------------------------
def ex_lorenz():
    lz = DD.lorenz()
    return {"type": "lorenz", "pts": lz["pts"], "series": lz["series"], "label": "% acumulado de mensajes, bajas y conversiones contra % acumulado de usuarios", "mark": [3]}


# 24. Mapa de calor: choque de equipos en el mismo usuario el mismo día --------------------------------------------
def ex_heat_choque():
    c = DD.choque_matriz()
    return {"type": "heatmap", "rows": c["rows"], "cols": c["cols"], "matrix": c["matrix"], "fmt": "x1", "labw": 150, "triangle": True,
            "label": f"M usuario-días con dos envíos el mismo día ({c['tot']:.0f} M); diagonal: el mismo equipo se repite"}


# 25. Combo: curva de bajas por días desde el primer email + familias que más bajas generan ------------------------
def ex_combo_bajas_dias():
    b = DD.bajas_dias()
    cum_d = [("% de las bajas acumulado", b["dias"]["cum"])]
    cum_e = [("% de las bajas acumulado", b["emails"]["cum"])]
    pts = b["fams"]
    cats_d = ["0 d", "7 d", "30 d", "90 d", "180 d", "más"]
    cats_e = ["1", "3", "10", "30", "más"]
    return {"type": "combo", "H": 330, "panels": [
        {"kind": "line", "w": 1, "title": "Días desde el primer email hasta la baja", "cats": cats_d, "series": cum_d, "fmt": "pct0", "ymin": 0, "ymax": 115, "point_labels": True, "end_labels": False, "xlab": "Días desde el primer email (acumulado)"},
        {"kind": "line", "w": 0.9, "title": "Emails recibidos antes de darse de baja", "cats": cats_e, "series": cum_e, "fmt": "pct0", "ymin": 0, "ymax": 115, "point_labels": True, "end_labels": False, "xlab": "Emails recibidos (acumulado)"},
        {"kind": "bubble", "w": 1.3, "title": "Familias que más bajas generan (mil)", "pts": pts, "groups": [t for t in TEAMS if any(q["g"] == t for q in pts)], "xmin": 1, "xmax": 200, "ymin": 0, "fmt": "int",
         "xticks": [(1, "1"), (7, "7"), (30, "30"), (90, "90"), (180, "180")], "xlab": "Días medianos hasta la baja", "labels": _top(pts, 5, key="y"), "rmax": 16}],
        "note": f"{b['tot']/1e3:.0f} mil usuarios nuevos se dieron de baja; la mitad en el primer mes y 45 % con 3 emails o menos."}


# 26. Burbujas: familias de email por entregados y bajas por mil -----------------------------------------------------
def ex_bubble_bajas_fam():
    b = DD.bajas_familias()
    pts = b["pts"]
    tot_d = sum(q["x"] for q in pts)
    ref = 1000 * b["tot"] / tot_d
    labels = _top(pts, 8)
    return {"type": "bubble", "groups": TEAMS, "size_label": "bajas generadas",
            "panels": [{"title": "Familias de email con 300 mil entregados o más: entregados contra bajas por mil", "pts": pts, "xmin": 3e5, "xmax": 5e7, "ymax": 8, "fmt": "x1",
                        "xlab": "Emails entregados en 9 meses (escala logarítmica)", "ref": (ref, f"promedio {ref:.1f} por mil"), "labels": labels}],
            "note": f"8 familias generan {b['top8_share']:.0f} % de las bajas; las de arriba a la derecha son grandes y queman la base a la vez."}


# 27. Burbujas por paso de Canvas: usuarios que llegan al paso contra % que abre -----------------------------------
def ex_strip_pasos():
    p = DD.pasos_scatter()
    st = p["stats"]
    rows = []
    for b in p["bands"]:
        pts = [{"x": q["y"], "size": q["x"], "label": q["label"], "g": q["team"]} for q in p["pts"] if q["g"] == b]
        rows.append({"gancho": b, "pts": pts, "wmean": st[b]["wopen"], "vol": sum(q["size"] for q in pts), "n": st[b]["n"],
                     "labels": _top(pts, 1, pred=lambda q: q["x"] < 1), "sub": f"{st[b]['under1']} pasos debajo de 1 %"})
    return {"type": "strip", "rows": rows, "label": "Apertura de cada paso de push en Canvas (un punto por paso), por posición del paso; barra azul: promedio ponderado",
            "size_label": "Tamaño: usuarios que reciben el paso", "xmin": 0.1, "xmax": 100, "jitter": True, "rh": 52,
            "xticks": [(0.1, "0.1 %"), (0.3, "0.3 %"), (1, "1 %"), (3, "3 %"), (10, "10 %"), (30, "30 %"), (100, "100 %")], "refs": [(1, "1 % de apertura", RED)],
            "note": f"La posición del paso no cambia la apertura (15 a 23 %). Lo que sí: {p['under1']} pasos de 2,073 abren menos de 1 % y siguen activos; 204 están del paso 5 en adelante."}


# 30. Dispersión conectada: antigüedad del usuario, mensajes por usuario contra respuesta ---------------------------
def ex_conn_antiguedad():
    a = DD.antiguedad_usuario()
    return {"type": "connscatter", "ncol": 2, "panels": [
        {"title": "Push: push por usuario contra apertura, por antigüedad", "pts": a["push"], "xfmt": "int", "yfmt": "pct2", "xlab": "Push por usuario en 9 meses", "label_all": True, "hl": [0, len(a["push"]) - 1]},
        {"title": "Email: emails por usuario contra clic, por antigüedad", "pts": a["email"], "xfmt": "int", "yfmt": "pct2", "xlab": "Emails por usuario en 9 meses", "label_all": True, "hl": [0, len(a["email"]) - 1]}],
        "note": "De izquierda a derecha, usuarios más antiguos. A los antiguos se les manda hasta 7 veces más push y responden 3 veces menos."}


# 32. Tira de puntos: ganchos del email, cada familia un punto, promedio ponderado marcado ---------------------------
def ex_strip_gancho():
    rows = DD.gancho_strip()
    for r in rows:
        r["labels"] = _top(r["pts"], 1)
        r["dim"] = r["wmean"] < 0.3
    return {"type": "strip", "rows": rows, "label": "Clic / entregado por gancho del email: cada punto es una familia, la barra azul el promedio ponderado",
            "size_label": "emails entregados", "xmin": 0.03, "xmax": 12, "refs": [(0.3, "mínimo email 0.3 %", RED)],
            "note": "Recordatorios y cobranza (lo que el usuario ya empezó) responden 10 veces más que descuentos, lanzamientos y referidos."}


# 35. Burbujas: tamaño de audiencia por envío contra clic, color por número de toques ------------------------------
def ex_bubble_toques():
    pts = DD.tamano_toques()
    groups = ["1 toque", "2 toques", "3 o más toques"]
    labels = _top(pts, 5) + _top(pts, 3, key="y", pred=lambda q: q["size"] > 1e6)
    return {"type": "bubble", "groups": groups, "size_label": "emails entregados",
            "panels": [{"title": "Familias de email: usuarios por envío contra clic, por toques al mismo usuario", "pts": pts, "xmin": 1e3, "xmax": 3e7, "ymax": 2.2, "fmt": "pct1",
                        "xlab": "Usuarios alcanzados por envío (escala logarítmica)", "ref": (0.3, "mínimo email 0.3 %"), "labels": labels}],
            "note": "Mientras más grande la audiencia por envío y más toques repetidos, menos clic. Las familias arriba de 2.2 % se muestran en el borde superior."}


# 40. Paralelas: tarjeta por equipo en siete medidas ----------------------------------------------------------------
def ex_parallel_scorecard():
    sc = DD.scorecard()
    axes = [{"name": "Email clic", "fmt": "pct2", "sub": "mínimo 0.30 %"}, {"name": "Push apertura", "fmt": "pct2", "sub": "mínimo 0.75 %"},
            {"name": "WhatsApp lectura", "fmt": "pct0", "sub": "mínimo 60 %"}, {"name": "WhatsApp entrega", "fmt": "pct0", "sub": "mínimo 85 %"},
            {"name": "In-app clic", "fmt": "pct0", "sub": "mínimo 10 %"}, {"name": "Bajas por mil emails", "fmt": "x1", "invert": True, "sub": "invertido: menos es mejor"},
            {"name": "% envíos que insisten", "fmt": "pct0", "invert": True, "sub": "invertido: menos es mejor"}]
    lines = [{"name": t, "vals": [sc[t]["email"], sc[t]["push"], sc[t]["wa"], sc[t]["wa_del"], sc[t]["inapp"], sc[t]["bajas"], sc[t]["insiste"]]} for t in TEAMS]
    return {"type": "parallel", "axes": axes, "lines": lines, "label": "Cada línea es un equipo; cada eje, una medida (arriba siempre es mejor)",
            "note": "Product Growth va abajo en email y arriba en insistencia; Marketing quema más la base (bajas); Collections y Others responden mejor con menos volumen."}


# 41. Insistencia: familias que siguieron mandando después de fallar el mínimo ---------------------------------------
def ex_insist():
    rows = DD.insisten_familias()
    cells = []
    for r in rows:
        fmt = "pct2" if r["canal"] in ("email", "push notification") else "pct0"
        cells.append({"title": r["label"], "sub": f"{r['team']} · {CAN.get(r['canal'], r['canal'])} · {sum(r['env']):.0f} M envíos", "team": r["team"], "resp": r["resp"],
                      "min": r["min"], "fail": r["fail"], "fmt": fmt, "after": f"{r['after']:.1f} M enviados después de fallar"})
    return {"type": "insist", "cells": cells, "cats": MESES}


# 43. Pareto: familias por volumen contra respuestas acumuladas -------------------------------------------------------
def ex_pareto():
    p = DD.pareto_piezas()
    return {"type": "pareto", "panels": [
        {"title": f"Email: {p['Email']['n']} familias", "pts": p["Email"]["pts"], "mark": 10, "label_idx": [0, 1, 2], "fmt": "pct2"},
        {"title": f"Push: {p['Push']['n']} familias", "pts": p["Push"]["pts"], "mark": 10, "label_idx": [0, 1, 2], "fmt": "pct2"}],
        "note": "Cuando la línea azul va arriba de la verde, las familias grandes aportan menos respuestas de las que su volumen justifica."}


# 46. Matriz de puntos: orden por equipo crudo ------------------------------------------------------------------------
def ex_dot_orden():
    rows = DD.orden_equipo(9)
    out = [{"label": r["label"], "sub": r["g"] if r["g"] != r["label"] else "", "g": r["g"], "vals": [r["n"], r["sin_ticket"], r["sin_conv"]], "total": f"{r['env']:.0f} M"} for r in rows]
    return {"type": "dotmatrix", "rows": out, "cols": ["Piezas en Braze", "Sin ticket", "Nombre fuera de norma"], "label": "Piezas por equipo tal como aparecen en Braze y cuántas rompen las reglas",
            "row_total_label": "Envíos 9 meses", "fmt": "int", "labw": 200, "note": "Not Tracked: 748 piezas sin dueño ni ticket que mandaron 85 M mensajes. QA/Test: 321 piezas, 4.5 M mensajes a usuarios reales."}


# 47. Matriz de puntos: versiones nuevas por familia y mes --------------------------------------------------------------
def ex_dot_versiones():
    v = DD.versiones_mes()
    rows = [{"label": r["label"], "sub": r["team"], "g": r["team"], "vals": r["n"], "total": f"{r['tot']} versiones · {sum(r['env']):.1f} M envíos"} for r in v["rows"]]
    return {"type": "dotmatrix", "rows": rows, "cols": v["cats"], "label": "Comunicaciones nuevas creadas cada mes dentro de la misma familia (misma audiencia y gancho)",
            "row_total_label": "Total", "fmt": "int", "labw": 230, "note": f"{v['n_fam5']} familias tienen 5 versiones o más; se vuelve a crear la pieza en vez de medir la que existe."}


# 50. Matriz de puntos: acciones del plan por equipo -----------------------------------------------------------------
AHORRO_EQUIPO = {"Product Growth": 1.30, "Marketing": 0.16, "Sales": 0.10, "Collections": 0.0, "Others": 0.04}


def ex_dot_acciones():
    a = DD.acciones_equipo()
    rows = [{"label": t, "g": t, "vals": a["n"][i], "total": f"{AHORRO_EQUIPO.get(t, 0):.2f} M MXN/mes"} for i, t in enumerate(a["rows"])]
    cols = ["Apagar", "Limpiar WhatsApp", "Re-segmentar", "Bajar frecuencia", "Proteger", "Escalar"]
    return {"type": "dotmatrix", "rows": rows, "cols": cols, "label": "Campañas activas en septiembre por acción recomendada y equipo (número = campañas)",
            "row_total_label": "Ahorro al mes", "fmt": "int", "labw": 190, "note": "Product Growth concentra el ahorro: apagar y re-segmentar sus Canvas de Tasa 0 y nuevos registrados."}


# 65. Burbujas: segmentos por envíos y respuesta, tamaño conversiones -------------------------------------------------
def ex_bubble_segmentos():
    pts = DD.segmentos_scatter()
    return {"type": "bubble", "groups": TEAMS, "size_label": "conversiones",
            "panels": [{"title": "Segmentos más usados: envíos contra respuesta, tamaño conversiones", "pts": pts, "xmin": 1e6, "xmax": 5e8, "ymax": max(q["y"] for q in pts) * 1.15, "fmt": "pct1",
                        "xlab": "Envíos en 9 meses (escala logarítmica)", "labels": pts, "rmax": 26}],
            "note": "Leads recibe lo más y responde poco; los segmentos pequeños de usuarios activos convierten más por envío."}


EXHIBITS = {
    "mekko_canal_equipo": ex_mekko_canal_equipo, "conn_canales": ex_conn_canales, "bubble_push_junio": ex_bubble_push_junio, "slope_wa": ex_slope_wa,
    "parallel_usuarios": ex_parallel_usuarios, "heat_patron": ex_heat_patron, "areacum_mudos": ex_areacum_mudos, "bubble_bloqueados": ex_bubble_bloqueados,
    "combo_entrega": ex_combo_entrega, "lorenz": ex_lorenz, "heat_choque": ex_heat_choque, "combo_bajas_dias": ex_combo_bajas_dias, "bubble_bajas_fam": ex_bubble_bajas_fam,
    "strip_pasos": ex_strip_pasos, "conn_antiguedad": ex_conn_antiguedad, "strip_gancho": ex_strip_gancho, "bubble_toques": ex_bubble_toques,
    "parallel_scorecard": ex_parallel_scorecard, "insist": ex_insist, "pareto": ex_pareto, "dot_orden": ex_dot_orden, "dot_versiones": ex_dot_versiones,
    "dot_acciones": ex_dot_acciones, "bubble_segmentos": ex_bubble_segmentos,
}
