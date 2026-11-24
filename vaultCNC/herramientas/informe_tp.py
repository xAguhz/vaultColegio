#!/usr/bin/env python3
"""Genera el informe (.docx) de un TP de torno CNC, con la estructura del "TP ALFIL".

Uso:
  python3 informe_tp.py <pieza.json> <carpeta_winunisoft> <carpeta_plano> <salida.docx>
         [--alumno "Nombre Apellido"] [--curso "7°1 Electromecánica"] [--fecha dd/mm/aaaa]
         [--profesor "Apellido Nombre"]

Solo biblioteca estándar (OOXML a mano). Necesita pdftoppm para pasar el plano a PNG.
La operación se arma a partir del programa .nc: una operación por bloque de herramienta (T).
"""
import argparse, glob, json, os, re, struct, subprocess, sys, tempfile, zipfile
from xml.sax.saxutils import escape

# ---------- datos del catálogo Kennametal Universal ----------
HERR = {  # T: (portaherramienta, pág, inserto, pág)
    'T0101': ('DCLN R/L 2020K12KC04', 'A22', 'CNMG120408RP', 'A10'),
    'T0303': ('DVJN R/L 2020K16KC04', 'A27', 'VNMG160404FP', 'A14'),
    'T0505': ('A4SM R/L 2016K0317', 'A75', 'A4G0305M03U02GMP', 'A73'),
    'T0909': ('SVJB R/L 1212N11 (3)', 'A36', 'VBMT110304LF', 'A19'),
    'T1010': ('SVJB R/L 1212N11 (4)', 'A36', 'VBMT110304LF', 'A19'),
    'T1111': ('A4SM R/L 3225P0626', 'A75', 'A4G0605M06U08GMP', 'A73'),
}
# nombre de operación, nombre de la herramienta, velocidad, avance, prof. máx. de corte
INFO = {
    'T0101': ('DESBASTE EXTERIOR', 'DESBASTE', '180 m/min o 600 sfm (100 m/min - 250 m/min o 320 sfm - 800 sfm)', '0.3 (0.2 - 0.6)', '6.4 mm'),
    'T0303': ('TERMINACIÓN: DIAGONALES Y RADIOS BRUTOS', 'TERMINACIÓN', '180 m/min o 600 sfm (100 m/min - 250 m/min o 320 sfm - 800 sfm)', '0.2 (0.1 - 0.3)', '2.5 mm'),
    'T0505': ('RANURADO', 'RANURADO ∅3', '105 m/min (70 m/min - 150 m/min)', '0.1', '17 mm'),
    'T0909': ('RADIOS Y DIAGONALES LADO DERECHO', 'ACABADO ULTRAFINO', '180 m/min o 600 sfm (100 m/min - 250 m/min o 320 sfm - 800 sfm)', '0.2 (0.2 - 0.4)', '2.5 mm'),
    'T1010': ('RADIOS Y DIAGONALES LADO IZQUIERDO', 'ACABADO ULTRAFINO', '180 m/min o 600 sfm (100 m/min - 250 m/min o 320 sfm - 800 sfm)', '0.2 (0.2 - 0.4)', '2.5 mm'),
    'T1111': ('TRONZADO', 'RANURADO-TRONZADO ∅6', '105 m/min (70 m/min - 150 m/min)', '0.19', '26 mm'),
}
TITULOS = {'PEON': 'PEÓN'}
CICLOS = ['G90', 'G94', 'G01', 'G02', 'G03']

# ---------- XML ----------
NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
      'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
      'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"')
W_TEXTO = 9026  # A4 con márgenes de 2,54 cm


def run(t, font='Calibri', sz=22, b=False, i=False, color='000000'):
    rp = (f'<w:rFonts w:ascii="{font}" w:hAnsi="{font}" w:cs="{font}" w:eastAsia="{font}"/>'
          + ('<w:b/><w:bCs/>' if b else '') + ('<w:i/><w:iCs/>' if i else '')
          + f'<w:color w:val="{color}"/><w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>')
    return f'<w:r><w:rPr>{rp}</w:rPr><w:t xml:space="preserve">{escape(t)}</w:t></w:r>'


def brk():
    return '<w:r><w:br/></w:r>'


def para(runs, jc='left', after=0, line=240, keep=False, pb=False):
    pp = (('<w:pageBreakBefore/>' if pb else '') + ('<w:keepNext/>' if keep else '')
          + f'<w:spacing w:before="0" w:after="{after}" w:line="{line}" w:lineRule="auto"/><w:jc w:val="{jc}"/>')
    return f'<w:p><w:pPr>{pp}</w:pPr>{"".join(runs)}</w:p>'


