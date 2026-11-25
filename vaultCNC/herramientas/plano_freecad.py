# -*- coding: utf-8 -*-
"""Plano de una pieza de ajedrez (torno CNC) en FreeCAD/TechDraw.

Uso: plano.sh <pieza.json> <carpeta_salida>  (pasa los datos por PLANO_JSON y PLANO_OUT)
Genera <NOMBRE>.FCStd y "<NOMBRE> plano.pdf". Normalmente se llama con plano.sh.
"""
import os, sys, json, math

import FreeCAD
import Part
import TechDraw
from FreeCAD import Vector as V

AQUI = os.path.dirname(os.path.abspath(__file__))
FUENTE = "Liberation Sans"
PLANTILLA = os.path.join(AQUI, "rotulo_eest3_A4.svg")


def salir(codigo):
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(codigo)


# ---------------------------------------------------------------- geometría
def fmt(v):
    """Número sin ceros de más y con coma decimal (34,5)."""
    s = ("%.2f" % v).rstrip("0").rstrip(".")
    return s.replace(".", ",")


def tramos(perfil):
    """Lista de tramos (z0, r0, z1, r1, arco) en el plano (z, r)."""
    out = []
    for a, b in zip(perfil[:-1], perfil[1:]):
        z0, r0 = a["z"], a["x"] / 2.0
        z1, r1 = b["z"], b["x"] / 2.0
        arco = None
        if "arco" in b:
            R = b["arco"]["r"]
            g = b["arco"]["g"].upper()
            dz, dr = z1 - z0, r1 - r0
            c = math.hypot(dz, dr)
            if c / 2.0 > R + 1e-9:
                raise ValueError("arco imposible (radio %s < media cuerda)" % R)
            h = math.sqrt(max(R * R - c * c / 4.0, 0.0))
            mz, mr = (z0 + z1) / 2.0, (r0 + r1) / 2.0
            nz, nr = -dr / c, dz / c  # normal a la izquierda del avance
            lado = 1.0 if g == "G03" else -1.0  # antihorario: centro a la izquierda
            cz, cr = mz + lado * nz * h, mr + lado * nr * h
            # punto medio del arco menor: del centro hacia el medio de la cuerda
            vz, vr = mz - cz, mr - cr
            n = math.hypot(vz, vr)
            if n < 1e-9:  # semicírculo exacto
                vz, vr = lado * nz * -1.0, lado * nr * -1.0
                n = 1.0
            pz, pr = cz + R * vz / n, cr + R * vr / n
            arco = dict(R=R, cz=cz, cr=cr, pz=pz, pr=pr)
        out.append((z0, r0, z1, r1, arco))
    return out


def pt(z, r):
    return V(r, 0, z)


def radio_maximo(tr):
    """Radio mayor de la pieza, incluyendo lo que se abomba en los arcos."""
    m = 0.0
    for z0, r0, z1, r1, arco in tr:
        m = max(m, r0, r1)
        if arco:
            a0 = math.atan2(r0 - arco["cr"], z0 - arco["cz"])
            a1 = math.atan2(r1 - arco["cr"], z1 - arco["cz"])
            pm = math.atan2(arco["pr"] - arco["cr"], arco["pz"] - arco["cz"])
            # recorrer a0 -> a1 pasando por pm
            def en_arco(a):
                d = (a - a0) % (2 * math.pi)
                dm = (pm - a0) % (2 * math.pi)
                de = (a1 - a0) % (2 * math.pi)
                if dm <= de:
                    return d <= de
                return d >= de or d == 0
            for k in range(0, 360):
                a = math.radians(k)
                if en_arco(a):
                    m = max(m, arco["cr"] + arco["R"] * math.sin(a))
    return m


def construir_solido(tr):
    aristas = []
    for z0, r0, z1, r1, arco in tr:
        if abs(z0 - z1) < 1e-9 and abs(r0 - r1) < 1e-9:
            continue
        if arco:
            aristas.append(Part.Arc(pt(z0, r0), pt(arco["pz"], arco["pr"]), pt(z1, r1)).toShape())
        else:
            aristas.append(Part.makeLine(pt(z0, r0), pt(z1, r1)))
    zf, rf = tr[-1][2], tr[-1][3]
    z0, r0 = tr[0][0], tr[0][1]
    if rf > 1e-9:
        aristas.append(Part.makeLine(pt(zf, rf), pt(zf, 0)))
    if abs(zf - z0) > 1e-9:
        aristas.append(Part.makeLine(pt(zf, 0), pt(z0, 0)))
    if r0 > 1e-9:
        aristas.append(Part.makeLine(pt(z0, 0), pt(z0, r0)))
    alambre = Part.Wire(Part.__sortEdges__(aristas))
    cara = Part.Face(alambre)
    return cara.revolve(V(0, 0, 0), V(0, 0, 1), 360)


