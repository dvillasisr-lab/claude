#!/usr/bin/env python3
import base64, pathlib, io, re, json, subprocess
from PIL import Image
import numpy as np
HERE = pathlib.Path(__file__).parent
A = HERE.parent.parent / 'assets'
FONTS = '/root/.claude/skills/synced/9983f56a-2d7a-4333-8a10-0941713cc597_0d8f03d3-28eb-42fc-935b-5b47bbd87cf0/canvas-design/canvas-fonts'
subprocess.run(['python3', str(HERE / 'hero.py')], check=True, capture_output=True)
P = json.loads((HERE / 'params.json').read_text())
H = json.loads((HERE / 'hero.json').read_text())
def b64f(p, mime): return f'data:{mime};base64,' + base64.b64encode(pathlib.Path(p).read_bytes()).decode()
def svg(name, fill=None, cls=''):
    s = (A / name).read_text(); s = s[s.index('<svg'):]
    if fill: s = s.replace('#F2F0E9', fill)
    s = s.replace('<svg class=""', '<svg', 1)
    return s.replace('<svg', f'<svg class="{cls}" preserveAspectRatio="xMinYMin meet"', 1)
def qr():
    s = (A / 'qr-tienda.svg').read_text(); s = s[s.index('<svg'):]
    return s.replace('<svg', '<svg style="display:block;width:100%;height:100%"', 1)

G = P['GROUND']
MX0, MX1 = P['MX0'], P['MX1']   # live area inset 8 px inside the safe zone so cut drift cannot make margins uneven
fx = H['front_contact'][0]
# ---------------- FRONT ----------------
F = []
# track: ground line from the safe edge to just under the front wheel, ticks every 10 ft ahead of the machine
PX = round(H['hitch_x'] - P['POST_AHEAD'])            # finish post x (left edge)
line_end = P['FRAME'][0] if P.get('FRAME') else round(fx + 30)
F.append(f'<img class="abs" id="herobg" src="{b64f(HERE/"hero-bg.png","image/png")}" style="left:{H["bg"][0]}px;top:{H["bg"][1]}px;width:{H["bg"][2]-H["bg"][0]}px;height:{H["bg"][3]-H["bg"][1]}px">')
FR = P.get('FRAME')
if FR:
    x0, y0, x1, y1 = FR; kw = P['FRAME_W']
    if P.get('FRAME_FILL'): F.append(f'<div class="abs" style="left:{x0}px;top:{y0}px;width:{x1-x0}px;height:{y1-y0}px;background:{P["FRAME_FILL"]}"></div>')
    F.append(f'<div class="abs" id="frame" style="left:{x0}px;top:{y0}px;width:{x1-x0}px;height:{y1-y0}px;border:{kw}px solid {P["FRAME_COL"]}"></div>')
F.append(f'<div class="abs rule" id="ground" style="left:{MX0}px;top:{G-1}px;width:{line_end-MX0}px;height:2px"></div>')
step = P['TICK']; x = PX + 2.5 + step; i = 1
while x < line_end - 4:
    h = 16 if i % 5 == 0 else 9
    F.append(f'<div class="abs rule" style="left:{x-1:.2f}px;top:{G-1-h}px;width:2px;height:{h}px"></div>')
    x += step; i += 1
F.append(f'<img class="abs" id="hero" src="{b64f(HERE/"hero.png","image/png")}" style="left:{H["x"]}px;top:{H["y"]}px;width:{H["w"]}px;height:{H["h"]}px">')
F.append(f'<div class="abs yel" id="post" style="left:{PX}px;top:{P["POST_T"]}px;width:5px;height:{G+P.get("POST_BELOW",8)-P["POST_T"]}px"></div>')
F.append(f'<div class="abs" id="flogo" data-safe style="left:{P["LOGO_X"]}px;top:{P["LOGO_Y"]}px">{svg("logo-linea.svg", "#F4F3EF", "logo logo-line")}</div>')
F.append(f'<div class="abs bs evil" id="evil" data-safe data-cap="{P["EVIL_CAP"]}" style="left:{P["LOGO_X"]-2}px">“THE EVIL ONE”</div>')
F.append(f'<div class="abs mono" id="fp-k" data-safe data-base="{G-12-P["PULL_FS"]*0.72-14}" style="left:{P["LOGO_X"]}px">Full pull</div>')
F.append(f'<div class="abs bs" id="fp-v" data-safe data-base="{G-12}" style="left:{P["LOGO_X"]-2}px;font-size:{P["PULL_FS"]}px">300<span class="mono" style="font-size:25px;margin-left:9px">FT</span></div>')
F.append(P.get('SERIAL_HTML', '').replace('{X}', str(P['LOGO_X'])).replace('{SB}', str(P.get('SERIAL_BASE', 584))).replace('{SR}', str(1125 - P['FRAME'][2] + P['FRAME_W'] if P.get('FRAME') else 75)))
FRONT = '\n'.join(F)
# ---------------- BACK ----------------
B = []
BX = MX0
LW = P['BLOGO_W']
B.append(f'<div class="abs" id="blogo" data-safe style="left:{BX}px;top:{P["BLOGO_Y"]}px">' + svg("logo-linea.svg", "#F4F3EF", "logo logo-line").replace('<svg class', '<svg style="width:%dpx" class' % LW) + '</div>')
B.append(f'<div class="abs mono" id="sub1" data-safe data-cap="{P["BLOGO_Y"]}" style="right:{1125-MX1}px">ProStock tractor pulling</div>')
B.append(f'<div class="abs mono" id="sub2" data-safe data-base="{P["BLOGO_Y"] + P["BLOGO_W"] * 0.13898}" style="right:{1125-MX1}px">Waterloo, Wisconsin</div>')


