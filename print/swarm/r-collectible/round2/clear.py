import numpy as np, sys
from PIL import Image
f=np.array(Image.open('front.png').convert('RGB')).astype(int)
logo=(f[:,:,0]>220)&(f[:,:,1]>220)&(f[:,:,2]>210)
logo[215:]=False
lb=np.full(1125,-1)
for x in range(1125):
    ys=np.where(logo[:,x])[0]
    if len(ys): lb[x]=ys.max()
t=Image.open('../../assets/tractor-motor-abierto-cutout.png').split()[3]
for W in [730,740,750,760]:
    sc=W/1671; L=1046-1668*sc; T=598-846*sc
    a=np.array(t.resize((round(1671*sc),round(846*sc))))>100
    gmin=999;at=None
    for x in range(a.shape[1]):
        X=int(round(L))+x
        ys=np.where(a[:,x])[0]
        if len(ys) and 0<=X<1125 and lb[X]>=0:
            g=T+ys.min()-lb[X]
            if g<gmin: gmin=g;at=X
    print(W, 'L',round(L,1),'T',round(T,1),'min vertical gap logo->tractor',round(gmin,1),'at x',at)
