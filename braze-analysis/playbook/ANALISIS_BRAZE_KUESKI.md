# Análisis de Braze para Kueski

Material que salió del playbook (versión 4, 15 de octubre de 2026) para dejarlo operativo. Aquí queda el análisis, las cifras de apoyo y las secciones de referencia. El Sheets `braze_auditoria_v4` tiene las mismas cifras con fórmulas vivas.

Contenido: plantilla de Canvas, diagnóstico de segmentos, plantillas, atributos, UTMs y permisos, limpieza pendiente, gobierno, cifras de apoyo (Anexo A), dónde está cada cosa en el Sheets (Anexo B), lo que no sabemos (Anexo C), supuestos (Anexo D) y evidencia (Anexo E).

---

# Cómo se arma el Canvas

Plantilla sugerida de 8 pasos. Se quita lo que no aplique.

```
01-Email-Oferta-T1          (o Push, según la tabla 0.1)
02-Espera-48h
03-Decision-AbrioT1
04-Push-Recordatorio-T2     (solo a quien no abrió)
05-Espera-72h
06-Decision-Senal           (abrió algo: sigue; no abrió: sale)
07-WA-Oferta-T2             (opcional, solo si la pieza vale más de 1 MXN)
08-Salida-Motivo
```

- Control del 10 % con la opción nativa de Braze en la entrada (5 % si pasa de 1 M).
- Re-elegibilidad apagada. Salida al convertir, al darse de baja o a los 30 días.
- Filtro de suscripción en cada paso de email. Horas de silencio y caducidad del push de 24 horas (sección 11).
- Máximo 2 toques por canal. Un paso con menos de 1 % de apertura en mil usuarios se apaga ese mes.

---

# Segmentos: pocos, con dueño

Hoy la audiencia se escribe de 731 formas distintas y dos equipos trabajan la misma base con ofertas distintas (Lending y Marketing sobre inactivos; Lending y Marketing con Tasa 0 al mismo usuario el mismo día).

Lo que Braze registra hoy en las comunicaciones (campos `segment`, `subsegment` y `group`): 41 valores de segmento, 330 de subsegmento y 62 de grupo, que forman 481 combinaciones. El 13 % de los envíos (84.7 M) trae segmento "Not Tracked" y el 25 % trae grupo "Not Tracked". El subsegmento se usa como nombre de la oferta (`Tasa0`, `ComerciodeldiaAbril`, `CuponeraDescuentosJunio`), no como audiencia. Lo mismo escrito de varias formas:

| Hoy | Queda |
|---|---|
| `SoftInactive_3MesesInactividad` y `Softnactive_3MesesInactividad` | Un solo valor, sin error de dedo |
| `Todos` y `Todos_Eligibles` | `Todos`. La elegibilidad es un filtro, no un segmento |
| `Comerciodeldia`, `ComercioDelDia`, `Comerciodeldía`, `ComerciodeldiaAbril` a `Septiembre`, `ComerciodelDíaSept` (11 valores) | Es un gancho, no una audiencia: va en el nombre de la pieza como `ComercioDelDia`. El mes no va en ningún lado |
| `CuponeraDescuentos<Mes>` (8 valores) | `Cuponera`, igual que arriba |
| Amazon (unos 20 valores) | `Amazon` con un detalle por guion bajo |
| `KUESKINUEVO25`, `KUESKINUEVO30`, `KUESKINUEVO40` | `KueskiNuevo`. El monto va en la pieza |
| Grupo `In`, `in`, `InApp`, `inApp` | `InApp` |
| `Variant 1` y `Variante 1` | `Variant 1` |

Los segmentos que de verdad usa la gente son pocos y se leen bien: Leads (201 M envíos, 8.5 % de respuesta), Recurrent (189 M, 7.0 %, el que más convierte en volumen), New (67 M, 2.1 %), Active (15 M, 21 % de respuesta), Precobranza (12 M, 45 conversiones por mil). Product Growth usa 18 nombres de segmento, Others 13, Collections 11, Marketing 7 y Sales 4.

Nombre: `SEG-Producto-Audiencia_Detalle`. Máximo 30 segmentos maestros en total.

| Familia | Segmentos | Dueño |
|---|---|---|
| Embudo de registro | `SEG-KCash-Anonimos`, `SEG-KCash-Leads_SinRegistro`, `SEG-KCash-Registrados_SinSolicitud`, `SEG-KCash-Registrados_FaltaVeriff`, `SEG-KPay-Registrados_FaltaVeriff` | Marketing (KCash), Acquisition (KPay) |
| Nuevos | `SEG-KCash-Nuevos_30d`, `SEG-KPay-Nuevos_30d` | Lending, Sales |
| Activos | `SEG-KCash-Activos`, `SEG-KCash-Recurrentes`, `SEG-KPay-Recurrentes_90d` | Lending, Sales |
| Fríos | `SEG-KCash-Inactivos_90a180d`, `SEG-KCash-Dormants_180a360d`, `SEG-KPay-Churn_12m`, `SEG-KCash-NeverActive` | Solo Lending. Marketing no crea segmentos fríos. |
| Cobranza | `SEG-KCash-BKT1`, `SEG-KCash-BKT2`, `SEG-KCash-BKT3`, `SEG-KCash-Precobranza` | Collections |
| Comercios | `SEG-KPayB2B-Comercios_Activos`, `SEG-KPayB2B-Comercios_Inactivos` | Sales |
| Exclusión | `EXC-Blacklist`, `EXC-REUS_ARCO`, `EXC-KPay_CCFreeze`, `EXC-BajaEmail`, `EXC-WA_SinEntrega3`, `EXC-SinRespuesta90d`, `EXC-Empleados` | MarTech (con Legal y Riesgo) |
| Interno | `SEG-Interno-QA` | MarTech |

Reglas:

