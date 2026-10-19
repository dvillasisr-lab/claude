"""Revisa largo de texto de una lámina según ESTANDAR.md. Uso: python3 lint.py a.json [b.json ...]"""
import json, sys
LIM = dict(titulo=110, que=90, quien=90, a_quien=90, causa=130, sowhat=110, fuente=220, impacto=120)
bad_words = ["piso", "recorte seguro", "disparador", "masivo", "familia", "quema", "falló", "fallado", "retargeting", "canal caro", "—", "–"]
rc = 0
for p in sys.argv[1:]:
    d = json.load(open(p, encoding="utf-8")); out = []
    for k, n in LIM.items():
        if d.get(k) and len(d[k]) > n: out.append(f"{k}: {len(d[k])} > {n}")
    lec = d.get("lecturas") or []
    if d.get("kind", "grafica") in ("grafica", "html") and lec and len(lec) != 3: out.append(f"lecturas: {len(lec)} (deben ser 3)")
    for i, x in enumerate(lec):
        if len(x) > 120: out.append(f"lectura {i+1}: {len(x)} > 120")
    for x in d.get("porques", []):
        if len(x) > 90: out.append(f"porqué: {len(x)} > 90")
    for k, x in (d.get("hipotesis") or {}).items():
        if len(x) > 100: out.append(f"hipótesis {k}: {len(x)} > 100")
    for x in d.get("como", []):
        if len(x) > 100: out.append(f"cómo: {len(x)} > 100")
    txt = json.dumps({k: v for k, v in d.items() if k not in ("svg", "html")}, ensure_ascii=False).lower()
    for w in bad_words:
        if w in txt: out.append(f"palabra a evitar: {w}")
    print(p, "OK" if not out else "\n  " + "\n  ".join(out)); rc |= bool(out)
sys.exit(rc)
