#!/usr/bin/env python3
"""Turn Chromium's RGB cards.pdf into a CMYK press PDF (PDF/X-4 style):
- every vector/text colour mapped to its specified CMYK build (no default RGB->CMYK conversion)
- QR modules K100 overprint on the yellow disc
- rich-black keep-away: every knocked-out element gets a 0.3 pt K100-only rim, so a CMY plate shift
  shows black, never a coloured fringe
- yellow elements spread 0.1 pt into the black (overprint), so misregistration never opens a paper gap
- tractor raster converted to CMYK through FOGRA39 (perceptual)
- TrimBox/BleedBox, CMYK transparency group, FOGRA39 OutputIntent, GTS_PDFXVersion PDF/X-4
Also writes cards-press-cropmarks.pdf (crop marks + colour-spec slug)."""
import pymupdf, re, io, math, zlib, sys, numpy as np
from PIL import Image, ImageCms

SRC, OUT = 'cards-rgb.pdf', 'cards.pdf'
ICC = '/usr/share/color/icc/colord/FOGRA39L_coated.icc'
# sRGB (as Chromium writes it, 4 dp) -> (CMYK, role)
MAP = {
    (.0392, .0392, .0431): ((.40, .30, .30, 1), 'ground'),
    (.949, .9412, .9137): ((0, 0, 0, 0), 'knock'),       # bone = paper
    (.9608, .7686, 0): ((0, .22, 1, .02), 'yellow'),
    (.6627, .6784, .6941): ((0, 0, 0, .40), 'knock'),     # dim label grey, K only
    (.8039, .8157, .8275): ((0, 0, 0, .22), 'knock'),     # silver, K only
    (.2275, .2392, .2588): ((0, 0, 0, .80), 'knock'),     # rule, K only
    (.0392, .0392, .0471): ((0, 0, 0, 1), 'qr'),          # QR modules, K100 overprint
    (0, 0, 0): ((0, 0, 0, 1), 'image'),                   # colour state before image Do (unused)
}
HALO_PT = 0.25     # keep-away rim outside each knockout
SPREAD_PT = 0.10   # yellow spread into black
f = lambda v: ('%.4f' % v).rstrip('0').rstrip('.') or '0'
def key(r, g, b):
    for k in MAP:
        if max(abs(k[0]-r), abs(k[1]-g), abs(k[2]-b)) < .002: return k
    raise SystemExit('unmapped colour %s %s %s' % (r, g, b))

