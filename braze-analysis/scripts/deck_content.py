# -*- coding: utf-8 -*-
"""Contenido del deck de la auditoría de Braze. Cada slide es un dict.

kind: title | section | content | exec
Exhibits: hbar, col, line, waterfall, table, stats, bullets, gantt, harvey
Las cifras salen del Sheets braze_auditoria_v4 (pestañas Insights, Plan_accion,
Estándares, B_Canales, N a U) y del archivo playbook/ANALISIS_BRAZE_KUESKI.md.
"""

import deck_data as DD

SRC_SHEETS = "Fuente: Sheets braze_auditoria_v4"
PERIODO = "enero a septiembre de 2026"

_CM = DD.canales_mes()
_CE = DD.canal_equipo()
_BP = DD.bandas_periodo()
_SO = DD.solape_mes()
_HD = DD.heat_dia()
_AN = DD.antiguedad()
_SU = DD.solape_usuarios()
_PC = DD.pares_choque()
_bt = {"|".join(k): v / 1e6 for k, v in _PC["by_team"]}


def _pz(name):
    """Nombre corto de una pieza: producto, audiencia y gancho sin ticket ni fecha."""
    parts = [q for q in name.split("-") if q and q.upper() not in ("N/A", "CANVAS", "PUSH", "IA", "E")]
    parts = [q for q in parts if not (q.isdigit() or (q[0] in "BTS" and q[1:].isdigit()))]
    return " ".join(parts[1:5]).replace("_", " ")[:48] if len(parts) > 1 else name[:48]


def _cn(a, b):
    m = {"push notification": "push", "email": "email", "in-app": "in-app", "whatsapp": "WhatsApp"}
    return m.get(a, a) if a == b else f"{m.get(a, a)} y {m.get(b, b)}"


MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep"]

