import numpy as np, math, sys
from PIL import Image
im=Image.open('tractor-hero.png')
def make(th, save=None):
    pm=im.convert('RGBa')
    r=pm.rotate(-th, resample=Image.BICUBIC, expand=True)  # PIL positive=CCW, so -th = clockwise
    r=r.convert('RGBA')
    a=np.array(r)[...,3]
    ys,xs=np.nonzero(a>128)
    x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
    r=r.crop((x0,y0,x1+1,y1+1)); a=np.array(r)[...,3]
    ys,xs=np.nonzero(a>128)
    W,H=r.size
    # rear contact: lowest pixels in right 35%
    m=xs>0.65*W; ly=ys[m].max(); lx=xs[m&(ys==ly)]
    fm=(xs>0.2*W)&(xs<0.5*W); fy=ys[fm].max(); fx=xs[fm&(ys==fy)]
    nm=xs<0.2*W; ny=ys[nm].max()
    if save: r.save(save)
    return W,H,ly,lx.min(),lx.max(),fy,fx.mean(),ny
if __name__=='__main__':
  CAP=466; BITE=float(sys.argv[1]) if len(sys.argv)>1 else 2
  for th in [6,7,8,9,10,11,12]:
    W,H,ly,lxa,lxb,fy,fx,ny=make(th)
    s=(CAP+BITE-75)/ly   # top at 75, rear lowest at CAP+BITE
    w=W*s; left=1049-w
    print(th,'w %.0f s %.4f left %.0f  rear contact x %.0f-%.0f  front wheel lift %.1f  front x %.0f  nose lift %.1f  bottom %.0f'%(w,s,left,left+lxa*s,left+lxb*s,(ly-fy)*s,left+fx*s,(ly-ny)*s,75+H*s))
