import numpy as np, json, sys
from PIL import Image
im = Image.open('tractor-final.png'); P = json.load(open('placement.json'))
W, H = round(P['w']), round(P['h'])
a = np.array(im.resize((W, H), Image.LANCZOS)).astype(float)
L = 0.2126*a[...,0] + 0.7152*a[...,1] + 0.0722*a[...,2]; m = a[...,3] > 200
def reg(name, x0, x1, y0, y1):
    sub = L[int(y0*H):int(y1*H), int(x0*W):int(x1*W)][m[int(y0*H):int(y1*H), int(x0*W):int(x1*W)]]
    print(f'{name:10s} mean {sub.mean():6.1f}  p10 {np.percentile(sub,10):6.1f}  p90 {np.percentile(sub,90):6.1f}')
reg('hood', 0.22, 0.42, 0.18, 0.40)
reg('sidepanel', 0.45, 0.62, 0.55, 0.72)
reg('frontwhl', 0.28, 0.40, 0.68, 0.98)
reg('reartire', 0.74, 0.97, 0.40, 0.95)
reg('cage', 0.68, 0.82, 0.04, 0.30)
reg('all', 0, 1, 0, 1)
