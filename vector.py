import numpy as np

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

        self.length = np.sqrt(self.x**2 + self.y**2 + self.z**2)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def to_list(self):
        return [self.x, self.y, self.z]
    
    def __repr__(self):
        return f"Vector(x={self.x}, y={self.y}, z={self.z})"
    
    def __str__(self):
        return f"({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"