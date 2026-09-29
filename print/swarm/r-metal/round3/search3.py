import ringsearch as R, math, numpy as np
res=[]
for r in range(150,176,2):
  for cx in range(550,640,4):
    for cy in range(370,420,3):
      e=R.evaluate(cx,cy,r)
      if not (e['logo']>=28 and e['kick']>=40 and e['title']>=60 and e['minrun']>=60 and e['low']<=575): continue
      g,_=R.graze(cx,cy,r)
      if g>12: continue
      # where does the top arc end on the right? find visible run containing top point
      n=int(2*math.pi*r); th=np.linspace(0,2*math.pi,n,endpoint=False)
      xs=cx+r*np.cos(th); ys=cy+r*np.sin(th)
      sil=R.A[::4,::4]>=0.5
      vis=~sil[np.clip(ys.astype(int),0,674),np.clip(xs.astype(int),0,1124)]
      i=int(n*0.75)  # top point (angle -90deg = 270deg)
      j=i
      while vis[j%n]: j+=1
      ex,ey=xs[j%n],ys[j%n]
      res.append((r,cx,cy,g,round(ex),round(ey),e['nruns'],e['frac']))
for t in sorted(res,key=lambda t:(-(735<=t[4]<=770),-t[0]))[:25]: print(t)
