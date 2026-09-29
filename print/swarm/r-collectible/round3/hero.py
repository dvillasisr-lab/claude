"""Builds the front hero raster at 300 ppi (1 canvas px = 1 image px):
tractor + tone work for press + rim light + floor light pool + contact shadows, one RGBA PNG."""
import json, pathlib, numpy as np
from PIL import Image, ImageFilter
HERE = pathlib.Path(__file__).parent
A = HERE.parent.parent / 'assets'
P = json.loads((HERE / 'params.json').read_text())
s = P['TR_S']; R = P['TR_R']; G = P['GROUND']
L = R - 1669 * s; T = G - 844 * s
# canvas-size RGBA layer (easier maths), cropped to bbox at the end
W, H = 1125, 675
src = Image.open(A / 'tractor-motor-abierto-cutout.png').convert('RGBA')
tw, th = round(1671 * s), round(846 * s)
# premultiplied resize to avoid dark/light fringes
a = np.array(src).astype(np.float32) / 255
pm = a.copy(); pm[..., :3] *= a[..., 3:4]
pm_img = [Image.fromarray((pm[..., i] * 255).astype(np.uint8)) for i in range(4)]
pm_r = np.stack([np.array(c.resize((tw, th), Image.LANCZOS)).astype(np.float32) / 255 for c in pm_img], -1)
al = pm_r[..., 3:4]
rgb = np.where(al > 0.002, pm_r[..., :3] / np.maximum(al, 1e-4), 0).clip(0, 1) * 255
al = al[..., 0]
# kill smoke / fringe
al[al < 24 / 255] = 0
# tone for press: lift shadows (0..60 -> +), cap stack highlight, extra lift on the rear tyre
lum = rgb.mean(-1, keepdims=True)
lift = np.where(rgb < 64, rgb + (64 - rgb) * 0.30, rgb)
xs = np.arange(tw)[None, :, None]
rear = np.clip((xs - 1330 * s) / (80 * s), 0, 1)   # ramps in over the rear tyre
lift = lift + rear * np.where(lift < 110, 12 * (1 - lift / 110), 0)
lift = np.minimum(lift, 238)
rgb = lift
# place on canvas
lay = np.zeros((H, W, 4), np.float32)
ox, oy = round(L), round(T)
def paste(dst, src, ox, oy):
    h, w = src.shape[:2]
    x0, y0 = max(ox, 0), max(oy, 0); x1, y1 = min(ox + w, W), min(oy + h, H)
    dst[y0:y1, x0:x1] = src[y0 - oy:y1 - oy, x0 - ox:x1 - ox]
trac = np.zeros((H, W, 4), np.float32)
paste(trac, np.dstack([rgb, al * 255]), ox, oy)
ta = trac[..., 3] / 255
# rim light: 1.5 px outside ring, stronger on the nose and front wheel
A_img = Image.fromarray((ta * 255).astype(np.uint8))
dil = np.array(A_img.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(0.6))).astype(np.float32) / 255
ring = np.clip(dil - ta, 0, 1)
X = np.arange(W)[None, :]
nose_x1 = L + 700 * s
rim_op = np.where(X < nose_x1, 0.42, 0.26) * np.ones((H, W))
ring = ring * rim_op
# light pool: soft floor ellipse under the machine + a back-light behind the nose (lighting, not decoration)
def ell(cx, cy, rx, ry, peak, blur):
    im = Image.new('L', (W, H), 0)
    from PIL import ImageDraw
    ImageDraw.Draw(im).ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=255)
    return np.array(im.filter(ImageFilter.GaussianBlur(blur))).astype(np.float32) / 255 * peak
fx, fy = L + 575 * s, G; rx_, ry_ = L + 1494 * s, T + 754 * s
pool = ell(L + 330 * s, T + 520 * s, 175, 105, 1.0, 55) * P['POOL_NOSE']
pool = np.maximum(pool, ell((fx + rx_) / 2 + 20, (fy + ry_) / 2 + 4, 330, 34, 1.0, 26) * P['POOL_FLOOR'])
# contact shadows (darker than the pool) under both tyres
shad = np.maximum(ell(fx, fy - 2, 62, 7, 1.0, 5), ell(rx_ - 6, ry_ - 2, 88, 8, 1.0, 6))
# compose background-light layer (grey with alpha) then tractor over it
bone = np.array([244, 243, 239], np.float32)
glow_col = np.array([46, 47, 51], np.float32)   # pool colour, alpha carries the falloff
out = np.zeros((H, W, 4), np.float32)
# pool
pa = pool * (1 - shad * 0.95)
out[..., :3] = glow_col; out[..., 3] = pa
# contact shadow: black with alpha over pool
sa = shad * 0.9
c = out[..., :3] * out[..., 3:4] * (1 - sa[..., None])
aa = out[..., 3] * (1 - sa) + sa
out[..., :3] = np.where(aa[..., None] > 0, c / np.maximum(aa[..., None], 1e-4), 0); out[..., 3] = aa
# rim ring (bone) over
def over(dst, col, a):
    a = a[..., None]
    da = dst[..., 3:4]
    na = a + da * (1 - a)
    dst[..., :3] = np.where(na > 0, (col * a + dst[..., :3] * da * (1 - a)) / np.maximum(na, 1e-4), 0)
    dst[..., 3:4] = na
def save(arr, name):
    a = arr.copy(); a[..., 3] *= 255
    img = Image.fromarray(a.clip(0, 255).astype(np.uint8), 'RGBA'); bb = img.getbbox(); img.crop(bb).save(HERE / name, optimize=True)
    return bb
bgbb = save(out, 'hero-bg.png')          # light pool + contact shadows: sits UNDER the card frame
fg = np.zeros((H, W, 4), np.float32)
over(fg, bone, ring)
over(fg, trac[..., :3], ta)
bb = save(fg, 'hero.png')                # tractor + rim light: sits OVER the card frame
json.dump({'bg': list(bgbb), 'x': bb[0], 'y': bb[1], 'w': bb[2] - bb[0], 'h': bb[3] - bb[1], 'L': L, 'T': T,
           'front_contact': [fx, fy], 'rear_contact': [rx_, ry_],
           'stack_x': [L + 950 * s, L + 1010 * s], 'cage_x': [L + 1150 * s, L + 1370 * s],
           'hitch_x': L + 5 * s, 'nose_x': L + 280 * s}, open(HERE / 'hero.json', 'w'), indent=1)
print(json.load(open(HERE / 'hero.json')))
