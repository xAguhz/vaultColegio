"""Renders del modelo de AutoLID: armado y con el despiece al 100 %.

    blender -b AutoLID/3D/autolid.blend --python herramientas/autolid_3d_render.py

Guarda Adjuntos/AutoLID/autolid_3d_armado.png y autolid_3d_despiece.png.
"""
import bpy
import math
import os
from mathutils import Vector

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(VAULT, 'Adjuntos', 'AutoLID')
os.makedirs(OUT, exist_ok=True)
sc = bpy.context.scene
for eng in ('BLENDER_EEVEE', 'BLENDER_EEVEE_NEXT'):
    try:
        sc.render.engine = eng
        break
    except TypeError:
        pass
sc.eevee.taa_render_samples = 48
sc.render.resolution_x, sc.render.resolution_y = 1600, 1000
sc.view_settings.view_transform = 'AgX'
sc.render.film_transparent = False

w = bpy.data.worlds.new('mundo')
sc.world = w
w.use_nodes = True
w.node_tree.nodes['Background'].inputs[0].default_value = (0.62, 0.68, 0.72, 1)
w.node_tree.nodes['Background'].inputs[1].default_value = 0.45

def light(name, loc, energy, size):
    ld = bpy.data.lights.new(name, 'AREA')
    ld.energy, ld.size = energy, size
    ob = bpy.data.objects.new(name, ld)
    sc.collection.objects.link(ob)
    ob.location = loc
    ob.rotation_euler = (Vector((0.1, -0.2, 0.45)) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()

light('clave', (1.2, -1.4, 1.8), 260, 1.2)
light('relleno', (-1.3, -0.8, 1.0), 90, 1.5)
light('contra', (0.2, 1.4, 1.4), 120, 1.0)

piso = bpy.data.meshes.new('piso')
piso.from_pydata([(-3, -3, 0), (3, -3, 0), (3, 3, 0), (-3, 3, 0)], [], [(0, 1, 2, 3)])
po = bpy.data.objects.new('piso', piso)
sc.collection.objects.link(po)
pm = bpy.data.materials.new('pisoM')
pm.use_nodes = True
pm.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.42, 0.46, 0.48, 1)
piso.materials.append(pm)

cd = bpy.data.cameras.new('cam')
cd.lens = 50
cam = bpy.data.objects.new('cam', cd)
sc.collection.objects.link(cam)
sc.camera = cam

def shoot(name, explode, tgt, loc):
    for ob in sc.objects:
        if 'explode' in ob:
            if 'base' not in ob:
                ob['base'] = list(ob.location)
            ob.location = Vector(ob['base']) + Vector(ob['explode']) * explode
    cam.location = loc
    cam.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = os.path.join(OUT, name)
    bpy.ops.render.render(write_still=True)

shoot('autolid_3d_armado.png', 0.0, (0.12, -0.12, 0.42), (1.05, -1.25, 0.95))
shoot('autolid_3d_despiece.png', 1.0, (0.2, -0.12, 0.55), (1.35, -1.55, 1.25))
shoot('autolid_3d_gabinete.png', 1.0, (0.34, 0.0, 0.62), (0.75, -0.62, 0.86))
print('RENDERS LISTOS')
