#!/usr/bin/env python3
"""Builds cards.html (Swiss motorsport poster direction) from template.html."""
import base64, pathlib, re
HERE = pathlib.Path(__file__).parent
A = HERE.parent / 'assets'
FONTS = '/root/.claude/skills/synced/9983f56a-2d7a-4333-8a10-0941713cc597_0d8f03d3-28eb-42fc-935b-5b47bbd87cf0/canvas-design/canvas-fonts'

def b64(p, mime):
    return f'data:{mime};base64,' + base64.b64encode(p.read_bytes()).decode()

def svg(name, fill=None, cls=''):
    s = (A / name).read_text()
    s = s[s.index('<svg'):]
    if fill: s = s.replace('#F2F0E9', fill).replace('#0a0b0c', fill)
    s = s.replace('<svg class=""', '<svg', 1)
    return s.replace('<svg', f'<svg class="{cls}" preserveAspectRatio="xMinYMin meet"', 1)

t = (HERE / 'template.html').read_text()
rep = {
  '{{FONTS}}': FONTS,
  '{{TRACTOR}}': b64(A / 'tractor-motor-abierto-cutout.png', 'image/png'),
  '{{LOGO_STACK}}': svg('logo-apilado.svg', '#F2F0E9', 'logo-stack'),
  '{{LOGO_LINE}}': svg('logo-linea.svg', '#F2F0E9', 'logo-line'),
  '{{QR}}': svg('qr-tienda.svg', None, 'qr'),
}
for k, v in rep.items(): t = t.replace(k, v)
(HERE / 'cards.html').write_text(t)
print('ok', len(t))
