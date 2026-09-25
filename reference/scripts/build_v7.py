# V7: fixed 90deg tower moved BEHIND the mast (over the battery bay) to keep the V4 wire chamber free.
import bpy, bmesh, math
exec(open("/private/tmp/claude-501/-Users-joneswang-Downloads-cart/123340a2-892d-4c68-b675-cc734aed0901/scratchpad/lib_v5.py").read())
COLL = "FABLE_V7"
STL = "/Users/joneswang/Downloads/code/acebott-qd001-phone-camera-mount/models/legacy/FableV4_OnePiece.stl"
XI, XO = 36.3, 39.5
PW, RW, LIPX = 40.75, 44.25, 36.25          # V4-verified slot 81.5 / lip inner edge
YP0, YP1 = -48.0, -44.6                     # plate: phone-contact face (rear side) / front face; 3.4 thick
SLOT = 18.5
YLIP, YRAIL, YCH = YP0-SLOT, YP0-SLOT-2.5, YP0-(SLOT-4.5)     # -66.5 / -69.0 / -62.0
YFLOOR = YP0 - 14.0                          # -62.0 bottom groove rear face
ZB, ZT = 54.0, 150.0
YTRAY0 = YP1 + 0.1                           # tray runs through the plate

def wipe():
    c = bpy.data.collections.get(COLL)
    if c:
        for o in list(c.objects):
            me = o.data; bpy.data.objects.remove(o, do_unlink=True)
            if me and me.users == 0: bpy.data.meshes.remove(me)
wipe()
sc = bpy.context.scene; sc.unit_settings.scale_length = 0.001; sc.unit_settings.length_unit = 'MILLIMETERS'
before = set(bpy.data.objects)
bpy.ops.wm.stl_import(filepath=STL)
body = [o for o in bpy.data.objects if o not in before][0]
for c in list(body.users_collection): c.objects.unlink(body)
coll().objects.link(body); body.name = "V7_Body"; body.data.name = "V7_Body"

# ---- cuts on V4
K = [box("c_top", -60, 60, -120, 70, 65, 300),                       # 35deg deck and everything above z65 (mast keeps its V4 height)
     box("c_rear", -60, 60, -120, -91.9, 2.5, 300),                  # corbel / cradle stub behind the tie band
     box("c_ribs", -XI, XI, -77.0, -19.9, 22, 70),                   # deck ribs over the battery bay
     box("c_comb", -XI, XI, -93, -76.4, 30, 70)]                     # rear fin comb -> 30 mm
tail = [(YRAIL, 60), (YRAIL, 200), (-100, 200), (-100, 29)]          # 45deg tail behind the lips
front = [(14, 65.5), (39, 40.5), (46, 40.5), (46, 200), (14, 200)]   # 45deg drop to z40 (15 mm above USB-C window), walls end at Y46
for xa, xb in ((30, 50), (-50, -30)):
    K.append(prism("c_tail", tail, fX, xa, xb)); K.append(prism("c_front", front, fX, xa, xb))
K.append(box("c_frontend", -50, 50, 46, 60, -1, 300))
cut(body, K); check(body)

# ---- unions
U = [box("fillR", 36.4, 39.4, -69.5, -31.5, 30.5, 64.5),              # V4 right wall window: fill under tray + bulkhead
     box("fillL", -39.4, -36.4, -55.5, -33.5, 42.5, 64.5),               # V4 left wall window: fill under the bulkhead root
     box("pad", -36.2, 36.2, -91.6, -76.6, 0.0, 2.0)]
# arched bulkhead = tower plate: 45deg haunches from the wall inner faces (z33) to a 30 mm bridge at z54.2, then the plate to z150
arch = [(-36.2, 37), (-15, 58.2), (15, 58.2), (36.2, 37), (36.2, 62), (-36.2, 62)]   # springs above the left gable (z35.5)
U += [prism("arch", arch, fY, YP0, YP1), box("plate", -RW, RW, YP0, YP1, 60.0, ZT)]
gus = [(YP1-1.0, 64), (-26.0, 64), (YP1-1.0, 118)]                   # front gussets on the bay walls (behind the mast, ahead of the plate)
U += [prism("gusR", gus, fX, 36.2, 39.6), prism("gusL", gus, fX, -39.6, -36.2)]
rg = [(YRAIL+0.05, 40), (YRAIL+0.05, 105), (-88, 40)]                # rear gussets: wall raised behind the lips, glued to the lip rear face
U += [prism("rgR", rg, fX, 36.2, 39.6), prism("rgL", rg, fX, -39.6, -36.2)]
prof = [(36.2, 41), (26, 51.2), (26, 60), (RW, 60), (RW, 49.05), (39.6, 44.4), (39.6, 41)]
U += [prism("trayR", prof, fY, YRAIL, YTRAY0), prism("trayL", mir(prof), fY, YRAIL, YTRAY0)]
railxy = [(PW, YP0+0.05), (RW, YP0+0.05), (RW, YRAIL), (LIPX, YRAIL), (LIPX, YLIP), (PW, YCH)]
U += [prism("railR", railxy, fZ, ZB, ZT), prism("railL", mir(railxy), fZ, ZB, ZT)]
union(body, U); check(body)

# ---- final cuts: floor groove, lead-in chamfer, plate window
K = []
for xa, xb in ((25.5, PW), (-PW, -25.5)):
    K.append(box("k_floor", xa, xb, YFLOOR, YP0+0.05, ZB, 70))
for xa, xb in ((25.5, LIPX-0.05), (-LIPX+0.05, -25.5)):
    K.append(prism("k_lead", [(YFLOOR, 56), (YFLOOR-4.0, 60), (YFLOOR-4.0, 70), (YFLOOR, 70)], fX, xa, xb))
K.append(prism("k_win", [(-22, 66), (22, 66), (22, 116), (0, 138), (-22, 116)], fY, YP0-3, YP1+3))
cut(body, K)
cleanup(body); ok = check(body); body.color = (0.8, 0.72, 0.4, 1)

# ---- keep-out proof: V4 wire chamber (between the walls, in front of the mast, above the board) and the front-module zone
def keepout(name, x0, x1, y0, y1, z0, z1):
    tmp = box(name, x0, x1, y0, y1, z0, z1)
    m = tmp.modifiers.new("i", 'BOOLEAN'); m.operation = 'INTERSECT'; m.object = body; m.solver = 'MANIFOLD'
    with bpy.context.temp_override(object=tmp, active_object=tmp, selected_objects=[tmp]):
        bpy.ops.object.modifier_apply(modifier=m.name)
    bm = bmesh.new(); bm.from_mesh(tmp.data); v = bm.calc_volume(); bm.free()
    me = tmp.data; bpy.data.objects.remove(tmp, do_unlink=True); bpy.data.meshes.remove(me)
    print(f"keep-out {name}: intersect volume = {v:.1f} mm3")
keepout("KO_wire_chamber", -36.25, 36.25, -17.55, 60, 40, 300)      # inside the walls, from the mast front face forward, above z40
keepout("KO_above_mast", -60, 60, -17.55, 60, 65.05, 300)           # nothing at all above the mast height in front of it
keepout("KO_front_module", -60, 60, 46.05, 80, -1, 300)             # nothing beyond Y46
