# Muestra E. Qué le llega a un usuario después de darse de baja de email (E5b)

Fuente: `data/e5b_comms_despues_baja.csv` (recibida 14 oct 2026), 97 familias con 500 o más emails. Un email cuenta aquí si llegó en un mes posterior al mes de la primera baja del usuario. Familia = nombre sin la fecha.

## Respuesta en una página

De los 1.42 M emails que llegaron a usuarios ya dados de baja, el 94 % es cobranza o transaccional, que es legítimo: la baja de marketing no cubre avisos de pago, contratos ni confirmaciones. El problema real es chico y está acotado: 80 mil emails promocionales en 33 familias, a 45 mil usuarios, casi todo de Marketing.

| Tipo | Familias | Emails | Usuarios aprox. | Abiertos | Clics |
|---|---|---|---|---|---|
| Cobranza | 20 | 783,911 | 112,918 | 145,261 | 8,650 |
| Transaccional u operativa | 27 | 559,075 | 208,722 | 201,750 | 18,750 |
| Promocional o lifecycle | 33 | 79,994 | 45,305 | 7,700 | 658 |

## Promocionales que ignoran la baja

| Familia | Equipo | Emails | Meses |
|---|---|---|---|
| Marketing-KCash-B0171 Leads_BBDDRezagada RescateTasa0 | Marketing | 13,943 | 5 |
| Marketing-KCash-B0326 Leads ReferralProgram | Marketing | 10,552 | 5 |
| Marketing-KCash-B0171 Leads_BBDDHotLeadsW1 RescateTasa0 | Marketing | 9,998 | 3 |
| Lending-KCash-B0211 Nuevos_RegistradosPay Tasa0 | Product Growth | 8,317 | 5 |
| Marketing-KCash-B0000 Leads_LeftFunnel Retargeting_Veriff | Marketing | 4,409 | 9 |
| NewProducts-Kueski-T0000 Portfolio_BillPay_Intro | Others | 3,050 | 1 |
| Sales-KPay-B0392 Leads CuponeraDescuentosMarzo | Sales | 2,597 | 3 |
| Newsletters (B0366, B0437, B0341, B0401) | Marketing | 6,729 | 4 |

Por equipo: Marketing 58,988, Product Growth 10,119, Sales 4,944, Others 4,550, Acquisition 1,393.

Patrón: son los mismos Canvas grandes del lente de campañas. Lo más probable es que el filtro de suscripción esté puesto en la entrada del Canvas y no en cada paso de email, así que quien se da de baja a mitad del recorrido sigue recibiendo los pasos que faltan. Se arregla en Braze con el filtro "subscribed or opted in" en cada paso de email, o con el grupo de suscripción global en la configuración del Canvas.

## Dos cosas que no son promocionales pero sí llaman la atención

- `PRUEBA_Collections-KCash-T000-CANVAS-BKT1` y `PRUEBA_Collections-...-Precobranza-ecosystem`: Canvas de prueba de cobranza que le llegaron a 5,166 usuarios reales ya dados de baja. Habría que confirmar que estas pruebas no estén activas con audiencia real.
- Dos versiones del mismo email transaccional conviven: `KCash-Loan-Application-disbursed-20240821` y `KCash-Loan-Application-disbursed_20251110`. En E6b también aparecen llegando juntas el mismo día a 600 mil usuarios. Una de las dos sobra.

## Qué hacer

1. En los 6 Canvas promocionales de la tabla, poner el filtro de suscripción en cada paso de email (no solo en la entrada). Son 80 mil emails al año que, además de molestar, pesan en reputación de dominio.
2. Pausar o archivar los Canvas `PRUEBA_` y `QA` con audiencia real (ver también muestra F).
3. Apagar la versión 20240821 del email de desembolso si la 20251110 la reemplaza.

Columna `emails_a_dados_de_baja` ya está por familia en `muestra_c_familias.csv` y en la página de campañas.
