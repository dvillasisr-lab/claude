# Muestra K. Convierten los que abren contra los que no abren (E7c)

Fuente: `data/e7c_abren_vs_no_abren.csv` (2,062 filas familia × canal con fecha en el nombre; colapsadas a 1,194 familias × canal). Por cada usuario-día con envío se marca si abrió (email, push), leyó (WhatsApp) o vio (in-app) el mensaje, y si convirtió (`is_converted`) en los 7 días siguientes. Es el método que ya usa el equipo: si quienes abren convierten igual que quienes no, el mensaje no mueve nada. Resultado en `hallazgos/muestra_k_abren_vs_no_abren.csv`; las columnas conv_abren_pct, conv_no_abren_pct y lift (veces) están también en `muestra_c_familias.csv` y en la página de campañas.

Muestra suficiente = al menos 1,000 usuarios-día de cada lado y 100 conversiones: 856 de 1,194 familias × canal la tienen (768 promocionales). In-app no tiene "no vieron" (la impresión es la vista), así que no tiene veces.

## Lo que dice

| Canal | Familias con muestra | Convierten quienes abren (mediana) | Convierten quienes no abren | Veces (mediana) | Apertura (mediana) |
|---|---|---|---|---|---|
| email | 334 | 8.3 % | 3.6 % | 2.3 | 10.6 % |
| push notification | 314 | 19.9 % | 6.6 % | 3.0 | 1.1 % |
| whatsapp | 208 | 6.1 % | 3.5 % | 2.1 | 41.4 % |

- **En casi todas las familias quienes abren convierten más que quienes no abren** (mediana 2 a 3 veces). Eso no prueba que el mensaje cause la conversión: quien abre ya es un usuario más activo. Por eso el dato se usa en dos pasos: primero, si quienes abren convierten al menos la mitad de lo normal del canal (hay a quién acotar la base); segundo, si abrir cambia la conversión (1.5 veces o más). Si falla cualquiera, el mensaje no mueve y se apaga.
- **64 familias × canal tienen veces menor a 1.5**: abrir casi no cambia nada. La mayoría son transaccionales y de cobranza (Autopay, Payment Received, disbursed, Precobranza), donde la conversión viene del flujo y no del mensaje; eso está bien, no se tocan. Las promocionales con veces menor a 1.5 son:

| Familia | Canal | Usuarios-día | Convierten quienes abren | Quienes no abren | Veces | Qué hacer hoy |
|---|---|---|---|---|---|---|
| Marketing-KCash-B0326-Canvas-Leads-ReferralProgram-N/A | email | 8.5 M | 0.64 % | 0.53 % | 1.21 | Confirmar apagado |
| Marketing-KCash-B0171-CANVAS-Leads_BBDDRezagada-NarrativaTasa0-N/A | email | 5.1 M | 0.21 % | 0.16 % | 1.31 | Bajar frecuencia |
| Marketing-KPay-B0326-Canvas-Leads-ReferralProgram-N/A | email | 1.7 M | 3.57 % | 2.97 % | 1.20 | Rehacer o re-segmentar |
| Lending-KCash-B0301-CANVAS-Active-Retargeting_Installments_SP | whatsapp | 910 mil | 11.05 % | 8.78 % | 1.26 | Seguir igual |
| Marketing-KCash-B0171-CANVAS-Leads_BBDDRezagada-NarrativaValueProp-N/A | email | 807 mil | 0.26 % | 0.23 % | 1.15 | Bajar frecuencia |
| Marketing-KCash-B0326-Canvas-Leads_Todos-ReferralProgram-N/A | email | 762 mil | 1.32 % | 1.01 % | 1.31 | Bajar frecuencia |
| Lending-KCash-B0074-CANVAS-Recurrentes_SeQuedanStepOffering-RetargetingNuevaImagen | email | 464 mil | 51.70 % | 35.19 % | 1.47 | Bajar frecuencia |
| Lending-KCash-B0301-CANVAS-Active-RecurrentesRetargeting_Installments_SP | whatsapp | 456 mil | 10.02 % | 8.87 % | 1.13 | Limpiar base de WhatsApp |
| Marketing-KPay-B0326-Canvas-Leads-ReferralProgram-N/A | whatsapp | 400 mil | 3.91 % | 3.04 % | 1.29 | Seguir igual |
| Marketing-KCash-B0301-CANVAS-Active-NuevosRetargeting_Installments_SP | whatsapp | 334 mil | 5.71 % | 3.91 % | 1.46 | Limpiar base de WhatsApp |
| Marketing-KPay-B0366-CANVAS-Leads-Newsletter-N/A | email | 317 mil | 0.42 % | 0.33 % | 1.26 | Confirmar apagado |
| Sales-KPay-B0355-CANVAS-Leads-KUESKINUEVO25Online-N/A | email | 304 mil | 0.25 % | 0.18 % | 1.42 | Confirmar apagado |
| Marketing-KPay-B0366-CANVAS-Recurrentes-Newsletter-N/A | email | 271 mil | 14.10 % | 10.46 % | 1.35 | Confirmar apagado |
| Marketing-KPay-B0278-CANVAS-Leads-LanzamientoSoriana-N/A | email | 244 mil | 0.31 % | 0.21 % | 1.43 | Confirmar apagado |
| Lending-Ecosistema-B0440-CANVAS-Todos-AnotayGana-P3v2 | whatsapp | 239 mil | 12.91 % | 10.58 % | 1.22 | Seguir igual |

