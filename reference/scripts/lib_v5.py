# helper library (STL frame: plate top z=0, X right, Y front, Z up, mm)
import bpy, bmesh, math, struct
from mathutils import Vector, Matrix
SOLVER = 'MANIFOLD'
COLL = "FABLE_V5"
def coll(name=None):
    name = name or COLL
    c = bpy.data.collections.get(name)
    if not c:
        c = bpy.data.collections.new(name); bpy.context.scene.collection.children.link(c)
    return c
def prism(name, poly, fmap, t0, t1, cname=None):
    n = len(poly)
    def _x(p1, p2, p3, p4):
        d = lambda a, b, c: (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])
        return d(p1, p2, p3)*d(p1, p2, p4) < -1e-9 and d(p3, p4, p1)*d(p3, p4, p2) < -1e-9
    for i in range(n):
        for j in range(i+2, n):
            if (j+1) % n == i: continue
            assert not _x(poly[i], poly[(i+1) % n], poly[j], poly[(j+1) % n]), f"self-intersecting polygon in {name}"
    bm = bmesh.new()
    lo = [bm.verts.new(fmap(a, b, t0)) for a, b in poly]
    hi = [bm.verts.new(fmap(a, b, t1)) for a, b in poly]
    f0 = bm.faces.new(lo); f1 = bm.faces.new(list(reversed(hi)))
    for i in range(n):
        j = (i+1) % n; bm.faces.new([lo[j], lo[i], hi[i], hi[j]])
    bm.normal_update()
    res = bmesh.ops.triangulate(bm, faces=[f0, f1], quad_method='FIXED', ngon_method='EAR_CLIP')
    v3 = [Vector(fmap(a, b, t0)) for a, b in poly]
    nw = Vector((0, 0, 0))
    for i in range(n): nw += v3[i].cross(v3[(i+1) % n])
    cap = sum(f.calc_area() for f in res['faces']) / 2
    assert abs(cap - nw.length/2) < 1e-3*max(1.0, cap), f"bad cap triangulation in {name}"
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); coll(cname).objects.link(o); return o
fX = lambda y, z, x: (x, y, z)    # poly in (Y,Z), extrude along X
fY = lambda x, z, y: (x, y, z)    # poly in (X,Z), extrude along Y
fZ = lambda x, y, z: (x, y, z)    # poly in (X,Y), extrude along Z
def box(name, x0, x1, y0, y1, z0, z1, cname=None):
    return prism(name, [(y0, z0), (y1, z0), (y1, z1), (y0, z1)], fX, x0, x1, cname)
def mir(poly): return [(-a, b) for a, b in reversed(poly)]
def boolean(tgt, tool, op):
    m = tgt.modifiers.new("b", 'BOOLEAN'); m.operation = op; m.object = tool; m.solver = SOLVER
    with bpy.context.temp_override(object=tgt, active_object=tgt, selected_objects=[tgt]):
        bpy.ops.object.modifier_apply(modifier=m.name)
    me = tool.data; bpy.data.objects.remove(tool, do_unlink=True); bpy.data.meshes.remove(me)
def union(tgt, parts):
    for p in parts: boolean(tgt, p, 'UNION')
def cut(tgt, tools):
    for t in tools: boolean(tgt, t, 'DIFFERENCE')
def shells(bm):
    seen = set(); comps = []
    for v in bm.verts:
        if v.index in seen: continue
        st = [v]; c = []
        while st:
            w = st.pop()
            if w.index in seen: continue
            seen.add(w.index); c.append(w); st.extend(e.other_vert(w) for e in w.link_edges)
        comps.append(c)
    return comps
