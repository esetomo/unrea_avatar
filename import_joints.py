import bpy
import xml.etree.ElementTree
import math

CHARACTER_DIR = "/Program Files (x86)/SecondLifeViewer2/character/"

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
        bone.use_inherit_rotation = False
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

def create_param_empty(panel, param, z):
    name = param.get("name")
    armature = armature_ob.data
    empty = bpy.data.objects.new(name, None)
    bpy.context.scene.objects.link(empty)
    empty.scale = (3, 3, 3)
    empty.location = (50, 0, z)
    empty.empty_draw_type = "SPHERE"
    empty.parent = panel
    limit_location = empty.constraints.new("LIMIT_LOCATION")
    limit_location.owner_space = "LOCAL"
    limit_location.min_x = 0
    limit_location.use_min_x = True
    limit_location.max_x = 100
    limit_location.use_max_x = True
    limit_location.min_y = 0
    limit_location.use_min_y = True
    limit_location.max_y = 0
    limit_location.use_max_y = True
    limit_location.min_z = z
    limit_location.use_min_z = True
    limit_location.max_z = z
    limit_location.use_max_z = True
    
    label = bpy.data.curves.new(name + " Label", "FONT")
    label.body = name
    label.align = "RIGHT"
    label_ob = bpy.data.objects.new(name + " Label", label)
    bpy.context.scene.objects.link(label_ob)    
    label_ob.location = (-5, 0, z - 1)
    label_ob.scale = (5, 5, 5)
    label_ob.rotation_euler = (math.pi/2, 0, 0)
    label_ob.parent = panel
    
    return empty

def add_scale_constraint(to, scale, value_min, value_max, target):
    c = to.constraints.new("TRANSFORM")
    c.owner_space = "LOCAL"
    c.from_min_x = 0
    c.from_max_x = 100
    c.map_from = "LOCATION"
    c.map_to = "SCALE"
    c.map_to_x_from = "X"
    c.map_to_y_from = "X"
    c.map_to_z_from = "X"
    c.target = target
    c.target_space = "LOCAL"
    c.to_min_x = 1.0 + scale[0] * value_min
    c.to_max_x = 1.0 + scale[0] * value_max
    c.to_min_y = 1.0 + scale[1] * value_min
    c.to_max_y = 1.0 + scale[1] * value_max
    c.to_min_z = 1.0 + scale[2] * value_min
    c.to_max_z = 1.0 + scale[2] * value_max

def add_offset_constraint(to, offset, value_min, value_max, target):
    c = to.constraints.new("TRANSFORM")
    c.owner_space = "LOCAL"
    c.from_min_x = 0
    c.from_max_x = 100
    c.map_from = "LOCATION"
    c.map_to = "LOCATION"
    c.map_to_x_from = "X"
    c.map_to_y_from = "X"
    c.map_to_z_from = "X"
    c.target = target
    c.target_space = "LOCAL"
    c.to_min_x = offset[0] * value_min
    c.to_max_x = offset[0] * value_max
    c.to_min_y = offset[1] * value_min
    c.to_max_y = offset[1] * value_max
    c.to_min_z = offset[2] * value_min
    c.to_max_z = offset[2] * value_max

def add_copy_constraint(to, type, target):
    c = to.constraints.new(type)
    c.target = target
    c.target_space = "LOCAL"
    c.use_offset = True
    c.use_x = True
    c.use_y = True
    c.use_z = True

def import_param_bone(panel, armature_ob, param_empty, value_min, value_max, bone_elem):
    name = bone_elem.get("name")
    bone = armature_ob.pose.bones[name]
    
    # TransformConstraint hasn't use_offset property
    constraint_empty = bpy.data.objects.new(param_empty.name + bone.name, None)
    bpy.context.scene.objects.link(constraint_empty)
    constraint_empty.parent = panel
    
    scale = get_vector(bone_elem, "scale")
    if scale:
        add_scale_constraint(constraint_empty, scale, value_min, value_max, param_empty)
        add_copy_constraint(bone, "COPY_SCALE", constraint_empty)
        
    offset = get_vector(bone_elem, "offset")
    if offset:
        add_offset_constraint(constraint_empty, offset, value_min, value_max, param_empty)
        add_copy_constraint(bone, "COPY_LOCATION", constraint_empty)

def import_param(panel, armature_ob, param, z):
    skeleton = param.find("param_skeleton")
    if skeleton is None:
        return
    
    value_min = float(param.get("value_min"))
    value_max = float(param.get("value_max"))
    
    param_empty = create_param_empty(panel, param, z)
    bpy.ops.object.select_name(name=armature_ob.name)
    bpy.ops.object.mode_set(mode="POSE")
    for bone_elem in skeleton.findall("bone"):
        import_param_bone(panel, armature_ob, param_empty, value_min, value_max, bone_elem)
        
    bpy.ops.object.mode_set(mode="OBJECT")

def import_lad(armature_ob):
    doc = xml.etree.ElementTree.parse(CHARACTER_DIR + "avatar_lad.xml")
    root = doc.getroot()
    skeleton = root.find("skeleton")
    
    panel = bpy.data.meshes.new("Panel")
    panel_ob = bpy.data.objects.new("Panel", panel)
    panel_ob.scale = (0.01, 0.01, 0.01)
    panel_ob.rotation_euler = (0, 0, math.pi/2)
    panel_ob.location = (0, 1, 2)
    bpy.context.scene.objects.link(panel_ob)
    z = -10
    for param in skeleton.findall("param"):
        import_param(panel_ob, armature_ob, param, z)
        z -= 10
        
    panel.vertices.add(4)
    panel.vertices[0].co = (-60, 0, 0)
    panel.vertices[1].co = (105, 0, 0)
    panel.vertices[2].co = (105, 0, z)
    panel.vertices[3].co = (-60, 0, z)
    panel.edges.add(4)
    panel.edges[0].vertices = (0, 1)
    panel.edges[1].vertices = (1, 2)
    panel.edges[2].vertices = (2, 3)
    panel.edges[3].vertices = (3, 0)
        
armature_ob = import_skeleton()
import_lad(armature_ob)