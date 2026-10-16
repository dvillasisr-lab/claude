# Notas de la parte 5: VIII Contenido y campañas, IX Malas prácticas, X Buenas prácticas

Scripts reproducibles en `scratchpad/v6parts/p5/` (common.py con clasificadores de tema y etapa por nombre, s64 a s81). Todo con pandas sobre `braze-analysis/data/*.csv` y `hallazgos/muestra_c_familias.csv`. WhatsApp siempre por entregado (0.05 MXN por email enviado, 1 MXN por WhatsApp entregado). Total de control: 667.4 M mensajes y 57.66 M MXN, igual al deck.

Se agregó una lámina nueva (66b, recuperar con medida). La numeración de la parte queda 64 a 83.

## Cifras nuevas y cómo se calcularon

| Lámina | Cifra | Cálculo |
|---|---|---|
| 64 | No responde: 293 M mensajes (44 %), 23.0 M MXN (40 %) | muestra_c, señal "apagar o rehacer", costo recalculado: WhatsApp = envíos por entrega_pct |
| 64 | Promocional que no responde por equipo: Marketing 110 M (40 %), Product Growth 104 M (37 %, 52 % del dinero), Others 33 M, Sales 29 M | igual, tipo promocional o lifecycle (277 M) |
| 64 | Por tema: Tasa 0 68 M, comercios KPay 64 M, referidos 35 M, BillPay 30 M, rescate 18 M (24 % del dinero) | clasificador `tema()` por nombre |
| 64 | Por etapa: leads 94 M, registrados sin crédito 72 M, ex clientes inactivos 39 M (30 % del dinero), Todos 34 M, activos 30 M | clasificador `etapa()` por nombre |
| 64 | 137 M ya no enviaban en septiembre; 89 activas con 27.7 M mensajes y 2.12 M MXN en septiembre | accion_tipo "Confirmar apagado" y E1 mes 9 |
| 65 | Top 10 email: 37.2 % de entregados y 29.9 % de clics; las 7 promocionales que no responden: 28.3 % y 7.0 % | E1 email, clic sobre entregados por campaña |
| 65 | Top 10 push: 25.2 % de volumen, 15.1 % de aperturas, 7 de Marketing | E1 push |
| 66 | Cinco campañas: 9.16 M MXN (40 % de 23.0 M); septiembre 1.03 M de 2.12 M (49 %) | muestra_c y E1 mes 9 |
| 66 | Costo por conversión de referencia email contra WhatsApp en la misma campaña: B0209 29 contra 114 MXN; B0333 121 contra 1,176; B0171 88 contra 263 | E1, costo por canal entre conversiones_filas |
| 66b | Recuperación KPay (B0331, B0332, B0333): conversión 0.67 %, 0.35 %, 0.06 % a 3, 6 y 12 meses; sin oferta 0.60 / 0.27 / 0.048 % contra con oferta 0.66 a 0.75 / 0.34 a 0.37 / 0.054 a 0.070 % | E15, suma de usuarios y convertidos por paso, oferta tomada del nombre del paso |
| 66b | Costo por conversión de WhatsApp por etapa: activos 17 MXN, leads 79, registrados sin crédito 119, ex clientes inactivos 191 | E1, WhatsApp entregado entre conversiones_filas |
| 66b, 70 | Programa de recuperación KPay: 14.9 M mensajes, 3.6 M MXN; push 0.97 %, email 0.16 %, WhatsApp 54 % | E1 y E15 |
| 67 | Top 8 de bajas: 379 mil eventos de 1.09 M (34.6 %); 6 de 8 con clic debajo de 1 % | E1 email_unsubscribe por campaña con 300 mil+ entregados |
| 68 | 33 campañas "responde pero se dan de baja": 35.6 M correos, unas 141 mil bajas, clic 2.15 %; Marketing 22 (77 % de las bajas); 23 a leads | muestra_c motivo "bajas altas"; bajas = bajas por mil por entregados |
| 68 | Mediana de bajas por mil de campañas de email (100 mil+): 1.7 | muestra_c |
| 69 | 308 correos (versiones con 200 mil+ entregados): 155 pasan 0.3 %, 38 llegan a 1.5 %; por tema y tamaño en la lámina | E1 por communication_id |
| 70 | 45 Canvas de más de 20 pasos: 44 de Product Growth; 27 del programa de recuperación KPay más una copia; 8 B0426 NonInterest KPay | E15 |
| 70 | El Canvas de 120 pasos: 40 push, 40 in-app, 30 email, 10 WhatsApp, cuatro semanas, hasta 8 ofertas | E15 |
| 71 | 74 campañas con 5+ versiones nuevas en 2026, 667 versiones, 266 M mensajes; en septiembre 43 campañas con 2+ versiones enviando a la vez (114 versiones) | E2 first_sent 2026 y E1 mes 9 |
| 72 | Inventario: 6,144 guardadas; 3,438 con envío en 2026; 2,120 creadas en 2026; 341 activas en septiembre (de 270 campañas); 186 sin archivar, ninguna sin envío en 90 días; 229 archivadas que enviaron en septiembre; 636 con nombre de prueba, 193 con envío | E2 y E1 |
| 72 | Por canal (año / septiembre): push 1,124 / 179, email 999 / 214, in-app 727 / 123, WhatsApp 601 / 68 | E1 comunicaciones con envíos |
| 72 | Por equipo (año / septiembre): Marketing 745 / 88, Product Growth 574 / 101, Sales 333 / 35, Others 328 / 95, Collections 23 / 22 | E1 |
| 74 | Matriz de 8 prácticas por equipo con mensajes, MXN y peor caso | p5/s74.py (se traslapan, no se suman) |
| 75 | Después de caer debajo del piso: 149 M (22 %), 10.0 M MXN; sin cobranza 138 M y 9.4 M MXN; 47 campañas siguen en septiembre; evitables con salida a dos meses: 93 M y 6.2 M MXN | regla de deck_data.insisten recalculada con WhatsApp por entregado |
| 76 | Recordatorio de registro: email 16.4 M, 65 mil bajas; apertura KPay 30 % a los 5 minutos y 5 a 7 % desde el día 3 | E1 y E15 (Acquisition T2727, T2728) |
| 77 | 163 comunicaciones con nombre de prueba, 6.7 M mensajes: 20 push sin aperturas (4.74 M), 14 envíos reales con nombre de prueba (1.97 M, 218 mil MXN, 19.7 mil conversiones), 129 pruebas chicas (14 mil) | E1, regla por nombre y por respuesta |
| 78 | Con disparador: 71 M (12 %), email 2.62 % contra 0.35 %, push 4.91 % contra 1.00 %, in-app 65 % contra 30 %, WhatsApp 67 % contra 69 %; 57 % de los clics de email | p5/s78.py, disparador por nombre |
| 79 | 150 campañas a ampliar, 3.2 M mensajes, 46 activas; Product Growth 68, Marketing 62 | muestra_c señal "escalar" |
| 80 | Sales: lift mediano 2.38 a 7 días y 1.55 a 90; 26 de 177 con 2+ a 90 días; otros equipos 2.5 a 2.6 a 7 y 1.5 a 1.7 a 90 | E9a, campañas con 1,000+ de cada lado y 100+ conversiones |
| 81 | Push: junio 46.8 M y 1.05 %; septiembre 24.4 M y 2.11 %; aperturas 493 mil y 516 mil; Marketing 26.0 a 9.4 M; Others 9.8 a 1.5; Sales 3.4 a 7.8; 16 campañas continuas 1.65 a 1.95 % | E1 push por mes, equipo y tema |

