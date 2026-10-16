# Notas de la sección III (equipos), láminas 20 a 31

Scripts en `v6parts/p2work/` (base.py, t1.py a t7.py). Todo se calcula desde `data/*.csv` y `hallazgos/*.csv`. No se modificó nada del repo.

## Cambios de estructura

- Título de sección nuevo: "Los equipos aciertan con quien acaba de actuar y chocan en las bases frías".
- Se agregó una lámina (24) para responder qué provoca la baja. La sección pasa de 11 a 12 láminas: todo lo que sigue se recorre un número (la sección IV empieza en 32).
- Orden nuevo (de lo general a lo particular). Antes y ahora:
  - 20 sigue en 20 (volumen y temas de Marketing y PG).
  - 21 sigue en 21 (ya no es mapa de calor: gráfica de pesas por equipo y tipo de audiencia).
  - 23 pasa a 22 (variación dentro del equipo: en qué temas y canales).
  - 22 pasa a 23 (Marketing pierde nuevos en días, PG base vieja en meses; título igual).
  - nueva 24 (qué provoca la baja).
  - 24 pasa a 25 (dos equipos sobre la misma persona).
  - Fichas 25 a 29 pasan a 26 a 30. Cierre 30 pasa a 31 (sin cambio de fondo).

## Definiciones que usé

- Costo: email 0.05 MXN por enviado (`email_sent`) + WhatsApp 1.00 MXN por entregado (`whatsapp_delivery`), desde E1. Total 57.66 M MXN, cuadra con el deck. No se usa `costo_mxn`.
- Respuesta: clic en email, apertura en push, lectura en WhatsApp, clic en in-app. Piso: 0.3 %, 0.75 %, 60 %, 10 %.
- "Arriba del piso": por campaña (nombre sin fecha) y canal en los nueve meses, con 50 mil o más entregados.
- Conversión de referencia: `conversiones_fraccional` de E1 (préstamo o solicitud de Cash en 7 días, repartida entre los mensajes del día). Solo Cash. Costo por conversión = costo del equipo o campaña / conversiones fraccionales.
- Tema: por regex sobre el nombre (base.py, `TEMAS`): Tasa 0 y rescate de leads, referidos, recordatorio de registro, oferta de crédito e Installments, recuperar inactivos y churn, promociones de comercios KPay, lanzamiento de BillPay y recargas, temporada y concursos, boletín, cobranza, aviso transaccional (tipo del catálogo), pruebas.
- Segmento: por la audiencia del nombre (base.py, `seg_of`). "Con acción reciente" = leads que dejaron el registro a medias, clientes activos y recurrentes, cartera en cobranza, evento transaccional, leads recientes (HotLeads). "Sin acción reciente" = leads, leads fríos (rezagados, anónimos, BDD Marketing), registrados sin crédito (Nuevos_RegistradosPay, NeverActive, MPNeverCash), inactivos y dormants, churn, masivos a 'Todos', sin segmento.
- Equipos: mapeo de deck_data (Lending = Product Growth; B2B = Sales; NewProducts, Shopping, Compliance, CX, Acquisition y QA en Others).

## Cifras nuevas y cómo salen

