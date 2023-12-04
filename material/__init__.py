import bpy
import os


def append_material(filepath: str, material_name: str):
    bpy.ops.wm.append(
        filepath=os.path.join(filepath, "Materials", material_name),
        directory=os.path.join(filepath, "Materials"),
        filename=material_name,
    )
    material = bpy.data.materials[material_name]
    return material


def link_material(filepath: str, material_name: str):
    # https://blender.stackexchange.com/questions/17876/import-object-without-bpy-ops-wm-link-append
    with bpy.data.libraries.load(filepath) as (data_from, data_to): # type: ignore
        data_to.materials = [material_name]
    material = bpy.data.materials[material_name]
    return material


def get_or_link_material(filepath: str, material_name: str):
    if material_name in bpy.data.materials: # type: ignore
        return bpy.data.materials[material_name]
    return link_material(filepath, material_name)


def get_or_append_material(filepath: str, material_name: str):
    if material_name in bpy.data.materials: # type: ignore
        return bpy.data.materials[material_name]
    return append_material(filepath, material_name)
