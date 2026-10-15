# Playbook de Braze para Kueski

Versión 4. 15 de octubre de 2026. Documento operativo: sugiere qué mandar, a quién, por qué canal, qué día y cuántas veces. Las sugerencias salen de nueve meses de envíos (enero a septiembre de 2026, 3,439 comunicaciones) y de 18 extracciones de Databricks. No son reglas fijas: cada equipo decide y las ajusta con sus propias pruebas. El análisis que las sostiene está aparte, en el Sheets `braze_auditoria_v4` y en `ANALISIS_BRAZE_KUESKI.md`.

## Cómo usar este documento

- **Vas a mandar algo:** sección 0. Busca tu caso en la tabla y te sugiere canal, día, veces, segmento, exclusiones y control. En la versión web el resolvedor lo arma con cinco respuestas.
- **Vas a crear algo nuevo:** ve a la sección 6 y sigue los 9 pasos. Antes de activar, pasa el checklist de la sección 7.
- **Quieres mejorar algo que ya existe:** busca la pieza en la pestaña Campañas del Sheets, lee su acción y aplica la sección 8.
- **Vas a poner orden en Braze:** secciones 1 (nombres), 2 (a quién no se le escribe) y 3 (cuántas veces). Se configuran una vez.
- **Vas a configurar la cuenta de Braze:** sección 11. Dieciocho ajustes que se hacen una vez y protegen todo lo demás.
- **Quieres ver el dato detrás de una sugerencia:** no está aquí. Está en el Sheets `braze_auditoria_v4` (pestaña Insights) y en el archivo de análisis.
- **Solo tienes cinco minutos:** lee las 12 reglas de abajo y el checklist de la sección 7. Con eso ya no rompes nada.

## Las 12 reglas en una página

1. **Una pieza se llama** `Ticket-Producto-Audiencia-Gancho`. Sin ticket no se activa.
2. **No se le escribe** a lista negra, REUS o ARCO, tarjeta KPay congelada, dados de baja, números de WhatsApp que fallaron 3 veces ni a quien no respondió nada en 90 días.
3. **Máximo 2 toques** de la misma pieza al mes. El segundo solo a quien no abrió el primero.
4. **Máximo 5 mensajes promocionales por semana** por usuario, 2 piezas al día y 1 push al día.
5. **Se manda por el canal al que el usuario responde.** Hoy 59 % de los mensajes van a un canal que el usuario nunca abrió.
6. **WhatsApp solo a quien ya dio señal** (abrió un push, un email o la app) o a clientes activos. Nunca a bases frías.
7. **Nada a toda la base.** Más de 1 millón de usuarios obliga a prueba al 10 % y a un segmento.
8. **Un recordatorio de algo que el usuario empezó** responde 5 a 10 veces más que una oferta nueva. Ese es el gancho principal.
9. **Referidos, lanzamientos y novedades van en in-app**, no por email. En in-app responden 43 a 55 %; por email 0.2 %.
10. **A las 4 semanas se revisa.** Si no llega al mínimo del canal, se apaga o se rehace. Sin discusión.
11. **Toda pieza lleva grupo de control de verdad:** 10 % que no recibe nada, con la opción nativa de Braze. Hoy ninguna lo tiene, así que nadie puede decir cuánto vende Braze.
12. **Un Canvas tiene máximo 8 pasos y el usuario entra una sola vez.** Hoy hay Canvas de inactividad con 120 pasos y 477 pasos que abren menos de 1 %.

---

# 0. Resuélvelo: qué mandar, a quién, por dónde y cuándo

Tablas de consulta. Buscas tu caso y la celda te dice lo que recomiendan los datos. Son sugerencias, no reglas: si tu prueba dice otra cosa, gana tu prueba.

## 0.1 Qué mandar: canal, día y veces

| Qué mandar | Canal | Mejor día | Mejor evitar | Veces | A quién | Control |
|---|---|---|---|---|---|---|
| Recordar algo que empezó (registro, Veriff, solicitud) | Email T1, push T2 | El mismo día o el siguiente. Cualquier día | | 2 en 7 días | Quien dejó el paso hace menos de 30 días | 10 % |
| Bienvenida | Email día 1, luego push e in-app | Lunes a viernes | Sábado y domingo | 1 email al día, 3 la primera semana | Nuevos (menos de 30 días) | 10 % |
| Oferta de crédito (Tasa 0, línea, monto) | Push. WhatsApp solo a quien abrió el push. Email no conviene | Martes a jueves | Lunes. Fin de semana | 2 al mes | Registrados y activos que abrieron un push en 60 días | 10 % |
| Descuento, cupón, cashback, comercio del día (KPay) | Push y WhatsApp. Email no conviene | Push martes a jueves. WhatsApp sábado | Lunes. Dos canales el mismo día | 1 WhatsApp al mes, 1 push al día | Recurrentes de KPay | 10 % |
| Referidos | In-app. Luego push | Cualquier día | Por email | 1 in-app por sesión, 1 push al mes | Activos | 10 % |
| Lanzamiento, novedad, newsletter | In-app | Martes a jueves | Lunes. Mayo, junio, agosto, noviembre. A toda la base | 1 vez | Activos | 10 % |
| Reactivar a un inactivo | Push. WhatsApp solo a quien abrió el push | Martes a jueves | Lunes. Fin de semana si pasa de 100 mil | 3 en 30 días y sale | Inactivos con señal en 90 días. Solo Lending | 10 % |
| Encuesta o aviso legal | In-app. Email una vez | Martes a jueves | | 1 | Quien aplica | No |
| Precobranza y cobranza | Email y push del proceso | Lunes a viernes. Precobranza 3 días antes del vencimiento | Domingo | Según el proceso | El bucket | No |
| Transaccional | El del proceso | Al instante | | 1 por evento | Quien hizo la acción | No |

