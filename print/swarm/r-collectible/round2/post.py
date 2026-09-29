import pymupdf, cv2, numpy as np
d = pymupdf.open('cards.pdf')
print('pages', len(d), [tuple(round(v,2) for v in pg.rect) for pg in d])
for pg in d:
    pg.set_bleedbox(pg.rect)
    pg.set_trimbox(pymupdf.Rect(9, 9, 261, 153))
d.set_metadata({'title': 'Heavy Metal business card, “THE EVIL ONE”', 'subject': 'Trim 3.5x2 in, bleed 0.125 in. Rich black C60 M40 Y40 K100; window K88; yellow #F5C400 = C0 M22 Y100 K2.', 'author': 'Heavy Metal ProStock'})
d.saveIncr() if False else None
d.save('cards_tmp.pdf'); d.close()
import os; os.replace('cards_tmp.pdf', 'cards.pdf')
d = pymupdf.open('cards.pdf')
mins = []
for i, pg in enumerate(d):
    print('page', i+1, 'trim', pg.trimbox, 'bleed', pg.bleedbox)
    for b in pg.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            for s in l['spans']:
                mins.append((round(s['size'],2), s['text'][:40], s['font']))
for m in sorted(set(mins))[:12]: print(m)
# press proof with crop marks: 4.25 x 2.75 in page, card centered, 0.25 in marks
src = pymupdf.open('cards.pdf'); out = pymupdf.open()
M = 18  # 0.25 in margin beyond bleed
for i in range(len(src)):
    pg = out.new_page(width=270 + 2*M, height=162 + 2*M)
    pg.show_pdf_page(pymupdf.Rect(M, M, M+270, M+162), src, i)
    tx0, ty0, tx1, ty1 = M+9, M+9, M+261, M+153
    for x in (tx0, tx1):
        for (a, b) in ((0, M-2), (M+162+2, 162+2*M)):
            pg.draw_line((x, a), (x, b), color=(0, 0, 0), width=0.25)
    for y in (ty0, ty1):
        for (a, b) in ((0, M-2), (M+270+2, 270+2*M)):
            pg.draw_line((a, y), (b, y), color=(0, 0, 0), width=0.25)
    pg.set_trimbox(pymupdf.Rect(tx0, ty0, tx1, ty1))
    pg.set_bleedbox(pymupdf.Rect(M, M, M+270, M+162))
out.save('cards-press-cropmarks.pdf')
# QR decode at 100%, 60%, 40%
im = cv2.imread('back.png')
det = cv2.QRCodeDetector()
for s in (1.0, 0.6, 0.4):
    r = cv2.resize(im, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
    val, pts, _ = det.detectAndDecode(r)
    print('QR', s, repr(val))
