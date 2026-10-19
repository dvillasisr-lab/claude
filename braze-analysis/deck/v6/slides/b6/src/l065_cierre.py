"""Lámina 65: cierre de la sección VII. Cifras de E7b (bajas totales), E8 (nuevos y base vieja), E1 (respuesta por tema) y E9a (campañas
que solo adelantan la compra, WhatsApp por entregado)."""
from tramos import *

j = pd.read_csv(H / 'muestra_j_patron_respuesta.csv'); bajas = j.usuarios_con_baja_email.sum()
_, r1, l1 = datos(1); _, r0, l0 = datos(0)
def share(l, tot, rx): return 100 * l[l.clave.str.contains(rx)].usuarios.sum() / tot
bp_reg = share(l1, r1.usuarios, r'BillPay_Intro|LeftFunnel-Retargeting_(?:Veriff|PersonalInfo|NIP)$')  # BillPay (lámina 59) y registro (láminas 59, 64 y 79)
promo = 100 * l1[l1.tipo == 'promocional o lifecycle'].usuarios.sum() / r1.usuarios
promo0 = 100 * l0[l0.tipo == 'promocional o lifecycle'].usuarios.sum() / r0.usuarios
e = load_e1(); e['gg'] = e.communication_name.map(gan_g)
p = e[~e.grupo.isin(['cobranza', 'transaccional']) & (e.canal == 'email')]
rec = resp(p[p.gg == 'recordatorio'], 'email'); ofs = [resp(p[p.gg == g], 'email') for g in ('tasa0', 'descuento', 'referidos', 'lanzamiento')]
pc = por_campana(e[~e.grupo.isin(['cobranza', 'transaccional']) & (e.tipo == 'promocional o lifecycle')], ('email',))
pc = pc[(pc.b >= 1e5) & (pc.resp > 0)]; pc['rec'] = pc.familia.map(gan_g) == 'recordatorio'
mrec, mof = pc[pc.rec].resp.median(), pc[~pc.rec].resp.median()   # medianas de la lámina 62
c = pd.read_csv(H / 'muestra_c_familias.csv'); tipo = c.groupby('familia').tipo.first()
m = pd.read_csv(H / 'muestra_m_ventanas.csv'); m = m[m.muestra == True].copy(); m['tipo'] = m.familia.map(tipo)
ma = m[(m.tipo == 'promocional o lifecycle') & (m.lift_7 >= 1.5) & (m.lift_90 < 1.5)]; vad = ma.envios_usuario_dia.sum()  # lámina 57
m = m[(m.tipo == 'promocional o lifecycle') & (m.lift_7 >= 1.5) & (m.lift_90 < 1.5) & (m.canal == 'whatsapp')]
wa = e[(e.canal == 'whatsapp') & e.familia.isin(set(m.familia))].whatsapp_delivery.sum() / 9
nmes = r1.usuarios / 8
print(bajas, promo, promo0, bp_reg, rec, ofs, wa, nmes, r1.familias_prom, r0.emails_mediana)

write(65, dict(
    kind='cierre',
    titulo='Por qué pasa: diseñamos los mensajes por lo que queremos vender, no por lo que la persona hizo',
    porques=[
        f'{bajas/1e3:.0f} mil personas dejaron el correo; nueve de cada diez, con una promoción.',
        f'La persona recibe ofertas de varios equipos: el nuevo, de {r1.familias_prom:.1f} campañas.',
        f'Cada campaña nace de lo que queremos vender: recordatorio {mrec:.1f} %, oferta {mof:.1f} % de clic.',
        'Braze no sabe qué empezó la persona ni si tiene la app, y no hay límite por persona.',
        'Causa raíz: nadie es dueño del recorrido completo ni mide con un grupo sin mensajes.',
    ],
    hipotesis={
        'A': f'Si cada promoción sale por algo que hizo la persona, el clic se acerca al del recordatorio ({mrec:.1f} %).',
        'O': 'Una sola bienvenida, un correo al día y salida a los 90 días sin abrir bajan las bajas de nuevos.',
        'G': 'Un dueño del recorrido, con calendario común y grupo sin mensajes, evita apilar ofertas.',
    },
    como=[
        'Semanas 1 a 4: un solo Canvas de registro (Marketing y Acquisition), con 10 % sin mensajes.',
        'Mes 2: MarTech y Datos ponen límites de mensajes por persona, canal preferido y horas de silencio.',
        'Desde la semana 3 y por 8 semanas: medir la recuperación de ex clientes con 10 % sin mensajes.',
        'Mes 3: decidir con la conversión contra el grupo sin mensajes y las bajas de nuevos por mes.',
    ],
    impacto=f'{nmes/1e3:.0f} mil nuevos al mes se dan de baja, {bp_reg:.0f} % con BillPay o el registro; {vad/1e6:.0f} M envíos solo adelantan compras.',
    sowhat='Escribir por lo que la persona hizo, por su canal y con pocos mensajes; medir contra un grupo sin mensajes.',
    fuente='Fuente: Braze, E7b (patrón de respuesta), E8 (días hasta la baja), E1 (envíos por campaña) y E9a (quien abre contra quien no), enero a septiembre 2026.',
))
