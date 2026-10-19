"""Lámina 32: cierre de la sección III (ronda 2, textos cortos). Cifras de las láminas 21 a 31 y del caso de negocio (muestras/s3.json)."""
from svgk import save, check
save(32, dict(kind='cierre',
  titulo='Por qué pasa: cada equipo persigue su meta con su canal, sin ver el costo ni lo que mandan los demás',
  porques=[
   'Marketing y Product Growth mandan dos de cada tres mensajes, casi todos ofertas.',
   'A quien no ha hecho nada le responde lo mínimo 39 % de los mensajes; a quien sí, 79 %.',
   'Dos equipos mandan la misma oferta a la misma persona el mismo día.',
   'Cada equipo mide su meta en su canal, no el costo por resultado ni las bajas.',
   'Causa raíz: la gente que no ha hecho nada y las promociones de KPay no tienen dueño.'],
  hipotesis={
   'A': 'El resultado depende de a quién se manda: explica 54 % de la diferencia; el equipo, 12 %.',
   'O': 'Dos equipos arman la misma oferta para la misma base y la mandan por correo a toda la lista.',
   'G': 'No hay dueño por grupo de personas, calendario común ni límite de gasto por equipo.'},
  como=[
   'Semanas 1 y 2: tablero por equipo con costo por respuesta, bajas y préstamos por campaña.',
   'Semanas 3 y 4: Product Growth dueño de ex clientes; un dueño de promociones de KPay.',
   'En Braze: límite mensual de WhatsApp por equipo y calendario para envíos a más de 1 M.',
   'Métrica semanal: parte de los mensajes que responde lo mínimo y bajas por mil correos.'],
  impacto='Hasta 2.34 M MXN al mes menos en mensajes: 1.57 M de Product Growth y 0.50 M de Marketing.',
  sowhat='Dar dueño, calendario y límite de gasto a la gente que no ha hecho nada corrige a los cinco equipos.',
  fuente='Fuente: láminas 21 a 31 (Braze, enero a septiembre 2026) y caso de negocio (ahorro por equipo al mes, septiembre 2026).'))
check(32)