doc = pymupdf.open(SRC)
used = set()
for page in doc:
    res = doc.xref_object(page.xref)
    # ExtGState line widths
    gslw = {}
    for name, xr in re.findall(r'/(G\d+) (\d+) 0 R', res):
        m = re.search(r'/LW ([\d.]+)', doc.xref_object(int(xr)))
        if m: gslw[name] = float(m.group(1))
    xrefs = page.get_contents()
    src = b''.join(doc.xref_stream(x) for x in xrefs).decode('latin1')
    lines = src.split('\n')
    out = []
    st = [dict(scale=1.0, col=None, lw=1.0)]
    path = []; textblk = None
    def cur(): return st[-1]
    def cmyk(c, stroke=False):
        return '%s %s %s %s %s' % (*map(f, c), 'K' if stroke else 'k')
    def halo_ops(body, is_text, paint_w=None):
        g = cur(); c, role = MAP[g['col']]
        if role not in ('knock', 'yellow'): return []
        ops = []
        hw = HALO_PT / g['scale']; sw = SPREAD_PT / g['scale']
        base = paint_w if paint_w is not None else 0
        tr = ['1 Tr'] if is_text else []
        # 1. keep-away rim: K100 only, knockout
        A0, A1 = (['/Artifact << /Type /Layout >> BDC', '/Span << /ActualText <FEFF> >> BDC'], ['EMC', 'EMC']) if is_text else ([], [])
        ops += A0 + ['q', '0 0 0 1 K', '/GNOP gs', f(base + 2*hw) + ' w', '1 j', *tr, *body, *([] if is_text else ['S']), 'Q'] + A1
        # 2. yellow spread, overprint (C and K preserved)
        if role == 'yellow':
            ops += A0 + ['q', '0 .22 1 0 K', '/GOP gs', f(base + 2*sw) + ' w', '1 j', *tr, *body, *([] if is_text else ['S']), 'Q'] + A1
        return ops
    for ln in lines:
        t = ln.strip(); toks = t.split()
        if textblk is not None:
            textblk.append(ln)
            if t == 'ET':
                out += halo_ops(textblk, True) + textblk; textblk = None
            continue
        if t == 'q': st.append(dict(st[-1])); out.append(ln); continue
        if t == 'Q': st.pop(); out.append(ln); continue
        if t.endswith(' cm') and len(toks) == 7:
            a, b, c_, d = map(float, toks[:4]); cur()['scale'] *= math.sqrt(abs(a*d - b*c_)); out.append(ln); continue
        m = re.fullmatch(r'([\d.]+) ([\d.]+) ([\d.]+) RG ([\d.]+) ([\d.]+) ([\d.]+) rg', t)
        if m:
            k = key(*map(float, m.groups()[3:])); cur()['col'] = k; used.add(k)
            c, role = MAP[k]
            out.append(cmyk(c, True) + ' ' + cmyk(c) + (' /GOP gs' if role == 'qr' else ' /GNOP gs')); continue
        if re.search(r'\b(rg|RG|sc|scn|SC|SCN|cs|CS)$', t): raise SystemExit('unhandled colour op: ' + t)
        if t.endswith(' gs') and toks[0][1:] in gslw: cur()['lw'] = gslw[toks[0][1:]]
        if t.endswith(' w') and len(toks) == 2: cur()['lw'] = float(toks[0])
        if t == 'BT': textblk = [ln]; continue
        if toks and toks[-1] in ('m', 'l', 'c', 're', 'v', 'y') or t == 'h': path.append(ln); out.append(ln); continue
        if t in ('f', 'f*', 'S', 'B', 'B*') and path:
            body = list(path)
            # emit halo BEFORE the original path: remove the path we already emitted, re-add after
            del out[len(out)-len(path):]
            out += halo_ops(body, False, paint_w=cur()['lw'] if t == 'S' else None) + body + [ln]
            path = []; continue
        if t in ('n', 'W n', 'W* n') or t.endswith(' n'): path = []
        out.append(ln)
    new = '\n'.join(out).encode('latin1')
    doc.update_stream(xrefs[0], new)
    for x in xrefs[1:]: doc.update_stream(x, b'')
    # overprint ExtGStates
    gop = doc.get_new_xref(); doc.update_object(gop, '<< /Type /ExtGState /OP true /op true /OPM 1 >>')
    gno = doc.get_new_xref(); doc.update_object(gno, '<< /Type /ExtGState /OP false /op false /OPM 1 >>')
    eg = doc.xref_get_key(page.xref, 'Resources/ExtGState')
    for nm, xr in (('GOP', gop), ('GNOP', gno)):
        doc.xref_set_key(page.xref, 'Resources/ExtGState/' + nm, '%d 0 R' % xr)
    doc.xref_set_key(page.xref, 'Group', '<< /Type /Group /S /Transparency /CS /DeviceCMYK >>')
    page.set_trimbox(pymupdf.Rect(9, 9, 261, 153)); page.set_bleedbox(page.mediabox)

