import bpy
import xml.etree.ElementTree
import math

CHARACTER_DIR = "/Program Files (x86)/SecondLifeViewer2/character/"

def get_vector(elem, attr):    
    a = elem.get(attr).split(" ")
    return list(map(float, a))

def build_bones(armature, parent, parent_bone):
    for elem in parent.findall("bone"):
        bone = armature.edit_bones.new(elem.get("name"))
        bone.parent = parent_bone
        v = get_vector(elem, "pos")
        if parent_bone:
            bone.head = (parent_bone.head.x + v[0], parent_bone.head.y + v[1], parent_bone.head.z + v[2])
        else:
            bone.head = v
        bone.tail = (bone.head.x, bone.head.y + 0.1, bone.head.z)
        bone.roll = 0
        build_bones(armature, elem, bone)

def import_skeleton():
    doc = xml.etree.ElementTree.parse(CHARACTER_DIR + "avatar_skeleton.xml")
    root = doc.getroot()

    armature = bpy.data.armatures.new("avatar")
    armature_ob = bpy.data.objects.new("avatar", armature)
    bpy.context.scene.objects.link(armature_ob)
    bpy.ops.object.select_name(name=armature_ob.name)
    bpy.ops.object.mode_set(mode="EDIT")

    build_bones(armature, root, None)
    
    bpy.ops.object.mode_set(mode="OBJECT")
    return armature_ob

def import_param(armature_ob, param, z):
    skeleton = param.find("param_skeleton")
    if skeleton is None:
        return
    
    name = param.get("name")
    armature = armature_ob.data
    empty = bpy.data.objects.new(name, None)
    bpy.context.scene.objects.link(empty)
    empty.scale = (0.03, 0.03, 0.03)
    empty.location = (0, 0, z)
    limit_location = empty.constraints.new("LIMIT_LOCATION")
    limit_location.min_x = 0
    limit_location.use_min_x = True
    limit_location.max_x = 0
    limit_location.use_max_x = True
    limit_location.min_y = 0
    limit_location.use_min_y = True
    limit_location.max_y = 1
    limit_location.use_max_y = True
    limit_location.min_z = z
    limit_location.use_min_z = True
    limit_location.max_z = z
    limit_location.use_max_z = True
    
    label = bpy.data.curves.new(name + " Label", "FONT")
    label.body = name
    label_ob = bpy.data.objects.new(name + " Label", label)
    bpy.context.scene.objects.link(label_ob)    
    label_ob.location = (0, -0.5, z)
    label_ob.scale = (0.05, 0.05, 0.05)
    label_ob.rotation_euler = (math.pi/2, 0, math.pi/2)

def import_lad(armature_ob):
    doc = xml.etree.ElementTree.parse(CHARACTER_DIR + "avatar_lad.xml")
    root = doc.getroot()
    skeleton = root.find("skeleton")
    z = -0.1
    for param in skeleton.findall("param"):
        import_param(armature_ob, param, z)
        z -= 0.1
        
armature_ob = import_skeleton()
import_lad(armature_ob)