SLIDES = [
    # 1 Portada
    {"kind": "title",
     "title": "Braze en Kueski: mandar menos y a quien sí",
     "subtitle": "Auditoría de comunicaciones, enero a septiembre de 2026",
     "meta": "Business case y plan de acción. 15 de octubre de 2026"},

    # 2 Resumen ejecutivo
    {"kind": "exec",
     "title": "Mandar menos y a quien sí ahorra 1.6 M MXN al mes y recupera la respuesta",
     "groups": [
         ("Qué pasa",
          ["Kueski mandó 667 M mensajes en 9 meses y gastó 57.7 M MXN. El volumen subió 86 % hasta junio y la respuesta cayó: 19 de 24 indicadores están debajo del estándar.",
           "73 % de los usuarios no respondió a nada. 59 % de los mensajes van a un canal que el usuario nunca abrió (18.7 M MXN).",
           "43.8 M mensajes promocionales llegaron a usuarios bloqueados, 80 mil emails a dados de baja y 1 de cada 4 WhatsApp no llega y se paga."]),
         ("Por qué",
          ["Se manda por volumen, no por señal: 5 % de los usuarios recibe 41 o más mensajes al mes y los equipos chocan en los mismos usuarios el mismo día.",
           "No hay grupo de control en ningún Canvas ni una prueba A/B de mensaje: nadie puede decir cuánto vende Braze.",
           "749 piezas sin ticket y 731 formas de escribir la audiencia: no hay dueños ni reglas."]),
         ("Qué hacer",
          ["Ejecutar el plan por campaña: 582 campañas a tocar, 1.6 M MXN al mes de ahorro (33 % del gasto) y 27 M mensajes menos al mes (42 %).",
           "Adoptar el playbook: 12 reglas, exclusiones, canal y frecuencia por usuario, control del 10 % en toda pieza.",
           "Configurar Braze una vez (topes, control nativo, horas de silencio, re-elegibilidad) y nombrar un dueño por cosa. 90 días."]),
     ]},

    # 3 Alcance
    {"kind": "content", "tracker": "Contexto",
     "title": "Revisamos 9 meses de envíos: 667 M mensajes, 3,439 comunicaciones y 18 extracciones de Databricks",
     "exhibit": {"type": "stats", "items": [
         ("667 M", "mensajes enviados", "email, push, WhatsApp, in-app"),
         ("57.7 M MXN", "costo variable", "email 0.05, WhatsApp 1.00 por entregado"),
         ("3,439", "comunicaciones", "1,822 familias, 1,913 campañas por canal"),
         ("19.5 M", "usuarios alcanzados", "20.1 M con email en el periodo"),
         ("5", "equipos", "Marketing, Product Growth, Sales, Collections, Others"),
         ("18", "extracciones", "E1 a E18b, agregadas, sin datos personales"),
     ]},
     "side": ["Respuesta: clic en email, apertura en push, lectura en WhatsApp, clic en in-app. Abrir un email no cuenta.",
              "Sin segmento: pieza que va a toda la base o a una etiqueta de estado ('Todos', 'Leads', 'Nuevos registrados', 'Full_Rollout') sin un filtro de comportamiento (abrió algo en 90 días, empezó una solicitud, tiene pago próximo). Con señal: pieza cuya audiencia se define por lo que el usuario hizo.",
              "Conversión a 7 días solo como referencia: no hay grupo de control.",
              "Costo variable sin el costo fijo de Braze (pendiente).",
              "Todo el modelo está en el Sheets con fórmulas vivas y 471 verificaciones."],
     "source": SRC_SHEETS + ", pestañas Léeme y Parámetros; Databricks braze.*"},

    # 4 Panorama canal
    {"kind": "content", "tracker": "Contexto",
     "title": "WhatsApp es 8 % del volumen y 71 % del costo: Marketing pone 22.9 M MXN y Product Growth 11.4 M; el email más grande es el de Product Growth (117 M) y el push más grande el de Marketing (131 M)",
     "exhibit": {"type": "stackbar", "segments": _CE["teams"], "panels": [
         {"title": "Envíos en 9 meses (M), por canal y equipo", "cats": _CE["cats"], "rows": _CE["env"], "fmt": "int"},
         {"title": "Costo variable (M MXN), por canal y equipo", "cats": _CE["cats"], "rows": _CE["cost"], "fmt": "MXN", "zero": "sin costo variable"}],
         "note": "Email 0.05 MXN por enviado; WhatsApp 1.00 MXN por entregado; push e in-app sin costo variable. Dentro de cada barra, el valor del segmento cuando cabe."},
     "kpis": [("71 %", "del costo variable es WhatsApp, con 8 % de los envíos"), ("22.9 M MXN", "de WhatsApp los puso Marketing en 9 meses; Product Growth 11.4 M"), ("131 M", "push de Marketing y 117 M emails de Product Growth: los dos bloques más grandes")],
     "side": ["Marketing es 39 % de los envíos y 47 % del costo: 31 M WhatsApp (22.9 M MXN) y 131 M push. Product Growth, 27 % y 30 %: 117 M emails (5.8 M MXN) y 16 M WhatsApp (11.4 M MXN).",
              "Sales usa WhatsApp con recurrentes de KPay (5.9 M MXN, 80 % de entrega, 78 % de lectura). Collections no usa WhatsApp.",
              "Respuesta por canal: in-app 38 %, WhatsApp 69 % de lectura, push 1.5 %, email 0.93 % de clic.",
              "El dinero está en el WhatsApp de Marketing y Product Growth; el volumen y las bajas, en el email de Product Growth y Marketing."],
     "source": SRC_SHEETS + ", B_Canales B2 (E4a)"},

    # 5 Serie mensual
    {"kind": "content", "tracker": "Contexto",
     "title": "El volumen subió 86 % de enero a junio y la respuesta cayó en los cuatro canales a la vez",
     "exhibit": {"type": "smallmult", "highlight": [5], "cells": [
         {"title": "Email", "cats": MESES, "vol": ("Enviados (M)", _CM["email"]["vol"]), "resp": ("Clic sobre entregados (%)", _CM["email"]["resp"]), "fmt_resp": "pct2"},
         {"title": "Push", "cats": MESES, "vol": ("Enviados (M)", _CM["push notification"]["vol"]), "resp": ("Apertura (%)", _CM["push notification"]["resp"]), "fmt_resp": "pct2"},
         {"title": "WhatsApp", "cats": MESES, "vol": ("Enviados (M)", _CM["whatsapp"]["vol"]), "resp": ("Lectura sobre entregados (%)", _CM["whatsapp"]["resp"]), "fmt_resp": "pct0", "ymin": 50},
         {"title": "In-app", "cats": MESES, "vol": ("Impresiones (M)", _CM["in-app"]["vol"]), "resp": ("Clic (%)", _CM["in-app"]["resp"]), "fmt_resp": "pct0"},
     ]},
     "side": ["Junio: 109 M envíos (el doble de enero) y el peor mes en email (0.67 %), push (1.05 %) y WhatsApp (67 % de lectura). Fue el email de BillPay a 16 M usuarios encima de Hot Sale.",
              "Septiembre: el push bajó a 24 M y abrió 2.12 %, el mejor del año. La respuesta se mueve al revés del volumen en los cuatro canales.",
              "WhatsApp perdió 10 puntos de lectura en el año (74 % a 64 %) mientras el volumen bajó: la base que queda responde menos."],
     "source": SRC_SHEETS + ", B_Canales B1 (E4a). Respuesta: clic sobre entregados (email), apertura (push), lectura sobre entregados (WhatsApp), clic sobre impresiones (in-app)"},

    # 6 Estándares
    {"kind": "content", "tracker": "Contexto",
     "title": "19 de 24 indicadores están debajo del estándar; email, push y WhatsApp no llegan al piso de la industria",
     "exhibit": {"type": "table", "head": ["Indicador", "Hoy", "Estándar", "Estado"],
                 "rows": [["Clic de email", "0.92 %", "1.5 %", "Debajo"],
                          ["Bajas de email por mil", "3.13", "2.5", "Debajo"],
                          ["Apertura de push", "1.53 %", "3 %", "Debajo"],
                          ["Entrega de WhatsApp", "74 %", "90 %", "Debajo"],
                          ["Lectura de WhatsApp", "69 %", "70 %", "Debajo por poco"],
                          ["Mensajes a canal mudo", "59 %", "20 %", "Debajo"],
                          ["Usuarios que nunca respondieron", "73 %", "50 %", "Debajo"],
                          ["Promocional a etapas bloqueadas", "43.8 M", "0", "Debajo"],
                          ["Canvas con grupo de control", "0 de 3,228", "Todos", "Debajo"],
                          ["Envíos con ticket", "87 %", "100 %", "Debajo"],
                          ["Entrega de email", "95.1 %", "95 %", "Cumple"],
                          ["Clic de in-app", "38 %", "5 a 20 %", "Cumple"]],
                 "status_col": 3},
     "side": ["Los 24 indicadores con definición, fórmula y estándar están en la pestaña Estándares del Sheets y en el anexo.",
              "El estándar es el piso del rango de la industria o una propuesta interna; es editable.",
              "Cumplen 5: entrega de email, apertura de email, clic de in-app, toques por pieza y usuario-días con 3 o más piezas."],
     "source": SRC_SHEETS + ", Estándares"},

    # A divider
    {"kind": "section", "num": "A", "title": "Mandamos a quien no responde",
     "subtitle": "La mitad del esfuerzo va a usuarios que no pueden o no quieren responder"},

    # 7
    {"kind": "content", "tracker": "A. A quien no responde",
     "title": "73 % de los usuarios no respondió a nada en 9 meses; el 11 % que responde a varios canales recibe la mitad de los mensajes",
     "exhibit": {"type": "hbar2", "cats": ["Ninguno", "Solo WhatsApp", "Solo in-app", "Solo email", "Varios canales"],
                 "series": [("% de usuarios", [73, 8, 6, 2, 11]), ("% de mensajes", [24, 15, 7, 2, 52]), ("% del costo", [14, 34, 4, 1, 47])],
                 "fmt": "pct0", "max": 80},
     "side": ["14.2 M usuarios sin una sola respuesta. Reciben 11 mensajes cada uno y convierten 0.08 %.",
              "Quien solo responde a WhatsApp es 8 % de los usuarios y 34 % del costo: recibe 58 M emails y 21 M push que nunca abre.",
              "Quien responde a varios canales convierte 30 a 75 % porque es cliente activo. Sirve para segmentar, no para decir que el mensaje vendió."],
     "source": SRC_SHEETS + ", J_Canal (E7b)"},

    # 8 canal mudo
    {"kind": "content", "tracker": "A. A quien no responde",
     "title": "59 % de los mensajes van a un canal que el usuario nunca abrió: 394 M mensajes y 18.7 M MXN",
     "exhibit": {"type": "stats", "items": [
         ("59 %", "de los mensajes a canal mudo", "394 M en 9 meses"),
         ("18.7 M MXN", "costo de esos mensajes", "32 % del costo variable"),
         ("149 M", "emails a quien responde a otro canal", "pero nunca hizo clic en un email"),
         ("3.2 M", "WhatsApp entregados", "a quien nunca leyó un WhatsApp"),
     ]},
     "side": ["Canal mudo: canal al que ese usuario nunca respondió aunque sí respondió a otro.",
              "Regla del playbook: se manda por el canal al que el usuario responde; el push es el canal de señal.",
              "Hace falta el atributo canal_preferido_90d en Braze para filtrarlo en cada pieza."],
     "source": SRC_SHEETS + ", J_Canal R22 y H22 (E7b)"},

    # 9 nunca respondió
    {"kind": "content", "tracker": "A. A quien no responde",
     "title": "97.5 M mensajes fueron a quien nunca respondió: 8.1 M MXN, 17 % de las bajas y cero conversiones",
     "exhibit": {"type": "hbar", "cats": ["Email", "Push", "WhatsApp", "In-app"],
                 "vals": [61.4, 31.0, 5.0, 0.1], "fmt": "M", "label": "Envíos a quien nunca respondió (M)",
                 "notes": ["18 % del canal, 3.1 M MXN, 191 mil bajas", "12 % del canal", "9 % del canal, 5.0 M MXN", "0.7 % del canal"],
                 "highlight": [0, 2]},
     "side": ["Cada mes 1.1 M de usuarios reciben email sin haber respondido jamás. En junio fueron 11.9 M por BillPay.",
              "Unos 900 mil MXN al mes. Nadie convirtió sin haber respondido antes.",
              "Regla: sin respuesta en 90 días, fuera de lo promocional (exclusión EXC-SinRespuesta90d). Se paga sola."],
     "source": SRC_SHEETS + ", T_SinRespuesta (E16)"},

    # 10 etapas bloqueadas
    {"kind": "content", "tracker": "A. A quien no responde",
     "title": "43.8 M mensajes promocionales llegaron a usuarios bloqueados y 80 mil emails a gente que ya se dio de baja",
     "exhibit": {"type": "hbar", "cats": ["Marketing", "Sales", "Product Growth", "Others", "Collections"],
                 "vals": [16.5, 13.0, 11.4, 2.8, 0], "fmt": "M", "label": "Envíos promocionales a etapas bloqueadas (M)",
                 "highlight": [0, 1, 2]},
     "side": ["Bloqueados: tarjeta KPay congelada (43.4 M), REUS o ARCO (249 mil), lista negra (146 mil).",
              "Contando todo tipo de mensaje: 57.4 M a tarjeta congelada (4.4 M usuarios, 5.1 M MXN) y 1.48 M a lista negra, REUS o ARCO.",
              "80 mil emails promocionales a dados de baja (Marketing 59 mil): el filtro de suscripción estaba solo a la entrada del Canvas.",
              "Regla: 7 exclusiones como filtro negativo en todo lo promocional. Legal decide sobre REUS y ARCO."],
     "source": SRC_SHEETS + ", H_Etapas (E7a), E_DespuesBaja (E5b). Golden dataset cubre 37 % de los envíos"},

    # 11 WhatsApp entrega
    {"kind": "content", "tracker": "A. A quien no responde",
     "title": "1 de cada 4 WhatsApp no llega: 14.2 M mensajes en 9 meses que se mandan a números que no reciben",
     "exhibit": {"type": "line", "cats": MESES, "series": [("Entrega de WhatsApp (%)", [80, 77, 74, 69, 67, 74, 73, 78, 77])],
                 "ymin": 60, "ymax": 90, "ref": (90, "Estándar 90 %"), "highlight": [3, 4]},
     "side": ["55.2 M enviados, 41.0 M entregados (74 %). Meta cobra por entregado; si cobrara por enviado serían 14.2 M MXN tirados.",
              "Entre quienes nunca responden la entrega es 34 %; entre quienes leen WhatsApp, 83 %. El número que no recibe es la primera señal de limpieza.",
              "Abril y mayo tocaron piso (69 % y 67 %) y se siguió mandando. Se recuperó cuando bajó el volumen.",
              "Regla: WhatsApp solo a quien ya dio señal. Exclusión EXC-WA_SinEntrega3 en toda pieza."],
     "source": SRC_SHEETS + ", B_Canales B4 (E4a), J_Canal (E7b)"},

    # B divider
    {"kind": "section", "num": "B", "title": "Mandamos demasiado y sin coordinación",
     "subtitle": "La presión por usuario, el choque entre equipos y los Canvas de 100 pasos"},

    # 12 concentración
    {"kind": "content", "tracker": "B. Demasiado y sin coordinación",
     "title": "5 % de los usuarios recibe 41 o más mensajes al mes y concentra 30 % del volumen; con 321 o más mensajes la baja se multiplica por 13",
     "exhibit": {"type": "panels", "cats": _BP["cats"], "highlight": [7], "panels": [
         {"title": "Usuarios (M) según mensajes recibidos en 9 meses", "kind": "col", "series": [("Usuarios (M)", _BP["usuarios"])], "fmt": "M"},
         {"title": "Bajas de email por 100 usuarios", "kind": "line", "series": [("Bajas por 100", _BP["bajas"])], "fmt": "pct1"},
         {"title": "Usuarios que convirtieron (%)", "kind": "line", "series": [("Convirtieron", _BP["conv"])], "fmt": "pct0"},
     ]},
     "side": ["Un usuario recibe 10.4 mensajes al mes en promedio; 5 % recibe 41 o más al mes y concentra 30 % del volumen.",
              "339 mil usuarios recibieron 321 o más mensajes en 9 meses: 16.5 bajas por 100 usuarios contra 1.3 en la banda de 1 a 5.",
              "La conversión también sube con los mensajes, pero por selección: el cliente activo recibe cobranza y transaccionales. No prueba que el mensaje convierta; la baja sí es consecuencia directa.",
              "Regla: 5 promocionales por semana, 2 piezas al día, 1 push al día, 1 WhatsApp al mes."],
     "source": SRC_SHEETS + ", B_Canales B3 (E4b), G_Practicas (E3)"},

    # 13 solape
    {"kind": "content", "tracker": "B. Demasiado y sin coordinación",
     "title": "Cada mes 1.3 a 2.2 M usuarios reciben 3 o más campañas distintas el mismo día; desde junio su baja por mil se duplica, mientras quien recibe una sola bajó de 0.57 a 0.34",
     "exhibit": {"type": "panels", "cats": MESES, "ph": 112, "highlight": [5], "panels": [
         {"title": "Usuarios (M) que recibieron 2, 3 a 4, 5 a 7 u 8 o más campañas distintas en un mismo día, por mes (color más oscuro = más campañas)", "kind": "line", "series": _SU["usuarios"], "fmt": "M", "point_labels": False, "ymin": 0, "ramp": True},
         {"title": "Bajas de email por mil usuario-días, según campañas distintas recibidas ese día", "kind": "line", "series": [(f"{b} campañas" if b != "1" else "1 campaña", v) for b, v in _SO["baja"]], "fmt": "pct2", "point_labels": False, "ymin": 0, "ymax": 1.5, "ramp": True}]},
     "side": [f"Cuántos: la banda de 8 o más son {min(_SU['u8']):.0f} a {max(_SU['u8']):.0f} mil usuarios al mes ({min(_SU['msgs_8']):.1f} a {max(_SU['msgs_8']):.1f} M mensajes); la de 2 campañas, 1.7 a 3.3 M usuarios. 9 % de los usuario-días reciben 3 o más campañas y son 24 % de los mensajes.",
              f"Quién: {_PC['same_share']:.0f} % del choque es dentro del mismo equipo. Marketing con Marketing {_bt['Marketing|Marketing']:.0f} M usuario-días, Sales con Sales {_bt['Sales|Sales']:.0f} M, Marketing con Sales {_bt['Marketing|Sales']:.0f} M, Product Growth con Marketing {_bt['Marketing|Product Growth']:.0f} M.",
              "Cuándo y de qué: junio, piezas a 'Todos' (lanzamiento de BillPay, Día del Padre, AnotayGana, Mundial) encima de los Canvas que corren diario. La siguiente lámina lista los pares."],
     "source": SRC_SHEETS + ", F_Solape (E6a, E6b). Usuario-día: un usuario en un día con al menos un envío"},

    # 14 nuevos
    {"kind": "content", "tracker": "B. Demasiado y sin coordinación",
     "title": "Un usuario nuevo se da de baja a los 27 días con 5 emails; un solo envío masivo explica 31 % de esas bajas",
     "exhibit": {"type": "hbar", "cats": ["BillPay Intro (email masivo, junio)", "Retargeting de registro (2 emails al día)", "Rescates de Tasa 0", "Resto"],
                 "vals": [31, 22, 8.5, 38.5], "fmt": "pct0", "label": "% de las bajas de usuarios nuevos según la pieza que llegó el día de la baja",
                 "highlight": [0, 1]},
     "side": ["158 mil usuarios nuevos se dieron de baja en el periodo. 33 % con el primer email; 7.4 % el mismo día.",
              "Antes de irse recibieron 5 emails de 4 piezas distintas. No es cansancio acumulado, es el contenido y la cantidad del primer mes.",
              "Los nuevos son los que mejor responden (clic 2.4 %, push 3.4 %) y los que más se dan de baja (6.9 por mil).",
              "Regla: una sola secuencia de bienvenida, 1 email al día, 3 la primera semana. Ningún masivo incluye a usuarios con menos de 30 días."],
     "source": SRC_SHEETS + ", L_Baja (E8), O_Antiguedad (E12)"},

    # 15 Canvas pasos
    {"kind": "content", "tracker": "B. Demasiado y sin coordinación",
     "title": "45 Canvas pasan de 20 pasos y 477 pasos abren menos de 1 %; la insistencia no sube la apertura",
     "exhibit": {"type": "colline", "cats": ["Paso 1", "Paso 2", "Paso 3", "Paso 4", "Paso 5 o más"],
                 "cols": ("Usuarios que llegan (M)", [31.5, 28.6, 16.7, 7.0, 6.0]),
                 "line": ("Apertura del paso (%)", [15.7, 16.0, 25.8, 16.4, 15.7]), "highlight": []},
     "side": ["959 Canvas con 5,986 pasos. La mitad tiene 3 pasos o menos; 45 pasan de 20 y 19 pasan de 50. Los de inactividad tienen entre 96 y 120 pasos para 734 mil usuarios.",
              "El paso 3 abre más porque ahí entran los filtros de quien ya reaccionó, no porque el tercer mensaje convenza. Push detrás de una señal abre 6 % contra 2 %.",
              "477 pasos con mil o más usuarios abren menos de 1 %; 80 tienen más de 10 mil usuarios y menos de 0.5 %.",
              "Regla: máximo 8 pasos, 2 toques por canal, un paso de Decision después de cada envío."],
     "source": SRC_SHEETS + ", S_Pasos (E15). El orden del paso es aproximado"},

    # 16 día de la semana
    {"kind": "content", "tracker": "B. Demasiado y sin coordinación",
     "title": "El lunes concentra 23 % del email con el peor clic de la semana (0.65 %); el fin de semana responde más en todos los equipos salvo Collections",
     "exhibit": {"type": "heatmap", "cols": _HD["cols"], "rows": _HD["rows"], "matrix": _HD["matrix"], "share": _HD["share"],
                 "share_label": "% de los emails enviados, por día", "label": "Clic de email sobre entregados (%), por equipo y día", "fmt": "pct2"},
     "side": ["Product Growth: 0.29 % el lunes contra 1.53 % el domingo. Sales no pasa de 0.38 % ningún día: su problema es la pieza, no el calendario.",
              "El domingo también tiene el triple de bajas por mil (7.7 contra 2.3): responde más porque las piezas son chicas y van a gente caliente, no porque sea domingo.",
              "WhatsApp se entrega y se lee mejor en fin de semana (87 % y 89 % en domingo contra 71 a 75 % entre semana). Push e in-app no cambian con el día."],
     "source": SRC_SHEETS + ", N_DiaSemana (E10). Celdas con menos de 50 mil entregados en gris"},

    # 17 antigüedad
    {"kind": "content", "tracker": "B. Demasiado y sin coordinación",
     "title": "56 % de los envíos van a usuarios con más de un año en la base, que reciben 7 veces más push y abren la tercera parte",
     "exhibit": {"type": "panels", "cats": _AN["cats"], "highlight": [4, 5], "panels": [
         {"title": "Envíos en 9 meses (M), por antigüedad del usuario", "kind": "col", "series": [("Envíos (M)", _AN["vol"])], "fmt": "M"},
         {"title": "Respuesta (%)", "kind": "line", "series": [("Clic de email", _AN["click"]), ("Apertura de push", _AN["push"])], "fmt": "pct2"},
         {"title": "Bajas por mil emails", "kind": "line", "series": [("Bajas por mil", _AN["bajas"])], "fmt": "pct1", "ymin": 0, "ymax": 4.5},
     ]},
     "side": ["A más antigüedad, más mensajes y menos respuesta: el usuario de más de 2 años recibió 91 push en 9 meses; el de menos de 1 mes, 13.",
              "Las bajas por mil son iguales en todas las bandas: el nuevo no se da de baja más por email que el viejo, se da de baja por la cantidad.",
              "Regla: a más de 1 año sin respuesta en 90 días, fuera de lo promocional. Push a más de 2 años solo a quien abrió un push en 90 días. La frecuencia alta se reserva para el primer mes."],
     "source": SRC_SHEETS + ", O_Antiguedad (E12). Push por usuario en 9 meses"},

    # C divider
    {"kind": "section", "num": "C", "title": "Sabemos qué funciona",
     "subtitle": "Gancho, canal, tamaño, toques y equipo: los datos ya dicen qué mandar"},

    # 18 gancho
    {"kind": "content", "tracker": "C. Qué funciona",
     "title": "Recordar algo que el usuario empezó responde 3.09 % por email; una oferta nueva, entre 0.22 % y 0.53 %",
     "exhibit": {"type": "hbar", "cats": ["Retargeting o recordatorio", "Tasa 0", "Descuento, cupón, oferta", "Cross sell", "Referidos", "Lanzamiento, novedades"],
                 "vals": [3.09, 0.53, 0.41, 0.34, 0.22, 0.22], "fmt": "pct2", "label": "Clic de email por gancho (%)",
                 "notes": ["23.6 M emails", "54.3 M emails", "35.0 M", "2.7 M", "40.8 M", "33.0 M"], "highlight": [0]},
     "side": ["Tasa 0 es el gancho con más emails (54 M) y responde 6 veces menos que un recordatorio.",
              "Referidos y lanzamientos responden 0.22 % por email y 43 a 55 % en in-app: van en in-app.",
              "Regla: el gancho principal es recordar algo que el usuario empezó. Una sola pieza de Tasa 0 por audiencia."],
     "source": SRC_SHEETS + ", Campañas (E1), gancho leído del nombre de la pieza"},

    # 19 canal
    {"kind": "content", "tracker": "C. Qué funciona",
     "title": "In-app responde 38 % y no cuesta; email responde 0.93 % y WhatsApp cuesta 20 veces más por mensaje",
     "exhibit": {"type": "table", "head": ["Canal", "Respuesta hoy", "Mínimo para seguir", "Costo por mensaje", "Funciona para", "No funciona para"],
                 "rows": [["In-app", "38 % de clic", "10 %", "0", "Referidos, lanzamientos, retargeting, onboarding", "Ofertas genéricas (14 %)"],
                          ["WhatsApp", "69 % de lectura, 74 % de entrega", "60 % y 80 %", "1.00 MXN", "Activos y recurrentes de KPay", "Bases frías, primer toque, repetir a los 2 a 6 días"],
                          ["Push", "1.5 % de apertura", "0.75 %", "0", "Cobranza, nuevos, retargeting, recurrentes; es el canal de señal", "Leads, anónimos, fríos, lanzamientos"],
                          ["Email", "0.93 % de clic, 3.1 bajas por mil", "0.3 % y 2.5", "0.05 MXN", "Transaccional, retargeting a registrados, nuevos", "Tasa 0, referidos, newsletters, bases frías, más de 1 M"]],
                 "highlight_rows": [0]},
     "side": ["Email: no es el asunto (abren 24 %), es que no hay qué hacer adentro. Un solo llamado a la acción.",
              "Push: primero push, y el resto solo a quien lo abrió.",
              "WhatsApp: nunca como primer toque.",
              "In-app: lo informativo va ahí primero."],
     "source": SRC_SHEETS + ", B_Canales, Medianas, Parámetros"},

    # 20 tamaño y toques
    {"kind": "content", "tracker": "C. Qué funciona",
     "title": "Audiencias de 10 a 100 mil usuarios y 2 toques responden 7 veces más que envíos de más de 1 M con 3 toques",
     "exhibit": {"type": "hbar2", "cats": ["10 a 100 mil usuarios", "100 mil a 1 M", "Más de 1 M", "1 toque", "2 toques", "3 a 4 toques"],
                 "series": [("Clic de email (%)", [1.2, 0.6, 0.16, 0.8, 1.8, 0.5])], "fmt": "pct2", "max": 2.2, "highlight": [0, 4]},
     "side": ["Tamaño: a más de 1 M el clic cae a 0.16 %. Regla: más de 1 M obliga a prueba al 10 % y a un segmento.",
              "Toques: el segundo toque sube la respuesta (1.8 %); el tercero la hunde (0.5 %). Regla: 2 toques y se acabó, el segundo solo a quien no abrió el primero.",
              "El tamaño ideal es 10 a 100 mil usuarios con un criterio."],
     "source": SRC_SHEETS + ", G_Practicas (E1 por banda de tamaño y de toques)"},

    # 21 equipo
    {"kind": "content", "tracker": "C. Qué funciona",
     "title": "Cada equipo tiene un canal que le funciona y otro que le cuesta",
     "exhibit": {"type": "table", "head": ["Equipo", "Envíos", "Costo", "Funciona", "No funciona", "Ahorro al mes"],
                 "rows": [["Marketing", "262 M (39 %)", "27.2 M (47 %)", "Retargeting Veriff (email 3.0 %, push 5.8 %), in-app de registro (87 %)", "Rescates por push a anónimos (0.6 a 0.8 % en 22 M), referidos por email (0.1 a 0.2 % en 15 M), 4.95 bajas por mil", "0.16 M MXN"],
                          ["Product Growth", "177 M (27 %)", "17.3 M (30 %)", "Retargeting Installments a activos (push 11 %), in-app 46 %", "Tasa 0 por email a registrados (35 M, 0.28 %), NeverActive (13 M, 0.10 %), Canvas de inactividad de 120 pasos", "1.30 M MXN"],
                          ["Sales", "85 M (13 %)", "7.1 M (12 %)", "Push y WhatsApp a recurrentes KPay (80 % entrega, 78 % lectura, push 4.2 %)", "Email (0.21 %, el peor), promoción a tarjetas congeladas (13 M)", "0.10 M MXN"],
                          ["Collections", "45 M (7 %)", "1.6 M (3 %)", "Precobranza: email 4.3 %, push 5.3 %, la mejor pieza de la empresa", "Ticket T000 en todo; Canvas PRUEBA_ a 5 mil usuarios reales", "0"],
                          ["Others", "98 M (15 %)", "4.4 M (8 %)", "Transaccional (Payment Confirmation 3.8 %)", "BillPay Intro (16 M, 0.11 %, 31 % de las bajas de nuevos), Shopping (7 M, 0.12 %)", "0.04 M MXN"]],
                 "highlight_rows": [1]},
     "side": [],
     "source": SRC_SHEETS + ", Vista_equipo, Campañas, Plan_accion P3"},

    # 22 top piezas
    {"kind": "content", "tracker": "C. Qué funciona",
     "title": "10 piezas concentran 125 M envíos con respuesta debajo del mínimo; 6 piezas hay que proteger",
     "exhibit": {"type": "table", "head": ["Pieza (nombre actual)", "Canal", "Envíos", "Respuesta", "Acción"],
                 "rows": [["Lending-KCash-B0211 Nuevos_RegistradosPay Tasa0", "email", "34.9 M", "0.28 %", "Apagar"],
                          ["NewProducts T0000 Portfolio_BillPay_Intro", "email", "16.1 M", "0.11 %", "Confirmar apagado"],
                          ["Lending-KCash-B0223 Nuevos_NeverActive Installments", "email", "13.5 M", "0.10 %", "Apagar"],
                          ["Marketing-KCash-B0391 Leads RescateFinesDeSemana", "push", "13.4 M", "0.76 %", "Rehacer"],
                          ["Marketing-KCash-B0000 Leads Retargeting_Veriff", "email", "9.7 M", "3.04 %", "Bajar frecuencia"],
                          ["Marketing-KCash-B0171 Anonimos RescateTasa0", "push", "8.9 M", "0.56 %", "Apagar"],
                          ["Marketing-KCash-B0326 Leads ReferralProgram", "email", "8.5 M", "0.23 %", "Confirmar apagado"],
                          ["Marketing-KCash-B0326 Recurrentes_Dormants ReferralProgram", "email", "7.0 M", "0.07 %", "Apagar"],
                          ["Shopping-KPay-S0004 WeeklyRecommendations", "email", "7.0 M", "0.12 %", "Rehacer"],
                          ["Sales-KPay-B0335 Recurrentes PromocionesMerchants", "email", "6.4 M", "0.22 %", "Rehacer"]],
                 "status_col": 4},
     "side": ["Proteger: Precobranza (email 4.3 %, push 5.3 %), Retargeting Veriff (push 5.8 %), Retargeting Installments a activos (push 11 %), Payment Confirmation (3.8 %), registro de línea MX in-app (87 %), Quincenas sin intereses (push 4.2 %).",
              "La acción de cada pieza sale de una regla con datos (señal, canal, abren contra no abren), no del nombre."],
     "source": SRC_SHEETS + ", Plan_accion P4, Campañas"},

    # D divider
    {"kind": "section", "num": "D", "title": "Nadie puede demostrar cuánto vende Braze",
     "subtitle": "Sin grupo de control, sin pruebas A/B y sin nombres, no hay forma de defender una pieza"},

    # 23 control
    {"kind": "content", "tracker": "D. Sin medición",
     "title": "0 de 3,228 Canvas tienen grupo de control real y no hubo una sola prueba A/B de mensaje en 9 meses",
     "exhibit": {"type": "stats", "items": [
         ("0 de 3,228", "Canvas con control real", "22 tienen usuarios marcados; el único grande abrió el mensaje 84 %"),
         ("0", "pruebas A/B de mensaje", "313 Canvas con 'experimento' son caminos de audiencia; la variante es siempre Variant 1"),
         ("4", "Canvas con push silencioso", "650 mil usuarios para simular control"),
         ("2.3 veces", "convierten más los que abren", "no es causal: parte iba a comprar igual"),
     ]},
     "side": ["Consecuencia: ninguna cifra de conversión es incremental. Dice quién convierte después de recibir, no cuánto más convierte por recibir.",
              "Braze trae grupo de control nativo en campañas y en la entrada del Canvas, y reporta el lift solo.",
              "Regla: 10 % de control en toda pieza (5 % si pasa de 1 M). A las 4 semanas se lee el lift; lift cero, se apaga aunque 'convierta'. Una prueba A/B por equipo al mes."],
     "source": SRC_SHEETS + ", Q_Control (E13), R_Experimentos (E14), K_Abren (E7c)"},

    # 24 orden
    {"kind": "content", "tracker": "D. Sin medición",
     "title": "749 piezas sin ticket, 731 formas de escribir la audiencia y 171 pruebas que llegaron a usuarios reales",
     "exhibit": {"type": "table", "head": ["Qué", "Cuánto", "Qué se hace"],
                 "rows": [["Piezas sin ticket", "749 (Others solo tiene ticket en 49 % de sus envíos)", "Sin ticket no se activa"],
                          ["Formas de escribir la audiencia", "731; 41 segmentos, 330 subsegmentos, 62 grupos; 13 % 'Not Tracked'", "30 segmentos maestros con dueño"],
                          ["Piezas activas duplicadas", "109 en 13 combinaciones; 15 familias con 10 o más versiones", "Una por combinación"],
                          ["Pruebas y copias a usuarios reales", "171 comunicaciones, 7.26 M envíos; un QA con 1.87 M push", "Se pausan hoy; roles de aprobación"],
                          ["Canvas con más de 20 pasos", "45 (19 con más de 50)", "Se parten por audiencia, 8 pasos"],
                          ["Comercio del día y Cuponera", "11 y 8 segmentos distintos solo por el mes", "Una pieza que lee del catálogo"]]},
     "side": ["Regla de nombres: Ticket-Producto-Audiencia-Gancho. El equipo sale de la letra del ticket.",
              "Tags obligatorios de lista cerrada: tipo, equipo, producto y trimestre.",
              "Los tags no llegan a Databricks: hoy no se pueden auditar."],
     "source": SRC_SHEETS + ", Catálogo, P_Segmentos (E11)"},

    # E divider
    {"kind": "section", "num": "E", "title": "El plan",
     "subtitle": "Limpiar, configurar, medir: 90 días"},

    # 25 plan ahorro
    {"kind": "content", "tracker": "E. El plan",
     "title": "582 campañas a tocar: 1.6 M MXN al mes de ahorro (33 % del gasto) y 27 M mensajes menos al mes (42 %)",
     "exhibit": {"type": "waterfall", "cats": ["Gasto al mes hoy", "Apagar (48)", "Limpiar base WhatsApp (56)", "Rehacer o re-segmentar (162)", "Gasto al mes después"],
                 "vals": [4.82, -1.16, -0.24, -0.20, 3.22], "fmt": "MXN", "label": "MXN al mes (M)"},
     "side": ["Apagar: 48 campañas activas, 18.4 M mensajes al mes. Confirmar apagado: 232 que ya no envían, que no revivan.",
              "Bajar frecuencia: 84. Proteger: 138. Escalar: 154.",
              "Es un techo: supone apagar todo lo que tiene señal. WhatsApp cobrado por entregado; por enviado el ahorro sería el doble.",
              "No incluye el costo fijo de Braze ni los MAU que dejan de contarse."],
     "source": SRC_SHEETS + ", Plan_accion P1 y P2"},

    # 26 por equipo
    {"kind": "content", "tracker": "E. El plan",
     "title": "Product Growth tiene 81 % del ahorro; Marketing tiene el mayor volumen a bajar frecuencia",
     "exhibit": {"type": "hbar", "cats": ["Product Growth", "Marketing", "Sales", "Others", "Collections"],
                 "vals": [1.30, 0.16, 0.10, 0.04, 0], "fmt": "MXN", "label": "Ahorro al mes si se ejecuta el plan (M MXN)",
                 "notes": ["74 campañas con señal; Apagar 17 (B0211, B0223)", "141 con señal; 51 a bajar frecuencia", "91 con señal; 51 a rehacer", "19 con señal", "Fuera del alcance (cobranza)"],
                 "highlight": [0]},
     "side": ["Product Growth: 1.04 M MXN al mes solo con Apagar (17 campañas, 9 M mensajes al mes).",
              "Marketing: 23 a apagar y 23 WhatsApp a limpiar base (11.9 M MXN del periodo).",
              "Sales: el ahorro está en rehacer 18 campañas activas de email a recurrentes.",
              "Collections no entra: cobranza no se toca sin Legal."],
     "source": SRC_SHEETS + ", Plan_accion P3"},

    # 27 top 10 acción
    {"kind": "content", "tracker": "E. El plan",
     "title": "Diez piezas con acción concreta cubren 125 M envíos",
     "exhibit": {"type": "table", "head": ["Pieza", "Acción", "Qué cambia"],
                 "rows": [["B0211 Tasa0 a registrados (email, 34.9 M)", "Apagar", "Se deja en push acotado a quien abrió un push en 60 días, 2 toques"],
                          ["BillPay Intro (email, 16.1 M)", "Confirmar apagado", "Archivar; BillPay entra a las reglas de todos"],
                          ["B0223 NeverActive Installments (email, 13.5 M)", "Apagar", "Fríos solo con señal y solo Lending"],
                          ["B0391 RescateFinesDeSemana (push, 13.4 M)", "Rehacer", "Solo a quien abrió un push en 60 días; nunca a nuevos en fin de semana"],
                          ["B0000 Retargeting Veriff (email, 9.7 M)", "Bajar frecuencia", "De 2 emails al día a 1; funciona (3.04 %)"],
                          ["B0171 RescateTasa0 a anónimos (push, 8.9 M)", "Apagar", "Anónimos van por in-app"],
                          ["B0326 ReferralProgram (email, 15.5 M en dos)", "Apagar y confirmar", "Referidos a in-app y push a clientes activos"],
                          ["S0004 WeeklyRecommendations (email, 7.0 M)", "Rehacer", "Solo recurrentes KPay; quitar 57 mil REUS"],
                          ["B0335 PromocionesMerchants (email, 6.4 M)", "Rehacer", "Push y WhatsApp a recurrentes; email no"],
                          ["Canvas ConSinOferta B0331 a B0333 (19 Canvas, 734 mil usuarios)", "Rehacer", "8 pasos, control 10 %, partidos por audiencia"]],
                 "status_col": 1},
     "side": [],
     "source": SRC_SHEETS + ", Plan_accion P4; playbook sección 8"},

    # 28 playbook 12 reglas
    {"kind": "content", "tracker": "E. El plan",
     "title": "El playbook en 12 reglas evita que el desorden vuelva",
     "exhibit": {"type": "rules", "items": [
         "Una pieza se llama Ticket-Producto-Audiencia-Gancho. Sin ticket no se activa.",
         "No se le escribe a lista negra, REUS o ARCO, tarjeta congelada, dados de baja, WhatsApp fallido 3 veces ni a quien no respondió en 90 días.",
         "Máximo 2 toques de la misma pieza al mes. El segundo solo a quien no abrió el primero.",
         "Máximo 5 promocionales por semana, 2 piezas al día y 1 push al día.",
         "Se manda por el canal al que el usuario responde.",
         "WhatsApp solo a quien ya dio señal o a clientes activos. Nunca a bases frías.",
         "Nada a toda la base. Más de 1 millón: prueba al 10 % y un segmento.",
         "El gancho principal es recordar algo que el usuario empezó.",
         "Referidos, lanzamientos y novedades van en in-app, no por email.",
         "A las 4 semanas se revisa. Debajo del mínimo del canal se apaga o se rehace.",
         "Toda pieza lleva grupo de control del 10 % con la opción nativa de Braze.",
         "Un Canvas tiene máximo 8 pasos y el usuario entra una sola vez."]},
     "side": ["El playbook completo tiene tablas de consulta por tipo de mensaje, día, mes, segmento, equipo y producto, un checklist de activación y un resolvedor web que arma la pieza con cinco respuestas.",
              "Son sugerencias con datos, no reglas fijas: cada equipo las ajusta con sus pruebas."],
     "source": "Playbook de Braze para Kueski, versión 4"},

    # 29 qué mandar por tipo
    {"kind": "content", "tracker": "E. El plan",
     "title": "Qué mandar por tipo: el canal, el día y las veces ya están decididos con datos",
     "exhibit": {"type": "table", "head": ["Vas a mandar", "Canal", "Día", "Veces", "Control"],
                 "rows": [["Retargeting de algo empezado", "Email y push", "Martes a jueves", "2 en 7 días", "10 %"],
                          ["Bienvenida", "Email día 1, luego push e in-app", "El día que entra", "1 al día, 3 la primera semana", "10 %"],
                          ["Oferta de crédito (Tasa 0)", "Push a quien abrió push en 60 días; WhatsApp solo detrás", "Martes a jueves", "2 al mes", "10 %"],
                          ["Descuento o comercio KPay", "Push y WhatsApp a recurrentes", "Sábado WhatsApp; martes a jueves push", "2 por evento", "10 %"],
                          ["Referidos, lanzamiento, novedades", "In-app", "Cualquiera", "1", "10 %"],
                          ["Reactivación de fríos", "Push barato; WhatsApp solo con señal", "Martes a jueves", "3 en 30 días y sale 90", "10 %"],
                          ["Encuesta", "In-app o email", "Martes a jueves", "1", "No"],
                          ["Cobranza", "El del proceso", "Según el proceso", "Según el proceso", "No"]]},
     "side": [],
     "source": "Playbook de Braze para Kueski, sección 0"},

    # 30 configuración Braze
    {"kind": "content", "tracker": "E. El plan",
     "title": "Dieciocho ajustes de Braze que se configuran una vez y protegen todo lo demás",
     "exhibit": {"type": "table", "head": ["Ajuste", "Cómo se deja", "Por qué"],
                 "rows": [["Frequency capping global", "5 promocionales por semana, 2 piezas al día, 1 push al día, 1 WhatsApp al mes", "9 % de los usuario-días reciben 3 o más piezas"],
                          ["Grupo de control nativo", "10 % en toda pieza promocional, 5 % si pasa de 1 M, conversión a 7 días", "Hoy no hay ninguno"],
                          ["Horas de silencio", "21:00 a 9:00 hora del usuario", "No hay hora en Databricks; es la única protección"],
                          ["Re-elegibilidad", "Apagada en lifecycle y oferta", "Causa probable de 17 a 31 envíos de la misma pieza"],
                          ["Salida del Canvas", "Al convertir, al darse de baja o a los 30 días", "Hoy sigue mandando después de convertir"],
                          ["Caducidad del push", "24 horas promocional, 72 cobranza", "Un push de dos días después se abre como spam"],
                          ["Centro de preferencias", "7 grupos de suscripción y baja total en el pie", "3.1 bajas por mil; hoy la única opción es irse del todo"],
                          ["Calidad de WhatsApp", "Un número por tipo, plantillas con categoría correcta, pausa si baja la calidad", "1 de 4 no llega y se paga"],
                          ["Roles y permisos", "Editor crea, aprobador activa, nadie activa lo que creó", "171 pruebas llegaron a usuarios reales"],
                          ["Currents a Databricks", "Hora de envío, dispositivo, rebotes y quejas", "Hoy no se puede medir hora ni rebotes"]]},
     "side": ["Los otros 8: Intelligent Timing y Channel a prueba contra control, permiso de notificaciones in-app, dominio de email con SPF, DKIM y DMARC, Liquid con valor por defecto, prioridad de in-app, catálogos, MAU y puntos de datos, nombre y tags obligatorios."],
     "source": "Playbook de Braze para Kueski, sección 11"},

    # 31 gobierno
    {"kind": "content", "tracker": "E. El plan",
     "title": "Un dueño por cosa y un calendario único: así se sostiene",
     "exhibit": {"type": "table", "head": ["Qué", "Dueño", "Cómo"],
                 "rows": [["Nombres, tags, suscripciones, plantillas, exclusiones, frequency cap", "MarTech", "Nadie activa una pieza que no cumpla"],
                          ["Calendario y estándares", "CRM", "Una vista compartida: fecha, equipo, pieza, audiencia, canal, gancho, tamaño"],
                          ["Cada familia de segmentos", "Marketing (embudo), Lending (nuevos, activos, fríos), Sales (comercios), Collections (mora)", "Un segmento nuevo se pide en el ticket y lo aprueba el dueño"],
                          ["Cada pieza", "El ticket", "Un dueño, un evento de conversión, un grupo de control"],
                          ["Piezas a Todos, más de 1 M, cambios a exclusiones", "Comité quincenal de 30 minutos", "Se defienden con grupo de control, no con opinión"],
                          ["Excepciones", "Comité", "Con fecha de fin"],
                          ["Indicador en rojo dos meses seguidos", "El equipo que lo mueve", "Abre un ticket"]]},
     "side": ["Cada mes: semana 1 datos y lift, semana 2 plan de acción y limpieza, semana 3 calendario del mes siguiente, semana 4 piezas nuevas con checklist.",
              "Cada trimestre: archivar segmentos, tags y plantillas sin uso; actualizar el playbook."],
     "source": "Playbook de Braze para Kueski, sección 9"},

    # 32 roadmap
    {"kind": "content", "tracker": "E. El plan",
     "title": "Plan a 90 días: limpiar en 30, configurar en 60, medir en 90",
     "exhibit": {"type": "gantt", "cols": ["Semanas 1 y 2", "Semanas 3 y 4", "Mes 2", "Mes 3"],
                 "rows": [("Apagar 48 campañas y pausar 171 pruebas", [1, 0, 0, 0], "Cada equipo con MarTech"),
                          ("Confirmar 232 apagados y limpiar base de WhatsApp (56)", [1, 1, 0, 0], "MarTech"),
                          ("7 exclusiones como filtro negativo en todo lo promocional", [1, 1, 0, 0], "MarTech con Legal y Riesgo"),
                          ("Frequency cap, horas de silencio, TTL, re-elegibilidad", [0, 1, 0, 0], "MarTech"),
                          ("Rehacer 62 campañas activas con señal, 8 pasos y control", [0, 1, 1, 0], "Dueños con ticket"),
                          ("30 segmentos maestros, nombres y tags; roles de aprobación", [0, 1, 1, 0], "MarTech y dueños"),
                          ("Calendario único y comité quincenal", [0, 1, 1, 1], "CRM"),
                          ("Leer el lift a 4 semanas; apagar lo que da cero", [0, 0, 1, 1], "CRM con cada equipo"),
                          ("Primera prueba A/B por equipo (día, asunto, monto)", [0, 0, 1, 1], "Cada equipo"),
                          ("Hora, dispositivo y rebotes de Currents a Databricks", [0, 0, 1, 1], "Datos")]},
     "side": [],
     "source": "Plan de acción y playbook secciones 6, 9 y 11"},

    # 33 costo de no hacer nada
    {"kind": "content", "tracker": "E. El plan",
     "title": "No hacer nada cuesta 19 M MXN al año y 50 mil bajas al mes",
     "exhibit": {"type": "stats", "items": [
         ("19.2 M MXN", "al año en campañas con señal", "1.6 M al mes que ya se sabe que no responden"),
         ("50 mil", "bajas de email al mes", "457 mil usuario-mes en 9 meses; 2.2 % de la base"),
         ("14.2 M", "usuarios que no responden a nada", "siguen contando como MAU facturable si reciben algo"),
         ("0", "piezas con lift medido", "sin control, cada discusión sigue siendo de opinión"),
     ]},
     "side": ["Las bajas no se recuperan: cada usuario que se da de baja de email deja de ser alcanzable por el canal más barato.",
              "WhatsApp a números que no reciben degrada la calidad del número ante Meta y baja el tope diario.",
              "El costo fijo de Braze (MAU y puntos de datos) crece con usuarios que no responden."],
     "source": SRC_SHEETS + ", Plan_accion P2, B_Canales B2, J_Canal"},

    # 34 lo que no sabemos
    {"kind": "content", "tracker": "E. El plan",
     "title": "Lo que todavía no sabemos y qué dato lo resuelve",
     "exhibit": {"type": "table", "head": ["Pregunta", "Estado", "Qué hace falta"],
                 "rows": [["Cuánto vende Braze de verdad (lift)", "No medible hoy", "Grupos de control desde el día uno; se lee a las 4 semanas"],
                          ["Hora del día que funciona", "No medible", "Agregar hora del envío desde Currents; mientras, prueba A/B"],
                          ["iOS contra Android", "Sí se puede", "Correr la query E18c sobre braze.int_communications_joined"],
                          ["Rebotes y quejas de spam", "No están en Databricks", "Eventos de Currents"],
                          ["Tags", "No están en Databricks", "Exportar la lista de campañas con tags desde Braze"],
                          ["Banderas de contactabilidad del golden dataset", "No coinciden con el comportamiento", "Datos define fecha y fuente"],
                          ["Costo fijo de Braze", "Pendiente", "Significado de 7,020 USD al mes y 32,474 créditos"],
                          ["Región", "No está en ninguna tabla", "Atributo de usuario"]]},
     "side": [],
     "source": "Playbook y Sheets, pestaña Léeme"},

    # 35 próximos pasos
    {"kind": "content", "tracker": "E. El plan",
     "title": "Próximos pasos: quién hace qué esta semana",
     "exhibit": {"type": "table", "head": ["Qué", "Quién", "Cuándo"],
                 "rows": [["Aprobar el plan de acción por campaña (582) y el playbook", "Dirección y líderes de equipo", "Esta semana"],
                          ["Apagar las 48 campañas con señal y pausar las 171 pruebas", "Cada equipo con MarTech", "Semana 1"],
                          ["Cargar las 7 exclusiones y el frequency cap en Braze", "MarTech con Legal y Riesgo", "Semana 2"],
                          ["Nombrar dueños: MarTech, CRM y uno por familia de segmentos", "Dirección", "Semana 1"],
                          ["Confirmar el costo fijo de Braze y la base de cobro de WhatsApp", "Finanzas y MarTech", "Semana 1"],
                          ["Pedir a Datos hora, dispositivo y rebotes en Databricks", "CRM", "Semana 2"],
                          ["Primer comité quincenal con el calendario de noviembre", "CRM", "Semana 3"],
                          ["Primer corte mensual del Sheets con el plan ejecutado", "Datos y CRM", "Mes 2"]]},
     "side": [],
     "source": "Plan de acción"},

    # Anexo divider
    {"kind": "section", "num": "Anexo", "title": "Método, estándares y datos de apoyo", "subtitle": ""},

    # 36 método
    {"kind": "content", "tracker": "Anexo",
     "title": "Método: 18 extracciones agregadas de Databricks, un modelo en Sheets con fórmulas vivas y 471 verificaciones",
     "exhibit": {"type": "table", "head": ["Extracción", "Qué trae", "Lente"],
                 "rows": [["E1, E2", "Comunicación por mes y canal; catálogo", "Campañas, Catálogo, Plan_accion"],
                          ["E3, E4a, E4b", "Distribución por usuario; serie semanal y mensual; concentración", "Presión, canales"],
                          ["E5, E5b, E8", "Cohorte de baja; qué llega después; días hasta la baja", "Bajas"],
                          ["E6a, E6b", "Solape por usuario-día; pares de familias", "Solapamiento"],
                          ["E7a, E7b, E7c, E9", "Etapa del golden dataset; canal al que responde; abren contra no abren", "Segmentación"],
                          ["E10, E11, E12", "Día de la semana; segmentos reales; antigüedad", "N, P, O"],
                          ["E13, E14, E15", "Grupos de control; experimentos; pasos de Canvas", "Q, R, S"],
                          ["E16, E17, E18b", "Sin respuesta; canal contactable; llave de dispositivo", "T, U"]]},
     "side": ["Respuesta: clic en email, apertura en push, lectura en WhatsApp, clic en in-app.",
              "Familia: la pieza con todas sus versiones. Campaña: familia por canal.",
              "Costos: email 0.05 MXN por enviado, WhatsApp 1.00 por entregado (parámetro editable).",
              "Equipo, audiencia y gancho se leen del nombre; 17 % cae en 'otros'."],
     "source": SRC_SHEETS + ", Léeme, Parámetros, Verificación"},

    # 37 estándares completos
    {"kind": "content", "tracker": "Anexo",
     "title": "Estándares: los 24 indicadores con su valor actual",
     "exhibit": {"type": "table", "head": ["Indicador", "Hoy", "Estándar", "Estado", "Indicador", "Hoy", "Estándar", "Estado"],
                 "rows": [["Entrega de email", "95.1 %", "95 %", "Cumple", "Mensajes a canal mudo", "59 %", "20 %", "Debajo"],
                          ["Apertura de email", "23.6 %", "15 a 25 %", "Cumple", "Usuarios sin respuesta", "73 %", "50 %", "Debajo"],
                          ["Clic de email", "0.92 %", "1.5 %", "Debajo", "Promo a etapas bloqueadas", "43.8 M", "0", "Debajo"],
                          ["Bajas por mil", "3.13", "2.5", "Debajo", "Promo a dados de baja", "79,994", "0", "Debajo"],
                          ["Apertura de push", "1.53 %", "3 %", "Debajo", "Dados de baja que reciben email", "16 %", "10 %", "Debajo"],
                          ["Entrega de WhatsApp", "74 %", "90 %", "Debajo", "Email activo a 1 M o más", "0", "0", "Cumple"],
                          ["Lectura de WhatsApp", "69 %", "70 %", "Debajo por poco", "Activas debajo del mínimo", "85", "0", "Debajo"],
                          ["Clic de in-app", "38 %", "5 a 20 %", "Cumple", "Canvas con control", "0 de 3,228", "Todos", "Debajo"],
                          ["Toques por pieza al mes", "1.71", "2", "Cumple", "Envíos con ticket", "87 %", "100 %", "Debajo"],
                          ["Mensajes por usuario al mes", "10.4", "20", "Cumple", "Pruebas A/B en 9 meses", "0", "1 por equipo al mes", "Debajo"],
                          ["Usuarios con 41+ al mes", "5.3 %", "5 %", "Debajo", "Canvas con más de 8 pasos", "45 con más de 20", "0", "Debajo"],
                          ["Usuario-días con 3+ piezas", "9.0 %", "10 %", "Cumple", "Pasos con menos de 1 %", "477", "0", "Debajo"]],
                 "status_col": [3, 7], "small": True},
     "side": [],
     "source": SRC_SHEETS + ", Estándares"},

    # 38 por mes
    {"kind": "content", "tracker": "Anexo",
     "title": "Por mes: envíos, respuesta, bajas y costo",
     "exhibit": {"type": "table", "head": ["Mes", "Envíos", "Clic email", "Apertura push", "WhatsApp enviados", "Entrega WA", "Lectura WA", "Clic in-app", "Bajas (usuarios)", "Costo MXN"],
                 "rows": [["Ene", "58.7 M", "1.20 %", "1.83 %", "5.6 M", "80 %", "75 %", "48 %", "69,226", "7.4 M"],
                          ["Feb", "67.5 M", "0.88 %", "1.43 %", "7.8 M", "77 %", "73 %", "19 %", "57,965", "9.5 M"],
                          ["Mar", "67.8 M", "1.03 %", "1.81 %", "10.4 M", "74 %", "72 %", "24 %", "50,413", "12.2 M"],
                          ["Abr", "64.3 M", "0.98 %", "1.53 %", "5.9 M", "69 %", "66 %", "36 %", "38,422", "7.6 M"],
                          ["May", "85.0 M", "0.86 %", "1.28 %", "6.1 M", "67 %", "67 %", "47 %", "38,034", "8.1 M"],
                          ["Jun", "109.0 M", "0.67 %", "1.05 %", "7.1 M", "74 %", "67 %", "45 %", "63,425", "9.7 M"],
                          ["Jul", "71.7 M", "1.00 %", "1.77 %", "4.8 M", "73 %", "62 %", "37 %", "52,912", "6.4 M"],
                          ["Ago", "78.0 M", "0.95 %", "1.57 %", "4.4 M", "78 %", "64 %", "42 %", "50,340", "6.1 M"],
                          ["Sep", "65.6 M", "0.92 %", "2.12 %", "3.2 M", "77 %", "64 %", "42 %", "36,639", "5.0 M"]],
                 "highlight_rows": [5]},
     "side": [],
     "source": SRC_SHEETS + ", B_Canales B1 (E4a)"},

    # 39 por día
    {"kind": "content", "tracker": "Anexo",
     "title": "Por día de la semana: volumen, respuesta y bajas",
     "exhibit": {"type": "table", "head": ["Día", "Envíos", "% del total", "Clic email", "Bajas por mil", "Apertura push", "Entrega WA", "Lectura WA", "Conv. WA por mil"],
                 "rows": [["Domingo", "51.2 M", "7.7 %", "1.91 %", "7.7", "1.26 %", "87 %", "89 %", "56"],
                          ["Lunes", "124.0 M", "18.6 %", "0.65 %", "2.3", "1.63 %", "72 %", "66 %", "16"],
                          ["Martes", "113.6 M", "17.0 %", "0.82 %", "3.2", "1.56 %", "75 %", "67 %", "20"],
                          ["Miércoles", "92.2 M", "13.8 %", "1.01 %", "4.1", "1.63 %", "73 %", "70 %", "16"],
                          ["Jueves", "110.0 M", "16.5 %", "0.95 %", "3.6", "1.53 %", "75 %", "66 %", "15"],
                          ["Viernes", "111.7 M", "16.7 %", "0.82 %", "2.8", "1.64 %", "71 %", "70 %", "18"],
                          ["Sábado", "64.7 M", "9.7 %", "1.58 %", "5.5", "1.44 %", "82 %", "82 %", "34"]],
                 "highlight_rows": [1]},
     "side": ["Clic de email por equipo y día: Marketing 1.00 % lunes contra 1.66 % domingo; Product Growth 0.29 % lunes contra 1.53 % domingo; Sales 0.15 a 0.38 % todos los días.",
              "Compara la misma pieza en dos días antes de concluir."],
     "source": SRC_SHEETS + ", N_DiaSemana (E10)"},

    # 40 segmentos
    {"kind": "content", "tracker": "Anexo",
     "title": "Segmentos registrados en Braze: pocos concentran el volumen y 13 % no se rastrea",
     "exhibit": {"type": "hbar", "cats": ["Leads", "Recurrent", "Not Tracked", "New", "Todos", "BKT1", "Active", "Precobranza", "Anonimos"],
                 "vals": [201, 189, 84.7, 67, 24.5, 18, 15, 12, 9.3], "fmt": "M", "label": "Envíos por segmento (M)",
                 "notes": ["8.5 % respuesta, 3.5 conv por mil", "7.0 %, 12.5 conv por mil", "no se mide", "2.1 %", "", "1.5 %", "21 %, 50 conv por mil", "45 conv por mil", "0.8 %"],
                 "highlight": [2]},
     "side": ["41 valores de segmento, 330 de subsegmento y 62 de grupo forman 481 combinaciones. El subsegmento se usa como nombre de la oferta, no como audiencia.",
              "Lo mismo escrito de varias formas: Comercio del día en 11 valores, Cuponera en 8, SoftInactive con error de dedo.",
              "Propuesta: 30 segmentos maestros SEG-Producto-Audiencia con dueño y 7 exclusiones EXC-."],
     "source": SRC_SHEETS + ", P_Segmentos (E11)"},

    # 41 supuestos
    {"kind": "content", "tracker": "Anexo",
     "title": "Supuestos y dónde está cada cosa",
     "exhibit": {"type": "table", "head": ["Supuesto", "Detalle"],
                 "rows": [["Periodo", "1 de enero a 30 de septiembre de 2026, 273 días"],
                          ["Respuesta", "Clic en email, apertura en push, lectura en WhatsApp, clic en in-app. Abrir un email no cuenta"],
                          ["Conversión", "A 7 días, como referencia, no como atribución"],
                          ["Costos", "Email 0.05 MXN por enviado, WhatsApp 1.00 por entregado, push e in-app 0, sin costo fijo de Braze"],
                          ["Audiencia, gancho y tipo", "Se leen del nombre de la pieza; 17 % cae en 'otros'"],
                          ["Etapas", "Golden dataset cubre 37 % de los envíos; banderas a la fecha de la extracción"],
                          ["Bajas", "Solo existen para email. 457 mil usuario-mes, 439 mil usuarios únicos"],
                          ["Control, experimentos, pasos", "Solo Canvas (3,228); un usuario cuenta una vez por Canvas, grupo o paso"],
                          ["Antigüedad", "days_on_book a la fecha de la extracción menos los días desde el envío; 1.1 % con alta posterior al envío"]]},
     "side": ["Sheets braze_auditoria_v4: Léeme, Parámetros, Vista_equipo, Insights, Plan_accion, Estándares, Catálogo, Campañas, lentes B a U, extracciones E1 a E18b y Verificación (471 filas).",
              "Playbook: PLAYBOOK_BRAZE_KUESKI (md, docx y versión web con resolvedor).",
              "Análisis de apoyo: ANALISIS_BRAZE_KUESKI.md."],
     "source": SRC_SHEETS + ", Léeme y Parámetros"},
]


