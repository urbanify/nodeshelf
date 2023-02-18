import random
import bpy
import os
import subprocess
import sys
import csv
from bpy_extras.io_utils import ImportHelper
import shutil
import addon_utils

active_pack = 'Pack'


def send_to_blend(groupName):
    ## get blender exe automatically

    nodeshelf_props = bpy.context.scene.nodeshelf_props
    ns_prefs = bpy.context.preferences.addons['NodeShelf'].preferences
    pack_preview = nodeshelf_props.pack_preview
    packname = pack_preview.replace('.png', '.blend')
    data_folder = ns_prefs.data_folder
    packFolder = os.path.join(data_folder, "NodePacks")

    thisBlend = bpy.data.filepath
    blender = r'C:\Blender Launcher\stable\blender-3.3.0+lts.0759f671ce1f\blender.exe'
    blendFile = os.path.join(packFolder, packname)
    pyPath = sys.executable
    scriptFile = os.path.join(data_folder, "receiver.py")

    myargs = [blender, blendFile, "--background", "--python", scriptFile, "--", groupName, thisBlend]
    subprocess.run(myargs)


def get_node_groups(self, context):
    nodeshelf_props = context.scene.nodeshelf_props
    ns_prefs = context.preferences.addons['NodeShelf'].preferences
    pack_preview = nodeshelf_props.pack_preview
    packname = pack_preview.replace('.png', '.blend')
    data_folder = ns_prefs.data_folder
    packFolder = os.path.join(data_folder, "NodePacks")
    blendPath = os.path.join(packFolder, packname)
    ## append from blend
    items = []
    with bpy.data.libraries.load(blendPath, link=False) as (data_from, data_to):
        for ng in data_from.node_groups:
            if "NS_" in ng:
                name = ng.replace('NS_', '')
                item = (name, name, name)
                items.append(item)


    return items

def scan_dir(self, context, pcoll, enum_items, scDir, asset_list):
    # Scan the directory for png files
    image_paths = []
    for fn in os.listdir(scDir):
        if (fn.lower().endswith(".png")) or (fn.lower().endswith(".jpg")) or (fn.lower().endswith(".jpeg")):
            #if os.path.splitext(fn)[0] in asset_list:
            image_paths.append(fn)
    for i, name in enumerate(image_paths):
        # generates a thumbnail preview for a file.
        if ("Default" not in name):
            filepath = os.path.join(scDir, name)
            icon = pcoll.get(name)
            if not icon:
                thumb = pcoll.load(name, filepath, 'IMAGE')
            else:
                thumb = pcoll[name]
            enum_items.append((name, name, "", thumb.icon_id, i+1))
        x = i



    return enum_items

def get_previews(self, context):
    ns_prefs = context.preferences.addons['NodeShelf'].preferences
    nodeshelf_props = context.scene.nodeshelf_props
    data_folder = ns_prefs.data_folder
    items = []
    """EnumProperty callback"""
    enum_items = []

    if context is None:
        return enum_items
    enumDir = os.path.join(data_folder, "NodePacks")

    # Get the preview collection (defined in register func).
    pcoll = preview_collections["main"]

    if enumDir == pcoll.asset_preview_dir:
        return pcoll.asset_preview

    print("Scanning directory: %s" % enumDir)

    if enumDir and os.path.exists(enumDir):
        default = "Default.png"
        defIcon = pcoll.get(default)
        filepath = os.path.join(enumDir, default)
        if not defIcon:
            thumb = pcoll.load(default, filepath, 'IMAGE')
        else:
            thumb = pcoll[default]
        enum_items.append(("Default", "Default", "", thumb.icon_id, 0))

        enum_items = scan_dir(self, context, pcoll, enum_items, enumDir, 1)

    pcoll.asset_preview = enum_items
    pcoll.asset_preview_dir = enumDir
    return pcoll.asset_preview

def update_pack(self, context):
    global active_pack
    nodeshelf_props = context.scene.nodeshelf_props
    ns_prefs = context.preferences.addons['NodeShelf'].preferences
    pack_preview = nodeshelf_props.pack_preview
    active_pack = pack_preview.replace('.png', '')

