"""Modelo 3D por conjuntos del torno Femar TM300 (plataforma C0632A).

Se corre con Blender en segundo plano (no hace falta abrirlo):

    blender -b --factory-startup --python herramientas/torno_tm300_3d.py

Genera 3D/torno_tm300.blend, 3D/torno_tm300.glb y 3D/visor/torno_tm300.json
(el mismo modelo como glTF embebido, que es lo que carga el visor web).
Unidades: metros. Ejes de Blender: X a lo largo de la bancada (cabezal a la
izquierda), Y hacia atrás (frente del torno = -Y), Z hacia arriba.

Cada objeto es una pieza seleccionable. Lleva como propiedades propias
(exportadas como "extras" del glTF):
  - pid: identificador que usa el visor para buscar su ficha
  - conjunto: conjunto al que pertenece
  - explode: desplazamiento [x, y, z] en metros cuando el despiece está al 100 %

Medidas tomadas del manual C0632A (cap. 2): altura de centros 166 mm, ancho de
guías 187 mm, altura de bancada 290 mm, distancia entre puntas 1000 mm,
tornillo patrón Ø22, barra de avances Ø19, caña del contrapunto Ø32, plato
Ø200 (K11-200), recorridos de carros 160/95 mm. Lo que el manual no da
(gabinetes, cabezal, delantal) son proporciones de un torno 12x36 genérico.
"""
import bpy
import bmesh
import math
import os
from mathutils import Matrix, Vector

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(VAULT, '3D')
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- medidas
TRAY_Z = 0.65            # cara superior de la bandeja de virutas
BT = TRAY_Z + 0.29       # cara superior de las guías (altura de bancada 290 mm)
AX = BT + 0.166          # eje del husillo (altura de centros 166 mm)
BED_L = 1.80             # largo de bancada (1000 mm entre puntas)
XC = 1.05                # posición del carro (centro)

# ---------------------------------------------------------------- escena
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'

MATS = {}


def mat(name, color, metal=0.0, rough=0.5):
    if name in MATS:
        return MATS[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    bsdf.inputs['Base Color'].default_value = (*color, 1.0)
    bsdf.inputs['Metallic'].default_value = metal
    bsdf.inputs['Roughness'].default_value = rough
    m.diffuse_color = (*color, 1.0)
    MATS[name] = m
    return m


def srgb(h):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92 for v in c)


M = {
    'pintura': mat('Fundición pintada', srgb('#d8d4c8'), 0.0, 0.55),
    'gabinete': mat('Chapa gabinete', srgb('#55606a'), 0.1, 0.6),
    'acero': mat('Acero mecanizado', srgb('#b9bec4'), 0.9, 0.32),
    'acero_osc': mat('Acero pavonado', srgb('#5c6168'), 0.85, 0.4),
    'negro': mat('Plástico negro', srgb('#1d1f22'), 0.0, 0.45),
    'goma': mat('Goma', srgb('#2a2a2a'), 0.0, 0.8),
    'bronce': mat('Bronce', srgb('#b58a4c'), 0.9, 0.35),
    'rojo': mat('Rojo emergencia', srgb('#c62f25'), 0.0, 0.4),
    'verde': mat('Verde', srgb('#2f8f4e'), 0.0, 0.4),
    'motor': mat('Motor', srgb('#3d6c8f'), 0.2, 0.5),
    'amarillo': mat('Amarillo seguridad', srgb('#e2b13c'), 0.0, 0.45),
    'vidrio': mat('Visor', srgb('#9fc6d8'), 0.0, 0.1),
    'cobre': mat('Manguera', srgb('#3b4a55'), 0.3, 0.5),
}

# ---------------------------------------------------------------- geometría


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

# ================================================================ BANCADA Y GABINETE
CJ = 'Bancada y gabinete'

bed = P()
bed.box(0, BED_L, -0.15, 0.15, TRAY_Z, BT - 0.03, M['pintura'])          # cuerpo
bed.box(0, BED_L, -0.16, 0.16, BT - 0.045, BT - 0.02, M['pintura'])       # ala superior
for y in (-0.112, 0.112):                                                 # guías en V
    bed.profile('X', (BED_L / 2, y, BT - 0.02), [(-0.016, 0), (0.016, 0), (0, 0.02)], BED_L, M['acero'])
for y0, y1 in ((-0.075, -0.045), (0.045, 0.075)):                          # guías planas
    bed.box(0, BED_L, y0, y1, BT - 0.02, BT, M['acero'])
for x in (0.55, 0.85, 1.15, 1.45):                                        # nervios
    bed.box(x - 0.015, x + 0.015, -0.152, 0.152, TRAY_Z, BT - 0.04, M['pintura'])
make('bancada', 'Bancada', CJ, bed, (0, 0, 0), bevel=0.003)

