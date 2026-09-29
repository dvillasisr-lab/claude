import numpy as np, json
from PIL import Image
f=np.array(Image.open('/home/user/claude/print/swarm/r-iconic/round3/front.png').convert('RGB')).astype(float)
L=0.2126*f[...,0]+0.7152*f[...,1]+0.0722*f[...,2]
def r(n,x0,y0,x1,y1):
    s=L[y0:y1,x0:x1]; print(f'{n:14s} mean {s.mean():6.1f} median {np.median(s):6.1f} p90 {np.percentile(s,90):6.1f}')
r('hood',520,195,640,260); r('sidepanel',640,340,780,380); r('frontwhl',525,360,560,420); r('reartire tread',860,300,920,420); r('reartire side',975,420,1010,450); r('reartire all',850,260,1030,460); r('cage',840,160,930,230); r('ground',150,200,250,230)
