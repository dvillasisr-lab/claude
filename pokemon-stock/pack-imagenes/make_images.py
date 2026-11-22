#!/usr/bin/env python3
"""Genera las imagenes de venta del pack Black Bolt + White Flare (1080x1080).

Uso:
    python3 make_images.py          # escribe html/*.html
    node render.js                  # convierte html/*.html a out/*.png

Cambia PACK_PRICE (y los precios individuales) abajo y vuelve a correr los dos comandos.
Las fotos son imagenes de catalogo (ilustrativas); conviene agregar fotos reales del producto.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))

os.makedirs(os.path.join(HERE, "html"), exist_ok=True)
PACK_PRICE = 8600  # MXN, precio sugerido del pack completo (editable)
ITEMS = [  # nombre corto, set, imagen, precio individual de referencia (Collectr, MXN)
    ("Elite Trainer Box", "Black Bolt", "bb_etb.jpg", 2910),
    ("Booster Bundle", "Black Bolt", "bb_bundle.jpg", 1801),
    ("Elite Trainer Box", "White Flare", "wf_etb.jpg", 2608),
    ("Booster Bundle", "White Flare", "wf_bundle.jpg", 1729),
]
BLUE, PINK, INK, PAPER = "#1593C9", "#D6246E", "#12161C", "#F3F0E8"

total = sum(i[3] for i in ITEMS)
saving = total - PACK_PRICE
pct = round(100 * saving / total)
money = lambda n: f"${n:,.0f}"
color = lambda s: BLUE if s == "Black Bolt" else PINK

BASE = f"""
<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=1080">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1080px;height:1080px;background:{PAPER};font-family:'Inter','DejaVu Sans',sans-serif;color:{INK};-webkit-font-smoothing:antialiased}}
.slide{{width:1080px;height:1080px;padding:64px;position:relative;overflow:hidden;display:flex;flex-direction:column}}
.band{{position:absolute;left:0;top:0;width:1080px;height:14px;background:linear-gradient(90deg,{BLUE} 0 50%,{PINK} 50% 100%)}}
.pill{{display:inline-block;align-self:flex-start;font-weight:800;font-size:24px;letter-spacing:.12em;text-transform:uppercase;padding:12px 22px;border-radius:999px;background:{INK};color:#fff}}
h1{{font-size:96px;line-height:.98;font-weight:900;letter-spacing:-.03em;margin-top:28px}}
h1 .b{{color:{BLUE}}} h1 .p{{color:{PINK}}}
.sub{{font-size:34px;font-weight:600;margin-top:20px;color:#3b424c}}
.tile{{background:#fff;border-radius:22px;box-shadow:0 2px 0 rgba(0,0,0,.06),0 14px 30px rgba(18,22,28,.10);display:flex;align-items:center;justify-content:center;overflow:hidden;position:relative}}
.tile img{{max-width:88%;max-height:88%;object-fit:contain}}
.tag{{position:absolute;left:12px;bottom:12px;font-size:18px;font-weight:800;color:#fff;padding:5px 11px;border-radius:8px}}
.price{{margin-top:auto;display:flex;align-items:flex-end;justify-content:space-between;gap:24px}}
.label{{font-size:26px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#5a626d}}
.big{{font-size:132px;font-weight:900;letter-spacing:-.04em;line-height:1}}
.big small{{font-size:40px;font-weight:800;letter-spacing:0;margin-left:10px;color:#5a626d}}
.badge{{background:{INK};color:#fff;border-radius:22px;padding:18px 26px;text-align:center}}
.badge b{{display:block;font-size:50px;font-weight:900;line-height:1.05}}
.badge span{{font-size:22px;font-weight:700;letter-spacing:.06em;text-transform:uppercase}}
.foot{{font-size:20px;font-weight:500;color:#6b7280;margin-top:22px}}
</style></head><body>
"""


def page(name, body):
    with open(os.path.join(HERE, "html", f"{name}.html"), "w", encoding="utf-8") as f:
        f.write(BASE + body + "</body></html>")


def img(src):
    return f"../src/{src}"


# 1) Portada
tiles = "".join(
    f'<div class="tile" style="width:215px;height:270px"><img src="{img(i[2])}"><span class="tag" style="background:{color(i[1])}">{i[1]}</span></div>'
    for i in ITEMS
)
page("1-portada", f"""
<div class="slide"><div class="band"></div>
<span class="pill" style="margin-top:14px">Pack 4 en 1 &middot; Producto sellado</span>
<h1><span class="b">Black Bolt</span><br>+ <span class="p">White Flare</span></h1>
<div class="sub">2 Elite Trainer Box + 2 Booster Bundle</div>
<div style="display:flex;gap:24px;margin-top:34px">{tiles}</div>
<div class="price"><div><div class="label">Precio del pack</div><div class="big">{money(PACK_PRICE)}<small>MXN</small></div></div>
<div class="badge"><b>-{pct}%</b><span>vs. por separado</span></div></div>
<div class="foot">Fotos ilustrativas del producto.</div>
</div>""")

# 2) Que incluye + precios
rows = "".join(
    f'''<div style="display:flex;align-items:center;gap:22px;padding:14px 0;border-bottom:2px solid rgba(18,22,28,.10)">
<div class="tile" style="width:118px;height:118px;flex:none"><img src="{img(i[2])}"></div>
<div style="flex:1"><div style="font-size:38px;font-weight:800;line-height:1.1">{i[0]}</div>
<div style="display:inline-block;margin-top:8px;font-size:21px;font-weight:800;color:#fff;background:{color(i[1])};padding:4px 12px;border-radius:8px">{i[1]}</div></div>
<div style="font-size:42px;font-weight:800">{money(i[3])}</div></div>'''
    for i in ITEMS
)
page("2-incluye", f"""
<div class="slide"><div class="band"></div>
<span class="pill" style="margin-top:14px">Qu&eacute; incluye</span>
<h1 style="font-size:64px;margin-top:22px">Los 4 productos del pack</h1>
<div style="margin-top:14px">{rows}</div>
<div style="margin-top:auto;display:flex;align-items:center;justify-content:space-between;gap:20px">
<div><div class="label">Por separado</div><div style="font-size:48px;font-weight:800;text-decoration:line-through;text-decoration-thickness:4px;color:#6b7280">{money(total)}</div></div>
<div style="text-align:right"><div class="label">Pack completo</div><div class="big" style="font-size:104px">{money(PACK_PRICE)}</div></div></div>
<div class="foot">Ahorras {money(saving)} MXN. Precios por pieza de referencia (Collectr). Fotos ilustrativas.</div>
</div>""")

# 3) Que trae cada producto
def card(titulo, items, c, imgs):
    lis = "".join(f'<li style="margin-top:12px">{x}</li>' for x in items)
    pics = "".join(f'<div style="flex:1;height:230px;border-radius:16px;background:#fff;display:flex;align-items:center;justify-content:center;position:relative;box-shadow:inset 0 0 0 2px rgba(18,22,28,.08)"><img src="{img(a)}" style="max-width:86%;max-height:86%;object-fit:contain"><span class="tag" style="background:{color(sset)}">{sset}</span></div>' for a, sset in imgs)
    return f"""<div class="tile" style="flex:1;align-items:stretch;justify-content:flex-start;flex-direction:column;padding:34px 34px 34px;border-top:12px solid {c}">
<div style="font-size:30px;font-weight:900;letter-spacing:.04em;text-transform:uppercase;color:{c}">{titulo}</div>
<ul style="font-size:30px;font-weight:600;line-height:1.25;list-style:none;margin-top:10px">{lis}</ul>
<div style="margin-top:auto;display:flex;gap:14px">{pics}</div></div>"""


etb = card("Elite Trainer Box (x2)", ["Sobres de refuerzo", "Carta promo hologr&aacute;fica", "65 fundas para cartas", "45 cartas de energ&iacute;a", "Caja para guardar"], BLUE, [("bb_etb.jpg", "Black Bolt"), ("wf_etb.jpg", "White Flare")])
bun = card("Booster Bundle (x2)", ["6 sobres de refuerzo por bundle", "Producto sellado de f&aacute;brica", "Ideal para abrir o coleccionar"], PINK, [("bb_bundle.jpg", "Black Bolt"), ("wf_bundle.jpg", "White Flare")])
page("3-detalle", f"""
<div class="slide"><div class="band"></div>
<span class="pill" style="margin-top:14px">Detalle</span>
<h1 style="font-size:64px;margin-top:22px">Una de cada, de los dos sets</h1>
<div class="sub" style="font-size:30px">Un ETB y un Booster Bundle de cada set.</div>
<div style="display:flex;gap:28px;margin-top:34px;flex:1;margin-bottom:6px">{etb}{bun}</div>
<div class="foot">El contenido exacto puede variar por regi&oacute;n o versi&oacute;n del producto. Pregunta antes de comprar.</div>
</div>""")

# 4) Llamado a la accion
page("4-oferta", f"""
<div class="slide" style="background:{INK};color:#fff"><div class="band"></div>
<span class="pill" style="margin-top:14px;background:#fff;color:{INK}">Oferta pack</span>
<h1 style="font-size:84px;margin-top:30px"><span style="color:#5CC8F2">Black Bolt</span><br>+ <span style="color:#FF6FA6">White Flare</span></h1>
<div class="sub" style="color:#c9ced6">2 ETB + 2 Booster Bundle, todo sellado</div>
<div style="margin-top:46px"><div class="label" style="color:#9aa3af">Precio del pack</div>
<div class="big" style="font-size:190px;color:#fff">{money(PACK_PRICE)}<small style="color:#9aa3af">MXN</small></div></div>
<div style="margin-top:auto;display:flex;flex-direction:column;gap:14px;font-size:36px;font-weight:700">
<div>&#10003; Ahorras {money(saving)} MXN contra comprarlos por separado</div>
<div>&#10003; Se vende completo, los 4 juntos</div>
<div>&#10003; Aceptamos ofertas razonables</div></div>
<div style="margin-top:34px;background:#fff;color:{INK};border-radius:22px;padding:24px 30px;font-size:38px;font-weight:900;text-align:center">Escr&iacute;beme por WhatsApp para apartarlo</div>
</div>""")

print("ok", money(total), money(PACK_PRICE), f"-{pct}%")