- Las piezas usan el segmento maestro y afinan con un filtro adentro del Canvas ("y abrió un push en 60 días"). No se crea un segmento por campaña.
- Un segmento nuevo se pide en el ticket y lo aprueba el dueño de la familia.
- Cada trimestre se archivan los segmentos sin uso en 90 días.

---

# Lo demás

- **Plantillas:** `TPL-Canal-Uso-vN` (`TPL-Email-Promo-v3`). Bloques compartidos para encabezado y pie legal. Nadie edita el pie dentro de una campaña.
- **Atributos de usuario que hacen falta:** `canal_preferido_90d` (último canal al que respondió), `ultima_respuesta`, `wa_fallos_seguidos`, `etapa_golden`, `producto_activo`, `fecha_alta`. En minúsculas con guion bajo.
- **Evento de conversión:** uno por pieza, ventana de 7 días. Lending: `solicitud_enviada`. KPay: `compra_kpay`. Embudo: el siguiente paso. Cobranza: `pago_recibido`.
- **UTMs:** `utm_source=braze`, `utm_medium=email|push|whatsapp|inapp`, `utm_campaign=<ticket>`, `utm_content=<paso>`.
- **Archivo:** sin envíos en 90 días se archiva. Una sola versión activa por pieza.
- **Permisos:** activar a un segmento real lo hace el dueño del segmento más MarTech. Más de 1 M de usuarios o "Todos": también CRM. Exclusiones: MarTech con Legal o Riesgo.

# Limpieza que hay que hacer hoy

| Qué | Cuánto |
|---|---|
| Piezas activas duplicadas (mismo equipo, producto, audiencia y gancho) | 109 piezas en 13 combinaciones. Se queda una por combinación. |
| Piezas con 10 o más versiones | 15 familias. Se consolidan en una. |
| Pruebas y copias que mandan a usuarios reales | 171 comunicaciones, 7.26 M envíos. Se pausan hoy. La más grande: `QA-KPay-B001 ReminderRegistroTelefono`, 1.87 M push con 0.01 % de apertura. |
| Dos versiones del email de desembolso activas | 20240821 y 20251110 llegan juntas a 600 mil usuarios. Se apaga la de 2024. |
| Piezas sin ticket | 749. Others solo tiene ticket en 49 % de sus envíos. |
| Collections con ticket T000 en todo | Un ticket C por bucket. |
| Segmentos con el mismo significado escrito distinto | 41 segmentos, 330 subsegmentos, 62 grupos. Se dejan 30 maestros (ver Segmentos) y el mes sale del nombre. |
| Canvas con más de 20 pasos | 45 Canvas (19 con más de 50). Se parten por audiencia y se recortan a 8 pasos. |
| Pasos con menos de 1 % de apertura en mil o más usuarios | 477 pasos. 80 tienen más de 10 mil usuarios y menos de 0.5 %. Se apagan. |
| Canvas `ControlGroupSplit` (push silencioso para simular control) | 4 Canvas de KPay, 650 mil usuarios. Se sustituyen por el grupo de control nativo. |
| Mensajes a quien nunca respondió en 9 meses | 97.5 M envíos y 8.1 M MXN (900 mil al mes). Entra la exclusión `EXC-SinRespuesta90d`. |

---

# Gobierno


- **Dueños.** Un dueño por familia de segmentos. Un dueño por pieza (el ticket). MarTech es dueño de nombres, tags, suscripciones, plantillas, exclusiones y frequency cap. CRM es dueño del calendario y de los estándares.
- **Calendario único.** Una vista compartida con fecha, equipo, pieza, audiencia, canal, gancho y tamaño. Nada promocional se activa sin estar ahí.
- **Comité quincenal de 30 minutos.** Conflictos de calendario, piezas a Todos, cambios a exclusiones, y piezas en Apagar que un equipo quiera defender (con grupo de control, no con opinión).
- **Excepciones** se piden en el ticket, se aprueban en el comité y tienen fecha de fin.
- Un indicador en rojo dos meses seguidos abre un ticket al equipo que lo mueve.

---

# Anexo A. Cifras de apoyo

## A1. Estándares de hoy (Estándares del Sheets)

| Indicador | Hoy | Estándar | Estado |
|---|---|---|---|
| Entrega de email | 95.1 % | 95 % | Cumple |
| Apertura de email | 23.6 % | 15 a 25 % | Cumple (no decidir con ella) |
| Clic de email | 0.92 % | 1.5 % | Debajo en los 4 equipos |
| Bajas de email por mil | 3.13 | 2.5 | Debajo |
| Apertura de push | 1.53 % | 3 % | Debajo |
| Entrega de WhatsApp | 74.2 % | 90 % | Debajo |
| Lectura de WhatsApp | 68.8 % | 70 % | Debajo por poco |
| Clic de in-app | 38.2 % | 5 a 20 % | Cumple |
| Toques por pieza y usuario al mes | 1.71 | 2 | Cumple (Collections 3.86) |
| Usuarios con 41 o más mensajes en el periodo | 5.3 % | | Debajo |
| Usuario-días con 3 o más piezas | 9.0 % | 10 % | Cumple, pero es 24 % de los mensajes |
| Mensajes a canal mudo | 58.9 % | | Debajo |
| Usuarios que nunca respondieron | 72.9 % | | Debajo |
| Promocional a etapas bloqueadas | 43.78 M | 0 | Debajo |
| Promocional a dados de baja | 79,994 | 0 | Debajo |
| Piezas activas debajo del mínimo | 85 | 0 | Debajo |
| Envíos con ticket | 87.4 % | 100 % | Debajo (Others 48.7 %) |
| Canvas con grupo de control real | 0 de 3,228 | Todos los promocionales | Debajo |
| Pruebas A/B de mensaje en 9 meses | 0 | 1 por equipo al mes | Debajo |
| Mensajes a quien nunca respondió | 14.6 % (8.1 M MXN) | 0 | Debajo |
| Canvas con más de 8 pasos | 45 con más de 20 | 0 | Debajo |
| Pasos con menos de 1 % de apertura (mil o más usuarios) | 477 | 0 | Debajo |
| Email en lunes | 19 % del volumen, 0.65 % de clic | Repartir martes a jueves | Debajo |