def borders():
    return ''.join(f'<w:{s} w:val="single" w:sz="4" w:space="0" w:color="000000"/>' for s in ('top', 'left', 'bottom', 'right'))


def cell(content, w, valign='center', span=1):
    sp = f'<w:gridSpan w:val="{span}"/>' if span > 1 else ''
    return (f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/>{sp}<w:tcBorders>{borders()}</w:tcBorders>'
            f'<w:tcMar><w:left w:w="108" w:type="dxa"/><w:right w:w="108" w:type="dxa"/></w:tcMar>'
            f'<w:vAlign w:val="{valign}"/></w:tcPr>{content or para([])}</w:tc>')


def row(cells, h=569, split=False):
    return (f'<w:tr><w:trPr>{"" if split else "<w:cantSplit/>"}<w:trHeight w:val="{h}" w:hRule="atLeast"/></w:trPr>'
            f'{"".join(cells)}</w:tr>')


def table(rows, widths):
    grid = ''.join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    return (f'<w:tbl><w:tblPr><w:tblW w:w="{sum(widths)}" w:type="dxa"/><w:jc w:val="center"/>'
            f'<w:tblLayout w:type="fixed"/></w:tblPr><w:tblGrid>{grid}</w:tblGrid>{"".join(rows)}</w:tbl>')


def txt(t, **k):
    return para([run(t, **k)], jc=k.pop('jc', 'center') if False else 'center')


def tc(t, w, sz=22, b=False, jc='center', valign='center'):
    """celda con una o varias líneas (separadas por \\n)"""
    ps = ''.join(para([run(l, sz=sz, b=b)], jc=jc) for l in t.split('\n'))
    return cell(ps, w, valign)


def png_size(path):
    with open(path, 'rb') as f:
        h = f.read(24)
    return struct.unpack('>II', h[16:24])


