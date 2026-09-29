from PIL import Image; import numpy as np
for f in ['front','back']:
    a=np.array(Image.open(f'scan-{f}.png').convert('RGB')).astype(int)
    ink=(np.abs(a-[10,10,11]).sum(-1)>40)
    ys,xs=np.where(ink); print(f,'ink bbox',xs.min(),xs.max(),ys.min(),ys.max())
    yel=(a[...,0]>200)&(a[...,1]>150)&(a[...,2]<80)
    ys,xs=np.where(yel); print(f,'yellow bbox',xs.min(),xs.max(),ys.min(),ys.max())