- **Promocionales de volumen donde ni quien abre convierte** (menos de la mitad de la mediana del canal, un millón o más de usuarios-día): aquí no hay a quién acotar, por eso la acción es apagar el canal.

| Familia | Canal | Usuarios-día | Convierten quienes abren | Quienes no abren | Veces | Qué hacer hoy |
|---|---|---|---|---|---|---|
| Lending-KCash-B0211-CANVAS-Nuevos_RegistradosPay-Tasa0-N/A | email | 34.9 M | 0.47 % | 0.12 % | 3.8 | Apagar |
| NewProducts-Kueski-T0000-E-Portfolio_BillPay_Intro_Full_Rollout | email | 16.1 M | 0.80 % | 0.16 % | 5.0 | Confirmar apagado |
| Lending-KCash-B0223-CANVAS-Nuevos_NeverActive-InstallmentsNoCash-N/A | email | 13.5 M | 0.13 % | 0.03 % | 4.0 | Apagar |
| Marketing-KCash-B0391-CANVAS-Leads_BDDMarketing-RescateFinesDeSemana-N/A | push notification | 13.4 M | 6.62 % | 0.97 % | 6.9 | Rehacer o re-segmentar |
| Marketing-KCash-B0171-CANVAS-Anonimos-RescateTasa0-N/A | push notification | 8.9 M | 7.50 % | 1.03 % | 7.3 | Apagar |
| Marketing-KCash-B0326-Canvas-Leads-ReferralProgram-N/A | email | 8.5 M | 0.64 % | 0.53 % | 1.2 | Confirmar apagado |
| Lending-KCash-B0337-CANVAS-Leads_Eligibles-CuestaEnero-N/A | email | 7.4 M | 2.18 % | 0.38 % | 5.8 | Confirmar apagado |
| Marketing-KCash-B0326-Canvas-Recurrentes_Dormants-ReferralProgram-N/A | email | 7.0 M | 3.13 % | 0.69 % | 4.5 | Apagar |
| Marketing-KCash-B0326-Canvas-Leads-ReferralProgram-N/A | push notification | 6.4 M | 7.29 % | 1.43 % | 5.1 | Confirmar apagado |
| Marketing-KCash-B0171-CANVAS-Leads_BBDDRezagada-RescateTasa0-N/A | push notification | 5.8 M | 6.30 % | 0.77 % | 8.1 | Apagar |
| Marketing-KCash-B0171-CANVAS-Leads_BBDDRezagada-NarrativaTasa0-N/A | whatsapp | 5.4 M | 1.02 % | 0.32 % | 3.2 | Seguir igual |
| Marketing-KPay-B0326-Canvas-Recurrentes_Dormants-ReferralProgram-N/A | email | 5.2 M | 1.12 % | 0.33 % | 3.4 | Apagar |
| Marketing-KCash-B0171-CANVAS-Leads_BBDDRezagada-RescateTasa0-N/A | email | 5.2 M | 0.50 % | 0.31 % | 1.6 | Seguir igual |
| Marketing-KCash-B0171-CANVAS-Leads_BBDDRezagada-RescateTasa0-N/A | whatsapp | 5.2 M | 1.07 % | 0.24 % | 4.5 | Apagar |
| Lending-KCash-B0211-CANVAS-Nuevos_RegistradosPay-Tasa0-N/A | push notification | 5.1 M | 5.98 % | 0.33 % | 17.9 | Apagar |

