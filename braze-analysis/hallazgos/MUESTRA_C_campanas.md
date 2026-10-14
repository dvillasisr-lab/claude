# Muestra del lente C: qué campañas y equipos tienen que eficientar

Periodo: enero a septiembre 2026 (9 meses completos). Fuente: `data/e1_comunicacion_mes_canal.csv` (E1). Query reproducible: `sql/muestra_c_campanas.sql`. Tabla completa: `hallazgos/muestra_c_familias.csv` (1,917 familias). Vista interactiva con filtros: `tablero/muestra_campanas.html` (publicada en https://claude.ai/code/artifact/1ad2c43e-0072-4e46-a27a-6e58fa8d0043).

**Familia** = una comunicación sin la fecha del nombre. Las versiones mensuales de la misma Canvas (B0326 de enero, de febrero, de marzo) se juntan en una sola fila para juzgar la idea, no la versión.

**La señal usa métricas de comunicación, no conversión.** Por decisión del usuario, el evento de conversión es poco confiable y solo aplica a Cash, así que queda como columna de referencia. Respuesta = clic en email (sobre entregados), apertura en push (sobre enviados), lectura en WhatsApp (sobre entregados), clic en in-app (sobre impresiones).

| Señal | Regla |
|---|---|
| Apagar o rehacer | Envíos iguales o mayores a la mediana de su canal, y respuesta debajo del mínimo: email clic < 0.3 %, push apertura < 0.75 %, WhatsApp lectura < 60 %, in-app clic < 10 % |
| Revisar | Envíos arriba de la mediana y respuesta debajo de la mediana del canal, o email con 2.5 o más bajas por mil entregados. La columna motivo dice cuál |
| Proteger | Envíos arriba de la mediana y respuesta 1.5 veces la mediana o más |
| Escalar | Envíos debajo de la mediana (y al menos 1,000), respuesta al doble de la mediana o más |

Medianas de respuesta del periodo: email 0.50 %, push 1.07 %, WhatsApp 64.5 %, in-app 18.2 %. Las familias se marcan también por tipo: cobranza (Collections), transaccional u operativa (nombre fuera de la convención de ticket) y promocional o lifecycle. Las dos primeras no se apagan por respuesta baja.

## Respuesta en una página

| Señal | Familias | Envíos | Costo variable MXN | Qué significa |
|---|---|---|---|---|
| Apagar o rehacer | 356 | 293.1 M (44 %) | 29.8 M (41 %) | Mucho volumen y la gente no responde |
| Revisar | 227 | 135.4 M (20 %) | 11.4 M (16 %) | Mucho volumen y respuesta floja, o bajas altas |
| Proteger | 196 | 121.4 M (18 %) | 2.9 M (4 %) | Mucho volumen y la gente sí responde. No tocar |
| Escalar | 186 | 4.2 M (1 %) | 0.1 M | Poco volumen y respuesta al doble. Ampliar audiencia |
| Sin señal | 952 | 113.3 M (17 %) | 27.8 M (39 %) | Dentro de lo normal |

Solo promocionales o lifecycle (quitando cobranza y transaccionales): 340 familias a apagar o rehacer con 276.9 M envíos y 29.1 M MXN. De esas, 89 seguían activas en septiembre y juntas mandan unos 28 M mensajes y gastan unos 3.2 M MXN al mes. Ese es el ahorro mensual si se apagan hoy, antes de rehacer nada.

## Ahorro potencial

| Concepto | Cómo se calcula | Total | Product Growth | Marketing | Sales | Others |
|---|---|---|---|---|---|---|
| Ahorro al mes si se apagan hoy | Costo variable mensual de las familias "apagar o rehacer" promocionales que enviaron en septiembre (89 familias) | 3.2 M MXN y 28 M mensajes menos al mes | 1.9 M MXN | 1.1 M MXN | 0.1 M MXN | 0.04 M MXN |
| Lo que costaron en el periodo | Costo variable de las 340 familias promocionales "apagar o rehacer" en 9 meses | 29.1 M MXN | 15.1 M | 10.9 M | 1.8 M | 1.4 M |
| WhatsApp no entregado | Envíos de WhatsApp sin entrega × 1 MXN, en cualquier señal. Se recupera limpiando números, sin apagar nada | 14.3 M MXN en 9 meses (1.6 M al mes) | 4.5 M | 8.0 M | 1.5 M | 0.04 M |

Casi todo el ahorro en dinero está en WhatsApp: las 5 familias con más ahorro mensual son WhatsApp a bases frías (B0171 rezagados 868 mil MXN al mes, B0333 churn 12 meses 331 mil, B0209 inactivos 258 mil, B0223 never active 206 mil) y el email B0211 RegistradosPay-Tasa0 (194 mil MXN y 3.9 M emails al mes). Push no ahorra dinero pero sí mensajes: 31 M push al mes a gente que no los abre. Falta sumar el costo fijo de Braze por mensaje cuando se tenga el contrato; con eso el ahorro de push y de email sube.

## Por equipo (solo promocionales o lifecycle, señal apagar o rehacer)

| Equipo | Familias | Envíos | Costo MXN | Activas en sep | Msgs al mes de las activas | MXN al mes de las activas | Dónde está el problema |
|---|---|---|---|---|---|---|---|
| Marketing | 151 | 110.4 M | 10.9 M | 33 | 12.1 M | 1.1 M | 71 familias de push con 59 M envíos y apertura < 0.75 %; 46 de email con 39 M envíos; 13 de WhatsApp que cuestan 8.9 M MXN |
| Product Growth | 79 | 103.8 M | 15.1 M | 35 | 10.7 M | 1.9 M | 29 familias de email con 81 M envíos (Tasa0 a registrados, NeverActive); 29 de WhatsApp que cuestan 11.0 M MXN |
| Sales | 98 | 29.3 M | 1.8 M | 20 | 4.7 M | 0.1 M | 28 familias de email (20 M) y 32 de push (6 M), muchas chicas |
| Others | 12 | 33.4 M | 1.4 M | 1 | 0.8 M | 0.04 M | BillPay intro por email a 16 M usuarios en junio (clic 0.10 %) y sus push |

Collections tiene 8 familias en "apagar" (BKT1 a BKT3 por email, 12.6 M envíos) pero su resultado es pago, no está en la tabla, y no se juzga aquí.

## El ejemplo que ya conoces: dormants referral (B0326)

| Versión | Canal | Envíos | Por mes | Respuesta | Bajas por mil | Conv. ref. por mil | Costo MXN | Señal |
|---|---|---|---|---|---|---|---|---|
| KPay | Email | 5.24 M | 654 mil | Clic 0.05 % | 1.56 | 0.22 | 262 mil | Apagar o rehacer |
| KCash | Email | 7.04 M | 880 mil | Clic 0.06 % | 1.20 | 0.52 | 352 mil | Apagar o rehacer |
| KPay | Push | 1.55 M | 194 mil | Apertura 0.34 % | | 0.33 | 0 | Apagar o rehacer |
| KCash | Push | 1.88 M | 235 mil | Apertura 0.50 % | | 1.06 | 0 | Apagar o rehacer |
| KPay | WhatsApp | 636 mil | 318 mil (2 meses) | Lectura 51.5 % | | 0.60 | 636 mil | Apagar o rehacer |
| KCash | WhatsApp | 839 mil | 420 mil (2 meses) | Lectura 61.1 % | | 2.93 | 839 mil | Revisar |
| KPay | In-app | 108 mil | 27 mil | Clic 8.7 % | | 8.42 | 0 | Apagar o rehacer |
| KCash | In-app | 175 mil | 44 mil | Clic 9.5 % | | 21.47 | 0 | Apagar o rehacer |

Lectura: el email de dormants tuvo clic de 0.05 a 0.06 %, diez veces menos que la mediana de email (0.50 %), y costó 614 mil MXN en 9 meses. La señal lo marca sin necesidad de conversión. En los datos sigue apareciendo con envíos hasta septiembre; si se apagó en octubre, se verá en la extracción del mes parcial.

## Las 15 familias donde más dinero se recupera (apagar o rehacer, por costo)

| Familia | Equipo | Canal | Envíos | Costo MXN | Respuesta | Entrega | Bajas por mil | Último mes |
|---|---|---|---|---|---|---|---|---|
| Marketing-KCash-B0171 Leads_BBDDRezagada-RescateTasa0 | Marketing | WhatsApp | 5.21 M | 5.21 M | Lectura 57.7 % | 62.8 % | | Sep |
| Lending-KCash-B0209 Recurrentes_Inactivos-DescuentoDirecto | Product Growth | WhatsApp | 2.32 M | 2.32 M | Lectura 59.8 % | 63.5 % | | Sep |
| Lending-KPay-B0333 Churn_12MesesInactividad-ConSinOferta | Product Growth | WhatsApp | 2.32 M | 2.32 M | Lectura 48.9 % | 73.8 % | | Sep |
| Lending-KCash-B0223 Nuevos_NeverActive-InstallmentsNoCash | Product Growth | WhatsApp | 1.85 M | 1.85 M | Lectura 50.8 % | 52.1 % | | Sep |
| Lending-KCash-B0211 Nuevos_RegistradosPay-Tasa0 | Product Growth | Email | 34.92 M | 1.75 M | Clic 0.25 % | 94.6 % | 1.10 | Sep |
| NewProducts-Kueski-T0000 Portfolio_BillPay_Intro_Full_Rollout | Others | Email | 16.11 M | 806 mil | Clic 0.10 % | 88.9 % | 2.60 | Jun (una vez) |
| Lending-KCash-B0223 Nuevos_NeverActive-InstallmentsNoCash | Product Growth | Email | 13.45 M | 673 mil | Clic 0.09 % | 93.3 % | 0.99 | Sep |
| Marketing-KPay-B0326 Recurrentes_Dormants-ReferralProgram | Marketing | WhatsApp | 636 mil | 636 mil | Lectura 51.5 % | 69.1 % | | Mar |
| Marketing-KCash-B0171 Leads-BBDDHotLeadsW2RescateTasa0 | Marketing | WhatsApp | 635 mil | 635 mil | Lectura 58.8 % | 69.0 % | | Sep |
| Lending-KPay-B0332 HardInactive_6MesesInactividad-ConSinOferta | Product Growth | WhatsApp | 629 mil | 629 mil | Lectura 55.9 % | 82.4 % | | Ago |
| Marketing-KPay-B0252 Recurrentes-LanzamientoPalaciodeHierro | Marketing | WhatsApp | 620 mil | 620 mil | Lectura 57.6 % | 77.1 % | | Abr (una vez) |
| Lending-KCash-B0210 Nuevos_MPNeverCash-Tasa0 | Product Growth | WhatsApp | 512 mil | 512 mil | Lectura 52.4 % | 83.4 % | | Sep |
| Lending-KCash-B0440 Recurrentes-AnotayGana-P4 | Product Growth | WhatsApp | 445 mil | 445 mil | Lectura 59.4 % | 66.4 % | | Jun |
| Marketing-KCash-B0326 Leads-ReferralProgram | Marketing | Email | 8.46 M | 423 mil | Clic 0.20 % | 95.6 % | 3.03 | Jun |
| Marketing-KCash-B0391 Leads_BDDMarketing-RescateFinesDeSemana | Marketing | Push | 13.38 M | 0 | Apertura 0.76 % | | | Sep |

Los push más grandes con apertura debajo de 0.75 %: B0171 Anonimos-RescateTasa0 (8.9 M, 0.55 %), B0326 Leads-ReferralProgram (6.4 M, 0.52 %), B0171 Leads_BBDDRezagada-RescateTasa0 (5.8 M, 0.55 %), B0211 RegistradosPay-Tasa0 (5.1 M, 0.48 %), BillPay Reminder (4.8 M, 0.65 %). No cuestan, pero son 31 M push a gente que no los abre.

Dos patrones se repiten:

1. **WhatsApp a bases frías** (rezagados, inactivos 6 y 12 meses, never active). Cuesta 1 MXN por mensaje, entre un cuarto y la mitad no se entrega, y de lo entregado se lee menos del 60 %. Son 11 de las 15 familias y 16 M MXN. Aquí está el ahorro grande.
2. **Email masivo a registrados que nunca han tomado crédito** (RegistradosPay-Tasa0, NeverActive, Leads-Referral, BillPay intro). Decenas de millones de envíos con clic de 0.1 a 0.25 %. Casi no cuestan, pero son la mayor fuente de bajas: B0326 Leads email tiene 3.0 bajas por mil entregados y BillPay intro 2.6, contra 1.1 a 1.2 en el resto.

## Bajas altas con buena respuesta (señal revisar, motivo bajas altas)

33 familias de email con 35.6 M envíos responden bien pero queman base: Retargeting_Veriff (9.7 M envíos, clic 3.0 %, 3.9 bajas por mil), Retargeting_PersonalInfo (2.7 M, clic 3.0 %, 4.6 bajas por mil), Eligibles-Christmas (2.5 M, 5.8 bajas por mil), NarrativaTasa0 (5.1 M, 4.9 bajas por mil). Aquí la acción no es apagar sino bajar frecuencia.

## Las que hay que proteger y las que hay que escalar

Proteger (volumen alto y respuesta 1.5 veces la mediana): 152 familias promocionales con 63 M envíos. Las más grandes son transaccionales (confirmación de pago KPay, contratos, dispersión) y cobranza (Precobranza email 4.3 % clic, push 5.3 % apertura). Promocionales grandes que funcionan: Lending-KCash-B0301 Active-Retargeting_Installments_SP email (3.4 M, clic 2.8 %), Marketing-KCash-B0326 ClienteKCashCompraKCash push (2.9 M, apertura 2.4 %), Retargeting_Veriff push (2.9 M, apertura 5.8 %).

Escalar (poco volumen, respuesta al doble): Lending-KCash-B0154 Tardan45días email (114 mil, clic 3.9 %), Lending-KPay-B0184 CompraEnTemu-XSellaKCash push (75 mil, apertura 3.3 %), Marketing-KPay-B0001 RetargetingOffering-Canceló push (71 mil, apertura 9.5 %), Lending-KCash-B0229 AniversarioPares email (109 mil, clic 1.8 %). El patrón: audiencias con una acción reciente responden 3 a 10 veces más que las bases frías. El dinero de WhatsApp debería moverse de las bases frías a estas.

## Notas de lectura

- **Cobranza no se juzga aquí.** La tabla no tiene pago. BKT1 a BKT3 se ven en la lista con tipo cobranza para que no se pierdan, pero la decisión necesita su propia métrica.
- **Transaccionales y operativas** (confirmaciones, contratos, dispersión, cobro fallido) se marcan por tipo y no se apagan por respuesta baja.
- **La señal es un semáforo, no una sentencia.** El dueño de cada familia confirma. Por eso la tabla trae equipo, ticket, audiencia y último mes.
- **Conversión solo de referencia.** Se deja porque sirve para ordenar dentro de una señal, no para decidirla.

## Qué sigue para que esto sea un plan de acción

1. Filtrar la vista por equipo y mandarla a cada dueño, con tres columnas para que llenen: mantener, apagar, rehacer, y por qué.
2. Para las 89 activas en septiembre, calcular el ahorro mensual exacto con el mes de septiembre (ya está en E1).
3. Cruzar con E6 (solapamiento): si varias de estas familias le llegan al mismo usuario el mismo día, apagar una sube la respuesta de las demás.
4. Cruzar con E7 (segmentación): para cada familia, en qué etapa y qué canal sí responde, para rehacer con audiencia más chica en vez de apagar.