Empate de canal: in-app, push, email, WhatsApp, en ese orden. Si el usuario respondió a un canal en 90 días, ese canal.

## 0.2 Mejor día para mandar X

Sí = recomendado. No = no recomendado, no prohibido.

| Qué mandar | Lun | Mar | Mié | Jue | Vie | Sáb | Dom |
|---|---|---|---|---|---|---|---|
| Email masivo (más de 100 mil) | No | Sí | Sí | Sí | Sí | No | No |
| Email acotado (menos de 100 mil, a quien respondió en 60 días) | No | Sí | Sí | Sí | Sí | Sí | Sí, el mejor |
| Email a usuarios nuevos | Sí | Sí | Sí | Sí | Sí | No | No |
| Push | Sí | Sí | Sí | Sí | Sí | Sí | Sí |
| WhatsApp a recurrentes | No | No | No | No | No | Sí, el mejor | Solo acotado |
| In-app | Sí | Sí | Sí | Sí | Sí | Sí | Sí |
| Oferta de crédito | No | Sí | Sí | Sí | Sí | No | No |
| Descuento o evento KPay | No | Push | Push | Push | Push | WhatsApp | No |
| Reactivación | No | Sí | Sí | Sí | Sí | Solo chica | Solo chica |
| Lanzamiento in-app | No | Sí | Sí | Sí | Sí | No | No |
| Cobranza | Sí | Sí | Sí | Sí | Sí | Rinde menos | No |

El mejor día de email de cada equipo:

| Equipo | Mejor día | Peor día |
|---|---|---|
| Marketing | Jueves. Sábado y domingo solo acotado | Miércoles |
| Product Growth (Lending) | Miércoles. Sábado y domingo solo acotado | Lunes |
| Sales | No manda email. Push martes a jueves, WhatsApp sábado | Todos |
| Collections | Lunes a viernes | Sábado y domingo |

Hora: no hay dato. Horas de silencio de 21:00 a 9:00 (sección 11). La hora se prueba con A/B.

## 0.3 Qué conviene mandar cada mes

Sí = recomendado. No = mejor esperar a otro mes.

| Mes | Evento | Oferta de crédito | Descuento y evento KPay | Lanzamiento o newsletter | Reactivación | Email masivo | WhatsApp | Pruebas A/B y relanzar |
|---|---|---|---|---|---|---|---|---|
| Enero | Cuesta de enero | Sí, con control | Sí, una por equipo | No | No | Sí, una pieza nueva por audiencia | Sí | No |
| Febrero | | Sí | Sí | Sí | Sí | Sí | Sí, 1 al mes | Sí |
| Marzo | | Sí | Sí | Sí | Sí | Sí | Solo acotado, es el mes más caro | Sí |
| Abril | | Sí | Sí | Sí | No | Sí | No, hasta limpiar la base | Sí |
| Mayo | Hot Sale | Solo acotada | Sí, una por equipo y canal | No | No | No | Solo recurrentes, sábado | No |
| Junio | | No | No | No | No | No | Solo acotado | No |
| Julio | | Sí | Sí | Sí | Sí | Sí | Sí | Sí, es el mes para probar |
| Agosto | Regreso a clases | Solo acotada | Sí, una por equipo y canal | No | No | No | Solo recurrentes, sábado | No |
| Septiembre | | Sí | Sí | Sí | Sí | Sí, sin subir el push | Sí | Sí, preparar Buen Fin |
| Octubre | | Sí | Sí | Sí | Sí | Sí | Sí | Sí |
| Noviembre | Buen Fin | Solo acotada | Sí, una por equipo y canal. Preventa por WhatsApp en sábado | No | No | No | Solo recurrentes, sábado | No |
| Diciembre | | Sí | Sí | No | No | No a bases que no reciben | Sí | No |

Octubre a diciembre no tienen dato de este año; la fila sale del calendario comercial y de las reglas de los otros meses.

Sugerencias según el tipo de mes:

- Mes con evento (enero, mayo, agosto, noviembre): una pieza por equipo y canal, nada a toda la base, ningún lanzamiento.
- Mes después de un evento (junio): se baja el volumen. Solo retargeting, cobranza y transaccional masivo.
- Mes sin evento (febrero, julio, octubre): pruebas A/B y relanzamientos con control.
- Si la entrega de WhatsApp del mes anterior bajó de 75 %: este mes no sube el WhatsApp.
- El push de un mes no sube más de 1.3 veces el promedio de los tres anteriores.

## 0.4 A quién: segmento y antigüedad

