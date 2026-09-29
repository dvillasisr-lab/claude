import numpy as np, json, sys
from PIL import Image
from rot import make
CAP=466;BITE=2;TOP=75;RIGHT=1049
for th in map(float,sys.argv[1:]):
    W,H,ly,*_=make(th,save='/tmp/claude-0/r.png')
    s=(CAP+BITE-TOP)/ly; w=W*s; left=RIGHT-w
    im=Image.open('/tmp/claude-0/r.png').resize((round(w),round(H*s)),Image.LANCZOS)
    a=np.array(im)[...,3]>100
    print('angle',th,'width',round(w),'left',round(left))
    for x in range(250,620,20):
        cx=x-round(left)
        if 0<=cx<a.shape[1]:
            col=np.nonzero(a[:,cx])[0]
            print('  x',x,'top',col.min()+TOP if len(col) else '-', 'bottom',col.max()+TOP if len(col) else '-')
