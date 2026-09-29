import pymupdf, numpy as np
from PIL import Image
OUT='/home/user/claude/print/swarm/r-iconic/round2'
d=pymupdf.open(f'{OUT}/cards.pdf')
for p in d:
    p.set_bleedbox(p.mediabox); p.set_trimbox(pymupdf.Rect(9,9,261,153))
d.set_metadata({'title':'Heavy Metal business card, round 2','author':'Heavy Metal ProStock','subject':'3.5x2 in trim, 0.125 in bleed. Rich black C40 M30 Y30 K100; yellow #F5C400 = C0 M22 Y100 K2; silver type single K40 tint; bone = paper. 0.2 pt spread trap on yellow.','keywords':'TrimBox 9 9 261 153 pt; BleedBox = MediaBox'})
d.saveIncr() if False else d.save(f'{OUT}/work/cards_boxed.pdf')
d.close()
import shutil; shutil.move(f'{OUT}/work/cards_boxed.pdf', f'{OUT}/cards.pdf')
d=pymupdf.open(f'{OUT}/cards.pdf')
for i,(p,side) in enumerate(zip(d,['front','back'])):
    print(i, p.mediabox, p.trimbox, p.bleedbox)
    pix=p.get_pixmap(dpi=300); pix.save(f'{OUT}/work/pdf-{side}.png')
    a=np.array(Image.open(f'{OUT}/work/pdf-{side}.png').convert('RGB')).astype(int)
    b=np.array(Image.open(f'{OUT}/{side}.png').convert('RGB')).astype(int)
    print(side,'pdf size',a.shape, 'mean abs diff vs png', np.abs(a-b).mean().round(2), 'px diff>60:', (np.abs(a-b).max(2)>60).sum())
