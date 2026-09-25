# Renders V7 and V8 from identical orthographic cameras (Workbench, studio light, cavity, outline) and
# writes V8 views + side-by-side V7 | V8 comparison images.   Run:  blender -b -P render_v8.py
import bpy, bmesh, math, os, mathutils
from mathutils import Matrix
HERE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else None
ROOT = os.environ.get("MOUNT_REPO") or (os.path.abspath(os.path.join(HERE, "..", "..")) if HERE
        else "/Users/joneswang/Downloads/code/acebott-qd001-phone-camera-mount")
OUT = os.path.join(ROOT, "docs/renders/v8"); os.makedirs(os.path.join(OUT, "compare"), exist_ok=True)
MODELS = {"V7": ("models/current/ACEBOTT_QD001_PhoneMount_V7_90deg_OnePiece.stl", -48.0),
          "V8": ("models/current/ACEBOTT_QD001_PhoneMount_V8_90deg_OnePiece.stl", -23.0)}   # (stl, plate phone face Y)

if bpy.app.background: bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene; sc.render.engine = 'BLENDER_WORKBENCH'
sh = sc.display.shading; sh.light = 'STUDIO'; sh.color_type = 'OBJECT'; sh.show_cavity = True; sh.cavity_type = 'BOTH'
sh.show_shadows = False; sh.show_object_outline = True
sc.render.resolution_x = 1300; sc.render.resolution_y = 1000; sc.display.render_aa = '8'
sc.render.image_settings.file_format = 'PNG'
if sc.world is None: sc.world = bpy.data.worlds.new("W")
sc.world.color = (1, 1, 1)
cam_d = bpy.data.cameras.new("C"); cam_d.type = 'ORTHO'; cam_d.clip_start = 1; cam_d.clip_end = 5000
cam = bpy.data.objects.new("C", cam_d); sc.collection.objects.link(cam); sc.camera = cam
O = bpy.data.objects; V = mathutils.Vector

def dummy(name, dims, M, col):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0); me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); sc.collection.objects.link(o)
    o.matrix_world = M @ Matrix.Diagonal((dims[0], dims[1], dims[2], 1)); o.color = col; return o
parts = {}
for tag, (path, yp0) in MODELS.items():
    before = set(bpy.data.objects); bpy.ops.wm.stl_import(filepath=os.path.join(ROOT, path))
    o = [x for x in bpy.data.objects if x not in before][0]; o.name = tag; o.color = (0.8, 0.72, 0.4, 1)
    ph = dummy(f"Phone_{tag}", (79, 12, 160), Matrix.Translation((0, yp0 - 6, 54 + 80)), (0.2, 0.4, 0.9, 1))   # back on the plate face
    parts[tag] = (o, ph)
bat = dummy("Bat", (72, 44, 22), Matrix.Translation((0, -49, 11)), (0.12, 0.12, 0.12, 1))                     # Y -71 .. -27

def show(names):
    for o in O: o.hide_render = o.name not in names
def shoot(tag, view, names, d, scale=230, ctr=V((0, -22, 70)), clip=5000):
    show(names); d = V(d).normalized(); cam.location = ctr + d * 1500
    cam.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler(); cam_d.ortho_scale = scale; cam_d.clip_end = clip
    sc.render.filepath = os.path.join(OUT, "compare", f"{view}_{tag}.png"); bpy.ops.render.render(write_still=True)

VIEWS = [  # (view, with_battery, with_phone, direction, scale, centre, clip)   clip=1500 cuts the far half away (section at X=0)
    ("0_front_into_chamber", False, False, (0, 1, 0.35), 230, V((0, -22, 60)), 5000),
    ("1_side_left", True, True, (-1, 0, 0), 230, V((0, -22, 70)), 1500),
    ("1b_side_left_nophone", True, False, (-1, 0, 0), 230, V((0, -22, 70)), 1500),
    ("1c_side_right_full", True, True, (1, 0, 0), 230, V((0, -22, 70)), 5000),
    ("2_front", False, False, (0, 1, 0), 230, V((0, -22, 70)), 5000),
    ("3_rear", False, False, (0, -1, 0), 230, V((0, -22, 70)), 5000),
    ("3b_rear_phone", True, True, (0, -1, 0.02), 300, V((0, -22, 105)), 5000),
    ("4_top34_rear", True, True, (-0.8, -1.2, 0.9), 300, V((0, -22, 100)), 5000),
    ("4b_top34_front", True, False, (-1, 1.2, 0.8), 230, V((0, -22, 70)), 5000),
    ("5_rear_low", False, False, (0.5, -1, 0.15), 230, V((0, -22, 70)), 5000),
    ("6_tray_closeup", True, False, (-0.9, -1, 0.9), 80, None, 5000),          # centre follows the slot
    ("7_top", False, False, (0, -0.001, 1), 230, V((0, -22, 70)), 5000),
]
for view, wb, wp, d, scale, ctr, clip in VIEWS:
    for tag, (o, ph) in parts.items():
        names = [tag] + (["Bat"] if wb else []) + ([ph.name] if wp else [])
        c = ctr if ctr is not None else V((-30, MODELS[tag][1] + 9, 58))
        shoot(tag, view, names, d, scale, c, clip)
print("renders written to", OUT)
