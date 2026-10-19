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
  f'El 1 de junio el clic cayó a {clic["2026-06-01"]:.2f} %; en junio salieron {cj["new_env"]/1e6:.0f} M push nuevos.',
  'Los picos son lanzamientos y temporadas a toda la base que caen la misma semana.',
  'Cada equipo fija su fecha sin ver las de los demás; BillPay salió por dos equipos.',
  'El reporte es mensual: promedia el golpe y llega cuatro semanas tarde.',
  'Causa raíz: no hay calendario único ni límite semanal por canal con dueño.',
 ],
 hipotesis={
  'A': f'Con menos correos por semana sube el clic: cada millón de más lo baja {abs(fe["b"]):.2f} puntos.',
  'O': 'Si todo envío de más de 1 M sale primero a 10 %, un correo como BillPay Intro se frena a tiempo.',
  'G': 'Con un solo dueño del calendario no caen tres lanzamientos a toda la base la misma semana.',
 },
 como=[
  'Semana 1, Braze: límite semanal por canal y un solo envío a toda la base por semana. CRM.',
  'Semana 2: calendario único de lanzamientos de los cuatro equipos, con fecha aprobada. CRM.',
  'Semana 3, Braze: todo envío de más de 1 M sale primero a 10 % con grupo sin mensajes.',
  'Semana 4: lectura semanal por campaña con alerta; el día se cambia solo con prueba.',
 ],
 impacto=f'Evitar semanas como la del 1 de junio: un correo de 0.8 M MXN y {bi_p/1e3:.0f} mil personas dadas de baja.',
 sowhat='Coordinar las fechas vale más que elegir el día.',
 fuente='Fuente: Braze, enero a septiembre 2026: E4a (serie semanal), E1 (campañas por mes), E8 (bajas desde BillPay Intro) y E10 (día de la semana).'))
