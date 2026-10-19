"""Arma deck/v6/DECK_v6.html con todas las láminas en deck/v6/slides/**/NNN*.json (ordenadas por "n").
Uso: python3 deck_v6_render.py                      -> deck completo
     python3 deck_v6_render.py --solo RUTA.json OUT.html   -> una lámina sola (para revisarla con Playwright)
Tipos ("kind"): portada, divisor, grafica (por defecto), html (tabla, checklist, gantt, cifra grande en "html"), cierre.
"""
import html, json, pathlib, sys
from muestra_v6_render import CSS as BASE_CSS
E = lambda s: html.escape(str(s))
ROOT = pathlib.Path(__file__).resolve().parent.parent
SL = ROOT / "deck" / "v6" / "slides"
OUT = ROOT / "deck" / "v6" / "DECK_v6.html"

CSS = BASE_CSS + """
.slide.portada .s{justify-content:center;gap:2cqi;background:#FFFFFF}
.portada .brand{font-size:1.1cqi;letter-spacing:.14em;text-transform:uppercase;color:var(--blue);font-weight:700}
.portada h1{margin:0;font-size:4.6cqi;line-height:1.05;letter-spacing:-.02em;max-width:70cqi}
.portada .sub{font-size:1.7cqi;color:var(--ink-2);max-width:70cqi}
.portada .meta{font-size:1.1cqi;color:var(--ink-3)}
.slide.divisor{background:var(--blue)}
.divisor .s{justify-content:center;gap:1.6cqi;color:#FFFFFF}
.divisor .acto{font-size:1.2cqi;letter-spacing:.16em;text-transform:uppercase;opacity:.8;font-weight:600}
.divisor h2{font-size:3.6cqi;color:#FFFFFF;max-width:80cqi;line-height:1.12}
.divisor .sub{font-size:1.6cqi;max-width:70cqi;opacity:.92;line-height:1.35}
.divisor .src{color:rgba(255,255,255,.7)}
.body.full{grid-template-columns:minmax(0,1fr)}
.hx{min-height:0;height:100%;overflow:hidden;font-size:1.02cqi;line-height:1.35;color:var(--ink-2)}
.hx table{width:100%;border-collapse:collapse;font-size:1cqi;line-height:1.3}
.hx th{text-align:left;font-weight:600;color:var(--ink-3);font-size:.82cqi;letter-spacing:.06em;text-transform:uppercase;border-bottom:1.5px solid var(--ink);padding:.4cqi .7cqi .4cqi 0;vertical-align:bottom}
.hx td{border-bottom:1px solid var(--rule);padding:.42cqi .7cqi .42cqi 0;vertical-align:top;color:var(--ink)}
.hx td.num,.hx th.num{text-align:right;font-variant-numeric:tabular-nums}
.hx .big{font-size:4cqi;font-weight:700;letter-spacing:-.02em;color:var(--ink);line-height:1}
.hx .bigl{font-size:1.05cqi;color:var(--ink-2);margin-top:.4cqi}
.cierre .grid3{flex:1;min-height:0;display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr) minmax(0,1fr);gap:2.2cqi}
.cierre h4{margin:0 0 .5cqi;font-size:.82cqi;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);font-weight:600}
.cierre ol,.cierre ul{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:.55cqi}
.cierre li{font-size:.98cqi;line-height:1.32;color:var(--ink-2);position:relative;padding-left:1.9cqi}
.cierre ol{counter-reset:p}.cierre ol li{counter-increment:p}
.cierre ol li::before{content:counter(p);position:absolute;left:0;top:.1cqi;width:1.35cqi;height:1.35cqi;border-radius:50%;background:var(--blue-soft);color:var(--blue);font-size:.8cqi;font-weight:700;display:flex;align-items:center;justify-content:center}
.cierre ol li:last-child{color:var(--ink);font-weight:600}
.cierre ol li:last-child::before{background:var(--ink);color:#fff}
.cierre .hip li{padding-left:2.4cqi}
.cierre .hip li b{position:absolute;left:0;top:.05cqi;font-size:.8cqi;color:var(--blue);background:var(--blue-soft);border-radius:.25cqi;padding:0 .35cqi}
.cierre .como li::before{content:"";position:absolute;left:.3cqi;top:.55cqi;width:.6cqi;height:.6cqi;background:var(--green);border-radius:1px}
.cierre .imp{margin-top:.9cqi;background:var(--green-soft);padding:.6cqi .9cqi;font-size:.98cqi;line-height:1.32;color:var(--ink)}
.cierre .imp b{display:block;font-size:.8cqi;letter-spacing:.1em;text-transform:uppercase;color:var(--green);margin-bottom:.2cqi}
@media (max-width:720px){
 .portada h1{font-size:30px}.portada .sub{font-size:16px}.portada .brand,.portada .meta{font-size:12px}
 .divisor h2{font-size:24px}.divisor .sub{font-size:15px}.divisor .acto{font-size:12px}
 .cierre .grid3{grid-template-columns:1fr;gap:14px}.cierre li,.cierre .imp{font-size:14px}.cierre h4{font-size:11px}
 .hx{font-size:14px;overflow:visible}.hx table{font-size:13px}.hx th{font-size:11px}.hx .big{font-size:34px}.hx .bigl{font-size:14px}
}
"""

