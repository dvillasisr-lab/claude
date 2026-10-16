# Base común: E1 con familia, equipo, tipo, tema, segmento, costo por entregado y respuesta.
import re, pandas as pd, numpy as np
R='/home/user/claude/braze-analysis/'
TEAM_MAP={"Lending":"Product Growth","Product Growth":"Product Growth","Marketing":"Marketing","Sales":"Sales","B2B":"Sales","Collections":"Collections"}
def team_of(t): return TEAM_MAP.get(str(t).strip(),"Others")
MIN={'email':0.3,'push notification':0.75,'whatsapp':60.0,'in-app':10.0}
CH={'email':'Email','push notification':'Push','whatsapp':'WhatsApp','in-app':'In-app','banner':'Banner'}
TEMAS=[
 ("Pruebas y copias", r"^copy of|^qa|qa-|qa_|prueba_|-test$|test\b"),
 ("Cobranza", r"collections|bkt|precobranza|chargeoff|domic"),
 ("Recordatorio de registro", r"leftfunnel|retargeting_veriff|personalinfo|retargeting_nip|accountcreation|requestinfo|faltaveriff|retargeting_address|reminderregistro"),
 ("Tasa 0 y rescate de leads", r"tasa.?0|rescate|narrativa|valueprop|b0171"),
 ("Referidos", r"referral|referid"),
 ("Recuperar inactivos y churn", r"(?<!activoe)churn|inactiv|dormant|lazaro|segundaoportunidad|medium_?active|softnactive|hardinactive|descuentodirecto|tardan45"),
 ("Oferta de crédito e Installments", r"installments|increaseutilization|montopreaprobado|plazoefectivo|transaccionalidad|xsell|neveractive|nevercash|stepoffering|eligibles"),
 ("Promos de comercios KPay", r"comerciodel|cuponera|hotsale|amazon|temu|privalia|palacio|huawei|soriana|viva|cashback|merchant|flashsale|primavera|valentin|kueski30|nuevo30|instore|highstreet|nutrisa|promo|shein|liverpool|walmart|sears|coppel|elektra|fashion|mktplace|comercio"),
 ("Lanzamiento BillPay y recargas", r"billpay|bill_pay|topup|billpayments"),
 ("Temporada y concursos", r"anotaygana|mundial|christmas|reyes|cuestaenero|backtoschool|diapadres|diadelamadre|madres|concurso|ganadores|aniversario|cumple|buenfin|verano|fiestaspatrias|navidad"),
 ("Boletín y contenido", r"newsletter|weekly|educativa|insignia|mejorespracticas|registrolinea|felicit"),
]
def tema_of(name, tipo=None):
    n=str(name).lower()
    if tipo=='transaccional u operativa' and not re.search(r"collections|bkt|precobranza", n): return "Aviso transaccional"
    if 'portafolioactivoeinactivo' in n: return "Promos de comercios KPay"
    for t,p in TEMAS:
        if re.search(p,n): return t
    if tipo=='cobranza': return "Cobranza"
    if re.search(r"noninterest|increaseticket|quincenas|sinintereses", n): return "Oferta de crédito e Installments"
    if 'kpay' in n and re.search(r"^(marketing|sales|leads|lending)", n): return "Promos de comercios KPay"
    return "Otro promocional"
def seg_of(aud, name=''):
    a=(str(aud)+' '+str(name)).lower()
    if re.search(r"bkt|precobranza|chargeoff",a): return "Cartera en cobranza"
    if re.search(r"churn",a): return "Churn (12 meses sin uso)"
    if re.search(r"dormant|inactiv|lazaro|medium_?active|softnactive|hardinactive",a): return "Inactivos y dormants"
    if re.search(r"rezagad|bddmarketing|bbddmarketing|anonimos|bddlending",a): return "Leads fríos (rezagados, anónimos)"
    if re.search(r"leftfunnel|prospect|faltaveriff|requestinfo",a): return "Leads en registro"
    if re.search(r"neveractive|nevercash|registradospay|nuevos",a): return "Registrados sin crédito"
    if re.search(r"hotleads",a): return "Leads recientes"
    if re.search(r"todos|portfolio|ecosistema|blast",a): return "Todos (masivo)"
    if re.search(r"recurr|recurentes|active|activos|cliente|eligible|tardan|aniversario|cumple|xsell",a): return "Clientes activos y recurrentes"
    if re.search(r"lead",a): return "Leads"
    return "Evento o sin segmento"
def colapsa(s): return re.sub(r'-\d{8}-','-',str(s))
def load():
    e1=pd.read_csv(R+'data/e1_comunicacion_mes_canal.csv')
    e1['familia']=e1.communication_name.map(colapsa)
    e1['equipo']=e1.team.map(team_of)
    e1['costo']=0.05*e1.email_sent.fillna(0)+1.0*e1.whatsapp_delivery.fillna(0)
    c=pd.read_csv(R+'hallazgos/muestra_c_familias.csv')
    tip=c.drop_duplicates('familia').set_index('familia')
    e1['tipo']=e1.familia.map(tip.tipo)
    e1['tipo']=e1.tipo.fillna(pd.Series(np.where(e1.equipo.eq('Collections'),'cobranza','promocional o lifecycle'),index=e1.index))
    e1['audiencia']=e1.familia.map(tip.audiencia)
    e1['tema']=[tema_of(n,t) for n,t in zip(e1.familia,e1.tipo)]
    e1['seg']=[seg_of(a,n) if t!='transaccional u operativa' else 'Evento (transaccional)' for a,n,t in zip(e1.audiencia,e1.familia,e1.tipo)]
    base=np.select([e1.canal.eq('email'),e1.canal.eq('push notification'),e1.canal.eq('whatsapp'),e1.canal.eq('in-app')],
                   [e1.email_delivery,e1.pn_send,e1.whatsapp_delivery,e1.in_app_impression],0)
    resp=np.select([e1.canal.eq('email'),e1.canal.eq('push notification'),e1.canal.eq('whatsapp'),e1.canal.eq('in-app')],
                   [e1.email_click,e1.pn_open,e1.whatsapp_read,e1.in_app_click],0)
    e1['base']=base; e1['resp']=resp
    return e1, c
def agg(df, by):
    g=df.groupby(by).agg(env=('envios','sum'),costo=('costo','sum'),base=('base','sum'),resp=('resp','sum'),
        bajas=('email_unsubscribe','sum'),edel=('email_delivery','sum'),conv=('conversiones_filas','sum'),
        wsend=('whatsapp_send','sum'),wdel=('whatsapp_delivery','sum'),usr=('usuarios_aprox','sum')).reset_index()
    g['resp_pct']=100*g.resp/g.base.replace(0,np.nan)
    g['bajas_mil']=1000*g.bajas/g.edel.replace(0,np.nan)
    return g
