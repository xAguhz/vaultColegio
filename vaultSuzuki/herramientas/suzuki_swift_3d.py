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

El perfil, las ventanillas, las puertas y las ópticas se midieron sobre una foto
lateral del auto; el ancho a lo largo y la caída de los costados, sobre vistas de
frente, cola y planta generadas con Gemini (Adjuntos/Gemini). Cotas del catálogo
japonés (1.5XS, DBA-ZC21S): largo 3755, ancho 1690, alto
1510, distancia entre ejes 2390, despeje 140 mm; neumáticos 185/60R15. Datos y ubicación de la
mecánica del manual de taller (RS415 en inglés y la edición en castellano de 2005):
escape y catalizador adelante, admisión atrás, piezas internas con sus medidas. La forma de la
carrocería sigue esas referencias, pero no es un relevamiento del auto.

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
    'vidrio': mat('Cristal', srgb('#25313a'), 0.0, 0.05, alpha=0.55),
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
        antes = set(self.bm.faces)
        self.bm.from_mesh(me)
        self._tag([f for f in self.bm.faces if f not in antes], m)
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
    antes = set(part.bm.faces)
    part.bm.from_mesh(me)
    for f in [f for f in part.bm.faces if f not in antes]:
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

# ================================================================ materiales extra
M.update({
    'bajos': mat('Bajos (antióxido)', srgb('#2a2c2f'), 0.1, 0.8),
    'ambar': mat('Ámbar', srgb('#e08a1e'), 0.1, 0.2, alpha=0.85),
    'reflector': mat('Reflector cromado', srgb('#e6e8ea'), 1.0, 0.08),
    'placa': mat('Patente', srgb('#f2f2ee'), 0.0, 0.4),
    'blanco_luz': mat('Lente cristal', srgb('#f4f6f7'), 0.0, 0.1, alpha=0.6),
    'gris_trim': mat('Plástico gris', srgb('#55585c'), 0.0, 0.6),
    'cuero': mat('Volante (uretano)', srgb('#202124'), 0.0, 0.55),
    'alfombra': mat('Alfombra', srgb('#2f3033'), 0.0, 0.95),
    'tela': mat('Tela del asiento', srgb('#4a4d53'), 0.0, 0.95),
    'aguja': mat('Aguja roja', srgb('#e5462c'), 0.0, 0.4),
})


# ================================================================ helpers geométricos extra
def merge(self, other, mtx=None):
    """Agrega otra pieza armada en coordenadas locales, transformada con mtx."""
    if mtx is not None:
        bmesh.ops.transform(other.bm, matrix=mtx, verts=other.bm.verts)
    me = bpy.data.meshes.new('tmp_merge')
    other.bm.to_mesh(me)
    for m in other.mats:
        me.materials.append(m)
    self.add_mesh(me)
    bpy.data.meshes.remove(me)
    other.bm.free()
    return self


def ellip(self, center, radii, m, rot=None, segs=24, rings=12):
    """Elipsoide (esfera escalada y rotada)."""
    rot = rot or Matrix.Identity(3)
    mtx = Matrix.Translation(Vector(center)) @ rot.to_4x4() @ Matrix.Diagonal((*radii, 1))

    def build():
        bmesh.ops.create_uvsphere(self.bm, u_segments=segs, v_segments=rings, radius=1.0, matrix=mtx)
    self._tag(self._new(build), m)
    return self


def rbox(self, center, size, r, m, rot=None, seg=2):
    """Caja con aristas redondeadas (radio r)."""
    rot = rot or Matrix.Identity(3)
    tmp = bmesh.new()
    bmesh.ops.create_cube(tmp, size=1.0)
    bmesh.ops.scale(tmp, vec=Vector(size), verts=tmp.verts)
    r = min(r, min(size) * 0.45)
    try:
        bmesh.ops.bevel(tmp, geom=list(tmp.edges) + list(tmp.verts), offset=r, segments=seg, profile=0.5,
                        affect='EDGES', clamp_overlap=True)
    except TypeError:
        bmesh.ops.bevel(tmp, geom=list(tmp.edges) + list(tmp.verts), offset=r, segments=seg, profile=0.5,
                        vertex_only=False, clamp_overlap=True)
    bmesh.ops.transform(tmp, matrix=Matrix.Translation(Vector(center)) @ rot.to_4x4(), verts=tmp.verts)
    me = bpy.data.meshes.new('tmp_rbox')
    tmp.to_mesh(me)
    tmp.free()
    antes = set(self.bm.faces)
    self.bm.from_mesh(me)
    i = self._mi(m)
    for f in [f for f in self.bm.faces if f not in antes]:
        f.material_index = i
    bpy.data.meshes.remove(me)
    return self


def lathe_z(self, center, prof, m, mtx=None, segs=48):
    """Sólido de revolución alrededor del eje Z local; prof = [(radio, z)] abierto o cerrado.
    mtx orienta y ubica la pieza (si falta, solo se traslada a center)."""
    tmp = P()
    rings = []

    def build():
        for i in range(segs):
            a = 2 * math.pi * i / segs
            rings.append([tmp.bm.verts.new((r * math.cos(a), r * math.sin(a), z)) for r, z in prof])
        n = len(prof)
        for i in range(segs):
            A, B = rings[i], rings[(i + 1) % segs]
            for j in range(n - 1):
                tmp.bm.faces.new((A[j], A[j + 1], B[j + 1], B[j]))
    tmp._tag(tmp._new(build), m)
    self.merge(tmp, (mtx if mtx is not None else Matrix.Identity(4)) if center is None
               else Matrix.Translation(Vector(center)) @ (mtx if mtx is not None else Matrix.Identity(4)))
    return self


Part.merge = merge
Part.ellip = ellip
Part.rbox = rbox
Part.lathe_z = lathe_z


def eje_a(v):
    """Matriz 4x4 que lleva el eje Z local a la dirección v."""
    return Vector((0, 0, 1)).rotation_difference(Vector(v).normalized()).to_matrix().to_4x4()


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




# ================================================================ cotas generales
WB = 2.390                 # distancia entre ejes
XF, XR = WB / 2, -WB / 2   # eje delantero y trasero
TF, TR = 1.470, 1.475      # trochas (aprox.)
YF, YR = TF / 2, TR / 2
R_RUEDA = (0.381 + 2 * 0.185 * 0.60) / 2   # 185/60R15 → 0,3015 m
ZA = R_RUEDA               # altura de los ejes (con el auto apoyado)
X_NARIZ, X_COLA = 1.935, -1.820   # 3755 mm de largo
ESP = 0.012                # espesor que se le da a la chapa del modelo
GAP = 0.0035               # luz entre paneles (puertas, capó, portón)

# ---------------------------------------------------------------- foto de perfil → metros
# Las cotas de perfil se midieron sobre la foto lateral de referencia (agrandada al doble):
# ejes en x=197 y x=980 px, piso en y=700 px, 3,04 mm por px en alto. Los voladizos se
# estiran para llegar al largo del catálogo (3755 mm).
_FX = [(0, X_NARIZ), (197, XF), (980, XR), (1133, X_COLA)]


def px(x2):
    for (a0, b0), (a1, b1) in zip(_FX[:-1], _FX[1:]):
        if x2 <= a1 or (a1, b1) == _FX[-1]:
            return b0 + (b1 - b0) * (x2 - a0) / (a1 - a0)


def pz(y2):
    return (700 - y2) * 0.00304


def foto(pts):
    return [(px(x), pz(y)) for x, y in pts]


def cr(keys, x):
    """Interpolación suave (Hermite con limitador) sobre puntos clave (x, valor)."""
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


# Silueta superior medida sobre la foto (x, z) en metros
K_TECHO = [(-1.825, 0.56), (-1.81, 0.69), (-1.76, 0.83), (-1.71, 0.94), (-1.66, 1.02), (-1.60, 1.08),
           (-1.52, 1.17), (-1.42, 1.27), (-1.34, 1.36), (-1.29, 1.435), (-1.22, 1.458), (-1.00, 1.476),
           (-0.80, 1.496), (-0.50, 1.508), (-0.30, 1.514), (0.0, 1.508), (0.15, 1.49), (0.30, 1.468),
           (0.40, 1.44), (0.47, 1.404), (0.55, 1.36), (0.65, 1.29), (0.73, 1.235), (0.80, 1.186),
           (0.88, 1.13), (0.95, 1.088), (1.02, 1.052), (1.10, 1.022), (1.20, 1.003), (1.30, 0.985),
           (1.43, 0.96), (1.52, 0.936), (1.61, 0.906), (1.70, 0.866), (1.76, 0.832), (1.80, 0.79),
           (1.85, 0.735), (1.89, 0.668), (1.918, 0.61), (1.935, 0.55)]
K_PISO = [(-1.825, 0.36), (-1.79, 0.31), (-1.70, 0.292), (-1.60, 0.285), (-1.45, 0.24), (1.45, 0.232),
          (1.58, 0.245), (1.80, 0.258), (1.90, 0.285), (1.935, 0.32)]
# línea de cintura (borde de abajo de los vidrios), medida sobre la foto
K_CINTURA = [(-1.825, 1.00), (-1.60, 1.06), (-1.35, 1.09), (-1.134, 1.119), (-0.89, 1.10), (-0.157, 1.058),
             (0.76, 1.018), (0.96, 1.03), (1.30, 0.96), (1.60, 0.88), (1.85, 0.75), (1.935, 0.60)]
# planta: ancho relativo (vista superior de referencia) × semiancho máximo 0,845 m
K_PLANTA = [(-1.825, 0.30), (-1.80, 0.64), (-1.741, 0.81), (-1.662, 0.905), (-1.583, 0.957), (-1.505, 0.98),
            (-1.33, 1.0), (1.41, 1.0), (1.484, 0.99), (1.563, 0.966), (1.642, 0.927), (1.721, 0.861),
            (1.80, 0.759), (1.879, 0.58), (1.935, 0.36)]
# semiancho del techo / borde superior de los vidrios (vista de frente y de cola)
K_TECHO_ANCHO = [(-1.825, 0.42), (-1.60, 0.58), (-1.40, 0.54), (-1.20, 0.50), (-0.50, 0.49), (0.0, 0.49),
                 (0.40, 0.50), (0.70, 0.58), (0.96, 0.66), (1.20, 0.66), (1.935, 0.42)]
W_MAX = 0.845
M_HALF = 36     # puntos por media sección


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
    """Media sección (y >= 0) desde abajo en el centro hasta arriba en el centro.
    La forma lateral (panza, hombro y caída de los vidrios) sale de la vista de frente de referencia."""
    zb, zt = cr(K_PISO, x), cr(K_TECHO, x)
    w = W_MAX * cr(K_PLANTA, x)
    zc = min(cr(K_CINTURA, x), zt - 0.05)
    h = zt - zc
    k = max(0.0, min(1.0, (h - 0.03) / 0.22))
    wr = min(cr(K_TECHO_ANCHO, x), 0.86 * w)
    wt = 0.80 * w * (1 - k) + wr * k
    L = zc - zb
    pts = [(0.0, zb), (0.80 * w, zb), (0.95 * w, zb + 0.012), (0.985 * w, zb + 0.15 * L), (w, zb + 0.45 * L),
           (0.975 * w, zb + 0.72 * L), (0.905 * w, zc),
           (wt + 0.06 * k, zt - 0.065 * k - 0.014 * (1 - k)), (wt * 0.62, zt - 0.006), (0.0, zt)]
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
        fino = (x < X_COLA + 0.10) or (x > X_NARIZ - 0.12)
        x += 0.007 if fino else 0.028
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
    # piso: las caras que miran hacia abajo van con pintura de bajos
    for f in bm.faces:
        f.material_index = 2 if (f.normal.z < -0.6 and f.calc_center_median().z < 0.40) else 0
    me = bpy.data.meshes.new('carroceria_solida')
    bm.to_mesh(me)
    bm.free()
    for m in (M['pintura'], M['interior_chapa'], M['bajos']):
        me.materials.append(m)
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


def offset_poly(pts, d):
    """Agranda (d > 0) un polígono cerrado moviendo cada vértice por la bisectriz."""
    n = len(pts)
    area = sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n))
    s = 1 if area > 0 else -1
    out = []
    for i in range(n):
        p0, p1, p2 = Vector(pts[i - 1]), Vector(pts[i]), Vector(pts[(i + 1) % n])
        e1, e2 = (p1 - p0).normalized(), (p2 - p1).normalized()
        n1, n2 = Vector((e1.y, -e1.x)) * s, Vector((e2.y, -e2.x)) * s
        b = (n1 + n2)
        if b.length < 1e-6:
            b = n1
        b.normalize()
        k = 1.0 / max(0.35, b.dot(n1))
        q = p1 + b * d * k
        out.append((q.x, q.y))
    return out


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


def cilindro_cut(name, cx, cz, r, y0, y1, n=64, plano='XZ'):
    pts = [(cx + r * math.cos(2 * math.pi * i / n), cz + r * math.sin(2 * math.pi * i / n)) for i in range(n)]
    return prisma(name, pts, plano, y0, y1)


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


def cortador(name, a, b, op='INTERSECT'):
    """Combina dos prismas en un cortador nuevo (intersección o unión)."""
    ob = bpy.data.objects.new('c_' + name, booleana(a, [b], op))
    CUT_COLL.objects.link(ob)
    return ob


def ob_de(me, name='tmp_ob'):
    ob = bpy.data.objects.new(name, me)
    CUT_COLL.objects.link(ob)
    return ob