| Cifra | Valor | Cómo |
|---|---|---|
| Mezcla de temas de Marketing | Tasa 0 32 % del volumen y 51 % del costo; referidos 25 % y 31 %; promociones KPay 25 % y 12 %; recordatorio de registro 7 % y 2.5 % | E1 por equipo y tema (t1.py) |
| Mezcla de temas de PG | Installments y crédito 36 % y 36 %; Tasa 0 25 % y 14 %; inactivos y churn 23 % y 36 %; concursos 16 % y 13 % | ídem |
| Sales | 96 % promociones KPay; Comercio del día 15 %, códigos KUESKI 10 %, Hot Sale 10 %, Amazon 9 % | E1, subtemas por regex |
| Segmentos por equipo | PG: registrados sin crédito 38 %; Marketing: leads 28 % y leads fríos 25 %; Sales: recurrentes 74 % | E1 por audiencia del nombre |
| Parte del volumen arriba del piso según audiencia | con acción reciente 79 %; sin ella 39 % (292 M y 364 M envíos) | t5.py, campaña por canal con 50 mil o más entregados |
| Por equipo, volumen sin acción reciente y su parte arriba del piso | PG 72 % y 29 %; Marketing 68 % y 52 %; Others 44 % y 23 %; Sales 25 % y 25 %; Collections 0 % | ídem |
| Gasto debajo del piso | PG 9.9 M MXN (57 % de su gasto); Marketing 2.9 M (11 %); Sales 1.0 M; Others 1.4 M; Collections 0.6 M | ídem |
| Qué explica la respuesta entre campañas de email | equipo 12 %, segmento 54 %, tema 52 % (push: 14 %, 22 %, 38 %) | varianza explicada del log de respuesta frente al piso, ponderada por entregados, 303 campañas de email |
| Qué explica las bajas entre campañas de email | segmento 49 %, tema 39 %, equipo 26 %, tipo 24 %, veces que llega en el mes 8 %, tamaño 9 %, mes 9 % | t3.py, 866 campaña-mes de email con 20 mil o más entregados; bajas del mismo mes / entregados |
| Bajas por mil por segmento | registro a medias 4.1; leads fríos 3.5; leads 2.4; 'Todos' 2.1; clientes 1.7; registrados sin crédito 1.4; transaccional 0.65; cobranza 0.25 | ídem |
| Bajas por mil por veces que llega la campaña en el mes | 1 vez 2.2; 1 a 2 1.5; 2 a 3 1.7; 3 a 5 1.5; 5 a 8 1.3 | ídem |
| Bajas el día de la baja por tema (E8) | Nuevos: BillPay 30 %, recordatorio de registro 24 %, Tasa 0 17 %. Base vieja: Tasa 0 28 %, referidos 18 %, Installments y crédito 14 % | muestra_l con tema por regex (t4.py); doble conteo por día como en MUESTRA_L |
| Marketing nuevos por tema | recordatorio de registro 34.7 mil de 70 mil; Tasa 0 20.0 mil | ídem |
| Conversión de referencia por equipo | Marketing 0.84 M a 32.5 MXN; PG 0.81 M a 21.3; Sales 0.43 M a 16.6; Collections 0.27 M a 6.0; Others 1.04 M a 4.3 | E1 conversiones fraccionales |
| Costo por conversión por tema | Marketing: Tasa 0 158, referidos 22, recordatorio 14. PG: Installments 12, inactivos 68, Tasa 0 141 | ídem |
| Campañas clave | B0211 email 656 MXN por conversión; B0223 email 2,574 y WhatsApp 6,920; B0171 Rezagada WhatsApp 844; NarrativaTasa0 WhatsApp 694; B0301 email 2.7; Veriff email 21; referidos a clientes KCash email 2.9 | ídem |
| Choques entre equipos | 45 % de los choques promocionales (41.7 de 92.4 M usuario-días) en los mil pares de E6b; Marketing y Sales 14.3 M; Marketing y PG 9.0 M | E6b con tipo del catálogo |
| Tasa 0 doble | B0211 (PG) y B0171 Anónimos (Marketing): 124 mil personas, 0.56 M usuario-días en agosto | E6b |
| Descuento y referidos al mismo dormant | B0209 y B0326 Dormants: 187 mil por email; 171 mil con los dos WhatsApp el mismo día | E6b |
| Mismas promociones KPay en dos equipos | Comercio del día: Marketing 17.7 M, Sales 13.1 M; Amazon 7.8 M y 8.1 M | E1 por subtema |
| Mensajes y bajas por campañas distintas en el día | 1: 1.0 mensajes y 0.36 bajas por mil usuario-días; 3 a 4: 3.6 y 0.42; 8+: 9.9 y 0.70 | E6a |
| Churn de KPay (B0333) | WhatsApp 51.5 % de lectura, 74 % de entrega, 1.71 M MXN; email 0.10 %; push 0.57 %; usuarios por mes: push 31 mil, WhatsApp 56 mil, email 27 mil, in-app 5.5 mil | E1 por canal, promedio mensual de usuarios_aprox |
| Collections | BKT2 a BKT6 por email: 12.1 M a 0.11 a 0.18 %, 4 a 7 correos por persona al mes; BKT1 email 0.41 % contra push 3.11 % | E1 + muestra C |

