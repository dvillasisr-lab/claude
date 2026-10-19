"""Bloque 5 (láminas 47 a 55, sección VI). Calcula todas las cifras desde data/*.csv y hallazgos/*.csv y las guarda en b5_datos.json.
Costo: email 0.05 MXN por enviado, WhatsApp 1.00 MXN por entregado, push e in-app 0.
Grupos de audiencia por el nombre de la campaña (misma regla que p4work/p4_calc.py: separa ex clientes de leads que nunca activaron).
Uso: python3 b5_datos.py"""
import json, pathlib, re, sys
import numpy as np, pandas as pd

H = pathlib.Path(__file__).resolve().parent
R = pathlib.Path('/home/user/claude/braze-analysis/')
D, HA = R / 'data', R / 'hallazgos'
sys.path.insert(0, str(R / 'scripts'))
from deck_data import gancho_of  # tema por el nombre de la campaña


def grupo(n):
    s = str(n).lower()
    if s.startswith('collections') or 'cobranza' in s or 'bkt' in s: return 'cobranza'
    if s.startswith('transaccional') or 'payment' in s or 'contracts' in s or 'disbursed' in s: return 'transaccional'
    if 'mpnevercash' in s or 'portafolioactivoeinactivo' in s: return 'activos'
    if re.search(r'dormant|inactiv|churn|lazaro|softnactive', s): return 'ex'
    if re.search(r'rezagad|never|anonim|hotlead', s): return 'nunca'
    if re.search(r'leads|registrad|prospect|leftfunnel', s): return 'leads'
    if re.search(r'nuevos|onboarding|1er|1ra|welcome', s): return 'nuevos'
    if re.search(r'recurrente|active|activo|cliente', s): return 'activos'
    return 'todos'


GN = {'activos': 'Activos y recurrentes', 'leads': 'Leads y registrados recientes', 'nunca': 'Leads que nunca activaron',
      'ex': 'Ex clientes inactivos', 'nuevos': 'Nuevos y onboarding', 'cobranza': 'Cobranza', 'transaccional': 'Transaccional', 'todos': 'Todos y otros'}
RESP = {'email': ('email_delivery', 'email_click'), 'push notification': ('pn_send', 'pn_open'),
        'whatsapp': ('whatsapp_delivery', 'whatsapp_read'), 'in-app': ('in_app_impression', 'in_app_click')}
TEAM = {'Lending': 'Product Growth', 'Product Growth': 'Product Growth', 'Marketing': 'Marketing', 'Sales': 'Sales', 'Collections': 'Collections', 'Acquisition': 'Acquisition'}
fam = lambda s: re.sub(r'-\d{8,9}-', '-', str(s))
OUT = {}

# ---------- E1 ----------
e1 = pd.read_csv(D / 'e1_comunicacion_mes_canal.csv')
e1['communication_name'] = e1.communication_name.fillna('(sin nombre)')
e1['familia'] = e1.communication_name.map(fam)
e1['costo'] = e1.email_sent.fillna(0) * 0.05 + e1.whatsapp_delivery.fillna(0) * 1.0
e1['g'] = e1.communication_name.map(grupo)
e1['equipo'] = e1.team.map(lambda t: TEAM.get(t, 'Others'))
x = e1[e1.canal != 'banner']
TOTC = e1.conversiones_fraccional.sum()

# Por grupo: mensajes, costo, conversiones del mismo día
tg = e1.groupby('g').agg(env=('envios', 'sum'), costo=('costo', 'sum'), conv=('conversiones_fraccional', 'sum'), wa=('whatsapp_delivery', 'sum'))
for c in ('env', 'costo', 'conv', 'wa'):
    tg['p_' + c] = 100 * tg[c] / tg[c].sum()
tg['mxn_conv'] = tg.costo / tg.conv
OUT['grupos'] = {k: {c: float(v) for c, v in r.items()} for k, r in tg.iterrows()}
OUT['tot'] = dict(env=float(e1.envios.sum()), costo=float(e1.costo.sum()), conv=float(TOTC), wa=float(e1.whatsapp_delivery.sum()))

# Grupo x canal: respuesta, costo, MXN por conversión, conversiones por mil
gc = {}
for (g, c), d in x.groupby(['g', 'canal']):
    b, r = RESP[c]
    gc[f'{g}|{c}'] = dict(env=float(d.envios.sum()), costo=float(d.costo.sum()), conv=float(d.conversiones_fraccional.sum()),
                          base=float(d[b].sum()), resp=float(100 * d[r].sum() / max(d[b].sum(), 1)),
                          mxn_conv=float(d.costo.sum() / max(d.conversiones_fraccional.sum(), 1e-9)),
                          sol=float(d.solicitudes_filas.sum()), mxn_sol=float(d.costo.sum() / max(d.solicitudes_filas.sum(), 1e-9)),
                          conv_mil=float(1000 * d.conversiones_fraccional.sum() / max(d.envios.sum(), 1)),
                          entrega=float(100 * d.whatsapp_delivery.sum() / max(d.whatsapp_send.sum(), 1)) if c == 'whatsapp' else None,
                          wsend=float(d.whatsapp_send.sum()))
