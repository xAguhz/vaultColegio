"""Modelo 3D por conjuntos del Suzuki Swift 1.5 XS (DBA-ZC21S, mercado japonés, 2008).

Se corre con Blender en segundo plano (no hace falta abrirlo):

    blender -b --factory-startup --python herramientas/suzuki_swift_3d.py

Genera 3D/suzuki_swift.blend, 3D/suzuki_swift.glb y 3D/visor/suzuki_swift.json
(el mismo modelo como glTF embebido, que es lo que carga el visor web).
Unidades: metros. Ejes de Blender: X hacia adelante (trompa en +X), Y hacia la
izquierda del auto, Z hacia arriba. El origen está en el piso, a mitad de la
distancia entre ejes y en el centro del ancho.

La carrocería se arma como una superficie por secciones (como las cuadernas de
un barco), se le da espesor y después se corta con prismas (booleanas) para
separar puertas, capó, portón, paragolpes, ópticas y cristales. La mecánica se
arma con primitivas.

Cotas del catálogo japonés (1.5XS, DBA-ZC21S): largo 3755, ancho 1690, alto
1510, distancia entre ejes 2390, despeje 140 mm; neumáticos 185/60R15. Datos de
mecánica del manual de taller RS415 (motor M15A, caja 4AT). La forma de la
carrocería es una aproximación hecha a ojo sobre fotos de perfil: no es un
relevamiento.

Cada objeto es una pieza seleccionable con propiedades propias (extras del
glTF): pid, nombre, conjunto y explode (desplazamiento [x, y, z] en metros
cuando el despiece está al 100 %).
"""
import bpy
import bmesh
import math
import os
from mathutils import Matrix, Vector

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(VAULT, '3D')
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
        for attr, val in (('surface_render_method', 'BLENDED'), ('blend_method', 'BLEND')):
            try:
                setattr(m, attr, val)
            except (AttributeError, TypeError):
                pass
    m.diffuse_color = (*color, alpha)
    MATS[name] = m
    return m


def srgb(h):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92 for v in c)


