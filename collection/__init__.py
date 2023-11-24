import bpy
from bpy.types import Object, Collection


def get_or_create_collection(name: str):
    if name in bpy.data.collections:  # type: ignore
        return bpy.data.collections[name]

    collection = bpy.data.collections.new(name=name)
    bpy.context.scene.collection.children.link(collection)
    return collection


def link_to_primary_collection(object: Object):
    bpy.context.scene.collection.children[0].objects.link(object)


def link_to_collection(collection: Collection, object: Object):
    if object.name in collection.objects:  # type: ignore
        return
    collection.objects.link(object)

def unlink_from_all_collections(object: Object):
    for collection in bpy.data.collections:  # type: ignore
        if object.name in collection.objects:  # type: ignore
            collection.objects.unlink(object)
