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

## Qué hacer en cada una y por qué

Cada familia × canal tiene tres columnas más: `accion_tipo` (una de nueve acciones), `accion` (la instrucción concreta) y `por_que` (los números de esa familia que la justifican). Las asigna `scripts/acciones_campanas.py` **solo a partir de datos, no del nombre de la campaña**: la señal (respuesta y bajas), el canal, y E7c (si quienes abren convierten y cuánto más que quienes no abren). También se agregan `toques_usuario_mes` (envíos entre usuarios alcanzados, por mes activo, de E1), `usuarios_por_envio`, `otros_canales` (canales de la misma familia que sí responden, para no perder el contacto al apagar uno), `conv_abren_pct`, `conv_no_abren_pct`, `lift` y `lift_muestra` (E7c), `pct_prospectos` (E7a: parte de los envíos con etapa conocida que va a prospectos sin crédito), `emails_a_dados_de_baja` (E5b) y `envios_etapa_bloqueada` (E7a). En la página de campañas están como columnas "Qué hacer" y "Por qué", con filtro.

**Qué significa "abrió" o "leyó" en las acciones.** Es el canal en general: cualquier email, push o WhatsApp de Kueski en los últimos 90 días (60 en push), no solo de esta campaña. Es un filtro de receptividad al canal; en Braze es la fecha del último open o read por canal. Lo único que sí es de la campaña es "excluir a quien no abrió ninguno de sus últimos 3 envíos".

**Cuándo un mensaje "mueve".** Con E7c, un mensaje mueve si quienes lo abren convierten al menos la mitad de lo normal del canal (medianas entre quienes abren: email 8.3 %, push 19.9 %, WhatsApp 6.1 %) y abrirlo cambia la conversión (1.5 veces o más contra quienes no abren). Hace falta muestra: 1,000 usuarios-día de cada lado y 100 conversiones. Sin muestra, decide la respuesta: menos de la mitad del mínimo del canal = no mueve.

### Reglas

| Situación | Qué hacer | Por qué |
|---|---|---|
| Apagar o rehacer, y el mensaje no mueve (ni quien abre convierte, o abrir no cambia nada) | **Apagar** ese canal; si otro canal de la misma familia responde, dejarlo como contacto | No hay a quién acotar la base: ni los que abren convierten. Insistir cuesta y quema el permiso |
| Apagar o rehacer, pero quien abre sí convierte | **Rehacer o re-segmentar**: solo quien abrió algo del canal en 90 días (60 en push), tope de 2 al mes | El mensaje funciona para quien lo ve; el problema es a quién y cuántas veces se manda |
| Apagar o rehacer en WhatsApp, y quien lee sí convierte; o revisar en WhatsApp | **Limpiar base de WhatsApp**: quitar números sin entrega, enviar a quien leyó algún WhatsApp en 90 días | Cada envío cuesta 1 MXN se entregue o no; 14.3 M MXN del periodo fueron mensajes no entregados |
| Apagar o rehacer en in-app con clic menor a 5 % | **Apagar**: quitar la pieza | No cuesta, pero ocupa la pantalla y le quita lugar a piezas que sí funcionan (18 % de clic la mediana) |
| Revisar por bajas altas | **Bajar frecuencia**: 2 emails al mes y excluir a quien no abrió ninguno de los últimos 3 envíos de la campaña | El clic es bueno, así que el contenido sirve; lo que molesta es la presión |
| Revisar por respuesta baja | **Rehacer o re-segmentar**: probar gancho, asunto u horario y acotar a quien abre el canal | Está debajo de la mediana del canal |
| Apagar o rehacer pero sin envíos en septiembre | **Confirmar apagado** | Ya no envía; solo verificar que esté archivada para que no vuelva |
| Proteger | **Proteger**: no tocar y evitar que otras campañas le lleguen el mismo día | Respuesta 1.5 veces la mediana con volumen alto |
| Escalar | **Escalar**: ampliar audiencia por pasos, duplicar y medir cada mes | Respuesta al doble de la mediana con poco volumen |
| Sin señal, pero 4.5 o más mensajes por usuario al mes | **Bajar frecuencia** a 2 | Con 3 o más toques el clic de email cae a 0.48 % (2 toques: 1.76 %) |
| Sin señal, email a más de 1 M de usuarios por envío | **Rehacer**: dividir en segmentos | Arriba de 1 M de audiencia el clic cae 5 veces |
| Cobranza o transaccional | **No tocar** | Su resultado es el pago o la operación, no la respuesta; solo vigilar que no incluya dados de baja (E5b) |
| Resto | **Seguir igual** | Respuesta en rango o volumen bajo |

