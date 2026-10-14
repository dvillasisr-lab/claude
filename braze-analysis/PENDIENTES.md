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
| 1.7 | Bajas de email en tres vistas: parte del mes (% de las bajas del periodo), acumulado sobre la base, y tasa mensual (usuarios con baja / usuarios con email entregado en el mes) | E4a | Listo en el tablero | 457 mil usuarios únicos en 9 meses, 1.09 M eventos. Definición en METRICAS.md sección Bajas |
| 1.8 | Bajas por canal | No existe para push ni WhatsApp | Bloqueado por dato | Solo email tiene campo de baja. Ver METRICAS.md sección Bajas |
| 1.9 | Concentración de mensajes: usuarios y mensajes por banda de mensajes, por mes | E4b | Datos listos | |
| 1.10 | Usuarios con baja que siguen recibiendo mensajes | E5 | Datos listos: 17 % de los que se dan de baja reciben email después (1.27 M emails, 40 % abiertos). E5b recibida: 94 % es cobranza o transaccional; 80 mil emails promocionales en 33 familias, casi todo Marketing. Ver `hallazgos/MUESTRA_E_despues_de_baja.md` | `email_subscribe` no sirve para esto. Se mediría como usuarios con baja en el mes M que reciben email después. Necesita extracción E5 por cohorte de baja. Decidir si vale la pena |

## 2. Lo demás del plan (lentes A a I)

| # | Outcome | Fuente | Estado |
|---|---|---|---|
| 2.1 | Inventario: qué existe, qué está activo, qué no se envía hace 90 días, tipo de comunicación | E2 + E1 | Pendiente, datos listos |
| 2.2 | Ranking de comunicaciones por eficiencia y cuadrantes (volumen vs resultado) | E1 | Muestra lista: `hallazgos/MUESTRA_C_campanas.md` y `muestra_c_familias.csv` |
| 2.2b | Plan de acción por campaña y equipo: familias con señal apagar o rehacer, revisar, proteger, escalar, basada en respuesta y bajas (conversión solo de referencia), con filtros por equipo, canal y tipo | E1 | Muestra lista: página `tablero/muestra_campanas.html` (publicada). 340 familias promocionales a apagar o rehacer, 89 activas en septiembre con 28 M msgs y 3.2 M MXN al mes . Cada familia tiene acción concreta (qué hacer) y justificación (por qué) con `scripts/acciones_campanas.py`: 42 Apagar, 44 Limpiar base WA, 190 Rehacer, 41 Bajar frecuencia |
| 2.2c | Solapamiento: a qué usuarios les llegan varias comunicaciones parecidas el mismo día, y qué pares de familias coinciden más | E6 | E6 recibida. Muestra en `hallazgos/MUESTRA_F_solapamiento.md`: 9 % de usuario-días con 3+ campañas concentra 24 % de mensajes; 62 % del solape es entre equipos; Canvas QA con 1.87 M envíos |
| 2.2d | Segmentación: a quién le funciona qué (familia × canal × etapa, y patrón de respuesta por usuario) | E7 | E7a recibida: 44 M envíos promocionales a usuarios con tarjeta congelada, REUS/ARCO o lista negra. Ver `hallazgos/MUESTRA_H_etapas_bloqueadas.md`. Falta E7b |
| 2.2e | Buenas prácticas con datos propios: qué audiencia, gancho, tamaño e intensidad ayudan o empeoran, y checklist antes de lanzar | E1 + E3 | Muestra lista: `hallazgos/MUESTRA_G_buenas_practicas.md` |
| 2.2f | Abren y convierten vs no abren (método del equipo para decidir si un email aporta) | E7c | Query escrita, pendiente de correr |
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

## 4. Extracciones pendientes

| Extracción | Para qué | Tamaño esperado |
|---|---|---|
| E4a (semana y mes × canal) | Recibida, `data/e4a_serie_semana_mes_canal.csv` | 245 filas |
| E4b (mes × banda de mensajes) | Recibida, `data/e4b_concentracion_mes.csv` | 72 filas |
| E5 (cohorte de baja) | Recibida, `data/e5_cohorte_baja.csv`. Falta la línea del denominador (usuarios con email en el periodo) | 9 filas |
| E5b (qué comunicaciones llegan después de la baja) | Recibida 14 oct, `data/e5b_comms_despues_baja.csv` | 200 a 500 filas |
| E6a (solapamiento por usuario-día, por mes y banda de familias) | Recibida 14 oct, `data/e6a_solape_dia_mes.csv` | 45 filas |
| E6b (pares de familias que coinciden en el mismo usuario el mismo día) | Recibida 14 oct, `data/e6b_pares_familias.csv` | hasta 1,000 filas |
| E7a (familia × canal × etapa del golden record) | Recibida 14 oct, `data/e7a_familia_canal_etapa.csv` | 10 a 20 mil filas |
| E7b (patrón de respuesta por usuario: a qué canal responde y cuánto se le manda) | Escrita, pendiente de correr | 16 filas |
| E7c (convierten los que abren vs los que no, por familia y canal) | Escrita, pendiente de correr | 1 a 3 mil filas |

Con E1 a E4 están todos los datos para arrancar la Ola 2 (analistas por lente). Muestras del formato en `hallazgos/MUESTRA_B_canales.md` (canales) y `hallazgos/MUESTRA_C_campanas.md` (campañas y equipos), y del tablero en `tablero/muestra_tablero.html` (publicado en https://claude.ai/code/artifact/81c8ba2e-4305-498c-8c18-6148df86320a).

Periodo decidido: meses enero a septiembre 2026 (los 9 son completos). Semanas: 38 completas del 5 de enero al 27 de septiembre; se excluyen las dos semanas parciales de las orillas.
