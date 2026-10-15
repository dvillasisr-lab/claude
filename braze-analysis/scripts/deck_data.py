"""Datos multivariable para las gráficas del deck, calculados desde data/*.csv."""
import csv
import math
import re
import os
import statistics
from collections import defaultdict

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
TEAMS = ["Product Growth", "Marketing", "Sales", "Collections", "Others"]
MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep"]


TEAM_MAP = {"Lending": "Product Growth", "Product Growth": "Product Growth", "Marketing": "Marketing", "Sales": "Sales", "B2B": "Sales", "Collections": "Collections"}


def team_of(t):
    return TEAM_MAP.get((t or "").strip(), "Others")


def rows(name):
    with open(os.path.join(DATA, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def mes_idx(s):
    return int(s[5:7]) - 1


# 1. Scatter: tamaño de la pieza contra respuesta, por canal y equipo (E1)
def scatter_piezas(min_deliv=200_000):
    agg = {}
    for r in rows("e1_comunicacion_mes_canal.csv"):
        c = r["canal"]
        if c not in ("email", "push notification"):
            continue
        k = (r["communication_id"], c)
        a = agg.setdefault(k, {"name": r["communication_name"], "team": team_of(r["team"]), "canal": c, "deliv": 0.0, "resp": 0.0, "env": 0.0})
        if c == "email":
            a["deliv"] += f(r["email_delivery"]); a["resp"] += f(r["email_click"])
        else:
            a["deliv"] += f(r["pn_send"]); a["resp"] += f(r["pn_open"])
        a["env"] += f(r["envios"])
    out = {"email": [], "push": []}
    for a in agg.values():
        if a["deliv"] < min_deliv:
            continue
        out["email" if a["canal"] == "email" else "push"].append({
            "x": a["deliv"], "y": 100 * a["resp"] / a["deliv"], "g": a["team"], "name": a["name"]})
    return out


# 2. Series por canal y mes: envíos y respuesta (E4a)
def canales_mes():
    out = {}
    for r in rows("e4a_serie_semana_mes_canal.csv"):
        if r["grano"] != "mes":
            continue
        m = mes_idx(r["periodo"])
        c = r["canal"]
        if c == "email":
            v, resp = f(r["email_sent"]), 100 * f(r["email_click"]) / max(1, f(r["email_delivery"]))
        elif c == "push notification":
            v, resp = f(r["pn_send"]), 100 * f(r["pn_open"]) / max(1, f(r["pn_send"]))
        elif c == "whatsapp":
            v, resp = f(r["whatsapp_send"]), 100 * f(r["whatsapp_read"]) / max(1, f(r["whatsapp_delivery"]))
        elif c == "in-app":
            v, resp = f(r["in_app_impression"]), 100 * f(r["in_app_click"]) / max(1, f(r["in_app_impression"]))
        else:
            continue
        d = out.setdefault(c, {"vol": [0.0] * 9, "resp": [0.0] * 9})
        d["vol"][m] = v / 1e6
        d["resp"][m] = resp
    return out


# 3. Dispersión de respuesta por familia dentro de cada equipo (E7a)
def dispersion_equipo(canal="email", min_env=100_000):
    agg = defaultdict(lambda: {"env": 0.0, "resp": 0.0, "team": None})
    for r in rows("e7a_familia_canal_etapa.csv"):
        if r["canal"] != canal:
            continue
        a = agg[r["familia"]]
        a["env"] += f(r["envios"]); a["resp"] += f(r["respuestas"]); a["team"] = team_of(r["equipo"])
    by = defaultdict(list)
    for fam, a in agg.items():
        if a["env"] >= min_env:
            by[a["team"]].append((100 * a["resp"] / a["env"], a["env"], fam))
    out = []
    for t in TEAMS:
        pts = by.get(t, [])
        if len(pts) < 3:
            continue
        vals = [p[0] for p in pts]
        wmean = sum(p[0] * p[1] for p in pts) / sum(p[1] for p in pts)
        out.append({"cat": t, "n": len(pts), "mean": statistics.mean(vals), "sd": statistics.pstdev(vals),
                    "median": statistics.median(vals), "wmean": wmean, "pts": [(p[0], p[1]) for p in pts]})
    return out


# 4. Mapa de calor: clic de email por equipo y día de la semana (E10) + % de envíos por día
def heat_dia():
    days = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    order = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}
    ent = defaultdict(lambda: [0.0] * 7); resp = defaultdict(lambda: [0.0] * 7)
    env_day = [0.0] * 7
    for r in rows("e10_dia_semana.csv"):
        if r["canal"] != "email":
            continue
        d = order[r["dia_semana"]]
        t = team_of(r["team"])
        ent[t][d] += f(r["email_entregados"]); resp[t][d] += f(r["respuestas"])
        ent["Todos"][d] += f(r["email_entregados"]); resp["Todos"][d] += f(r["respuestas"])
        env_day[d] += f(r["envios"])
    tot = sum(env_day)
    cats = ["Todos"] + [t for t in TEAMS if sum(ent[t]) > 1e6]
    matrix = [[(100 * resp[t][d] / ent[t][d]) if ent[t][d] > 50_000 else None for d in range(7)] for t in cats]
    return {"cols": days, "rows": cats, "matrix": matrix, "share": [100 * v / tot for v in env_day]}


# 5. Bajas por banda de mensajes al mes, comparando meses (E4b)
def bandas_mes(meses=(0, 5, 8)):
    bands = ["01-05", "06-10", "11-20", "21-40", "41-80", "081-160", "161+"]
    labels = ["1 a 5", "6 a 10", "11 a 20", "21 a 40", "41 a 80", "81 a 160", "161+"]
    d = defaultdict(dict)
    for r in rows("e4b_concentracion_mes.csv"):
        if r["banda_msgs_mes"] in bands:
            d[mes_idx(r["mes"])][r["banda_msgs_mes"]] = (f(r["usuarios"]), f(r["usuarios_con_baja_email"]))
    series = []
    for m in meses:
        vals = [100 * d[m][b][1] / max(1, d[m][b][0]) for b in bands]
        series.append((MESES[m], vals))
    return {"cats": labels, "series": series}


# 5b. Bandas de mensajes en el periodo: usuarios, bajas y conversión (E3)
def bandas_periodo():
    bands = ["01-05", "06-10", "11-20", "21-40", "41-80", "081-160", "161-320", "321+"]
    labels = ["1 a 5", "6 a 10", "11 a 20", "21 a 40", "41 a 80", "81 a 160", "161 a 320", "321+"]
    d = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])
    for r in rows("e3_usuarios_distribucion.csv"):
        b = r["banda_msgs"]
        if b in bands:
            d[b][0] += f(r["usuarios"]); d[b][1] += f(r["bajas_email"]); d[b][2] += f(r["usuarios_con_conversion"]); d[b][3] += f(r["msgs"])
    return {"cats": labels,
            "usuarios": [d[b][0] / 1e6 for b in bands],
            "msgs": [d[b][3] / 1e6 for b in bands],
            "bajas": [100 * d[b][1] / max(1, d[b][0]) for b in bands],
            "conv": [100 * d[b][2] / max(1, d[b][0]) for b in bands]}


# 6. Antigüedad: envíos, clic de email, apertura de push y bajas por mil (E12)
def antiguedad():
    bands = ["0. menos de 1 mes", "1. 1 a 3 meses", "2. 3 a 6 meses", "3. 6 a 12 meses", "4. 1 a 2 años", "5. más de 2 años"]
    labels = ["< 1 mes", "1 a 3 m", "3 a 6 m", "6 a 12 m", "1 a 2 años", "> 2 años"]
    env = defaultdict(float); e_env = defaultdict(float); e_resp = defaultdict(float)
    p_env = defaultdict(float); p_resp = defaultdict(float); bajas = defaultdict(float)
    for r in rows("e12_antiguedad.csv"):
        b = r["banda_antiguedad"]
        if b not in bands:
            continue
        env[b] += f(r["envios"]); bajas[b] += f(r["bajas_email_eventos"])
        if r["canal"] == "email":
            e_env[b] += f(r["envios"]); e_resp[b] += f(r["respuestas"])
        if r["canal"] == "push notification":
            p_env[b] += f(r["envios"]); p_resp[b] += f(r["respuestas"])
    return {"cats": labels,
            "vol": [env[b] / 1e6 for b in bands],
            "click": [100 * e_resp[b] / max(1, e_env[b]) for b in bands],
            "push": [100 * p_resp[b] / max(1, p_env[b]) for b in bands],
            "bajas": [1000 * bajas[b] / max(1, e_env[b]) for b in bands]}


# 7. Solape: respuesta y baja por usuario-día según campañas distintas ese día, por mes (E6a)
def solape_mes():
    bands = ["1", "2", "3 a 4", "5 a 7", "8+"]
    d = defaultdict(dict)
    for r in rows("e6a_solape_dia_mes.csv"):
        d[r["banda_familias_dia"]][mes_idx(r["mes"])] = (f(r["usuario_dias"]), f(r["usuario_dias_con_respuesta"]), f(r["usuario_dias_con_baja"]))
    resp = [(b, [100 * d[b][m][1] / max(1, d[b][m][0]) for m in range(9)]) for b in bands]
    baja = [(b, [1000 * d[b][m][2] / max(1, d[b][m][0]) for m in range(9)]) for b in bands]
    share = [(b, [d[b][m][0] for m in range(9)]) for b in bands]
    return {"cats": MESES, "resp": resp, "baja": baja, "share": share}



