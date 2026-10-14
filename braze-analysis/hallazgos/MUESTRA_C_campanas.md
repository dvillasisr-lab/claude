# Muestra del lente C: qué campañas y equipos tienen que eficientar

Periodo: enero a septiembre 2026 (9 meses completos). Fuente: `data/e1_comunicacion_mes_canal.csv` (E1). Query reproducible: `sql/muestra_c_campanas.sql`. Tabla completa: `hallazgos/muestra_c_familias.csv` (1,917 familias).

**Familia** = una comunicación sin la fecha del nombre. Las versiones mensuales de la misma Canvas (B0326 de enero, de febrero, de marzo) se juntan en una sola fila para juzgar la idea, no la versión.

## Respuesta en una página

De las 1,917 familias que enviaron algo, 331 cumplen las tres condiciones de "apagar o rehacer": volumen arriba de la mediana de su canal, conversión por mil envíos debajo de la mediana de su canal, y respuesta debajo del umbral mínimo (clic email < 0.5 %, apertura push < 1 %, lectura WhatsApp < 60 %, clic in-app < 10 %).

| Señal | Familias | Envíos | Costo variable MXN | Conversiones Cash | Qué significa |
|---|---|---|---|---|---|
| Apagar o rehacer | 331 | 312.7 M (47 %) | 27.5 M (38 %) | 239 mil (7 %) | Mucho volumen, poca respuesta, poca conversión |
| Revisar | 172 | 104.3 M | 23.7 M | 209 mil | Mucho volumen y poca conversión, pero la gente sí responde. Mensaje bien, oferta o audiencia mal |
| Escalar | 331 | 4.8 M | 0.9 M | 93 mil | Poco volumen y conversión al doble de la mediana. Ampliar audiencia |
| Sin señal | 1,083 | 245.6 M | 19.7 M | 2.84 M | Dentro de lo normal |

La mitad de los envíos del periodo sale de familias que casi no mueven resultados. Las 331 de "apagar o rehacer" generan 7 % de las conversiones con 47 % de los envíos.

## Por equipo

| Equipo | Familias a apagar o rehacer | Envíos | Costo variable MXN | Dónde está el problema |
|---|---|---|---|---|
| Marketing | 158 | 132.4 M | 9.6 M | 87 familias de push con 84 M envíos y apertura < 1 %; 10 familias de WhatsApp que cuestan 7.8 M MXN |
| Product Growth | 82 | 108.7 M | 14.6 M | 32 familias de email con 84 M envíos (Tasa0 a registrados, NeverActive); 23 de WhatsApp que cuestan 10.4 M MXN |
| Others | 16 | 36.0 M | 1.4 M | El envío de BillPay intro a 16 M usuarios en junio (clic 0.10 %) y WeeklyRecommendations |
| Collections | 9 | 22.9 M | 1.1 M | Buckets BKT1 a BKT3 por email. Ver nota: cobranza no se debe juzgar por conversión a préstamo |
| Sales | 66 | 12.7 M | 0.7 M | Muchas familias chicas de push e in-app |

Lo que sigue activo: 91 de las 331 familias enviaron en septiembre. Juntas mandan unos 29 M mensajes al mes y gastan unos 3.0 M MXN al mes en variable (Marketing 13.8 M mensajes y 1.1 M MXN; Product Growth 11.2 M mensajes y 1.7 M MXN; Collections 2.8 M mensajes). Ese es el ahorro mensual si se apagan hoy, antes de rehacer nada.

## El ejemplo que ya conoces: dormants referral (B0326)

La familia Marketing-B0326 Recurrentes_Dormants-ReferralProgram sale sola en el corte, en las dos versiones de producto:

