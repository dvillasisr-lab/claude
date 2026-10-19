# Datos de la lámina 3 (caso de negocio). Correr desde braze-analysis/. Lee los pickles de p6work (s1, s2, s5).
import re, json, pandas as pd, numpy as np
W = '/tmp/claude-0/-home-user-claude/e114ba4f-39d4-57f8-9f24-b0f0c0cbef51/scratchpad/v6parts/p6work/'
c = pd.read_pickle(W + 'c_sep2.pkl'); g1 = pd.read_pickle(W + 'g1.pkl'); camp = pd.read_pickle(W + 'camp.pkl')

# ---- 1. Verificación: ¿la cifra cuenta las lecturas de WhatsApp registradas el mes siguiente?
w = g1[g1.canal == 'whatsapp']
late = w[w.env == 0]
wr_all = w.groupby(['fam', 'canal']).wr.sum(); wr_act = w[w.env > 0].groupby(['fam', 'canal']).wr.sum()
cw = camp[camp.canal == 'whatsapp'].set_index(['fam', 'canal'])
ok = bool(np.allclose(cw.wr, wr_all.reindex(cw.index).fillna(0)))
# señal con y sin lecturas tardías
cw2 = cw.copy(); cw2['wr_sin'] = wr_act.reindex(cw.index).fillna(0); cw2['wd_sin'] = w[w.env > 0].groupby(['fam', 'canal']).wd.sum().reindex(cw.index).fillna(0)
cw2['resp_sin'] = cw2.wr_sin / cw2.wd_sin.where(cw2.wd_sin > 0)
cambia = cw2[(cw2.vol == 'alto') & (cw2.resp >= 0.60) & (cw2.resp_sin < 0.60)]
verif = dict(camp_wr_igual_a_todas_las_filas_E1=ok, filas_wa_sin_envio=int(len(late)), lecturas_en_filas_sin_envio=int(late.wr.sum()),
             familias_wa_que_salen_de_apagar_por_lecturas_tardias=int(len(cambia)))
print('VERIFICACION', verif)
print(cambia[['resp', 'resp_sin', 'equipo']].round(3))

# ---- 2. Palancas (septiembre, MXN al mes), mismo orden y reglas de s2/s6
rec = c.aud.str.startswith('recup')
c['ap_act'] = c.apagar * (~rec); c['ap_rec'] = c.apagar * rec
c['limpiar_wa'] = np.where(c.canal == 'whatsapp', c.limpiar_rehacer, 0.0)
c['rehacer_em'] = np.where(c.canal == 'email', c.limpiar_rehacer, 0.0)
# duplicados (E6b, igual que s2) con equipo por familia_a
e6 = pd.read_csv('data/e6b_pares_familias.csv')
col = lambda x: x.str.replace(r'-\d{8}-', '-', regex=True).str.lower()
dup = e6[(col(e6.familia_a) == col(e6.familia_b)) & (e6.canal_a == e6.canal_b)].copy()
ent_wa = c[c.canal == 'whatsapp'].wd.sum() / c[c.canal == 'whatsapp'].ws.sum()
dup['mxn'] = np.select([dup.canal_a == 'email', dup.canal_a == 'whatsapp'], [dup.usuario_dias_juntas * 0.05, dup.usuario_dias_juntas * ent_wa], 0.0) / 9
famq = c.drop_duplicates('fam').assign(k=lambda d: d.fam.str.lower()).set_index('k').equipo
dup['equipo'] = col(dup.familia_a).map(lambda f: famq.get(f, np.nan))
dup['equipo'] = dup.equipo.fillna(dup.familia_a.str.split('-').str[0].map({'Mkt': 'Marketing', 'Marketing': 'Marketing', 'Lending': 'Product Growth', 'Sales': 'Sales'})).fillna('Others')
print('dup sin equipo directo', dup.equipo.isna().sum(), dup.groupby('equipo').mxn.sum().round(0).to_dict())

PAL = [  # clave, etiqueta, certeza
    ('bloqueados', 'Excluir bloqueados', 'seguro'),
    ('duplicados', 'Quitar duplicados del mismo día', 'seguro'),
    ('pruebas', 'Pruebas internas a clientes', 'seguro'),
    ('ap_act', 'Apagar canal caro: leads y registrados', 'seguro'),
    ('rehacer_em', 'Rehacer email', 'seguro'),
    ('limpiar_wa', 'Limpiar WhatsApp', 'seguro'),
    ('canal_preferido', 'Canal preferido', 'seguro'),
    ('ap_rec', 'Apagar canal caro: ex clientes', 'medir'),
    ('sin_respuesta_90d', 'Sin respuesta en 90 días', 'medir'),
]
EQ = ['Product Growth', 'Marketing', 'Sales', 'Others', 'Collections']
rows = []
for k, lab, cert in PAL:
    by = (dup.groupby('equipo').mxn.sum() if k == 'duplicados' else c.groupby('equipo')[k].sum()).reindex(EQ).fillna(0)
    tot = by.sum(); top = by.idxmax()
    rows.append(dict(k=k, lab=lab, cert=cert, mxn=tot, top=top, top_sh=by[top] / tot, eq=by.to_dict()))
T = pd.DataFrame(rows)
SEP = c.c_sep.sum(); AVG = 57662758 / 9
seg = T[T.cert == 'seguro'].mxn.sum(); med = T[T.cert == 'medir'].mxn.sum(); tot = seg + med
eqtot = pd.DataFrame([r['eq'] for r in rows]).sum()
eqmed = pd.DataFrame([r['eq'] for r in rows if r['cert'] == 'medir']).sum()
R = dict(sep=SEP, avg=AVG, seguro=seg, medir=med, total=tot, resultante=SEP - tot, tras_seguro=SEP - seg,
         pct_sep=tot / SEP, pct_avg=tot / AVG, anual=tot * 12, anual_seg=seg * 12, anual_med=med * 12,
         seg_pct_sep=seg / SEP, seg_pct_avg=seg / AVG,
         desperdicio=T[T.k.isin(['bloqueados', 'duplicados', 'pruebas'])].mxn.sum(),
         cortar30=T[T.k.isin(['ap_act', 'rehacer_em', 'limpiar_wa'])].mxn.sum(),
         eq=eqtot.to_dict(), eq_sh=(eqtot / tot).to_dict(), eq_medir=eqmed.to_dict(),
         msgs=sum(c[x + '_msgs'].sum() for x in ['pruebas', 'bloqueados', 'apagar', 'limpiar_rehacer', 'canal_preferido', 'sin_respuesta_90d']),
         msgs_sep=c.env_sep.sum(), verif=verif)
print(T[['lab', 'cert', 'mxn', 'top', 'top_sh']].round(3).to_string())
for k, v in R.items(): print(k, v if isinstance(v, dict) else round(v / 1e6, 3) if v > 10 else round(v, 4))
json.dump(dict(T=T.to_dict('records'), R=R), open('/tmp/claude-0/-home-user-claude/e114ba4f-39d4-57f8-9f24-b0f0c0cbef51/scratchpad/muestras/s3_datos.json', 'w'), default=float, ensure_ascii=False, indent=1)
