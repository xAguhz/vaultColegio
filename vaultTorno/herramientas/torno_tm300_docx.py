"""Regenera el Word del TP del torno a partir de las notas de "Torno TM300" (solo stdlib + PIL). Uso: python3 herramientas/torno_tm300_docx.py"""
import re, os, zipfile, sys
from xml.sax.saxutils import escape
from PIL import Image

VAULT = '/home/chagus/Colegio/vaultColegio/vaultTorno'
TDIR = VAULT + '/Torno TM300'
IMGDIR = VAULT + '/Adjuntos/Torno TM300'
OUT = TDIR + '/TP Torno TM300 - Manual de mantenimiento y repuestos.docx'

CHAPTERS = ['01 Identificación y equivalencias', '02 Historia', '03 Partes y movimientos', '04 Normas de seguridad',
            '05 Instalación y puesta en marcha', '06 Lubricación', '07 Avances y roscado', '08 Circuito eléctrico',
            '09 Ajustes y puesta a punto', '10 Cambio de partes', '11 Diagnóstico de fallas', '12 Plan de mantenimiento',
            '13 Repuestos y compras', '14 Conclusiones']
DESP = ['Bancada y transmisión', 'Cabezal', 'Caja Norton y lira', 'Delantal', 'Carros', 'Contrapunto', 'Lunetas', 'Refrigeración']
DESP_LETTER = {n: f'A.{i+1}' for i, n in enumerate(DESP)}

FONT = 'Calibri'
ACCENT = '1F4E79'
CALLOUT = {'summary': ('Resumen', 'DEEBF7', '2E75B6'), 'warning': ('Atención', 'FFF2CC', 'BF8F00'), 'danger': ('Peligro', 'FBE4E4', 'C00000'),
           'tip': ('Consejo', 'E2EFDA', '548235'), 'note': ('Nota', 'EDEDED', '7F7F7F'), 'info': ('Info', 'DEEBF7', '2E75B6'),
           'important': ('Importante', 'FCE4D6', 'C55A11'), 'caution': ('Precaución', 'FCE4D6', 'C55A11'), 'todo': ('Pendiente', 'E2EFDA', '548235')}

rels = []      # (rId, type, target, external)
media = []     # (name, path)
body = []
_id = [100]


def nid():
    _id[0] += 1
    return _id[0]


def add_rel(typ, target, external=False):
    rid = f'rId{len(rels) + 10}'
    rels.append((rid, typ, target, external))
    return rid


# ---------- inline ----------
def link_text(m):
    target, alias = m.group(1), m.group(2)
    if alias:
        return alias
    note, _, sec = target.partition('#')
    note = note.strip()
    if note.endswith('.excalidraw') or note.endswith('.canvas'):
        return 'diagrama del vault de Obsidian'
    mm = re.match(r'^(\d\d) ', note)
    if mm:
        s = f'cap. {int(mm.group(1))}'
    elif note in DESP:
        s = f'Anexo {DESP_LETTER[note]} ({note})'
    else:
        s = note
    if sec:
        s += f', «{sec}»'
    return s


def run(text, b=False, i=False, code=False, color=None, size=None, link_rid=None):
    if not text:
        return ''
    rpr = ''
    if code:
        rpr += '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>'
    if b:
        rpr += '<w:b/>'
    if i:
        rpr += '<w:i/>'
    if link_rid:
        rpr += '<w:color w:val="0563C1"/><w:u w:val="single"/>'
    elif color:
        rpr += f'<w:color w:val="{color}"/>'
    if size:
        rpr += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
    r = f'<w:r>{"<w:rPr>" + rpr + "</w:rPr>" if rpr else ""}<w:t xml:space="preserve">{escape(text)}</w:t></w:r>'
    if link_rid:
        r = f'<w:hyperlink r:id="{link_rid}" w:history="1">{r}</w:hyperlink>'
    return r


TOKEN = re.compile(r'(\*\*[^*]+\*\*|\*[^*\s][^*]*\*|`[^`]+`|\[[^\]]+\]\([^)]+\))')


