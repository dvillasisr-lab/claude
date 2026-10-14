# Pendientes y outcomes del entregable final

Lista viva de lo que debe salir en el análisis final (tablero, Excel y deck). Se actualiza conforme llegan datos y decisiones. Estado: pendiente, en curso, listo, bloqueado.

## 1. Serie de tiempo por mes y por semana (las dos vistas)

Todo lo de esta sección se muestra por mes y por semana, por canal y total, para el periodo enero a septiembre 2026.

| # | Outcome | Fuente | Estado | Nota |
|---|---|---|---|---|
| 1.1 | Mix de envíos por canal (volumen y % del total) | E1 (mes), E4 (semana) | Datos listos (E1 y E4a) | |
| 1.2 | Costo variable MXN por canal y total | E1, E4 | Datos listos (E1 y E4a) | Email 0.05, WhatsApp 1.00, push e in-app sin costo variable |
| 1.3 | Entrega: email y WhatsApp (entregados / enviados) | E1, E4 | Datos listos (E1 y E4a) | Push e in-app no tienen evento de entrega |
| 1.4 | Apertura: email (abiertos / entregados) y push (abiertos / enviados) | E1, E4 | Datos listos (E1 y E4a) | |
| 1.5 | Lectura WhatsApp (leídos / entregados) | E1, E4 | Datos listos (E1 y E4a) | |
| 1.6 | Clic: email (clics / entregados), in-app y banner (clics / impresiones) | E1, E4 | Datos listos (E1 y E4a) | Push y WhatsApp no tienen clic en la tabla |
| 1.7b | Días hasta la baja y emails antes de la baja | E8 | Datos listos (versión 3, 88 % de las bajas): mediana 27 días y 5 emails para usuarios nuevos; 33 % se va con el primer email; el envío masivo de BillPay de junio explica 31 % de las bajas de nuevos y el retargeting de registro 22 %. Ver `hallazgos/MUESTRA_L_dias_hasta_baja.md` |
| 1.7 | Bajas de email en tres vistas: parte del mes (% de las bajas del periodo), acumulado sobre la base, y tasa mensual (usuarios con baja / usuarios con email entregado en el mes) | E4a | Listo en el tablero | 457 mil usuarios únicos en 9 meses, 1.09 M eventos. Definición en METRICAS.md sección Bajas |
| 1.8 | Bajas por canal | No existe para push ni WhatsApp | Bloqueado por dato | Solo email tiene campo de baja. Ver METRICAS.md sección Bajas |
| 1.9 | Concentración de mensajes: usuarios y mensajes por banda de mensajes, por mes | E4b | Datos listos | |
| 1.10 | Usuarios con baja que siguen recibiendo mensajes | E5 | Datos listos: 17 % de los que se dan de baja reciben email después (1.27 M emails, 40 % abiertos). E5b recibida: 94 % es cobranza o transaccional; 80 mil emails promocionales en 33 familias, casi todo Marketing. Ver `hallazgos/MUESTRA_E_despues_de_baja.md` | `email_subscribe` no sirve para esto. Se mediría como usuarios con baja en el mes M que reciben email después. Necesita extracción E5 por cohorte de baja. Decidir si vale la pena |

## 2. Lo demás del plan (lentes A a I)

| # | Outcome | Fuente | Estado |
|---|---|---|---|
| 2.1 | Inventario: qué existe, qué está activo, qué no se envía hace 90 días, tipo de comunicación | E2 + E1 | Pendiente, datos listos |
| 2.2 | Ranking de comunicaciones por eficiencia y cuadrantes (volumen vs resultado) | E1 | Muestra lista: `hallazgos/MUESTRA_C_campanas.md` y `muestra_c_familias.csv` |
| 2.2b | Plan de acción por campaña y equipo: familias con señal apagar o rehacer, revisar, proteger, escalar, basada en respuesta y bajas (conversión solo de referencia), con filtros por equipo, canal y tipo | E1 | Muestra lista: página `tablero/muestra_campanas.html` (publicada). 340 familias promocionales a apagar o rehacer, 89 activas en septiembre con 28 M msgs y 3.2 M MXN al mes . Cada familia tiene acción concreta (qué hacer) y justificación (por qué) con `scripts/acciones_campanas.py`, decidida solo con datos (señal, canal, E7c abren vs no abren, E7a), no con el nombre: 50 Apagar, 45 Limpiar base WA, 181 Rehacer, 41 Bajar frecuencia. Ahorro 3.2 M MXN al mes |
| 2.2c | Solapamiento: a qué usuarios les llegan varias comunicaciones parecidas el mismo día, y qué pares de familias coinciden más | E6 | E6 recibida. Muestra en `hallazgos/MUESTRA_F_solapamiento.md`: 9 % de usuario-días con 3+ campañas concentra 24 % de mensajes; 62 % del solape es entre equipos; Canvas QA con 1.87 M envíos |
| 2.2d | Segmentación: a quién le funciona qué (familia × canal × etapa, y patrón de respuesta por usuario) | E7 | E7a recibida: 44 M envíos promocionales a usuarios con tarjeta congelada, REUS/ARCO o lista negra. Ver `hallazgos/MUESTRA_H_etapas_bloqueadas.md`. E7b recibida: 73 % de los usuarios no responde a nada; 59 % de los mensajes van a un canal al que el usuario nunca respondió (25.8 M MXN). Ver `hallazgos/MUESTRA_J_canal_preferido.md` |
| 2.2e | Buenas prácticas con datos propios: qué audiencia, gancho, tamaño e intensidad ayudan o empeoran, y checklist antes de lanzar | E1 + E3 | Muestra lista: `hallazgos/MUESTRA_G_buenas_practicas.md` |
| 2.2f | Abren y convierten vs no abren (método del equipo para decidir si un email aporta) | E7c | E7c recibida: 856 familias × canal con muestra; quienes abren convierten 2 a 3 veces más (mediana); 64 con menos de 1.5 veces. Entra en la regla de acciones. Ver `hallazgos/MUESTRA_K_abren_vs_no_abren.md` |
| 2.3 | Gobernanza: envíos, costo y resultado por equipo y producto, concentración, naming | E1 + E2 | Pendiente, datos listos |
| 2.4 | Presión por usuario: distribución, banda 321+, costo de la presión | E3 | Pendiente, datos listos |
| 2.5 | Costo por conversión y gasto en comunicaciones que no convierten (solo Cash) | E1 | Pendiente, datos listos |
| 2.6 | Recomendaciones priorizadas con impacto en MXN | Síntesis | Pendiente |
| 2.7 | Excel con fórmulas vivas y deck estilo consultoría | Producción | Pendiente |

