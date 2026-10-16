# Parte 3: notas de IV (presión sobre la persona) y V (cuándo mandamos), láminas 31 a 44

Scripts en `v6parts/p3work/` (a31.py, a32.py, a34*.py, a35.py, a36*.py, a38*.py, a39.py, a40.py, a42.py, a43.py, tema.py). Todo sale de `braze-analysis/data/*.csv`. WhatsApp a 1 MXN por entregado y email a 0.05 MXN por enviado.

## Cifras nuevas y cómo se calcularon

| Lámina | Cifra | Cómo |
|---|---|---|
| 31 | El grupo de 41 o más mensajes en 9 meses (4.47 M personas, 22.9 %) recibe 86.2 % de los mensajes, 96.3 % del push, 85.6 % del WhatsApp entregado y 83.7 % del costo variable (48.7 de 58.3 M MXN) | E3, suma de bandas 41-80, 81-160, 161-320 y 321+ |
| 31 | Ese grupo tiene 90.4 % de las personas con conversión y 42 % de los eventos de baja de email | E3 |
| 31 | Bajas por mil correos por banda de 9 meses: 1 a 5 = 10.9; 6 a 10 = 14.9; 41 a 80 = 2.35; 81 a 160 = 1.72; 161 a 320 = 1.28; 321+ = 1.24 | E3, bajas_email / msgs_email |
| 31 | Prospectos (etapa 7 de la tabla de filtros): 631 mil en el grupo de 41+ con 191 M mensajes (303 por persona); KPay CC Freeze 272 mil con 52 M | E3 por etapa (solo cubre 7 % de los usuarios con golden record) |
| 31 | Mensajes por persona al mes por campaña: Marketing B0561 Comercio del día push a leads 7.7; Collections BKT1 email 6.1; Veriff email 5.3; B0391 Rescate fines de semana 5.0; B0171 Rescate Tasa 0 anónimos 4.8; B0211 Tasa 0 email 4.75 | E1, envíos / suma de usuarios_aprox mensuales, campañas con más de 3 M envíos |
| 32 | Por mes (E4b, todos los meses juntos): 1 a 5 mensajes = 0.59 bajas por 100 personas y 3.04 por mil correos; 41 a 80 = 0.44 y 0.30. Se repite en los 9 meses | E4b, usuarios_con_baja_email (personas) |
| 32 | Por día (E6a): enero a mayo sin gradiente (0.41 con una campaña, 0.45 con 8+); junio a septiembre 0.30 contra 0.91; julio a septiembre 0.32, 0.35, 0.47, 0.65 y 1.10 por mil personas-día | E6a por periodo |
| 33 | En choques promocionales (E6b, 92.8 M personas-día, 65 % de los pares): Marketing participa en 62.6 %, Sales 41.4 %, Product Growth 24.6 %, Others (NewProducts, QA, Shopping) 16.8 %, Collections 0 % | E6b, tipo promocional con la regla del Sheets (ticket en el nombre y equipo distinto de Collections) |
| 34 | Mismo equipo = 54.6 % del choque promocional; entre equipos 45.4 % (42 M). Mismo nombre de audiencia: Sales con Sales 82 %, Marketing con Sales 58 %, Marketing con Marketing 50 %, Product Growth con Sales 24 %, Marketing con Product Growth 12 % | E6b con audiencia tomada del sexto segmento del nombre y agrupada |
| 35 | Repeticiones de la misma campaña: 54 pares, 9.9 M personas-día (7 % de los 143 M); Marketing 5.9 M, Product Growth 1.7 M, Sales 1.2 M, desembolso KCash 1.1 M; 72 % en el mismo canal | E6b, misma campaña sin fecha o mismo ticket del mismo equipo, sin tickets genéricos |
| 35 | WhatsApp con WhatsApp repetido: 1.06 M personas-día; con entrega real de esas campañas (70 %) = 0.75 M MXN en 9 meses | E6b y E1 |
| 36 | Push por persona al mes por antigüedad: menos de 1 mes 12.8; 1 a 3 meses 13.0; 3 a 6 10.6; 6 a 12 7.2; 1 a 2 años 6.9 (piso); más de 2 años 10.1 (piso). Email por persona al mes: 8.8; 4.4; 4.0; 1.7; 1.5; 1.9 | E12, mensajes por persona entre los meses que dura la banda dentro del periodo |
| 36 | Más de 6 meses en la base: 72.8 % de los envíos y 73.2 % del push | E12 |
| 36 | Push por audiencia del nombre: Sales a recurrentes 44.7 M (1.27 %), Marketing a recurrentes 26.2 M (1.63 %), Product Growth a recurrentes 9.9 M (5.0 %), Marketing a leads 69.9 M (1.03 %), Marketing a dormants 3.4 M (0.43 %) | E1 |
| 38 | Regresión semanal sin junio: email pendiente -0.094, R² 0.65; push -0.101, R² 0.39; WhatsApp R² 0.02 | deck_data._ols sobre E4a, quitando semanas de junio |
| 38 | Junio contra promedio enero a abril: +44.4 M mensajes; Others (NewProducts) +25.7 M, Marketing +20.1 M, Collections +3.6 M, Sales -5.8 M | E1 por equipo y mes |
| 38 | Campañas detrás de cada semana pico (25 may, 1 jun, 8 jun, 15 jun, 20 jul, 10 ago) | E1 cruzado con first_sent y last_sent de E2, campañas que duran 10 días o menos (16 % del volumen) |
| 39 | BillPay en push de junio: 9.6 M (NewProducts 6.4 M, Marketing 3.2 M). Clic de email de junio sin BillPay Intro: 0.89 % (mayo 0.84 %) | E1 |
| 40 | Bajas por equipo y tema, en eventos de E1. Enero: Marketing 51 %, Product Growth 39 %; Tasa 0 31 %, temporada 19 %, newsletter 11 %. Junio: NewProducts 36 %, Marketing 35 %, Product Growth 26 %; BillPay 30 % | E1 email_unsubscribe por mes |
| 40 | BillPay Intro: 37,272 eventos de baja en junio, 24,791 en julio, 17,599 en agosto, 354 en septiembre (80,016 en total) | E1 |
| 41 | Semana del 1 de junio sin BillPay Intro: clic 0.79 %, apertura 20.3 %; BillPay fue 64 % del email de esa semana | E4a semana menos los totales de BillPay en E1 |
| 42 | Email del lunes por equipo: Product Growth 39 % (0.29 % de clic, 40 mil por campaña contra 19 mil otros días), Others 31 %, Marketing 18 % (1.00 %). Lunes sin BillPay: 19 % del email y 0.78 % de clic | E10 menos BillPay Intro (E1) |
| 43 | WhatsApp por día y equipo: Product Growth domingo 84 % entrega y 91 % lectura contra lunes 63 % y 59 %; Marketing 87 y 77 contra 74 y 67; Sales domingo 175 % de lectura | E10 |

