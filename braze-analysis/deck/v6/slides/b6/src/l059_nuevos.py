"""Lámina 59 (ronda 2): nuevos (primer correo de febrero en adelante) que se dieron de baja del email (E8, muestra L). Franja por equipo:
cada punto es una campaña que llegó el día de la baja, en la mediana de días desde el primer correo; tamaño = personas."""
from tramos import *

REG = r'BillPay|LeftFunnel|AccountCreation|NIPconCupon'
ET = {'NewProducts-Kueski-T0000-E-Portfolio_BillPay_Intro_Full_Rollout': (0, -20, 'middle'),
      'Marketing-KCash-B0000-CANVAS-Leads_LeftFunnel-Retargeting_Veriff': (14, -16, 'start'),
      'Marketing-KCash-B0000-CANVAS-Leads_LeftFunnel-Retargeting_PersonalInfo': (-12, -16, 'end'),
      'Lending-KCash-B0211-CANVAS-Nuevos_RegistradosPay-Tasa0-N/A': (10, -16, 'start'),
      'KCash Rechazo transaccional FraudRisk': (-12, -14, 'end'),
      'Acquisition-KPay-T2728-CANVAS-Prospect_FaltaVeriff-RetargetingNIPconCupon-N/A': (12, -12, 'start')}
s, bd, res, l = grafica(1, ['Marketing', 'Others', 'Product Growth', 'Acquisition', 'Collections'], lambda c: bool(re.search(REG, c)),
                        'Cada punto es una campaña que llegó el día de la baja de un usuario nuevo, por equipo', ET,
                        'Nuevos que se dieron de baja del correo: campaña del día de la baja, por equipo')
s.legend([(BLUE, 'BillPay y recordatorios de registro', 'dot'), (M1, 'Otras campañas', 'dot'), (INK, 'Mediana del equipo', 'rect')], 0, 24, size=11)
s.t(0, 414, 'Tamaño: personas que se dieron de baja. Escala logarítmica. Una baja cuenta en dos campañas si ese día llegaron dos.', 10.5, SEC)
tot = res.usuarios
e8 = pd.read_csv(D / 'e8_dias_hasta_baja.csv')
uno = e8[(e8.bloque == 'banda_emails') & (e8.cohorte_limpia == 1) & (e8.clave == '01')].usuarios.iloc[0]
bp = l.set_index('clave').loc['NewProducts-Kueski-T0000-E-Portfolio_BillPay_Intro_Full_Rollout']
reg = l[l.clave.str.contains('LeftFunnel')]
p17 = 100 * bd.loc[['0 mismo día', '1 a 7'], 'usuarios'].sum() / tot
write(59, dict(
    titulo='El nuevo se va pronto y por dos golpes: BillPay enviado a toda la base y el recordatorio diario de registro',
    que='Lanzamiento de BillPay, recordatorios de terminar el registro, rescate con Tasa 0.',
    quien='Marketing (registro), Others (BillPay de NewProducts), Product Growth y Acquisition.',
    a_quien=f'{tot/1e3:.0f} mil personas con primer correo de febrero en adelante que se dieron de baja.',
    lecturas=[
        f'{p17:.0f} % se va en la primera semana; la mitad recibió {res.emails_mediana:.0f} correos antes de irse.',
        f'{100*uno/tot:.0f} % se fue con su primer correo, casi siempre BillPay: {bp.usuarios/1e3:.0f} mil bajas de nuevos.',
        f'Los recordatorios de registro de Marketing se llevan {reg.usuarios.sum()/1e3:.0f} mil a los {min(reg.dias_mediana)} o {max(reg.dias_mediana)} días.',
    ],
    causa=f'Cada equipo le escribe al nuevo por su lado: antes de irse ya recibió correos de {res.familias_prom:.1f} campañas.',
    sowhat='Una sola bienvenida, máximo un correo al día y tres en la primera semana.',
    fuente='Fuente: Braze, días y correos hasta la baja del email por persona (E8), primer correo de febrero a septiembre 2026. Campañas con 500 bajas o más.',
    svg=s.svg()))
