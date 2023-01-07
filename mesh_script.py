import bpy
import bmesh
import numpy as np


# must be in edit mode, add mesh to existing object
def create_mesh(verts, edges, faces):
    edit_obj = bpy.context.edit_object
    new_mesh = bpy.data.meshes.new("mesh")
    new_mesh.from_pydata(verts, edges, faces)
    bm = bmesh.from_edit_mesh(edit_obj.data)
    bm.from_mesh(new_mesh)
    bmesh.update_edit_mesh(edit_obj.data)


# creates new object
def new_mesh(verts, edges, faces):
    mesh = bpy.data.meshes.new("mesh")
    obj = bpy.data.objects.new(mesh.name, mesh)
    col = bpy.data.collections["Collection"]
    col.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    mesh.from_pydata(verts, edges, faces)


# faces
def faces_array(verts2):
    faces_array = []
    for pos0, vert in enumerate(verts2):
        try:
            pos1 = verts2.index((vert[0],vert[1]+5))
            pos2 = verts2.index((vert[0]+5,vert[1]+5))
            pos3 = verts2.index((vert[0]+5,vert[1]))
            faces_array.append([pos0, pos1, pos2, pos3])
        except ValueError:
            pass
    return faces_array

  
# edges
def edges_array(verts2):
    edges_array = []
    for pos0, vert in enumerate(verts2):
        try:
            pos1 = verts2.index((vert[0]+5, vert[1]))
            edges_array.append([pos0, pos1])
        except ValueError:
            pass    
        try:
            pos2 = verts2.index((vert[0], vert[1]+5))
            edges_array.append([pos0, pos2])
        except ValueError:
            pass   
    return edges_array


# load data
data = np.load("data.npy")

# center location to world origin
x_mean = data[:, 0].mean()
y_mean = data[:, 1].mean()
z_min = data[:, 2].min()
data[:, 0] = data[:, 0] - x_mean
data[:, 1] = data[:, 1] - y_mean
data[:, 2] = data[:, 2] - z_min

# need x,y,z data
verts = data[:, 0:3]

# x,y to tuples
verts2 = verts[:,0:2]
verts2 = [(row[0],row[1]) for row in verts.tolist()]


# two options to make a mesh

# 1st: make faces directly
faces = faces_array(verts2)
new_mesh(verts, [], faces)

# 2nd: make edges, then grid fill
#edges= edges_array(verts2)
#create_mesh(verts, edges, [])
     

'''
Script runs 35s on C8 data (39k verts).

For better view of results scale down and shade smooth.

'''
