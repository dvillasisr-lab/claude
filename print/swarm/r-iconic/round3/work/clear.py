# min distance between each text/device element's ink and the tractor silhouette (front)
import numpy as np, json, cv2
from PIL import Image
P = json.load(open('placement.json'))
im = Image.open('tractor-final.png'); W, H = round(P['w']), round(P['h'])
a = np.array(im.resize((W, H), Image.LANCZOS))[..., 3] > 60
M = np.zeros((675, 1125), bool); L, T = round(P['left']), round(P['top'])
M[T:T+H, L:L+W] = a[:675-T, :1125-L][:H, :W]
dist = cv2.distanceTransform((~M).astype(np.uint8), cv2.DIST_L2, 5)
ink = np.array(Image.open('../work/ink-front.png').convert('RGB')).astype(int)
inkm = np.abs(ink - [11, 11, 12]).sum(2) > 60
boxes = json.load(open('boxes.json'))
for card, name, x0, y0, x1, y1 in boxes:
    if card != 'front' or name in ('logo-line',): continue
    sub = inkm[max(y0-2,0):y1+2, max(x0-2,0):x1+2]
    d = dist[max(y0-2,0):y1+2, max(x0-2,0):x1+2][sub]
    ys, xs = np.nonzero(sub)
    print(f'{name:8s} ink x {xs.min()+max(x0-2,0)}-{xs.max()+max(x0-2,0)} y {ys.min()+max(y0-2,0)}-{ys.max()+max(y0-2,0)}  min dist to tractor {d.min():.0f}')
ys, xs = np.nonzero(M); print('tractor bbox', xs.min(), ys.min(), xs.max(), ys.max())
# logo clearance from tractor except contact
logo = inkm.copy(); logo[:460] = False
print('logo-tractor min dist', dist[logo].min())
