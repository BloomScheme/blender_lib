import bpy
import os


def append_node_tree(filepath: str, node_tree_name: str):
    # https://blender.stackexchange.com/questions/17876/import-object-without-bpy-ops-wm-link-append
    with bpy.data.libraries.load(filepath, link=True) as (data_from, data_to): # type: ignore
        data_to.node_groups = [node_tree_name]
    node_tree = bpy.data.node_groups[node_tree_name]
    return node_tree


def link_node_tree(filepath: str, node_tree_name: str):
    # https://blender.stackexchange.com/questions/17876/import-object-without-bpy-ops-wm-link-append
    with bpy.data.libraries.load(filepath, link=True) as (data_from, data_to): # type: ignore
        data_to.node_groups = [node_tree_name]
    node_tree = bpy.data.node_groups[node_tree_name]
    return node_tree


def get_or_link_node_tree(filepath: str, node_tree_name: str):
    if node_tree_name in bpy.data.node_groups: # type: ignore
        return bpy.data.node_groups[node_tree_name]
    return link_node_tree(filepath, node_tree_name)


def get_or_append_node_tree(filepath: str, node_tree_name: str):
    if node_tree_name in bpy.data.node_groups: # type: ignore
        return bpy.data.node_groups[node_tree_name]
    return append_node_tree(filepath, node_tree_name)
