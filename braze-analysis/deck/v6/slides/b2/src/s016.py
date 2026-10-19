"""Lámina 16: franjas de puntos por equipo: cada campaña de push por su apertura (escala por múltiplos), tamaño = push enviados,
color = abre menos de 1 de cada 100 (azul) o más (gris). A la derecha, push de cada equipo debajo de 1 %."""
import math
from b2base import *

d = load_b()
p = d[d.canal == 'push notification']
fa = p.groupby(['fam', 'equipo', 'gan', 'aud']).agg(env=('pn_send', 'sum'), op=('pn_open', 'sum')).reset_index()
fa['ab'] = 100 * fa.op / fa.env
fa['bajo'] = fa.ab < 1
T = fa.env.sum() / 1e6
B = fa[fa.bajo].env.sum() / 1e6
eq = fa.groupby('equipo').apply(lambda g: pd.Series({'env': g.env.sum() / 1e6, 'bajo': g[g.bajo].env.sum() / 1e6, 'ab': 100 * g.op.sum() / g.env.sum()}))
eq['pct'] = 100 * eq.bajo / eq.env
eq['share_bajo'] = 100 * eq.bajo / B
gan = fa.groupby('gan').apply(lambda g: 100 * g[g.bajo].env.sum() / g.env.sum())
aud = fa.groupby('aud').apply(lambda g: 100 * g[g.bajo].env.sum() / g.env.sum())
mes = p.groupby('m').apply(lambda g: 100 * g.pn_open.sum() / g.pn_send.sum())
print('total', T, 'bajo', B, B / T, 'apertura', 100 * fa.op.sum() / fa.env.sum(), 'max mes', mes.max())
print(eq.round(2)); print(gan.round(0).to_dict()); print(aud.round(0).to_dict())
sel = fa[fa.env >= 1e5]
print('campañas con 100 mil o más', len(sel), sel.env.sum() / fa.env.sum())

S = Svg('Cada punto es una campaña de push con 100 mil o más envíos, por equipo, según cuántos la abren de cada cien; '
        'en Marketing la mayor parte del push abre menos de 1 de cada 100.')
S.circle(5, 14, 5, BLUE, '')
S.t(15, 18, 'Abre menos de 1 de cada 100', 11.5, INK, w=600)
S.circle(205, 14, 5, G1, '')
S.t(215, 18, 'Abre 1 o más de cada 100', 11.5, TXT)
S.line(398, 7, 398, 21, INK, 2.4)
S.t(406, 18, 'Apertura de todo el push del equipo', 11.5, TXT)
S.t(0, 36, 'Cada punto es una campaña con todas sus versiones; el tamaño es el número de push enviados.', 10.5, SEC)
EQ = ['Marketing', 'Others', 'Product Growth', 'Sales', 'Collections']
X0, X1 = 112, 560
LO, HI = math.log10(0.1), math.log10(20)
sx = lambda v: X0 + (X1 - X0) * (math.log10(min(max(v, 0.1), 20)) - LO) / (HI - LO)
Y0, RH = 86, 54
YB = Y0 + RH * len(EQ)
for v in (0.1, 0.2, 0.5, 1, 2, 5, 10, 20):
    S.line(sx(v), Y0 - 10, sx(v), YB - 6, GRID)
    S.t(sx(v), YB + 10, '0.1 % o menos' if v == 0.1 else f'{v:g} %', 11, SEC, 'middle')
