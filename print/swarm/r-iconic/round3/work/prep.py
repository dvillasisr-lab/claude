# Hero cutout for press: clean fringe, PIL curves (not CSS) so the black machine holds on rich black.
import numpy as np, json, sys
from PIL import Image, ImageFilter
src = Image.open('/home/user/claude/print/swarm/assets/tractor-motor-abierto-cutout.png').convert('RGBA')
A = np.array(src).astype(np.float32)
rgb, a = A[..., :3], A[..., 3]
a[a < 60] = 0
H, W = a.shape
C = json.load(open('curves.json'))
def lut(xs, ys):
    l = np.interp(np.arange(256), xs, ys); pad = np.pad(l, 6, mode='edge')
    return np.convolve(pad, np.ones(13)/13, 'valid')
body = lut(*C['body']); tyre = lut(*C['tyre'])
# soft masks for the two tyres (source coords)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
def ell(cx, cy, rx, ry, feather):
    d = np.sqrt(((xx-cx)/rx)**2 + ((yy-cy)/ry)**2)
    return np.clip((1-d)/feather + .5, 0, 1)
tm = np.maximum(ell(C['rear'][0]*W, C['rear'][1]*H, C['rear'][2]*W, C['rear'][3]*H, .08),
                ell(C['front'][0]*W, C['front'][1]*H, C['front'][2]*W, C['front'][3]*H, .08))
idx = np.clip(rgb, 0, 255).astype(np.uint8)
out = body[idx]*(1-tm[..., None]) + tyre[idx]*tm[..., None]
img = Image.fromarray(np.dstack([out, a]).clip(0, 255).astype(np.uint8), 'RGBA')
# gentle local contrast so the lifted blacks stay crisp, not flat grey
r, g, b, al = img.split()
rgbim = Image.merge('RGB', (r, g, b)).filter(ImageFilter.UnsharpMask(radius=6, percent=C.get('usm', 40), threshold=2))
img = Image.merge('RGBA', (*rgbim.split(), al))
img.save('tractor-hero.png')
np.save('tyremask.npy', (tm > .5))
# stats in source coords
Lm = np.array(rgbim.convert('L')).astype(float); m = a > 200
def reg(name, x0, x1, y0, y1, cap=None, extra=None):
    s = (slice(int(y0*H), int(y1*H)), slice(int(x0*W), int(x1*W)))
    v = Lm[s][m[s]]
    if cap: v = v[v < cap]
    print(f'{name:10s} mean {v.mean():6.1f} p10 {np.percentile(v,10):6.1f} p50 {np.percentile(v,50):6.1f} p90 {np.percentile(v,90):6.1f}')
reg('hood', .17, .42, .20, .45)
reg('hoodpaint', .17, .42, .20, .45, cap=150)
reg('reartire', .73, .97, .30, .92)
reg('cage', .67, .82, .02, .25)
reg('frontwhl', .28, .42, .70, .97)
reg('body', .45, .70, .55, .75)
