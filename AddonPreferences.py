import random
import bpy
import os

import addon_utils




class NODESHELF_AddonPrefs(bpy.types.AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __package__

    for mod in addon_utils.modules():
        if mod.bl_info['name'] == "NodeShelf":
            filepath = mod.__file__
    folder = filepath.replace("__init__.py", "")

    data_folder: bpy.props.StringProperty(
        name="Data Folder",
        description="Choose a folder where NodeShelf can store all of its data",
        subtype="DIR_PATH",
        default=folder,
    )

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Welcome to the NodeShelf Add-on!")
        box = layout.box()
        box.prop(self, "data_folder")


def register():
    bpy.utils.register_class(NODESHELF_AddonPrefs)

def unregister():
    bpy.utils.unregister_class(NODESHELF_AddonPrefs)

