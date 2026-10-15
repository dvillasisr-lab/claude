"""Convierte un markdown sencillo (encabezados, párrafos, listas, tablas, negritas, código) a .docx.

Uso: python3 scripts/md_to_docx.py entrada.md salida.docx
"""
import re
import sys

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor, Cm

INLINE = re.compile(r'(\*\*.+?\*\*|`[^`]+`)')


def add_runs(par, text, base_size=None):
    for part in INLINE.split(text):
        if not part:
            continue
        if part.startswith('**') and part.endswith('**'):
            r = par.add_run(part[2:-2]); r.bold = True
        elif part.startswith('`') and part.endswith('`'):
            r = par.add_run(part[1:-1]); r.font.name = 'Consolas'
            r._element.rPr.rFonts.set(qn('w:eastAsia'), 'Consolas')
            r.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
        else:
            r = par.add_run(part)
        if base_size:
            r.font.size = Pt(base_size)


def shade(cell, hex_fill):
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), hex_fill)
    tcPr.append(shd)


def add_table(doc, rows):
    cells = [[c.strip() for c in r.strip().strip('|').split('|')] for r in rows]
    cells = [r for r in cells if not all(re.fullmatch(r':?-{2,}:?', c or '---') for c in r)]
    if not cells:
        return
    ncol = max(len(r) for r in cells)
    t = doc.add_table(rows=len(cells), cols=ncol)
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    # ancho por columna proporcional al texto más largo (acotado), mínimo 1.4 cm
    lens = [max(min(len(r[j]) if j < len(r) else 0, 60) for r in cells) for j in range(ncol)]
    lens = [max(l, 6) for l in lens]
    total = 17.0
    widths = [max(1.4, total * l / sum(lens)) for l in lens]
    k = total / sum(widths); widths = [w * k for w in widths]
    size = 8.5 if ncol <= 8 else 7.5
    for i, row in enumerate(cells):
        for j in range(ncol):
            txt = row[j] if j < len(row) else ''
            cell = t.cell(i, j)
            cell.text = ''
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            add_runs(p, txt, base_size=size)
            cell.width = Cm(widths[j])
            if i == 0:
                for r in p.runs:
                    r.bold = True
                shade(cell, 'E8EEF4')
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def convert(src, dst):
    doc = Document()
    sec = doc.sections[0]
    sec.left_margin = sec.right_margin = Cm(2)
    sec.top_margin = sec.bottom_margin = Cm(2)
    st = doc.styles['Normal']
    st.font.name = 'Calibri'; st.font.size = Pt(10.5)
    st.element.rPr.rFonts.set(qn('w:eastAsia'), 'Calibri')
    for lvl, size in ((1, 18), (2, 14), (3, 12)):
        h = doc.styles[f'Heading {lvl}']
        h.font.name = 'Calibri'; h.font.size = Pt(size); h.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
        h.element.rPr.rFonts.set(qn('w:eastAsia'), 'Calibri')

    lines = open(src, encoding='utf-8').read().split('\n')
    i = 0
    first_h1 = True
    break_next = False
    while i < len(lines):
        ln = lines[i]
        if ln.startswith('|'):
            j = i
            while j < len(lines) and lines[j].startswith('|'):
                j += 1
            add_table(doc, lines[i:j]); i = j; continue
        if ln.strip() == '---':
            break_next = True; i += 1; continue
        if ln.startswith('```'):
            j = i + 1
            while j < len(lines) and not lines[j].startswith('```'):
                p = doc.add_paragraph(); r = p.add_run(lines[j]); r.font.name = 'Consolas'
                r._element.rPr.rFonts.set(qn('w:eastAsia'), 'Consolas'); r.font.size = Pt(9)
                r.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79); p.paragraph_format.space_after = Pt(0)
                j += 1
            doc.add_paragraph().paragraph_format.space_after = Pt(2)
            i = j + 1; continue
        m = re.match(r'^(#{1,3})\s+(.*)', ln)
        if m:
            lvl = len(m.group(1))
            if lvl == 1 and first_h1:
                p = doc.add_paragraph(); r = p.add_run(m.group(2)); r.bold = True; r.font.size = Pt(26)
                r.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79); first_h1 = False
            else:
                h = doc.add_heading(m.group(2), level=lvl)
                if break_next:
                    h.paragraph_format.page_break_before = True; break_next = False
            i += 1; continue
        m = re.match(r'^\s*[-*]\s+(.*)', ln)
        if m:
            p = doc.add_paragraph(style='List Bullet'); add_runs(p, m.group(1)); i += 1; continue
        m = re.match(r'^\s*(\d+)\.\s+(.*)', ln)
        if m:
            p = doc.add_paragraph(style='List Number'); add_runs(p, m.group(2)); i += 1; continue
        if ln.strip() == '':
            i += 1; continue
        # párrafo: juntar líneas consecutivas no vacías que no sean otra cosa
        buf = [ln]; j = i + 1
        while j < len(lines) and lines[j].strip() and not lines[j].startswith(('|', '#', '- ', '* ', '```')) and not re.match(r'^\s*\d+\.\s', lines[j]) and lines[j].strip() != '---':
            buf.append(lines[j]); j += 1
        p = doc.add_paragraph(); add_runs(p, ' '.join(s.strip() for s in buf))
        p.paragraph_format.space_after = Pt(6)
        i = j
    doc.save(dst)


if __name__ == '__main__':
    convert(sys.argv[1], sys.argv[2])
    print('ok', sys.argv[2])
