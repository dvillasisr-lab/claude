# Muestra F. Solapamiento: a quién le llegan varias campañas el mismo día (E6a y E6b)

Fuente: `data/e6a_solape_dia_mes.csv` (usuario-días por banda de familias distintas en el día, por mes) y `data/e6b_pares_familias.csv` (los 1,000 pares de familias que más coinciden el mismo día en el mismo usuario). Recibidas 14 oct 2026.

## Respuesta en una página

Tres de cada cuatro días en que un usuario recibe algo recibe una sola campaña. Pero el 9 % de los usuario-días con 3 o más campañas distintas concentra el 24 % de los mensajes, y cada mes entre 1.3 M y 2.3 M de usuarios viven al menos un día así. El solape no es entre equipos lejanos: el 62 % de las coincidencias es entre equipos distintos y el 65 % es promocional con promocional. Marketing con Marketing y Marketing con Sales son las parejas que más se pisan.

## E6a. Cuántas campañas distintas recibe un usuario en un día

| Campañas distintas en el día | Usuario-días | % usuario-días | % de los mensajes | Mensajes por usuario-día | Bajas por mil usuario-días |
|---|---|---|---|---|---|
| 1 | 325.1 M | 73.8 | 51.2 | 1.05 | 0.36 |
| 2 | 75.6 M | 17.2 | 24.4 | 2.15 | 0.38 |
| 3 a 4 | 32.8 M | 7.5 | 17.8 | 3.60 | 0.42 |
| 5 a 7 | 6.2 M | 1.4 | 5.8 | 6.15 | 0.47 |
| 8 o más | 0.5 M | 0.1 | 0.8 | 9.94 | 0.70 |

Usuarios con al menos un día de 3 o más campañas: enero 1.30 M, febrero 1.70 M, marzo 1.57 M, abril 1.43 M, mayo 1.89 M, junio 2.26 M, julio 1.70 M, agosto 2.09 M, septiembre 1.48 M. Mayo, junio y agosto son los meses de más solape (Hot Sale, lanzamiento de BillPay, regreso a clases).

Lectura con cuidado: la respuesta y la conversión por usuario-día suben con la banda, pero no porque mandar más funcione mejor. Los días de muchas campañas suelen ser días en que el usuario está en proceso (desembolso, pago, cobranza) y recibe transaccional más promocional. Lo que sí es limpio es la baja: por usuario-día se duplica de 0.36 a 0.70 por mil entre 1 campaña y 8 o más.

## E6b. Qué pares se pisan más

Por combinación de equipos (usuario-días con las dos campañas el mismo día):

| Equipos | Usuario-días |
|---|---|
| Marketing + Marketing | 27.6 M |
| Sales + Sales | 15.4 M |
| Marketing + Sales | 14.5 M |
| Lending (Product Growth) + Marketing | 9.0 M |
| Lending + Lending | 5.9 M |
| Lending + Sales | 5.1 M |

Los pares concretos que más pesan, promocional con promocional:

| Campaña A | Campaña B | Canales | Usuarios | Lectura |
|---|---|---|---|---|
| Marketing B0444 PushFelicitacionDiaPadres | Marketing B00527 Billpayments Onboarding | push + push | 1.54 M | Dos push de Marketing el mismo día a la misma gente |
| Marketing B00527 Billpayments Onboarding | QA-KPay-B001 ReminderRegistroTelefono | push + push | 1.45 M | Un Canvas de QA mandando a 1.45 M de usuarios reales |
| Lending B0440 AnotayGana | NewProducts T0000 BillPay Intro | push + push | 1.23 M | Dos lanzamientos de equipos distintos el mismo día |
| Marketing B0444 ReferralProgram | Marketing B0444 BAUMundial | push + push | 1.13 M | Mismo ticket, dos push |
| Sales B0491 AmazonHotSale | Sales B0493 HotSale KUESKIPROMO | push + push | 0.88 M | Dos ofertas de Hot Sale de Sales, 4 meses |
| Lending B0209 Recurrentes_Inactivos Descuento | Marketing B0326 Recurrentes_Dormants Referral | email + email | 0.40 M | Dos equipos persiguiendo a los mismos inactivos con ofertas distintas |
| Lending B0211 RegistradosPay Tasa0 | Marketing B0171 Anonimos RescateTasa0 | email/push + push | 0.12 M | Dos equipos con "tasa 0" al mismo usuario |
| Marketing B0495 Cuponera HotSale | Sales B0493 HotSale KUESKIPROMO | email + push | 0.53 M | Marketing y Sales con la misma promoción, 5 meses |

Y el mismo Canvas pegándose a sí mismo en dos versiones o dos canales:

| Canvas | Canales | Usuarios | Lectura |
|---|---|---|---|
| KCash-Loan-Application-disbursed 20240821 y 20251110 | email + email | 0.60 M | Dos versiones del mismo transaccional activas a la vez |
| Lending B0223 NeverActive InstallmentsNoCash | email + WhatsApp | 0.40 M | Email y WhatsApp el mismo día, tres meses |
| Lending B0333 Churn 12 meses | WhatsApp + WhatsApp | 0.30 M | Versiones del mismo WhatsApp de pago con 2 a 6 días de diferencia |
| Sales B0417 Comercio del día marzo | email + push | 0.34 M | |
| Sales B0493 HotSale KUESKIPROMO | push + push, push + WhatsApp | 0.45 M | |

## Gobernanza: pruebas y copias con audiencia real

En E1 hay 171 comunicaciones con "QA", "PRUEBA", "Copy of" o "test" en el nombre que sí enviaron: 7.26 M envíos a 5.9 M usuarios en el periodo. Las más grandes:

| Comunicación | Envíos | Usuarios |
|---|---|---|
| QA-KPay-20260811-B001 ReminderRegistroTelefono | 1,872,378 | 1,835,458 |
| QA_CC-More3k_29Jan26 | 942,374 | 714,254 |
| Copy of Lending-KPay-20260706-B0332 HardInactive | 724,434 | 264,081 |
| QA_CC | 644,635 | 633,536 |
| Copy of QA-Sales-KPay-20260518-B0490 AmazonPreHotSale | 377,467 | 368,077 |
| Copy of Marketing-KPay-20260121 Recurrentes-Performance | 363,791 | 364,382 |

Algunas pueden ser campañas reales mal nombradas (la de QA con 1.87 M parece una campaña de producción con prefijo equivocado). Hay que revisar una por una, pero en cualquier caso el nombre no permite saber qué es, y eso ya es un problema de gobernanza.

## Qué hacer

1. **Calendario único de envíos promocionales** entre Marketing, Sales y Product Growth, al menos para los push: hoy los tres mandan a las mismas bases el mismo día. Regla sugerida: máximo 2 campañas promocionales por usuario al día y 1 push promocional al día.
2. **Un solo dueño por audiencia fría**: inactivos y dormants los trabajan Lending (B0209, B0333, B0332) y Marketing (B0326) a la vez con ofertas distintas. Elegir una.
3. **Frequency cap en Braze** a nivel global: con tope de 1 push promocional al día se evitan de entrada los pares de la tabla.
4. **Revisar y archivar** los Canvas QA, PRUEBA y Copy of que siguen activos; renombrar los que sean producción.
5. **Apagar una de las dos versiones** del email de desembolso.

Lo que falta para cerrar este lente: E7b (a qué canal responde cada usuario) permite pasar de "no mandes dos push el mismo día" a "mándale por el canal que sí abre".
