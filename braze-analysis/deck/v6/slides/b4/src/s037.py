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
ROWS = [
 ('B0444', 'Mundial y Referidos', 'Versiones del mismo push'),
 ('B0171', 'Rescate Tasa 0', 'Dos audiencias; WhatsApp doble'),
 ('disbursed', 'Aviso de desembolso KCash', 'Dos versiones del correo'),
 ('B0326', 'Referidos', 'Versiones de correo y push'),
 ('B0333', 'Churn de 12 meses', 'Tres versiones del WhatsApp'),
 ('B0440', 'Anota y Gana', 'Versión KCash y versión KPay'),
 ('B0493', 'Hot Sale KUESKIPROMO', 'El mismo push el 27 y el 29 de mayo'),
 ('B0490', 'Amazon antes del Hot Sale', 'Dos versiones; push y correo'),
 ('B0223', 'Nunca activos', 'Correo y WhatsApp el mismo día'),
]
TEAMC = {'Marketing': BLUE, 'Product Growth': GREEN, 'Sales': INK, 'Others': SEC}
h = ['<table><tr><th>Campaña</th><th>Equipo</th><th>Qué se repite</th><th class="num">Personas-día</th><th class="num">WhatsApp de más</th></tr>']
used = 0
for k, name, what in ROWS:
    r = g.loc[k]; used += r.pd_
    team_lab = {'Product Growth': 'Prod. Growth'}.get(r.team, r.team) if k != 'disbursed' else 'Sin equipo'
    col = TEAMC.get(r.team, SEC) if k != 'disbursed' else SEC
    cwa = f'{r.cwa/1e3:.0f} mil MXN' if r.cwa > 0 else '0 MXN'
    pers = f'{r.pers/1e6:.2f} M' if r.pers >= 1e6 else f'{r.pers/1e3:.0f} mil'
    h.append(f'<tr><td>{name}</td><td style="color:{col};font-weight:600">{team_lab}</td><td>{what}</td><td class="num">{r.pd_/1e6:.2f} M</td><td class="num">{cwa}</td></tr>')
rest = TOT - used; rest_cwa = costo - sum(g.loc[k].cwa for k, *_ in ROWS)
h.append(f'<tr><td>Otras {len(g) - len(ROWS)} campañas</td><td></td><td></td><td class="num">{rest/1e6:.2f} M</td><td class="num">{rest_cwa/1e3:.0f} mil MXN</td></tr>' if rest_cwa > 500 else
         f'<tr><td>Otras {len(g) - len(ROWS)} campañas</td><td></td><td></td><td class="num">{rest/1e6:.2f} M</td><td class="num"></td></tr>')
h.append(f'<tr><td style="font-weight:700">Total medido</td><td></td><td></td><td class="num" style="font-weight:700">{TOT/1e6:.1f} M</td><td class="num" style="font-weight:700">{costo/1e6:.2f} M MXN</td></tr></table>')

write(37, dict(kind='html', seccion='IV. La misma persona, demasiadas veces',
 titulo=f'La misma campaña le llega dos veces el mismo día a la misma persona, y solo el WhatsApp repetido costó {costo/1e6:.2f} M MXN',
 que='La misma campaña en dos versiones, dos audiencias o dos canales: Rescate Tasa 0, Mundial y Referidos, Hot Sale, Comercio del día, churn por WhatsApp, nunca activos y el aviso de desembolso.',
 quien=f'Marketing {byteam["Marketing"]:.1f} M de {TOT/1e6:.1f} M personas-día repetidas; Product Growth {byteam["Product Growth"]:.1f} M; Sales {byteam["Sales"]:.1f} M; aviso de desembolso de KCash (transaccional, sin equipo en el nombre) {byteam["Others"]:.1f} M.',
 a_quien='Hot leads y base rezagada (Marketing), churn de 12 meses y nunca activos (Product Growth), recurrentes de KPay (Sales) y clientes que acaban de recibir su préstamo.',
 lecturas=[
  f'{mismo/10:.0f} de cada diez repeticiones son en el mismo canal: dos push o dos correos iguales el mismo día.',
  'Se lanza la misma campaña por audiencia o por día sin excluir a quien ya la recibió, y la versión vieja sigue activa cuando se crea la nueva.',
  f'WhatsApp repetido: {ww/1e6:.2f} M envíos de más; con la entrega real de esas campañas ({100*ent:.0f} %) son {costo/1e6:.2f} M MXN en 9 meses, unos {costo/9/1e3:.0f} mil MXN al mes.',
 ],
 causa='No hay una regla en Braze que impida mandar la misma campaña dos veces el mismo día a la misma persona, ni alguien que apague la versión vieja.',
 sowhat='Una regla de Braze (no repetir la misma campaña a la misma persona el mismo día) y apagar versiones viejas lo resuelve sin tocar el contenido.',
 fuente=f'Fuente: Braze, E6b (1,000 pares de campañas más frecuentes el mismo día; {TOT/1e6:.1f} M de {ALL/1e6:.0f} M personas-día, {100*TOT/ALL:.0f} %, es un mínimo). Misma campaña = mismo nombre sin fecha o mismo ticket del mismo equipo, sin tickets genéricos. Entrega de WhatsApp: E1, a 1.00 MXN por entregado.',
 html=''.join(h)))