# ---- Bloque 2: regresión, distribución, velas, semanas, cascada, segmentos, mudos ----
def _ols(xs, ys):
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs); sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    b = sxy / sxx; a = my - b * mx
    ss = sum((y - my) ** 2 for y in ys); sr = sum((y - (a + b * x)) ** 2 for x, y in zip(xs, ys))
    return {"a": a, "b": b, "r2": 1 - sr / ss if ss else 0.0, "n": n}


def _semanas():
    """Semanas completas (lunes 5 ene a lunes 21 sep) por canal: (semana, volumen M, respuesta %)."""
    out = defaultdict(list)
    for r in rows("e4a_serie_semana_mes_canal.csv"):
        if r["grano"] != "semana" or not ("2026-01-05" <= r["periodo"] <= "2026-09-21"):
            continue
        c = r["canal"]
        if c == "email":
            v, resp = f(r["email_sent"]), 100 * f(r["email_click"]) / max(1, f(r["email_delivery"]))
        elif c == "push notification":
            v, resp = f(r["pn_send"]), 100 * f(r["pn_open"]) / max(1, f(r["pn_send"]))
        elif c == "whatsapp":
            v, resp = f(r["whatsapp_send"]), 100 * f(r["whatsapp_read"]) / max(1, f(r["whatsapp_delivery"]))
        elif c == "in-app":
            v, resp = f(r["in_app_impression"]), 100 * f(r["in_app_click"]) / max(1, f(r["in_app_impression"]))
        else:
            continue
        out[c].append((r["periodo"], v / 1e6, resp))
    for c in out:
        out[c].sort()
    return out


# 8. Regresión semanal: volumen de la semana contra respuesta (E4a)
def regresion_semana():
    W = _semanas()
    out = {}
    for c in ("email", "push notification", "whatsapp"):
        pts = [{"x": v, "y": resp, "lab": p[5:].replace("-", "/"), "g": MESES[int(p[5:7]) - 1]} for p, v, resp in W[c]]
        fit = _ols([q["x"] for q in pts], [q["y"] for q in pts])
        out[c] = {"pts": pts, "fit": fit}
    return out


# 9. Regresión por día y equipo: tamaño por pieza contra clic de email (E10)
def regresion_dia():
    order = {"Monday": "Lun", "Tuesday": "Mar", "Wednesday": "Mié", "Thursday": "Jue", "Friday": "Vie", "Saturday": "Sáb", "Sunday": "Dom"}
    agg = defaultdict(lambda: defaultdict(float))
    for r in rows("e10_dia_semana.csv"):
        if r["canal"] != "email":
            continue
        k = (order[r["dia_semana"]], team_of(r["team"]))
        for c in ("envios", "usuarios_aprox", "comunicaciones", "email_entregados", "respuestas"):
            agg[k][c] += f(r[c])
    pts = []
    for (d, t), a in agg.items():
        if a["email_entregados"] < 50_000:
            continue
        pts.append({"x": a["envios"] / a["comunicaciones"], "y": 100 * a["respuestas"] / a["email_entregados"], "g": t,
                    "mk": "d" if d in ("Sáb", "Dom") else "o", "lab": f"{d} {t}", "dia": d,
                    "piezas": a["comunicaciones"], "env": a["envios"], "por_usuario": a["envios"] / max(1, a["usuarios_aprox"])})
    promo = [q for q in pts if q["g"] in ("Product Growth", "Marketing", "Sales")]
    fit = _ols([math.log10(q["x"]) for q in promo], [q["y"] for q in promo])
    todo = _ols([math.log10(q["x"]) for q in pts], [q["y"] for q in pts])
    dias = {}
    for d in ("Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"):
        a = defaultdict(float)
        for (dd, t), v in agg.items():
            if dd == d:
                for c in v:
                    a[c] += v[c]
        dias[d] = {"env": a["envios"] / 1e6, "piezas": a["comunicaciones"], "tam": a["envios"] / a["comunicaciones"],
                   "por_usuario": a["envios"] / a["usuarios_aprox"], "clic": 100 * a["respuestas"] / a["email_entregados"]}
    return {"pts": pts, "fit": fit, "fit_todos": todo, "dias": dias}


# 10. Distribución de la respuesta por pieza-mes: histograma y campana normal (E1)
def distribucion_piezas(min_deliv=100_000):
    vals = {"email": [], "push": []}
    for r in rows("e1_comunicacion_mes_canal.csv"):
        if r["canal"] == "email" and f(r["email_delivery"]) >= min_deliv:
            vals["email"].append(100 * f(r["email_click"]) / f(r["email_delivery"]))
        elif r["canal"] == "push notification" and f(r["pn_send"]) >= min_deliv:
            vals["push"].append(100 * f(r["pn_open"]) / f(r["pn_send"]))

    def hist(v, edges):
        counts = [0] * (len(edges) - 1)
        for x in v:
            for i in range(len(edges) - 1):
                if edges[i] <= x < edges[i + 1] or (i == len(edges) - 2 and x >= edges[i + 1]):
                    counts[i] += 1; break
        return counts

    out = {}
    for k, v in vals.items():
        v = [max(x, 0.01) for x in v]
        mean, sd, med = statistics.mean(v), statistics.pstdev(v), statistics.median(v)
        top = 4.0 if k == "email" else 8.0
        step = 0.25 if k == "email" else 0.5
        edges = [i * step for i in range(int(top / step) + 1)]
        counts = hist(v, edges)
        n = len(v)
        normal = [n * step * math.exp(-0.5 * ((e + step / 2 - mean) / sd) ** 2) / (sd * math.sqrt(2 * math.pi)) for e in edges[:-1]]
        lv = [math.log10(x) for x in v]
        lmean, lsd = statistics.mean(lv), statistics.pstdev(lv)
        ledges = [-2 + 0.25 * i for i in range(0, 15)]  # 0.01 % a 10 %
        lcounts = hist(lv, ledges)
        lnormal = [n * 0.25 * math.exp(-0.5 * ((e + 0.125 - lmean) / lsd) ** 2) / (lsd * math.sqrt(2 * math.pi)) for e in ledges[:-1]]
        p90 = sorted(v)[int(0.9 * n)]
        out[k] = {"n": n, "mean": mean, "sd": sd, "median": med, "p90": p90, "max": max(v),
                  "edges": edges, "counts": counts, "normal": normal,
                  "ledges": ledges, "lcounts": lcounts, "lnormal": lnormal, "lmean": lmean, "lsd": lsd,
                  "share_under": {s: 100 * sum(1 for x in v if x < s) / n for s in (0.5, 1.0, 1.5, 3.0)}}
    return out


# 11. Velas: apertura, máximo, mínimo y cierre de la respuesta semanal dentro de cada mes (E4a)
def velas_mes():
    W = _semanas()
    out = {}
    for c in ("email", "push notification", "whatsapp", "in-app"):
        bym = defaultdict(list)
        for p, v, resp in W[c]:
            bym[int(p[5:7]) - 1].append(resp)
        out[c] = [(bym[m][0], max(bym[m]), min(bym[m]), bym[m][-1]) if bym.get(m) else None for m in range(9)]
    return out


# 12. Semanas indexadas: volumen y respuesta de cada canal contra su promedio de enero = 100 (E4a)
def semanas_indexadas():
    W = _semanas()
    cats = [p[5:].replace("-", "/") for p, _, _ in W["email"]]
    vol, resp = [], []
    for c, name in (("email", "Email"), ("push notification", "Push"), ("whatsapp", "WhatsApp"), ("in-app", "In-app")):
        ene_v = statistics.mean([v for p, v, _ in W[c] if p[5:7] == "01"])
        ene_r = statistics.mean([r for p, _, r in W[c] if p[5:7] == "01"])
        vol.append((name, [100 * v / ene_v for _, v, _ in W[c]]))
        resp.append((name, [100 * r / ene_r for _, _, r in W[c]]))
    return {"cats": cats, "vol": vol, "resp": resp}


# 13. Cascada de usuarios según a cuántos canales respondieron (E7b)
def usuarios_cascada():
    tot = none = one = multi = 0.0
    conv = defaultdict(float); msgs = defaultdict(float)
    for r in rows("e7b_patron_respuesta.csv"):
        k = sum(int(r[c]) for c in ("resp_email", "resp_push", "resp_wa", "resp_inapp"))
        u = f(r["usuarios"]); tot += u
        kk = "none" if k == 0 else ("one" if k == 1 else "multi")
        conv[kk] += f(r["usuarios_con_conversion"])
        msgs[kk] += sum(f(r[c]) for c in ("msgs_email", "msgs_push", "msgs_wa", "msgs_inapp"))
        if k == 0: none += u
        elif k == 1: one += u
        else: multi += u
    ctot = sum(conv.values())
    return {"tot": tot, "none": none, "one": one, "multi": multi, "conv": dict(conv), "conv_tot": ctot, "msgs": dict(msgs)}


