"""Lámina 31 (ronda 2): ficha de Others (BillPay y recargas de NewProducts, avisos de KPay y KCash, Shopping, Compliance, CX,
Acquisition y QA). Gráfica común en ficha2.py. Puntos arriba de 40 veces el mínimo o debajo de 0.02 se dibujan en el borde."""
from ficha2 import *
CASOS = [('Aviso de rechazo de KPay (fuera de escala)', 'Transaccional-KPay-Mail-Rejections', 'email', 'b', -12, 16),
         ('Lanzamiento de BillPay por in-app', 'IA-Portfolio_BillPay_Intro_Full_Rollout', 'in-app', 'b', -12, 24),
         ('Confirmación de pago de KPay', 'Transaccional-KPay-Mail-Payment-Confirmation', 'email', 'b', -12, -30),
         ('El mismo lanzamiento por correo', 'E-Portfolio_BillPay_Intro_Full_Rollout', 'email', 'w', -12, 40, costo),
         ('Recomendaciones semanales de Shopping', 'Shopping-KPay-S0004-CAMPAIGN-WeeklyRecommendations', 'email', 'w', -12, 80),
         ('Prueba QA que llegó a clientes', 'QA-KPay-B001-CANVAS-Todos-ReminderRegistroTelefono', 'push notification', 'w', -12, -20)]
svg, d, det = build('Others', CASOS)
for k, z in det.items(): print(k, z.canal, round(z.env / 1e6, 2), round(z.resp_pct, 3), round(z.vs_min, 2))
save(31, dict(kind='grafica',
  titulo='En Others, el mismo lanzamiento de BillPay tuvo 85 % de clic por in-app y casi ninguno por correo',
  que='Avisos de pago y cuenta, lanzamiento de BillPay y recargas, Shopping, pruebas QA.',
  quien='BillPay (NewProducts), avisos de KPay y KCash, Shopping, CX y QA: 98 M mensajes.',
  a_quien='Avisos por algo que la persona hizo 52 %, envíos a toda la base 35 %.',
  lecturas=[
   'BillPay: 85 % de clic en in-app y 1 por cada mil en 16.1 M correos; 58 mil personas se dieron de baja ese día.',
   'Sus avisos responden lo mínimo en 92 % de los mensajes: el rechazo de KPay tiene 18.6 % de clic.',
   'Recomendaciones de Shopping: 7.0 M correos con 0.12 % de clic; una prueba QA llegó a 1.9 M clientes.'],
  causa='Lanzamientos y recomendaciones salen por correo a toda la base sin probar antes con un grupo chico.',
  sowhat='Avisos sin cambios; lanzamientos primero por in-app y por correo solo a quien abrió algo en 90 días.',
  fuente='Fuente: Braze, envíos por campaña, mes y canal, enero a septiembre 2026; campañas con 50 mil o más entregados. Bajas de BillPay por día de la baja (E8).',
  svg=svg))
check(31)
