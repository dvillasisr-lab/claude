"""Lámina 55 (ronda 2): cierre de la sección VI con textos cortos. Cifras de b5_datos.json; el 0.85 M MXN al mes es el oficial del caso de negocio."""
from b5_svg import *

G = D['grupos']; GC = D['gc']; C = D['control']; P = D['prog']; T = D['tot']
fr_costo = G['ex']['costo'] + G['nunca']['costo']
wa_fr = GC['ex|whatsapp']['costo'] + GC['nunca|whatsapp']['costo']
guarda(55, dict(
    kind='cierre',
    titulo='Por qué pasa: Braze no sabe quién es cada persona ni qué hizo, y nadie mide si recuperar recupera',
    porques=[
        f'73 % no respondió en nueve meses; {100*fr_costo/T["costo"]:.0f} % del gasto va a ex clientes y leads fríos.',
        f'A todos les llegan las mismas promociones, y {M(wa_fr)} M MXN de WhatsApp a quien ya no compra.',
        'Cada equipo arma su lista por nombre de campaña y nadie quita a los bloqueados.',
        f'De {C["canvas"]} Canvas de recuperación, {C["con_control"]} dejan un grupo sin mensajes; ninguno de ex clientes.',
        'Causa raíz: Braze no tiene etapa, meses sin uso, última respuesta ni app de cada persona.',
    ],
    hipotesis={
        'A': f'Con meses sin uso en Braze, el gasto va a quien se fue hace poco: {P["30a90"]["mxn_conv"]:.0f} MXN por conversión contra {P["12m"]["mxn_conv"]:.0f}.',
        'O': 'WhatsApp solo a quien leyó uno en 90 días: baja el gasto y la conversión sigue por correo e in-app.',
        'G': 'Con dueño, límite de gasto y 10 % sin mensajes, en dos meses sabemos qué programa recupera.',
    },
    como=[
        f'Semana 1, MarTech con Legal y Riesgo: exclusiones de cuenta en Braze ({M(D["excl_min"])} M promociones menos).',
        'Semanas 2 a 4, Datos: etapa, meses sin uso, última respuesta y si tiene app, diario en Braze.',
        'Semana 4, Product Growth y Marketing: recuperar por meses sin uso, máximo tres mensajes en 30 días.',
        'Desde semana 4: límite de gasto y 10 % sin mensajes por programa; métrica: costo por recuperado.',
    ],
    impacto=f'Hasta 0.85 M MXN al mes, solo si el grupo sin mensajes muestra que no recupera, y {M(D["excl_min"])} M promociones menos.',
    sowhat='Recuperar sí, sabiendo quién es la persona, por el canal que usa y con un grupo sin mensajes.',
    fuente='Fuente: láminas 48 a 54 (Braze E1, E3, E5b, E7a, E7b, E9a, E13 y E17, enero a septiembre 2026). 0.85 M MXN al mes: caso de negocio oficial.',
))
