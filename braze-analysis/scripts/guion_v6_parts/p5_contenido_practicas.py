"""Parte 5 del guion v6: secciones VIII (contenido y campañas), IX (malas prácticas) y X (buenas prácticas).

Láminas 64 a 82 de la numeración global, más una nueva (66b). Cifras recalculadas con pandas sobre data/*.csv;
WhatsApp siempre por ENTREGADO. Scripts en scratchpad/v6parts/p5/. Detalle de cálculo en p5_contenido_practicas_notas.md.
Glosario usado en pantalla (sin jerga inventada):
- "campaña" = una comunicación con todas sus versiones mensuales (en las notas técnicas se llama familia).
- "versión" = cada copia de la campaña que se relanza con otra fecha en el nombre.
- "piso" = respuesta mínima que fijamos por canal: 0.3 % de clic en email, 0.75 % de apertura en push, 60 % de lectura en WhatsApp, 10 % de clic en in-app.
"""

PISO = "0.3 % de clic en email, 0.75 % de apertura en push, 60 % de lectura en WhatsApp y 10 % de clic en in-app"

SECS = [
 dict(n="VIII", nombre="Qué mandamos: un puñado de campañas concentra el volumen, el gasto y las bajas",
      arg="Unas cuantas campañas masivas, casi todas promocionales y dirigidas a gente sin crédito, pesan más que todo lo demás. En vez de medirlas, las copiamos cada mes. Llamamos campaña a una idea con todas sus versiones: 1,071 campañas enviaron algo en el año.",
      subs=[dict(nombre=None, sl=[

   dict(
     t="Casi la mitad de los mensajes del año fue en campañas que casi nadie responde: Tasa 0, promociones de comercios y referidos",
     tipo="Gráfica + lecturas",
     viz="Matriz de burbujas tema por equipo, solo campañas que responden menos que el piso: tamaño = mensajes, color = sigue activa en septiembre o ya se detuvo; columna lateral con MXN por tema. Arriba, franja del semáforo completo (no responde, revisar, proteger, ampliar, normal) con mensajes y MXN.",
     ctx=[
       ("Qué se manda", "Promocional. Tasa 0 de KCash (68 M mensajes), promociones de comercios KPay (64 M), referidos (35 M), lanzamiento de BillPay (30 M) y ofertas para que vuelva el inactivo (18 M)."),
       ("Quién", "Marketing 110 M mensajes (40 %), Product Growth 104 M (37 %, pero 52 % del dinero), Others 33 M (BillPay y Shopping), Sales 29 M."),
       ("A quién", "Leads que no terminaron su registro (94 M, 34 %), registrados que nunca tomaron crédito (72 M, 26 %), ex clientes inactivos (39 M, 14 % del volumen y 30 % del dinero), 'Todos' sin segmento (34 M) y activos (30 M)."),
       ("Ejemplos", "Lending-KCash-B0211 Nuevos_RegistradosPay-Tasa0: Tasa 0 de KCash por email a registrados de KPay sin crédito, 35 M emails, 0.25 % de clic. NewProducts T0000 BillPay_Intro: lanzamiento de BillPay a toda la base, 16 M emails en junio, 0.10 %. Marketing-KCash-B0326 Leads-ReferralProgram: invita a un amigo, a leads, 8.5 M emails, 0.20 %."),
       ("Impacto", "293 M mensajes (44 % del año) y 23.0 M MXN (40 % del gasto variable). La mitad ya se detuvo antes de septiembre; 89 campañas por canal seguían activas en septiembre con 28 M mensajes y 2.1 M MXN ese mes."),
     ],
     h=[
       "No responde (debajo del piso con volumen alto): 356 campañas por canal, 293 M mensajes, 23.0 M MXN. Revisar: 227, 135 M. Proteger (responden 1.5 veces la típica o más): 196, 121 M. Ampliar (chicas que responden el doble): 186, solo 4.2 M.",
       "Product Growth pone 37 % del volumen que no responde pero 52 % del dinero, porque ahí está el WhatsApp a ex clientes inactivos y a registrados sin crédito.",
       "Ex clientes inactivos son 14 % de estos mensajes y 30 % del dinero: se les escribe para recuperarlos, por eso la respuesta no es apagar sino cambiar canal y poner tope (lámina siguiente y 66b).",
       "De los 277 M promocionales que no responden, 137 M ya no enviaron en septiembre: el problema vivo son 89 campañas.",
     ],
     sw="El desperdicio no está repartido: está en pocas campañas masivas a gente que todavía no es cliente o que ya se fue.",
     resp="Temas: Tasa 0 (25 %), promociones de comercios KPay (23 %), referidos (13 %), BillPay (11 %). Equipos: Marketing 40 % y Product Growth 37 % del volumen; Product Growth concentra 52 % del dinero.",
     nota="Fuente: hallazgos/muestra_c_familias.csv (señal por campaña y canal), costo recalculado con WhatsApp por entregado (23.0 M MXN; con WhatsApp por enviado eran 29.8 M). Tema y etapa clasificados por el nombre con reglas en p5/common.py. Señal: debajo del piso y con envíos iguales o mayores a la mediana de su canal.",
     estado="rehacer",
   ),

   dict(
     t="Siete de los diez correos más grandes son promociones masivas a gente sin crédito: llevan 28 % del email y 7 % de los clics",
     tipo="Gráfica + lecturas",
     viz="Pareto de las 30 campañas de email más grandes: barras de correos entregados coloreadas por equipo, línea acumulada de volumen contra línea acumulada de clics; las 10 primeras con etiqueta de tema y a quién van. Panel chico igual para push.",
     ctx=[
       ("Qué se manda", "Promocional, salvo cobranza (BKT1) y la confirmación de pago KPay (transaccional). Tasa 0, BillPay, crédito en plazos, referidos, descuento para volver, sorteo AnotayGana y recomendaciones semanales de Shopping."),
       ("Quién", "Product Growth 4 de las 10 (19 % del email y 6 % de los clics), Others 3 (BillPay, Shopping, transaccional), Marketing 2 (Veriff y referidos), Collections 1."),
       ("A quién", "Registrados de KPay sin crédito KCash, registrados que nunca activaron, leads, ex clientes inactivos y 'Todos'."),
       ("Ejemplos", "B0211 Tasa 0 a registrados de KPay (Product Growth): 10.4 % del email, 3.2 % de los clics. B0223 NeverActive InstallmentsNoCash (Product Growth): 4.0 % del email, 0.4 % de los clics. S0004 WeeklyRecommendations (Shopping, en Others): 2.1 % y 0.3 %. En contraste, Retargeting_Veriff (Marketing) pesa 3.0 % y da 9.9 % de los clics."),
       ("Impacto", "Las 10 más grandes de 1,250 campañas de email son 37 % de los correos entregados y 30 % de los clics. Sin Veriff, la confirmación de pago y cobranza, las otras siete son 28 % del volumen y 7 % de los clics."),
     ],
     h=[
       "Las dos que sí responden son un recordatorio de registro (Veriff, 3.0 % de clic) y un transaccional (confirmación de pago, 3.8 %): van a alguien que acaba de hacer algo.",
       "Las siete que no responden hacen entre 0.10 % y 0.55 % de clic; el promedio de email es 0.93 %.",
       "En push pasa lo mismo: las 10 más grandes son 25 % del volumen y 15 % de las aperturas; siete son de Marketing a leads (RescateFinesDeSemana, RescateTasa0, Referidos, BillPay).",
     ],
     sw="El email masivo a quien no tiene crédito es la mayor parte del volumen y casi no aporta clics.",
     resp="Son siete campañas promocionales: tres de Product Growth (Tasa 0 a registrados de KPay, crédito en plazos a quien nunca activó, sorteo AnotayGana a todos), una más de Product Growth a ex clientes (descuento directo), una de Marketing (referidos a leads) y dos de Others (BillPay a toda la base y recomendaciones semanales de Shopping). Significa que una tercera parte del email se va en mensajes que casi nadie abre ni toca.",
     nota="Fuente: E1, email, clic sobre entregados por campaña sin fecha en el nombre (1,250 campañas de email). Los porcentajes son de correos entregados y de clics.",
     estado="rehacer",
   ),

   dict(
     t="Cinco campañas son la mitad del gasto que hoy no responde; cuatro son WhatsApp para recuperar a quien se fue o nunca empezó",
     tipo="Gráfica + lecturas",
     viz="Cascada del gasto de septiembre de las 89 campañas activas que no responden, una barra por campaña, color = canal, etiqueta = segmento; las cinco primeras nombradas. Al lado, tabla chica: costo por conversión de referencia por canal en las mismas campañas (WhatsApp contra email).",
     ctx=[
       ("Qué se manda", "Promocional de recuperación: Tasa 0 de KCash a leads rezagados, oferta con o sin cupón a clientes KPay sin compra en 12 meses, descuento directo a clientes KCash inactivos, crédito en plazos a registrados que nunca activaron y Tasa 0 por email a registrados de KPay."),
       ("Quién", "Marketing (RescateTasa0) y Product Growth (las otras cuatro)."),
       ("A quién", "Leads que no terminaron registro y quedaron rezagados; ex clientes KPay con 12 meses sin compra (churn); clientes KCash inactivos (dormant); registrados que nunca tomaron crédito."),
       ("Ejemplos", "Marketing-KCash-B0171 Leads_BBDDRezagada-RescateTasa0 por WhatsApp: 3.3 M MXN de abril a septiembre, 63 % de entrega, cerca de 60 % de lectura. Lending-KPay-B0333 Churn_12MesesInactividad por WhatsApp: 1.7 M MXN, 49 % de lectura. Lending-KCash-B0209 Recurrentes_Inactivos-DescuentoDirecto por WhatsApp: 1.5 M MXN. Lending-KCash-B0223 Nuevos_NeverActive por WhatsApp: 1.0 M MXN. Lending-KCash-B0211 Tasa 0 por email: 1.7 M MXN."),
       ("Impacto", "9.2 M MXN en el año, 40 % del gasto que no responde; en septiembre 1.0 M MXN de 2.1 M (49 %)."),
     ],
     h=[
       "En las mismas campañas el email cuesta mucho menos por conversión de referencia: descuento a inactivos 29 MXN por email contra 114 por WhatsApp; churn KPay 121 contra 1,176; RescateTasa0 88 contra 263.",
       "Entre uno de cada cuatro y la mitad de los WhatsApp a estas bases no se entrega (Meta no lo cobra, pero baja la calidad del número), y de lo entregado se lee cerca de 60 % o menos.",
       "Son programas de recuperación: no se trata de dejar de escribirles, sino de hacerlo por el canal barato que sí usan, con pocos toques, un tope de gasto y un grupo de control que diga si recuperan.",
     ],
     sw="Recuperar sí, pero no por WhatsApp masivo: email o in-app primero y WhatsApp solo a quien leyó uno en los últimos 90 días, con tope de presupuesto.",
     resp="Se les manda Tasa 0, descuentos y cupones para que vuelvan. Van a leads rezagados (Marketing) y a ex clientes inactivos de 6 y 12 meses y registrados que nunca activaron (Product Growth). Recomendación: mantener el programa con equilibrio: canal más barato que sí usan, máximo dos toques al mes, WhatsApp solo a quien lee, tope de gasto mensual y 10 % de control.",
     nota="WhatsApp por entregado. El ahorro mensual de la nota de campañas (868 mil MXN al mes solo en RescateTasa0) usaba WhatsApp por enviado; por entregado es unos 550 mil al mes en promedio y 174 mil en septiembre. Lectura de RescateTasa0: 57.7 % contando solo lecturas del mes del envío, 61.5 % sumando las que llegan el mes siguiente. Conversión de referencia: solicitud o préstamo de Cash en 7 días; en campañas KPay no mide la compra en KPay.",
     estado="rehacer",
   ),

   dict(
     t="Recuperar clientes sí vale, pero con medida: a 12 meses sin compra se convierte diez veces menos que a 3 y la oferta casi no cambia el resultado",
     tipo="Pequeños múltiplos",
     viz="Tres paneles (inactivos 3, 6 y 12 meses de KPay): barras de conversión por oferta (sin oferta, cupón, descuento en tasa, plazos con intereses). Cuarto panel: costo por conversión de WhatsApp por etapa (activos, leads, registrados sin crédito, ex clientes inactivos).",
     ctx=[
       ("Qué se manda", "Promocional de recuperación de KPay: el mismo Canvas con ramas sin oferta, con cupón, con descuento en tasa y con plazos con intereses, a veces solo para Amazon."),
       ("Quién", "Product Growth (Lending-KPay B0331, B0332 y B0333, 'ConSinOferta')."),
       ("A quién", "Ex clientes KPay: suaves (3 meses sin compra), duros (6 meses) y churn (12 meses). Pueden no tener la app."),
       ("Ejemplos", "B0331 Softnactive_3MesesInactividad, B0332 HardInactive_6MesesInactividad, B0333 Churn_12MesesInactividad."),
       ("Impacto", "14.9 M mensajes y 3.6 M MXN en el año (3.3 M en WhatsApp). Conversión de referencia: 0.67 % a 3 meses, 0.35 % a 6 y 0.06 % a 12."),
     ],
     h=[
       "Sin oferta convierte casi igual que con oferta: 0.60 % contra 0.66 a 0.75 % a 3 meses; 0.27 % contra 0.34 a 0.37 % a 6 meses; 0.05 % contra 0.05 a 0.07 % a 12 meses.",
       "Cada conversión de referencia por WhatsApp cuesta 17 MXN en activos, 79 en leads, 119 en registrados sin crédito y 191 en ex clientes inactivos.",
       "Las ramas sin oferta funcionan como un grupo de comparación de la oferta, no del mensaje: falta un grupo que no reciba nada para saber cuánto recupera el programa.",
     ],
     sw="La regla no es apagar: es gastar más donde todavía se recupera (3 meses) y poner tope y canal barato donde casi no (12 meses).",
     resp="Lámina nueva para el matiz pedido: a churn y dormants se les escribe para recuperarlos. Propuesta: inactivos de 3 meses con su secuencia completa; 6 y 12 meses con email o in-app, uno o dos toques al mes, WhatsApp solo a quien leyó uno en 90 días, tope mensual de gasto y 10 % de control.",
     nota="Fuente: E15 (embudo por paso de Canvas), conversión por rama sumando usuarios por paso; E1 para costo por conversión por etapa (etapa por el nombre de la campaña). Conversión de referencia (Databricks, sobre todo Cash); para KPay no captura la compra en KPay. Falta la extracción de quién tiene app (E18c).",
     estado="nuevo",
   ),

   dict(
     t="Ocho campañas de email generan un tercio de las bajas, y seis de ellas casi no reciben clics",
     tipo="Gráfica + lecturas",
     viz="Burbujas por campaña de email: correos entregados (x) contra bajas por mil (y), tamaño = bajas, color = equipo, etiqueta = tema y a quién va; línea de la campaña típica (1.7 bajas por mil).",
     ctx=[
       ("Qué se manda", "Promocional: lanzamiento de BillPay, Tasa 0 (dos), referidos, recordatorio de verificación (Veriff), sorteo AnotayGana, Cuesta de Enero y crédito en plazos."),
       ("Quién", "Product Growth 4 (163 mil bajas), Marketing 3 (136 mil), Others 1 (BillPay, 80 mil)."),
       ("A quién", "Toda la base (BillPay, AnotayGana), leads (referidos, NarrativaTasa0, Veriff, CuestaEnero) y registrados sin crédito (Tasa 0 a registrados de KPay, NeverActive)."),
       ("Ejemplos", "NewProducts BillPay_Intro (Others): 80 mil bajas, 5.6 por mil. Lending-KCash-B0211 Tasa 0 a registrados (Product Growth): 79 mil. Marketing-KCash-B0326 Leads-ReferralProgram: 54 mil, 6.7 por mil. Marketing-KCash-B0171 NarrativaTasa0 a base rezagada: 44 mil, 9.1 por mil. Retargeting_Veriff (Marketing): 38 mil."),
       ("Impacto", "379 mil eventos de baja de 1.09 M (35 %). Seis de las ocho tienen clic debajo de 1 %; las otras dos son Veriff (3.0 %) y NarrativaTasa0 (1.0 %)."),
     ],
     h=[
       "BillPay Intro se mandó una vez a 16 M personas en junio: fue el primer o segundo correo para casi la mitad de quienes se dieron de baja ese día.",
       "NarrativaTasa0 a leads rezagados genera 9 bajas por cada mil correos, cinco veces la campaña típica.",
       "Quien se da de baja del email ya no recibe nada por ese canal: cada una es un cliente que perdimos como contacto.",
     ],
     sw="Las bajas no salen de todo el email: salen de ocho envíos masivos que además casi no responden.",
     resp="BillPay Intro (Others, a toda la base), Tasa 0 a registrados de KPay, AnotayGana a todos, Cuesta de Enero a leads y NeverActive (Product Growth), y referidos a leads, NarrativaTasa0 a rezagados y Veriff (Marketing).",
     nota="Eventos de baja de E1 (1.09 M, incluye 458 mil registradas en meses sin entrega de esa campaña). Por campaña no hay usuarios únicos; el total de usuarios únicos dados de baja es 439 mil (ver conflictos). El 37 % del deck usaba otro denominador; recalculado da 35 %.",
     estado="rehacer",
   ),

   dict(
     t="Hay correos que la gente sí abre, pero los mandamos tan seguido que muchos se dan de baja",
     tipo="Gráfica + lecturas",
     viz="Dispersión de campañas de email: clic (x) contra bajas por mil (y), tamaño = correos por persona al mes, color = equipo; cuadrante marcado 'responde bien, pero se dan de baja' (clic arriba de la mediana 0.5 % y más de 2.5 bajas por mil).",
     ctx=[
       ("Qué se manda", "Recordatorios de registro (Veriff, datos personales, NIP, dirección), Tasa 0 y newsletters. Promocional y de activación."),
       ("Quién", "Marketing 22 de 33 campañas (26 M correos, 77 % de estas bajas), Others 8 (Acquisition KPay, cumpleaños), Product Growth 3."),
       ("A quién", "Sobre todo leads que acaban de empezar su registro (23 de 33)."),
       ("Ejemplos", "Marketing-KCash-B0000 Leads_LeftFunnel-Retargeting_Veriff: recuerda verificar la identidad, 3.0 % de clic, 3.9 bajas por mil, 5.3 correos por persona al mes. Retargeting_PersonalInfo: 3.0 % y 4.6. Acquisition-KPay-T2728 FaltaVeriff NIP con cupón: 2.8 % y 4.7."),
       ("Impacto", "33 campañas, 35.6 M correos, unas 141 mil bajas. Clic promedio 2.2 %, cuatro veces la campaña típica."),
     ],
     h=[
       "Se dan de baja 4 a 5 de cada mil que lo reciben; la campaña típica de email tiene 1.7.",
       "El contenido funciona (hacen clic); lo que molesta es la frecuencia: cinco correos al mes por persona en los recordatorios de registro.",
       "Aquí no se apaga: se baja a dos correos al mes y se deja de mandar a quien no abrió los últimos tres.",
     ],
     sw="'Quemar la base' quiere decir esto: un mensaje bueno que mandamos tantas veces que la gente se da de baja y ya no podemos volver a escribirle por email.",
     resp="Quemar es que la persona se dé de baja del email por recibir demasiados correos: después ya no podemos escribirle por ese canal. Pasa en 33 campañas que sí reciben clics, casi todas de Marketing a leads que empezaron su registro.",
     nota="Fuente: muestra_c_familias.csv, señal 'revisar' con motivo 'bajas altas' (2.5 bajas por mil o más con clic sobre la mediana). Bajas estimadas como bajas por mil por correos entregados. Mediana de bajas por mil de campañas de email con 100 mil+ envíos: 1.7.",
     estado="rehacer",
   ),

   dict(
     t="Uno de cada ocho correos responde bien, y casi todos son recordatorios, cobranza o transaccionales: los separa el tema, no el tamaño",
     tipo="Gráfica + lecturas",
     viz="Franja de puntos por tema (filas): cada punto es un correo (una versión con 200 mil o más entregados), x = clic, tamaño = entregados, color = equipo; líneas del piso (0.3 %) y de 'responde bien' (1.5 %). Columna lateral: cuántos responden bien por tamaño (200 a 500 mil, 0.5 a 1 M, 1 a 3 M, más de 3 M).",
     ctx=[
       ("Qué se manda", "Todo el email con volumen relevante: 308 correos de 200 mil o más entregados."),
       ("Quién", "Others (transaccionales) 45 % responden bien; Collections 31 %; Marketing 9 %; Product Growth 5 %; Sales 0 %."),
       ("A quién", "Los que responden bien van a quien está en un proceso: se registró, tiene un pago, acaba de pagar."),
       ("Ejemplos", "Responden bien: Retargeting_Veriff (Marketing, 9.6 M, 3.0 %), confirmación de pago KPay (9.1 M, 3.8 %), Precobranza KCash (Collections, 4.1 M, 4.3 %), Active Retargeting Installments (Product Growth, 3.3 M, 2.8 %). No: 89 correos de promociones de comercios KPay, ninguno llega a 1.5 %."),
       ("Impacto", "38 de 308 responden bien (1.5 % de clic o más). 155 pasan el piso de 0.3 %; los que no lo pasan son la mitad del volumen de estos correos y 8 % de sus clics."),
     ],
     h=[
       "Por tema: recordatorio de registro 10 de 10 responden bien; transaccional 11 de 20; cobranza 4 de 13; Tasa 0 2 de 32; referidos 0 de 31; promociones de comercios 0 de 89; ofertas para volver 0 de 26.",
       "Por tamaño: responden bien 9 % de los de 200 a 500 mil y 25 % de los de más de 3 M. Hay buenos y malos de todos los tamaños, así que achicar la audiencia no basta.",
       "En push: 26 de 314 responden bien (3 % de apertura o más); casi todos son cobranza, pagos recibidos e Installments a activos.",
     ],
     sw="Para que un correo responda no hay que hacerlo más chico: hay que mandarlo por una razón de la persona.",
     resp="Pieza es cada correo que salió: una versión de una campaña, con su propia fecha. 'Existen en todos los tamaños' quería decir que hay correos buenos con 200 mil destinatarios y con 9 M: el tamaño no explica la respuesta; el tema y el motivo del envío sí.",
     nota="Fuente: E1 agregado por versión (communication_id) con 200 mil o más entregados. Contradicción: la lámina anterior llamaba 'mínimo' a 1.5 % de clic y 3 % de apertura, no al piso de 0.3 % y 0.75 % que usa el resto del deck. Aquí se separan: piso (0.3 %) y responde bien (1.5 %).",
     estado="rehacer",
   ),

   dict(
     t="Los Canvas para recuperar clientes de KPay tienen hasta 120 mensajes distintos y su push casi nadie lo abre",
     tipo="Gráfica + lecturas",
     viz="Mapa de un Canvas largo: filas = semana 1 a 4, columnas = canal (push, in-app, email, WhatsApp), celda = cuántos mensajes distintos hay y su respuesta; al lado, barras de respuesta por canal del programa completo contra el piso.",
     ctx=[
       ("Qué se manda", "Promocional de recuperación de KPay: cuatro semanas de mensajes por cuatro canales, con hasta ocho ofertas (cupón, descuento en tasa, plazos con intereses, sin oferta, cada una también 'solo Amazon')."),
       ("Quién", "Product Growth: 44 de los 45 Canvas con más de 20 pasos; el otro es una copia de uno de ellos."),
       ("A quién", "Ex clientes KPay con 3, 6 y 12 meses sin compra. Pueden no tener la app, lo que explica parte del push sin aperturas."),
       ("Ejemplos", "Lending-KPay-20260310-B0332 HardInactive_6MesesInactividad-ConSinOferta: 120 pasos (40 push, 40 in-app, 30 email, 10 WhatsApp). B0333 Churn_12Meses de agosto: 104 pasos y 83 mil personas en el paso más grande."),
       ("Impacto", "Programa completo: 14.9 M mensajes y 3.6 M MXN. Push 0.97 % de apertura, email 0.16 % de clic, WhatsApp 54 % de lectura. Cada persona recibe entre 5 y 10 mensajes al mes."),
     ],
     h=[
       "'120 pasos' no son 120 mensajes a la misma persona: son 120 mensajes distintos (combinaciones de semana, canal y oferta). Cada persona recibe la rama de su oferta.",
       "28 de los 45 Canvas largos son este programa (27 más una copia); 8 son ofertas sin intereses a clientes activos de KPay (B0426); el resto son Installments a activos (que sí responde), Tasa 0, Lázaro, Cuesta de Enero y AnotayGana.",
       "En todos los Canvas, 278 pasos con más de 5 mil personas abren menos de 1 %; 275 son push, casi todos de Tasa 0 (Cuesta de Enero, registrados de KPay) y AnotayGana.",
     ],
     sw="Más ramas no recuperan más: el programa necesita menos ofertas, un canal que la persona sí use y un grupo de control.",
     resp="Son de Product Growth y casi todos son el programa de recuperación de KPay (inactivos de 3, 6 y 12 meses, con o sin oferta). '120 pasos' significa que el Canvas tiene 120 mensajes distintos: cuatro semanas por cuatro canales por varias ofertas.",
     nota="Fuente: E15 (embudo por paso). Conflicto conocido: 96 a 120 pasos en el playbook contra 72 a 200 en el análisis; en E15 el máximo es 120 y hay 45 Canvas con más de 20. La apertura por posición del paso no cae de forma clara (email 14 a 19 % en todas las posiciones), por eso se quitó 'los pasos tardíos siguen mandando'.",
     estado="rehacer",
   ),

   dict(
     t="En vez de medir una campaña, la copiamos cada mes: 74 campañas sacaron cinco o más versiones este año",
     tipo="Gráfica + lecturas",
     viz="Línea de tiempo por campaña (filas = las 10 con más versiones): un punto por versión nueva en su mes de salida, barra gris con los mensajes del mes, color = equipo; marcadas las versiones viejas que siguen enviando en septiembre.",
     ctx=[
       ("Qué se manda", "Tasa 0 (13 campañas, 148 versiones), ofertas para volver (9 y 101), promociones de comercios KPay (12 y 97), referidos (14 y 97). Promocional."),
       ("Quién", "Product Growth 31 campañas y 303 versiones; Marketing 35 y 283; Sales 6 y 56; Others 2 y 25."),
       ("A quién", "Registrados sin crédito, leads, ex clientes inactivos y recurrentes."),
       ("Ejemplos", "Lending-KCash-B0210 Nuevos_MPNeverCash-Tasa0: 22 versiones. B0337 CuestaEnero: 20. B0223 NeverActive: 19. Marketing-KCash-B0171 RescateTasa0 a rezagados: 18. B0333 Churn 12 meses KPay: 18. El Canvas B0211 Tasa 0 a registrados se recrea cada mes y la versión de enero siguió enviando hasta octubre."),
       ("Impacto", "667 versiones nuevas en 2026. Esas 74 campañas, con todas sus versiones, mandaron 266 M mensajes (40 % del año): 139 M por email, 86 M push, 34 M WhatsApp y 6 M in-app."),
     ],
     h=[
       "Una versión es una copia de la misma campaña con otra fecha en el nombre; casi todas son Canvas que mandan por varios canales.",
       "Las versiones viejas no se apagan: en septiembre 43 campañas tenían dos o más versiones enviando al mismo tiempo (114 versiones), lo que puede mandar dos veces a la misma persona.",
       "Cada copia reinicia la medición: nadie compara la versión nueva contra la anterior.",
     ],
     sw="Copiar es más fácil que medir, y por eso la campaña que no responde se repite doce veces.",
     resp="Versiones de la misma campaña: copias con fecha nueva, casi siempre un Canvas multicanal. Las campañas con más copias son de Tasa 0, ofertas para volver, referidos y comercios KPay, de Product Growth y Marketing. 'Piezas' eran esas versiones.",
     nota="Fuente: E2 (catálogo, fecha del primer envío en 2026) y E1 (mensajes). Campaña = nombre sin fecha (función _fam de deck_data). 184 campañas tienen cinco o más versiones contando años anteriores.",
     estado="rehacer",
   ),

   dict(
     t="Braze tiene 6,144 comunicaciones guardadas, pero en septiembre solo 341 mandaron algo",
     tipo="Cifra grande",
     viz="Flujo del catálogo: guardadas (6,144), con envío en 2026 (3,438), creadas en 2026 (2,120), activas en septiembre (341) y con nombre de prueba (636). Tabla al lado: activas en septiembre por canal y por equipo.",
     ctx=[
       ("Qué se manda", "Comunicación = cada campaña suelta o Canvas guardado en Braze (5,173 Canvas y 971 campañas). Un Canvas puede mandar por varios canales."),
       ("Quién", "Con envío en el año: Marketing 745, Product Growth 574, Sales 333, Others 328, Collections 23. En septiembre: Product Growth 101, Others 95, Marketing 88, Sales 35, Collections 22."),
       ("A quién", "No aplica: es el inventario."),
       ("Ejemplos", "De 3,439 comunicaciones que enviaron en el año salen 1,071 campañas (sin fecha en el nombre). En septiembre, 341 comunicaciones de 270 campañas."),
       ("Impacto", "Por canal, en el año: push 1,124 comunicaciones, email 999, in-app 727, WhatsApp 601. En septiembre: email 214, push 179, in-app 123, WhatsApp 68."),
     ],
     h=[
       "2,120 comunicaciones se crearon en 2026, unas 235 al mes.",
       "No hay comunicaciones sin archivar y sin envío en 90 días: las 186 sin archivar mandaron algo en el último trimestre.",
       "El estado 'archivada' no es confiable: 229 comunicaciones marcadas como archivadas enviaron en septiembre.",
       "636 tienen nombre de prueba o copia; 193 mandaron algo en el año (lámina 77).",
     ],
     sw="El catálogo está lleno de copias viejas: limpiar y nombrar bien es un trabajo de una vez.",
     resp="Comunicación es cada campaña o Canvas guardado en Braze. Hay 6,144; 3,438 mandaron algo en 2026 y 341 en septiembre (email 214, push 179, in-app 123, WhatsApp 68). Ninguna sin archivar lleva 90 días sin enviar.",
     nota="Fuente: E2 (catálogo con estado, primer y último envío al 7 de octubre) y E1 (envíos por mes). El cruce por canal usa las banderas de canal de E2 y la columna canal de E1.",
     estado="rehacer",
   ),

   dict(
     t="Por qué pasa: nadie compara volumen contra respuesta, y copiar una campaña es más fácil que medirla",
     tipo="Cierre de sección",
     viz="Cierre: cadena de causas (5 porqués), hipótesis analítica, operativa y de gobierno, cómo (semana, dónde en Braze, equipo, métrica) y qué ganamos.",
     ctx=[
       ("Qué se manda", "Tasa 0, comercios KPay, referidos, BillPay y ofertas para volver por email y WhatsApp masivo."),
       ("Quién", "Product Growth y Marketing concentran tres cuartas partes del volumen que no responde."),
       ("A quién", "Leads, registrados sin crédito y ex clientes inactivos."),
       ("Ejemplos", "B0211 Tasa 0 a registrados de KPay, B0171 RescateTasa0 por WhatsApp, B0333 Churn 12 meses."),
       ("Impacto", "293 M mensajes y 23 M MXN en campañas que no responden; 89 siguen activas."),
     ],
     h=[
       "Cómo: revisión mensual de las 20 campañas más grandes contra el piso; si en dos meses no lo pasa, se rehace o se apaga.",
       "Programas de recuperación con tope de gasto, canal barato y 10 % de control.",
       "Una sola versión viva por campaña: al lanzar la nueva se archiva la anterior.",
     ],
     resp="Pendiente de revisar al final, como pediste.",
     estado=None, cierre=True,
   ),
 ])]),

 dict(n="IX", nombre="Lo que hay que dejar de hacer: ocho hábitos que cuestan dinero y clientes",
      arg="Ocho prácticas explican la mayor parte del desperdicio. Cada una tiene un equipo donde más pesa y una campaña que la ejemplifica.",
      subs=[dict(nombre=None, sl=[

   dict(
     t="Ocho hábitos explican la mayor parte del desperdicio, y en cinco de ellos el primer lugar es de Product Growth o Marketing",
     tipo="Mapa de calor",
     viz="Matriz práctica por equipo: celda = millones de mensajes, color = MXN; última columna = la campaña que más pesa en cada práctica.",
     ctx=[
       ("Qué se manda", "Promocional en todas las prácticas; cobranza y transaccionales se excluyen."),
       ("Quién", "Product Growth y Marketing en cinco prácticas; Others en masivos, pruebas y sin ticket; Sales en promociones a bloqueados."),
       ("A quién", "Leads, registrados sin crédito, ex clientes inactivos, 'Todos' y bloqueados."),
       ("Ejemplos", "Ver columna de la campaña que más pesa en cada práctica."),
       ("Impacto", "Seguir mandando lo que ya no responde: 138 M mensajes y 9.4 M MXN. WhatsApp que se lee menos de 60 %: 10.3 M y 7.3 M MXN."),
     ],
     h=[
       "1. Masivo a más de un millón sin segmento: 70 M mensajes, 2.0 M MXN. Others 27 M, Product Growth 26 M, Marketing 17 M. Peor caso: BillPay Intro (Others).",
       "2. Seguir mandando lo que ya no responde: 138 M, 9.4 M MXN. Product Growth 69 M y 6.0 M MXN, Marketing 57 M. Peor caso: B0211 Tasa 0 a registrados (Product Growth).",
       "3. WhatsApp que se lee menos de 60 %: 10.3 M, 7.3 M MXN. Product Growth 8.6 M y 6.1 M MXN. Peor caso: B0333 Churn 12 meses KPay.",
       "4. Copiar en vez de medir: 266 M en campañas con 5+ versiones. Marketing 135 M, Product Growth 113 M. Peor caso: B0210 MPNeverCash Tasa 0, 22 versiones.",
       "5. Pruebas y copias con envío real: 6.7 M. Others 5.8 M. Peor caso: QA-KPay-B001 ReminderRegistroTelefono.",
       "6. Promocional a bloqueados (tarjeta KPay congelada, REUS o ARCO, lista negra): 44.7 M, 3.8 M MXN. Marketing 16.6 M, Sales 13.2 M, Product Growth 11.4 M. Peor caso: B0326 Referidos a dormants KPay. Más 111 mil correos promocionales a dados de baja (Marketing 59 mil).",
       "7. Canvas de más de 20 pasos: 40.8 M, 4.8 M MXN, casi todo Product Growth. Peor caso: programa de recuperación de KPay (B0331, B0332, B0333) y Cuesta de Enero.",
       "8. Sin ticket (sin dueño rastreable): 43.3 M, todo Others. Peor caso: BillPay Intro y WeeklyRecommendations.",
     ],
     sw="No es una campaña mala: son hábitos repetidos por los mismos dos equipos.",
     resp="Primeros lugares por práctica: Others (BillPay Intro) en masivos y sin ticket; Product Growth (B0211 Tasa 0, B0333 Churn KPay, recuperación KPay) en insistir, WhatsApp que no se lee y Canvas largos; Marketing (B0326 Referidos) en copiar y en promociones a bloqueados; Others (QA-KPay) en pruebas. Pendiente de revisar al final.",
     nota="Las prácticas se traslapan (una campaña puede estar en varias), no se suman. 'Masivo' = versión con un millón o más de personas en un mes. 'Ya no responde' = mensajes después del primer mes con 50 mil+ personas debajo del piso. Bloqueados de E7a (etapa del golden dataset, cubre 37 % de los envíos). Costo con WhatsApp por entregado.",
     estado="rehacer",
   ),

   dict(
     t="Uno de cada cinco mensajes salió de campañas que ya habían respondido menos que el piso un mes antes",
     tipo="Gráfica + lecturas",
     viz="Tiras mensuales por campaña (las ocho con más mensajes después de caer debajo del piso): respuesta de cada mes contra la línea del piso, sombreado el volumen enviado después del primer mes debajo; color = equipo.",
     ctx=[
       ("Qué se manda", "Tasa 0 (52 M), referidos (29 M), ofertas para volver (16 M, 2.5 M MXN por WhatsApp), crédito en plazos (14 M)."),
       ("Quién", "Product Growth 69 M (39 % de su volumen), Marketing 57 M (22 %), Others 7 M (8 %), Sales 5 M (6 %). Collections 11 M (24 %), pero cobranza se juzga por el pago."),
       ("A quién", "Registrados sin crédito (51 M), leads (41 M), ex clientes inactivos (29 M y 3.4 M MXN)."),
       ("Ejemplos", "Lending-KCash-B0211 Tasa 0 a registrados de KPay: en febrero tuvo 0.29 % de clic y siguió siete meses más, 29 M correos. B0223 NeverActive: 0.12 % en febrero, 12.6 M más. Marketing-KCash-B0326 Referidos a dormants: 0.13 % en febrero, 6.6 M más. Shopping S0004 WeeklyRecommendations: 0.17 % en enero, 6.2 M más."),
       ("Impacto", "149 M mensajes (22 % del año) y 10.0 M MXN; sin cobranza, 138 M y 9.4 M MXN. 47 de esas campañas seguían enviando en septiembre."),
     ],
     h=[
       "Email 99 M, push 40 M, WhatsApp 7.1 M (5.0 M MXN).",
       "Ninguna regla obliga a revisar una campaña cuando cae debajo del piso; se apagan cuando termina la promoción, no cuando dejan de responder.",
       "Si cada campaña se hubiera detenido dos meses después de caer debajo del piso, se habrían evitado 93 M de estos mensajes y 6.2 M MXN.",
     ],
     sw="La campaña que no responde no se detiene sola: hay que ponerle una regla de salida.",
     resp="'Fallado' quería decir esto: un mes en que la campaña llegó a 50 mil personas o más y respondió menos que el piso (" + PISO + "). Contamos todo lo que mandó en los meses siguientes.",
     nota="Recalculado de E1 con la regla de deck_data.insisten (familia por canal y mes). El deck decía 12 M MXN porque cobraba WhatsApp por enviado. Los 93 M y 6.2 M MXN evitables suman lo enviado desde el segundo mes después del primer mes debajo del piso, sin cobranza ni transaccionales. El deck decía '85 campañas debajo del mínimo siguen activas' con otra definición; aquí 47 siguen enviando en septiembre.",
     estado="rehacer",
   ),

   dict(
     t="El recordatorio de registro sí funciona, pero manda hasta dos correos al día y es la campaña recurrente que más bajas causa entre los nuevos",
     tipo="Gráfica + lecturas",
     viz="Línea de días desde que la persona se quedó en un paso (5 minutos, día 1, 3, 7, 10, 15 y 30) contra la apertura de cada correo, para el recordatorio de KPay; barras de bajas de nuevos por campaña de recordatorio (Veriff, datos personales, NIP, dirección).",
     ctx=[
       ("Qué se manda", "Correos, push e in-app que recuerdan terminar un paso del registro: verificar identidad (Veriff), datos personales, NIP, dirección, crear cuenta. Es de activación, no una oferta nueva."),
       ("Quién", "Marketing en KCash (Leads_LeftFunnel, 17 M mensajes) y Acquisition en KPay (T2706, T2713, T2727, T2728; cae en Others, 3 M)."),
       ("A quién", "Personas que empezaron a pedir su crédito o su cuenta y se quedaron en un paso."),
       ("Ejemplos", "Marketing-KCash-B0000 Leads_LeftFunnel-Retargeting_Veriff: 9.7 M correos y 2.9 M push. Retargeting_PersonalInfo: 2.7 M. Acquisition-KPay-T2727 RetargetingVeriff: un correo a los 5 minutos y otros en los días 1, 3, 7, 10, 15 y 30."),
       ("Impacto", "Email 16.4 M; clic 3.0 % en Veriff y PersonalInfo y 4.2 % en NIP, seis a ocho veces la campaña típica. 65 mil bajas de email; entre los nuevos, Veriff, PersonalInfo y NIP explican 22 % de las bajas (34 mil personas)."),
     ],
     h=[
       "En KPay la apertura cae de 30 % en el correo de los 5 minutos a 5 a 7 % desde el día 3: los primeros dos correos hacen casi todo el trabajo.",
       "En KCash cada persona recibe unos cinco correos al mes; quien se da de baja lo hace a los 3 o 4 días, después de 5 a 8 correos: uno o dos al día.",
       "Quien abre el de Veriff convierte 4.5 % contra 2.6 % de quien no abre: el mensaje sirve.",
     ],
     sw="No hay que quitar el recordatorio: hay que dejar los dos primeros correos y pasar el resto a push o in-app, con tope de tres en la primera semana.",
     resp="Retargeting de registro es el recordatorio para terminar el registro: le llega a quien empezó a pedir su crédito KCash o su cuenta KPay y se quedó en un paso (verificar identidad, datos, NIP, dirección). Llega a los 5 minutos y luego en los días 1, 3, 7, 10, 15 y 30; en KCash, unos cinco correos al mes. Lo mandan Marketing (KCash) y Acquisition (KPay).",
     nota="Fuentes: E15 (pasos del Canvas Acquisition-KPay T2727 y T2728; el Canvas de Marketing B0000 no trae pasos en E15), E1 (volumen, clic y bajas), E8 y MUESTRA_L (bajas de nuevos por campaña del día). 'Uno o dos al día' sale de la mediana de 3 a 4 días con 5 a 8 correos; no hay dato diario por persona.",
     estado="rehacer",
   ),

   dict(
     t="Lo que parecían pruebas a clientes son, sobre todo, push sin aperturas y campañas reales con nombre de prueba",
     tipo="Gráfica + lecturas",
     viz="Tres columnas (push sin aperturas, envío real con nombre de prueba o copia, prueba chica de menos de mil personas): mensajes, personas y respuesta; debajo, lista de los casos más grandes con su equipo.",
     ctx=[
       ("Qué se manda", "Comunicaciones con QA, Test, Prueba o 'Copy of' en el nombre. Hay de todo: push técnicos, recordatorios, cobranza y promociones reales."),
       ("Quién", "Others (QA, Acquisition, Compliance) 5.8 M mensajes; Sales 0.4 M (copias de Lanzamiento Iberia y 4QSI); Collections 0.4 M (PRUEBA_ de cobranza). La copia del programa HardInactive de Product Growth y las de AmazonPreHotSale de Sales quedaron registradas sin equipo y caen en Others."),
       ("A quién", "Clientes reales: hasta 1.8 M personas en un solo envío."),
       ("Ejemplos", "Push sin aperturas: QA-KPay-B001 ReminderRegistroTelefono (1.9 M push a 1.8 M personas, 0.01 %), QA_CC y QA_CC-More3k (1.6 M), AmazonPreHotSale QA y su copia (0.65 M). Envío real con nombre de copia: Copy of Lending-KPay-B0332 HardInactive (724 mil mensajes, WhatsApp 52 % de lectura, 170 mil MXN), Copy of Acquisition T2727 RetargetingVeriff-Test (331 mil correos, 2.9 % de clic), PRUEBA_Collections BKT1 y Precobranza (415 mil en septiembre)."),
       ("Impacto", "163 comunicaciones, 6.7 M mensajes y 0.2 M MXN. Push sin aperturas 4.7 M; envíos reales con nombre de prueba 2.0 M y 20 mil conversiones de referencia; pruebas chicas 14 mil mensajes."),
     ],
     h=[
       "Push sin aperturas (20 envíos, 4.7 M): abrieron 0.00 a 0.05 %. Probablemente son técnicos o silenciosos (algunos lo dicen en el nombre: Silent_Push); no sabemos si la persona los vio.",
       "Envío real con nombre de prueba (14, 2.0 M): responden como cualquier campaña. Es la operación normal con el nombre equivocado, como sospechabas.",
       "Pruebas de verdad (129, menos de mil personas cada una): 14 mil mensajes, sin problema.",
       "Lo que sí es riesgo: PRUEBA_ de cobranza llegó a 5 mil personas ya dadas de baja y QA-KPay-B001 a 5 mil en REUS o ARCO y 8.6 mil en lista negra.",
     ],
     sw="El problema no es probar con clientes: es que el nombre no dice qué es, y así nadie puede auditar ni medir.",
     resp="Sí: la mayoría no son pruebas. 2.0 M mensajes son campañas reales que se copiaron y no se renombraron (programa HardInactive KPay, recordatorio Veriff de KPay, cobranza PRUEBA_). 4.7 M son push que casi nadie abrió, probablemente técnicos. Solo 14 mil mensajes son pruebas chicas de verdad.",
     nota="Fuente: E1, nombre con QA, Test, Prueba, Copy of, copia, dummy o demo (163 comunicaciones con envío; antes se reportaban 171 y 7.26 M con otra regla). Para confirmar si un push era silencioso hace falta el tipo de push del Canvas (extracción del paso con su bandera de contenido).",
     estado="rehacer",
   ),
 ])]),

 dict(n="X", nombre="Lo que ya funciona: escribirle a quien acaba de hacer algo",
      arg="Ya tenemos campañas que responden cinco a ocho veces más que el promedio. Tienen en común que salen porque la persona hizo algo, no porque está en una lista.",
      subs=[dict(nombre=None, sl=[

   dict(
     t="Los mensajes que salen porque la persona hizo algo son 12 % del volumen y responden siete veces más en email",
     tipo="Tabla",
     viz="Tabla de disparadores: qué hizo la persona, campañas, equipo, mensajes y respuesta por canal, contra la fila 'sin disparador (lista o base)'. Barra de color en la celda = veces la respuesta sin disparador.",
     ctx=[
       ("Qué se manda", "Recordatorios de algo empezado, aviso de pago por vencer, sugerencias después de una compra, bienvenida, aniversario y regreso a los 45 días."),
       ("Quién", "Marketing (recordatorio de registro, referidos después de comprar, Canceló), Product Growth (Installments a activos, Tardan 45 días, Temu, aniversario, onboarding KPay), Collections (precobranza)."),
       ("A quién", "Personas en un momento concreto: se registró, compró, tiene un pago, canceló."),
       ("Ejemplos", "Empezó su registro y se quedó a medias: Retargeting_Veriff, email 3.1 %, push 5.7 %. Tiene un pago por vencer: Precobranza, email 3.6 %, push 4.5 %. Acaba de comprar: Lending-KCash-B0301 Active-Retargeting_Installments_SP, email 2.8 %, push 11 %. Canceló una oferta: Marketing-KPay-B0001 RetargetingOffering-Canceló, push 9.5 %. Lleva 45 días sin volver a pedir: B0220 Tardan45días, email 1.5 %, push 3.6 %. Se registró hace poco: onboarding, push 10 %."),
       ("Impacto", "71 M mensajes (12 % de lo promocional y precobranza). Email 2.6 % de clic contra 0.35 % sin disparador; push 4.9 % contra 1.0 %; in-app 65 % contra 30 %. WhatsApp no cambia (67 % contra 69 %)."),
     ],
     h=[
       "Con 12 % del volumen se llevan 57 % de los clics de email.",
       "Fuera de los transaccionales, Precobranza e Installments a activos son las campañas grandes que mejor responden en Braze.",
       "La regla que se puede copiar: cada campaña promocional nace de un evento de la persona (registro, compra, pago, cancelación, días sin volver), no de una lista.",
     ],
     sw="Escribir a quien acaba de hacer algo funciona; escribirle a una lista, casi no.",
     resp="Sí, son eventos. Los disparadores: empezó su registro y se quedó a medias, tiene un pago por vencer, acaba de comprar o usar su crédito, canceló una oferta, lleva 45 días sin volver a pedir, compró en un comercio con KPay, aniversario de cuenta y bienvenida. Las campañas de cada uno están en la tabla.",
     nota="Disparador inferido por el nombre de la campaña (regla en p5/s78.py); no tenemos el evento de entrada del Canvas. Se excluyen transaccionales, BillPay y cobranza salvo precobranza. Quien recibe por un evento ya es más activo: la diferencia no prueba cuánto vende el mensaje sin grupo de control.",
     estado="rehacer",
   ),

   dict(
     t="Hay 150 campañas chicas que responden el doble de lo normal y valdría la pena ampliar con el mismo disparador",
     tipo="Gráfica + lecturas",
     viz="Dispersión de campañas promocionales: tamaño (x, escala logarítmica) contra respuesta en veces la típica de su canal (y), color = equipo; resaltadas las activas en septiembre con más de 30 mil mensajes.",
     ctx=[
       ("Qué se manda", "Recordatorios, ofertas después de cancelar, crédito a quien compró en un comercio, bienvenida y aniversario. Promocional y de activación."),
       ("Quién", "Product Growth 68 campañas, Marketing 62, Others 17 (Acquisition KPay, NewProducts), Sales 3."),
       ("A quién", "Clientes activos (56 campañas) y leads con una acción reciente (52)."),
       ("Ejemplos", "Marketing-KPay-B0001 RetargetingOffering-Canceló, push a quien canceló una compra: 9.5 % de apertura, 9 veces la típica, 71 mil mensajes. Lending-KCash-B0154 Tardan45díasrecurrir-Ganadores, email a quien lleva 45 días sin volver a pedir: 3.9 %, 8 veces. Lending-KPay-T2853 Nuevos-Onboarding, email: 3.6 %, 7 veces. Lending-KPay-B0186 Onboarding_SiCompletoCompra, push: 6.8 %. Lending-KPay-B0184 CompraEnTemu-XSellaKCash, push a quien compró en Temu: 3.3 %. Lending-KCash-B0229 AniversarioNones: email 2.0 %, push 4.1 %."),
       ("Impacto", "150 campañas con 3.2 M mensajes, 0.5 % del año; 46 siguen activas."),
     ],
     h=[
       "Casi todas comparten la regla de la lámina anterior: salen por algo que hizo la persona.",
       "Ampliar no es mandarlas a toda la base: es aplicar el mismo disparador a más productos o etapas (por ejemplo, 'Canceló' también en KCash; 'compró en un comercio' en más comercios).",
       "Cada ampliación con 10 % de control y revisión a dos meses.",
     ],
     sw="Lo que funciona ya existe; está chico porque nadie lo ha escalado.",
     resp="Las mandan sobre todo Product Growth y Marketing. Temas: oferta a quien canceló, regreso a los 45 días, bienvenida de KPay, crédito a quien compró en Temu, aniversario y recordatorio de dirección o datos.",
     nota="Fuente: muestra_c_familias.csv, señal 'escalar' (envíos debajo de la mediana de su canal, al menos mil, respuesta al doble de la mediana o más). Mediana de email 0.50 % de clic, push 1.07 %.",
     estado="rehacer",
   ),

   dict(
     t="Las promociones de comercios a clientes de KPay sí mueven a quien las abre, aunque a 90 días la ventaja se achica",
     tipo="Gráfica + lecturas",
     viz="Puntos por campaña de Sales: veces que convierte quien abre contra quien no abre a 7 días (x) y a 90 días (y), tamaño = mensajes, color = canal; diagonal de referencia y línea de 2 veces.",
     ctx=[
       ("Qué se manda", "Promocional: Comercio del día, Hot Sale, Amazon, Cuponera, Privalia, Venta Azul Aeroméxico, Kueski Promotor en tienda."),
       ("Quién", "Sales (KPay): 85 M mensajes en el año, 60 % por push."),
       ("A quién", "Clientes recurrentes de KPay (64 M mensajes, 75 %), leads (14 M) y la base activa e inactiva (6 M)."),
       ("Ejemplos", "Sales-KPay-B0615 ComerciodeldiaSeptiembre, push: 3.5 veces a 7 días y 2.5 a 90. B0598 y B0623 PrivaliaAniversario: 3.1 y 3.7 veces a 7 días, 2.2 y 2.8 a 90. B0599 VentaAzulAeromexico: 2.5 y 2.0. B0335 PromocionesMerchants por email: 2.2 y 1.5."),
       ("Impacto", "En 177 campañas de Sales, quien abre convierte 2.4 veces más a 7 días y 1.5 veces a 90 (mediana). 26 campañas mantienen 2 veces o más a 90 días."),
     ],
     h=[
       "'Mover' quiere decir que quien abre convierte más que quien recibió el mismo mensaje y no lo abrió.",
       "A 90 días la ventaja baja en todos los equipos (Marketing 2.6 a 1.7, Product Growth 2.5 a 1.7, Collections 3.3 a 2.3): parte de esas compras iban a pasar igual.",
       "Las que mantienen 2 veces a 90 días son sobre todo de agosto y septiembre, cuya ventana de 90 días todavía no se completa.",
     ],
     sw="La promoción a quien ya compra con KPay parece funcionar, pero solo un grupo de control dirá cuánto vende de verdad.",
     resp="Las manda Sales, a clientes recurrentes de KPay. 'Si mueven' significa que quien abre convierte más que quien no abre: 2.4 veces a 7 días y 1.5 a 90. No prueba que el mensaje cause la venta, porque quien abre ya era más activo.",
     nota="Fuente: E9a (conversión de quienes abren y no abren a 7, 30, 90 días), campañas con mil o más de cada lado y 100 conversiones. La conversión es la de Databricks (solicitud o préstamo, sobre todo Cash): no confirma la compra en el comercio. Cambia el mensaje de la lámina anterior ('2 a 2.5 veces a 90 días'): eso solo vale para 26 de 177 campañas.",
     estado="rehacer",
   ),

   dict(
     t="Cuando terminaron los masivos de junio, mandamos la mitad de push y lo abrió el mismo número de personas",
     tipo="Gráfica + lecturas",
     viz="Barras apiladas mensuales de push enviados por equipo, con línea de aperturas totales y línea de tasa de apertura; junio resaltado. Panel chico: apertura de las mismas campañas que siguieron de junio a septiembre.",
     ctx=[
       ("Qué se manda", "Lo que se dejó de mandar: lanzamiento y recordatorios de BillPay y recargas, felicitación del Día del Padre, Mundial, sorteo AnotayGana, Comercio del día de Marketing y referidos."),
       ("Quién", "Marketing pasó de 26.0 M push en junio a 9.4 M en septiembre; Others (NewProducts) de 9.8 M a 1.5 M; Product Growth de 5.8 M a 3.1 M. Sales subió de 3.4 M a 7.8 M."),
       ("A quién", "Toda la base y leads (los masivos de junio)."),
       ("Ejemplos", "NewProducts BillPay_Reminder (4.8 M push en junio), Marketing-KPay-B00527 LanzamientoBillpayments_Onboarding (3.2 M), Lending-Ecosistema-B0440 AnotayGana (3.1 M), Marketing-KPay-B0444 BAUMundial (2.2 M), PushFelicitacionDiaPadres (1.6 M)."),
       ("Impacto", "Junio 46.8 M push con 1.05 % de apertura; septiembre 24.4 M con 2.11 %, el mejor del año. Aperturas: 493 mil en junio y 516 mil en septiembre."),
     ],
     h=[
       "Por tema, la caída fue BillPay y recargas (12 M menos al mes), fechas especiales (6 M), AnotayGana (3 M) y referidos (2 M).",
       "Las 16 campañas que siguieron de junio a septiembre con más de 100 mil push subieron de 1.65 % a 1.95 % de apertura: con menos presión, el mismo mensaje se abre más.",
       "No fue una decisión: se acabaron los lanzamientos. Es la prueba natural de que el tope de volumen funciona.",
     ],
     sw="Mandar menos no costó aperturas: las mismas personas siguieron abriendo.",
     resp="Bajó el push promocional masivo de junio: Marketing (Comercio del día, Mundial, Día del Padre, referidos, lanzamiento de BillPay) y Others (BillPay y recargas de NewProducts), y Product Growth (AnotayGana). No se bajó por decisión; terminaron esos lanzamientos.",
     nota="Fuente: E1, push por mes, equipo y tema. No es un experimento: también cambió la mezcla (más transaccional de Others y Sales a recurrentes). Usar como evidencia de dirección, no de magnitud.",
     estado="rehacer",
   ),

   dict(
     t="Antes de lanzar una campaña: seis preguntas y una regla para apagarla",
     tipo="Checklist",
     viz="Lista de verificación de una página: pregunta, qué significa en Braze, el dato de Kueski que la respalda y quién la responde. Abajo, la regla de apagado en una línea por canal.",
     ctx=[
       ("Qué se manda", "Toda campaña promocional nueva o relanzada (no cobranza ni transaccional)."),
       ("Quién", "El equipo dueño la llena; CRM la revisa antes de activar."),
       ("A quién", "Aplica a todos los segmentos; para inactivos y churn, con tope de gasto y control."),
       ("Ejemplos", "B0211 Tasa 0 a registrados no habría pasado la pregunta 1; RescateTasa0 por WhatsApp no habría pasado la 2."),
       ("Impacto", "Con la regla de apagado se habrían evitado buena parte de los 149 M mensajes enviados después de caer debajo del piso."),
     ],
     h=[
       "1. ¿Qué hizo la persona para recibirla? (registro, compra, pago, cancelación, días sin volver). Con evento, el email responde 2.6 %; sin evento, 0.35 %.",
       "2. ¿Va por el canal que esa persona usa y que cuesta menos? WhatsApp solo a quien leyó uno en 90 días. Por WhatsApp, una conversión cuesta 17 MXN en activos y 191 en ex clientes inactivos.",
       "3. ¿Cuántos mensajes le llegan? Máximo dos al mes por campaña, el segundo solo a quien no abrió. Con dos el clic sube a 1.76 %; con tres o cuatro cae a 0.48 %.",
       "4. ¿Le llega otra campaña el mismo día? Revisar el calendario común antes de activar.",
       "5. ¿Tiene grupo de control? 10 % que no la recibe. Si va a más de un millón de personas, primero una prueba al 10 %.",
       "6. ¿Tiene dueño y ticket, y una sola versión viva? Al lanzar la nueva se archiva la anterior.",
       "Regla de apagado: si en dos meses responde menos que el piso (" + PISO + ") o tiene más de 2.5 bajas por mil correos, se rehace o se apaga.",
     ],
     sw="Seis preguntas antes de activar y una regla para apagar evitan casi todo lo que vimos en esta sección.",
     resp="Lo reescribí en lenguaje llano: cada pregunta dice qué se revisa, con qué dato de Kueski y quién la responde. 'Límite de salida' ahora es 'regla para apagarla': si en dos meses no pasa el piso, se rehace o se apaga.",
     nota="Datos: disparadores (lámina 78), costo por conversión de WhatsApp por etapa (66b), toques de G_Practicas G4 (MUESTRA_G), envíos después de caer debajo del piso (75).",
     estado="rehacer",
   ),
 ])]),
]


if __name__ == "__main__":
    n = 63
    for sec in SECS:
        print("==", sec["n"], sec["nombre"])
        for sub in sec["subs"]:
            for s in sub["sl"]:
                n += 1
                print(n, s["t"])
