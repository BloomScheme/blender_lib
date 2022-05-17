import imp
from typing import List, Optional, Tuple
from xmlrpc.client import Boolean
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

