# Parte 4: secciones VI y VII (láminas 45 a 63). Notas de cálculo

Scripts (scratchpad, no en el repo): `v6parts/p4work/p4_calc.py` (grupos de audiencia y programas de recuperación), `p4work/p4_app.py` (alcance de push e in-app por grupo), `p4work/p4_calc3.py` (bloqueados, dados de baja, ventanas, push por tema, ejemplos por tema). Salidas: `p4work/out1.txt`, `out3.txt`, `out_l.txt`, `programas_recuperacion.csv`, `programas_ticket.csv`.

Costo en todo: email 0.05 MXN por enviado + WhatsApp 1 MXN por entregado (no la columna costo_mxn de E1 ni de muestra_c, que cobran WhatsApp por enviado). Total que da: 57.66 M MXN, cuadra con el deck.

## 1. Cifras nuevas y cómo salen

### Grupos de audiencia por el nombre de la campaña (E1)
Regla en orden: cobranza (Collections, cobranza, BKT); transaccional (Transaccional, payment, contracts, disbursed); activos si dice MPNeverCash o PortafolioActivoEInactivo; **ex clientes inactivos** (Dormant, Inactiv, Churn, Lazaro, Softnactive); **leads que nunca activaron** (Rezagad, Never, Anonim, HotLead); leads y registrados recientes (Leads, Registrad, Prospect, LeftFunnel); nuevos y onboarding (Nuevos, Onboarding, 1er, 1ra, Welcome); activos y recurrentes (Recurrente, Active, Activo, Cliente); resto "todos y otros". Es la regla de la muestra G pero separa ex cliente de lead, como pidió el usuario.

| Grupo | Mensajes | % msgs | Costo MXN | % costo | Conv. mismo día | % conv | MXN por conv |
|---|---|---|---|---|---|---|---|
| Activos y recurrentes | 170.5 M | 25.6 | 15.37 M | 26.7 | 1.53 M | 45.2 | 10 |
| Leads y registrados recientes | 183.2 M | 27.4 | 11.72 M | 20.3 | 245 mil | 7.2 | 48 |
| Leads que nunca activaron | 77.2 M | 11.6 | 15.19 M | 26.3 | 53.0 mil | 1.6 | 287 |
| Ex clientes inactivos | 54.5 M | 8.2 | 7.83 M | 13.6 | 73.7 mil | 2.2 | 106 |
| Nuevos y onboarding | 10.4 M | 1.6 | 0.95 M | 1.7 | 57.7 mil | 1.7 | 17 |
| Cobranza | 45.0 M | 6.7 | 1.63 M | 2.8 | 269 mil | 7.9 | 6 |
| Transaccional | 42.7 M | 6.4 | 1.71 M | 3.0 | 801 mil | 23.7 | 2 |
| Todos y otros | 83.9 M | 12.6 | 3.25 M | 5.6 | 354 mil | 10.5 | 9 |

Ex clientes + leads que nunca activaron: 131.7 M mensajes (19.7 %), 23.0 M MXN (39.9 %), 126.6 mil conversiones (3.7 %). WhatsApp entregado a esos dos grupos: 19.65 M de 40.99 M (47.9 %).
Conversión del mismo día = `conversiones_fraccional` de E1 (la conversión del usuario-día se reparte entre las comunicaciones de ese día). Es referencia.

Por canal (respuesta, MXN por conversión del mismo día):
- Ex clientes: email 0.27 % clic, 74 MXN; WhatsApp 57.9 % lectura, 71 % entrega, 468 MXN; push 0.95 %; in-app 13.4 %, 26 mil conv.
- Leads que nunca activaron: email 0.64 %, 5.9 bajas por mil, 289 MXN; WhatsApp 68.6 %, 68 % entrega, 546 MXN; push 0.72 %; in-app 26.6 %.
- Leads recientes: email 66 MXN, WhatsApp 143 MXN. Activos: WhatsApp 16.5 conv por mil.

