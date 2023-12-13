import bpy, bmesh, math
from bpy.types import Object
from typing import List, Union, Literal
from mathutils import Quaternion, Vector, Matrix

from ..collection import link_to_primary_collection
from ..object import (
    ObjectMode,
    deselect_all,
    get_active_object,
    is_mesh_object,
    set_active_object,
)


def min(a: float, b: float) -> float:
    if a < b:
        return a
    return b


def max(a: float, b: float) -> float:
    if a > b:
        return a
    return b


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


def align_object_to_normal(object: Object, normal: Vector):
    rotation_axis = normal.to_track_quat("Z", "Y")
    object.rotation_euler = rotation_axis.to_euler("XYZ")  # type: ignore
    object.rotation_euler.rotate_axis("Z", math.radians(90))


def calculate_face_normal(points: List[Vector]) -> Vector:
    return (points[1] - points[0]).cross(points[2] - points[0]).normalized()


def get_global_face_normal(object: Object, face_index: int) -> Vector:
    mesh: bpy.types.Mesh = object.data  # type: ignore
    face = mesh.polygons[face_index]
    global_points: List[Vector] = [object.matrix_world @ mesh.vertices[index].co for index in face.vertices]  # type: ignore
    return calculate_face_normal(global_points)
    # return object.matrix_world @ face.normal  # type: ignore


def rotation_of_global_normal(global_normal: Vector) -> Quaternion:
    return global_normal.to_track_quat("Z", "Y").to_matrix().to_4x4().to_quaternion()


def align_rotation_to_face_normal(object: Object, face_index: int):
    mesh: bpy.types.Mesh = object.data  # type: ignore

    # 法線をグローバル座標系に変換する
    global_normal = get_global_face_normal(object, face_index)

    # グローバル座標系における法線の逆変換行列を計算する
    rotation_matrix = global_normal.to_track_quat("Z", "Y").to_matrix().to_4x4()

    # メッシュデータに逆変換を適用する
    mesh.transform(rotation_matrix.inverted())

    # オブジェクトを回転させる
    object.rotation_mode = "QUATERNION"
    object.rotation_quaternion = rotation_matrix.to_quaternion()


class BMeshHelper:
    def __init__(self, object: bpy.types.Object) -> None:
        if object.type != "MESH":
            raise ValueError("object is not mesh.")
        self.object = object
        mesh: bpy.types.Mesh = object.data  # type: ignore
        self.mesh = mesh
        self.object_mode = ObjectMode(self.object)
        self.object_mode.set_mode("EDIT")
        self.bmesh = bmesh.from_edit_mesh(self.mesh)

    def exit(self):
        self.bmesh.free()
        self.object_mode.restore_mode()

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

    def get_face_of_edge(self, edge: bmesh.types.BMEdge) -> bmesh.types.BMFace:
        return edge.link_faces[0]  # type: ignore

    def scale_mesh(self, scale: Vector):
        self.bmesh.transform(Matrix.Diagonal(scale).to_4x4())

    def calc_dimensions(self) -> Vector:
        min_point = Vector((math.inf, math.inf, math.inf))
        max_point = Vector((-math.inf, -math.inf, math.inf))
        for vertex in self.bmesh.verts:  # type: ignore
            min_point.x = min(min_point.x, vertex.co.x)
            min_point.y = min(min_point.y, vertex.co.y)
            min_point.z = min(min_point.z, vertex.co.z)
            max_point.x = max(max_point.x, vertex.co.x)
            max_point.y = max(max_point.y, vertex.co.y)
            max_point.z = max(max_point.z, vertex.co.z)
        return max_point - min_point

    def set_dimensions(self, dimensions: Vector):
        current_dimensions = self.calc_dimensions()
        scale = Vector(
            (
                dimensions.x / current_dimensions.x,
                dimensions.y / current_dimensions.y,
                dimensions.z / current_dimensions.z,
            )
        )
        self.scale_mesh(scale)
