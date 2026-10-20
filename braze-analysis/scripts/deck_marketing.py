"""Versión corta del deck v6 para Marketing: solo diagnóstico (qué pasa y por qué), sin plan. 15 minutos.
Toma láminas del deck v6 tal cual, agrega portada, resumen y cierre propios, y renumera.
Salida: deck/v6/marketing/DECK_marketing.html (y el PPTX con deck/v6/tools/html2pptx.js)."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from deck_v6_render import page

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


def grid(cols, inner, top='0'):
    return f'<div style="display:grid;grid-template-columns:repeat({cols},minmax(0,1fr));gap:1.3cqi 2.4cqi;margin-top:{top}">{inner}</div>'


portada = dict(kind='portada', titulo='Braze en Marketing: qué está pasando y por qué',
               subtitulo='Diagnóstico de enero a septiembre 2026 de los mensajes que manda Marketing, comparado con los demás equipos.',
               meta='262 M mensajes de Marketing, 27.2 M MXN en nueve meses · Octubre 2026')

resumen = dict(kind='html', ancho_completo=True,
    titulo='Marketing pone 39 % de los mensajes y 47 % del gasto de Braze, y trae 25 % de las conversiones',
    que='Tasa 0, referidos, rescates a leads y recordatorios de registro.',
    quien='Marketing; se compara con Product Growth, Sales, Collections y Others.',
    a_quien='Leads, registrados sin crédito, ex clientes y clientes activos.',
    html=grid(3, card('3.0 M MXN', 'al mes en mensajes; 84 % se va en WhatsApp')
              + card('32 MXN', 'por conversión; Product Growth 21 y el resto de 4 a 17')
              + card('5.9', 'bajas por cada mil correos; el resto de los equipos, 2.6', '#1F4FD8', '#E8EEFC'), '0')
         + grid(2, item(1, 'A quién.', 'La mitad del dinero va a Tasa 0 a leads que casi no convierte; por WhatsApp, una base fría cuesta 13 veces más por conversión.')
                + item(2, 'Por qué canal.', 'Dos terceras partes del push que abre menos de 1 de cada 100 personas son de Marketing.')
                + item(3, 'Cuántas veces.', 'Hasta 2.3 M personas al mes reciben tres o más campañas el mismo día, casi siempre con Marketing.')
                + item(4, 'Qué sí funciona.', 'El recordatorio de registro: 21 MXN por préstamo. Lo que nace de algo que hizo la persona responde siete veces más.'),
                '1.8cqi'),
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


gobierno = dict(kind='html', ancho_completo=True,
    titulo='Braze no tiene dueño ni reglas comunes, y se nota en ocho datos de la cuenta',
    que='Todo lo que vive en Braze: campañas, Canvas, listas y configuración.',
    quien='Todos los equipos; nadie es dueño de la cuenta completa.',
    a_quien='Toda la base, incluidos bloqueados y dados de baja.',
    html=('<div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:2.2cqi 2cqi">'
          + tile('Orden', '6,144', 'comunicaciones guardadas; en septiembre solo 341 mandaron algo')
          + tile('Orden', '229', 'marcadas como archivadas siguieron enviando en septiembre')
          + tile('Dueño', '748', 'comunicaciones sin equipo ni ticket; 210 de ellas mandaron 85 M mensajes en 2026')
          + tile('Dueño', '74', 'campañas se copiaron cinco o más veces en vez de medirse: 667 versiones')
          + tile('Reglas', '43 M', 'promociones a personas con KPay congelado', True)
          + tile('Reglas', '9.8 M', 'WhatsApp a personas marcadas como baja', True)
          + tile('Reglas', '9.9 M', 'veces una persona recibió la misma campaña dos veces el mismo día', True)
          + tile('Medición', '1 de 3,228', 'Canvas tiene grupo de control real; solo el correo registra bajas por campaña', True)
          + '</div>'),
    sowhat='No es una campaña mala: es una cuenta sin dueño, sin reglas comunes y sin forma de medir.',
    fuente='Fuente: Braze, catálogo de campañas y Canvas, envíos por comunicación (E1, E2), bloqueados (E7a, Sheets v4), grupos de control (E13), enero a septiembre 2026.')


def main():
    ds = [portada, resumen]
    for n in ORDEN:
        p = next(SL.glob(f'*/{n}.json'))
        ds.append(json.loads(p.read_text(encoding='utf-8')))
    ds.append(gobierno)
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
