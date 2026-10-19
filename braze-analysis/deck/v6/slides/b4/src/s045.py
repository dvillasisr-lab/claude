"""Lámina 45: WhatsApp por día de la semana y equipo (E10). Mapa de calor de lectura sobre entregados con envíos por día arriba."""
import pandas as pd
from kit import *
e = pd.read_csv(D + 'e10_dia_semana.csv'); e['T'] = e.team.map(team); w = e[e.canal == 'whatsapp']
O = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']; DL = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
def tab(g):
    d = g.groupby('dia_semana')[['envios', 'wa_entregados', 'respuestas', 'comunicaciones']].sum().reindex(O).fillna(0)
    d['ent'] = 100 * d.wa_entregados / d.envios; d['lec'] = 100 * d.respuestas / d.wa_entregados; d['k'] = d.envios / d.comunicaciones
    return d
T = {'Todos los equipos': tab(w)}
for t in ['Marketing', 'Product Growth', 'Sales']: T[t] = tab(w[w['T'] == t])
tot = w.envios.sum(); vt = w.groupby('T').envios.sum()
al = T['Todos los equipos']; dom_sh = 100 * al.loc['Sunday', 'envios'] / tot
print({k: v[['ent', 'lec']].round(1).to_dict() for k, v in T.items()}, dom_sh, (vt / 1e6).round(1).to_dict(), tot / 1e6, al.k.round(0).to_dict())
S = Svg('Mapa de calor: lectura de WhatsApp sobre entregados por día de la semana y equipo, con envíos por día en barras arriba; celdas arriba de 100 % en gris')
LX, CW, Y0 = 150, 86, 40
S.t(0, 14, 'WhatsApp enviados por día de la semana, millones (9 meses)', 11.5, INK, w=600)
mx = al.envios.max() / 1e6
for j, dd in enumerate(O):
    v = al.loc[dd, 'envios'] / 1e6; h = 70 * v / mx; x = LX + CW * j
    S.rect(x + CW * 0.25, Y0 + 80 - h, CW * 0.5, h, BLUE if dd == 'Sunday' else G1)
    S.t(x + CW / 2, Y0 + 80 - h - 5, f'{v:.1f} M', 10.5, INK, 'middle', 700 if dd == 'Sunday' else 400)
    S.t(x + CW / 2, Y0 + 96, DL[j], 11.5, INK, 'middle', 700 if dd in ('Monday', 'Sunday') else 400)
S.line(LX, Y0 + 82, LX + CW * 7, Y0 + 82, SEC)
S.t(0, Y0 + 124, 'Lectura sobre entregados; abajo, entrega sobre enviados', 11.5, INK, w=600)
RY, RH = Y0 + 136, 52
for i, (t, d) in enumerate(T.items()):
    y = RY + RH * i
    S.t(LX - 10, y + RH / 2 + 4, t, 11.5, INK, 'end', 700 if i == 0 else 400)
    for j, dd in enumerate(O):
        x = LX + CW * j; lec, ent = d.loc[dd, 'lec'], d.loc[dd, 'ent']
        if lec > 100:
            S.rect(x + 1, y + 1, CW - 2, RH - 2, '#F0F2F5')
            S.t(x + CW / 2, y + 23, f'{lec:.0f} %', 13, SEC, 'middle', 700); S.t(x + CW / 2, y + 39, 'imposible', 10.5, SEC, 'middle')
            continue
        op = max(0.08, min(0.95, (lec - 55) / 40))
        S.raw(f'<rect x="{x+1:.1f}" y="{y+1:.1f}" width="{CW-2:.1f}" height="{RH-2:.1f}" fill="{GREEN}" fill-opacity="{op:.2f}"/>')
        col = '#FFFFFF' if op > 0.55 else INK
        S.t(x + CW / 2, y + 23, f'{lec:.0f} %', 13, col, 'middle', 700)
        S.t(x + CW / 2, y + 39, f'entrega {ent:.0f} %', 10.5, col, 'middle')
S.t(LX, RY + RH * 4 + 18, 'Color más intenso, más lectura. Gris: más de 100 %, porque el día suma lecturas de mensajes de días anteriores.', 10.5, SEC)

write(45, dict(kind='grafica', seccion='V. El ritmo lo marcan los lanzamientos, no el cliente',
 titulo=f'WhatsApp parece leerse mejor en domingo, pero con {dom_sh:.0f} % de los envíos no alcanza para mover el calendario',
 que='WhatsApp promocional: Tasa 0, referidos, churn, inactivos y Hot Sale.',
 quien=f'Marketing {100*vt["Marketing"]/tot:.0f} % del WhatsApp ({vt["Marketing"]/1e6:.1f} M), Product Growth {100*vt["Product Growth"]/tot:.0f} % ({vt["Product Growth"]/1e6:.1f} M) y Sales {100*vt["Sales"]/tot:.0f} % ({vt["Sales"]/1e6:.1f} M) de {tot/1e6:.1f} M.',
 a_quien='Leads rezagados, churn, inactivos y recurrentes.',
 lecturas=[
  f'Domingo: {al.loc["Sunday","ent"]:.0f} % de entrega y {al.loc["Sunday","lec"]:.0f} % de lectura contra {al.loc["Monday","ent"]:.0f} % y {al.loc["Monday","lec"]:.0f} % el lunes, pero solo {al.loc["Sunday","envios"]/1e6:.1f} M de {tot/1e6:.0f} M WhatsApp. Cada campaña del domingo llega a unas {al.loc["Sunday","k"]/1e3:.1f} mil personas contra {al.loc["Monday","k"]/1e3:.0f} mil el lunes.',
  f'Por equipo se repite: Product Growth en domingo {T["Product Growth"].loc["Sunday","lec"]:.0f} % de lectura contra {T["Product Growth"].loc["Monday","lec"]:.0f} % el lunes; Marketing {T["Marketing"].loc["Sunday","lec"]:.0f} % contra {T["Marketing"].loc["Monday","lec"]:.0f} %.',
  f'Sales marca {T["Sales"].loc["Sunday","lec"]:.0f} % de lectura el domingo: imposible si solo contara lo enviado ese día. La lectura se registra el día en que ocurre y el domingo suma mensajes del viernes y el sábado.',
 ],
 causa='El domingo son envíos chicos y de seguimiento, y su tasa se infla con lecturas de otros días. No sabemos si pasa todos los meses ni en qué campañas: E10 no trae mes ni campaña.',
 sowhat='Antes de mover WhatsApp al fin de semana hay que probarlo: la misma campaña en domingo y en martes, con un grupo sin mensajes para comparar.',
 fuente='Fuente: Braze, E10 (WhatsApp por día de la semana y equipo, enero a septiembre 2026). Lectura sobre entregados y entrega sobre enviados, por fecha del evento. WhatsApp se cobra a 1.00 MXN por entregado. Extracción que lo resuelve: E10 con mes, campaña y lectura atribuida al día del envío.',
 svg=S.svg()))
