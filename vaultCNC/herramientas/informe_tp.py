#!/usr/bin/env python3
"""Genera el informe (.docx) de un TP de torno CNC, con la estructura del "TP ALFIL".

Uso:
  python3 informe_tp.py <pieza.json> <carpeta_winunisoft> <carpeta_plano> <salida.docx>
         [--alumno "Nombre Apellido"] [--curso "7°1 Electromecánica"] [--fecha dd/mm/aaaa]
         [--profesor "Apellido Nombre"] [--capturas <carpeta con las imágenes del catálogo>]

Solo biblioteca estándar (OOXML a mano). Necesita pdftoppm para pasar el plano a PNG.
La operación se arma a partir del programa .nc: una operación por bloque de herramienta (T).
"""
import argparse, glob, json, os, re, struct, subprocess, sys, tempfile, zipfile
from xml.sax.saxutils import escape

# ---------- datos del catálogo Kennametal Universal ----------
HERR = {  # T: (portaherramienta, pág, inserto, pág)
    'T0101': ('DCLN R/L 2020K12KC04', 'A22', 'CNMG120408RP', 'A10'),
    'T0303': ('DVJN R/L 2020K16KC04', 'A27', 'VNMG160404FP', 'A14'),
    'T0505': ('A4SM R/L 2016K0317', 'A75', 'A4G0305M03U02GMN', 'A73'),
    'T0909': ('DVVNN 2020K16KC04 (8)', 'A28', 'VNMG160404FP', 'A14'),
    'T1010': ('SVJB R/L 1212N11 (4)', 'A36', 'VBMT110304LF', 'A19'),
    'T1111': ('A4SM R/L 3225P0626', 'A75', 'A4G0605M06U08GMP', 'A73'),
    'T0404': ('DVJN R/L 2020K16KC04 (4)', 'A27', 'VNMG160404FP', 'A14'),
}
# operación, nombre, grado, sfm de catálogo, pág. de velocidad, rango de avance, prof. máx., tira de avance
# (grupo P = acero aleado, SAE 4140; datos de Kennametal Universal, ver capturas/indice.json)
INFO = {
    'T0101': ('DESBASTE EXTERIOR', 'DESBASTE', 'KU30T', 500, 'A5', '0,2 - 0,6', '6,4 mm', 'tira_T0101_RP.png'),
    'T0303': ('TERMINACIÓN: DIAGONALES Y RADIOS BRUTOS', 'TERMINACIÓN', 'KU10T', 650, 'A5', '0,1 - 0,3', '2,5 mm', 'tira_T0303_FP.png'),
    'T0505': ('RANURADO Y TRONZADO', 'RANURADO-TRONZADO ∅3', 'KU30T', 400, 'A71', None, 'aprox. 1,6 - 2,0 mm (según gráfico A70)\n(17 mm = profundidad de la ranura del portaherramienta, CD)', None),
    'T0909': ('ACABADO DEL PERFIL (NEUTRA, EN LOS DOS SENTIDOS)', 'ACABADO NEUTRO', 'KU10T', 650, 'A5', '0,1 - 0,3', '2,5 mm', 'tira_T0303_FP.png'),
    'T1010': ('RADIOS Y DIAGONALES LADO IZQUIERDO', 'ACABADO ULTRAFINO', 'KU10T', 650, 'A5', '0,2 - 0,4', '2,3 mm', 'tira_T0909_LF.png'),
    'T0404': ('TERMINACIÓN LADO IZQUIERDO: PAREDES QUE BAJAN HACIA LA BASE', 'TERMINACIÓN IZQUIERDA', 'KU10T', 650, 'A5', '0,1 - 0,3', '2,5 mm', 'tira_T0303_FP.png'),
    'T1111': ('TRONZADO', 'RANURADO-TRONZADO ∅6', 'KU30T', 400, 'A71', None, 'aprox. 4 mm (según gráfico A70)\n(26 mm = profundidad de la ranura del portaherramienta, CD)', None),
}
TAMANO = {'T0505': 3, 'T1111': 6}  # tamaño de inserto (gráfico A70)
# página de catálogo: (título rojo, imagen, herramientas que la usan)
PAGINAS_CAT = [('T0101', 'T0101.png', ('T0101',)), ('T0303', 'T0303.png', ('T0303',)),
               ('T0505', 'T0505_GMN.png', ('T0505',)), ('T1111', 'T1111.png', ('T1111',)),
               ('T0909 (8)', 'T0909_DVVNN.png', ('T0909',)),
               ('T0909 (3) / T1010 (4)', 'T0909_T1010.png', ('T1010',))]