### Programas de recuperación (E1 + muestra_m de E9a)
MXN por conversión del mismo día, por recencia: 30 a 90 días (B0208) 6; 3 meses (B0331) 50; 6 meses (B0332, B0206 y la variante 202600903) 107; 12 meses (B0333, B0207) 590; inactivos sin plazo (B0209) 83; dormants referidos (B0326 KCash y KPay) 108; rescate Tasa 0 a leads (B0171) 262; never active (B0223) 2,004. B0333 solo: 666. WhatsApp de B0333: 2,244 MXN por conversión; de B0171: 509; de B0209: 297 (email de B0209: 70).
Quien abre contra quien no, totales por grupo y canal (por persona-día): ex clientes email 3.3 % contra 1.0 % a 7 días y 13.1 % contra 5.9 % a 90; push 11.5/2.8 y 34.7/14.7; WhatsApp 2.2/0.8 y 9.7/5.1. Leads que nunca activaron: email 0.42/0.25 y 1.88/1.44 (B0171 email: 0.93 veces a 90 días, quien abre convierte menos); push 7.5/1.1 y 17.1/4.3 (4.0 veces a 90 días); WhatsApp 1.6/0.5 y 5.6/2.6.
Control (e13): de 673 Canvas con nombre de recuperación, 7 tienen grupo de control, todos B0171, con 134 personas en total. Ningún Canvas de ex clientes tiene control. (La versión anterior decía "B0326 Dormants tiene 2 en control": ese Canvas es B0326 Recurrentes_Todos, no Dormants.)

### Quién tiene app (E7b, E9b, E4a, E1)
- Abrió al menos un push: 1,153,171 personas en 9 meses (5.9 % de 19.5 M); 646,431 en 90 días (9.1 % de 7.07 M).
- Abrió push o hizo clic en in-app: 3,176,876 (16.3 %) y 1,992,617 (28.2 %). Estas personas son 92 % y 88 % de las personas con conversión.
- Quien no responde a nada: 0.02 vistas de in-app y 3 push por persona; quien responde: 5.27 y 39.5.
- E4a: push llega a 1.50 a 2.28 M personas al mes; in-app se ve por 0.80 a 1.18 M; email 4.5 a 5.2 M (junio 17.6 M por BillPay).
- E1, campañas con email y push el mismo mes, por cada 100 que reciben el email: activos 60 a 68 reciben push, 24 a 30 ven in-app, 3.7 abren push; ex clientes 32 a 34, 9 a 11, 0.8 a 0.9; leads que nunca activaron 31, 3, 0.6; leads recientes 34 a 37, 9 a 10, 1.2; nuevos 20, 7, 1.7. Usuarios aproximados sumados entre campañas: sirve como razón, no como conteo.

### Bloqueados (E7a)
KPay congelado: 56.6 M envíos, 43.35 M promocionales. Por equipo: Marketing 16.5 M, Sales 12.8 M, Product Growth 11.3 M, NewProducts 1.6 M, Shopping 0.5 M, QA 0.2 M. Por tema: descuento o cupón 16.1 M, referidos 7.3 M, lanzamientos 5.7 M, recordatorio 2.4 M, Tasa 0 1.9 M, otro 9.0 M. Por producto ofrecido: KPay 30.1 M, KCash 9.8 M. Por canal: push 22.0 M, email 14.5 M, WhatsApp 3.8 M enviados, in-app 3.0 M. Personas (E3): 552 mil, 105 mensajes cada una, 20.9 % con conversión.
REUS o ARCO: 249 mil promocionales (Product Growth 97 mil, Shopping 58 mil, Sales 51 mil, Marketing 26 mil); 34 mil por WhatsApp. Lista negra: 146 mil (Sales 58 mil, Product Growth 40 mil, Marketing 37 mil, QA 9 mil).
Exclusión mínima (promociones de KPay a congelados + REUS, ARCO y lista negra): 30.5 M. Con KCash: 43.8 M.

### Dados de baja (E5b)
Promocional 79.3 mil: Tasa 0 35.1 mil, lanzamientos y newsletters 11.3 mil, referidos 11.1 mil, descuentos 9.7 mil, recordatorio 7.1 mil.

### Ventanas de 7 y 90 días (muestra_m)
Promocionales con muestra: 779; "solo adelanta" (1.5 veces o más a 7 días y menos de 1.5 a 90): 199, con 69.4 M de 525.4 M personas-día. Por equipo, parte del volumen que solo adelanta: Sales 25.9 %, Marketing 14.4 %, Product Growth 8.4 %. Por tema: recordatorio 43.9 %, otros temas 5 a 14 %, Tasa 0 5.4 % (Tasa 0: 2.0 veces a 90 días, pero 10.4 % de conversión entre quienes abren). De 7 a 90 días la conversión de quien no abre se multiplica por 4.1 a 4.7 y la de quien abre por 2.5 a 3.4 (medianas por canal).

