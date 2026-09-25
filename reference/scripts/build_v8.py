# V8: the V7 tower moved 25 mm toward the car centre. The tower plate now merges with the V4 mast
#     (plate front face 2.0 mm behind the mast front face = 2 mm margin to the wire keep-out), the rear
#     foot (fins / tie band / pad) is pulled 4 mm toward the battery box, and the rail / plate outer faces
#     are slimmed 1 mm (rail 3.5 -> 2.5 mm). The phone-slot fit (81.5 x 18.5, lips, chamfer, groove, pads)
#     is unchanged from V7. Front gussets are gone (no room behind the mast); the mast + walls are the root.
#
# Run inside Blender >= 4.5 (MANIFOLD boolean solver):  blender -b -P build_v8.py
# or paste into the text editor. Set MOUNT_REPO if the repo is not two levels above this file.
import bpy, bmesh, math, os
HERE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else None
ROOT = os.environ.get("MOUNT_REPO") or (os.path.abspath(os.path.join(HERE, "..", "..")) if HERE
        else "/Users/joneswang/Downloads/code/acebott-qd001-phone-camera-mount")
exec(open(os.path.join(ROOT, "reference/scripts/lib_v5.py")).read())
COLL = "FABLE_V8"
STL = os.path.join(ROOT, "models/legacy/FableV4_OnePiece.stl")
OUT_STL = os.path.join(ROOT, "models/current/ACEBOTT_QD001_PhoneMount_V8_90deg_OnePiece.stl")
OUT_BLEND = os.path.join(ROOT, "models/current/spoiler_v10_fable_v8.blend")

# ---- V8 parameters (everything else is V7)
SHIFT = 25.0                                 # tower forward: V7 plate phone face -48 -> -23
TAIL_SHIFT = 4.0                             # rear foot toward the battery box: fin fronts -76.5 -> -72.5, part ends at -87.9
MAST_FRONT = -17.6                           # V4 mast front face (wire keep-out starts at -17.55)
WIRE_MARGIN = 2.0                            # user: leave ~2 mm behind the mast plane for the real bundle + print tolerance
XI, XO = 36.3, 39.5
PW, LIPX = 40.75, 36.25                      # V7-verified slot 81.5 / lip inner edge  (UNCHANGED)
RW = 43.25                                   # rail outer face 44.25 -> 43.25 (rail 3.5 -> 2.5 mm, plate 88.5 -> 86.5 wide)
YP0, YP1 = -48.0 + SHIFT, -44.6 + SHIFT      # plate: phone-contact face -23 / front face -19.6 ; 3.4 thick
SLOT = 18.5                                  # UNCHANGED
YLIP, YRAIL, YCH = YP0-SLOT, YP0-SLOT-2.5, YP0-(SLOT-4.5)     # -41.5 / -44.0 / -37.0
YFLOOR = YP0 - 14.0                          # -37.0 bottom groove rear face (14 mm groove, unchanged)
ZB, ZT = 54.0, 150.0
YTRAY0 = YP1 + 0.1                           # tray runs through the plate into the mast
assert YP1 <= MAST_FRONT - WIRE_MARGIN + 1e-9, "plate front face must stay >= 2 mm behind the mast front face"

def wipe():
    c = bpy.data.collections.get(COLL)
    if c:
        for o in list(c.objects):
            me = o.data; bpy.data.objects.remove(o, do_unlink=True)
            if me and me.users == 0: bpy.data.meshes.remove(me)
if bpy.app.background:                       # standalone run: start from an empty file
    bpy.ops.wm.read_factory_settings(use_empty=True)
wipe()
sc = bpy.context.scene; sc.unit_settings.scale_length = 0.001; sc.unit_settings.length_unit = 'MILLIMETERS'
before = set(bpy.data.objects)
bpy.ops.wm.stl_import(filepath=STL)
body = [o for o in bpy.data.objects if o not in before][0]
for c in list(body.users_collection): c.objects.unlink(body)
coll().objects.link(body); body.name = "V8_Body"; body.data.name = "V8_Body"

