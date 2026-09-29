"""Genera las 3 variantes de tarjetas de Sussek Machine Company.

Edita PERSONA y corre:  python3 generar.py
Cada variante sale como HTML (frente + reverso, 89 x 51 mm con 3 mm de sangrado).
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
DASH = 'stroke-dasharray="2.4 .7 .45 .7"'


# ---------- dibujos (unidades = mm de la tarjeta, viewBox 0 0 95 57) ----------

def gear(cx, cy, R, N=22, w=.3, detail=True):
    s = R / 21
    Rr = 18.2 * s
    pts = []
    for i in range(N):
        a, p = 2 * math.pi * i / N, 2 * math.pi / N
        for f, r in [(0, Rr), (.18, Rr), (.32, R), (.58, R), (.72, Rr)]:
            pts.append((cx + r * math.cos(a + f * p), cy + r * math.sin(a + f * p)))
    out = [f'<path d="M{" L".join(f"{x:.3f},{y:.3f}" for x, y in pts)}Z" {S} stroke-width="{w}"/>']
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{16.6*s:.3f}" {S} stroke-width="{w*.45:.3f}" {DASH}/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{13.2*s:.3f}" {S} stroke-width="{w*.8:.3f}"/>')
    if detail:
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{9.2*s:.3f}" {S} stroke-width="{w*.45:.3f}" {DASH}/>')
        for i in range(6):
            a = math.pi / 6 + i * math.pi / 3
            out.append(f'<circle cx="{cx+9.2*s*math.cos(a):.3f}" cy="{cy+9.2*s*math.sin(a):.3f}" r="{1.35*s:.3f}" {S} stroke-width="{w*.8:.3f}"/>')
        r, k, h = 4.6 * s, 1.1 * s, 5.6 * s
        yk = cy - math.sqrt(r * r - k * k)
        out.append(f'<path d="M{cx-k:.3f},{yk:.3f} A{r:.3f},{r:.3f} 0 1 0 {cx+k:.3f},{yk:.3f} V{cy-h:.3f} H{cx-k:.3f}Z" {S} stroke-width="{w}"/>')
    e = R + 3.5 * s
    out.append(f'<path d="M{cx-e:.3f},{cy} H{cx+e:.3f} M{cx},{cy-e:.3f} V{cy+e:.3f}" {S} stroke-width="{w*.4:.3f}" {DASH}/>')
    return "\n".join(out)


def leader(x1, y1, x2, y2, x3, text, w=.14, anchor="start"):
    """Cota con flecha en (x1,y1), quiebre en (x2,y2) y texto sobre la línea hasta x3."""
    ang = math.atan2(y1 - y2, x1 - x2)
    a1, a2 = ang + 2.75, ang - 2.75
    tip = f"M{x1:.2f},{y1:.2f} L{x1+1.3*math.cos(a1):.2f},{y1+1.3*math.sin(a1):.2f} L{x1+1.3*math.cos(a2):.2f},{y1+1.3*math.sin(a2):.2f}Z"
    tx = min(x2, x3) + .4 if anchor == "start" else max(x2, x3) - .4
    return (f'<path d="M{x1:.2f},{y1:.2f} L{x2:.2f},{y2:.2f} H{x3:.2f}" {S} stroke-width="{w}"/>'
            f'<path d="{tip}" fill="currentColor"/>'
            f'<text x="{tx:.2f}" y="{y2-.7:.2f}" class="dim" text-anchor="{anchor}">{text}</text>')


def shaft(x0, yc, s=1.0, w=.3):
    seg = [(0, 3.4), (7, 5.0), (17, 6.6), (29, 5.0), (40, 3.4), (47, None)]
    P = lambda x, y: f"{x0+x*s:.3f},{yc+y*s:.3f}"
    top, bot = [], []
    for i in range(len(seg) - 1):
        (xa, r), xb = seg[i], seg[i + 1][0]
        top += [P(xa, -r), P(xb, -r)]
        bot += [P(xa, r), P(xb, r)]
    out = [f'<path d="M{" L".join(top + bot[::-1])}Z" {S} stroke-width="{w}"/>']
    for i in range(1, len(seg) - 1):
        r = max(seg[i][1], seg[i - 1][1])
        out.append(f'<path d="M{P(seg[i][0], -r)} L{P(seg[i][0], r)}" {S} stroke-width="{w*.65:.3f}"/>')
    out.append(f'<path d="M{P(-3, 0)} L{P(50, 0)}" {S} stroke-width="{w*.4:.3f}" {DASH}/>')
    cid = f"half{int(x0*10)}{int(yc*10)}"
    out.append(f'<clipPath id="{cid}"><path d="M{" L".join(bot)} L{P(47, 0)} L{P(0, 0)}Z"/></clipPath>')
    hatch = "".join(f"M{P(i*1.3, 8)} l{8*s:.3f},{-8*s:.3f} " for i in range(-6, 40))
    out.append(f'<path d="{hatch}" {S} stroke-width="{w*.33:.3f}" clip-path="url(#{cid})"/>')
    return "\n".join(out)


def ruler(x0, x1, y, up=True, labels=True):
    """Regla en mm reales: la tarjeta impresa mide de verdad."""
    d, t = [], []
    sgn = -1 if up else 1
    for i, x in enumerate(range(int(x0), int(x1) + 1)):
        L = 2.6 if i % 10 == 0 else 1.6 if i % 5 == 0 else 1.0
        d.append(f"M{x},{y} v{sgn*L}")
        if labels and i % 10 == 0:
            t.append(f'<text x="{x}" y="{y+sgn*3.9:.2f}" class="dim" text-anchor="middle">{i//10}</text>')
    return f'<path d="{" ".join(d)}" {S} stroke-width=".16"/>' + "".join(t)


def crosshair(x, y, r=1.6):
    return (f'<circle cx="{x}" cy="{y}" r="{r*.55:.2f}" {S} stroke-width=".14"/>'
            f'<path d="M{x-r},{y} H{x+r} M{x},{y-r} V{y+r}" {S} stroke-width=".14"/>')


# ---------- HTML ----------

BASE_CSS = """
  @page { size: 95mm 57mm; margin: 0; }
  :root{
    --navy:#202054; --navy-deep:#17173f; --line:#c9d2ea; --soft:#b3b8dc; --ink:#1f1f22; --mist:#f3f4f7;
    --steel:linear-gradient(90deg,#8e949b,#e9ecef 30%,#a9afb5 55%,#f4f6f7 75%,#8e949b);
    --bleed:3mm; --safe:5.5mm; --m:calc(var(--bleed) + var(--safe));
  }
  *{box-sizing:border-box;margin:0;padding:0}
  html,body{background:#d9dce1}
  body{font-family:"Open Sans",Helvetica,Arial,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  .card{width:95mm;height:57mm;position:relative;overflow:hidden;page-break-after:always;break-after:page}
  .draw{position:absolute;inset:0;width:95mm;height:57mm}
  .dim{font-family:"IBM Plex Mono",monospace;font-size:1.5px;letter-spacing:.04px;fill:currentColor}
  .abs{position:absolute}

  .lockup{display:flex;align-items:center;gap:3mm}
  .lockup img{height:11mm;width:auto;display:block}
  .word{font-family:"EB Garamond",Garamond,Georgia,serif;font-weight:500;font-size:4.3mm;line-height:1.06;letter-spacing:.02mm}
  .word span{display:block}
  .word span::first-letter{font-size:1.16em;font-weight:600}
  .caps{font-size:1.7mm;font-weight:700;letter-spacing:.24mm;text-transform:uppercase;line-height:1.75}
  .caps .sub{font-weight:600}
  .rule{display:block;width:9mm;height:.5mm;background:var(--steel);margin-bottom:2mm}

  .who h1{font-family:"EB Garamond",Garamond,Georgia,serif;font-weight:500;font-size:5mm;line-height:1.05;letter-spacing:.01mm}
  .who p{font-size:1.75mm;font-weight:700;letter-spacing:.26mm;text-transform:uppercase;margin-top:1.8mm}
  .data{display:grid;grid-template-columns:auto 1fr;align-items:baseline;column-gap:2.6mm;row-gap:1mm;font-size:1.95mm;line-height:1.3}
  .data dt{font-family:"IBM Plex Mono",monospace;font-weight:500;font-size:1.55mm}

  @media screen{
    body{display:flex;flex-wrap:wrap;gap:10mm;padding:12mm;justify-content:center}
    .card{box-shadow:0 2mm 6mm rgba(0,0,0,.22)}
  }
"""

FONTS = '<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;600&family=Open+Sans:wght@400;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">'

LOCKUP = '<div class="lockup"><img src="sussek-icono.png" alt=""><div class="word"><span>Sussek</span><span>Machine</span><span>Company</span></div></div>'


def data_block(p):
    return (f'<dl class="data"><dt>T</dt><dd>{p["tel"]}</dd><dt>E</dt><dd>{p["email"]}</dd>'
            f'<dt>W</dt><dd>{p["web"]}</dd><dt>A</dt><dd>{p["dir"]}</dd></dl>')


def who(p):
    return f'<div class="who"><h1>{p["nombre"]}</h1><p>{p["cargo"]}</p></div>'


def svg(inner):
    return f'<svg class="draw" viewBox="0 0 95 57">{inner}</svg>'


# Variante 1: plano azul con engrane / reverso blanco con eje y cuadro de rótulo
def v1(p):
    cx, cy, R = 70.5, 28.5, 17.5
    a = math.radians(222)
    x1, y1 = cx + R * math.cos(a), cy + R * math.sin(a)
    front = svg(gear(cx, cy, R) + leader(x1, y1, x1 - 4.2, 9.6, x1 - 18.5, "Ø35.000 ±0.005"))
    back = svg(f'<g opacity=".6">{shaft(55, 20, .66, .36)}{leader(55+23*.66, 20-6.6*.66, 55+23*.66+2.2, 11.4, 86.5, "Ø13.200 h6", anchor="end")}</g>')
    css = """
  .v1.front{background:radial-gradient(120% 140% at 78% 45%,#29296c 0%,var(--navy) 45%,var(--navy-deep) 100%);color:#fff}
  .v1.front .grid{position:absolute;inset:0;opacity:.08;background-image:linear-gradient(#fff .12mm,transparent .12mm),linear-gradient(90deg,#fff .12mm,transparent .12mm);background-size:4mm 4mm;background-position:1mm 1.5mm}
  .v1.front .draw{color:var(--line)}
  .v1.front .lockup{left:var(--m);top:17.5mm}
  .v1.front .caps{left:var(--m);bottom:var(--m)}
  .v1.front .caps .sub{color:var(--soft)}
  .v1.back{background:#fff;color:var(--navy)}
  .v1.back .draw{color:var(--navy)}
  .v1.back .who{left:var(--m);top:var(--m)}
  .v1.back .who p{color:#6b6f95}
  .v1.back .data{left:var(--m);bottom:calc(var(--m) + 9mm);color:var(--ink)}
  .v1.back .data dt{color:var(--navy)}
  .v1.back .block{left:var(--m);right:var(--m);bottom:var(--m);height:5.4mm;display:grid;grid-template-columns:auto 1fr 1fr 1fr auto;border:.25mm solid var(--navy);font-size:1.45mm;font-weight:700;letter-spacing:.2mm;text-transform:uppercase}
  .v1.back .block>*{display:flex;align-items:center;justify-content:center;padding:0 1.8mm;border-left:.18mm solid var(--navy)}
  .v1.back .block>:first-child{border-left:0;background:var(--navy);padding:0 1.3mm}
  .v1.back .block img{height:3.6mm}
  .v1.back .block .geo{background:var(--navy);color:#fff}
"""
    html = f"""
<section class="card front v1"><div class="grid"></div>{front}
  <div class="abs lockup-wrap">{LOCKUP}</div>
  <p class="abs caps"><i class="rule"></i>Precision Machining<br><span class="sub">Assembly · Engineering</span></p>
</section>
<section class="card back v1">{back}
  <div class="abs who-wrap">{who(p)}</div>
  <div class="abs data-wrap">{data_block(p)}</div>
  <div class="abs block"><div><img src="sussek-icono.png" alt=""></div><div>Machining</div><div>Assembly</div><div>Engineering</div><div class="geo">USA · MX · CN</div></div>
</section>"""
    return css, html


# Variante 2: frente claro con engrane gigante que sale por la esquina / reverso azul con eje
def v2(p):
    front = svg(f'<g opacity=".9">{gear(84, 49, 30, N=26, w=.34)}</g>' + crosshair(84, 49, 3))
    back = svg(f'<g opacity=".55">{shaft(57, 17.5, .6, .38)}</g>')
    css = """
  .v2.front{background:linear-gradient(135deg,#ffffff 0%,#f1f3f7 60%,#e6e9ef 100%);color:var(--navy)}
  .v2.front .draw{color:var(--navy)}
  .v2.front .lockup{left:var(--m);top:var(--m)}
  .v2.front .caps{left:var(--m);bottom:var(--m);color:var(--navy)}
  .v2.front .caps .sub{color:#7a7ea3}
  .v2.back{background:var(--navy);color:#fff}
  .v2.back .draw{color:var(--line)}
  .v2.back .edge{position:absolute;top:0;bottom:0;left:0;width:calc(var(--bleed) + 1.4mm);background-image:linear-gradient(180deg,#8e949b,#eef0f2 30%,#a9afb5 55%,#f4f6f7 75%,#8e949b)}
  .v2.back .who{left:var(--m);top:var(--m)}
  .v2.back .who p{color:var(--soft)}
  .v2.back .data{left:var(--m);bottom:calc(var(--m) + 6.5mm)}
  .v2.back .data dt{color:var(--soft)}
  .v2.back .foot{left:var(--m);right:var(--m);bottom:var(--m);padding-top:2mm;border-top:.2mm solid rgba(255,255,255,.22);display:flex;justify-content:space-between;font-size:1.5mm;font-weight:700;letter-spacing:.22mm;text-transform:uppercase;color:var(--soft)}
  .v2.back .foot b{color:#fff;font-weight:700}
"""
    html = f"""
<section class="card front v2">{front}
  <div class="abs lockup-wrap">{LOCKUP}</div>
  <p class="abs caps"><i class="rule"></i>Precision Machining<br><span class="sub">Assembly · Engineering</span></p>
</section>
<section class="card back v2"><div class="edge"></div>{back}
  <div class="abs who-wrap">{who(p)}</div>
  <div class="abs data-wrap">{data_block(p)}</div>
  <div class="abs foot"><span>Precision Machining · Assembly · Engineering</span><span><b>USA</b> · <b>MX</b> · <b>CN</b></span></div>
</section>"""
    return css, html


# Variante 3: regla milimétrica real + miras de centrado / reverso blanco con cuarto de engrane
def v3(p):
    marks = crosshair(11, 11) + crosshair(84, 11)
    front = svg(ruler(7.5, 87.5, 54, up=True) + marks)
    back = svg(f'<g opacity=".5">{gear(92, 3, 24, N=24, w=.34)}</g>' + ruler(7.5, 47.5, 3, up=False, labels=False))
    css = """
  .v3.front{background:radial-gradient(130% 120% at 50% 30%,#29296c 0%,var(--navy) 50%,var(--navy-deep) 100%);color:#fff}
  .v3.front .draw{color:var(--line)}
  .v3.front .lockup-wrap{left:0;right:0;top:12mm;display:flex;justify-content:center}
  .v3.front .lockup img{height:13mm}
  .v3.front .word{font-size:5mm}
  .v3.front .caps{left:0;right:0;top:36mm;text-align:center;color:#fff}
  .v3.front .caps .sub{color:var(--soft)}
  .v3.back{background:#fff;color:var(--navy)}
  .v3.back .draw{color:var(--navy)}
  .v3.back .who{left:var(--m);top:calc(var(--m) + 2mm)}
  .v3.back .who p{color:#6b6f95}
  .v3.back .data{left:var(--m);bottom:calc(var(--m) + 7mm);color:var(--ink)}
  .v3.back .data dt{color:var(--navy)}
  .v3.back .band{left:0;right:0;bottom:0;height:calc(var(--bleed) + 7.2mm);background:var(--navy);color:#fff;display:flex;align-items:flex-start;justify-content:space-between;padding:2.7mm var(--m) 0;font-size:1.5mm;font-weight:700;letter-spacing:.22mm;text-transform:uppercase}
  .v3.back .band::before{content:"";position:absolute;left:0;right:0;top:0;height:.5mm;background:var(--steel)}
  .v3.back .band span:last-child{color:var(--soft)}
"""
    html = f"""
<section class="card front v3">{front}
  <div class="abs lockup-wrap">{LOCKUP}</div>
  <p class="abs caps">Precision Machining <span class="sub">· Assembly · Engineering</span></p>
</section>
<section class="card back v3">{back}
  <div class="abs who-wrap">{who(p)}</div>
  <div class="abs data-wrap">{data_block(p)}</div>
  <div class="abs band"><span>Precision Machining · Assembly · Engineering</span><span>USA · MX · CN</span></div>
</section>"""
    return css, html


VARIANTES = {"variante-1-plano": v1, "variante-2-acero": v2, "variante-3-regla": v3}


def page(title, css, body):
    # los contenedores .abs envuelven a .lockup/.who/.data; las reglas de posición van al envoltorio
    for cls in ("lockup", "who", "data"):
        css = css.replace(f" .{cls}{{left", f" .{cls}-wrap{{left").replace(f" .{cls}{{right", f" .{cls}-wrap{{right")
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
    for name, fn in VARIANTES.items():
        css, body = fn(PERSONA)
        (here / f"{name}.html").write_text(page(f"Sussek · {name}", css, body))
        print("ok", name)