cab_l = P().box(-0.13, 0.42, -0.25, 0.22, 0, TRAY_Z - 0.03, M['gabinete'])
cab_l.box(-0.08, 0.37, -0.255, -0.25, 0.08, 0.52, M['gabinete'])         # puerta
cab_l.cyl('Y', (0.30, -0.258, 0.45), 0.012, 0.012, M['negro'])
make('gabinete_izq', 'Gabinete izquierdo (motor)', CJ, cab_l, (-0.28, 0, -0.42), bevel=0.004)

cab_r = P().box(1.42, 1.86, -0.22, 0.20, 0, TRAY_Z - 0.03, M['gabinete'])
cab_r.box(1.47, 1.81, -0.225, -0.22, 0.08, 0.52, M['gabinete'])
cab_r.cyl('Y', (1.52, -0.228, 0.45), 0.012, 0.012, M['negro'])
make('gabinete_der', 'Gabinete derecho (refrigerante)', CJ, cab_r, (0.30, 0, -0.42), bevel=0.004)

tray = P().box(-0.14, 1.88, -0.34, 0.28, TRAY_Z - 0.03, TRAY_Z - 0.02, M['gabinete'])
for (x0, x1, y0, y1) in ((-0.14, 1.88, -0.34, -0.33), (-0.14, 1.88, 0.27, 0.28),
                         (-0.14, -0.13, -0.34, 0.28), (1.87, 1.88, -0.34, 0.28)):
    tray.box(x0, x1, y0, y1, TRAY_Z - 0.03, TRAY_Z + 0.03, M['gabinete'])
make('bandeja', 'Bandeja de virutas', CJ, tray, (0, 0, -0.22))

guard = P().box(0.0, 1.80, 0.27, 0.28, TRAY_Z, TRAY_Z + 0.62, M['pintura'])
guard.box(0.0, 1.80, 0.25, 0.28, TRAY_Z + 0.61, TRAY_Z + 0.62, M['pintura'])
make('guardasalpicaduras', 'Guardasalpicaduras trasero', CJ, guard, (0, 0.55, 0.05))

brake = P().cyl('X', (0.92, -0.31, 0.12), 0.012, 1.0, M['acero_osc'])
brake.box(0.55, 1.30, -0.36, -0.30, 0.10, 0.13, M['amarillo'])           # pedal
brake.box(0.43, 0.46, -0.32, -0.28, 0.10, 0.30, M['acero_osc'])          # brazo
make('freno_pie', 'Freno de pie', CJ, brake, (0, -0.30, -0.42), bevel=0.003)

rack = P().box(0.30, 1.78, -0.172, -0.160, BT - 0.075, BT - 0.045, M['acero_osc'])
for i in range(0, 148):
    x = 0.305 + i * 0.01
    rack.box(x, x + 0.005, -0.176, -0.172, BT - 0.075, BT - 0.068, M['acero_osc'])
make('cremallera', 'Cremallera', CJ, rack, (0, -0.16, -0.12), smooth=False)

# ================================================================ MOTOR Y TRANSMISIÓN
CJ = 'Motor y transmisión'
MY, MZ = 0.06, 0.32          # eje del motor
HY, HZ = 0.08, AX - 0.06     # eje de entrada del cabezal (polea)

mot = P().cyl('X', (0.14, MY, MZ), 0.088, 0.24, M['motor'])
for i in range(10):                                                        # aletas
    a = 2 * math.pi * i / 10
    mot.obox((0.14, MY + 0.09 * math.cos(a), MZ + 0.09 * math.sin(a)), (0.22, 0.012, 0.012),
             Matrix.Rotation(a, 3, 'X'), M['motor'])
mot.cyl('X', (0.005, MY, MZ), 0.07, 0.03, M['motor'])
mot.cyl('X', (0.275, MY, MZ), 0.07, 0.03, M['motor'])
mot.cyl('X', (-0.03, MY, MZ), 0.012, 0.06, M['acero'])                   # eje
mot.box(0.04, 0.24, MY - 0.08, MY + 0.08, MZ - 0.11, MZ - 0.09, M['motor'])  # patas
mot.box(0.10, 0.18, MY - 0.04, MY + 0.04, MZ + 0.085, MZ + 0.13, M['motor'])  # bornera
make('motor', 'Motor 1,5 kW (IEC 90S-4)', CJ, mot, (-0.40, -0.55, -0.38), bevel=0.002)

pm = P().cyl('X', (-0.065, MY, MZ), 0.045, 0.05, M['acero_osc'])
for x in (-0.077, -0.053):
    pm.torus('X', (x, MY, MZ), 0.045, 0.006, M['acero_osc'])
make('polea_motor', 'Polea del motor', CJ, pm, (-0.75, -0.55, -0.38))

