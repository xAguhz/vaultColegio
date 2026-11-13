"""Convierte el HTML del TP8 (subconjunto simple) en un .docx con OOXML a mano. Uso: python3 html2docx.py in.html out.docx"""
import re, sys, zipfile
from html.parser import HTMLParser
from xml.sax.saxutils import escape

FONT = 'Arial'
ACCENT = '1F3B57'
ACCENT2 = '2E5C82'
TEXT_W = 9638  # 17 cm en twips (A4 con márgenes de 2 cm)
PT = 20  # twips por punto


class Node:
    def __init__(self, tag, attrs=None, parent=None):
        self.tag, self.attrs, self.parent, self.children = tag, dict(attrs or {}), parent, []


class P(HTMLParser):
    VOID = {'br', 'hr', 'meta', 'img'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node('root')
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.cur)
        self.cur.children.append(n)
        if tag not in self.VOID:
            self.cur = n

    def handle_endtag(self, tag):
        c = self.cur
        while c is not self.root and c.tag != tag:
            c = c.parent
        if c is not self.root:
            self.cur = c.parent

    def handle_data(self, data):
        self.cur.children.append(data)


def style_of(n):
    d = {}
    for part in n.attrs.get('style', '').split(';'):
        if ':' in part:
            k, v = part.split(':', 1)
            d[k.strip()] = v.strip()
    return d


rels = []


def add_link(url):
    rid = f'rId{len(rels) + 10}'
    rels.append((rid, url))
    return rid


def run(text, b=False, i=False, color=None, size=None, link=None):
    if not text:
        return ''
    rpr = ('<w:b/>' if b else '') + ('<w:i/>' if i else '')
    if link:
        rpr += '<w:color w:val="0563C1"/><w:u w:val="single"/>'
    elif color:
        rpr += f'<w:color w:val="{color}"/>'
    if size:
        rpr += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
    r = f'<w:r>{"<w:rPr>" + rpr + "</w:rPr>" if rpr else ""}<w:t xml:space="preserve">{escape(text)}</w:t></w:r>'
    if link:
        r = f'<w:hyperlink r:id="{add_link(link)}" w:history="1">{r}</w:hyperlink>'
    return r


def inlines(n, b=False, i=False, color=None, size=None, link=None):
    out = []
    for c in n.children:
        if isinstance(c, str):
            t = re.sub(r'\s+', ' ', c)
            out.append(run(t, b, i, color, size, link))
            continue
        st = style_of(c)
        cb, ci, cc, cs, cl = b, i, color, size, link
        if c.tag in ('b', 'strong', 'th'):
            cb = True
        if c.tag in ('i', 'em'):
            ci = True
        if c.tag == 'a':
            cl = c.attrs.get('href')
        if 'color' in st:
            cc = st['color'].lstrip('#').upper()
        if 'font-size' in st:
            cs = int(float(st['font-size'].replace('pt', '')) * 2)
        if c.tag == 'br':
            out.append('<w:r><w:br/></w:r>')
        else:
            out.append(inlines(c, cb, ci, cc, cs, cl))
    s = ''.join(out)
    return s


def strip_edges(xml):
    # quita espacios sobrantes al principio y al final de un párrafo
    xml = re.sub(r'^(<w:r>(?:<w:rPr>.*?</w:rPr>)?<w:t xml:space="preserve">)\s+', r'\1', xml)
    xml = re.sub(r'\s+(</w:t></w:r>)$', r'\1', xml)
    xml = re.sub(r'<w:r>(<w:rPr>[^<]*(?:<[^/][^>]*/>)*</w:rPr>)?<w:t xml:space="preserve"></w:t></w:r>', '', xml)
    return xml


def para(content, style=None, align=None, spacing=None, numbering=None, pagebreak=False, keep_next=False):
    ppr = ''
    if style:
        ppr += f'<w:pStyle w:val="{style}"/>'
    if keep_next:
        ppr += '<w:keepNext/>'
    if pagebreak:
        ppr += '<w:pageBreakBefore/>'
    if numbering:
        ppr += f'<w:numPr><w:ilvl w:val="0"/><w:numId w:val="{numbering}"/></w:numPr>'
    if spacing:
        ppr += f'<w:spacing w:before="{spacing[0]}" w:after="{spacing[1]}"/>'
    if align:
        ppr += f'<w:jc w:val="{align}"/>'
    return f'<w:p>{"<w:pPr>" + ppr + "</w:pPr>" if ppr else ""}{strip_edges(content)}</w:p>'


