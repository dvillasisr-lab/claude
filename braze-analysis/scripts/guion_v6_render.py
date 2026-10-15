"""Renderiza el guion fantasma v6 (deck/v6/GUION_v6.html) desde guion_v6.py."""
import html, pathlib
from guion_v6 import META, SECCIONES

E = lambda s: html.escape(str(s))
OUT = pathlib.Path(__file__).resolve().parent.parent / "deck" / "v6" / "GUION_v6.html"

CSS = """
/* Guion fantasma: documento de trabajo; columna de lectura con secciones y filas de lámina */
:root{
  --ink:#0B1220; --ink-2:#3B4556; --ink-3:#6B7484; --rule:#DDE2EA; --paper:#FFFFFF; --wash:#F3F6FA;
  --blue:#1F4FD8; --blue-soft:#E7EDFC; --green:#127A5B; --green-soft:#E3F3EC; --gray-soft:#EEF0F3;
  --font:"Inter",ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){color-scheme:dark;
  --ink:#EEF1F6; --ink-2:#C2C9D4; --ink-3:#8D96A5; --rule:#2A3242; --paper:#0E131C; --wash:#151C28;
  --blue:#7FA1FF; --blue-soft:#1A2848; --green:#4CC59A; --green-soft:#12322A; --gray-soft:#1C2330;}}
:root[data-theme="dark"]{color-scheme:dark;
  --ink:#EEF1F6; --ink-2:#C2C9D4; --ink-3:#8D96A5; --rule:#2A3242; --paper:#0E131C; --wash:#151C28;
  --blue:#7FA1FF; --blue-soft:#1A2848; --green:#4CC59A; --green-soft:#12322A; --gray-soft:#1C2330;}
body{background:var(--paper);color:var(--ink);font-family:var(--font);font-size:15px;line-height:1.5;
  padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:28px 64px}
.wrap{max-width:1080px;margin:0 auto;display:flex;flex-direction:column;gap:28px}
h1{font-size:30px;line-height:1.15;margin:0;letter-spacing:-.02em;text-wrap:balance}
.eyebrow{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3);font-weight:600}
.lead{font-size:18px;color:var(--ink-2);max-width:70ch;margin:0}
.box{background:var(--wash);border-radius:8px;padding:18px 20px;display:flex;flex-direction:column;gap:10px}
.box h2{font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);margin:0}
.scqa{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
.scqa div b{display:block;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--blue);margin-bottom:4px}
.scqa div{font-size:14px;color:var(--ink-2)}
.method{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;font-size:14px;color:var(--ink-2)}
.method b{color:var(--ink)}
.toc{display:flex;flex-wrap:wrap;gap:6px}
.toc a{font-size:13px;color:var(--ink);text-decoration:none;border:1px solid var(--rule);border-radius:999px;padding:3px 10px}
.toc a:hover,.toc a:focus-visible{border-color:var(--blue);outline:none}
.sec{display:flex;flex-direction:column;gap:12px;scroll-margin-top:16px}
.sec-h{display:flex;gap:14px;align-items:baseline;border-bottom:2px solid var(--ink);padding-bottom:8px}
.sec-h .n{font-size:13px;font-weight:700;color:var(--blue);min-width:2.2em}
.sec-h h2{margin:0;font-size:21px;letter-spacing:-.01em}
.sec-arg{margin:0;color:var(--ink-2);font-size:15px;max-width:80ch}
.sub{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);font-weight:600;margin-top:6px}
.sl{display:grid;grid-template-columns:3.2em minmax(0,1fr);gap:4px 12px;padding:10px 0;border-bottom:1px solid var(--rule)}
.sl .no{font-variant-numeric:tabular-nums;color:var(--ink-3);font-size:13px;padding-top:2px}
.sl .t{font-weight:600;font-size:16px;line-height:1.35;text-wrap:balance}
.sl .meta{grid-column:2;display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.chip{font-size:11.5px;border-radius:4px;padding:1px 7px;background:var(--gray-soft);color:var(--ink-2)}
.chip.new{background:var(--green-soft);color:var(--green);font-weight:600}
.chip.fix{background:var(--blue-soft);color:var(--blue);font-weight:600}
.sl .viz{grid-column:2;font-size:13.5px;color:var(--ink-2)}
.sl .viz b{color:var(--ink);font-weight:600}
.sl ul{grid-column:2;margin:2px 0 0;padding-left:18px;font-size:13.5px;color:var(--ink-2)}
.sl ul li{margin:1px 0}
.sl .sw{grid-column:2;font-size:13.5px;color:var(--ink)}
.sl .sw b{color:var(--blue);font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;margin-right:6px}
.sl.close{background:var(--blue-soft);border-radius:6px;padding:10px 10px;border-bottom:0}
.open{font-size:14px;color:var(--ink-2)} .open li{margin:4px 0}
@media (max-width:720px){.scqa,.method{grid-template-columns:1fr 1fr}}
@media (max-width:440px){.scqa,.method{grid-template-columns:1fr}.sl{grid-template-columns:2.4em minmax(0,1fr)}}
"""