## A2. Por equipo

| Equipo | Familias | Envíos | % envíos | Costo MXN | % costo | Email clic | Bajas por mil | Push | WA entrega | WA lectura | In-app | Ahorro al mes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Marketing | 368 | 262.3 M | 39 % | 27.2 M | 47 % | 0.93 % | 4.95 | 1.09 % | 74 % | 71 % | 34 % | 160,647 |
| Product Growth | 184 | 177.2 M | 27 % | 17.3 M | 30 % | 0.45 % | 3.02 | 2.10 % | 72 % | 61 % | 46 % | 1,296,806 |
| Sales | 205 | 85.3 M | 13 % | 7.1 M | 12 % | 0.21 % | 3.71 | 1.23 % | 80 % | 78 % | 8 % | 102,271 |
| Collections | 23 | 44.7 M | 7 % | 1.6 M | 3 % | 1.09 % | 0.25 | 3.61 % | | | 13 % | 0 |
| Others | 283 | 98.0 M | 15 % | 4.4 M | 8 % | 1.83 % | 2.20 | 2.76 % | 71 % | 69 % | 80 % | 38,639 |

## A3. Por mes

| Mes | Envíos | Email clic | Bajas (usuarios) | Push apertura | WhatsApp enviados | WA entrega | WA lectura | In-app clic | Costo MXN |
|---|---|---|---|---|---|---|---|---|---|
| Ene | 58.7 M | 1.20 % | 69,226 | 1.83 % | 5.6 M | 80 % | 75 % | 48 % | 7.4 M |
| Feb | 67.5 M | 0.88 % | 57,965 | 1.43 % | 7.8 M | 77 % | 73 % | 19 % | 9.5 M |
| Mar | 67.8 M | 1.03 % | 50,413 | 1.81 % | 10.4 M | 74 % | 72 % | 24 % | 12.2 M |
| Abr | 64.3 M | 0.98 % | 38,422 | 1.53 % | 5.9 M | 69 % | 66 % | 36 % | 7.6 M |
| May | 85.0 M | 0.86 % | 38,034 | 1.28 % | 6.1 M | 67 % | 67 % | 47 % | 8.1 M |
| Jun | 109.0 M | 0.67 % | 63,425 | 1.05 % | 7.1 M | 74 % | 67 % | 45 % | 9.7 M |
| Jul | 71.7 M | 1.00 % | 52,912 | 1.77 % | 4.8 M | 73 % | 62 % | 37 % | 6.4 M |
| Ago | 78.0 M | 0.95 % | 50,340 | 1.57 % | 4.4 M | 78 % | 64 % | 42 % | 6.1 M |
| Sep | 65.6 M | 0.92 % | 36,639 | 2.12 % | 3.2 M | 77 % | 64 % | 42 % | 5.0 M |

## A4. Por audiencia y por gancho (según el nombre de la pieza)

| Audiencia | Email clic | Bajas por mil | Push | WA lectura | WA entrega | WA costo MXN |
|---|---|---|---|---|---|---|
| Nuevos y onboarding | 1.25 % | 6.9 | 3.18 % | 68 % | 77 % | 0.8 M |
| Activos y recurrentes | 0.72 % | 3.1 | 1.75 % | 70 % | 82 % | 14.9 M |
| Leads y registrados sin crédito | 0.75 % | 4.6 | 0.94 % | 73 % | 75 % | 15.1 M |
| Fríos | 0.35 % | 4.3 | 0.77 % | 65 % | 68 % | 23.0 M |

| Gancho | Email envíos | Email clic | Bajas por mil | Push | WA lectura | In-app clic |
|---|---|---|---|---|---|---|
| Retargeting o recordatorio | 23.6 M | 3.09 % | 3.8 | 2.16 % | 70 % | 58 % |
| Tasa 0 | 54.3 M | 0.53 % | 4.6 | 0.68 % | 69 % | 22 % |
| Descuento, cupón, oferta | 35.0 M | 0.41 % | 3.4 | 1.38 % | 58 % | 14 % |
| Cross sell | 2.7 M | 0.34 % | 2.0 | 1.69 % | 54 % | 25 % |
| Referidos | 40.8 M | 0.22 % | 4.3 | 1.15 % | 71 % | 43 % |
| Lanzamiento, novedades, newsletter | 33.0 M | 0.22 % | 5.6 | 0.82 % | 73 % | 55 % |

## A5. Por etapa del usuario (golden dataset, cubre 37 % de los envíos)

| Etapa | Envíos | Promocional | Email clic (promo) | Push (promo) | In-app (promo) |
|---|---|---|---|---|---|
| Prospectos | 189.1 M | 167.2 M | 0.27 % | 1.33 % | 27 % |
| Tarjeta KPay congelada | 56.6 M | 43.4 M | 0.38 % | 1.45 % | 33 % |
| REUS o ARCO | 0.49 M | 0.25 M | | | |
| Lista negra | 0.43 M | 0.15 M | | | |
| Sin etapa | 416.2 M | 356.3 M | 0.67 % | 1.20 % | 51 % |

## A6. A qué canal responde la gente (9 meses)

| Responde a | Usuarios | % usuarios | % mensajes | % costo | Mensajes por usuario | Convierten | Baja de email |
|---|---|---|---|---|---|---|---|
| Ninguno | 14.2 M | 73 % | 24 % | 14 % | 11 | 0.08 % | 1.4 % |
| Solo WhatsApp | 1.6 M | 8 % | 15 % | 34 % | 63 | 2.0 % | 3.4 % |
| Solo in-app | 1.1 M | 6 % | 7 % | 4 % | 43 | 8.8 % | 1.7 % |
| Solo email | 365 mil | 2 % | 2 % | 1 % | 33 | 5.0 % | 15.8 % |
| Varios canales | 2.2 M | 11 % | 52 % | 47 % | 120 a 262 | 30 a 75 % | 2 a 8 % |

