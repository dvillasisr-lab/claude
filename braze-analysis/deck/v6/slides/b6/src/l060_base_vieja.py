"""Lámina 60: la base que ya recibía email en enero se cansa despacio, con meses de Tasa 0 y referidos (E8 cohorte 0, muestra L).
Mismo formato que la lámina 59. Para esta cohorte los días y correos son lo mínimo: su historia empieza el 1 de enero."""
from tramos import *

TR = r'Tasa0|Referral|AnotayGana'
s, bd, res, l = grafica(0, ['Marketing', 'Product Growth', 'Others', 'Sales'], lambda c: bool(re.search(TR, c)),
                        'Bajas del email de la base que ya recibía correo en enero, por días desde enero, y campaña que llegó el día de la baja, por equipo',
                        lambda i: i >= 3, 'Personas que se dieron de baja, por días desde el 1 de enero o su primer correo del año')
s.t(0, 418, 'Cada círculo suma las campañas del equipo cuya mediana de días cae en el tramo; se nombra la de más bajas. Azul: Tasa 0 y referidos.', 10.5, SEC)
tot = res.usuarios
l['tema'] = l.clave.map(gancho_of)
te = 100 * l.groupby('tema').usuarios.sum() / tot
e8 = pd.read_csv(D / 'e8_dias_hasta_baja.csv')
m30 = e8[(e8.bloque == 'banda_emails') & (e8.cohorte_limpia == 0) & (e8.clave == '31+')].usuarios.iloc[0]
p180 = 100 * bd.loc['181+', 'usuarios'] / tot
eqp = {t: 100 * l[l.team == t].usuarios.sum() / tot for t in ['Marketing', 'Product Growth', 'Others', 'Sales']}
eqd = {t: wmed(l[l.team == t]) for t in eqp}
c = l.set_index('clave')
b211 = c.loc['Lending-KCash-B0211-CANVAS-Nuevos_RegistradosPay-Tasa0-N/A']; b326 = c.loc['Marketing-KCash-B0326-Canvas-Leads-ReferralProgram-N/A']
b209 = c.loc['Lending-KCash-B0209-CANVAS-Recurrentes_Inactivos-DescuentoDirecto-N/A']
dk = c.loc['Marketing-KCash-B0326-Canvas-Recurrentes_Dormants-ReferralProgram-N/A']; dp = c.loc['Marketing-KPay-B0326-Canvas-Recurrentes_Dormants-ReferralProgram-N/A']
rec = b209.usuarios + dk.usuarios + dp.usuarios
print(tot, res.dias_mediana, res.emails_mediana, p180, te.round(1).to_dict(), m30 / tot, eqp, eqd, rec)
write(60, dict(
    titulo='La base vieja se cansa despacio: aguanta meses de Tasa 0 y referidos hasta que se da de baja',
    que=f'Tasa 0 ({te["Tasa 0"]:.0f} % de las bajas), referidos ({te["Referidos"]:.0f} %), descuentos y cupones ({te["Descuento, cupón u oferta"]:.0f} %), lanzamientos y boletines ({te["Lanzamiento y novedades"]:.0f} %) y ofertas a registrados que nunca pidieron crédito ({te["Bienvenida y activación"]:.0f} %).',
    quien=f'Marketing, {eqp["Marketing"]:.0f} % de las bajas (a los {eqd["Marketing"]:.0f} días, mediana); Product Growth, {eqp["Product Growth"]:.0f} % (a los {eqd["Product Growth"]:.0f}); Others, {eqp["Others"]:.0f} %, y Sales, {eqp["Sales"]:.0f} %.',
    a_quien=f'{tot/1e3:.0f} mil personas que ya recibían correo en enero y se dieron de baja del email entre enero y septiembre.',
    lecturas=[
        f'La mitad aguantó {res.dias_mediana:.0f} días y {res.emails_mediana:.0f} correos antes de irse; {p180:.0f} % más de 180 días. Es lo mínimo: su historia empieza el 1 de enero.',
        f'Lo que la cansa es repetir el mismo tema: la Tasa 0 a registrados sin crédito de Product Growth (B0211) se llevó {b211.usuarios/1e3:.0f} mil personas a los {b211.dias_mediana} días y {b211.emails_prom:.0f} correos; los referidos de Marketing (B0326), {b326.usuarios/1e3:.0f} mil a los {b326.dias_mediana} días.',
        f'Recuperar ex clientes también cuesta suscripciones: {rec/1e3:.1f} mil personas se dieron de baja con el descuento a inactivos (B0209, {b209.emails_prom:.0f} correos) y los referidos a dormants de KCash y KPay (B0326).',
    ],
    causa=f'Las campañas por calendario no tienen fin: siguen escribiendo aunque la persona no abra nada en meses. {100*m30/tot:.0f} % se fue después de más de 30 correos.',
    sowhat='Límite mensual de promociones por persona y salida automática de la campaña si no abre nada en 90 días, también en las de recuperación.',
    fuente='Fuente: Braze, días y correos hasta la baja del email por persona (E8), personas que ya recibían correo en enero de 2026; días y correos cuentan desde el 1 de enero. Tema por el nombre de la campaña; una baja cuenta en dos campañas si ese día llegaron dos.',
    svg=s.svg()))
