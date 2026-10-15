"""Construye braze_auditoria_v2.xlsx: todo lo de v1 más Catálogo, Campañas, Medianas y una pestaña de cálculo por lente.
Uso: python3 scripts/build_sheets_v2.py [--lo-test]   (desde braze-analysis/)
--lo-test escribe como valores las columnas que usan REGEX (familia, audiencia, gancho, ticket) para poder recalcular
el archivo con LibreOffice 24.2, que no tiene esas funciones. El archivo que se entrega se genera SIN la bandera.
Las fórmulas usan sintaxis de Google Sheets; el archivo se abre con Google Sheets, no con Excel.
"""
import pandas as pd, numpy as np, hashlib, re, os, sys
from openpyxl import Workbook
from openpyxl.utils import get_column_letter as L
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.styles import Font, Alignment

LO_TEST = '--lo-test' in sys.argv
D = 'data/'
VERSION = 'v3'
OUT = f'sheets/braze_auditoria_{VERSION}_lo_test.xlsx' if LO_TEST else f'sheets/braze_auditoria_{VERSION}.xlsx'
HOY = '14 de octubre de 2026'

TABS = [
 ('E1',  'e1_comunicacion_mes_canal.csv',   'Volumen por comunicación × mes × canal: envíos, entregas, aperturas, clics, bajas, conversiones. Es la base del análisis por campaña.', 'comunicación × mes × canal (deduplicado por usuario × comunicación × día)', 'communication_id'),
 ('E2',  'e2_catalogo.csv',                 'Catálogo de piezas de Braze (campañas y canvas): nombre, equipo, producto, ticket, canales, fechas de primer y último envío, estado.', 'una fila por communication_id', 'communication_id'),
 ('E3',  'e3_usuarios_distribucion.csv',    'Distribución de usuarios por banda de mensajes recibidos en el periodo, suscripción, etapa y contactabilidad.', 'banda × suscripción × etapa (usuarios agregados)', 'banda_msgs'),
 ('E4a', 'e4a_serie_semana_mes_canal.csv',  'Serie de tiempo por canal con dos granos: semana y mes. Toda fórmula debe filtrar la columna grano.', 'grano × periodo × canal', 'grano'),
 ('E4b', 'e4b_concentracion_mes.csv',       'Concentración: cuántos usuarios recibieron cuántos mensajes cada mes (bandas).', 'mes × banda de mensajes', 'mes'),
 ('E5',  'e5_cohorte_baja.csv',             'Cohorte de usuarios dados de baja por mes y qué recibieron después de la baja (meses 1, 2, 3 y total).', 'mes de baja', 'mes_baja'),
 ('E5b', 'e5b_comms_despues_baja.csv',      'Familias que siguieron mandando email a usuarios ya dados de baja.', 'familia (con fecha; ver familia derivada)', 'familia'),
 ('E6a', 'e6a_solape_dia_mes.csv',          'Solapamiento: cuántas familias distintas recibe un usuario el mismo día, por mes.', 'mes × banda de familias por día', 'mes'),
 ('E6b', 'e6b_pares_familias.csv',          'Pares de familias que llegan al mismo usuario el mismo día (top 1,000 por LIMIT en la query).', 'par de familias (con fecha; ver derivadas)', 'familia_a'),
 ('E7a', 'e7a_familia_canal_etapa.csv',     'Envíos por familia × canal × etapa del usuario (golden record: Blacklist, CC Freeze, Reus/Arco, Prospects, sin_golden).', 'familia (con fecha) × canal × etapa', 'canal'),
 ('E7b', 'e7b_patron_respuesta.csv',        'Patrón de respuesta por usuario en todo el periodo: 16 combinaciones de respondió o no por canal, con mensajes recibidos, conversiones y bajas.', '16 combinaciones de respuesta (usuarios agregados)', 'usuarios'),
 ('E7c', 'e7c_abren_vs_no_abren.csv',       'Por familia y canal: usuarios que abrieron o no, y cuántos convirtieron en cada grupo (todo el periodo).', 'familia (con fecha) × canal', 'canal'),
 ('E8',  'e8_dias_hasta_baja.csv',          'Días y emails desde el primer email hasta la baja. Bloques: resumen, banda_dias, banda_emails y familia_dia_baja (familia enviada el día de la baja). cohorte_limpia 1 = primer email dentro del periodo; 0 = ya recibía antes de enero.', 'bloque × clave × cohorte', 'bloque'),
 ('E9a', 'e9a_abren_vs_no_abren_ventanas.csv', 'Como E7c pero con ventanas de conversión a 7, 30, 90 días y fin de periodo. La familia ya viene sin fecha.', 'familia × canal', 'canal'),
 ('E9b', 'e9b_patron_respuesta_90d.csv',    'Como E7b pero solo julio a septiembre 2026 (último trimestre).', '16 combinaciones de respuesta (usuarios agregados)', 'usuarios'),
]
TEXT_COLS = {'communication_id','ticket_number','banda_msgs','banda_msgs_mes','banda_familias_dia','clave','fecha_codigo','grupo','mes','periodo','mes_baja','first_sent','last_sent','created_at','tipo_pieza','nombre','familia','familia_a','familia_b'}
NUM_RE = re.compile(r'^-?\d+(\.\d+)?$')
CANALES = ['email', 'push notification', 'whatsapp', 'in-app', 'banner']
C4 = CANALES[:4]
MESES = [f'2026-0{m}' for m in range(1, 10)]
ETAPAS = ['3.Blacklist', '4.Kpay CC Freeze', '6.Reus or Arco', '7.Prospects', 'sin_golden']
BLOQUEADAS = ETAPAS[:3]
TIPOS = ['promocional o lifecycle', 'transaccional u operativa', 'cobranza']
EQUIPOS = ['Marketing', 'Product Growth', 'Sales', 'Collections', 'Others']
SENALES = ['apagar o rehacer', 'revisar', 'proteger', 'escalar']
ACCIONES = ['Apagar', 'Limpiar base de WhatsApp', 'Rehacer o re-segmentar', 'Bajar frecuencia', 'Confirmar apagado', 'Proteger', 'Escalar', 'No tocar', 'Seguir igual']
AUD = [('cobranza', r'(^Collections|cobranza|BKT)'), ('transaccional', r'(^Transaccional|payment|Contracts|disbursed)'),
       ('fríos: dormants, inactivos, rezagados, never active', r'(Dormant|Inactiv|Churn|Rezagad|Never)'),
       ('leads y registrados sin crédito', r'(Leads|Anonim|Anónim|Registrad)'), ('nuevos y onboarding', r'(Nuevos|Onboarding|1er|1ra|Welcome)'),
       ('clientes activos y recurrentes', r'(Recurrente|Active|Activo|Cliente)')]
GAN = [('tasa 0', r'(Tasa0|Tasa 0)'), ('descuento, cupón u oferta', r'(Descuento|Cupon|Cupón|Oferta)'), ('referidos', r'(Referral|AnotayGana)'),
       ('retargeting o recordatorio', r'(Retargeting|Rescate|Recordatorio|Reminder)'), ('lanzamiento, novedades, newsletter', r'(Lanzamiento|Intro|Newsletter|Recommendations)'),
       ('cross sell', r'(XSell|Cross)')]
AUDS = [a for a, _ in AUD] + ['otros']; GANS = [g for g, _ in GAN] + ['otros']
TAM = ['menos de 10 mil', '10 a 100 mil', '100 mil a 1 M', '1 M+']; TOQ = ['1', '2', '3 a 4', '5+']
TICKET_RE = r'-[A-Z]?[BTS]0?\d{3,5}-'

def md5(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()
def read(path): return pd.read_csv(path, dtype=str, keep_default_na=False)
def fam_pd(s): return s.str.replace(r'-\d{8}-', '-', regex=True).replace({'null': '(sin nombre)', '': '(sin nombre)'})
def clasif(name, rules):
    for lab, rx in rules:
        if re.search(rx, name, re.I): return lab
    return 'otros'
def nested_if(ref, rules, default):
    """IF anidado con REGEXMATCH(ref, patrón) en el orden de rules."""
    s = f'"{default}"'
    for lab, rx in reversed(rules):
        s = f'IF(REGEXMATCH({ref},"(?i){rx}"),"{lab}",{s})'
    return s

wb = Workbook(); wb.remove(wb.active)
bold = Font(bold=True); wrap = Alignment(wrap_text=True, vertical='top')
INFO = {}; E = {}

def typed(series, name):
    vals = series.tolist(); nulls = 0; out = []
    nonnull = [v for v in vals if v not in ('', 'null')]
    numeric = name not in TEXT_COLS and len(nonnull) > 0 and all(NUM_RE.match(v) for v in nonnull)
    allint = numeric and all('.' not in v for v in nonnull)
    for v in vals:
        if v == 'null': nulls += 1; out.append(None)
        elif v == '': out.append(None)
        elif numeric: out.append(int(v) if allint else float(v))
        else: out.append(v)
    return out, nulls

def write_raw(tab, fname):
    df = read(D + fname); E[tab] = df
    ws = wb.create_sheet(tab)
    cols = list(df.columns); letters = {}; nulls = {}; data_cols = []
    for j, c in enumerate(cols, start=1):
        ws.cell(1, j, c).font = bold; letters[c] = L(j)
        vals, n = typed(df[c], c); data_cols.append(vals); nulls[c] = n
    for i in range(len(df)):
        for j, vals in enumerate(data_cols, start=1):
            if vals[i] is not None: ws.cell(i + 2, j, vals[i])
    ws.freeze_panes = 'A2'
    INFO[tab] = dict(filas=len(df), md5=md5(D + fname), cols=cols, letters=letters, nulls=nulls, derived=[], archivo=fname, ws=ws)

def add_derived(tab, hdr, fn, values=None):
    """Agrega una columna derivada; fn(r, letters) devuelve la fórmula. values: lista para --lo-test (sustituye la fórmula)."""
    i = INFO[tab]; ws = i['ws']; j = len(i['cols']) + len(i['derived']) + 1
    ws.cell(1, j, hdr).font = bold; i['letters'][hdr] = L(j); i['derived'].append(hdr)
    for r in range(2, i['filas'] + 2):
        v = values[r - 2] if (LO_TEST and values is not None) else fn(r, i['letters'])
        if v is not None and v != '': ws.cell(r, j, v)

def finish_raw(tab):
    i = INFO[tab]; ws = i['ws']; last = L(len(i['cols']) + len(i['derived']))
    ws.auto_filter.ref = f'A1:{last}{i["filas"] + 1}'
    for j in range(1, len(i['cols']) + len(i['derived']) + 1): ws.column_dimensions[L(j)].width = 14

def rng(tab, col):
    i = INFO[tab]; return f"{tab}!${i['letters'][col]}$2:${i['letters'][col]}${i['filas'] + 1}"
def cell(tab, col, r): return f"{tab}!${INFO[tab]['letters'][col]}{r}"
def num(tab, col): return pd.to_numeric(E[tab][col].replace({'null': None, '': None}), errors='coerce')
def S(tab, col): return float(num(tab, col).sum())

# ---------- pestañas en orden final
leeme = wb.create_sheet('Léeme'); par = wb.create_sheet('Parámetros')
for tab, fname, *_ in TABS: write_raw(tab, fname)
CALC = ['Catálogo', 'Campañas', 'Medianas', 'B_Canales', 'E_DespuesBaja', 'F_Solape', 'G_Practicas', 'H_Etapas', 'J_Canal', 'K_Abren', 'L_Baja', 'M_Ventanas']
NEW = ['Vista_equipo', 'Insights', 'Plan_accion', 'Estándares']
WS = {n: wb.create_sheet(n) for n in CALC + NEW}
ver = wb.create_sheet('Verificación')

# ---------- pandas base
e1 = E['E1']
e1name = e1.communication_name.replace('null', '')
e1f_raw = fam_pd(e1name)
e1mes = e1.mes.str[:7]; e1env = num('E1', 'envios'); e1usr = num('E1', 'usuarios_aprox')
# Familias que solo cambian en mayúsculas/minúsculas (p. ej. "...-in-App" y "...-in-app") son la misma familia:
# SUMIFS, COUNTIF y VLOOKUP de Sheets no distinguen mayúsculas, así que la réplica pandas tampoco debe hacerlo.
# CANON: minúsculas -> nombre representativo (la variante con más envíos en E1; si no está en E1, la primera vista).
def _build_canon():
    m = {}
    g_ = pd.DataFrame(dict(f=e1f_raw, e=e1env)).groupby('f').e.sum().sort_values(ascending=False)
    for f in g_.index: m.setdefault(f.lower(), f)
    for s_ in [fam_pd(E['E2'].nombre), fam_pd(E['E5b'].familia), fam_pd(E['E6b'].familia_a), fam_pd(E['E6b'].familia_b),
               fam_pd(E['E7a'].familia), fam_pd(E['E7c'].familia), fam_pd(E['E9a'].familia), fam_pd(E['E8'].clave)]:
        for f in s_.unique(): m.setdefault(f.lower(), f)
    return m
CANON = _build_canon()
def canon(s_): return s_.str.lower().map(CANON).fillna(s_)
e1f = canon(e1f_raw)
CASE_PAIRS = int(e1f_raw.nunique() - e1f.nunique())  # familias de E1 que se juntan por mayúsculas/minúsculas (8)
e1aud = e1name.map(lambda s: clasif(s, AUD)); e1gan = e1name.map(lambda s: clasif(s, GAN))
e1tam = pd.cut(e1usr, [-1, 9999.999, 99999.999, 999999.999, 1e18], labels=TAM).astype(str)
ratio = e1env / e1usr.where(e1usr > 0)
e1toq = pd.Series(np.where(e1usr > 0, pd.cut(ratio, [-1, 1.4999999, 2.4999999, 4.4999999, 1e18], labels=TOQ).astype(str), ''), index=e1.index)

# ---------- Parámetros
P = [
 ('parámetro', 'valor', 'unidad', 'nota'),
 ('Costo por email enviado', 0.05, 'MXN por email_sent', 'Dato del usuario. Aplica a todo email enviado.'),
 ('Costo por WhatsApp', 1.00, 'MXN por mensaje', 'Dato del usuario. Se multiplica por entregados o por enviados según la fila 6.'),
 ('Costo por push', 0, 'MXN por pn_send', 'Sin costo variable.'),
 ('Costo por in-app', 0, 'MXN por in_app_impression', 'Sin costo variable.'),
 ('Base de cobro WhatsApp', 'entregado', 'entregado | enviado', 'Meta cobra por mensaje entregado (default). Cambia a "enviado" para ver el escenario que se usó en las muestras anteriores. Toda fórmula de costo lee esta celda.'),
 ('Costo fijo Braze por mes', None, 'MXN', 'PENDIENTE del usuario: significado de $7,020/mes y 32,474 créditos. Vacío hasta tenerlo; ninguna fórmula lo suma mientras esté vacío.'),
 ('Usuarios con email en el periodo', 20137560, 'usuarios', 'Denominador de la tasa de baja (E5, línea de denominador). Count distinct aproximado.'),
 ('Periodo inicio', '2026-01-01', 'fecha', 'Rango de event_date en todas las queries.'),
 ('Periodo fin', '2026-09-30', 'fecha', ''),
 ('Mínimo de respuesta email (clic / entregado)', 0.003, 'proporción', 'Debajo de esto la campaña "no tiene señal" en email. Editable: Campañas y Verificación se recalculan.'),
 ('Mínimo de respuesta push (apertura / enviado)', 0.0075, 'proporción', 'Editable.'),
 ('Mínimo de respuesta WhatsApp (lectura / entregado)', 0.60, 'proporción', 'Editable.'),
 ('Mínimo de respuesta in-app (clic / impresión)', 0.10, 'proporción', 'Editable.'),
 ('Fracción del mínimo para marcar "sin señal"', 0.5, 'proporción', 'Regla de acción: respuesta menor a (mínimo × esta fracción) = no mueve, se apaga en vez de rehacer.'),
 ('Lift mínimo (convierten los que abren / los que no abren)', 1.5, 'veces', 'Regla "mueve": conv de los que abren ≥ mitad de la mediana del canal y lift ≥ este valor.'),
 ('Muestra mínima: usuarios que abrieron', 1000, 'usuarios', 'Debajo no se juzga la campaña por conversión.'),
 ('Muestra mínima: usuarios que no abrieron', 1000, 'usuarios', ''),
 ('Muestra mínima: conversiones', 100, 'conversiones', ''),
 ('In-app: clic debajo del cual se quita la pieza', 0.05, 'proporción', 'Informativo en v2 (la regla de in-app usa el mínimo de la fila 14 y la fracción de la fila 15, igual que los demás canales).'),
 ('Definición de respuesta: email', 'clic (email_click)', 'texto', 'No se usa la apertura de email porque Apple y Gmail abren automáticamente.'),
 ('Definición de respuesta: push', 'apertura (pn_open)', 'texto', ''),
 ('Definición de respuesta: WhatsApp', 'lectura (whatsapp_read)', 'texto', ''),
 ('Definición de respuesta: in-app', 'clic (in_app_click)', 'texto', ''),
 ('Definición de baja', 'email_unsubscribe = true', 'texto', 'Solo baja de email. Usuario-mes (E4a) = un usuario cuenta cada mes que se da de baja; usuarios únicos (E5, E7b) = una vez en el periodo.'),
 # 26+ nuevos en v2
 ('Bajas por mil entregados para marcar "revisar" (email)', 2.5, 'bajas por mil', 'Señal revisar con motivo "bajas altas" si la familia llega o pasa este valor.'),
 ('Factor sobre la mediana para "proteger"', 1.5, 'veces', 'Volumen alto y respuesta ≥ mediana del canal × este factor.'),
 ('Factor sobre la mediana para "escalar"', 2, 'veces', 'Volumen bajo (pero ≥ fila 29) y respuesta ≥ mediana × este factor.'),
 ('Envíos mínimos para "escalar"', 1000, 'envíos', ''),
 ('Toques por usuario al mes para "bajar frecuencia"', 4.5, 'mensajes', 'Familias activas sin señal, email y push: envíos / usuarios_aprox ≥ este valor.'),
 ('Audiencia por envío para "re-segmentar" email', 1000000, 'usuarios', 'Email activo sin señal con usuarios_aprox promedio ≥ este valor.'),
 ('WhatsApp no entregado (MXN) para "limpiar base"', 10000, 'MXN', 'WhatsApp activo sin señal con (enviados − entregados) × costo ≥ este valor.'),
 ('Emails a dados de baja para marcar la familia (E5b)', 500, 'emails', 'Informativo en Campañas (columna emails_a_dados_de_baja).'),
 ('Envíos a etapa bloqueada para marcar la familia (E7a)', 10000, 'envíos', 'Informativo en Campañas (columna envios_etapa_bloqueada).'),
 ('Etapa conocida mínima para calcular % prospectos', 0.20, 'proporción', 'Solo se calcula pct_prospectos si al menos esta parte de los envíos tiene etapa distinta de sin_golden.'),
 ('% prospectos para señalarlo', 0.60, 'proporción', 'Informativo.'),
 ('Días del periodo', 273, 'días', '1 de enero a 30 de septiembre de 2026.'),
]
for i, row in enumerate(P, start=1):
    for j, v in enumerate(row, start=1):
        c = par.cell(i, j, v)
        if i == 1: c.font = bold
for r in (11, 12, 13, 14, 15, 20, 35, 36): par.cell(r, 2).number_format = '0.00%'
par.cell(2, 2).number_format = '0.00'; par.cell(3, 2).number_format = '0.00'
dv = DataValidation(type='list', formula1='"entregado,enviado"', allow_blank=False); par.add_data_validation(dv); dv.add('B6')
# tabla de equipos (editable)
MAP_ROW = len(P) + 3
par.cell(MAP_ROW - 1, 1, 'Mapeo de equipos (editable). Columna A: equipo como viene en E1 (team). Columna B: equipo para la vista por equipo. Todo lo que no esté aquí cae en Others.').font = bold
par.cell(MAP_ROW, 1, 'equipo en E1').font = bold; par.cell(MAP_ROW, 2, 'equipo para la vista').font = bold; par.cell(MAP_ROW, 3, 'filas en E1').font = bold
teams = e1.team.value_counts()
MAP = {t: (t if t in EQUIPOS else 'Others') for t in teams.index}
for k, (t, n) in enumerate(teams.items()):
    par.cell(MAP_ROW + 1 + k, 1, t); par.cell(MAP_ROW + 1 + k, 2, MAP[t]); par.cell(MAP_ROW + 1 + k, 3, f'=COUNTIF({rng("E1","team")},A{MAP_ROW + 1 + k})')
MAP_RNG = f'Parámetros!$A${MAP_ROW + 1}:$B${MAP_ROW + len(teams)}'
par.column_dimensions['A'].width = 56; par.column_dimensions['B'].width = 18; par.column_dimensions['C'].width = 26; par.column_dimensions['D'].width = 110
par.freeze_panes = 'A2'
PB = {k: f'Parámetros!$B${r}' for k, r in dict(costo_email=2, costo_wa=3, costo_push=4, costo_inapp=5, base_wa=6, usuarios_email=8,
      inapp_quitar=20, min_email=11, min_push=12, min_wa=13, min_inapp=14, frac=15, lift=16, m_ab=17, m_noab=18, m_conv=19,
      bajas_mil=26, f_prot=27, f_esc=28, env_esc=29, toques=30, aud=31, wa_noent=32, e5b=33, e7a=34, etapa_min=35, pros=36, dias=37).items()}
e1equipo = e1.team.map(MAP)

# ---------- derivadas en pestañas crudas
def fam_formula(l, namecol, idcol=None):
    if idcol:
        pass  # el id ya no forma parte del nombre: hay una sola comunicación sin nombre y así cruza igual en todas las pestañas
    return lambda r, l=l: f'=IF({l[namecol]}{r}="","(sin nombre)",REGEXREPLACE({l[namecol]}{r},"-\\d{{8}}-","-"))'

add_derived('E1', 'familia (derivada)', fam_formula(None, 'communication_name', 'communication_id'), e1f_raw.tolist())
add_derived('E1', 'mes_clave (derivada)', lambda r, l: f'=LEFT({l["mes"]}{r},7)')
add_derived('E1', 'mes_num (derivada)', lambda r, l: f'=VALUE(RIGHT({l["mes_clave (derivada)"]}{r},2))')
add_derived('E1', 'equipo (derivada)', lambda r, l: f'=IFERROR(VLOOKUP({l["team"]}{r},{MAP_RNG},2,FALSE),"Others")')
add_derived('E1', 'audiencia (derivada)', lambda r, l: '=' + nested_if(f'{l["communication_name"]}{r}', AUD, 'otros'), e1aud.tolist())
add_derived('E1', 'gancho (derivada)', lambda r, l: '=' + nested_if(f'{l["communication_name"]}{r}', GAN, 'otros'), e1gan.tolist())
add_derived('E1', 'banda_tamaño (derivada)', lambda r, l: f'=IF({l["usuarios_aprox"]}{r}<10000,"{TAM[0]}",IF({l["usuarios_aprox"]}{r}<100000,"{TAM[1]}",IF({l["usuarios_aprox"]}{r}<1000000,"{TAM[2]}","{TAM[3]}")))')
add_derived('E1', 'banda_toques (derivada)', lambda r, l: f'=IF({l["usuarios_aprox"]}{r}<=0,"",IF({l["envios"]}{r}/{l["usuarios_aprox"]}{r}<1.5,"1",IF({l["envios"]}{r}/{l["usuarios_aprox"]}{r}<2.5,"2",IF({l["envios"]}{r}/{l["usuarios_aprox"]}{r}<4.5,"3 a 4","5+"))))')
# tipo en E1 se agrega después de definir el Catálogo (VLOOKUP)
add_derived('E2', 'familia (derivada)', fam_formula(None, 'nombre'), fam_pd(E['E2'].nombre).tolist())
add_derived('E4a', 'mes_clave (derivada)', lambda r, l: f'=LEFT({l["periodo"]}{r},7)')
add_derived('E4b', 'mes_clave (derivada)', lambda r, l: f'=LEFT({l["mes"]}{r},7)')
add_derived('E6a', 'mes_clave (derivada)', lambda r, l: f'=LEFT({l["mes"]}{r},7)')
add_derived('E5b', 'familia (derivada)', fam_formula(None, 'familia'), fam_pd(E['E5b'].familia).tolist())
add_derived('E6b', 'familia_a (derivada)', fam_formula(None, 'familia_a'), fam_pd(E['E6b'].familia_a).tolist())
add_derived('E6b', 'familia_b (derivada)', fam_formula(None, 'familia_b'), fam_pd(E['E6b'].familia_b).tolist())
add_derived('E7a', 'familia (derivada)', fam_formula(None, 'familia'), fam_pd(E['E7a'].familia).tolist())
add_derived('E7c', 'familia (derivada)', fam_formula(None, 'familia'), fam_pd(E['E7c'].familia).tolist())
add_derived('E9a', 'familia (derivada)', fam_formula(None, 'familia'), fam_pd(E['E9a'].familia).tolist())
add_derived('E8', 'familia (derivada)', lambda r, l: f'=IF({l["bloque"]}{r}="familia_dia_baja",IF({l["clave"]}{r}="","(sin nombre)",{l["clave"]}{r}),"")')

# ---------- Catálogo (una fila por familia de E1)
FAMS = sorted(e1f.unique())
cat = WS['Catálogo']; NC = len(FAMS)
CAT_COLS = ['familia', 'ticket', 'communication_ids', 'versiones (ids)', 'equipo_original (E1 team)', 'equipo', 'producto', 'canales con envíos', 'tipo', 'audiencia (por nombre)', 'gancho (por nombre)',
            'primer_mes', 'ultimo_mes', 'activa_sep', 'meses con envíos', 'envíos', 'costo_mxn', 'está en E2', 'acciones (de Campañas)']
CL = {c: L(j) for j, c in enumerate(CAT_COLS, start=1)}
INFO['Catálogo'] = dict(filas=NC, letters=CL, cols=CAT_COLS)
for j, c in enumerate(CAT_COLS, start=1): cat.cell(1, j, c).font = bold
def cat_rng(col): return rng('Catálogo', col)
def cat_lookup(ref, col): return f'IFERROR(VLOOKUP({ref},Catálogo!$A$2:${CL[CAT_COLS[-1]]}${NC + 1},{CAT_COLS.index(col) + 1},FALSE),"no está en E1")'
l1 = INFO['E1']['letters']
def e1r(col): return rng('E1', col)
FAM1 = e1r('familia (derivada)'); CAN1 = e1r('canal'); ENV1 = e1r('envios'); MESN1 = e1r('mes_num (derivada)')
def costo_sumifs(crit):
    """Costo con base de cobro seleccionada; crit = texto de criterios SUMIFS (rango,criterio,...)."""
    return (f'SUMIFS({e1r("email_sent")},{crit})*{PB["costo_email"]}+IF({PB["base_wa"]}="entregado",SUMIFS({e1r("whatsapp_delivery")},{crit}),SUMIFS({e1r("whatsapp_send")},{crit}))*{PB["costo_wa"]}'
            f'+SUMIFS({e1r("pn_send")},{crit})*{PB["costo_push"]}+SUMIFS({e1r("in_app_impression")},{crit})*{PB["costo_inapp"]}')

# pandas réplica del Catálogo
g1 = pd.DataFrame(dict(fam=e1f, team=e1.team, prod=e1.product_service, ticket=e1.ticket_number, canal=e1.canal, mes=e1mes, env=e1env, usr=e1usr,
                       es=num('E1','email_sent'), ed=num('E1','email_delivery'), eo=num('E1','email_open'), ec=num('E1','email_click'), eu=num('E1','email_unsubscribe'),
                       ps=num('E1','pn_send'), po=num('E1','pn_open'), ws=num('E1','whatsapp_send'), wd=num('E1','whatsapp_delivery'), wr=num('E1','whatsapp_read'),
                       ii=num('E1','in_app_impression'), ic=num('E1','in_app_click'), bi=num('E1','banner_impression'), bc=num('E1','banner_click'), cf=num('E1','conversiones_fraccional'),
                       aud=e1aud, gan=e1gan, cid=e1.communication_id))
first = g1.groupby('fam', sort=True).first()
def ticket_of(fam):
    t = first.loc[fam, 'ticket']
    if t == 'null': t = ''
    if t != 'Other': return t
    m = re.search(r'-([A-Z]?[BTS]0?\d{3,5})-', fam); return m.group(1) if m else ''
catp = pd.DataFrame(index=FAMS)
catp['ticket'] = [ticket_of(f) for f in FAMS]
catp['team'] = first.team; catp['equipo'] = catp.team.map(MAP); catp['prod'] = first['prod']
catp['tipo'] = ['cobranza' if t == 'Collections' else ('transaccional u operativa' if (f.startswith('Transaccional') or not re.search(TICKET_RE, f)) else 'promocional o lifecycle') for f, t in zip(FAMS, catp.team)]
act = g1[g1.env > 0]
catp['meses'] = act.groupby('fam').mes.nunique().reindex(FAMS).fillna(0)
catp['ultimo'] = act.groupby('fam').mes.max().reindex(FAMS); catp['activa'] = (catp.ultimo == '2026-09').astype(int)
catp['env'] = g1.groupby('fam').env.sum().reindex(FAMS)
catp['en_e2'] = pd.Series(FAMS).isin(set(canon(fam_pd(E['E2'].nombre)))).values
TIPO_F = lambda eq, fam: f'IF({eq}="Collections","cobranza",IF(OR(LEFT({fam},13)="Transaccional",NOT(REGEXMATCH({fam},"{TICKET_RE}"))),"transaccional u operativa","promocional o lifecycle"))'
for i, f in enumerate(FAMS):
    r = i + 2; A = f'$A{r}'
    crit = f'{FAM1},{A}'
    row = {
     'familia': f,
     'ticket': (catp.ticket.iloc[i] if LO_TEST else f'=IFERROR(IF(INDEX({e1r("ticket_number")},MATCH({A},{FAM1},0))<>"Other",INDEX({e1r("ticket_number")},MATCH({A},{FAM1},0)),REGEXEXTRACT({A},"-([A-Z]?[BTS]0?\\d{{3,5}})-")),"")'),
     'communication_ids': f'=IFERROR(TEXTJOIN(", ",TRUE,UNIQUE(FILTER({e1r("communication_id")},{FAM1}={A}))),"")',
     'versiones (ids)': f'=IFERROR(COUNTA(UNIQUE(FILTER({e1r("communication_id")},{FAM1}={A}))),0)',
     'equipo_original (E1 team)': f'=INDEX({e1r("team")},MATCH({A},{FAM1},0))',
     'equipo': f'=IFERROR(VLOOKUP({CL["equipo_original (E1 team)"]}{r},{MAP_RNG},2,FALSE),"Others")',
     'producto': f'=INDEX({e1r("product_service")},MATCH({A},{FAM1},0))',
     'canales con envíos': f'=IFERROR(TEXTJOIN(", ",TRUE,UNIQUE(FILTER({CAN1},{FAM1}={A},{ENV1}>0))),"")',
     'tipo': (catp.tipo.iloc[i] if LO_TEST else '=' + TIPO_F(f'{CL["equipo_original (E1 team)"]}{r}', A)),
     'audiencia (por nombre)': f'=INDEX({e1r("audiencia (derivada)")},MATCH({A},{FAM1},0))',
     'gancho (por nombre)': f'=INDEX({e1r("gancho (derivada)")},MATCH({A},{FAM1},0))',
     'primer_mes': f'=IF({CL["meses con envíos"]}{r}=0,"","2026-"&TEXT(MINIFS({MESN1},{FAM1},{A},{ENV1},">0"),"00"))',
     'ultimo_mes': f'=IF({CL["meses con envíos"]}{r}=0,"","2026-"&TEXT(MAXIFS({MESN1},{FAM1},{A},{ENV1},">0"),"00"))',
     'activa_sep': f'=IF({CL["ultimo_mes"]}{r}="2026-09",1,0)',
     'meses con envíos': '=' + '+'.join(f'(COUNTIFS({FAM1},{A},{ENV1},">0",{MESN1},{m})>0)' for m in range(1, 10)),
     'envíos': f'=SUMIFS({ENV1},{crit})',
     'costo_mxn': '=' + costo_sumifs(crit),
     'está en E2': f'=IF(COUNTIF({rng("E2","familia (derivada)")},{A})>0,"sí","no")',
     'acciones (de Campañas)': None,  # se llena después de definir Campañas
    }
    for c in CAT_COLS:
        v = row[c]
        if v is not None: cat.cell(r, CAT_COLS.index(c) + 1, v)
cat.freeze_panes = 'B2'; cat.auto_filter.ref = f'A1:{CL[CAT_COLS[-1]]}{NC + 1}'
for c in CAT_COLS: cat.column_dimensions[CL[c]].width = 60 if c == 'familia' else (40 if c in ('communication_ids', 'acciones (de Campañas)', 'canales con envíos') else 14)
# tipo en E1 (lookup al Catálogo)
add_derived('E1', 'tipo (derivada)', lambda r, l: f'=IFERROR(VLOOKUP({l["familia (derivada)"]}{r},Catálogo!$A$2:${CL["tipo"]}${NC + 1},{CAT_COLS.index("tipo") + 1},FALSE),"")')
for t, col in [('E5b', 'familia (derivada)'), ('E7a', 'familia (derivada)'), ('E8', 'familia (derivada)')]:
    add_derived(t, 'equipo (derivada)', lambda r, l, col=col: f'=IF({l[col]}{r}="","",{cat_lookup(f"{l[col]}{r}", "equipo")})')
    add_derived(t, 'tipo (derivada)', lambda r, l, col=col: f'=IF({l[col]}{r}="","",{cat_lookup(f"{l[col]}{r}", "tipo")})')
for s in 'ab':
    add_derived('E6b', f'equipo_{s} (derivada)', lambda r, l, s=s: '=' + cat_lookup(f'{l[f"familia_{s} (derivada)"]}{r}', 'equipo'))
    add_derived('E6b', f'tipo_{s} (derivada)', lambda r, l, s=s: '=' + cat_lookup(f'{l[f"familia_{s} (derivada)"]}{r}', 'tipo'))
add_derived('E6b', 'par_equipos (derivada)', lambda r, l: f'=IF({l["equipo_a (derivada)"]}{r}<={l["equipo_b (derivada)"]}{r},{l["equipo_a (derivada)"]}{r}&" + "&{l["equipo_b (derivada)"]}{r},{l["equipo_b (derivada)"]}{r}&" + "&{l["equipo_a (derivada)"]}{r})')
add_derived('E6b', 'ambas promocionales (derivada)', lambda r, l: f'=IF(AND({l["tipo_a (derivada)"]}{r}="promocional o lifecycle",{l["tipo_b (derivada)"]}{r}="promocional o lifecycle"),1,0)')
for tab, *_ in TABS: finish_raw(tab)

# =====================================================================================
# ---------- Campañas: una fila por familia × canal con envíos > 0
# =====================================================================================
RAW = ['es', 'ed', 'eo', 'ec', 'eu', 'ps', 'po', 'ws', 'wd', 'wr', 'ii', 'ic', 'bi', 'bc', 'cf']
RAWCOL = dict(es='email_sent', ed='email_delivery', eo='email_open', ec='email_click', eu='email_unsubscribe', ps='pn_send', po='pn_open', ws='whatsapp_send', wd='whatsapp_delivery', wr='whatsapp_read', ii='in_app_impression', ic='in_app_click', bi='banner_impression', bc='banner_click', cf='conversiones_fraccional')
kact = act.groupby(['fam', 'canal']).agg(env=('env', 'sum'), usr=('usr', 'sum'), usr_mean=('usr', 'mean'), meses=('mes', 'nunique'), primer=('mes', 'min'), ultimo=('mes', 'max'), versiones=('cid', 'nunique'))
camp = kact.join(g1.groupby(['fam', 'canal'])[RAW].sum()).reset_index()
camp['env'] = g1.groupby(['fam', 'canal']).env.sum().reindex(pd.MultiIndex.from_frame(camp[['fam', 'canal']])).values  # igual, pero sobre todas las filas
camp = camp.sort_values(['env', 'fam', 'canal'], ascending=[False, True, True]).reset_index(drop=True)
camp['tipo'] = camp.fam.map(catp.tipo); camp['equipo'] = camp.fam.map(catp.equipo); camp['ticket'] = camp.fam.map(catp.ticket)
camp['activo'] = (camp.ultimo == '2026-09').astype(int)
camp['env_mes'] = camp.env / camp.meses
camp['toques'] = camp.env / camp.usr.where(camp.usr > 0)
def div(a, b): return a / b.where(b > 0)
c = camp.canal
camp['resp'] = np.select([c == 'email', c == 'push notification', c == 'whatsapp', c == 'in-app'], [div(camp.ec, camp.ed), div(camp.po, camp.ps), div(camp.wr, camp.wd), div(camp.ic, camp.ii)], np.nan)
camp['entrega'] = np.select([c == 'email', c == 'whatsapp'], [div(camp.ed, camp.es), div(camp.wd, camp.ws)], np.nan)
camp['bajas_mil'] = np.where(c == 'email', div(camp.eu, camp.ed) * 1000, np.nan)
camp['costo_ent'] = camp.es * 0.05 + camp.wd * 1.0; camp['costo_env'] = camp.es * 0.05 + camp.ws * 1.0
camp['wa_noent'] = np.where(c == 'whatsapp', camp.ws - camp.wd, 0.0)
MINP = {'email': 0.003, 'push notification': 0.0075, 'whatsapp': 0.60, 'in-app': 0.10}
camp['minimo'] = c.map(MINP)
med_env = camp.groupby('canal').env.median(); med_resp = camp.groupby('canal').resp.median()
camp['med_env'] = c.map(med_env); camp['med_resp'] = c.map(med_resp)
camp['vol'] = np.where(camp.env >= camp.med_env, 'alto', 'bajo')
def senal(r):
    if pd.isna(r.resp): return ''
    alto = r.vol == 'alto'
    if alto and r.resp < r.minimo: return 'apagar o rehacer'
    if alto and (r.resp < r.med_resp or (not pd.isna(r.bajas_mil) and r.bajas_mil >= 2.5)): return 'revisar'
    if alto and r.resp >= 1.5 * r.med_resp: return 'proteger'
    if (not alto) and r.env >= 1000 and r.resp >= 2 * r.med_resp: return 'escalar'
    return ''
camp['senal'] = camp.apply(senal, axis=1)
def motivo(r):
    if r.senal == 'apagar o rehacer': return 'respuesta debajo del mínimo'
    if r.senal == 'revisar':
        hb = (not pd.isna(r.bajas_mil)) and r.bajas_mil >= 2.5
        if hb and r.resp < r.med_resp: return 'respuesta baja y bajas altas'
        return 'bajas altas' if hb else 'respuesta baja'
    return {'proteger': 'respuesta alta con volumen', 'escalar': 'respuesta alta sin volumen'}.get(r.senal, '')
camp['motivo'] = camp.apply(motivo, axis=1)
# E7c
e7c = E['E7c']; k7 = pd.DataFrame(dict(fam=canon(fam_pd(e7c.familia)), canal=e7c.canal, eud=num('E7c', 'envios_usuario_dia'), ab=num('E7c', 'abrieron'), abc=num('E7c', 'abrieron_y_convirtieron'), nabc=num('E7c', 'no_abrieron_y_convirtieron'))).groupby(['fam', 'canal']).sum()
camp = camp.merge(k7, left_on=['fam', 'canal'], right_index=True, how='left').fillna({'eud': 0, 'ab': 0, 'abc': 0, 'nabc': 0})
camp['noab'] = camp.eud - camp.ab
camp['conv_ab'] = div(camp.abc, camp.ab); camp['conv_noab'] = div(camp.nabc, camp.noab); camp['lift'] = div(camp.conv_ab, camp.conv_noab)
camp['muestra'] = ((camp.ab >= 1000) & (camp.noab >= 1000) & (camp.abc + camp.nabc >= 100)).astype(int)
med_conv = camp[camp.muestra == 1].groupby('canal').conv_ab.median(); camp['med_conv'] = c.map(med_conv)
def mueve(r):
    if r.muestra == 1 and not pd.isna(r.conv_ab) and not pd.isna(r.lift) and not pd.isna(r.med_conv):
        return int(r.conv_ab >= r.med_conv / 2 and r.lift >= 1.5)
    return int((not pd.isna(r.resp)) and (not pd.isna(r.minimo)) and r.resp >= r.minimo * 0.5)
camp['mueve'] = camp.apply(mueve, axis=1)
# E5b, E7a
e5b = E['E5b']; b5 = pd.DataFrame(dict(fam=canon(fam_pd(e5b.familia)), em=num('E5b', 'emails_despues_de_baja'))).groupby('fam').em.sum()
camp['e5b'] = np.where(c == 'email', camp.fam.map(b5).fillna(0), 0.0)
e7a = E['E7a']; a7 = pd.DataFrame(dict(fam=canon(fam_pd(e7a.familia)), canal=e7a.canal, etapa=e7a.etapa, env=num('E7a', 'envios')))
p7 = a7.pivot_table(index=['fam', 'canal'], columns='etapa', values='env', aggfunc='sum', fill_value=0)
for et in ETAPAS:
    if et not in p7.columns: p7[et] = 0
idx = pd.MultiIndex.from_frame(camp[['fam', 'canal']])
camp['bloq'] = p7[BLOQUEADAS].sum(axis=1).reindex(idx).fillna(0).values
camp['e7a_tot'] = p7[ETAPAS].sum(axis=1).reindex(idx).fillna(0).values
camp['e7a_sg'] = p7['sin_golden'].reindex(idx).fillna(0).values
camp['e7a_pro'] = p7['7.Prospects'].reindex(idx).fillna(0).values
conocida = camp.e7a_tot - camp.e7a_sg
camp['pct_con'] = div(conocida, camp.e7a_tot)
camp['pct_pros'] = np.where((camp.pct_con >= 0.2) & (conocida > 0), camp.e7a_pro / conocida.where(conocida > 0), np.nan)
def accion(r):
    if r.tipo in ('cobranza', 'transaccional u operativa'): return 'No tocar'
    if r.senal == 'apagar o rehacer' and r.activo == 0: return 'Confirmar apagado'
    if r.senal == 'apagar o rehacer':
        if r.mueve == 0: return 'Apagar'
        return 'Limpiar base de WhatsApp' if r.canal == 'whatsapp' else 'Rehacer o re-segmentar'
    if r.senal == 'revisar':
        if 'bajas' in r.motivo: return 'Bajar frecuencia'
        return 'Limpiar base de WhatsApp' if r.canal == 'whatsapp' else 'Rehacer o re-segmentar'
    if r.senal == 'proteger': return 'Proteger'
    if r.senal == 'escalar': return 'Escalar'
    if r.activo == 1 and not pd.isna(r.toques) and r.toques >= 4.5 and r.canal in ('email', 'push notification'): return 'Bajar frecuencia'
    if r.activo == 1 and r.canal == 'whatsapp' and r.wa_noent * 1.0 >= 10000: return 'Limpiar base de WhatsApp'
    if r.activo == 1 and r.canal == 'email' and not pd.isna(r.usr_mean) and r.usr_mean >= 1e6: return 'Rehacer o re-segmentar'
    return 'Seguir igual'
camp['accion'] = camp.apply(accion, axis=1)
apaga = (camp.senal == 'apagar o rehacer') & (camp.accion != 'No tocar')
camp['ahorro_per_ent'] = np.where(apaga, camp.costo_ent, 0.0); camp['ahorro_per_env'] = np.where(apaga, camp.costo_env, 0.0)
camp['ahorro_mes_ent'] = np.where(apaga & (camp.activo == 1), camp.costo_ent / camp.meses, 0.0); camp['ahorro_mes_env'] = np.where(apaga & (camp.activo == 1), camp.costo_env / camp.meses, 0.0)
camp['msgs_ahorro'] = np.where(apaga & (camp.activo == 1), camp.env_mes, 0.0)
camp['costo_mes_ent'] = np.where(camp.activo == 1, camp.costo_ent / camp.meses, 0.0); camp['costo_mes_env'] = np.where(camp.activo == 1, camp.costo_env / camp.meses, 0.0)
camp['msgs_mes'] = np.where(camp.activo == 1, camp.env_mes, 0.0)
# otros canales que responden (texto, solo para --lo-test)
def otros(r):
    g = camp[(camp.fam == r.fam) & (camp.canal != r.canal) & (camp.env >= 1000) & camp.resp.notna() & camp.canal.isin(['email', 'push notification', 'in-app'])]
    g = g[g.resp >= g.minimo]
    return ', '.join(g.canal)
camp['otros'] = camp.apply(otros, axis=1) if LO_TEST else ''
NCAMP = len(camp)

cm = WS['Campañas']
CAMP_COLS = ['familia', 'canal', 'ticket', 'communication_ids', 'equipo', 'producto', 'tipo', 'audiencia (por nombre)', 'gancho (por nombre)',
 'envíos', 'meses con envíos', 'envíos_mes_prom', 'primer_mes', 'ultimo_mes', 'activo_sep', 'versiones (ids)', 'usuarios_aprox (suma de filas con envíos)', 'usuarios_por_envío (promedio)', 'toques_usuario_mes',
 'email_sent', 'email_delivery', 'email_open', 'email_click', 'email_unsubscribe', 'pn_send', 'pn_open', 'whatsapp_send', 'whatsapp_delivery', 'whatsapp_read', 'in_app_impression', 'in_app_click', 'banner_impression', 'banner_click', 'conversiones_fraccional (ref)',
 'costo_mxn', 'wa_no_entregados', 'wa_no_entregado_mxn', 'costo_mxn_mes', 'entrega', 'apertura', 'clic', 'respuesta', 'bajas_por_mil', 'conv_por_mil (ref)',
 'mínimo del canal', 'mediana envíos del canal', 'mediana respuesta del canal', 'volumen', 'señal', 'motivo', 'ahorro_mxn_periodo', 'ahorro_mxn_mes', 'msgs_mes_ahorrados',
 'abrieron (E7c)', 'no_abrieron (E7c)', 'abrieron_y_convirtieron (E7c)', 'no_abrieron_y_convirtieron (E7c)', 'conv_abren', 'conv_no_abren', 'lift', 'muestra_ok', 'mediana conv_abren del canal', 'mueve',
 'emails_a_dados_de_baja (E5b)', 'envios_con_etapa (E7a)', 'envios_etapa_bloqueada (E7a)', 'envios_sin_golden (E7a)', 'pct_etapa_conocida', 'envios_prospects (E7a)', 'pct_prospectos',
 'otros canales que responden', 'accion_tipo', 'por_qué (resumen)']
ML = {c: L(j) for j, c in enumerate(CAMP_COLS, start=1)}
INFO['Campañas'] = dict(filas=NCAMP, letters=ML, cols=CAMP_COLS)
def cr(col): return rng('Campañas', col)
for j, c in enumerate(CAMP_COLS, start=1): cm.cell(1, j, c).font = bold
MED_COLS = ['canal', 'familias (filas en Campañas)', 'mediana envíos', 'mediana respuesta', 'familias con muestra E7c', 'mediana conv_abren (con muestra)', 'mínimo de respuesta (Parámetros)',
            'apagar o rehacer', 'revisar', 'proteger', 'escalar', 'sin señal'] + ACCIONES + ['envíos', 'costo_mxn', 'ahorro_mxn_mes', 'ahorro_mxn_periodo', 'msgs_mes_ahorrados', 'wa_no_entregado_mxn']
MEDL = {c: L(j) for j, c in enumerate(MED_COLS, start=1)}
INFO['Medianas'] = dict(filas=5, letters=MEDL, cols=MED_COLS)
def med_lookup(canalref, col): return f'IFERROR(VLOOKUP({canalref},Medianas!$A$2:${MEDL[MED_COLS[-1]]}$6,{MED_COLS.index(col) + 1},FALSE),"")'

def min_formula(B): return f'IF({B}="email",{PB["min_email"]},IF({B}="push notification",{PB["min_push"]},IF({B}="whatsapp",{PB["min_wa"]},IF({B}="in-app",{PB["min_inapp"]},""))))'

for i, r0 in camp.iterrows():
    r = i + 2; A = f'$A{r}'; B = f'$B{r}'
    K = f'{FAM1},{A},{CAN1},{B}'
    x = {c: f'{ML[c]}{r}' for c in CAMP_COLS}
    resp, mn, medr, bajas = x['respuesta'], x['mínimo del canal'], x['mediana respuesta del canal'], x['bajas_por_mil']
    sen, vol, env = x['señal'], x['volumen'], x['envíos']
    row = {
     'familia': r0.fam, 'canal': r0.canal,
     'ticket': '=' + cat_lookup(A, 'ticket'), 'communication_ids': '=' + cat_lookup(A, 'communication_ids'), 'equipo': '=' + cat_lookup(A, 'equipo'), 'producto': '=' + cat_lookup(A, 'producto'),
     'tipo': '=' + cat_lookup(A, 'tipo'), 'audiencia (por nombre)': '=' + cat_lookup(A, 'audiencia (por nombre)'), 'gancho (por nombre)': '=' + cat_lookup(A, 'gancho (por nombre)'),
     'envíos': f'=SUMIFS({ENV1},{K})',
     'meses con envíos': '=' + '+'.join(f'(COUNTIFS({K},{ENV1},">0",{MESN1},{m})>0)' for m in range(1, 10)),
     'envíos_mes_prom': f'=IF({x["meses con envíos"]}>0,{env}/{x["meses con envíos"]},"")',
     'primer_mes': f'="2026-"&TEXT(MINIFS({MESN1},{K},{ENV1},">0"),"00")',
     'ultimo_mes': f'="2026-"&TEXT(MAXIFS({MESN1},{K},{ENV1},">0"),"00")',
     'activo_sep': f'=IF({x["ultimo_mes"]}="2026-09",1,0)',
     'versiones (ids)': (int(r0.versiones) if LO_TEST else f'=IFERROR(COUNTA(UNIQUE(FILTER({e1r("communication_id")},{FAM1}={A},{CAN1}={B},{ENV1}>0))),0)'),
     'usuarios_aprox (suma de filas con envíos)': f'=SUMIFS({e1r("usuarios_aprox")},{K},{ENV1},">0")',
     'usuarios_por_envío (promedio)': f'=IFERROR(AVERAGEIFS({e1r("usuarios_aprox")},{K},{ENV1},">0"),"")',
     'toques_usuario_mes': f'=IF({x["usuarios_aprox (suma de filas con envíos)"]}>0,{env}/{x["usuarios_aprox (suma de filas con envíos)"]},"")',
     'costo_mxn': '=' + costo_sumifs(K),
     'wa_no_entregados': f'=IF({B}="whatsapp",{x["whatsapp_send"]}-{x["whatsapp_delivery"]},0)',
     'wa_no_entregado_mxn': f'={x["wa_no_entregados"]}*{PB["costo_wa"]}',
     'costo_mxn_mes': f'=IF({x["activo_sep"]}=1,IFERROR({x["costo_mxn"]}/{x["meses con envíos"]},0),0)',
     'entrega': f'=IF({B}="email",IFERROR({x["email_delivery"]}/{x["email_sent"]},""),IF({B}="whatsapp",IFERROR({x["whatsapp_delivery"]}/{x["whatsapp_send"]},""),""))',
     'apertura': f'=IF({B}="email",IFERROR({x["email_open"]}/{x["email_delivery"]},""),IF({B}="push notification",IFERROR({x["pn_open"]}/{x["pn_send"]},""),IF({B}="whatsapp",IFERROR({x["whatsapp_read"]}/{x["whatsapp_delivery"]},""),"")))',
     'clic': f'=IF({B}="email",IFERROR({x["email_click"]}/{x["email_delivery"]},""),IF({B}="in-app",IFERROR({x["in_app_click"]}/{x["in_app_impression"]},""),IF({B}="banner",IFERROR({x["banner_click"]}/{x["banner_impression"]},""),"")))',
     'respuesta': f'=IF({B}="email",IFERROR({x["email_click"]}/{x["email_delivery"]},""),IF({B}="push notification",IFERROR({x["pn_open"]}/{x["pn_send"]},""),IF({B}="whatsapp",IFERROR({x["whatsapp_read"]}/{x["whatsapp_delivery"]},""),IF({B}="in-app",IFERROR({x["in_app_click"]}/{x["in_app_impression"]},""),""))))',
     'bajas_por_mil': f'=IF({B}="email",IFERROR({x["email_unsubscribe"]}/{x["email_delivery"]}*1000,""),"")',
     'conv_por_mil (ref)': f'=IFERROR({x["conversiones_fraccional (ref)"]}/{env}*1000,"")',
     'mínimo del canal': '=' + min_formula(B),
     'mediana envíos del canal': '=' + med_lookup(B, 'mediana envíos'),
     'mediana respuesta del canal': '=' + med_lookup(B, 'mediana respuesta'),
     'volumen': f'=IF({env}>={x["mediana envíos del canal"]},"alto","bajo")',
     'señal': f'=IF(NOT(ISNUMBER({resp})),"",IF(AND({vol}="alto",{resp}<{mn}),"apagar o rehacer",IF(AND({vol}="alto",OR({resp}<{medr},AND(ISNUMBER({bajas}),{bajas}>={PB["bajas_mil"]}))),"revisar",IF(AND({vol}="alto",{resp}>={PB["f_prot"]}*{medr}),"proteger",IF(AND({vol}="bajo",{env}>={PB["env_esc"]},{resp}>={PB["f_esc"]}*{medr}),"escalar","")))))',
     'motivo': f'=IF({sen}="apagar o rehacer","respuesta debajo del mínimo",IF({sen}="revisar",IF(AND(ISNUMBER({bajas}),{bajas}>={PB["bajas_mil"]},{resp}<{medr}),"respuesta baja y bajas altas",IF(AND(ISNUMBER({bajas}),{bajas}>={PB["bajas_mil"]}),"bajas altas","respuesta baja")),IF({sen}="proteger","respuesta alta con volumen",IF({sen}="escalar","respuesta alta sin volumen",""))))',
     'ahorro_mxn_periodo': f'=IF(AND({sen}="apagar o rehacer",{x["accion_tipo"]}<>"No tocar"),{x["costo_mxn"]},0)',
     'ahorro_mxn_mes': f'=IF(AND({sen}="apagar o rehacer",{x["accion_tipo"]}<>"No tocar",{x["activo_sep"]}=1),{x["costo_mxn"]}/{x["meses con envíos"]},0)',
     'msgs_mes_ahorrados': f'=IF(AND({sen}="apagar o rehacer",{x["accion_tipo"]}<>"No tocar",{x["activo_sep"]}=1),{x["envíos_mes_prom"]},0)',
     'abrieron (E7c)': f'=SUMIFS({rng("E7c","abrieron")},{rng("E7c","familia (derivada)")},{A},{rng("E7c","canal")},{B})',
     'no_abrieron (E7c)': f'=SUMIFS({rng("E7c","envios_usuario_dia")},{rng("E7c","familia (derivada)")},{A},{rng("E7c","canal")},{B})-{x["abrieron (E7c)"]}',
     'abrieron_y_convirtieron (E7c)': f'=SUMIFS({rng("E7c","abrieron_y_convirtieron")},{rng("E7c","familia (derivada)")},{A},{rng("E7c","canal")},{B})',
     'no_abrieron_y_convirtieron (E7c)': f'=SUMIFS({rng("E7c","no_abrieron_y_convirtieron")},{rng("E7c","familia (derivada)")},{A},{rng("E7c","canal")},{B})',
     'conv_abren': f'=IF({x["abrieron (E7c)"]}>0,{x["abrieron_y_convirtieron (E7c)"]}/{x["abrieron (E7c)"]},"")',
     'conv_no_abren': f'=IF({x["no_abrieron (E7c)"]}>0,{x["no_abrieron_y_convirtieron (E7c)"]}/{x["no_abrieron (E7c)"]},"")',
     'lift': f'=IF(AND(ISNUMBER({x["conv_abren"]}),ISNUMBER({x["conv_no_abren"]})),IF({x["conv_no_abren"]}>0,{x["conv_abren"]}/{x["conv_no_abren"]},""),"")',
     'muestra_ok': f'=IF(AND({x["abrieron (E7c)"]}>={PB["m_ab"]},{x["no_abrieron (E7c)"]}>={PB["m_noab"]},{x["abrieron_y_convirtieron (E7c)"]}+{x["no_abrieron_y_convirtieron (E7c)"]}>={PB["m_conv"]}),1,0)',
     'mediana conv_abren del canal': '=' + med_lookup(B, 'mediana conv_abren (con muestra)'),
     'mueve': f'=IF(AND({x["muestra_ok"]}=1,ISNUMBER({x["conv_abren"]}),ISNUMBER({x["lift"]}),ISNUMBER({x["mediana conv_abren del canal"]})),IF(AND({x["conv_abren"]}>={x["mediana conv_abren del canal"]}/2,{x["lift"]}>={PB["lift"]}),1,0),IF(AND(ISNUMBER({resp}),ISNUMBER({mn})),IF({resp}>={mn}*{PB["frac"]},1,0),0))',
     'emails_a_dados_de_baja (E5b)': f'=IF({B}="email",SUMIFS({rng("E5b","emails_despues_de_baja")},{rng("E5b","familia (derivada)")},{A}),0)',
     'envios_con_etapa (E7a)': f'=SUMIFS({rng("E7a","envios")},{rng("E7a","familia (derivada)")},{A},{rng("E7a","canal")},{B})',
     'envios_etapa_bloqueada (E7a)': '=' + '+'.join(f'SUMIFS({rng("E7a","envios")},{rng("E7a","familia (derivada)")},{A},{rng("E7a","canal")},{B},{rng("E7a","etapa")},"{et}")' for et in BLOQUEADAS),
     'envios_sin_golden (E7a)': f'=SUMIFS({rng("E7a","envios")},{rng("E7a","familia (derivada)")},{A},{rng("E7a","canal")},{B},{rng("E7a","etapa")},"sin_golden")',
     'pct_etapa_conocida': f'=IF({x["envios_con_etapa (E7a)"]}>0,({x["envios_con_etapa (E7a)"]}-{x["envios_sin_golden (E7a)"]})/{x["envios_con_etapa (E7a)"]},"")',
     'envios_prospects (E7a)': f'=SUMIFS({rng("E7a","envios")},{rng("E7a","familia (derivada)")},{A},{rng("E7a","canal")},{B},{rng("E7a","etapa")},"7.Prospects")',
     'pct_prospectos': f'=IF(AND(ISNUMBER({x["pct_etapa_conocida"]}),{x["pct_etapa_conocida"]}>={PB["etapa_min"]},{x["envios_con_etapa (E7a)"]}-{x["envios_sin_golden (E7a)"]}>0),{x["envios_prospects (E7a)"]}/({x["envios_con_etapa (E7a)"]}-{x["envios_sin_golden (E7a)"]}),"")',
     'otros canales que responden': (r0.otros if LO_TEST else f'=IFERROR(TEXTJOIN(", ",TRUE,FILTER({cr("canal")},{cr("familia")}={A},{cr("canal")}<>{B},{cr("envíos")}>=1000,ISNUMBER({cr("respuesta")}),{cr("respuesta")}>={cr("mínimo del canal")},({cr("canal")}="email")+({cr("canal")}="push notification")+({cr("canal")}="in-app"))),"")'),
     'accion_tipo': (f'=IF(OR({x["tipo"]}="cobranza",{x["tipo"]}="transaccional u operativa"),"No tocar",'
                     f'IF(AND({sen}="apagar o rehacer",{x["activo_sep"]}=0),"Confirmar apagado",'
                     f'IF({sen}="apagar o rehacer",IF({x["mueve"]}=0,"Apagar",IF({B}="whatsapp","Limpiar base de WhatsApp","Rehacer o re-segmentar")),'
                     f'IF({sen}="revisar",IF(ISNUMBER(SEARCH("bajas",{x["motivo"]})),"Bajar frecuencia",IF({B}="whatsapp","Limpiar base de WhatsApp","Rehacer o re-segmentar")),'
                     f'IF({sen}="proteger","Proteger",IF({sen}="escalar","Escalar",'
                     f'IF(AND({x["activo_sep"]}=1,ISNUMBER({x["toques_usuario_mes"]}),{x["toques_usuario_mes"]}>={PB["toques"]},OR({B}="email",{B}="push notification")),"Bajar frecuencia",'
                     f'IF(AND({x["activo_sep"]}=1,{B}="whatsapp",{x["wa_no_entregado_mxn"]}>={PB["wa_noent"]}),"Limpiar base de WhatsApp",'
                     f'IF(AND({x["activo_sep"]}=1,{B}="email",ISNUMBER({x["usuarios_por_envío (promedio)"]}),{x["usuarios_por_envío (promedio)"]}>={PB["aud"]}),"Rehacer o re-segmentar","Seguir igual")))))))))'),
     'por_qué (resumen)': (f'={x["accion_tipo"]}&" ("&{x["tipo"]}&"). "&IF(ISNUMBER({resp}),"Respuesta "&TEXT({resp},"0.00%")&" con mínimo "&TEXT({mn},"0.00%")&" y mediana del canal "&TEXT({medr},"0.00%")&"; volumen "&{vol},"Sin respuesta medible")'
                           f'&IF(ISNUMBER({bajas}),"; "&TEXT({bajas},"0.0")&" bajas por mil entregados","")&IF(ISNUMBER({x["toques_usuario_mes"]}),"; "&TEXT({x["toques_usuario_mes"]},"0.0")&" toques por usuario al mes","")'
                           f'&IF({x["muestra_ok"]}=1,"; quienes abren convierten "&TEXT({x["conv_abren"]},"0.00%")&" y quienes no "&TEXT({x["conv_no_abren"]},"0.00%")&" (lift "&TEXT({x["lift"]},"0.0")&", mediana del canal "&TEXT({x["mediana conv_abren del canal"]},"0.00%")&")","; sin muestra suficiente de conversión")'
                           f'&IF({x["mueve"]}=1,"; el mensaje sí mueve a quien lo abre","; el mensaje no mueve")'
                           f'&IF({x["emails_a_dados_de_baja (E5b)"]}>={PB["e5b"]},"; "&TEXT({x["emails_a_dados_de_baja (E5b)"]},"#,##0")&" emails a usuarios ya dados de baja (E5b)","")'
                           f'&IF({x["envios_etapa_bloqueada (E7a)"]}>={PB["e7a"]},"; "&TEXT({x["envios_etapa_bloqueada (E7a)"]},"#,##0")&" envíos a Blacklist, CC Freeze o REUS/ARCO (E7a)","")'
                           f'&IF(AND(ISNUMBER({x["pct_prospectos"]}),{x["pct_prospectos"]}>={PB["pros"]}),"; "&TEXT({x["pct_prospectos"]},"0%")&" de los envíos con etapa conocida va a prospectos sin crédito","")'
                           f'&IF({x["wa_no_entregado_mxn"]}>={PB["wa_noent"]},"; "&TEXT({x["wa_no_entregado_mxn"]},"#,##0")&" MXN de WhatsApp no entregado si se cobrara por enviado","")'),
    }
    for k2, col in RAWCOL.items():
        name = col if k2 != 'cf' else 'conversiones_fraccional (ref)'
        row[name] = f'=SUMIFS({e1r(col)},{K})'
    for cname in CAMP_COLS:
        cm.cell(r, CAMP_COLS.index(cname) + 1, row[cname])
    for cname in ('entrega', 'apertura', 'clic', 'respuesta', 'conv_abren', 'conv_no_abren', 'pct_etapa_conocida', 'pct_prospectos', 'mínimo del canal', 'mediana respuesta del canal', 'mediana conv_abren del canal'):
        cm.cell(r, CAMP_COLS.index(cname) + 1).number_format = '0.00%'
    for cname in ('costo_mxn', 'ahorro_mxn_periodo', 'ahorro_mxn_mes', 'envíos', 'envíos_mes_prom', 'wa_no_entregado_mxn', 'costo_mxn_mes'):
        cm.cell(r, CAMP_COLS.index(cname) + 1).number_format = '#,##0'
cm.freeze_panes = 'C2'; cm.auto_filter.ref = f'A1:{ML[CAMP_COLS[-1]]}{NCAMP + 1}'
for cname in CAMP_COLS: cm.column_dimensions[ML[cname]].width = 60 if cname == 'familia' else (50 if cname in ('por_qué (resumen)', 'communication_ids') else 13)
# Catálogo: acciones de Campañas
for i in range(NC):
    r = i + 2
    cat.cell(r, CAT_COLS.index('acciones (de Campañas)') + 1, f'=IFERROR(TEXTJOIN(" | ",TRUE,FILTER({cr("canal")}&": "&{cr("accion_tipo")},{cr("familia")}=$A{r})),"")' if not LO_TEST else '')

# ---------- Medianas (resumen por canal)
md = WS['Medianas']
for j, c in enumerate(MED_COLS, start=1): md.cell(1, j, c).font = bold
from openpyxl.worksheet.formula import ArrayFormula
def median_filter(valrng, condrng, condval_ref, extra_num=None, extra_flag=None, cellref=None):
    """MEDIAN(FILTER(...)) en Google; en --lo-test, fórmula matricial MEDIAN(IF(...)) que LibreOffice sí evalúa."""
    if not LO_TEST:
        conds = f'{condrng}={condval_ref}'
        if extra_num: conds += f',ISNUMBER({extra_num})'
        if extra_flag: conds += f',{extra_flag}=1'
        return f'=IFERROR(MEDIAN(FILTER({valrng},{conds})),"")'
    conds = f'({condrng}={condval_ref})'
    if extra_num: conds += f'*ISNUMBER({extra_num})'
    if extra_flag: conds += f'*({extra_flag}=1)'
    return ArrayFormula(cellref, f'=IFERROR(MEDIAN(IF({conds},{valrng},"")),"")')
for k, canal in enumerate(CANALES):
    r = k + 2; A = f'$A{r}'
    vals = {'canal': canal,
     'familias (filas en Campañas)': f'=COUNTIF({cr("canal")},{A})',
     'mediana envíos': median_filter(cr('envíos'), cr('canal'), A, cellref=f'{MEDL["mediana envíos"]}{r}'),
     'mediana respuesta': median_filter(cr('respuesta'), cr('canal'), A, extra_num=cr('respuesta'), cellref=f'{MEDL["mediana respuesta"]}{r}'),
     'familias con muestra E7c': f'=COUNTIFS({cr("canal")},{A},{cr("muestra_ok")},1)',
     'mediana conv_abren (con muestra)': median_filter(cr('conv_abren'), cr('canal'), A, extra_num=cr('conv_abren'), extra_flag=cr('muestra_ok'), cellref=f'{MEDL["mediana conv_abren (con muestra)"]}{r}'),
     'mínimo de respuesta (Parámetros)': '=' + min_formula(A),
     'envíos': f'=SUMIFS({cr("envíos")},{cr("canal")},{A})', 'costo_mxn': f'=SUMIFS({cr("costo_mxn")},{cr("canal")},{A})',
     'ahorro_mxn_mes': f'=SUMIFS({cr("ahorro_mxn_mes")},{cr("canal")},{A})', 'ahorro_mxn_periodo': f'=SUMIFS({cr("ahorro_mxn_periodo")},{cr("canal")},{A})',
     'msgs_mes_ahorrados': f'=SUMIFS({cr("msgs_mes_ahorrados")},{cr("canal")},{A})', 'wa_no_entregado_mxn': f'=SUMIFS({cr("wa_no_entregado_mxn")},{cr("canal")},{A})'}
    for s in SENALES: vals[s] = f'=COUNTIFS({cr("canal")},{A},{cr("señal")},"{s}")'
    vals['sin señal'] = f'=COUNTIFS({cr("canal")},{A},{cr("señal")},"")'
    for a in ACCIONES: vals[a] = f'=COUNTIFS({cr("canal")},{A},{cr("accion_tipo")},"{a}")'
    for cname, v in vals.items(): md.cell(r, MED_COLS.index(cname) + 1, v)
    for cname in ('mediana respuesta', 'mediana conv_abren (con muestra)', 'mínimo de respuesta (Parámetros)'): md.cell(r, MED_COLS.index(cname) + 1).number_format = '0.00%'
md.cell(7, 1, 'todos los canales').font = bold
for cname in MED_COLS[1:2] + MED_COLS[4:5] + MED_COLS[7:]:
    col = MED_COLS.index(cname) + 1; md.cell(7, col, f'=SUM({MEDL[cname]}2:{MEDL[cname]}6)')
md.cell(9, 1, 'Cómo leer: "volumen alto" en Campañas = envíos de la familia ≥ mediana envíos de su canal. La señal compara la respuesta de la familia contra el mínimo (Parámetros) y contra la mediana del canal. Las medianas se calculan sobre las familias con respuesta medible (ISNUMBER). mediana conv_abren solo usa familias con muestra suficiente (Parámetros filas 17 a 19).').alignment = wrap
md.cell(10, 1, 'Disclaimer: la mediana cambia si cambian los datos o el periodo; una familia puede pasar de "revisar" a "sin señal" solo porque la mediana del canal se movió. Por eso la señal se lee junto con el mínimo (fijo) y no sola.').alignment = wrap
md.freeze_panes = 'B2'
for cname in MED_COLS: md.column_dimensions[MEDL[cname]].width = 16
md.column_dimensions['A'].width = 22

# =====================================================================================
# ---------- pestañas por lente
# =====================================================================================
def header(ws, title, fuente, disclaimer):
    ws.cell(1, 1, title).font = bold
    ws.cell(2, 1, 'Fuente: ' + fuente).alignment = wrap
    ws.cell(3, 1, 'Supuestos y disclaimer: ' + disclaimer).alignment = wrap
    ws.column_dimensions['A'].width = 44
    for col in 'BCDEFGHIJKLMNOPQRSTUVWXYZ': ws.column_dimensions[col].width = 15

def table(ws, r0, title, headers, rows, pct_cols=(), int_cols=()):
    """Escribe título en r0, encabezados en r0+1 y filas desde r0+2. Devuelve (letras, primera fila, última fila)."""
    ws.cell(r0, 1, title).font = bold
    letters = {h: L(j) for j, h in enumerate(headers, start=1)}
    for j, h in enumerate(headers, start=1): ws.cell(r0 + 1, j, h).font = bold
    for i, row in enumerate(rows):
        r = r0 + 2 + i
        for j, v in enumerate(row, start=1):
            if v is None or v == '': continue
            cc = ws.cell(r, j, v)
            if headers[j - 1] in pct_cols: cc.number_format = '0.00%'
            elif headers[j - 1] in int_cols: cc.number_format = '#,##0'
    return letters, r0 + 2, r0 + 1 + len(rows)

def trng(ws, letters, col, a, b): return f"{ws.title}!${letters[col]}${a}:${letters[col]}${b}"
def spill(ws, r0, title, headers, formula, note):
    ws.cell(r0, 1, title).font = bold
    for j, h in enumerate(headers, start=1): ws.cell(r0 + 1, j, h).font = bold
    if LO_TEST: ws.cell(r0 + 2, 1, '(lista omitida en la prueba local: usa SORT y FILTER)')
    else: ws.cell(r0 + 2, 1, formula)
    ws.cell(r0 + 1, len(headers) + 1, note).alignment = wrap

def e4(col): return rng('E4a', col)
DEN = {'email': 'email_delivery', 'push notification': 'pn_send', 'whatsapp': 'whatsapp_delivery', 'in-app': 'in_app_impression', 'banner': 'banner_impression'}
NUMR = {'email': 'email_click', 'push notification': 'pn_open', 'whatsapp': 'whatsapp_read', 'in-app': 'in_app_click', 'banner': 'banner_click'}
RESP_LABEL = {'email': 'clic / entregado', 'push notification': 'apertura / enviado', 'whatsapp': 'lectura / entregado', 'in-app': 'clic / impresión', 'banner': 'clic / impresión'}

# ---------- B_Canales
ws = WS['B_Canales']
header(ws, 'Lente B. Canales: volumen, respuesta, bajas y costo por mes y canal',
       'E4a (grano mes), E4b (concentración por banda), Parámetros (costos y base de cobro).',
       'E4a cuenta eventos sin deduplicar (0.01 % arriba de E1). Respuesta = clic/entregado en email, apertura/enviado en push, lectura/entregado en WhatsApp, clic/impresión en in-app. Bajas solo existen en email: eventos (una fila por evento) y usuario-mes (un usuario cuenta cada mes). Costo = email_sent × costo email + WhatsApp (entregado o enviado según Parámetros!B6) × costo WhatsApp; push e in-app sin costo. Costo fijo de Braze no incluido.')
H1 = ['mes', 'canal', 'envíos', 'denominador de respuesta (entregados, enviados o impresiones)', 'numerador de respuesta', 'respuesta', 'definición de respuesta', 'bajas_email_eventos', 'bajas_email_usuarios (usuario-mes)', 'bajas por mil entregados (email)', 'costo_mxn', 'comunicaciones activas', 'email_sent', 'whatsapp_send', 'whatsapp_delivery', 'pn_send', 'in_app_impression']
rows = []
for m in MESES:
    for cnl in CANALES:
        crit = f'{e4("grano")},"mes",{e4("mes_clave (derivada)")},"{m}",{e4("canal")},"{cnl}"'
        rr = len(rows) + 6
        rows.append([m, cnl, f'=SUMIFS({e4("envios")},{crit})', f'=SUMIFS({e4(DEN[cnl])},{crit})', f'=SUMIFS({e4(NUMR[cnl])},{crit})', f'=IFERROR(E{rr}/D{rr},"")', RESP_LABEL[cnl],
                     f'=SUMIFS({e4("bajas_email_eventos")},{crit})', f'=SUMIFS({e4("bajas_email_usuarios")},{crit})', f'=IF(B{rr}="email",IFERROR(H{rr}/D{rr}*1000,""),"")',
                     f'=M{rr}*{PB["costo_email"]}+IF({PB["base_wa"]}="entregado",O{rr},N{rr})*{PB["costo_wa"]}+P{rr}*{PB["costo_push"]}+Q{rr}*{PB["costo_inapp"]}',
                     f'=SUMIFS({e4("comunicaciones")},{crit})', f'=SUMIFS({e4("email_sent")},{crit})', f'=SUMIFS({e4("whatsapp_send")},{crit})', f'=SUMIFS({e4("whatsapp_delivery")},{crit})', f'=SUMIFS({e4("pn_send")},{crit})', f'=SUMIFS({e4("in_app_impression")},{crit})'])
LB1, b1a, b1b = table(ws, 4, 'B1. Mes × canal (45 filas)', H1, rows, pct_cols=('respuesta',), int_cols=('envíos', 'costo_mxn'))
BR = lambda col: trng(ws, LB1, col, b1a, b1b)
r0 = b1b + 3
H2 = ['canal', 'envíos', 'denominador', 'numerador', 'respuesta', 'bajas_email_eventos', 'bajas_email_usuarios (usuario-mes)', 'bajas por mil entregados', 'costo_mxn', '% del costo', '% de los envíos', 'whatsapp_send', 'whatsapp_delivery', '% entrega WhatsApp']
rows = []
for k, cnl in enumerate(CANALES):
    rr = r0 + 2 + k
    rows.append([cnl, f'=SUMIFS({BR("envíos")},{BR("canal")},A{rr})', f'=SUMIFS({BR(H1[3])},{BR("canal")},A{rr})', f'=SUMIFS({BR("numerador de respuesta")},{BR("canal")},A{rr})', f'=IFERROR(D{rr}/C{rr},"")',
                 f'=SUMIFS({BR("bajas_email_eventos")},{BR("canal")},A{rr})', f'=SUMIFS({BR("bajas_email_usuarios (usuario-mes)")},{BR("canal")},A{rr})', f'=IF(A{rr}="email",IFERROR(F{rr}/C{rr}*1000,""),"")',
                 f'=SUMIFS({BR("costo_mxn")},{BR("canal")},A{rr})', f'=IFERROR(I{rr}/I${r0 + 7},"")', f'=IFERROR(B{rr}/B${r0 + 7},"")', f'=SUMIFS({BR("whatsapp_send")},{BR("canal")},A{rr})', f'=SUMIFS({BR("whatsapp_delivery")},{BR("canal")},A{rr})', f'=IF(A{rr}="whatsapp",IFERROR(M{rr}/L{rr},""),"")'])
rr = r0 + 7
rows.append(['total', f'=SUM(B{r0 + 2}:B{r0 + 6})', '', '', '', f'=SUM(F{r0 + 2}:F{r0 + 6})', f'=SUM(G{r0 + 2}:G{r0 + 6})', '', f'=SUM(I{r0 + 2}:I{r0 + 6})', '', '', f'=SUM(L{r0 + 2}:L{r0 + 6})', f'=SUM(M{r0 + 2}:M{r0 + 6})', f'=IFERROR(M{rr}/L{rr},"")'])
LB2, b2a, b2b = table(ws, r0, 'B2. Total del periodo por canal', H2, rows, pct_cols=('respuesta', '% del costo', '% de los envíos', '% entrega WhatsApp'), int_cols=('envíos', 'costo_mxn'))
B2ROW = {cnl: b2a + k for k, cnl in enumerate(CANALES)}
r0 = b2b + 3
BANDAS4B = ['00', '01-05', '06-10', '11-20', '21-40', '41-80', '081-160', '161+']
H3 = ['mes', 'usuarios con fila'] + [f'usuarios banda {b}' for b in BANDAS4B] + ['% usuarios con 41+ msgs', 'msgs totales', 'msgs de usuarios con 41+', '% msgs a usuarios con 41+', 'baja por 100 usuarios banda 01-05', 'baja por 100 usuarios banda 41+']
rows = []
def e4b(col): return rng('E4b', col)
for k, m in enumerate(MESES):
    rr = r0 + 2 + k; cm_ = f'{e4b("mes_clave (derivada)")},A{rr}'
    row = [m, f'=SUMIFS({e4b("usuarios")},{cm_})'] + [f'=SUMIFS({e4b("usuarios")},{cm_},{e4b("banda_msgs_mes")},"{b}")' for b in BANDAS4B]
    c41 = f'(H{rr}+I{rr}+J{rr})'
    row += [f'=IFERROR({c41}/B{rr},"")', f'=SUMIFS({e4b("msgs")},{cm_})', '=' + '+'.join(f'SUMIFS({e4b("msgs")},{cm_},{e4b("banda_msgs_mes")},"{b}")' for b in BANDAS4B[5:]), f'=IFERROR(M{rr}/L{rr},"")',
            f'=IFERROR(SUMIFS({e4b("usuarios_con_baja_email")},{cm_},{e4b("banda_msgs_mes")},"01-05")/D{rr}*100,"")', '=IFERROR((' + '+'.join(f'SUMIFS({e4b("usuarios_con_baja_email")},{cm_},{e4b("banda_msgs_mes")},"{b}")' for b in BANDAS4B[5:]) + f')/{c41}*100,"")']
    rows.append(row)
LB3, b3a, b3b = table(ws, r0, 'B3. Concentración (E4b): cuántos usuarios reciben cuántos mensajes al mes. La banda 00 son usuarios con fila pero sin mensaje contado.', H3, rows, pct_cols=('% usuarios con 41+ msgs', '% msgs a usuarios con 41+'))
r0 = b3b + 3
H4 = ['mes', 'whatsapp_send', 'whatsapp_delivery', '% entrega', 'no entregados', 'MXN que costarían los no entregados si se cobrara por enviado', 'whatsapp_read', 'lectura / entregado']
rows = []
for k, m in enumerate(MESES):
    rr = r0 + 2 + k
    rows.append([m, f'=SUMIFS({BR("whatsapp_send")},{BR("mes")},A{rr},{BR("canal")},"whatsapp")', f'=SUMIFS({BR("whatsapp_delivery")},{BR("mes")},A{rr},{BR("canal")},"whatsapp")', f'=IFERROR(C{rr}/B{rr},"")', f'=B{rr}-C{rr}', f'=E{rr}*{PB["costo_wa"]}',
                 f'=SUMIFS({BR("numerador de respuesta")},{BR("mes")},A{rr},{BR("canal")},"whatsapp")', f'=IFERROR(G{rr}/C{rr},"")'])
LB4, b4a, b4b = table(ws, r0, 'B4. WhatsApp: entrega por mes (la base que no recibe es la primera señal de limpieza)', H4, rows, pct_cols=('% entrega', 'lectura / entregado'), int_cols=('whatsapp_send', 'whatsapp_delivery', 'no entregados'))
ws.freeze_panes = 'A6'

# ---------- E_DespuesBaja
ws = WS['E_DespuesBaja']
header(ws, 'Lente E. Qué reciben los usuarios después de darse de baja de email',
       'E5 (cohorte por mes de baja), E5b (familias que mandaron email a dados de baja), Catálogo (equipo y tipo de la familia).',
       'La baja es de email (email_unsubscribe). "Reciben email después" = al menos un email enviado después de la fecha de baja dentro del periodo; los meses finales tienen menos tiempo de observación (septiembre casi no tiene "después"). Un usuario dado de baja NO debería recibir email promocional; el transaccional sí puede llegar. El tipo de la familia sale del Catálogo por el nombre (ticket) y el equipo, no de Braze.')
def e5(col, r): return f'E5!${INFO["E5"]["letters"][col]}${r}'
H1 = ['mes_baja', 'usuarios_baja', 'reciben_email_m1', '% m1', 'emails_m1', 'reciben_email_m2', '% m2', 'emails_m2', 'reciben_email_m3', '% m3', 'emails_m3', 'reciben_email_despues_total', '% que recibe algo después', 'emails_despues_total', 'emails por usuario que recibió', 'abiertos_despues_total', '% abiertos', 'se_dan_de_baja_otra_vez', '% se dan de baja otra vez']
rows = []
n5 = INFO['E5']['filas']
for k in range(n5):
    r5 = k + 2; rr = 6 + k
    rows.append([f'={e5("mes_baja", r5)}', f'={e5("usuarios_baja", r5)}', f'={e5("reciben_email_m1", r5)}', f'=IFERROR(C{rr}/B{rr},"")', f'={e5("emails_m1", r5)}', f'={e5("reciben_email_m2", r5)}', f'=IFERROR(F{rr}/B{rr},"")', f'={e5("emails_m2", r5)}',
                 f'={e5("reciben_email_m3", r5)}', f'=IFERROR(I{rr}/B{rr},"")', f'={e5("emails_m3", r5)}', f'={e5("reciben_email_despues_total", r5)}', f'=IFERROR(L{rr}/B{rr},"")', f'={e5("emails_despues_total", r5)}', f'=IFERROR(N{rr}/L{rr},"")',
                 f'={e5("abiertos_despues_total", r5)}', f'=IFERROR(P{rr}/N{rr},"")', f'={e5("se_dan_de_baja_otra_vez", r5)}', f'=IFERROR(R{rr}/B{rr},"")'])
rr = 6 + n5; a, b = 6, 5 + n5
rows.append(['total', f'=SUM(B{a}:B{b})', f'=SUM(C{a}:C{b})', f'=IFERROR(C{rr}/B{rr},"")', f'=SUM(E{a}:E{b})', f'=SUM(F{a}:F{b})', f'=IFERROR(F{rr}/B{rr},"")', f'=SUM(H{a}:H{b})', f'=SUM(I{a}:I{b})', f'=IFERROR(I{rr}/B{rr},"")', f'=SUM(K{a}:K{b})', f'=SUM(L{a}:L{b})', f'=IFERROR(L{rr}/B{rr},"")', f'=SUM(N{a}:N{b})', f'=IFERROR(N{rr}/L{rr},"")', f'=SUM(P{a}:P{b})', f'=IFERROR(P{rr}/N{rr},"")', f'=SUM(R{a}:R{b})', f'=IFERROR(R{rr}/B{rr},"")'])
LE1, e1a, e1b = table(ws, 4, 'E1. Cohorte por mes de baja (E5). m1 = primer mes después de la baja, m2 el segundo, m3 el tercero.', H1, rows, pct_cols=('% m1', '% m2', '% m3', '% que recibe algo después', '% abiertos', '% se dan de baja otra vez'))
E_TOTAL_ROW = e1b
r0 = e1b + 3
def e5b(col): return rng('E5b', col)
H2 = ['tipo de la familia', 'familias', 'emails_despues_de_baja', '% de los emails', 'usuarios_aprox (suma, no únicos)', 'abiertos', 'clics']
rows = []
for k, t in enumerate(TIPOS + ['no está en E1']):
    rr = r0 + 2 + k
    rows.append([t, f'=COUNTIF({e5b("tipo (derivada)")},A{rr})', f'=SUMIFS({e5b("emails_despues_de_baja")},{e5b("tipo (derivada)")},A{rr})', f'=IFERROR(C{rr}/C${r0 + 6},"")', f'=SUMIFS({e5b("usuarios_aprox")},{e5b("tipo (derivada)")},A{rr})', f'=SUMIFS({e5b("abiertos")},{e5b("tipo (derivada)")},A{rr})', f'=SUMIFS({e5b("clics")},{e5b("tipo (derivada)")},A{rr})'])
rows.append(['total', f'=SUM(B{r0 + 2}:B{r0 + 5})', f'=SUM(C{r0 + 2}:C{r0 + 5})', '', f'=SUM(E{r0 + 2}:E{r0 + 5})', f'=SUM(F{r0 + 2}:F{r0 + 5})', f'=SUM(G{r0 + 2}:G{r0 + 5})'])
LE2, e2a, e2b = table(ws, r0, 'E2. Emails a dados de baja por tipo de familia (E5b). Lo grave es lo promocional: el transaccional y la cobranza pueden llegar aunque el usuario esté dado de baja.', H2, rows, pct_cols=('% de los emails',), int_cols=('emails_despues_de_baja',))
E_TIPO_ROW = {t: e2a + k for k, t in enumerate(TIPOS + ['no está en E1'])}
r0 = e2b + 3
H3 = ['equipo', 'familias', 'emails_despues_de_baja', '% de los emails', 'de los cuales promocionales']
rows = []
for k, t in enumerate(EQUIPOS + ['no está en E1']):
    rr = r0 + 2 + k
    rows.append([t, f'=COUNTIF({e5b("equipo (derivada)")},A{rr})', f'=SUMIFS({e5b("emails_despues_de_baja")},{e5b("equipo (derivada)")},A{rr})', f'=IFERROR(C{rr}/SUM(C${r0 + 2}:C${r0 + 7}),"")', f'=SUMIFS({e5b("emails_despues_de_baja")},{e5b("equipo (derivada)")},A{rr},{e5b("tipo (derivada)")},"promocional o lifecycle")'])
LE3, e3a, e3b = table(ws, r0, 'E3. Por equipo (equipo del Catálogo, con el mapeo de Parámetros)', H3, rows, pct_cols=('% de los emails',), int_cols=('emails_despues_de_baja', 'de los cuales promocionales'))
r0 = e3b + 3
spill(ws, r0, 'E4. Familias promocionales que mandaron email a usuarios ya dados de baja, de mayor a menor (lista viva: se recalcula con el Catálogo)',
      ['familia', 'equipo', 'emails_despues_de_baja', 'usuarios_aprox', 'abiertos', 'clics', 'meses', 'ticket'],
      f'=SORT(FILTER({{{e5b("familia (derivada)")},{e5b("equipo (derivada)")},{e5b("emails_despues_de_baja")},{e5b("usuarios_aprox")},{e5b("abiertos")},{e5b("clics")},{e5b("meses")},ARRAYFORMULA(IFERROR(VLOOKUP({e5b("familia (derivada)")},Catálogo!$A$2:$B${NC + 1},2,FALSE),""))}},{e5b("tipo (derivada)")}="promocional o lifecycle"),3,FALSE)',
      'Qué hacer: en cada Canvas de esta lista revisar que el paso de email tenga el filtro de suscripción (subscribed o opted_in) y no "todos".')
ws.freeze_panes = 'A6'

# ---------- F_Solape
ws = WS['F_Solape']
header(ws, 'Lente F. Solapamiento: cuántas familias distintas recibe un usuario el mismo día',
       'E6a (usuario-días por banda de familias distintas en el día), E6b (top 1,000 pares de familias que coinciden en el mismo usuario-día), Catálogo.',
       'Grano usuario-día: un usuario cuenta una vez por cada día con al menos un mensaje. "Con respuesta" = ese día tuvo clic de email, apertura de push, lectura de WhatsApp o clic de in-app. "Con baja" = ese día se dio de baja de email. E6b trae solo los 1,000 pares más grandes (LIMIT): sirve para ver quién choca con quién, no para totales. Los mensajes de E6a quedan 0.5 % debajo de E1 por el grano.')
def e6(col): return rng('E6a', col)
BANDAS6 = ['1', '2', '3 a 4', '5 a 7', '8+']
H1 = ['familias distintas en el día', 'usuario_dias', '% usuario-días', 'msgs', 'msgs por usuario-día', 'usuarios_aprox (suma de meses)', 'usuario_dias_con_respuesta', '% con respuesta', 'usuario_dias_con_conversion', '% con conversión', 'usuario_dias_con_baja', 'bajas por mil usuario-días']
rows = []
for k, b in enumerate(BANDAS6):
    rr = 6 + k; cb = f'{e6("banda_familias_dia")},A{rr}'
    rows.append([b, f'=SUMIFS({e6("usuario_dias")},{cb})', f'=IFERROR(B{rr}/B$11,"")', f'=SUMIFS({e6("msgs")},{cb})', f'=IFERROR(D{rr}/B{rr},"")', f'=SUMIFS({e6("usuarios_aprox")},{cb})', f'=SUMIFS({e6("usuario_dias_con_respuesta")},{cb})', f'=IFERROR(G{rr}/B{rr},"")',
                 f'=SUMIFS({e6("usuario_dias_con_conversion")},{cb})', f'=IFERROR(I{rr}/B{rr},"")', f'=SUMIFS({e6("usuario_dias_con_baja")},{cb})', f'=IFERROR(K{rr}/B{rr}*1000,"")'])
rows.append(['total', '=SUM(B6:B10)', '', '=SUM(D6:D10)', '=IFERROR(D11/B11,"")', '', '=SUM(G6:G10)', '=IFERROR(G11/B11,"")', '=SUM(I6:I10)', '=IFERROR(I11/B11,"")', '=SUM(K6:K10)', '=IFERROR(K11/B11*1000,"")'])
LF1, f1a, f1b = table(ws, 4, 'F1. Por banda de familias distintas en el día (todo el periodo)', H1, rows, pct_cols=('% usuario-días', '% con respuesta', '% con conversión'), int_cols=('usuario_dias', 'msgs'))
r0 = f1b + 3
H2 = ['mes', 'usuario_dias', 'usuario_dias con 1 familia', 'usuario_dias con 3 o más', '% con 3 o más', 'bajas por mil usuario-días (1 familia)', 'bajas por mil usuario-días (3 o más)']
rows = []
for k, m in enumerate(MESES):
    rr = r0 + 2 + k; cm_ = f'{e6("mes_clave (derivada)")},A{rr}'
    tres = lambda col: '(' + '+'.join(f'SUMIFS({e6(col)},{cm_},{e6("banda_familias_dia")},"{b}")' for b in BANDAS6[2:]) + ')'
    rows.append([m, f'=SUMIFS({e6("usuario_dias")},{cm_})', f'=SUMIFS({e6("usuario_dias")},{cm_},{e6("banda_familias_dia")},"1")', '=' + tres('usuario_dias'), f'=IFERROR(D{rr}/B{rr},"")',
                 f'=IFERROR(SUMIFS({e6("usuario_dias_con_baja")},{cm_},{e6("banda_familias_dia")},"1")/C{rr}*1000,"")', f'=IFERROR({tres("usuario_dias_con_baja")}/D{rr}*1000,"")'])
LF2, f2a, f2b = table(ws, r0, 'F2. Por mes', H2, rows, pct_cols=('% con 3 o más',), int_cols=('usuario_dias', 'usuario_dias con 1 familia', 'usuario_dias con 3 o más'))
r0 = f2b + 3
def e6b(col): return rng('E6b', col)
e6bdf = E['E6b']
eqa = canon(fam_pd(e6bdf.familia_a)).map(catp.equipo).fillna('no está en E1'); eqb = canon(fam_pd(e6bdf.familia_b)).map(catp.equipo).fillna('no está en E1')
pares = pd.Series([f'{a} + {b}' if a <= b else f'{b} + {a}' for a, b in zip(eqa, eqb)])
ud = num('E6b', 'usuario_dias_juntas'); par_sum = ud.groupby(pares).sum().sort_values(ascending=False)
H3 = ['par de equipos', 'pares de familias (filas de E6b)', 'usuario_dias_juntas', '% de los usuario-días de E6b', 'pares donde ambas son promocionales', 'usuario_dias_juntas de esos pares']
rows = []
for k, lab in enumerate(par_sum.index):
    rr = r0 + 2 + k; cp_ = f'{e6b("par_equipos (derivada)")},A{rr}'
    rows.append([lab, f'=COUNTIF({e6b("par_equipos (derivada)")},A{rr})', f'=SUMIFS({e6b("usuario_dias_juntas")},{cp_})', f'=IFERROR(C{rr}/SUM({e6b("usuario_dias_juntas")}),"")', f'=COUNTIFS({cp_},{e6b("ambas promocionales (derivada)")},1)', f'=SUMIFS({e6b("usuario_dias_juntas")},{cp_},{e6b("ambas promocionales (derivada)")},1)'])
LF3, f3a, f3b = table(ws, r0, 'F3. Quién choca con quién: pares de equipos (equipo del Catálogo). Las etiquetas vienen de los datos actuales; si cambia el mapeo de equipos, agrega las filas que falten.', H3, rows, pct_cols=('% de los usuario-días de E6b',), int_cols=('usuario_dias_juntas', 'usuario_dias_juntas de esos pares'))
r0 = f3b + 3
spill(ws, r0, 'F4. Los 30 pares de familias que más coinciden en el mismo usuario el mismo día',
      ['familia_a', 'familia_b', 'canal_a', 'canal_b', 'equipo_a', 'equipo_b', 'usuario_dias_juntas', 'usuarios_aprox', 'meses', 'tipo_a', 'tipo_b'],
      f'=ARRAY_CONSTRAIN(SORT({{{e6b("familia_a (derivada)")},{e6b("familia_b (derivada)")},{e6b("canal_a")},{e6b("canal_b")},{e6b("equipo_a (derivada)")},{e6b("equipo_b (derivada)")},{e6b("usuario_dias_juntas")},{e6b("usuarios_aprox")},{e6b("meses")},{e6b("tipo_a (derivada)")},{e6b("tipo_b (derivada)")}}},7,FALSE),30,11)',
      'Qué hacer: para cada par promocional + promocional, regla de exclusión mutua en Braze (frequency capping o "no enviar si recibió X en las últimas 24 h").')
ws.freeze_panes = 'A6'

# ---------- G_Practicas
ws = WS['G_Practicas']
header(ws, 'Lente G. Buenas prácticas: qué audiencias, ganchos, tamaños y frecuencias responden mejor',
       'E1 con columnas derivadas audiencia, gancho, banda_tamaño y banda_toques (por nombre de la comunicación y por envíos / usuarios_aprox), E3 (fatiga por banda de mensajes).',
       'Audiencia y gancho se infieren del NOMBRE de la comunicación con palabras clave (ver Léeme); "otros" = el nombre no dice. Tamaño = usuarios_aprox del mes; toques = envíos / usuarios_aprox del mes de esa comunicación (solo filas con más de 1,000 usuarios). Las tablas de gancho, tamaño y toques excluyen audiencias cobranza y transaccional. Respuesta por canal igual que en Campañas. Correlación, no causalidad: una audiencia fría responde menos por ser fría, no solo por el mensaje.')
AUD1 = e1r('audiencia (derivada)'); GAN1 = e1r('gancho (derivada)'); TAM1 = e1r('banda_tamaño (derivada)'); TOQ1 = e1r('banda_toques (derivada)'); USR1 = e1r('usuarios_aprox')
def resp_cols(cnl, crit, rr, col_num, col_den):
    return [f'=SUMIFS({e1r(DEN[cnl])},{crit})', f'=SUMIFS({e1r(NUMR[cnl])},{crit})', f'=IFERROR({col_num}{rr}/{col_den}{rr},"")']
def g_table(r0, title, key_name, keys, extra_crit, excl_cobranza, canales):
    H = [key_name, 'canal', 'comunicación-meses (filas de E1)', 'envíos', 'denominador de respuesta', 'numerador de respuesta', 'respuesta', 'bajas por mil entregados (email)', 'costo_mxn', 'conv por mil envíos (ref)']
    rows = []
    for key in keys:
        for cnl in canales:
            rr = r0 + 2 + len(rows)
            crit = f'{extra_crit},A{rr},{CAN1},B{rr}' + (f',{AUD1},"<>cobranza",{AUD1},"<>transaccional"' if excl_cobranza else '')
            rows.append([key, cnl, f'=COUNTIFS({crit})', f'=SUMIFS({ENV1},{crit})'] + resp_cols(cnl, crit, rr, 'F', 'E') +
                        [f'=IF(B{rr}="email",IFERROR(SUMIFS({e1r("email_unsubscribe")},{crit})/E{rr}*1000,""),"")', '=' + costo_sumifs(crit), f'=IFERROR(SUMIFS({e1r("conversiones_fraccional")},{crit})/D{rr}*1000,"")'])
    return table(ws, r0, title, H, rows, pct_cols=('respuesta',), int_cols=('envíos', 'costo_mxn'))
LG1, g1a, g1b = g_table(4, 'G1. Audiencia (por nombre) × canal', 'audiencia', AUDS, AUD1, False, C4)
LG2, g2a, g2b = g_table(g1b + 3, 'G2. Gancho (por nombre) × canal, sin cobranza ni transaccional', 'gancho', GANS, GAN1, True, C4)
LG3, g3a, g3b = g_table(g2b + 3, 'G3. Tamaño de audiencia del envío (usuarios_aprox del mes) × canal, sin cobranza ni transaccional', 'banda_tamaño', TAM, TAM1, True, ['email', 'push notification'])
# G4 toques con usuarios_aprox > 1000
r0 = g3b + 3
H = ['banda_toques (envíos / usuarios del mes)', 'canal', 'comunicación-meses (filas de E1 con más de 1,000 usuarios)', 'envíos', 'denominador de respuesta', 'numerador de respuesta', 'respuesta', 'bajas por mil entregados (email)', 'apertura email (abiertos / entregados)']
rows = []
for key in TOQ:
    for cnl in ['email', 'push notification']:
        rr = r0 + 2 + len(rows); crit = f'{TOQ1},A{rr},{CAN1},B{rr},{USR1},">1000",{AUD1},"<>cobranza",{AUD1},"<>transaccional"'
        rows.append([key, cnl, f'=COUNTIFS({crit})', f'=SUMIFS({ENV1},{crit})'] + resp_cols(cnl, crit, rr, 'F', 'E') + [f'=IF(B{rr}="email",IFERROR(SUMIFS({e1r("email_unsubscribe")},{crit})/E{rr}*1000,""),"")', f'=IF(B{rr}="email",IFERROR(SUMIFS({e1r("email_open")},{crit})/E{rr},""),"")'])
LG4, g4a, g4b = table(ws, r0, 'G4. Toques de la misma comunicación por usuario en el mes × canal, sin cobranza ni transaccional', H, rows, pct_cols=('respuesta', 'apertura email (abiertos / entregados)'), int_cols=('envíos',))
r0 = g4b + 3
def e3(col): return rng('E3', col)
BANDAS3 = ['00', '01-05', '06-10', '11-20', '21-40', '41-80', '081-160', '161-320', '321+']
H = ['banda_msgs (mensajes en el periodo)', 'usuarios', '% usuarios', 'msgs', 'msgs por usuario', 'eventos de baja de email por 100 usuarios', 'usuarios_con_conversion', '% con conversión', 'costo_mxn (Parámetros)', 'costo por usuario', 'msgs_email', 'msgs_whatsapp', 'msgs_whatsapp_entregados']
rows = []
for k, b in enumerate(BANDAS3):
    rr = r0 + 2 + k; cb = f'{e3("banda_msgs")},A{rr}'
    rows.append([b, f'=SUMIFS({e3("usuarios")},{cb})', f'=IFERROR(B{rr}/SUM({e3("usuarios")}),"")', f'=SUMIFS({e3("msgs")},{cb})', f'=IFERROR(D{rr}/B{rr},"")', f'=IFERROR(SUMIFS({e3("bajas_email")},{cb})/B{rr}*100,"")', f'=SUMIFS({e3("usuarios_con_conversion")},{cb})', f'=IFERROR(G{rr}/B{rr},"")',
                 f'=K{rr}*{PB["costo_email"]}+IF({PB["base_wa"]}="entregado",M{rr},L{rr})*{PB["costo_wa"]}', f'=IFERROR(I{rr}/B{rr},"")', f'=SUMIFS({e3("msgs_email")},{cb})', f'=SUMIFS({e3("msgs_whatsapp")},{cb})', f'=SUMIFS({e3("msgs_whatsapp_entregados")},{cb})'])
LG5, g5a, g5b = table(ws, r0, 'G5. Fatiga (E3): bajas y conversión según cuántos mensajes recibió el usuario en los nueve meses. Push e in-app no cuestan; el costo es email y WhatsApp.', H, rows, pct_cols=('% usuarios', '% con conversión'), int_cols=('usuarios', 'msgs', 'costo_mxn (Parámetros)'))
ws.freeze_panes = 'A6'

# ---------- H_Etapas
ws = WS['H_Etapas']
header(ws, 'Lente H. Etapas del usuario (golden record): a quién le llega lo promocional',
       'E7a (envíos por familia × canal × etapa) con equipo y tipo del Catálogo.',
       'La etapa es la del usuario al momento del envío. Solo aparecen 3.Blacklist, 4.Kpay CC Freeze, 6.Reus or Arco, 7.Prospects y sin_golden (sin golden record); cubre 37 % de los envíos de E1. Etapas bloqueadas = Blacklist, CC Freeze y REUS/ARCO: un usuario ahí no debería recibir promoción. E7a queda 0.7 % debajo de E1 por filas sin familia y deduplicación. Tipo = del Catálogo (equipo Collections = cobranza; sin ticket en el nombre = transaccional u operativa).')
def e7(col): return rng('E7a', col)
TIP7 = e7('tipo (derivada)'); ETA7 = e7('etapa'); ENV7 = e7('envios'); EQ7 = e7('equipo (derivada)')
H = ['etapa'] + TIPOS + ['no está en E1', 'total', '% promocional en la etapa', '% de todos los envíos de E7a']
rows = []
for k, et in enumerate(ETAPAS):
    rr = 6 + k
    rows.append([et] + [f'=SUMIFS({ENV7},{ETA7},$A{rr},{TIP7},"{t}")' for t in TIPOS + ['no está en E1']] + [f'=SUM(B{rr}:E{rr})', f'=IFERROR(B{rr}/F{rr},"")', f'=IFERROR(F{rr}/F$11,"")'])
rows.append(['total', '=SUM(B6:B10)', '=SUM(C6:C10)', '=SUM(D6:D10)', '=SUM(E6:E10)', '=SUM(F6:F10)', '=IFERROR(B11/F11,"")', ''])
rows.append(['etapas bloqueadas (3 + 4 + 6)', '=B6+B7+B8', '=C6+C7+C8', '=D6+D7+D8', '=E6+E7+E8', '=F6+F7+F8', '=IFERROR(B12/F12,"")', '=IFERROR(F12/F11,"")'])
LH1, h1a, h1b = table(ws, 4, 'H1. Envíos por etapa × tipo de familia', H, rows, pct_cols=('% promocional en la etapa', '% de todos los envíos de E7a'), int_cols=tuple(TIPOS + ['no está en E1', 'total']))
r0 = h1b + 3
H = ['etapa', 'canal', 'envíos', 'respuestas', 'respuesta', 'bajas_email_eventos', 'bajas por mil envíos (email)', 'envíos promocionales', 'respuestas promocionales', 'respuesta promocional']
rows = []
for et in ETAPAS:
    for cnl in C4:
        rr = r0 + 2 + len(rows); crit = f'{ETA7},A{rr},{e7("canal")},B{rr}'; critp = crit + f',{TIP7},"promocional o lifecycle"'
        rows.append([et, cnl, f'=SUMIFS({ENV7},{crit})', f'=SUMIFS({e7("respuestas")},{crit})', f'=IFERROR(D{rr}/C{rr},"")', f'=SUMIFS({e7("bajas_email_eventos")},{crit})', f'=IF(B{rr}="email",IFERROR(F{rr}/C{rr}*1000,""),"")', f'=SUMIFS({ENV7},{critp})', f'=SUMIFS({e7("respuestas")},{critp})', f'=IFERROR(I{rr}/H{rr},"")'])
LH2, h2a, h2b = table(ws, r0, 'H2. Respuesta por etapa × canal (respuestas = clic email, apertura push, lectura WhatsApp o clic in-app según el canal, como lo trae E7a)', H, rows, pct_cols=('respuesta', 'respuesta promocional'), int_cols=('envíos', 'envíos promocionales'))
r0 = h2b + 3
H = ['equipo', 'envíos promocionales a etapas bloqueadas', '% de los envíos promocionales a bloqueadas', 'envíos promocionales a 7.Prospects', 'envíos promocionales con etapa conocida', '% a prospectos sobre etapa conocida']
rows = []
for k, eq in enumerate(EQUIPOS + ['no está en E1']):
    rr = r0 + 2 + k; base = f'{EQ7},A{rr},{TIP7},"promocional o lifecycle"'
    bl = '+'.join(f'SUMIFS({ENV7},{base},{ETA7},"{et}")' for et in BLOQUEADAS)
    rows.append([eq, f'={bl}', f'=IFERROR(B{rr}/SUM(B${r0 + 2}:B${r0 + 7}),"")', f'=SUMIFS({ENV7},{base},{ETA7},"7.Prospects")', f'=SUMIFS({ENV7},{base})-SUMIFS({ENV7},{base},{ETA7},"sin_golden")', f'=IFERROR(D{rr}/E{rr},"")'])
LH3, h3a, h3b = table(ws, r0, 'H3. Promocional a etapas bloqueadas y a prospectos, por equipo', H, rows, pct_cols=('% de los envíos promocionales a bloqueadas', '% a prospectos sobre etapa conocida'), int_cols=('envíos promocionales a etapas bloqueadas', 'envíos promocionales a 7.Prospects', 'envíos promocionales con etapa conocida'))
r0 = h3b + 3
spill(ws, r0, 'H4. Las 40 familias promocionales con más envíos a etapas bloqueadas (familia × canal × etapa)',
      ['familia', 'canal', 'etapa', 'envíos', 'equipo', 'respuestas', 'ticket'],
      f'=ARRAY_CONSTRAIN(SORT(FILTER({{{e7("familia (derivada)")},{e7("canal")},{ETA7},{ENV7},{EQ7},{e7("respuestas")},ARRAYFORMULA(IFERROR(VLOOKUP({e7("familia (derivada)")},Catálogo!$A$2:$B${NC + 1},2,FALSE),""))}},{TIP7}="promocional o lifecycle",({ETA7}="3.Blacklist")+({ETA7}="4.Kpay CC Freeze")+({ETA7}="6.Reus or Arco")),4,FALSE),40,7)',
      'Qué hacer: excluir estas etapas en el segmento de entrada de cada Canvas promocional (atributo de golden record).')
ws.freeze_panes = 'A6'

# ---------- J_Canal
ws = WS['J_Canal']
header(ws, 'Lente J. A qué canal responde cada usuario y cuánto se le manda por canales a los que nunca respondió',
       'E7b (enero a septiembre) y E9b (julio a septiembre): 16 combinaciones de respondió / no respondió por canal, con usuarios, mensajes, conversiones y bajas.',
       '"Respondió a un canal" = al menos UNA respuesta en el periodo: clic en email, apertura de push, lectura de WhatsApp, clic en in-app. "Ninguno" = recibió mensajes y no tuvo ni una respuesta en ningún canal (puede haber abierto emails sin clic). "Canal mudo" = canal al que ese grupo nunca respondió; sus mensajes por ese canal se cuentan como mensajes a canal mudo. Costo = msgs_email × costo email + WhatsApp (entregado o enviado según Parámetros!B6) × costo WhatsApp. Si el usuario tiene apagadas las confirmaciones de lectura de WhatsApp aparece como no leído: "ninguno" es un techo.')
def j_block(r0, tab, title):
    def t(col): return rng(tab, col)
    def c_(col, r): return f'{tab}!${INFO[tab]["letters"][col]}${r}'
    H = ['responde a', 'resp_email', 'resp_push', 'resp_wa', 'resp_inapp', 'usuarios', '% usuarios', 'msgs totales', '% msgs', 'msgs por usuario', 'costo_mxn', '% costo', 'MXN por usuario', 'usuarios_con_conversion', '% convierten', 'usuarios_con_baja_email', '% baja email',
         'msgs a canal mudo', '% de sus msgs a canal mudo', 'costo de msgs a canal mudo', 'msgs_email', 'msgs_push', 'msgs_wa', 'msgs_wa_entregados', 'msgs_inapp', '% entrega WhatsApp']
    rows = []; n = INFO[tab]['filas']; tot = r0 + 2 + n
    for k in range(n):
        rr = r0 + 2 + k; rs = k + 2
        rows.append([f'=IF(B{rr}+C{rr}+D{rr}+E{rr}=0,"ninguno",TRIM(IF(B{rr}=1,"email ","")&IF(C{rr}=1,"push ","")&IF(D{rr}=1,"WhatsApp ","")&IF(E{rr}=1,"in-app ","")))',
                     f'={c_("resp_email", rs)}', f'={c_("resp_push", rs)}', f'={c_("resp_wa", rs)}', f'={c_("resp_inapp", rs)}', f'={c_("usuarios", rs)}', f'=IFERROR(F{rr}/F${tot},"")',
                     f'=U{rr}+V{rr}+W{rr}+Y{rr}', f'=IFERROR(H{rr}/H${tot},"")', f'=IFERROR(H{rr}/F{rr},"")',
                     f'=U{rr}*{PB["costo_email"]}+IF({PB["base_wa"]}="entregado",X{rr},W{rr})*{PB["costo_wa"]}+V{rr}*{PB["costo_push"]}+Y{rr}*{PB["costo_inapp"]}', f'=IFERROR(K{rr}/K${tot},"")', f'=IFERROR(K{rr}/F{rr},"")',
                     f'={c_("usuarios_con_conversion", rs)}', f'=IFERROR(N{rr}/F{rr},"")', f'={c_("usuarios_con_baja_email", rs)}', f'=IFERROR(P{rr}/F{rr},"")',
                     f'=(1-B{rr})*U{rr}+(1-C{rr})*V{rr}+(1-D{rr})*W{rr}+(1-E{rr})*Y{rr}', f'=IFERROR(R{rr}/H{rr},"")',
                     f'=(1-B{rr})*U{rr}*{PB["costo_email"]}+(1-D{rr})*IF({PB["base_wa"]}="entregado",X{rr},W{rr})*{PB["costo_wa"]}+(1-C{rr})*V{rr}*{PB["costo_push"]}+(1-E{rr})*Y{rr}*{PB["costo_inapp"]}',
                     f'={c_("msgs_email", rs)}', f'={c_("msgs_push", rs)}', f'={c_("msgs_wa", rs)}', f'={c_("msgs_wa_entregados", rs)}', f'={c_("msgs_inapp", rs)}', f'=IFERROR(X{rr}/W{rr},"")'])
    a, b = r0 + 2, r0 + 1 + n
    rows.append(['total', '', '', '', '', f'=SUM(F{a}:F{b})', '', f'=SUM(H{a}:H{b})', '', f'=IFERROR(H{tot}/F{tot},"")', f'=SUM(K{a}:K{b})', '', f'=IFERROR(K{tot}/F{tot},"")', f'=SUM(N{a}:N{b})', f'=IFERROR(N{tot}/F{tot},"")', f'=SUM(P{a}:P{b})', f'=IFERROR(P{tot}/F{tot},"")',
                 f'=SUM(R{a}:R{b})', f'=IFERROR(R{tot}/H{tot},"")', f'=SUM(T{a}:T{b})', f'=SUM(U{a}:U{b})', f'=SUM(V{a}:V{b})', f'=SUM(W{a}:W{b})', f'=SUM(X{a}:X{b})', f'=SUM(Y{a}:Y{b})', f'=IFERROR(X{tot}/W{tot},"")'])
    LJ, ja, jb = table(ws, r0, title, H, rows, pct_cols=('% usuarios', '% msgs', '% costo', '% convierten', '% baja email', '% de sus msgs a canal mudo', '% entrega WhatsApp'), int_cols=('usuarios', 'msgs totales', 'costo_mxn', 'msgs a canal mudo', 'costo de msgs a canal mudo'))
    # resumen
    s0 = jb + 2
    nin = f'SUMIFS(F{a}:F{b},A{a}:A{b},"ninguno")'
    res = [('Usuarios que recibieron algo', f'=F{tot}'),
           ('Usuarios que no respondieron a nada ("ninguno")', f'={nin}'), ('% que no respondieron a nada', f'=IFERROR({nin}/F{tot},"")'),
           ('Mensajes a quienes no respondieron a nada', f'=SUMIFS(H{a}:H{b},A{a}:A{b},"ninguno")'), ('% de los mensajes', f'=IFERROR(SUMIFS(H{a}:H{b},A{a}:A{b},"ninguno")/H{tot},"")'),
           ('Costo de los mensajes a quienes no respondieron a nada', f'=SUMIFS(K{a}:K{b},A{a}:A{b},"ninguno")'), ('% del costo', f'=IFERROR(SUMIFS(K{a}:K{b},A{a}:A{b},"ninguno")/K{tot},"")'),
           ('Mensajes a canal mudo (incluye a los que no responden a nada)', f'=R{tot}'), ('% de los mensajes', f'=IFERROR(R{tot}/H{tot},"")'),
           ('Costo de mensajes a canal mudo', f'=T{tot}'), ('% del costo', f'=IFERROR(T{tot}/K{tot},"")'),
           ('Mensajes a canal mudo de quienes SÍ responden a otro canal', f'=R{tot}-SUMIFS(R{a}:R{b},A{a}:A{b},"ninguno")'), ('Costo de esos mensajes', f'=T{tot}-SUMIFS(T{a}:T{b},A{a}:A{b},"ninguno")'),
           ('Emails a usuarios que responden a otro canal pero nunca hicieron clic en un email', f'=SUMIFS(U{a}:U{b},B{a}:B{b},0)-SUMIFS(U{a}:U{b},A{a}:A{b},"ninguno")'),
           ('Usuarios en esa situación', f'=SUMIFS(F{a}:F{b},B{a}:B{b},0)-{nin}'),
           ('WhatsApp entregados a usuarios que responden a otro canal pero nunca leyeron un WhatsApp', f'=SUMIFS(X{a}:X{b},D{a}:D{b},0)-SUMIFS(X{a}:X{b},A{a}:A{b},"ninguno")'),
           ('Push a usuarios que responden a otro canal pero nunca abrieron un push', f'=SUMIFS(V{a}:V{b},C{a}:C{b},0)-SUMIFS(V{a}:V{b},A{a}:A{b},"ninguno")'),
           ('% entrega WhatsApp entre quienes no respondieron a nada', f'=IFERROR(SUMIFS(X{a}:X{b},A{a}:A{b},"ninguno")/SUMIFS(W{a}:W{b},A{a}:A{b},"ninguno"),"")'),
           ('% entrega WhatsApp entre quienes sí leen WhatsApp', f'=IFERROR(SUMIFS(X{a}:X{b},D{a}:D{b},1)/SUMIFS(W{a}:W{b},D{a}:D{b},1),"")')]
    ws.cell(s0, 1, 'Resumen').font = bold
    for k, (lab, f) in enumerate(res):
        ws.cell(s0 + 1 + k, 1, lab); cc = ws.cell(s0 + 1 + k, 2, f); cc.number_format = '0.00%' if lab.startswith('%') else '#,##0'
    return LJ, ja, jb, tot, s0, {lab: s0 + 1 + k for k, (lab, _) in enumerate(res)}
LJ7, j7a, j7b, J7TOT, j7s, J7RES = j_block(4, 'E7b', 'J1. Enero a septiembre (E7b)')
LJ9, j9a, j9b, J9TOT, j9s, J9RES = j_block(j7s + 24, 'E9b', 'J2. Julio a septiembre, ventana de 90 días (E9b). Solo cuentan respuestas y mensajes del trimestre: un clic de enero ya no rescata a nadie.')
ws.freeze_panes = 'B6'

# ---------- K_Abren
ws = WS['K_Abren']
header(ws, 'Lente K. Convierten los que abren contra los que no abren (por campaña)',
       'Campañas (columnas de E7c agregadas por familia × canal), Medianas.',
       'E7c cuenta usuario-días: "abrieron" = usuario-días con apertura (email), apertura (push), lectura (WhatsApp) o impresión con clic (in-app). conv_abren = convirtieron entre los que abrieron; conv_no_abren = entre los que no. lift = conv_abren / conv_no_abren: si es cercano a 1, abrir el mensaje no cambia la conversión (el mensaje no mueve). Solo se juzga con muestra suficiente (Parámetros filas 17 a 19). La conversión es de referencia (is_converted poco confiable, solo Cash): aquí se usa para comparar grupos dentro de la misma campaña, no para atribuir.')
H = ['canal', 'familias en Campañas', 'familias con muestra suficiente', 'mediana conv_abren (con muestra)', 'mediana conv_no_abren (con muestra)', 'mediana lift (con muestra)', 'familias con muestra y lift < lift mínimo', 'familias con muestra donde ni quien abre convierte (conv_abren < mediana / 2)', 'familias con muestra que sí mueven (mueve = 1)', 'familias con muestra que no mueven', 'abrieron (suma)', 'no_abrieron (suma)']
rows = []
for k, cnl in enumerate(C4):
    rr = 6 + k; A = f'$A{rr}'
    rows.append([cnl, f'=COUNTIF({cr("canal")},{A})', f'=COUNTIFS({cr("canal")},{A},{cr("muestra_ok")},1)', '=' + med_lookup(A, 'mediana conv_abren (con muestra)'),
                 median_filter(cr('conv_no_abren'), cr('canal'), A, extra_num=cr('conv_no_abren'), extra_flag=cr('muestra_ok'), cellref=f'E{rr}'),
                 median_filter(cr('lift'), cr('canal'), A, extra_num=cr('lift'), extra_flag=cr('muestra_ok'), cellref=f'F{rr}'),
                 f'=COUNTIFS({cr("canal")},{A},{cr("muestra_ok")},1,{cr("lift")},"<"&{PB["lift"]})', f'=COUNTIFS({cr("canal")},{A},{cr("muestra_ok")},1,{cr("conv_abren")},"<"&D{rr}/2)',
                 f'=COUNTIFS({cr("canal")},{A},{cr("muestra_ok")},1,{cr("mueve")},1)', f'=COUNTIFS({cr("canal")},{A},{cr("muestra_ok")},1,{cr("mueve")},0)', f'=SUMIFS({cr("abrieron (E7c)")},{cr("canal")},{A})', f'=SUMIFS({cr("no_abrieron (E7c)")},{cr("canal")},{A})'])
LK1, k1a, k1b = table(ws, 4, 'K1. Por canal', H, rows, pct_cols=('mediana conv_abren (con muestra)', 'mediana conv_no_abren (con muestra)'), int_cols=('abrieron (suma)', 'no_abrieron (suma)'))
r0 = k1b + 3
spill(ws, r0, 'K2. Familias con muestra suficiente donde abrir casi no cambia la conversión (lift < lift mínimo), de mayor a menor por usuarios que abrieron',
      ['familia', 'canal', 'equipo', 'tipo', 'abrieron', 'conv_abren', 'conv_no_abren', 'lift', 'respuesta', 'señal', 'accion_tipo', 'ticket'],
      f'=SORT(FILTER({{{cr("familia")},{cr("canal")},{cr("equipo")},{cr("tipo")},{cr("abrieron (E7c)")},{cr("conv_abren")},{cr("conv_no_abren")},{cr("lift")},{cr("respuesta")},{cr("señal")},{cr("accion_tipo")},{cr("ticket")}}},{cr("muestra_ok")}=1,ISNUMBER({cr("lift")}),{cr("lift")}<{PB["lift"]}),5,FALSE)',
      'Qué hacer: en estas familias el mensaje no está moviendo la conversión; si además la respuesta está debajo del mínimo, apagar en vez de rehacer.')
ws.freeze_panes = 'A6'

# ---------- L_Baja
ws = WS['L_Baja']
header(ws, 'Lente L. En cuántos días se dan de baja y cuántos emails recibieron antes',
       'E8 (bloques resumen, banda_dias, banda_emails y familia_dia_baja) con equipo y tipo del Catálogo.',
       'Cohorte 1 (limpia) = el primer email del usuario cae dentro del periodo: días y emails exactos. Cohorte 0 = ya recibía antes de enero: días y emails medidos desde enero, son un piso. "Familia del día de la baja" = la familia que le llegó el último día con email entregado antes de la baja o ese mismo día; si ese día recibió dos familias cuenta en las dos (por eso la suma pasa de 100 %). Cubre 91 % de los usuarios únicos con baja (E5). Promedios y medianas vienen de la query (PERCENTILE_APPROX).')
def e8c(col): return rng('E8', col)
BLQ = e8c('bloque'); CLV = e8c('clave'); COH = e8c('cohorte_limpia'); USR8 = e8c('usuarios')
def s8(col, bloque, clave_ref, coh): return f'SUMIFS({e8c(col)},{BLQ},"{bloque}",{CLV},{clave_ref},{COH},{coh})'
# Para familia_dia_baja la clave se cruza por la columna familia (derivada), que convierte la clave vacía (null) en "(sin nombre)".
def s8f(col, clave_ref, coh): return f'SUMIFS({e8c(col)},{BLQ},"familia_dia_baja",{e8c("familia (derivada)")},{clave_ref},{COH},{coh})'
H = ['cohorte_limpia', 'qué es', 'usuarios', 'dias_prom', 'dias_mediana', 'dias_p90', 'emails_prom', 'emails_mediana', 'familias_prom', '% de los usuarios únicos con baja (E5)']
rows = []
for k, (coh, lab) in enumerate([(1, 'primer email dentro del periodo (nuevos)'), (0, 'ya recibía email antes de enero')]):
    rr = 6 + k
    rows.append([coh, lab] + [f'={s8(col, "resumen", chr(34) + "todos" + chr(34), f"$A{rr}")}' for col in ['usuarios', 'dias_prom', 'dias_mediana', 'dias_p90', 'emails_prom', 'emails_mediana', 'familias_prom']] + [f'=IFERROR(C{rr}/SUM({rng("E5","usuarios_baja")}),"")'])
rows.append(['ambas', '', '=C6+C7', '', '', '', '', '', '', '=IFERROR(C8/SUM(' + rng('E5', 'usuarios_baja') + '),"")'])
LL1, l1a, l1b = table(ws, 4, 'L1. Resumen por cohorte (E8 bloque resumen)', H, rows, pct_cols=('% de los usuarios únicos con baja (E5)',), int_cols=('usuarios',))
L_COH_ROW = {1: 6, 0: 7}
r0 = l1b + 3
BD = ['0 mismo día', '1 a 7', '08 a 30', '31 a 90', '91 a 180', '181+']
H = ['banda_dias (días desde el primer email)', 'cohorte_limpia', 'usuarios', '% de la cohorte', '% acumulado', 'emails_prom', 'emails_mediana', 'familias_prom']
rows = []
for coh in (1, 0):
    for k, b in enumerate(BD):
        rr = r0 + 2 + len(rows); first_r = r0 + 2 + (0 if coh == 1 else len(BD))
        rows.append([b, coh, f'={s8("usuarios", "banda_dias", f"$A{rr}", f"$B{rr}")}', f'=IFERROR(C{rr}/$C${L_COH_ROW[coh]},"")', f'=SUM(D${first_r}:D{rr})', f'={s8("emails_prom", "banda_dias", f"$A{rr}", f"$B{rr}")}', f'={s8("emails_mediana", "banda_dias", f"$A{rr}", f"$B{rr}")}', f'={s8("familias_prom", "banda_dias", f"$A{rr}", f"$B{rr}")}'])
LL2, l2a, l2b = table(ws, r0, 'L2. Días hasta la baja por cohorte', H, rows, pct_cols=('% de la cohorte', '% acumulado'), int_cols=('usuarios',))
r0 = l2b + 3
BE_ = ['01', '02 a 3', '04 a 10', '11 a 30', '31+']
H = ['banda_emails (emails antes de la baja)', 'cohorte_limpia', 'usuarios', '% de la cohorte', '% acumulado', 'dias_prom', 'dias_mediana', 'familias_prom']
rows = []
for coh in (1, 0):
    for k, b in enumerate(BE_):
        rr = r0 + 2 + len(rows); first_r = r0 + 2 + (0 if coh == 1 else len(BE_))
        rows.append([b, coh, f'={s8("usuarios", "banda_emails", f"$A{rr}", f"$B{rr}")}', f'=IFERROR(C{rr}/$C${L_COH_ROW[coh]},"")', f'=SUM(D${first_r}:D{rr})', f'={s8("dias_prom", "banda_emails", f"$A{rr}", f"$B{rr}")}', f'={s8("dias_mediana", "banda_emails", f"$A{rr}", f"$B{rr}")}', f'={s8("familias_prom", "banda_emails", f"$A{rr}", f"$B{rr}")}'])
LL3, l3a, l3b = table(ws, r0, 'L3. Emails recibidos antes de la baja por cohorte', H, rows, pct_cols=('% de la cohorte', '% acumulado'), int_cols=('usuarios',))
r0 = l3b + 3
e8 = E['E8']; fdb = e8[e8.bloque == 'familia_dia_baja'].copy(); fdb['clave'] = canon(fdb.clave.replace({'null': '(sin nombre)', '': '(sin nombre)'})); fdb['u'] = pd.to_numeric(fdb.usuarios); fdb['c'] = fdb.cohorte_limpia.astype(int)
fdb = fdb.sort_values(['c', 'u'], ascending=[False, False])
H = ['familia del día de la baja', 'cohorte_limpia', 'ticket', 'equipo', 'tipo', 'usuarios', '% de la cohorte', 'dias_mediana', 'dias_prom', 'emails_prom', 'familias_prom']
rows = []
for k, (_, fr) in enumerate(fdb.iterrows()):
    rr = r0 + 2 + k
    rows.append([fr.clave, fr.c, '=' + cat_lookup(f'$A{rr}', 'ticket'), '=' + cat_lookup(f'$A{rr}', 'equipo'), '=' + cat_lookup(f'$A{rr}', 'tipo'), f'={s8f("usuarios", f"$A{rr}", f"$B{rr}")}',
                 f'=IFERROR(F{rr}/IF($B{rr}=1,$C${L_COH_ROW[1]},$C${L_COH_ROW[0]}),"")', f'={s8f("dias_mediana", f"$A{rr}", f"$B{rr}")}', f'={s8f("dias_prom", f"$A{rr}", f"$B{rr}")}', f'={s8f("emails_prom", f"$A{rr}", f"$B{rr}")}', f'={s8f("familias_prom", f"$A{rr}", f"$B{rr}")}'])
LL4, l4a, l4b = table(ws, r0, 'L4. Familia que llegó el día de la baja (cohorte 1 primero, de mayor a menor). Las claves son estáticas: si se recarga E8, pegar aquí las claves nuevas. "(sin nombre)" = fila de E8 con clave vacía (null en la query): la comunicación sin nombre de E1.', H, rows, pct_cols=('% de la cohorte',), int_cols=('usuarios',))
L4R = lambda col: trng(ws, LL4, col, l4a, l4b)
r0 = l4b + 3
H = ['equipo', 'cohorte_limpia', 'bajas (usuarios, con doble conteo)', '% de la cohorte', 'familias en la lista']
rows = []
for coh in (1, 0):
    for eq in EQUIPOS + ['no está en E1']:
        rr = r0 + 2 + len(rows)
        rows.append([eq, coh, f'=SUMIFS({L4R("usuarios")},{L4R("equipo")},A{rr},{L4R("cohorte_limpia")},B{rr})', f'=IFERROR(C{rr}/IF(B{rr}=1,$C${L_COH_ROW[1]},$C${L_COH_ROW[0]}),"")', f'=COUNTIFS({L4R("equipo")},A{rr},{L4R("cohorte_limpia")},B{rr})'])
LL5, l5a, l5b = table(ws, r0, 'L5. Por equipo y cohorte (suma de L4; pasa de 100 % por el doble conteo)', H, rows, pct_cols=('% de la cohorte',), int_cols=('bajas (usuarios, con doble conteo)',))
r0 = l5b + 3
H = ['tipo', 'cohorte_limpia', 'bajas (usuarios, con doble conteo)', '% de la cohorte', 'familias en la lista']
rows = []
for coh in (1, 0):
    for t in TIPOS + ['no está en E1']:
        rr = r0 + 2 + len(rows)
        rows.append([t, coh, f'=SUMIFS({L4R("usuarios")},{L4R("tipo")},A{rr},{L4R("cohorte_limpia")},B{rr})', f'=IFERROR(C{rr}/IF(B{rr}=1,$C${L_COH_ROW[1]},$C${L_COH_ROW[0]}),"")', f'=COUNTIFS({L4R("tipo")},A{rr},{L4R("cohorte_limpia")},B{rr})'])
LL6, l6a, l6b = table(ws, r0, 'L6. Por tipo de familia y cohorte', H, rows, pct_cols=('% de la cohorte',), int_cols=('bajas (usuarios, con doble conteo)',))
ws.freeze_panes = 'A6'

# ---------- M_Ventanas
ws = WS['M_Ventanas']
header(ws, 'Lente M. Abren contra no abren con ventanas de conversión a 7, 30, 90 días y fin de periodo',
       'E9a (familia × canal, ya sin fecha en el nombre), Catálogo, Parámetros (muestra mínima y lift mínimo).',
       'Misma lógica que K pero la conversión se cuenta dentro de 7, 30 o 90 días después del envío, o hasta el fin del periodo. Un lift que cae al alargar la ventana dice que la conversión iba a pasar de todos modos. Muestra suficiente = abrieron y no abrieron por arriba de Parámetros filas 17 y 18, y conversiones a 90 días por arriba de la fila 19. Conversión de referencia (is_converted), para comparar grupos, no para atribuir.')
e9 = E['E9a']; e9k = pd.DataFrame(dict(fam=canon(fam_pd(e9.familia)), canal=e9.canal, env=num('E9a', 'envios_usuario_dia'))).sort_values(['env', 'fam'], ascending=[False, True])
def e9r(col): return rng('E9a', col)
H = ['familia', 'canal', 'ticket', 'equipo', 'tipo', 'envios_usuario_dia', 'abrieron', 'no_abrieron', 'conv_abren_7', 'conv_no_abren_7', 'lift_7', 'conv_abren_30', 'conv_no_abren_30', 'lift_30', 'conv_abren_90', 'conv_no_abren_90', 'lift_90', 'conv_abren_fin', 'conv_no_abren_fin', 'lift_fin', 'muestra_ok']
rows = []
for k, (_, fr) in enumerate(e9k.iterrows()):
    rr = 6 + k; K9 = f'{e9r("familia (derivada)")},$A{rr},{e9r("canal")},$B{rr}'
    row = [fr.fam, fr.canal, '=' + cat_lookup(f'$A{rr}', 'ticket'), '=' + cat_lookup(f'$A{rr}', 'equipo'), '=' + cat_lookup(f'$A{rr}', 'tipo'), f'=SUMIFS({e9r("envios_usuario_dia")},{K9})', f'=SUMIFS({e9r("abrieron")},{K9})', f'=F{rr}-G{rr}']
    cols = 'IJKLMNOPQRST'
    for i_, w in enumerate(['7', '30', '90', 'fin']):
        ca, cn, cl = cols[i_ * 3], cols[i_ * 3 + 1], cols[i_ * 3 + 2]
        row += [f'=IF(G{rr}>0,SUMIFS({e9r("ab_conv_" + w)},{K9})/G{rr},"")', f'=IF(H{rr}>0,SUMIFS({e9r("no_conv_" + w)},{K9})/H{rr},"")', f'=IF(AND(ISNUMBER({ca}{rr}),ISNUMBER({cn}{rr})),IF({cn}{rr}>0,{ca}{rr}/{cn}{rr},""),"")']
    row.append(f'=IF(AND(G{rr}>={PB["m_ab"]},H{rr}>={PB["m_noab"]},SUMIFS({e9r("ab_conv_90")},{K9})+SUMIFS({e9r("no_conv_90")},{K9})>={PB["m_conv"]}),1,0)')
    rows.append(row)
LM1, m1a, m1b = table(ws, 4, 'M1. Por familia × canal (claves estáticas de E9a, de mayor a menor por envíos)', H, rows, pct_cols=tuple(h for h in H if h.startswith('conv_')), int_cols=('envios_usuario_dia', 'abrieron', 'no_abrieron'))
INFO['M_Ventanas'] = dict(filas=len(rows), letters=LM1, cols=H, first=m1a, last=m1b)
MR = lambda col: trng(ws, LM1, col, m1a, m1b)
r0 = m1b + 3
H = ['canal', 'familias', 'familias con muestra', 'mediana lift_7', 'mediana lift_30', 'mediana lift_90', 'mediana lift_fin', 'familias con muestra y lift_90 < lift mínimo', 'mediana conv_abren_90 (con muestra)', 'mediana conv_no_abren_90 (con muestra)']
rows = []
for k, cnl in enumerate(C4):
    rr = r0 + 2 + k; A = f'$A{rr}'
    rows.append([cnl, f'=COUNTIF({MR("canal")},{A})', f'=COUNTIFS({MR("canal")},{A},{MR("muestra_ok")},1)'] +
                [median_filter(MR(f'lift_{w}'), MR('canal'), A, extra_num=MR(f'lift_{w}'), extra_flag=MR('muestra_ok'), cellref=f'{L(4 + i_)}{rr}') for i_, w in enumerate(['7', '30', '90', 'fin'])] +
                [f'=COUNTIFS({MR("canal")},{A},{MR("muestra_ok")},1,{MR("lift_90")},"<"&{PB["lift"]})',
                 median_filter(MR('conv_abren_90'), MR('canal'), A, extra_num=MR('conv_abren_90'), extra_flag=MR('muestra_ok'), cellref=f'I{rr}'), median_filter(MR('conv_no_abren_90'), MR('canal'), A, extra_num=MR('conv_no_abren_90'), extra_flag=MR('muestra_ok'), cellref=f'J{rr}')])
LM2, m2a, m2b = table(ws, r0, 'M2. Por canal: cómo cambia el lift al alargar la ventana', H, rows, pct_cols=('mediana conv_abren_90 (con muestra)', 'mediana conv_no_abren_90 (con muestra)'))
ws.freeze_panes = 'A6'

# =====================================================================================
# ---------- v3: Estándares, Insights, Plan_accion, Vista_equipo
# =====================================================================================
def cs(col, eq=None):
    """Suma de una columna de Campañas, total o del equipo eq (referencia de celda o texto entre comillas)."""
    return f'SUM({cr(col)})' if eq is None else f'SUMIFS({cr(col)},{cr("equipo")},{eq})'
def ratio(numcol, dencol, mult=''):
    return lambda eq: f'IFERROR({cs(numcol, eq)}/{cs(dencol, eq)}{mult},"")'
NOEQ = 'no se parte por equipo'
DEF = 'Válido con los parámetros default. Si cambias Parámetros (mínimos, factores, muestra), esta fila sale REVISAR a propósito: el valor esperado está fijo con los defaults.'
CATA = f'Catálogo!$A$2:$A${NC + 1}'
def catc(col): return f'Catálogo!${CL[col]}$2:${CL[col]}${NC + 1}'
SEL = 'Vista_equipo!$B$2'

# ---------- Estándares
ws = WS['Estándares']
header(ws, 'Estándares y buenas prácticas: qué es cada métrica, dónde estamos, qué estándar y qué hacer',
       'Campañas (sumas de E1 por familia × canal con el equipo del Catálogo), B_Canales (E4b), F_Solape (E6a), E_DespuesBaja (E5, E5b), H_Etapas (E7a), J_Canal (E7b), L_Baja (E8), Catálogo, Parámetros.',
       'El valor actual es fórmula viva. El estándar propuesto (columna G) es editable: sale de benchmarks públicos de la industria (se toma el piso del rango), de Parámetros o de una propuesta interna; la columna I dice de dónde. Estado = compara el valor actual con el estándar en el sentido de la columna H. Las columnas por equipo (P a T) usan el equipo del Catálogo (mapeo de Parámetros); las métricas que vienen por usuario (E4b, E6a, E7b, E8 resumen) no se parten por equipo. Benchmarks: email promocional apertura 15 a 25 %, clic 1.5 a 3 %, baja menor a 0.3 %; push apertura 3 a 10 %; WhatsApp lectura 70 a 90 %, entrega mayor a 90 %; in-app clic 5 a 20 % (METRICAS.md). Son referencia, no juicio final: una audiencia fría responde menos por ser fría.')
EST_COLS = ['#', 'tema', 'métrica u operación', 'qué es', 'cómo se calcula aquí', 'valor actual (todos los equipos)', 'estándar propuesto (editable)', 'sentido', 'de dónde sale el estándar', 'brecha (actual − estándar)', 'estado', 'qué significa quedarse debajo', 'qué hacer', 'fuente (E)', 'supuestos'] + EQUIPOS + ['equipos debajo del estándar']
EL = {c: L(j) for j, c in enumerate(EST_COLS, start=1)}
SUP_CAMP = 'Sumas de E1 por familia × canal (Campañas). Equipo = del Catálogo con el mapeo de Parámetros.'
def h3_eq(eq): return f'IFERROR(INDEX(H_Etapas!$B${h3a}:$B${h3a + 4},MATCH({eq},H_Etapas!$A${h3a}:$A${h3a + 4},0)),"")'
def e3_eq(eq): return f'IFERROR(INDEX(E_DespuesBaja!$E${e3a}:$E${e3a + 4},MATCH({eq},E_DespuesBaja!$A${e3a}:$A${e3a + 4},0)),"")'
def l5_eq(eq): return f'IFERROR(INDEX(L_Baja!$C${l5a}:$C${l5a + 4},MATCH({eq},L_Baja!$A${l5a}:$A${l5a + 4},0)),"")'
# (tema, métrica, qué es, cómo, f(eq) o texto, estándar, sentido, de dónde, significa, hacer, fuente, supuestos, formato)
EST = [
 ('Entrega', 'Entrega de email (entregados / enviados)', 'Qué parte de los emails enviados llegó a una bandeja.', 'SUM(email_delivery) / SUM(email_sent) de Campañas', ratio('email_delivery', 'email_sent'), 0.95, 'mayor es mejor',
  'Benchmark de industria: 95 % o más. Debajo hay lista sucia o problema de reputación del dominio.', 'Rebotes: direcciones inválidas o dominio con mala reputación. Se paga por enviado (Parámetros B2): cada punto debajo es dinero en correos que no llegan y además baja la entrega de todos los equipos.', 'Quitar hard bounces y direcciones sin apertura en 12 meses; revisar SPF, DKIM y DMARC; no comprar ni importar listas.', 'E1', SUP_CAMP, 'pct'),
 ('Email', 'Apertura de email (abiertos / entregados)', 'Qué parte de los emails entregados se abrió. Solo referencia: Apple Mail y Gmail abren solos.', 'SUM(email_open) / SUM(email_delivery) de Campañas', ratio('email_open', 'email_delivery'), 0.15, 'mayor es mejor',
  'Benchmark promocional 15 a 25 % (piso). Inflado por aperturas automáticas: no se usa como señal, por eso la respuesta de email es el clic.', 'Asunto o remitente que no llaman; o la métrica está inflada y el clic dirá la verdad.', 'Probar asunto y preheader con prueba del 10 %; leer siempre junto con el clic.', 'E1', SUP_CAMP + ' Apertura inflada por Apple Mail Privacy Protection y Gmail.', 'pct'),
 ('Email', 'Clic de email (clics / entregados) = respuesta email', 'Qué parte de los emails entregados tuvo clic. Es la respuesta que usa toda la auditoría en email.', 'SUM(email_click) / SUM(email_delivery) de Campañas', ratio('email_click', 'email_delivery'), 0.015, 'mayor es mejor',
  'Benchmark promocional 1.5 a 3 % (piso). El mínimo interno para apagar es más bajo: Parámetros B11 (0.3 %); el estándar es la meta, el mínimo es el piso.', 'El contenido o la audiencia no interesan. Debajo del mínimo interno la campaña no tiene señal y se apaga o se rehace (Campañas, señal).', 'Plan_accion: Apagar las que no mueven, Rehacer o re-segmentar las que sí; probar oferta y asunto al 10 % antes del envío completo.', 'E1', SUP_CAMP, 'pct'),
 ('Email', 'Bajas por mil emails entregados', 'Cuántos eventos de baja (email_unsubscribe) hay por cada mil emails entregados.', 'SUM(email_unsubscribe) / SUM(email_delivery) × 1000 de Campañas', ratio('email_unsubscribe', 'email_delivery', '*1000'), f'={PB["bajas_mil"]}', 'menor es mejor',
  'Parámetros B26 (2.5 por mil). Benchmark de industria: menos de 3 por mil (0.3 %) en promocional.', 'Cada baja es un usuario que no vuelve a recibir NINGÚN email, también los útiles. Arriba del estándar la lista se desgasta más rápido de lo que crece.', 'Bajar frecuencia (Plan_accion), cuidar los primeros emails del usuario nuevo (L_Baja) y no mandar promocional a quien ya se dio de baja (E_DespuesBaja).', 'E1', SUP_CAMP + ' Eventos, no usuarios: un usuario puede generar varios eventos de baja.', 'num2'),
 ('Push', 'Apertura de push (aperturas / enviados) = respuesta push', 'Qué parte de los push enviados se abrió.', 'SUM(pn_open) / SUM(pn_send) de Campañas', ratio('pn_open', 'pn_send'), 0.03, 'mayor es mejor',
  'Benchmark 3 a 10 % de apertura directa (piso). Mínimo interno Parámetros B12 (0.75 %).', 'Un push que nadie abre gasta el permiso del usuario: desactiva las notificaciones y se pierde el canal, que no cuesta dinero pero sí atención.', 'Tope de 1 push promocional al día por usuario; apagar las familias con señal apagar; disparar por evento del usuario y no a toda la base.', 'E1', SUP_CAMP + ' Push no tiene entrega ni baja en la tabla.', 'pct'),
 ('WhatsApp', 'Entrega de WhatsApp (entregados / enviados)', 'Qué parte de los WhatsApp enviados llegó al teléfono.', 'SUM(whatsapp_delivery) / SUM(whatsapp_send) de Campañas', ratio('whatsapp_delivery', 'whatsapp_send'), 0.90, 'mayor es mejor',
  'Benchmark: más de 90 % de entrega. Meta cobra por entregado (Parámetros B6), pero el no entregado marca la base como sucia y, si se cobrara por enviado, costaría lo de la columna wa_no_entregado_mxn.', 'Números inválidos, sin WhatsApp o que bloquearon a la empresa. Debajo de 90 % la base necesita limpieza.', 'Limpiar base de WhatsApp (Plan_accion): quitar números con 3 no-entregas seguidas; verificar el número antes de meterlo al Canvas.', 'E1', SUP_CAMP, 'pct'),
 ('WhatsApp', 'Lectura de WhatsApp (leídos / entregados) = respuesta WhatsApp', 'Qué parte de los WhatsApp entregados se leyó.', 'SUM(whatsapp_read) / SUM(whatsapp_delivery) de Campañas', ratio('whatsapp_read', 'whatsapp_delivery'), 0.70, 'mayor es mejor',
  'Benchmark 70 a 90 % de lectura (piso). Mínimo interno Parámetros B13 (60 %).', 'Un WhatsApp entregado y no leído cuesta 1 MXN y no sirve. Si el usuario tiene apagadas las confirmaciones de lectura cuenta como no leído: la cifra es un piso.', 'Mandar WhatsApp solo a quien ya leyó uno antes (J_Canal) y en horario de respuesta; plantillas cortas y con una sola acción.', 'E1', SUP_CAMP + ' Confirmaciones de lectura apagadas cuentan como no leído.', 'pct'),
 ('In-app', 'Clic de in-app (clics / impresiones) = respuesta in-app', 'Qué parte de las impresiones de la pieza dentro de la app tuvo clic.', 'SUM(in_app_click) / SUM(in_app_impression) de Campañas', ratio('in_app_click', 'in_app_impression'), f'={PB["inapp_quitar"]}', 'mayor es mejor',
  'Parámetros B20 (5 %). Benchmark 5 a 20 % sobre impresiones.', 'La pieza estorba dentro de la app sin que nadie la toque.', 'Quitar la pieza o cambiar el disparador; una sola pieza in-app por sesión.', 'E1', SUP_CAMP, 'pct'),
 ('Frecuencia', 'Toques de la misma comunicación por usuario al mes (envíos / usuarios del mes)', 'Cuántas veces al mes le llega la misma comunicación al mismo usuario, en promedio.', 'SUM(envíos) / SUM(usuarios_aprox) de Campañas', ratio('envíos', 'usuarios_aprox (suma de filas con envíos)'), 2, 'menor es mejor',
  'Propuesta interna (lente G4): con 1 o 2 toques la respuesta se mantiene; de 3 en adelante cae y suben las bajas. Regla: máximo 2 toques de la misma comunicación por usuario al mes.', 'La misma pieza llega 3, 4 o 5 veces al mismo usuario en el mes: fatiga sin respuesta extra.', 'Frequency cap por Canvas: 2 por usuario por mes; re-entrada bloqueada 30 días.', 'E1', 'usuarios_aprox es APPROX_COUNT_DISTINCT del mes (error 1 a 2 %). Incluye cobranza y transaccional.', 'num2'),
 ('Frecuencia', 'Mensajes por usuario al mes, todos los canales (E4b)', 'Mensajes que recibe un usuario en un mes, promedio sobre los usuarios con al menos una fila.', 'SUM(msgs totales) / SUM(usuarios con fila) de B_Canales B3 (9 meses)', f'IFERROR(SUM(B_Canales!$L${b3a}:$L${b3b})/SUM(B_Canales!$B${b3a}:$B${b3b}),"")', 20, 'menor es mejor',
  'Umbral de presión de METRICAS: 5 mensajes por semana promocional + lifecycle, unos 20 al mes. Aquí se cuentan todos los canales y tipos, así que es un techo.', 'Arriba de 20 el usuario recibe casi un mensaje diario. La banda 41+ tiene más bajas por 100 usuarios que la banda 01-05 (B_Canales B3).', 'Tope global de frecuencia en Braze (frequency capping) por usuario: 5 a la semana promocional; transaccional y cobranza fuera del tope.', 'E4b', NOEQ + ' (E4b es por usuario). Incluye push e in-app, que no cuestan.', 'num2'),
 ('Frecuencia', '% de usuarios con 41 o más mensajes al mes (E4b)', 'Qué parte de los usuarios con mensajes en el mes está en las bandas 41-80, 081-160 y 161+.', 'SUM(bandas 41+) / SUM(usuarios con fila) de B_Canales B3', f'IFERROR(SUM(B_Canales!$H${b3a}:$J${b3b})/SUM(B_Canales!$B${b3a}:$B${b3b}),"")', 0.05, 'menor es mejor',
  'Propuesta interna: la cola de usuarios saturados no debería pasar del 5 %.', 'Hay un grupo que recibe más de un mensaje al día; concentra bajas y quejas.', 'Frequency cap global y revisar qué Canvas se acumulan en esos usuarios (F_Solape F4).', 'E4b', NOEQ + ' (E4b es por usuario).', 'pct'),
 ('Solapamiento', '% de usuario-días con 3 o más familias distintas el mismo día (E6a)', 'De los días en que un usuario recibe algo, en qué parte le llegan 3 o más campañas distintas.', '(F_Solape B8 + B9 + B10) / B11', 'IFERROR((F_Solape!$B$8+F_Solape!$B$9+F_Solape!$B$10)/F_Solape!$B$11,"")', 0.10, 'menor es mejor',
  'Propuesta interna (METRICAS: solapamiento = 3 o más campañas distintas el mismo día). Regla: máximo 2 familias por usuario por día.', 'Varios equipos le hablan al mismo usuario el mismo día; las bajas por mil usuario-días suben con las familias del día (F_Solape F1).', 'Exclusión mutua entre Canvas promocionales (no enviar si recibió otro promocional en 24 h); calendario único entre equipos; los pares que más chocan están en F_Solape F4.', 'E6a', NOEQ + ' (E6a es por usuario-día). Grano usuario-día.', 'pct'),
 ('Bajas', 'Días hasta la baja, mediana, usuarios nuevos (E8 cohorte 1)', 'Cuántos días pasan entre el primer email del usuario y su baja (mediana), para usuarios cuyo primer email cae en el periodo.', 'L_Baja E6', 'L_Baja!$E$6', 90, 'mayor es mejor',
  'Propuesta interna: un usuario nuevo debería durar al menos 90 días suscrito.', 'Se dan de baja en el primer mes: la secuencia de bienvenida quema la lista que acaba de entrar.', 'Revisar los primeros 5 emails del usuario nuevo (orden y frecuencia); la familia que llegó el día de la baja está en L_Baja L4.', 'E8', NOEQ + ' (E8 resumen es por usuario). PERCENTILE_APPROX.', 'num0'),
 ('Bajas', 'Emails recibidos antes de la baja, mediana, usuarios nuevos (E8 cohorte 1)', 'Cuántos emails recibió el usuario nuevo antes de darse de baja (mediana).', 'L_Baja H6', 'L_Baja!$H$6', 10, 'mayor es mejor',
  'Propuesta interna: si se van con menos de 10 emails no es cansancio acumulado, es el contenido o la audiencia de los primeros envíos.', 'La baja llega con pocos emails: el problema está en los primeros mensajes, no en la frecuencia.', 'Rediseñar la secuencia de los primeros 10 emails; empezar por lo útil (transaccional, educación) antes de lo promocional.', 'E8', NOEQ + ' (E8 resumen es por usuario). PERCENTILE_APPROX.', 'num0'),
 ('Bajas', '% de usuarios nuevos que se dan de baja el mismo día del primer email (E8 cohorte 1)', 'De los usuarios nuevos con baja, qué parte se dio de baja el mismo día en que recibió su primer email.', f'L_Baja D{l2a} (banda 0 mismo día, cohorte 1)', f'L_Baja!$D${l2a}', 0.05, 'menor es mejor',
  'Propuesta interna.', 'El primer email ya los echó: audiencia que no pidió el correo (leads, registros sin crédito) o asunto que no corresponde.', 'Confirmación de interés antes del primer promocional; no meter leads fríos a la secuencia de bienvenida; probar el primer email al 10 %.', 'E8', NOEQ + ' (E8 banda_dias es por usuario).', 'pct'),
 ('Canal mudo', '% de mensajes a canal mudo (canal al que ese usuario nunca respondió, E7b enero a septiembre)', 'De todos los mensajes del periodo, qué parte fue por un canal al que el usuario nunca respondió (ni un clic, apertura o lectura en nueve meses).', f'J_Canal R{J7TOT} / H{J7TOT}', f'IFERROR(J_Canal!$R${J7TOT}/J_Canal!$H${J7TOT},"")', 0.20, 'menor es mejor',
  'Propuesta interna: no más del 20 % de los mensajes a canales sin respuesta histórica.', 'Se paga y se satura un canal que para ese usuario no existe; en WhatsApp es dinero directo, en email son bajas.', 'Regla de canal preferido en Braze: si el usuario respondió a push o in-app y nunca a email, no mandar email promocional; misma regla para WhatsApp. Reactivación acotada a 3 toques en 30 días.', 'E7b', NOEQ + ' (E7b es por usuario). "Respondió" = clic email, apertura push, lectura WhatsApp o clic in-app; abrir un email sin clic no cuenta.', 'pct'),
 ('Canal mudo', '% de usuarios que nunca respondieron a nada (E7b enero a septiembre)', 'De los usuarios que recibieron algo en nueve meses, qué parte no tuvo ni una respuesta en ningún canal.', f'J_Canal B{J7RES["% que no respondieron a nada"]}', f'J_Canal!$B${J7RES["% que no respondieron a nada"]}', 0.50, 'menor es mejor',
  'Propuesta interna. En julio a septiembre (ventana de 90 días, J2) la cifra es más baja porque la ventana es más corta.', 'Más de la mitad de la base recibe mensajes y no reacciona a ninguno: la segmentación no está separando a quién vale la pena hablarle.', 'Reactivación acotada: 3 toques en 30 días a quien no responde; si sigue sin responder pasa a frecuencia mínima (1 al mes) o sale del promocional. Ver definición explícita de "nunca respondió" en Léeme.', 'E7b', NOEQ + ' (E7b es por usuario). Es un techo: confirmaciones de lectura de WhatsApp apagadas cuentan como no leído.', 'pct'),
 ('Segmentación', 'Envíos promocionales a etapas bloqueadas: Blacklist, CC Freeze, REUS/ARCO (E7a)', 'Envíos de familias promocionales a usuarios que en ese momento estaban en una etapa que no debe recibir promoción.', 'H_Etapas B12 (total) y H3 por equipo', 'H_Etapas!$B$12', 0, 'menor es mejor',
  'Regla de negocio: cero. Un usuario en Blacklist, con tarjeta congelada o con solicitud REUS/ARCO no debe recibir promoción.', 'Riesgo legal (ARCO) y de marca; además no convierten.', 'Excluir las tres etapas en el segmento de entrada de todo Canvas promocional (atributo de golden record); las 40 familias que más lo hacen están en H_Etapas H4.', 'E7a', 'Etapa del usuario al momento del envío; E7a cubre 37 % de los envíos con etapa conocida. Tipo promocional = regla por nombre y equipo (Catálogo). Por equipo: H_Etapas H3.', 'num0', h3_eq),
 ('Segmentación', 'Emails promocionales a usuarios ya dados de baja (E5b)', 'Emails de familias promocionales enviados a usuarios después de su fecha de baja.', f'E_DespuesBaja C{E_TIPO_ROW["promocional o lifecycle"]} (total) y E3 columna E por equipo', f'E_DespuesBaja!$C${E_TIPO_ROW["promocional o lifecycle"]}', 0, 'menor es mejor',
  'Regla de negocio y de Braze: cero. El transaccional y la cobranza sí pueden llegar después de la baja.', 'Quejas y marcado como spam, que daña la entrega de todos los equipos; además es un usuario que ya dijo que no.', 'Filtro de suscripción (subscribed u opted_in) en cada paso de email de cada Canvas promocional, nunca "todos"; la lista de familias está en E_DespuesBaja E4.', 'E5b', 'Tipo promocional = regla por nombre y equipo (Catálogo). Por equipo: E_DespuesBaja E3.', 'num0', e3_eq),
 ('Segmentación', '% de dados de baja que vuelven a recibir email después (E5, cualquier tipo)', 'De los usuarios con baja, qué parte recibió al menos un email después de la baja dentro del periodo.', f'E_DespuesBaja M{E_TOTAL_ROW}', f'E_DespuesBaja!$M${E_TOTAL_ROW}', 0.10, 'menor es mejor',
  'Propuesta interna: solo transaccional y cobranza deberían llegar después de la baja.', 'Una parte grande de los dados de baja sigue recibiendo email; si es promocional, es la fila anterior.', 'Misma acción que la fila anterior; revisar que el transaccional no lleve contenido promocional.', 'E5', NOEQ + ' (E5 es por usuario). Los meses finales tienen poco tiempo de observación.', 'pct'),
 ('Envíos masivos', 'Campañas de email activas con 1 M o más de usuarios por envío', 'Filas de Campañas (familia × canal email) activas en septiembre cuyo promedio de usuarios por mes es 1 M o más (Parámetros B31).', 'COUNTIFS sobre Campañas: canal email, usuarios_por_envío ≥ B31, activo_sep = 1', lambda eq: f'COUNTIFS({cr("canal")},"email",{cr("usuarios_por_envío (promedio)")},">="&{PB["aud"]},{cr("activo_sep")},1' + ('' if eq is None else f',{cr("equipo")},{eq}') + ')', 0, 'menor es mejor',
  'Propuesta interna (Parámetros B31): ningún envío a 1 M o más de usuarios sin prueba previa del 10 % y grupo de control.', 'Un envío masivo malo quema cientos de miles de usuarios de un golpe: en L_Baja L4 un solo email explica un tercio de las bajas de los usuarios nuevos.', 'Prueba al 10 % con 48 horas de lectura antes del envío completo; grupo de control del 10 %; segmentar en vez de mandar a toda la base.', 'E1', 'usuarios_por_envío = promedio mensual de usuarios_aprox (APPROX_COUNT_DISTINCT).', 'num0'),
 ('Envíos masivos', 'Campañas con respuesta debajo del mínimo que siguen activas (señal apagar o rehacer, activas en septiembre, sin cobranza ni transaccional)', 'Filas de Campañas con señal "apagar o rehacer", activas en septiembre y con acción distinta de No tocar.', 'COUNTIFS sobre Campañas: señal, activo_sep, accion_tipo', lambda eq: f'COUNTIFS({cr("señal")},"apagar o rehacer",{cr("activo_sep")},1,{cr("accion_tipo")},"<>No tocar"' + ('' if eq is None else f',{cr("equipo")},{eq}') + ')', 0, 'menor es mejor',
  'Regla interna (Parámetros B11 a B14): una campaña con volumen alto y respuesta debajo del mínimo de su canal no debería seguir corriendo.', 'Se sigue pagando y saturando usuarios con mensajes que no tienen respuesta.', 'Plan_accion: Apagar (no mueve), Rehacer o re-segmentar (sí mueve) o Limpiar base de WhatsApp.', 'E1', 'Depende de Parámetros (mínimos) y de las medianas por canal.', 'num0'),
 ('Grupos de control', 'Campañas promocionales con grupo de control', 'Si cada Canvas promocional reserva un grupo que no recibe el mensaje para medir conversión incremental.', 'No se puede medir con estas extracciones (no hay marca de control en la tabla).', 'no medible con estas extracciones', '10 % de holdout en toda campaña promocional', '', 
  'Práctica estándar de Braze (Control Group en Canvas) y de medición de incrementalidad.', 'Sin control no se sabe si la campaña mueve algo: la conversión "atribuida" puede ser gente que iba a convertir de todos modos (K_Abren y M_Ventanas: lift cercano a 1 en varias familias).', 'Activar Control Group del 10 % en cada Canvas promocional y leer conversión incremental, no conversión total.', '', 'La conversión de la tabla (is_converted) es de referencia.', 'txt'),
 ('Nomenclatura', '% de familias con ticket (B0211, T2728, S0004) en Braze o en el nombre', 'Qué parte de las familias del Catálogo tiene ticket, ya sea en ticket_number o dentro del nombre.', '1 − COUNTBLANK(ticket) / COUNTA(familia) del Catálogo', lambda eq: (f'IFERROR(1-COUNTBLANK({catc("ticket")})/COUNTA({CATA}),"")' if eq is None else f'IFERROR(1-SUMPRODUCT(({catc("equipo")}={eq})*({catc("ticket")}=""))/COUNTIF({catc("equipo")},{eq}),"")'), 1, 'mayor es mejor',
  'Regla interna de nomenclatura: toda pieza lleva su ticket.', 'Sin ticket no se sabe quién pidió la pieza ni se puede clasificar: aquí queda como transaccional u operativa aunque sea promocional.', 'Campo ticket_number obligatorio en Braze y ticket en el nombre con la forma Equipo-Producto-Ticket-Fecha-Nombre-Canal.', 'E1', 'El ticket sale de ticket_number si no es Other; si no, del nombre con regex; si no, vacío.', 'pct'),
]
EST_ROW0 = 6
for j, c in enumerate(EST_COLS, start=1): ws.cell(5, j, c).font = bold
ws.cell(4, 1, 'Una fila por métrica u operación. Columnas P a T: valor actual del equipo (mismo cálculo, filtrado por el equipo del Catálogo). Columna G editable.').font = bold
EST_ROWS = {}
for k, st in enumerate(EST):
    r = EST_ROW0 + k
    tema, met, que, como, f, std, sentido, fuente_std, signif, hacer, fuenteE, sup, fmt = st[:13]
    f_eq = st[13] if len(st) > 13 else (f if callable(f) else None)
    EST_ROWS[k + 1] = r
    vals = {'#': k + 1, 'tema': tema, 'métrica u operación': met, 'qué es': que, 'cómo se calcula aquí': como,
            'valor actual (todos los equipos)': ('=' + (f(None) if callable(f) else f)) if fmt != 'txt' else f,
            'estándar propuesto (editable)': std, 'sentido': sentido, 'de dónde sale el estándar': fuente_std,
            'brecha (actual − estándar)': f'=IF(AND(ISNUMBER({EL["valor actual (todos los equipos)"]}{r}),ISNUMBER({EL["estándar propuesto (editable)"]}{r})),{EL["valor actual (todos los equipos)"]}{r}-{EL["estándar propuesto (editable)"]}{r},"")',
            'estado': f'=IF(NOT(ISNUMBER({EL["valor actual (todos los equipos)"]}{r})),"sin medir",IF(NOT(ISNUMBER({EL["estándar propuesto (editable)"]}{r})),"sin estándar",IF({EL["sentido"]}{r}="mayor es mejor",IF({EL["valor actual (todos los equipos)"]}{r}>={EL["estándar propuesto (editable)"]}{r},"cumple","debajo"),IF({EL["valor actual (todos los equipos)"]}{r}<={EL["estándar propuesto (editable)"]}{r},"cumple","debajo"))))',
            'qué significa quedarse debajo': signif, 'qué hacer': hacer, 'fuente (E)': fuenteE, 'supuestos': sup}
    for eq in EQUIPOS:
        vals[eq] = ('=' + f_eq(f'{EL[eq]}$5')) if (callable(f_eq) and fmt != 'txt') else NOEQ
    tr = f'{EL[EQUIPOS[0]]}{r}:{EL[EQUIPOS[-1]]}{r}'
    vals['equipos debajo del estándar'] = f'=IF(OR(NOT(ISNUMBER({EL["estándar propuesto (editable)"]}{r})),COUNT({tr})=0),"",IF({EL["sentido"]}{r}="mayor es mejor",COUNTIF({tr},"<"&{EL["estándar propuesto (editable)"]}{r}),COUNTIF({tr},">"&{EL["estándar propuesto (editable)"]}{r})))'
    for c, v in vals.items():
        cc = ws.cell(r, EST_COLS.index(c) + 1, v)
        if c in ('valor actual (todos los equipos)', 'estándar propuesto (editable)', 'brecha (actual − estándar)') or c in EQUIPOS:
            cc.number_format = {'pct': '0.00%', 'num2': '#,##0.00', 'num0': '#,##0', 'txt': 'General'}[fmt]
        if c in ('qué es', 'cómo se calcula aquí', 'de dónde sale el estándar', 'qué significa quedarse debajo', 'qué hacer', 'supuestos', 'métrica u operación'): cc.alignment = wrap
EST_LAST = EST_ROW0 + len(EST) - 1
ws.freeze_panes = 'D6'; ws.auto_filter.ref = f'A5:{EL[EST_COLS[-1]]}{EST_LAST}'
for c, w in {'#': 4, 'tema': 13, 'métrica u operación': 40, 'qué es': 40, 'cómo se calcula aquí': 34, 'valor actual (todos los equipos)': 14, 'estándar propuesto (editable)': 14, 'sentido': 14, 'de dónde sale el estándar': 44, 'brecha (actual − estándar)': 12, 'estado': 10, 'qué significa quedarse debajo': 50, 'qué hacer': 50, 'fuente (E)': 8, 'supuestos': 44, 'equipos debajo del estándar': 12}.items():
    ws.column_dimensions[EL[c]].width = w
for eq in EQUIPOS: ws.column_dimensions[EL[eq]].width = 14

# ---------- Insights
ws = WS['Insights']
header(ws, 'Insights: todos los hallazgos en una sola tabla con filtros (lente, equipo, producto, canal, tipo de hallazgo)',
       'Cada cifra es una referencia viva a la celda de cálculo que la sostiene (columna O dice cuál); si cambian Parámetros o los datos, la cifra cambia. Las filas con equipo "todos" aplican a toda la operación; las filas con un equipo son la parte de ese equipo.',
       'Confianza alta = conteo directo de eventos; media = usa usuarios aproximados, clasificación por nombre o medianas; baja = usa la conversión de referencia (is_converted). Tipo de hallazgo: gasto (dinero), fatiga (frecuencia y bajas), segmentación (a quién le llega), calidad de dato (nombres, tickets, campos), oportunidad (lo que sí funciona y se puede escalar). "Estándar relacionado" es el número de fila (#) en la pestaña Estándares. Supuestos generales: costos de Parámetros, base de cobro de WhatsApp en B6, usuarios aproximados, familia = nombre sin fecha.')
INS_COLS = ['#', 'lente', 'equipo', 'producto', 'canal', 'tipo de hallazgo', 'hallazgo', 'cifra (fórmula viva)', 'unidad', 'fuente (E)', 'confianza', 'qué significa', 'qué hacer', 'estándar relacionado (#)', 'celda de origen', 'supuestos']
IL = {c: L(j) for j, c in enumerate(INS_COLS, start=1)}
INS = []
def ins(lente, equipo, producto, canal, tipo, hallazgo, f, unidad, fuente, conf, signif, hacer, est='', sup=''):
    INS.append((lente, equipo, producto, canal, tipo, hallazgo, f, unidad, fuente, conf, signif, hacer, est, sup))
MDc = lambda col, r=7: f'Medianas!${MEDL[col]}${r}'
B2 = lambda col, cnl: f'B_Canales!${LB2[col]}${B2ROW[cnl]}'
SUPC = 'Costo con la base de cobro de Parámetros B6; push e in-app sin costo; costo fijo de Braze no incluido.'
# B
ins('B', 'todos', 'todos', 'todos', 'gasto', 'Costo variable total del periodo (email + WhatsApp)', f'=B_Canales!${LB2["costo_mxn"]}${b2a + 5}', 'MXN', 'E4a', 'alta', 'Es lo que se paga en nueve meses por email y WhatsApp con los costos unitarios de Parámetros.', 'Todo el ahorro de esta auditoría se mide contra esta cifra.', '', SUPC)
ins('B', 'todos', 'todos', 'whatsapp', 'gasto', 'Parte del costo variable que es WhatsApp', f'={B2("% del costo", "whatsapp")}', '% del costo', 'E4a', 'alta', 'WhatsApp es la mayor parte del gasto aunque sea una parte chica de los envíos: cada mensaje cuesta 20 veces lo que un email.', 'Toda regla de ahorro empieza en WhatsApp: entrega, lectura y canal mudo.', '6', SUPC)
ins('B', 'todos', 'todos', 'whatsapp', 'calidad de dato', 'WhatsApp enviados que no se entregaron en el periodo (mensajes)', f'={B2("whatsapp_send", "whatsapp")}-{B2("whatsapp_delivery", "whatsapp")}', 'mensajes', 'E4a', 'alta', 'Números inválidos o que bloquearon a la empresa. Con la base "entregado" no se pagan, pero la base está sucia.', 'Limpiar base de WhatsApp: quitar números con 3 no-entregas seguidas antes de volver a enviar.', '6', 'Base entregado (Parámetros B6).')
ins('B', 'todos', 'todos', 'whatsapp', 'gasto', 'Lo que costarían esos WhatsApp no entregados si se cobrara por enviado', f'=SUM(B_Canales!$F${b4a}:$F${b4b})', 'MXN', 'E4a', 'alta', 'Es el escenario de las muestras anteriores (base enviado). Si el contrato cobra por enviado, este dinero se está tirando.', 'Confirmar con Meta o el proveedor la base real de cobro; si es por enviado, la limpieza es urgente.', '6', 'Costo por WhatsApp de Parámetros B3 sobre (enviados − entregados).')
ins('B', 'todos', 'todos', 'whatsapp', 'calidad de dato', '% de entrega de WhatsApp en el periodo', f'={B2("% entrega WhatsApp", "whatsapp")}', '% entregados / enviados', 'E4a', 'alta', 'Debajo del 90 % la base necesita limpieza.', 'Ver estándar 6.', '6', '')
ins('B', 'todos', 'todos', 'push notification', 'fatiga', 'Parte de todos los envíos que son push', f'={B2("% de los envíos", "push notification")}', '% de los envíos', 'E4a', 'alta', 'Más de la mitad del volumen es push, el canal que no cuesta dinero pero sí permiso del usuario.', 'Tope de 1 push promocional al día; apagar las familias push con señal apagar.', '5', '')
ins('B', 'todos', 'todos', 'push notification', 'fatiga', 'Respuesta de push en el periodo (aperturas / enviados)', f'={B2("respuesta", "push notification")}', '% apertura', 'E4a', 'alta', 'Debajo del benchmark (3 %): la mayoría de los push no se abre.', 'Disparar push por evento del usuario y no a toda la base; ver Plan_accion canal push.', '5', '')
ins('B', 'todos', 'todos', 'email', 'fatiga', 'Respuesta de email en el periodo (clics / entregados)', f'={B2("respuesta", "email")}', '% clic', 'E4a', 'alta', 'Debajo del benchmark promocional (1.5 %), arriba del mínimo interno (0.3 %).', 'Trabajar las familias con señal apagar o revisar en email (Plan_accion).', '3', '')
ins('B', 'todos', 'todos', 'email', 'fatiga', 'Bajas de email usuario-mes en el periodo (CIFRA A)', f'={B2("bajas_email_usuarios (usuario-mes)", "email")}', 'usuarios-mes', 'E4a', 'alta', 'Un usuario cuenta en cada mes en que se dio de baja. Los usuarios únicos (CIFRA B) están en la lente E.', 'Bajar frecuencia y cuidar el primer email (lente L).', '4', 'Usuario-mes, no usuarios únicos.')
ins('B', 'todos', 'todos', 'email', 'fatiga', 'Bajas por mil emails entregados en el periodo', f'={B2("bajas por mil entregados", "email")}', 'bajas por mil', 'E4a', 'alta', 'Arriba del estándar (2.5) la lista se desgasta más rápido de lo que crece.', 'Ver estándar 4.', '4', 'Eventos de baja, no usuarios.')
ins('B', 'todos', 'todos', 'todos', 'fatiga', '% de usuarios con 41 o más mensajes al mes (promedio de los 9 meses)', f'=IFERROR(SUM(B_Canales!$H${b3a}:$J${b3b})/SUM(B_Canales!$B${b3a}:$B${b3b}),"")', '% usuarios', 'E4b', 'alta', 'Un grupo recibe más de un mensaje al día.', 'Frequency cap global (estándar 10 y 11).', '11', 'E4b cuenta filas por usuario.')
ins('B', 'todos', 'todos', 'email', 'fatiga', 'Bajas de email por 100 usuarios en la banda 41+ mensajes al mes (promedio de meses)', f'=IFERROR(AVERAGE(B_Canales!$P${b3a}:$P${b3b}),"")', 'bajas por 100 usuarios', 'E4b', 'media', 'Comparar con la fila siguiente (banda 01-05): a más mensajes, más bajas por usuario. Eso es fatiga.', 'Frequency cap global; revisar qué Canvas se acumulan en esos usuarios.', '10', 'Promedio simple de 9 meses.')
ins('B', 'todos', 'todos', 'email', 'fatiga', 'Bajas de email por 100 usuarios en la banda 01-05 mensajes al mes (promedio de meses)', f'=IFERROR(AVERAGE(B_Canales!$O${b3a}:$O${b3b}),"")', 'bajas por 100 usuarios', 'E4b', 'media', 'Referencia de la fila anterior.', '', '10', 'Promedio simple de 9 meses.')
# Campañas / Medianas
ins('C', 'todos', 'todos', 'todos', 'gasto', 'Campañas (familia × canal) con señal "apagar o rehacer": volumen alto y respuesta debajo del mínimo', f'={MDc("apagar o rehacer")}', 'campañas', 'E1', 'alta', 'Son las que gastan y no responden. Campañas, columna señal.', 'Plan_accion: Apagar, Rehacer o re-segmentar, Limpiar base de WhatsApp o Confirmar apagado según el caso.', '22', DEF)
ins('C', 'todos', 'todos', 'todos', 'gasto', 'Ahorro al mes si se apagan las campañas con señal apagar que siguen activas (sin cobranza ni transaccional)', f'={MDc("ahorro_mxn_mes")}', 'MXN al mes', 'E1', 'alta', 'Techo: supone que se apaga todo lo que tiene esa señal, no solo lo que no mueve.', 'Ejecutar el Plan_accion en orden: Apagar primero, luego Limpiar y Rehacer.', '22', DEF + ' ' + SUPC)
ins('C', 'todos', 'todos', 'todos', 'gasto', 'Ahorro del periodo (9 meses) con la misma regla', f'={MDc("ahorro_mxn_periodo")}', 'MXN', 'E1', 'alta', 'Lo que ya se gastó en campañas sin respuesta en estos nueve meses.', '', '22', DEF + ' ' + SUPC)
ins('C', 'todos', 'todos', 'todos', 'fatiga', 'Mensajes al mes que dejan de salir si se apagan esas campañas', f'={MDc("msgs_mes_ahorrados")}', 'mensajes al mes', 'E1', 'alta', 'Menos presión sobre los usuarios además del ahorro.', '', '10', DEF)
for a in ACCIONES:
    ins('C', 'todos', 'todos', 'todos', 'oportunidad' if a in ('Proteger', 'Escalar') else ('calidad de dato' if a == 'No tocar' else 'gasto'), f'Campañas con acción "{a}"', f'={MDc(a)}', 'campañas', 'E1', 'alta', 'Conteo de filas de Campañas con esa acción (todos los canales).', 'Ver Plan_accion P1 (qué implica y cómo se ejecuta) y P4 (lista por campaña con ticket e ids).', '22', DEF)
for k, cnl in enumerate(C4):
    ins('C', 'todos', 'todos', cnl, 'fatiga', f'Mediana de respuesta de las campañas de {cnl}', f'=Medianas!${MEDL["mediana respuesta"]}${k + 2}', '% respuesta', 'E1', 'media', 'La mitad de las campañas del canal responde menos que esto. Es el corte de "revisar".', 'Comparar contra el mínimo (Parámetros) y el benchmark (Estándares).', {'email': '3', 'push notification': '5', 'whatsapp': '7', 'in-app': '8'}[cnl], 'Mediana sobre familias con respuesta medible.')
ins('C', 'todos', 'todos', 'email', 'fatiga', 'Campañas de email con bajas por mil entregados en o arriba del umbral de Parámetros B26', f'=COUNTIFS({cr("canal")},"email",{cr("bajas_por_mil")},">="&{PB["bajas_mil"]})', 'campañas', 'E1', 'alta', 'Cada una está desgastando la lista.', 'Bajar frecuencia y revisar audiencia (Plan_accion, acción Bajar frecuencia).', '4', DEF)
ins('C', 'todos', 'todos', 'email', 'segmentación', 'Campañas de email activas que mandan a 1 M o más de usuarios por envío', f'=Estándares!${EL["valor actual (todos los equipos)"]}${EST_ROWS[21]}', 'campañas', 'E1', 'media', 'Envíos masivos sin prueba previa: un solo email malo puede explicar un tercio de las bajas de usuarios nuevos (lente L).', 'Prueba al 10 % y grupo de control antes de cada envío masivo (estándar 21).', '21', 'usuarios_aprox promedio por mes.')
# E
ins('E', 'todos', 'todos', 'email', 'fatiga', 'Usuarios únicos que se dieron de baja de email en el periodo (CIFRA B)', f'=E_DespuesBaja!$B${E_TOTAL_ROW}', 'usuarios', 'E5', 'alta', 'Cada usuario una vez. Comparado con los usuarios con email (Parámetros B8) es la tasa de baja del periodo.', 'Lente L dice cuándo y con qué email se van.', '4', '')
ins('E', 'todos', 'todos', 'email', 'segmentación', 'Emails enviados a usuarios ya dados de baja (todos los tipos)', f'=E_DespuesBaja!$C${E_TIPO_ROW["no está en E1"] + 1}', 'emails', 'E5b', 'alta', 'Incluye transaccional y cobranza, que sí pueden llegar.', 'La fila siguiente aísla lo promocional, que es lo grave.', '19', 'Tipo del Catálogo por nombre y equipo.')
ins('E', 'todos', 'todos', 'email', 'segmentación', 'Emails PROMOCIONALES enviados a usuarios ya dados de baja', f'=E_DespuesBaja!$C${E_TIPO_ROW["promocional o lifecycle"]}', 'emails', 'E5b', 'alta', 'No debería pasar: el usuario pidió no recibir. Riesgo de spam y de queja.', 'Filtro de suscripción en cada paso de email de cada Canvas promocional (lista en E_DespuesBaja E4).', '19', 'Tipo del Catálogo por nombre y equipo.')
ins('E', 'todos', 'todos', 'email', 'segmentación', '% de los dados de baja que recibió al menos un email después de la baja', f'=E_DespuesBaja!$M${E_TOTAL_ROW}', '% usuarios', 'E5', 'alta', 'Los meses finales tienen poco tiempo de observación: la cifra real es mayor.', 'Ver estándar 20.', '20', '')
ins('E', 'todos', 'todos', 'email', 'fatiga', '% de los dados de baja que se vuelve a dar de baja después', f'=E_DespuesBaja!$S${E_TOTAL_ROW}', '% usuarios', 'E5', 'alta', 'Segunda baja = siguieron recibiendo y volvieron a decir que no.', '', '19', '')
for k, eq in enumerate(EQUIPOS):
    ins('E', eq, 'todos', 'email', 'segmentación', f'Emails promocionales a usuarios ya dados de baja de familias del equipo {eq}', f'=E_DespuesBaja!$E${e3a + k}', 'emails', 'E5b', 'alta', 'Parte del total de la fila "Emails PROMOCIONALES a dados de baja" que corresponde a este equipo.', 'Revisar el filtro de suscripción en los Canvas del equipo (E_DespuesBaja E4, columna equipo).', '19', 'Equipo del Catálogo con el mapeo de Parámetros.')
# F
ins('F', 'todos', 'todos', 'todos', 'fatiga', '% de usuario-días con 3 o más familias distintas el mismo día', '=IFERROR((F_Solape!$B$8+F_Solape!$B$9+F_Solape!$B$10)/F_Solape!$B$11,"")', '% usuario-días', 'E6a', 'alta', 'Varios equipos le hablan al mismo usuario el mismo día.', 'Exclusión mutua entre Canvas promocionales (24 h); calendario único.', '12', 'Grano usuario-día.')
ins('F', 'todos', 'todos', 'email', 'fatiga', 'Bajas por mil usuario-días cuando el usuario recibe 1 sola familia en el día', '=F_Solape!$L$6', 'bajas por mil usuario-días', 'E6a', 'alta', 'Referencia para la fila siguiente.', '', '12', '')
ins('F', 'todos', 'todos', 'email', 'fatiga', 'Bajas por mil usuario-días cuando el usuario recibe 3 o más familias en el día', '=IFERROR((F_Solape!$K$8+F_Solape!$K$9+F_Solape!$K$10)/(F_Solape!$B$8+F_Solape!$B$9+F_Solape!$B$10)*1000,"")', 'bajas por mil usuario-días', 'E6a', 'alta', 'Si es mayor que la fila anterior, el solapamiento produce bajas por sí mismo.', 'Máximo 2 familias por usuario por día (estándar 12).', '12', '')
ins('F', 'todos', 'todos', 'todos', 'fatiga', f'Usuario-días en que chocan los dos equipos que más coinciden ({par_sum.index[0]}, entre los 1,000 pares más grandes)', f'=F_Solape!$C${f3a}', 'usuario-días', 'E6b', 'media', 'Quién choca con quién: la etiqueta del par sale de los datos actuales (F_Solape F3, primera fila).', 'Acordar calendario y exclusión mutua entre esos dos equipos primero; los 30 pares de familias concretos están en F_Solape F4.', '12', 'E6b trae solo los 1,000 pares más grandes (LIMIT).')
ins('F', 'todos', 'todos', 'todos', 'fatiga', 'Usuario-días de pares donde AMBAS familias son promocionales (suma de los 1,000 pares)', f'=SUM(F_Solape!$F${f3a}:$F${f3b})', 'usuario-días', 'E6b', 'media', 'Choques evitables: dos promociones el mismo día al mismo usuario.', 'Regla de exclusión mutua promocional + promocional.', '12', 'Top 1,000 pares, no el total.')
# G
GROW = lambda a, cnl, base, keys, ncan=4: base + keys.index(a) * ncan + (C4.index(cnl) if ncan == 4 else ['email', 'push notification'].index(cnl))
fria = 'fríos: dormants, inactivos, rezagados, never active'; activos = 'clientes activos y recurrentes'
ins('G', 'todos', 'todos', 'email', 'segmentación', 'Respuesta de email a audiencias frías (dormants, inactivos, rezagados, never active), por el nombre de la comunicación', f'=G_Practicas!$G${GROW(fria, "email", g1a, AUDS)}', '% clic', 'E1', 'media', 'Las audiencias frías responden menos: mandarles lo mismo que a los activos no las despierta.', 'Reactivación acotada (3 toques en 30 días) con gancho distinto; después, frecuencia mínima.', '17', 'Audiencia por palabras clave en el nombre.')
ins('G', 'todos', 'todos', 'email', 'oportunidad', 'Respuesta de email a clientes activos y recurrentes, por el nombre de la comunicación', f'=G_Practicas!$G${GROW(activos, "email", g1a, AUDS)}', '% clic', 'E1', 'media', 'Referencia de la fila anterior: la misma empresa, otra audiencia.', 'Concentrar el presupuesto de WhatsApp y email en quien responde.', '3', 'Audiencia por palabras clave en el nombre.')
ins('G', 'todos', 'todos', 'email', 'segmentación', 'Respuesta de email cuando el envío va a 1 M o más de usuarios (banda de tamaño), sin cobranza ni transaccional', f'=G_Practicas!$G${GROW(TAM[3], "email", g3a, TAM, 2)}', '% clic', 'E1', 'media', 'Los envíos masivos responden menos que los chicos (comparar con la fila siguiente).', 'Segmentar en vez de mandar a toda la base; prueba al 10 % (estándar 21).', '21', 'Tamaño = usuarios_aprox del mes.')
ins('G', 'todos', 'todos', 'email', 'oportunidad', 'Respuesta de email cuando el envío va a menos de 10 mil usuarios, sin cobranza ni transaccional', f'=G_Practicas!$G${GROW(TAM[0], "email", g3a, TAM, 2)}', '% clic', 'E1', 'media', 'Referencia de la fila anterior.', '', '21', '')
ins('G', 'todos', 'todos', 'email', 'fatiga', 'Respuesta de email con 1 toque de la misma comunicación por usuario en el mes', f'=G_Practicas!$G${GROW("1", "email", g4a, TOQ, 2)}', '% clic', 'E1', 'media', 'Referencia para la fila siguiente.', '', '9', 'Filas de E1 con más de 1,000 usuarios.')
ins('G', 'todos', 'todos', 'email', 'fatiga', 'Respuesta de email con 5 o más toques de la misma comunicación por usuario en el mes', f'=G_Practicas!$G${GROW("5+", "email", g4a, TOQ, 2)}', '% clic', 'E1', 'media', 'Repetir la misma pieza 5 veces no multiplica la respuesta y sí las bajas (columna H de G4).', 'Frequency cap de 2 toques por comunicación al mes (estándar 9).', '9', 'Filas de E1 con más de 1,000 usuarios.')
ins('G', 'todos', 'todos', 'email', 'fatiga', 'Bajas por mil entregados con 5 o más toques de la misma comunicación en el mes', f'=G_Practicas!$H${GROW("5+", "email", g4a, TOQ, 2)}', 'bajas por mil', 'E1', 'media', 'Comparar con la banda 1 toque (G4, columna H).', '', '9', '')
ins('G', 'todos', 'todos', 'todos', 'fatiga', 'Usuarios que recibieron 321 o más mensajes en los nueve meses', f'=G_Practicas!$B${g5a + 8}', 'usuarios', 'E3', 'alta', 'Más de un mensaje al día durante nueve meses.', 'Frequency cap global.', '10', 'E3 cuenta filas por usuario.')
ins('G', 'todos', 'todos', 'email', 'fatiga', 'Eventos de baja de email por 100 usuarios en la banda 321+ mensajes', f'=G_Practicas!$F${g5a + 8}', 'bajas por 100 usuarios', 'E3', 'alta', 'Comparar con la banda 01-05 (fila siguiente): fatiga.', '', '10', '')
ins('G', 'todos', 'todos', 'email', 'fatiga', 'Eventos de baja de email por 100 usuarios en la banda 01-05 mensajes', f'=G_Practicas!$F${g5a + 1}', 'bajas por 100 usuarios', 'E3', 'alta', 'Referencia de la fila anterior.', '', '10', '')
# H
ins('H', 'todos', 'todos', 'todos', 'segmentación', 'Envíos promocionales a etapas bloqueadas (Blacklist + CC Freeze + REUS/ARCO)', '=H_Etapas!$B$12', 'envíos', 'E7a', 'alta', 'Usuarios que no deben recibir promoción la están recibiendo. Riesgo legal (ARCO) y de marca.', 'Excluir las tres etapas en el segmento de entrada de todo Canvas promocional (H_Etapas H4 lista las 40 familias).', '18', 'Etapa al momento del envío; E7a cubre 37 % de los envíos.')
ins('H', 'todos', 'todos', 'todos', 'segmentación', 'Envíos promocionales a usuarios en Blacklist', '=H_Etapas!$B$6', 'envíos', 'E7a', 'alta', '', 'Excluir etapa 3.Blacklist.', '18', '')
ins('H', 'todos', 'todos', 'todos', 'segmentación', 'Envíos promocionales a usuarios con tarjeta Kpay congelada (CC Freeze)', '=H_Etapas!$B$7', 'envíos', 'E7a', 'alta', 'Es el bloque más grande de las etapas bloqueadas.', 'Excluir etapa 4.Kpay CC Freeze.', '18', '')
ins('H', 'todos', 'todos', 'todos', 'segmentación', 'Envíos promocionales a usuarios con solicitud REUS o ARCO', '=H_Etapas!$B$8', 'envíos', 'E7a', 'alta', 'Riesgo legal directo: el usuario pidió no ser contactado o ejerció derechos ARCO.', 'Excluir etapa 6.Reus or Arco y auditar los Canvas que lo hicieron.', '18', '')
ins('H', 'todos', 'todos', 'todos', 'segmentación', 'Envíos promocionales a prospectos sin crédito (7.Prospects)', '=H_Etapas!$B$9', 'envíos', 'E7a', 'alta', 'No es error, pero vale preguntar si la oferta aplica a quien no tiene crédito.', 'Revisar Campañas, columna pct_prospectos: familias con más del 60 % a prospectos.', '', '')
for k, eq in enumerate(EQUIPOS):
    ins('H', eq, 'todos', 'todos', 'segmentación', f'Envíos promocionales a etapas bloqueadas de familias del equipo {eq}', f'=H_Etapas!$B${h3a + k}', 'envíos', 'E7a', 'alta', 'Parte del total de etapas bloqueadas que corresponde a este equipo.', 'Excluir las tres etapas en los Canvas del equipo.', '18', 'Equipo del Catálogo con el mapeo de Parámetros.')
# J
J7 = lambda lab: f'J_Canal!$B${J7RES[lab]}'; J9 = lambda lab: f'J_Canal!$B${J9RES[lab]}'
ins('J', 'todos', 'todos', 'todos', 'segmentación', '% de usuarios que NUNCA respondieron a nada en nueve meses (ni clic en email, ni apertura de push, ni lectura de WhatsApp, ni clic in-app)', '=' + J7('% que no respondieron a nada'), '% usuarios', 'E7b', 'alta', 'Casi tres de cada cuatro usuarios reciben mensajes y no reaccionan a ninguno. Es un techo: abrir un email sin clic no cuenta y las confirmaciones de lectura de WhatsApp apagadas cuentan como no leído.', 'Reactivación acotada (3 toques en 30 días); después, frecuencia mínima o fuera del promocional.', '17', 'Ver definición explícita en Léeme.')
ins('J', 'todos', 'todos', 'todos', 'segmentación', 'Usuarios que nunca respondieron a nada (enero a septiembre)', '=' + J7('Usuarios que no respondieron a nada ("ninguno")'), 'usuarios', 'E7b', 'alta', '', '', '17', '')
ins('J', 'todos', 'todos', 'todos', 'gasto', 'Mensajes enviados a quienes nunca respondieron a nada', '=' + J7('Mensajes a quienes no respondieron a nada'), 'mensajes', 'E7b', 'alta', 'Volumen que no produjo ni una respuesta.', '', '16', '')
ins('J', 'todos', 'todos', 'todos', 'gasto', 'Costo de los mensajes a quienes nunca respondieron a nada', '=' + J7('Costo de los mensajes a quienes no respondieron a nada'), 'MXN', 'E7b', 'alta', 'Dinero en email y WhatsApp a usuarios que no reaccionaron en nueve meses.', 'Es el ahorro máximo de una regla de canal preferido + reactivación acotada.', '16', SUPC)
ins('J', 'todos', 'todos', 'todos', 'gasto', 'Mensajes a canal mudo (canal al que ese usuario nunca respondió, incluye a los que no responden a nada)', '=' + J7('Mensajes a canal mudo (incluye a los que no responden a nada)'), 'mensajes', 'E7b', 'alta', 'Para ese usuario el canal no existe.', 'Regla de canal preferido en Braze (estándar 16).', '16', '')
ins('J', 'todos', 'todos', 'todos', 'gasto', 'Costo de los mensajes a canal mudo', '=' + J7('Costo de mensajes a canal mudo'), 'MXN', 'E7b', 'alta', '', '', '16', SUPC)
ins('J', 'todos', 'todos', 'email', 'segmentación', 'Emails a usuarios que SÍ responden a otro canal pero nunca hicieron clic en un email', '=' + J7('Emails a usuarios que responden a otro canal pero nunca hicieron clic en un email'), 'emails', 'E7b', 'alta', 'El usuario sí reacciona (push, in-app, WhatsApp) pero no por email: ese email es ruido pagado.', 'Para esos usuarios, mover lo promocional al canal que sí responde.', '16', '')
ins('J', 'todos', 'todos', 'whatsapp', 'gasto', 'WhatsApp entregados a usuarios que responden a otro canal pero nunca leyeron un WhatsApp', '=' + J7('WhatsApp entregados a usuarios que responden a otro canal pero nunca leyeron un WhatsApp'), 'mensajes', 'E7b', 'alta', 'Cuesta 1 MXN cada uno y el usuario ya mostró por dónde sí responde.', 'Sacar de WhatsApp a quien responde por otro canal y nunca leyó uno.', '16', '')
ins('J', 'todos', 'todos', 'whatsapp', 'calidad de dato', '% de entrega de WhatsApp entre quienes nunca respondieron a nada', '=' + J7('% entrega WhatsApp entre quienes no respondieron a nada'), '% entregados / enviados', 'E7b', 'alta', 'Comparar con la fila siguiente: la base muda también es la base que no recibe.', 'Limpieza de WhatsApp empezando por este grupo.', '6', '')
ins('J', 'todos', 'todos', 'whatsapp', 'calidad de dato', '% de entrega de WhatsApp entre quienes sí leen WhatsApp', '=' + J7('% entrega WhatsApp entre quienes sí leen WhatsApp'), '% entregados / enviados', 'E7b', 'alta', 'Referencia de la fila anterior.', '', '6', '')
ins('J', 'todos', 'todos', 'todos', 'segmentación', '% de usuarios que no respondieron a nada en julio a septiembre (ventana de 90 días)', '=' + J9('% que no respondieron a nada'), '% usuarios', 'E9b', 'alta', 'Más bajo que en nueve meses porque la ventana es más corta, pero sigue siendo la mayoría.', 'Misma regla de reactivación acotada.', '17', 'Solo respuestas y mensajes del trimestre.')
ins('J', 'todos', 'todos', 'todos', 'gasto', 'Costo de los mensajes a quienes no respondieron a nada en julio a septiembre', '=' + J9('Costo de los mensajes a quienes no respondieron a nada'), 'MXN', 'E9b', 'alta', 'Gasto trimestral en usuarios mudos: dividido entre 3 es el ahorro mensual posible.', '', '16', SUPC)
# K
for k, cnl in enumerate(C4):
    ins('K', 'todos', 'todos', cnl, 'oportunidad', f'Familias de {cnl} con muestra suficiente donde abrir casi no cambia la conversión (lift menor a Parámetros B16)', f'=K_Abren!$G${6 + k}', 'familias', 'E7c', 'baja', 'En esas familias quien abre convierte casi igual que quien no abre: el mensaje no mueve. Si además la respuesta está debajo del mínimo, se apaga.', 'Lista en K_Abren K2; acción en Plan_accion.', '23', 'Conversión de referencia (is_converted); solo compara grupos dentro de la misma campaña.')
    ins('K', 'todos', 'todos', cnl, 'oportunidad', f'Mediana del lift (convierten los que abren / los que no abren) en {cnl}, familias con muestra', f'=K_Abren!$F${6 + k}', 'veces', 'E7c', 'baja', 'Cuánto más convierte quien abre que quien no abre, en la familia típica del canal.', '', '23', 'Conversión de referencia.')
# L
ins('L', 'todos', 'todos', 'email', 'fatiga', 'Usuarios nuevos (primer email dentro del periodo) que se dieron de baja', '=L_Baja!$C$6', 'usuarios', 'E8', 'alta', 'Cohorte limpia: días y emails exactos.', '', '13', '')
ins('L', 'todos', 'todos', 'email', 'fatiga', 'Días hasta la baja, mediana, usuarios nuevos', '=L_Baja!$E$6', 'días', 'E8', 'media', 'Se van en el primer mes.', 'Rediseñar la secuencia de bienvenida (estándar 13).', '13', 'PERCENTILE_APPROX.')
ins('L', 'todos', 'todos', 'email', 'fatiga', 'Emails recibidos antes de la baja, mediana, usuarios nuevos', '=L_Baja!$H$6', 'emails', 'E8', 'media', 'Pocos emails bastan para la baja: el problema está en los primeros envíos.', 'Estándar 14.', '14', 'PERCENTILE_APPROX.')
ins('L', 'todos', 'todos', 'email', 'fatiga', '% de usuarios nuevos que se dan de baja el mismo día del primer email', f'=L_Baja!$D${l2a}', '% de la cohorte 1', 'E8', 'alta', 'El primer email ya los echó.', 'Confirmación de interés antes del primer promocional (estándar 15).', '15', '')
ins('L', 'todos', 'todos', 'email', 'segmentación', f'Familia que llegó el día de la baja a más usuarios nuevos (la primera fila de L_Baja L4: {fdb.clave.iloc[0]})', f'=L_Baja!$A${l4a}', 'familia', 'E8', 'alta', 'Un solo email explica una parte muy grande de las bajas de usuarios nuevos (fila siguiente).', 'Revisar esa pieza: audiencia, asunto, frecuencia; ticket e ids en L_Baja L4 y Catálogo.', '21', 'Clave estática: si se recarga E8, la primera fila puede cambiar.')
ins('L', 'todos', 'todos', 'email', 'segmentación', 'Usuarios nuevos que recibieron esa familia el día de su baja', f'=L_Baja!$F${l4a}', 'usuarios', 'E8', 'alta', '', '', '21', 'Doble conteo si recibió dos familias ese día.')
ins('L', 'todos', 'todos', 'email', 'segmentación', '% de las bajas de usuarios nuevos que explica esa familia', f'=L_Baja!$G${l4a}', '% de la cohorte 1', 'E8', 'alta', 'Casi un tercio de las bajas de nuevos con un solo email.', 'Prueba al 10 % y grupo de control antes de envíos masivos (estándar 21).', '21', '')
for k, eq in enumerate(EQUIPOS):
    ins('L', eq, 'todos', 'email', 'fatiga', f'Bajas de usuarios nuevos cuya familia del día de la baja es del equipo {eq}', f'=L_Baja!$C${l5a + k}', 'usuarios (con doble conteo)', 'E8', 'media', 'Qué equipo mandó el email que llegó el día de la baja. Pasa de 100 % por el doble conteo.', 'Revisar en L_Baja L4 las familias del equipo con más usuarios.', '13', 'Equipo del Catálogo; doble conteo.')
# M
for k, cnl in enumerate(C4):
    ins('M', 'todos', 'todos', cnl, 'oportunidad', f'Mediana del lift a 7 días en {cnl} (familias con muestra)', f'=M_Ventanas!$D${m2a + k}', 'veces', 'E9a', 'baja', 'Comparar con la fila siguiente: si el lift cae al alargar la ventana, la conversión iba a pasar de todos modos.', '', '23', 'Conversión de referencia.')
    ins('M', 'todos', 'todos', cnl, 'oportunidad', f'Mediana del lift a fin de periodo en {cnl} (familias con muestra)', f'=M_Ventanas!$G${m2a + k}', 'veces', 'E9a', 'baja', 'Ver fila anterior.', 'Grupo de control del 10 % para medir incrementalidad real (estándar 23).', '23', 'Conversión de referencia.')
# por producto y por equipo (Campañas)
prods = catp['prod'].value_counts().index.tolist()
for pr in prods:
    ins('C', 'todos', pr, 'todos', 'gasto', f'Costo del periodo de las campañas del producto {pr}', f'=SUMIFS({cr("costo_mxn")},{cr("producto")},"{pr}")', 'MXN', 'E1', 'alta', 'Producto = product_service de la primera fila de la familia en E1.', '', '', SUPC)
    ins('C', 'todos', pr, 'todos', 'gasto', f'Ahorro al mes posible en campañas del producto {pr}', f'=SUMIFS({cr("ahorro_mxn_mes")},{cr("producto")},"{pr}")', 'MXN al mes', 'E1', 'alta', '', 'Plan_accion P4 filtrando por producto.', '22', DEF)
    ins('C', 'todos', pr, 'email', 'fatiga', f'Respuesta de email de las campañas del producto {pr} (clics / entregados)', f'=IFERROR(SUMIFS({cr("email_click")},{cr("producto")},"{pr}")/SUMIFS({cr("email_delivery")},{cr("producto")},"{pr}"),"")', '% clic', 'E1', 'alta', '', '', '3', '')
for eq in EQUIPOS:
    q = f'"{eq}"'
    ins('C', eq, 'todos', 'todos', 'gasto', f'Costo del periodo de las campañas del equipo {eq}', f'={cs("costo_mxn", q)}', 'MXN', 'E1', 'alta', 'Suma de costo_mxn de Campañas del equipo.', '', '', SUPC)
    ins('C', eq, 'todos', 'todos', 'gasto', f'Costo al mes de las campañas activas del equipo {eq}', f'={cs("costo_mxn_mes", q)}', 'MXN al mes', 'E1', 'alta', 'Costo del periodo / meses con envíos, solo campañas activas en septiembre.', '', '', SUPC)
    ins('C', eq, 'todos', 'todos', 'gasto', f'Ahorro al mes posible en campañas del equipo {eq}', f'={cs("ahorro_mxn_mes", q)}', 'MXN al mes', 'E1', 'alta', 'Campañas del equipo con señal apagar, activas, sin cobranza ni transaccional.', 'Plan_accion P3 y P4 (filtrar por equipo) o Vista_equipo.', '22', DEF)
    ins('C', eq, 'todos', 'todos', 'gasto', f'Campañas del equipo {eq} con señal "apagar o rehacer"', f'=COUNTIFS({cr("equipo")},{q},{cr("señal")},"apagar o rehacer")', 'campañas', 'E1', 'alta', '', 'Vista_equipo, bloque V2.', '22', DEF)
    ins('C', eq, 'todos', 'email', 'fatiga', f'Respuesta de email del equipo {eq} (clics / entregados)', f'={ratio("email_click", "email_delivery")(q)}', '% clic', 'E1', 'alta', 'Comparar con el estándar 3 y con la mediana del canal.', '', '3', '')
    ins('C', eq, 'todos', 'email', 'fatiga', f'Bajas por mil emails entregados del equipo {eq}', f'={ratio("email_unsubscribe", "email_delivery", "*1000")(q)}', 'bajas por mil', 'E1', 'alta', '', 'Bajar frecuencia si pasa de Parámetros B26.', '4', '')
    ins('C', eq, 'todos', 'push notification', 'fatiga', f'Apertura de push del equipo {eq}', f'={ratio("pn_open", "pn_send")(q)}', '% apertura', 'E1', 'alta', '', '', '5', '')
    ins('C', eq, 'todos', 'whatsapp', 'calidad de dato', f'Entrega de WhatsApp del equipo {eq}', f'={ratio("whatsapp_delivery", "whatsapp_send")(q)}', '% entregados / enviados', 'E1', 'alta', '', 'Limpiar base de WhatsApp si está debajo de 90 %.', '6', '')
    ins('C', eq, 'todos', 'whatsapp', 'fatiga', f'Lectura de WhatsApp del equipo {eq}', f'={ratio("whatsapp_read", "whatsapp_delivery")(q)}', '% leídos / entregados', 'E1', 'alta', '', '', '7', '')
INS_ROW0 = 6
for j, c in enumerate(INS_COLS, start=1): ws.cell(5, j, c).font = bold
ws.cell(4, 1, 'Filtra por lente, equipo, producto, canal o tipo de hallazgo. equipo = "todos" aplica a toda la operación.').font = bold
for k, (lente, equipo, producto, canal, tipo, hallazgo, f, unidad, fuente, conf, signif, hacer, est, sup) in enumerate(INS):
    r = INS_ROW0 + k
    vals = [k + 1, lente, equipo, producto, canal, tipo, hallazgo, f, unidad, fuente, conf, signif, hacer, est, f[1:] if f.startswith('=') else f, sup]
    for j, v in enumerate(vals, start=1):
        cc = ws.cell(r, j, v)
        if j == 8:
            u = unidad.lower()
            cc.number_format = '0.00%' if u.startswith('%') else ('#,##0.00' if ('por mil' in u or 'veces' in u or 'por 100' in u) else '#,##0')
        if j in (7, 12, 13, 16): cc.alignment = wrap
INS_LAST = INS_ROW0 + len(INS) - 1
ws.freeze_panes = 'H6'; ws.auto_filter.ref = f'A5:{IL[INS_COLS[-1]]}{INS_LAST}'
for c, w in {'#': 4, 'lente': 6, 'equipo': 14, 'producto': 12, 'canal': 14, 'tipo de hallazgo': 14, 'hallazgo': 60, 'cifra (fórmula viva)': 14, 'unidad': 18, 'fuente (E)': 8, 'confianza': 9, 'qué significa': 50, 'qué hacer': 50, 'estándar relacionado (#)': 10, 'celda de origen': 40, 'supuestos': 40}.items():
    ws.column_dimensions[IL[c]].width = w

# ---------- Plan_accion
ws = WS['Plan_accion']
header(ws, 'Plan de acción: resumen por acción y lista por campaña con ticket e ids (todo fórmula sobre Campañas)',
       'Campañas (accion_tipo, envíos, costo, ahorro), Parámetros.',
       'La acción de cada campaña sale de la regla de Campañas (ver Léeme, "accion_tipo"). Ahorro = costo de las campañas con señal "apagar o rehacer" que no son cobranza ni transaccional; es un techo (supone apagar todo lo que tiene esa señal). Mensajes y costo "al mes" = solo campañas activas en septiembre, costo del periodo / meses con envíos. Si cambias Parámetros, las acciones y este plan se recalculan.')
PA_H = ['acción', 'qué implica', 'campañas (filas familia × canal)', 'de las cuales activas en septiembre', 'familias distintas', 'envíos del periodo', 'mensajes al mes (activas)', 'costo del periodo (MXN)', 'costo al mes (MXN, activas)', 'ahorro al mes si se ejecuta (MXN)', 'ahorro del periodo (MXN)', 'mensajes al mes que dejan de salir', 'orden sugerido', 'cómo se ejecuta en Braze']
IMPL = {'Apagar': ('Volumen alto, respuesta debajo del mínimo del canal y el mensaje no mueve a quien lo abre. Se detiene.', 1, 'Pausar o archivar el Canvas o la campaña; quitar de los calendarios recurrentes.'),
        'Confirmar apagado': ('Señal apagar pero ya no envía en septiembre: confirmar que esté archivado para que no reviva.', 2, 'Buscar por communication_id en Braze y archivar si sigue activo o programado.'),
        'Limpiar base de WhatsApp': ('WhatsApp con respuesta baja o mucho no entregado. Antes de apagar, quitar números que no reciben o no leen.', 3, 'Segmento de exclusión: números con 3 no-entregas seguidas o sin lectura en 90 días; verificar número antes de entrar al Canvas.'),
        'Bajar frecuencia': ('Bajas altas o 4.5 o más toques por usuario al mes.', 4, 'Frequency cap en el Canvas (máximo 2 por usuario al mes); re-entrada bloqueada 30 días.'),
        'Rehacer o re-segmentar': ('Respuesta baja pero el mensaje sí mueve a quien lo abre, o audiencia de 1 M o más por envío: cambiar audiencia, asunto u oferta.', 5, 'Nuevo segmento (quitar fríos y canal mudo), prueba al 10 % con grupo de control, luego envío completo.'),
        'Escalar': ('Respuesta alta con poco volumen: ampliar audiencia por pasos midiendo respuesta.', 6, 'Duplicar la audiencia en cada corte semanal mientras la respuesta se mantenga arriba de la mediana del canal.'),
        'Proteger': ('Respuesta alta con volumen: no tocar sin prueba; documentar qué hace bien.', 7, 'Congelar cambios sin prueba A/B; documentar audiencia, gancho y frecuencia como referencia para los demás.'),
        'Seguir igual': ('Sin señal: se mantiene y se revisa en el siguiente corte.', 8, 'Nada por ahora.'),
        'No tocar': ('Cobranza y transaccional u operativa: fuera del alcance de esta auditoría.', 9, 'Nada. Solo revisar que no lleven contenido promocional.')}
def pa_row(rr, crit_a, extra=''):
    c_ = f'{cr("accion_tipo")},{crit_a}{extra}'
    return [f'=COUNTIFS({c_})', f'=COUNTIFS({c_},{cr("activo_sep")},1)', (None if LO_TEST else f'=IFERROR(COUNTA(UNIQUE(FILTER({cr("familia")},{cr("accion_tipo")}={crit_a}{extra}))),0)'),
            f'=SUMIFS({cr("envíos")},{c_})', f'=SUMIFS({cr("envíos_mes_prom")},{c_},{cr("activo_sep")},1)', f'=SUMIFS({cr("costo_mxn")},{c_})', f'=SUMIFS({cr("costo_mxn_mes")},{c_})', f'=SUMIFS({cr("ahorro_mxn_mes")},{c_})', f'=SUMIFS({cr("ahorro_mxn_periodo")},{c_})', f'=SUMIFS({cr("msgs_mes_ahorrados")},{c_})']
rows = []
for k, a in enumerate(ACCIONES):
    rr = 6 + k
    r_ = pa_row(rr, f'$A{rr}')
    rows.append([a, IMPL[a][0]] + r_ + [IMPL[a][1], IMPL[a][2]])
rr = 6 + len(ACCIONES)
rows.append(['total', ''] + [f'=SUM({L(j)}6:{L(j)}{rr - 1})' for j in range(3, 13)] + ['', ''])
LPA, pa1a, pa1b = table(ws, 4, 'P1. Resumen por acción', PA_H, rows, int_cols=tuple(PA_H[2:12]))
PA_TOT = pa1b
r0 = pa1b + 3
tot_ = lambda col: f'{LPA[col]}{PA_TOT}'
res = [('Mensajes al mes hoy (campañas activas en septiembre, promedio por mes)', f'=SUMIFS({cr("envíos_mes_prom")},{cr("activo_sep")},1)', '#,##0'),
       ('Costo al mes hoy (campañas activas en septiembre)', f'=SUM({cr("costo_mxn_mes")})', '#,##0'),
       ('Ahorro al mes si se ejecuta el plan (Apagar, Limpiar, Rehacer y Confirmar sobre las que tienen señal apagar)', f'={tot_("ahorro al mes si se ejecuta (MXN)")}', '#,##0'),
       ('% del costo al mes que se ahorra', f'=IFERROR({tot_("ahorro al mes si se ejecuta (MXN)")}/SUM({cr("costo_mxn_mes")}),"")', '0.00%'),
       ('Mensajes al mes que dejan de salir', f'={tot_("mensajes al mes que dejan de salir")}', '#,##0'),
       ('% de los mensajes al mes que dejan de salir', f'=IFERROR({tot_("mensajes al mes que dejan de salir")}/SUMIFS({cr("envíos_mes_prom")},{cr("activo_sep")},1),"")', '0.00%'),
       ('Campañas a tocar (Apagar + Confirmar apagado + Limpiar base de WhatsApp + Bajar frecuencia + Rehacer o re-segmentar)', '=' + '+'.join(f'{LPA["campañas (filas familia × canal)"]}{6 + ACCIONES.index(a)}' for a in ['Apagar', 'Confirmar apagado', 'Limpiar base de WhatsApp', 'Bajar frecuencia', 'Rehacer o re-segmentar']), '#,##0'),
       ('Campañas a cuidar (Proteger + Escalar)', '=' + '+'.join(f'{LPA["campañas (filas familia × canal)"]}{6 + ACCIONES.index(a)}' for a in ['Proteger', 'Escalar']), '#,##0')]
ws.cell(r0, 1, 'P2. Totales').font = bold
PA_RES = {}
for k, (lab, f, fmt) in enumerate(res):
    ws.cell(r0 + 1 + k, 1, lab); cc = ws.cell(r0 + 1 + k, 2, f); cc.number_format = fmt; PA_RES[lab] = r0 + 1 + k
r0 = r0 + len(res) + 3
PA3_H = ['equipo', 'acción', 'campañas (filas familia × canal)', 'de las cuales activas en septiembre', 'envíos del periodo', 'mensajes al mes (activas)', 'costo del periodo (MXN)', 'costo al mes (MXN, activas)', 'ahorro al mes si se ejecuta (MXN)', 'ahorro del periodo (MXN)', 'mensajes al mes que dejan de salir']
rows = []
for eq in EQUIPOS:
    for a in ACCIONES:
        rr = r0 + 2 + len(rows); c_ = f'{cr("accion_tipo")},$B{rr},{cr("equipo")},$A{rr}'
        rows.append([eq, a, f'=COUNTIFS({c_})', f'=COUNTIFS({c_},{cr("activo_sep")},1)', f'=SUMIFS({cr("envíos")},{c_})', f'=SUMIFS({cr("envíos_mes_prom")},{c_},{cr("activo_sep")},1)', f'=SUMIFS({cr("costo_mxn")},{c_})', f'=SUMIFS({cr("costo_mxn_mes")},{c_})', f'=SUMIFS({cr("ahorro_mxn_mes")},{c_})', f'=SUMIFS({cr("ahorro_mxn_periodo")},{c_})', f'=SUMIFS({cr("msgs_mes_ahorrados")},{c_})'])
LPA3, pa3a, pa3b = table(ws, r0, 'P3. Por equipo × acción (equipo del Catálogo con el mapeo de Parámetros)', PA3_H, rows, int_cols=tuple(PA3_H[2:]))
r0 = pa3b + 3
P4_COLS = ['accion_tipo', 'familia', 'canal', 'equipo', 'producto', 'ticket', 'communication_ids', 'tipo', 'envíos', 'envíos_mes_prom', 'activo_sep', 'costo_mxn', 'costo_mxn_mes', 'ahorro_mxn_mes', 'respuesta', 'mínimo del canal', 'mediana respuesta del canal', 'bajas_por_mil', 'mueve', 'por_qué (resumen)']
spill(ws, r0, 'P4. Lista por campaña con ticket e ids, en orden de ahorro al mes y envíos (acciones distintas de Seguir igual y No tocar; lista viva)', P4_COLS,
      f'=SORT(FILTER({{{",".join(cr(c) for c in P4_COLS)}}},({cr("accion_tipo")}<>"Seguir igual")*({cr("accion_tipo")}<>"No tocar")),{P4_COLS.index("ahorro_mxn_mes") + 1},FALSE,{P4_COLS.index("envíos") + 1},FALSE)',
      'Para una campaña: buscar el ticket o el communication_id en Braze, aplicar "cómo se ejecuta" de P1 según la acción, y leer por_qué para el contexto.')
PA_P4 = r0
ws.freeze_panes = 'A6'
for col, w in zip('ABCDEFGHIJKLMN', (26, 60, 14, 14, 14, 14, 14, 16, 16, 16, 16, 16, 10, 70)): ws.column_dimensions[col].width = w
for rr_ in range(6, 6 + len(ACCIONES)):
    ws.cell(rr_, 2).alignment = wrap; ws.cell(rr_, 14).alignment = wrap

# ---------- Vista_equipo
ws = WS['Vista_equipo']
ws.cell(1, 1, 'Vista por equipo: elige el equipo en B2 y toda la pestaña se recalcula').font = bold
ws.cell(2, 1, 'Equipo seleccionado (elige en B2):').font = bold
ws.cell(2, 2, EQUIPOS[0]).font = bold
dv2 = DataValidation(type='list', formula1='"' + ','.join(EQUIPOS) + '"', allow_blank=False); ws.add_data_validation(dv2); dv2.add('B2')
ws.cell(3, 1, 'Equipo = equipo del Catálogo (mapeo de Parámetros). Mensajes y costo de Campañas (sumas de E1); emails a dados de baja de E_DespuesBaja E3; etapas bloqueadas de H_Etapas H3; bajas de nuevos de L_Baja L5. Lo que viene por usuario (E4b, E6a, E7b, E9b, E8 resumen) no se parte por equipo. Las listas (V5 a V8) son fórmulas SORT y FILTER vivas. Costos con la base de cobro de Parámetros B6.').alignment = wrap
S_ = '$B$2'
def tsum(col): return f'SUMIFS({cr(col)},{cr("equipo")},{S_})'
V1 = [('Familias en el Catálogo', f'=COUNTIF({catc("equipo")},{S_})', '#,##0', 'COUNTIF en Catálogo, columna equipo'),
      ('Campañas (filas familia × canal con envíos)', f'=COUNTIF({cr("equipo")},{S_})', '#,##0', 'COUNTIF en Campañas, columna equipo'),
      ('Campañas activas en septiembre', f'=COUNTIFS({cr("equipo")},{S_},{cr("activo_sep")},1)', '#,##0', ''),
      ('Envíos del periodo', f'={tsum("envíos")}', '#,##0', 'SUMIFS envíos'),
      ('% de los envíos de toda la operación', f'=IFERROR({tsum("envíos")}/SUM({cr("envíos")}),"")', '0.00%', ''),
      ('Mensajes al mes (campañas activas en septiembre, promedio por mes)', f'=SUMIFS({cr("envíos_mes_prom")},{cr("equipo")},{S_},{cr("activo_sep")},1)', '#,##0', 'SUMIFS envíos_mes_prom con activo_sep = 1'),
      ('Costo del periodo (MXN)', f'={tsum("costo_mxn")}', '#,##0', 'SUMIFS costo_mxn'),
      ('% del costo de toda la operación', f'=IFERROR({tsum("costo_mxn")}/SUM({cr("costo_mxn")}),"")', '0.00%', ''),
      ('Costo al mes (MXN, campañas activas)', f'={tsum("costo_mxn_mes")}', '#,##0', 'SUMIFS costo_mxn_mes'),
      ('Ahorro al mes si se ejecuta el plan (MXN)', f'={tsum("ahorro_mxn_mes")}', '#,##0', 'SUMIFS ahorro_mxn_mes'),
      ('% del costo al mes del equipo que se ahorra', f'=IFERROR({tsum("ahorro_mxn_mes")}/{tsum("costo_mxn_mes")},"")', '0.00%', ''),
      ('Ahorro del periodo (MXN)', f'={tsum("ahorro_mxn_periodo")}', '#,##0', ''),
      ('Mensajes al mes que dejan de salir', f'={tsum("msgs_mes_ahorrados")}', '#,##0', ''),
      ('WhatsApp no entregados (mensajes)', f'={tsum("wa_no_entregados")}', '#,##0', ''),
      ('Respuesta email (clics / entregados)', f'=IFERROR({tsum("email_click")}/{tsum("email_delivery")},"")', '0.00%', 'Estándar 3'),
      ('Bajas por mil emails entregados', f'=IFERROR({tsum("email_unsubscribe")}/{tsum("email_delivery")}*1000,"")', '#,##0.00', 'Estándar 4'),
      ('Apertura push (aperturas / enviados)', f'=IFERROR({tsum("pn_open")}/{tsum("pn_send")},"")', '0.00%', 'Estándar 5'),
      ('Entrega WhatsApp (entregados / enviados)', f'=IFERROR({tsum("whatsapp_delivery")}/{tsum("whatsapp_send")},"")', '0.00%', 'Estándar 6'),
      ('Lectura WhatsApp (leídos / entregados)', f'=IFERROR({tsum("whatsapp_read")}/{tsum("whatsapp_delivery")},"")', '0.00%', 'Estándar 7'),
      ('Clic in-app (clics / impresiones)', f'=IFERROR({tsum("in_app_click")}/{tsum("in_app_impression")},"")', '0.00%', 'Estándar 8'),
      ('Emails promocionales a usuarios ya dados de baja (E5b)', '=' + e3_eq(S_), '#,##0', 'E_DespuesBaja E3, columna E'),
      ('Envíos promocionales a etapas bloqueadas (E7a)', '=' + h3_eq(S_), '#,##0', 'H_Etapas H3, columna B'),
      ('Bajas de usuarios nuevos cuya familia del día de la baja es del equipo (E8, con doble conteo)', '=' + l5_eq(S_), '#,##0', 'L_Baja L5, cohorte 1')]
ws.cell(5, 1, 'V1. Resumen del equipo').font = bold
ws.cell(5, 2, 'valor').font = bold; ws.cell(5, 3, 'cómo se calcula').font = bold
VE_RES = {}
for k, (lab, f, fmt, how) in enumerate(V1):
    rr = 6 + k; ws.cell(rr, 1, lab); cc = ws.cell(rr, 2, f); cc.number_format = fmt; ws.cell(rr, 3, how); VE_RES[lab] = rr
r0 = 6 + len(V1) + 2
VE_H2 = ['acción', 'campañas', 'activas en septiembre', 'envíos del periodo', 'mensajes al mes (activas)', 'costo del periodo (MXN)', 'costo al mes (MXN, activas)', 'ahorro al mes (MXN)', 'qué implica']
rows = []
for k, a in enumerate(ACCIONES):
    rr = r0 + 2 + k; c_ = f'{cr("accion_tipo")},$A{rr},{cr("equipo")},{S_}'
    rows.append([a, f'=COUNTIFS({c_})', f'=COUNTIFS({c_},{cr("activo_sep")},1)', f'=SUMIFS({cr("envíos")},{c_})', f'=SUMIFS({cr("envíos_mes_prom")},{c_},{cr("activo_sep")},1)', f'=SUMIFS({cr("costo_mxn")},{c_})', f'=SUMIFS({cr("costo_mxn_mes")},{c_})', f'=SUMIFS({cr("ahorro_mxn_mes")},{c_})', IMPL[a][0]])
rr = r0 + 2 + len(ACCIONES)
rows.append(['total'] + [f'=SUM({L(j)}{r0 + 2}:{L(j)}{rr - 1})' for j in range(2, 9)] + [''])
LV2, v2a, v2b = table(ws, r0, 'V2. Campañas del equipo por acción', VE_H2, rows, int_cols=tuple(VE_H2[1:8]))
r0 = v2b + 3
VE_H3 = ['canal', 'campañas', 'envíos del periodo', 'respuesta del equipo en el canal', 'mediana del canal (todos los equipos)', 'mínimo del canal (Parámetros)', 'costo del periodo (MXN)', 'ahorro al mes (MXN)']
rows = []
for k, cnl in enumerate(CANALES):
    rr = r0 + 2 + k; c_ = f'{cr("canal")},$A{rr},{cr("equipo")},{S_}'
    rows.append([cnl, f'=COUNTIFS({c_})', f'=SUMIFS({cr("envíos")},{c_})', f'=IFERROR(SUMIFS({cr(NUMR[cnl])},{c_})/SUMIFS({cr(DEN[cnl])},{c_}),"")' if cnl != 'banner' else '', '=' + med_lookup(f'$A{rr}', 'mediana respuesta'), '=' + min_formula(f'$A{rr}'), f'=SUMIFS({cr("costo_mxn")},{c_})', f'=SUMIFS({cr("ahorro_mxn_mes")},{c_})'])
LV3, v3a, v3b = table(ws, r0, 'V3. Por canal', VE_H3, rows, pct_cols=('respuesta del equipo en el canal', 'mediana del canal (todos los equipos)', 'mínimo del canal (Parámetros)'), int_cols=('campañas', 'envíos del periodo', 'costo del periodo (MXN)', 'ahorro al mes (MXN)'))
r0 = v3b + 3
VE_H4 = ['#', 'métrica u operación', 'valor del equipo', 'estándar propuesto', 'sentido', 'estado del equipo', 'valor de toda la operación', 'qué hacer']
rows = []
for k in range(len(EST)):
    er = EST_ROW0 + k; rr = r0 + 2 + k
    rows.append([f'=Estándares!$A${er}', f'=Estándares!${EL["métrica u operación"]}${er}', f'=INDEX(Estándares!${EL[EQUIPOS[0]]}${er}:${EL[EQUIPOS[-1]]}${er},1,MATCH({S_},Estándares!${EL[EQUIPOS[0]]}$5:${EL[EQUIPOS[-1]]}$5,0))', f'=Estándares!${EL["estándar propuesto (editable)"]}${er}', f'=Estándares!${EL["sentido"]}${er}',
                 f'=IF(NOT(ISNUMBER(C{rr})),IF(C{rr}="{NOEQ}","{NOEQ}","sin medir"),IF(NOT(ISNUMBER(D{rr})),"sin estándar",IF(E{rr}="mayor es mejor",IF(C{rr}>=D{rr},"cumple","debajo"),IF(C{rr}<=D{rr},"cumple","debajo"))))', f'=Estándares!${EL["valor actual (todos los equipos)"]}${er}', f'=Estándares!${EL["qué hacer"]}${er}'])
LV4, v4a, v4b = table(ws, r0, 'V4. Estándares: dónde está el equipo (valor del equipo contra el estándar de la pestaña Estándares)', VE_H4, rows)
for k, st in enumerate(EST):
    fmt = st[12]; rr = v4a + k
    for col in ('C', 'D', 'G'): ws[f'{col}{rr}'].number_format = {'pct': '0.00%', 'num2': '#,##0.00', 'num0': '#,##0', 'txt': 'General'}[fmt]
ws.cell(v4b + 1, 1, 'Debajo del estándar (cuántas filas)'); ws.cell(v4b + 1, 2, f'=COUNTIF(F{v4a}:F{v4b},"debajo")')
r0 = v4b + 4
TOP_COLS = ['familia', 'canal', 'ticket', 'communication_ids', 'tipo', 'envíos', 'envíos_mes_prom', 'activo_sep', 'costo_mxn', 'respuesta', 'mínimo del canal', 'bajas_por_mil', 'señal', 'accion_tipo']
topf = lambda extra, sortcol: f'=IFERROR(ARRAY_CONSTRAIN(SORT(FILTER({{{",".join(cr(c) for c in TOP_COLS)}}},{cr("equipo")}={S_}{extra}),{TOP_COLS.index(sortcol) + 1},FALSE),10,{len(TOP_COLS)}),"sin campañas")'
spill(ws, r0, 'V5. Las 10 campañas del equipo con más envíos', TOP_COLS, topf('', 'envíos'), 'Lista viva (SORT y FILTER sobre Campañas).')
VE_V5 = r0; r0 += 14
spill(ws, r0, 'V6. Los 10 emails del equipo con más bajas por mil entregados (al menos 1,000 entregados)', TOP_COLS, topf(f',{cr("canal")}="email",{cr("email_delivery")}>=1000,ISNUMBER({cr("bajas_por_mil")})', 'bajas_por_mil'), 'Lista viva.')
VE_V6 = r0; r0 += 14
INS_SEL = INS_COLS[:14]
spill(ws, r0, 'V7. Insights del equipo (los del equipo y los que aplican a todos)', INS_SEL,
      f'=FILTER(Insights!$A${INS_ROW0}:${IL[INS_SEL[-1]]}${INS_LAST},(Insights!${IL["equipo"]}${INS_ROW0}:${IL["equipo"]}${INS_LAST}={S_})+(Insights!${IL["equipo"]}${INS_ROW0}:${IL["equipo"]}${INS_LAST}="todos"))',
      'Lista viva sobre Insights. Las cifras son las mismas celdas vivas.')
VE_V7 = r0; r0 += len(INS) - 5 * len(EQUIPOS) + 2 * 5 + 6  # globales + los del equipo + margen
spill(ws, r0, 'V8. Todas las campañas del equipo con acción (sin Seguir igual ni No tocar), por ahorro al mes y envíos', P4_COLS,
      f'=IFERROR(SORT(FILTER({{{",".join(cr(c) for c in P4_COLS)}}},{cr("equipo")}={S_},({cr("accion_tipo")}<>"Seguir igual")*({cr("accion_tipo")}<>"No tocar")),{P4_COLS.index("ahorro_mxn_mes") + 1},FALSE,{P4_COLS.index("envíos") + 1},FALSE),"sin campañas con acción")',
      'Lista viva. Igual que Plan_accion P4 filtrada por el equipo.')
VE_V8 = r0
ws.freeze_panes = 'A4'
for col, w in zip('ABCDEFGHIJKLMN', (58, 18, 40, 16, 16, 16, 16, 16, 16, 16, 14, 14, 14, 14)): ws.column_dimensions[col].width = w
ws.cell(3, 1).alignment = wrap


# =====================================================================================
# ---------- Verificación
# =====================================================================================
e4a = E['E4a']; mes4 = e4a.grano == 'mes'
def S4(col, g='mes'): return float(num('E4a', col)[e4a.grano == g].sum())
costo_ent = S('E1', 'email_sent') * 0.05 + S('E1', 'whatsapp_delivery') * 1.0
costo_env = S('E1', 'email_sent') * 0.05 + S('E1', 'whatsapp_send') * 1.0
def xc(sheet, col, r): return f"'{sheet}'!${col}${r}" if '_' in sheet or ' ' in sheet else f"{sheet}!${col}${r}"
def xr(sheet, col, a, b): return f"{sheet}!${col}${a}:${col}${b}"
def base_if(ent, env): return f'=IF({PB["base_wa"]}="entregado",{ent},{env})'
DEF = 'Válido con los parámetros default. Si cambias Parámetros (mínimos, factores, muestra), esta fila sale REVISAR a propósito: el valor esperado está fijo con los defaults.'
UQ = ' UNIQUE de Google Sheets puede juntar o no las familias que solo cambian en mayúsculas/minúsculas; por eso la tolerancia es el número de esos pares. SUMIFS, COUNTIF y VLOOKUP siempre las juntan.'

V = []  # (grupo, pestaña, comprobación, fórmula, esperado, explicación, tolerancia)
def add(g, t, q, f, exp, ex='', tol=0.5): V.append((g, t, q, f, exp, ex, tol))

# ----- bloque 1: lo mismo que v1 (datos crudos)
for tab, *_, keycol in TABS:
    add('Filas', tab, f'Filas de datos (cuenta {keycol}, columna sin vacíos)', f'=COUNTA({rng(tab, keycol)})', INFO[tab]['filas'], 'Debe ser igual al CSV. Si difiere, la pega quedó incompleta.')
for c_ in ['envios','email_sent','email_delivery','email_open','email_click','email_unsubscribe','pn_send','pn_open','whatsapp_send','whatsapp_delivery','whatsapp_read','in_app_impression','in_app_click','banner_impression','banner_click','conversiones_filas','conversiones_fraccional','usuarios_aprox']:
    add('E1 totales', 'E1', f'Suma de {c_}', f'=SUM({rng("E1", c_)})', S('E1', c_), 'usuarios_aprox suma usuarios por fila: no es usuarios únicos.' if c_ == 'usuarios_aprox' else '')
add('E1 totales', 'E1', 'Suma de costo_mxn precalculado (NO USAR: WhatsApp sobre enviados)', f'=SUM({rng("E1","costo_mxn")})', S('E1','costo_mxn'), 'Columna heredada de la query. Coincide con el costo "base enviado" de abajo. El costo del análisis sale siempre de Parámetros.')
add('E1 totales', 'E1', 'Celdas vacías en monto_filas (eran null en Databricks)', f'=COUNTBLANK({rng("E1","monto_filas")})', int((e1.monto_filas == 'null').sum()), 'null = sin conversiones con monto. Se dejó vacío para que SUM funcione.')
add('E1 totales', 'E1', 'Filas con envíos = 0', f'=COUNTIF({rng("E1","envios")},0)', int((e1env == 0).sum()), 'Meses con aperturas o bajas de envíos anteriores pero sin envío nuevo. Las campañas activas se cuentan con envíos > 0.')
add('E1 totales', 'E1', 'Filas con ticket_number = "Other"', f'=COUNTIF({rng("E1","ticket_number")},"Other")', int((e1.ticket_number == 'Other').sum()), 'Sin ticket en Braze. El Catálogo lo saca del nombre con regex cuando se puede.')
add('E1 totales', 'E1', 'Filas sin communication_name (una comunicación sin nombre, 3 meses)', f'=COUNTBLANK({rng("E1","communication_name")})', int((e1.communication_name == 'null').sum()), 'Un solo communication_id. En familia (derivada) aparece como "(sin nombre)" en E1, E7a, E7c, E9a y E8 (en esas pestañas viene como null).')
add('E1 derivadas', 'E1', 'communication_id distintos sin nombre (deben ser 1 para que "(sin nombre)" sea una sola familia)', f'=COUNTA(UNIQUE(FILTER({rng("E1","communication_id")},{rng("E1","communication_name")}="")))', int(e1[e1.communication_name.isin(['null', ''])].communication_id.nunique()), 'Si pasa de 1, "(sin nombre)" junta varias comunicaciones y hay que separarlas por id.')
add('E1 derivadas', 'E1', 'communication_id distintos', f'=COUNTA(UNIQUE({rng("E1","communication_id")}))', int(e1.communication_id.nunique()), '')
add('E1 derivadas', 'E1', 'familias distintas (incluye "(sin nombre)")', f'=COUNTA(UNIQUE({rng("E1","familia (derivada)")}))', int(e1f.nunique()), 'familia = nombre sin la fecha -AAAAMMDD-. Comprueba que REGEXREPLACE evaluó en todas las filas. Debe ser igual a las filas del Catálogo.' + UQ, CASE_PAIRS)
add('E1 derivadas', 'E1', 'Filas con mes_clave con forma 2026-MM', f'=COUNTIF({rng("E1","mes_clave (derivada)")},"2026-*")', int(e1mes.str.startswith('2026').sum()), 'Debe ser igual a las filas.')
for m in sorted(e1mes.unique()):
    add('E1 derivadas', 'E1', f'Filas del mes {m}', f'=COUNTIF({rng("E1","mes_clave (derivada)")},"{m}")', int((e1mes == m).sum()), '')
add('E1 derivadas', 'E1', 'Filas de septiembre con envíos > 0', f'=COUNTIFS({rng("E1","mes_clave (derivada)")},"2026-09",{rng("E1","envios")},">0")', int(((e1mes == '2026-09') & (e1env > 0)).sum()), '')
add('E1 derivadas', 'E1', 'Familias activas en septiembre (envíos > 0)', f'=COUNTA(UNIQUE(FILTER({rng("E1","familia (derivada)")},{rng("E1","mes_clave (derivada)")}="2026-09",{rng("E1","envios")}>0)))', int(e1f[(e1mes == '2026-09') & (e1env > 0)].nunique()), 'Debe ser igual a la suma de activa_sep en el Catálogo.' + UQ, CASE_PAIRS)
add('E1 derivadas', 'E1', 'Suma de mes_num (derivada)', f'=SUM({rng("E1","mes_num (derivada)")})', int(e1mes.str[5:7].astype(int).sum()), 'Comprueba que mes_num quedó numérico en todas las filas (lo usan MINIFS y MAXIFS de primer y último mes).')
for eq in EQUIPOS:
    add('E1 derivadas', 'E1', f'Filas con equipo (derivada) = {eq}', f'=COUNTIF({rng("E1","equipo (derivada)")},"{eq}")', int((e1equipo == eq).sum()), 'Sale del mapeo de equipos en Parámetros. Si cambias el mapeo, cambia a propósito.')
for a in AUDS:
    add('E1 derivadas', 'E1', f'Filas con audiencia (derivada) = {a}', f'=COUNTIF({rng("E1","audiencia (derivada)")},"{a}")', int((e1aud == a).sum()), 'Clasificación por palabras clave en el nombre (ver Léeme).')
for g_ in GANS:
    add('E1 derivadas', 'E1', f'Filas con gancho (derivada) = {g_}', f'=COUNTIF({rng("E1","gancho (derivada)")},"{g_}")', int((e1gan == g_).sum()), '')
for b in TAM:
    add('E1 derivadas', 'E1', f'Filas con banda_tamaño = {b}', f'=COUNTIF({rng("E1","banda_tamaño (derivada)")},"{b}")', int((e1tam == b).sum()), '')
for b in TOQ:
    add('E1 derivadas', 'E1', f'Filas con banda_toques = {b}', f'=COUNTIF({rng("E1","banda_toques (derivada)")},"{b}")', int((e1toq == b).sum()), 'Vacío cuando usuarios_aprox es 0.')
add('Costos', 'E1 + Parámetros', 'Costo variable total con la base de cobro seleccionada', f'=SUM({rng("E1","email_sent")})*{PB["costo_email"]}+IF({PB["base_wa"]}="entregado",SUM({rng("E1","whatsapp_delivery")}),SUM({rng("E1","whatsapp_send")}))*{PB["costo_wa"]}+SUM({rng("E1","pn_send")})*{PB["costo_push"]}+SUM({rng("E1","in_app_impression")})*{PB["costo_inapp"]}', base_if(costo_ent, costo_env), 'Prueba del selector: cambia Parámetros!B6 entre entregado y enviado; esta fila y la esperada deben moverse juntas.')
add('Costos', 'E1', 'Costo variable si WhatsApp se cobra por entregado (fijo, para comparar)', f'=SUM({rng("E1","email_sent")})*0.05+SUM({rng("E1","whatsapp_delivery")})*1', costo_ent, 'Supone 0.05 por email y 1.00 por WhatsApp.')
add('Costos', 'E1', 'Costo variable si WhatsApp se cobra por enviado (fijo, para comparar)', f'=SUM({rng("E1","email_sent")})*0.05+SUM({rng("E1","whatsapp_send")})*1', costo_env, 'Cifra de las muestras viejas (71.9 M). Queda superada.')
add('Costos', 'E1', 'WhatsApp enviados que no se entregaron', f'=SUM({rng("E1","whatsapp_send")})-SUM({rng("E1","whatsapp_delivery")})', S('E1','whatsapp_send') - S('E1','whatsapp_delivery'), '14.2 M mensajes. Con base entregado no cuestan; con base enviado costarían 14.2 M MXN.')
add('E4a vs E1', 'E4a', 'Filas con grano = mes', f'=COUNTIF({rng("E4a","grano")},"mes")', int(mes4.sum()), '9 meses × 5 canales.')
add('E4a vs E1', 'E4a', 'Filas con grano = semana', f'=COUNTIF({rng("E4a","grano")},"semana")', int((~mes4).sum()), '')
for c_, ex in [('envios','E4a cuenta eventos; E1 deduplica usuario × comunicación × día. Diferencia esperada menor a 0.01 %.'),('email_sent',''),('pn_send',''),('whatsapp_send',''),('whatsapp_delivery',''),('in_app_impression','Misma razón que envíos.'),('email_click',''),('bajas_email_eventos','Igual a email_unsubscribe de E1 (eventos).')]:
    e1c = 'email_unsubscribe' if c_ == 'bajas_email_eventos' else c_
    add('E4a vs E1', 'E4a', f'Suma de {c_} con grano = mes', f'=SUMIF({rng("E4a","grano")},"mes",{rng("E4a",c_)})', S4(c_), ex)
    add('E4a vs E1', 'E4a', f'  diferencia contra E1 ({e1c})', f'=SUMIF({rng("E4a","grano")},"mes",{rng("E4a",c_)})-SUM({rng("E1",e1c)})', S4(c_) - S('E1', e1c), 'Cero o casi cero.' if not ex else ex)
add('Bajas', 'E4a', 'Bajas usuario-mes (bajas_email_usuarios, grano mes)', f'=SUMIF({rng("E4a","grano")},"mes",{rng("E4a","bajas_email_usuarios")})', S4('bajas_email_usuarios'), 'CIFRA A: 457,376. Un usuario cuenta en cada mes en que se dio de baja.')
add('Bajas', 'E4a', 'Bajas usuario-semana (grano semana)', f'=SUMIF({rng("E4a","grano")},"semana",{rng("E4a","bajas_email_usuarios")})', S4('bajas_email_usuarios', 'semana'), 'Mayor que usuario-mes porque un usuario puede caer en dos semanas del mismo mes.')
add('Bajas', 'E5', 'Usuarios únicos con baja (suma usuarios_baja)', f'=SUM({rng("E5","usuarios_baja")})', S('E5','usuarios_baja'), 'CIFRA B: 439,269. Un usuario cuenta una vez en el periodo.')
add('Bajas', 'E7b', 'Usuarios únicos con baja (suma usuarios_con_baja_email)', f'=SUM({rng("E7b","usuarios_con_baja_email")})', S('E7b','usuarios_con_baja_email'), '')
add('Bajas', 'E5 vs E7b', 'E5 menos E7b (debe dar cero)', f'=SUM({rng("E5","usuarios_baja")})-SUM({rng("E7b","usuarios_con_baja_email")})', S('E5','usuarios_baja') - S('E7b','usuarios_con_baja_email'), 'Dos queries distintas, misma definición.')
add('Bajas', 'E4a vs E5', 'Usuario-mes menos únicos', f'=SUMIF({rng("E4a","grano")},"mes",{rng("E4a","bajas_email_usuarios")})-SUM({rng("E5","usuarios_baja")})', S4('bajas_email_usuarios') - S('E5','usuarios_baja'), '18 mil usuarios se dieron de baja en más de un mes. Las dos cifras son correctas con su definición.')
add('Bajas', 'E1', 'Eventos de baja (email_unsubscribe)', f'=SUM({rng("E1","email_unsubscribe")})', S('E1','email_unsubscribe'), '1.09 M eventos: un usuario puede generar varios eventos de baja en un mes. No usar como usuarios.')
add('Bajas', 'E3', 'Eventos de baja según E3 (bajas_email)', f'=SUM({rng("E3","bajas_email")})', S('E3','bajas_email'), '0.2 % arriba de E1 por deduplicación de E1.')
add('Bajas', 'E4b', 'usuarios_con_baja_email (usuario-mes dentro de banda)', f'=SUM({rng("E4b","usuarios_con_baja_email")})', S('E4b','usuarios_con_baja_email'), '1.3 % debajo de E4a. E4b no se usa para contar bajas, solo para concentración de mensajes.')
add('Bajas', 'E5 + Parámetros', 'Tasa de baja del periodo = únicos / usuarios con email', f'=SUM({rng("E5","usuarios_baja")})/{PB["usuarios_email"]}', S('E5','usuarios_baja') / 20137560, '2.2 %. Denominador en Parámetros.', 1e-6)
add('E3 vs E7b', 'E3', 'Usuarios (suma)', f'=SUM({rng("E3","usuarios")})', S('E3','usuarios'), '19.5 M usuarios con al menos una fila en el periodo.')
add('E3 vs E7b', 'E7b', 'Usuarios (suma)', f'=SUM({rng("E7b","usuarios")})', S('E7b','usuarios'), 'Debe ser igual a E3.')
for c3, c7 in [('msgs','msgs'),('msgs_email','msgs_email'),('msgs_push','msgs_push'),('msgs_whatsapp','msgs_wa'),('msgs_whatsapp_entregados','msgs_wa_entregados'),('msgs_inapp','msgs_inapp')]:
    f3 = f'=SUM({rng("E3",c3)})'
    if c7 == 'msgs': f7 = f'=SUM({rng("E7b","msgs_email")})+SUM({rng("E7b","msgs_push")})+SUM({rng("E7b","msgs_wa")})+SUM({rng("E7b","msgs_inapp")})'; v7 = S('E7b','msgs_email') + S('E7b','msgs_push') + S('E7b','msgs_wa') + S('E7b','msgs_inapp')
    else: f7 = f'=SUM({rng("E7b",c7)})'; v7 = S('E7b', c7)
    add('E3 vs E7b', 'E3', f'Suma de {c3}', f3, S('E3', c3), '')
    add('E3 vs E7b', 'E7b', f'Suma de {c7} (E7b menos E3, debe dar cero)', f'{f7}-SUM({rng("E3",c3)})', v7 - S('E3', c3), 'Mismo grano (filas por usuario).')
add('E3 vs E1', 'E3', 'msgs_email de E3 menos email_sent de E1', f'=SUM({rng("E3","msgs_email")})-SUM({rng("E1","email_sent")})', S('E3','msgs_email') - S('E1','email_sent'), 'E3 cuenta filas; E1 deduplica. 0.2 % esperado.')
add('E3 vs E1', 'E3', 'msgs_whatsapp_entregados de E3 menos whatsapp_delivery de E1', f'=SUM({rng("E3","msgs_whatsapp_entregados")})-SUM({rng("E1","whatsapp_delivery")})', S('E3','msgs_whatsapp_entregados') - S('E1','whatsapp_delivery'), '1.3 % esperado por la misma razón.')
add('E3 vs E1', 'E4b', 'msgs de E4b menos msgs de E3 (debe dar cero)', f'=SUM({rng("E4b","msgs")})-SUM({rng("E3","msgs")})', S('E4b','msgs') - S('E3','msgs'), '')
def nunca(tab):
    d = E[tab]; return float(num(tab, 'usuarios')[(d.resp_email == '0') & (d.resp_push == '0') & (d.resp_wa == '0') & (d.resp_inapp == '0')].sum())
add('E7b', 'E7b', 'Usuarios que nunca respondieron (fila con los cuatro resp en 0)', f'=SUMIFS({rng("E7b","usuarios")},{rng("E7b","resp_email")},0,{rng("E7b","resp_push")},0,{rng("E7b","resp_wa")},0,{rng("E7b","resp_inapp")},0)', nunca('E7b'), '14.2 M de 19.5 M (73 %). Ver definición explícita en Léeme.')
add('E7b', 'E7b', 'Conversiones de usuarios (usuarios_con_conversion)', f'=SUM({rng("E7b","usuarios_con_conversion")})', S('E7b','usuarios_con_conversion'), '1.19 M usuarios. No comparar con conversiones_fraccional de E1.')
add('E9b', 'E9b', 'Usuarios jul-sep (suma)', f'=SUM({rng("E9b","usuarios")})', S('E9b','usuarios'), '7.07 M usuarios con mensajes en el trimestre.')
add('E9b', 'E9b', 'Usuarios que nunca respondieron en jul-sep', f'=SUMIFS({rng("E9b","usuarios")},{rng("E9b","resp_email")},0,{rng("E9b","resp_push")},0,{rng("E9b","resp_wa")},0,{rng("E9b","resp_inapp")},0)', nunca('E9b'), '4.10 M (58 %).')
add('E9b', 'E9b vs E1', 'msgs_email de E9b menos email_sent de E1 jul-sep', f'=SUM({rng("E9b","msgs_email")})-SUMIF({rng("E1","mes_clave (derivada)")},"2026-07",{rng("E1","email_sent")})-SUMIF({rng("E1","mes_clave (derivada)")},"2026-08",{rng("E1","email_sent")})-SUMIF({rng("E1","mes_clave (derivada)")},"2026-09",{rng("E1","email_sent")})', S('E9b','msgs_email') - float(num('E1','email_sent')[e1mes >= '2026-07'].sum()), '0.3 % por deduplicación de E1.')
res = num('E8', 'usuarios')
add('E8', 'E8', 'Usuarios en bloque resumen', f'=SUMIF({rng("E8","bloque")},"resumen",{rng("E8","usuarios")})', float(res[e8.bloque == 'resumen'].sum()), '400,821 usuarios con baja y al menos un email antes de la baja.')
add('E8', 'E8', 'Usuarios en bloque banda_dias (debe ser igual)', f'=SUMIF({rng("E8","bloque")},"banda_dias",{rng("E8","usuarios")})', float(res[e8.bloque == 'banda_dias'].sum()), '')
add('E8', 'E8', 'Usuarios en bloque banda_emails (debe ser igual)', f'=SUMIF({rng("E8","bloque")},"banda_emails",{rng("E8","usuarios")})', float(res[e8.bloque == 'banda_emails'].sum()), '')
add('E8', 'E8', 'Cohorte limpia (cohorte_limpia = 1, bloque resumen)', f'=SUMIFS({rng("E8","usuarios")},{rng("E8","bloque")},"resumen",{rng("E8","cohorte_limpia")},1)', float(res[(e8.bloque == 'resumen') & (e8.cohorte_limpia == '1')].sum()), 'Primer email dentro del periodo: la medida de días es exacta.')
add('E8', 'E8', 'Cohorte 0 (ya recibía antes de enero)', f'=SUMIFS({rng("E8","usuarios")},{rng("E8","bloque")},"resumen",{rng("E8","cohorte_limpia")},0)', float(res[(e8.bloque == 'resumen') & (e8.cohorte_limpia == '0')].sum()), 'Días medidos desde enero: subestimados.')
add('E8', 'E8 vs E5', 'Cobertura de E8 sobre usuarios únicos con baja', f'=SUMIF({rng("E8","bloque")},"resumen",{rng("E8","usuarios")})/SUM({rng("E5","usuarios_baja")})', float(res[e8.bloque == 'resumen'].sum()) / S('E5','usuarios_baja'), '91 %. El resto se dio de baja sin email previo en el periodo.', 1e-6)
add('E8', 'E8', 'Usuarios en bloque familia_dia_baja', f'=SUMIF({rng("E8","bloque")},"familia_dia_baja",{rng("E8","usuarios")})', float(res[e8.bloque == 'familia_dia_baja'].sum()), 'Mayor que 400,821 por el doble conteo (~104 %).')
for tab, c_, ex in [('E7a','envios','E7a agrupa por familia × canal × etapa; 0.7 % debajo de E1. Solo para distribución por etapa.'),('E6a','msgs','Grano usuario-día. 0.5 % debajo de E1. Solo para solapamiento.'),('E7c','envios_usuario_dia','Grano usuario-día; 0.9 % debajo de E1. Solo para abren vs no abren.'),('E9a','envios_usuario_dia','Igual que E7c, con ventanas.'),('E5b','emails_despues_de_baja','1.42 M emails a usuarios ya dados de baja.'),('E6b','usuario_dias_juntas','Top 1,000 pares por LIMIT: no es el total.')]:
    add('Otros granos', tab, f'Suma de {c_}', f'=SUM({rng(tab,c_)})', S(tab, c_), ex)
    if tab in ('E7a','E6a','E7c','E9a'):
        add('Otros granos', tab, f'  {c_} menos envíos de E1', f'=SUM({rng(tab,c_)})-SUM({rng("E1","envios")})', S(tab, c_) - S('E1','envios'), 'Diferencia esperada por grano, ver fila anterior.')
add('E2', 'E2', 'Piezas tipo canvas', f'=COUNTIF({rng("E2","tipo_pieza")},"canvas")', int((E['E2'].tipo_pieza == 'canvas').sum()), '')
add('E2', 'E2', 'Piezas tipo campaign', f'=COUNTIF({rng("E2","tipo_pieza")},"campaign")', int((E['E2'].tipo_pieza == 'campaign').sum()), '')
add('E2', 'E2', 'Familias distintas en el catálogo', f'=COUNTA(UNIQUE({rng("E2","familia (derivada)")}))', int(canon(fam_pd(E['E2'].nombre)).nunique()), 'Más que en E1 porque E2 trae piezas que no enviaron en el periodo.' + UQ, int(fam_pd(E['E2'].nombre).nunique() - canon(fam_pd(E['E2'].nombre)).nunique()))
add('E2', 'E2 vs E1', 'Ids de E2 que sí enviaron en el periodo (están en E1)', f'=SUMPRODUCT(--(COUNTIF({rng("E1","communication_id")},{rng("E2","communication_id")})>0))', int(E['E2'].communication_id.isin(e1.communication_id).sum()), '3,438 de 6,144. El id de la comunicación sin nombre de E1 no está en E2.')
# familias con fecha en las pestañas crudas
for tab, col in [('E5b', 'familia'), ('E7a', 'familia'), ('E7c', 'familia'), ('E9a', 'familia'), ('E6b', 'familia_a')]:
    d = E[tab][col]
    add('Familias con fecha', tab, f'Filas cuyo {col} trae fecha -AAAAMMDD- (la derivada la quita)', f'=SUMPRODUCT(--REGEXMATCH({rng(tab, col)},"-\\d{{8}}-"))', int(d.str.contains(r'-\d{8}-').sum()), 'E5b, E6b, E7a y E7c traen la familia con fecha; E9a y E8 ya vienen sin fecha (0). Por eso toda fórmula cruza por la columna familia (derivada), nunca por la original.')
    add('Familias con fecha', tab, f'Valores distintos de {col} (derivada)', f'=COUNTA(UNIQUE({rng(tab, col + " (derivada)")}))', int(canon(fam_pd(d)).nunique()), f'Original: {d.nunique()} valores distintos.' + UQ, int(fam_pd(d).nunique() - canon(fam_pd(d)).nunique()))

# ----- bloque 2: Catálogo
CATA = f'Catálogo!$A$2:$A${NC + 1}'
def catc(col): return f'Catálogo!${CL[col]}$2:${CL[col]}${NC + 1}'
add('Catálogo', 'Catálogo', 'Familias (filas)', f'=COUNTA({CATA})', NC, 'Una fila por familia de E1. Debe ser igual a "familias distintas" de E1.')
add('Catálogo', 'Catálogo', 'Suma de envíos (debe ser igual a E1)', f'=SUM({catc("envíos")})', S('E1','envios'), 'Comprueba que ninguna familia se perdió en el SUMIFS.')
add('Catálogo', 'Catálogo', 'Suma de costo_mxn (base de cobro seleccionada)', f'=SUM({catc("costo_mxn")})', base_if(costo_ent, costo_env), 'Igual al costo total de E1 + Parámetros.')
add('Catálogo', 'Catálogo', 'Suma de versiones (ids) = communication_id distintos de E1', f'=SUM({catc("versiones (ids)")})', int(e1.communication_id.nunique()), 'Cada id pertenece a una sola familia.')
add('Catálogo', 'Catálogo', 'Suma de meses con envíos', f'=SUM({catc("meses con envíos")})', int(catp.meses.sum()), '')
add('Catálogo', 'Catálogo', 'Familias activas en septiembre (activa_sep = 1)', f'=SUM({catc("activa_sep")})', int(catp.activa.sum()), 'Igual a la fila "Familias activas en septiembre" de E1 derivadas.')
add('Catálogo', 'Catálogo', 'Familias con primer_mes = 2026-01', f'=COUNTIF({catc("primer_mes")},"2026-01")', int((act.groupby('fam').mes.min().reindex(FAMS) == '2026-01').sum()), 'MINIFS sobre mes_num. Si da 0, MINIFS no evaluó.')
for t in TIPOS:
    add('Catálogo', 'Catálogo', f'Familias con tipo = {t}', f'=COUNTIF({catc("tipo")},"{t}")', int((catp.tipo == t).sum()), 'tipo = cobranza si el equipo de E1 es Collections; transaccional u operativa si el nombre empieza con Transaccional o no trae ticket; lo demás promocional o lifecycle.')
for eq in EQUIPOS:
    add('Catálogo', 'Catálogo', f'Familias con equipo = {eq}', f'=COUNTIF({catc("equipo")},"{eq}")', int((catp.equipo == eq).sum()), 'Con el mapeo de Parámetros.')
add('Catálogo', 'Catálogo', 'Familias sin ticket (vacío)', f'=COUNTBLANK({catc("ticket")})', int((catp.ticket == '').sum()), 'Ni Braze ni el nombre traen ticket.')
add('Catálogo', 'Catálogo', 'Familias con ticket = B0211', f'=COUNTIF({catc("ticket")},"B0211")', int((catp.ticket == 'B0211').sum()), 'Ejemplo de búsqueda por ticket.')
add('Catálogo', 'Catálogo', 'Familias que están en E2 ("sí")', f'=COUNTIF({catc("está en E2")},"sí")', int(catp.en_e2.sum()), '')
add('Catálogo', 'Catálogo', 'Familias con audiencia = cobranza', f'=COUNTIF({catc("audiencia (por nombre)")},"cobranza")', int((g1.groupby("fam").aud.first().reindex(FAMS) == 'cobranza').sum()), 'Audiencia de la primera fila de la familia en E1.')

# ----- bloque 3: Campañas
add('Campañas', 'Campañas', 'Filas (familia × canal con envíos > 0)', f'=COUNTA({cr("familia")})', NCAMP, '')
add('Campañas', 'Campañas', 'Suma de envíos (debe ser igual a E1)', f'=SUM({cr("envíos")})', S('E1','envios'), 'Las filas de E1 con envíos = 0 pertenecen a alguna familia × canal que sí envió, o suman 0.')
for k2, col in RAWCOL.items():
    name = col if k2 != 'cf' else 'conversiones_fraccional (ref)'
    add('Campañas', 'Campañas', f'Suma de {name}', f'=SUM({cr(name)})', float(camp[k2].sum()), 'Puede quedar debajo de E1 si una familia × canal tiene eventos pero nunca envíos > 0.' if k2 in ('eo', 'ec', 'eu', 'po', 'wr', 'ic', 'bc', 'cf') else '')
add('Campañas', 'Campañas', 'Suma de costo_mxn (base seleccionada)', f'=SUM({cr("costo_mxn")})', base_if(float(camp.costo_ent.sum()), float(camp.costo_env.sum())), '')
for cnl in CANALES:
    add('Campañas', 'Campañas', f'Filas con canal = {cnl}', f'=COUNTIF({cr("canal")},"{cnl}")', int((camp.canal == cnl).sum()), '')
add('Campañas', 'Campañas', 'Filas activas en septiembre (activo_sep = 1)', f'=SUM({cr("activo_sep")})', int(camp.activo.sum()), '')
add('Campañas', 'Campañas', 'Suma de versiones (ids)', f'=SUM({cr("versiones (ids)")})', int(camp.versiones.sum()), 'Un id puede contar en dos canales.')
add('Campañas', 'Campañas', 'Suma de usuarios_aprox (filas con envíos)', f'=SUM({cr("usuarios_aprox (suma de filas con envíos)")})', float(camp.usr.sum()), '')
add('Campañas', 'Campañas', 'Filas con respuesta medible (ISNUMBER)', f'=SUMPRODUCT(--ISNUMBER({cr("respuesta")}))', int(camp.resp.notna().sum()), 'Banner y filas con denominador 0 quedan vacías.')
add('Campañas', 'Campañas', 'Filas con volumen = alto', f'=COUNTIF({cr("volumen")},"alto")', int((camp.vol == 'alto').sum()), 'envíos ≥ mediana de envíos del canal (Medianas). Depende solo de los datos, no de Parámetros.')
for s_ in SENALES:
    add('Campañas', 'Campañas', f'Filas con señal = {s_}', f'=COUNTIF({cr("señal")},"{s_}")', int((camp.senal == s_).sum()), DEF)
add('Campañas', 'Campañas', 'Filas sin señal', f'=COUNTIF({cr("señal")},"")', int((camp.senal == '').sum()), DEF)
for a in ACCIONES:
    add('Campañas', 'Campañas', f'Filas con accion_tipo = {a}', f'=COUNTIF({cr("accion_tipo")},"{a}")', int((camp.accion == a).sum()), DEF)
add('Campañas', 'Campañas', 'Suma de ahorro_mxn_periodo (base seleccionada)', f'=SUM({cr("ahorro_mxn_periodo")})', base_if(float(camp.ahorro_per_ent.sum()), float(camp.ahorro_per_env.sum())), DEF + ' Costo del periodo de las familias con señal "apagar o rehacer" que no son cobranza ni transaccional.')
add('Campañas', 'Campañas', 'Suma de ahorro_mxn_mes (base seleccionada)', f'=SUM({cr("ahorro_mxn_mes")})', base_if(float(camp.ahorro_mes_ent.sum()), float(camp.ahorro_mes_env.sum())), DEF + ' Solo familias activas en septiembre: costo del periodo / meses con envíos.')
add('Campañas', 'Campañas', 'Suma de msgs_mes_ahorrados', f'=SUM({cr("msgs_mes_ahorrados")})', float(camp.msgs_ahorro.sum()), DEF)
add('Campañas', 'Campañas', 'Filas con muestra_ok = 1', f'=SUM({cr("muestra_ok")})', int(camp.muestra.sum()), DEF)
add('Campañas', 'Campañas', 'Filas con mueve = 1', f'=SUM({cr("mueve")})', int(camp.mueve.sum()), DEF)
add('Campañas', 'Campañas vs E7c', 'Suma de abrieron (E7c)', f'=SUM({cr("abrieron (E7c)")})', float(camp.ab.sum()), f'E7c suma {S("E7c","abrieron"):,.0f}; la diferencia es una familia de E7c que no está en E1.')
add('Campañas', 'Campañas vs E7c', 'Suma de abrieron + no_abrieron', f'=SUM({cr("abrieron (E7c)")})+SUM({cr("no_abrieron (E7c)")})', float(camp.eud.sum()), f'E7c envios_usuario_dia suma {S("E7c","envios_usuario_dia"):,.0f}.')
add('Campañas', 'Campañas vs E7a', 'Suma de envios_con_etapa (E7a)', f'=SUM({cr("envios_con_etapa (E7a)")})', float(camp.e7a_tot.sum()), f'E7a suma {S("E7a","envios"):,.0f}; la diferencia es una familia de E7a que no está en E1.')
add('Campañas', 'Campañas vs E7a', 'Suma de envios_etapa_bloqueada (E7a)', f'=SUM({cr("envios_etapa_bloqueada (E7a)")})', float(camp.bloq.sum()), '')
add('Campañas', 'Campañas vs E5b', 'Suma de emails_a_dados_de_baja (filas email)', f'=SUM({cr("emails_a_dados_de_baja (E5b)")})', float(camp.e5b.sum()), f'E5b suma {S("E5b","emails_despues_de_baja"):,.0f}; la diferencia son familias de E5b sin fila email en Campañas.')
add('Campañas', 'Campañas', 'Filas con pct_prospectos ≥ 60 % (Parámetros B36)', f'=COUNTIF({cr("pct_prospectos")},">="&{PB["pros"]})', int((camp.pct_pros >= 0.6).sum()), DEF)
add('Campañas', 'Campañas', 'Filas email con bajas_por_mil ≥ 2.5 (Parámetros B26)', f'=COUNTIFS({cr("canal")},"email",{cr("bajas_por_mil")},">="&{PB["bajas_mil"]})', int((camp.bajas_mil >= 2.5).sum()), DEF)
add('Campañas', 'Campañas', 'Filas con 3 o más toques por usuario al mes', f'=COUNTIF({cr("toques_usuario_mes")},">=3")', int((camp.toques >= 3).sum()), '')
add('Campañas', 'Campañas', 'Filas con lift ≥ 1.5 y muestra_ok = 1', f'=COUNTIFS({cr("muestra_ok")},1,{cr("lift")},">="&{PB["lift"]})', int(((camp.muestra == 1) & (camp.lift >= 1.5)).sum()), DEF)

# ----- bloque 4: Medianas
for k, cnl in enumerate(CANALES):
    r = k + 2
    add('Medianas', 'Medianas', f'{cnl}: familias (filas en Campañas)', f'=Medianas!$B${r}', int((camp.canal == cnl).sum()), '')
    add('Medianas', 'Medianas', f'{cnl}: mediana envíos', f'=Medianas!${MEDL["mediana envíos"]}${r}', float(med_env[cnl]), 'Mediana de envíos de las familias del canal. Corte de "volumen alto".')
    if cnl != 'banner':
        add('Medianas', 'Medianas', f'{cnl}: mediana respuesta', f'=Medianas!${MEDL["mediana respuesta"]}${r}', float(med_resp[cnl]), 'Solo familias con respuesta medible.', 1e-6)
        add('Medianas', 'Medianas', f'{cnl}: familias con muestra E7c', f'=Medianas!${MEDL["familias con muestra E7c"]}${r}', int(((camp.canal == cnl) & (camp.muestra == 1)).sum()), DEF)
        if cnl in med_conv.index and not pd.isna(med_conv[cnl]):
            add('Medianas', 'Medianas', f'{cnl}: mediana conv_abren (con muestra)', f'=Medianas!${MEDL["mediana conv_abren (con muestra)"]}${r}', float(med_conv[cnl]), DEF, 1e-6)
add('Medianas', 'Medianas', 'Total envíos (fila "todos los canales")', f'=Medianas!${MEDL["envíos"]}$7', S('E1','envios'), '')
add('Medianas', 'Medianas', 'Total filas por señal + sin señal = filas de Campañas', '=' + '+'.join(f'Medianas!${MEDL[s_]}$7' for s_ in SENALES + ['sin señal']), NCAMP, 'Toda fila tiene una señal o está vacía.')
add('Medianas', 'Medianas', 'Total filas por acción = filas de Campañas', '=' + '+'.join(f'Medianas!${MEDL[a]}$7' for a in ACCIONES), NCAMP, 'Toda fila tiene exactamente una acción.')

# ----- bloque 5: lentes
# B
e4m = e4a[mes4]
add('B_Canales', 'B_Canales', 'B2 total envíos (igual a E4a grano mes)', f'=B_Canales!$B${b2a + 5}', S4('envios'), '')
add('B_Canales', 'B_Canales', 'B2 total costo_mxn (base seleccionada)', f'=B_Canales!$I${b2a + 5}', base_if(S4('email_sent') * 0.05 + S4('whatsapp_delivery'), S4('email_sent') * 0.05 + S4('whatsapp_send')), 'Sobre E4a, que cuenta eventos: 0.01 % arriba del costo de E1.')
add('B_Canales', 'B_Canales', 'B2 email: bajas usuario-mes', f'=B_Canales!$G${B2ROW["email"]}', float(num('E4a','bajas_email_usuarios')[mes4 & (e4a.canal == 'email')].sum()), 'CIFRA A (457,376).')
add('B_Canales', 'B_Canales', 'B2 whatsapp: envíos', f'=B_Canales!$B${B2ROW["whatsapp"]}', float(num('E4a','envios')[mes4 & (e4a.canal == 'whatsapp')].sum()), '')
add('B_Canales', 'B_Canales', 'B1 respuesta email enero (clic / entregado)', f'=B_Canales!$F$6', float(num('E4a','email_click')[mes4 & (e4a.canal == 'email') & (e4a.periodo.str[:7] == '2026-01')].sum() / num('E4a','email_delivery')[mes4 & (e4a.canal == 'email') & (e4a.periodo.str[:7] == '2026-01')].sum()), 'Primera fila de B1.', 1e-6)
add('B_Canales', 'B_Canales', 'B3 usuarios con fila en enero (E4b)', f'=B_Canales!$B${b3a}', float(num('E4b','usuarios')[E['E4b'].mes.str[:7] == '2026-01'].sum()), '')
add('B_Canales', 'B_Canales', 'B4 suma whatsapp_send de los 9 meses', f'=SUM(B_Canales!$B${b4a}:$B${b4b})', float(num('E4a','whatsapp_send')[mes4 & (e4a.canal == 'whatsapp')].sum()), '')
# E
e5bt = pd.DataFrame(dict(fam=canon(fam_pd(E['E5b'].familia)), em=num('E5b','emails_despues_de_baja'))); e5bt['tipo'] = e5bt.fam.map(catp.tipo).fillna('no está en E1'); e5bt['equipo'] = e5bt.fam.map(catp.equipo).fillna('no está en E1')
add('E_DespuesBaja', 'E_DespuesBaja', 'E1 total usuarios_baja (igual a E5)', f'=E_DespuesBaja!$B${E_TOTAL_ROW}', S('E5','usuarios_baja'), '')
add('E_DespuesBaja', 'E_DespuesBaja', 'E1 total reciben_email_despues_total', f'=E_DespuesBaja!$L${E_TOTAL_ROW}', S('E5','reciben_email_despues_total'), '')
add('E_DespuesBaja', 'E_DespuesBaja', 'E2 total emails a dados de baja (igual a E5b)', f'=E_DespuesBaja!$C${E_TIPO_ROW["no está en E1"] + 1}', S('E5b','emails_despues_de_baja'), '')
for t in TIPOS + ['no está en E1']:
    add('E_DespuesBaja', 'E_DespuesBaja', f'E2 emails a dados de baja de familias {t}', f'=E_DespuesBaja!$C${E_TIPO_ROW[t]}', float(e5bt.em[e5bt.tipo == t].sum()), 'Tipo del Catálogo. "no está en E1" = la familia no envió en el periodo según E1 (nombre distinto o fuera de E1).')
add('E_DespuesBaja', 'E_DespuesBaja', 'E3 emails a dados de baja del equipo Marketing', f'=E_DespuesBaja!$C${e3a}', float(e5bt.em[e5bt.equipo == 'Marketing'].sum()), 'Con el mapeo de Parámetros.')
# F
add('F_Solape', 'F_Solape', 'F1 total usuario_dias (igual a E6a)', '=F_Solape!$B$11', S('E6a','usuario_dias'), '')
add('F_Solape', 'F_Solape', 'F1 usuario-días con 3 o más familias (3 a 4 + 5 a 7 + 8+)', '=F_Solape!$B$8+F_Solape!$B$9+F_Solape!$B$10', float(num('E6a','usuario_dias')[E['E6a'].banda_familias_dia.isin(BANDAS6[2:])].sum()), '')
add('F_Solape', 'F_Solape', 'F2 suma usuario_dias de los 9 meses', f'=SUM(F_Solape!$B${f2a}:$B${f2b})', S('E6a','usuario_dias'), '')
add('F_Solape', 'F_Solape', 'F3 suma usuario_dias_juntas (igual a E6b)', f'=SUM(F_Solape!$C${f3a}:$C${f3b})', S('E6b','usuario_dias_juntas'), 'Si el mapeo de equipos cambia, un par puede quedar fuera de las etiquetas y esta fila sale REVISAR.')
add('F_Solape', 'F_Solape', 'F3 primer par de equipos (el más grande)', f'=F_Solape!$C${f3a}', float(par_sum.iloc[0]), f'Etiqueta: {par_sum.index[0]}.')
add('F_Solape', 'F_Solape', 'F3 pares donde ambas son promocionales (suma)', f'=SUM(F_Solape!$E${f3a}:$E${f3b})', int(((canon(fam_pd(e6bdf.familia_a)).map(catp.tipo) == 'promocional o lifecycle') & (canon(fam_pd(e6bdf.familia_b)).map(catp.tipo) == 'promocional o lifecycle')).sum()), '')
# G
add('G_Practicas', 'G_Practicas', 'G1 suma de envíos (E1 en los 4 canales con respuesta)', f'=SUM(G_Practicas!$D${g1a}:$D${g1b})', float(g1.env[g1.canal.isin(C4)].sum()), 'Sin banner.')
add('G_Practicas', 'G_Practicas', 'G1 suma de comunicación-meses', f'=SUM(G_Practicas!$C${g1a}:$C${g1b})', int(g1.canal.isin(C4).sum()), 'Filas de E1 sin banner.')
add('G_Practicas', 'G_Practicas', 'G2 suma de envíos (sin cobranza ni transaccional)', f'=SUM(G_Practicas!$D${g2a}:$D${g2b})', float(g1.env[g1.canal.isin(C4) & ~g1.aud.isin(['cobranza', 'transaccional'])].sum()), '')
add('G_Practicas', 'G_Practicas', 'G3 suma de envíos (email y push, sin cobranza ni transaccional)', f'=SUM(G_Practicas!$D${g3a}:$D${g3b})', float(g1.env[g1.canal.isin(['email', 'push notification']) & ~g1.aud.isin(['cobranza', 'transaccional'])].sum()), '')
add('G_Practicas', 'G_Practicas', 'G4 suma de envíos (filas con más de 1,000 usuarios)', f'=SUM(G_Practicas!$D${g4a}:$D${g4b})', float(g1.env[g1.canal.isin(['email', 'push notification']) & ~g1.aud.isin(['cobranza', 'transaccional']) & (g1.usr > 1000)].sum()), '')
add('G_Practicas', 'G_Practicas', 'G5 suma de usuarios (igual a E3)', f'=SUM(G_Practicas!$B${g5a}:$B${g5b})', S('E3','usuarios'), '')
add('G_Practicas', 'G_Practicas', 'G5 costo_mxn total (base seleccionada)', f'=SUM(G_Practicas!$I${g5a}:$I${g5b})', base_if(S('E3','msgs_email') * 0.05 + S('E3','msgs_whatsapp_entregados'), S('E3','msgs_email') * 0.05 + S('E3','msgs_whatsapp')), 'Sobre E3 (filas por usuario): 0.2 % arriba de E1.')
# H
a7['tipo'] = a7.fam.map(catp.tipo).fillna('no está en E1')
add('H_Etapas', 'H_Etapas', 'H1 total envíos (igual a E7a)', '=H_Etapas!$F$11', S('E7a','envios'), '')
add('H_Etapas', 'H_Etapas', 'H1 envíos a etapas bloqueadas (3 + 4 + 6)', '=H_Etapas!$F$12', float(a7.env[a7.etapa.isin(BLOQUEADAS)].sum()), '')
add('H_Etapas', 'H_Etapas', 'H1 envíos promocionales a etapas bloqueadas', '=H_Etapas!$B$12', float(a7.env[a7.etapa.isin(BLOQUEADAS) & (a7.tipo == 'promocional o lifecycle')].sum()), 'Lo que no debería pasar.')
add('H_Etapas', 'H_Etapas', 'H1 envíos sin_golden', '=H_Etapas!$F$10', float(a7.env[a7.etapa == 'sin_golden'].sum()), '')
add('H_Etapas', 'H_Etapas', 'H1 envíos de familias que no están en E1', '=H_Etapas!$E$11', float(a7.env[a7.tipo == 'no está en E1'].sum()), 'Debe ser 0: la familia null de E7a es la comunicación sin nombre de E1 y cruza como "(sin nombre)".')
add('H_Etapas', 'H_Etapas', 'H2 suma de envíos (4 canales × 5 etapas)', f'=SUM(H_Etapas!$C${h2a}:$C${h2b})', float(a7.env[a7.canal.isin(C4)].sum()), 'Sin banner.')
add('H_Etapas', 'H_Etapas', 'H3 suma promocional a bloqueadas por equipo', f'=SUM(H_Etapas!$B${h3a}:$B${h3b})', float(a7.env[a7.etapa.isin(BLOQUEADAS) & (a7.tipo == 'promocional o lifecycle')].sum()), 'Igual a H1 fila 12 columna B.')
# J
def j_pd(tab):
    u = num(tab, 'usuarios'); re_, rp, rw, ri = [num(tab, c_) for c_ in ['resp_email', 'resp_push', 'resp_wa', 'resp_inapp']]
    me, mp, mw, mwe, mi = [num(tab, c_) for c_ in ['msgs_email', 'msgs_push', 'msgs_wa', 'msgs_wa_entregados', 'msgs_inapp']]
    nin = (re_ + rp + rw + ri) == 0; msgs = me + mp + mw + mi
    return dict(users=float(u.sum()), nin=float(u[nin].sum()), pct_nin=float(u[nin].sum() / u.sum()), msgs=float(msgs.sum()), msgs_nin=float(msgs[nin].sum()),
                mudo=float(((1 - re_) * me + (1 - rp) * mp + (1 - rw) * mw + (1 - ri) * mi).sum()),
                costo_ent=float((me * 0.05 + mwe).sum()), costo_env=float((me * 0.05 + mw).sum()),
                mudo_ent=float(((1 - re_) * me * 0.05 + (1 - rw) * mwe).sum()), mudo_env=float(((1 - re_) * me * 0.05 + (1 - rw) * mw).sum()))
for tab, RES, TOT, lab in [('E7b', J7RES, J7TOT, 'J1 (E7b, ene-sep)'), ('E9b', J9RES, J9TOT, 'J2 (E9b, jul-sep)')]:
    j = j_pd(tab)
    add('J_Canal', 'J_Canal', f'{lab} usuarios que recibieron algo', f'=J_Canal!$B${RES["Usuarios que recibieron algo"]}', j['users'], '')
    add('J_Canal', 'J_Canal', f'{lab} usuarios que no respondieron a nada', f'=J_Canal!$B${RES["Usuarios que no respondieron a nada (\"ninguno\")"]}', j['nin'], 'Misma cifra que "nunca respondieron" del bloque E7b / E9b.')
    add('J_Canal', 'J_Canal', f'{lab} % que no respondieron a nada', f'=J_Canal!$B${RES["% que no respondieron a nada"]}', j['pct_nin'], '73 % en ene-sep, 58 % en jul-sep.', 1e-6)
    add('J_Canal', 'J_Canal', f'{lab} mensajes totales', f'=J_Canal!$H${TOT}', j['msgs'], 'email + push + WhatsApp enviados + in-app.')
    add('J_Canal', 'J_Canal', f'{lab} mensajes a quienes no respondieron a nada', f'=J_Canal!$B${RES["Mensajes a quienes no respondieron a nada"]}', j['msgs_nin'], '')
    add('J_Canal', 'J_Canal', f'{lab} mensajes a canal mudo', f'=J_Canal!$B${RES["Mensajes a canal mudo (incluye a los que no responden a nada)"]}', j['mudo'], 'Mensajes por un canal al que ese grupo nunca respondió (WhatsApp cuenta enviados).')
    add('J_Canal', 'J_Canal', f'{lab} costo total (base seleccionada)', f'=J_Canal!$K${TOT}', base_if(j['costo_ent'], j['costo_env']), '')
    add('J_Canal', 'J_Canal', f'{lab} costo de mensajes a canal mudo (base seleccionada)', f'=J_Canal!$B${RES["Costo de mensajes a canal mudo"]}', base_if(j['mudo_ent'], j['mudo_env']), '')
# K
kab = camp.groupby('canal').ab.sum()
for k, cnl in enumerate(C4):
    add('K_Abren', 'K_Abren', f'K1 {cnl}: abrieron (suma)', f'=K_Abren!$K${6 + k}', float(kab.get(cnl, 0)), 'Suma de Campañas para ese canal.')
    add('K_Abren', 'K_Abren', f'K1 {cnl}: familias con muestra suficiente', f'=K_Abren!$C${6 + k}', int(((camp.canal == cnl) & (camp.muestra == 1)).sum()), DEF)
    n_ok = int(((camp.canal == cnl) & (camp.muestra == 1) & (camp.lift < 1.5)).sum())
    add('K_Abren', 'K_Abren', f'K1 {cnl}: familias con muestra y lift < lift mínimo', f'=K_Abren!$G${6 + k}', n_ok, DEF)
    sub = camp[(camp.canal == cnl) & (camp.muestra == 1)]
    if len(sub) and sub.lift.notna().any():
        add('K_Abren', 'K_Abren', f'K1 {cnl}: mediana lift (con muestra)', f'=K_Abren!$F${6 + k}', float(sub.lift.median()), DEF, 1e-6)
# L
fdb['equipo'] = fdb.clave.map(catp.equipo).fillna('no está en E1'); fdb['tipo'] = fdb.clave.map(catp.tipo).fillna('no está en E1')
r8 = e8[(e8.bloque == 'resumen')]
def r8v(col, coh): return float(pd.to_numeric(r8[r8.cohorte_limpia == str(coh)][col]).iloc[0])
add('L_Baja', 'L_Baja', 'L1 cohorte 1: usuarios', '=L_Baja!$C$6', r8v('usuarios', 1), '158,520 nuevos.')
add('L_Baja', 'L_Baja', 'L1 cohorte 0: usuarios', '=L_Baja!$C$7', r8v('usuarios', 0), '242,301 ya recibían en enero.')
add('L_Baja', 'L_Baja', 'L1 cohorte 1: dias_mediana', '=L_Baja!$E$6', r8v('dias_mediana', 1), '27 días.')
add('L_Baja', 'L_Baja', 'L1 cohorte 1: emails_mediana', '=L_Baja!$H$6', r8v('emails_mediana', 1), '5 emails.')
add('L_Baja', 'L_Baja', 'L2 suma usuarios por banda_dias (ambas cohortes)', f'=SUM(L_Baja!$C${l2a}:$C${l2b})', float(res[e8.bloque == 'banda_dias'].sum()), '')
add('L_Baja', 'L_Baja', 'L3 suma usuarios por banda_emails (ambas cohortes)', f'=SUM(L_Baja!$C${l3a}:$C${l3b})', float(res[e8.bloque == 'banda_emails'].sum()), '')
add('L_Baja', 'L_Baja', 'L4 suma usuarios familia_dia_baja (igual a E8)', f'=SUM(L_Baja!$F${l4a}:$F${l4b})', float(fdb.u.sum()), 'Con doble conteo.')
add('L_Baja', 'L_Baja', 'L4 primera fila: usuarios (la familia con más bajas de la cohorte 1)', f'=L_Baja!$F${l4a}', float(fdb.u.iloc[0]), f'{fdb.clave.iloc[0]}.')
add('L_Baja', 'L_Baja', 'L4 primera fila: % de la cohorte 1', f'=L_Baja!$G${l4a}', float(fdb.u.iloc[0] / r8v('usuarios', 1)), '31 %: un solo email explica casi un tercio de las bajas de usuarios nuevos.', 1e-6)
for eq in EQUIPOS:
    add('L_Baja', 'L_Baja', f'L5 cohorte 1, equipo {eq}: bajas', f'=L_Baja!$C${l5a + EQUIPOS.index(eq)}', float(fdb.u[(fdb.c == 1) & (fdb.equipo == eq)].sum()), 'Con el mapeo de Parámetros y el tipo del Catálogo.')
add('L_Baja', 'L_Baja', 'L6 cohorte 1, promocional o lifecycle: bajas', f'=L_Baja!$C${l6a}', float(fdb.u[(fdb.c == 1) & (fdb.tipo == 'promocional o lifecycle')].sum()), '')
# M
e9g = pd.DataFrame(dict(fam=canon(fam_pd(e9.familia)), canal=e9.canal, env=num('E9a','envios_usuario_dia'), ab=num('E9a','abrieron'), a90=num('E9a','ab_conv_90'), n90=num('E9a','no_conv_90'))).groupby(['fam', 'canal']).sum()
e9g['noab'] = e9g.env - e9g.ab; e9m = ((e9g.ab >= 1000) & (e9g.noab >= 1000) & (e9g.a90 + e9g.n90 >= 100))
mi = INFO['M_Ventanas']
add('M_Ventanas', 'M_Ventanas', 'M1 filas (familia × canal de E9a)', f'=COUNTA(M_Ventanas!$A${mi["first"]}:$A${mi["last"]})', mi['filas'], '')
add('M_Ventanas', 'M_Ventanas', 'M1 suma envios_usuario_dia (igual a E9a)', f'=SUM(M_Ventanas!$F${mi["first"]}:$F${mi["last"]})', S('E9a','envios_usuario_dia'), '')
add('M_Ventanas', 'M_Ventanas', 'M1 suma abrieron (igual a E9a)', f'=SUM(M_Ventanas!$G${mi["first"]}:$G${mi["last"]})', S('E9a','abrieron'), '')
add('M_Ventanas', 'M_Ventanas', 'M1 filas con muestra_ok = 1', f'=SUM(M_Ventanas!$U${mi["first"]}:$U${mi["last"]})', int(e9m.sum()), DEF)
for k, cnl in enumerate(C4):
    add('M_Ventanas', 'M_Ventanas', f'M2 {cnl}: familias con muestra', f'=M_Ventanas!$C${m2a + k}', int(e9m[e9g.index.get_level_values("canal") == cnl].sum()), DEF)

# ----- bloque 6: pestañas nuevas de v3 (Estándares, Insights, Plan_accion, Vista_equipo)
VE_NOTE = 'Válido con Marketing en Vista_equipo!B2 (el default). Si cambias el selector, esta fila sale REVISAR a propósito.'
def est_v(n, col='valor actual (todos los equipos)'): return f'=Estándares!${EL[col]}${EST_ROWS[n]}'
mk = camp.equipo == 'Marketing'
add('Estándares', 'Estándares', 'Filas de estándares', f'=COUNTA(Estándares!$A${EST_ROW0}:$A${EST_LAST})', len(EST), 'Una por métrica u operación.')
add('Estándares', 'Estándares', 'Valores actuales con error de fórmula', f'=SUMPRODUCT(--ISERROR(Estándares!${EL["valor actual (todos los equipos)"]}${EST_ROW0}:${EL["valor actual (todos los equipos)"]}${EST_LAST}))', 0, 'Debe ser 0.')
add('Estándares', 'Estándares', 'Filas con estado "sin medir"', f'=COUNTIF(Estándares!${EL["estado"]}${EST_ROW0}:${EL["estado"]}${EST_LAST},"sin medir")', sum(1 for st in EST if st[12] == 'txt'), 'Solo grupos de control (no medible con estas extracciones).')
add('Estándares', 'Estándares', '#1 entrega de email (entregados / enviados)', est_v(1), float(camp.ed.sum() / camp.es.sum()), 'Sumas de Campañas.', 1e-6)
add('Estándares', 'Estándares', '#3 clic de email (clics / entregados)', est_v(3), float(camp.ec.sum() / camp.ed.sum()), '', 1e-6)
add('Estándares', 'Estándares', '#3 clic de email, columna Marketing', est_v(3, 'Marketing'), float(camp.ec[mk].sum() / camp.ed[mk].sum()), 'Equipo del Catálogo con el mapeo de Parámetros.', 1e-6)
add('Estándares', 'Estándares', '#4 bajas por mil emails entregados', est_v(4), float(camp.eu.sum() / camp.ed.sum() * 1000), '', 1e-6)
add('Estándares', 'Estándares', '#5 apertura de push (aperturas / enviados)', est_v(5), float(camp.po.sum() / camp.ps.sum()), '', 1e-6)
add('Estándares', 'Estándares', '#6 entrega de WhatsApp (entregados / enviados)', est_v(6), float(camp.wd.sum() / camp.ws.sum()), '', 1e-6)
add('Estándares', 'Estándares', '#7 lectura de WhatsApp (leídos / entregados)', est_v(7), float(camp.wr.sum() / camp.wd.sum()), '', 1e-6)
add('Estándares', 'Estándares', '#8 clic de in-app (clics / impresiones)', est_v(8), float(camp.ic.sum() / camp.ii.sum()), '', 1e-6)
add('Estándares', 'Estándares', '#9 toques por usuario al mes (envíos / usuarios_aprox)', est_v(9), float(camp.env.sum() / camp.usr.sum()), 'usuarios_aprox sumado sobre filas con envíos.', 1e-6)
add('Estándares', 'Estándares', '#18 envíos promocionales a etapas bloqueadas (igual a H_Etapas B12)', est_v(18), float(a7.env[a7.etapa.isin(BLOQUEADAS) & (a7.tipo == 'promocional o lifecycle')].sum()), 'Tipo del Catálogo.')
add('Estándares', 'Estándares', '#19 emails promocionales a dados de baja (igual a E_DespuesBaja E2)', est_v(19), float(e5bt.em[e5bt.tipo == 'promocional o lifecycle'].sum()), 'Tipo del Catálogo.')
add('Estándares', 'Estándares', '#19 emails promocionales a dados de baja, columna Marketing', est_v(19, 'Marketing'), float(e5bt.em[e5bt.equipo == 'Marketing'].sum()), 'E_DespuesBaja E3: todos los tipos del equipo (igual que la fila E3 de Verificación).')
add('Estándares', 'Estándares', '#21 campañas de email activas con 1 M o más usuarios por envío', est_v(21), int(((camp.canal == 'email') & (camp.activo == 1) & (camp.usr_mean >= 1e6)).sum()), DEF)
add('Estándares', 'Estándares', '#22 campañas con señal apagar o rehacer, activas, sin No tocar', est_v(22), int(((camp.senal == 'apagar o rehacer') & (camp.activo == 1) & (camp.accion != 'No tocar')).sum()), DEF)
add('Estándares', 'Estándares', '#24 % de familias con ticket', est_v(24), float(1 - catp.ticket.fillna('').eq('').sum() / NC), 'ticket_number de Braze o regex sobre el nombre.', 1e-6)
add('Insights', 'Insights', 'Filas de insights', f'=COUNTA(Insights!$A${INS_ROW0}:$A${INS_LAST})', len(INS), '')
add('Insights', 'Insights', 'Cifras con error de fórmula', f'=SUMPRODUCT(--ISERROR(Insights!${IL["cifra (fórmula viva)"]}${INS_ROW0}:${IL["cifra (fórmula viva)"]}${INS_LAST}))', 0, 'Debe ser 0. Una cifra vacía ("") no es error: la métrica no aplica.')
add('Insights', 'Insights', 'Insights que aplican a todos los equipos (equipo = "todos")', f'=COUNTIF(Insights!${IL["equipo"]}${INS_ROW0}:${IL["equipo"]}${INS_LAST},"todos")', sum(1 for x in INS if x[1] == 'todos'), '')
for eq in EQUIPOS:
    add('Insights', 'Insights', f'Insights del equipo {eq}', f'=COUNTIF(Insights!${IL["equipo"]}${INS_ROW0}:${IL["equipo"]}${INS_LAST},"{eq}")', sum(1 for x in INS if x[1] == eq), '')
cpa = lambda col: f'=Plan_accion!${LPA[col]}${PA_TOT}'
add('Plan_accion', 'Plan_accion', 'P1 total campañas (suma de las 9 acciones)', cpa('campañas (filas familia × canal)'), NCAMP, 'Toda campaña tiene exactamente una acción.')
add('Plan_accion', 'Plan_accion', 'P1 total activas en septiembre', cpa('de las cuales activas en septiembre'), int(camp.activo.sum()), '')
add('Plan_accion', 'Plan_accion', 'P1 total envíos del periodo (igual a E1)', cpa('envíos del periodo'), float(camp.env.sum()), '')
add('Plan_accion', 'Plan_accion', 'P1 total mensajes al mes (activas)', cpa('mensajes al mes (activas)'), float(camp.msgs_mes.sum()), 'envíos_mes_prom de las activas en septiembre.')
add('Plan_accion', 'Plan_accion', 'P1 total costo del periodo (base seleccionada)', cpa('costo del periodo (MXN)'), base_if(float(camp.costo_ent.sum()), float(camp.costo_env.sum())), '')
add('Plan_accion', 'Plan_accion', 'P1 total costo al mes (activas, base seleccionada)', cpa('costo al mes (MXN, activas)'), base_if(float(camp.costo_mes_ent.sum()), float(camp.costo_mes_env.sum())), '')
add('Plan_accion', 'Plan_accion', 'P1 total ahorro al mes (base seleccionada)', cpa('ahorro al mes si se ejecuta (MXN)'), base_if(float(camp.ahorro_mes_ent.sum()), float(camp.ahorro_mes_env.sum())), DEF)
add('Plan_accion', 'Plan_accion', 'P1 total mensajes al mes que dejan de salir', cpa('mensajes al mes que dejan de salir'), float(camp.msgs_ahorro.sum()), DEF)
for a in ACCIONES:
    add('Plan_accion', 'Plan_accion', f'P1 campañas con acción {a}', f'=Plan_accion!${LPA["campañas (filas familia × canal)"]}${6 + ACCIONES.index(a)}', int((camp.accion == a).sum()), DEF)
add('Plan_accion', 'Plan_accion', 'P2 mensajes al mes hoy', f'=Plan_accion!$B${PA_RES["Mensajes al mes hoy (campañas activas en septiembre, promedio por mes)"]}', float(camp.msgs_mes.sum()), '')
add('Plan_accion', 'Plan_accion', 'P2 ahorro al mes si se ejecuta el plan', f'=Plan_accion!$B${PA_RES["Ahorro al mes si se ejecuta el plan (Apagar, Limpiar, Rehacer y Confirmar sobre las que tienen señal apagar)"]}', base_if(float(camp.ahorro_mes_ent.sum()), float(camp.ahorro_mes_env.sum())), DEF)
add('Plan_accion', 'Plan_accion', 'P3 suma de campañas (5 equipos × 9 acciones)', f'=SUM(Plan_accion!${LPA3["campañas (filas familia × canal)"]}${pa3a}:${LPA3["campañas (filas familia × canal)"]}${pa3b})', NCAMP, '')
add('Plan_accion', 'Plan_accion', 'P3 suma de ahorro al mes (base seleccionada)', f'=SUM(Plan_accion!${LPA3["ahorro al mes si se ejecuta (MXN)"]}${pa3a}:${LPA3["ahorro al mes si se ejecuta (MXN)"]}${pa3b})', base_if(float(camp.ahorro_mes_ent.sum()), float(camp.ahorro_mes_env.sum())), DEF)
for eq in EQUIPOS:
    add('Plan_accion', 'Plan_accion', f'P3 {eq}: campañas (suma de sus 9 acciones)', f'=SUMIFS(Plan_accion!${LPA3["campañas (filas familia × canal)"]}${pa3a}:${LPA3["campañas (filas familia × canal)"]}${pa3b},Plan_accion!$A${pa3a}:$A${pa3b},"{eq}")', int((camp.equipo == eq).sum()), '')
vv = lambda lab: f'=Vista_equipo!$B${VE_RES[lab]}'
add('Vista_equipo', 'Vista_equipo', 'V1 familias en el Catálogo (Marketing)', vv('Familias en el Catálogo'), int((catp.equipo == 'Marketing').sum()), VE_NOTE)
add('Vista_equipo', 'Vista_equipo', 'V1 campañas (Marketing)', vv('Campañas (filas familia × canal con envíos)'), int(mk.sum()), VE_NOTE)
add('Vista_equipo', 'Vista_equipo', 'V1 envíos del periodo (Marketing)', vv('Envíos del periodo'), float(camp.env[mk].sum()), VE_NOTE)
add('Vista_equipo', 'Vista_equipo', 'V1 costo del periodo (Marketing, base seleccionada)', vv('Costo del periodo (MXN)'), base_if(float(camp.costo_ent[mk].sum()), float(camp.costo_env[mk].sum())), VE_NOTE)
add('Vista_equipo', 'Vista_equipo', 'V1 ahorro al mes (Marketing, base seleccionada)', vv('Ahorro al mes si se ejecuta el plan (MXN)'), base_if(float(camp.ahorro_mes_ent[mk].sum()), float(camp.ahorro_mes_env[mk].sum())), VE_NOTE + ' ' + DEF)
add('Vista_equipo', 'Vista_equipo', 'V1 respuesta email (Marketing)', vv('Respuesta email (clics / entregados)'), float(camp.ec[mk].sum() / camp.ed[mk].sum()), VE_NOTE, 1e-6)
add('Vista_equipo', 'Vista_equipo', 'V1 emails promocionales a dados de baja (Marketing)', vv('Emails promocionales a usuarios ya dados de baja (E5b)'), float(e5bt.em[e5bt.equipo == 'Marketing'].sum()), VE_NOTE + ' Igual que E_DespuesBaja E3.')
add('Vista_equipo', 'Vista_equipo', 'V2 total campañas del equipo (Marketing)', f'=Vista_equipo!$B${v2b}', int(mk.sum()), VE_NOTE)
add('Vista_equipo', 'Vista_equipo', 'V2 total ahorro al mes del equipo (Marketing, base seleccionada)', f'=Vista_equipo!${LV2["ahorro al mes (MXN)"]}${v2b}', base_if(float(camp.ahorro_mes_ent[mk].sum()), float(camp.ahorro_mes_env[mk].sum())), VE_NOTE + ' ' + DEF)
add('Vista_equipo', 'Vista_equipo', 'V3 suma de campañas por canal (Marketing)', f'=SUM(Vista_equipo!$B${v3a}:$B${v3b})', int(mk.sum()), VE_NOTE)
add('Vista_equipo', 'Vista_equipo', 'V4 filas de estándares', f'=COUNTA(Vista_equipo!$A${v4a}:$A${v4b})', len(EST), '')
add('Vista_equipo', 'Vista_equipo', 'V4 valor del equipo, estándar #3 clic de email (Marketing)', f'=Vista_equipo!$C${v4a + 2}', float(camp.ec[mk].sum() / camp.ed[mk].sum()), VE_NOTE, 1e-6)
add('Vista_equipo', 'Vista_equipo', 'V4 valores del equipo con error de fórmula', f'=SUMPRODUCT(--ISERROR(Vista_equipo!$C${v4a}:$C${v4b}))', 0, 'Debe ser 0.')

# ----- escribir Verificación
H = ['#', 'grupo', 'pestaña', 'qué se comprueba', 'valor en este Sheets (fórmula)', 'valor esperado (pandas sobre el CSV)', 'diferencia (debe ser 0)', 'estado', 'qué significa la cifra y por qué puede diferir', 'tolerancia']
for j, h in enumerate(H, start=1): ver.cell(1, j, h).font = bold
for i, (g, t, q, f, exp, ex, tol) in enumerate(V, start=2):
    ver.cell(i, 1, i - 1); ver.cell(i, 2, g); ver.cell(i, 3, t); ver.cell(i, 4, q); ver.cell(i, 5, f); ver.cell(i, 6, exp)
    ver.cell(i, 7, f'=IF(AND(ISNUMBER(E{i}),ISNUMBER(F{i})),E{i}-F{i},"")')
    ver.cell(i, 8, f'=IF(ISERROR(E{i}),"error en fórmula",IF(NOT(ISNUMBER(E{i})),"vacío",IF(ABS(G{i})<=J{i},"ok","REVISAR")))')
    ver.cell(i, 9, ex); ver.cell(i, 10, tol)
    for col in (5, 6, 7): ver.cell(i, col).number_format = '#,##0.00' if tol >= 0.5 else '0.000000'
n = len(V) + 1
ver.cell(n + 2, 4, 'Resumen').font = bold
ver.cell(n + 3, 4, 'Filas ok'); ver.cell(n + 3, 5, f'=COUNTIF(H2:H{n},"ok")')
ver.cell(n + 4, 4, 'Filas a REVISAR'); ver.cell(n + 4, 5, f'=COUNTIF(H2:H{n},"REVISAR")')
ver.cell(n + 5, 4, 'Filas con error de fórmula'); ver.cell(n + 5, 5, f'=COUNTIF(H2:H{n},"error en fórmula")')
ver.cell(n + 6, 4, 'Filas vacías (la fórmula devolvió texto o vacío)'); ver.cell(n + 6, 5, f'=COUNTIF(H2:H{n},"vacío")')
ver.cell(n + 7, 4, 'Filas que dependen de los parámetros default (si los cambias, salen REVISAR a propósito)'); ver.cell(n + 7, 5, f'=COUNTIF(I2:I{n},"Válido con los parámetros default*")')
ver.freeze_panes = 'A2'; ver.auto_filter.ref = f'A1:J{n}'
for col, w in zip('ABCDEFGHIJ', (5, 14, 16, 62, 22, 22, 16, 18, 110, 10)): ver.column_dimensions[col].width = w

# =====================================================================================
# ---------- Léeme
# =====================================================================================
R = []
R.append(['Auditoría Braze Kueski: datos, catálogo, campañas y cálculo por lente (archivo ' + VERSION + ', etapa 3 de 3)'])
R.append(['Cambios v3 respecto a v2b', 'Cuatro pestañas nuevas al frente: Vista_equipo (selector en B2), Insights (una sola pestaña con filtros), Plan_accion y Estándares. En Campañas se agregó la columna costo_mxn_mes (costo del periodo / meses con envíos, solo activas en septiembre) para los totales "al mes" del plan. Parámetros!B20 (clic mínimo in-app para quitar la pieza) ahora se usa como estándar #8. Verificación creció con un bloque para las pestañas nuevas. Nada de v2b cambió de lugar ni de fórmula.'])
R.append(['Cambios v2b respecto a v2', 'En Google Sheets v2 salían 9 filas en REVISAR (181, 293, 294, 296, 297, 347 a 350). Causa única: la comunicación sin nombre de E1 llega como null en E7a, E7c, E9a y E8 y no cruzaba. Ahora se llama "(sin nombre)" en todas las pestañas y su ticket queda vacío. Nada más cambió.'])
R.append([''])
R.append(['Qué es este archivo', 'Todo lo de v1 (queries E1 a E9b pegadas completas, Parámetros, Verificación) más el Catálogo de familias, la tabla de Campañas (una fila por familia × canal con señal y acción), Medianas por canal y una pestaña de cálculo por lente (B, E, F, G, H, J, K, L, M). Todo es fórmula sobre las pestañas crudas: si cambias un parámetro o pegas datos nuevos, todo se recalcula. Más las cuatro pestañas de v3: Estándares y buenas prácticas, Insights con filtros, Plan de acción y Vista_equipo con selector.'])
R.append(['Fuente', 'analytics_engineering_production.xplore._dim_braze_users_and_communications (Databricks). Sin identificadores de usuario: todo viene agregado.'])
R.append(['Periodo', '1 de enero a 30 de septiembre de 2026 (event_date). E9b solo julio a septiembre.'])
R.append(['Fecha de corrida', f'Queries corridas por el usuario el {HOY}. E3, E4b, E7b y E9b en versión 2 (agregan WhatsApp entregado y quitan costo).'])
R.append(['Formato', 'Plano, sin colores. Pestañas crudas: encabezado en la fila 1, filtros, columnas derivadas marcadas "(derivada)" al final. Pestañas de cálculo: fila 1 título, fila 2 fuente, fila 3 supuestos y disclaimer, tablas desde la fila 4 con su título. Catálogo, Campañas y Medianas son tablas planas con encabezado en la fila 1.'])
R.append(['Cómo se verifica', f'Pestaña Verificación ({len(V)} filas): cada fila compara una cifra calculada aquí con fórmula contra la misma cifra calculada en pandas sobre el CSV original. Estado ok = la diferencia está dentro de la tolerancia (columna J; 0.5 para conteos y sumas, 0.000001 para proporciones). REVISAR = algo se pegó mal o una fórmula falló, SALVO en las filas marcadas "Válido con los parámetros default": esas comparan contra los defaults y salen REVISAR a propósito cuando cambias Parámetros (es la forma de ver que el cambio sí movió las cosas). Al volver los parámetros a su valor, deben regresar a ok.'])
R.append(['Tiempo de cálculo', f'Campañas tiene {len(camp):,} filas × {len(CAMP_COLS)} columnas con SUMIFS sobre E1 ({len(e1):,} filas) y el Catálogo {NC:,} filas. La primera vez que se abre en Google Sheets tarda de 1 a 3 minutos en calcular todo (aparece "Calculando..." arriba). Esperar a que termine antes de leer Verificación; si una fila dice "error en fórmula" o "Loading", esperar y volver a mirar.'])
R.append([''])
R.append(['Orden de las pestañas y qué hay en cada una', ''])
for name, desc in [
 ('Parámetros', 'Costos, base de cobro de WhatsApp (B6), mínimos de respuesta por canal (B11 a B14), reglas de acción (B15 a B19, B26 a B37) y la tabla de mapeo de equipos (abajo). Todo lo editable está aquí; ninguna pestaña de cálculo tiene números escritos a mano salvo las claves de familia en Catálogo, Campañas, L4 y M1.'),
 ('Vista_equipo', 'Elige el equipo en B2 (lista: Marketing, Product Growth, Sales, Collections, Others) y toda la pestaña se recalcula: V1 resumen (familias, campañas, envíos, costo, ahorro, respuesta por canal, E5b, E7a, E8), V2 campañas del equipo por acción, V3 por canal contra la mediana y el mínimo, V4 cada estándar con el valor del equipo y si cumple, V5 las 10 campañas con más envíos, V6 los 10 emails con más bajas por mil, V7 insights del equipo y los globales, V8 todas las campañas del equipo con acción (ticket e ids incluidos). V5 a V8 son listas vivas con SORT y FILTER.'),
 ('Insights', 'Una fila por hallazgo con filtros: lente (B, C, E, F, G, H, J, K, L, M), equipo ("todos" = toda la operación), producto, canal, tipo de hallazgo, hallazgo en una frase, cifra (fórmula viva que apunta a la celda de la lente ya verificada), unidad, fuente E, confianza, qué significa, qué hacer, estándar relacionado (# de Estándares) y celda de origen (la fórmula escrita como texto, para ir a verla).'),
 ('Plan_accion', 'P1 resumen por acción (campañas, activas, familias, envíos, mensajes al mes, costo, ahorro, orden sugerido y cómo se ejecuta en Braze); P2 totales (mensajes y costo al mes hoy, ahorro, % que se ahorra, campañas a tocar y a cuidar); P3 equipo × acción; P4 lista viva por campaña con ticket, communication_ids, por_qué, en orden de ahorro al mes y envíos (sin Seguir igual ni No tocar). Ahorro es un techo: supone apagar todo lo que tiene señal apagar o rehacer.'),
 ('Estándares', 'Una fila por métrica u operación (24): qué es, cómo se calcula aquí, valor actual (fórmula viva), estándar propuesto (columna G, EDITABLE: benchmark público, Parámetros o propuesta interna; la columna I dice cuál), sentido, brecha, estado (cumple o debajo), qué significa quedarse debajo, qué hacer, fuente E, supuestos, y columnas P a T con el valor por equipo (las métricas por usuario no se parten por equipo). Columna U cuenta cuántos equipos están debajo. Es la base del playbook.'),
 ('Catálogo', f'Una fila por familia ({NC:,}): ticket, communication_ids, versiones, equipo original y equipo mapeado, producto, canales, tipo, audiencia y gancho por nombre, primer y último mes, activa_sep, meses, envíos, costo, si está en E2 y las acciones que le salieron en Campañas. Para buscar una campaña por ticket (B0211, T2728) o por UUID, filtra aquí.'),
 ('Campañas', f'Una fila por familia × canal con envíos > 0 ({NCAMP:,}). Métricas crudas sumadas de E1, tasas, costo, señal (volumen × respuesta contra mínimo y mediana), motivo, ahorro si se apaga, bloque E7c (abren vs no abren, lift, mueve), E5b (emails a dados de baja), E7a (etapas), otros canales que sí responden, accion_tipo y por_qué en texto. Filtra por equipo, canal, señal o acción.'),
 ('Medianas', 'Por canal: mediana de envíos (corte de volumen alto), mediana de respuesta, mediana de conv_abren, conteo de familias por señal y por acción, envíos, costo y ahorro. Fila 7 totales.'),
 ('B_Canales', 'Lente B. Mes × canal (envíos, respuesta, bajas, costo), total por canal, concentración de mensajes por usuario (E4b) y entrega de WhatsApp por mes.'),
 ('E_DespuesBaja', 'Lente E. Cohorte de dados de baja por mes y qué email recibieron después (E5); emails a dados de baja por tipo y equipo de la familia (E5b); lista de familias promocionales que lo hicieron.'),
 ('F_Solape', 'Lente F. Cuántas familias distintas recibe un usuario el mismo día (E6a), por mes, y qué pares de equipos y de familias chocan (E6b).'),
 ('G_Practicas', 'Lente G. Respuesta por audiencia, gancho, tamaño del envío y toques por usuario (clasificación por nombre de la comunicación) y fatiga por banda de mensajes (E3).'),
 ('H_Etapas', 'Lente H. Envíos por etapa del usuario (golden record) × tipo y canal; promocional a etapas bloqueadas y a prospectos por equipo; las 40 familias que más lo hacen.'),
 ('J_Canal', 'Lente J. A qué canal responde cada usuario (16 combinaciones), cuántos no responden a nada, mensajes y costo a canal mudo. Enero a septiembre (E7b) y julio a septiembre (E9b).'),
 ('K_Abren', 'Lente K. Convierten los que abren contra los que no (E7c, por canal) y la lista de familias con muestra donde abrir no cambia la conversión.'),
 ('L_Baja', 'Lente L. Días y emails hasta la baja por cohorte (E8), bandas, familia que llegó el día de la baja con equipo y tipo, y resumen por equipo y tipo.'),
 ('M_Ventanas', 'Lente M. Igual que K con ventanas de conversión a 7, 30, 90 días y fin de periodo (E9a).'),
 ('E1 a E9b', 'Las 15 pestañas crudas, igual que en v1, con más columnas derivadas (ver tabla abajo).'),
 ('Verificación', 'Al final. Ver "Cómo se verifica".')]:
    R.append([name, desc])
R.append([''])
R.append(['Pestaña', 'Archivo CSV', 'md5 del CSV', 'Filas de datos', 'Grano', 'Qué contiene', 'Columnas derivadas', 'Celdas null convertidas a vacío (columna: cuántas)'])
for tab, fname, desc, grano, _ in TABS:
    i = INFO[tab]
    nul = ', '.join(f'{c_}: {n_}' for c_, n_ in i['nulls'].items() if n_) or 'ninguna'
    R.append([tab, fname, i['md5'], i['filas'], grano, desc, ', '.join(i['derived']) or 'ninguna', nul])
R.append([''])
R.append(['Columnas derivadas', ''])
R.append(['familia (derivada)', 'Nombre de la comunicación sin la fecha "-AAAAMMDD-" (REGEXREPLACE). Agrupa las copias que Braze crea con fecha distinta para la misma campaña. Si la comunicación no tiene nombre, queda "(sin nombre)": hay UNA sola comunicación sin nombre en E1 (su id está en la columna communication_ids del Catálogo; 325 mil envíos de email, equipo Others) y en E7a, E7c, E9a y E8 llega como null, así que con ese nombre cruza en todas las pestañas. Si algún día hubiera más de una, se juntarían en esa fila (Verificación lo vigila: "communication_id distintos sin nombre"). CORRECCIÓN respecto a v1: E5b, E6b, E7a y E7c traen la familia CON fecha (la query no la quitó), por eso tienen su propia columna familia (derivada) y todo cruce usa esa columna, nunca la original. E9a y E8 sí vienen sin fecha. La pestaña Verificación cuenta cuántas filas traen fecha en cada una. MAYÚSCULAS: hay familias que solo cambian en mayúsculas/minúsculas (por ejemplo "...-CuestaEnero-in-App" y "...-CuestaEnero-in-app", o "AmazonPrimeDays" y "AmazonPrimedays"); SUMIFS, COUNTIF y VLOOKUP de Sheets no distinguen mayúsculas, así que se tratan como UNA sola familia: en E1 son ' + str(CASE_PAIRS) + ' pares y el Catálogo tiene ' + str(NC) + ' filas (una por familia). En E8 (familia_dia_baja) hay una fila con clave vacía (null en la query, 1,227 usuarios de la cohorte 1): la columna familia (derivada) la nombra "(sin familia)" para que no se pierda.'])
R.append(['mes_clave y mes_num (derivadas)', 'mes_clave = primeros 7 caracteres de la fecha ("2026-06"). mes_num = el mes como número (6), para que MINIFS y MAXIFS calculen primer y último mes. En E4a las filas de grano semana llevan el mes de la fecha de inicio de la semana.'])
R.append(['equipo (derivada)', 'E1 trae 11 equipos (team). La tabla de mapeo al final de Parámetros los lleva a 5 para la vista por equipo: Marketing, Product Growth, Sales, Collections y Others (Compliance, Acquisition, CX, B2B, NPS y Security caen en Others). Es editable: cambia la columna B del mapeo y todo se recalcula. El Catálogo guarda también el equipo original.'])
R.append(['tipo (derivada)', 'cobranza si el equipo original es Collections; transaccional u operativa si el nombre empieza con "Transaccional" o no trae un ticket con forma -B0211- / -T2728- / -S0004-; promocional o lifecycle todo lo demás. Es una regla por nombre, no un dato de Braze: una familia promocional sin ticket queda como transaccional. Se puede corregir a mano en el Catálogo (la columna es fórmula; si la sobreescribes, anótalo aquí).'])
R.append(['audiencia y gancho (derivadas, E1)', 'Clasificación por palabras clave en el nombre, en este orden (gana la primera que coincide, sin distinguir mayúsculas). Audiencia: ' + '; '.join(f'{a} = {rx}' for a, rx in AUD) + '; otros. Gancho: ' + '; '.join(f'{g_} = {rx}' for g_, rx in GAN) + '; otros. Sirve para la lente G; es aproximada.'])
R.append(['banda_tamaño y banda_toques (derivadas, E1)', 'banda_tamaño por usuarios_aprox del mes: <10 mil, 10 a 100 mil, 100 mil a 1 M, 1 M+. banda_toques = envíos / usuarios_aprox del mes: 1 (<1.5), 2 (<2.5), 3 a 4 (<4.5), 5+. Vacío si usuarios_aprox es 0.'])
R.append(['par_equipos y ambas promocionales (E6b)', 'Par de equipos ordenado alfabéticamente ("Marketing + Product Growth") y 1 si las dos familias del par son promocionales. Para la tabla F3.'])
R.append([''])
R.append(['Cómo se calcula la señal y la acción de cada campaña (Campañas)', ''])
R.append(['respuesta', 'email = clic / entregado; push = apertura / enviado; WhatsApp = lectura / entregado; in-app = clic / impresión. Banner no tiene respuesta definida (queda vacío).'])
R.append(['volumen', 'alto si los envíos de la familia en ese canal son ≥ la mediana de envíos del canal (Medianas); bajo si no.'])
R.append(['señal', 'apagar o rehacer = volumen alto y respuesta < mínimo del canal (Parámetros B11 a B14). revisar = volumen alto y (respuesta < mediana del canal o bajas por mil entregados ≥ B26). proteger = volumen alto y respuesta ≥ mediana × B27. escalar = volumen bajo, envíos ≥ B29 y respuesta ≥ mediana × B28. Vacío = nada de lo anterior.'])
R.append(['mueve', 'Con muestra suficiente (abrieron ≥ B17, no abrieron ≥ B18, conversiones ≥ B19): mueve = 1 si conv_abren ≥ mediana conv_abren del canal / 2 y lift ≥ B16. Sin muestra: mueve = 1 si respuesta ≥ mínimo × B15.'])
R.append(['accion_tipo', 'En este orden: No tocar (cobranza o transaccional) → Confirmar apagado (señal apagar y no activa en septiembre) → Apagar (señal apagar y no mueve) → Limpiar base de WhatsApp o Rehacer o re-segmentar (señal apagar y sí mueve; WhatsApp va a limpiar) → Bajar frecuencia (señal revisar por bajas) → Limpiar base de WhatsApp o Rehacer o re-segmentar (señal revisar por respuesta) → Proteger → Escalar → sin señal pero activa: Bajar frecuencia (email o push con toques ≥ B30), Limpiar base de WhatsApp (WhatsApp con no entregado × costo ≥ B32), Rehacer o re-segmentar (email con ≥ B31 usuarios por envío) → Seguir igual.'])
R.append(['ahorro', 'ahorro_mxn_periodo = costo del periodo de las familias con señal apagar o rehacer que no sean No tocar. ahorro_mxn_mes = ese costo / meses con envíos, solo si la familia sigue activa en septiembre. msgs_mes_ahorrados = envíos por mes de esas familias. Es un techo: supone que se apaga todo, no solo lo que no mueve.'])
R.append(['Prueba rápida', 'Cambia Parámetros!B11 de 0.30 % a 0.50 %: en Campañas varias filas de email pasan de "revisar" o vacío a "apagar o rehacer" y su accion_tipo cambia; Medianas fila 2 (email) mueve sus conteos; en Verificación las filas marcadas "Válido con los parámetros default" salen REVISAR. Regrésalo a 0.30 % y todo vuelve a ok. Lo mismo con B6 (entregado / enviado): cambia costo_mxn, ahorro y las filas de costo en Verificación, que siguen en ok porque el esperado también lee B6.'])
R.append([''])
R.append(['Definiciones que hay que tener claras', ''])
R.append(['Respuesta por canal', 'email = clic (email_click); push = apertura (pn_open); WhatsApp = lectura (whatsapp_read); in-app = clic (in_app_click). La apertura de email NO cuenta como respuesta porque Apple Mail y Gmail abren los correos automáticamente y la inflan.'])
R.append(['"Nunca respondió" (E7b y E9b, fila con resp_email, resp_push, resp_wa y resp_inapp en 0)', 'Un usuario entra aquí si en TODO el periodo (enero a septiembre en E7b; julio a septiembre en E9b) no tuvo NI UN clic en ningún email, NI UNA apertura de ningún push, NI UNA lectura de ningún WhatsApp, NI UN clic en ningún in-app, en ninguna comunicación de ningún equipo. Sí recibió mensajes: las columnas msgs_* dicen cuántos (y msgs_wa_entregados cuántos WhatsApp le llegaron de verdad). No significa que no convirtió: usuarios_con_conversion cuenta los que convirtieron aun sin responder (por ejemplo entraron solos a la app). No significa que se dio de baja: eso lo dice usuarios_con_baja_email. Una apertura de email no lo saca de este grupo. Si tiene apagadas las confirmaciones de lectura de WhatsApp, aparece como no leído: la cifra es un techo.'])
R.append(['Canal mudo (J_Canal)', 'Para cada grupo de usuarios, un canal es mudo si ese grupo nunca respondió por él. Los mensajes que recibieron por ese canal son "mensajes a canal mudo". Incluye a los que no responden a nada (todos sus canales son mudos) y a los que responden a un canal pero reciben por otros.'])
R.append(['Bajas: dos cifras con nombre propio', 'CIFRA A, bajas usuario-mes = 457,376 (E4a, grano mes): un usuario cuenta en cada mes en que se dio de baja. CIFRA B, usuarios únicos con baja = 439,269 (E5 y E7b): cada usuario una vez. La diferencia (18 mil) son usuarios que se dieron de baja en más de un mes. E1 y E3 traen EVENTOS de baja (1.09 M), que no son usuarios. bajas_por_mil en Campañas = eventos de baja / emails entregados × 1000.'])
R.append(['Deduplicación de E1', 'E1 toma el máximo por usuario × comunicación × día, así que una fila repetida del mismo envío cuenta una vez. E3, E4b y E7b cuentan filas por usuario. Por eso E3 y E7b quedan 0.2 % arriba de E1 en email y 1.3 % en WhatsApp entregado. E1 manda en volumen por campaña; E3 y E7b mandan en distribución por usuario.'])
R.append(['usuarios_aprox', 'APPROX_COUNT_DISTINCT de Databricks: error típico de 1 a 2 %. Sumar usuarios_aprox de varias filas no da usuarios únicos. En Campañas, usuarios_aprox es la suma de los meses (sirve para toques = envíos / usuarios) y usuarios_por_envío el promedio por mes (sirve para el tamaño de audiencia).'])
R.append(['Conversión', 'Solo de referencia (is_converted poco confiable y casi solo Cash). conversiones_filas cuenta filas con is_converted; conversiones_fraccional reparte cada conversión entre las comunicaciones del día; usuarios_con_conversion (E7b) cuenta usuarios. La única conversión que se usa para decidir es la comparación "convierten los que abren vs los que no" dentro de la misma campaña (E7c, E9a), porque compara dos grupos del mismo envío.'])
R.append(['Costo', 'Siempre con fórmula desde Parámetros: email_sent × costo por email + WhatsApp (entregado por default, o enviado según B6) × costo por WhatsApp. Las columnas costo_mxn de E1 y E4a vienen de la query con WhatsApp sobre enviados y NO se usan. Costo fijo de Braze pendiente (B7 vacío). Diferencia contra las muestras anteriores (MUESTRA_B y C): ahí WhatsApp se cobró por enviado (71.9 M); aquí por entregado (58.3 M).'])
R.append(['Ticket', 'ticket_number viene de Braze (B0211, T2728, S0004). "Other" = sin ticket; el Catálogo lo saca del nombre con regex (-B0211-) cuando se puede. En Catálogo y Campañas está siempre junto a communication_ids para buscar la pieza en Braze.'])
R.append(['Etapa (E7a)', 'Golden record del usuario al momento del envío. Solo aparecen 3.Blacklist, 4.Kpay CC Freeze, 6.Reus or Arco, 7.Prospects y sin_golden; cubre 37 % de los envíos. Bloqueadas = 3, 4 y 6.'])
R.append(['E8 cohorte_limpia', '1 = el primer email del usuario cae dentro del periodo, los días hasta la baja son exactos. 0 = ya recibía antes de enero, los días se miden desde enero y están subestimados.'])
R.append([''])
R.append(['Supuestos de este archivo (aplican a todo cálculo)', ''])
for s_ in ['Costos: 0.05 MXN por email enviado y 1.00 MXN por WhatsApp entregado (Parámetros). Push e in-app sin costo variable. Costo fijo de Braze no incluido.',
           'WhatsApp se cobra por entregado porque Meta cobra por mensaje entregado. El selector B6 permite ver el escenario sobre enviados.',
           'Conteos de usuarios aproximados (APPROX_COUNT_DISTINCT); percentiles aproximados (PERCENTILE_APPROX).',
           'Familia = nombre sin fecha. Dos campañas con el mismo nombre y fecha distinta se tratan como una. El equipo, producto, audiencia y gancho de la familia son los de su primera fila en E1.',
           'Tipo (cobranza, transaccional u operativa, promocional o lifecycle) es una regla por nombre y equipo, no un dato de Braze.',
           'Señal y acción dependen de medianas: si cambian los datos o el periodo, una familia puede cambiar de señal aunque ella no haya cambiado. Por eso la señal se lee junto con el mínimo fijo.',
           'Las celdas "null" de Databricks se dejaron vacías para que SUM y MEDIAN funcionen.',
           'E6b trae solo 1,000 pares (LIMIT): sirve para ver los pares más grandes, no para totales.',
           'E8 familia_dia_baja tiene doble conteo (un usuario puede recibir varias familias el día de la baja).',
           'E1 cambia el denominador por canal: email y WhatsApp sobre entregados, push sobre enviados, in-app sobre impresiones.',
           'Las claves de familia en Catálogo, Campañas, L4 y M1 son estáticas (texto). Si se recarga una query con familias nuevas, hay que agregar las filas que falten; Verificación avisa (filas y sumas dejan de cuadrar).',
           'Una familia de E7a, una de E7c y una de E8 no están en E1 (nombre distinto): aparecen como "no está en E1" y no entran a Campañas.']:
    R.append(['', s_])
R.append([''])
R.append(['Cómo actualizar si se vuelve a correr una query', 'Pegar el CSV completo en su pestaña desde A1 (encabezado incluido), sin borrar las columnas derivadas; arrastrar las fórmulas derivadas hasta la última fila; si cambió el número de filas, los rangos de todas las fórmulas están acotados a la última fila actual y hay que extenderlos (lo más práctico es regenerar el archivo con scripts/build_sheets_v2.py); anotar aquí el nuevo md5 y la fecha.'])
R.append(['Cómo usar Vista_equipo', 'Cambia la celda B2 (lista desplegable). Lo que se recalcula al instante: V1 a V4. Las listas V5 a V8 (SORT y FILTER) tardan unos segundos. Si una lista dice "sin campañas", el equipo no tiene filas con ese criterio. Para compartir con un equipo: duplica la pestaña (clic derecho, Duplicar), fija B2 en su equipo y comparte el archivo; o pon B2 en su equipo y exporta a PDF.'])
R.append(['Pendiente del usuario', 'Costo fijo de Braze (Parámetros B7 vacío): falta saber a qué corresponden "$7,020 al mes" y "32,474 créditos". Con eso se prorratea por envío o por usuario activo (METRICAS, lente I).'])
R.append(['Qué sigue', 'Con el Sheets cerrado (v3 ok): 1) Playbook de Braze: nomenclatura (Equipo-Producto-Ticket-Fecha-Nombre-Canal), reglas de frecuencia y solapamiento, canal por usuario, etapas y suscripción excluidas, grupos de control, checklist antes de lanzar y guía para crear algo nuevo (a quién, por qué canal, cuántas veces, con qué gancho, cómo medir). Cada fila de Estándares se vuelve una regla. 2) Deck estilo consultor (business case): gráficas, qué funciona y qué no, insights, findings, costo de no hacer nada y plan con ahorro. Para "cuándo" (hora y día de la semana) hace falta una extracción nueva (E10); con las actuales solo se ve por mes y semana.'])
for i, row in enumerate(R, start=1):
    for j, v in enumerate(row, start=1):
        c_ = leeme.cell(i, j, v); c_.alignment = Alignment(wrap_text=True, vertical='top')
        if i == 1 or (len(row) >= 8 and j <= 8 and row[0] == 'Pestaña') or (len(row) == 2 and row[1] == ''): c_.font = bold
leeme.column_dimensions['A'].width = 34; leeme.column_dimensions['B'].width = 120
for col in 'CDEFGH': leeme.column_dimensions[col].width = 30

# ---------- orden final y guardar
# MINIFS, MAXIFS y TEXTJOIN necesitan el prefijo _xlfn. en el xlsx (estándar OOXML). Google Sheets lo quita al importar; LibreOffice lo exige.
_XLFN = re.compile(r'(?<![\w.])(MINIFS|MAXIFS|TEXTJOIN)\(')
for ws_ in [WS[n_] for n_ in CALC + NEW] + [ver]:
    for row_ in ws_.iter_rows():
        for c_ in row_:
            if isinstance(c_.value, str) and c_.value.startswith('=') and _XLFN.search(c_.value):
                c_.value = _XLFN.sub(r'_xlfn.\1(', c_.value)
wb._sheets = [leeme, par] + [WS[n_] for n_ in NEW] + [WS[n_] for n_ in CALC] + [INFO[t]['ws'] for t, *_ in TABS] + [ver]
wb.save(OUT)
print('guardado', OUT, os.path.getsize(OUT) // 1024, 'KB; filas verificación', len(V), '; familias', NC, '; campañas', NCAMP)
print('señales', camp.senal.value_counts().to_dict()); print('acciones', camp.accion.value_counts().to_dict())
print('ahorro mes ent', round(camp.ahorro_mes_ent.sum()), 'periodo ent', round(camp.ahorro_per_ent.sum()), 'msgs mes', round(camp.msgs_ahorro.sum()))
print('medianas env', med_env.round(0).to_dict(), 'resp', med_resp.round(5).to_dict(), 'conv', med_conv.round(5).to_dict())
