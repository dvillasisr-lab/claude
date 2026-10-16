# Lámina 3 (Plan / caso de negocio): cascada del gasto de septiembre al gasto resultante.
# Uso: cd braze-analysis && python3 <este script>. Calcula con s3_datos.py (misma carpeta) y escribe s3.json.
import json, subprocess, sys, os
H = os.path.dirname(os.path.abspath(__file__))
subprocess.run([sys.executable, os.path.join(H, 's3_datos.py')], check=True, stdout=subprocess.DEVNULL)
D = json.load(open(os.path.join(H, 's3_datos.json'))); T = D['T']; R = D['R']
m = lambda v: f'{v/1e6:.2f}'
pc = lambda v: f'{v*100:.0f} %'
EQS = {'Product Growth': 'Product Growth', 'Marketing': 'Marketing', 'Sales': 'Sales', 'Others': 'Others', 'Collections': 'Collections'}

INK, TXT, SEC, MARK, GRID = '#0B1220', '#3B4556', '#6B7484', '#A3AAB5', '#DDE2EA'
BLUE, GREEN, GREEN_L = '#1F4FD8', '#127A5B', '#7CC4A8'
F = 'font-family="Inter, system-ui, sans-serif"'

# filas: total, pasos seguros, subtotal, pasos a medir, total
rows = [dict(kind='total', lab='Gasto de septiembre', v=R['sep'])]
rows += [dict(kind='step', **t) for t in T if t['cert'] == 'seguro']
rows += [dict(kind='total', lab='Tras el recorte seguro', v=R['tras_seguro'])]
rows += [dict(kind='step', **t) for t in T if t['cert'] == 'medir']
rows += [dict(kind='total', lab='Gasto resultante', v=R['resultante'])]

X0, X1, VMAX = 262, 552, 4.5e6          # área de barras
sx = lambda v: X0 + (X1 - X0) * v / VMAX
TOPY, RH, BH = 58, 28.5, 16             # primera fila, alto de fila, grosor de barra
TEAMX = 618
o = [f'<svg viewBox="0 0 780 420" width="100%" role="img" '
     f'aria-label="Cascada del gasto de septiembre, {m(R["sep"])} M MXN al mes, al gasto resultante, {m(R["resultante"])} M. '
     f'Recorte seguro {m(R["seguro"])} M en siete palancas; recuperación a medir con grupo de control {m(R["medir"])} M en dos palancas. '
     f'A la derecha, el equipo que más aporta a cada palanca." xmlns="http://www.w3.org/2000/svg">',
     f'<rect width="780" height="420" fill="#FFFFFF"/>']
# leyenda (dos series) y encabezado de la columna de equipos
o.append(f'<rect x="0" y="6" width="12" height="12" rx="2" fill="{BLUE}"/>'
         f'<text x="18" y="16.5" {F} font-size="12" fill="{INK}"><tspan font-weight="600">Recorte seguro {m(R["seguro"])} M</tspan>'
         f'<tspan fill="{SEC}">: se corta en 1 a 60 días</tspan></text>')
o.append(f'<rect x="0.75" y="26.75" width="10.5" height="10.5" rx="2" fill="{GREEN_L}" stroke="{GREEN}" stroke-width="1.5"/>'
         f'<text x="18" y="36.5" {F} font-size="12" fill="{INK}"><tspan font-weight="600">Recuperación a medir {m(R["medir"])} M</tspan>'
         f'<tspan fill="{SEC}">: se corta solo si el grupo de control no recupera</tspan></text>')
o.append(f'<text x="{TEAMX}" y="50" {F} font-size="11.5" fill="{SEC}">Equipo que más aporta</text>')
# rejilla y eje
AX = TOPY + len(rows) * RH + 2
for t in range(0, 5):
    x = sx(t * 1e6)
    o.append(f'<line x1="{x:.1f}" y1="{TOPY - 6}" x2="{x:.1f}" y2="{AX}" stroke="{GRID}" stroke-width="1"/>')
    o.append(f'<text x="{x:.1f}" y="{AX + 14}" {F} font-size="11.5" fill="{SEC}" text-anchor="middle">{t if t else 0}{" M" if t else ""}</text>')
o.append(f'<text x="{X1 + 40}" y="{AX + 14}" {F} font-size="11.5" fill="{SEC}" text-anchor="start">MXN al mes</text>')
o.append(f'<line x1="{X0}" y1="{TOPY - 6}" x2="{X0}" y2="{AX}" stroke="{MARK}" stroke-width="1"/>')

