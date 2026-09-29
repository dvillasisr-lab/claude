from PIL import Image; import numpy as np, json, sys, math
P=json.load(open('params.json'))
tw=P['TW']; th=tw*846/1671
al=Image.open('tractor-hero.png').split()[3].resize((round(tw*4),round(th*4)),Image.LANCZOS)
A=np.zeros((675*4,1125*4),np.float32)
x0,y0=round(P['TL']*4),round(P['TT']*4)
arr=np.array(al).astype(np.float32)/255
h,w=arr.shape; A[y0:y0+h,x0:x0+w]=arr[:min(h,2700-y0),:min(w,4500-x0)]
logo=np.array(Image.open('scan-front.png').convert('L'))>60
logo[230:]=False
ly,lx=np.where(logo)
def evaluate(cx,cy,r,sw=10,verbose=False):
    n=int(2*math.pi*r); th_=np.linspace(0,2*math.pi,n,endpoint=False)
    vis=np.zeros(n,bool)
    for d in np.linspace(-sw/2+.5,sw/2-.5,6):
        xs=(cx+(r+d)*np.cos(th_))*4; ys=(cy+(r+d)*np.sin(th_))*4
        xi=np.clip(xs.astype(int),0,4499); yi=np.clip(ys.astype(int),0,2699)
        vis|=A[yi,xi]<0.5
    # runs
    if vis.all(): runs=[(0,n)]
    else:
        k=np.argmin(vis); v=np.roll(vis,-k); runs=[]; i=0
        while i<n:
            if v[i]:
                j=i
                while j<n and v[j]: j+=1
                runs.append(((i+k)%n,j-i)); i=j
            else: i+=1
    # clearance to logo
    d=np.sqrt((lx-cx)**2+(ly-cy)**2)-r-sw/2; logo_clear=d.min()
    # visible point lowest y
    ys=cy+r*np.sin(th_); lowvis=ys[vis].max() if vis.any() else 0
    xs=cx+r*np.cos(th_)
    kick=min(np.hypot(np.clip(xs[vis],75,352.5)-xs[vis],np.clip(ys[vis],234.5,293.5)-ys[vis]).min()-sw/2, 999)
    title=(np.hypot(np.clip(xs[vis],75,265)-xs[vis],np.clip(ys[vis],305,522)-ys[vis]).min()-sw/2)
    frac=vis.mean(); minrun=min(l for s,l in runs)
    if verbose:
        for s,l in runs:
            t0=s/n*2*math.pi; t1=(s+l)/n*2*math.pi
            print(f'  run len {l}px from ({cx+r*math.cos(t0):.0f},{cy+r*math.sin(t0):.0f}) to ({cx+r*math.cos(t1):.0f},{cy+r*math.sin(t1):.0f})')
    return dict(logo=round(float(logo_clear),1),low=round(float(lowvis),1),kick=round(float(kick),1),title=round(float(title),1),frac=round(float(frac),3),minrun=minrun,nruns=len(runs))
if __name__=='__main__':
    if len(sys.argv)>1:
        cx,cy,r=map(float,sys.argv[1:4]); print(evaluate(cx,cy,r,verbose=True)); sys.exit()
    res=[]
    for r in range(160,215,5):
      for cx in range(560,760,10):
        for cy in range(360,470,5):
            e=evaluate(cx,cy,r)
            if e['logo']>=26 and e['low']<=578 and e['kick']>=40 and e['title']>=60 and e['minrun']>=60:
                res.append((r,cx,cy,e))
    res.sort(key=lambda t:(-t[0],-t[3]['frac']))
    for t in res[:40]: print(t)
    print(len(res))

from scipy import ndimage
def graze(cx,cy,r,sw=10):
    # distance (px) from each visible ring-edge sample to the tractor silhouette; report visible samples with 1<d<22 away from run ends
    sil=A[::4,::4]>=0.5
    dist=ndimage.distance_transform_edt(~sil)
    n=int(2*math.pi*r); t=np.linspace(0,2*math.pi,n,endpoint=False)
    out=[]
    for rr in (r-sw/2,r+sw/2):
        xs=np.clip((cx+rr*np.cos(t)).astype(int),0,1124); ys=np.clip((cy+rr*np.sin(t)).astype(int),0,674)
        d=dist[ys,xs]; out.append(d)
    d=np.minimum(*out)
    vis=d>0
    # samples near silhouette but visible, at least 20 px (arc) from any hidden sample
    hidden=~vis; idx=np.where(hidden)[0]
    near=[]
    for i in np.where((d>0)&(d<22))[0]:
        if len(idx)==0 or np.min(np.abs(((idx-i)+n//2)%n-n//2))>20: near.append(i)
    return len(near), [(int(cx+r*math.cos(t[i])),int(cy+r*math.sin(t[i])),round(float(d[i]),1)) for i in near[::10]]