OUT['gc'] = gc
# equipos en los dos grupos fríos
ge = e1[e1.g.isin(['ex', 'nunca'])].groupby(['g', 'equipo']).agg(env=('envios', 'sum'), costo=('costo', 'sum'))
OUT['frio_equipo'] = {f'{g}|{t}': dict(env=float(r.env), costo=float(r.costo)) for (g, t), r in ge.iterrows()}

# ---------- Programas de recuperación (lámina 49) ----------
PROG = [('30a90', '30 a 90 días sin usar', r'-B0208-', 'ex'), ('3m', '3 meses', r'-B0331-', 'ex'),
        ('6m', '6 meses', r'-B0332-|-B0206-|202600903', 'ex'), ('12m', '12 meses (churn)', r'-B0333-|-B0207-', 'ex'),
        ('inact', 'Inactivos sin plazo', r'-B0209-', 'ex'), ('dorm', 'Dormants, referidos', r'-B0326-', 'ex'),
        ('b0171', 'Leads: rescate Tasa 0', r'-B0171-', 'nunca'), ('b0223', 'Nunca activaron: Installments', r'-B0223-', 'nunca')]
m = pd.read_csv(HA / 'muestra_m_ventanas.csv')
prog = {}
for k, lab, rx, g in PROG:
    d = x[x.familia.str.contains(rx) & (x.g == g)]
    mm = m[m.familia.str.contains(rx) & m.canal.isin(['email', 'push notification', 'whatsapp']) & m.familia.map(grupo).eq(g)]
    eq = d.groupby('equipo').envios.sum().sort_values(ascending=False)
    prog[k] = dict(lab=lab, env=float(d.envios.sum()), costo=float(d.costo.sum()), conv=float(d.conversiones_fraccional.sum()),
                   mxn_conv=float(d.costo.sum() / d.conversiones_fraccional.sum()), equipo=eq.index[0],
                   ca7=float(100 * mm.ab_conv_7.sum() / mm.abrieron.sum()), cn7=float(100 * mm.no_conv_7.sum() / mm.no_abrieron.sum()),
                   ca90=float(100 * mm.ab_conv_90.sum() / mm.abrieron.sum()), cn90=float(100 * mm.no_conv_90.sum() / mm.no_abrieron.sum()),
                   familias=sorted(d.familia.unique().tolist())[:12])
# B0333 solo
d = x[x.familia.str.contains('-B0333-')]
prog['12m']['b0333_mxn'] = float(d.costo.sum() / d.conversiones_fraccional.sum())
prog['12m']['b0333_env'] = float(d.envios.sum()); prog['12m']['b0333_costo'] = float(d.costo.sum()); prog['12m']['b0333_conv'] = float(d.conversiones_fraccional.sum())
d = x[x.familia.str.contains('-B0208-')]
prog['30a90']['b0208'] = dict(env=float(d.envios.sum()), costo=float(d.costo.sum()), conv=float(d.conversiones_fraccional.sum()))
OUT['prog'] = prog
# quien abre contra quien no, por familia y canal clave
def abre(rx, canal):
    q = m[m.familia.str.contains(rx) & (m.canal == canal)]
    return dict(ca90=float(100 * q.ab_conv_90.sum() / q.abrieron.sum()), cn90=float(100 * q.no_conv_90.sum() / q.no_abrieron.sum()))
OUT['abre'] = {'b0209_email': abre(r'KCash-B0209-CANVAS-Recurrentes_Inactivos-DescuentoDirecto', 'email'),
               'b0326kcash_email': abre(r'Marketing-KCash-B0326-Canvas-Recurrentes_Dormants', 'email')}
# ex clientes, todos los programas, email: quien no abre
mx = m[m.familia.map(grupo).eq('ex')]
OUT['ex_email_noabre'] = {c: dict(ca90=float(100 * q.ab_conv_90.sum() / q.abrieron.sum()), cn90=float(100 * q.no_conv_90.sum() / q.no_abrieron.sum()),
                                   ca7=float(100 * q.ab_conv_7.sum() / q.abrieron.sum()), cn7=float(100 * q.no_conv_7.sum() / q.no_abrieron.sum()))
                          for c, q in mx[mx.canal.isin(['email', 'push notification', 'whatsapp'])].groupby('canal')}
