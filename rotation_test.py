from vector import Vector
import numpy as np

pi = np.pi

vec1 = Vector(1, 0, 0)

rx = -1.216
ry = 1.205 
rz = -1.209

vec2 = vec1.rotate(rx, ry, rz)

print(vec1)
print(vec2)

rx = 2.43
ry = -2.408
rz = 2.415