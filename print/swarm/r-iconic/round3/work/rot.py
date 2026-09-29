import numpy as np
from PIL import Image
im = Image.open('tractor-hero.png')
def make(th, save=None, src=None):
    pm = (src or im).convert('RGBa')
    r = pm.rotate(-th, resample=Image.BICUBIC, expand=True).convert('RGBA')  # -th: clockwise in PIL => we pass negative for nose-up
    a = np.array(r)[..., 3]
    ys, xs = np.nonzero(a > 128)
    r = r.crop((xs.min(), ys.min(), xs.max()+1, ys.max()+1)); a = np.array(r)[..., 3]
    ys, xs = np.nonzero(a > 128); W, H = r.size
    m = xs > 0.65*W; ly = ys[m].max(); lx = xs[m & (ys == ly)]
    fm = (xs > 0.2*W) & (xs < 0.5*W); fy = ys[fm].max(); fx = xs[fm & (ys == fy)]
    if save: r.save(save)
    return dict(W=W, H=H, ly=ly, lx=lx.mean(), fy=fy, fx=fx.mean(), rx=xs.max())