def separar(cuerpo, cutter, hueco=None):
    """Saca de la carrocería la parte que queda dentro del cortador y devuelve su malla.
    Si se da 'hueco' (el mismo cortador agrandado), la carrocería pierde un poco más:
    así queda la luz entre el panel y el resto, como en el auto."""
    pieza = booleana(cuerpo, [cutter], 'INTERSECT')
    resto = booleana(cuerpo, [hueco or cutter], 'DIFFERENCE')
    old = cuerpo.data
    cuerpo.data = resto
    bpy.data.meshes.remove(old)
    return pieza


def partir(me, cutter):
    """Divide una malla en (adentro, afuera) del cortador."""
    ob = ob_de(me)
    a = booleana(ob, [cutter], 'INTERSECT')
    b = booleana(ob, [cutter], 'DIFFERENCE')
    bpy.data.objects.remove(ob)
    return a, b


def prisma_gap(name, pts, plano, a0, a1):
    """Prisma exacto y su versión agrandada GAP (para la luz entre paneles)."""
    return prisma(name, pts, plano, a0, a1), prisma(name + '_h', offset_poly(pts, GAP), plano, a0, a1)


# ================================================================ CARROCERÍA
cuerpo = carroceria_base()

# ---------- pasaruedas (radio medido en la foto: 0,375 adelante y 0,385 atrás)
arcos = None
for xa, r in ((XF, 0.375), (XR, 0.385)):
    for s in (1, -1):
        c = cilindro_cut(f'arco{xa:.1f}{s}', xa, ZA, r, 0.46 if s > 0 else -1.0, 1.0 if s > 0 else -0.46)
        arcos = c if arcos is None else cortador('arcos', arcos, c, 'UNION')
me = booleana(cuerpo, [arcos], 'DIFFERENCE')
old = cuerpo.data
cuerpo.data = me
bpy.data.meshes.remove(old)

# ---------- parabrisas (con banda negra serigrafiada en el borde)
banda = [(0.44, 1.30), (0.975, 0.96), (0.975, 1.30), (0.44, 1.62)]
plan_pb = [(0.975, -0.64), (0.975, 0.64), (0.43, 0.485), (0.43, -0.485)]
c_pb = cortador('pb', prisma('pb_a', banda, 'XZ', -1, 1), prisma('pb_b', plan_pb, 'XY', 0, 2))
c_pb_in = cortador('pb_in', prisma('pbi_a', banda, 'XZ', -1, 1),
                   prisma('pbi_b', offset_poly(plan_pb, -0.035), 'XY', 0, 2))
para = separar(cuerpo, c_pb)
para_vidrio, para_borde = partir(para, c_pb_in)

# ---------- faros (perfil medido en la foto; solo en los costados del frente)
FARO = foto([(12, 478), (30, 440), (70, 420), (118, 410), (114, 426), (80, 446), (46, 476), (24, 498)])
faros = {}
for lado, (y0, y1) in (('izq', (0.40, 1.0)), ('der', (-1.0, -0.40))):
    faros[lado] = separar(cuerpo, prisma('faro' + lado, FARO, 'XZ', y0, y1))

# ---------- calaveras (vista de cola ∩ vista lateral)
CAL_LADO = [(-1.338, 1.082), (-2.0, 1.082), (-2.0, 0.73), (-1.67, 0.73), (-1.521, 0.973), (-1.358, 0.997)]
calaveras = {}
for lado, s in (('izq', 1), ('der', -1)):
    cola = [(s * 0.62, 1.07), (s * 0.75, 1.07), (s * 0.86, 0.73), (s * 0.515, 0.73)]
    c = cortador('cal' + lado, prisma('cal_a' + lado, CAL_LADO, 'XZ', -1, 1), prisma('cal_b' + lado, cola, 'YZ', -2.2, -1.2))
    calaveras[lado] = separar(cuerpo, c)

# ---------- parrilla, toma inferior y nichos de antinieblas (medidos en la vista de frente)
c_par = caja_cut('parr', 1.80, 2.1, -0.42, 0.42, 0.576, 0.717)
c_toma = caja_cut('toma', 1.80, 2.1, -0.41, 0.41, 0.243, 0.397)
c_fog = cortador('fogs', caja_cut('fogL', 1.62, 2.1, 0.485, 0.705, 0.27, 0.41),
                 caja_cut('fogR', 1.62, 2.1, -0.705, -0.485, 0.27, 0.41), 'UNION')
parrilla = separar(cuerpo, c_par)
toma = separar(cuerpo, c_toma)
nichos = separar(cuerpo, c_fog)

# ---------- tapa de combustible (lado izquierdo, círculo de la foto)
X_TAPA, Z_TAPA = px(1030), pz(420)
c_tapa = cilindro_cut('tapa', X_TAPA, Z_TAPA, 0.074, 0.55, 1.0)
c_tapa_h = cilindro_cut('tapa_h', X_TAPA, Z_TAPA, 0.074 + GAP, 0.55, 1.0)
tapa = separar(cuerpo, c_tapa, c_tapa_h)

# ---------- vidrios laterales (medidos en la foto): marco negro exterior y vidrio interior
DLO_OUT = foto([(272, 364), (447, 231), (918, 231), (928, 250), (920, 330), (908, 338), (804, 342), (650, 347),
                (420, 355), (345, 366)])
VID_DEL = foto([(398, 358), (470, 247), (640, 242), (640, 350)])
VID_TRA = foto([(702, 244), (804, 244), (804, 346), (702, 349)])
VID_FIJO = foto([(814, 244), (895, 244), (910, 258), (906, 333), (814, 342)])
c_dlo = prisma('dlo', DLO_OUT, 'XZ', -1, 1)

# ---------- puertas (polígonos de la foto), con luz entre paneles
PUERTA_D = foto([(318, 596), (322, 372), (345, 366), (460, 236), (656, 233), (656, 596)])
PUERTA_T = foto([(662, 596), (662, 233), (918, 233), (928, 250), (965, 330), (972, 400), (952, 470), (905, 526),
                 (862, 566), (838, 596)])
puertas = {}
for np_, pol, vids in (('del', PUERTA_D, [VID_DEL]), ('tra', PUERTA_T, [VID_TRA, VID_FIJO])):
    for lado, (y0, y1) in (('izq', (0.40, 1.0)), ('der', (-1.0, -0.40))):
        c, ch = prisma_gap(f'p_{np_}_{lado}', pol, 'XZ', y0, y1)
        pieza = separar(cuerpo, c, ch)
        marco_y_vidrio, chapa = partir(pieza, c_dlo)
        vidrios = []
        resto = marco_y_vidrio
        for k, v in enumerate(vids):
            vi, resto = partir(resto, prisma(f'v_{np_}_{lado}{k}', v, 'XZ', y0, y1))
            vidrios.append(vi)
        puertas[(np_, lado)] = (chapa, resto, vidrios)

# ---------- capó (corte por la línea del guardabarros), portón, paragolpes
CAPO = [(0.958, 1.005), (1.20, 0.958), (1.50, 0.872), (1.70, 0.80), (1.85, 0.722), (2.0, 0.70), (2.0, 1.4),
        (0.958, 1.4)]
c, ch = prisma_gap('capo', CAPO, 'XZ', -0.74, 0.74)
capo = separar(cuerpo, c, ch)

PORTON = [(-0.50, 0.655), (0.50, 0.655), (0.53, 1.045), (0.64, 1.075), (0.575, 1.40), (0.46, 1.50),
          (-0.46, 1.50), (-0.575, 1.40), (-0.64, 1.075), (-0.53, 1.045)]
c, ch = prisma_gap('porton', PORTON, 'YZ', -2.2, -1.285)
porton = separar(cuerpo, c, ch)
banda_l = [(-1.25, 1.30), (-1.60, 0.93), (-1.75, 0.93), (-1.75, 1.60), (-1.25, 1.60)]
cola_l = [(-0.645, 1.065), (0.645, 1.065), (0.53, 1.41), (-0.53, 1.41)]
c_lun = cortador('lun', prisma('lun_a', banda_l, 'XZ', -1, 1), prisma('lun_b', cola_l, 'YZ', -2.2, -1.2))
c_lun_in = cortador('lun_in', prisma('luni_a', banda_l, 'XZ', -1, 1),
                    prisma('luni_b', offset_poly(cola_l, -0.03), 'YZ', -2.2, -1.2))
luneta, porton = partir(porton, c_lun)
luneta_vidrio, luneta_borde = partir(luneta, c_lun_in)

PG_DEL = [(1.555, -0.1), (1.555, 0.53), (1.70, 0.60), (1.785, 0.638), (2.1, 0.665), (2.1, -0.1)]
c, ch = prisma_gap('pgdel', PG_DEL, 'XZ', -1.0, 1.0)
pg_del = separar(cuerpo, c, ch)
PG_TRA = [(-1.585, -0.1), (-1.585, 0.55), (-1.66, 0.63), (-1.72, 0.655), (-2.2, 0.655), (-2.2, -0.1)]
c, ch = prisma_gap('pgtra', PG_TRA, 'XZ', -1.0, 1.0)
pg_tra = separar(cuerpo, c, ch)

# ---------- lo que queda del marco negro (parante A) y el casco
parante_a = separar(cuerpo, c_dlo)

# ================================================================ piezas de carrocería
CJ = 'Carrocería'
b = P().add_mesh(cuerpo.data, None).add_mesh(parante_a, M['negro_brillo'])
# guardabarros interiores (negros) en los cuatro pasaruedas
for xa, r in ((XF, 0.375), (XR, 0.385)):
    for s in (1, -1):
        b.tube('Y', (xa, s * 0.66, ZA), r - 0.004, r + 0.012, 0.30, M['bajos'], a0=172, a1=368, segs=56)
# antena en la parte de atrás del techo
xa_, za_ = px(880), cr(K_TECHO, px(880))
b.cyl('Z', (xa_, 0, za_ + 0.008), 0.018, 0.02, M['negro'])
b.barra((xa_, 0, za_ + 0.015), (xa_ - 0.14, 0, za_ + 0.15), 0.0035, M['negro'])
# repetidores de giro en los guardabarros delanteros
for s in (1, -1):
    xr_, zr_ = px(290), pz(437)
    b.ellip((xr_, s * (surf_y(xr_, zr_) + 0.002), zr_), (0.028, 0.006, 0.013), M['ambar'], segs=16, rings=8)
# rejilla del torpedo (entre capó y parabrisas)
b.box(0.93, 0.985, -0.62, 0.62, 1.0, 1.035, M['negro'])
make('casco', 'Casco (carrocería autoportante)', CJ, b, (0, 0, 0), angle=40)

cp = P().add_mesh(capo)
make('capo', 'Capó', CJ, cp, (0.30, 0, 0.85), angle=40)

po = P().add_mesh(porton).add_mesh(luneta_vidrio, M['vidrio']).add_mesh(luneta_borde, M['negro_brillo'])
# alerón de techo con la tercera luz de freno
xs_ = -1.285
po.rbox((xs_, 0, cr(K_TECHO, xs_) + 0.004), (0.10, 0.92, 0.026), 0.011, M['pintura'], rot=Matrix.Rotation(math.radians(-14), 3, 'Y'))
po.rbox((xs_ - 0.048, 0, cr(K_TECHO, xs_) - 0.008), (0.012, 0.30, 0.014), 0.004, M['calavera'])
# manija del portón y limpialuneta
po.rbox((-1.812, 0, 0.705), (0.03, 0.15, 0.04), 0.01, M['cromo'])
xp_ = -1.605
zp_ = cr(K_TECHO, xp_)
xe_ = -1.43
ze_ = seccion(xe_)
ze_ = max(z for (yy, z) in ze_ if abs(yy) <= 0.33) - 0.004
po.barra((xp_, 0.0, zp_ + 0.01), (xe_, 0.32, ze_ + 0.012), 0.006, M['negro'])
po.barra((xp_ + 0.01, 0.02, zp_ + 0.004), (xe_ + 0.01, 0.34, ze_ + 0.006), 0.004, M['goma'])
po.cyl('Z', (xp_, 0.0, zp_ + 0.005), 0.02, 0.03, M['negro'])
make('porton', 'Portón trasero con luneta', CJ, po, (-0.70, 0, 0.40), angle=40)

pd = P().add_mesh(pg_del)
# patente delantera (japonesa: 330 × 165 mm), sobre el paragolpes
pd.rbox((X_NARIZ + 0.004, 0, 0.495), (0.008, 0.33, 0.165), 0.008, M['placa'])
pd.box(X_NARIZ - 0.004, X_NARIZ + 0.001, -0.18, 0.18, 0.40, 0.59, M['negro'])
make('paragolpes_del', 'Paragolpes delantero', CJ, pd, (0.75, 0, -0.05), angle=40)

pt = P().add_mesh(pg_tra)
pt.box(X_COLA - 0.006, X_COLA + 0.01, -0.19, 0.19, 0.38, 0.58, M['gris_trim'])          # nicho de la patente
pt.rbox((X_COLA - 0.009, 0, 0.48), (0.008, 0.33, 0.165), 0.008, M['placa'])
make('paragolpes_tra', 'Paragolpes trasero', CJ, pt, (-0.75, 0, -0.05), angle=40)

pr = P().add_mesh(parrilla, M['negro']).add_mesh(toma, M['negro']).add_mesh(nichos, M['negro'])
# panal de la parrilla: celdas hexagonales; toma inferior: tres barras
for i in range(-9, 10):
    for j in range(3):
        y = i * 0.042 + (0.021 if j % 2 else 0)
        if abs(y) < 0.38:
            pr.cyl('X', (1.905 - 0.03 * (abs(y) / 0.42) ** 2, y, 0.60 + j * 0.04), 0.017, 0.012, M['negro_brillo'], segs=6)
