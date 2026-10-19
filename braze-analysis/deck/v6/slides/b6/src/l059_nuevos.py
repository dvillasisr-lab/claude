"""Lámina 59: el usuario nuevo (primer correo de febrero en adelante) se da de baja pronto, con el lanzamiento de BillPay y los
recordatorios de terminar el registro (E8 cohorte limpia, muestra L)."""
from tramos import *

REG = r'BillPay|LeftFunnel|AccountCreation|NIPconCupon'
s, bd, res, l = grafica(1, ['Marketing', 'Others', 'Product Growth', 'Acquisition'], lambda c: bool(re.search(REG, c)),
                        'Bajas del email de usuarios nuevos por días desde su primer correo y campaña que llegó el día de la baja, por equipo',
                        lambda i: i <= 2)
s.t(0, 418, 'Cada círculo suma las campañas del equipo cuya mediana de días cae en el tramo; se nombra la de más bajas. Azul: BillPay y registro.', 10.5, SEC)
tot = res.usuarios
mes1 = bd.loc[['0 mismo día', '1 a 7', '08 a 30'], 'usuarios'].sum()
e8 = pd.read_csv(D / 'e8_dias_hasta_baja.csv')
uno = e8[(e8.bloque == 'banda_emails') & (e8.cohorte_limpia == 1) & (e8.clave == '01')].usuarios.iloc[0]
c = l.set_index('clave')
bp = c.loc['NewProducts-Kueski-T0000-E-Portfolio_BillPay_Intro_Full_Rollout']
reg = l[l.clave.str.contains('LeftFunnel')]
kp = l[l.clave.str.contains('AccountCreation|NIPconCupon')]
l0 = pd.read_csv(H / 'muestra_l_familias_baja.csv')
bp0 = l0[(l0.cohorte_limpia == 0) & (l0.clave == bp.name)].usuarios.sum()
e1 = pd.read_csv(D / 'e1_comunicacion_mes_canal.csv')
bpe1 = e1[e1.communication_name.fillna('').str.contains('BillPay_Intro_Full_Rollout') & (e1.canal == 'email')]
bpe1j = e1.loc[e1.communication_name.fillna('').str.contains('BillPay_Intro_Full_Rollout') & (e1.canal == 'email') & e1.mes.str.startswith('2026-06')].email_unsubscribe.sum()
bpe1 = bpe1.email_unsubscribe.sum()
eqp = {t: 100 * l[l.team == t].usuarios.sum() / tot for t in ['Marketing', 'Others', 'Product Growth', 'Acquisition']}
eqd = {t: wmed(l[l.team == t]) for t in eqp}
p0, p17, p830 = (100 * bd.loc[k, 'usuarios'] / tot for k in ('0 mismo día', '1 a 7', '08 a 30'))
print(tot, mes1 / tot, uno / tot, bp.usuarios, reg.usuarios.sum(), reg.dias_mediana.tolist(), kp.usuarios.sum(), eqp, eqd, res.emails_mediana, res.familias_prom)
write(59, dict(
    titulo='El usuario nuevo se da de baja pronto y por dos golpes: el envío de BillPay a toda la base y los recordatorios diarios de registro',
    que='Lanzamiento de BillPay (pago de servicios), recordatorios para terminar el registro (verificar identidad, completar datos, poner NIP), rescate con Tasa 0 y Tasa 0 a registrados.',
    quien=f'Marketing, {eqp["Marketing"]:.0f} % de las bajas de nuevos (a los {eqd["Marketing"]:.0f} días, mediana); Others, {eqp["Others"]:.0f} % (BillPay de NewProducts, a los {eqd["Others"]:.0f}); Product Growth, {eqp["Product Growth"]:.0f} % (a los {eqd["Product Growth"]:.0f}); Acquisition, {eqp["Acquisition"]:.0f} % (a los {eqd["Acquisition"]:.0f}).',
    a_quien=f'{tot/1e3:.1f} mil personas cuyo primer correo llegó de febrero en adelante y que se dieron de baja del email.',
    lecturas=[
        f'{100*mes1/tot:.0f} % se va en el primer mes: {p0:.0f} % el mismo día del primer correo, {p17:.0f} % en la primera semana y {p830:.0f} % entre el día 8 y el 30. La mitad había recibido {res.emails_mediana:.0f} correos.',
        f'Uno de cada tres ({100*uno/tot:.0f} %) se fue con el primer correo que recibió, casi siempre el lanzamiento de BillPay de junio: {bp.usuarios/1e3:.0f} mil bajas de nuevos, que habían recibido {bp.emails_prom:.1f} correos.',
        f'Los recordatorios de registro de Marketing llegan uno o dos al día: {reg.usuarios.sum()/1e3:.0f} mil bajas a los {min(reg.dias_mediana)} o {max(reg.dias_mediana)} días. Los de KPay (Acquisition), {kp.usuarios.sum()/1e3:.1f} mil bajas a los 1 o 2 días.',
    ],
    causa=f'Cada equipo le escribe al nuevo por su lado: antes de irse ya había recibido correos de {res.familias_prom:.1f} campañas distintas, y nadie cuida cuántos correos le llegan en su primera semana.',
    sowhat='Una sola secuencia de bienvenida, máximo un correo al día y tres en la primera semana; nada de envíos a toda la base a quien no ha abierto ningún correo.',
    fuente=f'Fuente: Braze, días y correos hasta la baja del email por persona (E8), primer correo de febrero a septiembre 2026. La campaña del día de la baja cuenta dos veces si ese día llegaron dos. BillPay: {bp.usuarios/1e3:.0f} mil bajas de nuevos más {bp0/1e3:.0f} mil de la base anterior; el conteo por campaña (E1) le atribuye {bpe1j/1e3:.0f} mil bajas en junio y {bpe1/1e3:.0f} mil con las bajas registradas de julio a septiembre.',
    svg=s.svg()))
