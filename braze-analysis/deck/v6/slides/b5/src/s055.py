"""Lámina 55 (ronda 2): cierre de la sección VI con textos cortos. Cifras de b5_datos.json; el 0.85 M MXN al mes es el oficial del caso de negocio."""
import pandas as pd
from b5_svg import *
t = pd.read_csv(H / 'b5_camp.csv')
c8 = t[t.familia.str.contains('B0208-CANVAS-Recurrentes_Inactivos30a90dias') & (t.canal == 'email')].sort_values('env').iloc[-1].mxn_conv
c33 = t[t.familia.str.contains('B0333-CANVAS-Churn') & (t.canal == 'whatsapp')].sort_values('env').iloc[-1].mxn_conv

G = D['grupos']; GC = D['gc']; C = D['control']; P = D['prog']; T = D['tot']
fr_costo = G['ex']['costo'] + G['nunca']['costo']
wa_fr = GC['ex|whatsapp']['costo'] + GC['nunca|whatsapp']['costo']
guarda(55, dict(
    kind='cierre',
    titulo='Por qué pasa: Braze no sabe quién es cada persona ni qué hizo, y nadie mide si recuperar recupera',
    porques=[
        f'73 % no respondió en nueve meses; {100*wa_fr/T["wa"]:.0f} % del WhatsApp va a ex clientes y leads fríos.',
        f'A todos les llegan las mismas promociones, y {M(wa_fr)} M MXN de WhatsApp a quien ya no compra.',
        'Cada equipo arma su lista por nombre de campaña y nadie quita a los bloqueados.',
        f'De {C["canvas"]} Canvas de recuperación, ninguno deja un grupo sin mensajes de verdad.',
        'Causa raíz: Braze no tiene etapa, meses sin uso, última respuesta ni app de cada persona.',
    ],
    hipotesis={
        'A': f'Con meses sin uso en Braze: {c8:.0f} MXN por conversión a 30 a 90 días contra {fmt(c33)} a 12 meses.',
        'O': 'WhatsApp solo a quien leyó uno en 90 días: baja el gasto y la conversión sigue por correo e in-app.',
        'G': 'Con dueño, límite de gasto y 10 % sin mensajes, en dos meses sabemos qué programa recupera.',
    },
    como=[
        f'Semana 1, MarTech con Legal y Riesgo: exclusiones de cuenta en Braze ({M(D["excl_min"])} M promociones menos).',
        'Semanas 2 a 4, Datos: etapa, meses sin uso, última respuesta y si tiene app, diario en Braze.',
        'Semana 4, Product Growth y Marketing: recuperar por meses sin uso, máximo tres mensajes en 30 días.',
        'Desde la semana 3, por 8 semanas: 10 % sin mensajes en cada programa; mes 3: decidir qué se quita.',
    ],
    impacto=f'Hasta 0.85 M MXN al mes, solo si el grupo sin mensajes muestra que no recupera, y {M(D["excl_min"])} M promociones menos.',
    sowhat='Recuperar sí, sabiendo quién es la persona, por el canal que usa y con un grupo sin mensajes.',
    fuente='Fuente: láminas 48 a 54 (Braze E1, E3, E5b, E7a, E7b, E9a, E13 y E17, enero a septiembre 2026). 0.85 M MXN al mes: caso de negocio oficial.',
))
