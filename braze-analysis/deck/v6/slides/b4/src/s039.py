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
 titulo='Por qué pasa: no hay un límite de mensajes por persona ni un calendario común; cada campaña se suma sin ver las demás',
 porques=[
  f'Una cuarta parte de la base recibe 86 % de los mensajes y en septiembre {sep:.2f} M personas tuvieron al menos un día con tres o más campañas.',
  'Le llegan promociones de dos o tres equipos el mismo día, y a veces la misma campaña dos veces.',
  'Cada equipo arma su audiencia con su propio nombre y nadie excluye a quien ya recibió la campaña de otro equipo.',
  'Las versiones viejas siguen activas cuando se crea la nueva, y el push se sigue mandando a quien dejó de abrirlo.',
  'Causa raíz: el límite global de mensajes por persona de Braze está apagado y nadie es dueño del calendario.',
 ],
 hipotesis={
  'A': f'Si limitamos a dos promocionales por persona al día, las bajas de los días saturados regresan al nivel del día con una campaña ({js["1"]:.2f} por mil personas-día, contra {js["8+"]:.2f} con ocho o más).',
  'O': 'Si Braze no deja repetir la misma campaña a la misma persona el mismo día y se apagan las versiones viejas, desaparecen los 9.9 M personas-día repetidos sin tocar el contenido.',
  'G': 'Si un solo equipo de CRM es dueño del calendario y de los límites, los lanzamientos de Marketing, Sales, Product Growth y NewProducts dejan de caer sobre la misma persona.',
 },
 como=[
  'Semana 1, Braze (límite global de frecuencia): máximo 2 promocionales al día y 1 push promocional al día por persona; cobranza y avisos de servicio quedan fuera, con una sola versión activa. Equipo de CRM.',
  'Semana 2, Braze (reglas de reingreso y exclusiones): no repetir la misma campaña a la misma persona el mismo día; apagar las versiones viejas de Rescate Tasa 0, Mundial, churn y desembolso. Cada equipo dueño.',
  'Semana 3, Braze (segmentos): push solo a quien abrió uno en los últimos 90 días; una sola serie de bienvenida para el nuevo. Marketing y Product Growth.',
  'Semana 4: calendario único para envíos de más de 1 M de personas y 5 promocionales a la semana como punto de partida. Métrica semanal: personas con 3 o más campañas al día, bajas por mil personas-día y apertura de push en la base de más de 6 meses.',
 ],
 impacto=f'Unos {menos:.0f} M mensajes menos al mes al rehacer y bajar frecuencia, 0.75 M MXN de WhatsApp repetido en 9 meses (unos 83 mil MXN al mes) y menos bajas en los días saturados.',
 sowhat='Se corrige con reglas en Braze y un dueño del calendario, no campaña por campaña.',
 fuente='Fuente: Braze, enero a septiembre 2026: E3, E6a, E6b, E12; mensajes menos al mes: campañas activas en septiembre con acción "rehacer" o "bajar frecuencia" (MUESTRA_C). El límite de 5 por semana es un punto de partida (METRICAS.md), no sale de un dato semanal; el de 2 por día sí tiene dato (E6a).'))
