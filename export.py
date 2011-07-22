import bpy.ops
import sys
import os

def modify_armature():
    bpy.ops.object.mode_set(mode="EDIT")
    armature = bpy.context.active_object.data
    for bone in armature.edit_bones:
        bone.use_connect = False
    for bone in armature.edit_bones:
        bone.tail = (bone.head.x, bone.head.y + 0.1, bone.head.z)
        bone.roll = 0
    bpy.ops.object.mode_set(mode="OBJECT")

filepath = sys.argv[-1]
name = os.path.basename(filepath).replace(".dae", "")

bpy.ops.object.mode_set(mode="OBJECT")

bpy.ops.object.select_name(name=name)
# bpy.ops.object.vertex_group_normalize_all(lock_active=False)

for mod in bpy.context.active_object.modifiers:
    if isinstance(mod, bpy.types.ArmatureModifier):
        bpy.ops.object.select_name(name=mod.object.name)
        modify_armature()
        bpy.ops.object.select_name(name=name,extend=True)
    else:
        bpy.ops.object.modifier_apply(modifier=mod.name)

bpy.ops.wm.collada_export(filepath=filepath,selected=True)
bpy.ops.export_scene.fbx(filepath=name+".fbx",use_selection=True)
bpy.ops.wm.quit_blender()
