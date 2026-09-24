import bpy, mathutils, math, bmesh
from mathutils import Matrix
OUT="/private/tmp/claude-501/-Users-joneswang-Downloads-cart/123340a2-892d-4c68-b675-cc734aed0901/scratchpad/v6"
sc=bpy.context.scene; sc.render.engine='BLENDER_WORKBENCH'
sh=sc.display.shading; sh.light='STUDIO'; sh.color_type='OBJECT'; sh.show_cavity=True; sh.cavity_type='BOTH'; sh.show_shadows=False; sh.show_object_outline=True
sc.render.resolution_x=1300; sc.render.resolution_y=1000; sc.display.render_aa='8'
if sc.world: sc.world.color=(1,1,1)
def unex(lc):
    lc.exclude=False; lc.hide_viewport=False
    for c in lc.children: unex(c)
unex(bpy.context.view_layer.layer_collection)
cam_d=bpy.data.cameras.new("C"); cam_d.type='ORTHO'; cam_d.clip_start=1; cam_d.clip_end=5000
cam=bpy.data.objects.new("C",cam_d); sc.collection.objects.link(cam); sc.camera=cam
O=bpy.data.objects; V=mathutils.Vector
O["V6_Body"].color=(0.8,0.72,0.4,1)
def dummy(name,dims,M,col):
    bm=bmesh.new(); bmesh.ops.create_cube(bm,size=1.0); me=bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o=bpy.data.objects.new(name,me); sc.collection.objects.link(o); o.matrix_world=M@Matrix.Diagonal((dims[0],dims[1],dims[2],1)); o.color=col; return o
dummy("Bat",(72,44,22),Matrix.Translation((0,-49,11)),(0.12,0.12,0.12,1))
dummy("Phone",(79,12,160),Matrix.Translation((0,-20.9-6,54+80)),(0.2,0.4,0.9,1))   # 90deg, back on the plate face
def show(names):
    for o in O: o.hide_render = o.name not in names; o.hide_viewport=False
def shoot(tag,names,d,scale=230,ctr=V((0,-22,70))):
    show(names); d=V(d).normalized(); cam.location=ctr+d*1500
    cam.rotation_euler=(-d).to_track_quat('-Z','Y').to_euler(); cam_d.ortho_scale=scale
    sc.render.filepath=f"{OUT}/{tag}.png"; bpy.ops.render.render(write_still=True)
P=["V6_Body"]; B=P+["Bat"]
cam_d.clip_end=1500; shoot("1_side_left",B+["Phone"],(-1,0,0)); shoot("1b_side_left_nophone",B,(-1,0,0)); cam_d.clip_end=5000
shoot("2_front",P,(0,1,0)); shoot("3_rear",P,(0,-1,0)); shoot("3b_rear_phone",B+["Phone"],(0,-1,0.02),scale=300,ctr=V((0,-22,105)))
shoot("4_top34_rear",B+["Phone"],(-0.8,-1.2,0.9),scale=300,ctr=V((0,-22,100))); shoot("4b_top34_front",B,(-1,1.2,0.8))
shoot("5_rear_low",P,(0.5,-1,0.15)); shoot("6_tray_closeup",B,(-0.9,-1,0.9),scale=80,ctr=V((-30,-32,58)))
shoot("7_top",P,(0,-0.001,1))
