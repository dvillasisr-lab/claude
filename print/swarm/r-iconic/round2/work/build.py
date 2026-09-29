#!/usr/bin/env python3
# Round 2 build: computes the wheelie placement from the cutout's alpha and writes ../cards.html
import base64, pathlib, re, math, json, sys
from rot import make
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

# ---- tractor placement (rear tyre lowest pixel lands on the METAL A shoulder) ----
th = P['angle']
W, H, ly, lxa, lxb, fy, fx, ny = make(th, save=str(HERE/'tractor-final.png'))
CAP = P['cap']; s = (CAP + P['bite'] - P['ttop']) / ly
tw = W*s; tleft = P['tright'] - tw
info = dict(angle=th, width=round(tw,1), left=round(tleft,1), top=P['ttop'], height=round(H*s,1),
            rear_contact_x=(round(tleft+lxa*s,1), round(tleft+lxb*s,1)), rear_contact_y=round(P['ttop']+ly*s,1),
            front_wheel_bottom=round(P['ttop']+fy*s,1), front_x=round(tleft+fx*s,1), nose_bottom=round(P['ttop']+ny*s,1))
print(json.dumps(info))

# ---- seal arc text ----
def arc(text, cx, cy, r, top=True, fs=28, track=.16, cls='arc'):
    adv = (0.6 + track) * fs
    n = len(text); total = adv * (n - 1)
    out = []
    for i, ch in enumerate(text):
        if ch == ' ': continue
        off = (i * adv - total/2) / r            # radians along the arc
        if top:
            ang = -math.pi/2 + off; rot = math.degrees(off)
        else:
            ang = math.pi/2 - off; rot = -math.degrees(off)
        x = cx + r*math.cos(ang); y = cy + r*math.sin(ang)
        out.append(f'<text x="{x:.2f}" y="{y:.2f}" transform="rotate({rot:.3f} {x:.2f} {y:.2f})" text-anchor="middle">{ch}</text>')
    return '\n    '.join(out)
S = P['seal']
cx, cy, R = S['cx'], S['cy'], S['r']
fs = S['fs']; capH = 0.698*fs   # Plex Mono cap height
band_mid = (S['disc'] + R - S['stroke']/2)/2
top_r = band_mid - capH/2       # baseline radius, letters grow outward
bot_r = band_mid + capH/2       # baseline radius, letters grow inward
arcs = arc(S['top'], cx, cy, top_r, True, fs, S['track']) + '\n    ' + arc(S['bottom'], cx, cy, bot_r, False, fs, S['track'])
dots = f'<circle cx="{cx-band_mid:.2f}" cy="{cy}" r="4.5" fill="#A9ADB1"/><circle cx="{cx+band_mid:.2f}" cy="{cy}" r="4.5" fill="#A9ADB1"/>'
qr = (HERE/'qr-path.svg').read_text().replace('<svg', '<svg class="qr"', 1)

t = (HERE/'template.html').read_text()
rep = {'{{FONTS}}': FONTS, '{{TRACTOR}}': b64(HERE/'tractor-final.png','image/png'),
       '{{TW}}': f'{tw:.2f}', '{{TL}}': f'{tleft:.2f}', '{{TT}}': str(P['ttop']),
       '{{LOGO}}': logo('#F2F0E9','logo-line'), '{{LOGO_SM}}': logo('#F2F0E9','logo-sm'),
       '{{CX}}': str(cx), '{{CY}}': str(cy), '{{R}}': str(R), '{{STROKE}}': str(S['stroke']), '{{DISC}}': str(S['disc']),
       '{{ARCS}}': arcs, '{{DOTS}}': dots, '{{QR}}': qr, '{{QRS}}': str(S['qr']),
       '{{QRX}}': f"{cx - S['qr']/2:.2f}", '{{QRY}}': f"{cy - S['qr']/2:.2f}"}
for k, v in P.get('css', {}).items(): rep['{{'+k+'}}'] = str(v)
for k, v in rep.items(): t = t.replace(k, v)
left = re.findall(r'\{\{[A-Z_]+\}\}', t)
if left: print('UNFILLED', left)
(HERE.parent/'cards.html').write_text(t)
(HERE/'placement.json').write_text(json.dumps(info))
