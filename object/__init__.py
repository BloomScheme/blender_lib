from enum import Enum
import imp
from typing import List, Optional, Tuple
from xmlrpc.client import Boolean
from mathutils import Vector
import bpy

from bpy.types import Object

Objects = List[Object]


def get_active_object() -> Optional[Object]:
    return bpy.context.object


def set_active_object(object: Optional[Object]):
    bpy.context.view_layer.objects.active = object
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


def duplicate_objects(objects: Objects) -> Objects:
    deselect_all()
    select_objects(objects, True)
    bpy.ops.object.duplicate()
    return bpy.context.selected_objects

def filter_objects_by_type(objects: Objects, type:str) -> Objects:
    filtered_objects:Objects = []

    for object in objects:
        if object.type == type:
            filtered_objects.append(object)

    return filtered_objects


def get_3d_cursor_location() -> Vector:
    return bpy.context.scene.cursor.location

def set_3d_cursor_location(location:Vector):
    bpy.context.scene.cursor.location = location

def snap_3d_cursor_to_object():
    bpy.ops.view3d.snap_cursor_to_selected()

def set_origin_to_3d_cursor():
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

def is_mesh_object(object:Object):
    if object is None or object.type != "MESH":
        return False
    return True

def get_ancestors(object:Object):
    ancestors:Objects = []

    def store_parent(object: Object):
        if object.parent == None:
            return False
        ancestors.append(object.parent)
        store_parent(object.parent)

    store_parent(object)
    return ancestors
