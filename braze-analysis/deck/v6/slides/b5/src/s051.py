"""Lámina 51: promociones a quien no puede comprar con KPay (línea congelada) y a quien pidió no recibir publicidad.
Arriba: mapa de calor equipo x tema de las promociones a personas con KPay congelado (M mensajes), con la parte que ofrece KPay.
Abajo: promociones a REUS o ARCO y a lista negra por equipo. Fuente E7a (campaña x canal x etapa) y E3 (personas por etapa)."""
from b5_svg import *

B = D['bloq']; F = B['freeze']; RE = B['reus']; NE = B['negra']; E3 = D['e3']
EQS = ['Marketing', 'Sales', 'Product Growth', 'Others']
TEM = [('Descuento, cupón u oferta', 'Descuento|o cupón'), ('Referidos', 'Referidos|'), ('Lanzamiento y novedades', 'Lanzamientos|'),
       ('Recordatorio de algo empezado', 'Recordatorio|de algo'), ('Tasa 0', 'Tasa 0|'), (None, 'Otros|')]
def cel(e, t):
    if t: return F['eq_tema'].get(f'{e}|{t}', 0)
    return F['eq'][e] - sum(F['eq_tema'].get(f'{e}|{tt}', 0) for tt, _ in TEM if tt)
MX = max(cel(e, t) for e in EQS for t, _ in TEM)
S = Svg('Promociones a personas con la línea KPay congelada por equipo y tema, en millones, con la parte que ofrece KPay; y promociones a quien pidió no recibir publicidad o está en lista negra, por equipo, en miles.')
S.t(0, 14, f'Promociones a las {mil(E3["4.Kpay CC Freeze"]["u"])} mil personas con la línea KPay congelada, M mensajes', 12, INK, w=600)
CX0, CW, RH, TOP = 112, 66, 31, 58
for j, (_, lab) in enumerate(TEM):
    l1, l2 = lab.split('|')
    S.t(CX0 + CW * j + CW / 2, TOP - 20 if l2 else TOP - 8, l1, 10.5, SEC, 'middle')
    if l2: S.t(CX0 + CW * j + CW / 2, TOP - 8, l2, 10.5, SEC, 'middle')
TX = CX0 + CW * len(TEM) + 26
S.t(TX, TOP - 8, 'Total', 10.5, SEC, 'middle')
KX0, KX1 = TX + 34, W - 4
S.t(KX0, TOP - 8, 'Qué producto ofrece', 10.5, SEC)
for i, e in enumerate(EQS):
    y = TOP + RH * i
    S.t(CX0 - 8, y + RH / 2 + 4, e, 12, INK, 'end', 600)
    for j, (t, _) in enumerate(TEM):
        v = cel(e, t); op = 0.06 + 0.86 * v / MX
        S.rect(CX0 + CW * j + 1, y + 1, CW - 2, RH - 2, BLUE, f' fill-opacity="{op:.2f}"')
        S.t(CX0 + CW * j + CW / 2, y + RH / 2 + 4, f'{v/1e6:.1f}' if v >= 50000 else '0', 11.5, '#FFFFFF' if op > 0.5 else INK, 'middle', 600 if v >= 3e6 else 400)
    S.t(TX, y + RH / 2 + 4, f'{F["eq"][e]/1e6:.1f}', 12, INK, 'middle', 600)
    kp = F['eq_prod'].get(f'{e}|kpay', 0); kc = F['eq_prod'].get(f'{e}|kcash', 0); tt = F['eq'][e]
    x = KX0; bw = KX1 - KX0 - 72
    for v, col in [(kp, BLUE), (kc, BLUEL), (tt - kp - kc, MARK2)]:
        w = bw * v / tt
        if w > 0.5: S.rect(x, y + 9, w - 1, RH - 18, col)
        x += w
    S.t(KX1, y + RH / 2 + 4, f'{100*kp/tt:.0f} % KPay', 11, INK, 'end', 600)
LY = TOP + RH * 4 + 16
lx = KX0
for lab, col in [('KPay', BLUE), ('KCash', BLUEL), ('Otro', MARK2)]:
    S.rect(lx, LY - 9, 10, 10, col); S.t(lx + 14, LY, lab, 10.5, TXT); lx += 14 + len(lab) * 6 + 12
