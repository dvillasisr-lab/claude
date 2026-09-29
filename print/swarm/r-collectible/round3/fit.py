from PIL import Image; import numpy as np, sys
lg=np.array(Image.open('logo1000.png').convert('L'))>128
lb=np.array([ (np.where(lg[:,x])[0].max() if lg[:,x].any() else -999) for x in range(1000)])
ta=np.array(Image.open('/home/user/claude/print/swarm/assets/tractor-motor-abierto-cutout.png'))[:,:,3]>100
ttop=np.array([ (np.where(ta[:,x])[0].min() if ta[:,x].any() else 9999) for x in range(1671)])
def gap(s,L,G,x0,x1,y0):
  sc=(x1-x0)/1000.; T=G-844*s; g=999;at=None
  for X in range(int(L),int(L+1671*s)):
    ix=int((X-L)/s)
    if ix>=1671: continue
    lx=int((X-x0)/sc)
    if 0<=lx<1000 and lb[lx]>-999 and ttop[ix]<9999:
      d=T+ttop[ix]*s-(y0+lb[lx]*sc)
      if d<g: g=d;at=X
  return g,at
if __name__=='__main__':
  for x0,x1 in [(83,1042),(80,1045),(83,1000),(83,980),(125,1042),(100,1042)]:
    for s in [0.44,0.45,0.46,0.47]:
      best=None
      for R in range(1000,1036,2):
        L=R-1669*s; g,at=gap(s,L,598,x0,x1,x0)
        if best is None or g>best[0]: best=(round(g,1),at,R,round(L))
      print((x0,x1),s,round(1671*s),best)