Quien responde a varios canales convierte mucho más porque es cliente activo que usa la app. Sirve para segmentar, no para decir que el mensaje convirtió. Quien solo responde a WhatsApp es 8 % de los usuarios y 34 % del costo, y recibe 58 M emails y 21 M push que nunca abre.

## A7. Las piezas que más pesan hoy

| Pieza (nombre actual) | Canal | Envíos | Respuesta | Acción |
|---|---|---|---|---|
| Lending-KCash-B0211 Nuevos_RegistradosPay Tasa0 | email | 34.9 M | 0.28 % | Apagar |
| NewProducts T0000 Portfolio_BillPay_Intro | email | 16.1 M | 0.11 % | Confirmar apagado |
| Lending-KCash-B0223 Nuevos_NeverActive Installments | email | 13.5 M | 0.10 % | Apagar |
| Marketing-KCash-B0391 Leads RescateFinesDeSemana | push | 13.4 M | 0.76 % | Rehacer o re-segmentar |
| Marketing-KCash-B0000 Leads_LeftFunnel Retargeting_Veriff | email | 9.7 M | 3.04 % | Bajar frecuencia |
| Marketing-KCash-B0171 Anonimos RescateTasa0 | push | 8.9 M | 0.56 % | Apagar |
| Marketing-KCash-B0326 Leads ReferralProgram | email | 8.5 M | 0.23 % | Confirmar apagado |
| Marketing-KCash-B0326 Recurrentes_Dormants ReferralProgram | email | 7.0 M | 0.07 % | Apagar |
| Shopping-KPay-S0004 WeeklyRecommendations | email | 7.0 M | 0.12 % | Rehacer o re-segmentar |
| Sales-KPay-B0335 Recurrentes PromocionesMerchants | email | 6.4 M | 0.22 % | Rehacer o re-segmentar |

Las que hay que proteger: Precobranza (email 4.3 %, push 5.3 %), Retargeting Veriff (push 5.8 %), Retargeting Installments a activos (push 11 %), Payment Confirmation (3.8 %), registro de línea MX in-app (87 %), Quincenas sin intereses (push 4.2 %).

## A8. Por día de la semana (todos los equipos)

| Día | Envíos | % | Email clic | Email bajas por mil | Email conv. por mil | Push | WA entrega | WA lectura | WA conv. por mil |
|---|---|---|---|---|---|---|---|---|---|
| Domingo | 51.2 M | 7.7 % | 1.91 % | 7.7 | 11.8 | 1.26 % | 87 % | 89 % | 56 |
| Lunes | 124.0 M | 18.6 % | 0.65 % | 2.3 | 4.2 | 1.63 % | 72 % | 66 % | 16 |
| Martes | 113.6 M | 17.0 % | 0.82 % | 3.2 | 5.2 | 1.56 % | 75 % | 67 % | 20 |
| Miércoles | 92.2 M | 13.8 % | 1.01 % | 4.1 | 7.1 | 1.63 % | 73 % | 70 % | 16 |
| Jueves | 110.0 M | 16.5 % | 0.95 % | 3.6 | 5.9 | 1.53 % | 75 % | 66 % | 15 |
| Viernes | 111.7 M | 16.7 % | 0.82 % | 2.8 | 5.6 | 1.64 % | 71 % | 70 % | 18 |
| Sábado | 64.7 M | 9.7 % | 1.58 % | 5.5 | 10.5 | 1.44 % | 82 % | 82 % | 34 |

El fin de semana se ve mejor porque salen otras piezas a otra gente, no porque el día ayude. Compara la misma pieza en dos días antes de concluir.

## A9. Segmentos registrados en Braze (campo `segment`)

| Segmento | Envíos | Respuesta | Conversiones por mil | Quién lo usa |
|---|---|---|---|---|
| Leads | 201 M | 8.5 % | 3.5 | Marketing |
| Recurrent | 189 M | 7.0 % | 12.5 | Product Growth, Sales |
| Not Tracked | 84.7 M | | 0 (no se mide) | Others |
| New | 67 M | 2.1 % | 1.3 | Product Growth |
| Todos | 24.5 M | | | Marketing, Others |
| BKT1 | 18 M | 1.5 % | | Collections |
| Active | 15 M | 21 % | 50 | Product Growth |
| Precobranza | 12 M | | 45 | Collections |
| Anonimos | 9.3 M | 0.8 % | | Marketing |

## A10. Mensajes a quien nunca respondió (9 meses)

| Canal | Envíos a quien nunca respondió | % del canal | Costo MXN | Bajas de email |
|---|---|---|---|---|
| Email | 61.4 M | 18.4 % | 3.1 M | 190,737 (17 % de todas) |
| Push | 31.0 M | 12.3 % | 0 | |
| WhatsApp | 5.0 M | 9.1 % | 5.0 M | |
| In-app | 0.1 M | 0.7 % | 0 | |
| Total | 97.5 M | 14.6 % | 8.1 M | |

Sin junio (BillPay) son 1.12 M de usuarios al mes recibiendo email sin haber respondido nunca. Nadie convirtió sin haber respondido antes.

## A11. Embudo por paso del Canvas (usuarios por orden de paso, 959 Canvas)

| Paso | Usuarios | Apertura | Conversión | Email abre | Push abre | WA lee |
|---|---|---|---|---|---|---|
| 1 | 31.5 M | 15.7 % | 0.55 % | 13.8 % | 2.3 % | 44.6 % |
| 2 | 28.6 M | 16.0 % | 1.32 % | 17.3 % | 2.0 % | 44.0 % |
| 3 | 16.7 M | 25.8 % | 1.83 % | 20.1 % | 6.4 % | 39.0 % |
| 4 | 7.0 M | 16.4 % | 2.87 % | 17.3 % | 6.3 % | 52.7 % |
| 5 o más | 6.0 M | 15.7 % | 1.96 % | | | |