# "So what" de cada lámina: qué significa y qué se hace. Clave = número de lámina.
SOWHAT = {
    2: "Decisión que se pide hoy: aprobar el plan por campaña y el playbook, y nombrar un dueño de Braze. El ahorro empieza en la semana 1.",
    3: "Las cifras salen de datos agregados de toda la base, no de muestras: lo que se decida aquí se ejecuta y se mide campaña por campaña.",
    4: "El dinero está en WhatsApp y las bajas en email: la limpieza empieza por WhatsApp y la frecuencia se baja primero en email.",
    5: "Subir volumen no sube resultados, los baja. Ningún envío a más de 1 M de usuarios sin prueba al 10 % y un segmento con criterio.",
    6: "No es un problema de una campaña ni de un equipo: es la forma de operar Braze. Se corrige con reglas y configuración, no pieza por pieza.",
    8: "Dejar de mandar a los 14.2 M que nunca respondieron no cuesta ventas (convierten 0.08 %). Es la primera exclusión que se carga en Braze.",
    9: "Mandar por el canal que el usuario sí abre ahorra 18.7 M MXN en 9 meses sin perder respuesta. Requiere un atributo en Braze: canal_preferido_90d.",
    10: "Exclusión EXC-SinRespuesta90d en todo lo promocional: ahorra unos 900 mil MXN al mes y 17 % de las bajas sin perder una sola conversión.",
    11: "Son mensajes que no debían salir y un riesgo legal. Las 7 exclusiones se cargan en Braze esta semana; Legal decide sobre REUS y ARCO.",
    12: "Exclusión EXC-WA_SinEntrega3 en toda pieza de WhatsApp: deja de pagar por números que no reciben y protege la calidad del número ante Meta.",
    14: "Frequency cap global en Braze (5 promocionales por semana, 1 push al día): recorta la cola de 41 o más y saca a los usuarios de la banda donde la baja se multiplica por 13.",
    15: "El problema no son 90 mil usuarios con 8 campañas: son 2 a 3 M con dos piezas el mismo día, casi siempre del mismo equipo. Calendario único por equipo antes que reglas entre equipos.",
    16: "Una sola secuencia de bienvenida (1 email al día, 3 la primera semana) y ningún masivo a menores de 30 días: protege al segmento que mejor responde.",
    17: "Máximo 8 pasos y 2 toques por canal: los 477 pasos que abren menos de 1 % se apagan sin perder respuesta, porque insistir no la sube.",
    18: "El lunes es el día de los masivos sin segmento (23 % del email). Antes de mover el calendario, la siguiente lámina muestra que el tamaño de la pieza explica el clic, no el día.",
    19: "A más de 1 año sin respuesta en 90 días, fuera de lo promocional: ahí está el 56 % del volumen con la respuesta más baja.",
    21: "El gancho que vende es recordar lo que el usuario empezó. Tasa 0 se reduce a una pieza por audiencia; referidos y lanzamientos pasan a in-app.",
    22: "Lo informativo va en in-app, el push es el primer toque, el email lleva un solo llamado a la acción y WhatsApp nunca abre la conversación.",
    23: "Audiencias de 10 a 100 mil con un criterio y 2 toques: más de 1 M obliga a prueba al 10 % y el tercer toque desaparece.",
    24: "Cada equipo escala el canal que le funciona y apaga el que le cuesta: la regla de canal se fija por equipo, no una para toda la empresa.",
    25: "Estas 10 piezas son 19 % del volumen: su acción (apagar, rehacer, bajar frecuencia) se decide esta semana con el dueño de cada una.",
    27: "Mientras no haya control del 10 % en toda pieza, ninguna cifra de conversión justifica mantener una campaña. Se activa en Braze en una semana.",
    28: "Sin ticket ni nombre estándar no hay dueño ni auditoría: regla de nombres y tags de lista cerrada obligatorios desde la próxima pieza.",
    30: "Aprobar el plan por campaña: 1.6 M MXN al mes es un techo, pero apagar las 48 con señal ya vale 1.16 M al mes y se hace en 30 días.",
    31: "Product Growth decide primero: 17 campañas a apagar valen 1.04 M MXN al mes. Marketing limpia la base de WhatsApp; Sales rehace su email.",
    32: "Cada pieza tiene dueño y acción: se ejecuta en las semanas 1 y 2 del plan sin esperar la configuración de Braze.",
    33: "Las 12 reglas son el estándar de activación: ninguna pieza nueva sale sin cumplirlas (checklist de la sección 7 del playbook).",
    34: "El equipo ya no decide canal, día ni frecuencia pieza por pieza: lo toma de esta tabla y solo prueba lo que quiera cambiar.",
    35: "Los 10 primeros ajustes se configuran en la semana 2 y protegen todo aunque una pieza salga mal: tope de frecuencia, control, silencio y exclusiones.",
    36: "Sin dueño no se sostiene: Dirección nombra esta semana a MarTech, CRM y un dueño por familia de segmentos.",
    37: "Limpiar en 30 días captura el ahorro grande; configurar en 60 evita que vuelva; medir en 90 permite demostrar cuánto vende Braze.",
    38: "Cada mes sin actuar cuesta 1.6 M MXN y 50 mil usuarios que dejan de ser alcanzables. La decisión es esta semana, no el próximo trimestre.",
    39: "Tres datos (hora, dispositivo, rebotes) y el costo fijo de Braze cierran lo que falta: se piden a Datos y Finanzas en las semanas 1 y 2.",
    40: "Ocho acciones con dueño y fecha: si se aprueban hoy, el ahorro empieza en la semana 1.",
    42: "Todo es reproducible: cambiar un parámetro (por ejemplo el costo de WhatsApp) recalcula el plan completo.",
    43: "Los estándares son editables: cambiarlos cambia el semáforo de toda la auditoría, no las conclusiones.",
    44: "Junio es el mes de referencia de lo que no se debe repetir; septiembre, de lo que sí.",
    45: "El día importa menos que la pieza y la audiencia: compara la misma pieza en dos días antes de mover el calendario.",
    46: "30 segmentos maestros con dueño sustituyen 481 combinaciones: así los segmentos y tags se pueden auditar.",
    47: "Sheets, playbook y análisis se actualizan juntos cada mes y viven en el mismo repositorio.",
}
for _i, _t in SOWHAT.items():
    SLIDES[_i - 1]["sowhat"] = _t


