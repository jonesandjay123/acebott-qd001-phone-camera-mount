# V6: fixed 90deg phone tower, one piece, built from FableV4_OnePiece.stl (plate top = z0)
import bpy, bmesh, math
exec(open("/private/tmp/claude-501/-Users-joneswang-Downloads-cart/123340a2-892d-4c68-b675-cc734aed0901/scratchpad/lib_v5.py").read())
COLL = "FABLE_V6"
STL = "/Users/joneswang/Downloads/cart/FableV4_OnePiece.stl"
XI, XO = 36.3, 39.5
PW, RW, LIPX = 40.75, 44.25, 36.25          # V4 slot 81.5, rail outer, lip inner edge (3.25 mm over bezel)
YP0, YP1 = -20.9, -17.5                     # plate: phone-contact face / front face (3.4 thick, rooted in the mast)
SLOT = 18.5                                 # user: 20 -> 18.5
YLIP = YP0 - SLOT                            # -39.4 lip underside
YRAIL = YLIP - 2.5                           # -41.9 lip outer face (V4 lip 2.5 thick)
YCH = YP0 - (SLOT - 4.5)                     # -34.9 chamfer start (V4: 45deg from PW to lip)
ZB, ZT = 54.0, 150.0                         # phone bottom (floor) / tower top
YFLOOR = YP0 - 14.0                          # -34.9 bottom groove rear face (phone 12 + 2)
YTRAY0 = -17.4

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
coll().objects.link(body); body.name = "V6_Body"; body.data.name = "V6_Body"

# ---- cuts on V4: upper structure, rear stub, deck ribs, rear comb (to z30), rear & front wall trims
K = [box("c_top", -60, 60, -120, 70, 65, 300),
     box("c_rear", -60, 60, -120, -91.9, 2.5, 300),
     box("c_ribs", -XI, XI, -77.0, -19.9, 22, 70),
     box("c_comb", -XI, XI, -93, -76.4, 30, 70)]
rear = [(-42, 60), (-42, 200), (-100, 200), (-100, 33), (-69, 33)]          # 45deg tail down to z33
front = [(14, 65.5), (44, 35), (60, 35), (60, 200), (14, 200)]              # 45deg drop to z35 at the front
for xa, xb in ((30, 50), (-50, -30)):
    K.append(prism("c_tail", rear, fX, xa, xb)); K.append(prism("c_front", front, fX, xa, xb))
cut(body, K); check(body)

# ---- unions
U = [box("fillR", 36.4, 39.4, -42, -31.5, 30.5, 64.5),                      # right window fill under the tray root
     box("pad", -36.2, 36.2, -91.6, -76.6, 0.0, 2.0),                        # grounded pad under the fins
     box("plate", -RW, RW, YP0, YP1, ZB, ZT)]                                # vertical tower plate
gus = [(YP1-1.0, 64), (10.0, 64), (YP1-1.0, 125)]
U += [prism("gusR", gus, fX, 36.2, 39.6), prism("gusL", gus, fX, -39.6, -36.2)]
prof = [(36.2, 41), (26, 51.2), (26, 60), (RW, 60), (RW, 49.05), (39.6, 44.4), (39.6, 41)]
U += [prism("trayR", prof, fY, YRAIL, YTRAY0), prism("trayL", mir(prof), fY, YRAIL, YTRAY0)]
railxy = [(PW, YP0+0.05), (RW, YP0+0.05), (RW, YRAIL), (LIPX, YRAIL), (LIPX, YLIP), (PW, YCH)]   # V4 rail section, vertical
U += [prism("railR", railxy, fZ, ZB, ZT), prism("railL", mir(railxy), fZ, ZB, ZT)]
union(body, U); check(body)

# ---- final cuts: bottom groove floor, lead-in chamfer, plate lightening window (gable top, no bridge)
K = []
for xa, xb in ((25.5, PW), (-PW, -25.5)):
    K.append(box("k_floor", xa, xb, YFLOOR, YP0+0.05, ZB, 70))
for xa, xb in ((25.5, LIPX-0.05), (-LIPX+0.05, -25.5)):
    K.append(prism("k_lead", [(YFLOOR, 56), (YFLOOR-4.0, 60), (YFLOOR-4.0, 70), (YFLOOR, 70)], fX, xa, xb))
K.append(prism("k_win", [(-22, 66), (22, 66), (22, 116), (0, 138), (-22, 116)], fY, -25, -15))
cut(body, K)
cleanup(body); ok = check(body); body.color = (0.8, 0.72, 0.4, 1)
print("slot depth", YP0 - YLIP, " groove", YP0 - YFLOOR, " lip over bezel", PW - LIPX)
