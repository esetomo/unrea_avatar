import bpy
import xml.etree.ElementTree
import math

CHARACTER_DIR = "/Program Files (x86)/SecondLifeViewer2/character/"

SHAPE = {
    'Male_Skeleton': 0,
    'Height': 0,
    'Thickness': 0,
    'Shoulders': 0,
    'Hip Width': 50,
    'Hip Length': 0,
    'Torso Length': 0,
    'EyeBone_Spread': 50,
    'EyeBone_Head_Shear': 50,
    'EyeBone_Head_Elongate': 50,
    'EyeBone_Bug': 50,
    'Head Size': 50,
    'Shoe_Heels': 0,
    'Shoe_Platform': 0,
    'Hand Size': 0,
    'Neck Thickness': 50,
    'EyeBone_Big_Eyes': 50,
    'Leg Length': 30,
    'Arm Length': 35,
    'Neck Length': 0,
}

def get_vector(elem, attr):
    v = elem.get(attr)    
    if v is None:
        return None
    a = v.split(" ")
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
        bone.use_inherit_scale = False
        bone.use_inherit_rotation = True
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

def add_scale(bone, scale, param_name, value_min, value_max, rev):
    param_value = SHAPE[param_name]
    value = value_min + (value_max - value_min) * param_value / 100.0
    scale_x = 1.0 + scale[0] * value
    scale_y = 1.0 + scale[1] * value
    scale_z = 1.0 + scale[2] * value

    if rev:
        bone.scale = (bone.scale.x / scale_x, bone.scale.y / scale_y, bone.scale.z / scale_z)
    else:    
        bone.scale = (bone.scale.x * scale_x, bone.scale.y * scale_y, bone.scale.z * scale_z)

def add_offset(bone, offset, param_name, value_min, value_max, rev):
    param_value = SHAPE[param_name]
    value = value_min + (value_max - value_min) * param_value / 100.0
    offset_x = offset[0] * value
    offset_y = offset[1] * value
    offset_z = offset[2] * value

    if rev:    
        bone.location = (bone.location.x - offset_x, bone.location.y - offset_y, bone.location.z - offset_z)
    else:
        bone.location = (bone.location.x + offset_x, bone.location.y + offset_y, bone.location.z + offset_z)

def import_param_bone(armature_ob, param_name, value_min, value_max, bone_elem, rev):
    name = bone_elem.get("name")
    bone = armature_ob.pose.bones[name]
    
    scale = get_vector(bone_elem, "scale")
    if scale:
        add_scale(bone, scale, param_name, value_min, value_max, rev)
        
    offset = get_vector(bone_elem, "offset")
    if offset:
        add_offset(bone, offset, param_name, value_min, value_max, rev)

def import_param(armature_ob, param, rev):
    skeleton = param.find("param_skeleton")
    if skeleton is None:
        return
    
    param_name = param.get("name")
    value_min = float(param.get("value_min"))
    value_max = float(param.get("value_max"))
    
    bpy.ops.object.select_name(name=armature_ob.name)
    bpy.ops.object.mode_set(mode="POSE")
    
    for bone_elem in skeleton.findall("bone"):
        import_param_bone(armature_ob, param_name, value_min, value_max, bone_elem, rev)

    bpy.ops.object.mode_set(mode="OBJECT")

def import_lad(armature_ob, rev):
    doc = xml.etree.ElementTree.parse(CHARACTER_DIR + "avatar_lad.xml")
    root = doc.getroot()
    skeleton = root.find("skeleton")
    
    for param in skeleton.findall("param"):
        import_param(armature_ob, param, rev)
                        
armature_ob = import_skeleton()
import_lad(armature_ob, False)

bpy.ops.object.select_name(name=armature_ob.name)
bpy.ops.object.mode_set(mode="POSE")
bpy.ops.pose.armature_apply()    
bpy.ops.object.mode_set(mode="OBJECT")

import_lad(armature_ob, True)

bpy.ops.object.select_name(name=armature_ob.name)
bpy.ops.object.mode_set(mode="POSE")
bpy.ops.poselib.new()
bpy.ops.poselib.pose_add(name="Default Shape")
bpy.ops.object.mode_set(mode="OBJECT")
