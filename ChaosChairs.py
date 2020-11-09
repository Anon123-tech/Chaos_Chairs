import bpy
from math import radians
import random
from bpy.props import *

class ChaosChairs(bpy.types.Operator):
    """Pure Chaos"""
    bl_idname = "object.chaoschairs"
    bl_label = "Chaos Chairs"
    bl_options = {'REGISTER', 'UNDO'}
    
    #Create Properties
    rand_seed : FloatProperty(
        name = "Seed",
        description = "The random seed value",
        default = 0,
        min = 0,
        max = 999999999999999999
    )
    
    iterations : IntProperty(
        name = "Iterations",
        description = "The number of chairs",
        default = 1,
        min = 1,
        max = 2000
    ) 

    def execute(self, context):
        
        #Delete previous try

        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()



        #Add Chair Seat

        bpy.ops.mesh.primitive_plane_add(size=0.4, enter_editmode=True, location=(0, 0, 0.45))
        so = bpy.context.active_object
        verts = so.data.vertices

        #Select vertices where Y>0

        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.editmode_toggle()

        for v in verts:
            if v.co[1] > 0:
                v.select = True
            else:
                v.select = False

        #Make rear narrow and subdivide

        bpy.ops.object.editmode_toggle()
        bpy.ops.transform.resize(value=(0.8, 0.8, 0.8))
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.subdivide(number_cuts=2)
        bpy.ops.object.editmode_toggle()

        #Add Modifiers

        bpy.ops.object.modifier_add(type='SUBSURF')
        bpy.context.object.modifiers["Subdivision"].levels = 2

        bpy.ops.object.modifier_add(type='SOLIDIFY')
        bpy.context.object.modifiers["Solidify"].thickness = 0.025

        bpy.ops.object.modifier_add(type='BEVEL')
        bpy.context.object.modifiers["Bevel"].width = 0.003



        #Adding Legs

        bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.01, depth=0.44, enter_editmode=True, location=(0, 0, 0.22))
        bpy.ops.mesh.subdivide(number_cuts=1, smoothness=0.06)

        #move leg
        bpy.ops.mesh.duplicate_move(MESH_OT_duplicate={"mode":1}, TRANSFORM_OT_translate={"value":(0.15, 0.15, 0)})
        bpy.ops.transform.rotate(value=0.10472, orient_axis='X', orient_type='GLOBAL')
        bpy.ops.transform.rotate(value=-0.10472, orient_axis='Y', orient_type='GLOBAL')

        #make cross rail
        bpy.ops.mesh.select_all(action='INVERT')
        bpy.ops.transform.resize(value=(0.67, 0.67, 0.67))
        bpy.ops.transform.rotate(value=1.5708, orient_axis='Y', orient_type='GLOBAL')

        #make side rail
        bpy.ops.mesh.duplicate_move(MESH_OT_duplicate={"mode":1}, TRANSFORM_OT_translate={"value":(0.15, 0, 0)})
        bpy.ops.transform.rotate(value=1.5708, orient_axis='Z', orient_type='GLOBAL')
        bpy.ops.object.editmode_toggle()

        #shade smooth
        bpy.ops.object.shade_smooth()
        bpy.context.object.data.use_auto_smooth = True
        bpy.context.object.data.auto_smooth_angle = radians(80)

        #mirror
        bpy.ops.object.modifier_add(type='MIRROR')
        bpy.context.object.modifiers["Mirror"].use_axis[1] = True
        bpy.context.object.modifiers["Mirror"].use_bisect_axis[0] = True
        bpy.context.object.modifiers["Mirror"].use_bisect_axis[1] = True



        #Adding Back

        bpy.ops.mesh.primitive_cylinder_add(vertices=5, radius=0.012, depth=0.3, enter_editmode=True, location=(0, 0.15, 0.59))
        bpy.ops.transform.translate(value=(0.15, 0, 0))
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.editmode_toggle()

        for v in bpy.context.active_object.data.vertices:
            if v.co[2] > 0:
                v.select = True
            else:
                v.select = False
                
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.spin(angle=-1.7, center=(0, 0, 0.73), axis=(0, -1, 0))
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.transform.rotate(value=-0.1, orient_axis='X', orient_type='GLOBAL')
        bpy.ops.transform.rotate(value=0.05, orient_axis='Y', orient_type='GLOBAL')
        bpy.ops.object.editmode_toggle()

        #shade smooth
        bpy.ops.object.shade_smooth()
        bpy.context.object.data.use_auto_smooth = True
        bpy.context.object.data.auto_smooth_angle = radians(30)

        #mirror
        bpy.ops.object.modifier_add(type='MIRROR')
        bpy.context.object.modifiers["Mirror"].use_bisect_axis[0] = True



        #Add Spindles
        bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.005, depth=0.44, enter_editmode=True, location=(0, 0.17, 0.66))
        bpy.ops.transform.translate(value=(0.025, 0, 0))
        bpy.ops.mesh.duplicate_move(MESH_OT_duplicate={"mode":1}, TRANSFORM_OT_translate={"value":(0.05, 0, 0)})
        bpy.ops.transform.resize(value=(1, 1, 0.9))
        bpy.ops.transform.rotate(value=0.03, orient_axis='Y', orient_type='GLOBAL')
        bpy.ops.mesh.duplicate_move(MESH_OT_duplicate={"mode":1}, TRANSFORM_OT_translate={"value":(0.05, -0.005, 0)})
        bpy.ops.transform.resize(value=(1, 1, 0.75))
        bpy.ops.transform.rotate(value=0.03, orient_axis='Y', orient_type='GLOBAL')

        #Straighten base
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.editmode_toggle()

        for v in bpy.context.active_object.data.vertices:
            if v.co[2] < 0:
                v.select = True
            else:
                v.select = False

        bpy.ops.object.editmode_toggle()
        bpy.ops.transform.resize(value=(1, 1, 0))
        bpy.ops.transform.translate(value=(0, 0, -0.035))
        bpy.ops.object.editmode_toggle()

        #shade smooth
        bpy.ops.object.shade_smooth()
        bpy.context.object.data.use_auto_smooth = True
        bpy.context.object.data.auto_smooth_angle = radians(80)

        #mirror
        bpy.ops.object.modifier_add(type='MIRROR')



        #Apply Modifiers and Join
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.convert(target='MESH')

        bpy.ops.object.join()
        
        
        #Add a Material
        new_mat = bpy.data.materials.new(name = "ChaosChair")
        bpy.context.active_object.data.materials.append(new_mat)
        new_mat.use_nodes = True
        nodes = new_mat.node_tree.nodes
                
        material_output = nodes.get("Material Output")
        node_diffuse = nodes.new(type = 'ShaderNodeBsdfDiffuse')
        
        node_diffuse.inputs[0].default_value = (0.01, 0.005, 0.005, 1)
        node_diffuse.inputs[1].default_value = (0.3)
        
        links = new_mat.node_tree.links
        new_link = links.new(node_diffuse.outputs[0], material_output.inputs[0])

                

        #Rename to Chair
        bpy.context.object.name = "ChaosChair"

        #Set Origin to base
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

        #Set Rigid Body
        bpy.ops.rigidbody.objects_add(type='ACTIVE')



        #Duplicate (seed 'a' is variable, range(x) is variable)
        random.seed(a=self.rand_seed, version=2)
        for i in range(self.iterations-1):
            randList = (random.sample(range(-20,20), 4))
            randListZ = (random.sample(range(0,20), 1))
            bpy.ops.object.duplicate_move_linked(OBJECT_OT_duplicate={"linked":True}, TRANSFORM_OT_translate={"value":(randList[0]/10, randList[1]/10, randListZ[0]/100)})
            bpy.ops.transform.trackball(value=(randList[2]/10, randList[3]/10))


        #Go to start 
        bpy.ops.screen.frame_jump(end=False)
        
        return {'FINISHED'}


def register():
    bpy.utils.register_class(ChaosChairs)


def unregister():
    bpy.utils.unregister_class(ChaosChairs)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.chaoschairs()
