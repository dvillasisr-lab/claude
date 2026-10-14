# Asigna a cada familia × canal una acción concreta ("qué hacer") y su justificación ("por qué").
# Todo sale de datos: señal de respuesta y bajas (muestra C), toques por usuario y tamaño (E1), conversión de quienes abren
# contra quienes no abren (E7c), etapa del usuario (E7a) y emails después de la baja (E5b). El nombre de la campaña no se usa
# para decidir; solo "tipo" (cobranza = equipo Collections; transaccional = sin ticket en el nombre) viene del catálogo.
# Entrada: hallazgos/muestra_c_familias.csv, data/e1_comunicacion_mes_canal.csv y, si existen, data/e7c_abren_vs_no_abren.csv,
#          data/e7a_familia_canal_etapa.csv y data/e5b_comms_despues_baja.csv.
# Salida: el mismo CSV con accion_tipo, accion, por_que, toques_usuario_mes, usuarios_por_envio, otros_canales,
#         conv_abren_pct, conv_no_abren_pct, lift, lift_muestra, pct_prospectos, emails_a_dados_de_baja, envios_etapa_bloqueada;
#         y el JSON para la página de campañas si se pasa una ruta como segundo argumento.
# Uso: python3 -I scripts/acciones_campanas.py hallazgos/muestra_c_familias.csv [salida.json]
import sys, os, json, math
import pandas as pd

MIN = {'email': 0.3, 'push notification': 0.75, 'whatsapp': 60.0, 'in-app': 10.0, 'banner': 10.0}
MED = {'email': 0.50, 'push notification': 1.07, 'whatsapp': 64.49, 'in-app': 18.24, 'banner': 18.24}
LABEL = {'email': 'clic', 'push notification': 'apertura', 'whatsapp': 'lectura', 'in-app': 'clic', 'banner': 'clic'}
CANAL = {'email': 'email', 'push notification': 'push', 'whatsapp': 'WhatsApp', 'in-app': 'in-app', 'banner': 'banner'}
VERBO = {'email': 'abren', 'push notification': 'abren', 'whatsapp': 'leen', 'in-app': 'ven', 'banner': 'ven'}
GEN = [
    'toques_usuario_mes', 'usuarios_por_envio', 'otros_canales', 'accion_tipo', 'accion', 'por_que', 'emails_a_dados_de_baja',
    'envios_etapa_bloqueada', 'conv_abren_pct', 'conv_no_abren_pct', 'lift', 'lift_muestra', 'pct_prospectos',
]

def isnan(v):
    return v is None or (isinstance(v, float) and math.isnan(v))

def fmt_m(v):
    if isnan(v): return ''
    if v >= 1e6: return f'{v/1e6:.1f} M'.replace('.0 M', ' M')
    if v >= 1e3: return f'{v/1e3:.0f} mil'
    return f'{v:.0f}'

def fmt_p(v, d=2):
    return '' if isnan(v) else f'{v:.{d}f} %'

def colapsa(s):
    return s.str.replace(r'-\d{8}-', '-', regex=True)