class NSProps(bpy.types.PropertyGroup):
    width: bpy.props.FloatProperty(
        name="Width",
        description="Room Width",
        default=4,
        min=0, soft_max=10
    )
    folder_path: bpy.props.StringProperty(
        name="Folder Path",
        subtype='DIR_PATH',
        default=""
    )
    pack_name: bpy.props.StringProperty(
        name="Pack Name",
        default="Node Pack Name",
        description="your node pack will be saved with this name"
    )
    group_name: bpy.props.StringProperty(
        name="Group Name",
        default="Node Group Name",
        description="your node group will be saved with this name",

    )
    node_library: bpy.props.EnumProperty(
        name="Node Groups",
        description="Select the node group you want to load",
        items=get_node_groups
    )
    panel_text: bpy.props.StringProperty(
        name="Panel",
        description="",
        default="Output"
    )

    pack_preview: bpy.props.EnumProperty(
        items=get_previews,
        default=0,
        update=update_pack
    )

    auto_place: bpy.props.BoolProperty(
        name="Auto-Place",
        default=False,
    )



class NODESHELF_PT_Main(bpy.types.Panel):
    bl_idname = 'NODESHELF_PT_Main'
    bl_label = 'NodeShelf 2.0'
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'NodeShelf'

    def draw(self, context):
        nodeshelf_props = context.scene.nodeshelf_props
        layout = self.layout
        row = layout.row()
        op = self.layout.operator(
            'wm.url_open',
            text='Follow Us',
            icon='URL'
            )
        op.url = 'https://linktr.ee/urbanify.io'



class NODESHELF_PT_Packs(bpy.types.Panel):
    bl_idname = 'NODESHELF_PT_Packs'
    bl_label = 'Manage Packs'
    bl_parent_id = 'NODESHELF_PT_Main'
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'NodeShelf'

    def draw(self, context):
        nodeshelf_props = context.scene.nodeshelf_props
        pack_preview = nodeshelf_props.pack_preview
        layout = self.layout
        box = layout.box()
        row = box.row()
        row.alignment = 'CENTER'
        row.label(text="Choose or Create a Node Pack", icon="ASSET_MANAGER")
        row = box.row()
        row.template_icon_view(nodeshelf_props, "pack_preview")

        row = box.row()
        row.label(text=f"{pack_preview.replace('.png', '')} Pack")
        row.operator("nodeshelf.add_pack", text=f"", icon="ADD")
        row.operator("nodeshelf.remove_pack", text=f"", icon="REMOVE")
        row.operator("nodeshelf.assign_img", text=f"", icon="IMAGE_DATA")
        row.operator("nodeshelf.rename", text=f"", icon="GREASEPENCIL")


        box = box.box()
        row = box.row()
        row.prop(nodeshelf_props, "node_library")


class NODESHELF_PT_Save(bpy.types.Panel):
    bl_idname = 'NODESHELF_PT_Save'
    bl_label = 'Save Group to Pack'
    bl_parent_id = 'NODESHELF_PT_Main'
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'NodeShelf'

    def draw(self, context):
        global active_pack
        nodeshelf_props = context.scene.nodeshelf_props
        layout = self.layout
        box = layout.box()
        row = box.row()
        row.prop(nodeshelf_props, "group_name")
        row = box.row()
        row.operator("nodeshelf.save", text=f"Save Group to {active_pack} Pack")


class NODESHELF_PT_Load(bpy.types.Panel):
    bl_idname = 'NODESHELF_PT_Load'
    bl_label = 'Load Pack'
    bl_parent_id = 'NODESHELF_PT_Main'
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'NodeShelf'

    def draw(self, context):
        nodeshelf_props = context.scene.nodeshelf_props
        layout = self.layout
        box = layout.box()
        row = box.row()
        row.prop(nodeshelf_props, "auto_place")
        row = box.row()
        row.operator("nodeshelf.load_group")
        row.operator("nodeshelf.load")


class NODESHELF_PT_Tools(bpy.types.Panel):
    bl_idname = 'NODESHELF_PT_Tools'
    bl_label = 'NodeShelf Tools'
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'NodeShelf'

    def draw(self, context):
        nodeshelf_props = context.scene.nodeshelf_props
        layout = self.layout

        box = layout.box()
        row = box.row()
        row.label(text="Coming Soon", text_ctxt="", translate=True)





def formatNode(name):
    for mod in addon_utils.modules():
        if mod.bl_info['name'] == "NodeShelf":
            filepath = mod.__file__
    folder = filepath.replace("__init__.py", "")
    csvNames = os.path.join(folder, "NodeNames.csv")

    return ""


def refresh():
    addon_utils.disable("NodeShelf")
    addon_utils.enable("NodeShelf")