# 14. Segmentos por canal: respuesta y % de envíos (E11)
def segmentos_canal(top=9):
    agg = defaultdict(lambda: defaultdict(float))
    for r in rows("e11_segmentacion.csv"):
        for k in ("envios", "respuestas"):
            agg[(r["segment"], r["canal"])][k] += f(r[k]); agg[(r["segment"], "ALL")][k] += f(r[k])
    segs = sorted({k[0] for k in agg}, key=lambda g: -agg[(g, "ALL")]["envios"])
    segs = [g for g in segs if g not in ("BKT1", "BKT3", "Anonimos")][:top]
    tot = sum(agg[(g, "ALL")]["envios"] for g in {k[0] for k in agg})
    canales = [("email", "Email (clic)"), ("push notification", "Push (apertura)"), ("whatsapp", "WhatsApp (lectura)"), ("in-app", "In-app (clic)")]
    short = {"HardInactive_6MesesInactividad": "HardInac. 6m", "Churn_12MesesInactividad": "Churn 12m", "SoftInactive_3MesesInactividad": "SoftInac. 3m", "Precobranza": "Precobr.", "Not Tracked": "No rastr."}
    matrix = [[(100 * agg[(g, c)]["respuestas"] / agg[(g, c)]["envios"]) if agg[(g, c)]["envios"] >= 100_000 else None for g in segs] for c, _ in canales]
    env = [[agg[(g, c)]["envios"] / 1e6 for g in segs] for c, _ in canales]
    return {"cols": [short.get(g, g) for g in segs], "rows": [n for _, n in canales], "matrix": matrix, "env": env,
            "share": [100 * agg[(g, "ALL")]["envios"] / tot for g in segs]}


# 15. Envíos a usuarios que nunca respondieron, por canal y mes (E16)
def mudos_mes():
    m = defaultdict(float); mt = defaultdict(float); cost = defaultdict(float)
    for r in rows("e16_sin_respuesta.csv"):
        k = (mes_idx(r["mes"]), r["canal"])
        mt[k] += f(r["envios"])
        if r["respondio_alguna_vez"] == "0":
            m[k] += f(r["envios"]); cost[k] += f(r["costo_mxn"])
    out = {"cats": MESES, "share": [], "vol": [], "costo": {}}
    for c, name in (("email", "Email"), ("push notification", "Push"), ("whatsapp", "WhatsApp")):
        out["share"].append((name, [100 * m[(i, c)] / max(1, mt[(i, c)]) for i in range(9)]))
        out["vol"].append((name, [m[(i, c)] / 1e6 for i in range(9)]))
        out["costo"][name] = sum(cost[(i, c)] for i in range(9)) / 1e6
    return out


# 16. Solape: usuarios por banda de campañas distintas el mismo día, por mes (E6a)
def solape_usuarios():
    bands = ["2", "3 a 4", "5 a 7", "8+"]
    d = defaultdict(dict)
    for r in rows("e6a_solape_dia_mes.csv"):
        d[r["banda_familias_dia"]][mes_idx(r["mes"])] = (f(r["usuarios_aprox"]), f(r["msgs"]))
    usuarios = [(b + (" campañas" if b != "8+" else " campañas"), [d[b][m][0] / 1e6 for m in range(9)]) for b in bands]
    tres = [sum(d[b][m][0] for b in bands[1:]) / 1e6 for m in range(9)]
    msgs8 = [d["8+"][m][1] / 1e6 for m in range(9)]
    return {"cats": MESES, "usuarios": usuarios, "tres_o_mas": tres, "msgs_8": msgs8, "u8": [d["8+"][m][0] / 1e3 for m in range(9)]}


# 17. Pares de familias que más chocan el mismo día (E6b)
def pares_choque(top=6):
    TR = ("CR", "Payment Received", "KCash", "Transaccional", "Domic", "KCash Rechazo transaccional FraudRisk", "B2C")
    out, tot, same, by_team = [], 0.0, 0.0, defaultdict(float)
    for r in rows("e6b_pares_familias.csv"):
        ud = f(r["usuario_dias_juntas"]); tot += ud
        a, b = r["equipo_a"].strip(), r["equipo_b"].strip()
        if a == b:
            same += ud
        by_team[tuple(sorted((team_of(a) if a not in TR else "Transaccional", team_of(b) if b not in TR else "Transaccional")))] += ud
        out.append({"ud": ud, "usuarios": f(r["usuarios_aprox"]), "meses": int(f(r["meses"])), "a": a, "b": b, "fa": r["familia_a"], "fb": r["familia_b"],
                    "ca": r["canal_a"], "cb": r["canal_b"], "promo": a not in TR and b not in TR})
    out.sort(key=lambda q: -q["ud"])
    promo, seen = [], set()
    for q in out:
        key = (q["fa"].split("-20")[0] + q["fa"].split("-")[-2] if "-" in q["fa"] else q["fa"], q["fb"].split("-20")[0] + q["fb"].split("-")[-2] if "-" in q["fb"] else q["fb"])
        if q["promo"] and q["usuarios"] >= 300_000 and key not in seen:
            seen.add(key); promo.append(q)
        if len(promo) >= top:
            break
    return {"top": promo, "tot": tot, "same_share": 100 * same / tot, "by_team": sorted(by_team.items(), key=lambda kv: -kv[1])}

# ---- Bloque 3: culpables (qué pieza, de qué equipo, cuándo, a cuántos) -----------
def _fam(name):
    """Familia: nombre de la pieza sin la fecha y sin el prefijo de canal del nombre."""
    n = re.sub(r"-\d{8}-", "-", name)
    return re.sub(r"-(Push|CANVAS|E|IA)-Portfolio_", "-Portfolio_", n)


def semanas_indexadas_canal():
    """Por canal: índice semanal de volumen y de respuesta contra el promedio de enero (=100)."""
    W = _semanas()
    cats = [p[5:].replace("-", "/") for p, _, _ in W["email"]]
    out = []
    for c, name in (("email", "Email"), ("push notification", "Push"), ("whatsapp", "WhatsApp"), ("in-app", "In-app")):
        ene_v = statistics.mean([v for p, v, _ in W[c] if p[5:7] == "01"])
        ene_r = statistics.mean([r for p, _, r in W[c] if p[5:7] == "01"])
        vol = [100 * v / ene_v for _, v, _ in W[c]]
        resp = [100 * r / ene_r for _, _, r in W[c]]
        out.append({"title": name, "vol": vol, "resp": resp, "vmax": max(vol), "vmax_i": vol.index(max(vol)), "rmin": min(resp), "rmin_i": resp.index(min(resp))})
    return {"cats": cats, "cells": out}


def culpables_push_junio(top=8):
    """Push de junio: piezas que no existían en mayo, agrupadas por familia (E1)."""
    R = rows("e1_comunicacion_mes_canal.csv")
    jun, may = defaultdict(lambda: [0.0, 0.0, 0.0, 0]), defaultdict(float)
    tot = defaultdict(float); top_ = defaultdict(float)
    for r in R:
        if r["canal"] != "push notification":
            continue
        m = mes_idx(r["mes"]) + 1
        tot[m] += f(r["pn_send"]); top_[m] += f(r["pn_open"])
        k = (r["communication_name"], r["team"])
        if m == 6:
            v = jun[k]; v[0] += f(r["pn_send"]); v[1] += f(r["pn_open"]); v[2] += f(r["usuarios_aprox"]); v[3] += 1
        if m == 5:
            may[k] += f(r["pn_send"])
    new = {k: v for k, v in jun.items() if may.get(k, 0) == 0}
    old = {k: v for k, v in jun.items() if may.get(k, 0) > 0}
    fam = defaultdict(lambda: [0.0, 0.0, 0.0, 0, None])
    for (n, t), v in new.items():
        q = fam[(_fam(n), team_of(t))]
        q[0] += v[0]; q[1] += v[1]; q[2] = max(q[2], v[2]); q[3] += 1; q[4] = n
    lst = sorted(fam.items(), key=lambda kv: -kv[1][0])[:top]
    sum_ = lambda d: sum(v[0] for v in d.values())
    by_team = defaultdict(float)
    for (n, t), v in new.items():
        by_team[team_of(t)] += v[0]
    return {"top": [{"fam": k[0], "team": k[1], "env": v[0], "open": 100 * v[1] / v[0], "users": v[2], "piezas": v[3]} for k, v in lst],
            "new_env": sum_(new), "new_open": 100 * sum(v[1] for v in new.values()) / sum_(new), "new_n": len(new),
            "old_env": sum_(old), "old_open": 100 * sum(v[1] for v in old.values()) / sum_(old),
            "jun": tot[6], "may": tot[5], "open_mes": {m: 100 * top_[m] / tot[m] for m in tot}, "by_team": dict(by_team)}


def _aud_grupo(name):
    p = name.split("-")
    a = p[5] if len(p) > 5 else ""
    if "Rezagad" in a:
        return "Leads rezagados"
    if "Churn" in a or "Inactiv" in a or "Dormant" in a:
        return "Churn e inactivos"
    if "Lead" in a:
        return "Leads"
    if "Recurrent" in a or "Active" in a:
        return "Recurrentes y activos"
    return "Otros"


