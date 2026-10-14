# Muestra J. A qué canal responde cada usuario y cuánto le mandamos por los canales a los que no responde (E7b)

Fuente: `data/e7b_patron_respuesta.csv` (16 filas, una por combinación de canales a los que el usuario respondió alguna vez en el periodo). Respondió = abrió un email, abrió un push, leyó un WhatsApp o hizo clic en un in-app, al menos una vez entre enero y septiembre 2026. Canal mudo = el usuario recibió mensajes por ese canal y nunca respondió a ninguno. Resultado en `hallazgos/muestra_j_patron_respuesta.csv`.

## Qué significa "respondió" y "no respondió a nada" (leer antes de usar los números)

- **Respondió a un canal** = en la tabla de Braze hay al menos una fila de ese usuario, en ese canal, con el evento de respuesta prendido. El evento es distinto por canal: email = abrió el correo (`email_open`); push = tocó la notificación (`pn_open`); WhatsApp = el mensaje aparece como leído (`whatsapp_read`); in-app = hizo clic en el mensaje dentro de la app (`in_app_click`). Ver un in-app sin tocarlo no cuenta; recibir un WhatsApp sin que marque leído no cuenta.
- **"Alguna vez" (E7b)** = al menos una vez entre el 1 de enero y el 30 de septiembre de 2026. Basta una sola apertura en nueve meses para contar como "responde a email".
- **"En los últimos 90 días" (E9b)** = lo mismo, pero mirando solo del 1 de julio al 30 de septiembre, y contando solo los mensajes de esos 90 días.
- **No respondió a nada** = recibió al menos un mensaje en el periodo (por cualquier canal) y no tiene ni una sola apertura de email, ni un toque de push, ni un WhatsApp leído, ni un clic en in-app. Ni una. Es el usuario al que le mandamos y nunca dio señal de vida.
- **Canal mudo** = el usuario sí respondió a algún canal, pero a este canal en particular nunca. Ejemplo: alguien que leyó WhatsApps pero jamás abrió un email; para él, el email es canal mudo y cada email que recibe es un mensaje a canal mudo.
- **Lo que no es.** No es "no convirtió" (eso es otra columna). No es "se dio de baja". No es "no le llegó": aquí se cuentan mensajes enviados, le hayan llegado o no.
- **Ruido conocido.** Si el usuario tiene apagadas las confirmaciones de lectura en WhatsApp, o su correo no carga imágenes (el open de email se mide con una imagen), aparece como que no respondió aunque haya leído. Por eso "no respondió a nada" es un techo: el número real de usuarios realmente mudos es algo menor.

## Lo que dice

- **19.5 M usuarios recibieron algo. 14.2 M (73 %) no respondieron a nada en nueve meses.** Se llevaron 24 % de los mensajes (159.5 M) y 18 % del costo (13.1 M MXN), con 0.08 % de conversión y 1.4 % de baja. Son en promedio 11 mensajes por usuario, poco presionados pero muchos.
- **394.4 M mensajes (59 % del total) fueron a un canal al que el usuario nunca respondió**, por 25.8 M MXN (36 % del costo variable). Quitando a los que no responden a nada, quedan 234.9 M mensajes a canales mudos de gente que sí responde por otro lado.
- **149.0 M emails a 3.9 M usuarios que responden a otro canal pero nunca abrieron un email** (7.5 M MXN). Para ellos el email es ruido y hay un canal que sí funciona.
- **5.2 M WhatsApp (5.2 M MXN) a usuarios que responden por otro canal pero nunca leyeron un WhatsApp**, y 80.1 M push a usuarios que nunca abrieron uno.
- **Quienes solo responden a WhatsApp son 8 % de los usuarios y 33 % del costo** (23.8 M MXN): reciben 63 mensajes al año cada uno, de los cuales 58.2 M emails y 20.7 M push que nunca abren.
- **Quien responde a varios canales convierte mucho más**: email + push + WhatsApp + in-app convierte 75 %, in-app solo 8.8 %, WhatsApp solo 2.0 %. No es que los canales conviertan: es que los clientes activos usan la app y por eso ven in-app y convierten. Sirve para segmentar, no para atribuir.
- **La baja de email se concentra en quienes responden a email**: 15.8 % en "solo email" y 13.9 % en "email + WhatsApp", contra 1.4 % en los que no responden. Es lógico (para darse de baja hay que abrir), pero dice que el lector de email que no usa la app es el que más se cansa.

## Tabla

