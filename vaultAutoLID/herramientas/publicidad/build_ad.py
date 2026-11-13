"""Publicidad AutoLID: construye la escena completa en Blender.
Uso: blender -b --factory-startup --python build_ad.py -- <salida_frames_dir> [--test] [--blend archivo.blend]
"""
import bpy, bmesh, json, math, os, sys
from math import radians, sin, cos, pi
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUTDIR = argv[0] if argv else "/tmp/autolid_frames"
TEST = "--test" in argv
BLEND = argv[argv.index("--blend") + 1] if "--blend" in argv else None
HERE = os.path.dirname(os.path.abspath(__file__))
SCH = json.load(open(os.path.join(HERE, "schedule.json")))
FPS = SCH["fps"]
DUR = SCH["duration"]
CUTS = SCH["cuts"]


def F(t):
    return int(round(t * FPS)) + 1


# ───────────────────────── Escena base ─────────────────────────
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.fps = FPS
sc.frame_start = 1
sc.frame_end = F(DUR) - 1
sc.render.resolution_x = 1920
sc.render.resolution_y = 1080
sc.render.resolution_percentage = 100
for eng in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"):
    try:
        sc.render.engine = eng
        break
    except TypeError:
        pass
ee = sc.eevee
ee.taa_render_samples = 16
for attr, val in (("use_gtao", True), ("use_shadows", True), ("use_raytracing", True)):
    if hasattr(ee, attr):
        try:
            setattr(ee, attr, val)
        except Exception:
            pass
try:
    sc.render.use_motion_blur = True
    sc.render.motion_blur_shutter = 0.45
except Exception:
    pass
sc.view_settings.view_transform = "AgX"
try:
    sc.view_settings.look = "AgX - Medium High Contrast"
except Exception:
    pass
sc.render.film_transparent = False
sc.render.use_lock_interface = True

world = bpy.data.worlds.new("World")
sc.world = world
world.use_nodes = True
bg = world.node_tree.nodes["Background"]

FONT_B = bpy.data.fonts.load("/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf")
FONT_R = bpy.data.fonts.load("/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf")
for p in ("/usr/share/fonts/truetype/noto/NotoSans-Black.ttf", "/usr/share/fonts/truetype/noto/NotoSans-ExtraBold.ttf"):
    if os.path.exists(p):
        FONT_X = bpy.data.fonts.load(p)
        break
else:
    FONT_X = FONT_B

# Paleta (de la web de AutoLID)
def hexc(h, a=1.0):
    h = h.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    return (*lin, a)


C_ECO = hexc("3ec3d8")
C_ECO_D = hexc("08798c")
C_BLOQ = hexc("f0884e")
C_TINTA = hexc("12202a")
C_NAVY = hexc("0b1820")
C_BLANCO = hexc("f4f6f4")
C_GRIS = hexc("7d8a92")


# ───────────────────────── Animación: utilidades ─────────────────────────
def _fcurves(idb):
    ad = idb.animation_data
    if not ad or not ad.action:
        return []
    act = ad.action
    try:
        from bpy_extras import anim_utils
        cb = anim_utils.action_get_channelbag_for_slot(act, ad.action_slot)
        if cb:
            return list(cb.fcurves)
    except Exception:
        pass
    try:
        return list(act.fcurves)
    except Exception:
        return []


def kf(owner, struct, prop, t, value, interp="BEZIER", easing="EASE_IN_OUT", index=-1):
    """Inserta una clave en el segundo t y fija la interpolación del tramo que empieza ahí."""
    frame = F(t)
    cur = getattr(struct, prop)
    if index >= 0:
        cur[index] = value
    elif hasattr(cur, "__len__") and not isinstance(value, (int, float)):
        for i, v in enumerate(value):
            cur[i] = v
    else:
        setattr(struct, prop, value)
    struct.keyframe_insert(prop, index=index, frame=frame)
    path = struct.path_from_id(prop)
    for fc in _fcurves(owner):
        if fc.data_path == path and (index < 0 or fc.array_index == index):
            for p in fc.keyframe_points:
                if abs(p.co.x - frame) < 0.01:
                    p.interpolation = interp
                    p.easing = easing
                    if interp == "BACK":
                        p.back = 1.4
            if interp == "BEZIER":
                for p in fc.keyframe_points:
                    p.handle_left_type = p.handle_right_type = "AUTO_CLAMPED"


def ob_kf(ob, prop, t, value, interp="BEZIER", easing="EASE_IN_OUT", index=-1):
    kf(ob, ob, prop, t, value, interp, easing, index)


