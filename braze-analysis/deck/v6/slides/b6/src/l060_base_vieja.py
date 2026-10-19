"""Lámina 60 (ronda 2): misma gráfica que la 59 para quien ya recibía correo en enero (E8 cohorte 0). Días y correos cuentan desde el
1 de enero, así que son lo mínimo."""
from tramos import *

TR = r'Tasa0|Referral|AnotayGana'
ET = {'Lending-KCash-B0211-CANVAS-Nuevos_RegistradosPay-Tasa0-N/A': (-150, -6, 'end'),
      'Marketing-KCash-B0326-Canvas-Leads-ReferralProgram-N/A': (0, -18, 'middle'),
      'Marketing-KCash-B0171-CANVAS-Leads_BBDDRezagada-NarrativaTasa0-N/A': (-150, -10, 'end'),
      'Lending-KCash-B0209-CANVAS-Recurrentes_Inactivos-DescuentoDirecto-N/A': (-160, 30, 'end')}
s, bd, res, l = grafica(0, ['Marketing', 'Product Growth', 'Others', 'Sales', 'Collections'], lambda c: bool(re.search(TR, c)),
                        'Cada punto es una campaña que llegó el día de la baja de alguien de la base vieja, por equipo', ET,
                        'Base vieja que se dio de baja del correo: campaña del día de la baja, por equipo')
s.legend([(BLUE, 'Tasa 0 y referidos', 'dot'), (M1, 'Otras campañas', 'dot'), (INK, 'Mediana del equipo', 'rect')], 0, 24, size=11)
s.t(0, 414, 'Tamaño: personas que se dieron de baja. Días desde el 1 de enero o el primer correo del año. Escala logarítmica.', 10.5, SEC)
tot = res.usuarios
l['tema'] = l.clave.map(gancho_of)
te = 100 * l.groupby('tema').usuarios.sum() / tot
p180 = 100 * bd.loc['181+', 'usuarios'] / tot
c = l.set_index('clave')
rec = sum(c.loc[k, 'usuarios'] for k in ['Lending-KCash-B0209-CANVAS-Recurrentes_Inactivos-DescuentoDirecto-N/A',
                                          'Marketing-KCash-B0326-Canvas-Recurrentes_Dormants-ReferralProgram-N/A',
                                          'Marketing-KPay-B0326-Canvas-Recurrentes_Dormants-ReferralProgram-N/A'])
write(60, dict(
    titulo='La base vieja se cansa despacio: aguanta meses de Tasa 0 y referidos hasta que se da de baja',
    que='Tasa 0, referidos, descuentos, lanzamientos y ofertas a quien nunca pidió crédito.',
    quien='Marketing y Product Growth; Others (BillPay, recomendaciones) y Sales.',
    a_quien=f'{tot/1e3:.0f} mil personas que ya recibían correo en enero y se dieron de baja.',
    lecturas=[
        f'La mitad aguantó {res.dias_mediana:.0f} días y {res.emails_mediana:.0f} correos; {p180:.0f} % más de 180 días.',
        f'Tasa 0 explica {te["Tasa 0"]:.0f} % de las bajas y los referidos {te["Referidos"]:.0f} %.',
        f'Recuperar ex clientes también cuesta: {rec/1e3:.0f} mil bajas con descuento a inactivos y referidos a dormants.',
    ],
    causa='Las campañas por calendario no tienen fin: siguen escribiendo aunque la persona no abra nada en meses.',
    sowhat='Límite mensual de promociones por persona y salida de la campaña si no abre en 90 días.',
    fuente='Fuente: Braze, días y correos hasta la baja del email por persona (E8), quienes ya recibían correo en enero de 2026. Tema por el nombre.',
    svg=s.svg()))
