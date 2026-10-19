"""Lámina 37: la misma campaña repetida el mismo día a la misma persona (E6b) y costo del WhatsApp repetido (E1)."""
import re, pandas as pd
from kit import *
from e6b import load
p = load()
GEN = {'B0000', 'T0000', 'B001', 'T000', 'S0004'}
def core(n):
    s = str(n).split('-')
    if len(s) >= 7 and re.fullmatch(r'\d{8}', s[2]): return '-'.join([s[0], s[1], s[3]] + s[5:])
    return re.sub(r'\d{8}', '', str(n)).lower().replace('push', '').replace('email', '').replace('mail', '').strip(' -_')
same = (p.fam_a == p.fam_b) | ((p.tick_a == p.tick_b) & p.tick_a.notna() & ~p.tick_a.isin(GEN) & (p.ta == p.tb)) | (p.familia_a.map(core) == p.familia_b.map(core))
s = p[same].copy()
s['g'] = ['disbursed' if 'disbursed' in a else t for a, t in zip(s.familia_a, s.tick_a)]
s['ww'] = (s.canal_a == 'whatsapp') & (s.canal_b == 'whatsapp')
TOT, ALL = s.usuario_dias_juntas.sum(), p.usuario_dias_juntas.sum()
mismo = 100 * s[s.canal_a == s.canal_b].usuario_dias_juntas.sum() / TOT
# entrega real de las campañas con WhatsApp repetido (E1)
e1 = pd.read_csv(D + 'e1_comunicacion_mes_canal.csv')
names = set(s[s.ww].familia_a) | set(s[s.ww].familia_b)
w = e1[(e1.canal == 'whatsapp') & e1.communication_name.isin(names)]
ent = w.whatsapp_delivery.sum() / w.whatsapp_send.sum()
ww = s[s.ww].usuario_dias_juntas.sum(); costo = ww * ent * 1.0
print('repetido M', TOT / 1e6, 'de', ALL / 1e6, 'mismo canal', mismo, 'ww', ww / 1e6, 'entrega', ent, 'costo M MXN', costo / 1e6, 'nombres', len(names), len(w.communication_name.unique()))
byteam = s.groupby('ta').usuario_dias_juntas.sum() / 1e6; print(byteam.round(2).to_dict())
g = s.groupby('g').agg(pd_=('usuario_dias_juntas', 'sum'), pers=('usuarios_aprox', 'max'), team=('ta', 'first'),
                        ww=('usuario_dias_juntas', lambda x: x[s.loc[x.index, 'ww']].sum())).sort_values('pd_', ascending=False)
g['cwa'] = g.ww * ent
print(g)
s['vez'] = s.usuario_dias_juntas / s.usuarios_aprox
s['kind'] = ['ww' if w else ('mismo' if ca == cb else 'dos') for w, ca, cb in zip(s.ww, s.canal_a, s.canal_b)]
print(s.sort_values('vez', ascending=False).head(8)[['familia_a', 'familia_b', 'kind', 'usuarios_aprox', 'vez', 'meses']].to_string())
COLK = {'ww': GREEN, 'mismo': BLUE, 'dos': G1}
S = Svg('Dispersión: cada punto es una campaña que le llegó dos veces el mismo día a la misma persona; personas contra veces por persona en el periodo')
S.circle(6, 15, 4.5, GREEN); S.t(15, 19, 'WhatsApp dos veces (se paga cada uno)', 11, TXT)
S.circle(246, 15, 4.5, BLUE); S.t(255, 19, 'Dos push o dos correos iguales', 11, TXT)
S.circle(450, 15, 4.5, G1); S.t(459, 19, 'La misma campaña por dos canales', 11, TXT)
S.t(0, 38, f'{len(s)} repeticiones; tamaño = personas-día repetidas.', 10.5, SEC)
import math
X0, X1, Y0, Y1 = 44, 770, 60, 352
lo, hi_ = math.log10(15000), math.log10(2e6); ylo, yhi = math.log10(0.8), math.log10(14)
sx = lambda v: X0 + (X1 - X0) * (math.log10(v) - lo) / (hi_ - lo); sy = lambda v: Y1 - (Y1 - Y0) * (math.log10(v) - ylo) / (yhi - ylo)
for v in (1, 2, 4, 8):
    S.line(X0, sy(v), X1, sy(v)); S.t(X0 - 6, sy(v) + 4, f'{v}', 10.5, SEC, 'end')