belts = P()
for x in (-0.077, -0.053):
    belts.loop(x, (MY, MZ), 0.042, (HY, HZ), 0.075, 0.009, 0.013, M['goma'])
make('correas', 'Correas en V A32 (A-813)', CJ, belts, (-0.55, 0, 0))

ph = P().cyl('X', (-0.065, HY, HZ), 0.078, 0.05, M['acero_osc'])
ph.cyl('X', (-0.065, HY, HZ), 0.03, 0.07, M['acero_osc'])
make('polea_cabezal', 'Polea del cabezal (eje de entrada)', CJ, ph, (-0.75, 0, 0.18))

# ================================================================ CABEZAL
CJ = 'Cabezal'
HX0, HX1 = 0.0, 0.47
HTOP = AX + 0.165

hs = P().box(HX0, HX1, -0.17, 0.16, BT, HTOP, M['pintura'])
hs.box(HX0 + 0.01, HX1 - 0.01, -0.175, -0.17, BT + 0.02, HTOP - 0.02, M['pintura'])   # tapa frontal
hs.cyl('X', (HX1 + 0.005, 0, AX), 0.075, 0.012, M['pintura'])                       # boca del husillo
hs.cyl('Y', (0.40, -0.178, BT + 0.10), 0.018, 0.006, M['vidrio'])                  # visor de aceite
hs.box(0.20, 0.36, -0.178, -0.175, HTOP - 0.08, HTOP - 0.03, M['acero'])           # chapa de velocidades
make('cabezal_carcasa', 'Carcasa del cabezal', CJ, hs, (0, 0, 0.45), bevel=0.006)

top = P().box(0.02, 0.45, -0.15, 0.14, HTOP, HTOP + 0.015, M['pintura'])
top.cyl('Z', (0.36, 0.0, HTOP + 0.02), 0.018, 0.012, M['negro'])                  # tapón de carga
make('cabezal_tapa', 'Tapa superior del cabezal', CJ, top, (0, 0, 0.68), bevel=0.004)

lev = P()
lev.cyl('Y', (0.11, -0.19, AX + 0.07), 0.05, 0.03, M['negro'])                     # selector alta/baja
lev.obox((0.11, -0.215, AX + 0.07), (0.13, 0.025, 0.03), Matrix.Rotation(math.radians(35), 3, 'Y'), M['negro'])
lev.cyl('Y', (0.11, -0.19, AX - 0.06), 0.035, 0.03, M['negro'])                    # selector 4 posiciones
lev.cyl('Y', (0.11, -0.22, AX - 0.06), 0.008, 0.06, M['acero'])
lev.cyl('Z', (0.11, -0.25, AX - 0.02), 0.012, 0.06, M['rojo'])
make('cabezal_palancas', 'Palancas de velocidad', CJ, lev, (0, -0.38, 0.45))

spi = P().cyl('X', (0.25, 0, AX), 0.03, 0.48, M['acero'])
spi.cyl('X', (0.485, 0, AX), 0.065, 0.03, M['acero'])                             # nariz Camlock D1-4
for i in range(3):
    a = 2 * math.pi * i / 3 + math.pi / 2
    spi.cyl('X', (0.502, 0.05 * math.cos(a), AX + 0.05 * math.sin(a)), 0.007, 0.012, M['acero_osc'])
spi.gear('X', (0.30, 0, AX), 0.062, 40, 0.025, M['acero'])
spi.gear('X', (0.20, 0, AX), 0.048, 31, 0.025, M['acero'])
spi.gear('X', (0.06, 0, AX), 0.035, 24, 0.02, M['acero'])
spi.tube('X', (0.25, 0, AX), 0.019, 0.0302, 0.49, M['acero_osc'])               # pasaje Ø38
make('husillo', 'Husillo principal', CJ, spi, (0, 0, 0))

brg_f = P().tube('X', (0.43, 0, AX), 0.030, 0.055, 0.028, M['acero_osc'])
brg_f.tube('X', (0.43, 0, AX), 0.036, 0.049, 0.030, M['bronce'])
make('rodamiento_delantero', 'Rodamiento delantero 30212', CJ, brg_f, (0, 0, 0.24))

brg_r = P().tube('X', (0.11, 0, AX), 0.030, 0.050, 0.024, M['acero_osc'])
brg_r.tube('X', (0.11, 0, AX), 0.035, 0.045, 0.026, M['bronce'])
make('rodamiento_trasero', 'Rodamiento trasero 30210', CJ, brg_r, (0, 0, 0.24))

