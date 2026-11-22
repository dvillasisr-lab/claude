#!/usr/bin/env python3
"""Valora el inventario sellado de Pokemon con precios de TCGplayer (via tcgcsv.com).

Uso:
    python3 value.py                 # precios de hoy + tendencia 7/30/90 dias
    python3 value.py --no-history    # solo precios de hoy (sin descargar archivos)

Salida: report.csv (una fila por producto) y un resumen en pantalla.
Dependencia opcional para la tendencia: pip install py7zr
Precio usado: marketPrice de TCGplayer (USD); si falta, midPrice o lowPrice.
"""
import argparse, csv, datetime as dt, io, json, os, sys, tempfile, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "pokemon-stock-tracker/0.1"}
CAT = 3  # Pokemon en TCGplayer
HIST_DAYS = (7, 30, 90)


def get(url, timeout=60):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()


def jget(url):
    return json.loads(get(url))


def pick(row):
    for k in ("marketPrice", "midPrice", "lowPrice"):
        if row.get(k):
            return float(row[k])
    return None


def load_inventory():
    with open(os.path.join(HERE, "inventory.csv"), newline="") as f:
        out = []
        for r in csv.DictReader(f):
            r["qty"] = int(r["qty"])
            r["paid_each_mxn"] = float(r["paid_each_mxn"])
            r["collectr_total_mxn"] = float(r["collectr_total_mxn"]) if r.get("collectr_total_mxn") else None
            r["items"] = [(int(g), n) for g, n in (x.split(":", 1) for x in r["tcgplayer"].split("|"))]
            out.append(r)
        return out


def resolve_products(groups):
    """(group, name) -> productId. Nombre exacto; falla fuerte si no existe o es ambiguo."""
    by_name = {}
    for g in groups:
        for p in jget(f"https://tcgcsv.com/tcgplayer/{CAT}/{g}/products")["results"]:
            by_name.setdefault((g, p["name"]), []).append(p["productId"])
    return by_name


def prices_today(groups):
    out = {}
    for g in groups:
        for p in jget(f"https://tcgcsv.com/tcgplayer/{CAT}/{g}/prices")["results"]:
            if p["subTypeName"] == "Normal":
                out[p["productId"]] = pick(p)
    return out


def prices_on(date, groups):
    """Precios de una fecha pasada desde el archivo diario (7z). None si no esta disponible."""
    try:
        import py7zr
    except ImportError:
        return None
    url = f"https://tcgcsv.com/archive/tcgplayer/prices-{date}.ppmd.7z"
    try:
        data = get(url, timeout=120)
    except Exception:
        return None
    want = [f"{date}/{CAT}/{g}/prices" for g in groups]
    with tempfile.TemporaryDirectory() as tmp:
        with py7zr.SevenZipFile(io.BytesIO(data)) as z:
            names = set(z.getnames())
            z.extract(path=tmp, targets=[w for w in want if w in names])
        out = {}
        for w in want:
            fp = os.path.join(tmp, w)
            if os.path.exists(fp):
                for p in json.load(open(fp))["results"]:
                    if p["subTypeName"] == "Normal":
                        out[p["productId"]] = pick(p)
        return out


def fx_mxn_per_usd():
    d = jget("https://api.frankfurter.dev/v1/latest?base=USD&symbols=MXN")
    return d["rates"]["MXN"], d["date"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-history", action="store_true")
    a = ap.parse_args()

    inv = load_inventory()
    groups = sorted({g for r in inv for g, _ in r["items"]})
    names = resolve_products(groups)
    today = prices_today(groups)
    fx, fx_date = fx_mxn_per_usd()

    hist = {}
    if not a.no_history:
        for d in HIST_DAYS:
            date = (dt.date.today() - dt.timedelta(days=d)).isoformat()
            hist[d] = prices_on(date, groups)
            if hist[d] is None:
                print(f"  (sin historial a {d} dias: instala py7zr o el archivo no existe)", file=sys.stderr)

    rows, problems = [], []
    for r in inv:
        pids, usd, usd_hist = [], 0.0, {d: 0.0 for d in HIST_DAYS}
        ok, hist_ok = True, {d: True for d in HIST_DAYS}
        for g, n in r["items"]:
            ids = names.get((g, n), [])
            if len(ids) != 1:
                problems.append(f"{r['product']} / {r['collection']}: '{n}' -> {len(ids)} coincidencias")
                ok = False
                continue
            pid = ids[0]
            pids.append(str(pid))
            p = today.get(pid)
            if p is None:
                problems.append(f"{r['product']} / {r['collection']}: sin precio hoy para {pid}")
                ok = False
                continue
            usd += p
            for d in HIST_DAYS:
                hp = (hist.get(d) or {}).get(pid)
                if hp is None:
                    hist_ok[d] = False
                else:
                    usd_hist[d] += hp
        paid = r["paid_each_mxn"] * r["qty"]
        row = {
            "producto": r["product"], "coleccion": r["collection"], "cantidad": r["qty"],
            "pagado_total_mxn": round(paid, 2),
            "tcgplayer_ids": "|".join(pids),
            "precio_usd_c/u": round(usd, 2) if ok else "",
            "valor_usd": round(usd * r["qty"], 2) if ok else "",
            "valor_mxn": round(usd * r["qty"] * fx, 2) if ok else "",
        }
        row["ganancia_mxn"] = round(row["valor_mxn"] - paid, 2) if ok else ""
        row["ganancia_pct"] = round(100 * (row["valor_mxn"] / paid - 1), 1) if ok and paid else ""
        for d in HIST_DAYS:
            if ok and hist_ok[d] and usd_hist[d]:
                row[f"cambio_{d}d_pct"] = round(100 * (usd / usd_hist[d] - 1), 1)
            else:
                row[f"cambio_{d}d_pct"] = ""
        row["collectr_mxn"] = r["collectr_total_mxn"] if r["collectr_total_mxn"] is not None else ""
        row["nota"] = "aprox: suma de 2 productos" if len(r["items"]) > 1 else ""
        if "Case" in r["tcgplayer"] and r["product"] == "Display":
            row["nota"] = "aprox: Display valuado con el precio del Case"
        rows.append(row)

    out = os.path.join(HERE, "report.csv")
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    tot_paid = sum(x["pagado_total_mxn"] for x in rows)
    valued = [x for x in rows if x["valor_mxn"] != ""]
    tot_mxn = sum(x["valor_mxn"] for x in valued)
    tot_usd = sum(x["valor_usd"] for x in valued)
    paid_valued = sum(x["pagado_total_mxn"] for x in valued)
    print(f"Tipo de cambio: {fx} MXN/USD ({fx_date})")
    print(f"Filas valuadas: {len(valued)}/{len(rows)}")
    print(f"Pagado (valuadas): ${paid_valued:,.0f} MXN | Pagado (total hoja): ${tot_paid:,.0f} MXN")
    print(f"Valor hoy TCGplayer: ${tot_usd:,.2f} USD = ${tot_mxn:,.0f} MXN")
    print(f"Ganancia vs pagado: ${tot_mxn - paid_valued:,.0f} MXN ({100 * (tot_mxn / paid_valued - 1):.1f}%)")
    for p in problems:
        print("  PROBLEMA:", p)
    print(f"-> {out}")


if __name__ == "__main__":
    main()
