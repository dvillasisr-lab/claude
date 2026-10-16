# Notas parte 6: medición, caso de negocio, plan y anexo (láminas 83 a 105, ahora 83 a 107)

Scripts (scratchpad, no repo): `v6parts/p6work/s1_camp.py` (reconstruye en memoria la pestaña Campañas del Sheets v4 ejecutando `build_sheets_v4.py` hasta `NCAMP`, sin guardar el xlsx), `s2_ahorro.py` (palancas en septiembre), `s3_cortes.py`, `s4_puente.py` (puente entre cifras), `s5_extra.py` (acciones, bajas, top por equipo), `s6_buckets.py` (certeza). Correr desde `braze-analysis/`.

## 1. Reconciliación del ahorro

### De dónde sale cada cifra

| Cifra | Fuente | Regla | WhatsApp | Mes | Lecturas tardías |
|---|---|---|---|---|---|
| 3.18 M MXN al mes (nota de campañas) | `sql/muestra_c_campanas.sql` y `hallazgos/muestra_c_familias.csv`, columna `ahorro_mxn_mes` | campaña por canal promocional, activa en septiembre, señal apagar o rehacer (89 filas, 59 familias); costo del periodo entre meses con envío | por enviado (`costo_mxn` de E1) | promedio de meses con envío | NO: el query filtra `WHERE envios > 0`, así que tira las lecturas y entregas registradas en meses sin envío |
| 1.60 M MXN al mes (deck, "582 campañas") | `build_sheets_v4.py` (Plan_accion P1/P2, columna `ahorro_mes_ent`), reproducido exacto: 1,598,363 | misma regla, 85 filas activas (Apagar 48, Rehacer 33, Limpiar 4); cuenta 100 % del costo de limpiar y rehacer | por entregado | promedio de meses con envío | SÍ (suma todas las filas de E1) |

"582 campañas" no son las que ahorran: son las filas con alguna acción (48 apagar + 56 limpiar + 162 rehacer + 84 bajar frecuencia + 232 confirmar apagado).

### Puente

| Paso | MXN al mes |
|---|---|
| Nota de campañas (WA enviado, sin lecturas tardías) | 3.18 M |
| Cobrar WhatsApp por entregado | menos 0.78 M = 2.40 M |
| Contar lecturas tardías: 4 WhatsApp pasan de 60 % de lectura y salen de apagar (Marketing B0171 Leads_BBDDRezagada-RescateTasa0 0.54 M: 57.7 % a 61.5 %; B0209 Recurrentes_Inactivos 0.16 M; B0171 HotLeadsW2 0.07 M; B0331 Softnactive 0.03 M) | menos 0.81 M = 1.60 M (deck) |
| Mismas 85 filas con el costo de septiembre | 1.76 M |
| Propuesta (ver abajo) | 2.34 M |

Product Growth 59 % contra 81 %: la diferencia es casi toda B0171 Rezagada (Marketing), que sale del ahorro al contar lecturas tardías. En la propuesta, Product Growth 67 %.

### Propuesta: una cifra, septiembre, WhatsApp por entregado, sin doble conteo

Base: costo de septiembre por campaña por canal (E1, todas las filas de septiembre), email 0.05 por enviado, WhatsApp 1.00 por entregado. Gasto de septiembre 4.23 M (promocional 3.69 M). Palancas en este orden; cada una toma lo que dejó la anterior; solo promocional (más pruebas internas de cualquier tipo):

1. Pruebas internas a clientes (nombre con prueba, test, QA, copy, copia, dummy, demo): 0.013 M.
2. Bloqueados: proporción de envíos a tarjeta congelada, REUS o ARCO y lista negra de E7a por campaña y canal, por el costo de septiembre: 0.171 M.
3. Duplicados: E6b, misma campaña (otra versión), mismo canal, mismo día; usuario-días por costo unitario, entre 9: 0.023 M (mínimo, solo 1,000 pares).
4. Apagar: señal apagar, quien abre no convierte (columna `mueve` = 0), activa: 1.315 M (0.762 M a leads, registrados y cross sell; 0.553 M a churn, dormants e inactivos).
5. Limpiar WhatsApp y rehacer email (señal apagar, quien abre sí convierte): solo la parte a quien no responde por ese canal en 90 días (E9b: 23.3 % del WhatsApp entregado, 87.6 % del email): 0.177 M (WhatsApp 0.042, email 0.135).
6. Canal preferido en el resto del promocional: WhatsApp a quien no leyó WhatsApp pero responde por otro (10.0 %) y email a quien no hizo clic pero responde por otro (42.5 %): 0.338 M.
7. Quien no respondió a nada en 90 días (13.3 % del WhatsApp, 45.1 % del email): 0.299 M.

Total 2.336 M MXN al mes; 31.6 M mensajes menos al mes (48 % de 65.6 M en septiembre).

| Por certeza | MXN al mes | Al año | % gasto sept (4.23 M) | % gasto promedio (6.41 M) | Mensajes al mes |
|---|---|---|---|---|---|
| Desperdicio claro (pruebas, bloqueados, duplicados) | 0.21 M | 2.5 M | 4.9 % | 3.2 % | 3.4 M |
| Cortar en 30 días (apagar canal caro a leads, registrados, cross sell; limpiar; rehacer) | 0.94 M | 11.3 M | 22 % | 15 % | 19.2 M |
| Canal preferido | 0.34 M | 4.1 M | 8 % | 5 % | 3.7 M |
| Seguro (suma anterior) | 1.48 M | 17.8 M | 35 % | 23 % | |
| Recuperación a medir (apagar a churn, dormants, inactivos + sin respuesta 90 días) | 0.85 M | 10.2 M | 20 % | 13 % | 5.4 M |
| Total | 2.34 M | 28.0 M | 55 % | 36 % | 31.6 M |