- **Las promocionales donde abrir más cambia la conversión** (veces más alto, con muestra):

| Familia | Canal | Usuarios-día | Convierten quienes abren | Quienes no abren | Veces |
|---|---|---|---|---|---|
| Lending-KCash-B0211-CANVAS-Nuevos_RegistradosPay-Tasa0-N/A | push notification | 5.1 M | 5.98 % | 0.33 % | 17.9 |
| Marketing-KCash-B0171-CANVAS-Leads-BBDDRezagada180360DiasReaccionanWA-N/A | whatsapp | 48 mil | 1.13 % | 0.07 % | 17.4 |
| Marketing-KCash-B0171-CANVAS-Leads_BBDDRezagada-Tasa0-N/A | push notification | 277 mil | 4.29 % | 0.36 % | 12.0 |
| Marketing-KCash-B0171-CANVAS-Leads_BBDDRezagada-NarrativaTasa0-N/A | push notification | 2.5 M | 5.56 % | 0.48 % | 11.6 |
| Marketing-KPay-B0534-CANVAS-Leads-Comerciodeldia-N/A | push notification | 1.3 M | 2.67 % | 0.24 % | 11.1 |
| Marketing-KPay-B0444-CANVAS-Leads-BAUMundial-N/A | push notification | 701 mil | 2.98 % | 0.28 % | 10.8 |
| Lending-KCash-B0224-CANVAS-Recurrentes_Lazaro-SegundaOportunidad-N/A | push notification | 123 mil | 12.47 % | 1.27 % | 9.8 |
| Marketing-KPay-B0422-CANVAS-Leads-KUESKINUEVO30Big7-N/A | push notification | 979 mil | 5.04 % | 0.53 % | 9.5 |
| Marketing-KCash-B0171-CANVAS-Leads_BBDDRezagadaHotLeads-NarrativaTasa0-N/A | push notification | 671 mil | 7.80 % | 0.83 % | 9.4 |
| Acquisition-KPay-T2706-CANVAS-Prospect-Retargeting_AccountCreation-Prod | email | 1.3 M | 4.43 % | 0.52 % | 8.5 |

Lectura: B0211 Nuevos Registrados (push 17.9 veces) y B0171 Rezagados (push 8 a 12 veces) tienen un mensaje que sí mueve a quien lo abre, pero menos del 1 % lo abre y quienes abren convierten 4 a 6 %, debajo de la mitad de lo normal en push (19.9 %). Es el caso típico de "el push está bien, la base no": acotar a quienes abrieron algún push en 60 días.

## Veriff, la referencia del equipo

| Familia | Canal | Convierten quienes abren | Quienes no abren | Veces | Apertura |
|---|---|---|---|---|---|
| Acquisition-KPay-T2727-CANVAS-Prospect_FaltaVeriff-RetargetingVeriff-Prod | email | 8.18 % | 4.73 % | 1.73 | 11.0 % |
| Acquisition-KPay-T2728-CANVAS-Prospect_FaltaVeriff-RetargetingNIPconCupon-N/A | email | 3.96 % | 1.64 % | 2.42 | 10.8 % |
| Copy of Acquisition-KPay-T2727-CANVAS-Prospect_FaltaVeriff-RetargetingVeriff-Test | email | 12.35 % | 6.67 % | 1.85 | 14.1 % |
| Marketing-KCash-B0000-CANVAS-Leads_LeftFunnel-Retargeting_Veriff | email | 4.48 % | 2.58 % | 1.73 | 16.4 % |
| Marketing-KCash-B0000-CANVAS-Leads_LeftFunnel-Retargeting_Veriff | push notification | 11.26 % | 4.41 % | 2.55 | 5.8 % |

