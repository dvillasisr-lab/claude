# Muestra: lente B, canales

Esto es una muestra de cómo se verá cada lente del análisis. Un archivo por lente, con el mismo formato: respuesta primero, hallazgos con cifra, comparación, query y confianza, luego la tabla de serie de tiempo y las preguntas abiertas. Si el formato te sirve, los nueve lentes se producen igual.

Periodo: enero a septiembre 2026 (9 meses completos). Vista semanal: 38 semanas completas, del 5 de enero al 27 de septiembre.
Fuentes: `data/e1_comunicacion_mes_canal.csv`, `data/e4a_serie_semana_mes_canal.csv`, `data/e4b_concentracion_mes.csv`. Queries en `sql/muestra_b_canales.sql` (DuckDB sobre los CSV).

## Respuesta en una página

WhatsApp se lleva el 77 % del costo variable con el 8 % de los envíos, y uno de cada cuatro mensajes no se entrega: 14.2 M MXN pagados por mensajes que nunca llegaron. Push es el 38 % del volumen y el 58 % de ese volumen va en comunicaciones que abre menos del 1 % de la gente. Email cumple en apertura pero no en clic ni en bajas. In-app es el canal más eficiente por envío y el menos usado.

Tres movimientos salen de aquí: limpiar la base de WhatsApp antes de enviar, poner tope de frecuencia a push y mover a in-app lo que hoy va por push a usuarios que abren la app.

## Hallazgos

### H-B1. Pagamos 14.2 M MXN en 9 meses por WhatsApp que no se entregaron
Cifra: 14.2 M de 55.2 M mensajes WhatsApp sin entrega (25.8 %). A 1 MXN cada uno, 14.2 M MXN. Periodo: enero a septiembre 2026. Denominador: WhatsApp enviados.
Comparación: la entrega cayó de 80 % en enero a 67 % en mayo y se recuperó a 77 % en septiembre. El benchmark de entrega de WhatsApp es arriba de 90 %.
Query: Q5 y Q6 en `sql/muestra_b_canales.sql`.
Confianza: alta. La tabla trae envío y entrega por fila y el costo es el que diste (1 MXN por mensaje). Motivo de duda: no sabemos si el proveedor cobra el mensaje no entregado; si no cobra, el costo real es menor y el hallazgo pasa a ser de calidad de base.
Implicación: validar números antes de enviar (formato, país, opt-in de WhatsApp) y suprimir los que fallaron dos veces. Es el ahorro más directo del análisis.

| Mes | Enviados | Entregados | Entrega | Costo perdido MXN |
|---|---|---|---|---|
| Ene | 5.6 M | 4.5 M | 80.0 % | 1.12 M |
| Feb | 7.8 M | 6.0 M | 77.1 % | 1.78 M |
| Mar | 10.4 M | 7.7 M | 73.9 % | 2.72 M |
| Abr | 5.9 M | 4.1 M | 69.3 % | 1.80 M |
| May | 6.1 M | 4.1 M | 67.3 % | 1.99 M |
| Jun | 7.1 M | 5.3 M | 74.3 % | 1.83 M |
| Jul | 4.8 M | 3.5 M | 72.9 % | 1.29 M |
| Ago | 4.4 M | 3.4 M | 78.0 % | 0.97 M |
| Sep | 3.2 M | 2.5 M | 77.3 % | 0.73 M |

### H-B2. El 58 % del volumen de push va en comunicaciones que abre menos del 1 % de la gente
Cifra: 146 M de 251 M push en comunicaciones con apertura menor a 1 %. Apertura global de push: 1.5 %. Periodo: enero a septiembre 2026. Denominador: push enviados.
Comparación: benchmark de apertura directa de push 3 a 10 %. Ningún mes llega a 2.2 %.
Query: Q8 y Q9.
Confianza: alta en la cifra. Media en la lectura: Braze registra apertura directa; la influida no está en la tabla, así que la apertura real es algo mayor pero no 3 veces mayor.
Implicación: las Canvas "Rescate" de Marketing (Anonimos-RescateTasa0 con 8.3 M envíos y 0.55 % de apertura, RescateFinesDeSemana con 10.5 M en cuatro versiones y menos de 1 %) son las primeras a revisar. Y hay una campaña con prefijo QA (ReminderRegistroTelefono) que mandó 1.9 M push a producción con 0.01 % de apertura: apagar hoy.

