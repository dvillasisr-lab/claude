"""Tarjeta de presentación de Sussek Machine Company.

Las piezas dibujadas están tomadas de lo que Sussek fabrica (sussek.com):
una flecha con engrane helicoidal tallado y estrías (tallado CNC de 5 ejes,
temple por inducción) y una brida con barrenos.

Edita PERSONA y corre:  python3 generar.py
Sale tarjeta.html (frente + reverso, 89 x 51 mm + 3 mm de sangrado).
"""
import math
from pathlib import Path

PERSONA = {
    "nombre": "Full Name",
    "cargo": "Job Title",
    "tel": "920.478.2126",
    "email": "sales@sussek.com",
    "web": "sussek.com",
    "dir": "805 Pierce St · Waterloo, WI 53594",
}

S = 'stroke="currentColor" fill="none"'
CL = 'stroke-dasharray="2.6 .7 .45 .7"'   # línea de centro
HID = 'stroke-dasharray=".9 .5"'          # línea oculta
W, W2, W3 = .3, .17, .11                  # grosores: contorno, detalle, cota


def f(v):
    return f"{v:.3f}".rstrip("0").rstrip(".")


def arrow(x, y, ang, L=1.25, spread=.3):
    a1, a2 = ang + math.pi - spread, ang + math.pi + spread
    return (f'<path d="M{f(x)},{f(y)} L{f(x+L*math.cos(a1))},{f(y+L*math.sin(a1))} '
            f'L{f(x+L*math.cos(a2))},{f(y+L*math.sin(a2))}Z" fill="currentColor"/>')


def leader(x1, y1, x2, y2, x3, text, anchor="start"):
    ang = math.atan2(y1 - y2, x1 - x2)
    tx = (min(x2, x3) + .4) if anchor == "start" else (max(x2, x3) - .4)
    return (f'<path d="M{f(x1)},{f(y1)} L{f(x2)},{f(y2)} H{f(x3)}" {S} stroke-width="{W3}"/>'
            + arrow(x1, y1, ang)
            + f'<text x="{f(tx)}" y="{f(y2-.75)}" class="dim" text-anchor="{anchor}">{text}</text>')


def fcf(x, y, sym, tol, datum=None, h=3.2):
    """Marco de control geométrico (GD&T): símbolo | tolerancia | datum."""
    cells = [3.2, 2.2 + .95 * len(tol)] + ([3.0] if datum else [])
    out, cx = [], x
    for wdt in cells:
        out.append(f'<rect x="{f(cx)}" y="{f(y)}" width="{f(wdt)}" height="{h}" {S} stroke-width="{W3}"/>')
        cx += wdt
    mx, my = x + 1.6, y + h / 2
    if sym == "perp":
        out.append(f'<path d="M{f(mx-1)},{f(my+1)} H{f(mx+1)} M{f(mx)},{f(my+1)} V{f(my-1.05)}" {S} stroke-width="{W3}"/>')
    elif sym == "runout":
        out.append(f'<path d="M{f(mx-.9)},{f(my+.9)} L{f(mx+.8)},{f(my-.8)}" {S} stroke-width="{W3}"/>' + arrow(mx + .95, my - .95, -math.pi / 4, .9, .45))
    elif sym == "pos":
        out.append(f'<circle cx="{f(mx)}" cy="{f(my)}" r=".7" {S} stroke-width="{W3}"/><path d="M{f(mx-1.1)},{f(my)} H{f(mx+1.1)} M{f(mx)},{f(my-1.1)} V{f(my+1.1)}" {S} stroke-width="{W3}"/>')
    out.append(f'<text x="{f(x+3.2+1.1)}" y="{f(my+.55)}" class="dim">{tol}</text>')
    if datum:
        out.append(f'<text x="{f(x+cells[0]+cells[1]+1.5)}" y="{f(my+.55)}" class="dim" text-anchor="middle">{datum}</text>')
    return "".join(out)


def datum(x, y, letter, down=True):
    s = 1 if down else -1
    return (f'<path d="M{f(x-.9)},{f(y)} H{f(x+.9)} L{f(x)},{f(y+s*1.3)}Z" fill="currentColor"/>'
            f'<path d="M{f(x)},{f(y+s*1.3)} V{f(y+s*2.4)}" {S} stroke-width="{W3}"/>'
            f'<rect x="{f(x-1.4)}" y="{f(y+s*2.4 - (0 if down else 2.8))}" width="2.8" height="2.8" {S} stroke-width="{W3}"/>'
            f'<text x="{f(x)}" y="{f(y+s*2.4 + (2.0 if down else -.8))}" class="dim" text-anchor="middle">{letter}</text>')