## Preguntas que no se pueden responder con estos datos

1. Bajas en push y WhatsApp (lámina 24, canal): solo el email registra la baja. Extracción: opt out de push y desinstalación por día, y bloqueos o reportes de WhatsApp por campaña y mes.
2. Qué provoca cada par de campañas que choca (lámina 25): E6b trae usuario-días juntos, no respuesta ni baja por par. Extracción: por par que coincide el mismo día, respuesta, baja y conversión de quien recibió las dos contra quien recibió solo una.
3. Si Marketing, Sales y el churn de KPay venden (láminas 26 a 28): la conversión es solo Cash. Extracción: compra con KPay a 7 y 30 días por usuario y campaña; altas por referido (programa de referidos); pagos de servicios con BillPay.
4. Cuánto es incremental: no hay grupo de control (lámina 83). Todo costo por conversión es referencia.
5. Quién del churn no tiene la app: solo hay promedios por canal; falta la llave de dispositivo (E18c) para cruzar por persona.
6. Resultado de Collections: el pago por canal y etapa no está en Braze; hace falta la tabla de pagos.

## Contradicciones nuevas

1. **Lectura de WhatsApp con o sin lecturas del mes siguiente.** E1 registra lecturas (y algunas entregas) en meses posteriores al envío, en filas con 0 envíos. Con ellas la lectura total es 68.9 % (lo que usa el deck); sin ellas, 65.8 %. Por equipo: PG 60.6 % contra 58.2 %, Marketing 70.7 % contra 67.6 %, Sales 77.7 % contra 73.4 %. La muestra C (señal y acciones) usa la versión sin ellas: 11 campañas de WhatsApp con más de 100 mil envíos cruzan el piso de 60 %. Entre ellas **B0171 Rezagada Rescate Tasa 0 (57.7 % en muestra C, 61.5 % con lecturas tardías)**, la campaña de mayor ahorro del caso de negocio, y **B0209 descuento a inactivos (59.8 % contra 63.4 %)**. Recomiendo fijar una sola regla antes de cerrar la lista de "apagar"; lo más defendible es contar todas las lecturas de lo entregado. Para estas dos, el argumento de recorte sigue en pie por costo por conversión (844 y 297 MXN) y entrega (63 %), no por lectura.
2. **Costo en muestra C por enviado.** `costo_mxn` y `ahorro_mxn_mes` de muestra_c_familias.csv cobran WhatsApp por enviado (B0171 Rezagada: 5.21 M MXN = envíos). Por entregado son 3.29 M. Las cifras de ahorro de las fichas viejas (868 mil MXN al mes) heredan esto.
3. **'BKT1 a BKT3 no refrescan audiencia'** (ficha vieja de Collections): no encontré la fuente en inventarios, muestras ni playbook. Lo quité.
4. **Marketing Tasa 0 'pasa el piso' pero no rinde.** La señal de muestra C marca B0171 como apagar por lectura; con la lectura completa responde, pero cuesta 694 a 844 MXN por conversión de referencia. Conviene decir el porqué correcto (costo por resultado y bajas), no 'no responde'.
5. **Bajas por mil por equipo.** E1 total (con bajas en meses sin entrega): Marketing 5.93, PG 3.15. Solo meses con entrega: Marketing 2.55, PG 1.52. El deck usa la primera; la lámina 24 usa la segunda para comparar campañas y lo dice en la nota.
6. **Choques entre equipos.** Con solo promociones en los mil pares de E6b: 45 %. Se suma a las cifras ya en conflicto (62 % y 46 %).
