#!/usr/bin/env python3
"""Builds cards.html (premium collectible card direction) from template.html."""
import base64, pathlib, io
from PIL import Image, ImageEnhance
import numpy as np
HERE = pathlib.Path(__file__).parent
A = HERE.parent.parent / 'assets'
FONTS = '/root/.claude/skills/synced/9983f56a-2d7a-4333-8a10-0941713cc597_0d8f03d3-28eb-42fc-935b-5b47bbd87cf0/canvas-design/canvas-fonts'

def b64(data, mime):
    return f'data:{mime};base64,' + base64.b64encode(data).decode()

def tractor():
    im = Image.open(A / 'tractor-motor-abierto-cutout.png').convert('RGBA')
    a = np.array(im).astype(np.float32)
    rgb = a[:, :, :3]
    # shadow lift on levels 0..48 so the black body holds detail on press
    lift = np.where(rgb < 48, rgb + (48 - rgb) * 0.22, rgb)
    # tame blown stack highlight to ~240
    lift = np.minimum(lift, 242)
    a[:, :, :3] = lift
    # remove faint smoke / fringe: kill very low alpha
    al = a[:, :, 3]
    al[al < 24] = 0
    a[:, :, 3] = al
    out = Image.fromarray(a.clip(0, 255).astype(np.uint8), 'RGBA')
    buf = io.BytesIO(); out.save(buf, 'PNG', optimize=True)
    return b64(buf.getvalue(), 'image/png')

def svg(name, fill=None, cls=''):
    s = (A / name).read_text()
    s = s[s.index('<svg'):]
    if fill: s = s.replace('#F2F0E9', fill).replace('#0a0b0c', fill)
    s = s.replace('<svg class=""', '<svg', 1)
    return s.replace('<svg', f'<svg class="{cls}" preserveAspectRatio="xMinYMin meet"', 1)

def emblem():
    im = Image.open(A / 'emblema-v8-3208-mask.png').convert('L')
    im = im.crop(im.getbbox())
    rgba = Image.new('RGBA', im.size, (242, 240, 233, 0)); rgba.putalpha(im)
    buf = io.BytesIO(); rgba.save(buf, 'PNG'); return b64(buf.getvalue(), 'image/png')

t = (HERE / 'template.html').read_text()
rep = {
  '{{FONTS}}': FONTS,
  '{{TRACTOR}}': tractor(),
  '{{LOGO_STACK}}': svg('logo-apilado.svg', '#F4F3EF', 'logo logo-stack'),
  '{{LOGO_LINE}}': svg('logo-linea.svg', '#F4F3EF', 'logo logo-line'),
  '{{LOGO_LINE_SM}}': svg('logo-linea.svg', '#F4F3EF', 'logo logo-line-sm'),
  '{{QR}}': svg('qr-tienda.svg', None, 'qr'),
  '{{EMBLEM}}': emblem(),
}
for k, v in rep.items(): t = t.replace(k, v)
(HERE / 'cards.html').write_text(t)
print('ok', len(t))
