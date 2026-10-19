"""Lámina 31: ficha de Others (NewProducts con BillPay y recargas, avisos transaccionales de KPay y KCash, Shopping, Compliance, CX, Acquisition y QA)."""
from ficha import *
x = e1(); t = x[(x.equipo == 'Others') & (x.canal != 'banner')]
TM = fam().set_index('familia').tema.to_dict()
T = lambda n: TM.get(n)
FILAS = [('Avisos de pago y cuenta', lambda n: T(n) == 'Aviso transaccional'),
         ('BillPay y recargas', lambda n: T(n) == 'Lanzamiento BillPay y recargas'),
         ('Boletín y Shopping', lambda n: T(n) == 'Boletín y contenido'),
         ('Pruebas QA y copias', lambda n: T(n) == 'Pruebas y copias')]
def toques(c):
    z = t[(t.familia == c['familia']) & (t.canal == c['canal'])]
    g = z.groupby('mes').agg(e=('envios', 'sum'), u=('usuarios_aprox', 'sum'))
    return f"{c['costo']/1e6:.2f} M MXN · {(g.e / g.u).mean():.1f} correos por persona al mes"
l = pd.read_csv(R + 'hallazgos/muestra_l_familias_baja.csv')
bp = l[(l.bloque == 'familia_dia_baja') & l.clave.str.contains('BillPay_Intro', na=False)].usuarios.sum()
print('bajas el día de BillPay Intro', bp)
MEJ = [('Aviso de rechazo de KPay', 'Transaccional-KPay-Mail-Rejections', 'email', None),
       ('Lanzamiento de BillPay por in-app', 'BillPay_Intro_Full_Rollout', 'in-app', None),
       ('Confirmación de pago de KPay', 'Transaccional-KPay-Mail-Payment-Confirmation', 'email', None)]
PEO = [('Lanzamiento de BillPay por correo', 'E-Portfolio_BillPay_Intro_Full_Rollout', 'email', lambda c: f"{c['costo']/1e6:.2f} M MXN · {bp/1e3:.0f} mil bajas el día que llegó"),
       ('Recomendaciones semanales de Shopping', 'Shopping-KPay-S0004-CAMPAIGN-WeeklyRecommendations', 'email', toques),
       ('Prueba QA de registro telefónico', 'QA-KPay-B001-CANVAS-Todos-ReminderRegistroTelefono', 'push notification', lambda c: 'una prueba que llegó a clientes reales')]
svg, cel, tot, det, d = build('Others', FILAS, MEJ, PEO, 'Others: qué manda, por qué canal y cuánto le responden', 'Otros')
print(tot.assign(env=tot.env / 1e6, costo=tot.costo / 1e6).round(2))
print(cel.assign(env=cel.env / 1e6).round(2)[['fila', 'canal', 'env', 'r']].to_string())
for k, c in det.items(): print(k, round(c['env'] / 1e6, 2), round(c['resp'], 2), round(c['costo'] / 1e6, 2))
f = fam(); g = f[f.equipo == 'Others']
for s_ in ['Evento (transaccional)', 'Todos (masivo)']:
    z = g[g.seg == s_]; print(s_, round(z.env.sum() / 1e6, 1), 'pasa %.0f %%' % (100 * z[z.pasa].env.sum() / z.env.sum()))
print('bajas/mil %.2f; sin ticket %.0f %%' % (1000 * t.email_unsubscribe.sum() / t.email_delivery.sum(), 100 * t[t.ticket_number.isna() | (t.ticket_number.astype(str).str.strip().isin(['', 'nan', 'N/A']))].envios.sum() / t.envios.sum()))
save(31, dict(kind='grafica',
  titulo='En Others, el mismo lanzamiento de BillPay tuvo 85 % de clic por in-app y casi ningún clic por correo a toda la base',
  que='Avisos de algo que la persona hizo (51 %: pagos, rechazos, contratos, desembolsos) y promoción: lanzamiento de BillPay y recargas (29 %), boletín y Shopping (10 %) y pruebas QA o copias (4 %).',
  quien='BillPay (NewProducts), avisos de KPay y KCash, Shopping, Compliance, CX, Acquisition y QA: 283 campañas, 92 activas en septiembre; 98 M mensajes (15 %) y 4.4 M MXN (8 %).',
  a_quien='Un evento de la persona (avisos) 52 %, envíos a toda la base 35 % y campañas sin segmento en el nombre 8 %.',
  lecturas=[
   'Lo bueno: los avisos responden lo mínimo aceptable en 92 % de sus mensajes; el aviso de rechazo de KPay tiene 18.6 % de clic y la confirmación de pago 3.8 % en 9.3 M correos.',
   f'El mismo lanzamiento de BillPay tuvo 85 % de clic en in-app y 0.11 % por correo a 16.1 M personas: 0.81 M MXN y {bp/1e3:.0f} mil bajas el día que llegó.',
   'Lo malo: envíos a toda la base sin filtro (27 % responde lo mínimo), recomendaciones semanales de Shopping que casi nadie abre (0.12 %) y pruebas QA que llegan a clientes reales.'],
  causa='Los lanzamientos y recomendaciones salen a toda la base por correo, sin probar primero con un grupo chico ni filtrar a quien abrió algo, y las pruebas no usan una audiencia de prueba.',
  sowhat='Avisos sin cambios; lanzamientos primero por in-app y por correo solo a quien abrió algo en 90 días, probando con 5 % antes de escalar; pruebas QA con audiencia de prueba.',
  fuente='Fuente: Braze, envíos por campaña, mes y canal, enero a septiembre 2026; campañas con 50 mil o más mensajes entregados. Bajas del lanzamiento de BillPay por día de la baja (E8): 58 mil, contra 37 mil atribuidas en E1. No medimos pagos de servicios con BillPay.',
  svg=svg))
check(31)
