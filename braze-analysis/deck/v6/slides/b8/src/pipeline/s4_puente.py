import pandas as pd, numpy as np
W='/tmp/claude-0/-home-user-claude/e114ba4f-39d4-57f8-9f24-b0f0c0cbef51/scratchpad/v6parts/p6work/'
c=pd.read_pickle(W+'c_sep.pkl')
mc=pd.read_csv('hallazgos/muestra_c_familias.csv')
mc['ah_ent']=np.where(mc.canal=='whatsapp', mc.ahorro_mxn_mes*mc.entrega_pct/100, mc.ahorro_mxn_mes)
ap=(c.senal=='apagar o rehacer')&(c.accion!='No tocar')&(c.activo==1)
print('Sheets señal apagar activas filas', ap.sum(), 'por accion', c[ap].accion.value_counts().to_dict())
print('promedio mensual (Sheets)', c[ap].ahorro_mes_ent.sum()/1e6, 'por accion', (c[ap].groupby('accion').ahorro_mes_ent.sum()/1e6).round(3).to_dict())
print('mismo set en septiembre', c[ap].c_sep.sum()/1e6, (c[ap].groupby('accion').c_sep.sum()/1e6).round(3).to_dict())
# muestra C vs Sheets por familia
m=mc[mc.ahorro_mxn_mes>0][['familia','canal','team','ah_ent','ahorro_mxn_mes','respuesta_pct']].rename(columns={'familia':'fam'})
j=m.merge(c[['fam','canal','senal','accion','resp','ahorro_mes_ent']],on=['fam','canal'],how='outer')
j['d']=j.ah_ent.fillna(0)-j.ahorro_mes_ent.fillna(0)
print(j.sort_values('d',ascending=False).head(12)[['fam','canal','team','ah_ent','ahorro_mes_ent','respuesta_pct','resp','senal','accion']].to_string())
print('suma diferencias positivas', j.d[j.d>0].sum()/1e6, 'negativas', j.d[j.d<0].sum()/1e6)
# cuantas filas muestra C cambian de señal a otra por lecturas tardías (WA)
print('muestra C activas con ahorro', len(m), 'en Sheets con señal apagar', j[(j.ah_ent>0)&(j.senal=='apagar o rehacer')].shape[0])
# 89 activas en muestra C
x=mc[(mc.senal=='apagar o rehacer')&(mc.tipo=='promocional o lifecycle')&(mc.activo_sep==1)]
print('muestra C promo apagar activas filas', len(x), 'familias', x.familia.nunique(), 'msgs/mes', x.envios_mes_prom.sum()/1e6)
print('Sheets msgs mes ahorro', c.msgs_ahorro.sum()/1e6, 'promo apagar activas', c[ap].shape[0])