class NODESHELF_OT_assign_img(bpy.types.Operator, ImportHelper):
    bl_idname = 'nodeshelf.assign_img'
    bl_label = 'Assign Image to Pack'

    def execute(self, context):
        nodeshelf_props = context.scene.nodeshelf_props
        ns_prefs = context.preferences.addons['NodeShelf'].preferences

        pack_preview = nodeshelf_props.pack_preview
        data_folder = ns_prefs.data_folder
        packFolder = os.path.join(data_folder, "NodePacks")
        fdir = self.properties.filepath
        imgPath = fdir
        nuImgPath = os.path.join(packFolder, f"{pack_preview}")

        shutil.copy(imgPath, nuImgPath)

        refresh()

        return {'FINISHED'}

class NODESHELF_OT_rename(bpy.types.Operator):
    bl_idname = 'nodeshelf.rename'
    bl_label = 'Rename Pack'

    new_name: bpy.props.StringProperty(
        name="New Name",
        default=""
    )

    def execute(self, context):
        nodeshelf_props = context.scene.nodeshelf_props
        ns_prefs = context.preferences.addons['NodeShelf'].preferences

        pack_preview = nodeshelf_props.pack_preview
        data_folder = ns_prefs.data_folder
        packFolder = os.path.join(data_folder, "NodePacks")

        blendPath = os.path.join(packFolder, f"{pack_preview.replace('.png', '.blend')}")
        nuBlendPath = os.path.join(packFolder, f"{self.new_name}.blend")

        imgPath = os.path.join(packFolder, f"{pack_preview}")
        nuImgPath = os.path.join(packFolder, f"{self.new_name}.png")


        os.rename(blendPath, nuBlendPath)
        os.rename(imgPath, nuImgPath)


        refresh()

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


class NODESHELF_OT_remove_pack(bpy.types.Operator):
    bl_idname = 'nodeshelf.remove_pack'
    bl_label = 'Remove Pack'
    confirmation: bpy.props.EnumProperty(name="Are you Sure?", items=[
        ('Yes', 'Yes, Remove Forever', 'Remove Forever'),
        ('No', 'No, Keep this Pack', 'Keep This Pack')
    ], default=1)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        nodeshelf_props = context.scene.nodeshelf_props
        ns_prefs = context.preferences.addons['NodeShelf'].preferences
        pack_preview = nodeshelf_props.pack_preview
        data_folder = ns_prefs.data_folder
        packFolder = os.path.join(data_folder, "NodePacks")
        blendPath = os.path.join(packFolder, f"{pack_preview.replace('.png', '.blend')}")
        imgPath = os.path.join(packFolder, f"{pack_preview}")

        if self.confirmation == "Yes":
            os.remove(blendPath)
            os.remove(imgPath)

        refresh()

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


class NODESHELF_OT_add_pack(bpy.types.Operator):
    bl_idname = 'nodeshelf.add_pack'
    bl_label = 'Add Pack'
    bl_options = {'REGISTER', 'UNDO'}

    pack_name:bpy.props.StringProperty(name="Pack Name", default='Pack Name Here')

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        #Create New Blend File
        pname = self.pack_name
        nodeshelf_props = context.scene.nodeshelf_props
        ns_prefs = context.preferences.addons['NodeShelf'].preferences

        pack_preview = nodeshelf_props.pack_preview
        data_folder = ns_prefs.data_folder
        packFolder = os.path.join(data_folder, "NodePacks")

        blendPath = os.path.join(os.path.join(packFolder, "src"), "Empty.blend")
        nuBlendPath = os.path.join(packFolder, f"{pname}.blend")

        shutil.copy(blendPath, nuBlendPath)

        imgPath = os.path.join(os.path.join(packFolder, "src"), "Empty.png")
        nuImgPath = os.path.join(packFolder, f"{pname}.png")
        shutil.copy(imgPath, nuImgPath)

        refresh()

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)



class NODESHELF_OT_save(bpy.types.Operator):
    bl_idname = 'nodeshelf.save'
    bl_label = 'Save Group to Pack'
    bl_description = 'Select a Node Group and Save it to your Node Pack'


    @classmethod
    def poll(cls, context):
        nodeshelf_props = context.scene.nodeshelf_props
        group_name = nodeshelf_props.group_name
        active_tree = context.space_data.node_tree

        is_group = False
        for node in active_tree.nodes:
            if node.select == True:
                try:
                    grp_tree = node.node_tree
                    is_group = True
                except:
                    pass

        return is_group

    def execute(self, context):
        nodeshelf_props = context.scene.nodeshelf_props
        ns_prefs = context.preferences.addons['NodeShelf'].preferences
        data_folder = ns_prefs.data_folder

        active_tree = context.space_data.node_tree
        for node in active_tree.nodes:
            if node.select == True:
                grp_tree = node.node_tree
        nodeshelf_props.group_name = grp_tree.name
        send_to_blend(grp_tree.name)
        pass

        return {'FINISHED'}





