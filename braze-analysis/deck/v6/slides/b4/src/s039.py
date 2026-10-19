"""Lámina 39: cierre de la sección IV. Cifras de E6a, E6b, E12 y MUESTRA_C (familias activas en septiembre)."""
import pandas as pd
from kit import *
a = pd.read_csv(D + 'e6a_solape_dia_mes.csv'); a['m'] = a.mes.str[5:7].astype(int)
hi = a[a.banda_familias_dia.isin(['3 a 4', '5 a 7', '8+'])]
sep = hi[hi.m == 9].usuarios_aprox.sum() / 1e6
js = a[a.m.isin([7, 8, 9])].groupby('banda_familias_dia')[['usuario_dias', 'usuario_dias_con_baja']].sum()
js = 1000 * js.usuario_dias_con_baja / js.usuario_dias
c = pd.read_csv(R + 'hallazgos/muestra_c_familias.csv'); act = c[c.activo_sep == 1]
menos = act[act.accion_tipo.isin(['Rehacer o re-segmentar', 'Bajar frecuencia'])].envios_mes_prom.sum() / 1e6
print(sep, js.round(2).to_dict(), menos)
write(39, dict(kind='cierre', seccion='IV. La misma persona, demasiadas veces',
 titulo='Qué lo explica: no hay un límite de mensajes por persona ni un calendario común entre equipos',
 porques=[
  f'Un cuarto de la base recibe 86 %; hasta 2.3 M al mes tienen días de 3 o más campañas.',
  'Le llegan promociones de dos o tres equipos el mismo día, y a veces la misma dos veces.',
  'Cada equipo nombra su audiencia y nadie excluye a quien ya recibió la de otro equipo.',
  'Las versiones viejas siguen activas y el push sigue saliendo a quien ya no lo abre.',
  'Causa raíz: el límite global de Braze está apagado y nadie es dueño del calendario.',
 ],
 hipotesis={
  'A': f'Con 2 promocionales al día, las bajas bajan de {js["8+"]:.2f} a cerca de {js["1"]:.2f} por mil personas-día.',
  'O': 'Sin repetir campaña el mismo día y sin versiones viejas, se van 9.9 M personas-día repetidas.',
  'G': 'Con un solo dueño del calendario, los lanzamientos de cuatro equipos no caen en la misma persona.',
 },
 como=[
  'Semanas 1 a 4, Braze: no repetir campaña el mismo día; apagar versiones viejas. Cada equipo.',
  'Semanas 1 a 4: apagar el push que no se abre, con 10 % sin mensajes; una sola bienvenida.',
  'Mes 2, Braze: máximo 2 promocionales y 1 push promocional al día por persona. MarTech y Datos.',
  'Mes 2: calendario único para envíos de más de 1 M; medir personas con 3 o más campañas al día.',
 ],
 impacto=f'Unos {menos:.0f} M mensajes menos al mes, 0.02 M MXN al mes de WhatsApp repetido y menos bajas en días saturados.',
 sowhat='Se corrige con reglas en Braze y un dueño del calendario, no campaña por campaña.',
 fuente='Fuente: Braze, enero a septiembre 2026: E3, E6a, E6b y E12. Mensajes menos al mes: campañas activas en septiembre marcadas para rehacer o bajar frecuencia (MUESTRA_C).'))
