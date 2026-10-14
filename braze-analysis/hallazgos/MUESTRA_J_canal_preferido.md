# Muestra J. A qué canal responde cada usuario y cuánto le mandamos por los canales a los que no responde (E7b y E9b, versión 2)

Fuentes: `data/e7b_patron_respuesta.csv` (enero a septiembre) y `data/e9b_patron_respuesta_90d.csv` (julio a septiembre), 16 filas cada una, una por combinación de canales a los que el usuario respondió. Versión 2 del 15 de octubre: traen WhatsApp entregado y ya no traen costo; el costo aquí se calcula como emails enviados × 0.05 más WhatsApp entregados × 1.00 (Meta cobra el mensaje entregado). Cálculo en `hallazgos/muestra_j_patron_respuesta.csv` y `hallazgos/muestra_j_patron_respuesta_90d.csv`.

## Qué significa "respondió" y "no respondió a nada" (leer antes de usar los números)

- **Respondió a un canal** = en la tabla de Braze hay al menos una fila de ese usuario, en ese canal, con el evento de respuesta prendido. El evento es distinto por canal: **email = hizo clic en el correo (`email_click`)**, abrirlo no cuenta; push = tocó la notificación (`pn_open`); WhatsApp = el mensaje aparece como leído (`whatsapp_read`); in-app = hizo clic en el mensaje dentro de la app (`in_app_click`). Ver un in-app sin tocarlo no cuenta; recibir un WhatsApp sin que marque leído no cuenta. Es la misma definición de respuesta que usa la señal de campañas.
- **Corrección respecto a la versión anterior de esta nota**: decía que en email contaba la apertura. E7b siempre midió clic; E9b en su primera versión sí medía apertura, y por eso daba 44 % sin respuesta. Ahora las dos miden clic y son comparables.
- **"Alguna vez" (E7b)** = al menos una vez entre el 1 de enero y el 30 de septiembre de 2026. Basta un solo clic en nueve meses para contar como "responde a email".
- **"En los últimos 90 días" (E9b)** = lo mismo, pero mirando solo del 1 de julio al 30 de septiembre, y contando solo los mensajes de esos 90 días.
- **No respondió a nada** = recibió al menos un mensaje en el periodo (por cualquier canal) y no tiene ni un solo clic en email, ni un toque de push, ni un WhatsApp leído, ni un clic en in-app. Ni uno. Es el usuario al que le mandamos y nunca dio señal de vida. Puede haber abierto emails sin hacer clic: por eso este grupo sí tiene algo de conversión.
- **Canal mudo** = el usuario sí respondió a algún canal, pero a este canal en particular nunca. Ejemplo: alguien que leyó WhatsApps pero jamás hizo clic en un email; para él, el email es canal mudo y cada email que recibe es un mensaje a canal mudo.
- **Lo que no es.** No es "no convirtió" (eso es otra columna). No es "se dio de baja". No es "no le llegó": aquí se cuentan mensajes enviados, le hayan llegado o no, salvo donde se dice "entregados".
- **Ruido conocido.** Si el usuario tiene apagadas las confirmaciones de lectura en WhatsApp aparece como que no leyó aunque haya leído. Por eso "no respondió a nada" es un techo: el número real de usuarios mudos es algo menor.

## Lo que dice (enero a septiembre, E7b)

- **19.5 M usuarios recibieron algo. 14.2 M (73 %) no respondieron a nada en nueve meses.** Se llevaron 24 % de los mensajes (159.5 M) y 14 % del costo (8.0 M MXN), con 0.08 % de conversión y 1.4 % de baja. Son 11 mensajes por usuario en promedio.
- **A ese grupo solo se le entrega el 34 % de sus WhatsApp** (7.6 M enviados, 2.6 M entregados), contra 83 % entre quienes sí leen WhatsApp. Buena parte del "nunca responde" es "no le llega": números dados de baja, cambiados o inexistentes. Es la señal más clara de que la base de WhatsApp necesita limpieza antes que más mensajes.
- **394.4 M mensajes (59 % del total) fueron a un canal al que el usuario nunca respondió**, por 18.7 M MXN (32 % del costo variable). Quitando a los que no responden a nada, quedan 234.9 M mensajes y 10.7 M MXN a canales mudos de gente que sí responde por otro lado.
- **149.0 M emails a 3.9 M usuarios que responden a otro canal pero nunca hicieron clic en un email** (7.5 M MXN). Para ellos el email es ruido y hay un canal que sí funciona.
- **3.2 M WhatsApp entregados (3.2 M MXN; 5.2 M enviados) a usuarios que responden por otro canal pero nunca leyeron un WhatsApp**, y 80.1 M push a usuarios que nunca abrieron uno.
- **Quienes solo responden a WhatsApp son 8 % de los usuarios y 34 % del costo** (19.9 M MXN): reciben 63 mensajes al año cada uno, de los cuales 58.2 M emails y 20.7 M push que nunca abren.
- **Quien responde a varios canales convierte mucho más**: email + push + WhatsApp + in-app convierte 75 %, in-app solo 8.8 %, WhatsApp solo 2.0 %. No es que los canales conviertan: es que los clientes activos usan la app y por eso ven in-app y convierten. Sirve para segmentar, no para atribuir.
- **La baja de email se concentra en quienes responden a email**: 15.8 % en "solo email" y 13.9 % en "email + WhatsApp", contra 1.4 % en los que no responden. Es lógico (para darse de baja hay que abrir), pero dice que el lector de email que no usa la app es el que más se cansa.

