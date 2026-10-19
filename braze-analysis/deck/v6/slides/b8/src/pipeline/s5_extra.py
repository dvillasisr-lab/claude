import pandas as pd, numpy as np
pd.set_option('display.width',250); pd.set_option('display.max_colwidth',85)
W='/tmp/claude-0/-home-user-claude/e114ba4f-39d4-57f8-9f24-b0f0c0cbef51/scratchpad/v6parts/p6work/'
c=pd.read_pickle(W+'c_sep.pkl'); g1=pd.read_pickle(W+'g1.pkl')
L=['pruebas','bloqueados','apagar','limpiar_rehacer','canal_preferido','sin_respuesta_90d']
c['tot']=c[L].sum(axis=1)
# por accion: filas, activas, msgs sept, costo sept
a=c.groupby('accion').agg(filas=('fam','size'),activas=('activo','sum'),env_sep=('env_sep','sum'),c_sep=('c_sep','sum'),ahorro_prop=('tot','sum'),env_per=('env','sum'))
print((a.assign(env_sep=a.env_sep/1e6,c_sep=a.c_sep/1e6,ahorro_prop=a.ahorro_prop/1e6,env_per=a.env_per/1e6)).round(2))
# bajas de email
e=pd.read_csv('data/e4a_serie_semana_mes_canal.csv'); m=e[(e.grano=='mes')&(e.canal=='email')]
print(m[['periodo','bajas_email_eventos','bajas_email_usuarios','email_sent']].to_string())
s=g1[g1.mes=='2026-09'].groupby(['fam','canal']).eu.sum().rename('eu_sep').reset_index()
c=c.merge(s,on=['fam','canal'],how='left').fillna({'eu_sep':0})
print('bajas eventos sept total', c.eu_sep.sum())
print(c[c.canal=='email'].groupby('accion').eu_sep.sum())
print('bajas sep en promo', c[(c.canal=='email')&(c.tipo=='promocional o lifecycle')].eu_sep.sum())
# top familias por equipo en el ahorro
for eq in ['Product Growth','Marketing','Sales','Others']:
    t=c[c.equipo==eq].groupby(['fam','canal','aud'])[L+['tot']].sum().sort_values('tot',ascending=False).head(7)
    print('\n##',eq); print((t/1e3).round(0).to_string())
# recuperacion: que familias
r=c[c.aud.str.startswith('recup')].groupby(['fam','canal'])[L+['tot']].sum().sort_values('tot',ascending=False).head(10); print((r/1e3).round(0).to_string())
c.to_pickle(W+'c_sep2.pkl')
