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

from bpy.props import *
from bpy.types import AddonPreferences
import sys
import math
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
import bpy
import bmesh
import mathutils
import os
from math import *
from bpy.props import (
    BoolProperty,
    EnumProperty,
    FloatProperty,
    IntProperty,
)
from bpy.types import WindowManager


class OBJECT_OT_ApplyButton(bpy.types.Operator):
    bl_idname = "tkdw.apply"
    bl_label = "Add part view"

    def execute(self, context):

        refX = 0
        refY = 0
        refZ = 0
        refDimX = 0
        refDimY = 0
        refDimZ = 0
        refState = False

        resultRef = not bpy.context.scene.Ref is None
        resultRef = resultRef and (
            bpy.context.scene.Ref.name in context.view_layer.objects)

        if resultRef == True:
            target_ref = bpy.context.scene.Ref
            bpy.ops.object.select_all(action='DESELECT')
            target_ref.select_set(state=True)
            bpy.context.view_layer.objects.active = target_ref
            refState = True
            refX = bpy.context.object.location[0]
            refY = bpy.context.object.location[1]
            refZ = bpy.context.object.location[2]
            refDimX = bpy.context.object.dimensions[0]
            refDimY = bpy.context.object.dimensions[1]
            refDimZ = bpy.context.object.dimensions[2]

        result = not bpy.context.scene.Target is None
        result = result and (
            bpy.context.scene.Target.name in context.view_layer.objects)

        if result == True:
            target_obj = bpy.context.scene.Target
            dim_draw = bpy.context.scene.draw_distance

            xValueC = bpy.context.scene.cursor.location[0]
            yValueC = bpy.context.scene.cursor.location[1]
            zValueC = bpy.context.scene.cursor.location[2]

            bpy.ops.object.select_all(action='DESELECT')
            target_obj.select_set(state=True)
            bpy.context.view_layer.objects.active = target_obj

            bpy.ops.object.transform_apply(
                location=False, rotation=True, scale=False)

            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

            xmin = bpy.context.object.location[0]
            xmax = bpy.context.object.location[0]
            ymin = bpy.context.object.location[1]
            ymax = bpy.context.object.location[1]
            zmin = bpy.context.object.location[2]
            zmax = bpy.context.object.location[2]

            matrix = target_obj.matrix_world
            vertObj = target_obj.data.vertices

            for v in vertObj:
                vPos = matrix@v.co
                xV = vPos[0]
                yV = vPos[1]
                zV = vPos[2]
                if xV < xmin:
                    xmin = xV
                if xV > xmax:
                    xmax = xV
                if yV < ymin:
                    ymin = yV
                if yV > ymax:
                    ymax = yV
                if zV < zmin:
                    zmin = zV
                if zV > zmax:
                    zmax = zV

            dimX = bpy.context.object.dimensions[0]
            dimY = bpy.context.object.dimensions[1]
            dimZ = bpy.context.object.dimensions[2]

            bpy.context.scene.cursor.location[0] = xmin + ((xmax - xmin)/2)
            bpy.context.scene.cursor.location[1] = ymin + ((ymax - ymin)/2)
            bpy.context.scene.cursor.location[2] = zmin + ((zmax - zmin)/2)

            bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

            locX = bpy.context.object.location[0]
            locY = bpy.context.object.location[1]
            locZ = bpy.context.object.location[2]

            if refState == True:
                bpy.context.scene.cursor.location[0] = refX
                bpy.context.scene.cursor.location[1] = refY
                bpy.context.scene.cursor.location[2] = refZ
                bpy.ops.object.origin_set(
                    type='ORIGIN_CURSOR', center='MEDIAN')

                locX = refX
                locY = refY
                locZ = refZ
                dimX = refDimX
                dimY = refDimY
                dimZ = refDimZ

            if bpy.context.scene.lv_bool:
                bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={
                                              "linked": False, "mode": 'TRANSLATION'}, TRANSFORM_OT_translate={"value": (0, 0, 0)})
                bpy.context.object.location[0] = locX + \
                    dim_draw + dimX/2 + dimZ/2
                bpy.context.object.rotation_euler[1] = pi/2
                rd = bpy.context.active_object
                OBJECT_OT_ApplyButton.calculOrigin(rd)

            bpy.ops.object.select_all(action='DESELECT')
            target_obj.select_set(state=True)
            bpy.context.view_layer.objects.active = target_obj

            if bpy.context.scene.rv_bool:
                bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={
                                              "linked": False, "mode": 'TRANSLATION'}, TRANSFORM_OT_translate={"value": (0, 0, 0)})
                bpy.context.object.location[0] = locX - \
                    dim_draw - dimX/2 - dimZ/2
                bpy.context.object.rotation_euler[1] = -pi/2
                rd = bpy.context.active_object
                OBJECT_OT_ApplyButton.calculOrigin(rd)

            bpy.ops.object.select_all(action='DESELECT')
            target_obj.select_set(state=True)
            bpy.context.view_layer.objects.active = target_obj

            if bpy.context.scene.bv_bool:
                bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={
                                              "linked": False, "mode": 'TRANSLATION'}, TRANSFORM_OT_translate={"value": (0, 0, 0)})
                bpy.context.object.location[0] = locX + \
                    dim_draw + dimX/2 + dimZ + dim_draw + dimX/2
                bpy.context.object.rotation_euler[1] = pi
                rd = bpy.context.active_object
                OBJECT_OT_ApplyButton.calculOrigin(rd)

            bpy.ops.object.select_all(action='DESELECT')
            target_obj.select_set(state=True)
            bpy.context.view_layer.objects.active = target_obj

            if bpy.context.scene.dv_bool:
                bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={
                                              "linked": False, "mode": 'TRANSLATION'}, TRANSFORM_OT_translate={"value": (0, 0, 0)})
                bpy.context.object.location[1] = locY + \
                    dim_draw + dimY/2 + dimZ/2
                bpy.context.object.rotation_euler[0] = -pi/2
                rd = bpy.context.active_object
                OBJECT_OT_ApplyButton.calculOrigin(rd)

            bpy.ops.object.select_all(action='DESELECT')
            target_obj.select_set(state=True)
            bpy.context.view_layer.objects.active = target_obj

            if bpy.context.scene.uv_bool:
                bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={
                                              "linked": False, "mode": 'TRANSLATION'}, TRANSFORM_OT_translate={"value": (0, 0, 0)})
                bpy.context.object.location[1] = locY - \
                    dim_draw - dimY/2 - dimZ/2
                bpy.context.object.rotation_euler[0] = pi/2
                rd = bpy.context.active_object
                OBJECT_OT_ApplyButton.calculOrigin(rd)

            bpy.ops.object.select_all(action='DESELECT')
            target_obj.select_set(state=True)
            bpy.context.view_layer.objects.active = target_obj

            if bpy.context.scene.drv_bool:
                bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={
                                              "linked": False, "mode": 'TRANSLATION'}, TRANSFORM_OT_translate={"value": (0, 0, 0)})
                bpy.context.object.location[0] = locX + \
                    dim_draw + dimX/2 + dimZ/2
                bpy.context.object.location[1] = locY - \
                    dim_draw - dimY/2 - dimZ/2
                bpy.context.object.rotation_euler[0] = pi/4
                bpy.context.object.rotation_euler[1] = pi/4
                rd = bpy.context.active_object
                OBJECT_OT_ApplyButton.calculOrigin(rd)

            bpy.ops.object.select_all(action='DESELECT')
            target_obj.select_set(state=True)
            bpy.context.view_layer.objects.active = target_obj

            if bpy.context.scene.dlv_bool:
                bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={
                                              "linked": False, "mode": 'TRANSLATION'}, TRANSFORM_OT_translate={"value": (0, 0, 0)})
                bpy.context.object.location[0] = locX - \
                    dim_draw - dimX/2 - dimZ/2
                bpy.context.object.location[1] = locY - \
                    dim_draw - dimY/2 - dimZ/2
                bpy.context.object.rotation_euler[0] = pi/4
                bpy.context.object.rotation_euler[1] = -pi/4
                rd = bpy.context.active_object
                OBJECT_OT_ApplyButton.calculOrigin(rd)

            bpy.ops.object.select_all(action='DESELECT')
            target_obj.select_set(state=True)
            bpy.context.view_layer.objects.active = target_obj

            if bpy.context.scene.urv_bool:
                bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={
                                              "linked": False, "mode": 'TRANSLATION'}, TRANSFORM_OT_translate={"value": (0, 0, 0)})
                bpy.context.object.location[0] = locX + \
                    dim_draw + dimX/2 + dimZ/2
                bpy.context.object.location[1] = locY + \
                    dim_draw + dimY/2 + dimZ/2
                bpy.context.object.rotation_euler[0] = -pi/4
                bpy.context.object.rotation_euler[1] = pi/4
                rd = bpy.context.active_object
                OBJECT_OT_ApplyButton.calculOrigin(rd)

            bpy.ops.object.select_all(action='DESELECT')
            target_obj.select_set(state=True)
            bpy.context.view_layer.objects.active = target_obj

            if bpy.context.scene.ulv_bool:
                bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={
                                              "linked": False, "mode": 'TRANSLATION'}, TRANSFORM_OT_translate={"value": (0, 0, 0)})
                bpy.context.object.location[0] = locX - \
                    dim_draw - dimX/2 - dimZ/2
                bpy.context.object.location[1] = locY + \
                    dim_draw + dimY/2 + dimZ/2
                bpy.context.object.rotation_euler[0] = -pi/4
                bpy.context.object.rotation_euler[1] = -pi/4
                rd = bpy.context.active_object
                OBJECT_OT_ApplyButton.calculOrigin(rd)

            bpy.ops.object.select_all(action='DESELECT')
            target_obj.select_set(state=True)
            bpy.context.view_layer.objects.active = target_obj
            rd = bpy.context.active_object
            OBJECT_OT_ApplyButton.calculOrigin(rd)

            bpy.context.scene.cursor.location[0] = xValueC
            bpy.context.scene.cursor.location[1] = yValueC
            bpy.context.scene.cursor.location[2] = zValueC

            bpy.context.scene.fv_bool = False
            bpy.context.scene.lv_bool = False
            bpy.context.scene.rv_bool = False
            bpy.context.scene.bv_bool = False
            bpy.context.scene.uv_bool = False
            bpy.context.scene.dv_bool = False
            bpy.context.scene.ulv_bool = False
            bpy.context.scene.urv_bool = False
            bpy.context.scene.dlv_bool = False
            bpy.context.scene.drv_bool = False
            context.window_manager.checkAll = False

        return {'FINISHED'}

    def calculOrigin(rd):

        bpy.ops.object.select_all(action='DESELECT')
        rd.select_set(state=True)
        bpy.context.view_layer.objects.active = rd
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        rotX = bpy.context.object.rotation_euler[0]
        rotY = bpy.context.object.rotation_euler[1]
        rotZ = bpy.context.object.rotation_euler[2]
        xmin = bpy.context.object.location[0]
        xmax = bpy.context.object.location[0]
        ymin = bpy.context.object.location[1]
        ymax = bpy.context.object.location[1]
        zmin = bpy.context.object.location[2]
        zmax = bpy.context.object.location[2]

        matrix = rd.matrix_world
        vertObj = rd.data.vertices

        for v in vertObj:
            vPos = matrix@v.co
            xV = vPos[0]
            yV = vPos[1]
            zV = vPos[2]
            if xV < xmin:
                xmin = xV
            if xV > xmax:
                xmax = xV
            if yV < ymin:
                ymin = yV
            if yV > ymax:
                ymax = yV
            if zV < zmin:
                zmin = zV
            if zV > zmax:
                zmax = zV

        dimX = bpy.context.object.dimensions[0]
        dimY = bpy.context.object.dimensions[1]
        dimZ = bpy.context.object.dimensions[2]

        bpy.context.scene.cursor.location[0] = xmin + ((xmax - xmin)/2)
        bpy.context.scene.cursor.location[1] = ymin + ((ymax - ymin)/2)
        bpy.context.scene.cursor.location[2] = zmin + ((zmax - zmin)/2)

        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

        return {'FINISHED'}