El equipo tenía 22 % contra 17 %. Aquí sale 4.5 % contra 2.6 % en Marketing-KCash-B0000 Retargeting_Veriff (email) y 8.2 % contra 4.7 % en Acquisition-KPay-T2727. La diferencia está en la definición: aquí la conversión es `is_converted` en 7 días por usuario-día de envío, y la del equipo seguramente fue por usuario único en una ventana más larga, o completar Veriff en vez de convertir. La conclusión es la misma: quienes abren convierten 1.7 a 2.4 veces más, pero la mitad de la diferencia es que quien abre ya venía más interesado.

## Qué hacer con esto

1. Usar las dos columnas como filtro de salida de cualquier campaña nueva: a las 4 semanas, si quienes abren no convierten al menos la mitad de lo normal del canal, se apaga sin discutir.
2. Para probar causalidad de verdad hace falta un grupo de control (holdout) en Braze: 5 a 10 % de la audiencia que no recibe el mensaje. Es la única forma de separar "el mensaje mueve" de "quien abre ya iba a convertir".
3. En in-app medir con holdout también: no hay "no vieron" y el clic es la única señal.

## Con ventanas de 7, 30 y 90 días y hasta fin de periodo (E9a)

Fuente: `data/e9a_abren_vs_no_abren_ventanas.csv` (1,225 filas; 867 familias × canal con muestra). Resultado en `hallazgos/muestra_m_ventanas.csv`. Mismo cálculo que E7c pero la conversión se busca en 7, 30 y 90 días después del envío, y hasta el 30 de septiembre.

| Canal | Convierten quienes abren / quienes no, a 7 días | A 30 días | A 90 días | Hasta fin de periodo | Veces a 7 días | Veces a 90 días |
|---|---|---|---|---|---|---|
| Email | 8.4 % / 3.6 % | 18.9 % / 9.8 % | 25.3 % / 13.6 % | 24.0 % / 12.4 % | 2.3 | 1.6 |
| Push | 19.8 % / 6.6 % | 35.5 % / 18.3 % | 43.9 % / 25.2 % | 41.4 % / 22.6 % | 3.0 | 1.9 |
| WhatsApp | 5.9 % / 3.3 % | 14.4 % / 9.7 % | 23.0 % / 15.4 % | 21.9 % / 14.6 % | 2.1 | 1.5 |

(Medianas entre familias con muestra. "Hasta fin de periodo" sale un poco menor que 90 días porque los envíos de agosto y septiembre tienen menos días por delante.)

- **La diferencia se achica al abrir la ventana, pero no desaparece.** Las veces pasan de 2.3 a 1.6 en email, de 3.0 a 1.9 en push y de 2.1 a 1.5 en WhatsApp: la mitad de la ventaja de quienes abren es de corto plazo (el mensaje adelanta la conversión) y la otra mitad se sostiene a 90 días (quien abre es alguien distinto, más activo).
- **A 90 días, 285 de 867 familias × canal (33 %) ya tienen menos de 1.5 veces**, contra 65 a 7 días. Entre promocionales son 248 de 779. Eso quiere decir que para un tercio de las campañas, en tres meses quienes no abrieron alcanzan a quienes abrieron: el mensaje movió el calendario, no el resultado.
- **Las que apagamos siguen mal con cualquier ventana.** B0211 Nuevos Registrados por email: quienes abren convierten 2.3 % a 90 días contra 1.0 % de quienes no; en email lo normal entre quienes abren a 90 días es 25 %. B0223 NeverActive: 0.8 % contra 0.3 %. B0171 Rezagados WhatsApp: 4.2 % contra 1.7 % (normal 23 %). La ventana no las rescata.
- **Las de ventas a recurrentes (Sales KPay, Privalia, Comercio del día, Venta Azul) sí sostienen la diferencia** a 90 días (2 a 2.5 veces) y con conversión alta entre quienes abren (27 a 39 %). Son las que vale la pena re-segmentar en vez de apagar.
- **Veriff (email) cae a 1.5 veces a 90 días** (12.1 % contra 8.1 %): dos tercios de su diferencia a 7 días era adelanto. Refuerza la lectura de bajar frecuencia en vez de insistir.

Qué ventana usar: 7 días para medir si la pieza mueve a corto plazo (es la que entra en la regla de acciones); 90 días para saber si cambió el resultado. Cuando las dos coinciden, la decisión es segura; cuando a 7 días se ve bien y a 90 no, el mensaje adelanta pero no suma, y la discusión es de costo (vale si es push o in-app, no si es WhatsApp).
