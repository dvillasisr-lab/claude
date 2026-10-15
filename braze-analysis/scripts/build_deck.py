# -*- coding: utf-8 -*-
"""Genera el deck de la auditoría de Braze en dos formatos a partir de deck_content.py:

  deck/BRAZE_KUESKI_DECK.html   (versión web, un slide por pantalla, 16:9)
  deck/BRAZE_KUESKI_DECK.pptx   (PowerPoint con gráficas nativas)

Uso: python3 scripts/build_deck.py [--html solo] [--pptx solo]
"""
import html as H
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from deck_content import SLIDES  # noqa: E402

OUT = os.path.join(os.path.dirname(HERE), "deck")
os.makedirs(OUT, exist_ok=True)

ACCENT = "1F4FD8"
ACCENT2 = "7A9BF0"
GRAY = "A3AAB5"
GRAY2 = "D5D9E0"
INK = "1A1D24"
INK2 = "5B6270"
RED = "B5342B"
GREEN = "2C7A4B"
AMBER = "B8860B"

# ----------------------------------------------------------------------------
# utilidades
# ----------------------------------------------------------------------------

def fmtv(v, fmt):
    if v is None:
        return ""
    if fmt == "pct0":
        return f"{v:.0f} %"
    if fmt == "pct1":
        return f"{v:.1f} %"
    if fmt == "pct2":
        return f"{v:.2f} %"
    if fmt == "M":
        return f"{v:.1f} M"
    if fmt == "MXN":
        return f"{v:.2f} M"
    if fmt == "int":
        return f"{v:.0f}"
    if fmt == "x1":
        return f"{v:.1f}"
    if fmt == "x2":
        return f"{v:.2f}"
    return f"{v}"


def status_class(s):
    s = (s or "").lower()
    if s.startswith("cumple"):
        return "ok"
    if s.startswith("debajo por poco"):
        return "warn"
    if s.startswith("debajo"):
        return "bad"
    if s in ("apagar", "confirmar apagado", "apagar y confirmar"):
        return "bad"
    if s in ("rehacer", "rehacer o re-segmentar", "bajar frecuencia"):
        return "warn"
    if s in ("proteger", "escalar"):
        return "ok"
    return ""


def section_titles():
    out = []
    for i, s in enumerate(SLIDES):
        if s["kind"] == "section":
            out.append((i, s))
    return out


# ----------------------------------------------------------------------------
# SVG
# ----------------------------------------------------------------------------

def esc(t):
    return H.escape(str(t), quote=True).replace(" %", "\u00a0%")


def svg_hbar(ex, W=760, highlight_color="#" + ACCENT):
    cats, vals = ex["cats"], ex["vals"]
    fmt = ex.get("fmt", "")
    notes = ex.get("notes")
    hl = set(ex.get("highlight", []))
    n = len(cats)
    rowh = 58 if n <= 5 else (48 if n <= 7 else 38)
    top = 28 if ex.get("label") else 8
    labw = 250
    noteh = 14 if notes else 0
    Hh = top + n * (rowh + noteh) + 10
    vmax = max(vals) if max(vals) > 0 else 1
    barmax = W - labw - 110
    o = [f'<svg viewBox="0 0 {W} {Hh}" class="chart" role="img" aria-label="{esc(ex.get("label",""))}">']
    if ex.get("label"):
        o.append(f'<text x="0" y="16" class="c-lab">{esc(ex["label"])}</text>')
    y = top
    for i, (c, v) in enumerate(zip(cats, vals)):
        col = highlight_color if i in hl else "#" + GRAY
        w = max(2, v / vmax * barmax)
        bh = rowh - 14
        o.append(f'<text x="{labw-10}" y="{y+bh/2+5}" text-anchor="end" class="c-cat">{esc(c)}</text>')
        o.append(f'<rect x="{labw}" y="{y}" width="{w:.1f}" height="{bh}" rx="3" fill="{col}"/>')
        o.append(f'<text x="{labw+w+8:.1f}" y="{y+bh/2+5}" class="c-val">{esc(fmtv(v, fmt))}</text>')
        if notes:
            o.append(f'<text x="{labw}" y="{y+bh+13}" class="c-note">{esc(notes[i])}</text>')
        y += rowh + noteh
    o.append("</svg>")
    return "".join(o)


def svg_hbar2(ex, W=760):
    cats, series = ex["cats"], ex["series"]
    fmt = ex.get("fmt", "")
    hl = set(ex.get("highlight", []))
    n, k = len(cats), len(series)
    bh = (18 if n <= 5 else 14) if k > 1 else 30
    gap = 3
    group = k * bh + (k - 1) * gap
    rowh = group + 18
    top = 30
    labw = 220
    Hh = top + n * rowh + 10
    vmax = ex.get("max") or max(max(s[1]) for s in series)
    barmax = W - labw - 110
    cols = ["#" + ACCENT, "#" + GRAY, "#" + GRAY2][:k] if k > 1 else None
    o = [f'<svg viewBox="0 0 {W} {Hh}" class="chart" role="img" preserveAspectRatio="xMinYMin meet">']
    # leyenda
    x = 0
    if k > 1:
        for j, (name, _) in enumerate(series):
            o.append(f'<rect x="{x}" y="6" width="12" height="12" rx="2" fill="{cols[j]}"/><text x="{x+16}" y="17" class="c-note">{esc(name)}</text>')
            x += 16 + 7 * len(name) + 24
    else:
        o.append(f'<text x="0" y="16" class="c-lab">{esc(series[0][0])}</text>')
    y = top
    for i, c in enumerate(cats):
        o.append(f'<text x="{labw-10}" y="{y+group/2+5}" text-anchor="end" class="c-cat">{esc(c)}</text>')
        for j, (name, vals) in enumerate(series):
            v = vals[i]
            w = max(1.5, v / vmax * barmax)
            if k > 1:
                col = cols[j]
            else:
                col = "#" + ACCENT if i in hl else "#" + GRAY
            yy = y + j * (bh + gap)
            o.append(f'<rect x="{labw}" y="{yy}" width="{w:.1f}" height="{bh}" rx="2" fill="{col}"/>')
            o.append(f'<text x="{labw+w+6:.1f}" y="{yy+bh/2+4}" class="c-val{" c-sm" if k>1 else ""}">{esc(fmtv(v, fmt))}</text>')
        y += rowh
    o.append("</svg>")
    return "".join(o)


def _col_panel(o, x0, y0, w, h, cats, vals, hl, fmt, title, kind="col", ymin=None, ymax=None, ref=None, labels=None, ticks=4):
    n = len(cats)
    lab = set(range(n)) if labels is None else set(labels)
    o.append(f'<text x="{x0}" y="{y0-8}" class="c-lab">{esc(title)}</text>')
    lo = 0 if ymin is None else ymin
    hi = (max(vals) * 1.12) if ymax is None else ymax
    nlo, nhi, step = _nice_axis(lo, hi, ticks)
    if ymin is None:
        lo = min(0, nlo) if nlo >= 0 else nlo
    if ymax is None:
        hi = nhi
    if hi <= lo:
        hi = lo + 1
    def Y(v):
        return y0 + h - (v - lo) / (hi - lo) * h
    # grid con ticks redondos
    for gv in _ticks(lo if ymin is None else nlo, hi, step):
        if gv < lo - 1e-9 or gv > hi + 1e-9:
            continue
        yy = Y(gv)
        o.append(f'<line x1="{x0}" y1="{yy:.1f}" x2="{x0+w}" y2="{yy:.1f}" class="c-grid"/>')
        o.append(f'<text x="{x0-6}" y="{yy+4:.1f}" text-anchor="end" class="c-note">{esc(fmtv(gv, fmt))}</text>')
    if ref:
        rv, rl = ref
        yy = Y(rv)
        o.append(f'<line x1="{x0}" y1="{yy:.1f}" x2="{x0+w}" y2="{yy:.1f}" class="c-ref"/><text x="{x0+w}" y="{yy-4:.1f}" text-anchor="end" class="c-note">{esc(rl)}</text>')
    slot = w / n
    if kind == "col":
        bw = slot * 0.6
        for i, (c, v) in enumerate(zip(cats, vals)):
            x = x0 + i * slot + (slot - bw) / 2
            col = "#" + ACCENT if i in hl else "#" + GRAY
            o.append(f'<rect x="{x:.1f}" y="{Y(v):.1f}" width="{bw:.1f}" height="{y0+h-Y(v):.1f}" rx="3" fill="{col}"/>')
            if i in lab:
                o.append(f'<text x="{x+bw/2:.1f}" y="{Y(v)-5:.1f}" text-anchor="middle" class="c-val c-sm">{esc(fmtv(v, fmt))}</text>')
            o.append(f'<text x="{x+bw/2:.1f}" y="{y0+h+16}" text-anchor="middle" class="c-cat">{esc(c)}</text>')
    else:
        pts = []
        for i, v in enumerate(vals):
            x = x0 + i * slot + slot / 2
            pts.append((x, Y(v)))
        d = " ".join(f'{"M" if i==0 else "L"}{x:.1f},{y:.1f}' for i, (x, y) in enumerate(pts))
        o.append(f'<path d="{d}" fill="none" stroke="#{ACCENT}" stroke-width="2.5"/>')
        for i, ((x, y), v) in enumerate(zip(pts, vals)):
            col = "#" + ACCENT
            r = 6 if i in hl else 4
            o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{col}" stroke="#fff" stroke-width="2"/>')
            if i in lab:
                o.append(f'<text x="{x:.1f}" y="{y-10:.1f}" text-anchor="middle" class="c-val c-sm{" c-hl" if i in hl else ""}">{esc(fmtv(v, fmt))}</text>')
            o.append(f'<text x="{x:.1f}" y="{y0+h+16}" text-anchor="middle" class="c-cat">{esc(cats[i])}</text>')


def svg_colline(ex, W=760):
    cats = ex["cats"]
    hl = set(ex.get("highlight", []))
    Hh = 400
    o = [f'<svg viewBox="0 0 {W} {Hh}" class="chart" role="img" preserveAspectRatio="xMinYMin meet">']
    name1, v1 = ex["cols"]
    name2, v2 = ex["line"]
    f1 = "M" if "(M)" in name1 else ""
    f2 = "pct2" if "%" in name2 else "pct1"
    _col_panel(o, 60, 30, W - 70, 135, cats, v1, hl, f1, name1, "col")
    _col_panel(o, 60, 236, W - 70, 135, cats, v2, hl, f2, name2, "line")
    o.append("</svg>")
    return "".join(o)


def svg_line(ex, W=760):
    cats = ex["cats"]
    hl = set(ex.get("highlight", []))
    name, vals = ex["series"][0]
    Hh = 330
    o = [f'<svg viewBox="0 0 {W} {Hh}" class="chart" role="img" preserveAspectRatio="xMinYMin meet">']
    _col_panel(o, 60, 30, W - 70, 260, cats, vals, hl, "pct0", name, "line", ex.get("ymin"), ex.get("ymax"), ex.get("ref"))
    o.append("</svg>")
    return "".join(o)


def svg_waterfall(ex, W=760):
    cats, vals = ex["cats"], ex["vals"]
    fmt = ex.get("fmt", "")
    n = len(cats)
    Hh = 360
    x0, y0, w, h = 60, 40, W - 80, 240
    o = [f'<svg viewBox="0 0 {W} {Hh}" class="chart" role="img" preserveAspectRatio="xMinYMin meet">']
    o.append(f'<text x="{x0}" y="22" class="c-lab">{esc(ex.get("label",""))}</text>')
    hi = max(vals) * 1.1
    def Y(v):
        return y0 + h - v / hi * h
    slot = w / n
    bw = slot * 0.55
    run = 0
    for i, (c, v) in enumerate(zip(cats, vals)):
        x = x0 + i * slot + (slot - bw) / 2
        if i == 0 or i == n - 1:
            top, bot, col = v, 0, "#" + (ACCENT if i == n - 1 else INK2)
            run = v
        else:
            top, bot = run, run + v
            col = "#" + RED
            run = run + v
            o.append(f'<line x1="{x-slot*0.225:.1f}" y1="{Y(top):.1f}" x2="{x:.1f}" y2="{Y(top):.1f}" class="c-grid"/>')
        yt, yb = Y(max(top, bot)), Y(min(top, bot))
        o.append(f'<rect x="{x:.1f}" y="{yt:.1f}" width="{bw:.1f}" height="{max(2, yb-yt):.1f}" rx="3" fill="{col}"/>')
        lab = fmtv(abs(v), fmt) if i not in (0, n - 1) else fmtv(v, fmt)
        if i not in (0, n - 1):
            lab = "−" + lab
        if ex.get("sublabels") and ex["sublabels"][i]:
            lab = f'{lab} · {ex["sublabels"][i]}'
        o.append(f'<text x="{x+bw/2:.1f}" y="{yt-6:.1f}" text-anchor="middle" class="c-val c-sm">{esc(lab)}</text>')
        # categoría en dos líneas si es larga
        parts = c.split(" (")
        o.append(f'<text x="{x+bw/2:.1f}" y="{y0+h+18}" text-anchor="middle" class="c-cat">{esc(parts[0])}</text>')
        if len(parts) > 1:
            o.append(f'<text x="{x+bw/2:.1f}" y="{y0+h+34}" text-anchor="middle" class="c-note">({esc(parts[1])}</text>')
    if ex.get("note"):
        o.append(f'<text x="{x0+w}" y="{y0+h+60}" text-anchor="end" class="c-note">{esc(ex["note"])}</text>')
    o.append("</svg>")
    return "".join(o)


def html_table(ex):
    head, rows = ex["head"], ex["rows"]
    sc = ex.get("status_col")
    scs = sc if isinstance(sc, list) else ([sc] if sc is not None else [])
    hr = set(ex.get("highlight_rows", []))
    cls = "tbl" + (" tbl-sm" if (ex.get("small") or len(rows) >= 8) else "")
    o = [f'<div class="tblwrap"><table class="{cls}"><thead><tr>']
    for h in head:
        o.append(f"<th>{esc(h)}</th>")
    o.append("</tr></thead><tbody>")
    for ri, r in enumerate(rows):
        o.append(f'<tr{" class=\"hl\"" if ri in hr else ""}>')
        for ci, c in enumerate(r):
            if ci in scs:
                k = status_class(c)
                o.append(f'<td><span class="pill {k}">{esc(c)}</span></td>')
            else:
                o.append(f"<td>{esc(c)}</td>")
        o.append("</tr>")
    o.append("</tbody></table></div>")
    return "".join(o)


def html_stats(ex):
    o = ['<div class="stats">']
    for big, lab, sub in ex["items"]:
        o.append(f'<div class="stat"><div class="s-big">{esc(big)}</div><div class="s-lab">{esc(lab)}</div><div class="s-sub">{esc(sub)}</div></div>')
    o.append("</div>")
    return "".join(o)


def html_rules(ex):
    o = ['<ol class="rules">']
    for r in ex["items"]:
        o.append(f"<li>{esc(r)}</li>")
    o.append("</ol>")
    return "".join(o)


