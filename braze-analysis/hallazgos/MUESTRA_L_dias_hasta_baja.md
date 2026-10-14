# Muestra L. En cuántos días se dan de baja y cuántos emails recibieron antes (E8)

Fuente: `data/e8_dias_hasta_baja.csv` (79 filas, 4 bloques). Para cada usuario que se dio de baja de email: días entre su primer email entregado y la baja, emails y familias distintas que recibió hasta la baja, y qué familia le llegó el día de la baja. Agregado, sin identificadores.

Dos cohortes. **Cohorte limpia** = su primer email fue de febrero en adelante, así que el conteo de días es real. **Cohorte 0** = ya recibía email en enero; la historia empieza el 1 de enero, así que sus días y emails son un piso, no la cifra real.

**Aviso sobre el conteo.** Esta corrida encontró 115 mil bajas (47.6 mil limpias y 67.2 mil de la cohorte 0) contra las 457 mil del periodo. La primera versión de la query pedía que la fila de la baja tuviera también entrega, y en la tabla la baja viene muchas veces en una fila aparte. La query ya está corregida en `sql/extraccion.sql` (versión 2); la distribución de días y emails no debería cambiar mucho, pero los totales por familia sí crecerán.

## Lo que dice (cohorte limpia, 47.6 mil usuarios)

| | Días hasta la baja | Emails antes de la baja | Familias distintas |
|---|---|---|---|
| Promedio | 25.5 | 9.7 | 4.3 |
| Mediana | 4 | 6 | |
| p90 | 92 | | |

- **La mitad se da de baja en los primeros 4 días y 63 % en la primera semana** (25 % el mismo día del primer email, 38 % entre el día 1 y el 7). Solo 10 % aguanta más de 90 días.
- **Se van después de 6 emails (mediana)**. Quien se da de baja en la primera semana recibió en promedio 5.9 emails en esos días: casi uno al día. 16 % se da de baja con el primer email.
- **Casi la mitad (48 %) se da de baja el día que le llega un email del retargeting de registro** (Leads_LeftFunnel: Retargeting_Veriff 31 %, Retargeting_PersonalInfo 12.5 %, Retargeting_NIP 4 %). Mediana de 1 a 3 días desde el primer email y 4 a 7 emails en ese lapso: son dos emails al día a alguien que acaba de registrarse y no terminó.
- Después vienen Rechazo transaccional FraudRisk (9 %, mismo día), BillPay Intro (7 %, mismo día: el envío a 16 M de junio), B0211 Nuevos Registrados Tasa 0 (5 %, pero a los 87 días y después de 17 emails) y los retargetings de Installments (6 %).

| Familia del día de la baja | Usuarios | % de las bajas | Días (mediana) | Emails antes |
|---|---|---|---|---|
| Marketing-KCash-B0000-CANVAS-Leads_LeftFunnel-Retargeting_Veriff | 14,848 | 31 % | 3 | 7.3 |
| Marketing-KCash-B0000-CANVAS-Leads_LeftFunnel-Retargeting_PersonalInfo | 5,964 | 13 % | 1 | 4.2 |
| KCash Rechazo transaccional FraudRisk | 4,304 | 9 % | 0 | 7.0 |
| NewProducts-Kueski-T0000-E-Portfolio_BillPay_Intro_Full_Rollout | 3,289 | 7 % | 0 | 2.1 |
| Lending-KCash-B0211-CANVAS-Nuevos_RegistradosPay-Tasa0-N/A | 2,384 | 5 % | 87 | 17.1 |
| Marketing-KCash-B0000-CANVAS-Leads_LeftFunnel-Retargeting_NIP | 2,012 | 4 % | 2 | 6.5 |
| Marketing-KCash-B0301-CANVAS-Active-NuevosRetargeting_Installments_SP | 1,597 | 3 % | 1 | 8.1 |
| Acquisition-KPay-T2728-CANVAS-Prospect_FaltaVeriff-RetargetingNIPconCupon-N/A | 1,533 | 3 % | 1 | 5.1 |
| Collections-KCash-T000-CANVAS-Precobranza-ecosystem | 1,518 | 3 % | 29 | 15.8 |
| Lending-KCash-B0301-CANVAS-Active-Retargeting_Installments_SP | 1,360 | 3 % | 1 | 9.0 |

## Por equipo, tipo y cohorte

Las familias con 500 o más bajas cubren todas las bajas de la cohorte limpia y 84 % de la cohorte 0. Para cada baja se toma la familia que le llegó el día de la baja y su equipo y tipo (del catálogo). Días y emails son medianas y promedios ponderados por usuarios.

| Cohorte | Equipo | Bajas | % de la cohorte | Días hasta la baja (mediana) | Emails antes |
|---|---|---|---|---|---|
| Nuevos (feb a sep) | Marketing | 27.0 mil | 57 % | 5 | 7 |
| Nuevos | Others (transaccional, BillPay) | 12.2 mil | 26 % | 7 | 9 |
| Nuevos | Product Growth | 3.7 mil | 8 % | 56 | 14 |
| Nuevos | Acquisition (KPay) | 3.3 mil | 7 % | 1 | 4 |
| Nuevos | Collections | 2.2 mil | 5 % | 34 | 19 |
| Ya recibían en enero | Marketing | 27.0 mil | 40 % | 51 | 16 |
| Ya recibían | Product Growth | 18.8 mil | 28 % | 111 | 32 |
| Ya recibían | Others | 7.7 mil | 12 % | 80 | 31 |
| Ya recibían | Collections, Sales, Compliance | 3.1 mil | 5 % | 88 a 118 | 32 a 61 |

- **Por tipo**: 79 % de las bajas de nuevos y 74 % de las de la base vieja caen el día de un email promocional; 19 % y 8 % el día de un transaccional (FraudRisk, Payment Confirmation, BillPay); 5 % y 2 % en cobranza.
- **Por producto**: Cash concentra 69 % y 65 %. KPay es 7 % en nuevos pero con la baja más rápida de todas (mediana 1 día, 4 emails: los retargetings de Veriff y NIP con cupón).
- **Lectura**: Marketing pierde al usuario nuevo en la primera semana con el onboarding; Product Growth lo pierde a los tres meses con la insistencia de Tasa 0 (B0211) e Installments (B0223). Son dos problemas distintos con dos arreglos distintos: tope diario en el primero, tope mensual y salida por no apertura en el segundo.

## Cohorte 0 (ya recibía email en enero, 67.2 mil usuarios)

Mediana 62 días y 15 emails (piso, por la censura). Aquí mandan las campañas de insistencia a bases viejas: B0171 Rezagados NarrativaTasa0 (13 %, a los 29 días), B0211 Nuevos Registrados Tasa 0 (12 %, a los 108 días y 29 emails), B0326 Leads Referral (9 %, 85 días, 20 emails), B0223 NeverActive (5 %, 182 días, 44 emails). Es el cansancio lento: muchos emails durante meses hasta que el usuario se harta.

## Qué hacer con esto

1. **Tope en el onboarding**: el retargeting de registro (Veriff, PersonalInfo, NIP) a 1 email al día y máximo 3 en la primera semana, con push o in-app para el resto. Hoy manda 2 al día y genera la mitad de las bajas de usuarios nuevos.
2. **Regla de los 6 emails**: si un usuario nuevo no abrió ninguno de sus primeros 6 emails, parar lo promocional antes de que se dé de baja (y perder también lo transaccional de valor).
3. **Para las bases viejas** la receta ya está en la vista de campañas: B0171, B0211, B0326 y B0223 son las mismas familias que salen en apagar o rehacer.
