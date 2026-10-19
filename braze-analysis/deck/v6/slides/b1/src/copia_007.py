"""Lámina 7: ya aprobada por el usuario. Copia muestras/s1.json con "n": 7 y "kind": "grafica" (no se rehace)."""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent
src = H.parents[2] / 'muestras' / 's1.json'
d = json.loads(src.read_text(encoding='utf-8'))
o = {'n': 7, 'kind': 'grafica', **{k: v for k, v in d.items() if k not in ('n', 'kind')}}
o.update(  # texto recortado a los límites de ESTANDAR.md; el SVG aprobado no se toca
    que='Junio: lanzamiento de BillPay y push de Mundial, Comercio del día y Anota y Gana.',
    quien='En junio contra enero, Marketing sumó 28 M mensajes y Others 25 M.',
    a_quien='Casi toda la base: el correo de BillPay llegó a 16 M personas.',
    lecturas=['Septiembre mandó 66 M mensajes, casi como enero (59 M), pero trajo 54 respuestas por cada mil contra 84.',
              'Junio fue el pico: 109 M mensajes. Después mandamos menos y la respuesta quedó en 61, 56 y 54 por mil.',
              'WhatsApp, que sí se lee, bajó de 10 % a 5 % de los mensajes; push, que casi no se abre, subió de 27 % a 37 %.'],
    causa='Escribimos a toda la base por push y correo, sin límite de mensajes por persona ni calendario entre equipos.',
    sowhat='Mandar menos no basta: hay que escribir a quien responde, por su canal y con un límite semanal.',
    fuente='Fuente: Braze, envíos por comunicación, mes y canal, enero a septiembre 2026. Respuesta = clic de correo, apertura de push, lectura de WhatsApp y clic in-app, por cada mil enviados.')
(H.parent / '007.json').write_text(json.dumps(o, ensure_ascii=False, indent=1), encoding='utf-8')
print('escrito 007.json')
