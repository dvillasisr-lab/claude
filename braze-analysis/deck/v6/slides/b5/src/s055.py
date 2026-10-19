"""Lámina 55: cierre de la sección VI (a quién le escribimos). Cifras de b5_datos.json; el ahorro mensual es el oficial del caso de negocio."""
from b5_svg import *

G = D['grupos']; GC = D['gc']; C = D['control']; P = D['prog']; T = D['tot']; E7 = D['e7b']
fr_costo = G['ex']['costo'] + G['nunca']['costo']
wa_fr = GC['ex|whatsapp']['costo'] + GC['nunca|whatsapp']['costo']
B = D['bloq']; ex_all = B['freeze']['promo'] + B['reus']['promo'] + B['negra']['promo']
guarda(55, dict(
    kind='cierre',
    titulo='Por qué pasa: Braze no sabe quién es cada persona ni qué hizo hace poco, y nadie mide si recuperar recupera',
    porques=[
        f'Tres de cada cuatro personas no respondieron en nueve meses, y {100*fr_costo/T["costo"]:.0f} % del gasto ({M(fr_costo)} M MXN) va a ex clientes y a leads que nunca activaron.',
        f'Les escribimos igual a todos: las mismas promociones y el canal más caro, WhatsApp ({M(wa_fr)} M MXN), aunque lleven un año sin usar el producto o ya no les llegue.',
        'Cada equipo arma su lista por el nombre de la campaña y usa su canal de costumbre; nadie quita a quien no puede comprar con KPay, pidió no recibir publicidad o se dio de baja.',
        f'Nadie mide si recuperar recupera: de {C["canvas"]} Canvas de recuperación, {C["con_control"]} dejan a un grupo sin mensajes y ninguno de ex clientes.',
        'Causa raíz: Braze no tiene la etapa de cada persona, sus meses sin usar el producto, su última respuesta por canal ni si tiene la app, y ningún programa tiene dueño con límite de gasto y grupo sin mensajes.',
    ],
    hipotesis={
        'A': f'Con la etapa y los meses sin uso en Braze, el gasto se va a quien se fue hace poco ({P["30a90"]["mxn_conv"]:.0f} MXN por conversión a los 30 a 90 días contra {P["12m"]["mxn_conv"]:.0f} a los 12 meses) y baja el costo sin perder conversiones.',
        'O': f'Si el WhatsApp de recuperación va solo a quien leyó uno en 90 días, la mayor parte de los {M(wa_fr)} M MXN a bases frías se quita y las conversiones se mantienen por correo, push e in-app.',
        'G': 'Si cada programa tiene dueño, límite mensual de gasto y 10 % sin mensajes, en dos meses sabremos cuánto recupera cada uno y cuál se quita.',
    },
    como=[
        f'Semana 1, MarTech con Legal y Riesgo: exclusiones de cuenta en Braze (KPay congelado en promociones de KPay, REUS, ARCO y lista negra) y filtro de suscripción en cada paso de correo. Quita {M(D["excl_min"])} M promociones; métrica: cero promociones a bloqueados.',
        'Semanas 2 a 4, Datos: tres atributos diarios en Braze: etapa (lead, nuevo, activo, inactivo con meses sin uso, churn), última respuesta por canal en 90 días y tiene app con entrada en el mes.',
        'Semana 4, Product Growth y Marketing: ex clientes de hasta 6 meses por correo, push e in-app; churn de 12 meses y leads que nunca activaron, tres mensajes en 30 días por el canal más barato que usen; WhatsApp solo a quien leyó uno en 90 días.',
        'Desde la semana 4, cada programa con límite mensual de gasto y 10 % sin mensajes en su Canvas. Métrica: costo por conversión recuperada contra ese grupo; a los dos meses se decide qué se quita.',
    ],
    impacto=f'Hasta 0.85 M MXN al mes en mensajes a ex clientes y a quien no responde en 90 días, que se quitan solo si el grupo sin mensajes muestra que no recuperan clientes; y {M(D["excl_min"])} M promociones menos a quien no debe recibirlas, sin tocar ninguna campaña.',
    sowhat='Recuperar sí, pero sabiendo quién es la persona, por el canal que usa, con límite de gasto y con un grupo sin mensajes que diga cuánto recupera.',
    fuente=f'Fuente: láminas 48 a 54 (Braze E1, E7a, E7b, E9a, E9b, E4a, E5b, E13, E17, enero a septiembre 2026). 0.85 M MXN al mes: caso de negocio oficial (se quita solo si no recupera clientes). Con KCash y el resto de las promociones a congelados, las exclusiones llegan a {M(ex_all)} M.',
))
