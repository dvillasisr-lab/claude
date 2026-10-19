"""Lámina 27 (ronda 2): ficha de Product Growth (Lending en Braze). Gráfica común en ficha2.py."""
from ficha2 import *
CASOS = [('Recordatorio de Installments a activos', 'B0301-CANVAS-Active-Retargeting_Installments_SP', 'push notification', 'b', -40, -22),
         ('El mismo recordatorio por correo', 'B0301-CANVAS-Active-Retargeting_Installments_SP', 'email', 'b', 30, -26),
         ('Anota y gana por in-app', 'KCash-B0440-CANVAS-Todos-AnotayGana', 'in-app', 'b', -30, -20),
         ('Tasa 0 a registrados sin crédito', 'B0211-CANVAS-Nuevos_RegistradosPay', 'email', 'w', -10, 112),
         ('Installments a quien nunca activó', 'B0223-CANVAS-Nuevos_NeverActive', 'email', 'w', -10, 44),
         ('Churn de KPay por WhatsApp', 'B0333-CANVAS-Churn', 'whatsapp', 'w', -30, 50)]
svg, d, det = build('Product Growth', CASOS)
for k, z in det.items(): print(k, z.canal, round(z.env / 1e6, 2), round(z.resp_pct, 2), round(z.vs_min, 2), round(z.costo / 1e6, 2), round(z.costo / max(z.convf, 1), 0))
save(27, dict(kind='grafica',
  titulo='Product Growth acierta al recordar Installments a quien lo empezó y no al ofrecer crédito a quien no lo pidió',
  que='Crédito e Installments, Tasa 0 a registrados, recuperar ex clientes y concursos.',
  quien='Product Growth (Lending en Braze): 186 campañas, 177 M mensajes, 17.3 M MXN.',
  a_quien='Registrados sin crédito 38 %, clientes 29 %, ex clientes inactivos 16 %, todos 12 %.',
  lecturas=[
   'Recordatorio de Installments a activos: 11 % de apertura en push y 2.78 % de clic en correo, a 2.7 MXN por préstamo.',
   'Tasa 0 a registrados: 34.9 M correos con 0.28 % de clic, 1.75 M MXN y 656 MXN por préstamo o solicitud de Cash.',
   'Churn de KPay: lee el WhatsApp (52 %) pero solo 74 % se entrega; 1.71 M MXN en nueve meses.'],
  causa='Las ofertas de crédito salen por correo a listas completas, no a partir de algo que la persona hizo.',
  sowhat='Sacar del correo la Tasa 0 a registrados y ampliar el recordatorio de Installments a quien ya lo empezó.',
  fuente='Fuente: Braze, envíos por campaña, mes y canal, enero a septiembre 2026; campañas con 50 mil o más entregados. Préstamo o solicitud de Cash en 7 días: referencia.',
  svg=svg))
check(27)
