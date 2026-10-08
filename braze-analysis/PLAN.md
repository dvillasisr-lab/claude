# Auditoría de uso de Braze con agentes y swarms

Plan para analizar qué comunicaciones enviamos por Braze, por qué canal, quién las manda, cuánto recibe cada usuario, si son eficientes, cuánto gastamos y qué cambiar. Nivel de exigencia: entregable de VP de consultoría estratégica. Está pensado para correrse en Claude Code con subagentes en paralelo (Agent tool o Workflow) a partir de tablas exportadas de Braze (Currents, Snowflake Data Share, Segment Extracts o CSVs del dashboard).

Entregables finales: `ENTREGABLE.md` (respuesta ejecutiva), `braze_auditoria.xlsx` (modelo con fórmulas vivas) y `deck/` (presentación estilo McKinsey con títulos de acción). Más una sección "Qué más analizar" con las preguntas que los datos abren y no cierran.

Estándar de calidad que se exige a cada agente:

- **Exhaustivo.** Se revisa cada tabla y cada columna. El Mapeador produce una matriz de cobertura (tabla × lente) y el Crítico rechaza la entrega si una tabla quedó sin usar sin justificación.
- **So what en cada hallazgo.** Cifra, comparación (vs benchmark, vs otro canal, vs otro periodo) e implicación de negocio. Un número solo no es hallazgo.
- **Pirámide.** La respuesta primero, luego los 3 a 5 argumentos, luego la evidencia. Títulos de acción, no descriptivos.
- **Cuantificado en dinero cuando se pueda.** Ingreso incremental, gasto desperdiciado, costo por conversión.
- **Qué más analizar.** Cada analista cierra con 3 a 5 preguntas abiertas que detectó y qué dato haría falta.
- **Fácil de leer.** Frases cortas. Viñetas y tablas, no párrafos. Una idea por línea. Cada término técnico se explica la primera vez. Un documento que necesite leerse dos veces se devuelve.

## 0. Primer paso cuando lleguen las tablas: mapeo y traducción

Antes de analizar nada, se hace esto y se valida contigo:

1. **Inventario de tablas.** Nombre, para qué sirve en una frase, cuántas filas, qué periodo cubre.
2. **Diccionario de columnas.** Por tabla: columna, tipo, qué significa en palabras simples, ejemplo de valor, % de vacíos.
3. **Mapa de uniones.** Qué columna une cada tabla con cuál. Un diagrama simple y una tabla.
4. **Traducción de métricas.** Una tabla por métrica: nombre, de qué tabla sale, qué columnas usa, fórmula en palabras, fórmula en SQL, dudas abiertas. Ejemplo:

| Métrica | Tabla | Columnas | En palabras | SQL | Dudas |
|---|---|---|---|---|---|
| Tasa de apertura email | email_send, email_open | dispatch_id, user_id | Usuarios que abrieron entre usuarios que recibieron | count distinct opens / count distinct delivered | ¿Hay tabla delivery o usamos send menos bounce? |

5. **Lista de lo que no se puede calcular** con estas tablas y qué haría falta.

Salida: `data/mapeo.md`. Hasta que no lo apruebes, los analistas no arrancan. Esto evita que nueve agentes calculen con supuestos distintos.

Archivos de esta carpeta:

- `PLAN.md` (este): objetivo, supuestos, arquitectura del swarm, fases, entregables.
- `METRICAS.md`: definiciones y fórmulas de cada métrica para que todos los agentes calculen igual.
- `PROMPTS.md`: prompts listos para copiar: orquestador, perfilador, analistas por lente, crítico, sintetizador y el prompt de arranque.

---

## 1. Preguntas de negocio que debe responder

