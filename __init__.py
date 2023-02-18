bl_info = {
    "name": "NodeShelf",
    "author": "Artificium Studios",
    "version": (2, 0),
    "blender": (3, 4, 0),
    "location": "View3D > UI > NodeShelf",
    "description": "NodeShelf is a blender add-on that manages your geometry node groups and provides tools that will help speed up your workflow across multiple projects.",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}

modulesNames = ['pilotScript', 'AddonPreferences']

import sys
import importlib


modulesFullNames = {}
for currentModuleName in modulesNames:
    modulesFullNames[currentModuleName] = ('{}.{}'.format(__name__, currentModuleName))

for currentModuleFullName in modulesFullNames.values():
    if currentModuleFullName in sys.modules:
        importlib.reload(sys.modules[currentModuleFullName])
    else:
        globals()[currentModuleFullName] = importlib.import_module(currentModuleFullName)
        setattr(globals()[currentModuleFullName], 'modulesNames', modulesFullNames)




def register():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                sys.modules[currentModuleName].register()


def unregister():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()


if __name__ == "__main__":
    register()