# ---------------------------------------------------------------- escala
def parsear_escala(txt):
    try:
        a, b = txt.replace(" ", "").split(":")
        return float(a.replace(",", ".")) / float(b.replace(",", "."))
    except Exception:
        return None


ESCALAS = [(2, "2:1"), (1, "1:1"), (1 / 1.5, "1:1,5"), (0.5, "1:2"), (0.4, "1:2,5"),
           (1 / 3.0, "1:3"), (0.25, "1:4"), (0.2, "1:5")]

DIM_PASO = 5.5        # separación entre cotas encadenadas (mm de hoja)
MAX_Y = 224.0         # límite inferior del dibujo (rótulo empieza en 227)


def distribuir(L, rmax, zs_n, n_top, n_bot, s, rh=None):
    """Calcula posiciones (mm desde arriba-izquierda) para la escala s. Devuelve (ok, dict)."""
    Ls, rs = L * s, rmax * s
    punta_y = 14 + 6 * n_top + 6
    base_y = punta_y + Ls
    fin_dim1 = base_y + 10 + 5.5 * max(n_bot - 1, 0) + (3 if n_bot else 0)
    cx1 = max(58.0, 25 + rs + 24)
    # vista 3: punta a la derecha
    if rh:     # misma cuenta que la cadena real (vista 3): r_hasta + 6, o la anterior + DIM_PASO
        prev = 0.0
        for r in rh:
            prev = max(r * s + 6, prev + DIM_PASO)
        cadena = prev + 4.0
    else:
        cadena = 8 + rs * 0.5 + DIM_PASO * zs_n
    y3 = MAX_Y - cadena
    y2 = max(y3, fin_dim1 + 8 + rs)
    punta_x3 = 190.0
    ok = (Ls <= 92 and
          y2 + rs <= MAX_Y - 4 and
          y3 - rs >= 14 and
          punta_x3 - Ls > cx1 + rs + 8 and
          punta_y > 14)
    return ok, dict(punta_y=punta_y, cx1=cx1, y1=punta_y + Ls / 2.0, y2=y2, y3=y3,
                    x3=punta_x3 - Ls / 2.0, punta_x3=punta_x3, Ls=Ls, rs=rs)