| Si quieres llegar a | Segmento | Canal | Veces | Dueño |
|---|---|---|---|---|
| Quien no se registra | `SEG-KCash-Anonimos`, `SEG-KCash-Leads_SinRegistro` | Push e in-app | 2 en 7 días | Marketing |
| Registrado sin crédito o sin Veriff | `SEG-KCash-Registrados_SinSolicitud`, `SEG-KCash-Registrados_FaltaVeriff`, `SEG-KPay-Registrados_FaltaVeriff` | Email y push de retargeting | 2 | Marketing (KCash), Acquisition (KPay) |
| Nuevo (menos de 30 días) | `SEG-KCash-Nuevos_30d`, `SEG-KPay-Nuevos_30d` | Email día 1, luego push e in-app | 1 email al día, 3 la primera semana | Lending, Sales |
| Activo o recurrente | `SEG-KCash-Activos`, `SEG-KCash-Recurrentes`, `SEG-KPay-Recurrentes_90d` | Cualquiera | 5 promocionales a la semana, 1 WhatsApp al mes | Lending, Sales |
| Inactivo, dormant, churn | `SEG-KCash-Inactivos_90a180d`, `SEG-KCash-Dormants_180a360d`, `SEG-KPay-Churn_12m`, `SEG-KCash-NeverActive` | Push con señal. WhatsApp solo detrás del push | 3 en 30 días y sale | Solo Lending |
| En mora | `SEG-KCash-BKT1`, `SEG-KCash-BKT2`, `SEG-KCash-BKT3`, `SEG-KCash-Precobranza` | El del proceso | Según el proceso | Collections |
| Comercio | `SEG-KPayB2B-Comercios_Activos`, `SEG-KPayB2B-Comercios_Inactivos` | Email y WhatsApp | 2 al mes | Sales |
| Toda la base | No existe. Va por in-app | In-app | 1 | CRM aprueba |

Siempre con las 7 exclusiones de la sección 2 (cobranza y transaccional: solo lista negra).

| Lleva en la base | Qué le conviene | Mejor evitar |
|---|---|---|
| Menos de 1 mes | Solo su bienvenida: hasta 3 emails la primera semana y 1 push al día | Masivos. Fin de semana |
| 1 a 6 meses | Retargeting y ofertas con señal. 2 al mes | Más de 1 push al día |
| 6 meses a 1 año | Solo con señal en 90 días. 2 al mes | Reactivaciones de más de 3 toques |
| 1 a 2 años | Solo si respondió en 90 días | Push sin señal |
| Más de 2 años | Push solo a quien abrió un push en 90 días. Email solo transaccional y cobranza | Masivos |

## 0.5 Qué manda cada equipo

| Equipo | Canal | Día | Le funciona | Le conviene evitar |
|---|---|---|---|---|
| Marketing | Email y push de retargeting. In-app para referidos y lanzamientos | Jueves | Retargeting de registro y Veriff. Referidos por in-app | Push a anónimos y leads sin señal. Referidos y lanzamientos por email. 2 emails al día en onboarding. Nada a bases frías |
| Product Growth (Lending) | Push con señal e in-app. Email solo retargeting a activos | Miércoles | Retargeting de Installments. Descuento a inactivos con señal | Tasa 0 por email a registrados. NeverActive por email. Canvas de más de 8 pasos |
| Sales | Push y WhatsApp a recurrentes de KPay | Push martes a jueves. WhatsApp sábado | Quincenas sin intereses, evento del comercio | Email. El mismo evento por dos canales el mismo día. Promoción a tarjetas congeladas |
| Collections | Email y push del proceso | Lunes a viernes | Precobranza 3 días antes del vencimiento, cobranza por bucket | Pruebas a usuarios reales. Piezas sin ticket |
| Others (transaccional, BillPay, Shopping, Compliance) | Transaccional por el del proceso. BillPay y Shopping con las reglas promocionales | Martes a jueves | Confirmaciones y estados de cuenta | BillPay y Shopping a toda la base |

## 0.6 Qué se manda por producto

| Producto | Canal | Audiencia | Sugerencia |
|---|---|---|---|
| KCash | Push con señal, email de retargeting, in-app | Un dueño por audiencia | Una pieza de Tasa 0 por audiencia |
| KPay | Push y WhatsApp | `SEG-KPay-Recurrentes_90d` | Comercio del día y Cuponera: una pieza con catálogo, no una por mes. Nunca a tarjetas congeladas |
| Installments | Email y push de retargeting | Activos | Se escala por segmento |
| BillPay | In-app y push | Activos | Nada a toda la base |
| Ecosistema | In-app | | Nada a Todos sin in-app primero |
| Dos productos | | | Se parte en dos piezas |

---

# 1. Cómo se nombra cada cosa

## 1.1 Piezas (campañas y Canvas)

Cuatro partes separadas por guion:

`Ticket-Producto-Audiencia-Gancho`

```
S0600-KPay-Recurrentes-BuenFin
L0301-KCash-Activos-Retargeting_Installments
C0012-KCash-BKT1-Cobranza
M0610-KCash-Leads_LeftFunnel-Retargeting_Veriff
```

| Parte | Qué va | Lista permitida |
|---|---|---|
| Ticket | Letra del equipo y número del ticket | M Marketing, L Lending (Product Growth), S Sales, C Collections, A Acquisition, P Producto y transaccional, K Compliance y legal |
| Producto | El producto del que habla la pieza | KCash, KPay, KPayB2B, BillPay, Installments, Ecosistema, Kueski (solo corporativo) |
| Audiencia | El segmento maestro (tabla 0.4) | Anonimos, Leads, Registrados, Nuevos, Activos, Recurrentes, Inactivos, Dormants, Churn, Comercios, Todos. Cobranza: BKT1, BKT2, BKT3, Precobranza |
| Gancho | Qué le ofreces o le recuerdas | Tasa0, Descuento, Cupon, Cashback, Referidos, Retargeting, Recordatorio, Bienvenida, Lanzamiento, Newsletter, CrossSell, Encuesta, Informativo, Cobranza, Transaccional, o el nombre del evento: HotSale, BuenFin, CuestaEnero, BackToSchool, DiaMadres |

Reglas:

