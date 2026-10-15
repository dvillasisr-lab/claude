# Storyline del deck (ghost deck)

Audiencia: dirección y líderes de Marketing, Product Growth, Sales, Collections y CRM. Decisión que deben tomar: aprobar el plan de limpieza (582 campañas), adoptar el playbook y pagar la configuración de Braze (control, topes, exclusiones).

Idea de gobierno: Kueski manda 667 M mensajes en 9 meses y gasta 57.7 M MXN, pero el 59 % va a un canal que el usuario nunca abre y 73 % de los usuarios no responde a nada. Mandando menos, a quien sí responde y con grupo de control, se ahorran 1.6 M MXN al mes (33 % del gasto) y se recupera la respuesta.

SCQA
- Situación: 5 equipos, 1,913 campañas por canal, 667 M mensajes, 57.7 M MXN de costo variable (WhatsApp 71 %).
- Complicación: 19 de 24 indicadores debajo del estándar; la mitad del esfuerzo va a quien no puede o no quiere responder; no hay grupo de control ni pruebas A/B; los equipos chocan en los mismos usuarios.
- Pregunta: qué cambiar para que Braze venda más gastando menos.
- Respuesta: mandar menos y a quien sí. Cuatro movimientos: apagar lo que no responde, excluir y respetar al usuario, canal y frecuencia por usuario, medir con control. Más un playbook y un dueño por cosa.

Títulos de acción en orden (66 láminas). Cada lámina de contenido lleva: exhibit o cifras grandes que prueban el punto, franja Hipótesis / Causa (con tipo: saturación, solape, producto u oferta, audiencia sin segmento, canal, operación, sin medición, método) / Si lo resolvemos, y banda So what.

