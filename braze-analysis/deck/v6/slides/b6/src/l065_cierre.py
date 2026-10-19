"""Lámina 65: cierre de la sección VII. Cifras de E7b (bajas totales), E8 (nuevos y base vieja), E1 (respuesta por tema) y E9a (campañas
que solo adelantan la compra, WhatsApp por entregado)."""
from tramos import *

j = pd.read_csv(H / 'muestra_j_patron_respuesta.csv'); bajas = j.usuarios_con_baja_email.sum()
_, r1, l1 = datos(1); _, r0, l0 = datos(0)
def share(l, tot, rx): return 100 * l[l.clave.str.contains(rx)].usuarios.sum() / tot
bp_reg = share(l1, r1.usuarios, r'BillPay|LeftFunnel|AccountCreation|NIPconCupon|FaltaVeriff|RequestInfo')
promo = 100 * l1[l1.tipo == 'promocional o lifecycle'].usuarios.sum() / r1.usuarios
promo0 = 100 * l0[l0.tipo == 'promocional o lifecycle'].usuarios.sum() / r0.usuarios
e = load_e1(); e['gg'] = e.communication_name.map(gan_g)
p = e[~e.grupo.isin(['cobranza', 'transaccional']) & (e.canal == 'email')]
rec = resp(p[p.gg == 'recordatorio'], 'email'); ofs = [resp(p[p.gg == g], 'email') for g in ('tasa0', 'descuento', 'referidos', 'lanzamiento')]
c = pd.read_csv(H / 'muestra_c_familias.csv'); tipo = c.groupby('familia').tipo.first()
m = pd.read_csv(H / 'muestra_m_ventanas.csv'); m = m[m.muestra == True].copy(); m['tipo'] = m.familia.map(tipo)
m = m[(m.tipo == 'promocional o lifecycle') & (m.lift_7 >= 1.5) & (m.lift_90 < 1.5) & (m.canal == 'whatsapp')]
wa = e[(e.canal == 'whatsapp') & e.familia.isin(set(m.familia))].whatsapp_delivery.sum() / 9
nmes = r1.usuarios / 8
print(bajas, promo, promo0, bp_reg, rec, ofs, wa, nmes, r1.familias_prom, r0.emails_mediana)

write(65, dict(
    kind='cierre',
    titulo='Por qué pasa: diseñamos los mensajes por lo que queremos vender, no por lo que la persona hizo',
    porques=[
        f'{bajas/1e3:.0f} mil personas se dieron de baja del email en nueve meses, nueve de cada diez el día de un correo promocional.',
        f'Porque la misma persona recibe las ofertas de varios equipos a la vez: el nuevo, correos de {r1.familias_prom:.1f} campañas antes de irse; la base vieja, {r0.emails_mediana:.0f} correos antes de irse, sobre todo de Tasa 0 y referidos.',
        f'Porque cada campaña nace de lo que queremos vender (Tasa 0, referidos, BillPay), aunque el recordatorio de algo empezado responde {rec:.2f} % por correo y las ofertas {min(ofs):.2f} a {max(ofs):.2f} %.',
        'Porque Braze no tiene a la mano lo que la persona hizo (registro a medias, compra en curso, días sin usar, si tiene la app) ni un límite de mensajes por persona entre equipos.',
        'Causa raíz: nadie es dueño del recorrido completo de cada persona ni mide contra un grupo sin mensajes; cada equipo cuida su campaña y nadie ve el cansancio ni cuánto suma.',
    ],
    hipotesis={
        'A': f'Si cada promoción sale por algo que hizo la persona, la respuesta del correo se acerca a la del recordatorio ({rec:.1f} %) y las bajas de nuevos bajan.',
        'O': 'Una sola secuencia de bienvenida para KCash y KPay, con un correo al día como máximo y salida a los 90 días sin abrir, reduce bajas sin perder registros terminados.',
        'G': 'Un dueño del recorrido del cliente, con calendario común y grupo sin mensajes obligatorio, evita que cada equipo sume su oferta sobre la de otro.',
    },
    como=[
        'Semanas 1 y 2. Datos y CRM cargan a diario en Braze la etapa del registro, la compra en curso, los días sin usar y si tiene la app. Métrica: % de campañas armadas por una acción.',
        'Semanas 2 a 4. Marketing y Acquisition unen sus recordatorios de registro en un solo Canvas: un correo al día, tres en la primera semana; nada de BillPay ni Tasa 0 al nuevo hasta que abra. Métrica: bajas por cada mil nuevos.',
        'Semanas 2 a 6. Cada equipo en sus Canvas: máximo dos mensajes por campaña al mes, el segundo solo a quien no abrió, y salida tras 90 días sin abrir, también en recuperación. Métrica: bajas por cada mil personas.',
        'Semanas 4 a 8. Grupo sin mensajes de 10 % en cada campaña promocional, leído a 7 y a 90 días; lo que solo adelanta la compra pasa a push o in-app. Métrica: conversión contra el grupo sin mensajes.',
    ],
    impacto=f'Hoy se dan de baja {nmes/1e3:.0f} mil nuevos al mes, {bp_reg:.0f} % con BillPay o los recordatorios de registro: es la parte que se corrige primero. Además, {wa/1e6:.1f} M MXN al mes de WhatsApp van a campañas donde la compra solo se adelanta; el grupo sin mensajes dirá cuánto de eso se puede quitar.',
    sowhat='Escribir por lo que la persona hizo, por el canal que usa y con pocos mensajes; y medir cada campaña contra un grupo que no recibe nada.',
    fuente='Fuente: Braze, E7b (patrón de respuesta), E8 (días hasta la baja), E1 (envíos por campaña, mes y canal) y E9a (quien abre contra quien no, a 7 y 90 días), enero a septiembre 2026. WhatsApp a 1.00 MXN por entregado.',
))