El orden es aproximado (fecha de creación del paso). En Canvas con 10 mil o más usuarios en el paso 1, al paso 2 llega el 36 %.

# Anexo B. Dónde está cada cosa en el Sheets

| Pestaña | Qué trae | Sirve para |
|---|---|---|
| Parámetros | Costos, mínimos y topes. Cambiarlos recalcula todo | Secciones 0, 3 y 5 |
| Canales | Volumen, respuesta, costo y bajas por canal y mes | 0.3, 5.1, E3, E4 |
| Equipos | Lo mismo por equipo | 0.5, E2 |
| Campañas | Una fila por pieza y canal con señal y acción | Sección 8 |
| Catálogo | Una fila por familia: ticket, audiencia, gancho, estado, versiones | 1.7, paso 2 de la sección 6 |
| Vista_equipo | Todo lo anterior para un equipo (celda B2) | Sección 9 |
| Insights | Hallazgos con cifra, filtrables | Anexo E |
| Plan_accion | Ahorro por acción, las diez que más pesan, por equipo | Secciones 8 y 9 |
| Estándares | 24 indicadores con valor actual, estándar y estado por equipo | Anexo A1, sección 9 |
| N_DiaSemana | Envíos y respuesta por día de la semana, canal y equipo | 0.2, E9, A8 |
| O_Antiguedad | Respuesta, push por usuario y bajas por banda de antigüedad | 0.4, E10 |
| P_Segmentos | Los 41 segmentos, 330 subsegmentos y 62 grupos reales con envíos y respuesta, y la lista de duplicados | 1.3, A9 |
| Q_Control | Los 22 Canvas con usuarios en control y las piezas grandes sin control | E11 |
| R_Experimentos | Ramas y variantes por Canvas con conversión | E12 |
| S_Pasos | Una fila por paso de Canvas con usuarios, apertura y conversión; los 477 pasos a apagar | 0.7, E13, A11 |
| T_SinRespuesta | Envíos, costo y bajas a usuarios que nunca respondieron, por mes y canal | Sección 2, E0, A10 |
| U_Contactable | Envíos por canal contra canal contactable y banderas del golden dataset | Sección 2, E0 |

# Anexo C. Lo que todavía no sabemos

| Qué | Estado |
|---|---|
| Tags | No están en Databricks. Si alguien exporta la lista de campañas con tags desde Braze, se audita en una hora. |
| Día de la semana | Listo (0.2, E9 y A8). |
| Segmentos reales de Braze | Listo (1.3 y A9). |
| Antigüedad del usuario | Listo (0.4 y E10). `days_on_book` tiene 1.1 % de registros con alta posterior al envío. |
| Lift real contra control | No se puede hoy: no hay grupos de control (E11). Se podrá medir 4 semanas después de activar piezas con control. |
| Pruebas A/B | No hay ninguna de mensaje (E12). |
| Tipo de celular (iOS o Android) | Sí se puede: `braze.int_communications_joined` trae `device_id` y `platform`. Falta correr la query E18c. |
| Hora del día | La tabla de comunicaciones solo trae fecha. Pedir a Datos que la agregue desde Currents (sección 11). |
| Rebotes y quejas de spam | No están en Databricks. Mismo pedido. |
| Banderas de contactabilidad | Las del golden dataset no coinciden con el comportamiento (Anexo E0). Datos debe definir fecha y fuente. |
| Región | No está en ninguna tabla. |

# Anexo D. Supuestos

- Periodo enero a septiembre de 2026. Respuesta = clic en email, apertura en push, lectura en WhatsApp, clic en in-app.
- Conversión a 7 días como referencia, no como atribución (no hay grupo de control hoy).
- Costos: email 0.05 MXN por enviado, WhatsApp 1.00 MXN por entregado, push e in-app 0. No incluye el costo fijo de Braze.
- Audiencia, gancho y tipo se leen del nombre de la pieza; el 17 % que no sigue la convención cae en "otros".
- Las etapas del golden dataset cubren 37 % de los envíos.
- Las bajas solo existen para email. Lectura de WhatsApp subestimada si el usuario apagó las confirmaciones.
- Grupo de control, experimentos y pasos salen de `_fct_braze_canvas_user_engagement`: solo Canvas (3,228), un usuario cuenta una vez por Canvas, grupo o paso. El orden del paso es por fecha de creación del paso.
- "Nunca respondió" = sin apertura de email, clic, apertura de push, lectura de WhatsApp ni clic en in-app o banner en los 9 meses. Quien respondió por última vez en diciembre cuenta como sin respuesta.
- Antigüedad = `days_on_book` a la fecha de la extracción menos los días desde el envío. Las banderas del golden dataset son a la fecha de la extracción, no a la del envío.
- El día de la semana es el del envío en la zona horaria de la tabla, no la del usuario.

# Anexo E. Evidencia: qué funciona y qué no

Aquí está el análisis que sostiene las tablas de las secciones 0 y 5. Se lee cuando alguien pregunta "por qué". Para saber qué hacer no hace falta leerlo.

## E0. Lo que cuesta no excluir (sección 2)

**Cuánto cuesta escribirle a quien nunca responde.** En 9 meses, 97.5 M mensajes (14.6 % de todo) y 8.1 M MXN (11 % del costo variable, unos 900 mil MXN al mes) fueron a usuarios que no respondieron ni una vez a nada. Por canal: 18 % de los emails (61 M), 12 % de los push (31 M), 9 % de los WhatsApp (5 M, que son 5 M MXN). Generaron 17 % de las bajas de email (191 mil) y ninguna conversión. Cada mes 1.1 M de usuarios reciben email sin haber respondido jamás; en junio fueron 11.9 M por el email de BillPay. La regla "sin respuesta en 90 días, fuera" se paga sola.

