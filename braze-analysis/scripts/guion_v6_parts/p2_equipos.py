"""Guion v6, sección III (equipos). Láminas 20 a 31 de la numeración global (se agregó una lámina).

Cifras nuevas: scripts en v6parts/p2work (base.py, t1 a t7). Costo = email 0.05 MXN por enviado + WhatsApp 1.00 MXN por entregado,
calculado desde E1 (no se usa la columna costo_mxn). Conversión = préstamo o solicitud de Cash en 7 días, repartida entre los
mensajes del día (conversiones_fraccional de E1): referencia, no prueba de que el mensaje vendió.
"Piso" = el mínimo que fijamos por canal: 0.3 % de clic en email, 0.75 % de apertura en push, 60 % de lectura en WhatsApp y 10 % de clic en in-app.
"""

PISO = "Piso: 0.3 % de clic en email, 0.75 % de apertura en push, 60 % de lectura en WhatsApp, 10 % de clic en in-app."

FICHA_VIZ = ("Ficha en tres bloques. Izquierda: puntos tema por canal (eje x = respuesta frente al piso del canal, tamaño = envíos, "
             "etiqueta = costo en MXN). Derecha: mejores y peores campañas con nombre, envíos, respuesta, costo, bajas y conversión de referencia. "
             "Abajo: a quién le escribe (barra apilada al 100 % por segmento) y qué cambiar.")