def cleanup(o):
    bm = bmesh.new(); bm.from_mesh(o.data); bm.verts.ensure_lookup_table()
    kill = [v for c in shells(bm) if len(c) < 12 for v in c]
    if kill: bmesh.ops.delete(bm, geom=kill, context='VERTS'); print("removed sliver verts:", len(kill))
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)
    bmesh.ops.dissolve_degenerate(bm, edges=bm.edges, dist=1e-5)
    loose = [e for e in bm.edges if not e.link_faces]
    if loose: bmesh.ops.delete(bm, geom=loose, context='EDGES')
    lv = [v for v in bm.verts if not v.link_edges]
    if lv: bmesh.ops.delete(bm, geom=lv, context='VERTS')
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(o.data); bm.free(); o.data.update()
def check(o):
    bm = bmesh.new(); bm.from_mesh(o.data)
    nm = sum(1 for e in bm.edges if not e.is_manifold); vol = bm.calc_volume(); sh = len(shells(bm))
    bb = [v.co for v in bm.verts]
    print(f"{o.name}: verts={len(bm.verts)} nonmanifold_edges={nm} shells={sh} volume={vol/1000:.1f} cm3 "
          f"bbox=({min(v.x for v in bb):.1f},{min(v.y for v in bb):.1f},{min(v.z for v in bb):.1f})..({max(v.x for v in bb):.1f},{max(v.y for v in bb):.1f},{max(v.z for v in bb):.1f})")
    bm.free(); return nm == 0 and sh == 1
def printcheck(name, res=1.0, zbed=0.0, eps=0.0):
    # eps: shifts the sample grid so voxel centres do not land exactly on flat faces (z22.5 roof, z35.5 gable, z7.5 notch),
    # which otherwise shows up as 1-voxel phantom islands. 0.0 keeps the V5..V7 behaviour.
    import numpy as np
    from mathutils.bvhtree import BVHTree
    o = bpy.data.objects[name]
    bm = bmesh.new(); bm.from_mesh(o.data); bmesh.ops.triangulate(bm, faces=bm.faces); bvh = BVHTree.FromBMesh(bm)
    co = np.array([v.co[:] for v in bm.verts]); mn, mx = co.min(0), co.max(0)
    xs = np.arange(mn[0]+res/2+eps, mx[0], res); ys = np.arange(mn[1]+res/2+eps, mx[1], res)
    nz = int(np.ceil((mx[2]-mn[2])/res)); zc = mn[2] + (np.arange(nz)+0.5)*res + eps
    V = np.zeros((nz, len(ys), len(xs)), bool); up = Vector((0, 0, 1))
    for iy, y in enumerate(ys):
        for ix, x in enumerate(xs):
            z = mn[2]-1.0; h = []
            while True:
                loc, nrm, idx, dist = bvh.ray_cast(Vector((x+1e-4, y+1e-4, z)), up)
                if loc is None: break
                if not h or loc.z-h[-1] > 1e-3: h.append(loc.z)
                z = loc.z+1e-4
            for a, b in zip(h[0::2], h[1::2]): V[(zc > a) & (zc < b), iy, ix] = True
    bm.free()
    islands = []; worst = []
    for k in range(1, nz):
        L = V[k]; below = V[k-1]; sup = np.zeros_like(L); pad = np.pad(below, 1)
        for dy in (0, 1, 2):
            for dx in (0, 1, 2): sup |= pad[dy:dy+L.shape[0], dx:dx+L.shape[1]]
        sup &= L
        lab = np.zeros(L.shape, int); cur = 0
        for sy, sx in zip(*np.nonzero(L)):
            if lab[sy, sx]: continue
            cur += 1; st = [(sy, sx)]; lab[sy, sx] = cur; cells = []
            while st:
                cy, cx = st.pop(); cells.append((cy, cx))
                for ny, nx in ((cy+1, cx), (cy-1, cx), (cy, cx+1), (cy, cx-1)):
                    if 0 <= ny < L.shape[0] and 0 <= nx < L.shape[1] and L[ny, nx] and not lab[ny, nx]:
                        lab[ny, nx] = cur; st.append((ny, nx))
            c = np.array(cells)
            if not sup[c[:, 0], c[:, 1]].any():
                islands.append((round(zc[k], 1), len(cells), round(xs[c[:, 1]].min(), 1), round(xs[c[:, 1]].max(), 1), round(ys[c[:, 0]].min(), 1), round(ys[c[:, 0]].max(), 1)))
        un = L & ~sup
        if un.any():
            d = np.zeros(L.shape, int); front = sup.copy(); seen = sup.copy(); step = 0
            while True:
                step += 1; p = np.pad(front, 1)
                grow = (p[:-2, 1:-1] | p[2:, 1:-1] | p[1:-1, :-2] | p[1:-1, 2:]) & L & ~seen
                if not grow.any(): break
                d[grow] = step; seen |= grow; front = grow
            m = d.max()
            if m*res >= 6:
                yy, xx = np.unravel_index(d.argmax(), d.shape); worst.append((int(m*res), round(zc[k], 1), round(xs[xx], 1), round(ys[yy], 1)))
    print(f"[{name}] res={res} voxels={V.sum()} layers={nz}")
    print("ISLANDS (start in mid-air):", islands if islands else "none")
    worst.sort(reverse=True); print("largest unsupported reach (mm to nearest support, z, x, y):", worst[:10])
    # first-layer footprint
    print("bed contact area mm2:", int(V[0].sum()*res*res))
    return islands