| Versión | Canal | Envíos | Por mes | Respuesta | Conversiones | Conv por mil | Costo MXN | Señal |
|---|---|---|---|---|---|---|---|---|
| KPay | Email | 5.24 M | 650 mil | Clic 0.05 % | 1,154 | 0.22 | 262 mil | Apagar o rehacer |
| KCash | Email | 7.04 M | 880 mil | Clic 0.06 % | 3,694 | 0.52 | 352 mil | Apagar o rehacer |
| KPay | Push | 1.55 M | 190 mil | Apertura 0.34 % | 519 | 0.33 | 0 | Apagar o rehacer |
| KCash | Push | 1.88 M | 235 mil | Apertura 0.50 % | 1,990 | 1.06 | 0 | Apagar o rehacer |
| KPay | WhatsApp | 636 mil | 2 meses | Lectura 51.5 % | 379 | 0.60 | 636 mil | Apagar o rehacer (1,679 MXN por conversión) |
| KCash | WhatsApp | 839 mil | 2 meses | Lectura 61.1 % | 2,460 | 2.93 | 839 mil | Revisar |
| KPay | In-app | 108 mil | 4 meses | Clic 8.7 % | 907 | 8.42 | 0 | Normal |
| KCash | In-app | 175 mil | 4 meses | Clic 9.5 % | 3,760 | 21.47 | 0 | Normal |

Lectura: el email de dormants costó 614 mil MXN en 9 meses y convirtió 0.2 a 0.5 por cada mil envíos, 5 a 10 veces menos que la mediana de email (2.4 por mil). El in-app de la misma idea convirtió 21 por mil en KCash. La audiencia no es el problema, el canal sí. En los datos, el email sigue apareciendo con envíos hasta septiembre; si ya se apagó en octubre, aquí se verá en la extracción del mes parcial.

## Las 15 familias donde más dinero se recupera

Ordenadas por costo variable. Conv por mil = conversiones Cash por cada mil envíos. Mediana del canal: email 2.4, push 1.7, WhatsApp 4.5, in-app 15.9.

| Familia | Equipo | Canal | Envíos | Costo MXN | Conv por mil | Respuesta | Último mes |
|---|---|---|---|---|---|---|---|
| Marketing-KCash-B0171 Leads_BBDDRezagada-RescateTasa0 | Marketing | WhatsApp | 5.21 M | 5.21 M | 0.75 | Lectura 57.7 % | Sep |
| Lending-KCash-B0209 Recurrentes_Inactivos-DescuentoDirecto | Product Growth | WhatsApp | 2.32 M | 2.32 M | 2.15 | Lectura 59.8 % | Sep |
| Lending-KPay-B0333 Churn_12MesesInactividad-ConSinOferta | Product Growth | WhatsApp | 2.32 M | 2.32 M | 0.33 | Lectura 48.9 % | Sep |
| Lending-KCash-B0223 Nuevos_NeverActive-InstallmentsNoCash | Product Growth | WhatsApp | 1.85 M | 1.85 M | 0.08 | Lectura 50.8 % | Sep |
| Lending-KCash-B0211 Nuevos_RegistradosPay-Tasa0 | Product Growth | Email | 34.92 M | 1.75 M | 0.08 | Clic 0.25 % | Sep |
| NewProducts-Kueski-T0000 Portfolio_BillPay_Intro_Full_Rollout | Others | Email | 16.11 M | 806 mil | 0.11 | Clic 0.10 % | Jun (una vez) |
| Lending-KCash-B0223 Nuevos_NeverActive-InstallmentsNoCash | Product Growth | Email | 13.45 M | 673 mil | 0.02 | Clic 0.09 % | Sep |
| Marketing-KPay-B0326 Recurrentes_Dormants-ReferralProgram | Marketing | WhatsApp | 636 mil | 636 mil | 0.60 | Lectura 51.5 % | Mar |
| Marketing-KCash-B0171 Leads-BBDDHotLeadsW2RescateTasa0 | Marketing | WhatsApp | 635 mil | 635 mil | 2.62 | Lectura 58.8 % | Sep |
| Lending-KPay-B0332 HardInactive_6MesesInactividad-ConSinOferta | Product Growth | WhatsApp | 629 mil | 629 mil | 2.10 | Lectura 55.9 % | Ago |
| Lending-KCash-B0210 Nuevos_MPNeverCash-Tasa0 | Product Growth | WhatsApp | 512 mil | 512 mil | 1.73 | Lectura 52.4 % | Sep |
| Collections-KCash-T000 BKT1 | Collections | Email | 10.22 M | 511 mil | 1.81 | Clic 0.41 % | Sep (ver nota) |
| Lending-KCash-B0440 Recurrentes-AnotayGana-P4 | Product Growth | WhatsApp | 445 mil | 445 mil | 2.52 | Lectura 59.4 % | Jun |
| Marketing-KCash-B0326 Leads-ReferralProgram | Marketing | Email | 8.46 M | 423 mil | 0.37 | Clic 0.20 % | Jun |
| Lending-KCash-B0337 Leads_Eligibles-CuestaEnero | Product Growth | Email | 7.43 M | 371 mil | 0.28 | Clic 0.16 % | Feb |

