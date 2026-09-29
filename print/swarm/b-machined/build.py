import base64,re,pathlib
A=pathlib.Path('/home/user/claude/print/swarm/assets')
def b64(p,m): return f"data:{m};base64,"+base64.b64encode((A/p).read_bytes()).decode()
lin=(A/'logo-linea.svg').read_text(); api=(A/'logo-apilado.svg').read_text()
def inner(s): return s[s.index('>',s.index('<svg'))+1:s.rindex('</svg>')]
def chrome(s,grad): return inner(s).replace('fill="#F2F0E9"',f'fill="url(#{grad})"')
qr=(A/'qr-tienda.svg').read_text()
t=pathlib.Path('template.html').read_text()
rep={'{{TRACTOR}}':b64('tractor-motor-abierto-cutout.png','image/png'),
 '{{EMBLEM}}':b64('emblema-v8-3208-mask.png','image/png'),
 '{{LOGO_LINE}}':chrome(lin,'chromeL'),'{{LOGO_LINE_S}}':chrome(lin,'chromeS'),
 '{{LOGO_STACK}}':chrome(api,'chromeL'),
 '{{QR}}':inner(qr),
 '{{FONTS}}':'/root/.claude/skills/synced/9983f56a-2d7a-4333-8a10-0941713cc597_0d8f03d3-28eb-42fc-935b-5b47bbd87cf0/canvas-design/canvas-fonts'}
for k,v in rep.items(): t=t.replace(k,v)
pathlib.Path('cards.html').write_text(t)
print('ok',len(t))
