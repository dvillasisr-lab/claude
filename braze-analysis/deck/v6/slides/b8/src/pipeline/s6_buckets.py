import pandas as pd, numpy as np
pd.set_option('display.width',250)
W='/tmp/claude-0/-home-user-claude/e114ba4f-39d4-57f8-9f24-b0f0c0cbef51/scratchpad/v6parts/p6work/'
c=pd.read_pickle(W+'c_sep2.pkl')
rec=c.aud.str.startswith('recup')
B={}
B['1 desperdicio claro']=c.pruebas+c.bloqueados
B['2 cortar en 30 dias (leads, registrados, cross sell)']=c.apagar*(~rec)+c.limpiar_rehacer
B['3 canal preferido']=c.canal_preferido
B['4 recuperacion a medir']=c.apagar*rec+c.sin_respuesta_90d
Bm={}
Bm['1']=c.pruebas_msgs+c.bloqueados_msgs; Bm['2']=c.apagar_msgs*(~rec)+c.limpiar_rehacer_msgs; Bm['3']=c.canal_preferido_msgs; Bm['4']=c.apagar_msgs*rec+c.sin_respuesta_90d_msgs
DUP=0.0233e6
for (k,v),(k2,m) in zip(B.items(),Bm.items()): print(f'{k:55s} {v.sum()/1e6:6.3f} M MXN  {m.sum()/1e6:6.2f} M msgs')
tot=sum(v.sum() for v in B.values())+DUP; print('total con duplicados', tot/1e6)
seg=B['1 desperdicio claro'].sum()+DUP+B['2 cortar en 30 dias (leads, registrados, cross sell)'].sum()+B['3 canal preferido'].sum(); print('seguro', seg/1e6, 'a medir', B['4 recuperacion a medir'].sum()/1e6)
SEP=4233202; AVG=57662758/9
for nm,v in [('total',tot),('seguro',seg),('medir',B['4 recuperacion a medir'].sum())]:
    print(nm, 'mes', round(v/1e6,2),'año', round(v*12/1e6,1), '%sep', round(v/SEP*100,1), '%prom', round(v/AVG*100,1))
print('año gasto sep run-rate', SEP*12/1e6, 'prom', AVG*12/1e6)
for k,v in B.items():
    c[k]=v
K=list(B.keys())
print((c.groupby('equipo')[K].sum()/1e6).round(3))
print((c.groupby('canal')[K].sum()/1e6).round(3))
print((c.groupby('p2' if 'p2' in c else c['prod'].replace({'Kcash':'KCash'}).where(c['prod'].replace({'Kcash':'KCash'}).isin(['KCash','KPay']),'Otro'))[K].sum()/1e6).round(3))
print('levers', {l: round(c[l].sum()/1e6,3) for l in ['pruebas','bloqueados','apagar','limpiar_rehacer','canal_preferido','sin_respuesta_90d']})
lw=c[c.canal=='whatsapp'].limpiar_rehacer.sum(); le=c[c.canal=='email'].limpiar_rehacer.sum(); print('limpiar WA', lw/1e6, 'rehacer email', le/1e6)
print('apagar rec', (c.apagar*rec).sum()/1e6, 'apagar no rec', (c.apagar*~rec).sum()/1e6)
print('msgs total', sum(m.sum() for m in Bm.values())/1e6, 'sept msgs', c.env_sep.sum()/1e6)
