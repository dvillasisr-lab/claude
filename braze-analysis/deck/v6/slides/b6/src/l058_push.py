"""Lámina 58: apertura de push por tema dentro de cada grupo de audiencia (E1; grupo y tema por el nombre de la campaña) y, al lado,
de cada 100 personas que reciben el correo de una campaña, cuántas reciben su push y cuántas lo abren (E1, mismas campañas y mes)."""
from comun import *

e1 = load_e1()
e1['tema'] = e1.communication_name.map(gancho_of)
pp = e1[e1.canal == 'push notification'].groupby(['grupo', 'tema']).agg(env=('pn_send', 'sum'), op=('pn_open', 'sum'))
pp['ap'] = 100 * pp.op / pp.env
pp = pp[pp.env > 500000]
OF = ['Tasa 0', 'Referidos', 'Descuento, cupón u oferta', 'Lanzamiento y novedades']
# alcance: campañas con email y push el mismo mes (p4_app.py)
x = e1[e1.canal.isin(['email', 'push notification', 'in-app'])]
pv = x.pivot_table(index=['grupo', 'familia', 'mes'], columns='canal', values='usuarios_aprox', aggfunc='sum').fillna(0)
pv = pv.join(x[x.canal == 'push notification'].groupby(['grupo', 'familia', 'mes']).pn_open.sum()).fillna(0)
both = pv[(pv['email'] > 1000) & (pv['push notification'] > 0)]
al = both.groupby('grupo')[['email', 'push notification', 'in-app', 'pn_open']].sum()
al['push'] = 100 * al['push notification'] / al.email; al['inapp'] = 100 * al['in-app'] / al.email; al['abre'] = 100 * al.pn_open / al.email
G = [('nuevos', 'Nuevos'), ('activos', 'Activos y recurrentes'), ('leads', 'Leads y registrados recientes'), ('ex clientes', 'Ex clientes inactivos'), ('nunca activaron', 'Leads que nunca activaron')]
k = pd.read_csv(H / 'muestra_k_abren_vs_no_abren.csv').set_index(['fam', 'canal'])
b211 = k.loc[('Lending-KCash-B0211-CANVAS-Nuevos_RegistradosPay-Tasa0-N/A', 'push notification')]
def fr(pat, ch='push notification'):
    g = e1[e1.familia.str.contains(pat, regex=False) & (e1.canal == ch)]; return resp(g, ch), g.envios.sum()
ap211, _ = fr('Lending-KCash-B0211-CANVAS-Nuevos_RegistradosPay-Tasa0'); ap171, v171 = fr('Marketing-KCash-B0171-CANVAS-Anonimos-RescateTasa0')
apvf, _ = fr('Marketing-KCash-B0000-CANVAS-Leads_LeftFunnel-Retargeting_Veriff'); ap301, _ = fr('Lending-KCash-B0301-CANVAS-Active-Retargeting_Installments_SP')
print(pp.round(2)); print(al[['push', 'inapp', 'abre']].round(1)); print(ap211, ap171, v171, apvf, ap301, b211.lift)

s = SVG('Apertura de push por grupo de audiencia: recordatorio de algo empezado contra ofertas; y de cada 100 que reciben el correo, cuántos reciben y abren el push')
s.t(0, 16, 'Apertura del push, enero a septiembre', 12, INK, w=600)
s.legend([(GREEN, 'Recordatorio de algo empezado', 'dot'), (BLUE, 'Tasa 0', 'dot'), (M1, 'Otras ofertas', 'dot')], 0, 26, size=11)
X0, X1 = 196, 470
xs = lambda v: X0 + (X1 - X0) * v / 13
TOP, RH = 92, 58
for v in (0, 4, 8, 12):
    s.line(xs(v), TOP - 14, xs(v), TOP + RH * 5 - 20); s.t(xs(v), TOP + RH * 5 - 4, f'{v} %', 11, SEC, 'middle')
