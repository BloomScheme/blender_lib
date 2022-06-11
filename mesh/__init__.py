import re
import bpy
from bpy.types import Object
from typing import List
from mathutils import Vector

from ..collection import link_to_primary_collection
from ..object import deselect_all, get_active_object, is_mesh_object, set_active_object


def generate_mesh_object(
    name: str, vertices: List[Vector], edges: List[int], faces: List[int]
) -> Object:
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    object = bpy.data.objects.new(name, mesh)
    link_to_primary_collection(object)
    return object


def join_mesh_object_into(object: Object, target: Object):
    if object.type != "MESH":
        raise ValueError("object is not mesh.")
    if target.type != "MESH":
        raise ValueError("target is not mesh.")

    deselect_all()
    set_active_object(target)
    object.select_set(True)

    bpy.ops.object.join()


def get_or_create_vertex_group(object: Object, name: str):
    if not is_mesh_object(object):
        raise ValueError("object is not mesh.")
    if name not in object.vertex_groups:
        return object.vertex_groups.new(name=name)
    return object.vertex_groups[name]


def set_vertex_group(
    object: Object, vertex_group_name: str, vetex_indices: List[int], weight: float
):
    vertex_group = get_or_create_vertex_group(object, vertex_group_name)
    vertex_group.add(vetex_indices, weight, "REPLACE")


def get_freezed_mesh_object(object: Object):
    deselect_all()
    set_active_object(object)
    bpy.ops.object.convert(target="MESH", keep_original=True)
    return get_active_object()