def shaft(x0, yc):
    """Flecha: muñón, asiento de balero, engrane helicoidal tallado, hombro, estrías, ranura, muñón."""
    segs = [("end", 4.0, 2.6), ("brg", 7.5, 3.6), ("gear", 10.0, 8.4), ("sh", 2.6, 5.0),
            ("spl", 13.0, 4.5), ("grv", 1.2, 3.7), ("brg2", 26.0, 3.6)]
    out, x, pos = [], x0, {}
    top, bot = [], []
    for name, L, r in segs:
        pos[name] = (x, x + L, r)
        c = .5 if name in ("end", "gear") else 0
        top += [(x, yc - r + c), (x + c, yc - r), (x + L - c, yc - r), (x + L, yc - r + c)]
        bot += [(x, yc + r - c), (x + c, yc + r), (x + L - c, yc + r), (x + L, yc + r - c)]
        x += L
    pts = top + bot[::-1]
    out.append(f'<path d="M{" L".join(f"{f(a)},{f(b)}" for a, b in pts)}Z" {S} stroke-width="{W}"/>')
    for name, (a, b, r) in pos.items():   # líneas de cambio de sección
        out.append(f'<path d="M{f(a)},{f(yc-r)} V{f(yc+r)}" {S} stroke-width="{W2}"/>')
    ga, gb, gr = pos["gear"]               # dientes helicoidales
    out.append(f'<clipPath id="gclip"><rect x="{f(ga)}" y="{f(yc-gr+.5)}" width="{f(gb-ga)}" height="{f(2*gr-1)}"/></clipPath>')
    teeth = "".join(f"M{f(ga+i*1.25)},{f(yc-gr)} l{f(3.2)},{f(2*gr)} " for i in range(-4, 10))
    out.append(f'<path d="{teeth}" {S} stroke-width="{W3}" clip-path="url(#gclip)"/>')
    out.append(f'<path d="M{f(ga)},{f(yc-gr+1.3)} H{f(gb)} M{f(ga)},{f(yc+gr-1.3)} H{f(gb)}" {S} stroke-width="{W3}" {HID}/>')
    sa, sb, sr = pos["spl"]                # estrías
    spl = "".join(f"M{f(sa+.6)},{f(yc+k)} H{f(sb-.6)} " for k in (-3.1, -1.6, 0, 1.6, 3.1) if k)
    out.append(f'<path d="{spl}" {S} stroke-width="{W3}"/>')
    out.append(f'<path d="M{f(x0-3)},{yc} H{f(x+3)}" {S} stroke-width="{W3}" {CL}/>')
    return "".join(out), pos


def flange(cx, cy, R=10.5):
    """Brida en vista frontal: 4 barrenos pasados, maza, barreno central con cuñero."""
    out = [f'<circle cx="{cx}" cy="{cy}" r="{R}" {S} stroke-width="{W}"/>',
           f'<circle cx="{cx}" cy="{cy}" r="{f(R-.6)}" {S} stroke-width="{W3}"/>',
           f'<circle cx="{cx}" cy="{cy}" r="{f(R*.58)}" {S} stroke-width="{W2}"/>',
           f'<circle cx="{cx}" cy="{cy}" r="{f(R*.78)}" {S} stroke-width="{W3}" {CL}/>']
    for i in range(4):
        a = math.pi / 4 + i * math.pi / 2
        hx, hy = cx + R * .78 * math.cos(a), cy + R * .78 * math.sin(a)
        out.append(f'<circle cx="{f(hx)}" cy="{f(hy)}" r="1.05" {S} stroke-width="{W}"/>')
        out.append(f'<path d="M{f(hx-1.7)},{f(hy)} H{f(hx+1.7)} M{f(hx)},{f(hy-1.7)} V{f(hy+1.7)}" {S} stroke-width="{W3*.8}"/>')
    r, k, h = R * .34, .9, R * .34 + 1.1
    yk = cy - math.sqrt(r * r - k * k)
    out.append(f'<path d="M{f(cx-k)},{f(yk)} A{f(r)},{f(r)} 0 1 0 {f(cx+k)},{f(yk)} V{f(cy-h)} H{f(cx-k)}Z" {S} stroke-width="{W}"/>')
    e = R + 2.6
    out.append(f'<path d="M{f(cx-e)},{cy} H{f(cx+e)} M{cx},{f(cy-e)} V{f(cy+e)}" {S} stroke-width="{W3}" {CL}/>')
    return "".join(out)


