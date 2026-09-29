"""RGB Chromium PDF -> press CMYK PDF with the designer's exact builds.
- every vector/text colour is mapped from its sRGB value to a named CMYK build (unknown colours abort)
- the photo is converted sRGB -> GRACoL 2006 Coated (relative colorimetric + BPC), TAC limited to 300
- GRACoL output intent embedded, TrimBox/BleedBox set, print notes in Info/XMP and in a hidden note
- a second file cards-press.pdf adds crop marks and a visible slug with the notes."""
import pikepdf, zlib, io, datetime, numpy as np
from pikepdf import Name, Operator, Array, Dictionary, String
from PIL import Image, ImageCms
SRC, OUT = 'cards-rgb.pdf', 'cards.pdf'
ICC = '/usr/share/color/icc/colord/GRACoL_TR006_coated.icc'
BUILDS = {  # sRGB (as written by Chromium, 4 dp) -> (C, M, Y, K), name
    (0.0392, 0.0392, 0.0431): ((0.30, 0, 0, 1.00), 'ground C30 K100'),
    (0.9569, 0.9529, 0.9373): ((0, 0, 0, 0), 'bone = paper'),
    (0.9608, 0.7686, 0.0):    ((0, 0.22, 1.00, 0), 'yellow M22 Y100'),
    (0.2275, 0.2392, 0.2588): ((0.30, 0, 0, 0.75), 'rule C30 K75'),
    (0.0392, 0.0431, 0.0471): ((0, 0, 0, 1.00), 'QR K100'),
    (0.0863, 0.0902, 0.1020): ((0.30, 0, 0, 0.88), 'disc C30 K88'),
    (0.0, 0.0, 0.0):          ((0, 0, 0, 1.00), 'K100'),
}
NOTES = ('HEAVY METAL business card, “THE EVIL ONE”. Trim 3.5 x 2 in, bleed 0.125 in, safe 0.25 in. '
         'CMYK builds by the designer: ground C30 K100 (two-plate cool black so every knockout registers on 2 plates); '
         'rules and ruler ticks C30 K75 (same plates as the ground, cannot misregister); bone type and logo = paper (knockout); '
         'yellow M22 Y100, spread trap 0.1 mm; QR modules K100 only on a paper tile (29 modules, 140 px = 0.47 in, 0.41 mm per module, quiet zone 4.8+ modules); '
         'photo sRGB to GRACoL 2006 Coated, relative colorimetric + BPC, TAC 300 max, 300 ppi. '
         'Smallest type 6 pt Plex Mono Bold, paper white. Stock: 32 pt black-core triplex or 16 pt uncoated with soft-touch, corners die-cut 1/8 in radius. '
         'Hard proof on the chosen stock before the run.')
used = {}
def mapc(vals):
    key = tuple(round(float(v), 4) for v in vals)
    for k, (c, n) in BUILDS.items():
        if all(abs(a - b) < 0.003 for a, b in zip(k, key)):
            used[n] = used.get(n, 0) + 1
            return c
    raise SystemExit(f'unmapped colour {key}')
def fix_stream(owner, pdf):
    ins = pikepdf.parse_content_stream(owner)
    out = []
    for operands, op in ins:
        o = str(op)
        if o in ('rg', 'RG'):
            c = mapc(operands)
            out.append(([pikepdf.Object.parse(str(v).encode()) if False else v for v in c], Operator('k' if o == 'rg' else 'K')))
        elif o in ('cs', 'CS', 'sc', 'scn', 'SC', 'SCN', 'sh'):
            raise SystemExit(f'unexpected colour op {o}')
        else:
            out.append((operands, op))
    return pikepdf.unparse_content_stream(out)
srgb = ImageCms.createProfile('sRGB')
gracol = ImageCms.getOpenProfile(ICC)
xf = ImageCms.buildTransform(srgb, gracol, 'RGB', 'CMYK', renderingIntent=ImageCms.Intent.RELATIVE_COLORIMETRIC,
                             flags=ImageCms.Flags.BLACKPOINTCOMPENSATION)
def fix_image(x):
    im = pikepdf.PdfImage(x).as_pil_image().convert('RGB')
    c = np.array(ImageCms.applyTransform(im, xf)).astype(np.float32)
    tac = c.sum(-1); lim = 300 / 100 * 255
    over = tac > lim
    if over.any():  # pull CMY down proportionally, keep K
        k = c[..., 3]; cmy = c[..., :3]; s = cmy.sum(-1)
        f = np.where(over, np.clip((lim - k) / np.maximum(s, 1), 0, 1), 1)
        c[..., :3] = cmy * f[..., None]
    c = c.clip(0, 255).astype(np.uint8)
    x.write(zlib.compress(c.tobytes(), 9), filter=Name.FlateDecode)
    x.ColorSpace = Name.DeviceCMYK; x.BitsPerComponent = 8
    if '/DecodeParms' in x: del x['/DecodeParms']
    return round(float((c.astype(int).sum(-1)).max() / 255 * 100), 1)
pdf = pikepdf.open(SRC)
tacs = []
for pg in pdf.pages:
    conts = pg.Contents if isinstance(pg.Contents, pikepdf.Array) else [pg.Contents]
    data = b''.join(fix_stream(c, pdf) for c in conts)
    pg.Contents = pdf.make_stream(data)
    for k, x in pg.Resources.get('/XObject', {}).items():
        if x.Subtype == '/Image': tacs.append(fix_image(x))
        else: raise SystemExit('form xobject not expected')
    pg.TrimBox = Array([9, 9, 261, 153]); pg.BleedBox = Array([0, 0, 270, 162]); pg.MediaBox = Array([0, 0, 270, 162])
    if '/Group' in pg: pg.Group.CS = Name.DeviceCMYK
    # hidden (NoView) note with the spec, listed in the comments panel, never printed or drawn
    annot = pdf.make_indirect(Dictionary(Type=Name.Annot, Subtype=Name.Text, Rect=Array([0, 0, 9, 9]), F=32,
                                         Contents=String(NOTES), T=String('Print spec')))
    pg.Annots = Array([annot])
icc = pdf.make_stream(open(ICC, 'rb').read()); icc.N = 4
pdf.Root.OutputIntents = Array([Dictionary(Type=Name.OutputIntent, S=Name.GTS_PDFX, OutputConditionIdentifier=String('CGATS21_CRPC1'),
    OutputCondition=String('GRACoL 2006 Coated (TR006)'), RegistryName=String('http://www.color.org'), DestOutputProfile=icc)])
with pdf.open_metadata() as m:
    m['dc:title'] = 'Heavy Metal business card, “THE EVIL ONE” 1/1'
    m['dc:description'] = NOTES
    m['pdf:Keywords'] = 'CMYK; GRACoL 2006; trim 3.5x2 in; bleed 0.125 in'
pdf.docinfo['/Title'] = 'Heavy Metal business card, “THE EVIL ONE” 1/1'
pdf.docinfo['/Subject'] = NOTES
pdf.docinfo['/Keywords'] = 'CMYK; GRACoL 2006 Coated; ground C30 K100; rules C30 K75; yellow M22 Y100; QR K100; trim 3.5x2 in; bleed 0.125 in'
pdf.save(OUT)
print('colour builds used:', used)
print('image TAC max:', tacs)
