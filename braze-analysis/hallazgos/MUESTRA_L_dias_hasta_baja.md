# Muestra L. En cuántos días se dan de baja y cuántos emails recibieron antes (E8, versión 3)

Fuente: `data/e8_dias_hasta_baja.csv` (163 filas, 4 bloques: resumen, banda_dias, banda_emails, familia_dia_baja). Para cada usuario que se dio de baja de email: días entre su primer email entregado y la baja, emails y familias distintas que recibió hasta la baja, y qué familia le llegó el día de la baja. Agregado, sin identificadores. Cálculo de apoyo en `hallazgos/muestra_l_familias_baja.csv` (familias con equipo, tipo y producto del catálogo).

Dos cohortes. **Cohorte limpia (nuevos)** = su primer email fue de febrero en adelante, así que el conteo de días y emails es real. **Cohorte 0 (ya recibían en enero)** = la historia empieza el 1 de enero, así que sus días y emails son un piso, no la cifra real.

**Cobertura.** La versión 3 encontró 400,821 bajas (158,520 nuevos y 242,301 de la cohorte 0), 91 % de los 439,269 usuarios únicos que se dieron de baja en el periodo (E5 y E7b coinciden en esa cifra; los 457,376 de la vista de canales cuentan usuario por mes, y 18 mil usuarios se dieron de baja en más de un mes). El 9 % restante son usuarios cuya baja no tiene un email entregado antes dentro del periodo (por ejemplo solo envíos rebotados). La versión 1 solo encontraba 115 mil porque pedía entrega en la misma fila de la baja; los porcentajes de esa versión quedaron sustituidos por estos.

**Cómo leer "familia del día de la baja".** Es la familia que le llegó el último día con email entregado antes de la baja o el mismo día. Si ese día recibió dos familias, cuenta en las dos; por eso la suma por familia da 104 % en nuevos y 99 % en la cohorte 0 (el 1 % faltante son familias con menos de 500 bajas, que la query no lista).

## Lo que dice (nuevos, 158,520 usuarios)

| | Días hasta la baja | Emails antes de la baja | Familias distintas |
|---|---|---|---|
| Promedio | 43.3 | 9.7 | 4.2 |
| Mediana | 27 | 5 | |
| p90 | 112 | | |

| Días desde el primer email | Usuarios | % | Emails recibidos (promedio) |
|---|---|---|---|
| Mismo día | 11,742 | 7.4 % | 1.6 |
| 1 a 7 | 37,752 | 23.8 % | 4.4 |
| 8 a 30 | 34,897 | 22.0 % | 6.5 |
| 31 a 90 | 50,958 | 32.1 % | 9.1 |
| 91 a 180 | 19,849 | 12.5 % | 26.2 |
| 181 o más | 3,322 | 2.1 % | 41.2 |

| Emails antes de la baja | Usuarios | % | Días hasta la baja (mediana) |
|---|---|---|---|
| 1 | 52,533 | 33.1 % | 22 |
| 2 a 3 | 18,936 | 11.9 % | 3 |
| 4 a 10 | 40,649 | 25.6 % | 10 |
| 11 a 30 | 35,034 | 22.1 % | 54 |
| 31 o más | 11,368 | 7.2 % | 126 |

- **Uno de cada tres se da de baja con el primer email que recibe** (33 %). La mayoría de ellos son los que recibieron el email masivo de BillPay de junio como primer o segundo email: por eso la mediana de días en ese grupo es 22 y no 0 (el email llegó y la baja se registró días después, sin otro email entregado en medio).
- **La mitad se va en el primer mes** (31 % en la primera semana, 53 % en los primeros 30 días) y 85 % antes de los 90 días. Quien se va en la primera semana recibió 4.4 emails en esos días.
- **Se van después de 5 emails (mediana)**. Quien aguanta más de 90 días ya recibió 26 a 41 emails de 11 a 15 familias distintas: es el cansancio lento.

