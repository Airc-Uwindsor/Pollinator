from vector import Vector
import numpy as np

pi = np.pi

goal = Vector(
    0.12,
    -0.0325,
    -0.08
)

current = Vector(
    0.0325,
    0.08,
    0.12
)

rx = -1.216
ry = 1.205 
rz = -1.209

rotation_vector = Vector(rx, ry, rz)

print(f'Goal: {goal}')
print(f'Current: {current}')

goal = goal.undo_rotate(rotation_vector)
print(f'Goal: {goal}')