Costo total del periodo con esta base: 58.3 M MXN (72.5 M si se cobrara el WhatsApp enviado).

| Responde a | Usuarios | % usuarios | % msgs | % costo | Msgs por usuario | MXN por usuario | Convierten | Baja email | Msgs a canal mudo | WhatsApp entregado |
|---|---|---|---|---|---|---|---|---|---|---|
| ninguno | 14.2 M | 72.9 % | 23.8 % | 13.8 % | 11 | 0.6 | 0.08 % | 1.4 % | 159.5 M | 34 % |
| WhatsApp | 1.6 M | 8.1 % | 14.9 % | 34.2 % | 63 | 12.6 | 2.03 % | 3.4 % | 79.0 M | 81 % |
| in-app | 1.1 M | 5.5 % | 6.9 % | 3.7 % | 43 | 2.0 | 8.84 % | 1.7 % | 42.5 M | 65 % |
| WhatsApp + in-app | 511 mil | 2.6 % | 9.2 % | 11.5 % | 120 | 13.1 | 37.33 % | 2.9 % | 51.5 M | 86 % |
| push + WhatsApp + in-app | 371 mil | 1.9 % | 12.9 % | 10.5 % | 234 | 16.5 | 62.14 % | 2.1 % | 26.6 M | 87 % |
| email | 365 mil | 1.9 % | 1.8 % | 1.2 % | 33 | 1.9 | 5.03 % | 15.8 % | 2.4 M | 35 % |
| push + in-app | 280 mil | 1.4 % | 5.9 % | 2.5 % | 142 | 5.2 | 36.96 % | 1.8 % | 13.5 M | 71 % |
| email + push + WhatsApp + in-app | 255 mil | 1.3 % | 10.0 % | 8.2 % | 262 | 18.7 | 75.47 % | 5.1 % | 0 | 86 % |
| email + WhatsApp + in-app | 228 mil | 1.2 % | 4.5 % | 6.0 % | 134 | 15.3 | 56.13 % | 7.2 % | 8.2 M | 85 % |
| email + in-app | 205 mil | 1.1 % | 2.4 % | 1.6 % | 78 | 4.6 | 30.33 % | 7.9 % | 5.4 M | 63 % |
| email + WhatsApp | 169 mil | 0.9 % | 1.8 % | 3.9 % | 73 | 13.4 | 17.13 % | 13.9 % | 1.6 M | 77 % |
| email + push + in-app | 134 mil | 0.7 % | 3.6 % | 1.6 % | 181 | 7.1 | 57.47 % | 5.5 % | 752 mil | 67 % |
| push | 58 mil | 0.3 % | 1.0 % | 0.2 % | 111 | 2.3 | 6.13 % | 1.7 % | 1.7 M | 53 % |
| push + WhatsApp | 36 mil | 0.2 % | 0.9 % | 0.8 % | 173 | 13.1 | 12.81 % | 2.3 % | 1.7 M | 84 % |
| email + push | 10 mil | 0.1 % | 0.2 % | 0.1 % | 108 | 3.3 | 25.87 % | 7.2 % | 48 mil | 42 % |
| email + push + WhatsApp | 9 mil | 0.1 % | 0.2 % | 0.2 % | 142 | 11.1 | 34.90 % | 7.6 % | 36 mil | 80 % |

## Con ventana de 90 días (julio a septiembre, E9b)

Misma lógica, pero solo cuentan las respuestas y los mensajes del 1 de julio al 30 de septiembre. Es la versión fina de "canal mudo", porque un clic de enero ya no rescata a nadie.