for k in range(3):
    pr.box(1.885, 1.925, -0.39, 0.39, 0.27 + k * 0.045, 0.285 + k * 0.045, M['negro_brillo'])
make('parrilla', 'Parrilla, toma inferior y nichos de antinieblas', CJ, pr, (1.10, 0, 0.05), angle=40)

tp = P().add_mesh(tapa)
make('tapa_combustible', 'Tapa de combustible', CJ, tp, (-0.10, 0.45, 0.05), angle=40)

# ================================================================ PUERTAS Y CRISTALES
CJ = 'Puertas y cristales'
for (np_, lado), (chapa, marco, vidrios) in puertas.items():
    s = 1 if lado == 'izq' else -1
    pp = P().add_mesh(chapa).add_mesh(marco, M['negro_brillo'])
    for v in vidrios:
        pp.add_mesh(v, M['vidrio'])
    # manija (medida en la foto)
    xh, zh = (px(617), pz(388)) if np_ == 'del' else (px(907), pz(377))
    yh = surf_y(xh, zh)
    pp.rbox((xh, s * (yh + 0.012), zh), (0.13, 0.022, 0.024), 0.01, M['cromo'])
    pp.rbox((xh + 0.055, s * (yh + 0.006), zh), (0.035, 0.014, 0.03), 0.006, M['pintura'])     # cilindro de la cerradura
    if np_ == 'tra':
        xb = px(809)
        pp.box(xb - 0.012, xb + 0.012, s * (surf_y(xb, 1.25) - 0.004), s * (surf_y(xb, 1.25) + 0.006), pz(345), pz(244),
               M['negro_brillo'])                                                            # parante del vidrio fijo
    if np_ == 'del':
        # espejo retrovisor: base en el triángulo negro y carcasa redondeada
        xm, zm = px(385), pz(348)
        ym = surf_y(xm, zm)
        rz = Matrix.Rotation(math.radians(5 * s), 3, 'Z')
        pp.rbox((xm + 0.03, s * (ym + 0.012), zm - 0.01), (0.10, 0.03, 0.07), 0.012, M['negro'])        # base
        pp.rbox((xm + 0.01, s * (ym + 0.045), zm), (0.05, 0.05, 0.03), 0.01, M['negro'])                 # brazo
        pp.rbox((xm, s * 0.80, zm + 0.02), (0.085, 0.19, 0.115), 0.035, M['pintura'], rot=rz, seg=3)    # carcasa
        pp.rbox((xm - 0.043, s * 0.80, zm + 0.02), (0.006, 0.165, 0.092), 0.02, M['cromo'], rot=rz)      # espejo
        nombre = f"Puerta delantera {'izquierda' if s > 0 else 'derecha (conductor)'}"
    else:
        nombre = f"Puerta trasera {'izquierda' if s > 0 else 'derecha'}"
    dx = 0.15 if np_ == 'del' else -0.15
    make(f'puerta_{np_}_{lado}', nombre, CJ, pp, (dx, s * 0.90, 0.05), angle=40)

make('parabrisas', 'Parabrisas laminado', CJ, P().add_mesh(para_vidrio, M['vidrio']).add_mesh(para_borde, M['negro_brillo']),
     (0.40, 0, 0.65), angle=40)

wp = P()
for yy, L, a in ((-0.47, 0.60, 4), (0.10, 0.50, 8)):
    rot = Matrix.Rotation(math.radians(a), 3, 'Z') @ Matrix.Rotation(math.radians(-30), 3, 'Y')
    base = Vector((0.955, yy, 1.04))
    wp.cyl('Z', base, 0.016, 0.03, M['negro'])
    wp.obox(base + rot @ Vector((0, L / 2, 0)) + Vector((-0.02, 0, 0.012)), (0.012, L * 0.95, 0.008), rot, M['negro'])
    wp.obox(base + rot @ Vector((-0.012, L / 2 + 0.02, 0)) + Vector((-0.02, 0, 0.02)), (0.008, L * 0.98, 0.016), rot,
            M['goma'])
make('limpiaparabrisas', 'Limpiaparabrisas', CJ, wp, (0.30, 0, 0.80))

# ================================================================ ILUMINACIÓN
CJ = 'Iluminación'
for lado, s in (('izq', 1), ('der', -1)):
    f = P().add_mesh(faros[lado], M['blanco_luz'])
    # interior del faro: carcasa negra, dos parábolas cromadas (alta y baja) y el giro ámbar
    for (xc, zc, r) in ((1.76, 0.745, 0.058), (1.655, 0.79, 0.045)):
        yc = s * (surf_y(xc, zc) - 0.07)
        f.lathe_z(None, [(0.004, -0.045), (r * 0.55, -0.03), (r * 0.9, -0.01), (r, 0.0)], M['reflector'],
                  mtx=Matrix.Translation((xc, yc, zc)) @ eje_a((0.75, s * 0.55, 0.12)), segs=28)
        f.ellip((xc, yc, zc), (0.012, 0.012, 0.012), M['blanco_luz'], segs=10, rings=6)
    xg, zg = 1.58, 0.84
    f.ellip((xg, s * (surf_y(xg, zg) - 0.03), zg), (0.05, 0.02, 0.016), M['ambar'], segs=14, rings=7)
    make(f'faro_{lado}', f"Faro delantero {'izquierdo' if s > 0 else 'derecho'}", CJ, f, (0.50, s * 0.50, 0.25), angle=40)

    # sectores de la calavera (referencia de cola): abajo marcha atrás, al medio giro ámbar, arriba rojo
    blanco, resto = partir(calaveras[lado], caja_cut('cb' + lado, -2.2, -1.2, -1.0, 1.0, 0.70, 0.815))
    ambar, rojo = partir(resto, caja_cut('ca' + lado, -2.2, -1.2, -1.0, 1.0, 0.815, 0.905))
    c = P().add_mesh(rojo, M['calavera']).add_mesh(ambar, M['ambar']).add_mesh(blanco, M['blanco_luz'])
    make(f'calavera_{lado}', f"Calavera (luz trasera) {'izquierda' if s > 0 else 'derecha'}", CJ, c, (-0.50, s * 0.50, 0.25),
         angle=40)

    fg = P()
    fg.lathe_z(None, [(0.0, 0.0), (0.045, 0.0), (0.05, -0.02), (0.05, -0.05)], M['reflector'],
               mtx=Matrix.Translation((1.84, s * 0.595, 0.34)) @ eje_a((1, s * 0.25, 0)), segs=28)
    fg.ellip((1.842, s * 0.595, 0.34), (0.008, 0.044, 0.044), M['blanco_luz'], rot=Matrix.Rotation(math.radians(14 * s), 3, 'Z'))
    make(f'antiniebla_{lado}', f"Faro antiniebla {'izquierdo' if s > 0 else 'derecho'}", CJ, fg, (0.80, s * 0.35, -0.05))


# ================================================================ helpers de piezas
def fuelle(part, p0, p1, r0, r1, pliegues, m, segs=24):
    """Fuelle de goma (homocinéticas, cremallera): sólido de revolución con pliegues."""
    p0, p1 = Vector(p0), Vector(p1)
    L = (p1 - p0).length
    prof = [(0.0, 0.0)]
    n = pliegues * 2
    for i in range(n + 1):
        t = i / n
        r = r0 + (r1 - r0) * t
        prof.append((r * (1.0 if i % 2 == 0 else 0.82), L * t))
    prof.append((0.0, L))
    part.lathe_z(None, prof, m, mtx=Matrix.Translation(p0) @ eje_a(p1 - p0), segs=segs)
    return part


Part.fuelle = fuelle

# ================================================================ RUEDAS
CJ = 'Ruedas'
# neumático 185/60R15: perfil con hombros redondeados y 4 surcos en la banda de rodamiento
R_T = R_RUEDA
TIRE = [(0.1915, -0.080), (0.200, -0.090), (0.235, -0.0935), (0.270, -0.091), (0.290, -0.084), (0.298, -0.072),
        (R_T, -0.060)]
for g in (-0.042, -0.014, 0.014, 0.042):          # surcos
    TIRE += [(R_T, g - 0.006), (R_T - 0.008, g - 0.005), (R_T - 0.008, g + 0.005), (R_T, g + 0.006)]
TIRE += [(R_T, 0.060), (0.298, 0.072), (0.290, 0.084), (0.270, 0.091), (0.235, 0.0935), (0.200, 0.090), (0.1915, 0.080)]
for eje, xa, ya in (('del', XF, YF), ('tra', XR, YR)):
    for lado, s in (('izq', 1), ('der', -1)):
        w = P().lathe((xa, s * ya, ZA), TIRE, M['goma'], sign=s, segs=64)
        # llanta 15 × 5½ JJ: aro con pestaña, cara cóncava, 6 rayos, tapa central y 4 tuercas
        w.lathe((xa, s * ya, ZA), [(0.168, -0.072), (0.1905, -0.072), (0.1985, -0.068), (0.1985, -0.060), (0.188, -0.058),
                                   (0.188, 0.058), (0.1985, 0.060), (0.1985, 0.068), (0.1905, 0.072), (0.168, 0.072)],
                M['llanta'], sign=s, segs=64)
        cara = s * (ya + 0.035)
        w.cyl('Y', (xa, cara, ZA), 0.072, 0.03, M['llanta'])
        w.cyl('Y', (xa, s * (ya + 0.051), ZA), 0.032, 0.006, M['acero_osc'])              # tapa central
        for k in range(4):                                                                 # tuercas (4 × 100)
            a = 2 * math.pi * k / 4 + math.pi / 4
            w.cyl('Y', (xa + 0.05 * math.cos(a), s * (ya + 0.05), ZA + 0.05 * math.sin(a)), 0.0095, 0.018, M['cromo'], segs=6)
        for k in range(6):
            a = 2 * math.pi * k / 6
            rot = Matrix.Rotation(-a, 3, 'Y')
            for r0, r1, wd, dy in ((0.07, 0.13, 0.044, 0.0), (0.13, 0.172, 0.034, -0.012)):
                c = Vector((xa, cara + s * dy, ZA)) + rot @ Vector(((r0 + r1) / 2, 0, 0))
                w.obox(c, (r1 - r0 + 0.01, 0.026, wd), rot, M['llanta'])
        w.tube('Y', (xa, s * (ya + 0.04), ZA), 0.168, 0.182, 0.02, M['llanta'])
        nombre = f"Rueda {'delantera' if eje == 'del' else 'trasera'} {'izquierda' if s > 0 else 'derecha'}"
        make(f'rueda_{eje}_{lado}', nombre, CJ, w, (0, s * 1.00, 0), angle=40)

# ================================================================ FRENOS
CJ = 'Frenos'
for lado, s in (('izq', 1), ('der', -1)):
    yd = s * (YF - 0.055)
    d = P()
    # disco ventilado: dos pistas de 6 mm con aletas entre medio y la "campana" del cubo
    d.tube('Y', (XF, yd - s * 0.007, ZA), 0.085, 0.1275, 0.006, M['disco'], segs=56)
    d.tube('Y', (XF, yd + s * 0.007, ZA), 0.085, 0.1275, 0.006, M['disco'], segs=56)
    for k in range(30):
        a = 2 * math.pi * k / 30
        rot = Matrix.Rotation(-a, 3, 'Y')
        d.obox(Vector((XF, yd, ZA)) + rot @ Vector((0.106, 0, 0)), (0.04, 0.008, 0.004), rot, M['fundicion'])
    d.lathe((XF, yd, ZA), [(0.03, 0.006), (0.085, 0.006), (0.085, 0.035), (0.075, 0.04), (0.03, 0.04)], M['disco'], sign=s)
    make(f'disco_{lado}', f"Disco de freno ventilado {'izquierdo' if s > 0 else 'derecho'}", CJ, d, (0.0, s * 0.65, 0.28))

    c = P()
    ang = math.radians(160)
    cc = Vector((XF + 0.112 * math.cos(ang), yd, ZA + 0.112 * math.sin(ang)))
    rot = Matrix.Rotation(-(ang - math.pi), 3, 'Y')
    c.rbox(cc + Vector((0, -s * 0.024, 0)), (0.07, 0.045, 0.15), 0.012, M['caliper'], rot=rot)          # cuerpo con pistón
    c.rbox(cc + Vector((0, s * 0.02, 0)), (0.05, 0.022, 0.12), 0.008, M['caliper'], rot=rot)            # puente exterior
    c.rbox(cc + Vector((0.035, -s * 0.03, 0)), (0.03, 0.05, 0.20), 0.006, M['acero_osc'], rot=rot)      # soporte
    for dz in (-0.055, 0.055):                                                                           # guías
        c.cyl('Y', cc + rot @ Vector((0, 0, dz)) + Vector((0, -s * 0.05, 0)), 0.009, 0.03, M['goma'])
    c.cyl('Y', cc + Vector((0, -s * 0.047, 0)), 0.006, 0.01, M['cromo'])                                # purgador
    c.curve([tuple(cc + Vector((0, -s * 0.05, 0.03))), tuple(cc + Vector((0.05, -s * 0.12, 0.10))),
             (XF - 0.05, s * 0.50, 0.55)], 0.006, M['negro'])                                            # flexible
    make(f'mordaza_{lado}', f"Mordaza (caliper) delantera {'izquierda' if s > 0 else 'derecha'}", CJ, c, (-0.28, s * 0.58, 0.38))

    t = P()
    yt = s * (YR - 0.06)
    prof = [(0.03, -0.028), (0.122, -0.028), (0.122, 0.0)]
    for k in range(5):                                       # aletas de refrigeración del tambor
        prof += [(0.122, 0.004 + k * 0.009), (0.128, 0.006 + k * 0.009), (0.128, 0.009 + k * 0.009)]
    prof += [(0.122, 0.05), (0.06, 0.05), (0.05, 0.03), (0.03, 0.03)]
    t.lathe((XR, yt, ZA), prof, M['fundicion'], sign=s, segs=48)
    t.cyl('Y', (XR, s * (YR - 0.096), ZA), 0.125, 0.006, M['acero_osc'])                                # plato portazapatas
    t.cyl('X', (XR, s * (YR - 0.105), ZA + 0.09), 0.012, 0.05, M['acero'])                              # bombín
    t.curve([(XR, s * (YR - 0.11), ZA + 0.09), (XR + 0.15, s * (YR - 0.2), ZA + 0.05), (XR + 0.5, s * 0.45, 0.22)],
            0.003, M['acero'])                                                                           # caño de freno
    t.curve([(XR - 0.02, s * (YR - 0.11), ZA - 0.08), (XR + 0.3, s * 0.55, 0.20), (-0.3, s * 0.08, 0.30)], 0.0035,
            M['acero_osc'])                                                                              # cable del freno de mano
    make(f'tambor_{lado}', f"Freno a tambor trasero {'izquierdo' if s > 0 else 'derecho'}", CJ, t, (0, s * 0.65, 0.28))

