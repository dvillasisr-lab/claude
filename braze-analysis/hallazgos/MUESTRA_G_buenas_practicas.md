# Muestra del lente G: qué ayuda y qué empeora (buenas prácticas con datos propios)

Periodo: enero a septiembre 2026. Fuentes: E1 (comunicación × mes × canal) y E3 (distribución por usuario). Query reproducible: `sql/muestra_g_buenas_practicas.sql`. Solo promocionales y lifecycle; cobranza y transaccionales se excluyen de las comparaciones. Respuesta = clic en email, apertura en push, lectura en WhatsApp, clic en in-app. Conversión solo de referencia.

La idea: en vez de benchmarks de la industria, comparar nuestras propias comunicaciones entre sí por audiencia, gancho, tamaño, intensidad y canal, y convertir las diferencias en reglas. Con E6 y E7 se afinan (solapamiento y respuesta por segmento).

## 1. La audiencia pesa más que el canal

| Audiencia (por el nombre) | Email clic | Email bajas por mil | Push apertura | WhatsApp lectura | WhatsApp entrega | WhatsApp costo MXN |
|---|---|---|---|---|---|---|
| Clientes activos y recurrentes | 0.72 % | 3.1 | 1.75 % | 70.1 % | 81.6 % | 14.9 M |
| Nuevos y onboarding | 1.25 % | 6.9 | 3.18 % | 67.5 % | 77.4 % | 0.8 M |
| Leads y registrados sin crédito | 0.75 % | 4.6 | 0.94 % | 73.4 % | 74.9 % | 15.1 M |
| Fríos: dormants, inactivos, rezagados, never active | 0.35 % | 4.3 | 0.77 % | 64.6 % | 68.5 % | 23.0 M |

Lo que empeora: las bases frías. Responden la mitad que los activos en email y push, un tercio de sus WhatsApp no se entrega, y aun así se llevan 23 M MXN de WhatsApp (la tercera parte del gasto del canal) con 1.1 conversiones de referencia por mil contra 17 en activos.

Regla: a bases frías no se les manda WhatsApp masivo. Primero push o email de bajo costo para detectar señal de vida (apertura o clic), y WhatsApp solo a los que reaccionan.

## 2. El gancho: "tasa 0" es el más usado y el que menos responde

| Gancho (por el nombre) | Email envíos | Email clic | Email bajas por mil | Push apertura | WhatsApp lectura | In-app clic |
|---|---|---|---|---|---|---|
| Retargeting o recordatorio | 23.1 M | 2.99 % | 3.8 | 2.16 % | 70.3 % | 57.9 % |
| Cross sell | 2.7 M | 0.34 % | 2.0 | 1.69 % | 53.8 % | 24.7 % |
| Descuento, cupón u oferta | 35.0 M | 0.41 % | 3.4 | 1.38 % | 57.8 % | 14.4 % |
| Tasa 0 | 54.3 M | 0.53 % | 4.6 | 0.68 % | 68.8 % | 21.7 % |
| Referidos | 40.8 M | 0.22 % | 4.3 | 1.15 % | 71.4 % | 42.7 % |
| Lanzamiento, novedades, newsletter | 33.0 M | 0.22 % | 5.6 | 0.91 % | 73.1 % | 54.5 % |

Lo que ayuda: recordar algo que el usuario ya empezó (retargeting) responde 5 a 10 veces más que ofrecer algo nuevo. Lo que empeora: tasa 0 y newsletters son los que más bajas generan por mil entregados. Referidos no funciona por email (0.22 %) pero sí en in-app (42.7 %): el mensaje está bien, el canal no.

Regla: el gancho principal de email es "lo que dejaste a medias". Referidos y lanzamientos van en in-app, no en email masivo.

## 3. El tamaño de la audiencia: más grande, peor

| Usuarios por envío (comunicación × mes) | Email clic | Email bajas por mil | Push apertura |
|---|---|---|---|
| 10 mil a 100 mil | 1.15 % | 2.0 | 1.98 % |
| 100 mil a 1 M | 0.57 % | 1.9 | 1.16 % |
| 1 M o más | 0.16 % | 2.5 | 0.93 % |

Un envío a más de un millón de usuarios responde 7 veces menos por email que uno de 10 a 100 mil, y genera más bajas. No es el tamaño en sí: es que a esa escala ya no hay segmentación.