def culpables_whatsapp(top=8):
    """WhatsApp julio a septiembre: piezas con más entregas y su lectura, contra enero a junio (E1)."""
    R = rows("e1_comunicacion_mes_canal.csv")
    pc = defaultdict(lambda: [0.0, 0.0, 0.0, set()])
    grp = {h: defaultdict(lambda: [0.0, 0.0]) for h in ("H1", "H2")}
    team = defaultdict(lambda: [0.0, 0.0])
    tot = {h: [0.0, 0.0] for h in ("H1", "H2")}
    for r in R:
        if r["canal"] != "whatsapp":
            continue
        m = mes_idx(r["mes"]) + 1
        h = "H1" if m <= 6 else "H2"
        d, rd = f(r["whatsapp_delivery"]), f(r["whatsapp_read"])
        tot[h][0] += d; tot[h][1] += rd
        g = grp[h][_aud_grupo(r["communication_name"])]; g[0] += d; g[1] += rd
        t = team[team_of(r["team"])]; t[0] += d; t[1] += rd
        if h == "H2":
            k = (_fam(r["communication_name"]), team_of(r["team"]), _aud_grupo(r["communication_name"]))
            v = pc[k]; v[0] += d; v[1] += rd; v[2] = max(v[2], f(r["usuarios_aprox"])); v[3].add(MESES[m - 1])
    lst = sorted(pc.items(), key=lambda kv: -kv[1][0])[:top]
    return {"top": [{"fam": k[0], "team": k[1], "deliv": v[0], "read": 100 * v[1] / v[0], "users": v[2], "meses": ", ".join(sorted(v[3], key=MESES.index)), "grupo": k[2]} for k, v in lst],
            "tot": {h: {"deliv": v[0], "read": 100 * v[1] / v[0]} for h, v in tot.items()},
            "grupos": {h: {g: {"deliv": v[0], "read": 100 * v[1] / v[0], "share": 100 * v[0] / tot[h][0]} for g, v in grp[h].items()} for h in grp},
            "team": {t: {"deliv": v[0], "read": 100 * v[1] / v[0]} for t, v in team.items()}}


def culpables_bajas(top=8):
    """Bajas de email por pieza: solo meses con entrega de esa pieza (E1)."""
    R = rows("e1_comunicacion_mes_canal.csv")
    pc = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0, set()])
    tu = td = anom = 0.0
    by_team = defaultdict(float); aud = defaultdict(lambda: [0.0, 0.0])
    for r in R:
        if r["canal"] != "email":
            continue
        u, d = f(r["email_unsubscribe"]), f(r["email_delivery"])
        if d == 0:
            anom += u
            continue
        tu += u; td += d; by_team[team_of(r["team"])] += u
        k = (_fam(r["communication_name"]), team_of(r["team"]))
        v = pc[k]; v[0] += u; v[1] += d; v[2] += f(r["email_click"]); v[3] = max(v[3], f(r["usuarios_aprox"])); v[4].add(MESES[mes_idx(r["mes"])])
        a = _aud_grupo(r["communication_name"]); a = "Todos" if "-Todos" in r["communication_name"] else a
        aud[a][0] += d; aud[a][1] += u
    lst = sorted([kv for kv in pc.items() if kv[1][1] >= 100_000], key=lambda kv: -kv[1][0])[:top]
    cum = 0.0; out = []
    for k, v in lst:
        cum += v[0]
        out.append({"fam": k[0], "team": k[1], "bajas": v[0], "deliv": v[1], "por_mil": 1000 * v[0] / v[1], "clic": 100 * v[2] / v[1], "users": v[3], "meses": ", ".join(sorted(v[4], key=MESES.index)), "cum": 100 * cum / tu})
    return {"top": out, "tot": tu, "anom": anom, "por_mil": 1000 * tu / td, "by_team": {t: 100 * v / tu for t, v in by_team.items()},
            "aud": {a: {"deliv": v[0], "por_mil": 1000 * v[1] / v[0], "share": 100 * v[1] / tu} for a, v in aud.items()}}


if __name__ == "__main__":
    import json
    sp = scatter_piezas()
    print("scatter", {k: len(v) for k, v in sp.items()})
    for k in sp:
        top = sorted(sp[k], key=lambda p: -p["x"])[:3]
        print(k, [(round(p["x"] / 1e6, 1), round(p["y"], 2), p["g"], p["name"][:40]) for p in top])
    cm = canales_mes()
    for c, d in cm.items():
        print(c, [round(v, 1) for v in d["vol"]], [round(v, 2) for v in d["resp"]])
    for canal in ("email", "push notification"):
        print(canal)
        for e in dispersion_equipo(canal):
            print("  ", e["cat"], e["n"], round(e["mean"], 2), round(e["sd"], 2), round(e["median"], 2), round(e["wmean"], 2))
    h = heat_dia()
    print(h["rows"]); print([round(v, 1) for v in h["share"]])
    for r, m in zip(h["rows"], h["matrix"]):
        print(r, [None if v is None else round(v, 2) for v in m])
    print(json.dumps({k: (v if k == "cats" else [(n, [round(x, 2) for x in vals]) for n, vals in v]) for k, v in bandas_mes().items()}))
    a = antiguedad()
    print({k: [round(x, 2) for x in v] if k != "cats" else v for k, v in a.items()})
    s = solape_mes()
    for b, v in s["resp"]: print("resp", b, [round(x, 1) for x in v])
    for b, v in s["baja"]: print("baja", b, [round(x, 2) for x in v])


# ---- Bloque 4: quién insiste, entrega por equipo, gancho por canal, versiones, scorecard ----
MINIMOS = {"email": 0.3, "push notification": 0.75, "whatsapp": 60.0, "in-app": 10.0}


def _resp_cols(c):
    return {"email": ("email_delivery", "email_click"), "push notification": ("pn_send", "pn_open"),
            "whatsapp": ("whatsapp_delivery", "whatsapp_read"), "in-app": ("in_app_impression", "in_app_click")}[c]


def _fam_mes(min_base=50_000):
    """Familia x canal x mes: base, respuestas, envíos, costo, equipo (E1)."""
    agg = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])
    team = {}
    for r in rows("e1_comunicacion_mes_canal.csv"):
        c = r["canal"]
        if c not in _resp_cols.__code__.co_consts and c not in ("email", "push notification", "whatsapp", "in-app"):
            continue
        if c == "banner":
            continue
        b, rr = _resp_cols(c)
        k = (_fam(r["communication_name"]), c)
        v = agg[k]
        v[0] += f(r[b]); v[1] += f(r[rr]); v[2] += f(r["envios"]); v[3] += f(r["costo_mxn"])
        team[k] = team_of(r["team"])
    return agg, team


def insisten():
    """Por equipo: volumen enviado en meses posteriores a que una familia ya estaba debajo del mínimo del canal."""
    per = defaultdict(lambda: defaultdict(lambda: [0.0, 0.0, 0.0, 0.0]))  # (fam, canal) -> mes -> base, resp, env, costo
    team = {}
    for r in rows("e1_comunicacion_mes_canal.csv"):
        c = r["canal"]
        if c not in MINIMOS:
            continue
        b, rr = _resp_cols(c)
        k = (_fam(r["communication_name"]), c)
        m = mes_idx(r["mes"])
        v = per[k][m]
        v[0] += f(r[b]); v[1] += f(r[rr]); v[2] += f(r["envios"]); v[3] += f(r["costo_mxn"])
        team[k] = team_of(r["team"])
    out = {t: {"env_tot": 0.0, "env_insiste": 0.0, "costo_insiste": 0.0, "fams": set(), "meses": 0} for t in TEAMS}
    ejemplos = []
    for k, months in per.items():
        t = team[k]
        bad = False
        ins_env, ins_cost, ins_m = 0.0, 0.0, 0
        for m in sorted(months):
            base, resp, env, cost = months[m]
            out[t]["env_tot"] += env
            if bad and base >= 20_000:
                ins_env += env; ins_cost += cost; ins_m += 1
            if base >= 50_000 and 100 * resp / base < MINIMOS[k[1]]:
                bad = True
        if ins_env > 0:
            out[t]["env_insiste"] += ins_env; out[t]["costo_insiste"] += ins_cost; out[t]["fams"].add(k); out[t]["meses"] += ins_m
            ejemplos.append({"fam": k[0], "canal": k[1], "team": t, "env": ins_env, "meses": ins_m, "costo": ins_cost})
    ejemplos.sort(key=lambda q: -q["env"])
    res = {}
    for t, v in out.items():
        res[t] = {"env_tot": v["env_tot"], "env_insiste": v["env_insiste"], "share": 100 * v["env_insiste"] / v["env_tot"] if v["env_tot"] else 0,
                  "costo": v["costo_insiste"], "n_fam": len(v["fams"])}
    tot_env = sum(v["env_tot"] for v in out.values()); tot_ins = sum(v["env_insiste"] for v in out.values())
    return {"team": res, "tot_share": 100 * tot_ins / tot_env, "tot_env": tot_ins, "tot_costo": sum(v["costo_insiste"] for v in out.values()), "ejemplos": ejemplos[:8]}