TITULOS = {'PEON': 'PEÓN'}
CICLOS = ['G90', 'G94', 'G01', 'G02', 'G03']

# ---------- XML ----------
NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
      'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
      'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"')
W_TEXTO = 9026  # A4 con márgenes de 2,54 cm
ANCHO_CM = 15.9  # ancho útil en cm (9026 dxa = 15,92 cm)


def run(t, font='Calibri', sz=22, b=False, i=False, color='000000', hl=False):
    rp = (f'<w:rFonts w:ascii="{font}" w:hAnsi="{font}" w:cs="{font}" w:eastAsia="{font}"/>'
          + ('<w:b/><w:bCs/>' if b else '') + ('<w:i/><w:iCs/>' if i else '')
          + f'<w:color w:val="{color}"/>' + ('<w:highlight w:val="yellow"/>' if hl else '') + f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>')
    return f'<w:r><w:rPr>{rp}</w:rPr><w:t xml:space="preserve">{escape(t)}</w:t></w:r>'


def brk():
    return '<w:r><w:br/></w:r>'


def para(runs, jc='left', after=0, line=240, keep=False, pb=False, ind=0):
    pp = (('<w:pageBreakBefore/>' if pb else '') + ('<w:keepNext/>' if keep else '')
          + f'<w:spacing w:before="0" w:after="{after}" w:line="{line}" w:lineRule="auto"/>'
          + (f'<w:ind w:left="{ind}"/>' if ind else '') + f'<w:jc w:val="{jc}"/>')
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
    par = pieza.get('estrategia') == 'par'   # TP con herramientas derecha e izquierda
    if par:
        HERR['T0505'] = ('A4SM R/L 2020K0317', 'A75', 'A4G0305M03U02GMN', 'A73')
        INFO['T0303'] = ('TERMINACIÓN LADO DERECHO: PERFIL HACIA LA BASE',) + INFO['T0303'][1:]
        PAGINAS_CAT[:] = [('T0101', 'T0101.png', ('T0101',)),
                          ('T0303 (3) / T0404 (4)', 'T0303.png', ('T0303', 'T0404')),
                          ('T0505', 'T0505_2020_GMN.png', ('T0505',))]
    titulo = TITULOS.get(nombre, nombre)
    bruto = pieza['bruto']
    ncs = glob.glob(os.path.join(args.winunisoft, '*.nc'))
    if not ncs:
        sys.exit('No hay .nc en ' + args.winunisoft)
    nc = ncs[0]
    prj = nc[:-3] + '.prj'
    bloques = parsear_nc(nc)
    usa4 = any(b['t'] == 'T0404' for b in bloques)
    if par and not usa4:
        PAGINAS_CAT[1] = ('T0303', 'T0303.png', ('T0303',))
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
    vista = recorte_vista_lateral(plano, tmp) if plano else None
    if vista:
        cuerpo.append(para([im.inline(vista, 12.0, 7.5)], 'center', 120))
        cuerpo.append(para([run('Vista lateral de la pieza (recorte del plano en FreeCAD)', sz=18, i=True, color='595959')], 'center', 600))
    else:
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
    # una sola tabla de 4 columnas a todo el ancho útil; las 3 filas de arriba van combinadas (gridSpan=4)
    w4 = [1700, 2800, 2100, 2426]
    assert sum(w4) == W_TEXTO
    def tc4(t, sz=22):
        ps = ''.join(para([run(l, sz=sz)], jc='center') for l in t.split('\n'))
        return cell(ps, W_TEXTO, 'center', span=4)
    cuerpo.append(para([], pb=True))
    cuerpo.append(table([
        row([tc4('ESCUELA DE EDUCACIÓN SECUNDARIA TÉCNICA N°3', 24)]),
        row([tc4('DISEÑO Y PROCESAMIENTO MECÁNICO', 24)]),
        row([tc4('MATERIAL ' + pieza['material'])]),
        row([tc('ESTUDIANTE', w4[0]), tc(args.alumno, w4[1]), tc('REVISADO POR', w4[2]), tc('', w4[3])]),
        row([tc('TEMA', w4[0]), tc('TRABAJO PRÁCTICO: ' + nombre, w4[1]), tc('FECHA PRESENTACIÓN', w4[2]), tc(args.fecha, w4[3])]),
    ], w4))
    filas = [row([tc('OPERACIÓN N°', w4[0], b=True), tc('PARÁMETROS', w4[1], b=True),
                  tc('HERRAMIENTAS', w4[2], b=True), tc('ESQUEMA DE PROCESO', w4[3], b=True)], 400)]
    for n, b in enumerate(bloques, 1):
        t = b['t']
        hold, hp, ins, ip = HERR[t]
        op = INFO[t][0]
        if par and t == 'T0505':
            op = 'TRONZADO' if any('X-1' in l for l in b['lineas']) else 'RANURADO Y DESBASTE DE VALLES'
        par = f'VC: {b["vc"]} m/min\n(grupo P, {INFO[t][2]}, pág. {INFO[t][4]})\nAVANCE: ' + ' / '.join(fmt(v) for v in b['f']) + ' mm/vuelta\nCICLO: ' + '-'.join(b['ciclos'])
        her = f'{t}\nINSERTO: {ins} (pág. {ip})\nPORTAHERRAMIENTA: {hold} (pág. {hp})'
        if b['xs'] and b['zs']:
            m5 = lambda v: fmt(round(v * 2) / 2)  # a 0,5 mm
            esq = (f'Zona de corte:\nZ {m5(min(0.0, max(b["zs"])))} a {m5(min(b["zs"]))} mm\n'
                   f'Ø {m5(max(0.0, min(b["xs"])))} a {m5(max(b["xs"]))} mm')
        else:
            esq = ''
        op_img = os.path.join(args.esquemas, f'op{n}.png') if args.esquemas else ''
        if op_img and os.path.exists(op_img):
            from PIL import Image as _I
            rec = os.path.join(tmp, f'esq{n}.png')
            _I.open(op_img).convert('RGB').crop((400, 290, 885, 640)).save(rec)
            celda = cell(para([im.inline(rec, 3.1)], 'center') +
                         ''.join(para([run(l, sz=16)], 'center') for l in esq.split('\n')[1:]), w4[3], 'center')
        else:
            celda = tc(esq, w4[3], sz=18)
        filas.append(row([tc(f'{n}\n{op}', w4[0]), tc(par, w4[1], sz=20), tc(her, w4[2], sz=16), celda], 1300))
    cuerpo.append(para([], after=0))
    cuerpo.append(table(filas, w4))
    if tray:
        cuerpo.append(para([run('TRAYECTORIA DE LAS HERRAMIENTAS (WinUnisoft)', sz=22, b=True)], 'center', 60, keep=True))
        cuerpo.append(para([im.inline(tray, ANCHO_CM, 20.0)], 'center', 60, keep=True))
        cuerpo.append(para([run('Trayectoria de las herramientas generada desde el programa (cada color es una herramienta; '
                                'las líneas punteadas son movimientos rápidos G00).', sz=20, i=True)], 'center', 120))
        fin = sorted(glob.glob(os.path.join(args.esquemas, 'op*.png')), key=lambda f: int(re.findall(r'\d+', os.path.basename(f))[0])) if args.esquemas else []
        if fin:
            cuerpo.append(para([run('SIMULACIÓN EN WINUNISOFT (PIEZA TERMINADA, SIN COLISIONES)', sz=22, b=True)], 'center', 60, keep=True))
            from PIL import Image as _I
            rec = os.path.join(tmp, 'final.png')
            _I.open(fin[-1]).convert('RGB').crop((250, 250, 885, 680)).save(rec)
            cuerpo.append(para([im.inline(rec, ANCHO_CM, 10.5)], 'center', 60))

    # 4. plano
    cuerpo.append(para([run('PLANO', sz=48, b=True)], 'left', 120, pb=True, keep=True))
    if plano:
        cuerpo.append(para([im.inline(plano, ANCHO_CM, 23.3)], 'center'))

    # 5. programación CNC
    cuerpo.append(para([run('PROGRAMACIÓN CNC', sz=48, b=True)], 'left', 200, pb=True, keep=True))
    # programa largo (más de 120 líneas): tres columnas, para que entre en una página
    ncol = 3 if len(prog) > 120 else 2
    paso = (len(prog) + ncol - 1) // ncol
    def col(ls):
        return ''.join(para([run(l, 'Courier New', 18)]) for l in ls)
    cw = [W_TEXTO // ncol] * (ncol - 1) + [W_TEXTO - (W_TEXTO // ncol) * (ncol - 1)]
    cuerpo.append(table([row([cell(col(prog[k * paso:(k + 1) * paso]), cw[k], 'top') for k in range(ncol)], 300, split=True)], cw))

    def img(nombre):
        p = os.path.join(args.capturas, nombre) if args.capturas else ''
        return p if p and os.path.exists(p) else None

    def roja(t, sz=40, pb=False):
        return para([run(t, sz=sz, color='C00000')], 'left', 120, pb=pb, keep=True)

    def vcs(t):
        return next((b['vc'] for b in bloques if b['t'] == t), None)

    # 6. aclaraciones
    cuerpo.append(para([run('ACLARACIONES:', sz=48, b=True, color='ff0000')], 'left', 200, pb=True, keep=True))
    cuerpo.append(para([run('Cuando una herramienta esté señalizada con un número entre paréntesis al lado [(3) o (4)] se refiere a su '
                            'código de forma. Solo se emplea en las herramientas en las que este fue cambiado, de lo contrario, el '
                            'código de forma es 3 siempre.'), brk(),
                        run('EJ: T0404 (4) = herramienta izquierda' if par else 'EJ: T0909 (8) = herramienta neutra')], 'left', 300))
    cuerpo.append(para([run('Las velocidades de corte se toman del catálogo Kennametal Universal con el grupo P, porque el '
                            + pieza['material'] + ' es un acero aleado.'
                            + ('' if par else ' En los TP anteriores se usó el grupo M (acero inoxidable).'))], 'left', 200))
    if par:
        cuerpo.append(para([run('Selección de herramientas: se usan las mismas herramientas en los dos sentidos (derecha e '
                                'izquierda). La T0303 es un portaherramientas DVJN R/L 2020K16KC04 (93°, página A27) '
                                'con inserto VNMG160404FP (página A14). La T0404 es el mismo portaherramientas en su versión izquierda '
                                '(código de forma 4): termina las paredes que bajan de diámetro hacia la base cortando hacia +Z, donde la '
                                'T0303 no llega porque su ángulo libre es de unos 52°. La T0101 (DCLN R/L 2020K12KC04 con CNMG120408RP) '
                                'desbasta; no hace falta su versión izquierda (T0202) porque los valles quedan entre dos paredes y desde la '
                                'base no se puede entrar. La T0505 es el A4SM R/L 2020K0317 (página A75), con mango de 20×20 como las '
                                'demás, e inserto A4G0305M03U02GMN (página A73): ranura, desbasta los valles con G90 en los dos sentidos '
                                '(el sistema A4 ranura y tornea) y tronza. GMN es la geometría para acero (página A70).'
                                + ('' if usa4 else ' En esta pieza no hace falta la T0404: ninguna pared baja de diámetro hacia '
                                   'la base más empinada que 46°, así que la T0303 termina todo el perfil.'))], 'left', 200))
        cuerpo.append(para([run('Optimización de pasadas (página A7): el G90 de la T0101 baja 6 mm en diámetro por pasada (3 mm por '
                                'lado, rango del rompevirutas RP de 1,1 a 6,4 mm) con avance de 0,4 mm/vuelta (rango de 0,2 a 0,6). '
                                'Después la misma T0101 hace una pasada de contorno que deja 0,3 mm por lado. En los valles, la T0505 '
                                'entra en el punto más hondo y desbasta con G90 de 3,2 mm en diámetro (1,6 mm por lado, gráfico A70). '
                                + ('La T0303 y la T0404 sacan' if usa4 else 'La T0303 saca') +
                                ' los 0,3 mm finales, dentro del rango de 0,3 a 2,5 mm del rompevirutas FP. '
                                'El inserto de ranurado mide 3,05 mm de ancho y tiene radio 0,2; el programa usa ese ancho para las '
                                'ranuras y el tronzado. El programa usa solo G00, G01, G02, G03 y G90, sin ciclos automáticos '
                                'como G71 o G72.')], 'left', 200))
    if not par:
      cuerpo.append(para([run('Selección de herramientas: la T0909 es un portaherramientas neutro DVVNN (72,5°) con el mismo inserto '
                            'VNMG160404FP de la T0303; copia el perfil en los dos sentidos, así que reemplaza a las dos herramientas '
                            'de acabado (derecha e izquierda) y tiene más despeje en cuellos y gargantas. La T0505 (3,05 mm) ranura y '
                            'también tronza: alcanza para piezas de hasta Ø26 y se pierde menos material que con una cuchilla de 6 mm. '
                            'El inserto de ranurado es A4G...GMN, porque la página A70 del catálogo recomienda GMN para acero '
                            '(GMP es para acero inoxidable).')], 'left', 200))
    if not par:
      cuerpo.append(para([run('Profundidades de pasada (página A7 del catálogo): el desbaste con G90 baja 2,4 mm en diámetro '
                            '(1,2 mm por lado), dentro del rango de 1,1 a 6,4 mm del rompevirutas RP. El desbaste deja 0,6 mm '
                            'por lado: la T0303 saca 0,3 mm y la T0909 los 0,3 mm finales, dentro del rango de 0,3 a 2,5 mm del '
                            'rompevirutas FP. El inserto de ranurado A4G0305M03U02GMN mide 3,05 mm de ancho y tiene radio 0,2 '
                            '(página A73); el programa usa ese ancho para las ranuras y el tronzado.')], 'left', 200))
    for nom, pg in (('vel_A5_P.png', 'A5'), ('vel_A71_P.png', 'A71')):
        if img(nom):
            cuerpo.append(para([run(f'Velocidad de las herramientas de {"torneado" if pg == "A5" else "ranurado"} ', sz=22),
                                run(f'(P) (PÁG {pg})', hl=True)], 'left', 60, keep=True))
            cuerpo.append(para([im.inline(img(nom), 15.5)], 'left', 200))

    # 7. características de la pieza
    cuerpo.append(para([run('CARACTERÍSTICAS PIEZA:', sz=48, b=True)], 'left', 200, pb=True, keep=True))
    carac = [('Nombre', nombre), ('Material', pieza['material'] + ' (grupo P, acero aleado)'),
             ('Bruto', f'Ø = {bruto["d"]} mm, L = {bruto["l"]} mm'),
             ('Largo de la pieza', f'{pieza["largo"]} mm'),
             ('Punto cero', f'G54, Z = {fmt(bruto["l"] - 1)} mm'),
             ('Torno', 'Apolo, control Fanuc 16i-TA (simulador WinUnisoft)'),
             *([('Tiempo de mecanizado', args.tiempo + ' (simulación en WinUnisoft)')] if args.tiempo else []),
             ('Catálogo de herramientas', 'Kennametal Universal')]
    for t in dict.fromkeys(b['t'] for b in bloques):
        _, _, gr, sfm, pg, _, _, _ = INFO[t]
        carac.append((f'Velocidad {t}', f'{vcs(t)} m/min (grupo P, {gr}, pág. {pg})'))
    wc = [3400, W_TEXTO - 3400]
    cuerpo.append(table([row([tc(a, wc[0], b=True, jc='left'), tc(v, wc[1], jc='left')], 400) for a, v in carac], wc))

    # 8. una sección por herramienta, en el estilo del informe original
    for k, t in enumerate(dict.fromkeys(b['t'] for b in bloques)):
        op, nom, gr, sfm, pg, rango, prof, tira = INFO[t]
        forma = formas.get(t, 4 if t in ('T1010', 'T0404') else 3)
        bl = next(b for b in bloques if b['t'] == t)
        f_usado = ' / '.join(fmt(v) for v in bl['f'])
        ficha = os.path.join(args.fichas, f'{t}.png') if args.fichas else ''
        if ficha and os.path.exists(ficha):
            # como el TP original: página propia con la ficha de la herramienta en WinUnisoft
            cuerpo.append(para([run(f'HERRAMIENTA {nom} ({t})', sz=40, color='C00000')], 'center', 120, pb=True, keep=True))
            cuerpo.append(para([im.inline(ficha, ANCHO_CM, 14.0)], 'center', 160))
        cuerpo.append(roja(f'CARACTERÍSTICAS {t}:', pb=False))
        vel = f'Velocidad: {bl["vc"]} m/min o {sfm}sfm (grupo P, grado {gr}, pág. {pg})'
        if rango:
            av = f'Avance: {f_usado} ({rango})'
        else:
            av = f'Avance: según gráfico A70 (en el programa: {f_usado})'
        pl = prof.split('\n')
        extra = ['Ver gráfico de avance A70.'] if not tira else []
        con_tira = bool(tira and img(tira))
        for l in (vel, av, f'Profundidad de corte máxima: {pl[0]}', *pl[1:], f'Código de forma: {forma}', *extra):
            cuerpo.append(para([run(l)], 'left', 60, keep=con_tira))  # con tira: título, líneas y tira juntos
        if con_tira:
            cuerpo.append(para([im.inline(img(tira), ANCHO_CM * 0.75)], 'left', 100))

    # 9. herramientas usadas (texto plano)
    cuerpo.append(para([run('HERRAMIENTAS USADAS', sz=48, b=True)], 'left', 200, pb=True, keep=True))
    if alumno:
        cuerpo.append(para([run('ALUMNO: ' + alumno)]))
    cuerpo.append(para([run('MANUAL USADO: “Kennametal Universal”')], 'left', 200))
    cuerpo.append(para([run('HERRAMIENTAS USADAS:')], 'left', 100))
    base = lambda t: (HERR[t][0].split(' (')[0], HERR[t][2])
    ordenadas = list(dict.fromkeys(b['t'] for b in bloques))
    vistos = []
    for t in ordenadas:
        if base(t) in vistos:
            continue
        vistos.append(base(t))
        hold, hp, ins, ip = HERR[t]
        grupo = [x for x in ordenadas if base(x) == base(t)]
        uso = 'RÓMBICA ULTRAFINA' if len(grupo) > 1 else INFO[t][1]
        cuerpo.append(para([run(f'PORTAHERRAMIENTA {uso} ({", ".join(grupo)}): {base(t)[0]} (PÁG {hp})'.upper())], 'left', 0, ind=567))
        cuerpo.append(para([run(f'INSERTO {uso}: {ins} (PÁG {ip})'.upper())], 'left', 160, ind=567))

    # 10. avance de ranurado (A70)
    ran = [t for t in ('T1111', 'T0505') if t in {b['t'] for b in bloques}]
    if ran:
        cuerpo.append(para([run('AVANCE ' + ' / '.join(ran) + ':', sz=40, color='C00000')], 'left', 120, keep=True))
        a70 = 'avance_A70_GMN.png' if img('avance_A70_GMN.png') else 'avance_A70.png'
        if img(a70):
            cuerpo.append(para([im.inline(img(a70), 15.0, 15.0)], 'left', 120))
        for t in ran:
            f = ' / '.join(fmt(v) for v in next(b for b in bloques if b['t'] == t)['f'])
            cuerpo.append(para([run(f'El tamaño del inserto de {t} es {TAMANO[t]}, por eso la herramienta se usa con un avance de {f} mm/vuelta (PÁG A70).')], 'left', 100))

    # 11. páginas de catálogo: una por herramienta, al final
    usadas = {b['t'] for b in bloques}
    for titulo_p, nombre_img, ts in PAGINAS_CAT:
        if img(nombre_img) and usadas & set(ts):
            cuerpo.append(roja(titulo_p, sz=56, pb=True))
            cuerpo.append(para([im.inline(img(nombre_img), ANCHO_CM, 23.2)], 'center'))

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



def recorte_vista_lateral(png_plano, carpeta):
    """Recorta del plano (A4 a 150 dpi) la vista lateral horizontal con sus cotas: zona abajo a la derecha,
    sobre el rótulo; después ajusta el recorte a lo dibujado."""
    try:
        from PIL import Image, ImageOps
    except ImportError:
        return None
    im = Image.open(png_plano).convert('L')
    k = im.width / 210.0                       # px por mm
    caja = im.crop((int(103 * k), int(112 * k), int(197 * k), int(224 * k)))
    bb = ImageOps.invert(caja).point(lambda v: 255 if v > 40 else 0).getbbox()
    if not bb:
        return None
    m = int(2 * k)
    bb = (max(0, bb[0] - m), max(0, bb[1] - m), min(caja.width, bb[2] + m), min(caja.height, bb[3] + m))
    salida = os.path.join(carpeta, 'vista_lateral.png')
    caja.crop(bb).convert('RGB').save(salida)
    return salida

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
    ap.add_argument('--capturas', default='')
    ap.add_argument('--esquemas', default='', help='carpeta con op1.png, op2.png... (pieza después de cada operación, WinUnisoft)')
    ap.add_argument('--fichas', default='', help='carpeta con T0101.png... (ficha de cada herramienta en WinUnisoft)')
    ap.add_argument('--tiempo', default='', help='tiempo de mecanizado de la simulación, p. ej. 10:53 min')
    construir(ap.parse_args())


if __name__ == '__main__':
    main()
