import sys
import os
import bpy
import Blender
from Blender import Scene, Window, Object

lib = bpy.libraries.load("//unrea.blend")
scene = lib.scenes.append("Scene")
scene.makeCurrent()

filepath = sys.argv[-1]
name = os.path.basename(filepath).replace("24.dae", "")

Window.EditMode(0)

obj = Object.Get(name)
obj.select(1)

bpy.ops.wm.collada_export(filepath=filepath,selected=True)

# Blender.Quit()