def ctx(d):
    if not any(d.get(k) for k in ("que", "quien", "a_quien")):
        return ""
    return (f'<div class="ctx"><div><b>Qué se manda</b>{E(d.get("que",""))}</div><div><b>Quién</b>{E(d.get("quien",""))}</div>'
            f'<div><b>A quién</b>{E(d.get("a_quien",""))}</div></div>')

def foot(d, i):
    sw = f'<div class="sw"><b>So what</b><span>{E(d["sowhat"])}</span></div>' if d.get("sowhat") else ""
    return sw + f'<div class="src"><span>{E(d.get("fuente",""))}</span><span>{i}</span></div>'

def side(d):
    if not d.get("lecturas") and not d.get("causa"):
        return ""
    lec = "".join(f"<li>{E(x)}</li>" for x in d.get("lecturas", []))
    root = f'<div class="root"><b>Causa raíz</b>{E(d["causa"])}</div>' if d.get("causa") else ""
    return f'<div class="side"><h4>Qué dice la gráfica</h4><ol>{lec}</ol>{root}</div>'

def slide(d, i):
    k = d.get("kind", "grafica")
    if k == "portada":
        return (f'<section class="slide portada" id="l{i}"><div class="s"><div class="brand">Kueski · Braze</div><h1>{E(d["titulo"])}</h1>'
                f'<div class="sub">{E(d.get("subtitulo",""))}</div><div class="meta">{E(d.get("meta",""))}</div></div></section>')
    if k == "divisor":
        return (f'<section class="slide divisor" id="l{i}"><div class="s"><div class="acto">{E(d.get("acto",""))}</div><h2>{E(d["titulo"])}</h2>'
                f'<div class="sub">{E(d.get("subtitulo",""))}</div><div class="src"><span></span><span>{i}</span></div></div></section>')
    if k == "cierre":
        pq = "".join(f"<li>{E(x)}</li>" for x in d.get("porques", []))
        hp = d.get("hipotesis", {})
        hip = "".join(f'<li><b>{L}</b>{E(hp[L])}</li>' for L in ("A", "O", "G") if hp.get(L))
        como = "".join(f"<li>{E(x)}</li>" for x in d.get("como", []))
        imp = f'<div class="imp"><b>Si lo resolvemos</b>{E(d["impacto"])}</div>' if d.get("impacto") else ""
        return (f'<section class="slide cierre" id="l{i}"><div class="s"><h2>{E(d["titulo"])}</h2>'
                f'<div class="grid3"><div><h4>Por qué pasa, de lo visible a la causa</h4><ol>{pq}</ol></div>'
                f'<div><h4>Hipótesis: A analítica, O operativa, G gobierno</h4><ul class="hip">{hip}</ul></div>'
                f'<div><h4>Cómo lo resolvemos</h4><ul class="como">{como}</ul>{imp}</div></div>{foot(d, i)}</div></section>')
    body_l = d["svg"] if k == "grafica" else f'<div class="hx">{d.get("html","")}</div>'
    sd = side(d)
    full = " full" if (not sd or d.get("ancho_completo")) else ""
    return (f'<section class="slide" id="l{i}"><div class="s"><h2>{E(d["titulo"])}</h2>{ctx(d)}'
            f'<div class="body{full}"><div class="ex">{body_l}</div>{"" if full else sd}</div>{foot(d, i)}</div></section>')

def page(ds, title="Braze en Kueski · Deck v6", note=""):
    o = [f'<title>{E(title)}</title>', '<meta name="claude:viewport-fit-sides" content="cover">',
         '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap">',
         f'<style>{CSS}</style><div class="deck">']
    if note:
        o.append(f'<div class="top"><b>{E(title)}</b><span>{E(note)}</span></div>')
    o += [slide(d, d.get("n", i)) for i, d in enumerate(ds, 1)]
    o.append("</div>")
    return "".join(o)

def load_all():
    ds = []
    for p in sorted(SL.rglob("*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            print("ERROR", p, e); continue
        if isinstance(d, dict) and "n" in d:
            ds.append(d)
    return sorted(ds, key=lambda d: (d["n"], d.get("sub", 0)))

if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "--solo":
        d = json.loads(pathlib.Path(sys.argv[2]).read_text(encoding="utf-8"))
        pathlib.Path(sys.argv[3]).write_text(page([d], "Revisión"), encoding="utf-8"); print(sys.argv[3])
    else:
        ds = load_all()
        OUT.write_text(page(ds, "Braze en Kueski · Deck v6", f"{len(ds)} láminas. Se publica sección por sección conforme se terminan."), encoding="utf-8")
        print(OUT, len(ds))