tr = P().cyl('X', (0.20, HY, HZ), 0.013, 0.46, M['acero'])                         # eje de entrada
tr.gear('X', (0.30, HY, HZ), 0.035, 22, 0.025, M['acero'])
tr.gear('X', (0.20, HY, HZ), 0.050, 32, 0.025, M['acero'])
tr.cyl('X', (0.05, HY, HZ), 0.02, 0.03, M['acero_osc'])
tr.tube('X', (0.012, HY, HZ), 0.013, 0.022, 0.01, M['goma'])                       # retén 25x40x10
make('cabezal_engranajes', 'Eje de entrada y engranajes', CJ, tr, (0, 0.22, 0.10))

chk = P().cyl('X', (0.555, 0, AX), 0.10, 0.09, M['acero'])
chk.cyl('X', (0.505, 0, AX), 0.085, 0.012, M['acero_osc'])                        # placa adaptadora
chk.cyl('X', (0.601, 0, AX), 0.03, 0.004, M['acero_osc'])
for i in range(3):
    a = 2 * math.pi * i / 3 + math.pi / 6
    chk.cyl('Y' if abs(math.cos(a)) > 0.5 else 'Z', (0.555, 0.1 * math.cos(a), AX + 0.1 * math.sin(a)), 0.008, 0.01, M['acero_osc'])
make('plato', 'Plato de 3 mordazas Ø200', CJ, chk, (0.36, 0, 0), bevel=0.003)

for i in range(3):
    a = 2 * math.pi * i / 3 + math.pi / 2
    d = Vector((0, math.cos(a), math.sin(a)))
    rot = Matrix.Rotation(a - math.pi / 2, 3, 'X')
    jw = P()
    for k, (rr, h) in enumerate(((0.035, 0.022), (0.055, 0.03), (0.075, 0.038))):
        c = Vector((0.600 + h / 2, 0, AX)) + d * rr
        jw.obox(c, (h, 0.022, 0.02), rot, M['acero'])
    make(f'mordaza_{i + 1}', f'Mordaza {i + 1}', CJ, jw,
         (0.44, d.y * 0.13, d.z * 0.13), bevel=0.002)

cg = P().tube('X', (0.56, 0, AX), 0.125, 0.130, 0.14, M['amarillo'], a0=20, a1=160)
cg.cyl('Y', (0.56, 0.13, AX + 0.04), 0.008, 0.06, M['acero_osc'])
make('protector_plato', 'Protector del plato', CJ, cg, (0.36, 0, 0.32))

# ================================================================ LIRA Y CAJA NORTON
CJ = 'Lira y caja Norton'

lc = P().box(-0.13, -0.10, -0.18, 0.17, TRAY_Z + 0.01, HTOP, M['pintura'])
lc.box(-0.10, 0.0, -0.18, -0.17, TRAY_Z + 0.01, HTOP, M['pintura'])
lc.box(-0.10, 0.0, 0.16, 0.17, TRAY_Z + 0.01, HTOP, M['pintura'])
lc.box(-0.10, 0.0, -0.18, 0.17, HTOP - 0.01, HTOP, M['pintura'])
lc.cyl('X', (-0.135, 0.0, AX - 0.15), 0.02, 0.012, M['negro'])
make('tapa_lira', 'Tapa de la lira', CJ, lc, (-0.95, 0, 0), bevel=0.004)

gr = P()
gr.gear('X', (-0.025, -0.02, AX), 0.035, 30, 0.012, M['acero'])                   # salida del cabezal (a)
gr.gear('X', (-0.025, -0.075, AX - 0.12), 0.076, 120, 0.012, M['acero'])         # rueda doble 120T
gr.gear('X', (-0.04, -0.075, AX - 0.12), 0.080, 127, 0.012, M['acero_osc'])      # 127T
gr.gear('X', (-0.04, -0.02, BT - 0.16), 0.045, 40, 0.012, M['acero'])            # entrada caja Norton (b)
gr.profile('X', (-0.012, -0.05, AX - 0.12),
           [(-0.03, -0.20), (0.03, -0.20), (0.04, 0.10), (-0.04, 0.10)], 0.006, M['pintura'])  # lira (guitarra)
make('lira_engranajes', 'Engranajes de cambio (lira)', CJ, gr, (-0.45, -0.32, 0.0))

nb = P().box(0.02, 0.44, -0.30, -0.15, TRAY_Z + 0.02, BT - 0.05, M['pintura'])
nb.cyl('Y', (0.40, -0.302, TRAY_Z + 0.06), 0.012, 0.006, M['vidrio'])              # visor A12
make('caja_norton', 'Caja Norton', CJ, nb, (0, -0.36, -0.12), bevel=0.005)

kn = P()
for x, z in ((0.10, TRAY_Z + 0.17), (0.25, TRAY_Z + 0.17), (0.10, TRAY_Z + 0.08), (0.25, TRAY_Z + 0.08)):
    kn.cyl('Y', (x, -0.315, z), 0.032, 0.03, M['negro'])
    kn.box(x - 0.006, x + 0.006, -0.345, -0.325, z - 0.03, z + 0.03, M['negro'])
