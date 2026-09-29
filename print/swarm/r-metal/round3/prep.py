# Hero cutout for round 2: clean wisp, fill engine bay, decontaminate edge colour,
# harden + re-antialias the alpha, smooth the under-chassis line, tone for press.
from PIL import Image, ImageFilter
import numpy as np
src = Image.open('../../assets/tractor-motor-abierto-cutout.png').convert('RGBA')
im = np.array(src).astype(np.float32)
rgb, a = im[..., :3], im[..., 3]
H, W = a.shape
ys, xs = np.mgrid[0:H, 0:W]
lum = rgb.mean(-1)
# 1. smoke wisp right of the stack
wisp = (xs > 1010) & (ys < 150) & (((xs < 1092) & (lum < 130)) | ((xs < 1112) & (ys < 128) & (lum < 130)))
a[wisp] = 0
a[(xs > 1005) & (xs < 1112) & (ys < 150) & (a < 90)] = 0
# 2. engine bay see-through: composite onto deep shadow over the whole bay (wider than round 1)
bay = (xs > 700) & (xs < 1150) & (ys > 225) & (ys < 470) & (a < 250) & (a > 0)
k = (a[bay] / 255.0)[:, None]
rgb[bay] = rgb[bay] * k + np.array([18, 18, 19]) * (1 - k)
a[bay] = 255
# 3. smooth under-chassis / far tyre edge: binarise, morphological close+open, blur, re-threshold
und = (xs > 700) & (xs < 1300) & (ys > 480) & (ys < 760)
m = Image.fromarray(((a > 110) * 255).astype(np.uint8))
m = m.filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.MinFilter(7))   # close pits
m = m.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.MaxFilter(5))   # remove specks
m = np.array(m.filter(ImageFilter.GaussianBlur(3))).astype(np.float32)
a[und] = m[und]
# 4. global alpha harden: choke ~1px, then a short ramp (≈0.5 px AA at card scale)
a = np.clip((a - 150) * (255 / 90), 0, 255)   # 150..240 -> 0..255
# 5. edge colour decontamination: pull partially transparent pixels to the colour of the
#    nearest solid pixels (dilated solid colour), so no background fringe survives
solid = a >= 250
acc = np.zeros_like(rgb); wgt = np.zeros(a.shape, np.float32)
for dy in range(-3, 4):
    for dx in range(-3, 4):
        s = np.roll(np.roll(solid, dy, 0), dx, 1)
        c = np.roll(np.roll(rgb, dy, 0), dx, 1)
        acc += c * s[..., None]; wgt += s
edge = (a > 0) & (a < 250) & (wgt > 0)
rgb[edge] = acc[edge] / wgt[edge][:, None]
# 6. tone: shadow lift for press, highlight cap 242
x = rgb / 255.0
x = 0.035 + x * (0.95 - 0.035) + 0.06 * x * (1 - x) ** 3 * 4
rgb = np.clip(x * 255, 0, 242)
out = np.dstack([rgb, a]).astype(np.uint8)
Image.fromarray(out, 'RGBA').save('tractor-hero.png', optimize=True)
ys2, xs2 = np.where(out[..., 3] > 128)
print('bbox', xs2.min(), xs2.max(), ys2.min(), ys2.max())
