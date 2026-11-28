#!/usr/bin/env python3
"""Verifica un programa .nc de torno (Fanuc 16i-TA, WinUnisoft) y dibuja la trayectoria."""
import argparse
import math
import os
import re
import sys

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

G_OK = {0, 1, 2, 3, 54, 90, 94, 96, 97}
M_OK = {3, 4, 5, 30}
COLORES = ["#1f77b4", "#2ca02c", "#9467bd", "#ff7f0e", "#8c564b", "#e377c2",
           "#17becf", "#bcbd22", "#0b6e4f", "#7f7f7f", "#d4a017", "#006d77"]


def leer_prj(ruta):
    """Lee el .prj (INI con claves repetidas) y devuelve un dict simple."""
    d = {"diam": None, "largo": None, "g54z": 0.0, "tools": {}}
    seccion = ""
    with open(ruta, encoding="latin-1") as f:
        for lin in f:
            lin = lin.strip()
            m = re.match(r"\[(.+)\]$", lin)
            if m:
                seccion = m.group(1).upper()
                continue
            if seccion == "BRUTO":
                if lin.startswith("ZMax/DExt="):
                    d["diam"] = float(lin.split("=")[1])
                elif lin.startswith("YMax/ZMax="):
                    d["largo"] = float(lin.split("=")[1])
            elif seccion == "ORIGEN" and lin.startswith("G54="):
                p = lin.split("=")[1].split(",")
                if len(p) >= 3:
                    d["g54z"] = float(p[2])
            elif seccion == "TOOLS" and lin.startswith("Tool="):
                n = re.search(r"_NumHta=(\d+)", lin)
                if n:
                    t = re.search(r"Type=(\w+)", lin)
                    d["tools"][int(n.group(1))] = t.group(1) if t else "?"
    return d


class Sim:
    def __init__(self, args, prj):
        self.errores = []
        self.avisos = []
        self.segs = []  # (tipo, p0, p1, herramienta, arco) ; p=(x_diam, z)
        self.prj = prj
        self.agarre = args.agarre
        self.margen = args.margen
        d = prj["diam"] if prj else None
        L = prj["largo"] if prj else None
        self.D, self.L = d, L
        if d is not None and L is not None:
            self.ztop = max(0.0, L - prj["g54z"])
            self.zbot = self.ztop - L
            self.zchuck = -(L - self.agarre)

    def err(self, n, msg):
        self.errores.append((n, msg))

    def warn(self, n, msg):
        self.avisos.append((n, msg))


def arco(p0, p1, R, cw):
    """Devuelve (centro_z, centro_r, radio) en plano (z, r) o None si la cuerda no cierra."""
    z0, r0 = p0[1], p0[0] / 2
    z1, r1 = p1[1], p1[0] / 2
    dz, dr = z1 - z0, r1 - r0
    c = math.hypot(dz, dr)
    if c < 1e-9 or c > 2 * abs(R) + 1e-6:
        return None
    h = math.sqrt(max(abs(R) ** 2 - (c / 2) ** 2, 0))
    # normal a la derecha del sentido de marcha (u=z a la derecha, v=r arriba)
    nz, nr = dr / c, -dz / c
    s = 1 if cw else -1
    if R < 0:
        s = -s  # arco mayor de 180 grados
    return ((z0 + z1) / 2 + s * h * nz, (r0 + r1) / 2 + s * h * nr, abs(R), cw)