# images -> CMYK
srgb = ImageCms.createProfile('sRGB'); fogra = ImageCms.getOpenProfile(ICC)
tf = ImageCms.buildTransform(srgb, fogra, 'RGB', 'CMYK', renderingIntent=ImageCms.Intent.PERCEPTUAL)
done = set()
for page in doc:
    for im in page.get_images(full=True):
        xr = im[0]
        if xr in done: continue
        done.add(xr)
        pix = pymupdf.Pixmap(doc, xr)
        if pix.alpha: pix = pymupdf.Pixmap(pix, 0)
        if pix.n != 3: continue
        rgb = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
        cm = ImageCms.applyTransform(rgb, tf)
        doc.update_stream(xr, cm.tobytes(), compress=True)
        doc.xref_set_key(xr, 'ColorSpace', '/DeviceCMYK')
        doc.xref_set_key(xr, 'BitsPerComponent', '8')
        doc.xref_set_key(xr, 'DecodeParms', 'null')
        c = np.asarray(cm).astype(int)
        print('image', xr, pix.width, pix.height, '-> CMYK, max TAC %d%%' % (c.sum(-1).max() * 100 // 255))

# OutputIntent + PDF/X-4 identification
icc = open(ICC, 'rb').read()
ix = doc.get_new_xref(); doc.update_object(ix, '<< /N 4 >>'); doc.update_stream(ix, icc, compress=True)
oi = doc.get_new_xref()
OI = '<< /Type /OutputIntent /S /GTS_PDFX /OutputConditionIdentifier (FOGRA39) /OutputCondition (Coated FOGRA39, ISO 12647-2:2004) /RegistryName (http://www.color.org) /Info (Coated FOGRA39 \\(ISO 12647-2:2004\\)) /DestOutputProfile %d 0 R >>'
doc.update_object(oi, OI % ix)
cat = doc.pdf_catalog()
doc.xref_set_key(cat, 'OutputIntents', '[%d 0 R]' % oi)
doc.set_metadata({'title': 'Heavy Metal "The Evil One" business card', 'author': 'Heavy Metal ProStock', 'subject': '3.5 x 2 in, 0.125 in bleed, CMYK FOGRA39', 'creator': 'Chromium + post.py', 'producer': 'PyMuPDF'})
info = doc.xref_get_key(-1, 'Info')
if info[0] == 'xref':
    ixr = int(info[1].split()[0])
    doc.xref_set_key(ixr, 'GTS_PDFXVersion', '(PDF/X-4)'); doc.xref_set_key(ixr, 'Trapped', '/True')
doc.set_xml_metadata('''<?xpacket begin="﻿" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/"><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
<rdf:Description rdf:about="" xmlns:pdfxid="http://www.npes.org/pdfx/ns/id/" xmlns:pdf="http://ns.adobe.com/pdf/1.3/" xmlns:dc="http://purl.org/dc/elements/1.1/">
<pdfxid:GTS_PDFXVersion>PDF/X-4</pdfxid:GTS_PDFXVersion><pdf:Trapped>True</pdf:Trapped>
<dc:title><rdf:Alt><rdf:li xml:lang="x-default">Heavy Metal "The Evil One" business card</rdf:li></rdf:Alt></dc:title>
</rdf:Description></rdf:RDF></x:xmpmeta><?xpacket end="w"?>''')
doc.save(OUT, garbage=3, deflate=True)
print('used colours', len(used), 'of', len(MAP))

# press sheet with crop marks + slug
src = pymupdf.open(OUT); out = pymupdf.open(); M = 48
for i in range(len(src)):
    pg = out.new_page(width=270 + 2*M, height=162 + 2*M)
    pg.show_pdf_page(pymupdf.Rect(M, M, M+270, M+162), src, i)
    k = (0, 0, 0, 1)
    for x in (M+9, M+261):
        pg.draw_line((x, 0), (x, M-4), color=k, width=.25); pg.draw_line((x, M+166), (x, 2*M+162), color=k, width=.25)
    for y in (M+9, M+153):
        pg.draw_line((0, y), (M-4, y), color=k, width=.25); pg.draw_line((M+274, y), (2*M+270, y), color=k, width=.25)
    slug = ('HEAVY METAL "THE EVIL ONE" card %s. Trim 3.5 x 2 in, bleed 0.125 in. CMYK baked in file: ground C40 M30 Y30 K100 (TAC 200); '
            'yellow C0 M22 Y100 K2 with 0.1 pt overprint spread; labels K40, role K22, rules K80 (single plate); logo and name paper knockout; '
            'all knockouts carry a 0.25 pt K100-only keep-away; QR K100 overprint on yellow; photo FOGRA39. Hard proof required.') % ('FRONT' if i == 0 else 'BACK')
    pg.insert_textbox(pymupdf.Rect(M+14, M+168, M+256, 2*M+162), slug, fontsize=4, color=k)
    p2 = out[-1]; p2.set_trimbox(pymupdf.Rect(M+9, M+9, M+261, M+153)); p2.set_bleedbox(pymupdf.Rect(M, M, M+270, M+162))
ix2 = out.get_new_xref(); out.update_object(ix2, '<< /N 4 >>'); out.update_stream(ix2, icc, compress=True)
oi2 = out.get_new_xref(); out.update_object(oi2, OI % ix2)
out.xref_set_key(out.pdf_catalog(), 'OutputIntents', '[%d 0 R]' % oi2)
for pg in out: out.xref_set_key(pg.xref, 'Group', '<< /Type /Group /S /Transparency /CS /DeviceCMYK >>')
out.save('cards-press-cropmarks.pdf', garbage=3, deflate=True); print('press ok')