**Las banderas de contactabilidad del golden dataset todavía no sirven como exclusión.** Al cruzar los envíos con `dim_braze_filters` (cubre 250 M envíos): 8.2 M emails a usuarios con `email_unsubscribed = true` hicieron clic 0.95 % (más que el promedio), 9.8 M WhatsApp a `wa_unsubscribed = true` se leyeron 55.7 %, 58.6 M push a `app_uninstall = true` se abrieron 1.52 % (igual que el resto) y 16.5 M push fueron a usuarios "sin notificaciones". O la bandera está mal o se calcula a otra fecha. Hasta que Datos la defina, las exclusiones se arman con los eventos de Braze (baja, desinstalación, fallo de WhatsApp). Lo que sí se usa hoy: `is_blacklist`, `is_reus`, `is_arco` y `cc_freeze`. Contando todo tipo de mensaje: 1.48 M envíos a lista negra, REUS o ARCO (130 mil usuarios) y 57.4 M a tarjeta KPay congelada (4.4 M usuarios, 5.1 M MXN).

Cada punto trae el dato y la regla que sale de él. Las reglas ya están en el cuerpo del documento (secciones 0 a 5); aquí queda la evidencia.

## E1. En general

- **Funciona:** in-app (38 % de clic), WhatsApp cuando llega (69 % de lectura), recordar algo empezado, 2 toques, audiencias de 10 a 100 mil con un criterio.
- **No funciona:** email masivo a prospectos, push a bases frías (0.8 %), WhatsApp a bases frías, enviar a toda la base, 3 o más toques, dos equipos sobre la misma gente el mismo día, email masivo en lunes, Canvas de 100 pasos, escribirle 9 meses a quien nunca respondió.
- **Regla:** antes de agregar un mensaje, quita uno. El problema no es mandar mejor, es mandar menos y a quien sí.

## E2. Por equipo

**Marketing.** El que más manda (39 %), más gasta (47 %) y más bajas genera (4.95 por mil, el doble del estándar).

- Funciona: retargeting de Veriff (email 3.0 %, push 5.8 %), referidos a clientes KCash por push (2.4 %), in-app de registro de línea (87 %).
- No funciona: rescates por push a anónimos y leads (0.6 a 0.8 % en 22 M envíos), referidos por email a leads y dormants (0.1 a 0.2 % en 15 M emails), onboarding con 2 emails al día.
- Regla: referidos y lanzamientos salen del email y van a in-app. Rescates por push solo a quien abrió un push en 60 días. Onboarding a 1 email al día.

**Product Growth (Lending).** Donde está el ahorro más grande: 1.3 M MXN al mes.

- Funciona: retargeting de Installments a activos (email 2.8 %, push 11 %), descuento directo a inactivos (0.55 %), in-app (46 %).
- No funciona: Tasa 0 por email a registrados (B0211: 35 M emails, 0.28 % de clic, y ni quien abre convierte), NeverActive por email (13 M, 0.10 %), insistir 3 meses (pierde al usuario a los 92 a 128 días y 17 a 31 emails), los Canvas de inactividad `ConSinOferta` con 72 a 200 pasos (B0331, B0332, B0333: 19 Canvas, 734 mil usuarios).
- Regla: Tasa 0 solo con señal y 2 toques al mes. B0211 y B0223 se apagan por email y se dejan en push acotado. Lending es el único dueño de las bases frías. Los tres Canvas de inactividad se rehacen con 8 pasos y control.

**Sales.** Peor email de todos (0.21 %) y mejor WhatsApp (80 % de entrega, 78 % de lectura).

- Funciona: push y WhatsApp a recurrentes de KPay (Quincenas sin intereses 4.2 %, Primavera 2.2 %, Comercio del día 1.1 a 1.8 %). Sus ventas a recurrentes sí sostienen la conversión a 90 días.
- No funciona: promociones de comercios por email a todo el portafolio (6.4 M, 0.22 %), el mismo evento por dos canales el mismo día, promoción a tarjetas congeladas (13 M envíos).
- Regla: Sales manda por push y WhatsApp a recurrentes, no por email. Un evento = una pieza por canal y calendario con Marketing.

**Collections.** No entra a las reglas promocionales. Precobranza es la pieza que mejor responde de toda la empresa (email 4.3 %, push 5.3 %): protegerla. Pendientes: un ticket por bucket, pausar los Canvas `PRUEBA_` que llegaron a 5 mil usuarios reales, y Legal decide sobre REUS y ARCO.

**Others (transaccional, BillPay, Shopping, Compliance).** Lo transaccional funciona (Payment Confirmation 3.8 %). Lo que no: BillPay Intro (16 M emails, 0.11 %, causó 31 % de las bajas de usuarios nuevos del año) y Shopping WeeklyRecommendations (7 M, 0.12 %, 57 mil a REUS). Regla: BillPay y Shopping entran a las reglas de todos. Lo transaccional se nombra con ticket.

## E3. Por canal

| Canal | Hoy | Mínimo para seguir | Funciona | No funciona |
|---|---|---|---|---|
| Email | 0.92 % de clic, 3.1 bajas por mil | 0.3 % de clic, 2.5 bajas por mil | Transaccional, retargeting, nuevos, 2 toques | Tasa 0, referidos, newsletters, bases frías, más de 1 M |
| Push | 1.5 % de apertura | 0.75 % | Cobranza, nuevos, retargeting, recurrentes | Leads, anónimos, fríos, lanzamientos |
| WhatsApp | 74 % de entrega, 69 % de lectura | 80 % de entrega, 60 % de lectura | Activos, recurrentes de KPay | Bases frías, repetir el mismo WhatsApp a los 2 a 6 días |
| In-app | 38 % de clic | 10 % | Casi todo: referidos, lanzamientos, retargeting, onboarding | Ofertas genéricas (14 %) |