def entrega_equipo():
    """Por equipo: enviados, entregados y no entregados en email y WhatsApp (E1)."""
    agg = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])
    for r in rows("e1_comunicacion_mes_canal.csv"):
        t = team_of(r["team"])
        v = agg[t]
        v[0] += f(r["email_sent"]); v[1] += f(r["email_delivery"]); v[2] += f(r["whatsapp_send"]); v[3] += f(r["whatsapp_delivery"])
    return {t: {"email_sent": v[0], "email_del": v[1], "email_pct": 100 * v[1] / v[0] if v[0] else 0,
                "wa_sent": v[2], "wa_del": v[3], "wa_pct": 100 * v[3] / v[2] if v[2] else 0} for t, v in agg.items()}


_GANCHOS = [
    ("Recordatorio de algo empezado", r"retarget|recordator|reminder|abandon|incomplet|pending|pendiente|veriff|personalinfo|carrito|end.?to.?end"),
    ("Cobranza y pagos", r"cobranza|precobranza|bkt|mora|pago|payment|collection|vencid"),
    ("Bienvenida y activación", r"bienvenid|welcome|onboard|neveractive|activaci|primer"),
    ("Tasa 0", r"tasa.?0|tasa0|sinintereses|0%"),
    ("Descuento, cupón u oferta", r"descuent|cupon|cuponera|oferta|promo|discount|rescate|comercio|merchant|cashback|topup|billpay"),
    ("Referidos", r"referral|referid"),
    ("Lanzamiento y novedades", r"lanzamiento|launch|intro|novedad|new|nuevo|mundial|anotaygana|dia.?del|newsletter|weekly"),
]


def gancho_of(name):
    n = name.lower()
    for g, pat in _GANCHOS:
        if re.search(pat, n):
            return g
    return "Otro"


def gancho_canal(min_base=200_000):
    """Respuesta por gancho y canal, con volumen (E1)."""
    agg = defaultdict(lambda: [0.0, 0.0, 0.0])
    for r in rows("e1_comunicacion_mes_canal.csv"):
        c = r["canal"]
        if c not in MINIMOS:
            continue
        b, rr = _resp_cols(c)
        v = agg[(gancho_of(r["communication_name"]), c)]
        v[0] += f(r[b]); v[1] += f(r[rr]); v[2] += f(r["envios"])
    ganchos = [g for g, _ in _GANCHOS] + ["Otro"]
    canales = ["email", "push notification", "in-app", "whatsapp"]
    out = {"rows": ganchos, "cols": ["Email (clic)", "Push (apertura)", "In-app (clic)", "WhatsApp (lectura)"], "matrix": [], "share": []}
    tot = sum(v[2] for v in agg.values())
    for g in ganchos:
        row = []
        for c in canales:
            v = agg.get((g, c))
            row.append(None if (not v or v[0] < min_base) else 100 * v[1] / v[0])
        out["matrix"].append(row)
        out["share"].append(100 * sum(agg.get((g, c), [0, 0, 0])[2] for c in canales) / tot)
    return out


def versiones():
    """Familias con más versiones (comunicaciones distintas) y su respuesta; repetición de segmentos (E1, E11)."""
    fams = defaultdict(lambda: {"ids": set(), "env": 0.0, "base": 0.0, "resp": 0.0, "team": None, "canal": None})
    for r in rows("e1_comunicacion_mes_canal.csv"):
        c = r["canal"]
        if c not in MINIMOS:
            continue
        b, rr = _resp_cols(c)
        k = (_fam(r["communication_name"]), c)
        v = fams[k]
        v["ids"].add(r["communication_id"]); v["env"] += f(r["envios"]); v["base"] += f(r[b]); v["resp"] += f(r[rr]); v["team"] = team_of(r["team"]); v["canal"] = c
    lst = [{"fam": k[0], "canal": k[1], "team": v["team"], "n": len(v["ids"]), "env": v["env"], "resp": 100 * v["resp"] / v["base"] if v["base"] else 0} for k, v in fams.items()]
    lst.sort(key=lambda q: -q["n"])
    n_multi = sum(1 for q in lst if q["n"] >= 5)
    env_multi = sum(q["env"] for q in lst if q["n"] >= 5)
    # segmentos: valores distintos de segment/subsegment que son variantes del mismo nombre
    segs = defaultdict(set)
    for r in rows("e11_segmentacion.csv"):
        for col in ("segment", "subsegment"):
            s = r[col]
            base = re.sub(r"[^a-z]", "", s.lower())
            base = re.sub(r"(20\d\d|ene|feb|mar|abr|may|jun|jul|ago|sep|enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre)$", "", base)
            if base:
                segs[base].add(s)
    dup = sorted(((k, len(v)) for k, v in segs.items() if len(v) >= 3), key=lambda q: -q[1])
    return {"top": lst[:10], "n_multi": n_multi, "env_multi": env_multi, "tot_env": sum(q["env"] for q in lst), "dup_segs": dup[:8], "n_dup_values": sum(n for _, n in dup)}


def scorecard():
    """Por equipo: clic email, apertura push, lectura WA, bajas por mil, entrega WA, % volumen que insiste."""
    agg = defaultdict(lambda: defaultdict(float))
    for r in rows("e1_comunicacion_mes_canal.csv"):
        t = team_of(r["team"])
        a = agg[t]
        for col in ("email_delivery", "email_click", "email_unsubscribe", "pn_send", "pn_open", "whatsapp_send", "whatsapp_delivery", "whatsapp_read", "in_app_impression", "in_app_click", "envios", "costo_mxn"):
            a[col] += f(r[col])
    ins = insisten()["team"]
    out = {}
    for t in TEAMS:
        a = agg[t]
        out[t] = {
            "email": 100 * a["email_click"] / a["email_delivery"] if a["email_delivery"] else None,
            "push": 100 * a["pn_open"] / a["pn_send"] if a["pn_send"] else None,
            "wa": 100 * a["whatsapp_read"] / a["whatsapp_delivery"] if a["whatsapp_delivery"] > 100_000 else None,
            "inapp": 100 * a["in_app_click"] / a["in_app_impression"] if a["in_app_impression"] > 100_000 else None,
            "bajas": 1000 * a["email_unsubscribe"] / a["email_delivery"] if a["email_delivery"] else None,
            "wa_del": 100 * a["whatsapp_delivery"] / a["whatsapp_send"] if a["whatsapp_send"] > 100_000 else None,
            "insiste": ins[t]["share"],
            "envios": a["envios"], "costo": a["costo_mxn"],
        }
    return out


def canal_equipo():
    """Envíos (M) y costo variable (M MXN) por canal y equipo (E1)."""
    env = defaultdict(float); cost = defaultdict(float)
    for r in rows("e1_comunicacion_mes_canal.csv"):
        c = r["canal"]
        if c not in MINIMOS:
            continue
        t = team_of(r["team"])
        env[(c, t)] += f(r["envios"])
        cost[(c, t)] += 0.05 * f(r["email_sent"]) + 1.0 * f(r["whatsapp_delivery"])
    canales = [("email", "Email"), ("push notification", "Push"), ("whatsapp", "WhatsApp"), ("in-app", "In-app")]
    return {"cats": [n for _, n in canales], "teams": TEAMS,
            "env": [[env[(c, t)] / 1e6 for t in TEAMS] for c, _ in canales],
            "cost": [[cost[(c, t)] / 1e6 for t in TEAMS] for c, _ in canales]}


# ---- Bloque 5: datos para gráficas multivariable (deck v6) ---------------------
def _short_fam(name, n=30):
    toks = [q for q in re.split(r"[-]", name) if q and q.upper() not in ("N/A", "NA", "CANVAS", "E", "FULL_ROLLOUT", "MAIL", "PUSH", "IA")
            and not re.fullmatch(r"\d{6,8}|[A-Z]\d{3,5}", q)]
    s = " ".join(toks[2:]) if len(toks) > 2 else " ".join(toks)
    return s.replace("_", " ")[:n]