class OBJECT_OT_UpdateButton(bpy.types.Operator):
    bl_idname = "tkdw.update"
    bl_label = "Update view"

    def execute(self, context):

        xValueC = bpy.context.scene.cursor.location[0]
        yValueC = bpy.context.scene.cursor.location[1]
        zValueC = bpy.context.scene.cursor.location[2]

        resultUpdate = not bpy.context.scene.Update is None
        resultUpdate = resultUpdate and (
            bpy.context.scene.Update.name in context.view_layer.objects)

        if resultUpdate == True:
            updater = bpy.context.scene.Update

            locXObj = []
            locYObj = []
            locZObj = []

            nbObj = len(bpy.context.selected_objects)

            if nbObj > 0:
                listObj = bpy.context.selected_objects
                listObj.append(updater)
                for o in listObj:
                    OBJECT_OT_ApplyButton.calculOrigin(o)
                for o in listObj:
                    o.select_set(state=True)
                    bpy.context.view_layer.objects.active = o

            if nbObj > 0:
                listObj = bpy.context.selected_objects
                listObj.append(updater)
                updater.select_set(state=True)
                bpy.context.view_layer.objects.active = updater
                for o in listObj:
                    # OBJECT_OT_ApplyButton.calculOrigin(o)
                    locXObj.append(o.location[0])
                    locYObj.append(o.location[1])
                    locZObj.append(o.location[2])

            bpy.ops.object.make_links_data(type='OBDATA')
            bpy.ops.object.make_single_user(
                type='SELECTED_OBJECTS', object=True, obdata=True, material=False, animation=False)

            i = 0
            if nbObj > 0:
                listObj = bpy.context.selected_objects
                for o in listObj:
                    OBJECT_OT_ApplyButton.calculOrigin(o)
                    coordXObj = locXObj[i]
                    coordYObj = locYObj[i]
                    coordZObj = locZObj[i]
                    o.location[0] = coordXObj
                    o.location[1] = coordYObj
                    o.location[2] = coordZObj
                    i = i + 1
                    OBJECT_OT_DrawPartsButton.refreshTextureCut(o)
                    bpy.ops.object.select_all(action='DESELECT')

            bpy.context.scene.cursor.location[0] = xValueC
            bpy.context.scene.cursor.location[1] = yValueC
            bpy.context.scene.cursor.location[2] = zValueC

        bpy.context.scene.Update = None

        return {'FINISHED'}


class OBJECT_OT_AddCameraButton(bpy.types.Operator):
    bl_idname = "tkdw.cam"
    bl_label = "Add camera"

    def execute(self, context):

        resultTarget = not bpy.context.scene.Target is None
        resultTarget = resultTarget and (
            bpy.context.scene.Target.name in context.view_layer.objects)

        if resultTarget == True:
            target_obj = bpy.context.scene.Target
            bpy.ops.object.select_all(action='DESELECT')
            target_obj.select_set(state=True)
            bpy.context.view_layer.objects.active = target_obj
            xTarget = bpy.context.object.location[0]
            yTarget = bpy.context.object.location[1]
        else:
            xTarget = 0
            yTarget = 0

        result = not bpy.context.scene.Collection is None
        if result == True:
            target_collection = bpy.context.scene.Collection
            nameCollection = target_collection.name
            self.master_collection = bpy.context.scene.collection
            self.layer_collection = bpy.data.collections[nameCollection]

            bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(
                xTarget, yTarget, 10), rotation=(0, 0, 0))
            bpy.context.object.name = "Cam_view"

            bpy.context.object.data.type = 'ORTHO'
            bpy.context.object.data.ortho_scale = 5
            bpy.ops.object.move_to_collection(
                collection_index=0, is_new=False, new_collection_name="")
            self.layer_collection.objects.link(bpy.context.object)
            self.master_collection.objects.unlink(bpy.context.object)

            bpy.context.scene.camera = bpy.data.objects["Cam_view"]

        return {'FINISHED'}


class OBJECT_OT_FormatButton(bpy.types.Operator):
    bl_idname = "tkdw.format"
    bl_label = "Add sheets"

    def execute(self, context):

        scene_collection = bpy.context.view_layer.layer_collection
        bpy.context.view_layer.active_layer_collection = scene_collection

        prefs = bpy.context.preferences.addons[__package__].preferences

        path = prefs.pathTemplates
        scaleSheetsPref = prefs.scaleSheets

        formatSheets = bpy.context.scene.format_type
        formatOrientation = bpy.context.scene.orientation_type
        formatCartridge = bpy.context.scene.cartridge_type

        sheets = formatSheets + "_" + formatOrientation

        fileNameForAppend = "FormatSheets.blend\\Collection\\" + sheets

        bpy.ops.wm.append(
            filepath="FormatSheets.blend",
            directory=path,
            filename=fileNameForAppend)

        bpy.ops.object.select_all(action='DESELECT')

        if formatCartridge != "None":

            bpy.data.objects[sheets].select_set(state=True)
            bpy.context.view_layer.objects.active = bpy.data.objects[sheets]
            c01 = bpy.context.active_object
            xSheets = bpy.context.object.dimensions[0]
            ySheets = bpy.context.object.dimensions[1]

            fileNameForAppend = "FormatSheets.blend\\Collection\\" + formatCartridge

            bpy.ops.wm.append(
                filepath="FormatSheets.blend",
                directory=path,
                filename=fileNameForAppend)

            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects[formatCartridge].select_set(state=True)
            bpy.context.view_layer.objects.active = bpy.data.objects[formatCartridge]
            c02 = bpy.context.active_object

            bpy.context.object.location[0] = (xSheets/2) - 0.007
            bpy.context.object.location[1] = (-ySheets/2) + 0.007

            bpy.ops.object.select_all(action='DESELECT')

            CoC = c02.constraints.new(type='CHILD_OF')
            CoC.name = "childSheets"
            bpy.context.object.constraints[CoC.name].target = bpy.data.objects[sheets]

            bpy.data.objects[sheets].select_set(state=True)
            bpy.context.view_layer.objects.active = bpy.data.objects[sheets]

            bpy.context.object.scale[0] = scaleSheetsPref
            bpy.context.object.scale[1] = scaleSheetsPref

            bpy.ops.object.select_all(action='DESELECT')

            CoC.name = "childOfSheets"
            c01.name = sheets + "1"
            c02.name = formatCartridge + "_1"

            bpy.data.collections[sheets].children.link(
                bpy.data.collections[formatCartridge])
            master_collection = bpy.context.scene.collection
            master_collection.children.unlink(
                bpy.data.collections[formatCartridge])

            bpy.data.collections[formatCartridge].name = formatCartridge + "_1"
            bpy.data.collections[sheets].name = sheets + "_1"

        return {'FINISHED'}