1. **Qué enviamos.** Inventario de campañas y Canvas activos, por tipo (transaccional, promocional, lifecycle, operativo), por canal y por frecuencia.
2. **Por qué canal.** Mix de volumen y resultados por email, push, SMS, WhatsApp, in-app, Content Cards y webhooks.
3. **Quién lo manda.** Equipos, owners y convenciones de nombre o tags. Qué tan concentrado está el envío en pocas personas o equipos. Gobernanza.
4. **Si es eficiente.** Apertura, clic, CTOR, conversión, ingreso por envío, bajas, rebotes y spam contra benchmarks por canal. Campañas muertas, redundantes o que dañan la lista.
5. **Cuánta presión le ponemos al usuario.** Mensajes por usuario por semana, solapamiento de campañas el mismo día, fatiga (relación entre frecuencia y bajas).
6. **Cuánto recibe cada quién.** Tabla por usuario: mensajes totales, por canal, por tipo (transaccional, promocional, lifecycle), estado de suscripción global y por grupo, y si sigue recibiendo promocionales estando dado de baja.
7. **Cuánto gastamos.** Costo por canal, por campaña y por equipo. Costo por conversión y por 1,000 envíos. Qué parte del gasto va a campañas que no convierten.
8. **Qué hacer.** Lista priorizada de apagar, consolidar, re-segmentar, cambiar de canal, y reglas de frecuencia.

## 2. Supuestos sobre las tablas (ajustar al recibirlas)

Tablas estándar de Braze Currents / Snowflake que esperamos. Si tus tablas tienen otros nombres, el Perfilador (fase 0) hace el mapeo.

| Grupo | Tablas típicas | Para qué sirve |
|---|---|---|
| Email | `users_messages_email_send`, `_delivery`, `_open`, `_click`, `_bounce`, `_softbounce`, `_markasspam`, `_unsubscribe` | Embudo y salud de email |
| Push | `users_messages_pushnotification_send`, `_open`, `_influencedopen`, `_bounce` | Embudo push |
| SMS / WhatsApp | `users_messages_sms_send`, `_delivery`, `_rejection`, `_shortlinkclick`; `users_messages_whatsapp_send`, `_delivery`, `_read`, `_failure` | Embudo mensajería |
| In-app / Content Cards | `users_messages_inappmessage_impression`, `_click`; `users_messages_contentcard_send`, `_impression`, `_click`, `_dismiss` | Canales in-product |
| Webhook | `users_messages_webhook_send` | Integraciones salientes |
| Conversión | `users_campaigns_conversion`, `users_canvas_conversion`, `users_canvas_entry`, `users_canvas_exit` | Atribución y eficiencia |
| Comportamiento | `users_behaviors_purchase`, `users_behaviors_customevent`, `users_behaviors_app_sessionstart` | Ingreso y actividad |
| Suscripción | `users_behaviors_subscription_globalstatechange`, `users_behaviors_subscriptiongroup_statechange` | Bajas y opt-outs |
| Metadata | export de campañas y Canvas (nombre, tags, teams, canales, schedule, created_at, updated_at, estado) | Inventario y dueños |
| Usuarios | export de usuarios o `users` (external_id, email_subscribe, push_subscribe, grupos de suscripción, país, fecha de alta, atributos) | Vista por usuario y suscripción |
| Costos | tarifas por canal (SMS y WhatsApp por mensaje y país, email por envío si aplica), contrato Braze (MAU, data points), costo de proveedores | Lente de gasto |

Campos clave que unen todo: `campaign_id`, `campaign_name`, `canvas_id`, `canvas_name`, `canvas_step_id`, `message_variation_id`, `dispatch_id`, `send_id`, `user_id` / `external_user_id`, `time`, `app_group_id`.

**Sobre "quién manda".** Braze Currents no trae el autor. El dueño sale de: (a) campo `teams` o `tags` en el export de metadata, (b) convención de nombre (`[CRM] ...`, `growth_...`), (c) el Changelog del admin (quién creó o editó). Si no hay ninguna fuente, el analista de gobernanza lo infiere por nombre y lo marca como inferido.

## 3. Arquitectura del swarm

Un orquestador y cuatro olas. Cada ola arranca cuando la anterior deja su archivo de salida. Los analistas de la ola 2 corren en paralelo porque son independientes.

