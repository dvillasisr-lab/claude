"""Lámina 7: ya aprobada por el usuario. Copia muestras/s1.json con "n": 7 y "kind": "grafica" (no se rehace)."""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent
src = H.parents[2] / 'muestras' / 's1.json'
d = json.loads(src.read_text(encoding='utf-8'))
o = {'n': 7, 'kind': 'grafica', **{k: v for k, v in d.items() if k not in ('n', 'kind')}}
(H.parent / '007.json').write_text(json.dumps(o, ensure_ascii=False, indent=1), encoding='utf-8')
print('escrito 007.json')