class OBJECT_OT_SFRenderButton(bpy.types.Operator):
    bl_idname = "tkdw.sfrender"
    bl_label = "Update settings"

    def execute(self, context):

        resultSheets = not bpy.context.scene.Sheets is None
        resultSheets = resultSheets and (
            bpy.context.scene.Sheets.name in context.view_layer.objects)
        resultCamera = not bpy.context.scene.Camera is None
        resultCamera = resultCamera and (
            bpy.context.scene.Camera.name in context.view_layer.objects)

        if (resultSheets == True) and (resultCamera == True):

            prefs = bpy.context.preferences.addons[__package__].preferences
            resolX = prefs.resolutionX

            target_Sheets = bpy.context.scene.Sheets
            target_Camera = bpy.context.scene.Camera

            bpy.ops.object.select_all(action='DESELECT')
            target_Sheets.select_set(state=True)
            bpy.context.view_layer.objects.active = target_Sheets

            if bpy.context.scene.custom_scale != 'None':
                line = bpy.context.scene.custom_scale
                s = line.split('/')
                bpy.context.object.scale[0] = (int(s[1])/int(s[0]))
                bpy.context.object.scale[1] = (int(s[1])/int(s[0]))

            bpy.ops.object.select_all(action='DESELECT')
            target_Sheets.select_set(state=True)
            bpy.context.view_layer.objects.active = target_Sheets

            xdim = bpy.context.object.dimensions[0]
            ydim = bpy.context.object.dimensions[1]

            bpy.context.scene.render.resolution_x = resolX

            if (xdim - ydim) >= 0:
                bpy.context.scene.render.resolution_y = resolX * (ydim/xdim)
            if (xdim - ydim) < 0:
                bpy.context.scene.render.resolution_y = resolX * (ydim/xdim)

            bpy.ops.object.select_all(action='DESELECT')
            target_Camera.select_set(state=True)
            bpy.context.view_layer.objects.active = target_Camera

            if (xdim - ydim) >= 0:
                bpy.context.object.data.ortho_scale = xdim
            if (xdim - ydim) < 0:
                bpy.context.object.data.ortho_scale = ydim

            xLocCam = bpy.context.object.location[0]
            yLocCam = bpy.context.object.location[1]

            bpy.ops.object.select_all(action='DESELECT')
            target_Sheets.select_set(state=True)
            bpy.context.view_layer.objects.active = target_Sheets

            bpy.context.object.location[0] = xLocCam
            bpy.context.object.location[1] = yLocCam

            bpy.ops.object.select_all(action='DESELECT')

        return {'FINISHED'}


class OBJECT_OT_CageRefButton(bpy.types.Operator):
    bl_idname = "tkdw.cageref"
    bl_label = "Multi-parts Ref"

    def execute(self, context):

        nbObj = len(bpy.context.selected_objects)

        if nbObj > 0:
            xmin = bpy.context.object.location[0]
            xmax = bpy.context.object.location[0]
            ymin = bpy.context.object.location[1]
            ymax = bpy.context.object.location[1]
            zmin = bpy.context.object.location[2]
            zmax = bpy.context.object.location[2]

            listObj = bpy.context.selected_objects

            for o in listObj:
                matrix = o.matrix_world
                vertObj = o.data.vertices

                for v in vertObj:
                    vPos = matrix@v.co
                    xV = vPos[0]
                    yV = vPos[1]
                    zV = vPos[2]
                    if xV < xmin:
                        xmin = xV
                    if xV > xmax:
                        xmax = xV
                    if yV < ymin:
                        ymin = yV
                    if yV > ymax:
                        ymax = yV
                    if zV < zmin:
                        zmin = zV
                    if zV > zmax:
                        zmax = zV

            bpy.ops.mesh.primitive_cube_add(
                size=1, enter_editmode=False, location=(0, 0, 0))
            bpy.context.object.display_type = 'WIRE'
            bpy.context.object.hide_render = True
            bpy.context.object.name = "Ref"
            bpy.context.object.location[0] = (xmin + xmax) / 2
            bpy.context.object.location[1] = (ymin + ymax) / 2
            bpy.context.object.location[2] = (zmin + zmax) / 2

            bpy.context.object.scale[0] = xmax - xmin
            bpy.context.object.scale[1] = ymax - ymin
            bpy.context.object.scale[2] = zmax - zmin
            bpy.context.scene.Ref = bpy.context.object

        return {'FINISHED'}


class OBJECT_OT_CheckAllButton(bpy.types.Operator):
    bl_idname = "tkdw.checkall"
    bl_label = ""
    bl_description = "Check or Uncheck all view"

    def execute(self, context):

        if context.window_manager.checkAll is False:
            context.window_manager.checkAll = True
            bpy.context.scene.fv_bool = True
            bpy.context.scene.lv_bool = True
            bpy.context.scene.rv_bool = True
            bpy.context.scene.bv_bool = True
            bpy.context.scene.uv_bool = True
            bpy.context.scene.dv_bool = True
            bpy.context.scene.ulv_bool = True
            bpy.context.scene.urv_bool = True
            bpy.context.scene.dlv_bool = True
            bpy.context.scene.drv_bool = True
        else:
            context.window_manager.checkAll = False
            bpy.context.scene.fv_bool = False
            bpy.context.scene.lv_bool = False
            bpy.context.scene.rv_bool = False
            bpy.context.scene.bv_bool = False
            bpy.context.scene.uv_bool = False
            bpy.context.scene.dv_bool = False
            bpy.context.scene.ulv_bool = False
            bpy.context.scene.urv_bool = False
            bpy.context.scene.dlv_bool = False
            bpy.context.scene.drv_bool = False

        return {'FINISHED'}


class OBJECT_OT_HideCageButton(bpy.types.Operator):
    bl_idname = "tkdw.hidecage"
    bl_label = ""
    bl_description = ""

    def execute(self, context):

        resultRef = not bpy.context.scene.Ref is None
        resultRef = resultRef and (
            bpy.context.scene.Ref.name in context.view_layer.objects)

        if resultRef == True:
            target_ref = bpy.context.scene.Ref
            bpy.ops.object.select_all(action='DESELECT')
            target_ref.select_set(state=True)
            bpy.context.view_layer.objects.active = target_ref

            if context.window_manager.hideCages is False:
                context.window_manager.hideCages = True
                bpy.context.object.hide_viewport = False

            else:
                context.window_manager.hideCages = False
                bpy.context.object.hide_viewport = True
            bpy.ops.object.select_all(action='DESELECT')

        return {'FINISHED'}


class OBJECT_OT_MultiAddButton(bpy.types.Operator):
    bl_idname = "tkdw.multiadd"
    bl_label = "Add multi-parts view"
    bl_description = ""

    def execute(self, context):

        if bpy.context.scene.fv_bool == True:
            fv = True
        else:
            fv = False
        if bpy.context.scene.lv_bool == True:
            lv = True
        else:
            lv = False
        if bpy.context.scene.rv_bool == True:
            rv = True
        else:
            rv = False
        if bpy.context.scene.bv_bool == True:
            bv = True
        else:
            bv = False
        if bpy.context.scene.uv_bool == True:
            uv = True
        else:
            uv = False
        if bpy.context.scene.dv_bool == True:
            dv = True
        else:
            dv = False
        if bpy.context.scene.ulv_bool == True:
            ulv = True
        else:
            ulv = False
        if bpy.context.scene.urv_bool == True:
            urv = True
        else:
            urv = False
        if bpy.context.scene.dlv_bool == True:
            dlv = True
        else:
            dlv = False
        if bpy.context.scene.drv_bool == True:
            drv = True
        else:
            drv = False

        nbObj = len(bpy.context.selected_objects)
        i = 0

        if nbObj > 0:
            listObj = bpy.context.selected_objects
            for o in listObj:
                i = i + 1
                bpy.context.scene.Target = o
                OBJECT_OT_ApplyButton.execute(self, context)
                if i < nbObj:
                    bpy.context.scene.fv_bool = fv
                    bpy.context.scene.lv_bool = lv
                    bpy.context.scene.rv_bool = rv
                    bpy.context.scene.bv_bool = bv
                    bpy.context.scene.uv_bool = uv
                    bpy.context.scene.dv_bool = dv
                    bpy.context.scene.ulv_bool = ulv
                    bpy.context.scene.urv_bool = urv
                    bpy.context.scene.dlv_bool = dlv
                    bpy.context.scene.drv_bool = drv

        return {'FINISHED'}