```
Orquestador
  │
  ├─ Ola 0  Perfilador de datos (1 agente por tabla, en paralelo)
  │          → data/diccionario.md, data/calidad.md
  │
  ├─ Ola 1  Mapeador de esquema (1 agente)
  │          → data/modelo.md  (joins, grano, dimensiones campaign/canvas/canal/owner)
  │          → sql/vistas_base.sql  (vista unificada de envíos y eventos)
  │
  ├─ Ola 2  Analistas por lente (9 agentes en paralelo)
  │          A inventario   B canales   C eficiencia   D gobernanza
  │          E frecuencia   F salud de lista   G audiencias
  │          H vista por usuario y suscripción   I costo y gasto
  │          → hallazgos/A.md ... hallazgos/I.md  (cada cifra con su query)
  │
  ├─ Ola 3  Crítico (1 agente)
  │          → hallazgos/revision.md  (recalcula, cruza totales, baja o sube confianza)
  │
  ├─ Ola 4  Sintetizador (1 agente)
  │          → ENTREGABLE.md  (respuesta ejecutiva, hallazgos, recomendaciones, qué más analizar)
  │          → hallazgos/storyline.md  (guion del deck: título de acción por slide + exhibit)
  │
  └─ Ola 5  Productores (2 agentes en paralelo)
             Excel: braze_auditoria.xlsx con datos crudos agregados y KPIs por fórmula (skill xlsx)
             Deck: deck/ con la skill consulting-deck a partir de storyline.md
```

### Roles y skills sugeridas de la biblioteca

| Rol | Base en la biblioteca | Nota |
|---|---|---|
| Orquestador | general-purpose | Coordina, no analiza. Pasa a cada agente solo su prompt y las rutas. |
| Perfilador | `voltagent/sql-pro` + `voltagent/data-engineer` | Grano, llaves, nulos, rangos de fecha, duplicados. |
| Mapeador | `voltagent/data-engineer` | Modelo estrella: hecho = envío/evento; dims = campaña, canal, owner, fecha, usuario. |
| Analistas A a I | `voltagent/data-analyst`, `voltagent/cohort-analysis`, `marketing/emails`, `marketing/churn-prevention` | Uno por lente. Mismo template de prompt, cambia el lente. |
| Crítico | `voltagent/qa-expert` + `voltagent/business-analyst` | Adversarial: busca errores, dobles conteos, denominadores mal elegidos. |
| Sintetizador | `voltagent/business-analyst` | Pirámide: respuesta primero, evidencia después. Escribe el storyline del deck. |
| Productor Excel | skill `anthropic-skills:xlsx` | Hojas de datos + hojas de KPIs con SUMIFS, COUNTIFS, AVERAGEIFS. Nada pegado como valor si se puede calcular. |
| Productor Deck | skill `consulting-deck` | Un mensaje por slide, exhibit con fuente, títulos de acción. |

Para cargar un agente de voltagent: `library/fetch-source.sh voltagent` y luego leer `/tmp/skill-sources/voltagent/categories/05-data-ai/data-analyst.md` y pasarlo como parte del prompt.

## 4. Fases en detalle

### Ola 0. Perfilado
Por cada tabla: filas, rango de `time`, grano (una fila es un envío, un evento, un usuario), llave primaria candidata, % nulos por columna, cardinalidad de `campaign_id` y `canvas_id`, duplicados de `dispatch_id`/`id`. Salida: diccionario y lista de problemas de calidad con severidad.

### Ola 1. Modelo
Define cómo se unen las tablas, produce la matriz de cobertura tabla × lente, y construye una vista base `v_envios` (una fila por mensaje enviado, con canal, campaña/canvas, owner, fecha) y `v_eventos` (opens, clicks, conversiones, bajas, rebotes, con la llave al envío). Decide y documenta la ventana de atribución (default: la de Braze para conversión; 72 h para clic sobre apertura si no hay dato) y la zona horaria.