S.t(0, LY, f'Total {M(F["promo"])} M promociones; {M(F["prod"]["kpay"])} M ofrecen KPay.', 11, INK, w=600)
# ---------- abajo: REUS o ARCO y lista negra ----------
BY = LY + 30
S.line(0, BY - 14, W, BY - 14, GRID)
for k, (blk, tit, x0) in enumerate([(RE, f'Pidieron no recibir publicidad (REUS o ARCO): {mil(blk_p := RE["promo"])} mil promociones', 0),
                                     (NE, f'Lista negra: {mil(NE["promo"])} mil promociones', 400)]):
    S.t(x0, BY + 4, tit, 11.5, INK, w=600)
    mx = max(blk['eq'].values())
    for i, e in enumerate(EQS):
        y = BY + 18 + 30 * i
        S.t(x0 + 100, y + 11, e, 11, TXT, 'end')
        v = blk['eq'].get(e, 0); w = 200 * v / mx
        S.rect(x0 + 108, y + 1, max(w, 1), 14, BLUE if k == 0 else MARK)
        S.t(x0 + 114 + w, y + 12, f'{mil(v)} mil', 11, INK, w=600)
S.t(0, HH - 6, 'Línea KPay congelada: la marca cc_freeze del golden dataset dice que la persona no puede comprar con KPay; la causa de cada caso no viene en los datos.', 10.5, SEC)
SVG = S.done()

ex_min = D['excl_min']; ex_all = F['promo'] + RE['promo'] + NE['promo']
u = E3['4.Kpay CC Freeze']
guarda(51, dict(
    kind='grafica',
    titulo='Le mandamos promociones a quien no puede comprar con KPay y a quien pidió no recibir publicidad',
    que=f'Promociones: descuentos y cupones ({M(F["tema"]["Descuento, cupón u oferta"])} M), referidos ({M(F["tema"]["Referidos"])} M), lanzamientos ({M(F["tema"]["Lanzamiento y novedades"])} M) y Tasa 0 ({M(F["tema"]["Tasa 0"])} M). Ofrecen KPay: Comercio del día, Hot Sale, promociones de comercios, referidos KPay y recomendaciones semanales.',
    quien=f'A KPay congelado: Marketing {M(F["eq"]["Marketing"])} M, Sales {M(F["eq"]["Sales"])} M, Product Growth {M(F["eq"]["Product Growth"])} M y Others (BillPay de NewProducts, Shopping y QA) {M(F["eq"]["Others"])} M. A REUS o ARCO, sobre todo Product Growth y Shopping.',
    a_quien=f'{mil(u["u"])} mil personas con la línea KPay congelada, que recibieron {u["m"]/u["u"]:.0f} mensajes cada una en nueve meses; {mil(E3["6.Reus or Arco"]["u"])} mil que pidieron no recibir publicidad (REUS o ARCO) y {mil(E3["3.Blacklist"]["u"])} mil en lista negra.',
    lecturas=[
        f'{M(F["promo"])} M promociones fueron a personas que no pueden comprar con KPay, y {M(F["prod"]["kpay"])} M ofrecen justo KPay. Otras {M(F["prod"]["kcash"])} M ofrecen KCash: si proceden lo decide Riesgo, porque {100*u["c"]/u["u"]:.0f} % de estas personas sí convirtió.',
        f'REUS o ARCO es la petición formal de no recibir publicidad. Aun así llegaron {mil(RE["promo"])} mil promociones, {mil(RE["canal"]["whatsapp"])} mil por WhatsApp, y {mil(NE["promo"])} mil a lista negra. Cada una es una queja posible ante Condusef.',
        f'Se arregla con exclusiones de cuenta en Braze que se cargan una vez: quitan {M(ex_min)} M promociones (KPay a congelados, REUS, ARCO y lista negra) sin tocar ninguna campaña; {M(ex_all)} M si se excluye toda promoción a congelados.',
    ],
    causa='No hay exclusiones de cuenta en Braze para bloqueados: cada equipo arma su segmento con su propia lista y nadie revisa que salga quien no puede comprar o pidió no recibir publicidad.',
    sowhat='Excluir de una vez: línea KPay congelada de toda promoción de KPay, y REUS, ARCO y lista negra de toda promoción. Riesgo decide sobre KCash.',
    fuente=f'Fuente: Braze E7a (campaña, canal y etapa del golden dataset) y E3 (personas por etapa), enero a septiembre 2026. Promocional según el catálogo de campañas; tema por el nombre. La etapa cubre 37 % de los envíos: las cifras son un piso. El WhatsApp a bloqueados ({M(F["canal"]["whatsapp"])} M enviados a congelados) se cobra solo si se entregó. Personas en REUS o ARCO: {mil(E3["6.Reus or Arco"]["u"])} mil en E3; el guion decía 104 mil.',
    svg=SVG,
))
print(round(ex_min / 1e6, 2), round(ex_all / 1e6, 2), {e: round(F['eq'][e] / 1e6, 2) for e in EQS})