R1, R2 = P['R1'], P['R2']
BW = P['FRAME_W']
B.append(f'<div class="abs" id="statbox" style="left:{MX0}px;top:{R1}px;width:{MX1-MX0}px;height:{R2-R1}px;border:{BW}px solid var(--paper)"></div>')
ix0, ix1 = MX0 + BW, MX1 - BW; cw = (ix1 - ix0) / 4
stats = [('CAT V8', '3208', ''), ('Weight', '10,000', 'LB'), ('Rear tires', '24.5-32', ''), ('Full pull', '300', 'FT')]
PADX = P['STAT_PADX']
if P.get('BACK_TICKS'):
    step = P['BTICK']; x = ix0 + step; i = 1
    while x < ix1 - 2:
        h = 12 if i % 5 == 0 else 7
        B.append(f'<div class="abs rule" style="left:{x-1:.2f}px;top:{R2-BW-h}px;width:2px;height:{h}px"></div>')
        x += step; i += 1
for j, (k, v, u) in enumerate(stats):
    cx = ix0 + j * cw
    col = 'var(--y)' if j == 3 else 'var(--paper)'
    B.append(f'<div class="abs mono" data-safe data-cap="{R1+P["STAT_PAD"]}" style="left:{cx+PADX:.2f}px">{k}</div>')
    uu = f'<span class="mono" style="margin-left:9px;color:var(--paper)">{u}</span>' if u else ''
    B.append(f'<div class="abs bs stat" data-safe data-cap="{R1+P["STAT_PAD"]+18+P["STAT_GAP"]}" style="left:{cx+PADX-1:.2f}px;font-size:{P["STAT_FS"]}px;color:{col};letter-spacing:.005em">{v}{uu}</div>')
    if j: B.append(f'<div class="abs rule" style="left:{cx-1:.2f}px;top:{R1+BW}px;width:2px;height:{R2-R1-2*BW}px"></div>')
B.append(f'<div class="abs bs" id="ttl" data-safe data-cap="{R1 + BW / 2 - P["TTL_FS"] * 0.37}" style="left:{ix0 + PADX - 14}px;font-size:{P["TTL_FS"]}px;color:var(--y);letter-spacing:.01em;background:var(--ink);padding:0 14px">“THE EVIL ONE”</div>')
QCOL = ix0 + 3 * cw + PADX   # QR tile aligns with the text inset of the FULL PULL cell
B.append(f'<div class="abs bs" id="name" data-safe data-cap="{P["NAME_CAP"]}" style="left:{BX-4}px;font-size:{P["NAME_FS"]}px;letter-spacing:.005em">NOMBRE APELLIDO</div>')
B.append(f'<div class="abs mono" id="role" data-safe data-cap="{P["ROLE_CAP"]}" style="left:{BX}px">Team Owner · Driver</div>')
ct = [('Tel', '(000) 000-0000'), ('Mail', 'heavymetalevil72@gmail.com'), ('Web', 'heavymetalprostock.com')]
for j, (k, v) in enumerate(ct):
    B.append(f'<div class="abs mono ct" id="ct{j}" data-safe data-base="{P["CT_BASE"]+j*P["CT_LH"]}" style="left:{BX+1}px"><i>{k}</i>{v}</div>')
QS = P['QR_S']; QZ = P['QR_Z']; QZX = P['QR_ZX']; tw_ = QS + 2 * QZX; th_ = QS + 2 * QZ
QT = P['QT_T']
tw_ = MX1 - round(QCOL); QZX = (tw_ - QS) / 2
B.append(f'<div class="abs" id="qrt" data-safe style="left:{MX1-tw_}px;top:{QT}px;width:{tw_}px;height:{th_}px;background:var(--paper)"><div class="abs" style="left:{QZX}px;top:{QZ}px;width:{QS}px;height:{QS}px">{qr()}</div></div>')
B.append(f'<div class="abs mono" id="cap" data-safe data-base="{P["CAP_BASE"]}" style="left:{MX1-tw_}px;width:{tw_}px;text-align:center;letter-spacing:.04em;padding-left:.04em">Shop the gear</div>')
BACK = '\n'.join(B)

t = (HERE / 'template.html').read_text()
for k, v in {'{{FONTS}}': FONTS, '{{FRONT}}': FRONT, '{{BACK}}': BACK}.items(): t = t.replace(k, v)
for k, v in P.items(): t = t.replace('{{%s}}' % k, str(v))
left = re.findall(r'{{\w+}}', t); assert not left, left
(HERE / 'cards.html').write_text(t)
print('ok', len(t))