def simular(lineas, sim, args):
    st = {"tool": None, "spin": False, "F": None, "mode": None,
          "pos": None, "cx": None, "cz": None}
    corte = {}  # evita repetir el mismo aviso por linea

    def mover(n, tipo, p1, R=None, cw=None):
        p0 = st["pos"]
        if p0 is None:
            st["pos"] = p1
            return
        arc = None
        if tipo == "F" and R is not None:
            arc = arco(p0, p1, R, cw)
        sim.segs.append((tipo, p0, p1, st["tool"], arc))
        if tipo == "F":
            revisar_corte(n, p0, p1)
        elif tipo == "R":
            if p1[0] < p0[0] - 1e-9 and p1[1] < 0 and (sim.D is None or p1[0] < sim.D):
                sim.warn(n, "G00 baja X con Z<0: posible rapido contra material")
        st["pos"] = p1

    def revisar_corte(n, p0, p1):
        if st["tool"] is None and "t" not in corte.setdefault(n, set()):
            corte[n].add("t")
            sim.err(n, "Movimiento de corte sin herramienta (T) activa")
        if not st["spin"] and "s" not in corte.setdefault(n, set()):
            corte[n].add("s")
            sim.err(n, "Movimiento de corte sin husillo en marcha (M3/M4)")
        if st["F"] is None and "f" not in corte.setdefault(n, set()):
            corte[n].add("f")
            sim.err(n, "Movimiento de avance sin F definido")
        for p in (p1,):
            x, z = p
            # hasta X-2: con compensación del radio de punta la punta teórica pasa un poco del eje
            if x < 0 and not (-2 <= x < 0):
                sim.err(n, "Avance con X=%g (negativo, pasa del eje)" % x)
            if sim.D is not None:
                if x > sim.D + sim.margen:
                    sim.err(n, "Avance con X=%g fuera del bruto (D=%g)" % (x, sim.D))
                if z > sim.ztop + sim.margen:
                    sim.err(n, "Avance con Z=%g fuera del bruto (cara en Z=%g)" % (z, sim.ztop))
                if z < sim.zchuck - 1e-9 and "c" not in corte.setdefault((n, z), set()):
                    corte[(n, z)].add("c")
                    sim.err(n, "Z=%g entra en la zona de plato (limite Z=%g, agarre %g)"
                            % (z, sim.zchuck, sim.agarre))

    for n, texto in lineas:
        t = re.sub(r"\(.*?\)", "", texto).strip()
        if not t or t == "%" or re.fullmatch(r"O\d+", t):
            continue
        palabras = []
        resto = t.upper()
        pos = 0
        for m in re.finditer(r"([A-Z])\s*([-+]?(?:\d+\.?\d*|\.\d+))", resto):
            palabras.append((m.group(1), float(m.group(2)), m.group(2)))
        limpio = re.sub(r"([A-Z])\s*([-+]?(?:\d+\.?\d*|\.\d+))", "", resto)
        if limpio.strip():
            sim.err(n, "Texto no reconocido: '%s'" % limpio.strip())
        v = {}
        gs = []
        for l, val, _ in palabras:
            if l == "G":
                if int(val) not in G_OK or val != int(val):
                    sim.err(n, "Palabra no soportada: G%g" % val)
                else:
                    gs.append(int(val))
            elif l == "M":
                if int(val) not in M_OK:
                    sim.err(n, "Palabra no soportada: M%g" % val)
                elif int(val) in (3, 4):
                    st["spin"] = True
                elif int(val) == 5:
                    st["spin"] = False
            elif l == "T":
                num = int(val)
                tt = num // 100 if num >= 100 else num
                st["tool"] = tt
                if sim.prj and (tt not in sim.prj["tools"] or tt == 0):
                    sim.err(n, "Herramienta T%d no existe en [TOOLS] del .prj" % tt)
            elif l == "F":
                st["F"] = val
            elif l in "XZR":
                v[l] = val
            elif l in "OS":
                pass
            else:
                sim.err(n, "Palabra no soportada: %s" % l + ("%g" % val))
        for g in gs:
            if g in (0, 1, 2, 3, 90, 94):
                st["mode"] = g
                if g in (90, 94):
                    st["cx"] = st["cz"] = None
        if not ("X" in v or "Z" in v):
            continue
        mode = st["mode"]
        if mode is None:
            sim.err(n, "Movimiento sin G00/G01/G02/G03/G90/G94 activo")
            continue
        p = st["pos"]
        x = v.get("X", p[0] if p else None)
        z = v.get("Z", p[1] if p else None)
        if x is None or z is None:
            if mode in (0, 1, 2, 3):
                st["pos"] = (x if x is not None else 0.0, z if z is not None else 0.0)
            continue
        if mode in (0, 1):
            mover(n, "R" if mode == 0 else "F", (x, z))
        elif mode in (2, 3):
            if "R" not in v:
                sim.err(n, "G0%d sin R" % mode)
                mover(n, "F", (x, z))
            else:
                p0 = st["pos"]
                if p0 is not None and arco(p0, (x, z), v["R"], mode == 2) is None:
                    c = math.hypot(z - p0[1], x / 2 - p0[0] / 2)
                    sim.err(n, "Arco G0%d: cuerda %.3f > 2*R (%.3f)" % (mode, c, 2 * v["R"]))
                mover(n, "F", (x, z), v["R"], mode == 2)
        else:
            if "X" in v:
                st["cx"] = v["X"]
            if "Z" in v:
                st["cz"] = v["Z"]
            if st["cx"] is None or st["cz"] is None:
                sim.err(n, "Ciclo G%d sin X y Z completos" % mode)
                continue
            if p is None:
                sim.err(n, "Ciclo G%d sin punto de partida" % mode)
                continue
            xs, zs = p
            cx, cz = st["cx"], st["cz"]
            if mode == 90:
                ruta = [("R", (cx, zs)), ("F", (cx, cz)), ("F", (xs, cz)), ("R", (xs, zs))]
            else:
                ruta = [("R", (xs, cz)), ("F", (cx, cz)), ("F", (cx, zs)), ("R", (xs, zs))]
            for tipo, q in ruta:
                mover(n, tipo, q)