S.t(X0 + 2, Y0 - 6, 'Días con la repetición por persona (escala logarítmica)', 10.5, SEC)
for v, l in ((20000, '20 mil'), (50000, '50 mil'), (100000, '100 mil'), (250000, '250 mil'), (500000, '500 mil'), (1000000, '1 M')):
    S.line(sx(v), Y1, sx(v), Y1 + 5, SEC); S.t(sx(v), Y1 + 18, l, 10.5, SEC, 'middle')
S.line(X0, Y1, X1, Y1, SEC); S.t((X0 + X1) / 2, Y1 + 33, 'Personas que recibieron la campaña dos veces el mismo día (escala logarítmica)', 10.5, SEC, 'middle')
for _, q in s.sort_values('usuario_dias_juntas', ascending=False).iterrows():
    S.circle(sx(q.usuarios_aprox), sy(max(q.vez, 0.85)), 3 + 9 * math.sqrt(q.usuario_dias_juntas / 1.2e6), COLK[q.kind], '#FFFFFF', 1)
def nm(k1, k2, kind, tx, ty, l1, l2, anc='start'):
    q = s[s.familia_a.str.contains(k1) & s.familia_b.str.contains(k2) & (s.kind == kind)].sort_values('usuario_dias_juntas').iloc[-1]
    lab(S, sx(q.usuarios_aprox), sy(max(q.vez, 0.85)), sx(tx), sy(ty), l1, l2, anc)
nm('BBDDHotLeadsW1RescateTasa0', 'BBDDRezagada-RescateTasa0', 'ww', 300000, 5.5, 'Rescate Tasa 0 (Marketing), 1 jun', '112 mil personas, dos WhatsApp unas 3 veces')
nm('Anonimos-RescateTasa0', 'BBDDRezagada-RescateTasa0', 'mismo', 60000, 12, 'Rescate Tasa 0 por push (Marketing)', 'anónimos y rezagados, 11 días por persona')
nm('Churn_12MesesInactividad', 'Churn_12MesesInactividad', 'ww', 22000, 2.6, 'Churn de 12 meses (Product Growth)', 'tres versiones del WhatsApp en abril')
nm('disbursed', 'disbursed', 'mismo', 1.6e6, 3.2, 'Aviso de desembolso de KCash', 'dos versiones, 600 mil, 4 meses', 'end')
nm('ReferralProgram', 'BAUMundial', 'mismo', 1.9e6, 1.3, 'Mundial y Referidos (Marketing)', '11 jun, dos push a 1.13 M', 'end')
nm('HotSaleKUESKIPROMOEnterprise', 'HotSaleKUESKIPROMOEnterprise', 'mismo', 130000, 1.6, 'Hot Sale (Sales): el mismo push', '27 y 29 de mayo a 326 mil', 'start')

write(37, dict(kind='grafica', seccion='IV. La misma persona, demasiadas veces',
 titulo=f'La misma campaña le llega dos veces el mismo día a la misma persona; el WhatsApp repetido costó {costo/1e6:.2f} M MXN',
 que='Rescate Tasa 0, Mundial y Referidos, Hot Sale, churn, nunca activos y aviso de desembolso',
 quien='Marketing (6 de cada 10), Product Growth, Sales y el aviso de desembolso de KCash',
 a_quien='Hot leads y base rezagada, churn, recurrentes de KPay y clientes con préstamo nuevo',
 lecturas=[
  f'{TOT/1e6:.1f} M personas-día con la misma campaña repetida; {mismo/10:.0f} de cada 10 en el mismo canal.',
  f'WhatsApp repetido: {ww/1e6:.2f} M envíos de más, {costo/1e6:.2f} M MXN en 9 meses (unos {costo/9/1e3:.0f} mil MXN al mes).',
  'Se lanza la misma campaña por audiencia o por día sin excluir a quien ya la recibió.',
 ],
 causa='Braze no impide repetir la misma campaña el mismo día y nadie apaga la versión vieja al crear la nueva.',
 sowhat='Una regla de Braze (no repetir campaña el mismo día) y apagar versiones viejas lo resuelve.',
 fuente=f'Fuente: Braze, E6b (1,000 pares más frecuentes, enero a septiembre 2026; es un mínimo) y E1 (entrega de WhatsApp {100*ent:.0f} %, a 1.00 MXN por entregado). Misma campaña = mismo nombre sin fecha o mismo ticket.',
 svg=S.svg()))