- **Detalle con guion bajo.** Si necesitas precisar, una palabra después del guion bajo: `Leads_LeftFunnel`, `Retargeting_Veriff`, `BuenFin_Preventa`, `Cobranza_Dia5`.
- **Varias piezas del mismo ticket** se distinguen por el detalle. Si dos quedarían con el mismo nombre, o es la misma pieza (se queda una) o es una versión nueva.
- **Versión nueva:** sufijo `-v2`, `-v3`. Al activar la nueva se archiva la anterior el mismo día. Nunca dos versiones activas.
- **Campañas de un solo canal con el mismo contenido:** canal al final: `C0012-KCash-BKT1-Cobranza_Dia5-WA`. En un Canvas no hace falta, el canal va en el paso.
- **Pruebas:** prefijo `TEST-` y audiencia de prueba (`SEG-Interno-QA`). Se archivan a los 7 días. Nunca a un segmento real.
- **Prohibido:** espacios, acentos, "Copy of", "N/A", "Not Tracked", "Blast", nombres de personas, fechas en el nombre.
- Anota el nombre y el `communication_id` en el ticket.

Ejemplos de hoy y cómo quedarían:

| Hoy | Queda |
|---|---|
| `Marketing-KCash-20260501-B0391-CANVAS-Leads_BDDMarketing-RescateFinesDeSemana-N/A` | `M0391-KCash-Leads-Tasa0_FinDeSemana` |
| `Sales-KPay-20260518-B0493-CANVAS-Recurrentes-HotSaleKUESKIPROMOEnterprise-N/A` | `S0493-KPay-Recurrentes-HotSale` |
| `Copy of Lending-KPay-20260706-B0332 HardInactive` | `L0332-KPay-Inactivos-Descuento-v2` |
| `QA-KPay-20260811-B001 ReminderRegistroTelefono` | `TEST-A0001-KPay-Registrados-Recordatorio_Telefono` (o su nombre real si es producción) |
| `Collections-KCash-T000-CANVAS-BKT1-NA` | `C0012-KCash-BKT1-Cobranza` |

Nota para datos: el parser de Databricks que llena `team`, `product`, `audience`, `offer` y `ticket_number` hay que ajustarlo a este orden (ticket, producto, audiencia, gancho; `team` sale de la letra del ticket; `familia` = nombre sin `-vN` y sin canal). Las piezas viejas se siguen leyendo con el formato anterior.

## 1.2 Pasos de un Canvas

`NN-Canal-Proposito-Toque`

```
01-Email-Oferta-T1
02-Espera-48h
03-Decision-AbrioEmail
04-Push-Recordatorio-T2
05-Salida-SinRespuesta
```

- `NN` es el orden. Canal: Email, Push, WA, InApp, Espera, Decision, Salida.
- `T1`, `T2` es el toque. Máximo T2 en promocional.
- Antes de un paso de WhatsApp siempre hay un paso de Decision: solo pasa quien abrió algo antes.
- Cada paso de email lleva el filtro de suscripción (1.4). Hoy 80 mil emails llegaron a gente dada de baja porque el filtro estaba solo a la entrada.
- Todo Canvas termina en un paso de Salida con el motivo. Si no, el usuario sigue recibiendo pasos aunque ya haya convertido.
- El grupo de control (10 %) se configura con la opción nativa de Braze, no como un camino llamado "Control".
- **Máximo 8 pasos.** Hoy 45 Canvas pasan de 20 pasos y 19 pasan de 50: los de inactividad `ConSinOferta` tienen entre 96 y 120 pasos para 734 mil usuarios. Un Canvas así no se puede leer ni medir. Se parte por audiencia.
- **Re-elegibilidad apagada.** El usuario entra una vez al Canvas. Si tiene que volver a entrar es otra pieza (sección 11).
- **Un paso que abre menos de 1 % con mil o más usuarios se apaga ese mes.** Hoy hay 477 pasos así.

## 1.3 Tags

Los tags no están en Databricks, así que no sabemos cómo se usan hoy. Regla para adelante: cuatro tags obligatorios por pieza, de lista cerrada, en minúsculas.

| Tag | Valores |
|---|---|
| `tipo:` | promocional, lifecycle, transaccional, cobranza, interno |
| `equipo:` | marketing, lending, sales, collections, acquisition, producto, compliance |
| `prod:` | kcash, kpay, billpay, ecosistema, kueski |
| `q:` | trimestre en que se activó: 2026q4, 2027q1 |

Opcional: `gancho:` con el mismo valor que el nombre, y `estado:revision` para lo que está en el Plan_accion. Nadie crea tags fuera de la lista.

## 1.4 Grupos de suscripción

| Grupo | Se puede dar de baja | Quién lo usa |
|---|---|---|
| KCash Promociones | Sí | Marketing, Lending |
| KPay Promociones y comercios | Sí | Sales, Marketing |
| Novedades Kueski | Sí | Producto, Marketing |
| Referidos | Sí | Marketing |
| Encuestas | Sí | CX |
| Avisos de cuenta y pagos | No | Producto |
| Cobranza | No | Collections |

Cada paso de email promocional filtra por su grupo. El pie del email ofrece la baja del grupo y la baja total.

---

# 2. A quién no se le escribe

Siete exclusiones. Se ponen una vez como filtro negativo en todo lo promocional y lifecycle.

| Excluir a | Por qué | Cuánto se manda hoy |
|---|---|---|
| Lista negra | Riesgo | 146 mil envíos promocionales |
| REUS o ARCO | Pidieron no recibir publicidad. Queja potencial ante Condusef. | 249 mil promocionales (57 mil de Shopping, 47 mil de Lending Churn) |
| Tarjeta KPay congelada (para promociones de KPay) | No pueden pagar con KPay | 43.4 M promocionales |
| Dados de baja de email | Siguen recibiendo por el filtro mal puesto | 80 mil emails, 59 mil de Marketing |
| WhatsApp que falló 3 veces seguidas | El número no existe. Se paga y castiga la calidad del número de la empresa | 1 de cada 4 WhatsApp no se entrega: 14.2 M MXN en 9 meses |
| Sin respuesta en 90 días en ningún canal | 36 % de los mensajes, 0.37 % de conversión | 4.1 M usuarios |
| Empleados y cuentas de prueba | | |