# ---- Láminas nuevas con gráficas multivariable ---------------------------------
def _short(name):
    parts = [q for q in name.split("-")[5:] if q and q.upper() not in ("N/A", "NA", "CANVAS", "E", "FULL_ROLLOUT")]
    tail = parts[-1] if parts else name
    if len(tail) <= 6 and len(parts) >= 2:
        tail = parts[-2] + " " + tail
    return tail.replace("_", " ")[:24]


_SP = DD.scatter_piezas()


def _short2(name):
    import re
    toks = [q for q in name.split("-")[2:] if q and q.upper() not in ("N/A", "NA", "CANVAS", "E", "FULL_ROLLOUT", "MAIL")
            and not re.fullmatch(r"\d{6,8}|[A-Z]\d{3,4}", q)]
    if not toks:
        return name[:24]
    tail = toks[-1]
    if len(tail) <= 13 and len(toks) >= 2:
        tail = toks[-2] + " " + tail
    return tail.replace("_", " ")[:26]


def _labels(pts, k=3, thr=None):
    out = []
    if thr is None:
        pick = sorted(pts, key=lambda q: -q["x"])[:k]
    else:
        pick = sorted([p for p in pts if p["y"] >= thr], key=lambda q: -q["x"])[:2] + sorted([p for p in pts if p["y"] < thr], key=lambda q: -q["x"])[:1]
    for i, p in enumerate(pick):
        out.append((_short2(p["name"]), p["x"], p["y"], -7, -8 if i % 2 == 0 else 15))
    return out


def _above(pts, std):
    return sum(1 for p in pts if p["y"] >= std), len(pts)


_ae, _ne = _above(_SP["email"], 1.5)
_ap, _np = _above(_SP["push"], 3.0)


def _bands(pts, thr):
    out = []
    for lo, hi, lab in ((2e5, 1e6, "200 mil a 1 M"), (1e6, 5e6, "1 a 5 M"), (5e6, 2e7, "más de 5 M")):
        b = [p for p in pts if lo <= p["x"] < (hi if hi < 2e7 else 1e12)]
        out.append((lo, hi, f"{sum(1 for p in b if p['y'] >= thr)} de {len(b)} pasan"))
    return out


def _fail_share(pts, thr):
    tot = sum(p["x"] for p in pts); totr = sum(p["x"] * p["y"] for p in pts)
    fl = [p for p in pts if p["y"] < thr]
    return 100 * sum(p["x"] for p in fl) / tot, 100 * sum(p["x"] * p["y"] for p in fl) / totr


_fe_v, _fe_r = _fail_share(_SP["email"], 1.5)
_fp_v, _fp_r = _fail_share(_SP["push"], 3.0)
_SCATTER = {"kind": "content", "tracker": "C. Qué funciona",
    "title": f"Solo {_ae} de {_ne} piezas de email y {_ap} de {_np} de push pasan el mínimo, y las que pasan existen en todos los tamaños: las {_ne-_ae} que no pasan son {_fe_v:.0f} % del volumen de email y {_fe_r:.0f} % de los clics",
    "exhibit": {"type": "scatter", "mode": "pass", "groups": DD.TEAMS, "panels": [
        {"title": f"Email: clic por pieza. En verde las {_ae} que pasan 1.5 %", "pts": _SP["email"], "ymax": 4.0, "fmt": "pct1", "ref": (1.5, "Mínimo 1.5 %"), "labels": _labels(_SP["email"], 2, 1.5), "bands": _bands(_SP["email"], 1.5)},
        {"title": f"Push: apertura por pieza. En verde las {_ap} que pasan 3 %", "pts": _SP["push"], "ymax": 8.0, "fmt": "pct1", "ref": (3.0, "Mínimo 3 %"), "labels": _labels(_SP["push"], 2, 3.0), "bands": _bands(_SP["push"], 3.0)},
    ]},
    "kpis": [(f"{_ae} de {_ne}", "piezas de email pasan el mínimo de 1.5 %"), (f"{_ap} de {_np}", "piezas de push pasan el mínimo de 3 %"), (f"{_fe_v:.0f} % / {_fe_r:.0f} %", "del volumen y de los clics de email están en piezas que no pasan")],
    "side": ["Cada punto es una pieza con 200 mil o más entregados (email) o enviados (push). Verde: pasa el mínimo del canal; gris: no pasa. Debajo de cada panel, cuántas pasan en cada banda de tamaño.",
             "Pasan piezas chicas y grandes (Veriff con 9.7 M, Precobranza, Payment Confirmation): lo que las separa es que van a quien ya hizo algo, no su tamaño.",
             f"Las {_ne-_ae} piezas de email que no pasan concentran {_fe_v:.0f} % del volumen y aportan {_fe_r:.0f} % de los clics; en push, las {_np-_ap} que no pasan son {_fp_v:.0f} % del volumen y {_fp_r:.0f} % de las aperturas."],
    "source": SRC_SHEETS + ", Campañas (E1). Escala horizontal logarítmica; puntos arriba del tope se dibujan en el tope",
    "sowhat": "No hay piezas grandes malas y piezas chicas buenas: hay piezas con señal y piezas sin señal. El criterio para apagar es la respuesta contra el mínimo a las 4 semanas, no el tamaño."}

_DE = DD.dispersion_equipo("email")
_DP = {e["cat"]: e for e in DD.dispersion_equipo("push notification")}
_DISP = {"kind": "content", "tracker": "C. Qué funciona",
    "title": "Dentro de cada equipo la respuesta varía más que entre equipos: Marketing promedia 0.62 % de clic con una desviación de 1.09 puntos; Sales, 0.20 % con 0.14",
    "exhibit": {"type": "dotrange", "fmt": "pct2", "xmax": 3.0, "ref": (1.5, "Mínimo 1.5 %"),
                "label": "Clic de email por pieza (100 mil o más envíos), por equipo",
                "rows": [{"cat": e["cat"], "n": e["n"], "mean": e["mean"], "sd": e["sd"], "median": e["median"], "pts": e["pts"]} for e in _DE]},
    "side": ["Promedio simple por pieza. Ponderado por volumen: Marketing 0.89 %, Product Growth 0.40 %, Sales 0.20 %, Collections 1.05 %.",
             f"Push (apertura): Product Growth {_DP['Product Growth']['mean']:.2f} % ± {_DP['Product Growth']['sd']:.2f}, Marketing {_DP['Marketing']['mean']:.2f} % ± {_DP['Marketing']['sd']:.2f}, Sales {_DP['Sales']['mean']:.2f} % ± {_DP['Sales']['sd']:.2f}, Collections {_DP['Collections']['mean']:.2f} % ± {_DP['Collections']['sd']:.2f}.",
             "Sales no tiene una sola pieza de email arriba de 0.6 %: su email se rehace o se apaga, no se optimiza. La mitad de las piezas de Marketing y Product Growth está debajo de 0.32 % y 0.25 %."],
    "source": SRC_SHEETS + ", Campañas (E7a). Desviación estándar poblacional entre piezas; puntos arriba de 3 % se dibujan en el tope",
    "sowhat": "La palanca no es cambiar de equipo sino replicar las piezas de arriba de cada equipo y apagar su cola: cada equipo ya tiene piezas que pasan el mínimo y sabe cómo se ven."}



# ---- Bloque 2: regresión, campana, velas, semanas, cascada, segmentos, mudos ----
def _after(substr, *new):
    """Inserta láminas después de la primera cuyo título contiene substr."""
    for i, s in enumerate(SLIDES):
        if substr in s.get("title", ""):
            for k, n in enumerate(new):
                SLIDES.insert(i + 1 + k, n)
            return
    raise KeyError(substr)


_RS = DD.regresion_semana()
_RD = DD.regresion_dia()
_HI = DD.distribucion_piezas()
_VE = DD.velas_mes()
_SI = DD.semanas_indexadas()
_UC = DD.usuarios_cascada()
_SG = DD.segmentos_canal()
_MU = DD.mudos_mes()


def _wk(pts, key):
    q = max(pts, key=key)
    return (f"Sem. {q['lab']}", q["x"], q["y"])


_fe, _fp, _fw = _RS["email"]["fit"], _RS["push notification"]["fit"], _RS["whatsapp"]["fit"]
_e_hi = max(_RS["email"]["pts"], key=lambda q: q["x"]); _e_lo = min(_RS["email"]["pts"], key=lambda q: q["x"])
_p_hi = max(_RS["push notification"]["pts"], key=lambda q: q["x"])
for _c in _RS:
    for _q in _RS[_c]["pts"]:
        _q["mk"] = "d" if _q["g"] == "Jun" else "o"