# ---------------------------------------------------------------- principal
def main(ruta_json, carpeta):
    with open(ruta_json, encoding="utf-8") as f:
        P = json.load(f)
    rot = dict(P.get("rotulo", {}))
    nombre = P.get("nombre", rot.get("titulo", "PIEZA"))
    perfil = P["perfil"]
    L = abs(perfil[-1]["z"])
    tr = tramos(perfil)
    rmax = radio_maximo(tr)
    os.makedirs(carpeta, exist_ok=True)

    # cotas: diámetros y cadena de longitudes
    zs = sorted({round(abs(p["z"]), 4) for p in perfil if abs(p["z"]) > 1e-9})
    diams = sorted({round(p["x"], 4) for p in perfil if p["x"] > 1e-9})
    # clasificación arriba/abajo: según la zona de la pieza donde aparece cada diámetro
    def zmin_de(d):
        return min(abs(p["z"]) for p in perfil if abs(p["x"] - d) < 1e-6)
    arriba = [d for d in diams if zmin_de(d) < L / 2.0]
    abajo = [d for d in diams if d not in arriba]

    rh = [max(max(t[1], t[3]) for t in tr if t[2] >= -zz - 1e-9) for zz in zs]
    esc = parsear_escala(rot.get("escala", ""))
    esc_txt = rot.get("escala", "")
    if esc:
        ok, lay = distribuir(L, rmax, len(zs), len(arriba), len(abajo), esc, rh)
        s = esc
    else:
        s = None
        for cand, txt in ESCALAS:
            ok, lay = distribuir(L, rmax, len(zs), len(arriba), len(abajo), cand, rh)
            if ok:
                s, esc_txt = cand, txt
                break
        if s is None:
            s, esc_txt = ESCALAS[-1]
            ok, lay = distribuir(L, rmax, len(zs), len(arriba), len(abajo), s, rh)
        rot["escala"] = esc_txt
    print("Escala %s (%.3f)" % (esc_txt, s))

    doc = FreeCAD.newDocument(nombre)
    pieza = doc.addObject("Part::Feature", "Pieza")
    pieza.Shape = construir_solido(tr)
    pieza.Label = nombre

    tmpl = doc.addObject("TechDraw::DrawSVGTemplate", "Rotulo")
    tmpl.Template = PLANTILLA
    campos = {
        "titulo": rot.get("titulo", nombre), "colegio": rot.get("colegio", ""),
        "dibujo_fecha": rot.get("dibujo_fecha", ""), "dibujo_nombre": rot.get("dibujo_nombre", ""),
        "reviso_fecha": rot.get("reviso_fecha", ""), "reviso_nombre": rot.get("reviso_nombre", ""),
        "aprobo_fecha": rot.get("aprobo_fecha", ""), "aprobo_nombre": rot.get("aprobo_nombre", ""),
        "escala": rot.get("escala", ""), "normativa": rot.get("normativa", ""),
        "curso": rot.get("curso", ""), "lamina": rot.get("lamina", ""),
        "nota": rot.get("nota", ""), "observacion": rot.get("observacion", ""),
    }
    tmpl.EditableTexts = campos
    page = doc.addObject("TechDraw::DrawPage", "Plano")
    page.Template = tmpl

    def vista(nom, direccion, xdir, cx, cy):
        v = doc.addObject("TechDraw::DrawViewPart", nom)
        page.addView(v)
        v.Source = [pieza]
        v.Direction = direccion
        v.XDirection = xdir
        v.ScaleType = "Custom"
        v.Scale = s
        v.X = cx
        v.Y = 297 - cy
        v.HardHidden = False
        v.SmoothHidden = False
        return v

    v1 = vista("Vista1", V(0, -1, 0), V(1, 0, 0), lay["cx1"], lay["y1"])
    v2 = vista("Vista2", V(0, 0, 1), V(1, 0, 0), lay["cx1"], lay["y2"])
    v3 = vista("Vista3", V(0, -1, 0), V(0, 0, 1), lay["x3"], lay["y3"])
    for v in (v1, v2, v3):
        try:
            vp = v.ViewObject
            vp.LineWidth = 0.7
            vp.FaceColor = (1.0, 1.0, 1.0, 1.0)
        except Exception:
            pass
    doc.recompute()
    esperar_geometria((v1, v2, v3))
    acotar(doc, page, v1, v2, v3, lay, zs, arriba, abajo, tr, L, rmax, s)
    doc.recompute()
    return doc, page, (v1, v2, v3), lay, nombre


# ---------------------------------------------------------------- cotas
def esperar_geometria(vistas, limite=60.0):
    """TechDraw (FreeCAD 1.x) proyecta las vistas en segundo plano: esperar a que terminen."""
    import time
    try:
        from PySide import QtGui
        app = QtGui.QApplication.instance()
    except Exception:
        app = None
    t0 = time.time()
    while time.time() - t0 < limite:
        listas = True
        for v in vistas:
            try:
                if not v.getVisibleEdges():
                    listas = False
            except Exception:
                listas = False
        if listas:
            return
        if app:
            app.processEvents()
        time.sleep(0.1)
        for v in vistas:
            try:
                if not v.getVisibleEdges():
                    v.recompute()
            except Exception:
                pass
    print("AVISO: alguna vista no tiene geometria despues de %.0f s" % limite)


def indice_vertice(vista, x, y, tol=0.05):
    # las coordenadas de los vertices vienen ya multiplicadas por la escala de la vista
    x, y = x * vista.Scale, y * vista.Scale
    mejor, d_mejor = None, 1e9
    for i, q in enumerate(vista.getVisibleVertexes()):
        d = math.hypot(q.x - x, q.y - y)
        if d < d_mejor:
            mejor, d_mejor = i, d
    if d_mejor > tol:
        raise ValueError("vertice no encontrado (%.2f, %.2f) dist %.3f" % (x, y, d_mejor))
    return mejor


