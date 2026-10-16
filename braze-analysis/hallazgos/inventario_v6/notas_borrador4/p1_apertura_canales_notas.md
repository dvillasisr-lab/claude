# Notas de la parte 1 (secciones 0, I y II; láminas 1 a 19 más una nueva)

Scripts: `scratchpad/v6parts/p1/base.py` (carga de E1 con equipo, tipo, audiencia y tema por las reglas del Sheets v4) y cálculos en línea con pandas. Todo sobre `data/e1_comunicacion_mes_canal.csv` salvo donde se indica. Costo = email enviado × 0.05 + WhatsApp entregado × 1.00 (no se usa la columna costo_mxn de E1, que cobra WhatsApp enviado). Equipo: Marketing, Product Growth, Sales y Collections tal cual; todo lo demás (NewProducts, Compliance, Acquisition, CX, B2B, etc.) es Others.

## Cambios de estructura

- Se agrega una lámina después de la 11: "WhatsApp funciona con clientes activos y referidos; con bases frías cada conversión cuesta 13 veces más". Responde "¿funciona o no? ¿cuál es la recomendación?" sin cargar la lámina 11. La numeración global de las secciones siguientes se corre una posición.
- La sección II queda en tres subtemas: dónde se va el dinero, dónde está la respuesta y dónde se pierde.
- Títulos de sección nuevos: 0 "Síntesis: lo que pasa y lo que proponemos"; I "Una operación grande que nos responde cada vez menos"; II "Pagamos el canal más caro y desaprovechamos el que más responde".
- Portada: tres opciones de título en `resp` de la lámina 1.

## Cifras nuevas y cómo se calcularon