Cada "por qué" agrega, cuando aplica: cuánto convierten quienes abren y quienes no (E7c), qué parte de los envíos va a prospectos sin crédito (E7a, si 60 % o más), cuántos emails llegaron a dados de baja (E5b, si 500 o más) y cuántos envíos fueron a REUS o ARCO, lista negra o tarjeta congelada (E7a, si 10 mil o más).

### Resumen por acción

| Qué hacer | Familias | Activas en sep. | Envíos al mes (activas) | Ahorro MXN al mes | WA no entregado MXN |
|---|---|---|---|---|---|
| Apagar | 50 | 50 | 19.6 M | 2.6 M | 4.5 M |
| Limpiar base de WhatsApp | 45 | 19 | 1.7 M | 417 mil | 3.8 M |
| Rehacer o re-segmentar | 181 | 64 | 15.9 M | 203 mil |  |
| Bajar frecuencia | 41 | 14 | 2.8 M |  |  |
| Confirmar apagado | 251 | 0 |  |  | 2.0 M |
| Proteger | 152 | 54 | 5.5 M |  |  |
| Escalar | 150 | 46 | 415 mil |  |  |
| No tocar | 289 | 118 | 12.1 M |  | 1 mil |
| Seguir igual | 758 | 116 | 6.9 M |  | 4.0 M |

Lectura: el ahorro en dinero está casi todo en **Apagar** (50 familias activas, 2.6 M MXN al mes, casi todo WhatsApp donde ni quien lee convierte) y en **Limpiar base de WhatsApp** (417 mil MXN al mes más lo que se recupera de los no entregados). **Rehacer** y **Bajar frecuencia** casi no ahorran dinero (push no cuesta) pero quitan 18.6 M mensajes al mes de encima de los usuarios, que es donde están la fatiga y las bajas.

### Las 22 activas donde primero hay que actuar

Las 12 con más ahorro al mes y las 10 de mayor volumen entre las que no ahorran dinero pero sí mensajes.