# ───────────────────────── Materiales ─────────────────────────
def mat_pbr(name, color, rough=0.4, metal=0.0, coat=0.0, emit=None, estr=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = color
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if "Coat Weight" in b.inputs:
        b.inputs["Coat Weight"].default_value = coat
    if emit:
        b.inputs["Emission Color"].default_value = emit
        b.inputs["Emission Strength"].default_value = estr
    return m


def mat_flat(name, color, strength=1.0, fade=1.0):
    """Material plano (emisión) con transparencia animable: nodes['Fade'].outputs[0]."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs[0].default_value = color
    em.inputs[1].default_value = strength
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    mix.name = "Mix"
    val = nt.nodes.new("ShaderNodeValue")
    val.name = "Fade"
    val.outputs[0].default_value = fade
    nt.links.new(val.outputs[0], mix.inputs[0])
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    try:
        m.surface_render_method = "BLENDED"
    except Exception:
        m.blend_method = "BLEND"
    return m


def fade(m, t, v, interp="BEZIER", easing="EASE_IN_OUT"):
    sock = m.node_tree.nodes["Fade"].outputs[0]
    kf(m.node_tree, sock, "default_value", t, v, interp, easing)


def fade_in_out(m, t_in, t_out=None, d=0.35):
    fade(m, 0.0, 0.0)
    fade(m, t_in, 0.0)
    fade(m, t_in + d, 1.0)
    if t_out is not None:
        fade(m, t_out, 1.0)
        fade(m, t_out + d, 0.0)


M_LOZA = mat_pbr("Loza", hexc("f2f3f1"), rough=0.18, coat=0.4)
M_ACERO = mat_pbr("Acero", hexc("b9c0c4"), rough=0.28, metal=1.0)
M_OSCURO = mat_pbr("Sensor", hexc("1a2228"), rough=0.4)
M_PERSONA = mat_pbr("Persona", hexc("8fa3b0"), rough=0.6)
M_ECO = mat_pbr("Eco", C_ECO, rough=0.3, emit=C_ECO, estr=3.0)


# ───────────────────────── Geometría ─────────────────────────
def link(ob):
    bpy.context.scene.collection.objects.link(ob)
    return ob


def mesh_obj(name, bm, mat=None, smooth=True, bevel=0.0, subsurf=0):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = link(bpy.data.objects.new(name, me))
    if mat:
        me.materials.append(mat)
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    if bevel:
        mod = ob.modifiers.new("Bevel", "BEVEL")
        mod.width = bevel
        mod.segments = 3
        mod.limit_method = "ANGLE"
    if subsurf:
        mod = ob.modifiers.new("Sub", "SUBSURF")
        mod.levels = mod.render_levels = subsurf
    return ob


def bm_box(sx, sy, sz):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(sx, sy, sz), verts=bm.verts)
    return bm


def bm_cone(r1, r2, d, seg=48):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r1, radius2=r2, depth=d)
    return bm


def bm_sphere(r, seg=32, rings=16):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=rings, radius=r)
    return bm


def capsule(name, r, length, mat):
    """Cápsula a lo largo de -Z desde el origen (para piernas, brazos)."""
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=24, v_segments=12, radius=r)
    for v in bm.verts:
        if v.co.z < 0:
            v.co.z -= length
    bmesh.ops.translate(bm, vec=(0, 0, 0), verts=bm.verts)
    return mesh_obj(name, bm, mat)


def empty(name, loc=(0, 0, 0), parent=None):
    e = link(bpy.data.objects.new(name, None))
    e.empty_display_size = 0.1
    e.location = loc
    if parent:
        e.parent = parent
    return e


def make_toilet(prefix, origin, autolid=False):
    """Inodoro estilizado. Frente = -Y. Devuelve dict con la bisagra de la tapa."""
    root = empty(prefix + "_root", origin)
    bm = bm_cone(0.135, 0.205, 0.40)
    bmesh.ops.scale(bm, vec=(1, 1.32, 1), verts=bm.verts)
    bowl = mesh_obj(prefix + "_taza", bm, M_LOZA, bevel=0.02, subsurf=1)
    bowl.parent = root
    bowl.location = (0, 0, 0.20)
    # Interior oscuro de la taza
    bm = bm_cone(0.13, 0.17, 0.02)
    bmesh.ops.scale(bm, vec=(1, 1.3, 1), verts=bm.verts)
    agua = mesh_obj(prefix + "_agua", bm, mat_pbr(prefix + "_aguaM", hexc("9fc6cf"), rough=0.05), smooth=True)
    agua.parent = root
    agua.location = (0, -0.01, 0.395)
    # Asiento
    bpy.ops.mesh.primitive_torus_add(major_radius=0.168, minor_radius=0.024, major_segments=48, minor_segments=12)
    seat = bpy.context.active_object
    seat.name = prefix + "_asiento"
    seat.scale = (1, 1.3, 0.55)
    seat.data.materials.append(M_LOZA)
    for p in seat.data.polygons:
        p.use_smooth = True
    seat.parent = root
    seat.location = (0, 0, 0.413)
    # Mochila
    tank = mesh_obj(prefix + "_mochila", bm_box(0.44, 0.17, 0.40), M_LOZA, bevel=0.03)
    tank.parent = root
    tank.location = (0, 0.36, 0.62)
    tapa_m = mesh_obj(prefix + "_tapaMochila", bm_box(0.46, 0.19, 0.03), M_LOZA, bevel=0.012)
    tapa_m.parent = root
    tapa_m.location = (0, 0.36, 0.835)
    boton = mesh_obj(prefix + "_boton", bm_cone(0.025, 0.025, 0.012), M_ACERO)
    boton.parent = root
    boton.location = (0, 0.36, 0.855)
    # Tapa con bisagra (rota en X; negativo = abre)
    hinge = empty(prefix + "_bisagra", (0, 0.245, 0.432), root)
    bm = bm_cone(0.205, 0.205, 0.026)
    bmesh.ops.scale(bm, vec=(1, 1.3, 1), verts=bm.verts)
    lid = mesh_obj(prefix + "_tapa", bm, M_LOZA, bevel=0.01, subsurf=1)
    lid.parent = hinge
    lid.location = (0, -0.245, 0.013)
    parts = {"root": root, "hinge": hinge, "lid": lid, "seat": seat}
    if autolid:
        box = mesh_obj(prefix + "_autolid", bm_box(0.115, 0.10, 0.09), M_ACERO, bevel=0.012)
        box.parent = root
        box.location = (0.255, 0.245, 0.43)
        led = mesh_obj(prefix + "_led", bm_sphere(0.008, 12, 6), mat_flat(prefix + "_ledM", C_ECO, 6.0))
        led.parent = box
        led.location = (0, -0.051, 0.02)
        arm = mesh_obj(prefix + "_pletina", bm_box(0.06, 0.16, 0.012), M_ACERO, bevel=0.004)
        arm.parent = hinge
        arm.location = (0.19, -0.07, 0.018)
        # Sensor frontal HC-SR04
        sen = mesh_obj(prefix + "_sensor", bm_box(0.075, 0.02, 0.035), M_OSCURO, bevel=0.004)
        sen.parent = root
        sen.location = (0, -0.272, 0.30)
        for dx in (-0.019, 0.019):
            eye = mesh_obj(prefix + "_ojo", bm_cone(0.012, 0.012, 0.012), M_ACERO)
            eye.parent = sen
            eye.rotation_euler = (radians(90), 0, 0)
            eye.location = (dx, -0.012, 0)
        # Sensor de peso FSR (se ilumina)
        fsr_m = mat_pbr(prefix + "_fsrM", hexc("5d6870"), rough=0.4, emit=C_BLOQ, estr=0.0)
        bm = bm_cone(0.03, 0.03, 0.004)
        fsr = mesh_obj(prefix + "_fsr", bm, fsr_m)
        fsr.parent = root
        fsr.location = (-0.12, -0.12, 0.428)
        parts.update(box=box, sensor=sen, fsr=fsr, fsr_mat=fsr_m)
    return parts


def make_person(prefix, loc, rot_z=0.0):
    """Figura articulada simple. Mira hacia -Y con rot_z = 0. Origen en la cadera."""
    root = empty(prefix + "_root", loc)
    root.rotation_euler = (0, 0, rot_z)
    torso = capsule(prefix + "_torso", 0.15, 0.36, M_PERSONA)
    torso.parent = root
    torso.rotation_euler = (radians(180), 0, 0)
    torso.location = (0, 0, 0.12)
    head = mesh_obj(prefix + "_cabeza", bm_sphere(0.11), M_PERSONA)
    head.parent = root
    head.location = (0, 0, 0.78)
    legs = {}
    for side, x in (("L", -0.085), ("R", 0.085)):
        hip = empty(f"{prefix}_cadera{side}", (x, 0, 0.02), root)
        thigh = capsule(f"{prefix}_muslo{side}", 0.07, 0.36, M_PERSONA)
        thigh.parent = hip
        knee = empty(f"{prefix}_rodilla{side}", (0, 0, -0.42), hip)
        shin = capsule(f"{prefix}_pierna{side}", 0.06, 0.36, M_PERSONA)
        shin.parent = knee
        legs[side] = (hip, knee)
    for side, x in (("L", -0.2), ("R", 0.2)):
        sh = empty(f"{prefix}_hombro{side}", (x, 0, 0.55), root)
        arm = capsule(f"{prefix}_brazo{side}", 0.055, 0.42, M_PERSONA)
        arm.parent = sh
        legs["arm" + side] = sh
    return {"root": root, "legs": legs, "torso": torso}


def walk(person, t0, t1, step=0.36, amp=24):
    """Balanceo de piernas y brazos mientras camina."""
    legs = person["legs"]
    n = int((t1 - t0) / step)
    for i in range(n + 1):
        t = t0 + i * step
        s = 1 if i % 2 == 0 else -1
        a = amp if i not in (0, n) else 0
        ob_kf(legs["L"][0], "rotation_euler", t, radians(a * s), index=0)
        ob_kf(legs["R"][0], "rotation_euler", t, radians(-a * s), index=0)
        ob_kf(legs["L"][1], "rotation_euler", t, radians(max(0, -a * s) * 0.8), index=0)
        ob_kf(legs["R"][1], "rotation_euler", t, radians(max(0, a * s) * 0.8), index=0)
        ob_kf(legs["armL"], "rotation_euler", t, radians(-a * s * 0.7), index=0)
        ob_kf(legs["armR"], "rotation_euler", t, radians(a * s * 0.7), index=0)


def pose(person, t, sit, d=0.0):
    """sit=0 de pie, sit=1 sentado (muslos hacia adelante = -Y)."""
    legs = person["legs"]
    for side in ("L", "R"):
        ob_kf(legs[side][0], "rotation_euler", t, radians(-88 * sit), index=0)
        ob_kf(legs[side][1], "rotation_euler", t, radians(88 * sit), index=0)
    for side in ("armL", "armR"):
        ob_kf(legs[side], "rotation_euler", t, radians(-25 * sit), index=0)


def plane(name, sx, sy, mat, loc, rot=(0, 0, 0)):
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.5)
    bmesh.ops.scale(bm, vec=(sx, sy, 1), verts=bm.verts)
    ob = mesh_obj(name, bm, mat, smooth=False)
    ob.location = loc
    ob.rotation_euler = rot
    return ob


def area_light(name, loc, energy, size, color=(1, 1, 1), target=None, spot=False):
    ld = bpy.data.lights.new(name, "SPOT" if spot else "AREA")
    ld.energy = energy
    ld.color = color[:3]
    if spot:
        ld.spot_size = radians(38)
        ld.spot_blend = 0.6
        ld.shadow_soft_size = size
    else:
        ld.size = size
    ob = link(bpy.data.objects.new(name, ld))
    ob.location = loc
    if target:
        c = ob.constraints.new("TRACK_TO")
        c.target = target
        c.track_axis = "TRACK_NEGATIVE_Z"
        c.up_axis = "UP_Y"
    return ob


# ───────────────────────── Cámaras + HUD ─────────────────────────
FADER = mat_flat("Fader", hexc("05080a"), 1.0, fade=1.0)
CAMS = []


def camera(name, loc, target_loc, lens=40):
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    cd.clip_start = 0.05
    cd.clip_end = 60
    cam = link(bpy.data.objects.new(name, cd))
    cam.location = loc
    tgt = empty(name + "_obj", target_loc)
    c = cam.constraints.new("TRACK_TO")
    c.target = tgt
    c.track_axis = "TRACK_NEGATIVE_Z"
    c.up_axis = "UP_Y"
    fp = plane(name + "_fader", 2, 2, FADER, (0, 0, -0.15))
    fp.parent = cam
    CAMS.append(cam)
    return cam, tgt


def hud_text(cam, body, fx, fy, size, color, font=None, align="LEFT", name=None, valign="CENTER", fade_val=0.0, strength=1.0):
    """Texto pegado a la cámara. fx: -0.5..0.5 del ancho; fy: -0.28..0.28; size en fracción del ancho."""
    W = 36.0 / cam.data.lens  # ancho visible a 1 m
    cu = bpy.data.curves.new(name or ("t_" + body[:12]), "FONT")
    cu.body = body
    cu.font = font or FONT_B
    cu.size = size * W
    cu.align_x = align
    cu.align_y = valign
    cu.space_line = 1.05
    ob = link(bpy.data.objects.new(name or ("t_" + body[:12]), cu))
    m = mat_flat("m_" + ob.name, color, strength, fade=fade_val)
    cu.materials.append(m)
    ob.parent = cam
    ob.location = (fx * W, fy * W, -1.0)
    ob["W"] = W
    return ob, m


def hud_slide(ob, m, t_in, t_out=None, dy=0.02, d=0.45):
    """Entra subiendo con fundido y sale con fundido."""
    W = ob["W"]
    y = ob.location.y
    ob_kf(ob, "location", 0.0, y - dy * W, index=1)
    ob_kf(ob, "location", t_in, y - dy * W, index=1)
    ob_kf(ob, "location", t_in + d, y, "EXPO", "EASE_OUT", index=1)
    fade(m, 0.0, 0.0)
    fade(m, t_in, 0.0)
    fade(m, t_in + d * 0.8, 1.0)
    if t_out is not None:
        ob_kf(ob, "location", t_out, y, index=1)
        ob_kf(ob, "location", t_out + d, y + dy * W, "EXPO", "EASE_IN", index=1)
        fade(m, t_out, 1.0)
        fade(m, t_out + d * 0.8, 0.0)


def world_color(t, col, strength=1.0):
    kf(world.node_tree, bg.inputs[0], "default_value", t, col, "CONSTANT")
    kf(world.node_tree, bg.inputs[1], "default_value", t, strength, "CONSTANT")


# ═════════════════════════ ESCENA A (0–6 s): el problema ═════════════════════════
A = Vector((0, 0, 0))
world_color(0.0, hexc("06090b"), 1.0)
pisoA = plane("A_piso", 8, 8, mat_pbr("A_pisoM", hexc("1b2329"), rough=0.35), A + Vector((0, 0, 0)))
paredA = plane("A_pared", 8, 4, mat_pbr("A_paredM", hexc("161d22"), rough=0.6), A + Vector((0, 0.62, 2)), (radians(90), 0, 0))
tA = make_toilet("A", A)
spotA = area_light("A_spot", A + Vector((0.6, -0.6, 2.6)), 900, 0.4, color=hexc("ffe6c8"), target=tA["root"], spot=True)
rimA = area_light("A_rim", A + Vector((-1.6, 1.2, 1.4)), 120, 1.5, color=hexc("7fb8ff"), target=tA["root"])
camA, tgtA = camera("CamA", A + Vector((1.9, -2.7, 1.25)), A + Vector((-0.32, 0, 0.42)), lens=42)
ob_kf(camA, "location", 0.0, A + Vector((1.9, -2.7, 1.25)), "LINEAR")
ob_kf(camA, "location", 6.0, A + Vector((1.15, -1.75, 0.95)), "LINEAR")
# La tapa intenta subir y vuelve a caer (no es tan simple)
h = tA["hinge"]
for t, a, ip, ez in ((0.0, 0, "BEZIER", "EASE_IN_OUT"), (2.55, 0, "SINE", "EASE_OUT"), (2.85, -9, "QUAD", "EASE_IN"),
                     (3.05, 0, "BOUNCE", "EASE_OUT"), (3.5, 0, "SINE", "EASE_OUT"), (3.85, -14, "QUAD", "EASE_IN"),
                     (4.1, 0, "BOUNCE", "EASE_OUT"), (4.5, 0, "BEZIER", "EASE_IN_OUT")):
    ob_kf(h, "rotation_euler", t, radians(a), ip, ez, index=0)
tx1, m1 = hud_text(camA, "Levantar la tapa.", -0.43, 0.06, 0.055, C_BLANCO, FONT_B, name="A_t1")
hud_slide(tx1, m1, 0.9, 5.5)
tx2, m2 = hud_text(camA, "Para millones,\nno es tan simple.", -0.43, -0.07, 0.042, C_ECO, FONT_B, name="A_t2")
hud_slide(tx2, m2, 3.2, 5.5)

# ═════════════════════════ ESCENA B (6–17 s): los datos ═════════════════════════
B = Vector((100, 0, 0))
camB, tgtB = camera("CamB", B + Vector((0, -6.0, 1.15)), B + Vector((0, 0, 1.15)), lens=50)
ob_kf(camB, "location", 6.0, B + Vector((0.15, -6.3, 1.15)), "LINEAR")
ob_kf(camB, "location", 17.0, B + Vector((-0.15, -5.7, 1.15)), "LINEAR")
fondoB = plane("B_fondo", 14, 8, mat_flat("B_fondoM", hexc("0c1a23"), 1.0, fade=1.0), B + Vector((0, 1.5, 1.2)), (radians(90), 0, 0))
# grilla sutil
for i in range(-6, 7):
    g = plane(f"B_linea{i}", 0.006, 8, mat_flat(f"B_lm{i}", hexc("16303c"), 1.0, fade=1.0), B + Vector((i * 0.6, 1.45, 1.2)), (radians(90), 0, 0))

def text3d(name, body, loc, size, color, font=FONT_B, align="CENTER", strength=1.0, extrude=0.0, fade_val=0.0):
    cu = bpy.data.curves.new(name, "FONT")
    cu.body = body
    cu.font = font
    cu.size = size
    cu.align_x = align
    cu.align_y = "CENTER"
    cu.extrude = extrude
    ob = link(bpy.data.objects.new(name, cu))
    m = mat_flat("m_" + name, color, strength, fade=fade_val)
    cu.materials.append(m)
    ob.location = loc
    ob.rotation_euler = (radians(90), 0, 0)
    return ob, m


def stat_group(prefix, t_in, t_out):
    g = empty(prefix, B + Vector((0, 0, 0)))
    # entra desde la derecha con rebote suave, sale hacia la izquierda
    ob_kf(g, "location", 0.0, B + Vector((5.5, 0, 0)), "CONSTANT")
    ob_kf(g, "location", t_in, B + Vector((5.5, 0, 0)), "BACK", "EASE_OUT")
    ob_kf(g, "location", t_in + 0.7, B + Vector((0, 0, 0)), "LINEAR")
    if t_out:
        ob_kf(g, "location", t_out, B + Vector((0, 0, 0)), "EXPO", "EASE_IN")
        ob_kf(g, "location", t_out + 0.55, B + Vector((-6, 0, 0)), "LINEAR")
    return g


def child(ob, parent):
    ob.parent = parent
    ob.location = ob.location - parent.location if parent.location.length > 50 else ob.location
    return ob


M_ICON = mat_pbr("Icono", hexc("5e7280"), rough=0.5)
M_ICON_ON = mat_pbr("IconoOn", C_ECO, rough=0.3, emit=C_ECO, estr=0.0)


def figure_icon(name, x, z, mat, parent):
    root = empty(name, (x, 0, z), parent)
    head = mesh_obj(name + "_c", bm_sphere(0.085, 24, 12), mat)
    head.parent = root
    head.location = (0, 0, 0.36)
    body = capsule(name + "_b", 0.11, 0.2, mat)
    body.parent = root
    body.location = (0, 0, 0.18)
    return root


def house_icon(name, x, z, mat, parent):
    root = empty(name, (x, 0, z), parent)
    base = mesh_obj(name + "_b", bm_box(0.42, 0.25, 0.32), mat, bevel=0.02)
    base.parent = root
    base.location = (0, 0, 0.16)
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=4, radius1=0.36, radius2=0.0, depth=0.24)
    bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=__import__("mathutils").Matrix.Rotation(radians(45), 3, "Z"))
    bmesh.ops.scale(bm, vec=(1, 0.5, 1), verts=bm.verts)
    roof = mesh_obj(name + "_r", bm, mat, smooth=False, bevel=0.01)
    roof.parent = root
    roof.location = (0, 0, 0.44)
    return root


def glow(mat, t, on=True):
    b = mat.node_tree.nodes["Principled BSDF"]
    kf(mat.node_tree, b.inputs["Emission Strength"], "default_value", t, 0.0)
    kf(mat.node_tree, b.inputs["Emission Strength"], "default_value", t + 0.35, 2.5 if on else 0.0)


# Dato 1: 1 de cada 10
g1 = stat_group("B_g1", 6.35, 9.7)
n1, mn1 = text3d("B_n1", "1 de cada 10", B + Vector((0, 0, 1.95)), 0.55, C_BLANCO, FONT_X, fade_val=1.0)
n1.parent = g1; n1.location = (0, 0, 1.95)
l1, ml1 = text3d("B_l1", "argentinos vive con alguna discapacidad", (0, 0, 0.42), 0.17, hexc("c9d6dc"), FONT_R, fade_val=1.0)
l1.parent = g1
s1, ms1 = text3d("B_s1", "INDEC · Estudio Nacional sobre el Perfil de las Personas con Discapacidad, 2018", (0, 0, 0.12), 0.075, hexc("6f8793"), FONT_R, fade_val=1.0)
s1.parent = g1
M_ON1 = mat_pbr("IconoOn1", hexc("8fa3b0"), rough=0.4, emit=C_ECO, estr=0.0)
for i in range(10):
    x = (i - 4.5) * 0.36
    fig = figure_icon(f"B_fig{i}", x, 0.75, M_ON1 if i == 3 else M_ICON, g1)
    if i == 3:
        ob_kf(fig, "location", 7.2, 0.75, "BACK", "EASE_OUT", index=2)
        ob_kf(fig, "location", 7.55, 0.92, "BOUNCE", "EASE_OUT", index=2)
        ob_kf(fig, "location", 8.1, 0.75, index=2)
        ob_kf(fig, "scale", 7.2, (1, 1, 1), "BACK", "EASE_OUT")
        ob_kf(fig, "scale", 7.6, (1.25, 1.25, 1.25))
glow(M_ON1, 7.2)
kf(M_ON1.node_tree, M_ON1.node_tree.nodes["Principled BSDF"].inputs["Base Color"], "default_value", 7.2, hexc("8fa3b0"))
kf(M_ON1.node_tree, M_ON1.node_tree.nodes["Principled BSDF"].inputs["Base Color"], "default_value", 7.55, C_ECO)

# Dato 2: 1 de cada 4 hogares
g2 = stat_group("B_g2", 9.75, 13.05)
n2, _ = text3d("B_n2", "1 de cada 4", (0, 0, 1.95), 0.55, C_BLANCO, FONT_X, fade_val=1.0)
n2.parent = g2
l2, _ = text3d("B_l2", "hogares tiene una persona con discapacidad", (0, 0, 0.42), 0.17, hexc("c9d6dc"), FONT_R, fade_val=1.0)
l2.parent = g2
s2, _ = text3d("B_s2", "INDEC, 2018", (0, 0, 0.12), 0.075, hexc("6f8793"), FONT_R, fade_val=1.0)
s2.parent = g2
M_ON2 = mat_pbr("IconoOn2", hexc("8fa3b0"), rough=0.4, emit=C_ECO, estr=0.0)
for i in range(4):
    x = (i - 1.5) * 0.75
    hs = house_icon(f"B_casa{i}", x, 0.7, M_ON2 if i == 2 else M_ICON, g2)
    if i == 2:
        ob_kf(hs, "scale", 10.6, (1, 1, 1), "BACK", "EASE_OUT")
        ob_kf(hs, "scale", 11.0, (1.18, 1.18, 1.18))
glow(M_ON2, 10.6)
kf(M_ON2.node_tree, M_ON2.node_tree.nodes["Principled BSDF"].inputs["Base Color"], "default_value", 10.6, hexc("8fa3b0"))
kf(M_ON2.node_tree, M_ON2.node_tree.nodes["Principled BSDF"].inputs["Base Color"], "default_value", 10.95, C_ECO)

# Dato 3: +5,5 millones de 65 años o más (contador)
g3 = stat_group("B_g3", 13.1, 16.6)
n3, _ = text3d("B_n3", "+5,5 millones", (0, 0, 1.55), 0.52, C_ECO, FONT_X, fade_val=1.0, strength=1.2)
n3.parent = g3
l3, _ = text3d("B_l3", "de argentinos tienen 65 años o más", (0, 0, 0.78), 0.17, hexc("c9d6dc"), FONT_R, fade_val=1.0)
l3.parent = g3
s3, _ = text3d("B_s3", "INDEC · Censo 2022 (11,9 % de 46,2 millones)", (0, 0, 0.12), 0.075, hexc("6f8793"), FONT_R, fade_val=1.0)
s3.parent = g3
barra = mesh_obj("B_barra", bm_box(1, 0.04, 0.05), M_ECO, bevel=0.01)
barra.parent = g3
barra.location = (0, 0, 1.08)
ob_kf(barra, "scale", 0.0, (0.001, 1, 1), "CONSTANT")
ob_kf(barra, "scale", 13.4, (0.001, 1, 1), "EXPO", "EASE_OUT")
ob_kf(barra, "scale", 14.7, (3.2, 1, 1))

COUNT = (F(13.3), F(14.6))


def contador(scene, *_):
    f = scene.frame_current
    if f <= COUNT[0]:
        v = 0.0
    elif f >= COUNT[1]:
        v = 5.5
    else:
        x = (f - COUNT[0]) / (COUNT[1] - COUNT[0])
        v = 5.5 * (1 - (1 - x) ** 3)
    txt = f"+{v:.1f}".replace(".", ",") + " millones"
    ob = bpy.data.objects.get("B_n3")
    if ob and ob.data.body != txt:
        ob.data.body = txt


bpy.app.handlers.frame_change_pre.clear()
bpy.app.handlers.frame_change_pre.append(contador)

area_light("B_luz", B + Vector((0, -4, 4)), 600, 6, target=g1)

# ═════════════════════════ ESCENA C (17–23 s): gérmenes ═════════════════════════
C = Vector((200, 0, 0))
pisoC = plane("C_piso", 12, 12, mat_pbr("C_pisoM", hexc("1a242b"), rough=0.4), C)
paredC = plane("C_pared", 12, 5, mat_pbr("C_paredM", hexc("141c22"), rough=0.6), C + Vector((-1.2, 0, 2.5)), (radians(90), 0, radians(90)))
tC = make_toilet("C", C)
tC["hinge"].rotation_euler = (radians(-100), 0, 0)
area_light("C_key", C + Vector((2.0, -1.5, 3.0)), 700, 2.0, color=hexc("fff1e0"), target=tC["root"])
area_light("C_fill", C + Vector((3.0, -3.0, 1.0)), 120, 3.0, color=hexc("8ac8ff"), target=tC["root"])
camC, tgtC = camera("CamC", C + Vector((5.2, -0.6, 1.25)), C + Vector((0, -0.9, 0.85)), lens=34)
ob_kf(camC, "location", 17.0, C + Vector((5.2, -0.4, 1.25)), "LINEAR")
ob_kf(camC, "location", 23.0, C + Vector((4.6, -0.9, 1.15)), "LINEAR")
import random
random.seed(3)
M_GERM = mat_flat("C_germM", hexc("9be36a"), 2.5, fade=1.0)
M_GERM2 = mat_flat("C_germM2", hexc("5ed2b8"), 2.5, fade=1.0)
for m in (M_GERM, M_GERM2):
    fade(m, 17.0, 1.0)
    fade(m, 21.6, 1.0)
    fade(m, 22.6, 0.0)
t_burst = 18.45
src = C + Vector((0, -0.02, 0.45))
for i in range(260):
    r = 0.012 + random.random() * 0.02
    ob = mesh_obj(f"C_g{i}", bm_sphere(r, 8, 4), M_GERM if i % 3 else M_GERM2)
    th = random.uniform(-pi, pi)
    reach = 0.4 + random.random() ** 0.6 * 1.75
    dirx = cos(th) * 0.55
    diry = -abs(sin(th)) * 1.0 - 0.3 if random.random() < 0.75 else sin(th) * 0.6
    v = Vector((dirx, diry, 0)).normalized() * reach
    end = src + Vector((v.x, v.y, 0.15 + random.random() * 1.35 * (1 - reach / 2.4) + 0.2))
    delay = random.random() * 0.5
    ob.location = src
    ob_kf(ob, "location", 0.0, src, "CONSTANT")
    ob_kf(ob, "location", t_burst + delay, src, "EXPO", "EASE_OUT")
    ob_kf(ob, "location", t_burst + delay + 1.6 + random.random() * 0.6, end, "SINE", "EASE_IN_OUT")
    ob_kf(ob, "location", 22.8, end + Vector((0, 0, -0.25)))
    ob_kf(ob, "scale", 0.0, (0.01, 0.01, 0.01), "CONSTANT")
    ob_kf(ob, "scale", t_burst + delay, (0.2, 0.2, 0.2), "BACK", "EASE_OUT")
    ob_kf(ob, "scale", t_burst + delay + 0.4, (1, 1, 1))
# Regla de 2 m
M_REGLA = mat_flat("C_reglaM", C_BLANCO, 1.0, fade=0.0)
regla = mesh_obj("C_regla", bm_box(0.012, 1, 0.012), None)
regla.data.materials.append(M_REGLA)
regla.location = C + Vector((0.32, -1.0, 0.03))
ob_kf(regla, "scale", 0.0, (1, 0.001, 1), "CONSTANT")
ob_kf(regla, "scale", 19.6, (1, 0.001, 1), "EXPO", "EASE_OUT")
ob_kf(regla, "scale", 20.6, (1, 2.0, 1))
fade_in_out(M_REGLA, 19.5, 22.5)
for k in range(5):
    tk = mesh_obj(f"C_tick{k}", bm_box(0.012, 0.012, 0.07), None)
    tk.data.materials.append(M_REGLA)
    tk.location = C + Vector((0.32, -0.5 * k, 0.05))
rot2, mr2 = text3d("C_2m", "2 m", C + Vector((0.34, -2.0, 0.22)), 0.22, C_BLANCO, FONT_B)
rot2.rotation_euler = (radians(90), 0, radians(90))
fade_in_out(mr2, 20.3, 22.5)
cx1, mc1 = hud_text(camC, "Hasta 2 metros", 0.44, 0.2, 0.06, C_BLANCO, FONT_X, align="RIGHT", name="C_t1")
hud_slide(cx1, mc1, 19.0, 22.4)
cx2, mc2 = hud_text(camC, "viajan los gérmenes al tirar la cadena\ncon la tapa abierta", 0.44, 0.125, 0.026, hexc("c9d6dc"), FONT_R, align="RIGHT", name="C_t2")
hud_slide(cx2, mc2, 19.3, 22.4)
cx3, mc3 = hud_text(camC, "Best et al., 2012 · Johnson et al., 2013", 0.44, -0.25, 0.014, hexc("6f8793"), FONT_R, align="RIGHT", name="C_t3")
hud_slide(cx3, mc3, 19.5, 22.4)

# ═════════════════════════ ESCENA D (23–36 s): AutoLID ═════════════════════════
D = Vector((300, 0, 0))
M_PISO_D = mat_pbr("D_pisoM", hexc("b9c3c5"), rough=0.25)
M_PARED_D = bpy.data.materials.new("D_azulejos")
M_PARED_D.use_nodes = True
nt = M_PARED_D.node_tree
bsdf = nt.nodes["Principled BSDF"]
brick = nt.nodes.new("ShaderNodeTexBrick")
brick.offset = 0.0
brick.inputs["Color1"].default_value = hexc("dfe5e6")
brick.inputs["Color2"].default_value = hexc("d6dddf")
brick.inputs["Mortar"].default_value = hexc("a7b3b6")
brick.inputs["Scale"].default_value = 6.0
brick.inputs["Mortar Size"].default_value = 0.012
brick.inputs["Brick Width"].default_value = 0.5
brick.inputs["Row Height"].default_value = 0.25
coord = nt.nodes.new("ShaderNodeTexCoord")
nt.links.new(coord.outputs["Object"], brick.inputs["Vector"])
nt.links.new(brick.outputs["Color"], bsdf.inputs["Base Color"])
bsdf.inputs["Roughness"].default_value = 0.2
pisoD = plane("D_piso", 10, 10, M_PISO_D, D)
paredD = plane("D_pared", 10, 4, M_PARED_D, D + Vector((0, 0.47, 2)), (radians(90), 0, 0))
paredD2 = plane("D_pared2", 10, 4, M_PARED_D, D + Vector((-2.8, 0, 2)), (radians(90), 0, radians(90)))
tD = make_toilet("D", D, autolid=True)
area_light("D_key", D + Vector((1.8, -1.6, 2.8)), 380, 2.5, color=hexc("fff4e8"), target=tD["root"])
area_light("D_fill", D + Vector((-1.0, -2.8, 1.6)), 90, 3.0, color=hexc("e6f4ff"), target=tD["root"])
area_light("D_top", D + Vector((0, -0.4, 3.2)), 120, 2.0, target=tD["root"])
world_color(23.0 - 0.0, hexc("dfe7ea"), 0.12)
world_color(CUTS[3], hexc("081218"), 1.0)
world_color(6.0, hexc("081218"), 1.0)
world_color(17.0, hexc("06090b"), 1.0)

camD, tgtD = camera("CamD", D + Vector((2.6, -1.2, 0.9)), D + Vector((0, -0.05, 0.5)), lens=32)
# Revelación orbital y luego plano estable de 3/4
ob_kf(camD, "location", 23.0, D + Vector((2.4, -0.9, 0.75)), "SINE", "EASE_OUT")
ob_kf(camD, "location", 25.3, D + Vector((1.75, -1.9, 1.05)), "BEZIER")
ob_kf(camD, "location", 27.2, D + Vector((2.7, -2.4, 1.45)), "BEZIER")
ob_kf(camD, "location", 36.0, D + Vector((2.85, -2.6, 1.5)), "LINEAR")
ob_kf(tgtD, "location", 23.0, D + Vector((0.12, 0.05, 0.48)), "BEZIER")
ob_kf(tgtD, "location", 25.3, D + Vector((0.15, 0.0, 0.5)), "BEZIER")
ob_kf(tgtD, "location", 27.2, D + Vector((-0.1, -0.45, 0.78)), "BEZIER")
ob_kf(tgtD, "location", 36.0, D + Vector((-0.1, -0.5, 0.78)))

# Brillo de la caja AutoLID al presentarla
M_HALO = mat_flat("D_haloM", C_ECO, 2.0, fade=0.0)
bm = bmesh.new()
bmesh.ops.create_circle(bm, cap_ends=True, segments=48, radius=0.12)
halo = mesh_obj("D_halo", bm, M_HALO, smooth=False)
halo.parent = tD["box"]
halo.location = (0, 0, 0.0475 + 0.002)
ob_kf(halo, "scale", 25.4, (0.6, 0.6, 0.6), "EXPO", "EASE_OUT")
ob_kf(halo, "scale", 26.4, (1.8, 1.8, 1.8))
fade(M_HALO, 0.0, 0.0)
fade(M_HALO, 25.4, 0.0)
fade(M_HALO, 25.55, 0.8)
fade(M_HALO, 26.4, 0.0)

# Persona
P = make_person("D_p", D + Vector((-1.15, -1.95, 0.9)), radians(132))
pr = P["root"]
ob_kf(pr, "location", 0.0, D + Vector((-1.15, -1.95, 0.9)), "CONSTANT")
ob_kf(pr, "location", 27.3, D + Vector((-1.15, -1.95, 0.9)), "SINE", "EASE_OUT")
ob_kf(pr, "location", 28.9, D + Vector((0.05, -0.86, 0.9)))
ob_kf(pr, "rotation_euler", 27.3, radians(132), index=2)
ob_kf(pr, "rotation_euler", 28.9, radians(180), index=2)
walk(P, 27.3, 28.9)
# gira y se sienta (después de que abre la tapa)
ob_kf(pr, "location", 30.5, D + Vector((0.05, -0.86, 0.9)), "SINE", "EASE_IN_OUT")
ob_kf(pr, "rotation_euler", 30.5, radians(180), index=2)
ob_kf(pr, "rotation_euler", 31.0, radians(360), index=2)
ob_kf(pr, "location", 31.0, D + Vector((0.05, -0.5, 0.9)), "SINE", "EASE_IN_OUT")
ob_kf(pr, "location", 31.55, D + Vector((0.05, -0.04, 0.53)))
pose(P, 30.9, 0)
pose(P, 31.55, 1)
# se levanta y se va hacia la derecha del cuadro
ob_kf(pr, "location", 32.6, D + Vector((0.05, -0.04, 0.53)), "SINE", "EASE_IN_OUT")
pose(P, 32.6, 1)
ob_kf(pr, "location", 33.15, D + Vector((0.1, -0.6, 0.9)), "LINEAR")
pose(P, 33.15, 0)
ob_kf(pr, "rotation_euler", 33.15, radians(360), index=2)
ob_kf(pr, "rotation_euler", 33.5, radians(320), index=2)
ob_kf(pr, "location", 34.4, D + Vector((-1.3, -2.3, 0.9)), "SINE", "EASE_IN")
walk(P, 33.15, 34.4)
ob_kf(pr, "location", 36.0, D + Vector((-2.4, -3.6, 0.9)))

# Tapa: abre 29.0–30.6 y cierra 34.0–35.4 (servo suave)
hD = tD["hinge"]
ob_kf(hD, "rotation_euler", 0.0, 0.0, "CONSTANT", index=0)
ob_kf(hD, "rotation_euler", 29.0, 0.0, "SINE", "EASE_IN_OUT", index=0)
ob_kf(hD, "rotation_euler", 30.6, radians(-98), "CONSTANT", index=0)
ob_kf(hD, "rotation_euler", 34.0, radians(-98), "SINE", "EASE_IN_OUT", index=0)
ob_kf(hD, "rotation_euler", 35.4, 0.0, index=0)

# Ondas del ultrasonido
M_ONDA = mat_flat("D_ondaM", C_ECO, 2.0, fade=0.0)
for k, t0 in enumerate((28.3, 28.7, 29.1, 29.5)):
    bpy.ops.mesh.primitive_torus_add(major_radius=0.1, minor_radius=0.004, major_segments=48, minor_segments=6)
    ring = bpy.context.active_object
    ring.name = f"D_onda{k}"
    ring.data.materials.append(M_ONDA if k == 0 else M_ONDA.copy())
    mk = ring.data.materials[0]
    ring.parent = tD["sensor"]
    ring.location = (0, -0.02, 0)
    ring.rotation_euler = (radians(90), 0, 0)
    ob_kf(ring, "scale", 0.0, (0.1, 0.1, 0.1), "CONSTANT")
    ob_kf(ring, "scale", t0, (0.2, 0.2, 0.2), "QUAD", "EASE_OUT")
    ob_kf(ring, "scale", t0 + 0.9, (4.5, 4.5, 4.5))
    ob_kf(ring, "location", t0, -0.02, "QUAD", "EASE_OUT", index=1)
    ob_kf(ring, "location", t0 + 0.9, -0.45, index=1)
    fade(mk, 0.0, 0.0)
    fade(mk, t0, 0.0)
    fade(mk, t0 + 0.08, 0.9)
    fade(mk, t0 + 0.9, 0.0)

# FSR se ilumina (alguien sentado)
fb = tD["fsr_mat"].node_tree
es = fb.nodes["Principled BSDF"].inputs["Emission Strength"]
kf(fb, es, "default_value", 0.0, 0.0, "CONSTANT")
kf(fb, es, "default_value", 31.45, 0.0, "BACK", "EASE_OUT")
kf(fb, es, "default_value", 31.75, 6.0)
kf(fb, es, "default_value", 32.6, 6.0)
kf(fb, es, "default_value", 32.9, 0.0)

# Textos de la escena D
dA, mdA = hud_text(camD, "Auto", -0.43, 0.19, 0.075, C_TINTA, FONT_X, name="D_auto")
dL, mdL = hud_text(camD, "LID", -0.43, 0.19, 0.075, C_ECO_D, FONT_X, name="D_lid")
bpy.context.view_layer.update()
dL.location.x = dA.location.x + dA.dimensions.x + 0.003
hud_slide(dA, mdA, 23.4, 26.9)
hud_slide(dL, mdL, 23.4, 26.9)
dt2, md2 = hud_text(camD, "Se instala en minutos.\nSin obra. Sin cables a 220 V.", -0.43, 0.1, 0.03, C_TINTA, FONT_B, name="D_t2")
hud_slide(dt2, md2, 25.5, 26.9)

def step_caption(name, txt, color, t_in, t_out, y=-0.205):
    ob, m = hud_text(camD, txt, -0.43, y, 0.036, color, FONT_B, name=name)
    hud_slide(ob, m, t_in, t_out)
    return ob

step_caption("D_c1", "Te acercás: se abre sola.", C_ECO_D, 28.0, 30.5)
step_caption("D_c2", "Te sentás: no se cierra.", hexc("c2541a"), 30.85, 32.75)
step_caption("D_c3", "Te vas: se cierra sola.", C_ECO_D, 32.95, 35.6)
sub, msub = hud_text(camD, "Sensor de peso bajo el asiento: el cierre queda bloqueado.", -0.43, -0.25, 0.021, C_TINTA, FONT_B, name="D_c2b")
hud_slide(sub, msub, 31.4, 32.75)

# ═════════════════════════ ESCENA E (36–42 s): cierre ═════════════════════════
E = Vector((400, 0, 0))
camE, tgtE = camera("CamE", E + Vector((0, -6.0, 1.1)), E + Vector((0, 0, 1.1)), lens=50)
ob_kf(camE, "location", 36.0, E + Vector((0, -6.4, 1.1)), "SINE", "EASE_OUT")
ob_kf(camE, "location", 42.0, E + Vector((0, -5.9, 1.1)))
plane("E_fondo", 14, 8, mat_flat("E_fondoM", hexc("0a161d"), 1.0, fade=1.0), E + Vector((0, 1.5, 1.2)), (radians(90), 0, 0))
logo = empty("E_logo", E + Vector((0, 0, 1.45)))
la, mla = text3d("E_auto", "Auto", (0, 0, 0), 0.95, C_BLANCO, FONT_X, align="RIGHT", extrude=0.0, fade_val=1.0)
lb, mlb = text3d("E_lid", "LID", (0, 0, 0), 0.95, C_ECO, FONT_X, align="LEFT", extrude=0.0, fade_val=1.0, strength=1.3)
for o in (la, lb):
    o.parent = logo
la.location = (0.02, 0, 0)
lb.location = (0.04, 0, 0)
ob_kf(logo, "scale", 0.0, (0.6, 0.6, 0.6), "CONSTANT")
ob_kf(logo, "scale", 36.2, (0.6, 0.6, 0.6), "BACK", "EASE_OUT")
ob_kf(logo, "scale", 37.0, (1, 1, 1), "LINEAR")
ob_kf(logo, "scale", 42.0, (1.04, 1.04, 1.04))
for m in (mla, mlb):
    fade(m, 0.0, 0.0)
    fade(m, 36.2, 0.0)
    fade(m, 36.6, 1.0)
tag, mtag = text3d("E_tag", "Higiene y autonomía, sin tocar nada.", E + Vector((0, 0, 0.72)), 0.2, hexc("d5e1e6"), FONT_R)
fade_in_out(mtag, 37.0)
ob_kf(tag, "location", 37.0, E + Vector((0, 0, 0.62)), "EXPO", "EASE_OUT")
ob_kf(tag, "location", 37.6, E + Vector((0, 0, 0.72)))
esc, mesc = text3d("E_esc", "Proyecto de 7° 1° · EEST N° 3 de San Antonio de Padua", E + Vector((0, 0, 0.3)), 0.1, hexc("8aa0ab"), FONT_R)
fade_in_out(mesc, 37.6)
mail, mmail = text3d("E_mail", "contacto.autolid@gmail.com", E + Vector((0, 0, 0.12)), 0.1, C_ECO, FONT_B)
fade_in_out(mmail, 37.9)
# anillos de "ultrasonido" detrás del logo
for k in range(3):
    bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.006, major_segments=96, minor_segments=6)
    rg = bpy.context.active_object
    rg.name = f"E_anillo{k}"
    mr = mat_flat(f"E_anM{k}", C_ECO, 1.5, fade=0.0)
    rg.data.materials.append(mr)
    rg.location = E + Vector((0, 0.3, 1.4))
    rg.rotation_euler = (radians(90), 0, 0)
    t0 = 36.4 + k * 0.5
    ob_kf(rg, "scale", 0.0, (0.3, 0.3, 0.3), "CONSTANT")
    ob_kf(rg, "scale", t0, (0.3, 0.3, 0.3), "QUAD", "EASE_OUT")
    ob_kf(rg, "scale", t0 + 2.2, (3.2, 3.2, 3.2))
    fade(mr, 0.0, 0.0)
    fade(mr, t0, 0.0)
    fade(mr, t0 + 0.15, 0.5)
    fade(mr, t0 + 2.2, 0.0)
area_light("E_luz", E + Vector((0, -4, 4)), 400, 6, target=logo)

# ───────────────────────── Cortes y fundidos ─────────────────────────
for cam, t in ((camA, 0.0), (camB, CUTS[0]), (camC, CUTS[1]), (camD, CUTS[2]), (camE, CUTS[3])):
    mk = sc.timeline_markers.new(cam.name, frame=F(t) if t > 0 else 1)
    mk.camera = cam
sc.camera = camA
fade(FADER, 0.0, 1.0)
fade(FADER, 0.6, 0.0)
for c in CUTS:
    fade(FADER, c - 0.32, 0.0)
    fade(FADER, c - 0.02, 1.0, "CONSTANT")
    fade(FADER, c, 1.0)
    fade(FADER, c + 0.35, 0.0)
fade(FADER, DUR - 0.9, 0.0)
fade(FADER, DUR - 0.1, 1.0)

# ───────────────────────── Salida ─────────────────────────
os.makedirs(OUTDIR, exist_ok=True)
sc.render.image_settings.file_format = "JPEG"
sc.render.image_settings.quality = 93
sc.render.filepath = os.path.join(OUTDIR, "f_")
if BLEND:
    bpy.ops.wm.save_as_mainfile(filepath=BLEND)

TEST_T = [float(x) for x in os.environ.get("TEST_T", "2.0,4.0,7.8,11.2,14.9,20.6,24.2,26.0,29.6,31.9,34.8,38.6").split(",")]
if TEST:
    sc.render.resolution_percentage = int(os.environ.get("TEST_PCT", "50"))
    for t in TEST_T:
        sc.frame_set(F(t))
        sc.render.filepath = os.path.join(OUTDIR, f"test_{t:05.1f}.jpg")
        bpy.ops.render.render(write_still=True)
    print("TEST LISTO")
else:
    bpy.ops.render.render(animation=True)
    print("RENDER LISTO")