def inline(text, b=False, i=False, color=None, size=None):
    text = re.sub(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]', link_text, text)
    out = []
    for part in TOKEN.split(text):
        if not part:
            continue
        if part.startswith('**') and part.endswith('**'):
            out.append(inline(part[2:-2], True, i, color, size))
        elif part.startswith('`') and part.endswith('`'):
            out.append(run(part[1:-1], b, i, True, color, size))
        elif part.startswith('[') and '](' in part:
            t, u = re.match(r'\[([^\]]+)\]\(([^)]+)\)', part).groups()
            rid = add_rel('http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink', u, True)
            tb = t.startswith('**') and t.endswith('**')
            out.append(run(t.strip('*'), b or tb, i, False, None, size, rid))
        elif part.startswith('*') and part.endswith('*') and len(part) > 2:
            out.append(inline(part[1:-1], b, True, color, size))
        else:
            out.append(run(part, b, i, False, color, size))
    return ''.join(out)


def para(content, style=None, align=None, ind=None, spacing=None, keep_next=False, numbering=None, shade=None, pagebreak_before=False):
    ppr = ''
    if style:
        ppr += f'<w:pStyle w:val="{style}"/>'
    if keep_next:
        ppr += '<w:keepNext/>'
    if pagebreak_before:
        ppr += '<w:pageBreakBefore/>'
    if numbering:
        ppr += f'<w:numPr><w:ilvl w:val="{numbering[1]}"/><w:numId w:val="{numbering[0]}"/></w:numPr>'
    if shade:
        ppr += f'<w:shd w:val="clear" w:color="auto" w:fill="{shade}"/>'
    if spacing:
        ppr += f'<w:spacing w:before="{spacing[0]}" w:after="{spacing[1]}"/>'
    if ind:
        ppr += f'<w:ind w:left="{ind[0]}" w:hanging="{ind[1]}"/>'
    if align:
        ppr += f'<w:jc w:val="{align}"/>'
    return f'<w:p>{"<w:pPr>" + ppr + "</w:pPr>" if ppr else ""}{content}</w:p>'


# ---------- images ----------
def image(name, width_cm=15.0, max_h_cm=21.0):
    path = os.path.join(IMGDIR, name)
    if not os.path.exists(path):
        print('FALTA imagen', name, file=sys.stderr)
        return ''
    w, h = Image.open(path).size
    wc = width_cm
    hc = wc * h / w
    if hc > max_h_cm:
        hc = max_h_cm
        wc = hc * w / h
    cx, cy = int(wc * 360000), int(hc * 360000)
    mname = f'image{len(media) + 1}.png'
    media.append((mname, path))
    rid = add_rel('http://schemas.openxmlformats.org/officeDocument/2006/relationships/image', f'media/{mname}')
    i = nid()
    drawing = (f'<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/>'
               f'<wp:docPr id="{i}" name="Imagen {i}"/><wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>'
               f'<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic>'
               f'<pic:nvPicPr><pic:cNvPr id="{i}" name="{escape(name)}"/><pic:cNvPicPr/></pic:nvPicPr>'
               f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
               f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
               f'</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r>')
    return para(drawing, align='center', spacing=(120, 40), keep_next=True)


# ---------- tables ----------
TABLE_W = 9638  # 17 cm in twips