_REG_SEM = {"kind": "content", "tracker": "Contexto",
    "title": f"Cada millón de emails más en la semana baja el clic {abs(_fe['b']):.2f} puntos y cada millón de push baja la apertura {abs(_fp['b']):.2f}: el volumen semanal explica {100*_fe['r2']:.0f} % y {100*_fp['r2']:.0f} % de la respuesta",
    "exhibit": {"type": "regress", "marker_note": "Rombos: semanas de junio", "panels": [
        {"title": "Email: enviados en la semana contra clic", "pts": _RS["email"]["pts"], "fit": _fe, "xmin": 0, "xmax": 27, "ymax": 1.6, "fmt": "pct1",
         "xticks": [(5, "5 M"), (10, "10 M"), (15, "15 M"), (20, "20 M"), (25, "25 M")], "xlab": "Emails enviados en la semana",
         "eq": f"clic = {_fe['a']:.2f} − {abs(_fe['b']):.3f} × millones   R² = {_fe['r2']:.2f}   n = {_fe['n']}",
         "labels": [(f"Sem. {_e_hi['lab']}: {_e_hi['x']:.0f} M, {_e_hi['y']:.2f} %", _e_hi["x"], _e_hi["y"], -8, -8), (f"Sem. {_e_lo['lab']}", _e_lo["x"], _e_lo["y"], 8, -8)]},
        {"title": "Push: enviados en la semana contra apertura", "pts": _RS["push notification"]["pts"], "fit": _fp, "xmin": 0, "xmax": 14, "ymax": 3.0, "fmt": "pct1",
         "xticks": [(2, "2 M"), (4, "4 M"), (6, "6 M"), (8, "8 M"), (10, "10 M"), (12, "12 M")], "xlab": "Push enviados en la semana",
         "eq": f"apertura = {_fp['a']:.2f} − {abs(_fp['b']):.3f} × millones   R² = {_fp['r2']:.2f}   n = {_fp['n']}",
         "labels": [(f"Sem. {_p_hi['lab']}: {_p_hi['x']:.0f} M", _p_hi["x"], _p_hi["y"], -8, -8)]}],
        "note": "Regresión lineal por mínimos cuadrados sobre las 38 semanas completas (5 de enero a 21 de septiembre). Cada punto es una semana."},
    "side": [f"Con 5 M de emails en la semana el modelo espera {_fe['a']+_fe['b']*5:.2f} % de clic; con 25 M, {_fe['a']+_fe['b']*25:.2f} %. La semana del 1 de junio (BillPay Intro a 16 M) es el extremo, no la excepción: sin ella el R² es similar.",
             f"WhatsApp no depende del volumen (R² = {_fw['r2']:.2f}): su lectura cayó de 74 % a 64 % por tendencia, no por cantidad. Ahí el problema es la base, no la frecuencia.",
             "Es correlación en datos agregados, no un experimento. El mecanismo es conocido: las semanas grandes son las de masivos sin segmento, que responden 0.1 a 0.3 %."],
    "source": SRC_SHEETS + ", Serie semanal (E4a). Tasa sobre entregados (email) y sobre enviados (push)",
    "sowhat": "Tope semanal de volumen: ninguna semana arriba de 10 M de emails ni de 8 M de push sin aprobación del comité. Es la regla más simple y recupera 0.3 puntos de clic."}

_IC = DD.semanas_indexadas_canal()
_IDX = {"kind": "content", "tracker": "Contexto",
    "title": "Semana a semana: push triplicó su volumen la semana del 15 de junio y su apertura cayó a la mitad; email solo se disparó la semana del 1 de junio y WhatsApp lleva desde julio entre 80 y 87 % de la respuesta de enero",
    "exhibit": {"type": "idxgrid", "cats": _IC["cats"], "cells": _IC["cells"], "ymax": 360, "cat_every": 6,
                "note": "Índice: promedio de las 4 semanas de enero = 100, por canal. Línea de color = volumen; línea gris = respuesta (clic, apertura, lectura, clic). 38 semanas completas."},
    "side": ["Un panel por canal y el mismo eje en los cuatro: así se compara el push (3.4 veces enero) con el email (1.1 veces) sin que uno aplaste al otro.",
             "Push: el pico de volumen (342) y el mínimo de apertura (51) caen en la misma semana, la del 15 de junio. La siguiente lámina dice qué piezas fueron.",
             "Email: fuera de la semana del 1 de junio (313, BillPay Intro a 16 M) el volumen se mueve entre 64 y 148 y el clic entre 57 y 129.",
             "WhatsApp: el volumen baja desde marzo y la respuesta no se recupera (80 en agosto): el problema es a quién se manda, no cuánto."],
    "source": SRC_SHEETS + ", F_Serie semanal (E4a). Semanas completas del 5 de enero al 21 de septiembre",
    "hipotesis": "Si la respuesta cae por fatiga del canal, debería recuperarse cuando baja el volumen.",
    "causa": "Push sí se recupera (julio: volumen 185, apertura 107): la causa fueron las piezas nuevas de junio. WhatsApp no se recupera con menos volumen: la causa es la audiencia (leads rezagados y churn), no la cantidad.",
    "sowhat": "El push se recupera con solo bajar volumen (ya pasó en julio); WhatsApp no. Por eso el plan apaga volumen en push y cambia la base en WhatsApp: son palancas distintas."}
_VEL = {"kind": "content", "tracker": "Contexto",
    "title": "Dentro de un mes la respuesta se mueve más que entre meses: en junio el clic de email abrió en 0.36 % y cerró en 1.00 %; push cerró septiembre 0.5 puntos debajo de donde abrió",
    "exhibit": {"type": "candle", "cells": [
        {"title": "Email: clic sobre entregados", "cats": MESES, "ohlc": _VE["email"], "fmt": "pct2"},
        {"title": "Push: apertura", "cats": MESES, "ohlc": _VE["push notification"], "fmt": "pct2"},
        {"title": "WhatsApp: lectura sobre entregados", "cats": MESES, "ohlc": _VE["whatsapp"], "fmt": "pct0"},
        {"title": "In-app: clic sobre impresiones", "cats": MESES, "ohlc": _VE["in-app"], "fmt": "pct0"}]},
    "side": ["Cada vela resume las 4 o 5 semanas del mes: apertura = primera semana, cierre = última, mecha = máximo y mínimo semanal.",
             "Email: la mecha de junio (0.36 a 1.14 %) es más larga que todo el movimiento de enero a septiembre. El promedio mensual (0.6 %) no describe ninguna semana.",
             "WhatsApp: ocho de nueve velas cierran igual o abajo de donde abrieron; es una tendencia, no ruido semanal.",
             "In-app: mechas largas (febrero 16 a 38 %) porque pocas piezas grandes cambian la tasa del canal."],
    "source": SRC_SHEETS + ", Serie semanal (E4a). Semanas asignadas al mes de su lunes; 38 semanas completas",
    "sowhat": "Medir y decidir por semana, no por mes: una semana de masivo hunde la respuesta y la siguiente se recupera. El tablero del playbook es semanal por canal."}

_ct = _UC["conv_tot"]
_CAS = {"kind": "content", "tracker": "A. A quien no responde",
    "title": f"{_UC['multi']/1e6:.1f} M usuarios que responden a 2 o más canales ({100*_UC['multi']/_UC['tot']:.0f} % de la base) concentran {100*_UC['conv']['multi']/_ct:.0f} % de las conversiones; los {_UC['none']/1e6:.1f} M que nunca respondieron, {100*_UC['conv']['none']/_ct:.0f} %",
    "exhibit": {"type": "waterfall", "fmt": "M", "unit": " M", "label": "Usuarios (M), según a cuántos canales respondieron en 9 meses",
                "cats": ["Usuarios en la base", f"Nunca respondieron ({100*_UC['conv']['none']/_ct:.0f} % de las conversiones)", f"Respondieron a 1 canal ({100*_UC['conv']['one']/_ct:.0f} %)", f"Responden a 2 o más canales ({100*_UC['conv']['multi']/_ct:.0f} %)"],
                "vals": [_UC["tot"] / 1e6, -_UC["none"] / 1e6, -_UC["one"] / 1e6, _UC["multi"] / 1e6],
                "note": f"Conversiones en el periodo: {_ct/1e6:.2f} M usuarios. Mensajes: {_UC['msgs']['none']/1e6:.0f} M a mudos, {_UC['msgs']['one']/1e6:.0f} M a un canal, {_UC['msgs']['multi']/1e6:.0f} M a varios"},
    "side": [f"Los {_UC['none']/1e6:.1f} M mudos recibieron {_UC['msgs']['none']/1e6:.0f} M mensajes ({100*_UC['msgs']['none']/sum(_UC['msgs'].values()):.0f} % del total) y convirtieron {_UC['conv']['none']/1e3:.0f} mil: {100*_UC['conv']['none']/_UC['none']:.2f} % de ellos.",
             f"Quien responde a 2 o más canales convierte {100*_UC['conv']['multi']/_UC['multi']:.0f} % en el periodo; quien responde a uno, {100*_UC['conv']['one']/_UC['one']:.1f} %.",
             "La conversión es de Databricks (solicitud o préstamo), no de Braze: por eso no se puede atribuir a un mensaje, pero sí decir a quién no conviene escribirle."],
    "source": SRC_SHEETS + ", Patrón de respuesta (E7b). Respuesta: clic de email o in-app, apertura de push, lectura de WhatsApp",
    "sowhat": "La base útil para promocional son 5.3 M usuarios, no 19.5 M. Toda audiencia promocional se construye desde quien ya respondió a algo; los mudos solo reciben transaccional y una prueba de reactivación al trimestre."}

_MUD = {"kind": "content", "tracker": "A. A quien no responde",
    "title": "La parte del email que va a quien nunca respondió no baja: 14 a 16 % cada mes y 33 % en junio; push sí mejoró, de 15 % en enero a 5 % en septiembre",
    "exhibit": {"type": "multiline", "cats": MESES, "series": _MU["share"], "fmt": "pct0", "ymin": 0, "ymax": 40, "highlight": [5, 8],
                "label": "% de los envíos del mes que fueron a usuarios que nunca respondieron en 9 meses, por canal",
                "note": f"Costo en el periodo de esos envíos: email {_MU['costo']['Email']:.1f} M MXN, WhatsApp {_MU['costo']['WhatsApp']:.1f} M MXN, push 0"},
    "side": ["Push bajó de 15 a 5 % sin ninguna regla: es el canal donde los equipos ya segmentan por señal (quien abrió). Es la prueba de que la exclusión funciona.",
             "Email no cambia porque los masivos a toda la base y las secuencias de bienvenida no filtran por respuesta; junio es BillPay Intro.",
             "WhatsApp se mueve entre 6 y 16 % según el mes: cada punto son 1.00 MXN por mensaje entregado a alguien que nunca ha leído uno."],
    "source": SRC_SHEETS + ", R_SinRespuesta (E16). Mudo: sin clic, apertura ni lectura en ningún canal en los 9 meses",
    "sowhat": "Esta curva es el indicador de la exclusión EXC-SinRespuesta90d: la meta es email y WhatsApp debajo de 5 % en 60 días, como ya está push."}

_he = _HI["email"]
_lin_lab = [("0" if i == 0 else f"{e:.0f} %" if e == int(e) else "") for i, e in enumerate(_he["edges"][:-1])]
_lin_lab[-1] = ""
_log_lab = ["0.01 %", "", "", "", "0.1 %", "", "", "", "1 %", "", "", "", "10 %", ""]
_CAMP = {"kind": "content", "tracker": "C. Qué funciona",
    "title": f"La respuesta por pieza no es una campana: la mitad de las piezas de email está debajo de {_he['median']:.2f} % y el promedio de {_he['mean']:.2f} % lo infla el 10 % de piezas arriba de {_he['p90']:.1f} %",
    "exhibit": {"type": "hist", "cells": [
        {"title": f"Email: clic por pieza-mes, escala lineal (n = {_he['n']})", "counts": _he["counts"], "normal": _he["normal"], "xlabels": _lin_lab,
         "marks": [(f"Mediana {_he['median']:.2f} %", _he["median"] / 0.25, 0), (f"Promedio {_he['mean']:.2f} %", _he["mean"] / 0.25, 16), ("Mínimo 1.5 %", 6, 32)],
         "xlab": "Clic sobre entregados (último rango: 3.75 % o más)", "note": f"Desviación estándar {_he['sd']:.2f} puntos: 2 veces el promedio"},
        {"title": "Email: la misma distribución en escala logarítmica", "counts": _he["lcounts"], "normal": _he["lnormal"], "xlabels": _log_lab,
         "marks": [(f"Centro {10**_he['lmean']:.2f} %", (_he["lmean"] + 2) / 0.25, 0), ("Mínimo 1.5 %", (0.1761 + 2) / 0.25, 16)],
         "xlab": "Clic sobre entregados (cada rango multiplica por 1.8)", "note": "Aquí sí es una campana: la respuesta es log-normal"}]},
    "side": [f"Piezas-mes de email con 100 mil o más entregados. {_he['share_under'][0.5]:.0f} % están debajo de 0.5 %; {_he['share_under'][1.5]:.0f} % debajo del mínimo de 1.5 %.",
             f"Push (apertura, n = {_HI['push']['n']}): mediana {_HI['push']['median']:.2f} %, promedio {_HI['push']['mean']:.2f} %, {_HI['push']['share_under'][3.0]:.0f} % debajo del mínimo de 3 %.",
             "Que sea log-normal significa que las mejoras se miden en múltiplos, no en puntos: pasar de 0.3 a 0.6 % es el mismo salto que de 1.5 a 3 %."],
    "source": SRC_SHEETS + ", Campañas (E1). Campana: normal con el mismo promedio y desviación que los datos",
    "sowhat": f"Las metas se fijan con la mediana, no con el promedio: una pieza 'promedio' no existe. El mínimo de 1.5 % ya lo pasan {_he['n']-int(_he['n']*_he['share_under'][1.5]/100)} piezas-mes: es exigente, no imposible."}

_dd = _RD["dias"]
_pt = {(q["dia"], q["g"]): q for q in _RD["pts"]}
def _lab(d, t, dx, dy):
    q = _pt[(d, t)]
    return (f"{d} {t}: {q['x']/1e3:.0f} mil por pieza, {q['y']:.2f} %", q["x"], q["y"], dx, dy)
_REG_DIA = {"kind": "content", "tracker": "B. Demasiado y sin coordinación",
    "title": f"El fin de semana responde más porque cada pieza llega a 5 veces menos gente ({_dd['Dom']['tam']/1e3:.0f} mil el domingo contra {_dd['Lun']['tam']/1e3:.0f} mil el lunes), no por el día: el tamaño por pieza explica {100*_RD['fit']['r2']:.0f} % del clic en los equipos promocionales",
    "exhibit": {"type": "regress", "groups": DD.TEAMS, "marker_note": "Rombos: sábado y domingo. Círculos: lunes a viernes", "panels": [
        {"title": "Clic de email según usuarios alcanzados por pieza, por día y equipo (34 celdas)", "pts": _RD["pts"], "fit": _RD["fit"], "xlog": True,
         "xmin": 3000, "xmax": 300000, "ymax": 3.5, "fmt": "pct1", "fit_filter": lambda q: q["g"] in ("Product Growth", "Marketing", "Sales"),
         "xticks": [(5000, "5 mil"), (10000, "10 mil"), (25000, "25 mil"), (50000, "50 mil"), (100000, "100 mil"), (250000, "250 mil")],
         "xlab": "Envíos del día entre piezas distintas que salieron ese día (escala logarítmica)",
         "eq": f"Recta: Product Growth, Marketing y Sales. R² = {_RD['fit']['r2']:.2f}   n = {_RD['fit']['n']}",
         "labels": [_lab("Dom", "Product Growth", 8, 4), _lab("Lun", "Product Growth", 8, 14), _lab("Lun", "Marketing", 8, -6), _lab("Lun", "Collections", -8, -8)]}]},
    "side": [f"Cada día salen casi las mismas piezas ({_dd['Sáb']['piezas']:.0f} a {_dd['Mié']['piezas']:.0f}): los Canvas corren diario. Lo que cambia es que los masivos a toda la base salen entre semana, sobre todo el lunes ({_dd['Lun']['env']:.0f} M de envíos contra {_dd['Dom']['env']:.0f} M el domingo).",
             f"Por usuario también: {_dd['Lun']['por_usuario']:.1f} emails el lunes contra {_dd['Dom']['por_usuario']:.1f} el domingo. El cruce entre familias por día de la semana no está en las extracciones (E6a es mensual); este es su proxy.",
             "Collections es plano todos los días (transaccional, 200 mil por pieza, 1 %) y Others mezcla todo: por eso quedan fuera de la recta. Con los 34 puntos el R² cae a 0.02."],
    "source": SRC_SHEETS + ", N_DiaSemana (E10). Celdas con 50 mil o más entregados; recta por mínimos cuadrados sobre el logaritmo del tamaño",
    "sowhat": "No mover campañas al fin de semana: segmentarlas. Un masivo de 1 M el domingo respondería como un masivo de lunes. La regla es tamaño máximo por pieza, no día."}

_SEG = {"kind": "content", "tracker": "C. Qué funciona",
    "title": "Active y Precobranza responden 3 a 10 veces más que Leads y Recurrent en email y push, pero reciben 4 % de los envíos; Leads y Recurrent reciben 58 %",
    "exhibit": {"type": "heatmap", "cols": _SG["cols"], "rows": _SG["rows"], "matrix": _SG["matrix"], "share": _SG["share"], "row_scale": True, "labw": 150, "labw_in": 1.9,
                "share_label": "% de todos los envíos, por segmento", "label": "Respuesta por segmento y canal (color relativo dentro de cada canal)", "fmt": "pct2"},
    "side": ["Nueve segmentos con más envíos (92 % del total). Celdas en gris: menos de 100 mil envíos en ese canal.",
             "Leads y Recurrent son la mitad del volumen y responden 0.4 a 0.9 % en email; Active responde 2.5 % en email y 9.8 % en push con 2 % de los envíos.",
             "Not Tracked (13 %) responde bien porque es transaccional sin etiquetar: hay que etiquetarlo, no apagarlo. Churn y HardInactive responden 0.1 a 0.2 % en email: ahí solo push barato con señal.",
             "WhatsApp e in-app leen o hacen clic entre 20 y 80 % en todos los segmentos: el canal, no el segmento, explica esa tasa."],
    "source": SRC_SHEETS + ", P_Segmentos (E11). Respuesta: clic (email, in-app), apertura (push), lectura (WhatsApp)",
    "sowhat": "El volumen sigue a la respuesta: Active y Precobranza pueden recibir más; Leads y Recurrent solo con oferta probada y prueba al 10 %. Not Tracked se etiqueta este mes."}

_after("El volumen subió 86 %", _REG_SEM, _IDX, _VEL)
_after("73 % de los usuarios no respondió", _CAS)
_after("97.5 M mensajes fueron a quien nunca respondió", _MUD)
_PARES = {"kind": "content", "tracker": "B. Demasiado y sin coordinación",
     "title": "Los choques más grandes son dos piezas a 'Todos' el mismo día: 1.5 M usuarios recibieron dos push de Marketing el 21 de junio y un Canvas de QA chocó con 1.45 M usuarios reales",
     "exhibit": {"type": "table", "head": ["Pieza A (equipo)", "Pieza B (equipo)", "Canales", "Usuarios", "Meses juntas"],
                 "rows": [[f"{_pz(q['fa'])} ({DD.team_of(q['a']) if q['a'] != 'QA' else 'QA'})", f"{_pz(q['fb'])} ({DD.team_of(q['b']) if q['b'] != 'QA' else 'QA'})", _cn(q['ca'], q['cb']), f"{q['usuarios']/1e6:.2f} M", str(q["meses"])] for q in _PC["top"]],
                 "small": True},
     "side": ["Pares promocionales con más usuario-días juntos (E6b, 1,000 pares). Los pares transaccionales (préstamo dispersado con confirmación de pago, 0.5 a 0.6 M usuarios) son legítimos y no se tocan.",
              "La fecha en el nombre de la pieza es la del lanzamiento; 'meses juntas' es en cuántos meses coincidieron.",
              "Ninguno de estos pares pasó por un calendario: cada equipo activó su pieza sin ver la del otro, y QA activó a usuarios reales."],
     "source": SRC_SHEETS + ", F_Solape (E6b). Usuarios aproximados que recibieron ambas piezas el mismo día",
     "sowhat": "Calendario único con fecha, equipo, pieza, audiencia y canal, y comité quincenal: ninguna pieza a 'Todos' o a más de 1 M sale el mismo día que otra. QA nunca con audiencias reales."}
# ---- Culpables: qué pieza, de qué equipo, cuándo y a cuántos -------------------
_CP = DD.culpables_push_junio()
_CW = DD.culpables_whatsapp()
_CB = DD.culpables_bajas()


def _fz(fam):
    """Nombre corto de una familia (ya sin fecha)."""
    parts = [q for q in fam.split("-") if q and q.upper() not in ("N/A", "CANVAS", "PUSH", "IA", "E", "CAMPAIGN")]
    parts = [q for q in parts if not (q.isdigit() or (q[0] in "BTS" and q[1:].isdigit()))]
    return " ".join(parts[1:5]).replace("_", " ")[:46] if len(parts) > 1 else fam[:46]


