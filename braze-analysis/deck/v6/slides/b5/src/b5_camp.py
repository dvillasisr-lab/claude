"""Ronda 2 del bloque 5: tablas por campaña (la unidad de las gráficas). Escribe b5_camp.csv (campaña x canal, E1 + E9a)
y b5_camp_todo.csv (campaña con todos sus canales). Uso: python3 b5_camp.py"""
import pathlib, re
import numpy as np, pandas as pd
from b5_datos import grupo, RESP, TEAM, fam  # misma regla de grupos y costo que la ronda 1 (importar corre b5_datos y refresca b5_datos.json)

H = pathlib.Path(__file__).resolve().parent
R = pathlib.Path('/home/user/claude/braze-analysis/')
e1 = pd.read_csv(R / 'data/e1_comunicacion_mes_canal.csv')
e1['communication_name'] = e1.communication_name.fillna('(sin nombre)')
e1['familia'] = e1.communication_name.map(fam)
e1['costo'] = e1.email_sent.fillna(0) * 0.05 + e1.whatsapp_delivery.fillna(0) * 1.0
e1 = e1[e1.canal != 'banner']
rows = []
for (f, c), d in e1.groupby(['familia', 'canal']):
    b, r = RESP[c]
    rows.append(dict(familia=f, canal=c, g=grupo(f), equipo=TEAM.get(str(d.team.iloc[0]), 'Others'), env=d.envios.sum(), costo=d.costo.sum(),
                     conv=d.conversiones_fraccional.sum(), base=d[b].sum(), r=d[r].sum(), wsend=d.whatsapp_send.sum(), meses=d.mes.nunique(),
                     usr=d.usuarios_aprox.sum()))
t = pd.DataFrame(rows)
t['resp'] = 100 * t.r / t.base.replace(0, np.nan)
t['mxn_conv'] = t.costo / t.conv.replace(0, np.nan)
t['conv_mil'] = 1000 * t.conv / t.env.replace(0, np.nan)
m = pd.read_csv(R / 'hallazgos/muestra_m_ventanas.csv')
t = t.merge(m[['familia', 'canal', 'abrieron', 'no_abrieron', 'ab_conv_90', 'no_conv_90', 'ca_90', 'cn_90', 'muestra']], on=['familia', 'canal'], how='left')
t.to_csv(H / 'b5_camp.csv', index=False)
a = t.groupby('familia').agg(g=('g', 'first'), equipo=('equipo', 'first'), env=('env', 'sum'), costo=('costo', 'sum'), conv=('conv', 'sum')).reset_index()
a['conv_mil'] = 1000 * a.conv / a.env
a['mxn_conv'] = a.costo / a.conv.replace(0, np.nan)
a.to_csv(H / 'b5_camp_todo.csv', index=False)
print(len(t), len(a))