class OBJECT_OT_GridAddButton(bpy.types.Operator):
    bl_idname = "tkdw.gridadd"
    bl_label = "Add table"
    bl_description = ""

    def execute(self, context):

        resultGrid = not bpy.context.scene.Target_Table is None
        resultGrid = resultGrid and (
            bpy.context.scene.Target_Table.name in context.view_layer.objects)
        resultCollecGrid = not bpy.context.scene.Collection_Table is None

        if (resultGrid == True) and (resultCollecGrid == True):

            xValueC = bpy.context.scene.cursor.location[0]
            yValueC = bpy.context.scene.cursor.location[1]
            zValueC = bpy.context.scene.cursor.location[2]

            target_collection = bpy.context.scene.Collection_Table
            nameCollection = target_collection.name
            self.master_collection = bpy.context.scene.collection
            self.layer_collection = bpy.data.collections[nameCollection]

            xSubdivisions = bpy.context.scene.x_Subdivisions + 1
            ySubdivisions = bpy.context.scene.y_Subdivisions + 1
            textGridBool = bpy.context.scene.textGrid_bool
            targetTable = bpy.context.scene.Target_Table

            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects[targetTable.name].select_set(state=True)
            bpy.context.view_layer.objects.active = bpy.data.objects[targetTable.name]
            c03 = bpy.context.active_object

            scaleY = bpy.context.object.scale[0]
            xDimTarget = 0.196 * scaleY

            bpy.ops.object.select_all(action='DESELECT')

            bpy.ops.mesh.primitive_grid_add(
                x_subdivisions=xSubdivisions, y_subdivisions=ySubdivisions, size=xDimTarget, enter_editmode=True, location=(0, 0, 0))
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.mark_freestyle_edge(clear=False)
            bpy.ops.object.editmode_toggle()

            bpy.context.object.dimensions[1] = 0.007 * \
                (ySubdivisions - 1) * scaleY
            bpy.ops.object.transform_apply(
                location=False, rotation=False, scale=True)

            if context.window_manager.orignGridState == 1:
                bpy.context.scene.cursor.location[0] = xDimTarget / 2
                bpy.context.scene.cursor.location[1] = (
                    (-0.007) * (ySubdivisions-1) * scaleY) / 2
                bpy.context.scene.cursor.location[2] = 0
                locXText = xDimTarget
                locYText = 0
            if context.window_manager.orignGridState == 2:
                bpy.context.scene.cursor.location[0] = -xDimTarget / 2
                bpy.context.scene.cursor.location[1] = (
                    (-0.007) * (ySubdivisions-1) * scaleY) / 2
                bpy.context.scene.cursor.location[2] = 0
                locXText = 0
                locYText = 0
            if context.window_manager.orignGridState == 3:
                bpy.context.scene.cursor.location[0] = xDimTarget / 2
                bpy.context.scene.cursor.location[1] = (
                    (0.007) * (ySubdivisions-1) * scaleY) / 2
                bpy.context.scene.cursor.location[2] = 0
                locXText = xDimTarget
                locYText = (0.007) * (ySubdivisions-1) * scaleY
            if context.window_manager.orignGridState == 4:
                bpy.context.scene.cursor.location[0] = -xDimTarget / 2
                bpy.context.scene.cursor.location[1] = (
                    (0.007) * (ySubdivisions-1) * scaleY) / 2
                bpy.context.scene.cursor.location[2] = 0
                locXText = 0
                locYText = (0.007) * (ySubdivisions-1) * scaleY

            bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

            bpy.context.object.location[0] = 0
            bpy.context.object.location[1] = 0

            c01 = bpy.context.active_object

            material_name = "GridColor"
            materialGrid = bpy.data.materials.get(material_name)

            if materialGrid is None:
                materialGrid = bpy.data.materials.new(material_name)

            materialGrid.use_nodes = True

            principled_bsdf = materialGrid.node_tree.nodes.get(
                'Principled BSDF')

            if principled_bsdf is not None:
                principled_bsdf.inputs[0].default_value = (1, 1, 1, 1)

            bpy.data.objects[c01.name].active_material = materialGrid

            bpy.ops.object.move_to_collection(
                collection_index=0, is_new=False, new_collection_name="")
            self.layer_collection.objects.link(bpy.context.object)
            self.master_collection.objects.unlink(bpy.context.object)

            if textGridBool == True:

                material_name = "TextColor"
                materialFont = bpy.data.materials.get(material_name)

                if materialFont is None:
                    materialFont = bpy.data.materials.new(material_name)

                materialFont.use_nodes = True

                principled_bsdf = materialFont.node_tree.nodes.get(
                    'Principled BSDF')

                if principled_bsdf is not None:
                    principled_bsdf.inputs[0].default_value = (0, 0, 0, 1)
                    principled_bsdf.inputs[5].default_value = 0

                dimTxt = 0.006 * scaleY
                for l in range(ySubdivisions - 1):
                    for c in range(xSubdivisions - 1):
                        bpy.ops.object.text_add(
                            radius=dimTxt, enter_editmode=False, location=(0, 0, 0))
                        bpy.context.object.location[0] = (
                            c * ((xDimTarget)/(xSubdivisions - 1))) + (0.001 * scaleY) - locXText
                        bpy.context.object.location[1] = (
                            l * (0.007 * scaleY)) + (0.002 * scaleY) - locYText
                        nameText = bpy.context.active_object
                        bpy.data.objects[nameText.name].active_material = materialFont

                        bpy.ops.object.move_to_collection(
                            collection_index=0, is_new=False, new_collection_name="")
                        self.layer_collection.objects.link(bpy.context.object)
                        self.master_collection.objects.unlink(
                            bpy.context.object)

                        c02 = bpy.context.active_object
                        bpy.ops.object.select_all(action='DESELECT')
                        CoC = c02.constraints.new(type='CHILD_OF')
                        CoC.name = "childTxtGrid"
                        bpy.context.object.constraints[CoC.name].target = bpy.data.objects[c01.name]
                        bpy.data.objects[c01.name].select_set(state=True)
                        bpy.context.view_layer.objects.active = bpy.data.objects[c01.name]

                        bpy.ops.object.select_all(action='DESELECT')
                        CoC.name = "childOfTxtGrid"
                        c02.name = c02.name + "_1"

                c01.name = c01.name + "_1"
                bpy.data.objects[c01.name].select_set(state=True)
                bpy.context.view_layer.objects.active = bpy.data.objects[c01.name]

                bpy.context.object.location[0] = xValueC
                bpy.context.object.location[1] = yValueC
                bpy.context.object.location[2] = zValueC

                bpy.context.scene.cursor.location[0] = xValueC
                bpy.context.scene.cursor.location[1] = yValueC
                bpy.context.scene.cursor.location[2] = zValueC

                bpy.ops.object.select_all(action='DESELECT')
                CoCg = c01.constraints.new(type='CHILD_OF')
                CoCg.name = "childGridTarget"
                bpy.context.object.constraints[CoCg.name].target = bpy.data.objects[c03.name]
                CoCg.inverse_matrix = CoCg.target.matrix_world.inverted()

                bpy.ops.object.select_all(action='DESELECT')

        return {'FINISHED'}


class OBJECT_OT_OriginGridButton(bpy.types.Operator):
    bl_idname = "tkdw.origgrid"
    bl_label = ""
    bl_description = ""

    def execute(self, context):

        blockBool = False

        if (context.window_manager.orignGridState == 1) and (blockBool is False):
            context.window_manager.orignGridState = 2
            blockBool = True

        if (context.window_manager.orignGridState == 2) and (blockBool is False):
            context.window_manager.orignGridState = 3
            blockBool = True

        if (context.window_manager.orignGridState == 3) and (blockBool is False):
            context.window_manager.orignGridState = 4
            blockBool = True

        if (context.window_manager.orignGridState == 4) and (blockBool is False):
            context.window_manager.orignGridState = 1
            blockBool = True

        return {'FINISHED'}


class OBJECT_OT_CutDrawButton(bpy.types.Operator):
    bl_idname = "tkdw.cutdraw"
    bl_label = ""
    bl_description = ""

    def execute(self, context):

        blockBool = False

        if (context.window_manager.cutDrawState == 1) and (blockBool is False):
            context.window_manager.cutDrawState = 2
            blockBool = True

        if (context.window_manager.cutDrawState == 2) and (blockBool is False):
            context.window_manager.cutDrawState = 3
            blockBool = True

        if (context.window_manager.cutDrawState == 3) and (blockBool is False):
            context.window_manager.cutDrawState = 4
            blockBool = True

        if (context.window_manager.cutDrawState == 4) and (blockBool is False):
            context.window_manager.cutDrawState = 1
            blockBool = True

        return {'FINISHED'}


class OBJECT_OT_CutAddButton(bpy.types.Operator):
    bl_idname = "tkdw.cutadd"
    bl_label = "Apply cutting"
    bl_description = ""

    def execute(self, context):

        resultCut = not bpy.context.scene.Cutter is None
        resultCut = resultCut and (
            bpy.context.scene.Cutter.name in context.view_layer.objects)
        resultParts = not bpy.context.scene.Parts is None
        resultParts = resultParts and (
            bpy.context.scene.Parts.name in context.view_layer.objects)

        if (resultCut == True) and (resultParts == True):
            target_cut = bpy.context.scene.Cutter
            target_parts = bpy.context.scene.Parts

            bpy.ops.object.select_all(action='DESELECT')
            target_parts.select_set(state=True)
            bpy.context.view_layer.objects.active = target_parts

            if bpy.data.objects[target_parts.name].active_material is None:
                material_name = "PartsMaterial"
                materialParts = bpy.data.materials.get(material_name)
                if materialParts is None:
                    materialParts = bpy.data.materials.new(material_name)
                materialParts.use_nodes = True
                principled_bsdf = materialParts.node_tree.nodes.get(
                    'Principled BSDF')

                if principled_bsdf is not None:
                    principled_bsdf.inputs[0].default_value = (1, 1, 1, 1)
                    principled_bsdf.inputs[5].default_value = 0
                materialParts.name = "PartsMaterial_1"
                nameParts = bpy.context.active_object
                bpy.data.objects[nameParts.name].active_material = materialParts

            if target_cut != target_parts:
                bpy.ops.object.modifier_add(type='BOOLEAN')
                bpy.context.object.modifiers["Boolean"].object = bpy.data.objects[target_cut.name]
                bpy.context.object.modifiers["Boolean"].name = "cutParts_1"

                bpy.ops.object.select_all(action='DESELECT')
                target_cut.select_set(state=True)
                bpy.context.view_layer.objects.active = target_cut
                bpy.context.object.display_type = 'WIRE'
                bpy.context.object.hide_render = True
                OBJECT_OT_DrawPartsButton.refreshTextureCut(target_parts)

        return {'FINISHED'}


