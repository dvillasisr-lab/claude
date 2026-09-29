# Clean the hero cutout: remove smoke wisp by the stack, cap blown highlights, lift deep shadows slightly for press.
from PIL import Image
import numpy as np
im = np.array(Image.open('../../assets/tractor-motor-abierto-cutout.png')).astype(np.float32)
rgb, a = im[..., :3], im[..., 3]
lum = rgb.mean(-1)
# smoke wisp right of stack (dark, low-contrast pixels above the hood line)
ys, xs = np.mgrid[0:a.shape[0], 0:a.shape[1]]
wisp = (xs > 1010) & (ys < 150) & (((xs < 1092) & (lum < 130)) | ((xs < 1112) & (ys < 128) & (lum < 130)))
a[wisp] = 0
a[(xs > 1005) & (xs < 1112) & (ys < 150) & (a < 90)] = 0
# dark blobs flanking stack base above hood line
blob = (ys > 120) & (ys < 152) & (((xs > 900) & (xs < 928)) | ((xs > 1002) & (xs < 1035))) & (lum < 40)
# (kept: blobs are the hood lip)
# engine bay see-through holes -> fill with deep shadow so a background disc never leaks through
bay = (xs > 760) & (xs < 1010) & (ys > 225) & (ys < 340) & (a < 250)
rgb[bay] = rgb[bay] * (a[bay, None] / 255.0) + np.array([18, 18, 19]) * (1 - a[bay, None] / 255.0)
a[bay] = 255
# crisp the soft under-chassis / far-tyre edge
und = (xs > 880) & (xs < 1260) & (ys > 520) & (ys < 720)
a[und] = np.where(a[und] > 110, 255, 0)
# tone: shadow lift (0..40 -> 10..46), highlight cap 242
x = rgb / 255.0
x = 0.035 + x * (0.95 - 0.035) + 0.06 * x * (1 - x) ** 3 * 4
rgb = np.clip(x * 255, 0, 242)
out = np.dstack([rgb, a]).astype(np.uint8)
Image.fromarray(out, 'RGBA').save('tractor-hero.png', optimize=True)
print('ok')