def patron_matrix():
    """Canal al que responde el usuario (filas) contra mensajes recibidos por canal (columnas), en M (E7b)."""
    R = rows("e7b_patron_respuesta.csv")
    groups = ["Ninguno", "Solo WhatsApp", "Solo in-app", "Solo email", "Solo push", "Dos o más canales"]
    cols = ["Email", "Push", "WhatsApp entregado", "In-app"]
    agg = {g: [0.0] * 5 for g in groups}
    resp = {"Ninguno": set(), "Solo WhatsApp": {"WhatsApp entregado"}, "Solo in-app": {"In-app"}, "Solo email": {"Email"}, "Solo push": {"Push"}, "Dos o más canales": set(cols)}
    for r in R:
        flags = (int(r["resp_email"]), int(r["resp_push"]), int(r["resp_wa"]), int(r["resp_inapp"]))
        n = sum(flags)
        if n == 0:
            g = "Ninguno"
        elif n >= 2:
            g = "Dos o más canales"
        else:
            g = ["Solo email", "Solo push", "Solo WhatsApp", "Solo in-app"][flags.index(1)]
        v = agg[g]
        v[0] += f(r["msgs_email"]); v[1] += f(r["msgs_push"]); v[2] += f(r["msgs_wa_entregados"]); v[3] += f(r["msgs_inapp"]); v[4] += f(r["usuarios"])
    tu = sum(v[4] for v in agg.values())
    M = [[agg[g][j] / 1e6 for j in range(4)] for g in groups]
    tint = [[("mix" if g == "Dos o más canales" else ("ok" if c in resp[g] else "bad")) for c in cols] for g in groups]
    mute = cost_mute = 0.0
    for r in R:
        fl = (int(r["resp_email"]), int(r["resp_push"]), int(r["resp_wa"]), int(r["resp_inapp"]))
        ms = (f(r["msgs_email"]), f(r["msgs_push"]), f(r["msgs_wa_entregados"]), f(r["msgs_inapp"]))
        mute += sum(m for fg, m in zip(fl, ms) if not fg)
        cost_mute += (0.05 * ms[0] if not fl[0] else 0) + (1.0 * ms[2] if not fl[2] else 0)
    tot = sum(agg[g][j] for g in groups for j in range(4))
    return {"rows": groups, "cols": cols, "matrix": M, "tint": tint, "row_share": [100 * agg[g][4] / tu for g in groups],
            "mute": mute / 1e6, "mute_share": 100 * mute / tot, "cost_mute": cost_mute / 1e6}


def mudos_mes_canal():
    """Envíos por mes y canal a usuarios que nunca respondieron, y costo acumulado (E16)."""
    env = defaultdict(float); cost = defaultdict(float)
    for r in rows("e16_sin_respuesta.csv"):
        if r["respondio_alguna_vez"] != "0" or r["canal"] == "banner":
            continue
        m = mes_idx(r["mes"])
        env[(r["canal"], m)] += f(r["envios"]); cost[m] += f(r["costo_mxn"])
    canales = [("email", "Email"), ("push notification", "Push"), ("whatsapp", "WhatsApp"), ("in-app", "In-app")]
    series = [(n, [env[(c, m)] / 1e6 for m in range(9)]) for c, n in canales]
    cum, acc = [], 0.0
    for m in range(9):
        acc += cost[m]; cum.append(acc / 1e6)
    return {"cats": MESES, "series": series, "cum_cost": cum, "tot": sum(env.values()) / 1e6}


def bloqueados_familias(min_bloq=40_000):
    """Por familia: envíos totales, envíos a etapas bloqueadas y su porcentaje (E7a)."""
    BL = ("4.Kpay CC Freeze", "6.Reus or Arco", "3.Blacklist")
    agg = defaultdict(lambda: [0.0, 0.0, None])
    for r in rows("e7a_familia_canal_etapa.csv"):
        k = r["familia"]
        v = agg[k]
        e = f(r["envios"])
        v[0] += e
        if r["etapa"] in BL:
            v[1] += e
        v[2] = team_of(r["equipo"])
    def promo(k, t):
        return t in ("Marketing", "Sales", "Product Growth") or (t == "Others" and re.search(r"-[BTS]\d{3,5}-", k) and "Compliance" not in k)
    pts = []
    for k, v in agg.items():
        if v[1] >= min_bloq and v[0] > 0 and promo(k, v[2]):
            pts.append({"x": v[0], "y": 100 * v[1] / v[0], "size": v[1], "g": v[2], "name": k, "label": _short_fam(k)})
    pts.sort(key=lambda p: -p["size"])
    by_team = defaultdict(float)
    for k, v in agg.items():
        if promo(k, v[2]):
            by_team[v[2]] += v[1]
    return {"pts": pts, "tot": sum(by_team.values()) / 1e6, "by_team": {t: v / 1e6 for t, v in by_team.items()}}


def entrega_equipo_mes(min_sent=50_000):
    """Entrega (%) de email y WhatsApp por equipo y mes (E1)."""
    agg = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])
    for r in rows("e1_comunicacion_mes_canal.csv"):
        v = agg[(team_of(r["team"]), mes_idx(r["mes"]))]
        v[0] += f(r["email_sent"]); v[1] += f(r["email_delivery"]); v[2] += f(r["whatsapp_send"]); v[3] += f(r["whatsapp_delivery"])
    out = {"email": [], "wa": []}
    for t in TEAMS:
        em = [100 * agg[(t, m)][1] / agg[(t, m)][0] if agg[(t, m)][0] >= min_sent else None for m in range(9)]
        wa = [100 * agg[(t, m)][3] / agg[(t, m)][2] if agg[(t, m)][2] >= min_sent else None for m in range(9)]
        if any(v is not None for v in em):
            out["email"].append((t, em))
        if any(v is not None for v in wa):
            out["wa"].append((t, wa))
    return out


def lorenz():
    """Curva de concentración: % acumulado de usuarios (de más a menos mensajes) contra % de mensajes, bajas y conversiones (E3)."""
    order = ["321+", "161-320", "081-160", "41-80", "21-40", "11-20", "06-10", "01-05"]
    labels = {"321+": "321 o más", "161-320": "161 a 320", "081-160": "81 a 160", "41-80": "41 a 80", "21-40": "21 a 40", "11-20": "11 a 20", "06-10": "6 a 10", "01-05": "1 a 5"}
    d = defaultdict(lambda: [0.0] * 4)
    for r in rows("e3_usuarios_distribucion.csv"):
        b = r["banda_msgs"]
        if b in order:
            v = d[b]; v[0] += f(r["usuarios"]); v[1] += f(r["msgs"]); v[2] += f(r["bajas_email"]); v[3] += f(r["usuarios_con_conversion"])
    tot = [sum(d[b][i] for b in order) for i in range(4)]
    pts, acc = [{"x": 0, "y": [0, 0, 0], "lab": ""}], [0.0] * 4
    for b in order:
        for i in range(4):
            acc[i] += d[b][i]
        pts.append({"x": 100 * acc[0] / tot[0], "y": [100 * acc[1] / tot[1], 100 * acc[2] / tot[2], 100 * acc[3] / tot[3]], "lab": labels[b], "users": d[b][0], "msgs": d[b][1]})
    return {"pts": pts, "series": ["Mensajes", "Bajas de email", "Usuarios que convirtieron"]}


def bajas_dias():
    """Bajas de nuevos: distribución acumulada por días desde el alta y por emails recibidos; familias del día de la baja (E8)."""
    dd = defaultdict(float); de = defaultdict(float); fam = defaultdict(lambda: [0.0, 0.0])
    for r in rows("e8_dias_hasta_baja.csv"):
        u = f(r["usuarios"])
        if r["cohorte_limpia"] != "1":
            continue
        if r["bloque"] == "banda_dias":
            dd[r["clave"]] += u
        elif r["bloque"] == "banda_emails":
            de[r["clave"]] += u
        elif r["bloque"] == "familia_dia_baja":
            v = fam[r["clave"]]; v[0] += u; v[1] += u * f(r["dias_mediana"])
    od = ["0 mismo día", "1 a 7", "08 a 30", "31 a 90", "91 a 180", "181+"]
    oe = ["01", "02 a 3", "04 a 10", "11 a 30", "31+"]
    td, te = sum(dd.values()), sum(de.values())
    cum_d, acc = [], 0.0
    for b in od:
        acc += dd[b]; cum_d.append(100 * acc / td)
    cum_e, acc = [], 0.0
    for b in oe:
        acc += de[b]; cum_e.append(100 * acc / te)
    fams = sorted(fam.items(), key=lambda kv: -kv[1][0])[:10]
    pts = [{"x": v[1] / v[0], "y": v[0] / 1e3, "g": team_of(k.split("-")[0]), "name": k, "label": _short_fam(k, 26)} for k, v in fams]
    return {"dias": {"cats": ["Mismo día", "1 a 7", "8 a 30", "31 a 90", "91 a 180", "181 o más"], "cum": cum_d},
            "emails": {"cats": ["1", "2 a 3", "4 a 10", "11 a 30", "31 o más"], "cum": cum_e},
            "fams": pts, "tot": td}


def bajas_familias(min_deliv=300_000):
    """Por familia de email: entregados, bajas por mil y bajas totales (E1)."""
    pc = defaultdict(lambda: [0.0, 0.0, None])
    for r in rows("e1_comunicacion_mes_canal.csv"):
        if r["canal"] != "email":
            continue
        d = f(r["email_delivery"])
        if d == 0:
            continue
        v = pc[_fam(r["communication_name"])]
        v[0] += d; v[1] += f(r["email_unsubscribe"]); v[2] = team_of(r["team"])
    pts = [{"x": v[0], "y": 1000 * v[1] / v[0], "size": v[1], "g": v[2], "name": k, "label": _short_fam(k)} for k, v in pc.items() if v[0] >= min_deliv]
    pts.sort(key=lambda p: -p["size"])
    tot = sum(v[1] for v in pc.values())
    return {"pts": pts, "tot": tot, "top8_share": 100 * sum(p["size"] for p in pts[:8]) / tot}