_CULP_PUSH = {"kind": "content", "tracker": "Contexto",
    "title": f"El salto de push de junio lo pusieron {_CP['new_n']} piezas nuevas de Marketing ({_CP['by_team']['Marketing']/1e6:.1f} M), NewProducts ({_CP['by_team']['Others']/1e6:.1f} M) y Product Growth ({_CP['by_team']['Product Growth']/1e6:.1f} M): abrieron {_CP['new_open']:.2f} % contra {_CP['old_open']:.2f} % de las piezas que ya existían",
    "exhibit": {"type": "barcause", "fmt": "M", "label": "Push enviados en junio por piezas que no existían en mayo (M), por familia; color = equipo",
                "teams": ["Marketing", "NewProducts", "Product Growth", "Sales"], "team_colors": {"NewProducts": "#7C5CC4"},
                "rows": [{"name": _fz(q["fam"])[:34], "team": q["team"] if q["team"] != "Others" else "NewProducts", "val": q["env"] / 1e6, "tag": f"abre {q['open']:.2f} %, {q['users']/1e6:.1f} M usuarios"} for q in _CP["top"]],
                "cause": {"title": "Apertura en junio (%)", "cats": [f"{_CP['new_n']} piezas nuevas ({_CP['new_env']/1e6:.0f} M)", f"Piezas que ya existían ({_CP['old_env']/1e6:.1f} M)"], "vals": [_CP["new_open"], _CP["old_open"]], "fmt": "pct2", "hl": [0], "labw": 150,
                          "note": "Las de siempre abrieron igual: la caída es de las nuevas"}},
    "kpis": [(f"{_CP['new_env']/1e6:.0f} M", f"push de junio salieron de {_CP['new_n']} piezas que no existían en mayo"), (f"{_CP['new_open']:.2f} %", f"abrieron, contra {_CP['old_open']:.2f} % de las piezas que ya existían"), ("3 en 11 días", "veces que NewProducts repitió el recordatorio de BillPay a los mismos 1.6 M usuarios")],
    "side": [f"Junio: {_CP['jun']/1e6:.1f} M push contra {_CP['may']/1e6:.1f} M en mayo. {_CP['new_env']/1e6:.1f} M salieron de piezas que no existían en mayo.",
             "Las ocho familias de la tabla son 20 M: lanzamientos a toda la base (BillPay, TopUp, AnotayGana, Mundial, Día del Padre) con audiencias de 1.1 a 3.2 M usuarios.",
             "NewProducts mandó el recordatorio de BillPay tres veces en 11 días (3, 6 y 12 de junio) y el de TopUp dos veces, a los mismos 1.6 M usuarios.",
             f"Apertura mensual de push: mayo {_CP['open_mes'][5]:.2f} %, junio {_CP['open_mes'][6]:.2f} %, julio {_CP['open_mes'][7]:.2f} %: en cuanto se fueron las piezas nuevas, volvió."],
    "source": SRC_SHEETS + ", F_Piezas (E1). Piezas de push con envíos en junio y sin envíos en mayo, agrupadas por familia; apertura = aperturas / envíos",
    "hipotesis": "Si el push se cansó por el volumen total, las piezas de siempre también deberían abrir menos en junio.",
    "causa": f"No pasó: las piezas que ya existían abrieron {_CP['old_open']:.2f} %. La caída la causan las {_CP['new_n']} piezas nuevas a 'Todos' ({_CP['new_open']:.2f} %), y tres equipos las lanzaron el mismo mes sin calendario común.",
    "sowhat": "Un lanzamiento masivo por push no se repite tres veces en 11 días ni coincide con el de otro equipo: tope de un push a 'Todos' por semana en todo Kueski, y los recordatorios de producto solo a quien no abrió el primero."}

_H1, _H2 = _CW["tot"]["H1"], _CW["tot"]["H2"]
_G1, _G2 = _CW["grupos"]["H1"], _CW["grupos"]["H2"]
_CULP_WA = {"kind": "content", "tracker": "Contexto",
    "title": f"WhatsApp bajó de {_H1['deliv']/6e6:.1f} M entregados al mes a {_H2['deliv']/3e6:.1f} M y la lectura de {_H1['read']:.1f} a {_H2['read']:.1f} %: lo que queda va a leads rezagados y churn de Marketing y Product Growth, que leen 50 a 62 %",
    "exhibit": {"type": "barcause", "fmt": "MXN", "label": "WhatsApp entregados de julio a septiembre (M, = M MXN), por familia; color = equipo",
                "teams": ["Marketing", "Product Growth", "Sales"], "team_colors": {"Marketing": "#B5342B", "Product Growth": "#1F4FD8", "Sales": "#1F9E89"},
                "rows": [{"name": _fz(q["fam"])[:34], "team": q["team"], "val": q["deliv"] / 1e6, "tag": f"{q['grupo']}, lee {q['read']:.0f} %"} for q in _CW["top"]],
                "cause": {"title": "Lectura por audiencia, julio a septiembre (%)", "cats": ["Leads", "Recurrentes y activos", "Leads rezagados", "Churn e inactivos"],
                          "vals": [_CW["grupos"]["H2"][g]["read"] for g in ("Leads", "Recurrentes y activos", "Leads rezagados", "Churn e inactivos")], "fmt": "pct0", "hl": [2, 3], "labw": 128,
                          "note": f"Rezagados y churn pasaron de {_CW['grupos']['H1']['Leads rezagados']['share']+_CW['grupos']['H1']['Churn e inactivos']['share']:.0f} % a {_CW['grupos']['H2']['Leads rezagados']['share']+_CW['grupos']['H2']['Churn e inactivos']['share']:.0f} % de las entregas"}},
    "kpis": [(f"{_CW['tot']['H1']['read']:.0f} % a {_CW['tot']['H2']['read']:.0f} %", "lectura de WhatsApp, primer contra segundo semestre"), (f"{_CW['grupos']['H2']['Leads rezagados']['share']+_CW['grupos']['H2']['Churn e inactivos']['share']:.0f} %", "de las entregas de julio a septiembre van a rezagados y churn (leen 55 a 62 %)"), (f"{(_CW['grupos']['H2']['Leads rezagados']['deliv']+_CW['grupos']['H2']['Churn e inactivos']['deliv'])/3e6:.1f} M MXN", "al mes en WhatsApp a esas audiencias; por push costaría cero")],
    "side": [f"Enero a junio: Leads y Recurrentes eran {_G1['Leads']['share']+_G1['Recurrentes y activos']['share']:.0f} % de las entregas y leían {_G1['Leads']['read']:.0f} a {_G1['Recurrentes y activos']['read']:.0f} %. Julio a septiembre: churn e inactivos subieron de {_G1['Churn e inactivos']['share']:.0f} a {_G2['Churn e inactivos']['share']:.0f} % con {_G2['Churn e inactivos']['read']:.0f} % de lectura.",
             f"Por equipo en 9 meses: Sales lee {_CW['team']['Sales']['read']:.0f} % ({_CW['team']['Sales']['deliv']/1e6:.1f} M), Marketing {_CW['team']['Marketing']['read']:.0f} % ({_CW['team']['Marketing']['deliv']/1e6:.1f} M), Product Growth {_CW['team']['Product Growth']['read']:.0f} % ({_CW['team']['Product Growth']['deliv']/1e6:.1f} M).",
             "RescateTasa0 a la base rezagada (Marketing) y Churn 12 meses (Product Growth) corren los tres meses a 225 a 310 mil usuarios: 2.5 M MXN en el trimestre con la lectura más baja del canal.",
             "Cada entregado cuesta 1.00 MXN; un push a la misma audiencia cuesta cero."],
    "source": SRC_SHEETS + ", F_Piezas (E1). Entregas y lecturas de WhatsApp por pieza; audiencia según el nombre de la pieza",
    "hipotesis": "Si el canal se desgastó, todas las audiencias deberían leer menos en el segundo semestre.",
    "causa": f"Leads y Recurrentes siguen leyendo {_G2['Leads']['read']:.0f} y {_G2['Recurrentes y activos']['read']:.0f} %. La lectura total cae porque cambió la mezcla: Marketing y Product Growth movieron el WhatsApp a bases rezagadas y churn, que leen {_G2['Leads rezagados']['read']:.0f} y {_G2['Churn e inactivos']['read']:.0f} %.",
    "sowhat": "WhatsApp a 1 MXN por entregado se reserva a Active, Recurrentes y Precobranza (lectura arriba de 67 %). Churn, inactivos y bases rezagadas van por push o email; si no responden ahí, no van."}

_CULP_BAJAS = {"kind": "content", "tracker": "A. A quien no responde",
    "title": f"Ocho familias de email generan {_CB['top'][-1]['cum']:.0f} % de las bajas: Tasa0 a nuevos registrados ({_CB['top'][0]['bajas']/1e3:.0f} mil, nueve meses), ReferralProgram y Retargeting Veriff de Marketing (38 mil cada una) y BillPay Intro en un solo envío (37 mil)",
    "exhibit": {"type": "barcause", "fmt": "int", "label": "Bajas de email en 9 meses (miles), por familia; color = equipo",
                "teams": ["Product Growth", "Marketing", "NewProducts"], "team_colors": {"NewProducts": "#7C5CC4"},
                "rows": [{"name": _fz(q["fam"])[:34], "team": q["team"] if q["team"] != "Others" else "NewProducts", "val": q["bajas"] / 1e3, "tag": f"{q['por_mil']:.1f} por mil, clic {q['clic']:.2f} %, {q['meses'].count(',')+1} {'mes' if q['meses'].count(',')==0 else 'meses'}"} for q in _CB["top"]],
                "cause": {"title": "Bajas por mil entregados, según audiencia", "cats": ["'Todos'", "Leads rezagados", "Leads", "Churn e inactivos", "Recurrentes y activos"],
                          "vals": [_CB["aud"][g]["por_mil"] for g in ("Todos", "Leads rezagados", "Leads", "Churn e inactivos", "Recurrentes y activos")], "fmt": "x1", "hl": [0, 1, 2], "labw": 128,
                          "note": "A audiencias frías la baja es 2 a 3 veces mayor que a recurrentes"}},
    "kpis": [(f"{_CB['top'][-1]['cum']:.0f} %", "de las bajas vienen de 8 familias"), (f"{_CB['aud']['Todos']['por_mil']:.1f} contra {_CB['aud']['Recurrentes y activos']['por_mil']:.1f}", "bajas por mil: 'Todos' contra recurrentes y activos"), ("7 de 8", "familias hacen clic debajo de 1 %; solo Veriff responde (3.04 %)")],
    "side": [f"{_CB['tot']/1e3:.0f} mil bajas con entrega en el mismo mes; promedio {_CB['por_mil']:.1f} por mil entregados. Marketing {_CB['by_team']['Marketing']:.0f} %, Product Growth {_CB['by_team']['Product Growth']:.0f} %, NewProducts {_CB['by_team']['Others']:.0f} %.",
             f"Por audiencia: 'Todos' {_CB['aud']['Todos']['por_mil']:.1f} por mil y Leads {_CB['aud']['Leads']['por_mil']:.1f}, contra Recurrentes y Active {_CB['aud']['Recurrentes y activos']['por_mil']:.1f}. Leads y 'Todos' son {_CB['aud']['Leads']['share']+_CB['aud']['Todos']['share']+_CB['aud']['Leads rezagados']['share']:.0f} % de las bajas.",
             "Veriff se da de baja 3.9 por mil pero hace clic 3.04 %: es la pieza que más responde; se protege y se le baja la frecuencia. Las otras siete hacen clic debajo de 1 %.",
             f"Otras {_CB['anom']/1e3:.0f} mil bajas se registran en meses en que la pieza no entregó nada (Braze las atribuye al último envío recibido); se excluyen de la tabla."],
    "source": SRC_SHEETS + ", F_Piezas (E1). Bajas de email por pieza y mes, solo meses con entrega; familias con 100 mil entregados o más",
    "hipotesis": "Si las bajas vinieran de piezas puntuales mal hechas, se concentrarían en pocas piezas de un mes.",
    "causa": "Vienen de piezas que corren todos los meses a audiencias frías: Leads, bases rezagadas y 'Todos' se dan de baja 3.2 a 4.6 por mil, dos a tres veces más que Recurrentes. La causa es a quién se manda y cuántas veces, no el copy.",
    "sowhat": "ReferralProgram y NarrativaTasa0 (más de 4 bajas por mil, clic debajo de 1 %) se detienen esta semana. Tasa0 a nuevos entra a la secuencia de bienvenida con tope de 3 emails. Ninguna pieza a 'Todos' sin segmento."}
_after("Semana a semana: push triplicó", _CULP_PUSH, _CULP_WA)
_after("Un usuario nuevo se da de baja", _CULP_BAJAS)

_after("Cada mes 1.3 a 2.2 M usuarios", _PARES)
_after("El lunes concentra 23 % del email", _REG_DIA)
_after("Audiencias de 10 a 100 mil usuarios", _SCATTER, _CAMP)
_after("Cada equipo tiene un canal que le funciona", _DISP, _SEG)


# ---- Bloque 3: entrega por equipo, quién insiste, qué interesa, scorecard, repetición ----
_EN = DD.entrega_equipo()
_IN = DD.insisten()
_GC = DD.gancho_canal()
_SC = DD.scorecard()
_VR = DD.versiones()
_T4 = ["Product Growth", "Marketing", "Sales", "Collections", "Others"]
_short_team = {"Product Growth": "Product Growth", "Marketing": "Marketing", "Sales": "Sales", "Collections": "Collections", "Others": "Others (transaccional)"}

_ENTREGA = {"kind": "content", "tracker": "A. A quien no responde",
    "title": f"Recibidos y no recibidos: Product Growth pierde {100-_EN['Product Growth']['wa_pct']:.0f} % de sus WhatsApp y {100-_EN['Product Growth']['email_pct']:.0f} % de sus emails antes de llegar; Sales entrega {_EN['Sales']['wa_pct']:.0f} % y {_EN['Sales']['email_pct']:.0f} %",
    "exhibit": {"type": "stackbar", "segments": ["Entregados", "No entregados"], "colors": ["#1F9E89", "#B5342B"], "panels": [
        {"title": "Email en 9 meses (M): llegó y no llegó, por equipo", "cats": _T4, "rows": [[_EN[t]["email_del"] / 1e6, (_EN[t]["email_sent"] - _EN[t]["email_del"]) / 1e6] for t in _T4], "fmt": "int"},
        {"title": "WhatsApp en 9 meses (M): llegó y no llegó, por equipo", "cats": _T4, "rows": [[_EN[t]["wa_del"] / 1e6, (_EN[t]["wa_sent"] - _EN[t]["wa_del"]) / 1e6] for t in _T4], "fmt": "x1"}],
        "note": "Email: entregados sobre enviados. WhatsApp: entregados sobre enviados; Meta cobra por entregado. Collections no usa WhatsApp."},
    "kpis": [(f"{sum(_EN[t]['wa_sent']-_EN[t]['wa_del'] for t in _T4)/1e6:.1f} M", "WhatsApp que no llegaron en 9 meses (26 %)"), (f"{sum(_EN[t]['email_sent']-_EN[t]['email_del'] for t in _T4)/1e6:.0f} M", "emails que no llegaron (5 %)"), (f"{_EN['Sales']['wa_pct']:.0f} %", f"entrega de WhatsApp de Sales, la mejor; Product Growth {_EN['Product Growth']['wa_pct']:.0f} %")],
    "side": [f"Email: Sales entrega {_EN['Sales']['email_pct']:.1f} %, Marketing {_EN['Marketing']['email_pct']:.1f} %, Product Growth {_EN['Product Growth']['email_pct']:.1f} %. La diferencia son los correos de nuevos registrados sin verificar (Tasa0, NeverActive) que rebotan.",
             f"WhatsApp: Sales {_EN['Sales']['wa_pct']:.0f} % (recurrentes KPay con número reciente), Marketing {_EN['Marketing']['wa_pct']:.0f} %, Product Growth {_EN['Product Growth']['wa_pct']:.0f} % (churn e inactivos de 12 meses con número viejo).",
             "Cada WhatsApp que no llega no se cobra, pero degrada la calidad del número ante Meta y baja el tope diario para los que sí llegan.",
             "Regla: WhatsApp solo a quien ya dio señal y exclusión tras 3 fallos de entrega; email a nuevos solo con correo verificado."],
    "source": SRC_SHEETS + ", F_Piezas (E1). Entregados sobre enviados por equipo",
    "hipotesis": "Si la entrega dependiera del canal, todos los equipos perderían la misma proporción.",
    "causa_tag": "audiencia",
    "causa": "La pérdida va con la audiencia, no con el canal: Product Growth manda WhatsApp a churn de 12 meses y email a registrados sin verificar; Sales manda a recurrentes de KPay con datos recientes y entrega 80 y 97 %.",
    "impacto": "Con la entrega de Sales en todos los equipos, 3 M WhatsApp y 6 M emails más llegarían en 9 meses sin mandar uno más, y el número de WhatsApp conserva su tope diario.",
    "sowhat": "No se compra más entrega con más envíos: se limpia la base. Exclusión EXC-WA_SinEntrega3 y correo verificado como condición de entrada a cualquier pieza de email a nuevos."}

_ej = _IN["ejemplos"]
_cn2 = {"email": "email", "push notification": "push", "whatsapp": "WhatsApp", "in-app": "in-app"}
_INSISTE = {"kind": "content", "tracker": "C. Qué funciona",
    "title": f"{_IN['tot_share']:.0f} % de los envíos ({_IN['tot_env']/1e6:.0f} M, {_IN['tot_costo']/1e6:.0f} M MXN) salieron en meses posteriores a que la pieza ya estaba debajo del mínimo: Product Growth insiste con {_IN['team']['Product Growth']['share']:.0f} % de su volumen (Tasa0 a nuevos, 7 meses seguidos), Marketing con {_IN['team']['Marketing']['share']:.0f} %, Sales con {_IN['team']['Sales']['share']:.0f} %",
    "exhibit": {"type": "barcause", "fmt": "M", "label": "Envíos después de que la pieza ya había fallado (M), por familia; color = equipo",
                "teams": ["Product Growth", "Marketing", "Others"], "team_colors": {"Others": "#7C5CC4"},
                "rows": [{"name": _fz(q["fam"])[:34], "team": q["team"], "val": q["env"] / 1e6, "tag": f"{_cn2[q['canal']]}, {q['meses']} {'mes' if q['meses']==1 else 'meses'} más"} for q in _ej],
                "cause": {"title": "% del volumen del equipo que insiste", "cats": _T4, "vals": [_IN["team"][t]["share"] for t in _T4], "fmt": "pct0", "hl": [0, 1, 3], "labw": 110,
                          "note": "Collections: cobranza, no se toca sin Legal"}},
    "kpis": [(f"{_IN['tot_env']/1e6:.0f} M", "mensajes enviados cuando la pieza ya estaba debajo del mínimo"), (f"{_IN['tot_costo']/1e6:.0f} M MXN", "costo de insistir, 9 meses"), ("7 meses", "siguió Tasa0 a nuevos registrados (29 M emails) después de fallar")],
    "side": ["Una pieza 'falló' el primer mes en que, con 50 mil o más entregados, respondió debajo del mínimo del canal (email 0.3 %, push 0.75 %, WhatsApp 60 %, in-app 10 %). Se cuenta lo que mandó después.",
             f"Product Growth: {_IN['team']['Product Growth']['n_fam']} familias, {_IN['team']['Product Growth']['env_insiste']/1e6:.0f} M envíos y {_IN['team']['Product Growth']['costo']/1e6:.1f} M MXN. Marketing: {_IN['team']['Marketing']['n_fam']} familias, {_IN['team']['Marketing']['env_insiste']/1e6:.0f} M y {_IN['team']['Marketing']['costo']/1e6:.1f} M MXN.",
             f"Sales insiste poco ({_IN['team']['Sales']['share']:.0f} %) y Others ({_IN['team']['Others']['share']:.0f} %): sus piezas son transaccionales o se apagan solas al terminar la campaña.",
             "Ninguna de las ocho familias de la gráfica cambió de audiencia ni de gancho entre el mes que falló y el último envío."],
    "source": SRC_SHEETS + ", F_Piezas (E1). Familia por canal y mes; mínimo del canal según Parámetros",
    "hipotesis": "Si hubiera revisión, una pieza que falla se apaga o se rehace al mes siguiente.",
    "causa_tag": "medicion",
    "causa": "Nadie revisa la pieza a las 4 semanas: sin tablero por pieza ni regla de apagado, un Canvas que falló en febrero sigue corriendo en septiembre con la misma audiencia y el mismo gancho.",
    "impacto": f"Regla de 4 semanas (debajo del mínimo se apaga o se rehace): {_IN['tot_env']/9e6:.0f} M mensajes menos al mes, {_IN['tot_costo']/9e6:.1f} M MXN al mes y las bajas de esas piezas con ellas.",
    "sowhat": "La regla más barata del playbook: a las 4 semanas se mira la respuesta contra el mínimo y lo que no pasa se apaga. Product Growth y Marketing la aplican primero: tienen 125 M de los 149 M."}