S.t(X1, YB + 28, 'Personas que abren de cada cien que reciben el push (escala que crece por múltiplos)', 11, SEC, 'end')
S.line(sx(1), Y0 - 18, sx(1), YB - 6, INK, 1.2)
S.t(sx(1) + 4, Y0 - 20, '1 de cada 100', 11, INK, 'start', 600, halo=True)
S.line(sx(0.75), Y0 - 10, sx(0.75), YB - 6, INK, 1, ' stroke-dasharray="3 3" opacity="0.6"')
S.t(sx(0.75) - 4, Y0 - 20, 'Mínimo aceptable: 0.75', 10.5, SEC, 'end', halo=True)
r = lambda env: 1.8 + 1.15 * math.sqrt(env / 1e5)
rng = np.random.default_rng(7)
C1, C2 = 690, 778
S.t(C1, Y0 - 26, 'Push que abre', 10.5, SEC, 'end')
S.t(C1, Y0 - 14, 'menos de 1 %', 10.5, SEC, 'end')
S.t(C2, Y0 - 26, 'Parte de', 10.5, SEC, 'end')
S.t(C2, Y0 - 14, 'su push', 10.5, SEC, 'end')
for k, e_ in enumerate(EQ):
    yc = Y0 + RH * k + RH / 2 - 8
    hi = e_ == 'Marketing'
    S.t(X0 - 12, yc + 4, e_, 11.5, INK if hi else TXT, 'end', 600 if hi else 400)
    S.line(0, Y0 + RH * k + RH - 6, 780, Y0 + RH * k + RH - 6, GRID, 0.6)
    g = sel[sel.equipo == e_].sort_values('env', ascending=False)
    for q in g.itertuples():
        jit = rng.uniform(-13, 13)
        S.circle(sx(q.ab), yc + jit, r(q.env), BLUE if q.bajo else G1, ' fill-opacity="0.75" stroke="#FFFFFF" stroke-width="0.8"')
    med = float(np.average(g.ab, weights=g.env))
    S.line(sx(med), yc - 19, sx(med), yc + 19, INK, 2.4)
    S.t(sx(med), yc - 22, f'{med:.1f} %', 10.5, INK, 'middle', 700, halo=True)
    S.t(C1, yc - 2, (f'{eq.loc[e_, "bajo"]:.1f}' if eq.loc[e_, "bajo"] < 1 else f'{eq.loc[e_, "bajo"]:.0f}') + f' M de {eq.loc[e_, "env"]:.0f} M', 11.5, INK if hi else TXT, 'end', 600 if hi else 400)
    S.t(C1, yc + 12, f'{eq.loc[e_, "share_bajo"]:.0f} % del total', 10.5, SEC, 'end')
    S.t(C2, yc + 4, f'{eq.loc[e_, "pct"]:.0f} %', 12, BLUE if eq.loc[e_, 'pct'] >= 50 else INK, 'end', 700)
S.t(0, 404, f'Total: {B:.0f} M de {T:.0f} M push ({100*B/T:.0f} %) en campañas que abre menos de 1 de cada 100.', 11.5, INK, w=600)
svg = S.done()
camp = lambda s: fa[fa.fam.str.contains(s, regex=False)].sort_values('env').iloc[-1]
rf = camp('Leads_BDDMarketing-RescateFinesDeSemana'); an = camp('Anonimos-RescateTasa0'); pg = camp('Nuevos_RegistradosPay-Tasa0')
pr = camp('Payment Received'); ai = camp('Active-Retargeting_Installments'); pc = camp('Precobranza-ecosystem'); qs = fa[fa.fam.str.contains('Quincenas')].sort_values('env').iloc[-1]
print(rf.env, rf.ab, an.env, an.ab, pg.env, pg.ab, pr.ab, ai.ab, pc.ab, qs.fam, qs.ab)
save(16, dict(
    kind='grafica',
    titulo='La mitad del push va en campañas que casi nadie abre, y dos terceras partes de ese push son de Marketing',
    que='Tasa 0, lanzamientos, rescates de fin de semana y referidos.',
    quien=f'Marketing pone {eq.loc["Marketing","bajo"]:.0f} M de los {B:.0f} M push que abre menos de 1 de cada 100.',
    a_quien=f'Leads ({aud["leads"]:.0f} % de su push abre menos de 1 %) y bases frías ({aud["frios"]:.0f} %).',
    lecturas=[
        f'{B:.0f} M de {T:.0f} M push ({100*B/T:.0f} %) van en campañas que abre menos de 1 de cada 100 personas.',
        f'Rescate de fin de semana a leads de Marketing: {rf.env/1e6:.1f} M push y {rf.ab:.2f} % de apertura.',
        f'Sí se abren los que la persona espera: pago recibido {pr.ab:.0f} %, Installments a activos {ai.ab:.0f} %.',
    ],
    causa='El push se usa para mandar ofertas a toda la lista porque no cuesta, sin ver si esa persona abrió uno en meses.',
    sowhat='Push solo a quien abrió uno en 60 días y con una razón para esa persona; para el resto, otro canal.',
    fuente=f'{FUENTE_E1}. Apertura directa sobre enviados. {len(sel)} campañas con 100 mil o más push ({100*sel.env.sum()/fa.env.sum():.0f} % del canal).',
    svg=svg,
))