class OBJECT_OT_DrawPartsButton(bpy.types.Operator):
    bl_idname = "tkdw.drawparts"
    bl_label = "Paint cutter"
    bl_description = ""

    def execute(self, context):

        resultCut = not bpy.context.scene.Cutter is None
        resultCut = resultCut and (
            bpy.context.scene.Cutter.name in context.view_layer.objects)
        resultParts = not bpy.context.scene.Parts is None
        resultParts = resultParts and (
            bpy.context.scene.Parts.name in context.view_layer.objects)

        if resultCut == True:

            my_areas = bpy.context.workspace.screens[0].areas
            my_shading = 'MATERIAL'  # 'WIREFRAME' 'SOLID' 'MATERIAL' 'RENDERED'
            for area in my_areas:
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.shading.type = my_shading

            target_cut = bpy.context.scene.Cutter
            target_parts = bpy.context.scene.Parts
            bpy.ops.object.select_all(action='DESELECT')
            target_cut.select_set(state=True)
            bpy.context.view_layer.objects.active = target_cut
            context.window_manager.hideCutter = True
            bpy.context.object.hide_viewport = False

            colorDrawing = bpy.context.scene.cut_color
            hatchType = bpy.context.scene.hatch_type
            drawingType = context.window_manager.cutDrawState
            texturePath = bpy.context.scene.texture_path
            img_formats = True

            if (texturePath.split('.')[-1] != 'jpg') and (texturePath.split('.')[-1] != 'jepg') and (texturePath.split('.')[-1] != 'png') and (texturePath.split('.')[-1] != 'bmp'):
                bpy.context.scene.texture_path = "ERROR FORMAT FILE"
                img_formats = False

            if drawingType != 4:
                material_name = "CutMaterial"

                materialCut = bpy.data.materials.get(material_name)

                if materialCut is None:
                    materialCut = bpy.data.materials.new(material_name)

                materialCut.use_nodes = True

                principled_bsdf = materialCut.node_tree.nodes.get(
                    'Principled BSDF')

                if principled_bsdf is not None:
                    principled_bsdf.inputs[0].default_value = colorDrawing
                    principled_bsdf.inputs[5].default_value = 0

                if drawingType == 2:

                    colorRamp = materialCut.node_tree.nodes.new(
                        'ShaderNodeValToRGB')
                    if colorRamp is not None:
                        colorRamp.color_ramp.elements[0].position = 0.06
                        colorRamp.color_ramp.elements[1].position = 0.2

                    mapping = materialCut.node_tree.nodes.new(
                        'ShaderNodeMapping')

                    textureCoord = materialCut.node_tree.nodes.new(
                        'ShaderNodeTexCoord')

                    if hatchType == "Magic":
                        textureHatch = materialCut.node_tree.nodes.new(
                            'ShaderNodeTexMagic')
                        if textureHatch is not None:
                            textureHatch.inputs[1].default_value = 20.0
                            textureHatch.inputs[2].default_value = 8.0

                    if hatchType == "Musgrave":
                        textureHatch = materialCut.node_tree.nodes.new(
                            'ShaderNodeTexMusgrave')
                        if textureHatch is not None:
                            textureHatch.inputs[1].default_value = 30.0
                            textureHatch.inputs[2].default_value = 10.0
                            textureHatch.inputs[3].default_value = 0.1
                            textureHatch.inputs[4].default_value = 1.5

                    if hatchType == "Noise":
                        textureHatch = materialCut.node_tree.nodes.new(
                            'ShaderNodeTexNoise')
                        if textureHatch is not None:
                            textureHatch.inputs[1].default_value = 20.0
                            textureHatch.inputs[2].default_value = 3.5
                            textureHatch.inputs[3].default_value = 3.0
                        if colorRamp is not None:
                            colorRamp.color_ramp.elements[0].position = 0.465
                            colorRamp.color_ramp.elements[1].position = 0.535

                    if hatchType == "Voronoi":
                        textureHatch = materialCut.node_tree.nodes.new(
                            'ShaderNodeTexVoronoi')
                        if textureHatch is not None:
                            textureHatch.inputs[1].default_value = 60.0
                        if colorRamp is not None:
                            colorRamp.color_ramp.elements[0].position = 0.195
                            colorRamp.color_ramp.elements[1].position = 0.225

                    if hatchType == "Brick":
                        textureHatch = materialCut.node_tree.nodes.new(
                            'ShaderNodeTexBrick')
                        if textureHatch is not None:
                            textureHatch.inputs[4].default_value = 10.0
                            textureHatch.inputs[5].default_value = 0.015

                    if hatchType == "Wave":
                        textureHatch = materialCut.node_tree.nodes.new(
                            'ShaderNodeTexWave')
                        if textureHatch is not None:
                            textureHatch.inputs[1].default_value = 20.0

                    if hatchType == "Wave_distorded":
                        textureHatch = materialCut.node_tree.nodes.new(
                            'ShaderNodeTexWave')
                        if textureHatch is not None:
                            textureHatch.inputs[1].default_value = 10.0
                            textureHatch.inputs[2].default_value = 30.0
                            textureHatch.inputs[3].default_value = 2.0
                            textureHatch.inputs[4].default_value = 4.0

                    materialCut.node_tree.links.new(
                        colorRamp.outputs[0], principled_bsdf.inputs[0])
                    materialCut.node_tree.links.new(
                        textureHatch.outputs[0], colorRamp.inputs[0])
                    materialCut.node_tree.links.new(
                        mapping.outputs[0], textureHatch.inputs[0])
                    materialCut.node_tree.links.new(
                        textureCoord.outputs[2], mapping.inputs[0])

                    colorRamp.location = -300, 200
                    textureHatch.location = -500, 200
                    mapping.location = -900, 200
                    textureCoord.location = -1100, 200

                if (img_formats == True):
                    if drawingType == 3:
                        mapping = materialCut.node_tree.nodes.new(
                            'ShaderNodeMapping')

                        textureCoord = materialCut.node_tree.nodes.new(
                            'ShaderNodeTexCoord')

                        imageDraw = materialCut.node_tree.nodes.new(
                            'ShaderNodeTexImage')
                        if imageDraw is not None:
                            imageDraw.image = bpy.data.images.load(texturePath)

                        materialCut.node_tree.links.new(
                            imageDraw.outputs[0], principled_bsdf.inputs[0])
                        materialCut.node_tree.links.new(
                            mapping.outputs[0], imageDraw.inputs[0])
                        materialCut.node_tree.links.new(
                            textureCoord.outputs[2], mapping.inputs[0])

                        imageDraw.location = -300, 200
                        mapping.location = -700, 200
                        textureCoord.location = -900, 200

                materialCut.name = "CutMaterial_1"
                nameCut = bpy.context.active_object
                bpy.data.objects[nameCut.name].active_material = materialCut
                bpy.context.scene.texture_path = ""

            if drawingType == 4:
                bpy.ops.object.material_slot_remove()

            if(resultParts == True):
                OBJECT_OT_DrawPartsButton.refreshTextureCut(target_parts)

        return {'FINISHED'}

    def refreshTextureCut(objCut):

        # Selected object with modifiers
        object = objCut

        for modifier in object.modifiers:
            # Check if modifier is boolean AND has a boolean object selected
            if modifier.type == "BOOLEAN" and modifier.object:
                bo = modifier.object
                for mat in bo.data.materials:
                    object.data.materials.append(mat)

        return {'FINISHED'}


class OBJECT_OT_HideCutterButton(bpy.types.Operator):
    bl_idname = "tkdw.hidecutter"
    bl_label = ""
    bl_description = ""

    def execute(self, context):

        resultCut = not bpy.context.scene.Cutter is None
        resultCut = resultCut and (
            bpy.context.scene.Cutter.name in context.view_layer.objects)

        if resultCut == True:
            target_cut = bpy.context.scene.Cutter
            bpy.ops.object.select_all(action='DESELECT')
            target_cut.select_set(state=True)
            bpy.context.view_layer.objects.active = target_cut

            if context.window_manager.hideCutter is False:
                context.window_manager.hideCutter = True
                bpy.context.object.hide_viewport = False

            else:
                context.window_manager.hideCutter = False
                bpy.context.object.hide_viewport = True
            bpy.ops.object.select_all(action='DESELECT')

        return {'FINISHED'}


class OBJECT_OT_TDModeButton(bpy.types.Operator):
    bl_idname = "tkdw.tdmode"
    bl_label = "ON"
    bl_description = "Freestyle ON and World white"

    def execute(self, context):
        bpy.context.scene.render.use_freestyle = True

        bpy.context.scene.world.use_nodes = False
        bpy.context.scene.world.color = (1, 1, 1)

        bpy.context.scene.view_settings.view_transform = 'Standard'

        return {'FINISHED'}


class OBJECT_OT_TDModeOffButton(bpy.types.Operator):
    bl_idname = "tkdw.tdmodeoff"
    bl_label = "OFF"
    bl_description = "Freestyle OFF"

    def execute(self, context):
        bpy.context.scene.render.use_freestyle = False

        bpy.context.scene.world.use_nodes = True

        bpy.context.scene.view_settings.view_transform = 'Standard'

        return {'FINISHED'}