def table(rows, header=True, widths=None, font_size=18):
    ncol = max(len(r) for r in rows)
    rows = [r + [''] * (ncol - len(r)) for r in rows]
    if not widths:
        lens = [max(4, min(40, max(len(re.sub(r'[*`\[\]]', '', r[c])) for r in rows))) for c in range(ncol)]
        tot = sum(lens)
        widths = [int(TABLE_W * l / tot) for l in lens]
        widths[-1] += TABLE_W - sum(widths)
    grid = ''.join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    x = [f'<w:tbl><w:tblPr><w:tblW w:w="{TABLE_W}" w:type="dxa"/><w:tblBorders>'
         + ''.join(f'<w:{s} w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>' for s in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'))
         + '</w:tblBorders><w:tblLayout w:type="fixed"/><w:tblCellMar><w:left w:w="70" w:type="dxa"/><w:right w:w="70" w:type="dxa"/></w:tblCellMar></w:tblPr>'
         + f'<w:tblGrid>{grid}</w:tblGrid>']
    for ri, r in enumerate(rows):
        hdr = header and ri == 0
        trpr = '<w:trPr><w:tblHeader/><w:cantSplit/></w:trPr>' if hdr else '<w:trPr><w:cantSplit/></w:trPr>'
        x.append(f'<w:tr>{trpr}')
        for ci, cell in enumerate(r):
            shd = f'<w:shd w:val="clear" w:color="auto" w:fill="{ACCENT}"/>' if hdr else ('<w:shd w:val="clear" w:color="auto" w:fill="F2F2F2"/>' if ri % 2 == 0 else '')
            content = inline(cell.strip(), b=hdr, color='FFFFFF' if hdr else None, size=font_size)
            x.append(f'<w:tc><w:tcPr><w:tcW w:w="{widths[ci]}" w:type="dxa"/>{shd}</w:tcPr>'
                     + para(content, spacing=(20, 20)) + '</w:tc>')
        x.append('</w:tr>')
    x.append('</w:tbl>')
    return ''.join(x) + para('', spacing=(0, 60))


def callout(kind, title, lines):
    label, fill, border = CALLOUT.get(kind.lower(), ('Nota', 'EDEDED', '7F7F7F'))
    paras = [para(inline(title or label, b=True, color=border), spacing=(40, 40))]
    for ln in lines:
        m = re.match(r'^(\d+)\.\s+(.*)', ln)
        if ln.startswith('- '):
            paras.append(para(run('• ') + inline(ln[2:]), ind=(360, 240), spacing=(0, 30)))
        elif m:
            paras.append(para(run(m.group(1) + '. ') + inline(m.group(2)), ind=(360, 280), spacing=(0, 30)))
        elif ln.strip():
            paras.append(para(inline(ln), spacing=(0, 40)))
    return (f'<w:tbl><w:tblPr><w:tblW w:w="{TABLE_W}" w:type="dxa"/><w:tblBorders>'
            f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{border}"/></w:tblBorders>'
            f'<w:tblCellMar><w:left w:w="160" w:type="dxa"/><w:right w:w="120" w:type="dxa"/></w:tblCellMar></w:tblPr>'
            f'<w:tblGrid><w:gridCol w:w="{TABLE_W}"/></w:tblGrid><w:tr><w:trPr><w:cantSplit/></w:trPr><w:tc><w:tcPr><w:tcW w:w="{TABLE_W}" w:type="dxa"/>'
            f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/></w:tcPr>{"".join(paras)}</w:tc></w:tr></w:tbl>') + para('', spacing=(0, 80))


# ---------- markdown note -> body ----------
def convert(md, chapter_title, level_shift=0, first_pagebreak=True):
    md = re.sub(r'^---\n.*?\n---\n', '', md, flags=re.S)
    lines = md.split('\n')
    out = []
    i = 0
    first_h1 = True
    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if not s or s == '---' or s.startswith('Volver a ') or s.startswith('Ver también:') or 'TP Torno TM300 - Manual' in s:
            i += 1
            continue
        if s.startswith('# '):
            if first_h1:
                out.append(para(inline(chapter_title), style='Heading1', pagebreak_before=first_pagebreak, keep_next=True))
                first_h1 = False
            i += 1
            continue
        m = re.match(r'^(#{2,4}) (.*)', s)
        if m:
            lvl = len(m.group(1)) + level_shift
            out.append(para(inline(m.group(2)), style=f'Heading{min(lvl, 4)}', keep_next=True))
            i += 1
            continue
        m = re.match(r'^!\[\[([^\]|]+)(?:\|(\d+))?\]\]', s)
        if m:
            w = min(15.5, int(m.group(2)) * 0.03) if m.group(2) else 15.5
            out.append(image(m.group(1), w))
            if i + 1 < len(lines) and re.match(r'^\*[^*].*\*$', lines[i + 1].strip()):
                out.append(para(inline(lines[i + 1].strip()[1:-1], i=True, color='595959', size=18), align='center', spacing=(0, 160)))
                i += 1
            i += 1
            continue
        if s.startswith('>'):
            block = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                block.append(re.sub(r'^\s*>\s?', '', lines[i]))
                i += 1
            m = re.match(r'^\[!(\w+)\]\s*(.*)', block[0])
            if m:
                out.append(callout(m.group(1), m.group(2).strip(), block[1:]))
            else:
                out.append(callout('note', '', block))
            continue
        if s.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                cells = [c for c in lines[i].strip().strip('|').split('|')]
                if not all(re.match(r'^\s*:?-{3,}:?\s*$', c) for c in cells):
                    rows.append(cells)
                i += 1
            empty_header = all(not c.strip() for c in rows[0])
            if empty_header:
                rows = rows[1:]
            fs = 16 if len(rows[0]) >= 6 else 18
            out.append(table(rows, header=not empty_header, font_size=fs))
            continue
        if s.startswith('- '):
            while i < len(lines) and lines[i].strip().startswith('- '):
                out.append(para(inline(lines[i].strip()[2:]), numbering=(1, 0), spacing=(0, 60)))
                i += 1
            continue
        m = re.match(r'^(\d+)\.\s+(.*)', s)
        if m:
            out.append(para(run(m.group(1) + '.  ', b=True) + inline(m.group(2)), ind=(426, 426), spacing=(0, 60)))
            i += 1
            continue
        if re.match(r'^\*[^*].*\*$', s):
            out.append(para(inline(s[1:-1], i=True, color='595959', size=18), align='center', spacing=(0, 160)))
            i += 1
            continue
        out.append(para(inline(s), spacing=(0, 120)))
        i += 1
    return out


def read(name):
    return open(os.path.join(TDIR, name + '.md'), encoding='utf-8').read()


# ---------- cover ----------
def cover():
    c = []
    c.append(para(run('TRABAJO PRÁCTICO', b=True, color='7F7F7F', size=24), align='center', spacing=(600, 120)))
    c.append(para(run('Torno paralelo Femar Turn Master TM300', b=True, color=ACCENT, size=48), align='center', spacing=(0, 80)))
    c.append(para(run('Manual de mantenimiento, cambio de partes y repuestos', color='404040', size=32), align='center', spacing=(0, 300)))
    c.append(image('tm300_portada.png', 13, 10))
    rows = [['Dato', 'Detalle'],
            ['Unidad del taller', 'Femar Turn Master TM300 · S/N 831930 · fabricación 08/2008'],
            ['Plataforma de fábrica', 'C0632A / CQ6230A — clones: Hafco AL-340, Grizzly G4003, Axminster CQ6230A-2, Lüsqtoff TBL-330'],
            ['Máquina de referencia histórica', 'PBR TM300 (Ø610 × 4000 mm, Italia)'],
            ['Fuentes', 'Manual de fábrica AL340 / C0632A (inglés, traducido) · Manual de repuestos Femar · TP original'],
            ['Relevamiento de precios', 'Mercado Libre Argentina, tiendas y distribuidores · 12/11/2026'],
            ['Área', 'Electromecánica: Máquinas Herramienta · Mantenimiento Industrial · Instalaciones Eléctricas'],
            ['Alumno/a · Curso', ' ']]
    c.append(table(rows, widths=[3000, TABLE_W - 3000]))
    return c


def contents():
    c = [para(inline('Contenido'), style='Heading1', pagebreak_before=True)]
    for n in CHAPTERS:
        num, name = n.split(' ', 1)
        c.append(para(run(f'{int(num)}. ', b=True) + run(name), spacing=(0, 60)))
    c.append(para(run('Anexo A. ', b=True) + run('Despiece traducido: ' + ', '.join(f'{DESP_LETTER[d]} {d}' for d in DESP)), spacing=(60, 60)))
    c.append(para(run('Anexo B. ', b=True) + run('Fuentes'), spacing=(0, 200)))
    c.append(callout('info', 'Cómo usar este manual', [
        '- Para **mantenimiento de rutina**: cap. 6 (lubricación) y cap. 12 (planilla).',
        '- Si **algo falla**: cap. 11 (diagnóstico) → cap. 4 (seguridad y LOTO) → cap. 10 (cambio de partes) → cap. 9 (ajustes).',
        '- Para **comprar un repuesto**: buscar el ítem en el Anexo A, tomar el código o la medida comercial y seguir el cap. 13.',
        'Las notas equivalentes, con mapas y dibujos editables, están en el vault de Obsidian (carpeta "Torno TM300").']))
    return c


# ---------- assemble ----------
body += cover()
body += contents()
for n in CHAPTERS:
    num, name = n.split(' ', 1)
    title = f'{int(num)}. ' + re.sub(r'^#\s*', '', [l for l in read(n).split('\n') if l.startswith('# ')][0])
    body += convert(read(n), title)
body.append(para(inline('Anexo A. Despiece traducido'), style='Heading1', pagebreak_before=True))
body.append(para(inline('Listas de piezas del manual de fábrica (capítulos 11 a 18) traducidas, con las láminas originales y el equivalente comercial de rodamientos, retenes y correas. Los números de ítem son los de cada lámina y se usan en el cap. 10.'), spacing=(0, 120)))
body.append(callout('note', 'Cómo leer los códigos', [
    '- `GB…`, `JB…`, `HG…`: piezas normalizadas chinas (tornillos, chavetas, rodamientos, retenes). Se compran por medida.',
    '- `32…`, `33…`, `6220…`, `CL6132…`: piezas propias de la plataforma C0632A / AL-340. Se piden por código o se fabrican copiando la original.',
    '- Variantes: (C0632A) volteo 330 mm / (C0636A) volteo 358 mm; (bancada 750/1000 mm) según el largo entre puntas.']))
for d in DESP:
    md = read('Despiece/' + d)
    md = re.sub(r'\n> \[!note\] Cómo leer los códigos\n(?:>.*\n?)*', '\n', md)
    title = f'{DESP_LETTER[d]} ' + [l for l in md.split('\n') if l.startswith('# ')][0][2:].replace('Despiece: ', '')
    conv = convert(md, title, level_shift=1)
    conv[0] = conv[0].replace('<w:pStyle w:val="Heading1"/>', '<w:pStyle w:val="Heading2"/>')
    body += conv
body.append(para(inline('Anexo B. Fuentes'), style='Heading1', pagebreak_before=True))
for f in ['Manual de fábrica: *AL340 series lathe after 12-2011 (with new type 4 knob feed box) — Operation Manual & Parts List*, modelos C0632A, C0636A, C0636C (56 págs., inglés). Traducido completo en este trabajo.',
          'Manual de Repuestos, Equivalencias y Mantenimiento — Torno Femar Turn Master TM300 (S/N 831930), 7 págs.',
          'Trabajo Práctico: Torno Paralelo PBR TM300 / Femar Turn Master TM300 (documento original del curso).',
          'Relevamiento de repuestos y precios (12/11/2026): Mercado Libre Argentina, PPi Máquinas, J. C. Narcisi, Alfa Rodamientos, CP Goma, La Ferre Store, Distribuidora Uriburu, Distribuidora MEI, Performance Lube, Machineseeker Argentina, Hare & Forbes Machineryhouse.',
          'Los procedimientos de desarme del cap. 10 se elaboraron a partir de las láminas de despiece y de práctica general de taller: no figuran en el manual original.']:
    body.append(para(inline(f), numbering=(1, 0), spacing=(0, 80)))

# ---------- package ----------
NS = ('xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
      'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
      'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
      'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"')
hdr_rid = add_rel('http://schemas.openxmlformats.org/officeDocument/2006/relationships/header', 'header1.xml')
ftr_rid = add_rel('http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer', 'footer1.xml')
sect = (f'<w:sectPr><w:headerReference w:type="default" r:id="{hdr_rid}"/><w:footerReference w:type="default" r:id="{ftr_rid}"/>'
        '<w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" w:header="567" w:footer="567" w:gutter="0"/>'
        '<w:titlePg/></w:sectPr>')
document = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {NS}><w:body>{"".join(body)}{sect}</w:body></w:document>'

header = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:hdr {NS}>'
          + para(run('TP · Torno Femar Turn Master TM300 — Manual de mantenimiento y repuestos', color='7F7F7F', size=16), align='right')
          + '</w:hdr>')
footer = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:ftr {NS}>'
          + para(run('Página ', color='7F7F7F', size=16)
                 + '<w:r><w:rPr><w:color w:val="7F7F7F"/><w:sz w:val="16"/></w:rPr><w:fldChar w:fldCharType="begin"/></w:r>'
                 + '<w:r><w:rPr><w:color w:val="7F7F7F"/><w:sz w:val="16"/></w:rPr><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
                 + '<w:r><w:rPr><w:color w:val="7F7F7F"/><w:sz w:val="16"/></w:rPr><w:fldChar w:fldCharType="separate"/></w:r>'
                 + '<w:r><w:rPr><w:color w:val="7F7F7F"/><w:sz w:val="16"/></w:rPr><w:t>1</w:t></w:r>'
                 + '<w:r><w:rPr><w:color w:val="7F7F7F"/><w:sz w:val="16"/></w:rPr><w:fldChar w:fldCharType="end"/></w:r>', align='center')
          + '</w:ftr>')


