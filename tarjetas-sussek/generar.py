"""Tarjeta de presentación de Sussek Machine Company.

Las piezas dibujadas están tomadas de lo que Sussek fabrica (sussek.com):
una flecha con engrane helicoidal tallado y estrías (tallado CNC de 5 ejes,
temple por inducción) y una brida con barrenos.

Edita PERSONA y corre:  python3 generar.py
Salen 3 diseños distintos, cada uno como diseno-N.html (frente + reverso,
89 x 51 mm + 3 mm de sangrado).
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


def gear_geom(R, N=22, alpha=20):
    """Geometría de un engrane recto con diente de evolvente (medidas en mm)."""
    m = 2 * R / (N + 2)                  # módulo
    rp = m * N / 2                       # radio primitivo
    rb = rp * math.cos(math.radians(alpha))
    rf = rp - 1.25 * m
    s = R / 21                           # escala para maza y barrenos
    return dict(m=m, rp=rp, rb=rb, rf=rf, ra=R, N=N, bc=9.2 * s, hole=1.35 * s, hub=13.2 * s, s=s)


def gear(cx, cy, R, N=22, w=.3):
    """Engrane en vista frontal: dientes de evolvente, círculo primitivo, maza, barrenos y cuñero."""
    g = gear_geom(R, N)
    rb, rf, ra, rp = g["rb"], g["rf"], g["ra"], g["rp"]
    inv = lambda a: math.tan(a) - a
    al = math.radians(20)
    half = math.pi / (2 * N) + inv(al)   # medio ancho angular del diente en el círculo base
    flank = []                           # (radio, ángulo relativo) de un flanco, de la raíz a la punta
    flank.append((rf, half))
    steps = 8
    r0 = max(rb, rf)
    for i in range(steps + 1):
        r = r0 + (ra - r0) * i / steps
        flank.append((r, half - inv(math.acos(min(1, rb / r)))))
    pts = []
    for k in range(N):
        c = 2 * math.pi * k / N
        for r, t in flank:                              # flanco izquierdo, subiendo
            pts.append((r, c - t))
        for r, t in reversed(flank):                    # flanco derecho, bajando
            pts.append((r, c + t))
        # raíz hasta el siguiente diente
        a1, a2 = c + half, c + 2 * math.pi / N - half
        for j in range(1, 4):
            pts.append((rf, a1 + (a2 - a1) * j / 4))
    d = "M" + " L".join(f"{f(cx + r * math.cos(t))},{f(cy + r * math.sin(t))}" for r, t in pts) + "Z"
    sc = g["s"]
    out = [f'<path d="{d}" {S} stroke-width="{w}" stroke-linejoin="round"/>',
           f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(rp)}" {S} stroke-width="{f(w*.45)}" {CL}/>',
           f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(g["hub"])}" {S} stroke-width="{f(w*.8)}"/>',
           f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(g["bc"])}" {S} stroke-width="{f(w*.45)}" {CL}/>']
    for i in range(6):
        t = math.pi / 6 + i * math.pi / 3
        out.append(f'<circle cx="{f(cx+g["bc"]*math.cos(t))}" cy="{f(cy+g["bc"]*math.sin(t))}" r="{f(g["hole"])}" {S} stroke-width="{f(w*.8)}"/>')
    r, k, h = 4.6 * sc, 1.1 * sc, 5.6 * sc
    yk = cy - math.sqrt(r * r - k * k)
    out.append(f'<path d="M{f(cx-k)},{f(yk)} A{f(r)},{f(r)} 0 1 0 {f(cx+k)},{f(yk)} V{f(cy-h)} H{f(cx-k)}Z" {S} stroke-width="{w}"/>')
    e = R + 3.5 * sc
    out.append(f'<path d="M{f(cx-e)},{f(cy)} H{f(cx+e)} M{f(cx)},{f(cy-e)} V{f(cy+e)}" {S} stroke-width="{f(w*.4)}" {CL}/>')
    return "".join(out)


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



def dim_h(x1, x2, y, text, ext_from=None):
    """Cota horizontal con líneas de extensión y texto al centro."""
    out = []
    if ext_from is not None:
        out.append(f'<path d="M{f(x1)},{f(ext_from)} V{f(y-1)} M{f(x2)},{f(ext_from)} V{f(y-1)}" {S} stroke-width="{W3}"/>')
    mid, gap = (x1 + x2) / 2, .52 * len(text) + .8
    out.append(f'<path d="M{f(x1)},{f(y)} H{f(mid-gap)} M{f(mid+gap)},{f(y)} H{f(x2)}" {S} stroke-width="{W3}"/>')
    out.append(arrow(x1, y, math.pi) + arrow(x2, y, 0))
    out.append(f'<text x="{f(mid)}" y="{f(y+.5)}" class="dim" text-anchor="middle">{text}</text>')
    return "".join(out)


def dim_v(x, y1, y2, text, ext_from=None):
    out = []
    if ext_from is not None:
        out.append(f'<path d="M{f(ext_from)},{f(y1)} H{f(x+1)} M{f(ext_from)},{f(y2)} H{f(x+1)}" {S} stroke-width="{W3}"/>')
    mid = (y1 + y2) / 2
    out.append(f'<path d="M{f(x)},{f(y1)} V{f(y2)}" {S} stroke-width="{W3}"/>')
    out.append(arrow(x, y1, -math.pi / 2) + arrow(x, y2, math.pi / 2))
    out.append(f'<text x="{f(x-1)}" y="{f(mid+.5)}" class="dim" text-anchor="end">{text}</text>')
    return "".join(out)


BASE_CSS = """
  @page { size: 95mm 57mm; margin: 0; }
  :root{
    --navy:#202054; --navy-deep:#15153a; --line:#cdd5ee; --soft:#aab0d8; --ink:#1d1d22; --muted:#6b6f95; --glow:#f39a2b;
    --steel:linear-gradient(90deg,#8e949b,#e9ecef 30%,#a9afb5 55%,#f4f6f7 75%,#8e949b);
    --m:8.5mm; --paper:#f5f3ee;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  html,body{background:#d9dce1}
  body{font-family:"Open Sans",Helvetica,Arial,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  .card{width:95mm;height:57mm;position:relative;overflow:hidden;page-break-after:always;break-after:page}
  .draw{position:absolute;inset:0;width:95mm;height:57mm}
  .dim{font-family:"IBM Plex Mono",monospace;font-size:1.45px;letter-spacing:.03px;fill:currentColor}
  .abs{position:absolute}
  .serif{font-family:"EB Garamond",Garamond,Georgia,serif}

  .lockup{display:flex;align-items:center;gap:3mm}
  .lockup img{height:12.5mm;width:auto;display:block}
  .word{font-family:"EB Garamond",Garamond,Georgia,serif;font-weight:500;font-size:4.6mm;line-height:1.02}
  .word span{display:block}
  .word span::first-letter{font-size:1.16em;font-weight:600}

  .who h1{font-family:"EB Garamond",Garamond,Georgia,serif;font-weight:500;font-size:4.8mm;line-height:1.05}
  .who p{font-size:1.65mm;font-weight:700;letter-spacing:.24mm;text-transform:uppercase;margin-top:1.6mm}
  .data{display:grid;grid-template-columns:auto 1fr;align-items:baseline;column-gap:2.4mm;row-gap:.9mm;font-size:1.9mm;line-height:1.3}
  .data dt{font-family:"IBM Plex Mono",monospace;font-weight:500;font-size:1.5mm}
  .eyebrow{font-size:1.6mm;font-weight:700;letter-spacing:.2mm;text-transform:uppercase}

  @media screen{
    body{display:flex;flex-wrap:wrap;gap:10mm;padding:12mm;justify-content:center}
    .card{box-shadow:0 2mm 6mm rgba(0,0,0,.22)}
  }
"""

FONTS = '<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,500&family=Open+Sans:wght@400;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=Archivo:wdth,wght@62..125,500..900&display=swap" rel="stylesheet">'
WORD = '<div class="word"><span>Sussek</span><span>Machine</span><span>Company</span></div>'
LOCKUP = f'<div class="lockup"><img src="sussek-icono.png" alt="">{WORD}</div>'


def data_html(p):
    return (f'<dt>T</dt><dd>{p["tel"]}</dd><dt>E</dt><dd>{p["email"]}</dd>'
            f'<dt>W</dt><dd>{p["web"]}</dd><dt>A</dt><dd>{p["dir"]}</dd>')


# ---------- Diseño 1: PLANO (azul, flecha vertical, cuadro de rótulo) ----------

def diseno_1(p):
    css = """
  .d1.front{background:radial-gradient(110% 130% at 72% 70%,#2a2a6e 0%,var(--navy) 42%,var(--navy-deep) 100%);color:#fff}
  .d1.front .grid{position:absolute;inset:0;opacity:.07;background-image:linear-gradient(#fff .1mm,transparent .1mm),linear-gradient(90deg,#fff .1mm,transparent .1mm);background-size:3mm 3mm;background-position:.5mm .5mm}
  .d1.front .draw{color:var(--line)}
  .d1.front .lockup{left:var(--m);top:var(--m)}
  .d1.front .pitch{left:var(--m);bottom:var(--m)}
  .d1 .pitch h2{font-family:"EB Garamond",Garamond,Georgia,serif;font-weight:500;font-size:5.6mm;line-height:1.02}
  .d1 .pitch .eyebrow{margin-bottom:2.2mm;color:var(--soft)}
  .d1.back{background:#fff;color:var(--navy)}
  .d1.back .draw{color:var(--navy)}
  .d1.back .who{left:var(--m);top:var(--m)}
  .d1.back .who p{color:var(--muted)}
  .d1.back .data{left:var(--m);top:22mm;color:var(--ink)}
  .d1.back .data dt{color:var(--navy)}
  .d1.back .cta{left:var(--m);top:36.4mm;font-style:italic;font-size:2.35mm}
  .d1 .block{left:var(--m);right:var(--m);bottom:var(--m);height:6.6mm;display:grid;grid-template-columns:7.4mm 1fr 1.25fr 2.1fr 1fr;border:.25mm solid var(--navy)}
  .d1 .block>div{border-left:.16mm solid var(--navy);padding:.8mm 1.3mm .9mm;display:flex;flex-direction:column;justify-content:space-between}
  .d1 .block>div:first-child{border-left:0;align-items:center;justify-content:center;padding:0}
  .d1 .block img{height:4.6mm}
  .d1 .block small{font-family:"IBM Plex Mono",monospace;font-size:1.15mm;letter-spacing:.08mm;color:var(--muted);text-transform:uppercase}
  .d1 .block b{font-size:1.6mm;font-weight:700;letter-spacing:.12mm;white-space:nowrap}
"""
    html = f"""
<section class="card front d1">
  <div class="grid"></div>
  <svg class="draw" viewBox="0 0 95 57">{front_art()}</svg>
  <div class="abs lockup-wrap" style="left:8.5mm;top:8.5mm">{LOCKUP}</div>
  <div class="abs pitch"><p class="eyebrow">Machined parts &amp; assemblies</p><h2>From print<br><em>to part.</em></h2></div>
</section>
<section class="card back d1">
  <svg class="draw" viewBox="0 0 95 57">{back_art()}</svg>
  <div class="abs who"><h1>{p["nombre"]}</h1><p>{p["cargo"]}</p></div>
  <dl class="abs data">{data_html(p)}</dl>
  <p class="abs cta serif">Request a quote at sussek.com</p>
  <div class="abs block">
    <div><img src="sussek-icono.png" alt=""></div>
    <div><small>Since</small><b>1960</b></div>
    <div><small>Capacity</small><b>250+ CNC</b></div>
    <div><small>Certified</small><b>ISO 9001 · IATF · AS9100</b></div>
    <div><small>Plants</small><b>US · MX · CN</b></div>
  </div>
</section>"""
    return css, html


# ---------- Diseño 2: FOTO (temple por inducción de su planta, duotono azul) ----------

def diseno_2(p):
    css = """
  .d2.front{background:#101030 url(foto-temple.jpg) center/cover no-repeat;color:#fff}
  .d2.front .shade{position:absolute;inset:0;background:
      linear-gradient(90deg,rgba(16,16,48,.92) 0%,rgba(16,16,48,.7) 38%,rgba(16,16,48,0) 70%),
      linear-gradient(0deg,rgba(16,16,48,.75) 0%,rgba(16,16,48,0) 45%)}
  .d2.front .lockup-wrap{left:var(--m);top:var(--m)}
  .d2.front .pitch{left:var(--m);bottom:var(--m)}
  .d2 .pitch h2{font-family:"EB Garamond",Garamond,Georgia,serif;font-weight:500;font-size:5.4mm;line-height:1.04}
  .d2 .pitch em{color:#ffc27a}
  .d2 .pitch .eyebrow{margin-bottom:2.2mm;color:#d7dbf0}
  .d2 .pitch .eyebrow b{color:var(--glow)}
  .d2.back{background:#fff;color:var(--navy)}
  .d2.back .lockup-wrap{left:var(--m);top:var(--m)}
  .d2.back .lockup img{height:10.5mm}
  .d2.back .word{font-size:3.9mm;color:var(--navy)}
  .d2.back .who{right:var(--m);top:var(--m);text-align:right}
  .d2.back .who p{color:var(--muted)}
  .d2.back .rule{left:var(--m);right:var(--m);top:25.5mm;height:.5mm;background:linear-gradient(90deg,var(--glow) 0 12mm,#e3e5ee 12mm)}
  .d2.back .data{left:var(--m);top:29.5mm;color:var(--ink)}
  .d2.back .data dt{color:var(--glow)}
  .d2.back .caps{right:var(--m);bottom:var(--m);text-align:right;font-size:1.5mm;font-weight:700;letter-spacing:.18mm;text-transform:uppercase;line-height:1.9;color:var(--navy)}
  .d2.back .caps span{color:var(--muted);font-weight:600}
"""
    html = f"""
<section class="card front d2">
  <div class="shade"></div>
  <div class="abs lockup-wrap">{LOCKUP}</div>
  <div class="abs pitch"><p class="eyebrow">Machining · Hobbing · <b>Heat treat</b></p><h2>Tight tolerances.<br><em>On time.</em></h2></div>
</section>
<section class="card back d2">
  <div class="abs lockup-wrap">{LOCKUP}</div>
  <div class="abs who"><h1>{p["nombre"]}</h1><p>{p["cargo"]}</p></div>
  <i class="abs rule"></i>
  <dl class="abs data">{data_html(p)}</dl>
  <p class="abs caps">Since 1960 · 250+ CNC<br><span>ISO 9001 · IATF 16949 · AS9100</span><br>US · MX · CN</p>
</section>"""
    return css, html


# ---------- Diseño 3: BLANCO (el logo acotado como si fuera una pieza) ----------

def diseno_3_front():
    # lockup centrado: ícono 16 mm de alto; medidas en mm de la tarjeta
    ix1, ix2, iy1, iy2 = 22.5, 40.5, 15.5, 31.5          # caja del ícono
    wx2 = 72.5                                          # fin del nombre
    out = [dim_h(ix1, wx2, 10.2, "50.000 ±0.005", ext_from=iy1 - 1.2),
           dim_v(ix1 - 3.2, iy1, iy2, "16.000", ext_from=ix1 - 1),
           leader(ix1 + .7, iy2 - .7, ix1 + 3.2, 36, ix1 + 15, "R2.5 TYP")]
    out.append(f'<path d="M{f((ix1+ix2)/2)},{f(iy1-2.5)} V{f(iy2+2.5)} M{f(ix1-2.5)},{f((iy1+iy2)/2)} H{f(ix2+2.5)}" {S} stroke-width="{W3}" {CL}/>')
    return "".join(out)


def diseno_3_back():
    return f'<g opacity=".9">{flange(84, 22, 17)}</g>'


def diseno_3(p):
    css = """
  .d3.front{background:linear-gradient(160deg,#ffffff 0%,#f3f4f8 100%);color:var(--navy)}
  .d3.front .draw{color:#8a8fb4}
  .d3.front .lockup-wrap{left:22.5mm;top:15.5mm}
  .d3.front .lockup img{height:16mm}
  .d3.front .word{font-size:5.4mm;color:var(--navy)}
  .d3.front .foot{left:var(--m);right:var(--m);bottom:var(--m);display:flex;justify-content:space-between;align-items:baseline;border-top:.2mm solid #d5d8e4;padding-top:2mm}
  .d3.front .foot em{font-size:2.6mm;color:var(--navy)}
  .d3.front .foot span{font-size:1.5mm;font-weight:700;letter-spacing:.2mm;text-transform:uppercase;color:var(--muted)}
  .d3.back{background:var(--navy-deep);color:#fff}
  .d3.back .draw{color:#5d64a8}
  .d3.back .who{left:var(--m);top:var(--m)}
  .d3.back .who p{color:var(--soft)}
  .d3.back .data{left:var(--m);top:23mm}
  .d3.back .data dt{color:var(--soft)}
  .d3.back .foot{left:var(--m);bottom:var(--m);display:flex;align-items:center;gap:2mm;font-size:1.5mm;font-weight:700;letter-spacing:.2mm;text-transform:uppercase;color:var(--soft)}
  .d3.back .foot img{height:4.5mm}
"""
    html = f"""
<section class="card front d3">
  <svg class="draw" viewBox="0 0 95 57">{diseno_3_front()}</svg>
  <div class="abs lockup-wrap">{LOCKUP}</div>
  <div class="abs foot"><em class="serif">Precision you can measure.</em><span>Machined parts &amp; assemblies</span></div>
</section>
<section class="card back d3">
  <svg class="draw" viewBox="0 0 95 57">{diseno_3_back()}</svg>
  <div class="abs who"><h1>{p["nombre"]}</h1><p>{p["cargo"]}</p></div>
  <dl class="abs data">{data_html(p)}</dl>
  <p class="abs foot"><img src="sussek-icono.png" alt="">Since 1960 · 250+ CNC · ISO 9001 · IATF · AS9100</p>
</section>"""
    return css, html



# =====================================================================
# Conceptos: la tarjeta cuenta algo (inspirados en las referencias)
# =====================================================================

def balloon(x_feat, y_feat, x, y, n, label):
    """Globo numerado de plano con su etiqueta en dos renglones debajo."""
    l1, l2 = label
    return (f'<path d="M{f(x_feat)},{f(y_feat)} L{f(x)},{f(y-1.7)}" {S} stroke-width="{W3}"/>'
            f'<circle cx="{f(x_feat)}" cy="{f(y_feat)}" r=".35" fill="currentColor"/>'
            f'<circle cx="{f(x)}" cy="{f(y)}" r="1.7" {S} stroke-width="{W2}"/>'
            f'<text x="{f(x)}" y="{f(y+.62)}" class="dim b" text-anchor="middle">{n}</text>'
            f'<text x="{f(x)}" y="{f(y+3.9)}" class="lab" text-anchor="middle">{l1}</text>'
            f'<text x="{f(x)}" y="{f(y+5.7)}" class="lab" text-anchor="middle">{l2}</text>')


def bracket(x1, x2, y, label, up=True):
    """Corchete de anotación sobre (o bajo) un texto, con su etiqueta."""
    s = -1 if up else 1
    mid = (x1 + x2) / 2
    return (f'<path d="M{f(x1)},{f(y)} v{f(s*1.2)} H{f(x2)} v{f(-s*1.2)} M{f(mid)},{f(y+s*1.2)} v{f(s*1.2)}" {S} stroke-width="{W2}"/>'
            f'<text x="{f(mid)}" y="{f(y+s*(3.9 if up else 4.6))}" class="note" text-anchor="middle">{label}</text>')


CONCEPT_CSS = """
  .dim.b{font-weight:600}
  .lab{font-family:"IBM Plex Mono",monospace;font-size:1.4px;font-weight:600;letter-spacing:.06px;fill:currentColor}
  .note{font-family:"EB Garamond",Garamond,Georgia,serif;font-style:italic;font-size:2.3px;fill:currentColor}
  .mail{font-family:"IBM Plex Mono",monospace;font-size:3.6px;font-weight:500;fill:#1d1d22}
"""


# ---------- Concepto 1: GLOBOS (la pieza explica lo que hacen) ----------

def concepto_1(p):
    yc = 32.5
    body, pos = shaft(15, yc)
    ga, gb, gr = pos["gear"]
    sa, sb, sr = pos["spl"]
    b2a, b2b, b2r = pos["brg2"]
    art = [body,
           balloon((ga+gb)/2, yc+gr, (ga+gb)/2, 44.2, 1, ("5-AXIS", "HOBBING")),
           balloon((sa+sb)/2, yc+sr, (sa+sb)/2+1.5, 44.2, 2, ("INDUCTION", "HARDENED")),
           balloon(b2a+9, yc+b2r, b2a+11, 44.2, 3, ("CNC TURNED", "& GROUND")),
           balloon(b2b-4, yc+b2r, b2b-1.5, 44.2, 4, ("ASSEMBLED", "& SHIPPED"))]
    # reverso: correo anotado con corchetes (monoespaciada: 2.16 mm por letra)
    email = p["email"]
    cw = 3.6 * .6
    x0 = 47.5 - cw * len(email) / 2
    at = email.index("@")
    ym = 29.5
    back = [f'<text x="{f(x0)}" y="{f(ym)}" class="mail">{email}</text>',
            bracket(x0, x0 + cw * at, ym - 3.6, "our team"),
            bracket(x0 + cw * (at + 1), x0 + cw * len(email), ym - 3.6, "website"),
            bracket(x0, x0 + cw * len(email), ym + 1.6, "send us your print", up=False)]
    css = CONCEPT_CSS + """
  .c1.front{background:#fff;color:var(--navy)}
  .c1.front .draw{color:var(--navy)}
  .c1.front .lockup-wrap{left:var(--m);top:var(--m)}
  .c1.front .lockup img{height:9mm}
  .c1.front .word{font-size:3.3mm;color:var(--navy)}
  .c1.front .tag{right:var(--m);top:var(--m);text-align:right;font-family:"IBM Plex Mono",monospace;font-size:1.45mm;line-height:1.7;color:var(--muted)}
  .c1.front .tag b{color:var(--navy);font-weight:600}
  .c1.back{background:var(--paper);color:var(--navy)}
  .c1.back .draw{color:var(--navy)}
  .c1.back .who{left:0;right:0;top:var(--m);text-align:center}
  .c1.back .who p{color:var(--muted)}
  .c1.back .line{left:0;right:0;top:39.5mm;text-align:center;font-size:1.85mm;line-height:1.8;color:var(--ink)}
  .c1.back .mark{left:0;right:0;bottom:var(--m);display:flex;justify-content:center;align-items:center;gap:1.6mm;font-family:"EB Garamond",Garamond,Georgia,serif;font-weight:600;font-size:2.4mm;color:var(--navy)}
  .c1.back .mark img{height:4.2mm}
"""
    html = f"""
<section class="card front c1">
  <svg class="draw" viewBox="0 0 95 57">{"".join(art)}</svg>
  <div class="abs lockup-wrap">{LOCKUP}</div>
  <p class="abs tag">DWG <b>SMC-1960</b><br>REV <b>A</b> · SCALE <b>1:1</b></p>
</section>
<section class="card back c1">
  <svg class="draw" viewBox="0 0 95 57">{"".join(back)}</svg>
  <div class="abs who"><h1>{p["nombre"]}</h1><p>{p["cargo"]}</p></div>
  <p class="abs line">{p["tel"]} · {p["dir"]}</p>
  <p class="abs certs">ISO 9001 · IATF 16949 · AS9100 · 250+ CNC · USA · MX · CN</p>
  <div class="abs mark"><img src="sussek-icono.png" alt="">Sussek Machine Company</div>
</section>"""
    return css, html, False


# ---------- Concepto 2: REPORTE DE INSPECCIÓN (vertical, como tabla nutricional) ----------

def concepto_2(p):
    css = CONCEPT_CSS + """
  .c2.front{background:var(--paper);color:var(--ink)}
  .c2 .report{position:absolute;left:7.2mm;right:7.2mm;top:7.2mm;bottom:7.2mm;border:.35mm solid var(--ink);padding:2.6mm 2.8mm;display:flex;flex-direction:column}
  .c2 .report h2{font-family:"Archivo",Arial,sans-serif;font-stretch:78%;font-weight:900;font-size:5.5mm;line-height:.95;letter-spacing:-.05mm;text-transform:uppercase}
  .c2 .thick{height:1.8mm;background:var(--ink);margin:1.6mm 0 1.4mm}
  .c2 .mid{height:.9mm;background:var(--ink);margin:1.4mm 0 1.2mm}
  .c2 .k{font-family:"IBM Plex Mono",monospace;font-size:1.45mm;text-transform:uppercase;color:#55575f}
  .c2 .part b{display:block;font-family:"Archivo",Arial,sans-serif;font-stretch:90%;font-weight:800;font-size:3.9mm;line-height:1.05;margin-top:.5mm}
  .c2 .part span{font-size:1.8mm;font-weight:600}
  .c2 .row{display:flex;justify-content:space-between;align-items:baseline;gap:2mm;border-top:.18mm solid var(--ink);padding:.95mm 0;font-size:1.72mm}
  .c2 .row b{font-weight:700;text-align:right}
  .c2 .result{display:flex;justify-content:space-between;align-items:center;margin-top:auto}
  .c2 .result .k{line-height:1.6;white-space:nowrap}
  .c2 .stamp{transform:rotate(-9deg);border:.5mm solid var(--navy);color:var(--navy);padding:.8mm 2mm .6mm;font-family:"Archivo",Arial,sans-serif;font-stretch:80%;font-weight:900;font-size:3.3mm;letter-spacing:.25mm;box-shadow:inset 0 0 0 .35mm var(--paper),inset 0 0 0 .6mm var(--navy);opacity:.9}
  .c2 .sign{font-family:"EB Garamond",Garamond,Georgia,serif;font-style:italic;font-size:2.2mm;margin-top:1.8mm}
  .c2.back{background:var(--navy);color:#fff}
  .c2.back .grid{position:absolute;inset:0;opacity:.07;background-image:linear-gradient(#fff .1mm,transparent .1mm),linear-gradient(90deg,#fff .1mm,transparent .1mm);background-size:3mm 3mm}
  .c2.back .logo{left:0;right:0;top:14mm;display:flex;flex-direction:column;align-items:center;gap:3.4mm;text-align:center}
  .c2.back .logo img{height:17mm}
  .c2.back .logo .word{font-size:5mm}
  .c2.back .rule{left:50%;top:57mm;width:10mm;margin-left:-5mm;height:.5mm;background:var(--steel)}
  .c2.back .data{left:0;right:0;bottom:12mm;display:block;text-align:center;font-size:1.9mm;line-height:1.85}
  .c2.back .data .dim2{color:var(--soft)}
"""
    html = f"""
<section class="card front c2">
  <div class="report">
    <h2>Inspection<br>Report</h2>
    <div class="thick"></div>
    <div class="part"><span class="k">Part</span><b>{p["nombre"]}</b><span>{p["cargo"]}</span></div>
    <div class="mid"></div>
    <div class="row"><span class="k">Supplier</span><b>Sussek Machine Co.</b></div>
    <div class="row"><span class="k">Process</span><b>Milling · Turning · Hobbing</b></div>
    <div class="row"><span class="k">Capacity</span><b>250+ CNC centers</b></div>
    <div class="row"><span class="k">Certified</span><b>ISO 9001 · IATF · AS9100</b></div>
    <div class="row"><span class="k">Since</span><b>1960</b></div>
    <div class="row"><span class="k">Tolerance</span><b>±0.005</b></div>
    <div class="thick"></div>
    <div class="result"><span class="k">Result<br>100% checked</span><span class="stamp">APPROVED</span></div>
    <p class="sign">Ready for your next part.</p>
  </div>
</section>
<section class="card back c2">
  <div class="grid"></div>
  <div class="abs logo"><img src="sussek-icono.png" alt="">{WORD}</div>
  <i class="abs rule"></i>
  <p class="abs data">{p["tel"]}<br>{p["email"]}<br>{p["web"]}<br><span class="dim2">{p["dir"]}</span></p>
</section>"""
    return css, html, True


# ---------- Concepto 3: PLACA DE MÁQUINA (acero con remaches) ----------

RIVETS = "".join(f'<i class="rivet" style="left:{x}mm;top:{y}mm"></i>' for x, y in [(6.2, 6.2), (86.6, 6.2), (6.2, 48.6), (86.6, 48.6)])


def concepto_3(p):
    css = CONCEPT_CSS + """
  .c3.front{color:var(--navy);background:
      repeating-linear-gradient(90deg,rgba(255,255,255,.10) 0 .12mm,rgba(0,0,0,.035) .12mm .26mm,rgba(255,255,255,0) .26mm .5mm),
      linear-gradient(120deg,#c9cdd3 0%,#eef0f2 28%,#b3b9c0 50%,#e7eaed 72%,#aeb4bb 100%)}
  .c3.back{color:#fff;background:
      repeating-linear-gradient(90deg,rgba(255,255,255,.04) 0 .12mm,rgba(0,0,0,.06) .12mm .26mm,rgba(255,255,255,0) .26mm .5mm),
      linear-gradient(120deg,#1a1a45 0%,#2a2a66 35%,#191942 60%,#26265c 100%)}
  .c3 .rivet{position:absolute;width:3.2mm;height:3.2mm;margin:-1.6mm 0 0 -1.6mm;border-radius:50%;
      background:radial-gradient(circle at 35% 30%,#ffffff 0%,#d4d8dd 25%,#8c939b 70%,#5d636b 100%);box-shadow:0 .2mm .35mm rgba(0,0,0,.45),inset 0 -.2mm .3mm rgba(0,0,0,.3)}
  .c3 .frame{position:absolute;left:9.5mm;right:9.5mm;top:9mm;bottom:9mm;border:.3mm solid currentColor;border-radius:1.2mm}
  .c3.front .frame{box-shadow:0 .15mm 0 rgba(255,255,255,.7)}
  .c3 .eng{text-shadow:0 .14mm 0 rgba(255,255,255,.65)}
  .c3.back .eng{text-shadow:0 -.12mm 0 rgba(0,0,0,.5)}
  .c3.front .lockup-wrap{left:12.5mm;top:12mm}
  .c3.front .lockup img{height:11mm;filter:drop-shadow(0 .2mm .3mm rgba(0,0,0,.35))}
  .c3.front .word{font-size:4.1mm}
  .c3.front .made{right:12.5mm;top:12.6mm;text-align:right;font-family:"IBM Plex Mono",monospace;font-size:1.4mm;line-height:1.75;font-weight:600;letter-spacing:.08mm}
  .c3.front .cells{left:12.5mm;right:12.5mm;bottom:12mm;display:grid;grid-template-columns:1.5fr 1fr 1fr;border:.25mm solid var(--navy)}
  .c3.front .cells>div{padding:.8mm 1.3mm .9mm;border-left:.2mm solid var(--navy)}
  .c3.front .cells>div:first-child{border-left:0}
  .c3.front .cells>div.wide{grid-column:1/4;border-left:0;border-top:.2mm solid var(--navy)}
  .c3 small{display:block;font-family:"IBM Plex Mono",monospace;font-size:1.1mm;letter-spacing:.1mm;opacity:.75}
  .c3.front .cells b{font-size:1.65mm;font-weight:700;letter-spacing:.1mm;white-space:nowrap}
  .c3.back .who{left:12.5mm;top:12.5mm}
  .c3.back .who p{color:var(--soft)}
  .c3.back .data{left:12.5mm;bottom:12.5mm;font-size:1.85mm}
  .c3.back .data dt{color:var(--soft)}
  .c3.back .tag{right:12.5mm;top:13mm;text-align:right;font-family:"IBM Plex Mono",monospace;font-size:1.4mm;line-height:1.75;color:var(--soft)}
  .c3.back .tag img{height:6.5mm;display:block;margin:0 0 1.4mm auto}
"""
    html = f"""
<section class="card front c3">
  <div class="frame"></div>{RIVETS}
  <div class="abs lockup-wrap eng">{LOCKUP}</div>
  <p class="abs made eng">MADE IN<br>USA · MX · CN</p>
  <div class="abs cells eng">
    <div><small>MODEL</small><b>PRECISION PARTS</b></div>
    <div><small>CAPACITY</small><b>250+ CNC</b></div>
    <div><small>EST.</small><b>1960</b></div>
    <div class="wide"><small>CERTIFIED</small><b>ISO 9001 · IATF 16949 · AS9100</b></div>
  </div>
</section>
<section class="card back c3">
  <div class="frame" style="color:rgba(255,255,255,.35)"></div>{RIVETS}
  <div class="abs who eng"><h1>{p["nombre"]}</h1><p>{p["cargo"]}</p></div>
  <p class="abs tag"><img src="sussek-icono.png" alt="">S/N SMC-1960</p>
  <dl class="abs data eng">{data_html(p)}</dl>
</section>"""
    return css, html, False



# =====================================================================
# Variaciones finales: combinan los elementos elegidos
# =====================================================================

ICON_AR = 249 / 221          # ancho/alto del ícono
WORD_W = {4.4: 17.85}        # ancho medido del nombre (mm) según tamaño de letra
WORD_H = {4.4: 15.84}


def dim_v_rot(x, y1, y2, text):
    """Cota vertical con el texto girado, centrado sobre la línea."""
    mid, gap = (y1 + y2) / 2, .52 * len(text) + .7
    return (f'<path d="M{f(x)},{f(y1)} V{f(mid-gap)} M{f(x)},{f(mid+gap)} V{f(y2)}" {S} stroke-width="{W3}"/>'
            + arrow(x, y1, -math.pi / 2) + arrow(x, y2, math.pi / 2)
            + f'<text x="{f(x)}" y="{f(mid+.5)}" class="dim" text-anchor="middle" transform="rotate(-90 {f(x)} {f(mid)})">{text}</text>')


def ext_v(x, y_from, y_to):
    return f'<path d="M{f(x)},{f(y_from)} V{f(y_to)}" {S} stroke-width="{W3}"/>'


def ext_h(y, x_from, x_to):
    return f'<path d="M{f(x_from)},{f(y)} H{f(x_to)}" {S} stroke-width="{W3}"/>'


def gear_callout(cx, cy, R, x_end, y_text):
    """Cota de los barrenos con su medida real impresa (escala 1:1, mm)."""
    g = gear_geom(R)
    a = -math.pi / 6
    hx, hy = cx + g["bc"] * math.cos(a), cy + g["bc"] * math.sin(a)
    txt = f"6× Ø{2*g['hole']:.2f} EQ SP ON Ø{2*g['bc']:.2f}"
    return leader(hx + .8, hy - .8, hx + 4.5, y_text, x_end, txt, anchor="end")


def gear_od_callout(cx, cy, R, x_end, y_text, N=22):
    """Cota del diámetro exterior con dientes y módulo."""
    g = gear_geom(R, N)
    a = math.radians(160)
    x1, y1 = cx + R * math.cos(a), cy + R * math.sin(a)
    return leader(x1 - .2, y1 + .1, x1 - 3.6, y_text, x_end, f"Ø{2*R:.2f} · {N}T", anchor="start")


# ---------- Variación 1: plano azul con engrane + logo acotado / correo anotado ----------

def variacion_1(p):
    ix, top, ih, fs = 12.0, 13.0, 12.0, 4.4
    iw = ih * ICON_AR
    lh = max(ih, WORD_H[fs])
    iy1 = top + (lh - ih) / 2
    iy2 = iy1 + ih
    wx2 = ix + iw + 3 + WORD_W[fs]
    cx, cy, R = 72.0, 28.5, 16.5
    art = [gear(cx, cy, R), gear_callout(cx, cy, R, 86.5, 9.8),
           gear_od_callout(cx, cy, R, 38.5, 36.2),
           ext_v(ix, top - .8, 8.9), ext_v(wx2, top - .8, 8.9), dim_h(ix, wx2, 9.8, f"{wx2-ix:.2f}"),
           ext_h(iy1, ix - .8, 8.2), ext_h(iy2, ix - .8, 8.2), dim_v_rot(9.1, iy1, iy2, f"{ih:.2f}"),
           leader(ix + .7, iy2 - .7, ix + 3, iy2 + 3.8, ix + 14, "R2.5 TYP"),
           '<text x="86.5" y="48.5" class="dim" text-anchor="end">MM · SCALE 1:1</text>']
    email = p["email"]
    cw = 3.6 * .6
    x0 = 47.5 - cw * len(email) / 2
    at = email.index("@")
    ym = 28.8
    back = [f'<text x="{f(x0)}" y="{f(ym)}" class="mail">{email}</text>',
            bracket(x0, x0 + cw * at, ym - 3.6, "our team"),
            bracket(x0 + cw * (at + 1), x0 + cw * len(email), ym - 3.6, "website"),
            f'<path d="M{f(x0+1)},{f(ym+1.4)} v2.6 h3.2" {S} stroke-width="{W2}"/>' + arrow(x0 + 4.4, ym + 4, 0, 1, .4),
            f'<text x="{f(x0+5.4)}" y="{f(ym+4.75)}" class="note">send us your print</text>']
    css = CONCEPT_CSS + f"""
  .v1.front{{background:radial-gradient(110% 130% at 75% 50%,#2a2a6e 0%,var(--navy) 45%,var(--navy-deep) 100%);color:#fff}}
  .v1.front .grid{{position:absolute;inset:0;opacity:.04;background-image:linear-gradient(#fff .1mm,transparent .1mm),linear-gradient(90deg,#fff .1mm,transparent .1mm);background-size:3mm 3mm;background-position:.5mm .5mm}}
  .v1.front .draw{{color:var(--line)}}
  .v1.front .lockup-wrap{{left:{ix}mm;top:{top}mm}}
  .v1.front .lockup img{{height:{ih}mm}}
  .v1.front .word{{font-size:{fs}mm}}
  .v1.front .pitch{{left:var(--m);bottom:var(--m)}}
  .v1 .pitch h2{{font-family:"EB Garamond",Garamond,Georgia,serif;font-weight:500;font-size:5.4mm;line-height:1.02}}
  .v1.back{{background:var(--paper);color:var(--navy)}}
  .v1.back .draw{{color:var(--navy)}}
  .v1.back .who{{left:0;right:0;top:var(--m);text-align:center}}
  .v1.back .who p{{color:var(--muted)}}
  .v1.back .line{{left:0;right:0;top:36.9mm;text-align:center;font-size:1.85mm;color:var(--ink)}}
  .v1.back .certs{{left:0;right:0;top:40.6mm;text-align:center;font-size:1.4mm;font-weight:700;letter-spacing:.2mm;color:var(--muted)}}
  .v1.back .mark{{left:0;right:0;bottom:var(--m);display:flex;justify-content:center;align-items:center;gap:1.6mm;font-family:"EB Garamond",Garamond,Georgia,serif;font-weight:600;font-size:2.4mm}}
  .v1.back .mark img{{height:4.2mm}}
"""
    html = f"""
<section class="card front v1">
  <div class="grid"></div>
  <svg class="draw" viewBox="0 0 95 57">{"".join(art)}</svg>
  <div class="abs lockup-wrap">{LOCKUP}</div>
  <div class="abs pitch"><h2>From print<br><em>to part.</em></h2></div>
</section>
<section class="card back v1">
  <svg class="draw" viewBox="0 0 95 57">{"".join(back)}</svg>
  <div class="abs who"><h1>{p["nombre"]}</h1><p>{p["cargo"]}</p></div>
  <p class="abs line">{p["tel"]} · {p["dir"]}</p>
  <p class="abs certs">ISO 9001 · IATF 16949 · AS9100 · 250+ CNC · USA · MX · CN</p>
  <div class="abs mark"><img src="sussek-icono.png" alt="">Sussek Machine Company</div>
</section>"""
    return css, html, False


# ---------- Variación 2: reporte de inspección / reverso azul con logo acotado ----------

def variacion_2(p):
    css, html, _ = concepto_2(p)
    ih, top = 17.0, 16.0
    iw = ih * ICON_AR
    ix1, ix2 = 28.5 - iw / 2, 28.5 + iw / 2
    iy2 = top + ih
    art = [ext_v(ix1, top - .8, 11.6), ext_v(ix2, top - .8, 11.6), dim_h(ix1, ix2, 12.5, f"{iw:.3f}"),
           ext_h(top, ix1 - .8, 13.9), ext_h(iy2, ix1 - .8, 13.9), dim_v_rot(14.8, top, iy2, f"{ih:.3f}"),
           f'<path d="M28.5,{f(top-2.2)} V{f(iy2+2.2)} M{f(ix1-2)},{f(top+ih/2)} H{f(ix2+2.2)}" {S} stroke-width="{W3}" {CL}/>']
    svg = f'<svg class="draw" viewBox="0 0 57 95" style="width:57mm;height:95mm;color:var(--line)">{"".join(art)}</svg>'
    html = html.replace('<div class="grid"></div>', '<div class="grid"></div>' + svg)
    css = css.replace(".c2.back .logo{left:0;right:0;top:14mm;", ".c2.back .logo{left:0;right:0;top:16mm;")
    return css, html, True


# ---------- Variación 3: pieza con globos / reverso azul con engrane ----------

def variacion_3(p):
    css, html, _ = concepto_1(p)
    front = html[:html.index('<section class="card back c1">')]
    cx, cy, R = 73.0, 28.5, 17.0
    art = gear(cx, cy, R) + gear_callout(cx, cy, R, 86.5, 9.8)
    css += """
  .c1.back2{background:radial-gradient(110% 130% at 78% 50%,#2a2a6e 0%,var(--navy) 45%,var(--navy-deep) 100%);color:#fff}
  .c1.back2 .grid{position:absolute;inset:0;opacity:.07;background-image:linear-gradient(#fff .1mm,transparent .1mm),linear-gradient(90deg,#fff .1mm,transparent .1mm);background-size:3mm 3mm;background-position:.5mm .5mm}
  .c1.back2 .draw{color:var(--line)}
  .c1.back2 .who{left:var(--m);top:var(--m)}
  .c1.back2 .who p{color:var(--soft)}
  .c1.back2 .data{left:var(--m);top:22.5mm}
  .c1.back2 .data dt{color:var(--soft)}
  .c1.back2 .mark2{left:var(--m);bottom:var(--m);display:flex;align-items:center;gap:1.6mm;font-family:"EB Garamond",Garamond,Georgia,serif;font-weight:600;font-size:2.4mm}
  .c1.back2 .mark2 img{height:4.2mm}
"""
    back = f"""
<section class="card c1 back2">
  <div class="grid"></div>
  <svg class="draw" viewBox="0 0 95 57">{art}</svg>
  <div class="abs who"><h1>{p["nombre"]}</h1><p>{p["cargo"]}</p></div>
  <dl class="abs data">{data_html(p)}</dl>
  <div class="abs mark2"><img src="sussek-icono.png" alt="">Sussek Machine Company</div>
</section>"""
    return css, front + back, False



# ---------- Variación 5: TARJETA HERRAMIENTA (galgas de radio + reglas reales) ----------

PX = 96 / 25.4   # px por mm (para el recorte de la vista previa)


def tool_shape(mirror=False, k=1.0):
    """Contorno de corte (con 3 mm de sangrado): esquina R5 convexa, muesca R2.5 cóncava, R1.5 en las otras.
    mirror=True da el contorno visto desde el reverso; k escala a otras unidades (px para la vista previa)."""
    X = (lambda x: (95 - x) * k) if mirror else (lambda x: x * k)
    Y = lambda y: y * k
    sw = (lambda v: 1 - v) if mirror else (lambda v: v)
    arc = lambda r, flag, x, y: f"A{f(r*k)},{f(r*k)} 0 0 {sw(flag)} {f(X(x))},{f(Y(y))}"
    return " ".join([f"M{f(X(8))},{f(Y(3))}", f"H{f(X(90.5))}", arc(1.5, 1, 92, 4.5), f"V{f(Y(51.5))}",
                     arc(2.5, 0, 89.5, 54), f"H{f(X(4.5))}", arc(1.5, 1, 3, 52.5), f"V{f(Y(8))}",
                     arc(5, 1, 8, 3), "Z"])


def inch_ruler(x0, y, inches=3):
    d, t = [], []
    for k in range(inches * 16 + 1):
        x = x0 + k * 25.4 / 16
        L = 2.6 if k % 16 == 0 else 2.0 if k % 8 == 0 else 1.5 if k % 4 == 0 else 1.1 if k % 2 == 0 else .7
        d.append(f"M{f(x)},{y} v{L}")
        if k % 16 == 0:
            t.append(f'<text x="{f(x+.6)}" y="{f(y+3.9)}" class="dim">{k//16}{" IN" if k == 0 else ""}</text>')
    return f'<path d="{" ".join(d)}" {S} stroke-width=".15"/>' + "".join(t)


def mm_ruler(x0, y, mm=70):
    d, t = [], []
    for k in range(mm + 1):
        x = x0 + k
        L = 2.6 if k % 10 == 0 else 1.7 if k % 5 == 0 else 1.0
        d.append(f"M{f(x)},{y} v{-L}")
        if k % 10 == 0:
            t.append(f'<text x="{f(x)}" y="{f(y-3.6)}" class="dim" text-anchor="middle">{k//10 if k else "0 CM"}</text>')
    return f'<path d="{" ".join(d)}" {S} stroke-width=".15"/>' + "".join(t)


def inch_ruler_edge(x0, y_trim, y_bleed, inches=3):
    """Regla en pulgadas cuyas rayas nacen en el sangrado: tras el corte tocan la orilla."""
    s_ = 1 if y_bleed < y_trim else -1
    d, t = [], []
    for k in range(inches * 16 + 1):
        x = x0 + k * 25.4 / 16
        L = 2.6 if k % 16 == 0 else 2.0 if k % 8 == 0 else 1.5 if k % 4 == 0 else 1.1 if k % 2 == 0 else .7
        d.append(f"M{f(x)},{f(y_bleed)} V{f(y_trim + s_*L)}")
        if k % 16 == 0:
            t.append(f'<text x="{f(x+.6)}" y="{f(y_trim + s_*3.9)}" class="dim">{k//16}{" IN" if k == 0 else ""}</text>')
    return f'<path d="{" ".join(d)}" {S} stroke-width=".15"/>' + "".join(t)


def mm_ruler_edge(x0, y_trim, y_bleed, mm=70):
    s_ = 1 if y_bleed < y_trim else -1
    d, t = [], []
    for k in range(mm + 1):
        x = x0 + k
        L = 2.6 if k % 10 == 0 else 1.7 if k % 5 == 0 else 1.0
        d.append(f"M{f(x)},{f(y_bleed)} V{f(y_trim + s_*L)}")
        if k % 10 == 0:
            t.append(f'<text x="{f(x)}" y="{f(y_trim + s_*3.6)}" class="dim" text-anchor="middle">{k//10 if k else "0 CM"}</text>')
    return f'<path d="{" ".join(d)}" {S} stroke-width=".15"/>' + "".join(t)


def variacion_5(p):
    front_art = (inch_ruler(13, 3) + mm_ruler(6, 54)
                 + '<text x="4.6" y="12.6" class="dim b">R5</text>'
                 + '<text x="88.6" y="48.2" class="dim b" text-anchor="end">R2.5</text>')
    css = CONCEPT_CSS + f"""
  .v5.front{{background:radial-gradient(110% 130% at 70% 45%,#2a2a6e 0%,var(--navy) 45%,var(--navy-deep) 100%);color:#fff}}
  .v5.front .draw{{color:var(--line)}}
  .v5.front .lockup-wrap{{left:var(--m);top:19mm}}
  .v5.front .lockup img{{height:12mm}}
  .v5.front .word{{font-size:4.4mm}}
  .v5.front .pitch{{right:var(--m);top:21mm;text-align:right}}
  .v5 .pitch h2{{font-family:"EB Garamond",Garamond,Georgia,serif;font-weight:500;font-size:5.4mm;line-height:1.02}}
  .v5 .pitch p{{margin-top:2mm;font-family:"IBM Plex Mono",monospace;font-size:1.45mm;letter-spacing:.1mm;color:var(--soft)}}
  .v5.back{{background:var(--paper);color:var(--ink)}}
  .v5 .rep{{position:absolute;left:8mm;right:8mm;top:7.6mm;bottom:7.6mm;display:flex;flex-direction:column}}
  .v5 .head{{display:flex;justify-content:space-between;align-items:baseline}}
  .v5 .head h2{{font-family:"Archivo",Arial,sans-serif;font-stretch:78%;font-weight:900;font-size:3.9mm;letter-spacing:-.03mm;text-transform:uppercase}}
  .v5 .k{{font-family:"IBM Plex Mono",monospace;font-size:1.3mm;text-transform:uppercase;color:#55575f}}
  .v5 .sn{{font-family:"IBM Plex Mono",monospace;font-size:1.5mm;font-weight:600}}
  .v5 .bar{{height:1.1mm;background:var(--ink);margin:1.1mm 0 1.6mm}}
  .v5 .cols{{display:grid;grid-template-columns:1fr 1.15fr;gap:3.4mm}}
  .v5 .part b{{display:block;font-family:"Archivo",Arial,sans-serif;font-stretch:90%;font-weight:800;font-size:3.1mm;line-height:1.05;margin-top:.3mm}}
  .v5 .part span{{font-size:1.55mm;font-weight:600}}
  .v5 .cont{{margin-top:1.8mm;display:grid;grid-template-columns:auto 1fr;column-gap:1.6mm;row-gap:.35mm;font-size:1.5mm;align-items:baseline}}
  .v5 .cont dt{{font-family:"IBM Plex Mono",monospace;font-size:1.25mm;color:var(--navy);font-weight:600}}
  .v5 .row{{display:flex;justify-content:space-between;align-items:baseline;gap:1.5mm;border-top:.15mm solid var(--ink);padding:.55mm 0;font-size:1.45mm}}
  .v5 .row b{{font-weight:700;text-align:right;white-space:nowrap}}
  .v5 .foot{{margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end;border-top:.5mm solid var(--ink);padding-top:1.2mm}}
  .v5 .foot em{{font-family:"EB Garamond",Garamond,Georgia,serif;font-size:2.1mm}}
  .v5 .stamp{{transform:rotate(-8deg) translate(-1mm,-.6mm);border:.45mm solid var(--navy);color:var(--navy);padding:.5mm 1.6mm .4mm;font-family:"Archivo",Arial,sans-serif;font-stretch:80%;font-weight:900;font-size:2.7mm;letter-spacing:.22mm;box-shadow:inset 0 0 0 .3mm var(--paper),inset 0 0 0 .5mm var(--navy);opacity:.9}}
  .dieline{{background:#fff}}
  @media screen{{
    .v5.front{{clip-path:path('{tool_shape(k=PX)}')}}
    .v5.back{{clip-path:path('{tool_shape(True, k=PX)}')}}
    .dieline{{display:none}}
  }}
"""
    html = f"""
<section class="card front v5">
  <svg class="draw" viewBox="0 0 95 57">{front_art}</svg>
  <div class="abs lockup-wrap">{LOCKUP}</div>
  <div class="abs pitch"><h2>From print<br><em>to part.</em></h2><p>MM + IN · SCALE 1:1 · MEASURE IT.</p></div>
</section>
<section class="card back v5">
  <div class="rep">
    <div class="head"><h2>Inspection Report</h2><span class="sn">S/N 000347</span></div>
    <div class="bar"></div>
    <div class="cols">
      <div>
        <div class="part"><span class="k">Part</span><b>{p["nombre"]}</b><span>{p["cargo"]}</span></div>
        <dl class="cont">{data_html(p)}</dl>
      </div>
      <div>
        <div class="row"><span class="k">Supplier</span><b>Sussek Machine Co.</b></div>
        <div class="row"><span class="k">Process</span><b>Milling · Turning · Hobbing</b></div>
        <div class="row"><span class="k">Capacity</span><b>250+ CNC</b></div>
        <div class="row"><span class="k">Certified</span><b>ISO 9001 · IATF · AS9100</b></div>
        <div class="row"><span class="k">Since</span><b>1960 · US · MX · CN</b></div>
      </div>
    </div>
    <div class="foot"><em>Ready for your next part.</em><span class="stamp">APPROVED</span></div>
  </div>
</section>
<section class="card dieline">
  <svg class="draw" viewBox="0 0 95 57">
    <rect x="0" y="0" width="95" height="57" fill="none" stroke="#bbb" stroke-width=".1" stroke-dasharray="1 .6"/>
    <path d="{tool_shape()}" fill="none" stroke="#e6007e" stroke-width=".2"/>
    <text x="47.5" y="24" class="dim" text-anchor="middle" fill="#e6007e" style="fill:#e6007e;font-size:2px">DIE LINE · TROQUEL (FRENTE)</text>
    <text x="47.5" y="28" class="dim" text-anchor="middle" style="fill:#555;font-size:1.6px">89 × 51 MM · R5 CONVEXO SUP. IZQ. · R2.5 CÓNCAVO INF. DER. · R1.5 RESTO</text>
    <text x="47.5" y="31" class="dim" text-anchor="middle" style="fill:#555;font-size:1.6px">SANGRADO 3 MM · NO IMPRIMIR ESTA PÁGINA</text>
  </svg>
</section>"""
    return css, html, False



# ---------- Tarjeta REGLA: frente con reglas reales / reverso con brida y cuadro de rótulo ----------

def regla(p, troquel=True):
    x_in = 13 if troquel else 8.5
    if troquel:
        W, H, B = 95, 57, 3
        front_art = inch_ruler(x_in, 3) + mm_ruler(x_in - 7, 54)
    else:
        W, H, B = 95.25, 57.15, 3.175            # 3.5 x 2 in + 1/8 in de sangrado
        front_art = inch_ruler_edge(8.5, B, 0) + mm_ruler_edge(8.5, H - B, H)
    if troquel:
        front_art += ('<text x="4.6" y="12.6" class="dim b">R5</text>'
                      '<text x="88.6" y="48.2" class="dim b" text-anchor="end">R2.5</text>')
    # reverso: brida redonda a escala 1:1 (mm)
    cx, cy, R = 74.0, 22.5, 10.5
    bc, hole = R * .78, 1.05
    a = math.radians(225)
    hx, hy = cx + bc * math.cos(a), cy + bc * math.sin(a)
    back_art = (flange(cx, cy, R)
                + leader(hx - .75, hy - .75, hx - 3.4, 9.6, hx - 15.5, f"4× Ø{2*hole:.2f} THRU", anchor="start")
                + leader(cx + R * math.cos(math.radians(-40)) + .1, cy + R * math.sin(math.radians(-40)) - .1,
                         cx + 10.6, 9.6, 86.5, f"Ø{2*R:.2f}", anchor="end")
                + fcf(cx - 8.2, cy + R + 3.2, "pos", f"Ø0.02", "A"))
    cls = "rg" + ("t" if troquel else "c")
    clip = ""
    if troquel:
        clip = f"""
  @media screen{{
    .{cls}.front{{clip-path:path('{tool_shape(k=PX)}')}}
    .{cls}.back{{clip-path:path('{tool_shape(True, k=PX)}')}}
    .dieline{{display:none}}
  }}"""
    css = CONCEPT_CSS + f"""
  .{cls}.front{{background:radial-gradient(110% 130% at 70% 45%,#2a2a6e 0%,var(--navy) 45%,var(--navy-deep) 100%);color:#fff}}
  .{cls}.front .draw{{color:var(--line)}}
  .{cls}.front .lockup-wrap{{left:var(--m);top:19mm}}
  .{cls}.front .lockup img{{height:12mm}}
  .{cls}.front .word{{font-size:4.4mm}}
  .{cls}.front .pitch{{right:var(--m);top:21mm;text-align:right}}
  .{cls} .pitch h2{{font-family:"EB Garamond",Garamond,Georgia,serif;font-weight:500;font-size:5.4mm;line-height:1.02}}
  .{cls} .pitch p{{margin-top:2mm;font-family:"IBM Plex Mono",monospace;font-size:1.45mm;letter-spacing:.1mm;color:var(--soft)}}
  .{cls}.back{{background:#fff;color:var(--navy)}}
  .{cls}.back .draw{{color:var(--navy)}}
  .{cls}.back .who{{left:var(--m);top:var(--m)}}
  .{cls}.back .who p{{color:var(--muted)}}
  .{cls}.back .data{{left:var(--m);top:22.5mm;color:var(--ink)}}
  .{cls}.back .data dt{{color:var(--navy)}}
  .{cls}.back .foot{{left:var(--m);right:var(--m);bottom:var(--m);display:flex;align-items:center;gap:2.6mm}}
  .{cls}.back .foot img{{height:5.8mm;display:block}}
  .{cls}.back .block{{flex:1;height:5.4mm;display:grid;grid-template-columns:1fr 1fr 1fr auto;border:.25mm solid var(--navy);font-size:1.45mm;font-weight:700;letter-spacing:.2mm;text-transform:uppercase}}
  .{cls}.back .block>*{{display:flex;align-items:center;justify-content:center;padding:0 1.8mm;border-left:.18mm solid var(--navy)}}
  .{cls}.back .block>:first-child{{border-left:0}}
  .{cls}.back .block .geo{{background:var(--navy);color:#fff}}
  .dieline{{background:#fff}}{clip}
"""
    if not troquel:
        css += f"""
  @page {{ size: {W}mm {H}mm; margin: 0; }}
  .card{{width:{W}mm;height:{H}mm}}
  .draw{{width:{W}mm;height:{H}mm}}
  @media screen{{ .card{{clip-path:inset({B}mm round .4mm)}} }}
"""
    front_note = "MM + IN · SCALE 1:1 · MEASURE IT."
    html = f"""
<section class="card front {cls}">
  <svg class="draw" viewBox="0 0 {W} {H}">{front_art}</svg>
  <div class="abs lockup-wrap">{LOCKUP}</div>
  <div class="abs pitch"><h2>From print<br><em>to part.</em></h2><p>{front_note}</p></div>
</section>
<section class="card back {cls}">
  <svg class="draw" viewBox="0 0 {W} {H}">{back_art}</svg>
  <div class="abs who"><h1>{p["nombre"]}</h1><p>{p["cargo"]}</p></div>
  <dl class="abs data">{data_html(p)}</dl>
  <div class="abs foot"><img src="sussek-icono.png" alt="">
    <div class="block"><div>Machining</div><div>Assembly</div><div>Engineering</div><div class="geo">USA · MX · CN</div></div>
  </div>
</section>"""
    if troquel:
        html += f"""
<section class="card dieline">
  <svg class="draw" viewBox="0 0 95 57">
    <rect x="0" y="0" width="95" height="57" fill="none" stroke="#bbb" stroke-width=".1" stroke-dasharray="1 .6"/>
    <path d="{tool_shape()}" fill="none" stroke="#e6007e" stroke-width=".2"/>
    <text x="47.5" y="24" class="dim" text-anchor="middle" style="fill:#e6007e;font-size:2px">DIE LINE · TROQUEL (FRENTE)</text>
    <text x="47.5" y="28" class="dim" text-anchor="middle" style="fill:#555;font-size:1.6px">89 × 51 MM · R5 CONVEXO SUP. IZQ. · R2.5 CÓNCAVO INF. DER. · R1.5 RESTO</text>
    <text x="47.5" y="31" class="dim" text-anchor="middle" style="fill:#555;font-size:1.6px">SANGRADO 3 MM · NO IMPRIMIR ESTA PÁGINA</text>
  </svg>
</section>"""
    return css, html, False


DISENOS = {"variacion-1-plano": variacion_1, "variacion-2-inspeccion": variacion_2, "variacion-3-globos": variacion_3,
           "variacion-5-herramienta": variacion_5,
           "regla-troquel": lambda p: regla(p, True), "regla-cuadrada": lambda p: regla(p, False)}


def page(title, css, body, vertical=False):
    if vertical:
        css += """
  @page { size: 57mm 95mm; margin: 0; }
  .card{width:57mm;height:95mm}
"""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
{FONTS}
<style>{BASE_CSS}{css}</style>
</head>
<body>
<!-- Nombre y cargo son de ejemplo; datos de la planta de Waterloo tomados de sussek.com -->
{body}
</body>
</html>
"""


if __name__ == "__main__":
    here = Path(__file__).parent
    for name, fn in DISENOS.items():
        css, body, vertical = fn(PERSONA)
        (here / f"{name}.html").write_text(page(f"Sussek · {name}", css, body, vertical))
        print("ok", name)
