#!/usr/bin/env python3
import base64, pathlib, re, math, json
import numpy as np
from PIL import Image, ImageFilter
from place import place
HERE = pathlib.Path(__file__).parent
A = pathlib.Path('/home/user/claude/print/swarm/assets')
FONTS = '/root/.claude/skills/synced/9983f56a-2d7a-4333-8a10-0941713cc597_0d8f03d3-28eb-42fc-935b-5b47bbd87cf0/canvas-design/canvas-fonts'
P = json.loads((HERE/'params.json').read_text())
def b64(p, mime): return f'data:{mime};base64,' + base64.b64encode(pathlib.Path(p).read_bytes()).decode()
def logo(fill, cls):
    s = (A/'logo-linea.svg').read_text(); s = s[s.index('<svg'):]
    s = s.replace('#F2F0E9', fill)
    s = re.sub(r'viewBox="[^"]*"', 'viewBox="20.66 8.68 2177.58 302.63"', s, count=1)
    s = re.sub(r'<svg[^>]*?(?=\sviewBox)', '<svg xmlns="http://www.w3.org/2000/svg"', s, count=1)
    return s.replace('<svg', f'<svg data-safe="{cls}" class="{cls}" preserveAspectRatio="xMinYMin meet" role="img" aria-label="Heavy Metal"', 1)

# ---------- tractor ----------
T = P['tractor']
pl = place(T['angle'], T['w'], T['right'], cap=T['cap'], bite=T['bite'], save=str(HERE/'tractor-rot.png'))
im = Image.open(HERE/'tractor-rot.png').convert('RGBA')
# 1 px bone rim light baked behind the cutout (0 0 1px rgba(242,240,233,.25))
if T.get('rim', 0) > 0:
    a = im.split()[3]
    halo = a.filter(ImageFilter.GaussianBlur(T['rim_blur']))
    halo = Image.fromarray((np.array(halo).astype(float) * T['rim']).clip(0, 255).astype(np.uint8))
    rim = Image.new('RGBA', im.size, (242, 240, 233, 0)); rim.putalpha(halo)
    im = Image.alpha_composite(rim, im)
im.save(HERE/'tractor-final.png')
info = {k: (round(float(v), 1) if not isinstance(v, tuple) else tuple(round(float(x), 1) for x in v)) for k, v in pl.items()}
print('tractor', json.dumps(info))

# ---------- seal ----------
def arc(text, cx, cy, r, top=True, fs=28, track=.14):
    adv = (0.6 + track) * fs; n = len(text); total = adv * (n - 1); out = []
    for i, ch in enumerate(text):
        if ch == ' ': continue
        off = (i * adv - total/2) / r
        if top: ang = -math.pi/2 + off; rot = math.degrees(off)
        else:   ang = math.pi/2 - off; rot = -math.degrees(off)
        x = cx + r*math.cos(ang); y = cy + r*math.sin(ang)
        out.append(f'<text x="{x:.2f}" y="{y:.2f}" transform="rotate({rot:.3f} {x:.2f} {y:.2f})" text-anchor="middle">{ch}</text>')
    return '\n    '.join(out), math.degrees(total/r)

rep = {'{{FONTS}}': FONTS, '{{TRACTOR}}': b64(HERE/'tractor-final.png', 'image/png'),
       '{{TW}}': f"{pl['w']:.2f}", '{{TL}}': f"{pl['left']:.2f}", '{{TT}}': f"{pl['top']:.2f}",
       '{{LOGO}}': logo('#F2F0E9', 'logo-line')}
S = P.get('seal')
if S:
    cx, cy, R = S['cx'], S['cy'], S['r']; fs = S['fs']; capH = 0.698*fs
    inner = R - S['stroke']/2
    band_mid = (S['disc'] + inner)/2
    ta, tdeg = arc(S['top'], cx, cy, band_mid - capH/2 + S.get('top_adj', 0), True, fs, S['track'])
    ba, bdeg = arc(S['bottom'], cx, cy, band_mid + capH/2 + S.get('bot_adj', 0), False, fs, S['track'])
    print('arc spans', round(tdeg, 1), round(bdeg, 1))
    dots = f'<circle cx="{cx-band_mid:.2f}" cy="{cy}" r="4.5" fill="#A9ADB1"/><circle cx="{cx+band_mid:.2f}" cy="{cy}" r="4.5" fill="#A9ADB1"/>'
    q = S['qr']
    qr = (HERE/'qr-path.svg').read_text().replace('<svg', f'<svg class="qr" style="position:absolute;left:{cx-q/2:.2f}px;top:{cy-q/2:.2f}px;width:{q}px;height:{q}px"', 1)
    rep['{{SEAL}}'] = (f'<svg class="seal" style="position:absolute;left:0;top:0;width:1125px;height:675px" viewBox="0 0 1125 675" data-safe="seal">'
        f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="#F5C400" stroke-width="{S["stroke"]}"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{S["disc"]}" fill="#F2F0E9"/>\n    {ta}\n    {ba}\n    {dots}</svg>\n  {qr}')
for k, v in P['vars'].items(): rep['{{'+k+'}}'] = str(v)
t = (HERE/'template.html').read_text()
for _ in range(2):
    for k, v in rep.items(): t = t.replace(k, v)
left = re.findall(r'\{\{[A-Z_]+\}\}', t)
if left: print('UNFILLED', left)
(HERE.parent/'cards.html').write_text(t)
(HERE/'placement.json').write_text(json.dumps(info))