### Push por tema dentro del mismo grupo (E1)
Leads y registrados recientes: recordatorio 6.03 %, referidos 0.86 %, descuentos 0.73 %, lanzamientos 0.64 %, Tasa 0 0.48 %. Activos: recordatorio 10.39 %, Tasa 0 1.63 %, referidos 1.68 %, descuentos 1.35 %, lanzamientos 1.11 %. Nuevos: recordatorio 12.08 %.

### Bajas por tema (muestra_l)
Nuevos: BillPay 31 %, recordatorio de registro (Veriff, PersonalInfo, NIP, AccountCreation, NIP con cupón) 24.5 %, Tasa 0 17 %. Base vieja: Tasa 0 25 %, referidos 18 %, descuentos 13.5 %, lanzamientos 9.9 %, never active 6.2 %. Ex clientes que se fueron con correos de recuperación: B0209 6,602 y B0326 Dormants KCash 5,063.
Bajas por antigüedad (E12, email, por mil enviados): menos de 1 mes 2.98; 1 a 3 meses 3.58; 3 a 6 3.34; 6 a 12 3.46; 1 a 2 años 3.45; más de 2 años 3.12.

### Patrones de respuesta (E7b)
2 o más canales: 2.21 M personas (11.3 %), 86.4 % de las personas con conversión, 51.7 % de los mensajes. Quien responde a email: 1.37 M (7.0 %), 9.9 % de baja, 30.9 % de las bajas. Quien no responde a nada: 202 mil bajas, 46 % del total.

## 2. Preguntas que no se pueden responder con los datos de hoy

1. **Lámina 46, qué segmentos son el 73 %.** Ninguna extracción cruza el patrón de respuesta por persona con su segmento. Extracción E7d: E7b agregando la audiencia del último Canvas que tocó a la persona, la etapa del golden dataset y los meses desde su último crédito (para separar dormant, churn, inactivo y lead que nunca activó). Con eso también sale el tema que más responde por patrón (lámina 54).
2. **Cuánto recupera de verdad cada programa.** Sin grupo de control en ningún Canvas de ex clientes. Lo que hay es conversión del mismo día y quien abre contra quien no (con sesgo: quien abre ya era más activo). Hace falta un control de 10 % por programa.
3. **Quién tiene app.** Solo hay piso (abrió push o clic en in-app) y techo (le llegó push). Falta: atributo diario de app instalada, último login en app y push habilitado; y E18c (tipo de celular con `braze.int_communications_joined`). with_app y app_uninstall del golden dataset no son confiables (push a desinstalados abre 1.52 %).
4. **Por qué está congelada la línea KPay.** cc_freeze no trae causa; confirmar con Riesgo si las promociones de KCash a esas personas proceden.
5. **Costo del WhatsApp a bloqueados.** E7a no trae entrega; 3.8 M enviados es techo.
6. **Copy exacto de los mensajes.** No hay texto en los datos; los ejemplos describen el tema por el nombre de la campaña.

## 3. Contradicciones nuevas o cambios contra el guion v6

1. **WhatsApp a bases frías:** el guion decía 23 M MXN y un tercio del WhatsApp (muestra G: juntaba ex clientes y leads y cobraba por enviado). Con WhatsApp por entregado: 19.6 M MXN, 48 % de 41.0 M.
2. **Personas con KPay congelado:** 552 mil (E3, personas únicas) contra 4.4 M del análisis del playbook (suma de E17 por canal y equipo, cuenta repetido).
3. **Etapa "7.Prospects" del golden dataset:** 706 mil personas con 273 mensajes cada una y 41.6 % con conversión en el periodo (E3). No cuadra con "prospecto sin crédito". El guion v6 decía "Prospectos sin crédito: 189 M envíos y 0.27 % de clic": lo quité de la lámina 51 y uso los grupos por nombre. Hay que preguntar a Datos qué fecha y qué regla usa la etapa.
4. **Grupo de control de Dormants:** el guion decía que B0326 Dormants tenía 2 personas en control; es B0326 Recurrentes_Todos. Los únicos Canvas de recuperación con control son 7 del B0171 (134 personas).
5. **costo_mxn de muestra_c_familias.csv** cobra WhatsApp por enviado (B0171 WhatsApp: 5.21 M MXN por 5.21 M enviados). Todo lo de esta parte se recalculó por entregado.
6. **Nuevos se dan de baja más:** se mantiene la explicación (6.9 por mil en campañas a nuevos por nombre contra 3.0 a 3.6 por antigüedad). Las dos son ciertas: lo que sube la baja son las campañas de registro.
7. **"Push después de una acción, 6 % contra 2 %"** (lámina 56) viene del análisis v1 (CU-08) y no se pudo recalcular con las extracciones actuales.