sf = P()
sf.lathe_z(None, [(0.0, 0.0), (0.108, 0.0), (0.116, 0.025), (0.116, 0.085), (0.108, 0.11), (0.0, 0.11)], M['acero_osc'],
           mtx=Matrix.Translation((0.985, -0.40, 0.82)) @ eje_a((1, 0, 0.05)), segs=40)
sf.cyl('X', (1.16, -0.40, 0.83), 0.025, 0.13, M['aluminio'])                                         # bomba de freno
sf.rbox((1.15, -0.40, 0.89), (0.10, 0.07, 0.07), 0.015, M['bateria'])                                 # depósito
sf.cyl('Z', (1.15, -0.40, 0.935), 0.02, 0.02, M['amarillo'])
for dy in (-0.012, 0.012):
    sf.curve([(1.20, -0.40 + dy, 0.82), (1.28, -0.47 + dy, 0.80), (1.33, -0.52 + dy, 0.74)], 0.003, M['acero'])
sf.cyl('X', (0.96, -0.40, 0.82), 0.012, 0.05, M['acero'])                                             # varilla al pedal
make('servofreno', 'Servofreno, bomba y depósito de freno', CJ, sf, (0.25, -0.35, 1.05))

ab = P()
ab.rbox((1.34, -0.56, 0.72), (0.11, 0.09, 0.08), 0.01, M['aluminio'])                                 # bloque hidráulico
ab.cyl('Z', (1.34, -0.56, 0.79), 0.035, 0.07, M['acero_osc'])                                         # motor de la bomba
ab.rbox((1.34, -0.505, 0.72), (0.10, 0.025, 0.07), 0.008, M['negro'])                                  # módulo de control
for k, (dx, tgt) in enumerate(((-0.03, (XF, 0.55, 0.55)), (0.0, (XF, -0.55, 0.55)), (0.03, (-0.3, 0.0, 0.25)))):
    ab.curve([(1.34 + dx, -0.56, 0.765), (1.30 + dx, -0.45, 0.74), tgt], 0.0028, M['acero'])
make('abs', 'Unidad de ABS (hidráulica y control)', CJ, ab, (0.30, -0.55, 0.90))
se = P()
for xa, ya, tr in ((XF, YF, 'del'), (XR, YR, 'tra')):
    for s in (1, -1):
        yr_ = s * (ya - 0.10)
        se.tube('Y', (xa, yr_, ZA), 0.040, 0.048, 0.008, M['acero_osc'], segs=40)                    # anillo dentado
        ps = Vector((xa - 0.03, yr_ - s * 0.01, ZA + 0.055))
        se.cyl('Z', ps, 0.009, 0.04, M['negro'])                                                        # sensor
        se.curve([tuple(ps + Vector((0, 0, 0.02))), (xa - 0.05, s * (ya - 0.20), 0.55), (xa - 0.10, s * 0.50, 0.75)],
                 0.0035, M['negro'])
make('sensores_abs', 'Sensores de velocidad de rueda y anillos del ABS', CJ, se, (0, 0, -0.35))

fm = P()
fm.rbox((0.05, 0.0, 0.40), (0.30, 0.035, 0.05), 0.012, M['negro'], rot=Matrix.Rotation(math.radians(-18), 3, 'Y'))
fm.rbox((0.21, 0.0, 0.448), (0.05, 0.03, 0.03), 0.01, M['cromo'])
fm.rbox((-0.08, 0.0, 0.36), (0.08, 0.08, 0.06), 0.01, M['acero_osc'])
make('freno_mano', 'Palanca del freno de mano', CJ, fm, (0, 0.15, 1.25))

# ================================================================ SUSPENSIÓN Y DIRECCIÓN
CJ = 'Suspensión y dirección'
for lado, s in (('izq', 1), ('der', -1)):
    st = P()
    base = Vector((XF + 0.01, s * (YF - 0.14), ZA + 0.07))
    top = Vector((XF + 0.035, s * (YF - 0.215), 0.87))
    ax = (top - base).normalized()
    st.barra(base, base + ax * 0.33, 0.027, M['amortiguador'])                                       # cuerpo
    st.barra(base + ax * 0.33, top, 0.011, M['cromo'])                                                # vástago
    st.fuelle(base + ax * 0.34, base + ax * 0.50, 0.024, 0.024, 6, M['goma'])                         # guardapolvo
    lo, hi = base + ax * 0.23, top - ax * 0.04
    st.helice(lo, hi, 0.074, 6, 0.0085, M['resorte'], n=110)
    for p_, r_ in ((lo, 0.092), (hi, 0.097)):
        st.barra(p_ - ax * 0.006, p_ + ax * 0.006, r_, M['acero_osc'], segs=24)                       # platos del resorte
    st.lathe_z(None, [(0.0, 0.0), (0.085, 0.0), (0.075, 0.035), (0.0, 0.035)], M['goma'],
               mtx=Matrix.Translation(top) @ eje_a(ax), segs=24)                                       # copela superior
    # mangueta y cubo
    st.rbox(Vector((XF + 0.005, s * (YF - 0.12), ZA - 0.03)), (0.07, 0.06, 0.24), 0.02, M['fundicion'])
    st.cyl('Y', (XF, s * (YF - 0.09), ZA), 0.05, 0.05, M['fundicion'])
    st.rbox(Vector((XF - 0.11, s * (YF - 0.14), ZA + 0.03)), (0.14, 0.03, 0.03), 0.01, M['fundicion'])   # brazo de dirección
    make(f'amortiguador_del_{lado}', f"Columna McPherson {'izquierda' if s > 0 else 'derecha'} (amortiguador y resorte)",
         CJ, st, (0, s * 0.48, 0.60))
    br = P()
    rot = Matrix.Rotation(0, 3, 'Z')
    br.caja_entre((XF - 0.005, s * (YF - 0.13), ZA - 0.14), (XF + 0.03, s * 0.33, 0.19), 0.07, 0.03, M['acero_osc'])
    br.caja_entre((XF + 0.03, s * 0.33, 0.19), (XF - 0.24, s * 0.36, 0.195), 0.055, 0.03, M['acero_osc'])
    br.caja_entre((XF - 0.005, s * (YF - 0.13), ZA - 0.14), (XF - 0.24, s * 0.36, 0.195), 0.03, 0.025, M['acero_osc'])
    br.ellip((XF - 0.005, s * (YF - 0.13), ZA - 0.125), (0.025, 0.025, 0.025), M['negro'])           # rótula
    br.cyl('Y', (XF + 0.03, s * 0.33, 0.19), 0.03, 0.07, M['goma'])
    br.cyl('X', (XF - 0.24, s * 0.36, 0.195), 0.035, 0.07, M['goma'])
    make(f'brazo_{lado}', f"Brazo inferior de suspensión {'izquierdo' if s > 0 else 'derecho'}", CJ, br, (0, s * 0.42, -0.25))

estab = P().curve([(XF + 0.01, 0.585, 0.40), (XF - 0.16, 0.54, 0.27), (XF - 0.19, 0.30, 0.245), (XF - 0.19, -0.30, 0.245),
                   (XF - 0.16, -0.54, 0.27), (XF + 0.01, -0.585, 0.40)], 0.011, M['acero_osc'], segs=16)
for s in (1, -1):
    estab.cyl('Y', (XF - 0.19, s * 0.30, 0.245), 0.022, 0.05, M['goma'])
    estab.barra((XF + 0.01, s * 0.585, 0.40), (XF + 0.012, s * 0.60, 0.50), 0.008, M['acero'])       # bieleta
make('estabilizadora', 'Barra estabilizadora delantera con bieletas', CJ, estab, (-0.30, 0, -0.38))

bast = P()                                                                                            # bastidor auxiliar
bast.rbox((XF - 0.22, 0, 0.21), (0.10, 0.95, 0.06), 0.015, M['acero_osc'])
for s in (1, -1):
    bast.caja_entre((XF - 0.22, s * 0.40, 0.21), (XF + 0.25, s * 0.42, 0.24), 0.07, 0.05, M['acero_osc'])
    bast.cyl('Z', (XF + 0.25, s * 0.42, 0.26), 0.03, 0.04, M['goma'])
make('bastidor', 'Bastidor auxiliar delantero (cuna)', CJ, bast, (0, 0, -0.55))

ej = P()
ej.rbox((XR + 0.20, 0, 0.30), (0.11, 1.20, 0.10), 0.02, M['acero_osc'])
for s in (1, -1):
    ej.caja_entre((XR + 0.60, s * 0.62, 0.31), (XR, s * 0.64, ZA), 0.06, 0.10, M['acero_osc'])
    ej.cyl('Y', (XR + 0.60, s * 0.62, 0.31), 0.042, 0.075, M['goma'])
    ej.cyl('Y', (XR, s * (YR - 0.12), ZA), 0.05, 0.06, M['fundicion'])
    ej.cyl('Z', (XR + 0.08, s * 0.56, 0.355), 0.075, 0.012, M['acero_osc'])                          # asiento del resorte
make('eje_torsion', 'Eje trasero de torsión (viga en U y brazos)', CJ, ej, (-0.35, 0, -0.45))
for lado, s in (('izq', 1), ('der', -1)):
    rt = P()
    rt.helice((XR + 0.08, s * 0.56, 0.36), (XR + 0.08, s * 0.56, 0.60), 0.062, 6, 0.0078, M['resorte'], n=110)
    rt.cyl('Z', (XR + 0.08, s * 0.56, 0.61), 0.07, 0.012, M['goma'])
    rt.barra((XR - 0.09, s * 0.62, 0.27), (XR - 0.12, s * 0.585, 0.48), 0.023, M['amortiguador'])
    rt.barra((XR - 0.12, s * 0.585, 0.48), (XR - 0.135, s * 0.575, 0.74), 0.0095, M['cromo'])
    rt.fuelle((XR - 0.12, s * 0.585, 0.49), (XR - 0.13, s * 0.578, 0.62), 0.022, 0.022, 5, M['goma'])
    rt.cyl('Y', (XR - 0.09, s * 0.62, 0.27), 0.02, 0.04, M['goma'])
    make(f'amortiguador_tra_{lado}', f"Resorte y amortiguador trasero {'izquierdo' if s > 0 else 'derecho'}", CJ, rt,
         (-0.20, s * 0.42, 0.60))

dirc = P()
dirc.cyl('Y', (XF - 0.12, 0, 0.36), 0.026, 0.56, M['aluminio'])
dirc.cyl('Y', (XF - 0.12, -0.20, 0.36), 0.038, 0.10, M['aluminio'])                                 # caja del piñón (der.)
for s in (1, -1):
    dirc.fuelle((XF - 0.12, s * 0.28, 0.36), (XF - 0.12, s * 0.42, 0.36), 0.03, 0.016, 7, M['goma'])
    dirc.barra((XF - 0.12, s * 0.42, 0.36), (XF - 0.115, s * (YF - 0.20), 0.335), 0.011, M['acero'])
    dirc.ellip((XF - 0.11, s * (YF - 0.19), 0.335), (0.022, 0.022, 0.02), M['acero_osc'])            # rótula de bieleta
dirc.barra((XF - 0.12, -0.21, 0.39), (XF - 0.16, -0.25, 0.50), 0.022, M['aluminio'])                 # piñón
make('cremallera', 'Caja de dirección a cremallera, fuelles y bieletas', CJ, dirc, (-0.20, 0, -0.30))

VOL = Vector((0.36, -0.37, 0.985))                       # centro del volante (conductor a la derecha)
NV = Vector((-0.90, 0, 0.44)).normalized()              # hacia donde mira el volante
col = P()
col.curve([(XF - 0.16, -0.25, 0.50), (1.00, -0.30, 0.60), (0.86, -0.35, 0.70)], 0.012, M['acero'])  # eje intermedio
for p_ in ((XF - 0.16, -0.25, 0.50), (0.86, -0.35, 0.70)):
    col.ellip(p_, (0.022, 0.022, 0.022), M['acero_osc'])                                               # crucetas
