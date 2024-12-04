import bpy


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
    # can change the position, rotation, and scale of the object
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

