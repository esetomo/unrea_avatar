import bpy.ops
import sys
import os

filepath = sys.argv[-1]
name = os.path.basename(filepath).replace(".dae", "")

bpy.ops.object.mode_set(mode="OBJECT")

bpy.ops.object.select_name(name=name)
for mod in bpy.context.active_object.modifiers:
    if isinstance(mod, bpy.types.ArmatureModifier):
        bpy.ops.object.select_name(name=mod.object.name,extend=True)
    else:
        bpy.ops.object.modifier_apply(modifier=mod.name)

bpy.ops.wm.collada_export(filepath=filepath,selected=True)
bpy.ops.wm.quit_blender()
