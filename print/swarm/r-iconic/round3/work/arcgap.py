import numpy as np
from PIL import Image
a=np.array(Image.open('ink-back.png').convert('RGB')).astype(int)
import json; S=json.load(open("params.json"))["seal"]; cx,cy,D=S["cx"],S["cy"],S["disc"]
yy,xx=np.mgrid[0:675,0:1125]; r=np.hypot(xx+.5-cx,yy+.5-cy)
# silver text pixels: neutral grey-ish, not yellow, not bone disc
sil=(np.abs(a[...,0]-a[...,2])<25)&(a.sum(2)>200)&(r>D+2)&(r<200)
dots=(np.abs(yy+.5-cy)<8)
for name,m in [('top',sil&(yy<cy-10)&~dots),('bottom',sil&(yy>cy+10)&~dots)]:
    rr=r[m]; print(name,'ink r %.1f-%.1f'%(rr.min(),rr.max()),'gap to disc %.1f'%(rr.min()-D),'gap to ring inner(202.5) %.1f'%(202.5-rr.max()),
      ' p2-p98 %.1f-%.1f'%(np.percentile(rr,2),np.percentile(rr,98)))
