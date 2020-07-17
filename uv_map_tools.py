# ### BEGIN GPL LICENSE BLOCK ###
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ### END GPL LICENSE BLOCK ###

import bpy
from bpy.types import Operator

bl_info = {
    "name": "UV Tools",
    "author": "Jake Dube, cdeguise, bovesan",
    "version": (1, 1),
    "blender": (2, 80, 0),
    "location": "UV maps in properties window",
    "description": "Some tools for uv maps that should already be in Blender.",
    "category": "UV"}


def make_active(name):
    uvs = bpy.context.view_layer.objects.active.data.uv_layers
    for uv in uvs:
        if uv.name == name:
            uvs.active = uv
            return
    print("Could not find:", name, "\n(this should never happen)")


def move_to_bottom(index):
#    uvs = bpy.context.scene.objects.active.data.uv_textures
    uvs = bpy.context.view_layer.objects.active.data.uv_layers
    uvs.active_index = index
    new_name = uvs.active.name

    bpy.ops.mesh.uv_texture_add()

    # delete the "old" one
    make_active(new_name)
    bpy.ops.mesh.uv_texture_remove()

    # set the name of the last one
    uvs.active_index = len(uvs) - 1
    uvs.active.name = new_name


class MoveUVMapDown(Operator):
    bl_idname = "uv_tools.move_uvmap_down"
    bl_label = "Move Down"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        uvs = context.view_layer.objects.active.data.uv_layers

        # get the selected UV map
        orig_ind = uvs.active_index
        orig_name = uvs.active.name

        if orig_ind == len(uvs) - 1:
            return {'FINISHED'}

        # use "trick" on the one after it
        move_to_bottom(orig_ind + 1)

        # use the "trick" on the UV map
        move_to_bottom(orig_ind)

        # use the "trick" on the rest that are after where it was
        for i in range(orig_ind, len(uvs) - 2):
            move_to_bottom(orig_ind)

        make_active(orig_name)

        return {'FINISHED'}


class MoveUVMapUp(Operator):
    bl_idname = "uv_tools.move_uvmap_up"
    bl_label = "Move Up"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        uvs = bpy.context.view_layer.objects.active.data.uv_layers

        if uvs.active_index == 0:
            return {'FINISHED'}

        original = uvs.active.name
        uvs.active_index -= 1
        bpy.ops.uv_tools.move_uvmap_down()
        make_active(original)

        return {'FINISHED'}


def uv_tools_addition(self, context):
    layout = self.layout
    col = layout.column(align=True)
    col.operator("uv_tools.move_uvmap_up", icon='TRIA_UP')
    col.operator("uv_tools.move_uvmap_down", icon='TRIA_DOWN')


def register():
    bpy.utils.register_class(MoveUVMapDown)
    bpy.utils.register_class(MoveUVMapUp)
    bpy.types.DATA_PT_uv_texture.append(uv_tools_addition)


def unregister():
    bpy.utils.unregister_class(MoveUVMapDown)
    bpy.utils.unregister_class(MoveUVMapUp)
    bpy.types.DATA_PT_uv_texture.remove(uv_tools_addition)


if __name__ == "__main__":
    register()
