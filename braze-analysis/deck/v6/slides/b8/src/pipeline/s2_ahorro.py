# Reconciliación del ahorro: septiembre como mes base, WhatsApp por entregado, palancas sin doble conteo.
# Uso: cd braze-analysis && python3 <este script>
import re, pandas as pd, numpy as np
W = '/tmp/claude-0/-home-user-claude/e114ba4f-39d4-57f8-9f24-b0f0c0cbef51/scratchpad/v6parts/p6work/'
camp = pd.read_pickle(W + 'camp.pkl'); g1 = pd.read_pickle(W + 'g1.pkl')
M = lambda v: f'{v/1e6:.2f} M'

# ---------- 1. Las dos cifras viejas
print('== Cifras previas')
print('Sheets/deck (WA entregado, promedio de meses con envío):', M(camp.ahorro_mes_ent.sum()), ' por enviado:', M(camp.ahorro_mes_env.sum()))
mc = pd.read_csv('hallazgos/muestra_c_familias.csv')
print('Muestra C (WA enviado, prom meses, sin lecturas tardías):', M(mc.ahorro_mxn_mes.sum()), 'filas activas con ahorro', (mc.ahorro_mxn_mes > 0).sum())
print(mc[mc.ahorro_mxn_mes > 0].groupby('team').ahorro_mxn_mes.sum().round(-3))
# muestra C con WA por entregado (entrega_pct de la propia muestra)
mc['ah_ent'] = np.where(mc.canal == 'whatsapp', mc.ahorro_mxn_mes * mc.entrega_pct / 100, mc.ahorro_mxn_mes)
print('Muestra C pasada a entregado:', M(mc.ah_ent.sum()))
print('Sheets camp por equipo:', (camp.groupby('equipo').ahorro_mes_ent.sum() / 1e6).round(2).to_dict())

# ---------- 2. Septiembre por familia x canal (todas las filas de septiembre, incluidas entregas tardías)
s = g1[g1.mes == '2026-09'].groupby(['fam', 'canal'])[['env', 'es', 'ws', 'wd', 'ps', 'ii']].sum().reset_index()
s['c_sep'] = s.es * 0.05 + s.wd * 1.0
c = camp.merge(s[['fam', 'canal', 'env', 'c_sep', 'wd', 'es']].rename(columns={'env': 'env_sep', 'wd': 'wd_sep', 'es': 'es_sep'}), on=['fam', 'canal'], how='left').fillna({'env_sep': 0, 'c_sep': 0, 'wd_sep': 0, 'es_sep': 0})
print('\n== Septiembre: costo total en camp', M(c.c_sep.sum()), 'envíos', M(c.env_sep.sum()))

# audiencia por nombre
def aud(f):
    if re.search(r'Churn|Dormant|Inactiv|Medium_active|Winback|Reactiv', f, re.I): return 'recuperación (ex clientes: churn, dormants, inactivos)'
    if re.search(r'Lead|Anonim|Anónim|Registrad|NeverActive|NeverCash|Never|Rezagad|LeftFunnel|Nuevos|Prospect', f, re.I): return 'activación (leads y registrados sin crédito)'
    if re.search(r'Recurrente|Active|Activo|Cliente|Eligible', f, re.I): return 'clientes activos'
    return 'otros o sin audiencia en el nombre'
c['aud'] = c.fam.map(aud)
c['prod'] = c.fam.str.extract(r'^[^-]+-([^-]+)-')[0].replace({'Kpay': 'KPay', 'KCASH': 'KCash'})
promo = c.tipo == 'promocional o lifecycle'
TEST = re.compile(r'prueba|test|\bqa\b|copy of|copia|dummy|demo', re.I)
c['es_prueba'] = c.fam.map(lambda f: bool(TEST.search(f)))

# ---------- 3. Palancas en orden, sin doble conteo (cada palanca toma solo lo que dejó la anterior)
c['rest'] = np.where(promo | c.es_prueba, c.c_sep, 0.0)   # solo promocional (y pruebas de cualquier tipo)
c['rest_msgs'] = np.where(promo | c.es_prueba, c.env_sep, 0.0)
out = {}
def take(name, mask, frac, msgs=True):
    v = c.rest * frac * mask
    mm = c.rest_msgs * frac * mask
    c[name] = v; c[name + '_msgs'] = mm
    c['rest'] = c.rest - v; c['rest_msgs'] = c.rest_msgs - mm
    out[name] = (v.sum(), mm.sum())