def verificar_formato(raw, lineas, sim):
    texto = raw.decode("latin-1")
    sl = [(i + 1, l.rstrip("\r\n")) for i, l in enumerate(texto.splitlines(True))]
    for i, l in enumerate(texto.splitlines(True)):
        if l.endswith("\n") and not l.endswith("\r\n"):
            sim.err(i + 1, "Fin de linea LF (se necesita CRLF)")
            break
        if not l.endswith("\n") and i != len(texto.splitlines(True)) - 1:
            sim.err(i + 1, "Fin de linea CR solo (se necesita CRLF)")
            break
    for n, l in sl:
        if any(ord(c) > 127 for c in l):
            sim.err(n, "Caracter no ASCII")
    no_vacias = [(n, l.strip()) for n, l in sl if l.strip()]
    if not no_vacias:
        sim.err(1, "Archivo vacio")
        return sl
    if no_vacias[0][1] != "%":
        sim.err(no_vacias[0][0], "El archivo debe empezar con %")
    if no_vacias[-1][1] != "%":
        sim.err(no_vacias[-1][0], "El archivo debe terminar con %")
    if not any(re.fullmatch(r"O\d+", l) for _, l in no_vacias):
        sim.err(1, "Falta el numero de programa (O....)")
    if not any(re.search(r"\bM0*30\b", l) for _, l in no_vacias):
        sim.err(no_vacias[-1][0], "Falta M30")
    return sl


def limites(sim):
    zs, rs = [], []
    for tipo, p0, p1, _, _ in sim.segs:
        if tipo == "F":
            for p in (p0, p1):
                zs.append(p[1])
                rs.append(p[0] / 2)
    if sim.D is not None:
        zs += [sim.zbot, sim.ztop]
        rs += [0, sim.D / 2]
    if not zs:
        zs, rs = [-10, 10], [0, 10]
    return min(zs), max(zs), min(rs + [0]), max(rs)