make('perillas_norton', 'Perillas de la caja Norton', CJ, kn, (0, -0.58, -0.12))

# ================================================================ DELANTAL Y BARRAS
CJ = 'Delantal y barras'
YR = -0.205
Z_LS, Z_FR, Z_CR = BT - 0.085, BT - 0.135, BT - 0.18

ls = P().cyl('X', ((0.44 + 1.78) / 2, YR, Z_LS), 0.011, 1.34, M['acero_osc'], segs=20)
for i in range(0, 447):                                                   # filete paso 3 mm
    x = 0.44 + i * 0.003
    ls.cyl('X', (x, YR, Z_LS), 0.0118, 0.0012, M['acero_osc'], segs=12)
make('tornillo_patron', 'Tornillo patrón Ø22', CJ, ls, (0, -0.22, -0.26), smooth=False)

fr = P().cyl('X', ((0.44 + 1.78) / 2, YR, Z_FR), 0.0095, 1.34, M['acero'], segs=20)
fr.box(0.44, 1.78, YR - 0.002, YR + 0.002, Z_FR + 0.007, Z_FR + 0.0097, M['acero_osc'])  # chavetero
make('barra_avances', 'Barra de avances Ø19', CJ, fr, (0, -0.22, -0.34))

cr = P().cyl('X', ((0.44 + 1.78) / 2, YR - 0.01, Z_CR), 0.008, 1.34, M['acero'], segs=20)
cr.cyl('Y', (1.30, YR - 0.03, Z_CR), 0.012, 0.04, M['acero_osc'])
cr.cyl('Z', (1.30, YR - 0.05, Z_CR + 0.06), 0.006, 0.12, M['acero'])
cr.cyl('Z', (1.30, YR - 0.05, Z_CR + 0.13), 0.013, 0.03, M['rojo'])
make('barra_mando', 'Barra de mando (marcha/parada)', CJ, cr, (0, -0.22, -0.42))

sup = P().box(1.76, 1.82, -0.24, -0.15, Z_CR - 0.03, BT - 0.05, M['pintura'])
sup.cyl('X', (1.825, YR, Z_LS), 0.016, 0.012, M['acero_osc'])
make('soporte_derecho', 'Soporte derecho de barras', CJ, sup, (0.30, -0.22, -0.26), bevel=0.004)

AXP = (0.92, 1.20)
ap = P().box(AXP[0], AXP[1], -0.255, -0.165, BT - 0.26, BT - 0.01, M['pintura'])
ap.cyl('Y', (1.17, -0.258, BT - 0.22), 0.012, 0.006, M['vidrio'])                  # visor A20
make('delantal', 'Delantal', CJ, ap, (0, -0.42, -0.06), bevel=0.006)

hw = P().handwheel('Y', (0.99, -0.29, BT - 0.11), 0.085, M['acero'], M['acero'], spokes=3, sign=1)
hw.cyl('Y', (0.99, -0.27, BT - 0.11), 0.012, 0.04, M['acero'])
make('volante_longitudinal', 'Volante de avance longitudinal', CJ, hw, (0, -0.68, -0.06))

al = P()
al.cyl('Y', (1.14, -0.27, BT - 0.07), 0.018, 0.03, M['acero_osc'])                 # media tuerca
al.obox((1.165, -0.29, BT - 0.05), (0.07, 0.014, 0.014), Matrix.Rotation(math.radians(-35), 3, 'Y'), M['acero_osc'])
al.cyl('Z', (1.195, -0.29, BT - 0.025), 0.011, 0.025, M['negro'])
al.cyl('Y', (1.14, -0.27, BT - 0.16), 0.016, 0.03, M['acero_osc'])                 # selector de avance
al.obox((1.14, -0.29, BT - 0.16), (0.012, 0.012, 0.07), Matrix.Identity(3), M['acero_osc'])
al.cyl('Y', (1.14, -0.30, BT - 0.125), 0.011, 0.02, M['negro'])
make('delantal_palancas', 'Palancas de media tuerca y avance', CJ, al, (0, -0.62, 0.02))

mn = P()
mn.tube('X', (1.05, YR, Z_LS), 0.011, 0.022, 0.05, M['bronce'], a0=-90, a1=90)
mn.tube('X', (1.05, YR, Z_LS), 0.011, 0.022, 0.05, M['bronce'], a0=95, a1=265)
make('media_tuerca', 'Media tuerca 33-4035', CJ, mn, (0, -0.42, -0.52))

wc = P()
wc.cyl('X', (1.05, YR, Z_FR), 0.017, 0.07, M['acero'])                             # sinfín
for i in range(12):
    wc.cyl('X', (1.02 + i * 0.006, YR, Z_FR), 0.021, 0.0025, M['acero'], segs=20)