## Preguntas que no se pueden responder con los datos (y qué extracción lo resuelve)

1. **31: qué campañas exactas recibe el grupo de 41 o más.** E3 no trae campaña. Se aproximó con mensajes por persona al mes de cada campaña (E1). Extracción: E3 con familia y equipo (personas por banda de 9 meses y campaña).
2. **33: quién es responsable de los días de tres o más campañas.** E6a no trae equipo y E6b solo trae los 1,000 pares más grandes, sin mes. Extracción: E6a con equipos presentes en el día y mes.
3. **35: si las repeticiones causan bajas o respuesta extra.** No hay un corte de baja por par. Extracción: E6b con bajas y respuesta del día para los pares.
4. **36: temas, equipos y bajas de push por antigüedad.** E12 no trae equipo ni campaña, y push no registra quien apaga notificaciones. Extracción: E12 con familia y equipo; para push, estado de permiso de notificaciones por usuario (token o push_subscribe real).
5. **38: reparto exacto de cada semana por equipo y campaña.** E4a no trae equipo. Extracción: E4a con equipo y familia.
6. **42: qué campañas de Product Growth salen el lunes.** E10 no trae campaña. Extracción: E10 con familia.
7. **43: si el domingo de WhatsApp se repite cada mes y en qué campañas.** E10 no trae mes ni campaña, y la lectura está fechada el día de la lectura. Extracción: E10 con mes, familia y entrega y lectura atribuidas al día del envío.
8. **Por qué la relación entre días saturados y bajas aparece solo desde junio.** Hipótesis: desde junio esos días traen lanzamientos promocionales. Extracción: E6a con tipo de campaña (promocional, transaccional, cobranza) en el día.