| Familia del día de la baja | Usuarios | % de las bajas de nuevos | Días (mediana) | Emails antes (promedio) |
|---|---|---|---|---|
| NewProducts-Kueski-T0000-E-Portfolio_BillPay_Intro_Full_Rollout | 49,314 | 31 % | 35 | 1.8 |
| Marketing-KCash-B0000-CANVAS-Leads_LeftFunnel-Retargeting_Veriff | 22,577 | 14 % | 4 | 7.9 |
| Marketing-KCash-B0000-CANVAS-Leads_LeftFunnel-Retargeting_PersonalInfo | 8,836 | 5.6 % | 3 | 4.9 |
| Lending-KCash-B0211-CANVAS-Nuevos_RegistradosPay-Tasa0-N/A | 7,351 | 4.6 % | 92 | 18.1 |
| KCash Rechazo transaccional FraudRisk | 6,469 | 4.1 % | 2 | 8.4 |
| Marketing-KCash-B0171-CANVAS-Leads-BBDDHotLeadsW1RescateTasa0-N/A | 5,165 | 3.3 % | 29 | 13.7 |
| Marketing-KCash-B0171-CANVAS-Leads_BBDDRezagada-RescateTasa0-N/A | 5,079 | 3.2 % | 93 | 18.5 |
| Marketing-KCash-B0171-CANVAS-Leads_BBDDHotLeadsW1-RescateTasa0-N/A | 3,124 | 2.0 % | 29 | 11.0 |
| Marketing-KCash-B0301-CANVAS-Active-NuevosRetargeting_Installments_SP | 2,978 | 1.9 % | 5 | 10.5 |
| Marketing-KCash-B0000-CANVAS-Leads_LeftFunnel-Retargeting_NIP | 2,672 | 1.7 % | 3 | 6.8 |
| Lending-KCash-B0301-CANVAS-Active-Retargeting_Installments_SP | 2,533 | 1.6 % | 7 | 11.1 |
| Acquisition-KPay-T2728-CANVAS-Prospect_FaltaVeriff-RetargetingNIPconCupon-N/A | 2,428 | 1.5 % | 2 | 6.8 |
| Acquisition-KPay-T2706-CANVAS-Prospect-Retargeting_AccountCreation-Prod | 2,400 | 1.5 % | 1 | 3.9 |
| Collections-KCash-T000-CANVAS-Precobranza-ecosystem | 2,089 | 1.3 % | 31 | 17.4 |
| KCash-Loan-Application-disbursed_late_fees | 2,089 | 1.3 % | 19 | 14.4 |

- **Un solo email explica el 31 % de las bajas de usuarios nuevos del año**: el BillPay Intro de junio, enviado a 16.1 M de usuarios. En E1 ese envío tiene 37,272 bajas atribuidas directamente; en E8, 49,314 usuarios nuevos y 9,117 de la cohorte 0 se dieron de baja el día que les llegó (58 mil en total). Les llegó como primer o segundo email (1.8 en promedio): gente que casi no recibía email y que con un envío masivo se perdió para siempre como canal.
- **El retargeting de registro (Leads_LeftFunnel: Veriff, PersonalInfo, NIP) explica el 22 %**, con mediana de 3 a 4 días y 5 a 8 emails en ese lapso: entre uno y dos emails al día a alguien que acaba de registrarse y no terminó. En la versión 1 parecía el 48 %; con la cobertura completa baja al 22 % porque aparece BillPay, pero sigue siendo la causa número uno entre las campañas recurrentes.
- Después vienen los rescates de Tasa 0 (B0171 HotLeads y Rezagada, 8.5 % entre las tres variantes), B0211 Nuevos Registrados Tasa 0 (4.6 %, pero a los 92 días y después de 18 emails), el transaccional FraudRisk (4.1 %, al día 2) y los retargetings de Installments (3.5 %).

## Por equipo, tipo y producto

Para cada baja se toma la familia que le llegó el día de la baja y su equipo, tipo y producto (del catálogo, igual que en la vista de campañas). Días es la mediana ponderada y emails el promedio ponderado por usuarios. Las sumas pasan de 100 % por el doble conteo explicado arriba.