def load_group(self, context):
    nodeshelf_props = context.scene.nodeshelf_props
    ns_prefs = context.preferences.addons['NodeShelf'].preferences
    data_folder = ns_prefs.data_folder
    node_library = nodeshelf_props.node_library
    csvFile = os.path.join(data_folder, f"{node_library}.csv")
    active_tree = context.space_data.node_tree

    exists = False
    for ng in bpy.data.node_groups:
        if ng.name == node_library:
            exists = True
    if not exists:
        pass

    else:
        self.report({"INFO"}, message="Node Group is already in this Blend file")


class NODESHELF_OT_load(bpy.types.Operator):
    bl_idname = 'nodeshelf.load'
    bl_label = 'Load Pack'
    bl_description = 'Load all the groups in the Selected Node Pack'

    def execute(self, context):
        nodeshelf_props = context.scene.nodeshelf_props
        ns_prefs = context.preferences.addons['NodeShelf'].preferences
        pack_preview = nodeshelf_props.pack_preview
        packname = pack_preview.replace('.png', '.blend')
        data_folder = ns_prefs.data_folder
        packFolder = os.path.join(data_folder, "NodePacks")
        blendPath = os.path.join(packFolder, packname)
        ## append from blend
        with bpy.data.libraries.load(blendPath, link=False) as (data_from, data_to):
            n_gs = []
            for ng in data_from.node_groups:
                if 'NS_' in ng:
                    if not existing(ng.replace('NS_', '')):
                        n_gs.append(ng)
                    else:
                        self.report({'INFO'}, message=f"Some or All Groups in Pack Already in File")
            data_to.node_groups = n_gs
        #Remove Prefix
        for ng in bpy.data.node_groups:
            theName = ng.name
            if theName.startswith("NS_"):
                ng.name = theName.replace('NS_', '')


        return {'FINISHED'}



def existing(theName):
    for ng in bpy.data.node_groups:
        if theName in ng.name:
            return True
    return False

class NODESHELF_OT_load_group(bpy.types.Operator):
    bl_idname = 'nodeshelf.load_group'
    bl_label = 'Load Group'
    bl_description = 'Load the Selected Group from the drop down menu'

    def execute(self, context):
        nodeshelf_props = context.scene.nodeshelf_props
        ns_prefs = context.preferences.addons['NodeShelf'].preferences
        pack_preview = nodeshelf_props.pack_preview
        node_library = nodeshelf_props.node_library
        auto_place = nodeshelf_props.auto_place

        packname = pack_preview.replace('.png', '.blend')
        data_folder = ns_prefs.data_folder
        packFolder = os.path.join(data_folder, "NodePacks")
        blendPath = os.path.join(packFolder, packname)

        active_tree = context.space_data.node_tree

        ## append from blend
        with bpy.data.libraries.load(blendPath, link=False) as (data_from, data_to):
            n_gs = []
            for ng in data_from.node_groups:
                if node_library in ng:
                    if not existing(node_library):
                        n_gs.append(ng)
                    else:
                        self.report({'INFO'}, message=f"{node_library} Already in File")
            data_to.node_groups = n_gs
        # Remove Prefix
        for ng in bpy.data.node_groups:
            theName = ng.name
            if theName.startswith("NS_"):
                ng.name = theName.replace('NS_', '')
                if auto_place:
                    nugroup = active_tree.nodes.new('GeometryNodeGroup')
                    nugroup.node_tree = ng

        return {'FINISHED'}


classes = [
    NSProps,NODESHELF_OT_assign_img,
    NODESHELF_OT_save,
    NODESHELF_OT_load,NODESHELF_OT_remove_pack,
    NODESHELF_OT_load_group,NODESHELF_OT_add_pack,NODESHELF_OT_rename,
    NODESHELF_PT_Main,NODESHELF_PT_Packs,
    NODESHELF_PT_Save,
    NODESHELF_PT_Load,NODESHELF_PT_Tools
]

preview_collections = {}
def register():
    pcoll = bpy.utils.previews.new()
    pcoll.asset_preview_dir = ""
    pcoll.asset_preview = ()
    preview_collections["main"] = pcoll
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.nodeshelf_props = bpy.props.PointerProperty(type=NSProps)



def unregister():
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.nodeshelf_props

