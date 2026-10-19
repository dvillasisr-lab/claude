"""Lámina 10: tabla semáforo por canal contra el mínimo de la industria (Estándares del Sheets v4, METRICAS) y lo que ganaríamos al llegar.
Regla de tres sobre los totales de E1; bajas en personas con E4a."""
import pandas as pd
from comun import load, write, ROOT, BLUE, GREEN, SEC, INK, FUENTE_E1

d = load()
s = d[['email_sent', 'email_delivery', 'email_open', 'email_click', 'email_unsubscribe', 'pn_send', 'pn_open', 'whatsapp_send',
       'whatsapp_delivery', 'whatsapp_read', 'in_app_impression', 'in_app_click']].sum()
r = dict(e_ent=100 * s.email_delivery / s.email_sent, e_ab=100 * s.email_open / s.email_delivery, e_clic=1000 * s.email_click / s.email_delivery,
         e_baja=1000 * s.email_unsubscribe / s.email_delivery, p_ab=1000 * s.pn_open / s.pn_send, w_ent=100 * s.whatsapp_delivery / s.whatsapp_send,
         w_lec=100 * s.whatsapp_read / s.whatsapp_delivery, i_clic=100 * s.in_app_click / s.in_app_impression)
# Ganancias al llegar al mínimo
clic_mas = s.email_delivery * 0.015 - s.email_click
email_menos = s.email_sent * (1 - (s.email_click / s.email_delivery) / 0.015)
push_mas = s.pn_send * 0.03 - s.pn_open
push_menos = s.pn_send * (1 - (s.pn_open / s.pn_send) / 0.03)
wa_env_menos = s.whatsapp_send - s.whatsapp_delivery / 0.90
wa_mxn_75 = (s.whatsapp_delivery - s.whatsapp_read / 0.75) * 1.0
e4 = pd.read_csv(ROOT / 'data/e4a_serie_semana_mes_canal.csv'); e4 = e4[(e4.grano == 'mes') & (e4.canal == 'email')]
bu = e4.bajas_email_usuarios.sum(); bajas_menos = bu * (1 - 2.5 / r['e_baja'])
resp_mas = clic_mas + push_mas
print({k: round(v, 2) for k, v in r.items()}, clic_mas / 1e6, email_menos / 1e6, push_mas / 1e6, push_menos / 1e6, push_menos / s.pn_send, wa_env_menos / 1e6, wa_mxn_75 / 1e6, bu, bajas_menos, resp_mas / 1e6)

EST = {'Lejos': (BLUE, 700), 'Cerca': (SEC, 600), 'Cumple': (GREEN, 600)}
def est(e):
    c, w = EST[e]
    return f'<span style="color:{c};font-weight:{w}">&#9679; {e}</span>'
def tr(canal, ind, hoy, mini, e, gana):
    b = ' style="font-weight:600"' if e == 'Lejos' else ''
    return f'<tr><td>{canal}</td><td{b}>{ind}</td><td class="num"{b}>{hoy}</td><td class="num">{mini}</td><td>{est(e)}</td><td>{gana}</td></tr>'
M = lambda v: f'{v / 1e6:.1f} M'
html = (
    '<table style="table-layout:fixed">'
    '<tr><th style="width:8%">Canal</th><th style="width:22%">Indicador</th><th class="num" style="width:9%">Kueski hoy</th><th class="num" style="width:11%">Mínimo de la industria</th>'
    '<th style="width:9%">Estado</th><th style="width:41%">Qué ganaríamos al llegar al mínimo</th></tr>'
    + tr('Correo', 'Clics por cada mil correos entregados', f'{r["e_clic"]:.1f} por mil', '15 por mil', 'Lejos',
         f'<b>{M(clic_mas)} clics más</b> con los mismos correos, o los mismos clics con {email_menos / 1e6:.0f} M correos menos ({email_menos * 0.05 / 1e6:.1f} M MXN en nueve meses, {email_menos * 0.05 / 9e6:.1f} M MXN al mes).')
    + tr('Push', 'Aperturas por cada mil push', f'{r["p_ab"]:.1f} por mil', '30 por mil', 'Lejos',
         f'<b>{M(push_mas)} aperturas más</b> con los mismos push, o las mismas con {push_menos / 1e6:.0f} M push menos (la mitad).')
    + tr('WhatsApp', 'Entregados de cada 100 enviados', f'{r["w_ent"]:.1f} %', '90 %', 'Lejos',
         f'{wa_env_menos / 1e6:.1f} M envíos menos a números que no reciben. No ahorra dinero, porque solo se paga lo entregado.')
    + tr('Correo', 'Bajas por cada mil correos entregados', f'{r["e_baja"]:.1f} por mil', '2.5 por mil como máximo', 'Lejos',
         f'Unas {bajas_menos / 1e3:.0f} mil personas menos dadas de baja del correo en nueve meses.')
    + tr('WhatsApp', 'Leídos de cada 100 entregados', f'{r["w_lec"]:.1f} %', '70 %', 'Cerca',
         f'A 75 % (nuestra meta), las mismas lecturas con {wa_mxn_75 / 1e6:.1f} M MXN menos en nueve meses.')
    + tr('Correo', 'Entregados de cada 100 enviados', f'{r["e_ent"]:.1f} %', '95 %', 'Cumple', '')
    + tr('Correo', 'Abiertos de cada 100 entregados', f'{r["e_ab"]:.1f} %', '15 %', 'Cumple', f'<span style="color:{SEC}">Inflada por aperturas automáticas de algunos correos: no decidir con ella.</span>')
    + tr('In-app', 'Clics de cada 100 vistas', f'{r["i_clic"]:.1f} %', '5 %', 'Cumple', f'<span style="color:{SEC}">El canal que más responde y no cuesta.</span>')
    + '</table>'
    f'<div style="margin-top:.9cqi;font-size:1.05cqi;color:{INK}"><b>Correo y push al mínimo: {resp_mas / 1e6:.1f} M respuestas más con los mismos mensajes.</b> '
    f'<span style="color:{SEC}">Cuántas ventas serían no se puede decir sin un grupo que no reciba mensajes.</span></div>')

write(10, dict(kind='html', ancho_completo=True,
    titulo=f'Si correo y push respondieran lo mínimo de la industria, tendríamos {resp_mas / 1e6:.1f} M respuestas más con los mismos mensajes',
    que='Todo lo que sale por cada canal; la distancia al mínimo viene casi toda de las promociones.',
    quien='Todos los equipos; más adelante se ve qué equipo está más lejos en cada canal.',
    a_quien=f'Toda la base: 19.5 M personas.',
    html=html,
    sowhat='Hay margen grande sin gastar más: está en a quién y qué mandamos, no en mandar más.',
    fuente=(f'{FUENTE_E1} (E1); bajas en personas por mes de E4a. Mínimo de la industria = valor más bajo del rango público (METRICAS, Estándares del Sheets v4): clic de correo 1.5 a 3 %, push 3 a 10 %, '
            'WhatsApp lectura 70 a 90 % y entrega mayor a 90 %, in-app 5 a 20 %; bajas 2.5 por mil es estándar propuesto. Regla de tres sobre los totales del canal; WhatsApp a 1.00 MXN por entregado, correo a 0.05 MXN por enviado.')))