### H-B3. Email abre bien, pero no genera clic y pierde entre 0.75 % y 1.5 % de su base cada mes
Cifra: apertura 23.7 % sobre entregados, clic 0.93 %, bajas 457 mil usuarios únicos en 9 meses. Periodo: enero a septiembre 2026. Denominador: emails entregados y usuarios únicos con email entregado.
Comparación: benchmark de email promocional: apertura 15 a 25 % (cumple), clic 1.5 a 3 % (no cumple), baja menor a 0.3 % por envío. La tasa mensual por usuario de 0.75 a 1.5 % es alta: a ese ritmo se pierde cerca del 10 % de la base contactable al año.
Query: Q2.
Confianza: alta. Las bajas son usuarios únicos con `email_unsubscribe = true`, según lo que confirmaste.
Implicación: el problema de email no es que no lo abran, es que no hay qué hacer dentro. Revisar llamadas a la acción y relevancia antes que asunto. El envío de BillPay de junio es el ejemplo: 16.1 M emails, apertura 7.7 % contra 22.6 % del resto del mes, clic 0.10 %, 37 mil eventos de baja, 806 mil MXN.

### H-B4. In-app convierte 12 veces más que email por envío y cuesta cero, pero es solo el 4 % del volumen
Cifra: en Cash, 31.3 conversiones por cada 1,000 impresiones in-app contra 2.6 por 1,000 emails, 3.1 por 1,000 push y 4.9 por 1,000 WhatsApp. Clic sobre impresión 38 %. Periodo: enero a septiembre 2026. Denominador: envíos del canal en Cash, conversión fraccional.
Comparación: entre canales, mismo producto, misma atribución.
Query: Q1 y Q10.
Confianza: media. In-app solo llega a quien ya abrió la app, que de entrada está más cerca de convertir. La diferencia real es menor que 12 veces, pero el orden se sostiene.
Implicación: para usuarios activos en la app, in-app debería ser el canal por defecto y push el respaldo, no al revés. Hoy push manda 95 M a Cash e in-app 10 M.

### H-B5. Una conversión de Cash por WhatsApp cuesta 204 MXN, por email 19 MXN
Cifra: costo variable entre conversiones fraccionales, solo Cash. WhatsApp 34.6 M MXN entre 170 mil conversiones; email 9.0 M MXN entre 470 mil. Periodo: enero a septiembre 2026.
Comparación: 10.7 veces más caro. Push e in-app tienen costo variable cero.
Query: Q10.
Confianza: media. La atribución fraccional reparte la conversión del día entre todas las comunicaciones que llegaron ese día, así que ningún canal se lleva el crédito completo. El costo fijo de Braze no está incluido (pendiente del contrato).
Implicación: WhatsApp solo donde email y push no llegan, o para montos altos donde 204 MXN por conversión se justifica. Hoy se usa como canal masivo.

### H-B6. Entre 4 % y 8 % de los usuarios reciben entre 20 % y 37 % de los mensajes, y la concentración no ha bajado desde mayo
Cifra: usuarios con 41 o más mensajes al mes. Enero: 3.6 % de los usuarios, 19.6 % de los mensajes. Mayo: 6.6 % y 37.0 %. Septiembre: 6.2 % y 30.1 %. Periodo: por mes. Denominador: usuarios con al menos una fila en el mes y mensajes del mes.
Comparación: contra enero, la concentración subió 10 puntos y se quedó.
Query: Q4.
Confianza: alta. E4b suma exacto contra E3.
Implicación: tope de frecuencia por usuario (el lente E lo cuantifica por semana y cruza con bajas). 41 mensajes al mes son 10 por semana, el doble del umbral de 5 que fijamos.

## Serie mensual (la vista de tablero)

