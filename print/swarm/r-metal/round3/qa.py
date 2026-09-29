import pymupdf, cv2, numpy as np, json
from PIL import Image
P=json.load(open('params.json'))
d=pymupdf.open('cards.pdf')
print('pages',len(d),[(p.rect.width/72,p.rect.height/72) for p in d])
for i,p in enumerate(d):
    sp=[]
    for b in p.get_text('dict')['blocks']:
        for l in b.get('lines',[]):
            for s in l['spans']:
                if s['text'].strip(): sp.append((round(s['size'],2),s['font'].split('+')[-1],s['text'][:26]))
    print('page',i+1,'min span',min(sp)[:2],'| sizes',sorted(set((x[0],x[1]) for x in sp)))
    for im in p.get_images(full=True):
        r=p.get_image_rects(im[0])[0]; print('  image',im[5],'ppi %.0f'%(im[2]/(r.width/72)))
txt=''.join(p.get_text() for p in d); print('dashes',[c for c in txt if c in '–—'], 'quotes', txt.count('“'), txt.count('”'))
det=cv2.QRCodeDetector()
for sc in (1,.8,.6):
    im=cv2.imread('back.png'); im=cv2.resize(im,None,fx=sc,fy=sc,interpolation=cv2.INTER_AREA); print('qr png',sc,repr(det.detectAndDecode(im)[0]))
pix=d[1].get_pixmap(dpi=600); pix.save('/tmp/claude-0/b600.png'); im=cv2.imread('/tmp/claude-0/b600.png')
for sc in (.5,.25): print('qr pdf600',sc,repr(det.detectAndDecode(cv2.resize(im,None,fx=sc,fy=sc,interpolation=cv2.INTER_AREA))[0]))
for f in ['front','back']:
    a=np.array(Image.open(f'scan-{f}.png').convert('RGB')).astype(int); ink=(np.abs(a-[10,10,11]).sum(-1)>40)
    ys,xs=np.where(ink); print(f,'text/logo/QR ink bbox x',xs.min(),xs.max(),'y',ys.min(),ys.max(), 'SAFE' if xs.min()>=75 and xs.max()<=1050 and ys.min()>=75 and ys.max()<=600 else 'OUT')
tw=P['TW']; s=tw/1671
print('tractor right %.1f  front tyre contact %.1f  rear tyre bottom %.1f  hitch %.1f  stack top %.1f'%(P['TL']+1668*s,P['TT']+841*s,P['TT']+752*s,P['TL']+7*s,P['TT']))