def trazar_arco(seg, n=40):
    tipo, p0, p1, _, arc = seg
    cz, cr, R, cw = arc
    a0 = math.atan2(p0[0] / 2 - cr, p0[1] - cz)
    a1 = math.atan2(p1[0] / 2 - cr, p1[1] - cz)
    da = a1 - a0
    # sentido horario en el plano (z a la derecha, r arriba): angulo decrece
    if cw:
        while da > 0:
            da -= 2 * math.pi
    else:
        while da < 0:
            da += 2 * math.pi
    return [(cz + R * math.cos(a0 + da * k / n), cr + R * math.sin(a0 + da * k / n))
            for k in range(n + 1)]


def polilineas(sim):
    """Devuelve lista de (tipo, tool, puntos(z,r))."""
    out = []
    for seg in sim.segs:
        tipo, p0, p1, tool, arc = seg
        if arc is None:
            pts = [(p0[1], p0[0] / 2), (p1[1], p1[0] / 2)]
        else:
            pts = trazar_arco(seg)
        out.append((tipo, tool, pts))
    return out


def dibujar(sim, ruta, nombre):
    zmin, zmax, rmin, rmax = limites(sim)
    pad = 5
    x0, x1 = zmin - pad, zmax + pad
    y0, y1 = -2, rmax + pad
    lineas = polilineas(sim)
    herr = sorted({t for tipo, t, _ in lineas if tipo == "F" and t is not None})
    col = {t: COLORES[i % len(COLORES)] for i, t in enumerate(herr)}
    if plt is not None and not ruta.lower().endswith(".svg"):
        fig, ax = plt.subplots(figsize=(11, 6))
        if sim.D is not None:
            ax.add_patch(plt.Rectangle((sim.zbot, 0), sim.ztop - sim.zbot, sim.D / 2,
                                       fc="#dddddd", ec="#888888"))
            ax.add_patch(plt.Rectangle((sim.zbot, 0), sim.zchuck - sim.zbot, sim.D / 2,
                                       fc="none", ec="#444444", hatch="///"))
        for tipo, t, pts in lineas:
            zs, rs = zip(*pts)
            if tipo == "R":
                ax.plot(zs, rs, "--", color="red", lw=0.8)
            else:
                ax.plot(zs, rs, "-", color=col.get(t, "k"), lw=1.6)
        ax.plot([], [], "--", color="red", label="G00")
        for t in herr:
            ax.plot([], [], color=col[t], label="T%d" % t)
        ax.set_xlim(x0, x1)
        ax.set_ylim(y0, y1)
        ax.set_aspect("equal")
        ax.set_xlabel("Z (mm)")
        ax.set_ylabel("Radio = X/2 (mm)")
        ax.set_title(nombre)
        ax.legend(loc="upper left")
        fig.savefig(ruta, dpi=130, bbox_inches="tight")
        return ruta
    # SVG a mano
    if not ruta.lower().endswith(".svg"):
        ruta = os.path.splitext(ruta)[0] + ".svg"
    esc = 900.0 / (x1 - x0)
    W = 900
    H = int((y1 - y0) * esc) + 60

    def X(z):
        return (z - x0) * esc

    def Y(r):
        return H - 20 - (r - y0) * esc

    s = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'
         % (W, H, W, H),
         '<defs><pattern id="h" width="8" height="8" patternUnits="userSpaceOnUse" '
         'patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="8" stroke="#444" '
         'stroke-width="1.5"/></pattern><clipPath id="c"><rect x="0" y="0" width="%d" '
         'height="%d"/></clipPath></defs>' % (W, H),
         '<rect width="100%%" height="100%%" fill="white"/>',
         '<text x="10" y="18" font-family="sans-serif" font-size="14">%s</text>' % nombre]
    if sim.D is not None:
        s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#ddd" stroke="#888"/>'
                 % (X(sim.zbot), Y(sim.D / 2), (sim.ztop - sim.zbot) * esc, sim.D / 2 * esc))
        s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="url(#h)" stroke="#444"/>'
                 % (X(sim.zbot), Y(sim.D / 2), (sim.zchuck - sim.zbot) * esc, sim.D / 2 * esc))
    s.append('<line x1="0" y1="%.1f" x2="%d" y2="%.1f" stroke="#999" stroke-dasharray="10 3 2 3"/>'
             % (Y(0), W, Y(0)))
    s.append('<g clip-path="url(#c)" fill="none">')
    for tipo, t, pts in lineas:
        d = " ".join("%.1f,%.1f" % (X(z), Y(r)) for z, r in pts)
        if tipo == "R":
            s.append('<polyline points="%s" stroke="red" stroke-width="1" '
                     'stroke-dasharray="5 4"/>' % d)
        else:
            s.append('<polyline points="%s" stroke="%s" stroke-width="2"/>'
                     % (d, col.get(t, "#000")))
    s.append("</g>")
    ly = 40
    s.append('<line x1="10" y1="%d" x2="40" y2="%d" stroke="red" stroke-dasharray="5 4"/>'
             '<text x="46" y="%d" font-family="sans-serif" font-size="12">G00</text>'
             % (ly, ly, ly + 4))
    for t in herr:
        ly += 18
        s.append('<line x1="10" y1="%d" x2="40" y2="%d" stroke="%s" stroke-width="3"/>'
                 '<text x="46" y="%d" font-family="sans-serif" font-size="12">T%d</text>'
                 % (ly, ly, col[t], ly + 4, t))
    if sim.D is not None:
        ly += 18
        s.append('<rect x="10" y="%d" width="30" height="10" fill="url(#h)" stroke="#444"/>'
                 '<text x="46" y="%d" font-family="sans-serif" font-size="12">zona de plato</text>'
                 % (ly - 5, ly + 4))
    s.append("</svg>")
    with open(ruta, "w") as f:
        f.write("\n".join(s))
    return ruta