def nueva_cota(doc, page, tipo, vista, refs, x, y, formato, valor=None, fuente=3.5):
    d = doc.addObject("TechDraw::DrawViewDimension", "Cota")
    page.addView(d)
    d.Type = tipo
    d.References2D = [(vista, r) for r in refs]
    d.FormatSpec = formato
    if valor is not None:
        # el texto sale del JSON (evita 2,99 por redondeos de la proyección)
        # coma decimal (34,5): el texto queda fijo, la geometria sigue siendo la misma
        d.Arbitrary = True
        d.FormatSpec = formato.split("%")[0] + fmt(valor)
    d.ShowUnits = False
    d.X = x
    d.Y = y
    try:
        vp = d.ViewObject
        vp.Font = FUENTE
        vp.Fontsize = fuente
        vp.LineWidth = 0.25
        vp.Arrowsize = 2.5
    except Exception:
        pass
    return d


def linea_eje(vista, p1, p2):
    tag = vista.makeCosmeticLine(V(p1[0], p1[1], 0), V(p2[0], p2[1], 0))
    ce = vista.getCosmeticEdge(tag)
    ce.Format = {'style': 4, 'weight': 0.25, 'color': (0.0, 0.0, 0.0, 1.0), 'visible': True}
    return ce


def acotar(doc, page, v1, v2, v3, lay, zs, arriba, abajo, tr, L, rmax, s):
    zc = -L / 2.0
    # ---- ejes
    ext = 6.0 / s
    linea_eje(v1, (0, -L / 2 - ext), (0, L / 2 + ext))
    linea_eje(v3, (-L / 2 - ext, 0), (L / 2 + ext, 0))
    linea_eje(v2, (-rmax - ext, 0), (rmax + ext, 0))
    linea_eje(v2, (0, -rmax - ext), (0, rmax + ext))

    # ---- vista 1: diametros (x = +-r; y hacia abajo = -(z - zc))
    def y1(z):
        return -(z - zc)

    zs_d = {}
    for t in tr:
        for (z, r) in ((t[0], t[1]), (t[2], t[3])):
            zs_d.setdefault(round(2 * r, 4), []).append(z)
    cx, cy = lay["cx1"], lay["y1"]
    # arriba: el mayor queda mas afuera
    for k, d in enumerate(sorted(arriba, reverse=True)):
        z = max(zs_d[d])  # el vertice mas cercano a la punta
        yv = y1(z)
        i1 = indice_vertice(v1, -d / 2.0, yv)
        i2 = indice_vertice(v1, d / 2.0, yv)
        yl = (lay["punta_y"] - 8 - 6 * (len(arriba) - 1 - k))
        # posicion de la cota: relativa al centro de la vista, en hoja
        nueva_cota(doc, page, "DistanceX", v1, ["Vertex%d" % i1, "Vertex%d" % i2],
                   0, (cy - yl), "\u00d8%.2w", d)
    for k, d in enumerate(sorted(abajo)):
        z = min(zs_d[d])
        yv = y1(z)
        i1 = indice_vertice(v1, -d / 2.0, yv)
        i2 = indice_vertice(v1, d / 2.0, yv)
        yl = lay["punta_y"] + lay["Ls"] + 10 + 5.5 * k
        nueva_cota(doc, page, "DistanceX", v1, ["Vertex%d" % i1, "Vertex%d" % i2],
                   0, -(yl - cy), "\u00d8%.2w", d)

    # ---- vista 1: radios de los arcos (se toma el arco del lado izquierdo)
    bordes = list(v1.getVisibleEdges())
    ultimo_R, ultimo_z = None, None
    for z0, r0, z1, r1, arco in tr:
        if not arco:
            continue
        p0, p1 = (-r0 * s, y1(z0) * s), (-r1 * s, y1(z1) * s)
        hallado = None
        for i, e in enumerate(bordes):
            if len(e.Vertexes) < 2 or type(e.Curve).__name__ != "Circle":
                continue
            a, b = e.Vertexes[0].Point, e.Vertexes[-1].Point
            def cerca(q, p):
                return math.hypot(q.x - p[0], q.y - p[1]) < 0.05
            if (cerca(a, p0) and cerca(b, p1)) or (cerca(a, p1) and cerca(b, p0)):
                hallado = i
                break
        if hallado is None:
            continue
        # dos arcos seguidos del mismo radio (collarín) llevan una sola cota
        if ultimo_R is not None and abs(ultimo_R - arco["R"]) < 1e-9 and abs(ultimo_z - z0) < 1e-9:
            ultimo_R, ultimo_z = arco["R"], z1
            continue
        ultimo_R, ultimo_z = arco["R"], z1
        lx = -(rmax * s + 14)
        ly = -y1(arco["pz"]) * s + 7
        if arco["R"] * s > 25:
            # radio grande (cóncavo): el centro cae fuera de la hoja y la cota de radio
            # trazaría la línea desde ahí; se pone texto + línea de referencia corta
            nota = doc.addObject("TechDraw::DrawViewAnnotation", "RadioGrande")
            page.addView(nota)
            nota.Text = ["R" + fmt(arco["R"])]
            nota.TextSize = 3.5
            try:
                nota.Font = FUENTE
            except Exception:
                pass
            nota.X = float(getattr(v1.X, "Value", v1.X)) + lx + 3
            nota.Y = float(getattr(v1.Y, "Value", v1.Y)) + ly + 1.5
            q = (-arco["pr"], y1(arco["pz"]))
            fin = ((lx + 8) / s, y1(arco["pz"]) - 7 / s)
            tag = v1.makeCosmeticLine(V(q[0], q[1], 0), V(fin[0], fin[1], 0))
            ce = v1.getCosmeticEdge(tag)
            ce.Format = {'style': 1, 'weight': 0.25, 'color': (0.0, 0.0, 0.0, 1.0), 'visible': True}
            continue
        nueva_cota(doc, page, "Radius", v1, ["Edge%d" % hallado], lx, ly, "R%.2w", arco["R"])

    # ---- vista 3: cadena de longitudes desde la punta (x = z - zc, hacia la derecha la punta)
    def x3(z):
        return z - zc
    cy3 = lay["y3"]
    prev = 0.0
    for k, zz in enumerate(zs):
        z = -zz
        # ultimo vertice (el mas bajo de la hoja = y mayor) en esa z
        cands = [(q.y, i) for i, q in enumerate(v3.getVisibleVertexes()) if abs(q.x - x3(z) * s) < 0.05]
        if not cands:
            continue
        i_z = max(cands)[1]
        # vertice de la punta: sobre el eje si es una bola; si la cara es plana (torre) no hay
        # vertice en el eje, se toma cualquiera en Z0 (la cota DistanceX solo mira la X)
        tips = [(q.y, i) for i, q in enumerate(v3.getVisibleVertexes()) if abs(q.x - x3(0) * s) < 0.05]
        itip = max(tips)[1] if tips else indice_vertice(v3, x3(0), 0)
        # radio visible hasta z: sobre el eje hay que pasar la silueta
        r_hasta = max(max(t[1], t[3]) for t in tr if t[2] >= z - 1e-9) * s
        prev = max(r_hasta + 6, prev + DIM_PASO)
        xm = (x3(0) + x3(z)) / 2.0
        nueva_cota(doc, page, "DistanceX", v3, ["Vertex%d" % itip, "Vertex%d" % i_z],
                   xm * s, -prev, "%.2w", zz, 3.2)