- 7.07 M usuarios recibieron algo en el trimestre. **4.10 M (58 %) no respondieron a nada en esos 90 días**: 77.6 M mensajes (36 %), 3.6 M MXN (24 % del costo del trimestre), 19 mensajes por usuario, 0.37 % de conversión y 1.9 % de baja. Solo se les entrega 42 % de sus WhatsApp.
- Sumando los canales mudos de quienes sí responden a algo, **152.9 M mensajes (71 %) del trimestre fueron a alguien que no respondió por ese canal en 90 días**, por 6.7 M MXN (46 % del costo). Quitando a los que no responden a nada: 75.3 M mensajes y 3.1 M MXN por trimestre.
- 2.45 M usuarios responden por otro canal pero no hicieron clic en ningún email en 90 días, y recibieron 43.7 M emails (2.2 M MXN). 0.96 M WhatsApp entregados (1.5 M enviados) fueron a quien no leyó ninguno en 90 días.
- Quien responde solo a email convierte 7.1 % y se da de baja 10.2 %; quien responde a email, WhatsApp e in-app convierte 49 %; quien responde a los cuatro canales 65 %. La relación es la misma que en nueve meses.

| Responde a (90 días) | Usuarios | % usuarios | % msgs | % costo | Msgs por usuario | Convierten | Baja email | Msgs a canal mudo | WhatsApp entregado |
|---|---|---|---|---|---|---|---|---|---|
| ninguno | 4.10 M | 57.9 % | 35.9 % | 24.4 % | 19 | 0.37 % | 1.9 % | 77.6 M | 42 % |
| in-app | 867 mil | 12.3 % | 9.8 % | 6.1 % | 24 | 6.51 % | 0.9 % | 18.8 M | 65 % |
| WhatsApp | 775 mil | 11.0 % | 12.7 % | 29.5 % | 35 | 3.56 % | 1.3 % | 23.4 M | 91 % |
| WhatsApp + in-app | 301 mil | 4.3 % | 8.5 % | 12.5 % | 61 | 32.48 % | 1.2 % | 15.2 M | 91 % |
| push + in-app | 187 mil | 2.7 % | 6.1 % | 3.0 % | 71 | 31.98 % | 0.8 % | 4.3 M | 69 % |
| push + WhatsApp + in-app | 186 mil | 2.6 % | 9.0 % | 8.7 % | 105 | 55.12 % | 0.8 % | 5.5 M | 91 % |
| email | 162 mil | 2.3 % | 1.5 % | 1.2 % | 21 | 7.09 % | 10.2 % | 749 mil | 47 % |
| email + in-app | 105 mil | 1.5 % | 1.8 % | 1.3 % | 37 | 22.89 % | 5.6 % | 1.3 M | 60 % |
| push | 77 mil | 1.1 % | 2.7 % | 1.1 % | 76 | 12.47 % | 0.6 % | 2.1 M | 72 % |
| email + WhatsApp + in-app | 74 mil | 1.0 % | 2.0 % | 3.2 % | 60 | 48.51 % | 4.4 % | 1.3 M | 90 % |
| email + push + WhatsApp + in-app | 65 mil | 0.9 % | 3.3 % | 3.2 % | 111 | 65.41 % | 2.9 % | 0 | 90 % |
| email + push + in-app | 55 mil | 0.8 % | 2.0 % | 1.0 % | 77 | 46.58 % | 3.7 % | 102 mil | 62 % |
| push + WhatsApp | 52 mil | 0.7 % | 2.7 % | 2.4 % | 113 | 32.48 % | 0.7 % | 1.8 M | 92 % |
| email + WhatsApp | 44 mil | 0.6 % | 0.9 % | 1.7 % | 44 | 26.83 % | 7.9 % | 564 mil | 90 % |
| email + push | 12 mil | 0.2 % | 0.5 % | 0.2 % | 79 | 29.72 % | 3.6 % | 60 mil | 64 % |
| email + push + WhatsApp | 11 mil | 0.2 % | 0.6 % | 0.5 % | 113 | 48.95 % | 2.6 % | 74 mil | 92 % |

## Qué hacer con esto

1. **Canal preferido como regla de envío.** En Braze, un atributo por usuario con el último canal al que respondió (clic, toque o lectura) en los últimos 90 días. Las campañas promocionales se mandan por ese canal y no por los demás. Con la ventana de 90 días quita 75 M mensajes y 3.1 M MXN por trimestre (unos 12.5 M MXN al año) a canales mudos de gente que sí responde por otro lado.
2. **Los que no responden a nada en 90 días (4.1 M)**: una secuencia de reactivación corta (3 toques en 30 días, un canal, el más barato que tengan contactable) y si no responden, salen de todo lo promocional. Hoy reciben 36 % de los mensajes del trimestre y producen 0.37 % de conversión.
3. **Limpiar la base de WhatsApp antes de mandar más.** El 34 % de entrega entre quienes nunca responden dice que una parte grande de esos números no existe. Quitar de WhatsApp a quien no tiene entrega en sus últimos 3 envíos ahorra el envío y evita que Meta castigue la calidad del número de la empresa.
4. **Dejar de pagar WhatsApp a quien nunca lo lee** (3.2 M MXN al año en entregados) y dejar de mandar email a quien nunca hace clic (7.5 M MXN al año y menos bajas).
