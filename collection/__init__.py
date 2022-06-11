import bpy
from bpy.types import Object, Collection

def get_or_create_collection(name:str):
    if name in bpy.data.collections:
        return bpy.data.collections[name]
    
    collection = bpy.data.collections.new(name=name)
    bpy.context.scene.collection.children.link(collection)
    return collection

def link_to_primary_collection(object: Object):
    bpy.context.scene.collection.children[0].objects.link(object)

def link_to_collection(collection:Collection, object:Object):
    if object.name in collection.objects:
        return
    collection.objects.link(object)
