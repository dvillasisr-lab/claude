# Muestra H. Envíos por etapa del usuario y a quién no deberíamos escribirle (E7a)

Fuente: `data/e7a_familia_canal_etapa.csv` (recibida 14 oct 2026): familia × canal × etapa de `product.customer_golden_dataset.dim_braze_filters`. La tabla de etapas cubre al 37 % de los envíos (el resto queda como `sin_golden`), bastante más que el 7 % de usuarios que se estimaba, porque los usuarios que sí están en ella reciben más mensajes.

## Respuesta en una página

De los envíos que sí tienen etapa, 56.6 M (8.5 % del total del periodo) fueron a usuarios con la tarjeta KPay congelada, 490 mil a usuarios en REUS o ARCO (pidieron formalmente no recibir publicidad) y 426 mil a usuarios en lista negra. En promocional eso son 43.4 M, 249 mil y 146 mil envíos. Ninguno de los tres grupos debería recibir promoción: el primero no puede usar el producto que se le ofrece y los otros dos son tema de cumplimiento.

| Etapa | Envíos | % del total | Promocional | Transaccional | Cobranza | Respuesta | Conv. ref. por mil |
|---|---|---|---|---|---|---|---|
| 7. Prospects | 189.1 M | 28.5 | 167.2 M | 15.9 M | 6.1 M | 6.99 % | 10.7 |
| 4. KPay CC Freeze | 56.6 M | 8.5 | 43.4 M | 7.7 M | 5.5 M | 6.35 % | 7.9 |
| 6. REUS o ARCO | 0.49 M | 0.07 | 0.25 M | 0.18 M | 0.06 M | 5.21 % | 7.9 |
| 3. Blacklist | 0.43 M | 0.06 | 0.15 M | 0.23 M | 0.05 M | 2.79 % | 5.9 |
| Sin etapa en la tabla | 416.2 M | 62.8 | 356.3 M | 26.8 M | 33.2 M | 6.80 % | 5.3 |

## Promocional a quien no debe recibirlo

**REUS o ARCO (249 mil envíos, 104 mil usuarios).** Lo más grande: `Shopping-KPay-S0004 WeeklyRecommendations` por email (57 mil), `Lending-KPay-B0333 Churn 12 meses` por WhatsApp, email y push (47 mil), `Lending-KPay-B0332 HardInactive` (22 mil), `Sales-KPay-B0335 PromocionesMerchants` (6 mil), `QA-KPay-B001` (5 mil). Un usuario en REUS que recibe WhatsApp promocional es una queja potencial ante Condusef.

**Lista negra (146 mil envíos, 69 mil usuarios).** Cumpleaños y aniversario automatizados (B0152, B0153: 24 mil), `QA-KPay-B001` (8.6 mil), Sales B0335 y B0367, Referral B0326, Cashback B0324 y B0359.

**Tarjeta KPay congelada (43.4 M envíos, 28.7 M usuario-familia).** Lo que más pesa: `Marketing-KPay-B0326 Referral Dormants` email 1.96 M, `Sales-KPay-B0335 PromocionesMerchants` email 1.27 M, `Sales B0367 Comercio del día` push 631 mil, `Marketing B0326 Referral Activos` push 571 mil, `Marketing-KCash-B0391 RescateFinesDeSemana` push 564 mil, `Sales B0493 HotSale` push 560 mil, `Sales B0417` push 531 mil, `Shopping S0004` email 531 mil. Son promociones de KPay a gente que no puede pagar con KPay.

## Las etapas también explican la respuesta

Promocionales, respuesta por etapa:

| Canal | Prospects | CC Freeze | Sin etapa |
|---|---|---|---|
| Email (clic) | 0.27 % | 0.38 % | 0.67 % |
| Push (apertura) | 1.33 % | 1.45 % | 1.20 % |
| WhatsApp (lectura) | 54.3 % | 51.7 % | 49.2 % |
| In-app (clic) | 26.8 % | 32.9 % | 50.9 % |

El email a prospectos (167 M envíos promocionales, 28 % de todo lo que se manda) hace 0.27 % de clic, debajo del mínimo que usamos para apagar. Confirma el lente de campañas por otro camino: el volumen grande de email está en gente que todavía no es cliente y no responde al email.

## Qué hacer

1. **Exclusión global en Braze**: segmento con etapa 3, 4 y 6 como filtro negativo en todos los Canvas promocionales. Es un cambio una vez y quita 44 M envíos del periodo sin tocar ninguna campaña. Para WhatsApp son 3.8 M MXN en el periodo (CC Freeze y REUS por WhatsApp).
2. **Para REUS o ARCO**, además, revisar con legal si el filtro debe cubrir también cobranza (hoy 61 mil envíos).
3. **Prospectos por email**: tratarlos como base fría en el lente de campañas (ya lo están cuando el nombre dice Leads o Anónimos).

Columna `envios_etapa_bloqueada` ya está por familia × canal en `muestra_c_familias.csv` y en la página de campañas.

Nota técnica: en el resultado de Databricks la familia conservó la fecha (`regexp_replace` con `\d` no se aplicó; en Spark SQL hay que escribir `\\d`). Se colapsó en el análisis con la misma regla.