def hstyle(i, size, color, before, after):
    return (f'<w:style w:type="paragraph" w:styleId="Heading{i}"><w:name w:val="heading {i}"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="9"/><w:qFormat/>'
            f'<w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="{before}" w:after="{after}"/><w:outlineLvl w:val="{i - 1}"/></w:pPr>'
            f'<w:rPr><w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}"/><w:b/><w:color w:val="{color}"/><w:sz w:val="{size}"/><w:szCs w:val="{size}"/></w:rPr></w:style>')


styles = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
          f'<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}" w:eastAsia="{FONT}" w:cs="{FONT}"/><w:sz w:val="21"/><w:szCs w:val="21"/><w:lang w:val="es-AR"/></w:rPr></w:rPrDefault>'
          '<w:pPrDefault><w:pPr><w:spacing w:after="80" w:line="264" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>'
          '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>'
          + hstyle(1, 36, ACCENT, 240, 200) + hstyle(2, 28, '2E75B6', 300, 120) + hstyle(3, 24, '2E75B6', 220, 80) + hstyle(4, 22, '404040', 160, 60)
          + '<w:style w:type="table" w:default="1" w:styleId="TableNormal"><w:name w:val="Normal Table"/><w:tblPr><w:tblInd w:w="0" w:type="dxa"/><w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:left w:w="108" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/><w:right w:w="108" w:type="dxa"/></w:tblCellMar></w:tblPr></w:style>'
          '</w:styles>')