col.barra((0.86, -0.35, 0.70), VOL + NV * 0.06, 0.018, M['acero'])
col.barra((0.78, -0.355, 0.74), VOL + NV * 0.12, 0.045, M['negro'])                                   # tubo de columna
col.cyl('Y', (0.69, -0.29, 0.79), 0.045, 0.11, M['acero_osc'])                                        # motor de la EPS
col.rbox((0.69, -0.42, 0.78), (0.10, 0.06, 0.10), 0.01, M['aluminio'])                               # sensor de par / módulo
col.rbox(VOL + NV * 0.12 + Vector((0.0, 0, -0.04)), (0.16, 0.13, 0.12), 0.03, M['tablero'])          # cubre columna
for s in (1, -1):                                                                                     # palancas (giro der., limpia izq.)
    col.barra(VOL + NV * 0.10 + Vector((0, s * 0.05, 0.02)), VOL + NV * 0.10 + Vector((0.02, s * 0.17, 0.0)), 0.007, M['negro'])
make('columna_eps', 'Columna de dirección con asistencia eléctrica (EPS)', CJ, col, (0.10, -0.30, 0.95))

vol = P().torus('Z', (0, 0, 0), 0.185, 0.016, M['cuero'], segs=56, rsegs=10)
vol.rbox((0, 0, 0.03), (0.15, 0.13, 0.05), 0.025, M['cuero'])                                         # tapa del airbag
for a in (0, 180, 270):
    r = Matrix.Rotation(math.radians(a), 3, 'Z')
    vol.obox(r @ Vector((0.125, 0, 0.012)), (0.12, 0.05, 0.016), r, M['cuero'])
vol.cyl('Z', (0, 0, -0.03), 0.035, 0.05, M['acero_osc'])
mtx = Matrix.Translation(VOL) @ eje_a(NV) @ Matrix.Rotation(math.radians(90), 4, 'Z')
make('volante', 'Volante con airbag (lado derecho, mano japonesa)', CJ, P().merge(vol, mtx), (-0.10, -0.25, 1.10))

# ================================================================ MOTOR M15A
# Ubicación según el manual de taller (sección 1A, "Ubicación de los componentes"; 1D y 1K):
# escape y catalizador ADELANTE (hacia el radiador), admisión ATRÁS (hacia el torpedo),
# distribución a la derecha y caja a la izquierda. El alternador y el termostato quedan atrás
# (para sacar el termostato hay que sacar antes el múltiple de admisión y el alternador).
CJ = 'Motor M15A'
CYL_Y = [-0.335, -0.245, -0.155, -0.065]   # cilindro 1 del lado de la distribución (derecha)
XC, ZC = 1.375, 0.40                      # eje del cigüeñal
CARRERA = 0.078                           # 78 mm de carrera, 78 mm de diámetro
BIELA = 0.130                             # largo entre centros de biela (aprox.)
bl = P()
bl.rbox((XC, -0.19, 0.46), (0.25, 0.43, 0.33), 0.02, M['aluminio'])
for y in CYL_Y:                                                                                       # nervios del bloque
    bl.box(1.495, 1.51, y - 0.008, y + 0.008, 0.33, 0.60, M['aluminio'])
    bl.box(1.24, 1.255, y - 0.008, y + 0.008, 0.33, 0.60, M['aluminio'])
bl.rbox((XC, -0.19, 0.25), (0.23, 0.40, 0.09), 0.015, M['acero_osc'])                               # cárter
for k in range(5):
    bl.box(1.27, 1.48, -0.37 + k * 0.08, -0.36 + k * 0.08, 0.205, 0.215, M['acero_osc'])
bl.cyl('Z', (1.42, -0.20, 0.198), 0.012, 0.01, M['acero'])                                          # tapón de vaciado
bl.lathe_z(None, [(0.0, 0.0), (0.036, 0.0), (0.038, 0.01), (0.038, 0.07), (0.03, 0.085), (0.0, 0.085)], M['resorte'],
           mtx=Matrix.Translation((1.51, -0.13, 0.34)) @ eje_a((0.85, 0, -0.5)), segs=28)          # filtro de aceite (adelante)
bl.curve([(1.50, 0.0, 0.40), (1.52, 0.01, 0.60), (1.53, 0.02, 0.80), (1.53, 0.03, 0.86)], 0.006, M['negro'])  # tubo varilla
bl.torus('Y', (1.53, 0.03, 0.88), 0.018, 0.005, M['amarillo'], segs=20, rsegs=6)                    # varilla de aceite
bl.cyl('X', (1.24, -0.30, 0.36), 0.012, 0.03, M['negro'])                                           # sensor de detonación
make('bloque', 'Bloque de cilindros, cárter y filtro de aceite', CJ, bl, (0.70, -0.15, 1.25))

cz = P()
cz.rbox((XC, -0.19, 0.685), (0.235, 0.42, 0.12), 0.012, M['aluminio'])
for y in CYL_Y:
    cz.cyl('X', (1.25, y, 0.70), 0.01, 0.01, M['acero'])
    cz.cyl('X', (1.49, y, 0.70), 0.01, 0.01, M['acero'])
cz.cyl('Y', (1.31, 0.025, 0.72), 0.03, 0.012, M['acero_osc'])                                       # sensor de árbol de levas (CMP)
cz.rbox((XC, 0.04, 0.69), (0.07, 0.05, 0.06), 0.01, M['aluminio'])                                  # tapa de salida de agua
cz.cyl('Z', (XC + 0.03, 0.05, 0.73), 0.008, 0.03, M['negro'])                                       # sensor de temperatura (ECT)
cz.rbox((1.26, -0.39, 0.70), (0.03, 0.05, 0.06), 0.008, M['negro'])                                  # válvula de control de aceite (OCV)
make('culata', 'Tapa de cilindros (culata) DOHC 16 válvulas', CJ, cz, (0.70, -0.15, 1.62))

tv = P()
tv.rbox((XC, -0.19, 0.77), (0.20, 0.40, 0.05), 0.02, M['motor_negro'])
for k in range(6):
    tv.box(1.29, 1.455, -0.37 + k * 0.07, -0.364 + k * 0.07, 0.795, 0.803, M['motor_negro'])
tv.cyl('Z', (1.42, -0.10, 0.805), 0.026, 0.025, M['amarillo'])                                      # tapa de aceite
tv.cyl('Y', (1.30, -0.05, 0.78), 0.012, 0.06, M['negro'])                                            # válvula PCV
for y in (CYL_Y[0], CYL_Y[3]):
    tv.rbox((XC, y, 0.82), (0.07, 0.05, 0.06), 0.01, M['negro'])                                     # bobinas (cil. 1 y 4)
    tv.cyl('Z', (XC, y, 0.86), 0.01, 0.02, M['negro'])
for y0, y1 in ((CYL_Y[0], CYL_Y[1]), (CYL_Y[3], CYL_Y[2])):
    tv.curve([(XC + 0.02, y0, 0.84), (XC + 0.05, (y0 + y1) / 2, 0.88), (XC + 0.02, y1, 0.81)], 0.0055, M['negro'])
    tv.cyl('Z', (XC + 0.02, y1, 0.80), 0.012, 0.03, M['negro'])
make('tapa_valvulas', 'Tapa de válvulas, bobinas y cables de alta', CJ, tv, (0.70, -0.15, 1.95))

dist = P()
dist.rbox((1.385, -0.42, 0.50), (0.26, 0.035, 0.52), 0.015, M['aluminio'])
for k in range(8):
    a = 2 * math.pi * k / 8
    dist.cyl('Y', (1.385 + 0.11 * math.cos(a), -0.44, 0.50 + 0.22 * math.sin(a)), 0.006, 0.01, M['acero'], segs=6)
dist.cyl('Y', (1.31, -0.44, 0.72), 0.045, 0.012, M['acero_osc'])                                     # tapa del VVT
dist.cyl('X', (1.25, -0.42, 0.40), 0.012, 0.03, M['negro'])                                          # sensor de cigüeñal (CKP)
make('distribucion', 'Tapa de distribución (con la bomba de aceite)', CJ, dist, (0.70, -0.62, 1.25))

# admisión atrás: colector de plástico con la cámara junto al torpedo
adm = P()
adm.cyl('Y', (1.11, -0.17, 0.62), 0.055, 0.40, M['negro'])                                         # cámara (plenum)
adm.rbox((1.06, -0.17, 0.62), (0.02, 0.36, 0.06), 0.005, M['negro'])
for y in CYL_Y:
    adm.curve([(1.255, y, 0.70), (1.20, y, 0.745), (1.13, y, 0.72), (1.105, y, 0.665)], 0.023, M['negro'])
    adm.cyl('X', (1.235, y, 0.735), 0.008, 0.055, M['negro'])                                        # inyectores
adm.cyl('Y', (1.215, -0.20, 0.765), 0.012, 0.36, M['acero'])                                         # tubo de descarga (riel)
adm.curve([(1.215, 0.0, 0.765), (1.20, 0.10, 0.70), (1.10, 0.30, 0.50), (0.98, 0.20, 0.30)], 0.005, M['negro'])  # caño de nafta
adm.cyl('Y', (1.11, 0.065, 0.62), 0.04, 0.07, M['aluminio'])                                         # cuerpo de mariposa
adm.rbox((1.11, 0.07, 0.675), (0.05, 0.03, 0.03), 0.008, M['negro'])                                 # sensor TP
adm.rbox((1.11, -0.30, 0.68), (0.04, 0.03, 0.03), 0.008, M['negro'])                                 # sensor MAP
make('admision', 'Múltiple de admisión, inyectores y cuerpo de mariposa', CJ, adm, (-0.45, 0.10, 1.10))

af = P()
af.rbox((1.43, 0.25, 0.70), (0.26, 0.24, 0.16), 0.03, M['negro'])
af.rbox((1.43, 0.25, 0.785), (0.27, 0.25, 0.012), 0.005, M['negro'])
for dx in (-0.11, 0.11):
    af.rbox((1.43 + dx, 0.375, 0.775), (0.03, 0.02, 0.03), 0.006, M['acero'])
af.curve([(1.56, 0.30, 0.70), (1.70, 0.36, 0.72), (1.82, 0.38, 0.66)], 0.035, M['negro'])           # toma de aire
af.cyl('X', (1.29, 0.20, 0.74), 0.04, 0.05, M['negro'])                                              # caudalímetro (MAF)
af.fuelle((1.27, 0.19, 0.74), (1.13, 0.10, 0.63), 0.042, 0.042, 6, M['goma'])                       # manguera a la mariposa
make('filtro_aire', 'Caja del filtro de aire y caudalímetro', CJ, af, (0.75, 0.60, 1.05))

# escape adelante: el múltiple lleva el catalizador incorporado (sección 1K)
esc = P()
for y in CYL_Y:
    esc.curve([(1.495, y, 0.70), (1.55, y, 0.68), (1.585, (y - 0.20) / 2, 0.60), (1.60, -0.20, 0.53)], 0.021, M['escape'])
esc.lathe_z(None, [(0.0, 0.0), (0.03, 0.0), (0.068, 0.04), (0.068, 0.20), (0.035, 0.25), (0.0, 0.25)], M['escape'],
            mtx=Matrix.Translation((1.60, -0.20, 0.53)) @ eje_a((0, 0, -1)), segs=32)                # catalizador
esc.rbox((1.565, -0.19, 0.62), (0.06, 0.40, 0.16), 0.02, M['aluminio'], rot=Matrix.Rotation(math.radians(-12), 3, 'Y'))
for k in range(6):
    esc.box(1.535, 1.545, -0.36 + k * 0.07, -0.33 + k * 0.07, 0.56, 0.68, M['aluminio'])
esc.cyl('X', (1.60, -0.12, 0.60), 0.01, 0.05, M['negro'])                                           # sonda de oxígeno 1
esc.cyl('X', (1.61, -0.20, 0.27), 0.01, 0.05, M['negro'])                                           # sonda de oxígeno 2
make('multiple_escape', 'Múltiple de escape con catalizador y sondas', CJ, esc, (1.35, -0.20, 0.95))

# lado de las correas (derecha): bomba de agua y alternador atrás con una correa; compresor adelante con otra
acc = P()
acc.lathe((XC, -0.455, ZC), [(0.02, -0.025), (0.07, -0.025), (0.068, -0.015), (0.072, -0.006), (0.068, 0.004),
                              (0.072, 0.014), (0.07, 0.025), (0.02, 0.025)], M['acero_osc'], sign=-1, segs=40)
acc.lathe((1.40, -0.455, 0.62), [(0.01, -0.015), (0.05, -0.015), (0.05, 0.015), (0.01, 0.015)], M['acero_osc'], sign=-1)
alt = [(0.0, -0.07)]
for k in range(8):
    alt += [(0.062, -0.065 + k * 0.016), (0.066, -0.058 + k * 0.016)]
alt += [(0.062, 0.065), (0.0, 0.07)]
acc.lathe((1.19, -0.38, 0.60), alt, M['aluminio'], sign=-1, segs=32)                                 # alternador (atrás, arriba)
acc.cyl('Y', (1.19, -0.455, 0.60), 0.03, 0.03, M['acero_osc'])
acc.curve([(XC, -0.455, 0.33), (1.43, -0.455, 0.36), (1.45, -0.455, 0.62), (1.40, -0.455, 0.67), (1.19, -0.455, 0.63),
           (1.16, -0.455, 0.60), (1.20, -0.455, 0.57), (1.31, -0.455, 0.42), (XC, -0.455, 0.33)], 0.0055, M['correa'], segs=6)