### Ola 2. Lentes de análisis
- **A. Inventario.** Qué existe, qué está activo, qué no se envió en 90 días. Clasificación transaccional / promocional / lifecycle / operativo por nombre y comportamiento. Frecuencia de envío (one-shot, recurrente, trigger).
- **B. Canales.** Volumen, costo aproximado si lo hay, embudo por canal, por mes. Canales subutilizados y sobreutilizados.
- **C. Eficiencia.** Ranking de campañas por conversión, ingreso por 1,000 envíos, CTOR, tasa de baja. Cuadrantes: alto volumen y bajo resultado (apagar o rehacer), bajo volumen y alto resultado (escalar). Variantes A/B sin ganador declarado.
- **D. Gobernanza.** Envíos por owner/equipo, concentración (top 3 equipos = % del volumen), campañas sin tag ni owner, naming inconsistente, duplicadas en intención.
- **E. Frecuencia y presión.** Distribución de mensajes por usuario por semana, por canal. % de usuarios sobre el umbral (default 5 por semana). Días con solapamiento de 3 o más campañas. Correlación frecuencia vs baja.
- **F. Salud de lista.** Rebotes duros y suaves, spam, bajas globales vs por grupo de suscripción, tendencia mensual, campañas que más bajas generan por 1,000 envíos.
- **G. Audiencias.** Tamaño de audiencia por campaña, reach único por mes, usuarios que nunca reciben nada, usuarios que reciben todo.
- **H. Vista por usuario y suscripción.** Una fila por usuario con: mensajes recibidos en el periodo, por canal, por tipo (transaccional, promocional, lifecycle), última fecha de envío, estado de suscripción global (opted_in, subscribed, unsubscribed) y por grupo de suscripción, fecha de la baja si existe. Cruces: usuarios dados de baja que siguieron recibiendo promocionales (riesgo legal), usuarios suscritos que no reciben nada, distribución de mensajes por estado. Salida: tabla `usuarios_resumen.csv` completa más el análisis en `H.md`.
- **I. Costo y gasto.** Costo por envío por canal (SMS y WhatsApp por país, email, push casi cero, costo fijo de Braze prorrateado por envío o por MAU). Gasto total por canal, por campaña, por equipo y por mes. Costo por conversión, costo por 1,000 envíos, y % del gasto en campañas del cuadrante "alto volumen y bajo resultado". Si no hay tarifas, usar tarifas de lista del proveedor marcadas como estimación.

### Ola 3. Crítica
El crítico recibe todos los hallazgos y las queries. Recalcula al menos las 10 cifras más importantes, verifica que los totales por canal sumen al total general, detecta dobles conteos (reenvíos, variantes, pasos de Canvas) y asigna confianza alta/media/baja a cada hallazgo. Un hallazgo sin query o sin reproducir se baja a "no verificado".

### Ola 4. Síntesis
Entregable con pirámide: 1 página de respuesta, 8 a 12 hallazgos clave con cifra, comparación e implicación, tabla de recomendaciones con impacto en dinero, esfuerzo y owner propuesto, roadmap de 30, 60 y 90 días, sección "Qué más analizar" consolidada, anexos por lente. Además escribe `storyline.md`: la lista ordenada de slides con título de acción, mensaje, exhibit y fuente.

### Ola 5. Producción
- **Excel `braze_auditoria.xlsx`.** Hojas: `Leeme` (supuestos, periodo, fuentes), `Parametros` (benchmarks, tarifas, umbrales, editables), `Envios` (agregado por campaña × canal × mes × tipo × owner), `Eventos` (opens, clicks, conversiones, bajas, rebotes al mismo grano), `Usuarios` (una fila por usuario, lente H), `Costos` (tarifas y gasto por campaña), `KPI_Campanas`, `KPI_Canales`, `KPI_Owners`, `KPI_Usuarios`, `Cuadrantes`, `Recomendaciones`. Todas las hojas KPI se calculan con fórmulas (SUMIFS, COUNTIFS, AVERAGEIFS, IFERROR, XLOOKUP o INDEX/MATCH) que apuntan a las hojas de datos y a `Parametros`, para que al cambiar una tarifa o un umbral se recalcule todo. Semáforos con formato condicional. Se recalcula con LibreOffice antes de entregar para verificar que no hay errores.
- **Deck.** Con la skill `consulting-deck`: portada, resumen ejecutivo, 1 slide por hallazgo clave con exhibit, recomendaciones con impacto, roadmap, qué más analizar, anexo metodológico. Cada exhibit cita hoja y rango del Excel o la query.

