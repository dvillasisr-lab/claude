"""Lámina 32: cierre de la sección III. Cifras de las láminas 21 a 31 (scripts s021 a s031) y del caso de negocio aprobado (muestras/s3.json)."""
from svgk import save, check
save(32, dict(kind='cierre',
  titulo='Por qué pasa: cada equipo persigue su meta con su canal, sin ver el costo ni lo que mandan los demás',
  porques=[
   'Marketing y Product Growth mandan dos de cada tres mensajes, y siete de cada diez van a gente que no ha hecho nada reciente.',
   'Cuando el mensaje va a quien no ha hecho nada, responde lo mínimo aceptable 39 % de las veces; cuando sale porque la persona hizo algo, 79 %.',
   'Dos equipos le escriben a la misma persona el mismo día con la misma oferta (Tasa 0, descuentos, promociones de KPay), porque nadie ve lo que manda el otro.',
   'Cada equipo mide su meta (préstamos, compras con KPay, registros) por su canal, no el costo por resultado ni las bajas que provoca.',
   'Causa raíz: la gente que no ha hecho nada y las promociones de KPay no tienen un dueño, ni un calendario ni un límite de gasto por equipo.'],
  hipotesis={
   'A': 'El resultado depende de a quién y qué se manda, no del equipo: a quién explica 54 % de la diferencia de respuesta entre correos y el equipo 12 %.',
   'O': 'Dos equipos arman la misma oferta para la misma base y la mandan por correo a toda la lista, el canal por defecto.',
   'G': 'No hay dueño por grupo de personas, ni calendario común, ni límite mensual de gasto en WhatsApp por equipo.'},
  como=[
   'Semanas 1 y 2: tablero común por equipo con costo por respuesta, bajas por mil correos y préstamos o solicitudes de Cash por campaña (equipo de análisis).',
   'Semanas 3 y 4: Product Growth queda como dueño de inactivos, dormidos y churn; un solo dueño de promociones de KPay entre Marketing y Sales.',
   'En Braze: límite mensual de gasto en WhatsApp por equipo y calendario compartido para cualquier envío a más de 1 M de personas.',
   'En Braze: límite de mensajes por persona a la semana entre equipos, y en la primera semana del usuario nuevo un correo al día y tres en total.',
   'Métrica semanal: parte de los mensajes de cada equipo que responde lo mínimo aceptable y bajas por cada mil correos.'],
  impacto='Hasta 2.34 M MXN al mes menos de gasto en mensajes, casi todo en Product Growth (1.57 M) y Marketing (0.50 M), y menos bajas: esos dos equipos provocan 73 % de las bajas de correo medidas.',
  sowhat='Dar dueño, calendario y límite de gasto a la gente que no ha hecho nada y a las promociones de KPay corrige a los cinco equipos a la vez.',
  fuente='Fuente: láminas 21 a 31 (Braze, enero a septiembre 2026) y caso de negocio (ahorro por equipo al mes, septiembre 2026; WhatsApp a 1.00 MXN por entregado, correo a 0.05 por enviado).'))
check(32)