Cobranza y transaccional solo excluyen lista negra. Legal decide si cobranza también excluye REUS y ARCO (hoy 61 mil envíos).

Mientras Datos no defina las banderas de contactabilidad del golden dataset, las exclusiones se arman con los eventos de Braze (baja, desinstalación, fallo de WhatsApp) y con `is_blacklist`, `is_reus`, `is_arco` y `cc_freeze`.


---

# 3. Cuántas veces

| Regla | Límite | Por qué |
|---|---|---|
| Misma pieza al mismo usuario en el mes | 2 toques. El segundo solo a quien no abrió | Con 2 toques el clic sube de 0.8 % a 1.8 %. Con 3 o 4 cae a 0.5 % |
| Promocionales por semana (todo junto) | 5 | Las bajas se disparan a partir del sexto mensaje |
| Piezas promocionales distintas al día | 2 | La baja se duplica cuando llegan 3 o más el mismo día |
| Push promocional al día | 1 | Marketing y Sales mandan dos push el mismo día a 1.5 M de usuarios |
| Separación entre promocionales | 24 horas | |
| WhatsApp promocional al mes | 1 | |
| Onboarding (retargeting de registro) | 1 email al día, máximo 3 la primera semana. El resto por push o in-app | Hoy manda 2 al día y causa 22 % de las bajas de usuarios nuevos |
| Usuario nuevo | Una sola secuencia de bienvenida. Nada más hasta que termine | 33 % se da de baja con el primer email. Antes de irse recibe 4 piezas distintas |
| Reactivación de quien no responde | 3 toques en 30 días, un canal, un gancho. Si no responde, fuera | 73 % de los usuarios no respondió nada en 9 meses |
| Push a usuarios con más de 2 años en la base | Solo a quien abrió un push en 90 días | Reciben 91 push en 9 meses (10 al mes) y abren 1.3 %. Un usuario nuevo recibe 13 y abre 3.4 % |

Se configura con el frequency capping de Braze (global por tipo y canal) y con el tope del Canvas.

---

# 4. Por qué canal

## 4.1 Según a quién le escribes

| Audiencia | Canal | No usar | Dato |
|---|---|---|---|
| Nuevos (0 a 30 días) | Email de bienvenida, push, in-app | WhatsApp como primer toque | Responden más que nadie (clic 1.3 %, push 3.2 %) pero se dan de baja más (6.9 por mil). Cuida la frecuencia, no el mensaje |
| Leads y registrados sin crédito | Push, in-app. Email solo para recordar el paso que dejaron | Email masivo, WhatsApp | Email a prospectos: 0.27 % de clic en 167 M envíos. Es el 28 % de todo lo que se manda |
| Activos y recurrentes | Cualquiera. WhatsApp si la pieza vale más de 1 MXN por mensaje. In-app para novedades | | WhatsApp se entrega 82 % y se lee 70 % |
| Fríos (inactivos, dormants, churn) | Push barato primero. WhatsApp solo a quien reaccionó | WhatsApp masivo | Responden la mitad, un tercio de sus WhatsApp no llega y se llevan 23 M MXN del canal |
| Comercios | Email, WhatsApp | | |
| Cobranza | El del proceso | | No aplica frecuencia promocional |

## 4.2 Según qué le dices

| Gancho | Canal | Dato |
|---|---|---|
| Recordar algo que empezó (retargeting) | Email y push | Clic 3.1 % en email, 2.2 % en push. Lo único que funciona bien por email |
| Referidos | In-app, luego push a activos | In-app 43 %. Email 0.2 % |
| Lanzamiento, novedad, newsletter | In-app | In-app 55 %. Email 0.2 % y las bajas más altas (5.6 por mil) |
| Tasa 0 | Push a quien abrió un push en 60 días. WhatsApp solo detrás de esa señal | Email 0.5 %. Quien abre el push convierte 6 a 18 veces más, pero abre menos del 1 % |
| Descuento, cupón, evento (KPay) | Push y WhatsApp a recurrentes | Es lo que le funciona a Sales (78 % de lectura). Email 0.2 % |
| Encuesta, aviso legal | In-app. Email una vez | |
| Transaccional | El del proceso | Clic 2.7 %. No se toca |

Si el usuario ya tiene `canal_preferido_90d`, ese canal manda. Empate: in-app, push, email, WhatsApp, en ese orden (del más barato al más caro).

---

# 5. Qué funciona y qué no, en una tabla

Resumen operativo: solo lo que conviene hacer.