# ---- cuts on V4 (identical to V7 except the tail, which is cut after the rear-foot shift)
K = [box("c_top", -60, 60, -120, 70, 65, 300),                       # 35deg deck and everything above z65 (mast keeps its V4 height)
     box("c_rear", -60, 60, -120, -91.9, 2.5, 300),                  # corbel / cradle stub behind the tie band
     box("c_ribs", -XI, XI, -77.0, -19.9, 22, 70),                   # deck ribs over the battery bay
     box("c_comb", -XI, XI, -93, -76.4, 30, 70)]                     # rear fin comb -> 30 mm
front = [(14, 65.5), (39, 40.5), (46, 40.5), (46, 200), (14, 200)]   # 45deg drop to z40 (15 mm above USB-C window), walls end at Y46
for xa, xb in ((30, 50), (-50, -30)): K.append(prism("c_front", front, fX, xa, xb))
K.append(box("c_frontend", -50, 50, 46, 60, -1, 300))
cut(body, K); check(body)

# ---- rear-foot shift: everything behind the fin fronts (walls, fins, tie band, centre wedge) moves +TAIL_SHIFT
YCUT = -76.45                                                        # 0.05 in front of the V4 fin fronts (-76.5)
rear = body.copy(); rear.data = body.data.copy(); rear.name = "V8_rear"; coll().objects.link(rear)
boolean(rear, box("i_rear", -50, 50, -100, YCUT, -1, 300), 'INTERSECT')
cut(body, [box("c_rearfoot", -50, 50, -100, YCUT, -1, 300)])
rear.data.transform(Matrix.Translation((0, TAIL_SHIFT, 0)))
union(body, [rear]); check(body)
tail = [(YRAIL, 60), (YRAIL, 200), (-100, 200), (-100, 35), (YRAIL-25, 35)]   # 45deg from the lip rear face down to z35, flat behind
cut(body, [prism("c_tail", tail, fX, xa, xb) for xa, xb in ((30, 50), (-50, -30))]); check(body)

# ---- unions
U = [box("fillR", 36.4, 39.4, -69.5, -31.5, 30.5, 64.5),              # V4 right wall window: fill (tray + rear gusset sit on it)
     box("fillL", -39.4, -36.4, -55.5, -33.5, 42.5, 64.5),               # V4 left wall window: fill
     box("pad", -36.2, 36.2, -91.6+TAIL_SHIFT, -76.6+TAIL_SHIFT, 0.0, 2.0)]   # 2 mm grounded pad under the fins
# arched bulkhead = tower plate, now 0.3 mm into the mast's rear face: 45deg haunches from the wall inner faces (z37, above the
# left gable) to a 30 mm bridge at z58.2 that is backed by the solid top of the mast (z54..65), then the plate to z150
arch = [(-36.2, 37), (-15, 58.2), (15, 58.2), (36.2, 37), (36.2, 62), (-36.2, 62)]
U += [prism("arch", arch, fY, YP0, YP1), box("plate", -RW, RW, YP0, YP1, 60.0, ZT)]
# no front gussets: in front of the plate is the 2 mm wire margin and then the keep-out. Root = mast + arch + both walls.
rg = [(YRAIL+0.05, 40), (YRAIL+0.05, 105), (YRAIL-19, 40)]           # rear gussets: wall raised behind the lips, glued to the lip rear face
U += [prism("rgR", rg, fX, 36.2, 39.6), prism("rgL", rg, fX, -39.6, -36.2)]
prof = [(36.2, 41), (26, 51.2), (26, 60), (RW, 60), (RW, 44.4 + RW - 39.6), (39.6, 44.4), (39.6, 41)]   # 45deg haunch / flare as V7
U += [prism("trayR", prof, fY, YRAIL, YTRAY0), prism("trayL", mir(prof), fY, YRAIL, YTRAY0)]
railxy = [(PW, YP0+0.05), (RW, YP0+0.05), (RW, YRAIL), (LIPX, YRAIL), (LIPX, YLIP), (PW, YCH)]
U += [prism("railR", railxy, fZ, ZB, ZT), prism("railL", mir(railxy), fZ, ZB, ZT)]
union(body, U); check(body)

