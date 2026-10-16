"""Arma deck/v6/MUESTRA_v6.html con las láminas de muestra de estilo (s1..s3 JSON del scratchpad o de deck/v6/muestras)."""
import html, json, pathlib, sys
E = lambda s: html.escape(str(s))
ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "deck" / "v6" / "muestras"
OUT = ROOT / "deck" / "v6" / "MUESTRA_v6.html"

CSS = """
/* Láminas 16:9 sobre fondo gris; un solo mundo visual claro (papel blanco), elegido a propósito */
:root{--ink:#0B1220;--ink-2:#3B4556;--ink-3:#6B7484;--mark:#A3AAB5;--rule:#DDE2EA;--paper:#FFFFFF;--desk:#E9ECF1;
--blue:#1F4FD8;--blue-soft:#E8EEFC;--green:#127A5B;--green-soft:#E4F2EC;--font:"Inter",ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
body{background:var(--desk);color:var(--ink);font-family:var(--font);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:24px 48px}
.deck{max-width:1280px;margin:0 auto;display:flex;flex-direction:column;gap:24px}
.top{display:flex;flex-wrap:wrap;gap:6px 16px;align-items:baseline;color:var(--ink-2);font-size:14px}
.top b{color:var(--ink);font-size:16px}
.slide{container-type:inline-size;aspect-ratio:16/9;width:100%;background:var(--paper);border-radius:4px;box-shadow:0 1px 2px rgba(11,18,32,.08);position:relative;overflow:hidden}
.s{position:absolute;inset:0;padding:3.4cqi 4.2cqi 2.6cqi;display:flex;flex-direction:column;gap:1.1cqi}
.trk{position:absolute;top:1.9cqi;right:4.2cqi;font-size:1.0cqi;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);max-width:50cqi;text-align:right}
h2{margin:0;font-size:2.35cqi;line-height:1.18;font-weight:600;letter-spacing:-.012em;max-width:80cqi;text-wrap:balance}
.ctx{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1.6cqi;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:.7cqi 0}
.ctx div{font-size:1.02cqi;line-height:1.32;color:var(--ink-2)}
.ctx b{display:block;font-size:.82cqi;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);font-weight:600;margin-bottom:.2cqi}
.body{flex:1;min-height:0;display:grid;grid-template-columns:minmax(0,61fr) minmax(0,30fr);gap:2.4cqi}
.ex{min-height:0;display:flex;align-items:flex-start}
.ex svg{width:100%;height:auto;max-height:100%}
.side{display:flex;flex-direction:column;gap:.9cqi;min-width:0}
.side h4{margin:0;font-size:.82cqi;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);font-weight:600}
.side ol{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:.8cqi;counter-reset:l}
.side li{counter-increment:l;position:relative;padding-left:2cqi;font-size:1.1cqi;line-height:1.36;color:var(--ink-2)}
.side li::before{content:counter(l);position:absolute;left:0;top:.1cqi;width:1.35cqi;height:1.35cqi;border-radius:50%;background:var(--blue-soft);color:var(--blue);font-size:.8cqi;font-weight:700;display:flex;align-items:center;justify-content:center}
.root{border-left:.3cqi solid var(--ink);padding:.6cqi 1cqi;background:#F4F6F9;font-size:1.06cqi;line-height:1.34;color:var(--ink)}
.root b{display:block;font-size:.8cqi;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);margin-bottom:.25cqi}
.sw{display:flex;gap:1.3cqi;align-items:baseline;background:var(--blue-soft);padding:.8cqi 1.3cqi;font-size:1.25cqi;line-height:1.3;color:var(--ink)}
.sw b{flex:0 0 auto;font-size:.85cqi;letter-spacing:.12em;text-transform:uppercase;color:var(--blue)}
.src{font-size:.88cqi;color:var(--ink-3);display:flex;justify-content:space-between;gap:2cqi}
.note{font-size:13px;color:var(--ink-2);max-width:90ch}
"""

def slide(i, d):
    lec = "".join(f"<li>{E(x)}</li>" for x in d["lecturas"])
    return (f'<section class="slide" aria-label="Lámina {i}"><div class="s"><div class="trk">{E(d["seccion"])}</div>'
            f'<h2>{E(d["titulo"])}</h2>'
            f'<div class="ctx"><div><b>Qué se manda</b>{E(d["que"])}</div><div><b>Quién</b>{E(d["quien"])}</div><div><b>A quién</b>{E(d["a_quien"])}</div></div>'
            f'<div class="body"><div class="ex">{d["svg"]}</div><div class="side"><h4>Qué dice la gráfica</h4><ol>{lec}</ol>'
            f'<div class="root"><b>Causa raíz</b>{E(d["causa"])}</div></div></div>'
            f'<div class="sw"><b>So what</b><span>{E(d["sowhat"])}</span></div>'
            f'<div class="src"><span>{E(d["fuente"])}</span><span>{i}</span></div></div></section>')

def main():
    ds = [json.loads((SRC / f"s{i}.json").read_text(encoding="utf-8")) for i in (1, 2, 3) if (SRC / f"s{i}.json").exists()]
    o = ['<title>Muestras de estilo Braze v6</title>', '<meta name="claude:viewport-fit-sides" content="cover">',
         '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap">',
         f'<style>{CSS}</style><div class="deck"><div class="top"><b>Tres láminas de muestra de estilo</b><span>Panorama, diagnóstico y plan. Mismo marco para todo el deck: contexto arriba, gráfica a la izquierda, lecturas y causa a la derecha, so what abajo.</span></div>']
    o += [slide(i, d) for i, d in enumerate(ds, 1)]
    o.append("</div>")
    OUT.write_text("".join(o), encoding="utf-8")
    print(OUT, len(ds))

if __name__ == "__main__":
    main()
