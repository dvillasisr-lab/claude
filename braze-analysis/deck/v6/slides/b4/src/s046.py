"""Lámina 46: cierre de la sección V. Cifras de E4a, E1, E8 y deck_data.regresion_semana."""
import sys, pandas as pd
from kit import *
sys.path.insert(0, R + 'scripts')
import deck_data as dd
fe = dd.regresion_semana()['email']['fit']
e = pd.read_csv(D + 'e4a_serie_semana_mes_canal.csv'); w = e[(e.grano == 'semana') & (e.canal == 'email')].set_index('periodo')
clic = 100 * w.email_click / w.email_delivery
e8 = pd.read_csv(D + 'e8_dias_hasta_baja.csv'); bi_p = e8[(e8.bloque == 'familia_dia_baja') & e8.clave.str.contains('BillPay_Intro')].usuarios.sum()
cj = dd.culpables_push_junio()
print(clic['2026-06-01'], clic['2026-06-08'], bi_p, cj['new_env'] / 1e6, fe)
write(46, dict(kind='cierre', seccion='V. El ritmo lo marcan los lanzamientos, no el cliente',
 titulo='Por qué pasa: no hay un límite semanal de mensajes ni una revisión semanal, y los lanzamientos no se coordinan',
 porques=[
  f'La semana del 1 de junio el clic de correo cayó a {clic["2026-06-01"]:.2f} % y la siguiente volvió a {clic["2026-06-08"]:.2f} %; en junio salieron {cj["new_env"]/1e6:.0f} M push nuevos que abrieron 0.87 %.',
  'Los picos de volumen son lanzamientos y temporadas a toda la base (BillPay, Hot Sale, Mundial, Día del Padre, Navidad) que caen la misma semana.',
  'Cada equipo fija la fecha de su lanzamiento sin ver la de los demás; BillPay salió por dos equipos y cuatro veces en un mes.',
  'El reporte es mensual: promedia el golpe y se lee cuatro semanas tarde, cuando ya salió lo que sigue.',
  'Causa raíz: no hay un calendario único de lanzamientos ni un límite semanal de mensajes por canal con dueño que lo vigile.',
 ],
 hipotesis={
  'A': f'Si limitamos los correos de la semana, el clic sube: cada millón de correos de más en la semana lo baja {abs(fe["b"]):.2f} puntos (R² {fe["r2"]:.2f}).',
  'O': 'Si cada envío de más de 1 M de personas sale primero a 10 % y se lee en su primera semana, un correo como BillPay Intro se frena antes de llegar a 16.1 M.',
  'G': 'Si un solo equipo de CRM administra el calendario, no caen tres lanzamientos a toda la base en la misma semana; el día de la semana se decide solo con prueba.',
 },
 como=[
  'Semana 1, Braze (límite de velocidad de envío y límite global de frecuencia): límite semanal por canal y máximo un envío a toda la base por semana. Equipo de CRM.',
  'Semana 2: calendario único de lanzamientos para Marketing, Sales, Product Growth y NewProducts; ningún envío de más de 1 M sin fecha aprobada. Dueño: CRM.',
  'Semana 3, Braze (pruebas A/B con grupo sin mensajes): todo envío de más de 1 M sale primero a 10 %; sigue solo si llega a 3 clics por cada mil correos o 7.5 aperturas por cada mil push.',
  'Semana 4: lectura semanal por campaña con alerta en la primera semana. Métrica: clic de correo y apertura de push por semana, y bajas por semana.',
  'Día de la semana: no mover envíos sin probar la misma campaña en dos días con grupo sin mensajes; el lunes se arregla quitando el envío a toda la base, no el lunes.',
 ],
 impacto=f'Evitar semanas como la del 1 de junio: sin BillPay Intro su clic habría sido 0.79 % y no {clic["2026-06-01"]:.2f} %; ese correo costó 0.8 M MXN y desde él se dieron de baja {bi_p/1e3:.0f} mil personas.',
 sowhat='Coordinar las fechas vale más que elegir el día.',
 fuente='Fuente: Braze, enero a septiembre 2026: E4a (serie semanal), E1 (campañas por mes), E8 (personas que se dieron de baja desde BillPay Intro), E10 (día de la semana); regresión semanal de 38 semanas.'))