| Familia | Canal | Envíos al mes | Qué hacer | Por qué |
|---|---|---|---|---|
| Marketing-KCash-B0171-CANVAS-Leads_BBDDRezagada-RescateTasa0-N/A | whatsapp | 868 mil | **Apagar.** Apagar el WhatsApp de esta familia; mantener el contacto por email (clic 0.52 %), in-app (clic 29.3 %). | Lectura 57.7 % con mínimo 60 %, entrega 62.8 %. Cuesta 868 mil MXN al mes. Quienes lo leen convierten 1.07 % y quienes no 0.24 % (4.5 veces); lo normal en WhatsApp es 6.1 % entre quienes leen. Ni quien lo lee convierte: no hay a quién acotar la base. Se pagaron 1.9 M MXN de mensajes que no se entregaron. Ahorro: 868 mil MXN al mes. 22 mil envíos fueron a usuarios en REUS o ARCO, lista negra o con tarjeta congelada: excluirlos del segmento. |
| Lending-KPay-B0333-CANVAS-Churn_12MesesInactividad-ConSinOferta-N/A | whatsapp | 331 mil | **Apagar.** Apagar el WhatsApp de esta familia; si hace falta tocar a esta base, usar push o in-app, que no cuestan. | Lectura 48.9 % con mínimo 60 %, entrega 73.8 %. Cuesta 331 mil MXN al mes. Quienes lo leen convierten 0.69 % y quienes no 0.34 % (2.0 veces); lo normal en WhatsApp es 6.1 % entre quienes leen. Ni quien lo lee convierte: no hay a quién acotar la base. El 88 % de sus envíos con etapa conocida va a prospectos sin crédito (E7a). Se pagaron 608 mil MXN de mensajes que no se entregaron. Ahorro: 331 mil MXN al mes. 284 mil envíos fueron a usuarios en REUS o ARCO, lista negra o con tarjeta congelada: excluirlos del segmento. |
| Lending-KCash-B0209-CANVAS-Recurrentes_Inactivos-DescuentoDirecto-N/A | whatsapp | 258 mil | **Apagar.** Apagar el WhatsApp de esta familia; mantener el contacto por email (clic 0.54 %), push (apertura 1.19 %), in-app (clic 19.8 %). | Lectura 59.8 % con mínimo 60 %, entrega 63.5 %. Cuesta 258 mil MXN al mes. Quienes lo leen convierten 2.28 % y quienes no 0.52 % (4.4 veces); lo normal en WhatsApp es 6.1 % entre quienes leen. Ni quien lo lee convierte: no hay a quién acotar la base. Se pagaron 847 mil MXN de mensajes que no se entregaron. Ahorro: 258 mil MXN al mes. 42 mil envíos fueron a usuarios en REUS o ARCO, lista negra o con tarjeta congelada: excluirlos del segmento. |
| Lending-KCash-B0223-CANVAS-Nuevos_NeverActive-InstallmentsNoCash-N/A | whatsapp | 206 mil | **Apagar.** Apagar el WhatsApp de esta familia; mantener el contacto por in-app (clic 18.1 %). | Lectura 50.8 % con mínimo 60 %, entrega 52.1 %. Cuesta 206 mil MXN al mes. Quienes lo leen convierten 0.15 % y quienes no 0.02 % (7.5 veces); lo normal en WhatsApp es 6.1 % entre quienes leen. Ni quien lo lee convierte: no hay a quién acotar la base. El 89 % de sus envíos con etapa conocida va a prospectos sin crédito (E7a). Se pagaron 886 mil MXN de mensajes que no se entregaron. Ahorro: 206 mil MXN al mes. 41 mil envíos fueron a usuarios en REUS o ARCO, lista negra o con tarjeta congelada: excluirlos del segmento. |
| Lending-KCash-B0211-CANVAS-Nuevos_RegistradosPay-Tasa0-N/A | email | 3.9 M | **Apagar.** Apagar el email de esta familia; dejar solo in-app (clic 32.5 %). | Clic 0.25 % con mínimo 0.3 %, 3.9 M envíos al mes, 4.8 mensajes por usuario al mes. Quienes lo abren convierten 0.47 % y quienes no 0.12 % (3.9 veces); lo normal en email es 8.3 % entre quienes abren. Ni quien lo abre convierte: no hay a quién acotar la base. Ahorro: 194 mil MXN al mes. Además llegaron 8 mil emails a usuarios que ya se habían dado de baja: revisar el filtro de suscripción del Canvas. 104 mil envíos fueron a usuarios en REUS o ARCO, lista negra o con tarjeta congelada: excluirlos del segmento. |
| Lending-KPay-202600903-B0332-CANVAS-HardInactive_6MesesInactividad-ConSinOferta-N/A | whatsapp | 192 mil | **Apagar.** Apagar el WhatsApp de esta familia; mantener el contacto por push (apertura 0.99 %). | Lectura 51.8 % con mínimo 60 %, entrega 84.3 %. Cuesta 192 mil MXN al mes. Quienes lo leen convierten 2.68 % y quienes no 1.50 % (1.8 veces); lo normal en WhatsApp es 6.1 % entre quienes leen. Ni quien lo lee convierte: no hay a quién acotar la base. El 95 % de sus envíos con etapa conocida va a prospectos sin crédito (E7a). Se pagaron 30 mil MXN de mensajes que no se entregaron. Ahorro: 192 mil MXN al mes. |
| Lending-KPay-B0331-CANVAS-Medium_active-ConSinOferta-N/A | whatsapp | 151 mil | **Limpiar base de WhatsApp.** Limpiar la base (quitar números sin entrega) y enviar solo a quien leyó cualquier WhatsApp de Kueski en los últimos 90 días, no solo de esta campaña. | Lectura 57.4 % con mínimo 60 %, entrega 86.7 %. Cuesta 151 mil MXN al mes. Quienes lo leen convierten 9.19 % y quienes no 4.93 % (1.9 veces); lo normal en WhatsApp es 6.1 % entre quienes leen. Quien lo lee sí convierte: el problema es la base, no el mensaje. El 94 % de sus envíos con etapa conocida va a prospectos sin crédito (E7a). Se pagaron 20 mil MXN de mensajes que no se entregaron. |
| Lending-KCash-B0619-CANVAS-XSell_KPayToKCash-FiestasPatrias-N/A | whatsapp | 107 mil | **Apagar.** Apagar el WhatsApp de esta familia; mantener el contacto por in-app (clic 78.5 %). | Lectura 48.9 % con mínimo 60 %, entrega 74.5 %. Cuesta 107 mil MXN al mes. Quienes lo leen convierten 1.45 % y quienes no 0.55 % (2.6 veces); lo normal en WhatsApp es 6.1 % entre quienes leen. Ni quien lo lee convierte: no hay a quién acotar la base. El 91 % de sus envíos con etapa conocida va a prospectos sin crédito (E7a). Se pagaron 27 mil MXN de mensajes que no se entregaron. Ahorro: 107 mil MXN al mes. 10 mil envíos fueron a usuarios en REUS o ARCO, lista negra o con tarjeta congelada: excluirlos del segmento. |
| Marketing-KCash-B0171-CANVAS-Leads-BBDDHotLeadsW2RescateTasa0-N/A | whatsapp | 106 mil | **Limpiar base de WhatsApp.** Limpiar la base (quitar números sin entrega) y enviar solo a quien leyó cualquier WhatsApp de Kueski en los últimos 90 días, no solo de esta campaña. | Lectura 58.9 % con mínimo 60 %, entrega 69.0 %. Cuesta 106 mil MXN al mes. Quienes lo leen convierten 4.14 % y quienes no 1.59 % (2.6 veces); lo normal en WhatsApp es 6.1 % entre quienes leen. Quien lo lee sí convierte: el problema es la base, no el mensaje. Se pagaron 197 mil MXN de mensajes que no se entregaron. |
| Lending-KPay-B0620-CANVAS-Leads-XSellCashaPay-N/A | whatsapp | 93 mil | **Apagar.** Apagar el WhatsApp de esta familia; mantener el contacto por push (apertura 0.78 %). | Lectura 56.1 % con mínimo 60 %, entrega 70.7 %. Cuesta 93 mil MXN al mes. Quienes lo leen convierten 0.90 % y quienes no 0.43 % (2.1 veces); lo normal en WhatsApp es 6.1 % entre quienes leen. Ni quien lo lee convierte: no hay a quién acotar la base. Se pagaron 27 mil MXN de mensajes que no se entregaron. Ahorro: 93 mil MXN al mes. |
| Lending-KCash-B0223-CANVAS-Nuevos_NeverActive-InstallmentsNoCash-N/A | email | 1.7 M | **Apagar.** Apagar el email de esta familia; dejar solo in-app (clic 18.1 %). | Clic 0.09 % con mínimo 0.3 %, 1.7 M envíos al mes, 3.4 mensajes por usuario al mes. Quienes lo abren convierten 0.13 % y quienes no 0.03 % (4.3 veces); lo normal en email es 8.3 % entre quienes abren. Ni quien lo abre convierte: no hay a quién acotar la base. El 90 % de sus envíos con etapa conocida va a prospectos sin crédito (E7a). Ahorro: 84 mil MXN al mes. 299 mil envíos fueron a usuarios en REUS o ARCO, lista negra o con tarjeta congelada: excluirlos del segmento. |
| Lending-KCash-B0210-CANVAS-Nuevos_MPNeverCash-Tasa0-N/A | whatsapp | 57 mil | **Limpiar base de WhatsApp.** Limpiar la base (quitar números sin entrega) y enviar solo a quien leyó cualquier WhatsApp de Kueski en los últimos 90 días, no solo de esta campaña. | Lectura 52.4 % con mínimo 60 %, entrega 83.4 %. Cuesta 57 mil MXN al mes. Quienes lo leen convierten 4.81 % y quienes no 2.09 % (2.3 veces); lo normal en WhatsApp es 6.1 % entre quienes leen. Quien lo lee sí convierte: el problema es la base, no el mensaje. El 91 % de sus envíos con etapa conocida va a prospectos sin crédito (E7a). Se pagaron 85 mil MXN de mensajes que no se entregaron. 44 mil envíos fueron a usuarios en REUS o ARCO, lista negra o con tarjeta congelada: excluirlos del segmento. |
| Sales-KPay-B0615-CANVAS-Recurrentes-ComerciodeldiaSeptiembre-N/A | push notification | 1.9 M | **Rehacer o re-segmentar.** Probar copy y horario; acotar a quienes abrieron algún push de Kueski en 60 días. | Apertura 0.93 % debajo de la mediana 1.07 %, 1.9 M envíos al mes, 7.0 mensajes por usuario al mes. Quienes lo abren convierten 20.34 % y quienes no 5.83 % (3.5 veces); lo normal en push es 19.9 % entre quienes abren. 181 mil envíos fueron a usuarios en REUS o ARCO, lista negra o con tarjeta congelada: excluirlos del segmento. |
| Marketing-KCash-B0391-CANVAS-Leads_BDDMarketing-RescateFinesDeSemana-N/A | push notification | 1.9 M | **Rehacer o re-segmentar.** Probar copy y horario; acotar a quienes abrieron algún push de Kueski en 60 días. | Apertura 0.76 % debajo de la mediana 1.07 %, 1.9 M envíos al mes, 5.0 mensajes por usuario al mes. Quienes lo abren convierten 6.62 % y quienes no 0.97 % (6.8 veces); lo normal en push es 19.9 % entre quienes abren. 564 mil envíos fueron a usuarios en REUS o ARCO, lista negra o con tarjeta congelada: excluirlos del segmento. |
| Marketing-KCash-B0171-CANVAS-Anonimos-RescateTasa0-N/A | push notification | 1.5 M | **Apagar.** Apagar el push de esta familia; dejar in-app (clic 13.2 %). | Apertura 0.55 % con mínimo 0.75 %, 1.5 M envíos al mes, 4.8 mensajes por usuario al mes. Quienes lo abren convierten 7.50 % y quienes no 1.03 % (7.3 veces); lo normal en push es 19.9 % entre quienes abren. Ni quien lo abre convierte: no hay a quién acotar la base. No cuesta, pero gasta el permiso de push y suma fatiga: los usuarios más contactados generan 16 bajas por cada 100. 290 mil envíos fueron a usuarios en REUS o ARCO, lista negra o con tarjeta congelada: excluirlos del segmento. |
| Marketing-KPay-B0615-CANVAS-Leads-ComerciodeldiaSeptiembre-N/A | push notification | 1.3 M | **Apagar.** Apagar el push de esta familia; dejar email (clic 0.50 %). | Apertura 0.66 % con mínimo 0.75 %, 1.3 M envíos al mes, 6.5 mensajes por usuario al mes. Quienes lo abren convierten 6.69 % y quienes no 1.53 % (4.4 veces); lo normal en push es 19.9 % entre quienes abren. Ni quien lo abre convierte: no hay a quién acotar la base. No cuesta, pero gasta el permiso de push y suma fatiga: los usuarios más contactados generan 16 bajas por cada 100. |
| Marketing-KCash-B0000-CANVAS-Leads_LeftFunnel-Retargeting_Veriff | email | 1.1 M | **Bajar frecuencia.** Mantener el contenido, bajar a 2 emails al mes y excluir a quien no abrió ninguno de los últimos 3 envíos de esta campaña. | Clic 3.04 % está bien (mediana 0.5 %) pero genera 3.9 bajas por mil (umbral 2.5), 5.2 mensajes por usuario al mes. El mensaje funciona, la presión molesta. Quienes lo abren convierten 4.48 % y quienes no 2.58 % (1.7 veces); lo normal en email es 8.3 % entre quienes abren. Además llegaron 4 mil emails a usuarios que ya se habían dado de baja: revisar el filtro de suscripción del Canvas. 93 mil envíos fueron a usuarios en REUS o ARCO, lista negra o con tarjeta congelada: excluirlos del segmento. |
| Marketing-KCash-B0171-CANVAS-Leads_BBDDRezagada-RescateTasa0-N/A | push notification | 969 mil | **Apagar.** Apagar el push de esta familia; dejar email (clic 0.52 %), in-app (clic 29.3 %). | Apertura 0.55 % con mínimo 0.75 %, 969 mil envíos al mes, 2.5 mensajes por usuario al mes. Quienes lo abren convierten 6.30 % y quienes no 0.77 % (8.2 veces); lo normal en push es 19.9 % entre quienes abren. Ni quien lo abre convierte: no hay a quién acotar la base. No cuesta, pero gasta el permiso de push y suma fatiga: los usuarios más contactados generan 16 bajas por cada 100. 189 mil envíos fueron a usuarios en REUS o ARCO, lista negra o con tarjeta congelada: excluirlos del segmento. |
| Marketing-KPay-B00527-CANVAS-Leads-BillpaymentsOnboarding-N/A | push notification | 876 mil | **Rehacer o re-segmentar.** Re-segmentar: solo usuarios que abrieron cualquier push de Kueski en los últimos 60 días (no solo de esta campaña), máximo 2 al mes. | Apertura 0.73 % con mínimo 0.75 %, 876 mil envíos al mes. Quienes lo abren convierten 12.43 % y quienes no 3.05 % (4.1 veces); lo normal en push es 19.9 % entre quienes abren. Quien lo abre sí convierte: el problema es a quién y cuántas veces se manda. El 72 % de sus envíos con etapa conocida va a prospectos sin crédito (E7a). 108 mil envíos fueron a usuarios en REUS o ARCO, lista negra o con tarjeta congelada: excluirlos del segmento. |
| Sales-KPay-B0622-CANVAS-Recurrentes-KUESKIPROMOTORInstore-N/A | push notification | 617 mil | **Rehacer o re-segmentar.** Re-segmentar: solo usuarios que abrieron cualquier push de Kueski en los últimos 60 días (no solo de esta campaña), máximo 2 al mes. | Apertura 0.65 % con mínimo 0.75 %, 617 mil envíos al mes, 4.1 mensajes por usuario al mes. Quienes lo abren convierten 19.88 % y quienes no 5.71 % (3.5 veces); lo normal en push es 19.9 % entre quienes abren. Quien lo abre sí convierte: el problema es a quién y cuántas veces se manda. El 69 % de sus envíos con etapa conocida va a prospectos sin crédito (E7a). 190 mil envíos fueron a usuarios en REUS o ARCO, lista negra o con tarjeta congelada: excluirlos del segmento. |
| Lending-KCash-B0211-CANVAS-Nuevos_RegistradosPay-Tasa0-N/A | push notification | 566 mil | **Apagar.** Apagar el push de esta familia; dejar in-app (clic 32.5 %). | Apertura 0.48 % con mínimo 0.75 %, 566 mil envíos al mes, 4.1 mensajes por usuario al mes. Quienes lo abren convierten 5.98 % y quienes no 0.33 % (18.1 veces); lo normal en push es 19.9 % entre quienes abren. Ni quien lo abre convierte: no hay a quién acotar la base. No cuesta, pero gasta el permiso de push y suma fatiga: los usuarios más contactados generan 16 bajas por cada 100. 33 mil envíos fueron a usuarios en REUS o ARCO, lista negra o con tarjeta congelada: excluirlos del segmento. |
| Sales-KPay-B0599-CANVAS-Recurrentes-VentaAzulAeromexico-N/A | push notification | 560 mil | **Rehacer o re-segmentar.** Re-segmentar: solo usuarios que abrieron cualquier push de Kueski en los últimos 60 días (no solo de esta campaña), máximo 2 al mes. | Apertura 0.73 % con mínimo 0.75 %, 560 mil envíos al mes, 2.1 mensajes por usuario al mes. Quienes lo abren convierten 23.03 % y quienes no 9.16 % (2.5 veces); lo normal en push es 19.9 % entre quienes abren. Quien lo abre sí convierte: el problema es a quién y cuántas veces se manda. El 91 % de sus envíos con etapa conocida va a prospectos sin crédito (E7a). 49 mil envíos fueron a usuarios en REUS o ARCO, lista negra o con tarjeta congelada: excluirlos del segmento. |

Cruce con las decisiones ya tomadas: Retargeting_Veriff sale como **Bajar frecuencia** (clic 3.04 %, 3.9 bajas por mil, 5.2 emails por usuario al mes; quienes abren convierten 4.5 % contra 2.6 %). Dormants referral (B0326) sale como **Apagar** en email: quienes abren convierten 1.1 a 3.1 %, menos de la mitad de lo normal en email (8.3 %), así que no hay a quién acotar.

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
