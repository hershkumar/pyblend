import bpy # type: ignore
import os 

filename = "test.blend"


def setup_cycles():
    bpy.data.scenes["Scene"].render.engine = "CYCLES"

    bpy.context.scene.cycles.samples = 64  # Use lower samples (default is 128 or higher)
    bpy.context.scene.cycles.preview_samples = 16  # Reduce viewport samples for faster previews

    bpy.context.scene.cycles.use_denoising = True

    bpy.context.scene.cycles.max_bounces = 4  # Default is often 12
    bpy.context.scene.cycles.glossy_bounces = 2
    bpy.context.scene.cycles.transmission_bounces = 2

    bpy.context.scene.cycles.device = 'GPU'
    bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'METAL'


def setup():
    # see if the file already exists
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass

    # delete all objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    setup_cycles()



def render(fps, run_time, objects_list):
    frames = fps * run_time
    resolution = 1 / fps

    bpy.context.scene.render.fps = fps
    bpy.data.scenes["Scene"].frame_end = frames

    bpy.context.scene.frame_set(1)


    # create the objects
    for obje in objects:
        obj = obje.obj_dict
        if obj['shape'] == 'cube':
            bpy.ops.mesh.primitive_cube_add(location=obj['location'])
        elif obj['shape'] == 'sphere':
            bpy.ops.mesh.primitive_uv_sphere_add(location=obj['location'])

        bpy.context.object.name = obj['name']
        bpy.context.object.scale = obj['scale']
        bpy.context.object.rotation_euler = obj['rotation']

    # main render loop
    for i in range(1, frames + 1):
        print(f"Rendering frame {i} of {frames}")
        # set the frame number
        bpy.context.scene.frame_set(i)

        # do all the actual moving of objects here
        for obj in objects:
            obj.update(dtheta = (0.0, 0.0, 0.1))
            obj.get_object().keyframe_insert(data_path="rotation_euler", index=-1)

    # render to a file
    bpy.context.scene.frame_set(1)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(filename))



class Object:
    def __init__(self, name, shape, location, scale, rotation):
        self.name = name
        self.shape = shape
        self.location = location
        self.scale = scale
        self.rotation = rotation
        self.obj_dict = {'name': name, 'shape': shape, 'location': location, 'scale': scale, 'rotation': rotation}

    def __str__(self):
        return f"{self.name} is a {self.shape} at {self.location} with scale {self.scale} and rotation {self.rotation}"
    
    def __repr__(self): 
        return self.__str__()
    
    # returns the scene data
    def get_object(self):
        return bpy.data.objects[self.name]

    # lets you update the object in the scene
    def update(self, **kwargs): 
        d_loc = kwargs.get('dr', (0,0,0)) 
        d_rot = kwargs.get('dtheta', (0,0,0)) 
        d_scale = kwargs.get('dmag', (0,0,0)) 
        # move the object in the scene
        for i in range(3):
            bpy.data.objects[self.name].location[i] += d_loc[i]
            bpy.data.objects[self.name].rotation_euler[i] += d_rot[i]
            bpy.data.objects[self.name].scale[i] += d_scale[i]
        # update the object dictionary
        self.obj_dict['location'] = bpy.data.objects[self.name].location
        self.obj_dict['rotation'] = bpy.data.objects[self.name].rotation_euler
        self.obj_dict['scale'] = bpy.data.objects[self.name].scale


setup()

# test objects
objects = []

objects.append(Object('c1','cube',(0,0,0), (1,1,1), (0,0,0)))
objects.append(Object('c2','cube',(4,4,4), (1,1,1), (0,0,0)))
objects.append(Object('c3','sphere',(-4,-4,-4), (1,1,1), (0,0,0)))

render(60, 100, objects)
