import bpy

obj = bpy.data.objects['unrea_body']
mesh = obj.data

for vertex in mesh.vertices:
    for vg in vertex.groups:
        if vg.weight < 0.01:
            group = obj.vertex_groups[vg.group]
            print(group, vertex.index, vg.weight)
            group.remove([vertex.index])

for vertex in mesh.vertices:
    if len(vertex.groups) > 2:
        for vg in vertex.groups:
            group = obj.vertex_groups[vg.group]
            print(group, vertex.index, vg.weight)
        print("")           