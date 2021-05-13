# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
#

bl_info = {
    "name": "TechDraw",
    "author": "Laurent Tesson",
    "version": (0,0,5),
    "location": "View 3D > Object Mode > Tool Shelf",
    "blender": (2, 82, 0),
    "description": "Outils for technical drawing",
    "warning": "",
    "category": "Object",
    }


if "bpy" in locals():
    import importlib
    importlib.reload(techdraw)
else:
    from . import techdraw

import bpy
import blf
import os
from bpy.types import Menu


def get_itemsScale(self, context):    
    prefs = bpy.context.preferences.addons['techdraw'].preferences        
    path = prefs.pathTemplates
    scales_file = path + os.sep + 'Scales.txt'
    
    l = [];    

    if(os.path.isfile(scales_file) == False):
        file = open(scales_file, "w")
        file.write('None,None,,' + '\n')
        file.write('1,1/1,,' + '\n')
        file.write('2,1/2,,' + '\n')
        file.write('5,1/5,,' + '\n')
        file.write('10,1/10,,' + '\n')
        file.write('20,1/20,,' + '\n')
        file.write('50,1/50,,' + '\n')
        file.write('100,1/100,,' + '\n')
        file.write('200,1/200,,' + '\n')
        file.write('500,1/500,,' + '\n')
        file.write('1000,1/1000,,' + '\n')
        file.close()

    with open(scales_file, 'r') as f:
        for line in f:
            s = line.split(',')
            l.append((s[1], s[1], s[2]))
    return l;


class IO_Prefs(bpy.types.AddonPreferences):
    bl_idname = __name__
    
    path = os.path.join(os.path.dirname(__file__), "templates")
    
    scaleSheets:  bpy.props.FloatProperty(default=10)    
    resolutionX:  bpy.props.IntProperty(default=4200)    
    pathTemplates:  bpy.props.StringProperty(default = path)
    
    def draw(self, context):
        layout = self.layout
        box = layout.box()
        split = box.split()
        col = split.column()
        col.label(text="Default Values:")
        col.prop(self, "scaleSheets",text="Scale Sheets")
        col.separator()
        col.prop(self, "resolutionX",text="Resolution X (px) render image")
        col.separator()
        col.prop(self, "pathTemplates",text="Path Templates")
        
# Register
classes = [
    techdraw.OB_PT_LSToolsPanel,
    techdraw.OB_PT_LSToolsPanelLayout,
    techdraw.OB_PT_LSToolsPanelRender,
    techdraw.OBJECT_OT_ApplyButton,
    techdraw.OBJECT_OT_UpdateButton,
    techdraw.OBJECT_OT_FormatButton,
    techdraw.OBJECT_OT_AddCameraButton,
    techdraw.OBJECT_OT_SFRenderButton,
    techdraw.OBJECT_OT_CageRefButton,
    techdraw.OBJECT_OT_CheckAllButton,
    techdraw.OBJECT_OT_HideCageButton,
    techdraw.OBJECT_OT_MultiAddButton,
    techdraw.OBJECT_OT_GridAddButton,
    techdraw.OBJECT_OT_OriginGridButton,
    techdraw.OBJECT_OT_CutDrawButton,
    techdraw.OBJECT_OT_CutAddButton,
    techdraw.OBJECT_OT_DrawPartsButton,
    techdraw.OBJECT_OT_HideCutterButton,
    techdraw.OBJECT_OT_TDModeButton,
    techdraw.OBJECT_OT_TDModeOffButton,
    techdraw.OBJECT_OT_TDModeAddButton,
    techdraw.OBJECT_OT_TDModeVisibleButton,    
    techdraw.OBJECT_OT_DupliBoolButton,
    techdraw.OBJECT_OT_SnapPartsButton,
    techdraw.OBJECT_OT_AddScaleButton,
    techdraw.OBJECT_OT_RemoveScaleButton,
    IO_Prefs,
]

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    
    bpy.types.Object.IO_scaleSheets = bpy.props.FloatProperty(
    name="Scale Sheets",
    description="Scale Sheets",
    min=0.01, max=100,
    default = bpy.context.preferences.addons['techdraw'].preferences.scaleSheets,
    )
    
    bpy.types.Object.IO_resolutionX = bpy.props.IntProperty(
    name="Resolution X (px) render image",
    description="Resolution X (px) render image",
    min=100, max=10000,
    default = bpy.context.preferences.addons['techdraw'].preferences.resolutionX,
    )
    
    path = os.path.join(os.path.dirname(__file__), "Templates")
    bpy.types.Object.IO_pathTemplates = bpy.props.StringProperty(
    name="pathTemplates",
    description="Path Templates",
    default = "path",
    )
    
    bpy.types.Scene.custom_scale = bpy.props.EnumProperty(items=get_itemsScale)

def unregister():    
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == "__main__":
    register()
