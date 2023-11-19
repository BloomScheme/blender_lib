import re
import bpy, bmesh
from bpy.types import Object
from typing import List, Union, Literal
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
    if name not in object.vertex_groups:  # type: ignore
        return object.vertex_groups.new(name=name)
    return object.vertex_groups[name]


def set_vertex_group(
    object: Object, vertex_group_name: str, vetex_indices: List[int], weight: float
):
    vertex_group = get_or_create_vertex_group(object, vertex_group_name)
    vertex_group.add(vetex_indices, weight, "REPLACE")  # type: ignore


def get_freezed_mesh_object(object: Object):
    deselect_all()
    set_active_object(object)
    bpy.ops.object.convert(target="MESH", keep_original=True)
    return get_active_object()


def deselect_all_vertex(object: Object):
    if not is_mesh_object(object):
        raise ValueError("object is not mesh.")
    for vertex in object.data.vertices:  # type: ignore
        vertex.select = False


class BMeshHelper:
    def __init__(self, mesh: bpy.types.Mesh) -> None:
        self.mesh = mesh
        self.bmesh = bmesh.from_edit_mesh(mesh)

    def get_active_element(self, type: Literal["BMVert", "BMEdge", "BMFace"]):
        if self.bmesh.select_history:
            # self.bmesh.select_history を逆にたどっていく
            for elem in reversed(self.bmesh.select_history):  # type: ignore
                if type == "BMVert" and isinstance(elem, bmesh.types.BMVert):
                    return elem
                if type == "BMEdge" and isinstance(elem, bmesh.types.BMEdge):
                    return elem
                if type == "BMFace" and isinstance(elem, bmesh.types.BMFace):
                    return elem
        return None

    def get_active_vertex(self) -> bmesh.types.BMVert:
        return self.get_active_element("BMVert")  # type: ignore

    def get_active_edge(self) -> bmesh.types.BMEdge:
        return self.get_active_element("BMEdge")  # type: ignore

    def get_active_face(self) -> bmesh.types.BMFace:
        return self.get_active_element("BMFace")  # type: ignore

    def calc_edge_length_world(self, edge: bmesh.types.BMEdge):
        return (edge.verts[0].co - edge.verts[1].co).length  # type: ignore
    
    def get_edge_by_index(self, index: int) -> bmesh.types.BMEdge:
        self.bmesh.edges.ensure_lookup_table()
        return self.bmesh.edges[index]  # type: ignore
