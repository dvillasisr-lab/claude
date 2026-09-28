#!/usr/bin/env python3
"""Regenerates library/CATALOG.md from library/skills and the plugin sources.
Run library/fetch-source.sh all first so the plugin repos are in /tmp/skill-sources."""
import glob, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = "/tmp/skill-sources"
SOURCES = [
    ("superpowers", "obra/superpowers", "Workflow de ingenieria: planear, TDD, debugging, code review, worktrees", ["skills/*/SKILL.md"]),
    ("mattpocock", "mattpocock/skills", "Ingenieria y productividad: specs, tickets, TDD, arquitectura, escritura", ["skills/*/*/SKILL.md"]),
    ("marketing", "coreyhaines31/marketingskills", "Marketing: SEO, copy, CRO, ads, emails, pricing, lanzamientos", ["skills/*/SKILL.md"]),
    ("caveman", "JuliusBrussee/caveman", "Respuestas comprimidas para ahorrar tokens, refactors seguros, reviews", ["skills/*/SKILL.md", "agents/*.md"]),
    ("voltagent", "VoltAgent/awesome-claude-code-subagents", "161 subagentes especializados por categoria", ["categories/*/*.md"]),
    ("ecc", "affaan-m/ECC", "Sistema de ingenieria completo: 292 skills y 68 agentes (muy grande)", ["skills/*/SKILL.md", "agents/*.md"]),
]

def meta(path):
    text = open(path, encoding="utf-8", errors="ignore").read()
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    if not m:
        return None, None
    fm = m.group(1)
    name = re.search(r"^name:\s*(.+)$", fm, re.M)
    desc = re.search(r"^description:\s*(>-?|\|)?\s*(.*?)(?=^\S[\w-]*:|\Z)", fm, re.M | re.S)
    d = " ".join(desc.group(2).split()).strip("\"'") if desc else ""
    if len(d) > 160:
        d = d[:157].rsplit(" ", 1)[0] + "..."
    return (name.group(1).strip().strip("\"'") if name else None), d

def short(d, n=90):
    return d if len(d) <= n else d[:n - 3].rsplit(" ", 1)[0] + "..."

out = ["# Catalogo de skills y agentes", "",
       "Nada de esto se carga solo. Leer este indice, elegir, y abrir solo el SKILL.md o agente elegido.", "",
       "## Locales: leer `library/skills/<nombre>/SKILL.md`", ""]
for f in sorted(glob.glob(os.path.join(ROOT, "skills/*/SKILL.md"))):
    n, d = meta(f)
    out.append(f"- **{os.path.basename(os.path.dirname(f))}**: {short(d)}")

out += ["", "## Fuentes externas: detalle en `library/catalog/<fuente>.md`", "",
        "Antes de leer un archivo de una fuente: `library/fetch-source.sh <fuente>` (clona en /tmp/skill-sources/<fuente>).", ""]
os.makedirs(os.path.join(ROOT, "catalog"), exist_ok=True)
for key, repo, blurb, pats in SOURCES:
    base = os.path.join(SRC, key)
    rows = []
    for pat in pats:
        for f in sorted(glob.glob(os.path.join(base, pat))):
            if os.path.basename(f).upper() == "README.MD":
                continue
            n, d = meta(f)
            if n:
                rows.append(f"| {n} | {d.replace('|', '/')} | `{os.path.relpath(f, base)}` |")
    out.append(f"- **{key}** ({len(rows)}): {blurb}")
    doc = [f"# {key} ({repo})", "", blurb, "",
           f"Traer con `library/fetch-source.sh {key}`. Rutas relativas a `{base}`.", "",
           "| Nombre | Para que | Archivo |", "|---|---|---|"] + rows
    open(os.path.join(ROOT, "catalog", key + ".md"), "w").write("\n".join(doc) + "\n")

open(os.path.join(ROOT, "CATALOG.md"), "w").write("\n".join(out) + "\n")
print("CATALOG.md:", len(out), "lines")
