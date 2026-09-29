import pymupdf, cv2, numpy as np
doc = pymupdf.open('cards.pdf')
print('pages', len(doc), [ (p.rect.width, p.rect.height) for p in doc])
for p in doc:
    p.set_trimbox(pymupdf.Rect(9, 9, 261, 153)); p.set_bleedbox(p.mediabox)
doc.save('cards_tmp.pdf'); doc.close()
import os; os.replace('cards_tmp.pdf', 'cards.pdf')
doc = pymupdf.open('cards.pdf')
mins = {}
for i, p in enumerate(doc):
    print('page', i+1, 'trim', p.trimbox, 'bleed', p.bleedbox)
    for b in p.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            for s in l['spans']:
                if s['text'].strip(): mins.setdefault(i, []).append((round(s['size'], 2), s['font'], s['text'][:24]))
    print(sorted(set(mins[i]))[:6])
    print('images', [(im[2], im[3]) for im in p.get_images()])
pix = doc[1].get_pixmap(dpi=600); pix.save('/tmp/claude-0/back600.png')
d = cv2.QRCodeDetector()
for f, sc in [('back.png', 1), ('back.png', .6), ('/tmp/claude-0/back600.png', .25)]:
    im = cv2.imread(f); im = cv2.resize(im, None, fx=sc, fy=sc, interpolation=cv2.INTER_AREA)
    print(f, sc, repr(d.detectAndDecode(im)[0]))
txt = ''.join(p.get_text() for p in doc)
print('dashes', [c for c in txt if c in '–—'])
# press version: crop marks + slug with colour spec
src = pymupdf.open('cards.pdf'); out = pymupdf.open()
M = 48
for i in range(len(src)):
    pg = out.new_page(width=270 + 2*M, height=162 + 2*M)
    pg.show_pdf_page(pymupdf.Rect(M, M, M+270, M+162), src, i)
    k = (0, 0, 0)
    for x in (M+9, M+261):
        pg.draw_line((x, 0), (x, M-4), color=k, width=.25); pg.draw_line((x, M+166), (x, 2*M+162), color=k, width=.25)
    for y in (M+9, M+153):
        pg.draw_line((0, y), (M-4, y), color=k, width=.25); pg.draw_line((M+274, y), (2*M+270, y), color=k, width=.25)
    slug = ('HEAVY METAL · "THE EVIL ONE" · card %s · 3.5 x 2 in trim, 0.125 in bleed · ground rich black C40 M30 Y30 K100 (TAC 200) · '
            'vinyl disc C30 M20 Y20 K92 · yellow #F5C400 = C0 M22 Y100 K2, spread 0.1 pt under black · small type K-only knockout · hard proof required') % ('FRONT' if i == 0 else 'BACK')
    pg.insert_textbox(pymupdf.Rect(M+14, M+168, M+256, 2*M+162), slug, fontsize=4, color=k)
    p2 = out[-1]; p2.set_trimbox(pymupdf.Rect(M+9, M+9, M+261, M+153)); p2.set_bleedbox(pymupdf.Rect(M, M, M+270, M+162))
out.save('cards-press-cropmarks.pdf'); print('press ok')
