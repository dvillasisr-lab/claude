import json, sys, numpy as np
from PIL import Image
from rot import make
def place(th, w, right, cap=465, bite=8, save=None):
    d = make(th, save=save)
    s = w / d['W']
    left = right - w
    top = cap + bite - d['ly']*s
    return dict(angle=th, w=w, s=s, left=left, top=top, h=d['H']*s,
                rear=(left+d['lx']*s, top+d['ly']*s), front=(left+d['fx']*s, top+d['fy']*s))
if __name__ == '__main__':
    th, w, right = map(float, sys.argv[1:4])
    p = place(th, w, right, save='/tmp/claude-0/t.png')
    print(p)
    im = Image.open('/tmp/claude-0/t.png').resize((round(p['w']), round(p['h'])), Image.LANCZOS)
    a = np.array(im)[..., 3] > 100
    L, T = round(p['left']), round(p['top'])
    for y in range(80, 480, 20):
        r = np.nonzero(a[y-T]) [0] if 0 <= y-T < a.shape[0] else []
        print(' y', y, 'x', (r.min()+L, r.max()+L) if len(r) else '-')