- Email: no es el asunto (abren 24 %), es que no hay qué hacer adentro. Un solo llamado a la acción.
- Push: es el canal de señal. Primero push, y el resto solo a quien lo abrió. Septiembre tuvo el mejor push del año (2.1 %) con el menor volumen desde marzo: menos push, más apertura.
- WhatsApp: 8 % de los envíos y 77 % del costo. Nunca como primer toque.
- In-app: gratis y es el que más responde. Lo que sea informativo va ahí primero.

## E4. Por mes

- **Junio fue el peor mes:** 109 M envíos (el doble de enero), clic 0.67 %, push 1.05 %, 63 mil bajas. Fue el mes del email de BillPay a 16 M usuarios encima de Hot Sale. Más volumen no trajo más respuesta.
- **Enero:** el mejor clic (1.2 %) y las bajas más altas (69 mil). Muchas piezas nuevas sobre bases que no recibían en diciembre.
- **Marzo:** el más caro (12.2 M MXN) por 10 M de WhatsApp.
- **Abril y mayo:** la entrega de WhatsApp tocó piso (69 % y 67 %). Se siguió mandando. Se recuperó a 78 % cuando bajó el volumen.
- **Mayo, junio y agosto:** los meses donde más gente recibe 3 o más piezas el mismo día (Hot Sale, BillPay, regreso a clases).


## E5. Por producto

- **KCash:** 48 % de los envíos, 58 % del costo. Responde el doble que KPay. Su problema es la insistencia (Tasa 0 a registrados) y dos equipos sobre la misma base. Regla: un dueño por audiencia, una pieza de Tasa 0 por audiencia.
- **KPay:** casi el doble de piezas que KCash (985) para menos volumen: muchas piezas chicas y repetidas (Comercio del día por mes). Menor respuesta en email (0.44 %) y push (1.1 %). Regla: Comercio del día es una sola pieza con versiones, no una por mes. Canal: push y WhatsApp a recurrentes.
- **Ecosistema:** piezas a "Todos", bajas más altas (3.9 por mil), clic más bajo (0.37 %). Regla: nada a Todos sin pasar por in-app primero.
- **Installments:** responde bien (1.4 % de clic, 0.5 bajas por mil) con poco volumen. Regla: escalar con segmento.
- Una pieza no cubre dos productos. Se parte en dos.

## E6. Por tamaño y por toques

- 10 a 100 mil usuarios: clic 1.2 %. 100 mil a 1 M: 0.6 %. Más de 1 M: 0.16 %. Regla: el tamaño ideal es 10 a 100 mil con un criterio. Más de 1 M obliga a prueba al 10 %.
- 1 toque: 0.8 % de clic. 2 toques: 1.8 %. 3 a 4: 0.5 %. Regla: 2 toques y se acabó.

## E7. Usuarios nuevos

- 33 % se da de baja con el primer email. La mitad se va en el primer mes. Antes de irse recibieron 5 emails de 4 piezas distintas.
- Las causas: el email masivo de BillPay (31 % de las bajas de nuevos), el retargeting de registro de Marketing con 2 emails al día (22 %), los rescates de Tasa 0 (8.5 %).
- Regla: un nuevo entra a una sola secuencia de bienvenida. 1 email al día, 3 la primera semana. Si no abrió ninguno de sus primeros 5 emails, se pausa lo promocional por email. Ningún envío masivo incluye a usuarios con menos de 30 días.

## E8. Cómo saber si una pieza sirve: abren contra no abren

Por cada pieza se compara cuánto convierten los que abrieron contra los que no, a 7 días. Lo normal: quien abre convierte 2 a 3 veces más (email 8 % contra 4 %; push 20 % contra 7 %; WhatsApp 6 % contra 3 %).

- Si quienes abren convierten menos de la mitad de lo normal del canal: no hay a quién acotar. Se apaga.
- Si quienes abren convierten igual que quienes no (menos de 1.5 veces): el mensaje no cambia nada. Se rehace o se apaga.
- Si quienes abren convierten mucho más pero abren pocos: la pieza está bien, la base no. Se acota a quien abrió algo en 60 días.
- Para saber de verdad si el mensaje causa la conversión hace falta grupo de control. Hoy no hay ninguno (E11).

## E9. Por día de la semana

- **Lunes** es el día con más email (72 M entregados, 19 % de todo lo que se manda) y el peor clic (0.65 %). **Domingo** tiene el mejor clic (1.91 %) y las peores bajas (7.7 por mil, el doble que entre semana). Sábado parecido: 1.58 % de clic, 5.5 bajas por mil.
- **WhatsApp** se entrega y se lee mejor en fin de semana: entrega 87 % domingo y 82 % sábado contra 71 a 75 % entre semana; lectura 89 y 82 % contra 65 a 70 %.
- **Push e in-app** no cambian con el día (push 1.3 a 1.6 %, in-app 37 a 39 %).
- **Cuidado:** el fin de semana no responde mejor por el día, sino por lo que se manda ese día: piezas más chicas y a gente más caliente. Product Growth tiene 14.5 % de respuesta en fin de semana con 13.6 M envíos, contra 6.3 % entre semana con 163.6 M. Collections no manda en domingo y su sábado es peor que la semana (11 contra 16 a 18 conversiones por mil).
- **Regla:** el lunes no se manda email masivo; el volumen se reparte de martes a jueves. En fin de semana solo piezas acotadas, con tope de bajas, y nunca a usuarios nuevos. WhatsApp a recurrentes en sábado. La hora buena no se adivina: se prueba (E12 y sección 11).

Clic de email por equipo y día:

| Equipo | Dom | Lun | Mar | Mié | Jue | Vie | Sáb |
|---|---|---|---|---|---|---|---|
| Marketing | 1.66 % | 1.00 % | 0.74 % | 0.69 % | 1.21 % | 0.80 % | 1.55 % |
| Product Growth | 1.53 % | 0.29 % | 0.46 % | 0.77 % | 0.34 % | 0.33 % | 1.29 % |
| Sales | 0.15 a 0.38 % todos los días | | | | | | |

## E10. Por antigüedad del usuario

