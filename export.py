import bpy.ops
import sys
import os

filepath = sys.argv[-1]
name = os.path.basename(filepath).replace(".dae", "")

bpy.ops.object.mode_set(mode="OBJECT")

bpy.ops.object.select_name(name="avatar")
bpy.ops.object.mode_set(mode="POSE")
bpy.ops.pose.select_all(action="SELECT")
bpy.ops.poselib.apply_pose()
bpy.ops.object.mode_set(mode="OBJECT")

bpy.ops.object.select_name(name=name)

for mod in bpy.context.active_object.modifiers:
    bpy.ops.object.modifier_apply(modifier=mod.name)

if bpy.context.active_object.parent:
    bpy.ops.object.select_name(name="avatar")
    bpy.ops.object.mode_set(mode="POSE")
    bpy.ops.pose.select_all(action="SELECT")
    bpy.ops.pose.armature_apply()
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_name(name=name)
    bpy.ops.object.select_name(name="avatar", extend=True)
    bpy.ops.object.parent_clear(type="CLEAR")
    bpy.ops.object.parent_set(type="ARMATURE")

bpy.ops.wm.collada_export(filepath=filepath,selected=True)
bpy.ops.wm.quit_blender()