| Lámina | Cifra | Cálculo |
|---|---|---|
| 2, 5 | Gasto mensual promedio 6.4 M MXN | 57.66 M / 9 |
| 2 | 1.6 M al mes = 25 % del promedio y 38 % de septiembre | 1.6 / 6.41 y 1.6 / 4.23 (septiembre con WhatsApp entregado) |
| 5 | Embudo por canal: email 333.5 / 317.1 / 75.2 / 2.9 M; push 251.1 / 3.8 M; WhatsApp 55.2 / 41.0 / 28.2 M; in-app 27.4 / 10.5 M; 3.38 M conversiones atribuidas | sumas de E1 |
| 5 | 1,829 campañas (familias) y 3,439 comunicaciones | nunique de nombre sin fecha y de communication_id |
| 6 | Promoción 85.6 % de mensajes, 93.1 % del gasto (53.7 M), 63.4 % de las conversiones; avisos 7.6 %, 4.0 %, 28.7 %; cobranza 6.7 %, 2.8 %, 7.9 % | tipo con regla del Sheets (Collections = cobranza; nombre "Transaccional" o sin ticket = aviso) |
| 6 | Clic email 0.60 / 2.74 / 1.09 %; push 1.26 / 6.17 / 3.61 %; bajas por mil 4.3 / 1.0 / 0.3 | por tipo |
| 6 | Tema dentro de promoción: Tasa 0 17.7 %, referidos 15.5 %, recordatorios 12.1 %, descuento 9.6 %, lanzamiento 9.2 % del volumen | regla de gancho del Sheets |
| 7 | Gasto marzo 9.5 M, septiembre 4.2 M (WhatsApp entregado) | suma mensual |
| 7 | Respuestas por mil mensajes 84 (ene), 102 (mar), 54 (sep); conversiones por mil 6.9 a 4.9; MXN por conversión 15.4 (ene), 26.1 (mar), 13.2 (sep) | respuesta = clic email + apertura push + lectura WA + clic in-app |
| 7 | WhatsApp entregado Marketing 5.64 M (mar) a 0.78 M (sep); Sales 1.49 M (feb) a 0.32 M; Product Growth 0.8 a 2.2 M | por equipo y mes |
| 7 | Parte del WhatsApp entregado que va a bases frías: 32 % en enero, 42 % en septiembre | audiencia por nombre |
| 8 | Banda 321+: 220 comunicaciones distintas y 210 días con envío en promedio; 60 % push; 62 % con conversión; 75 % etapa Prospects | E3 ponderado por usuarios |
| 8 | Envíos con 3 o más toques por persona al mes: Marketing 87.5 M, Product Growth 65.5 M, Collections 31.9 M, Sales 13.6 M, Others 8.6 M | E1, envíos / usuarios_aprox por comunicación y mes, filas con 10 mil o más usuarios |
| 9 | Junio menos enero: +50.3 M; Marketing +28.0, Others +25.4, Collections +5.1, Product Growth menos 6.2, Sales menos 2.0 | por equipo y mes |
| 9 | Campañas que más sumaron en junio: BillPay Intro email 16.1 M, BillPay Reminder push 4.8 M, Billpayments Onboarding push 3.2 M, AnotayGana push 3.1 M, BAUMundial 2.2 M | familia × canal, junio contra enero |
| 10 | Email al 1.5 %: +1.81 M clics o 127 M emails menos (6.35 M MXN en 9 meses); push al 3 %: +3.69 M aperturas o 123 M push menos; WhatsApp al 90 % de entrega: 9.7 M envíos menos; lectura al 75 %: 3.36 M MXN menos; bajas a 2.5 por mil: unos 120 mil usuarios menos | regla de tres sobre los totales del canal |
| 11 | Gasto WhatsApp por equipo: Marketing 22.9 M (55.8 %), PG 11.4 M (27.9 %), Sales 5.9 M (14.5 %), Others 0.8 M; por tema: Tasa 0 31 %, otros 26 %, referidos 19 %, descuento 14 %, recordatorio 5 %; por audiencia: fríos 38.5 %, activos 29.7 %, leads 27.5 % | E1 WhatsApp |
| 11b | MXN por conversión atribuida en WhatsApp: activos 48, leads 181, fríos 629; Sales activos 41, Marketing activos 42, PG activos 63, Marketing fríos 676, PG fríos 579 | costo / conversiones_fraccional |
| 11b | Fríos partidos: ex clientes (Dormant, Inactiv, Churn) WhatsApp 6.2 M MXN y 468 MXN por conversión, email 34 MXN; nunca activaron (Rezagad, Never) 9.6 M MXN y 809, email 268 | regex sobre el nombre |
| 11b | WhatsApp entregado julio a septiembre a personas sin ninguna lectura de WhatsApp en 90 días: 2.22 M (23 % de 9.52 M) | E9b, filas con resp_wa = 0 |
| 11b | Campañas: ReferralProgram ClienteKPay 27 MXN por conversión, ClienteKCash 43; Active Retargeting Installments 152; NeverActive 6,920; Churn 12 meses 2,255; RescateTasa0 rezagada 844; NarrativaTasa0 694 | por familia |
| 12 | Cash: WhatsApp 24.7 M MXN y 169.5 mil conversiones = 146 MXN; email 9.0 M y 470 mil = 19 MXN (7.6 veces). Por audiencia WhatsApp contra email: activos 51 contra 4.5; leads 142 contra 74; fríos 602 contra 106 | product_service = Cash |
| 13 | In-app: 99 % promoción; vistas por equipo Marketing 47 %, PG 32 %, Sales 13 %, Others 8 %; clic PG 46 %, Sales 8 %; parte del volumen de cada equipo que va por in-app 0.2 a 5 % | E1 in-app |
| 14 | Clic sobre apertura: promoción 2.85 %, avisos 6.67 %, cobranza 5.18 %; recordatorio 13.96 %, referidos 0.74 %; Sales 0.85 %, PG 2.91 %, Marketing 3.15 %; por tamaño 10 a 100 mil 7.2 %, más de 1 M 1.2 % | email_click / email_open |
| 15 | Push debajo de 1 % por campaña: 140.7 M de 251.1 M (56 %); por equipo Marketing 70.5 %, Others 61.6 %, PG 47.9 %, Sales 34.6 %, Collections 3.0 %; Tasa 0 92 %, leads 83 %, fríos 75 %, activos 29 % | familia × canal |
| 16 | No entregado por equipo Marketing 7.95 M (56 %), PG 4.46 M (31 %), Sales 1.49 M (11 %); por audiencia fríos 51 %, leads 27 %, activos 19 %; diez campañas = 53 %; Marketing a fríos 68 % de entrega contra 84 % a activos | WhatsApp enviado menos entregado |
| 18 | Campañas promocionales por canal con 50 mil o más de base: 831; 306 debajo del piso con 266 M envíos (47 %) y 15.2 M MXN; 161 activas en septiembre. Email 44 % de campañas y 64 % del volumen; push 37 % y 37 %; WhatsApp 21 % y 19 %; in-app 38 % y 28 % | piso: email 0.3 % clic, push 0.75 %, WhatsApp 60 % lectura, in-app 10 % |

