# Pendientes y outcomes del entregable final

Lista viva de lo que debe salir en el análisis final (tablero, Excel y deck). Se actualiza conforme llegan datos y decisiones. Estado: pendiente, en curso, listo, bloqueado.

## 1. Serie de tiempo por mes y por semana (las dos vistas)

Todo lo de esta sección se muestra por mes y por semana, por canal y total, para el periodo enero a septiembre 2026.

| # | Outcome | Fuente | Estado | Nota |
|---|---|---|---|---|
| 1.1 | Mix de envíos por canal (volumen y % del total) | E1 (mes), E4 (semana) | Mes listo con E1, semana pendiente de E4 | |
| 1.2 | Costo variable MXN por canal y total | E1, E4 | Igual que 1.1 | Email 0.05, WhatsApp 1.00, push e in-app sin costo variable |
| 1.3 | Entrega: email y WhatsApp (entregados / enviados) | E1, E4 | Igual que 1.1 | Push e in-app no tienen evento de entrega |
| 1.4 | Apertura: email (abiertos / entregados) y push (abiertos / enviados) | E1, E4 | Igual que 1.1 | |
| 1.5 | Lectura WhatsApp (leídos / entregados) | E1, E4 | Igual que 1.1 | |
| 1.6 | Clic: email (clics / entregados), in-app y banner (clics / impresiones) | E1, E4 | Igual que 1.1 | Push y WhatsApp no tienen clic en la tabla |
| 1.7 | Bajas de email: eventos y usuarios únicos por periodo, tasa sobre entregados | E4 | Pendiente de E4 | E1 solo trae eventos, no usuarios únicos. Definición en METRICAS.md sección Bajas |
| 1.8 | Bajas por canal | No existe para push ni WhatsApp | Bloqueado por dato | Solo email tiene campo de baja. Ver METRICAS.md sección Bajas |
| 1.9 | Concentración de mensajes: usuarios y mensajes por banda de mensajes, por mes | E4b | Pendiente de E4b | E3 lo da para los 9 meses juntos, no por mes |
| 1.10 | Usuarios con baja que siguen recibiendo mensajes | E3 (parcial) | Bloqueado por duda | Depende de confirmar qué significa `email_subscribe = false` (mapeo sección 12) |

## 2. Lo demás del plan (lentes A a I)

| # | Outcome | Fuente | Estado |
|---|---|---|---|
| 2.1 | Inventario: qué existe, qué está activo, qué no se envía hace 90 días, tipo de comunicación | E2 + E1 | Pendiente, datos listos |
| 2.2 | Ranking de comunicaciones por eficiencia y cuadrantes (volumen vs resultado) | E1 | Pendiente, datos listos |
| 2.3 | Gobernanza: envíos, costo y resultado por equipo y producto, concentración, naming | E1 + E2 | Pendiente, datos listos |
| 2.4 | Presión por usuario: distribución, banda 321+, costo de la presión | E3 | Pendiente, datos listos |
| 2.5 | Costo por conversión y gasto en comunicaciones que no convierten (solo Cash) | E1 | Pendiente, datos listos |
| 2.6 | Recomendaciones priorizadas con impacto en MXN | Síntesis | Pendiente |
| 2.7 | Excel con fórmulas vivas y deck estilo consultoría | Producción | Pendiente |

## 3. Dudas abiertas que bloquean outcomes

| Duda | Bloquea | Qué se necesita |
|---|---|---|
| Significado de `email_subscribe = false` (89 % de los emails van a usuarios `false`) | 1.10 | Confirmar cómo se construye la columna en `_dim_braze_users` |
| `push_subscribe` es `false` para el 100 % | 1.10 | Buscar el estado real de permiso de push |
| Cobertura del golden record (93 % sin golden) | Cruces por etapa y riesgo | Saber a quién cubre `dim_braze_filters` |

## 4. Extracciones pendientes

| Extracción | Para qué | Tamaño esperado |
|---|---|---|
| E4a (semana y mes × canal) | Sección 1, puntos 1.1 a 1.7 en vista semanal y bajas únicas | Unas 250 filas |
| E4b (mes × banda de mensajes) | Punto 1.9 | Unas 80 filas |

Las dos queries están en `sql/extraccion.sql`. Son ligeras: agregan sobre la misma base que E1 y no traen identificadores de usuario.