Regla: ningún envío promocional a más de 1 M de usuarios sin una prueba previa al 10 % y sin un criterio de segmento (etapa, última acción, canal donde respondió).

## 4. Intensidad: dos mensajes al mes por usuario es el punto óptimo

| Mensajes de la misma comunicación por usuario en el mes | Email clic | Email apertura | Email bajas por mil | Push apertura |
|---|---|---|---|---|
| 1 | 0.75 % | 21.7 % | 2.0 | 1.17 % |
| 2 | 1.76 % | 35.3 % | 1.5 | 2.52 % |
| 3 a 4 | 0.48 % | 19.2 % | 1.6 | 1.56 % |
| 5 o más | 0.84 % | 14.1 % | 1.4 | 1.11 % |

Un recordatorio (dos toques) duplica la respuesta del primer envío. El tercero y el cuarto ya no suman: el clic cae a la cuarta parte. Cinco o más es cobranza y transaccional, que responden por otra razón.

Regla: tope de 2 toques por comunicación por usuario al mes en promocionales. El segundo solo a quien no abrió el primero.

## 5. Fatiga por usuario: a más mensajes, más bajas

De E3, eventos de baja de email por cada 100 usuarios, según cuántos mensajes recibió el usuario en 9 meses (todos los canales):

| Mensajes al usuario en 9 meses | Usuarios | % de usuarios | Eventos de baja por 100 usuarios | Costo por usuario MXN |
|---|---|---|---|---|
| 1 a 5 | 11.1 M | 57 % | 1.3 | 0.1 |
| 6 a 10 | 0.9 M | 5 % | 9.7 | 1.0 |
| 11 a 20 | 1.3 M | 7 % | 11.9 | 2.5 |
| 21 a 40 | 1.7 M | 9 % | 12.5 | 4.3 |
| 41 a 80 | 2.1 M | 11 % | 9.5 | 8.9 |
| 81 a 160 | 1.4 M | 7 % | 9.6 | 12.0 |
| 161 a 320 | 0.7 M | 3 % | 11.0 | 18.2 |
| 321 o más | 0.3 M | 2 % | 16.5 | 35.3 |

Son eventos, no usuarios únicos (un usuario puede darse de baja varias veces), así que la cifra sirve para comparar bandas, no como tasa. La lectura: el salto grande está entre 5 y 6 mensajes en 9 meses, y el grupo de 321 o más (339 mil usuarios, 482 mensajes cada uno) es el que más se da de baja y el que más cuesta. La conversión también sube con los mensajes, pero al revés: los clientes activos reciben más mensajes porque son activos, no convierten porque reciban más.

Regla: tope global por usuario (todas las comunicaciones promocionales), a definir con E6. Punto de partida: 5 por semana como dice METRICAS.md, y revisar el grupo 321+.

## 6. Lo que no se puede concluir todavía

- Multicanal: la misma idea en 3 o más canales no responde claramente mejor ni peor que en uno. Necesita E6 (quién recibe qué el mismo día).
- Horario y día de envío: E1 es mensual. Sale de E4a por semana, o de una extracción por día de la semana y hora.
- Qué segmento responde a qué: sale de E7a (etapa del golden record) y E7b (patrón por usuario).
- Abren y convierten vs no abren: el método que ya usas para decidir sale de E7c (escrita).

## Checklist antes de lanzar o renovar una comunicación promocional

1. Audiencia con una acción reciente o una etapa clara. Si es base fría, primero push o email, WhatsApp solo a quien reaccionó.
2. Gancho: qué dejó a medias el usuario. Tasa 0 y novedades solo con segmento.
3. Tamaño: más de 1 M de usuarios obliga a prueba al 10 % y criterio de segmento.
4. Toques: máximo 2 por mes por comunicación, el segundo solo a quien no abrió.
5. Canal por tipo de mensaje: referidos y lanzamientos en in-app; recordatorios en push y email; WhatsApp para activos con entrega arriba de 80 %.
6. Salida: si en 2 meses la respuesta queda debajo del mínimo del canal (email clic 0.3 %, push 0.75 %, WhatsApp lectura 60 %, in-app 10 %) o las bajas pasan de 2.5 por mil, se apaga o se rehace.
7. Límite global por usuario: contar todas las promocionales que recibe en la semana antes de agregar una más.