num_ids = [2]  # 1 = viñetas; desde 2, listas numeradas (cada una reinicia)
numbered = []


def table(n):
    rows = [r for r in iter_tags(n, 'tr')]
    first = [c for c in rows[0].children if not isinstance(c, str) and c.tag in ('td', 'th')]
    pts = []
    for c in first:
        m = re.search(r'width:(\d+)pt', c.attrs.get('style', ''))
        pts.append(int(m.group(1)) if m else 100)
    tw = int(re.search(r'width:(\d+)pt', n.attrs.get('style', 'width:468pt')).group(1))
    total_tw = min(TEXT_W, int(tw / 468 * TEXT_W))
    widths = [int(total_tw * p / sum(pts)) for p in pts]
    widths[-1] += total_tw - sum(widths)
    centered = n.attrs.get('align') == 'center'
    grid = ''.join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    x = [f'<w:tbl><w:tblPr><w:tblW w:w="{total_tw}" w:type="dxa"/>' + ('<w:jc w:val="center"/>' if centered else '')
         + '<w:tblBorders>' + ''.join(f'<w:{s} w:val="single" w:sz="4" w:space="0" w:color="BFC7D1"/>' for s in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'))
         + '</w:tblBorders><w:tblLayout w:type="fixed"/><w:tblCellMar><w:top w:w="60" w:type="dxa"/><w:left w:w="100" w:type="dxa"/><w:bottom w:w="60" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tblCellMar></w:tblPr>'
         + f'<w:tblGrid>{grid}</w:tblGrid>']
    for ri, r in enumerate(rows):
        cells = [c for c in r.children if not isinstance(c, str) and c.tag in ('td', 'th')]
        hdr = all(c.tag == 'th' for c in cells)
        x.append('<w:tr><w:trPr>' + ('<w:tblHeader/>' if hdr else '') + '<w:cantSplit/></w:trPr>')
        for ci, c in enumerate(cells):
            shd = '<w:shd w:val="clear" w:color="auto" w:fill="E8EEF4"/>' if c.tag == 'th' else ''
            x.append(f'<w:tc><w:tcPr><w:tcW w:w="{widths[ci]}" w:type="dxa"/>{shd}</w:tcPr>'
                     + para(inlines(c, b=c.tag == 'th', size=19), spacing=(0, 0)) + '</w:tc>')
        x.append('</w:tr>')
    x.append('</w:tbl>')
    return ''.join(x)


def iter_tags(n, tag):
    for c in n.children:
        if isinstance(c, str):
            continue
        if c.tag == tag:
            yield c
        else:
            yield from iter_tags(c, tag)


def block(n, out):
    for c in n.children:
        if isinstance(c, str):
            continue
        st = style_of(c)
        align = 'center' if st.get('text-align') == 'center' else None
        if c.tag in ('h1', 'h2', 'h3'):
            lvl = int(c.tag[1])
            out.append(para(inlines(c), style=f'Heading{lvl}', pagebreak='page-break-before' in c.attrs.get('style', '')))
        elif c.tag == 'p':
            size = 18 if 'chico' in c.attrs.get('class', '') else None
            color = '555555' if size else None
            out.append(para(inlines(c, color=color, size=size), align=align))
        elif c.tag in ('ul', 'ol'):
            if c.tag == 'ol':
                nid = num_ids[0]
                num_ids[0] += 1
                numbered.append(nid)
            else:
                nid = 1
            items = list(iter_tags(c, 'li'))
            for k, li in enumerate(items):
                out.append(para(inlines(li), numbering=nid, spacing=(0, 120 if k == len(items) - 1 else 40)))
        elif c.tag == 'table':
            out.append(table(c))
            out.append(para('', spacing=(0, 80)))
        elif c.tag == 'hr':
            continue
        else:
            block(c, out)


src, dst = sys.argv[1], sys.argv[2]
p = P()
p.feed(open(src, encoding='utf-8').read())
body_node = next(iter_tags(p.root, 'body'))
out = []
block(body_node, out)

sect = (f'<w:sectPr><w:footerReference w:type="default" r:id="rId4"/><w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" w:header="567" w:footer="567" w:gutter="0"/><w:titlePg/></w:sectPr>')
document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><w:body>' + ''.join(out) + sect + '</w:body></w:document>')
footer = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
          'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
          + para('<w:r><w:rPr><w:color w:val="7F7F7F"/><w:sz w:val="16"/></w:rPr><w:t xml:space="preserve">Sistemas Mecánicos · TP N° 8 · 7° 1° · Página </w:t></w:r>'
                 '<w:r><w:rPr><w:color w:val="7F7F7F"/><w:sz w:val="16"/></w:rPr><w:fldChar w:fldCharType="begin"/></w:r>'
                 '<w:r><w:rPr><w:color w:val="7F7F7F"/><w:sz w:val="16"/></w:rPr><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
                 '<w:r><w:rPr><w:color w:val="7F7F7F"/><w:sz w:val="16"/></w:rPr><w:fldChar w:fldCharType="separate"/></w:r>'
                 '<w:r><w:rPr><w:color w:val="7F7F7F"/><w:sz w:val="16"/></w:rPr><w:t>2</w:t></w:r>'
                 '<w:r><w:rPr><w:color w:val="7F7F7F"/><w:sz w:val="16"/></w:rPr><w:fldChar w:fldCharType="end"/></w:r>', align='right')
          + '</w:ftr>')