Dos patrones se repiten:

1. **WhatsApp a bases frías** (rezagados, inactivos 6 y 12 meses, never active). Cuesta 1 MXN por mensaje, la mitad no se lee, y convierte menos que la mediana. Son 9 de las 15 familias y 15 M MXN. Aquí está el ahorro grande.
2. **Email masivo a registrados que nunca han tomado crédito** (RegistradosPay-Tasa0, NeverActive, Leads-Referral). Decenas de millones de envíos con clic de 0.1 a 0.25 % y conversión 20 veces debajo de la mediana. Casi no cuestan, pero son la mayor fuente de bajas: B0326 Leads email tiene 3.0 bajas por mil entregados y BillPay intro 2.6, contra 1.1 a 1.2 en el resto.

## Las que hay que escalar

Poco volumen y conversión al doble o más de la mediana del canal. Son candidatas a ampliar audiencia antes de inventar campañas nuevas.

| Familia | Equipo | Canal | Envíos | Conversiones | Conv por mil |
|---|---|---|---|---|---|
| Marketing-KPay-B0001 Recurrentes-RetargetingOffering | Marketing | Email | 64 mil | 4,424 | 68.6 |
| Lending-KPay-T2853 Nuevos-Onboarding | Product Growth | Email | 60 mil | 3,983 | 66.2 |
| Marketing-KCash-B0440 Leads_1erLoanKCash-AnotayGana | Marketing | Push | 37 mil | 3,539 | 95.8 |
| Marketing-KPay-B0001 Recurrentes-RetargetingOffering | Marketing | Push | 47 mil | 2,945 | 63.1 |
| Lending-KPay-B0184 ClienteKPayCompraEnTemu-XSellaKCash | Product Growth | Email | 113 mil | 2,568 | 22.7 |
| Marketing-KCash-B0326 Leads_1raCompraenKCash-ReferralProgram | Marketing | WhatsApp | 30 mil | 2,439 | 80.7 |
| Sales-KPay-B0434 Recurrentes-AdidasInstore | Sales | WhatsApp | 47 mil | 1,800 | 38.3 |

El patrón: audiencias con una acción reciente (compró en Temu, canceló una oferta, hizo su primera compra) convierten 10 a 40 veces más que las bases frías. El dinero de WhatsApp debería moverse de las bases frías a estas.

## Notas de lectura

- **Cobranza (Collections) no se juzga por conversión a préstamo.** BKT1 a BKT3 salen en "apagar" porque la métrica de resultado de E1 es `is_converted` (préstamo). Para cobranza el resultado es pago, que no está en la tabla. Se dejan en la lista para que se vea, pero la decisión necesita su propia métrica.
- **QA y pruebas** aparecen en Others con decenas de envíos. No pesan en dinero y se ignoran.
- **La señal es un semáforo, no una sentencia.** Una campaña de "apagar o rehacer" puede ser transaccional o regulatoria y tener que seguir. El dueño de cada familia confirma. Por eso la tabla completa trae equipo, ticket y último mes.
- **Conversión es solo Cash.** Para KPay el `is_converted` de la tabla no aplica, así que una campaña de KPay con conversión baja puede estar funcionando para compras. En KPay la señal útil es la respuesta (clic, apertura, lectura), que sí está en la tabla.

## Qué sigue para que esto sea un plan de acción

1. Mandar la tabla `muestra_c_familias.csv` filtrada por equipo a cada dueño, con tres columnas para que llenen: mantener, apagar, rehacer, y por qué.
2. Para las 91 activas en septiembre, calcular el ahorro mensual exacto con el mes de septiembre (ya está en E1).
3. Cruzar con E6 (solapamiento): si varias de estas familias le llegan al mismo usuario el mismo día, apagar una sube la respuesta de las demás.
4. Cruzar con E7 (segmentación): para cada familia, en qué etapa y qué canal sí responde, para rehacer con audiencia más chica en vez de apagar.