| Dimensión | Funciona | No funciona | Sugerencia |
|---|---|---|---|
| En general | In-app, WhatsApp a quien ya respondió, recordar algo empezado, 2 toques, audiencias de 10 a 100 mil con un criterio | Email masivo a prospectos, push y WhatsApp a bases frías, enviar a toda la base, 3 o más toques, dos equipos sobre la misma gente el mismo día, email masivo en lunes, Canvas de 100 pasos | Antes de agregar un mensaje, quita uno |
| Canal | In-app para lo informativo. Push como canal de señal. WhatsApp a recurrentes. Email para retargeting y transaccional | Email para Tasa 0, referidos y novedades. WhatsApp como primer toque | Tabla 0.1 y mínimos de 5.1 |
| Día | Martes a jueves para email masivo. Sábado para WhatsApp a recurrentes | Lunes masivo. Fin de semana a nuevos o a bases grandes | Tabla 0.2 |
| Mes | Los meses sin evento, para probar y relanzar | Masivos en mayo, junio y agosto. Lanzamientos en el mes de un evento | Tabla 0.3 |
| Tamaño | 10 a 100 mil usuarios (clic 1.2 %) | Más de 1 M (0.16 %) | Más de 1 M obliga a prueba al 10 % |
| Toques | 2 (clic 1.8 %) | 3 o más (0.5 %) | 2 y se acabó |
| Antigüedad | El primer mes, que es cuando responde | Más de 1 año sin señal | Tabla 0.4 |
| Equipo y producto | Cada equipo en su canal: Marketing retargeting, Lending push con señal, Sales push y WhatsApp a recurrentes | Sales por email. Marketing en bases frías. Dos equipos con Tasa 0 al mismo usuario | Tablas 0.5 y 0.6 |
| Pasos del Canvas | 8 o menos, con Decision entre envíos. Push detrás de una señal (abre 6 % contra 2 %) | 100 pasos. Pasos con menos de 1 % | Pasos con 1.2 |
| Control | 10 % nativo de Braze y lectura del lift a 4 semanas | Caminos llamados "Control" y push silencioso | Sin lift nadie defiende una pieza |
| Pruebas | A/B de una variable, misma base, mismo día, 50/50 | Caminos de audiencia presentados como experimento | Una prueba por equipo al mes |

## 5.1 Mínimo por canal

Si a las 4 semanas la pieza está debajo del mínimo, se apaga o se rehace.

| Canal | Hoy | Mínimo para seguir | Funciona | No funciona |
|---|---|---|---|---|
| Email | 0.92 % de clic, 3.1 bajas por mil | 0.3 % de clic, 2.5 bajas por mil | Transaccional, retargeting, nuevos, 2 toques | Tasa 0, referidos, newsletters, bases frías, más de 1 M |
| Push | 1.5 % de apertura | 0.75 % | Cobranza, nuevos, retargeting, recurrentes | Leads, anónimos, fríos, lanzamientos |
| WhatsApp | 74 % de entrega, 69 % de lectura | 80 % de entrega, 60 % de lectura | Activos, recurrentes de KPay | Bases frías, repetir el mismo WhatsApp a los 2 a 6 días |
| In-app | 38 % de clic | 10 % | Casi todo: referidos, lanzamientos, retargeting, onboarding | Ofertas genéricas (14 %) |

- Email: un solo llamado a la acción. El problema no es el asunto (abren 24 %), es que no hay qué hacer adentro.
- Push: primero push, y el resto solo a quien lo abrió. Menos push, más apertura.
- WhatsApp: nunca como primer toque. Es 8 % de los envíos y 77 % del costo.
- In-app: todo lo informativo va ahí primero. Es gratis y es el que más responde.

## 5.2 Cómo saber si una pieza sirve

Por cada pieza se compara cuánto convierten los que abrieron contra los que no, a 7 días. Lo normal es que quien abre convierta 2 a 3 veces más (email 8 % contra 4 %, push 20 % contra 7 %, WhatsApp 6 % contra 3 %).

| Lo que ves | Qué significa | Qué haces |
|---|---|---|
| Quienes abren convierten menos de la mitad de lo normal del canal | No hay a quién acotar | Se apaga |
| Quienes abren convierten igual que quienes no (menos de 1.5 veces) | El mensaje no cambia nada | Se rehace o se apaga |
| Quienes abren convierten mucho más, pero abren pocos | La pieza está bien, la base no | Se acota a quien abrió algo en 60 días |
| El lift contra el grupo de control es cero | La gente iba a comprar igual | Se apaga aunque "convierta" |

Esto se lee en la pestaña Campañas del Sheets (columna señal y acción) y en la sección 8.

---

# 6. Crear algo nuevo en 9 pasos

1. **Qué quieres que pase.** Un evento de conversión (ventana de 7 días) y el tipo: promocional, lifecycle, transaccional o cobranza. El tipo decide qué reglas aplican.
2. **A quién.** Un segmento maestro (tabla 0.4) más un filtro si hace falta. Nunca "Todos" sin filtro de respuesta en 90 días. Revisa en Catálogo que no exista ya una pieza viva con la misma audiencia y gancho: si existe, se mejora esa.
3. **Por qué canal.** Tabla 0.1 (y 4.1, 4.2 si tu caso no está). Si el usuario tiene canal preferido, ese.
4. **Cuántas veces.** Máximo 2 toques al mes, el segundo solo a quien no abrió. Revisa que la audiencia no esté ya en el tope semanal (sección 3).
5. **Cuándo.** Día según la tabla 0.2 y mes según la 0.3. Revisa el calendario único. No en la misma semana que un evento de otro equipo a la misma gente.
6. **Cómo se llama.** Sección 1.1. Pasos con 1.2. Tags con 1.3. Grupo de suscripción en cada paso de email. UTMs con ticket.
7. **Cómo se prueba.** Grupo de control del 10 % (5 % si pasa de 1 M) con la opción nativa de Braze, no con un camino que se llame Control ni con push silencioso. Más de 1 M: primero al 10 % durante 48 horas y lees bajas por mil y respuesta contra el mínimo del canal. 100 mil a 1 M: al 5 %. Si la pieza tiene dos versiones, A/B 50/50 de una sola variable.
8. **Cómo se mide.** A las 4 semanas: respuesta contra el mínimo del canal (5.1), bajas por mil (menos de 2.5), abren contra no abren (5.2), lift contra el control. Aparece sola en el Sheets el mes siguiente.
9. **Cómo termina.** Fecha de revisión en el ticket. Si a las 4 semanas no cumple, se apaga o se rehace. Si cumple, revisión mensual. Sin envíos en 90 días, se archiva.