def main(path, out_json=None):
    d = pd.read_csv(path)
    d['familia'] = d.familia.fillna('(sin nombre)')
    d = d.drop(columns=[c for c in GEN if c in d.columns])

    # E1: toques por usuario al mes y tamaño de audiencia por envío
    e1 = pd.read_csv('data/e1_comunicacion_mes_canal.csv')
    e1['familia'] = colapsa(e1.communication_name)
    act = e1[e1.envios > 0].groupby(['familia', 'canal']).agg(env=('envios', 'sum'), usr=('usuarios_aprox', 'sum'),
                                                              usr_mes=('usuarios_aprox', 'mean')).reset_index()
    act['toques_usuario_mes'] = (act.env / act.usr.where(act.usr > 0)).round(2)
    act['usuarios_por_envio'] = act.usr_mes.round(0)
    d = d.merge(act[['familia', 'canal', 'toques_usuario_mes', 'usuarios_por_envio']], on=['familia', 'canal'], how='left')

    # otros canales de la misma familia que sí responden (alternativa para no perder el contacto)
    alt = {}
    for fam, g in d.groupby('familia'):
        alt[fam] = {r.canal: r.respuesta_pct for r in g.itertuples() if r.envios >= 1000}
    def alternativa(fam, canal):
        outs = []
        for c, resp in alt.get(fam, {}).items():
            if c == canal or isnan(resp): continue
            if resp >= MIN.get(c, 0) and c in ('push notification', 'in-app', 'email'):
                outs.append(f'{CANAL[c]} ({LABEL[c]} {fmt_p(resp, 1 if c=="in-app" else 2)})')
        return ', '.join(outs)
    d['otros_canales'] = [alternativa(f, c) for f, c in zip(d.familia, d.canal)]

    # E7c: convierten los que abren vs los que no abren (7 días). Muestra suficiente: 1,000 de cada lado y 100 conversiones.
    d['conv_abren_pct'] = float('nan'); d['conv_no_abren_pct'] = float('nan'); d['lift'] = float('nan'); d['lift_muestra'] = 0
    med_conv = {}
    if os.path.exists('data/e7c_abren_vs_no_abren.csv'):
        k = pd.read_csv('data/e7c_abren_vs_no_abren.csv')
        k['familia'] = colapsa(k.familia)
        k = k.groupby(['familia', 'canal'], as_index=False)[['envios_usuario_dia', 'abrieron', 'abrieron_y_convirtieron', 'no_abrieron_y_convirtieron']].sum()
        k['no_abrieron'] = k.envios_usuario_dia - k.abrieron
        k['conv_abren_pct'] = (k.abrieron_y_convirtieron / k.abrieron.where(k.abrieron > 0) * 100).round(2)
        k['conv_no_abren_pct'] = (k.no_abrieron_y_convirtieron / k.no_abrieron.where(k.no_abrieron > 0) * 100).round(2)
        k['lift'] = (k.conv_abren_pct / k.conv_no_abren_pct.where(k.conv_no_abren_pct > 0)).round(2)
        k['lift_muestra'] = ((k.abrieron >= 1000) & (k.no_abrieron >= 1000) & ((k.abrieron_y_convirtieron + k.no_abrieron_y_convirtieron) >= 100)).astype(int)
        med_conv = k[k.lift_muestra == 1].groupby('canal').conv_abren_pct.median().to_dict()
        d = d.drop(columns=['conv_abren_pct', 'conv_no_abren_pct', 'lift', 'lift_muestra']).merge(
            k[['familia', 'canal', 'conv_abren_pct', 'conv_no_abren_pct', 'lift', 'lift_muestra']], on=['familia', 'canal'], how='left')
        d['lift_muestra'] = d.lift_muestra.fillna(0).astype(int)

    # E5b: emails que llegaron a usuarios ya dados de baja (solo email).
    # E7a: envíos a etapas que no deberían recibir promoción, y qué parte de los envíos con etapa conocida va a prospectos sin crédito.
    d['emails_a_dados_de_baja'] = 0.0; d['envios_etapa_bloqueada'] = 0.0; d['pct_prospectos'] = float('nan')
    if os.path.exists('data/e5b_comms_despues_baja.csv'):
        b = pd.read_csv('data/e5b_comms_despues_baja.csv')
        b['familia'] = colapsa(b.familia)
        b = b.groupby('familia').emails_despues_de_baja.sum()
        m = d.canal.eq('email')
        d.loc[m, 'emails_a_dados_de_baja'] = d.loc[m, 'familia'].map(b).fillna(0).values
    if os.path.exists('data/e7a_familia_canal_etapa.csv'):
        e7 = pd.read_csv('data/e7a_familia_canal_etapa.csv')
        e7['familia'] = colapsa(e7.familia)
        blo = e7[e7.etapa.isin(['3.Blacklist', '4.Kpay CC Freeze', '6.Reus or Arco'])].groupby(['familia', 'canal']).envios.sum()
        d['envios_etapa_bloqueada'] = [blo.get((f, c), 0) for f, c in zip(d.familia, d.canal)]
        p = e7.pivot_table(index=['familia', 'canal'], columns='etapa', values='envios', aggfunc='sum', fill_value=0)
        conocida = p.sum(axis=1) - p.get('sin_golden', 0)
        pct_con = conocida / p.sum(axis=1).where(p.sum(axis=1) > 0) * 100
        pct_pro = p.get('7.Prospects', 0) / conocida.where(conocida > 0) * 100
        pct_pro = pct_pro.where(pct_con >= 20)  # solo si al menos 20 % de los envíos tiene etapa conocida
        d['pct_prospectos'] = [pct_pro.get((f, c), float('nan')) for f, c in zip(d.familia, d.canal)]
        d['pct_prospectos'] = d.pct_prospectos.round(0)

    tipos, acciones, porques = [], [], []
    for r in d.itertuples():
        canal, lab = r.canal, LABEL.get(r.canal, 'respuesta')
        dec = 1 if canal in ('whatsapp', 'in-app') else 2
        resp = r.respuesta_pct
        resp_txt = f'{lab} {fmt_p(resp, dec)}'
        env_mes = fmt_m(r.envios_mes_prom)
        costo_mes = r.costo_mxn / r.meses if r.meses else 0
        toques = r.toques_usuario_mes
        toques_txt = f', {toques:.1f} mensajes por usuario al mes' if toques and toques >= 1.5 else ''
        noent = r.wa_no_entregado_mxn if canal == 'whatsapp' and r.wa_no_entregado_mxn else 0
        noent_txt = f' Se pagaron {fmt_m(noent)} MXN de mensajes que no se entregaron.' if noent >= 1000 else ''
        altc = r.otros_canales
        tam = r.usuarios_por_envio
        tam_txt = f' Audiencia de {fmt_m(tam)} usuarios por envío; arriba de 1 M el clic de email cae 5 veces.' if canal == 'email' and tam and tam >= 1e6 else ''
        activo = r.activo_sep == 1
        senal = r.senal if isinstance(r.senal, str) else ''
        motivo = r.motivo if isinstance(r.motivo, str) else ''
        # E7c: qué dice la conversión de quienes abren
        muestra = r.lift_muestra == 1 and not isnan(r.conv_abren_pct) and not isnan(r.lift)
        medc = med_conv.get(canal)
        conv_txt = ''
        if muestra:
            conv_txt = f' Quienes lo {VERBO[canal]} convierten {fmt_p(r.conv_abren_pct)} y quienes no {fmt_p(r.conv_no_abren_pct)} ({r.lift:.1f} veces)'
            conv_txt += f'; lo normal en {CANAL[canal]} es {fmt_p(medc, 1)} entre quienes {VERBO[canal]}.' if medc else '.'
        # ¿el mensaje mueve a quien lo abre? Sí = quienes abren convierten al menos la mitad de lo normal del canal y abrir cambia la conversión (lift 1.5+)
        if muestra and medc:
            mueve = r.conv_abren_pct >= medc / 2 and r.lift >= 1.5
            mueve_por = f' Ni quien lo {VERBO[canal][:-1]} convierte: no hay a quién acotar la base.' if r.conv_abren_pct < medc / 2 else (f' {"Leerlo" if canal == "whatsapp" else "Abrirlo"} casi no cambia la conversión: el mensaje no está moviendo nada.' if r.lift < 1.5 else '')
        else:
            mueve = not (isnan(resp) or resp < MIN[canal] / 2)
            mueve_por = '' if mueve else f' Ni la mitad del mínimo, y sin muestra de conversión que lo rescate.'
        pros_txt = f' El {r.pct_prospectos:.0f} % de sus envíos con etapa conocida va a prospectos sin crédito (E7a).' if not isnan(r.pct_prospectos) and r.pct_prospectos >= 60 else ''

        if r.tipo == 'cobranza':
            t, a, p = 'No tocar', 'Fuera de la optimización promocional: es cobranza.', 'Su resultado es el pago, no la respuesta al mensaje.' + noent_txt
        elif r.tipo == 'transaccional u operativa':
            t, a, p = 'No tocar', 'No apagar: es transaccional u operativa.', 'Debe llegar aunque la respuesta sea baja. Solo revisar que no incluya usuarios dados de baja (sale en E5b).' + noent_txt
        elif senal == 'apagar o rehacer' and not activo:
            t = 'Confirmar apagado'
            a = f'Confirmar que esté archivada; último envío en {r.ultimo_mes}.'
            p = f'{resp_txt.capitalize()} debajo del mínimo ({fmt_p(MIN[canal], dec)}). Ya no envía, pero si se reactiva aplicar lo mismo que a las activas.' + conv_txt
        elif senal == 'apagar o rehacer':
            if canal == 'whatsapp':
                base = f'{resp_txt.capitalize()} con mínimo 60 %, entrega {fmt_p(r.entrega_pct, 1)}. Cuesta {fmt_m(costo_mes)} MXN al mes.'
                if not mueve:
                    t = 'Apagar'
                    a = 'Apagar el WhatsApp de esta familia' + (f'; mantener el contacto por {altc}.' if altc else '; si hace falta tocar a esta base, usar push o in-app, que no cuestan.')
                    p = base + conv_txt + mueve_por + pros_txt + noent_txt + f' Ahorro: {fmt_m(r.ahorro_mxn_mes)} MXN al mes.'
                else:
                    t = 'Limpiar base de WhatsApp'
                    a = 'Limpiar la base (quitar números sin entrega) y enviar solo a quien leyó cualquier WhatsApp de Kueski en los últimos 90 días, no solo de esta campaña.'
                    p = base + conv_txt + ' Quien lo lee sí convierte: el problema es la base, no el mensaje.' + pros_txt + noent_txt
            elif canal == 'email':
                base = f'{resp_txt.capitalize()} con mínimo 0.3 %, {env_mes} envíos al mes{toques_txt}.'
                if not mueve:
                    t = 'Apagar'
                    a = 'Apagar el email de esta familia' + (f'; dejar solo {altc}.' if altc else '; si hace falta tocar a esta base, usar push o in-app.')
                    p = base + conv_txt + mueve_por + pros_txt + f' Ahorro: {fmt_m(r.ahorro_mxn_mes)} MXN al mes.'
                else:
                    t = 'Rehacer o re-segmentar'
                    a = 'Re-segmentar: solo quienes abrieron cualquier email de Kueski en los últimos 90 días (no solo de esta campaña), máximo 2 al mes.'
                    p = base + conv_txt + ' Quien lo abre sí convierte: el problema es a quién y cuántas veces se manda.' + pros_txt + tam_txt
            elif canal == 'push notification':
                base = f'{resp_txt.capitalize()} con mínimo 0.75 %, {env_mes} envíos al mes{toques_txt}.'
                if not mueve:
                    t = 'Apagar'
                    a = 'Apagar el push de esta familia' + (f'; dejar {altc}.' if altc else '; dejar in-app si existe.')
                    p = base + conv_txt + mueve_por + pros_txt + ' No cuesta, pero gasta el permiso de push y suma fatiga: los usuarios más contactados generan 16 bajas por cada 100.'
                else:
                    t = 'Rehacer o re-segmentar'
                    a = 'Re-segmentar: solo usuarios que abrieron cualquier push de Kueski en los últimos 60 días (no solo de esta campaña), máximo 2 al mes.'
                    p = base + conv_txt + ' Quien lo abre sí convierte: el problema es a quién y cuántas veces se manda.' + pros_txt
            else:
                base = f'{resp_txt.capitalize()} con mínimo 10 %, {env_mes} impresiones al mes.'
                if not mueve:
                    t = 'Apagar'
                    a = 'Quitar la pieza de la pantalla.'
                    p = base + ' Ni la mitad del mínimo. No cuesta, pero ocupa la pantalla y le quita lugar a piezas que sí funcionan (in-app bien hecho da 18 % de clic).'
                else:
                    t = 'Rehacer o re-segmentar'
                    a = 'Rehacer la creatividad o cambiar la pantalla donde aparece.'
                    p = base + ' In-app bien hecho da 18 % de clic (mediana).' + (f' Quienes lo ven convierten {fmt_p(r.conv_abren_pct)}.' if not isnan(r.conv_abren_pct) else '')
        elif senal == 'revisar':
            bajas = 'bajas' in motivo; baja_resp = 'respuesta' in motivo
            if bajas and baja_resp:
                t = 'Bajar frecuencia'
                a = 'Bajar a 2 emails al mes, excluir a quien no abrió ninguno de los últimos 3 envíos de esta campaña y probar otro asunto.'
                p = f'{r.bajas_por_mil:.1f} bajas por mil (umbral 2.5) y clic {fmt_p(r.clic_pct)} debajo de la mediana 0.5 %{toques_txt}. Molesta y no mueve.' + conv_txt + tam_txt
            elif bajas:
                t = 'Bajar frecuencia'
                a = 'Mantener el contenido, bajar a 2 emails al mes y excluir a quien no abrió ninguno de los últimos 3 envíos de esta campaña.'
                p = f'Clic {fmt_p(r.clic_pct)} está bien (mediana 0.5 %) pero genera {r.bajas_por_mil:.1f} bajas por mil (umbral 2.5){toques_txt}. El mensaje funciona, la presión molesta.' + conv_txt
            elif canal == 'whatsapp':
                t = 'Limpiar base de WhatsApp'
                a = 'Limpiar la base (números sin entrega, y solo quien leyó algún WhatsApp de Kueski en 90 días) y probar la misma pieza en push antes de seguir pagando.'
                p = f'{resp_txt.capitalize()} debajo de la mediana 64.5 %, entrega {fmt_p(r.entrega_pct, 1)}, {fmt_m(costo_mes)} MXN al mes.' + conv_txt + noent_txt
            elif canal == 'email':
                t = 'Rehacer o re-segmentar'
                a = 'Probar otro gancho o asunto y acotar a quienes abrieron algún email de Kueski en 90 días.'
                p = f'{resp_txt.capitalize()} debajo de la mediana 0.5 %, {env_mes} envíos al mes{toques_txt}.' + conv_txt + tam_txt
            elif canal == 'push notification':
                t = 'Rehacer o re-segmentar'
                a = 'Probar copy y horario; acotar a quienes abrieron algún push de Kueski en 60 días.'
                p = f'{resp_txt.capitalize()} debajo de la mediana 1.07 %, {env_mes} envíos al mes{toques_txt}.' + conv_txt
            else:
                t = 'Rehacer o re-segmentar'
                a = 'Probar otra creatividad o ubicación.'
                p = f'{resp_txt.capitalize()} debajo de la mediana 18.2 %, {env_mes} impresiones al mes.'
        elif senal == 'proteger':
            t = 'Proteger'
            a = 'No tocar. Protegerla del solapamiento: que otras campañas no le lleguen el mismo día.'
            p = f'{resp_txt.capitalize()}, {resp/MED[canal]:.1f} veces la mediana del canal, con {env_mes} envíos al mes.' + conv_txt
        elif senal == 'escalar':
            t = 'Escalar'
            a = ('Reactivar y ' if not activo else '') + 'ampliar la audiencia por pasos: duplicar y medir cada mes.'
            p = f'{resp_txt.capitalize()}, {resp/MED[canal]:.1f} veces la mediana del canal, con solo {env_mes} envíos al mes.' + conv_txt
        else:
            if activo and toques and toques >= 4.5 and canal in ('email', 'push notification'):
                t = 'Bajar frecuencia'
                a = 'Bajar a 2 mensajes por usuario al mes.'
                p = f'{toques:.1f} mensajes por usuario al mes con respuesta normal ({resp_txt}). Con 3 o más toques el clic de email cae a 0.48 %.'
            elif activo and canal == 'whatsapp' and noent >= 10000:
                t = 'Limpiar base de WhatsApp'
                a = 'Limpiar números sin entrega antes del siguiente envío.'
                p = f'Entrega {fmt_p(r.entrega_pct, 1)}.' + noent_txt
            elif activo and canal == 'email' and tam and tam >= 1e6:
                t = 'Rehacer o re-segmentar'
                a = 'Dividir la audiencia en segmentos y mandar a cada uno su mensaje.'
                p = tam_txt.strip() + f' Hoy {resp_txt}.' + conv_txt
            else:
                t = 'Seguir igual'
                a = 'Sin cambio; seguir midiendo.'
                p = (f'Respuesta en rango o volumen bajo ({resp_txt}).' if not isnan(resp) else 'Sin respuesta medible en el periodo.') + conv_txt
        if r.tipo == 'promocional o lifecycle':
            if r.emails_a_dados_de_baja >= 500:
                p += f' Además llegaron {fmt_m(r.emails_a_dados_de_baja)} emails a usuarios que ya se habían dado de baja: revisar el filtro de suscripción del Canvas.'
            if r.envios_etapa_bloqueada >= 10000:
                p += f' {fmt_m(r.envios_etapa_bloqueada)} envíos fueron a usuarios en REUS o ARCO, lista negra o con tarjeta congelada: excluirlos del segmento.'
        tipos.append(t); acciones.append(a); porques.append(p)

    d['accion_tipo'], d['accion'], d['por_que'] = tipos, acciones, porques
    # cobranza y transaccional no se apagan: su ahorro no cuenta
    nt = d.accion_tipo == 'No tocar'
    d.loc[nt, ['ahorro_mxn_periodo', 'ahorro_mxn_mes', 'msgs_mes_ahorrados']] = 0
    d.to_csv(path, index=False)
    if out_json:
        recs = d.to_dict(orient='records')
        for rec in recs:
            for k2, v in rec.items():
                if isinstance(v, float) and math.isnan(v): rec[k2] = None
            if rec['senal'] is None: rec['senal'] = ''
            if rec['motivo'] is None: rec['motivo'] = ''
        with open(out_json, 'w') as f: json.dump(recs, f, ensure_ascii=False)
    print('medianas conv. de quienes abren:', {k2: round(v, 2) for k2, v in med_conv.items()})
    print(d.accion_tipo.value_counts().to_string())

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
