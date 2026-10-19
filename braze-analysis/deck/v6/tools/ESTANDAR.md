# Estándar de gráficas y texto del deck v6 (lo que el usuario sí aprobó)

## Las gráficas que le gustan (referencia obligatoria; míralas con Read)
deck/v6/tools/ref/s06.png s07.png s27.png s29.png s36.png s39.png s41.png s43.png (láminas 6, 7, 27, 29, 36, 39, 41 y 43 del deck v5; su código está en scripts/build_deck.py, deck_content.py y deck_exhibits.py).
Lo que tienen en común, y que TODA gráfica analítica del deck debe cumplir:
1. La unidad es granular: cada punto es una campaña, una semana, un paso de Canvas, un día por equipo o un mes por campaña. Se ven decenas o cientos de puntos, no 4 a 6 barras de categorías.
2. Muestra la relación entre dos medidas (volumen contra respuesta, tamaño contra clic, posición contra apertura, acumulado de volumen contra acumulado de respuesta, tiempo contra índice), con una estadística clara: recta y R², mediana y mitad central, curva de Pareto, línea del mínimo aceptable, índice enero = 100.
3. Pequeños múltiplos con la misma escala cuando hay canales o equipos (correo | push; un panel por canal; una fila por equipo).
4. Los casos que importan van nombrados sobre la gráfica (campaña limpia, equipo, cifra), con línea guía si hace falta. Gris para el contexto, azul o verde para lo que prueba el título.
5. Una sola gráfica que llena el área (o 2 a 4 paneles iguales). Nada de mezclar una tabla, unas barras y un mapa en la misma lámina.
6. Prohibido: barras al 100 %, mekko, donas, tablas como gráfica principal (salvo resumen, plan y anexo), barras de una variable por categoría, mapas de calor con texto en cada celda como única gráfica.
Formas buenas: dispersión con recta, franja de puntos (strip/beeswarm) por equipo, Pareto acumulado, índice semanal en pequeños múltiplos, mapa campaña por mes con la celda marcada, pendientes (slope) con muchas líneas, mancuernas con muchas filas, cascada (solo caso de negocio), Gantt (solo plan).

## Texto: mucho menos (el usuario dijo "está feo, mucho texto")
Revisa con: python3 /home/user/claude/braze-analysis/deck/v6/tools/lint.py RUTA.json  (debe decir OK)
- título: máx. 110 caracteres, una idea, a lo más una cifra con unidad.
- que / quien / a_quien: máx. 90 caracteres cada uno (una línea corta; nombres de temas, equipos y segmentos, sin cifras salvo una).
- lecturas: exactamente 3, máx. 120 caracteres cada una; empieza con la cifra o el nombre, sin rodeos.
- causa: máx. 130 caracteres. sowhat: máx. 110 caracteres. fuente: máx. 220 caracteres.
- Láminas de resumen y decisiones: visuales, no tabla de párrafos: 3 cifras grandes con una línea cada una, o 4 tarjetas con título, una línea y una cifra.
- Cierre: porqués 4 a 5 de máx. 90 caracteres; hipótesis A, O y G de máx. 100; cómo 3 a 4 pasos de máx. 100; impacto máx. 120.
- Siguen todas las reglas de SPEC2 (unidades, lenguaje llano, palabras prohibidas, WhatsApp por entregado, ahorro oficial 2.34 M MXN al mes).
