import pandas as pd
c=pd.read_pickle('/tmp/claude-0/-home-user-claude/e114ba4f-39d4-57f8-9f24-b0f0c0cbef51/scratchpad/v6parts/p6work/c_sep.pkl')
L=['pruebas','bloqueados','apagar','limpiar_rehacer','canal_preferido','sin_respuesta_90d']
c['tot']=c[L].sum(axis=1); c['totm']=c[[l+'_msgs' for l in L]].sum(axis=1)
pp=c['prod'].replace({'Kcash':'KCash'})
c['p2']=pp.where(pp.isin(['KCash','KPay']),'Otro')
pd.set_option('display.width',250); pd.set_option('display.max_colwidth',90)
for k in ['equipo','canal','p2','aud']:
  t=c.groupby(k)[L+['tot']].sum()/1e6; print(t.round(3))
print('msgs tot', c.totm.sum()/1e6, 'by lever', {l: round(c[l+'_msgs'].sum()/1e6,2) for l in L})
print((pd.crosstab(c.equipo,c.canal,values=c.tot,aggfunc='sum')/1e6).round(3))
print((pd.crosstab(c.equipo,c.aud,values=c.tot,aggfunc='sum')/1e6).round(3))
print((pd.crosstab(c.p2,c.canal,values=c.tot,aggfunc='sum')/1e6).round(3))
print((pd.crosstab(c.p2,c.aud,values=c.tot,aggfunc='sum')/1e6).round(3))
print((pd.crosstab(c.p2,c.equipo,values=c.tot,aggfunc='sum')/1e6).round(3))
pr=c.tipo=='promocional o lifecycle'
print('sept promo cost', c[pr].c_sep.sum()/1e6, 'by prod', (c[pr].groupby('p2').c_sep.sum()/1e6).round(2).to_dict(), 'all by prod', (c.groupby('p2').c_sep.sum()/1e6).round(2).to_dict())
print('sept cost by canal', (c.groupby('canal').c_sep.sum()/1e6).round(2).to_dict(), 'promo', (c[pr].groupby('canal').c_sep.sum()/1e6).round(2).to_dict())
print('sept by equipo', (c.groupby('equipo').c_sep.sum()/1e6).round(2).to_dict())
a=c[c.apagar>0].sort_values('apagar',ascending=False)[['fam','canal','equipo','aud','env_sep','c_sep','apagar','resp','entrega','conv_ab','lift','meses']]
print(a.head(22).to_string())
b=c[c.limpiar_rehacer>0].sort_values('limpiar_rehacer',ascending=False)[['fam','canal','equipo','env_sep','c_sep','limpiar_rehacer','resp']]; print(b.head(10).to_string())
d=c[c.bloqueados>0].sort_values('bloqueados',ascending=False)[['fam','canal','equipo','sh_bloq','c_sep','bloqueados']]; print(d.head(10).to_string())
e=c[c.pruebas_msgs>0].sort_values('pruebas_msgs',ascending=False)[['fam','canal','equipo','env_sep','pruebas']]; print(e.head(8).to_string())
f=c[c.canal_preferido>0].sort_values('canal_preferido',ascending=False)[['fam','canal','equipo','aud','c_sep','canal_preferido','sin_respuesta_90d']]; print(f.head(10).to_string())
