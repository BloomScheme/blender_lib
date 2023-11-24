from typing import List, Literal, Optional
import bpy


def get_or_create_modifier(object: bpy.types.Object, name: str, type: str):
    if name in object.modifiers:  # type: ignore
        mod = object.modifiers[name]
        if mod.type != type:
            raise ValueError(f"modifier {name} is not {type}.")
        return object.modifiers[name]
    return object.modifiers.new(name, type)


def set_bool(
    name: str,
    object: bpy.types.Object,
    target: bpy.types.Object,
    operation: Literal["DIFFERENCE", "UNION", "INTERSECT"],
):
    boolean: bpy.types.BooleanModifier = get_or_create_modifier(object, name, "BOOLEAN")  # type: ignore
    boolean.object = target
    boolean.operation = operation
    boolean.solver = "EXACT"
    boolean.use_self = True
    boolean.use_hole_tolerant = True


def apply_modifier(name: str):
    try:
        bpy.ops.object.modifier_apply(modifier=name)
    except Exception as e:
        bpy.ops.object.modifier_remove(modifier=name)


class ModSortCondition:
    def __init__(
        self,
        type: Optional[str] = None,
        name: Optional[str] = None,
        keyword: Optional[str] = None,
        prefix: Optional[str] = None,
        suffix: Optional[str] = None,
    ) -> None:
        self.type = type
        self.name = name
        self.keyword = keyword
        self.prefix = prefix
        self.suffix = suffix

    def test(self, modifier: bpy.types.Modifier):
        if self.type is not None and modifier.type != self.type:
            return False
        if self.name is not None and modifier.name != self.name:
            return False
        if self.keyword is not None and self.keyword not in modifier.name:
            return False
        if self.prefix is not None and not modifier.name.startswith(self.prefix):
            return False
        if self.suffix is not None and not modifier.name.endswith(self.suffix):
            return False
        return True


class ModSorter:
    def __init__(self) -> None:
        self.mod_conditions: List[ModSortCondition] = []

    def add_condition(self, condition: ModSortCondition):
        self.mod_conditions.append(condition)

    def sort(self, object: bpy.types.Object):
        sorted_modifiers: List[bpy.types.Modifier] = []

        modifiers = object.modifiers
        for condition in self.mod_conditions:
            for modifier in modifiers:
                if condition.test(modifier):
                    sorted_modifiers.append(modifier)

        # for modifier in object.modifiers:
        #     if modifier not in sorted_modifiers:
        #         sorted_modifiers.append(modifier)

        for modifier in sorted_modifiers:
            from_index = object.modifiers.find(modifier.name)
            object.modifiers.move(from_index, len(object.modifiers) - 1)