def slide(n, s):
    cls = "sl close" if s.get("cierre") else "sl"
    chips = [f'<span class="chip">{E(s.get("tipo","Diagnóstico"))}</span>']
    if s.get("estado") == "nuevo": chips.append('<span class="chip new">Nuevo</span>')
    if s.get("estado") == "rehacer": chips.append('<span class="chip fix">Rehacer</span>')
    o = [f'<div class="{cls}"><div class="no">{n}</div><div class="t">{E(s["t"])}</div>',
         f'<div class="meta">{"".join(chips)}</div>']
    if s.get("viz"): o.append(f'<div class="viz"><b>Gráfica:</b> {E(s["viz"])}</div>')
    if s.get("h"): o.append("<ul>" + "".join(f"<li>{E(x)}</li>" for x in s["h"]) + "</ul>")
    if s.get("sw"): o.append(f'<div class="sw"><b>So what</b>{E(s["sw"])}</div>')
    o.append("</div>")
    return "".join(o)

def main():
    o = ['<title>Guion Braze Kueski v6</title>',
         '<meta name="claude:viewport-fit-sides" content="cover">',
         '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap">',
         f'<style>{CSS}</style><div class="wrap">']
    m = META
    o.append(f'<header style="display:flex;flex-direction:column;gap:10px"><div class="eyebrow">{E(m["eyebrow"])}</div><h1>{E(m["idea"])}</h1><p class="lead">{E(m["lead"])}</p></header>')
    o.append('<section class="box"><h2>La historia en cuatro frases</h2><div class="scqa">' + "".join(f'<div><b>{E(k)}</b>{E(v)}</div>' for k, v in m["scqa"]) + '</div></section>')
    o.append('<section class="box"><h2>Cómo está armado</h2><div class="method">' + "".join(f'<div><b>{E(k)}.</b> {E(v)}</div>' for k, v in m["metodo"]) + '</div></section>')
    o.append('<nav class="toc" aria-label="Secciones">' + "".join(f'<a href="#s{i}">{E(sec["n"])} {E(sec["nombre"])}</a>' for i, sec in enumerate(SECCIONES)) + '</nav>')
    n = 0
    for i, sec in enumerate(SECCIONES):
        o.append(f'<section class="sec" id="s{i}"><div class="sec-h"><span class="n">{E(sec["n"])}</span><h2>{E(sec["nombre"])}</h2></div><p class="sec-arg">{E(sec["arg"])}</p>')
        for sub in sec["subs"]:
            if sub.get("nombre"): o.append(f'<div class="sub">{E(sub["nombre"])}</div>')
            for s in sub["sl"]:
                n += 1; o.append(slide(n, s))
        o.append("</section>")
    if m.get("abiertas"):
        o.append('<section class="box"><h2>Lo que necesito que decidas</h2><ol class="open">' + "".join(f"<li>{E(x)}</li>" for x in m["abiertas"]) + "</ol></section>")
    o.append("</div>")
    OUT.write_text("".join(o), encoding="utf-8")
    print(OUT, n, "láminas")

if __name__ == "__main__":
    main()