# WhatsApp por programa (lámina 50)
OUT['wa_prog'] = {}
for k, rx in [('b0171', '-B0171-'), ('b0333', '-B0333-'), ('b0209', '-B0209-')]:
    xf = x[x.g.isin(['ex', 'nunca'])]
    d = xf[xf.familia.str.contains(rx) & (xf.canal == 'whatsapp')]; de = xf[xf.familia.str.contains(rx) & (xf.canal == 'email')]
    OUT['wa_prog'][k] = dict(send=float(d.whatsapp_send.sum()), costo=float(d.costo.sum()), mxn=float(d.costo.sum() / d.conversiones_fraccional.sum()),
                             email_mxn=float(de.costo.sum() / de.conversiones_fraccional.sum()))

# Grupos de control (E13)
e13 = pd.read_csv(D / 'e13_lift_control.csv')
e13['g'] = e13.canvas_name.fillna('').map(grupo)
rc = e13[e13.g.isin(['ex', 'nunca'])]
ctl = rc[rc.grupo == 'control']
OUT['control'] = dict(canvas=int(rc.canvas_id.nunique()), con_control=int(ctl.canvas_id.nunique()), personas=int(ctl.usuarios.sum()),
                      min=int(ctl.usuarios.min()), max=int(ctl.usuarios.max()), ex_con_control=int(ctl[ctl.g == 'ex'].canvas_id.nunique()),
                      todos_b0171=bool(ctl.canvas_name.str.contains('B0171').all()))

# ---------- E7b / E9b: patrón de respuesta por persona ----------
def patron(fn):
    p = pd.read_csv(D / fn)
    p['msgs'] = p.msgs_email + p.msgs_push + p.msgs_wa + p.msgs_inapp
    no = p[(p.resp_email + p.resp_push + p.resp_wa + p.resp_inapp) == 0].sum()
    si = p[(p.resp_email + p.resp_push + p.resp_wa + p.resp_inapp) > 0].sum()
    tot = p.sum()
    f = lambda s: dict(usuarios=float(s.usuarios), msgs=float(s.msgs), email=float(s.msgs_email), push=float(s.msgs_push), wa=float(s.msgs_wa),
                       wa_ent=float(s.msgs_wa_entregados), inapp=float(s.msgs_inapp), conv=float(s.usuarios_con_conversion), bajas=float(s.usuarios_con_baja_email),
                       costo=float(0.05 * s.msgs_email + s.msgs_wa_entregados))
    abre_push = p[p.resp_push == 1].usuarios.sum()
    push_o_inapp = p[(p.resp_push == 1) | (p.resp_inapp == 1)]
    return dict(no=f(no), si=f(si), tot=f(tot), abre_push=float(abre_push), push_o_inapp=float(push_o_inapp.usuarios.sum()),
                push_o_inapp_conv=float(push_o_inapp.usuarios_con_conversion.sum()))
OUT['e7b'] = patron('e7b_patron_respuesta.csv')
OUT['e9b'] = patron('e9b_patron_respuesta_90d.csv')

# ---------- E4a: personas por canal al mes ----------
e4 = pd.read_csv(D / 'e4a_serie_semana_mes_canal.csv')
e4 = e4[(e4.grano == 'mes')]
OUT['e4a'] = {c: {p[5:7]: float(u) for p, u in zip(d.periodo, d.usuarios_aprox)} for c, d in e4.groupby('canal') if c != 'banner'}

# ---------- E1: alcance de push e in-app por cada 100 que reciben el email ----------
pv = x.pivot_table(index=['g', 'familia', 'mes'], columns='canal', values='usuarios_aprox', aggfunc='sum').fillna(0)
pv = pv.join(x[x.canal == 'push notification'].groupby(['g', 'familia', 'mes']).pn_open.sum()).fillna(0)
both = pv[(pv['email'] > 1000) & (pv['push notification'] > 0)]
ga = both.groupby('g')[['email', 'push notification', 'in-app', 'pn_open']].sum()
OUT['alcance'] = {g: dict(push=float(100 * r['push notification'] / r.email), inapp=float(100 * r['in-app'] / r.email), abre=float(100 * r.pn_open / r.email))
                  for g, r in ga.iterrows()}
a3 = pv[(pv['email'] > 1000) & (pv['push notification'] > 0) & (pv['in-app'] > 0)].groupby('g')[['email', 'push notification', 'in-app', 'pn_open']].sum()
OUT['alcance3'] = {g: dict(push=float(100 * r['push notification'] / r.email), inapp=float(100 * r['in-app'] / r.email), abre=float(100 * r.pn_open / r.email))
                   for g, r in a3.iterrows()}
def alc_fam(rx):
    q = both[both.index.get_level_values('familia').str.contains(rx)].sum()
    return dict(push=float(100 * q['push notification'] / q.email), inapp=float(100 * q['in-app'] / q.email))