class OBJECT_OT_TDModeAddButton(bpy.types.Operator):
    bl_idname = "tkdw.tdmodeadd"
    bl_label = "Add line set"
    bl_description = "Line set"

    def execute(self, context):

        nameLineset = bpy.context.scene.lineset_name

        resultCollectionFree = not bpy.context.scene.CollectionFree is None

        visibilityEdges = context.window_manager.visibleLine

        thickness = bpy.context.scene.thickness_line

        colorLine = bpy.context.scene.line_color

        edgeMark = bpy.context.scene.edgemark_bool

        dashLine = bpy.context.scene.dashedline_bool

        dash_One = bpy.context.scene.dashOne

        gap_One = bpy.context.scene.gapOne

        if nameLineset == "":
            nameLineset = "TeckDraw"

        sceneF = bpy.context.scene
        view_layer = context.view_layer
        freestyle = view_layer.freestyle_settings

        linestyle = freestyle.linesets.new(nameLineset)

        if resultCollectionFree == True:
            target_free = bpy.context.scene.CollectionFree
            linestyle.select_by_collection = True
            linestyle.collection = target_free

        if visibilityEdges == True:
            linestyle.visibility = 'VISIBLE'
        else:
            linestyle.visibility = 'HIDDEN'

        if edgeMark == True:
            linestyle.select_silhouette = False
            linestyle.select_border = False
            linestyle.select_crease = False
            linestyle.select_edge_mark = True

        linestyle.linestyle.name = nameLineset

        linestyle.linestyle.thickness = thickness

        linestyle.linestyle.color = colorLine

        if dashLine == True:
            linestyle.linestyle.use_dashed_line = True
            linestyle.linestyle.dash1 = dash_One
            linestyle.linestyle.gap1 = gap_One

        linestyle.linestyle.caps = 'ROUND'

        bpy.context.scene.lineset_name = ""
        bpy.context.scene.CollectionFree = None
        context.window_manager.visibleLine = True
        bpy.context.scene.edgemark_bool = False
        bpy.context.scene.dashedline_bool = False

        nb_line = context.window_manager.nbLine + 1
        context.window_manager.nbLine = nb_line

        return {'FINISHED'}


class OBJECT_OT_TDModeVisibleButton(bpy.types.Operator):
    bl_idname = "tkdw.tdmodevisible"
    bl_label = ""
    bl_description = "Select visible or hidden feature edges"

    def execute(self, context):

        blockBool = False

        if (context.window_manager.visibleLine == True) and (blockBool is False):
            context.window_manager.visibleLine = False
            blockBool = True

        if (context.window_manager.visibleLine == False) and (blockBool is False):
            context.window_manager.visibleLine = True
            blockBool = True

        return {'FINISHED'}


class OBJECT_OT_DupliBoolButton(bpy.types.Operator):
    bl_idname = "tkdw.duplibool"
    bl_label = "Special duplicate"
    bl_description = "Duplicate and apply modifier"

    def execute(self, context):

        xValueC = bpy.context.scene.cursor.location[0]
        yValueC = bpy.context.scene.cursor.location[1]
        zValueC = bpy.context.scene.cursor.location[2]

        nbObj = len(bpy.context.selected_objects)

        dimX = 0.0

        if nbObj > 0:
            listObj = bpy.context.selected_objects
            bpy.ops.object.select_all(action='DESELECT')

            for o in listObj:
                if o.dimensions[0] > dimX:
                    dimX = o.dimensions[0]
                o.select_set(state=True)
                bpy.context.view_layer.objects.active = o

        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={
                                      "linked": False, "mode": 'TRANSLATION'}, TRANSFORM_OT_translate={"value": (xValueC, yValueC, zValueC)})

        bpy.ops.object.convert(target='MESH')

        return {'FINISHED'}


class OBJECT_OT_SnapPartsButton(bpy.types.Operator):
    bl_idname = "tkdw.snapparts"
    bl_label = "Special snap"
    bl_description = "Snapping with object reference"

    def execute(self, context):

        xValueC = bpy.context.scene.cursor.location[0]
        yValueC = bpy.context.scene.cursor.location[1]
        zValueC = bpy.context.scene.cursor.location[2]

        resultS1 = not bpy.context.scene.S1 is None
        resultS1 = resultS1 and (
            bpy.context.scene.S1.name in context.view_layer.objects)
        resultS2 = not bpy.context.scene.S2 is None
        resultS2 = resultS2 and (
            bpy.context.scene.S2.name in context.view_layer.objects)
        resultS3 = not bpy.context.scene.S3 is None
        resultS3 = resultS3 and (
            bpy.context.scene.S3.name in context.view_layer.objects)
        resultS4 = not bpy.context.scene.S4 is None
        resultS4 = resultS4 and (
            bpy.context.scene.S4.name in context.view_layer.objects)

        if (resultS1 == True) and (resultS2 == True) and (resultS3 == True) and (resultS4 == True):

            target_s1 = bpy.context.scene.S1
            target_s2 = bpy.context.scene.S2
            target_s3 = bpy.context.scene.S3
            target_s4 = bpy.context.scene.S4
            listObj = [target_s1, target_s2, target_s3, target_s4]
            nbObj = 4
            i = 1
            locObj1 = []
            locObj2 = []
            locObj3 = []
            locObj4 = []

            for o in listObj:
                bpy.ops.object.select_all(action='DESELECT')
                o.select_set(state=True)
                bpy.context.view_layer.objects.active = o
                bpy.ops.object.origin_set(
                    type='ORIGIN_GEOMETRY', center='MEDIAN')
                xmin = bpy.context.object.location[0]
                xmax = bpy.context.object.location[0]
                ymin = bpy.context.object.location[1]
                ymax = bpy.context.object.location[1]
                zmin = bpy.context.object.location[2]
                zmax = bpy.context.object.location[2]

                matrix = o.matrix_world
                vertObj = o.data.vertices

                for v in vertObj:
                    vPos = matrix@v.co
                    xV = vPos[0]
                    yV = vPos[1]
                    zV = vPos[2]
                    if xV < xmin:
                        xmin = xV
                    if xV > xmax:
                        xmax = xV
                    if yV < ymin:
                        ymin = yV
                    if yV > ymax:
                        ymax = yV
                    if zV < zmin:
                        zmin = zV
                    if zV > zmax:
                        zmax = zV

                if i == 1:
                    locObj1 = [xmin + ((xmax - xmin)/2), ymin +
                               ((ymax - ymin)/2), zmin + ((zmax - zmin)/2)]
                    bpy.context.scene.cursor.location[0] = xmin + \
                        ((xmax - xmin)/2)
                    bpy.context.scene.cursor.location[1] = ymin + \
                        ((ymax - ymin)/2)
                    bpy.context.scene.cursor.location[2] = zmin + \
                        ((zmax - zmin)/2)
                    bpy.ops.object.origin_set(
                        type='ORIGIN_CURSOR', center='MEDIAN')
                if i == 2:
                    locObj2 = [xmin + ((xmax - xmin)/2), ymin +
                               ((ymax - ymin)/2), zmin + ((zmax - zmin)/2)]
                    bpy.context.scene.cursor.location[0] = xmin + \
                        ((xmax - xmin)/2)
                    bpy.context.scene.cursor.location[1] = ymin + \
                        ((ymax - ymin)/2)
                    bpy.context.scene.cursor.location[2] = zmin + \
                        ((zmax - zmin)/2)
                    bpy.ops.object.origin_set(
                        type='ORIGIN_CURSOR', center='MEDIAN')
                if i == 3:
                    locObj3 = [xmin + ((xmax - xmin)/2), ymin +
                               ((ymax - ymin)/2), zmin + ((zmax - zmin)/2)]
                    bpy.context.scene.cursor.location[0] = xmin + \
                        ((xmax - xmin)/2)
                    bpy.context.scene.cursor.location[1] = ymin + \
                        ((ymax - ymin)/2)
                    bpy.context.scene.cursor.location[2] = zmin + \
                        ((zmax - zmin)/2)
                    bpy.ops.object.origin_set(
                        type='ORIGIN_CURSOR', center='MEDIAN')
                if i == 4:
                    locObj4 = [xmin + ((xmax - xmin)/2), ymin +
                               ((ymax - ymin)/2), zmin + ((zmax - zmin)/2)]
                    bpy.context.scene.cursor.location[0] = xmin + \
                        ((xmax - xmin)/2)
                    bpy.context.scene.cursor.location[1] = ymin + \
                        ((ymax - ymin)/2)
                    bpy.context.scene.cursor.location[2] = zmin + \
                        ((zmax - zmin)/2)
                    bpy.ops.object.origin_set(
                        type='ORIGIN_CURSOR', center='MEDIAN')
                    o.location[0] = locObj3[0] - (locObj1[0] - locObj2[0])
                    o.location[1] = locObj3[1] - (locObj1[1] - locObj2[1])
                    o.location[2] = locObj3[2] - (locObj1[2] - locObj2[2])

                i = i + 1

                bpy.context.scene.cursor.location[0] = xValueC
                bpy.context.scene.cursor.location[1] = yValueC
                bpy.context.scene.cursor.location[2] = zValueC

        return {'FINISHED'}


class OBJECT_OT_AddScaleButton(bpy.types.Operator):
    bl_idname = "tkdw.addscale"
    bl_label = ""
    bl_description = "Add new scale"

    type: bpy.props.StringProperty(
        default="",
        # options={'SKIP_SAVE'}
    )

    def execute(self, context):

        if self.type != '':
            prefs = bpy.context.preferences.addons[__package__].preferences
            path = prefs.pathTemplates
            scales_file = path + os.sep + 'Scales.txt'

            i = 0
            ls = []
            with open(scales_file, 'r') as f:
                for line in f:
                    vs = line.split(',')
                    ls.append((vs[0], vs[1], vs[2]))
                    i = + 1

            line = self.type

            verifLine = False
            index = 0
            while index < len(line):
                if line[index] == '/':
                    verifLine = True
                index = index + 1

            if verifLine == True:
                s = line.split('/')

                if (s[0].isdigit()) and (s[1].isdigit()):
                    v1 = str(1/(int(s[0])/int(s[1])))
                    v2 = str(int(s[0])/int(s[1]))
                    number_tuple = (v1, self.type, v2)

                    j = 1
                    cop = False
                    while j < len(ls):
                        if float(v1) <= float(ls[j][0]):
                            ls.insert(j, number_tuple)
                            cop = True
                            break
                        j = j + 1

                    if cop == False:
                        if float(v1) > float(ls[j-1][0]):
                            ls.append(number_tuple)

                    if (os.path.isfile(scales_file) == True):
                        file = open(scales_file, "w")
                        j = 0
                        while j < len(ls):
                            file.write(ls[j][0] + ',' + ls[j]
                                       [1] + ',' + ',' + '\n')
                            j = j + 1
                        file.close()

        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=200)

    def draw(self, context):
        row = self.layout
        row.label(text="New scale:")
        row.prop(self, "type", text="")
        row.separator()


