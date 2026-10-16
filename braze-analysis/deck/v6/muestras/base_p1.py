import pandas as pd, re, numpy as np
D='/home/user/claude/braze-analysis/data/'
AUD = [('cobranza', r'(^Collections|cobranza|BKT)'), ('transaccional', r'(^Transaccional|payment|Contracts|disbursed)'),
       ('frios', r'(Dormant|Inactiv|Churn|Rezagad|Never)'),
       ('leads', r'(Leads|Anonim|Anónim|Registrad)'), ('nuevos', r'(Nuevos|Onboarding|1er|1ra|Welcome)'),
       ('activos', r'(Recurrente|Active|Activo|Cliente)')]
GAN = [('tasa0', r'(Tasa0|Tasa 0)'), ('descuento', r'(Descuento|Cupon|Cupón|Oferta)'), ('referidos', r'(Referral|AnotayGana)'),
       ('recordatorio', r'(Retargeting|Rescate|Recordatorio|Reminder)'), ('lanzamiento', r'(Lanzamiento|Intro|Newsletter|Recommendations)'),
       ('xsell', r'(XSell|Cross)')]
TICKET_RE = r'-[A-Z]?[BTS]0?\d{3,5}-'
def clasif(name, rules):
    for lab, rx in rules:
        if re.search(rx, name, re.I): return lab
    return 'otros'
def team5(t):
    return t if t in ('Marketing','Product Growth','Sales','Collections') else 'Others'
def load():
    d=pd.read_csv(D+'e1_comunicacion_mes_canal.csv', keep_default_na=False, na_values=[''])
    d['communication_name']=d['communication_name'].fillna('(sin nombre)').astype(str)
    num=[c for c in d.columns if c not in ('communication_id','communication_name','team','product_service','ticket_number','grupo','canal','mes')]
    for c in num: d[c]=pd.to_numeric(d[c],errors='coerce').fillna(0)
    d['equipo']=d.team.map(team5)
    d['fam']=d.communication_name.str.replace(r'-\d{8}-','-',regex=True)
    d['tipo']=np.where(d.equipo=='Collections','cobranza',np.where(d.fam.str.startswith('Transaccional')|~d.fam.str.contains(TICKET_RE,regex=True),'transaccional','promocional'))
    d['aud']=d.fam.map(lambda n: clasif(n,AUD))
    d['gan']=d.fam.map(lambda n: clasif(n,GAN))
    d['costo']=d.email_sent*0.05+d.whatsapp_delivery*1.0
    d['m']=d.mes.str[5:7].astype(int)
    return d
RESP={'email':('email_delivery','email_click'),'push notification':('pn_send','pn_open'),'whatsapp':('whatsapp_delivery','whatsapp_read'),'in-app':('in_app_impression','in_app_click')}
def resp(g,c):
    b,r=RESP[c]; return 100*g[r].sum()/g[b].sum() if g[b].sum() else np.nan
def wagg(g):
  return pd.Series({'send':g.whatsapp_send.sum()/1e6,'deliv':g.whatsapp_delivery.sum()/1e6,'nodel':(g.whatsapp_send.sum()-g.whatsapp_delivery.sum())/1e6,'entrega':100*g.whatsapp_delivery.sum()/g.whatsapp_send.sum(),'lect':100*g.whatsapp_read.sum()/max(1,g.whatsapp_delivery.sum()),'costoM':g.costo.sum()/1e6,'conv':g.conversiones_fraccional.sum(),'mxn_conv':g.costo.sum()/max(1,g.conversiones_fraccional.sum()),'meses':g.m.nunique()})