def datum_left(x, y, letter):
    """Símbolo de datum apuntando a una superficie a su derecha."""
    return (f'<path d="M{f(x)},{f(y-.9)} V{f(y+.9)} L{f(x-1.3)},{f(y)}Z" fill="currentColor"/>'
            f'<path d="M{f(x-1.3)},{f(y)} H{f(x-2.4)}" {S} stroke-width="{W3}"/>'
            f'<rect x="{f(x-5.2)}" y="{f(y-1.4)}" width="2.8" height="2.8" {S} stroke-width="{W3}"/>'
            f'<text x="{f(x-3.8)}" y="{f(y+.55)}" class="dim" text-anchor="middle">{letter}</text>')


def front_art():
    """Flecha vertical que atraviesa la tarjeta, como sale de la talladora."""
    ax = 74.0                                  # eje de la flecha en la tarjeta
    body, p = shaft(-2, 0)
    Y = lambda x: x                            # coordenada a lo largo de la flecha -> y de la tarjeta
    out = [f'<g transform="translate({ax} 0) rotate(90)">{body}</g>']
    ga, gb, gr = p["gear"]
    sa, sb, sr = p["spl"]
    ba, bb, br = p["brg"]
    # engrane: diámetro y número de dientes
    out.append(leader(ax - gr - .1, Y(ga) + 3.2, ax - gr - 4, Y(ga) + .6, ax - gr - 19, "Ø16.800 -0.013", anchor="end"))
    out.append(f'<text x="{f(ax-gr-4.4)}" y="{f(Y(ga)+2.9)}" class="dim" text-anchor="end">HELICAL 28T</text>')
    # estrías: cabeceo con marco GD&T
    fy = Y(sa) + 3.4
    fx = 50.5
    out.append(fcf(fx, fy, "runout", "0.010", "A"))
    x_end = fx + 3.2 + 2.2 + .95 * 5 + 3.0
    out.append(f'<path d="M{f(x_end)},{f(fy+1.6)} H{f(ax-sr)}" {S} stroke-width="{W3}"/>' + arrow(ax - sr, fy + 1.6, 0))
    out.append(f'<text x="{f(fx)}" y="{f(fy+6.1)}" class="dim">SPLINE 24T · HRC 58</text>')
    # datum A en el asiento de balero
    out.append(datum_left(ax - br, Y(ba) + 4.2, "A"))
    return "".join(out)


def back_art():
    cx, cy, R = 75.5, 21, 10.5
    out = [flange(cx, cy, R)]
    a = math.radians(225)
    hx, hy = cx + R * .78 * math.cos(a), cy + R * .78 * math.sin(a)
    out.append(leader(hx - .75, hy - .75, hx - 3.6, 8.6, hx - 17.5, "4× Ø2.100 THRU", anchor="start"))
    out.append(fcf(cx - 8.2, cy + R + 3.2, "pos", "Ø0.02", "A"))
    return "".join(out)