---

# 7. Checklist antes de activar

Lo firma el dueño del segmento y MarTech. Si falta una, no se activa.

1. Tipo declarado y tag `tipo:` puesto.
2. Ticket con letra de equipo. Nombre con las 4 partes y listas permitidas. Sin "Copy of", "TEST", "N/A", fechas.
3. Audiencia = segmento maestro. Si es "Todos" o más de 1 M: aprobación de CRM y prueba al 10 %.
4. Las 7 exclusiones como filtro negativo.
5. Filtro de suscripción en cada paso de email.
6. Canal y día según la sección 0. WhatsApp solo detrás de una señal y con `EXC-WA_SinEntrega3`.
7. Máximo 2 toques, el segundo con Decision "no abrió". Paso de Salida con motivo.
8. Dentro del tope semanal, diario y de push.
9. Grupo de control del 10 % y evento de conversión a 7 días.
10. Plantilla vigente, UTMs con ticket, un solo llamado a la acción.
11. Calendario revisado: nadie más le manda lo mismo a esa audiencia esa semana.
12. Fecha de revisión a 4 semanas en el ticket y versión anterior archivada.
13. Máximo 8 pasos, re-elegibilidad apagada, salida al convertir, horas de silencio y caducidad del push (sección 11).

---

# 8. Mejorar algo que ya existe

Busca la pieza en la pestaña Campañas del Sheets (una fila por pieza y canal). La columna acción dice qué hacer:

| Acción | Qué significa | Qué haces en Braze |
|---|---|---|
| Apagar | Mucho volumen, poca respuesta, y ni quien abre convierte | Archivar en ese canal. Si en otro canal sí funciona, dejar solo ese acotado a quien abrió en 60 días |
| Confirmar apagado | Debajo del mínimo y ya sin envíos | Confirmar que está archivada, no pausada |
| Bajar frecuencia | Responde, pero se da de baja arriba de 2.5 por mil o manda 3 o más toques | Tope de 2 toques con Decision "no abrió". Quitar pasos 3 en adelante. Filtro de suscripción en cada paso |
| Rehacer o re-segmentar | Poca respuesta pero quien abre sí convierte, o más de 1 M sin criterio | Cambiar al segmento maestro más filtro de señal. Cambiar el gancho si es Tasa 0 o novedades por email. Relanzar como v2 con control |
| Limpiar base de WhatsApp | Entrega debajo de 80 % | Aplicar `EXC-WA_SinEntrega3`. Pausar hasta que una prueba al 5 % pase de 80 % |
| Escalar | Buena respuesta con audiencia chica | Ampliar al siguiente segmento maestro de la misma familia, con control. No tocar el mensaje |
| Proteger | Mucho volumen y buena respuesta | No tocar. Vigilar bajas y toques. Es la referencia para rehacer las demás |
| Seguir igual | Cumple | Revisión mensual |
| No tocar | Transaccional o cobranza | Solo nombre, ticket y una versión activa |

Hoy hay 85 piezas activas debajo del mínimo. El ahorro por acción está en Plan_accion y por equipo en Vista_equipo.

---

# 9. Cada mes

| Semana | Qué | Quién |
|---|---|---|
| 1 | Actualizar las extracciones y generar el Sheets del mes como archivo nuevo | Datos |
| 1 | Leer Estándares: qué indicador se movió y qué equipo lo mueve | CRM |
| 1 | Leer el lift de las piezas que cumplieron 4 semanas con control. Lift cero: se apaga | CRM con cada equipo |
| 1 | Revisar MAU y puntos de datos consumidos contra el contrato de Braze | MarTech |
| 2 | Ejecutar Plan_accion: Apagar, Confirmar apagado y Limpiar WhatsApp se hacen; Rehacer y Bajar frecuencia se asignan con ticket | Cada equipo con MarTech |
| 2 | Limpieza: piezas sin envío en 90 días, versiones duplicadas, pruebas activas, nombres fuera de regla | MarTech |
| 3 | Calendario del mes siguiente: una pieza por equipo, canal y audiencia | Marketing, Lending, Sales con CRM |
| 4 | Piezas nuevas pasan el checklist y se activan con control | Dueños y MarTech |
| Cada trimestre | Revisar segmentos, tags, grupos de suscripción, plantillas. Archivar lo sin uso. Actualizar este playbook | MarTech y CRM |

---

# 10. Glosario