numbering = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
             '<w:abstractNum w:abstractNumId="0"><w:multiLevelType w:val="hybridMultilevel"/>'
             '<w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="•"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="426" w:hanging="284"/></w:pPr><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/></w:rPr></w:lvl>'
             '</w:abstractNum><w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num></w:numbering>')
settings = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            '<w:defaultTabStop w:val="709"/><w:characterSpacingControl w:val="doNotCompress"/><w:compat><w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/></w:compat></w:settings>')
core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        '<dc:title>Torno Femar Turn Master TM300 — Manual de mantenimiento, cambio de partes y repuestos</dc:title><dc:language>es-AR</dc:language>'
        '<dcterms:created xsi:type="dcterms:W3CDTF">2026-11-12T00:00:00Z</dcterms:created></cp:coreProperties>')

ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
      '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
      '<Default Extension="png" ContentType="image/png"/>'
      '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
      '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
      '<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>'
      '<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>'
      '<Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>'
      '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>'
      '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/></Types>')
root_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
             '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
             '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/></Relationships>')
doc_rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>',
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>',
            '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>']
for rid, typ, tgt, ext in rels:
    doc_rels.append(f'<Relationship Id="{rid}" Type="{typ}" Target="{escape(tgt, {chr(34): "&quot;"})}"{" TargetMode=" + chr(34) + "External" + chr(34) if ext else ""}/>')
doc_rels.append('</Relationships>')

if os.path.exists(OUT):
    os.remove(OUT)
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', ct)
    z.writestr('_rels/.rels', root_rels)
    z.writestr('docProps/core.xml', core)
    z.writestr('word/document.xml', document)
    z.writestr('word/styles.xml', styles)
    z.writestr('word/numbering.xml', numbering)
    z.writestr('word/settings.xml', settings)
    z.writestr('word/header1.xml', header)
    z.writestr('word/footer1.xml', footer)
    z.writestr('word/_rels/document.xml.rels', ''.join(doc_rels))
    for name, path in media:
        z.write(path, 'word/media/' + name)
print('OK', OUT, f'{os.path.getsize(OUT) / 1e6:.1f} MB', len(media), 'imágenes', len(rels), 'relaciones')
