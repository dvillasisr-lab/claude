#!/usr/bin/env python3
import base64, json, pathlib, sys
HERE = pathlib.Path(__file__).parent
A = HERE.parent.parent / 'assets'
FONTS = '/root/.claude/skills/synced/9983f56a-2d7a-4333-8a10-0941713cc597_0d8f03d3-28eb-42fc-935b-5b47bbd87cf0/canvas-design/canvas-fonts'
P = json.loads((HERE / 'params.json').read_text())
if len(sys.argv) > 1: P.update(json.loads(sys.argv[1]))
def b64(p, mime): return f'data:{mime};base64,' + base64.b64encode(p.read_bytes()).decode()
def svg(name, fill=None, cls=''):
    s = (A / name).read_text(); s = s[s.index('<svg'):]
    if fill: s = s.replace('#F2F0E9', fill).replace('#0a0b0c', fill)
    s = s.replace('<svg class=""', '<svg', 1)
    return s.replace('<svg', f'<svg class="{cls}" data-safe="" preserveAspectRatio="xMinYMin meet"', 1)
t = (HERE / 'template.html').read_text()
q = P['QRS']; off = (P['DD'] - q) / 2
rep = {'{{FONTS}}': FONTS,
  '{{TRACTOR}}': b64(HERE / 'tractor-hero.png', 'image/png'),
  '{{LOGO_LINE}}': svg('logo-linea.svg', '#F2F0E9', 'logo-line'),
  '{{LOGO_LINE_SM}}': svg('logo-linea.svg', '#F2F0E9', 'logo-sm').replace('<svg', '<svg style="left:74px;top:74px;width:284px;height:auto"', 1),
  '{{QR}}': svg('qr-tienda.svg', '#0A0A0C', 'qr').replace('<svg', f'<svg style="left:{off}px;top:{off}px;width:{q}px;height:{q}px"', 1)}
for k, v in P.items(): rep['{{%s}}' % k] = str(v)
for k, v in rep.items(): t = t.replace(k, v)
assert '{{' not in t, t[t.index('{{'):t.index('{{')+30]
(HERE / 'cards.html').write_text(t); print('ok', len(t))