| Antigüedad en la base | % de envíos | Respuesta | Email clic | Push | Push por usuario (9 meses) | Conversiones por mil | Bajas por mil |
|---|---|---|---|---|---|---|---|
| Menos de 1 mes | 7 % | 8.7 % | 2.41 % | 3.44 % | 13 | 8.2 | 3.0 |
| 1 a 3 meses | 8 % | 7.6 % | 1.30 % | 1.94 % | 26 | 7.4 | 3.6 |
| 3 a 6 meses | 11 % | 7.7 % | 0.88 % | 1.48 % | 32 | 6.4 | 3.3 |
| 6 a 12 meses | 16 % | 7.2 % | 0.76 % | 1.29 % | 43 | 6.4 | 3.5 |
| 1 a 2 años | 26 % | 5.9 % | 0.65 % | 1.30 % | 62 | 6.7 | 3.5 |
| Más de 2 años | 31 % | 5.7 % | 0.55 % | 1.27 % | 91 | 6.7 | 3.1 |

- El 56 % de los envíos va a usuarios con más de un año en la base, que son los que menos responden. A más antigüedad, más mensajes y menos respuesta: el usuario de más de 2 años recibe 7 veces más push que el nuevo y abre la tercera parte.
- Las bajas por mil son iguales en todas las bandas (3 a 3.6). El usuario nuevo no se da de baja más por email que el viejo; se da de baja por la cantidad (E7).
- **Regla:** a más de 1 año en la base y sin respuesta en 90 días, fuera de lo promocional (regla 2). El push a usuarios de más de 2 años solo a quien abrió un push en 90 días. La frecuencia alta se reserva para el primer mes, que es cuando responden.
- Dato: 1.1 % de los envíos cae en usuarios cuya fecha de alta es posterior al envío. `days_on_book` tiene un problema que Datos debe revisar.

## E11. Grupo de control: hoy no existe

- De 3,228 Canvas, 22 tienen usuarios marcados como control y solo uno tiene más de mil (`B0301 Retargeting Installments`, 71 mil en "control"). Y ese grupo abrió el mensaje 84 % de las veces: es un camino del Canvas que se llama Control, no un grupo que no recibe nada.
- 4 Canvas `ControlGroupSplit` de KPay (650 mil usuarios en total) usan un push silencioso para simular control. Braze trae grupo de control nativo en campañas y en la entrada del Canvas, y reporta el lift solo. Se usa ese.
- **Consecuencia:** ninguna cifra de conversión de este documento es incremental. Dice quién convierte después de recibir, no cuánto más convierte por recibir. Con 7 % de respuesta y 12 conversiones por mil en recurrentes, parte de esa gente iba a comprar igual.
- **Regla:** toda pieza nueva o relanzada lleva 10 % de control (5 % si pasa de 1 M) desde el día uno. A las 4 semanas se lee el lift: conversión de quien recibió menos conversión del control. Si el lift es cero, la pieza se apaga aunque "convierta".
- Las piezas más grandes sin control hoy, y las primeras en recibirlo al relanzar: Referral Program (2.38 M usuarios), QA ReminderRegistroTelefono (1.87 M), BillPay onboarding (1.7 M por tres Canvas), NarrativaTasa0 (1.65 M), Día del Padre push (1.57 M), AnotayGana (1.56 M por dos).

## E12. Experimentos: hay caminos, no pruebas

- 313 Canvas tienen "experimento" (31.4 M usuarios) y 122 tienen más de una rama, pero casi todas las ramas son caminos de audiencia (`Path 1`, `Path 2`, `Contactados`) y la variante de mensaje es siempre `Variant 1`. En 9 meses no hay una sola prueba A/B de mensaje: ni asunto, ni copy, ni hora, ni día.
- Lo que sí se puede comparar hoy: Installments contra Single Payment contra SP en B0301 (conversión 30.9 %, 29.5 % y 40.4 %); Precobranza por email contra push (22.3 % contra 21.6 %, iguales, y el push es gratis); Referral a leads camino 1 contra camino 2 (0.55 % contra 1.51 %); NarrativaTasa0 camino 1 (5.8 % de apertura) contra caminos 2 y 3 (27 %).
- **Regla:** cada equipo corre una prueba A/B de verdad al mes: una sola variable, misma base, mismo día, 50/50 y con control. Las primeras tres: día de envío (martes contra sábado con la misma pieza), asunto del email, push con y sin monto. La variante va en el nombre del paso (`04-Push-Oferta-T1-B`) y el ganador se anota en el ticket. Lo que no se prueba no se discute en el comité.

## E13. Por paso del Canvas

- 959 Canvas con 5,986 pasos. La mitad tiene 3 pasos o menos; 45 pasan de 20 y 19 pasan de 50.
- De los usuarios que entran al paso 1 (31.5 M), al paso 3 llega la mitad (16.7 M) y al paso 4 una quinta parte (7 M). La apertura por paso no sube con la insistencia: 16 %, 16 %, 26 %, 16 %, 16 %. El paso 3 abre más porque ahí suelen entrar los filtros de quien ya reaccionó, no porque el tercer mensaje convenza.
- Por canal, el paso 3 y 4 de push abren 6 % contra 2 % en los dos primeros: cuando el push va detrás de una señal, funciona. WhatsApp se lee igual en cualquier paso (39 a 53 %).
- 477 pasos con mil o más usuarios abren menos de 1 %. 80 tienen más de 10 mil usuarios y abren menos de 0.5 %: el email de CuestaEnero paso 1 (1.09 M usuarios, 0.01 %), otro paso de 516 mil usuarios con 0.00 %, los push de Nuevos_MPNeverCash (170 mil, 0.4 %).
- **Regla:** máximo 8 pasos y 2 toques por canal. Después de cada envío, un paso de Decision. Un paso con menos de 1 % en mil usuarios se apaga ese mes. El orden del paso en Databricks es aproximado (sale de la fecha de creación), por eso el nombre del paso lleva su número (1.2).