def pasos_canvas(top=7, min_steps=6):
    """Canvas largos: % de usuarios que llega a cada paso y apertura del paso (E15)."""
    cv = defaultdict(lambda: defaultdict(lambda: [0.0, 0.0]))
    meta = {}
    for r in rows("e15_embudo_pasos.csv"):
        n = r["canvas_name"]
        if n in ("", "null"):
            continue
        o = int(f(r["orden_aprox"]))
        v = cv[n][o]; v[0] = max(v[0], f(r["usuarios"])); v[1] += f(r["usuarios_abrieron"])
        meta[n] = team_of(r["team"])
    lines = []
    for n, steps in cv.items():
        if len(steps) < min_steps:
            continue
        ords = sorted(steps)
        u1 = max(steps[o][0] for o in ords)
        if u1 < 100_000:
            continue
        reach = [100 * steps[o][0] / u1 for o in ords[:12]]
        opn = [100 * min(steps[o][1], steps[o][0]) / steps[o][0] if steps[o][0] else None for o in ords[:12]]
        lines.append({"name": n, "label": _short_fam(n, 26), "team": meta[n], "u1": u1, "n_steps": len(steps), "reach": reach, "open": opn})
    lines.sort(key=lambda q: -q["u1"])
    return lines[:top]


def antiguedad_usuario():
    """Por antigüedad: push y emails por usuario en 9 meses, apertura de push y clic de email (E12)."""
    bands = ["0. menos de 1 mes", "1. 1 a 3 meses", "2. 3 a 6 meses", "3. 6 a 12 meses", "4. 1 a 2 años", "5. más de 2 años"]
    labels = ["< 1 mes", "1 a 3 m", "3 a 6 m", "6 a 12 m", "1 a 2 años", "> 2 años"]
    agg = defaultdict(lambda: [0.0, 0.0, 0.0])
    for r in rows("e12_antiguedad.csv"):
        b = r["banda_antiguedad"]
        if b not in bands or r["canal"] not in ("email", "push notification"):
            continue
        v = agg[(b, r["canal"])]; v[0] += f(r["envios"]); v[1] += f(r["usuarios_aprox"]); v[2] += f(r["respuestas"])
    out = {"labels": labels, "push": [], "email": []}
    for b, l in zip(bands, labels):
        p = agg[(b, "push notification")]; e = agg[(b, "email")]
        out["push"].append({"lab": l, "x": p[0] / max(1, p[1]), "y": 100 * p[2] / max(1, p[0])})
        out["email"].append({"lab": l, "x": e[0] / max(1, e[1]), "y": 100 * e[2] / max(1, e[0])})
    return out


def gancho_strip(min_deliv=200_000):
    """Por gancho: cada familia de email como un punto (clic, entregados) y el promedio ponderado del gancho (E1)."""
    pc = defaultdict(lambda: [0.0, 0.0, None])
    for r in rows("e1_comunicacion_mes_canal.csv"):
        if r["canal"] != "email":
            continue
        v = pc[_fam(r["communication_name"])]
        v[0] += f(r["email_delivery"]); v[1] += f(r["email_click"]); v[2] = team_of(r["team"])
    ganchos = [g for g, _ in _GANCHOS] + ["Otro"]
    rows_ = []
    for g in ganchos:
        pts = [{"x": 100 * v[1] / v[0], "size": v[0], "g": v[2], "name": k, "label": _short_fam(k, 22)} for k, v in pc.items() if v[0] >= min_deliv and gancho_of(k) == g]
        if len(pts) < 2:
            continue
        tot = sum(p["size"] for p in pts); wm = sum(p["x"] * p["size"] for p in pts) / tot
        rows_.append({"gancho": g, "pts": pts, "wmean": wm, "vol": tot, "n": len(pts)})
    rows_.sort(key=lambda q: -q["wmean"])
    return rows_


def tamano_toques(min_deliv=200_000):
    """Por familia de email: tamaño de audiencia por envío, toques por usuario y clic (E1)."""
    pc = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0, 0, None])
    for r in rows("e1_comunicacion_mes_canal.csv"):
        if r["canal"] != "email" or f(r["envios"]) <= 0:
            continue
        v = pc[_fam(r["communication_name"])]
        v[0] += f(r["email_delivery"]); v[1] += f(r["email_click"]); v[2] += f(r["envios"]); v[3] += f(r["usuarios_aprox"]); v[4] += 1; v[5] = team_of(r["team"])
    pts = []
    for k, v in pc.items():
        if v[0] < min_deliv or v[3] <= 0:
            continue
        toques = v[2] / v[3]
        band = "1 toque" if toques < 1.5 else ("2 toques" if toques < 2.5 else "3 o más toques")
        pts.append({"x": v[3] / v[4], "y": 100 * v[1] / v[0], "g": band, "size": v[0], "name": k, "label": _short_fam(k, 22), "toques": toques})
    return pts


def insisten_familias(top=6):
    """Familias que siguieron enviando después de caer debajo del mínimo: respuesta y envíos por mes (E1)."""
    per = defaultdict(lambda: defaultdict(lambda: [0.0, 0.0, 0.0]))
    team = {}
    for r in rows("e1_comunicacion_mes_canal.csv"):
        c = r["canal"]
        if c not in MINIMOS:
            continue
        b, rr = _resp_cols(c)
        k = (_fam(r["communication_name"]), c)
        v = per[k][mes_idx(r["mes"])]
        v[0] += f(r[b]); v[1] += f(r[rr]); v[2] += f(r["envios"])
        team[k] = team_of(r["team"])
    out = []
    for k, months in per.items():
        resp = [100 * months[m][1] / months[m][0] if months[m][0] >= 20_000 else None for m in range(9)]
        env = [months[m][2] / 1e6 for m in range(9)]
        fail = None; after = 0.0
        for m in range(9):
            if fail is not None:
                after += env[m]
            elif months[m][0] >= 50_000 and resp[m] is not None and resp[m] < MINIMOS[k[1]]:
                fail = m
        if fail is not None and after > 0:
            out.append({"fam": k[0], "canal": k[1], "team": team[k], "resp": resp, "env": env, "fail": fail, "after": after, "min": MINIMOS[k[1]], "label": _short_fam(k[0], 28)})
    out.sort(key=lambda q: -q["after"])
    return out[:top]


def pareto_piezas():
    """Por canal: familias ordenadas por volumen y % acumulado de volumen y de respuestas (E1)."""
    out = {}
    for c, name in (("email", "Email"), ("push notification", "Push")):
        b, rr = _resp_cols(c)
        pc = defaultdict(lambda: [0.0, 0.0])
        for r in rows("e1_comunicacion_mes_canal.csv"):
            if r["canal"] != c:
                continue
            v = pc[_fam(r["communication_name"])]; v[0] += f(r[b]); v[1] += f(r[rr])
        lst = sorted(pc.items(), key=lambda kv: -kv[1][0])
        tb, tr = sum(v[0] for _, v in lst), sum(v[1] for _, v in lst)
        cum, ab, ar = [], 0.0, 0.0
        for k, v in lst:
            ab += v[0]; ar += v[1]
            cum.append({"name": k, "label": _short_fam(k, 22), "vol": 100 * ab / tb, "resp": 100 * ar / tr, "rate": 100 * v[1] / v[0] if v[0] else 0, "base": v[0]})
        out[name] = {"pts": cum, "n": len(lst), "tot_base": tb}
    return out


def versiones_mes(top=8):
    """Familias con más versiones: cuántas comunicaciones nuevas se crearon cada mes y cuánto enviaron (E2, E1)."""
    first = {}
    for r in rows("e2_catalogo.csv"):
        fs = r["first_sent"]
        if fs and fs[:4] == "2026":
            first[r["communication_id"]] = (_fam(r["nombre"]), mes_idx(fs), team_of(r["team_limpio"]))
    cnt = defaultdict(lambda: [0] * 9); team = {}
    for cid, (fam, m, t) in first.items():
        if m < 9:
            cnt[fam][m] += 1; team[fam] = t
    env = defaultdict(lambda: [0.0] * 9)
    for r in rows("e1_comunicacion_mes_canal.csv"):
        env[_fam(r["communication_name"])][mes_idx(r["mes"])] += f(r["envios"])
    fams = sorted(cnt.items(), key=lambda kv: -sum(kv[1]))[:top]
    return {"cats": MESES, "rows": [{"fam": k, "label": _short_fam(k, 34), "team": team[k], "n": v, "env": [x / 1e6 for x in env[k]], "tot": sum(v)} for k, v in fams],
            "n_fam5": sum(1 for v in cnt.values() if sum(v) >= 5)}


def acciones_equipo():
    """Campañas activas por equipo y acción del plan (hallazgos/muestra_c_familias.csv)."""
    import csv as _csv
    p = os.path.join(os.path.dirname(DATA), "hallazgos", "muestra_c_familias.csv")
    acts = ["Apagar", "Limpiar base de WhatsApp", "Rehacer o re-segmentar", "Bajar frecuencia", "Proteger", "Escalar"]
    n = defaultdict(int); msgs = defaultdict(float)
    with open(p, newline="", encoding="utf-8") as fh:
        for r in _csv.DictReader(fh):
            if r["activo_sep"] != "1":
                continue
            t = team_of(r["team"]); a = r["accion_tipo"]
            if a in acts:
                n[(t, a)] += 1; msgs[(t, a)] += f(r["envios_mes_prom"])
    return {"cols": acts, "rows": TEAMS, "n": [[n[(t, a)] for a in acts] for t in TEAMS], "msgs": [[msgs[(t, a)] / 1e6 for a in acts] for t in TEAMS]}