## Preguntas que no se pueden responder con estos datos

- **¿Quién tiene la app?** (66b, 70, 76): sin app no hay push ni in-app. Falta la extracción E18c (llave de dispositivo).
- **¿El push sin aperturas de QA era silencioso o lo vio el cliente?** (77): hace falta el tipo de mensaje del paso del Canvas (bandera de contenido o push silencioso).
- **¿Cuánto recupera de verdad un programa de recuperación?** (66, 66b): no hay grupo que no reciba nada; las ramas sin oferta solo comparan ofertas.
- **¿Las promociones de Sales venden en KPay?** (80): la conversión de Databricks es solicitud o préstamo, sobre todo de Cash; no trae la compra KPay. Hace falta el evento de compra KPay por usuario y fecha.
- **Bajas por campaña en usuarios únicos** (67, 68): E1 trae eventos. Se necesita la baja por usuario con la campaña del día.
- **Cadencia diaria por persona del recordatorio de registro de KCash** (76): el Canvas B0000 de Marketing no aparece con pasos en E15; "uno o dos al día" se infiere de la mediana de días y correos antes de la baja (E8).
- **Disparador real de cada Canvas** (78, 79): se infiere del nombre. La extracción de la entrada del Canvas (evento o segmento) lo confirmaría.
- **Respuesta a 90 días completa de campañas de agosto y septiembre** (80): la ventana todavía no cierra.