_GANCHO = {"kind": "content", "tracker": "C. Qué funciona",
    "title": "Lo que más abren los usuarios es lo que ya empezaron o deben pagar: recordatorios (3.1 % en email, 3.8 % en push) y cobranza (1.8 %, 4.0 %); ofertas, Tasa 0, referidos y lanzamientos responden 0.2 a 0.5 % por email y 0.8 a 1.1 % por push, y son 59 % de los envíos",
    "exhibit": {"type": "heatmap", "cols": _GC["cols"], "rows": _GC["rows"], "matrix": _GC["matrix"], "row_share": _GC["share"], "col_scale": True, "fmts": ["pct2", "pct2", "pct0", "pct0"], "labw": 190, "labw_in": 2.3,
                "share_label": "% de los envíos", "label": "Respuesta por gancho y canal (color relativo dentro de cada canal)", "fmt": "pct2"},
    "kpis": [("3.1 %", "clic de email de un recordatorio de algo empezado"), ("0.22 a 0.26 %", "clic de referidos, lanzamientos y ofertas por email"), ("59 %", "de los envíos son ofertas, Tasa 0, referidos y lanzamientos")],
    "side": ["Gancho leído del nombre de la pieza; celdas en gris: menos de 200 mil entregados en ese canal. 'Otro' incluye transaccionales y encuestas.",
             "En in-app casi todo responde (22 a 69 %) porque solo lo ve quien ya abrió la app; en WhatsApp la lectura es 56 a 73 % en todos los ganchos: ahí el gancho no cambia el resultado, cambia el costo.",
             "Bienvenida y activación responde 0.16 % por email y 2.5 % por push: al nuevo se le habla por push e in-app, no por email.",
             "La única forma de subir la respuesta de ofertas y lanzamientos es mandarlos a quien dio una señal (carrito, solicitud empezada, pago próximo) o moverlos a in-app."],
    "source": SRC_SHEETS + ", F_Piezas (E1). Respuesta: clic (email, in-app), apertura (push), lectura (WhatsApp) sobre entregados o impresiones",
    "hipotesis": "Si el usuario quisiera ofertas, el gancho con más volumen sería el que más responde.",
    "causa_tag": "producto",
    "causa": "El volumen va a lo que el equipo quiere vender (ofertas, Tasa 0, referidos, lanzamientos: 59 % de los envíos), no a lo que el usuario tiene pendiente (recordatorios y pagos: 18 %). La oferta nueva sin señal es el gancho que menos interesa.",
    "impacto": "Si la mitad de ofertas y lanzamientos por email (37 M) fueran recordatorios de algo empezado, ese volumen pasaría de 0.26 % a 3.1 % de clic: más de 1 M de clics adicionales en 9 meses.",
    "sowhat": "El playbook invierte la mezcla: el gancho por defecto es recordar algo que el usuario empezó o debe pagar; ofertas, referidos y lanzamientos van a in-app o a un segmento con señal, nunca a 'Todos'."}

_sc_panels = [
    {"title": "Clic de email (%)", "vals": [_SC[t]["email"] for t in _T4], "fmt": "pct2"},
    {"title": "Apertura de push (%)", "vals": [_SC[t]["push"] for t in _T4], "fmt": "pct2"},
    {"title": "Lectura de WhatsApp (%)", "vals": [_SC[t]["wa"] for t in _T4], "fmt": "pct0", "na": "no usa"},
    {"title": "Bajas de email por mil entregados", "vals": [_SC[t]["bajas"] for t in _T4], "fmt": "x1", "better": "low"},
    {"title": "Entrega de WhatsApp (%)", "vals": [_SC[t]["wa_del"] for t in _T4], "fmt": "pct0", "na": "no usa"},
    {"title": "% del volumen que insiste tras fallar", "vals": [_SC[t]["insiste"] for t in _T4], "fmt": "pct0", "better": "low"},
]
_SCORE = {"kind": "content", "tracker": "C. Qué funciona",
    "title": "Quién lo maneja mejor: Others (transaccional) y Collections tienen la mejor respuesta por canal y Sales la mejor entrega; Product Growth insiste con 39 % de su volumen tras fallar y Marketing se da de baja 5.9 por mil, el doble que el resto",
    "exhibit": {"type": "hbarmult", "cats": [_short_team[t] for t in _T4], "panels": _sc_panels, "ncol": 3},
    "kpis": [("3.6 %", "apertura de push de Collections, la mejor; Others 1.8 % de clic en email"), ("80 %", "entrega de WhatsApp de Sales, la mejor; Product Growth 72 %"), ("39 %", "del volumen de Product Growth insiste tras fallar; Marketing 5.9 bajas por mil")],
    "side": ["Verde: el mejor equipo en ese indicador; rojo: el peor. Collections y Others no usan WhatsApp o no llegan a 100 mil entregados.",
             "Others responde bien porque es transaccional (confirmación de pago, préstamo dispersado): es la prueba de que el usuario abre lo que le concierne.",
             "Collections tiene la mejor apertura de push (3.6 %) y las menores bajas (0.25 por mil): manda a quien tiene un pago, con una razón.",
             "Marketing tiene el mejor clic de email entre los promocionales (0.95 %) pero paga con bajas (5.9 por mil): el mismo equipo tiene Veriff (3.0 %) y Referral (0.2 %)."],
    "source": SRC_SHEETS + ", F_Piezas (E1), Vista_equipo. Tasas ponderadas por volumen en 9 meses",
    "hipotesis": "Si hubiera un equipo que lo hace bien en todo, bastaría copiar su forma de operar.",
    "causa_tag": "medicion",
    "causa": "No hay uno: cada equipo opera Braze solo y gana donde manda con una razón (pago, transacción, recurrente) y pierde donde manda masivo sin señal. Nadie compara su tablero con el de los otros ni revisa a las 4 semanas.",
    "impacto": "Un tablero por equipo con estos 6 indicadores y revisión mensual: Product Growth y Marketing dejan de insistir con 125 M mensajes (10.8 M MXN en 9 meses) y Marketing baja sus bajas a la mitad al sacar Leads y 'Todos' de sus masivos.",
    "sowhat": "El equipo que 'lo maneja mejor' es el que manda con una razón del usuario: cobranza y transaccional. El playbook lleva esa lógica a lo promocional: señal antes que volumen, y un tablero común para que se vea."}

_VERS = {"kind": "content", "tracker": "D. Sin medición",
    "title": f"Repetición: {_VR['n_multi']} familias tienen 5 o más versiones y concentran {100*_VR['env_multi']/_VR['tot_env']:.0f} % de los envíos; 'Comercio del día' existe en 9 segmentos distintos y 'Cuponera' en 7: el mismo segmento se vuelve a crear cada mes",
    "exhibit": {"type": "hbar", "cats": ["Comercio del día", "BKT (cobranza)", "Cuponera de descuentos", "BBDD hot leads rescate Tasa 0", "Temu", "Kueski nuevo", "Registro de línea MX", "Newsletter"],
                "vals": [n for _, n in _VR["dup_segs"]], "fmt": "int", "label": "Valores distintos de segmento o subsegmento que nombran lo mismo (solo cambia el mes, la versión o la ortografía)",
                "highlight": [0, 1, 2]},
    "kpis": [(f"{_VR['n_multi']}", "familias con 5 o más versiones de la misma pieza"), (f"{100*_VR['env_multi']/_VR['tot_env']:.0f} %", "de los envíos salen de esas familias"), (f"{_VR['n_dup_values']}", "valores de segmento que repiten 8 nombres")],
    "side": ["Una versión es una comunicación distinta en Braze con el mismo nombre de familia (sin la fecha): se copia la pieza, se cambia la fecha y se activa, sin archivar la anterior.",
             "El segmento se escribe con el mes ('ComercioDelDia_Junio'), con la ola ('W1', 'W2') o con un error de dedo: 481 combinaciones de segmento, subsegmento y grupo para 30 audiencias reales.",
             "109 piezas activas duplicadas en 13 combinaciones de producto, audiencia y gancho: dos versiones vivas de lo mismo mandan al mismo usuario dos veces.",
             "Comercio del día y Cuponera son una sola pieza que lee del catálogo, no 16 segmentos."],
    "source": SRC_SHEETS + ", Catálogo (E1, E2), P_Segmentos (E11). Agrupación por nombre normalizado",
    "hipotesis": "Si hubiera segmentos maestros con dueño, una audiencia tendría un solo nombre y una pieza una sola versión viva.",
    "causa_tag": "operacion",
    "causa": "Sin segmentos maestros ni dueño del catálogo, cada mes se crea un segmento nuevo con el nombre del mes y una copia de la pieza; Braze acumula versiones que nadie archiva y dos versiones vivas chocan en el mismo usuario.",
    "impacto": "30 segmentos maestros con dueño y una pieza viva por combinación: 55 valores duplicados pasan a 8, las 109 piezas activas duplicadas a una por combinación, y los choques de la misma familia desaparecen.",
    "sowhat": "Nomenclatura Ticket-Producto-Audiencia-Gancho, segmentos SEG- con dueño y archivo trimestral de lo que no se usa: es trabajo de MarTech de dos semanas y evita el 38 % de choques dentro del mismo equipo."}

_after("1 de cada 4 WhatsApp no llega", _ENTREGA)
_after("Dentro de cada equipo la respuesta varía", _SCORE, _INSISTE)
_after("Recordar algo que el usuario empezó", _GANCHO)
_after("749 piezas sin ticket", _VERS)

# ---- KPIs (3 números grandes) en láminas que solo tenían tabla, reglas o gantt ----
KPIS = {
 "19 de 24 indicadores": [("19 de 24", "indicadores debajo del estándar"), ("0.92 %", "clic de email contra 1.5 % de estándar"), ("1.53 %", "apertura de push contra 3 %")],
 "In-app responde 38 %": [("38 %", "clic de in-app, sin costo"), ("0.93 %", "clic de email a 0.05 MXN por envío"), ("20 veces", "más caro WhatsApp que email por mensaje")],
 "Cada equipo tiene un canal que le funciona": [("1.30 M MXN", "ahorro al mes en Product Growth, 81 % del total"), ("0.21 %", "clic de email de Sales, el peor de los cinco"), ("4.3 % y 5.3 %", "Precobranza por email y push, la mejor pieza de la empresa")],
 "10 piezas concentran 125 M envíos": [("125 M", "envíos en 10 piezas, 19 % del total"), ("0.07 a 0.76 %", "respuesta de 9 de las 10"), ("6", "piezas a proteger (3 a 87 % de respuesta)")],
 "749 piezas sin ticket": [("749", "piezas sin ticket"), ("731", "formas de escribir la audiencia"), ("171", "pruebas y copias que llegaron a usuarios reales")],
 "Los choques más grandes son dos piezas": [("1.5 M", "usuarios con dos push de Marketing el 21 de junio"), ("1.45 M", "usuarios reales alcanzados por un Canvas de QA"), ("38 %", "de los choques son dentro del mismo equipo")],
 "Diez piezas con acción concreta": [("125 M", "envíos cubiertos por diez acciones"), ("6 de 10", "se apagan o se confirma su apagado"), ("14 M", "mensajes menos al mes")],
 "El playbook en 12 reglas": [("12", "reglas"), ("15 de 19", "indicadores en rojo que atacan"), ("10 %", "grupo de control en toda pieza")],
 "Qué mandar por tipo": [("8", "tipos de mensaje con canal, día y veces decididos"), ("3.09 %", "clic de un recordatorio por email, el gancho base"), ("2", "toques máximo; el segundo solo a quien no abrió")],
 "Dieciocho ajustes de Braze": [("18", "ajustes que se configuran una vez"), ("5 / 2 / 1", "promocionales por semana, piezas al día, push al día"), ("10 %", "grupo de control nativo en toda pieza")],
 "Un dueño por cosa y un calendario único": [("1", "dueño por nombre, segmento, calendario y pieza"), ("30 min", "comité quincenal para 'Todos' y más de 1 M"), ("2 meses", "en rojo abren un ticket")],
 "Plan a 90 días": [("30 días", "limpiar: apagar 48, pausar 171, 7 exclusiones"), ("60 días", "configurar: frequency cap, control, segmentos"), ("90 días", "medir: primer lift y primera prueba A/B por equipo")],
 "Lo que todavía no sabemos": [("8", "preguntas abiertas"), ("6 de 8", "se resuelven con datos que ya existen"), ("1", "depende de Finanzas: el costo fijo de Braze")],
 "Próximos pasos": [("8", "tareas con dueño esta semana"), ("48", "campañas a apagar en la semana 1"), ("7", "exclusiones a cargar en la semana 2")],
 "Método: 18 extracciones": [("18", "extracciones agregadas"), ("471", "verificaciones en el Sheets"), ("0", "datos personales")],
 "Estándares: los 24 indicadores": [("24", "indicadores con definición y fórmula"), ("19", "debajo del estándar"), ("5", "cumplen")],
 "Por mes: envíos, respuesta, bajas y costo": [("109 M", "envíos en junio, el doble de enero"), ("0.67 %", "clic de email en junio, el peor del año"), ("2.12 %", "apertura de push en septiembre, la mejor")],
 "Por día de la semana: volumen": [("18.6 %", "de los envíos salen el lunes"), ("0.65 %", "clic de email del lunes"), ("1.91 %", "clic del domingo, con piezas chicas")],
 "Supuestos y dónde está cada cosa": [("0.05 y 1.00", "MXN por email enviado y por WhatsApp entregado"), ("7 días", "ventana de conversión, solo como referencia"), ("37 %", "de los envíos cubre el golden dataset")],
}
for _s in SLIDES:
    if _s.get("kind") != "content" or _s.get("kpis"):
        continue
    for _k, _v in KPIS.items():
        if _s.get("title", "").startswith(_k):
            _s["kpis"] = _v
            break