wc.gear('Y', (1.05, YR + 0.01, Z_FR + 0.05), 0.034, 30, 0.014, M['bronce'])       # corona
make('sinfin_corona', 'Sinfín y corona del delantal', CJ, wc, (0, -0.42, -0.62))

td = P().cyl('Z', (1.23, -0.205, BT + 0.005), 0.026, 0.02, M['acero'])
td.box(1.215, 1.245, -0.215, -0.195, BT - 0.08, BT - 0.005, M['pintura'])
td.cyl('Y', (1.23, -0.19, BT - 0.065), 0.014, 0.01, M['acero_osc'])
make('reloj_roscar', 'Reloj de roscar', CJ, td, (0.14, -0.42, 0.16))

# ================================================================ CARROS
CJ = 'Carros'
S0, S1 = BT, BT + 0.045
sd = P().box(XC - 0.17, XC + 0.17, -0.165, 0.165, S0 + 0.012, S1, M['pintura'])
for y0, y1 in ((-0.165, -0.085), (0.085, 0.165)):
    sd.box(XC - 0.17, XC + 0.17, y0, y1, S0, S0 + 0.012, M['pintura'])
sd.box(XC - 0.06, XC + 0.06, -0.20, 0.165, S1 - 0.01, S1, M['pintura'])
sd.box(XC - 0.172, XC - 0.168, -0.15, 0.15, S0 + 0.004, S1 - 0.01, M['goma'])     # limpiaguías
sd.box(XC + 0.168, XC + 0.172, -0.15, 0.15, S0 + 0.004, S1 - 0.01, M['goma'])
make('carro_principal', 'Carro principal (bancada del carro)', CJ, sd, (0, 0, 0.14), bevel=0.004)

C0, C1 = S1, S1 + 0.04
cs = P().box(XC - 0.075, XC + 0.075, -0.235, 0.12, C0, C1, M['pintura'])
cs.box(XC - 0.08, XC - 0.075, -0.235, 0.12, C0, C1 - 0.008, M['acero_osc'])        # cuña
make('carro_transversal', 'Carro transversal', CJ, cs, (0, 0, 0.28), bevel=0.004)

cw = P().handwheel('Y', (XC, -0.27, C0 + 0.02), 0.055, M['acero'], M['acero'], spokes=3, sign=1)
cw.cyl('Y', (XC, -0.245, C0 + 0.02), 0.022, 0.022, M['acero'])                     # tambor graduado
make('volante_transversal', 'Volante del carro transversal', CJ, cw, (0, -0.30, 0.28))

nut = P().box(XC - 0.02, XC + 0.02, -0.08, -0.04, C0 - 0.03, C0, M['bronce'])
nut.cyl('Y', (XC, -0.06, C0 - 0.015), 0.006, 0.30, M['acero_osc'])
make('tuerca_transversal', 'Husillo y tuerca del transversal', CJ, nut, (0, 0, 0.21))

CY = -0.07
B0, B1 = C1, C1 + 0.015
sb = P().cyl('Z', (XC, CY, (B0 + B1) / 2), 0.065, B1 - B0, M['pintura'], segs=48)
sb.tube('Z', (XC, CY, B1 - 0.002), 0.062, 0.066, 0.004, M['acero'])
make('base_giratoria', 'Base giratoria del charriot', CJ, sb, (0, 0, 0.40))

T0, T1 = B1, B1 + 0.035
tp = P().box(XC - 0.10, XC + 0.10, CY - 0.045, CY + 0.045, T0, T1, M['pintura'])
tp.box(XC - 0.10, XC + 0.10, CY + 0.045, CY + 0.05, T0, T1 - 0.006, M['acero_osc'])  # cuña
make('charriot', 'Charriot (carro superior)', CJ, tp, (0, 0, 0.50), bevel=0.004)

ch = P().cyl('X', (XC + 0.13, CY, T0 + 0.018), 0.006, 0.06, M['acero'])
ch.handwheel('X', (XC + 0.165, CY, T0 + 0.018), 0.038, M['acero'], M['acero'], spokes=2, sign=1)
make('manija_charriot', 'Manija del charriot', CJ, ch, (0.18, 0, 0.50))

TPX = XC - 0.05
tw = P().box(TPX - 0.04, TPX + 0.04, CY - 0.04, CY + 0.04, T1, T1 + 0.075, M['acero_osc'])
tw.cyl('Z', (TPX, CY, T1 + 0.095), 0.014, 0.04, M['acero'])
tw.obox((TPX + 0.04, CY - 0.03, T1 + 0.11), (0.12, 0.012, 0.012), Matrix.Rotation(math.radians(-30), 3, 'Z'), M['acero'])
tw.cyl('Z', (TPX + 0.09, CY - 0.06, T1 + 0.11), 0.01, 0.03, M['negro'])
for dx in (-0.02, 0.02):
    tw.cyl('Z', (TPX + dx, CY - 0.045, T1 + 0.072), 0.006, 0.012, M['acero'])