run = R['sep']; prev_x = None
for i, r in enumerate(rows):
    yc = TOPY + i * RH + RH / 2; yb = yc - BH / 2
    if r['kind'] == 'total':
        x0, x1 = sx(0), sx(r['v']); fill, stroke = MARK, None
        lab_w = '600'; val = f'{m(r["v"])} M'
        if r['lab'] == 'Gasto resultante':
            val += f' ({pc(r["v"] / R["sep"])} de septiembre)'
        tip = f'{r["lab"]}: {m(r["v"])} M MXN al mes'
        edge = x1
    else:
        x1 = sx(run); run -= r['mxn']; x0 = sx(run)
        if x1 - x0 < 2: x0 = x1 - 2
        fill = BLUE if r['cert'] == 'seguro' else GREEN_L; stroke = None if r['cert'] == 'seguro' else GREEN
        lab_w = '400'; val = f'{m(r["mxn"])}'
        tip = f'{r["lab"]}: {m(r["mxn"])} M MXN al mes; ' + ', '.join(f'{k} {v/1e6:.2f}' for k, v in r['eq'].items() if v > 500)
        edge = x0
    o.append(f'<g><title>{tip}</title>')
    o.append(f'<text x="{X0 - 10}" y="{yc + 4.3:.1f}" {F} font-size="12.5" font-weight="{lab_w}" fill="{INK if r["kind"] == "total" else TXT}" text-anchor="end">{r["lab"]}</text>')
    if stroke:
        o.append(f'<rect x="{x0 + .75:.1f}" y="{yb + .75:.1f}" width="{x1 - x0 - 1.5:.1f}" height="{BH - 1.5}" rx="2" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
    else:
        o.append(f'<rect x="{x0:.1f}" y="{yb:.1f}" width="{x1 - x0:.1f}" height="{BH}" rx="2" fill="{fill}"/>')
    # valor a la derecha del extremo derecho de la barra
    o.append(f'<text x="{x1 + 6:.1f}" y="{yc + 4.5:.1f}" {F} font-size="13" font-weight="{"600" if r["kind"] == "total" else "400"}" fill="{INK}">{val}</text>')
    # conector desde la fila anterior
    if prev_x is not None:
        o.append(f'<line x1="{prev_x:.1f}" y1="{yb - (RH - BH):.1f}" x2="{prev_x:.1f}" y2="{yb:.1f}" stroke="{MARK}" stroke-width="1"/>')
    prev_x = x0 if r['kind'] == 'step' else edge
    if r['kind'] == 'step':
        o.append(f'<text x="{TEAMX}" y="{yc + 4.3:.1f}" {F} font-size="12" fill="{TXT}">{EQS[r["top"]]} <tspan fill="{SEC}">{pc(r["top_sh"])}</tspan></text>')
    o.append('</g>')
o.append('</svg>')
svg = ''.join(o)

eq = R['eq']; sh = R['eq_sh']; tot = R['total']
pg_sin_dup = eq['Product Growth'] - [t for t in T if t['k'] == 'duplicados'][0]['eq']['Product Growth']
out = {
 "seccion": "Plan · Caso de negocio",
 "titulo": f"Corregirlo vale hasta {tot/1e6:.1f} M MXN al mes, y casi dos tercios se cortan sin riesgo",
 "que": "Promoción por el canal caro a quien no responde (Tasa 0, cross sell, ofertas a ex clientes), pruebas internas, duplicados del mismo día y envíos a bloqueados. Cobranza y transaccional no se tocan.",
 "quien": f"Product Growth {pg_sin_dup/1e6:.2f} M ({pg_sin_dup/tot*100:.0f} %) más los duplicados, Marketing {eq['Marketing']/1e6:.2f} M ({sh['Marketing']*100:.0f} %), Sales {eq['Sales']/1e6:.2f} M ({sh['Sales']*100:.0f} %), Others {eq['Others']/1e6:.2f} M.",
 "a_quien": "Leads y registrados sin crédito, ex clientes (churn, dormants, inactivos), bloqueados y quien no responde por ese canal en 90 días.",
 "lecturas": [
   f"{m(tot)} M MXN al mes es {pc(R['pct_sep'])} del gasto de septiembre ({m(R['sep'])} M) y {pc(R['pct_avg'])} del gasto mensual promedio de enero a septiembre ({R['avg']/1e6:.1f} M). Al año son {R['anual']/1e6:.1f} M MXN.",
   f"{m(R['seguro'])} M al mes ({R['anual_seg']/1e6:.1f} M al año) se cortan sin riesgo. Lo más grande es apagar el canal caro a leads y registrados que no responden: {m([t for t in T if t['k']=='ap_act'][0]['mxn'])} M, casi todo de Product Growth.",
   f"{m(R['medir'])} M al mes ({R['anual_med']/1e6:.1f} M al año) son ex clientes y personas sin respuesta en 90 días; {m(R['eq_medir']['Product Growth'])} M son de Product Growth. Se mide con grupo de control antes de cortar."],
 "causa": "No hay piso de respuesta ni grupo de control obligatorio, así que nadie apaga el canal caro aunque la persona nunca lo lea.",
 "sowhat": f"Aprobar hoy el recorte seguro de {m(R['seguro'])} M al mes y decidir los {m(R['medir'])} M de recuperación con el grupo de control en dos meses.",
 "fuente": "Fuente: E1 por campaña, canal y mes (septiembre 2026, incluye lecturas registradas el mes siguiente), acciones del Sheets v4, E9b (respuesta en 90 días), E7a (bloqueados), E6b (duplicados); WhatsApp a 1.00 MXN por entregado, email a 0.05 por enviado.",
 "svg": svg,
}
json.dump(out, open(os.path.join(H, 's3.json'), 'w'), ensure_ascii=False, indent=1)
open(os.path.join(H, 's3.svg'), 'w').write(svg)
print(json.dumps({k: v for k, v in out.items() if k != 'svg'}, ensure_ascii=False, indent=1))