def export_clean(obj_name, path, zoff=0.0):
    o = bpy.data.objects[obj_name]
    bm = bmesh.new(); bm.from_mesh(o.data); v0 = bm.calc_volume()
    col = []
    for v in bm.verts:
        if len(v.link_edges) == 2:
            a, b = [e.other_vert(v).co - v.co for e in v.link_edges]
            if a.length > 1e-6 and b.length > 1e-6 and a.normalized().dot(b.normalized()) < -0.9999999: col.append(v)
    if col: bmesh.ops.dissolve_verts(bm, verts=col)
    bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method='FIXED', ngon_method='EAR_CLIP')
    for it in range(50):
        deg = [f for f in bm.faces if f.is_valid and f.calc_area() < 1e-6]
        if not deg: break
        f = deg[0]; e = max(f.edges, key=lambda e: e.calc_length())
        m = [v for v in f.verts if v not in e.verts][0]; p, q = e.verts
        others = [g for g in e.link_faces if g is not f]
        twins = [g for g in others if g.calc_area() < 1e-6 and m in g.verts]
        if twins: bmesh.ops.delete(bm, geom=[f, twins[0]], context='FACES_ONLY')
        else:
            g = others[0]; r = [v for v in g.verts if v not in e.verts][0]; nrm = g.normal.copy()
            bmesh.ops.delete(bm, geom=[f, g], context='FACES_ONLY')
            for tri in ((p, m, r), (m, q, r)):
                nf = bm.faces.new(tri); nf.normal_update()
                if nf.normal.dot(nrm) < 0: nf.normal_flip()
        loose = [ed for ed in bm.edges if not ed.link_faces]
        if loose: bmesh.ops.delete(bm, geom=loose, context='EDGES')
    lv = [v for v in bm.verts if not v.link_edges]
    if lv: bmesh.ops.delete(bm, geom=lv, context='VERTS')
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:]); bm.normal_update()
    bad = sum(1 for e in bm.edges if len(e.link_faces) != 2); zero = sum(1 for f in bm.faces if f.calc_area() < 1e-6)
    flip = sum(1 for e in bm.edges if len(e.link_faces) == 2 and not e.is_contiguous); comps = len(shells(bm)); vol = bm.calc_volume()
    print(f"[{obj_name}] tris={len(bm.faces)} edges_not_2_faces={bad} zero_area={zero} flipped={flip} components={comps} volume={vol/1000:.3f} cm3 (source {v0/1000:.3f})")
    ok = bad == 0 and zero == 0 and flip == 0 and comps == 1 and abs(vol-v0) < 0.5
    if ok:
        M = Matrix.Translation((0, 0, zoff))
        with open(path, "wb") as fh:
            fh.write(obj_name.encode().ljust(80, b" ")); fh.write(struct.pack("<I", len(bm.faces)))
            for t in bm.faces:
                v = [M @ l.vert.co for l in t.loops]; fh.write(struct.pack("<12fH", *t.normal, *v[0], *v[1], *v[2], 0))
        print("STL written:", path)
    else: print("NOT written - checks failed")
    bm.free(); return ok
