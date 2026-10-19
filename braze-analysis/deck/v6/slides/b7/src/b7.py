"""Base común del bloque 7 (láminas 66 a 85): carga de datos, clasificadores por nombre, ayuda para SVG y escritura de JSON.
Clasificadores de tema y etapa copiados de scratchpad/v6parts/p5/common.py (los que usó el guion). WhatsApp por entregado."""
import sys, re, json, html, pathlib
sys.path.insert(0, "/home/user/claude/braze-analysis/scripts")
import pandas as pd, numpy as np
from deck_data import _fam, team_of

R = "/home/user/claude/braze-analysis/"
D = R + "data/"
H = R + "hallazgos/"
OUT = pathlib.Path(R + "deck/v6/slides/b7")
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40); pd.set_option("display.max_colwidth", 90); pd.set_option("display.max_rows", 200)

MIN = {"email": 0.3, "push notification": 0.75, "whatsapp": 60.0, "in-app": 10.0}
RESP = {"email": ("email_delivery", "email_click"), "push notification": ("pn_send", "pn_open"),
        "whatsapp": ("whatsapp_delivery", "whatsapp_read"), "in-app": ("in_app_impression", "in_app_click")}
CHN = {"email": "Email", "push notification": "Push", "whatsapp": "WhatsApp", "in-app": "In-app", "banner": "Banner"}
TEAMS = ["Product Growth", "Marketing", "Sales", "Collections", "Others"]
MINTXT = "Lo mínimo aceptable: 3 clics por cada mil correos, 7.5 aperturas por cada mil push, 6 de cada 10 WhatsApp leídos o 1 de cada 10 in-app con clic."
MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep"]


def load_e1():
    e = pd.read_csv(D + "e1_comunicacion_mes_canal.csv", low_memory=False)
    e["communication_name"] = e.communication_name.fillna("")
    e["fam"] = e.communication_name.map(_fam)
    e["equipo"] = e.team.map(team_of)
    e["m"] = e.mes.str[5:7].astype(int)
    e["costo"] = 0.05 * e.email_sent.fillna(0) + 1.0 * e.whatsapp_delivery.fillna(0)
    e["base"] = np.select([e.canal.eq(c) for c in RESP], [e[b] for b, _ in RESP.values()], 0)
    e["resp"] = np.select([e.canal.eq(c) for c in RESP], [e[r] for _, r in RESP.values()], 0)
    return e


TEMAS = [
 ("Prueba o copia", r"^qa|[-_ ]qa[-_ ]|prueba|\btest|copy of"),
 ("Cobranza", r"bkt|precobranza|cobranza"),
 ("Transaccional", r"transaccional-|payment.confirmation|contracts|account.statement|disbursed|rechazo|payment received|advance payment|^cr - |late.fee|domic|subscription|autopay|paymentreminder|rollout 95"),
 ("BillPay y recargas", r"billpay|billpayment|topup"),
 ("Recordatorio de registro", r"veriff|personalinfo|\bnip\b|_nip|nip_|leftfunnel|endtoend|registro|credencial|accountcreation|requestinfo"),
 ("Referidos", r"referral|referid"),
 ("Tasa 0", r"tasa.?0"),
 ("Oferta para volver", r"consinoferta|conoferta|sinoferta|descuentodirecto|descuentoescalonado|lazaro|segundaoportunidad|rescate"),
 ("Promociones de comercios KPay", r"comercio|merchant|hotsale|temu|amazon|adidas|cuponera|ventaazul|privalia|palacio|cashback|flashsale|promotor|kueski(nuevo|final|verano|julio|fit)|qsi|viva|chedraui|oferta50|vuelos|liverpool|coppel|walmart|shein|sale"),
 ("Uso y recompra del crédito", r"installment|increaseutilization|montopreaprobado|transaccionalidad|tardan|retargeting_offering|retargetingoffering|cancel"),
 ("Fechas y temporadas", r"christmas|reyes|cuestaenero|mundial|diapadres|diamadres|fiestas|aniversario|felicit|cumple|buenfin|navidad"),
 ("Sorteos y concursos", r"anotaygana|sorteo|concurso"),
 ("Venta cruzada KPay y KCash", r"xsell|cross"),
 ("Novedades y recomendaciones", r"weekly|newsletter|recommend|novedad|lanzamiento|intro|insignia|mejorespracticas|survey|narrativavalue|nuevaimagen"),
]


def tema(name):
    n = (name if isinstance(name, str) else "").lower()
    for t, p in TEMAS:
        if re.search(p, n): return t
    return "Otro"


