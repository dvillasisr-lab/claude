"""Datos comunes del bloque b3 (sección III, equipos). Misma lógica que v6parts/p2work/base.py y muestras/base_p2.py:
E1 por campaña (nombre sin fecha), mes y canal; costo = email 0.05 MXN por enviado + WhatsApp 1.00 MXN por entregado;
respuesta = clic email, apertura push, lectura WhatsApp (incluye lecturas registradas el mes siguiente), clic in-app."""
import sys, pathlib
sys.path.insert(0, '/home/user/claude/braze-analysis/deck/v6/muestras')
from base_p2 import load, agg, MIN, team_of, tema_of, seg_of, colapsa, R  # noqa
import pandas as pd, numpy as np  # noqa
REC = {'Leads en registro', 'Clientes activos y recurrentes', 'Cartera en cobranza', 'Evento (transaccional)', 'Leads recientes'}
EQUIPOS = ['Product Growth', 'Marketing', 'Sales', 'Collections', 'Others']
OUT = pathlib.Path('/home/user/claude/braze-analysis/deck/v6/slides/b3')
_cache = {}
def e1():
    if 'e1' not in _cache:
        d, c = load(); _cache['e1'] = d; _cache['c'] = c
    return _cache['e1']
def fam(minbase=50000):
    """Campaña x canal en los nueve meses (sin banner), con 'con' (acción reciente) y 'pasa' (responde lo mínimo)."""
    x = e1(); x = x[x.canal != 'banner']
    f = agg(x, ['equipo', 'familia', 'canal', 'tema', 'seg'])
    cf = x.groupby(['familia', 'canal']).conversiones_fraccional.sum()
    f['convf'] = [cf.get((a, b), 0) for a, b in zip(f.familia, f.canal)]
    f['vs_min'] = f.resp_pct / f.canal.map(MIN)
    if minbase: f = f[(f.base >= minbase) & f.canal.isin(MIN.keys())].copy()
    f['con'] = f.seg.isin(REC); f['pasa'] = f.vs_min >= 1
    return f
