"""Lámina 22: aprobada (muestras/s2.json). Se conserva el SVG; solo se recorta el texto (ronda 2, ESTANDAR.md)."""
import json
from svgk import OUT, check
p = OUT / '022.json'; d = json.loads(p.read_text(encoding='utf-8'))
d.update(
  que='A quien no ha hecho nada: Tasa 0, rescates, promociones de KPay. A quien sí: avisos.',
  quien='Los cinco equipos; Others es BillPay, avisos de KPay y KCash, Shopping y pruebas de QA.',
  a_quien='Hizo algo: registro a medias, cliente activo, pago por vencer. No: leads fríos, inactivos.',
  lecturas=['Product Growth: 88 M de sus 173 M mensajes (51 %) van a quien no ha hecho nada y no responde.',
            'Marketing: 85 M en esa situación; el mayor es el rescate de Tasa 0 por push a anónimos (8.9 M).',
            'Si el mensaje sale porque la persona hizo algo, responde lo mínimo 8 de cada 10 veces; si no, 4 de 10.'],
  causa='Las campañas se arman para listas grandes y no a partir de algo que la persona acaba de hacer.',
  sowhat='Dejar de mandar esos 173 M mensajes a quien no responde y escribir cuando la persona hace algo.',
  fuente='Fuente: Braze, envíos por campaña, mes y canal, enero a septiembre 2026; campañas con 50 mil o más entregados (657 M mensajes). A quién, según el nombre de la campaña.')
p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')
check(22)
