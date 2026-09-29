import numpy as np, json, re, cv2, pymupdf
from PIL import Image
OUT='/home/user/claude/print/swarm/r-iconic/round3'
for side in ['front','back']:
    a=np.array(Image.open(f'{OUT}/work/ink-{side}.png').convert('RGB')).astype(int)
    ink=np.abs(a-[11,11,12]).sum(2)>30
    out=ink.copy(); out[75:601,75:1051]=False
    ys,xs=np.nonzero(ink); print(side,'ink bbox',xs.min(),ys.min(),xs.max(),ys.max(),'outside safe:',out.sum())
# QR decode at several scales
im=cv2.imread(f'{OUT}/back.png'); det=cv2.QRCodeDetector()
for s in [1,.6,.33]:
    r=cv2.resize(im,None,fx=s,fy=s,interpolation=cv2.INTER_AREA); v,_,_=det.detectAndDecode(r); print('QR',s,repr(v))
html=open(f'{OUT}/cards.html').read()
body=re.sub(r'<[^>]+>',' ',re.sub(r'(?s)<(style|script|svg)[^>]*>.*?</\1>','',html.split('</head>')[1]))
print('dashes in copy:', [c for c in body if c in '–—'])
print('visible copy:', ' | '.join(t.strip() for t in body.split('  ') if t.strip()))
d=pymupdf.open(f'{OUT}/cards.pdf')
for i,p in enumerate(d):
    sizes=set()
    for b in p.get_text('dict')['blocks']:
        for l in b.get('lines',[]):
            for s in l['spans']: sizes.add((round(s['size'],2), s['font'], s['text'][:30]))
    print('page',i, sorted(sizes))