make('torre', 'Torre portaherramientas (4 posiciones)', CJ, tw, (0, 0, 0.66), bevel=0.003)

tool = P().box(TPX - 0.008, TPX + 0.008, CY - 0.03, CY + 0.07, AX - 0.016, AX, M['acero'])
tool.profile('X', (TPX, CY + 0.075, AX - 0.008), [(-0.005, -0.008), (0.005, -0.008), (0.0, 0.008)], 0.016, M['amarillo'])
make('cuchilla', 'Cuchilla 16×16', CJ, tool, (0, 0.16, 0.66))

# ================================================================ CONTRAPUNTO
CJ = 'Contrapunto'
TX0, TX1 = 1.47, 1.70
tb = P().box(TX0, TX1, -0.13, 0.13, BT, BT + 0.03, M['pintura'])
tb.box(TX0 + 0.02, TX1 - 0.02, -0.13, 0.13, BT - 0.03, BT, M['pintura'])
make('contrapunto_base', 'Base del contrapunto', CJ, tb, (0.30, 0, 0), bevel=0.004)

tbd = P().box(TX0 + 0.01, TX1 - 0.01, -0.07, 0.07, BT + 0.03, AX, M['pintura'])
tbd.cyl('X', ((TX0 + TX1) / 2, 0, AX), 0.07, TX1 - TX0 - 0.02, M['pintura'])
tbd.box(TX1 - 0.04, TX1 - 0.01, -0.075, -0.07, BT + 0.035, BT + 0.06, M['acero'])  # escala de desplazamiento
make('contrapunto_cuerpo', 'Cuerpo del contrapunto', CJ, tbd, (0.30, 0, 0.20), bevel=0.006)

q = P().cyl('X', (TX0 - 0.03, 0, AX), 0.016, 0.12, M['acero'])
q.cyl('X', (TX0 - 0.115, 0, AX), 0.016, 0.05, M['acero'], r2=0.0)                 # punta MT3
q.cyl('X', (TX0 - 0.083, 0, AX), 0.009, 0.015, M['acero_osc'])
make('cana', 'Caña Ø32 con punta MT3', CJ, q, (0.12, 0, 0.20))

tw2 = P().cyl('X', (TX1 + 0.02, 0, AX), 0.009, 0.04, M['acero'])
tw2.handwheel('X', (TX1 + 0.045, 0, AX), 0.06, M['acero'], M['acero'], spokes=3, sign=1)
make('volante_contrapunto', 'Volante del contrapunto', CJ, tw2, (0.55, 0, 0.20))

tl = P()
tl.cyl('Y', (TX0 + 0.05, -0.075, AX + 0.045), 0.012, 0.02, M['acero_osc'])         # traba de caña
tl.obox((TX0 + 0.05, -0.09, AX + 0.07), (0.01, 0.01, 0.05), Matrix.Identity(3), M['acero_osc'])
tl.cyl('Y', (TX1 - 0.03, -0.14, BT + 0.015), 0.012, 0.02, M['acero_osc'])         # traba a la bancada
tl.obox((TX1 + 0.01, -0.15, BT + 0.04), (0.09, 0.012, 0.012), Matrix.Rotation(math.radians(-30), 3, 'Y'), M['acero_osc'])
tl.cyl('Y', (TX1 + 0.05, -0.15, BT + 0.065), 0.012, 0.03, M['negro'])
make('contrapunto_trabas', 'Palancas de traba', CJ, tl, (0.30, -0.22, 0.20))

# ================================================================ LUNETAS
CJ = 'Lunetas'
LX = 0.79
lf = P().box(LX - 0.03, LX + 0.03, -0.14, 0.14, BT, BT + 0.03, M['pintura'])
lf.tube('X', (LX, 0, AX), 0.075, 0.105, 0.04, M['pintura'], a0=-60, a1=240)
lf.box(LX - 0.02, LX + 0.02, -0.10, 0.10, BT + 0.03, AX - 0.06, M['pintura'])
for k in range(3):
    a = math.radians(90 + 120 * k)
    d = Vector((0, math.cos(a), math.sin(a)))
    c = Vector((LX, 0, AX)) + d * 0.075
    lf.obox(c, (0.012, 0.012, 0.05), Matrix.Rotation(a - math.pi / 2, 3, 'X'), M['bronce'])
    lf.cyl('X', Vector((LX, 0, AX)) + d * 0.105, 0.008, 0.03, M['acero_osc'])
