# Prepares the hero cutout: removes smoke wisps / low-alpha fringe, lifts shadows for press, tames blown stack top.
import numpy as np
from PIL import Image
src = Image.open('/home/user/claude/print/swarm/assets/tractor-motor-abierto-cutout.png').convert('RGBA')
A = np.array(src).astype(np.float32)
rgb, a = A[..., :3], A[..., 3]
a[a < 60] = 0                                  # smoke / fringe wisps
# shadow lift (curve on 0..60) + highlight cap at 242
x = rgb / 255.0
lift = 0.035 * (1 - x) ** 3
x = x + lift
x = np.minimum(x, 242 / 255.0)
# gentle global contrast on midtones so black paint reads as satin
x = np.clip(x, 0, 1)
out = np.dstack([x * 255, a]).clip(0, 255).astype(np.uint8)
Image.fromarray(out, 'RGBA').save('tractor-hero.png')
print('ok')