def html_gantt(ex):
    cols = ex["cols"]
    o = ['<div class="tblwrap"><table class="tbl tbl-sm gantt"><thead><tr><th>Qué</th>']
    for c in cols:
        o.append(f"<th class=\"gc\">{esc(c)}</th>")
    o.append("<th>Quién</th></tr></thead><tbody>")
    for name, cells, who in ex["rows"]:
        o.append(f"<tr><td>{esc(name)}</td>")
        for v in cells:
            o.append(f'<td class="gc"><span class="gbar{" on" if v else ""}"></span></td>')
        o.append(f"<td class=\"who\">{esc(who)}</td></tr>")
    o.append("</tbody></table></div>")
    return "".join(o)


# ---- Gráficas multivariable (SVG) --------------------------------------------
PAL = ["#" + ACCENT, "#B5342B", "#1F9E89", "#A8720F", "#7C5CC4"]


def _mix(a, b, t):
    a = a.lstrip("#"); b = b.lstrip("#")
    return "#" + "".join(f"{int(int(a[i:i+2],16)*(1-t)+int(b[i:i+2],16)*t):02X}" for i in (0, 2, 4))


def _nice_axis(lo, hi, nticks=4):
    """Devuelve (lo, hi, paso) con ticks redondos (1, 2, 2.5, 5 x 10^k) que cubren [lo, hi]."""
    import math
    if hi <= lo:
        hi = lo + 1
    raw = (hi - lo) / max(1, nticks - 1)
    mag = 10 ** math.floor(math.log10(raw))
    step = next(s * mag for s in (1, 2, 2.5, 5, 10) if s * mag >= raw)
    lo2 = math.floor(lo / step) * step
    hi2 = math.ceil(hi / step) * step
    if hi2 <= lo2:
        hi2 = lo2 + step
    return lo2, hi2, step


def _ticks(lo, hi, step):
    t, out = lo, []
    while t <= hi + step * 1e-6:
        out.append(round(t, 10))
        t += step
    return out


def _spread(items, gap, lo, hi):
    """items: lista de [y, ...]. Separa las y al menos gap, dentro de [lo, hi]. Devuelve lista ordenada."""
    items = sorted(items, key=lambda q: q[0])
    for i in range(1, len(items)):
        if items[i][0] - items[i - 1][0] < gap:
            items[i][0] = items[i - 1][0] + gap
    over = items[-1][0] - hi if items else 0
    if over > 0:
        for q in items:
            q[0] -= over
        for i in range(len(items) - 2, -1, -1):
            if items[i + 1][0] - items[i][0] < gap:
                items[i][0] = items[i + 1][0] - gap
    return items


def _ramp(n, base=None):
    """Rampa secuencial de n pasos, claro a oscuro, sobre el azul principal."""
    base = base or PAL[0]
    if n == 1:
        return [base]
    return [_mix("#C3D0F2", "#0E2E8A", i / (n - 1)) for i in range(n)]


def _legend(o, x, y, names, cols):
    for j, name in enumerate(names):
        o.append(f'<circle cx="{x+6}" cy="{y}" r="5" fill="{cols[j]}"/><text x="{x+16}" y="{y+4}" class="c-note">{esc(name)}</text>')
        x += 16 + 6.5 * len(name) + 22
    return x


def _line_multi(o, x0, y0, w, h, cats, series, fmt, title, ymin=None, ymax=None, ref=None, hl=(), end_labels=True, point_labels=None, sel=None, ticks=4, cat_every=1, markers=True, cols=None, emph=None):
    n = len(cats)
    if title:
        o.append(f'<text x="{x0}" y="{y0-8}" class="c-lab">{esc(title)}</text>')
    allv = [v for _, vs in series for v in vs if v is not None]
    lo = 0 if ymin is None else ymin
    hi = (max(allv) * 1.12 if allv else 1) if ymax is None else ymax
    nlo, nhi, step = _nice_axis(lo, hi, ticks)
    if ymax is None:
        hi = nhi
    if hi <= lo:
        hi = lo + 1
    Y = lambda v: y0 + h - (v - lo) / (hi - lo) * h
    for gv in _ticks(nlo, hi, step):
        if gv < lo - 1e-9 or gv > hi + 1e-9:
            continue
        o.append(f'<line x1="{x0}" y1="{Y(gv):.1f}" x2="{x0+w}" y2="{Y(gv):.1f}" class="c-grid"/>')
        o.append(f'<text x="{x0-6}" y="{Y(gv)+4:.1f}" text-anchor="end" class="c-note">{esc(fmtv(gv, fmt))}</text>')
    if ref:
        o.append(f'<line x1="{x0}" y1="{Y(ref[0]):.1f}" x2="{x0+w}" y2="{Y(ref[0]):.1f}" class="c-ref"/><text x="{x0+4}" y="{Y(ref[0])-4:.1f}" class="c-note">{esc(ref[1])}</text>')
    slot = w / n
    for i, c in enumerate(cats):
        if i % cat_every == 0:
            o.append(f'<text x="{x0+i*slot+slot/2:.1f}" y="{y0+h+16}" text-anchor="middle" class="c-cat">{esc(c)}</text>')
    pl = point_labels if point_labels is not None else (len(series) <= 2)
    ends = []
    for j, (name, vals) in enumerate(series):
        if cols:
            col = cols[j % len(cols)]
        else:
            col = PAL[j % len(PAL)] if len(series) > 1 else PAL[0]
        strong = (emph is None) or (j in emph)
        if not strong:
            col = "#" + GRAY
        pts = [(x0 + i * slot + slot / 2, Y(v)) for i, v in enumerate(vals) if v is not None]
        d = " ".join(f'{"M" if i==0 else "L"}{x:.1f},{y:.1f}' for i, (x, y) in enumerate(pts))
        o.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{2.5 if strong else 1.5}"/>')
        for i, v in enumerate(vals):
            if v is None:
                continue
            x, y = x0 + i * slot + slot / 2, Y(v)
            if markers or i in hl or i == len(vals) - 1:
                o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{5 if i in hl else 3.5}" fill="{col}" stroke="#fff" stroke-width="1.5"/>')
            if pl and (sel is None or i in sel):
                dy = -9 if (j % 2 == 0 or len(series) == 1) else 16
                o.append(f'<text x="{x:.1f}" y="{y+dy:.1f}" text-anchor="middle" class="c-val c-sm">{esc(fmtv(v, fmt))}</text>')
        if end_labels and len(series) > 1 and pts:
            ends.append([pts[-1][1], pts[-1][0], name, col, strong])
    if ends:
        ends = _spread(ends, 13, y0 + 4, y0 + h + 4)
        for yy, x, name, col, strong in ends:
            o.append(f'<text x="{x+9:.1f}" y="{yy+4:.1f}" class="c-val c-sm" style="fill:{col if strong else "#"+INK2};font-weight:{700 if strong else 400}">{esc(name)}</text>')


def svg_multiline(ex, W=760):
    cats, series = ex["cats"], ex["series"]
    Hh = 380
    o = [f'<svg viewBox="0 0 {W} {Hh}" class="chart" role="img" preserveAspectRatio="xMinYMin meet">']
    x = 60
    if ex.get("label"):
        o.append(f'<text x="{x}" y="16" class="c-lab">{esc(ex["label"])}</text>')
    cols = _ramp(len(series)) if ex.get("ramp") else PAL
    emph = ex.get("emph")
    _legend(o, x, 36, [s[0] for s in series], [c if (emph is None or j in emph) else "#" + GRAY for j, c in enumerate(cols)])
    _line_multi(o, x, 60, W - 140, 270, cats, series, ex.get("fmt", ""), None, ex.get("ymin"), ex.get("ymax"), ex.get("ref"), set(ex.get("highlight", [])), True, ex.get("point_labels"), cat_every=ex.get("cat_every", 1), markers=ex.get("markers", True), cols=cols, emph=emph)
    if ex.get("note"):
        o.append(f'<text x="{x}" y="{Hh-6}" class="c-note">{esc(ex["note"])}</text>')
    o.append("</svg>")
    return "".join(o)


def svg_panels(ex, W=760):
    cats, panels = ex["cats"], ex["panels"]
    hl = set(ex.get("highlight", []))
    ph, gap, top = ex.get("ph", 92), 58, 30
    Hh = top + len(panels) * (ph + gap)
    o = [f'<svg viewBox="0 0 {W} {Hh}" class="chart" role="img" preserveAspectRatio="xMinYMin meet">']
    y = top
    for p in panels:
        if p.get("kind", "col") == "col":
            _col_panel(o, 60, y, W - 130, ph, cats, p["series"][0][1], hl, p.get("fmt", ""), p["title"], "col")
        else:
            cols = _ramp(len(p["series"])) if (p.get("ramp") or ex.get("ramp")) else None
            _line_multi(o, 60, y, W - 130, ph, cats, p["series"], p.get("fmt", ""), p["title"], p.get("ymin"), p.get("ymax"), p.get("ref"), hl, point_labels=p.get("point_labels"), cat_every=ex.get("cat_every", 1), markers=ex.get("markers", True), cols=cols, emph=p.get("emph"))
        y += ph + gap
    o.append("</svg>")
    return "".join(o)


