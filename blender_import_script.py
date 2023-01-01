import bpy
import bmesh
import numpy as np


verts = np.load("data.npy")
x_max = verts[:, 0].max()
y_max = verts[:, 1].max()
verts[:, 0] = verts[:, 0] - x_max
verts[:, 1] = verts[:, 1] - y_max 

mesh = bpy.data.meshes.new("mesh")
obj = bpy.data.objects.new(mesh.name, mesh)
col = bpy.data.collections["Collection"]
col.objects.link(obj)
bpy.context.view_layer.objects.active = obj

mesh.from_pydata(verts, [], [])