M = {
    'pintura': mat('Pintura roja', srgb('#b3121f'), 0.35, 0.28),
    'interior_chapa': mat('Chapa interior', srgb('#8a8d91'), 0.2, 0.6),
    'vidrio': mat('Cristal', srgb('#3c4c58'), 0.0, 0.05, alpha=0.38),
    'negro': mat('Plástico negro', srgb('#1b1c1e'), 0.0, 0.5),
    'negro_brillo': mat('Negro brillante', srgb('#0d0e10'), 0.1, 0.15),
    'faro': mat('Óptica', srgb('#c9d6de'), 0.6, 0.12, alpha=0.75),
    'calavera': mat('Calavera roja', srgb('#a3141b'), 0.1, 0.15, alpha=0.85),
    'cromo': mat('Cromado', srgb('#d4d7da'), 1.0, 0.12),
    'goma': mat('Goma', srgb('#232323'), 0.0, 0.85),
    'llanta': mat('Llanta de aleación', srgb('#b7bcc2'), 0.9, 0.3),
    'acero': mat('Acero', srgb('#9aa0a6'), 0.85, 0.35),
    'acero_osc': mat('Acero oscuro', srgb('#4f545a'), 0.8, 0.45),
    'fundicion': mat('Fundición', srgb('#6d6a66'), 0.6, 0.6),
    'aluminio': mat('Aluminio', srgb('#a9adb0'), 0.85, 0.4),
    'disco': mat('Disco de freno', srgb('#7c7f83'), 0.9, 0.38),
    'caliper': mat('Mordaza', srgb('#3f4347'), 0.5, 0.5),
    'resorte': mat('Resorte', srgb('#2f6db0'), 0.4, 0.4),
    'amortiguador': mat('Amortiguador', srgb('#d9b23a'), 0.3, 0.4),
    'tapizado': mat('Tapizado', srgb('#3b3e44'), 0.0, 0.9),
    'tablero': mat('Tablero', srgb('#2b2d31'), 0.0, 0.7),
    'radiador': mat('Radiador', srgb('#5b5f63'), 0.7, 0.5),
    'bateria': mat('Batería', srgb('#e8e6df'), 0.0, 0.5),
    'rojo_tapa': mat('Tapa roja', srgb('#c62f25'), 0.0, 0.4),
    'amarillo': mat('Amarillo', srgb('#e2b13c'), 0.0, 0.45),
    'escape': mat('Escape', srgb('#7a6a5a'), 0.7, 0.55),
    'tanque': mat('Tanque', srgb('#3a3d40'), 0.2, 0.6),
    'motor_negro': mat('Tapa de válvulas', srgb('#26282b'), 0.3, 0.45),
    'correa': mat('Correa', srgb('#151515'), 0.0, 0.8),
    'cuadro': mat('Cuadro de instrumentos', srgb('#e9eef2'), 0.0, 0.3),
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



def add_mesh(part, me, override=None):
    """Agrega una malla ya hecha (por ejemplo, el resultado de una booleana) a la pieza."""
    n0 = len(part.bm.faces)
    part.bm.from_mesh(me)
    part.bm.faces.ensure_lookup_table()
    for f in part.bm.faces[n0:]:
        src = override
        if src is None:
            src = me.materials[f.material_index] if len(me.materials) > f.material_index else M['pintura']
            if src is None:
                src = M['pintura']
        f.material_index = part._mi(src)
    return part


Part.add_mesh = add_mesh


def transform_part(part, mtx):
    bmesh.ops.transform(part.bm, matrix=mtx, verts=part.bm.verts)
    return part


def make(pid, nombre, conjunto, part, explode, smooth=True, angle=32):
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
        mod.split_angle = math.radians(angle)
    return ob


P = Part

# ================================================================ cotas generales
WB = 2.390                 # distancia entre ejes
XF, XR = WB / 2, -WB / 2   # eje delantero y trasero
TF, TR = 1.470, 1.475      # trochas (aprox.)
R_RUEDA = (0.381 + 2 * 0.185 * 0.60) / 2   # 185/60R15 → 0,3015 m
ZA = R_RUEDA               # altura de los ejes (con el auto apoyado)
X_NARIZ, X_COLA = 1.935, -1.820   # 3755 mm de largo
ESP = 0.012                # espesor que se le da a la chapa del modelo


def cr(keys, x):
    """Interpolación suave (Catmull-Rom) sobre puntos clave (x, valor)."""
    if x <= keys[0][0]:
        return keys[0][1]
    if x >= keys[-1][0]:
        return keys[-1][1]
    for i in range(len(keys) - 1):
        if keys[i][0] <= x <= keys[i + 1][0]:
            break
    x0, y0 = keys[max(i - 1, 0)]
    x1, y1 = keys[i]
    x2, y2 = keys[i + 1]
    x3, y3 = keys[min(i + 2, len(keys) - 1)]
    t = (x - x1) / (x2 - x1)
    m1 = (y2 - y0) / (x2 - x0) * (x2 - x1) if x2 != x0 else 0
    m2 = (y3 - y1) / (x3 - x1) * (x2 - x1) if x3 != x1 else 0
    # limitador (como PCHIP) para que no haya rebotes
    d = y2 - y1
    if d == 0:
        m1 = m2 = 0
    else:
        if m1 * d < 0:
            m1 = 0
        if m2 * d < 0:
            m2 = 0
        m1 = max(-3 * abs(d), min(3 * abs(d), m1))
        m2 = max(-3 * abs(d), min(3 * abs(d), m2))
    t2, t3 = t * t, t * t * t
    return (2 * t3 - 3 * t2 + 1) * y1 + (t3 - 2 * t2 + t) * m1 + (-2 * t3 + 3 * t2) * y2 + (t3 - t2) * m2


# perfil lateral y planta (aproximados sobre fotos; cotas generales del catálogo)
K_TECHO = [(-1.835, 0.95), (-1.815, 1.06), (-1.76, 1.24), (-1.66, 1.38), (-1.54, 1.455), (-1.30, 1.495),
           (-0.60, 1.510), (-0.05, 1.495), (0.12, 1.465), (0.35, 1.36), (0.62, 1.19), (0.95, 0.965),
           (1.25, 0.922), (1.55, 0.868), (1.76, 0.808), (1.87, 0.752), (1.922, 0.675), (1.945, 0.575)]
K_PISO = [(-1.835, 0.32), (-1.80, 0.26), (-1.70, 0.215), (-1.45, 0.19), (1.45, 0.19), (1.80, 0.235),
          (1.90, 0.27), (1.945, 0.31)]
K_CINTURA = [(-1.835, 1.00), (-1.40, 1.005), (-0.30, 0.975), (0.40, 0.95), (0.95, 0.925), (1.30, 0.878),
             (1.60, 0.832), (1.85, 0.745), (1.945, 0.60)]
K_ANCHO = [(-1.835, 0.70), (-1.80, 0.775), (-1.70, 0.815), (-1.50, 0.838), (-1.10, 0.845), (0.60, 0.845),
           (1.20, 0.838), (1.50, 0.815), (1.72, 0.765), (1.86, 0.69), (1.92, 0.615), (1.945, 0.54)]
K_TECHO_ANCHO = [(-1.835, 0.52), (-1.70, 0.56), (-1.40, 0.615), (-0.60, 0.635), (0.10, 0.62), (0.60, 0.66),
                 (0.95, 0.70), (1.945, 0.50)]
M_HALF = 26     # puntos por media sección


def chaikin(pts, it=3):
    for _ in range(it):
        out = [pts[0]]
        for a, b in zip(pts[:-1], pts[1:]):
            out.append((0.75 * a[0] + 0.25 * b[0], 0.75 * a[1] + 0.25 * b[1]))
            out.append((0.25 * a[0] + 0.75 * b[0], 0.25 * a[1] + 0.75 * b[1]))
        out.append(pts[-1])
        pts = out
    return pts


def resample(pts, n):
    d = [0.0]
    for a, b in zip(pts[:-1], pts[1:]):
        d.append(d[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    L = d[-1]
    out, j = [], 0
    for i in range(n):
        s = L * i / (n - 1)
        while j < len(d) - 2 and d[j + 1] < s:
            j += 1
        seg = d[j + 1] - d[j] or 1e-9
        t = (s - d[j]) / seg
        a, b = pts[j], pts[j + 1]
        out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
    return out


def seccion(x):
    """Media sección (y >= 0) desde abajo en el centro hasta arriba en el centro."""
    zb, zt = cr(K_PISO, x), cr(K_TECHO, x)
    w = cr(K_ANCHO, x)
    zc = min(cr(K_CINTURA, x), zt - 0.05)
    h = zt - zc                                    # altura del invernadero (vidrios)
    k = max(0.0, min(1.0, (h - 0.06) / 0.30))
    wt = (w - 0.10) * (1 - k) + cr(K_TECHO_ANCHO, x) * k
    zm = zb + 0.45 * (zc - zb)
    pts = [(0.0, zb), (w - 0.10, zb), (w - 0.01, zb + 0.07), (w, zm), (w - 0.004, zc),
           (w - 0.035 * k, zc + 0.02 * k), (wt + 0.06 * k, zt - 0.03 - 0.03 * k), (wt * 0.6, zt), (0.0, zt + 0.012)]
    return resample(chaikin(pts, 3), M_HALF)


def surf_y(x, z):
    """Semiancho exterior de la carrocería a la altura z en la estación x."""
    half = seccion(x)
    best = 0.0
    for (y0, z0), (y1, z1) in zip(half[:-1], half[1:]):
        if min(z0, z1) <= z <= max(z0, z1) and z1 != z0:
            best = max(best, y0 + (y1 - y0) * (z - z0) / (z1 - z0))
    return best


def estaciones():
    xs, x = [], X_COLA
    while x < X_NARIZ - 1e-6:
        xs.append(x)
        fino = (x < X_COLA + 0.12) or (x > X_NARIZ - 0.14)
        x += 0.012 if fino else 0.04
    xs.append(X_NARIZ)
    return xs


def carroceria_base():
    bm = bmesh.new()
    rings = []
    for x in estaciones():
        half = seccion(x)
        loop = half + [(-y, z) for (y, z) in reversed(half[1:-1])]
        rings.append([bm.verts.new((x, y, z)) for (y, z) in loop])
    n = len(rings[0])
    for a, b in zip(rings[:-1], rings[1:]):
        for i in range(n):
            j = (i + 1) % n
            bm.faces.new((a[i], a[j], b[j], b[i]))
    bm.faces.new(list(reversed(rings[0])))
    bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new('carroceria_solida')
    bm.to_mesh(me)
    bm.free()
    me.materials.append(M['pintura'])
    me.materials.append(M['interior_chapa'])
    ob = bpy.data.objects.new('carroceria_solida', me)
    scene.collection.objects.link(ob)
    sol = ob.modifiers.new('chapa', 'SOLIDIFY')
    sol.thickness = ESP
    sol.offset = -1
    sol.use_even_offset = True
    sol.material_offset = 1
    sol.material_offset_rim = 1
    dg = bpy.context.evaluated_depsgraph_get()
    me2 = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
    bpy.data.objects.remove(ob)
    ob2 = bpy.data.objects.new('carroceria', me2)
    scene.collection.objects.link(ob2)
    return ob2


# ---------------------------------------------------------------- booleanas
CUT_COLL = bpy.data.collections.new('cortadores')
scene.collection.children.link(CUT_COLL)
SOLVERS = [i.identifier for i in bpy.types.BooleanModifier.bl_rna.properties['solver'].enum_items]
SOLVER = 'EXACT' if 'EXACT' in SOLVERS else SOLVERS[0]


def prisma(name, pts, plano, a0, a1):
    """Prisma: polígono en el plano ('XZ', 'XY' o 'YZ') extruido entre a0 y a1 en el eje que falta."""
    bm = bmesh.new()

    def v(p, a):
        if plano == 'XZ':
            return (p[0], a, p[1])
        if plano == 'XY':
            return (p[0], p[1], a)
        return (a, p[0], p[1])
    vb = [bm.verts.new(v(p, a0)) for p in pts]
    vt = [bm.verts.new(v(p, a1)) for p in pts]
    bm.faces.new(vb)
    bm.faces.new(list(reversed(vt)))
    n = len(pts)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((vb[i], vt[i], vt[j], vb[j]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new('c_' + name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new('c_' + name, me)
    CUT_COLL.objects.link(ob)
    return ob


def caja_cut(name, x0, x1, y0, y1, z0, z1):
    return prisma(name, [(x0, z0), (x1, z0), (x1, z1), (x0, z1)], 'XZ', y0, y1)


def cilindro_cut(name, cx, cz, r, y0, y1, n=48):
    pts = [(cx + r * math.cos(2 * math.pi * i / n), cz + r * math.sin(2 * math.pi * i / n)) for i in range(n)]
    return prisma(name, pts, 'XZ', y0, y1)


def booleana(src, cutters, op):
    """Devuelve una malla nueva = src (op) cada cortador, sin tocar src."""
    tmp = bpy.data.objects.new('tmp_bool', src.data.copy())
    scene.collection.objects.link(tmp)
    for c in cutters:
        mod = tmp.modifiers.new('b', 'BOOLEAN')
        mod.operation = op
        mod.object = c
        mod.solver = SOLVER
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(tmp.evaluated_get(dg))
    old = tmp.data
    bpy.data.objects.remove(tmp)
    bpy.data.meshes.remove(old)
    return me


def separar(cuerpo, cutters):
    """Saca de la carrocería la parte que queda dentro de los cortadores.
    Devuelve la malla de la pieza; la carrocería queda sin esa parte."""
    pieza = booleana(cuerpo, cutters[:1], 'INTERSECT') if len(cutters) == 1 else None
    if pieza is None:
        # varios cortadores: se unen primero en uno solo
        u = cutters[0]
        for c in cutters[1:]:
            me = booleana(u, [c], 'UNION')
            u = bpy.data.objects.new('union', me)
            CUT_COLL.objects.link(u)
        pieza = booleana(cuerpo, [u], 'INTERSECT')
        cutters = [u]
    resto = booleana(cuerpo, cutters, 'DIFFERENCE')
    old = cuerpo.data
    cuerpo.data = resto
    bpy.data.meshes.remove(old)
    return pieza


def espejo_y(pts_xy):
    return [(x, -y) for (x, y) in reversed(pts_xy)]


# ================================================================ CARROCERÍA
cuerpo = carroceria_base()

# pasaruedas
arcos = []
for i, xa in enumerate((XF, XR)):
    for s in (1, -1):
        arcos.append(cilindro_cut(f'arco{i}{s}', xa, ZA, 0.352, 0.50 * s if s > 0 else -1.0, 1.0 if s > 0 else -0.50))
me = booleana(cuerpo, arcos, 'DIFFERENCE')
old = cuerpo.data
cuerpo.data = me
bpy.data.meshes.remove(old)

# ---------- cristales: se separan de la chapa y se les cambia el material
DLO = [(0.915, 0.965), (0.60, 1.165), (0.32, 1.33), (0.15, 1.42), (-0.20, 1.448), (-1.10, 1.452),
       (-1.27, 1.43), (-1.335, 1.33), (-1.31, 1.03)]          # ventanas laterales (perfil)
lat = separar(cuerpo, [prisma('dlo', DLO, 'XZ', -1.0, 1.0)])
para = separar(cuerpo, [prisma('parabrisas', [(0.935, 0.90), (0.15, 1.39), (0.15, 1.70), (0.935, 1.20)], 'XZ', -0.60, 0.60)])
luneta = separar(cuerpo, [prisma('luneta', [(-1.565, 1.40), (-1.79, 1.085), (-1.95, 1.10), (-1.95, 1.60), (-1.565, 1.60)],
                                  'XZ', -0.53, 0.53)])
lat_ob = bpy.data.objects.new('lat_tmp', lat)
scene.collection.objects.link(lat_ob)

# ---------- ópticas, parrilla
FARO_L = [(1.952, 0.36), (1.935, 0.60), (1.84, 0.775), (1.66, 0.86), (1.47, 0.875), (1.50, 0.80), (1.70, 0.63),
          (1.84, 0.42)]
faro_l = separar(cuerpo, [prisma('faroL', FARO_L, 'XY', 0.665, 0.93)])
faro_r = separar(cuerpo, [prisma('faroR', [(x, -y) for x, y in FARO_L], 'XY', 0.665, 0.93)])
cal_l = separar(cuerpo, [caja_cut('calL', -1.95, -1.67, 0.50, 1.0, 0.80, 1.20)])
cal_r = separar(cuerpo, [caja_cut('calR', -1.95, -1.67, -1.0, -0.50, 0.80, 1.20)])
parrilla = separar(cuerpo, [caja_cut('parr', 1.86, 2.0, -0.36, 0.36, 0.46, 0.635),
                            caja_cut('toma', 1.85, 2.0, -0.42, 0.42, 0.25, 0.37)])

# ---------- puertas (polígonos de perfil, extruidos solo en el costado)
PUERTA_D = [(0.80, 0.215), (0.83, 0.70), (0.935, 0.935), (0.62, 1.16), (0.18, 1.47), (-0.275, 1.47), (-0.275, 0.215)]
PUERTA_T = [(-0.295, 0.215), (-0.295, 1.47), (-1.255, 1.47), (-1.20, 1.00), (-0.98, 0.78), (-0.86, 0.60), (-0.845, 0.215)]
puertas = {}
for nombre_p, pol in (('del', PUERTA_D), ('tra', PUERTA_T)):
    for lado, (y0, y1) in (('izq', (0.42, 1.0)), ('der', (-1.0, -0.42))):
        c = prisma(f'p_{nombre_p}_{lado}', pol, 'XZ', y0, y1)
        chapa = separar(cuerpo, [c])
        vidrio = booleana(lat_ob, [c], 'INTERSECT')
        me2 = booleana(lat_ob, [c], 'DIFFERENCE')
        old = lat_ob.data
        lat_ob.data = me2
        bpy.data.meshes.remove(old)
        puertas[(nombre_p, lado)] = (chapa, vidrio)

# ---------- capó, portón y paragolpes
capo = separar(cuerpo, [prisma('capo', [(0.955, 0.885), (1.872, 0.70), (1.872, 1.30), (0.955, 1.30)], 'XZ', -0.745, 0.745)])
porton = separar(cuerpo, [caja_cut('porton', -1.95, -1.50, -0.66, 0.66, 0.635, 1.60)])
pg_del = separar(cuerpo, [caja_cut('pgdel', 1.60, 2.0, -1.0, 1.0, 0.0, 0.672)])
pg_tra = separar(cuerpo, [caja_cut('pgtra', -2.0, -1.565, -1.0, 1.0, 0.0, 0.635)])

CJ = 'Carrocería'
EXP = 1.0
b = P().add_mesh(cuerpo.data, None)
# parantes B negros (en el Swift, los parantes A y B van en negro: techo "flotante")
for s in (1, -1):
    pts = [(-0.285, s * (surf_y(-0.285, z) + 0.004), z) for z in (0.985, 1.10, 1.22, 1.33, 1.425)]
    for xo in (-0.02, 0.0, 0.02):
        b.curve([(px + xo, py, pz) for px, py, pz in pts], 0.012, M['negro_brillo'])
make('casco', 'Casco (carrocería autoportante)', CJ, b, (0, 0, 0), angle=40)

make('capo', 'Capó', CJ, P().add_mesh(capo), (0.25, 0, 0.75), angle=40)
po = P().add_mesh(porton).add_mesh(luneta, M['vidrio'])
po.box(-1.83, -1.80, -0.14, 0.14, 0.86, 0.90, M['cromo'])          # manija del portón
make('porton', 'Portón trasero con luneta', CJ, po, (-0.65, 0, 0.35), angle=40)
pd = P().add_mesh(pg_del)
make('paragolpes_del', 'Paragolpes delantero', CJ, pd, (0.70, 0, -0.05), angle=40)
make('paragolpes_tra', 'Paragolpes trasero', CJ, P().add_mesh(pg_tra), (-0.70, 0, -0.05), angle=40)
make('parrilla', 'Parrilla y toma inferior', CJ, P().add_mesh(parrilla, M['negro']), (1.05, 0, 0.05), angle=40)

CJ = 'Puertas y cristales'
for (np_, lado), (chapa, vidrio) in puertas.items():
    s = 1 if lado == 'izq' else -1
    pp = P().add_mesh(chapa).add_mesh(vidrio, M['vidrio'])
    xm = 0.05 if np_ == 'del' else -0.90
    yh = surf_y(xm, 0.92)
    pp.box(xm - 0.08, xm + 0.08, s * yh - 0.012, s * yh + 0.012, 0.905, 0.93, M['negro'])   # manija
    if np_ == 'del':   # espejo retrovisor (va en la puerta)
        ym = surf_y(0.84, 0.95)
        pp.box(0.79, 0.87, s * (ym - 0.03), s * (ym + 0.05), 0.95, 0.985, M['negro'])
        pp.obox((0.80, s * (ym + 0.115), 1.00), (0.10, 0.17, 0.12), Matrix.Rotation(math.radians(8 * s), 3, 'Z'), M['pintura'])
        pp.obox((0.748, s * (ym + 0.12), 1.00), (0.012, 0.15, 0.095), Matrix.Rotation(math.radians(8 * s), 3, 'Z'), M['cromo'])
    nombre = f"Puerta {'delantera' if np_ == 'del' else 'trasera'} {'izquierda' if s > 0 else 'derecha'}"
    dx = 0.15 if np_ == 'del' else -0.15
    make(f'puerta_{np_}_{lado}', nombre, CJ, pp, (dx, s * 0.85, 0.05), angle=40)
make('parabrisas', 'Parabrisas laminado', CJ, P().add_mesh(para, M['vidrio']), (0.35, 0, 0.55), angle=40)
make('vidrios_fijos', 'Vidrios fijos traseros (cuartos)', CJ, P().add_mesh(lat_ob.data, M['vidrio']), (-0.25, 0, 0.45), angle=40)
bpy.data.objects.remove(lat_ob)

# limpiaparabrisas
wp = P()
for yy, L in ((-0.42, 0.55), (0.12, 0.48)):
    a = math.radians(4)
    wp.obox((0.95, yy + L / 2 * 0.98, 0.955), (0.022, L, 0.012), Matrix.Rotation(a, 3, 'Z'), M['negro'])
    wp.cyl('Z', (0.96, yy, 0.95), 0.015, 0.03, M['negro'])
make('limpiaparabrisas', 'Limpiaparabrisas', CJ, wp, (0.30, 0, 0.75))

CJ = 'Iluminación'
make('faro_izq', 'Faro delantero izquierdo', CJ, P().add_mesh(faro_l, M['faro']), (0.45, 0.45, 0.25), angle=40)
make('faro_der', 'Faro delantero derecho', CJ, P().add_mesh(faro_r, M['faro']), (0.45, -0.45, 0.25), angle=40)
make('calavera_izq', 'Calavera (luz trasera) izquierda', CJ, P().add_mesh(cal_l, M['calavera']), (-0.45, 0.45, 0.25), angle=40)
make('calavera_der', 'Calavera (luz trasera) derecha', CJ, P().add_mesh(cal_r, M['calavera']), (-0.45, -0.45, 0.25), angle=40)


# ================================================================ helpers de mecánica
def lathe(part, center, prof, m, sign=1, segs=48):
    """Sólido de revolución alrededor de un eje paralelo a Y. prof = [(radio, desplazamiento en Y)] cerrado."""
    cx, cy, cz = center

    def build():
        rings = []
        for i in range(segs):
            a = 2 * math.pi * i / segs
            rings.append([part.bm.verts.new((cx + r * math.cos(a), cy + sign * d, cz + r * math.sin(a))) for r, d in prof])
        n = len(prof)
        for i in range(segs):
            A, B = rings[i], rings[(i + 1) % segs]
            for j in range(n):
                k = (j + 1) % n
                part.bm.faces.new((A[j], A[k], B[k], B[j]))
    part._tag(part._new(build), m)
    return part


def helice(part, p0, p1, R, vueltas, r, m, n=None):
    """Resorte helicoidal entre p0 y p1."""
    p0, p1 = Vector(p0), Vector(p1)
    ax = (p1 - p0)
    L = ax.length
    ax.normalize()
    u = ax.orthogonal().normalized()
    v = ax.cross(u)
    n = n or int(vueltas * 14)
    pts = []
    for i in range(n + 1):
        t = i / n
        a = 2 * math.pi * vueltas * t
        pts.append(tuple(p0 + ax * (L * t) + u * (R * math.cos(a)) + v * (R * math.sin(a))))
    part.curve(pts, r, m, segs=2)
    return part


def barra(part, p0, p1, r, m, segs=16):
    """Cilindro entre dos puntos cualesquiera."""
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    rot = Vector((0, 0, 1)).rotation_difference(d.normalized()).to_matrix().to_4x4()
    mtx = Matrix.Translation((p0 + p1) / 2) @ rot

    def build():
        bmesh.ops.create_cone(part.bm, cap_ends=True, cap_tris=False, segments=segs,
                              radius1=r, radius2=r, depth=d.length, matrix=mtx)
    part._tag(part._new(build), m)
    return part


def caja_entre(part, p0, p1, ancho, alto, m):
    """Caja alargada entre dos puntos (brazos, largueros)."""
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    rot = Vector((1, 0, 0)).rotation_difference(d.normalized()).to_matrix()
    part.obox((p0 + p1) / 2, (d.length, ancho, alto), rot, m)
    return part


Part.lathe = lathe
Part.helice = helice
Part.barra = barra
Part.caja_entre = caja_entre

YF, YR = TF / 2, TR / 2

# ================================================================ RUEDAS
CJ = 'Ruedas'
TIRE = [(0.192, -0.084), (0.212, -0.093), (0.272, -0.093), (0.294, -0.080), (0.3015, -0.045), (0.3015, 0.045),
        (0.294, 0.080), (0.272, 0.093), (0.212, 0.093), (0.192, 0.084)]
for eje, xa, ya in (('del', XF, YF), ('tra', XR, YR)):
    for lado, s in (('izq', 1), ('der', -1)):
        w = P().lathe((xa, s * ya, ZA), TIRE, M['goma'], sign=s)
        w.lathe((xa, s * ya, ZA), [(0.170, -0.078), (0.191, -0.078), (0.191, 0.078), (0.170, 0.078)], M['llanta'], sign=s)
        # cara de la llanta y 5 rayos dobles
        w.cyl('Y', (xa, s * (ya + 0.045), ZA), 0.065, 0.03, M['llanta'])
        w.cyl('Y', (xa, s * (ya + 0.062), ZA), 0.03, 0.01, M['acero_osc'])
        for k in range(5):
            a = 2 * math.pi * k / 5
            for da in (-0.13, 0.13):
                rot = Matrix.Rotation(-(a + da), 3, 'Y')
                c = Vector((xa, s * (ya + 0.045), ZA)) + rot @ Vector((0.118, 0, 0))
                w.obox(c, (0.11, 0.022, 0.024), rot, M['llanta'])
        w.tube('Y', (xa, s * (ya + 0.06), ZA), 0.168, 0.186, 0.014, M['llanta'])
        nombre = f"Rueda {'delantera' if eje == 'del' else 'trasera'} {'izquierda' if s > 0 else 'derecha'}"
        make(f'rueda_{eje}_{lado}', nombre, CJ, w, (0, s * 0.95, 0), angle=40)

# ================================================================ FRENOS
CJ = 'Frenos'
for lado, s in (('izq', 1), ('der', -1)):
    d = P().tube('Y', (XF, s * (YF - 0.055), ZA), 0.055, 0.1275, 0.020, M['disco'])
    d.cyl('Y', (XF, s * (YF - 0.035), ZA), 0.075, 0.02, M['disco'])
    make(f'disco_{lado}', f"Disco de freno ventilado {'izquierdo' if s > 0 else 'derecho'}", CJ, d, (0.0, s * 0.62, 0.25))
    c = P()
    ang = math.radians(150)
    cc = Vector((XF + 0.112 * math.cos(ang), s * (YF - 0.055), ZA + 0.112 * math.sin(ang)))
    c.obox(cc, (0.06, 0.075, 0.13), Matrix.Rotation(-(ang - math.pi), 3, 'Y'), M['caliper'])
    c.obox(cc + Vector((-0.03, -s * 0.03, 0)), (0.05, 0.05, 0.10), Matrix.Rotation(-(ang - math.pi), 3, 'Y'), M['caliper'])
    c.barra(cc + Vector((0, -s * 0.04, 0.03)), cc + Vector((0.1, -s * 0.15, 0.12)), 0.006, M['negro'])   # flexible
    make(f'mordaza_{lado}', f"Mordaza (caliper) delantera {'izquierda' if s > 0 else 'derecha'}", CJ, c, (-0.25, s * 0.55, 0.35))
    t = P().cyl('Y', (XR, s * (YR - 0.06), ZA), 0.115, 0.05, M['fundicion'])
    t.cyl('Y', (XR, s * (YR - 0.09), ZA), 0.12, 0.008, M['acero_osc'])     # plato portazapatas
    t.cyl('Y', (XR, s * (YR - 0.03), ZA), 0.05, 0.02, M['fundicion'])
    make(f'tambor_{lado}', f"Freno a tambor trasero {'izquierdo' if s > 0 else 'derecho'}", CJ, t, (0, s * 0.62, 0.25))

sf = P().cyl('X', (1.035, -0.42, 0.72), 0.11, 0.11, M['acero_osc'])
sf.cyl('X', (1.16, -0.42, 0.72), 0.026, 0.15, M['aluminio'])
sf.box(1.11, 1.22, -0.46, -0.38, 0.75, 0.82, M['bateria'])
sf.cyl('Z', (1.165, -0.42, 0.83), 0.022, 0.025, M['amarillo'])
make('servofreno', 'Servofreno y bomba de freno', CJ, sf, (0.2, -0.35, 1.0))

# ================================================================ SUSPENSIÓN Y DIRECCIÓN
CJ = 'Suspensión y dirección'
for lado, s in (('izq', 1), ('der', -1)):
    st = P()
    base = (XF + 0.01, s * (YF - 0.13), ZA + 0.05)
    top = (XF + 0.03, s * (YF - 0.20), 0.82)
    st.barra(base, top, 0.026, M['amortiguador'])
    st.barra(base, (XF + 0.012, s * (YF - 0.135), ZA - 0.10), 0.03, M['fundicion'])     # mangueta
    st.cyl('Y', (XF, s * (YF - 0.10), ZA), 0.05, 0.05, M['fundicion'])                     # cubo
    lo = Vector(base).lerp(Vector(top), 0.45)
    hi = Vector(base).lerp(Vector(top), 0.93)
    st.helice(lo, hi, 0.072, 5, 0.008, M['resorte'])
    st.barra(Vector(lo) - Vector((0, 0, 0.006)), Vector(lo) + Vector((0, 0, 0.006)), 0.085, M['acero_osc'])
    st.barra(hi, Vector(hi) + Vector((0, 0, 0.03)), 0.09, M['negro'])
    make(f'amortiguador_del_{lado}', f"Columna McPherson {'izquierda' if s > 0 else 'derecha'} (amortiguador y resorte)",
         CJ, st, (0, s * 0.45, 0.55))
    br = P()
    br.caja_entre((XF - 0.01, s * (YF - 0.13), ZA - 0.10), (XF + 0.03, s * 0.30, 0.215), 0.06, 0.03, M['acero_osc'])
    br.caja_entre((XF + 0.03, s * 0.30, 0.215), (XF - 0.25, s * 0.33, 0.215), 0.05, 0.03, M['acero_osc'])
    br.cyl('Y', (XF + 0.03, s * 0.30, 0.215), 0.03, 0.06, M['goma'])
    br.cyl('X', (XF - 0.25, s * 0.33, 0.215), 0.035, 0.06, M['goma'])
    make(f'brazo_{lado}', f"Brazo inferior de suspensión {'izquierdo' if s > 0 else 'derecho'}", CJ, br, (0, s * 0.40, -0.25))

estab = P().curve([(XF - 0.02, 0.60, 0.33), (XF - 0.17, 0.52, 0.27), (XF - 0.18, 0.25, 0.25), (XF - 0.18, -0.25, 0.25),
                   (XF - 0.17, -0.52, 0.27), (XF - 0.02, -0.60, 0.33)], 0.011, M['acero_osc'])
make('estabilizadora', 'Barra estabilizadora delantera', CJ, estab, (-0.30, 0, -0.35))

ej = P()
ej.obox((XR + 0.20, 0, 0.30), (0.09, 1.16, 0.10), Matrix.Identity(3), M['acero_osc'])
for s in (1, -1):
    ej.caja_entre((XR + 0.58, s * 0.62, 0.31), (XR, s * 0.64, ZA), 0.06, 0.09, M['acero_osc'])
    ej.cyl('Y', (XR + 0.58, s * 0.62, 0.31), 0.04, 0.07, M['goma'])
    ej.cyl('Y', (XR, s * (YR - 0.11), ZA), 0.045, 0.06, M['fundicion'])
make('eje_torsion', 'Eje trasero de torsión (barra en U y brazos)', CJ, ej, (-0.35, 0, -0.45))
for lado, s in (('izq', 1), ('der', -1)):
    rt = P()
    rt.helice((XR + 0.08, s * 0.56, 0.35), (XR + 0.08, s * 0.56, 0.58), 0.06, 5, 0.0075, M['resorte'])
    rt.barra((XR - 0.09, s * 0.62, 0.27), (XR - 0.13, s * 0.58, 0.70), 0.022, M['amortiguador'])
    rt.barra((XR - 0.115, s * 0.595, 0.45), (XR - 0.13, s * 0.58, 0.70), 0.03, M['acero_osc'])
    make(f'amortiguador_tra_{lado}', f"Resorte y amortiguador trasero {'izquierdo' if s > 0 else 'derecho'}", CJ, rt,
         (-0.20, s * 0.40, 0.55))

dirc = P()
dirc.cyl('Y', (XF - 0.12, 0, 0.36), 0.026, 0.62, M['aluminio'])
for s in (1, -1):
    dirc.cyl('Y', (XF - 0.12, s * 0.355, 0.36), 0.03, 0.09, M['goma'], r2=0.014)
    dirc.barra((XF - 0.12, s * 0.40, 0.36), (XF - 0.13, s * (YF - 0.14), 0.33), 0.011, M['acero'])
dirc.barra((XF - 0.12, -0.30, 0.38), (XF - 0.16, -0.32, 0.50), 0.022, M['aluminio'])     # piñón
make('cremallera', 'Caja de dirección a cremallera y bieletas', CJ, dirc, (-0.20, 0, -0.30))

col = P()
col.curve([(XF - 0.16, -0.32, 0.50), (0.98, -0.34, 0.60), (0.80, -0.36, 0.76), (0.47, -0.37, 0.92)], 0.018, M['acero'])
col.barra((0.70, -0.37, 0.81), (0.55, -0.37, 0.88), 0.045, M['negro'])                    # tubo de columna
col.cyl('Y', (0.63, -0.30, 0.84), 0.045, 0.10, M['acero_osc'])                            # motor de la dirección eléctrica (EPS)
make('columna_eps', 'Columna de dirección con asistencia eléctrica (EPS)', CJ, col, (0.10, -0.30, 0.90))

vol = P().handwheel('Z', (0, 0, 0), 0.185, M['negro'], M['negro'], spokes=3, handle=False)
vol.cyl('Z', (0, 0, 0.03), 0.075, 0.05, M['negro'])               # módulo del airbag
transform_part(vol, Matrix.Translation((0.40, -0.37, 0.95)) @ Matrix.Rotation(math.radians(-64), 4, 'Y'))
make('volante', 'Volante con airbag (lado derecho, mano japonesa)', CJ, vol, (-0.10, -0.25, 1.05))

# ================================================================ MOTOR M15A
CJ = 'Motor M15A'
CYL_Y = [-0.335, -0.245, -0.155, -0.065]   # cilindro 1 del lado de la distribución (derecha)
bl = P()
bl.box(1.245, 1.50, -0.40, 0.02, 0.29, 0.625, M['aluminio'])
for y in CYL_Y:
    bl.cyl('X', (1.50, y, 0.48), 0.035, 0.012, M['aluminio'])                 # nervios
bl.box(1.26, 1.49, -0.385, 0.0, 0.20, 0.29, M['acero_osc'])                   # cárter
bl.cyl('Z', (1.42, -0.20, 0.195), 0.012, 0.01, M['acero'])                    # tapón de vaciado
bl.cyl('X', (1.215, -0.10, 0.38), 0.036, 0.075, M['azul'] if 'azul' in M else M['resorte'])   # filtro de aceite
make('bloque', 'Bloque de cilindros y cárter', CJ, bl, (0.65, -0.15, 1.20))

cz = P()
cz.box(1.255, 1.49, -0.40, 0.02, 0.625, 0.745, M['aluminio'])
make('culata', 'Tapa de cilindros (culata) DOHC 16 válvulas', CJ, cz, (0.65, -0.15, 1.55))
tv = P()
tv.box(1.275, 1.47, -0.39, 0.01, 0.745, 0.79, M['motor_negro'])
tv.cyl('Z', (1.37, -0.15, 0.80), 0.025, 0.025, M['amarillo'])                # tapa de llenado de aceite
for y in (CYL_Y[0], CYL_Y[3]):
    tv.box(1.35, 1.41, y - 0.025, y + 0.025, 0.79, 0.835, M['negro'])         # bobinas (cil. 1 y 4)
for y0, y1 in ((CYL_Y[0], CYL_Y[1]), (CYL_Y[3], CYL_Y[2])):
    tv.curve([(1.38, y0, 0.835), (1.40, (y0 + y1) / 2, 0.86), (1.38, y1, 0.80)], 0.006, M['negro'])   # cables de alta
make('tapa_valvulas', 'Tapa de válvulas, bobinas y cables de alta', CJ, tv, (0.65, -0.15, 1.85))

dist = P().box(1.245, 1.52, -0.435, -0.40, 0.25, 0.76, M['aluminio'])
make('distribucion', 'Tapa de distribución (cadena)', CJ, dist, (0.65, -0.55, 1.20))

adm = P()
adm.cyl('Y', (1.615, -0.16, 0.50), 0.05, 0.40, M['negro'])                   # cámara de admisión (plenum)
for y in CYL_Y:
    adm.curve([(1.49, y, 0.69), (1.56, y, 0.70), (1.63, y, 0.62), (1.62, y, 0.53)], 0.022, M['negro'])
adm.cyl('Y', (1.615, 0.07, 0.50), 0.038, 0.06, M['aluminio'])                # cuerpo de mariposa
adm.curve([(1.615, 0.10, 0.50), (1.58, 0.20, 0.56), (1.50, 0.22, 0.66)], 0.035, M['negro'])
make('admision', 'Múltiple de admisión y cuerpo de mariposa', CJ, adm, (1.10, 0.10, 1.10))

esc = P()
for y in CYL_Y:
    esc.curve([(1.255, y, 0.68), (1.20, y, 0.66), (1.17, (y - 0.20) / 2, 0.56), (1.16, -0.20, 0.47)], 0.02, M['escape'])
esc.box(1.14, 1.27, -0.38, 0.0, 0.55, 0.72, M['aluminio'])                    # cubrecalor
make('multiple_escape', 'Múltiple de escape y cubrecalor', CJ, esc, (0.15, -0.20, 1.25))

acc = P()
acc.cyl('Y', (1.36, -0.455, 0.40), 0.07, 0.035, M['acero_osc'])              # polea del cigüeñal
acc.cyl('Y', (1.42, -0.455, 0.63), 0.05, 0.03, M['acero_osc'])               # bomba de agua
acc.cyl('Y', (1.56, -0.38, 0.36), 0.065, 0.13, M['aluminio'])                # alternador
acc.cyl('Y', (1.56, -0.455, 0.36), 0.03, 0.03, M['acero_osc'])
acc.curve([(1.36, -0.455, 0.33), (1.56, -0.455, 0.33), (1.59, -0.455, 0.36), (1.56, -0.455, 0.39),
           (1.46, -0.455, 0.60), (1.42, -0.455, 0.68), (1.37, -0.455, 0.63), (1.29, -0.455, 0.42), (1.36, -0.455, 0.33)],
          0.006, M['correa'])
make('accesorios', 'Alternador, bomba de agua y correa de accesorios', CJ, acc, (0.85, -0.70, 0.95))

arr = P().cyl('Y', (1.17, 0.08, 0.40), 0.042, 0.17, M['acero_osc'])
arr.cyl('Y', (1.17, 0.18, 0.40), 0.03, 0.04, M['negro'])
make('arranque', 'Motor de arranque', CJ, arr, (-0.35, 0.40, 0.90))

fa = P()
fa.box(1.30, 1.56, 0.12, 0.38, 0.62, 0.78, M['negro'])
fa.curve([(1.55, 0.30, 0.70), (1.68, 0.38, 0.72), (1.80, 0.38, 0.66)], 0.03, M['negro'])
make('filtro_aire', 'Caja del filtro de aire', CJ, fa, (0.70, 0.55, 1.00))

# ================================================================ TRANSMISIÓN
CJ = 'Transmisión'
ta = P()
ta.cyl('Y', (1.36, 0.07, 0.42), 0.17, 0.10, M['aluminio'], r2=0.15)
ta.box(1.12, 1.46, 0.12, 0.40, 0.22, 0.56, M['aluminio'])
ta.cyl('Y', (1.20, 0.26, 0.30), 0.11, 0.26, M['aluminio'])                   # diferencial
ta.box(1.30, 1.40, 0.38, 0.42, 0.30, 0.45, M['negro'])                        # conector solenoides
make('caja_4at', 'Caja automática de 4 marchas (4AT) con diferencial', CJ, ta, (0.30, 0.70, 0.75))
for lado, s in (('izq', 1), ('der', -1)):
    sm = P()
    y0 = 0.40 if s > 0 else -0.10
    sm.barra((1.20, y0 * s if s > 0 else y0, 0.30), (XF, s * (YF - 0.13), ZA), 0.013, M['acero'])
    sm.cyl('Y', (1.20, (0.43 if s > 0 else -0.14), 0.30), 0.045, 0.08, M['goma'], r2=0.03)
    sm.cyl('Y', (XF + 0.002, s * (YF - 0.17), ZA), 0.03, 0.08, M['goma'], r2=0.045)
    make(f'semieje_{lado}', f"Semieje (palier) {'izquierdo' if s > 0 else 'derecho'} con homocinéticas", CJ, sm,
         (0, s * 0.30, -0.25))
pl = P()
pl.box(0.25, 0.50, -0.10, 0.10, 0.30, 0.62, M['tablero'])
pl.box(0.29, 0.45, -0.05, 0.05, 0.62, 0.63, M['cromo'])
pl.cyl('Z', (0.36, 0.0, 0.70), 0.008, 0.16, M['cromo'])
pl.cyl('Z', (0.36, 0.0, 0.79), 0.025, 0.06, M['negro'])
make('palanca', 'Consola y palanca selectora (P R N D 3 2 L)', CJ, pl, (0, 0, 1.25))

# ================================================================ REFRIGERACIÓN
CJ = 'Refrigeración'
rad = P().box(1.755, 1.785, -0.33, 0.33, 0.30, 0.66, M['radiador'])
for s in (1, -1):
    rad.box(1.75, 1.79, s * 0.33, s * 0.37, 0.29, 0.67, M['negro'])
rad.cyl('X', (1.79, 0.30, 0.68), 0.02, 0.03, M['acero'])
make('radiador', 'Radiador', CJ, rad, (1.20, 0, 0.20))
ven = P().box(1.70, 1.745, -0.32, 0.32, 0.31, 0.65, M['negro'])
ven.cyl('X', (1.69, 0.0, 0.48), 0.05, 0.05, M['acero_osc'])
make('electroventilador', 'Electroventilador del radiador', CJ, ven, (0.90, 0, 0.45))
dep = P().box(1.62, 1.72, -0.60, -0.48, 0.56, 0.72, M['bateria'])
dep.cyl('Z', (1.67, -0.54, 0.73), 0.02, 0.02, M['negro'])
make('deposito_refrigerante', 'Depósito recuperador de refrigerante', CJ, dep, (0.70, -0.55, 0.70))

# ================================================================ ELÉCTRICO
CJ = 'Eléctrico'
bat = P().box(1.30, 1.538, 0.415, 0.544, 0.40, 0.627, M['bateria'])
bat.box(1.30, 1.538, 0.415, 0.544, 0.40, 0.43, M['negro'])
bat.cyl('Z', (1.33, 0.48, 0.64), 0.012, 0.025, M['rojo_tapa'])
bat.cyl('Z', (1.51, 0.48, 0.64), 0.012, 0.025, M['negro'])
make('bateria', 'Batería 46B24R (12 V, 36 Ah)', CJ, bat, (0.35, 0.80, 0.90))
fus = P().box(1.00, 1.13, 0.44, 0.58, 0.58, 0.70, M['negro'])
fus.box(1.005, 1.125, 0.445, 0.575, 0.70, 0.705, M['amarillo'])
make('fusibles', 'Caja de fusibles y relés del motor', CJ, fus, (0.10, 0.70, 0.85))
fus2 = P().box(0.60, 0.70, -0.70, -0.55, 0.50, 0.62, M['negro'])
make('fusibles_cabina', 'Caja de empalmes (fusibles de cabina)', CJ, fus2, (0, -0.60, 0.70))

# ================================================================ COMBUSTIBLE Y ESCAPE
CJ = 'Combustible y escape'
tq = P().box(-1.00, -0.60, -0.42, 0.42, 0.155, 0.30, M['tanque'])
tq.box(-0.95, -0.65, -0.37, 0.37, 0.30, 0.33, M['tanque'])
tq.cyl('Z', (-0.80, 0.15, 0.335), 0.06, 0.012, M['negro'])                   # bomba y aforador
tq.curve([(-0.98, -0.40, 0.28), (-1.20, -0.62, 0.55), (-1.36, -0.76, 0.86)], 0.022, M['negro'])
make('tanque', 'Tanque de combustible (43 L) con bomba', CJ, tq, (0, 0, -0.65))
ex = P()
ex.curve([(1.16, -0.20, 0.47), (1.12, -0.15, 0.30), (1.04, -0.06, 0.235), (0.92, -0.05, 0.225)], 0.025, M['escape'])
ex.cyl('X', (0.74, -0.05, 0.225), 0.06, 0.34, M['escape'])                   # catalizador
ex.curve([(0.57, -0.05, 0.215), (-0.30, -0.05, 0.205), (-0.50, -0.25, 0.20), (-0.62, -0.50, 0.20), (-1.25, -0.50, 0.20),
          (-1.40, -0.40, 0.26)], 0.022, M['escape'])
ex.cyl('Y', (-1.55, -0.24, 0.31), 0.10, 0.42, M['escape'])                   # silenciador
ex.curve([(-1.62, -0.42, 0.29), (-1.75, -0.46, 0.27), (-1.86, -0.46, 0.27)], 0.022, M['escape'])
ex.cyl('X', (-1.85, -0.46, 0.27), 0.028, 0.06, M['cromo'])
make('escape', 'Línea de escape (catalizador y silenciador)', CJ, ex, (0, 0, -0.55))

# ================================================================ INTERIOR
CJ = 'Interior'
for lado, s in (('izq', 1), ('der', -1)):
    a = P()
    yc = s * 0.37
    a.box(-0.12, 0.38, yc - 0.24, yc + 0.24, 0.27, 0.36, M['acero_osc'])
    a.box(-0.14, 0.40, yc - 0.25, yc + 0.25, 0.36, 0.49, M['tapizado'])
    a.obox((-0.20, yc, 0.78), (0.12, 0.50, 0.62), Matrix.Rotation(math.radians(-14), 3, 'Y'), M['tapizado'])
    a.obox((-0.285, yc, 1.17), (0.10, 0.26, 0.17), Matrix.Rotation(math.radians(-10), 3, 'Y'), M['tapizado'])
    nombre = 'Asiento del conductor (derecho)' if s < 0 else 'Asiento del acompañante (izquierdo)'
    make(f'asiento_{lado}', nombre, CJ, a, (0.10, s * 0.25, 1.30), angle=40)
ab = P()
ab.box(-1.06, -0.58, -0.62, 0.62, 0.32, 0.47, M['tapizado'])
ab.obox((-1.12, 0, 0.77), (0.11, 1.24, 0.60), Matrix.Rotation(math.radians(-12), 3, 'Y'), M['tapizado'])
for y in (-0.42, 0.0, 0.42):
    ab.obox((-1.20, y, 1.13), (0.09, 0.24, 0.14), Matrix.Rotation(math.radians(-10), 3, 'Y'), M['tapizado'])
make('asiento_trasero', 'Asiento trasero rebatible', CJ, ab, (-0.25, 0, 1.30), angle=40)
tb = P()
tb.box(0.55, 0.86, -0.74, 0.74, 0.62, 0.92, M['tablero'])
tb.obox((0.66, 0, 0.94), (0.30, 1.48, 0.05), Matrix.Rotation(math.radians(12), 3, 'Y'), M['tablero'])
tb.box(0.52, 0.66, -0.53, -0.21, 0.92, 1.01, M['tablero'])                   # visera del cuadro
for y, r in ((-0.30, 0.055), (-0.44, 0.055), (-0.37, 0.035)):
    tb.cyl('X', (0.525, y, 0.95 if r < 0.05 else 0.935), r, 0.008, M['cuadro'])   # tres relojes
tb.box(0.50, 0.56, -0.09, 0.09, 0.62, 0.86, M['negro'])                      # consola central (audio y aire)
for y in (-0.05, 0.0, 0.05):
    tb.cyl('X', (0.495, y, 0.68), 0.018, 0.012, M['cromo'])                  # perillas del aire
make('tablero', 'Tablero e instrumentos', CJ, tb, (0.25, 0, 1.45), angle=40)
pe = P()
pe.barra((0.80, -0.27, 0.70), (0.72, -0.27, 0.40), 0.008, M['acero_osc'])
pe.obox((0.715, -0.27, 0.40), (0.02, 0.09, 0.07), Matrix.Rotation(math.radians(-30), 3, 'Y'), M['goma'])
pe.barra((0.82, -0.45, 0.62), (0.76, -0.45, 0.35), 0.006, M['acero_osc'])
pe.obox((0.75, -0.45, 0.33), (0.015, 0.05, 0.14), Matrix.Rotation(math.radians(-35), 3, 'Y'), M['goma'])
make('pedalera', 'Pedalera (freno y acelerador)', CJ, pe, (0.20, -0.30, 1.05))

# ---------------------------------------------------------------- limpieza
for ob in list(CUT_COLL.objects):
    bpy.data.objects.remove(ob)
bpy.data.collections.remove(CUT_COLL)
for ob in list(scene.collection.objects):     # restos sueltos (la carrocería ya está copiada en 'casco')
    if 'pid' not in ob:
        bpy.data.objects.remove(ob)

# ---------------------------------------------------------------- guardar y exportar
for ob in scene.objects:
    ob.select_set(True)
blend = os.path.join(OUT, 'suzuki_swift.blend')
glb = os.path.join(OUT, 'suzuki_swift.glb')
gltf_json = os.path.join(OUT, 'visor', 'suzuki_swift.json')
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
# copia como glTF con el binario embebido y extensión .json (los Artifacts no sirven .glb)
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

# ---------------------------------------------------------------- láminas (renders) para el vault y el visor
LAM = os.environ.get('SWIFT_LAMINAS')
if LAM:
    os.makedirs(LAM, exist_ok=True)
    scene.render.engine = 'BLENDER_WORKBENCH'
    sh = scene.display.shading
    sh.light = 'STUDIO'
    sh.color_type = 'MATERIAL'
    sh.show_cavity = True
    sh.show_shadows = True
    scene.render.film_transparent = False
    w = bpy.data.worlds.new('fondo')
    w.color = (0.80, 0.82, 0.84)
    scene.world = w
    sh.background_type = 'WORLD'
    scene.render.resolution_x, scene.render.resolution_y = 1400, 900
    scene.render.image_settings.file_format = 'JPEG'
    scene.render.image_settings.quality = 86
    cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam'))
    scene.collection.objects.link(cam)
    scene.camera = cam

    def foto(nombre, loc, target, lens=45, solo=None, despiece=0.0, xray=False):
        for o in scene.objects:
            if 'pid' not in o:
                continue
            e = Vector(o['explode'])
            o.location = e * despiece
            o.hide_render = bool(solo) and o['conjunto'] not in solo
        sh.show_xray = xray
        sh.xray_alpha = 0.35
        cam.data.lens = lens
        cam.location = loc
        cam.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
        scene.render.filepath = os.path.join(LAM, nombre + '.jpg')
        bpy.ops.render.render(write_still=True)

    foto('swift_34_delantera', (5.2, 4.3, 2.3), (0.05, 0, 0.62))
    foto('swift_34_trasera', (-5.2, -4.0, 2.5), (0.0, 0, 0.62))
    foto('swift_perfil', (0.05, 8.0, 0.8), (0.05, 0, 0.75), lens=50)
    foto('swift_despiece', (7.0, 6.2, 4.2), (0.2, 0, 1.0), lens=40, despiece=1.0)
    mec = ['Motor M15A', 'Transmisión', 'Refrigeración', 'Eléctrico', 'Suspensión y dirección', 'Frenos', 'Ruedas',
           'Combustible y escape', 'Interior']
    foto('swift_mecanica', (4.6, 4.0, 2.6), (0.0, 0, 0.45), solo=mec)
    lam = {
        'lamina_motor': (['Motor M15A', 'Transmisión', 'Refrigeración', 'Eléctrico'], (2.5, 1.5, 2.3), (1.35, -0.02, 0.50), 0.0),
        'lamina_motor_despiece': (['Motor M15A'], (3.4, 1.9, 2.4), (1.75, -0.2, 1.4), 1.0),
        'lamina_suspension': (['Suspensión y dirección', 'Frenos', 'Ruedas'], (3.6, 3.6, 2.2), (0.0, 0, 0.35), 0.0),
        'lamina_frenos': (['Frenos'], (2.2, 2.6, 1.3), (0.6, 0, 0.55), 0.0),
        'lamina_interior': (['Interior', 'Suspensión y dirección'], (2.0, 2.6, 2.6), (0.1, 0, 0.6), 0.0),
        'lamina_combustible': (['Combustible y escape', 'Ruedas'], (3.0, 4.0, 1.8), (-0.3, 0, 0.25), 0.0),
        'lamina_carroceria': (['Carrocería', 'Puertas y cristales', 'Iluminación'], (6.5, 6.0, 3.6), (0.1, 0, 0.8), 1.0),
    }
    for nombre, (solo, loc, tgt, de) in lam.items():
        foto(nombre, loc, tgt, solo=solo, despiece=de)
    for o in scene.objects:
        if 'pid' in o:
            o.location = (0, 0, 0)
            o.hide_render = False
    print('láminas en', LAM)
