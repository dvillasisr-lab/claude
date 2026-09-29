"""cards-press.pdf: each face on a 4.5 x 3 in sheet with crop marks and a slug carrying the print spec."""
import pymupdf, textwrap
src = pymupdf.open('cards.pdf')
out = pymupdf.open()
M = 27  # 0.375 in around the bleed
notes = src.metadata['subject']
for i in range(len(src)):
    pg = out.new_page(width=270 + 2 * M, height=162 + 2 * M + 34)
    pg.show_pdf_page(pymupdf.Rect(M, M, M + 270, M + 162), src, i)
    tx0, ty0, tx1, ty1 = M + 9, M + 9, M + 261, M + 153
    reg = (0, 0, 0, 1)
    for x in (tx0, tx1):
        pg.draw_line((x, 2), (x, M - 3), color=reg, width=0.25)
        pg.draw_line((x, M + 162 + 3), (x, M + 162 + M - 2), color=reg, width=0.25)
    for y in (ty0, ty1):
        pg.draw_line((2, y), (M - 3, y), color=reg, width=0.25)
        pg.draw_line((M + 270 + 3, y), (2 * M + 270 - 2, y), color=reg, width=0.25)
    face = 'FRONT' if i == 0 else 'BACK'
    txt = (f'HEAVY METAL card, {face}. ' + notes).replace('“', '"').replace('”', '"')
    r = pymupdf.Rect(M, 2 * M + 162 + 2, M + 270, 2 * M + 162 + 34)
    pg.insert_textbox(r, txt, fontsize=3.6, fontname='helv', color=(0, 0, 0, 1))
    pg.set_trimbox(pymupdf.Rect(tx0, ty0, tx1, ty1))
    pg.set_bleedbox(pymupdf.Rect(M, M, M + 270, M + 162))
out.set_metadata({'title': 'Heavy Metal business card, press sheet with crop marks', 'subject': notes})
out.save('cards-press.pdf')
print('ok', len(out))
