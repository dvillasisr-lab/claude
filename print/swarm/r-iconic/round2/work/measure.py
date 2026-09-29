import numpy as np, json, sys
from PIL import Image
OUT='/home/user/claude/print/swarm/r-iconic/round2'
def bbox(m):
    ys,xs=np.nonzero(m); 
    return (xs.min(),ys.min(),xs.max(),ys.max()) if len(xs) else None
for side in ['front','back']:
    a=np.array(Image.open(f'{OUT}/work/ink-{side}.png').convert('RGB')).astype(int)
    bg=np.array([11,11,12])
    ink=(np.abs(a-bg).sum(2)>30)
    bb=bbox(ink)
    out=ink.copy(); out[75:601,75:1051]=False
    print(side,'ink bbox',bb,'pixels outside safe:',out.sum())
    full=np.array(Image.open(f'{OUT}/{side}.png').convert('RGB')).astype(int)
    chroma=(full.max(2)-full.min(2))
    # chromatic pixels among near-neutral text areas (exclude yellow & photo)
    yel=(full[...,0]>150)&(full[...,2]<120)
    print(side,'max chroma outside yellow',chroma[~yel].max() if side=='back' else '-', )
def rows(side, x0,x1,y0,y1,thr=60):
    a=np.array(Image.open(f'{OUT}/work/ink-{side}.png').convert('L')).astype(int)[y0:y1,x0:x1]
    m=a>thr; r=np.nonzero(m.any(1))[0]; c=np.nonzero(m.any(0))[0]
    # group rows into bands
    bands=[];s=None;prev=None
    for y in r:
        if s is None: s=y
        elif y!=prev+1: bands.append((s+y0,prev+y0)); s=y
        prev=y
    if s is not None: bands.append((s+y0,prev+y0))
    return bands, (c.min()+x0, c.max()+x0) if len(c) else None
if len(sys.argv)>1:
    for spec in sys.argv[1:]:
        side,*v=spec.split(':'); v=list(map(int,v[0].split(',')))
        print(spec, rows(side,*v))