class OBJECT_OT_RemoveScaleButton(bpy.types.Operator):
    bl_idname = "tkdw.removescale"
    bl_label = ""
    bl_description = "Remove scale"

    def execute(self, context):

        if (bpy.context.scene.custom_scale != '') and (bpy.context.scene.custom_scale != 'None'):
            prefs = bpy.context.preferences.addons[__package__].preferences
            path = prefs.pathTemplates
            scales_file = path + os.sep + 'Scales.txt'

            line = bpy.context.scene.custom_scale
            s = line.split('/')
            v1 = str(1/(int(s[0])/int(s[1])))
            v2 = str(int(s[0])/int(s[1]))

            with open(scales_file, "r+") as f:
                d = f.readlines()
                f.seek(0)
                for i in d:
                    if i.startswith(v1 + ',' + line) == False:
                        f.write(i)
                f.truncate()

            bpy.context.scene.custom_scale = 'None'

        return {'FINISHED'}


class OB_PT_LSToolsPanel(bpy.types.Panel):
    bl_label = "Parts Settings"
    bl_idname = "OB_PT_LSToolsPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "TechDraw"

    bpy.types.Scene.Target = PointerProperty(type=bpy.types.Object)

    bpy.types.Scene.Ref = PointerProperty(type=bpy.types.Object)

    bpy.types.Scene.Parts = PointerProperty(type=bpy.types.Object)

    bpy.types.Scene.Cutter = PointerProperty(type=bpy.types.Object)

    bpy.types.Scene.S1 = PointerProperty(type=bpy.types.Object)

    bpy.types.Scene.S2 = PointerProperty(type=bpy.types.Object)

    bpy.types.Scene.S3 = PointerProperty(type=bpy.types.Object)

    bpy.types.Scene.S4 = PointerProperty(type=bpy.types.Object)

    bpy.types.Scene.Update = PointerProperty(type=bpy.types.Object)

    bpy.types.Scene.lv_bool = BoolProperty(
        name="",
        description="Left view",
        default=False)

    bpy.types.Scene.rv_bool = BoolProperty(
        name="",
        description="Right view",
        default=False)

    bpy.types.Scene.bv_bool = BoolProperty(
        name="",
        description="Back view",
        default=False)

    bpy.types.Scene.fv_bool = BoolProperty(
        name="",
        description="Front view",
        default=False)

    bpy.types.Scene.uv_bool = BoolProperty(
        name="",
        description="Up view",
        default=False)

    bpy.types.Scene.dv_bool = BoolProperty(
        name="",
        description="Down view",
        default=False)

    bpy.types.Scene.ulv_bool = BoolProperty(
        name="",
        description="3d view",
        default=False)

    bpy.types.Scene.urv_bool = BoolProperty(
        name="",
        description="3d view",
        default=False)

    bpy.types.Scene.dlv_bool = BoolProperty(
        name="",
        description="3d view",
        default=False)

    bpy.types.Scene.drv_bool = BoolProperty(
        name="",
        description="3d view",
        default=False)

    bpy.types.Scene.draw_distance = FloatProperty(
        name="Draw Distance",
        description="Distance between view",
        min=0.0,
        default=1.0)

    bpy.types.Scene.cut_color = FloatVectorProperty(name="",
                                                    description="Color cut",
                                                    default=(
                                                        0.5, 0.5, 0.5, 1.0),
                                                    min=0.1,
                                                    max=1,
                                                    subtype='COLOR',
                                                    size=4)

    hatch_types = [("Wave", "Line", "", 0),
                   ("Wave_distorded", "Wave distorded", "", 1),
                   ("Magic", "Magic", "", 3),
                   ("Musgrave", "Musgrave", "", 4),
                   ("Noise", "Noise", "", 5),
                   ("Voronoi", "Voronoi", "", 6),
                   ("Brick", "Brick", "", 7)
                   ]

    bpy.types.Scene.hatch_type = bpy.props.EnumProperty(items=hatch_types,
                                                        name="",
                                                        default=hatch_types[0][0])

    bpy.types.Scene.texture_path = StringProperty(
        name="",
        subtype='FILE_PATH',
        description='Path to textures'
    )

    wm = WindowManager
    # register internal property
    wm.hideCages = BoolProperty(default=True)
    wm.hideCutter = BoolProperty(default=True)
    wm.checkAll = BoolProperty(default=False)
    wm.cutDrawState = IntProperty(default=1)

    def draw(self, context):

        layout = self.layout
        row = layout.row()
        col = row.column()
        col.label(text="Parts:", icon='MOD_ARRAY')
        col.prop(context.scene, "Target")
        row = layout.row()
        col = row.column()
        col.operator("tkdw.cageref", icon='OBJECT_DATA')
        row = layout.row()
        col = row.column()
        col.prop(context.scene, "Ref")

        if context.window_manager.hideCages is False:
            icon = 'HIDE_OFF'
            txt = 'Show Ref'
        else:
            icon = "HIDE_ON"
            txt = 'Hide Ref'

        row = layout.row()
        col = row.column()
        col.operator("tkdw.hidecage", text=txt, icon=icon)

        row = layout.row()
        col = row.column()
        col.separator()

        if context.window_manager.checkAll is False:
            icon = 'CHECKBOX_HLT'
            txt = 'Check All'
        else:
            icon = "CHECKBOX_DEHLT"
            txt = 'Uncheck All'

        row = layout.row()
        col = row.column()
        col.label(text="View:", icon='LIGHT_HEMI')
        col = row.column()
        col.operator("tkdw.checkall", text=txt, icon=icon)
        row = layout.row()
        col = row.column()
        col.prop(context.scene, "ulv_bool")
        col = row.column()
        col.prop(context.scene, "dv_bool")
        col = row.column()
        col.prop(context.scene, "urv_bool")

        row = layout.row()
        col = row.column()
        col.prop(context.scene, "rv_bool")
        col = row.column()
        col.prop(context.scene, "fv_bool")
        col = row.column()
        col.prop(context.scene, "lv_bool")
        col = row.column()
        col.prop(context.scene, "bv_bool")

        row = layout.row()
        col = row.column()
        col.prop(context.scene, "dlv_bool")
        col = row.column()
        col.prop(context.scene, "uv_bool")
        col = row.column()
        col.prop(context.scene, "drv_bool")
        row = layout.row()
        col = row.column()
        col.prop(context.scene, "draw_distance")
        row = layout.row()
        col = row.column()
        col.separator()
        col.operator("tkdw.apply", icon='ADD')
        col.operator("tkdw.multiadd", icon='RNA_ADD')
        row = layout.row()
        col = row.column()
        col.separator()
        col.prop(context.scene, "Update", text="Update")
        col.operator("tkdw.update", icon='FILE_REFRESH')
        row = layout.row()
        col = row.column()
        col.separator()
        col.operator("tkdw.duplibool", icon='DUPLICATE')
        row = layout.row()
        col = row.column()
        col.separator()

        row = layout.row()
        col = row.column()
        col.label(text="Group 1")
        col = row.column()
        col.label(text="Group 2")
        row = layout.row()
        col = row.column()
        col.prop(context.scene, "S1", text="")
        col = row.column()
        col.prop(context.scene, "S3", text="")
        row = layout.row()
        col = row.column()
        col.prop(context.scene, "S2", text="")
        col = row.column()
        col.prop(context.scene, "S4", text="")
        row = layout.row()
        col = row.column()
        col.operator("tkdw.snapparts", icon='SNAP_ON')

        row = layout.row()
        col = row.column()
        col.separator()
        col.label(text="Cutting:", icon='SELECT_SUBTRACT')
        row = layout.row()
        col = row.column()
        col.prop(context.scene, "Cutter")
        row = layout.row()
        col = row.column()
        col.label(text="Drawing types:")
        if context.window_manager.cutDrawState == 1:
            txt = 'Color'
        if context.window_manager.cutDrawState == 2:
            txt = 'Texture'
        if context.window_manager.cutDrawState == 3:
            txt = 'Image'
        if context.window_manager.cutDrawState == 4:
            txt = 'None'
        col.operator("tkdw.cutdraw", text=txt, icon='IMAGE')
        row = layout.row()
        col = row.column()
        if context.window_manager.cutDrawState == 1:
            col.prop(context.scene, "cut_color")
        if context.window_manager.cutDrawState == 2:
            col.prop(context.scene, "hatch_type")
        if context.window_manager.cutDrawState == 3:
            col.prop(context.scene, "texture_path")
        row = layout.row()
        col = row.column()
        col.operator("tkdw.drawparts", icon='BRUSH_DATA')
        row = layout.row()
        col = row.column()
        col.separator()
        row = layout.row()
        col = row.column()
        col.prop(context.scene, "Parts")
        row = layout.row()
        col = row.column()
        col.operator("tkdw.cutadd", icon='ADD')
        row = layout.row()
        col = row.column()
        if context.window_manager.hideCutter is False:
            icon = 'HIDE_OFF'
            txt = 'Show cutter'
        else:
            icon = "HIDE_ON"
            txt = 'Hide cutter'

        row = layout.row()
        col = row.column()
        col.operator("tkdw.hidecutter", text=txt, icon=icon)

    def execute(self, context):

        return {'FINISHED'}