acc.cyl('Y', (1.56, -0.36, 0.30), 0.062, 0.16, M['aluminio'])                                        # compresor del aire (adelante, abajo)
acc.cyl('Y', (1.56, -0.465, 0.30), 0.056, 0.025, M['acero_osc'])
acc.curve([(XC, -0.468, 0.47), (1.56, -0.468, 0.356), (1.62, -0.468, 0.30), (1.56, -0.468, 0.244), (XC, -0.468, 0.33),
           (1.31, -0.468, 0.40), (XC, -0.468, 0.47)], 0.005, M['correa'], segs=6)
make('accesorios', 'Alternador, bomba de agua, compresor del aire y correas', CJ, acc, (0.90, -0.80, 0.95))

arr = P().cyl('Y', (1.17, 0.08, 0.40), 0.042, 0.17, M['acero_osc'])
arr.cyl('Y', (1.17, 0.18, 0.40), 0.03, 0.04, M['negro'])
arr.cyl('Y', (1.19, 0.06, 0.45), 0.02, 0.09, M['acero_osc'])
arr.curve([(1.19, 0.10, 0.47), (1.25, 0.20, 0.55), (1.33, 0.43, 0.66)], 0.005, M['rojo_tapa'])
make('arranque', 'Motor de arranque', CJ, arr, (-0.40, 0.45, 0.70))

# soportes (sección 1D): derecho arriba en la distribución, izquierdo sobre la caja y trasero (barra de reacción) a la cuna
so = P()
so.rbox((1.40, -0.47, 0.66), (0.10, 0.08, 0.06), 0.01, M['acero_osc'])
so.cyl('Y', (1.40, -0.56, 0.68), 0.05, 0.08, M['goma'])
so.rbox((1.40, -0.63, 0.68), (0.12, 0.06, 0.10), 0.01, M['acero_osc'])
so.rbox((1.30, 0.43, 0.58), (0.10, 0.06, 0.06), 0.01, M['acero_osc'])
so.cyl('Y', (1.30, 0.52, 0.60), 0.05, 0.08, M['goma'])
so.rbox((1.30, 0.59, 0.60), (0.12, 0.06, 0.10), 0.01, M['acero_osc'])
so.caja_entre((1.13, 0.12, 0.26), (0.97, 0.05, 0.21), 0.05, 0.03, M['acero_osc'])
so.cyl('Y', (0.97, 0.05, 0.21), 0.03, 0.05, M['goma'])
make('soportes_motor', 'Soportes del motor (derecho, izquierdo y trasero)', CJ, so, (0.20, 0, 0.50))

# ================================================================ MOTOR POR DENTRO (cigüeñal, pistones, levas, válvulas, cadena)
CJ = 'Motor por dentro'
ANG = {0: 0, 3: 0, 1: 180, 2: 180}        # muñequillas 1-4 arriba, 2-3 abajo (orden 1-3-4-2)
cg = P()
for k in range(5):                                                                                    # muñones de bancada Ø52
    yj = -0.38 + k * 0.09
    cg.cyl('Y', (XC, yj, ZC), 0.026, 0.022, M['acero'])
for i, y in enumerate(CYL_Y):
    a = math.radians(ANG[i])
    px_, pz_ = XC + (CARRERA / 2) * math.sin(a), ZC + (CARRERA / 2) * math.cos(a)
    cg.cyl('Y', (px_, y, pz_), 0.0225, 0.024, M['acero'])                                             # muñequilla Ø45
    for dy in (-0.022, 0.022):                                                                         # brazos y contrapesos
        cg.obox(((XC + px_) / 2, y + dy, (ZC + pz_) / 2), (0.05, 0.018, 0.075),
                Matrix.Rotation(-a, 3, 'Y'), M['acero_osc'])
        cg.tube('Y', (XC, y + dy, ZC), 0.004, 0.062, 0.018, M['acero_osc'], a0=ANG[i] + 30, a1=ANG[i] + 150, segs=24)
cg.cyl('Y', (XC, -0.42, ZC), 0.02, 0.04, M['acero'])                                                  # punta delantera
cg.gear('Y', (XC, -0.405, ZC), 0.022, 18, 0.012, M['acero_osc'])                                     # piñón de distribución
cg.cyl('Y', (XC, 0.035, ZC), 0.13, 0.008, M['acero_osc'])                                             # placa de arrastre (A/T)
cg.gear('Y', (XC, 0.035, ZC), 0.142, 90, 0.010, M['acero_osc'])                                       # corona del arranque
make('ciguenal', 'Cigüeñal con placa de arrastre', CJ, cg, (1.05, -0.15, 0.10))

pb = P()
for i, y in enumerate(CYL_Y):
    a = math.radians(ANG[i])
    px_, pz_ = XC + (CARRERA / 2) * math.sin(a), ZC + (CARRERA / 2) * math.cos(a)
    zp = pz_ + math.sqrt(BIELA ** 2 - (px_ - XC) ** 2)                                                 # perno del pistón
    pb.barra((px_, y, pz_), (XC, y, zp), 0.011, M['acero_osc'])                                       # biela
    pb.cyl('Y', (px_, y, pz_), 0.031, 0.022, M['acero_osc'])                                          # cabeza de biela
    pb.cyl('Y', (XC, y, zp), 0.016, 0.022, M['acero_osc'])                                            # pie de biela
    pb.cyl('Y', (XC, y, zp), 0.010, 0.07, M['acero'])                                                 # perno Ø20
    pist = [(0.0, -0.03), (0.0385, -0.03), (0.0385, 0.012), (0.0375, 0.013), (0.0375, 0.016), (0.0388, 0.017),
            (0.0388, 0.019), (0.0375, 0.020), (0.0375, 0.023), (0.0388, 0.024), (0.0388, 0.026), (0.0375, 0.027),
            (0.0375, 0.030), (0.0388, 0.031), (0.0388, 0.035), (0.034, 0.036), (0.0, 0.036)]
    pb.lathe_z(None, pist, M['aluminio'], mtx=Matrix.Translation((XC, y, zp)), segs=32)               # pistón Ø78 con 3 aros
make('pistones', 'Pistones, aros y bielas', CJ, pb, (1.05, -0.15, 0.55))

XI, XE, ZL = 1.315, 1.435, 0.735          # árboles de levas: admisión atrás, escape adelante
lv = P()
for xl, nom in ((XI, 'adm'), (XE, 'esc')):
    lv.cyl('Y', (xl, -0.19, ZL), 0.012, 0.42, M['acero'])
    for k in range(5):
        lv.cyl('Y', (xl, -0.38 + k * 0.09, ZL), 0.0145, 0.02, M['acero'])                            # apoyos
        lv.rbox((xl, -0.38 + k * 0.09, ZL + 0.02), (0.04, 0.022, 0.012), 0.004, M['aluminio'])       # sombreretes
    for i, y in enumerate(CYL_Y):
        for dy in (-0.019, 0.019):
            ang = math.radians(90 * i + (0 if nom == 'adm' else 100))
            lv.ellip((xl + 0.008 * math.sin(ang), y + dy, ZL - 0.008 * math.cos(ang)), (0.02, 0.008, 0.02),
                     M['acero_osc'], rot=Matrix.Rotation(-ang, 3, 'Y'), segs=16, rings=8)              # levas (45 mm de alto)
lv.gear('Y', (XI, -0.40, ZL), 0.05, 36, 0.012, M['acero_osc'])                                        # piñón con VVT
lv.cyl('Y', (XI, -0.385, ZL), 0.043, 0.03, M['aluminio'])                                            # actuador del VVT
lv.gear('Y', (XE, -0.40, ZL), 0.045, 36, 0.012, M['acero_osc'])
make('arboles_levas', 'Árboles de levas y actuador del VVT', CJ, lv, (1.05, -0.15, 1.75))

va = P()
for i, y in enumerate(CYL_Y):
    for dy in (-0.019, 0.019):
        for xl, sgn, rh in ((XI, -1, 0.0145), (XE, 1, 0.0125)):
            top = Vector((xl, y + dy, ZL - 0.025))
            d_ = Vector((sgn * 0.30, 0, -1)).normalized()                                              # válvulas en V
            va.cyl('Z', top + Vector((0, 0, -0.002)), 0.0155, 0.018, M['acero'])                      # botador (Ø31)
            va.helice(top + d_ * 0.012, top + d_ * 0.042, 0.011, 5, 0.0016, M['resorte'], n=40)       # resorte (36,8 mm libre)
            va.barra(top + d_ * 0.01, top + d_ * 0.080, 0.00275, M['acero'], segs=8)                  # vástago Ø5,5
            va.lathe_z(None, [(0.0, 0.0), (rh, 0.0), (rh, 0.002), (0.004, 0.008)], M['acero'],
                       mtx=Matrix.Translation(top + d_ * 0.082) @ eje_a(-d_), segs=16)                # cabeza
make('valvulas', 'Válvulas, resortes y botadores (16)', CJ, va, (1.05, -0.15, 1.42))

ca = P()
# cadena: tramos rectos entre el piñón del cigüeñal y los de las levas, con guías y tensor
pts = [(XC + 0.022, ZC), (XE + 0.045, ZL), (XE, ZL + 0.045), (XI, ZL + 0.05), (XI - 0.05, ZL), (XC - 0.022, ZC),
       (XC, ZC - 0.022), (XC + 0.022, ZC)]
ca.curve([(x, -0.40, z) for x, z in pts], 0.004, M['acero'], segs=4)
ca.rbox((XE + 0.055, -0.40, (ZC + ZL) / 2), (0.012, 0.016, 0.26), 0.004, M['negro'],
        rot=Matrix.Rotation(math.radians(-6), 3, 'Y'))                                                # guía fija
ca.rbox((XI - 0.06, -0.40, (ZC + ZL) / 2), (0.012, 0.016, 0.26), 0.004, M['negro'],
        rot=Matrix.Rotation(math.radians(8), 3, 'Y'))                                                 # guía del tensor
ca.rbox((XI - 0.085, -0.40, 0.50), (0.03, 0.03, 0.04), 0.006, M['aluminio'])                          # tensor
make('cadena', 'Cadena de distribución, guías y tensor', CJ, ca, (1.05, -0.95, 1.30))

bo_ = P()
bo_.gear('Y', (XC, -0.43, ZC), 0.032, 10, 0.012, M['acero'])                                          # rotor interior
bo_.tube('Y', (XC, -0.43, ZC), 0.033, 0.045, 0.012, M['acero_osc'])                                   # rotor exterior
bo_.curve([(XC + 0.02, -0.25, 0.30), (XC + 0.03, -0.20, 0.24), (XC + 0.02, -0.18, 0.215)], 0.008, M['acero'])  # colador
bo_.cyl('Z', (XC + 0.02, -0.18, 0.212), 0.035, 0.006, M['acero'])
bo_.lathe((1.40, -0.425, 0.62), [(0.005, -0.006), (0.035, -0.006), (0.035, 0.006), (0.005, 0.006)], M['acero'], sign=-1)
for k in range(6):                                                                                     # turbina de la bomba de agua
    r = Matrix.Rotation(-2 * math.pi * k / 6, 3, 'Y')
    bo_.obox(Vector((1.40, -0.41, 0.62)) + r @ Vector((0.018, 0, 0)), (0.03, 0.012, 0.003), r, M['acero'])
make('bombas', 'Bomba de aceite (rotores) y bomba de agua', CJ, bo_, (1.05, -0.95, 0.85))

# ================================================================ TRANSMISIÓN
CJ = 'Transmisión'
ta = P()
ta.cyl('Y', (1.36, 0.07, 0.42), 0.17, 0.10, M['aluminio'], r2=0.15)
ta.rbox((1.29, 0.26, 0.39), (0.34, 0.28, 0.33), 0.03, M['aluminio'])
ta.cyl('Y', (1.20, 0.26, 0.30), 0.11, 0.26, M['aluminio'])                                          # diferencial
for k in range(4):
    ta.box(1.14 + k * 0.08, 1.15 + k * 0.08, 0.12, 0.40, 0.55, 0.56, M['aluminio'])                  # nervios
ta.rbox((1.35, 0.405, 0.38), (0.10, 0.02, 0.14), 0.01, M['negro'])                                   # conector de solenoides
ta.rbox((1.29, 0.26, 0.22), (0.26, 0.22, 0.03), 0.01, M['acero_osc'])                                # cárter de aceite
for dz in (0.0, 0.02):                                                                                # caños del enfriador del ATF
    ta.curve([(1.40, 0.18, 0.45 + dz), (1.55, 0.25, 0.42 + dz), (1.74, 0.36, 0.40 + dz)], 0.005, M['negro'])
ta.curve([(1.30, 0.40, 0.47), (1.10, 0.30, 0.45), (0.50, 0.05, 0.40)], 0.004, M['negro'])           # cable de la palanca
make('caja_4at', 'Caja automática de 4 marchas (4AT) con diferencial', CJ, ta, (0.30, 0.75, 0.75))
cv = P()
cv.lathe((XC, 0.045, ZC), [(0.03, 0.0), (0.12, 0.0), (0.132, 0.015), (0.132, 0.055), (0.115, 0.075), (0.04, 0.08),
                           (0.03, 0.10), (0.02, 0.10), (0.02, 0.0)], M['aluminio'], sign=1, segs=48)
for k in range(3):                                                                                    # tuercas de fijación a la placa
    a_ = 2 * math.pi * k / 3
    cv.cyl('Y', (XC + 0.10 * math.cos(a_), 0.042, ZC + 0.10 * math.sin(a_)), 0.008, 0.008, M['acero'], segs=6)
