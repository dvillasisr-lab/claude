"""Lámina 29 (ronda 2): ficha de Sales (incluye B2B). Gráfica común en ficha2.py."""
from ficha2 import *
def entrega(z): return f"llega {100*z.wdel/z.wsend:.0f} %"
CASOS = [('Amazon a clientes recurrentes', 'B0415-CANVAS-Recurrentes-Amazon', 'push notification', 'b', -12, -30),
         ('Quincenas sin intereses', 'B0345-CANVAS-Recurrentes-Quincenas', 'push notification', 'b', 12, -24),
         ('Flash Sale de Amazon por WhatsApp', 'B0416-CANVAS-Recurrentes-FlashSaleAmazon', 'whatsapp', 'b', 12, -14, entrega),
         ('Promociones a todo el portafolio', 'B0335-CANVAS-Recurrentes_PortafolioActivo', 'email', 'w', -12, 92, costo),
         ('Temu de febrero a recurrentes', 'B0368-CANVAS-Recurrentes-TemuFebrero', 'email', 'w', -12, 26),
         ('Comercio del día de septiembre', 'ComerciodeldiaSeptiembre', 'push notification', 'w', 12, 40)]
svg, d, det = build('Sales', CASOS)
for k, z in det.items(): print(k, z.canal, round(z.env / 1e6, 2), round(z.resp_pct, 2), round(z.vs_min, 2))
save(29, dict(kind='grafica',
  titulo='Sales manda promociones de comercios de KPay a sus clientes: funcionan por push y WhatsApp y no por correo',
  que='Comercio del día, Hot Sale y códigos KUESKI, Amazon, Temu, lanzamientos de tiendas.',
  quien='Sales (incluye B2B): 211 campañas por canal, 83 M mensajes (13 %), 7.1 M MXN (12 %).',
  a_quien='Clientes recurrentes de KPay 74 %, leads 15 %, ex clientes inactivos 8 %.',
  lecturas=[
   'Amazon a recurrentes abre 5.5 % en push; su WhatsApp es el que más se lee (78 %) y entrega (80 %) de los cinco equipos.',
   'Su correo tiene 0.21 % de clic en 23.8 M correos, el más bajo de los cinco; Temu, 0.09 %.',
   'Comercio del día llega 7 a 9 veces por persona al mes por push, y Marketing manda el mismo.'],
  causa='El correo sigue como canal por defecto y Comercio del día sale casi a diario sin límite por persona.',
  sowhat='Sales ya sabe a quién escribir: le sobra el correo y le falta un límite al push diario.',
  fuente='Fuente: Braze, envíos por campaña, mes y canal, enero a septiembre 2026; campañas con 50 mil o más entregados. No medimos compras con KPay.',
  svg=svg))
check(29)
