"""Modelo 3D con vista explotada de AutoLID montado en un inodoro de referencia.

Se corre con Blender en segundo plano (no hace falta abrirlo):

    blender -b --factory-startup --python herramientas/autolid_3d.py

Genera AutoLID/3D/autolid.blend, AutoLID/3D/autolid.glb y AutoLID/3D/visor/autolid.json
(el mismo modelo como glTF embebido, que es lo que carga el visor web).
Unidades: metros. Ejes de Blender: X a lo ancho del inodoro (derecha = +X),
Y hacia atrás (frente del inodoro = -Y), Z hacia arriba. El origen está en el
eje de la bisagra, bajo el centro del gabinete, para que el "Corte" del visor
muestre el interior de la caja.

Cada objeto es una pieza seleccionable con propiedades propias (exportadas como
"extras" del glTF): pid, nombre, conjunto y explode (desplazamiento [x, y, z] en
metros con el despiece al 100 %).

Medidas del INFORME FINAL (10/11/2026): gabinete IP65 150×150×100 mm, servo DS3218
(40×20×40,5 mm), 2 celdas 18650 (Ø18,4×65 mm), Arduino Nano (18×43 mm), HC-SR04
(45×20 mm), FSR 402 (Ø18 mm activo), adaptador de bisagra PETG para pasos de
38–43 mm, pletina de acero inoxidable, carcasa AISI 304. El inodoro es genérico.
"""
import bpy
import bmesh
import math
import os
from mathutils import Matrix, Vector

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(VAULT, 'AutoLID', '3D')
os.makedirs(os.path.join(OUT, 'visor'), exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'

MATS = {}


def mat(name, color, metal=0.0, rough=0.5, alpha=1.0):
    if name in MATS:
        return MATS[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    bsdf.inputs['Base Color'].default_value = (*color, 1.0)
    bsdf.inputs['Metallic'].default_value = metal
    bsdf.inputs['Roughness'].default_value = rough
    if alpha < 1.0:
        bsdf.inputs['Alpha'].default_value = alpha
        try:
            m.surface_render_method = 'BLENDED'
        except Exception:
            m.blend_method = 'BLEND'
    m.diffuse_color = (*color, alpha)
    MATS[name] = m
    return m


def srgb(h):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92 for v in c)


M = {
    'loza': mat('Loza', srgb('#eef0ee'), 0.0, 0.18),
    'agua': mat('Agua', srgb('#9fc6cf'), 0.0, 0.05),
    'inox': mat('Acero inoxidable AISI 304', srgb('#c3c9cd'), 1.0, 0.25),
    'inox_osc': mat('Acero inoxidable (bulones)', srgb('#8e969c'), 1.0, 0.35),
    'ip65': mat('Policarbonato gris IP65', srgb('#b9c0c3'), 0.0, 0.45),
    'ip65_tapa': mat('Policarbonato translúcido', srgb('#d6dee2'), 0.0, 0.15, alpha=0.55),
    'goma': mat('Goma EPDM', srgb('#222426'), 0.0, 0.85),
    'petg': mat('PETG impreso', srgb('#2f5d6b'), 0.0, 0.55),
    'servo': mat('Plástico negro servo', srgb('#1b1d20'), 0.0, 0.4),
    'aluminio': mat('Aluminio anodizado', srgb('#9aa3a8'), 0.9, 0.3),
    'pcb': mat('PCB verde', srgb('#1f6b3a'), 0.0, 0.45),
    'pcb_azul': mat('PCB azul', srgb('#1f4f9a'), 0.0, 0.45),
    'chip': mat('Circuito integrado', srgb('#141414'), 0.0, 0.35),
    'estano': mat('Pines y estaño', srgb('#c9c9c2'), 0.9, 0.3),
    'usb': mat('Conector metálico', srgb('#b5b8bb'), 0.95, 0.25),
    'bobina': mat('Inductor', srgb('#3a3a3a'), 0.3, 0.5),
    'pot': mat('Preset azul', srgb('#2f6fd0'), 0.0, 0.4),
    'celda': mat('Celda 18650', srgb('#2c7a7a'), 0.0, 0.35),
    'celda_tapa': mat('Polo de celda', srgb('#c0c4c6'), 0.95, 0.25),
    'portapila': mat('Portapila negro', srgb('#26282b'), 0.0, 0.55),
    'hcsr': mat('PCB HC-SR04', srgb('#1d5fa8'), 0.0, 0.45),
    'transductor': mat('Transductor', srgb('#c7cbcf'), 0.85, 0.3),
    'malla': mat('Malla del transductor', srgb('#2b2b2b'), 0.0, 0.8),
    'goretex': mat('Membrana Gore-Tex', srgb('#f2f2ee'), 0.0, 0.9, alpha=0.7),
    'fsr': mat('FSR 402', srgb('#c9a35a'), 0.0, 0.5),
    'fsr_cola': mat('Cola del FSR', srgb('#d8b56d'), 0.0, 0.5),
    'cable': mat('Cable', srgb('#2c3e50'), 0.0, 0.6),
    'blanco': mat('Conector blanco', srgb('#efefe8'), 0.0, 0.5),
    'led': mat('LED', srgb('#3ec3d8'), 0.0, 0.3),
}




class Part:
    """Junta primitivas en un solo bmesh, con un material por primitiva."""

    def __init__(self):
        self.bm = bmesh.new()
        self.mats = []

    def _mi(self, m):
        if m not in self.mats:
            self.mats.append(m)
        return self.mats.index(m)

    def _tag(self, faces, m):
        i = self._mi(m)
        for f in faces:
            f.material_index = i

    def _new(self, fn):
        before = set(self.bm.faces)
        fn()
        return [f for f in self.bm.faces if f not in before]

    def box(self, x0, x1, y0, y1, z0, z1, m):
        c = Vector(((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
        s = Matrix.Diagonal((abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), 1))
        mtx = Matrix.Translation(c) @ s
        self._tag(self._new(lambda: bmesh.ops.create_cube(self.bm, size=1.0, matrix=mtx)), m)
        return self

    def obox(self, center, size, rot, m):
        """Caja orientada: rot es una Matrix 3x3."""
        mtx = Matrix.Translation(Vector(center)) @ rot.to_4x4() @ Matrix.Diagonal((*size, 1))
        self._tag(self._new(lambda: bmesh.ops.create_cube(self.bm, size=1.0, matrix=mtx)), m)
        return self

    @staticmethod
    def _axis(axis):
        if axis == 'X':
            return Matrix.Rotation(math.radians(90), 4, 'Y')
        if axis == 'Y':
            return Matrix.Rotation(math.radians(-90), 4, 'X')
        return Matrix.Identity(4)

    def cyl(self, axis, center, r, length, m, r2=None, segs=32):
        mtx = Matrix.Translation(Vector(center)) @ self._axis(axis)
        self._tag(self._new(lambda: bmesh.ops.create_cone(
            self.bm, cap_ends=True, cap_tris=False, segments=segs,
            radius1=r, radius2=r if r2 is None else r2, depth=length, matrix=mtx)), m)
        return self

    def profile(self, axis, center, pts, length, m):
        """Extruye un perfil 2D cerrado (u, v) a lo largo del eje."""
        def build():
            mtx = Matrix.Translation(Vector(center)) @ self._axis(axis)
            vb = [self.bm.verts.new(mtx @ Vector((u, v, -length / 2))) for u, v in pts]
            vt = [self.bm.verts.new(mtx @ Vector((u, v, length / 2))) for u, v in pts]
            n = len(pts)
            self.bm.faces.new(list(reversed(vb)))
            self.bm.faces.new(vt)
            for i in range(n):
                j = (i + 1) % n
                self.bm.faces.new((vb[i], vb[j], vt[j], vt[i]))
        self._tag(self._new(build), m)
        return self

    def tube(self, axis, center, r_in, r_out, length, m, a0=0.0, a1=360.0, segs=48):
        """Anillo o sector de anillo (a0..a1 en grados, en el plano del eje)."""
        full = (a1 - a0) >= 360
        n = segs if full else max(4, int(segs * (a1 - a0) / 360) + 1)
        angs = [math.radians(a0 + (a1 - a0) * i / (n if full else n - 1)) for i in range(n)]
        outer = [(r_out * math.cos(a), r_out * math.sin(a)) for a in angs]
        inner = [(r_in * math.cos(a), r_in * math.sin(a)) for a in angs]

        def build():
            mtx = Matrix.Translation(Vector(center)) @ self._axis(axis)
            h = length / 2
            ob = [self.bm.verts.new(mtx @ Vector((u, v, -h))) for u, v in outer]
            ot = [self.bm.verts.new(mtx @ Vector((u, v, h))) for u, v in outer]
            ib = [self.bm.verts.new(mtx @ Vector((u, v, -h))) for u, v in inner]
            it = [self.bm.verts.new(mtx @ Vector((u, v, h))) for u, v in inner]
            rng = range(n) if full else range(n - 1)
            for i in rng:
                j = (i + 1) % n
                self.bm.faces.new((ob[i], ob[j], ot[j], ot[i]))
                self.bm.faces.new((it[i], it[j], ib[j], ib[i]))
                self.bm.faces.new((ot[i], ot[j], it[j], it[i]))
                self.bm.faces.new((ib[i], ib[j], ob[j], ob[i]))
            if not full:
                self.bm.faces.new((ob[0], ot[0], it[0], ib[0]))
                self.bm.faces.new((ib[-1], it[-1], ot[-1], ob[-1]))
        self._tag(self._new(build), m)
        return self

    def gear(self, axis, center, r, teeth, width, m, bore=0.0):
        ht = min(0.006, r * 0.12)
        pts = []
        for i in range(teeth):
            a = 2 * math.pi * i / teeth
            s = 2 * math.pi / teeth
            for k, rr in ((0.0, r - ht), (0.18, r), (0.5, r), (0.68, r - ht)):
                pts.append((rr * math.cos(a + k * s), rr * math.sin(a + k * s)))
        self.profile(axis, center, pts, width, m)
        return self

    def torus(self, axis, center, R, r, m, segs=48, rsegs=12):
        def build():
            mtx = Matrix.Translation(Vector(center)) @ self._axis(axis)
            rings = []
            for i in range(segs):
                a = 2 * math.pi * i / segs
                ring = []
                for j in range(rsegs):
                    b = 2 * math.pi * j / rsegs
                    p = Vector(((R + r * math.cos(b)) * math.cos(a),
                                (R + r * math.cos(b)) * math.sin(a), r * math.sin(b)))
                    ring.append(self.bm.verts.new(mtx @ p))
                rings.append(ring)
            for i in range(segs):
                for j in range(rsegs):
                    a, b = rings[i], rings[(i + 1) % segs]
                    self.bm.faces.new((a[j], b[j], b[(j + 1) % rsegs], a[(j + 1) % rsegs]))
        self._tag(self._new(build), m)
        return self

    def handwheel(self, axis, center, R, m_rim, m_hub, spokes=3, handle=True, sign=-1):
        """Volante: aro, cubo, rayos y manija. sign = hacia dónde mira la manija."""
        self.torus(axis, center, R, R * 0.09, m_rim)
        self.cyl(axis, center, R * 0.22, R * 0.35, m_hub)
        rot = self._axis(axis).to_3x3()
        for k in range(spokes):
            a = 2 * math.pi * k / spokes + math.pi / 2
            mid = Vector((R * 0.55 * math.cos(a), R * 0.55 * math.sin(a), 0))
            rs = Matrix.Rotation(a, 3, 'Z')
            self.obox(Vector(center) + rot @ mid, (R * 0.9, R * 0.1, R * 0.06), rot @ rs, m_rim)
        if handle:
            a = math.pi / 2 + math.pi / spokes
            p = Vector((R * 0.92 * math.cos(a), R * 0.92 * math.sin(a), sign * R * 0.35))
            n = rot @ Vector((0, 0, 1))
            c = Vector(center) + rot @ p
            ax = 'X' if abs(n.x) > 0.5 else ('Y' if abs(n.y) > 0.5 else 'Z')
            self.cyl(ax, c, R * 0.1, R * 0.55, M['negro'])
        return self

    def curve(self, pts, radius, m, segs=10):
        """Tubo que sigue una polilínea suavizada (mangueras, brazos)."""
        cu = bpy.data.curves.new('tmp', 'CURVE')
        cu.dimensions = '3D'
        sp = cu.splines.new('BEZIER')
        sp.bezier_points.add(len(pts) - 1)
        for bp, p in zip(sp.bezier_points, pts):
            bp.co = p
            bp.handle_left_type = bp.handle_right_type = 'AUTO'
        cu.bevel_depth = radius
        cu.bevel_resolution = 3
        cu.use_fill_caps = True
        cu.resolution_u = segs
        ob = bpy.data.objects.new('tmp', cu)
        scene.collection.objects.link(ob)
        dg = bpy.context.evaluated_depsgraph_get()
        me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
        n0 = len(self.bm.faces)
        self.bm.from_mesh(me)
        self.bm.faces.ensure_lookup_table()
        self._tag(self.bm.faces[n0:], m)
        bpy.data.objects.remove(ob)
        bpy.data.curves.remove(cu)
        bpy.data.meshes.remove(me)
        return self

    def loop(self, axis_x, c1, r1, c2, r2, thick, width, m, n=40):
        """Correa en V: envolvente de dos poleas en el plano YZ, a la altura x."""
        pts = []
        for (cy, cz), r in ((c1, r1 + thick / 2), (c2, r2 + thick / 2)):
            for i in range(n):
                a = 2 * math.pi * i / n
                pts.append((cy + r * math.cos(a), cz + r * math.sin(a)))
        pts = sorted(set(pts))

        def cross(o, a, b):
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
        lo, hi = [], []
        for p in pts:
            while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
                lo.pop()
            lo.append(p)
        for p in reversed(pts):
            while len(hi) >= 2 and cross(hi[-2], hi[-1], p) <= 0:
                hi.pop()
            hi.append(p)
        hull = lo[:-1] + hi[:-1]
        # offset hacia afuera y hacia adentro para darle espesor
        cy = sum(p[0] for p in hull) / len(hull)
        cz = sum(p[1] for p in hull) / len(hull)

        def build():
            h = width / 2
            vo, vi = [], []
            for (y, z) in hull:
                d = Vector((0, y - cy, z - cz))
                # normal aproximada: hacia afuera desde el centro de la polea más cercana
                cc = min((c1, c2), key=lambda c: (c[0] - y) ** 2 + (c[1] - z) ** 2)
                nrm = Vector((0, y - cc[0], z - cc[1])).normalized()
                vo.append((Vector((0, y, z)), nrm))
            outer_b = [self.bm.verts.new((axis_x - h, p.y + nn.y * thick / 2, p.z + nn.z * thick / 2)) for p, nn in vo]
            outer_t = [self.bm.verts.new((axis_x + h, p.y + nn.y * thick / 2, p.z + nn.z * thick / 2)) for p, nn in vo]
            inner_b = [self.bm.verts.new((axis_x - h, p.y - nn.y * thick / 2, p.z - nn.z * thick / 2)) for p, nn in vo]
            inner_t = [self.bm.verts.new((axis_x + h, p.y - nn.y * thick / 2, p.z - nn.z * thick / 2)) for p, nn in vo]
            k = len(vo)
            for i in range(k):
                j = (i + 1) % k
                self.bm.faces.new((outer_b[i], outer_b[j], outer_t[j], outer_t[i]))
                self.bm.faces.new((inner_t[i], inner_t[j], inner_b[j], inner_b[i]))
                self.bm.faces.new((outer_t[i], outer_t[j], inner_t[j], inner_t[i]))
                self.bm.faces.new((inner_b[i], inner_b[j], outer_b[j], outer_b[i]))
        self._tag(self._new(build), m)
        return self


COLL = {}


def make(pid, nombre, conjunto, part, explode, bevel=0.0, smooth=True):
    me = bpy.data.meshes.new(pid)
    bmesh.ops.remove_doubles(part.bm, verts=part.bm.verts, dist=1e-6)
    bmesh.ops.recalc_face_normals(part.bm, faces=part.bm.faces)
    part.bm.to_mesh(me)
    part.bm.free()
    for m in part.mats:
        me.materials.append(m)
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    ob = bpy.data.objects.new(pid, me)
    if conjunto not in COLL:
        c = bpy.data.collections.new(conjunto)
        scene.collection.children.link(c)
        COLL[conjunto] = c
    COLL[conjunto].objects.link(ob)
    ob['pid'] = pid
    ob['nombre'] = nombre
    ob['conjunto'] = conjunto
    ob['explode'] = [round(v, 4) for v in explode]
    if smooth:
        mod = ob.modifiers.new('suave', 'EDGE_SPLIT')
        mod.split_angle = math.radians(35)
    if bevel:
        b = ob.modifiers.new('bisel', 'BEVEL')
        b.width = bevel
        b.segments = 2
        b.limit_method = 'ANGLE'
        b.angle_limit = math.radians(40)
        ob.modifiers.move(len(ob.modifiers) - 1, 0)
    return ob


P = Part


# ---------------------------------------------------------------- formas propias
def loft(part, loops, m, cap_bottom=True, cap_top=False):
    """Une anillos de puntos (mismo largo) con caras; tapa abajo y/o arriba."""
    def build():
        vs = [[part.bm.verts.new(Vector(p)) for p in loop] for loop in loops]
        n = len(loops[0])
        for a, b in zip(vs, vs[1:]):
            for i in range(n):
                j = (i + 1) % n
                part.bm.faces.new((a[i], a[j], b[j], b[i]))
        if cap_bottom:
            part.bm.faces.new(list(reversed(vs[0])))
        if cap_top:
            part.bm.faces.new(vs[-1])
    part._tag(part._new(build), m)
    return part


def oval(cx, cy, z, rx, ry, n=56, a0=0.0):
    return [(cx + rx * math.cos(a0 + 2 * math.pi * i / n), cy + ry * math.sin(a0 + 2 * math.pi * i / n), z) for i in range(n)]


def oval_torus(part, cx, cy, cz, Rx, Ry, r, m, segs=56, rsegs=12, flat=1.0):
    def build():
        rings = []
        for i in range(segs):
            a = 2 * math.pi * i / segs
            ca, sa = math.cos(a), math.sin(a)
            # normal aproximada de la elipse en ese punto
            nx, ny = ca / Rx, sa / Ry
            ln = math.hypot(nx, ny)
            nx, ny = nx / ln, ny / ln
            ring = []
            for j in range(rsegs):
                b = 2 * math.pi * j / rsegs
                ring.append(part.bm.verts.new(Vector((cx + Rx * ca + r * math.cos(b) * nx,
                                                      cy + Ry * sa + r * math.cos(b) * ny,
                                                      cz + r * flat * math.sin(b)))))
            rings.append(ring)
        for i in range(segs):
            a, b = rings[i], rings[(i + 1) % segs]
            for j in range(rsegs):
                k = (j + 1) % rsegs
                part.bm.faces.new((a[j], b[j], b[k], a[k]))
    part._tag(part._new(build), m)
    return part


def bar(part, p0, p1, width, thick, m):
    """Planchuela recta de p0 a p1 (ancho horizontal, espesor vertical)."""
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    rot = d.to_track_quat('X', 'Z').to_matrix()
    return part.obox((p0 + p1) / 2, (d.length, width, thick), rot, m)


# ---------------------------------------------------------------- medidas generales
BY = -0.25          # centro de la taza (el frente del inodoro es -Y)
RIM = 0.40          # borde superior de la taza
HZ = 0.44           # eje de la bisagra y del servo
# gabinete IP65 150 × 150 × 100 mm, a la derecha de la bisagra
GX0, GX1, GY0, GY1, GZ0, GZ1 = 0.215, 0.365, -0.075, 0.075, 0.405, 0.505
W = 0.003           # espesor de pared
B = (0.13, 0.0, 0.0)  # el gabinete completo se corre a la derecha en el despiece


def ex(*extra):
    return tuple(b + e for b, e in zip(B, extra))


# ================================================================ INODORO (referencia)
CJ = 'Inodoro (referencia)'
taza = P()
loft(taza, [oval(0, BY, 0.0, 0.12, 0.16), oval(0, BY, 0.20, 0.155, 0.205), oval(0, BY, RIM, 0.19, 0.255),
            oval(0, BY + 0.01, RIM, 0.15, 0.205), oval(0, BY + 0.03, 0.30, 0.11, 0.15), oval(0, BY + 0.05, 0.20, 0.06, 0.08)],
     M['loza'], cap_bottom=True, cap_top=True)
taza.box(-0.17, 0.17, -0.03, 0.10, 0.34, RIM, M['loza'])          # repisa trasera
loft(taza, [oval(0, BY + 0.04, 0.255, 0.085, 0.115)], M['agua'], cap_bottom=False, cap_top=True)
make('taza', 'Taza del inodoro', CJ, taza, (0, 0, 0), bevel=0.004)

moch = P().box(-0.20, 0.20, 0.10, 0.27, RIM, 0.78, M['loza'])
moch.box(-0.212, 0.212, 0.09, 0.28, 0.78, 0.805, M['loza'])
moch.cyl('Z', (0, 0.185, 0.81), 0.022, 0.012, M['inox'])
make('mochila', 'Mochila', CJ, moch, (0, 0, 0), bevel=0.012)

asiento = oval_torus(P(), 0, BY, 0.418, 0.17, 0.225, 0.017, M['loza'], flat=0.95)
for sx in (-0.08, 0.08):
    asiento.cyl('X', (sx, 0.0, HZ), 0.011, 0.034, M['loza'])
make('asiento', 'Asiento', CJ, asiento, (0, 0, 0.14))

tapa = P()
loft(tapa, [oval(0, BY, 0.437, 0.205, 0.262), oval(0, BY, 0.452, 0.203, 0.26), oval(0, BY, 0.459, 0.19, 0.245)],
     M['loza'], cap_bottom=True, cap_top=True)
make('tapa', 'Tapa del inodoro', CJ, tapa, (0, 0, 0.26))

# ================================================================ MONTAJE
CJ = 'Montaje y transmisión'
ad = P().box(0.045, GX1, -0.03, 0.03, 0.397, GZ0, M['petg'])        # base que recibe la caja
ad.cyl('Z', (0.08, 0.0, 0.401), 0.0205, 0.008, M['petg'])           # collar Ø41 (pasos de 38 a 43 mm)
ad.cyl('Z', (0.08, 0.0, 0.365), 0.007, 0.07, M['petg'])             # tetón que entra en el agujero de la bisagra
ad.box(0.245, 0.335, -0.07, -0.03, 0.397, GZ0, M['petg'])           # alas que apoyan la caja
ad.box(0.245, 0.335, 0.03, 0.07, 0.397, GZ0, M['petg'])
make('adaptador_petg', 'Adaptador de bisagra (PETG)', CJ, ad, (0, 0, 0), bevel=0.0015)

horn = P().cyl('X', (0.2035, 0.0, HZ), 0.012, 0.004, M['aluminio'])
horn.box(0.2015, 0.2055, -0.004, 0.004, HZ, HZ + 0.03, M['aluminio'])
make('brazo_servo', 'Brazo del servo (horn)', CJ, horn, (-0.03, 0, 0.03))

ple = bar(P(), (0.199, -0.002, HZ + 0.026), (0.17, -0.135, 0.463), 0.016, 0.003, M['inox'])
ple.box(0.15, 0.19, -0.15, -0.12, 0.459, 0.466, M['inox'])        # clip sobre la tapa
make('pletina', 'Pletina de distribución (inox)', CJ, ple, (-0.04, -0.05, 0.36))

# ================================================================ GABINETE
CJ = 'Gabinete y carcasa'
caja = P().box(GX0, GX1, GY0, GY1, GZ0, GZ0 + W, M['ip65'])
caja.box(GX0, GX0 + W, GY0, GY1, GZ0, GZ1, M['ip65']).box(GX1 - W, GX1, GY0, GY1, GZ0, GZ1, M['ip65'])
caja.box(GX0, GX1, GY0, GY0 + W, GZ0, GZ1, M['ip65']).box(GX0, GX1, GY1 - W, GY1, GZ0, GZ1, M['ip65'])
for sx in (GX0 + 0.009, GX1 - 0.009):
    for sy in (GY0 + 0.009, GY1 - 0.009):
        caja.cyl('Z', (sx, sy, (GZ0 + GZ1) / 2), 0.005, GZ1 - GZ0, M['ip65'])   # torretas para los tornillos
caja.cyl('X', (GX0 - 0.001, 0.0, HZ), 0.006, 0.004, M['goma'])                 # retén del eje del servo
make('caja_ip65', 'Gabinete estanco IP65', CJ, caja, B, bevel=0.0008, smooth=False)

junta = P()
i = 0.0015
junta.box(GX0 + i, GX1 - i, GY0 + i, GY0 + i + 0.003, GZ1, GZ1 + 0.003, M['goma'])
junta.box(GX0 + i, GX1 - i, GY1 - i - 0.003, GY1 - i, GZ1, GZ1 + 0.003, M['goma'])
junta.box(GX0 + i, GX0 + i + 0.003, GY0 + i, GY1 - i, GZ1, GZ1 + 0.003, M['goma'])
junta.box(GX1 - i - 0.003, GX1 - i, GY0 + i, GY1 - i, GZ1, GZ1 + 0.003, M['goma'])
make('junta', 'Junta elastomérica', CJ, junta, ex(0, 0, 0.30), smooth=False)

tapa_ip = P().box(GX0 - 0.001, GX1 + 0.001, GY0 - 0.001, GY1 + 0.001, GZ1 + 0.003, GZ1 + 0.011, M['ip65_tapa'])
make('tapa_ip65', 'Tapa del gabinete', CJ, tapa_ip, ex(0, 0, 0.34), bevel=0.001, smooth=False)

bul = P()
for sx in (GX0 + 0.009, GX1 - 0.009):
    for sy in (GY0 + 0.009, GY1 - 0.009):
        bul.cyl('Z', (sx, sy, GZ1 + 0.0125), 0.0028, 0.003, M['inox_osc'])
        bul.cyl('Z', (sx, sy, GZ1 - 0.005), 0.0015, 0.03, M['inox_osc'])
make('bulones', 'Tornillos M3 inox', CJ, bul, ex(0, 0, 0.40))

car = P()
CX0, CX1, CY0, CY1, CZ1 = GX0 - 0.006, GX1 + 0.006, GY0 - 0.006, GY1 + 0.006, GZ1 + 0.019
car.box(CX0, CX1, CY0, CY1, CZ1 - 0.0015, CZ1, M['inox'])
car.box(CX0, CX0 + 0.0015, CY0, CY1, GZ0 - 0.003, CZ1, M['inox']).box(CX1 - 0.0015, CX1, CY0, CY1, GZ0 - 0.003, CZ1, M['inox'])
car.box(CX0, CX1, CY0, CY0 + 0.0015, GZ0 - 0.003, CZ1, M['inox']).box(CX0, CX1, CY1 - 0.0015, CY1, GZ0 - 0.003, CZ1, M['inox'])
car.cyl('Z', (CX1 - 0.02, CY0 + 0.02, CZ1 + 0.0006), 0.003, 0.001, M['led'])   # testigo LED
make('carcasa_inox', 'Carcasa de acero inoxidable', CJ, car, ex(0, 0, 0.48), bevel=0.0012, smooth=False)

pren = P().cyl('Y', (0.335, GY0 - 0.009, 0.445), 0.0075, 0.012, M['servo'])
pren.cyl('Y', (0.335, GY0 - 0.004, 0.445), 0.009, 0.004, M['servo'], segs=6)
make('prensacables', 'Prensacables estanco', CJ, pren, ex(0, -0.07, 0))

# ================================================================ ACTUADOR
CJ = 'Actuador'
sv = P().box(0.222, 0.2625, -0.02, 0.02, HZ - 0.01, HZ + 0.01, M['servo'])
sv.box(0.236, 0.2385, -0.027, 0.027, HZ - 0.01, HZ + 0.01, M['servo'])       # orejas de montaje
sv.cyl('X', (0.219, 0.0, HZ), 0.0065, 0.006, M['servo'])                     # cuello del eje
sv.cyl('X', (GX0 - 0.006, 0.0, HZ), 0.0029, 0.022, M['aluminio'])            # eje estriado (25T)
sv.box(0.245, 0.26, -0.0201, -0.0199, HZ - 0.006, HZ + 0.006, M['estano'])  # etiqueta
make('servo_ds3218', 'Servomotor DS3218', CJ, sv, ex(0, 0, 0.12), bevel=0.0012)

# ================================================================ ELECTRÓNICA
CJ = 'Electrónica'
PZ = 0.458
pcb = P().box(0.272, 0.358, -0.065, 0.065, PZ, PZ + 0.0016, M['pcb'])
for sx in (0.276, 0.354):
    for sy in (-0.061, 0.061):
        pcb.cyl('Z', (sx, sy, (GZ0 + W + PZ) / 2), 0.0025, PZ - GZ0 - W, M['blanco'])   # separadores
for k, sy in enumerate((-0.05, -0.02, 0.02, 0.05)):
    pcb.box(0.348, 0.356, sy - 0.004, sy + 0.004, PZ + 0.0016, PZ + 0.0076, M['blanco'])  # conectores JST
make('pcb', 'Placa PCB doble faz', CJ, pcb, ex(0, 0, 0.20), smooth=False)

nano = P().box(0.290, 0.308, -0.0215, 0.0215, PZ + 0.0046, PZ + 0.0062, M['pcb_azul'])
for sx in (0.2915, 0.3065):
    nano.box(sx - 0.0012, sx + 0.0012, -0.019, 0.019, PZ + 0.0016, PZ + 0.0046, M['chip'])   # tiras de pines
nano.obox((0.299, -0.002, PZ + 0.0068), (0.007, 0.007, 0.0012), Matrix.Rotation(math.radians(45), 3, 'Z'), M['chip'])
nano.box(0.295, 0.303, 0.0155, 0.0235, PZ + 0.0062, PZ + 0.0102, M['usb'])   # mini USB
nano.box(0.3005, 0.3035, -0.014, -0.010, PZ + 0.0062, PZ + 0.0072, M['led'])
make('arduino_nano', 'Arduino Nano V3', CJ, nano, ex(0, 0, 0.25), smooth=False)

tp = P().box(0.314, 0.331, -0.060, -0.034, PZ + 0.0046, PZ + 0.0058, M['pcb_azul'])
tp.box(0.3175, 0.3275, -0.0625, -0.0555, PZ + 0.0058, PZ + 0.0090, M['usb'])  # USB-C
tp.box(0.319, 0.325, -0.048, -0.042, PZ + 0.0058, PZ + 0.0072, M['chip'])
tp.box(0.3155, 0.3165, -0.059, -0.035, PZ + 0.0016, PZ + 0.0046, M['estano'])
make('tp4056', 'Cargador TP4056 (USB-C)', CJ, tp, ex(0, -0.04, 0.25), smooth=False)

mt = P().box(0.314, 0.331, 0.022, 0.059, PZ + 0.0046, PZ + 0.0058, M['pcb_azul'])
mt.box(0.3185, 0.3265, 0.030, 0.038, PZ + 0.0058, PZ + 0.0098, M['bobina'])    # inductor
mt.box(0.319, 0.326, 0.045, 0.054, PZ + 0.0058, PZ + 0.0128, M['pot'])         # preset de ajuste
mt.cyl('Z', (0.3225, 0.0495, PZ + 0.0135), 0.0017, 0.0015, M['estano'])
mt.box(0.3155, 0.3165, 0.023, 0.058, PZ + 0.0016, PZ + 0.0046, M['estano'])
make('mt3608', 'Elevador MT3608 (5 V)', CJ, mt, ex(0, 0.04, 0.25), smooth=False)

cab = P()
cab.curve([(0.335, GY0 - 0.015, 0.445), (0.34, -0.12, 0.43), (0.33, -0.22, 0.40), (0.23, -0.40, 0.36),
           (0.10, -0.47, 0.32), (0.012, -0.484, 0.30)], 0.0022, M['cable'])
cab.curve([(0.330, GY0 - 0.015, 0.441), (0.29, -0.10, 0.405), (0.15, -0.30, 0.402), (-0.06, -0.43, 0.4012),
           (-0.12, -0.425, 0.4008)], 0.0014, M['cable'])
make('cableado', 'Cableado a los sensores', CJ, cab, (0, 0, 0))

# ================================================================ ENERGÍA
CJ = 'Energía'
pp = P().box(0.283, 0.334, -0.036, 0.036, GZ0 + W, GZ0 + W + 0.003, M['portapila'])
for sy in (-0.036, 0.0335):
    pp.box(0.283, 0.334, sy, sy + 0.0025, GZ0 + W, 0.432, M['portapila'])
for sx in (0.297, 0.320):
    for sy in (-0.033, 0.0325):
        pp.cyl('Y', (sx, sy, 0.4205), 0.004, 0.0015, M['celda_tapa'])        # contactos
make('portapilas', 'Portapilas 1S2P', CJ, pp, ex(0, 0, 0.10), smooth=False)

cel = P()
for sx in (0.297, 0.320):
    cel.cyl('Y', (sx, 0.0, 0.4205), 0.0092, 0.063, M['celda'])
    cel.cyl('Y', (sx, -0.0322, 0.4205), 0.0085, 0.0014, M['celda_tapa'])
    cel.cyl('Y', (sx, 0.0322, 0.4205), 0.0035, 0.0018, M['celda_tapa'])
make('celdas_18650', 'Celdas Li-Ion 18650 (×2)', CJ, cel, ex(0, 0, 0.15))

# ================================================================ SENSORES
CJ = 'Sensores'
SY = -0.4835
hc = P().box(-0.0225, 0.0225, SY, SY + 0.0016, 0.29, 0.31, M['hcsr'])
for sx in (-0.0135, 0.0135):
    hc.cyl('Y', (sx, SY - 0.006, 0.30), 0.008, 0.012, M['transductor'])
    hc.cyl('Y', (sx, SY - 0.0121, 0.30), 0.0068, 0.0004, M['malla'])
hc.box(-0.004, 0.004, SY + 0.0016, SY + 0.0036, 0.296, 0.304, M['usb'])   # cristal
hc.box(-0.01, 0.01, SY + 0.0016, SY + 0.004, 0.306, 0.309, M['petg'])     # soporte PETG
for k in range(4):
    hc.box(-0.0045 + 0.003 * k - 0.0005, -0.0045 + 0.003 * k + 0.0005, SY + 0.0016, SY + 0.004, 0.287, 0.29, M['estano'])
make('hc_sr04', 'Sensor ultrasónico HC-SR04', CJ, hc, (0, -0.09, 0), smooth=False)

mem = P().box(-0.025, 0.025, SY - 0.0135, SY - 0.0125, 0.287, 0.313, M['goretex'])
make('membrana', 'Membrana hidrofóbica (Gore-Tex)', CJ, mem, (0, -0.16, 0), smooth=False)

FX, FY = -0.12, -0.41
fsr = P().cyl('Z', (FX, FY, RIM + 0.0007), 0.0095, 0.0004, M['fsr'])
fsr.box(FX + 0.006, FX + 0.012, FY - 0.003, FY + 0.003, RIM + 0.0005, RIM + 0.0009, M['fsr_cola'])
fsr.curve([(FX + 0.012, FY, RIM + 0.0008), (FX + 0.03, FY - 0.005, RIM + 0.0008), (FX + 0.04, FY - 0.012, RIM + 0.0006)],
          0.0006, M['fsr_cola'])
make('fsr402', 'Sensor de fuerza FSR 402', CJ, fsr, (0, 0, 0.045), smooth=False)

gom = P().cyl('Z', (FX, FY, RIM + 0.0011 + 0.001), 0.012, 0.002, M['goma'])
make('goma_fsr', 'Goma de 2 mm (reparto de carga)', CJ, gom, (0, 0, 0.09))

# ---------------------------------------------------------------- guardar y exportar
for ob in scene.objects:
    ob.select_set(True)

blend = os.path.join(OUT, 'autolid.blend')
glb = os.path.join(OUT, 'autolid.glb')
gltf_json = os.path.join(OUT, 'visor', 'autolid.json')
bpy.ops.wm.save_as_mainfile(filepath=blend)
bpy.ops.export_scene.gltf(filepath=glb, export_format='GLB', export_apply=True,
                          export_extras=True, export_yup=True, export_materials='EXPORT',
                          use_selection=False)

n = sum(1 for o in scene.objects if o.type == 'MESH')
tris = 0
dg = bpy.context.evaluated_depsgraph_get()
for o in scene.objects:
    if o.type == 'MESH':
        me = o.evaluated_get(dg).to_mesh()
        me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        o.evaluated_get(dg).to_mesh_clear()
# copia del modelo como glTF con el binario embebido y extensión .json:
# las páginas publicadas como Artifact no sirven archivos .glb
import json, struct, base64
raw = open(glb, 'rb').read()
jlen, = struct.unpack_from('<I', raw, 12)
doc = json.loads(raw[20:20 + jlen])
blen, = struct.unpack_from('<I', raw, 20 + jlen)
binc = raw[28 + jlen:28 + jlen + blen]
doc['buffers'][0]['uri'] = 'data:application/octet-stream;base64,' + base64.b64encode(binc).decode()
with open(gltf_json, 'w') as fh:
    json.dump(doc, fh, separators=(',', ':'))

print(f'OK piezas={n} triangulos={tris} glb={os.path.getsize(glb) / 1e6:.2f} MB')
for c, coll in COLL.items():
    print(' ', c, ':', ', '.join(o.name for o in coll.objects))