| Responde a | Usuarios | % usuarios | % msgs | % costo | Msgs por usuario | MXN por usuario | Convierten | Baja email | Msgs a canal mudo |
|---|---|---|---|---|---|---|---|---|---|
| ninguno | 14.2 M | 72.9 % | 23.8 % | 18.1 % | 11 | 0.9 | 0.08 % | 1.4 % | 159.5 M |
| WhatsApp | 1.6 M | 8.1 % | 14.9 % | 32.9 % | 63 | 15.0 | 2.03 % | 3.4 % | 79.0 M |
| in-app | 1.1 M | 5.5 % | 6.9 % | 3.8 % | 43 | 2.6 | 8.84 % | 1.7 % | 42.5 M |
| WhatsApp + in-app | 511 mil | 2.6 % | 9.2 % | 10.4 % | 120 | 14.8 | 37.33 % | 2.9 % | 51.5 M |
| push + WhatsApp + in-app | 371 mil | 1.9 % | 12.9 % | 9.4 % | 234 | 18.4 | 62.14 % | 2.1 % | 26.6 M |
| email | 365 mil | 1.9 % | 1.8 % | 1.5 % | 33 | 3.0 | 5.03 % | 15.8 % | 2.4 M |
| push + in-app | 280 mil | 1.4 % | 5.9 % | 2.5 % | 142 | 6.5 | 36.96 % | 1.8 % | 13.5 M |
| email + push + WhatsApp + in-app | 255 mil | 1.3 % | 10.0 % | 7.4 % | 262 | 20.9 | 75.47 % | 5.1 % |  |
| email + WhatsApp + in-app | 228 mil | 1.2 % | 4.5 % | 5.5 % | 134 | 17.4 | 56.13 % | 7.2 % | 8.2 M |
| email + in-app | 205 mil | 1.1 % | 2.4 % | 1.7 % | 78 | 6.0 | 30.33 % | 7.9 % | 5.4 M |
| email + WhatsApp | 169 mil | 0.9 % | 1.8 % | 3.9 % | 73 | 16.8 | 17.13 % | 13.9 % | 1.6 M |
| email + push + in-app | 134 mil | 0.7 % | 3.6 % | 1.6 % | 181 | 8.9 | 57.47 % | 5.5 % | 752 mil |
| push | 58 mil | 0.3 % | 1.0 % | 0.3 % | 111 | 3.3 | 6.13 % | 1.7 % | 1.7 M |
| push + WhatsApp | 36 mil | 0.2 % | 0.9 % | 0.8 % | 173 | 15.2 | 12.81 % | 2.3 % | 1.7 M |
| email + push | 10 mil | 0.1 % | 0.2 % | 0.1 % | 108 | 4.6 | 25.87 % | 7.2 % | 48 mil |
| email + push + WhatsApp | 9 mil | 0.1 % | 0.2 % | 0.2 % | 142 | 13.2 | 34.90 % | 7.6 % | 36 mil |

## Qué hacer con esto

1. **Canal preferido como regla de envío.** En Braze, un atributo por usuario con el último canal al que respondió (open, read o click). Las campañas promocionales se mandan por ese canal y no por los demás. Quita de golpe 234.9 M mensajes al año a canales mudos y 12.7 M MXN de email y WhatsApp.
2. **Los 14.2 M que no responden a nada**: una secuencia de reactivación corta (3 toques en 30 días, un canal) y si no responden, salen de todo lo promocional. Hoy reciben 24 % de los mensajes y producen 0.08 % de conversión.
3. **Dejar de pagar WhatsApp a quien nunca lo lee** (5.2 M MXN al año) y dejar de mandar email a quien nunca lo abre (7.5 M MXN al año y menos bajas).

Límites: "respondió alguna vez" es laxo (un open accidental cuenta). La versión fina sería "respondió en los últimos 90 días", que se puede sacar con la misma query cambiando la ventana.

## Con ventana de 90 días (E9b, julio a septiembre)

Fuente: `data/e9b_patron_respuesta_90d.csv`. Misma lógica, pero solo cuentan las respuestas y los mensajes del 1 de julio al 30 de septiembre.

- 7.07 M usuarios recibieron algo en el trimestre. **3.12 M (44 %) no respondieron a nada en esos 90 días**: 54.8 M mensajes (25 %), 3.8 M MXN (22 % del costo del trimestre), cero conversiones y 1.7 % de baja de email.
- Sumando los canales mudos de quienes sí responden a algo, **111 M mensajes (52 %) del trimestre fueron a alguien que no respondió por ese canal en 90 días**, por 6.9 M MXN. En nueve meses eran 59 %; con ventana corta baja a 52 % porque hay menos tiempo para que un usuario quede "mudo" por casualidad, y aun así es la mitad de todo lo que se manda.
- 1.43 M usuarios responden por otro canal pero no abrieron ningún email en 90 días, y recibieron 17.7 M emails. 2.2 M WhatsApp fueron a quien no leyó ninguno en 90 días (2.2 M MXN).
- Quien responde solo a email convierte 2.4 % y se da de baja 3.7 %; quien responde a email, WhatsApp e in-app convierte 43 %; quien responde a los cuatro canales 63 %. La relación es la misma que en nueve meses: responder a varios canales va con usar la app.

Para la regla de envío, la ventana de 90 días es la buena: "canal preferido" = el canal al que respondió en los últimos 90 días; si no respondió a ninguno en 90 días, entra a reactivación y después sale de lo promocional.