def svg_smallmult(ex, W=760):
    cells = ex["cells"]
    hl = set(ex.get("highlight", []))
    cw, ch = W / 2, 222
    ncol = 2
    nrow = (len(cells) + 1) // 2
    Hh = nrow * ch + 10
    o = [f'<svg viewBox="0 0 {W} {Hh}" class="chart" role="img" preserveAspectRatio="xMinYMin meet">']
    for i, c in enumerate(cells):
        cx = (i % ncol) * cw + 52
        cy = (i // ncol) * ch
        w = cw - 70
        o.append(f'<text x="{cx}" y="{cy+16}" class="c-lab" style="fill:{PAL[0]}">{esc(c["title"])}</text>')
        n1, v1 = c["vol"]; n2, v2 = c["resp"]
        def key(v):
            return {0, len(v) - 1, v.index(max(v)), v.index(min(v))} | hl
        _col_panel(o, cx, cy + 44, w, 48, c["cats"], v1, hl, c.get("fmt_vol", "M"), n1, "col", labels=key(v1), ticks=2)
        _line_multi(o, cx, cy + 146, w, 44, c["cats"], [(n2, v2)], c.get("fmt_resp", "pct1"), n2, c.get("ymin"), None, None, hl, False, True, sel=key(v2), ticks=2)
    o.append("</svg>")
    return "".join(o)


def svg_scatter(ex, W=1000):
    panels, groups = ex["panels"], ex["groups"]
    cols = {g: PAL[i % len(PAL)] for i, g in enumerate(groups)}
    passmode = ex.get("mode") == "pass"
    Hh = 360 if any(p.get("bands") for p in panels) else 340
    o = [f'<svg viewBox="0 0 {W} {Hh}" class="chart" role="img" preserveAspectRatio="xMinYMin meet">']
    if passmode:
        _legend(o, 60, 18, ["Pasa el mínimo del canal", "No pasa"], ["#1F9E89", "#" + GRAY])
    else:
        _legend(o, 60, 18, groups, [cols[g] for g in groups])
    pw = (W - 60) / len(panels) - 40
    import math
    for pi, p in enumerate(panels):
        x0 = 60 + pi * (pw + 40)
        y0, h = 56, 212
        o.append(f'<text x="{x0}" y="{y0-10}" class="c-lab">{esc(p["title"])}</text>')
        xmin, xmax = p.get("xmin", 2e5), p.get("xmax", 2e7)
        ymax = p["ymax"]
        X = lambda v: x0 + (math.log10(max(v, xmin)) - math.log10(xmin)) / (math.log10(xmax) - math.log10(xmin)) * pw
        Y = lambda v: y0 + h - min(v, ymax) / ymax * h
        for t in range(0, 4):
            gv = ymax * t / 3
            o.append(f'<line x1="{x0}" y1="{Y(gv):.1f}" x2="{x0+pw}" y2="{Y(gv):.1f}" class="c-grid"/>')
            o.append(f'<text x="{x0-6}" y="{Y(gv)+4:.1f}" text-anchor="end" class="c-note">{esc(fmtv(gv, p.get("fmt", "pct1")))}</text>')
        for xv, xl in p.get("xticks", [(2e5, "200 mil"), (1e6, "1 M"), (5e6, "5 M"), (2e7, "20 M")]):
            if xmin <= xv <= xmax:
                o.append(f'<line x1="{X(xv):.1f}" y1="{y0}" x2="{X(xv):.1f}" y2="{y0+h}" class="c-grid"/><text x="{X(xv):.1f}" y="{y0+h+16}" text-anchor="middle" class="c-cat">{esc(xl)}</text>')
        if p.get("ref"):
            rv, rl = p["ref"]
            o.append(f'<line x1="{x0}" y1="{Y(rv):.1f}" x2="{x0+pw}" y2="{Y(rv):.1f}" class="c-ref"/><text x="{x0+pw}" y="{Y(rv)-4:.1f}" text-anchor="end" class="c-note">{esc(rl)}</text>')
        over = 0
        thr = p["ref"][0] if (passmode and p.get("ref")) else None
        order = sorted(p["pts"], key=lambda q: (q["y"] >= thr if thr is not None else 0, -q["x"]))
        for pt in order:
            clipped = pt["y"] > ymax
            over += clipped
            if thr is not None:
                ok = pt["y"] >= thr
                fill, op, r = ("#1F9E89", 0.95, 4.8) if ok else ("#" + GRAY, 0.55, 3.6)
            else:
                fill, op, r = cols.get(pt["g"], "#999"), (0.9 if clipped else 0.7), (4.5 if clipped else 4)
            o.append(f'<circle cx="{X(pt["x"]):.1f}" cy="{Y(pt["y"]):.1f}" r="{r}" fill="{fill}" fill-opacity="{op}" stroke="#fff" stroke-width="0.8"/>')
        for b in p.get("bands", []):
            xa, xb, txt = b
            xa_, xb_ = X(max(xa, xmin)), X(min(xb, xmax))
            o.append(f'<line x1="{xa_:.1f}" y1="{y0+h+24}" x2="{xb_:.1f}" y2="{y0+h+24}" stroke="#1F9E89" stroke-width="1.5"/>')
            o.append(f'<text x="{(xa_+xb_)/2:.1f}" y="{y0+h+38}" text-anchor="middle" class="c-val c-sm" style="fill:#1F9E89">{esc(txt)}</text>')
        for lab in p.get("labels", []):
            name, xv, yv, dx, dy = lab
            o.append(f'<text x="{X(xv)+dx:.1f}" y="{Y(yv)+dy:.1f}" text-anchor="{"end" if dx < 0 else "start"}" class="c-note" style="fill:var(--ink)">{esc(name)}</text>')
        o.append(f'<text x="{x0+pw/2:.1f}" y="{y0+h+(54 if p.get("bands") else 36)}" text-anchor="middle" class="c-note">{esc(p.get("xlab", "Mensajes entregados (escala logarítmica)"))}</text>')
        if over:
            o.append(f'<text x="{x0+4}" y="{y0+12}" class="c-note">{over} piezas arriba de {fmtv(ymax, p.get("fmt","pct1"))} (se muestran en el tope)</text>')
    o.append("</svg>")
    return "".join(o)


def svg_dotrange(ex, W=760):
    rowsx = ex["rows"]
    fmt = ex.get("fmt", "pct2")
    xmax = ex["xmax"]
    labw, top, rh = 150, 46, 60
    pw = W - labw - 40
    Hh = top + len(rowsx) * rh + 36
    o = [f'<svg viewBox="0 0 {W} {Hh}" class="chart" role="img" preserveAspectRatio="xMinYMin meet">']
    o.append(f'<text x="0" y="16" class="c-lab">{esc(ex.get("label",""))}</text>')
    X = lambda v: labw + min(v, xmax) / xmax * pw
    # leyenda
    lx = 0
    o.append(f'<circle cx="{lx+5}" cy="34" r="3" fill="#{GRAY}" fill-opacity=".7"/><text x="{lx+13}" y="38" class="c-note">una pieza</text>')
    o.append(f'<rect x="{lx+90}" y="28" width="24" height="12" fill="var(--accent-soft)"/><text x="{lx+118}" y="38" class="c-note">promedio ± 1 desviación estándar</text>')
    o.append(f'<line x1="{lx+330}" y1="28" x2="{lx+330}" y2="40" stroke="#{ACCENT}" stroke-width="3"/><text x="{lx+336}" y="38" class="c-note">promedio</text>')
    o.append(f'<line x1="{lx+410}" y1="28" x2="{lx+410}" y2="40" stroke="#{INK}" stroke-width="2" stroke-dasharray="3 2"/><text x="{lx+416}" y="38" class="c-note">mediana</text>')
    if ex.get("ref"):
        rv, rl = ex["ref"]
        o.append(f'<line x1="{lx+500}" y1="28" x2="{lx+500}" y2="40" class="c-ref"/><text x="{lx+506}" y="38" class="c-note">{esc(rl)}</text>')
        o.append(f'<line x1="{X(rv):.1f}" y1="{top}" x2="{X(rv):.1f}" y2="{top+len(rowsx)*rh}" class="c-ref"/>')
    import random
    rnd = random.Random(7)
    for i, r in enumerate(rowsx):
        y = top + i * rh
        cy = y + rh / 2
        o.append(f'<line x1="{labw}" y1="{cy:.1f}" x2="{labw+pw}" y2="{cy:.1f}" class="c-grid"/>')
        o.append(f'<text x="{labw-10}" y="{cy+1:.1f}" text-anchor="end" class="c-cat">{esc(r["cat"])}</text><text x="{labw-10}" y="{cy+15:.1f}" text-anchor="end" class="c-note">{r["n"]} piezas</text>')
        lo, hi = max(0, r["mean"] - r["sd"]), r["mean"] + r["sd"]
        o.append(f'<rect x="{X(lo):.1f}" y="{cy-14:.1f}" width="{max(1, X(hi)-X(lo)):.1f}" height="28" fill="var(--accent-soft)"/>')
        over = 0
        for v, w in r["pts"]:
            over += v > xmax
            o.append(f'<circle cx="{X(v):.1f}" cy="{cy+rnd.uniform(-10,10):.1f}" r="{3.2 if w > 1e6 else 2.4}" fill="#{GRAY}" fill-opacity=".7"/>')
        o.append(f'<line x1="{X(r["median"]):.1f}" y1="{cy-16:.1f}" x2="{X(r["median"]):.1f}" y2="{cy+16:.1f}" stroke="#{INK}" stroke-width="2" stroke-dasharray="3 2"/>')
        o.append(f'<line x1="{X(r["mean"]):.1f}" y1="{cy-16:.1f}" x2="{X(r["mean"]):.1f}" y2="{cy+16:.1f}" stroke="#{ACCENT}" stroke-width="3"/>')
        o.append(f'<text x="{labw+pw+6}" y="{cy-2:.1f}" class="c-val c-sm">{esc(fmtv(r["mean"], fmt))}</text><text x="{labw+pw+6}" y="{cy+11:.1f}" class="c-note">± {esc(fmtv(r["sd"], fmt))}</text>')
        if over:
            o.append(f'<text x="{labw+pw-4}" y="{cy-18:.1f}" text-anchor="end" class="c-note">{over} arriba de {esc(fmtv(xmax, fmt))}</text>')
    for t in range(0, 5):
        v = xmax * t / 4
        o.append(f'<text x="{X(v):.1f}" y="{top+len(rowsx)*rh+16}" text-anchor="middle" class="c-cat">{esc(fmtv(v, fmt))}</text>')
    o.append("</svg>")
    return "".join(o)


def svg_heatmap(ex, W=760):
    cols, rws, M, share = ex["cols"], ex["rows"], ex["matrix"], ex.get("share")
    fmt = ex.get("fmt", "pct2")
    labw, top = ex.get("labw", 130), 26
    rshare = ex.get("row_share")
    rsw = 110 if rshare else 0
    cw = (W - labw - 10 - rsw) / len(cols)
    rh = 40 if len(rws) <= 6 else 32
    sh = 78 if share else 0
    Hh = top + sh + 26 + len(rws) * rh + 10
    o = [f'<svg viewBox="0 0 {W} {Hh}" class="chart" role="img" preserveAspectRatio="xMinYMin meet">']
    y = top
    if share:
        o.append(f'<text x="{labw}" y="{y-8}" class="c-lab">{esc(ex.get("share_label", "% de los envíos"))}</text>')
        mx = max(share)
        for j, v in enumerate(share):
            bh = v / mx * 36
            x = labw + j * cw + cw * 0.2
            o.append(f'<rect x="{x:.1f}" y="{y+56-bh:.1f}" width="{cw*0.6:.1f}" height="{bh:.1f}" rx="2" fill="#{GRAY}"/>')
            o.append(f'<text x="{x+cw*0.3:.1f}" y="{y+56-bh-4:.1f}" text-anchor="middle" class="c-val c-sm">{v:.0f} %</text>')
        y += sh
    o.append(f'<text x="{labw}" y="{y+2}" class="c-lab">{esc(ex.get("label",""))}</text>')
    y += 10
    for j, c in enumerate(cols):
        o.append(f'<text x="{labw+j*cw+cw/2:.1f}" y="{y+12}" text-anchor="middle" class="c-cat">{esc(c)}</text>')
    if rshare:
        o.append(f'<text x="{labw+len(cols)*cw+rsw/2+6:.1f}" y="{y+12}" text-anchor="middle" class="c-cat">{esc(ex.get("share_label", "% de los envíos"))}</text>')
    y += 18
    vals = [v for row in M for v in row if v is not None]
    lo, hi = min(vals), max(vals)
    rs, cs = ex.get("row_scale"), ex.get("col_scale")
    fmts = ex.get("fmts")
    colrange = []
    for j in range(len(cols)):
        cv = [row[j] for row in M if row[j] is not None]
        colrange.append((min(cv), max(cv)) if cv else (0, 1))
    for i, r in enumerate(rws):
        if rs:
            rv = [v for v in M[i] if v is not None]
            lo, hi = min(rv), max(rv)
        yy = y + i * rh
        o.append(f'<text x="{labw-10}" y="{yy+rh/2+4:.1f}" text-anchor="end" class="c-cat" style="font-weight:{700 if i==0 else 400}">{esc(r)}</text>')
        for j, v in enumerate(M[i]):
            x = labw + j * cw
            if v is None:
                o.append(f'<rect x="{x+1:.1f}" y="{yy+1}" width="{cw-2:.1f}" height="{rh-2}" fill="var(--paper-2)"/>')
                continue
            if cs:
                lo, hi = colrange[j]
            t = (v - lo) / (hi - lo) if hi > lo else 0
            fill = _mix("#FFFFFF", "#" + ACCENT, 0.08 + 0.92 * t)
            o.append(f'<rect x="{x+1:.1f}" y="{yy+1}" width="{cw-2:.1f}" height="{rh-2}" fill="{fill}"/>')
            o.append(f'<text x="{x+cw/2:.1f}" y="{yy+rh/2+4:.1f}" text-anchor="middle" class="c-val c-sm" style="fill:{"#fff" if t>0.55 else "#"+INK}">{esc(fmtv(v, fmts[j] if fmts else fmt))}</text>')
        if rshare:
            mx = max(rshare)
            bw = rshare[i] / mx * (rsw - 48)
            x0 = labw + len(cols) * cw + 8
            o.append(f'<rect x="{x0:.1f}" y="{yy+rh/2-7:.1f}" width="{bw:.1f}" height="14" rx="2" fill="#{GRAY}"/>')
            o.append(f'<text x="{x0+bw+5:.1f}" y="{yy+rh/2+4:.1f}" class="c-val c-sm">{rshare[i]:.0f} %</text>')
    o.append("</svg>")
    return "".join(o)


def _marker(o, x, y, mk, col, r=4.5, op=0.75):
    if mk == "d":
        o.append(f'<rect x="{x-r:.1f}" y="{y-r:.1f}" width="{2*r:.1f}" height="{2*r:.1f}" transform="rotate(45 {x:.1f} {y:.1f})" fill="{col}" fill-opacity="{op}" stroke="#fff" stroke-width="0.8"/>')
    else:
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r*0.9:.1f}" fill="{col}" fill-opacity="{op}" stroke="#fff" stroke-width="0.8"/>')


def svg_regress(ex, W=760):
    """Dispersión con recta de regresión lineal (OLS), ecuación, R² y n por panel."""
    import math
    panels = ex["panels"]
    groups = ex.get("groups") or []
    cols = {g: PAL[i % len(PAL)] for i, g in enumerate(groups)}
    Hh = ex.get("height", 340)
    o = [f'<svg viewBox="0 0 {W} {Hh}" class="chart" role="img" preserveAspectRatio="xMinYMin meet">']
    if groups:
        _legend(o, 60, 18, groups, [cols[g] for g in groups])
    if ex.get("marker_note"):
        o.append(f'<text x="{W-10}" y="36" text-anchor="end" class="c-note">{esc(ex["marker_note"])}</text>')
    npan = len(panels)
    pw = (W - 60) / npan - 40
    for pi, p in enumerate(panels):
        x0 = 60 + pi * (pw + 40)
        y0, h = 60, Hh - 130
        o.append(f'<text x="{x0}" y="{y0-12}" class="c-lab">{esc(p["title"])}</text>')
        xlog = p.get("xlog", False)
        pts = p["pts"]
        xs = [q["x"] for q in pts]
        xmin, xmax = p.get("xmin", min(xs)), p.get("xmax", max(xs))
        tx = (lambda v: math.log10(v)) if xlog else (lambda v: v)
        X = lambda v: x0 + (tx(max(v, xmin)) - tx(xmin)) / (tx(xmax) - tx(xmin)) * pw
        lo = p.get("ymin", 0)
        hi = p["ymax"]
        Y = lambda v: y0 + h - (min(max(v, lo), hi) - lo) / (hi - lo) * h
        fmt = p.get("fmt", "pct1")
        for t in range(0, 4):
            gv = lo + (hi - lo) * t / 3
            o.append(f'<line x1="{x0}" y1="{Y(gv):.1f}" x2="{x0+pw}" y2="{Y(gv):.1f}" class="c-grid"/>')
            o.append(f'<text x="{x0-6}" y="{Y(gv)+4:.1f}" text-anchor="end" class="c-note">{esc(fmtv(gv, fmt))}</text>')
        for xv, xl in p["xticks"]:
            if xmin <= xv <= xmax:
                o.append(f'<line x1="{X(xv):.1f}" y1="{y0}" x2="{X(xv):.1f}" y2="{y0+h}" class="c-grid"/><text x="{X(xv):.1f}" y="{y0+h+16}" text-anchor="middle" class="c-cat">{esc(xl)}</text>')
        if p.get("ref"):
            rv, rl = p["ref"]
            o.append(f'<line x1="{x0}" y1="{Y(rv):.1f}" x2="{x0+pw}" y2="{Y(rv):.1f}" class="c-ref"/><text x="{x0+pw}" y="{Y(rv)-4:.1f}" text-anchor="end" class="c-note">{esc(rl)}</text>')
        # recta de regresión en el rango observado
        fit = p.get("fit")
        if fit:
            fx = [q["x"] for q in pts if p.get("fit_filter", lambda q: True)(q)]
            a, b = fit["a"], fit["b"]
            x1, x2 = min(fx), max(fx)
            y1, y2 = a + b * tx(x1), a + b * tx(x2)
            o.append(f'<line x1="{X(x1):.1f}" y1="{Y(y1):.1f}" x2="{X(x2):.1f}" y2="{Y(y2):.1f}" stroke="#{INK}" stroke-width="2" stroke-opacity="0.85"/>')
            eq = p.get("eq") or f'R² = {fit["r2"]:.2f}   n = {fit["n"]}'
            o.append(f'<text x="{x0+pw}" y="{y0+2}" text-anchor="end" class="c-val c-sm">{esc(eq)}</text>')
        for q in pts:
            col = cols.get(q.get("g"), "#" + ACCENT) if groups else ("#" + ACCENT if q.get("mk") != "d" else "#" + RED)
            _marker(o, X(q["x"]), Y(q["y"]), q.get("mk", "o"), col)
        for name, xv, yv, dx, dy in p.get("labels", []):
            o.append(f'<text x="{X(xv)+dx:.1f}" y="{Y(yv)+dy:.1f}" class="c-note" style="fill:var(--ink)" text-anchor="{"end" if dx < 0 else "start"}">{esc(name)}</text>')
        o.append(f'<text x="{x0+pw/2:.1f}" y="{y0+h+36}" text-anchor="middle" class="c-note">{esc(p.get("xlab", ""))}</text>')
    if ex.get("note"):
        o.append(f'<text x="60" y="{Hh-6}" class="c-note">{esc(ex["note"])}</text>')
    o.append("</svg>")
    return "".join(o)


def svg_hist(ex, W=760):
    """Histograma con curva normal superpuesta (campana) y marcas de promedio, mediana y mínimo."""
    cells = ex["cells"]
    Hh = 340
    o = [f'<svg viewBox="0 0 {W} {Hh}" class="chart" role="img" preserveAspectRatio="xMinYMin meet">']
    npan = len(cells)
    pw = (W - 60) / npan - 40
    for pi, c in enumerate(cells):
        x0 = 60 + pi * (pw + 40)
        y0, h = 56, 190
        o.append(f'<text x="{x0}" y="{y0-12}" class="c-lab">{esc(c["title"])}</text>')
        counts, normal = c["counts"], c["normal"]
        n = len(counts)
        hi = max(max(counts), max(normal)) * 1.12
        Y = lambda v: y0 + h - v / hi * h
        bw = pw / n
        for t in range(0, 4):
            gv = hi * t / 3
            o.append(f'<line x1="{x0}" y1="{Y(gv):.1f}" x2="{x0+pw}" y2="{Y(gv):.1f}" class="c-grid"/>')
            o.append(f'<text x="{x0-6}" y="{Y(gv)+4:.1f}" text-anchor="end" class="c-note">{gv:.0f}</text>')
        for i, v in enumerate(counts):
            x = x0 + i * bw
            o.append(f'<rect x="{x+1:.1f}" y="{Y(v):.1f}" width="{bw-2:.1f}" height="{max(0, y0+h-Y(v)):.1f}" fill="#{ACCENT}" fill-opacity="0.55"/>')
        for i, lab in enumerate(c["xlabels"]):
            if lab:
                o.append(f'<text x="{x0+i*bw:.1f}" y="{y0+h+16}" text-anchor="middle" class="c-cat">{esc(lab)}</text>')
        d = " ".join(f'{"M" if i==0 else "L"}{x0+(i+0.5)*bw:.1f},{Y(v):.1f}' for i, v in enumerate(normal))
        o.append(f'<path d="{d}" fill="none" stroke="#{INK}" stroke-width="2.25"/>')
        for lab, pos, yy in c.get("marks", []):
            x = x0 + pos * bw
            o.append(f'<line x1="{x:.1f}" y1="{y0}" x2="{x:.1f}" y2="{y0+h}" class="c-ref"/>')
            o.append(f'<text x="{x+4:.1f}" y="{y0+12+yy}" class="c-val c-sm">{esc(lab)}</text>')
        o.append(f'<text x="{x0+pw/2:.1f}" y="{y0+h+36}" text-anchor="middle" class="c-note">{esc(c.get("xlab", ""))}</text>')
        o.append(f'<text x="{x0+pw}" y="{y0+h+54}" text-anchor="end" class="c-note">{esc(c.get("note", ""))}</text>')
    o.append(f'<text x="60" y="{Hh-6}" class="c-note">{esc(ex.get("note", "Barras: número de piezas-mes por rango. Línea: campana normal con el mismo promedio y desviación."))}</text>')
    o.append("</svg>")
    return "".join(o)