# 3a. Pruebas y copias a clientes reales
take('pruebas', c.es_prueba.astype(float), 1.0)
# 3b. Bloqueados (tarjeta congelada, REUS o ARCO, lista negra) en promocional: proporción de E7a por familia x canal
c['sh_bloq'] = (c.bloq / c.e7a_tot.where(c.e7a_tot > 0)).fillna(0)
take('bloqueados', promo.astype(float), c.sh_bloq)
# 3c. Duplicados: misma familia (otra versión) el mismo día y mismo canal, E6b (top 1,000 pares, 9 meses) -> /9
e6 = pd.read_csv('data/e6b_pares_familias.csv')
col = lambda x: x.str.replace(r'-\d{8}-', '-', regex=True).str.lower()
dup = e6[(col(e6.familia_a) == col(e6.familia_b)) & (e6.canal_a == e6.canal_b)].copy()
ent_wa = c[c.canal == 'whatsapp'].wd.sum() / c[c.canal == 'whatsapp'].ws.sum()
dup['mxn'] = np.select([dup.canal_a == 'email', dup.canal_a == 'whatsapp'], [dup.usuario_dias_juntas * 0.05, dup.usuario_dias_juntas * ent_wa], 0.0)
print('\n== Duplicados E6b: pares', len(dup), 'usuario-días', M(dup.usuario_dias_juntas.sum()), 'MXN 9m', M(dup.mxn.sum()), 'al mes', M(dup.mxn.sum() / 9))
print(dup.groupby('canal_a').usuario_dias_juntas.sum())
# 3d. Email a dados de baja (E5b) en promocional: /9 meses
e5 = pd.read_csv('data/e5b_comms_despues_baja.csv')
print('E5b emails a dados de baja total', M(e5.emails_despues_de_baja.sum()), 'MXN al mes', e5.emails_despues_de_baja.sum() * 0.05 / 9)

# 3e. Apagar: señal apagar, no mueve, promocional activa -> separado por audiencia
ap = promo & (c.senal == 'apagar o rehacer') & (c.mueve == 0) & (c.activo == 1)
take('apagar', ap.astype(float), 1.0)
# 3f. Limpiar WhatsApp y rehacer (señal apagar, quien abre sí convierte): solo la parte que va a quien no lee/no hace clic en 90 días (E9b)
e9 = pd.read_csv('data/e9b_patron_respuesta_90d.csv')
wa_tot = e9.msgs_wa_entregados.sum(); em_tot = e9.msgs_email.sum()
sh_wa_noread = e9[e9.resp_wa == 0].msgs_wa_entregados.sum() / wa_tot
sh_em_noclic = e9[e9.resp_email == 0].msgs_email.sum() / em_tot
sh_wa_none = e9[(e9.resp_email + e9.resp_push + e9.resp_wa + e9.resp_inapp) == 0].msgs_wa_entregados.sum() / wa_tot
sh_em_none = e9[(e9.resp_email + e9.resp_push + e9.resp_wa + e9.resp_inapp) == 0].msgs_email.sum() / em_tot
print('\n== E9b: WA entregado a quien no leyó WA en 90d', round(sh_wa_noread * 100, 1), '% (de ellos a quien no responde nada', round(sh_wa_none * 100, 1), '%); email a quien no hizo clic en 90d', round(sh_em_noclic * 100, 1), '% (nada:', round(sh_em_none * 100, 1), '%)')
lim = promo & (c.senal == 'apagar o rehacer') & (c.mueve == 1) & (c.activo == 1)
frac = np.select([c.canal == 'whatsapp', c.canal == 'email'], [sh_wa_noread, sh_em_noclic], 0.0)
take('limpiar_rehacer', lim.astype(float), frac)
# 3g. Canal preferido sobre el resto del promocional: quitar el canal mudo de quien responde por otro (no incluye a quien no responde a nada)
frac_cp = np.select([c.canal == 'whatsapp', c.canal == 'email'], [sh_wa_noread - sh_wa_none, sh_em_noclic - sh_em_none], 0.0)
take('canal_preferido', promo.astype(float), frac_cp)
# 3h. A quien no responde a nada en 90 días (resto): reactivación acotada con control, no corte
frac_n = np.select([c.canal == 'whatsapp', c.canal == 'email'], [sh_wa_none, sh_em_none], 0.0)
take('sin_respuesta_90d', promo.astype(float), frac_n)

print('\n== Palancas (septiembre, MXN y mensajes)')
for k, (v, m) in out.items(): print(f'{k:20s} {M(v):>10s} MXN  {M(m):>10s} msgs')
tot = sum(v for v, _ in out.values()); print('total', M(tot))
SEP = 4233202; AVG = 57662758 / 9
print('sep cost', M(SEP), 'avg', M(AVG))
# corte por audiencia de la palanca apagar y limpiar
for k in ['apagar', 'limpiar_rehacer', 'bloqueados', 'canal_preferido', 'sin_respuesta_90d', 'pruebas']:
    print('\n--', k, 'por audiencia'); print((c.groupby('aud')[k].sum() / 1e6).round(3).to_string())
    print('-- por equipo'); print((c.groupby('equipo')[k].sum() / 1e6).round(3).to_string())
    print('-- por canal'); print((c.groupby('canal')[k].sum() / 1e6).round(3).to_string())
    print('-- por producto'); print((c.groupby('prod')[k].sum() / 1e6).round(3).to_string())
c.to_pickle(W + 'c_sep.pkl')
