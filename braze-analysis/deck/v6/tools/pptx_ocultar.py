"""Marca como ocultas en PowerPoint las láminas que html2pptx.js listó en <deck>.pptx.ocultas.json (atributo show="0")."""
import json, pathlib, re, shutil, sys, tempfile, zipfile

deck = pathlib.Path(sys.argv[1])
ocultas = json.loads(pathlib.Path(str(deck) + '.ocultas.json').read_text())
tmp = pathlib.Path(tempfile.mkdtemp())
with zipfile.ZipFile(deck) as z:
    z.extractall(tmp)
    names = z.namelist()
for n in ocultas:
    p = tmp / 'ppt' / 'slides' / f'slide{n}.xml'
    s = p.read_text(encoding='utf-8')
    if ' show="0"' not in s:
        s = re.sub(r'<p:sld ', '<p:sld show="0" ', s, count=1)
        p.write_text(s, encoding='utf-8')
out = deck.with_suffix('.tmp.pptx')
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for n in names:  # mismo orden; [Content_Types].xml primero
        z.write(tmp / n, n)
shutil.move(out, deck)
shutil.rmtree(tmp)
print('ocultas:', ocultas)