1. Braze en Kueski: mandar menos y a quien sí
2. Mandar menos y a quien sí ahorra 1.6 M MXN al mes y recupera la respuesta
3. Revisamos 9 meses de envíos: 667 M mensajes, 3,439 comunicaciones y 18 extracciones de Databricks  [stats]
4. WhatsApp es 8 % del volumen y 71 % del costo: Marketing pone 22.9 M MXN y Product Growth 11.4 M; el email más grande es el de Product Growth (117 M) y el push más grande el de Marketing (131 M)  [cifras, stackbar]
5. El volumen subió 86 % de enero a junio y la respuesta cayó en los cuatro canales a la vez  [smallmult]
6. Cada millón de emails más en la semana baja el clic 0.05 puntos y cada millón de push baja la apertura 0.11: el volumen semanal explica 60 % y 53 % de la respuesta  [regress]
7. Semana a semana: push triplicó su volumen la semana del 15 de junio y su apertura cayó a la mitad; email solo se disparó la semana del 1 de junio y WhatsApp lleva desde julio entre 80 y 87 % de la respuesta de enero  [idxgrid]
8. El salto de push de junio lo pusieron 139 piezas nuevas de Marketing (25.6 M), NewProducts (9.4 M) y Product Growth (5.5 M): abrieron 0.87 % contra 3.11 % de las piezas que ya existían  [cifras, barcause]
9. WhatsApp bajó de 5.3 M entregados al mes a 3.1 M y la lectura de 70.5 a 63.3 %: lo que queda va a leads rezagados y churn de Marketing y Product Growth, que leen 50 a 62 %  [cifras, barcause]
10. Dentro de un mes la respuesta se mueve más que entre meses: en junio el clic de email abrió en 0.36 % y cerró en 1.00 %; push cerró septiembre 0.5 puntos debajo de donde abrió  [candle]
11. 19 de 24 indicadores están debajo del estándar; email, push y WhatsApp no llegan al piso de la industria  [cifras, table]
A. Mandamos a quien no responde
13. 73 % de los usuarios no respondió a nada en 9 meses; el 11 % que responde a varios canales recibe la mitad de los mensajes  [hbar2]
14. 2.2 M usuarios que responden a 2 o más canales (11 % de la base) concentran 86 % de las conversiones; los 14.2 M que nunca respondieron, 1 %  [waterfall]
15. 59 % de los mensajes van a un canal que el usuario nunca abrió: 394 M mensajes y 18.7 M MXN  [stats]
16. 97.5 M mensajes fueron a quien nunca respondió: 8.1 M MXN, 17 % de las bajas y cero conversiones  [hbar]
17. La parte del email que va a quien nunca respondió no baja: 14 a 16 % cada mes y 33 % en junio; push sí mejoró, de 15 % en enero a 5 % en septiembre  [multiline]
18. 43.8 M mensajes promocionales llegaron a usuarios bloqueados y 80 mil emails a gente que ya se dio de baja  [hbar]
19. 1 de cada 4 WhatsApp no llega: 14.2 M mensajes en 9 meses que se mandan a números que no reciben  [line]
20. Recibidos y no recibidos: Product Growth pierde 28 % de sus WhatsApp y 6 % de sus emails antes de llegar; Sales entrega 80 % y 97 %  [cifras, stackbar]
B. Mandamos demasiado y sin coordinación
22. 5 % de los usuarios recibe 41 o más mensajes al mes y concentra 30 % del volumen; con 321 o más mensajes la baja se multiplica por 13  [panels]
23. Cada mes 1.3 a 2.2 M usuarios reciben 3 o más campañas distintas el mismo día; desde junio su baja por mil se duplica, mientras quien recibe una sola bajó de 0.57 a 0.34  [panels]
24. Los choques más grandes son dos piezas a 'Todos' el mismo día: 1.5 M usuarios recibieron dos push de Marketing el 21 de junio y un Canvas de QA chocó con 1.45 M usuarios reales  [cifras, table]
25. Un usuario nuevo se da de baja a los 27 días con 5 emails; un solo envío masivo explica 31 % de esas bajas  [hbar]
26. Ocho familias de email generan 37 % de las bajas: Tasa0 a nuevos registrados (46 mil, nueve meses), ReferralProgram y Retargeting Veriff de Marketing (38 mil cada una) y BillPay Intro en un solo envío (37 mil)  [cifras, barcause]
27. 45 Canvas pasan de 20 pasos y 477 pasos abren menos de 1 %; la insistencia no sube la apertura  [colline]
28. El lunes concentra 23 % del email con el peor clic de la semana (0.65 %); el fin de semana responde más en todos los equipos salvo Collections  [heatmap]
29. El fin de semana responde más porque cada pieza llega a 5 veces menos gente (9 mil el domingo contra 45 mil el lunes), no por el día: el tamaño por pieza explica 71 % del clic en los equipos promocionales  [regress]
30. 56 % de los envíos van a usuarios con más de un año en la base, que reciben 7 veces más push y abren la tercera parte  [panels]
C. Sabemos qué funciona
32. Recordar algo que el usuario empezó responde 3.09 % por email; una oferta nueva, entre 0.22 % y 0.53 %  [hbar]
33. Lo que más abren los usuarios es lo que ya empezaron o deben pagar: recordatorios (3.1 % en email, 3.8 % en push) y cobranza (1.8 %, 4.0 %); ofertas, Tasa 0, referidos y lanzamientos responden 0.2 a 0.5 % por email y 0.8 a 1.1 % por push, y son 59 % de los envíos  [cifras, heatmap]
34. In-app responde 38 % y no cuesta; email responde 0.93 % y WhatsApp cuesta 20 veces más por mensaje  [cifras, table]
35. Audiencias de 10 a 100 mil usuarios y 2 toques responden 7 veces más que envíos de más de 1 M con 3 toques  [hbar2]
36. Solo 38 de 308 piezas de email y 26 de 314 de push pasan el mínimo, y las que pasan existen en todos los tamaños: las 270 que no pasan son 81 % del volumen de email y 31 % de los clics  [cifras, scatter]
37. La respuesta por pieza no es una campana: la mitad de las piezas de email está debajo de 0.35 % y el promedio de 1.14 % lo infla el 10 % de piezas arriba de 2.9 %  [hist]
38. Cada equipo tiene un canal que le funciona y otro que le cuesta  [cifras, table]
39. Dentro de cada equipo la respuesta varía más que entre equipos: Marketing promedia 0.62 % de clic con una desviación de 1.09 puntos; Sales, 0.20 % con 0.14  [dotrange]
40. Quién lo maneja mejor: Others (transaccional) y Collections tienen la mejor respuesta por canal y Sales la mejor entrega; Product Growth insiste con 39 % de su volumen tras fallar y Marketing se da de baja 5.9 por mil, el doble que el resto  [cifras, hbarmult]
41. 22 % de los envíos (149 M, 12 M MXN) salieron en meses posteriores a que la pieza ya estaba debajo del mínimo: Product Growth insiste con 39 % de su volumen (Tasa0 a nuevos, 7 meses seguidos), Marketing con 22 %, Sales con 6 %  [cifras, barcause]
42. Active y Precobranza responden 3 a 10 veces más que Leads y Recurrent en email y push, pero reciben 4 % de los envíos; Leads y Recurrent reciben 58 %  [heatmap]
43. 10 piezas concentran 125 M envíos con respuesta debajo del mínimo; 6 piezas hay que proteger  [cifras, table]
D. Nadie puede demostrar cuánto vende Braze
45. 0 de 3,228 Canvas tienen grupo de control real y no hubo una sola prueba A/B de mensaje en 9 meses  [stats]
46. 749 piezas sin ticket, 731 formas de escribir la audiencia y 171 pruebas que llegaron a usuarios reales  [cifras, table]
47. Repetición: 187 familias tienen 5 o más versiones y concentran 35 % de los envíos; 'Comercio del día' existe en 9 segmentos distintos y 'Cuponera' en 7: el mismo segmento se vuelve a crear cada mes  [cifras, hbar]
E. El plan
49. 582 campañas a tocar: 1.6 M MXN al mes de ahorro (33 % del gasto) y 27 M mensajes menos al mes (42 %)  [waterfall]
50. Product Growth tiene 81 % del ahorro; Marketing tiene el mayor volumen a bajar frecuencia  [hbar]
51. Diez piezas con acción concreta cubren 125 M envíos  [cifras, table]
52. El playbook en 12 reglas evita que el desorden vuelva  [cifras, rules]
53. Qué mandar por tipo: el canal, el día y las veces ya están decididos con datos  [cifras, table]
54. Dieciocho ajustes de Braze que se configuran una vez y protegen todo lo demás  [cifras, table]
55. Un dueño por cosa y un calendario único: así se sostiene  [cifras, table]
56. Plan a 90 días: limpiar en 30, configurar en 60, medir en 90  [cifras, gantt]
57. No hacer nada cuesta 19 M MXN al año y 50 mil bajas al mes  [stats]
58. Lo que todavía no sabemos y qué dato lo resuelve  [cifras, table]
59. Próximos pasos: quién hace qué esta semana  [cifras, table]
Anexo. Método, estándares y datos de apoyo
61. Método: 18 extracciones agregadas de Databricks, un modelo en Sheets con fórmulas vivas y 471 verificaciones  [cifras, table]
62. Estándares: los 24 indicadores con su valor actual  [cifras, table]
63. Por mes: envíos, respuesta, bajas y costo  [cifras, table]
64. Por día de la semana: volumen, respuesta y bajas  [cifras, table]
65. Segmentos registrados en Braze: pocos concentran el volumen y 13 % no se rastrea  [hbar]
66. Supuestos y dónde está cada cosa  [cifras, table]

Láminas de culpables (quién, qué pieza, cuándo, a cuántos, por qué): 8 (push de junio por familia y equipo, con la causa al lado), 9 (WhatsApp julio a septiembre por pieza y audiencia), 24 (pares de piezas que chocan), 26 (bajas de email por familia) y 41 (quién insiste tras fallar, por familia y equipo).
Láminas de los temas pedidos: 20 (recibidos y no recibidos por equipo), 33 (qué gancho interesa más por canal), 40 (qué equipo lo maneja mejor, tablero de 6 indicadores), 41 (quién sigue mandando cuando la pieza ya falló) y 47 (repetición de versiones y segmentos duplicados).
Gráficas multivariable: regresión semanal (6), índices por canal (7), velas mensuales (10), cascada de usuarios (14), mudos por mes (17), solape por bandas (22 y 23), regresión por día (29), campana e histograma log (37), dispersión pasa/no pasa con bandas de tamaño (36), heatmap gancho × canal (33) y de segmentos (42), tablero por equipo (40).
