"""Versión corta del deck v6 para Marketing: solo diagnóstico (qué pasa y por qué), sin plan. 15 minutos.
Toma láminas del deck v6 tal cual, agrega portada, resumen y cierre propios, y renumera.
Salida: deck/v6/marketing/DECK_marketing.html (y el PPTX con deck/v6/tools/html2pptx.js)."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from deck_v6_render import page
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / 'deck' / 'v6' / 'marketing'))
import graficas

ROOT = pathlib.Path(__file__).resolve().parent.parent
SL = ROOT / 'deck' / 'v6' / 'slides'
OUT = ROOT / 'deck' / 'v6' / 'marketing'

# Láminas del deck v6, en el orden de la historia
ORDEN = ['007', '028', '012', '016', '035', '024', '052', '070', '081']

FUENTE = 'Fuente: Braze, envíos por comunicación, mes y canal (E1), enero a septiembre 2026. WhatsApp a 1.00 MXN por entregado, correo a 0.05 MXN.'


def card(big, txt, color='#0B1220', bg='#F4F6F9'):
    return (f'<div style="background:{bg};padding:1.6cqi 1.5cqi;display:flex;flex-direction:column;gap:.7cqi">'
            f'<div class="big" style="color:{color};font-size:4.2cqi">{big}</div>'
            f'<div style="font-size:1.25cqi;line-height:1.35;color:#0B1220">{txt}</div></div>')


def item(n, head, txt):
    return ('<div style="display:flex;gap:.9cqi;align-items:flex-start;border-top:1px solid #DDE2EA;padding-top:1.1cqi">'
            '<div style="flex:0 0 auto;width:1.9cqi;height:1.9cqi;border-radius:50%;background:#E8EEFC;color:#1F4FD8;font-weight:700;'
            f'font-size:1cqi;display:flex;align-items:center;justify-content:center">{n}</div>'
            f'<div style="font-size:1.3cqi;line-height:1.4;color:#0B1220"><b>{head}</b> {txt}</div></div>')


def cardS(big, txt, color='#0B1220', bg='#F4F6F9'):
    return (f'<div style="background:{bg};padding:1cqi 1.3cqi;display:flex;flex-direction:column;gap:.35cqi">'
            f'<div class="big" style="color:{color};font-size:3.4cqi">{big}</div>'
            f'<div style="font-size:1.08cqi;line-height:1.3;color:#0B1220">{txt}</div></div>')


def itemS(n, head, txt):
    return ('<div style="display:flex;gap:.8cqi;align-items:flex-start;border-top:1px solid #DDE2EA;padding-top:.7cqi">'
            '<div style="flex:0 0 auto;width:1.7cqi;height:1.7cqi;border-radius:50%;background:#E8EEFC;color:#1F4FD8;font-weight:700;'
            f'font-size:.95cqi;display:flex;align-items:center;justify-content:center">{n}</div>'
            f'<div style="font-size:1.1cqi;line-height:1.35;color:#0B1220"><b>{head}</b> {txt}</div></div>')


def dos(izq, der, cols='55fr 45fr', top='1.4cqi'):
    return (f'<div style="display:grid;grid-template-columns:{cols};gap:2.4cqi;margin-top:{top};align-items:start">'
            f'<div>{izq}</div><div style="display:flex;flex-direction:column;gap:.6cqi">{der}</div></div>')


def gtitle(s):
    return f'<div style="font-size:1cqi;font-weight:600;color:#0B1220;margin-bottom:.5cqi">{s}</div>'


def grid(cols, inner, top='0'):
    return f'<div style="display:grid;grid-template-columns:repeat({cols},minmax(0,1fr));gap:1.3cqi 2.4cqi;margin-top:{top}">{inner}</div>'


portada = dict(kind='portada', titulo='Braze en Marketing: qué está pasando y por qué',
               subtitulo='Diagnóstico de enero a septiembre 2026 de los mensajes que manda Marketing, comparado con los demás equipos.',
               meta='262 M mensajes de Marketing, 27.2 M MXN en nueve meses · Octubre 2026')

SVG_EQ, EQ = graficas.costo_dispersion()
resumen = dict(kind='html', ancho_completo=True,
    titulo='Marketing pone 39 % de los mensajes y 47 % del gasto de Braze, y trae 25 % de las conversiones',
    que='Tasa 0, referidos, rescates a leads y recordatorios de registro.',
    quien='Marketing; se compara con Product Growth, Sales, Collections y Others.',
    a_quien='Leads, registrados sin crédito, ex clientes y clientes activos.',
    html=grid(3, cardS('3.0 M MXN', 'al mes en mensajes; 84 % se va en WhatsApp')
              + cardS('32 MXN', 'por conversión; Product Growth 21 y el resto de 4 a 17')
              + cardS('5.9', 'bajas por cada mil correos; el resto de los equipos, 2.6', '#1F4FD8', '#E8EEFC'), '0')
         + dos(gtitle('Cada punto es una campaña con 20 mil MXN o más: gasto contra MXN por conversión') + SVG_EQ,
               itemS(1, 'A quién.', 'La campaña típica de Marketing paga 128 MXN por conversión; la del resto, 34. Gastar más no la abarata (R² 0.03).')
               + itemS(2, 'Por qué canal.', 'Dos terceras partes del push que abre menos de 1 de cada 100 personas son de Marketing.')
               + itemS(3, 'Cuántas veces.', 'Hasta 2.3 M personas al mes reciben tres o más campañas el mismo día, casi siempre con Marketing.')
               + itemS(4, 'Qué sí funciona.', 'El recordatorio de registro: 21 MXN por préstamo; lo que nace de algo que hizo la persona responde siete veces más.')),
    sowhat='El dinero de Marketing se va en WhatsApp a quien no responde; funciona lo que nace de lo que hizo la persona.',
    fuente=FUENTE + ' Conversión: crédito otorgado en 7 días, repartido. Bajas sobre correos entregados.')

causas = dict(kind='html', ancho_completo=True,
    titulo='Qué lo explica: escribimos por lo que queremos vender, cada equipo por su cuenta y sin medir',
    html=grid(3, card('73 %', 'de las personas no respondió a nada en nueve meses')
              + card('2.3 M', 'personas al mes con tres o más campañas el mismo día')
              + card('1 de 3,228', 'Canvas tiene un grupo de control real', '#1F4FD8', '#E8EEFC'), '0')
         + grid(3,
        item(1, 'Escribimos por lo que queremos vender.', 'Las promociones salen a listas por etapa, no por lo que la persona hizo, '
             'y le seguimos escribiendo a quien no responde.')
        + item(2, 'Cada equipo decide solo.', 'No hay límite de mensajes por persona ni calendario común: Marketing, Product Growth y Sales '
               'le escriben a la misma gente el mismo día.')
        + item(3, 'Nadie compara volumen contra respuesta.', 'Copiar una campaña cada mes es más fácil que medirla: 4 de cada 10 mensajes '
               'salen de campañas debajo del mínimo.'), '1.8cqi'),
    sowhat='Es la forma de operar, no una campaña: por eso se corrige con reglas comunes, no apagando todo.',
    fuente='Fuente: láminas de diagnóstico del deck v6 (Braze E1, E7b, E13, enero a septiembre 2026).')


def tile(tema, big, txt, alert=False):
    c = '#1F4FD8' if alert else '#0B1220'
    return ('<div style="border-top:2px solid #0B1220;padding-top:.9cqi;display:flex;flex-direction:column;gap:.45cqi">'
            f'<div style="font-size:.82cqi;letter-spacing:.1em;text-transform:uppercase;color:#6B7484;font-weight:600">{tema}</div>'
            f'<div class="big" style="color:{c};font-size:3.2cqi">{big}</div>'
            f'<div style="font-size:1.15cqi;line-height:1.35;color:#3B4556">{txt}</div></div>')


TD = 'style="padding:.45cqi .9cqi .45cqi 0;vertical-align:top"'
TDB = 'style="padding:.45cqi .9cqi .45cqi 0;vertical-align:top;white-space:nowrap"'
TDE = 'style="padding:.45cqi 0 .45cqi 0;vertical-align:top;color:#6B7484"'


def fila(tema, dato):
    return f'<tr><td {TDB}><b>{tema}</b></td><td {TD}>{dato}</td></tr>'


SVG_HIG, HIG = graficas.higiene()
gobierno = dict(kind='html', ancho_completo=True,
    titulo='Tres de cada diez comunicaciones que mandan no tienen equipo, ticket o nombre en regla: 36 % de los mensajes',
    html=grid(4, cardS('6,144', 'comunicaciones guardadas; en septiembre solo 341 mandaron algo')
              + cardS('183', 'nombres distintos en el campo de equipo, para 5 equipos')
              + cardS('731', 'nombres de audiencia; 85 M mensajes con segmento "Not Tracked"')
              + cardS('1 de 3,228', 'Canvas con grupo de control real', '#1F4FD8', '#E8EEFC'), '0').replace('gap:1.3cqi 2.4cqi', 'gap:1.3cqi 1.3cqi')
         + dos(gtitle('Cada punto es una comunicación que mandó algo en 2026, por problema de orden') + SVG_HIG,
               itemS(1, 'Nombres.', '1,053 fuera de la convención: "Recurentes", "Recurrentess", "Softnactive", fecha "202600903".')
               + itemS(2, 'Equipo y ticket.', '"Copy of Copy of Copy of Copy of Marketing" es un equipo; T0000 y B0000 sirven de ticket, y B0171 cubre 362.')
               + itemS(3, 'Copias.', '63 % de lo que manda cada mes se creó ese mes: se arma una campaña nueva en vez de reusar la anterior.'),
               '64fr 36fr'),
    sowhat='Sin nombre, equipo, ticket ni audiencia confiables, nadie puede saber qué manda Braze ni de quién es.',
    fuente='Fuente: Braze, catálogo de campañas y Canvas (E2), envíos por comunicación (E1), segmentos (E11), pasos de Canvas (E15) y grupos de control (E13), enero a septiembre 2026.')

def tile(tema, big, txt):
    return ('<div style="border-top:2px solid #0B1220;padding-top:.9cqi;display:flex;flex-direction:column;gap:.45cqi">'
            f'<div style="font-size:.82cqi;letter-spacing:.1em;text-transform:uppercase;color:#6B7484;font-weight:600">{tema}</div>'
            f'<div class="big" style="color:#1F4FD8;font-size:3.2cqi">{big}</div>'
            f'<div style="font-size:1.12cqi;line-height:1.35;color:#3B4556">{txt}</div></div>')


no_deberiamos = dict(kind='html', ancho_completo=True,
    titulo='Le escribimos a quien no debería recibir promociones: congelados, dados de baja y quien pidió no recibirlas',
    que='Promociones: Tasa 0, referidos, ofertas de KPay y de comercios.',
    quien='Todos los equipos; Marketing manda la mayor parte de lo que llega tras la baja.',
    a_quien='Personas con KPay congelado, dados de baja, REUS, ARCO y lista negra.',
    html=('<div style="display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:1.3cqi">'
          + cardS('43.3 M', 'promociones a quien tiene KPay congelado y no puede comprar', '#1F4FD8', '#E8EEFC')
          + cardS('9.8 M', 'WhatsApp a personas marcadas como baja de WhatsApp', '#1F4FD8', '#E8EEFC')
          + cardS('249 mil', 'promociones a quien pidió no recibir publicidad (REUS o ARCO)', '#1F4FD8', '#E8EEFC')
          + cardS('146 mil', 'promociones a personas en lista negra', '#1F4FD8', '#E8EEFC')
          + cardS('79 mil', 'promociones a quien ya se dio de baja del correo', '#1F4FD8', '#E8EEFC')
          + '</div>'
          + dos(gtitle('502 campañas mandaron promociones a quien no debía recibirlas; las 10 primeras suman solo 24 %') + graficas.pareto_no_deberiamos()[0],
                itemS(1, 'KPay congelado.', 'Su línea de KPay está bloqueada y no puede comprar; 30.1 M de esas promociones ofrecían justo KPay.')
                + itemS(2, 'REUS o ARCO.', 'REUS: registro de CONDUSEF para no recibir publicidad. ARCO: pidió cancelar u oponerse al uso de sus datos.')
                + itemS(3, 'Baja de correo.', 'De 79 mil promociones a quien ya se dio de baja, 58 mil son de Marketing; la mayor, rescate de Tasa 0.'),
                '62fr 38fr')),
    sowhat='Es riesgo legal y de marca, no de una campaña: ninguna exclusión es común a toda la cuenta.',
    fuente='Fuente: Braze, envíos por comunicación (E1), banderas de contacto (E7a, E17) y envíos tras la baja (E5b), enero a septiembre 2026.')

def main():
    ds = [portada, resumen]
    for n in ORDEN:
        p = next(SL.glob(f'*/{n}.json'))
        ds.append(json.loads(p.read_text(encoding='utf-8')))
    ds.append(gobierno)
    ds.append(no_deberiamos)
    ds.append(causas)
    for i, d in enumerate(ds, 1):
        d['n'] = i
        d.pop('sub', None); d.pop('oculta', None)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'DECK_marketing.html').write_text(page(ds, 'Braze en Marketing · Diagnóstico'), encoding='utf-8')
    for i, d in enumerate(ds, 1):
        (OUT / f'{i:02d}.json').write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')
    print(OUT / 'DECK_marketing.html', len(ds))


if __name__ == '__main__':
    main()