SECS = [
 dict(n="III", nombre="Los equipos aciertan con quien acaba de actuar y chocan en las bases frías",
      arg="Marketing y Product Growth ponen dos de cada tres mensajes. Los cinco equipos responden bien cuando escriben a quien acaba de hacer algo y mal cuando insisten con ofertas a quien no ha hecho nada, muchas veces sobre la misma persona y el mismo día que otro equipo.",
      subs=[
  dict(nombre="Qué manda cada equipo, a quién y dónde se cruzan", sl=[

   dict(
     t="Marketing y Product Growth ponen dos de cada tres mensajes, y la mayoría son ofertas a gente que no ha hecho nada reciente",
     tipo="Gráfica + lecturas",
     viz=("Mekko equipo por tema: ancho de cada columna = envíos del equipo; bloques = temas (Tasa 0, referidos, promociones de comercios KPay, "
          "Installments, recuperar inactivos, cobranza, avisos); color del bloque = parte que responde arriba del piso (color) o debajo (gris); "
          "etiqueta = costo del bloque en MXN. Los temas que mandan dos equipos (Tasa 0, inactivos y dormants, promociones de KPay) llevan el mismo contorno."),
     ctx=[
       ("Qué se manda", "Marketing: Tasa 0 a leads (32 % de su volumen y 51 % de su costo), referidos (25 % y 31 %) y promociones de comercios KPay como Comercio del día, Amazon, Hot Sale y Cuponera (25 % y 12 %). Product Growth: oferta de crédito e Installments (36 %), Tasa 0 a registrados (25 %), recuperar inactivos y churn (23 % del volumen y 36 % de su costo) y concursos como Anota y gana y Cuesta de enero (16 %). Todo promocional."),
       ("Quién", "Marketing (262 M envíos, 39 % del total, 27.2 M MXN, 47 % del costo) y Product Growth, que en Braze aparece como Lending (177 M, 27 %, 17.3 M MXN, 30 %)."),
       ("A quién", "Marketing: leads 28 %, leads fríos (rezagados y anónimos) 25 %, clientes 19 %. Product Growth: registrados sin crédito 38 %, clientes 29 %, inactivos y dormants 16 %, masivos a 'Todos' 12 %, churn de KPay 5 %."),
       ("Ejemplos", "PG B0211 Tasa 0 a registrados sin crédito: 34.9 M correos. Marketing B0171 Rescate Tasa 0 a leads rezagados: 16.4 M mensajes por email, push y WhatsApp. Marketing B0326 programa de referidos: 66.7 M mensajes."),
       ("Impacto", "Juntos: 66 % de los mensajes, 77 % del costo y 83 % del gasto de WhatsApp (Marketing 22.9 M MXN y PG 11.4 M)."),
     ],
     h=[
       "Se cruzan en dos temas: los dos mandan Tasa 0 (Marketing a leads, PG a registrados) y los dos le escriben a inactivos y dormants (PG con descuento directo, Marketing con referidos). Marketing además repite las promociones de KPay que manda Sales.",
       "Product Growth está mal en respuesta: 57 % de su gasto (9.9 M MXN) va a campañas que responden debajo del piso.",
       "Marketing está mal en costo y en bajas, no en respuesta: solo 11 % de su gasto está debajo del piso, pero su Tasa 0 cuesta 158 MXN por conversión de referencia (el promedio del equipo es 32.5) y su correo genera 5.9 bajas por mil, el doble que el resto.",
       "Los dos le escriben sobre todo a gente sin una acción reciente: 68 % del volumen de Marketing y 72 % del de PG.",
     ],
     sw="Dos equipos concentran el volumen y el gasto, mandan ofertas parecidas a las mismas bases y por eso chocan.",
     resp="Mandan ofertas: Tasa 0, Installments y descuentos (PG); Tasa 0, referidos y promociones de KPay (Marketing). Se cruzan en Tasa 0 y en inactivos (lámina 25). En PG está mal porque más de la mitad de su gasto no obtiene respuesta; en Marketing la respuesta llega al piso pero cada resultado cuesta más que en cualquier otro equipo y pierde el doble de suscriptores.",
     nota="Temas clasificados por el nombre de la campaña (scripts p2work/base.py). Costo con WhatsApp por entregado, desde E1. 'Debajo del piso' se mide por campaña y canal en los nueve meses, con 50 mil o más entregados. " + PISO,
     estado="rehacer", cierre=False),

   dict(
     t="Todos los equipos aciertan cuando escriben a quien acaba de hacer algo y fallan cuando insisten con quien no ha hecho nada",
     tipo="Gráfica + lecturas",
     viz=("Gráfica de pesas por equipo, alineada a la izquierda (no mapa de calor). Por equipo, dos puntos: parte del volumen que responde arriba del piso "
          "cuando va a quien hizo algo reciente y cuando va a quien no; tamaño del punto = envíos de cada grupo. Junto a cada punto, la campaña que más pesa ahí "
          "con su respuesta. Equipos ordenados por qué parte de su volumen va a gente sin acción reciente (PG 72 %, Marketing 68 %, Others 44 %, Sales 25 %, Collections 0 %)."),
     ctx=[
       ("Qué se manda", "Lo que funciona: recordatorios de algo que la persona empezó (registro, Veriff, Installments), precobranza y avisos de pago. Lo que no: Tasa 0, referidos, concursos y lanzamientos a bases que no han hecho nada."),
       ("Quién", "Los cinco equipos."),
       ("A quién", "Con acción reciente: dejó el registro a medias, cliente activo o recurrente, pago por vencer, acaba de pagar o de pedir. Sin acción reciente: leads, leads fríos, registrados sin crédito, inactivos, dormants, churn y masivos a 'Todos'."),
       ("Ejemplos", "PG: recordatorio de Installments a activos (B0301) 11 % de apertura en push contra Tasa 0 a registrados (B0211) 0.28 % de clic en 34.9 M correos. Marketing: recordatorio de Veriff (B0000) 3.04 % de clic contra referidos a dormants (B0326) 0.07 %. Sales: Quincenas sin intereses 4.2 % en push contra promociones a todo el portafolio por email (B0335) 0.22 %. Collections: precobranza 4.3 % de clic contra cobranza avanzada (BKT3) 0.14 %. Others: avisos de rechazo 18.6 % contra BillPay Intro a 16 M personas 0.11 %."),
       ("Impacto", "Con acción reciente responde arriba del piso 79 % del volumen; sin ella, 39 %. Son 364 M mensajes sin acción reciente, más de la mitad del total."),
     ],
     h=[
       "Product Growth: 72 % de su volumen va a gente sin acción reciente y ahí solo 29 % responde arriba del piso; cuando escribe a quien empezó algo, 74 %.",
       "Marketing: 68 % sin acción reciente, con 52 % arriba del piso (lo sube el WhatsApp, que se lee); lo que manda a quien dejó el registro a medias responde arriba del piso en su totalidad.",
       "Sales y Collections aciertan más porque casi todo va a clientes con relación viva: 75 % y 100 % de su volumen.",
       "Others muestra los dos extremos: sus avisos transaccionales responden 92 % arriba del piso y sus masivos a 'Todos' (BillPay, recomendaciones de Shopping) 27 %.",
     ],
     sw="El equipo no explica el resultado; a quién se le escribe, sí. Corregir es mover volumen de las bases sin acción reciente a quien acaba de hacer algo.",
     resp="Qué y quién: cada equipo tiene una campaña que funciona y otra que no, y la diferencia es a quién va. Por qué: quien acaba de hacer algo espera el mensaje; quien no ha hecho nada en meses lo ignora o se da de baja.",
     nota="Cálculo propio sobre 657 M envíos de campañas con 50 mil o más entregados (E1). Grupo según la audiencia del nombre de la campaña. 'Arriba del piso' por campaña y canal en los nueve meses. Las lecturas de WhatsApp incluyen las que se registran el mes siguiente al envío (ver notas). Sustituye al mapa de calor de seis medidas. " + PISO,
     estado="rehacer", cierre=False),

   dict(
     t="Dentro de cada equipo, el tema y el canal hacen que una campaña responda hasta treinta veces más que otra",
     tipo="Pequeños múltiplos",
     viz=("Franjas de puntos, una por equipo: cada punto es una campaña en un canal; eje x = respuesta frente al piso del canal (escala logarítmica, piso marcado en 1); "
          "tamaño = envíos; color = tema. Etiquetadas la mejor y la peor de cada equipo con el mismo producto o el mismo tema en otro canal."),
     ctx=[
       ("Qué se manda", "El mismo producto o la misma oferta, a públicos distintos o por canales distintos."),
       ("Quién", "Los cinco equipos."),
       ("A quién", "La campaña que responde va a quien ya empezó algo; la que no, a la base completa o fría."),
       ("Ejemplos", "Collections: precobranza 4.3 % de clic contra cobranza avanzada BKT3 0.14 % (30 veces). PG: Installments a activos que lo empezaron (B0301) 2.78 % contra Installments a registrados que nunca activaron (B0223) 0.10 % (28 veces, mismo producto). Marketing: referidos a leads de KCash por email 0.23 %, por in-app 14.7 % y por WhatsApp 87 % de lectura. Sales: Amazon a recurrentes por push 5.5 % contra Comercio del día de septiembre 0.93 %. Others: BillPay Intro por in-app 84.7 % contra 0.11 % por email."),
       ("Impacto", "En email, saber el equipo explica 12 % de la diferencia de respuesta entre campañas; saber a quién va, 54 %, y el tema, 52 %."),
     ],
     h=[
       "Las ofertas por email masivo casi no llegan al piso: Tasa 0 a registrados 0.28 %, referidos 0.22 %, promociones KPay 0.20 a 0.30 %, lanzamiento de BillPay 0.11 %. La excepción es la Tasa 0 de Marketing a leads rezagados (1 %), que a cambio pierde 9 suscriptores por mil.",
       "En push pasa lo mismo: recordatorio de registro 5.95 % y de Installments 11 %, contra rescates de Tasa 0 y de fin de semana de 0.55 a 0.76 % en 30 M envíos.",
       "El mismo mensaje cambia de canal y cambia de resultado: Anota y gana responde 76 % en in-app y 0.19 % por email; BillPay Intro 85 % y 0.11 %.",
       "Sales es la excepción por canal: por tema, su email no pasa de 0.32 % de clic y su WhatsApp a recurrentes se lee 78 %.",
     ],
     sw="La mejora no es cambiar de equipo dueño, es mover cada tema al público y al canal donde ya funciona.",
     resp="En dónde: en las campañas de oferta a bases sin acción reciente y, sobre todo, en el email masivo. Qué: el mismo producto (Installments, referidos, BillPay) funciona con quien ya lo empezó o por in-app y no funciona por correo a toda la base.",
     nota="Varianza explicada (ponderada por entregados) de la respuesta frente al piso entre 303 campañas de email con 50 mil o más entregados. En push: equipo 14 %, tema 38 %. Los factores se traslapan, no suman 100 %. " + PISO,
     estado="rehacer", cierre=False),

   dict(
     t="Marketing pierde a los usuarios nuevos en días; Product Growth pierde a la base vieja en meses",
     tipo="Gráfica + lecturas",
     viz=("Puntos por equipo y grupo (nuevos y base vieja): eje x = días hasta la baja (mediana), eje y = correos recibidos antes de irse, "
          "tamaño = personas que se dieron de baja, color = tema del correo que llegó el día de la baja. Líneas guía de un correo al día y de uno a la semana."),
     ctx=[
       ("Qué se manda", "El día de la baja llega, en nuevos: el recordatorio de registro (Veriff, datos personales, NIP), el rescate de Tasa 0 y el lanzamiento de BillPay. En la base vieja: Tasa 0 a registrados, referidos, Installments a quien nunca activó y descuentos a inactivos."),
       ("Quién", "Marketing y Product Growth; Others por un solo envío (BillPay Intro)."),
       ("A quién", "Nuevos: su primer correo llegó de febrero en adelante (158.5 mil bajas). Base vieja: ya recibían correo en enero (242.3 mil bajas)."),
       ("Ejemplos", "Marketing B0000 recordatorio de Veriff: 22.6 mil nuevos se fueron a los 4 días con 6 correos (mediana). PG B0211 Tasa 0 a registrados: 31.2 mil de la base vieja a los 128 días con 26 correos. PG B0223 Installments a quien nunca activó: 13.8 mil a los 178 días con 29 correos."),
       ("Impacto", "Marketing: 70 mil nuevos (44 %) y 95 mil de la base vieja (40 %). PG: 87.5 mil de la base vieja (36 %). BillPay Intro: 49 mil nuevos en un solo envío."),
     ],
     h=[
       "Nuevos: Marketing los pierde en 5 días con 10 correos, uno a dos al día. La mitad de esas bajas (35 mil) llega con el recordatorio de registro y otros 20 mil con el rescate de Tasa 0.",
       "Base vieja: Marketing en 64 días con 17 correos (referidos 44 mil, Tasa 0 35 mil); PG en 128 días con 31 correos, unos dos por semana (Tasa 0 a registrados, Installments a quien nunca activó, descuento a inactivos).",
       "Uno de cada tres nuevos se va con el primer correo y la mitad en el primer mes.",
     ],
     sw="Dos formas de perder a la misma persona: Marketing satura al recién llegado y Product Growth cansa durante meses a quien nunca pidió crédito.",
     resp="Marketing pierde por frecuencia sobre gente nueva; Product Growth por acumulación de ofertas de crédito que el usuario no pidió. Qué pesa más está en la lámina siguiente.",
     nota="E8 versión 3 y muestra_l_familias_baja.csv. Días = mediana ponderada; correos = promedio. Una baja cuenta en dos campañas si ese día le llegaron dos. BillPay: 58 mil bajas el día que llegó (49.3 mil nuevos y 9.1 mil de la base vieja) contra 37 mil atribuidas en E1; usamos 58 mil por día de la baja y lo anotamos (META['conflictos']).",
     estado="rehacer", cierre=False),

   dict(
     t="Lo que más provoca la baja es a quién le escribimos y con qué oferta, más que la frecuencia de la campaña o el canal",
     tipo="Gráfica + lecturas",
     viz=("Dispersión de campañas de email por mes: eje x = segmento, ordenado por bajas; eje y = bajas por mil correos entregados; tamaño = correos; color = tema. "
          "Panel lateral de puntos: qué parte de la diferencia en bajas explica cada factor (segmento, tema, equipo, veces que llega la campaña en el mes, tamaño del envío)."),
     ctx=[
       ("Qué se manda", "Las bajas altas vienen de recordatorios de registro diarios, lanzamientos masivos, referidos, Installments y Tasa 0. Avisos transaccionales y cobranza casi no generan bajas."),
       ("Quién", "Marketing (2.6 bajas por mil en sus campañas de email por mes) y Product Growth (1.5) concentran 73 % de las bajas medidas."),
       ("A quién", "Leads que dejaron el registro a medias: 4.1 bajas por mil. Leads fríos: 3.5. Leads: 2.4. Masivos a 'Todos': 2.1. Clientes activos: 1.7. Avisos transaccionales: 0.65. Cobranza: 0.25."),
       ("Ejemplos", "Recordatorio de registro de Marketing: 6 correos en 4 días hasta la baja. BillPay Intro: un solo correo a 16 M personas, 5.6 bajas por mil. Boletines de Marketing: 10 bajas por mil."),
       ("Impacto", "Promocional: 93 % de las bajas medidas con 77 % de los correos."),
     ],
     h=[
       "Entre campañas de email, el segmento explica la mitad de la diferencia en bajas (49 %), el tema 39 % y el equipo 26 %. Las veces que la misma campaña le llega a la persona en el mes explican 8 % y el tamaño del envío 9 %.",
       "Por tema: recordatorio de registro 4.0 bajas por mil, lanzamiento de BillPay 2.6, referidos 1.9, Installments 1.9, promociones KPay 1.8 y Tasa 0 1.8, contra 0.6 de avisos y 0.3 de cobranza.",
       "La frecuencia sí pesa cuando se acumula sobre el nuevo: quien se va en su primera semana recibió 4.4 correos en 3 días. La campaña de un solo envío al mes tiene más bajas (2.2 por mil) que la que llega 2 a 8 veces (1.3 a 1.7): son masivos a gente que casi no recibía correo.",
       "Canal: solo el email registra la baja. En push y WhatsApp no sabemos quién se va.",
     ],
     sw="Para perder menos gente hay que cambiar a quién y qué se manda; el tope de frecuencia ayuda sobre todo en el primer mes.",
     resp="El principal motor es a quién le escribimos: gente sin relación reciente o recién registrada que recibe promociones. En los nuevos lo agravan uno a dos correos al día del recordatorio de registro y un masivo de un solo envío (BillPay); en la base vieja, meses de ofertas de crédito. Canal: solo podemos medir email; para push y WhatsApp hace falta extraer bajas de push (opt out y desinstalación) y bloqueos de WhatsApp por campaña y mes.",
     nota="Cálculo propio: E1, 866 campañas de email por mes con 20 mil o más entregados; bajas por mil sobre entregados del mismo mes; varianza explicada ponderada por entregados. Quedan fuera 458 mil bajas registradas en meses sin entrega de esa campaña. Los factores se traslapan y no suman 100 %. Días y correos hasta la baja de E8.",
     estado="nuevo", cierre=False),

   dict(
     t="Dos equipos le mandan la misma oferta a la misma persona el mismo día: Tasa 0, descuentos y promociones de KPay",
     tipo="Gráfica + lecturas",
     viz=("Red de equipos: nodos = equipos (tamaño = envíos); líneas = usuario-días con dos promociones de equipos distintos el mismo día (grosor), "
          "etiquetada cada línea con el tema que se repite. Al lado, escalera: campañas distintas que recibe una persona en un día contra mensajes ese día y bajas por mil usuario-días."),
     ctx=[
       ("Qué se manda", "Tasa 0 de dos equipos, descuento directo y referidos al mismo dormant, y la misma promoción de comercio de KPay (Comercio del día, Amazon, Hot Sale, Cuponera) de Marketing y de Sales."),
       ("Quién", "Product Growth con Marketing, Marketing con Sales y Product Growth con NewProducts."),
       ("A quién", "Registrados sin crédito y anónimos (Tasa 0), inactivos y dormants (descuento y referidos), clientes recurrentes de KPay (promociones)."),
       ("Ejemplos", "PG B0211 Tasa 0 a registrados (email y push) con Marketing B0171 Rescate Tasa 0 a anónimos (push): 124 mil personas, cuatro a cinco días distintos en agosto. PG B0209 descuento directo a inactivos con Marketing B0326 referidos a dormants: 187 mil personas el mismo día por email y 171 mil con los dos WhatsApp el mismo día en marzo. Marketing B0495 Cuponera Hot Sale (email) con Sales B0493 Hot Sale (push): 0.53 M personas en cinco meses. PG B0440 Anota y gana con BillPay Intro (push): 1.23 M el mismo día de junio."),
       ("Impacto", "Entre equipos distintos ocurre 45 % de los choques entre promociones (41.7 de 92.4 M usuario-días en los mil pares con más coincidencias). Marketing y Sales: 14.3 M; Marketing y PG: 9.0 M."),
     ],
     h=[
       "Marketing y Sales mandan las dos Comercio del día (17.7 M y 13.1 M envíos), Amazon (7.8 M y 8.1 M), Hot Sale y Cuponera.",
       "Cuánto al día: con una campaña la persona recibe un mensaje; con tres o cuatro, 3.6; con ocho o más, 10. Uno de cada once usuario-días tiene tres o más campañas.",
       "Qué provoca: la baja pasa de 0.36 por mil usuario-días con una campaña a 0.42 con tres o cuatro y 0.70 con ocho o más, casi el doble. Con dos WhatsApp el mismo día se cobran dos mensajes si los dos se entregan.",
     ],
     sw="Sin dueño de la base fría ni de las promociones de KPay, cada equipo le escribe a la misma persona por su lado.",
     resp="Qué mandan: Tasa 0, descuentos, referidos y promociones de KPay. Cuánto: de uno a diez mensajes el mismo día. Qué provoca: más bajas (casi el doble con ocho o más campañas). No tenemos la respuesta ni la baja de cada par de campañas; se resuelve extrayendo, por par que coincide, respuesta y baja de quien recibió las dos contra quien recibió solo una.",
     nota="E6b (mil pares con más coincidencias, no el total) y E6a. Promociones según el tipo del catálogo. La respuesta por usuario-día sube con más campañas porque las reciben los usuarios más activos: no es efecto del choque. Conflicto conocido: 62 % (nota de solape) contra 46 % (deck); aquí 45 % solo entre promociones.",
     estado="rehacer", cierre=False),
  ]),

  dict(nombre="Una lámina por equipo", sl=[

   dict(
     t="Product Growth acierta cuando recuerda Installments a quien ya lo empezó y falla cuando ofrece Tasa 0 y crédito a quien nunca lo pidió",
     tipo="Ficha de equipo",
     viz=FICHA_VIZ,
     ctx=[
       ("Qué se manda", "Casi todo promocional. Oferta de crédito e Installments 36 % del volumen, Tasa 0 25 %, recuperar inactivos y churn 23 %, concursos y temporada (Anota y gana, Cuesta de enero, Navidad) 16 %."),
       ("Quién", "Product Growth (Lending en Braze): 186 campañas, contando cada una con todas sus versiones mensuales; 56 activas en septiembre. 177 M envíos y 17.3 M MXN."),
       ("A quién", "Registrados sin crédito 38 %, clientes activos y recurrentes 29 %, inactivos y dormants 16 %, masivos a 'Todos' 12 %, churn de KPay de 12 meses 5 %."),
       ("Temas por canal", "Email 117 M (66 % de su volumen) a 0.45 % de clic. Push 35.6 M a 2.10 %. WhatsApp 15.9 M a 61 % de lectura y 72 % de entrega, 11.4 M MXN (66 % de su costo). In-app 8.8 M a 46 %. Tasa 0: email 36.4 M a 0.28 %. Installments y crédito: email 43.3 M a 0.61 %, push 10.1 M a 4.4 %. Inactivos y churn: email 21.5 M a 0.47 %, WhatsApp 7.1 M a 57 % de lectura y 5.1 M MXN."),
       ("Mejores", "B0301 recordatorio de Installments a activos que lo empezaron: push 11.0 %, email 2.78 %, in-app 75 %; 18 conversiones de referencia por mil correos, 2.7 MXN por conversión. B0440 Anota y gana por in-app: 76 %. B0218 a recurrentes con plazo de menos de 15 días: push 6.4 %."),
       ("Peores", "B0211 Tasa 0 a registrados sin crédito: 34.9 M correos a 0.28 %, 1.75 M MXN, 656 MXN por conversión. B0223 Installments a registrados que nunca activaron: email 13.5 M a 0.10 % y WhatsApp 1.85 M a 55 % de lectura, 2,574 y 6,920 MXN por conversión. B0333 churn de KPay por WhatsApp: 1.71 M MXN, 51.5 % de lectura y 74 % de entrega. B0337 Cuesta de enero y B0440 Anota y gana por email: 7.4 M y 7.3 M a 0.19 %."),
       ("Bajas, costo y conversión", "3.15 bajas por mil correos; 87.5 mil personas de la base vieja se dieron de baja el día de un correo suyo, tras 128 días y 31 correos. 0.81 M conversiones de Cash de referencia, 21 MXN cada una: Installments 12, recuperar inactivos 68, Tasa 0 141."),
       ("Qué cambiar", "Tasa 0 a registrados y Installments a quien nunca activó: fuera del email masivo; in-app y push solo a quien abrió un push en 60 días, máximo dos al mes. Inactivos y churn: no apagar; ver la propuesta de churn. Ampliar el recordatorio de Installments a activos. Concursos por in-app, no por email."),
       ("Impacto", "57 % de su gasto (9.9 M MXN) en campañas debajo del piso; 39 % de su volumen salió cuando la campaña ya respondía debajo del piso el mes anterior."),
     ],
     h=[
       "Por qué no jala: ofrece crédito a quien no lo ha pedido. 72 % de su volumen va a gente sin acción reciente y ahí solo 29 % responde arriba del piso; con quien ya empezó algo, 74 %.",
       "Ni quien abre el correo de Tasa 0 convierte: 0.47 % contra 8.3 % normal en email.",
       "Churn sin app: el churn de KPay (B0333) lee WhatsApp (51.5 %) y casi no hace clic en email (0.10 %); el push solo llega a quien tiene la app (unos 31 mil al mes contra 56 mil por WhatsApp) y abre 0.6 %. In-app no le llega a quien no abre la app.",
       "Propuesta para churn y dormants: seguir escribiendo, con equilibrio. Un WhatsApp al mes solo a números que entregan y a quien leyó en 90 días, con oferta concreta y tope de presupuesto; un email al mes como canal barato; 10 % de grupo de control para medir si vuelven a comprar.",
     ],
     sw="El problema de Product Growth no es el canal ni el mensaje: es ofrecer crédito por email masivo a quien nunca lo pidió.",
     resp="Qué mandan: crédito (Installments, Tasa 0, descuentos) y concursos, casi todo por email. 'Familia' era nuestra palabra para una campaña con todas sus versiones mensuales; aquí decimos campaña. No jala porque se ofrece a registrados que nunca pidieron crédito y a clientes que dejaron Kueski hace meses. Al churn no se le deja de escribir: se le escribe poco, por WhatsApp a números que entregan y por email, con tope y grupo de control para saber si regresa.",
     nota="Costos con WhatsApp por entregado (E1). Conversión de referencia: préstamo o solicitud de Cash en 7 días; para el churn de KPay no mide compras con KPay, que es lo que se busca recuperar (extracción pendiente: compra con KPay a 30 días por usuario y campaña, con grupo de control). Usuarios por canal del churn: promedio mensual de E1, sin cruce por persona; quién tiene la app sigue sin dato (lámina 52). Conversión de quien abre B0211 de inventario B (EQU-09).",
     estado="rehacer", cierre=False),

   dict(
     t="Marketing gana con el recordatorio de registro y gasta la mitad de su dinero en Tasa 0 para leads que casi no convierten",
     tipo="Ficha de equipo",
     viz=FICHA_VIZ,
     ctx=[
       ("Qué se manda", "Todo promocional. Tasa 0 y rescate de leads 32 % del volumen y 51 % del costo; referidos 25 % y 31 %; promociones de comercios KPay (Comercio del día, Amazon, Cuponera, Hot Sale) 25 % y 12 %; recordatorio de registro (Veriff, datos personales, NIP) 7 % y 2.5 %; boletines, lanzamiento de pago de servicios y concursos, el resto."),
       ("Quién", "Marketing: 372 campañas con sus versiones, 70 activas en septiembre. 262 M envíos (39 %) y 27.2 M MXN (47 %)."),
       ("A quién", "Leads 28 %, leads fríos (rezagados y anónimos) 25 %, clientes activos y recurrentes 19 %, dormants 7 %, leads que dejaron el registro a medias 7 %, masivos 6 %."),
       ("Temas por canal", "Tasa 0: WhatsApp 18.6 M a 70 % de lectura y 12.8 M MXN; push 43.3 M a 0.85 %; email 19.9 M a 1.05 % con 8.8 bajas por mil. Referidos: email 29.2 M a 0.22 %, push 25.9 M a 1.12 %, WhatsApp 8.3 M a 72.5 % y 6.9 M MXN, in-app 3.2 M a 22 %. Promociones KPay: push 42.5 M a 0.86 %, email 17.4 M a 0.30 %. Recordatorio de registro: email 13.4 M a 3.08 %, push 3.2 M a 5.95 %, in-app 50 %."),
       ("Mejores", "B0000 recordatorio de Veriff: email 9.7 M a 3.04 %, push 5.83 %, 21 MXN por conversión de referencia. B0326 referidos a clientes que ya compraron con KCash: push 2.43 %, 17 conversiones por mil correos y 2.9 MXN cada una. Registro de línea MX por in-app: 86.6 %."),
       ("Peores", "B0171 Rescate Tasa 0 a leads rezagados por WhatsApp: 3.3 M MXN, solo llega 63 % y se lee 61.5 %, 844 MXN por conversión. B0171 NarrativaTasa0 por WhatsApp: 4.0 M MXN y 694 MXN por conversión; por email 9.1 bajas por mil. B0326 referidos a dormants por email: 7.0 M a 0.07 % (KCash) y 5.2 M a 0.05 % (KPay). B0171 Anónimos por push 8.9 M a 0.56 %; B0391 rescate de fin de semana por push 13.4 M a 0.76 %."),
       ("Bajas, costo y conversión", "84 % de su costo es WhatsApp (22.9 M MXN). 5.9 bajas por mil correos, el doble que el resto; 59 mil de los 80 mil correos promocionales a gente dada de baja son suyos. 0.84 M conversiones de Cash de referencia a 32.5 MXN cada una, el costo más alto de los cinco equipos: Tasa 0 158 MXN, referidos 22, recordatorio de registro 14."),
       ("Qué cambiar", "Tasa 0 por WhatsApp: tope de presupuesto mensual, solo a números que entregan y a quien leyó en 90 días, y grupo de control. Referidos: a clientes que ya compraron y por in-app; fuera del email a dormants y leads. Recordatorio de registro: protegerlo con tope de un correo al día y tres la primera semana. Promociones KPay: un solo dueño con Sales. Filtro de suscripción en cada paso del Canvas."),
       ("Impacto", "Sus campañas debajo del piso cuestan 2.9 M MXN (11 % de su gasto); el problema está en el costo por resultado y en las bajas."),
     ],
     h=[
       "¿Sirve? Como referencia, sí: 0.84 M préstamos o solicitudes de Cash en los 7 días siguientes a un mensaje suyo. Pero cada uno cuesta 32.5 MXN, contra 21 de Product Growth y 17 de Sales.",
       "Tasa 0 a leads rezagados se lee por WhatsApp pero no convierte: una conversión o menos por mil mensajes y entre 694 y 844 MXN por conversión.",
       "Lo que sí le regresa: recordatorio de registro y referidos a clientes que ya compraron, entre 3 y 21 MXN por conversión por email.",
       "No sabemos cuánto vende de KPay ni cuántos clientes nuevos traen los referidos: la conversión que tenemos es solo de Cash y no hay grupo de control.",
     ],
     sw="Marketing no necesita mandar más: necesita mover su dinero de WhatsApp a leads fríos hacia lo que ya le regresa.",
     resp="Temas: Tasa 0 a leads, referidos y promociones de KPay. Como referencia, sí deja transacciones (0.84 M de Cash), pero al costo más alto de la empresa y con el doble de bajas; Tasa 0 cuesta más de diez veces más por conversión que el recordatorio de registro. No sabemos su efecto en KPay ni en referidos, ni cuánto es incremental: falta extraer compras con KPay y altas por referido, y poner grupo de control.",
     nota="Lectura de WhatsApp de B0171 Rezagada: 61.5 % contando lecturas registradas el mes siguiente (E1) y 57.7 % sin ellas (muestra C); ver notas. Conversiones fraccionales de E1 (Cash, 7 días). 59 mil promocionales a dados de baja de MUESTRA_E.",
     estado="rehacer", cierre=False),

   dict(
     t="Sales manda promociones de comercios de KPay a sus clientes: funcionan por push y WhatsApp y no por email",
     tipo="Ficha de equipo",
     viz=FICHA_VIZ,
     ctx=[
       ("Qué se manda", "96 % promociones de comercios KPay: Comercio del día 15 %, códigos de descuento KUESKI 10 %, Hot Sale 10 %, Amazon 9 %, lanzamientos de comercios (Palacio de Hierro, Huawei, Gran Vía) 9 %, promociones a todo el portafolio (B0335) 8 %, Temu 6 %, Cuponera 5 %, cashback y Quincenas sin intereses 3 %. Todo promocional."),
       ("Quién", "Sales: 206 campañas con sus versiones, 30 activas en septiembre. 85 M envíos (13 %) y 7.1 M MXN (12 %)."),
       ("A quién", "Clientes recurrentes de KPay 74 %, leads 15 %, portafolio inactivo 8 %."),
       ("Temas por canal", "Push 50.6 M (59 %) a 1.23 %. Email 23.8 M a 0.21 %, el peor de la empresa. WhatsApp 7.4 M a 78 % de lectura y 80 % de entrega, el mejor; 5.9 M MXN. In-app 3.5 M a 8.1 %, debajo del piso de 10 %."),
       ("Mejores", "B0415 Amazon a recurrentes: push 5.5 %. B0345 Quincenas sin intereses: push 4.2 %. B0416 Flash Sale Amazon y B0396 lanzamiento Huawei por WhatsApp: 87 a 88 % de lectura."),
       ("Peores", "B0335 promociones a todo el portafolio activo e inactivo por email: 6.4 M a 0.22 %. Temu, Amazon y códigos KUESKI por email: 0.03 a 0.09 %. Comercio del día por push: 7 a 9 envíos por persona al mes, 0.93 % en septiembre."),
       ("Bajas, costo y conversión", "3.76 bajas por mil correos; 10.7 mil bajas en la base vieja tras 39 correos. 83 % de su costo es WhatsApp. A 90 días quien abre convierte 1.55 veces más que quien no (mediana); solo 26 de 177 campañas mantienen 2 veces o más. 13 M envíos a tarjetas KPay congeladas."),
       ("Qué cambiar", "Email solo para comercios; promociones por push y WhatsApp a recurrentes que leen. Comercio del día: máximo dos push por semana y solo a quien abrió un push en 60 días. Excluir tarjetas congeladas. Un calendario y un dueño de promociones KPay con Marketing."),
       ("Impacto", "65 % de su volumen responde arriba del piso; lo que queda debajo es casi todo email."),
     ],
     h=[
       "Manda lo mismo que Marketing en KPay: Comercio del día, Amazon, Hot Sale y Cuponera, a veces el mismo día a la misma persona.",
       "Su email queda en 0.21 % de clic; por tema va de 0.08 % (Temu) a 0.32 % (Comercio del día), cuando por push esas mismas promociones abren 1 a 1.9 %.",
       "Su WhatsApp a recurrentes es el que mejor se entrega y se lee de la empresa.",
     ],
     sw="Sales ya sabe a quién escribirle; le sobra el email y le falta tope en el push diario.",
     resp="Promociones de comercios que aceptan KPay (Comercio del día, Amazon, Hot Sale, Temu, Cuponera, lanzamientos de tiendas) a sus clientes recurrentes, casi todo por push.",
     nota="No medimos compras con KPay: las 0.43 M conversiones de referencia de Sales son préstamos de Cash. Extracción pendiente: compra con KPay a 7 y 30 días por usuario y campaña. Envíos a tarjetas congeladas: inventario B (EQU-21). Lift a 90 días: muestra K.",
     estado="rehacer", cierre=False),

   dict(
     t="Collections enseña a escribir con una razón; lo que puede mejorar es la cobranza avanzada por email",
     tipo="Ficha de equipo",
     viz=FICHA_VIZ,
     ctx=[
       ("Qué se manda", "Cobranza: precobranza antes del vencimiento y cobranza por etapa de atraso (BKT1 a BKT6) de KCash, KPay e Installments."),
       ("Quién", "Collections: 23 campañas, 22 activas en septiembre. 44.7 M envíos (7 %) y 1.6 M MXN (3 %). No usa WhatsApp."),
       ("A quién", "Cartera con un pago por vencer o vencido (99.5 %)."),
       ("Temas por canal", "Email 32.4 M (72 %) a 1.09 % de clic; push 12.2 M a 3.61 %."),
       ("Mejores", "Precobranza de KCash: email 4.3 % y push 5.3 %, de lo mejor de la empresa con millones de envíos. Precobranza de KPay: 2.5 % y 3.4 %. BKT1 por push: 3.1 %."),
       ("Peores", "BKT2 a BKT6 por email: 12.1 M correos a 0.11 a 0.18 % de clic, con 4 a 7 correos por persona al mes. BKT1 por email: 10.2 M a 0.41 %, contra 3.1 % del mismo BKT1 por push."),
       ("Bajas, costo y conversión", "0.25 bajas por mil correos, menos de la mitad que lo transaccional y 24 veces menos que Marketing. Su resultado es el pago y no está en los datos."),
       ("Qué aprendemos", "Escribir por un evento con fecha (el vencimiento), solo a quien le aplica y con una acción clara. Por eso responde más y casi nadie se da de baja."),
       ("Qué cambiar", "Cobranza avanzada primero por push y menos correos por persona; archivar los Canvas PRUEBA_ que llegaron a 5,166 personas reales dadas de baja; ticket propio por etapa en vez de T000; revisar con Legal los 61 mil envíos a REUS o ARCO; medir pago por canal."),
       ("Impacto", "72 % de su volumen responde arriba del piso; la parte que no, es casi toda email de BKT2 en adelante."),
     ],
     h=[
       "Le escribe a cada persona 3.86 veces al mes con la misma campaña, el doble que los demás equipos: en cobranza avanzada eso ya no suma respuesta.",
       "El mismo BKT1 responde casi ocho veces más por push que por email.",
       "24 % de su volumen salió cuando la campaña ya respondía debajo del piso el mes anterior: casi todo BKT2 a BKT6 por email.",
     ],
     sw="Lo que hace Collections (razón, fecha, público exacto) es la regla que deberían seguir los equipos promocionales.",
     resp="Sí: la cobranza avanzada por email repite mucho y responde poco, y sus pruebas llegaron a usuarios reales. Lo que aprendemos: un mensaje con una razón y una fecha responde más y no cansa.",
     nota="La respuesta de cobranza no se juzga solo por clic: falta el pago por canal y etapa (extracción pendiente con Collections). PRUEBA_ a usuarios reales: MUESTRA_E. REUS o ARCO: inventario B (AUD-08). Toques por persona: inventario B (EQU-22). Se quitó 'BKT1 a BKT3 no refrescan audiencia': no encontramos la fuente.",
     estado="rehacer", cierre=False),

   dict(
     t="En Others, el mismo lanzamiento de BillPay funcionó en in-app y falló por email a toda la base",
     tipo="Ficha de equipo",
     viz=FICHA_VIZ,
     ctx=[
       ("Qué se manda", "Mitad transaccional (51 %: confirmaciones de pago, rechazos, contratos, estados de cuenta, desembolsos, domiciliación) y mitad promocional: lanzamiento de BillPay y recargas 29 %, boletín y recomendaciones semanales de Shopping 10 %, campañas con nombre QA o 'Copy of' 4 %."),
       ("Quién", "Others agrupa NewProducts (BillPay, recargas), transaccional, Shopping, Compliance, CX, Acquisition y QA. 283 campañas, 92 activas en septiembre. 98 M envíos (15 %) y 4.4 M MXN (8 %). La mitad de sus envíos no trae ticket."),
       ("A quién", "Un evento del usuario (transaccional) 52 %, masivos a 'Todos' 35 %, sin segmento en el nombre 8 %."),
       ("Temas por canal", "Avisos: email 41.8 M a 2.75 % y 0.88 bajas por mil, push 8.0 M a 6.2 %. BillPay y recargas: email 16.4 M a 0.11 % y 5.6 bajas por mil, push 10.1 M a 0.91 %, in-app 1.9 M a 84 %. Boletín y Shopping: email 9.4 M a 0.29 %."),
       ("Mejores", "Rechazos por email: 18.6 %. Payment Received por push: 14.2 %. Payment Confirmation por email: 9.3 M a 3.8 %. BillPay Intro por in-app: 1.5 M a 84.7 %. Recordatorio de creación de cuenta de Acquisition (T2706): 3.85 % de clic, aunque con 3.1 bajas por mil."),
       ("Peores", "BillPay Intro por email a 16.1 M personas en junio: 0.11 % de clic, 0.81 M MXN y 58 mil bajas el día que llegó. BillPay Reminder por push: 4.8 M a 0.65 %. Shopping Weekly Recommendations: 7.0 M correos a 0.12 %, casi cuatro por persona al mes. QA-KPay recordatorio de registro telefónico: push a 1.87 M personas reales con 0.01 %."),
       ("Bajas, costo y conversión", "2.23 bajas por mil correos. BillPay Intro explica 31 % de las bajas de usuarios nuevos del año (49 mil). La conversión de referencia de Others es casi toda transaccional de Cash, que sigue al préstamo: no es efecto del mensaje. No medimos pagos de servicios con BillPay."),
       ("Qué cambiar", "Avisos transaccionales: no tocar, solo ponerles ticket. Lanzamientos: in-app primero; por email solo a quien abrió algo en 90 días, probando con 5 % y un tope de bajas por mil antes de escalar. Shopping: una vez al mes o solo a quien hizo clic en 90 días. QA y copias: audiencia de prueba y archivar."),
       ("Impacto", "Sus avisos responden 92 % arriba del piso; sus masivos a 'Todos', 27 %."),
     ],
     h=[
       "Lo bueno: avisos transaccionales por email y push, y el lanzamiento por in-app.",
       "Lo malo: un correo a toda la base sin filtro, recomendaciones semanales que nadie abre y pruebas que llegan a clientes.",
       "El canal decidió el resultado del mismo mensaje: BillPay Intro respondió 84.7 % en in-app y 0.11 % por email.",
     ],
     sw="Others prueba que el mensaje de lanzamiento sí interesa; lo que falló fue mandarlo por correo a 16 M personas.",
     resp="Lo bueno son los avisos transaccionales (email y push) y los lanzamientos por in-app. Lo malo son los lanzamientos y las recomendaciones por email a toda la base, el push de recordatorio de BillPay y las pruebas a usuarios reales.",
     nota="Others sigue el mapeo del deck (Acquisition, Compliance, CX, Shopping y NewProducts en Others; B2B en Sales). Bajas de BillPay: 58 mil por día de la baja (E8) contra 37 mil atribuidas (E1), conflicto ya anotado. QA y copias: MUESTRA_F.",
     estado="rehacer", cierre=False),
  ]),

  dict(nombre=None, sl=[
   dict(
     t="Por qué pasa: cada equipo persigue su meta con su canal, sin ver el costo ni lo que mandan los demás",
     tipo="Cierre de sección",
     viz="Cierre: cadena de causas (5 porqués), hipótesis analítica, operativa y de gobierno, cómo (semana, dónde en Braze, equipo, métrica) y qué ganamos.",
     ctx=[
       ("Qué se manda", "Ofertas de crédito y promociones de KPay a bases sin acción reciente, por varios equipos a la vez."),
       ("Quién", "Los cinco equipos; sobre todo Marketing y Product Growth."),
       ("A quién", "Registrados sin crédito, leads, inactivos, dormants y churn, que no tienen un dueño."),
       ("Ejemplos", "Tasa 0 de PG y de Marketing el mismo día; Comercio del día de Marketing y de Sales."),
       ("Impacto", "Con acción reciente responde arriba del piso 79 % del volumen; sin ella, 39 %."),
     ],
     h=[
       "Porqués: cada equipo tiene meta de producto (créditos, compras KPay, registros), no de respuesta ni de costo por resultado; mide su canal por separado; nadie ve qué recibe la persona de otros equipos; las bases frías y las promociones de KPay no tienen un solo dueño.",
       "Hipótesis analítica: el resultado depende de a quién y qué se manda, no del equipo. Operativa: dos equipos con la misma oferta sobre la misma base. De gobierno: sin dueño por base, sin calendario y sin tope de gasto por equipo.",
       "Cómo: semanas 1 y 2, tablero común por equipo con costo por respuesta, bajas por mil y conversión de referencia; semanas 3 y 4, Product Growth dueño de inactivos, dormants y churn, y un dueño de promociones KPay entre Marketing y Sales; en Braze, tope mensual de WhatsApp por equipo y calendario compartido para envíos a más de 1 M.",
       "Métrica: parte del volumen que responde arriba del piso por equipo y bajas por mil correos, revisadas cada semana.",
     ],
     sw=None,
     resp="Sin cambio de fondo: es el cierre que el usuario aprobó, con las causas de esta sección.",
     nota=None,
     estado=None, cierre=True),
  ]),
 ]),
]