| Cohorte | Equipo | Bajas | % de la cohorte | Días hasta la baja (mediana) | Emails antes |
|---|---|---|---|---|---|
| Nuevos (feb a sep) | Marketing | 70.0 mil | 44 % | 5 | 10 |
| Nuevos | Others (BillPay y transaccionales) | 67.0 mil | 42 % | 35 | 5 |
| Nuevos | Product Growth | 14.6 mil | 9 % | 92 | 17 |
| Nuevos | Acquisition (KPay) | 6.5 mil | 4 % | 2 | 6 |
| Nuevos | Collections | 5.4 mil | 3 % | 51 | 28 |
| Ya recibían en enero | Marketing | 95.4 mil | 39 % | 64 | 17 |
| Ya recibían | Product Growth | 87.5 mil | 36 % | 128 | 31 |
| Ya recibían | Others | 37.4 mil | 15 % | 97 | 31 |
| Ya recibían | Sales | 10.7 mil | 4 % | 87 | 39 |
| Ya recibían | Collections y Compliance | 7.8 mil | 3 % | 106 a 111 | 29 a 49 |

- **Por tipo**: 89 % de las bajas de nuevos y 87 % de las de la base vieja caen el día de un email promocional o de lifecycle (BillPay cuenta aquí); 11 % y 10 % el día de un transaccional u operativo (FraudRisk, Payment Confirmation, late fees); 3 % en cobranza.
- **Por producto**: Cash 52 % de nuevos y 68 % de la base vieja. "Others" (BillPay y transaccionales) es 42 % en nuevos solo por el envío de junio. KPay es 8.5 % en nuevos y tiene la baja más rápida de todas las de Acquisition (mediana 1 a 2 días, 4 a 7 emails: los retargetings de cuenta y de NIP con cupón).
- **Lectura**: en usuarios nuevos hay dos causas y dos arreglos. Un envío masivo sin filtro (BillPay) que se evita con una regla de audiencia; y el onboarding de Marketing (retargeting de registro) que se arregla con un tope diario. Product Growth pierde al usuario a los tres meses con la insistencia de Tasa 0 (B0211) e Installments (B0223): ahí el arreglo es tope mensual y salida por no apertura.

## Cohorte 0 (ya recibía email en enero, 242,301 usuarios)

Mediana 86 días y 17 emails (piso, por la censura); 21 % aguanta más de 180 días y 31 % recibió más de 30 emails antes de irse. Aquí mandan las campañas de insistencia a bases viejas: B0211 Nuevos Registrados Tasa 0 (12.9 %, a los 128 días y 29 emails), B0326 Leads Referral (10.7 %, 88 días, 19 emails), B0171 Rezagada NarrativaTasa0 (8.4 %, 29 días), B0223 NeverActive Installments (5.7 %, 178 días, 37 emails), BillPay (3.8 %), B0337 CuestaEnero (2.9 %), B0209 Recurrentes Inactivos (2.7 %, 167 días, 45 emails). Es el cansancio lento: muchos emails durante meses hasta que el usuario se harta. Son las mismas familias que salen en apagar o rehacer en la vista de campañas.

## Qué hacer con esto

1. **Regla para envíos masivos**: nada a toda la base. Un envío a 16.1 M de usuarios costó 0.8 M MXN en email (16.1 M × 0.05) y se llevó 58 mil usuarios en un día, el 31 % de las bajas de nuevos del año. Antes de un envío grande: mandar solo a quien abrió algo en los últimos 90 días, probar con 5 % de la audiencia y medir bajas por mil entregados contra el promedio del canal (3.45 por mil) antes de escalar.
2. **Tope en el onboarding**: el retargeting de registro (Veriff, PersonalInfo, NIP) a 1 email al día y máximo 3 en la primera semana, con push o in-app para el resto. Hoy manda hasta 2 al día y genera el 22 % de las bajas de usuarios nuevos.
3. **El primer email decide**: 33 % se va con el primero. Un usuario nuevo no debe entrar a varias canvases a la vez (recibe 4.2 familias distintas antes de irse); una sola secuencia de bienvenida y lo demás después.
4. **Regla de los 5 emails**: si un usuario nuevo no abrió ninguno de sus primeros 5 emails (la mediana antes de la baja), parar lo promocional antes de que se dé de baja y se pierda también lo transaccional de valor.
5. **Para las bases viejas** la receta ya está en la vista de campañas: B0211, B0326, B0171, B0223 y B0209 son las mismas familias que salen en apagar o rehacer. Tope mensual y salida por no apertura.