## Contradicciones nuevas o aclaradas

1. **"Mínimo" en la lámina 69 anterior**: decía "38 de 308 pasan el mínimo", pero ese mínimo era 1.5 % de clic y 3 % de apertura, no el piso de 0.3 % y 0.75 % que usa el resto del deck. Con el piso pasan 155 de 308. En la lámina se separan "piso" y "responde bien".
2. **Lectura de WhatsApp de RescateTasa0 (B0171 rezagados)**: 57.7 % en muestra_c (solo lecturas del mes del envío) contra 61.5 % recalculado de E1 (suma lecturas que llegan el mes siguiente, en filas sin envío). Afecta si esa campaña queda debajo o arriba del piso de 60 %. Hay que fijar una regla; en pantalla se dice "cerca de 60 %".
3. **Ahorro de las cinco campañas**: muestra_c (868 mil MXN al mes solo B0171) cobra WhatsApp por enviado. Por entregado, el promedio mensual de B0171 es unos 550 mil y en septiembre 174 mil. Las 89 activas cuestan 2.4 M MXN al mes en promedio de sus meses activos y 2.1 M en septiembre (no 3.2 M).
4. **"Seguir mandando lo que falló"**: 12 M MXN en el deck (WhatsApp por enviado) contra 10.0 M por entregado. "85 campañas debajo del mínimo siguen activas" (Estándares #22) contra 47 que siguen enviando en septiembre con la regla de insisten. Son definiciones distintas.
5. **Pruebas y copias**: 171 comunicaciones y 7.26 M (MUESTRA_F) contra 163 y 6.72 M aquí (otra expresión regular y solo con envío mayor a cero). Además, la mayor parte no son pruebas: 4.7 M son push sin aperturas y 2.0 M envíos reales mal nombrados.
6. **Ventas de Sales a 90 días**: el guion decía "2 a 2.5 veces a 90 días" para Sales. La mediana de Sales es 1.55; solo 26 de 177 campañas mantienen 2 o más, y muchas son de agosto y septiembre con ventana incompleta.
7. **Pasos tardíos**: el guion decía que los pasos tardíos siguen mandando aunque nadie abra. En E15 la apertura de email por posición va de 11 % a 19 % sin caída clara; el problema es el push (275 de los 278 pasos con menos de 1 %), no la posición.
8. **Estado del catálogo**: 229 comunicaciones marcadas como archivadas enviaron en septiembre y 728 tienen último envío en octubre; el estado "archivada" de E2 no sirve para saber si algo sigue vivo.
9. **Top 8 de bajas**: el deck decía 37 %; recalculado con E1 da 34.6 % sobre 1.09 M eventos (el deck usaba otro denominador). Seis de ocho con clic debajo de 1 %, no siete.
10. **Equipo de copias**: las copias ("Copy of Lending...", "Copy of QA-Sales...") quedan con equipo "Copy of ..." y caen en Others, aunque el programa sea de Product Growth o Sales.
