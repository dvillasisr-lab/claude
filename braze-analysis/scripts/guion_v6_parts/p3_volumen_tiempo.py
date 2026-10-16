"""Guion v6, parte 3: secciones IV (presión sobre la persona) y V (cuándo mandamos). Láminas 31 a 44.

Cifras nuevas y método en p3_volumen_tiempo_notas.md. Scripts de cálculo en v6parts/p3work/.
"""

SECS = [
 dict(n="IV", nombre="La misma persona, demasiadas veces",
      arg="Una cuarta parte de la base recibe casi todo lo que mandamos, varias campañas le llegan el mismo día y nadie ve el total que recibe una persona. Las bajas no vienen del total acumulado: vienen del primer correo a quien no nos conoce y de los días saturados.",
      subs=[dict(nombre=None, sl=[

   dict(
     t="Una cuarta parte de la base recibe 86 % de los mensajes, y es la que más compra: el recorte va en lo que ignora, no en la persona",
     tipo="Gráfica + lecturas",
     viz="Curva de concentración con cuatro líneas: % acumulado de personas (de quien más recibe a quien menos) contra % acumulado de mensajes, de push, de costo variable y de conversiones; punto marcado en 23 % de personas. Panel chico: por banda de mensajes en 9 meses, mensajes por persona contra bajas por mil correos.",
     ctx=[
       ("Qué se manda", "Mezcla de promocional y operativo. En este grupo: 46 % email, 42 % push, 8 % WhatsApp y 4 % in-app. Lo que más se repite por persona: cobranza diaria, Comercio del día, recordatorio de registro, rescates por push y Tasa 0."),
       ("Quién", "Marketing (Comercio del día, Rescate fines de semana, Rescate Tasa 0, recordatorio de registro), Product Growth (Tasa 0 a registrados, nunca activos, inactivos), Collections (cobranza, se justifica) y Others (Shopping, recomendaciones semanales)."),
       ("A quién", "4.5 M personas que recibieron 41 o más mensajes en 9 meses: 129 cada una, unos 14 al mes. Incluye 631 mil prospectos (según la tabla de filtros de cliente) con 303 mensajes cada uno y 272 mil con tarjeta KPay congelada."),
       ("Ejemplos", "Marketing B0561 Comercio del día por push a leads: 7.7 push al mes por persona, abre 0.88 %. Marketing B0391 Rescate fines de semana: 13.4 M push, 5 al mes por persona, abre 0.76 %. Product Growth B0211 Tasa 0 a registrados sin crédito: 34.9 M correos, 4.8 al mes por persona, clic 0.28 %. Collections BKT1 (cobranza, operativo): 6 correos al mes por persona."),
       ("Impacto", "86 % de los mensajes, 96 % del push, 86 % del WhatsApp entregado y 84 % del costo variable (48.7 de 58.3 M MXN, WhatsApp por entregado). También 90 % de las personas que convirtieron."),
     ],
     h=[
       "En 9 meses, 23 % de las personas recibe 86 % de los mensajes. Medido por mes, 5 % recibe 41 o más y se lleva 31 % del volumen; en enero era 20 % y desde mayo está entre 30 y 37 %.",
       "Quien recibe 321 o más en 9 meses (339 mil personas, 482 mensajes cada una) cuesta 31 MXN por persona; quien recibe 1 a 5 cuesta 0.08 MXN.",
       "Este grupo no se da de baja más por correo recibido: 1.2 a 2.4 bajas por mil correos, contra 10.9 en quien recibe 1 a 5. Es la base activa.",
       "Lo que sobra adentro: push que casi nadie abre (Rescate fines de semana 0.76 %, Rescate Tasa 0 a anónimos 0.56 %) y WhatsApp a bases frías.",
     ],
     sw="Cortar parejo a quien recibe mucho le pega a quien compra; hay que quitar lo que esa persona ya no abre.",
     resp="Periodo: enero a septiembre 2026; por mes la foto es 5 % que recibe 41 o más y se lleva 31 %. Canal: sobre todo push (96 % del push va a este grupo) y WhatsApp (86 %). Temas: cobranza diaria, Comercio del día, recordatorio de registro, rescates por push y Tasa 0. ¿Provoca bajas? No por sí solo: por correo se dan de baja menos que quien recibe poco; el daño es push que no abren y WhatsApp caro.",
     nota="E3 (9 meses) y E4b (por mes). Bajas de E3 son eventos. Temas por persona salen de E1 (mensajes por persona al mes de cada campaña), no de un cruce persona por campaña; para confirmarlo: E3 con campaña y equipo.",
     estado="rehacer", cierre=False),

   dict(
     t="Las bajas vienen del primer correo a quien no nos conoce y del día saturado, no del total de mensajes",
     tipo="Pequeños múltiplos",
     viz="Tres paneles con la misma escala, uno por periodo de medición. Nueve meses: banda de mensajes contra bajas por 100 personas y por mil correos. Un mes: la misma lectura con E4b. Un día: campañas distintas el mismo día contra bajas por mil personas-día, enero a mayo contra julio a septiembre. Muestra por qué 'a más mensajes, más bajas' cambia según el periodo.",
     ctx=[
       ("Qué se manda", "Email promocional: lanzamiento de BillPay, recordatorio de registro, Tasa 0 y referidos. Solo el email registra bajas."),
       ("Quién", "Base antigua: Marketing 39 % y Product Growth 36 % de las bajas. Nuevos: NewProducts con BillPay Intro y Marketing con el recordatorio de registro."),
       ("A quién", "Nuevos (primer correo dentro del periodo) y base antigua (ya recibían antes de enero)."),
       ("Ejemplos", "NewProducts BillPay Intro (lanzamiento de BillPay a toda la base): 31 % de las bajas de nuevos, casi todas con su primer o segundo correo. Marketing B0000 Leads_LeftFunnel Retargeting Veriff, PersonalInfo y NIP (recordatorio de registro): 22 % de las bajas de nuevos, a los 3 o 4 días y con 5 a 8 correos. Product Growth B0211 Tasa 0 a registrados: 13 % de las bajas de la base antigua, después de 128 días y 29 correos."),
       ("Impacto", "439 mil personas se dieron de baja del email en 9 meses (2.2 % de quienes recibieron email). Uno de cada tres nuevos que se va lo hace con el primer correo."),
     ],
     h=[
       "Nueve meses: quien recibe 321 o más se da de baja 13 veces más por persona (16.5 contra 1.3 por 100), pero recibió cien veces más correos. Por correo es al revés: 10.9 bajas por mil correos en quien recibe 1 a 5 contra 1.2 en quien recibe 321 o más.",
       "Un mes: quien recibe 1 a 5 mensajes en el mes se da de baja más que quien recibe 41 o más (0.59 contra 0.44 por 100 personas; 3.0 contra 0.3 por mil correos). Pasa en los nueve meses.",
       "Un día: aquí sí hay saturación, y solo desde junio. De julio a septiembre, el día con 3 o 4 campañas tiene 47 % más bajas que el día con una (0.47 contra 0.32 por mil) y con 8 o más, tres veces más (1.10).",
       "El salto 'de cinco a seis mensajes' es de nueve meses, no de una semana: compara a quien recibió un solo masivo con quien recibe algo cada mes. No sostiene un tope semanal.",
     ],
     sw="El tope que sí tiene datos es por día y para el nuevo: máximo dos promocionales al día y una sola secuencia de bienvenida.",
     resp="El dato original era de 9 meses (E3), no por día ni por semana. Con el mismo dato por mes (E4b) y por día (E6a) la conclusión cambia: el total acumulado no explica las bajas; las explican el primer correo a quien no nos conoce (BillPay Intro de NewProducts y recordatorio de registro de Marketing) y los días con muchas campañas desde junio. Afirmamos eso y quitamos 'el salto de cinco a seis'.",
     nota="Resuelve el conflicto 'Más mensajes, más bajas' de META. Bajas de E3 son eventos; E4b, E4a y E8 son personas. En E6a la relación día saturado y baja no aparece de enero a mayo y sí de junio a septiembre. Equipos y campañas de las bajas: E8 (campaña del día de la baja, nuevos y base antigua).",
     estado="rehacer", cierre=False),

   dict(
     t="Cada mes hasta 2.3 M personas reciben tres o más campañas el mismo día, casi siempre con Marketing en el choque",
     tipo="Gráfica + lecturas",
     viz="Matriz mes contra campañas distintas el mismo día (1, 2, 3 a 4, 5 a 7, 8 o más): color = bajas por mil personas-día, tamaño del círculo = personas-día. Al lado, tabla de equipos con el % de choques promocionales en que participa cada uno y su tema principal.",
     ctx=[
       ("Qué se manda", "Dos o más promociones el mismo día a la misma persona: Hot Sale, Comercio del día, lanzamiento de BillPay, Anota y Gana, Mundial y Día del Padre, Tasa 0. 65 % de los choques medidos es promocional con promocional."),
       ("Quién", "Marketing participa en 63 % de los choques promocionales (medidos en personas-día, una persona en un día), Sales en 41 %, Product Growth en 25 % y NewProducts y QA en 17 %. Un choque cuenta para los dos equipos. Collections no aparece en choques promocionales."),
       ("A quién", "Recurrentes y activos de KPay, leads y 'Todos'. Mayo, junio y agosto son los meses con más choque (Hot Sale, BillPay, regreso a clases)."),
       ("Ejemplos", "21 de junio: Marketing B0444 Felicitación Día del Padre y Marketing B00527 Onboarding de Billpayments, dos push a 1.54 M personas. 11 de agosto: QA-KPay B001 Reminder registro teléfono (un Canvas de prueba que salió a clientes) y Marketing B00527, dos push a 1.45 M. Junio: Product Growth B0440 Anota y Gana y NewProducts BillPay Intro, dos push a 1.23 M."),
       ("Impacto", "Los días con tres o más campañas son 9 % de las personas-día y llevan 24 % de los mensajes. Bajas por mil personas-día: 0.36 con una campaña y 0.70 con ocho o más; de julio a septiembre, 0.32 contra 1.10."),
     ],
     h=[
       "Personas con al menos un día de tres o más campañas: 1.30 M en enero, 2.26 M en junio, 2.09 M en agosto y 1.48 M en septiembre.",
       "Por pareja, Marketing con Marketing es el choque más grande (27.6 M personas-día), luego Sales con Sales (15.3 M) y Marketing con Sales (14.3 M).",
       "La regla no tiene dueño: nadie administra el calendario y el tope global de frecuencia de Braze está apagado.",
       "La respuesta sube en los días con más campañas porque son días de clientes activos con transaccionales; no prueba que mandar más funcione.",
     ],
     sw="Sin un tope por persona y por día, cada equipo suma su campaña sin ver las de los demás.",
     resp="Por campaña, Marketing: está en dos de cada tres choques promocionales; después Sales y Product Growth. Por la regla, nadie: no hay dueño del calendario ni tope global en Braze. Proponemos que el calendario y el tope los administre un solo equipo de CRM y que Braze los aplique a todos.",
     nota="E6a para bandas y bajas; E6b para equipos (solo los 1,000 pares más frecuentes, 143 M personas-día; es muestra, no universo). Promocional = nombre con ticket y equipo distinto de Collections, misma regla del Sheets.",
     estado="rehacer", cierre=False),

   dict(
     t="Marketing, Sales y Product Growth le escriben a la misma gente con nombres de audiencia distintos",
     tipo="Gráfica + lecturas",
     viz="Matriz equipo contra equipo con personas-día de choque promocional (color) y el tema principal escrito en cada celda. Al lado, por pareja de equipos: % de choques con el mismo nombre de audiencia contra % con nombre distinto pero la misma persona.",
     ctx=[
       ("Qué se manda", "Marketing con Sales: Hot Sale, Comercio del día y cashback para KPay. Marketing con Product Growth: Tasa 0, descuentos y referidos para KCash. Product Growth con Sales: Anota y Gana contra Hot Sale. Todo promocional."),
       ("Quién", "Marketing, Sales, Product Growth y NewProducts."),
       ("A quién", "Recurrentes y activos de KPay (Marketing y Sales). Registrados, anónimos, inactivos y dormants de KCash (Product Growth y Marketing)."),
       ("Ejemplos", "Product Growth B0211 Tasa 0 a registrados y Marketing B0171 Rescate Tasa 0 a anónimos: la misma oferta de dos equipos a 124 mil personas el mismo día, unas cuatro veces cada una. Product Growth B0209 Descuento directo a inactivos y Marketing B0326 Referidos a dormants: dos correos el mismo día a 187 mil. Marketing B0492 Hot Sale comercios deportivos, Sales B0491 Amazon Hot Sale y Sales B0493 Hot Sale KUESKIPROMO: tres push el mismo día a 326 mil recurrentes. Marketing B0495 Cuponera Hot Sale y Sales B0493: cinco meses a 530 mil."),
       ("Impacto", "Choques entre equipos distintos: 42 M de 93 M personas-día de choque promocional (45 %). Marketing con Sales 14.3 M, Marketing con Product Growth 9.0 M, Marketing con NewProducts y QA 7.2 M, Product Growth con Sales 5.1 M."),
     ],
     h=[
       "Sí usan las mismas audiencias. Marketing y Sales coinciden en el nombre de la audiencia en 58 % de sus choques: los recurrentes de KPay.",
       "Marketing y Product Growth coinciden en el nombre solo en 12 %, pero es la misma gente: 'anónimos' para uno y 'registrados' para el otro, 'dormants' para uno e 'inactivos' para el otro.",
       "Los temas que más chocan entre equipos: Hot Sale con Hot Sale, Comercio del día con referidos, inactivos con referidos, y BillPay con Hot Sale y con Anota y Gana.",
     ],
     sw="El nombre de la audiencia esconde el traslape; hace falta un dueño por audiencia y exclusiones entre equipos.",
     resp="Sí, son las mismas personas. Con Sales son los recurrentes de KPay y los temas son Hot Sale, Comercio del día y cashback. Con Product Growth son registrados, anónimos, inactivos y dormants de KCash y los temas son Tasa 0, descuento directo y referidos. Como cada equipo nombra su audiencia distinto, nadie ve que es la misma gente.",
     nota="E6b, 1,000 pares más frecuentes. La columna misma_audiencia de E6b no sirve (compara el tipo de pieza, no la audiencia); la audiencia se tomó del nombre de la campaña y se agrupó. Se traslapa con la lámina 24 (equipos); conviene dejar ahí la idea y aquí el detalle.",
     estado="rehacer", cierre=False),

   dict(
     t="La misma campaña le llega dos veces el mismo día a la misma persona, y solo el WhatsApp repetido costó 0.75 M MXN",
     tipo="Tabla",
     viz="Tabla de repeticiones de una misma campaña (dos versiones, dos audiencias o dos canales): equipo, tipo, canales, personas, personas-día y costo de lo repetido; ordenada por personas-día y con color por equipo.",
     ctx=[
       ("Qué se manda", "La misma campaña en dos versiones, dos audiencias o dos canales: Rescate Tasa 0, Mundial y referidos, Hot Sale, Comercio del día, churn por WhatsApp, nunca activos por email y WhatsApp, y el correo de desembolso (transaccional)."),
       ("Quién", "Marketing 5.9 M de 9.9 M personas-día repetidas; Product Growth 1.7 M; Sales 1.2 M; el correo de desembolso de KCash (transaccional, sin equipo en el nombre) 1.1 M."),
       ("A quién", "Hot leads y base rezagada (Marketing), churn de 12 meses y nunca activos (Product Growth), recurrentes de KPay (Sales) y clientes que acaban de recibir su préstamo (desembolso)."),
       ("Ejemplos", "Marketing B0171 Rescate Tasa 0 a 'hot leads' y a 'base rezagada' (1 de junio): 112 mil personas recibieron los dos WhatsApp el mismo día, unas tres veces cada una, y 102 mil recibieron email y WhatsApp, varias veces. Marketing B0444 Referidos y Mundial, mismo ticket (11 de junio): dos push a 1.13 M. Product Growth B0333 Churn 12 meses: tres versiones del mismo WhatsApp entre el 8 y el 14 de abril. Product Growth B0223 Nunca activos: email y WhatsApp el mismo día en abril, mayo y junio. Sales B0493 Hot Sale: el mismo push el 27 y el 29 de mayo a 326 mil. KCash desembolso: dos versiones del correo activas a la vez, 600 mil personas con dos correos de desembolso el mismo día durante cuatro meses."),
       ("Impacto", "9.9 M personas-día con la misma campaña repetida (7 % de los choques medidos; es un piso). WhatsApp repetido: 1.06 M envíos, cerca de 0.75 M MXN en 9 meses con la entrega real de esas campañas (70 %)."),
     ],
     h=[
       "Siete de cada diez repeticiones son en el mismo canal: dos push o dos correos iguales el mismo día.",
       "La causa es operativa: se lanza la misma campaña por audiencia o por día sin excluir a quien ya la recibió, y la versión vieja sigue activa cuando se crea la nueva.",
       "Ahorro directo: cerca de 0.75 M MXN de WhatsApp (unos 83 mil al mes) y hasta 10 M de mensajes; el beneficio mayor es tener menos días saturados, que desde junio traen más bajas.",
     ],
     sw="Una regla de Braze (no repetir la misma campaña a la misma persona el mismo día) y apagar versiones viejas lo resuelven sin tocar el contenido.",
     resp="Ejemplos en la tabla. Causa mensajes de más sin respuesta adicional y días saturados. Se ahorra cerca de 0.75 M MXN de WhatsApp en 9 meses y hasta 10 M de mensajes. Responsables: Marketing en seis de cada diez repeticiones (Rescate Tasa 0, Mundial y referidos), Product Growth (churn y nunca activos), Sales (Hot Sale, Comercio del día) y el dueño del correo de desembolso de KCash.",
     nota="E6b: pares con la misma campaña sin fecha o el mismo ticket del mismo equipo, sin tickets genéricos (B0000, T0000, B001). Cifras piso porque E6b solo trae los 1,000 pares más grandes. Una persona-día puede contar en varios pares si la campaña tiene tres versiones (Mundial).",
     estado="rehacer", cierre=False),

   dict(
     t="Después del tercer mes casi nadie abre el push, y le seguimos mandando unos diez al mes",
     tipo="Gráfica + lecturas",
     viz="Por antigüedad del usuario al momento del envío (menos de 1 mes, 1 a 3, 3 a 6, 6 a 12 meses, 1 a 2 años, más de 2 años): push por persona al mes en barras y apertura de push en línea; segunda línea con correos por persona al mes. Etiqueta con bajas por mil correos en cada banda.",
     ctx=[
       ("Qué se manda", "Push promocional: Comercio del día, Hot Sale, referidos, rescates de fin de semana, Anota y Gana."),
       ("Quién", "Push a recurrentes: Sales 44.7 M (abre 1.27 %), Marketing 26.2 M (1.63 %), Product Growth 9.9 M (5.0 %). Push a leads de bases viejas: Marketing 69.9 M (1.03 %). Push a dormants: Marketing 3.4 M (0.43 %)."),
       ("A quién", "Usuarios con más de 6 meses en la base: reciben 73 % de todos los envíos y 73 % del push."),
       ("Ejemplos", "Sales B0493 Hot Sale KUESKIPROMO a recurrentes de KPay: 4.6 M push, abre 1.09 %. Sales B0585 Comercio del día de agosto a recurrentes: 2.8 M, 1.08 %. Marketing B0391 Rescate fines de semana a recurrentes de Lending: 2.8 M, 1.42 %. Marketing B0561 Comercio del día a recurrentes: 2.7 M, 1.20 %."),
       ("Impacto", "Más de 2 años en la base: 71.5 M push en 9 meses a 783 mil personas, abre 1.27 %. El piso que fijamos para push es 0.75 % de apertura y el estándar de la industria 3 a 10 %."),
     ],
     h=[
       "Por mes, el push casi no cambia con la antigüedad: unos 13 al mes en los primeros 3 meses y 7 a 10 después. Lo que cambia es la apertura: 3.4 % el primer mes, 1.9 % del mes 1 al 3 y 1.3 % desde el sexto.",
       "El 'siete veces más push' comparaba 9 meses de un usuario antiguo con el único mes de un nuevo; por mes es parecido. Lo corregimos.",
       "El email pega al inicio: 9 correos en el primer mes, unos 4 al mes hasta el sexto y menos de 2 después.",
       "Las bajas de email son iguales en todas las antigüedades (3.0 a 3.6 por mil correos). En push no sabemos: no hay registro de quien apaga las notificaciones.",
     ],
     sw="Al antiguo no le mandamos más, le seguimos mandando igual aunque ya no abre: el push debe ir a quien abrió uno en los últimos 90 días.",
     resp="Temas: Comercio del día, Hot Sale, referidos y rescates de fin de semana, casi todo promocional. ¿Se desuscriben? Por email no más que los nuevos; en push no podemos saberlo. Responsables: Sales y Marketing, con push a recurrentes de KPay y a leads de bases viejas. Momento: la apertura cae a la mitad entre el primer y el tercer mes y se queda en 1.3 % desde el sexto.",
     nota="E12 mide la antigüedad al momento del envío; cada banda dura distinto (el nuevo pasa como máximo un mes en 'menos de 1 mes', el antiguo pasa los 9 meses en 'más de 2 años'). Por mes = mensajes por persona entre la duración de la banda dentro del periodo (piso). E12 no trae equipo ni campaña; se aproxima con la audiencia del nombre en E1. Extracción que lo resuelve: E12 con campaña y equipo.",
     estado="rehacer", cierre=False),

   dict(
     t="Por qué pasa: no hay tope de mensajes por persona ni calendario común; cada Canvas suma sin ver los demás",
     tipo="Cierre de sección",
     viz="Cierre: cadena de causas, hipótesis analítica, operativa y de gobierno, cómo (semana, dónde en Braze, equipo, métrica) y qué ganamos.",
     ctx=[
       ("Qué se manda", "Promocionales que más presionan. Marketing: Comercio del día (B0561, B0534), Rescate fines de semana (B0391), Rescate Tasa 0 (B0171), Referidos (B0326), Mundial y Día del Padre (B0444), Onboarding de Billpayments (B00527), recordatorio de registro (B0000 Veriff, PersonalInfo, NIP). Sales: Hot Sale (B0491, B0493) y Comercio del día. Product Growth: Tasa 0 a registrados (B0211), Anota y Gana (B0440), nunca activos (B0223), churn por WhatsApp (B0333). NewProducts: BillPay Intro y sus recordatorios."),
       ("Quién", "Marketing, Product Growth, Sales y NewProducts. Collections y los transaccionales quedan fuera del tope."),
       ("A quién", "Recurrentes de KPay, leads y registrados de KCash, nuevos en su primer mes."),
       ("Ejemplos", "Ver láminas 31 a 36."),
       ("Impacto", "Cerca de 19 M mensajes menos al mes al rehacer y bajar frecuencia, y menos bajas en los días saturados."),
     ],
     h=[
       "Causas: cada equipo arma su audiencia con su propio nombre; el tope global de frecuencia de Braze está apagado; nadie es dueño del calendario; las versiones viejas no se apagan.",
       "Cómo: en Braze, máximo 2 promocionales al día y 1 push promocional al día por persona; 5 promocionales a la semana como punto de partida; no repetir la misma campaña a la misma persona el mismo día; una sola secuencia de bienvenida; calendario único para envíos de más de 1 M; push solo a quien abrió uno en 90 días.",
       "Transaccional y cobranza (Collections BKT, desembolso, pagos) quedan fuera del tope, pero con una sola versión activa.",
       "Métrica: personas con 3 o más campañas al día, bajas por mil personas-día y apertura de push en la base de más de 6 meses, cada semana.",
     ],
     sw="Se corrige con reglas en Braze y un dueño del calendario, no campaña por campaña.",
     resp="Los promocionales que hay que nombrar están en 'Qué se manda': Comercio del día, Rescate fines de semana, Rescate Tasa 0, Referidos, Mundial y Día del Padre y Onboarding de Billpayments de Marketing; Hot Sale y Comercio del día de Sales; Tasa 0, Anota y Gana, nunca activos y churn de Product Growth; BillPay de NewProducts.",
     nota="19 M mensajes al mes: MUESTRA_C (18.6 M; la tabla suma 18.7 M). El tope de 5 por semana viene de METRICAS.md y no de un dato semanal; el de 2 por día sí tiene dato (E6a).",
     estado="rehacer", cierre=True),
 ])]),

 dict(n="V", nombre="El ritmo lo marcan los lanzamientos, no el cliente",
      arg="Los picos de volumen son lanzamientos de Marketing y NewProducts que caen la misma semana. En esas semanas la respuesta baja y las bajas siguen llegando uno o dos meses después; medir por mes lo esconde y el día de la semana importa menos de lo que parece.",
      subs=[dict(nombre=None, sl=[

   dict(
     t="Las semanas pico son semanas de lanzamientos, y en ellas la respuesta cae",
     tipo="Gráfica + lecturas",
     viz="Dispersión semanal: volumen de la semana contra respuesta, un panel por canal (clic de email, apertura de push, lectura de WhatsApp), con recta y R²; cada semana pico etiquetada con el lanzamiento y el equipo que la explica.",
     ctx=[
       ("Qué se manda", "Lanzamientos y campañas de temporada a casi toda la base: BillPay, Hot Sale, Comercio del día, Mundial y Día del Padre, Anota y Gana, regreso a clases. Promocional."),
       ("Quién", "Marketing está en las cinco semanas pico y NewProducts explica la más grande; Sales en Hot Sale y regreso a clases. Junio tuvo 44 M mensajes más que el promedio de enero a abril: 26 M de NewProducts y 20 M de Marketing."),
       ("A quién", "'Todos', leads y recurrentes de KPay."),
       ("Ejemplos", "Semana del 1 de junio, 39.6 M: BillPay Intro por email a 16.1 M (NewProducts) más push de Hot Sale de Sales y Marketing. Semana del 25 de mayo, 26.2 M: Hot Sale de Sales (B0491 Amazon, B0493 KUESKIPROMO, B0500 TEMU) y Referidos de Marketing a 1.2 M. Semana del 15 de junio, 22.6 M: Marketing B00527 Onboarding de Billpayments 3.2 M, Comercio del día 3.2 M, Día del Padre 1.6 M y Mundial 1.1 M. Semana del 10 de agosto, 21.6 M: QA B001 Reminder registro teléfono 1.9 M y Marketing B00527 1.7 M. Semana del 20 de julio, 20.4 M: Marketing B0561 Comercio del día, 6.6 M push."),
       ("Impacto", "Email: cada millón extra en la semana baja el clic 0.05 puntos (R² 0.60); sin junio, 0.09 puntos (R² 0.65). Push: 0.11 puntos de apertura por millón (R² 0.53). WhatsApp no depende del volumen (R² 0.01)."),
     ],
     h=[
       "La mayoría de las semanas lleva entre 12 y 18 M y la sostienen los Canvas de siempre (Tasa 0, recordatorio de registro, cobranza); lo que sube la semana son los lanzamientos.",
       "En email la relación se mantiene sin junio: no es solo el efecto de BillPay.",
       "No es solo volumen: en las semanas pico entra gente que casi nunca responde. El efecto es volumen más audiencia fría.",
     ],
     sw="El volumen no se decide semana a semana: se acumula porque cada equipo fija su lanzamiento sin ver el de los demás.",
     resp="Lo que sube el volumen son lanzamientos y campañas de temporada a toda la base: BillPay (NewProducts y Marketing), Hot Sale (Sales y Marketing), Comercio del día, Mundial y Día del Padre (Marketing) y una prueba de QA que salió a clientes. Marketing está en las cinco semanas pico; NewProducts en la más grande.",
     nota="Semanas: E4a. Para nombrar lo que hay detrás de cada semana se usaron las fechas de primer y último envío del catálogo (E2) en campañas que duran 10 días o menos; cubre 16 % del volumen, alcanza para nombrar los picos pero no para repartir cada semana. Para eso: E4a con equipo y campaña.",
     estado="rehacer", cierre=False),

   dict(
     t="Junio sumó 43 M push nuevos de cuatro equipos y casi nadie los abrió",
     tipo="Gráfica + lecturas",
     viz="Línea semanal de push de mayo a julio con la apertura en un segundo panel, cada lanzamiento anotado con equipo y tema. Al lado, matriz tema contra equipo con envíos de push nuevos (tamaño) y apertura (color).",
     ctx=[
       ("Qué se manda", "Lanzamiento de BillPay (intro, tres recordatorios y onboarding), recordatorio de TopUps, Anota y Gana, Mundial y Día del Padre, Comercio del día, referidos, rescate de fin de semana y Hot Sale. Todo promocional."),
       ("Quién", "Push nuevo de junio (campañas que no mandaron push en mayo): Marketing 25.6 M, NewProducts 9.4 M, Product Growth 5.5 M, Sales 2.5 M."),
       ("A quién", "Toda la base y leads; cada push masivo llegó a entre 1.2 y 3.2 M personas."),
       ("Ejemplos", "NewProducts BillPay Reminder: tres push en 11 días a los mismos 1.6 M, abre 0.65 %. Marketing B00527 Onboarding de Billpayments a leads y recurrentes: 3.2 M, 0.55 %. Product Growth B0440 Anota y Gana a 'Todos': 3.1 M, 0.76 %. Marketing B0444 Mundial: 2.2 M, 1.12 %. Marketing B0534 Comercio del día: 2.0 M, 0.98 %. Marketing B0444 Felicitación Día del Padre: 1.6 M, 0.96 %."),
       ("Impacto", "Push de junio: 46.8 M, 33 % más que mayo. Los 139 push nuevos (43 M) abrieron 0.87 % contra 3.11 % de las que ya existían; la apertura del mes cayó a 1.05 %, la más baja del año."),
     ],
     h=[
       "El tema que más pesó fue BillPay: 9.6 M push en junio entre NewProducts y Marketing, dos equipos con el mismo lanzamiento.",
       "La semana del 8 de junio tres equipos mandaron push masivo a la vez: NewProducts (TopUps y BillPay, 1.6 M cada uno), Product Growth (Anota y Gana, 1.6 M) y Marketing (Mundial, 1.1 M).",
       "En email junio no fue un mes malo, fue un correo malo: sin BillPay Intro el clic de junio fue 0.89 %, igual que mayo (0.84 %).",
     ],
     sw="Un lanzamiento no debería salir a toda la base por dos equipos y cuatro veces en un mes.",
     resp="Temas: lanzamiento de BillPay (NewProducts y Marketing), Anota y Gana (Product Growth), Mundial, Día del Padre, Comercio del día y referidos (Marketing), TopUps (NewProducts) y Hot Sale (Sales). Todo promocional y casi todo a toda la base.",
     nota="deck_data.culpables_push_junio (E1). Nuevo = la campaña no mandó push en mayo. El guion decía 'tres equipos'; en el mes fueron cuatro, y tres la misma semana del 8 de junio.",
     estado="rehacer", cierre=False),

   dict(
     t="Las bajas suben con las temporadas de ofertas: Navidad y Tasa 0 en enero, BillPay en junio",
     tipo="Gráfica + lecturas",
     viz="Línea mensual de personas que se dan de baja del email; debajo, barras apiladas por mes con el tema del correo desde el que se dieron de baja (Tasa 0, temporada, lanzamiento de BillPay, referidos, recordatorio de registro, otros), con la campaña principal de cada pico anotada.",
     ctx=[
       ("Qué se manda", "Enero: Tasa 0 (31 % de las bajas del mes), Navidad, Reyes y Cuesta de enero (19 %) y newsletter (11 %). Junio: lanzamiento de BillPay (30 %), Tasa 0 (12 %) y Anota y Gana (11 %). Promocional."),
       ("Quién", "Enero: Marketing 51 % y Product Growth 39 % de las bajas del mes. Junio: NewProducts 36 %, Marketing 35 % y Product Growth 26 %."),
       ("A quién", "Enero: base rezagada y anónimos (Marketing), registrados y elegibles (Product Growth). Junio: toda la base con email."),
       ("Ejemplos", "Enero: Product Growth B0312 Christmas a nuevos elegibles (2.5 M correos, 5.8 bajas por mil, clic 0.18 %); Marketing B0308 No Tasa 0 a anónimos y rezagados (salió en diciembre y dejó 18 mil bajas en enero); Marketing B0171 Narrativa Tasa 0 a rezagados (7.4 bajas por mil); Product Growth B0337 Cuesta de enero. Junio: NewProducts BillPay Intro, un correo a 16.1 M con clic de 0.10 %."),
       ("Impacto", "Enero 69 mil personas y junio 63 mil; el mes promedio es 51 mil. BillPay Intro siguió sumando bajas en julio y agosto: 58 mil personas se dieron de baja desde ese correo, y por eso julio también salió alto (53 mil)."),
     ],
     h=[
       "Enero no tiene un masivo: es la cola de las ofertas de diciembre (Navidad, No Tasa 0) más Tasa 0 y Cuesta de enero.",
       "Junio sí es un solo correo: BillPay Intro, 30 % de las bajas del mes.",
       "El daño de un masivo no se ve completo en su mes: sigue llegando durante dos o tres meses.",
     ],
     sw="Las temporadas y los lanzamientos necesitan un límite de audiencia y de toques, no solo una fecha.",
     resp="Junio: BillPay Intro de NewProducts, un correo de lanzamiento de BillPay a 16.1 M personas, promocional. Enero no fue un masivo sino la temporada: Navidad, Reyes y Cuesta de enero de Product Growth y Tasa 0 de Marketing a bases rezagadas, más la cola de lo enviado en diciembre.",
     nota="Personas por mes: E4a (enero 69,226; junio 63,425; julio 52,912). Reparto por tema y equipo: eventos de E1, que cuentan bajas que llegan después del envío. BillPay Intro: 37,272 eventos en junio, 24,791 en julio y 17,599 en agosto (E1); 58 mil personas en E8. Se usa 58 mil personas (ver META, 'Bajas por BillPay Intro'). Mes promedio: 457 mil personas-mes entre 9 = 51 mil (el guion decía 49 mil).",
     estado="rehacer", cierre=False),

   dict(
     t="Un solo correo hundió la semana: el clic cayó a un tercio con BillPay y volvió a la normalidad la semana siguiente",
     tipo="Gráfica + lecturas",
     viz="Línea semanal de clic de email de mayo a julio con el volumen en barras; segunda línea con el clic de esa misma semana sin BillPay Intro; marca en la semana en que el reporte mensual habría mostrado el problema (inicio de julio).",
     ctx=[
       ("Qué se manda", "BillPay Intro: lanzamiento de BillPay por email a toda la base. Promocional."),
       ("Quién", "NewProducts (en Others)."),
       ("A quién", "16.1 M personas, casi toda la base con email, incluidas las que nunca habían respondido."),
       ("Ejemplos", "NewProducts-Kueski-20260601 BillPay Intro Full Rollout, enviado el lunes 1 de junio: 64 % de los correos de esa semana, apertura 7.7 %, clic 0.10 %, costo 0.8 M MXN."),
       ("Impacto", "Semana del 1 de junio: clic 0.36 % contra 1.05 % la siguiente; sin BillPay esa semana habría tenido 0.79 %. El mes cerró en 0.67 % y el problema se leyó en julio, cuando ya habían salido los tres recordatorios de BillPay por push."),
     ],
     h=[
       "Lo atribuimos a una sola campaña: sin BillPay Intro la semana y el mes de junio responden como mayo.",
       "Medir por mes promedia el golpe y llega cuatro semanas tarde.",
       "Pasa también en push: las semanas del 8 y del 15 de junio abrieron 1.13 % y 0.92 % con siete lanzamientos encima.",
     ],
     sw="Hace falta una lectura semanal por campaña con alerta: si un envío de más de 1 M queda debajo del piso (0.3 % de clic en email, 0.75 % de apertura en push) en su primera semana, se frena lo que sigue.",
     resp="La versión anterior de la lámina decía que el reporte mensual nos avisó tarde. Lo atribuimos a un solo correo: BillPay Intro de NewProducts fue 64 % del email de la semana del 1 de junio y casi nadie le dio clic; sin él la semana habría tenido 0.79 % de clic, un valor normal.",
     nota="E4a semanal y E1. Supone que el correo de BillPay salió completo la semana del 1 de junio (campaña con primer envío ese día). Rango semanal de junio: 0.36 % a 1.14 % (el guion decía 1.00 %, que es la semana del 29 de junio).",
     estado="rehacer", cierre=False),

   dict(
     t="El lunes no responde peor por ser lunes: sin el correo de BillPay, su clic es igual al de cualquier día",
     tipo="Gráfica + lecturas",
     viz="Matriz día de la semana contra equipo: color = clic de email, círculo = correos entregados; fila extra 'lunes sin BillPay Intro'. Advertencia en sábado y domingo por pocos envíos.",
     ctx=[
       ("Qué se manda", "El lunes salen el lanzamiento de BillPay (NewProducts) y los correos más grandes de Product Growth (Tasa 0, inactivos, nunca activos). Promocional."),
       ("Quién", "Email del lunes: Product Growth 39 % (clic 0.29 %), Others 31 % (casi todo BillPay Intro), Marketing 18 % (1.00 %), Collections 7 %, Sales 4 %."),
       ("A quién", "Registrados sin crédito, inactivos y nunca activos (Product Growth); toda la base (BillPay)."),
       ("Ejemplos", "BillPay Intro salió el lunes 1 de junio: 14.3 M correos entregados, 20 % de todo el email de los lunes en 9 meses. Product Growth manda el lunes envíos de 40 mil personas por campaña contra 19 mil el resto de la semana, y su clic baja de 0.51 % a 0.29 %."),
       ("Impacto", "Lunes: 23 % del email y 0.65 % de clic. Sin BillPay: 19 % y 0.78 %, casi igual que martes y viernes (0.82 %)."),
     ],
     h=[
       "Lo que hunde al lunes es un masivo (BillPay) y el tamaño de los envíos de Product Growth, no el día.",
       "El domingo parece el mejor día (1.91 % de clic), pero lleva 5 % del email y parte de sus clics son de correos de días anteriores: la tabla registra el clic el día en que ocurre.",
       "No se puede nombrar cada campaña de Product Growth del lunes: E10 no trae campaña.",
     ],
     sw="La regla no es 'no mandar en lunes' sino 'no mandar masivos sin prueba', cualquier día.",
     resp="El masivo más grande del lunes es BillPay Intro (NewProducts, lanzamiento de BillPay a 16 M el 1 de junio). Después vienen los correos de Product Growth, que el lunes salen al doble de tamaño; por volumen, los candidatos son Tasa 0 a registrados (B0211), Descuento directo a inactivos (B0209) y Nunca activos (B0223). Confirmarlo pide E10 con campaña.",
     nota="E10. Las tasas por día mezclan respuestas de envíos de días anteriores (se registran por fecha del evento), lo que infla los días con pocos envíos. Ver contradicciones nuevas en las notas.",
     estado="rehacer", cierre=False),

   dict(
     t="WhatsApp parece leerse mejor en domingo, pero con 3 % de los envíos no alcanza para mover el calendario",
     tipo="Gráfica + lecturas",
     viz="Matriz día de la semana contra equipo para WhatsApp: color = lectura sobre entregados, círculo = envíos; en gris las celdas arriba de 100 % (lecturas de envíos de otros días).",
     ctx=[
       ("Qué se manda", "WhatsApp promocional: Tasa 0, referidos, churn, inactivos, Hot Sale."),
       ("Quién", "Marketing 56 % del WhatsApp, Product Growth 29 %, Sales 13 %."),
       ("A quién", "Leads rezagados, churn, inactivos y recurrentes."),
       ("Ejemplos", "El domingo cada campaña de WhatsApp llega a unas 2.7 mil personas, contra 16 mil el lunes: son envíos chicos y de seguimiento, no masivos."),
       ("Impacto", "Domingo: 87 % de entrega y 89 % de lectura contra 72 % y 66 % el lunes, pero solo 1.6 M de 55 M WhatsApp (3 %)."),
     ],
     h=[
       "Por equipo se repite: Product Growth en domingo 84 % de entrega y 91 % de lectura contra 63 % y 59 % el lunes; Marketing 87 % y 77 % contra 74 % y 67 %.",
       "Sales marca 175 % de lectura el domingo: imposible si solo contara lo enviado ese día. La tabla registra la lectura el día en que ocurre, y el domingo suma lecturas de mensajes del viernes y el sábado.",
       "No sabemos si pasa todos los meses ni en qué campañas: E10 no trae mes ni campaña.",
     ],
     sw="Antes de mover WhatsApp al fin de semana hay que probarlo: la misma campaña en domingo y en martes, con grupo de control.",
     resp="No sabemos si es siempre: E10 no trae el mes. Aparece en Product Growth, Marketing y Sales, pero el domingo es 3 % del WhatsApp, con envíos mucho más chicos, y parte de la lectura es de mensajes de otros días. No hay datos por campaña. Extracción que lo resuelve: E10 con mes, campaña y lectura atribuida al día del envío.",
     nota="E10. Volumen de WhatsApp por equipo: Marketing 30.8 M, Product Growth 15.9 M, Sales 7.4 M de 55.2 M.",
     estado="rehacer", cierre=False),

   dict(
     t="Por qué pasa: no hay tope semanal de volumen ni revisión semanal; los lanzamientos no se coordinan",
     tipo="Cierre de sección",
     viz="Cierre: cadena de causas, hipótesis analítica, operativa y de gobierno, cómo (semana, dónde en Braze, equipo, métrica) y qué ganamos.",
     ctx=[
       ("Qué se manda", "Lanzamientos y temporadas a toda la base: BillPay, Hot Sale, Mundial, Día del Padre, regreso a clases, Navidad y Cuesta de enero."),
       ("Quién", "NewProducts, Marketing, Sales y Product Growth."),
       ("A quién", "'Todos', leads y recurrentes."),
       ("Ejemplos", "Semana del 1 de junio (BillPay Intro), semana del 8 de junio (tres equipos con push masivo), enero (Navidad y Tasa 0)."),
       ("Impacto", "Una sola semana mal coordinada dejó clic de 0.36 % y 58 mil bajas de un solo correo."),
     ],
     h=[
       "Causas: cada equipo lanza a toda la base en su fecha; nadie ve que caen la misma semana; el reporte es mensual y llega tarde.",
       "Cómo: calendario único de lanzamientos con máximo un envío a toda la base por semana; prueba al 10 % antes de cualquier envío de más de 1 M; tope semanal por canal y límite de velocidad de envío en Braze; lectura semanal por campaña con alerta en la primera semana.",
       "Día de la semana: no mover envíos por día sin probarlo con grupo de control; el lunes se arregla quitando el masivo, no el lunes.",
     ],
     sw="Coordinar las fechas vale más que elegir el día.",
     resp="Sin pregunta (ok). Se ajustó al nuevo hallazgo: el problema es el masivo, no el día.",
     nota=None,
     estado=None, cierre=True),
 ])]),
]
