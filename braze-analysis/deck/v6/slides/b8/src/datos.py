# Datos comunes del bloque b8. Reutiliza la reconciliación de ahorro (septiembre, WhatsApp por entregado)
# hecha en pipeline/ (copias de v6parts/p6work y muestras/s3_datos.py). Si faltan los pickles, los regenera.
import os, subprocess, sys, json, re
import pandas as pd, numpy as np
ROOT = '/home/user/claude/braze-analysis/'
W = '/tmp/claude-0/-home-user-claude/e114ba4f-39d4-57f8-9f24-b0f0c0cbef51/scratchpad/v6parts/p6work/'
S3J = '/home/user/claude/braze-analysis/deck/v6/muestras/s3_datos.json'
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pipeline')

def _run(s):
    subprocess.run([sys.executable, os.path.join(P, s)], check=True, cwd=ROOT, stdout=subprocess.DEVNULL)

def load_c():
    os.makedirs(W, exist_ok=True)
    if not os.path.exists(W + 'camp.pkl'): _run('s1_camp.py')
    if not os.path.exists(W + 'c_sep.pkl'): _run('s2_ahorro.py')
    if not os.path.exists(W + 'c_sep2.pkl'): _run('s5_extra.py')
    c = pd.read_pickle(W + 'c_sep2.pkl')
    c['rec'] = c.aud.str.startswith('recup')
    pp = c['prod'].replace({'Kcash': 'KCash'})
    c['p2'] = pp.where(pp.isin(['KCash', 'KPay']), 'Otro')
    c['b_desp'] = c.pruebas + c.bloqueados
    c['b_cortar'] = c.apagar * (~c.rec) + c.limpiar_rehacer
    c['b_pref'] = c.canal_preferido
    c['b_medir'] = c.apagar * c.rec + c.sin_respuesta_90d
    c['bm_desp'] = c.pruebas_msgs + c.bloqueados_msgs
    c['bm_cortar'] = c.apagar_msgs * (~c.rec) + c.limpiar_rehacer_msgs
    c['bm_pref'] = c.canal_preferido_msgs
    c['bm_medir'] = c.apagar_msgs * c.rec + c.sin_respuesta_90d_msgs
    return c

def load_g1():
    if not os.path.exists(W + 'g1.pkl'): _run('s1_camp.py')
    return pd.read_pickle(W + 'g1.pkl')

def load_s3():
    if not os.path.exists(S3J): load_c(); _run('s3_datos.py')
    return json.load(open(S3J))

def dup_mes():
    "Duplicados del mismo día (E6b), MXN al mes, igual que s3_datos."
    return load_s3()['T'][1]['mxn']

def e1():
    d = pd.read_csv(ROOT + 'data/e1_comunicacion_mes_canal.csv')
    d['communication_name'] = d.communication_name.astype(str)
    d['costo'] = d.email_sent * 0.05 + d.whatsapp_delivery * 1.0
    return d

# Nombres limpios de campaña (regla 5 del usuario)
NOMBRES = {
 'B0211': 'Tasa 0 a registrados de KPay sin Cash', 'B0223': 'Installments a registrados que nunca activaron',
 'B0333': 'Oferta a clientes KPay sin compra en un año', 'B0332': 'Oferta a clientes KPay sin compra en 6 meses',
 'B0326': 'Referidos', 'B0000': 'Recordatorio de terminar la verificación', 'B0171': 'Rescate Tasa 0 a leads',
 'B0603': 'Cuponera', 'B0598': 'Privalia', 'B0541': 'Amazon', 'B0335': 'Promociones de comercios',
 'B0619': 'Cross sell KPay a Cash', 'B0620': 'Cross sell KPay a Cash',
}
def ticket(f):
    m_ = re.search(r'-([A-Z]?[BTS]0?\d{3,5})-', f); return m_.group(1) if m_ else ''