class Imgs:
    def __init__(self):
        self.lista = []  # (rId, ruta)

    def inline(self, path, ancho_cm, alto_max_cm=None):
        w, h = png_size(path)
        cx = ancho_cm * 360000
        cy = cx * h / w
        if alto_max_cm and cy > alto_max_cm * 360000:
            cy = alto_max_cm * 360000
            cx = cy * w / h
        n = len(self.lista) + 1
        rid = f'rIdImg{n}'
        self.lista.append((rid, path))
        d = (f'<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{int(cx)}" cy="{int(cy)}"/>'
             f'<wp:docPr id="{n}" name="Imagen {n}"/><a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
             f'<pic:pic><pic:nvPicPr><pic:cNvPr id="{n}" name="img{n}.png"/><pic:cNvPicPr/></pic:nvPicPr>'
             f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
             f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{int(cx)}" cy="{int(cy)}"/></a:xfrm>'
             f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r>')
        return d


# ---------- análisis del programa .nc ----------
def parsear_nc(path):
    lineas = [l.strip() for l in open(path, encoding='utf-8', errors='replace').read().splitlines()]
    bloques, cur = [], None
    for l in lineas:
        m = re.match(r'^(T\d{4})\b', l)
        if m:
            cur = {'t': m.group(1), 'lineas': []}
            bloques.append(cur)
        if cur is not None and l and l != '%':
            cur['lineas'].append(l)
    for b in bloques:
        txt_ = ' '.join(b['lineas'])
        m = re.search(r'G96\s+S(\d+)', txt_)
        b['vc'] = int(m.group(1)) if m else None
        fs = []
        for f in re.findall(r'F(\.?\d*\.?\d+)', txt_):
            v = float(f if not f.startswith('.') else '0' + f)
            if v not in fs:
                fs.append(v)
        b['f'] = fs
        cod = set(re.findall(r'\bG0?(\d{1,2})\b', txt_))
        b['ciclos'] = [c for c in CICLOS if c[1:].lstrip('0') in {x.lstrip('0') for x in cod}]
        # zona de corte (movimientos que no son G00)
        modo, x, z, xs, zs = None, None, None, [], []
        for l in b['lineas']:
            g = re.search(r'\bG(\d+)', l)
            if g:
                modo = int(g.group(1))
            mx, mz = re.search(r'X(-?[\d.]+)', l), re.search(r'Z(-?[\d.]+)', l)
            if mx:
                x = float(mx.group(1))
            if mz:
                z = float(mz.group(1))
            if modo in (1, 2, 3, 90, 94) and (mx or mz):
                if x is not None:
                    xs.append(x)
                if z is not None:
                    zs.append(z)
        b['xs'], b['zs'] = xs, zs
    return [b for b in bloques if b['t'] in HERR]


def fmt(v):
    return ('%g' % v).replace('.', ',')


def forma_desde_prj(prj):
    """código de forma por herramienta (campo _CodForma de [TOOLS])"""
    res = {}
    if prj and os.path.exists(prj):
        for l in open(prj, encoding='utf-8', errors='replace'):
            m = re.match(r'Tool=T(\d+)\^.*?_CodForma=(\d+)', l)
            if m:
                res['T%02d%02d' % (int(m.group(1)), int(m.group(1)))] = int(m.group(2))
    return res


# ---------- armado del documento ----------
def construir(args):
    pieza = json.load(open(args.pieza, encoding='utf-8'))
    nombre = pieza['nombre'].upper()
    titulo = TITULOS.get(nombre, nombre)
    bruto = pieza['bruto']
    ncs = glob.glob(os.path.join(args.winunisoft, '*.nc'))
    if not ncs:
        sys.exit('No hay .nc en ' + args.winunisoft)
    nc = ncs[0]
    prj = nc[:-3] + '.prj'
    bloques = parsear_nc(nc)
    formas = forma_desde_prj(prj)
    prog = [l.strip() for l in open(nc, encoding='utf-8', errors='replace').read().splitlines() if l.strip()]
    tray = (glob.glob(os.path.join(args.winunisoft, '*trayectoria.png')) or [None])[0]
    tmp = tempfile.mkdtemp()
    pdfs = glob.glob(os.path.join(args.plano, '*.pdf'))
    plano = None
    if pdfs:
        base = os.path.join(tmp, 'plano')
        subprocess.run(['pdftoppm', '-r', '150', '-png', '-singlefile', pdfs[0], base], check=True)
        plano = base + '.png'
    im = Imgs()
    alumno = args.alumno.upper()
    cuerpo = []

    # 1. carátula
    cuerpo.append(para([run('TRABAJO PRÁCTICO:', 'Cambria', 100, b=True), brk(), run(titulo, 'Cambria', 100, b=True)], 'center', 80))
    cuerpo.append(para([], after=1800))
    def linea(et, val):
        return para([run(et + ' ', sz=40, b=True, i=True, color='262626'), run(val, sz=40, i=True, color='262626')], 'left', 200, 276)
    cuerpo.append(linea('TALLER:', 'DISEÑO Y PROCESAMIENTO MECÁNICO (CNC)'))
    if args.profesor:
        cuerpo.append(linea('PROFESOR:', args.profesor.upper()))
    if alumno:
        cuerpo.append(linea('ALUMNO:', alumno))
    if args.curso:
        cuerpo.append(linea('CURSO:', args.curso.upper()))
    cuerpo.append(linea('ESCUELA:', 'ESCUELA DE EDUCACIÓN SECUNDARIA TÉCNICA N°3 (EEST3)'))
    if args.fecha:
        cuerpo.append(linea('FECHA:', args.fecha))

    # 2. rótulo + 3. hoja de proceso
    wt = [W_TEXTO]
    cuerpo.append(para([], pb=True))
    cuerpo.append(table([
        row([tc('ESCUELA DE EDUCACION SECUNDARIA TECNICA N°3', W_TEXTO, sz=24)]),
        row([tc('DISEÑO Y PROCESAMIENTO MECANICO', W_TEXTO, sz=24)]),
        row([tc('MATERIAL ' + pieza['material'], W_TEXTO)]),
    ], wt))
    w4 = [1900, 2400, 2300, 2426]
    info = table([
        row([tc('ESTUDIANTE', w4[0]), tc(args.alumno, w4[1]), tc('REVISADO POR', w4[2]), tc('', w4[3])]),
        row([tc('TEMA', w4[0]), tc('TRABAJO PRACTICO: ' + nombre, w4[1]), tc('FECHA PRESENTACION', w4[2]), tc(args.fecha, w4[3])]),
    ], w4)
    cuerpo.append(info)
    filas = [row([tc('OPERACIÓN N°', w4[0], b=True), tc('PARAMETROS', w4[1], b=True),
                  tc('HERRAMIENTAS', w4[2], b=True), tc('ESQUEMA DE PROCESO', w4[3], b=True)], 400)]
    for n, b in enumerate(bloques, 1):
        t = b['t']
        hold, hp, ins, ip = HERR[t]
        op = INFO[t][0]
        par = f'VC: {b["vc"]} m/min\nAVANCE: ' + ' / '.join(fmt(v) for v in b['f']) + ' mm/vuelta\nCICLO: ' + '-'.join(b['ciclos'])
        her = f'{t}\nINSERTO: {ins} (pág. {ip})\nPORTAHERRAMIENTA: {hold} (pág. {hp})'
        if b['xs'] and b['zs']:
            m5 = lambda v: fmt(round(v * 2) / 2)  # a 0,5 mm
            esq = (f'Zona de corte:\nZ {m5(min(0.0, max(b["zs"])))} a {m5(min(b["zs"]))} mm\n'
                   f'Ø {m5(max(0.0, min(b["xs"])))} a {m5(max(b["xs"]))} mm')
        else:
            esq = ''
        filas.append(row([tc(f'{n}\n{op}', w4[0]), tc(par, w4[1]), tc(her, w4[2], sz=18), tc(esq, w4[3], sz=18)], 1500))
    cuerpo.append(para([], after=0))
    cuerpo.append(table(filas, w4))
    if tray:
        cuerpo.append(para([run('TRAYECTORIA DE LAS HERRAMIENTAS (WinUnisoft)', sz=22, b=True)], 'center', 60, keep=True))
        cuerpo.append(para([im.inline(tray, 15.5)], 'center'))

    # 4. plano
    cuerpo.append(para([run('PLANO', sz=48, b=True)], 'left', 120, pb=True, keep=True))
    if plano:
        cuerpo.append(para([im.inline(plano, 14.5, 22.0)], 'center'))

    # 5. programación CNC
    cuerpo.append(para([run('PROGRAMACIÓN CNC', sz=48, b=True)], 'left', 200, pb=True, keep=True))
    mitad = (len(prog) + 1) // 2
    def col(ls):
        return ''.join(para([run(l, 'Courier New', 18)]) for l in ls)
    cw = [W_TEXTO // 2, W_TEXTO - W_TEXTO // 2]
    cuerpo.append(table([row([cell(col(prog[:mitad]), cw[0], 'top'), cell(col(prog[mitad:]), cw[1], 'top')], 300, split=True)], cw))

    # 6. aclaraciones
    cuerpo.append(para([run('ACLARACIONES:', sz=48, b=True, color='ff0000')], 'left', 200, pb=True, keep=True))
    cuerpo.append(para([run('Cuando una herramienta esté señalizada con un número entre paréntesis al lado [(3) o (4)] se refiere a su '
                            'código de forma. Solo se emplea en las herramientas en las que este fue cambiado, de lo contrario, el '
                            'código de forma es 3 siempre.'), brk(), run('EJ: T0909 (3)')], 'left', 300))

    # 7. características de la pieza
    cuerpo.append(para([run('CARACTERÍSTICAS PIEZA:', sz=48, b=True)], 'left', 200, keep=True))
    carac = [('Nombre', nombre), ('Material', pieza['material']),
             ('Bruto', f'Ø = {bruto["d"]} mm, L = {bruto["l"]} mm'),
             ('Largo de la pieza', f'{pieza["largo"]} mm'),
             ('Punto cero', f'G54, Z = {fmt(bruto["l"] - 1)} mm'),
             ('Torno', 'Apolo, control Fanuc 16i-TA (simulador WinUnisoft)'),
             ('Catálogo de herramientas', 'Kennametal Universal'),
             ('Velocidad de torneado (pág. A5)', '180 m/min (100 m/min - 250 m/min)'),
             ('Velocidad de ranurado (pág. A71)', '105 m/min (70 m/min - 150 m/min)')]
    wc = [3400, W_TEXTO - 3400]
    cuerpo.append(table([row([tc(a, wc[0], b=True, jc='left'), tc(v, wc[1], jc='left')], 400) for a, v in carac], wc))

    # 8. una sección por herramienta
    for t in dict.fromkeys(b['t'] for b in bloques):
        hold, hp, ins, ip = HERR[t]
        op, nom, vel, av, prof = INFO[t]
        forma = formas.get(t, 4 if t in ('T1010',) else 3)
        bl = next(b for b in bloques if b['t'] == t)
        cuerpo.append(para([run(f'HERRAMIENTA {nom} ({t})', sz=28, b=True, color='ff0000')], 'left', 120, pb=True, keep=True))
        filas = [('Operación', op), ('Portaherramienta', f'{hold} (pág. {hp})'), ('Inserto', f'{ins} (pág. {ip})'),
                 ('Velocidad de corte', vel), ('Avance (mm/vuelta)', av),
                 ('Profundidad de corte máxima', prof), ('Código de forma', str(forma)),
                 ('Programa', f'G96 S{bl["vc"]}, F ' + ' / '.join(fmt(v) for v in bl['f']) + ', ciclos ' + '-'.join(bl['ciclos']))]
        cuerpo.append(table([row([tc(a, wc[0], b=True, jc='left'), tc(v, wc[1], jc='left')], 400) for a, v in filas], wc))
    cuerpo.append(para([], after=200))
    cuerpo.append(para([run('MANUAL USADO: “Kennametal Universal”', b=True)], 'left', 100, pb=False))
    if alumno:
        cuerpo.append(para([run('ALUMNO: ' + alumno, b=True)]))

    sect = ('<w:sectPr><w:headerReference w:type="default" r:id="rIdH1"/><w:headerReference w:type="first" r:id="rIdH2"/>'
            '<w:footerReference w:type="default" r:id="rIdF1"/><w:footerReference w:type="first" r:id="rIdF2"/>'
            '<w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1304" w:right="1440" w:bottom="1304" w:left="1440" w:header="567" w:footer="567" w:gutter="0"/>'
            '<w:titlePg/></w:sectPr>')
    doc = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {NS}><w:body>'
           + ''.join(cuerpo) + sect + '</w:body></w:document>')

    cab = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:hdr {NS}>'
           + para([run('TP: ' + nombre, sz=20, b=True)], 'right') + '</w:hdr>')
    cab0 = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:hdr {NS}>{para([])}</w:hdr>'
    campo = ('<w:r><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="20"/></w:rPr><w:fldChar w:fldCharType="begin"/></w:r>'
             '<w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
             '<w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:fldChar w:fldCharType="separate"/></w:r>'
             '<w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>1</w:t></w:r>'
             '<w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:fldChar w:fldCharType="end"/></w:r>')
    tab = '<w:r><w:tab/></w:r>'
    pie = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:ftr {NS}><w:p><w:pPr><w:tabs>'
           f'<w:tab w:val="center" w:pos="{W_TEXTO // 2}"/><w:tab w:val="right" w:pos="{W_TEXTO}"/></w:tabs></w:pPr>'
           + campo + tab + run(alumno, sz=20) + tab + run('EEST3', sz=20) + '</w:p></w:ftr>')
    pie0 = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:ftr {NS}>{para([])}</w:ftr>'

    styles = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles {NS}><w:docDefaults><w:rPrDefault><w:rPr>'
              '<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri" w:eastAsia="Calibri"/><w:sz w:val="22"/><w:lang w:val="es-AR"/>'
              '</w:rPr></w:rPrDefault></w:docDefaults><w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style></w:styles>')
    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/>'
          '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
          '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
          + ''.join(f'<Override PartName="/word/header{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>'
                    f'<Override PartName="/word/footer{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>' for i in (1, 2))
          + '</Types>')
    R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            f'<Relationship Id="rId1" Type="{R}/officeDocument" Target="word/document.xml"/></Relationships>')
    drels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
             f'<Relationship Id="rIdS" Type="{R}/styles" Target="styles.xml"/>'
             f'<Relationship Id="rIdH1" Type="{R}/header" Target="header1.xml"/><Relationship Id="rIdH2" Type="{R}/header" Target="header2.xml"/>'
             f'<Relationship Id="rIdF1" Type="{R}/footer" Target="footer1.xml"/><Relationship Id="rIdF2" Type="{R}/footer" Target="footer2.xml"/>'
             + ''.join(f'<Relationship Id="{rid}" Type="{R}/image" Target="media/img{k}.png"/>' for k, (rid, _) in enumerate(im.lista, 1))
             + '</Relationships>')

    os.makedirs(os.path.dirname(os.path.abspath(args.salida)), exist_ok=True)
    with zipfile.ZipFile(args.salida, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', ct)
        z.writestr('_rels/.rels', rels)
        z.writestr('word/document.xml', doc)
        z.writestr('word/styles.xml', styles)
        z.writestr('word/header1.xml', cab)
        z.writestr('word/header2.xml', cab0)
        z.writestr('word/footer1.xml', pie)
        z.writestr('word/footer2.xml', pie0)
        z.writestr('word/_rels/document.xml.rels', drels)
        for k, (rid, p) in enumerate(im.lista, 1):
            z.write(p, f'word/media/img{k}.png')
    print('Informe generado:', args.salida, f'({len(bloques)} operaciones)')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('pieza')
    ap.add_argument('winunisoft')
    ap.add_argument('plano')
    ap.add_argument('salida')
    ap.add_argument('--alumno', default='')
    ap.add_argument('--curso', default='')
    ap.add_argument('--fecha', default='')
    ap.add_argument('--profesor', default='')
    construir(ap.parse_args())


if __name__ == '__main__':
    main()