make('luneta_fija', 'Luneta fija', CJ, lf, (-0.12, 0, 0.52), bevel=0.003)

FX = XC - 0.19
lm = P().box(FX - 0.02, FX + 0.02, 0.02, 0.07, S1, AX + 0.07, M['pintura'])
lm.box(FX - 0.02, FX + 0.02, -0.04, 0.07, AX + 0.05, AX + 0.08, M['pintura'])
lm.box(FX - 0.006, FX + 0.006, -0.006, 0.006, AX + 0.016, AX + 0.05, M['bronce'])  # patín superior
lm.box(FX - 0.006, FX + 0.006, 0.016, 0.03, AX - 0.006, AX + 0.006, M['bronce'])   # patín trasero
lm.box(FX - 0.006, FX + 0.006, 0.03, 0.04, AX - 0.006, AX + 0.006, M['pintura'])
make('luneta_movil', 'Luneta móvil', CJ, lm, (-0.06, 0, 0.50), bevel=0.002)

# ================================================================ REFRIGERACIÓN
CJ = 'Refrigeración'
tk = P().box(1.48, 1.80, -0.15, 0.12, 0.03, 0.20, M['acero_osc'])
tk.box(1.49, 1.79, -0.14, 0.11, 0.20, 0.205, M['cobre'])
make('deposito', 'Depósito de refrigerante', CJ, tk, (0.30, -0.55, -0.50), bevel=0.003)

pu = P().cyl('Z', (1.70, 0.02, 0.27), 0.045, 0.12, M['verde'])
pu.cyl('Z', (1.70, 0.02, 0.17), 0.03, 0.08, M['verde'])
pu.cyl('Y', (1.70, -0.025, 0.30), 0.018, 0.02, M['negro'])
make('bomba', 'Electrobomba AB-12', CJ, pu, (0.30, -0.55, -0.26))

hose = P().curve([(1.70, 0.02, 0.33), (1.62, 0.20, 0.55), (1.35, 0.21, TRAY_Z + 0.10),
                  (1.12, 0.20, BT + 0.08), (XC - 0.02, 0.10, AX + 0.12)], 0.007, M['cobre'])
hose.curve([(XC - 0.02, 0.10, AX + 0.12), (XC - 0.05, 0.02, AX + 0.10), (XC - 0.06, -0.03, AX + 0.04)],
           0.006, M['amarillo'])
hose.cyl('Z', (1.12, 0.20, BT + 0.08), 0.012, 0.03, M['negro'])                    # canilla
make('manguera', 'Caño articulado y canilla', CJ, hose, (0, 0.30, 0.32))

# ================================================================ ELÉCTRICO
CJ = 'Eléctrico'
eb = P().box(0.06, 0.40, 0.16, 0.245, BT + 0.02, HTOP - 0.01, M['gabinete'])
eb.box(0.08, 0.38, 0.245, 0.248, BT + 0.04, HTOP - 0.03, M['gabinete'])
make('tablero', 'Tablero eléctrico', CJ, eb, (0, 0.52, 0.45), bevel=0.003)

bp = P().box(0.30, 0.45, -0.185, -0.175, BT + 0.015, BT + 0.075, M['negro'])
bp.cyl('Y', (0.33, -0.198, BT + 0.045), 0.022, 0.02, M['rojo'], r2=0.016)         # seta de emergencia
bp.cyl('Y', (0.38, -0.19, BT + 0.045), 0.009, 0.012, M['verde'])                   # marcha
bp.cyl('Y', (0.42, -0.19, BT + 0.045), 0.009, 0.012, M['amarillo'])                # piloto
make('botonera', 'Botonera y seta de emergencia', CJ, bp, (0, -0.34, 0.36))

lamp = P().box(0.30, 0.36, 0.17, 0.23, HTOP, HTOP + 0.02, M['negro'])
lamp.curve([(0.33, 0.20, HTOP + 0.02), (0.36, 0.20, HTOP + 0.20), (0.50, 0.10, HTOP + 0.28),
            (0.62, 0.02, HTOP + 0.22)], 0.007, M['acero_osc'])
lamp.cyl('Z', (0.64, 0.01, HTOP + 0.18), 0.04, 0.07, M['negro'], r2=0.022)
make('lampara', 'Lámpara de trabajo', CJ, lamp, (0.10, 0.40, 0.60))

# ---------------------------------------------------------------- guardar y exportar
for ob in scene.objects:
    ob.select_set(True)

blend = os.path.join(OUT, 'torno_tm300.blend')
glb = os.path.join(OUT, 'torno_tm300.glb')
gltf_json = os.path.join(OUT, 'visor', 'torno_tm300.json')
os.makedirs(os.path.dirname(gltf_json), exist_ok=True)
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
