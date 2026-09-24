import bpy, bmesh, math
exec(open("/private/tmp/claude-501/-Users-joneswang-Downloads-cart/123340a2-892d-4c68-b675-cc734aed0901/scratchpad/lib_v5.py").read())
STL = "/Users/joneswang/Downloads/cart/FableV4_OnePiece.stl"
T10 = math.tan(math.radians(10.0))
Z0, YC0, TP, ZT = 54.0, -20.2, 3.2, 154.0        # phone-bottom level, plate contact face at Z0, plate thickness, tower top
def Yc(z): return YC0 - (z - Z0) * T10           # phone-contact face of the 100deg tower plate
def Yf(z): return Yc(z) + TP                     # its front (+Y) face
XI, XO = 36.3, 39.5                              # side wall inner / outer faces (from V4)
PW, RW = 40.75, 44.25                            # rail inner / outer half width (slot 81.5)
LIPX = 36.25                                     # lip inner edge (3.25 mm over the bezel)
YLIP, YRAIL = -53.8, -57.3                       # lip face (phone side) / rail rear face
YTRAY0 = -17.0
# treads: 100 / 95 / 100deg positions -> phone front-bottom corner stops
YT = [Yc(Z0)]                                    # -20.2
for th in (10, 5, 0): YT.append(Yc(ZT) + 100*math.tan(math.radians(th)) - 12*math.cos(math.radians(th)) - 0.9)
print("tread stops (Y):", [round(y, 1) for y in YT])   # [-20.2, -33.0?, -42.1, -50.7]

def wipe():
    c = bpy.data.collections.get(COLL)
    if c:
        for o in list(c.objects):
            me = o.data; bpy.data.objects.remove(o, do_unlink=True)
            if me and me.users == 0: bpy.data.meshes.remove(me)
wipe()
sc = bpy.context.scene; sc.unit_settings.scale_length = 0.001; sc.unit_settings.length_unit = 'MILLIMETERS'
for o in list(sc.collection.objects):
    if o.type == 'MESH': bpy.data.objects.remove(o, do_unlink=True)      # default cube etc.
before = set(bpy.data.objects)
bpy.ops.wm.stl_import(filepath=STL)
body = [o for o in bpy.data.objects if o not in before][0]
for c in list(body.users_collection): c.objects.unlink(body)
coll().objects.link(body); body.name = "V5_Body"; body.data.name = "V5_Body"
check(body)

# ---- cuts: remove the 35deg upper structure, rear stub, deck ribs over the bay, trim rear comb
cut(body, [box("c_top", -60, 60, -120, 70, 65, 300),
           box("c_rear", -60, 60, -120, -91.9, 2.5, 300),
           box("c_ribs", -XI, XI, -76.5, -19.9, 22, 70),
           box("c_comb", -XI, XI, -93, -76.4, 45, 70)])
check(body)

# ---- unions: window fills under the tower, grounded pad under the fins
union(body, [box("fillR", 36.4, 39.4, -66.5, -31.5, 30.5, 64.5),
             box("fillL", -39.4, -36.4, -55.5, -33.5, 42.5, 64.5),
             box("pad", -36.2, 36.2, -91.6, -76.6, 0.0, 2.0)])
# ---- tower plate (100deg, rooted in the mast), front gussets
union(body, [prism("plate", [(Yc(Z0), Z0), (Yf(Z0), Z0), (Yf(ZT), ZT), (Yc(ZT), ZT)], fX, -RW, RW)])
gus = [(Yf(64)-1.0, 64), (10.0, 64), (Yf(125)-1.0, 125)]
union(body, [prism("gusR", gus, fX, 36.2, 39.6), prism("gusL", gus, fX, -39.6, -36.2)])
# ---- trays (haunch in, flare out), rails, lips
prof = [(36.2, 41), (26, 51.2), (26, 66), (RW, 66), (RW, 49.05), (39.6, 44.4), (39.6, 41)]
union(body, [prism("trayR", prof, fY, YRAIL, YTRAY0), prism("trayL", mir(prof), fY, YRAIL, YTRAY0)])
rail = [(Yf(Z0), Z0), (YRAIL, Z0), (YRAIL, ZT), (Yf(ZT), ZT)]
union(body, [prism("railR", rail, fX, PW, RW), prism("railL", rail, fX, -RW, -PW),
             box("lipR", LIPX, RW, YRAIL, YLIP, Z0, ZT), box("lipL", -RW, -LIPX, YRAIL, YLIP, Z0, ZT)])
# ---- stepped treads (3 positions), cut from both trays; +Y edge follows the leaning plate face
K = []
for sg in (1, -1):
    xa, xb = sorted((sg*25.5, sg*PW))
    K.append(prism("t0", [(YT[1], 54), (Yc(54)-0.05, 54), (Yc(70)-0.05, 70), (YT[1], 70)], fX, xa, xb))
    K.append(box("t1", xa, xb, YT[2], YT[1], 57, 70))
    K.append(box("t2", xa, xb, YT[3], YT[2], 60, 70))
cut(body, K)
cleanup(body); ok = check(body)
body.color = (0.8, 0.72, 0.4, 1)
