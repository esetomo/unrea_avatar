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
    if len(vertex.groups) > 4:
        for vg in vertex.groups:
            group = obj.vertex_groups[vg.group]
            print(group, vertex.index, vg.weight)
        print("")           
        
for vertex in mesh.vertices:
    if len(vertex.groups) == 0:
        print(vertex)

for vertex in mesh.vertices:
    total = 0
    for vg in vertex.groups:
        total += vg.weight
    if total != 1.0:
        print(vertex.index, total)
        
for vertex in mesh.vertices:
    print(vertex.co)

print("end")