## 3. Dudas abiertas que bloquean outcomes

| Duda | Bloquea | Qué se necesita |
|---|---|---|
| `email_subscribe` y `push_subscribe` de `_dim_braze_users` | Resuelto: no se usan | La baja se mide con `email_unsubscribe` (usuarios únicos). Push y WhatsApp no tienen estado de suscripción |
| Cobertura del golden record (93 % sin golden) | Cruces por etapa y riesgo | Saber a quién cubre `dim_braze_filters` |
| Costo fijo de Braze ("$7,020/mes, 32,474 créditos") | Costo total por mensaje y por conversión | Pendiente del usuario. En el Sheets final los costos serán celdas de parámetro (email 0.05, WhatsApp 1.00, fijo Braze vacío) para editarlos sin tocar fórmulas |
| Base de cobro de WhatsApp: enviado o entregado | Todo el costo de WhatsApp (55.2 M MXN sobre enviados; 41.0 M sobre entregados) | Pregunta del usuario el 15 oct. Hoy todas las queries cobran por `whatsapp_send`. Meta cobra el mensaje entregado, así que el default debe ser entregado y quedar como parámetro en el Sheets. E1 y E4a ya traen `whatsapp_delivery`; E3, E4b, E7b y E9b solo traen mensajes enviados y costo precalculado: ya tienen versión 2 en `sql/extraccion.sql` con la columna de WhatsApp entregado y sin costo. Pendiente de correr las cuatro. E9b versión 2 además corrige la definición de respuesta en email (clic, igual que E7b; la versión 1 usaba apertura) |

## 4. Extracciones pendientes

| Extracción | Para qué | Tamaño esperado |
|---|---|---|
| E4a (semana y mes × canal) | Recibida, `data/e4a_serie_semana_mes_canal.csv` | 245 filas |
| E4b (mes × banda de mensajes) | Recibida, `data/e4b_concentracion_mes.csv` | 72 filas |
| E5 (cohorte de baja) | Recibida, `data/e5_cohorte_baja.csv`. Denominador recibido 15 oct: 20,137,560 usuarios únicos con email en el periodo (bajas = 2.27 % de la base) | 9 filas |
| E5b (qué comunicaciones llegan después de la baja) | Recibida 14 oct, `data/e5b_comms_despues_baja.csv` | 200 a 500 filas |
| E6a (solapamiento por usuario-día, por mes y banda de familias) | Recibida 14 oct, `data/e6a_solape_dia_mes.csv` | 45 filas |
| E6b (pares de familias que coinciden en el mismo usuario el mismo día) | Recibida 14 oct, `data/e6b_pares_familias.csv` | hasta 1,000 filas |
| E7a (familia × canal × etapa del golden record) | Recibida 14 oct, `data/e7a_familia_canal_etapa.csv` | 10 a 20 mil filas |
| E7b (patrón de respuesta por usuario: a qué canal responde y cuánto se le manda) | Recibida 14 oct, `data/e7b_patron_respuesta.csv` | 16 filas |
| E7c (convierten los que abren vs los que no, por familia y canal) | Recibida 14 oct, `data/e7c_abren_vs_no_abren.csv` | 2,062 filas |
| E8 (días entre el primer email y la baja, emails antes de la baja, familia del día de la baja) | Recibida versión 3 el 15 oct, `data/e8_dias_hasta_baja.csv`. Cubre 400,821 de las 457,376 bajas (88 %). Ver `hallazgos/MUESTRA_L_dias_hasta_baja.md` | 163 filas |
| E9a (abren vs no abren con ventanas de 7, 30, 90 días y fin de periodo) | Recibida 15 oct, `data/e9a_abren_vs_no_abren_ventanas.csv`. Ver sección de ventanas en `hallazgos/MUESTRA_K_abren_vs_no_abren.md` | 1,225 filas |
| E9b (patrón de respuesta por usuario en los últimos 90 días, julio a septiembre) | Recibida 15 oct, `data/e9b_patron_respuesta_90d.csv`. Ver `hallazgos/MUESTRA_J_canal_preferido.md` | 16 filas |

Con E1 a E4 están todos los datos para arrancar la Ola 2 (analistas por lente). Muestras del formato en `hallazgos/MUESTRA_B_canales.md` (canales) y `hallazgos/MUESTRA_C_campanas.md` (campañas y equipos), y del tablero en `tablero/muestra_tablero.html` (publicado en https://claude.ai/code/artifact/81c8ba2e-4305-498c-8c18-6148df86320a).

Periodo decidido: meses enero a septiembre 2026 (los 9 son completos). Semanas: 38 completas del 5 de enero al 27 de septiembre; se excluyen las dos semanas parciales de las orillas.