def etapa(name):
    n = (name if isinstance(name, str) else "").lower()
    if re.search(r"bkt|precobranza", n): return "En cobranza"
    if re.search(r"dormant|churn|inactiv|lazaro", n): return "Ex clientes inactivos"
    if re.search(r"neveractive|nevercash|registradospay|nuevos|onboard", n): return "Registrados sin crédito o nuevos"
    if re.search(r"lead|leftfunnel|anonim|bbdd|bdd|rezagad|prospect", n): return "Leads (no terminaron registro)"
    if re.search(r"recurrent|recurent|active|activo|cliente|eligible", n): return "Clientes activos y recurrentes"
    if re.search(r"todos|portfolio|portafolio|ecosistema", n): return "Todos (sin segmento)"
    return "Sin dato en el nombre"


def load_c():
    c = pd.read_csv(H + "muestra_c_familias.csv")
    c["costo_ent"] = np.where(c.canal == "whatsapp", c.envios * c.entrega_pct.fillna(0) / 100, c.costo_mxn)
    c["equipo"] = c.team.map(team_of); c["tema"] = c.familia.map(tema); c["etapa"] = c.familia.map(etapa)
    return c


# ---------------- SVG ----------------
INK, TXT, SEC, MARK, MARK2, GRID = "#0B1220", "#3B4556", "#6B7484", "#A3AAB5", "#C9CED6", "#DDE2EA"
BLUE, BLUEL, GREEN, GREENL = "#1F4FD8", "#8FA8EE", "#127A5B", "#7CC4A8"
FF = "Inter, system-ui, sans-serif"
E = lambda s: html.escape(str(s), quote=False)


class SVG:
    def __init__(self, label, W=780, Hh=420):
        self.o = [f'<svg viewBox="0 0 {W} {Hh}" width="100%" role="img" aria-label="{html.escape(label)}" font-family="{FF}">']

    def t(self, x, y, s, size=11.5, fill=TXT, anchor="start", w=400, halo=False, italic=False):
        h = ' stroke="#FFFFFF" stroke-width="4" stroke-linejoin="round" paint-order="stroke"' if halo else ""
        it = ' font-style="italic"' if italic else ""
        self.o.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{w}"{h}{it}>{E(s)}</text>')

    def tspans(self, x, y, parts, size=11.5, anchor="start", halo=False):
        """parts = [(texto, color, peso)]"""
        h = ' stroke="#FFFFFF" stroke-width="4" stroke-linejoin="round" paint-order="stroke"' if halo else ""
        sp = "".join(f'<tspan fill="{c}" font-weight="{w}">{E(s)}</tspan>' for s, c, w in parts)
        self.o.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}"{h}>{sp}</text>')

    def rect(self, x, y, w, h, fill, extra=""):
        self.o.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w, 0):.1f}" height="{max(h, 0):.1f}" fill="{fill}"{extra}/>')

    def line(self, x1, y1, x2, y2, stroke=GRID, sw=1, extra=""):
        self.o.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{extra}/>')

    def circle(self, cx, cy, r, fill, stroke="#FFFFFF", sw=1.5, extra=""):
        self.o.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{extra}/>')

    def raw(self, s):
        self.o.append(s)

    def legend(self, items, x=0, y=14, gap=16, size=11.5):
        """items = [(texto, color, forma)] forma: 'sq', 'ci', 'ln'"""
        for lab, col, sh in items:
            if sh == "ci": self.circle(x + 5, y - 4, 5, col, sw=0)
            elif sh == "ln": self.line(x, y - 4, x + 14, y - 4, col, 2.5)
            elif sh == "ring": self.circle(x + 5, y - 4, 4.5, "#FFFFFF", col, 1.8)
            else: self.rect(x, y - 9, 10, 10, col)
            dx = 18 if sh == "ln" else 15
            self.t(x + dx, y, lab, size, TXT)
            x += dx + len(lab) * size * 0.53 + gap
        return x

    def out(self):
        return "".join(self.o) + "</svg>"


def write(n, d):
    d = dict(n=n, **d)
    d.setdefault("kind", "grafica")
    txt = json.dumps(d, ensure_ascii=False, indent=1)
    for bad in ("—", "–", "→", "←"):
        assert bad not in txt, (n, bad)
    (OUT / f"{n:03d}.json").write_text(txt, encoding="utf-8")
    print("escrito", n)


def M(v, d=1):
    return f"{v/1e6:.{d}f}"


def num(v, d=0):
    return f"{v:,.{d}f}"