## Contradicciones nuevas

1. **"Siete veces más push" a los antiguos (lámina 36) es un efecto del ancho de la banda.** E12 mide antigüedad al momento del envío: el nuevo pasa como máximo un mes en "menos de 1 mes" y el antiguo pasa los 9 meses en "más de 2 años". Por mes, el push es parecido (13 al mes al inicio, 7 a 10 después). Lo que sí cambia es la apertura (3.4 % a 1.3 %). Se corrigió el título.
2. **Tasas por día de la semana mezclan eventos de otros días (láminas 42 y 43).** E10 agrupa por fecha del evento, no del envío: Sales marca 175 % de lectura de WhatsApp el domingo, Others más de 100 % de entrega, y Collections un clic de email altísimo en domingo sin enviar ese día. Los días con pocos envíos (sábado y domingo) salen inflados. El 1.91 % de clic del domingo y la mejor lectura de WhatsApp en domingo no se pueden tomar como efecto del día.
3. **El lunes malo es casi todo BillPay Intro.** Sin ese correo el lunes hace 0.78 % de clic, igual que martes y viernes. El guion decía que el lunes es el día de "los masivos" en plural; en realidad es uno y el tamaño de los envíos de Product Growth.
4. **La columna `misma_audiencia` de E6b no sirve.** La query compara `split_part(familia, '-', 5)`, pero la familia conserva la fecha (el regexp no funcionó en Spark), así que el quinto segmento es el tipo de pieza (CANVAS), no la audiencia. Cualquier cifra previa basada en esa columna hay que rehacerla.
5. **"Más mensajes, más bajas" (META).** Resuelta así: en 9 meses sube por acumulación de oportunidades; por correo y por mes baja con el volumen (quien recibe poco se va más); por día sí sube, pero solo de junio a septiembre. El "salto de 5 a 6" es de 9 meses y no sostiene un tope semanal; el tope de 5 por semana viene de METRICAS.md, no de un dato.
6. **El efecto del día saturado no es estable.** En enero a mayo no hay gradiente (0.41 con una campaña, 0.45 con ocho o más). La cifra "con ocho o más la baja se duplica" (0.36 a 0.70) es un promedio de dos periodos distintos.
7. **Mes promedio de bajas.** 457,376 personas-mes entre 9 = 51 mil, no 49 mil como decía el guion.
8. **Rango del clic semanal en junio.** 0.36 % a 1.14 %, no 0.36 % a 1.00 % (1.00 % es la semana del 29 de junio).
9. **Bajas de BillPay Intro.** 37 mil eventos en junio, pero 80 mil en total de junio a septiembre (E1) y 58 mil personas en E8. Se usa 58 mil personas. Explica por qué julio (53 mil) también salió alto.
10. **"Tres equipos lanzaron masivos la misma semana" (lámina 39).** En junio el push nuevo fue de cuatro equipos (Marketing, NewProducts, Product Growth y Sales); tres coinciden la semana del 8 de junio.
11. **Enero no tiene "un masivo detrás".** Es la cola de diciembre (Marketing B0308 No Tasa 0 dejó 18 mil bajas en enero sin enviar en enero; Product Growth B0312 Christmas) más Tasa 0 y Cuesta de enero.
12. **Traslape con la lámina 24 (sección III).** "Dos equipos persiguen a la misma persona" repite la idea de la 34. Sugiero dejar en la 24 solo el mensaje y en la 34 el detalle de audiencias y temas.