make('convertidor', 'Convertidor de par', CJ, cv, (0.30, 0.45, 0.30))
for lado, s in (('izq', 1), ('der', -1)):
    sm = P()
    p0 = Vector((1.20, 0.40 if s > 0 else -0.10, 0.30))
    p1 = Vector((XF, s * (YF - 0.13), ZA))
    d_ = (p1 - p0).normalized()
    sm.barra(p0, p1, 0.013, M['acero'])
    sm.fuelle(p0 + d_ * 0.01, p0 + d_ * 0.13, 0.045, 0.02, 6, M['goma'])
    sm.fuelle(p1 - d_ * 0.12, p1 - d_ * 0.01, 0.02, 0.045, 6, M['goma'])
    make(f'semieje_{lado}', f"Semieje (palier) {'izquierdo' if s > 0 else 'derecho'} con homocinéticas", CJ, sm,
         (0, s * 0.32, -0.28))
pl = P()
pl.rbox((0.37, 0.0, 0.45), (0.30, 0.20, 0.32), 0.03, M['tablero'])                                   # consola
pl.rbox((0.42, 0.0, 0.615), (0.16, 0.10, 0.012), 0.004, M['cromo'])                                  # placa de posiciones
pl.box(0.37, 0.48, -0.006, 0.006, 0.618, 0.622, M['negro'])                                          # ranura
pl.cyl('Z', (0.45, 0.0, 0.69), 0.008, 0.15, M['cromo'])
pl.ellip((0.45, 0.0, 0.78), (0.03, 0.025, 0.045), M['negro'])
pl.rbox((0.23, 0.0, 0.55), (0.10, 0.12, 0.05), 0.015, M['tablero'])                                  # portavasos
make('palanca', 'Consola y palanca selectora (P R N D 3 2 L)', CJ, pl, (0, 0, 1.30))

# ================================================================ REFRIGERACIÓN
CJ = 'Refrigeración'
rad = P().box(1.755, 1.785, -0.33, 0.33, 0.30, 0.66, M['radiador'])
for k in range(16):                                                                                   # tubos del panal
    rad.box(1.785, 1.79, -0.32, 0.32, 0.315 + k * 0.021, 0.322 + k * 0.021, M['acero_osc'])
for s in (1, -1):
    rad.rbox((1.77, s * 0.35, 0.48), (0.05, 0.04, 0.38), 0.01, M['negro'])                            # tanques laterales
rad.cyl('Z', (1.77, 0.35, 0.68), 0.022, 0.03, M['acero'])                                             # tapa del radiador
rad.cyl('X', (1.76, -0.35, 0.33), 0.012, 0.03, M['acero'])                                            # tapón de purga
make('radiador', 'Radiador', CJ, rad, (1.25, 0, 0.20))
ven = P().rbox((1.722, 0, 0.48), (0.035, 0.66, 0.36), 0.02, M['negro'])
ven.cyl('X', (1.69, 0.0, 0.48), 0.055, 0.06, M['acero_osc'])                                          # motor del ventilador
for k in range(7):
    r = Matrix.Rotation(2 * math.pi * k / 7, 3, 'X') @ Matrix.Rotation(math.radians(25), 3, 'Y')
    ven.obox(Vector((1.70, 0.0, 0.48)) + Matrix.Rotation(2 * math.pi * k / 7, 3, 'X') @ Vector((0, 0.095, 0)),
             (0.008, 0.10, 0.05), r, M['negro'])
make('electroventilador', 'Electroventilador del radiador', CJ, ven, (0.95, 0, 0.45))
mg = P()
mg.curve([(XC, 0.065, 0.69), (1.50, 0.18, 0.74), (1.66, 0.28, 0.70), (1.77, 0.33, 0.64)], 0.018, M['goma'])      # superior
mg.rbox((1.20, 0.0, 0.46), (0.07, 0.07, 0.07), 0.012, M['aluminio'])                                 # caja del termostato (atrás)
mg.curve([(1.77, -0.33, 0.33), (1.68, -0.20, 0.22), (1.40, 0.05, 0.19), (1.24, 0.06, 0.30), (1.21, 0.03, 0.43)],
         0.018, M['goma'])                                                                             # inferior al termostato
mg.curve([(1.21, -0.03, 0.47), (1.24, -0.20, 0.42), (1.30, -0.40, 0.55), (1.38, -0.42, 0.60)], 0.012, M['acero'])  # tubo a la bomba
mg.curve([(1.17, 0.0, 0.48), (1.05, -0.10, 0.60), (0.99, -0.10, 0.72)], 0.008, M['goma'])            # mangueras de la calefacción
mg.curve([(1.30, 0.02, 0.66), (1.05, -0.16, 0.66), (0.99, -0.16, 0.70)], 0.008, M['goma'])
make('mangueras', 'Mangueras del radiador, termostato y calefacción', CJ, mg, (0.80, -0.20, 0.80))
dep = P().rbox((1.67, -0.54, 0.64), (0.10, 0.12, 0.16), 0.02, M['bateria'])
dep.cyl('Z', (1.67, -0.54, 0.73), 0.02, 0.02, M['negro'])
dep.curve([(1.67, -0.48, 0.70), (1.72, -0.40, 0.70), (1.77, 0.34, 0.69)], 0.005, M['goma'])
make('deposito_refrigerante', 'Depósito recuperador de refrigerante', CJ, dep, (0.75, -0.60, 0.70))

# ================================================================ ELÉCTRICO
CJ = 'Eléctrico'
bat = P().rbox((1.419, 0.48, 0.514), (0.238, 0.129, 0.227), 0.008, M['bateria'])
bat.rbox((1.419, 0.48, 0.63), (0.238, 0.129, 0.012), 0.004, M['negro'])
bat.cyl('Z', (1.33, 0.44, 0.645), 0.011, 0.02, M['rojo_tapa'])
bat.cyl('Z', (1.51, 0.44, 0.645), 0.011, 0.02, M['acero_osc'])
bat.box(1.30, 1.54, 0.41, 0.55, 0.38, 0.40, M['negro'])                                               # bandeja
bat.box(1.41, 1.43, 0.41, 0.55, 0.636, 0.65, M['acero_osc'])                                          # traba
bat.curve([(1.33, 0.44, 0.66), (1.30, 0.38, 0.70), (1.10, 0.52, 0.68)], 0.007, M['rojo_tapa'])       # cable positivo
bat.curve([(1.51, 0.44, 0.66), (1.56, 0.40, 0.62), (1.52, 0.30, 0.50)], 0.007, M['negro'])          # cable negativo
make('bateria', 'Batería 46B24R (12 V, 36 Ah)', CJ, bat, (0.40, 0.85, 0.95))
fus = P().rbox((1.065, 0.51, 0.66), (0.13, 0.14, 0.12), 0.012, M['negro'])
fus.rbox((1.065, 0.51, 0.725), (0.135, 0.145, 0.02), 0.008, M['negro'])
fus.rbox((1.065, 0.51, 0.738), (0.05, 0.03, 0.004), 0.002, M['amarillo'])
make('fusibles', 'Caja de fusibles y relés del motor', CJ, fus, (0.10, 0.75, 0.90))
ecu = P().rbox((1.62, 0.55, 0.40), (0.16, 0.04, 0.12), 0.006, M['aluminio'])
ecu.rbox((1.62, 0.525, 0.40), (0.07, 0.012, 0.06), 0.004, M['negro'])
make('ecu', 'Computadora del motor (ECM)', CJ, ecu, (0.70, 0.70, 0.25))
bo = P().lathe_z(None, [(0.006, -0.01), (0.04, 0.0), (0.042, 0.02), (0.0, 0.02)], M['negro'],
                 mtx=Matrix.Translation((1.83, -0.50, 0.42)) @ eje_a((1, 0, 0)), segs=24)
make('bocina', 'Bocina', CJ, bo, (0.70, -0.40, 0.0))
fus2 = P().rbox((0.66, -0.66, 0.60), (0.10, 0.12, 0.12), 0.012, M['negro'])
make('fusibles_cabina', 'Caja de empalmes (fusibles de cabina)', CJ, fus2, (0, -0.65, 0.75))

# ================================================================ COMBUSTIBLE Y ESCAPE
CJ = 'Combustible y escape'
tq = P().rbox((-0.80, 0.0, 0.225), (0.40, 0.84, 0.15), 0.04, M['tanque'])
tq.rbox((-0.80, 0.0, 0.31), (0.30, 0.74, 0.04), 0.02, M['tanque'])
tq.cyl('Z', (-0.80, 0.15, 0.335), 0.065, 0.012, M['negro'])                                          # bomba y aforador
tq.rbox((-0.80, 0.15, 0.35), (0.04, 0.06, 0.02), 0.006, M['negro'])
for dx in (-0.12, 0.12):
    tq.box(-0.80 + dx - 0.015, -0.80 + dx + 0.015, -0.44, 0.44, 0.145, 0.152, M['acero_osc'])          # flejes
# boca de carga hasta la tapa del lado izquierdo
tq.curve([(-0.95, 0.38, 0.28), (-1.15, 0.55, 0.45), (X_TAPA + 0.02, 0.70, Z_TAPA - 0.05), (X_TAPA, 0.78, Z_TAPA)], 0.024, M['negro'])
tq.cyl('Y', (X_TAPA, 0.785, Z_TAPA), 0.035, 0.02, M['negro'])
tq.curve([(-0.70, 0.15, 0.35), (-0.30, -0.15, 0.24), (0.60, -0.20, 0.235), (1.10, -0.20, 0.34)], 0.0045, M['acero'])
make('tanque', 'Tanque de combustible (43 L) con bomba y boca de carga', CJ, tq, (0, 0.05, -0.70))
cn = P().cyl('Z', (1.02, 0.66, 0.53), 0.05, 0.17, M['negro'])
cn.cyl('Z', (1.02, 0.66, 0.625), 0.02, 0.02, M['negro'])
cn.curve([(1.02, 0.66, 0.64), (1.06, 0.40, 0.70), (1.11, -0.10, 0.68)], 0.005, M['goma'])            # a la válvula de purga
cn.rbox((1.11, -0.12, 0.68), (0.03, 0.04, 0.03), 0.006, M['negro'])                                  # válvula de purga
cn.curve([(1.02, 0.66, 0.45), (0.80, 0.45, 0.24), (-0.70, 0.20, 0.25), (-0.82, 0.15, 0.34)], 0.004, M['negro'])
make('canister', 'Recipiente de EVAP (canister) y válvula de purga', CJ, cn, (0.20, 0.55, 0.40))
ex = P()
ex.curve([(1.61, -0.20, 0.27), (1.58, -0.18, 0.18), (1.45, -0.10, 0.165), (1.25, -0.06, 0.17), (1.10, -0.05, 0.19)],
         0.024, M['escape'])                                                                          # caño delantero n° 1
ex.fuelle((1.10, -0.05, 0.19), (0.98, -0.05, 0.20), 0.03, 0.03, 8, M['acero'])                      # flexible
ex.curve([(0.98, -0.05, 0.20), (0.40, -0.05, 0.205), (0.20, -0.05, 0.205)], 0.022, M['escape'])
ex.lathe_z(None, [(0.0, 0.0), (0.025, 0.0), (0.06, 0.05), (0.06, 0.40), (0.025, 0.45), (0.0, 0.45)], M['escape'],
           mtx=Matrix.Translation((0.20, -0.05, 0.205)) @ eje_a((-1, 0, 0)), segs=28)                 # resonador (silenciador central)
ex.curve([(-0.25, -0.05, 0.205), (-0.45, -0.18, 0.20), (-0.62, -0.47, 0.20), (-1.25, -0.47, 0.20),
          (-1.38, -0.38, 0.25)], 0.022, M['escape'])                                                  # caño central
ex.rbox((-1.55, -0.22, 0.31), (0.24, 0.44, 0.17), 0.07, M['escape'], seg=3)                          # silenciador trasero
ex.curve([(-1.62, -0.36, 0.29), (-1.74, -0.37, 0.27), (-1.80, -0.367, 0.265)], 0.022, M['escape'])
ex.cyl('X', (-1.81, -0.367, 0.265), 0.03, 0.07, M['cromo'])                                          # puntera
ex.rbox((-0.95, -0.47, 0.245), (0.50, 0.20, 0.008), 0.004, M['aluminio'])                           # protector de calor bajo el piso
for p_ in ((-0.45, -0.18, 0.21), (-1.30, -0.42, 0.24), (-1.60, -0.05, 0.36), (0.95, -0.05, 0.23)):   # colgadores de goma
    ex.cyl('Z', p_, 0.012, 0.05, M['goma'])
make('escape', 'Línea de escape (caño delantero, resonador y silenciador)', CJ, ex, (0, 0, -0.60))

# ================================================================ AIRE ACONDICIONADO Y CALEFACCIÓN (secciones 7A y 7B)
CJ = 'Aire acondicionado y calefacción'
co = P().box(1.80, 1.815, -0.34, 0.34, 0.32, 0.64, M['radiador'])
for k in range(14):
    co.box(1.815, 1.818, -0.33, 0.33, 0.335 + k * 0.021, 0.340 + k * 0.021, M['acero_osc'])
for s in (1, -1):
    co.box(1.798, 1.818, s * 0.34, s * 0.36, 0.31, 0.65, M['aluminio'])                              # tanques del condensador
