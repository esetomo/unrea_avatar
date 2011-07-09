import bpy.ops
import sys
import os

filepath = sys.argv[-1]
name = os.path.basename(filepath).replace(".dae", "")

if bpy.context.active_object:
    if bpy.context.active_object.mode == "EDIT":
        bpy.ops.object.editmode_toggle()

scene = bpy.context.scene

for obj in scene.objects:
    if obj.name != name:
        scene.objects.unlink(obj)

bpy.ops.object.select_name(name=name)
for mod in bpy.context.active_object.modifiers:
    bpy.ops.object.modifier_apply(modifier=mod.name)

bpy.ops.wm.collada_export(filepath=filepath)
bpy.ops.wm.quit_blender()