# ---- Hipótesis, causa atribuida (con tipo) y qué pasa si se resuelve, en cada lámina ----
# tipo: saturacion | solape | producto | audiencia | canal | operacion | medicion | metodo
HC = {
 "Revisamos 9 meses de envíos": ("Con datos agregados de toda la base se puede atribuir cada hallazgo a piezas, equipos y meses concretos.", "metodo", "Las 18 extracciones cruzan pieza, equipo, canal, mes, usuario y respuesta: cada lámina puede decir quién, qué y cuándo.", "Cada acción del plan se mide campaña por campaña desde el primer mes con el mismo Sheets; no hace falta acceso a Braze para auditar."),
 "WhatsApp es 8 % del volumen": ("El costo debería seguir al volumen: el canal más usado sería el más caro.", "audiencia", "WhatsApp cuesta 1.00 MXN por entregado y Marketing (22.9 M MXN) y Product Growth (11.4 M) lo usan como canal masivo a leads rezagados y churn, que leen 55 a 62 %.", "Reservar WhatsApp a quien ya respondió (lectura arriba de 67 %) mueve cerca de 1 M MXN al mes a push sin costo y sube la lectura del canal 10 puntos."),
 "El volumen subió 86 %": ("Más mensajes deberían traer más respuesta total aunque la tasa baje.", "saturacion", "La tasa cayó en los cuatro canales a la vez porque el volumen nuevo fue masivo sin segmento y concentrado: 139 piezas de push nuevas en junio, BillPay Intro a 16 M por email, WhatsApp a bases rezagadas.", "Con el volumen de enero (59 M al mes) el email daba 1.20 % de clic; junio dio 0.67 % con 109 M: el mismo número de clics con la mitad de los envíos y sin las 63 mil bajas de junio."),
 "Cada millón de emails más": ("La respuesta semanal depende del volumen de esa semana.", "saturacion", "Email R² 0.60 y push 0.53: las semanas arriba de 10 M de email y 8 M de push son las de lanzamientos a 'Todos' de Marketing, NewProducts y Product Growth (junio: BillPay, AnotayGana, Mundial). WhatsApp R² 0.01: ahí manda la audiencia.", "Un tope de 10 M de emails y 8 M de push por semana recupera 0.3 puntos de clic (de 0.9 a 1.2 %) y 0.5 de apertura sin tocar una sola pieza."),
 "Dentro de un mes la respuesta": ("El promedio mensual representa bien el mes.", "medicion", "Una sola semana de masivo mueve más que todo el año: la mecha de junio en email es BillPay Intro (16 M, 0.1 % de clic) la semana del 1 de junio. Nadie lo vio a tiempo porque el tablero es mensual.", "Con un tablero semanal, una semana como la del 1 de junio (0.36 %) se detecta en 7 días y se frena el segundo envío antes de que salga."),
 "19 de 24 indicadores": ("Estamos cerca del estándar y falta ajustar el copy.", "audiencia", "19 de 24 en rojo porque el problema es estructural: audiencias masivas sin segmento (Leads, 'Todos'), frecuencia sin tope y canales sin regla de preferencia. Ninguna pieza masiva llega al piso.", "Las 12 reglas del playbook atacan 15 de los 19 en rojo; en 90 días la meta es 10 en verde: clic 1.5 %, apertura 3 %, bajas 2.5 por mil."),
 "73 % de los usuarios no respondió": ("La base es grande y toda vale lo mismo para recibir mensajes.", "audiencia", "14.2 M usuarios no respondieron a nada en 9 meses y reciben 24 % del volumen: son leads y no rastreados a los que Marketing y Product Growth mandan masivos sin segmento cada mes.", "Excluir a los 14.2 M mudos de lo promocional ahorra cerca de 900 mil MXN al mes y 17 % de las bajas sin perder conversiones (convierten 0.08 %)."),
 "2.2 M usuarios que responden a 2": ("Mandar a todos maximiza conversiones.", "audiencia", "86 % de las conversiones vienen del 11 % que responde a varios canales; los 14.2 M mudos reciben 160 M mensajes y aportan 1 %. El volumen va a donde no hay resultado porque nadie segmenta por respuesta.", "Dejar de mandar promocional a mudos quita 160 M mensajes (24 %) y 1 % de las conversiones: el presupuesto se concentra en los 5.3 M que sí responden."),
 "59 % de los mensajes van a un canal": ("Insistir por todos los canales sube la probabilidad de respuesta.", "canal", "Cada equipo manda por su canal (Collections email, Sales push, Marketing WhatsApp) sin ver a qué canal responde el usuario; no existe el atributo canal_preferido en Braze.", "Mandar por el canal al que responde ahorra 18.7 M MXN en 9 meses (2.1 M al mes) con la misma respuesta: 149 M emails y 3.2 M WhatsApp menos."),
 "97.5 M mensajes fueron a quien nunca": ("Los mudos son pocos y cuestan poco.", "audiencia", "8.1 M MXN: 5.0 M en WhatsApp de Marketing y Product Growth a bases rezagadas y churn, 3.1 M en email de Tasa0 a nuevos y masivos a 'Todos'. No hay exclusión por inactividad en ninguna pieza promocional.", "Exclusión de 90 días sin respuesta: 900 mil MXN al mes, 191 mil bajas menos en 9 meses y cero conversiones perdidas (nadie convirtió sin responder antes)."),
 "La parte del email que va a quien nunca": ("Con el tiempo la lista se limpia sola.", "operacion", "En email no hay supresión por inactividad y el 33 % de junio es BillPay Intro a 16 M (toda la base). Push sí baja de 15 a 5 % porque la desinstalación y el permiso de notificación filtran solos.", "Supresión por inactividad en email, como ya pasa sola en push: la parte a mudos baja de 18 % a menos de 5 % y evita otro junio (11.9 M emails a quien nunca respondió)."),
 "43.8 M mensajes promocionales llegaron": ("Braze filtra automáticamente a quien se dio de baja o está bloqueado.", "operacion", "El filtro de suscripción aplica por canal, no por usuario, y los Canvas viejos no refrescan audiencia: Collections BKT1 a BKT3 (503 mil emails) y transaccionales de KPay siguen mandando a dados de baja; nadie cargó las etapas bloqueadas como exclusión.", "7 exclusiones como filtro negativo: 4.9 M mensajes menos al mes, 570 mil MXN al mes (tarjeta congelada) y cero riesgo legal por REUS y ARCO."),
 "1 de cada 4 WhatsApp no llega": ("El número está mal capturado.", "audiencia", "14.2 M sin entrega se concentran en bases rezagadas y leads comprados (Marketing) y churn de 12 meses (Product Growth): números sin WhatsApp o ajenos. No hay validación previa ni supresión después de dos fallos.", "Exclusión tras 3 fallos y WhatsApp solo con señal: la entrega sube de 74 a más de 85 % y el número conserva su tope diario ante Meta."),
 "5 % de los usuarios recibe 41": ("Los que más reciben son los clientes más activos.", "saturacion", "Son usuarios que caen en varios Canvas a la vez: la banda de 41 a 80 recibe 25 piezas distintas al mes y la de 321 o más, 220. Sin frequency cap global, cada equipo suma sin ver al otro.", "Frequency cap de 5 promocionales por semana: 339 mil usuarios salen de la banda de 321 o más (16.5 bajas por 100 contra 1.3) y el volumen baja cerca de 15 % sin tocar la conversión."),
 "Cada mes 1.3 a 2.2 M usuarios": ("Los choques son entre equipos distintos.", "solape", "38 % de los choques son del mismo equipo: Marketing con Marketing (27.6 M usuario-días) y Sales con Sales (15.4 M). Desde junio se suman piezas a 'Todos' encima de los Canvas diarios. No hay calendario único ni regla de un promocional por usuario por día.", "Un promocional por usuario por día: la baja de quien recibe 3 o más (0.9 a 1.3 por mil) cae a la de quien recibe una (0.34): 60 a 70 % menos bajas en el 9 % de usuario-días con choque."),
 "Los choques más grandes son dos piezas": ("Los choques son accidentes de un día.", "solape", "Son piezas a 'Todos' lanzadas el mismo mes por el mismo equipo (Día del Padre y Billpayments de Marketing) y un Canvas de QA activo con usuarios reales: nadie revisa el calendario antes de activar.", "Calendario único y comité quincenal: ninguno de estos pares se repite (5 M usuario-días) y QA fuera de audiencias reales evita 1.45 M envíos de prueba."),
 "Un usuario nuevo se da de baja": ("La baja del nuevo es por el contenido del email.", "saturacion", "Es por frecuencia y masivos en el primer mes: 5 emails de 4 piezas distintas en 27 días (retargeting 2 al día de Marketing, Tasa0 de Product Growth) y BillPay Intro (NewProducts, junio) explica 31 % de esas bajas.", "Una sola secuencia de bienvenida (3 emails la primera semana) y sin masivos a menores de 30 días: 53 % de las bajas de nuevos desaparecen, 84 mil usuarios en 9 meses."),
 "45 Canvas pasan de 20 pasos": ("Más pasos dan más oportunidades de convertir.", "saturacion", "477 pasos abren menos de 1 % porque insisten al mismo usuario que ya no abrió: retargeting de Marketing (Veriff, PersonalInfo) y Tasa0 de Product Growth encadenan hasta 50 pasos sin paso de decisión.", "Tope de 8 pasos y 2 toques por canal: los 477 pasos debajo de 1 % se apagan; 6 M usuarios dejan de recibir del paso 5 en adelante sin perder apertura (15.7 %, igual que el paso 1)."),
 "El lunes concentra 23 % del email": ("El lunes es un mal día para mandar.", "audiencia", "El lunes salen los masivos sin segmento de Product Growth y Marketing (45 mil usuarios por pieza contra 9 mil el domingo). El día no explica la respuesta; el tamaño de la pieza sí.", "Partir los masivos del lunes en segmentos de 10 a 100 mil: el clic del lunes sube de 0.65 % hacia el 1.0 % del resto de la semana, más de 400 mil clics en 9 meses."),
 "El fin de semana responde más": ("Mover campañas al fin de semana subiría la respuesta.", "audiencia", "El tamaño de la pieza explica 71 % de la variación del clic en Product Growth, Marketing y Sales. El fin de semana responde más porque ese día solo salen piezas chicas y segmentadas.", "No se mueve nada de día: con piezas de menos de 100 mil usuarios y una señal, cualquier día responde 1 % o más. Mover un masivo al domingo no cambia nada."),
 "56 % de los envíos van a usuarios con más de un año": ("Los usuarios antiguos ya no responden por desgaste natural.", "saturacion", "Reciben 7 veces más push porque acumulan Canvas recurrentes de Sales y Collections que nunca se apagan. Las bajas por mil son iguales en todas las bandas: es saturación, no edad.", "A más de 1 año sin respuesta en 90 días, fuera de lo promocional: se quita la mitad del volumen de donde la respuesta es más baja y el resultado no cambia, porque ese volumen no respondía."),
 "Recordar algo que el usuario empezó": ("Una oferta nueva mueve más que un recordatorio.", "producto", "El recordatorio de algo empezado (Veriff, datos personales, carrito) responde 3.09 % porque el usuario ya tenía intención; la oferta nueva a leads (Tasa 0, referidos, lanzamientos) responde 0.22 a 0.53 %. El volumen está en la oferta.", "Mover 30 M de los 54 M de Tasa 0 a recordatorios de algo empezado daría cerca de 770 mil clics más en 9 meses (3.09 % contra 0.53 %)."),
 "In-app responde 38 %": ("WhatsApp justifica su costo porque responde más.", "canal", "In-app responde 38 % porque solo lo ve quien ya abrió la app y cuesta cero; WhatsApp lee 63 a 70 % pero cuesta 20 veces más que email por mensaje. Referidos y lanzamientos van por email (0.22 %) cuando en in-app responden 43 a 55 %.", "Referidos y lanzamientos (74 M emails) a in-app: 3.7 M MXN de email que se ahorran en 9 meses y una respuesta de 43 a 55 % en lugar de 0.22 %."),
 "Audiencias de 10 a 100 mil usuarios": ("Más alcance, más resultado.", "audiencia", "Las audiencias de 10 a 100 mil son segmentos con una señal (Active, Precobranza, retargeting); las de más de 1 M son 'Todos' y Leads sin señal de Product Growth, NewProducts y Marketing. Es la audiencia, no el tamaño en sí.", "Prueba al 10 % y un segmento en todo envío de más de 1 M: los 125 M de las 10 piezas masivas responderían como las de 100 mil a 1 M (0.6 % contra 0.16 %), 4 veces más clics con la mitad del volumen."),
 "Solo ": ("Las piezas malas son pocas y grandes; el resto está bien.", "audiencia", "La mediana está en 0.3 %: el problema es general. 270 piezas de email y 288 de push usan la misma plantilla de audiencia sin segmento (Leads, 'Todos', Recurrentes); cambia el gancho, no el público.", "Rehacer con señal las 270 que no pasan: son 81 % del volumen y 31 % de los clics; si respondieran como las 38 que pasan, los clics de email se multiplican por 3 con el mismo volumen."),
 "La respuesta por pieza no es una campana": ("La respuesta se distribuye alrededor de un promedio útil.", "medicion", "Es log-normal: pocas piezas con señal (Precobranza, Veriff) inflan el promedio a 1.14 % mientras la mitad está debajo de 0.35 %. Decidir con el promedio esconde a la mayoría.", "Decidir por mediana y mínimo, no por promedio: la mitad de las piezas (debajo de 0.35 %) entra a revisión a las 4 semanas en lugar de esconderse detrás del 1.14 %."),
 "Cada equipo tiene un canal que le funciona": ("Cada equipo debería usar el canal que mejor le responde.", "canal", "Cada equipo usa el canal que tiene a la mano, no el que le responde: Collections manda email y le funciona el push; Sales lee 78 % en WhatsApp pero su volumen va por email a recurrentes (0.21 %).", "Cada equipo mueve su volumen al canal que le responde: Sales su email a push y WhatsApp (0.21 % a 1.2 % y 78 %), Collections su email a push (1.1 a 3.6 %)."),
 "Dentro de cada equipo la respuesta varía": ("Hay equipos buenos y equipos malos.", "audiencia", "La varianza está dentro del equipo: Marketing promedia 0.62 % con piezas de 0.1 a 3 %. Lo que separa una pieza de otra es su audiencia (Veriff con señal contra Referral a Leads), no el equipo que la manda.", "Sales rehace su email entero (ninguna pieza arriba de 0.6 %); Marketing y Product Growth apagan la mitad de sus piezas (debajo de 0.32 y 0.25 %) y replican la audiencia de las de arriba."),
 "Active y Precobranza responden": ("Leads necesita más toques porque todavía no conoce el producto.", "audiencia", "Active y Precobranza responden 3 a 10 veces más y reciben 4 % de los envíos; Leads y Recurrent sin señal reciben 58 %. El volumen está invertido respecto a la respuesta porque se manda por tamaño de lista.", "Leads y Recurrent solo con oferta probada y prueba al 10 %: 20 % menos volumen (80 M) con la misma respuesta total, porque lo que se quita va a quien no responde."),
 "10 piezas concentran 125 M envíos": ("Las 10 piezas más grandes son las más importantes.", "audiencia", "Son masivos sin segmento de Product Growth (Tasa0 a registrados, NeverActive), NewProducts (BillPay) y Marketing (Referral, Newsletter): 19 % del volumen con respuesta debajo del mínimo. Las 6 a proteger son segmentadas.", "Apagar o rehacer las 10 quita 125 M envíos (19 %) que aportan menos de 10 % de los clics de email; Veriff se protege y baja a 1 email al día."),
 "0 de 3,228 Canvas tienen grupo de control": ("El lift de Braze se puede medir con lo que hay.", "medicion", "Nadie activó el grupo de control que Braze ofrece en cada Canvas ni corrió una prueba A/B de mensaje: la conversión que se reporta es correlación con usuarios que ya iban a convertir.", "Control del 10 % en toda pieza: en 4 semanas se sabe el lift de las 20 piezas más grandes; lo que da cero se apaga con datos y el ahorro de 1.6 M MXN al mes pasa de techo a medición."),
 "749 piezas sin ticket": ("La nomenclatura se cumple y permite auditar.", "operacion", "749 piezas sin ticket, 731 formas de escribir la audiencia y 171 pruebas a usuarios reales: no hay revisión antes de activar ni dueño del catálogo en Braze.", "Nombre y ticket obligatorios y roles de aprobación: 171 pruebas (7.26 M envíos) no llegan a usuarios reales y 100 % del volumen se audita por equipo."),
 "582 campañas a tocar": ("Si se apagan las 48 con señal y se segmentan las masivas, el ahorro es 1.6 M MXN al mes.", "audiencia", "El ahorro sale de donde está el desperdicio: WhatsApp a mudos y bloqueados, email a quien nunca respondió, push repetido. Es un techo porque supone apagar todo lo que tiene señal.", "1.6 M MXN al mes (19 M al año), 27 M mensajes menos al mes y cerca de 50 mil bajas menos al mes si se ejecuta en 30 días."),
 "Product Growth tiene 81 % del ahorro": ("El ahorro se reparte parejo entre equipos.", "audiencia", "Product Growth concentra el WhatsApp a churn y el email Tasa0 masivo; Marketing tiene el volumen a bajar frecuencia (Referral, Newsletter, Rescate); Sales rehace su email. Collections no entra sin Legal.", "Product Growth solo con apagar 17 campañas: 1.04 M MXN al mes desde la semana 1; Marketing 0.16 M y Sales 0.10 M."),
 "Diez piezas con acción concreta": ("Si cada pieza tiene dueño y acción, 125 M envíos se corrigen en dos semanas.", "audiencia", "Las diez piezas salen de las láminas anteriores: masivos sin segmento, repetidos y a quien no responde. Cada acción tiene una regla con datos detrás.", "125 M envíos corregidos en dos semanas: cerca de 14 M mensajes menos al mes y 0.9 M MXN al mes del ahorro total."),
 "El playbook en 12 reglas": ("Si las reglas viven en Braze (exclusiones, frequency cap, calendario), el desorden no vuelve.", "operacion", "El desorden viene de que cada equipo opera Braze por separado sin reglas comunes ni dueño: 5 equipos, 5 formas de nombrar, segmentar y mandar.", "Las 12 reglas cubren las causas de 15 de los 19 indicadores en rojo; cargadas en Braze no dependen de que cada equipo se acuerde."),
 "Qué mandar por tipo": ("El canal, el día y la frecuencia de cada tipo de mensaje se decide con datos, no por costumbre.", "canal", "Hoy cada equipo elige canal y día por costumbre; los datos de respuesta por tipo, canal y tamaño ya dicen qué funciona.", "Cada pieza nueva nace con canal, día y veces decididos: respuesta esperada por tipo entre 1.5 y 5 %, no 0.2 a 0.5 %."),
 "Dieciocho ajustes de Braze": ("Si los ajustes se configuran una vez a nivel cuenta, protegen todas las piezas sin depender de cada equipo.", "operacion", "Los 18 ajustes atacan las causas de las láminas anteriores: exclusiones, frequency cap, canal preferido, grupo de control, validación de número. Hoy ninguno está activo.", "Frequency cap, exclusiones y control nativo protegen el 100 % de las piezas desde el día que se configuran; el ahorro deja de depender de revisar pieza por pieza."),
 "Un dueño por cosa y un calendario único": ("Con dueño por segmento, pieza y calendario, los choques y masivos sin segmento desaparecen.", "solape", "Los choques y repeticiones vienen de que nadie es dueño del calendario ni de los segmentos: 481 combinaciones de segmento sin dueño y piezas a 'Todos' que se activan sin ver las del otro equipo.", "Con calendario y comité quincenal no hay dos piezas a 'Todos' el mismo día: los choques de 3 o más campañas (9 % de los usuario-días, 24 % de los mensajes) bajan a cero por diseño."),
 "Plan a 90 días": ("Limpiar primero (apagar), configurar después (Braze) y medir al final (control) da resultados desde el primer mes.", "operacion", "El orden sigue a la causa: el desperdicio se apaga sin configurar nada; las reglas evitan que vuelva; el control mide lo que queda.", "Mes 1: cerca de 1.0 M MXN al mes de ahorro solo con apagar. Mes 2: reglas en Braze. Mes 3: primer lift medido."),
 "No hacer nada cuesta": ("Si no se actúa, el costo y las bajas siguen al ritmo de junio a septiembre.", "audiencia", "19 M MXN al año salen del costo variable actual de mensajes a mudos, bloqueados y repetidos; 50 mil bajas al mes salen de los masivos a Leads y 'Todos'.", "Cada mes sin actuar cuesta 1.6 M MXN y 50 mil usuarios que dejan de ser alcanzables por email; en un año, 19 M MXN y 600 mil bajas evitables."),
 "Lo que todavía no sabemos": ("Cada pregunta abierta tiene un dato que la resuelve.", "medicion", "Lo que falta no es análisis sino datos que hoy no existen: costo fijo de Braze, grupo de control, hora de envío, rebotes, canal preferido.", "Con hora, dispositivo y rebotes en Databricks y control en Braze, en 60 días se responden 6 de las 8 preguntas."),
 "Próximos pasos": ("Si cada tarea tiene dueño y fecha esta semana, el plan de 30 días arranca sin esperar a Braze.", "operacion", "Las tareas de la semana atacan las causas con más peso: masivos sin segmento, WhatsApp a quien no lee, exclusiones, pruebas a usuarios reales.", "Si las 8 tareas se cumplen, el ahorro empieza en la semana 1 y el primer lift se lee en el mes 2."),
 "Método: 18 extracciones": ("El modelo se puede reproducir y auditar sin acceso a Braze.", "metodo", "Todo sale de extracciones agregadas de Databricks; cambiar un parámetro recalcula el plan y las 471 verificaciones detectan si algo no cuadra.", "Cualquier cambio de parámetro (costo, mínimo, ventana) recalcula el plan y las láminas en minutos."),
 "Estándares: los 24 indicadores": ("Los estándares son el piso de la industria, no una meta de Kueski.", "metodo", "Cada indicador en rojo tiene una lámina que atribuye la causa: masivos sin segmento, frecuencia, canal mudo, falta de control.", "Con las 12 reglas, en 90 días 10 de los 19 en rojo pueden pasar a verde."),
 "Por mes: envíos, respuesta, bajas y costo": ("Junio es el mes que no se debe repetir; septiembre, el que sí.", "saturacion", "Junio concentra las piezas nuevas de push, BillPay Intro por email y el pico de bajas; septiembre tiene menos volumen y mejor respuesta.", "Repetir septiembre y no junio: 65 M al mes con 2.1 % de apertura de push y 5 M MXN de costo, contra 109 M, 1.05 % y 9.7 M MXN."),
 "Por día de la semana: volumen": ("El día de la semana no explica la respuesta.", "audiencia", "El tamaño de la pieza por día sí: el lunes salen las masivas de Product Growth y Marketing; el fin de semana, las segmentadas.", "Regla de tamaño por pieza, no de día: el lunes responde como el resto de la semana."),
 "Segmentos registrados en Braze": ("Los segmentos de Braze reflejan a quién se manda.", "operacion", "13 % del volumen no se rastrea y pocos segmentos concentran el volumen: los segmentos no tienen dueño ni nomenclatura.", "Etiquetar Not Tracked (85 M) y 30 segmentos maestros: 100 % del volumen con segmento auditable."),
 "Supuestos y dónde está cada cosa": ("Los supuestos son explícitos y cambiarlos cambia el resultado, no la conclusión.", "metodo", "Los supuestos cubren lo que no está en los datos: costo por mensaje, ventana de respuesta, costo fijo de Braze.", "Si WhatsApp se cobra por enviado y no por entregado, el ahorro del plan en WhatsApp sube cerca del doble."),
}
# Tipo de causa y efecto para las láminas que ya traen hipótesis y causa escritas en el bloque 2
HC_EXTRA = {
 "Semana a semana: push triplicó": ("saturacion", "Push vuelve solo con bajar el volumen (julio: apertura 1.77 %); WhatsApp solo con cambiar la base: 10 puntos de lectura (64 a 74 %) que no se recuperan mandando menos."),
 "El salto de push de junio": ("saturacion", f"Un push a 'Todos' por semana en todo Kueski y recordatorios solo a quien no abrió: la mitad de esos {_CP['new_env']/1e6:.0f} M push, a la apertura de las piezas existentes ({_CP['old_open']:.1f} %), habría dado {_CP['new_env']/2*_CP['old_open']/100/1e3:.0f} mil aperturas contra {_CP['new_env']*_CP['new_open']/100/1e3:.0f} mil."),
 "WhatsApp bajó de": ("audiencia", f"Churn y rezagados son {_G2['Leads rezagados']['share']+_G2['Churn e inactivos']['share']:.0f} % de lo entregado de julio a septiembre ({(_G2['Leads rezagados']['deliv']+_G2['Churn e inactivos']['deliv'])/3e6:.1f} M MXN al mes); por push cuestan cero y la lectura del canal vuelve arriba de 67 %."),
 "Ocho familias de email generan": ("audiencia", f"Detener Referral y NarrativaTasa0 y meter Tasa0 a nuevos en la bienvenida evita {(_CB['top'][0]['bajas']+_CB['top'][1]['bajas']+_CB['top'][4]['bajas'])/1e3:.0f} mil bajas en 9 meses y cerca de 55 M emails."),
}
for _s in SLIDES:
    if _s.get("kind") != "content":
        continue
    t = _s.get("title", "")
    if not _s.get("hipotesis"):
        for _k, (_h, _tag, _c, _i) in HC.items():
            if t.startswith(_k):
                _s["hipotesis"], _s["causa_tag"], _s["causa"], _s["impacto"] = _h, _tag, _c, _i
                break
    if not _s.get("impacto"):
        for _k, (_tag, _i) in HC_EXTRA.items():
            if t.startswith(_k):
                _s["causa_tag"], _s["impacto"] = _tag, _i
                break
_SIN_HC = [i + 1 for i, _s in enumerate(SLIDES) if _s.get("kind") == "content" and not (_s.get("hipotesis") and _s.get("causa_tag") and _s.get("impacto"))]