def hstyle(i, size, color, before, after):
    return (f'<w:style w:type="paragraph" w:styleId="Heading{i}"><w:name w:val="heading {i}"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="9"/><w:qFormat/>'
            f'<w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="{before}" w:after="{after}"/><w:outlineLvl w:val="{i - 1}"/></w:pPr>'
            f'<w:rPr><w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}"/><w:b/><w:color w:val="{color}"/><w:sz w:val="{size}"/><w:szCs w:val="{size}"/></w:rPr></w:style>')


styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
          f'<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}" w:eastAsia="{FONT}" w:cs="{FONT}"/><w:color w:val="222222"/><w:sz w:val="22"/><w:szCs w:val="22"/><w:lang w:val="es-AR"/></w:rPr></w:rPrDefault>'
          '<w:pPrDefault><w:pPr><w:spacing w:after="140" w:line="276" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>'
          '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>'
          + hstyle(1, 34, ACCENT, 360, 160) + hstyle(2, 28, ACCENT, 280, 120) + hstyle(3, 24, ACCENT2, 220, 80)
          + '<w:style w:type="table" w:default="1" w:styleId="TableNormal"><w:name w:val="Normal Table"/><w:tblPr><w:tblInd w:w="0" w:type="dxa"/><w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:left w:w="108" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/><w:right w:w="108" w:type="dxa"/></w:tblCellMar></w:tblPr></w:style>'
          '</w:styles>')
lvl_bullet = '<w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="•"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="426" w:hanging="284"/></w:pPr></w:lvl>'
lvl_dec = '<w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%1."/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="426" w:hanging="284"/></w:pPr></w:lvl>'
numbering = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
             f'<w:abstractNum w:abstractNumId="0"><w:multiLevelType w:val="hybridMultilevel"/>{lvl_bullet}</w:abstractNum>'
             f'<w:abstractNum w:abstractNumId="1"><w:multiLevelType w:val="hybridMultilevel"/>{lvl_dec}</w:abstractNum>'
             '<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>'
             + ''.join(f'<w:num w:numId="{n}"><w:abstractNumId w:val="1"/><w:lvlOverride w:ilvl="0"><w:startOverride w:val="1"/></w:lvlOverride></w:num>' for n in numbered)
             + '</w:numbering>')
ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
      '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
      '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
      '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
      '<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>'
      '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/></Types>')
root_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
             '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>')
doc_rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>',
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>',
            '<Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>']
for rid, url in rels:
    doc_rels.append(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" Target="{escape(url, {chr(34): "&quot;"})}" TargetMode="External"/>')
doc_rels.append('</Relationships>')
with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', ct)
    z.writestr('_rels/.rels', root_rels)
    z.writestr('word/document.xml', document)
    z.writestr('word/styles.xml', styles)
    z.writestr('word/numbering.xml', numbering)
    z.writestr('word/footer1.xml', footer)
    z.writestr('word/_rels/document.xml.rels', ''.join(doc_rels))
print('OK', dst, len(out), 'bloques', len(rels), 'links')