CSS = """
  @page { size: 95mm 57mm; margin: 0; }
  :root{
    --navy:#202054; --navy-deep:#15153a; --line:#cdd5ee; --soft:#aab0d8; --ink:#1d1d22; --muted:#6b6f95;
    --steel:linear-gradient(90deg,#8e949b,#e9ecef 30%,#a9afb5 55%,#f4f6f7 75%,#8e949b);
    --bleed:3mm; --m:8.5mm;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  html,body{background:#d9dce1}
  body{font-family:"Open Sans",Helvetica,Arial,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  .card{width:95mm;height:57mm;position:relative;overflow:hidden;page-break-after:always;break-after:page}
  .draw{position:absolute;inset:0;width:95mm;height:57mm}
  .dim{font-family:"IBM Plex Mono",monospace;font-size:1.45px;letter-spacing:.03px;fill:currentColor}
  .abs{position:absolute}

  .lockup{display:flex;align-items:center;gap:3mm}
  .lockup img{height:12.5mm;width:auto;display:block}
  .word{font-family:"EB Garamond",Garamond,Georgia,serif;font-weight:500;font-size:4.6mm;line-height:1.02}
  .word span{display:block}
  .word span::first-letter{font-size:1.16em;font-weight:600}

  /* FRENTE */
  .front{background:radial-gradient(110% 130% at 72% 70%,#2a2a6e 0%,var(--navy) 42%,var(--navy-deep) 100%);color:#fff}
  .front .grid{position:absolute;inset:0;opacity:.07;background-image:linear-gradient(#fff .1mm,transparent .1mm),linear-gradient(90deg,#fff .1mm,transparent .1mm);background-size:3mm 3mm;background-position:.5mm .5mm}
  .front .draw{color:var(--line)}
  .front .lockup{left:var(--m);top:var(--m)}
  .front .pitch{left:var(--m);bottom:var(--m)}
  .pitch h2{font-family:"EB Garamond",Garamond,Georgia,serif;font-weight:500;font-size:5.6mm;line-height:1.02;letter-spacing:-.02mm}
  .pitch h2 em{font-style:italic;color:#fff}
  .pitch p{margin-bottom:2.2mm;font-size:1.6mm;font-weight:600;letter-spacing:.2mm;text-transform:uppercase;color:var(--soft);line-height:1.6}

  /* REVERSO */
  .back{background:#fff;color:var(--navy)}
  .back .draw{color:var(--navy)}
  .back .who{left:var(--m);top:var(--m)}
  .who h1{font-family:"EB Garamond",Garamond,Georgia,serif;font-weight:500;font-size:4.8mm;line-height:1.05}
  .who p{font-size:1.65mm;font-weight:700;letter-spacing:.24mm;text-transform:uppercase;margin-top:1.6mm;color:var(--muted)}
  .back .data{left:var(--m);top:22mm;display:grid;grid-template-columns:auto 1fr;align-items:baseline;column-gap:2.4mm;row-gap:.9mm;font-size:1.9mm;line-height:1.3;color:var(--ink)}
  .data dt{font-family:"IBM Plex Mono",monospace;font-weight:500;font-size:1.5mm;color:var(--navy)}
  .back .cta{left:var(--m);top:36.4mm;font-family:"EB Garamond",Garamond,Georgia,serif;font-style:italic;font-size:2.35mm;color:var(--navy)}
  .block{left:var(--m);right:var(--m);bottom:var(--m);height:6.6mm;display:grid;grid-template-columns:7.4mm 1fr 1.25fr 2.1fr 1fr;border:.25mm solid var(--navy)}
  .block>div{border-left:.16mm solid var(--navy);padding:.8mm 1.3mm 0;display:flex;flex-direction:column;justify-content:space-between;padding-bottom:.9mm}
  .block>div:first-child{border-left:0;align-items:center;justify-content:center;padding:0}
  .block img{height:4.6mm}
  .block small{font-family:"IBM Plex Mono",monospace;font-size:1.15mm;letter-spacing:.08mm;color:var(--muted);text-transform:uppercase}
  .block b{font-size:1.6mm;font-weight:700;letter-spacing:.12mm;color:var(--navy);white-space:nowrap}

  @media screen{
    body{display:flex;flex-wrap:wrap;gap:10mm;padding:12mm;justify-content:center}
    .card{box-shadow:0 2mm 6mm rgba(0,0,0,.22)}
  }
"""

FONTS = '<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,500&family=Open+Sans:wght@400;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">'
LOCKUP = '<div class="abs lockup"><img src="sussek-icono.png" alt=""><div class="word"><span>Sussek</span><span>Machine</span><span>Company</span></div></div>'


def build(p, frase):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Sussek Machine Company · Tarjeta</title>
{FONTS}
<style>{CSS}</style>
</head>
<body>
<!-- Nombre y cargo son de ejemplo; datos de la planta de Waterloo tomados de sussek.com -->

<section class="card front">
  <div class="grid"></div>
  <svg class="draw" viewBox="0 0 95 57">{front_art()}</svg>
  {LOCKUP}
  <div class="abs pitch">
    <p>Machined parts &amp; assemblies</p>
    <h2>{frase}</h2>
  </div>
</section>

<section class="card back">
  <svg class="draw" viewBox="0 0 95 57">{back_art()}</svg>
  <div class="abs who"><h1>{p["nombre"]}</h1><p>{p["cargo"]}</p></div>
  <dl class="abs data">
    <dt>T</dt><dd>{p["tel"]}</dd><dt>E</dt><dd>{p["email"]}</dd>
    <dt>W</dt><dd>{p["web"]}</dd><dt>A</dt><dd>{p["dir"]}</dd>
  </dl>
  <p class="abs cta">Request a quote at sussek.com</p>
  <div class="abs block">
    <div><img src="sussek-icono.png" alt=""></div>
    <div><small>Since</small><b>1960</b></div>
    <div><small>Capacity</small><b>250+ CNC</b></div>
    <div><small>Certified</small><b>ISO 9001 · IATF · AS9100</b></div>
    <div><small>Plants</small><b>US · MX · CN</b></div>
  </div>
</section>

</body>
</html>
"""


FRASES = {
    "tarjeta-1": "From print<br><em>to part.</em>",
    "tarjeta-2": "Precision<br><em>you can measure.</em>",
    "tarjeta-3": "Tight tolerances.<br><em>On time.</em>",
}

if __name__ == "__main__":
    for name, frase in FRASES.items():
        (Path(__file__).parent / f"{name}.html").write_text(build(PERSONA, frase))
        print("ok", name)