Gasto anual de referencia: 50.8 M al ritmo de septiembre; 76.9 M al ritmo promedio (57.7 M entre 9 por 12).

Cortes: equipo PG 1.57, Marketing 0.50, Sales 0.18, Others 0.06, Collections 0.01 (pruebas). Canal email 1.11, WhatsApp 1.20. Producto KCash 1.20 (61 % de su promocional de septiembre, 1.97 M), KPay 1.09 (66 % de 1.65 M), otros 0.02. KCash es sobre todo cortar (0.67); KPay sobre todo recuperación (0.60).

Audiencia por nombre: recuperación = Churn, Dormant, Inactiv, Medium_active, Winback, Reactiv; activación = Lead, Anónimos, Registrad, NeverActive, NeverCash, Never, Rezagad, LeftFunnel, Nuevos, Prospect; activos = Recurrente, Active, Activo, Cliente, Eligible.

Limitaciones: (a) las proporciones de E9b son promedio de toda la base y se aplican a cada campaña; (b) respuesta en email = clic, si se contara apertura la palanca de email baja; (c) E7a no tiene mes, se usa la proporción del periodo; (d) duplicados es un mínimo; (e) no incluye costo fijo de Braze (X).

## 2. Otras cifras nuevas

- Grupo de control (E13): 22 Canvas con filas de control; 21 con 1 a 743 personas; uno real: Lending-KCash-20260201-B0301 Active-Retargeting_Installments_SP, 71,578 en control contra 871,744 (7.6 %), conversión 35.7 % control contra 27.0 % test, 83.9 % del control "abrió" algo.
- Sin dueño ni ticket (E2 por E1): 749 comunicaciones sin ticket (748 con team "Not Tracked"); 211 con envíos en 2026: 84.7 M mensajes (12.7 %) y 3.4 M MXN. Por tema (por nombre): transaccional u operativa 88 / 43.5 M / 2.1 M MXN; promocional 41 / 39.0 M / 1.3 M MXN; pruebas 82 / 2.2 M / 0.
- Acciones del Sheets v4 con costo de septiembre: Apagar 48 (48 activas, 20.2 M mensajes, 1.39 M MXN), Limpiar 56 (22, 1.6 M, 1.23 M), Rehacer 162 (62, 13.5 M, 0.24 M), Bajar frecuencia 84 (23, 4.7 M, 0.21 M), Confirmar 232 (0), Proteger 138 (50), Escalar 154 (45), No tocar 288 (117), Seguir igual 751 (113).
- Bajas de email: septiembre 36,639 personas (87,218 eventos); 77.2 % de los eventos de septiembre en campañas con acción (Apagar 33.5 %, Bajar frecuencia 28.6 %, Rehacer 15.1 %). E3: 8.4 M de 19.5 M con email suscrito.
- E17: 9.8 M WhatsApp a personas con bandera de baja de WhatsApp en el golden dataset (la bandera no es confiable).

## 3. Preguntas que no se pueden responder con los datos

- Lámina 92 (14.2 M sin respuesta, "¿qué temas o segmentos?"): no hay cruce persona sin respuesta por campaña o segmento. Se responde por canal (E7b) y con segmentos de E11 como aproximación. Extracción: E16 con campaña, segmento y etapa.
- Lámina 84 (Veriff): no se sabe de dónde salió el 22 % contra 17 % del equipo ni su definición.
- Si la recuperación de churn, dormants e inactivos recupera: solo con grupo de control.
- Cuántas bajas de email se evitarían: solo se sabe dónde ocurren.
- Costo fijo de Braze y si baja al excluir personas sin respuesta: contrato (X).
- Quién tiene app (para saber si churn y rezagados pueden recibir push e in-app).

## 4. Contradicciones nuevas

- La nota de campañas (muestra C) está desactualizada respecto a cómo se lee E1: su query descarta filas con `envios = 0`, que traen lecturas y entregas tardías. Afecta lectura y entrega de WhatsApp de varias campañas (B0171 Rezagada 57.7 % contra 61.5 %) y por tanto su señal y su acción. Las tablas de MUESTRA_C (50 apagar, 45 limpiar, 181 rehacer, 41 bajar frecuencia) ya no coinciden con el Sheets (48, 56, 162, 84). Usar el Sheets.
- MUESTRA_C dice "Cada envío cuesta 1 MXN se entregue o no" y "se pagaron X MXN de mensajes que no se entregaron" en la columna `por_que` de muchas campañas: contradice el supuesto de cobro por entregado.
- "Ninguno de los 3,228 Canvas tiene grupo de control": 22 tienen personas marcadas y uno tiene control real con resultado (control convirtió más que quien recibió).
- "Por producto el ahorro es mayor en KPay": con la cifra reconciliada KCash 1.20 contra KPay 1.09.
- Bandera de baja de WhatsApp del golden dataset (E17) marca como dados de baja a quienes recibieron 9.8 M WhatsApp.