co.cyl('Z', (1.80, 0.38, 0.48), 0.025, 0.20, M['acero_osc'])                                         # secador (receptor)
make('condensador', 'Condensador del A/C y filtro secador', CJ, co, (1.55, 0, 0.05))
cl = P()
cl.curve([(1.56, -0.28, 0.33), (1.62, -0.10, 0.40), (1.79, 0.30, 0.62)], 0.009, M['aluminio'])       # descarga (alta)
cl.curve([(1.80, 0.38, 0.38), (1.65, 0.50, 0.40), (1.30, 0.62, 0.62), (0.98, 0.25, 0.70)], 0.006, M['aluminio'])  # líquido
cl.curve([(0.98, 0.20, 0.66), (1.20, 0.30, 0.50), (1.45, -0.10, 0.36), (1.56, -0.28, 0.27)], 0.011, M['aluminio'])  # succión (baja)
cl.cyl('Z', (1.30, 0.62, 0.66), 0.012, 0.04, M['negro'])                                              # sensor de presión
make('canerias_ac', 'Cañerías del A/C (alta, líquido y succión)', CJ, cl, (0.60, 0.30, 0.75))
hv = P()
hv.rbox((0.80, 0.12, 0.70), (0.20, 0.50, 0.26), 0.03, M['negro'])                                    # caja HVAC
hv.rbox((0.80, 0.12, 0.70), (0.06, 0.30, 0.18), 0.006, M['aluminio'])                                # evaporador
hv.rbox((0.74, 0.0, 0.62), (0.03, 0.18, 0.12), 0.006, M['cobre'] if 'cobre' in M else M['aluminio']) # radiador de calefacción
hv.cyl('Z', (0.78, 0.45, 0.62), 0.07, 0.10, M['negro'])                                              # soplador
hv.cyl('Z', (0.78, 0.45, 0.555), 0.03, 0.04, M['acero_osc'])                                         # motor del soplador
hv.rbox((0.70, 0.45, 0.72), (0.06, 0.10, 0.03), 0.008, M['bateria'])                                  # filtro de habitáculo
for y in (-0.62, -0.10, 0.10, 0.62):
    hv.curve([(0.82, 0.12, 0.82), (0.75, y * 0.6, 0.90), (0.62, y, 0.93 if abs(y) > 0.3 else 0.97)], 0.025, M['negro'])  # conductos
make('unidad_hvac', 'Unidad HVAC: evaporador, calefacción y soplador', CJ, hv, (0.35, 0.10, 1.05))

# ================================================================ INTERIOR
CJ = 'Interior'
Z_PISO = 0.25


def butaca(xc, yc, ancho=0.50):
    a = P()
    a.box(xc - 0.25, xc + 0.25, yc - 0.20, yc + 0.20, Z_PISO, Z_PISO + 0.03, M['acero_osc'])        # correderas
    a.rbox((xc, yc, Z_PISO + 0.12), (0.46, ancho - 0.04, 0.14), 0.03, M['acero_osc'])               # base
    a.rbox((xc + 0.01, yc, Z_PISO + 0.24), (0.50, ancho - 0.10, 0.10), 0.04, M['tela'])             # almohadón
    for s in (1, -1):                                                                                # laterales del almohadón
        a.rbox((xc + 0.01, yc + s * (ancho / 2 - 0.04), Z_PISO + 0.26), (0.48, 0.08, 0.13), 0.035, M['tapizado'])
    rot = Matrix.Rotation(math.radians(-14), 3, 'Y')
    cb = Vector((xc - 0.25, yc, Z_PISO + 0.58))
    a.rbox(cb, (0.12, ancho - 0.10, 0.62), 0.04, M['tela'], rot=rot)                                 # respaldo
    for s in (1, -1):
        a.rbox(cb + Vector((0.02, s * (ancho / 2 - 0.045), -0.04)), (0.15, 0.09, 0.52), 0.035, M['tapizado'], rot=rot)
    hp = cb + rot @ Vector((0, 0, 0.40))
    a.rbox(hp, (0.10, 0.26, 0.16), 0.04, M['tapizado'], rot=rot)                                     # apoyacabeza
    for s in (1, -1):
        a.barra(hp + rot @ Vector((0, s * 0.07, -0.08)), hp + rot @ Vector((0, s * 0.07, -0.16)), 0.006, M['cromo'])
    a.rbox((xc - 0.25, yc + (ancho / 2 + 0.01) * (1 if yc > 0 else -1), Z_PISO + 0.20), (0.06, 0.04, 0.03), 0.01, M['negro'])
    return a


for lado, s in (('izq', 1), ('der', -1)):
    a = butaca(0.10, s * 0.37)
    # cinturón de 3 puntos desde el parante B
    yb = s * 0.66
    a.curve([(-0.25, yb, 1.28), (-0.17, s * 0.55, 1.05), (0.0, s * 0.32, 0.72), (-0.05, s * 0.12, 0.52)], 0.004, M['negro'])
    a.curve([(0.0, s * 0.62, 0.48), (0.06, s * 0.40, 0.56), (-0.05, s * 0.12, 0.52)], 0.004, M['negro'])
    a.rbox((-0.25, yb, 1.30), (0.04, 0.03, 0.06), 0.008, M['gris_trim'])
    nombre = 'Asiento del conductor (derecho)' if s < 0 else 'Asiento del acompañante (izquierdo)'
    make(f'asiento_{lado}', nombre, CJ, a, (0.10, s * 0.28, 1.40), angle=40)

ab_ = P()
ab_.rbox((-0.82, 0, Z_PISO + 0.17), (0.46, 1.26, 0.13), 0.04, M['tela'])
ab_.rbox((-0.84, 0, Z_PISO + 0.07), (0.44, 1.24, 0.12), 0.02, M['acero_osc'])
rot = Matrix.Rotation(math.radians(-12), 3, 'Y')
for y0, w_ in ((0.255, 0.75), (-0.38, 0.50)):                                                       # respaldo 60/40
    ab_.rbox((-1.09, y0, Z_PISO + 0.53), (0.12, w_ - 0.02, 0.60), 0.04, M['tela'], rot=rot)
for y in (-0.42, 0.0, 0.42):
    ab_.rbox((-1.165, y, Z_PISO + 0.90), (0.09, 0.24, 0.14), 0.035, M['tapizado'], rot=rot)
    for s in (1, -1):
        ab_.barra((-1.16, y + s * 0.065, Z_PISO + 0.82), (-1.15, y + s * 0.065, Z_PISO + 0.85), 0.005, M['cromo'])
make('asiento_trasero', 'Asiento trasero rebatible (60/40)', CJ, ab_, (-0.25, 0, 1.40), angle=40)

tb = P()
tb.rbox((0.72, 0, 0.86), (0.32, 1.46, 0.26), 0.05, M['tablero'])                                    # cuerpo
tb.rbox((0.78, 0, 1.005), (0.36, 1.40, 0.05), 0.025, M['tablero'], rot=Matrix.Rotation(math.radians(10), 3, 'Y'))  # tapa superior
tb.rbox((0.60, -0.37, 1.02), (0.16, 0.36, 0.10), 0.04, M['tablero'])                                 # visera del cuadro
for y, r in ((-0.29, 0.058), (-0.45, 0.058), (-0.37, 0.042)):                                         # tres relojes
    zc_ = 0.985 if r < 0.05 else 0.965
    tb.lathe_z(None, [(r - 0.006, 0.0), (r, 0.0), (r, -0.02)], M['cromo'],
               mtx=Matrix.Translation((0.552, y, zc_)) @ eje_a((-1, 0, 0.12)), segs=32)
    tb.cyl('X', (0.556, y, zc_), r - 0.006, 0.004, M['negro'])
    tb.obox((0.552, y + 0.015, zc_ + 0.012), (0.002, 0.004, r * 0.85), Matrix.Rotation(math.radians(-50), 3, 'X'), M['aguja'])
tb.rbox((0.565, 0.0, 0.83), (0.06, 0.22, 0.30), 0.02, M['negro'])                                    # consola central
tb.rbox((0.535, 0.0, 0.90), (0.01, 0.18, 0.06), 0.004, M['cuadro'])                                  # pantalla del audio
for y in (-0.06, 0.0, 0.06):
    tb.lathe_z(None, [(0.0, 0.0), (0.022, 0.0), (0.022, 0.02), (0.0, 0.02)], M['gris_trim'],
               mtx=Matrix.Translation((0.538, y, 0.74)) @ eje_a((-1, 0, 0)), segs=20)                # perillas del aire
for y in (-0.62, 0.62, -0.10, 0.10):                                                                  # rejillas redondas
    tb.lathe_z(None, [(0.0, -0.02), (0.035, -0.02), (0.045, 0.0), (0.038, 0.004)], M['gris_trim'],
               mtx=Matrix.Translation((0.565, y, 0.93 if abs(y) > 0.3 else 0.985)) @ eje_a((-1, 0, 0)), segs=24)
tb.rbox((0.58, 0.40, 0.80), (0.02, 0.36, 0.14), 0.02, M['tablero'])                                  # guantera
tb.rbox((0.572, 0.40, 0.83), (0.01, 0.08, 0.02), 0.005, M['gris_trim'])
tb.rbox((0.72, 0, 0.32), (0.30, 1.30, 0.02), 0.005, M['alfombra'])                                    # alfombra delantera
tb.rbox((-0.25, 0, Z_PISO + 0.005), (1.20, 1.30, 0.01), 0.004, M['alfombra'])
make('tablero', 'Tablero, instrumentos y alfombras', CJ, tb, (0.30, 0, 1.55), angle=40)

te = P()
xm_, zm_ = 0.47, 1.31
te.rbox((xm_, 0, zm_), (0.03, 0.22, 0.06), 0.02, M['negro'])                                          # espejo interior
te.barra((xm_ + 0.005, 0, zm_ + 0.03), (xm_ + 0.03, 0, zm_ + 0.07), 0.008, M['negro'])
for s in (1, -1):
    te.rbox((0.36, s * 0.33, 1.385), (0.18, 0.36, 0.02), 0.01, M['gris_trim'],
            rot=Matrix.Rotation(math.radians(-12), 3, 'Y'))                                            # parasoles
te.rbox((-0.30, 0, 1.475), (0.10, 0.10, 0.02), 0.01, M['gris_trim'])                                   # luz de techo
make('techo_interior', 'Espejo interior, parasoles y luz de techo', CJ, te, (0.0, 0, 1.0))

for lado, s in (('izq', 1), ('der', -1)):
    tp = P()
    for x0, x1 in ((0.78, -0.24), (-0.26, -1.10)):
        xc = (x0 + x1) / 2
        L = x0 - x1 - 0.04
        yi = s * (surf_y(xc, 0.94) - 0.05)
        tp.rbox((xc, yi, 0.66), (L, 0.03, 0.54), 0.02, M['tapizado'])                                # panel
        tp.rbox((xc - 0.05, yi - s * 0.035, 0.76), (L * 0.55, 0.06, 0.04), 0.015, M['tablero'])      # apoyabrazos
        tp.rbox((xc + L * 0.30, yi - s * 0.02, 0.88), (0.10, 0.02, 0.03), 0.008, M['cromo'])         # manija interior
        tp.lathe_z(None, [(0.0, 0.0), (0.06, 0.0), (0.06, 0.006), (0.0, 0.006)], M['negro'],
                   mtx=Matrix.Translation((xc + L * 0.25, yi - s * 0.016, 0.52)) @ eje_a((0, -s, 0)), segs=20)  # parlante
    make(f'tapizado_{lado}', f"Paneles interiores de puertas {'izquierdas' if s > 0 else 'derechas'}", CJ, tp,
         (0, s * 0.60, 0.20), angle=40)

pe = P()
pe.barra((0.80, -0.27, 0.70), (0.72, -0.27, 0.42), 0.008, M['acero_osc'])
pe.rbox((0.715, -0.27, 0.41), (0.025, 0.10, 0.075), 0.01, M['goma'], rot=Matrix.Rotation(math.radians(-30), 3, 'Y'))
pe.barra((0.82, -0.45, 0.62), (0.77, -0.45, 0.36), 0.006, M['acero_osc'])
pe.rbox((0.76, -0.45, 0.35), (0.018, 0.055, 0.15), 0.008, M['goma'], rot=Matrix.Rotation(math.radians(-35), 3, 'Y'))
pe.rbox((0.70, -0.13, 0.36), (0.03, 0.07, 0.15), 0.01, M['goma'], rot=Matrix.Rotation(math.radians(-40), 3, 'Y'))  # apoyapié
make('pedalera', 'Pedalera (freno y acelerador)', CJ, pe, (0.20, -0.30, 1.10))
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
    foto('swift_despiece', (7.4, 6.6, 4.6), (0.2, 0, 1.0), lens=40, despiece=1.0)
    foto('swift_frente_detalle', (3.7, 1.9, 1.15), (1.55, 0.05, 0.62), lens=50)
    foto('swift_cola_detalle', (-3.7, -1.9, 1.5), (-1.55, -0.05, 0.85), lens=50)
    mec = ['Motor M15A', 'Motor por dentro', 'Aire acondicionado y calefacción', 'Transmisión', 'Refrigeración', 'Eléctrico', 'Suspensión y dirección', 'Frenos', 'Ruedas',
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
        'lamina_vano_motor': (['Motor M15A', 'Transmisión', 'Refrigeración', 'Eléctrico', 'Aire acondicionado y calefacción',
                               'Frenos'], (3.0, 1.6, 1.9), (1.35, -0.02, 0.45), 0.0),
        'lamina_motor_dentro': (['Motor por dentro'], (2.3, -1.3, 1.1), (1.37, -0.18, 0.55), 0.0),
    }
    for nombre, (solo, loc, tgt, de) in lam.items():
        foto(nombre, loc, tgt, solo=solo, despiece=de)
    for o in scene.objects:
        if 'pid' in o:
            o.location = (0, 0, 0)
            o.hide_render = False
    print('láminas en', LAM)
