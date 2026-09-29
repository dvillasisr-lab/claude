#!/usr/bin/env python3
"""Builds cards.html for the Heavy Metal editorial-cover business card."""
import base64, re, pathlib

HERE = pathlib.Path(__file__).parent
A = pathlib.Path('/home/user/claude/print/swarm/assets')
F = '/root/.claude/skills/synced/9983f56a-2d7a-4333-8a10-0941713cc597_0d8f03d3-28eb-42fc-935b-5b47bbd87cf0/canvas-design/canvas-fonts'

def b64(p, mime):
    return f"data:{mime};base64," + base64.b64encode((A / p).read_bytes()).decode()

def font(name, fam, weight=400):
    data = base64.b64encode(pathlib.Path(F, name).read_bytes()).decode()
    return f"@font-face{{font-family:'{fam}';src:url(data:font/ttf;base64,{data}) format('truetype');font-weight:{weight};font-style:normal}}"

def logo(fname, fill, vb, cls):
    s = (A / fname).read_text()
    s = s.replace('#F2F0E9', fill)
    s = re.sub(r'<svg[^>]*>', f'<svg class="{cls}" viewBox="{vb}" xmlns="http://www.w3.org/2000/svg" aria-label="Heavy Metal">', s, count=1)
    return s

def qr():
    s = (A / 'qr-tienda.svg').read_text()
    return s.replace('<svg ', '<svg class="qr" ', 1)

from PIL import Image
import io
_e = Image.open(A/'emblema-v8-3208-mask.png').convert('L').crop((230,130,971,1056))
_buf = io.BytesIO(); _e.save(_buf,'PNG')
EMBLEM_CROP = 'data:image/png;base64,' + base64.b64encode(_buf.getvalue()).decode()
TRACTOR = b64('tractor-motor-abierto-cutout.png', 'image/png')
EMBLEM = b64('emblema-v8-3208-mask.png', 'image/png')

# glyph-tight viewBoxes measured with getBBox()
LOGO_LINE_VB = '21 9 2177 303'
FONTS = '\n'.join([
    font('BigShoulders-Bold.ttf', 'Display', 700),
    font('IBMPlexMono-Regular.ttf', 'Mono', 400),
    font('IBMPlexMono-Bold.ttf', 'Mono', 700),
    font('InstrumentSerif-Regular.ttf', 'Serif', 400),
])

html = (HERE / 'cards.template.html').read_text()
html = (html.replace('{{FONTS}}', FONTS)
            .replace('{{TRACTOR}}', TRACTOR)
            .replace('{{EMBLEM_CROP}}', EMBLEM_CROP)
            .replace('{{EMBLEM}}', EMBLEM)
            .replace('{{LOGO_MAST}}', logo('logo-linea.svg', '#F2F0E9', LOGO_LINE_VB, 'mast'))
            .replace('{{LOGO_SMALL}}', logo('logo-linea.svg', '#F2F0E9', LOGO_LINE_VB, 'mini'))
            .replace('{{QR}}', qr()))
(HERE / 'cards.html').write_text(html)
print('ok', len(html))