OUT['alc_fam'] = {'b0209': alc_fam('B0209-CANVAS-Recurrentes_Inactivos-DescuentoDirecto'), 'b0223': alc_fam('B0223-CANVAS-Nuevos_NeverActive')}
d = x[x.familia.str.contains('Marketing-KCash-B0171-CANVAS-Anonimos-RescateTasa0') & (x.canal == 'push notification')]
OUT['b0171_anon_push'] = dict(env=float(d.pn_send.sum()), usr=float(d.usuarios_aprox.sum()), ap=float(100 * d.pn_open.sum() / d.pn_send.sum()))

# ---------- E7a: bloqueados (lámina 51) ----------
c = pd.read_csv(HA / 'muestra_c_familias.csv')
tipo = c.groupby('familia').tipo.first()
a = pd.read_csv(D / 'e7a_familia_canal_etapa.csv')
a['familia'] = a.familia.fillna('(sin nombre)').map(fam)
a['tipo'] = a.familia.map(tipo).fillna('?')
def eq7(f):
    t = re.sub(r'^Copy of ', '', f).split('-')[0]
    return {'Lending': 'Product Growth', 'Marketing': 'Marketing', 'Maketing': 'Marketing', 'Sales': 'Sales'}.get(t, 'Others')
a['eq'] = a.familia.map(eq7)
a['tema'] = a.familia.map(gancho_of)
a['prod'] = a.familia.map(lambda f: re.sub(r'^Copy of ', '', f).split('-')[1].lower() if len(f.split('-')) > 1 else '')
bl = {}
for et, k in [('4.Kpay CC Freeze', 'freeze'), ('6.Reus or Arco', 'reus'), ('3.Blacklist', 'negra')]:
    p = a[(a.etapa == et) & (a.tipo == 'promocional o lifecycle')]
    bl[k] = dict(total=float(a[a.etapa == et].envios.sum()), promo=float(p.envios.sum()),
                 eq={t: float(v) for t, v in p.groupby('eq').envios.sum().items()},
                 tema={t: float(v) for t, v in p.groupby('tema').envios.sum().items()},
                 canal={t: float(v) for t, v in p.groupby('canal').envios.sum().items()},
                 prod={t: float(v) for t, v in p.groupby('prod').envios.sum().items()},
                 eq_tema={f'{e}|{t}': float(v) for (e, t), v in p.groupby(['eq', 'tema']).envios.sum().items()},
                 eq_prod={f'{e}|{t}': float(v) for (e, t), v in p.groupby(['eq', 'prod']).envios.sum().items()},
                 top=[[f, ch, e, float(v)] for (f, ch, e), v in p.groupby(['familia', 'canal', 'eq']).envios.sum().sort_values(ascending=False).head(15).items()])
OUT['bloq'] = bl
OUT['excl_min'] = bl['freeze']['prod'].get('kpay', 0) + bl['reus']['promo'] + bl['negra']['promo']
OUT['excl_kcash'] = OUT['excl_min'] + bl['freeze']['prod'].get('kcash', 0)
e3 = pd.read_csv(D / 'e3_usuarios_distribucion.csv')
s3 = e3.groupby('etapa').agg(u=('usuarios', 'sum'), m=('msgs', 'sum'), c=('usuarios_con_conversion', 'sum'))
OUT['e3'] = {k: dict(u=float(r.u), m=float(r.m), c=float(r.c)) for k, r in s3.iterrows()}

# ---------- E5b: después de la baja (lámina 52) ----------
b = pd.read_csv(D / 'e5b_comms_despues_baja.csv')
b['familia'] = b.familia.map(fam); b['tipo'] = b.familia.map(tipo).fillna('?'); b['tema'] = b.familia.map(gancho_of)
pb = b[b.tipo == 'promocional o lifecycle']
OUT['baja'] = dict(total=float(b.emails_despues_de_baja.sum()), promo=float(pb.emails_despues_de_baja.sum()),
                   tipo={t: float(v) for t, v in b.groupby('tipo').emails_despues_de_baja.sum().items()},
                   tema={t: float(v) for t, v in pb.groupby('tema').emails_despues_de_baja.sum().items()},
                   equipo={t: float(v) for t, v in pb.groupby('equipo').emails_despues_de_baja.sum().items()},
                   usuarios=float(pb.usuarios_aprox.sum()), abiertos=float(pb.abiertos.sum()), clics=float(pb.clics.sum()),
                   top=[dict(familia=r.familia, equipo=r.equipo, e=float(r.emails_despues_de_baja), meses=int(r.meses), tema=r.tema, usr=float(r.usuarios_aprox))
                        for r in pb.sort_values('emails_despues_de_baja', ascending=False).head(14).itertuples()])

json.dump(OUT, open(H / 'b5_datos.json', 'w'), ensure_ascii=False, indent=1)
print('ok', H / 'b5_datos.json')