PX = 530
s.t(PX, 16, 'De cada 100 que reciben el correo', 12, INK, w=600)
s.t(PX, 32, 'de la misma campaña y mes', 10.5, SEC)
s.legend([(M2, 'Reciben el push', 'rect'), (BLUE, 'Lo abren', 'rect')], PX, 40, size=11)
PW = 220; ps = lambda v: PW * v / 70
for i, (g, name) in enumerate(G):
    y = TOP + RH * i
    s.t(0, y + 4, name, 12, INK, w=600)
    s.line(0, y + 26, 780, y + 26, GRID)
    rows = pp.loc[g] if g in pp.index.get_level_values(0) else pd.DataFrame()
    of = rows[rows.index.isin(OF)]
    if len(of):
        s.line(xs(of.ap.min()), y, xs(of.ap.max()), y, M1, 2)
        for t_, q in of.iterrows():
            if t_ != 'Tasa 0': s.circle(xs(q.ap), y, 4.5, M1)
        lab_of = f'ofertas {of.ap.min():.1f} a {of.ap.max():.1f} %' if len(of) > 1 else f'{of.index[0]} {of.ap.iloc[0]:.1f} %'
        if 'Tasa 0' in of.index:
            s.circle(xs(of.loc['Tasa 0', 'ap']), y, 5.5, BLUE)
        s.t(xs(of.ap.min()) - 0, y + 18, lab_of, 10.5, SEC, 'start')
    if 'Recordatorio de algo empezado' in rows.index:
        v = rows.loc['Recordatorio de algo empezado', 'ap']
        s.circle(xs(v), y, 6, GREEN); s.t(xs(v), y - 10, f'{v:.1f} %', 11.5, INK, 'middle', 600, halo=True)
    else:
        s.t(X1, y - 8, 'sin recordatorio por push', 10.5, SEC, 'end')
    if g in al.index:
        q = al.loc[g]
        s.rect(PX, y - 9, ps(q.push), 10, M2); s.rect(PX, y + 3, max(ps(q.abre), 1.5), 10, BLUE)
        s.t(PX + ps(q.push) + 6, y + 0, f'{q.push:.0f}', 11.5, TXT)
        s.t(PX + max(ps(q.abre), 1.5) + 6, y + 12, f'{q.abre:.1f}', 11.5, INK, w=600)
s.t(0, 400, 'Grupo y tema según el nombre de la campaña. Otras ofertas: referidos, descuentos y lanzamientos, con 500 mil push o más en el grupo.', 10.5, SEC)
s.t(0, 414, 'Al lado: campañas con correo y push el mismo mes; personas sumadas entre campañas, sirve como proporción. Sin la app no hay push ni in-app.', 10.5, SEC)

L, A = pp.loc['leads'], pp.loc['activos']
ofA = A[A.index.isin(OF)].ap
write(58, dict(
    titulo='El push funciona cuando recuerda algo que la persona empezó; como oferta, y a quien no tiene la app, casi nadie lo abre',
    que='Ofertas: rescate con Tasa 0, referidos, Comercio del día y rescate de fin de semana. Recordatorios: terminar el registro y pagar la compra a meses.',
    quien='Marketing manda los push de oferta más grandes (B0171, B0391, B0326); Marketing y Product Growth, los recordatorios (B0000 y B0301).',
    a_quien='Ofertas a leads que nunca activaron, anónimos y registrados; recordatorios a quien está en registro o tiene una compra a meses.',
    lecturas=[
        f'Mismo grupo, distinto mensaje: entre leads y registrados recientes el recordatorio abre {L.loc["Recordatorio de algo empezado","ap"]:.1f} % y la Tasa 0 {L.loc["Tasa 0","ap"]:.2f} %; entre activos, {A.loc["Recordatorio de algo empezado","ap"]:.1f} % contra {ofA.min():.1f} a {ofA.max():.1f} % de las ofertas.',
        f'Distinto grupo, falta de app: de cada 100 leads que nunca activaron y reciben el correo, {al.loc["nunca activaron","push"]:.0f} reciben el push y {al.loc["nunca activaron","inapp"]:.0f} ven un in-app; en activos, {al.loc["activos","push"]:.0f} y {al.loc["activos","inapp"]:.0f}.',
        f'La Tasa 0 sí mueve a quien la abre: en el push de Product Growth a registrados sin crédito (B0211) quien abre convierte {b211.conv_abren:.1f} % contra {b211.conv_no_abren:.2f} %, pero lo abre {ap211:.2f} %, 1 de cada 200.',
    ],
    causa='Usamos el push como canal de ofertas para listas enteras, aunque buena parte no tiene la app, en lugar de usarlo para recordar lo que cada persona dejó a medias.',
    sowhat='Dos arreglos: push solo a quien tiene la app (dato de app instalada y último ingreso) y push como recordatorio de lo empezado, no como oferta repetida.',
    fuente=f'Fuente: Braze, envíos por campaña, mes y canal (E1) y quien abre contra quien no abre (E7c), enero a septiembre 2026. Ejemplos: rescate Tasa 0 a anónimos (B0171) {v171/1e6:.1f} M push con {ap171:.2f} % de apertura; recordatorio de verificar identidad (B0000) {apvf:.2f} %; compra a meses (B0301) {ap301:.1f} %.',
    svg=s.svg()))