class OB_PT_LSToolsPanelLayout(bpy.types.Panel):
    bl_label = "Layout Settings"
    bl_idname = "OB_PT_LSToolsPanelLayout"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "TechDraw"
    bl_options = {'DEFAULT_CLOSED'}

    bpy.types.Scene.Collection = PointerProperty(type=bpy.types.Collection)

    bpy.types.Scene.Sheets = PointerProperty(type=bpy.types.Object)

    bpy.types.Scene.Camera = PointerProperty(type=bpy.types.Object)

    bpy.types.Scene.Target_Table = PointerProperty(type=bpy.types.Object)

    bpy.types.Scene.Collection_Table = PointerProperty(
        type=bpy.types.Collection)

    format_types = [("A4", "A4", "", 0),
                    ("A3", "A3", "", 1),
                    ("A2", "A2", "", 2),
                    ("A1", "A1", "", 3),
                    ("A0", "A0", "", 4),
                    ("White", "White", "", 5)
                    ]

    bpy.types.Scene.format_type = bpy.props.EnumProperty(items=format_types,
                                                         name="Format",
                                                         default=format_types[1][0])

    orientation_types = [("Landscape", "Landscape", "", 0),
                         ("Portrait", "Portrait", "", 1)
                         ]

    bpy.types.Scene.orientation_type = bpy.props.EnumProperty(items=orientation_types,
                                                              name="Orientation",
                                                              default=orientation_types[0][0])

    cartridge_types = [("Type_1", "Type_1", "", 0),
                       ("Type_2", "Type_2", "", 1),
                       ("None", "None", "", 3)
                       ]

    bpy.types.Scene.cartridge_type = bpy.props.EnumProperty(items=cartridge_types,
                                                            name="Cartridge",
                                                            default=cartridge_types[0][0])

    bpy.types.Scene.x_Subdivisions = IntProperty(
        name="Column",
        description="X Subdivisions",
        min=1,
        default=3)

    bpy.types.Scene.y_Subdivisions = IntProperty(
        name="Line",
        description="Y Subdivisions",
        min=1,
        default=1)

    bpy.types.Scene.textGrid_bool = BoolProperty(
        name="Text in cells",
        description="Add text",
        default=False)

    wm = WindowManager
    # register internal property
    wm.orignGridState = IntProperty(default=1)

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        col = row.column()
        col.label(text="Camera:", icon='VIEW_CAMERA')
        row = layout.row()
        col = row.column()
        col.prop(context.scene, "Collection")
        row = layout.row()
        col = row.column()
        col.operator("tkdw.cam", icon='ADD')
        row = layout.row()
        col = row.column()
        col.separator()
        col.label(text="Sheets:", icon='RENDERLAYERS')
        col.prop(context.scene, "format_type")
        col.prop(context.scene, "orientation_type")
        col.prop(context.scene, "cartridge_type")
        row = layout.row()
        col = row.column()
        col.operator("tkdw.format", icon='ADD')
        row = layout.row()
        col = row.column()
        col.separator()
        col.label(text="Settings for render", icon='PREFERENCES')
        col.label(text="Choose:")
        col.prop(context.scene, "Sheets")
        col.prop(context.scene, "Camera")

        row = layout.row()
        col = row.column()
        col.prop(context.scene, "custom_scale", text="Scale")
        col = row.column()
        col.operator("tkdw.addscale", icon='ADD')
        col = row.column()
        col.operator("tkdw.removescale", icon='REMOVE')

        row = layout.row()
        col = row.column()
        col.operator("tkdw.sfrender", icon='SETTINGS')
        row = layout.row()
        col = row.column()
        col.separator()
        col.label(text="Table (Nomenclature)", icon='MESH_GRID')
        col.label(text="Subdivisions:")
        row = layout.row()
        col = row.column()
        col.prop(context.scene, "x_Subdivisions")
        col = row.column()
        col.prop(context.scene, "y_Subdivisions")
        row = layout.row()
        col = row.column()
        col.prop(context.scene, "textGrid_bool")
        row = layout.row()
        col = row.column()
        col.prop(context.scene, "Target_Table")
        col.prop(context.scene, "Collection_Table")
        row = layout.row()
        col = row.column()

        if context.window_manager.orignGridState == 1:
            txt = 'Orig: Right down'
        if context.window_manager.orignGridState == 2:
            txt = 'Orig: Left down'
        if context.window_manager.orignGridState == 3:
            txt = 'Orig: Right up'
        if context.window_manager.orignGridState == 4:
            txt = 'Orig: Left up'

        row = layout.row()
        col = row.column()
        col.operator("tkdw.origgrid", text=txt, icon='MOD_MESHDEFORM')
        row = layout.row()
        col = row.column()
        col.operator("tkdw.gridadd", icon='ADD')

    def execute(self, context):

        return {'FINISHED'}


class OB_PT_LSToolsPanelRender(bpy.types.Panel):
    bl_label = "Freestyle Settings"
    bl_idname = "OB_PT_LSToolsPanelRender"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "TechDraw"
    bl_options = {'DEFAULT_CLOSED'}

    bpy.types.Scene.CollectionFree = PointerProperty(type=bpy.types.Collection)

    bpy.types.Scene.edgemark_bool = BoolProperty(
        name="Edge Mark",
        description="Edge mark on",
        default=False)

    bpy.types.Scene.dashedline_bool = BoolProperty(
        name="Dashed Line",
        description="Dashed line on",
        default=False)

    bpy.types.Scene.lineset_name = StringProperty(
        name="Name",
        description='Path to textures'
    )

    bpy.types.Scene.thickness_line = FloatProperty(
        name="Thickness",
        description="Thickness line style",
        min=0.1,
        default=3.0)

    bpy.types.Scene.dashOne = IntProperty(
        name="D1",
        description="Thickness line style",
        min=0,
        default=0)

    bpy.types.Scene.gapOne = IntProperty(
        name="G1",
        description="Thickness line style",
        min=0,
        default=0)

    bpy.types.Scene.line_color = FloatVectorProperty(name="",
                                                     description="Color line",
                                                     default=(0.0, 0.0, 0.0),
                                                     min=0.1,
                                                     max=1,
                                                     subtype='COLOR',
                                                     size=3)

    wm = WindowManager
    # register internal property
    wm.visibleLine = BoolProperty(default=True)
    wm.nbLine = IntProperty(default=0)

    def draw(self, context):

        layout = self.layout
        row = layout.row()
        col = row.column()
        col.label(text="FreeStyle:", icon='MOD_WIREFRAME')
        row = layout.row()
        col = row.column()
        if bpy.context.scene.render.use_freestyle == False:
            col.operator("tkdw.tdmode", icon='RADIOBUT_ON')
        if bpy.context.scene.render.use_freestyle == True:
            col.operator("tkdw.tdmodeoff", icon='RADIOBUT_OFF')

        if bpy.context.scene.render.use_freestyle == True:
            row = layout.row()
            col = row.column()
            col.separator()
            col.label(text="Line settings:", icon='GREASEPENCIL')
            row = layout.row()
            col = row.column()
            col.prop(context.scene, "lineset_name")
            row = layout.row()
            col = row.column()
            col.prop(context.scene, "CollectionFree", text="Collection")
            row = layout.row()
            col = row.column()
            col.separator()
            if context.window_manager.visibleLine == True:
                txt = 'VISIBLE edges'
            if context.window_manager.visibleLine == False:
                txt = 'HIDDEN edges'
            col.operator("tkdw.tdmodevisible", text=txt, icon='CHECKBOX_HLT')

            row = layout.row()
            col = row.column()
            col.separator()
            col.prop(context.scene, "thickness_line")
            row = layout.row()
            col = row.column()
            col.prop(context.scene, "line_color", text="Base Color")
            row = layout.row()
            col = row.column()
            col.prop(context.scene, "edgemark_bool")
            row = layout.row()
            col = row.column()
            col.prop(context.scene, "dashedline_bool")
            row = layout.row()
            col = row.column()
            col.prop(context.scene, "dashOne")
            col = row.column()
            col.prop(context.scene, "gapOne")
            row = layout.row()
            col = row.column()
            col.separator()
            col.operator("tkdw.tdmodeadd", icon='ADD')
            row = layout.row()
            col = row.column()
            col.separator()
            txt = "Number line add: " + str(context.window_manager.nbLine)
            col.label(text=txt)

    def execute(self, context):

        return {'FINISHED'}


classes = [
    OBJECT_OT_ApplyButton,
    OBJECT_OT_UpdateButton,
    OBJECT_OT_AddCameraButton,
    OBJECT_OT_FormatButton,
    OBJECT_OT_SFRenderButton,
    OBJECT_OT_CageRefButton,
    OB_PT_LSToolsPanel,
    OB_PT_LSToolsPanelLayout,
    OB_PT_LSToolsPanelRender,
    OBJECT_OT_CheckAllButton,
    OBJECT_OT_HideCageButton,
    OBJECT_OT_MultiAddButton,
    OBJECT_OT_GridAddButton,
    OBJECT_OT_OriginGridButton,
    OBJECT_OT_CutDrawButton,
    OBJECT_OT_CutAddButton,
    OBJECT_OT_DrawPartsButton,
    OBJECT_OT_HideCutterButton,
    OBJECT_OT_TDModeButton,
    OBJECT_OT_TDModeOffButton,
    OBJECT_OT_TDModeAddButton,
    OBJECT_OT_TDModeVisibleButton,
    OBJECT_OT_DupliBoolButton,
    OBJECT_OT_SnapPartsButton,
    OBJECT_OT_AddScaleButton,
    OBJECT_OT_RemoveScaleButton,
]


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()
