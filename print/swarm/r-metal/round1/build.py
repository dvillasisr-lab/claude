#!/usr/bin/env python3
import base64, pathlib, sys
HERE = pathlib.Path(__file__).parent
A = HERE.parent.parent / 'assets'
FONTS = '/root/.claude/skills/synced/9983f56a-2d7a-4333-8a10-0941713cc597_0d8f03d3-28eb-42fc-935b-5b47bbd87cf0/canvas-design/canvas-fonts'
def b64(p, mime): return f'data:{mime};base64,' + base64.b64encode(p.read_bytes()).decode()
def svg(name, fill=None, cls=''):
    s = (A / name).read_text(); s = s[s.index('<svg'):]
    if fill: s = s.replace('#F2F0E9', fill).replace('#0a0b0c', fill)
    s = s.replace('<svg class=""', '<svg', 1)
    return s.replace('<svg', f'<svg class="{cls}" data-safe="" preserveAspectRatio="xMinYMin meet"', 1)
src = sys.argv[1] if len(sys.argv) > 1 else 'template.html'
out = sys.argv[2] if len(sys.argv) > 2 else 'cards.html'
t = (HERE / src).read_text()
rep = {'{{FONTS}}': FONTS,
  '{{TRACTOR}}': b64(HERE / 'tractor-hero.png', 'image/png'),
  '{{LOGO_LINE}}': svg('logo-linea.svg', '#F2F0E9', 'logo-line'),
  '{{LOGO_LINE_SM}}': svg('logo-linea.svg', '#F2F0E9', 'logo-sm'),
  '{{LOGO_STACK}}': svg('logo-apilado.svg', '#F2F0E9', 'logo-stack'),
  '{{QR}}': svg('qr-tienda.svg', None, 'qr')}
for k, v in rep.items(): t = t.replace(k, v)
(HERE / out).write_text(t); print('ok', out, len(t))
