import numpy as np, json, cv2
from PIL import Image
f = np.array(Image.open('front.png').convert('RGB')).astype(int)
b = np.array(Image.open('back.png').convert('RGB')).astype(int)
bg = np.array([10, 10, 11])
def ink_bbox(a, thr=40):
    d = np.abs(a - bg).sum(-1) > thr
    ys, xs = np.where(d); return xs.min(), ys.min(), xs.max(), ys.max()
# back: everything must be in safe zone
print('back ink bbox', ink_bbox(b))
# front: text/logo only -> mask bone and yellow pixels outside the tractor raster region
H = json.load(open('hero.json'))
bone = (f[..., 0] > 200) & (f[..., 1] > 200) & (f[..., 2] > 195)
yel = (f[..., 0] > 200) & (f[..., 1] > 150) & (f[..., 2] < 80)
ys, xs = np.where(bone | yel); print('front bone/yellow bbox (incl. frame, tractor highlights)', xs.min(), ys.min(), xs.max(), ys.max())
# logo -> tractor vertical gap per column (logo = bone above y 230)
logo = bone.copy(); logo[230:] = False
lb = np.full(1125, -1)
for x in range(1125):
    c = np.where(logo[:, x])[0]
    if len(c): lb[x] = c.max()
al = np.array(Image.open('hero.png'))[..., 3] > 100
tt = np.full(1125, 9999)
for x in range(al.shape[1]):
    c = np.where(al[:, x])[0]
    X = x + H['x']
    if len(c) and 0 <= X < 1125: tt[X] = c.min() + H['y']
g = [(tt[x] - lb[x], x) for x in range(1125) if lb[x] >= 0 and tt[x] < 9999]
print('min logo->tractor gap', min(g))
print('tractor bbox (alpha>100): x', H['x'] + np.where(al.any(0))[0].min(), H['x'] + np.where(al.any(0))[0].max(), 'y', H['y'] + np.where(al.any(1))[0].min(), H['y'] + np.where(al.any(1))[0].max())
# serial tab vs tractor
tab = (961, 265, 1047, 313)
sub = al[tab[1]-H['y']:tab[3]+30-H['y'], tab[0]-30-H['x']:tab[2]-H['x']]
ys_, xs_ = np.where(sub)
print('tractor pixels near tab: min y', (ys_.min() + tab[1]) if len(ys_) else None)
# luminance: tyres vs ground
Y = 0.2126 * f[..., 0] + 0.7152 * f[..., 1] + 0.0722 * f[..., 2]
print('rear tyre mean lum', Y[420:520, 850:900].mean().round(1), 'front tyre', Y[530:580, 510:540].mean().round(1), 'ground', Y[30:60, 30:60].mean().round(1))
det = cv2.QRCodeDetector()
im = cv2.imread('back.png')
for s in (1.0, 0.6, 0.4):
    r = cv2.resize(im, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
    print('QR', s, repr(det.detectAndDecode(r)[0]))
