#!/usr/bin/env python3
import base64, pathlib, re, sys
HERE = pathlib.Path(__file__).parent
A = pathlib.Path('/home/user/claude/print/swarm/assets')
FONTS = '/root/.claude/skills/synced/9983f56a-2d7a-4333-8a10-0941713cc597_0d8f03d3-28eb-42fc-935b-5b47bbd87cf0/canvas-design/canvas-fonts'
def b64(p, mime): return f'data:{mime};base64,' + base64.b64encode(pathlib.Path(p).read_bytes()).decode()
def svg(name, fill, cls, vb=None):
    s = (A / name).read_text(); s = s[s.index('<svg'):]
    s = s.replace('#F2F0E9', fill).replace('#0a0b0c', fill)
    s = s.replace('<svg class=""', '<svg', 1)
    if vb: s = re.sub(r'viewBox="[^"]*"', f'viewBox="{vb}"', s, count=1)
    return s.replace('<svg', f'<svg data-safe="{cls}" class="{cls}" preserveAspectRatio="xMinYMin meet"', 1)
t = (HERE / 'template.html').read_text()
rep = {
  '{{FONTS}}': FONTS,
  '{{TRACTOR}}': b64(HERE / 'tractor-hero.png', 'image/png'),
  '{{LOGO_LINE}}': svg('logo-linea.svg', '#F2F0E9', 'logo-line', '20.66 8.68 2177.58 302.63'),
  '{{LOGO_LINE_SM}}': svg('logo-linea.svg', '#F2F0E9', 'logo-sm', '20.66 8.68 2177.58 302.63'),
  '{{LOGO_STACK}}': svg('logo-apilado.svg', '#F2F0E9', 'logo-stack', '20.66 8.73 1062.68 596.56'),
  '{{QR}}': open(HERE/'qr-path.svg').read().replace('<svg', '<svg class="qr"', 1),
}
for k, v in rep.items(): t = t.replace(k, v)
(HERE.parent / 'cards.html').write_text(t)
print('built', len(t))