# ---- final cuts: floor groove, lead-in chamfer, plate window (all V7)
K = []
for xa, xb in ((25.5, PW), (-PW, -25.5)):
    K.append(box("k_floor", xa, xb, YFLOOR, YP0+0.05, ZB, 70))
for xa, xb in ((25.5, LIPX-0.05), (-LIPX+0.05, -25.5)):
    K.append(prism("k_lead", [(YFLOOR, 56), (YFLOOR-4.0, 60), (YFLOOR-4.0, 70), (YFLOOR, 70)], fX, xa, xb))
K.append(prism("k_win", [(-22, 66), (22, 66), (22, 116), (0, 138), (-22, 116)], fY, YP0-3, YP1+3))
cut(body, K)
cleanup(body); ok = check(body); body.color = (0.8, 0.72, 0.4, 1)

# ---- keep-out / clearance proof by boolean intersection (all must be 0)
def keepout(name, x0, x1, y0, y1, z0, z1):
    tmp = box(name, x0, x1, y0, y1, z0, z1)
    m = tmp.modifiers.new("i", 'BOOLEAN'); m.operation = 'INTERSECT'; m.object = body; m.solver = 'MANIFOLD'
    with bpy.context.temp_override(object=tmp, active_object=tmp, selected_objects=[tmp]):
        bpy.ops.object.modifier_apply(modifier=m.name)
    bm = bmesh.new(); bm.from_mesh(tmp.data); v = bm.calc_volume(); bm.free()
    me = tmp.data; bpy.data.objects.remove(tmp, do_unlink=True); bpy.data.meshes.remove(me)
    print(f"keep-out {name}: intersect volume = {v:.1f} mm3"); return v
KO = {}
KO["wire_chamber"]   = keepout("KO_wire_chamber", -36.25, 36.25, -17.55, 60, 40, 300)          # inside the walls, mast front face forward, above z40
KO["above_mast"]     = keepout("KO_above_mast", -60, 60, -17.55, 60, 65.05, 300)               # nothing above the mast height in front of it
KO["wire_margin"]    = keepout("KO_wire_margin", -60, 60, MAST_FRONT-WIRE_MARGIN+0.05, 60, 65.05, 300)   # ...nor within 2 mm behind its front face
KO["front_module"]   = keepout("KO_front_module", -60, 60, 46.05, 80, -1, 300)                 # nothing beyond Y46
KO["battery_bay"]    = keepout("KO_battery_bay", -36, 36, YCUT+TAIL_SHIFT+0.05, -28.05, -0.5, 31)   # box slides out sideways below z31
KO["mast_arch"]      = keepout("KO_mast_arch", -14.9, 14.9, -23.5, -17.0, 33, 53.9)            # wire opening through the mast stays open
KO["dc_plug"]        = keepout("KO_dc_plug", -45, -36.35, -21.95, -2.05, -0.5, 24.95)          # left wall window for the DC plug
KO["usbc"]           = keepout("KO_usbc", -45, -36.35, 12, 40, 12, 22)                         # left wall USB-C window
KO["screw_R"]        = keepout("KO_screw_R", 36.35, 45, 8, 21, -0.5, 6.5)                      # screw-head notches
KO["screw_L"]        = keepout("KO_screw_L", -45, -36.35, 8, 21, -0.5, 6.5)
bad = {k: v for k, v in KO.items() if v > 0.01}
print("KEEP-OUT RESULT:", "ALL CLEAR" if not bad else f"VIOLATIONS {bad}")

islands = printcheck("V8_Body", res=1.0, eps=0.013)   # eps: keep voxel centres off the z22.5 / z35.5 / z7.5 faces (phantom islands)
if ok and not bad and not islands:
    export_clean("V8_Body", OUT_STL)
    if bpy.app.background:
        bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND, compress=True)
        print("blend written:", OUT_BLEND)
else:
    print("NOT exported: manifold_ok =", ok, "keepout_bad =", bad, "islands =", islands)
