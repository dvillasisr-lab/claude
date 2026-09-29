#!/usr/bin/env python3
# Chromium RGB PDF -> press PDF: DeviceCMYK builds, K-only light pool, GRACoL image conversion, PDF/X-4 boxes + output intent.
import pikepdf, re, io, json, zlib
import numpy as np
from PIL import Image, ImageCms
from pikepdf import Name, Dictionary, Array, Stream
IN, OUT = 'cards-rgb.pdf', '../cards.pdf'
GRACOL = '/usr/share/color/icc/colord/GRACoL_TR006_coated.icc'
SRGB = '/usr/share/color/icc/colord/sRGB.icc'
V = json.load(open('params.json'))['vars']
CMYK = {  # exact builds
    '.0431 .0431 .0471': '.4 .3 .3 1',     # ground: rich black C40 M30 Y30 K100
    '.0392 .0431 .0471': '0 0 0 1',        # QR modules: K100 only
    '.6627 .6784 .6941': '.4 .3 .3 .4',    # silver: ground CMY, K40
    '.949 .9412 .9137': '0 0 0 0',         # bone: paper
    '.9608 .7686 0': '0 .22 1 .02',        # yellow #F5C400
    '0 0 0': '0 0 0 1',                    # fill state before the image Do (no ink)
}
pdf = pikepdf.open(IN)
def recolor(s):
    def rep(m):
        key = m.group(1); op = m.group(2)
        if key not in CMYK: raise SystemExit('unmapped colour ' + key)
        return CMYK[key] + (' k' if op == 'rg' else ' K')
    return re.sub(r'((?:-?[\d.]+ ){2}-?[\d.]+) (rg|RG)\b', rep, s)
for i, page in enumerate(pdf.pages):
    s = page.Contents.read_bytes().decode('latin1')
    s = recolor(s)
    if i == 0:
        # replace Chromium's RGB tiling pattern + soft mask with a K-only radial shading
        pat = re.search(r'/Pattern CS/Pattern cs/(P\d+) SCN/P\d+ scn\n0 0 1125 675 re\nf', s)
        assert pat, 'light pattern not found'
        lx, ly, lw, lh = float(V['LX']), float(V['LY']), float(V['LW']), float(V['LH'])
        k = lh / lw
        s = s.replace(pat.group(0), f'q 1 0 0 {k:.6f} 0 {ly*(1-k):.4f} cm /ShLight sh Q')
        del page.Resources.Pattern[Name('/' + pat.group(1))]
        if len(page.Resources.Pattern) == 0: del page.Resources[Name.Pattern]
        fn = Dictionary(FunctionType=2, Domain=[0, 1], C0=[.4, .3, .3, V.get('LK', .78)], C1=[.4, .3, .3, 1], N=1.6)
        sh = Dictionary(ShadingType=3, ColorSpace=Name.DeviceCMYK, Coords=[lx, ly, 0, lx, ly, lw], Function=fn, Extend=[True, True])
        page.Resources.Shading = Dictionary(ShLight=sh)
        # tractor image -> CMYK through GRACoL (relative colorimetric + BPC), keep its SMask
        for name, xo in page.Resources.XObject.items():
            if xo.get('/Subtype') != Name.Image: continue
            img = pikepdf.PdfImage(xo).as_pil_image().convert('RGB')
            tr = ImageCms.buildTransform(SRGB, GRACOL, 'RGB', 'CMYK', renderingIntent=1, flags=ImageCms.Flags.BLACKPOINTCOMPENSATION)
            cm = ImageCms.applyTransform(img, tr)
            xo.write(zlib.compress(cm.tobytes(), 9), filter=Name.FlateDecode)
            xo.ColorSpace = Name.DeviceCMYK; xo.BitsPerComponent = 8
            for kk in ('/DecodeParms',):
                if kk in xo: del xo[kk]
            print('image', name, img.size, '-> CMYK')
    page.Contents = pdf.make_stream(s.encode('latin1'))
    # any leftover RGB transparency groups -> CMYK
    for gs in page.Resources.get('/ExtGState', {}).values():
        pass
    page.obj.TrimBox = Array([9, 9, 261, 153]); page.obj.BleedBox = Array([0, 0, 270, 162]); page.obj.ArtBox = Array([9, 9, 261, 153])
    page.obj.Group = Dictionary(Type=Name.Group, S=Name.Transparency, CS=Name.DeviceCMYK)
# output intent + PDF/X-4 identification
icc = pdf.make_stream(open(GRACOL, 'rb').read()); icc.N = 4
pdf.Root.OutputIntents = Array([Dictionary(Type=Name.OutputIntent, S=Name.GTS_PDFX, OutputConditionIdentifier='CGATS TR 006',
    RegistryName='http://www.color.org', Info='GRACoL 2006 Coated #1 (CGATS TR 006)', DestOutputProfile=icc)])
with pdf.open_metadata(set_pikepdf_as_editor=False) as meta:
    meta['dc:title'] = 'Heavy Metal business card, round 3'
    meta['pdfxid:GTS_PDFXVersion'] = 'PDF/X-4'
    meta['pdf:Trapped'] = 'False'
pdf.docinfo[Name.Title] = 'Heavy Metal business card, round 3'
pdf.docinfo[Name.GTS_PDFXVersion] = 'PDF/X-4'
pdf.docinfo[Name.Trapped] = Name('/False')
pdf.docinfo[Name.Subject] = ('3.5 x 2 in trim, 0.125 in bleed. DeviceCMYK: ground C40 M30 Y30 K100; light pool K-only to K%d; '
    'silver C40 M30 Y30 K40; yellow C0 M22 Y100 K2 (or PMS 7408 C); bone = paper; QR K100 only. Image converted via GRACoL TR006.' % round(V.get('LK', .78)*100))
pdf.save(OUT, min_version='1.6')
print('saved', OUT)
