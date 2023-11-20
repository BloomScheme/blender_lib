from enum import Enum
import imp
from optparse import Option
from typing import List, Optional, Tuple, Union
from xmlrpc.client import Boolean
from mathutils import Vector
import bpy

from bpy.types import Object

Objects = Union[bpy.types.BlendDataObjects, List[Object]]


def get_active_object() -> Optional[Object]:
    return bpy.context.object


def set_active_object(object: Optional[Object]):
    bpy.context.view_layer.objects.active = object  # type: ignore
    if object is not None:
        object.select_set(True)


def deselect_all():
    bpy.ops.object.select_all(action="DESELECT")


def select_objects(objects: Objects, value: Boolean):
    for object in objects:
        object.select_set(value)


def get_other_objects() -> Objects:
    others: Objects = []
    active = get_active_object()

    for object in bpy.context.selected_objects:
        if object != active:
            others.append(object)

    return others


def get_another_object() -> Optional[Object]:
    others = get_other_objects()
    if len(others) == 0:
        return None
    return others[0]


def duplicate_objects(objects: Objects) -> Objects:
    deselect_all()
    select_objects(objects, True)
    bpy.ops.object.duplicate()
    return bpy.context.selected_objects  # type: ignore


def filter_objects_by_type(objects: Objects, type: str) -> Objects:
    filtered_objects: Objects = []

    for object in objects:
        if object.type == type:
            filtered_objects.append(object)

    return filtered_objects


def get_object_by_name(objects: Objects, name: str) -> Optional[Object]:
    for obj in objects:
        if obj.name == name:
            return obj

    return None


def get_3d_cursor_location() -> Vector:
    return bpy.context.scene.cursor.location  # type: ignore


def set_3d_cursor_location(location: Vector):
    bpy.context.scene.cursor.location = location


def snap_3d_cursor_to_object():
    bpy.ops.view3d.snap_cursor_to_selected()


def set_origin_to_3d_cursor():
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR", center="MEDIAN")


def is_mesh_object(object: Object):
    if object is None or object.type != "MESH":
        return False
    return True


def get_ancestors(object: Object):
    ancestors: Objects = []

    def store_parent(object: Object):
        if object.parent == None:
            return False
        ancestors.append(object.parent)
        store_parent(object.parent)

    store_parent(object)
    return ancestors


def make_it_child(
    parent: Object,
    child: Object,
):
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="DESELECT")
    child.select_set(True)
    parent.select_set(True)
    bpy.context.view_layer.objects.active = parent
    bpy.ops.object.parent_set(type="OBJECT", keep_transform=True)

def move_local_direction(object:bpy.types.Object, vector:Vector):
    object.location += object.rotation_euler.to_matrix() @ vector # type: ignore
