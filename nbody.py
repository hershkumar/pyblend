# file that defines Euler/Runge-Kutta particle dynamics for the n-body problem
# the updates are then passed to the render.py file to render the scene


import numpy as np
from object import Object

NUM_BODIES = 10

# determine the initial conditions
def initial_conditions():
    # set the initial conditions
    # for now, just make them random
    objects = []
    for i in range(NUM_BODIES):
        name = f"body_{i}"
        shape = 'sphere'
        location = (np.random.uniform(-10, 10), np.random.uniform(-10, 10), np.random.uniform(-10,10))
        scale = (.5, .5, .5)
        rotation = (0, 0, 0)
        objects.append(Object(name, shape, location, scale, rotation))
    return objects
