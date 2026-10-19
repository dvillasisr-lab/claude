"""Lámina 27: ficha de Product Growth (Lending en Braze)."""
import re
from ficha import *
x = e1(); t = x[(x.equipo == 'Product Growth') & (x.canal != 'banner')]
T = lambda n: tema_of(n)
FILAS = [('Installments a quien lo empezó', lambda n: 'B0301' in n),
         ('Crédito a quien nunca activó', lambda n: bool(re.search('neveractive|nevercash', n.lower())) and T(n) == 'Oferta de crédito e Installments'),
         ('Otras ofertas de crédito', lambda n: T(n) == 'Oferta de crédito e Installments'),
         ('Tasa 0 a registrados', lambda n: T(n) == 'Tasa 0 y rescate de leads'),
         ('Recuperar inactivos y churn', lambda n: T(n) == 'Recuperar inactivos y churn'),
         ('Concursos y temporada', lambda n: T(n) == 'Temporada y concursos')]
MEJ = [('Recordatorio de Installments a activos', 'B0301-CANVAS-Active-Retargeting_Installments', 'push notification', None),
       ('El mismo recordatorio por correo', 'B0301-CANVAS-Active-Retargeting_Installments', 'email', mxn_conv),
       ('Anota y gana por in-app', 'KCash-B0440-CANVAS-Todos-AnotayGana', 'in-app', None)]
PEO = [('Tasa 0 a registrados sin crédito', 'B0211-CANVAS-Nuevos_RegistradosPay', 'email', mxn_conv),
       ('Installments a quien nunca activó', 'B0223-CANVAS-Nuevos_NeverActive', 'email', mxn_conv),
       ('Churn de KPay por WhatsApp', 'B0333-CANVAS-Churn', 'whatsapp', mxn_wa)]
svg, cel, tot, det, d = build('Product Growth', FILAS, MEJ, PEO, 'Product Growth: qué manda, por qué canal y cuánto le responden')
print(tot.assign(env=tot.env / 1e6, costo=tot.costo / 1e6).round(2))
print(cel.assign(env=cel.env / 1e6).round(2)[['fila', 'canal', 'env', 'r', 'pasa']].to_string())
for k, c in det.items(): print(k, round(c['env'] / 1e6, 2), round(c['resp'], 2), round(c['costo'] / 1e6, 2), round(c['costo'] / max(c['convf'], 1), 1), round(c['bajas'], 2) if c['bajas'] == c['bajas'] else '')
w = t[t.familia.str.contains('B0333') & (t.canal == 'whatsapp')]; print('B0333 entrega %.1f %%' % (100 * w.whatsapp_delivery.sum() / w.whatsapp_send.sum()))
for ch in ['email', 'push notification', 'in-app']:
    z = t[t.familia.str.contains('B0333') & (t.canal == ch)]
    b = {'email': ('email_delivery', 'email_click'), 'push notification': ('pn_send', 'pn_open'), 'in-app': ('in_app_impression', 'in_app_click')}[ch]
    print('B0333', ch, round(100 * z[b[1]].sum() / max(z[b[0]].sum(), 1), 2), 'usuarios/mes %.0f' % (z.groupby('mes').usuarios_aprox.sum().mean()))
f = fam(); g = f[f.equipo == 'Product Growth']
print('sin acción %.1f %%, pasa sin %.1f %%, pasa con %.1f %%' % (100 * g[~g.con].env.sum() / g.env.sum(), 100 * g[~g.con & g.pasa].env.sum() / g[~g.con].env.sum(), 100 * g[g.con & g.pasa].env.sum() / g[g.con].env.sum()))
print('conv %.0f, MXN/conv %.1f, bajas/mil %.2f' % (t.conversiones_fraccional.sum(), t.costo.sum() / t.conversiones_fraccional.sum(), 1000 * t.email_unsubscribe.sum() / t.email_delivery.sum()))
save(27, dict(kind='grafica',
  titulo='Product Growth acierta al recordar Installments a quien ya lo empezó y no le responden cuando ofrece Tasa 0 y crédito a quien no lo pidió',
  que='Casi todo ofertas: crédito e Installments (36 % de sus mensajes), Tasa 0 a registrados (25 %), recuperar ex clientes inactivos y churn (23 %) y concursos como Anota y gana y Cuesta de enero (16 %).',
  quien='Product Growth (Lending en Braze): 186 campañas con todas sus versiones, 56 activas en septiembre. 177 M mensajes y 17.3 M MXN en nueve meses.',
  a_quien='Registrados que nunca pidieron crédito 38 %, clientes activos y recurrentes 29 %, ex clientes inactivos y dormidos 16 %, envíos a toda la base 12 % y churn de KPay (12 meses sin uso) 5 %.',
  lecturas=[
   'Acierta con quien ya empezó algo: el recordatorio de Installments a clientes activos abre 11 % en push y tiene 2.78 % de clic en correo, a 2.7 MXN por cada préstamo o solicitud de Cash.',
   'No le responden cuando ofrece crédito a quien no lo pidió: 72 % de sus mensajes van a gente que no ha hecho nada reciente y solo 29 % de ellos responde lo mínimo. Tasa 0 a registrados: 34.9 M correos con 2.8 clics por cada mil.',
   'Ex clientes sin app: el churn de KPay lee el WhatsApp (51.5 %) pero casi no hace clic en el correo (1 por cada mil); el push e in-app solo llegan a quien conserva la app.'],
  causa='Las ofertas de crédito se arman para listas completas (todos los registrados, todos los inactivos) y salen por correo a toda la lista, en lugar de partir de algo que la persona acaba de hacer.',
  sowhat='Sacar del correo a toda la lista la Tasa 0 y el crédito a quien nunca activó, ampliar el recordatorio de Installments y buscar al churn por WhatsApp con límite de gasto y grupo sin mensajes.',
  fuente='Fuente: Braze, envíos por campaña, mes y canal, enero a septiembre 2026; campañas con 50 mil o más mensajes entregados. Gasto: correo 0.05 MXN por enviado, WhatsApp 1.00 MXN por entregado. Préstamo o solicitud de Cash en 7 días: referencia, no mide compras con KPay. Lectura de WhatsApp incluye las del mes siguiente.',
  svg=svg))
check(27)