def exportar(doc, page, carpeta, nombre):
    """Guarda el .FCStd y exporta el PDF con la GUI (TechDrawGui, modo offscreen)."""
    ruta_fc = os.path.join(carpeta, nombre + ".FCStd")
    ruta_pdf = os.path.join(carpeta, nombre + " plano.pdf")
    doc.recompute()
    doc.saveAs(ruta_fc)
    print("Guardado:", ruta_fc)
    import FreeCADGui
    import TechDrawGui
    # abrir la hoja (crea la escena con rotulo y vistas) antes de exportar
    try:
        FreeCADGui.getDocument(doc.Name).getObject(page.Name).doubleClicked()
        FreeCADGui.updateGui()
    except Exception as e:
        print("aviso: no se pudo abrir la hoja:", e)
    TechDrawGui.exportPageAsPdf(page, ruta_pdf)
    print("PDF:", ruta_pdf)
    salir(0)


if True:  # FreeCAD ejecuta el script con otro __name__
    # por entorno (plano.sh) o por argumentos (FreeCADCmd ... script json carpeta)
    a = [os.environ.get("PLANO_JSON"), os.environ.get("PLANO_OUT")]
    if not all(a):
        idx = [i for i, x in enumerate(sys.argv) if x.endswith("plano_freecad.py")]
        a = sys.argv[idx[-1] + 1:] if idx else []
    if len(a) < 2:
        print("Uso: plano.sh <pieza.json> <carpeta_salida>")
        salir(2)
    try:
        doc, page, vistas, lay, nombre = main(a[0], a[1])
        exportar(doc, page, a[1], nombre)
    except Exception:
        import traceback
        traceback.print_exc()
        salir(1)