- **Pieza:** una campaña o un Canvas.
- **Familia:** la pieza con todas sus versiones.
- **Respuesta:** clic en email, apertura en push, lectura en WhatsApp, clic en in-app. Abrir un email no cuenta.
- **Toque:** un mensaje de la misma pieza al mismo usuario en el mes.
- **Canal mudo:** canal al que el usuario nunca respondió aunque sí respondió a otro.
- **Base fría:** inactivos, dormants, churn, never active, rezagados.
- **Señal:** el usuario abrió un push, hizo clic en un email o in-app, o leyó un WhatsApp en los últimos 60 a 90 días.
- **Mínimo del canal:** respuesta debajo de la cual una pieza se apaga: email 0.3 %, push 0.75 %, WhatsApp 60 % de lectura, in-app 10 %.
- **Etapa bloqueada:** lista negra, REUS o ARCO, tarjeta KPay congelada.
- **Grupo de control:** el 10 % de la audiencia que no recibe el mensaje, para medir si el mensaje mueve algo.
- **Segmento maestro:** segmento `SEG-` con dueño, que usan todas las piezas de esa audiencia.
- **Lift:** conversión de quien recibió el mensaje menos conversión del grupo de control. Es lo único que dice si el mensaje vende.
- **Camino (Path):** rama de un Canvas por audiencia o por condición. No es una prueba A/B.
- **Re-elegibilidad:** opción de Braze que deja que un usuario vuelva a entrar al mismo Canvas o campaña. Apagada en promocional.
- **Horas de silencio (Quiet Hours):** ventana en la que Braze no manda nada y espera al día siguiente.
- **MAU:** usuarios activos al mes que Braze cobra. Todo usuario que recibe un mensaje cuenta.
- **Puntos de datos:** cada atributo o evento que se escribe en Braze. También se cobran.

---

# 11. Configuración de Braze: lo que se pone una vez

Ajustes de la cuenta y de cada pieza que no dependen del mensaje. Los hace MarTech. Cada uno con el dato de Kueski que lo justifica cuando lo hay.

| Ajuste | Cómo se deja | Por qué |
|---|---|---|
| Horas de silencio | 21:00 a 9:00 hora del usuario en todo lo promocional y lifecycle. Cobranza según lo que marque Legal | No hay hora en Databricks, así que es la única protección contra push nocturnos. Se pide a Datos agregar la hora |
| Frequency capping global | Los topes de la sección 3 cargados en la cuenta: 5 promocionales por semana, 2 piezas al día, 1 push al día, 1 WhatsApp al mes. Transaccional y cobranza fuera del tope | 9 % de los usuario-días reciben 3 o más piezas; son 24 % de los mensajes |
| Grupo de control nativo | 10 % en toda pieza promocional y lifecycle, 5 % si pasa de 1 M. Siempre con el evento de conversión a 7 días | Hoy no hay ninguno |
| Re-elegibilidad | Apagada en lifecycle y en oferta. Encendida solo en transaccional y recordatorios de pago | Es la causa probable de que un usuario reciba la misma pieza 17 a 31 veces |
| Salida del Canvas | Toda pieza sale al ocurrir su evento de conversión, al darse de baja del grupo de suscripción o al cumplir 30 días dentro | Hoy el Canvas sigue mandando después de la conversión |
| Intelligent Timing e Intelligent Channel | Se prueban en 2 piezas por equipo contra control durante un mes. Si ganan, se extienden. No se activan en todo sin prueba | Sin hora en los datos no sabemos la hora buena. La prueba lo dice |
| Caducidad del push (TTL) | 24 horas en promocional, 72 en cobranza | Un push de oferta entregado dos días después se abre como spam y gasta envíos en celulares apagados |
| Permiso de notificaciones | Se pide dentro de la app después de la primera acción de valor, con una pantalla previa in-app que explique para qué | 16.5 M push fueron a usuarios marcados "sin notificaciones" en el golden dataset. El dato hay que confirmarlo, pero el permiso define el canal |
| Centro de preferencias de email | Una página con los 7 grupos de suscripción (1.4) y la baja total. Link en el pie de toda plantilla. Los grupos no promocionales no se pueden apagar | 3.1 bajas por mil. Hoy la única opción del usuario es irse del todo |
| Dominio de email | SPF, DKIM y DMARC en el dominio de envío. Dominio distinto para promocional y transaccional, con lista de supresión compartida | Protege la entrega de lo transaccional (95 %) del volumen promocional |
| Calidad del número de WhatsApp | Un número por tipo (promocional, cobranza). Plantillas con la categoría correcta (marketing o utility). Pausa automática si la calidad baja a "media". `EXC-WA_SinEntrega3` en toda pieza de WhatsApp | 1 de cada 4 WhatsApp no llega y se paga igual (14.2 M MXN). Un número castigado baja el tope diario de Meta |
| Liquid con valor por defecto | Todo campo personalizado con `default`. Prueba con un usuario sin datos antes de activar | Evita "Hola null". Prevención: no tenemos la cifra |
| Prioridad de in-app | Una sola in-app por sesión. Orden: transaccional, cobranza, onboarding, promocional | In-app es el canal que mejor responde (38 %). Varias a la vez se tapan |
| Catálogos | Comercios, cupones y ofertas en Catálogos de Braze. Una pieza que lee del catálogo, no una pieza por comercio ni por mes | Comercio del día y Cuponera tienen 11 y 8 segmentos distintos solo por el mes |
| MAU y puntos de datos | Revisar cada mes contra el contrato. Los atributos que cambian a cada rato (saldo, último login) se escriben una vez al día, no en cada evento | El costo fijo de Braze depende de ambos. Los 4.1 M usuarios sin respuesta en 90 días también cuentan como MAU si reciben algo |
| Currents a Databricks | Agregar a la tabla de comunicaciones: hora del envío, `device_id` y `platform`, rebote y queja de spam de email, rebote de push, fallo de WhatsApp | Hoy no se puede medir hora, celular ni rebotes. La llave de dispositivo ya existe en `braze.int_communications_joined` |
| Roles y permisos | Editor crea pero no activa. Aprobador (dueño del segmento y MarTech) activa. Admin solo MarTech. Nadie activa lo que creó | 171 pruebas y copias llegaron a usuarios reales (7.26 M envíos) |
| Nombre y tags obligatorios | Las reglas de la sección 1. Pieza sin ticket o sin tag `tipo:` no se aprueba | 749 piezas sin ticket. Los tags no llegan a Databricks |