## 5. Reglas de oro para todos los agentes

1. Ninguna cifra sin su query o cálculo reproducible al lado.
2. Denominador siempre explícito (envíos, entregados, usuarios únicos).
3. No inventar columnas. Si falta un dato, decirlo y proponer proxy marcado como tal.
4. Separar transaccional de promocional antes de comparar tasas.
5. Deduplicar por `dispatch_id` + `user_id` en envíos y por `id` de evento en eventos.
6. Cada hallazgo lleva: afirmación, cifra, periodo, query, confianza, implicación.
7. Escribir en español, sin el guion largo "–".

## 6. Entregables

| Archivo | Contenido |
|---|---|
| `data/diccionario.md` | Tablas, columnas, grano, llaves, rangos |
| `data/calidad.md` | Problemas de datos y cómo se trataron |
| `data/modelo.md` + `sql/vistas_base.sql` | Modelo y vistas |
| `hallazgos/A.md` ... `I.md` | Un archivo por lente |
| `hallazgos/usuarios_resumen.csv` | Una fila por usuario: mensajes por canal y tipo, estado de suscripción |
| `hallazgos/costos_por_campana.csv` | Gasto, envíos, conversiones y costo por conversión por campaña |
| `hallazgos/revision.md` | Veredicto del crítico |
| `data/cobertura.md` | Matriz tabla × lente: qué se usó dónde, qué quedó fuera y por qué |
| `ENTREGABLE.md` | Respuesta ejecutiva, hallazgos, recomendaciones, roadmap, qué más analizar |
| `hallazgos/storyline.md` | Guion del deck slide por slide |
| `braze_auditoria.xlsx` | Modelo con datos y KPIs por fórmula |
| `deck/` | Presentación estilo McKinsey (pptx o html según la skill) |

## 7. Cómo correrlo

**Opción simple (Agent tool).** Pegar el prompt de arranque de `PROMPTS.md` en Claude Code. El orquestador lanza la ola 0 en paralelo, espera, y sigue. Costo moderado a alto: 1 perfilador por tabla + 1 + 9 + 1 + 1 + 2 agentes.

**Opción Workflow.** Decir "usa un workflow" para que Claude use el Workflow tool con `parallel` en la ola 0 y la ola 2 y `pipeline` entre olas. Mismo flujo, menos intervención.

**Dónde corren las queries.** Si las tablas están en Snowflake, BigQuery o Supabase, los agentes usan el conector disponible. Si son CSV, los agentes cargan con DuckDB o pandas y escriben SQL sobre DuckDB para que las queries sigan siendo reproducibles.

## 8. Qué necesito de ti para arrancar

1. Las tablas: nombre, columnas y 20 filas de muestra de cada una, o acceso al warehouse, o los CSV.
2. Periodo a analizar (sugerido: últimos 6 meses completos).
3. Fuente de "dueño": tags, teams, changelog o convención de nombres.
4. Lista de campañas transaccionales si ya existe, para no mezclarlas con promocionales.
5. Umbrales que quieras usar si difieren de los defaults de `METRICAS.md`.
6. Ingreso por conversión o ticket promedio si quieres resultados en dinero.
7. Tarifas: costo por SMS y WhatsApp por país, costo del contrato Braze y de proveedores de email, para la lente de gasto.
8. Export de usuarios con estado de suscripción (o la tabla de cambios de suscripción) para la vista por usuario.