def svg_candle(ex, W=760):
    """Velas por mes: apertura = primera semana, cierre = última, mecha = máximo y mínimo semanal."""
    cells = ex["cells"]
    cw, ch = W / 2, 168
    ncol = 2
    nrow = (len(cells) + 1) // 2
    Hh = nrow * ch + 24
    o = [f'<svg viewBox="0 0 {W} {Hh}" class="chart" role="img" preserveAspectRatio="xMinYMin meet">']
    UP, DN = "#1F9E89", "#" + RED
    for i, c in enumerate(cells):
        cx = (i % ncol) * cw + 60
        cy = (i // ncol) * ch + 20
        w, h = cw - 80, 92
        o.append(f'<text x="{cx}" y="{cy}" class="c-lab">{esc(c["title"])}</text>')
        data = c["ohlc"]
        vals = [v for d in data if d for v in d]
        lo, hi = min(vals), max(vals)
        pad = (hi - lo) * 0.15 or 1
        lo, hi = max(0, lo - pad) if c.get("zero") else lo - pad, hi + pad
        y0 = cy + 14
        Y = lambda v: y0 + h - (v - lo) / (hi - lo) * h
        fmt = c.get("fmt", "pct2")
        for t in range(0, 3):
            gv = lo + (hi - lo) * t / 2
            o.append(f'<line x1="{cx}" y1="{Y(gv):.1f}" x2="{cx+w}" y2="{Y(gv):.1f}" class="c-grid"/>')
            o.append(f'<text x="{cx-6}" y="{Y(gv)+4:.1f}" text-anchor="end" class="c-note">{esc(fmtv(gv, fmt))}</text>')
        slot = w / len(data)
        bwid = slot * 0.5
        highs = [d[1] for d in data if d]; lows = [d[2] for d in data if d]
        for j, d in enumerate(data):
            x = cx + j * slot + slot / 2
            o.append(f'<text x="{x:.1f}" y="{y0+h+16}" text-anchor="middle" class="c-cat">{esc(c["cats"][j])}</text>')
            if not d:
                continue
            op, hg, lw, cl = d
            col = UP if cl >= op else DN
            o.append(f'<line x1="{x:.1f}" y1="{Y(hg):.1f}" x2="{x:.1f}" y2="{Y(lw):.1f}" stroke="{col}" stroke-width="1.5"/>')
            yt, yb = Y(max(op, cl)), Y(min(op, cl))
            o.append(f'<rect x="{x-bwid/2:.1f}" y="{yt:.1f}" width="{bwid:.1f}" height="{max(2, yb-yt):.1f}" fill="{col}" rx="1"/>')
            if hg == max(highs):
                o.append(f'<text x="{x:.1f}" y="{Y(hg)-5:.1f}" text-anchor="middle" class="c-val c-sm">{esc(fmtv(hg, fmt))}</text>')
            if lw == min(lows):
                o.append(f'<text x="{x:.1f}" y="{Y(lw)+13:.1f}" text-anchor="middle" class="c-val c-sm">{esc(fmtv(lw, fmt))}</text>')
        o.append(f'<text x="{cx+w}" y="{cy}" text-anchor="end" class="c-note">{esc(c.get("note", ""))}</text>')
    o.append(f'<text x="60" y="{Hh-4}" class="c-note">{esc(ex.get("note", "Cada vela es un mes: cuerpo de la primera a la última semana (verde sube, rojo baja); mecha del mínimo al máximo semanal."))}</text>')
    o.append("</svg>")
    return "".join(o)


def svg_idxgrid(ex, W=760):
    """Cuatro paneles, uno por canal: volumen y respuesta semanal indexados a enero (=100), mismo eje en los cuatro."""
    cells, cats = ex["cells"], ex["cats"]
    cw, ch = W / 2, 166
    nrow = (len(cells) + 1) // 2
    Hh = nrow * ch + 26
    o = [f'<svg viewBox="0 0 {W} {Hh}" class="chart" role="img" preserveAspectRatio="xMinYMin meet">']
    lo, hi = 0, ex.get("ymax", 360)
    GR = "#" + INK2
    for i, c in enumerate(cells):
        cx = (i % 2) * cw + 52
        cy = (i // 2) * ch + 22
        w, h = cw - 96, 92
        col = PAL[i % len(PAL)]
        o.append(f'<text x="{cx}" y="{cy}" class="c-lab" style="fill:{col}">{esc(c["title"])}</text>')
        y0 = cy + 14
        Y = lambda v: y0 + h - (v - lo) / (hi - lo) * h
        for gv in (0, 100, 200, 300):
            if gv > hi:
                continue
            cls = "c-ref" if gv == 100 else "c-grid"
            o.append(f'<line x1="{cx}" y1="{Y(gv):.1f}" x2="{cx+w}" y2="{Y(gv):.1f}" class="{cls}"/>')
            o.append(f'<text x="{cx-6}" y="{Y(gv)+4:.1f}" text-anchor="end" class="c-note">{gv}</text>')
        n = len(cats)
        slot = w / n
        for k, cat in enumerate(cats):
            if k % ex.get("cat_every", 6) == 0:
                o.append(f'<text x="{cx+k*slot+slot/2:.1f}" y="{y0+h+15}" text-anchor="middle" class="c-note">{esc(cat)}</text>')
        ends = {}
        for name, vals, color, width in (("Respuesta", c["resp"], GR, 1.75), ("Volumen", c["vol"], col, 2.5)):
            pts = [(cx + k * slot + slot / 2, Y(v)) for k, v in enumerate(vals)]
            d = " ".join(f'{"M" if k==0 else "L"}{x:.1f},{y:.1f}' for k, (x, y) in enumerate(pts))
            o.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linejoin="round"/>')
            x, y = pts[-1]
            o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="{color}" stroke="#fff" stroke-width="1.5"/>')
            ends[name] = (x, y, color, vals[-1])
        # etiquetas finales separadas si las dos líneas terminan juntas
        yv, yr = ends["Volumen"][1], ends["Respuesta"][1]
        if abs(yv - yr) < 13:
            mid = (yv + yr) / 2
            yv, yr = (mid - 7, mid + 7) if yv <= yr else (mid + 7, mid - 7)
        for name, yy in (("Volumen", yv), ("Respuesta", yr)):
            x, _, color, v = ends[name]
            o.append(f'<text x="{x+7:.1f}" y="{yy+4:.1f}" class="c-val c-sm" style="fill:{color}">{esc(name)} {v:.0f}</text>')
        # pico de volumen y mínimo de respuesta, anotados
        vi, ri = c["vmax_i"], c["rmin_i"]
        xv, yv = cx + vi * slot + slot / 2, Y(c["vmax"])
        o.append(f'<circle cx="{xv:.1f}" cy="{yv:.1f}" r="4" fill="{col}" stroke="#fff" stroke-width="1.5"/>')
        anchor = "end" if vi > n * 0.6 else "start"
        o.append(f'<text x="{xv+(-7 if anchor=="end" else 7):.1f}" y="{yv-6:.1f}" text-anchor="{anchor}" class="c-val c-sm" style="paint-order:stroke;stroke:#fff;stroke-width:3px">{c["vmax"]:.0f} sem {esc(cats[vi])}</text>')
        xr, yr = cx + ri * slot + slot / 2, Y(c["rmin"])
        o.append(f'<circle cx="{xr:.1f}" cy="{yr:.1f}" r="4" fill="{GR}" stroke="#fff" stroke-width="1.5"/>')
        anchor = "end" if ri > n * 0.6 else "start"
        yl = yr + 15 if yr + 15 < y0 + h - 2 else yr - 7
        o.append(f'<text x="{xr+(-7 if anchor=="end" else 7):.1f}" y="{yl:.1f}" text-anchor="{anchor}" class="c-val c-sm" style="fill:{GR};paint-order:stroke;stroke:#fff;stroke-width:3px">{c["rmin"]:.0f} sem {esc(cats[ri])}</text>')
    if ex.get("note"):
        o.append(f'<text x="52" y="{Hh-4}" class="c-note">{esc(ex["note"])}</text>')
    o.append("</svg>")
    return "".join(o)


def svg_hbarmult(ex, W=1000):
    """Rejilla de paneles de barras horizontales con la misma lista de categorías; mejor en verde, peor en rojo, resto gris."""
    panels, cats = ex["panels"], ex["cats"]
    ncol = ex.get("ncol", 3)
    nrow = (len(panels) + ncol - 1) // ncol
    n = len(cats)
    rowh, labw = 24, 14 + int(max(len(c) for c in cats) * 5.8)
    ph = 34 + n * rowh + 8
    pw = W / ncol
    Hh = nrow * ph + 6
    o = [f'<svg viewBox="0 0 {W} {Hh}" class="chart" role="img" preserveAspectRatio="xMinYMin meet">']
    for pi, p in enumerate(panels):
        x0 = (pi % ncol) * pw
        y0 = (pi // ncol) * ph
        vals = p["vals"]
        o.append(f'<text x="{x0}" y="{y0+16}" class="c-lab">{esc(p["title"])}</text>')
        vv = [v for v in vals if v is not None]
        vmax = max(vv) if vv else 1
        bw = pw - labw - 74
        best = vals.index(max(vv)) if p.get("better", "high") == "high" else vals.index(min(vv))
        worst = vals.index(min(vv)) if p.get("better", "high") == "high" else vals.index(max(vv))
        for i, (c, v) in enumerate(zip(cats, vals)):
            y = y0 + 28 + i * rowh
            o.append(f'<text x="{x0+labw-8}" y="{y+13}" text-anchor="end" class="c-cat">{esc(c)}</text>')
            if v is None:
                o.append(f'<text x="{x0+labw+4}" y="{y+13}" class="c-note">{esc(p.get("na", "no aplica"))}</text>')
                continue
            w = max(2, v / vmax * bw)
            col = "#1F9E89" if i == best else ("#B5342B" if i == worst else "#" + GRAY)
            o.append(f'<rect x="{x0+labw}" y="{y+2}" width="{w:.1f}" height="{rowh-7}" rx="2" fill="{col}"/>')
            o.append(f'<text x="{x0+labw+w+5:.1f}" y="{y+13}" class="c-val c-sm">{esc(fmtv(v, p.get("fmt", "")))}</text>')
    o.append("</svg>")
    return "".join(o)


def svg_stackbar(ex, W=900):
    """Barras horizontales apiladas por segmento (equipo), uno o dos paneles lado a lado."""
    panels = ex["panels"]
    segs = ex["segments"]
    cols = ex.get("colors") or PAL
    n = len(panels[0]["cats"])
    rowh, top, labw = 44, 44, 16 + int(max(len(c) for p in panels for c in p["cats"]) * 7.6)
    Hh = top + n * rowh + 30
    o = [f'<svg viewBox="0 0 {W} {Hh}" class="chart" role="img" preserveAspectRatio="xMinYMin meet">']
    _legend(o, 0, 14, segs, cols)
    npan = len(panels)
    pw = (W - labw * npan - 24 * (npan - 1)) / npan
    for pi, p in enumerate(panels):
        x0 = pi * (labw + pw + 24)
        o.append(f'<text x="{x0}" y="{top-8}" class="c-lab">{esc(p["title"])}</text>')
        tot = [sum(r) for r in p["rows"]]
        vmax = max(tot) if max(tot) > 0 else 1
        bw = pw - 70
        for i, (c, row) in enumerate(zip(p["cats"], p["rows"])):
            y = top + i * rowh + 6
            o.append(f'<text x="{x0+labw-10}" y="{y+18}" text-anchor="end" class="c-cat">{esc(c)}</text>')
            x = x0 + labw
            for j, v in enumerate(row):
                w = v / vmax * bw
                if w <= 0:
                    continue
                o.append(f'<rect x="{x:.1f}" y="{y}" width="{max(0, w-1.5):.1f}" height="26" rx="2" fill="{cols[j]}"/>')
                if w > 34 and p.get("seg_labels", True):
                    o.append(f'<text x="{x+w/2:.1f}" y="{y+17}" text-anchor="middle" class="c-val c-sm" style="fill:#fff">{esc(fmtv(v, p.get("fmt", "")))}</text>')
                x += w
            o.append(f'<text x="{x0+labw+tot[i]/vmax*bw+8:.1f}" y="{y+18}" class="c-val{"" if tot[i] > 0 else " c-sm"}" style="{"" if tot[i] > 0 else "fill:#"+INK2}">{esc(fmtv(tot[i], p.get("fmt", "")) if tot[i] > 0 else p.get("zero", "0"))}</text>')
    if ex.get("note"):
        o.append(f'<text x="0" y="{Hh-6}" class="c-note">{esc(ex["note"])}</text>')
    o.append("</svg>")
    return "".join(o)


def svg_barcause(ex, W=1000):
    """Izquierda: barras por pieza coloreadas por equipo (el quién). Derecha: la causa en 2 a 6 barras comparadas."""
    rows = ex["rows"]
    teams = ex.get("teams") or list(dict.fromkeys(r["team"] for r in rows))
    tcol = {t: PAL[i % len(PAL)] for i, t in enumerate(teams)}
    tcol.update(ex.get("team_colors", {}))
    n = len(rows)
    rowh, top, labw = 34, 46, 236
    lw = 620
    Hh = top + n * rowh + 24
    o = [f'<svg viewBox="0 0 {W} {Hh}" class="chart" role="img" preserveAspectRatio="xMinYMin meet">']
    _legend(o, 0, 14, teams, [tcol[t] for t in teams])
    o.append(f'<text x="0" y="{top-8}" class="c-lab">{esc(ex["label"])}</text>')
    vmax = max(r["val"] for r in rows) or 1
    maxtag = max(len(fmtv(r["val"], ex.get("fmt", ""))) + (len(r["tag"]) + 3 if r.get("tag") else 0) for r in rows)
    bw = lw - labw - 14 - maxtag * 5.6
    for i, r in enumerate(rows):
        y = top + i * rowh + 4
        o.append(f'<text x="{labw-10}" y="{y+16}" text-anchor="end" class="c-cat">{esc(r["name"])}</text>')
        w = max(2, r["val"] / vmax * bw)
        o.append(f'<rect x="{labw}" y="{y}" width="{w:.1f}" height="22" rx="2" fill="{tcol.get(r["team"], "#" + GRAY)}"/>')
        o.append(f'<text x="{labw+w+6:.1f}" y="{y+16}" class="c-val c-sm">{esc(fmtv(r["val"], ex.get("fmt", "")))}{(" · " + esc(r["tag"])) if r.get("tag") else ""}</text>')
    # panel causa
    c = ex["cause"]
    cx0 = lw + 30
    cw = W - cx0
    o.append(f'<line x1="{lw+8}" y1="{top-22}" x2="{lw+8}" y2="{Hh-10}" class="c-grid"/>')
    o.append(f'<text x="{cx0}" y="{top-8}" class="c-lab">{esc(c["title"])}</text>')
    m = len(c["cats"])
    avail = Hh - top - 20
    crow = min(46, avail / m)
    cvmax = max(c["vals"]) or 1
    clabw = c.get("labw", 118)
    cbw = cw - clabw - 62
    chl = set(c.get("hl", []))
    for i, (cat, v) in enumerate(zip(c["cats"], c["vals"])):
        y = top + i * crow + 4
        bh = min(22, crow - 10)
        o.append(f'<text x="{cx0+clabw-8}" y="{y+bh/2+4:.1f}" text-anchor="end" class="c-cat">{esc(cat)}</text>')
        w = max(2, v / cvmax * cbw)
        col = c.get("colors", {}).get(cat) or ("#B5342B" if i in chl else "#" + GRAY)
        o.append(f'<rect x="{cx0+clabw}" y="{y}" width="{w:.1f}" height="{bh}" rx="2" fill="{col}"/>')
        o.append(f'<text x="{cx0+clabw+w+6:.1f}" y="{y+bh/2+4:.1f}" class="c-val c-sm">{esc(fmtv(v, c.get("fmt", "")))}</text>')
    if c.get("note"):
        o.append(f'<text x="{cx0}" y="{Hh-6}" class="c-note">{esc(c["note"])}</text>')
    o.append("</svg>")
    return "".join(o)


RASTER_TYPES = ("regress", "hist", "candle", "idxgrid", "stackbar", "barcause", "hbarmult")


def render_exhibit(ex):
    t = ex["type"]
    if t == "regress":
        return svg_regress(ex)
    if t == "hist":
        return svg_hist(ex)
    if t == "candle":
        return svg_candle(ex)
    if t == "idxgrid":
        return svg_idxgrid(ex)
    if t == "stackbar":
        return svg_stackbar(ex)
    if t == "hbarmult":
        return svg_hbarmult(ex)
    if t == "barcause":
        return svg_barcause(ex)
    if t == "multiline":
        return svg_multiline(ex)
    if t == "panels":
        return svg_panels(ex)
    if t == "smallmult":
        return svg_smallmult(ex)
    if t == "scatter":
        return svg_scatter(ex)
    if t == "dotrange":
        return svg_dotrange(ex)
    if t == "heatmap":
        return svg_heatmap(ex)
    if t == "hbar":
        return svg_hbar(ex)
    if t == "hbar2":
        return svg_hbar2(ex)
    if t == "colline":
        return svg_colline(ex)
    if t == "line":
        return svg_line(ex)
    if t == "waterfall":
        return svg_waterfall(ex)
    if t == "table":
        return html_table(ex)
    if t == "stats":
        return html_stats(ex)
    if t == "rules":
        return html_rules(ex)
    if t == "gantt":
        return html_gantt(ex)
    raise ValueError(t)


# ----------------------------------------------------------------------------
# HTML
# ----------------------------------------------------------------------------

CSS = """
/* Layout: un slide 16:9 por pantalla, escalado con container queries; chrome exterior sigue el tema. */
:root{
  --accent:#%(A)s; --accent-soft:#E4EAFB; --ink:#%(I)s; --ink-2:#%(I2)s; --ink-3:#8A909B;
  --rule:#E3E6EB; --paper:#FFFFFF; --paper-2:#F6F7F9; --chrome:#EEF0F3; --chrome-ink:#4B515C;
  --bad:#%(R)s; --ok:#%(G)s; --warn:#%(AM)s; --bad-bg:#F8E7E5; --ok-bg:#E3F1E8; --warn-bg:#F7EFD6;
  --font:"Source Sans 3","Segoe UI",system-ui,sans-serif;
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){ --chrome:#15171B; --chrome-ink:#B9BEC7; --accent-soft:#E4EAFB; color-scheme:dark; } }
:root[data-theme="dark"]{ --chrome:#15171B; --chrome-ink:#B9BEC7; --accent-soft:#E4EAFB; color-scheme:dark; }
*{box-sizing:border-box}
body{margin:0;background:var(--chrome);color:var(--ink);font-family:var(--font);padding-inline:16px;padding-block:12px 40px}
.deck{max-width:1280px;margin:0 auto;display:flex;flex-direction:column;gap:18px}
.topbar{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center;color:var(--chrome-ink);font-size:14px;max-width:1280px;margin:0 auto 10px}
.topbar strong{color:var(--chrome-ink)}
.topbar .sp{flex:1}
.topbar a{color:var(--chrome-ink)}
.toc{display:flex;flex-wrap:wrap;gap:6px}
.toc a{display:inline-block;padding:3px 10px;border:1px solid currentColor;border-radius:999px;text-decoration:none;font-size:12.5px;opacity:.85}
.toc a:hover,.toc a:focus-visible{opacity:1;outline:2px solid var(--accent);outline-offset:1px}
.slide{container-type:inline-size;aspect-ratio:16/9;width:100%%;background:var(--paper);color:var(--ink);border-radius:6px;box-shadow:0 1px 2px rgba(0,0,0,.08),0 6px 24px rgba(0,0,0,.06);position:relative;overflow:hidden;scroll-margin-top:12px}
.s{position:absolute;inset:0;padding:3.8cqi 4.6cqi 3.2cqi;display:flex;flex-direction:column;gap:1.2cqi}
.tracker{position:absolute;top:2.2cqi;right:4.6cqi;font-size:1.25cqi;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3)}
.num{position:absolute;bottom:1.8cqi;right:4.6cqi;font-size:1.25cqi;color:var(--ink-3);font-variant-numeric:tabular-nums}
h2.t{margin:0;font-size:2.5cqi;line-height:1.2;font-weight:600;letter-spacing:-.01em;text-wrap:balance;max-width:84cqi;color:var(--ink)}
h2.t.t-long{font-size:2.2cqi;max-width:88cqi} h2.t.t-xl{font-size:1.95cqi;max-width:90cqi} h2.t::after{content:"";display:block;width:6cqi;height:.35cqi;background:var(--accent);margin-top:.7cqi;border-radius:2px}
.body{flex:1;display:grid;grid-template-columns:minmax(0,1.55fr) minmax(0,1fr);gap:3.4cqi;min-height:0}
.body.full{grid-template-columns:minmax(0,1fr)}
.ex{min-width:0;min-height:0;font-size:1.5cqi}
.side{min-width:0;font-size:1.42cqi;line-height:1.38;color:var(--ink-2);display:flex;flex-direction:column;gap:.9cqi}
.side p{margin:0;padding-left:1.4cqi;border-left:.3cqi solid var(--accent-soft)}
.side p strong{color:var(--ink)}
.src{font-size:1.15cqi;color:var(--ink-3);border-top:1px solid var(--rule);padding-top:.8cqi;padding-right:9cqi}
.ex{display:flex;align-items:flex-start}
.chart{width:100%%;height:100%%;max-height:100%%;display:block}
.hc{display:grid;grid-template-columns:1fr 1.25fr 1fr;gap:.6cqi 2cqi;margin-top:.3cqi;font-size:1.1cqi;line-height:1.26;color:var(--ink-2);padding-top:.5cqi;border-top:1px solid var(--rule)}
.hc p{margin:0}
.hc b{color:var(--ink);font-size:1.02cqi;letter-spacing:.1em;text-transform:uppercase;margin-right:.6cqi}
.hc .tag{display:inline-block;font-size:1.0cqi;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--bad);background:var(--bad-bg);padding:.05cqi .5cqi;border-radius:.3cqi;margin-right:.5cqi;vertical-align:.1cqi}
.hc .tag.ok{color:var(--ok);background:var(--ok-bg)}
.kpis{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.6cqi 2.4cqi;margin:0 0 .4cqi;padding-bottom:.6cqi;border-bottom:1px solid var(--rule)} .kpi{display:flex;align-items:baseline;gap:.9cqi;min-width:0} .kpis ~ .body .side{font-size:1.25cqi;gap:.7cqi}
.kpi .k-big{font-size:2.4cqi;font-weight:700;letter-spacing:-.02em;line-height:1;color:var(--accent);font-variant-numeric:tabular-nums;flex:0 0 auto;white-space:nowrap}
.kpi .k-lab{font-size:1.12cqi;color:var(--ink-2);line-height:1.22;min-width:0}
.sowhat{display:flex;gap:1.4cqi;align-items:flex-start;background:var(--accent-soft);border-left:.4cqi solid var(--accent);padding:.8cqi 1.4cqi;margin-top:.6cqi;font-size:1.4cqi;line-height:1.32;color:var(--ink)}
.sowhat b{flex:0 0 auto;color:var(--accent);font-size:1.1cqi;letter-spacing:.1em;text-transform:uppercase;padding-top:.3cqi}
.c-lab{font-size:15px;font-weight:600;fill:var(--ink)}
.c-cat{font-size:13.5px;fill:var(--ink-2)}
.c-val{font-size:13.5px;font-weight:600;fill:var(--ink);font-variant-numeric:tabular-nums}
.c-val.c-sm{font-size:12px}
.c-val.c-hl{fill:var(--accent)}
.c-note{font-size:11px;fill:var(--ink-3)}
.c-grid{stroke:var(--rule);stroke-width:1}
.c-ref{stroke:var(--ink-3);stroke-width:1;stroke-dasharray:4 4}
.tblwrap{overflow:auto;max-height:50cqi}
.tbl{width:100%%;border-collapse:collapse;font-size:1.35cqi;line-height:1.3}
.tbl th{text-align:left;font-weight:600;color:var(--ink-2);font-size:1.15cqi;letter-spacing:.04em;text-transform:uppercase;border-bottom:.18cqi solid var(--ink);padding:.5cqi .8cqi .5cqi 0}
.tbl td{padding:.62cqi .8cqi .62cqi 0;border-bottom:1px solid var(--rule);vertical-align:top;color:var(--ink)}
.tbl td:first-child{font-weight:600}
.tbl tr.hl td{background:var(--accent-soft)}
.tbl-sm{font-size:1.15cqi}
.tbl-sm td,.tbl-sm th{padding:.38cqi .5cqi .38cqi 0}
.pill{display:inline-block;padding:.1cqi .7cqi;border-radius:999px;font-size:1.1cqi;font-weight:600;white-space:nowrap;background:var(--paper-2);color:var(--ink-2)}
.pill.ok{background:var(--ok-bg);color:var(--ok)}.pill.bad{background:var(--bad-bg);color:var(--bad)}.pill.warn{background:var(--warn-bg);color:var(--warn)}
.stats{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1.6cqi 2.4cqi;align-content:start}
.stats:has(.stat:nth-child(5)){grid-template-columns:repeat(3,minmax(0,1fr))}
.stat{border-top:.25cqi solid var(--accent);padding-top:1cqi}
.s-big{font-size:3.6cqi;font-weight:700;letter-spacing:-.02em;line-height:1;color:var(--accent);font-variant-numeric:tabular-nums}
.s-lab{font-size:1.5cqi;font-weight:600;margin-top:.6cqi;color:var(--ink)}
.s-sub{font-size:1.25cqi;color:var(--ink-2);margin-top:.3cqi}
.rules{margin:0;padding:0;list-style:none;counter-reset:r;columns:2;column-gap:3cqi;font-size:1.42cqi;line-height:1.35}
.rules li{counter-increment:r;break-inside:avoid;display:flex;gap:.9cqi;margin-bottom:1cqi}
.rules li::before{content:counter(r);flex:0 0 2.4cqi;height:2.4cqi;border-radius:50%%;background:var(--accent);color:#fff;font-weight:700;font-size:1.25cqi;display:inline-flex;align-items:center;justify-content:center}
.gantt .gc{width:10cqi;text-align:center}
.gbar{display:block;height:1.4cqi;border-radius:3px;background:transparent}
.gbar.on{background:var(--accent)}
.gantt .who{color:var(--ink-2);font-weight:400}
/* portada y divisores */
.slide.cover .s{justify-content:center;background:linear-gradient(135deg,#FFFFFF 0%%,#EEF2FC 100%%)}
.cover h1{font-size:5.2cqi;line-height:1.08;margin:0;font-weight:700;letter-spacing:-.02em;max-width:70cqi;text-wrap:balance}
.cover .sub{font-size:2.2cqi;color:var(--ink-2);margin-top:1.6cqi}
.cover .meta{font-size:1.5cqi;color:var(--ink-3);margin-top:4cqi}
.cover .brand{position:absolute;top:4.2cqi;left:4.6cqi;font-size:1.3cqi;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);font-weight:700}
.slide.sec .s{justify-content:center;background:var(--accent);color:#fff}
.sec .big{font-size:9cqi;font-weight:800;line-height:1;opacity:.35}
.sec h2{font-size:4.2cqi;margin:.6cqi 0 0;font-weight:700;letter-spacing:-.015em;max-width:70cqi;text-wrap:balance}
.sec p{font-size:1.9cqi;opacity:.9;margin:1.2cqi 0 0;max-width:70cqi}
/* resumen ejecutivo */
.exec{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:3cqi;flex:1}
.exec h3{margin:0 0 1cqi;font-size:1.3cqi;letter-spacing:.08em;text-transform:uppercase;color:var(--accent)}
.exec ul{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:1.2cqi;font-size:1.45cqi;line-height:1.4;color:var(--ink)}
.exec li{padding-left:1.2cqi;border-left:.3cqi solid var(--accent-soft)}
@media (max-width:700px){ .body{grid-template-columns:minmax(0,1fr)} .side{display:none} .exec{grid-template-columns:minmax(0,1fr)} .rules{columns:1} }
@media print{ body{background:#fff;padding:0} .topbar{display:none} .slide{box-shadow:none;border-radius:0;page-break-after:always;width:100%%} .side{display:flex} }
""" % {"A": ACCENT, "I": INK, "I2": INK2, "R": RED, "G": GREEN, "AM": AMBER}

JS = """
(function(){
  var slides=[].slice.call(document.querySelectorAll('.slide'));
  var cur=0;
  function idx(){var y=window.scrollY+window.innerHeight/2;for(var i=slides.length-1;i>=0;i--){if(slides[i].offsetTop<=y)return i;}return 0;}
  function go(i){i=Math.max(0,Math.min(slides.length-1,i));slides[i].scrollIntoView({behavior:'smooth',block:'start'});}
  document.addEventListener('keydown',function(e){
    if(e.target.tagName==='INPUT')return;
    if(e.key==='ArrowRight'||e.key==='PageDown'||e.key===' '){e.preventDefault();go(idx()+1);}
    if(e.key==='ArrowLeft'||e.key==='PageUp'){e.preventDefault();go(idx()-1);}
    if(e.key==='Home'){go(0);} if(e.key==='End'){go(slides.length-1);}
  });
  // Ajuste fino: si una tabla o lista de reglas invade la banda So what, reduce su tamaño de letra por pasos.
  function fit(){
    slides.forEach(function(s){
      var sw=s.querySelector('.hc')||s.querySelector('.sowhat')||s.querySelector('.src'); var ex=s.querySelector('.ex'); var side=s.querySelector('.side');
      if(!sw||!ex)return;
      [ex,side].forEach(function(el){
        if(!el)return;
        var big=el.querySelector('.tbl,.rules,.stats')||el; var z=1; var k=0; big.style.zoom='';
        while(k<10&&big.getBoundingClientRect().bottom>sw.getBoundingClientRect().top-2){z*=0.95;big.style.zoom=z;k++;}
      });
    });
  }
  fit(); window.addEventListener('resize',fit); if(document.fonts&&document.fonts.ready){document.fonts.ready.then(fit);}
  var pos=document.getElementById('pos');
  function upd(){var i=idx();if(i!==cur){cur=i;}pos.textContent=(i+1)+' / '+slides.length;}
  window.addEventListener('scroll',upd,{passive:true});upd();
})();
"""


CAUSA_TAGS = {
    "saturacion": "Saturación: muchas piezas el mismo día",
    "solape": "Solape entre familias y equipos",
    "producto": "Producto u oferta",
    "audiencia": "Audiencia sin segmento",
    "canal": "Canal equivocado",
    "operacion": "Operación y configuración",
    "medicion": "Sin medición",
    "metodo": "Método",
}


def causa_html(s):
    tag = s.get("causa_tag")
    t = f'<span class="tag{" ok" if tag == "metodo" else ""}">{esc(CAUSA_TAGS.get(tag, tag))}</span>' if tag else ""
    return f'<p><b>Causa</b>{t}{esc(s["causa"])}</p>'


def kpis_html(s):
    k = s.get("kpis")
    if not k:
        return ""
    return '<div class="kpis">' + "".join(f'<div class="kpi"><div class="k-big">{esc(b)}</div><div class="k-lab">{esc(l)}</div></div>' for b, l in k) + "</div>"


def sowhat(s):
    t = s.get("sowhat")
    hc = ""
    if s.get("hipotesis") or s.get("causa") or s.get("impacto"):
        hc = ('<div class="hc">'
              + (f'<p><b>Hipótesis</b>{esc(s["hipotesis"])}</p>' if s.get("hipotesis") else "<p></p>")
              + (causa_html(s) if s.get("causa") else "<p></p>")
              + (f'<p><b>Si lo resolvemos</b>{esc(s["impacto"])}</p>' if s.get("impacto") else "<p></p>")
              + "</div>")
    return hc + (f'<div class="sowhat"><b>So what</b><span>{esc(t)}</span></div>' if t else "")


def build_html():
    o = []
    o.append("<title>Braze en Kueski</title>")
    o.append('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700;800&display=swap">')
    o.append(f"<style>{CSS}</style>")
    n = len(SLIDES)
    toc = "".join(f'<a href="#s{i+1}">{esc(s["num"])}. {esc(s["title"])}</a>' for i, s in section_titles())
    o.append(f'<div class="topbar"><strong>Braze en Kueski</strong><span>Auditoría enero a septiembre de 2026</span><span class="sp"></span><span class="toc"><a href="#s1">Inicio</a><a href="#s2">Resumen</a>{toc}</span><span id="pos">1 / {n}</span></div>')
    o.append('<div class="deck">')
    for i, s in enumerate(SLIDES, 1):
        k = s["kind"]
        if k == "title":
            o.append(f'<section class="slide cover" id="s{i}"><div class="s"><div class="brand">Kueski · Braze</div><h1>{esc(s["title"])}</h1><div class="sub">{esc(s["subtitle"])}</div><div class="meta">{esc(s["meta"])}</div></div><div class="num">{i}</div></section>')
        elif k == "section":
            o.append(f'<section class="slide sec" id="s{i}"><div class="s"><div class="big">{esc(s["num"])}</div><h2>{esc(s["title"])}</h2>{"<p>"+esc(s["subtitle"])+"</p>" if s.get("subtitle") else ""}</div><div class="num" style="color:#fff;opacity:.7">{i}</div></section>')
        elif k == "exec":
            cols = "".join(f'<div><h3>{esc(h)}</h3><ul>{"".join("<li>"+esc(b)+"</li>" for b in bs)}</ul></div>' for h, bs in s["groups"])
            o.append(f'<section class="slide" id="s{i}"><div class="s"><div class="tracker">Resumen ejecutivo</div><h2 class="t">{esc(s["title"])}</h2><div class="exec">{cols}</div>{sowhat(s)}<div class="src">{esc("Fuente: Sheets braze_auditoria_v4 (Insights, Plan_accion, Estándares); análisis")}</div></div><div class="num">{i}</div></section>')
        else:
            side = s.get("side") or []
            ex = render_exhibit(s["exhibit"])
            sidehtml = "".join(f"<p>{esc(b)}</p>" for b in side)
            body = f'{kpis_html(s)}<div class="body{"" if side else " full"}"><div class="ex">{ex}</div>{"<div class=\"side\">"+sidehtml+"</div>" if side else ""}</div>'
            o.append(f'<section class="slide" id="s{i}"><div class="s"><div class="tracker">{esc(s.get("tracker",""))}</div><h2 class="t{" t-long" if len(s["title"]) > 150 else ""}{" t-xl" if len(s["title"]) > 215 else ""}">{esc(s["title"])}</h2>{body}{sowhat(s)}<div class="src">{esc(s.get("source",""))}</div></div><div class="num">{i}</div></section>')
    o.append("</div>")
    o.append(f"<script>{JS}</script>")
    path = os.path.join(OUT, "BRAZE_KUESKI_DECK.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(o))
    return path


# ----------------------------------------------------------------------------
# PPTX
# ----------------------------------------------------------------------------

def build_pptx():
    from pptx import Presentation
    from pptx.chart.data import CategoryChartData
    from pptx.dml.color import RGBColor
    from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION, XL_TICK_LABEL_POSITION
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from pptx.util import Inches, Pt, Emu

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]
    C = lambda h: RGBColor.from_string(h)
    FONT = "Calibri"

    def tb(slide, x, y, w, h, text, size=14, bold=False, color=INK, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, font=FONT):
        s = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = s.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.02)
        tf.margin_top = tf.margin_bottom = Inches(0.02)
        tf.vertical_anchor = anchor
        lines = text if isinstance(text, list) else [text]
        for i, ln in enumerate(lines):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = align
            r = p.add_run()
            r.text = ln
            r.font.size = Pt(size)
            r.font.bold = bold
            r.font.name = font
            r.font.color.rgb = C(color)
        return s

    def bullets(slide, x, y, w, h, items, size=12, color=INK2):
        s = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = s.text_frame
        tf.word_wrap = True
        for i, it in enumerate(items):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.space_after = Pt(6)
            r = p.add_run()
            r.text = "•  " + it
            r.font.size = Pt(size)
            r.font.name = FONT
            r.font.color.rgb = C(color)
        return s

    def rect(slide, x, y, w, h, color, shape=MSO_SHAPE.RECTANGLE):
        s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
        s.fill.solid()
        s.fill.fore_color.rgb = C(color)
        s.line.fill.background()
        s.shadow.inherit = False
        return s

    def hc_box(slide, s):
        if not (s.get("hipotesis") or s.get("causa") or s.get("impacto")):
            return
        ln = slide.shapes.add_connector(1, Inches(0.6), Inches(5.42), Inches(12.73), Inches(5.42))
        ln.line.color.rgb = C("E3E6EB")
        widths = (3.55, 4.75, 3.55)
        x = 0.6
        for j, (lab, key) in enumerate((("HIPÓTESIS", "hipotesis"), ("CAUSA", "causa"), ("SI LO RESOLVEMOS", "impacto"))):
            wj = widths[j]
            if s.get(key):
                box = slide.shapes.add_textbox(Inches(x), Inches(5.46), Inches(wj - 0.12), Inches(0.62))
                tf = box.text_frame
                tf.word_wrap = True
                tf.margin_left = tf.margin_right = Inches(0.02)
                tf.margin_top = tf.margin_bottom = Inches(0.01)
                p = tf.paragraphs[0]
                r = p.add_run(); r.text = lab + "  "; r.font.size = Pt(7); r.font.bold = True; r.font.color.rgb = C(INK); r.font.name = FONT
                if key == "causa" and s.get("causa_tag"):
                    r = p.add_run(); r.text = CAUSA_TAGS.get(s["causa_tag"], s["causa_tag"]).upper() + "  "; r.font.size = Pt(7); r.font.bold = True; r.font.color.rgb = C(RED); r.font.name = FONT
                r = p.add_run(); r.text = s[key]; r.font.size = Pt(8.5); r.font.color.rgb = C(INK2); r.font.name = FONT
            x += wj + 0.08

    def kpis_box(slide, s):
        k = s.get("kpis")
        if not k:
            return 0
        cw = 12.13 / 3
        for j, (big, lab) in enumerate(k):
            x = 0.6 + j * cw
            tb(slide, x, 1.9, cw - 0.3, 0.45, big, 22, True, ACCENT)
            tb(slide, x, 2.33, cw - 0.3, 0.3, lab, 9.5, False, INK2)
        ln = slide.shapes.add_connector(1, Inches(0.6), Inches(2.68), Inches(12.73), Inches(2.68))
        ln.line.color.rgb = C("E3E6EB")
        return 0.85

    def sowhat_box(slide, s):
        hc_box(slide, s)
        t = s.get("sowhat")
        if not t:
            return
        rect(slide, 0.6, 6.1, 12.13, 0.72, "E4EAFB")
        rect(slide, 0.6, 6.1, 0.06, 0.72, ACCENT)
        box = slide.shapes.add_textbox(Inches(0.8), Inches(6.1), Inches(11.8), Inches(0.72))
        tf = box.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = tf.margin_right = Inches(0.05)
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = "SO WHAT   "
        r.font.size = Pt(9)
        r.font.bold = True
        r.font.name = FONT
        r.font.color.rgb = C(ACCENT)
        r = p.add_run()
        r.text = t
        r.font.size = Pt(11)
        r.font.name = FONT
        r.font.color.rgb = C(INK)

    def chrome(slide, num, tracker, title, source):
        if tracker:
            tb(slide, 9.0, 0.25, 3.9, 0.3, tracker.upper(), 9, False, "8A909B", PP_ALIGN.RIGHT)
        tb(slide, 0.6, 0.5, 12.1, 1.1, title, 22 if len(title) <= 110 else (19 if len(title) <= 150 else (17 if len(title) <= 215 else 15.5)), True, INK, anchor=MSO_ANCHOR.TOP)
        rect(slide, 0.6, 1.62, 0.8, 0.05, ACCENT)
        if source:
            ln = slide.shapes.add_connector(1, Inches(0.6), Inches(6.95), Inches(12.73), Inches(6.95))
            ln.line.color.rgb = C("E3E6EB")
            tb(slide, 0.6, 7.0, 11.2, 0.35, source, 8.5, False, "8A909B")
        tb(slide, 12.3, 7.0, 0.45, 0.35, str(num), 9, False, "8A909B", PP_ALIGN.RIGHT)

    def numfmt(fmt):
        return {"pct0": '0" %"', "pct1": '0.0" %"', "pct2": '0.00" %"', "M": '0.0" M"', "MXN": '0.00" M"'}.get(fmt, "General")

    def style_axis(ax, size=10, visible=True):
        ax.tick_labels.font.size = Pt(size)
        ax.tick_labels.font.name = FONT
        ax.tick_labels.font.color.rgb = C(INK2)
        ax.format.line.color.rgb = C("E3E6EB")
        ax.has_major_gridlines = False
        if not visible:
            ax.visible = False

    def add_chart(slide, kind, x, y, w, h, cats, series, fmt, highlight=(), legend=False, title=None, ymin=None, ymax=None, labels="all"):
        cd = CategoryChartData()
        cd.categories = cats
        for name, vals in series:
            cd.add_series(name, vals)
        gf = slide.shapes.add_chart(kind, Inches(x), Inches(y), Inches(w), Inches(h), cd)
        ch = gf.chart
        ch.font.name = FONT
        ch.font.size = Pt(10)
        ch.has_legend = legend
        if legend:
            ch.legend.position = XL_LEGEND_POSITION.TOP
            ch.legend.include_in_layout = False
            ch.legend.font.size = Pt(9)
        if title:
            ch.has_title = True
            ch.chart_title.text_frame.text = title
            p = ch.chart_title.text_frame.paragraphs[0]
            p.runs[0].font.size = Pt(11)
            p.runs[0].font.bold = True
            p.runs[0].font.name = FONT
            p.runs[0].font.color.rgb = C(INK)
        else:
            ch.has_title = False
        plot = ch.plots[0]
        if labels == "ends":
            # solo primer y último punto (y los resaltados): evita choques en gráficas chicas
            plot.has_data_labels = False
            keep = {0, len(cats) - 1} | set(i for i in highlight if isinstance(i, int))
            for sr in plot.series:
                vals = list(sr.values)
                for i in sorted(keep):
                    if i < 0 or i >= len(vals) or vals[i] is None:
                        continue
                    dlb = sr.points[i].data_label
                    dlb.has_text_frame = True
                    dlb.text_frame.text = fmtv(vals[i], fmt)
                    r0 = dlb.text_frame.paragraphs[0].runs[0]
                    r0.font.size = Pt(8); r0.font.name = FONT; r0.font.color.rgb = C(INK)
                    try:
                        dlb.position = XL_LABEL_POSITION.OUTSIDE_END if kind != XL_CHART_TYPE.LINE_MARKERS else XL_LABEL_POSITION.ABOVE
                    except Exception:
                        pass
        else:
            plot.has_data_labels = True
            dl = plot.data_labels
            dl.number_format = numfmt(fmt)
            dl.number_format_is_linked = False
            dl.font.size = Pt(9)
            dl.font.name = FONT
            dl.font.color.rgb = C(INK)
            try:
                dl.position = XL_LABEL_POSITION.OUTSIDE_END if kind != XL_CHART_TYPE.LINE_MARKERS else XL_LABEL_POSITION.ABOVE
            except Exception:
                pass
        if kind in (XL_CHART_TYPE.BAR_CLUSTERED, XL_CHART_TYPE.COLUMN_CLUSTERED):
            plot.gap_width = 60 if len(series) == 1 else 80
            plot.overlap = -10 if len(series) > 1 else 0
        style_axis(ch.category_axis, 10)
        va = ch.value_axis
        style_axis(va, 9, visible=False)
        va.has_major_gridlines = False
        if ymin is not None:
            va.minimum_scale = ymin
        if ymax is not None:
            va.maximum_scale = ymax
        if kind == XL_CHART_TYPE.BAR_CLUSTERED:
            ch.category_axis.reverse_order = True
            ch.category_axis.tick_label_position = XL_TICK_LABEL_POSITION.LOW
        pal = [ACCENT, GRAY, GRAY2]
        for si, s in enumerate(plot.series):
            if kind == XL_CHART_TYPE.LINE_MARKERS:
                s.format.line.color.rgb = C(ACCENT)
                s.format.line.width = Pt(2.25)
                s.marker.style = 8
                s.marker.size = 7
                s.marker.format.fill.solid()
                s.marker.format.fill.fore_color.rgb = C(ACCENT)
                s.marker.format.line.color.rgb = C("FFFFFF")
                s.smooth = False
            else:
                s.format.fill.solid()
                s.format.fill.fore_color.rgb = C(pal[si] if len(series) > 1 else GRAY)
                s.invert_if_negative = False
                if len(series) == 1:
                    for pi in range(len(cats)):
                        pt = s.points[pi]
                        pt.format.fill.solid()
                        pt.format.fill.fore_color.rgb = C(ACCENT if pi in highlight else GRAY)
        return ch

    def add_table(slide, ex, x, y, w, h):
        head, rows = ex["head"], ex["rows"]
        sc = ex.get("status_col")
        scs = sc if isinstance(sc, list) else ([sc] if sc is not None else [])
        hr = set(ex.get("highlight_rows", []))
        nr, nc = len(rows) + 1, len(head)
        shp = slide.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(w), Inches(h))
        t = shp.table
        small = ex.get("small") or nr > 11 or nc > 6
        fs = 8 if small else (9 if nr >= 8 else 10)
        rh_ = min(0.28, (h - 0.15) / nr)
        if rh_ < 0.24:
            fs = min(fs, 7.5 if rh_ < 0.2 else 8)
        # anchos: primera columna más ancha cuando hay texto largo
        lens = [max(len(str(r[c])) for r in [head] + rows) for c in range(nc)]
        tot = sum(min(l, 60) for l in lens)
        for c in range(nc):
            t.columns[c].width = Emu(int(Inches(w) * min(lens[c], 60) / tot))
        for ri in range(nr):
            t.rows[ri].height = Inches(rh_)
            for ci in range(nc):
                cell = t.cell(ri, ci)
                txt = head[ci] if ri == 0 else str(rows[ri - 1][ci])
                cell.margin_left = cell.margin_right = Inches(0.05)
                cell.margin_top = cell.margin_bottom = Inches(0.02)
                cell.fill.solid()
                if ri == 0:
                    cell.fill.fore_color.rgb = C("FFFFFF")
                elif (ri - 1) in hr:
                    cell.fill.fore_color.rgb = C("E4EAFB")
                else:
                    cell.fill.fore_color.rgb = C("FFFFFF" if ri % 2 else "F6F7F9")
                tf = cell.text_frame
                tf.word_wrap = True
                p = tf.paragraphs[0]
                r = p.add_run()
                r.text = txt
                r.font.name = FONT
                r.font.size = Pt(fs if ri else fs - 1)
                r.font.bold = (ri == 0) or (ci == 0)
                col = INK2 if ri == 0 else INK
                if ri and ci in scs:
                    k = status_class(txt)
                    col = {"ok": GREEN, "bad": RED, "warn": AMBER}.get(k, INK)
                    r.font.bold = True
                r.font.color.rgb = C(col)
        return shp

    def add_stats(slide, ex, x, y, w, h):
        items = ex["items"]
        cols = 3 if len(items) > 4 else 2
        rows = (len(items) + cols - 1) // cols
        cw, rh = w / cols, h / rows
        for i, (big, lab, sub) in enumerate(items):
            cx, cy = x + (i % cols) * cw, y + (i // cols) * rh
            rect(slide, cx, cy, cw - 0.3, 0.04, ACCENT)
            tb(slide, cx, cy + 0.12, cw - 0.3, 0.6, big, 26, True, ACCENT)
            tb(slide, cx, cy + 0.78, cw - 0.3, 0.4, lab, 12, True, INK)
            tb(slide, cx, cy + 1.12, cw - 0.3, 0.6, sub, 9.5, False, INK2)

    def add_rules(slide, ex, x, y, w, h):
        items = ex["items"]
        half = (len(items) + 1) // 2
        fs_ = 11 if h >= 3.2 else (9.5 if h >= 2.6 else 8.5)
        for col in range(2):
            sub = items[col * half:(col + 1) * half]
            s = slide.shapes.add_textbox(Inches(x + col * w / 2), Inches(y), Inches(w / 2 - 0.3), Inches(h))
            tf = s.text_frame
            tf.word_wrap = True
            for i, it in enumerate(sub):
                p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                p.space_after = Pt(7 if fs_ >= 11 else 4)
                r = p.add_run()
                r.text = f"{col*half+i+1}.  "
                r.font.bold = True
                r.font.size = Pt(fs_)
                r.font.name = FONT
                r.font.color.rgb = C(ACCENT)
                r2 = p.add_run()
                r2.text = it
                r2.font.size = Pt(fs_)
                r2.font.name = FONT
                r2.font.color.rgb = C(INK)

    def add_gantt(slide, ex, x, y, w, h):
        cols = ex["cols"]
        rows = ex["rows"]
        name_w, who_w = 4.6, 2.6
        cw = (w - name_w - who_w) / len(cols)
        rh = min(0.42, (h - 0.4) / len(rows))
        for j, c in enumerate(cols):
            tb(slide, x + name_w + j * cw, y, cw, 0.3, c, 9, True, INK2, PP_ALIGN.CENTER)
        ln = slide.shapes.add_connector(1, Inches(x), Inches(y + 0.32), Inches(x + w), Inches(y + 0.32))
        ln.line.color.rgb = C(INK)
        for i, (name, cells, who) in enumerate(rows):
            yy = y + 0.4 + i * rh
            tb(slide, x, yy, name_w - 0.1, rh, name, 9.5, True, INK, anchor=MSO_ANCHOR.MIDDLE)
            for j, v in enumerate(cells):
                if v:
                    rect(slide, x + name_w + j * cw + 0.08, yy + rh * 0.3, cw - 0.16, rh * 0.4, ACCENT)
            tb(slide, x + name_w + len(cols) * cw + 0.1, yy, who_w - 0.1, rh, who, 9, False, INK2, anchor=MSO_ANCHOR.MIDDLE)
            ln = slide.shapes.add_connector(1, Inches(x), Inches(yy + rh), Inches(x + w), Inches(yy + rh))
            ln.line.color.rgb = C("E3E6EB")

    def add_waterfall(slide, ex, x, y, w, h):
        cats, vals = ex["cats"], ex["vals"]
        n = len(cats)
        base, delta, ends = [], [], []
        run = 0
        for i, v in enumerate(vals):
            if i == 0 or i == n - 1:
                base.append(0); delta.append(0); ends.append(v); run = v
            else:
                run2 = run + v
                base.append(min(run, run2)); delta.append(abs(v)); ends.append(0); run = run2
        cd = CategoryChartData()
        cd.categories = cats
        cd.add_series("base", base)
        cd.add_series("Totales", ends)
        cd.add_series("Ahorro", delta)
        gf = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_STACKED, Inches(x), Inches(y), Inches(w), Inches(h), cd)
        ch = gf.chart
        ch.font.name = FONT
        ch.font.size = Pt(10)
        ch.has_legend = False
        ch.has_title = True
        ch.chart_title.text_frame.text = ex.get("label", "")
        r0 = ch.chart_title.text_frame.paragraphs[0].runs[0]
        r0.font.size = Pt(11); r0.font.bold = True; r0.font.name = FONT; r0.font.color.rgb = C(INK)
        plot = ch.plots[0]
        plot.gap_width = 55
        style_axis(ch.category_axis, 9)
        style_axis(ch.value_axis, 9, visible=False)
        s0, s1, s2 = plot.series
        s0.format.fill.background()
        s1.format.fill.solid(); s1.format.fill.fore_color.rgb = C(INK2)
        s1.points[n - 1].format.fill.solid(); s1.points[n - 1].format.fill.fore_color.rgb = C(ACCENT)
        s2.format.fill.solid(); s2.format.fill.fore_color.rgb = C(RED)
        unit = ex.get("unit", " M")
        for s, nf in ((s1, f'0.00"{unit}";;'), (s2, f'"−"0.00"{unit}";;')):
            s.data_labels.show_value = True
            s.data_labels.number_format = nf
            s.data_labels.number_format_is_linked = False
            s.data_labels.font.size = Pt(9)
            s.data_labels.font.name = FONT
            s.data_labels.font.color.rgb = C(INK)
            try:
                s.data_labels.position = XL_LABEL_POSITION.INSIDE_END
            except Exception:
                pass
        if ex.get("note"):
            tb(slide, x, y + h, w, 0.3, ex["note"], 9, False, INK2)

    # ---- Gráficas multivariable (PPTX) -------------------------------------
    PALP = [ACCENT, "B5342B", "1F9E89", "A8720F", "7C5CC4"]

    def restyle_lines(ch, n, ramp=False, emph=None):
        plot = ch.plots[0]
        if n > 1:
            plot.has_data_labels = False
        cols = [c.lstrip("#") for c in _ramp(n)] if ramp else PALP
        for si, s in enumerate(plot.series):
            col = cols[si % len(cols)] if n > 1 else ACCENT
            if emph is not None and si not in emph:
                col = GRAY
            s.format.line.color.rgb = C(col)
            s.format.line.width = Pt(2.25 if (emph is None or si in emph) else 1.25)
            s.marker.format.fill.solid()
            s.marker.format.fill.fore_color.rgb = C(col)

    def add_multiline(slide, ex, x, y, w, h):
        ch = add_chart(slide, XL_CHART_TYPE.LINE_MARKERS, x, y, w, h, ex["cats"], ex["series"], ex.get("fmt", ""), set(ex.get("highlight", [])), legend=len(ex["series"]) > 1, title=ex.get("label"), ymin=ex.get("ymin"), ymax=ex.get("ymax"))
        restyle_lines(ch, len(ex["series"]), bool(ex.get("ramp")), ex.get("emph"))
        if ex.get("ref"):
            tb(slide, x, y + h, w, 0.3, f"Línea de referencia: {ex['ref'][1]}", 9, False, INK2)

    def add_panels(slide, ex, x, y, w, h):
        n = len(ex["panels"])
        ph = (h - 0.1 * (n - 1)) / n
        hl = set(ex.get("highlight", []))
        for i, p in enumerate(ex["panels"]):
            yy = y + i * (ph + 0.1)
            if p.get("kind", "col") == "col":
                add_chart(slide, XL_CHART_TYPE.COLUMN_CLUSTERED, x, yy, w, ph, ex["cats"], p["series"], p.get("fmt", ""), hl, title=p["title"])
            else:
                ch = add_chart(slide, XL_CHART_TYPE.LINE_MARKERS, x, yy, w, ph, ex["cats"], p["series"], p.get("fmt", ""), hl, legend=len(p["series"]) > 1, title=p["title"], ymin=p.get("ymin"), ymax=p.get("ymax"))
                restyle_lines(ch, len(p["series"]), bool(p.get("ramp") or ex.get("ramp")), p.get("emph"))

    def add_smallmult(slide, ex, x, y, w, h):
        cells = ex["cells"]
        hl = set(ex.get("highlight", []))
        cw, chh = w / 2, h / 2
        for i, c in enumerate(cells):
            cx = x + (i % 2) * cw
            cy = y + (i // 2) * chh
            tb(slide, cx + 0.1, cy, cw - 0.2, 0.25, c["title"], 10, True, ACCENT)
            n1, v1 = c["vol"]; n2, v2 = c["resp"]
            half_w = (cw - 0.2) / 2
            add_chart(slide, XL_CHART_TYPE.COLUMN_CLUSTERED, cx, cy + 0.22, half_w, chh - 0.3, c["cats"], [(n1, v1)], c.get("fmt_vol", "M"), hl, title=n1, labels="ends")
            add_chart(slide, XL_CHART_TYPE.LINE_MARKERS, cx + half_w + 0.1, cy + 0.22, half_w, chh - 0.3, c["cats"], [(n2, v2)], c.get("fmt_resp", "pct1"), hl, title=n2, ymin=c.get("ymin"), labels="ends")

    def add_scatter(slide, ex, x, y, w, h):
        from pptx.chart.data import XyChartData
        from lxml import etree
        groups = ex["groups"]
        passmode = ex.get("mode") == "pass"
        n = len(ex["panels"])
        pw = (w - 0.3 * (n - 1)) / n
        for pi, p in enumerate(ex["panels"]):
            cd = XyChartData()
            if passmode:
                groups = ["No pasa el mínimo", "Pasa el mínimo"]
                thr = p["ref"][0]
                byg = {g: [] for g in groups}
                for pt in p["pts"]:
                    byg[groups[1] if pt["y"] >= thr else groups[0]].append((pt["x"], min(pt["y"], p["ymax"])))
            else:
                byg = {g: [] for g in groups}
                for pt in p["pts"]:
                    byg.setdefault(pt["g"], []).append((pt["x"], min(pt["y"], p["ymax"])))
            for g in groups:
                s = cd.add_series(g)
                for xv, yv in byg.get(g, []):
                    s.add_data_point(xv, yv)
            px = x + pi * (pw + 0.3)
            gf = slide.shapes.add_chart(XL_CHART_TYPE.XY_SCATTER, Inches(px), Inches(y), Inches(pw), Inches(h), cd)
            ch = gf.chart
            ch.font.name = FONT; ch.font.size = Pt(9)
            ch.has_title = True
            ch.chart_title.text_frame.text = p["title"]
            r = ch.chart_title.text_frame.paragraphs[0].runs[0]
            r.font.size = Pt(11); r.font.bold = True; r.font.name = FONT; r.font.color.rgb = C(INK)
            ch.has_legend = pi == 0
            if ch.has_legend:
                ch.legend.position = XL_LEGEND_POSITION.TOP; ch.legend.include_in_layout = False; ch.legend.font.size = Pt(9)
            plot = ch.plots[0]
            for si, s in enumerate(plot.series):
                s.format.line.fill.background()
                s.marker.style = 8; s.marker.size = 6
                s.marker.format.fill.solid(); s.marker.format.fill.fore_color.rgb = C((GRAY, "1F9E89")[si] if passmode else PALP[si % len(PALP)])
                s.marker.format.line.color.rgb = C("FFFFFF")
            va = ch.value_axis
            va.maximum_scale = p["ymax"]; va.minimum_scale = 0
            va.has_major_gridlines = True
            va.major_gridlines.format.line.color.rgb = C("E3E6EB")
            va.tick_labels.font.size = Pt(9)
            va.tick_labels.number_format = numfmt(p.get("fmt", "pct1")); va.tick_labels.number_format_is_linked = False
            ca = ch.category_axis
            ca.minimum_scale = p.get("xmin", 2e5); ca.maximum_scale = p.get("xmax", 2e7)
            ca.has_major_gridlines = False
            ca.tick_labels.font.size = Pt(9)
            ca.tick_labels.number_format = '#,##0,,"M"'; ca.tick_labels.number_format_is_linked = False
            # escala logarítmica en x (eje de valores horizontal)
            ns = "{http://schemas.openxmlformats.org/drawingml/2006/chart}"
            for ax in ch._chartSpace.iter(ns + "valAx"):
                axid = ax.find(ns + "axId").get("val")
                pos = ax.find(ns + "axPos").get("val")
                if pos == "b":
                    sc = ax.find(ns + "scaling")
                    lb = etree.SubElement(sc, ns + "logBase"); lb.set("val", "10")
                    sc.insert(0, lb)
                    ax.find(ns + "majorGridlines") is None or sc.getparent().remove(ax.find(ns + "majorGridlines"))
            if p.get("ref"):
                tb(slide, px, y + h, pw, 0.3, f"Mínimo: {p['ref'][1]}", 8.5, False, INK2)

    def add_dotrange(slide, ex, x, y, w, h):
        rowsx = ex["rows"]
        fmt = ex.get("fmt", "pct2")
        xmax = ex["xmax"]
        labw = 1.5
        pw = w - labw - 0.9
        top = y + 0.5
        rh = min(0.75, (h - 0.9) / len(rowsx))
        tb(slide, x, y, w, 0.3, ex.get("label", ""), 11, True, INK)
        X = lambda v: x + labw + min(v, xmax) / xmax * pw
        tb(slide, x + labw, y + 0.26, w - labw, 0.25, "Punto gris: una pieza. Banda: promedio ± 1 desviación estándar. Línea azul: promedio. Línea punteada: mediana.", 8, False, INK2)
        import random
        rnd = random.Random(7)
        for i, r in enumerate(rowsx):
            cy = top + i * rh + rh / 2
            tb(slide, x, cy - 0.2, labw - 0.1, 0.25, r["cat"], 10, True, INK, PP_ALIGN.RIGHT)
            tb(slide, x, cy + 0.02, labw - 0.1, 0.22, f"{r['n']} piezas", 8, False, INK2, PP_ALIGN.RIGHT)
            ln = slide.shapes.add_connector(1, Inches(x + labw), Inches(cy), Inches(x + labw + pw), Inches(cy)); ln.line.color.rgb = C("E3E6EB")
            lo, hi = max(0, r["mean"] - r["sd"]), r["mean"] + r["sd"]
            rect(slide, X(lo), cy - 0.16, max(0.02, X(hi) - X(lo)), 0.32, "E4EAFB")
            for v, wgt in r["pts"]:
                d = 0.07 if wgt > 1e6 else 0.05
                o = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(X(v) - d / 2), Inches(cy + rnd.uniform(-0.1, 0.1) - d / 2), Inches(d), Inches(d))
                o.fill.solid(); o.fill.fore_color.rgb = C("A3AAB5"); o.line.fill.background(); o.shadow.inherit = False
            m = slide.shapes.add_connector(1, Inches(X(r["median"])), Inches(cy - 0.18), Inches(X(r["median"])), Inches(cy + 0.18)); m.line.color.rgb = C(INK); m.line.width = Pt(1.5); m.line.dash_style = 4
            a = slide.shapes.add_connector(1, Inches(X(r["mean"])), Inches(cy - 0.18), Inches(X(r["mean"])), Inches(cy + 0.18)); a.line.color.rgb = C(ACCENT); a.line.width = Pt(3)
            tb(slide, x + labw + pw + 0.05, cy - 0.2, 0.85, 0.22, fmtv(r["mean"], fmt), 9, True, INK)
            tb(slide, x + labw + pw + 0.05, cy + 0.0, 0.85, 0.22, "± " + fmtv(r["sd"], fmt), 8, False, INK2)
        if ex.get("ref"):
            rv, rl = ex["ref"]
            rl_ = slide.shapes.add_connector(1, Inches(X(rv)), Inches(top), Inches(X(rv)), Inches(top + len(rowsx) * rh)); rl_.line.color.rgb = C(INK2); rl_.line.dash_style = 4
            tb(slide, X(rv) + 0.05, top - 0.02, 2.5, 0.22, rl, 8, False, INK2)
        for t in range(0, 5):
            v = xmax * t / 4
            tb(slide, X(v) - 0.4, top + len(rowsx) * rh + 0.02, 0.8, 0.22, fmtv(v, fmt), 8, False, INK2, PP_ALIGN.CENTER)

    def add_heatmap(slide, ex, x, y, w, h):
        cols, rws, M, share = ex["cols"], ex["rows"], ex["matrix"], ex.get("share")
        rshare = ex.get("row_share")
        fmt = ex.get("fmt", "pct2")
        nr = len(rws) + 1 + (1 if share else 0)
        nc = len(cols) + 1 + (1 if rshare else 0)
        rh_ = min(0.4, (h - 0.3) / nr)
        shp = slide.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(w), Inches(rh_ * nr))
        t = shp.table
        lw = ex.get("labw_in", 1.7)
        t.columns[0].width = Inches(lw)
        for c in range(1, nc):
            t.columns[c].width = Emu(int(Inches(w - lw) / (nc - 1)))
        vals = [v for row in M for v in row if v is not None]
        lo, hi = min(vals), max(vals)
        grid = [["", *cols, *([ex.get("share_label", "% de los envíos")] if rshare else [])]]
        if share:
            grid.append([ex.get("share_label", "% de los envíos"), *[f"{v:.0f} %" for v in share]])
        fmts = ex.get("fmts")
        colrange = []
        for j in range(len(cols)):
            cv = [row[j] for row in M if row[j] is not None]
            colrange.append((min(cv), max(cv)) if cv else (0, 1))
        for k, (r, row) in enumerate(zip(rws, M)):
            grid.append([r, *[fmtv(v, fmts[j] if fmts else fmt) if v is not None else "" for j, v in enumerate(row)], *([f"{rshare[k]:.0f} %"] if rshare else [])])
        for ri, row in enumerate(grid):
            t.rows[ri].height = Inches(rh_)
            for ci, val in enumerate(row):
                cell = t.cell(ri, ci)
                cell.text = str(val)
                cell.margin_left = cell.margin_right = Inches(0.05)
                cell.margin_top = cell.margin_bottom = Inches(0.02 if rh_ < 0.32 else 0.05)
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                cell.fill.solid()
                fill, color, bold = "FFFFFF", INK, ri == 0 or ci == 0
                mi = ri - (2 if share else 1)
                if ri >= (2 if share else 1) and 1 <= ci <= len(cols) and M[mi][ci - 1] is not None:
                    v = M[mi][ci - 1]
                    if ex.get("row_scale"):
                        rv = [q for q in M[mi] if q is not None]
                        lo, hi = min(rv), max(rv)
                    if ex.get("col_scale"):
                        lo, hi = colrange[ci - 1]
                    tt = (v - lo) / (hi - lo) if hi > lo else 0
                    fill = _mix("#FFFFFF", "#" + ACCENT, 0.08 + 0.92 * tt).lstrip("#")
                    color = "FFFFFF" if tt > 0.55 else INK
                elif share and ri == 1 and ci >= 1:
                    fill = "F6F7F9"
                elif rshare and ri >= 1 and ci == nc - 1:
                    fill = "F6F7F9"; color = INK2
                cell.fill.fore_color.rgb = C(fill)
                for p in cell.text_frame.paragraphs:
                    p.alignment = PP_ALIGN.CENTER if ci >= 1 else PP_ALIGN.LEFT
                    for r_ in p.runs:
                        r_.font.size = Pt((9 if ri else 8.5) if rh_ >= 0.32 else (7.5 if ri else 7)); r_.font.bold = bold; r_.font.name = FONT; r_.font.color.rgb = C(color if ri else INK2)
        if rh_ >= 0.3:
            tb(slide, x, y + rh_ * nr + 0.02, w, 0.25, ex.get("label", ""), 9, False, INK2)


    # ---- Rasterizado de las gráficas nuevas (regresión, campana, velas) ----
    import subprocess, tempfile
    RDIR = os.path.join(OUT, "raster")
    os.makedirs(RDIR, exist_ok=True)
    todo = [(i, s["exhibit"]) for i, s in enumerate(SLIDES, 1) if s.get("exhibit", {}).get("type") in RASTER_TYPES]
    if todo:
        page = ['<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700&display=swap">',
                f"<style>{CSS}</style><style>body{{background:#fff;padding:0}} .box{{width:1520px;background:#fff;padding:8px}} .chart{{max-height:none;height:auto}}</style>"]
        for i, ex in todo:
            page.append(f'<div class="box" id="r{i}">{render_exhibit(ex)}</div>')
        hp = os.path.join(RDIR, "raster.html")
        with open(hp, "w", encoding="utf-8") as fh:
            fh.write("\n".join(page))
        js = os.path.join(HERE, "deck_raster.js")
        env = dict(os.environ, NODE_PATH="/opt/node-tools/node_modules")
        subprocess.run(["node", js, hp, RDIR, *[str(i) for i, _ in todo]], check=True, env=env)

    def add_raster(slide, i, x, y, w, h):
        png = os.path.join(RDIR, f"r{i}.png")
        from PIL import Image
        iw, ih = Image.open(png).size
        ar = iw / ih
        pw, ph = w, w / ar
        if ph > h:
            ph, pw = h, h * ar
        slide.shapes.add_picture(png, Inches(x), Inches(y), Inches(pw), Inches(ph))

    def exhibit(slide, ex, x, y, w, h, idx=None):
        t = ex["type"]
        fmt = ex.get("fmt", "")
        hl = set(ex.get("highlight", []))
        if t in RASTER_TYPES:
            add_raster(slide, idx, x, y, w, h); return
        if t == "multiline":
            add_multiline(slide, ex, x, y, w, h); return
        if t == "panels":
            add_panels(slide, ex, x, y, w, h); return
        if t == "smallmult":
            add_smallmult(slide, ex, x, y, w, h); return
        if t == "scatter":
            add_scatter(slide, ex, x, y, w, h); return
        if t == "dotrange":
            add_dotrange(slide, ex, x, y, w, h); return
        if t == "heatmap":
            add_heatmap(slide, ex, x, y, w, h); return
        if t == "hbar":
            notes = ex.get("notes")
            cats = ex["cats"] if not notes else [f"{c}  ({n})" if n else c for c, n in zip(ex["cats"], notes)]
            add_chart(slide, XL_CHART_TYPE.BAR_CLUSTERED, x, y, w, h, cats, [(ex.get("label", ""), ex["vals"])], fmt, hl, title=ex.get("label"))
        elif t == "hbar2":
            add_chart(slide, XL_CHART_TYPE.BAR_CLUSTERED, x, y, w, h, ex["cats"], ex["series"], fmt, hl, legend=len(ex["series"]) > 1, title=None if len(ex["series"]) > 1 else ex["series"][0][0], ymax=ex.get("max"))
        elif t == "colline":
            n1, v1 = ex["cols"]; n2, v2 = ex["line"]
            add_chart(slide, XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, w, h / 2 - 0.05, ex["cats"], [(n1, v1)], "M" if "(M)" in n1 else "", hl, title=n1)
            add_chart(slide, XL_CHART_TYPE.LINE_MARKERS, x, y + h / 2 + 0.05, w, h / 2 - 0.05, ex["cats"], [(n2, v2)], "pct2" if "%" in n2 else "pct1", hl, title=n2)
        elif t == "line":
            n1, v1 = ex["series"][0]
            add_chart(slide, XL_CHART_TYPE.LINE_MARKERS, x, y, w, h, ex["cats"], [(n1, v1)], "pct0", hl, title=n1, ymin=ex.get("ymin"), ymax=ex.get("ymax"))
            if ex.get("ref"):
                tb(slide, x, y + h, w, 0.3, f"Línea de referencia: {ex['ref'][1]}", 9, False, INK2)
        elif t == "waterfall":
            add_waterfall(slide, ex, x, y, w, h - 0.3)
        elif t == "table":
            add_table(slide, ex, x, y, w, h)
        elif t == "stats":
            add_stats(slide, ex, x, y, w, h)
        elif t == "rules":
            add_rules(slide, ex, x, y, w, h)
        elif t == "gantt":
            add_gantt(slide, ex, x, y, w, h)

    for i, s in enumerate(SLIDES, 1):
        sl = prs.slides.add_slide(blank)
        k = s["kind"]
        if k == "title":
            rect(sl, 0, 0, 13.333, 7.5, "FFFFFF")
            rect(sl, 0, 0, 0.25, 7.5, ACCENT)
            tb(sl, 0.9, 0.6, 6, 0.4, "KUESKI · BRAZE", 11, True, ACCENT)
            tb(sl, 0.9, 2.3, 9.5, 1.8, s["title"], 40, True, INK)
            tb(sl, 0.9, 4.2, 9.5, 0.6, s["subtitle"], 18, False, INK2)
            tb(sl, 0.9, 5.6, 9.5, 0.4, s["meta"], 12, False, "8A909B")
        elif k == "section":
            rect(sl, 0, 0, 13.333, 7.5, ACCENT)
            tb(sl, 0.9, 1.6, 6, 1.4, s["num"], 72, True, "FFFFFF")
            tb(sl, 0.9, 3.2, 10, 1.2, s["title"], 32, True, "FFFFFF")
            if s.get("subtitle"):
                tb(sl, 0.9, 4.4, 10, 0.8, s["subtitle"], 16, False, "FFFFFF")
            tb(sl, 12.3, 7.0, 0.45, 0.35, str(i), 9, False, "FFFFFF", PP_ALIGN.RIGHT)
        elif k == "exec":
            chrome(sl, i, "Resumen ejecutivo", s["title"], "Fuente: Sheets braze_auditoria_v4 (Insights, Plan_accion, Estándares); análisis")
            cw = 12.1 / 3
            for j, (h, bs) in enumerate(s["groups"]):
                x = 0.6 + j * cw
                tb(sl, x, 1.95, cw - 0.3, 0.3, h.upper(), 10, True, ACCENT)
                bullets(sl, x, 2.3, cw - 0.3, 3.7, bs, 11.5, INK)
            sowhat_box(sl, s)
        else:
            chrome(sl, i, s.get("tracker", ""), s["title"], s.get("source", ""))
            side = s.get("side") or []
            eh = 3.3 if (s.get("hipotesis") or s.get("causa") or s.get("impacto")) else 4.05
            dy = kpis_box(sl, s)
            eh -= dy
            if side:
                exhibit(sl, s["exhibit"], 0.6, 1.95 + dy, 7.4, eh, i)
                bullets(sl, 8.3, 1.95 + dy, 4.45, eh, side, 10.5 if eh > 3.5 else 9.5, INK2)
            else:
                exhibit(sl, s["exhibit"], 0.6, 1.95 + dy, 12.13, eh, i)
            sowhat_box(sl, s)
    path = os.path.join(OUT, "BRAZE_KUESKI_DECK.pptx")
    prs.save(path)
    return path


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--pptx" not in args:
        print("html:", build_html())
    if "--html" not in args:
        print("pptx:", build_pptx())