## Preguntas que no se pueden responder con los datos

- Lámina 8: qué equipo satura a la banda de 321 o más mensajes. E3 no trae equipo ni campaña; hace falta E3 con equipo y familia por banda. Lo de la lámina es una aproximación por toques por persona al mes.
- Lámina 10: cuántas ventas más daría llegar al piso. Sin grupo de control no se puede pasar de respuestas a ventas.
- Lámina 14: si el problema es el copy o la oferta. Solo una prueba A/B de contenido lo separa; hoy no hay. La apertura de email está inflada por aperturas automáticas (la de 75 % de referidos a leads es sospechosa).
- Lámina 16: motivo de la falla de WhatsApp (número inválido, sin WhatsApp o bloqueo) y calificación de calidad del número. Hace falta el evento de falla de WhatsApp con su razón y el historial de calidad de Meta.
- Lámina 17: qué equipo manda más a canales sin respuesta. E7b y E9b no traen equipo; hace falta E7b con equipo y canal.
- Láminas 11b y 19: si el WhatsApp a dormants realmente recupera clientes. Solo un grupo de control lo dice; la conversión atribuida no es causal.
- Láminas 13 y 19: quién tiene la app (churn y rezagados pueden ser solo web). Falta token de push o login en app por persona.
- Costo fijo de Braze: sigue como supuesto X.

## Contradicciones nuevas o corregidas

1. Costo por conversión de Cash: la nota de canales (H-B5) y la lámina 12 decían 204 MXN y "diez veces" porque cobraban WhatsApp enviado. Con entregado son 146 MXN contra 19 MXN: 7.6 veces. Título corregido a "siete veces".
2. Costo mensual: la lámina 7 decía 12.2 M en marzo y 5.0 M en septiembre (WhatsApp enviado). Con entregado: 9.5 M y 4.2 M. Sigue siendo "menos de la mitad".
3. Ahorro del plan: 1.6 M MXN al mes es 25 % del gasto mensual promedio y 38 % de septiembre con WhatsApp entregado. El "33 %" del deck sale de septiembre con WhatsApp enviado (4.96 M), y el 1.6 M probablemente también se calculó con esa base. Falta reconciliar con los 3.2 M de la nota de campañas.
4. Costo por conversión mensual: bajó de 26 MXN en marzo a 13 MXN en septiembre aunque la respuesta por mensaje cayó; la mejora es de costo (menos WhatsApp), no de respuesta. El título anterior ("no porque mandemos mejor") era correcto en respuesta pero hay que decir lo del costo para no ser contradichos.
5. Campañas debajo del mínimo (lámina 18): el título anterior decía "la mayoría de las campañas activas" en cada canal. Con campañas promocionales de 50 mil o más personas, son 37 % de las campañas pero 47 % del volumen; la mayoría solo vale en volumen de email (64 %). Además, "185 familias de email y 330 de push a apagar o rehacer" usaba otro universo.
6. Push debajo de 1 %: 141 M por campaña con todas sus versiones contra 146 M contando cada versión mensual (MUESTRA_B). Mismo mensaje.
7. In-app de lanzamientos: 41 % de clic con la regla de gancho del Sheets; el playbook dice 54.5 % con otra clasificación.
8. Regla de audiencia: "Billpayments" cae en "transaccional" por la palabra "payment"; la campaña 'LanzamientoBillpayments_Onboarding' de Marketing es promoción. No cambia las cifras grandes, pero conviene corregir la regla.
9. Banda 321+: 75 % aparece como "Prospects" (registrados sin crédito) en la tabla de etapas, pero 62 % tuvo una conversión. La etapa puede ser la última conocida y no la del momento del envío; conviene confirmarlo antes de decir "prospectos" en pantalla.
10. "Cada fallo baja la calidad del número ante Meta" (título anterior de la lámina 16): la calidad depende de bloqueos y reportes, no de números inválidos. Se cambió el título y se dejó la duda en la nota.
