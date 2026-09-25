# Side-by-side verification of the exported V7 and V8 STLs under identical checks:
# volume / bbox / centre of mass (part alone and part + 200 g phone), keep-out & clearance intersections,
# voxel island check, bridging reach and bed contact.   Run:  blender -b -P verify_v7_v8.py
import bpy, bmesh, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else None
ROOT = os.environ.get("MOUNT_REPO") or (os.path.abspath(os.path.join(HERE, "..", "..")) if HERE
        else "/Users/joneswang/Downloads/code/acebott-qd001-phone-camera-mount")
exec(open(os.path.join(ROOT, "reference/scripts/lib_v5.py")).read())
COLL = "VERIFY"
FILES = {"V7": ("models/current/ACEBOTT_QD001_PhoneMount_V7_90deg_OnePiece.stl", -48.0, -76.5),
         "V8": ("models/current/ACEBOTT_QD001_PhoneMount_V8_90deg_OnePiece.stl", -23.0, -72.5)}   # (stl, plate phone face, fin front)
PLA = 1.24e-3          # g/mm3
PHONE_G, PHONE_Z = 200.0, 54 + 80        # 160 mm phone standing on the z54 floor, COM 80 mm up, 6 mm behind the plate face

if bpy.app.background: bpy.ops.wm.read_factory_settings(use_empty=True)
def load(tag, path):
    before = set(bpy.data.objects); bpy.ops.wm.stl_import(filepath=os.path.join(ROOT, path))
    o = [x for x in bpy.data.objects if x not in before][0]
    for c in list(o.users_collection): c.objects.unlink(o)
    coll().objects.link(o); o.name = tag; o.data.name = tag; return o
def com(o):
    bm = bmesh.new(); bm.from_mesh(o.data); bmesh.ops.triangulate(bm, faces=bm.faces)
    vol = 0.0; c = Vector((0, 0, 0))
    for f in bm.faces:
        a, b, d = [v.co for v in f.verts]; v = a.dot(b.cross(d)) / 6.0; vol += v; c += (a + b + d) / 4.0 * v
    bm.free(); return vol, c / vol
def inter(body, name, x0, x1, y0, y1, z0, z1):
    tmp = box(name, x0, x1, y0, y1, z0, z1)
    m = tmp.modifiers.new("i", 'BOOLEAN'); m.operation = 'INTERSECT'; m.object = body; m.solver = 'MANIFOLD'
    with bpy.context.temp_override(object=tmp, active_object=tmp, selected_objects=[tmp]):
        bpy.ops.object.modifier_apply(modifier=m.name)
    bm = bmesh.new(); bm.from_mesh(tmp.data); v = bm.calc_volume(); bm.free()
    me = tmp.data; bpy.data.objects.remove(tmp, do_unlink=True); bpy.data.meshes.remove(me); return v

R = {}
for tag, (path, yplate, yfin) in FILES.items():
    o = load(tag, path); r = {}
    bm = bmesh.new(); bm.from_mesh(o.data)
    r["nonmanifold"] = sum(1 for e in bm.edges if not e.is_manifold); r["shells"] = len(shells(bm))
    bb = [v.co for v in bm.verts]
    r["bbox"] = tuple(round(min(v[i] for v in bb), 1) for i in range(3)) + tuple(round(max(v[i] for v in bb), 1) for i in range(3)); bm.free()
    vol, c = com(o); r["volume_cm3"] = round(vol / 1000, 1); r["mass_g"] = round(vol * PLA, 0); r["com"] = tuple(round(x, 1) for x in c)
    mp = vol * PLA; ph = Vector((0, yplate - 6.0, PHONE_Z))
    r["com_with_phone"] = tuple(round(x, 1) for x in (c * mp + ph * PHONE_G) / (mp + PHONE_G)); r["phone_com_y"] = yplate - 6.0
    ko = {}
    ko["wire_chamber"] = inter(o, "k", -36.25, 36.25, -17.55, 60, 40, 300)
    ko["above_mast"] = inter(o, "k", -60, 60, -17.55, 60, 65.05, 300)
    ko["wire_margin_2mm"] = inter(o, "k", -60, 60, -19.55, 60, 65.05, 300)
    ko["front_module"] = inter(o, "k", -60, 60, 46.05, 80, -1, 300)
    ko["battery_bay"] = inter(o, "k", -36, 36, yfin + 0.05, -28.05, -0.5, 31)
    ko["mast_arch"] = inter(o, "k", -14.9, 14.9, -23.5, -17.0, 33, 53.9)
    ko["dc_plug"] = inter(o, "k", -45, -36.35, -21.95, -2.05, -0.5, 24.95)
    ko["usbc"] = inter(o, "k", -45, -36.35, 12, 40, 12, 22)
    ko["screw_R"] = inter(o, "k", 36.35, 45, 8, 21, -0.5, 6.5); ko["screw_L"] = inter(o, "k", -45, -36.35, 8, 21, -0.5, 6.5)
    ko["phone_camera_bar_z>150"] = inter(o, "k", -60, 60, -120, 80, 150.05, 400)
    r["keepout_mm3"] = {k: round(v, 1) for k, v in ko.items()}
    # slot fit sanity: the 81.5 x 18.5 pocket behind the plate face must be empty from the floor up
    r["slot_pocket_mm3"] = round(inter(o, "k", -40.7, 40.7, yplate - 18.45, yplate - 0.05, 54.05, 149.95), 1)
    print(f"\n===== {tag} =====")
    islands = printcheck(tag, res=1.0, eps=0.013)
    r["islands"] = len(islands); R[tag] = r
    o.hide_render = True

print("\n================ V7 vs V8 ================")
keys = ["volume_cm3", "mass_g", "bbox", "com", "com_with_phone", "phone_com_y", "nonmanifold", "shells", "islands", "slot_pocket_mm3"]
for k in keys: print(f"{k:18s} V7 = {R['V7'][k]!s:42s} V8 = {R['V8'][k]!s}")
for k in R["V7"]["keepout_mm3"]: print(f"keepout {k:22s} V7 = {R['V7']['keepout_mm3'][k]:8.1f}   V8 = {R['V8']['keepout_mm3'][k]:8.1f}")