| Mes | Envíos | Email % | Push % | WA % | In-app % | Costo MXN | Entrega email | Apertura email | Clic email | Baja email (usuarios) | Apertura push | Entrega WA | Lectura WA | Clic in-app | Msgs en usuarios 41+ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Ene | 58.7 M | 60 | 27 | 10 | 3 | 7.37 M | 91.5 % | 28.1 % | 1.20 % | 1.51 % | 1.83 % | 80.0 % | 74.6 % | 47.5 % | 19.6 % |
| Feb | 67.5 M | 52 | 32 | 11 | 4 | 9.52 M | 96.2 % | 28.0 % | 0.88 % | 1.25 % | 1.43 % | 77.1 % | 73.3 % | 19.1 % | 29.3 % |
| Mar | 67.7 M | 53 | 27 | 15 | 4 | 12.24 M | 96.4 % | 29.7 % | 1.03 % | 0.99 % | 1.81 % | 73.9 % | 72.5 % | 24.0 % | 21.5 % |
| Abr | 64.3 M | 53 | 35 | 9 | 4 | 7.55 M | 95.8 % | 26.9 % | 0.98 % | 0.85 % | 1.53 % | 69.3 % | 65.6 % | 36.0 % | 28.5 % |
| May | 85.0 M | 47 | 41 | 7 | 4 | 8.09 M | 95.8 % | 22.7 % | 0.86 % | 0.77 % | 1.28 % | 67.3 % | 67.1 % | 47.4 % | 37.0 % |
| Jun | 109.0 M | 46 | 43 | 7 | 4 | 9.65 M | 93.5 % | 18.1 % | 0.67 % | 0.41 % | 1.05 % | 74.3 % | 67.4 % | 45.4 % | 35.7 % |
| Jul | 71.7 M | 45 | 43 | 7 | 5 | 6.36 M | 95.9 % | 20.9 % | 1.00 % | 1.23 % | 1.77 % | 72.9 % | 62.5 % | 37.0 % | 32.6 % |
| Ago | 77.9 M | 45 | 46 | 6 | 4 | 6.13 M | 95.7 % | 20.7 % | 0.95 % | 1.13 % | 1.57 % | 78.0 % | 63.6 % | 41.5 % | 35.3 % |
| Sep | 65.6 M | 54 | 37 | 5 | 4 | 4.96 M | 95.6 % | 20.4 % | 0.92 % | 0.75 % | 2.12 % | 77.3 % | 64.1 % | 41.5 % | 30.1 % |

Lectura rápida: el costo bajó de 12.2 M en marzo a 5.0 M en septiembre porque WhatsApp bajó de 10.4 M a 3.2 M envíos. La apertura de email cae de 28 % a 20 % entre el primer y el tercer trimestre. La lectura de WhatsApp cae de 75 % a 64 %. Push sube de volumen y no mejora.

Nota sobre la baja de junio (0.41 %): el denominador ese mes son 15.5 M usuarios únicos por el envío de BillPay, contra 4.3 a 5.1 M los demás meses. En usuarios absolutos junio tuvo 63 mil bajas, el segundo peor mes.

## Serie semanal

Semanas completas (lunes a domingo) del 5 de enero al 27 de septiembre: 38 semanas. Volumen semanal entre 11.7 M y 26.2 M, con un pico de 39.6 M la semana del 1 de junio (BillPay). Las semanas del 29 de diciembre y del 28 de septiembre se excluyen porque solo tienen 3 días dentro del periodo. La serie completa por canal está en Q3 y en el tablero.

## Qué más analizar

1. ¿El proveedor cobra el WhatsApp no entregado? Cambia H-B1 de "dinero tirado" a "base sucia". Necesita la factura del proveedor.
2. ¿Qué parte de la no entrega de WhatsApp es número inválido, usuario sin WhatsApp o bloqueo? La tabla no distingue. Necesita el motivo de fallo de Braze (`whatsapp_failure` con `reason`).
3. ¿La apertura influida de push cambia la foto? Necesita `pushnotification_influencedopen`.
4. ¿Cuánto del volumen de push a Cash va a usuarios que abrieron la app esa semana (candidatos a in-app)? Necesita cruce con sesiones.
5. ¿El clic de email cae por diseño de pieza o por audiencia? Comparar clic por tipo de comunicación (lente A) y por equipo (lente D).