def main():
    ap = argparse.ArgumentParser(
        description="Verifica un programa .nc de torno (Fanuc 16i-TA, WinUnisoft) "
                    "y dibuja la trayectoria de las herramientas.")
    ap.add_argument("nc", help="archivo .nc a verificar")
    ap.add_argument("--prj", help="proyecto .prj (por defecto: mismo nombre que el .nc)")
    ap.add_argument("--agarre", type=float, default=30.0,
                    help="mm de bruto dentro del plato (por defecto 30)")
    ap.add_argument("--margen", type=float, default=10.0,
                    help="margen sobre el bruto en mm para avances en el aire (por defecto 10)")
    ap.add_argument("--dibujo", help="archivo de salida .png o .svg")
    a = ap.parse_args()

    prjruta = a.prj or os.path.splitext(a.nc)[0] + ".prj"
    prj = None
    if os.path.exists(prjruta):
        prj = leer_prj(prjruta)
        if prj["diam"] is None or prj["largo"] is None:
            prj = None
    with open(a.nc, "rb") as f:
        raw = f.read()
    sim = Sim(a, prj)
    sl = verificar_formato(raw, None, sim)
    simular(sl, sim, a)

    print("Archivo: %s" % a.nc)
    if prj:
        print("Proyecto: %s  bruto D%g x L%g, G54 Z=%g, plato desde Z=%g (agarre %g)"
              % (prjruta, sim.D, sim.L, prj["g54z"], sim.zchuck, a.agarre))
    else:
        print("Sin .prj: se omiten los controles de bruto, plato y herramientas.")
    for n, m in sorted(sim.errores, key=lambda e: e[0]):
        print("ERROR linea %d: %s" % (n, m))
    vistos = set()
    for n, m in sorted(sim.avisos, key=lambda e: e[0]):
        print("AVISO linea %d: %s" % (n, m))
    print("Resultado: %d errores, %d avisos" % (len(sim.errores), len(sim.avisos)))
    if a.dibujo:
        os.makedirs(os.path.dirname(os.path.abspath(a.dibujo)), exist_ok=True)
        print("Dibujo: %s" % dibujar(sim, a.dibujo, os.path.basename(a.nc)))
    return 1 if sim.errores else 0


if __name__ == "__main__":
    sys.exit(main())