def segmentos_scatter(top=12):
    """Segmentos de Braze: envíos, respuesta sobre envíos y conversiones por mil (E11)."""
    agg = defaultdict(lambda: [0.0, 0.0, 0.0, defaultdict(float)])
    for r in rows("e11_segmentacion.csv"):
        v = agg[r["segment"]]; e = f(r["envios"])
        v[0] += e; v[1] += f(r["respuestas"]); v[2] += f(r["conversiones_filas"]); v[3][team_of(r["team"])] += e
    lst = sorted(agg.items(), key=lambda kv: -kv[1][0])[:top]
    return [{"x": v[0], "y": 100 * v[1] / v[0] if v[0] else 0, "size": v[2], "g": max(v[3], key=v[3].get), "name": k, "label": k, "conv_mil": 1000 * v[2] / v[0] if v[0] else 0} for k, v in lst]


def sin_ticket_mes():
    """% de envíos sin ticket por equipo y mes (E1)."""
    SIN = ("", "null", "Other", "N/A", "T0000", "T000")
    agg = defaultdict(lambda: [0.0, 0.0])
    for r in rows("e1_comunicacion_mes_canal.csv"):
        v = agg[(team_of(r["team"]), mes_idx(r["mes"]))]; e = f(r["envios"])
        v[0] += e
        if (r["ticket_number"] or "") in SIN:
            v[1] += e
    series = []
    for t in TEAMS:
        series.append((t, [100 * agg[(t, m)][1] / agg[(t, m)][0] if agg[(t, m)][0] > 50_000 else None for m in range(9)]))
    tot = sum(v[0] for v in agg.values()); sin = sum(v[1] for v in agg.values())
    return {"cats": MESES, "series": series, "share": 100 * sin / tot, "sin": sin / 1e6}


def push_junio_scatter():
    """Push de junio: cada familia como punto (envíos, apertura); nuevas en junio contra existentes (E1)."""
    jun = defaultdict(lambda: [0.0, 0.0, None]); may = defaultdict(float)
    for r in rows("e1_comunicacion_mes_canal.csv"):
        if r["canal"] != "push notification":
            continue
        m = mes_idx(r["mes"]) + 1
        k = _fam(r["communication_name"])
        if m == 6:
            v = jun[k]; v[0] += f(r["pn_send"]); v[1] += f(r["pn_open"]); v[2] = team_of(r["team"])
        if m == 5:
            may[k] += f(r["pn_send"])
    pts = []
    for k, v in jun.items():
        if v[0] < 100_000:
            continue
        pts.append({"x": v[0], "y": 100 * v[1] / v[0], "size": v[0], "g": v[2], "name": k, "label": _short_fam(k, 24), "new": may.get(k, 0) == 0})
    pts.sort(key=lambda p: -p["x"])
    return pts


def wa_slope():
    """WhatsApp: lectura por grupo de audiencia y por equipo, enero a junio contra julio a septiembre (E1)."""
    g = defaultdict(lambda: [[0.0, 0.0], [0.0, 0.0]]); t = defaultdict(lambda: [[0.0, 0.0], [0.0, 0.0]])
    for r in rows("e1_comunicacion_mes_canal.csv"):
        if r["canal"] != "whatsapp":
            continue
        h = 0 if mes_idx(r["mes"]) < 6 else 1
        d, rd = f(r["whatsapp_delivery"]), f(r["whatsapp_read"])
        g[_aud_grupo(r["communication_name"])][h][0] += d; g[_aud_grupo(r["communication_name"])][h][1] += rd
        t[team_of(r["team"])][h][0] += d; t[team_of(r["team"])][h][1] += rd
    def pack(d):
        out = []
        for k, (a, b) in d.items():
            if a[0] < 100_000 or b[0] < 100_000:
                continue
            out.append({"name": k, "a": 100 * a[1] / a[0], "b": 100 * b[1] / b[0], "va": a[0] / 1e6, "vb": b[0] / 1e6})
        return sorted(out, key=lambda q: -q["vb"])
    return {"grupos": pack(g), "equipos": pack(t)}


def choque_matriz():
    """Usuario-días con dos piezas el mismo día, por par de equipos (E6b), en M."""
    pc = pares_choque()
    teams = TEAMS + ["Transaccional"]
    M = [[0.0] * len(teams) for _ in teams]
    for (a, b), v in pc["by_team"]:
        i, j = teams.index(a), teams.index(b)
        M[i][j] += v / 1e6
        if i != j:
            M[j][i] += v / 1e6
    tot = pc["tot"] / 1e6
    return {"rows": teams, "cols": teams, "matrix": M, "tot": tot, "same_share": pc["same_share"]}


def pasos_scatter(min_users=5_000):
    """Pasos de Canvas: usuarios que llegan al paso y apertura, por orden del paso (E15)."""
    pts = []
    for r in rows("e15_embudo_pasos.csv"):
        u = f(r["usuarios"])
        if u < min_users or r["canvas_name"] in ("", "null"):
            continue
        o = int(f(r["orden_aprox"]))
        band = "Paso 1" if o <= 1 else ("Paso 2" if o == 2 else ("Pasos 3 y 4" if o <= 4 else "Paso 5 o más"))
        pts.append({"x": u, "y": 100 * min(f(r["usuarios_abrieron"]), u) / u, "g": band, "name": r["canvas_name"], "label": _short_fam(r["canvas_name"], 24), "team": team_of(r["team"]), "orden": o})
    bands = ["Paso 1", "Paso 2", "Pasos 3 y 4", "Paso 5 o más"]
    stats = {}
    for b in bands:
        bp = [p for p in pts if p["g"] == b]
        tu = sum(p["x"] for p in bp)
        stats[b] = {"n": len(bp), "wopen": sum(p["x"] * p["y"] for p in bp) / tu if tu else 0, "under1": sum(1 for p in bp if p["y"] < 1)}
    return {"pts": pts, "bands": bands, "stats": stats, "under1": sum(1 for p in pts if p["y"] < 1 and p["x"] >= 1000)}


def pruebas_mes():
    """Pruebas, copias y QA que llegaron a usuarios reales: envíos por mes y equipo, y las piezas más grandes (E1)."""
    pat = re.compile(r"prueba|test|\bqa\b|copy of|copia|dummy|demo", re.I)
    agg = defaultdict(float); fam = defaultdict(lambda: [0.0, None, set(), ""])
    n_comm = set()
    for r in rows("e1_comunicacion_mes_canal.csv"):
        n = r["communication_name"] or ""
        if not pat.search(n):
            continue
        e = f(r["envios"])
        if e <= 0:
            continue
        t = team_of(r["team"]); m = mes_idx(r["mes"])
        agg[(t, m)] += e; n_comm.add(r["communication_id"])
        v = fam[_fam(n)]; v[0] += e; v[1] = t; v[2].add(MESES[m]); v[3] = r["canal"]
    series = [(t, [agg[(t, m)] / 1e6 for m in range(9)]) for t in TEAMS if sum(agg[(t, m)] for m in range(9)) > 0]
    top = sorted(fam.items(), key=lambda kv: -kv[1][0])[:6]
    return {"cats": MESES, "series": series, "n": len(n_comm), "tot": sum(agg.values()) / 1e6,
            "top": [{"fam": k, "label": _short_fam(k, 30), "team": v[1], "env": v[0], "meses": ", ".join(sorted(v[2], key=MESES.index)), "canal": v[3]} for k, v in top]}


def orden_equipo(top=8):
    """Orden por equipo crudo (sub-equipos de Others incluidos): piezas, sin ticket, sin convención y envíos (E2, E1)."""
    piezas = defaultdict(lambda: {"n": 0, "sin_ticket": 0, "sin_conv": 0, "env": 0.0, "clean": None})
    idk = {}
    for r in rows("e2_catalogo.csv"):
        k = r["team_limpio"] or r["team"]
        idk[r["communication_id"]] = k
        v = piezas[k]
        v["n"] += 1; v["sin_ticket"] += r["tiene_ticket"] != "1"; v["sin_conv"] += r["nombre_sigue_convencion"] != "1"; v["clean"] = team_of(r["team"])
    for r in rows("e1_comunicacion_mes_canal.csv"):
        k = idk.get(r["communication_id"])
        if k in piezas:
            piezas[k]["env"] += f(r["envios"])
    lst = [{"label": k, "g": v["clean"], "n": v["n"], "sin_ticket": v["sin_ticket"], "sin_conv": v["sin_conv"], "env": v["env"] / 1e6} for k, v in piezas.items() if v["n"] >= 20]
    lst.sort(key=lambda q: -(q["sin_ticket"] + q["sin_conv"]))
    return lst[:top]
